#!/usr/bin/env python3
"""Merge the V12 company curation into public/academy/data/vendors.json.

Inputs (repeatable, order matters only for tie-breaking):
  tools/markets-v12/vendors_chips_electronics.json   chips / electronics / energy …
  tools/markets-v12/vendors_computing_world.json     computing / world projects …
Each file: {"companies": [...], "courses": {courseId: [{companyId, role, roleEn}, ...]}}
The course lists are complete sets: they replace that course's previous links.
Optics courses (V12) keep the associations written by integrate-optics-v12.py.

What the merge does
  * company records: curated name, URLs and listing (symbol/exchange/currency)
    win; a specific existing description is kept, generic V11 template text is
    replaced; the curated description becomes the course-specific "business".
  * duplicates (same company under several ids, e.g. "rtx" / "rtx-raytheon")
    are merged into one canonical id and every course link is remapped.
  * companies no course links to any more are removed.
  * internal provenance notes ("verified") are kept out of the public file and
    summarised in tools/markets-v12/ticker-provenance.json.
"""
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'public/academy/data'
INPUTS = [ROOT / 'tools/markets-v12/vendors_chips_electronics.json', ROOT / 'tools/markets-v12/vendors_computing_world.json']
GENERIC = ('可用來比較本課的', 'compare the equipment, component or design-tool role', '不代表本網站推薦或廠商授課')
REVIEWED = '2026-10-15'
# Same company recorded twice under different ids (alias -> canonical).
ALIASES = {'corning-incorporated': 'corning', 'official-3932d5b8e9fb': 'keysight-technologies',
           'v11-publisher-8cbf04143c8a': 'vestas', 'andor-oxford-instruments': 'oxford-instruments-andor'}
# Divisions quoted through a listed parent group: (symbol, exchange) -> (zh, en).
LISTED_AS = {('AME', 'NYSE'): ('阿美特克 AMETEK', 'AMETEK'), ('OXIG', 'LSE'): ('牛津儀器 Oxford Instruments', 'Oxford Instruments'),
             ('MKSI', 'NASDAQ'): ('MKS', 'MKS Inc.'), ('SAF', 'EPA'): ('賽峰集團 Safran', 'Safran'),
             ('6302', 'TSE'): ('住友重機械工業', 'Sumitomo Heavy Industries'), ('TDY', 'NYSE'): ('Teledyne Technologies', 'Teledyne Technologies')}


def norm_name(name):
    name = re.sub(r'\(.*?\)|（.*?）', ' ', name or '').casefold()
    name = re.sub(r'\b(inc|corp|corporation|co|ltd|plc|ag|se|sa|nv|n\.v|group|holdings?)\b\.?', ' ', name)
    return re.sub(r'[^0-9a-zÀ-ɏ一-鿿]+', '', name)


def canonical_rank(vid, record):
    synthetic = vid.startswith(('v11-publisher-', 'official-'))
    return (synthetic, not record.get('security'), len(vid), vid)


def main():
    vendors = json.loads((DATA / 'vendors.json').read_text('utf-8'))
    featured_ids = {c['id'] for c in json.loads((DATA / 'featured.json').read_text('utf-8'))}
    vm = {v['id']: v for v in vendors['vendors']}
    am = {a['courseId']: a for a in vendors['courses']}
    titles = {c['id']: (c['title'], c['titleEn']) for c in json.loads((DATA / 'catalog.json').read_text('utf-8'))}
    provenance, curated_business, curated_courses = {}, {}, {}

    for path in INPUTS:
        cur = json.loads(path.read_text('utf-8'))
        for comp in cur['companies']:
            vid = comp['id']
            old = vm.get(vid, {})
            rec = {**old, 'id': vid, 'name': comp['name'], 'nameEn': comp['nameEn'],
                   'url': comp.get('url') or old.get('url', ''), 'investorUrl': comp.get('investorUrl') or old.get('investorUrl', ''),
                   'sourceUrl': old.get('sourceUrl') or comp.get('url', ''), 'reviewed': REVIEWED}
            if not old.get('business') or any(g in old.get('business', '') + old.get('businessEn', '') for g in GENERIC):
                rec['business'], rec['businessEn'] = comp['business'], comp['businessEn']
            if comp.get('security'):
                rec['security'] = comp['security']
            vm[vid] = rec
            curated_business[(path.name, vid)] = (comp['business'], comp['businessEn'])
            if comp.get('security'):
                provenance[vid] = {**comp['security'], 'nameEn': comp['nameEn'], 'note': comp.get('verified', '')}
        for cid, links in cur['courses'].items():
            if cid not in featured_ids:
                sys.exit(f'unknown course {cid} in {path.name}')
            if cid in curated_courses:
                sys.exit(f'course {cid} curated twice')
            curated_courses[cid] = (path.name, links)

    # Replace links of curated courses (complete sets).
    for cid, (fname, links) in curated_courses.items():
        title, title_en = titles.get(cid, (cid, cid))
        roles = []
        for link in links:
            business, business_en = curated_business.get((fname, link['companyId']), ('', ''))
            roles.append({'vendorId': link['companyId'], 'role': link['role'], 'roleEn': link['roleEn'],
                          'business': business, 'businessEn': business_en})
        am[cid] = {'courseId': cid, 'vendorIds': [r['vendorId'] for r in roles], 'roles': roles,
                   'connection': f'從「{title}」的材料、設備、設計、量測或系統整合問題，延伸查閱下列公司與機構的官方資料；這是教材關聯，不代表合作、採購、背書或投資建議。',
                   'connectionEn': f'Explore official information from companies and institutions related to the materials, equipment, design, measurement or system integration in {title_en}. This is a learning association, not a partnership, procurement, endorsement or investment advice.'}

    # One code per exchange (all Euronext listings here are Paris).
    for rec in vm.values():
        sec = rec.get('security')
        if sec and sec.get('exchange') in ('EURONEXT', 'PAR'):
            sec['exchange'] = 'EPA'

    # Merge duplicate companies.
    groups = defaultdict(list)
    for vid, rec in vm.items():
        groups[norm_name(rec.get('nameEn') or rec.get('name'))].append(vid)
    remap = {a: c for a, c in ALIASES.items() if a in vm and c in vm}
    for key, ids in groups.items():
        if len(ids) < 2 or not key:
            continue
        listed = {json.dumps({k: vm[i]['security'].get(k) for k in ('symbol', 'exchange')}) for i in ids if vm[i].get('security')}
        if len(listed) > 1:
            print('! same name, different listings — kept separate:', ids, listed, file=sys.stderr)
            continue
        keep = min(ids, key=lambda i: canonical_rank(i, vm[i]))
        for i in ids:
            if i != keep:
                remap[i] = keep
                if not vm[keep].get('security') and vm[i].get('security'):
                    vm[keep]['security'] = vm[i]['security']
                if any(g in vm[keep].get('business', '') for g in GENERIC) and not any(g in vm[i].get('business', '') for g in GENERIC):
                    vm[keep]['business'], vm[keep]['businessEn'] = vm[i]['business'], vm[i]['businessEn']
    def final(i):
        hops = 0
        while i in remap and hops < 10:
            i, hops = remap[i], hops + 1
        return i
    remap = {i: final(i) for i in remap}
    for entry in am.values():
        roles, seen = [], set()
        for r in entry.get('roles', []):
            r = {**r, 'vendorId': remap.get(r['vendorId'], r['vendorId'])}
            if r['vendorId'] not in seen:
                seen.add(r['vendorId']); roles.append(r)
        ids = list(dict.fromkeys(remap.get(i, i) for i in entry['vendorIds']))
        entry['vendorIds'], entry['roles'] = ids, roles
        for r in roles:
            r['productUrl'] = r.get('productUrl') or vm[r['vendorId']].get('url', '')
    for i in remap:
        vm.pop(i, None)

    used = {i for e in am.values() for i in e['vendorIds']}
    missing = used - vm.keys()
    if missing:
        sys.exit(f'links to unknown companies: {sorted(missing)[:10]}')
    removed = sorted(set(vm) - used)
    for i in removed:
        vm.pop(i)
    missing_courses = featured_ids - am.keys()
    order = [c for c in vendors['courses'] if c['courseId'] in am]
    known = {c['courseId'] for c in order}
    courses = [am[c['courseId']] for c in order] + [am[c] for c in sorted(am) if c not in known]
    # Subsidiaries/divisions quoted through their listed parent.
    by_listing = defaultdict(list)
    for rec in vm.values():
        rec.pop('verified', None)
        if rec.get('security'):
            rec['security'].pop('parent', None); rec['security'].pop('parentEn', None)
            by_listing[(rec['security']['symbol'], rec['security']['exchange'])].append(rec)
    for key, recs in by_listing.items():
        if len(recs) > 1:
            if key not in LISTED_AS:
                sys.exit(f'several companies share listing {key}: add them to ALIASES or LISTED_AS')
            zh, en = LISTED_AS[key]
            for r in recs:
                if r['nameEn'] != en:
                    r['security']['parent'], r['security']['parentEn'] = zh, en
    vendors.update(version=12, reviewed=REVIEWED, vendors=sorted(vm.values(), key=lambda v: v['id']), courses=courses)
    (DATA / 'vendors.json').write_text(json.dumps(vendors, ensure_ascii=False, indent=2) + '\n', 'utf-8')
    prov = {k: v for k, v in sorted(provenance.items()) if remap.get(k, k) in vm}
    (ROOT / 'tools/markets-v12/ticker-provenance.json').write_text(json.dumps(prov, ensure_ascii=False, indent=1) + '\n', 'utf-8')
    listed = sum(bool(v.get('security')) for v in vm.values())
    print(json.dumps({'companies': len(vm), 'listed': listed, 'courses': len(courses), 'coursesWithoutCompanies': len(missing_courses),
                      'mergedDuplicates': len(remap), 'removedUnused': len(removed),
                      'exchanges': Counter(v['security']['exchange'] for v in vm.values() if v.get('security')).most_common()}, ensure_ascii=False))


if __name__ == '__main__':
    main()
