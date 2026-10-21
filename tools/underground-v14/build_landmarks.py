#!/usr/bin/env python3
import json,sys
from pathlib import Path
from landmarks_core import C,parts,pair
from landmarks_models import calculate,TRACE
from landmarks_dossiers import P,B
H=Path(__file__).resolve().parent
T={x['id']:x for x in json.loads((H/'targets.json').read_text())}
COMMON=[dict(key='landmark-fhwa',title='FHWA 隧道土建技術手冊',titleEn='FHWA Technical Manual for Road Tunnel Civil Elements',publisher='Federal Highway Administration',url='https://rosap.ntl.bts.gov/view/dot/50019',sourceType='primary',scope='隧道土建、地工與施工的通用原理；不證明個別工程的假想算例。',scopeEn='General civil, geotechnical and construction principles, not evidence for hypothetical project calculations.'),dict(key='landmark-piarc',title='PIARC 道路隧道手冊',titleEn='PIARC Road Tunnels Manual',publisher='World Road Association PIARC',url='https://tunnelsmanual.piarc.org/en',sourceType='primary',scope='道路隧道營運、維護及系統原理；鐵路及儲存課僅作跨領域比較，不是其適用規範。',scopeEn='Road-tunnel operations, maintenance and systems; rail and storage courses use this for cross-domain comparison, not as their governing standard.')]
def make(ids=None):
 research=[];done=[];TRACE.clear()
 for ci,(cid,p) in enumerate(P.items()):
  if ids and cid not in ids:continue
  if cid not in B:continue
  t=T[cid];title=pair(t['title'],t['titleEn']);units=[]
  for ui,(k,scenario,evidence,diagnosis) in enumerate(B[cid]):
   c=C[k];sz,se=parts(scenario);mz,me=parts(c['mechanism']);vz,ve=parts(c['verify']);ez,ee=parts(evidence);fz,fe=parts(c['failure']);dz,de=parts(diagnosis);pz,pe=parts(c['practice']);az,ae=parts(c['anchor'])
   units.append(dict(anchor=c['anchor'],title=c['title'],mechanism=pair(sz+mz,se+' '+me),model=calculate(c['model'],ci,ui,cid),verify=pair(ez+vz+'比對時保留校正、時間與基準版本，允收採設計核准條件。',ee+' '+ve+' Retain calibration, timing and datum revisions, and compare against design-approved conditions.'),failure=pair(dz+fz,de+' '+fe),misconception=c['misconception'],practice=pair('本案「'+az+'」的交付需回答：'+ez+pz,'For '+t['titleEn']+', the '+ae.lower()+' handover must address the following evidence: '+ee+' '+pe)))
  bz,be=parts(p['summary']);fz,fe=parts(p['focus']);ez,ee=parts(p['event']);pubz,pube=parts(p['publisher']);year=str(p['year'])
  # Two explicit worked calculations plus sensitivity, not purported design data.
  m1z,m1e=parts(units[1]['model']);m2z,m2e=parts(units[5]['model'])
  example=pair('原創綜合審查：先計算「'+parts(units[1]['title'])[0]+'」，再獨立計算「'+parts(units[5]['title'])[0]+'」。'+m1z+m2z+'兩組結果的單位與邊界不同，不能直接相加。請列出一項缺少的現場輸入，說明它會影響哪個結論，以及哪種獨立量測可以縮小不確定度。','Original integrated review: first calculate '+parts(units[1]['title'])[1].lower()+', then independently calculate '+parts(units[5]['title'])[1].lower()+'. '+m1e+' '+m2e+' The outputs have different units and boundaries and cannot simply be added. Identify one missing field input, explain which conclusion it changes and select an independent measurement to reduce uncertainty.')
  source=dict(key='landmark-'+cid,title=pubz+'：'+t['title']+'公開資料',titleEn=pube+': '+t['titleEn']+' public information',publisher=pube,url=p['url'],sourceType='primary',scope='支持工程公開背景、尺度及所述事件；教材量測配置與計算值是明示假設，不表示原工程實際採用。',scopeEn='Supports public context, scale and the stated event; teaching measurement configurations and calculations are explicit assumptions, not claims of actual installation.')
  source['scope']=p.get('sourceScope',source['scope'])
  source['scopeEn']=p.get('sourceScopeEn',source['scopeEn'])
  sources=[source,*COMMON,*p.get('extra',[])]
  history=pair(year+' 年公開記錄：'+ez+'。'+bz+'本課把「'+fz+'」視為互相連動的系統，工程年代和名稱由所列公開來源核對；模型中的設備配置、荷載與量測數字另外標明為教學假設，只重建公開原理及工程推理，不是原始設計文件。','Public record for '+year+': '+ee+'. '+be+' The course treats '+fe.lower()+' as coupled engineering questions. Named events and dimensions follow the listed public sources; equipment scenarios, loads and measurement values are separately marked teaching assumptions. Only public principles and reasoning are reconstructed, not original design documents.')
  facts=[pair('公開工程尺度約為 '+p['scale']+'，保留所列來源的計量邊界。','The public scale is about '+p['scale']+'; retain the measurement boundary in the cited source.'),pair(year+' 年事件：'+ez+'。',year+' event: '+ee+'.')]
  courseTrace=[r for r in TRACE if r['courseId']==cid]
  for ix in (0,1,4,5):
   r=courseTrace[ix];q=r['inputs'][0];az,ae=parts(units[ix]['anchor']);un=q['unit'];zu={'dimensionless':'無因次','count':'個'}.get(un,un)
   facts.append(pair(f'教學「{az}」：{q["labelZh"]}={q["value"]:g} {zu}，其餘輸入依單元，結果={r["result"]:.6g} {r["unitLabel"]}；不是實測或允收值。',f'Teaching {ae.lower()}: {q["label"]}={q["value"]:g} {un}, with remaining inputs as in the unit, gives {r["result"]:.6g} {r["unitLabel"]}; not measured or accepted project data.'))

  timelines=[dict(year=year,event=p['event']),dict(year='2009',event=pair('方法文獻：FHWA出版隧道土建手冊，這不是本工程施工里程碑。','Method reference: FHWA publishes its civil tunnel manual; this is not a project construction milestone.')),dict(year='2026',event=pair('教材檢視：核對公開尺度並撰寫假想算例，這不是工程完工日期。','Educational review: public scales are checked and hypothetical exercises authored, not a project completion date.'))]
  timelines.sort(key=lambda x:int(x['year']))
  related=p.get('related',['b102','b103'])
  if cid in related:related=['hsuehshan' if cid!='hsuehshan' else 'b104','b106']
  vendors=[dict(name=pubz,nameEn=pube,business='提供本工程的公開計畫或營運資料，機構角色以來源頁為準。',businessEn='Provides public project or operational information; institutional role follows the cited page.',url=p['url'],investorUrl='',security=None,role='本課工程背景的直接來源，不宣稱與學院有合作或未核實供應合約。',roleEn='Direct project-context source; no academy partnership or unverified supply contract is claimed.'),dict(name='美國聯邦公路管理局',nameEn='Federal Highway Administration',business='發布隧道土建與地工技術參考資料，供模型邊界及驗證方法比較。',businessEn='Publishes civil and geotechnical references for comparing model boundaries and verification methods.',url=COMMON[0]['url'],investorUrl='',security=None,role='通用原理來源，並非本工程設計或施工參與者的宣稱。',roleEn='General-principles source, not a claim of participation in project design or construction.')]
  nodes=[parts(units[x]['anchor']) for x in [0,1,3,5,7,9]]
  d=dict(id=cid,title=title,discipline=t['discipline'],family=t['family'],focus=p['focus'],summary=p['summary'],units=units,example=example,history=history,facts=facts,timeline=timelines,codes=[pair('FHWA-NHI-10-034：道路隧道土建技術手冊，供公開原理比較。','FHWA-NHI-10-034: Technical Manual for Road Tunnel Civil Elements, for public principles.'),pair('PIARC 道路隧道手冊：系統、營運與維護，須核對跨領域適用性。','PIARC Road Tunnels Manual: systems, operations and maintenance; verify cross-domain applicability.')],landmarks=[pair(T[r]['title'],T[r]['titleEn']) for r in related],place=dict(name=pair(t['title']+'參照點',t['titleEn']+' reference'),country=p['country'],lat=p['lat'],lng=p['lng'],query=t['titleEn']),sources=sources,vendors=vendors,related=related,architectureNodes=nodes,architectureEdges=[[0,1],[1,2],[2,3],[3,4],[4,5],[1,5]])
  (H/'inputs'/f'{cid}.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');done.append(cid)
  eventUrl=p['url']
  if cid in ('b108','b109','b113','b114','b116','b119','b124','b125'):eventUrl=p['extra'][0]['url']
  verifiedClaims=[dict(claim='Published scale: '+p['scale'],sourceUrl=p['url'],scope='Retains stated route/section/storage boundary; not a model input.'),dict(claim=year+' event: '+ee,sourceUrl=eventUrl,scope='Project event type retained; breakthrough, partial use, construction and opening are distinct.')]
  research.append(dict(verifiedClaims=verifiedClaims,courseId=cid,reviewed='2026-10-21',publicScale=p['scale'],publicEvent=year+' '+ee,sourceUrls=[x['url'] for x in sources],claimsNote='Listed project sources support context, scale and event within their stated scopes; common method references do not verify hypothetical project values. Map point is approximate, not an entrance.',sourceAccess=p.get('sourceAccess','Project HTML or indexed primary extract read in browser search; common FHWA landing page and PIARC manual read'),conflictNote=p.get('conflictNote',''),scenarioProvenance='All 10 numerical examples and measurement scenarios are authored hypotheses.'))
 (H/'research_landmarks.json').write_text(json.dumps(research,ensure_ascii=False,indent=2)+'\n')
 (H/'calculation_landmarks.json').write_text(json.dumps(TRACE,ensure_ascii=False,indent=2)+'\n')
 print('Wrote',len(done),'courses',len(TRACE),'numerical units:',','.join(done))
if __name__=='__main__':make(sys.argv[1:] or None)
