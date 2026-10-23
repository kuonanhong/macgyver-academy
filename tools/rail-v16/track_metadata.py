"""Primary-source routing and distinct system architecture for the track range.
Dates refer to named publications or explicitly identified project events.
"""
def add(key,z,e,p,url,scopez,scopee):
 SOURCES[key]=(z,e,p,url,scopez,scopee)
add('betuwe-history','荷蘭基礎建設基金貝圖威歷史','Dutch Infrastructure Fund Betuweroute history','Ministry of Finance, Netherlands','https://www.rijksfinancien.nl/memorie-van-toelichting/2020/OWB/A','第十七點零二節的實際開通、港線改造與專案治理年代。','Section 17.02 dates actual opening, port-line conversion and project-governance milestones.')
add('plasser-history','普拉塞企業技術歷史','Plasser & Theurer history','Plasser & Theurer','https://www.plassertheurer.com/en/company/history','一九五三年企業創立作為機械化維護產業背景；不等於所有搗固技術的發明日期。','The 1953 company foundation is industry context, not the invention date of every tamping technique.')
add('energy','能源子系統互通規範','Energy TSI','European Union Agency for Railways','https://www.era.europa.eu/domains/technical-specifications-interoperability/energy-tsi_en','牽引供電固定設施與受流介面的規範入口及歷次修訂。','Regulatory entry point and amendments for fixed traction-energy installations and current-collection interfaces.')
add('energy-guide','能源互通規範應用指南','Guide for the application of the ENE TSI, 2023','European Union Agency for Railways','https://www.era.europa.eu/system/files/2023-12/ENE_TSI_Guide.pdf','二零二三年指南的適用範圍與條文解讀背景，不複製條文。','Scope and interpretation context of the 2023 guide without reproducing clauses.')
add('storage2010','交通再生煞車能量回收研究','TCRP Web-Only Document 51: Guiding the Selection and Application of Wayside Energy Storage Technologies for Rail Transit and Electric Utilities','Transportation Research Board','https://www.nationalacademies.org/read/22911/chapter/1','二零一零年公共運輸再生能量儲存研究背景。','Background to the 2010 research on transit regenerative-energy storage.')
add('wet2012','濕潤輪軌黏著影響因素研究','Influential Factors on Adhesion between Wheel and Rail under Wet Conditions','Railway Technical Research Institute','https://www.jstage.jst.go.jp/article/rtriqr/53/4/53_223/_article/-char/en','二零一二年原始研究，說明水膜與表面條件需分別驗證。','Original 2012 research motivating separate verification of water-film and surface conditions.')
add('wet2014','濕潤條件輪軌黏著機制','Wheel-rail adhesion mechanisms under wet conditions','Railway Technical Research Institute','https://www.rtri.or.jp/rd/division/rd50/rd5030/rd50300111.html','研究所技術解說與二零一四年研究參考；算例摩擦值為另設假設。','Institute technical explanation and 2014 research references; example coefficients are independent assumptions.')
add('tor2017','軌頂摩擦調節研究計畫','Determination of TOR lubricity','University of Nevada, Las Vegas','https://www.unlv.edu/railteam/research/determination-of-tor-lubricity','研究計畫期間二零一七至二零一九年，作為摩擦調節與量測背景。','The 2017–2019 project supplies context for friction management and measurement.')
add('rock2019','落石偵測原始研究','Monitoring and early warning method for a rockfall along railways based on vibration signal characteristics','Scientific Reports / research authors','https://www.nature.com/articles/s41598-019-43146-1','二零一九年原始研究用於比較偵測證據，不宣稱軌道系統已獲安全認證。','Original 2019 research for comparing detection evidence, without claiming railway safety certification.')
add('sbb-monitor','瑞士鐵路列車監測設備','SBB train-monitoring measuring systems','Swiss Federal Railways','https://company.sbb.ch/en/railway-development/services-rus/railway-environment/train-monitoring-systems/measuring-systems.html','營運者公開的監測設備分類，並非本課合成分類器的效能背書。','Operator-published monitoring-system categories, not endorsement of the synthetic classifier.')
add('ccs-guide','號誌互通規範應用指南','Guide for the application of the CCS TSI 2023/1695','European Union Agency for Railways','https://www.era.europa.eu/sites/default/files/2024-12/ccs-tsi-2023-application-guide.pdf','二零二四年六月十七日第一版指南的解讀背景。','Interpretation context for the first guide edition dated 17 June 2024.')
add('ccs2026','號誌互通規範修訂生效公告','Amendment to the CCS TSI Enters into Force','European Union Agency for Railways','https://www.era.europa.eu/content/amendment-ccs-tsi-enters-force','二零二六年五月五日修訂生效的官方公告。','Official notice of the amendment entering force on 5 May 2026.')

def source_keys(n):
 if n==335:return ['betuwe-history','tsi','brake']
 if n==340:return ['cwr','tsi','fra']
 if n in (341,342):return ['weld','ultra','cwr','tsi']
 if n==343:return ['tamp','plasser-history','trans','fra']
 if n==344:return ['clean','trans','tsi','fra']
 if n in (345,350,351,352):return ['fast','trans','tsi','fra']
 if n==349:return ['ultra','rtri','fra']
 if n==355:return ['cold','trans','fra']
 if n==359:return ['rock2019','sbb-monitor','tsi','fra']
 if 360<=n<=364:return ['energy','energy-guide','ole','elsafe']
 if n==365:return ['wet2012','wet2014','tor2017','fra']
 if n==366:return ['storage1979','storage2010','storage','elsafe']
 if n==367:return ['brake','ccs','ccs-guide','ccs2026']
 return ['trans','tsi','fra']

def event(year,z,e):return {'year':year,'event':z+'~'+e}
E_TRANS=event('2006-10','運輸研究委員會發布軌道過渡段比較研究摘要。','TRB published its comparative research digest on track transitions.')
E_TSI=event('2014-11-18','歐盟公布整合基礎設施互通規範第一二九九號法規。','The EU issued Regulation 1299/2014 for the infrastructure interoperability specification.')
E_FRA=event('2026-03-04','美國鐵路管理局發布新版軌道與構造物檢查手冊。','FRA issued its updated Track and Structures Compliance Manual.')
E_CWR=event('2009-08-25','美國鐵路管理局發布連續焊接鋼軌規則修訂。','FRA published its continuous welded rail final rule amendment.')

def course_timeline(n):
 if n==335:return [event('2007-06-16','貝圖威路線的高速公路平行區段正式啟用。','The Betuweroute A15 section officially entered service.'),event('2009-12-13','港區貨運線完成歐洲列車控制與二十五千伏系統投入使用。','The Havenspoorlijn brought ERTMS and 25 kV systems into service.'),event('2011-04-28','荷蘭議會結束貝圖威計畫的大型專案治理資格。','The Dutch parliament ended the Betuweroute major-project governance status.')]
 if n==340:return [E_CWR,E_TSI,E_FRA]
 if n in (341,342):return [E_CWR,E_TSI,event('2024-03','國際標準組織發布在役鋼軌超音波檢測第一部分。','ISO published Part 1 of its ultrasonic testing standard for installed rails.')]
 if n==343:return [event('1953','普拉塞公司創立，作為鐵路機械化維護的產業歷史背景。','Plasser & Theurer was founded, providing industry context for mechanized railway maintenance.'),E_TRANS,E_FRA]
 if n==349:return [event('2020','日本鐵道總研公布空氣超音波偵測鋼軌開口的研究成果。','RTRI reported research on detecting rail openings using aerial ultrasound.'),event('2024-03','國際標準組織發布在役鋼軌超音波檢測第一部分。','ISO published Part 1 of its ultrasonic testing standard for installed rails.'),E_FRA]
 if n==355:return [event('1969-06','美國寒區研究出版寒冷地區構造物基礎技術報告。','US cold-regions research published Foundations of Structures in Cold Regions.'),E_TRANS,E_FRA]
 if n==359:return [E_TSI,event('2019','科學報告期刊出版落石監測原始研究，作為偵測方法比較。','Scientific Reports published original rockfall-monitoring research for detection-method comparison.'),E_FRA]
 if 360<=n<=364:return [event('2014-11-18','歐盟公布能源子系統互通規範第一三零一號法規。','The EU issued Regulation 1301/2014 for energy-subsystem interoperability.'),event('2019-05-16','歐盟第七七六號修訂更新能源等鐵路互通規範。','EU Regulation 2019/776 amended energy and other railway interoperability specifications.'),event('2023-12-20','歐洲鐵路署發布二零二三版能源互通規範應用指南。','ERA issued the 2023 application guide for the Energy TSI.')]
 if n==365:return [event('2012-11-01','鐵道總研期刊出版濕潤輪軌黏著影響因素原始研究。','Quarterly Report of RTRI published original research on wet wheel-rail adhesion factors.'),event('2014','鐵道總研濕潤黏著技術頁引用同年研究作為機制說明。','RTRI wet-adhesion technical guidance cites research from this year to explain mechanisms.'),event('2017-01-01','內華達大學軌頂摩擦調節研究計畫開始，預定持續至二零一九年底。','The UNLV top-of-rail lubricity project began, with a scheduled end in December 2019.')]
 if n==366:return [event('1979-02-01','美國鐵路管理局出版軌旁儲能系統研究第二卷。','FRA published Volume 2 of its Wayside Energy Storage Study.'),event('2010','運輸研究委員會出版公共運輸煞車能量儲存研究文件。','TRB published research documentation on storing transit braking energy.'),event('2015-06-01','聯邦運輸署出版華盛頓都會區軌旁儲能展示報告。','FTA published the WMATA wayside energy-storage demonstration report.')]
 if n==367:return [event('2023-08-10','歐盟公布重編控制命令與號誌互通規範第一六九五號法規。','The EU issued recast CCS interoperability Regulation 2023/1695.'),event('2024-06-17','歐洲鐵路署出版新版號誌互通規範應用指南第一版。','ERA published version 1 of the recast CCS TSI application guide.'),event('2026-05-05','歐洲鐵路署公告號誌互通規範修訂正式生效。','ERA announced the CCS TSI amendment entering into force.')]
 return [E_TRANS,E_TSI,E_FRA]

def course_codes(n):
 base=['歐洲基礎設施互通技術規範：依地區與適用版本核對。~European Infrastructure TSI: verify jurisdiction and applicable edition.','美國聯邦法規第四十九篇第二百十三部分：軌道比較閱讀。~US 49 CFR Part 213: comparative reading on track requirements.']
 if n==340:base[1]='美國連續焊軌最終規則及現行四十九篇法規：分清歷史與現行要求。~US CWR final rule and current 49 CFR rules: distinguish historical and current requirements.'
 if n in (341,342,349):base[1]='ISO 5735-1:2024：在役鋼軌連續超音波檢測範圍，非焊廠生產驗收規範。~ISO 5735-1:2024: continuous testing of installed rails, not a production-plant weld acceptance code.'
 if n in (354,355,356,358):base[1]='軌道過渡段設計研究摘要第七十九號：比較方法指引而非通用允收門檻。~Design of Track Transitions, Digest 79: comparative methodological guidance, not universal acceptance limits.'
 if 360<=n<=364:return ['歐洲能源子系統互通技術規範：確認當地適用性與完整版本。~European Energy TSI: confirm local applicability and complete applicable edition.','歐洲鐵路署二零二三年能源互通規範應用指南：供解讀及界面比較。~ERA 2023 Energy TSI application guide: interpretation and interface comparison.']
 if n==365:return ['美國軌道與構造物檢查手冊：維護與檢查制度背景。~FRA Track and Structures Compliance Manual: maintenance and inspection framework.','鐵道總研濕潤輪軌黏著技術解說：研究指引而非施藥處方。~RTRI wet wheel-rail adhesion technical guidance: research guidance, not an application prescription.']
 if n==366:return ['華盛頓軌旁儲能展示報告：系統驗證研究指引。~WMATA Wayside Energy Storage Demonstration Report: system-verification research guidance.','英國鐵路網電氣安全指引：隔離與授權制度閱讀。~Network Rail Electrical Safety guidance: reading on isolation and authorization.']
 if n==367:return ['歐洲控制命令與號誌互通規範及適用修訂：核對所需基線。~European CCS TSI and applicable amendments: verify the required baseline.','歐洲鐵路署號誌互通規範應用指南：離線案例的範圍背景。~ERA CCS TSI application guide: scope context for offline examples.']
 return base

ARCH={
335:'港區裝卸~Port handling|貨列編組~Freight consist|路線牽引~Route traction|閉塞容量~Block capacity|港區周轉~Port turnover',
336:'共同里程~Shared chainage|平面曲率~Plan curvature|縱坡高程~Grade and elevation|過渡加速度~Transition acceleration|測量閉合~Survey closure',
337:'速度分布~Speed distribution|曲率半徑~Curve radius|軌道超高~Track cant|不足與過剩~Deficiency and excess|順坡變化率~Ramp rates',
338:'土層支承~Ground support|基礎混凝土~Foundation concrete|板底界面~Slab interface|排水熱變形~Drainage and thermal movement|試體品質~Specimen quality',
339:'控制網基準~Control datum|軌道板定位~Slab placement|精調支點~Adjustment points|灌漿層~Grout layer|相鄰接縫~Adjacent joints',
340:'軌溫量測~Rail temperature|自由伸縮~Free expansion|縱向約束~Longitudinal restraint|中性狀態~Neutral state|軌道穩定~Track stability',
341:'鋼軌端面~Rail ends|電阻加熱~Resistance heating|頂鍛接合~Upset joining|冷卻幾何~Cooling geometry|無損檢測~Nondestructive testing',
342:'焊接材料~Welding material|熱量收支~Heat balance|接頭凝固~Joint solidification|幾何整修~Geometry finishing|品質取證~Quality evidence',
343:'軌道幾何~Track geometry|搗固作用~Tamping action|道碴接觸~Ballast contact|支承剛度~Support stiffness|整正復測~Correction survey',
344:'道碴挖取~Ballast excavation|粒徑清篩~Particle screening|補碴輸送~Ballast supply|排水孔隙~Drainage voids|復舊幾何~Restored geometry',
345:'鋼軌載入~Rail loading|彈條扣壓~Clip force|墊板彈性~Pad elasticity|錨固支承~Anchored support|縱向阻力~Longitudinal resistance',
346:'輪軌激振~Wheel-rail excitation|浮置板質量~Floating mass|隔振支承~Isolation support|基礎反應~Foundation response|位移行程~Displacement travel',
347:'軌面波形~Rail profile|接觸激振~Contact excitation|研磨去除~Grinding removal|熱與表面~Heat and surface|復測頻譜~Post-work spectrum',
348:'里程定位~Chainage position|幾何感測~Geometry sensing|濾波頻寬~Filter bandwidth|缺陷波形~Defect waveform|獨立複測~Independent survey',
349:'超音波源~Ultrasonic source|耦合路徑~Coupling path|鋼軌反射~Rail reflection|回波時間~Echo timing|缺陷證據~Flaw evidence',
350:'軌枕幾何~Sleeper geometry|預力筋~Prestress tendon|彎曲載入~Bending load|裂縫變形~Cracking and deformation|耐久評估~Durability assessment',
351:'道岔中心線~Turnout centerline|尖軌構件~Switch rails|轍叉構件~Crossing components|軌距配合~Gauge compatibility|組裝檢驗~Assembly inspection',
352:'命令輸入~Command input|轉轍驅動~Point drive|可動心軌~Movable crossing|鎖閉回讀~Lock feedback|保守狀態~Conservative state',
353:'降雪熱負載~Snow thermal load|加熱元件~Heating element|傳熱接觸~Thermal contact|溫度回授~Temperature feedback|結冰監測~Ice monitoring',
354:'路基土層~Earth support|漸變支承~Graded support|橋台邊界~Abutment boundary|排水網路~Drainage network|沉陷幾何~Settlement geometry',
355:'地表熱通量~Surface heat flux|保溫與雪覆~Insulation and snow|凍土冰層~Frozen ice-bearing ground|活動融層~Active thaw layer|沉陷監測~Settlement monitoring',
356:'重載輪重~Heavy wheel load|鋼軌彎曲~Rail bending|離散扣件~Discrete fastenings|連續支承~Distributed support|撓度辨識~Deflection identification',
357:'車體與輪對~Body and wheelset|懸吊阻尼~Suspension damping|輪軌接觸~Wheel contact|軌道支承~Track support|時域驗證~Time-domain verification',
358:'橋梁溫度~Bridge temperature|橋梁支承~Bridge bearings|縱向扣件~Longitudinal fastenings|連續鋼軌~Continuous rails|橋端位移~Bridge-end movement',
359:'環境異物~Environmental obstruction|感測視場~Sensor field|事件判定~Event decision|警報通訊~Alarm communication|防護回讀~Protection feedback',
360:'支柱吊點~Supports and droppers|張力補償~Tension compensation|接觸導線~Contact conductor|受電弓力~Pantograph force|波動幾何~Wave geometry',
361:'弓線接觸~Pantograph contact|力與加速度~Force and acceleration|離線電弧~Contact loss and arcs|同步量測~Synchronized sensing|不確定度~Uncertainty',
362:'公共電網~Public grid|變壓整流~Transformer rectifier|牽引母線~Traction bus|饋線負載~Feeder load|保護量測~Protection measurement',
363:'直流饋線~DC feeder|第三導軌~Third rail|集電靴群~Collector shoes|車載負載~Onboard load|鋼軌回流~Rail return',
364:'列車回流~Train return|鋼軌接續~Rail bonds|軌地導納~Rail-earth conductance|收集路徑~Collection path|地電位參考~Earth-potential reference',
365:'輪軌法向力~Normal contact load|切向蠕滑~Tangential creepage|摩擦材料~Friction material|磨耗熱量~Wear and heat|黏著驗證~Adhesion verification',
366:'列車再生~Train regeneration|雙向轉換~Bidirectional conversion|儲能介質~Storage medium|荷電狀態~State of charge|電網削峰~Grid peak shaving',
367:'速度與位置~Speed and location|移動許可~Movement authority|制動包絡~Braking envelope|狀態監督~State supervision|保守回應~Conservative response'}
def architecture(n):return [x.split('~') for x in ARCH[n].split('|')]
def vendor(z,e,b,be,url,r,re):return dict(name=z,nameEn=e,business=b,businessEn=be,url=url,role=r,roleEn=re,security=None)
def power_vendors():return [vendor('西門子交通','Siemens Mobility','交流與直流鐵路牽引供電設備。','AC and DC railway traction-power equipment.','https://www.mobility.siemens.com/global/en/portfolio/rail-infrastructure/electrification.html','供電設備範圍比較，不宣稱承攬本課工程。','Supply-equipment scope comparison without claiming a contract for this course.'),vendor('日立能源','Hitachi Energy','鐵路變壓器與電氣化技術。','Railway transformers and electrification technology.','https://www.hitachienergy.com/us/en/markets/transportation/rail','電力設備延伸閱讀，不把產品額定值當教材輸入。','Power-equipment further reading without treating ratings as teaching inputs.')]
def control_vendors():return [vendor('西門子交通','Siemens Mobility','歐洲列車控制與軌旁、車載設備。','ETCS and trackside/onboard train-control equipment.','https://www.mobility.siemens.com/global/en/portfolio/rail-infrastructure/mainline/european-train-control-system.html','列車控制架構的產品範圍比較，不宣稱安全認證合作。','Product-scope comparison for train-control architecture without a certification partnership.'),vendor('日立軌道','Hitachi Rail','幹線鐵路控制與監督系統。','Mainline railway control and supervision systems.','https://www.hitachirail.com/products-and-solutions/mainline-rail-control-supervision/','號誌系統延伸閱讀，不宣稱參與課程假想模型。','Signalling-system further reading without claimed involvement in the assumed course models.')]
def course_landmarks(n):
 if n==335:return ['荷蘭貝圖威貨運鐵路~Betuweroute freight railway','印度西部專用貨運走廊~Western Dedicated Freight Corridor India']
 if n==355:return ['中國青藏鐵路~Qinghai Tibet Railway','俄羅斯貝阿鐵路~Baikal Amur Mainline']
 if n in (363,364):return ['倫敦地下鐵~London Underground','台北捷運~Taipei Metro']
 if n==366:return ['華盛頓都會區軌旁儲能展示工程~WMATA Wayside Energy Storage Demonstration','費城大眾運輸軌旁儲能工程~Philadelphia SEPTA Wayside Energy Storage']
 return ['台灣高速鐵路工程~Taiwan High Speed Rail','東海道新幹線工程~Tokaido Shinkansen']
def architecture_edges(n):
 # These are conceptual dependencies between named engineering subsystems.
 if n in (336,337,361,367):return [[0,2],[1,2],[2,3],[3,4],[4,2]]
 if n in (345,346,354,356,357,358,360):return [[0,1],[1,2],[2,3],[3,4],[4,1]]
 if n in (362,363,364,366):return [[0,1],[1,2],[2,3],[3,4],[4,0]]
 return [[0,1],[1,2],[2,3],[3,4],[4,1]]
