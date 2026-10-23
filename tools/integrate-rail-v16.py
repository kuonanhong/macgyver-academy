#!/usr/bin/env python3
"""Integrate the V16 rail and transport curricula (鐵道與交通工程 100 courses).

Run after tools/rail-v16/build_rail.py. Repeatable: previously
integrated V16 rail content is replaced, earlier editions are preserved,
and the existing step IDs of `b301` keep their
order (40 new steps are appended).
"""
import copy, csv, io, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'public/academy/data'
SRC = ROOT / 'tools/rail-v16/rail.json'
TAG = '-v16-'
NEW_STEPS = 40
DATE = '2026-10-23'


def read(p):
    return json.loads(p.read_text('utf-8'))


def write(p, value):
    text = json.dumps(value, ensure_ascii=False, **({'separators': (',', ':')} if p.name == 'featured.json' else {'indent': 2})) + '\n'
    tmp = p.with_suffix(p.suffix + '.tmp'); tmp.write_text(text, 'utf-8'); tmp.replace(p)


def strip_v16(course):
    """Remove previously integrated V16 stages so the script can be rerun."""
    course['stages'] = [st for st in course.get('stages', []) if TAG not in st['id']]
    return course


def main():
    o = read(SRC)
    courses = {c['id']: c for c in o['courses']}
    partial = '--allow-partial' in sys.argv  # development only: integrate the inputs written so far
    assert partial or len(courses) == 100, f'expected 100 rail courses, got {len(courses)}'
    featured = read(DATA / 'featured.json')
    catalog = read(DATA / 'catalog.json')
    sources = [s for s in read(DATA / 'sources.json') if not s['id'].startswith('v16s-')]
    srcmap = {s['id']: s for s in sources}
    for s in o['sources']:
        srcmap[s['id']] = {**srcmap.get(s['id'], {}), **s}
    sources = list(srcmap.values())

    fby = {c['id']: c for c in featured}
    new_order = []
    for cid, c in courses.items():
        if c.get('extendsExisting'):
            base = strip_v16(fby[cid])
            old_ids = [s['id'] for st in base['stages'] for s in st['steps']]
            assert len(old_ids) == c['existingStepCount'], (cid, len(old_ids), c['existingStepCount'])
            stages = copy.deepcopy(c['newStages'])
            stages[0]['steps'][0]['prerequisiteIds'] = [old_ids[-1]]
            base['stages'] = base['stages'] + stages
            base['sourceIds'] = c['sourceIds']
            base['enrichmentVersion'] = 16
            for key in ('learningTrack', 'learningSubdiscipline', 'learningTags', 'subcategory', 'subcategoryTitle', 'subcategoryTitleEn'):
                base[key] = c[key]
            # Keep the course's authored identity artwork; the V16 architecture is used only by the new steps' workbench.
            base['v16Architecture'] = {k: c[k] for k in ('architectureFamily', 'architectureNodes', 'architectureEdges')}
            base['v16Extension'] = {'stages': len(stages), 'steps': sum(len(st['steps']) for st in stages),
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
            if TAG in st['id']: st['order'] = i + 1
            for j, s in enumerate(st['steps']):
                number += 1
                if TAG in st['id']:
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
            slim = {k: v for k, v in full.items() if k not in ('stages', 'v12Extension', 'v16Extension', 'v16Architecture', 'dossier')}
            if courses[entry['id']].get('extendsExisting'):
                slim = {**entry, 'stepCount': full['stepCount'], 'estimatedMinutes': full['estimatedMinutes'],
                        'sourceIds': full['sourceIds'], 'enrichmentVersion': 16, 'status': 'guided',
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
            keep = [h for h in prev.get('history', []) if not h.get('v16')]
            add = [{**h, 'v16': True} for h in p['history'] if h['year'][:1].isdigit()]
            prev['history'] = keep + add
            refs = {r['url']: r for r in prev.get('references', []) if not r.get('v16')}
            for r in p['references']:
                refs.setdefault(r['url'], {**r, 'v16': True})
            prev['references'] = list(refs.values())
            prev['sourceIds'] = list(dict.fromkeys([sid for sid in prev.get('sourceIds', []) if not sid.startswith('v16s-') and sid not in p['sourceIds']] + p['sourceIds']))
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
        key, dkey = cid + '-v16-rail-guide', cid + '-v16-dossier'
        refs = [copy.deepcopy(srcmap[i]) for i in c['sourceIds'][-5:]]
        guide = {
            'id': key, 'title': '機制、算例與驗證：' + full['title'], 'titleEn': 'Mechanisms, calculations and verification: ' + full['titleEn'],
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
            'concept': c['focus'] + '。本頁區分公開工程資料與明示的教學假設；數值只用於學習比較，不是設計值。',
            'conceptEn': c['focusEn'] + '. This dossier distinguishes public project facts from explicitly labelled teaching assumptions; figures are for learning comparisons, not design values.',
            'facts': book['facts'], 'factsEn': book['factsEn'],
            'timeline': book['timeline'], 'timelineEn': book['timelineEn'],
            'codes': book['codes'], 'codesEn': book['codesEn'],
            'landmarks': book['landmarks'], 'landmarksEn': book['landmarksEn'],
            'procedure': ['把關鍵數據與本課算例逐項對照，標出哪些是公開工程數據、哪些是教學假設。',
                          '沿著工程時間軸，標出設計、施工、事件與維護改造的關鍵決策點，說明每個決策改變了哪一條系統路徑或檢核。',
                          '對照列出的規範與標準，找出本課試驗或允收步驟對應的條款類型，並註明版本與適用地區。',
                          '從代表工程中選一個與本課比較，列出軌距與限界、運輸需求、供電與號誌以及施工方法的差異。'],
            'procedureEn': ['Compare the key figures with this course\'s worked example and mark which are public project data and which are teaching assumptions.',
                            'Along the timeline, mark the key design, construction, event and retrofit decisions and say which system path or check each one changed.',
                            'Against the listed codes and standards, find the kind of clause behind this course\'s tests or acceptance steps, noting edition and jurisdiction.',
                            'Pick one landmark project to compare with this course and list differences in gauge and clearance, service demand, power, signalling and construction methods.'],
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
            ids.append(vid); roles.append({'vendorId': vid, 'role': link['role'], 'roleEn': link['roleEn'], 'business': link.get('business', ''), 'businessEn': link.get('businessEn', ''), 'productUrl': vm[vid]['url'], 'v16': True})
        prev = am.get(cid)
        # Retain the original association explicitly, so later edits can replace
        # V16 roles without accumulating obsolete links or reordering on reruns.
        baseline = copy.deepcopy(prev.get('v16Base', {'vendorIds': prev['vendorIds'], 'roles': prev.get('roles', [])})) if prev else {'vendorIds': [], 'roles': []}
        ids = list(dict.fromkeys(baseline['vendorIds'] + ids))
        roles = [r for r in baseline['roles'] if r['vendorId'] not in {x['vendorId'] for x in roles}] + roles
        am[cid] = {'courseId': cid, 'vendorIds': ids, 'roles': roles, 'v16Base': baseline,
                   'connection': f'從「{by[cid]["title"]}」的材料、構件、施工或監測延伸到下列公司、業主與機構的官方資料；這是教材關聯，不代表合作、採購或背書。',
                   'connectionEn': f'Explore official information from companies, owners and institutions related to the materials, members, construction or monitoring of {by[cid]["titleEn"]}. This is a learning association, not a partnership, procurement or endorsement.'}
    vendors.update(version=16, reviewed=DATE, vendors=list(vm.values()), courses=list(am.values()))

    for name, value in [('featured', featured), ('catalog', out_catalog), ('sources', sources),
                        ('course-places', {**places, 'version': 16, 'courses': list(pm.values())}),
                        ('related-skills', {**related, 'version': 16, 'courses': list(rm.values())}),
                        ('media', {**media, 'version': 16}), ('vendors', vendors)]:
        write(DATA / f'{name}.json', value)

    header = ['id', 'title_zh', 'title_en', 'category', 'subcategory_zh', 'subcategory_en', 'content_type', 'authored_steps', 'route']
    for filename, rows in [('catalog-index.csv', out_catalog), ('rail-transport-100.csv', [by[cid] for cid in courses])]:
        buf = io.StringIO(newline=''); w = csv.writer(buf, lineterminator='\n'); w.writerow(header)
        for c in rows:
            w.writerow([c['id'], c['title'], c['titleEn'], c['category'], c.get('subcategoryTitle', ''), c.get('subcategoryTitleEn', ''),
                        'guided' if c['id'] in by else 'research', c.get('stepCount', 0) if c['id'] in by else 0, '#project/' + c['id']])
        (DATA / filename).write_text(buf.getvalue(), 'utf-8-sig')

    allsteps = [s for c in featured for st in c['stages'] for s in st['steps']]
    ststeps = [s for cid in courses for st in by[cid]['stages'] if TAG in st['id'] for s in st['steps']]
    release = read(DATA / 'release.json')
    release.update(version='16.0.0', date=DATE, topics=len(out_catalog), guidedCourses=len(featured),
                   researchTopics=len(out_catalog) - len(featured), allSteps=len(allsteps),
                   knowledgePoints=sum(len(s['knowledge']) for s in allsteps), sources=len(sources),
                   railCourses=len(courses), railSteps=len(ststeps),
                   railSubdisciplines=len({by[c].get('subcategory') for c in courses}),
                   railDossiers=len(courses),
                   newGuidedCourses=99 if len(courses)==100 else sum(not c.get('extendsExisting') for c in courses.values()), newGuidedSteps=len(ststeps),
                   railOriginalDiagrams=len(courses), railOriginalSvgFiles=3*len(courses),
                   railInteractiveModels=0, railExecutableMiniLabs=0, executableMiniLabs=24,
                   newOriginalMediaSvgFiles=3*len(courses), newOriginalArchitectureSvgFiles=2*len(courses), newOriginalIconSvgFiles=len(courses),
                   learningMapTracks=22, learningMapBranches=80, learningMapRoutes=28,
                   aiRoutesScope='Configurable server-side OpenAI-compatible, Claude Messages, Gemini text/image, local Ollama CPU and explicitly loaded browser CPU text. Provider keys and large model weights are not bundled.',
                   languageScope='79 selectable language targets detected from browser preferences. Authored Traditional Chinese and English curricula; other full text needs configured translation, an explicitly loaded local model or supported browser translator. Completion state is reported; no claim of 79 fully reviewed offline translations.',
                   lazyLoadingScope='Homepage HTML first; slim catalogue then per-course lessons/resources and route-specific auxiliary data, with hashed JSON and file-mode scripts.',
                   courseHistories=len(pm), mapLocations=len(pm), curatedRelatedCourses=len(rm),
                   curatedComparisons=sum(len(r['related']) for r in rm.values()), mentorDemonstrations=len(allsteps),
                   narratedGuideSteps=len(allsteps), supplementalGuides=sum(len(m.get('guides', [])) for m in media['courses']),
                   industryEntities=len(vm), industryCourseAssociations=len(am), listedInstruments=sum(bool(v.get('security')) for v in vm.values()),
                   listedCompanies=sum(bool(v.get('security')) for v in vm.values()),
                   sharedInteractiveTasks=len(allsteps) - release.get('authoredInteractiveTasks', 52),
                   railScope='100 rail-and-transport curricula (99 new, b301 extended): 10 authored units per course, each expanded into mechanism, quantitative, verification and failure-diagnosis steps, plus a dossier of key figures, timeline, codes and landmark comparisons. Original teaching exercises, not design documents, method statements or work permits.')
    release.update(actualPhotos=len(read(DATA / 'photos.json')), newLicensedPhotos=11,
                   scenePhotoAssignments=2066, exactScenePhotoAssignments=11, representativeScenePhotoAssignments=2055, uniqueGuidedCourseIcons=len(featured),
                   categoryIcons=20, totalProjectIcons=2066, immersiveWarmupModels=10,
                   immersiveViewModes=3, ownerRole='server-verified owner; no purchase required',
                   photography='129 licensed photographs with author/license records; 11 newly verified primary-source records. Scene mappings clearly distinguish exact project photographs from representative imagery.',
                   demoScope='Photographic references with original projected 3D teaching equipment and ten simplified warmup models; not a calibrated or sensor-connected digital twin.',
                   projectVisualScope='Unique colorful geometry for all 1003 guided course icons and 20 category icons. 2066 topic icon files in total; unexpanded research topics can share geometry. 200 bilingual railway system relationship SVGs.',
                   lazyLoadingScope='HTML shell first; compact metadata next; only the free first stage when a visitor opens a course. Scene code/photos and resources load on demand. Authorized full courses use uncached server requests; full offline owner preview is explicit.')
    write(DATA / 'release.json', release)
    version_path=ROOT / 'SOURCE_VERSION.json'
    if read(version_path).get('version') != '16.0.0':
        prior=ROOT / 'docs/SOURCE_VERSION_PRE_V16.json'
        if not prior.exists(): prior.write_bytes(version_path.read_bytes())
    write(version_path, {'version':'16.0.0', 'date':DATE,
          'upstream':'https://github.com/kuonanhong/macgyver-academy',
          'base':{'version':'15.0.0', 'archive':'MacGyver_Engineering_Academy_v15.zip',
                  'sha256':'21b11b7ed0db9d7619831ba19da93b6843f1aa70ca6c12873fb5db5049cf8900'},
          'release':release})
    print(json.dumps({k: release[k] for k in ('topics', 'guidedCourses', 'allSteps', 'railCourses', 'railSteps', 'knowledgePoints', 'sources', 'industryEntities', 'listedCompanies')}, ensure_ascii=False))


if __name__ == '__main__':
    main()
