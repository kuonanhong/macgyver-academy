#!/usr/bin/env python3
"""Independent small-fixture checks; never package the actual project tree."""
from pathlib import Path
from unittest import mock
import hashlib
import importlib.util
import sys
import tempfile
import unittest
import zipfile

PROJECT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('v15_package_under_test', PROJECT / 'tools/package-v15.py')
PACKAGE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PACKAGE)


class PackageFixtureTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='v15-package-fixture-')
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name)
        self.source = self.folder / 'fixture-source'
        self.source.mkdir()
        self.root_patch = mock.patch.object(PACKAGE, 'ROOT', self.source)
        self.root_patch.start()
        self.addCleanup(self.root_patch.stop)

    def put(self, relative, content=b'fixture content\n'):
        p = self.source / relative
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(content)
        return p

    def expected(self, files):
        return {p.relative_to(self.source).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}

    def test_private_directories_at_multiple_depths(self):
        names = ['owner-private', 'local-documents', 'credentials', 'secrets',
                 'userdata', 'user-data', 'uploads', 'models', 'model-cache']
        for name in names:
            for parent in ['', 'docs/', 'public/nested/']:
                path = parent + name + '/private.json'
                with self.subTest(path=path):
                    self.assertFalse(PACKAGE.permitted(self.source / path))
        for path in ['incoming/private.txt', 'deliverables/private.zip',
                     'node_modules/pkg/index.js', '.git/config', '.env', '.env.local',
                     'docs/.env.production', '.openai/auth.json', '.openai/nested/hosting.json',
                     'public-player/.openai/auth.json', 'public-player/.openai/hosting.json']:
            with self.subTest(path=path):
                self.assertFalse(PACKAGE.permitted(self.source / path))

    def test_weights_keys_databases_and_stale_root_checksums_excluded(self):
        for suffix in ['.gguf', '.safetensors', '.ckpt', '.pt', '.pth', '.onnx', '.bin',
                       '.pem', '.key', '.p12', '.pfx', '.sqlite', '.sqlite3', '.db']:
            for extension in [suffix, suffix.upper()]:
                with self.subTest(extension=extension):
                    self.assertFalse(PACKAGE.permitted(self.source / ('assets/fixture' + extension)))
        for path in ['keys/id_rsa', 'keys/id_ed25519', 'x/store.sqlite3-wal',
                     'x/store.sqlite3-shm', 'SHA256SUMS.txt', 'SHA256SUMS', 'RELEASE_FILES_V15.json']:
            with self.subTest(path=path):
                self.assertFalse(PACKAGE.permitted(self.source / path))

    def test_portable_templates_are_exact_exceptions(self):
        for path in ['portable/data/README.md', 'portable/data/.gitkeep']:
            self.assertTrue(PACKAGE.permitted(self.source / path), path)
        for path in ['portable/data/local-knowledge.json', 'portable/data/learners.json',
                     'portable/data/nested/README.md', 'portable/data/nested/.gitkeep']:
            self.assertFalse(PACKAGE.permitted(self.source / path), path)

    def test_public_runtime_sources_remain_included(self):
        required = ['index.html', 'public/academy/index.html', 'public/academy/app.bundle.js',
                    'public/academy/data/lazy/index.json', 'public/academy/data/featured.json',
                    'public/academy/assets/labs/v15/run-water-labs.py',
                    'portable/server.py', 'portable/knowledge.py', 'portable/curriculum_parts.py',
                    'tools/index-documents.py', 'tools/model-manifest.json',
                    'tools/download_ai_model.py', 'tools/build-offline.mjs',
                    'tools/sync-v13/models_sync.py', 'tools/sync-v12/sync_github.py',
                    'run-local.sh', 'run-local.bat', 'start-mac.command', 'run-ai-local.ps1',
                    'requirements-documents.txt', 'package.json', 'pnpm-lock.yaml',
                    'scripts/run-framework.mjs', 'build/sites-worker.ts',
                    '.env.example', '.npmrc', '.github/workflows/pages.yml', '.openai/hosting.json']
        for path in required:
            with self.subTest(path=path):
                self.assertTrue((PROJECT / path).is_file(), 'Required source is absent: ' + path)
                self.assertTrue(PACKAGE.permitted(self.source / path), 'Required source excluded: ' + path)
        self.assertTrue(PACKAGE.permitted(self.source / 'public/academy/assets/labs/v11/SHA256SUMS.txt'))

    def test_zip_modes_crc_and_determinism(self):
        files = [self.put('start-mac.command', b'#!/bin/bash\necho fixture\n'),
                 self.put('run-local.sh', b'#!/bin/bash\necho fixture\n'),
                 self.put('docs/中文說明.md', '小型測試資料。\n'.encode())]
        expected = self.expected(files)
        first = self.folder / 'first.zip'
        second = self.folder / 'second.zip'
        one = PACKAGE.write_zip(first, files, expected)
        two = PACKAGE.write_zip(second, files, expected)
        self.assertEqual(one['sha256'], two['sha256'])
        self.assertEqual(first.read_bytes(), second.read_bytes())
        with zipfile.ZipFile(first) as z:
            self.assertIsNone(z.testzip())
            for path, mode in [('start-mac.command', 0o755), ('run-local.sh', 0o755), ('docs/中文說明.md', 0o644)]:
                info = z.getinfo(PACKAGE.NAME + '/' + path)
                self.assertEqual((info.external_attr >> 16) & 0o777, mode)
                self.assertEqual(info.date_time, PACKAGE.STAMP)
                self.assertEqual(hashlib.sha256(z.read(info)).hexdigest(), expected[path])

    def test_source_change_after_snapshot_is_rejected(self):
        changed = self.put('public/data.json', b'old value\n')
        expected = self.expected([changed])
        changed.write_bytes(b'new value\n')  # Same length: size alone cannot detect this.
        with self.assertRaisesRegex(ValueError, 'Source changed during packaging: public/data.json'):
            PACKAGE.write_zip(self.folder / 'rejected.zip', [changed], expected)
        self.assertEqual(changed.read_bytes(), b'new value\n', 'Packaging must not rewrite input.')

    def test_two_independent_parts_recreate_full_archive(self):
        files = [self.put('index.html', b'<p>fixture</p>\n'),
                 self.put('public/academy/data/lazy/course.json', b'{"fixture":true}\n'),
                 self.put('start-mac.command', b'#!/bin/bash\ntrue\n'),
                 self.put('docs/README.md', b'Extract every independent part into one directory.\n')]
        expected = self.expected(files)
        full = self.folder / 'complete.zip'
        PACKAGE.write_zip(full, files, expected)
        part_paths = []
        # Explicit independent groups exercise ZIP semantics without running
        # release gates, building curricula, or allocating artificial huge files.
        for n, group in enumerate((files[:2], files[2:]), 1):
            part = self.folder / f'fixture_part{n}of2.zip'
            PACKAGE.write_zip(part, group, expected)
            part_paths.append(part)
        union = {}
        extracted = self.folder / 'extracted'
        for part in part_paths:
            with zipfile.ZipFile(part) as z:
                self.assertIsNone(z.testzip())
                for name in z.namelist():
                    self.assertNotIn(name, union, 'Independent parts must have disjoint members.')
                    union[name] = z.read(name)
                z.extractall(extracted)
        with zipfile.ZipFile(full) as z:
            self.assertEqual(set(union), set(z.namelist()))
            for name, data in union.items():
                self.assertEqual(data, z.read(name))
                self.assertEqual((extracted / name).read_bytes(), data)
                relative = name.split('/', 1)[1]
                self.assertEqual(hashlib.sha256(data).hexdigest(), expected[relative])

    def test_existing_release_artifacts_refused_before_gates(self):
        names = [PACKAGE.NAME + '.zip', PACKAGE.NAME + '_part1of2.zip',
                 PACKAGE.NAME + '.zip.sha256', PACKAGE.NAME + '_parts.sha256', 'V15_ARCHIVES.json']
        for i, name in enumerate(names):
            with self.subTest(name=name):
                output = self.folder / f'existing-{i}'
                output.mkdir()
                existing = output / name
                existing.write_bytes(b'preserve existing release\n')
                with mock.patch.object(sys, 'argv', ['package-v15.py', '--output', str(output)]), \
                     mock.patch.object(PACKAGE.subprocess, 'run', side_effect=AssertionError('Must reject before release gates')) as runner, \
                     mock.patch.object(PACKAGE, 'write_zip', side_effect=AssertionError('No archive may be written')) as writer:
                    with self.assertRaisesRegex(ValueError, 'Release archives already exist'):
                        PACKAGE.main()
                    runner.assert_not_called()
                    writer.assert_not_called()
                self.assertEqual(existing.read_bytes(), b'preserve existing release\n')

    def test_source_tree_output_refused_before_gates(self):
        for output in [self.source, self.source / 'nested-output']:
            with self.subTest(output=output.name):
                with mock.patch.object(sys, 'argv', ['package-v15.py', '--output', str(output)]), \
                     mock.patch.object(PACKAGE.subprocess, 'run', side_effect=AssertionError('No release gates allowed')) as runner:
                    with self.assertRaisesRegex(ValueError, 'Output must be outside source tree'):
                        PACKAGE.main()
                    runner.assert_not_called()


if __name__ == '__main__':
    unittest.main(verbosity=2)
