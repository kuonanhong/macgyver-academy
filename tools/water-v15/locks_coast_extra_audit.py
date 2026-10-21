"""Independent arithmetic expressions for authored synthetic inputs; not design certification."""
from pathlib import Path
import json,math,hashlib,statistics
H=Path(__file__).resolve().parent
pi=math.pi;sqrt=math.sqrt
# Each entry is one authored unit, with one or more independently recomputed outputs.
# Values use explicit output units and tolerance no wider than stated rounding.
A={
'b256':[
[('sqrt(2e9/50e6)',6.325,.0005,'rad/s'),('2*pi*sqrt(50e6/2e9)',.9935,.00005,'s')],
[('50e6*.20*9.81/1e6',98.10,.005,'MN')],
[('2*.05*sqrt(2e9*50e6)',31622776.6,.05,'N s/m')],
[('1/sqrt((1-1**2)**2+(2*.05*1)**2)',10,1e-10,'dimensionless')],
[('.4*9.81/(2*pi)**2',.09940,.000005,'m')],
[('2*.05*(2*pi)*(6*pi)/(8*pi)',.47124,.000005,'1/s'),('2*.05/(8*pi)',.0039789,.00000005,'s'),('((2*.05*(2*pi)*(6*pi)/(8*pi))/(4*pi)+(2*.05/(8*pi))*(4*pi))/2',.04375,1e-8,'dimensionless')],
[('2*pi*sqrt(70e6/2e9)',1.1755,.00005,'s')],
[('12-(-8)',20,1e-9,'mm')],
[('.20/.005',40,1e-9,'points/cycle')],
[('60/100',.60,1e-9,'dimensionless'),('100-60',40,1e-9,'kPa')]],
'b257':[
[('8/40',.20,1e-9,'m'),('80/40',2,1e-9,'m')],
[('8/sqrt(40)',1.2649,.00005,'m/s')],
[('1000/40**2.5',.09882,.000005,'m3/s')],
[('120/sqrt(40)',18.974,.0005,'s')],
[('60/40',1.50,1e-9,'kPa')],
[('2e6/40**3',31.25,1e-9,'N')],
[('(8/sqrt(40))*.2/1e-6',252982,.5,'Re'),('8*8/1e-6',64000000,1e-8,'Re')],
[('1000*1.6*.2/.072',4444.4,.05,'We'),('40**2',1600,1e-9,'ratio')],
[('.0005*40',.020,1e-9,'m')],
[('statistics.mean([.098,.100,.102])',.100,1e-9,'m3/s'),('statistics.stdev([.098,.100,.102])',.002,1e-9,'m3/s'),('statistics.stdev([.098,.100,.102])/statistics.mean([.098,.100,.102])*100',2,1e-9,'%')]],
'b258':[
[('100*1800',180000,1e-9,'m3'),('-100*1800+100*1800',0,1e-9,'m3 total change')],
[('180000/600000',.300,1e-9,'m')],
[('600-200-15',385,1e-9,'m')],
[('1000*9.81*100*385*.90/1e6',339.9165,.00005,'MW')],
[('1000*9.81*100*415/.88/1e6',462.631,.0005,'MW')],
[('.88*.90',.792,1e-9,'dimensionless')],
[('720000/100',7200,1e-9,'s'),('720000/100/3600',2,1e-9,'h')],
[('(0+100)*300/2',15000,1e-9,'m3')],
[('1e6*.004',4000,1e-9,'m3/day')],
[('800000-200000',600000,1e-9,'m3')]],
'b259':[
[('2*2/(2*.02)',100,1e-9,'MPa')],
[('2*2/(4*.02)',50,1e-9,'MPa')],
[('2*2e6*pi*math.sin(pi/4)/1e6',8.8858,.00005,'MN')],
[('12e-6*100*30',.036,1e-9,'m')],
[('200e9*12e-6*30/1e6',72,1e-9,'MPa compression')],
[('9.81*(7850*pi/4*(2.04**2-2**2)+1000*pi)/1000',40.593,.0005,'kN/m')],
[('40*10**2/8',500,1e-9,'kNm'),('40*10/2',200,1e-9,'kN each')],
[('.15*400',60,1e-9,'kN limiting')],
[('2e6/4/1000',500,1e-9,'kPa')],
[('100*20/18',111.11,.005,'MPa'),('(20/18-1)*100',11.11,.005,'%')]],
'b260':[
[('sqrt(2.2e9/(1000*(1+2.2e9*2/(200e9*.02))))',1023.53,.005,'m/s')],
[('2*1000/1000',2,1e-9,'s')],
[('1000*1000*1/1e6',1,1e-9,'MPa'),('1000*1/9.81',101.94,.005,'m')],
[('(20-5)/100',.15,1e-9,'m/s')],
[('2*pi*sqrt(1000*100/(9.81*10))',200.607,.0005,'s')],
[('2*sqrt(1000*10/(9.81*100))',6.3855,.00005,'m')],
[('.02*(1000/2)*2**2/(2*9.81)',2.0387,.00005,'m')],
[('(10/(.65*2))**2/(2*9.81)',3.0159,.00005,'m')],
[('100-80',20,1e-9,'kPa absolute'),('100-80-2.34',17.66,1e-9,'kPa difference')],
[('1000*.10/100',1,1e-9,'Courant')]]}
B={
'b256':[('2*pi*sqrt(50e6/2.2e9)',.9472,.00005,'s'),('(1/sqrt(1.1)-1)*100',-4.65,.005,'%')],
'b257':[('1000/44**2.5',.07787,.000005,'m3/s'),('((40/44)**2.5-1)*100',-21.20,.005,'%')],
'b258':[('1000*9.81*100*423.5*.9/1e6',373.90815,.000005,'MW'),('(423.5/385-1)*100',10,1e-9,'%')],
'b259':[('2.2*2/(2*.02)',110,1e-9,'MPa'),('(2.2/2-1)*100',10,1e-9,'%')],
'b260':[('2*sqrt(1000*10/(9.81*110))',6.0883,.00005,'m'),('(1/sqrt(1.1)-1)*100',-4.65,.005,'%')]}
def checks(items):
 out=[]
 for expression,published,tolerance,unit in items:
  value=eval(expression,{'__builtins__':{}},{'pi':pi,'sqrt':sqrt,'math':math,'statistics':statistics})
  ok=abs(value-published)<=tolerance
  out.append(dict(expression=expression,recomputed=value,published=published,tolerance=tolerance,unit=unit,pass_=ok))
  assert ok,(expression,value,published,tolerance)
 return out
report=dict(date='2026-10-21',status='PASS',method='Author arithmetic recalculation using separately written Python SI expressions, rounding-aware assertions, and explicit physical-boundary review; not independent engineering certification.',courses={},limits=['All numerical inputs are original synthetic teaching assumptions.','No calculation approves a field operating limit, component capacity or site design.','External sources support published methods and project context, not synthetic values.'])
for cid,rows in A.items():
 raw=(H/'inputs'/f'{cid}.json').read_bytes();d=json.loads(raw);assert len(rows)==len(d['units'])==10
 models=[u['model']for u in d['units']]
 units=[dict(unit=i+1,modelSha256=hashlib.sha256(models[i].encode()).hexdigest(),model=models[i],checks=checks(x))for i,x in enumerate(rows)]
 report['courses'][cid]=dict(inputSha256=hashlib.sha256(raw).hexdigest(),modelsSha256=hashlib.sha256(json.dumps(models,ensure_ascii=False,separators=(',',':')).encode()).hexdigest(),units=units,sensitivity=checks(B[cid]))
report['unitModels']=sum(len(x['units'])for x in report['courses'].values())
report['numericAssertions']=sum(sum(len(u['checks'])for u in x['units'])+len(x['sensitivity'])for x in report['courses'].values())
report['physicalBoundaryReview']={
'b256':'Generalized mass and absolute acceleration distinguished; harmonic steady state is not earthquake response; pseudo spectrum and Rayleigh frequency dependence explicit; relative motion synchronous; fixed total stress required for pore-pressure increment.',
'b257':'Undistorted equal-density Froude scale uses Q ratio L^2.5, force L^3; Reynolds/Weber mismatch explicit; gauge/absolute pressure separated; uncertainty and repeatability not global validation.',
'b258':'Paired transfers conserve water; level needs storage curve; generation net head differs from pump lift; equal-head round trip and terminal storage explicit; ramp volume not water hammer; external weather exchange remains possible.',
'b259':'Thin-wall remote membrane only; closed-end freely extending axial boundary; equal-pressure elbow omits momentum/weight; thermal free versus restrained separated; full-water weight, static friction bound, centered full contact and uniform loss stated.',
'b260':'Specified wall factor for wave speed; single path round trip; rapid single-phase first increment not full envelope; rigid column excludes shaft inertia/friction/compressibility; zero initial level offset; Darcy convention, absolute pressure and grid convergence explicit.'}
(H/'locks_coast_extra_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(f"PASS {report['unitModels']} unit models; {len(B)} sensitivities; {report['numericAssertions']} assertions")
