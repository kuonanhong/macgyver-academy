#!/usr/bin/env python3
"""Validate the actual public Pages output before uploading it (Python 3.10+)."""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import stat
import sys

# Keep room beneath GitHub's documented 1 GB published-site limit.
DEFAULT_MAX_BYTES = 900_000_000
BLOCKED = {'.git', 'node_modules', 'models', 'local-documents', 'portable',
           'owner-private', 'credentials', 'secrets', 'uploads', 'userdata',
           'user-data', 'accounts', 'auth', 'owner-courses', 'owner-resources'}
SUFFIXES = {'.pem', '.key', '.p12', '.pfx', '.sqlite', '.sqlite3', '.db',
            '.gguf', '.safetensors', '.ckpt', '.pt', '.pth', '.onnx', '.bin',
            '.pyc', '.h5', '.hdf5', '.pb', '.npy', '.npz', '.pkl', '.pickle', '.keras'}
ALLOWED_HIDDEN = {'.nojekyll', '.macgyver-static-export'}


def inspect(root: Path, max_bytes=DEFAULT_MAX_BYTES):
    if root.is_symlink() or not root.is_dir():
        raise ValueError('Pages 輸出必須是實際資料夾。')
    root = root.resolve()
    for name in ('index.html', '.nojekyll', 'preview-manifest.json'):
        path = root / name
        if path.is_symlink() or not path.is_file():
            raise ValueError('Pages 缺少入口或匯出清單：' + name)
    manifest = json.loads((root / 'preview-manifest.json').read_text('utf-8'))
    if manifest.get('mode') != 'first-stage-preview' or manifest.get('memberBodies') != 0:
        raise ValueError('Pages 必須使用已檢查的公開首階段匯出。')
    files, directories, total, padded = [], 0, 0, 0
    for path in root.rglob('*'):
        relative = path.relative_to(root)
        info = path.lstat()
        if stat.S_ISLNK(info.st_mode):
            raise ValueError('Pages 不接受符號連結：' + relative.as_posix())
        lowered = {part.casefold() for part in relative.parts}
        if BLOCKED.intersection(lowered) or any(
                part.startswith('.') and part not in ALLOWED_HIDDEN for part in relative.parts):
            raise ValueError('公開輸出含私人、來源或隱藏目錄：' + relative.as_posix())
        if stat.S_ISDIR(info.st_mode):
            directories += 1
            continue
        if not stat.S_ISREG(info.st_mode) or info.st_nlink > 1:
            raise ValueError('Pages 不接受特殊檔案或硬連結：' + relative.as_posix())
        if path.suffix.lower() in SUFFIXES or path.name.casefold().startswith('.env'):
            raise ValueError('公開輸出含私人檔案類型：' + relative.as_posix())
        total += info.st_size
        padded += ((info.st_size + 511) // 512) * 512
        files.append((info.st_size, relative.as_posix()))
    # Include generously bounded PAX path/metadata headers, directory entries,
    # end markers and record padding. This is a conservative bound, not an
    # assertion of the eventual ZIP compression ratio.
    tar_upper_bound = padded + (len(files) + directories + 1) * 2048 + 10240
    report = {
        'status': 'PASS', 'files': len(files), 'directories': directories,
        'uncompressedBytes': total, 'tarUpperBoundBytes': tar_upper_bound,
        'budgetBytes': max_bytes, 'officialPublishedSiteLimitBytes': 1_000_000_000,
        'mode': manifest['mode'], 'httpOnly': manifest.get('httpOnly', False),
        'largestFiles': [{'path': name, 'bytes': size} for size, name in sorted(files, reverse=True)[:10]],
        'warnings': (['檔案超過 25,000 個；此為本專案效能提醒，並非 GitHub 公告的檔數上限。']
                     if len(files) > 25000 else []),
    }
    if total >= max_bytes or tar_upper_bound >= max_bytes:
        raise ValueError('Pages 輸出超過保守容量預算：檔案 %d bytes，tar 上界 %d bytes，預算 %d bytes；請先縮小公開輸出。'
                         % (total, tar_upper_bound, max_bytes))
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path, nargs='?', default=Path('github-pages'))
    parser.add_argument('--max-bytes', type=int, default=DEFAULT_MAX_BYTES)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    if not 1 <= args.max_bytes <= DEFAULT_MAX_BYTES:
        parser.error('--max-bytes 必須介於 1 與 900000000，不能繞過容量保護。')
    try:
        result = inspect(args.directory, args.max_bytes)
        encoded = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
        print(encoded, end='')
        if args.report:
            args.report.write_text(encoded, encoding='utf-8')
        summary = os.environ.get('GITHUB_STEP_SUMMARY')
        if summary:
            with open(summary, 'a', encoding='utf-8') as stream:
                stream.write('Pages 公開輸出驗證通過：%d 檔、%.1f MB；tar 保守上界 %.1f MB。\n'
                             % (result['files'], result['uncompressedBytes']/1e6, result['tarUpperBoundBytes']/1e6))
        return 0
    except (OSError, ValueError, TypeError) as error:
        print('Pages 預檢停止：' + str(error), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
