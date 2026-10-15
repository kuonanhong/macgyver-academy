#!/usr/bin/env python3
"""Compare this package with the GitHub repository and upload only differences.

How the comparison works (also explained in docs/UPLOAD_SYNC_V12_ZH.md):
  1. Build the reviewed public snapshot of this package (same rules as
     tools/export_github.py: no weights, credentials, accounts or private docs).
  2. Shallow-clone / fetch the GitHub branch into a private state folder.
  3. For every file compute Git's own blob id  sha1("blob <size>\\0" + bytes)
     and compare it with `git ls-tree` of the remote branch:
        added    = in the package, not on GitHub
        modified = on both, different blob id
        deleted  = on GitHub, no longer in the package (stale scripts/data)
        same     = identical, never re-uploaded
  4. --push writes only added/modified files, removes deleted ones, makes one
     commit and pushes it. Git transfers only the new objects.

Usage:
  python3 tools/sync-v12/sync_github.py --repo git@github.com:kuonanhong/macgyver-academy.git            # compare only
  python3 tools/sync-v12/sync_github.py --repo ... --push --message "V12 update"
  python3 tools/sync-v12/sync_github.py --repo ... --only public/academy/data/markets.json --push   # weekly data
  python3 tools/sync-v12/sync_github.py --repo ... --site-only --protect-content --push   # static site, paid stages stubbed
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('export_github', ROOT / 'tools/export_github.py')
export_github = importlib.util.module_from_spec(spec)
spec.loader.exec_module(export_github)

KEEP_REMOTE = {'CNAME', '.nojekyll', 'LICENSE', 'LICENSE.md'}


def blob_id(data: bytes) -> str:
    return hashlib.sha1(b'blob %d\0' % len(data) + data).hexdigest()


def git(cwd: Path, *args: str, capture: bool = True, check: bool = True) -> str:
    r = subprocess.run(['git', '-C', str(cwd), *args], text=True, check=check,
                       stdout=subprocess.PIPE if capture else None, stderr=subprocess.PIPE if capture else None)
    return (r.stdout or '').rstrip('\n')


def site_only(files: dict[str, bytes]) -> dict[str, bytes]:
    """Static website only (repo root redirect + public/academy)."""
    out = {k: v for k, v in files.items() if k.startswith('public/academy/') or k in ('index.html', '.nojekyll', '.gitignore', 'README.md', 'tools/markets-v12/update_markets.py', '.github/workflows/weekly-markets.yml')}
    out.setdefault('.nojekyll', b'')
    return out


def stub_paid_stages(files: dict[str, bytes], free_stages: int = 1) -> dict[str, bytes]:
    """Remove paid-stage content from every public curriculum copy and rebuild
    course-parts. Paid content must already be uploaded to Supabase
    (tools/paywall-v12/upload_protected_content.py)."""
    featured = json.loads((ROOT / 'public/academy/data/featured.json').read_text('utf-8'))
    def stub(course):
        stages = course.get('stages', [])
        keep = stages[:free_stages]
        rest = [{'id': st['id'], 'order': st.get('order'), 'title': st.get('title'), 'titleEn': st.get('titleEn'),
                 'steps': [{'id': s['id'], 'order': s.get('order'), 'sequence': s.get('sequence'), 'title': s.get('title'),
                            'titleEn': s.get('titleEn'), 'locked': True, 'prerequisiteIds': s.get('prerequisiteIds', []),
                            'sourceIds': s.get('sourceIds', []), 'knowledge': [],
                            'quiz': {'question': '', 'questionEn': '', 'options': ['', '', ''], 'optionsEn': ['', '', ''], 'answer': 0}}
                           for s in st.get('steps', [])]} for st in stages[free_stages:]]
        return {**course, 'stages': keep + rest, 'publicStub': True}
    courses = [stub(c) for c in featured]
    out = {k: v for k, v in files.items() if not k.startswith('public/academy/data/course-parts/')
           and not (k.startswith('public/academy/offline-data') and k.endswith('.js'))
           and not (k.startswith('tools/') and k != 'tools/markets-v12/update_markets.py')}
    # Rebuild bounded parts exactly like tools/build-offline.mjs.
    parts, batch, size = [], [], 0
    for c in courses:
        n = len(json.dumps(c, ensure_ascii=False, separators=(',', ':')).encode())
        if batch and size + n + len(batch) + 512 > 7 * 1024 * 1024:
            parts.append(batch); batch, size = [], 0
        batch.append(c); size += n
    if batch:
        parts.append(batch)
    index = {'schemaVersion': 1, 'dataSet': 'featured', 'courseCount': len(courses), 'parts': []}
    for i, group in enumerate(parts, 1):
        raw = json.dumps(group, ensure_ascii=False, separators=(',', ':')).encode()
        digest = hashlib.sha256(raw).hexdigest()
        name = f'part-{i:04d}-{digest[:16]}.json'
        out[f'public/academy/data/course-parts/{name}'] = raw
        index['parts'].append({'file': name, 'byteLength': len(raw), 'sha256': digest, 'courseCount': len(group), 'courseIds': [c['id'] for c in group]})
    out['public/academy/data/course-parts/index.json'] = (json.dumps(index, ensure_ascii=False, indent=2) + '\n').encode()
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--repo', required=True)
    ap.add_argument('--branch', default='main')
    ap.add_argument('--state', type=Path, default=ROOT.parent / 'MacGyver_GitHub_Sync_State')
    ap.add_argument('--push', action='store_true', help='upload the differences (default: compare only)')
    ap.add_argument('--message', default='Update MacGyver Engineering Academy (V12 sync)')
    ap.add_argument('--only', action='append', default=[], help='limit to these paths (repeatable)')
    ap.add_argument('--site-only', action='store_true', help='publish only the static website files')
    ap.add_argument('--protect-content', action='store_true', help='stub paid stages (requires Supabase content upload)')
    ap.add_argument('--no-delete', action='store_true', help='never delete remote files')
    ap.add_argument('--report', type=Path, help='write the comparison report (JSON) here')
    a = ap.parse_args()
    repo = export_github.valid_repo(a.repo)
    state = a.state.resolve()
    if state == ROOT or ROOT in state.parents or state in ROOT.parents:
        sys.exit('state folder must be outside the project')
    files, _ = export_github.snapshot(ROOT)
    files = {k: v for k, v in files.items() if k not in export_github.GENERATED_FOR_GIT}
    if a.site_only:
        files = site_only(files)
    if a.protect_content:
        files = stub_paid_stages(files)
    work = state / 'site'
    state.mkdir(parents=True, exist_ok=True)
    if (work / '.git').is_dir():
        if git(work, 'remote', 'get-url', 'origin') != repo:
            sys.exit(f'{work} points to another repository; use --state with a new folder')
        git(work, 'fetch', '--depth', '1', '--no-tags', 'origin', a.branch, capture=False)
        git(work, 'reset', '--hard', 'FETCH_HEAD')
        git(work, 'clean', '-fdq')
    else:
        if work.exists():
            shutil.rmtree(work)
        heads = subprocess.run(['git', 'ls-remote', '--heads', repo, a.branch], text=True, capture_output=True)
        if heads.returncode != 0:
            sys.exit('cannot reach the repository (check SSH key / network):\n' + heads.stderr[-800:])
        if heads.stdout.strip():
            subprocess.run(['git', 'clone', '--depth', '1', '--branch', a.branch, '--no-tags', repo, str(work)], check=True)
        else:
            work.mkdir(parents=True)
            git(work, 'init', '-q'); git(work, 'symbolic-ref', 'HEAD', f'refs/heads/{a.branch}'); git(work, 'remote', 'add', 'origin', repo)
    remote = {}
    if git(work, 'rev-parse', '--verify', '-q', 'HEAD', check=False):
        for line in git(work, 'ls-tree', '-r', '--full-tree', 'HEAD').splitlines():
            meta, path = line.split('\t', 1)
            remote[path] = meta.split()[2]
    scope = lambda p: not a.only or any(p == o or p.startswith(o.rstrip('/') + '/') for o in a.only)
    local = {k: v for k, v in files.items() if scope(k)}
    added = sorted(k for k in local if k not in remote)
    modified = sorted(k for k in local if k in remote and remote[k] != blob_id(local[k]))
    deleted = [] if a.no_delete or a.only else sorted(k for k in remote if k not in files and k not in KEEP_REMOTE and scope(k))
    same = len(local) - len(added) - len(modified)
    upload_bytes = sum(len(local[k]) for k in added + modified)
    report = {'repo': repo, 'branch': a.branch, 'added': added, 'modified': modified, 'deleted': deleted,
              'unchanged': same, 'uploadBytes': upload_bytes}
    print(f'比較結果 / comparison  ({repo} @ {a.branch})')
    print(f'  新增 added    : {len(added)}')
    print(f'  修改 modified : {len(modified)}')
    print(f'  刪除 deleted  : {len(deleted)}')
    print(f'  相同 unchanged: {same}（不會重新上傳）')
    print(f'  需上傳資料量  : {upload_bytes / 1024 / 1024:.1f} MiB（git 另行壓縮）')
    for label, items in (('+', added), ('~', modified), ('-', deleted)):
        for k in items[:60]:
            print(f'    {label} {k}')
        if len(items) > 60:
            print(f'    {label} …and {len(items) - 60} more')
    if a.report:
        a.report.write_text(json.dumps(report, ensure_ascii=False, indent=1), 'utf-8')
    (state / 'last-comparison.json').write_text(json.dumps(report, ensure_ascii=False, indent=1), 'utf-8')
    if not a.push:
        print('只比較，未上傳。加上 --push 才會上傳差異。')
        return 0
    if not (added or modified or deleted):
        print('GitHub 已是最新，沒有需要上傳的變更。')
        return 0
    for key in ('user.name', 'user.email'):
        if not git(work, 'config', key, check=False):
            sys.exit(f'請先設定 git config --global {key}')
    for k in added + modified:
        target = work / k
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(local[k])
        src = ROOT / k
        if src.exists() and os.access(src, os.X_OK):
            target.chmod(0o755)
    for k in deleted:
        (work / k).unlink(missing_ok=True)
    paths = added + modified
    for i in range(0, len(paths), 200):
        git(work, 'add', '--', *paths[i:i + 200])
    for i in range(0, len(deleted), 200):
        git(work, 'rm', '-q', '--cached', '--ignore-unmatch', '--', *deleted[i:i + 200])
    git(work, 'commit', '-q', '-m', a.message)
    for attempt in range(1, 4):
        r = subprocess.run(['git', '-C', str(work), 'push', 'origin', f'HEAD:refs/heads/{a.branch}'], text=True)
        if r.returncode == 0:
            print('已上傳差異到 GitHub。')
            return 0
        print(f'push 第 {attempt} 次失敗：雲端可能剛被更新（例如每週 Action），取回最新版本後重試…', file=sys.stderr)
        fetched = subprocess.run(['git', '-C', str(work), 'fetch', '--depth', '50', '--no-tags', 'origin', a.branch], text=True)
        rebased = fetched.returncode == 0 and subprocess.run(['git', '-C', str(work), 'rebase', 'FETCH_HEAD'], text=True).returncode == 0
        if not rebased:
            subprocess.run(['git', '-C', str(work), 'rebase', '--abort'], text=True, stderr=subprocess.DEVNULL)
            print('同一檔案在雲端也被修改（常見於 markets.json / fx.json 已由每週 Action 更新）。請重新執行同一命令，會以雲端最新版重新比對。', file=sys.stderr)
            return 1
    print('上傳未完成：本機提交保留在', work, '；檢查網路或是否有人同時更新遠端，再重跑同一命令。', file=sys.stderr)
    return 1


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (ValueError, subprocess.CalledProcessError) as e:
        print('停止：', e, file=sys.stderr)
        sys.exit(1)
