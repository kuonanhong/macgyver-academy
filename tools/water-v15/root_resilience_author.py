"""Original V15 resilience-course author helpers; no public build side effects."""
from pathlib import Path
import json, hashlib, math
HERE=Path(__file__).resolve().parent
TARGETS={x['id']:x for x in json.loads((HERE/'targets.json').read_text())}
def unit(title,mechanism,model,verify,failure,misconception,practice):
 return dict(anchor=title,title=title,mechanism=mechanism,model=model,verify=verify,failure=failure,misconception=misconception,practice=practice)
def source(key,title,en,publisher,url,scope,scope_en):
 return dict(key=key,title=title,titleEn=en,publisher=publisher,url=url,sourceType='primary',scope=scope,scopeEn=scope_en)
def entity(name,en,url,business,business_en,role,role_en):
 return dict(name=name,nameEn=en,url=url,business=business,businessEn=business_en,role=role,roleEn=role_en,security=None,investorUrl='')
def save(cid,**data):
 t=TARGETS[cid];d=dict(id=cid,title=t['title']+'~'+t['titleEn'],discipline=t['discipline'],family='water',**data)
 p=HERE/'inputs'/f'{cid}.json';temp=p.with_suffix('.tmp');temp.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');temp.replace(p)
 return d
def audit(cid,expressions):
 d=json.loads((HERE/'inputs'/f'{cid}.json').read_text());rows=[]
 for i,(expression,expected,tolerance) in enumerate(expressions,1):
  actual=eval(expression,{'__builtins__':{},'math':math});assert abs(actual-expected)<=tolerance,(cid,i,actual,expected)
  m=d['units'][i-1]['model'];rows.append(dict(courseId=cid,unit=i,expression=expression,result=actual,expected=expected,tolerance=tolerance,modelSha256=hashlib.sha256(m.encode()).hexdigest(),status='PASS'))
 out=HERE/'audit_root_resilience.json';report=json.loads(out.read_text()) if out.exists() else {'author':'root','scope':'Author recalculation, not independent peer review. All inputs are hypothetical teaching scenarios.','checks':[]}
 report['checks']=[x for x in report['checks'] if x['courseId']!=cid]+rows;out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
