"""High-impact export boundaries. No network or real GitHub repository is used."""
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('github_export', ROOT / 'tools/export_github.py')
export = importlib.util.module_from_spec(spec)
spec.loader.exec_module(export)
REPO = 'https://github.com/example/macgyver-academy.git'


class ExportTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name)
        self.source = self.base / 'source with spaces'
        self.source.mkdir()
        for path, text in {
            'index.html': '<html></html>',
            'public/academy/index.html': '<html></html>',
            'public/academy/app.bundle.js': 'console.log("academy");',
            '.github/workflows/pages.yml': 'name: test',
            '.openai/hosting.json': '{"project_id":"private-id","d1":"DB","r2":null}',
            '.gitignore': '/node_modules\n',
            'publish-github.sh': '#!/bin/bash\n',
            'build-offline.sh': '#!/bin/bash\nexit 0\n',
            'docs/public.txt': 'Public instructions',
            'supabase/001_learning_progress.sql': 'alter table academy_progress enable row level security;',
            'SHA256SUMS.txt': 'old checksum must be regenerated',
            '.env': 'PRIVATE=hidden',
            'portable/data/accounts.sqlite': 'private',
            'local-documents/private.txt': 'private',
            'models/model.gguf': 'model',
            'node_modules/private.txt': 'dependency',
        }.items():
            file = self.source / path
            file.parent.mkdir(parents=True, exist_ok=True)
            file.write_text(text)
        self.output = self.base / 'github output'

    def tearDown(self):
        self.temp.cleanup()

    def test_public_allowlist_and_project_id_removal(self):
        files, _ = export.snapshot(self.source)
        self.assertIn('docs/public.txt', files)
        self.assertIn('supabase/001_learning_progress.sql', files)
        self.assertNotIn(b'old checksum',files['SHA256SUMS.txt'])
        self.assertIn(b'supabase/001_learning_progress.sql',files['SHA256SUMS.txt'])
        self.assertNotIn('.env', files)
        self.assertFalse(any('accounts.sqlite' in k or 'model.gguf' in k or 'private.txt' in k for k in files))
        self.assertNotIn('project_id', json.loads(files['.openai/hosting.json']))
        self.assertIn('models/*', files['.gitignore'].decode())

    def test_dry_run_does_not_create_output_or_git(self):
        result = subprocess.run(['python3', str(ROOT / 'tools/export_github.py'), '--source', str(self.source), '--repo', REPO, '--out', str(self.output), '--dry-run'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('DRY RUN', result.stdout)
        self.assertFalse(self.output.exists())
        self.assertFalse((self.source / '.git').exists())

    def test_repeat_export_deletes_only_previous_generated_files(self):
        files, _ = export.snapshot(self.source)
        export.write_export(self.source, self.output, REPO, files, {})
        old = export.read_export(self.output, self.source, REPO)
        (self.source / 'docs/public.txt').unlink()
        newer, _ = export.snapshot(self.source)
        export.write_export(self.source, self.output, REPO, newer, old)
        self.assertFalse((self.output / 'docs/public.txt').exists())
        export.read_export(self.output, self.source, REPO)
        (self.output / 'index.html').write_text('manual edit')
        with self.assertRaisesRegex(ValueError, '手動修改'):
            export.read_export(self.output, self.source, REPO)

    def test_output_isolation_and_unknown_files(self):
        for output in (self.source, self.source / 'out', self.source.parent):
            with self.assertRaises(ValueError):
                export.read_export(output, self.source, REPO)
        self.output.mkdir()
        with self.assertRaises(ValueError):
            export.read_export(self.output, self.source, REPO)
        self.output.rmdir()
        files, _ = export.snapshot(self.source)
        export.write_export(self.source, self.output, REPO, files, {})
        (self.output / 'personal.txt').write_text('private')
        with self.assertRaisesRegex(ValueError, '額外檔案'):
            export.read_export(self.output, self.source, REPO)

    def test_credentials_and_100_mib_fail_before_copy(self):
        secret = self.source / 'docs/accidental.txt'
        secret.write_text('gh' + 'p_' + 'x' * 40)
        with self.assertRaisesRegex(ValueError, '疑似憑證'):
            export.snapshot(self.source)
        secret.unlink()
        with (self.source / 'public/huge.dat').open('wb') as f:
            f.truncate(100 * 1024 * 1024)
        with self.assertRaisesRegex(ValueError, '100 MiB'):
            export.snapshot(self.source)
        self.assertFalse(self.output.exists())

    def test_repo_url_never_accepts_credentials_or_other_hosts(self):
        for bad in ('https://TOKEN@github.com/a/b.git', 'https://evil.invalid/a/b', 'https://github.com/a/b?token=x', '/tmp/repo', 'https://github.com/a/../b'):
            with self.assertRaises(ValueError):
                export.valid_repo(bad)
        self.assertEqual(export.valid_repo('git@github.com:a/b.git'), 'git@github.com:a/b.git')

    def test_publication_slug_is_not_a_key_but_standalone_keys_are_rejected(self):
        public = self.source / 'docs/publication.txt'
        public.write_text('https://research-hub.nlr.gov/en/publications/iea-wind-tcp-task-37-definition-of-the-iea-15-megawatt-offshore-r/')
        self.assertIn('docs/publication.txt', export.snapshot(self.source)[0])
        for prefix in ('sk-', 'sk-proj-'):
            for wrapper in ('"{}"', 'Authorization: Bearer {}', 'api_key={}\\n'):
                public.write_text(wrapper.format(prefix + 'x' * 48))
                with self.assertRaisesRegex(ValueError, '疑似憑證'):
                    export.snapshot(self.source)

    def test_symlink_cannot_copy_outside_content(self):
        external = self.base / 'private.txt'
        external.write_text('private')
        try:
            (self.source / 'docs/link.txt').symlink_to(external)
        except OSError:
            self.skipTest('Symlinks unavailable')
        with self.assertRaisesRegex(ValueError, '符號連結'):
            export.snapshot(self.source)

    def test_generated_curriculum_is_downloaded_but_not_git_staged(self):
        path = self.source / 'public/academy/data/featured.json'
        path.parent.mkdir(parents=True)
        path.write_text('[]\n')
        files, _ = export.snapshot(self.source)
        self.assertIn('public/academy/data/featured.json', files)
        self.output.mkdir()
        (self.output / '.git').mkdir()
        calls = []
        def fake_git(directory, *args, capture=False, check=True):
            calls.append(args)
            if args[0] == 'symbolic-ref': return 'main'
            if args[0] == 'config': return 'test-identity'
            if args[0] == 'ls-files': return 'public/academy/data/featured.json\0index.html\0'
            if args[0] == 'ls-remote': return ''
            return '' if capture else 0
        with patch.object(export, 'git', fake_git), patch.object(export.shutil, 'which', return_value='/stub/git'):
            export.push(self.output, REPO, 'main', 'test', files)
        self.assertIn(('rm', '--cached', '--', 'public/academy/data/featured.json'), calls)
        staged = [name for args in calls if args[0] == 'add' for name in args[2:]]
        self.assertEqual(set(staged), set(files) - {'public/academy/data/featured.json'})


if __name__ == '__main__':
    unittest.main()
