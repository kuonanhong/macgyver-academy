#!/usr/bin/env python3
"""Validate UI dictionaries: python3 -I tools/i18n-v12/validate_i18n.py [lang ...]"""
import json, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
KEYS = json.loads((ROOT / 'tools/i18n-v12/ui_keys.json').read_text('utf-8'))
DIR = ROOT / 'public/academy/i18n'
def check(lang):
    p = DIR / f'{lang}.json'
    if not p.exists(): return [f'{lang}: missing file']
    d = json.loads(p.read_text('utf-8')); s = d.get('strings', {}); problems = []
    if d.get('lang') != lang: problems.append('lang field mismatch')
    missing = [k for k in KEYS if not isinstance(s.get(k), str) or not s[k].strip()]
    if missing: problems.append(f'{len(missing)} missing, e.g. {missing[:3]}')
    for k, v in s.items():
        if k not in KEYS: problems.append(f'unknown key {k[:40]!r}'); continue
        if not isinstance(v, str): continue
        if k.count('{n}') != v.count('{n}'): problems.append(f'placeholder mismatch in {k[:50]!r}')
        if '<' in v and '<' not in k: problems.append(f'markup added in {k[:40]!r}')
    same = sum(1 for k in KEYS if s.get(k) == k and re.search(r'[a-z]{4,}', k))
    if same > len(KEYS) * 0.15: problems.append(f'{same} strings left untranslated (identical to English)')
    return [f'{lang}: {x}' for x in problems[:12]]
langs = sys.argv[1:] or sorted(p.stem for p in DIR.glob('*.json') if p.stem != 'index')
bad = 0
for lang in langs:
    issues = check(lang)
    if issues: bad += 1; print('\n'.join(issues))
    else: print(f'{lang}: OK ({len(KEYS)} strings)')
sys.exit(1 if bad else 0)
