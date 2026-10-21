#!/usr/bin/env python3
import json,math,hashlib,sys
from pathlib import Path
from peer_landmarks_checks import B
H=Path(__file__).resolve().parents[1]
def sha(b):return hashlib.sha256(b).hexdigest()
def calc(e):return eval(e,{'__builtins__':{},'math':math,'abs':abs,'min':min,'max':max,'sum':sum,'round':round})
def main():
 rows=[];courses=[];values=0
 sensitivity=json.loads((H/'reviews/peer_landmarks_sensitivity_checks.json').read_text())
 for cid,(checks,note) in sorted(B.items()):
  p=H/'inputs'/f'{cid}.json';d=json.loads(p.read_text());md={k:v for k,v in d.items() if k!='units'}
  for j,(expr,expected,tol,notes) in enumerate(checks,1):
   actual=[calc(e) for e in expr] if isinstance(expr,list) else calc(expr)
   es=expected if isinstance(expected,list) else [expected];ts=tol if isinstance(tol,list) else [tol];vs=actual if isinstance(actual,list) else [actual]
   for a,e,t in zip(vs,es,ts): assert abs(a-e)<=t+1e-12,(cid,j,a,e,t)
   values+=len(vs);u=d['units'][j-1]
   rows.append(dict(courseId=cid,unit=j,modelSha256=sha(u['model'].encode()),quizSha256=sha(u['misconception'].encode()),expression=expr,actual=actual,expected=expected,tolerance=tol,boundaryNotes=notes+' Wrong quiz option read as a false belief.',status='PASS'))
  extra={}
  if cid in sensitivity:
   check=dict(sensitivity[cid]);check['actual']=[calc(e) for e in check['expression']]
   for a,e,t in zip(check['actual'],check['expected'],check['tolerance']):assert abs(a-e)<=t+1e-12,(cid,'sensitivity',a,e,t)
   check['exampleSha256']=sha(d['example'].encode());extra['sensitivityReview']=check
  courses.append(dict(courseId=cid,inputSha256=sha(p.read_bytes()),metadataSha256=sha(json.dumps(md,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()),metadataNotes=note,sourceURLs=[s['url'] for s in d['sources']],status='PASS',**extra))
 if '--final' in sys.argv:assert set(sensitivity)==set(B),'All twenty example sensitivity reviews required before final status'
 status='PASS' if len(B)==20 and '--final' in sys.argv else 'IN_PROGRESS'
 report=dict(reviewer='/root/courses_landmarks',nonAuthorReviewer=True,status=status,scope='Independent visible-model arithmetic, dimensional/boundary and false-option review; scoped metadata/source review and example sensitivity checks. Full input hashes captured after rereading confirmed author changes.',reviewedNumericValues=values,reviewedExampleSensitivities=len(sensitivity),sourceEvidenceFile='peer_landmarks_sources.json',rows=rows,courses=courses)
 (H/'reviews/peer_landmarks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 print(status,len(rows),'models',values,'values',len(courses),'metadata')
if __name__=='__main__':main()
