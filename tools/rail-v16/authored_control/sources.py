"""Verified primary-source bibliography. Contents are linked, not reproduced."""
SOURCES={}
def S(key,title,en,publisher,url,year,event,scope):
    SOURCES[key]=dict(key=key,title=title,titleEn=en,publisher=publisher,url=url,sourceType='primary',
                      scope=scope.split('~')[0],scopeEn=scope.split('~')[1],year=str(year),event=event)
S('rams-2002','鐵路可靠度安全方法早期版','Earlier railway RAMS specification','IEC','https://webstore.iec.ch/en/publication/6747',2002,
  '鐵路可靠度與安全方法早期版發布。~An early railway RAMS specification was published.',
  '支持該版標準的出版年代與主題；不提供本課數值或最新適用性判定。~Supports publication year and topic, not exercise values or a claim of current applicability.')
S('rams-2025','鐵路可靠度安全方法分冊','Railway RAMS specification part one','IEC','https://webstore.iec.ch/en/publication/68933',2025,
  '鐵路可靠度與安全方法第一分冊發布。~A new first part of railway RAMS was published.',
  '支持方法分冊的出版年代與範圍；不複製條文或宣稱教材為合規論證。~Supports edition year and scope; clauses are not reproduced and the lessons do not establish compliance.')
S('era-ccs','歐洲列控與自動駕駛技術規則','European control and automation technical regulation','European Commission / EUR-Lex','https://eur-lex.europa.eu/legal-content/en/TXT/?uri=oj%3AJOL_2023_222_R_0003',2023,
  '歐盟列控技術規則二零二三號一六九五發布。~European Commission Regulation twenty-twenty-three slash sixteen-ninety-five was adopted.',
  '支持二零二三年列控技術規則發布與範圍；不把簡化模型當成正式制動曲線。~Supports publication and scope of the twenty-twenty-three control regulation; simplified models are not operational braking curves.')
S('iso-risk','機械風險評估方法','Machinery risk-assessment methodology','ISO','https://www.iso.org/cms/live/live/en/sites/isoorg/contents/data/standard/05/15/51528.html?browse=tc',2010,
  '機械風險評估方法的該版標準發布。~This edition of machinery risk-assessment guidance was published.',
  '支持機械風險方法與出版年代；不提供特定設備額定能力或作業許可。~Supports machinery-risk methodology and edition year, not equipment ratings or work authorization.')
S('iso-control','機械安全控制設計方法','Machinery safety-related control design','ISO','https://www.iso.org/standard/73481.html',2023,
  '機械安全控制設計方法更新版發布。~An updated machinery safety-control design edition was published.',
  '支持安全相關控制設計的標準範圍；本課沒有宣稱達成特定性能等級。~Supports the scope of safety-related control design; no particular performance level is claimed.')
S('iso-quality','品質管理方法歷史版','Historical quality-management edition','ISO','https://www.iso.org/standard/62085.html?iframeView=true',2015,
  '品質管理方法的二零一五版發布。~The twenty-fifteen edition of quality-management requirements was published.',
  '僅支持歷史版出版與品質管理主題，不把歷史版宣稱為所有地區最新要求。~Supports historical edition and quality-management topic, without claiming universal current applicability.')
S('fta-emergency','軌道運輸緊急整備指南','Rail-transit emergency-preparedness guide','Federal Transit Administration','https://www.transit.dot.gov/sites/fta.dot.gov/files/docs/repg_rts.pdf',1991,
  '一九八五年緊急整備指南於該年重印。~The rail-transit emergency guide originally published in nineteen eighty-five was reprinted.',
  '提供緊急整備的歷史方法脈絡；本課數值不是指南的法定疏散限值。~Historical emergency-preparedness context; exercise values are not statutory egress limits from the guide.')
S('passenger-flow','地下車站與月台旅客流研究','Passenger flow in stations and platforms','Mineta Transportation Institute / USDOT repository','https://rosap.ntl.bts.gov/view/dot/28885',2015,
  '地下車站旅客流研究報告於該年出版。~A study of underground-station passenger flow was published.',
  '支持旅客流研究的背景與方法方向；所有流率及步速均為原創教學假設。~Supports passenger-flow research context; all flow rates and walking speeds are original assumptions.')
S('rb-station','鐵道車站概念設計指引','Rail-station conceptual-design guidance','交通部鐵道局','https://www.rb.gov.tw/zh-TW/main/main_71/main_80/main_115/20250916_113536/',2025,
  '臺灣鐵道車站概念設計指引函頒。~Taiwan issued guidance for conceptual railway-station design.',
  '支持車站整合設計的官方文件與函頒年代，不宣稱本課簡化算例已符合其全部要求。~Supports official station-design guidance and issue year, without claiming complete compliance by simplified exercises.')
S('access-ada','運輸設施無障礙官方標準','Official transportation accessibility standards','US Access Board / US DOT','https://www.access-board.gov/ada/',2006,
  '美國運輸部採用運輸設施無障礙標準。~The United States Department of Transportation adopted accessibility standards for transportation facilities.',
  '支持無障礙路徑與月台車輛介面範圍；幾何算例非條文限值或跨國合規判定。~Supports accessible-route and platform-interface scope; geometry exercises are not code limits or cross-national compliance decisions.')
S('fra-access','城際高速鐵路月台無障礙指引','Accessible intercity and high-speed platforms','Federal Railroad Administration','https://railroads.dot.gov/elibrary/americans-disabilities-act-1990-ada-intercity-and-high-speed-passenger-rail-platform',2022,
  '城際與高速鐵路月台無障礙指引發布。~Guidance for accessible intercity and high-speed platforms was released.',
  '支持月台與車輛協調的官方指引與發布年代；不提供本課假想誤差預算。~Supports official platform-vehicle guidance and year, not the hypothetical error budgets used here.')
S('crossing-handbook','公路鐵路平交道手冊第三版','Highway–rail crossing handbook third edition','Federal Highway Administration','https://highways.dot.gov/safety/hsip/xings/highway-rail-crossing-handbook-third-edition',2019,
  '公路鐵路平交道手冊第三版出版。~The third highway–rail crossing handbook edition was published.',
  '支持道路與鐵路界面安全的手冊脈絡；教學時序不可直接作為現場控制設定。~Supports road–rail interface context; teaching timings are not field control settings.')
S('crossing-human','平交道人因設計研究','Human factors at highway–rail intersections','Federal Railroad Administration','https://railroads.dot.gov/elibrary/human-factors-guidance-intelligent-transportation-systems-highway-rail-intersection',2006,
  '公路鐵路交會處的人因指引報告出版。~Human-factors guidance for highway–rail intersections was published.',
  '支持人因與警示介面研究背景；不把假想反應時間宣稱為普遍人員能力。~Supports human-factors and warning-interface context, not universal human-response times.')
S('frauscher','輪軸感測與計數產品資訊','Wheel sensing and axle-counting information','Frauscher','https://www.frauscher.com/en_us/products/axle-counters',2012,
  '輪偵測及計軸方法已有公開技術交流。~Wheel detection and axle counting had public technical presentations.',
  '僅支持廠商產品角色與計軸原理背景；不提供重置程序或現場閾值。~Supports supplier role and axle-counting context only, without reset procedures or field thresholds.')
S('frauscher-2012','輪偵測與計軸公開簡報','Public wheel-detection and axle-counting presentation','UNECE / Frauscher','https://unece.org/DAM/trans/main/temtermp/2012_2nd_Expert_Group_Meeting_Ankara/TEM_March_2012_frauscher_showcase_ankara.pdf',2012,
  '輪偵測及計軸技術於國際會議交流。~Wheel-detection and axle-counting techniques were presented internationally.',
  '支持二零一二年公開技術交流的日期與主題；不重製投影片。~Supports date and topic of a public technical presentation; slides are not reproduced.')
S('lathe','在軌輪對鏇削設備產品','Underfloor wheelset-machining equipment','Hegenscheidt','https://www.hegenscheidt.com/en/machine-portfolio/machines-for-wheelset-machining/underfloor-wheelset-lathes/',2010,
  '機械風險方法提供維修設備設計脈絡。~Machinery risk methods provide context for maintenance-equipment design.',
  '僅支持廠商提供輪對加工設備的角色，不把示例刀速或輪徑當成產品參數。~Supports the supplier role in wheelset machining, not assumed speeds or diameters as product specifications.')
S('cwr-2008','長焊鋼軌應力超音波研究','Ultrasonic investigation of longitudinal rail stress','Federal Railroad Administration','https://railroads.dot.gov/sites/fra.dot.gov/files/fra_net/2086/rr0805.pdf',2008,
  '長焊鋼軌縱向應力監測研究報告出版。~Research on monitoring longitudinal rail stress was published.',
  '支持應力量測方法的研究歷史；彈性熱應力算例是本課自行設定。~Supports the research history of stress measurement; elastic thermal-stress examples are original.')
S('cwr-2010','鋼軌應力自動量測研究','Automated measurement of rail stress','Federal Railroad Administration','https://rosap.ntl.bts.gov/view/dot/40238',2010,
  '連續焊軌應力自動量測報告出版。~An automated continuous-welded-rail stress measurement report was published.',
  '支持自動量測與無應力溫度研究脈絡，不提供現場放散程序。~Supports automated measurement and neutral-temperature context, not field destressing procedures.')
S('cwr-2021','長焊鋼軌計畫方法指引','Guidance for continuous-welded-rail plans','Federal Railroad Administration','https://railroads.dot.gov/sites/fra.dot.gov/files/2021-08/FRA%20CWR%20Generic%20Plan%20-%20Effective_July%202021%5B67%5D.pdf',2021,
  '長焊鋼軌計畫方法指引於該年更新。~Guidance for continuous-welded-rail plans was updated that year.',
  '支持計畫方法指引更新年代；本課模型不是核准計畫。~Supports the guidance update year; this model is not an approved plan.')
S('aps-2018','伊斯坦堡地面供電合約公告','Istanbul ground-level-power announcement','Alstom','https://www.alstom.com/press-releases-news/2018/4/alstom-to-supply-aps-ground-level-power-solution-for-tramway-in-istanbul-turkey',2018,
  '伊斯坦堡地面供電供應案對外公告。~An Istanbul ground-level-power supply project was announced.',
  '僅支持公告年代及地面供電產品角色，不引用合約細節作教材假設。~Supports announcement year and product role only, not contract details as exercise inputs.')
S('aps-2021','伊斯坦堡地面供電啟用公告','Istanbul ground-level-power deployment announcement','Alstom','https://www.alstom.com/press-releases-news/2021/1/alstom-deploys-its-first-aps-ground-level-power-solution-turkey-eminonu',2021,
  '伊斯坦堡地面供電路段開始營運。~The Istanbul ground-level-power section entered passenger service.',
  '支持啟用年代與工程背景；本課不重製廠商控制邏輯。~Supports deployment year and project context; proprietary control logic is not reproduced.')
S('aps-overview','波爾多地面供電歷史公告','Bordeaux ground-level-power history announcement','Alstom','https://www.alstom.com/press-releases-news/2018/8/alstom-supply-5-extra-citadis-trams-bordeaux-metropole',2003,
  '波爾多無架空線地面供電開始使用。~Bordeaux began using ground-level catenary-free tram power.',
  '支持地面供電產品範圍及代表工程背景，與車載儲能明確區別。~Supports product scope and reference-project context, distinguishing ground supply from onboard storage.')
S('hitachi-2001','小型單軌系統技術論文','Small-type monorail engineering paper','Hitachi','https://www.hitachi.com/content/dam/hitachi/global/en/insights/media/hitachihyoron/2001/r2001_04/r2001_04_104.pdf',2001,
  '小型單軌系統的技術論文出版。~A technical paper on small monorail systems was published.',
  '支持單軌系統工程研究的出版年代與主題，不提供本課假想梁截面。~Supports publication year and monorail engineering topic, not hypothetical beam sections.')
S('hitachi-2008','整合單軌系統技術論文','Integrated monorail systems engineering paper','Hitachi','https://www.hitachi.com/content/dam/hitachi/global/en/insights/media/hitachihyoron/2008/r2008_01/r2008_01_009.pdf',2008,
  '整合單軌系統的技術論文出版。~A technical paper on integrated monorail systems was published.',
  '支持單軌整合研究背景，不把跨座式系統當成懸掛式系統。~Supports monorail integration context without conflating straddle and suspended systems.')
S('wuppertal','烏帕塔爾懸掛鐵路歷史','History of the Wuppertal suspension railway','WSW','https://schwebebahn.de/geschichte-der-schwebebahn',1901,
  '烏帕塔爾懸掛式鐵路開始服務旅客。~The Wuppertal suspension railway began carrying passengers.',
  '支持代表性懸掛鐵路的歷史背景；轉轍算例不代表該系統實際機構。~Supports historical reference context; switch exercises do not reproduce the actual mechanism.')
S('maglev-1994','磁浮導梁精度與乘坐研究','Maglev guideway precision and ride study','Japan Society of Civil Engineers','https://www.jstage.jst.go.jp/article/jscej1984/1994/482/1994_482_67/_article/-char/ja/',1994,
  '磁浮導梁施工精度與乘坐研究出版。~Research linking maglev guideway precision and ride was published.',
  '支持導梁精度與動態關聯的原始研究年代；本課正弦算例另行原創。~Supports primary research year and precision–dynamics context; sinusoidal examples are original.')
S('maglev-1998','磁浮梁式導向道施工研究','Beam-type maglev guideway construction study','Japan Society of Civil Engineers','https://www.jstage.jst.go.jp/article/jscej1984/1998/609/1998_609_29/_article/-char/en',1998,
  '梁式磁浮導向道施工精度研究出版。~Research on beam-type maglev guideway construction accuracy was published.',
  '支持施工精度原始研究的年代與主題，不提供工程驗收容許值。~Supports date and topic of primary construction-accuracy research, not acceptance tolerances.')
S('rtri-maglev','超導磁浮公開原理','Public principles of superconducting maglev','Railway Technical Research Institute','https://www.rtri.or.jp/rd/maglev/principle.html',1998,
  '磁浮導向道工程持續形成公開研究。~Maglev guideway engineering continued to develop public research.',
  '支持電動懸浮、導向與推進原理；靜態磁壓例明確不冒充該系統模型。~Supports electrodynamic suspension, guidance and propulsion; the static-pressure example is explicitly not that system model.')

GROUPS={
 'control':['rams-2002','era-ccs','rams-2025'],
 'station':['fta-emergency','passenger-flow','rb-station'],
 'access':['access-ada','fra-access','rb-station'],
 'machinery':['iso-risk','iso-quality','iso-control'],
 'crossing':['crossing-human','crossing-handbook','rams-2025'],
 'cwr':['cwr-2008','cwr-2010','cwr-2021'],
 'aps':['aps-overview','aps-2018','aps-2021'],
 'monorail':['hitachi-2001','hitachi-2008','rams-2025'],
 'suspended':['wuppertal','iso-risk','iso-control'],
 'maglev':['maglev-1994','maglev-1998','rams-2025'],
}
