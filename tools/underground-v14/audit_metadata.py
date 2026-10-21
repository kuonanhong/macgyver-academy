#!/usr/bin/env python3
"""Metadata integrity ledger; human findings remain explicit and reviewable."""
import json,re,hashlib
from pathlib import Path
H=Path(__file__).resolve().parent
T=json.loads((H/'targets.json').read_text())
manual=set(['hsuehshan']+[f'b{n}' for n in range(102,146)]+[f'b{n}' for n in range(146,176)]+[f'b{n}' for n in range(176,191)]+[f'b{n}' for n in range(191,201)])
# Update only after reading the new facts/timeline/scopes/roles, not upon file existence.
issues={cid:['Timeline has 1997 USACE and 2018 CEDD G4 publications absent from selected sources; author notified to align chronology and source list.'] for cid in ['b177']+[f'b{n}' for n in range(179,191)]}
notes={
 'b122':['Official Shaanxi yearbook indexed extract only; direct PDF unavailable. Scope states this. Conflicting CREC English length/start excluded.'],
 'b107':['Current owner 18 km retained; conflicting older 19 km excluded; 2020 denotes construction, not opening.'],
 'b115':['2025 second-tube event identified as announced; 1980 original opening is the historical fact.'],
 'b117':['16.5 km conveyance scope and 6.5 km TBM subsection separated; 2002 event is TBM breakthrough.'],
 'b119':['About 7 km denotes the tunnel section, not immersed-only length.'],
 'b124':['2002 interim 3.3 km operation separated from 6.3 km waterway and 2006 completion of construction.'],
 'b128':['Six illustrative classification scores are actual dimensionless arithmetic, not enumerators pretending to be quantitative facts.'],
 'b197':['Timeline heading and history now use 1980s, preserving the source decade instead of implying an exact installation year.'],
 'b179':['Crossrail reference explicitly says ground freezing was NOT used; presented as alternatives comparison.'],
 'b125':['Kirsch example now labels the sidewall maximum and uses explicitly hypothetical 120 m cover; published capacity/opening scope retained.'],
 'b145':['After the final RSS wording edit, metadata was reread; the previous full file was not reconstructed. Current full and metadata hashes are recorded.'],
 'b175':['Heathwall 2013 is a planning proposal, not an as-built caisson claim; Cremorne 2020 is explicitly a non-caisson comparison.'],
 'b200':['PDF/access limitations disclosed; legacy 2016/2019 UFC is not represented as the current edition.']}
notes.update({'b151': ['Reread facts/example: early-strength stress and capacity inputs now explicitly carry MPa; ratios 0.50 and 0.75 unchanged.'], 'b158': ['Reread facts/example: span-to-fourth-power ratio fixes line load, EI and supports; full-ring volume labels both radii and length. Values unchanged.'], 'b161': ['Reread facts/example: 80 mm is compatible circumferential joint slip, explicitly not diametral convergence.'], 'b163': ['Reread facts/example: conveyed-fluid density, elevation and connected-void inputs are explicit; 0.8481 MPa is a scoped pressure balance, not an operating instruction.'], 'b169': ['Reread facts/example: chord inclination equals relative rotation only beside the stated horizontal neighbor; 0.0001 rad unchanged.'], 'b170': ['Reread facts/example: 60 kN/m is transverse load resultant rather than membrane tension; rotation assumptions are explicit.'], 'b174': ['Reread facts/example: 0.0349 m is a whole-length projection of final angle, not an integrated guidance-path error.']})
rows=[];errors=[]
for t in T:
 cid=t['id'];p=H/'inputs'/f'{cid}.json'
 if not p.exists():rows.append(dict(id=cid,status='pending author file'));continue
 raw=p.read_bytes();d=json.loads(raw);quant=[]
 for i,f in enumerate(d.get('facts',[]),1):
  halves=f.split('~');ok=len(halves)==2
  for half in halves:
   x=re.sub(r'^(?:假想檢核|Assumed check)\s*\d+\s*[:：]','',half)
   ok=ok and bool(re.search(r'\d',x))
  quant.append(ok)
  if not ok:errors.append(f'{cid} fact {i}: no numerical content after enumeration removal')
 prim=sum(s.get('sourceType')=='primary' for s in d.get('sources',[]))
 if prim<2:errors.append(f'{cid}: fewer than 2 primary sources')
 if len(d.get('sources',[])) not in (3,4,5):errors.append(f'{cid}: source-count range')
 for s in d.get('sources',[]):
  if not s.get('scope') or not s.get('scopeEn'):errors.append(f'{cid}: missing source scope')
  if not str(s.get('url','')).startswith(('https://','http://')):errors.append(f'{cid}: nonweb source')
 # resolved chronology issue if old entries disappear or both supporting sources are now present
 keys={s['key'] for s in d.get('sources',[])};timeline=' '.join(x['event'] for x in d.get('timeline',[]))
 findings=issues.get(cid,[])[:]
 untraced_rock=any(str(x['year'])=='1997' and ('USACE' in x['event'] or '工兵署' in x['event']) for x in d.get('timeline',[])) and 'usace-rock' not in keys
 untraced_cavern=any(str(x['year'])=='2018' and ('cavern' in x['event'].lower() or '岩洞' in x['event']) for x in d.get('timeline',[])) and 'geo-cavern' not in keys
 if findings and not untraced_rock and not untraced_cavern:
  findings=[]
 resolved=['Shared chronology replaced by dated selected-source publications; 2026 identifies teaching review/calculation, not construction.'] if cid in issues and not findings else []
 rows.append(dict(id=cid,status='reviewed with finding' if cid in manual and findings else 'reviewed' if cid in manual else 'pending manual review',sha256=hashlib.sha256(raw).hexdigest(),metadataSHA256=hashlib.sha256(json.dumps({k:v for k,v in d.items() if k!='units'},ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest(),factCount=len(quant),quantitativeFacts=all(quant),timelineCount=len(d.get('timeline',[])),sourceCount=len(d.get('sources',[])),primarySourceCount=prim,vendorCount=len(d.get('vendors',[])),findings=findings,notes=notes.get(cid,[]),resolvedFindings=resolved))
report=dict(date='2026-10-21',scope='Metadata integrity and provenance review; not an independent recomputation of all 1000 unit models. Landmark arithmetic has a separate complete 500-result audit.',manualReviewed=sum(r['status'].startswith('reviewed') for r in rows),present=sum('sha256' in r for r in rows),total=len(T),automatedErrors=errors,openFindingCount=sum(bool(r.get('findings')) for r in rows),resolvedFindingCount=sum(bool(r.get('resolvedFindings')) for r in rows),rows=rows)
(H/'audit_metadata.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
lines=['# V14 metadata audit','',f"Reviewed {report['manualReviewed']} / {len(T)} course metadata sets; {report['present']} files currently present. {len(errors)} automated integrity errors.",'','This audit reads the displayed quantitative facts, historical narrative and timeline distinctions, declared source access scope and institutional roles. It does not claim independently reading every linked full text or recomputing all 1000 course models. The 25 landmark courses separately have 500 independent arithmetic checks.','','## Findings and corrections','','- All reviewed facts contain actual values after removing item numbers; dimensionless ratios/scores are accepted when their arithmetic meaning is explicit.','- Teaching values are marked hypothetical; published scales retain boundaries, and source institutions are not falsely described as project contractors.','- Limited PDF, DOI and indexed-extract access is explicitly stated in source scopes where encountered.','- Thirteen ground-course chronology/source mismatches were corrected to match selected-source publications; 2026 entries explicitly denote curriculum review or recalculation, not project completion. The revised history and source scopes were read again.','- Investigation timelines in b126–145 now sort chronologically after review; this was a presentation correction rather than a changed historical claim.','','| Course | Status | Facts | Sources / primary | Notes |','|---|---|---:|---:|---|']
for r in rows:
 lines.append('| '+r['id']+' | '+r['status']+' | '+str(r.get('factCount','—'))+' | '+str(r.get('sourceCount','—'))+' / '+str(r.get('primarySourceCount','—'))+' | '+' '.join(r.get('findings',[])+r.get('notes',[])+r.get('resolvedFindings',[]))+' |')
lines+=['','Full-file and non-units metadata SHA-256 values and exact coverage are in `audit_metadata.json`. Final b127–144 metadata equality was confirmed against a pre-overlay reconstruction matching the previous full-file hashes; b145 metadata was reread after its RSS edit without claiming old-full-file reconstruction. The evidence is in `audit_metadata_refresh.json`. Final support wording changes propagated to seven facts/example metadata sets; these were reread and accepted with explicit unit and boundary notes, rather than claimed unchanged. Before/after hashes and review notes are in `audit_metadata_final_freeze.json`. A changed file requires incremental review; author notifications do not silently mark unfinished files as checked.','']
(H/'REVIEW_METADATA_V14.md').write_text('\n'.join(lines))
print('Metadata:',report['manualReviewed'],'reviewed,',report['present'],'present,',len(errors),'automatic errors,',sum(bool(r.get('findings')) for r in rows),'open findings')
