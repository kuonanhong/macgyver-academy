#!/usr/bin/env python3
"""V21/V22 public preview snapshot, with a transport that preserves unrelated files.

The complete owner/source edition is distributed in the downloadable ZIP.
GitHub receives only first-stage lesson bodies and public browser code/assets.
"""
from pathlib import Path
import argparse
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]


def module_at(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def ensure_built(source):
    # End-user ZIPs contain the verified prebuilt assets, so Node is only needed
    # after editing source or curriculum, not for normal uploads.
    if (source / 'public/academy/preview-manifest.json').is_file():
        return
    checked = subprocess.run([sys.executable, str(source / 'tools/check-offline.py')], capture_output=True, text=True)
    if checked.returncode == 0:
        return
    node = shutil.which('node')
    if not node:
        raise ValueError('本地教材或程式有更新，需要 Node.js 18+ 重建離線網站後才能上傳；未上傳過時 bundle。')
    subprocess.run([node, str(source / 'tools/build-offline.mjs')], check=True)
    subprocess.run([sys.executable, str(source / 'tools/check-offline.py')], check=True)


def public_snapshot(source, excluded=()):
    exporter = module_at('macgyver_v21_preview_export', source / 'tools/export-preview-v21.py')
    private_paths = [Path(path).expanduser().resolve() for path in excluded]
    if not os.environ.get('MACGYVER_UPLOAD_V21_TEST') == '1':
        ensure_built(source)
    files = {}
    with tempfile.TemporaryDirectory(prefix='macgyver-v21-public-') as directory:
        output = Path(directory) / 'preview'
        exported = exporter.export(source / 'public/academy', output)
        for path in output.rglob('*'):
            if not path.is_file() or path.name == exporter.MARKER:
                continue
            relative = path.relative_to(output)
            original = (source / 'public/academy' / relative).resolve()
            if any(original == base or base in original.parents for base in private_paths):
                raise ValueError('選定私人資料夾與必要公開網站路徑重疊，請移到專案外：' + relative.as_posix())
            data = path.read_bytes()
            files['public/academy/' + relative.as_posix()] = data
    # Deployment is deliberately independent of the full course compiler.
    required = ['index.html', 'deploy-static.sh', '.github/workflows/pages.yml', 'Update_MacGyver_v29.sh',
                '.github/workflows/weekly-markets.yml', 'tools/markets-v12/update_markets.py',
                'tools/check-pages-artifact-v28.py', 'tools/wait-pages-artifact-v34.py', 'tools/test-wait-pages-artifact-v34.py',
                'tools/deployment-marker-v32.py', 'tools/count-learning-tracks-v32.mjs', 'tools/verify-live-v32.py', 'tools/pages-doctor-v28.py', 'tools/read-json-array.mjs',
                'tools/export-preview-v21.py', 'macgyver.sh', 'Upload_MacGyver_v21_SSH.sh',
                'tools/upload-v21/site_sync.py', 'tools/upload-v21/upload.py',
                'tools/upload-v21/public_transport.py', 'tools/export_github.py',
                'tools/sync-v13/models_sync.py', 'tools/model-manifest.json']
    # Publish reviewed updater code with the browser preview so a future clone
    # cannot fall back to an old whole-source exporter. No authoring trees enter
    # this list; full owner curricula remain in the downloadable edition.
    if (source / 'Install_and_Upload_MacGyver_v22.sh').is_file():
        required.append('Install_and_Upload_MacGyver_v22.sh')
    if (source / 'Install_and_Upload_MacGyver_v23.sh').is_file():
        required.append('Install_and_Upload_MacGyver_v23.sh')
    if (source / 'Install_and_Upload_MacGyver_v24.sh').is_file():
        required.append('Install_and_Upload_MacGyver_v24.sh')
    if (source / 'Install_and_Upload_MacGyver_v25.sh').is_file():
        required.append('Install_and_Upload_MacGyver_v25.sh')
    if (source / 'Install_and_Upload_MacGyver_v26.sh').is_file():
        required.append('Install_and_Upload_MacGyver_v26.sh')
    if (source / 'Install_and_Upload_MacGyver_v27.sh').is_file():
        required.append('Install_and_Upload_MacGyver_v27.sh')
    for optional in ('Install_and_Upload_MacGyver_v28.sh', 'Update_MacGyver_v30.sh', 'Update_MacGyver_v31.sh', 'Update_MacGyver_v32.sh'):
        if (source / optional).is_file():
            required.append(optional)
    # The independent public cinema can be reproduced without owner curricula.
    for optional in ('README_PACKAGING_TOUR_V33.html', 'Start_Packaging_Tour_v33.sh',
                     'Upload_Packaging_YouTube_v33.sh', 'docs/PACKAGING_YOUTUBE_METADATA_V33.json',
                     'tools/test-publish-packaging-youtube-v33.py',
                     'tools/preview-packaging-tour-v33.py', 'tools/export-packaging-subtitles-v33.mjs',
                     'tools/finalize-packaging-videos-v33.py', 'tools/package-packaging-tour-v33.py',
                     'tools/add-line-qr-packaging-v33.py', 'tools/publish-packaging-youtube-v33.py',
                     'tools/test-packaging-tour-v33.mjs', 'docs/PACKAGING_TOUR_SOURCES_V33.md',
                     'docs/VALIDATION_PACKAGING_TOUR_V33.json'):
        if (source / optional).is_file():
            required.append(optional)
    for optional in (
            'Upload_Narrated_V34.sh', 'Publish_Packaging_Website_v34.sh',
            'Upload_Process_V34.sh', 'tools/publish-process-youtube-v34.py',
            'tools/test-publish-process-youtube-v34.py', 'docs/PROCESS_YOUTUBE_PUBLISH_V34.html',
            'tools/build-process-long-v34.py', 'tools/test-process-long-v34.py',
            'tools/test-publish-packaging-release-v34.py',
            'requirements-packaging-media-v34.txt', 'docs/PACKAGING_MEDIA_ENVIRONMENT_V34.json',
            'tools/publish-packaging-release-v34.py', 'tools/test-packaging-hosting-v33.py',
            'tools/build-native-narration-v34.py', 'tools/collect-packaging-narration-v34.py',
            'tools/test-native-narration-duration-v34.py',
            'tools/build-all-packaging-narration-v34.py', 'tools/mux-narrated-packaging-v34.py',
            'tools/prepare-narrated-youtube-job-v34.py', 'tools/build-c01-narrated-job-v34.py',
            'tools/test-narrated-packaging-v34.py', 'tools/export-bilingual-packaging-subtitles-v33.py',
            'tools/build-speech-aligned-subtitles-v34.py',
            'docs/PACKAGING_YOUTUBE_METADATA_V34.json', 'docs/PACKAGING_PROCESS_C01_YOUTUBE_METADATA_V34.json',
            'tools/test-bilingual-packaging-subtitles-v33.py',
            'tools/preview-packaging-process-v34.py', 'tools/test-packaging-process-v34.mjs',
            'tools/test-packaging-process-scene-v34.mjs',
            'tools/test-packaging-process-player-v34.mjs', 'tools/build-c01-semantic-mapping-v34.mjs',
            'docs/PACKAGING_PROCESS_ROADMAP_V34.json',
            'docs/packaging-process-scripts-v34/C01.json'):
        if (source / optional).is_file():
            required.append(optional)
    for name in required:
        path = source / name
        if path.is_symlink() or not path.is_file():
            raise ValueError('缺少公開部署檔案：' + name)
        original = path.resolve()
        if any(original == base or base in original.parents for base in private_paths):
            raise ValueError('選定私人資料夾與必要公開工具重疊，請移到專案外：' + name)
        files[name] = path.read_bytes()
    # Keep the public repository's version marker synchronized with its actual
    # source snapshot instead of leaving an older V17/V19 marker behind.
    source_major = str(exported['version'])
    version_file = source / 'SOURCE_VERSION.json'
    if version_file.exists():
        if version_file.is_symlink() or not version_file.is_file():
            raise ValueError('Unsafe SOURCE_VERSION.json')
        version = json.loads(version_file.read_text('utf-8'))
        source_major = str(version.get('version', '')).split('.')[0]
        if source_major not in {'21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32'}:
            raise ValueError('SOURCE_VERSION.json must identify V21, V22, V23, V24, V25, V26, V27, V28, V29, V30, V31 or V32 before uploading.')
        if source_major != str(exported['version']):
            raise ValueError('SOURCE_VERSION.json and the built public curriculum version disagree; rebuild the same release before uploading.')
        files['SOURCE_VERSION.json'] = (json.dumps(version, ensure_ascii=False, indent=2) + '\n').encode()
    files['.nojekyll'] = b''
    files['README.md'] = (
        f'# MacGyver Engineering Academy V{source_major}\n\n'
        'This branch serves the public first-stage preview. The downloadable owner/source '
        'ZIP contains the complete bilingual curricula and local backend.\n\n'
        'Run the **Publish static MacGyver Academy** GitHub Actions workflow to deploy Pages. '
        'Full member lessons require a separately configured authenticated content backend; '
        'GitHub Pages has no server-side account verification.\n\n'
        f'V{source_major} uploads replace public files and remove recognized legacy generated member '
        'payloads/authoring inputs. They preserve unrelated repository files and do not '
        'erase earlier Git history.\n'
    ).encode()
    # Check public bytes too; never echo possible secrets into the terminal.
    policy = module_at('macgyver_v21_public_policy', source / 'tools/export_github.py')
    for name, data in files.items():
        if len(data) >= policy.SIZE_LIMIT:
            raise ValueError('公開檔案達到 GitHub 單檔大小上限：' + name)
        if policy.SECRETS.search(data):
            raise ValueError('疑似憑證內容，已停止公開上傳：' + name)
    return files, []


def load_sync(excluded=()):
    sync = module_at('macgyver_v21_public_transport', ROOT / 'tools/upload-v21/public_transport.py')
    sync.verified_snapshot = lambda source: public_snapshot(source, excluded)
    return sync


def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--exclude-private', action='append', default=[])
    args, rest = parser.parse_known_args()
    if '--prune' in rest or '--protect-content' in rest or '--site-only' in rest:
        raise ValueError('V21 已使用經驗證的首節公開快照，不接受舊版 prune/protect-content/site-only 模式。')
    sync = load_sync(args.exclude_private)
    sys.argv = [sys.argv[0], *rest]
    return sync.main(snapshot_provider=sync.verified_snapshot)


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        print('停止：' + str(error), file=sys.stderr)
        sys.exit(1)
