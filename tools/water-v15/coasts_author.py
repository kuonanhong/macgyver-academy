"""Original bilingual coastal units; each numerical value is a declared teaching assumption."""
from pathlib import Path
import json,re,math,hashlib
from coasts_extensions import E
H=Path(__file__).resolve().parent
T={x['id']:x for x in json.loads((H/'targets.json').read_text())}
S={}
D={}
META={}
def pair(z,e):return z+'~'+e
def source(k,title,en,pub,url,scope,scopeEn,evidence,year=None):
 S[k]=dict(key=k,title=title,titleEn=en,publisher=pub,url=url,sourceType='primary',scope=scope,scopeEn=scopeEn,evidence=evidence,year=year,accessed='2026-10-21')
source('eurotop','海岸結構越波手冊','EurOtop: Manual on Wave Overtopping','EurOtop author consortium','https://www.overtopping-manual.com/','作者官網確認二〇〇七年首版、二〇一八年第二版及物理數值方法；不把舊計算器當新版。','Author site confirms the 2007 first and 2018 second editions and physical/numerical methods; the obsolete calculator is not treated as the new edition.','Opened turn140view0: editions and methods directly visible.',2018)
source('cem','海岸工程手冊官方書目','Coastal Engineering Manual official catalogue','US Army Corps of Engineers','https://www.publications.usace.army.mil/USACE-Publications/Engineer-Manuals/u43544q/636F617374616C20656E67696E656572696E67/','官方索引列二〇〇二年分冊及海岸過程與設計範圍；直接頁面拒絕存取，未宣稱全文核閱。','Official indexed catalogue lists 2002 parts and coastal-process/design scope; direct access was denied, so full-text review is not claimed.','Official search turn131search4; open turn140view2 returned403.',2002)
source('pwdm','香港海港工程設計手冊','Hong Kong Port Works Design Manual','Hong Kong CEDD','https://www.cedd.gov.hk/eng/publications/ceo/pwdm/index.html','官方列海堤防波堤、碼頭及海灘分冊和歷次勘誤；實際設計須核對相應最新版，算例不宣稱合規。','Official index lists seawall/breakwater, pier and beach parts and corrigenda; actual design needs the applicable current issue and examples do not claim compliance.','Opened turn133view0: Parts1–5, corrigenda2006/2014/2018/2020/2022/2025/2026.',2026)
source('newbiggin','紐比金灣海岸工程背景','Newbiggin Neighbourhood Plan coastal context','Newbiggin by the Sea Town Council','https://www.newbiggintowncouncil.gov.uk/wp-content/uploads/2023/02/01-Newbiggin-by-the-Sea-Submission-Draft-Plan.pdf','地方主管機關說明補砂與離岸防波堤；用來比較海岸功能，不推定本課消波塊或沉箱實際用於此處。','The authority describes sand recharge and an offshore breakwater; used for coastal-function comparison, without assuming course armour units or caissons were used there.','Opened turn171view0, January2023 town plan records2007 sand recharge and offshore breakwater; earlier county URL now404.',2023)
source('borth','博斯海岸防護與監測','Borth coastal defence and beach monitoring','Ceredigion County Council','https://www.ceredigion.gov.uk/resident/coast-countryside/coast-and-flood-risk-management/beach-monitoring/','主管機關確認海灘剖面監測支援博斯分期防護；方法背景不等於本課假設是現地量測。','Authority confirms beach-profile monitoring supporting Borth defence phases; methodological context does not turn the synthetic examples into field measurements.','Official search turn140search9 and report turn140search40 describe rock breakwaters, reef and shingle.')
source('sandmotor','荷蘭沙引擎養灘工程','The Sand Motor','Rijkswaterstaat','https://www.rijkswaterstaat.nl/en/projects/iconic-structures/the-sand-motor','主管機關確認二〇一一年沙引擎與自然搬運機制；不將單一案例效果普遍化。','Owner confirms the 2011 Sand Motor and natural redistribution; outcomes from one project are not universalized.','Opened turn171view2: owner confirms2011 execution and natural redistribution.',2011)
source('beachmanual','海灘管理手冊更新計畫','The updated Beach Management Manual','Environment Agency','https://www.gov.uk/flood-and-coastal-erosion-risk-management-research-reports/the-updated-beach-management-manual','官方頁區分二〇〇七年啟動、二〇一一年完成與二〇二一年網頁發布；支援維護與績效管理背景。','Official page distinguishes2007 project start,2011 completion and2021 webpage publication; supports maintenance and performance-management context.','Opened turn133view1 lines73–90 confirms completion2011 and risk/performance approach.',2011)
def compact(cid,focus,rows):
 units=[]
 for line in rows.strip().splitlines():
  if not line.strip():continue
  title,cause,model,measure,failure,mis=[x.strip()for x in line.split(' || ')]
  tz,te=title.split('~');cz,ce=cause.split('~');mz,me=model.split('~');vz,ve=measure.split('~');fz,fe=failure.split('~')
  x,y=E[cid][len(units)];xz,xe=x.split('~');yz,ye=y.split('~')
  units.append(dict(anchor=title,title=title,mechanism=pair(cz+' '+mz+' '+xz,ce+' '+me+' '+xe),model=pair('教學假設，非操作設定或設計允收值。'+mz,'Teaching assumptions, not operating settings or design acceptance limits. '+me),verify=pair(vz+yz,ve+' '+ye),failure=failure,misconception=mis,practice=measure))
 assert len(units)==10,(cid,len(units))
 D[cid]=dict(id=cid,focus=focus,units=units)
def generate():
 (H/'inputs').mkdir(exist_ok=True)
 for cid,d in D.items():
  t=T[cid];m=META[cid];u=d['units'];zf,ef=d['focus'].split('~')
  facts=[x['model'] for x in u if len(re.findall(r'[㐀-鿿]',x['model'].split('~')[0]))<=90 and len(re.findall(r'[A-Za-z]{2,}',x['model'].split('~')[1]))<=45][:6]
  assert len(facts)==6,(cid,'short numerical facts needed')
  summary=pair(zf+'。課程從邊界辨識與資料整理走到水理量化、構造介面及驗證紀錄；每一步把計算結果連回可量測的證據。十個不同單元分別處理關鍵機制，不以名義尺寸或單一通過率代替整體工程判斷，並明列合成算例與現地資料的差別。',ef+'. The course moves from boundary identification and evidence to hydraulic quantification, structural interfaces and verification records. Ten distinct units connect each calculated quantity to measurable evidence. Nominal geometry or a single pass rate does not establish whole-system performance, and synthetic teaching examples remain separate from field observations.')
  history=pair(m['history'][0],m['history'][1])
  example=pair('以下為原創合成算例，不是地標工程的實測或推薦操作值。'+u[0]['model'].split('~')[0]+m['sensitivity'].split('~')[0]+'重新計算前先列固定條件、單位、適用尺度及可能失效的邊界。把模型敏感度與測量誤差分開，不能將單一參數變化直接當成工程風險或壽命比例。比較兩次結果後，記錄還需要哪些獨立證據，並由負責專業人員判斷適用性。','This original synthetic example is neither a landmark measurement nor a recommended operating value. '+u[0]['model'].split('~')[1]+' '+m['sensitivity'].split('~')[1]+' Before recalculating, list fixed conditions, units, applicable scale and boundaries that could fail. Separate model sensitivity from measurement uncertainty: a parameter change does not directly give a proportional change in engineering risk or service life. Compare the results, record independent evidence still needed, and have the responsible specialist determine applicability.')
  vendors=[]
  for k in m['sources'][:2]:
   s=S[k];vendors.append(dict(name=s['publisher'],nameEn=s['publisher'],business='發布本課相關工程方法、研究或公共設施資訊。',businessEn='Publishes relevant engineering methods, research or public infrastructure information.',url=s['url'],investorUrl='',security=None,role=s['scope'],roleEn=s['scopeEn']))
  d.update(title=t['title']+'~'+t['titleEn'],discipline=t['discipline'],family='water',summary=summary,history=history,example=example,facts=facts,timeline=[dict(year=y,event=e)for y,e in m['timeline']],codes=m['codes'],landmarks=m['marks'],place=m['place'],sources=[{k:v for k,v in S[x].items()if k not in ('evidence','year','accessed')}for x in m['sources']],vendors=vendors,related=m['related'],architectureNodes=[x['title'].split('~')for x in [u[0],u[2],u[4],u[6],u[9]]],architectureEdges=[[0,1],[1,2],[2,3],[3,4],[4,1]])
  (H/'inputs'/f'{cid}.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
 research={'accessed':'2026-10-21','sources':S,'courses':{cid:m['sources']for cid,m in META.items()},'limits':['All numerical unit models and facts are declared synthetic teaching assumptions, not measured project data.','Landmarks are explicitly comparisons unless source text confirms the method.','No financial listing claims; every security is null.','Source scopes distinguish official indexed excerpts from direct reading.']}
 old=H/'research_coasts.json'
 if old.exists():
  previous=json.loads(old.read_text());previous['sources'].update(S);previous['courses'].update(research['courses']);research=previous
 old.write_text(json.dumps(research,ensure_ascii=False,indent=2)+'\n')
 print('Wrote',len(D),'coastal courses')
def coastal_meta(cid,sensitivity,sources=None):
 META[cid]=dict(sources=sources or ['eurotop','pwdm','cem','newbiggin','borth'],marks=['紐比金灣防護：功能比較~Newbiggin Bay defence: functional comparison','博斯海岸防護：監測比較~Borth coastal defence: monitoring comparison'],place=dict(name='紐比金灣公共海岸背景區~Newbiggin Bay public coastal context',country='英國~United Kingdom',lat=55.182,lng=-1.507,query='Newbiggin by the Sea Northumberland'),timeline=[('2002','美國工兵團官方目錄列海岸工程手冊分冊~USACE official catalogue lists Coastal Engineering Manual parts'),('2007','歐洲研究團隊發布首版海岸越波手冊~European research team publishes the first overtopping manual'),('2018','海岸越波手冊第二版擴展方法與解釋~The second overtopping manual expands methods and interpretation')],codes=['海岸工程手冊EM1110-2-1100，按分冊適用範圍閱讀~Coastal Engineering Manual EM1110-2-1100, within each part scope','海岸越波手冊EurOtop，第二版二〇一八年~EurOtop Manual, second edition2018','香港海港工程設計手冊第四部，核對現行勘誤~Hong Kong Port Works Design Manual Part4, check applicable corrigenda'],related=['b281','b282'] if cid not in ('b281','b282') else (['b282','b286']if cid=='b281'else['b281','b284']),sensitivity=sensitivity,history=('本課的知識脈絡採用可核對的工程文獻，而不替工法編造單一發明年份。美國工兵團官方目錄列出二〇〇二年海岸工程手冊分冊；越波研究團隊於二〇〇七年發布首版手冊，二〇一八年第二版擴展結構型式、試驗與結果解釋。香港海港手冊持續列出勘誤，提醒設計引用必須指定版本。紐比金灣與博斯是海岸防護和監測的比較案例，不表示兩地採用了本課每項構件或假設尺寸。歷史資料用於理解方法演進，合成數據則另作學徒推理練習。','The knowledge history follows verifiable publications rather than inventing a single date when the technique was created. USACE lists its Coastal Engineering Manual parts in2002. The overtopping authors issued the first manual in2007 and expanded structural types, testing and interpretation in the2018 edition. Hong Kong continues to list corrigenda, demonstrating why an applied design must identify its reference version. Newbiggin Bay and Borth are comparisons of coastal protection and monitoring, not claims that both used every component or assumed dimension in this course. Publication history explains methodological development; synthetic values separately support the apprentice exercises.'))
