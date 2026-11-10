#!/usr/bin/env bash
# V29 verified update: website and Pages; --with-assets includes existing private assets.
# Self-contained; supports macOS Bash 3.2, Linux, Windows Git Bash / WSL.
# Uses existing Python 3.10+; does not install software or download model weights.
# V29: Windows Python launcher fallback; staged conflict reports block accidental mixed-version uploads.
set -euo pipefail
TASK_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
TASK_PYTHON=()
for TASK_CANDIDATE in "${MACGYVER_PYTHON:-}" "${CONDA_PREFIX:+${CONDA_PREFIX}/bin/python}" python3 python; do
  [[ -n "$TASK_CANDIDATE" ]] || continue
  if command -v "$TASK_CANDIDATE" >/dev/null 2>&1 && "$TASK_CANDIDATE" -c 'import sys;sys.exit(sys.version_info<(3,10))' 2>/dev/null; then
    TASK_PYTHON=("$TASK_CANDIDATE")
    break
  fi
done
if [[ ${#TASK_PYTHON[@]} -eq 0 ]] && command -v py >/dev/null 2>&1 && py -3 -c 'import sys;sys.exit(sys.version_info<(3,10))' 2>/dev/null; then
  TASK_PYTHON=(py -3)
fi
if [[ ${#TASK_PYTHON[@]} -eq 0 ]]; then
  printf '%s\n' '需要 Python 3.10+；可用 MACGYVER_PYTHON 指定既有 Python。Windows 亦支援 py -3。' >&2
  exit 1
fi
export PYTHONUTF8=1
MACGYVER_PYTHON="$("${TASK_PYTHON[@]}" -c 'import sys; print(sys.executable)')"
export MACGYVER_PYTHON
exec "${TASK_PYTHON[@]}" - "$TASK_DIR" "$@" <<'PY'
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

VERSION = '29.0.0'
ROOT_NAME = 'MacGyver_Engineering_Academy_v29'
FULL_NAME = ROOT_NAME + '.zip'
PART_NAMES = ['MacGyver_v29_Alternative_%d_of_4.zip' % i for i in range(1, 5)]
MANIFEST_NAME = 'RELEASE_FILES_V29.json'
EMBEDDED_ARCHIVES_JSON = ''  # @MACGYVER_V29_ARCHIVE_MANIFEST@


def digest(path):
    checksum = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(4 * 1024 * 1024), b''):
            checksum.update(block)
    return checksum.hexdigest()


def safe_path(value):
    if (not isinstance(value, str) or not value or value.startswith('/')
            or '\\' in value or ':' in value or '\x00' in value
            or any(p in ('', '.', '..') for p in value.rstrip('/').split('/'))):
        raise ValueError('不安全的套件路徑，停止。')
    return PurePosixPath(value)


def safe_target(root, relative):
    target = root.joinpath(*safe_path(relative).parts)
    if root.is_symlink() or any(root.joinpath(*target.relative_to(root).parts[:i]).is_symlink()
                               for i in range(1, len(target.relative_to(root).parts) + 1)):
        raise ValueError('目的位置包含符號連結，停止：' + relative)
    if not target.resolve().is_relative_to(root.resolve()):
        raise ValueError('目的位置不在專案中，停止。')
    return target


def entries(path):
    document = json.loads(path.read_text('utf-8'))
    if document.get('version') != VERSION or not isinstance(document.get('files'), list):
        raise ValueError('V29 逐檔清單版本或格式不符。')
    result, names = {}, set()
    for item in document['files']:
        relative = safe_path(item.get('path')).as_posix()
        if (relative.casefold() in names or not re.fullmatch(r'[0-9a-f]{64}', item.get('sha256', ''))
                or type(item.get('bytes')) is not int or item['bytes'] < 0):
            raise ValueError('V29 逐檔清單含重複或無效欄位。')
        names.add(relative.casefold())
        result[relative] = item
    if not result:
        raise ValueError('V29 逐檔清單為空。')
    return result


def require_project(project, label='專案'):
    if project.is_symlink() or not project.is_dir():
        raise ValueError(label + '必須是實際資料夾：' + str(project))
    for name in ('macgyver.sh', 'public/academy/experience.html'):
        if not safe_target(project, name).is_file():
            raise ValueError(label + '不完整，缺少：' + name + '；位置：' + str(project))


def archive_expectations(folder, selected_manifest):
    if selected_manifest:
        path = selected_manifest.expanduser().resolve()
        document = json.loads(path.read_text('utf-8'))
    elif EMBEDDED_ARCHIVES_JSON:
        document = json.loads(EMBEDDED_ARCHIVES_JSON)
    else:
        path = folder / 'RELEASE_ARCHIVES_V29.json'
        if path.is_symlink() or not path.is_file():
            raise ValueError('請使用同次發行的 .sh，或補齊 RELEASE_ARCHIVES_V29.json；不跳過 SHA-256 校驗。')
        document = json.loads(path.read_text('utf-8'))
    if document.get('schema') != 1 or document.get('version') != VERSION or document.get('root') != ROOT_NAME:
        raise ValueError('V29 發行清單版本不符。')
    expected = {}
    for item in document.get('archives', []):
        name = item.get('filename')
        if (name not in [FULL_NAME, *PART_NAMES] or name in expected
                or not re.fullmatch(r'[0-9a-f]{64}', item.get('sha256', ''))
                or type(item.get('bytes')) is not int or item['bytes'] <= 0):
            raise ValueError('V29 壓縮檔清單無效。')
        expected[name] = item
    sums = folder / 'SHA256SUMS_V29.txt'
    if sums.exists():
        if sums.is_symlink():
            raise ValueError('校驗清單不可是符號連結。')
        for line in sums.read_text('utf-8').splitlines():
            fields = line.split(None, 1)
            if len(fields) == 2 and fields[1].lstrip('*') in expected:
                if fields[0] != expected[fields[1].lstrip('*')]['sha256']:
                    raise ValueError('兩份發行校驗清單不一致。')
    return document, expected


def install(folder, selected_manifest=None):
    project = folder / ROOT_NAME
    full = folder / FULL_NAME
    parts = [folder / name for name in PART_NAMES]
    if full.is_file() and not full.is_symlink():
        archives = [full]
    elif all(p.is_file() and not p.is_symlink() for p in parts):
        archives = parts
    elif project.is_dir() and not project.is_symlink():
        require_project(project)
        print('使用已解壓的專案，保留所有本機修改。', flush=True)
        return project
    else:
        raise ValueError('請把完整 ZIP 或全部四個 Alternative ZIP 與 .sh 放在同一資料夾；保留檔名。')
    document, expected = archive_expectations(folder, selected_manifest)
    for archive in archives:
        item = expected.get(archive.name)
        print('SHA-256 校驗：' + archive.name, flush=True)
        if not item or archive.stat().st_size != item['bytes'] or digest(archive) != item['sha256']:
            raise ValueError('壓縮檔校驗失敗，尚未解壓或上傳：' + archive.name)
    total, names = 0, set()
    for archive in archives:
        with zipfile.ZipFile(archive) as zipped:
            for info in zipped.infolist():
                relative = safe_path(info.filename)
                mode = info.external_attr >> 16
                if relative.parts[0] != ROOT_NAME or (len(relative.parts) < 2 and not info.is_dir()):
                    raise ValueError('壓縮檔根目錄不符。')
                if info.flag_bits & 1 or stat.S_ISLNK(mode) or (stat.S_IFMT(mode) and not (stat.S_ISREG(mode) or stat.S_ISDIR(mode))):
                    raise ValueError('壓縮檔含加密、符號連結或特殊檔案。')
                if not info.is_dir():
                    if info.filename.casefold() in names:
                        raise ValueError('壓縮檔重複路徑或大小寫衝突。')
                    names.add(info.filename.casefold())
                    total += info.file_size
                    if total > 12 * 1024 ** 3 or len(names) > 200000:
                        raise ValueError('壓縮檔超過套件容量上限。')
    if shutil.disk_usage(folder).free < total + 256 * 1024 ** 2:
        raise ValueError('磁碟空間不足；請另保留至少 256 MiB。')
    with tempfile.TemporaryDirectory(prefix='.macgyver-v29-unpack-', dir=folder) as temporary:
        staging = Path(temporary)
        for archive in archives:
            print('解壓並驗證 CRC：' + archive.name, flush=True)
            with zipfile.ZipFile(archive) as zipped:
                for info in zipped.infolist():
                    target = staging.joinpath(*PurePosixPath(info.filename).parts)
                    if info.is_dir():
                        target.mkdir(parents=True, exist_ok=True)
                        continue
                    target.parent.mkdir(parents=True, exist_ok=True)
                    with zipped.open(info) as source, target.open('xb') as dest:
                        shutil.copyfileobj(source, dest, 1024 * 1024)
                    if target.suffix in ('.sh', '.command'):
                        target.chmod(0o755)
        incoming = staging / ROOT_NAME
        require_project(incoming, '解壓後的套件')
        manifest = incoming / MANIFEST_NAME
        if (not re.fullmatch(r'[0-9a-f]{64}', document.get('releaseFilesSha256', ''))
                or digest(manifest) != document['releaseFilesSha256']):
            raise ValueError('套件逐檔清單 SHA-256 不符。')
        new_entries = entries(manifest)
        for name, item in new_entries.items():
            target = safe_target(incoming, name)
            if not target.is_file() or target.stat().st_size != item['bytes'] or digest(target) != item['sha256']:
                raise ValueError('解壓後逐檔校驗失敗：' + name)
        actual = {p.relative_to(incoming).as_posix() for p in incoming.rglob('*') if p.is_file()}
        if actual != set(new_entries) | {MANIFEST_NAME}:
            raise ValueError('套件含清單之外的檔案。')
        if not project.exists() and not project.is_symlink():
            incoming.rename(project)
        else:
            # An interrupted/manual extraction can leave a valid directory without
            # its launchers. The verified incoming package must be allowed to fill
            # these missing files before completeness is checked.
            if project.is_symlink() or not project.is_dir():
                raise ValueError('安裝目的位置必須是實際資料夾：' + str(project))
            old_manifest = safe_target(project, MANIFEST_NAME)
            if old_manifest.exists() and not old_manifest.is_file():
                raise ValueError('目的清單位置已被資料夾佔用：' + str(old_manifest))
            old_entries = entries(old_manifest) if old_manifest.is_file() else {}
            conflicts, missing = 0, 0
            operations, conflict_paths = [], []
            # Check every destination before changing any installed file.
            for name in sorted(new_entries):
                target = safe_target(project, name)
                source = incoming / name
                current = digest(target) if target.is_file() else None
                previous = old_entries.get(name, {}).get('sha256')
                if target.exists() and not target.is_file():
                    raise ValueError('目的檔案位置已被資料夾佔用：' + name)
                if current == new_entries[name]['sha256']:
                    continue
                if current is not None and current != previous:
                    target = safe_target(project, '.macgyver-updates-v29/' + name)
                    conflict_paths.append(name)
                    conflicts += 1
                elif current is None:
                    missing += 1
                if target.exists() and not target.is_file():
                    raise ValueError('目的檔案位置已被資料夾佔用：' + str(target))
                for parent in target.parents:
                    if parent == project:
                        break
                    if parent.exists() and not parent.is_dir():
                        raise ValueError('目的資料夾位置已被檔案佔用：' + str(parent))
                operations.append((source, target))
            print('既有專案：補齊 %d 個缺檔；保留本機修改。' % missing, flush=True)
            for source, target in operations:
                target.parent.mkdir(parents=True, exist_ok=True)
                with tempfile.NamedTemporaryFile(dir=target.parent, delete=False) as temp:
                    pending = Path(temp.name)
                    with source.open('rb') as stream:
                        shutil.copyfileobj(stream, temp)
                if target.suffix in ('.sh', '.command'):
                    pending.chmod(0o755)
                os.replace(pending, target)
            shutil.copyfile(manifest, old_manifest)
            conflict_report = safe_target(project, '.macgyver-updates-v29/CONFLICTS.json')
            if conflicts:
                conflict_report.parent.mkdir(parents=True, exist_ok=True)
                conflict_report.write_text(json.dumps({'version': VERSION, 'status': 'review-required',
                    'files': conflict_paths}, ensure_ascii=False, indent=2) + '\n', 'utf-8')
            elif conflict_report.is_file():
                conflict_report.unlink()
            print('保留本機修改與新增檔案；%d 個新版衝突檔位於 .macgyver-updates-v29。' % conflicts, flush=True)
        require_project(project, '安裝後的專案')
        print('完成 %d 個發行檔案的校驗與安裝。' % len(new_entries), flush=True)
    return project


def main():
    parser = argparse.ArgumentParser(prog='Update_MacGyver_v29.sh', description='V29 一鍵更新：預設更新公開網站並觸發 Pages；--with-assets 才上傳現有私人文件／模型。Python 3.10+、Git SSH、已登入的 gh。--extract-only 只安裝；--dry-run 只連線比較。')
    parser.add_argument('--project', type=Path, help='指定已存在的 V29 原始碼資料夾，避免更新錯誤專案')
    parser.add_argument('--accept-local-changes', action='store_true', help='已自行檢閱並整合衝突後，保留本機檔並繼續；不會覆寫或刪除本機檔')
    parser.add_argument('--website-only', action='store_true', help='不傳私人文件／模型；仍更新公開網站')
    parser.add_argument('--no-publish-pages', action='store_true', help='只上傳，不觸發 Pages；不需要 gh')
    parser.add_argument('--extract-only', action='store_true', help='只安裝；不連線或上傳')
    parser.add_argument('--dry-run', action='store_true', help='安裝並連線比較；不提交、不推送')
    parser.add_argument('--with-assets', action='store_true', help='將現有模型與私人文件另送私人 PRIVATE-MODELS')
    parser.add_argument('--manifest', type=Path, help='同次 RELEASE_ARCHIVES_V29.json')
    parser.add_argument('--models-dir', type=Path)
    parser.add_argument('--documents-dir', type=Path)
    parser.add_argument('--state', type=Path, help='專案以外的比較快取位置')
    parser.add_argument('--batch-mib', type=int, choices=range(40, 1025), metavar='40..1024')
    parser.add_argument('--cloud-worker', metavar='HTTPS_ORIGIN', help='連接 Worker、更新公開知識庫，再上傳網站')
    parser.add_argument('--knowledge-dir', type=Path, help='核准公開知識文件資料夾；需要 --cloud-worker')
    parser.add_argument('--cloud-only', action='store_true', help='只同步 Cloudflare 知識庫；需要 --cloud-worker')
    parser.add_argument('--cloud-translation', choices=('on', 'off'), help='設定公開頁翻譯；需同步啟用 Worker 的翻譯端點')
    parser.add_argument('--publish-pages', action='store_true', help='上傳完成後以已登入的 gh 觸發 GitHub Pages 部署')
    args = parser.parse_args(sys.argv[2:])
    if args.website_only and (args.with_assets or args.models_dir or args.documents_dir):
        parser.error('--website-only 不可同時要求私人資產。')
    if args.no_publish_pages and args.publish_pages:
        parser.error('--no-publish-pages 不可搭配 --publish-pages。')
    if not (args.extract_only or args.cloud_only):
        args.publish_pages = args.publish_pages or (not args.dry_run and not args.no_publish_pages)
    if (args.models_dir or args.documents_dir) and not args.with_assets:
        parser.error('--models-dir / --documents-dir 需要 --with-assets。')
    if (args.knowledge_dir or args.cloud_only or args.cloud_translation) and not args.cloud_worker:
        parser.error('Cloudflare 選項需要 --cloud-worker。')
    if args.extract_only and (args.with_assets or args.dry_run or args.cloud_worker or args.publish_pages):
        parser.error('--extract-only 只能安裝套件。')
    if args.dry_run and (args.cloud_worker or args.publish_pages):
        parser.error('--dry-run 不變更雲端資料或發布網站。')
    if args.cloud_only and (args.with_assets or args.publish_pages or args.cloud_translation):
        parser.error('--cloud-only 只同步公開知識庫。')
    if args.publish_pages:
        if not shutil.which('gh') or subprocess.run(['gh', 'auth', 'status', '--hostname', 'github.com'],
                                                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode:
            parser.error('--publish-pages 需要先執行 gh auth login。')
    folder = args.project.expanduser().resolve() if args.project else Path(sys.argv[1]).resolve()
    marker = folder / 'SOURCE_VERSION.json'
    if args.project:
        if args.project.expanduser().is_symlink() or not marker.is_file() or marker.is_symlink():
            parser.error('--project 必須指向含 SOURCE_VERSION.json 的既有 V29 實際資料夾。')
        if json.loads(marker.read_text('utf-8')).get('version') != VERSION:
            parser.error('--project 版本不是 V29；請先安裝 V29，再整合舊版自訂修改。')
        require_project(folder)

    current_version = (json.loads(marker.read_text('utf-8')).get('version')
                       if marker.is_file() and not marker.is_symlink() else None)
    if ((folder / 'macgyver.sh').is_file() and (folder / 'public/academy/experience.html').is_file()
            and (current_version == VERSION or (current_version is None and folder.name == ROOT_NAME))):
        require_project(folder)
        project = folder
        print('使用目前原始碼專案，保留本機修改。', flush=True)
    else:
        project = install(folder, args.manifest)
    print('專案位置：' + str(project), flush=True)
    conflict_report = safe_target(project, '.macgyver-updates-v29/CONFLICTS.json')
    if conflict_report.is_file():
        pending = json.loads(conflict_report.read_text('utf-8'))
        if pending.get('status') == 'review-required':
            if args.accept_local_changes:
                pending['status'] = 'local-changes-reviewed'
                conflict_report.write_text(json.dumps(pending, ensure_ascii=False, indent=2) + '\n', 'utf-8')
                print('保留已檢閱的本機修改；新版對照檔仍留在 .macgyver-updates-v29。', flush=True)
            elif not args.extract_only:
                raise ValueError('有 %d 個本機修改與新版衝突；未上傳混合版本。請檢閱 .macgyver-updates-v29/CONFLICTS.json 並整合；完成後加 --accept-local-changes。' % len(pending.get('files', [])))
    if args.extract_only:
        print('安裝完成；尚未連線或上傳。啟動：bash "' + str(project / 'run-local.sh') + '"', flush=True)
        return 0
    if args.cloud_worker:
        cloud_script = project / 'Configure_MacGyver_Cloud_v23.sh'
        if not cloud_script.is_file():
            raise ValueError('Cloudflare 上傳需使用含 Worker 原始碼的 V29 完整套件。')
        cloud = ['bash', str(cloud_script)]
        # Validate and normalize the publicly visible origin before contacting
        # the Worker. The sync tool owns credentials and public-source policy.
        sys.path.insert(0, str(project / 'tools'))
        from importlib import import_module
        configure = import_module('configure-cloud-v23')
        try:
            endpoint = configure.origin(args.cloud_worker)
            if not endpoint:
                raise argparse.ArgumentTypeError('必須填寫可用的 Worker HTTPS 網址。')
        except argparse.ArgumentTypeError as error:
            parser.error(str(error))
        sync = [*cloud, 'sync', '--endpoint', endpoint]
        if args.knowledge_dir:
            sync.extend(['--docs', str(args.knowledge_dir.expanduser().resolve())])
        if status := subprocess.run(sync, cwd=project).returncode:
            return status
        if args.cloud_only:
            return 0
        connect = [*cloud, 'connect', endpoint]
        if args.cloud_translation:
            connect.extend(['--translation', args.cloud_translation])
        if status := subprocess.run(connect, cwd=project).returncode:
            return status
    # Use local assets in this project first. Upgrades from V27 or V28 can reuse
    # adjacent asset folders without copying gigabytes or replacing their data.
    if args.with_assets:
        for argument, dirname in (('models_dir', 'models'), ('documents_dir', 'local-documents')):
            if getattr(args, argument):
                continue
            def has_content(path):
                return path.is_dir() and not path.is_symlink() and any(
                    entry.name.lower() not in ('readme.md', '.ds_store') for entry in path.iterdir())
            if has_content(project / dirname):
                continue
            candidates = []
            for base in (folder, project.parent, project.parent / 'MacGyver_Engineering_Academy_v28', project.parent / 'MacGyver_Engineering_Academy_v27'):
                candidate = base / dirname
                if candidate != project / dirname and has_content(candidate):
                    resolved = candidate.resolve()
                    if resolved not in candidates:
                        candidates.append(resolved)
            if len(candidates) > 1:
                raise ValueError('找到多個 ' + dirname + ' 來源；請用 --' + argument.replace('_', '-') + ' 指定要上傳的資料夾。')
            if candidates:
                setattr(args, argument, candidates[0])
                print('沿用本機資產來源：' + str(candidates[0]), flush=True)
    doctor = [sys.executable, str(project / 'tools/pages-doctor-v28.py')]
    if args.publish_pages:
        if status := subprocess.run([*doctor, '--configure-actions'], cwd=project).returncode:
            return status
    command = ['bash', str(project / 'macgyver.sh'), 'all']
    for flag in ('dry_run', 'with_assets'):
        if getattr(args, flag):
            command.append('--' + flag.replace('_', '-'))
    for name in ('models_dir', 'documents_dir', 'state'):
        value = getattr(args, name)
        if value:
            command.extend(['--' + name.replace('_', '-'), str(value.expanduser().resolve())])
    if args.batch_mib:
        command.extend(['--batch-mib', str(args.batch_mib)])
    print('公開網站：macgyver-academy；' + ('私人資產：PRIVATE-MODELS。' if args.with_assets else '此次不傳私人資產。') + '只傳差異，可重跑續傳，不下載權重、不強推。', flush=True)
    status = subprocess.run(command, cwd=project).returncode
    if status or not args.publish_pages:
        return status
    # Dispatch is not a deployment success. Wait for our unique workflow run
    # and return failure if publishing fails or cannot be verified.
    status = subprocess.run([*doctor, '--publish'], cwd=project).returncode
    return status


try:
    sys.exit(main())
except KeyboardInterrupt:
    print('已中止；可重新執行續傳。', file=sys.stderr)
    sys.exit(130)
except (OSError, ValueError, KeyError, TypeError, zipfile.BadZipFile) as error:
    print('停止：' + str(error), file=sys.stderr)
    sys.exit(1)
PY
