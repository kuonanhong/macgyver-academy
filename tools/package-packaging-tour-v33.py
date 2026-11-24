#!/usr/bin/env python3
"""Package the verified packaging cinema, 120-activity atlas and completed C01 film.

This never builds or publishes the academy and never collects its course data.
The final six-film manifest and validation report must already exist and pass.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
import math
import os
from pathlib import Path
import re
import stat
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = 'MacGyver_Packaging_Tour_v33'
TOURS = ('interposer', 'fanout', 'hybrid', 'bridge', 'chiplet', 'thermal')
LANGUAGES = ('zh-TW', 'en', 'ja', 'ko', 'zh-CN')
ASSETS = 'public/academy/assets/packaging-tour-v33'
FIXED_FILES = (
    'README_PACKAGING_TOUR_V33.html',
    'requirements-packaging-media-v34.txt',
    'docs/PACKAGING_MEDIA_ENVIRONMENT_V34.json',
    'Start_Packaging_Tour_v33.sh',
    'Upload_Packaging_YouTube_v33.sh',
    'tools/publish-packaging-youtube-v33.py',
    'tools/test-publish-packaging-youtube-v33.py',
    'docs/PACKAGING_YOUTUBE_METADATA_V33.json',
    'tools/preview-packaging-tour-v33.py',
    'tools/export-packaging-subtitles-v33.mjs',
    'tools/finalize-packaging-videos-v33.py',
    'tools/add-line-qr-packaging-v33.py',
    'tools/test-packaging-tour-v33.mjs',
    'tools/package-packaging-tour-v33.py',
    'public/academy/packaging-youtube-v33.js',
    'public/academy/packaging-narration-v33.js',
    'public/academy/packaging-captions-v33.js',
    'public/academy/packaging-media-v33.js',
    'tools/export-bilingual-packaging-subtitles-v33.py',
    'tools/test-bilingual-packaging-subtitles-v33.py',
    'Upload_Narrated_V34.sh',
    'tools/build-native-narration-v34.py',
    'tools/test-native-narration-duration-v34.py',
    'tools/collect-packaging-narration-v34.py',
    'tools/build-all-packaging-narration-v34.py',
    'tools/mux-narrated-packaging-v34.py',
    'tools/prepare-narrated-youtube-job-v34.py',
    'tools/build-c01-narrated-job-v34.py',
    'tools/test-narrated-packaging-v34.py',
    'tools/build-speech-aligned-subtitles-v34.py',
    'docs/PACKAGING_YOUTUBE_METADATA_V34.json',
    'docs/PACKAGING_PROCESS_C01_YOUTUBE_METADATA_V34.json',
    'tools/preview-packaging-process-v34.py',
    'tools/test-packaging-process-v34.mjs',
    'tools/test-packaging-process-scene-v34.mjs',
    'tools/test-packaging-process-player-v34.mjs',
    'tools/build-c01-semantic-mapping-v34.mjs',
    'docs/PACKAGING_PROCESS_ROADMAP_V34.json',
    'docs/packaging-process-scripts-v34/C01.json',
    'public/academy/packaging-process-v34.html',
    'public/academy/packaging-process-v34.css',
    'public/academy/packaging-process-v34.js',
    'public/academy/packaging-process-data-v34.js',
    'public/academy/packaging-process-c01-v34.js',
    'public/academy/packaging-process-scene-v34.js',
    'public/academy/packaging-process-film-v34.html',
    'public/academy/packaging-process-film-v34.js',
    'public/academy/packaging-process-film-v34.css',
    'public/academy/packaging-process-media-v34.js',
    'public/academy/packaging-process-captions-v34.js',
    'public/academy/packaging-process-studio-v34.html',
    'public/academy/packaging-process-studio-v34.js',
    'public/academy/packaging-tour-v33.html',
    'public/academy/packaging-tour-v33.js',
    'public/academy/packaging-tour-v33.css',
    'public/academy/packaging-tour-content-v33.js',
    'public/academy/packaging-tour-scene-v33.js',
    'public/academy/vendor/three.js',
    'public/academy/assets/brand/logo-static.svg',
    'public/academy/assets/brand/favicon.svg',
    'docs/PACKAGING_TOUR_SOURCES_V33.md',
    'docs/VALIDATION_PACKAGING_TOUR_V33.json',
)
THREE_LICENSES = (
    'public/academy/vendor/THREE-LICENSE.txt',
    'public/academy/vendor/three-license.txt',
    'public/academy/vendor/three.LICENSE',
    'public/academy/vendor/three-license',
)
BLOCK_SIZE = 1024 * 1024


def fail(message: str):
    raise ValueError(message)


def sha256_file(file: Path) -> str:
    digest = hashlib.sha256()
    with file.open('rb') as stream:
        for block in iter(lambda: stream.read(BLOCK_SIZE), b''):
            digest.update(block)
    return digest.hexdigest()


def checked_file(root: Path, relative: str) -> Path:
    rel = Path(relative)
    if rel.is_absolute() or '..' in rel.parts or any(p.startswith('.') for p in rel.parts):
        fail('Unsafe package path: ' + relative)
    source = root / rel
    current = root
    for part in rel.parts:
        current /= part
        if current.is_symlink():
            fail('Symlinks are not package inputs: ' + relative)
    if not source.is_file() or not source.resolve().is_relative_to(root):
        fail('Required package input is absent or unsafe: ' + relative)
    return source


def read_json(root: Path, relative: str):
    return json.loads(checked_file(root, relative).read_text('utf-8'))


def check_films(root: Path):
    manifest = read_json(root, ASSETS + '/videos/manifest.json')
    if manifest.get('status') != 'PASS':
        fail('Film manifest must have status PASS.')
    if manifest.get('silent') is not False:
        fail('The new delivery requires narrated films, not silent originals.')
    films = manifest.get('videos')
    if not isinstance(films, list) or len(films) != len(TOURS):
        fail('Six finalized films are required; a partial manifest cannot be packaged.')
    if sorted(v.get('id', '') for v in films) != sorted(TOURS):
        fail('The film manifest must contain each of the six tour IDs exactly once.')
    for film in films:
        identity = film['id']
        if not isinstance(film.get('duration'), (int, float)) or not math.isclose(
                film['duration'], 300.0, rel_tol=0, abs_tol=0.001):
            fail(identity + ': duration must be exactly 300 seconds (within 1 ms).')
        if film.get('frames') != 7200 or Fraction(str(film.get('fps', '0'))) != 24:
            fail(identity + ': expected 7,200 frames at 24 fps.')
        if (film.get('width'), film.get('height'), film.get('chapters')) != (1280, 720, 10):
            fail(identity + ': expected 1280×720 and ten chapters.')
        if sorted(film.get('subtitleLanguages', [])) != sorted(LANGUAGES):
            fail(identity + ': all five subtitle languages are required.')
        if sorted(film.get('audioLanguages', [])) != sorted(LANGUAGES):
            fail(identity + ': all five actual narration tracks are required.')
        file = checked_file(root, ASSETS + '/videos/' + identity + '.mp4')
        digest = film.get('sha256', '')
        if not re.fullmatch(r'[0-9a-f]{64}', digest) or file.stat().st_size != film.get('bytes'):
            fail(identity + ': manifest file size/hash is missing or invalid.')
        if sha256_file(file) != digest:
            fail(identity + ': finalized MP4 no longer matches its verified manifest.')
    report = read_json(root, 'docs/VALIDATION_PACKAGING_TOUR_V33.json')
    if report.get('status') != 'PASS':
        fail('Final docs/VALIDATION_PACKAGING_TOUR_V33.json must have status PASS.')
    if report.get('mediaVerification') != manifest:
        fail('Validation report is stale: mediaVerification must match the finalized film manifest.')
    source_hashes = report.get('sourceHashes', {})
    for relative in ('public/academy/packaging-tour-content-v33.js',
                     'public/academy/packaging-tour-scene-v33.js'):
        if source_hashes.get(relative) != sha256_file(checked_file(root, relative)):
            fail('Validation report is stale: revalidate changed content/scene before packaging: ' + relative)
    return manifest


def collect(root: Path) -> list[str]:
    selected = set(FIXED_FILES)
    for relative in THREE_LICENSES:
        if (root / relative).exists():
            selected.add(relative)
    vendor = root / 'public/academy/vendor/mediabunny'
    if vendor.is_symlink() or not vendor.is_dir():
        fail('The bundled Mediabunny directory is absent or unsafe.')
    for file in vendor.rglob('*'):
        if file.is_symlink():
            fail('Unexpected vendor symlink: ' + str(file))
        if not file.is_file() or file.name.endswith('.d.ts'):
            continue
        if file.suffix.lower() not in {'.js', '.mjs', '.txt', '.md', '.map'} and file.name not in {'LICENSE', 'NOTICE'}:
            fail('Unexpected vendor input: ' + str(file.relative_to(root)))
        selected.add(file.relative_to(root).as_posix())
    for required in ('mediabunny-1.66.2.min.mjs', 'LICENSE', 'SOURCE.txt'):
        if 'public/academy/vendor/mediabunny/' + required not in selected:
            fail('Bundled Mediabunny runtime/license/source reference missing: ' + required)

    # Exact asset families prevent accidentally packaging owner course content,
    # recordings-in-progress, credentials, or unrelated files in the source tree.
    expected_assets = {'videos/manifest.json', 'videos/hosting.json', 'line-530pgchc-qr.png', 'line-530pgchc-endcard.png'}
    for identity in TOURS:
        expected_assets.add('videos/' + identity + '.mp4')
        expected_assets.add('transcripts/' + identity + '.ffmetadata')
        for second in (15, 135, 225):
            expected_assets.add(f'stills/{identity}-{second}.jpg')
        for language in LANGUAGES:
            expected_assets.add(f'subtitles/{identity}.{language}.vtt')
            expected_assets.add(f'subtitles-bilingual/{identity}.{language}.vtt')
            expected_assets.add(f'subtitles-bilingual/{identity}.{language}.srt')
            expected_assets.add(f'audio/{identity}.{language}.m4a')
            expected_assets.add(f'transcripts/{identity}.{language}.json')
    asset_root = root / ASSETS
    for file in asset_root.rglob('*'):
        if file.is_symlink():
            fail('Unexpected asset symlink: ' + str(file))
        if file.is_file() and file.relative_to(asset_root).as_posix() not in expected_assets:
            fail('Unreviewed file in the tour asset folder: ' + str(file.relative_to(root)))
    selected.update(ASSETS + '/' + rel for rel in expected_assets)
    process_base = 'public/academy/assets/packaging-process-v34'
    process_assets = {'roadmap.json', 'C01/script.json', 'C01/poster.png', 'C01/C01.mp4', 'C01/manifest.json'}
    for language in LANGUAGES:
        process_assets.add(f'C01/audio/C01.{language}.m4a')
        process_assets.add(f'C01/subtitles/C01.{language}.vtt')
        process_assets.add(f'C01/subtitles/C01.{language}.srt')
    for file in (root / process_base).rglob('*'):
        if file.is_symlink() or (file.is_file() and file.relative_to(root / process_base).as_posix() not in process_assets):
            fail('Unreviewed process asset: ' + str(file.relative_to(root)))
    selected.update(process_base + '/' + rel for rel in process_assets)
    process_manifest = read_json(root, process_base + '/C01/manifest.json')
    process_file = checked_file(root, process_base + '/C01/C01.mp4')
    if (process_manifest.get('status') != 'PASS' or process_manifest.get('durationSeconds') != 300
            or process_manifest.get('sha256') != sha256_file(process_file)
            or process_manifest.get('bytes') != process_file.stat().st_size
            or set(process_manifest.get('audioLanguages', [])) != set(LANGUAGES)
            or set(process_manifest.get('subtitleLanguages', [])) != set(LANGUAGES)):
        fail('C01 process film must match its verified five-language manifest.')
    for relative in selected:
        checked_file(root, relative)
    return sorted(selected)


def redirect(target: str, label: str) -> bytes:
    # Retain tour/language query strings and hashes for file:// and HTTP entrypoints.
    return (
        '<!doctype html><html lang="zh-Hant"><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<title>MacGyver Engineering Cinema</title><script>location.replace('
        + json.dumps(target) + '+location.search+location.hash);</script>'
        '<p><a href="' + target + '">' + label + '</a></p></html>\n'
    ).encode('utf-8')


def serial(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8')


def verify_zip(archive: Path, expected: dict):
    with zipfile.ZipFile(archive) as z:
        if z.testzip() is not None:
            fail('ZIP CRC verification failed.')
        names = z.namelist()
        wanted = {PACKAGE + '/' + name for name in expected}
        if len(names) != len(wanted) or set(names) != wanted:
            fail('ZIP contains unexpected, duplicate, or missing entries.')
        for relative, item in expected.items():
            info = z.getinfo(PACKAGE + '/' + relative)
            if info.file_size != item['bytes']:
                fail('Archived file size changed: ' + relative)
            digest = hashlib.sha256()
            with z.open(info) as stream:
                for block in iter(lambda: stream.read(BLOCK_SIZE), b''):
                    digest.update(block)
            if digest.hexdigest() != item['sha256']:
                fail('Archived file hash changed: ' + relative)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=ROOT, help='Complete V32 source containing the v33 tour.')
    parser.add_argument('--out', type=Path, default=ROOT.parent / 'MacGyver_Packaging_Tour_Experiment', help='Destination directory, outside the source tree.')
    parser.add_argument('--check-only', action='store_true', help='Check the six-film manifest and precise input list without writing anything.')
    args = parser.parse_args()
    root = args.source.resolve()
    output = args.out.resolve()
    if output == root or output.is_relative_to(root):
        fail('Choose an output directory outside the source tree.')
    manifest = check_films(root)
    files = collect(root)
    if args.check_only:
        print(json.dumps({'status': 'PASS', 'mode': 'check-only', 'films': 6, 'sourceFiles': len(files), 'sourceBytes': sum((root / p).stat().st_size for p in files)}))
        return
    expected = {}
    for relative in files:
        source = checked_file(root, relative)
        expected[relative] = {'bytes': source.stat().st_size, 'sha256': sha256_file(source)}
    generated = {
        'index.html': redirect('public/academy/packaging-tour-v33.html', '開啟封裝俯瞰導覽 / Open packaging tours'),
        'public/academy/index.html': redirect('https://kuonanhong.github.io/macgyver-academy/', '回到線上工程學院 / Open the online academy'),
    }
    for relative, raw in generated.items():
        expected[relative] = {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}
    generated['PACKAGE_FILES_V33.json'] = serial({'package': PACKAGE, 'version': manifest['version'], 'files': expected})
    raw = generated['PACKAGE_FILES_V33.json']
    expected['PACKAGE_FILES_V33.json'] = {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}

    output.mkdir(parents=True, exist_ok=True)
    destination = output / (PACKAGE + '.zip')
    fd, temp_name = tempfile.mkstemp(prefix=PACKAGE + '-', suffix='.zip.partial', dir=output)
    os.close(fd)
    temporary = Path(temp_name)
    try:
        with zipfile.ZipFile(temporary, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6, allowZip64=True) as z:
            for relative in files:
                source = checked_file(root, relative)
                info = zipfile.ZipInfo.from_file(source, arcname=PACKAGE + '/' + relative)
                info.compress_type = zipfile.ZIP_STORED if source.suffix.lower() in {'.mp4', '.m4a', '.jpg', '.jpeg', '.png', '.webp'} else zipfile.ZIP_DEFLATED
                info.external_attr = (stat.S_IFREG | stat.S_IMODE(source.stat().st_mode)) << 16
                with source.open('rb') as stream, z.open(info, 'w') as target:
                    for block in iter(lambda: stream.read(BLOCK_SIZE), b''):
                        target.write(block)
            for relative, body in generated.items():
                info = zipfile.ZipInfo(PACKAGE + '/' + relative)
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = (stat.S_IFREG | 0o644) << 16
                z.writestr(info, body)
        verify_zip(temporary, expected)
        for relative in files:
            source = checked_file(root, relative)
            if source.stat().st_size != expected[relative]['bytes'] or sha256_file(source) != expected[relative]['sha256']:
                fail('Source changed while packaging; retry after edits finish: ' + relative)
        os.replace(temporary, destination)
    finally:
        temporary.unlink(missing_ok=True)
    archive_sha = sha256_file(destination)
    report = {
        'status': 'PASS', 'package': PACKAGE, 'version': manifest['version'],
        'createdAt': datetime.now(timezone.utc).isoformat(),
        'archive': destination.name, 'bytes': destination.stat().st_size, 'sha256': archive_sha,
        'files': len(expected), 'sourceFiles': len(files), 'generatedFiles': list(generated),
        'uncompressedBytes': sum(item['bytes'] for item in expected.values()),
        'zipCRC': 'PASS', 'archivedFileHashes': 'PASS', 'sourceUnchangedDuringPackaging': 'PASS',
        'videos': manifest['videos'], 'videoMetadataBasis': 'Finalized PASS manifest; every MP4 SHA-256 and size reverified.',
        'overviewFilms': 6, 'processFilms': 1, 'processRoadmapItems': 120,
        'audioFiles': 35, 'bilingualVttFiles': 35, 'bilingualSrtFiles': 35, 'legacySingleLanguageSubtitleFiles': 30,
        'stillImages': 18, 'privateCourseDataIncluded': False,
        'typeDeclarationsIncluded': False,
    }
    report_path = output / 'PACKAGE_VALIDATION_PACKAGING_TOUR_V33.json'
    report_path.write_bytes(serial(report))
    sums = archive_sha + '  ' + destination.name + '\n' + sha256_file(report_path) + '  ' + report_path.name + '\n'
    (output / 'SHA256SUMS_PACKAGING_TOUR_V33.txt').write_text(sums, 'utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, KeyError, TypeError, zipfile.BadZipFile) as error:
        raise SystemExit('Packaging refused: ' + str(error)) from error
