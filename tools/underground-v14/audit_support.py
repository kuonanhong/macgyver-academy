#!/usr/bin/env python3
"""Author's separate arithmetic check: one independently expressed result per unit.
Does not claim to validate site design or source project data. Inspect report for scope.
"""
import math,json,hashlib,pathlib
P=pathlib.Path(__file__).resolve().parent
pi=math.pi;sqrt=math.sqrt;sin=lambda d:math.sin(math.radians(d));tan=lambda d:math.tan(math.radians(d));atan=lambda x:math.degrees(math.atan(x))
# Each row lists independently recalculated outputs followed by displayed values.
R={
151:([.1*4/.15,.6/1.2,12*.82,25/.025/1000,.012/.3,15/100,200/(pi*.05**2)/1000,10000*.8/4000,(.3-.18)/30,18/20],[2.67,.5,9.84,1,.04,.15,25.46,2,.004,.9]),
152:([18/30,20*25,3000*.1*.1**2/6,100*math.cos(pi/3),80*.01,5/35,.5*.2,60/sqrt(9),420/500,7/8],[.6,500,.5,50,.8,.143,.1,20,.84,.875]),
153:([26*4/2,314*500/1000,pi*.05*2*.3*1000,80/.02/1000,100000*2000/(200000*314),100/.1/1000,(2.4-1.8)/10,(100-96)/100,(18/20)**2,8/10],[52,157,94.25,4,3.18,1,.06,.04,.81,.8]),
154:([.08*4*.75*1000,240*.05,pi*pi*200e9*2e-6/4/1000,9/.3,100/2,240/.4,10e9*.1/1e6,300*.02,(8-6)/8,46/50],[240,12,987,30,50,600,1000,6,.25,.92]),
155:([30*9/8,pi*(.114**4-.102**4)/64,.35-.114,12-9,12*tan(1),pi*(.17**2-.114**2)/4*12,10000*.005,12-4,2/500,180/300],[33.75,2.98e-6,.236,3,.209,.150,50,8,.004,.6]),
156:([12/6000,80/40,500*600/1000,pi*.04*4*.20*1000,12-7,10*tan(.5),.08/.2,(18-6)/3000,40*1.5,15/5],[.002,2,300,100.5,5,.0873,.4,.004,60,3]),
157:([1000*9.81*20/1000,5/100,1.6/2,300/50,300*288/293,100/1000,5/100,18/20,6/20,48/50],[196.2,.05,.8,6,294.9,.1,.05,.9,.3,.96]),
158:([5.3-5,24*3,1.1**4,360/.6,80*8,pi*(5.3**2-5**2)*10,1.5/6,20000*.0002,110-70,12/6],[.3,72,1.4641,600,640,97.08,.25,4,40,2]),
159:([.15*4,600*.03,.5*400,1200/6,12/3,60/.12,9.81*5*10,4/8000,.6-.2,.4-.05],[.6,18,200,200,4,500,490.5,.0005,.4,.35]),
160:([100**2/(2*50000)*1000,.5*100*5**2/1000,150*.2,.18-.1,1000*9.81/1000,5000*.002,min(300,180,250),24/6,3/20,150*.08],[100,1.25,30,.08,9.81,10,180,4,.15,12]),
161:([26*500/1000/3,20*(.08-.03),200*.15,.2-.14,15/3,4*20,35/50,2/50,.02*365,5/6],[4.33,1,30,.06,5,80,.7,.04,7.3,.833]),
162:([(120-100)/100,4/100,25/.005/1000,8/20,.2*1440,.02*2,100-65,.5*24,9.81*3,9/12],[.2,.04,5,.4,288,.04,35,12,29.43,.75]),
163:([9.81*80/1000,.9+.0981-.15,(.8481-.7848)*1000,1.1**3,pi*(.5**2-.05**2)*3*.1,.2/.04,(10-2)/10,.002/10,8/10,36/40],[.7848,.8481,63.3,1.331,.233,5,.8,.0002,.8,.9]),
164:([80-25,.020*.8*1000,.07069*.075**(2/3)*sqrt(.005)/.013,1000*9.81*.055*20/.7/1000,.055*600,2*40,.8**(8/3),2/.5,.05*.2*3600,(18-21)/6],[55,16,.0684,15.4,33,80,.5515,4,36,-.5]),
165:([12-14,.5*1440,.35-.2,(.15/.2)**3,.4/200,.8/1.6,9.81*3,.1*500*86400/1e6,3/4,4/20],[-2,720,.15,.4219,.002,.5,29.43,4.32,.75,.2]),
166:([100*14*8,.5*.33*18*8**2,200e9*.01*12e-6*10/1000,9.81*5*100,6000/4905,4/80,900/6,6/12000,20*2,sqrt(.01**2+.02**2+.02**2)],[11200,190.1,240,4905,1.223,.05,150,.0005,40,.03]),
167:([30e9*.3/20/1e6,(4/8)**2,3000*.025,.6-.2,900/.3/1000,18*2,9.81*4,18-11,9.81*12*100,11/12],[450,.25,75,.4,3,36,39.24,7,11772,.917]),
168:([25000*2.4,60000/1.025,3+8-9.5,6000/60000,500/(1.025*4000),.5*10.055*8*16,1e-5*12*30,.5*1025*200*1.5**2/1000,100*60**2/8,600/60000],[60000,58536.6,1.5,.1,.122,643.5,.0036,230.6,45000,.01]),
169:([40*1*200,20000/4000,.0002*50*5,20/200000,4000*.6,4/.5,20000/200,sqrt(.02**2+.03**2+.02**2),.5*1025*4,3800/4000],[8000,5,.05,.0001,2400,8,100,.0412,2050,.95]),
170:([30*.0005,40/100,.2*100,.2*.3*1000,1e-5*200*15,.02/200*10,1000/.5/1000,12/30,180/240,18/20],[.015,.4,20,60,.03,.001,2,.4,.75,.9]),
171:([(8*5-7*4)*24*20,25*.12,.15*5760,50*49/8,600/2,3000/1+150/.2,.04/20,.005*40*20,8/10000,120/720],[5760,3,864,306.25,300,3750,.002,4,.0008,.167]),
172:([250*pi*1.5**2/4,.05*(1300-1100)/(2650-1100),pi*1.5**2/4*.5,5*pi*1.5*100,1200/.3/1000,.003*100,.03*(200/.15)*1200*4/2,sqrt(2*pi)*4*.003,1000*9.81*12*1.5/1000,12/30],[441.8,.00645,.8836,2356,4,.3,96000,.0301,176.6,.4]),
173:([120*8+400,8*20*.01,1.5*600,.52-(.4+.1),2e6*100/(30e9*.4),200/.025/1000,2*1000*sin(1),150*.2,(1200-1000)/(4-2),(1.42/1.5)**2],[1360,1.6,900,.02,.0167,8,34.90,30,100,.8962]),
174:([3*sin(5),100*tan(.1),3/(.5*pi/180),.3/.5,atan(.5/20),200*tan(.02*.5),sqrt(.3**2+.4**2)-.1-.15,.02/(pi*(.6**2-.4**2)/4),.4/(2*200)+20/200000,sqrt(.05**2+.03**2+.04**2)],[.2615,.1745,343.8,.6,1.432,.0349,.25,.1273,.0011,.0707]),
175:([8000-3000-3500-1000,15*pi*10*20,6000/(pi*(100-81)/4),.02/10,8/5,.0001*100*10,.1/(1/60),9.81*10*pi*100/4,2/20,12000/(9.81*1000)],[500,9425,402.1,.002,1.6,.1,6,7705,.1,1.223])}
checks=[]
for cid,(calcs,expected) in sorted(R.items()):
 assert len(calcs)==len(expected)==10
 for unit,(a,b) in enumerate(zip(calcs,expected),1):
  assert math.isclose(a,b,rel_tol=.004,abs_tol=1e-12),(cid,unit,a,b)
  checks.append(dict(course=f'b{cid}',unit=unit,recalculated=a,displayed=b,result='pass',roundingToleranceRelative=.004))
files=[P/'inputs'/f'b{i}.json' for i in range(151,176)]
report=dict(reviewed='2026-10-21',reviewer='course author; independent expression self-check, not external certification',coverage=dict(courses=25,models=250,primaryNumericResults=250,unitScope='b151-b175, units 1-10 each',secondaryResults='manually reread alongside model formulas',limits='Arithmetic, dimensions and teaching boundary review only; no site design verification.'),boundaryChecks=['b160: static serial-force minimum is not system energy absorption; remaining work uses calibrated force and travel.','b168: tonnes denote mass; displacement and free-surface terms use compatible density and units.','b169: bed contact and differential settlement; no circular-ring assumption for immersed elements.','b170: pressure times seal span is transverse resultant, not membrane tension.','b172: slurry solids exclude recirculated carrier solids; equivalent-Newtonian pressure loss is illustrative.','b174: utility uncertainty deducted before radii; endpoint closure does not bound intermediate path error.','b175: upward gradient decreases effective stress; raw uplift ratio is not a code safety factor.','Heathwall is a 2013 proposed method; Cremorne is explicitly a non-caisson comparison.'],checks=checks,inputSha256={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in files})
(P/'audit_support.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('250/250 independently expressed primary outputs agree within displayed rounding; input hashes saved.')
