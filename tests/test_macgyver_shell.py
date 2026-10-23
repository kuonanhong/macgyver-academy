"""Offline launcher regressions: interpreter selection and fail-before-upload.

All Git, SSH and Node commands are local fixtures. Valid Python wrappers only
run the model-manifest inventory; no model download or repository is contacted.
"""
import json
import os
import re
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import tempfile
import unittest


SOURCE = Path(__file__).resolve().parents[1]
BASH = shutil.which('bash') or '/bin/bash'


class MacGyverShellTests(unittest.TestCase):
    def test_unicode_display_text_does_not_extend_variable_names(self):
        # Older locale-sensitive shells can treat a following UTF-8 byte as
        # part of the name. Braces establish a portable boundary.
        ambiguous = re.compile(r'\$[A-Za-z_][A-Za-z_0-9]*(?=[^\x00-\x7f])')
        for script in SOURCE.glob('*.sh'):
            with self.subTest(script=script.name):
                self.assertIsNone(ambiguous.search(script.read_text('utf-8')))

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='macgyver-shell-')
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.root = self.base / 'academy with spaces'
        self.root.mkdir()
        self.bin = self.base / 'fixture-bin'
        self.bin.mkdir()
        self.log = self.base / 'commands.log'
        self.conf = self.base / 'settings.conf'
        for name in ('macgyver.sh', 'macgyver-legacy-v15.sh', 'upload-all.sh', 'Upload_MacGyver_v16_SSH.sh'):
            shutil.copy2(SOURCE / name, self.root / name)
        (self.root / 'tools').mkdir()
        (self.root / 'tools/model-manifest.json').write_text(json.dumps({
            'models': [{'id': 'fixture-model', 'label': 'Fixture model',
                        'file': 'sample.gguf', 'bytes': 4}]
        }))
        for name in ('dirname', 'grep'):
            executable = shutil.which(name)
            self.assertIsNotNone(executable)
            (self.bin / name).symlink_to(executable)
        (self.bin / 'bash').symlink_to(BASH)
        self.command('git', '''case "$1" in
config) printf 'Fixture identity\\n' ;;
ls-remote) exit 0 ;;
*) printf 'Unexpected Git command\\n' >&2; exit 98 ;;
esac
''')
        self.command('ssh', '''printf "Hi fixture! You have successfully authenticated, but GitHub does not provide shell access.\\n"
exit 1
''')
        self.command('node', '''if [ "$1" = --version ]; then printf 'v22.13.0\\n'; else exit 98; fi
''')
        self.write_conf()
        self.env = {key: value for key, value in os.environ.items()
                    if key not in ('MACGYVER_PYTHON', 'CONDA_PREFIX', 'MACGYVER_CONF', 'BASH_ENV', 'ENV')}
        self.env.update(PATH=str(self.bin), MACGYVER_CONF=str(self.conf),
                        SHELL_TEST_COMMAND_LOG=str(self.log))

    def command(self, name, body):
        destination = self.bin / name
        destination.write_text('#!/bin/sh\n'
                               f'printf "{name}: %s\\n" "$*" >> "$SHELL_TEST_COMMAND_LOG"\n' + body)
        destination.chmod(0o755)
        return destination

    def python(self, destination, label, supported=True):
        destination.parent.mkdir(parents=True, exist_ok=True)
        body = ('#!/bin/sh\n'
                f'printf "{label}: %s\\n" "$*" >> "$SHELL_TEST_COMMAND_LOG"\n')
        if supported:
            body += f'exec {shlex.quote(sys.executable)} "$@"\n'
        else:
            body += 'if [ "$1" = --version ]; then printf "Python 3.9.20\\n"; exit 0; fi\nexit 1\n'
        destination.write_text(body)
        destination.chmod(0o755)
        return destination

    def write_conf(self, model_dir=None):
        values = {
            'SITE_REPO': 'git@github.com:fixture/site.git',
            'MODELS_REPO': 'git@github.com:fixture/models.git',
        }
        if model_dir is not None:
            values['MODEL_DIR'] = str(model_dir)
        self.conf.write_text(''.join(f'{key}={shlex.quote(value)}\n' for key, value in values.items()))

    def run_script(self, *arguments, script='macgyver.sh'):
        return subprocess.run([BASH, str(self.root / script), *arguments],
                              cwd=self.root, env=self.env, text=True,
                              capture_output=True, timeout=10)

    def commands(self):
        return self.log.read_text() if self.log.exists() else ''

    def assert_no_empty_command(self, result):
        self.assertNotIn('command not found', result.stderr)
        self.assertNotIn('指令找不到', result.stderr)

    def assert_no_upload(self):
        commands = self.commands()
        for marker in ('sync_github.py', 'models_sync.py', 'update_markets.py', 'git: push', 'git: clone', 'git: fetch'):
            self.assertNotIn(marker, commands)

    def test_doctor_without_python_reports_requirement_without_empty_command(self):
        result = self.run_script('doctor')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('缺少 Python 3.10+', result.stderr)
        self.assert_no_empty_command(result)
        self.assert_no_upload()

    def test_doctor_rejects_simulated_python_39(self):
        self.python(self.bin / 'python3', 'python39', supported=False)
        result = self.run_script('doctor')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('缺少 Python 3.10+', result.stderr)
        self.assertIn('python39: -c', self.commands())
        self.assertNotIn('python39: - ', self.commands())
        self.assert_no_empty_command(result)

    def test_conda_python_with_spaces_wins_over_older_path_python(self):
        self.python(self.bin / 'python3', 'path39', supported=False)
        conda = self.base / 'Conda environment with spaces'
        interpreter = self.python(conda / 'bin/python', 'conda-valid')
        self.env['CONDA_PREFIX'] = str(conda)
        result = self.run_script('doctor')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(str(interpreter), result.stdout)
        self.assertIn('conda-valid: - ', self.commands())
        self.assertNotIn('path39:', self.commands())
        self.assert_no_empty_command(result)

    def test_macgyver_python_takes_priority_over_conda_and_path(self):
        self.python(self.bin / 'python3', 'path-valid')
        conda = self.base / 'Conda env'
        self.python(conda / 'bin/python', 'conda-valid')
        explicit = self.python(self.base / 'chosen Python/bin/python', 'explicit-valid')
        self.env.update(CONDA_PREFIX=str(conda), MACGYVER_PYTHON=str(explicit))
        result = self.run_script('doctor')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(str(explicit), result.stdout)
        self.assertIn('explicit-valid: - ', self.commands())
        self.assertNotIn('conda-valid:', self.commands())
        self.assertNotIn('path-valid:', self.commands())

    def test_doctor_uses_configured_model_directory(self):
        self.python(self.bin / 'python3', 'path-valid')
        models = self.base / 'custom models with spaces'
        models.mkdir()
        (models / 'sample.gguf').write_bytes(b'GGUF')
        self.write_conf(model_dir=models)
        result = self.run_script('doctor')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('✓ fixture-model', result.stdout)
        self.assertIn('本機檔案存在', result.stdout)
        self.assertFalse((self.root / 'models/sample.gguf').exists())

    def test_deploy_without_python_stops_before_sync(self):
        result = self.run_script('deploy')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('需要 Python 3.10+', result.stderr)
        self.assert_no_empty_command(result)
        self.assertEqual(self.commands(), '')
        self.assert_no_upload()

    def test_upload_all_without_python_stops_before_sync(self):
        result = self.run_script('--skip-data', '--skip-models', script='upload-all.sh')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('需要 Python 3.10+', result.stderr)
        self.assert_no_empty_command(result)
        self.assertEqual(self.commands(), '')
        self.assert_no_upload()


if __name__ == '__main__':
    unittest.main()
