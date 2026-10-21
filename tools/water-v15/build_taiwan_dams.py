#!/usr/bin/env python3
"""Six independently authored water-engineering cases; all calculations are hypothetical."""
import json,math,re,runpy,hashlib
from pathlib import Path
H=Path(__file__).resolve().parent
T={x['id']:x for x in json.loads((H/'targets.json').read_text())}
C={};S={};R={}
def pair(z,e):return z+'~'+e
def split(x):return x.split('~',1)
def source(key,title,publisher,url,scope,evidence,ref,claims):
 z,e=split(title);sz,se=split(scope)
 S[key]=dict(key=key,title=z,titleEn=e,publisher=publisher,url=url,sourceType='primary',scope=sz,scopeEn=se)
 R[key]=dict(url=url,accessed='2026-10-21',retrievalRef=ref,accessEvidence=evidence,verifiedClaims=claims)
def project(cid,focus,summary,history,eventyear,event,dimension,place,keys,example):
 C[cid]=dict(focus=focus,summary=summary,history=history,eventyear=eventyear,event=event,dimension=dimension,place=place,keys=keys,example=example,units=[])
def units(cid,text):
 for line in text.strip().splitlines():
  if not line.strip():continue
  a=[x.strip() for x in line.split('||')];assert len(a)==12,(cid,len(a),a[0])
  title,cause,formula,boundary,verify,failure,misconception,practice,expr,value,resultunit,tol=a
  z,e=split(cause);fz,fe=split(failure);bz,be=split(boundary)
  model=pair('原創教學假設，以下數值不是本工程實測或設備設定：'+formula+'。適用邊界：'+bz+'。','Original teaching assumptions, not project measurements or equipment settings: '+formula+'. Applicable boundary: '+be+'.')
  unit=dict(anchor=title,title=title,mechanism=cause,model=model,verify=verify,failure=failure,misconception=misconception,practice=practice)
  C[cid]['units'].append((unit,dict(expression=expr,expected=float(value),resultUnit=resultunit,tolerance=float(tol),formula=formula,boundary=boundary)))
def build(cid,c):
 t=T[cid];ids=[f'b{x}' for x in range(215,221)];ix=ids.index(cid)
 units=[u for u,a in c['units']];assert len(units)==10,(cid,len(units))
 year=c['eventyear'];event=c['event'];keys=c['keys'];sources=[S[k] for k in keys]
 facts=[c['dimension'],pair(str(year)+' 年公開紀錄：'+split(event)[0],str(year)+' documented event: '+split(event)[1])]
 for u,a in c['units']:
  z,e=split(u['title']);f=pair('教學假設：'+z+'；'+a['formula'],'Teaching assumption, '+e+': '+a['formula'])
  if len(re.findall('[A-Za-z]{2,}',split(f)[1]))<=45 and len(re.findall('[㐀-鿿]',split(f)[0]))<=90:facts.append(f)
  if len(facts)==6:break
 assert len(facts)==6,cid
 isarch=cid in ['b215','b216','b218'];guideyear=1994 if isarch else 2014
 guideevent=pair('美國工兵團發布拱壩設計手冊，屬方法文獻年代而非本壩施工日期','USACE issues its arch-dam design manual; this dates a method reference rather than construction of this dam') if isarch else pair('美國墾務局設計標準索引列出滲流章一月版本，屬方法資料年代','The Reclamation standards index lists the January seepage chapter; this dates a methodological reference')
 timeline=[dict(year=str(year),event=event),dict(year=str(guideyear),event=guideevent),dict(year='2026',event=pair('本教材核對公開資料並獨立重算假想示例，不是新增工程完工紀錄','The curriculum checks public evidence and independently recalculates hypothetical examples; this is not a new project completion'))]
 timeline.sort(key=lambda x:x['year'])
 codes=[pair('美國工兵團拱壩設計手冊，歷史方法參考','USACE Arch Dam Design, historical methodological reference') if isarch else pair('美國墾務局設計標準十三：土石壩','Reclamation Design Standards No. 13: Embankment Dams'),pair('美國墾務局設計標準十四：水壩附屬構造物','Reclamation Design Standards No. 14: Appurtenant Structures for Dams')]
 ez,ee=split(c['example']);vz,ve=split(units[0]['verify']); example=pair(ez+' 核驗：'+c['units'][0][1]['formula']+'。'+vz,ee+' Verification: '+ve)
 source1=sources[0];source2=S['usace-arch'] if isarch else S['usbr-design']
 vendors=[]
 for s in [source1,source2]:
  vendors.append(dict(name=s['publisher'],nameEn=s['publisher'],business='提供本課相關工程背景或公開設計文獻的機構。',businessEn='Institution providing relevant project context or public engineering references.',url=s['url'],investorUrl='',security=None,role='本課引用其公開資料作比較研究，不表示參與本教材或承攬所有列舉工項。',roleEn='Public material is used for comparative study; this implies neither participation in the curriculum nor a contract for every listed work.'))
 z,e=split(t['title']+'~'+t['titleEn']);country,lat,lng,query=c['place']
 return dict(id=cid,title=z+'~'+e,discipline=t['discipline'],family='water',focus=c['focus'],summary=c['summary'],history=c['history'],example=example,units=units,facts=facts,timeline=timeline,codes=codes,landmarks=[z+'~'+e,T[ids[(ix+1)%6]]['title']+'~'+T[ids[(ix+1)%6]]['titleEn']],place=dict(name=z+'公開背景參照點~'+e+' public context reference',country=country,lat=lat,lng=lng,query=query),sources=sources,vendors=vendors,related=[ids[(ix+1)%6],ids[(ix+2)%6]],architectureNodes=[split(units[i]['title']) for i in [0,2,4,6,9]],architectureEdges=[[0,1],[1,2],[2,3],[3,4],[4,1]])
def main():
 runpy.run_path(str(H/'taiwan_dams_metadata.py'),init_globals=globals())
 for p in sorted(H.glob('taiwan_dams_units_*.py')):runpy.run_path(str(p),init_globals=globals())
 runpy.run_path(str(H/'taiwan_dams_revisions.py'),init_globals=globals())
 audit=[]
 for cid,c in sorted(C.items()):
  if len(c['units'])!=10:continue
  d=build(cid,c);(H/'inputs'/f'{cid}.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
  for i,(u,a) in enumerate(c['units'],1):audit.append(dict(courseId=cid,unit=i,title=u['title'],**a))
 (H/'research_taiwan_dams.json').write_text(json.dumps(dict(accessed='2026-10-21',sources=R,courses={cid:c['keys'] for cid,c in C.items()},scope='Owner facts are separately cited. All worked inputs and models are original hypothetical teaching scenarios; public source parameters are not operating instructions. Common guides were checked at the stated index or excerpt scope, not represented as fully reviewed project criteria.'),ensure_ascii=False,indent=2)+'\n')
 (H/'calculation_taiwan_dams.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n')
 print('Built',len(audit)//10,'courses;',len(audit),'numeric models')
if __name__=='__main__':main()
