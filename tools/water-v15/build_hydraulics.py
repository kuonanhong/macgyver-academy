#!/usr/bin/env python3
"""Rebuild only authored water-hydraulics inputs b241-b260."""
from pathlib import Path
import json,runpy,math,hashlib
P=Path(__file__).resolve().parent
C={};S={};GROUPS={};MARKS={};PROJECTS={}
def add(cid,focus,boundary,sensitivity,rows):
 units=[r.split('§') for r in rows.strip().splitlines() if r.strip()]
 assert len(units)==10 and all(len(u)==8 for u in units),(cid,[(len(u),u[0]) for u in units])
 C[cid]=dict(focus=focus,boundary=boundary,sensitivity=sensitivity,rows=units)
def pair(s):
 assert s.count('~')==1,s
 return s.split('~')
def bi(z,e):return z+'~'+e
def source(k,z,e,pub,url,scope,scopeEn):
 S[k]=dict(key=k,title=z,titleEn=e,publisher=pub,url=url,sourceType='primary',scope=scope,scopeEn=scopeEn)
source('usbr-manuals','美國墾務局水工手冊與專論目錄','Reclamation hydraulic manuals and monographs','Bureau of Reclamation','https://www.usbr.gov/tsc/techreferences/hydraulics_lab/pubs/manuals_monographs.html','官方目錄核實 1978 消能工專論、1980 水力試驗技術、1987 小壩設計及1990氣蝕專論；目錄日期不是工程啟用年。','Official catalog verifies the 1978 dissipator monograph, 1980 laboratory techniques, 1987 small-dam manual and 1990 cavitation monograph; publication dates are not project commissioning dates.')
source('usbr-standards','美國墾務局設計標準官方入口','Reclamation design standards portal','Bureau of Reclamation','https://www.usbr.gov/tsc/techreferences/designstandards-datacollectionguides/designstandards.html','官方章節目錄包括反濾、滲流、監測、地震及溢洪道；適用性仍需地方規範及專案評估。','Official chapters include filters, seepage, monitoring, seismic design and spillways; applicability still requires local codes and project assessment.')
source('usbr-monitoring','土石壩儀器與監測設計標準','Embankment-dam instrumentation and monitoring standard','Bureau of Reclamation','https://www.usbr.gov/tsc/techreferences/designstandards-datacollectionguides/finalds-pdfs/DS13-11.pdf','已讀2014年章節與滲流、孔壓、變形及潛在失效模式監測架構；教學數值另行假設。','Read the 2014 chapter framework for seepage, pore pressure, deformation and potential-failure-mode monitoring; numerical lessons are separately assumed.')
source('usbr-filters','土石壩反濾層設計標準','Embankment-dam protective-filter standard','Bureau of Reclamation','https://www.usbr.gov/tsc/techreferences/designstandards-datacollectionguides/finalds-pdfs/DS13-5.pdf','2011年官方索引及搜尋摘錄核實反濾功能分類；大型PDF超擷取限制，未聲稱全文取回，算例非規範允收值。','The 2011 official index and indexed passages verify filter-function classes; the large PDF exceeded retrieval limits, so full-text access is not claimed. Examples are not acceptance criteria.')
source('usbr-slopes','土石壩靜力穩定分析標準','Embankment-dam static stability analysis','Bureau of Reclamation','https://www.usbr.gov/tsc/techreferences/designstandards-datacollectionguides/finalds-pdfs/DS13-4.pdf','2011年章節提供穩定與水位工況脈絡，並非本課合成邊坡的地層資料。','The 2011 chapter supplies stability and reservoir-stage context, not ground data for the synthetic slopes.')
source('usbr-embankment-history','美國墾務局土石壩百年技術回顧','Reclamation century of embankment-dam engineering','Bureau of Reclamation','https://www.usbr.gov/pn/snakeriver/dams/uppersnake/teton/100years.pdf','2002年原始機構回顧包括Fontenelle及Teton事件與工程發展；不把教學模型當事故重現。','The 2002 institutional account includes Fontenelle and Teton events and engineering development; teaching models do not reconstruct those incidents.')
source('fema-seepage','FEMA 滲流與內部沖蝕評估監測','FEMA seepage and internal-erosion evaluation and monitoring','Federal Emergency Management Agency','https://www.fema.gov/sites/default/files/2020-08/fema_p1032_eval_monitoring_seepage_internal_erosion.pdf','官方檢索核實滲流與內部沖蝕監測指引；課程用於證據與失效路徑比較，不自訂警戒門檻。','Official retrieval identifies seepage and internal-erosion monitoring guidance; used for evidence and failure-path comparisons, not invented trigger thresholds.')
source('usgs-slopes','USGS 邊坡監測科學計畫','USGS landslide monitoring science','U.S. Geological Survey','https://www.usgs.gov/programs/landslide-hazards/monitoring','官方說明持續觀測邊坡與觸發機制研究；研究站資料不是本課案例量測。','Official overview describes sustained landslide observation and trigger research; station data are not measurements for these teaching cases.')
source('usgs-guobu','USGS 郭卜水庫邊坡水文控制研究','USGS Guobu reservoir-slope hydrological-control study','U.S. Geological Survey','https://www.usgs.gov/publications/hydrological-control-shift-river-level-rainfall-reactivated-guobu-slope-besides-laxiwa','原始研究記錄拉西瓦郭卜邊坡由庫水位轉為降雨相關的變形；僅比較監測解釋，不借用論文參數作設計。','Original research documents changing level and rainfall associations at Guobu beside Laxiwa; used to compare monitoring interpretations, not as design parameters.')
source('usace-spillway','USACE 溢洪道水力設計手冊','USACE hydraulic design of spillways','U.S. Army Corps of Engineers','https://www.publications.usace.army.mil/USACE-Publications/Engineer-Manuals/u43544q/31363033/','官方索引核實EM1110-2-1603與1990年日期；直接頁面取回受限，不聲稱全文閱讀。','Official index verifies EM1110-2-1603 and its 1990 date; direct retrieval was restricted, and full-text review is not claimed.')
source('hoover-owner','胡佛壩業主工程與歷史入口','Hoover Dam owner engineering and history portal','Bureau of Reclamation','https://www.usbr.gov/lc/hooverdam/','業主公開工程、歷史及水務資料入口；本課以水工系統作比較，不主張每種工法在此使用。','Owner portal for engineering, history and water operations; a hydraulic-system comparison, not an assertion that every method is used there.')
source('glen-owner','格倫峽谷壩業主資料','Glen Canyon Dam owner information','Bureau of Reclamation','https://www.usbr.gov/uc/rm/crsp/gc/','業主資料確認壩、進水、壓力管與溢洪道的系統脈絡；不採公開庫容當本課合成模型的輸入。','Owner information confirms dam, intake, penstock and spillway context; public storage figures are not inputs to synthetic lesson models.')


def unit(r,c):
 title,mech,calc,verify,fail,mis,expression,expected=r
 zt,et=pair(title);zm,em=pair(mech);zv,ev=pair(verify);zf,ef=pair(fail);zb,eb=pair(c['boundary'])
 return dict(anchor=title,title=title,
 mechanism=bi(zm+' 驗證時應'+zv+'，並辨識以下失效情境：'+zf+'。這有助於確認模型的水流、受力或量測邊界是否仍成立。',em+' Test this interpretation with the following evidence: '+ev+'. In particular, distinguish this failure mechanism: '+ef+'. That distinction determines whether the model boundary or measurement assumption remains valid.'),
 model=bi('原創教學假設：'+calc+'。數值只檢查量綱與機制，不是實測資料、設計設定或允收門檻。','Original teaching assumptions: '+calc+'. These values check dimensions and mechanism, not measured data, design settings or acceptance thresholds.'),
 verify=bi(zv+'。應將原始量測與本單元模型的輸入條件對齊，並針對「'+zf+'」取得獨立證據；同時保留儀器校正、測點位置與時間，避免把不同工況的資料直接相減。',ev+'. Match raw observations to the input conditions of this unit and obtain independent evidence for this specific scenario: '+ef+'. Preserve calibration, location and timing so that unlike operating states are not directly subtracted.'),
 failure=bi(zf+'。診斷時應採取以下查核：'+zv+'，確認異常是否同時出現在相關量測；未釐清原因就調整門檻，會使真正的機制變化被資料處理掩蓋。',ef+'. Diagnose it by the following check: '+ev+'. Establish whether related measurements corroborate the anomaly; changing thresholds before identifying the cause can conceal a real change in the governing mechanism.'),
 misconception=mis,
 practice=bi('交接時以'+zv+'作為可追溯證據，保存對應材料、構形與工況版本。針對'+zf+'，由負責工程師設定需補驗的項目與停留點，不能把教學結果當作現場操作許可。','At handover, use the following traceable evidence: '+ev+'. Record material, geometry and operating-state versions. Address this scenario: '+ef+'. The responsible engineer defines additional checks and hold points; the teaching result is not field operating authorization.'))

def metadata(cid,c,T):
 n=int(cid[1:]);r=c['rows'];tz,te=pair(T[cid]['title']+'~'+T[cid]['titleEn']);fz,fe=pair(c['focus']);bz,be=pair(c['boundary']);sz,se=pair(c['sensitivity']);titles=[pair(u[0]) for u in r]
 keys=['usbr-manuals','usbr-standards','usace-spillway','hoover-owner','glen-owner']
 if n==241:keys=['usbr-manuals','usbr-monitoring','fema-seepage','usbr-embankment-history']
 if n==242:keys=['usbr-manuals','usbr-filters','fema-seepage','usbr-embankment-history']
 if n==243:keys=['usbr-manuals','usbr-slopes','usbr-monitoring','usgs-slopes','usgs-guobu']
 keys=GROUPS.get(n,keys)
 sources=[S[k] for k in keys]
 marks=['胡佛壩（水工系統比較）~Hoover Dam (hydraulic-system comparison)','格倫峽谷壩（水工界面比較）~Glen Canyon Dam (hydraulic-interface comparison)']
 if n in (241,242):marks=['方特內爾壩（滲流證據比較）~Fontenelle Dam (seepage-evidence comparison)','提頓壩（內部沖蝕事件比較）~Teton Dam (internal-erosion comparison)']
 if n==243:marks=['拉西瓦郭卜邊坡（水文反應比較）~Laxiwa Guobu slope (hydrological-response comparison)','巴里灣邊坡（監測方法比較）~Barry Arm slope (monitoring-method comparison)']
 marks=MARKS.get(n,marks)
 summary=bi('本課以'+fz+'為主線，先用'+titles[0][0]+'與'+titles[1][0]+'界定水力與構造條件，再將'+titles[4][0]+'、'+titles[6][0]+'連結到'+titles[9][0]+'。'+bz+' 每單元以原創算例、量測與失效辨識共同檢查推論。','This course develops '+fe[0].lower()+fe[1:]+' through '+titles[0][1]+' and '+titles[1][1]+', then connects '+titles[4][1]+' and '+titles[6][1]+' to '+titles[9][1]+'. '+be+' Each unit combines original calculation, measurement and failure diagnosis to test the inference.')
 history=bi('本課所研究的'+fz+'，反映水工設計由單一尺寸選取走向水流、材料、施工與長期監測共同驗證的發展。'+bz+' 美國墾務局官方目錄列有1978年消能工專論、1980年水力試驗技術及1987年小壩設計，這些是技術文件出版年份，不是本課假想工程的啟用日期。所列具名工程只供公開原理與邊界比較，不主張取得其設計圖、現場紀錄或專有參數。','The focus on '+fe[0].lower()+fe[1:]+' reflects development from isolated sizing toward joint verification of flow, materials, construction and long-term observations. '+be+' The Reclamation catalog lists the 1978 energy-dissipator monograph, 1980 hydraulic laboratory techniques and 1987 small-dam manual. These are publication dates, not commissioning dates for a hypothetical project. Named works support comparisons of public principles and boundaries; this course claims no access to proprietary drawings, field records or project parameters.')
 ex=bi('整合算例輸入全為教學假設，先檢查'+titles[0][0]+'：'+r[0][2]+'；再獨立檢查'+titles[1][0]+'：'+r[1][2]+'。'+sz+' 兩個結果須按各自量綱解釋，不能直接相加或當成完整設計。'+bz+' 將'+pair(r[7][3])[0]+'作為獨立驗證，明確列出尚缺的現地輸入及其對結論的影響。','Every input in this integrated example is a teaching assumption. First examine '+titles[0][1]+': '+r[0][2]+'. Independently examine '+titles[1][1]+': '+r[1][2]+'. '+se+' Interpret each result in its own dimensions rather than adding them or treating them as a complete design. '+be+' Use the following independent check: '+pair(r[7][3])[1]+'. Identify missing field inputs and state which conclusions depend on them.')
 vendors=[]
 for s in [sources[0],next((s for s in sources if s['publisher']!='Bureau of Reclamation'),sources[-1])]:
  vendors.append(dict(name=s['publisher']+('（材料製造商）' if s['publisher']=='Sika' else '（公開資料機構）'),nameEn=s['publisher'],business=('製造止水與密封材料並提供產品施工資料。' if s['publisher']=='Sika' else '提供水工技術文件、工程資料或監測研究。'),businessEn=('Manufactures waterstop and sealing materials and publishes installation information.' if s['publisher']=='Sika' else 'Publishes hydraulic guidance, project information or monitoring research.'),url=s['url'],investorUrl='',security=None,role='可從公開資料研究'+titles[2][0]+'與證據界線，不表示承攬本課假想工程。',roleEn='Study '+titles[2][1]+' and evidence boundaries through public information; no role in a hypothetical project is asserted.'))
 d=dict(id=cid,title=tz+'~'+te,discipline=T[cid]['discipline'],family='water',focus=c['focus'],summary=summary,history=history,example=ex,units=[unit(u,c) for u in r],facts=[bi('教學假設：'+titles[i][0]+'；'+r[i][2],'Teaching assumption: '+titles[i][1]+'; '+r[i][2]) for i in range(6)],timeline=[dict(year='1978',event='美國墾務局消能池與消能工專論修訂版出版~Reclamation publishes its revised stilling-basin and energy-dissipator monograph'),dict(year='1980',event='美國墾務局水力試驗技術手冊出版，提供試驗方法脈絡~Reclamation publishes Hydraulic Laboratory Techniques as a laboratory-method reference'),dict(year='1987',event='美國墾務局小壩設計第三版出版，整合水工設計經驗~Reclamation publishes the third edition of Design of Small Dams')],codes=['美國墾務局小壩設計第三版~Reclamation Design of Small Dams third edition','美國墾務局水力試驗技術手冊~Reclamation Hydraulic Laboratory Techniques'],landmarks=marks,place=dict(name='美國墾務局丹佛技術服務中心參照點~Reclamation Denver Technical Service Center reference',country='美國~United States',lat=39.719,lng=-105.129,query='Bureau of Reclamation Technical Service Center Denver Federal Center'),sources=sources,vendors=vendors,related=[f'b{241+(n-240)%20}',f'b{241+(n-239)%20}'],architectureNodes=[titles[i] for i in (0,2,4,6,9)],architectureEdges=[[0,1],[1,2],[2,3],[3,4],[0,3]])
 if n==241:d['codes'][1]='美國墾務局土石壩儀器與監測標準~Reclamation Embankment Dams Instrumentation and Monitoring'
 if n==242:d['codes'][1]='美國墾務局土石壩反濾層設計標準~Reclamation Embankment Dams Protective Filters'
 if n==243:d['codes'][1]='美國墾務局土石壩靜力穩定分析標準~Reclamation Embankment Dams Static Stability Analysis'
 d.update(PROJECTS.get(cid,{}))
 if '_publicFacts' in d:
  pf=d.pop('_publicFacts');d['facts']=pf+d['facts'][:6-len(pf)]
 return d

def main():
 runpy.run_path(str(P/'hydraulics_sources.py'),init_globals={'source':source,'GROUPS':GROUPS,'MARKS':MARKS})
 runpy.run_path(str(P/'hydraulics_projects.py'),init_globals={'source':source,'GROUPS':GROUPS,'MARKS':MARKS,'PROJECTS':PROJECTS})
 for f in sorted(P.glob('hydraulics_rows_*.py')):runpy.run_path(str(f),init_globals={'add':add})
 T={t['id']:t for t in json.loads((P/'targets.json').read_text())};(P/'inputs').mkdir(exist_ok=True)
 for cid,c in sorted(C.items()):(P/'inputs'/f'{cid}.json').write_text(json.dumps(metadata(cid,c,T),ensure_ascii=False,indent=2)+'\n')
 (P/'research_hydraulics.json').write_text(json.dumps(dict(reviewed='2026-10-21',courses=sorted(C),courseSources={cid:[s['key'] for s in metadata(cid,c,T)['sources']] for cid,c in sorted(C.items())},sources=list(S.values()),scope='Original hypothetical calculations; source-supported principles and publication years; comparisons are not design reconstructions; security listings unverified and null.'),ensure_ascii=False,indent=2)+'\n')
 print('Wrote',len(C),'courses',len(C)*10,'units')
if __name__=='__main__':main()
