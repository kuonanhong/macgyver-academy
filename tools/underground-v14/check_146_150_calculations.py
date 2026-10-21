#!/usr/bin/env python3
"""Independent arithmetic ledger for the 50 authored teaching models; not engineering design checks."""
import json,math,pathlib
H=pathlib.Path(__file__).resolve().parent
rows={
'b146':[
 ('travel and rings',[1.8-.3,math.floor((1.8-.3)/1.2)],[1.5,1]),
 ('contact MPa',[8/4,8/2],[2,4]),
 ('friction MN and ratio',[.4*8,.4*8/2.8],[3.2,1.14]),
 ('shoe MN and MPa',[12/24,(12/24)/.1],[.5,5]),
 ('parallel minutes and saving percent',[max(30,25)+5,30+25+5,(60-35)/60*100],[35,60,41.7]),
 ('shield friction MN',[.3*.2*math.pi*6*4,.3*.2*math.pi*6*6],[4.52,6.79]),
 ('angle rad and degrees',[.010/5,math.degrees(.010/5)],[.002,.115]),
 ('specific energy kWh/m3 and MJ/m3',[800*.5/40,800*.5/40*3.6],[10,36]),
 ('advance m/day',[5*2*60*20*.5/1000,5*2*60*20*.4/1000],[6,4.8]),
 ('verified percent and unresolved',[114/120*100,120-114],[95,6])],
'b147':[
 ('block weight kN',[2.4*26],[62.4]),
 ('exposure hours',[6/.8,6/.4],[7.5,15]),
 ('bolt projected kN',[4*60*math.cos(math.radians(30))],[207.8]),
 ('elastic strip MPa',[6*2/(1*.12**2)/1000,6*2/(1*.10**2)/1000],[.833,1.2]),
 ('simple-beam mm and ratio',[5*20*3**4/(384*50000)*1000,5*20*4**4/(384*50000)*1000,(4/3)**4],[.422,1.333,3.16]),
 ('rate mm/hour and difference std mm',[(11-8)/6,math.hypot(.3,.3)],[.5,.424]),
 ('in-situ overbreak m3',[math.pi*(6.1**2-6**2)*2/4],[1.901]),
 ('stored m3 and fill hours',[(80-65)*2,20/(80-65)],[30,1.33]),
 ('mixing seconds',[600/20,math.log(10)*600/20],[30,69.1]),
 ('sampling percent',[20/100*100,1/10*100],[20,10])],
'b148':[
 ('curve intersection mm and MPa',[(.6+.1)/(.02+.01),.6-.02*((.6+.1)/(.02+.01))],[23.33,.133]),
 ('largest fraction percent and volume m3',[30/80*100,30*1],[37.5,30]),
 ('compression MPa and nominal ratio',[300/.2/1000,(300/.2/1000)/2],[1.5,.75]),
 ('edge MPa',[200/.25/1000+6*10/.25**2/1000,200/.25/1000-6*10/.25**2/1000],[1.76,-.16]),
 ('increment mm',[600/20,600/60],[30,10]),
 ('strain microstrain',[300/(6e6*.25)*1e6,300/(12e6*.25)*1e6],[200,100]),
 ('exponential convergence mm',[20*(1-math.exp(-5/5)),20*(1-math.exp(-10/5))],[12.64,17.29]),
 ('water resultant kN',[150*2],[300]),
 ('nonunique displacement mm',[500/50,1000/100],[10,10]),
 ('defect fraction percent',[8/200*100],[4])],
'b149':[
 ('support reaction kN',[900/2,900*.6,900*.4],[450,540,360]),
 ('exposure days',[12/2,12/2+3],[6,9]),
 ('bearing kPa',[600/1.2,600/.8],[500,750]),
 ('core volume m3 and fraction percent',[60*4,12*4,12/60*100],[240,48,20]),
 ('rotation rad and degrees',[.004/6,math.degrees(.004/6)],[.000667,.0382]),
 ('mass t and loose m3',[25*1.5*2400/1000,25*1.5*1.4],[90,52.5]),
 ('catch-up days and equal-speed relative m/day',[20/(3-2),2-2],[20,0]),
 ('mean std mm and unchanged common bias',[1/math.sqrt(4),2],[.5,2]),
 ('Darcy m3/s and m3/h',[.0001*15*8/12,.0001*15*8/12*3600],[.001,3.6]),
 ('clearance m',[5.2-5.05-.03],[.12])],
'b150':[
 ('simple beam moment kN m',[30*8**2/8,30*4**2/8],[240,60]),
 ('resultant and eccentricity m',[(600*2+400*10)/1000,6-(600*2+400*10)/1000],[5.2,.8]),
 ('Euler ideal force kN',[math.pi**2*20000/6**2,math.pi**2*20000/9**2],[5483,2437]),
 ('moment kN m and edge MPa',[500*.1,500/.3/1000+6*50/.3**2/1000,500/.3/1000-6*50/.3**2/1000],[50,5,-1.667]),
 ('spring displacement mm and force kN',[1000/(20+30),1000*20/(20+30),1000*30/(20+30),1000/30],[20,400,600,33.33]),
 ('ideal resistance and shortfall kN',[4*200,3*200,700-3*200],[800,600,100]),
 ('sum correlated and independent std mm',[math.sqrt(2**2+3**2+2*.5*2*3),math.hypot(2,3)],[4.36,3.61]),
 ('validation RMSE mm',[math.sqrt((1**2+0**2+2**2)/3)],[1.29]),
 ('water pressure kPa and local force kN',[9.81*18,9.81*18*1.5],[176.58,264.87]),
 ('register percent and unresolved',[76/80*100,80-76],[95,4])]
}
ledger=[]
for cid,checks in rows.items():
 d=json.loads((H/'inputs'/f'{cid}.json').read_text())
 assert len(checks)==len(d['units'])==10
 for n,(label,actual,rounded) in enumerate(checks,1):
  for a,b in zip(actual,rounded):
   decimals=len(str(b).split('.')[1]) if '.' in str(b) else 0
   assert round(a,decimals)==b,(cid,n,a,b)
  ledger.append(dict(course=cid,unit=n,label=label,computed=actual,publishedRounded=rounded,model=d['units'][n-1]['model']))
result=dict(passed=True,courseCount=5,unitCount=50,limitations='Arithmetic and stated teaching boundaries only; independent author review remains separate. No capacity, permit, operating limit or safety approval is established.',calculations=ledger)
(H/'calculation_146_150.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print('PASS 50 independent arithmetic evaluations; ledger calculation_146_150.json')
