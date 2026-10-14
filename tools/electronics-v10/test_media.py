#!/usr/bin/env python3
"""Verify V10 artifact provenance, coverage and executable-content boundaries."""
import json,hashlib,re,xml.etree.ElementTree as ET
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
m=json.loads((HERE/'media.json').read_text());base=json.loads((HERE/'media-course-baseline.json').read_text());ids={c['id']for c in base};assert len(ids)==199;assert {c['courseId']for c in m['courses']}==ids
sourceids={s['id']for s in json.loads((HERE/'media-source-baseline.json').read_text())}|{s['id']for s in m['sources']}
assert len(m['photos'])==31;shas=set()
for p in m['photos']:
 assert re.fullmatch(r'assets/photos/v10-[a-z0-9-]+\.(jpg|png)',p['path']),p['path']
 assert p['license'].startswith(('CC BY','CC0'))or p['license']=='Public domain';assert 'NC'not in p['license']
 assert all(p[k]for k in ['author','licenseUrl','sourceUrl','changes','note','noteEn'])
 path=ROOT/'public/academy'/p['path'];Image.open(path).verify();sha=hashlib.sha256(path.read_bytes()).hexdigest();assert sha==p['sha256'];assert sha not in shas;shas.add(sha)
 assert set(p['courseIds'])==set(p['courseContext'])
svgs=set();voices=set();guideids=set()
for c in m['courses']:
 assert len(c['guides'])==1 and c['videos'];g=c['guides'][0];assert g['id']not in guideids;guideids.add(g['id']);assert set(g['sourceIds'])<=sourceids
 for k in ['title','concept','procedure','evidence','pitfalls']:
  assert g[k] and g[k+'En']
 d=g['diagram'];assert d['original']and d['notToScale']
 for k in ['path','pathEn']:
  assert re.fullmatch(r'assets/diagrams/v10-[a-z0-9-]+\.svg',d[k]);p=ROOT/'public/academy'/d[k];ET.parse(p);s=p.read_text();assert not any(x in s.lower() for x in ['<script', 'foreignobject', 'onload=', 'javascript:', 'https://'])
  # Explicitly disallow external references and event handlers despite the required XML namespace.
  assert not re.search(r'\b(?:href|onload|onclick|onerror)\s*=',s,re.I)
  assert c['courseId'].upper()in s;assert p.name not in svgs;svgs.add(p.name)
 for v in c['videos']:
  assert re.fullmatch(r'[A-Za-z0-9_-]{11}',v['youtubeId']);assert v['embedUrl']=='https://www.youtube-nocookie.com/embed/'+v['youtubeId']
  assert v.get('watchFor')and v.get('watchForEn');assert not v['verification'].get('playbackTested');voices.add(v['youtubeId'])
assert len(svgs)==398 and len(voices)==9
print('PASS: 199-course coverage, 31 unique licensed rasters, 398 safe bilingual SVG maps, 9 scoped video IDs (7 new), source references and exact asset hashes.')
