#!/usr/bin/env python3
"""Produce a reviewed GitHub snapshot without reusing private Git history."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

DIRECTORIES = {'app', 'build', 'components', 'db', 'docs', 'drizzle', 'examples', 'hooks', 'lib', 'portable', 'public', 'scripts', 'supabase', 'tests', 'tools', 'vendor'}
ROOT_FILES = {'.env.example', '.gitignore', '.npmrc', 'README.md', 'SOURCE_VERSION.json', 'SHA256SUMS', 'SHA256SUMS.txt', 'cloudflare-env.d.ts', 'components.json', 'drizzle.config.ts', 'eslint.config.mjs', 'index.html', 'next.config.ts', 'package.json', 'pnpm-lock.yaml', 'pnpm-workspace.yaml', 'postcss.config.mjs', 'requirements-documents.txt', 'tsconfig.json', 'vite.config.ts'}
BLOCK_DIRS = {'.git', '.next', '.vinext', '.sites-runtime', '.wrangler', '.agents', '.codex', 'node_modules', '__pycache__', 'local-documents', 'credentials', 'secrets', 'userdata', 'user-data', 'uploads', 'coverage'}
BLOCK_SUFFIXES = {'.pem', '.key', '.p12', '.pfx', '.sqlite', '.sqlite3', '.db', '.gguf', '.safetensors', '.ckpt', '.pt', '.pth', '.onnx', '.bin', '.pyc'}
# Token prefixes start at a boundary: official publication slugs containing
# "task-..." must not be mistaken for an API key starting inside that word.
SECRETS = re.compile(rb'(?:github_pat_[A-Za-z0-9_]{30,}|gh[pousr]_[A-Za-z0-9_]{30,}|(?<![A-Za-z0-9_])sk-(?:proj-)?[A-Za-z0-9_-]{40,}|-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----)')
MARKER = '.macgyver-github-export.json'
SIZE_LIMIT = 100 * 1024 * 1024
# The full downloadable snapshot includes this materialized teaching dataset.
# Git keeps the validated parts and reconstructs it during build/server startup.
GENERATED_FOR_GIT = {'public/academy/data/featured.json'}
EXTRA_IGNORE = '\n# GitHub snapshot: never commit device/account data or weights.\n.macgyver-github-export.json\nmodels/*\n!models/README.md\n**/local-documents/\n**/credentials/\n**/secrets/\n**/user-data/\n**/userdata/\n**/uploads/\n*.gguf\n*.safetensors\n*.ckpt\n*.pt\n*.pth\n*.onnx\n*.bin\n*.key\n*.p12\n*.pfx\n*.db\n'


def fail(message):
    raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def valid_repo(value):
    if not re.fullmatch(r'(?:https://github\.com/|git@github\.com:)[A-Za-z0-9][A-Za-z0-9_.-]*/[A-Za-z0-9][A-Za-z0-9_.-]*(?:\.git)?', value):
        fail('請使用不含 token、密碼、查詢參數的 GitHub HTTPS 或 SSH 網址。')
    return value


def candidate(relative):
    parts = relative.parts
    if any(part in BLOCK_DIRS for part in parts) or parts[:2] == ('portable', 'data'):
        return False
    if any(part.startswith('.env') and part != '.env.example' for part in parts):
        return False
    if relative.name in {'id_rsa', 'id_ed25519', '.DS_Store', '.netrc', '.git-credentials'}:
        return False
    if relative.suffix.lower() in BLOCK_SUFFIXES or '.sqlite' in relative.name or relative.name.endswith('.tsbuildinfo'):
        return False
    if len(parts) == 1:
        return relative.name in ROOT_FILES or relative.suffix.lower() in {'.sh', '.bat', '.ps1', '.command'}
    if parts[0] in DIRECTORIES:
        return True
    if str(relative.as_posix()) in {'.github/workflows/pages.yml', '.openai/hosting.json', 'models/README.md', 'public-player/README_ZH.md'}:
        return True
    return parts[:2] == ('public-player', 'dist')


def snapshot(source):
    result = {}
    ignored = []
    for folder, directories, files in os.walk(source, followlinks=False):
        parent = Path(folder)
        directories[:] = sorted(d for d in directories if d not in BLOCK_DIRS and not (parent / d).is_symlink() and not (parent == source and d not in DIRECTORIES | {'.github', '.openai', 'models', 'public-player'}))
        for name in sorted(files):
            path = parent / name
            relative = path.relative_to(source)
            if not candidate(relative):
                ignored.append(relative.as_posix())
                continue
            if path.is_symlink():
                fail('拒絕符號連結，請改成實際公開檔案：' + relative.as_posix())
            if path.stat().st_size >= SIZE_LIMIT:
                fail('檔案達 100 MiB，請另用 LFS / 物件儲存：' + relative.as_posix())
            data = path.read_bytes()
            if SECRETS.search(data):
                fail('疑似憑證內容，停止匯出（不顯示秘密）：' + relative.as_posix())
            if relative.as_posix() == '.openai/hosting.json':
                config = json.loads(data)
                config.pop('project_id', None)
                data = (json.dumps(config, ensure_ascii=False, indent=2) + '\n').encode()
            if relative.as_posix() == '.gitignore':
                data += EXTRA_IGNORE.encode()
            result[relative.as_posix()] = data
    required = {'index.html', 'public/academy/index.html', 'public/academy/app.bundle.js', '.github/workflows/pages.yml', 'publish-github.sh'}
    if required - result.keys():
        fail('缺少必要檔案：' + ', '.join(sorted(required - result.keys())))
    for checksum_name in ('SHA256SUMS','SHA256SUMS.txt'):
        if checksum_name in result:
            result[checksum_name] = ''.join(f'{digest(data)}  {name}\n' for name, data in sorted(result.items()) if name not in {'SHA256SUMS','SHA256SUMS.txt'}).encode()
    return result, ignored


def read_export(output, source, repo):
    if output == source or output in source.parents or source in output.parents:
        fail('匯出資料夾必須在來源專案之外，不能是來源、其子目錄或上層。')
    if not output.exists():
        return {}
    if output.is_symlink() or not output.is_dir() or not (output / MARKER).is_file():
        fail('目的地已存在且不是本工具建立；請改用新的 --out 資料夾。')
    old = json.loads((output / MARKER).read_text('utf-8'))
    if old.get('version') != 1 or old.get('repo') != repo:
        fail('目的地的版本或 GitHub 倉庫不同；請改用新的 --out 資料夾。')
    files = old.get('files', {})
    if not isinstance(files, dict):
        fail('匯出清單損壞。')
    for name, expected in files.items():
        relative = Path(name)
        if relative.is_absolute() or '..' in relative.parts or not candidate(relative):
            fail('匯出清單含有不允許的路徑。')
        path = output / relative
        if path.is_symlink() or not path.is_file() or digest(path.read_bytes()) != expected:
            fail('匯出目錄有手動修改，為避免覆寫請先備份，再用新目錄：' + name)
    for folder, directories, names in os.walk(output, followlinks=False):
        directories[:] = [d for d in directories if not (Path(folder) == output and d == '.git')]
        for d in directories:
            if (Path(folder) / d).is_symlink():
                fail('匯出目錄包含符號連結。')
        for name in names:
            rel = (Path(folder) / name).relative_to(output).as_posix()
            if rel != MARKER and rel not in files:
                fail('匯出目錄有額外檔案，請先移出或使用新目錄：' + rel)
    if (output / '.git').exists():
        if not (output / '.git').is_dir() or (output / '.git').is_symlink():
            fail('只接受本工具建立的獨立 Git 目錄。')
        remotes = git(output, 'remote', capture=True).splitlines()
        if remotes != ['origin'] or git(output, 'remote', 'get-url', 'origin', capture=True) != repo:
            fail('匯出目錄的 origin 不符合指定網址；不修改任何既有 remote。')
    return files


def write_export(source, output, repo, files, old):
    output.mkdir(parents=True, exist_ok=True)
    for name, data in files.items():
        path = output / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        path.chmod((source / name).stat().st_mode & 0o777)
    # Only remove previously generated, unchanged files absent from this snapshot.
    for name in set(old) - files.keys():
        (output / name).unlink()
    marker = {'version': 1, 'repo': repo, 'files': {k: digest(v) for k, v in files.items()}}
    (output / MARKER).write_text(json.dumps(marker, ensure_ascii=False, indent=2) + '\n', 'utf-8')


def git(directory, *args, capture=False, check=True):
    result = subprocess.run(['git', '-C', str(directory), *args], check=check, text=True,
                            stdout=subprocess.PIPE if capture else None, stderr=subprocess.PIPE if capture else None)
    return result.stdout.rstrip('\r\n') if capture else result.returncode


def push(output, repo, branch, message, files):
    if not shutil.which('git'):
        fail('請先安裝 Git。')
    git(output, 'check-ref-format', '--branch', branch, capture=True)
    if not (output / '.git').exists():
        git(output, 'init')
        git(output, 'symbolic-ref', 'HEAD', 'refs/heads/' + branch)
        git(output, 'remote', 'add', 'origin', repo)
    else:
        if git(output, 'symbolic-ref', '--short', 'HEAD', capture=True) != branch:
            fail('匯出倉庫目前分支不同，請使用原分支或另選新目錄。')
    for key in ('user.name', 'user.email'):
        try:
            value = git(output, 'config', key, capture=True)
        except subprocess.CalledProcessError:
            value = ''
        if not value:
            fail('請先設定 git config --global ' + key + '，再重跑 --push。')
    # Only explicit snapshot paths can enter the index; never git add . / -A.
    tracked = git(output, 'ls-files', '-z', capture=True).split('\0')
    removed = [name for name in tracked if name and (name not in files or name in GENERATED_FOR_GIT)]
    if removed:
        git(output, 'rm', '--cached', '--', *removed)
    paths = sorted(set(files) - GENERATED_FOR_GIT)
    for start in range(0, len(paths), 50):
        git(output, 'add', '--', *paths[start:start + 50])
    if git(output, 'diff', '--cached', '--quiet', check=False) != 0:
        git(output, 'commit', '-m', message)
    # Fetch only if the branch exists. Authentication/network failures stop here.
    remote_heads = git(output, 'ls-remote', '--heads', 'origin', 'refs/heads/' + branch, capture=True)
    if remote_heads:
        git(output, 'fetch', '--no-tags', 'origin', branch)
        if git(output, 'merge-base', '--is-ancestor', 'FETCH_HEAD', 'HEAD', check=False) != 0:
            fail('遠端有不同歷史或新提交；已保留本地提交，沒有強推。請查看文件的「遠端已有檔案」。')
    git(output, 'push', '--set-upstream', 'origin', 'HEAD:refs/heads/' + branch)


def main():
    parser = argparse.ArgumentParser(description='匯出完整公開原始碼到獨立資料夾；預設只預覽。')
    parser.add_argument('--source', type=Path, default=Path(__file__).resolve().parents[1], help=argparse.SUPPRESS)
    parser.add_argument('--repo', required=True, help='https://github.com/OWNER/REPO.git')
    parser.add_argument('--out', type=Path, help='專案外的獨立輸出資料夾')
    parser.add_argument('--branch', default='main')
    parser.add_argument('--message', default='Update MacGyver Engineering Academy')
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument('--dry-run', action='store_true', help='只列出公開檔案，不改檔、不連線（預設）')
    modes.add_argument('--export', action='store_true', help='更新離線套件並匯出；不 git push')
    modes.add_argument('--push', action='store_true', help='匯出、提交並推送指定 GitHub 倉庫；不發布 Pages')
    args = parser.parse_args()
    source = args.source.resolve()
    output = (args.out or source.with_name(source.name + '-github')).resolve()
    repo = valid_repo(args.repo)
    old = read_export(output, source, repo)
    # Inspect before even rebuilding so accidentally pasted credentials fail early.
    files, ignored = snapshot(source)
    if args.export or args.push:
        subprocess.run(['bash', (source / 'build-offline.sh').as_posix(), '--if-needed'], check=True)
        files, ignored = snapshot(source)
        write_export(source, output, repo, files, old)
    for name in sorted(files):
        print(f'{len(files[name]):>10}  {name}')
    print(f'\n公開原始碼：{len(files)} 個檔案，{sum(map(len, files.values())) / 1024 / 1024:.1f} MiB')
    print('目的地：' + str(output))
    print('倉庫：' + repo)
    print('排除：既有 Git 歷史、私有教材、帳號資料庫、憑證、模型權重、node_modules、建置快取。')
    if args.push:
        push(output, repo, args.branch, args.message, files)
        print('GitHub 程式已上傳。Pages 網站需在 GitHub 另外啟用並手動執行工作流程。')
    elif args.export:
        print('匯出完成；尚未上傳或發布。確認清單後使用相同參數加 --push。')
    else:
        print('DRY RUN：未修改檔案、未建立 Git 倉庫、未連線或上傳。')


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, subprocess.CalledProcessError, json.JSONDecodeError) as error:
        print('停止：' + str(error), file=sys.stderr)
        sys.exit(1)
