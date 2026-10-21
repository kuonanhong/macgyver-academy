"""Independent peer arithmetic authored from displayed model text, not author audits."""
import json,math,hashlib
from pathlib import Path
P=Path(__file__).resolve().parents[1]
def sha(b):return hashlib.sha256(b).hexdigest()
R={
256:[
('2*math.pi*math.sqrt(50000000/2000000000)',.9935,.00005,'s; paired generalized modal mass and stiffness; period matching does not verify stress. False quiz rejects this inference.'),
('50000000*.2*9.81/1e6',98.10,.005,'MN; selected absolute acceleration, not surface PGA; quiz false for nonuniform structure response.'),
('2*.05*math.sqrt(2e9*5e7)',31622776.6,.05,'N s/m; viscous linear modal damping only; larger damping is not automatically truer.'),
('1/math.sqrt((1-1**2)**2+(2*.05*1)**2)',10,1e-10,'Dimensionless steady harmonic displacement magnification at resonance, not a finite earthquake peak factor.'),
('.4*9.81/(2*math.pi/1)**2',.09940,.000005,'m; pseudo-spectral acceleration at matching oscillator and damping, not arbitrary acceleration peak.'),
('(.1*(2*math.pi)*(6*math.pi)/(8*math.pi))/(2*4*math.pi)+(.1/(8*math.pi))*(4*math.pi)/2',.04375,1e-10,'Rayleigh damping dimensionless; alpha inverse seconds and beta seconds. Two fits do not imply a constant curve.'),
('2*math.pi*math.sqrt(7e7/2e9)',1.1755,.00005,'s; assumed equivalent modal added water mass with unchanged stiffness, not whole reservoir mass.'),
('12-(-8)',20,1e-10,'mm; simultaneous local-normal displacement difference with orientation fixed, not quadrature of separate peaks.'),
('.2/.005',40,1e-10,'points per cycle; dimensional temporal resolution only, not convergence or input-bandwidth proof.'),
('100-60',40,1e-10,'kPa; fixed total stress with excess pore pressure. ru=0.6 is not global liquefaction; false quiz confuses soil mechanism with damping.')],
257:[
('8/40',.20,1e-10,'m; undistorted common length ratio; another stated length80/40=2m. Visual likeness insufficient.'),
('8/math.sqrt(40)',1.2649,.00005,'m/s; equal-g Froude similarity only, not Reynolds similarity.'),
('1000/40**2.5',.09882,.000005,'m3/s; total flow scales L^(5/2), distinct from unit-width L^(3/2).'),
('120/math.sqrt(40)',18.974,.0005,'s; gravity-similar physical process, recording relabeling cannot fix incorrect actuation.'),
('60/40',1.5,1e-10,'kPa; matched-density gravity gauge pressure, not absolute atmospheric or cavitation similarity.'),
('2e6/40**3',31.25,1e-10,'N; integrate gravity pressure over area; shell/sensor dynamics and air impact excluded.'),
('(8/math.sqrt(40))*.2/1e-6',252982,.5,'Dimensionless Re using hydraulic-depth reference specified; prototype Re64e6. High bulk Re does not prove gap similarity.'),
('1000*1.6*.2/.072',4444.4,.05,'Dimensionless Weber; prototype/model is40^2=1600 at equal fluid, not preserved surface tension.'),
('.0005*40',.020,1e-10,'m standard uncertainty; exact assumed scale and coherent bias separate. Amplified measurement uncertainty cannot be ignored.'),
('math.sqrt(((.098-.1)**2+(.100-.1)**2+(.102-.1)**2)/2)/.1*100',2,1e-10,'percent sample coefficient of variation, n−1 denominator. Independent repeats do not remove systematic bias or validate untested conditions.')],
258:[
('100*1800',180000,1e-8,'m3 transferred; upper loses and lower gains equally, external exchanges excluded.'),
('180000/600000',.3,1e-10,'m; local constant-area approximation, different reservoirs need separate storage curves.'),
('600-200-15',385,1e-10,'m net generating head; losses subtract in generation and add in pumping.'),
('1000*9.81*100*385*.9/1e6',339.9165,.00005,'MW; overall efficiency applied to hydraulic power at stated head and flow, not nameplate guarantee.'),
('1000*9.81*100*415/.88/1e6',462.631,.0005,'MW electrical input divides by pumping efficiency; gravity9.81SI, auxiliaries explicitly separate.'),
('.88*.9',.792,1e-10,'dimensionless efficiency; equal constant head and closed cycle inventory, unlike adjacent unequal-head examples.'),
('720000/100/3600',2,1e-10,'hours at constant discharge from usable transferable volume; not constant electrical power.'),
('(0+100)/2*300',15000,1e-8,'m3; linear ramp integrated, neither transient pressure nor actuator safety established.'),
('1000000*.004',4000,1e-8,'m3 per day; specified daily evaporation over combined water surface, closed loop still has weather fluxes.'),
('800000-200000',600000,1e-8,'m3 remaining transferable inventory if other constraints permit; reservations cannot be double committed.')],
259:[
('2*2/(2*.020)',100,1e-10,'MPa; thin-wall gauge pressure2MPa D/t100 approximation away from supports, not buckling or weld proof.'),
('2*2/(4*.020)',50,1e-10,'MPa; closed-end membrane and no axial restraint. Fixed segments need Poisson/anchor model.'),
('2*2e6*(math.pi*2**2/4)*math.sin(math.pi/4)/1e6',8.8858,.00005,'MN; equal pressure vectors through90deg turn with momentum and weight excluded, vector direction noted.'),
('12e-6*100*30',.036,1e-10,'m; free uniform thermal expansion, not displacement possible between fixed anchors.'),
('200e9*12e-6*30/1e6',72,1e-10,'MPa compressive magnitude under full linear-elastic restraint, not yielding/sliding prediction.'),
('9.81*(7850*math.pi*(2.04**2-2**2)/4+1000*math.pi)/1000',40.593,.0005,'kN/m; exact steel annular area and water inner area, horizontal full pipe, external buoyancy excluded.'),
('40*10**2/8',500,1e-10,'kN m; uniform simply supported beam, reactions200kN; does not resolve saddle shell stress.'),
('.15*400',60,1e-10,'kN limiting Coulomb resistance, actual static friction may be lower; false quiz intentionally equates them.'),
('2000/4',500,1e-10,'kPa mean centered pressure in full contact; not allowable strength or overturning evaluation.'),
('100*20/18',111.11,.005,'MPa uniform-thinning membrane stress; reciprocal thickness, local pitting not represented.')],
260:[
('math.sqrt((2.2e9/1000)/(1+2.2e9*2/(200e9*.02)))',1023.53,.005,'m/s; thin elastic pipe, factor1 explicit; gas/restraint can change wave speed.'),
('2*1000/1000',2,1e-10,'s elastic round trip of specified path; no universal acceptable valve time.'),
('1000*1000*1/(1000*9.81)',101.94,.005,'m increment corresponding1MPa for rapid single-phase change0.5s<2s; initial pressure and reflections separate.'),
('(20-5)/100',.15,1e-10,'m/s instantaneous continuity at shaft; does not presume persistent imbalance.'),
('2*math.pi*math.sqrt(1000*100/(9.81*10))',200.607,.0005,'s lossless small rigid-column mode with fixed reservoir and negligible shaft inertia, distinct from acoustic time.'),
('2*math.sqrt(1000*10/(9.81*100))',6.3855,.00005,'m ideal energy upsurge from initial equal levels, instantaneous demand stop, no friction or elastic energy.'),
('.02*(1000/2)*2**2/(2*9.81)',2.0387,.00005,'m positive loss magnitude; applied force must oppose signed flow after reversal.'),
('(10/(.65*2))**2/(2*9.81)',3.0159,.00005,'m quasi-steady orifice head at stated coefficient and area; local cavitation not checked.'),
('100-80-2.34',17.66,.005,'kPa local absolute-pressure margin over vapor; negative gauge alone not vapor criterion.'),
('1000*.1/100',1,1e-10,'dimensionless Courant1 aligns characteristics on uniform grid, not complete model validation.')],
293:[
('3000*10',30000,1e-8,'m3 for vertical chamber and fixed floating displacement; vessel displacement cancels between endpoints.'),
('(3000*10+6000*4)/(3000+6000)',6,1e-10,'m weighted equilibrium on common datum with fixed areas; transfer3000*(10−6)=12000m3.'),
('1000*9.81*(3000*6000/(3000+6000))*6**2/2/1e6',353.16,.005,'MJ potential loss between resting endpoints, no recovery/external work. Water reuse is distinct from energy efficiency.'),
('18000/30000*100',60,1e-10,'percent internal reuse of stated gross exchange; external12000m3, not comparison with different lock sizes.'),
('.020*86400',1728,1e-8,'m3 daily constant leakage integrated over time, not field allowance or per-cycle loss.'),
('12000*.005',60,1e-10,'m3/day from stated daily evaporation depth and fixed exposed area, not multiplied by lockage count.'),
('.7*4*math.sqrt(2*9.81*2)',17.54,.005,'m3/s instantaneous effective orifice law; constant flow cannot persist to equalization.'),
('2*(math.sqrt(6)-math.sqrt(.1))/(.7*4*math.sqrt(2*9.81)*(1/3000+1/6000))',688.0,.05,'s; integrate both moving levels with constant areas and Cd to finite head0.1m, not operational valve timing.'),
('6000*.010',60,1e-10,'m3 coherent storage bias, not reduced by averaging independent readings sharing same datum.'),
('((30000*(1-.4))/(30000*(1-.6))-1)*100',50,1e-10,'percent makeup increase; reuse decreases20 percentage points with fixed gross volume, different denominator.')]
}
EXTRAS={
256:[('math.sqrt(2e9/5e7)',6.325,.0005),('.1*(2*math.pi)*(6*math.pi)/(8*math.pi)',.47124,.000005),('.1/(8*math.pi)',.0039789,.00000005),('2*math.pi*math.sqrt(5e7/2.2e9)',.9472,.00005),('(1-1/math.sqrt(1.1))*100',4.65,.005)],
257:[('1000/44**2.5',.07787,.000005),('(1-1/1.1**2.5)*100',21.20,.005)],
258:[('1000*9.81*100*423.5*.9/1e6',373.90815,.000005)],
259:[('40*10/2',200,1e-10),('(20/18-1)*100',11.11,.005)],
260:[('2*math.sqrt(1000*10/(9.81*110))',6.0883,.00005)],
293:[('3300*10*(1-.6)',13200,1e-8)]}
def run(status='IN_PROGRESS',metadata=None):
 rows=[];courses=[];extra=[]
 for cid,items in R.items():
  d=json.loads((P/'inputs'/f'b{cid}.json').read_text())
  for i,(ex,exp,tol,notes) in enumerate(items,1):
   actual=eval(ex,{'__builtins__':{},'math':math})
   assert abs(actual-exp)<=tol+1e-10,(cid,i,actual,exp,tol)
   u=d['units'][i-1];rows.append(dict(courseId=f'b{cid}',unit=i,modelSha256=sha(u['model'].encode()),quizSha256=sha(u['misconception'].encode()),expression=ex,actual=actual,expected=exp,tolerance=tol,boundaryNotes=notes+' Both-language model and false misconception read independently; no author calculation table used.',status='PASS'))
  for ex,exp,tol in EXTRAS[cid]:
   a=eval(ex,{'__builtins__':{},'math':math});assert abs(a-exp)<=tol,(cid,ex,a,exp)
   extra.append(dict(courseId=f'b{cid}',expression=ex,actual=a,expected=exp,tolerance=tol,status='PASS'))
  courses.append(dict(courseId=f'b{cid}',inputSha256=sha((P/'inputs'/f'b{cid}.json').read_bytes()),metadataSha256=sha(json.dumps({k:v for k,v in d.items() if k!='units'},sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()),metadataNotes=(metadata or {}).get(str(cid),'Numerical review complete; independent source and metadata review underway.'),sourceURLs=[s['url'] for s in d['sources']],status='PASS' if metadata else 'IN_PROGRESS'))
 report=dict(reviewer='/root/courses_ground',nonAuthorReviewer=True,status=status,reviewed='2026-10-21',rows=rows,courses=courses,extraChecks=extra,scope='60 independent model recalculations and false-quiz reviews, with separately recomputed secondary values and sensitivity examples; exact current file/model/quiz/metadata hashes.')
 (P/'reviews'/'peer_ground.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(len(rows),'models and',len(extra),'secondary values independently recalculated')
if __name__=='__main__':run()
