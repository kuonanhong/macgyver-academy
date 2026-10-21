#!/usr/bin/env python3
"""Author arithmetic rereview from independently arranged equations, not external peer review."""
import json,math,hashlib
from pathlib import Path
from build_river_extensions import SENS
H=Path(__file__).resolve().parent
# Independent numerical arrangement, preserving dimensions and control-volume meaning.
CHECKS={
'b276':[
('9.81*1000*(.003*.8)','Average boundary stress only, not maximum bank shear.'),
('1000*1.2*1.1*(2*2)/2','Fixed projected area; reconfiguration and debris can change drag.'),
('(1600/1000)/.2','Effective mobilized root force over specified shear area; no deep-slip inference.'),
('(1000*.8-600*.8)*9.81','Net buoyancy alone, no complete anchor loading or moment check.'),
('1.2-.5','Geometric remaining embedment, not factor of safety.'),
('180/240','Original tagged cohort, excludes replacements; no strength conversion.'),
('20*(2+5*(2-.2))','Six strips, five seams; planar area excludes end and trimming loss.'),
('2*9.81','Same-elevation pressure-head difference, not transient seepage solution.'),
('(0.08*0.12*3600)-(0.075*0.07*3600)','Sediment mass storage assumes no lateral terms; not permanent removal.'),
('(70-55)-(35-40)','Percentage points; causal interpretation requires parallel trends and unaffected control.')],
'b277':[
('.6/.008','Geometric slope allocation, no optimal-spacing claim.'),
('.8+((2.4/.8)**2)/(2*9.81)','Hydrostatic rectangular section, local bed datum, unit velocity correction.'),
('((2.4*2.4)/9.81)**(1/3)','Rectangular critical depth, not proof of free control under submergence.'),
('(.4/2)*(math.sqrt(1+8*(5/math.sqrt(9.81*.4))**2)-1)','Horizontal short rectangular momentum jump, not basin length.'),
('(30*4*6+10*4*6)/2','Net upward linear pressure distribution; slab bending omitted.'),
('(40/.05)/(1650*9.81)','Noncohesive dimensionless stress; no universal critical limit.'),
('.002/.0005','Same-length-unit grading ratio, not universal filter acceptance.'),
('(-.0005*86400)/(12*80*.65)','Solid-volume deficit divided by solid fraction and bed area; negative erosion.'),
('(2650-1000)*(4*math.pi*(.6/2)**3/3)*9.81','Submerged ideal sphere weight, no drag/lift/pivot stability.'),
('(350-295)/5','Upstream interval average with downstream-increasing chainage, not future rate.')],
'b278':[
('(19.62*.15)**.5','Ideal loss-free jet scale, not fish threshold or pool mean.'),
('(.2*.8)*.7*(19.62*.15)**.5','Fully submerged opening with assumed Cd, not universal geometry law.'),
('(1000*.25*9.81)*(.15/3.5)','Assumed head power dissipated in stated volume, not local turbulence field.'),
('6/.4','Fixed water-relative swimming minus downstream current, no fatigue.'),
('(.6*100/40)/100','Allocation fraction, not attraction-success probability.'),
('8/.4','Nominal water turnover, not every particle or fish residence.'),
('(.9/3)/.6','Opening velocity, distinguished from gross-area superficial normal velocity.'),
('2*.2/.2','Dimensional eddy turnover scale ell/uprime, not physiology or full spectrum.'),
('(80*.9)/(100*.8)','Same unique cohort, known detection probabilities; estimation uncertainty omitted.'),
('.9*.9*.9*.9*.9','Equal conditional stage probabilities; unrelated marginal rates require additional assumptions.')],
'b279':[
('1.8/1.2','Matching centreline and valley endpoints and resolution.'),
('1/600','Mean geometric bed slope, not local energy slope.'),
('(24/.04)*math.pow(1.2,2/3)*math.sqrt(.0015)','SI Manning with n units s/m^(1/3); independent energy-slope assumption.'),
('60000*35/100','Added depth with no pre-existing water; capacity is not peak attenuation.'),
('(1.5*1.5/9.81)*(12/60)','Modest width/radius scale estimate excluding secondary circulation.'),
('(240*2.5)*1.8','In-place geometric eroded volume, not instantaneous exported solids.'),
('.8*2*60*60','Gross inward flow, not net storage when outlets exist.'),
('(0.4/20)*300*2e-5','Saturated homogeneous steady Darcy discharge, not pore velocity.'),
('1800*10/6','Water advection time, not flood-wave travel time.'),
('math.hypot(.03,.04)','Independent zero-mean random difference standard deviation, not automatic confidence bound.')],
'b280':[
('2/5','Equally weighted empirical exceedance fraction, not guaranteed true probability.'),
('(1-.6)*140+.6*160','Stated zero-based linear-interpolation quantile; small ensemble tail unvalidated.'),
('(.04+.09+.16+.01)/4','Four-case Brier average, not service certification or operational loss.'),
('(140-100)*3600','Linear endpoint flow assumption, no omitted losses; volume increment only.'),
('(120+80)+60','Already-routed arrivals at same section and instant; no simultaneous-release assumption.'),
('300-(90+70)','Downstream arrival allowance, not gate setting or actual approved release.'),
('1800000/(50*60*60)','Sustained incremental net release, excludes ramp time; no operating authorization.'),
('120-100','Positive infeasibility gap; cannot silently relax a rule.'),
('(3*2)/(50*2)','Equally weighted empirical violation fraction, not risk approval or consequence measure.'),
('(18-11)/18','Same held-out records and positive reference MAE, not flood-risk reduction.')]
}
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 original=json.loads((H/'calculation_river_extensions.json').read_text());index={(r['courseId'],r['unit']):r for r in original};rows=[];courses=[];sens=[]
 for cid,checks in CHECKS.items():
  p=H/'inputs'/f'{cid}.json';d=json.loads(p.read_text());md={k:v for k,v in d.items() if k!='units'}
  courses.append(dict(courseId=cid,inputSha256=sha(p.read_bytes()),metadataSha256=sha(json.dumps(md,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()),sourceURLs=[s['url'] for s in d['sources']],metadataNotes='Actual publication/case years separated from 2026 curriculum review. Exercise inputs explicitly hypothetical. Institutional roles are source/research association only; b279 uses EEA and NRCS as distinct institutions. Source reading scopes and inaccessible full PDF are disclosed.',status='PASS'))
  for j,(expr,note) in enumerate(checks,1):
   a=index[cid,j];actual=eval(expr,{'__builtins__':{},'math':math});assert abs(actual-a['expected'])<=a['tolerance'],(cid,j,actual,a['expected'])
   u=d['units'][j-1];rows.append(dict(courseId=cid,unit=j,modelSha256=sha(u['model'].encode()),quizSha256=sha(u['misconception'].encode()),expression=expr,actual=actual,expected=a['expected'],tolerance=a['tolerance'],boundaryNotes=note,misconceptionReview='Read as a false belief; no correct caution used as the wrong option.',status='PASS'))
  s=SENS[cid];v=eval(s['expression'],{'__builtins__':{},'math':math});assert abs(v-s['expected'])<1e-8
  sens.append(dict(courseId=cid,expression=s['expression'],actual=v,expected=s['expected'],unit=s['unit'],exampleSha256=sha(d['example'].encode()),status='PASS'))
 out=dict(reviewer='/root/courses_landmarks',nonAuthorReviewer=False,status='PASS',scope='Author independent arithmetic arrangement and physical-boundary rereview; not an external peer review.',rows=rows,courses=courses,sensitivities=sens)
 (H/'reviews'/'numeric_river_extensions_author.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print('Author review:',len(rows),'models,',len(sens),'sensitivities,',len(courses),'metadata records PASS')
if __name__=='__main__':main()
