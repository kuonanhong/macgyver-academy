#!/usr/bin/env python3
"""Recompute authored numeric results from input quantities; do not modify course inputs."""
from pathlib import Path
import runpy,math,json,hashlib,re
P=Path(__file__).resolve().parent
B=runpy.run_path(str(P/'build_hydraulics.py'))
for p in sorted(P.glob('hydraulics_rows_*.py')):runpy.run_path(str(p),init_globals={'add':B['add']})
out=[]
for cid,c in sorted(B['C'].items()):
 for i,r in enumerate(c['rows'],1):
  value=eval(r[6],{'__builtins__':{}},{'math':math})
  expected=float(r[7]);ok=math.isclose(value,expected,rel_tol=1e-9,abs_tol=1e-10)
  literal=re.findall(r'=\s*([-+]?\d+(?:\.\d*)?(?:[eE][-+]?\d+)?)',r[2])[-1]
  from decimal import Decimal
  tolerance=0.5*10**Decimal(literal).as_tuple().exponent
  displayed=float(literal); displayOK=abs(displayed-value)<=tolerance+1e-9*abs(value)
  ok=ok and displayOK
  out.append(dict(course=cid,unit=i,title=r[0],model=r[2],expression=r[6],computed=value,expected=expected,displayed=displayed,displayTolerance=tolerance,displayPass=displayOK,passCheck=ok))
report=dict(scope='All authored primary numerical results recomputed from stated quantities; does not certify engineering design. Stored unrounded results checked at 1e-9 relative tolerance; display rounding checked separately.',checks=len(out),passed=sum(x['passCheck'] for x in out),inputs={cid:hashlib.sha256((P/'inputs'/f'{cid}.json').read_bytes()).hexdigest() for cid in sorted(B['C'])},results=out)
(P/'audit_hydraulics.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(report['passed'],'/',len(out))
for x in out:
 if not x['passCheck']:print(x['course'],x['unit'],x['computed'],x['expected'])
raise SystemExit(0 if report['passed']==len(out) else 1)
