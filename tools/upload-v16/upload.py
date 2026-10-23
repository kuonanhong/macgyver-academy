#!/usr/bin/env python3
"""Upload the public V16 source and existing private assets without downloads."""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import socket
import subprocess
import sys
import tempfile
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
import zipfile

ROOT = Path(__file__).resolve().parents[2]
SITE_REPO = 'git@github.com:kuonanhong/macgyver-academy.git'
PRIVATE_REPO = 'git@github.com:kuonanhong/PRIVATE-MODELS.git'
PREFIX = 'projects/macgyver/v16-assets'
MANIFEST = PREFIX + '/assets-manifest.json'
STATE_MARKER = '.macgyver-v16-upload-state.json'
WEIGHTS = {'.gguf', '.safetensors', '.onnx', '.bin', '.pt', '.pth', '.ckpt', '.model', '.h5', '.hdf5', '.pb', '.npy', '.npz'}
MODEL_SIDE = {'.json', '.txt', '.md', '.tiktoken', '.vocab', '.merges', '.yaml', '.yml'}
DOCUMENTS = {'.txt', '.md', '.csv', '.tsv', '.json', '.pdf', '.docx', '.pptx', '.xlsx', '.odt', '.ods', '.odp', '.html', '.htm', '.rtf', '.tex'}
BLOCK_DIRS = {'owner-private', 'portable', 'credentials', 'secrets', 'accounts', 'auth', 'userdata', 'user-data', 'node_modules', '__pycache__', 'cache', 'parts'}
BLOCK_NAMES = {'id_rsa', 'id_ed25519', 'id_dsa', '.netrc', '.git-credentials', 'cookies.txt', 'cookies.json', 'token.json', 'tokens.json', 'credentials.json', 'accounts.json', 'users.json', 'owner.json'}
BLOCK_NAME_RE = re.compile(r'(?i)(?:^|[._-])(?:passwords?|passwd|credentials?|secrets?|api[_-]?keys?|access[_-]?tokens?|private[_-]?keys?|account[_-]?db)(?:[._-]|$)')
SECRET = re.compile(
    rb'(?:github_pat_[A-Za-z0-9_]{30,}|gh[pousr]_[A-Za-z0-9_]{30,}|'
    rb'(?<![A-Za-z0-9_])sk-(?:proj-)?[A-Za-z0-9_-]{40,}|'
    rb'-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----|'
    rb'\$2[aby]\$\d\d\$[./A-Za-z0-9]{40,}|\$argon2(?:id|i|d)\$|'
    rb'(?i:(?:password_hash|passwordHash|secret_key|api_key|apiKey|access_token|refresh_token|client_secret))'
    rb'[\s"\x27]*[:=][\s"\x27]*[A-Za-z0-9_./+=$-]{12,}|'
    rb'(?i:(?:password|passwd|passphrase))[\s"\x27]*[:=][\s"\x27]*[^\s"\x27,}<>]{4,})')


def load_engine():
    spec = importlib.util.spec_from_file_location('macgyver_models_v13', ROOT / 'tools/sync-v13/models_sync.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.PREFIX = PREFIX
    return module


def note(message):
    print(message, flush=True)


def safe_relative(value):
    p = PurePosixPath(value)
    return bool(value) and not p.is_absolute() and '..' not in p.parts and '\\' not in value and '\x00' not in value


def scan_stream(stream, label):
    tail = b''
    while block := stream.read(1024 * 1024):
        data = tail + block
        if SECRET.search(data):
            raise ValueError('疑似金鑰、密碼雜湊或登入憑證，停止；未顯示秘密內容：' + label)
        tail = data[-2048:]


def collect(directory: Path, kind: str):
    if not directory.exists():
        note(f'{kind}：資料夾不存在，略過：{directory}')
        return []
    if directory.is_symlink() or not directory.is_dir():
        raise ValueError('只接受實際資料夾，不接受符號連結：' + str(directory))
    base = directory.resolve()
    if any(x.lower() in BLOCK_DIRS for x in base.parts[1:]) or base.name.startswith('.'):
        raise ValueError('不接受登入、憑證或系統資料夾及其子資料夾：' + str(base))
    allowed = WEIGHTS | MODEL_SIDE if kind == 'models' else DOCUMENTS
    result, skipped = [], 0
    for folder, dirs, names in os.walk(base, followlinks=False):
        dirs[:] = sorted(d for d in dirs if not d.startswith('.') and d.lower() not in BLOCK_DIRS and not (Path(folder) / d).is_symlink())
        for name in sorted(names):
            path = Path(folder) / name
            rel = path.relative_to(base)
            if path.is_symlink() or not path.is_file() or name.startswith('.') or name.lower() in BLOCK_NAMES or BLOCK_NAME_RE.search(name) or path.suffix.lower() not in allowed:
                skipped += 1
                continue
            if kind == 'models' and name.lower() == 'readme.md':
                continue
            with path.open('rb') as f:
                scan_stream(f, f'{kind}/{rel.as_posix()}')
            if path.suffix.lower() in {'.docx', '.pptx', '.xlsx', '.odt', '.ods', '.odp'}:
                with zipfile.ZipFile(path) as archive:
                    if sum(i.file_size for i in archive.infolist()) > 512 * 1024 * 1024:
                        raise ValueError('文件解壓縮內容超過 512 MiB，請拆成較小文件：' + str(rel))
                    for info in archive.infolist():
                        if info.is_dir():
                            continue
                        if info.flag_bits & 1:
                            raise ValueError('加密文件無法檢查憑證內容，請先解密：' + str(rel))
                        with archive.open(info) as stream:
                            scan_stream(stream, f'{kind}/{rel.as_posix()}')
            result.append(path)
    if kind == 'models' and not any(p.suffix.lower() in WEIGHTS for p in result):
        note('models：沒有現成權重，略過；不自動下載模型。')
        return []
    note(f'{kind}：{len(result)} 個可上傳檔案；排除 {skipped} 個非支援／私有設定檔。')
    return result


def plan_assets(engine, directories):
    plans = []
    for kind, directory, files in directories:
        if kind == 'models':
            engine.verify_pinned(directory, files)
        for item in engine.plan_local(directory, files, engine.chunk_bytes()):
            item['path'] = kind + '/' + item['path']
            plans.append(item)
    return plans


def check_private_repo(repo, test=False):
    """Anonymous 404 plus successful SSH access implies a non-public GitHub repo.

    Public metadata, rate limiting, timeouts and malformed responses fail closed.
    If gh is installed/authenticated, its explicit visibility flag is preferred.
    """
    if test:
        if not repo.startswith('file://'):
            raise ValueError('測試只接受 file:// 遠端。')
        return 'local test only'
    if repo != PRIVATE_REPO:
        raise ValueError('私人檔案僅允許送到固定 PRIVATE-MODELS SSH 倉庫。')
    if shutil.which('gh'):
        r = subprocess.run(['gh', 'api', 'repos/kuonanhong/PRIVATE-MODELS', '--jq', '.private'], capture_output=True, text=True)
        if r.returncode == 0:
            if r.stdout.strip() != 'true':
                raise ValueError('PRIVATE-MODELS 不是 Private，已停止私人檔案上傳。')
            return 'authenticated API: private'
    req = Request('https://api.github.com/repos/kuonanhong/PRIVATE-MODELS', headers={'User-Agent': 'MacGyver-V16-uploader', 'Accept': 'application/vnd.github+json'})
    try:
        with urlopen(req, timeout=20) as response:
            result = json.loads(response.read(200_000))
        if result.get('private') is True:
            return 'API: private'
        raise ValueError('PRIVATE-MODELS 可被匿名讀取，已停止私人檔案上傳。')
    except HTTPError as error:
        if error.code != 404:
            raise ValueError(f'無法確認私人倉庫（HTTP {error.code}），未上傳私人檔案。') from error
    except (URLError, OSError, TimeoutError, ValueError) as error:
        raise ValueError('無法確認 PRIVATE-MODELS 是私人倉庫，未上傳私人檔案；檢查網路或登入 gh auth login。') from error
    r = subprocess.run(['git', 'ls-remote', repo], capture_output=True, text=True)
    if r.returncode:
        raise ValueError('PRIVATE-MODELS 匿名不可讀取，而且 SSH 無法存取；請先建立私人倉庫並授權 SSH key。')
    return 'anonymous API: 404; authenticated SSH: accessible'


def validate_remote_manifest(doc):
    if doc.get('schema') != 1 or not isinstance(doc.get('files'), list):
        raise ValueError('私人資產清單格式不符，停止以保留遠端資料。')
    seen = set()
    for item in doc['files']:
        path = item.get('path', '')
        if not safe_relative(path) or not path.startswith(('models/', 'documents/')) or path in seen:
            raise ValueError('私人資產清單路徑不安全或重複。')
        seen.add(path)
        if not isinstance(item.get('size'), int) or item['size'] < 0 or not re.fullmatch(r'[0-9a-f]{64}', item.get('sha256', '')):
            raise ValueError('私人資產清單雜湊／大小無效。')
        total = 0
        for part in item.get('parts', []):
            if not re.fullmatch(r'parts/[0-9a-f]{2}/[0-9a-f]{64}\.part', part.get('path', '')) or not re.fullmatch(r'[0-9a-f]{64}', part.get('sha256', '')) or not isinstance(part.get('size'), int) or not 0 < part['size'] <= 48 * 1024 * 1024:
                raise ValueError('私人資產清單分片無效。')
            if part['path'] != f"parts/{part['sha256'][:2]}/{part['sha256']}.part":
                raise ValueError('私人資產清單分片路徑與雜湊不符。')
            total += part['size']
        if total != item['size']:
            raise ValueError('私人資產清單分片總大小不符。')
    return doc


def read_manifest(engine, work, tree):
    if MANIFEST not in tree:
        return {'schema': 1, 'files': []}
    try:
        return validate_remote_manifest(json.loads(engine.git(work, 'cat-file', 'blob', tree[MANIFEST])))
    except (KeyError, TypeError, json.JSONDecodeError) as error:
        raise ValueError('遠端私人資產清單損壞，未覆寫。') from error


def upload_assets(engine, plans, repo, branch, state, dry_run=False, batch_mib=120):
    work, tip, tree = engine.open_remote(repo, branch, state)
    old = read_manifest(engine, work, tree)
    fresh = engine.build_manifest(plans)
    merged = {f['path']: f for f in old['files']}
    merged.update({f['path']: f for f in fresh['files']})
    manifest = {'schema': 1, 'project': 'macgyver-academy-v16-private-assets', 'layout': PREFIX + '/',
                'chunk_bytes': engine.chunk_bytes(), 'files': [merged[k] for k in sorted(merged)]}
    # Existing records are retained when a local file is absent: never delete.
    need, have_path, have_blob, _ = engine.summarize(plans, tree, None)
    missing = sum(1 for _, _, new in need if new)
    note(f'私人資產：新增分片 {missing}，既有分片 {have_path}，可重用內容 {have_blob}；保留所有遠端其他檔案。')
    if dry_run:
        note('預覽完成：私人倉庫未寫入。')
        return
    if not need and old['files'] == manifest['files']:
        note('私人資產已是最新。')
        return
    index = state / 'v16-assets.index'
    index.unlink(missing_ok=True)
    env = dict(engine.GIT_ENV, GIT_INDEX_FILE=str(index))
    if tip:
        engine.git(work, 'read-tree', tip, env=env)
    parent, batch_size, done = tip, 0, 0
    for item, part, new in need:
        with item['file'].open('rb') as f:
            f.seek(part['offset'])
            data = f.read(part['size'])
        if len(data) != part['size'] or hashlib.sha256(data).hexdigest() != part['sha256']:
            raise ValueError('上傳期間本地檔案已變更：' + item['path'])
        oid = engine.git(work, 'hash-object', '-w', '--stdin', data=data) if new else part['blob']
        if oid != part['blob']:
            raise ValueError('Git blob 雜湊不符。')
        engine.git(work, 'update-index', '--add', '--cacheinfo', f"100644,{oid},{PREFIX}/{part['path']}", env=env)
        if new:
            done += 1
            batch_size += len(data)
        if new and batch_size >= batch_mib * 1024 * 1024:
            parent = engine.commit_and_push(work, parent, index, f'MacGyver V16 private asset chunks {done}/{missing}', branch)
            batch_size = 0
    raw = (json.dumps(manifest, ensure_ascii=False, indent=2) + '\n').encode()
    oid = engine.git(work, 'hash-object', '-w', '--stdin', data=raw)
    engine.git(work, 'update-index', '--add', '--cacheinfo', f'100644,{oid},{MANIFEST}', env=env)
    engine.commit_and_push(work, parent, index, 'Update MacGyver V16 private documents and models', branch)
    note(f'私人文件／模型完成：{MANIFEST}。中斷後重跑相同命令，已完成批次可重用。')


def restore_assets(engine, repo, branch, state, destination):
    work, tip, tree = engine.open_remote(repo, branch, state)
    if not tip or MANIFEST not in tree:
        raise ValueError('遠端沒有 V16 私人資產清單。')
    doc = read_manifest(engine, work, tree)
    destination = destination.expanduser().resolve()
    destination.mkdir(parents=True, exist_ok=True)
    for item in doc['files']:
        target = destination / item['path']
        if not target.resolve().is_relative_to(destination) or target.is_symlink():
            raise ValueError('還原目的地包含不安全的符號連結。')
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.is_file() and target.stat().st_size == item['size'] and engine.sha256_file(target) == item['sha256']:
            note('已驗證：' + item['path'])
            continue
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(dir=target.parent, prefix='.v16-restoring-', delete=False) as stream:
                temporary = Path(stream.name)
                whole = hashlib.sha256()
                for part in item['parts']:
                    full = PREFIX + '/' + part['path']
                    if full not in tree:
                        raise ValueError('遠端缺少分片：' + full)
                    r = subprocess.run(['git', '-C', str(work), 'cat-file', 'blob', tree[full]], capture_output=True, check=True, env=engine.GIT_ENV)
                    data = r.stdout
                    if len(data) != part['size'] or hashlib.sha256(data).hexdigest() != part['sha256']:
                        raise ValueError('分片 SHA-256 不符：' + full)
                    stream.write(data)
                    whole.update(data)
            if temporary.stat().st_size != item['size'] or whole.hexdigest() != item['sha256']:
                raise ValueError('還原整檔 SHA-256 不符：' + item['path'])
            os.replace(temporary, target)
            note('已還原並驗證：' + item['path'])
        finally:
            if temporary is not None:
                temporary.unlink(missing_ok=True)


@contextlib.contextmanager
def owned_state(path, source):
    path = path.expanduser().resolve()
    source = source.resolve()
    if path == source or source in path.parents or path in source.parents:
        raise ValueError('上傳狀態資料夾必須在專案外，不能是專案的上層。')
    marker = path / STATE_MARKER
    if path.exists() and any(path.iterdir()) and not marker.is_file():
        raise ValueError('狀態資料夾不是本工具建立；請用 --state 指定新的空資料夾。')
    path.mkdir(parents=True, exist_ok=True)
    expected = {'version': 1, 'source': str(source), 'site_repo': SITE_REPO, 'private_repo': PRIVATE_REPO}
    if marker.exists():
        if json.loads(marker.read_text('utf-8')) != expected:
            raise ValueError('狀態資料夾屬於其他來源，請另用 --state。')
    else:
        marker.write_text(json.dumps(expected, indent=2) + '\n', 'utf-8')
    lock = path / '.upload-running.json'
    record = {'pid': os.getpid(), 'host': socket.gethostname()}
    if lock.exists():
        previous = json.loads(lock.read_text('utf-8'))
        if previous.get('host') != record['host']:
            raise ValueError('狀態資料夾在另一台電腦使用中。')
        try:
            os.kill(int(previous['pid']), 0)
        except ProcessLookupError:
            lock.unlink()
        else:
            raise ValueError('另一個上傳程序正在使用狀態資料夾。')
    with lock.open('x', encoding='utf-8') as stream:
        json.dump(record, stream)
    try:
        yield path
    finally:
        lock.unlink(missing_ok=True)


def main(argv=None):
    ap = argparse.ArgumentParser(description='V16 一鍵 SSH：公開網站差異 → macgyver-academy；現成模型與 local-documents → PRIVATE-MODELS。無自動下載、無刪除、無強推。')
    ap.add_argument('--dry-run', action='store_true', help='連線比較，不提交、不上傳；會建立本地比較快取')
    ap.add_argument('--skip-models', action='store_true', help='略過模型；文件仍可上傳')
    ap.add_argument('--skip-documents', action='store_true', help='略過私人文件')
    # V15 upload-all callers may still pass this. V16 never refreshes markets.
    ap.add_argument('--skip-data', action='store_true', help=argparse.SUPPRESS)
    ap.add_argument('--models-dir', type=Path, default=ROOT / 'models')
    ap.add_argument('--documents-dir', type=Path, default=ROOT / 'local-documents')
    ap.add_argument('--state', type=Path, default=ROOT.parent / 'MacGyver_v16_SSH_Upload_State')
    ap.add_argument('--branch', default='main')
    ap.add_argument('--batch-mib', type=int, default=120, choices=range(40, 1025), metavar='40..1024')
    ap.add_argument('--restore-assets', type=Path, metavar='DEST', help='僅還原私人 documents/ 與 models/ 並核對 SHA-256，不上傳網站')
    args = ap.parse_args(argv)
    if not shutil.which('git') or not shutil.which('ssh'):
        raise ValueError('需要 Git 與 SSH。macOS 可執行 xcode-select --install。')
    if subprocess.run(['git', 'check-ref-format', '--branch', args.branch], capture_output=True).returncode:
        raise ValueError('Git 分支名稱無效。')
    os.environ.setdefault('GIT_TERMINAL_PROMPT', '0')
    os.environ.setdefault('GIT_SSH_COMMAND', 'ssh -o BatchMode=yes -o ConnectTimeout=20 -o ServerAliveInterval=15 -o ServerAliveCountMax=3')
    site_repo, private_repo = SITE_REPO, PRIVATE_REPO
    test = os.environ.get('MACGYVER_UPLOAD_V16_TEST') == '1'
    if test:
        site_repo = os.environ.get('MACGYVER_UPLOAD_V16_TEST_SITE', '')
        private_repo = os.environ.get('MACGYVER_UPLOAD_V16_TEST_PRIVATE', '')
        if not site_repo.startswith('file://') or not private_repo.startswith('file://'):
            raise ValueError('測試模式只接受兩個本地 file:// 倉庫。')
        os.environ['MACGYVER_SYNC_TEST_REMOTE'] = '1'
        os.environ['MACGYVER_MODELS_TEST_REMOTE'] = '1'
    engine = load_engine()
    if not args.dry_run and not args.restore_assets:
        for key in ('user.name', 'user.email'):
            if not subprocess.run(['git', 'config', '--get', key], capture_output=True, text=True).stdout.strip():
                raise ValueError(f'請先設定 git config --global {key} "你的資料"。')
    directories = []
    if not args.restore_assets:
        for kind, selected, skip in (('models', args.models_dir, args.skip_models), ('documents', args.documents_dir, args.skip_documents)):
            if not skip:
                selected = selected.expanduser()
                files = collect(selected, kind)
                if files:
                    directories.append((kind, selected.resolve(), files))
    if directories or args.restore_assets:
        note('檢查 PRIVATE-MODELS 可見性：' + check_private_repo(private_repo, test))
    plans = plan_assets(engine, directories)
    with owned_state(args.state, ROOT) as state:
        if args.restore_assets:
            if args.dry_run:
                raise ValueError('--restore-assets 不可搭配 --dry-run。')
            restore_assets(engine, private_repo, args.branch, state, args.restore_assets)
            return 0
        note('① 網站：只上傳新增與修改的公開原始碼；保留遠端其他檔案。')
        command = [sys.executable, str(ROOT / 'tools/sync-v12/sync_github.py'), '--repo', site_repo, '--branch', args.branch,
                   '--state', str(state), '--no-delete', '--message', 'Update MacGyver Engineering Academy V16']
        if not args.dry_run:
            command.append('--push')
        subprocess.run(command, check=True)
        if plans:
            note('② 私人文件／模型：40 MiB 分片，已完成批次重用，不刪除遠端資產。')
            upload_assets(engine, plans, private_repo, args.branch, state, args.dry_run, args.batch_mib)
        else:
            note('② 沒有選定的現成私人文件或模型，略過；不下載模型。')
    note('預覽完成，遠端未變更。' if args.dry_run else '上傳完成。網站是否發布，請查看 GitHub Actions／Pages；本工具不自動發布。')
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (ValueError, OSError, RuntimeError, subprocess.CalledProcessError, zipfile.BadZipFile) as error:
        print('停止：' + str(error), file=sys.stderr)
        sys.exit(1)
