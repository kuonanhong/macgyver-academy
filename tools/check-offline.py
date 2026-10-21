#!/usr/bin/env python3
"""Check prebuilt offline assets without requiring Node on an end-user machine."""
import hashlib
import json
import re
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root))
from portable.curriculum_parts import ensure_featured
public = root / 'public' / 'academy'
try:
    ensure_featured(public)
    manifest = json.loads((public / 'offline-build.json').read_text(encoding='utf-8'))
    sources = [root / 'tools' / 'build-offline.mjs', root / 'tools' / 'restore-featured.mjs']
    sources += [p for p in public.iterdir() if p.suffix in ('.js', '.css', '.html') and p.name not in ('app.bundle.js', 'offline-data.js') and not re.fullmatch(r'offline-data-\d+\.js', p.name)]
    sources += [p for p in (public / 'data').glob('*.json') if p.name not in ('markets.json', 'fx.json')]
    expected = {p.relative_to(root).as_posix() for p in sources}
    assert manifest['version'] == 1 and manifest.get('lazyVersion') == 1 and expected == set(manifest['inputs'])
    for group in ('inputs', 'outputs'):
        for name, digest in manifest[group].items():
            file = (root / name).resolve()
            assert file.is_relative_to(root)
            assert hashlib.sha256(file.read_bytes()).hexdigest() == digest
except (OSError, ValueError, KeyError, TypeError, AssertionError):
    raise SystemExit(1)
print('離線套件與目前程式和教材相符 / Offline bundle is current.')
