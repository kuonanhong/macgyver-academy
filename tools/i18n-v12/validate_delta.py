#!/usr/bin/env python3
"""Validate delta dictionaries: python3 -I tools/i18n-v12/validate_delta.py [lang ...]"""
import json, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
args = sys.argv[1:]
SET = 'delta'
if args[:1] == ['--set']:
    SET, args = args[1], args[2:]
DIR = ROOT / 'tools/i18n-v12' / SET
KEYS = json.loads((DIR / 'keys.json').read_text('utf-8'))
def check(lang):
    p = DIR / f'{lang}.json'
    if not p.exists(): return [f'{lang}: missing file']
    d = json.loads(p.read_text('utf-8')); s = d.get('strings', {}); out = []
    if d.get('lang') != lang: out.append('lang field mismatch')
    miss = [k for k in KEYS if not isinstance(s.get(k), str) or not s[k].strip()]
    if miss: out.append(f'{len(miss)} missing, e.g. {miss[:2]}')
    for k, val in s.items():
        if k not in KEYS: out.append(f'unknown key {k[:40]!r}'); continue
        if k.count('{n}') != val.count('{n}'): out.append(f'placeholder mismatch {k[:40]!r}')
        if k.endswith(':') and not val.rstrip().endswith((':', '：', '։', '፡', '፦', '៖')): out.append(f'colon lost {k[:30]!r}')
        if '<' in val: out.append('markup')
    same = sum(1 for k in KEYS if s.get(k) == k and re.search(r'[a-z]{4,}', k))
    if same > 6: out.append(f'{same} identical to English')
    return [f'{lang}: {x}' for x in out[:8]]
langs = args or sorted(p.stem for p in DIR.glob('*.json') if p.stem != 'keys')
bad = 0
for lang in langs:
    issues = check(lang)
    if issues: bad += 1; print('\n'.join(issues))
    else: print(f'{lang}: OK ({len(KEYS)} strings)')
sys.exit(1 if bad else 0)
