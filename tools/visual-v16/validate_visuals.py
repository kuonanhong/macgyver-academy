#!/usr/bin/env python3
"""Offline acceptance checks for shipped V16 icons and real-photo manifests.

This validator does not import the generators. It independently inspects every
shipped SVG, file digest, course assignment and new Commons provenance record.
"""
from pathlib import Path
import collections
import hashlib
import json
import re
import xml.etree.ElementTree as ET
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
PUBLIC = ROOT/'public/academy'
ALLOWED = {'svg','g','title','desc','path','rect','circle','ellipse','line','polyline','polygon','text'}
GEOMETRY = {'d','x','y','x1','x2','y1','y2','width','height','cx','cy','r','rx','ry','points'}

def read(path):
    return json.loads(path.read_text())

def asset(path):
    candidate = (PUBLIC/path).resolve()
    assert candidate.is_relative_to(PUBLIC.resolve()), 'Asset path escapes public root: '+path
    assert candidate.is_file(), 'Missing local asset: '+path
    return candidate

def vector_geometry(path):
    root = ET.parse(path).getroot()
    shapes = []
    def walk(node, parents=()):
        tag = node.tag.rsplit('}',1)[-1]
        assert tag in ALLOWED, (str(path), 'Unsafe/nonlocal SVG element', tag)
        for key,value in node.attrib.items():
            assert not key.lower().startswith('on'), (str(path), 'SVG event handler')
            assert not key.endswith('href'), (str(path), 'SVG external/reference dependency')
            assert 'url(' not in value.lower(), (str(path), 'SVG external style reference')
        if tag in {'title','desc','text'}:
            return
        transforms = parents + ((node.attrib['transform'],) if 'transform' in node.attrib else ())
        if tag in {'path','rect','circle','ellipse','line','polyline','polygon'}:
            attrs = tuple(sorted((key,re.sub(r'\s+',' ',value.strip())) for key,value in node.attrib.items() if key in GEOMETRY))
            shapes.append((tag,transforms,attrs))
        for child in node:
            walk(child,transforms)
    walk(root)
    assert shapes, 'Empty SVG: '+str(path)
    # Drawing order is irrelevant to uniqueness; color, text, ID, opacity,
    # style and metadata are deliberately absent.
    return hashlib.sha256(json.dumps(sorted(shapes),sort_keys=True).encode()).hexdigest()

def main():
    catalog = read(PUBLIC/'data/catalog.json')
    icons = read(PUBLIC/'data/icon-manifest-v16.json')
    scene = read(PUBLIC/'data/scene-photos-v16.json')
    photos = read(PUBLIC/'data/photos.json')
    required = {c['id'] for c in catalog if c.get('status')=='guided' or c['category']=='rail'}
    by_course = {c['id']:c for c in catalog}
    category_ids = {c['category'] for c in catalog}
    assert set(icons['icons']) == set(by_course), 'Project icon coverage mismatch'
    assert set(icons['categories']) == category_ids and len(category_ids)==20
    required_shapes = collections.defaultdict(list)
    all_shapes = set()
    for ident,item in icons['icons'].items():
        path = asset(item['path'])
        assert item['path']==f'assets/icons-v16/projects/{ident}.svg'
        assert hashlib.sha256(path.read_bytes()).hexdigest()==item['sha256'], (ident,'Icon digest')
        fingerprint = vector_geometry(path)
        all_shapes.add(fingerprint)
        if ident in required:
            required_shapes[fingerprint].append(ident)
    duplicate_required = [group for group in required_shapes.values() if len(group)>1]
    assert not duplicate_required, ('Repeated required topic geometry',duplicate_required)
    category_shapes = [vector_geometry(asset(item['path'])) for item in icons['categories'].values()]
    assert len(set(category_shapes))==20, 'Category geometry repeats'
    by_photo = {p['id']:p for p in photos}
    assert len(by_photo)==len(photos), 'Duplicate photo IDs'
    assert set(scene['courses']) == set(by_course), 'Scene course coverage mismatch'
    assert set(scene['categories']) == category_ids, 'Scene category coverage mismatch'
    assert {p['id']:p for p in scene['photos']}==by_photo, 'Embedded scene photos disagree with primary manifest'
    for photo in photos:
        path = asset(photo['path'])
        for field in ('author','license','licenseUrl','sourceUrl','changes'):
            assert photo.get(field), (photo['id'],'Missing attribution field',field)
        assert hashlib.sha256(path.read_bytes()).hexdigest()==photo['sha256'], (photo['id'],'Photo digest')
        with Image.open(path) as im:
            assert im.size==(photo['width'],photo['height']), (photo['id'],'Photo dimensions')
            im.verify()
    for ident,mapping in scene['courses'].items():
        assert mapping['photoId'] in by_photo and mapping['match'] in {'exact','representative'}, ident
        assert mapping['photoIds'][0]==mapping['photoId'], ident
        assert all(pid in by_photo for pid in mapping['photoIds']), ident
        assert mapping.get('note') and mapping.get('noteEn'), ident
    for cat,mapping in scene['categories'].items():
        assert mapping['photoId'] in by_photo and mapping['match']=='representative',cat
    selection = read(HERE/'photo-selection.json')
    for item in selection:
        photo = by_photo[item['id']]
        proof = read(ROOT/photo['provenance'])
        page = next(iter(proof['query']['pages'].values()))
        assert page['title'].replace('_',' ').casefold()==('File:'+item['file']).replace('_',' ').casefold(), (item['id'],'Wrong provenance source')
        info = page['imageinfo'][0]
        assert photo['sourceUrl']==info['descriptionurl'], (item['id'],'Source mismatch')
        assert photo['originalFileUrl']==info['url'] and photo['originalSha1']==info['sha1'], (item['id'],'Original mismatch')
        assert photo['license']==info['extmetadata']['LicenseShortName']['value'], (item['id'],'License mismatch')
    report = {
        'version':16,'status':'PASS','checked':'2026-10-23',
        'projectSvgsParsed':len(icons['icons']),'categories':len(category_shapes),
        'requiredTopics':len(required),'requiredGeometryUnique':len(required_shapes),
        'geometryUniqueAllTopics':len(all_shapes),'geometryExcludes':'Text, title, description, IDs, all color/style/opacity; normalized draw order.',
        'localPhotosVerified':len(photos),'newPrimarySourceProvenanceVerified':len(selection),
        'coursePhotoAssignments':len(scene['courses']),'categoryPhotoAssignments':len(scene['categories']),
        'photoMatchCounts':dict(collections.Counter(v['match'] for v in scene['courses'].values())),
        'limitations':['Geometry uniqueness is required for guided and railway courses; unexpanded backlog topics can share compositions.',
            'Photographs may be reused as explicitly labeled field references. They are not course-step-exclusive, current live views, or calibrated digital twins.',
            '118 inherited photos retain V15 author/license records; 11 new records have bundled primary-source API evidence.']}
    (HERE/'VALIDATION_VISUALS_V16.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=='__main__':
    main()
