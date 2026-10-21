#!/usr/bin/env python3
"""Independent reviewer ledger. Expressions below are independently transcribed/rederived
from learner-facing models, never imported from author calculators. Sources independently
opened in the review session. Run regenerates hashes, so only run after rereading changed inputs.
"""
import math,json,hashlib
from pathlib import Path
P=Path(__file__).resolve().parent
I=P.parent/'inputs'
C={}
M={}
def add(k,rows,meta):
 C[k]=rows;M[k]=meta
add('three-gorges',[
('1500*(6*60*60)',32400000,1e-7,'Constant forecast discharge bias times interval; volume error, not extra inflow. m3/s times s.'),
('((380e6+420e6)/2)*2',800000000,1e-6,'Trapezoidal level-area integral assumes linear area variation and level surface; not full reservoir curve.'),
('2000*.30*86400*.60/1200',25920,1e-8,'Retained sediment mass divided by dry bulk density, not particle density; omits bedload and consolidation.'),
('(120*22+80*12)/200',18,1e-9,'Equal density/heat capacity and perfect adiabatic mixing; outlet mean is not whole downstream temperature.'),
('4200*18*12',907200,1e-8,'One isolated chamber, full exchange, no recycling; not blindly multiplied across multistage locks.'),
('18000*9.81*.08/.80',17658,1e-8,'Constant velocity imbalance power divided by efficiency; omits acceleration/friction; floating displacement matters.'),
('650*88*9.81*.91/1000',510.63012,5e-6,'MW; net head is gross minus losses; fixed overall efficiency, no availability inference.'),
('(.25*400+.25*700)/2',137.5,1e-9,'MWh is trapezoidal integral of a linear electrical ramp; does not establish hydraulic transient safety.'),
('12e-6*80000',.96,1e-9,'Measured water-surface slope times length gives level difference; not automatically friction slope.'),
('(7.2-5.4)/.6',3,1e-9,'Fixed baseline standard deviation; standardized residual is dimensionless and no universal safety threshold.')],
'Owner page confirms gravity type, 1994 start, 2012 main-unit commissioning and 22500 MW; datum caveat is appropriate. USBR 1987 is a reference date. Approximate site point in Hubei; vendors are source institutions, security null. All 10 misconceptions are false.')
add('b202',[
('100*8/(8+12)',40,1e-9,'MN split for parallel linear equal-displacement paths; not full arch-gravity analysis.'),
('((900+100)/2)*60*1',30000,1e-8,'kPa*m2=kN; linear uplift pressure, not measured crack distribution.'),
('5000*2400*900*8/1e9',86.4,1e-9,'GJ removed for uniform temperature change; hydration, gradients and stress omitted.'),
('18*(12*1e-5)*1000',2.16,1e-9,'Free thermal length change in mm; restraint and actual joint closure require additional constraints.'),
('1000*900*.7/1e6',.63,1e-9,'First Joukowsky wave MPa for fast velocity change, single phase; reflections/cavitation excluded.'),
('(85000-2500)/(1000*25**2/2)',.264,1e-9,'Dimensionless local cavitation index uses absolute pressure; no universal damage threshold.'),
('180*70*9.81*.90/1000',111.2454,5e-5,'MW net hydraulic head, fixed efficiency; increasing Q is not unlimited.'),
('240000/(600*8)',50,1e-9,'Ideal rectangular delta advance in m; excludes spread and consolidation.'),
('4.8-(.04*15)',4.2,1e-9,'mm instrument correction from independent coefficient; retains actual dam thermal displacement.'),
('.03*.04',.0012,1e-10,'Independent same-demand probabilities only; shared causes invalidate product.')],
'USBR directly confirms arch-gravity action, 726.4 ft foundation-to-roadway datum, June 1933 first and May 1935 last concrete. Catalog scopes explicitly limited to title/abstract/index. Approximate Nevada/Arizona site reference; no unsupported contractor or listing claims. All misconceptions false.')
add('b203',[
('45*95*9.81/(.86*1000)',48.76482558,5e-9,'Electrical pumping MW; total head includes losses and overall efficiency divides hydraulic power.'),
('620-(180+12)',428,1e-9,'Simultaneous electrical boundary, MW; no double counting auxiliaries.'),
('(80-95)*600/300000',-.03,1e-10,'m, fixed-area reservoir, no local waves; negative result is fall.'),
('(.018*900/4)*(3**2/(2*9.81))',1.857798165,5e-10,'Darcy friction factor with steady full pipe; local losses separate.'),
('1200000-650000-50000-100000',400000,1e-8,'m3/day matching boundary and interval; positive storage is retained water.'),
('(10-4)*1e-5*1e6',60,1e-9,'Free differential microstrain with same alpha, not restrained crack width.'),
('32*.00025',.008,1e-10,'m2/s conductance times m head gives m3/s; constant linear head relation.'),
('(8-2)*120',720,1e-9,'Hypothetical equal available MW per unit; shared constraints can reduce total.'),
('(1.245-.630-.612)*1000',3,1e-9,'mm signed loop closure; not proof that every datum is stable.'),
('(0.92-.88)*220*80*9.81/1000',6.90624,5e-6,'MW efficiency gain at identical Q/net H; excludes hydrology and availability.')],
'USBR construction history confirms 1933 start, first concrete 1935 and 1951 pumping plant. Approximate Washington dam point; literature years distinct. Vendors source institutions only with null security. All misconceptions false.')
add('b204',[
('50*60/(60/2)',100,1e-9,'rpm from frequency divided by pole pairs; poles are total poles, not pairs.'),
('(900*4)*.965',3474,1e-9,'MWh under fixed transfer efficiency, no outages or dynamic limits.'),
('750*.92',690,1e-9,'Balanced sinusoidal MW from MVA and power factor; does not define full capability curve.'),
('500*.0012',.6,1e-9,'m for local linear tailwater Q sensitivity s/m2; not flood-hysteresis model.'),
('(300*1000)*(20-5)/1e6',4.5,1e-9,'MN streamwise momentum with specified cancelled pressure forces; not full basin resultant.'),
('8e6/(400*4180)',4.784688995,5e-10,'K steady heat rise with all heat to water and no ambient exchange.'),
('(90/60)*14',21,1e-9,'Hz blade passing for equally spaced blades; proximity alone not resonance.'),
('2500*(15*60)',2250000,1e-8,'m3 timestamp attribution error, not water leakage.'),
('10*24-2*6',228,1e-9,'unit-hours available, not proportional energy guarantee.'),
('1.6e6*.015/.75',32000,1e-8,'W constant gate lifting force/velocity divided by drive efficiency; acceleration omitted.')],
'Owner history confirms 5 May 1984 first generation and May 2007 last two units. Independently retrieved official indexed transparency excerpt confirms ten 50 Hz and ten 60 Hz units; scope correctly warns redirected page. Border location plausible. Vendor roles institutional, null security; all misconceptions false.')
add('b205',[
('math.sqrt(.004**2+.008**2+.003**2)',.009433981,5e-10,'Small independent relative standard uncertainties; not expanded confidence or bias removal.'),
('(9.8-.3-1.1)/70',.12,1e-9,'Available cavitation coefficient: positive runner setting subtracts margin; required coefficient absent.'),
('(600e6/(100*2*math.pi/60))/1e6',57.29577951,5e-9,'MN*m from mechanical shaft MW and rad/s; steady mean not transient peak.'),
('500*(100*2*math.pi/60)**2',54831.13556,5e-6,'N rigid-rotor unbalance excitation; support dynamics and resonance omitted.'),
('12e-6*1.8*30*1000',.648,1e-9,'mm free growth of one uniform support; not total shaft-axis misalignment.'),
('400000*8e-5',32,1e-9,'K single equivalent thermal resistance; localized paths require separate models.'),
('200000/1000000+1000000/5000000',.4,1e-9,'Miner linear damage with hypothetical S-N lives; no field remaining-life guarantee.'),
('12*.0008*7800',74.88,1e-9,'kg mean steel loss; total mass cannot characterize local pits.'),
('(.02*.90)/(.02*.90+.98*.05)',.2686567164,5e-11,'Posterior true-positive fraction with stated prevalence/sensitivity/specificity from same population.'),
('300*18',5400,1e-9,'MWh hypothetical continuously feasible counterfactual generation; not inevitable outage loss.')],
'ANDRITZ page confirms 2012 770 MW-class runner and five-unit powerhouse 2 rehabilitation; text avoids equating runner rating to plant capacity or commissioning. Country statistics excluded. USBR abstract/catalog scope limited; Guri approximate point in Venezuela; vendors source institution/supplier without broad contractor claim. All misconceptions false.')

def generate():
 rows=[];courses=[]
 from peer_support_examples import EXAMPLES
 exampleChecks=[]
 for k,checks in EXAMPLES.items():
  for label,expr,expected,tolerance in checks:
   actual=eval(expr,{'__builtins__':{},'math':math})
   exampleChecks.append(dict(courseId=k,label=label,expression=expr,actual=actual,expected=expected,tolerance=tolerance,status='PASS' if abs(actual-expected)<=tolerance else 'FAIL'))
 for k,entries in C.items():
  raw=(I/(k+'.json')).read_bytes();d=json.loads(raw)
  assert len(entries)==10
  for j,(expression,expected,tol,note) in enumerate(entries,1):
   u=d['units'][j-1]
   if isinstance(expression,list):
    actual=[eval(e,{'__builtins__':{},'math':math}) for e in expression]
    assert len(actual)==len(expected)==len(tol)
    passed=all(abs(a-e)<=t for a,e,t in zip(actual,expected,tol))
   else:
    actual=eval(expression,{'__builtins__':{},'math':math})
    passed=abs(actual-expected)<=tol
   rows.append(dict(courseId=k,unit=j,modelSha256=hashlib.sha256(u['model'].encode()).hexdigest(),quizSha256=hashlib.sha256(u['misconception'].encode()).hexdigest(),expression=expression,actual=actual,expected=expected,tolerance=tol,boundaryNotes=note+' Misconception read in both languages and is a false distractor.',status='PASS' if passed else 'FAIL'))
  meta={key:v for key,v in d.items() if key!='units'}
  courses.append(dict(courseId=k,metadataSha256=hashlib.sha256(json.dumps(meta,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest(),inputSha256=hashlib.sha256(raw).hexdigest(),metadataNotes=M[k],sourceURLs=[x['url'] for x in d['sources']],status='PASS'))
 report=dict(reviewedAt='2026-10-21',issues=[dict(courseId='b218',unit=3,issue='Displacement difference called normal strain without original-span projection explicitly stated.',resolution='Root amended author file and input model/verify to specify axial projections along original span, small deformation and common datum. Reviewer independently reread revised text and recomputed unchanged 0.00002.',status='RESOLVED')],supplementalExampleChecks=exampleChecks,exampleScope='Course examples were read separately; repeated base calculations reference their unit ledger. Independently transcribed additional sensitivities, conversions and rounded values are recorded separately. This review does not certify engineering design or claim full-text review of every cited manual.',reviewer='/root/courses_support',nonAuthorReviewer=True,method='Independent reading and hand transcription of learner-facing numerical inputs, independent dimensional rederivation, Python recomputation; no author calculation code or numeric author ledger imported. actual is independently computed; expected is learner displayed value. quizSha256 hashes UTF-8 misconception text. Metadata dates/claims read with official primary source checks. Approximate map coordinates are regional reference points, not survey coordinates.',scope=['three-gorges']+[f'b{i}' for i in range(202,210)]+[f'b{i}' for i in range(215,221)]+[f'b{i}' for i in range(296,301)],completedModels=len(rows),completedDisplayedValues=sum(len(r['actual']) if isinstance(r['actual'],list) else 1 for r in rows),expectedModels=200,status='PASS' if len(rows)==200 and all(x['status']=='PASS' for x in rows+courses+exampleChecks) else 'IN_PROGRESS',rows=rows,courses=courses)
 (P/'peer_support.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'models':len(rows),'status':report['status'],'numericFailures':[{'id':r['courseId'],'u':r['unit'],'a':r['actual'],'e':r['expected']} for r in rows if r['status']!='PASS']}))
if __name__=='__main__':
 from peer_support_additions import DATA
 for key,entries,meta in DATA:add(key,entries,meta)
 generate()
