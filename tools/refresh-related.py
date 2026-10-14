#!/usr/bin/env python3
"""Assemble reviewed transfer-learning data without network access."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'public/academy/data'

def read(path):
    return json.loads(path.read_text(encoding='utf-8'))

def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

def main():
    courses = []
    for group in ('semiconductor', 'civil', 'systems'):
        courses.extend(read(ROOT / 'tools/related' / f'{group}.json')['courses'])
    course_ids = {c['id'] for c in read(DATA / 'featured.json')}
    catalog_ids = {c['id'] for c in read(DATA / 'catalog.json')}
    assert len(courses) == len({c['courseId'] for c in courses}) == 17
    assert {c['courseId'] for c in courses} <= course_ids
    sources = [s for s in read(DATA/'sources.json') if not s['id'].startswith('v4-related-')]
    seen = {s['url'] for s in sources}
    for course in courses:
        assert course['overview'] and course['overviewEn']
        refs = {r['url'] for r in course['references']}
        assert len(refs) >= 3
        for related in course['related']:
            assert related.get('id') is None or related['id'] in catalog_ids, related
            for key in ('title','why','transfer','difference','practice'):
                assert related[key] and related[key+'En'], (course['courseId'], key)
            assert len(related['practice']) == len(related['practiceEn']) == 3
            assert set(related['referenceUrls']) <= refs
        for ref in course['references']:
            assert ref['url'].startswith('https://')
            if ref['url'] in seen:
                continue
            seen.add(ref['url'])
            sources.append({'id':'v4-related-'+hashlib.sha256(ref['url'].encode()).hexdigest()[:12],
                            'title':ref['title'],'titleEn':ref.get('titleEn',ref['title']),'publisher':ref['publisher'],'url':ref['url'],
                            'scope':ref['scope'], 'scopeEn':ref['scopeEn']})
    related_count = sum(len(c['related']) for c in courses)
    reference_count = len({r['url'] for c in courses for r in c['references']})
    write(DATA/'related-skills.json',{'version':4,'courses':courses,
        'scope':'Curated comparisons for 17 guided courses. Other catalogue topics receive clearly labelled same-category navigation suggestions.'})
    write(DATA/'sources.json',sources)
    release = read(DATA/'release.json')
    coverage = read(ROOT/'docs/EXERCISE_COVERAGE_V3.json')
    # V6 promotions are merged after these legacy comparisons. Their current
    # coverage is computed from the full curriculum by integrate-expansion.py.
    release.update(version='4.0.0',sources=len(sources),curatedRelatedSkills=related_count,
                   relatedReferenceUrls=reference_count,mentorDemonstrations=release['allSteps'],
                   authoredInteractiveTasks=coverage['authored'],sharedInteractiveTasks=coverage['shared'],
                   exerciseSceneFamilies=coverage['sceneFamilies'],
                   offlineEntry='index.html',demoScope='Teaching animations derived from exercise models; not a manufacturing digital twin.')
    write(DATA/'release.json',release)
    print(json.dumps({'courses':len(courses),'relatedSkills':related_count,'uniqueReferences':reference_count,'totalSources':len(sources)}))

if __name__ == '__main__':
    main()
