#!/usr/bin/env python3
"""Verify just this reviewer group using the release gate's arithmetic evaluator."""
import json,math,runpy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
G=runpy.run_path(str(ROOT/'tools/validate-review-snapshots-v15.py'))
H=ROOT/'tools/water-v15';p=H/'reviews/peer_landmarks.json';r=json.loads(p.read_text())
assert r['status']=='PASS' and r['nonAuthorReviewer'] is True and r['reviewer']=='/root/courses_landmarks'
ids={f'b{i}' for i in range(221,241)};inputs={cid:json.loads((H/'inputs'/f'{cid}.json').read_text()) for cid in ids}
seen=set();values=0
for row in r['rows']:
 cid=row['courseId'];j=row['unit'];key=(cid,j);assert cid in ids and 1<=j<=10 and key not in seen;seen.add(key)
 u=inputs[cid]['units'][j-1];assert row['status']=='PASS'
 assert row['modelSha256']==G['sha'](u['model'].encode())
 assert row['quizSha256']==G['sha'](u['misconception'].encode())
 cols=[row[k] for k in ['expression','actual','expected','tolerance']]
 records=zip(*cols) if isinstance(cols[0],list) else [cols]
 for expr,actual,expected,tol in records:
  result=G['evaluate'](expr);assert math.isclose(result,actual,rel_tol=1e-11,abs_tol=1e-11)
  assert abs(result-expected)<=tol+1e-12*max(1,abs(result));values+=1
assert seen=={(cid,j) for cid in ids for j in range(1,11)}
assert len(r['courses'])==20
sensitivities=0;sensitivity_values=0
for c in r['courses']:
 cid=c['courseId'];d=inputs[cid];assert c['status']=='PASS'
 assert c['inputSha256']==G['sha']((H/'inputs'/f'{cid}.json').read_bytes())
 assert c['metadataSha256']==G['metadata_hash'](d)
 assert set(c['sourceURLs'])=={s['url'] for s in d['sources']}
 s=c['sensitivityReview'];assert s['status']=='PASS' and s['exampleSha256']==G['sha'](d['example'].encode())
 for expr,a,e,t in zip(s['expression'],s['actual'],s['expected'],s['tolerance']):
  value=G['evaluate'](expr);assert math.isclose(value,a,rel_tol=1e-11,abs_tol=1e-11)
  assert abs(value-e)<=t+1e-12*max(1,abs(value));sensitivity_values+=1
 sensitivities+=1
assert sensitivities==20
print(json.dumps(dict(status='PASS',courses=20,models=len(seen),numericValues=values,quizReviews=len(seen),metadata=20,exampleSensitivities=sensitivities,sensitivityValues=sensitivity_values,reportSha256=G['sha'](p.read_bytes()))))
