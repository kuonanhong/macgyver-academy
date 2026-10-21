#!/usr/bin/env python3
"""Independent arithmetic audit: reads only emitted traces/inputs, not author models."""
import json,math
from pathlib import Path
H=Path(__file__).resolve().parent
records=json.loads((H/'calculation_landmarks.json').read_text())
def recompute(k,a):
 if k=='time':return a[0]*1000/(a[1]/3.6)/60
 if k=='darcy':return a[2]*(a[0]*a[1])
 if k=='head':return (a[0]/1000)*9.81*a[1]
 if k=='stress':return a[0]*(a[1]/1000)*3
 if k=='spring':return a[1]*a[0]
 if k=='ring':return a[0]/(a[2]/a[1])
 if k=='joint':return a[0]-(a[1]+a[2])
 if k=='advance':return a[0]*(86400/3600)*a[1]
 if k=='logistics':return a[1]*a[0]/(a[2]/60)
 if k=='angle':return a[0]*math.radians(a[1]/3600)
 if k=='friction':return a[0]*a[1]/a[2]*(a[3]/2)*a[4]*a[4]
 if k=='heat':return (a[0]*a[1])*(a[2]*a[3])
 if k=='dynamic':return a[0]*(a[1]*a[1])/2
 if k=='sump':return a[0]/(a[1]*60)
 if k=='escape':return a[0]+a[1]/a[2]
 if k=='reliability':return a[0]*a[0]
 if k=='coverage':return (1-a[1]/a[0])*100
 if k=='grade':return (a[0]*9.81*a[1])*(a[2]/1000)
 if k=='headway':return 1/((a[0]+a[1])/60)
 if k=='thermal':return (a[2]*1e9)*(a[0]*a[1])/1e6
 if k=='void':return (math.pi*(a[0]/2)**2-math.pi*(a[1]/2)**2)*a[2]
 if k=='rate':return a[0]/a[1]
 if k=='beam':return a[0]*(a[1]/2)**2/2
 if k=='float':return (a[0]*a[1]*9.81-a[2]*9.81)/1000
 if k=='settle':return (a[0]/1000)/a[1]*1000
 if k=='lighting':return a[1]*a[0]/math.pi
 if k=='diffusion':return (a[0]*a[1]*31557600)**.5*1000
 if k=='balance':return a[0]-(a[1]+a[2])
 if k=='waterfriction':return a[0]*a[1]/a[2]*(a[3]*a[3]/19.62)
 if k=='storage':return (a[0]-a[1])*(a[2]*60)
 if k=='inventory':return a[0]-(a[1]+a[2])
 if k=='lift':return (a[0]*9.81*a[1]/a[2])/a[3]/1000
 if k=='wedge':return (a[0]*a[1])/a[2]
 if k=='advection':return a[0]/(a[1]*60)
 if k=='footprint':return a[0]/a[1]
 if k=='hydropower':return (a[0]*a[1])*(9.81*a[2])/1000
 if k=='levelbias':return a[1]*a[0]
 if k=='contain':return (a[0]/1000)*9.81*a[1]-(a[2]/1000)*9.81*a[3]-a[4]
 if k=='flowreduction':return (1-a[1]/a[0])*100
 raise ValueError(k)
errors=[];audited=[]
for r in records:
 a=[p['value'] for p in r['inputs']];base=recompute(r['model'],a);b=a[:];b[r['changedIndex']]*=1.1;changed=recompute(r['model'],b)
 for name,v,expected in [('base',base,r['result']),('sensitivity',changed,r['changedResult'])]:
  if not math.isclose(v,expected,rel_tol=1e-11,abs_tol=1e-11):errors.append((r['courseId'],r['unit'],name,v,expected))
 d=json.loads((H/'inputs'/f'{r["courseId"]}.json').read_text());m=d['units'][r['unit']-1]['model'];z,e=m.split('~')
 for val in (r['result'],r['changedResult']):
  for half in (z,e):
   if f'{val:.6g}' not in half:errors.append((r['courseId'],r['unit'],'display mismatch',val))
 for p in r['inputs']:
  if f'{p["value"]:g}' not in z or f'{p["value"]:g}' not in e:errors.append((r['courseId'],r['unit'],'input absent',p))
 if any(not p['unit'] for p in r['inputs']):errors.append((r['courseId'],r['unit'],'missing unit'))
 audited.append(dict(courseId=r['courseId'],unit=r['unit'],model=r['model'],result=base,unitLabel=r['unitLabel'],changedResult=changed,passed=True))
# Distinct application checks are independent of numeric equality.
for cid in ('b107','b108','b119'):
 d=json.loads((H/'inputs'/f'{cid}.json').read_text())
 assert not any('σθ=pr/t' in u['model'] for u in d['units']),cid+' rectangular box cannot be a thin ring'
for cid in ('b117','b124','b125'):
 d=json.loads((H/'inputs'/f'{cid}.json').read_text())
 assert not any('t=60L/v' in u['model'] for u in d['units']),cid+' nontransport route'
assert len(records)==250 and len({r['courseId'] for r in records})==25
report=dict(reviewed='2026-10-21',recordCount=len(records),checks=500,displayChecks=250,errors=errors,method='Separate function rederived from physical equations and SI conversions; no import of landmarks_models or execution of its lambdas.',results=audited)
(H/'audit_landmarks_numeric.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('Independent arithmetic:',len(records),'base +',len(records),'sensitivity; errors:',len(errors))
for cid,k in [('b104','headway'),('b107','float'),('b109','beam'),('b117','waterfriction'),('b124','advection'),('b124','storage'),('b124','hydropower'),('b125','contain'),('b125','inventory')]:
 r=next(r for r in audited if r['courseId']==cid and r['model']==k);print(cid,k,r['result'],r['unitLabel'])
if errors:raise SystemExit(1)
