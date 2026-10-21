"""Original bilingual underground-course authoring source. Course numbers are teaching assumptions."""
from pathlib import Path
import json, math, sys
HERE=Path(__file__).resolve().parent
TARGET={x['id']:x for x in json.loads((HERE/'targets.json').read_text())}
COURSES={}
SOURCES={}
def source(key,zh,en,pub,url,scope,scopeen):
 SOURCES[key]=dict(key=key,title=zh,titleEn=en,publisher=pub,url=url,sourceType='primary',scope=scope,scopeEn=scopeen)
source('geo-site','土木工程拓展署：岩土指南二地盤勘察','CEDD: Geoguide 2, Guide to Site Investigation','Geotechnical Engineering Office, CEDD','https://www.cedd.gov.hk/eng/publications/geo/geoguides/geo-g2/','確認二〇一七年版本與勘察範圍；課內數值為原創教學假設，不是本指南的工程實測。','Confirms the 2017 edition and investigation scope; numerical exercises are original assumptions, not field data from this guide.')
source('geo-cavern','土木工程拓展署：岩土指南四岩洞工程','CEDD: Geoguide 4, Guide to Cavern Engineering','Geotechnical Engineering Office, CEDD','https://www.cedd.gov.hk/eng/publications/geo/geoguides/geo-g4/index.html','確認二〇一八年第二版與岩洞工程範圍；不是特定岩洞的施工設計。','Confirms the 2018 second edition and cavern-engineering scope; not a construction design for a particular cavern.')
source('geo-wall','土木工程拓展署：岩土指南一擋土牆設計','CEDD: Geoguide 1, Guide to Retaining Wall Design','Geotechnical Engineering Office, CEDD','https://www.cedd.gov.hk/eng/publications/geo/geoguides/geo-g1/index.html','一般土壓、水壓與擋土穩定背景；官方明言不全面涵蓋深開挖與海事結構，不能當其完整設計規範。','General earth-pressure, water-pressure and retaining-stability background; the official scope excludes comprehensive coverage of deep excavations and maritime structures.')
source('usace-rock','美國陸軍工兵署：岩石隧道與豎井手冊','USACE: Tunnels and Shafts in Rock, EM 1110-2-2901','U.S. Army Corps of Engineers','https://www.publications.usace.army.mil/USACE-Publications/Engineer-Manuals/u43544q/54756E6E656C7320616E642053686166747320696E20526F636B/','官方目錄確認一九九七年手冊；作為岩石開挖、襯砌與監測的公開指南背景。','Official catalog confirms the 1997 manual; public guidance background for rock excavation, lining and monitoring.')
source('fhwa-ground','美國聯邦公路管理局：地盤改良技術資料','FHWA: Ground Improvement','Federal Highway Administration','https://www.fhwa.dot.gov/engineering/geotech/improvement/','官方列明灌漿、排水板、碎石樁、夯實、攪拌等範圍，並連結二〇一七年地盤改良參考手冊。','Official scope includes grouting, drains, stone columns, compaction and mixing, with links to the 2017 ground-modification reference manuals.')
source('fhwa-anchors','美國聯邦公路管理局：地錨與錨定系統','FHWA: Ground Anchors and Anchored Systems, FHWA-IF-99-015','Federal Highway Administration / National Transportation Library','https://rosap.ntl.bts.gov/view/dot/712','確認一九九九年地錨指南、試驗、防蝕與整體穩定的範圍；不提供本課假設的允收值。','Confirms the 1999 anchor guide and scope of testing, corrosion protection and overall stability; does not supply acceptance limits for these hypothetical exercises.')
source('fhwa-micro','美國聯邦公路管理局：微型樁設計施工手冊','FHWA: Micropile Design and Construction, FHWA-NHI-05-039','Federal Highway Administration / National Transportation Library','https://rosap.ntl.bts.gov/view/dot/50231','確認二〇〇五年手冊與基礎托底、結構設計、檢驗和載重試驗範圍。','Confirms the 2005 manual and its foundation-support, structural-design, inspection and load-testing scope.')
source('herrenknecht-jansen','海瑞克：詹森礦井工程','Herrenknecht: Jansen Mine','Herrenknecht','https://www.herrenknecht.com/en/references/referencesdetail/jansen-mine/','製造商公開案例確認詹森使用兩台豎井懸臂式鑽掘機；本課性能數值另為假設。','Manufacturer case confirms two Shaft Boring Roadheaders at Jansen; course performance numbers are separate assumptions.')
source('herrenknecht-sbr','海瑞克：豎井懸臂式鑽掘機','Herrenknecht: Shaft Boring Roadheader','Herrenknecht','https://www.herrenknecht.com/en/products/productdetail/shaft-boring-roadheader-sbr/','公開設備型式與切削概念；不把產品能力當場址產能保證。','Public machine type and cutting concept; product capability is not a site-production guarantee.')
source('dmc-sbr','迪艾姆西：豎井鑽掘公開案例','DMC Mining: Leaders in SBR Technology','DMC Mining Services','https://dmcmining.com/shaft-sinking/sbr/','承包商確認詹森豎井施工經驗，用於設備與施工系統界面的比較。','Contractor confirms Jansen shaft-sinking experience, used to compare interfaces between machinery and construction systems.')
source('keller-tech','凱勒：地工技術目錄','Keller: Techniques','Keller Group','https://www.keller.com/expertise/techniques','承包商技術目錄確認地盤改良、基礎、擋土與監測技術分類；不聲稱任何未核對工程採用特定工法。','Contractor directory confirms improvement, foundation, retention and monitoring categories; no unverified project-method attribution is made.')
for key,slug,zh,en in [('keller-diaphragm','diaphragm-walls-barrettes-grab','連續壁與壁樁','Diaphragm walls and barrettes'),('keller-secant','secant-pile-walls','咬合樁牆','Secant pile walls'),('keller-jet','jet-grouting','噴射灌漿','Jet grouting'),('keller-compensation','compensation-fracture-grouting','補償與劈裂灌漿','Compensation and fracture grouting'),('keller-compaction','compaction-grouting','壓密灌漿','Compaction grouting')]:
 source(key,'凱勒：'+zh,'Keller: '+en,'Keller Group','https://www.keller.com/expertise/techniques/'+slug,'承包商公開說明'+zh+'的功能與工法範圍；本課算例不是廠商配方或實際施工參數。','Contractor description of the function and scope of '+en.lower()+'; exercises are neither vendor recipes nor actual operating parameters.')

def split(s):
 a=s.split('~'); assert len(a)==2,s; return a

def join(a,b): return a+'~'+b

def unit(row,course):
 # Seven authored fields; no model or mechanism is imported from another course.
 a,m,q,v,f,wrong,p = [s.strip() for s in row.split('||')]
 az,ae=split(a); mz,me=split(m); qz,qe=split(q); vz,ve=split(v); fz,fe=split(f); pz,pe=split(p)
 return dict(anchor=a,title=join(az+'的機理與驗證',ae+' mechanism and verification'),mechanism=m,
 model=join('原創教學假設：'+qz+'。此式用於量級與單位檢查，並非現場允收值。','Original teaching assumptions: '+qe+'. This calculation checks scale and units; it is not a site acceptance limit.'),
 verify=v,failure=f,misconception=wrong,practice=p)

def add(cid,focus,summary,rows,example,sources,marks,history=None,timeline=None):
 t=TARGET[cid]; units=[unit(r,cid) for r in rows.strip().splitlines() if r.strip()]; assert len(units)==10,(cid,len(units))
 zf,ef=split(focus)
 if history is None:
  history=join('地下工程的設計方法隨地盤勘察、材料試驗與施工監測逐步整合，單靠完工後的外觀已不能說明埋藏構件的性能。美國陸軍工兵署於一九九七年發布岩石隧道與豎井手冊，香港土木工程拓展署提供二〇一七年地盤勘察指南更新，二〇一八年再發布岩洞工程指南第二版。本課以'+zf+'為主軸，將公開指南的問題分類轉化成原創教學算例；比較案例不表示兩案使用相同構件或工法。本課只重建公開原理與工程邏輯，不代表任何專案的設計文件。','Underground engineering has progressively joined site investigation, material testing and construction monitoring because the visible finished surface does not reveal the performance of buried components. USACE published its rock tunnel and shaft manual in 1997; CEDD provides the 2017 site-investigation guide update and the 2018 second edition of its cavern guide. This course develops '+ef.lower()+' through original educational models. Named comparisons do not imply identical components or construction methods. The course reconstructs public principles and engineering reasoning only, not the design documents of any project.')
 if timeline is None:
  timeline=[dict(year='1997',event='美國陸軍工兵署發布岩石隧道與豎井工程手冊~USACE publishes its engineering manual for tunnels and shafts in rock'),dict(year='2017',event='香港地盤勘察指南提供持續更新版本作為調查依據~Hong Kong provides an updated site-investigation guide as an investigation reference'),dict(year='2018',event='香港岩洞工程指南第二版整合岩洞設計施工背景~The second Hong Kong cavern-engineering guide consolidates design and construction context')]
 facts=[]
 for u in units[:6]:
  qz,qe=split(u['model'])
  qz=qz.removeprefix('原創教學假設：').removesuffix('。此式用於量級與單位檢查，並非現場允收值。').split('；')[0]
  qe=qe.removeprefix('Original teaching assumptions: ').removesuffix('. This calculation checks scale and units; it is not a site acceptance limit.').split(';')[0]
  facts.append(join('合成教學假設：'+qz,'Synthetic teaching assumptions: '+qe))
 src=[SOURCES[k] for k in sources]
 vendors=[]
 for s in src[:2]:
  vendors.append(dict(name=s['publisher']+'（公開資料機構）',nameEn=s['publisher'],business='提供本課相關的公開技術資料，角色是工程知識來源而非工程性能背書。',businessEn='Provides relevant public technical information as an engineering knowledge source, not an endorsement of performance.',url=s['url'],investorUrl='',security=None,role='研究'+zf+'的公開技術範圍與證據限制',roleEn='Study the public technical scope and evidence limits for '+ef.lower()))
 num=int(cid[1:]); rel=['b'+str(num-1 if num>176 else 177),'b'+str(num+1 if num<200 else 198)]
 if len(set(rel))<2:rel=['b177','b178']
 nodes=[split(units[i]['anchor']) for i in [0,1,3,6,8,9]]
 COURSE=dict(id=cid,title=t['title']+'~'+t['titleEn'],discipline=t['discipline'],family=t['family'],focus=focus,summary=summary,units=units,example=example,history=history,facts=facts,timeline=timeline,codes=['地盤勘察岩土指南二：用於調查與描述的範圍界定~Geoguide 2, Guide to Site Investigation: scope for investigation and description','公開技術指南須按所在法域及專案設計基準選用~Public technical guides must be selected under the project jurisdiction and design basis'],landmarks=marks,place=dict(name='香港土木工程拓展署地工資料參照點~Hong Kong CEDD geotechnical information reference point',country='香港~Hong Kong',lat=22.297,lng=114.172,query='Civil Engineering and Development Department Hong Kong'),sources=src,vendors=vendors,related=rel,architectureNodes=nodes,architectureEdges=[[0,1],[1,2],[2,3],[3,4],[4,5],[3,0]])
 COURSE['codes'][1]=join(src[0]['title'],src[0]['titleEn'])
 COURSES[cid]=COURSE

def write():
 for cid,d in COURSES.items():
  enrich_metadata(d)
  (HERE/'inputs'/f'{cid}.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
 print('wrote',', '.join(COURSES))

def compact(rows):
 """Compose standalone fields from unit-specific physics, evidence and boundary notes.
 Repeated information across a unit is intentional: each generated step is standalone.
 No length-driven padding or copying between courses occurs.
 """
 out=[]
 for row in rows.strip().splitlines():
  if not row.strip():continue
  a,m,q,v,f,wrong,p,b=[s.strip() for s in row.split('||')]
  mz,me=split(m); vz,ve=split(v); fz,fe=split(f); pz,pe=split(p); bz,be=split(b)
  out.append(' || '.join([a,join(mz+bz,me+' '+be),q,join(vz+pz,ve+' '+pe),join(fz+bz,fe+' '+be),wrong,join(pz+bz,pe+' '+be)]))
 return '\n'.join(out)

# Public milestones are source publication/version dates, never invented project dates.
MILESTONES={
 'geo-site':('2017','香港地盤勘察指南二提供二〇一七年更新版本，作為調查證據背景','CEDD provides the 2017 updated Geoguide 2 as an investigation reference'),
 'geo-cavern':('2018','香港發布岩洞工程指南第二版，整理岩洞規劃設計及施工實務','CEDD publishes the second cavern-engineering guide covering planning, design and construction'),
 'geo-wall':('2020','香港擋土牆設計指南提供二〇二〇年版本，其適用範圍不全面涵蓋深開挖','CEDD provides the 2020 retaining-wall guide, whose scope does not comprehensively cover deep excavation'),
 'usace-rock':('1997','美國陸軍工兵署發布岩石隧道與豎井工程手冊，建立公開工程參考','USACE publishes its rock-tunnel and shaft manual as a public engineering reference'),
 'usace-sheet':('1994','美國陸軍工兵署發布鋼板樁牆設計手冊，涵蓋土體結構互制','USACE publishes its sheet-pile wall manual including soil-structure interaction'),
 'fhwa-anchors':('1999','美國聯邦公路管理局發布地錨及錨定系統指南，包含試驗與防蝕背景','FHWA publishes the ground-anchor guide including testing and corrosion-protection context'),
 'fhwa-micro':('2005','美國聯邦公路管理局發布微型樁設計施工參考手冊，整合檢驗與載重試驗','FHWA publishes the micropile design and construction reference including inspection and load testing'),
 'fhwa-ground':('2017','美國聯邦公路管理局地盤改良頁列入兩冊地盤改良參考手冊','FHWA lists the two-volume ground-modification reference manual in its improvement guidance'),
 'crossrail-passages':('2016','Crossrail發布聯絡通道工法與地質資料，明確說明所列通道未採凍結','Crossrail publishes its passage-method dataset, explicitly identifying nonuse of freezing in the listed passages')}
source('jtc-caverns','裕廊集團：裕廊岩洞','JTC: Jurong Rock Caverns','JTC Corporation','https://www.jtc.gov.sg/find-space/jurong-rock-caverns','業主確認地下儲存岩洞的用途與規模；用於大型岩洞比較，不宣稱本課假設是專案設計。','Owner confirms underground storage function and scale; used for cavern comparison without attributing educational models to the project.')
source('dsd-stanley','香港渠務署：赤柱污水處理廠岩洞','DSD: Stanley Sewage Treatment Works','Drainage Services Department, Hong Kong','https://www.dsd.gov.hk/EN/HTML/20520.html','業主確認岩洞污水處理設施、三個岩洞與一九九五年完工；本課僅作功能及地質界面比較。','Owner confirms the cavern sewage facility, three caverns and 1995 completion; used for functional and ground-interface comparison only.')
source('keller-benjamin','凱勒：倫敦本傑明街','Keller: Benjamin Street','Keller UK','https://www.keller.co.uk/projects/benjamin-street','承包商確認咬合樁地下室工程；網頁樁徑有明顯單位疑點，故不引用該尺寸。','Contractor confirms a secant-pile basement; the page has a suspect diameter unit, which is not quoted.')
source('keller-harley','凱勒：倫敦哈利街一四一號','Keller: 141 Harley Street','Keller UK','https://www.keller.co.uk/projects/141-harley-street','承包商確認受限淨高微型樁及咬合樁工程；其他課程僅比較空間及資產界面，不宣稱使用未核對工法。','Contractor confirms restricted-headroom mini and secant piling; other courses compare space and asset interfaces without unverified method attribution.')
source('keller-gallery','凱勒：倫敦國家美術館','Keller: National Gallery','Keller UK','https://www.keller.co.uk/projects/national-gallery','承包商確認受限空間小直徑咬合樁施工，僅比較設備及幾何約束。','Contractor confirms restricted-access secant minipiling, used only to compare equipment and geometric constraints.')
source('herrenknecht-nezhinsky','海瑞克：涅任斯基礦井','Herrenknecht: Nezhinsky Mine','Herrenknecht','https://www.herrenknecht.com/en/references/referencesdetail/nezhinsky-mine/','製造商確認豎井懸臂式鑽掘設備案例，只比較豎井系統而不代入未核對工程參數。','Manufacturer confirms a shaft-boring roadheader project, used for system comparison without unverified numerical project parameters.')

def enrich_metadata(d):
 cid=d['id']
 extra={'b176':['herrenknecht-jansen','herrenknecht-nezhinsky'],'b177':['herrenknecht-nezhinsky'],'b178':['jtc-caverns','dsd-stanley'],'b181':['keller-benjamin','keller-harley'],'b185':['keller-harley','keller-gallery']}.get(cid,[])
 if cid=='b176':d['landmarks']=['詹森礦井：深井襯砌界面比較~Jansen Mine: deep-lining interface comparison','涅任斯基礦井：豎井系統比較~Nezhinsky Mine: shaft-system comparison']
 if cid=='b181':d['sources']=[s for s in d['sources'] if s['key']!='geo-wall']
 for key in extra:
  if key not in [s['key'] for s in d['sources']]:d['sources'].append(SOURCES[key])
 assert len(d['sources'])<=5,(cid,'sources')
 events=[]
 for s in d['sources']:
  if s['key'] in MILESTONES:events.append(MILESTONES[s['key']])
 events=sorted(events,key=lambda x:x[0])[:3]
 while len(events)<2:
  events.append(('2026','本教材核對公開來源及其技術適用範圍，日期不是工程完工年份','This curriculum verifies public sources and technical scope; this is not a project completion date'))
 events.append(('2026','本教材重算原創帶單位算例及敏感度，明確區分公開事實與教學假設','This curriculum recalculates original unit-bearing examples and sensitivity, separating public facts from teaching assumptions'))
 d['timeline']=[dict(year=y,event=join(z,e)) for y,z,e in events]
 z,e=split(d['summary'])
 evz='；'.join(y+'年：'+zz for y,zz,ee in events[:-1]); eve='; '.join(y+': '+ee for y,zz,ee in events[:-1])
 d['history']=join(z+'公開資料沿革以指南出版及資料覆核為準，不冒充個別工程施工史。'+evz+'。比較案例僅說明工程用途與界面差異，未核對的工法不作實績聲稱。本課重建公開原理及原創教學算例，不代表任何專案設計文件。',e+' The source chronology records guide publication and evidence review rather than inventing a project construction history. '+eve+'. Named comparisons illustrate functions and interfaces without attributing unverified methods. This course reconstructs public principles with original educational calculations, not the design documents of any project.')
 # Guide names, rather than a contractor marketing page, occupy the guideline list.
 refs=[s for s in d['sources'] if s['key'] in MILESTONES and s['key']!='crossrail-passages']
 d['codes']=[join(s['title'],s['titleEn']) for s in refs[:3]]
 if len(d['codes'])<2:
  d['codes'].append('英國地盤勘察實務準則 BS 5930：由岩土指南二說明適用關係~BS 5930 Code of practice for ground investigations, as contextualized by Geoguide 2')
