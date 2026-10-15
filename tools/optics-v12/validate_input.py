#!/usr/bin/env python3
"""Validate one or more V12 optics course input files.
Usage: python3 -I tools/optics-v12/validate_input.py tools/optics-v12/inputs/a402.json [...]
Exit 0 only when every file passes; prints every problem found.
"""
from __future__ import annotations
import json, re, sys, pathlib

HERE = pathlib.Path(__file__).resolve().parent
TARGETS = {t['id']: t for t in json.loads((HERE / 'targets.json').read_text('utf-8'))}
ALL_IDS = set(TARGETS) | {'asml', 'a405'}
FAMILIES = {'lithography','imaging','fabrication','coating','modulator','microscope','spectrometer','interferometer','laser','inertial','electron','vacuum','cryo','stage','accelerator','detector','telescope','radio','gw'}
EXCHANGES = {'NASDAQ','NYSE','TWSE','TPEx','TSE','LSE','XETRA','EURONEXT','SIX','KRX','HKEX','SSE','SZSE','NSE','TSX','ASX','STO','OMX','OSE','BIT','BME','AMS','PAR','SWX','ETR','FRA'}
CJK = re.compile(r'[㐀-鿿]')
ASCII_WORD = re.compile(r'[A-Za-z]{2,}')

def pair(value, where, problems, zh_min=1, en_min=1, zh_max=100000, en_max=100000, need_digit=False):
    if not isinstance(value, str) or value.count('~') != 1:
        problems.append(f'{where}: must be one string "中文~English" with exactly one ~'); return ('', '')
    zh, en = (s.strip() for s in value.split('~', 1))
    if len(CJK.findall(zh)) < zh_min: problems.append(f'{where}: Chinese part too short ({len(CJK.findall(zh))} CJK chars < {zh_min})')
    if len(CJK.findall(zh)) > zh_max: problems.append(f'{where}: Chinese part too long')
    words = len(ASCII_WORD.findall(en))
    if words < en_min: problems.append(f'{where}: English part too short ({words} words < {en_min})')
    if words > en_max: problems.append(f'{where}: English part too long')
    if CJK.search(en): problems.append(f'{where}: English part contains CJK characters')
    if need_digit and not (re.search(r'\d', zh) and re.search(r'\d', en)): problems.append(f'{where}: must contain at least one number in both languages')
    for bad in ('待開發', 'TODO', 'lorem', '待補', 'placeholder'):
        if bad.lower() in value.lower(): problems.append(f'{where}: contains placeholder text "{bad}"')
    return zh, en

def url_ok(u): return isinstance(u, str) and re.fullmatch(r'https://[^\s<>"\']+', u) is not None

def validate(path: pathlib.Path) -> list[str]:
    problems: list[str] = []
    try: d = json.loads(path.read_text('utf-8'))
    except Exception as e: return [f'{path}: invalid JSON: {e}']
    cid = d.get('id')
    if cid not in TARGETS: return [f'{path}: id {cid!r} is not a V12 target']
    t = TARGETS[cid]
    if path.stem != cid: problems.append('file name must equal the course id')
    if d.get('title') != f"{t['title']}~{t['titleEn']}": problems.append(f"title must be exactly {t['title']}~{t['titleEn']}")
    if d.get('discipline') != t['discipline']: problems.append(f"discipline must be {t['discipline']}")
    if d.get('family') not in FAMILIES: problems.append(f'family must be one of {sorted(FAMILIES)}')
    pair(d.get('focus'), 'focus', problems, 8, 5, 60, 25)
    pair(d.get('summary'), 'summary', problems, 50, 30, 220, 120)
    pair(d.get('example'), 'example', problems, 70, 60, 700, 400, need_digit=True)
    pair(d.get('history'), 'history', problems, 80, 50, 500, 300)
    units = d.get('units')
    if not isinstance(units, list) or len(units) != 8: problems.append('units must be a list of exactly 8 objects')
    else:
        titles = set()
        for i, u in enumerate(units, 1):
            w = f'units[{i}]'
            if not isinstance(u, dict): problems.append(f'{w}: must be an object'); continue
            for key in ('anchor','title','mechanism','model','verify','failure','misconception'):
                if key not in u: problems.append(f'{w}.{key}: missing')
            z, e = pair(u.get('title'), f'{w}.title', problems, 4, 2, 40, 16)
            if z in titles: problems.append(f'{w}.title: duplicate unit title')
            titles.add(z)
            pair(u.get('anchor'), f'{w}.anchor', problems, 2, 1, 24, 10)
            pair(u.get('mechanism'), f'{w}.mechanism', problems, 80, 50, 400, 220)
            pair(u.get('model'), f'{w}.model', problems, 20, 18, 300, 170, need_digit=True)
            pair(u.get('verify'), f'{w}.verify', problems, 50, 30, 300, 170)
            pair(u.get('failure'), f'{w}.failure', problems, 30, 20, 260, 150)
            pair(u.get('misconception'), f'{w}.misconception', problems, 10, 6, 70, 40)
    place = d.get('place') or {}
    pair(place.get('name'), 'place.name', problems, 4, 2, 40, 15)
    pair(place.get('country'), 'place.country', problems, 2, 1, 12, 6)
    if not (isinstance(place.get('lat'), (int, float)) and -90 <= place['lat'] <= 90): problems.append('place.lat invalid')
    if not (isinstance(place.get('lng'), (int, float)) and -180 <= place['lng'] <= 180): problems.append('place.lng invalid')
    if not (isinstance(place.get('query'), str) and len(place['query']) >= 5): problems.append('place.query must be a map search string')
    sources = d.get('sources')
    if not isinstance(sources, list) or not 2 <= len(sources) <= 4: problems.append('sources must contain 2 to 4 entries')
    else:
        keys = set()
        for i, s in enumerate(sources, 1):
            w = f'sources[{i}]'
            for key in ('key','title','titleEn','publisher','url','sourceType','scope','scopeEn'):
                if not isinstance(s.get(key), str) or not s[key].strip(): problems.append(f'{w}.{key}: missing or empty')
            if not re.fullmatch(r'[a-z0-9][a-z0-9-]{2,60}', str(s.get('key', ''))): problems.append(f'{w}.key: use lowercase letters, digits and hyphens')
            if s.get('key') in keys: problems.append(f'{w}.key: duplicate')
            keys.add(s.get('key'))
            if not url_ok(s.get('url')): problems.append(f'{w}.url: must be https')
            if 'wikipedia.org' in str(s.get('url')) and s.get('sourceType') != 'secondary': problems.append(f'{w}: Wikipedia must be sourceType "secondary"')
            if s.get('sourceType') not in ('primary', 'secondary'): problems.append(f'{w}.sourceType: primary|secondary')
            if CJK.search(str(s.get('titleEn', ''))): problems.append(f'{w}.titleEn contains CJK')
            if not CJK.search(str(s.get('title', ''))): problems.append(f'{w}.title must be Chinese')
            if not CJK.search(str(s.get('scope', ''))): problems.append(f'{w}.scope must be Chinese')
        primaries = sum(1 for s in sources if isinstance(s, dict) and s.get('sourceType') == 'primary')
        if primaries < 2: problems.append('at least 2 primary (official/institutional) sources are required')
    vendors = d.get('vendors')
    if not isinstance(vendors, list) or not 2 <= len(vendors) <= 4: problems.append('vendors must contain 2 to 4 entries')
    else:
        for i, v in enumerate(vendors, 1):
            w = f'vendors[{i}]'
            for key in ('name','nameEn','business','businessEn','url','role','roleEn'):
                if not isinstance(v.get(key), str) or not v[key].strip(): problems.append(f'{w}.{key}: missing or empty')
            if not url_ok(v.get('url')): problems.append(f'{w}.url: must be https')
            if v.get('investorUrl') not in ('', None) and not url_ok(v.get('investorUrl')): problems.append(f'{w}.investorUrl: must be https or ""')
            sec = v.get('security', 'MISSING')
            if sec == 'MISSING': problems.append(f'{w}.security: required (object or null)')
            elif sec is not None:
                if not isinstance(sec, dict) or not re.fullmatch(r'[A-Z0-9.\-]{1,12}', str(sec.get('symbol', ''))): problems.append(f'{w}.security.symbol invalid')
                if sec.get('exchange') not in EXCHANGES: problems.append(f'{w}.security.exchange must be one of {sorted(EXCHANGES)}')
                if not re.fullmatch(r'[A-Z]{3}', str(sec.get('currency', ''))): problems.append(f'{w}.security.currency must be ISO code')
            if not CJK.search(str(v.get('business', ''))): problems.append(f'{w}.business must be Chinese')
            if CJK.search(str(v.get('businessEn', ''))): problems.append(f'{w}.businessEn contains CJK')
    rel = d.get('related')
    if not isinstance(rel, list) or len(rel) != 2 or len(set(rel)) != 2 or cid in rel or not set(rel) <= ALL_IDS: problems.append(f'related must be 2 distinct ids from the optics set (a401–a500, asml), not {cid}')
    nodes = d.get('architectureNodes')
    if not isinstance(nodes, list) or not 4 <= len(nodes) <= 6 or any(not (isinstance(n, list) and len(n) == 2 and CJK.search(n[0]) and not CJK.search(n[1])) for n in nodes): problems.append('architectureNodes must be 4–6 [中文, English] pairs')
    edges = d.get('architectureEdges')
    if isinstance(nodes, list) and (not isinstance(edges, list) or len(edges) < len(nodes) - 1 or any(not (isinstance(e, list) and len(e) == 2 and all(isinstance(x, int) and 0 <= x < len(nodes) for x in e) and e[0] != e[1]) for e in edges)): problems.append('architectureEdges must connect node indices (≥ nodes−1 edges, no self loops)')
    return [f'{path.name}: {p}' for p in problems]

if __name__ == '__main__':
    files = [pathlib.Path(a) for a in sys.argv[1:]] or sorted((HERE / 'inputs').glob('a*.json'))
    bad = 0
    for f in files:
        issues = validate(f)
        if issues:
            bad += 1; print('\n'.join(issues))
        else:
            print(f'{f.name}: OK')
    sys.exit(1 if bad else 0)
