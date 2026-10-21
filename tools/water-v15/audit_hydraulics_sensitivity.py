#!/usr/bin/env python3
"""Recalculate every hydraulics-author extended-example sensitivity."""
from pathlib import Path
import math,json
P=Path(__file__).resolve().parent
checks=[
('b210','Incremental evaporation storage loss, km3','500e6*(2.1-1.8)/1e9',0.15),
('b211','Seepage ratio at600m versus400m, fixedk/A/head','400/600',2/3),
('b212','Mean pressure on45m2, kPa','900/45',20),
('b213','Power at250m3/s, MW','1000*9.81*250*60*0.9/1e6',132.435),
('b214','Friction-resistance reduction, percent','((90000-20000)*0.7-(90000-30000)*0.7)/((90000-20000)*0.7)*100',14.285714285714286),
('b241','Darcy flow at15m head, m3/s','0.00002*500*15/50',0.003),
('b242','Retention geometry ratio atD15=0.90mm','0.90/0.20',4.5),
('b243','Friction resistance at90kPa pore pressure, kPa','(150-90)*math.tan(math.radians(30))',34.64101615137754),
('b244','Conjugate depth at15m/s, m','0.5*(math.sqrt(1+8*15**2/9.81)-1)',6.291285565563233),
('b245','Range at25m/s and30degrees, m','25**2*math.sin(math.radians(60))/9.81',55.17491104577211),
('b245','Range increase, percent','(25**2/20**2-1)*100',56.25),
('b246','Critical depth atq6, m','(36/9.81)**(1/3)',1.5424502472009343),
('b246','Critical-depth growth, percent','((6/4)**(2/3)-1)*100',31.037069710444822),
('b247','Side-channel discharge with3m2/s over40m, m3/s','3*40',120),
('b248','Free-weir head response ratio','1.5**1.5',1.8371173070873836),
('b248','Orifice head response ratio','math.sqrt(1.5)',1.224744871391589),
('b249','Cavitation index at30m/s','(100000-2300)/(0.5*1000*30**2)',0.21711111111111112),
('b249','Dynamic pressure increase, percent','(30**2/20**2-1)*100',125),
('b250','Horizontal load at7m depth, kN','0.5*9.81*8*7**2',1922.76),
('b250','Horizontal-force increase, percent','(7**2/6**2-1)*100',36.111111111111114),
('b251','Resistance at rolling coefficient0.03, kN','600*0.03',18),
('b252','Laminar slot discharge ratio','(0.30/0.20)**3',3.375),
('b253','Suspended flux at5kg/m3, kg/s','40*5',200),
('b254','Gravity-velocity ratio at doubled density excess','math.sqrt(2)',1.4142135623730951),
('b255','Solid production atCv0.15, m3/h','0.25*0.15*3600',135)]
rows=[]
for cid,quantity,expr,expected in checks:
 v=eval(expr,{'__builtins__':{}},{'math':math});rows.append(dict(course=cid,quantity=quantity,expression=expr,result=v,expected=expected,passed=math.isclose(v,expected,rel_tol=1e-9,abs_tol=1e-9)))
r=dict(courses=sorted(set(x['course'] for x in rows)),courseCount=len(set(x['course'] for x in rows)),numericChecks=len(rows),passed=sum(x['passed'] for x in rows),scope='One extended-example sensitivity per authored course; multiple checks where a paragraph states multiple comparative values. Original teaching scenarios, not design certification.',results=rows)
(P/'audit_hydraulics_sensitivity.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
print(r['courseCount'],'courses',r['passed'],'/',len(rows),'sensitivity checks')
assert r['passed']==len(rows)
