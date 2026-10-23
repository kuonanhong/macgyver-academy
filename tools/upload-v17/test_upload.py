#!/usr/bin/env python3
"""Real local Git fixtures; never contacts GitHub or changes global user config."""
from __future__ import annotations
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest import mock
from urllib.error import HTTPError, URLError
import zipfile

SOURCE = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('v17_upload_under_test', Path(__file__).with_name('upload.py'))
u = importlib.util.module_from_spec(spec)
spec.loader.exec_module(u)


def cmd(*args, cwd=None, env=None):
    return subprocess.run(list(args), cwd=cwd, env=env, check=True, capture_output=True, text=True).stdout.strip()


class UploadTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='macgyver-v17-upload-test-')
        self.base = Path(self.tmp.name)
        self.source = self.base / 'V17 source with spaces'
        self.source.mkdir()
        for name in ('macgyver.sh', 'upload-all.sh', 'Upload_MacGyver_v17_SSH.sh', 'tools/upload-v17/upload.py', 'tools/upload-v17/site_sync.py', 'tools/sync-v12/sync_github.py', 'tools/sync-v13/models_sync.py', 'tools/export_github.py', 'tools/model-manifest.json'):
            target = self.source / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(SOURCE / name, target)
        for name, data in {'index.html': 'V17 entry', 'public/academy/index.html': 'V17 home', 'public/academy/app.bundle.js': 'console.log(16)', 'publish-github.sh': '#!/bin/bash\n', '.github/workflows/pages.yml': 'name: fixture\n', '.gitignore': '*.gguf\n', 'owner-private/bootstrap.json': '{"owner":"PRIVATE-ONLY"}', 'portable/data/accounts.json': '{"account":"PRIVATE-ONLY"}'}.items():
            p = self.source / name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(data)
        config = self.base / 'gitconfig'
        config.write_text('[user]\nname = Upload Fixture\nemail = fixture@example.invalid\n[init]\ndefaultBranch = main\n')
        self.site = self.base / 'site.git'
        self.private = self.base / 'private.git'
        self.state = self.base / 'upload-state'
        self.env = dict(os.environ, GIT_CONFIG_GLOBAL=str(config), GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_COUNT='0',
                        MACGYVER_UPLOAD_V17_TEST='1', MACGYVER_UPLOAD_V17_TEST_SITE=self.site.as_uri(),
                        MACGYVER_UPLOAD_V17_TEST_PRIVATE=self.private.as_uri(), MACGYVER_MODELS_TEST_REMOTE='1',
                        MACGYVER_MODELS_TEST_CHUNK_BYTES='16')
        for path in (self.site, self.private):
            cmd('git', 'init', '--bare', str(path), env=self.env)
            seed = self.base / (path.stem + '-seed')
            cmd('git', 'clone', str(path), str(seed), env=self.env)
            (seed / 'remote-only.txt').write_text('keep me')
            cmd('git', 'add', 'remote-only.txt', cwd=seed, env=self.env)
            cmd('git', 'commit', '-m', 'seed', cwd=seed, env=self.env)
            cmd('git', 'push', 'origin', 'main', cwd=seed, env=self.env)

    def tearDown(self):
        self.tmp.cleanup()

    def run_upload(self, *args, check=True):
        return subprocess.run(['bash', str(self.source / 'Upload_MacGyver_v17_SSH.sh'), '--with-assets', '--state', str(self.state), *args],
                              env=self.env, cwd=self.base, text=True, capture_output=True, check=check)

    def head(self, repo):
        return cmd('git', '--git-dir', str(repo), 'rev-parse', 'refs/heads/main', env=self.env)

    def show(self, repo, path):
        return cmd('git', '--git-dir', str(repo), 'show', 'main:' + path, env=self.env)

    def assets(self):
        model = self.source / 'models/custom model.gguf'
        doc = self.source / 'local-documents/lesson.md'
        model.parent.mkdir(exist_ok=True)
        doc.parent.mkdir(exist_ok=True)
        model.write_bytes(b'MODEL-EXAMPLE-1234' * 8)
        doc.write_text('Private teaching notes, multilingual: 水利工程。')
        (doc.parent / '.env').write_text('NEVER_UPLOAD=credential')
        (doc.parent / 'accounts.sqlite').write_bytes(b'PRIVATE ACCOUNT DB')
        (model.parent / 'credentials.json').write_text('{"doNot":"upload"}')
        return model, doc

    def test_dry_run_has_no_remote_mutation(self):
        self.assets()
        old = (self.head(self.site), self.head(self.private))
        r = self.run_upload('--dry-run')
        self.assertIn('遠端未變更', r.stdout)
        self.assertEqual(old, (self.head(self.site), self.head(self.private)))

    def test_default_updates_only_public_website(self):
        self.assets()
        original = self.head(self.private)
        subprocess.run(['bash', str(self.source / 'Upload_MacGyver_v17_SSH.sh'), '--state', str(self.state)],
                       env=self.env, cwd=self.base, text=True, capture_output=True, check=True)
        self.assertEqual(original, self.head(self.private))
        self.assertEqual('V17 entry', self.show(self.site, 'index.html'))

    def test_generic_aliases_use_v17_and_accept_with_assets(self):
        self.assets()
        original = (self.head(self.site), self.head(self.private))
        for script, arguments in [('macgyver.sh', ['compare']), ('upload-all.sh', ['--dry-run'])]:
            result = subprocess.run(['bash', str(self.source / script), *arguments,
                                     '--with-assets', '--state', str(self.state)],
                                    env=self.env, cwd=self.base, text=True, capture_output=True, check=True)
            self.assertIn('遠端未變更', result.stdout)
            self.assertEqual(original, (self.head(self.site), self.head(self.private)))

    def test_upload_noop_modify_preserve_and_restore(self):
        model, doc = self.assets()
        self.run_upload()
        self.assertEqual('V17 entry', self.show(self.site, 'index.html'))
        for repo in (self.site, self.private):
            self.assertEqual('keep me', self.show(repo, 'remote-only.txt'))
        public_names = cmd('git', '--git-dir', str(self.site), 'ls-tree', '-r', '--name-only', 'main', env=self.env)
        for blocked in ('owner-private/', 'portable/data/', 'models/custom', 'local-documents/'):
            self.assertNotIn(blocked, public_names)
        manifest = json.loads(self.show(self.private, u.MANIFEST))
        self.assertEqual(['documents/lesson.md', 'models/custom model.gguf'], [x['path'] for x in manifest['files']])
        old = (self.head(self.site), self.head(self.private))
        self.run_upload()
        self.assertEqual(old, (self.head(self.site), self.head(self.private)))
        model.write_bytes(b'UPDATED-WEIGHT-ABCDE' * 8)
        original_doc = doc.read_bytes()
        doc.unlink()
        (self.source / 'index.html').write_text('V17 changed')
        self.run_upload()
        self.assertEqual('V17 changed', self.show(self.site, 'index.html'))
        manifest = json.loads(self.show(self.private, u.MANIFEST))
        self.assertEqual(['documents/lesson.md', 'models/custom model.gguf'], [x['path'] for x in manifest['files']])
        destination = self.base / 'restore destination'
        self.run_upload('--restore-assets', str(destination))
        self.assertEqual(model.read_bytes(), (destination / 'models/custom model.gguf').read_bytes())
        self.assertEqual(original_doc, (destination / 'documents/lesson.md').read_bytes())

    def test_skip_private_and_no_download(self):
        self.assets()
        old = self.head(self.private)
        self.run_upload('--skip-models', '--skip-documents')
        self.assertEqual(old, self.head(self.private))
        shutil.rmtree(self.source / 'models')
        shutil.rmtree(self.source / 'local-documents')
        r = self.run_upload()
        self.assertIn('不下載模型', r.stdout)
        self.assertFalse((self.source / 'models').exists())

    def test_reject_unsafe_credentials_before_any_push(self):
        self.assets()
        private = self.source / 'local-documents/lesson.md'
        private.write_text('service credential ' + 'sk-' + 'x' * 48)
        old = (self.head(self.site), self.head(self.private))
        r = self.run_upload(check=False)
        self.assertNotEqual(0, r.returncode)
        self.assertIn('疑似金鑰', r.stderr)
        self.assertNotIn('sk-' + 'x' * 48, r.stderr)
        self.assertEqual(old, (self.head(self.site), self.head(self.private)))

    def test_reject_office_embedded_credentials(self):
        directory = self.base / 'documents'
        directory.mkdir()
        with zipfile.ZipFile(directory / 'notes.docx', 'w', compression=zipfile.ZIP_DEFLATED) as f:
            f.writestr('word/document.xml', '<doc>' + 'github_' + 'pat_' + 'a' * 40 + '</doc>')
        with self.assertRaisesRegex(ValueError, '疑似金鑰'):
            u.collect(directory, 'documents')

    def test_owner_private_selected_subfolder_rejected(self):
        directory = self.source / 'owner-private' / 'models'
        directory.mkdir()
        (directory / 'model.gguf').write_bytes(b'weight')
        with self.assertRaisesRegex(ValueError, '子資料夾'):
            u.collect(directory, 'models')

    def test_unowned_state_is_never_reset(self):
        self.state.mkdir()
        p = self.state / 'precious.txt'
        p.write_text('keep')
        r = self.run_upload('--skip-models', '--skip-documents', check=False)
        self.assertNotEqual(0, r.returncode)
        self.assertEqual('keep', p.read_text())

    def test_private_visibility_fails_closed(self):
        with mock.patch.object(u.shutil, 'which', return_value=None):
            with mock.patch.object(u, 'urlopen', return_value=contextlib.nullcontext(io.BytesIO(b'{"private":false}'))):
                with self.assertRaises(ValueError):
                    u.check_private_repo(u.PRIVATE_REPO)
            with mock.patch.object(u, 'urlopen', side_effect=URLError('offline')):
                with self.assertRaises(ValueError):
                    u.check_private_repo(u.PRIVATE_REPO)
            with mock.patch.object(u, 'urlopen', side_effect=HTTPError('test', 404, 'missing', {}, None)), mock.patch.object(u.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, '', '')):
                self.assertIn('authenticated SSH', u.check_private_repo(u.PRIVATE_REPO))

    def test_unknown_model_and_document_paths_with_spaces(self):
        custom = self.base / 'external weights'
        custom.mkdir()
        (custom / 'custom.h5').write_bytes(b'my custom trained weights')
        docs = self.base / 'external docs'
        docs.mkdir()
        (docs / '實驗課程.txt').write_text('資料')
        self.run_upload('--models-dir', str(custom), '--documents-dir', str(docs))
        manifest = json.loads(self.show(self.private, u.MANIFEST))
        self.assertEqual(['documents/實驗課程.txt', 'models/custom.h5'], [x['path'] for x in manifest['files']])

    def test_selected_private_folder_inside_public_tree_is_not_published(self):
        private = self.source / 'docs' / 'my private teaching files'
        private.mkdir(parents=True)
        (private / 'notes.txt').write_text('Private class discussion')
        self.run_upload('--skip-models', '--documents-dir', str(private))
        public_names = cmd('git', '--git-dir', str(self.site), 'ls-tree', '-r', '--name-only', 'main', env=self.env)
        self.assertNotIn('my private teaching files', public_names)
        manifest = json.loads(self.show(self.private, u.MANIFEST))
        self.assertEqual(['documents/notes.txt'], [x['path'] for x in manifest['files']])

    def test_model_formats_and_uppercase_credentials_excluded_from_public(self):
        public = self.source / 'public' / 'academy'
        (public / 'training.h5').write_bytes(b'local weights')
        (public / 'training.model').write_bytes(b'local weights')
        (public / 'CREDENTIALS').mkdir()
        (public / 'CREDENTIALS' / 'notes.txt').write_text('Private account notes')
        self.run_upload('--skip-models', '--skip-documents')
        names = cmd('git', '--git-dir', str(self.site), 'ls-tree', '-r', '--name-only', 'main', env=self.env)
        self.assertNotIn('training.h5', names)
        self.assertNotIn('training.model', names)
        self.assertNotIn('CREDENTIALS', names)

    def test_interrupted_chunk_batches_resume(self):
        model, doc = self.assets()
        with mock.patch.dict(os.environ, self.env):
            engine = u.load_engine()
            plans = u.plan_assets(engine, [('models', model.parent, [model])])
            state = self.base / 'resume-state'
            original = engine.commit_and_push
            calls = 0
            def interrupted(*args, **kwargs):
                nonlocal calls
                calls += 1
                if calls == 2:
                    raise RuntimeError('simulated interruption')
                return original(*args, **kwargs)
            with mock.patch.object(engine, 'commit_and_push', side_effect=interrupted):
                with self.assertRaisesRegex(RuntimeError, 'simulated interruption'):
                    u.upload_assets(engine, plans, self.private.as_uri(), 'main', state, batch_mib=0)
            names = cmd('git', '--git-dir', str(self.private), 'ls-tree', '-r', '--name-only', 'main', env=self.env)
            self.assertIn(u.PREFIX + '/parts/', names)
            self.assertNotIn(u.MANIFEST, names)
            u.upload_assets(engine, plans, self.private.as_uri(), 'main', state, batch_mib=0)
            dest = self.base / 'resumed-restore'
            u.restore_assets(engine, self.private.as_uri(), 'main', state, dest)
            self.assertEqual(model.read_bytes(), (dest / 'models/custom model.gguf').read_bytes())

    def test_manifest_traversal_rejected(self):
        with self.assertRaises(ValueError):
            u.validate_remote_manifest({'schema': 1, 'files': [{'path': 'documents/../../owner-private/x'}]})

    def test_public_unicode_filename_does_not_recommit(self):
        p = self.source / 'docs/水利 教材.md'
        p.parent.mkdir()
        p.write_text('公開教材')
        self.run_upload('--skip-models', '--skip-documents')
        first = self.head(self.site)
        self.run_upload('--skip-models', '--skip-documents')
        self.assertEqual(first, self.head(self.site))
        self.assertEqual('公開教材', self.show(self.site, 'docs/水利 教材.md'))

    def test_password_assignments_rejected(self):
        data = ('{"pass' + 'word":"sample1234"}').encode()
        with self.assertRaises(ValueError):
            u.scan_stream(io.BytesIO(data), 'example.json')

    def test_retry_never_force_pushes(self):
        with mock.patch.dict(os.environ, self.env):
            engine = u.load_engine()
            with mock.patch.object(engine, 'git', side_effect=['tree', 'commit']), mock.patch.object(engine.subprocess, 'run', return_value=subprocess.CompletedProcess([], 1)) as run, mock.patch.object(engine.time, 'sleep'):
                with self.assertRaises(SystemExit):
                    engine.commit_and_push(self.base, None, self.base / 'index', 'test', 'main')
                self.assertEqual(4, run.call_count)
                self.assertTrue(all('--force' not in c.args[0] and '-f' not in c.args[0] for c in run.call_args_list))


if __name__ == '__main__':
    unittest.main(verbosity=2)
