#!/usr/bin/env python3
"""Rebuild the reviewed V3 media catalog; no network or automatic scraping."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'public/academy/data'
EDIT = ROOT / 'tools/media'

def read(path):
    return json.loads(path.read_text(encoding='utf-8'))

def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

courses = []
for name in ('media_semiconductor', 'media_civil', 'media_systems'):
    courses.extend(read(EDIT / (name + '.json'))['courses'])
assert len(courses) == len({c['courseId'] for c in courses}) == 17
enhancements = EDIT / 'additional_embeds.json'
if enhancements.exists():
    raw=read(enhancements)
    updates=raw.get('updates') if 'updates' in raw else [dict(value,courseId=course_id,videoId=video_id) for course_id,videos in raw.items() for video_id,value in videos.items()]
    for addition in updates:
        entry = next(c for c in courses if c['courseId'] == addition['courseId'])
        video = next(v for v in entry['videos'] if v['id'] == addition['videoId'])
        for key in ('embedUrl', 'nativeVideoUrl', 'nativeVideoType', 'url', 'sourcePage', 'title', 'titleEn', 'publisher'):
            if addition.get(key):
                video[key] = addition[key]
        video['playbackEvidence'] = addition.get('evidence', '')
write(DATA / 'media.json', {'version': 3, 'courses': courses,
    'scope': 'Project-level supporting material, not unique footage of every step. External media remains hosted by the publisher.'})

new_photos = read(EDIT / 'photos.json')
photos = [p for p in read(DATA / 'photos.json') if not p['id'].startswith('v3-')] + new_photos
write(DATA / 'photos.json', photos)
license_file = ROOT / 'public/academy/assets/photos/LICENSES.txt'
old_license = license_file.read_text(encoding='utf-8').split('\nV3 ADDITIONAL PHOTOGRAPHS\n')[0]
license_file.write_text(old_license + '\nV3 ADDITIONAL PHOTOGRAPHS\n\n' + '\n\n'.join(p['id']+'\n'+p['attribution']+'\nLicense: '+p['licenseUrl'] for p in new_photos)+'\n', encoding='utf-8')

sources = [s for s in read(DATA / 'sources.json') if not s['id'].startswith('v3-media-')]
seen = {s['url'] for s in sources}
for course in courses:
    refs = [{'title': v['title'], 'url': v['sourcePage'], 'publisher': v['publisher']} for v in course['videos']]
    refs += [s for guide in course['guides'] for s in guide.get('sources', [])]
    for source in refs:
        if source['url'] in seen:
            continue
        seen.add(source['url'])
        sources.append({'id': 'v3-media-' + hashlib.sha256(source['url'].encode()).hexdigest()[:12],
                        'title': source['title'], 'url': source['url'],
                        'publisher': source.get('publisher', 'Official educational reference'),
                        'scope': 'V3 專案教學影片或深化研習的一手來源；非逐工序影片或原廠 SOP。'})
write(DATA / 'sources.json', sources)

release = read(DATA / 'release.json')
release.update(version='3.0.0', date='2026-10-13', sources=len(sources), actualPhotos=len(photos),
               supplementalGuides=sum(len(c['guides']) for c in courses),
               videoResources=sum(len(c['videos']) for c in courses),
               embeddedVideos=sum(bool(v.get('embedUrl') or v.get('nativeVideoUrl')) for c in courses for v in c['videos']))
write(DATA / 'release.json', release)
print(json.dumps({k: release[k] for k in ('version','sources','actualPhotos','supplementalGuides','videoResources','embeddedVideos')}, ensure_ascii=False))
