#!/usr/bin/env python3
"""Merge reviewed V6 course promotions into the existing 2,000-topic catalog.

Never invent additional topic IDs, photographs, factory recipes or rankings.
The authored JSON files are reviewable source, not a scrape performed at runtime.
"""
import csv
import io
import json
import subprocess
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'public/academy/data'
GROUPS = ('technology', 'civil', 'mobility', 'science')

def read(path):
    return json.loads(path.read_text(encoding='utf-8'))

def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def main():
    catalog = read(DATA/'catalog.json')
    catalog_ids = {c['id'] for c in catalog}
    category_counts=Counter(c['category'] for c in catalog)
    assert len(catalog) == len(catalog_ids) == 2000
    groups = [read(ROOT/'tools/expansion'/f'{name}.json') for name in GROUPS]
    additions = [c for g in groups for c in g['courses']]
    added_ids = {c['id'] for c in additions}
    assert len(additions) == len(added_ids) == 20
    assert added_ids <= catalog_ids
    assert len({c['category'] for c in additions}) == 20
    sources = {s['id']: s for s in read(DATA/'sources.json')}
    for g in groups:
        for source in g['sources']:
            assert source['url'].startswith('https://'), source['id']
            if source['id'] in sources:
                assert source['url'] == sources[source['id']]['url'], source['id']
            sources[source['id']] = source
    for course in additions:
        course.update(status='guided', kind='course', depth=4,
                      contentStatus='reviewable-educational-curriculum',
                      languageCoverage=['zh-TW','en'], curriculumVersion=6)
        steps = [s for stage in course['stages'] for s in stage['steps']]
        assert len(course['stages']) == 3 and len(steps) == 12, course['id']
        assert len({s['id'] for s in steps}) == 12
        assert len({s['instruction'] for s in steps}) == 12
        course['stepCount'] = len(steps)
        course['estimatedMinutes'] = sum(s.get('estimatedMinutes', 15) for s in steps)
        for key in ('title','summary','scope'):
            assert course[key].strip() and course[key+'En'].strip()
        for i, step in enumerate(steps):
            for key in ('title','objective','instruction','observation','failure','check'):
                assert step[key].strip() and step[key+'En'].strip(), (step['id'],key)
            assert step['simulationOnly'] is True
            assert len(step['knowledge']) >= 2
            assert step['sourceIds'] and set(step['sourceIds']) <= sources.keys()
            assert set(step.get('prerequisiteIds',[])) <= {s['id'] for s in steps[:i]}, step['id']
            step['sequence'] = i + 1
            q = step['quiz']
            assert len(q['options']) == len(q['optionsEn']) == 3
            assert 0 <= q['answer'] < 3
        assert set(course['sourceIds']) <= sources.keys()
    featured = [c for c in read(DATA/'featured.json') if c['id'] not in added_ids and c.get('curriculumVersion',0) < 7] + additions
    assert len(featured) == 37
    by_id = {c['id']:c for c in featured}
    for i, entry in enumerate(catalog):
        if entry['id'] in by_id:
            catalog[i] = {k:v for k,v in by_id[entry['id']].items() if k != 'stages'}
    assert Counter(c['category'] for c in catalog)==category_counts, 'Promotions preserve topic categories'
    for key in ('id','title','titleEn'):
        assert len({c[key].casefold() for c in catalog}) == 2000, key
    places = read(DATA/'course-places.json')
    places['courses'] = [p for p in places['courses'] if p['courseId'] not in added_ids and p['courseId'] in by_id] + [p for g in groups for p in g['places']]
    assert len(places['courses']) == 37
    assert {p['courseId'] for p in places['courses']} == by_id.keys()
    places['version'] = 6
    for place in places['courses']:
        assert len(place['history']) >= 2 and len(place['references']) >= 2
    media=read(DATA/'media.json')
    additional_media=read(ROOT/'tools/expansion/media.json')['courses']
    media_ids={entry['courseId'] for entry in additional_media}
    media['courses']=[entry for entry in media['courses'] if entry['courseId'] not in media_ids]+additional_media
    media['version']=6
    for entry in additional_media:
        assert entry['courseId'] in by_id
        for video in entry['videos']:
            source_id='v6-video-'+video['youtubeId']
            sources[source_id]={'id':source_id,'title':video['title'],'titleEn':video['titleEn'],
                'publisher':video['publisher'],'url':video['sourcePage'],'scope':video['scope'],'scopeEn':video['scopeEn']}
            if source_id not in by_id[entry['courseId']]['sourceIds']:
                by_id[entry['courseId']]['sourceIds'].append(source_id)
    write(DATA/'media.json',media)
    write(DATA/'featured.json',featured)
    write(DATA/'catalog.json',catalog)
    write(DATA/'sources.json',list(sources.values()))
    write(DATA/'course-places.json',places)
    photo_file=ROOT/'tools/expansion/photos.json'
    photos=read(DATA/'photos.json')
    if photo_file.exists():
        added_photos=read(photo_file)
        if isinstance(added_photos,dict):
            added_photos=added_photos['photos']
        photos=[p for p in photos if not p['id'].startswith('v6-')]+added_photos
        assert len({p['id'] for p in photos})==len(photos)
        for p in added_photos:
            assert p['id'].startswith('v6-') and (ROOT/'public/academy'/p['path']).is_file()
            assert p['author'] and p['license'] and p['licenseUrl'] and p['sourceUrl']
            assert set(p['courseIds']) <= by_id.keys()
        write(DATA/'photos.json',photos)
        license_path=ROOT/'public/academy/assets/photos/LICENSES.txt'
        before=license_path.read_text(encoding='utf-8').split('\nV6 ADDITIONAL PHOTOGRAPHS\n')[0]
        license_path.write_text(before+'\nV6 ADDITIONAL PHOTOGRAPHS\n\n'+'\n\n'.join(p['id']+'\n'+p.get('attribution',p['author'])+'\nSource: '+p['sourceUrl']+'\nLicense: '+p['licenseUrl']+'\nChanges: '+p.get('changes','None') for p in added_photos)+'\n',encoding='utf-8')
    # Exercise test exercises every released step, and exports exact coverage.
    coverage = json.loads(subprocess.check_output(['node','tools/test-process-exercises.mjs'],cwd=ROOT,text=True))
    write(ROOT/'docs/EXERCISE_COVERAGE_V6.json',coverage)
    steps = [s for c in featured for stage in c['stages'] for s in stage['steps']]
    release = read(DATA/'release.json')
    release.update(version='6.0.0',date='2026-10-13',topics=2000,
        guidedCourses=len(featured),researchTopics=2000-len(featured),
        researchCheckpointsPerTopic=8,researchScope='Discipline-specific research worksheets; not authored manufacturing instructions.',
        allSteps=len(steps),knowledgePoints=sum(len(s['knowledge']) for s in steps),
        sources=len(sources),actualPhotos=len(photos),courseHistories=len(places['courses']),mapLocations=len(places['courses']),
        videoResources=sum(len(c['videos']) for c in media['courses']),
        embeddedVideos=sum(bool(v.get('embedUrl') or v.get('nativeVideoUrl')) for c in media['courses'] for v in c['videos']),
        mentorDemonstrations=len(steps),narratedGuideSteps=len(steps),
        authoredInteractiveTasks=coverage['authored'],sharedInteractiveTasks=coverage['shared'],exerciseSceneFamilies=coverage['sceneFamilies'],
        videoPlayerUrl='https://macgyver-public-player.kuonanhong.chatgpt.site/video-player.html',
        videoScope='A separate public HTTPS player removes academy/ChatGPT authentication from file-mode playback. YouTube, publisher, network and browser restrictions still apply.',
        catalogScope='Curated representative topics, not a verified global top-500/top-1000 ranking; includes historical antecedents predating the last century.')
    write(DATA/'release.json',release)
    output=io.StringIO(newline='')
    writer=csv.writer(output)
    writer.writerow(['id','title_zh','title_en','category','content_type','authored_steps','research_checkpoints','route'])
    for c in catalog:
        ready=c['id'] in by_id
        row=[c['id'],c['title'],c['titleEn'],c['category'],'guided' if ready else 'research',c.get('stepCount',0) if ready else 0,0 if ready else 8,'#project/'+c['id']]
        writer.writerow(["'"+v if isinstance(v,str) and v.startswith(('=','+','-','@')) else v for v in row])
    (DATA/'catalog-index.csv').write_text(output.getvalue(),encoding='utf-8-sig')
    print(json.dumps({k:release[k] for k in ('topics','guidedCourses','researchTopics','allSteps','knowledgePoints','sources','authoredInteractiveTasks','mapLocations')},ensure_ascii=False))

if __name__ == '__main__':
    main()
