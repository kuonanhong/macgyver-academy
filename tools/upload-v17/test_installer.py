#!/usr/bin/env python3
"""Small local fixtures for packaging and extraction; never publishes a release."""
import hashlib
import json
from pathlib import Path
import shutil
import stat
import subprocess
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[2]
NAME = 'MacGyver_Engineering_Academy_v17'
SCRIPT = 'Install_and_Upload_MacGyver_v17.sh'


class InstallerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = tempfile.TemporaryDirectory(prefix='macgyver-v17-small-package-')
        cls.base = Path(cls.fixture.name)
        cls.source = cls.base / 'source with spaces'
        cls.source.mkdir()
        for name in ('tools/package-v17.py', SCRIPT):
            target = cls.source / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, target)
        for name in ('tools/upload-v17/upload.py', 'tools/upload-v17/site_sync.py', 'tools/sync-v12/sync_github.py', 'tools/sync-v13/models_sync.py', 'Upload_MacGyver_v17_SSH.sh', 'run-local.sh'):
            target = cls.source / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text('# fixture only; never contacts GitHub\n')
        (cls.source / 'tools/upload-v17/upload.py').write_text(
            "import json, sys\nfrom pathlib import Path\nPath('UPLOADER_ARGUMENTS.json').write_text(json.dumps(sys.argv[1:]))\n")
        for name, content in {
            'docs/VALIDATION_V17.json': '{"status":"PASS","version":"17.0.0"}',
            'public/academy/index.html': '<h1>V17 城市學院</h1>',
            'docs/public notes.txt': 'Public reference',
            'models/real-model.gguf': 'LOCAL PRIVATE WEIGHT',
            'local-documents/private.md': 'PRIVATE DOCUMENT',
            'credentials/account.json': 'PRIVATE ACCOUNT',
            'public/academy/accidental.h5': 'PRIVATE WEIGHT OUTSIDE MODELS',
            'owner-private/owner-bootstrap.json': 'PRIVATE OWNER',
            'public/academy/assets/labs/v17/lesson.zip': 'Fixture lesson attachment',
        }.items():
            target = cls.source / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content)
        cls.output = cls.base / 'fixture release'
        subprocess.run(['python', str(cls.source / 'tools/package-v17.py'), str(cls.output), '--parts'], check=True, capture_output=True, text=True)

    @classmethod
    def tearDownClass(cls):
        cls.fixture.cleanup()

    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(prefix='macgyver-v17-extract-')
        self.folder = Path(self.directory.name)
        shutil.copyfile(self.output / SCRIPT, self.folder / SCRIPT)

    def tearDown(self):
        self.directory.cleanup()

    def run_installer(self, *args):
        return subprocess.run(['bash', str(self.folder / SCRIPT), '--extract-only', *args], cwd=self.folder.parent, capture_output=True, text=True)

    def copy_parts(self, count=4):
        for number in range(1, count + 1):
            name = 'MacGyver_v17_Alternative_%d_of_4.zip' % number
            shutil.copyfile(self.output / name, self.folder / name)

    def copy_full(self):
        shutil.copyfile(self.output / (NAME + '.zip'), self.folder / (NAME + '.zip'))

    def change_zip(self, modify):
        path = self.folder / (NAME + '.zip')
        with zipfile.ZipFile(path) as archive:
            members = {info.filename: archive.read(info) for info in archive.infolist()}
        modify(members)
        with zipfile.ZipFile(path, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
            for name, content in members.items():
                archive.writestr(name, content)
        document = json.loads((self.output / 'RELEASE_ARCHIVES_V17.json').read_text())
        record = next(item for item in document['archives'] if item['filename'] == path.name)
        record['bytes'] = path.stat().st_size
        record['sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
        (self.folder / 'new-manifest.json').write_text(json.dumps(document))

    def test_packager_excludes_private_assets(self):
        with zipfile.ZipFile(self.output / (NAME + '.zip')) as archive:
            names = archive.namelist()
        for fragment in ('real-model.gguf', 'private.md', 'account.json', 'accidental.h5', 'owner-bootstrap.json'):
            self.assertFalse(any(fragment in name for name in names), fragment)
        self.assertTrue(any(name.endswith('/assets/labs/v17/lesson.zip') for name in names))

    def test_full_zip_embedded_checksums_and_preserve_local_edits(self):
        self.copy_full()
        result = self.run_installer()
        self.assertEqual(0, result.returncode, result.stderr)
        project = self.folder / NAME
        target = project / 'docs/public notes.txt'
        target.write_text('My local update')
        added = project / 'docs/new local file.txt'
        added.write_text('New local file')
        again = self.run_installer()
        self.assertEqual(0, again.returncode, again.stderr)
        self.assertEqual('My local update', target.read_text())
        self.assertTrue(added.is_file())
        self.assertIn('保留', again.stdout)

    def test_four_parts_restore_same_files_without_external_manifest(self):
        self.copy_parts()
        result = self.run_installer()
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn('V17 城市學院', (self.folder / NAME / 'public/academy/index.html').read_text())

    def test_missing_part_stops_before_extract(self):
        self.copy_parts(3)
        result = self.run_installer()
        self.assertNotEqual(0, result.returncode)
        self.assertIn('尚缺第 4 包', result.stderr)
        self.assertFalse((self.folder / NAME).exists())

    def test_corrupt_zip_stops_before_extract(self):
        self.copy_full()
        with (self.folder / (NAME + '.zip')).open('ab') as stream:
            stream.write(b'corrupt download')
        result = self.run_installer()
        self.assertNotEqual(0, result.returncode)
        self.assertIn('SHA-256', result.stderr)
        self.assertFalse((self.folder / NAME).exists())

    def test_source_template_uses_external_current_manifest(self):
        self.copy_full()
        shutil.copyfile(ROOT / SCRIPT, self.folder / SCRIPT)
        shutil.copyfile(self.output / 'RELEASE_ARCHIVES_V17.json', self.folder / 'RELEASE_ARCHIVES_V17.json')
        result = self.run_installer()
        self.assertEqual(0, result.returncode, result.stderr)

    def test_path_traversal_and_unexpected_root_rejected(self):
        for malicious in (NAME + '/../escape.txt', 'wrong-root/escape.txt'):
            self.copy_full()
            self.change_zip(lambda members: members.update({malicious: b'bad'}))
            result = self.run_installer('--manifest', str(self.folder / 'new-manifest.json'))
            self.assertNotEqual(0, result.returncode)
            self.assertFalse((self.folder / NAME).exists())
            self.assertFalse((self.folder / 'escape.txt').exists())

    def test_internal_file_hash_mismatch_rejected_even_with_matching_archive_hash(self):
        self.copy_full()
        self.change_zip(lambda members: members.update({NAME + '/docs/public notes.txt': b'corrupted content'}))
        result = self.run_installer('--manifest', str(self.folder / 'new-manifest.json'))
        self.assertNotEqual(0, result.returncode)
        self.assertIn('逐檔 SHA-256', result.stderr)
        self.assertFalse((self.folder / NAME).exists())

    def test_symbolic_link_member_rejected_before_extract(self):
        self.copy_full()
        path = self.folder / (NAME + '.zip')
        info = zipfile.ZipInfo(NAME + '/public/link')
        info.create_system = 3
        info.external_attr = (stat.S_IFLNK | 0o777) << 16
        with zipfile.ZipFile(path, 'a') as archive:
            archive.writestr(info, '/outside/target')
        document = json.loads((self.output / 'RELEASE_ARCHIVES_V17.json').read_text())
        record = next(item for item in document['archives'] if item['filename'] == path.name)
        record.update(bytes=path.stat().st_size, sha256=hashlib.sha256(path.read_bytes()).hexdigest())
        manifest = self.folder / 'new-manifest.json'
        manifest.write_text(json.dumps(document))
        result = self.run_installer('--manifest', str(manifest))
        self.assertNotEqual(0, result.returncode)
        self.assertIn('符號連結', result.stderr)
        self.assertFalse((self.folder / NAME).exists())

    def test_help_does_not_need_archives(self):
        result = subprocess.run(['bash', str(self.folder / SCRIPT), '--help'], capture_output=True, text=True)
        self.assertEqual(0, result.returncode)
        self.assertIn('--with-assets', result.stdout)

    def test_with_assets_and_external_directories_forward_to_uploader(self):
        self.copy_full()
        models = self.folder / 'external model files'
        documents = self.folder / 'external private documents'
        result = subprocess.run(['bash', str(self.folder / SCRIPT), '--with-assets',
                                 '--models-dir', str(models), '--documents-dir', str(documents)],
                                cwd=self.folder.parent, capture_output=True, text=True)
        self.assertEqual(0, result.returncode, result.stderr)
        arguments = json.loads((self.folder / NAME / 'UPLOADER_ARGUMENTS.json').read_text())
        self.assertIn('--with-assets', arguments)
        self.assertEqual(str(models), arguments[arguments.index('--models-dir') + 1])
        self.assertEqual(str(documents), arguments[arguments.index('--documents-dir') + 1])

    def test_packager_rejects_credential_content_before_archiving(self):
        source = self.folder / 'secret fixture'
        (source / 'tools').mkdir(parents=True)
        (source / 'docs').mkdir()
        shutil.copyfile(ROOT / 'tools/package-v17.py', source / 'tools/package-v17.py')
        shutil.copyfile(ROOT / SCRIPT, source / SCRIPT)
        (source / 'docs/VALIDATION_V17.json').write_text('{"status":"PASS"}')
        (source / 'docs/key.txt').write_text('synthetic fixture: ' + 'ghp_' + 'x' * 40)
        result = subprocess.run(['python', str(source / 'tools/package-v17.py'), str(self.folder / 'blocked-release')], capture_output=True, text=True)
        self.assertNotEqual(0, result.returncode)
        self.assertIn('疑似憑證', result.stderr)
        self.assertNotIn('x' * 40, result.stderr)
        self.assertFalse((self.folder / 'blocked-release').exists())


if __name__ == '__main__':
    unittest.main(verbosity=2)
