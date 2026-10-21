#!/usr/bin/env python3
"""V15 world dam case authoring. Numerical scenarios are independently authored examples."""
import json,math,re,runpy,hashlib
from pathlib import Path
H=Path(__file__).resolve().parent
T={x['id']:x for x in json.loads((H/'targets.json').read_text())}
C={};S={};R={};EXT=runpy.run_path(str(H/'landmarks_extensions.py'))['EXT']
def pair(z,e):return z+'~'+e
def split(s):return s.split('~',1)
def source(key,title,publisher,url,scope,ref,claims):
 z,e=split(title);a,b=split(scope);S[key]=dict(key=key,title=z,titleEn=e,publisher=publisher,url=url,sourceType='primary',scope=a,scopeEn=b)
 R[key]=dict(url=url,retrievalRef=ref,verifiedClaims=claims,accessed='2026-10-21',scope=b)
def project(cid,focus,summary,history,fact,year,event,country,lat,lng,keys):
 C[cid]=dict(focus=focus,summary=summary,history=history,fact=fact,year=year,event=event,country=country,lat=lat,lng=lng,keys=keys,units=[])
def units(cid,text):
 for line in text.strip().splitlines():
  if not line.strip():continue
  r=[s.strip() for s in line.split('||')];assert len(r)==12,(cid,len(r),r[0]);title,cause,formula,boundary,verify,failure,misconception,practice,expr,value,resultunit,tol=r
  z,e=split(cause);fz,fe=split(EXT[cid][len(C[cid]['units'])]);bz,be=split(boundary)
  model=pair('原創假想算例，輸入均非本工程操作參數：'+formula+'。模型邊界：'+bz+'。','Original hypothetical example; inputs are not operating parameters of this project: '+formula+'. Model boundary: '+be+'.')
  u=dict(anchor=title,title=title,mechanism=pair(z+' '+fz,e+' '+fe),model=model,verify=verify,failure=failure,misconception=misconception,practice=practice)
  C[cid]['units'].append((u,dict(expression=expr,expected=float(value),resultUnit=resultunit,tolerance=float(tol),formula=formula,boundary=boundary)))
def build(cid,c):
 t=T[cid];ids=['three-gorges']+[f'b{x}' for x in range(202,215)];ix=ids.index(cid);us=[u for u,a in c['units']];assert len(us)==10
 facts=[c['fact'],pair(str(c['year'])+' 年官方紀錄：'+split(c['event'])[0],str(c['year'])+' official record: '+split(c['event'])[1])]
 for u,a in c['units']:
  z,e=split(u['title']);f=pair('假想教材：'+z+'；'+a['formula'],'Hypothetical teaching: '+e+'; '+a['formula'])
  if len(re.findall('[A-Za-z]{2,}',split(f)[1]))<=45 and len(re.findall('[㐀-鿿]',split(f)[0]))<=90:facts.append(f)
  if len(facts)==6:break
 assert len(facts)==6,(cid,facts)
 example=pair('以下為本課原創情境串接，所有數值是假設，不能視為業主設計圖或操作許可。先完成「'+split(us[0]['title'])[0]+'」的守恆與邊界檢核，再比較「'+split(us[1]['title'])[0]+'」及「'+split(us[2]['title'])[0]+'」的不同控制量。第一組計算為 '+c['units'][0][1]['formula']+'；第二組為 '+c['units'][1][1]['formula']+'。學員須保留量綱、資料時間與量測位置，討論誤差如何傳到結果，將第三單元的限制寫入同一張決策表。任何未納入的結構、河道或機組耦合都列為下一階段工作，不由單一得數推論全工程安全。','This original sequence connects the first three units using assumed inputs; none is an owner drawing or an operating authorization. First establish conservation and boundaries for '+split(us[0]['title'])[1]+', then compare the controlling variables in '+split(us[1]['title'])[1]+' and '+split(us[2]['title'])[1]+'. The first calculation is '+c['units'][0][1]['formula']+'; the second is '+c['units'][1][1]['formula']+'. Preserve dimensions, observation times, and measurement locations in the working sheet. Explain how input uncertainty changes each conclusion and include the third unit limitations in the same decision table. Structural, river, and machine interactions omitted by a model remain subsequent work; a single numerical answer cannot demonstrate safety of the complete project.')
 sources=[S[k] for k in c['keys']];vs=[]
 for s in [sources[0],S['usace-catalog'] if sources[0]['publisher']=='Bureau of Reclamation' else S['usbr-manuals']]:
  vs.append(dict(name=s['publisher'],nameEn=s['publisher'],business='提供本案例公開工程背景或大壩方法文獻的機構。',businessEn='Institution providing public project background or dam engineering reference literature.',url=s['url'],investorUrl='',security=None,role='依所列來源說明其資料關聯；未據此宣稱是全部工項承包商。',roleEn='Associated through the cited public source; this does not identify a contractor for every work item.'))
 timeline=[dict(year=str(c['year']),event=c['event']),dict(year='1987',event=pair('墾務局監測手冊出版，這是參考文獻年代而非本壩施工年份','Reclamation instrumentation manuals are published; this dates references rather than construction of this dam')),dict(year='2026',event=pair('本課核對公開來源並重算原創假想模型，屬教材修訂日期','This course verifies public references and recomputes original hypothetical models, a curriculum revision date'))];timeline.sort(key=lambda x:x['year'])
 return dict(id=cid,title=t['title']+'~'+t['titleEn'],discipline=t['discipline'],family='water',focus=c['focus'],summary=c['summary'],history=c['history'],example=example,units=us,facts=facts,timeline=timeline,codes=[pair('美國墾務局大壩監測手冊，混凝土或土石壩依型式選讀','Reclamation Dam Instrumentation Manuals, select concrete or embankment according to dam type'),pair('美國墾務局小壩設計手冊，僅作方法比較而非大型工程核准準則','Reclamation Design of Small Dams, comparative methods rather than approval criteria for this major project')],landmarks=[t['title']+'~'+t['titleEn'],T[ids[(ix+1)%len(ids)]]['title']+'~'+T[ids[(ix+1)%len(ids)]]['titleEn']],place=dict(name=t['title']+'案例參照點~'+t['titleEn']+' case reference',country=c['country'],lat=c['lat'],lng=c['lng'],query=t['titleEn']),sources=sources,vendors=vs,related=[ids[(ix+1)%len(ids)],ids[(ix+2)%len(ids)]],architectureNodes=[split(us[i]['title']) for i in [0,2,4,6,9]],architectureEdges=[[0,1],[1,2],[2,3],[3,4],[4,1]])
def main():
 runpy.run_path(str(H/'landmarks_metadata.py'),init_globals=globals())
 for p in sorted(H.glob('landmarks_units_*.py')):runpy.run_path(str(p),init_globals=globals())
 audit=[];built=[]
 for cid,c in C.items():
  if len(c['units'])!=10:continue
  d=build(cid,c);(H/'inputs'/f'{cid}.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');built.append(cid)
  for i,(u,a) in enumerate(c['units'],1):
   v=eval(a['expression'],{'__builtins__':{},'math':math,'abs':abs});assert abs(v-a['expected'])<=a['tolerance'],(cid,i,v,a['expected'])
   audit.append(dict(courseId=cid,unit=i,title=u['title'],**a,recomputed=v,passCheck=True))
 (H/'research_landmarks.json').write_text(json.dumps(dict(accessed='2026-10-21',sources=R,courses={cid:C[cid]['keys'] for cid in built},scope='Project facts are distinguished from original assumed engineering scenarios. Manual indexes/abstracts verify bibliographic scope, not full PDF review or project-specific design compliance.'),ensure_ascii=False,indent=2)+'\n')
 (H/'calculation_landmarks.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n');print('Built',len(built),'courses;',len(audit),'independently recomputed literal results')
if __name__=='__main__':main()
