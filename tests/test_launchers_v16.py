"""Local-only launcher regressions; no providers, downloads, uploads or tasks."""
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASH = shutil.which('bash') or '/bin/bash'


class V16LauncherTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='v16-shell-')
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.root = self.base / 'academy with spaces'
        self.root.mkdir()
        self.bin = self.base / 'bin'
        self.bin.mkdir()
        self.log = self.base / 'commands.log'
        for name in ('macgyver.sh', 'upload-all.sh', 'run-local.sh',
                     'run-ai-local.sh', 'run-ai-cloud.sh', 'run-ai-gemini.sh',
                     'run-ai-llamacpp.sh'):
            shutil.copy2(ROOT / name, self.root / name)
        for name in ('bash', 'dirname', 'cat'):
            (self.bin / name).symlink_to(shutil.which(name))
        self.env = {'PATH': str(self.bin), 'HOME': str(self.base),
                    'SHELL_TEST_LOG': str(self.log), 'GEMINI_API_KEY': 'fixture-only'}
        self.python = self.make_python(self.base / 'chosen Python/python', 'chosen')
        self.env['MACGYVER_PYTHON'] = str(self.python)
        portable = self.root / 'portable'
        portable.mkdir()
        (portable / '__init__.py').touch()
        (portable / 'server.py').write_text(
            'def read_dotenv(path): pass\n'
            'def ai_routes(): return [{"id": "fixture-route"}]\n')
        record = ('import json,os,sys\n'
                  'print(json.dumps({"args":sys.argv[1:],'
                  '"python":os.environ.get("MACGYVER_PYTHON")}))\n')
        (portable / 'launch_v16.py').write_text(record)
        for name in ('Upload_MacGyver_v16_SSH.sh', 'macgyver-legacy-v15.sh'):
            (self.root / name).write_text(
                '#!/usr/bin/env bash\n'
                'exec "$MACGYVER_PYTHON" "$(dirname "$0")/portable/launch_v16.py" "$@"\n')

    def make_python(self, path, label, valid=True):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text('#!/bin/sh\n'
                        f'printf "{label}: %s\\n" "$*" >> "$SHELL_TEST_LOG"\n' +
                        (f'exec {shlex.quote(sys.executable)} "$@"\n' if valid else 'exit 1\n'))
        path.chmod(0o755)
        return path

    def run_script(self, name, *args):
        return subprocess.run([BASH, str(self.root / name), *args],
                              env=self.env, cwd=self.root, text=True,
                              capture_output=True, timeout=15)

    def output(self, result):
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return json.loads(result.stdout.splitlines()[-1])

    def commands(self):
        return self.log.read_text() if self.log.exists() else ''

    def test_default_and_compatibility_aliases_forward_to_v16(self):
        self.assertEqual(self.output(self.run_script('macgyver.sh'))['args'], [])
        for command in ('upload', 'deploy', 'all'):
            with self.subTest(command=command):
                args = ['--dry-run', '--documents-dir', '/a path/學習文件']
                self.assertEqual(self.output(self.run_script('macgyver.sh', command, *args))['args'], args)
        self.assertEqual(self.output(self.run_script('upload-all.sh', '--skip-data', '--skip-models'))['args'],
                         ['--skip-data', '--skip-models'])
        self.assertEqual(self.output(self.run_script('macgyver.sh', '--dry-run'))['args'], ['--dry-run'])

    def test_compare_forces_dry_run_and_serve_forwards(self):
        self.assertEqual(self.output(self.run_script('macgyver.sh', 'compare', '--skip-models'))['args'],
                         ['--dry-run', '--skip-models'])
        self.assertEqual(self.output(self.run_script('macgyver.sh', 'serve', '--port', '8123'))['args'],
                         ['--port', '8123'])

    def test_legacy_commands_are_explicit_and_unknown_commands_fail(self):
        for command in ('doctor', 'config', 'models', 'models-compare', 'restore-models', 'stocks', 'schedule', 'unschedule'):
            with self.subTest(command=command):
                result = self.run_script('macgyver.sh', command, 'fixture')
                self.assertEqual(self.output(result)['args'], [command, 'fixture'])
                self.assertIn('Legacy V15 advanced command', result.stderr)
        self.log.unlink()
        result = self.run_script('macgyver.sh', 'misspelled-command')
        self.assertEqual(result.returncode, 2)
        self.assertEqual(self.commands(), '')

    def test_help_requires_no_python_models_or_credentials(self):
        self.env.pop('GEMINI_API_KEY')
        self.env['MACGYVER_PYTHON'] = '/nonexistent/python'
        self.env['CONDA_PREFIX'] = '/nonexistent/conda'
        for name in ('macgyver.sh', 'run-ai-local.sh', 'run-ai-cloud.sh', 'run-ai-gemini.sh', 'run-ai-llamacpp.sh'):
            with self.subTest(script=name):
                result = self.run_script(name, '--help')
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn('Usage: bash ', result.stdout)
        self.assertEqual(self.commands(), '')

    def test_cloud_and_gemini_explicit_python_wins_and_is_reused(self):
        conda = self.base / 'Conda environment'
        self.make_python(conda / 'bin/python', 'conda')
        self.make_python(self.bin / 'python3', 'path')
        self.env['CONDA_PREFIX'] = str(conda)
        for name in ('run-ai-cloud.sh', 'run-ai-gemini.sh'):
            with self.subTest(script=name):
                data = self.output(self.run_script(name, '--port', '8123'))
                self.assertEqual(data['python'], str(self.python))
                self.assertEqual(data['args'], ['--port', '8123'])
        self.assertNotIn('conda:', self.commands())
        self.assertNotIn('path:', self.commands())
        self.assertGreaterEqual(self.commands().count('chosen: - '), 2)

    def test_cloud_and_gemini_conda_path_with_spaces_wins_over_old_python(self):
        self.env.pop('MACGYVER_PYTHON')
        conda = self.base / 'Conda environment with spaces'
        chosen = self.make_python(conda / 'bin/python', 'conda')
        self.make_python(self.bin / 'python3', 'old-path', valid=False)
        self.env['CONDA_PREFIX'] = str(conda)
        for name in ('run-ai-cloud.sh', 'run-ai-gemini.sh'):
            with self.subTest(script=name):
                self.assertEqual(self.output(self.run_script(name))['python'], str(chosen))
        self.assertNotIn('old-path:', self.commands())

    def test_local_empty_arguments_and_spaced_arguments_do_not_download(self):
        ollama = self.bin / 'ollama'
        ollama.write_text('#!/bin/sh\n'
                          'printf "ollama: %s\\n" "$*" >> "$SHELL_TEST_LOG"\n'
                          'case "$1" in list|show) exit 0;; *) exit 99;; esac\n')
        ollama.chmod(0o755)
        self.assertEqual(self.output(self.run_script('run-ai-local.sh'))['args'], [])
        self.assertEqual(self.output(self.run_script('run-ai-local.sh', '--both', '--fixture', 'a path/教材'))['args'],
                         ['--fixture', 'a path/教材'])
        self.assertIn('ollama: show qwen3:4b', self.commands())
        self.assertIn('ollama: show qwen3-vl:2b', self.commands())
        self.assertNotIn('ollama: pull', self.commands())
        self.assertIn('${SERVER_ARGS[@]+"${SERVER_ARGS[@]}"}',
                      (ROOT / 'run-ai-local.sh').read_text())

    def test_root_shell_syntax(self):
        for path in ROOT.glob('*.sh'):
            with self.subTest(script=path.name):
                result = subprocess.run([BASH, '-n', str(path)], capture_output=True, text=True, timeout=10)
                self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == '__main__':
    unittest.main()
