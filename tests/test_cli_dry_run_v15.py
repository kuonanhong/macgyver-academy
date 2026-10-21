"""Real V15 launchers against local bare Git, without external uploads or rebuilds."""
import hashlib
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
GIT = shutil.which('git')
BASH = shutil.which('bash')

class LauncherDryRunTests(unittest.TestCase):
    def test_doctor_and_upload_dry_run_preserve_remote_and_generated_assets(self):
        with tempfile.TemporaryDirectory(prefix='macgyver-v15-cli-') as directory:
            temp = Path(directory)
            remote = temp / 'remote.git'
            seed = temp / 'seed'
            state = temp / 'state'
            models = temp / 'models with spaces'
            models.mkdir()
            seed.mkdir()
            env = dict(os.environ, GIT_AUTHOR_NAME='Fixture', GIT_AUTHOR_EMAIL='fixture@example.org',
                       GIT_COMMITTER_NAME='Fixture', GIT_COMMITTER_EMAIL='fixture@example.org',
                       GIT_ALLOW_PROTOCOL='file', MACGYVER_SYNC_TEST_REMOTE='1',
                       MACGYVER_PYTHON=sys.executable)
            def git(*args):
                return subprocess.run([GIT, *args], env=env, text=True, capture_output=True, check=True).stdout
            git('init', '--bare', '-q', str(remote))
            git('init', '-q', str(seed))
            (seed / 'owner-added.txt').write_text('Owner addition must survive preview.\n')
            git('-C', str(seed), 'add', '.')
            git('-C', str(seed), 'commit', '-qm', 'fixture')
            git('-C', str(seed), 'push', '-q', remote.as_uri(), 'HEAD:refs/heads/main')
            before_remote = git('--git-dir', str(remote), 'show-ref')
            config = temp / 'private settings.conf'
            config.write_text(''.join(f'{key}={shlex.quote(str(value))}\n' for key, value in {
                'SITE_REPO': remote.as_uri(), 'MODELS_REPO': remote.as_uri(), 'STATE': state,
                'MODEL_DIR': models, 'MODELS': '', 'BRANCH': 'main',
            }.items()))
            global_config = temp / 'gitconfig'
            global_config.write_text('[user]\n name = Fixture\n email = fixture@example.org\n')
            env.update(MACGYVER_CONF=str(config), GIT_CONFIG_GLOBAL=str(global_config))
            # Reject any attempted push after seeding, while permitting actual
            # local read/clone commands. GIT_ALLOW_PROTOCOL forbids network.
            binary = temp / 'bin'
            binary.mkdir()
            log = temp / 'git-calls.txt'
            wrapper = binary / 'git'
            wrapper.write_text('#!/bin/sh\n'
                               'for arg do if [ "$arg" = push ]; then exit 99; fi; done\n'
                               f'printf "%s\\n" "$*" >> {shlex.quote(str(log))}\n'
                               f'exec {shlex.quote(GIT)} "$@"\n')
            wrapper.chmod(0o755)
            env['PATH'] = str(binary) + os.pathsep + env['PATH']
            names = ['public/academy/offline-build.json', 'public/academy/app.bundle.js',
                     'public/academy/data/markets.json', 'public/academy/data/fx.json']
            digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
            before = {name: digest(ROOT / name) for name in names}
            doctor = subprocess.run([BASH, 'macgyver.sh', 'doctor'], cwd=ROOT, env=env,
                                    capture_output=True, text=True, timeout=30)
            self.assertEqual(doctor.returncode, 0, doctor.stdout + doctor.stderr)
            self.assertIn('環境檢查通過', doctor.stdout)
            preview = subprocess.run([BASH, 'upload-all.sh', '--dry-run', '--skip-models', '--skip-data'],
                                     cwd=ROOT, env=env, capture_output=True, text=True, timeout=120)
            self.assertEqual(preview.returncode, 0, preview.stdout + preview.stderr)
            self.assertIn('只比較，未上傳', preview.stdout)
            report = json.loads((state / 'last-comparison.json').read_text())
            self.assertIn('owner-added.txt', report['preservedRemote'])
            self.assertNotIn('owner-added.txt', report['deleted'])
            self.assertEqual(before_remote, git('--git-dir', str(remote), 'show-ref'))
            self.assertEqual(before, {name: digest(ROOT / name) for name in names})
            self.assertFalse(list(models.iterdir()), 'dry-run must not download model weights')
            self.assertFalse((state / 'models').exists())

if __name__ == '__main__':
    unittest.main()
