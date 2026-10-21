#!/usr/bin/env python3
"""V13: compare, upload, restore and import AI model weights for the PRIVATE-MODELS repo.

Shared-repository layout (works next to the HuaTuo academy's files):

    PRIVATE-MODELS/
      projects/huatuo/v3/...                 ← HuaTuo academy (never touched here)
      projects/macgyver/weights-manifest.json
      projects/macgyver/parts/<aa>/<sha256>.part   (40 MiB content-addressed chunks)

How "only upload what is new" works:
  * The repository is cloned with --filter=blob:none (trees only, no weight
    bytes are downloaded) and the remote file list with Git blob ids is read.
  * Every local model is cut into 40 MiB chunks (the same size the HuaTuo
    uploader uses). A chunk is named by its SHA-256, and its Git blob id is
    computed locally. If the same path — or an identical blob anywhere in the
    repository, e.g. a HuaTuo chunk of the same Qwen3 file — already exists,
    Git does not send those bytes again.
  * Only paths under projects/macgyver/ are added or removed. Chunks that the
    new manifest no longer references are deleted in the same final commit
    that publishes the manifest, so readers never see a missing chunk.
  * Large uploads are pushed in batches; rerunning the same command resumes.

Commands:
  compare        list local models and what would be uploaded / removed (no upload)
  push           upload new chunks + manifest (needs --private-confirmed)
  restore        rebuild and verify the models from the repository into a folder
  import-huatuo  rebuild Qwen3-0.6B-Q8_0.gguf from the four HuaTuo model ZIPs
                 (HuaTuo_v2_Qwen3_CPU_part1of4.zip … part4of4.zip) or copy a
                 verified GGUF from a HuaTuo folder, so it need not be downloaded again

Examples:
  python3 tools/sync-v13/models_sync.py compare --repo git@github.com:kuonanhong/PRIVATE-MODELS.git --models-dir models
  python3 tools/sync-v13/models_sync.py push    --repo git@github.com:kuonanhong/PRIVATE-MODELS.git --models-dir models --private-confirmed
  python3 tools/sync-v13/models_sync.py restore --repo git@github.com:kuonanhong/PRIVATE-MODELS.git --to ~/macgyver-models
  python3 tools/sync-v13/models_sync.py import-huatuo --search ~/Downloads --to models
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[2]
PREFIX = 'projects/macgyver'
CHUNK_MIB = 40
MAX_CHUNK = 48 * 1024 * 1024
WEIGHT_EXT = {'.gguf', '.safetensors', '.onnx', '.bin', '.pt', '.pth', '.model'}
SIDE_EXT = {'.json', '.txt', '.md', '.tiktoken', '.vocab', '.merges'}
BATCH_BYTES = 120 * 1024 * 1024  # small commit checkpoints; an interrupted pack may retransmit
GIT_ENV = dict(os.environ, GIT_TERMINAL_PROMPT='0')
GIT_ENV.setdefault('GIT_SSH_COMMAND','ssh -o BatchMode=yes -o ConnectTimeout=20 -o ServerAliveInterval=15 -o ServerAliveCountMax=3')


def chunk_bytes() -> int:
    """40 MiB in production; tests with a local file:// remote may use small chunks."""
    test = os.environ.get('MACGYVER_MODELS_TEST_CHUNK_BYTES', '')
    if os.environ.get('MACGYVER_MODELS_TEST_REMOTE') == '1' and test.isdigit():
        if not 1<=int(test)<=MAX_CHUNK:raise ValueError('Invalid test chunk size')
        return int(test)
    return CHUNK_MIB * 1024 * 1024
SSH_URL = re.compile(r'^(?:git@github\.com:|ssh://git@github\.com/)([A-Za-z0-9-]+)/([A-Za-z0-9._-]+?)(?:\.git)?/?$')


def say(msg: str) -> None:
    print(msg, flush=True)


def git(cwd: Path, *args: str, data: bytes | None = None, env: dict | None = None, check: bool = True) -> str:
    r = subprocess.run(['git', '-C', str(cwd), *args], input=data, capture_output=True, env=env or GIT_ENV)
    if check and r.returncode != 0:
        raise RuntimeError(f'git {" ".join(args[:3])} failed: {r.stderr.decode(errors="replace")[-800:]}')
    return r.stdout.decode(errors='replace').rstrip('\n')


def blob_id(data: bytes) -> str:
    return hashlib.sha1(b'blob %d\0' % len(data) + data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(4 * 1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def manifest_models() -> list[dict]:
    return json.loads((ROOT / 'tools/model-manifest.json').read_text('utf-8'))['models']


# ----------------------------------------------------------------- local side
def local_files(models_dir: Path) -> list[Path]:
    out = []
    for base, dirs, names in os.walk(models_dir, followlinks=False):
        dirs[:] = sorted(d for d in dirs if not d.startswith('.') and d not in ('parts', 'cache'))
        for name in sorted(names):
            p = Path(base) / name
            if name.startswith('.') or p.is_symlink() or not p.is_file():
                continue
            ext = p.suffix.lower()
            if ext in WEIGHT_EXT or (ext in SIDE_EXT and name.lower() not in ('readme.md',)):
                out.append(p)
    if not any(p.suffix.lower() in WEIGHT_EXT for p in out):
        raise SystemExit(f'{models_dir} 裡沒有模型權重（.gguf 等）。先執行：bash macgyver.sh models 會自動下載或從華佗 ZIP 匯入。')
    return out


def verify_pinned(models_dir: Path, files: list[Path]) -> None:
    """Pinned official models must match their SHA-256 before anything is uploaded."""
    pinned = {m['file']: m for m in manifest_models() if m.get('file')}
    for p in files:
        m = pinned.get(p.name)
        if m and (p.stat().st_size != m['bytes'] or sha256_file(p) != m['sha256']):
            raise SystemExit(f'{p.name} 與官方 SHA-256 不符，停止上傳。請刪除後重新下載：bash install-ai-models.sh --model {m["id"]} --download')


def plan_local(models_dir: Path, files: list[Path], chunk_bytes: int):
    """Yield (file entry, [(repo_path, blob, sha256, offset, size)]) without holding whole models in memory."""
    plans = []
    for p in files:
        rel = p.relative_to(models_dir).as_posix()
        whole, parts, offset = hashlib.sha256(), [], 0
        with p.open('rb') as f:
            while data := f.read(chunk_bytes):
                whole.update(data)
                digest = hashlib.sha256(data).hexdigest()
                parts.append({'path': f'parts/{digest[:2]}/{digest}.part', 'size': len(data), 'sha256': digest,
                              'blob': blob_id(data), 'offset': offset})
                offset += len(data)
        plans.append({'file': p, 'path': rel, 'size': offset, 'sha256': whole.hexdigest(), 'parts': parts})
    return plans


# ---------------------------------------------------------------- remote side
def check_private(repo: str) -> str:
    if os.environ.get('MACGYVER_MODELS_TEST_REMOTE') == '1' and repo.startswith('file://'):
        return 'local test remote'
    m = SSH_URL.match(repo)
    if not m:
        raise SystemExit('模型倉庫請用 SSH 網址，例如 git@github.com:kuonanhong/PRIVATE-MODELS.git')
    owner, name = m.group(1), m.group(2)
    try:
        with urlopen(Request(f'https://api.github.com/repos/{owner}/{name}', headers={'User-Agent': 'macgyver-models'}), timeout=15) as r:
            if json.loads(r.read(200_000)).get('private') is False:
                raise SystemExit(f'{owner}/{name} 是公開倉庫！權重倉庫必須是 Private，已停止。')
    except HTTPError as e:
        if e.code == 404:
            return 'private-or-missing (anonymous API 404)'
    except (URLError, TimeoutError, OSError):
        return 'unverified (offline)'
    return 'checked'


def open_remote(repo: str, branch: str, state: Path) -> tuple[Path, str | None, dict[str, str]]:
    """Blob-less shallow clone; returns (work dir, remote tip, {path: blob id})."""
    work = state / 'private-models'
    state.mkdir(parents=True, exist_ok=True)
    if not (work / '.git').is_dir():
        if work.exists():
            shutil.rmtree(work)
        work.mkdir(parents=True)
        git(work, 'init', '-q')
        git(work, 'remote', 'add', 'origin', repo)
        git(work, 'config', 'remote.origin.promisor', 'true')
        git(work, 'config', 'remote.origin.partialclonefilter', 'blob:none')
    elif git(work, 'remote', 'get-url', 'origin') != repo:
        raise SystemExit(f'{work} 指向另一個倉庫；請改用新的 --state 資料夾。')
    heads = subprocess.run(['git', 'ls-remote', '--heads', repo, branch], capture_output=True, text=True, env=GIT_ENV)
    if heads.returncode != 0:
        raise SystemExit('無法連上模型倉庫（請檢查 SSH key 與網路，或先執行 bash macgyver.sh doctor）：\n' + heads.stderr[-600:])
    if not heads.stdout.strip():
        return work, None, {}
    git(work, 'fetch', '--depth', '1', '--filter=blob:none', '--no-tags', 'origin', branch)
    tip = git(work, 'rev-parse', 'FETCH_HEAD')
    tree = {}
    for line in git(work, 'ls-tree', '-r', '--full-tree', tip).splitlines():
        meta, path = line.split('\t', 1)
        mode, kind, oid = meta.split()
        if kind == 'blob':
            tree[path] = oid
    return work, tip, tree


def remote_manifest(work: Path, tip: str | None, tree: dict[str, str]) -> dict | None:
    path = f'{PREFIX}/weights-manifest.json'
    if not tip or path not in tree:
        return None
    try:
        return json.loads(git(work, 'cat-file', 'blob', tree[path]))
    except (RuntimeError, ValueError):
        return None


def build_manifest(plans) -> dict:
    return {'schema': 1, 'project': 'macgyver-academy', 'layout': PREFIX + '/', 'chunk_bytes': chunk_bytes(),
            'updatedAt': dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds'),
            'files': [{'path': p['path'], 'size': p['size'], 'sha256': p['sha256'],
                       'parts': [{'path': x['path'], 'size': x['size'], 'sha256': x['sha256']} for x in p['parts']]} for p in plans]}


def summarize(plans, tree: dict[str, str], old: dict | None):
    blobs = set(tree.values())
    need, have_path, have_blob = [], 0, 0
    seen=set()
    for p in plans:
        for x in p['parts']:
            full = f'{PREFIX}/{x["path"]}'
            if full in seen:continue
            seen.add(full)
            if tree.get(full) == x['blob']:
                have_path += 1
            elif x['blob'] in blobs:
                have_blob += 1; need.append((p, x, False))
            else:
                need.append((p, x, True))
    wanted = {f'{PREFIX}/{x["path"]}' for p in plans for x in p['parts']}
    stale = sorted(k for k in tree if k.startswith(f'{PREFIX}/parts/') and k not in wanted)
    return need, have_path, have_blob, stale


def cmd_compare(a) -> int:
    models_dir = a.models_dir.resolve()
    files = local_files(models_dir)
    plans = plan_local(models_dir, files, chunk_bytes())
    work, tip, tree = open_remote(a.repo, a.branch, a.state)
    old = remote_manifest(work, tip, tree)
    need, have_path, have_blob, stale = summarize(plans, tree, old)
    upload = sum(x['size'] for _, x, new in need if new)
    say(f'模型倉庫比較 / model comparison  ({a.repo} @ {a.branch}，資料夾 {PREFIX}/)')
    for p in plans:
        say(f'  本機 {p["path"]}  {p["size"] / 1024**2:,.1f} MiB  sha256 {p["sha256"][:12]}…  {len(p["parts"])} 片')
    if old:
        say('  雲端已登記：' + '、'.join(f['path'] for f in old.get('files', [])))
    else:
        say('  雲端尚未有 MacGyver 模型清單。')
    huatuo = sum(1 for k in tree if k.startswith('projects/huatuo/'))
    if huatuo:
        say(f'  （同倉庫另有華佗學院檔案 {huatuo} 個，本工具不會修改）')
    say(f'  已存在（相同路徑）：{have_path} 片')
    say(f'  內容相同可直接引用（例如華佗已上傳的相同分片）：{have_blob} 片，不需再傳資料')
    say(f'  需要上傳：{sum(1 for _, _, n in need if n)} 片，約 {upload / 1024**2:,.1f} MiB')
    say(f'  不再使用、將刪除：{len(stale)} 片')
    if not a.json_report:
        return 0
    a.json_report.write_text(json.dumps({'need': [x['path'] for _, x, n in need if n], 'reuse': [x['path'] for _, x, n in need if not n],
                                         'stale': stale, 'uploadBytes': upload}, indent=1), 'utf-8')
    return 0


def commit_and_push(work: Path, parent: str | None, index: Path, message: str, branch: str) -> str:
    env = dict(GIT_ENV, GIT_INDEX_FILE=str(index))
    tree = git(work, 'write-tree', '--missing-ok', env=env)
    args = ['commit-tree', tree, '-m', message] + (['-p', parent] if parent else [])
    commit = git(work, *args)
    for attempt in range(1, 5):
        r = subprocess.run(['git', '-C', str(work), 'push', 'origin', f'{commit}:refs/heads/{branch}'], env=GIT_ENV)
        if r.returncode == 0:
            return commit
        say(f'  第 {attempt} 次上傳中斷，稍後重試（已上傳的批次會保留）…')
        if attempt<4:time.sleep(2**attempt)
    raise SystemExit('上傳未完成。請檢查網路後重跑同一命令，會從已完成的批次接續。')


def cmd_push(a) -> int:
    if not a.private_confirmed:
        raise SystemExit('請先在 GitHub 確認 PRIVATE-MODELS 是 Private，再加 --private-confirmed。')
    say('私人倉庫檢查：' + check_private(a.repo))
    for key in ('user.name', 'user.email'):
        if not subprocess.run(['git', 'config', '--get', key], capture_output=True, text=True).stdout.strip():
            raise SystemExit(f'請先設定 git config --global {key} "…"')
    models_dir = a.models_dir.resolve()
    files = local_files(models_dir)
    verify_pinned(models_dir, files)
    plans = plan_local(models_dir, files, chunk_bytes())
    work, tip, tree = open_remote(a.repo, a.branch, a.state)
    need, have_path, have_blob, stale = summarize(plans, tree, remote_manifest(work, tip, tree))
    manifest = build_manifest(plans)
    raw_manifest = (json.dumps(manifest, ensure_ascii=False, indent=2) + '\n').encode()
    old_raw = tree.get(f'{PREFIX}/weights-manifest.json')
    same_files = old_raw and (remote_manifest(work, tip, tree) or {}).get('files') == manifest['files']
    if not need and not stale and same_files:
        say('模型倉庫已是最新：沒有新分片、沒有要刪除的分片。')
        return 0
    index = a.state / 'models.index'
    env = dict(GIT_ENV, GIT_INDEX_FILE=str(index))
    index.unlink(missing_ok=True)
    if tip:
        git(work, 'read-tree', tip, env=env)
    parent, batch, batch_bytes, done = tip, 0, 0, 0
    total_new = sum(1 for _, _, n in need if n)
    for p, x, new in need:
        with p['file'].open('rb') as f:
            f.seek(x['offset'])
            data = f.read(x['size'])
        if hashlib.sha256(data).hexdigest() != x['sha256']:
            raise SystemExit(f'讀取期間模型檔改變：{p["path"]}')
        oid = git(work, 'hash-object', '-w', '--stdin', data=data) if new else x['blob']
        assert oid == x['blob']
        git(work, 'update-index', '--add', '--cacheinfo', f'100644,{oid},{PREFIX}/{x["path"]}', env=env)
        if new:
            batch += 1; batch_bytes += x['size']; done += 1
        if new and batch_bytes >= a.batch_mib*1024*1024:
            say(f'  上傳分片批次 {done}/{total_new}…')
            parent = commit_and_push(work, parent, index, f'MacGyver models: upload chunks {done}/{total_new}', a.branch)
            batch, batch_bytes = 0, 0
    # Final commit: manifest + removal of chunks no longer referenced (same transaction).
    mid = git(work, 'hash-object', '-w', '--stdin', data=raw_manifest)
    git(work, 'update-index', '--add', '--cacheinfo', f'100644,{mid},{PREFIX}/weights-manifest.json', env=env)
    for path in stale:
        git(work, 'update-index', '--force-remove', path, env=env)
    if a.prune_legacy_root:
        legacy = sorted(k for k in tree if k == 'weights-manifest.json' or k.startswith('parts/'))
        for path in legacy:
            git(work, 'update-index', '--force-remove', path, env=env)
        say(f'  移除 V12 舊版根目錄權重 {len(legacy)} 個檔案（--prune-legacy-root）')
    commit_and_push(work, parent, index, a.message, a.branch)
    reuse = sum(1 for _, _, n in need if not n)
    say(f'完成：新上傳 {total_new} 片、引用既有內容 {reuse} 片、刪除 {len(stale)} 片；清單 {PREFIX}/weights-manifest.json。')
    return 0


def cmd_restore(a) -> int:
    work, tip, tree = open_remote(a.repo, a.branch, a.state)
    doc = remote_manifest(work, tip, tree)
    if not doc or doc.get('schema') != 1:
        raise SystemExit(f'雲端沒有 {PREFIX}/weights-manifest.json。')
    dest = a.to.expanduser().resolve(); dest.mkdir(parents=True, exist_ok=True)
    for item in doc['files']:
        rel = Path(item['path'])
        if rel.is_absolute() or '..' in rel.parts:
            raise SystemExit('清單路徑不安全：' + item['path'])
        target = dest / rel
        if not target.resolve().is_relative_to(dest):raise SystemExit('Restore target escapes destination')
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists() and target.stat().st_size == item['size'] and sha256_file(target) == item['sha256']:
            say(f'已驗證：{rel}'); continue
        whole = hashlib.sha256()
        with tempfile.NamedTemporaryFile(dir=target.parent, prefix='.restoring-', delete=False) as tmp:
            temporary = Path(tmp.name)
            try:
                for part in item['parts']:
                    full = f'{PREFIX}/{part["path"]}'
                    if not re.fullmatch(r'parts/[0-9a-f]{2}/[0-9a-f]{64}\.part', part['path']) or full not in tree:
                        raise SystemExit('雲端缺少分片：' + full)
                    data = subprocess.run(['git', '-C', str(work), 'cat-file', 'blob', tree[full]], capture_output=True, check=True, env=GIT_ENV).stdout
                    if len(data) != part['size'] or hashlib.sha256(data).hexdigest() != part['sha256']:
                        raise SystemExit('分片雜湊不符：' + full)
                    tmp.write(data); whole.update(data)
            except BaseException:
                temporary.unlink(missing_ok=True); raise
        if temporary.stat().st_size != item['size'] or whole.hexdigest() != item['sha256']:
            temporary.unlink(); raise SystemExit('整檔 SHA-256 不符：' + item['path'])
        os.replace(temporary, target)
        say(f'已還原並驗證：{rel}')
    return 0


def cmd_import_huatuo(a) -> int:
    """Rebuild Qwen3-0.6B-Q8_0.gguf (identical to MacGyver's qwen3-06b) from HuaTuo assets."""
    model = next(m for m in manifest_models() if m['id'] == 'qwen3-06b')
    dest = a.to.resolve() / model['file']
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.stat().st_size == model['bytes'] and sha256_file(dest) == model['sha256']:
        say(f'已有驗證過的 {model["file"]}，不需匯入。'); return 0
    roots = [Path(s).expanduser() for s in a.search] or [ROOT.parent, Path.home() / 'Downloads', Path.home()]
    # 1) a restored HuaTuo GGUF
    for r in roots:
        for cand in [r / model['file'], r / 'models' / model['file'], *r.glob(f'*/models/{model["file"]}')]:
            if cand.is_file() and not cand.is_symlink() and cand.stat().st_size == model['bytes'] and sha256_file(cand) == model['sha256']:
                tmp = dest.with_suffix('.importing'); shutil.copyfile(cand, tmp); os.replace(tmp, dest)
                say(f'已從 {cand} 複製並驗證 {model["file"]}。'); return 0
    # 2) the four HuaTuo model ZIPs
    zips = []
    for r in roots:
        zips = sorted(r.glob('HuaTuo_v2_Qwen3_CPU_part[1-4]of4.zip'))
        if len(zips) == 4:
            break
    if len(zips) != 4:
        say('找不到華佗模型 ZIP（HuaTuo_v2_Qwen3_CPU_part1of4.zip～part4of4.zip）或已還原的 GGUF；改由官方來源下載。')
        return 2
    pieces, manifest = {}, None
    for z in zips:
        with zipfile.ZipFile(z) as archive:
            for info in archive.infolist():
                name = Path(info.filename).name
                if info.is_dir() or info.flag_bits & 0x1 or '..' in Path(info.filename).parts:
                    continue
                if name == 'manifest.json' and info.file_size < 200_000:
                    doc = json.loads(archive.read(info))
                    if doc.get('sha256') == model['sha256']:
                        manifest = doc
                elif re.fullmatch(re.escape(model['file']) + r'\.piece-\d{4}', name) and info.file_size <= 80 * 1024 * 1024:
                    pieces[name] = (z, info.filename, info.file_size)
    if not manifest:
        raise SystemExit('華佗 ZIP 中沒有與官方模型相符的分片清單。')
    tmp = dest.with_suffix('.importing'); whole = hashlib.sha256(); total = 0
    try:
        with tmp.open('wb') as out:
            for part in manifest['parts']:
                entry = pieces.get(part['filename'])
                if not entry or entry[2] != part['bytes']:
                    raise SystemExit('缺少或大小不符的分片：' + part['filename'])
                with zipfile.ZipFile(entry[0]) as archive:
                    data = archive.read(entry[1])
                if hashlib.sha256(data).hexdigest() != part['sha256']:
                    raise SystemExit('分片雜湊不符：' + part['filename'])
                out.write(data); whole.update(data); total += len(data)
        if total != model['bytes'] or whole.hexdigest() != model['sha256']:
            raise SystemExit('整檔 SHA-256 不符，未匯入。')
        os.replace(tmp, dest)
    finally:
        tmp.unlink(missing_ok=True)
    say(f'已由華佗 ZIP 還原並驗證 {model["file"]}（{model["bytes"] / 1024**2:,.0f} MiB），不必重新下載。')
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    for name in ('compare', 'push', 'restore'):
        s = sub.add_parser(name)
        s.add_argument('--repo', default='git@github.com:kuonanhong/PRIVATE-MODELS.git')
        s.add_argument('--branch', default='main')
        s.add_argument('--state', type=Path, default=ROOT.parent / 'MacGyver_GitHub_Sync_State')
        if name in ('compare', 'push'):
            s.add_argument('--models-dir', type=Path, default=ROOT / 'models')
        if name == 'compare':
            s.add_argument('--json-report', type=Path)
        if name == 'push':
            s.add_argument('--batch-mib',type=int,default=120,choices=range(40,1025),metavar='40..1024')
            s.add_argument('--private-confirmed', action='store_true')
            s.add_argument('--prune-legacy-root', action='store_true', help='also remove V12 root-level parts/ and weights-manifest.json')
            s.add_argument('--message', default='MacGyver Academy V13 model manifest')
        if name == 'restore':
            s.add_argument('--to', type=Path, required=True)
    s = sub.add_parser('import-huatuo')
    s.add_argument('--search', action='append', default=[], help='folder holding the HuaTuo ZIPs or HuaTuo package (repeatable)')
    s.add_argument('--to', type=Path, default=ROOT / 'models')
    a = ap.parse_args()
    if hasattr(a,'branch') and subprocess.run(['git','check-ref-format','--branch',a.branch],capture_output=True).returncode:ap.error('Invalid Git branch')
    if hasattr(a, 'state'):
        a.state = a.state.expanduser().resolve()
        if a.state == ROOT or ROOT in a.state.parents or a.state in ROOT.parents:
            raise SystemExit('--state 必須在專案資料夾之外。')
    return {'compare': cmd_compare, 'push': cmd_push, 'restore': cmd_restore, 'import-huatuo': cmd_import_huatuo}[a.cmd](a)


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (RuntimeError, subprocess.CalledProcessError) as e:
        print('停止：', e, file=sys.stderr)
        sys.exit(1)
