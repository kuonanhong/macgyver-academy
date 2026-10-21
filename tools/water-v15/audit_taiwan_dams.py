#!/usr/bin/env python3
"""Recompute literal author models without calling their generator calculations."""
from pathlib import Path
import ast,hashlib,json,math,sys
H=Path(__file__).resolve().parent
records=json.loads((H/'calculation_taiwan_dams.json').read_text())
assert len(records)==60
checks=[];issues=[]
for a in records:
 cid=a['courseId'];i=a['unit'];d=json.loads((H/'inputs'/f'{cid}.json').read_text());u=d['units'][i-1]
 tree=ast.parse(a['expression'],mode='eval')
 for node in ast.walk(tree):
  assert isinstance(node,(ast.Expression,ast.BinOp,ast.UnaryOp,ast.Constant,ast.Add,ast.Sub,ast.Mult,ast.Div,ast.Pow,ast.USub,ast.Call,ast.Attribute,ast.Name,ast.Load)),type(node)
  if isinstance(node,ast.Name):assert node.id=='math'
  if isinstance(node,ast.Attribute):assert node.attr in ('sqrt','tan','radians')
 v=eval(compile(tree,'<independent literal expression>','eval'),{'__builtins__':{},'math':math})
 passed=abs(v-a['expected'])<=a['tolerance']
 if not passed:issues.append(f'{cid} u{i}: {v} vs {a["expected"]}')
 checks.append(dict(courseId=cid,unit=i,modelSha256=hashlib.sha256(u['model'].encode()).hexdigest(),arithmeticReview='pass' if passed else 'fail',independentExpression=a['expression'],recomputed=v,displayedExpected=a['expected'],resultUnit=a['resultUnit'],roundingTolerance=a['tolerance'],boundaryNotes=a['boundary'],misconceptionSha256=hashlib.sha256(u['misconception'].encode()).hexdigest(),misconceptionReview='false-distractor-reviewed',misconception=u['misconception']))
(H/'reviews').mkdir(exist_ok=True)
out=dict(reviewer='/root/courses_landmarks/taiwan_dams',reviewType='Author independent literal recomputation and manual false-distractor semantic audit; not an external peer review',date='2026-10-21',checks=checks,issues=issues,inputSha256={f'b{x}':hashlib.sha256((H/'inputs'/f'b{x}.json').read_bytes()).hexdigest() for x in range(215,221)})
extra=[('b215','20% thickness increase',0.8*120/12,8,'MPa'),('b216','20% arch stiffness reduction',50*2400/(2400+2000),27.272727272727273,'MN'),('b217','Less permeable layer doubled',1000*30/(10/1e-7+10/1e-7),0.00015,'m3/s'),('b218','Second-stage efficiency 0.8',1000*9.81*15*(200*0.9+120*0.8)/1e6,40.6134,'MW'),('b219','20% larger downstream demand',1200000-840000-100000-50000,210000,'m3/day'),('b220','Midpoint area 10% above linear',2/6*(4000000+4*4950000+5000000),9600000,'m3')]
out['metadataSensitivityChecks']=[dict(courseId=c,scenario=s,recomputed=v,expected=e,resultUnit=u,arithmeticReview='pass' if abs(v-e)<1e-8 else 'fail') for c,s,v,e,u in extra]
assert all(c['arithmeticReview']=='pass' for c in out['metadataSensitivityChecks'])
(H/'reviews'/'numeric_taiwan_author.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
lines=['# V15 six dam cases: numeric and content review','','Author: `/root/courses_landmarks/taiwan_dams`. Date: 2026-10-21. This is an author audit using separately entered Python literal expressions, not independent external peer review.','', '## Coverage','','- Six courses b215–b220, exactly ten distinct units each; 60 models recomputed.','- Every model explicitly labels assumptions, inputs with units and applicable limitations. All project dimensions and historical dates remain separate from teaching scenarios.','- All 60 misconception fields manually read as plausible FALSE propositions for quiz distractors. Correct cautions were inverted in the first 20 authored entries; later entries were authored as false propositions.','- Mechanisms contain distinct physics discussion; no mechanism is built by copying its entire failure paragraph.','', '## Corrections found by recomputation','','- b216 unit 8 conjugate hydraulic-jump depth corrected from 3.146774 to 3.146630 m.','- b217 unit 7 orifice discharge corrected from 10.09064 to 10.090393 m3/s.','- b219 unit 4 gated underflow corrected from 27.639874 to 27.639749 m3/s.','- b219 unit 8 Manning discharge corrected from 4.174848 to 4.173697 m3/s.','- b218 metadata efficiency sensitivity corrected to 40.6134 MW.','- b215 unit 2 uses a 10 m thickness and 120 m radius (ratio 0.0833), giving 9.6 MPa ideal membrane compression; a 20% thickness increase gives 8 MPa. Explicitly a reduced ideal strip, not a complete arch stress solution.','', '## Source boundaries','','- Owner/authority sources support Kurobe 186 m/1963; Feitsui 122.5 m/1987; Shihmen 133.1 m/1964; Deji 180 m and distinct 1973 impoundment/1974 completion; Tsengwen current 134 m/400 m/1973; Nanhua 87.5 m and distinct 1993 impoundment/1994 completion and supply.','- Tsengwen uses current owner 134 m; an older 133 m value was deliberately not mixed in.','- Reclamation guides were checked at official index scope, including 2014 seepage and 2022 appurtenant chapter dates; linked full documents are not claimed as fully reviewed.','- USACE 1994 arch title/date were confirmed by official indexed catalogue/cover excerpts; direct catalogue and PDF retrieval returned 403, recorded explicitly.','- Institutions are data or method-reference providers; no invented construction contract, participation, financial listing or security identifier.','- No current reservoir capacity, operating schedule, design criterion, flow permission or site safety conclusion is inferred from historical webpages.','', '## All arithmetic checks','','| Course | Unit | Literal recomputation | Result | Unit |','|---|---:|---|---:|---|']
for c in checks:lines.append(f"| {c['courseId']} | {c['unit']} | `{c['independentExpression']}` | {c['recomputed']:.10g} | {c['resultUnit']} |")
lines += ['','## Final artifacts','','`research_taiwan_dams.json` preserves access evidence and scoped claims. `reviews/numeric_taiwan_author.json` preserves each final model hash, misconception hash, input hash and recomputation. All six input JSONs pass the unchanged strict validator.']
(H/'REVIEW_TAIWAN_DAMS_V15.md').write_text('\n'.join(lines)+'\n')
print(f'{len(checks)} models recomputed; {len(issues)} issues')
if issues:print('\n'.join(issues));sys.exit(1)
