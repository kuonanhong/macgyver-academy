#!/usr/bin/env python3
"""Integrate the V13 bridges & buildings curricula (橋樑與建築 100 courses).

Run after tools/structures-v13/build_structures.py. Repeatable: previously
integrated V13 structures content is replaced, earlier editions are preserved,
and the existing step IDs of `danjiang`, `b003`, `b015` and `b021` keep their
order (40 new steps are appended to each).
"""
import copy, csv, io, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'public/academy/data'
SRC = ROOT / 'tools/structures-v13/structures.json'
TAG = '-v13-'
NEW_STEPS = 40
DATE = '2026-10-15'


def read(p):
    return json.loads(p.read_text('utf-8'))


def write(p, value):
    text = json.dumps(value, ensure_ascii=False, **({'separators': (',', ':')} if p.name == 'featured.json' else {'indent': 2})) + '\n'
    tmp = p.with_suffix(p.suffix + '.tmp'); tmp.write_text(text, 'utf-8'); tmp.replace(p)


def strip_v13(course):
    """Remove previously integrated V13 stages so the script can be rerun."""
    course['stages'] = [st for st in course.get('stages', []) if TAG not in st['id']]
    return course


def main():
    o = read(SRC)
    courses = {c['id']: c for c in o['courses']}
    partial = '--allow-partial' in sys.argv  # development only: integrate the inputs written so far
    assert partial or len(courses) == 100, f'expected 100 structures courses, got {len(courses)}'
    featured = read(DATA / 'featured.json')
    catalog = read(DATA / 'catalog.json')
    sources = read(DATA / 'sources.json')
    srcmap = {s['id']: s for s in sources}
    for s in o['sources']:
        srcmap[s['id']] = {**srcmap.get(s['id'], {}), **s}
    sources = list(srcmap.values())

    fby = {c['id']: c for c in featured}
    new_order = []
    for cid, c in courses.items():
        if c.get('extendsExisting'):
            base = strip_v13(fby[cid])
            old_ids = [s['id'] for st in base['stages'] for s in st['steps']]
            assert len(old_ids) == c['existingStepCount'], (cid, len(old_ids), c['existingStepCount'])
            stages = copy.deepcopy(c['newStages'])
            stages[0]['steps'][0]['prerequisiteIds'] = [old_ids[-1]]
            base['stages'] = base['stages'] + stages
            base['sourceIds'] = c['sourceIds']
            base['enrichmentVersion'] = 13
            for key in ('learningTrack', 'learningSubdiscipline', 'learningTags', 'subcategory', 'subcategoryTitle', 'subcategoryTitleEn'):
                base[key] = c[key]
            # Keep the course's authored identity artwork; the V13 architecture is used only by the new steps' workbench.
            base['v13Architecture'] = {k: c[k] for k in ('architectureFamily', 'architectureNodes', 'architectureEdges')}
            base['v13Extension'] = {'stages': len(stages), 'steps': sum(len(st['steps']) for st in stages),
                                    'workedExample': c['workedExample'], 'focus': c['focus'], 'focusEn': c['focusEn']}
            target = base
        else:
            target = {k: v for k, v in c.items() if k not in ('focus', 'focusEn', 'dossier')}
            if cid not in fby:
                new_order.append(cid)
            fby[cid] = target
        steps = [s for st in target['stages'] for s in st['steps']]
        number = 0
        seen = set()
        for i, st in enumerate(target['stages']):
            st['order'] = i + 1
            for j, s in enumerate(st['steps']):
                number += 1
                s['order'] = j + 1
                s['sequence'] = number
                assert s['id'] not in seen, s['id']
                assert set(s.get('prerequisiteIds', [])) <= seen, s['id']
                seen.add(s['id'])
                assert set(s.get('sourceIds', [])) <= srcmap.keys(), s['id']
        target['stepCount'] = len(steps)
        target['estimatedMinutes'] = sum(s.get('estimatedMinutes', 20) for s in steps)
        assert target['stepCount'] == (c['existingStepCount'] + NEW_STEPS if c.get('extendsExisting') else NEW_STEPS), cid
    featured = [fby[c['id']] for c in featured] + [fby[cid] for cid in new_order]
    by = {c['id']: c for c in featured}

    # Slim catalog entries (no stages).
    out_catalog = []
    for entry in catalog:
        if entry['id'] in courses:
            full = by[entry['id']]
            slim = {k: v for k, v in full.items() if k not in ('stages', 'v12Extension', 'v13Extension', 'v13Architecture', 'dossier')}
            if courses[entry['id']].get('extendsExisting'):
                slim = {**entry, 'stepCount': full['stepCount'], 'estimatedMinutes': full['estimatedMinutes'],
                        'sourceIds': full['sourceIds'], 'enrichmentVersion': 13, 'status': 'guided',
                        **{k: full[k] for k in ('learningTrack', 'learningSubdiscipline', 'learningTags', 'subcategory', 'subcategoryTitle', 'subcategoryTitleEn')}}
            out_catalog.append(slim)
        else:
            out_catalog.append(entry)
    for key in ('id', 'title', 'titleEn'):
        vals = [str(c[key]).casefold() for c in out_catalog]
        assert len(vals) == len(set(vals)), 'duplicate ' + key

    # Places (with dated milestones) and related comparisons.
    places = read(DATA / 'course-places.json'); pm = {p['courseId']: p for p in places['courses']}
    for p in o['places']:
        cid = p['courseId']
        if p.get('extendsExisting') and cid in pm:
            prev = pm[cid]
            keep = [h for h in prev.get('history', []) if not h.get('v13')]
            add = [{**h, 'v13': True} for h in p['history'] if h['year'][:1].isdigit()]
            prev['history'] = keep + add
            refs = {r['url']: r for r in prev.get('references', [])}
            for r in p['references']:
                refs.setdefault(r['url'], r)
            prev['references'] = list(refs.values())
            prev['sourceIds'] = list(dict.fromkeys(prev.get('sourceIds', []) + p['sourceIds']))
        else:
            pm[cid] = {k: v for k, v in p.items() if k != 'extendsExisting'}
    related = read(DATA / 'related-skills.json'); rm = {r['courseId']: r for r in related['courses']}
    for r in o['related']:
        r = {k: v for k, v in r.items() if k != 'extendsExisting'}
        for v in r['related']:
            assert v['id'] in by and v['id'] in pm, v['id']
            v['place'] = copy.deepcopy(pm[v['id']]['place'])
            v['why'] = v['transfer']; v['whyEn'] = v['transferEn']
        assert partial or len(r['related']) == 2, r['courseId']
        prev = rm.get(r['courseId'])
        if prev and courses[r['courseId']].get('extendsExisting') and len(prev.get('related', [])) == 2:
            continue  # keep the two curated comparisons of an existing course (same rule as V12 optics)
        rm[r['courseId']] = r
    assert partial or (set(pm) >= set(by) and set(rm) >= set(by)), 'Every guided course needs places and comparisons'

    # Supplemental guides: principles/verification + engineering dossier.
    media = read(DATA / 'media.json'); mm = {m['courseId']: m for m in media['courses']}
    for cid, c in courses.items():
        full = by[cid]
        new_steps = [s for st in full['stages'] if TAG in st['id'] for s in st['steps']]
        entry = mm.setdefault(cid, {'courseId': cid, 'videos': [], 'guides': []})
        key, dkey = cid + '-v13-structures-guide', cid + '-v13-dossier'
        refs = [copy.deepcopy(srcmap[i]) for i in c['sourceIds'][-5:]]
        guide = {
            'id': key, 'title': '傳力、算例與驗證：' + full['title'], 'titleEn': 'Load paths, calculations and verification: ' + full['titleEn'],
            'concept': c['summary'], 'conceptEn': c['summaryEn'],
            'procedure': [s['instruction'].split(' 師傅任務')[0] for s in new_steps[::4]],
            'procedureEn': [s['instructionEn'].split(' Mentor task')[0] for s in new_steps[::4]],
            'evidence': [s['knowledge'][1]['text'] for s in new_steps[2::4]][:5],
            'evidenceEn': [s['knowledge'][1]['textEn'] for s in new_steps[2::4]][:5],
            'pitfalls': [s['instruction'].split(' 師傅任務')[0] for s in new_steps[3::8]],
            'pitfallsEn': [s['instructionEn'].split(' Mentor task')[0] for s in new_steps[3::8]],
            'sourceIds': c['sourceIds'][-5:], 'sources': refs,
            'simulationOnly': True, 'scope': c['scope'], 'scopeEn': c['scopeEn'],
        }
        book = c['dossier']
        dguide = {
            'id': dkey, 'title': '工程檔案：關鍵數據、年代、規範與案例', 'titleEn': 'Engineering dossier: key figures, timeline, codes and landmarks',
            'concept': c['focus'] + '。數據取自公開資料並經四捨五入，用於學習比較，不是設計值。',
            'conceptEn': c['focusEn'] + '. Figures come from public sources and are rounded for learning comparisons; they are not design values.',
            'facts': book['facts'], 'factsEn': book['factsEn'],
            'timeline': book['timeline'], 'timelineEn': book['timelineEn'],
            'codes': book['codes'], 'codesEn': book['codesEn'],
            'landmarks': book['landmarks'], 'landmarksEn': book['landmarksEn'],
            'procedure': ['把關鍵數據與本課算例逐項對照，標出哪些是公開工程數據、哪些是教學假設。',
                          '沿著工程時間軸，標出設計、施工、事件與維護改造的關鍵決策點，說明每個決策改變了哪一條傳力路徑或檢核。',
                          '對照列出的規範與標準，找出本課試驗或允收步驟對應的條款類型，並註明版本與適用地區。',
                          '從代表工程中選一個與本課比較，列出跨度或高度、結構系統、主要荷載與施工方法的差異。'],
            'procedureEn': ['Compare the key figures with this course\'s worked example and mark which are public project data and which are teaching assumptions.',
                            'Along the timeline, mark the key design, construction, event and retrofit decisions and say which load path or check each one changed.',
                            'Against the listed codes and standards, find the kind of clause behind this course\'s tests or acceptance steps, noting edition and jurisdiction.',
                            'Pick one landmark project to compare with this course and list differences in span or height, structural system, main loads and construction method.'],
            'pitfalls': ['把四捨五入的公開數據當成設計值或允收值使用。', '沒有確認規範版本、適用地區與荷載組合就直接套用另一國的條文。'],
            'pitfallsEn': ['Using rounded public figures as design or acceptance values.', 'Applying another country\'s clauses without checking edition, jurisdiction and load combinations.'],
            'sourceIds': c['sourceIds'][-5:], 'sources': refs,
            'simulationOnly': True, 'scope': c['scope'], 'scopeEn': c['scopeEn'],
        }
        entry['guides'] = [g for g in entry.get('guides', []) if g['id'] not in (key, dkey)] + [dguide, guide]
    media['courses'] = list(mm.values())

    # Vendors: companies + course associations.
    vendors = read(DATA / 'vendors.json'); vm = {v['id']: v for v in vendors['vendors']}; am = {a['courseId']: a for a in vendors['courses']}
    by_name = {v.get('nameEn', v['name']).casefold(): v['id'] for v in vm.values()}
    by_listing = {(v['security']['exchange'], v['security']['symbol']): v['id'] for v in vm.values() if v.get('security')}
    rename = {}
    for comp in o['companies']:
        sec = comp.get('security')
        existing = by_name.get(comp['nameEn'].casefold()) or (by_listing.get((sec['exchange'], sec['symbol'])) if sec else None)
        if existing:
            rename[comp['id']] = existing
            if not vm[existing].get('security') and comp.get('security'):
                vm[existing]['security'] = comp['security']
            continue
        vid = comp['id']
        while vid in vm:
            vid += '-x'
        rename[comp['id']] = vid
        vm[vid] = {**comp, 'id': vid}
        by_name[comp['nameEn'].casefold()] = vid
    for cid, links in o['associations'].items():
        ids, roles = [], []
        for link in links:
            vid = rename[link['companyId']]
            ids.append(vid); roles.append({'vendorId': vid, 'role': link['role'], 'roleEn': link['roleEn'], 'business': link.get('business', ''), 'businessEn': link.get('businessEn', ''), 'productUrl': vm[vid]['url']})
        prev = am.get(cid)
        if prev:
            ids = list(dict.fromkeys(prev['vendorIds'] + ids))
            roles = [r for r in prev.get('roles', []) if r['vendorId'] not in {x['vendorId'] for x in roles}] + roles
        am[cid] = {'courseId': cid, 'vendorIds': ids, 'roles': roles,
                   'connection': f'從「{by[cid]["title"]}」的材料、構件、施工或監測延伸到下列公司、業主與機構的官方資料；這是教材關聯，不代表合作、採購或背書。',
                   'connectionEn': f'Explore official information from companies, owners and institutions related to the materials, members, construction or monitoring of {by[cid]["titleEn"]}. This is a learning association, not a partnership, procurement or endorsement.'}
    vendors.update(version=13, reviewed=DATE, vendors=list(vm.values()), courses=list(am.values()))

    for name, value in [('featured', featured), ('catalog', out_catalog), ('sources', sources),
                        ('course-places', {**places, 'version': 13, 'courses': list(pm.values())}),
                        ('related-skills', {**related, 'version': 13, 'courses': list(rm.values())}),
                        ('media', {**media, 'version': 13}), ('vendors', vendors)]:
        write(DATA / f'{name}.json', value)

    header = ['id', 'title_zh', 'title_en', 'category', 'subcategory_zh', 'subcategory_en', 'content_type', 'authored_steps', 'route']
    for filename, rows in [('catalog-index.csv', out_catalog), ('bridges-buildings-100.csv', [by[cid] for cid in courses])]:
        buf = io.StringIO(newline=''); w = csv.writer(buf, lineterminator='\n'); w.writerow(header)
        for c in rows:
            w.writerow([c['id'], c['title'], c['titleEn'], c['category'], c.get('subcategoryTitle', ''), c.get('subcategoryTitleEn', ''),
                        'guided' if c['id'] in by else 'research', c.get('stepCount', 0) if c['id'] in by else 0, '#project/' + c['id']])
        (DATA / filename).write_text(buf.getvalue(), 'utf-8-sig')

    allsteps = [s for c in featured for st in c['stages'] for s in st['steps']]
    ststeps = [s for cid in courses for st in by[cid]['stages'] if TAG in st['id'] for s in st['steps']]
    release = read(DATA / 'release.json')
    release.update(version='13.0.0', date=DATE, topics=len(out_catalog), guidedCourses=len(featured),
                   researchTopics=len(out_catalog) - len(featured), allSteps=len(allsteps),
                   knowledgePoints=sum(len(s['knowledge']) for s in allsteps), sources=len(sources),
                   structuresCourses=len(courses), structuresSteps=len(ststeps),
                   structuresSubdisciplines=len({by[c].get('subcategory') for c in courses}),
                   structuresDossiers=len(courses),
                   courseHistories=len(pm), mapLocations=len(pm), curatedRelatedCourses=len(rm),
                   curatedComparisons=sum(len(r['related']) for r in rm.values()), mentorDemonstrations=len(allsteps),
                   narratedGuideSteps=len(allsteps), supplementalGuides=sum(len(m.get('guides', [])) for m in media['courses']),
                   industryEntities=len(vm), industryCourseAssociations=len(am), listedInstruments=sum(bool(v.get('security')) for v in vm.values()),
                   listedCompanies=sum(bool(v.get('security')) for v in vm.values()),
                   sharedInteractiveTasks=len(allsteps) - release.get('authoredInteractiveTasks', 52),
                   structuresScope='100 bridges-and-buildings curricula (96 new, danjiang, b003, b015 and b021 extended): 10 authored units per course, each expanded into load-path, quantitative, testing and failure-diagnosis steps, plus a dossier of key figures, timeline, codes and landmark comparisons. Original teaching exercises, not design documents, method statements or work permits.')
    write(DATA / 'release.json', release)
    print(json.dumps({k: release[k] for k in ('topics', 'guidedCourses', 'allSteps', 'structuresCourses', 'structuresSteps', 'knowledgePoints', 'sources', 'industryEntities', 'listedCompanies')}, ensure_ascii=False))


if __name__ == '__main__':
    main()
