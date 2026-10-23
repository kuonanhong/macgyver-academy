#!/usr/bin/env bash
# macOS Bash 3.2 / Linux / Windows Git Bash or WSL. Dependencies are not installed.
set -euo pipefail
if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
  cat <<'HELP'
用法：bash Install_and_Upload_MacGyver_v17.sh [選項]
將本檔與 V17 完整 ZIP，或 Alternative 第 1～4 包，放在同一資料夾。
不加選項：SHA-256 校驗、解壓、SSH 增量上傳公開網站至：
  git@github.com:kuonanhong/macgyver-academy.git（main）
  --extract-only       只校驗／解壓；不連線 GitHub。
  --dry-run            解壓並連線比較；不提交、不上傳。
  --with-assets        同時把現有模型與私人文件上傳至私人 PRIVATE-MODELS。
  --models-dir PATH    現有權重資料夾；配合 --with-assets。
  --documents-dir PATH 現有私人文件資料夾；配合 --with-assets。
  --manifest PATH      指定此次發行的 RELEASE_ARCHIVES_V17.json。
  --state PATH         指定專案外的增量比較快取資料夾。
已完整解壓的 V17 直接使用，保留本地修改；不刪遠端、不強推。
下載版 .sh 內含同次發行的 ZIP 校驗值；原始模板需同目錄的發行清單。
需要 Python 3.10+；上傳另需 Git、SSH 和 GitHub SSH key 的首次設定。
不自動下載模型，不把私人文件或權重放入公開網站。
HELP
  exit 0
fi
TASK_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
TASK_PYTHON=''
for TASK_CANDIDATE in "${MACGYVER_PYTHON:-}" "${CONDA_PREFIX:+${CONDA_PREFIX}/bin/python}" python3 python; do
  [[ -n "$TASK_CANDIDATE" ]] || continue
  if command -v "$TASK_CANDIDATE" >/dev/null 2>&1 && "$TASK_CANDIDATE" -c 'import sys;sys.exit(sys.version_info<(3,10))' 2>/dev/null; then
    TASK_PYTHON="$TASK_CANDIDATE"
    break
  fi
done
if [[ -z "$TASK_PYTHON" ]]; then
  printf '%s\n' '需要 Python 3.10+。可先啟用現有 Conda 環境，或用 MACGYVER_PYTHON 指定 Python 完整路徑。' >&2
  exit 1
fi
export PYTHONUTF8=1
exec "$TASK_PYTHON" - "$TASK_DIR" "$@" <<'PY'
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import zipfile

ROOT_NAME = 'MacGyver_Engineering_Academy_v17'
VERSION = '17.0.0'
FULL_NAME = ROOT_NAME + '.zip'
PART_NAMES = ['MacGyver_v17_Alternative_%d_of_4.zip' % number for number in range(1, 5)]
ARCHIVE_NAMES = {FULL_NAME, *PART_NAMES}
EMBEDDED_ARCHIVES_JSON = ''  # @MACGYVER_V17_ARCHIVE_MANIFEST@


def note(message):
    print(message, flush=True)


def digest(path):
    result = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(4 * 1024 * 1024), b''):
            result.update(block)
    return result.hexdigest()


def safe_path(value):
    if not isinstance(value, str) or not value or value.startswith('/') or '\\' in value or ':' in value or '\x00' in value:
        raise ValueError('ZIP／清單含不安全路徑，停止。')
    path = PurePosixPath(value)
    if any(part in ('', '.', '..') for part in value.rstrip('/').split('/')):
        raise ValueError('ZIP／清單含不安全路徑，停止。')
    return path


def check_project(project, fresh=False):
    manifest = project / 'RELEASE_FILES_V17.json'
    if project.is_symlink() or manifest.is_symlink() or not manifest.is_file():
        raise ValueError('V17 資料夾不完整：缺少 RELEASE_FILES_V17.json。請先把現有資料夾移到別處保留，再重新解壓。')
    document = json.loads(manifest.read_text(encoding='utf-8'))
    if document.get('version') != VERSION or not isinstance(document.get('files'), list) or not document['files']:
        raise ValueError('V17 檔案清單格式不符。')
    missing, changed, seen = [], [], set()
    for item in document['files']:
        relative = safe_path(item['path'])
        key = relative.as_posix().casefold()
        if key in seen or not re.fullmatch(r'[0-9a-f]{64}', item.get('sha256', '')) or not isinstance(item.get('bytes'), int) or item['bytes'] < 0:
            raise ValueError('檔案清單有重複路徑或無效校驗欄位。')
        seen.add(key)
        target = project.joinpath(*relative.parts)
        if not target.resolve().is_relative_to(project.resolve()):
            raise ValueError('V17 路徑指向專案外，停止。')
        if any(project.joinpath(*relative.parts[:index]).is_symlink() for index in range(1, len(relative.parts) + 1)):
            raise ValueError('V17 內含符號連結，停止。')
        if not target.is_file():
            missing.append(relative.as_posix())
        elif target.stat().st_size != item['bytes'] or digest(target) != item['sha256']:
            changed.append(relative.as_posix())
    if missing:
        raise ValueError('V17 尚缺少 %d 個檔案（例如 %s）。請保留現有資料夾，再用完整包或全部四包重新解壓。' % (len(missing), missing[0]))
    required = ('tools/upload-v17/upload.py', 'tools/upload-v17/site_sync.py', 'tools/sync-v12/sync_github.py', 'tools/sync-v13/models_sync.py', 'Upload_MacGyver_v17_SSH.sh')
    for item in required:
        if not (project / item).is_file():
            raise ValueError('缺少 V17 上傳工具：' + item)
    if fresh and changed:
        raise ValueError('解壓後逐檔 SHA-256 校驗失敗：' + changed[0])
    if changed:
        note('保留您已修改的 %d 個發行檔案，後續只比較新增／修改內容。' % len(changed))
    return len(document['files'])


def archive_manifest(folder, selected_path):
    if selected_path:
        path = selected_path.expanduser()
        if path.is_symlink():
            raise ValueError('發行清單不能是符號連結。')
        document = json.loads(path.read_text(encoding='utf-8'))
    elif EMBEDDED_ARCHIVES_JSON:
        document = json.loads(EMBEDDED_ARCHIVES_JSON)
    else:
        path = folder / 'RELEASE_ARCHIVES_V17.json'
        if path.is_symlink() or not path.is_file():
            raise ValueError('此原始模板尚未內嵌發行校驗值。請使用同次下載提供的獨立 .sh，或把 RELEASE_ARCHIVES_V17.json 放在同目錄。')
        document = json.loads(path.read_text(encoding='utf-8'))
    if document.get('schema') != 1 or document.get('version') != VERSION or document.get('root') != ROOT_NAME or not isinstance(document.get('archives'), list):
        raise ValueError('V17 發行清單版本／格式不符。')
    result = {}
    for item in document['archives']:
        name = item.get('filename')
        if name not in ARCHIVE_NAMES or name in result or not re.fullmatch(r'[0-9a-f]{64}', item.get('sha256', '')) or not isinstance(item.get('bytes'), int) or item['bytes'] <= 0:
            raise ValueError('發行清單有無效的 ZIP 名稱、大小或 SHA-256。')
        result[name] = item
    return result


def select_archive(folder, name):
    for candidate in (name, name[:-4] + '_Download.zip'):
        path = folder / candidate
        if path.is_file() and not path.is_symlink():
            return path
    return None


def extract(folder, manifest_path):
    project = folder / ROOT_NAME
    if project.exists() or project.is_symlink():
        check_project(project)
        note('已找到完整 V17，使用現有內容並保留本地修改。')
        return project
    parts = [select_archive(folder, name) for name in PART_NAMES]
    full = select_archive(folder, FULL_NAME)
    if all(parts):
        selected = list(zip(PART_NAMES, parts))
    elif full:
        selected = [(FULL_NAME, full)]
    else:
        missing = ', '.join(str(index + 1) for index, path in enumerate(parts) if path is None)
        raise ValueError('找不到完整 ZIP；四分包尚缺第 ' + missing + ' 包。把完整 ZIP 或第 1～4 包與本 .sh 放在同目錄，保留下載檔名。')
    expected = archive_manifest(folder, manifest_path)
    for name, path in selected:
        if name not in expected:
            raise ValueError('同次發行清單缺少此 ZIP：' + name)
        note('校驗 SHA-256：' + path.name)
        record = expected[name]
        if path.stat().st_size != record['bytes'] or digest(path) != record['sha256']:
            raise ValueError('ZIP 大小／SHA-256 校驗失敗，請重新下載：' + path.name + '；未解壓、未上傳。')
    total, entries = 0, set()
    for _, path in selected:
        with zipfile.ZipFile(path) as archive:
            for info in archive.infolist():
                relative = safe_path(info.filename)
                if relative.parts[0] != ROOT_NAME or (len(relative.parts) < 2 and not info.is_dir()):
                    raise ValueError('ZIP 根目錄不符，停止。')
                mode = info.external_attr >> 16
                if info.flag_bits & 1 or stat.S_ISLNK(mode) or (stat.S_IFMT(mode) and not (stat.S_ISREG(mode) or stat.S_ISDIR(mode))):
                    raise ValueError('ZIP 含加密、符號連結或特殊檔案，停止。')
                if not info.is_dir():
                    key = info.filename.casefold()
                    if key in entries:
                        raise ValueError('ZIP 檔案重複或名稱大小寫衝突，停止。')
                    entries.add(key)
                    total += info.file_size
                    if total > 12 * 1024 ** 3 or len(entries) > 200000:
                        raise ValueError('ZIP 宣告內容超過 V17 公開套件上限，停止。')
    if shutil.disk_usage(folder).free < total + 256 * 1024 * 1024:
        raise ValueError('可用磁碟不足；此次解壓需約 %.2f GiB，請另保留至少 256 MiB。' % (total / 1024 ** 3))
    staging = Path(tempfile.mkdtemp(prefix='.macgyver-v17-unpack-', dir=folder))
    try:
        for _, path in selected:
            note('解壓：' + path.name)
            with zipfile.ZipFile(path) as archive:
                for info in archive.infolist():
                    target = staging.joinpath(*PurePosixPath(info.filename).parts)
                    if info.is_dir():
                        target.mkdir(parents=True, exist_ok=True)
                        continue
                    target.parent.mkdir(parents=True, exist_ok=True)
                    with archive.open(info) as source, target.open('xb') as output:
                        shutil.copyfileobj(source, output, 1024 * 1024)
                    if target.suffix == '.sh':
                        target.chmod(0o755)
        count = check_project(staging / ROOT_NAME, fresh=True)
        if project.exists() or project.is_symlink():
            raise ValueError('解壓期間目的資料夾已存在，停止以保留現有資料。')
        (staging / ROOT_NAME).rename(project)
        note('校驗與解壓完成：%d 個發行檔案。' % count)
    finally:
        shutil.rmtree(staging, ignore_errors=True)
    return project


def main():
    parser = argparse.ArgumentParser(description='V17 校驗、解壓與 SSH 增量上傳')
    parser.add_argument('--extract-only', action='store_true')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--with-assets', action='store_true')
    parser.add_argument('--manifest', type=Path)
    parser.add_argument('--models-dir', type=Path)
    parser.add_argument('--documents-dir', type=Path)
    parser.add_argument('--state', type=Path)
    args = parser.parse_args(sys.argv[2:])
    folder = Path(sys.argv[1]).resolve()
    if (args.models_dir or args.documents_dir) and not args.with_assets:
        parser.error('--models-dir／--documents-dir 需要搭配 --with-assets。')
    if (folder / 'RELEASE_FILES_V17.json').is_file():
        project = folder
        check_project(project)
        note('使用目前 V17 專案，保留本地修改。')
    else:
        project = extract(folder, args.manifest)
    note('專案位置：' + str(project))
    if args.extract_only:
        note('只解壓完成；未連線、未上傳。啟動網站：bash "' + str(project / 'run-local.sh') + '"')
        return 0
    command = [sys.executable, str(project / 'tools/upload-v17/upload.py'), '--branch', 'main']
    if args.dry_run:
        command.append('--dry-run')
    if not args.with_assets:
        command.extend(['--skip-models', '--skip-documents'])
    else:
        command.append('--with-assets')
    for name in ('models_dir', 'documents_dir', 'state'):
        value = getattr(args, name)
        if value:
            command.extend(['--' + name.replace('_', '-'), str(value.expanduser().resolve())])
    note('SSH 目標：git@github.com:kuonanhong/macgyver-academy.git（main）')
    note('只新增／修改；不刪遠端、不強推。需要先完成 GitHub SSH key 與首次主機指紋驗證。')
    if args.with_assets:
        note('現有模型與私人文件另送 PRIVATE-MODELS；不下載權重、不公開私人資產。')
    return subprocess.run(command, cwd=project).returncode


try:
    sys.exit(main())
except KeyboardInterrupt:
    print('\n已中止；重新執行本檔即可再試。', file=sys.stderr)
    sys.exit(130)
except (OSError, ValueError, KeyError, TypeError, zipfile.BadZipFile) as error:
    print('停止：' + str(error), file=sys.stderr)
    sys.exit(1)
PY
