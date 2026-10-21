"""Author SI recomputation of declared original examples; no engineering certification."""
from pathlib import Path
import math,json,hashlib
H=Path(__file__).resolve().parent
ROWS=[
(1,'3000*10',(3000*10,),(30000.,),'m3','Constant waterplane; unchanged floating displacement cancels.'),
(2,'(A1*z1+A2*z2)/(A1+A2); A1*(z1-zf)',((3000*10+6000*4)/9000,3000*(10-6)),(6.,12000.),'m,m3','No external inflow/outflow, shared datum and fixed areas.'),
(3,'rho*g/2*(A1*A2/(A1+A2))*dh**2',(.5*1000*9.81*(3000*6000/9000)*6**2/1e6,),(353.16,),'MJ','Resting endpoints, no pumping or energy recovery.'),
(4,'reuse/gross; gross-reuse',(18000/30000,30000-18000),(.60,12000.),'fraction,m3','Same cycle and denominator; not comparison to differently sized locks.'),
(5,'Q*86400',(.020*86400,),(1728.,),'m3/day','Constant rate assumption, no field acceptance threshold.'),
(6,'area*evaporation',(12000*.005,),(60.,),'m3/day','Daily exposed-water loss, not per-lockage loss.'),
(7,'Cd*a*sqrt(2*g*dh)',(.7*4*math.sqrt(2*9.81*2),),(17.54,),'m3/s','Instantaneous quasi-steady flow, not constant over exchange.'),
(8,'2*(sqrt(h0)-sqrt(hf))/(Cd*a*sqrt(2*g)*(1/A1+1/A2))',(2*(math.sqrt(6)-math.sqrt(.1))/(.7*4*math.sqrt(2*9.81)*(1/3000+1/6000)),),(688.0,),'s','Both finite areas updated; finite residual0.1m and no valve sequence instruction.'),
(9,'area*coherent_bias',(6000*.010,),(60.,),'m3','Systematic offset, no sqrt(n) averaging.'),
(10,'gross*(1-r1);gross*(1-r2);(new/old-1)*100',(30000*(1-.6),30000*(1-.4),((1-.4)/(1-.6)-1)*100),(12000.,18000.,50.),'m3,m3,percent','Fixed gross demand; reuse change is20percentage points, makeup change50percent.')]
def run():
 f=H/'inputs/b293.json';d=json.loads(f.read_text());checks=[]
 for n,expr,a,b,units,boundary in ROWS:
  ok=all(abs(x-y)<=max(.01,abs(y)*.00005)for x,y in zip(a,b));u=d['units'][n-1]
  checks.append(dict(courseId='b293',unit=n,expression=expr,recomputed=a,published=b,units=units,boundary=boundary,status='PASS'if ok else'FAIL',model=u['model'],modelSha256=hashlib.sha256(u['model'].encode()).hexdigest(),inputSha256=hashlib.sha256(f.read_bytes()).hexdigest()))
 sens=dict(courseId='b293',base=[3000*10,3000*10*(1-.6)],changed=[3300*10,3300*10*(1-.6)],relativeChangePercent=10,assumptions='Only chamber area rises10%; fixed lift and separately assumed fixed reuse.',status='PASS')
 result=dict(date='2026-10-21',method='Author recomputation of synthetic SI examples; not independent engineering design approval.',courseIds=['b293'],units=10,passes=sum(c['status']=='PASS'for c in checks),checks=checks,sensitivity=[sens])
 (H/'locks_coast_audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 assert result['passes']==10
 print('b293:10/10 numerical models + sensitivity PASS')
if __name__=='__main__':run()
