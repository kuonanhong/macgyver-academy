#!/usr/bin/env python3
"""Integrate the V12 optics & precision-instrument curricula (101 courses).

Run after tools/optics-v12/build_optics.py. Repeatable: previously integrated
V12 optics content is replaced, earlier editions are preserved, and existing
step IDs of `asml` and `a405` keep their order (new steps are appended).
"""
import copy, csv, io, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'public/academy/data'
SRC = ROOT / 'tools/optics-v12/optics.json'


def read(p):
    return json.loads(p.read_text('utf-8'))


def write(p, value):
    text = json.dumps(value, ensure_ascii=False, **({'separators': (',', ':')} if p.name == 'featured.json' else {'indent': 2})) + '\n'
    tmp = p.with_suffix(p.suffix + '.tmp'); tmp.write_text(text, 'utf-8'); tmp.replace(p)


def strip_v12(course):
    """Remove previously integrated V12 stages so the script can be rerun."""
    course['stages'] = [st for st in course.get('stages', []) if '-v12-' not in st['id']]
    return course


def main():
    o = read(SRC)
    courses = {c['id']: c for c in o['courses']}
    assert len(courses) == 101, f'expected 101 optics courses, got {len(courses)}'
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
            base = strip_v12(fby[cid])
            old_ids = [s['id'] for st in base['stages'] for s in st['steps']]
            assert len(old_ids) == c['existingStepCount'], (cid, len(old_ids), c['existingStepCount'])
            stages = copy.deepcopy(c['newStages'])
            stages[0]['steps'][0]['prerequisiteIds'] = [old_ids[-1]]
            base['stages'] = base['stages'] + stages
            base['sourceIds'] = c['sourceIds']
            base['enrichmentVersion'] = 12
            for key in ('learningTrack', 'learningSubdiscipline', 'learningTags', 'subcategory', 'subcategoryTitle', 'subcategoryTitleEn'):
                base[key] = c[key]
            base['v12Extension'] = {'stages': len(stages), 'steps': sum(len(st['steps']) for st in stages),
                                    'workedExample': c['workedExample'], 'focus': c['focus'], 'focusEn': c['focusEn']}
            target = base
        else:
            target = {k: v for k, v in c.items() if k not in ('focus', 'focusEn')}
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
        assert target['stepCount'] == (c['existingStepCount'] + 32 if c.get('extendsExisting') else 32), cid
    featured = [fby[c['id']] for c in featured] + [fby[cid] for cid in new_order]
    by = {c['id']: c for c in featured}

    # Slim catalog entries (no stages).
    out_catalog = []
    for entry in catalog:
        if entry['id'] in courses:
            full = by[entry['id']]
            slim = {k: v for k, v in full.items() if k not in ('stages', 'v12Extension')}
            if courses[entry['id']].get('extendsExisting'):
                slim = {**entry, 'stepCount': full['stepCount'], 'estimatedMinutes': full['estimatedMinutes'],
                        'sourceIds': full['sourceIds'], 'enrichmentVersion': 12, 'status': 'guided',
                        **{k: full[k] for k in ('learningTrack', 'learningSubdiscipline', 'learningTags', 'subcategory', 'subcategoryTitle', 'subcategoryTitleEn')}}
            out_catalog.append(slim)
        else:
            out_catalog.append(entry)
    for key in ('id', 'title', 'titleEn'):
        vals = [str(c[key]).casefold() for c in out_catalog]
        assert len(vals) == len(set(vals)), 'duplicate ' + key

    # Places and related comparisons.
    places = read(DATA / 'course-places.json'); pm = {p['courseId']: p for p in places['courses']}
    for p in o['places']:
        pm[p['courseId']] = p
    related = read(DATA / 'related-skills.json'); rm = {r['courseId']: r for r in related['courses']}
    for r in o['related']:
        for v in r['related']:
            assert v['id'] in by and v['id'] in pm, v['id']
            v['place'] = copy.deepcopy(pm[v['id']]['place'])
            v['why'] = v['transfer']; v['whyEn'] = v['transferEn']
        assert len(r['related']) == 2, r['courseId']
        rm[r['courseId']] = r
    assert set(pm) >= set(by) and set(rm) >= set(by), 'Every guided course needs places and comparisons'

    # Supplemental guide per course.
    media = read(DATA / 'media.json'); mm = {m['courseId']: m for m in media['courses']}
    for cid, c in courses.items():
        full = by[cid]
        new_steps = [s for st in full['stages'] if '-v12-' in st['id'] for s in st['steps']]
        entry = mm.setdefault(cid, {'courseId': cid, 'videos': [], 'guides': []})
        key = cid + '-v12-optics-guide'
        guide = {
            'id': key, 'title': '原理、算例與驗證：' + full['title'], 'titleEn': 'Principles, examples and verification: ' + full['titleEn'],
            'concept': c['summary'], 'conceptEn': c['summaryEn'],
            'procedure': [s['instruction'] for s in new_steps[::4]], 'procedureEn': [s['instructionEn'] for s in new_steps[::4]],
            'evidence': [s['check'] for s in new_steps[2::8]], 'evidenceEn': [s['checkEn'] for s in new_steps[2::8]],
            'pitfalls': [s['instruction'].split(' 師傅任務')[0] for s in new_steps[3::16]],
            'pitfallsEn': [s['instructionEn'].split(' Mentor task')[0] for s in new_steps[3::16]],
            'sourceIds': c['sourceIds'][-4:], 'sources': [copy.deepcopy(srcmap[i]) for i in c['sourceIds'][-4:]],
            'simulationOnly': True, 'scope': c['scope'], 'scopeEn': c['scopeEn'],
        }
        entry['guides'] = [g for g in entry.get('guides', []) if g['id'] != key] + [guide]
    media['courses'] = list(mm.values())

    # Vendors: companies + course associations.
    vendors = read(DATA / 'vendors.json'); vm = {v['id']: v for v in vendors['vendors']}; am = {a['courseId']: a for a in vendors['courses']}
    by_name = {v.get('nameEn', v['name']).casefold(): v['id'] for v in vm.values()}
    rename = {}
    for comp in o['companies']:
        existing = by_name.get(comp['nameEn'].casefold())
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
                   'connection': f'從「{by[cid]["title"]}」的元件、量測或系統整合延伸到下列廠商與機構的官方資料；這是教材關聯，不代表合作、採購或背書。',
                   'connectionEn': f'Explore official information from companies and institutions related to the components, measurements or system integration of {by[cid]["titleEn"]}. This is a learning association, not a partnership, procurement or endorsement.'}
    vendors.update(version=12, reviewed='2026-10-15', vendors=list(vm.values()), courses=list(am.values()))

    for name, value in [('featured', featured), ('catalog', out_catalog), ('sources', sources),
                        ('course-places', {**places, 'version': 12, 'courses': list(pm.values())}),
                        ('related-skills', {**related, 'version': 12, 'courses': list(rm.values())}),
                        ('media', {**media, 'version': 12}), ('vendors', vendors)]:
        write(DATA / f'{name}.json', value)

    header = ['id', 'title_zh', 'title_en', 'category', 'subcategory_zh', 'subcategory_en', 'content_type', 'authored_steps', 'route']
    for filename, rows in [('catalog-index.csv', out_catalog), ('optics-precision-101.csv', [by[cid] for cid in courses])]:
        buf = io.StringIO(newline=''); w = csv.writer(buf, lineterminator='\n'); w.writerow(header)
        for c in rows:
            w.writerow([c['id'], c['title'], c['titleEn'], c['category'], c.get('subcategoryTitle', ''), c.get('subcategoryTitleEn', ''),
                        'guided' if c['id'] in by else 'research', c.get('stepCount', 0) if c['id'] in by else 0, '#project/' + c['id']])
        (DATA / filename).write_text(buf.getvalue(), 'utf-8-sig')

    allsteps = [s for c in featured for st in c['stages'] for s in st['steps']]
    optsteps = [s for cid in courses for st in by[cid]['stages'] if '-v12-' in st['id'] for s in st['steps']]
    release = read(DATA / 'release.json')
    release.update(version='12.0.0', date='2026-10-15', topics=len(out_catalog), guidedCourses=len(featured),
                   researchTopics=len(out_catalog) - len(featured), allSteps=len(allsteps),
                   knowledgePoints=sum(len(s['knowledge']) for s in allsteps), sources=len(sources),
                   opticsCourses=len(courses), opticsSteps=len(optsteps), opticsSubdisciplines=len({by[c].get('subcategory') for c in courses if not courses[c].get('extendsExisting')}),
                   courseHistories=len(pm), mapLocations=len(pm), curatedRelatedCourses=len(rm),
                   curatedComparisons=sum(len(r['related']) for r in rm.values()), mentorDemonstrations=len(allsteps),
                   narratedGuideSteps=len(allsteps), supplementalGuides=sum(len(m.get('guides', [])) for m in media['courses']),
                   industryEntities=len(vm), industryCourseAssociations=len(am), listedInstruments=sum(bool(v.get('security')) for v in vm.values()),
                   sharedInteractiveTasks=len(allsteps) - release.get('authoredInteractiveTasks', 52),
                   opticsScope='101 optics and precision-instrument curricula (99 new, asml and a405 extended): 8 authored units per course, each expanded into mechanism, quantitative, verification and failure-diagnosis steps. Original teaching exercises, not vendor recipes or operating procedures.')
    write(DATA / 'release.json', release)
    print(json.dumps({k: release[k] for k in ('topics', 'guidedCourses', 'allSteps', 'opticsCourses', 'opticsSteps', 'knowledgePoints', 'sources', 'industryEntities', 'listedInstruments')}, ensure_ascii=False))


if __name__ == '__main__':
    main()
