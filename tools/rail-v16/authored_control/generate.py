#!/usr/bin/env python3
"""Generate authored b368–b400 inputs, retaining inspectable numerical evidence."""
import json, math, pathlib, re, sys
HERE=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from models import MODELS
from courses import COURSES
try: import courses_tail
except ModuleNotFoundError as e:
    if e.name!='courses_tail': raise
from sources import SOURCES,GROUPS
ROOT=HERE.parent
TARGETS={t['id']:t for t in json.loads((ROOT/'targets.json').read_text())}

def split(s): return s.split('~')
def pair(z,e): return z+'~'+e
def join(*items):
    parts=[split(s) for s in items]
    return pair(''.join(p[0] for p in parts),' '.join(p[1] for p in parts))
def fmt(x): return format(x,'.6g')
def calc(m,values=None):
    vals={q[0]:q[1] for q in m['quantities']};vals.update(values or {})
    return eval(m['expression'],{'__builtins__':{},'sqrt':math.sqrt,'log10':math.log10,'pi':math.pi},vals)
def numeric(m):
    return pair('；'.join(f'{split(q[3])[0]} {q[0]}={fmt(q[1])} {q[2]}' for q in m['quantities']), '; '.join(f'{split(q[3])[1]} {q[0]}={fmt(q[1])} {q[2]}' for q in m['quantities']))
def scenario(m):
    key=m['sensitivity']; q=next(q for q in m['quantities'] if q[0]==key)
    is_count=q[2] in {'bits','cases','trains','persons','points','cycles','alarms','axles','packets','independent trials'}
    changed=q[1]+1 if is_count else q[1]*1.1
    vals={key:changed};v=calc(m);new=calc(m,vals)
    if key=='tested': assert changed<=next(q[1] for q in m['quantities'] if q[0]=='total')
    assert not is_count or changed==int(changed)
    return dict(symbol=key,base=q[1],changed=changed,inputUnit=q[2],integerStep=is_count,baseline=v,result=new,outputUnit=m['result_unit'],inputPercent=(changed/q[1]-1)*100,outputPercent=(new/v-1)*100 if v else None)

def model_text(m):
    z,e=split(numeric(m));bz,be=split(m['boundary']);res=fmt(calc(m));expr=m['expression'];unit=m['result_unit']
    return pair(f'原創假想教學輸入：{z}。公式 y={expr}，代入得 y={res} {unit}。邊界：{bz}',f'Original hypothetical teaching inputs: {e}. Formula y={expr} gives y={res} {unit}. Boundary: {be}')

def unit(row,index):
    m=MODELS[row['key']];tz,te=split(row['title']);bz,be=split(m['boundary']);cz,ce=split(row['context'])
    mechanism=join(row['context'],m['mechanism'],pair('解釋前先固定模型適用範圍：'+bz,'Before interpreting the result, fix its domain: '+be))
    verify=join(m['verification'],pair(f'以「{tz}」為驗證目標，先寫出預期變化方向及可分辨的替代原因，再保存原始讀值、單位、校正版本與時間窗。只有比較同一系統邊界的資料，才判定殘差是否支持這項機制。',f'For {te.lower()}, state the expected direction and distinguishable alternative causes before collecting data. Retain raw readings, units, calibration version and observation window. Compare evidence within the same system boundary before deciding whether the residual supports this mechanism.'))
    failure=join(m['failure'],pair(f'回到「{tz}」的輸入鏈逐項定位；先重播單一異常，再比較共同原因的組合。保留不確定項，避免為了讓結果符合預期而刪去不利證據。',f'Trace the input chain for {te.lower()}. Replay one anomaly first, then compare common-cause combinations. Retain uncertain observations rather than discarding adverse evidence to force the expected conclusion.'))
    s=scenario(m);key=s['symbol'];quantity=next(q for q in m['quantities'] if q[0]==key);qz,qe=split(quantity[3])
    delta='增加一個可計數單位' if s['integerStep'] else '增加百分之十'
    deltaen='increase by one whole count' if s['integerStep'] else 'increase by ten percent'
    practice=pair(f'只把{qz} {key} 從 {fmt(s["base"])} 改成 {fmt(s["changed"])} {s["inputUnit"]}（{delta}），其餘輸入固定。重算結果應由 {fmt(s["baseline"])} 變為 {fmt(s["result"])} {s["outputUnit"]}。先說明「{tz}」中變化的因果方向，再檢查適用邊界是否仍成立，提交計算與一個可反駁此解釋的觀測。',f'Change only {qe} {key} from {fmt(s["base"])} to {fmt(s["changed"])} {s["inputUnit"]} ({deltaen}), holding other inputs fixed. Recalculate {fmt(s["baseline"])} to {fmt(s["result"])} {s["outputUnit"]}. Explain the causal direction for {te.lower()}, check that the stated boundary still holds, and submit the calculation plus one observation that could refute the explanation.')
    return dict(anchor=row['title'],title=row['title'],mechanism=mechanism,model=model_text(m),verify=verify,failure=failure,misconception=m['misconception'],practice=practice)

CODES={
'control':['IEC 62278-1:2025 鐵路可靠度與安全方法；適用範圍須依專案確認~IEC 62278-1:2025 railway RAMS methodology; project applicability requires assessment','IEC 62278:2002 歷史版方法參考，不宣稱仍為現行要求~IEC 62278:2002 historical methodological reference, without claiming current mandatory status'],
'station':['FTA 軌道緊急整備指南，1985 原版及 1991 重印之歷史方法~FTA rail emergency-preparedness guide, original 1985 and 1991 reprint as historical methodology','臺灣鐵道車站概念設計指引，2025 年版，非跨國統一法規~Taiwan railway-station conceptual-design guidance, 2025 edition, not a universal international code'],
'access':['美國運輸部 ADA 運輸設施標準 2006 版；與司法部一般設施版區分~US DOT ADA transportation-facility standards, 2006 edition; distinguish the DOJ general-facility standards','FRA 城際與高速鐵路月台無障礙指引，2022 年版~FRA accessible intercity and high-speed rail platform guidance, 2022 edition'],
'machinery':['ISO 12100:2010 機械風險評估與降低方法，非設備額定證明~ISO 12100:2010 machinery risk assessment and reduction, not equipment rating certification','ISO 13849-1:2023 安全相關控制設計，教材不宣告性能等級~ISO 13849-1:2023 safety-related control design, with no performance-level claim for this lesson'],
'crossing':['FHWA 公路鐵路平交道手冊第三版，2019 年，美國方法背景~FHWA Highway–Rail Crossing Handbook, third edition, 2019, United States methodological context','FRA 平交道人因指引，2006 年研究報告，非現場控制設定~FRA human-factors guidance for highway–rail intersections, 2006 research report, not field control settings'],
'cwr':['FRA 長焊鋼軌通用計畫指引，2021 年版，美國適用背景~FRA continuous-welded-rail generic plan guidance, 2021 edition, United States context','IEC 62278-1:2025 鐵路可靠度與安全方法，監測證據範圍須確認~IEC 62278-1:2025 railway RAMS methodology; establish the scope of monitoring evidence'],
}
for g in ('aps','monorail','maglev'): CODES[g]=CODES['control']
CODES['suspended']=CODES['machinery']

def source(key,title,en,publisher,url,scope):
    return dict(key=key,title=title,titleEn=en,publisher=publisher,url=url,sourceType='primary',scope=split(scope)[0],scopeEn=split(scope)[1])
PROJECTS={
'gotthard':source('gotthard-reference','瑞士列車防護系統背景','Swiss train-protection reference','SBB','https://company.sbb.ch/en/railway-development/services-rus/railway-environment/railway-environment/etcs.html','支持聖哥達代表工程與列控背景；課程數值均非該隧道設定。~Supports Gotthard as a reference and train-control context; course values are not tunnel settings.'),
'elizabeth':source('elizabeth-reference','伊莉莎白線官方工程背景','Official Elizabeth line reference','Transport for London','https://tfl.gov.uk/modes/Elizabeth-line/','支持代表性鐵路路線名稱與官方營運來源，未聲稱其使用本課假想配置。~Supports the reference route and official operator, without claiming use of the hypothetical lesson arrangement.'),
'kings':source('kings-cross-reference','國王十字車站官方歷史','Official history of Kings Cross station','Network Rail','https://www.networkrail.co.uk/who-we-are/our-history/iconic-infrastructure/the-history-of-london-kings-cross-station/','支持車站整合與改建工程背景，不引用客流量或允收值。~Supports station integration and redevelopment context, without importing passenger flows or acceptance limits.'),
'main':source('taipei-main-reference','臺北車站官方資訊圖','Official Taipei Main Station information map','Taipei Rapid Transit Corporation','https://web.metro.taipei/img/ALL/INFOPDF/051.pdf','支持車站存在及轉乘背景，不複製圖像或宣稱本課為實際車站模型。~Supports station identity and interchange context; the map is not copied and this is not an actual station model.'),
'pat':source('pat-heung-reference','港鐵機廠官方背景','Official MTR depot reference','MTR Corporation','https://www.mtr.com.hk/en/corporate/operations/detail_depots.html','支持八鄉機廠作為維修工程參考，不聲稱使用任何特定算例設備。~Supports Pat Heung as a maintenance reference without claiming use of any particular exercise equipment.'),
'beitou':source('beitou-reference','北投維修組織官方背景','Official Beitou maintenance reference','Taipei Rapid Transit Corporation','https://www.metro.taipei/cp.aspx?n=195274F164A8EE0B&s=EAC107016EAB69E7','支持北投維修工程背景，不聲稱特定機具或供應合約。~Supports Beitou maintenance context, without asserting particular machines or supply contracts.'),
'japan':source('yamanashi-reference','山梨磁浮試驗線官方背景','Official Yamanashi maglev reference','Central Japan Railway Company','https://global.jr-central.co.jp/en/company/_pdf/superconducting_maglev.pdf','支持山梨及宮崎試驗發展背景，所有假想導梁數值另行設定。~Supports Yamanashi and Miyazaki development context; hypothetical guideway values are separately authored.'),
'dresden':source('dresden-reference','德勒斯登懸掛鐵路官方背景','Official Dresden suspension railway reference','Dresdner Verkehrsbetriebe','https://www.dvb.de/en-gb/excursions/hillside-railways/schwebebahn','支持第二個懸掛系統歷史對照；纜索牽引與烏帕塔爾的驅動方式不同。~Supports a second suspended-system comparison; its cable drive differs from Wuppertal.'),
'hitachi':source('monorail-reference','東京單軌官方產品背景','Official Tokyo monorail reference','Hitachi Rail','https://www.hitachirail.com/products-and-solutions/rolling-stock/monorail-solutions/tokyo-monorail/','支持東京單軌代表工程背景，不將公開產品數據作成本課梁設計。~Supports Tokyo monorail context without turning public product data into the beam design used here.'),
'chongqing':source('chongqing-reference','重慶單軌歷史工程公告','Historical Chongqing monorail announcement','Hitachi','https://www.hitachi.com/New/cnews/E/2002/1107/index.html','僅支持重慶跨座式單軌代表工程背景，未延伸推論其他設備合約。~Supports Chongqing straddle-monorail context only, without inferring other equipment contracts.'),
}

def vendor(name,en,business,enbusiness,url,role,enrole):
    return dict(name=name,nameEn=en,business=business,businessEn=enbusiness,url=url,role=role,roleEn=enrole,security=None)
VENDORS={
'control':[vendor('國際電工委員會','IEC','電工與鐵路方法標準','Electrical and railway methodological standards','https://webstore.iec.ch/en/publication/68933','方法出版機構，非本課設備供應商','Methodology publisher, not a supplier to the fictional lesson'),vendor('歐洲鐵路局','European Union Agency for Railways','鐵路互通規格與技術協調','Railway interoperability specifications and coordination','https://www.era.europa.eu/','官方規格資訊機構，不推論任何個別設備採購','Official specification information, with no claim about individual procurement')],
'station':[vendor('臺北捷運公司','Taipei Rapid Transit Corporation','捷運車站與列車營運','Metro station and train operation','https://www.metro.taipei/','營運工程參考機構，未宣稱本課是其設計','Operating reference organization; this is not represented as its design'),vendor('英國鐵路網公司','Network Rail','鐵路基礎設施與車站','Railway infrastructure and stations','https://www.networkrail.co.uk/','車站整合背景，無本課虛構採購關係','Station-integration context with no fictional procurement claim')],
'machinery':[vendor('海根賽特','Hegenscheidt','輪對加工與鐵路維修設備','Wheelset machining and railway maintenance equipment','https://www.hegenscheidt.com/en/','產品角色參考，不宣稱供應本課列出的任何機廠','Product-role reference; no claim of supplying any listed depot'),vendor('國際標準化組織','ISO','機械風險與品質方法標準','Machinery-risk and quality methodology standards','https://www.iso.org/standard/73481.html','標準出版機構而非設備認證結論','Standards publisher, not an equipment-certification conclusion')],
'aps':[vendor('阿爾斯通','Alstom','鐵路車輛及地面供電方案','Rail vehicles and ground-level power systems','https://www.alstom.com/solutions/infrastructure/aps-catenary-free-tramway-proven-operations-service','公開產品原理參考，算例非產品額定值','Public product context; example values are not product ratings'),vendor('國際電工委員會','IEC','鐵路可靠度與安全方法','Railway RAMS methodology','https://webstore.iec.ch/en/publication/68933','方法出版機構，不對本課示範提供認證','Method publisher, without certification of this demonstration')],
'monorail':[vendor('日立鐵道','Hitachi Rail','單軌與軌道系統產品','Monorail and railway systems','https://www.hitachirail.com/products-and-solutions/rolling-stock/monorail-solutions/','公開技術背景，課程梁截面並非其設計','Public technology context; the teaching section is not its design'),vendor('國際電工委員會','IEC','鐵路可靠度與安全方法','Railway RAMS methodology','https://webstore.iec.ch/en/publication/68933','方法出版機構，非本課工程供應關係','Method publisher, without a lesson-project supply claim')],
'maglev':[vendor('鐵道綜合技術研究所','Railway Technical Research Institute','鐵路與超導磁浮研究','Railway and superconducting-maglev research','https://www.rtri.or.jp/rd/maglev/principle.html','研究原理背景，靜態磁壓例非其系統模型','Research-principle context; static magnetic pressure is not its system model'),vendor('東海旅客鐵道','Central Japan Railway Company','鐵路營運與超導磁浮開發','Railway operation and superconducting-maglev development','https://global.jr-central.co.jp/en/','試驗工程背景，不宣稱本課代表真實試驗線','Test-project context; the lesson is not the actual test line')],
}
for g in ('access',):VENDORS[g]=VENDORS['station']
for g in ('crossing','cwr'):VENDORS[g]=VENDORS['control']
VENDORS['suspended']=VENDORS['machinery']

# Representative places are approximate orientation points, not access instructions.
PLACES={
'control':('聖哥達南側示意地點~Gotthard southern reference area','瑞士~Switzerland',46.375,8.967,'Gotthard Base Tunnel Switzerland'),
'crossing':('提莫尼姆道路平交道示意~Timonium Road crossing reference','美國~United States',39.438,-76.628,'Timonium Road light rail crossing Maryland'),
'station':('臺北車站示意地點~Taipei Main Station reference','臺灣~Taiwan',25.0478,121.517,'Taipei Main Station'),
'access':('臺北車站示意地點~Taipei Main Station reference','臺灣~Taiwan',25.0478,121.517,'Taipei Main Station'),
'machinery':('北投機廠示意地點~Beitou depot reference area','臺灣~Taiwan',25.138,121.484,'Beitou Depot Taipei'),
'cwr':('聖哥達南側示意地點~Gotthard southern reference area','瑞士~Switzerland',46.375,8.967,'Gotthard Base Tunnel Switzerland'),
'aps':('波爾多電車示意地點~Bordeaux tram reference area','法國~France',44.841,-0.57,'Bordeaux tramway France'),
'monorail':('東京單軌示意地點~Tokyo monorail reference area','日本~Japan',35.655,139.757,'Tokyo Monorail Hamamatsucho'),
'suspended':('烏帕塔爾示意地點~Wuppertal suspension reference area','德國~Germany',51.257,7.148,'Wuppertal Schwebebahn Germany'),
'maglev':('山梨磁浮示意地點~Yamanashi maglev reference area','日本~Japan',35.579,138.927,'Yamanashi Maglev Exhibition Center'),
}
MARKS={
'control':['聖哥達基線隧道~Gotthard Base Tunnel','倫敦伊莉莎白線~London Elizabeth line'],
'crossing':['洛杉磯佛農大道行人平交道~Los Angeles Vernon Avenue pedestrian crossing','馬里蘭提莫尼姆道路輕軌平交道~Maryland Timonium Road light-rail crossing'],
'station':['臺北車站轉乘系統~Taipei Main Station interchange','倫敦國王十字車站改建~London Kings Cross station redevelopment'],
'access':['臺北車站轉乘系統~Taipei Main Station interchange','倫敦國王十字車站改建~London Kings Cross station redevelopment'],
'machinery':['臺北捷運北投機廠~Taipei Metro Beitou Depot','香港港鐵八鄉機廠~Hong Kong MTR Pat Heung Depot'],
'cwr':['聖哥達基線隧道~Gotthard Base Tunnel','倫敦伊莉莎白線~London Elizabeth line'],
'aps':['波爾多無架空線電車~Bordeaux catenary-free tramway','伊斯坦堡艾米諾努電車~Istanbul Eminonu tramway'],
'monorail':['東京單軌電車~Tokyo Monorail','重慶跨座式單軌~Chongqing straddle monorail'],
'suspended':['烏帕塔爾懸掛鐵路~Wuppertal suspension railway','德勒斯登懸掛鐵路~Dresden suspension railway'],
'maglev':['山梨磁浮試驗線~Yamanashi Maglev Test Line','宮崎磁浮試驗線~Miyazaki Maglev Test Track'],
}
EXTRA={ 'control':['gotthard','elizabeth'],'crossing':[],'station':['main','kings'],'access':['main','kings'],'machinery':['beitou','pat'],'cwr':['gotthard','elizabeth'],'aps':[],'monorail':['hitachi','chongqing'],'suspended':['dresden'],'maglev':['japan'] }
ARCH={}
def A(cid,txt):ARCH[cid]=[x.split('~') for x in txt.split('|')]
A('b368','位置感測~Position sensor|速度規畫~Speed planner|牽引制動~Traction and braking|車輛運動~Vehicle motion|停準量測~Stopping measurement')
A('b369','列車回報~Train reports|狀態彙整~State aggregation|排程資源~Schedule resources|旅客資訊~Passenger information|事件紀錄~Event log')
A('b370','車載位置~Onboard position|無線傳輸~Radio link|地面處理~Wayside processing|資料時效~Data freshness|驗證重播~Verification replay')
A('b371','地標參考~Balise reference|車載版本~Onboard version|地面版本~Trackside version|模式機器~Mode machine|相容證據~Compatibility evidence')
A('b372','占用輸入~Occupancy input|進路需求~Route request|互斥邏輯~Conflict logic|狀態輸出~State output|反例重播~Counterexample replay')
A('b373','隔離電源~Isolated supply|鋼軌回路~Rail circuit|輪對分流~Wheelset shunt|接收判定~Receiver decision|占用證據~Occupancy evidence')
A('b374','輪對通過~Wheelset passage|感測線圈~Sensing coil|事件配對~Event pairing|進出計數~Entry exit count|有效性狀態~Validity state')
A('b375','隔離命令~Isolated command|馬達傳動~Motor transmission|連桿行程~Linkage travel|機械保持~Mechanical retention|位置回授~Position feedback')
A('b376','輪速觀測~Wheel observation|外部地標~External landmark|時間對齊~Time alignment|加權融合~Weighted fusion|不確定度~Uncertainty')
A('b377','到達需求~Arrival demand|區間資源~Section resources|月台停站~Platform dwell|衝突排程~Conflict schedule|擾動重播~Disruption replay')
A('b378','現場事件~Field event|日誌時基~Log timebase|資訊層次~Information hierarchy|人員判讀~Human interpretation|任務證據~Task evidence')
A('b379','危害定義~Hazard definition|原因結構~Cause structure|安全需求~Safety requirement|驗證案例~Verification case|變更證據~Change evidence')
A('b380','列車偵測~Train detection|道路需求~Road demand|警示介面~Warning interface|衝突區域~Conflict area|桌面重播~Desktop replay')
A('b381','停準感測~Stopping sensor|車門狀態~Train door state|月台門狀態~Platform door state|幾何配對~Geometric pairing|交接證據~Handoff evidence')
A('b382','到達人流~Passenger arrivals|通道網路~Passage network|局部存量~Local occupancy|列車交換~Train exchange|模擬證據~Simulation evidence')
A('b383','轉乘到達~Transfer arrivals|樓梯路徑~Stair route|電梯等候~Lift waiting|匯流平台~Merge landing|路徑量測~Route measurement')
A('b384','站外入口~External entrance|無障礙路徑~Accessible route|月台幾何~Platform geometry|車門介面~Vehicle doorway|使用者驗證~User verification')
A('b385','偵測事件~Detection event|通風模式~Ventilation mode|風門路徑~Damper path|煙流量測~Smoke flow measurement|疏散需求~Egress demand')
A('b386','列車通過~Train passage|隧道空氣~Tunnel air|旁通開口~Bypass opening|月台門壓力~Platform door pressure|同步量測~Synchronized measurement')
A('b387','車門出口~Carriage exit|連續步道~Continuous walkway|聯絡通道~Cross passage|緊急照明~Emergency lighting|協助流程~Assistance process')
A('b388','車輛到達~Vehicle arrival|檢修工位~Maintenance bay|備料路徑~Spares route|驗證工單~Verification order|交回證據~Return evidence')
A('b389','車體重量~Body weight|支承反力~Support reaction|同步升降~Synchronized lift|轉向架定位~Bogie alignment|獨立量測~Independent measurement')
A('b390','輪對幾何~Wheelset geometry|夾持基準~Clamping datum|加工接觸~Machining contact|輪廓掃描~Profile scan|壽命履歷~Life history')
A('b391','清洗供水~Wash water supply|噴洗接觸~Spray contact|回收處理~Recovery treatment|乾燥風路~Drying airflow|品質驗證~Quality verification')
A('b392','車輛位能~Vehicle potential energy|路徑阻力~Route resistance|調速耗能~Retarding energy|速度觀測~Speed observation|隔離重播~Isolated replay')
A('b393','貨櫃重心~Container centre of gravity|吊具支承~Spreader support|起升驅動~Hoist drive|擺動位移~Sway displacement|交接定位~Handoff alignment')
A('b394','鋼軌溫度~Rail temperature|拘束條件~Restraint condition|應變感測~Strain sensing|基準校正~Reference calibration|監測證據~Monitoring evidence')
A('b395','輪軌幾何~Wheel rail geometry|槽內排水~Groove drainage|路面需求~Street demand|幾何量測~Geometry survey|整合驗證~Integrated verification')
A('b396','地面饋電~Ground supply|車載儲能~Onboard storage|牽引負載~Traction load|能量量測~Energy measurement|狀態證據~State evidence')
A('b397','車輪載重~Wheel load|導梁彎曲~Beam bending|導梁扭轉~Beam torsion|溫度變形~Thermal movement|幾何驗證~Geometry verification')
A('b398','懸掛載重~Suspended load|轉轍梁位~Switch beam position|連桿驅動~Linkage drive|位置確認~Position confirmation|隔離試驗~Isolated testing')
A('b399','測量基準~Survey datum|導梁形狀~Guideway geometry|磁力介面~Magnetic interface|動態激振~Dynamic excitation|精度證據~Precision evidence')
A('b400','系統需求~System requirements|介面契約~Interface contract|測試環境~Test environment|整合證據~Integration evidence|變更回歸~Change regression')

checks=[]
for cid,c in sorted(COURSES.items()):
 t=TARGETS[cid];fz,fe=split(c['focus']);g=c['group'];rows=c['units'];titles=[split(r['title']) for r in rows]
 units=[unit(row,i) for i,row in enumerate(rows,1)]
 sourcekeys=GROUPS[g]
 sources=[{k:v for k,v in SOURCES[s].items() if k not in ('year','event')} for s in sourcekeys]
 sources += [PROJECTS[k] for k in EXTRA[g]]
 if g=='aps': sources += [{k:v for k,v in SOURCES[s].items() if k not in ('year','event')} for s in ('rams-2002','rams-2025')]
 if cid=='b374': sources[-1]={k:v for k,v in SOURCES['frauscher-2012'].items() if k not in ('year','event')}
 if cid=='b390': sources[-1]={k:v for k,v in SOURCES['lathe'].items() if k not in ('year','event')}
 if g=='maglev': sources.append({k:v for k,v in SOURCES['rtri-maglev'].items() if k not in ('year','event')})
 if cid=='b395':
  sources += [{k:v for k,v in SOURCES[s].items() if k not in ('year','event')} for s in ('aps-overview','aps-2021')]
 if g=='cwr':
  sources[-1]={k:v for k,v in SOURCES['rams-2025'].items() if k not in ('year','event')}
 timeline=[dict(year=SOURCES[k]['year'],event=SOURCES[k]['event']) for k in sourcekeys]
 timeline.sort(key=lambda x:int(x['year']))
 summary=pair(f'本課聚焦{fz}。從{titles[0][0]}建立物理或資訊邊界，接著把{titles[3][0]}與{titles[6][0]}連成可驗證的介面，最後以{titles[9][0]}整理證據。學徒逐一完成機制推導、數值算例、失效辨識及參數實驗，所有練習限定在離線模型或隔離教具，保留假設與量測的不確定度。',f'This course studies {fe.lower()}. Start with {titles[0][1].lower()} to define physical or information boundaries, connect {titles[3][1].lower()} with {titles[6][1].lower()} as verifiable interfaces, and organize evidence through {titles[9][1].lower()}. Each unit develops a mechanism, numerical example, failure diagnosis and parameter experiment in an offline model or isolated teaching rig, retaining assumptions and measurement uncertainty.')
 eventsz='；'.join(x['year']+' 年'+split(x['event'])[0] for x in timeline); eventse=' '.join(x['year']+': '+split(x['event'])[1] for x in timeline)
 history=pair(f'本課以可查核的工程與方法出版歷程建立背景：{eventsz}這些日期分別是工程事件、指南重印或標準研究出版，並非宣稱本課系統在該年問世。對{fz}而言，歷史脈絡的價值是理解需求如何從單一設備擴展到跨介面證據。本課再用{titles[1][0]}及{titles[8][0]}連結這些方法；代表工程僅提供觀察方向，假想參數不冒充現場資料，歷史版規範也不自動等於當地現行要求。',f'The background uses checkable project events and methodological publication history. {eventse} These dates identify project events, guide reprints, or standards and research publications, rather than claiming that the lesson system first appeared then. For {fe.lower()}, the useful historical perspective is the expansion from individual equipment to evidence across interfaces. The course connects that perspective through {titles[1][1].lower()} and {titles[8][1].lower()}. Reference projects guide observation only: hypothetical parameters are not field data, and historical editions do not automatically establish current local requirements.')
 m0=MODELS[rows[0]['key']]; m1=MODELS[rows[1]['key']];s=scenario(m0)
 az,ae=split(model_text(m0));dz,de=split(model_text(m1));cz,ce=split(rows[0]['context'])
 example=pair(f'原創整合工作單，所有輸入均為教學假設而非代表工程實測：先研究{titles[0][0]}。{az}敏感度只改 {s["symbol"]}={fmt(s["base"])} 至 {fmt(s["changed"])} {s["inputUnit"]}，輸出變為 {fmt(s["result"])} {s["outputUnit"]}；離散計數採整數變化。再獨立研究{titles[1][0]}：{dz}兩個結果不能因同一課程就任意相加，必須先確認單位、因果順序及共同邊界。{cz}最後提出一項量測能區分模型假設失效與儀器偏差，將輸入表、重算結果和適用限制一併交付。',f'Original integrated worksheet; every input is a teaching assumption rather than a measurement from a reference project. First investigate {titles[0][1].lower()}. {ae} For sensitivity, change only {s["symbol"]}={fmt(s["base"])} to {fmt(s["changed"])} {s["inputUnit"]}; the output becomes {fmt(s["result"])} {s["outputUnit"]}. Discrete counts use whole-number steps. Independently investigate {titles[1][1].lower()}: {de} Results cannot be added merely because they belong to the same course: check units, causal sequence and shared boundaries first. {ce} Propose one measurement distinguishing a failed model assumption from instrument bias, and deliver the input table, recomputed results and applicability limits together.')
 facts=[]
 for row in rows[:6]:
  m=MODELS[row['key']];q=m['quantities'][0];rz,re_=split(row['title']);qz,qe=split(q[3])
  facts.append(pair(f'教學假設：{rz}採 {q[0]}={fmt(q[1])} {q[2]}；本課公式結果 {fmt(calc(m))} {m["result_unit"]}，非現場額定值。',f'Teaching assumption for {re_.lower()}: {q[0]}={fmt(q[1])} {q[2]}; this model gives {fmt(calc(m))} {m["result_unit"]}, not a field rating.'))
 place=PLACES['aps'] if cid=='b395' else PLACES[g]
 marks=MARKS['aps'] if cid=='b395' else MARKS[g]
 family='control' if int(cid[1:])<=380 or cid=='b400' else 'station' if int(cid[1:])<=387 else 'depot' if int(cid[1:])<=393 else 'power' if cid=='b396' else 'track'
 d=dict(id=cid,title=t['title']+'~'+t['titleEn'],discipline=t['discipline'],family=family,focus=c['focus'],summary=summary,history=history,example=example,units=units,facts=facts,timeline=timeline,codes=CODES[g],landmarks=marks,place=dict(name=place[0],country=place[1],lat=place[2],lng=place[3],query=place[4]),sources=sources,vendors=VENDORS[g],related=['b'+str(367 if cid=='b368' else int(cid[1:])-1),'b'+str(301 if cid=='b400' else int(cid[1:])+1)],architectureNodes=ARCH[cid],architectureEdges=[[0,1],[1,2],[2,3],[3,4],[4,1]])
 (ROOT/'inputs').mkdir(exist_ok=True)
 (ROOT/'inputs'/f'{cid}.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
 for n,row in enumerate(rows,1):
  m=MODELS[row['key']]; checks.append(dict(course=cid,unit=n,model=row['key'],expression=m['expression'],quantities=m['quantities'],result=calc(m),sensitivity=scenario(m)))
(HERE/'numeric_checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
print(f'Emitted {len(COURSES)} courses / {len(checks)} units; numerical checks saved.')
