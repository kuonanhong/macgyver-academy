#!/usr/bin/env python3
"""Build reviewed course geography and V5 metadata, without network access."""
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
    for filename in ('technology.json', 'civil-systems.json'):
        group = read(ROOT/'tools/places'/filename)
        courses.extend(group if isinstance(group, list) else group['courses'])
    assert len(courses) == len({c['courseId'] for c in courses}) == 17
    assert {c['courseId'] for c in courses} <= {c['id'] for c in read(DATA/'featured.json')}
    sources = [s for s in read(DATA/'sources.json') if not s['id'].startswith('v5-place-')]
    seen = {s['url'] for s in sources}
    for course in courses:
        for field in ('summary','connection'):
            assert course[field] and course[field+'En'], (course['courseId'],field)
        place = course['place']
        assert -90 <= place['lat'] <= 90 and -180 <= place['lng'] <= 180
        for field in ('name','city','country'):
            assert place[field] and place[field+'En']
        assert place['mapQuery'] and len(course['history']) >= 2 and len(course['references']) >= 2
        for event in course['history']:
            assert event['year']
            for field in ('title','text'):
                assert event[field] and event[field+'En']
        for ref in course['references']:
            assert ref['url'].startswith('https://')
            if ref['url'] in seen:
                continue
            seen.add(ref['url'])
            sources.append({'id':'v5-place-'+hashlib.sha256(ref['url'].encode()).hexdigest()[:12],
                'title':ref['title'],'titleEn':ref.get('titleEn',ref['title']),'publisher':ref['publisher'],'url':ref['url'],
                'scope':'支持本工程歷史與代表性據點的教學介紹；不代表完整製造供應鏈或施工規範。',
                'scopeEn':'Supports the educational history and representative location, not a complete supply chain or construction specification.'})
    write(DATA/'course-places.json', {'version':5,'courses':courses,
        'scope':'Representative public engineering locations and original bilingual histories, not exclusive manufacturing locations.'})
    write(DATA/'sources.json',sources)
    release = read(DATA/'release.json')
    release.update(version='5.0.0', sources=len(sources), courseHistories=len(courses),
        mapLocations=len(courses), narratedGuideSteps=release['allSteps'],
        narrationScope='Native device speech; two authored core languages; other languages need configured translation and a matching installed voice. Text guidance is always available.',
        videoScope='YouTube needs network and a real HTTP(S) player context. Local files use a configurable HTTPS player; authentication, browser settings and publisher restrictions still apply.')
    write(DATA/'release.json',release)
    print(json.dumps({'courses':len(courses),'historyEvents':sum(len(c['history']) for c in courses),'sources':len(sources)}))

if __name__ == '__main__':
    main()
