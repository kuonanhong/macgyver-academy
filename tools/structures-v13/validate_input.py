#!/usr/bin/env python3
"""Validate V13 bridges & buildings course inputs (tools/structures-v13/inputs/<id>.json).
Usage: python3 -I tools/structures-v13/validate_input.py tools/structures-v13/inputs/b066.json [...]
Exit 0 only when every file passes; prints every problem found.
"""
from __future__ import annotations
import json, re, sys, pathlib

HERE = pathlib.Path(__file__).resolve().parent
TARGETS = {t['id']: t for t in json.loads((HERE / 'targets.json').read_text('utf-8'))}
ALL_IDS = set(TARGETS)
UNITS = 10
FAMILIES = {'suspension', 'cablestayed', 'arch', 'viaduct', 'segmental', 'deck', 'cable', 'bearing', 'pier',
            'foundation', 'tower', 'outrigger', 'damper', 'roof', 'membrane', 'shell', 'facade', 'connection',
            'concrete', 'survey', 'modular', 'fire', 'elevator'}
EXCHANGES = {'NASDAQ', 'NYSE', 'TWSE', 'TPEx', 'TSE', 'LSE', 'XETRA', 'EURONEXT', 'AMS', 'EBR', 'SIX', 'KRX', 'HKEX', 'SSE',
             'SZSE', 'STO', 'CPH', 'HEL', 'OSL', 'BIT', 'BME', 'TSX', 'ASX', 'NSE', 'DFM', 'VIE'}
CJK = re.compile(r'[㐀-鿿]')
WORD = re.compile(r'[A-Za-z]{2,}')
BAD = ('待開發', 'TODO', 'lorem', '待補', 'placeholder', 'TBD', 'XXX')


def pair(value, where, problems, zh=(1, 100000), en=(1, 100000), digit=False):
    if not isinstance(value, str) or value.count('~') != 1:
        problems.append(f'{where}: must be ONE string "中文~English" with exactly one ~'); return ('', '')
    z, e = (s.strip() for s in value.split('~', 1))
    nz, ne = len(CJK.findall(z)), len(WORD.findall(e))
    if nz < zh[0]: problems.append(f'{where}: Chinese part too short ({nz} CJK < {zh[0]})')
    if nz > zh[1]: problems.append(f'{where}: Chinese part too long ({nz} CJK > {zh[1]})')
    if ne < en[0]: problems.append(f'{where}: English part too short ({ne} words < {en[0]})')
    if ne > en[1]: problems.append(f'{where}: English part too long ({ne} words > {en[1]})')
    if CJK.search(e): problems.append(f'{where}: English part contains CJK characters')
    if digit and not (re.search(r'\d', z) and re.search(r'\d', e)): problems.append(f'{where}: needs at least one number in both languages')
    for bad in BAD:
        if bad.lower() in value.lower(): problems.append(f'{where}: placeholder text "{bad}"')
    return z, e


def url_ok(u):
    return isinstance(u, str) and re.fullmatch(r'https://[^\s<>"\']+', u) is not None


def validate(path: pathlib.Path) -> list[str]:
    P: list[str] = []
    try:
        d = json.loads(path.read_text('utf-8'))
    except Exception as e:  # noqa: BLE001
        return [f'{path}: invalid JSON: {e}']
    cid = d.get('id')
    if cid not in TARGETS: return [f'{path}: id {cid!r} is not a V13 structures target']
    t = TARGETS[cid]
    if path.stem != cid: P.append('file name must equal the course id')
    if d.get('title') != f"{t['title']}~{t['titleEn']}": P.append(f"title must be exactly {t['title']}~{t['titleEn']}")
    if d.get('discipline') != t['discipline']: P.append(f"discipline must be {t['discipline']}")
    if d.get('family') not in FAMILIES: P.append(f'family must be one of {sorted(FAMILIES)}')
    pair(d.get('focus'), 'focus', P, (8, 70), (5, 30))
    pair(d.get('summary'), 'summary', P, (60, 260), (35, 150))
    pair(d.get('example'), 'example', P, (100, 850), (80, 480), digit=True)
    pair(d.get('history'), 'history', P, (100, 560), (60, 330))
    units = d.get('units')
    if not isinstance(units, list) or len(units) != UNITS:
        P.append(f'units must be a list of exactly {UNITS} objects')
    else:
        titles, anchors = set(), set()
        for i, u in enumerate(units, 1):
            w = f'units[{i}]'
            if not isinstance(u, dict): P.append(f'{w}: must be an object'); continue
            for key in ('anchor', 'title', 'mechanism', 'model', 'verify', 'failure', 'misconception', 'practice'):
                if key not in u: P.append(f'{w}.{key}: missing')
            z, _ = pair(u.get('title'), f'{w}.title', P, (4, 40), (2, 16))
            if z in titles: P.append(f'{w}.title: duplicate unit title')
            titles.add(z)
            a, _ = pair(u.get('anchor'), f'{w}.anchor', P, (2, 24), (1, 10))
            if a in anchors: P.append(f'{w}.anchor: duplicate anchor')
            anchors.add(a)
            pair(u.get('mechanism'), f'{w}.mechanism', P, (100, 460), (60, 260))
            pair(u.get('model'), f'{w}.model', P, (20, 330), (14, 190), digit=True)
            pair(u.get('verify'), f'{w}.verify', P, (60, 330), (35, 190))
            pair(u.get('failure'), f'{w}.failure', P, (40, 290), (25, 170))
            pair(u.get('misconception'), f'{w}.misconception', P, (10, 70), (6, 40))
            pair(u.get('practice'), f'{w}.practice', P, (40, 270), (25, 160))
    facts = d.get('facts')
    if not isinstance(facts, list) or not 6 <= len(facts) <= 10: P.append('facts must list 6 to 10 "中文~English" items')
    else:
        for i, f in enumerate(facts, 1): pair(f, f'facts[{i}]', P, (6, 90), (3, 45), digit=True)
    timeline = d.get('timeline')
    if not isinstance(timeline, list) or not 3 <= len(timeline) <= 6: P.append('timeline must have 3 to 6 {year, event} objects')
    else:
        for i, m in enumerate(timeline, 1):
            if not isinstance(m, dict) or not re.search(r'\d{3,4}', str(m.get('year', ''))) or len(str(m.get('year', ''))) > 24:
                P.append(f'timeline[{i}].year: short string containing a year, e.g. "1998" or "1988–1998"')
            pair(m.get('event') if isinstance(m, dict) else None, f'timeline[{i}].event', P, (10, 130), (6, 70))
    codes = d.get('codes')
    if not isinstance(codes, list) or not 2 <= len(codes) <= 4: P.append('codes must list 2 to 4 real codes/standards/guides')
    else:
        for i, c in enumerate(codes, 1): pair(c, f'codes[{i}]', P, (4, 90), (3, 45))
    marks = d.get('landmarks')
    if not isinstance(marks, list) or not 2 <= len(marks) <= 4: P.append('landmarks must list 2 to 4 named real projects')
    else:
        for i, c in enumerate(marks, 1): pair(c, f'landmarks[{i}]', P, (2, 40), (1, 20))
    place = d.get('place') or {}
    pair(place.get('name'), 'place.name', P, (4, 40), (2, 16))
    pair(place.get('country'), 'place.country', P, (2, 12), (1, 6))
    if not (isinstance(place.get('lat'), (int, float)) and -90 <= place['lat'] <= 90): P.append('place.lat invalid')
    if not (isinstance(place.get('lng'), (int, float)) and -180 <= place['lng'] <= 180): P.append('place.lng invalid')
    if not (isinstance(place.get('query'), str) and len(place['query']) >= 5): P.append('place.query must be a map search string')
    sources = d.get('sources')
    if not isinstance(sources, list) or not 3 <= len(sources) <= 5: P.append('sources must contain 3 to 5 entries')
    else:
        keys = set()
        for i, s in enumerate(sources, 1):
            w = f'sources[{i}]'
            for key in ('key', 'title', 'titleEn', 'publisher', 'url', 'sourceType', 'scope', 'scopeEn'):
                if not isinstance(s.get(key), str) or not s[key].strip(): P.append(f'{w}.{key}: missing or empty')
            if not re.fullmatch(r'[a-z0-9][a-z0-9-]{2,60}', str(s.get('key', ''))): P.append(f'{w}.key: lowercase letters, digits, hyphens')
            if s.get('key') in keys: P.append(f'{w}.key: duplicate')
            keys.add(s.get('key'))
            if not url_ok(s.get('url')): P.append(f'{w}.url: must be https')
            if 'wikipedia.org' in str(s.get('url')) and s.get('sourceType') != 'secondary': P.append(f'{w}: Wikipedia must be "secondary"')
            if s.get('sourceType') not in ('primary', 'secondary'): P.append(f'{w}.sourceType: primary|secondary')
            if CJK.search(str(s.get('titleEn', ''))): P.append(f'{w}.titleEn contains CJK')
            if not CJK.search(str(s.get('title', ''))): P.append(f'{w}.title must be Chinese')
            if not CJK.search(str(s.get('scope', ''))): P.append(f'{w}.scope must be Chinese')
        if sum(1 for s in sources if isinstance(s, dict) and s.get('sourceType') == 'primary') < 2:
            P.append('at least 2 primary (official/institutional/owner/designer/standards) sources are required')
    vendors = d.get('vendors')
    if not isinstance(vendors, list) or not 2 <= len(vendors) <= 4: P.append('vendors must contain 2 to 4 entries')
    else:
        for i, v in enumerate(vendors, 1):
            w = f'vendors[{i}]'
            for key in ('name', 'nameEn', 'business', 'businessEn', 'url', 'role', 'roleEn'):
                if not isinstance(v.get(key), str) or not v[key].strip(): P.append(f'{w}.{key}: missing or empty')
            if not url_ok(v.get('url')): P.append(f'{w}.url: must be https')
            if v.get('investorUrl') not in ('', None) and not url_ok(v.get('investorUrl')): P.append(f'{w}.investorUrl: https or ""')
            sec = v.get('security', 'MISSING')
            if sec == 'MISSING': P.append(f'{w}.security: required (object or null)')
            elif sec is not None:
                if not isinstance(sec, dict) or not re.fullmatch(r'[A-Z0-9.\-]{1,12}', str(sec.get('symbol', ''))): P.append(f'{w}.security.symbol invalid')
                if sec.get('exchange') not in EXCHANGES: P.append(f'{w}.security.exchange must be one of {sorted(EXCHANGES)}')
                if not re.fullmatch(r'[A-Z]{3}', str(sec.get('currency', ''))): P.append(f'{w}.security.currency must be ISO code')
            if not CJK.search(str(v.get('business', ''))): P.append(f'{w}.business must be Chinese')
            if CJK.search(str(v.get('businessEn', ''))): P.append(f'{w}.businessEn contains CJK')
    rel = d.get('related')
    if not isinstance(rel, list) or len(rel) != 2 or len(set(rel)) != 2 or cid in rel or not set(rel) <= ALL_IDS:
        P.append(f'related must be 2 distinct ids from the structures set (danjiang, b002–b100), not {cid}')
    nodes = d.get('architectureNodes')
    if not isinstance(nodes, list) or not 4 <= len(nodes) <= 6 or any(not (isinstance(n, list) and len(n) == 2 and CJK.search(n[0]) and not CJK.search(n[1])) for n in nodes):
        P.append('architectureNodes must be 4–6 [中文, English] pairs')
    edges = d.get('architectureEdges')
    if isinstance(nodes, list) and (not isinstance(edges, list) or len(edges) < len(nodes) - 1 or any(not (isinstance(e, list) and len(e) == 2 and all(isinstance(x, int) and 0 <= x < len(nodes) for x in e) and e[0] != e[1]) for e in edges)):
        P.append('architectureEdges must connect node indices (≥ nodes−1 edges, no self loops)')
    return [f'{path.name}: {p}' for p in P]


if __name__ == '__main__':
    files = [pathlib.Path(a) for a in sys.argv[1:]] or sorted((HERE / 'inputs').glob('*.json'))
    bad = 0
    for f in files:
        issues = validate(f)
        if issues:
            bad += 1; print('\n'.join(issues))
        else:
            print(f'{f.name}: OK')
    sys.exit(1 if bad else 0)
