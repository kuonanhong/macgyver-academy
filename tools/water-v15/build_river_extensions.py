#!/usr/bin/env python3
"""Five original river restoration/coordination lessons, separate from frozen dam authors."""
import json,math,re,runpy,hashlib
from pathlib import Path
H=Path(__file__).resolve().parent;T={x['id']:x for x in json.loads((H/'targets.json').read_text())};C={};S={};R={}
def pair(z,e):return z+'~'+e
SENS={
'b276':dict(expression='1000*9.81*.88*.003',expected=25.8984,unit='Pa',text='固定 rho=1000 kg/m3、g=9.81 m/s2 與 S=0.003 無因次，只將 R 從 0.8 m 增至 0.88 m，tau=25.8984 Pa，相較 23.544 Pa 增加一成。這仍是河段平均，不能當外彎局部最大值。~Keep rho=1000 kg/m3, g=9.81 m/s2 and dimensionless S=0.003 fixed, changing only R from 0.8 m to 0.88 m. The stress becomes 25.8984 Pa, ten percent above 23.544 Pa. It remains a reach average rather than the outer-bank local maximum.'),
'b277':dict(expression='.66/(.012-.004)',expected=82.5,unit='m',text='固定兩個無因次坡度 S0=0.012 與 Se=0.004，將單一落差 dz 從 0.6 m 增至 0.66 m，L=82.5 m，相較 75 m 增加一成。此為幾何敏感度，沒有驗證較大落差的消能、通行或結構需求。~Hold dimensionless slopes S0=0.012 and Se=0.004 fixed and raise drop dz from 0.6 m to 0.66 m. Spacing becomes 82.5 m, ten percent above 75 m. This is geometric sensitivity and does not validate energy dissipation, passage or structural requirements at the larger drop.'),
'b278':dict(expression='math.sqrt(2*9.81*.18)',expected=1.8792551716,unit='m/s',text='固定 g=9.81 m/s2 與理想無損失假設，將 dh 從 0.15 m 增至 0.18 m，速度由 1.715517 m/s 增至 1.879255 m/s，約增加百分之九點五四。落差增加兩成而速度非增加兩成，且仍未判定魚種可通過性。~Keep g=9.81 m/s2 and the ideal loss-free assumption fixed while increasing dh from 0.15 m to 0.18 m. Velocity rises from 1.715517 m/s to 1.879255 m/s, approximately 9.54 percent. A twenty percent drop increase does not produce a twenty percent speed increase and still does not determine species passage suitability.'),
'b279':dict(expression='1980/1200',expected=1.65,unit='dimensionless',text='固定谷地參考長 Lv=1200 m，將中心線 Lc 從 1800 m 增至 1980 m，蜿蜒度由 1.5 增至 1.65。河長與指標同增一成，但這個比值不能單獨證明棲地、洪峰或泥砂平衡改善。~Keep valley reference length Lv=1200 m fixed and increase centreline Lc from 1800 m to 1980 m. Sinuosity rises from 1.5 to 1.65. Length and index both increase ten percent, but the ratio alone does not establish improvement in habitat, flood peaks or sediment balance.'),
'b280':dict(expression='10/20',expected=.5,unit='dimensionless',text='保持 N=20 個等權成員及同一流量門檻，把超越成員 Ne 從 8 增至 10，經驗比例由 0.4 增至 0.5，也就是增加十個百分點。這不是證明真實風險上升同樣幅度，仍須用獨立事件檢驗機率校準。~Keep N=20 equally weighted members and the same flow threshold, increasing exceedances Ne from 8 to 10. The empirical fraction rises from 0.4 to 0.5, an increase of ten percentage points. This does not prove an equal change in true risk; probability calibration still requires independent events.')}
def split(v):return v.split('~',1)
def source(key,title,publisher,url,scope,ref,claims):
 z,e=split(title);a,b=split(scope);S[key]=dict(key=key,title=z,titleEn=e,publisher=publisher,url=url,sourceType='primary',scope=a,scopeEn=b);R[key]=dict(url=url,retrievalRef=ref,verifiedClaims=claims,scope=b,accessed='2026-10-21')
def project(cid,focus,summary,history,facts,timeline,codes,landmarks,place,keys):
 C[cid]=dict(focus=focus,summary=summary,history=history,facts=facts,timeline=timeline,codes=codes,landmarks=landmarks,place=place,keys=keys,units=[])
def units(cid,text):
 for line in text.strip().splitlines():
  if not line.strip():continue
  a=[s.strip() for s in line.split('||')];assert len(a)==12,(cid,len(a),a[0]);title,cause,formula,boundary,verify,failure,misconception,practice,expr,value,resultunit,tol=a
  bz,be=split(boundary)
  model=pair('原創假想教材輸入，不是現地設計值或操作指令：'+formula+'。適用邊界：'+bz+'。','Original hypothetical teaching inputs, not field design values or operating instructions: '+formula+'. Applicable boundary: '+be+'.')
  u=dict(anchor=title,title=title,mechanism=cause,model=model,verify=verify,failure=failure,misconception=misconception,practice=practice)
  C[cid]['units'].append((u,dict(expression=expr,expected=float(value),resultUnit=resultunit,tolerance=float(tol),formula=formula,boundary=boundary)))
def build(cid,c):
 t=T[cid];ids=[f'b{x}' for x in range(276,281)];i=ids.index(cid);us=[u for u,a in c['units']];assert len(us)==10
 facts=c['facts'][:]
 for u,a in c['units']:
  z,e=split(u['title']);f=pair('教學假設：'+z+'；'+a['formula'],'Teaching assumption: '+e+'; '+a['formula'])
  if len(re.findall('[A-Za-z]{2,}',split(f)[1]))<=45 and len(re.findall('[㐀-鿿]',split(f)[0]))<=90:facts.append(f)
  if len(facts)==6:break
 assert len(facts)==6
 example=pair('本課先用「'+split(us[0]['title'])[0]+'」建立原創假想基準，再以「'+split(us[1]['title'])[0]+'」檢查另一個控制機制。第一組輸入及結果為 '+c['units'][0][1]['formula']+'；第二組為 '+c['units'][1][1]['formula']+'。學員需在同一張工作表分列量綱、時間、位置與適用範圍，先核對守恆，再解釋為何兩個得數不能互相代替。最後以第三單元提出的量測設計驗證假設，並將超出模型能力的水理、生態或治理問題列為待研究項目；這些示例並非所列案例的現場實測。','Begin with an original hypothetical baseline for '+split(us[0]['title'])[1]+' and examine another controlling mechanism through '+split(us[1]['title'])[1]+'. The first inputs and result are '+c['units'][0][1]['formula']+'; the second are '+c['units'][1][1]['formula']+'. Keep dimensions, time, location and validity conditions in separate columns of the same working sheet. Check conservation before explaining why the two numerical results cannot substitute for one another. Use the third unit measurement design to test assumptions and identify hydraulic, ecological or governance questions that exceed the model. These examples are not field observations from the named reference cases.')
 ez,ee=split(example);sz,se=split(SENS[cid]['text']);example=pair(ez+'敏感度重算：'+sz,ee+' Sensitivity recalculation: '+se)
 sources=[S[k] for k in c['keys']];chosen=[]
 for s in sources:
  if s['publisher'] not in [x['publisher'] for x in chosen]:chosen.append(s)
  if len(chosen)==2:break
 assert len(chosen)==2
 vendors=[dict(name=s['publisher'],nameEn=s['publisher'],business='提供本課引用的公開方法文獻或案例研究。',businessEn='Publishes the methodological reference or case evidence cited in this lesson.',url=s['url'],investorUrl='',security=None,role='資料及研究關聯機構，不據此宣稱為本例施工承包商。',roleEn='Associated as a source or research institution, not asserted to be a construction contractor for the examples.') for s in chosen]
 timeline=sorted(c['timeline']+[dict(year='2026',event=pair('教材來源核對與原創數值重算，屬編修事件而非工程完工','Source verification and original numerical recalculation, a curriculum event rather than project completion'))],key=lambda x:x['year'])
 return dict(id=cid,title=t['title']+'~'+t['titleEn'],discipline=t['discipline'],family='water',focus=c['focus'],summary=c['summary'],history=c['history'],example=example,units=us,facts=facts,timeline=timeline,codes=c['codes'],landmarks=c['landmarks'],place=c['place'],sources=sources,vendors=vendors,related=[ids[(i+1)%5],ids[(i+2)%5]],architectureNodes=[split(us[j]['title']) for j in [0,2,4,6,9]],architectureEdges=[[0,1],[1,2],[2,3],[3,4],[4,1]])
def main():
 runpy.run_path(str(H/'river_extensions_metadata.py'),init_globals=globals())
 for p in sorted(H.glob('river_extensions_units_*.py')):runpy.run_path(str(p),init_globals=globals())
 rows=[];built=[]
 for cid,c in C.items():
  if len(c['units'])!=10:continue
  d=build(cid,c);p=H/'inputs'/f'{cid}.json';p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');built.append(cid)
  for j,(u,a) in enumerate(c['units'],1):
   v=eval(a['expression'],{'__builtins__':{},'math':math,'abs':abs,'min':min,'max':max});assert abs(v-a['expected'])<=a['tolerance'],(cid,j,v,a['expected'])
   rows.append(dict(courseId=cid,unit=j,title=u['title'],**a,recomputed=v,passCheck=True,modelSha=hashlib.sha256(u['model'].encode()).hexdigest(),quizSha=hashlib.sha256(u['misconception'].encode()).hexdigest(),inputSha=hashlib.sha256(p.read_bytes()).hexdigest()))
 (H/'research_river_extensions.json').write_text(json.dumps(dict(accessed='2026-10-21',sources=R,courses={cid:C[cid]['keys'] for cid in built},scope='Primary references reviewed at stated page/excerpt scope; calculations independently authored hypothetical scenarios, not borrowed project inputs or legal design approvals.'),ensure_ascii=False,indent=2)+'\n')
 (H/'calculation_river_extensions.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n');print('Built',len(built),'river lessons;',len(rows),'literal results recomputed')
if __name__=='__main__':main()
