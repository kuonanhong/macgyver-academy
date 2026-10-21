#!/usr/bin/env python3
"""Verify two clean offline rebuilds recover canonical lessons from bounded parts.

Uses isolated temporary directories; never removes or modifies release sources.
"""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / 'public/academy'


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def main():
    expected = json.loads((PUBLIC / 'offline-build.json').read_text())
    canonical = sha(PUBLIC / 'data/featured.json')
    reports = []
    for iteration in range(1, 3):
        with tempfile.TemporaryDirectory(prefix='macgyver-v14-rebuild-') as directory:
            temp = Path(directory)
            (temp / 'tools').mkdir()
            for name in ('build-offline.mjs', 'restore-featured.mjs'):
                shutil.copy2(ROOT / 'tools' / name, temp / 'tools' / name)
            destination = temp / 'public/academy'
            (destination / 'data').mkdir(parents=True)
            for p in PUBLIC.iterdir():
                if p.is_file() and p.suffix in ('.js', '.css', '.html') and p.name not in ('app.bundle.js', 'offline-data.js') and not p.name.startswith('offline-data-'):
                    shutil.copy2(p, destination / p.name)
            for p in (PUBLIC / 'data').glob('*.json'):
                if p.name != 'featured.json':
                    shutil.copy2(p, destination / 'data' / p.name)
            shutil.copytree(PUBLIC / 'data/course-parts', destination / 'data/course-parts')
            assert not (destination / 'data/featured.json').exists()
            subprocess.run(['node', 'tools/build-offline.mjs'], cwd=temp, check=True, capture_output=True, text=True)
            restored = sha(destination / 'data/featured.json')
            assert restored == canonical, 'Restored canonical curriculum differs'
            actual = json.loads((destination / 'offline-build.json').read_text())
            assert actual == expected, 'Offline manifest differs after a clean rebuild'
            for name, digest in expected['outputs'].items():
                assert sha(temp / name) == digest, 'Generated output differs: ' + name
            subprocess.run(['node', 'tools/build-offline.mjs', '--check'], cwd=temp, check=True, capture_output=True, text=True)
            reports.append({'iteration': iteration, 'canonicalSHA256': restored, 'verifiedOutputs': len(expected['outputs'])})
    print(json.dumps({'status': 'PASS', 'scope': 'Two isolated builds with featured.json and all generated offline/lazy output initially absent; recovered from checked bounded parts.', 'builds': reports}, indent=2))


if __name__ == '__main__':
    main()
