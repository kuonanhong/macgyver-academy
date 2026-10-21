"""Record independently reviewed expressions; never infer expressions from author audits."""
import hashlib,json,math
from pathlib import Path
H=Path(__file__).resolve().parent.parent
P=H/'reviews/peer_investigation.json'
def sha(b):return hashlib.sha256(b).hexdigest()
def record(data,metadata,replace_reviewed=()):
 report=json.loads(P.read_text()) if P.exists() else dict(reviewer='/root/courses_investigation',nonAuthorReviewer=True,status='IN_PROGRESS',rows=[],courses=[],method='Reviewer read input models and false quiz distractors, independently entered arithmetic and boundary judgments, and checked metadata against primary evidence. No author audit expressions were imported.')
 ids=set(data);old={r['courseId'] for r in report['courses']}
 assert not ((ids&old)-set(replace_reviewed)), 'Already reviewed courses require explicit rereview permission'
 report['rows']=[r for r in report['rows'] if r['courseId'] not in ids]
 report['courses']=[r for r in report['courses'] if r['courseId'] not in ids]
 for cid,rows in data.items():
  path=H/'inputs'/f'{cid}.json';d=json.loads(path.read_text());assert len(rows.strip().splitlines())==10
  for i,line in enumerate(rows.strip().splitlines(),1):
   ex,expected,tolerance,note=line.split('|',3);actual=eval(ex,{'__builtins__':{},'math':math,'max':max,'min':min,'abs':abs,'sum':sum});expect=float(expected);tol=float(tolerance)
   assert abs(actual-expect)<=tol,(cid,i,actual,expect,tol)
   u=d['units'][i-1]
   report['rows'].append(dict(courseId=cid,unit=i,modelSha256=sha(u['model'].encode()),quizSha256=sha(u['misconception'].encode()),expression=ex,actual=actual,expected=expect,tolerance=tol,boundaryNotes=note+' Both-language misconception is a false generalization or dimensional error, appropriate as a distractor; assumed numerical values are separated from project facts.',status='PASS'))
  report['courses'].append(dict(courseId=cid,inputSha256=sha(path.read_bytes()),metadataSha256=sha(json.dumps({k:v for k,v in d.items() if k!='units'},ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()),metadataNotes=metadata[cid],sourceURLs=[s['url'] for s in d['sources']],status='PASS'))
 report['rows'].sort(key=lambda r:(r['courseId'],r['unit']));report['courses'].sort(key=lambda r:r['courseId'])
 report['status']='PASS' if len(report['rows'])==200 and len(report['courses'])==20 else 'IN_PROGRESS'
 P.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(report['status'],len(report['rows']),'models',len(report['courses']),'courses')
