#!/usr/bin/env python3
"""V22 real archive/install tests using local fixtures, never GitHub or model downloads."""
from __future__ import annotations
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import stat
import struct
import subprocess
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / 'Install_and_Upload_MacGyver_v22.sh'
NAME = 'MacGyver_Engineering_Academy_v22'
MANIFEST = 'RELEASE_FILES_V22.json'
VERSION = '22.0.0'


def checksum(data):
    return hashlib.sha256(data).hexdigest()


def fixture(folder, *, split=False, change=None, unsafe=None, symlink=False, stored=False):
    content = {'macgyver.sh': b'#!/usr/bin/env bash\nprintf "%s\\n" "$@" > routed-args.txt\n',
               'public/academy/experience.html': b'<!doctype html><title>Walk</title>',
               'public/academy/walk-world-v22.js': b'export const version=22;',
               'run-local.sh': b'#!/usr/bin/env bash\nexit 0\n',
               'docs/example.txt': b'original'}
    content.update(change or {})
    manifest = {'version': VERSION, 'files': [{'path': name, 'bytes': len(data), 'sha256': checksum(data)} for name, data in sorted(content.items())]}
    content[MANIFEST] = (json.dumps(manifest) + '\n').encode()
    bins = [list(content)] if not split else [list(content)[i::4] for i in range(4)]
    archives = []
    for index, names in enumerate(bins, 1):
        name = NAME + '.zip' if not split else 'MacGyver_v22_Alternative_%d_of_4.zip' % index
        path = folder / name
        with zipfile.ZipFile(path, 'w', compression=zipfile.ZIP_STORED if stored else zipfile.ZIP_DEFLATED) as archive:
            for member in names:
                archive.writestr(NAME + '/' + member, content[member])
            if unsafe and index == 1:
                archive.writestr(unsafe, b'unsafe')
            if symlink and index == 1:
                info = zipfile.ZipInfo(NAME + '/bad-link')
                info.create_system = 3
                info.external_attr = (stat.S_IFLNK | 0o777) << 16
                archive.writestr(info, 'outside')
        archives.append({'filename': name, 'bytes': path.stat().st_size, 'sha256': checksum(path.read_bytes())})
    release = {'schema': 1, 'version': VERSION, 'root': NAME, 'archives': archives, 'releaseFilesSha256': checksum(content[MANIFEST])}
    (folder / 'RELEASE_ARCHIVES_V22.json').write_text(json.dumps(release))
    (folder / 'SHA256SUMS_V22.txt').write_text(''.join(a['sha256'] + '  ' + a['filename'] + '\n' for a in archives))
    shutil.copyfile(INSTALLER, folder / INSTALLER.name)
    return release


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='macgyver-v22-tests-')
        self.folder = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def run_installer(self, *args, okay=True):
        result = subprocess.run(['bash', str(self.folder / INSTALLER.name), *args], cwd=self.folder, capture_output=True, text=True)
        if okay:
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        else:
            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        return result

    def update_archive_checksum(self, release):
        for item in release['archives']:
            path = self.folder / item['filename']
            item.update(bytes=path.stat().st_size, sha256=checksum(path.read_bytes()))
        (self.folder / 'RELEASE_ARCHIVES_V22.json').write_text(json.dumps(release))
        (self.folder / 'SHA256SUMS_V22.txt').write_text(''.join(a['sha256'] + '  ' + a['filename'] + '\n' for a in release['archives']))

    def test_full_archive_installs_and_checks_manifest(self):
        fixture(self.folder)
        result = self.run_installer('--extract-only')
        self.assertIn('CRC', result.stdout)
        self.assertEqual((self.folder / NAME / 'docs/example.txt').read_text(), 'original')
        self.assertFalse((self.folder / NAME / 'routed-args.txt').exists())

    def test_four_archives_are_plain_zip_and_install_together(self):
        fixture(self.folder, split=True)
        for path in self.folder.glob('*.zip'):
            with zipfile.ZipFile(path) as archive:
                self.assertIsNone(archive.testzip())
        self.run_installer('--extract-only')
        self.assertTrue((self.folder / NAME / MANIFEST).is_file())

    def test_missing_part_fails_without_partial_install(self):
        fixture(self.folder, split=True)
        (self.folder / 'MacGyver_v22_Alternative_3_of_4.zip').unlink()
        self.run_installer('--extract-only', okay=False)
        self.assertFalse((self.folder / NAME).exists())

    def test_sha_failure_happens_before_install(self):
        fixture(self.folder)
        with (self.folder / (NAME + '.zip')).open('ab') as stream:
            stream.write(b'changed')
        self.run_installer('--extract-only', okay=False)
        self.assertFalse((self.folder / NAME).exists())

    def test_traversal_rejected(self):
        fixture(self.folder, unsafe=NAME + '/../escaped.txt')
        self.run_installer('--extract-only', okay=False)
        self.assertFalse((self.folder / 'escaped.txt').exists())
        self.assertFalse((self.folder / NAME).exists())

    def test_absolute_path_rejected(self):
        fixture(self.folder, unsafe='/escaped.txt')
        self.run_installer('--extract-only', okay=False)
        self.assertFalse((self.folder / NAME).exists())

    def test_windows_drive_rejected(self):
        fixture(self.folder, unsafe=NAME + '/C:/escaped.txt')
        self.run_installer('--extract-only', okay=False)
        self.assertFalse((self.folder / NAME).exists())

    def test_archive_symlink_rejected(self):
        fixture(self.folder, symlink=True)
        self.run_installer('--extract-only', okay=False)
        self.assertFalse((self.folder / NAME).exists())

    def test_crc_failure_rolls_back_staging(self):
        release = fixture(self.folder, stored=True)
        path = self.folder / (NAME + '.zip')
        with zipfile.ZipFile(path) as archive:
            info = archive.getinfo(NAME + '/docs/example.txt')
        data = bytearray(path.read_bytes())
        name_length, extra_length = struct.unpack_from('<HH', data, info.header_offset + 26)
        data[info.header_offset + 30 + name_length + extra_length] ^= 1
        path.write_bytes(data)
        self.update_archive_checksum(release)
        self.run_installer('--extract-only', okay=False)
        self.assertFalse((self.folder / NAME).exists())
        self.assertFalse(list(self.folder.glob('.macgyver-v22-unpack-*')))

    def test_case_collision_rejected(self):
        fixture(self.folder, unsafe=NAME + '/DOCS/Example.txt')
        self.run_installer('--extract-only', okay=False)
        self.assertFalse((self.folder / NAME).exists())

    def test_unlisted_file_rejected(self):
        fixture(self.folder, unsafe=NAME + '/extra-executable.sh')
        self.run_installer('--extract-only', okay=False)
        self.assertFalse((self.folder / NAME).exists())

    def test_existing_local_edits_and_new_files_survive_repeat(self):
        fixture(self.folder)
        self.run_installer('--extract-only')
        project = self.folder / NAME
        (project / 'docs/example.txt').write_text('my edit')
        (project / 'local-new.txt').write_text('keep me')
        (project / 'run-local.sh').unlink()
        self.run_installer('--extract-only')
        self.assertEqual((project / 'docs/example.txt').read_text(), 'my edit')
        self.assertEqual((project / 'local-new.txt').read_text(), 'keep me')
        self.assertTrue((project / 'run-local.sh').is_file())
        self.assertEqual((project / '.macgyver-updates-v22/docs/example.txt').read_text(), 'original')

    def test_pristine_files_update_and_edited_files_get_incoming_copy(self):
        fixture(self.folder)
        self.run_installer('--extract-only')
        project = self.folder / NAME
        (project / 'docs/example.txt').write_text('my edit')
        fixture(self.folder, change={'docs/example.txt': b'new release', 'public/academy/experience.html': b'updated page'})
        self.run_installer('--extract-only')
        self.assertEqual((project / 'docs/example.txt').read_text(), 'my edit')
        self.assertEqual((project / '.macgyver-updates-v22/docs/example.txt').read_text(), 'new release')
        self.assertEqual((project / 'public/academy/experience.html').read_text(), 'updated page')

    def test_existing_destination_symlink_rejected(self):
        fixture(self.folder)
        self.run_installer('--extract-only')
        project = self.folder / NAME
        (project / 'docs/example.txt').unlink()
        (project / 'docs/example.txt').symlink_to(self.folder / 'outside.txt')
        self.run_installer('--extract-only', okay=False)
        self.assertFalse((self.folder / 'outside.txt').exists())

    def test_mismatching_sums_rejected(self):
        fixture(self.folder)
        (self.folder / 'SHA256SUMS_V22.txt').write_text('0' * 64 + '  ' + NAME + '.zip\n')
        self.run_installer('--extract-only', okay=False)
        self.assertFalse((self.folder / NAME).exists())

    def test_upload_flags_and_paths_forward_without_shell_interpretation(self):
        fixture(self.folder)
        result = self.run_installer('--dry-run', '--with-assets', '--models-dir', 'models with spaces', '--documents-dir', 'docs-$(touch BAD)', '--state', 'outside-state', '--batch-mib', '80')
        routed = (self.folder / NAME / 'routed-args.txt').read_text().splitlines()
        self.assertEqual(routed[0:3], ['all', '--dry-run', '--with-assets'])
        self.assertIn(str(self.folder / 'models with spaces'), routed)
        self.assertIn(str(self.folder / 'docs-$(touch BAD)'), routed)
        self.assertFalse((self.folder / NAME / 'BAD').exists())
        self.assertIn('--batch-mib', routed)

    def test_source_checkout_delegates_to_existing_entry_point(self):
        fixture(self.folder)
        self.run_installer('--extract-only')
        project = self.folder / NAME
        shutil.copyfile(INSTALLER, project / INSTALLER.name)
        result = subprocess.run(['bash', str(project / INSTALLER.name), '--dry-run'], cwd=self.folder, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual((project / 'routed-args.txt').read_text().splitlines(), ['all', '--dry-run'])

    def test_asset_paths_need_explicit_asset_flag(self):
        fixture(self.folder)
        self.run_installer('--models-dir', 'models', okay=False)
        self.assertFalse((self.folder / NAME).exists())

    def test_packager_and_embedded_installer_work_without_external_json(self):
        source = self.folder / 'source'
        output = self.folder / 'release'
        (source / 'tools').mkdir(parents=True)
        (source / 'docs').mkdir()
        (source / 'public/academy').mkdir(parents=True)
        (source / 'docs/VALIDATION_V22.json').write_text('{"status":"PASS"}')
        (source / 'macgyver.sh').write_text('#!/usr/bin/env bash\nexit 0\n')
        (source / 'public/academy/experience.html').write_text('<title>Package fixture</title>')
        (source / 'run-local.sh').write_text('#!/usr/bin/env bash\nexit 0\n')
        shutil.copyfile(INSTALLER, source / INSTALLER.name)
        shutil.copyfile(ROOT / 'tools/package-v22.py', source / 'tools/package-v22.py')
        result = subprocess.run(['python3', str(source / 'tools/package-v22.py'), str(output), '--split'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(len(list(output.glob('*.zip'))), 5)
        (output / (NAME + '.zip')).unlink()
        (output / 'RELEASE_ARCHIVES_V22.json').unlink()
        result = subprocess.run(['bash', str(output / INSTALLER.name), '--extract-only'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertTrue((output / NAME / 'public/academy/experience.html').is_file())
        report = json.loads((output / 'PACKAGE_VALIDATION_V22.json').read_text())
        self.assertEqual(report['zipCRC'], 'PASS')

    def test_packager_excludes_credentials_weights_and_atomic_leftovers(self):
        spec = importlib.util.spec_from_file_location('pack22', ROOT / 'tools/package-v22.py')
        package = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(package)
        source = self.folder / 'source'
        names = ['public/academy/walk-world-v22.js', 'public/academy/assets/photos/.photo.jpg.tmpXYZ',
                 'public/academy/data/.atomic-json.abc', 'credentials/token.json', 'models/model.gguf',
                 '.env', '.env.example', '.github/workflows/pages.yml', '.openai/hosting.json',
                 'public/academy/photo.jpg', 'docs/guide.md', 'docs/guide.md.bak', '.git/config']
        for name in names:
            path = source / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('fixture')
        selected = {p.relative_to(source).as_posix() for p in package.source_files(source)}
        self.assertEqual(selected, {'public/academy/walk-world-v22.js', '.env.example', '.github/workflows/pages.yml', '.openai/hosting.json', 'public/academy/photo.jpg', 'docs/guide.md'})


if __name__ == '__main__':
    unittest.main(verbosity=2)
