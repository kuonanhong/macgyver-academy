"""V13 model sync: shared PRIVATE-MODELS repo, chunk reuse, pruning and restore (local file:// remote)."""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / 'tools/sync-v13/models_sync.py'
CHUNK = 65536


def run(*args, cwd=None, check=True):
    env = dict(os.environ, MACGYVER_MODELS_TEST_REMOTE='1', MACGYVER_MODELS_TEST_CHUNK_BYTES=str(CHUNK),
               GIT_AUTHOR_NAME='t', GIT_AUTHOR_EMAIL='t@example.com', GIT_COMMITTER_NAME='t', GIT_COMMITTER_EMAIL='t@example.com')
    return subprocess.run(list(args), cwd=cwd, env=env, check=check, capture_output=True, text=True)


class ModelsSyncTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.t = Path(self.tmp.name)
        self.remote = self.t / 'remote.git'
        run('git', 'init', '-q', '--bare', str(self.remote))
        run('git', '-C', str(self.remote), 'config', 'uploadpack.allowfilter', 'true')
        run('git', '-C', str(self.remote), 'config', 'uploadpack.allowAnySHA1InWant', 'true')
        self.models = self.t / 'models'
        self.models.mkdir()
        data = os.urandom(CHUNK * 2 + 1000)
        (self.models / 'tiny.gguf').write_bytes(data)
        seed = self.t / 'seed'
        (seed / 'projects/huatuo/v3/chunks').mkdir(parents=True)
        (seed / 'projects/huatuo/v3/chunks/x.part').write_bytes(data[:CHUNK])  # same bytes as our first chunk
        (seed / 'README.md').write_text('private')
        run('git', 'init', '-q', str(seed))
        run('git', '-C', str(seed), 'add', '-A')
        run('git', '-C', str(seed), '-c', 'user.name=t', '-c', 'user.email=t@example.com', 'commit', '-qm', 'seed')
        run('git', '-C', str(seed), 'push', '-q', str(self.remote), 'HEAD:refs/heads/main', check=False)
        self.url = 'file://' + str(self.remote)
        self.state = self.t / 'state'

    def tearDown(self):
        self.tmp.cleanup()

    def tree(self):
        return run('git', '-C', str(self.remote), 'ls-tree', '-r', '--name-only', 'main').stdout.split()

    def test_push_reuse_prune_restore(self):
        out = run(sys.executable, str(TOOL), 'compare', '--repo', self.url, '--models-dir', str(self.models), '--state', str(self.state)).stdout
        self.assertIn('1 片，不需再傳資料', out)
        run(sys.executable, str(TOOL), 'push', '--repo', self.url, '--models-dir', str(self.models), '--state', str(self.state), '--private-confirmed')
        tree = self.tree()
        self.assertIn('projects/huatuo/v3/chunks/x.part', tree)  # never touched
        self.assertIn('projects/macgyver/weights-manifest.json', tree)
        self.assertEqual(sum(p.startswith('projects/macgyver/parts/') for p in tree), 3)
        again = run(sys.executable, str(TOOL), 'push', '--repo', self.url, '--models-dir', str(self.models), '--state', str(self.state), '--private-confirmed').stdout
        self.assertIn('已是最新', again)
        with (self.models / 'tiny.gguf').open('ab') as f:
            f.write(os.urandom(500))
        run(sys.executable, str(TOOL), 'push', '--repo', self.url, '--models-dir', str(self.models), '--state', str(self.state), '--private-confirmed')
        tree = self.tree()
        self.assertEqual(sum(p.startswith('projects/macgyver/parts/') for p in tree), 3)  # last chunk replaced, stale removed
        self.assertIn('projects/huatuo/v3/chunks/x.part', tree)
        dest = self.t / 'restored'
        run(sys.executable, str(TOOL), 'restore', '--repo', self.url, '--state', str(self.t / 'state2'), '--to', str(dest))
        self.assertEqual((dest / 'tiny.gguf').read_bytes(), (self.models / 'tiny.gguf').read_bytes())
        manifest = json.loads(run('git', '-C', str(self.remote), 'show', 'main:projects/macgyver/weights-manifest.json').stdout)
        self.assertEqual(manifest['schema'], 1)
        self.assertTrue(all(p['path'].startswith('parts/') for f in manifest['files'] for p in f['parts']))

    def test_push_requires_private_confirmation(self):
        r = run(sys.executable, str(TOOL), 'push', '--repo', self.url, '--models-dir', str(self.models), '--state', str(self.state), check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn('Private', r.stderr + r.stdout)


if __name__ == '__main__':
    unittest.main()
