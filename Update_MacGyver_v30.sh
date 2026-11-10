#!/usr/bin/env bash
# V30 one-click update and upload.
#   1. Verifies the V30 update ZIPs (SHA-256) and applies them on top of your V29 project.
#   2. Rebuilds featured.json, course parts and script wrappers with Python only, then
#      verifies every changed file against RELEASE_FILES_V30.json.
#   3. Uploads the public first-stage website over SSH and triggers GitHub Pages
#      (same uploader as V21-V29). --with-assets also sends your existing local
#      documents / model weights to the private PRIVATE-MODELS repository.
# Self-contained; macOS Bash 3.2, Linux, Windows Git Bash / WSL. Needs Python 3.10+.
# Installs nothing and downloads no model weights. Run: bash Update_MacGyver_v30.sh --help
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
  printf '%s\n' '需要 Python 3.10+；可用 MACGYVER_PYTHON 指定既有 Python。Windows 亦支援 py -3。 Python 3.10+ is required.' >&2
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

VERSION = '30.0.0'
BASE_VERSION = '29.0.0'
UPDATE_ROOT = 'MacGyver_Engineering_Academy_v30_update'
MANIFEST_NAME = 'RELEASE_FILES_V30.json'
BASE_MANIFEST_NAME = 'RELEASE_FILES_V29.json'
PLAN_NAME = 'UPDATE_PLAN_V30.json'
ARCHIVE = re.compile(r'MacGyver_v30_Update_(\d{1,2})_of_(\d{1,2})\.zip')
CONFLICT_DIR = '.macgyver-updates-v30'
EMBEDDED_ARCHIVES_JSON = ''  # @MACGYVER_V30_ARCHIVE_MANIFEST@
LAZY = 'public/academy/data/lazy/'
PARTS_DIR = 'public/academy/data/course-parts/'
FEATURED = 'public/academy/data/featured.json'
WRAPPED = re.compile(r'^public/academy/data/lazy/(courses|resources|owner-courses|owner-resources|data)/([a-z0-9]+(?:[-_][a-z0-9]+)*-[0-9a-f]{16})\.js$')
PART_BUDGET = 7 * 1024 * 1024


def say(message):
    print(message, flush=True)


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
        raise ValueError('不安全的套件路徑，停止。 Unsafe package path.')
    return PurePosixPath(value)


def safe_target(root, relative):
    target = root.joinpath(*safe_path(relative).parts)
    parts = target.relative_to(root).parts
    if root.is_symlink() or any(root.joinpath(*parts[:i]).is_symlink() for i in range(1, len(parts) + 1)):
        raise ValueError('目的位置包含符號連結，停止：' + relative)
    if not target.resolve().is_relative_to(root.resolve()):
        raise ValueError('目的位置不在專案中，停止。')
    return target


def entries(path, version):
    document = json.loads(path.read_text('utf-8'))
    if document.get('version') != version or not isinstance(document.get('files'), list):
        raise ValueError('逐檔清單版本或格式不符：' + path.name)
    result, names = {}, set()
    for item in document['files']:
        relative = safe_path(item.get('path')).as_posix()
        if (relative.casefold() in names or not re.fullmatch(r'[0-9a-f]{64}', item.get('sha256', ''))
                or type(item.get('bytes')) is not int or item['bytes'] < 0):
            raise ValueError('逐檔清單含重複或無效欄位：' + path.name)
        names.add(relative.casefold())
        result[relative] = item
    if not result:
        raise ValueError('逐檔清單為空：' + path.name)
    return result


def is_project(path):
    return (path.is_dir() and not path.is_symlink() and (path / 'macgyver.sh').is_file()
            and (path / 'public/academy/experience.html').is_file())


def project_version(project):
    marker = project / 'SOURCE_VERSION.json'
    if marker.is_symlink() or not marker.is_file():
        return None
    try:
        return json.loads(marker.read_text('utf-8')).get('version')
    except (OSError, ValueError):
        return None


def find_project(folder, selected):
    if selected:
        project = selected.expanduser().resolve()
        if not is_project(project):
            raise ValueError('--project 必須指向已解壓的 V29 或 V30 專案資料夾：' + str(project))
        return project
    for candidate in (folder, folder / 'MacGyver_Engineering_Academy_v30', folder / 'MacGyver_Engineering_Academy_v29',
                      folder.parent / 'MacGyver_Engineering_Academy_v29'):
        if is_project(candidate) and project_version(candidate) in (BASE_VERSION, VERSION):
            return candidate.resolve()
    installer = folder / 'Update_MacGyver_v29.sh'
    if installer.is_file() and (folder / 'MacGyver_v29_Alternative_1_of_4.zip').is_file():
        say('找不到已解壓的 V29；先以 Update_MacGyver_v29.sh --extract-only 解壓並校驗 V29（不連線、不上傳）。')
        if subprocess.run(['bash', str(installer), '--extract-only'], cwd=folder).returncode:
            raise ValueError('V29 解壓失敗；請先修正後重試。')
        project = folder / 'MacGyver_Engineering_Academy_v29'
        if is_project(project):
            return project.resolve()
    raise ValueError('找不到 V29 專案。請把本 .sh 與 V30 更新 ZIP 放在 MacGyver_Engineering_Academy_v29 資料夾旁（或其內），'
                     '或用 --project 指定；若只有 V29 的四個 ZIP，請連同 Update_MacGyver_v29.sh 放在同一資料夾。'
                     ' V29 project not found: place this script and the V30 update ZIPs beside (or inside) the V29 folder, or pass --project.')


def archive_expectations(folder, selected):
    if selected:
        document = json.loads(selected.expanduser().resolve().read_text('utf-8'))
    elif EMBEDDED_ARCHIVES_JSON:
        document = json.loads(EMBEDDED_ARCHIVES_JSON)
    else:
        path = folder / 'RELEASE_ARCHIVES_V30.json'
        if path.is_symlink() or not path.is_file():
            raise ValueError('請使用同次發行的 .sh，或補齊 RELEASE_ARCHIVES_V30.json；不跳過 SHA-256 校驗。')
        document = json.loads(path.read_text('utf-8'))
    if document.get('schema') != 1 or document.get('version') != VERSION or document.get('root') != UPDATE_ROOT:
        raise ValueError('V30 發行清單版本不符。')
    expected = {}
    for item in document.get('archives', []):
        name = item.get('filename')
        if (not isinstance(name, str) or not ARCHIVE.fullmatch(name) or name in expected
                or not re.fullmatch(r'[0-9a-f]{64}', item.get('sha256', ''))
                or type(item.get('bytes')) is not int or item['bytes'] <= 0):
            raise ValueError('V30 壓縮檔清單無效。')
        expected[name] = item
    if not expected:
        raise ValueError('V30 壓縮檔清單為空。')
    return document, expected


def find_archives(folder, project, expected):
    for base in (folder, project.parent, project):
        found = [base / name for name in expected if (base / name).is_file() and not (base / name).is_symlink()]
        if len(found) == len(expected):
            return sorted(found, key=lambda p: int(ARCHIVE.fullmatch(p.name).group(1)))
        if found:
            missing = sorted(set(expected) - {p.name for p in found})
            raise ValueError('V30 更新 ZIP 不完整，缺少：' + ', '.join(missing) + '；位置：' + str(base))
    return []


def replace_file(source, target, executable=False):
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=target.parent, delete=False) as temp:
        pending = Path(temp.name)
        with source.open('rb') as stream:
            shutil.copyfileobj(stream, temp, 1024 * 1024)
    pending.chmod(0o755 if executable else 0o644)
    os.replace(pending, target)


def write_bytes(target, data):
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=target.parent, delete=False) as temp:
        pending = Path(temp.name)
        temp.write(data)
    pending.chmod(0o644)
    os.replace(pending, target)


def script_payload(raw):
    return raw.decode('utf-8').strip().replace('<', '\\u003c').replace('\u2028', '\\u2028').replace('\u2029', '\\u2029')


def wrapper(group, stem, raw):
    name = f'data/lazy/{group}/{stem}.json'
    return ('/* Generated on-demand data. */\nwindow.MG_LAZY_DATA=window.MG_LAZY_DATA||Object.create(null);\n'
            'window.MG_LAZY_DATA[' + json.dumps(name) + ']={sha256:' + json.dumps(hashlib.sha256(raw).hexdigest())
            + ',value:' + script_payload(raw) + '};\n').encode('utf-8')


def rebuild_curriculum(project, new_entries):
    """featured.json and course parts from the per-course owner chunks, byte for byte."""
    lazy = project / LAZY
    guided = json.loads((lazy / 'index.json').read_text('utf-8'))['guidedIds']
    owner = json.loads((lazy / 'owner-index.json').read_text('utf-8'))['courses']
    parts_dir = project / PARTS_DIR
    parts_dir.mkdir(parents=True, exist_ok=True)
    featured = project / FEATURED
    parts, batch, used = [], [], 0

    def flush():
        nonlocal batch, used
        if not batch:
            return
        content = b'[' + b','.join(raw for _, raw in batch) + b']\n'
        sha = hashlib.sha256(content).hexdigest()
        name = f'part-{len(parts) + 1:04d}-{sha[:16]}.json'
        if len(content) > PART_BUDGET:
            raise ValueError('課程分段超過 7 MiB 上限：' + name)
        write_bytes(parts_dir / name, content)
        parts.append({'file': name, 'byteLength': len(content), 'sha256': sha,
                      'courseCount': len(batch), 'courseIds': [cid for cid, _ in batch]})
        batch, used = [], 0

    with tempfile.NamedTemporaryFile(dir=featured.parent, prefix='.featured-', suffix='.tmp', delete=False) as stream:
        pending = Path(stream.name)
        stream.write(b'[')
        for number, cid in enumerate(guided):
            descriptor = owner.get(cid)
            if not descriptor or not re.fullmatch(r'data/lazy/owner-courses/[a-z0-9_-]+\.json', descriptor.get('file', '')):
                raise ValueError('缺少完整課程描述：' + cid)
            path = safe_target(project, 'public/academy/' + descriptor['file'])
            raw = path.read_bytes() if path.is_file() else b''
            if len(raw) != descriptor['byteLength'] or hashlib.sha256(raw).hexdigest() != descriptor['sha256']:
                raise ValueError('完整課程檔與清單不符（V29 專案可能不完整或已被修改）：' + descriptor['file'])
            raw = raw[:-1] if raw.endswith(b'\n') else raw
            if number:
                stream.write(b',')
            stream.write(raw)
            # Same budget rule as tools/build-offline.mjs (script-safe escapes counted).
            length = len(raw) + 5 * raw.count(b'<') + 3 * raw.count(b'\xe2\x80\xa8') + 3 * raw.count(b'\xe2\x80\xa9')
            if length > PART_BUDGET:
                raise ValueError('單一課程超過分段上限：' + cid)
            if batch and used + length + len(batch) + 512 > PART_BUDGET:
                flush()
            batch.append((cid, raw))
            used += length
        stream.write(b']\n')
    flush()
    pending.chmod(0o644)
    os.replace(pending, featured)
    manifest = {'schemaVersion': 1, 'dataSet': 'featured', 'courseCount': len(guided), 'parts': parts}
    write_bytes(parts_dir / 'index.json', (json.dumps(manifest, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
    wanted = {'index.json', *(part['file'] for part in parts)}
    for old in parts_dir.iterdir():
        if re.fullmatch(r'part-\d{4}-[0-9a-f]{16}\.json', old.name) and old.name not in wanted:
            old.unlink()
    return len(guided), len(parts)


def apply_update(project, folder, selected_manifest, accept_local, verify_all):
    version = project_version(project)
    if version not in (BASE_VERSION, VERSION):
        raise ValueError('專案版本必須是 V29 或 V30；目前：' + str(version))
    manifest_path = safe_target(project, MANIFEST_NAME)
    already = version == VERSION and manifest_path.is_file()
    try:
        document, expected = archive_expectations(folder, selected_manifest)
        archives = find_archives(folder, project, expected)
    except ValueError:
        if not already:
            raise
        document, expected, archives = {}, {}, []
    if not archives:
        if already:
            say('專案已是 V30，且未提供更新 ZIP：略過安裝，直接使用現有 V30。')
            return
        raise ValueError('找不到 V30 更新 ZIP（' + ', '.join(sorted(expected)) + '）；請與本 .sh 放在同一資料夾。')
    for archive in archives:
        item = expected[archive.name]
        say('SHA-256 校驗：' + archive.name)
        if archive.stat().st_size != item['bytes'] or digest(archive) != item['sha256']:
            raise ValueError('壓縮檔校驗失敗，尚未變更任何檔案：' + archive.name)
    total, names = 0, set()
    for archive in archives:
        with zipfile.ZipFile(archive) as zipped:
            for info in zipped.infolist():
                relative = safe_path(info.filename)
                mode = info.external_attr >> 16
                if relative.parts[0] != UPDATE_ROOT or (len(relative.parts) < 2 and not info.is_dir()):
                    raise ValueError('壓縮檔根目錄不符。')
                if info.flag_bits & 1 or stat.S_ISLNK(mode) or (stat.S_IFMT(mode) and not (stat.S_ISREG(mode) or stat.S_ISDIR(mode))):
                    raise ValueError('壓縮檔含加密、符號連結或特殊檔案。')
                if not info.is_dir():
                    if info.filename.casefold() in names:
                        raise ValueError('壓縮檔重複路徑或大小寫衝突。')
                    names.add(info.filename.casefold())
                    total += info.file_size
                    if total > 4 * 1024 ** 3 or len(names) > 60000:
                        raise ValueError('壓縮檔超過套件容量上限。')
    if shutil.disk_usage(project).free < total * 2 + 2 * 1024 ** 3:
        raise ValueError('磁碟空間不足：更新需要約 %.1f GiB 可用空間。' % ((total * 2 + 2 * 1024 ** 3) / 1024 ** 3))
    base_path = safe_target(project, BASE_MANIFEST_NAME)
    if not base_path.is_file():
        raise ValueError('專案缺少 RELEASE_FILES_V29.json，無法確認 V29 基準；請先以 V29 套件完整安裝。')
    base = entries(base_path, BASE_VERSION)
    with tempfile.TemporaryDirectory(prefix='.macgyver-v30-unpack-', dir=project) as temporary:
        staging = Path(temporary)
        for archive in archives:
            say('解壓並驗證 CRC：' + archive.name)
            with zipfile.ZipFile(archive) as zipped:
                for info in zipped.infolist():
                    target = staging.joinpath(*PurePosixPath(info.filename).parts)
                    if info.is_dir():
                        target.mkdir(parents=True, exist_ok=True)
                        continue
                    target.parent.mkdir(parents=True, exist_ok=True)
                    with zipped.open(info) as source, target.open('xb') as dest:
                        shutil.copyfileobj(source, dest, 1024 * 1024)
        incoming = staging / UPDATE_ROOT
        manifest, plan_file = incoming / MANIFEST_NAME, incoming / PLAN_NAME
        if (not manifest.is_file() or not plan_file.is_file() or digest(manifest) != document.get('releaseFilesSha256')
                or digest(plan_file) != document.get('planSha256')):
            raise ValueError('更新套件的逐檔清單或更新計畫 SHA-256 不符。')
        new_entries = entries(manifest, VERSION)
        plan = json.loads(plan_file.read_text('utf-8'))
        if plan.get('schema') != 1 or plan.get('version') != VERSION or plan.get('base') != BASE_VERSION:
            raise ValueError('更新計畫版本不符。')
        if json.loads(manifest.read_text('utf-8')).get('baseReleaseFilesSha256') != digest(base_path):
            raise ValueError('此更新是針對另一份 V29 發行檔製作；RELEASE_FILES_V29.json 不相符。')
        ship, rebuild, remove = (plan.get(key) for key in ('ship', 'rebuild', 'remove'))
        if not all(isinstance(group, list) and all(isinstance(name, str) for name in group) for group in (ship, rebuild, remove)):
            raise ValueError('更新計畫格式無效。')
        actual = {p.relative_to(incoming).as_posix() for p in incoming.rglob('*') if p.is_file()}
        if actual != set(ship) | {MANIFEST_NAME, PLAN_NAME} or not set(ship) | set(rebuild) <= set(new_entries):
            raise ValueError('更新套件內容與更新計畫不一致。')
        for name in ship:
            source = incoming / name
            if source.stat().st_size != new_entries[name]['bytes'] or digest(source) != new_entries[name]['sha256']:
                raise ValueError('解壓後逐檔校驗失敗：' + name)
        say('檢查本機修改（不覆寫你改過的檔案）…')
        operations, conflicts = [], []
        for name in ship:
            target = safe_target(project, name)
            if target.exists() and not target.is_file():
                raise ValueError('目的檔案位置已被資料夾佔用：' + name)
            current = digest(target) if target.is_file() else None
            if current == new_entries[name]['sha256']:
                continue
            if current is not None and current != base.get(name, {}).get('sha256'):
                conflicts.append(name)
                operations.append((incoming / name, safe_target(project, CONFLICT_DIR + '/' + name), name))
            else:
                operations.append((incoming / name, target, name))
        blocked = []
        for name in rebuild:
            target = safe_target(project, name)
            if target.is_file() and name in base:
                current = digest(target)
                if current not in (base[name]['sha256'], new_entries[name]['sha256']):
                    blocked.append(name)
        report = safe_target(project, CONFLICT_DIR + '/CONFLICTS.json')
        if blocked and not accept_local:
            raise ValueError('下列由程式產生的教材檔已被本機修改，無法安全重建（尚未變更任何檔案）：' + ', '.join(blocked[:5])
                             + (' …' if len(blocked) > 5 else '') + '。若這些修改可以捨棄，請加 --accept-local-changes；'
                             '若你改過課程內容，請改用 tools/integrate-curriculum-v30.py 與 node tools/build-offline.mjs 重新整合。')
        for source, target, name in operations:
            replace_file(source, target, executable=name.endswith(('.sh', '.command')))
        say('已安裝 %d 個新增或更新的檔案。' % (len(operations) - len(conflicts)))
        say('重建指令稿包裝、完整課程檔與課程分段（只用 Python）…')
        wrappers = 0
        for name in rebuild:
            match = WRAPPED.match(name)
            if not match:
                continue
            source = safe_target(project, name[:-3] + '.json')
            if not source.is_file():
                raise ValueError('缺少可重建的 JSON：' + name[:-3] + '.json')
            write_bytes(safe_target(project, name), wrapper(match.group(1), match.group(2), source.read_bytes()))
            wrappers += 1
        if LAZY + 'owner-index.js' in rebuild:
            raw = safe_target(project, LAZY + 'owner-index.json').read_bytes()
            write_bytes(safe_target(project, LAZY + 'owner-index.js'), ('window.MG_OWNER_INDEX=' + script_payload(raw) + ';\n').encode('utf-8'))
        courses, parts = rebuild_curriculum(project, new_entries)
        say('已重建 %d 個包裝檔、%d 門完整課程、%d 個課程分段。' % (wrappers, courses, parts))
        removed = kept = 0
        for name in remove:
            if name in new_entries:
                continue
            target = safe_target(project, name)
            if not target.is_file():
                continue
            if digest(target) == base.get(name, {}).get('sha256'):
                target.unlink()
                removed += 1
            else:
                kept += 1
        say('已移除 %d 個被取代的 V29 產生檔；保留 %d 個本機改過的舊檔。' % (removed, kept))
        check = sorted(new_entries) if verify_all else sorted(set(ship) | set(rebuild))
        say('校驗 %d 個檔案的 SHA-256%s…' % (len(check), '（完整）' if verify_all else '（本次新增、更新與重建）'))
        failed = []
        for name in check:
            if name in conflicts:
                continue
            target = safe_target(project, name)
            if not target.is_file() or target.stat().st_size != new_entries[name]['bytes'] or digest(target) != new_entries[name]['sha256']:
                failed.append(name)
        if failed:
            raise ValueError('更新後校驗失敗（%d 個）：%s%s。請勿上傳；可重新執行本指令，或回報此訊息。'
                             % (len(failed), ', '.join(failed[:5]), ' …' if len(failed) > 5 else ''))
        replace_file(manifest, manifest_path)
        replace_file(plan_file, safe_target(project, PLAN_NAME))
        if conflicts:
            report.parent.mkdir(parents=True, exist_ok=True)
            report.write_text(json.dumps({'version': VERSION, 'status': 'review-required', 'files': conflicts}, ensure_ascii=False, indent=2) + '\n', 'utf-8')
            say('保留你的本機修改；%d 個新版對照檔位於 %s。' % (len(conflicts), CONFLICT_DIR))
        elif report.is_file():
            report.unlink()
    if project_version(project) != VERSION:
        raise ValueError('更新後版本標記不是 V30。')
    say('V30 更新完成並通過校驗：' + str(project))


def main():
    parser = argparse.ArgumentParser(prog='Update_MacGyver_v30.sh', description='V30 一鍵更新與上傳：先把 V30 更新套用到 V29 專案並逐檔校驗，再更新公開網站並觸發 Pages；--with-assets 才上傳現有私人文件／模型權重。需要 Python 3.10+、Git SSH、已登入的 gh。--update-only 只安裝不連線。')
    parser.add_argument('--project', type=Path, help='指定已解壓的 V29（或已更新的 V30）專案資料夾')
    parser.add_argument('--update-only', '--extract-only', dest='update_only', action='store_true', help='只套用並校驗 V30 更新；不連線、不上傳')
    parser.add_argument('--verify-all', action='store_true', help='更新後校驗全部檔案（約多 1–3 分鐘）')
    parser.add_argument('--accept-local-changes', action='store_true', help='已自行檢閱衝突後繼續；不覆寫你改過的原始檔')
    parser.add_argument('--website-only', action='store_true', help='不傳私人文件／模型；仍更新公開網站')
    parser.add_argument('--no-publish-pages', action='store_true', help='只上傳，不觸發 Pages；不需要 gh')
    parser.add_argument('--publish-pages', action='store_true', help='上傳完成後以已登入的 gh 觸發 GitHub Pages 部署')
    parser.add_argument('--dry-run', action='store_true', help='更新並連線比較；不提交、不推送')
    parser.add_argument('--with-assets', action='store_true', help='將現有模型權重與私人文件另送私人 PRIVATE-MODELS')
    parser.add_argument('--manifest', type=Path, help='同次 RELEASE_ARCHIVES_V30.json')
    parser.add_argument('--models-dir', type=Path)
    parser.add_argument('--documents-dir', type=Path)
    parser.add_argument('--state', type=Path, help='專案以外的比較快取位置')
    parser.add_argument('--batch-mib', type=int, choices=range(40, 1025), metavar='40..1024')
    parser.add_argument('--cloud-worker', metavar='HTTPS_ORIGIN', help='連接 Worker、更新公開知識庫（生成式 AI 師傅），再上傳網站')
    parser.add_argument('--knowledge-dir', type=Path, help='核准公開知識文件資料夾；需要 --cloud-worker')
    parser.add_argument('--cloud-only', action='store_true', help='只同步 Cloudflare 知識庫；需要 --cloud-worker')
    parser.add_argument('--cloud-translation', choices=('on', 'off'), help='設定公開頁翻譯；需同步啟用 Worker 的翻譯端點')
    args = parser.parse_args(sys.argv[2:])
    if args.website_only and (args.with_assets or args.models_dir or args.documents_dir):
        parser.error('--website-only 不可同時要求私人資產。')
    if args.no_publish_pages and args.publish_pages:
        parser.error('--no-publish-pages 不可搭配 --publish-pages。')
    if not (args.update_only or args.cloud_only):
        args.publish_pages = args.publish_pages or (not args.dry_run and not args.no_publish_pages)
    if (args.models_dir or args.documents_dir) and not args.with_assets:
        parser.error('--models-dir / --documents-dir 需要 --with-assets。')
    if (args.knowledge_dir or args.cloud_only or args.cloud_translation) and not args.cloud_worker:
        parser.error('Cloudflare 選項需要 --cloud-worker。')
    if args.update_only and (args.with_assets or args.dry_run or args.cloud_worker or args.publish_pages):
        parser.error('--update-only 只安裝更新。')
    if args.dry_run and (args.cloud_worker or args.publish_pages):
        parser.error('--dry-run 不變更雲端資料或發布網站。')
    if args.cloud_only and (args.with_assets or args.publish_pages or args.cloud_translation):
        parser.error('--cloud-only 只同步公開知識庫。')
    if args.publish_pages:
        if not shutil.which('gh') or subprocess.run(['gh', 'auth', 'status', '--hostname', 'github.com'],
                                                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode:
            parser.error('預設會觸發 GitHub Pages，需要先執行 gh auth login；或加 --no-publish-pages 只上傳。')
    folder = Path(sys.argv[1]).resolve()
    project = find_project(folder, args.project)
    say('專案位置：' + str(project))
    apply_update(project, folder, args.manifest, args.accept_local_changes, args.verify_all)
    report = safe_target(project, CONFLICT_DIR + '/CONFLICTS.json')
    if report.is_file():
        pending = json.loads(report.read_text('utf-8'))
        if pending.get('status') == 'review-required':
            if args.accept_local_changes:
                pending['status'] = 'local-changes-reviewed'
                report.write_text(json.dumps(pending, ensure_ascii=False, indent=2) + '\n', 'utf-8')
                say('保留已檢閱的本機修改；新版對照檔仍留在 ' + CONFLICT_DIR + '。')
            elif not args.update_only:
                raise ValueError('有 %d 個本機修改與新版衝突；未上傳混合版本。請檢閱 %s/CONFLICTS.json 並整合；完成後加 --accept-local-changes。'
                                 % (len(pending.get('files', [])), CONFLICT_DIR))
    if args.update_only:
        say('更新完成；尚未連線或上傳。本機啟動：bash "' + str(project / 'run-local.sh') + '"')
        return 0
    if args.cloud_worker:
        cloud_script = project / 'Configure_MacGyver_Cloud_v23.sh'
        if not cloud_script.is_file():
            raise ValueError('Cloudflare 上傳需使用含 Worker 原始碼的完整套件。')
        cloud = ['bash', str(cloud_script)]
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
            for base in (folder, project.parent, project.parent / 'MacGyver_Engineering_Academy_v29', project.parent / 'MacGyver_Engineering_Academy_v28'):
                candidate = base / dirname
                if candidate != project / dirname and has_content(candidate):
                    resolved = candidate.resolve()
                    if resolved not in candidates:
                        candidates.append(resolved)
            if len(candidates) > 1:
                raise ValueError('找到多個 ' + dirname + ' 來源；請用 --' + argument.replace('_', '-') + ' 指定要上傳的資料夾。')
            if candidates:
                setattr(args, argument, candidates[0])
                say('沿用本機資產來源：' + str(candidates[0]))
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
    say('公開網站：macgyver-academy；' + ('私人資產：PRIVATE-MODELS。' if args.with_assets else '此次不傳私人資產。') + '只傳差異，可重跑續傳，不下載權重、不強推。')
    status = subprocess.run(command, cwd=project).returncode
    if status or not args.publish_pages:
        return status
    return subprocess.run([*doctor, '--publish'], cwd=project).returncode


try:
    sys.exit(main())
except KeyboardInterrupt:
    print('已中止；可重新執行續傳。', file=sys.stderr)
    sys.exit(130)
except (OSError, ValueError, KeyError, TypeError, zipfile.BadZipFile) as error:
    print('停止：' + str(error), file=sys.stderr)
    sys.exit(1)
PY
