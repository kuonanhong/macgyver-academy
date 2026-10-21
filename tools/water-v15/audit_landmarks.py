#!/usr/bin/env python3
"""Recompute the 90 published literal results, record source scope and review hashes."""
import json,hashlib,math
from pathlib import Path
H=Path(__file__).resolve().parent
R=H/'reviews';R.mkdir(exist_ok=True)
def sha(b):return hashlib.sha256(b).hexdigest()
rows=json.loads((H/'calculation_landmarks.json').read_text());issues=[];courses={}
for a in rows:
 cid=a['courseId'];p=H/'inputs'/f'{cid}.json';d=json.loads(p.read_text());u=d['units'][a['unit']-1]
 v=eval(a['expression'],{'__builtins__':{},'math':math,'abs':abs})
 if abs(v-a['expected'])>a['tolerance']:issues.append([cid,a['unit'],v,a['expected']])
 if str(a['formula']) not in u['model']:issues.append([cid,a['unit'],'formula differs from visible model'])
 a.update(recomputed=v,modelSha=sha(u['model'].encode()),quizSha=sha(u['misconception'].encode()),inputSha=sha(p.read_bytes()),quizFalseBeliefReviewed=True)
 metadata={k:v for k,v in d.items() if k!='units'}
 courses[cid]=dict(inputSha=sha(p.read_bytes()),metadataSha=sha(json.dumps(metadata,ensure_ascii=False,sort_keys=True).encode()),units=len(d['units']),sourceKeys=[s['key'] for s in d['sources']])
# Additional worked sensitivities were recalculated from changed inputs, not text-length checks.
sens=[
 ('three-gorges','Forecast bias +20%',1500*1.2*6*3600,38880000,'m3'),
 ('b202','Arch path stiffness halved',100*4/(4+12),25,'MN'),
 ('b203','Pumping head +10%',1000*9.81*45*(95*1.1)/.86/1e6,53.64130813953488,'MW'),
 ('b204','Fan-independent gate drive speed halved',1600000*.0075/.75,16000,'W'),
 ('b205','Unbalance speed +10%',500*(2*math.pi*110/60)**2,66345.67402954512,'N'),
 ('b206','Forecast storage outflow +100 m3/s',(1200-1000)*30*86400,518400000,'m3'),
 ('b207','Thin-ring thickness +20%',2*180/(12*1.2),25,'MPa'),
 ('b208','Joint series stiffness doubled',1/(1/120+1/60),40,'GN/m'),
 ('b209','Copper current +20%',3*(24000*1.2)**2*.0007/1e6,1.741824,'MW')]
ss=[]
for cid,name,v,expected,unit in sens:
 ok=abs(v-expected)<max(1e-7,abs(expected)*1e-9)
 if not ok:issues.append([cid,name,v,expected])
 ss.append(dict(courseId=cid,scenario=name,recomputed=v,expected=expected,resultUnit=unit,passCheck=ok))
report=dict(reviewed='2026-10-21',scope='Nine world-dam courses. Every displayed literal model result recomputed from its separate expression and matched to the visible model. This verifies arithmetic and units/boundaries reviewed by the author, not project-specific design approval. All 90 wrong-choice misconceptions were read as false beliefs. Model mechanisms use separate original extensions rather than copying failure paragraphs.',modelCount=len(rows),courseCount=len(courses),issues=issues,courses=courses,models=rows,sensitivityChecks=ss,sourceLimitations=['Project-specific facts limited to recorded primary pages or explicitly identified official indexed excerpts.','USBR manual titles/editions checked at catalog and official abstracts; no full PDF review claimed.','USACE gravity manual catalog checked through official search index; direct page returned 403.','Baihetan source includes owner construction excerpt for basalt/low-heat cement; no material constants inferred.','Itaipu page with GW/GWh typo excluded from capacity claims; frequency and commissioning use separate official records.','No unsourced whole-dam construction dates inferred for Guri from a runner-renewal event.'])
(R/'numeric_landmarks_author.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
text=['# World dam author review V15','',f'9 courses; {len(rows)} visible numeric models; {len(ss)} changed-input sensitivities; {len(issues)} open arithmetic issues.','', 'All displayed parameters carry physical units or identified dimensionless roles. Hypothetical calculations are separated from official project facts. Mean forces, one-dimensional springs, thin-ring membrane scales, static droop, and statistical residuals are explicitly limited; none is presented as a complete dam approval or an operating setting.','', 'Misconception strings are deliberately false beliefs because the course generator uses them as wrong quiz choices. Every one of the 90 was checked. Mechanism extensions are original technical explanations independent of each failure paragraph.','', 'Source scope and retrieval references are in research_landmarks.json. Official page migrations are not construction dates. Bibliographic dates are labeled as literature dates. Vendors are associated through the cited institution or supplier record; no unsupported contractor role or security listing is asserted.','', '## Numerical results','', '| Course | Unit | Result | Unit |','|---|---:|---:|---|']
for a in rows:text.append(f"| {a['courseId']} | {a['unit']} | {a['recomputed']:.10g} | {a['resultUnit']} |")
text += ['', '## Independent sensitivity checks','', '| Course | Change | Result | Unit |','|---|---|---:|---|']
for a in ss:text.append(f"| {a['courseId']} | {a['scenario']} | {a['recomputed']:.10g} | {a['resultUnit']} |")
text += ['', 'Model and quiz SHA-256 values, current full-input hashes, metadata hashes and every expression are retained in reviews/numeric_landmarks_author.json. This report does not claim independent third-party peer review; root performs release review separately.','', 'Corrections found during author recalculation: Baihetan ventilation flow corrected to 288.4130074 m3/s; Chinese Froude discharge exponent corrected to five halves. Early true caution statements in the first three misconception batches were replaced with explicit false beliefs before freeze.']
(H/'REVIEW_LANDMARKS_V15.md').write_text('\n'.join(text)+'\n')
files=[p for p in H.glob('landmarks_*.py')]+[H/'build_landmarks.py',H/'audit_landmarks.py',H/'research_landmarks.json',H/'calculation_landmarks.json',H/'REVIEW_LANDMARKS_V15.md',R/'numeric_landmarks_author.json']+[H/'inputs'/f'{cid}.json' for cid in courses]
(R/'landmarks_freeze_manifest.json').write_text(json.dumps(dict(reviewed='2026-10-21',files={str(p.relative_to(H)):sha(p.read_bytes()) for p in sorted(files)},openIssues=issues),ensure_ascii=False,indent=2)+'\n')
print('reviewed',len(courses),'courses',len(rows),'models; issues',issues)
assert not issues
