#!/usr/bin/env python3
"""Rebuild the 33 V10 electrical/electronics courses from immutable title snapshots.
No network, mutable catalog counters, public datasets or progress records are read/modified.
"""
import json, math
from pathlib import Path
from copy import deepcopy
from group_b_specs import SPECS
from group_b_metadata import SOURCES, VENDORS, source
ROOT=Path(__file__).resolve().parent
CAT={c['id']:c for c in json.loads((ROOT/'group_b_catalog_snapshot.json').read_text())}
TITLES={c['id']:c for c in json.loads((ROOT/'group_b_related_snapshot.json').read_text())}

def ref(s): return {k:s[k] for k in ('title','titleEn','publisher','url')}
def sid(k): return source(k)['id']
def unique(v): return list(dict.fromkeys(v))

PLACES={
'wind':dict(name='DTU Risø 能源研究園區（研究代表點）',nameEn='DTU Risø energy campus (research reference)',city='羅斯基勒',cityEn='Roskilde',country='丹麥',countryEn='Denmark',lat=55.694,lng=12.099,address='Frederiksborgvej 399, 4000 Roskilde, Denmark',keys=['dtuplace','dtutest','wind15'],history=[('1958','能源研究園區啟用','Energy-research campus opens','Risø 於 1958 年啟用；其研究重心後來逐步轉向永續能源。這段沿革顯示大型能源技術需要長期場域與量測能力。','Risø opened in 1958 and later shifted toward sustainable energy, illustrating the long-lived facilities and measurement capability needed for energy research.','dtuplace'),('2020','公開海上風機參考模型','Open offshore reference model','NREL 與 DTU 合作的 IEA 15 MW 參考風機提供公開比較基準；本課使用其研究脈絡，不把參考模型視為產品製造規格。','The NREL/DTU IEA 15-MW reference turbine provides an open comparison baseline; this course uses its research context rather than treating it as a commercial manufacturing specification.','wind15')]),
'storage':dict(name='PNNL Richland 園區（儲能研究代表點）',nameEn='PNNL Richland campus (storage research reference)',city='里奇蘭',cityEn='Richland',country='美國',countryEn='United States',lat=46.343,lng=-119.277,address='902 Battelle Boulevard, Richland, WA, United States',keys=['pnnlplace','pnnlhistory','storage'],history=[('1965','跨領域研究機構成立','An interdisciplinary laboratory is founded','PNNL 官方沿革記載其成立於 1965 年。化學、材料和系統工程研究在此相連；這是儲能技術研究的代表脈絡，並非每項課程的發明地。','PNNL records its founding in 1965. Chemistry, materials and system engineering connect here; this is representative storage-research context, not the birthplace of every course topic.','pnnlhistory'),('2024','Grid Storage Launchpad 啟用','Grid Storage Launchpad opens','PNNL 於 2024 年公布 Grid Storage Launchpad 啟用，連結材料研究與儲能系統驗證。課程因而把元件指標與可交付系統性能分開檢查。','PNNL announced the Grid Storage Launchpad opening in 2024, connecting materials research and storage-system validation. The curriculum likewise checks component metrics separately from deliverable system performance.','pnnlhistory')]),
'marine':dict(name='EMEC Fall of Warness（潮流測試場代表區）',nameEn='EMEC Fall of Warness (tidal-test reference area)',city='Eday，奧克尼',cityEn='Eday, Orkney',country='英國',countryEn='United Kingdom',lat=59.13,lng=-2.80,address='Fall of Warness / Caldale, Eday, Orkney, Scotland, United Kingdom',keys=['emectidal','emechistory'],history=[('2003','海洋能源測試中心成立','Marine-energy test center established','EMEC 於 2003 年成立，將海洋資源、環境監測和電力測試放在共同場域內。這使原型表現能連到真實電網介面。','EMEC was established in 2003, bringing marine resources, environmental monitoring and electrical testing into a common setting that connects prototype behavior to grid interfaces.','emechistory'),('2006','潮流場開始運作','Tidal test site opens','Fall of Warness 潮流測試場於 2006 年開放；官方場址資料描述海纜與岸端調節設施。本課由此討論海洋機組到岸網的介面。','Fall of Warness opened in 2006; official site information describes subsea cables and onshore conditioning. This course uses that context to examine marine-device/grid interfaces.','emechistory')]),
'motor':dict(name='TI 達拉斯總部（電子控制產業代表點）',nameEn='TI Dallas headquarters (electronic-control industry reference)',city='達拉斯',cityEn='Dallas',country='美國',countryEn='United States',lat=32.912,lng=-96.752,address='12500 TI Boulevard, Dallas, TX 75243, United States',keys=['tiplace','tihistory','tifaq','motorcontrol'],history=[('1951','TI 名稱形成','The TI name takes shape','官方資料記錄公司源於 1930 年的 GSI，1951 年更名為 Texas Instruments；本課以其公開控制文件連結元件與機電系統。','Official records trace the company to GSI in 1930 and the Texas Instruments name in 1951; this course uses public control documentation to connect devices with electromechanical systems.','tifaq'),('1958','積體電路成為控制技術基礎','Integrated circuits underpin control technology','TI 官方歷史記載 Jack Kilby 在 1958 年的積體電路工作。今天的即時馬達控制結合量測、計算和功率元件；地圖代表控制產業脈絡，不是本課所有設備產地。','TI’s history records Jack Kilby’s integrated-circuit work in 1958. Modern real-time motor control combines sensing, computation and power devices; this map indicates industry context, not the origin of all course equipment.','tihistory')])}
PLACES['power']=deepcopy(PLACES['motor'])
PLACES['shore']=dict(name='蘇黎世：ABB 岸電技術供應商脈絡',nameEn='Zurich: ABB shore-power supplier context',city='蘇黎世',cityEn='Zurich',country='瑞士',countryEn='Switzerland',lat=47.3769,lng=8.5417,address='Zurich, Switzerland (city reference; not a port or installation)',keys=['abbhistory','abbheritage','shore'],history=[('1891','電機工程企業在 Baden 起步','Electrical-engineering company begins in Baden','BBC 於 1891 年在瑞士 Baden 成立，其電機工程傳承是理解今日電力轉換供應鏈的背景；地圖不代表當年的廠址。','BBC began in Baden, Switzerland, in 1891. Its engineering heritage gives context to modern power-conversion supply chains; this map is not the historic factory location.','abbheritage'),('1988','ABB 合併成立','ABB formed by merger','ASEA 和 BBC 於 1988 年合併成 ABB，總部在蘇黎世。岸電課以其公開頻率轉換產品資料連結供應商角色與船岸介面，並不宣稱課程是在瑞士港口實作。','ASEA and BBC merged into ABB in 1988 with headquarters in Zurich. Shore-power lessons connect its public frequency-converter documentation to ship/shore interfaces, without claiming a Swiss port implementation.','abbhistory')])
SPECS['a250']['group']='shore'


def place_for(cid,c):
    p=deepcopy(PLACES[c['group']]); hist=p.pop('history'); keys=p.pop('keys')
    p.update(addressEn=p['address'],mapQuery=p['address'],coordinateScope='依公開地址標示的概略園區／區域代表座標，不是已測量的設備位置或現場導航點；本課技術與廠商跨越多國。',coordinateScopeEn='Approximate campus/area coordinates associated with the public address, not a surveyed equipment location or field-navigation point; the course spans international technology and suppliers.')
    return dict(courseId=cid,place=p,summary=f'本課聚焦{c["focus"]}。地圖提供公開研究或產業交流的背景；本課的模型和假設不宣稱在該處實測、發明或量產。',summaryEn=f'This course focuses on {c["focusEn"]}. The map provides public research/industry context; course models and assumptions are not claimed to have been measured, invented or manufactured there.',history=[dict(year=y,title=t,titleEn=te,text=x,textEn=xe,sourceIds=[sid(k)]) for y,t,te,x,xe,k in hist],connection=f'從{c["units"][0][0]}的課程問題出發，依來源追溯研究、元件供應與系統驗證的分工；代表地點不等於完整供應鏈。',connectionEn=f'Start with {c["units"][0][1].lower()} and trace roles in research, components and system validation; the reference location does not represent the entire supply chain.',sourceIds=[sid(k) for k in keys],references=[ref(source(k)) for k in keys])

# Every relation names an actual shared engineering interface and a distinct model boundary.
REL={
'a236': [('發電機功率與 DC 能量平衡','Generator power and DC-energy balance','發電機課重電磁與海洋熱條件，變流器課重暫態限流','The generator course emphasizes electromagnetics/marine thermal conditions; converters emphasize transient limits'),('機組輸出與集電負載','Turbine output and collector loading','單機熱額定不能取代全場海纜潮流與備援分析','Unit thermal ratings do not replace farm-wide cable flow/redundancy analysis')],
'a237': [('軸功率與電流容量協調','Shaft-power/current-capacity coordination','發電機的機械與熱限制不能由控制器放寬','Controls cannot relax generator mechanical/thermal limits'),('變流器電流限幅與電網電壓','Converter current limits and grid voltage','跟網控制與成網控制具有不同角度及頻率基準','Grid-following and grid-forming controls use different angle/frequency references')],
'a238': [('故障電流與限流變流器','Fault current and current-limited converters','集電保護需加入電纜和多機拓樸','Collector protection adds cables and multi-turbine topology'),('海底電纜熱路與無功','Subsea-cable thermal paths and VARs','集電網還需多支路潮流、選擇性和故障後承載','Collectors additionally require branch flow, selectivity and post-fault capacity')],
'a239': [('水頭、流量與電機功率','Head, flow and machine power','抽蓄同時有抽水用電與庫容約束','Pumped storage adds pumping demand and reservoir constraints'),('模式切換與電網調節','Mode transitions and grid regulation','水力機組的水錘與轉換延遲不同於一般微電網設備','Hydraulic water-hammer and transition delays differ from general microgrid devices')],
'a240': [('海纜、電力調節與併網','Subsea cables, conditioning and interconnection','潮流反向與停潮不同於風場風速分布','Flow reversal and slack tides differ from wind-speed distributions'),('變動能源與儲能功率介面','Variable resources and storage interfaces','液流電池還需泵流與堆疊電壓限制','Flow batteries additionally require pumping and stack-voltage limits')],
'a241': [('單體限制到站級調度','Cell limits to plant dispatch','EMS 不能替代 BMS 的單體觀測與保護','EMS cannot replace cell-level BMS observation/protection'),('儲能 PCS 與成網服務','Storage PCS and grid-forming services','成網穩定需要動態模型，容量足夠並不保證穩定','Grid-forming stability needs dynamic models; capacity alone is insufficient')],
'a242': [('可用電量與功率限制','Available charge and power limits','整站需再計入 PCS、輔機與多串不平衡','Plants also include PCS, auxiliaries and string imbalance'),('電流偏移與庫侖積分','Current offset and coulomb integration','量測準確度不能獨自證明電池保護反應時間','Measurement accuracy alone does not prove battery-protection response')],
'a243': [('儲能調度與 AC/DC 能量帳','Storage dispatch and AC/DC ledgers','液流電池的泵耗與槽量和鋰電池不同','Flow-battery pumping/tank inventory differs from lithium-ion systems'),('堆疊電壓包絡與雙向隔離','Stack-voltage envelopes and bidirectional isolation','DAB 模型還需相移、循環電流與 ZVS 條件','DAB models add phase shift, circulation and ZVS conditions')],
'a244': [('串聯均衡與量測誤差','Series balancing and measurement error','電容電壓能量平方關係不同於電池 SOC 曲線','Capacitor squared-voltage energy differs from battery SOC curves'),('短時回生能量吸收','Short regenerative-energy absorption','電容需後續釋能，不能無限吸收重複制動','Capacitors need later discharge and cannot absorb repeated braking indefinitely')],
'a245': [('旋轉能量與磁浮控制','Rotational energy and magnetic control','磁浮穩定是額外自由度，不等於電機速度控制','Levitation stability is separate from motor-speed control'),('四象限能量回收','Four-quadrant energy recovery','飛輪以轉速窗口儲能，車輛則受行車及電池條件約束','Flywheels use speed-window storage; vehicles add motion and battery constraints')],
'a246': [('備援路徑與故障承載','Backup paths and post-fault loading','UPS 拓樸不能代替整個資料中心的共同失效分析','UPS topology does not replace data-center common-failure analysis'),('短暫負載缺口能量','Short load-gap energy','超級電容適合短時功率，需另證明長時續航','Supercapacitors suit brief power and need separate long-runtime evidence')],
'a247': [('UPS 轉移與供電容量','UPS transfer and supply capacity','雙路配電要驗證從來源到機櫃的完整獨立性','Dual distribution needs end-to-end independence to the rack'),('故障區段隔離','Faulted-section isolation','資料中心 A/B 維護情境與公用配電拓樸不同','Data-center A/B maintenance differs from utility distribution topology')],
'a248': [('電化學負載與 DC 電流品質','Electrochemical loads and DC-current quality','燃料電池產電，電解槽消耗電力，能量方向不可混用','Fuel cells generate and electrolyzers consume; energy directions differ'),('快速負載緩衝','Fast-load buffering','超級電容需電壓窗口管理，燃料電池受反應物流限制','Capacitors require voltage-window management; fuel cells have reactant limits')],
'a249': [('法拉第電量與系統效率','Faraday charge accounting and system efficiency','電解與燃料電池有不同極化及輔機條件','Electrolysis and fuel cells differ in polarization/auxiliaries'),('輸入諧波與電流成形','Input harmonics and current shaping','電解槽需額外 DC 紋波與最小負載限制','Electrolyzers add DC-ripple/minimum-load limits')],
'a250': [('負載轉移與電壓品質','Load transfer and voltage quality','岸船還有頻率差、海洋電纜和接地相容問題','Shore power adds frequency mismatch, marine cables and grounding compatibility'),('主動整流與電網電流','Active rectification and grid current','岸電含船側獨立 AC 頻率與輸出調壓','Shore systems add independent ship-side AC frequency/output regulation')],
'a251': [('疊片、繞組與熱公差','Laminations, windings and thermal tolerances','感應機用鼠籠與滑差，PMSM 加入永磁退磁條件','Induction uses cages/slip; PMSM adds magnet demagnetization'),('磁鏈與電流控制','Flux and current regulation','感應機轉子磁鏈估測與 PMSM 固定磁鏈不同','Induction rotor-flux estimation differs from PM flux')],
'a252': [('定轉子製造與公差','Stator/rotor manufacturing and tolerances','磁鐵保持和退磁是永磁機額外條件','Magnet retention/demagnetization are additional PM constraints'),('轉矩包絡與逆變器電壓','Torque envelopes and inverter voltage','SiC 器件切換和 EMI 不由電機磁路模型充分描述','Motor magnetics do not fully describe SiC switching/EMI')],
'a253': [('電角度與電流成形','Electrical angle and current shaping','SRM 非線性磁共能不能直接套用正弦 PMSM dq 模型','SR co-energy nonlinearity does not directly follow sinusoidal PMSM dq models'),('相電流換相與位置資訊','Phase commutation and position information','SRM 電感斜率產轉矩，BLDC 依永久磁鐵反電勢','SR torque follows inductance slope; BLDC uses permanent-magnet EMF')],
'a254': [('位置量測與誤差預算','Position measurement and error budgets','線性平台還需阿貝偏移、導軌與熱膨脹分析','Linear stages add Abbe offset, guides and thermal expansion'),('力控制與電流迴路','Force control and current loops','平移力與旋轉轉矩的機械模型不同','Translational force and rotational torque have different mechanics')],
'a255': [('反電勢過零與低速可觀測性','Back-EMF crossing and low-speed observability','六步換相與連續角度觀測器對波形的要求不同','Six-step and continuous-angle observers need different waveforms'),('橋臂時序與門極完整性','Bridge timing and gate integrity','驅動器延遲和 CMTI 是控制序列之外的器件限制','Driver delay/CMTI are device constraints beyond commutation sequences')],
'a256': [('尺解析度與實際定位','Scale resolution and physical positioning','線性平台加入幾何與熱誤差，不只是編碼器誤差','Linear stages add geometric/thermal errors beyond encoders'),('電角度與同步取樣','Electrical angle and synchronous sampling','FOC 還需電流尺度和電壓限制模型','FOC adds current-scaling and voltage-limit models')],
'a257': [('電壓模型與角度估測','Voltage models and angle estimation','觀測器在低速的資訊不足需另處理','Observer information loss at low speed needs separate treatment'),('角度延遲與零位','Angle delay and zero offset','編碼器精度不能替代完整閉環穩定驗證','Encoder accuracy does not replace closed-loop stability evidence')],
'a258': [('dq 模型與殘差修正','dq models and residual correction','無感測估測增加不可觀測區和參數誤差','Sensorless estimation adds unobservable regions/parameter errors'),('過零訊號與啟動','Zero crossings and startup','連續觀測角與六步扇區資訊精細度不同','Continuous angle and six-step sectors have different granularity')],
'a259': [('短時能量緩衝與電壓窗口','Transient buffers and voltage windows','電容只能提供有限能量餘裕，非完整制動保障','Capacitors offer finite energy headroom, not complete braking assurance'),('雙向功率與牽引限制','Bidirectional power and traction limits','車輛回生另受電池接受能力與機械制動協調約束','Vehicle recovery adds battery-acceptance and friction-brake constraints')],
'a260': [('高速旋轉能量與停機','High-speed energy and rundown','磁浮位置穩定不等同飛輪能量調度','Levitation stability is not flywheel energy dispatch'),('位置回授與延遲','Position feedback and delay','磁浮負剛性與轉子模態不同於一般軸編碼','Magnetic negative stiffness/rotor modes differ from general shaft encoding')],
'a261': [('電機轉矩與電壓包絡','Motor torque and voltage envelopes','電機磁鐵與熱限制獨立於 SiC 元件額定','Motor magnet/thermal limits are independent of SiC ratings'),('回生能量與 DC 母線','Regenerative energy and DC bus','逆變器可逆不保證電池隨時可接受回充','A reversible inverter does not guarantee battery charge acceptance')],
'a262': [('高頻軟切換與磁件','High-frequency soft switching and magnetics','LLC 需負載增益及雙諧振模型','LLC adds load-gain and dual-resonance models'),('圖騰柱高頻換流','High-frequency totem-pole commutation','PFC 另需線週、過零及諧波分析','PFC adds line-cycle, zero-crossing and harmonic analysis')],
'a263': [('隔離功率與 ZVS','Isolated power and ZVS','LLC 主要調頻，PSFB 以相移控制有效占空','LLC primarily varies frequency; PSFB varies effective duty via phase shift'),('高頻器件與寄生','High-frequency devices and parasitics','GaN 本身不保證整個 LLC 操作範圍軟切換','GaN alone does not ensure soft switching across LLC operation')],
'a264': [('變壓器隔離與諧振換流','Transformer isolation and resonant commutation','PSFB 續流和占空比損失不同於 LLC 增益控制','PSFB freewheel/duty loss differs from LLC gain control'),('相移功率與循環電流','Phase-shift power and circulation','DAB 次級也主動開關並支援雙向功率','DAB actively switches the secondary and supports bidirectional power')],
'a265': [('變動堆疊電壓與雙向轉換','Variable stack voltage and bidirectional conversion','液流系統再加入電化學及泵浦約束','Flow systems additionally impose electrochemical/pump constraints'),('漏感換流與軟切換','Leakage commutation and soft switching','PSFB 與 DAB 的次級導通和功率公式不同','PSFB/DAB secondary conduction and power formulas differ')],
'a266': [('電網電流品質與整流','Grid-current quality and rectification','電解系統還受 DC 電流與產氫需求約束','Electrolyzers add DC-current and production constraints'),('GaN 換流與寄生控制','GaN commutation and parasitic control','PFC 外環需避開二倍線頻，而一般 DC/DC 沒有此同一條件','PFC outer loops address twice-line-frequency ripple absent in a generic DC/DC stage')],
'a267': [('SiC 門極暫態與保護','SiC gate transients and protection','牽引系統另有驅動週期、熱循環及功能安全要求','Traction adds drive-cycle, thermal-cycle and functional-safety requirements'),('快速檢測與保護延遲','Fast detection and protection latency','電流感測精度不等於門極驅動關斷能力','Sensing accuracy is not gate turn-off capability')],
'a268': [('電流偏移與 SOC 誤差','Current offset and SOC error','BMS 還需單體電壓、溫度與化學條件','BMS adds cell voltage, temperature and chemistry'),('故障門檻與關斷時序','Fault thresholds and turn-off timing','感測器與隔離驅動器各自有獨立延遲和故障模式','Sensors and isolated drivers have independent delays/failure modes')]
}

REL['a257'].reverse()  # snapshot order is encoder a256, then sensorless a258

def related_for(cid,c):
    rr=[]
    for idx,target in enumerate(c['related']):
        title=TITLES[target]; shared,se,diff,de=REL[cid][idx]
        rr.append(dict(id=target,title=title['title'],titleEn=title['titleEn'],why=shared,whyEn=se,transfer=shared,transferEn=se,difference=diff,differenceEn=de,
          practice=[f'以「{shared}」建立兩課的共同介面圖，標示訊號、能量與單位。',f'用本課教學算例改變一個輸入，列出轉移到「{title["title"]}」時需補充的資料。',f'針對「{diff}」設計一個反例；先預測，再以合成資料或公開量測驗證。'],
          practiceEn=[f'Draw the shared interface for {se.lower()}, labeling signals, energy and units.',f'Change one input in this course’s worked example and list additional data needed for {title["titleEn"]}.',f'Design a counterexample to the transfer boundary: {de}. Predict first, then check using synthetic data or public measurements.'],referenceUrls=unique([source(k)['url'] for k in c['sourceKeys']])))
    return dict(courseId=cid,overview='以下是有共同物理與介面的延伸課程；每項都指出不可直接照搬的邊界。',overviewEn='These extensions share physics/interfaces; each identifies a boundary that prevents direct copying.',related=rr,references=[ref(source(k)) for k in unique(c['sourceKeys'])])

COURSES=[];PL=[];RL=[]
for cid,c in SPECS.items():
    base=deepcopy(CAT[cid]); srcids=unique([sid(k) for k in c['sourceKeys']]); stages=[]
    for sn,(stzh,sten) in enumerate(zip(c['stages'],c['stagesEn'])):
        steps=[]
        for ui in range(sn*3,sn*3+3):
            title,ten,principle,pen,evidence,een=c['units'][ui]
            for phase in range(2):
                seq=ui*2+phase+1; stepid=f'{cid}-v10-{seq:02d}'
                tz=title+('：反證與驗收' if phase else '：建立模型'); te=ten+(': challenge and acceptance' if phase else ': build the model')
                action=(f'先沿用模型，寫下會推翻「{principle}」的觀察。{evidence} 加入一個對照條件，分開記錄原始數據、推論與不確定度；若前提失效則暫緩判定。' if phase else f'{evidence} 先畫出系統邊界與能量或訊號方向，逐項寫明單位、定義和固定條件，再預測結果；只使用離線模型或已取得的公開紀錄。')
                ae=(f'Use the model and state an observation that would refute this claim: {pen} {een} Add a control condition and separate raw data, inference and uncertainty. Withhold acceptance if assumptions fail.' if phase else f'{een} First draw the system boundary and energy/signal direction. State units, definitions and controlled conditions, then predict the result. Use offline models or already available public records only.')
                correct=evidence if phase else principle; correcten=een if phase else pen
                distractors=['只要數值接近名目值，就不必檢查單位、量測邊界與誤差。','以其他課程或其他元件的額定值直接作本步的驗收門檻。']; d_en=['If a number is near its nominal value, units, boundaries and errors do not need checking.','Use a rating from another course or device directly as this step’s acceptance limit.']
                answer=(seq+int(cid[1:]))%3; opts=distractors[:]; oe=d_en[:]; opts.insert(answer,correct);oe.insert(answer,correcten)
                step=dict(id=stepid,order=seq,sequence=seq,estimatedMinutes=30,simulationOnly=True,sourceIds=srcids,prerequisiteIds=[] if seq==1 else [f'{cid}-v10-{seq-1:02d}'],title=tz,titleEn=te,
                  objective=f'以可檢驗證據理解{title}，辨識物理機制、量測條件與模型限制。',objectiveEn=f'Understand {ten.lower()} through testable evidence, distinguishing physics, measurement conditions and model limits.',instruction=action,instructionEn=ae,
                  observation=f'{evidence} 比較前先確認量綱與取樣時間一致；若差異小於不確定度，保留未定結論。',observationEn=f'{een} Match dimensions and sampling time before comparison; retain an unresolved conclusion if differences are below uncertainty.',
                  failure=f'若「{title}」的結果與預測不符，分別檢查定義／尺度、模型前提及感測或數據錯誤；不要把{c["focus"]}的限制隱藏在單一合格數字中。',failureEn=f'If {ten.lower()} disagrees with prediction, separately check definitions/scaling, assumptions and sensing/data faults. Do not hide the limits of {c["focusEn"]} behind one passing number.',
                  check=f'交付「{title}」的圖或計算、預測、指定對照、單位與一項尚未驗證的假設；說明何種觀察應暫緩放行。',checkEn=f'Submit a diagram/calculation for {ten.lower()}, prediction, specified comparison, units and one unvalidated assumption. State which observation requires withholding acceptance.',
                  knowledge=[dict(id=stepid+'-k1',title=title+'：原理',titleEn=ten+': principle',text=principle,textEn=pen,sourceIds=srcids),dict(id=stepid+'-k2',title=title+'：證據',titleEn=ten+': evidence',text=evidence,textEn=een,sourceIds=srcids),dict(id=stepid+'-k3',title='本課可重算的算例與適用範圍',titleEn='Course worked example and validity',text=c['example']+' '+c['limit'],textEn=c['exampleEn']+' '+c['limitEn'],sourceIds=srcids)],
                  quiz=dict(question=f'關於「{tz}」，哪一項是本步有依據的主張或驗證方式？',questionEn=f'For “{te}”, which claim or verification is justified?',options=opts,optionsEn=oe,answer=answer,explanation=principle+' '+evidence,explanationEn=pen+' '+een))
                steps.append(step)
        stages.append(dict(id=f'{cid}-v10-stage{sn+1:02d}',order=sn+1,title=stzh,titleEn=sten,description=f'以三個具體技術單元完成{stzh}；每單元先建立模型，再以對照和反證驗收。',descriptionEn=f'Complete {sten.lower()} through three technical units, each pairing a model with controlled verification.',steps=steps))
    base.update(kind='course',category='electronics',summary=f'以 4 階段、24 步探討{c["focus"]}，包含 12 個專題模型、對照驗證、原創教學算例及延伸工法。',summaryEn=f'Four stages and 24 steps explore {c["focusEn"]}, including 12 topic-specific models, controlled checks, original worked examples and related methods.',sourceIds=srcids,status='guided',contentStatus='reviewable-educational-curriculum',curriculumVersion=10,depth=4,stepCount=24,estimatedMinutes=720,simulationOnly=True,languageCoverage=['zh-TW','en'],scope='公開原理支持的離線工程教學；24 步是學習拆解，不是完整工廠或現場 SOP。數字明示為假設教學例，不冒充廠商機密、實測或通用設定。'+c['limit'],scopeEn='Offline engineering education based on public principles. The 24 steps are a learning decomposition, not a complete factory/field SOP. Numbers are explicit teaching assumptions, not proprietary recipes, measurements or universal settings. '+c['limitEn'],diagram=dict(type='electronics',labels=c['stages'],labelsEn=c['stagesEn'],original=True,notToScale=True),stages=stages,vendorHints=deepcopy(VENDORS[cid]))
    COURSES.append(base);PL.append(place_for(cid,c));RL.append(related_for(cid,c))

used=set()
for course in COURSES:
    used.update(course['sourceIds'])
    for vendor in course['vendorHints']:used.update(vendor['sourceIds'])
for place in PL:used.update(place['sourceIds'])
DATA=dict(version=10,scope='a236–a268: 33 electrical/electronics courses, 792 steps, 396 technical units; original bilingual teaching text and calculations, source links only.',courses=COURSES,sources=[s for s in SOURCES.values() if s['id'] in used],places=PL,related=RL)
assert len(COURSES)==33
assert all(len(set(c['sourceIds']))>=2 for c in COURSES), 'Every course needs two distinct primary sources after alias resolution'
assert sum(len(s['steps']) for c in COURSES for s in c['stages'])==792
assert all(len(c['stages'])==4 and all(len(s['steps'])==6 for s in c['stages']) for c in COURSES)
assert len({s['id'] for c in COURSES for st in c['stages'] for s in st['steps']})==792
assert all(len(r['related'])==2 and all(len(x['practice'])==len(x['practiceEn'])==3 for x in r['related']) for r in RL)
assert all(len(p['history'])>=2 for p in PL)
(ROOT/'group_b.json').write_text(json.dumps(DATA,ensure_ascii=False,indent=2)+'\n')
print(f'Group B: {len(COURSES)} courses, 792 steps, 2376 knowledge points, {len(DATA["sources"])} primary sources, 33 places, 66 related links')
