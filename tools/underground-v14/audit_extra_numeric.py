#!/usr/bin/env python3
"""Independent arithmetic review of the authored b196–b200 examples.
Reported values are transcribed from prose; references are recomputed in SI-compatible units.
This verifies arithmetic and explicitly reviewed boundaries, not field design adequacy.
"""
from pathlib import Path
import hashlib, json, math, re
radians=math.radians
cos=lambda d:math.cos(radians(d));tan=lambda d:math.tan(radians(d))
checks={
'b196':[(4905,9.81*500,.001),(78.48,9.81*8,.001),(.815,4000/4905,.0005),(200,(6000-4000)/10,.001),(1500,15*100,.001),(5886,9.81*200*3,.001),(160,80*4**2/8,.001),(2500,5000*.5,.001),(2943,9.81*300,.001),(500,7000+1000-7500,.001)],
'b197':[(25,65-40,.001),(666,1000*cos(30)-200,.05),(384.5,666*tan(30),.05),(187.9,200*cos(20),.05),(6,18-12,.001),(196.2,1000*9.81*20/1000,.001),(57.7,100*tan(30),.05),(10,5/cos(60),.001),(.5,3/6,.001),(12,100*(250-220)/250,.001)],
'b198':[(.1,.3/math.sqrt(9),.00001),(1.5,.1*30/2,.0001),(28.28,2*math.hypot(1,1)/.1,.005),(.2,1e8/5e8,.0001),(.135,math.exp(-2),.0005),(.20,(math.sqrt(9)-math.sqrt(4))/(math.sqrt(9)+math.sqrt(4)),.0001),(2,100*(10.2-10)/10,.0001),(10,100*.01/.1,.0001),(.158,math.hypot(30*.01/2,.1*1/2),.0005),(75,100*18/24,.0001)],
'b199':[(.6,6/10,.0001),(6.59,2*3000/(1-.3**2)*.01**3*1000,.005),(15,.6*.3/(2*.006),.001),(.579,(5/6)**3,.0005),(.90,1-20/200,.0001),(.50,1500/3000,.0001),(1.345,1.5*.96**(8/3),.0005),(.00785,math.pi*.1**2/4,.000005),(36,.02*1800,.0001),(95,100*19/20,.0001)],
'b200':[(.2,2/10,.0001),(.2,.02*1000*.01,.0001),(125.7,2*math.pi*1*20,.05),(7.57,20*780*.85/(.2*8760),.005),(36,12*3,.001),(.40,.2*2,.0001),(360,.1*3600,.001),(.2,1/5,.0001),(3,.60/.20,.0001),(1752,.20*8760,.001)]}
HERE=Path(__file__).resolve().parent
records=[]
for cid,rows in checks.items():
 course=json.loads((HERE/'inputs'/f'{cid}.json').read_text('utf-8'));assert len(course['units'])==len(rows)==10
 for unit,(reported,reference,tolerance) in enumerate(rows,1):
  assert abs(reported-reference)<=tolerance,(cid,unit,reported,reference)
  model=course['units'][unit-1]['model']
  for text in model.split('~'):
   numbers=[float(v) for v in re.findall(r'\d+(?:\.\d+)?(?:[eE][+-]?\d+)?',text.replace(',',''))]
   assert any(abs(v-reported)<1e-9 for v in numbers),(cid,unit,'transcribed result missing from visible model')
  records.append({'course':cid,'unit':unit,'reported':reported,'independentReference':reference,'absoluteTolerance':tolerance,'reviewedModelSha256':hashlib.sha256(model.encode()).hexdigest(),'status':'PASS'})
report={'date':'2026-10-21','scope':'50 prose numerical examples; independent arithmetic and unit review. No project design certification.','reviewedBoundaries':['Displaced sealed envelope differs from concrete volume; uplift margins are unfactored.','Joint/face angle difference is not slope factor of safety; force projections do not include extra friction.','GPR depth uses corrected two-way time; contrast sign depends on field convention; amplitude is not energy.','Thin ideal ring external pressure is not field allowable pressure; liner stiffness scales with thickness cubed.','Anode Ceff already includes electrochemical efficiency; annual Ah differs from current and annual rate.'],'records':records}
(HERE/'research'/'independent-extra-numeric.json').parent.mkdir(exist_ok=True)
(HERE/'research'/'independent-extra-numeric.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n','utf-8')
print('PASS independent arithmetic review: 50 authored examples b196–b200; units and model boundaries reviewed.')
