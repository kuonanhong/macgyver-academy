#!/usr/bin/env python3
"""Publish verified cinema assets to the academy's GitHub Release, then enable Pages URLs.

Requires an existing authenticated gh CLI. Never accepts or stores credentials.
Existing remote assets must have the same SHA-256; this tool never overwrites them.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
REPO = 'kuonanhong/macgyver-academy'
IDS = ('interposer', 'fanout', 'hybrid', 'bridge', 'chiplet', 'thermal')
LANGUAGES = {'zh-TW', 'zh-CN', 'en', 'ja', 'ko'}
BASE = ROOT / 'public/academy/assets/packaging-tour-v33/videos'


def gh(*args, allow_missing=False):
    result = subprocess.run(['gh', *args], text=True, capture_output=True,
                            env={**os.environ, 'GH_PROMPT_DISABLED': '1'})
    if result.returncode:
        if allow_missing and ('HTTP 404' in result.stderr or 'release not found' in result.stderr.lower()):
            return None
        raise ValueError('GitHub operation failed: ' + result.stderr.strip()[:600])
    return result.stdout


def sha(path):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def local_assets():
    manifest = json.loads((BASE / 'manifest.json').read_text('utf-8'))
    films = manifest.get('videos', [])
    if manifest.get('status') != 'PASS' or {v.get('id') for v in films} != set(IDS) or len(films) != 6:
        raise ValueError('All six finalized films must pass before release publication.')
    assets = []
    for item in films:
        path = BASE / (item['id'] + '.mp4')
        if (path.is_symlink() or not path.is_file() or path.stat().st_size != item.get('bytes')
                or sha(path) != item.get('sha256') or item.get('duration') != 300
                or set(item.get('audioLanguages', [])) != LANGUAGES
                or set(item.get('subtitleLanguages', [])) != LANGUAGES
                or item.get('chapters') != 10 or item.get('frames') != 7200
                or (item.get('width'), item.get('height')) != (1280, 720)
                or item.get('verification', {}).get('status') != 'PASS'
                or item.get('verification', {}).get('qrDecoded', {}).get('status') != 'PASS'):
            raise ValueError('Unverified narrated film: ' + item['id'])
        assets.append((path, item))
    return assets


def atomic_text(path, value):
    fd, temporary = tempfile.mkstemp(prefix='.' + path.name, dir=path.parent)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as stream:
            stream.write(value)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def verify_remote(release, assets, tag):
    if release.get('tag_name') != tag:
        raise ValueError('Release tag mismatch.')
    remote = {a['name']: a for a in release.get('assets', [])}
    for path, item in assets:
        found = remote.get(path.name)
        expected_url = f'https://github.com/{REPO}/releases/download/{tag}/{path.name}'
        if not found or (found.get('state') != 'uploaded' or found.get('size') != item['bytes']
                         or found.get('digest') != 'sha256:' + item['sha256']
                         or found.get('browser_download_url') != expected_url):
            raise ValueError('Remote asset size/SHA-256/URL mismatch: ' + path.name)
    return remote


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--tag', default='packaging-tours-v33.0.3')
    ap.add_argument('--target', default='main', help='Existing public branch or full commit SHA.')
    ap.add_argument('--publish', action='store_true', help='Upload, verify and publish; otherwise local validation only.')
    args = ap.parse_args()
    if not re.fullmatch(r'packaging-tours-v[0-9.]+', args.tag):
        raise ValueError('Expected an explicit packaging-tours version tag.')
    if args.target != 'main' and not re.fullmatch(r'[0-9a-f]{40}', args.target):
        raise ValueError('Target must be main or a full public commit SHA.')
    assets = local_assets()
    if not args.publish:
        print(json.dumps({'status': 'PASS', 'mode': 'local-check', 'films': len(assets), 'tag': args.tag}))
        return
    endpoint = f'repos/{REPO}/releases/tags/{args.tag}'
    raw = gh('api', endpoint, allow_missing=True)
    if raw is None:
        notes = ('Six 5-minute introductory advanced semiconductor packaging tours.\n\n'
                 'Each MP4 contains 5 narration tracks, bilingual captions, 10 chapters and the LINE QR end card. '
                 'Languages: Traditional Chinese, Simplified Chinese, English, Japanese and Korean. '
                 'Select an audio/subtitle track in a compatible media player.\n\n'
                 'These are illustrative 3D models, not factory drone footage or validated process recipes. '
                 'The 120-activity process roadmap is a separate production series. '
                 'Longer YouTube lessons are produced and tracked separately; these downloads are the introductory tours.\n\n'
                 'Academy: https://kuonanhong.github.io/macgyver-academy/\n'
                 'AERO Explorer: https://kuonanhong.github.io/AERO_Explorer/\n'
                 'LINE: https://line.me/R/ti/p/%40530pgchc\n')
        with tempfile.TemporaryDirectory(prefix='macgyver-release-') as tmp:
            file = Path(tmp) / 'notes.txt'
            file.write_text(notes, 'utf-8')
            gh('release', 'create', args.tag, '--repo', REPO, '--draft', '--latest=false',
               '--target', args.target, '--title', '先進封裝五語俯瞰導覽 · V33.0.3', '--notes-file', str(file))
        raw = gh('api', endpoint)
    release = json.loads(raw)
    existing = {a['name']: a for a in release.get('assets', [])}
    for path, item in assets:
        found = existing.get(path.name)
        if found:
            if found.get('size') != item['bytes'] or found.get('digest') != 'sha256:' + item['sha256']:
                raise ValueError('Existing asset differs; use a new version tag, not overwrite: ' + path.name)
            continue
        if not release.get('draft'):
            raise ValueError('Published release is incomplete; create a new version instead of modifying it.')
        gh('release', 'upload', args.tag, str(path), '--repo', REPO)
        print(json.dumps({'uploaded': path.name, 'bytes': item['bytes']}), flush=True)
    release = json.loads(gh('api', endpoint))
    verify_remote(release, assets, args.tag)
    if release.get('draft'):
        gh('release', 'edit', args.tag, '--repo', REPO, '--draft=false', '--latest=false')
        release = json.loads(gh('api', endpoint))
    remote = verify_remote(release, assets, args.tag)
    if release.get('draft') or not release.get('published_at'):
        raise ValueError('Release is not publicly published.')
    videos = {item['id']: {'url': remote[path.name]['browser_download_url'],
                           'bytes': item['bytes'], 'sha256': item['sha256']} for path, item in assets}
    policy = {'status': 'verified', 'verification': 'GitHub asset SHA-256 digest and size',
              'tag': args.tag, 'releaseUrl': release['html_url'], 'videos': videos}
    atomic_text(BASE / 'hosting.json', json.dumps(policy, ensure_ascii=False, indent=2) + '\n')
    js = {'version': '33.0.3', 'videos': {key: value['url'] for key, value in videos.items()}}
    atomic_text(ROOT / 'public/academy/packaging-media-v33.js',
                '/* Verified GitHub Release media; local copies remain in the offline package. */\n'
                'window.MACGYVER_PACKAGING_MEDIA=' + json.dumps(js, ensure_ascii=False, separators=(',', ':')) + ';\n')
    print(json.dumps({'status': 'PASS', 'release': release['html_url'], 'films': 6}))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, KeyError) as error:
        raise SystemExit(str(error))
