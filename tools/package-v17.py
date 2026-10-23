#!/usr/bin/env python3
"""Package V17 after final validation; produce a self-contained verified installer.

Example: python3 tools/package-v17.py /absolute/release/folder --parts
The four Alternative files are independent ordinary ZIPs extracted to one root.
This tool does not upload, publish, or download model weights.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
VERSION = '17.0.0'
ROOT_NAME = 'MacGyver_Engineering_Academy_v17'
INSTALLER = 'Install_and_Upload_MacGyver_v17.sh'
EMBED_MARKER = "EMBEDDED_ARCHIVES_JSON = ''  # @MACGYVER_V17_ARCHIVE_MANIFEST@"
BLOCKED_DIRS = {'.git', '.venv', 'venv', 'node_modules', '__pycache__', '.pytest_cache',
                '.next', '.vinext', '.wrangler', 'coverage', 'owner-private',
                'credentials', 'secrets', 'uploads', 'user-data', 'userdata',
                'github-pages', '.macgyver-state', '.sites-runtime', '.agents', '.codex',
                '.ssh', '.aws', '.azure', '.gnupg', 'gcloud', 'owner-kit', 'outputs', 'work'}
BLOCKED_FILES = {'id_rsa', 'id_ed25519', 'id_ecdsa', 'id_dsa', '.netrc', '.git-credentials',
                 '.gitconfig', 'credentials.json', 'tokens.json', 'token.json', 'cookies.txt',
                 'cookies.json', 'accounts.json', 'users.json', 'owner.json', '.ds_store'}
WEIGHTS = {'.gguf', '.safetensors', '.onnx', '.bin', '.pt', '.pth', '.ckpt', '.model',
           '.h5', '.hdf5', '.pb', '.npy', '.npz', '.pkl', '.pickle', '.keras'}
BLOCKED_SUFFIXES = WEIGHTS | {'.pyc', '.sqlite', '.sqlite3', '.db', '.pem', '.key', '.p12', '.pfx',
                            '.tar', '.tgz', '.7z'}
SECRETS = re.compile(rb'(?:github_pat_[A-Za-z0-9_]{30,}|gh[pousr]_[A-Za-z0-9_]{30,}|(?<![A-Za-z0-9_])sk-(?:proj-)?[A-Za-z0-9_-]{40,}|-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----)')
SECRET_PREFIXES = (b'github_pat_', b'ghp_', b'gho_', b'ghu_', b'ghs_', b'ghr_', b'sk-', b'-----BEGIN ')


def permitted(path, root=ROOT):
    relative = path.relative_to(root)
    parts = tuple(part.casefold() for part in relative.parts)
    name, suffix = path.name.casefold(), path.suffix.casefold()
    if any(part in BLOCKED_DIRS for part in parts) or parts[:2] == ('portable', 'data'):
        return False
    if 'local-documents' in parts or ('models' in parts and name != 'readme.md'):
        return False
    if any(part.startswith('.env') and part != '.env.example' for part in parts):
        return False
    if suffix in BLOCKED_SUFFIXES or name in BLOCKED_FILES:
        return False
    # Small downloadable lesson kits are part of the website. Arbitrary nested
    # release/private ZIPs are not copied into the public source distribution.
    if suffix == '.zip' and parts[:4] != ('public', 'academy', 'assets', 'labs'):
        return False
    if name.startswith(('owner-bootstrap', 'owner_bootstrap')) or name.endswith(('-wal', '-shm', '.part', '.tmp', '.download', '.tsbuildinfo')):
        return False
    if suffix in {'.zip', '.gz', '.bz2', '.xz'} and any(marker in name.replace('_', '-') for marker in ('owner-private', 'private-owner', 'private-models')):
        return False
    return path.is_file() and not path.is_symlink()


def source_files(root=ROOT):
    files = []
    for folder, directories, names in os.walk(root, followlinks=False):
        parent = Path(folder)
        directories[:] = sorted(name for name in directories if name.casefold() not in BLOCKED_DIRS and not (parent / name).is_symlink())
        for name in sorted(names):
            path = parent / name
            if permitted(path, root):
                files.append(path)
    return sorted(files)


def digest(path, check_secrets=False):
    result, tail = hashlib.sha256(), b''
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(4 * 1024 * 1024), b''):
            if check_secrets:
                data = tail + block
                # Every secret pattern starts with one of these byte prefixes.
                # C-level byte search avoids regex-scanning gigabytes of images
                # and generated lesson text that contain none of the prefixes.
                if any(prefix in data for prefix in SECRET_PREFIXES) and SECRETS.search(data):
                    raise ValueError('疑似憑證內容，停止打包；未顯示秘密：' + str(path.relative_to(ROOT)))
            result.update(block)
            tail = block[-256:]
    return result.hexdigest()


def write_text(path, content):
    if path.is_symlink():
        raise ValueError('Output must not be a symbolic link: ' + str(path))
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=path.parent, prefix='.' + path.name, delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(content)
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def make_archive(path, files, expected):
    if path.is_symlink():
        raise ValueError('Archive output must not be a symbolic link.')
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, prefix='.' + path.name, delete=False) as stream:
            temporary = Path(stream.name)
        with zipfile.ZipFile(temporary, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6, allowZip64=True) as archive:
            for source in files:
                relative = source.relative_to(ROOT).as_posix()
                archive.write(source, ROOT_NAME + '/' + relative)
        # Reading each member also verifies ZIP CRC. Check against the snapshot
        # hash so a concurrent edit cannot create a silently inconsistent release.
        with zipfile.ZipFile(temporary) as archive:
            for info in archive.infolist():
                relative = info.filename[len(ROOT_NAME) + 1:]
                checksum = hashlib.sha256()
                with archive.open(info) as stream:
                    for block in iter(lambda: stream.read(4 * 1024 * 1024), b''):
                        checksum.update(block)
                if checksum.hexdigest() != expected[relative]:
                    raise ValueError('Source changed while packaging: ' + relative)
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    return {'filename': path.name, 'bytes': path.stat().st_size, 'sha256': digest(path), 'files': len(files)}


def build_installer(template, manifest):
    if template.count(EMBED_MARKER) != 1:
        raise ValueError('Installer must contain exactly one archive-manifest placeholder.')
    embedded = json.dumps(manifest, ensure_ascii=False, separators=(',', ':'))
    return template.replace(EMBED_MARKER, 'EMBEDDED_ARCHIVES_JSON = ' + repr(embedded) + '  # generated for this release')


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('output', type=Path, help='Release folder outside the source tree')
    parser.add_argument('--parts', action='store_true', help='Also create four ordinary Alternative ZIP files')
    parser.add_argument('--validation-report', type=Path, default=ROOT / 'docs/VALIDATION_V17.json')
    parser.add_argument('--check-only', action='store_true', help='Check validation and source policy; do not write manifests or ZIPs')
    args = parser.parse_args()
    output = args.output.expanduser().resolve()
    if output == ROOT or ROOT in output.parents:
        raise ValueError('Output must be outside the source tree.')
    report = json.loads(args.validation_report.read_text(encoding='utf-8'))
    if report.get('status') != 'PASS':
        raise ValueError('A final passing docs/VALIDATION_V17.json report is required.')
    template = (ROOT / INSTALLER).read_text(encoding='utf-8')
    if template.count(EMBED_MARKER) != 1:
        raise ValueError('Use the source installer template, not an installer stamped for an older release.')
    files = source_files()
    seen = set()
    for path in files:
        key = path.relative_to(ROOT).as_posix().casefold()
        if key in seen:
            raise ValueError('Case-insensitive path collision: ' + str(path))
        seen.add(key)
    skip_manifests = {'RELEASE_FILES_V17.json', 'SHA256SUMS', 'SHA256SUMS_V17.txt'}
    entries = [{'path': path.relative_to(ROOT).as_posix(), 'bytes': path.stat().st_size,
                'sha256': digest(path, check_secrets=True)} for path in files if path.relative_to(ROOT).as_posix() not in skip_manifests]
    if args.check_only:
        print(json.dumps({'status': 'PASS', 'publicFiles': len(entries), 'bytes': sum(item['bytes'] for item in entries), 'archivesCreated': False}))
        return
    output.mkdir(parents=True, exist_ok=True)
    manifest = ROOT / 'RELEASE_FILES_V17.json'
    write_text(manifest, json.dumps({'version': VERSION, 'files': entries, 'privateOwnerDataIncluded': False, 'modelWeightsIncluded': False}, ensure_ascii=False, indent=2) + '\n')
    files = sorted({path for path in files if path.relative_to(ROOT).as_posix() not in skip_manifests} | {manifest})
    expected = {item['path']: item['sha256'] for item in entries}
    expected[manifest.name] = digest(manifest)
    sums = ROOT / 'SHA256SUMS'
    write_text(sums, ''.join(expected[path.relative_to(ROOT).as_posix()] + '  ' + path.relative_to(ROOT).as_posix() + '\n' for path in files))
    expected[sums.name] = digest(sums)
    files = sorted({*files, sums})
    archives = [make_archive(output / (ROOT_NAME + '.zip'), files, expected)]
    if args.parts:
        bins, sizes = [[] for _ in range(4)], [0] * 4
        for path in sorted(files, key=lambda item: item.stat().st_size, reverse=True):
            index = min(range(4), key=lambda number: sizes[number])
            bins[index].append(path)
            sizes[index] += path.stat().st_size
        for index, part in enumerate(bins, 1):
            archives.append(make_archive(output / ('MacGyver_v17_Alternative_%d_of_4.zip' % index), sorted(part), expected))
    release = {'schema': 1, 'version': VERSION, 'root': ROOT_NAME, 'archives': archives,
               'releaseFilesSha256': expected[manifest.name],
               'privateOwnerDataIncluded': False, 'modelWeightsIncluded': False}
    release_path = output / 'RELEASE_ARCHIVES_V17.json'
    write_text(release_path, json.dumps(release, ensure_ascii=False, indent=2) + '\n')
    installer = output / INSTALLER
    write_text(installer, build_installer(template, release))
    installer.chmod(0o755)
    validation_path = output / 'PACKAGE_VALIDATION_V17.json'
    write_text(validation_path, json.dumps({'status': 'PASS', 'version': VERSION, 'zipCRC': 'PASS',
               'archivedFileHashes': 'PASS', 'installerHasCurrentArchiveHashes': True,
               'archives': archives, 'publicSourceFiles': len(files),
               'uncompressedBytes': sum(path.stat().st_size for path in files),
               'privateOwnerDataIncluded': False, 'modelWeightsIncluded': False}, indent=2) + '\n')
    checks = [(item['filename'], item['sha256']) for item in archives]
    checks += [(path.name, digest(path)) for path in (release_path, installer, validation_path)]
    write_text(output / 'SHA256SUMS_V17.txt', ''.join(checksum + '  ' + name + '\n' for name, checksum in checks))
    write_text(output / (ROOT_NAME + '.zip.sha256'), ''.join(item['sha256'] + '  ' + item['filename'] + '\n' for item in archives))
    print(json.dumps({'archives': archives, 'installer': str(installer), 'publicFiles': len(files)}))


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, KeyError, zipfile.BadZipFile) as error:
        parser_message = 'Packaging stopped: ' + str(error)
        raise SystemExit(parser_message)
