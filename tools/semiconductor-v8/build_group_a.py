"""Original bilingual learning work packages; public references, not equipment recipes."""
import json, copy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
CAT={x['id']:x for x in json.loads((ROOT/'public/academy/data/catalog.json').read_text())}
COURSES={}
def add(cid,stages,sources,related,rows):
    r=[x.strip() for x in rows.strip().splitlines() if x.strip()]
    assert len(r)==24,(cid,len(r))
    COURSES[cid]=dict(stages=stages.split('|'),sources=sources.split(),related=related.split(),rows=r)

# Every row is independently scoped: observable engineering relationship, not a renamed generic step.
add('a003','晶棒與切片預算~Ingot and slicing budget|線網與切削互動~Wire web and cutting|片形與損傷證據~Geometry and damage|良率與後段交接~Yield and downstream handoff','sumco wafer','a004 a005',r'''
辨識晶向~Identify crystal orientation|晶向標記要連到晶棒座標，不能以外觀代替繞射證據。~Orientation marks require ingot coordinates and diffraction evidence, not appearance.
定義可用晶棒長~Define usable ingot length|頭尾排除長度會改變可用片數。~Head and tail exclusions change usable wafer count.
切縫預算~Budget kerf|每片占用長度包含晶圓厚度與切縫。~Length consumed per slice includes wafer thickness and kerf.
厚度留量~Reserve thickness allowance|切片厚度還須支付損傷移除與拋光留量。~Sliced thickness must cover damage removal and polishing allowance.
固定端受力圖~Draw mounting loads|偏心固定會讓進給負荷在切片中不均。~Eccentric mounting makes feed loading asymmetric.
來料電阻率分區~Map incoming resistivity|沿晶棒的電阻率變化不能用單片平均值代表。~One wafer average cannot describe axial resistivity variation.
線徑與槽距~Separate wire diameter and pitch|線徑、切縫與導輪槽距是不同幾何量。~Wire diameter, kerf and guide-groove pitch differ.
張力與撓曲~Relate tension and deflection|同一橫向負荷下張力改變線網撓曲。~Wire tension changes deflection under the same transverse load.
進給與線速分工~Separate feed and wire speed|進給速度決定進入速率，線速影響磨粒接觸歷程。~Feed controls penetration while wire speed changes abrasive contact history.
磨粒分布~Inspect abrasive distribution|少數過大磨粒可能留下深損傷，平均粒徑不足以判讀。~Oversized abrasive tails can cause deep damage despite a stable mean size.
排屑路徑~Trace debris removal|排屑不足會改變接觸與局部熱負荷。~Poor debris removal changes contact and local heating.
斷線事件~Reconstruct wire breakage|斷線前的張力尖峰與片序能限定受影響區域。~Pre-break tension spikes and slice order delimit affected material.
總厚度變異~Measure total thickness variation|TTV 是厚度最大與最小之差，不是表面粗糙度。~TTV is maximum minus minimum thickness, not roughness.
翹曲與弓形~Separate warp and bow|自由狀態形貌與夾持後平坦度不可混用。~Free-state shape differs from clamped flatness.
鋸痕方向~Register saw-mark direction|鋸痕方向應與線運動及進給座標一起比較。~Saw marks need registration to wire and feed directions.
次表面損傷~Estimate subsurface damage|表面看似光滑仍可能保有次表面裂紋。~An apparently smooth surface can retain subsurface cracks.
邊緣崩缺~Classify edge chips|邊緣缺口尺寸及位置共同影響後續破片風險。~Edge-chip size and position influence subsequent fracture risk.
量測重複性~Check measurement repeatability|重新放片的變異應先與片間差異分開。~Repositioning variation must be separated from wafer variation.
材料利用率~Compute material utilization|提高片數若同時增加報廢，未必提高有效矽利用率。~More slices may not improve usable silicon yield if rejects increase.
線耗追蹤~Track wire consumption|線耗量需按合格片數正規化。~Wire consumption should be normalized by accepted wafers.
切片序列圖~Plot slice-order trends|連續片的週期性厚度誤差可提示導輪相關因素。~Periodic slice-thickness errors can suggest guide-related causes.
移除留量交接~Transfer removal allowance|研磨端需要最深損傷估計而不只是平均厚度。~Lapping needs estimated deepest damage, not just mean thickness.
盲樣重驗~Recheck blinded samples|對邊界片重驗須保留原片序與量測版本。~Boundary-sample retests need original slice identity and measurement version.
切片批次放行~Release a slicing lot|厚度、損傷、邊緣與追溯證據須同時交付。~Release requires thickness, damage, edge and traceability evidence together.
''')
add('a005','基板與磊晶目標~Substrate and epitaxy target|反應與傳輸~Reaction and transport|晶體及摻雜判讀~Crystal and doping evidence|整合與放行~Integration and release','sumco epi mit','a020 a019',r'''
區分磊晶與沉積~Distinguish epitaxy from deposition|磊晶需要與基板有確定晶體關係。~Epitaxy requires a defined crystallographic relationship to the substrate.
基板電性階梯~Define substrate-layer electrical contrast|磊晶層與基板可有不同摻雜濃度。~The epitaxial layer and substrate can have different doping.
晶向與台階~Read orientation and terraces|微偏角影響表面台階密度及成長形貌。~Miscut changes terrace density and growth morphology.
原生氧化層~Assess native oxide|殘留氧化物會中斷外延晶格的延續。~Residual oxide interrupts crystalline registry.
表面潔淨交接~Specify the clean-to-growth handoff|清洗後等待時間可能改變再氧化與吸附。~Queue time after cleaning can change reoxidation and adsorption.
截面厚度目標~Set cross-section targets|膜厚目標應與電性用途及後段熱歷程連結。~Thickness targets require electrical purpose and later thermal history.
反應控制區~Identify reaction-limited growth|反應受限區對表面溫度較敏感。~Reaction-limited growth is more sensitive to surface temperature.
傳質控制區~Identify transport-limited growth|傳輸受限時增加表面反應速率未必增加成長。~Faster surface reaction need not accelerate transport-limited growth.
入口耗盡~Trace inlet depletion|反應物沿流向耗盡可形成厚度梯度。~Reactant depletion along flow can create thickness gradients.
旋轉平均效果~Assess rotation averaging|旋轉能平均角向不均，未必消除徑向梯度。~Rotation averages azimuthal variations but may preserve radial gradients.
自摻雜~Trace autodoping|基板釋出摻雜可污染原本設定的磊晶濃度。~Substrate dopants can alter intended epitaxial doping.
腔體記憶~Identify chamber memory|前批材料可能影響後批背景濃度。~Previous chamber history can affect subsequent background doping.
厚度均勻圖~Map thickness uniformity|中心邊緣與方位點都需納入採樣。~Sampling should include radial and azimuthal positions.
摻雜深度輪廓~Read doping depth profiles|濃度輪廓的陡峭程度會受量測解析度限制。~Measured profile abruptness is limited by instrument resolution.
電阻率與活化~Relate resistivity and activation|電阻率取決於載子濃度及遷移率。~Resistivity depends on both carrier density and mobility.
堆疊錯誤~Classify stacking defects|局部晶體缺陷應與基板缺陷座標配對。~Local crystal defects should be registered to substrate defects.
粗糙度尺度~Compare roughness scales|不同掃描面積可能得到不同粗糙度統計。~Roughness statistics depend on scan area.
界面擴散~Estimate interface broadening|後續熱處理會改變原先的摻雜階梯。~Later heating can broaden an initially abrupt doping transition.
熱預算帳本~Build a thermal-budget ledger|相同最終膜厚不代表相同熱歷程。~Equal final thickness does not imply equal thermal history.
圖案負載效應~Assess pattern loading|裸片結果不能直接代替有圖案表面的成長結果。~Blanket-wafer results do not directly predict patterned growth.
粒子與成長缺陷~Distinguish particles from growth defects|粒子沉積與晶格成長缺陷需要不同分析證據。~Deposited particles and crystalline growth defects require different evidence.
雙因子實驗~Design a two-factor study|改變溫度與流量時要保留交互作用判讀。~A temperature-flow study should preserve interaction effects.
電性見證片~Choose electrical witnesses|只量膜厚不能保證電性符合要求。~Thickness alone cannot establish electrical suitability.
磊晶交接檔~Assemble the epitaxy dossier|膜厚、摻雜、缺陷與熱歷程共同定義材料品質。~Thickness, doping, defects and thermal history jointly define quality.
''')
add('a006','SOI 結構分工~SOI layer functions|鍵合與層轉移~Bonding and layer transfer|薄層量測~Thin-layer measurements|元件相容性~Device compatibility','soitec sumco wafer','a014 a004',r'''
辨認三層結構~Identify the three-layer stack|頂矽、埋氧與支撐晶圓分別承擔不同功能。~Top silicon, buried oxide and handle wafer have different roles.
選擇層轉移路徑~Compare layer-transfer routes|鍵合後研薄與離子切割不是同一轉移機制。~Bond-and-thin and ion-cut use different transfer mechanisms.
頂矽厚度預算~Budget top-silicon thickness|分裂後修整會消耗頂矽留量。~Post-split finishing consumes top-silicon allowance.
埋氧厚度作用~Assess buried-oxide thickness|埋氧同時影響電隔離與熱傳。~Buried oxide affects electrical isolation and heat flow.
供體可回收性~Plan donor reuse|供體再使用需要表面修復與累計厚度帳本。~Donor reuse requires surface recovery and cumulative thickness accounting.
晶圓配對~Pair donor and handle wafers|熱膨脹及形貌不相容會影響鍵合品質。~Thermal-expansion and shape mismatch can impair bonding.
離子層深度~Locate the implanted split layer|佈植深度分布決定弱化層位置的不確定度。~Implant depth distribution sets split-layer position uncertainty.
活化表面~Compare activated surfaces|表面活化改善接合但也可能改變粗糙度。~Activation can assist bonding while changing surface roughness.
顆粒與空洞~Connect particles to voids|單一顆粒可能造成大於自身尺寸的未鍵合區。~One particle can create an unbonded region larger than itself.
鍵合波前~Track bonding-front propagation|波前不規則可提示局部氣體或接觸問題。~Irregular bonding fronts can indicate trapped gas or contact problems.
分裂與熱處理~Separate splitting from strengthening|分裂形成薄層，鍵合強化另有介面目標。~Splitting forms the thin layer while bond strengthening targets the interface.
供體修復~Define donor refresh evidence|再拋光後需重新確認形貌與殘留損傷。~Refreshed donors need renewed shape and damage assessment.
頂矽厚度圖~Map top-silicon thickness|厚度非均勻可能轉成元件臨界電壓變異。~Thickness nonuniformity can translate into threshold-voltage variation.
埋氧連續性~Inspect buried-oxide continuity|局部缺陷可能建立不預期的電性路徑。~Local oxide defects can create unintended electrical paths.
鍵合強度分布~Map bond strength|局部強度不能由單一平均破壞值代表。~One mean fracture value cannot describe local bond strength.
界面陷阱~Assess interface traps|幾何完整不等於界面電性良好。~Geometric integrity does not establish electrical interface quality.
表面粗糙度~Check transferred-surface roughness|分裂面與完成拋光面需分別比較。~The split surface and finished surface require separate comparisons.
缺陷邊緣排除~Specify edge exclusion|邊緣未鍵合區需與可用面積一起呈現。~Unbonded edges must be reported with usable area.
自熱效應~Analyze self-heating|埋氧的熱阻可提高局部溫升。~Buried-oxide thermal resistance can increase local heating.
背閘耦合~Trace back-gate coupling|支撐層電位可透過介電層耦合至通道。~Handle potential can couple through dielectric into the channel.
RF 基板差異~Compare RF substrate needs|高電阻支撐層與邏輯薄體需求並不等同。~High-resistivity RF handles and thin-body logic have different requirements.
應力翹曲~Assess stress-induced bow|多層應力平衡取決於厚度與材料組合。~Multilayer stress balance depends on thickness and material choice.
分層追溯~Trace layer provenance|頂層與支撐層的原始批號都要保留。~Both donor and handle lot identities must remain traceable.
SOI 放行矩陣~Release the SOI stack|隔離、薄層均勻、鍵合與熱管理需共同審查。~Isolation, layer uniformity, bonding and thermal behavior require joint review.
''')
add('a007','污染與表面目標~Contaminants and surface targets|清洗路徑~Cleaning pathways|沖洗乾燥~Rinsing and drying|潔淨證據~Cleanliness evidence','clean purity mit','a008 a009',r'''
污染分類~Classify contaminants|粒子、金屬、有機物與原生氧化層需要不同證據。~Particles, metals, organics and native oxide need different evidence.
基底相容表~Build substrate compatibility tables|能去除污染的處理也可能侵蝕功能薄膜。~A contaminant-removing treatment may also attack functional films.
先後順序圖~Map cleaning order|前一步產生的表面狀態會影響後一步。~Each surface state affects the next cleaning step.
空白見證片~Choose blank witnesses|容器與搬運也會貢獻背景污染。~Containers and handling contribute background contamination.
潔淨程度指標~Select cleanliness metrics|粒子數不能代表金屬濃度。~Particle counts cannot represent metal concentration.
接觸角限制~Bound contact-angle interpretation|接觸角反映濕潤狀態，不能單獨證明無污染。~Contact angle reflects wetting but cannot prove contaminant absence.
化學選擇性~Assess chemical selectivity|選擇性需同時計入污染移除及基底損失。~Selectivity includes contaminant removal and substrate loss.
粒子附著力~Draw particle adhesion forces|粒子尺寸與表面化學會改變去除難度。~Particle size and surface chemistry alter removal difficulty.
邊界層更新~Analyze boundary-layer renewal|流場影響反應物供給與產物移除。~Flow affects reactant supply and product removal.
超音波副作用~Assess acoustic side effects|提升去粒能力也可能傷害細長結構。~Stronger acoustic removal may damage slender structures.
槽液老化~Track bath aging|溶解污染累積使新液與使用後槽液不同。~Accumulated contaminants make used baths differ from fresh chemistry.
單片與批次~Compare single-wafer and batch cleaning|批次共用液體需要考慮片間交叉污染。~Shared batch liquids require inter-wafer contamination analysis.
沖洗置換模型~Model rinse displacement|僅靠出口平均值可能漏掉滯留區。~Outlet averages can miss stagnant regions.
水質進入點~Check incoming rinse quality|清洗末段也可能由水質帶回污染。~Final rinsing can reintroduce contamination through water quality.
殘液乾燥痕~Interpret drying marks|水痕可來自殘液濃縮而非原本薄膜缺陷。~Drying marks can result from concentrated residue rather than film defects.
毛細倒塌~Assess capillary collapse|液面收縮力對高深寬比結構尤其重要。~Receding-meniscus forces matter strongly for high-aspect-ratio features.
等待時間控制~Control queue-time evidence|乾燥後的暴露時間會改變再吸附。~Post-dry exposure changes readsorption.
搬運接觸點~Trace handling contact points|背面接觸污染仍可透過設備傳播。~Backside contact contamination can spread through equipment.
前後粒子差~Calculate particle adders|比較必須匹配同一掃描範圍與門檻。~Before-after counts need matching scan areas and thresholds.
金屬分析空白~Audit metal-analysis blanks|低濃度量測需要容器空白與方法檢出限。~Trace analysis needs container blanks and detection limits.
表面損失圖~Map substrate loss|去污有效仍需證明功能材料損失可接受。~Effective cleaning still requires acceptable functional-material loss.
缺陷空間關聯~Correlate defect locations|位置關聯能引導排查，不能獨自證明因果。~Spatial correlation guides diagnosis but does not establish causality alone.
重工邊界~Define rework limits|反覆清洗的累積損失可能不可逆。~Repeated cleaning can cause irreversible cumulative loss.
潔淨交接單~Complete the cleanliness handoff|移除效果、表面變化及等待上限應一併交付。~Removal, surface change and queue limits belong in the handoff.
''')
add('a008','用水需求與污染~Water demand and contaminants|純化系統分工~Purification functions|循環與監測~Distribution and monitoring|異常及永續~Excursions and sustainability','purity filtration clean','a007 a009',r'''
界定使用點~Define points of use|沖洗、配液與設備用水可能有不同品質要求。~Rinsing, blending and utilities can require different water quality.
峰值與平均流量~Separate peak and average flow|只按平均需求設計會漏掉同步用水尖峰。~Average demand misses coincident usage peaks.
污染質量帳~Build contaminant mass balances|濃度必須與流量合用才能換算污染通量。~Concentration and flow jointly determine contaminant flux.
電阻率盲區~Identify resistivity blind spots|高電阻率不能排除非離子有機物或粒子。~High resistivity does not exclude neutral organics or particles.
TOC 指標~Interpret total organic carbon|TOC 是總量指標而不是個別化合物身分。~TOC measures aggregate carbon, not compound identity.
回用水分流~Segregate recovery streams|回收前需區分不同製程流的污染負荷。~Recovery requires segregation by process contaminant load.
前處理功能~Assign pretreatment functions|前處理保護後段膜與樹脂，不等於末端純化。~Pretreatment protects downstream media but is not final polishing.
逆滲透物料平衡~Balance reverse-osmosis streams|產水、濃水與進水必須符合質量守恆。~Permeate, concentrate and feed must satisfy mass balance.
離子交換突破~Interpret ion-exchange breakthrough|樹脂接近耗盡時出水變化可能早於總體失效。~Effluent changes can precede full resin exhaustion.
有機物分解~Assess organic-removal stages|分解有機物可能生成需再去除的離子。~Organic decomposition can produce ions needing subsequent removal.
脫氣模組~Evaluate degassing|溶解氣體與液中粒子使用不同去除機制。~Dissolved gases and particles require different removal mechanisms.
終端過濾~Review final filtration|標稱截留尺寸不是所有污染物的保證去除率。~Nominal retention size is not universal contaminant removal efficiency.
循環管網~Trace the recirculation loop|持續循環降低滯留但不能代替材料潔淨度。~Recirculation reduces stagnation but cannot replace material cleanliness.
死角支管~Find dead legs|低流速滯留區可成為品質波動來源。~Stagnant branches can become contamination sources.
壓差與濾芯~Interpret filter pressure drop|壓差上升可提示負載，低壓差不證明無旁通。~Rising pressure drop suggests loading; low drop does not exclude bypass.
使用點採樣~Design point-of-use sampling|中央水站合格不代表所有末端合格。~Central quality does not prove every outlet meets requirements.
感測器延遲~Account for sensor delay|採樣管滯留時間會延後警報所代表的事件。~Sample-line residence time delays the event represented by an alarm.
溫度補償~Review temperature compensation|電性讀值須與溫度及補償方法一起記錄。~Electrical readings need temperature and compensation metadata.
異常隔離區~Define excursion boundaries|受影響晶圓需依暴露時間窗回溯。~Affected wafers should be traced through the exposure time window.
維護沖洗證據~Verify maintenance flushing|更換零件後需確認釋出污染與背景恢復。~After replacement, check leachables and return to baseline.
多指標交叉驗證~Cross-check quality indicators|單一感測器失效不能由其自身趨勢排除。~A sensor trend cannot rule out failure of that same sensor.
回收率權衡~Assess recovery tradeoffs|提高回收率可能增加濃縮負荷及能耗。~Higher recovery can increase concentration and energy burden.
停機重啟~Plan restart qualification|停滯後重啟需要重新建立末端品質證據。~Restart after stagnation needs renewed outlet-quality evidence.
水務放行報告~Assemble water-system acceptance|品質、供應穩定、採樣及異常追溯須同時成立。~Acceptance needs quality, supply stability, sampling and excursion traceability.
''')
add('a009','污染源與路徑~Sources and pathways|空氣與微環境~Air and microenvironments|液體接觸鏈~Liquid-contact chains|缺陷歸因~Defect attribution','contam purity clean','a007 a010',r'''
建立污染源地圖~Map contamination sources|人員、設備、氣體、液體與載具都是可能來源。~People, tools, gases, liquids and carriers are possible sources.
尺寸與危害~Separate size and hazard|相同尺寸的不同污染物未必有相同電性影響。~Equal-sized contaminants can have different electrical effects.
粒子與分子~Distinguish particles and molecules|粒子過濾不能自動證明分子污染受控。~Particle filtration does not establish molecular-contamination control.
暴露劑量~Estimate contamination exposure|表面負荷同時取決於濃度與暴露時間。~Surface burden depends on concentration and exposure duration.
沉積與再懸浮~Trace deposition and resuspension|清潔表面的擾動可能重新釋出粒子。~Disturbing a surface can resuspend deposited particles.
監控片安排~Choose monitoring wafers|監控片需要與實際搬運歷程一致。~Monitor wafers need representative handling histories.
氣流方向~Map airflow direction|平均風速無法取代局部回流辨識。~Mean velocity does not identify local recirculation.
濾材功能~Compare filter functions|粒子濾材與分子吸附媒材的壽命判準不同。~Particle filters and molecular sorbents need different lifetime criteria.
壓差邊界~Set pressure-boundary evidence|壓差方向會影響污染跨區遷移。~Pressure gradients influence cross-zone contaminant transport.
微環境開口~Assess minienvironment openings|開口期間的短暫交換可能主導暴露。~Brief exchange during opening can dominate exposure.
FOUP 釋氣~Assess FOUP outgassing|載具材料可能儲存並釋出分子污染。~Carrier materials can store and release molecular contaminants.
濕度耦合~Study humidity coupling|吸附與化學反應可能隨濕度改變。~Adsorption and reactions can change with humidity.
容器浸出物~Audit container extractables|化學液潔淨度會受包材與接觸時間影響。~Chemical purity depends on packaging and contact duration.
管線顆粒脫落~Trace tubing particle shedding|機械擾動與維護可改變管線釋粒。~Mechanical disturbance and maintenance can change particle shedding.
閥件死腔~Locate valve dead volumes|局部滯留可能使末端比主流更髒。~Stagnant valve volumes can contaminate outlets beyond bulk levels.
濾芯旁通~Check filtration bypass|濾膜性能良好仍可能有密封失效旁通。~A sound membrane can coexist with seal-related bypass.
靜電與吸附~Link electrostatics and attraction|帶電表面可能增加粒子捕獲。~Charged surfaces can increase particle capture.
化學批次更換~Compare chemical-lot transitions|更換批次的短暫尖峰可能被長時間平均掩蓋。~Lot-transition spikes can disappear in long averages.
檢出限標示~Report detection limits|未檢出不等於污染濃度嚴格為零。~Nondetection does not imply exactly zero contamination.
空間缺陷圖~Register defect maps|缺陷位置須與設備座標及晶圓旋轉對齊。~Defect maps need tool-coordinate and wafer-rotation registration.
時間序列比對~Align event timelines|維護、換料及缺陷資料需要同一時間基準。~Maintenance, material changes and defects need a shared clock.
單因素隔離~Isolate a contamination hypothesis|同時換多個零件會使因果歸因困難。~Replacing many components together obscures causal attribution.
恢復與放行~Define recovery evidence|恢復背景須用獨立見證而不是只消除警報。~Recovery needs independent witnesses, not merely cleared alarms.
污染控制報告~Compile the control dossier|來源、傳輸、沉積與電性後果應分層呈現。~Report source, transport, deposition and electrical consequence separately.
''')
add('a010','搬運圖與產能~Transport graph and capacity|任務與交握~Tasks and handshakes|壅塞及故障~Congestion and faults|驗收與資料~Acceptance and data','amhs daifuku contam','a009 a098',r'''
辨識載具與批號~Identify carriers and lots|載具 ID 與晶圓批號不是同一資料欄位。~Carrier identity and wafer-lot identity are separate fields.
建立有向路網~Build the directed route graph|單向軌道的可達性不能由直線距離判斷。~Reachability on directed tracks differs from straight-line distance.
工具負載埠~Represent load ports|設備加工能力與載入埠容量需分開建模。~Process capacity and load-port capacity require separate models.
搬運需求矩陣~Build a transport-demand matrix|製程回訪使晶圓不是只走一次單向流水線。~Reentrant processing makes wafer flow more than one pass down a line.
儲位與緩衝~Allocate storage buffers|緩衝減少阻塞但增加在製品與等待。~Buffers reduce blocking but increase work in process and waiting.
搬運時間拆解~Decompose transport time|等待、行車、升降與交握各有不同改善途徑。~Queueing, travel, hoisting and handshakes need different remedies.
任務狀態機~Draw the task state machine|已派工、已取貨與已送達不可合併為一個狀態。~Assigned, picked and delivered are distinct states.
載入前交握~Validate the loading handshake|設備就緒與載具身分均需確認才可完成交接。~Handoff requires both equipment readiness and carrier identity.
路段保留~Reserve track segments|避免碰撞需要互斥資源，不只是最短路徑。~Collision avoidance needs exclusive resources beyond shortest routing.
優先權與飢餓~Balance priority and starvation|高優先任務不應無限阻斷普通批次。~High-priority tasks should not indefinitely starve ordinary lots.
重試冪等性~Make retries idempotent|重送訊息不能產生第二個實體取貨任務。~Repeated messages must not create duplicate physical pickup tasks.
超時狀態~Handle timeout ambiguity|超時可能是訊息遺失而不是動作未發生。~Timeout may mean lost acknowledgement rather than no action.
瓶頸利用率~Measure bottleneck utilization|高平均車速不能證明最繁忙路段不塞車。~High average speed does not exclude congestion on a busy segment.
路口壅塞~Inspect junction queues|合流點服務率限制會擴散到上游路段。~Junction service limits propagate queues upstream.
故障車阻擋~Model a blocked vehicle|停在單線區的故障車可改變整個路網可達性。~A failed vehicle on a single lane can change network reachability.
負載埠拒收~Recover from port rejection|目的端拒收需要可追溯的回退任務。~Destination rejection requires a traceable fallback task.
掉線與恢復~Reconcile network recovery|恢復時要核對實體位置與系統任務狀態。~Recovery must reconcile physical locations with task states.
地震或急停~Model emergency-stop states|安全停機後的重啟不能沿用未核對的任務。~Restart after a safety stop needs task reconciliation.
搬運振動~Assess transport vibration|峰值加速度與振動頻譜都可能影響脆弱載荷。~Peak acceleration and vibration spectra can affect fragile payloads.
粒子增量~Measure transport particle adders|潔淨搬運需比較匹配歷程的前後監控片。~Clean transport requires matched before-after monitor histories.
尾端延遲~Report tail latency|中位搬運時間可能掩蓋少數嚴重逾時。~Median transfer time can hide severe tail delays.
事件追溯~Audit event traceability|每個交接事件應保留來源、時間與唯一任務 ID。~Each handoff needs source, time and unique task identity.
離散事件模擬~Build a discrete-event experiment|相同到達序列才能公平比較不同派工策略。~Dispatch strategies need identical arrival traces for fair comparison.
搬運系統驗收~Accept the transport system|產能、錯送防護、故障恢復及潔淨度均需證據。~Acceptance needs throughput, misdelivery prevention, recovery and cleanliness evidence.
''')
add('a011','界面與氧化目的~Interface and oxidation purpose|成長動力學~Growth kinetics|厚度與電性~Thickness and electrical evidence|元件熱整合~Device thermal integration','oxide mit frontend','a012 a017',r'''
分辨成長與沉積~Separate growth and deposition|熱氧化消耗基板矽，外加沉積的材料來源不同。~Thermal oxidation consumes substrate silicon; deposition has another material source.
界面位置移動~Track the moving interface|氧化後原表面不等於新的矽氧界面位置。~The original surface differs from the final silicon-oxide interface.
閘氧與場氧~Separate gate and field oxide|電容控制與區域隔離使用不同設計目標。~Gate capacitance and field isolation have different design targets.
乾氧與濕氧~Compare dry and wet oxidation|氧化氣氛改變成長速率及薄膜特性。~Oxidizing ambient changes growth kinetics and film properties.
原生氧化前史~Record initial oxide history|初始氧化層會改變短時間成長的起點。~Initial oxide changes the starting condition for short growth.
清洗後等待~Assess the clean-to-oxidation delay|吸附與再氧化會改變最初界面。~Adsorption and reoxidation change the starting interface.
線性成長區~Identify the linear regime|薄層成長可能主要受界面反應限制。~Thin-film growth can be mainly interface-reaction limited.
拋物線成長區~Identify the parabolic regime|厚氧化層增加氧化物穿越的傳輸阻力。~Thicker oxide increases transport resistance through the oxide.
模型初始條件~Set model initial conditions|套用成長模型需帶入原有膜厚而非從零開始。~Growth models need the existing thickness as an initial condition.
晶向效應~Assess orientation effects|不同矽晶面可能呈現不同界面反應速率。~Different silicon planes can have different interface reaction rates.
摻雜效應~Assess doping effects|重摻雜區與未摻雜區不能直接共用同一成長曲線。~Heavily doped and undoped regions need not share growth curves.
應力耦合~Trace oxidation stress|氧化體積變化與周邊拘束共同形成應力。~Oxidation volume change and surrounding constraints generate stress.
橢偏膜厚~Interpret ellipsometric thickness|光學膜厚反演需要折射率與堆疊假設。~Optical thickness extraction requires index and stack assumptions.
截面校對~Cross-check section thickness|局部截面可校核光學模型但不能代表整片。~A local section checks optical models but not full-wafer uniformity.
電容等效厚度~Infer electrical thickness|介面層與量子效應可能使電容厚度不同於物理厚度。~Interfacial and quantum effects can separate electrical and physical thickness.
漏電曲線~Read leakage curves|比較漏電需控制面積、電場及量測極性。~Leakage comparisons need matched area, field and polarity.
界面陷阱指標~Inspect interface-trap evidence|C-V 頻率依賴可能含介面態與量測寄生影響。~C-V frequency dependence can include interface states and measurement parasitics.
擊穿分布~Analyze breakdown distributions|單一最佳樣本不能代表批次可靠度。~One best specimen cannot represent lot reliability.
熱預算累加~Accumulate thermal history|長時間氧化會同時改變先前的摻雜輪廓。~Long oxidation can also change earlier dopant profiles.
邊角氧化~Assess corner oxidation|二維曲率與應力使角落成長不同於平面。~Two-dimensional curvature and stress alter corner growth.
固定電荷~Separate fixed charge|固定電荷造成的電壓位移不等同於功函數差。~Fixed-charge voltage shifts differ from work-function differences.
氮化選項~Evaluate nitridation tradeoffs|介面工程必須同時評估漏電、陷阱與遷移率。~Interface engineering must consider leakage, traps and mobility together.
模型失效界線~State model limits|經典厚膜模型不能無條件外推到極薄介面。~Classical thick-film models cannot be unconditionally extrapolated to ultrathin interfaces.
閘氧驗收~Accept the gate oxide|厚度圖、介面、漏電與可靠度缺一不可。~Acceptance needs thickness mapping, interface quality, leakage and reliability.
''')
add('a012','介電層與電容~Dielectric and capacitance|表面循環~Surface cycles|三維覆蓋~Three-dimensional coverage|電性及整合~Electrical behavior and integration','ald highk oxide','a011 a013',r'''
物理厚度與 EOT~Separate thickness and EOT|較高介電常數可在相同電容下容許較厚物理膜。~Higher permittivity permits greater physical thickness at equal capacitance.
串聯介面電容~Calculate series interface capacitance|薄介面層仍可能主導整體等效氧化厚度。~A thin interfacial layer can dominate equivalent oxide thickness.
基底終端基團~Identify surface termination|表面官能基影響前驅物吸附與成核。~Surface functional groups affect precursor adsorption and nucleation.
前驅物相容性~Review precursor compatibility|揮發性、穩定性及殘留物需一起考慮。~Volatility, stability and residues must be considered together.
成核延遲~Measure nucleation delay|最初幾個循環的成長量可能不同於穩態。~Initial-cycle growth can differ from steady-state growth.
熱式與電漿式~Compare thermal and plasma ALD|活性種來源不同，損傷與熱負荷也不同。~Different reactive-species sources change damage and thermal burden.
第一半反應~Trace the first half-reaction|飽和吸附後增加暴露不應無限增加單循環成長。~After saturation, exposure should not indefinitely increase cycle growth.
清除殘留氣體~Separate purge from reaction|不足的清除會讓氣相反應混入表面循環。~Insufficient purge allows gas-phase reactions into surface cycling.
第二半反應~Trace the second half-reaction|共反應物需轉化已吸附物並建立下一循環表面。~The co-reactant transforms adsorbates and prepares the next-cycle surface.
飽和曲線~Construct saturation curves|證明飽和需要掃描暴露量而不是只看單一點。~Saturation needs an exposure sweep rather than one operating point.
循環與膜厚~Relate cycles to thickness|線性外推需扣除成核截距並檢查成長模式。~Linear extrapolation needs nucleation intercept and growth-mode checks.
溫度窗~Identify the temperature window|太低可能冷凝，太高可能熱分解。~Low temperature can cause condensation and high temperature decomposition.
深槽反應物耗盡~Assess feature-scale depletion|入口飽和不代表高深寬比底部已飽和。~Entrance saturation does not prove bottom saturation in deep features.
側壁與底部比~Compare sidewall and bottom thickness|覆蓋率須明確指定厚度比的兩個位置。~Conformality ratios need explicit measurement locations.
成分均勻性~Map composition uniformity|厚度均勻不保證雜質與化學鍵分布均勻。~Uniform thickness does not guarantee uniform impurity or bonding composition.
針孔與漏電~Connect pinholes and leakage|少數局部缺陷可主導大面積漏電。~A few local defects can dominate area-scale leakage.
晶化風險~Assess crystallization|後續退火可能改變晶界與漏電路徑。~Later annealing can change grain boundaries and leakage pathways.
殘碳分析~Interpret residual carbon|成分量測深度與背景需跟殘留濃度一起報告。~Residual concentration needs measurement-depth and background metadata.
介面偶極~Trace interface dipoles|介面化學可能同時改變有效功函數。~Interface chemistry can also change effective work function.
遷移率代價~Assess mobility tradeoffs|高電容增益需與散射及陷阱造成的劣化比較。~Capacitance gain must be compared with scattering and trap penalties.
閘極填充空間~Budget gate-cavity volume|介電層變厚會消耗金屬可用填充空間。~Thicker dielectric consumes available metal-fill volume.
偏壓穩定性~Assess bias stability|初始良好電性不等於長時間偏壓穩定。~Good initial electrical behavior does not prove long-term bias stability.
配方變更見證~Define change-control witnesses|換前驅物要重新驗證覆蓋、雜質與可靠度。~A precursor change requires renewed coverage, impurity and reliability checks.
高介電層放行~Release the high-k layer|EOT、漏電、陷阱及三維覆蓋應共同審查。~Review EOT, leakage, traps and 3D coverage jointly.
''')
add('a013','能帶與閘極~Band alignment and gates|材料堆疊~Material stacks|選擇性加工~Selective processing|閾值與可靠度~Threshold and reliability','highk ald scaling','a012 a023',r'''
定義真空功函數~Define vacuum work function|金屬真空功函數不必等於器件中的有效功函數。~Vacuum work function need not equal effective work function in a device.
平帶條件~Draw flat-band conditions|平帶電壓也受介面電荷影響。~Flat-band voltage is also affected by interface charge.
NMOS 與 PMOS~Separate NMOS and PMOS targets|互補元件需要不同閾值設定策略。~Complementary devices need different threshold-setting strategies.
閘介電層串聯~Include the dielectric stack|相同金屬在不同介面堆疊可有不同有效功函數。~The same metal can have different effective work functions in different stacks.
閾值抽取定義~Choose threshold extraction|不同抽取方法會產生不可直接混比的閾值。~Different extraction methods can yield noncomparable thresholds.
厚度空間預算~Budget gate-stack thickness|奈米片間隙限制功函數金屬與填充金屬總厚度。~Nanosheet gaps limit total work-function and fill-metal thickness.
薄金屬連續性~Assess thin-metal continuity|極薄金屬可能未形成連續覆蓋。~An ultrathin metal layer may not be continuous.
介面偶極形成~Trace interface dipoles|介面反應可產生額外能帶位移。~Interface reactions can create additional band shifts.
氮含量與成分~Compare nitrogen and composition|材料名稱相同不代表化學計量與功函數相同。~A shared material name does not guarantee equal stoichiometry or work function.
晶粒與取向~Assess grain orientation|多晶金屬取向分布可帶來局部功函數差。~Polycrystalline orientation can introduce local work-function differences.
沉積成核~Inspect nucleation|初始成核差異會改變薄層完整性與界面。~Initial nucleation changes thin-layer integrity and interface behavior.
熱處理重分布~Track thermal redistribution|元素擴散會改變原先設計的閘堆疊。~Element diffusion can alter the intended gate stack.
區域保護層~Plan regional protection|選擇處理一種元件時需保護另一種閘堆疊。~Processing one device polarity requires protecting the other stack.
金屬回蝕~Assess metal recess|回蝕深度誤差可能破壞有效功函數層覆蓋。~Recess errors can compromise work-function-layer coverage.
選擇性去除~Check selective removal|去除上層金屬仍須量化下層損失。~Removing an upper metal still requires lower-layer loss measurement.
窄腔填充~Inspect narrow-cavity fill|外部封口可能掩蓋內部空洞。~Premature closure can conceal internal voids.
閘極電阻~Separate gate resistance|低閘電阻與正確閾值是不同驗收項目。~Low gate resistance and correct threshold are separate criteria.
金屬殘留短路~Locate residual-metal bridges|局部殘留可能在電性上連接原本隔離的閘。~Local residues can electrically connect isolated gates.
C-V 與 I-V~Cross-check C-V and I-V|兩種量測對介面與通道的敏感度不同。~C-V and I-V have different interface and channel sensitivities.
閾值空間圖~Map threshold variation|均值合格仍可能有尾端分布問題。~An acceptable mean can coexist with distribution-tail failures.
溫度依賴~Compare temperature dependence|不同溫度的閾值不能忽略量測條件直接比較。~Threshold comparisons across temperatures need matched measurement definitions.
偏壓老化~Track bias aging|閾值漂移需要與初始製程偏移分開。~Aging drift must be separated from initial process offsets.
雙極性整合~Review dual-polarity integration|NMOS 改善不應以未檢查的 PMOS 退化交換。~NMOS improvement must not hide untested PMOS degradation.
金屬閘極驗收~Accept the metal gate|功函數、覆蓋、電阻、分布及老化需聯合判讀。~Jointly assess work function, coverage, resistance, distributions and aging.
''')
add('a014','佈植目的與輪廓~Implant purpose and profiles|束流與遮罩~Beam and masks|損傷與活化~Damage and activation|量測及整合~Measurement and integration','implant implantmask frontend','a015 a006',r'''
劑量與濃度~Separate dose and concentration|面劑量與體濃度的單位及物理意義不同。~Areal dose and volume concentration have different units and meanings.
摻雜種類~Choose dopant roles|摻雜元素與晶格佔位共同決定電性作用。~Dopant species and lattice occupation jointly determine electrical behavior.
投影射程~Read projected range|射程平均值不能代表整個深度分布尾端。~Mean projected range does not represent the depth-distribution tail.
能量與深度~Relate energy and depth|能量影響深度，也同時影響損傷分布。~Energy affects both depth and damage distribution.
接面位置~Define junction depth|接面需由摻雜輪廓與背景濃度交會判斷。~Junction depth depends on profile intersection with background doping.
遮罩止擋條件~Set mask-stopping evidence|遮罩厚度須考慮射程展寬與薄弱區。~Mask thickness must account for range spread and weak regions.
質量分析~Trace mass selection|電荷質量比選擇有助區分束流物種。~Mass-to-charge selection helps distinguish beam species.
束流積分~Integrate beam dose|電流積分轉成劑量需要電荷態與照射面積。~Converting integrated current to dose requires charge state and area.
掃描均勻性~Assess scan uniformity|掃描速度與束流分布共同決定面劑量。~Scan speed and beam profile jointly determine areal dose.
晶向通道效應~Assess channeling|沿晶體通道的離子可能產生較深尾端。~Ions aligned with crystal channels can create deeper tails.
傾角與陰影~Assess tilt and shadowing|抑制通道效應的角度也可能增加圖案遮蔽。~Angles suppressing channeling can increase pattern shadowing.
晶圓充電~Assess wafer charging|絕緣結構上的電荷累積可能造成損傷。~Charge accumulation on insulating structures can cause damage.
碰撞損傷~Map collision damage|佈植後的化學濃度不代表可用載子濃度。~Post-implant chemical concentration is not active carrier concentration.
非晶化區~Identify amorphized regions|非晶層與晶體的退火恢復機制不同。~Amorphous and crystalline regions recover differently during annealing.
暫態增強擴散~Identify transient enhanced diffusion|過量點缺陷可在退火初期增強摻雜擴散。~Excess point defects can enhance early anneal diffusion.
活化比例~Estimate activation fraction|活化比例需化學與電性濃度的配對證據。~Activation needs paired chemical and electrical concentration evidence.
聚集與失活~Assess clustering and deactivation|更多摻雜原子未必產生等比例自由載子。~More dopant atoms need not produce proportional free carriers.
遮罩去除風險~Review mask stripping|高劑量佈植可能改變光阻移除難度。~High-dose implantation can change resist-removal difficulty.
SIMS 深度校準~Calibrate SIMS depth|濺鍍時間轉深度需材料相關校準。~Converting sputter time to depth needs material-dependent calibration.
片電阻判讀~Interpret sheet resistance|片電阻綜合濃度、遷移率與活化層厚度。~Sheet resistance integrates concentration, mobility and active-layer depth.
接面漏電~Inspect junction leakage|低片電阻不保證接面損傷已消除。~Low sheet resistance does not prove junction damage removal.
多重能量設計~Compare multi-energy profiles|多次佈植的輪廓需先在同一深度座標相加。~Multiple implant profiles must be summed on a shared depth coordinate.
熱歷程追蹤~Track subsequent heat treatments|佈植驗收需考慮後續製程的再次擴散。~Implant acceptance must consider diffusion during later processing.
佈植批次審查~Review the implant lot|劑量、深度、均勻、損傷及活化缺一不可。~Review dose, depth, uniformity, damage and activation together.
''')
add('a015','退火需求~Annealing requirements|升降溫控制~Heating and cooling|電性與形貌~Electrical and structural outcomes|製程窗口~Process-window evidence','rtp implant frontend','a014 a016',r'''
活化與擴散~Separate activation and diffusion|活化提高載子可用性，擴散改變空間分布。~Activation changes carrier availability while diffusion changes spatial distribution.
溫度時間軌跡~Draw temperature-time trajectories|峰值溫度相同不代表總熱暴露相同。~Equal peak temperature does not imply equal thermal exposure.
熱預算積分~Construct a thermal-budget integral|擴散預算應考慮溫度依賴係數而非只加時間。~Diffusion budgets need temperature-dependent coefficients, not time alone.
損傷恢復~Define damage-recovery targets|缺陷修復與摻雜活化可有不同時間尺度。~Damage repair and dopant activation can have different timescales.
前段堆疊~Inventory the incoming stack|表面材料會改變吸收、發射與熱傳。~Surface materials change absorption, emission and heat transfer.
氣氛角色~Assign ambient functions|氣氛可影響氧化與界面，不只是傳熱背景。~Ambient affects oxidation and interfaces beyond thermal transport.
燈區分配~Allocate heating zones|多區加熱需要處理區域之間的熱耦合。~Multizone heating must account for thermal coupling.
高溫計發射率~Assess pyrometer emissivity|亮度溫度取決於材料發射率模型。~Brightness temperature depends on the emissivity model.
背面狀態~Check backside conditions|背面薄膜與粗糙度可能改變溫度讀值。~Backside films and roughness can alter temperature readings.
升溫斜率~Compare ramp rates|快速升溫會改變晶圓內外的暫態溫差。~Fast ramps change transient temperature gradients.
旋轉與均勻~Assess rotation averaging|旋轉能平均方位誤差但不能消除所有徑向偏差。~Rotation averages angular errors but not all radial deviations.
冷卻尾端~Include the cooling tail|降溫期間仍可能累積擴散。~Diffusion can continue during cooling.
片電阻前後~Compare sheet resistance|片電阻下降需與接面深度同時比較。~Reduced sheet resistance should be assessed with junction depth.
濃度輪廓展寬~Measure profile broadening|較深的尾端可能使短通道控制變差。~Deeper profile tails can degrade short-channel control.
接面漏電圖~Map junction leakage|漏電圖可揭示局部殘留損傷。~Leakage maps can reveal localized residual damage.
滑移線~Inspect slip lines|熱應力可能造成晶體塑性缺陷。~Thermal stress can generate crystalline slip defects.
翹曲回復~Measure bow evolution|退火前後形貌變化需使用一致支撐條件。~Before-after shape comparisons need consistent support conditions.
圖案吸收差~Assess pattern-dependent absorption|裸晶圓均勻性不能保證圖案晶圓均勻性。~Blanket-wafer uniformity does not prove patterned-wafer uniformity.
峰值與停留權衡~Trade peak temperature against dwell|更短停留不能無條件抵銷更高峰值的所有效應。~Shorter dwell does not universally cancel all effects of higher peaks.
不確定度傳播~Propagate temperature uncertainty|小溫度誤差可放大為擴散或活化差異。~Small temperature errors can amplify into diffusion or activation changes.
監控片轉移~Transfer monitor calibration|監控片光學性質需與產品晶圓相容。~Monitor optical properties should represent product wafers.
批間漂移~Detect run-to-run drift|燈老化或腔體狀態變化可造成漸進漂移。~Lamp aging and chamber changes can create gradual drift.
跨模組交接~Handoff thermal constraints|閘介電層、接觸與應力層皆有各自熱限制。~Gate dielectrics, contacts and stress layers have distinct thermal limits.
退火窗口放行~Accept the annealing window|活化、擴散、漏電及結構損傷需共同滿足。~Activation, diffusion, leakage and structural damage must all meet criteria.
''')
add('a016','雷射熱歷程~Laser thermal history|光束與掃描~Beam and scanning|局部反應~Localized response|圖案相容性~Pattern compatibility','laser rtp implant','a015 a029',r'''
毫秒與奈秒~Separate millisecond and nanosecond regimes|不同脈衝時間不能視為同一熱處理。~Different pulse durations cannot be treated as the same thermal process.
光吸收深度~Assess optical penetration|光學吸收與熱擴散共同決定加熱深度。~Optical absorption and thermal diffusion jointly set heated depth.
熱擴散尺度~Estimate thermal diffusion length|熱擴散長度隨時間平方根改變。~Thermal diffusion length scales with the square root of time.
峰值與積分能量~Separate peak and integrated energy|相同能量可能有不同峰值溫度。~Equal energy can produce different peak temperatures.
熔融與非熔融~Distinguish melting regimes|是否熔融會改變再結晶及摻雜重分布機制。~Melting changes recrystallization and dopant redistribution mechanisms.
熱敏感下層~Identify sensitive underlying layers|表面短暫加熱仍需檢查下層最高溫度。~Brief surface heating still requires subsurface peak-temperature assessment.
光斑強度剖面~Read the beam profile|平均功率不能代表光斑內局部強度。~Mean power does not describe local beam intensity.
掃描速度~Relate scan speed and dwell|固定光斑寬度下掃速決定局部暴露時間。~With fixed beam width, scan speed determines local dwell.
重疊帶~Assess scan overlap|相鄰掃描重疊區可能接受不同累計暴露。~Adjacent scan overlaps can receive different cumulative exposure.
邊緣轉向~Inspect scan turnarounds|掃描加減速區應與有效晶圓區分開。~Acceleration regions must be distinguished from the usable wafer area.
溫度回授延遲~Account for thermal-feedback delay|感測延遲可能錯過短暫溫度峰值。~Sensor delay can miss short temperature peaks.
功率漂移~Track laser-power drift|校準與實際處理需使用同一光路狀態。~Calibration and processing need consistent optical-path conditions.
摻雜活化~Evaluate dopant activation|短熱歷程可改變活化與擴散的相對程度。~Short thermal histories change the balance between activation and diffusion.
接觸電阻改善~Assess contact-resistance change|總串聯電阻下降不能自動歸因於接觸界面。~Lower total series resistance cannot automatically be attributed to the contact interface.
再結晶前緣~Trace recrystallization fronts|結晶前緣與缺陷位置共同影響最終品質。~Recrystallization fronts and defect positions jointly affect final quality.
表面粗糙化~Inspect surface roughening|電性改善也可能伴隨表面形貌劣化。~Electrical improvement can coexist with surface degradation.
應力尖峰~Assess transient stress|局部急熱可產生與平均溫升不同的應力峰值。~Localized rapid heating can create stress peaks unlike average warming.
量測空間解析~Check spatial resolution|量測光斑過大會平均掉掃描邊界異常。~Large measurement spots can average out scan-boundary anomalies.
金屬圖案吸收~Compare patterned absorption|反射率差異使不同區塊接受不同熱負荷。~Reflectivity variations give different blocks different thermal loads.
圖案密度分組~Stratify pattern density|需分組比較圖案密度與溫度或電性偏移。~Compare temperature or electrical shifts by pattern-density group.
多次通過~Assess repeated passes|多次低能量不保證等同單次高能量。~Several low-energy passes need not equal one high-energy pass.
下層見證結構~Choose buried-layer witnesses|只量表面活化無法證明下層未受損。~Surface activation alone cannot prove buried layers remain undamaged.
失效區回溯~Trace failed scan regions|缺陷圖需轉到掃描時間與光斑座標。~Defect maps should be registered to scan time and beam coordinates.
雷射退火審查~Review laser-anneal evidence|活化收益需與熱峰值、均勻性及下層相容性一起評估。~Assess activation gain with thermal peaks, uniformity and buried-layer compatibility.
''')
add('a017','爐管與邊界~Furnace and boundaries|熱場與傳輸~Thermal field and transport|擴散輪廓~Diffusion profiles|均勻性驗收~Uniformity acceptance','implant frontend oxide','a011 a015',r'''
批次位置圖~Map batch positions|前中後片位是不同的熱與流體採樣位置。~Front, middle and rear slots sample different thermal and flow conditions.
晶舟載量~Specify boat loading|裝片數量及間距改變熱容量與流場。~Wafer count and spacing change thermal mass and flow.
爐溫與片溫~Separate furnace and wafer temperature|爐壁設定值不能直接當作晶圓瞬時溫度。~Wall setpoint is not instantaneous wafer temperature.
固定源與有限源~Separate constant and finite sources|邊界供應條件決定擴散解的形式。~Source boundary conditions determine the diffusion solution.
濃度守恆~Check concentration conservation|有限劑量擴散應保持總量，除非另有損失通量。~Finite-dose diffusion conserves total dose unless a loss flux is specified.
熱預算累計~Accumulate diffusion budgets|非恆溫歷程需積分溫度相關擴散係數。~Nonisothermal histories require integrating temperature-dependent diffusivity.
加熱區校準~Calibrate heating zones|各區控制需要考慮相鄰區熱耦合。~Zone control requires adjacent-zone thermal coupling.
端部熱損~Assess end losses|爐管入口出口常與中心區有不同熱邊界。~Tube ends often have different thermal boundaries from the center.
氣體耗盡~Track gas depletion|反應物沿爐長的消耗可造成片位差。~Reactant consumption along the furnace can cause slot dependence.
載入暫態~Model loading transients|載入冷晶舟會暫時擾動穩態熱場。~Loading a cold boat temporarily disturbs a steady thermal field.
升降溫對稱性~Compare heating and cooling|升溫與降溫的熱傳條件不必對稱。~Heating and cooling heat-transfer conditions need not be symmetric.
空載與滿載~Compare empty and full loads|空載均溫不能代替滿載產品驗證。~Empty-furnace uniformity cannot replace loaded validation.
Fick 通量方向~Draw Fickian flux|擴散通量由濃度梯度而不是濃度本身決定。~Diffusion flux depends on concentration gradient rather than concentration alone.
高斯有限源~Model a finite-source Gaussian|輪廓展寬時峰值降低以維持總劑量。~A finite-source profile broadens while its peak falls to conserve dose.
互補誤差函數~Model constant-surface diffusion|維持表面濃度需要持續供應摻雜原子。~Constant surface concentration requires continued dopant supply.
接面交點~Locate the junction intersection|接面深度需與基底背景濃度一起決定。~Junction depth is determined with the background doping.
濃度依賴擴散~Identify concentration dependence|高摻雜時常數擴散係數可能失去適用性。~Constant diffusivity can fail at high doping.
缺陷促進擴散~Assess defect-assisted diffusion|點缺陷前史會改變有效擴散行為。~Point-defect history changes effective diffusion behavior.
徑向與軸向圖~Separate radial and axial maps|片內徑向變異與片間軸向變異應分開報告。~Report within-wafer radial and slot-to-slot axial variation separately.
片電阻映射~Map sheet resistance|同一電阻結果可能來自不同濃度輪廓。~Equal resistance can arise from different concentration profiles.
校準熱電偶~Assess thermocouple calibration|感測器漂移可能被誤判為製程漂移。~Sensor drift can be mistaken for process drift.
設備清潔週期~Assess maintenance cycles|管壁沉積狀態可能影響批次間重現性。~Tube-wall deposits can affect run-to-run repeatability.
最差片位~Select worst-case slots|中心片合格不代表端部片位合格。~Center-wafer acceptance does not prove end-slot acceptance.
批次擴散驗收~Accept batch diffusion|熱場、濃度輪廓、位置差異及量測校準需一併審查。~Review thermal field, profiles, position effects and calibration together.
''')
add('a018','隔離幾何~Isolation geometry|溝槽與襯層~Trench and liner|填充與平坦化~Fill and planarization|漏電與應力~Leakage and stress','frontend legacy oxide','a011 a021',r'''
主動區邊界~Draw active-area boundaries|隔離區定義元件間電性邊界而非閘長。~Isolation defines electrical boundaries between devices, not gate length.
溝槽深度預算~Budget trench depth|隔離深度需與接面及漏電路徑一起評估。~Isolation depth must be assessed against junctions and leakage paths.
硬遮罩分工~Assign hard-mask functions|遮罩要兼顧蝕刻保護及後續平坦化停止。~Masks may provide both etch protection and a planarization stop.
襯墊氧化層~Assess pad oxide|襯墊層可改變應力傳遞與移除選擇性。~Pad layers alter stress transfer and removal selectivity.
圖案密度~Compare pattern density|稀疏與密集區可能有不同蝕刻及填充負載。~Sparse and dense regions can have different etch and fill loading.
邊角電場~Locate corner fields|尖角可能集中電場而增加局部漏電。~Sharp corners can concentrate fields and increase local leakage.
溝槽側壁角~Measure trench sidewall angle|側壁形狀會改變入口封閉與填充風險。~Sidewall shape changes opening closure and fill risk.
底部殘留~Inspect trench-bottom residue|殘留物可能阻礙襯層與填充界面。~Residues can compromise liner and fill interfaces.
蝕刻損傷~Assess etch damage|幾何正確仍可能存在電漿損傷。~Correct geometry can still contain plasma damage.
角落圓化~Compare corner rounding|圓化會改變電場及可用主動區尺寸。~Rounding changes fields and usable active dimensions.
襯層氧化消耗~Budget liner oxidation|襯層成長會消耗溝槽壁矽並改變寬度。~Liner growth consumes silicon walls and changes trench width.
襯層應力~Inspect liner stress|氧化與拘束產生的應力會傳到鄰近通道。~Oxidation and confinement stress can reach adjacent channels.
底部與側壁成長~Compare bottom and sidewall growth|不均勻成長可能造成入口先封閉。~Uneven growth can close the opening prematurely.
接縫空洞~Identify seams and voids|表面平坦不保證溝槽內部無空洞。~A flat surface does not prove void-free trench fill.
填充緻密化~Assess fill densification|退火收縮可能改變應力及表面凹陷。~Anneal shrinkage can change stress and surface recess.
CMP 停止層~Define the CMP stop|停止層剩餘量必須與過拋光風險一起考量。~Remaining stop-layer thickness must be assessed with overpolish risk.
碟形與侵蝕~Separate dishing and erosion|局部填充凹陷與大範圍材料侵蝕不同。~Local fill recess differs from broad-area erosion.
隔離高度~Measure isolation height|隔離頂部高度會影響後續閘堆疊形貌。~Isolation height affects subsequent gate-stack topography.
窄寬效應~Assess narrow-width effects|通道靠近隔離邊界時邊緣影響比例增加。~Edge effects become proportionally larger near isolation boundaries.
寄生通道~Trace parasitic channels|隔離邊緣可能形成不同於主通道的導通路徑。~Isolation edges can support conduction distinct from the main channel.
漏電測試結構~Choose isolation test structures|元件間隔離需要跨隔離區的測試配置。~Interdevice isolation needs test structures spanning the isolation region.
應力距離效應~Assess distance-to-isolation stress|相同元件尺寸可能因到隔離邊界距離不同而有不同表現。~Equal devices can differ because of distance to isolation boundaries.
截面抽樣~Choose section locations|需包含密集、稀疏及最窄溝槽。~Sections should include dense, sparse and narrowest trenches.
STI 整合放行~Accept STI integration|填充、平坦、漏電與通道應力需共同符合要求。~Fill, planarity, leakage and channel stress require joint acceptance.
''')
add('a019','應變與輸運~Strain and transport|應力來源~Stress sources|量測與校準~Measurement and calibration|效能及可靠度~Performance and reliability','epi strain scaling','a020 a022',r'''
應力與應變~Separate stress and strain|應力是力學載荷，應變是相對形變。~Stress describes loading while strain describes relative deformation.
通道晶向~Register channel orientation|遷移率對應變的反應依賴晶向與載子種類。~Mobility response depends on orientation and carrier type.
拉伸與壓縮~Compare tension and compression|同一應變符號對電子與電洞未必同樣有利。~One strain sign need not benefit electrons and holes equally.
張量分量~Resolve strain components|單一數值不能代表完整三維應變。~One scalar cannot represent full three-dimensional strain.
基準元件~Choose a reference device|比較需維持幾何、電壓與接觸條件一致。~Comparisons require matched geometry, voltage and contacts.
效能指標~Separate mobility and drive current|驅動電流還受到串聯電阻與電容限制。~Drive current is also constrained by series resistance and capacitance.
嵌入式源汲極~Trace embedded stressors|源汲極材料晶格差可透過拘束把應力傳入通道。~Source-drain lattice mismatch can transfer stress into a constrained channel.
接觸蝕刻停止層~Assess stress liners|應力薄膜的效果依賴厚度、覆蓋及幾何。~Stress-liner effects depend on thickness, coverage and geometry.
緩衝層鬆弛~Assess buffer relaxation|緩衝層鬆弛與缺陷生成需要一起評估。~Buffer relaxation must be considered alongside defect generation.
隔離區拘束~Include isolation constraints|隔離材料的拘束會改變通道應變分布。~Isolation constraints change channel strain distribution.
圖案切割~Compare patterned relaxation|圖案化後自由邊界增加，應變可能部分釋放。~Patterning introduces free boundaries that can release strain.
熱膨脹失配~Assess thermal mismatch|冷卻過程的膨脹係數差可形成額外應力。~Thermal-expansion mismatch during cooling adds stress.
拉曼位移~Interpret Raman shifts|峰位變化也需排除溫度及成分影響。~Peak shifts require separating temperature and composition effects.
XRD 倒易空間~Read reciprocal-space maps|成分與鬆弛不能只由單一峰位置唯一決定。~One peak position does not uniquely determine composition and relaxation.
局部 TEM 應變~Interpret local strain maps|局部薄片製備可能改變原結構拘束。~Thin-lamella preparation can change the original constraints.
有限元素邊界~Set finite-element boundaries|錯誤固定邊界可能人為放大通道應力。~Incorrect fixed boundaries can artificially amplify channel stress.
網格收斂~Check mesh convergence|尖角應力峰值需檢查網格依賴。~Corner stress peaks require mesh-dependence checks.
量測與模擬對齊~Register measurement and simulation|比較需採相同空間平均範圍及方向。~Comparisons need matching spatial averaging and directions.
有效遷移率~Extract effective mobility|抽取結果需控制閘電容與串聯電阻假設。~Extraction depends on gate-capacitance and series-resistance assumptions.
漏電代價~Assess leakage tradeoffs|提高導通電流仍需維持關斷電流限制。~Higher on-current must still satisfy off-current constraints.
接面缺陷~Inspect junction defects|增加失配可能帶來鬆弛缺陷及漏電。~Greater mismatch can introduce relaxation defects and leakage.
熱穩定性~Assess thermal stability|後續熱循環可能改變應變保持程度。~Later thermal cycles can change retained strain.
版圖相依性~Assess layout dependence|鄰近結構可能改變相同元件的應力環境。~Neighboring structures can change stress around otherwise equal devices.
應變整合結論~Review strain integration|需將輸運收益與缺陷、漏電及版圖變異一起呈現。~Report transport gains with defects, leakage and layout variation.
''')
add('a020','選擇性與晶格~Selectivity and lattice|表面與成長~Surface and growth|成分及形貌~Composition and morphology|接觸與整合~Contacts and integration','epi sige selective','a019 a028',r'''
選擇性定義~Define selectivity|在矽上成長且在介電層抑制成核是兩個需驗證的條件。~Growth on silicon and suppressed dielectric nucleation both need evidence.
鍺比例~Set germanium fraction|鍺比例同時影響晶格、能帶及材料穩定性。~Germanium fraction affects lattice, bands and material stability.
種晶表面~Identify seed surfaces|殘氧化層會阻礙預期晶體延續。~Residual oxide impedes intended crystalline continuation.
開口幾何~Define opening geometry|側壁角及暴露晶面會影響最終晶面形貌。~Sidewall angle and exposed planes affect final facets.
摻雜與成長~Couple doping and growth|原位摻雜可能改變成長動力學。~In-situ doping can change growth kinetics.
熱預算限制~Set thermal-budget bounds|鄰近閘與底層材料限制可採用的熱歷程。~Adjacent gates and underlying materials constrain thermal history.
表面前清潔~Assess pre-epitaxy cleaning|清潔需移除阻礙物而保留種晶幾何。~Cleaning must remove barriers while preserving seed geometry.
成長與蝕刻競爭~Balance deposition and etching|選擇性可來自成長與去除速率的競爭。~Selectivity can arise from competing growth and removal rates.
介電層成核延遲~Assess dielectric nucleation delay|短時間選擇性不證明長時間仍無寄生成核。~Short-term selectivity does not prove absence of later parasitic nuclei.
圖案負載~Assess pattern loading|不同開口密度可能改變局部反應物供應。~Opening density can change local reactant availability.
晶面演化~Track facet evolution|晶面成長速率差會改變截面外形。~Different facet growth rates change cross-section shape.
相鄰結構合併~Inspect coalescence|兩側成長前緣相遇可能留下晶體缺陷。~Merging growth fronts can leave crystalline defects.
鍺深度分布~Map germanium depth profiles|表面平均成分不能代表整層成分梯度。~Mean surface composition cannot represent a depth gradient.
摻雜活化~Assess dopant activation|化學摻雜濃度與活化濃度需分開量測。~Chemical and activated dopant concentrations need separate measurements.
應變保持~Measure retained strain|成長更厚不一定保留更多彈性應變。~Thicker growth need not retain more elastic strain.
失配位錯~Locate misfit dislocations|位錯可釋放應變並形成漏電來源。~Dislocations can relax strain and introduce leakage paths.
表面粗糙化~Inspect surface roughening|高成長速率可能伴隨形貌失控。~High growth rate can coexist with morphology degradation.
選擇性檢出限~Report selectivity detection limits|未看到寄生核需附檢測面積及解析度。~No observed nuclei requires stated inspection area and resolution.
接觸金屬反應~Assess metal reaction|接觸形成後的界面成分可能不同於原磊晶表面。~The contact interface can differ from the original epitaxial surface.
接觸面積預算~Budget contact area|晶面形貌會改變可利用的接觸面積。~Facet geometry changes available contact area.
奈米片端點~Analyze nanosheet endpoints|每層奈米片的暴露端點可能有不同成長條件。~Each nanosheet endpoint can experience different growth conditions.
後續選蝕耐受~Assess later selective-etch survival|源汲極需要在犧牲層移除時被保護。~Source-drain material needs protection during sacrificial-layer removal.
片內差異~Map across-wafer differences|成分、厚度及缺陷需在一致座標下比較。~Compare composition, thickness and defects in shared coordinates.
SiGe 模組交接~Complete the SiGe handoff|選擇性、活化、應變與接觸需求需共同驗收。~Accept selectivity, activation, strain and contact requirements jointly.
''')
add('a021','CMOS 功能與隔離~CMOS function and isolation|閘與接面~Gates and junctions|接觸及互連~Contacts and interconnects|電路與良率~Circuit and yield','mit frontend highk','a018 a022',r'''
互補反相器~Draw a complementary inverter|NMOS 與 PMOS 的連接決定靜態邏輯功能。~NMOS and PMOS connectivity determines static logic function.
井區與基板~Assign wells and substrate|不同極性元件需要適當的井及本體接點。~Different polarities need appropriate wells and body contacts.
遮罩層次~Map mask hierarchy|不同遮罩分別定義主動區、閘、接觸與配線。~Separate masks define active areas, gates, contacts and wiring.
隔離與寄生~Map isolation and parasitics|隔離不足可能產生原電路圖未畫出的路徑。~Insufficient isolation can create paths absent from the intended schematic.
閂鎖路徑~Trace latch-up paths|寄生雙極路徑取決於井與基板電阻及接點。~Parasitic bipolar paths depend on well and substrate resistance and contacts.
熱順序約束~Order thermal constraints|高溫步驟會改變已形成的摻雜及薄膜。~High-temperature steps modify existing dopants and films.
閘介電層~Assess gate dielectric|閘電容、漏電與可靠度是不同需求。~Gate capacitance, leakage and reliability are distinct needs.
閘長轉移~Track gate-length transfer|光阻尺寸與最終電性通道長度不同。~Resist dimensions differ from final electrical channel length.
延伸接面~Place source-drain extensions|淺延伸接面在電場與串聯電阻間取捨。~Shallow extensions trade electric-field control against series resistance.
側壁間隔層~Define sidewall spacers|間隔層把後續接面位置與閘邊緣分開。~Spacers separate later junction placement from gate edges.
重摻雜接面~Define heavily doped junctions|低電阻源汲極仍需維持接面隔離。~Low-resistance source-drain regions still need junction isolation.
活化退火~Integrate activation anneals|活化收益需與橫向擴散造成的通道縮短比較。~Activation gain must be compared with lateral-diffusion channel shortening.
矽化物形成~Assess silicide formation|導電接觸反應也會消耗表面矽。~Conductive contact reactions also consume surface silicon.
接觸孔位置~Place contact openings|接觸需落在目標區且避免碰到閘。~Contacts must land on targets while avoiding gates.
介電層平坦化~Plan dielectric planarization|台階形貌會傳遞到後續微影對焦。~Topography propagates into later lithography focus requirements.
第一層配線~Route first-level metal|電源與訊號連接需對應原始反相器網表。~Power and signal connections must match the inverter netlist.
通孔連通~Verify via connectivity|幾何重疊不能代替電性連通測試。~Geometric overlap does not replace electrical continuity tests.
天線效應~Trace antenna charging|長導線在製程中可把電荷集中到薄閘介電層。~Long conductors can collect process charge onto thin gate dielectrics.
轉移特性~Read inverter transfer curves|切換點取決於兩種元件的相對驅動能力。~Switching point depends on relative device strengths.
靜態功耗~Measure static power|理想互補邏輯仍有實際漏電與過渡導通。~Ideal complementary logic still has real leakage and transition conduction.
延遲與負載~Relate delay to load|相同元件在不同負載電容下有不同延遲。~Identical devices have different delays under different capacitive loads.
製程角落~Compare process corners|典型值不能代表快慢與失配的組合。~Typical values do not represent fast, slow and mismatch combinations.
失效定位~Localize circuit failures|電路失效需回連到元件、接觸或互連證據。~Circuit failures need device, contact or interconnect evidence.
整合流程審查~Review the integrated flow|步驟可單獨合格仍可能在相互作用後失敗。~Individually acceptable steps can fail through integration interactions.
''')
add('a022','鰭幾何與靜電~Fin geometry and electrostatics|鰭與隔離~Fins and isolation|三維閘與接觸~3D gates and contacts|變異與電路~Variation and circuits','scaling ald epi','a021 a023',r'''
三面閘控制~Draw three-sided gate control|閘對鰭側壁與頂面的控制不同於平面元件。~Gate control over fin sides and top differs from planar devices.
有效通道寬~Estimate effective channel width|有效寬度與鰭高、鰭寬及鰭數相關。~Effective width relates to fin height, fin width and fin count.
鰭數量化~Assess quantized drive sizing|整數鰭數限制連續調整元件驅動能力。~Integer fin counts constrain continuous drive sizing.
鰭間距~Budget fin pitch|更小間距也增加填充與隔離困難。~Smaller pitch also increases fill and isolation difficulty.
短通道指標~Choose short-channel metrics|導通電流需與關斷漏電及汲極耦合一起比較。~Compare on-current with off-leakage and drain coupling.
版圖測試車~Lay out a test vehicle|不同鰭數與密度需要可比較測試結構。~Fin count and density variants need comparable test structures.
鰭圖案轉移~Track fin pattern transfer|硬遮罩與蝕刻偏差會累積到最終鰭寬。~Hard-mask and etch biases accumulate into final fin width.
鰭側壁角~Measure fin taper|上下寬度差會改變電場與有效截面。~Top-bottom width differences alter fields and effective cross-section.
鰭粗糙度~Map fin roughness|邊緣起伏可轉為局部通道寬度變異。~Edge fluctuations translate into local channel-width variation.
隔離填充~Inspect isolation fill|鰭間填充要避免空洞與不均應力。~Inter-fin fill must avoid voids and nonuniform stress.
隔離回蝕~Control isolation recess evidence|回蝕高度決定暴露鰭高。~Isolation recess defines exposed fin height.
鰭切割~Define fin cuts|切割位置決定哪些鰭區實際連通。~Fin cuts define actual connectivity between fin regions.
三維介電覆蓋~Assess 3D dielectric coverage|頂部膜厚合格不代表側壁合格。~Acceptable top thickness does not prove sidewall coverage.
替換閘腔~Inspect replacement-gate cavities|窄腔需容納介電層、功函數層與填充金屬。~Narrow cavities must accommodate dielectric, work-function and fill layers.
源汲極磊晶~Shape source-drain epitaxy|相鄰鰭磊晶合併會改變接觸形貌。~Coalesced epitaxy across fins changes contact geometry.
間隔層覆蓋~Check spacer coverage|側壁針孔可能造成閘與接觸漏電。~Sidewall pinholes can create gate-contact leakage.
接觸落點~Assess contact landing|接觸窗口與磊晶形貌共同限制有效面積。~Contact windows and epitaxial shape jointly limit effective area.
串聯電阻~Separate series resistance|鰭增加的理想電流可能受接觸限制。~Ideal current gains from fins can be contact limited.
鰭高統計~Analyze fin-height distributions|平均鰭高不足以評估局部驅動差異。~Mean fin height is insufficient for local drive variation.
閾值分布~Measure threshold distributions|幾何、功函數及陷阱皆可能造成分布展寬。~Geometry, work function and traps can broaden distributions.
自熱效應~Assess fin self-heating|狹窄熱路徑可提高通道溫度。~Narrow heat paths can elevate channel temperature.
寄生電容~Budget parasitic capacitance|較高鰭可能同時提高驅動及寄生負載。~Taller fins can increase both drive and parasitic loading.
標準元件密度~Assess cell-level density|元件縮小不保證配線後標準元件同比縮小。~Device scaling does not guarantee equal cell scaling after routing.
FinFET 整合驗收~Accept FinFET integration|靜電、電阻、變異與標準元件效能需一起審查。~Review electrostatics, resistance, variability and cell performance jointly.
''')
add('a023','奈米片堆疊~Nanosheet stacks|內間隔與源汲極~Inner spacers and source-drain|釋放與環繞閘~Release and wraparound gate|每層及電路驗證~Per-sheet and circuit validation','scaling selective sparc','a028 a024',r'''
環繞閘拓撲~Draw the gate-all-around topology|閘須包覆通道四周而非只有上表面。~The gate surrounds the channel rather than covering only its top.
堆疊層角色~Assign stack-layer roles|通道層與可移除犧牲層需分開標示。~Channel layers and removable sacrificial layers need separate labels.
片寬與驅動~Relate sheet width and drive|較寬通道增加驅動但也改變電容與機械穩定。~Wider sheets change drive, capacitance and mechanical stability.
層間距預算~Budget inter-sheet spacing|間距需容納介電、功函數及閘金屬。~Spacing must fit dielectric, work-function and gate metal.
底部隔離~Define bottom isolation|底部寄生通道不能因上層環繞閘而自動消失。~Bottom parasitic conduction does not vanish merely because upper sheets are gated.
堆疊均勻性~Map stack uniformity|各層厚度偏差可形成不同電性通道。~Layer-thickness variation can create electrically different channels.
源汲極凹槽~Define source-drain recess|凹槽會暴露各片端點並設定後續磊晶區域。~The recess exposes sheet ends and defines subsequent epitaxial regions.
犧牲層側向凹蝕~Recess sacrificial layers laterally|凹蝕深度決定內間隔層的可用長度。~Lateral recess determines available inner-spacer length.
內間隔填充~Inspect inner-spacer fill|空洞或不完整保護會影響後續釋放。~Voids or incomplete protection affect later release.
端點清潔~Assess sheet-end cleaning|清潔需保留薄通道端點與間隔層。~Cleaning must preserve thin channel ends and spacers.
源汲極合併~Assess source-drain coalescence|不同高度成長前緣合併可能產生缺陷。~Growth fronts at different heights can merge with defects.
應變傳遞~Trace strain transfer|各層受拘束與支撐不同，應變可能不相同。~Different constraints and supports can give layers different strain.
犧牲層選蝕~Assess sacrificial-layer selectivity|需要移除犧牲層而盡量保留通道。~Sacrificial material must be removed while preserving channels.
釋放完整性~Check release completeness|入口已開不代表最深處已完全釋放。~An open entrance does not prove complete release at depth.
通道塌陷~Inspect sheet collapse|釋放後支撐及表面力可能改變幾何。~Support and surface forces can change geometry after release.
環繞介電層~Inspect wraparound dielectric|四面及片間都需要連續介電覆蓋。~Continuous dielectric is needed around sheets and between layers.
功函數金屬~Budget work-function metal|最窄間隙決定材料堆疊可用空間。~The narrowest gap limits available stack space.
閘填充空洞~Locate gate-fill voids|片間金屬不連續可能影響閘控制及電阻。~Discontinuous inter-sheet metal can affect gate control and resistance.
每層電性差~Assess per-sheet differences|總電流合格可能掩蓋某一層失效。~Acceptable total current can hide one failed layer.
短通道控制~Assess short-channel control|更完整閘包覆仍需確認接面與接觸寄生。~More complete gate coverage still requires junction and contact checks.
寄生電容預算~Budget parasitic capacitance|內間隔厚度與介電常數改變閘源汲耦合。~Inner-spacer thickness and permittivity change gate-source/drain coupling.
熱路徑~Trace heat pathways|堆疊層的散熱路徑不同於平面通道。~Stacked-sheet heat paths differ from planar-channel paths.
片寬設計組~Compare sheet-width variants|公平比較需相同漏電目標與工作電壓。~Fair comparison needs matched leakage targets and supply voltage.
GAA 整合審查~Review GAA integration|須同時交付釋放、覆蓋、接觸與變異證據。~Provide release, coverage, contact and variability evidence together.
''')
add('a024','互補堆疊架構~Complementary stacked architecture|中介隔離~Middle dielectric isolation|上下層接觸~Top and bottom contacts|研究驗證~Research validation','cfet scaling sige backside','a023 a025',r'''
垂直互補配置~Draw vertical complementary stacking|CFET 堆疊 n 與 p 元件，不只是多片同極性通道。~CFET stacks n and p devices, not merely multiple same-polarity channels.
單體與順序整合~Compare monolithic and sequential integration|單次堆疊加工與先後形成元件有不同熱限制。~Single-stack and sequential device formation have different thermal constraints.
標準元件高度~Budget standard-cell height|移除平面 n-p 間距不代表所有配線空間消失。~Removing lateral n-p separation does not eliminate routing space needs.
頂底通道分工~Assign top and bottom channels|兩層元件需要可辨識的電性及接觸測試。~Both device tiers need distinguishable electrical and contact tests.
共同閘選項~Assess common-gate options|共享閘連接仍需設定兩種元件的閾值。~Common gate connectivity still needs separate threshold setting for both polarities.
垂直節距~Budget vertical pitch|更小垂直距離會加劇隔離與加工空間限制。~Smaller vertical spacing tightens isolation and processing constraints.
中介層角色~Assign middle-layer function|中介介電層隔離上下閘而非代替全部元件隔離。~Middle dielectric isolates tier gates rather than all device isolation.
中介隔離順序~Compare isolation ordering|先做隔離或先做源汲極凹槽會改變加工邊界。~Isolation-first and recess-first sequences change processing boundaries.
內間隔共整合~Co-integrate inner spacers|中介隔離與內間隔需避免彼此破壞。~Middle isolation and inner spacers must survive each other's processing.
上下材料選擇性~Assess tier-material selectivity|加工一層時另一層仍需要保護。~Processing one tier requires protecting the other.
選擇性磊晶~Inspect tier-selective epitaxy|底層與頂層有不同的可達性與成核表面。~Top and bottom tiers differ in accessibility and seed surfaces.
低熱預算源汲極~Assess low-budget source-drain formation|降低熱暴露仍需維持活化與接觸品質。~Reduced thermal exposure must preserve activation and contact quality.
前側底層接觸~Trace frontside bottom contacts|底層接觸需穿越或繞過上層結構。~Bottom contacts from the front must pass or bypass upper structures.
背側底層接觸~Trace backside bottom contacts|背側連接另需鍵合、薄化與對準模組。~Backside access adds bonding, thinning and alignment modules.
源汲極隔離~Assess source-drain isolation|上下源汲極電性隔離與閘隔離是不同條件。~Source-drain tier isolation differs from gate isolation.
堆疊接觸電阻~Separate tier contact resistance|總串聯電阻會掩蓋頂底接觸差異。~Total series resistance can hide tier-contact differences.
垂直佈線擁塞~Map vertical routing congestion|器件面積縮小可能把瓶頸轉移到接觸與配線。~Smaller devices can move bottlenecks into contacts and routing.
對準誤差傳播~Propagate alignment error|不同模組的錯位需轉到同一三維座標。~Module misalignments must be expressed in a common 3D frame.
分層 I-V 測試~Test tier-resolved I-V|只有合併輸出無法確認每層獨立功能。~Combined output alone cannot establish each tier's function.
反相器轉移曲線~Assess inverter transfer|互補特性需由完整電路連接與轉移曲線驗證。~Complementarity needs circuit connectivity and transfer-curve evidence.
自熱與交互加熱~Assess mutual heating|一層發熱可能改變另一層的電性。~Heating one tier can alter the other's electrical behavior.
研究展示與量產~Separate demonstration from production|單一功能測試車不等於量產良率證明。~A functional test vehicle is not evidence of production yield.
跨節點比較~Compare research generations|不同研究必須對齊幾何、偏壓及抽取定義。~Cross-study comparisons need matched geometry, bias and extraction definitions.
CFET 證據地圖~Assemble a CFET evidence map|隔離、雙極性、接觸、電路與重現性需分層報告。~Report isolation, both polarities, contacts, circuits and repeatability separately.
''')
add('a026','電源路徑~Power pathways|埋入軌幾何~Buried-rail geometry|接觸與熱歷程~Contacts and thermal history|電源及可靠度~Power and reliability','bpr scaling backside','a025 a029',r'''
電源與訊號分離~Separate power and signals|埋入式軌改變電源位置，訊號仍需獨立連通。~Buried rails relocate power while signals still need separate connectivity.
正面與背面入口~Compare front and back access|有埋入軌不代表必然由背面供電。~Buried rails do not necessarily imply backside delivery.
電流回路~Trace the complete current loop|VDD 與回流路徑都貢獻元件壓降。~Both supply and return contribute to device voltage drop.
標準元件軌道~Budget cell tracks|釋出的配線軌道需經實際佈線才能確認收益。~Released tracks need routing verification to establish benefits.
埋入深度~Choose a depth study|更深軌會改變隔離、加工難度與接觸長度。~Deeper rails change isolation, process difficulty and contact length.
軌截面積~Assess rail cross-section|電阻與可用截面及材料電阻率一起相關。~Resistance depends on available cross-section and material resistivity.
隔離溝槽~Draw isolation trenches|電源金屬需與不應導通的矽區隔離。~Power metal must be isolated from unintended silicon connections.
介電襯層~Inspect dielectric liners|局部針孔可能形成電源到基板漏電。~Local liner pinholes can create rail-to-substrate leakage.
金屬填充~Assess metal fill|入口封口可能掩蓋軌內空洞。~Premature opening closure can hide voids inside rails.
軌頂封裝~Define rail capping|封蓋須在後續元件製程中維持隔離。~Rail caps must preserve isolation during later device processing.
金屬熱相容~Assess thermal compatibility|早期埋入金屬必須承受後續前段熱歷程。~Early buried metal must survive subsequent front-end thermal history.
形貌回復~Restore surface planarity|埋軌上方台階會影響後續元件圖案。~Topography above rails affects later device patterning.
軌接觸落點~Place rail contacts|通孔需要可靠落在軌上並維持周圍隔離。~Vias must land reliably on rails while preserving surrounding isolation.
接觸電阻分解~Separate contact resistance|通孔金屬、界面與軌本體是不同電阻來源。~Via metal, interfaces and rail body contribute separate resistances.
熱應力傳遞~Trace thermal stress|埋軌與矽熱膨脹差可影響鄰近通道。~Rail-silicon expansion mismatch can affect nearby channels.
漏電測試~Test rail leakage|低軌電阻不能證明介電隔離完整。~Low rail resistance does not establish dielectric isolation.
軌間短路~Locate inter-rail shorts|相鄰供電與回流軌需要獨立絕緣驗證。~Adjacent supply and return rails need isolation verification.
接觸鏈測試~Use contact chains|長鏈可放大接觸缺陷但不易定位單一失效。~Chains amplify contact defects but may not locate one failure.
直流壓降~Compute DC drop|串聯路徑的壓降需依局部電流分段計算。~Series drop should be computed with each segment's local current.
動態下陷~Assess transient droop|相同直流電阻可能有不同寄生及瞬態。~Equal DC resistance can coexist with different parasitics and transients.
電遷移~Assess electromigration|電流密度與溫度共同影響金屬可靠度。~Current density and temperature jointly affect metal reliability.
局部熱點~Locate rail hotspots|接觸狹窄處可能同時集中電流與熱。~Narrow contacts can concentrate both current and heat.
電路收益比較~Compare circuit benefit|面積收益需與功耗、延遲及良率一起評估。~Area benefits need power, delay and yield assessment.
埋軌放行~Release buried-rail integration|電性、隔離、熱相容與可佈線性需全部有證據。~Electrical, isolation, thermal compatibility and routability all need evidence.
''')
add('a027','節點與比較基準~Nodes and comparison baselines|元件及圖案~Devices and patterning|電源及互連~Power and interconnects|研究證據~Research evidence','scaling cfet backside','sub2nm a024',r'''
節點名稱~Interpret node names|節點名稱不是任何單一實體幾何的直接量測。~A node name is not a direct measurement of one physical dimension.
幾何參數表~Build a geometry table|閘長、閘節距、金屬節距與元件高度各自不同。~Gate length, gate pitch, metal pitch and cell height are distinct.
工作負載基準~Choose workload baselines|效能比較需要相同工作負載與限制條件。~Performance comparisons require matched workloads and constraints.
功耗效能面積~Separate PPA metrics|功耗、效能與面積通常不能同時單獨最佳化。~Power, performance and area generally cannot be independently optimized together.
模型與量測~Classify evidence types|模擬預測、單元展示與量產數據不可混稱。~Predictions, test demonstrations and production data are distinct evidence.
不確定度帳本~Create an uncertainty ledger|公開缺失參數須標記未知，不能補成廠商規格。~Missing public parameters remain unknown rather than invented specifications.
奈米片選項~Compare nanosheet options|寬度可調與堆疊製程限制需一起比較。~Width flexibility must be weighed against stack-processing limits.
Forksheet 選項~Assess forksheet options|介電牆改變 n-p 間距與閘加工空間。~A dielectric wall changes n-p separation and gate-processing space.
CFET 選項~Assess CFET options|垂直互補可省平面面積但增加上下接觸難題。~Vertical complementarity saves lateral area but complicates tier contacts.
通道材料~Compare channel materials|高遷移率材料仍需可用介面與接觸。~High-mobility materials still require workable interfaces and contacts.
圖案化分解~Decompose patterning needs|曝光解析度、套刻及缺陷率是不同限制。~Resolution, overlay and defectivity are distinct patterning limits.
High-NA 邊界~Assess High-NA boundaries|高數值孔徑改變成像條件但不自動解決全部整合。~Higher numerical aperture changes imaging but does not solve all integration issues.
接觸瓶頸~Locate contact bottlenecks|通道改善可能被增加的存取電阻抵銷。~Channel improvements can be offset by access resistance.
局部配線材料~Compare local interconnect materials|窄線電阻不可只套用塊材電阻率。~Narrow-line resistance cannot be inferred from bulk resistivity alone.
背面供電~Assess backside power|正背面分工可減少擁塞但增加薄化及接觸模組。~Front-back separation can reduce congestion but adds thinning and contacts.
熱路徑~Budget thermal pathways|高密度與垂直堆疊會改變局部熱阻。~Density and vertical stacking change local thermal resistance.
標準元件協同~Co-design standard cells|元件截面需與可實際連線的元件庫一起評估。~Device sections need evaluation with routable cell libraries.
SRAM 不同需求~Separate SRAM constraints|記憶體單元的穩定裕度不同於單純邏輯延遲。~Memory-cell stability differs from logic-delay optimization.
變異來源~Build a variability budget|幾何、材料與隨機缺陷需分開估算。~Geometry, materials and stochastic defects need separate estimates.
可靠度範圍~Define reliability conditions|加速壓力試驗須有可解釋的外推模型。~Accelerated stress tests need an interpretable extrapolation model.
良率與成本~Connect yield and cost|較小裸晶不保證每顆良品成本較低。~Smaller dies do not guarantee lower cost per good die.
路線圖日期~Version roadmap claims|研究路線圖是有日期的預測而非交貨承諾。~Roadmaps are dated projections rather than delivery commitments.
公平比較矩陣~Build a fair comparison matrix|只選各方案最佳單點會掩蓋共同限制。~Selecting each option's best isolated metric hides common constraints.
研究提案交付~Deliver a research proposal|提出可量測假說、對照組及失敗判準才可檢驗。~A testable proposal needs measurable hypotheses, controls and failure criteria.
''')
add('a028','間隔層功能~Spacer functions|側向凹蝕~Lateral recess|填充與回蝕~Fill and etchback|釋放保護~Protection during release','sparc selective scaling','a023 a020',r'''
內外間隔差別~Separate inner and outer spacers|內間隔位於片間端部，外間隔位於閘外側。~Inner spacers occupy inter-sheet ends while outer spacers flank the gate.
閘源汲隔離~Trace gate-source/drain isolation|內間隔同時影響電隔離及後續選蝕保護。~Inner spacers affect electrical isolation and later selective-etch protection.
寄生電容~Estimate parasitic coupling|介電常數與實際幾何共同決定耦合。~Permittivity and actual geometry jointly determine coupling.
間隔長度~Budget spacer length|太短增加耦合風險，太長可能增加存取電阻。~Short spacers increase coupling risk while long spacers can add access resistance.
片間可達性~Assess inter-sheet access|不同層的反應物到達及產物排出可能不同。~Reactant access and product removal can differ by layer.
源汲端點保護~Mark protected sheet ends|間隔形成不能消耗有效通道端點。~Spacer formation must preserve functional channel ends.
凹蝕選擇比~Define recess selectivity|犧牲材料去除量需與通道損失一起量測。~Measure sacrificial removal together with channel loss.
側向深度分布~Map recess-depth distributions|平均凹蝕深度會掩蓋頂底片差異。~Mean recess depth can hide top-bottom differences.
凹角形狀~Inspect recessed corners|圓角與尖角會改變後續填充截面。~Rounded and sharp corners produce different fill geometries.
薄層粗糙~Check thin-layer roughness|粗糙度相對於目標間隔長度可能不可忽略。~Roughness may be significant relative to spacer length.
過蝕風險~Assess overetch|延長處理以清除最慢位置會增加其他區域損失。~Extending treatment for the slowest region increases loss elsewhere.
圖案負載~Compare pattern loading|密集與稀疏結構需分別驗證凹蝕。~Dense and sparse structures need separate recess validation.
低介電材料~Compare low-k materials|低介電常數不保證機械與化學耐受。~Low permittivity does not guarantee mechanical or chemical robustness.
共形沉積~Assess conformal deposition|厚度共形還需檢查成分共形。~Thickness conformality also needs compositional conformality.
腔口封閉~Predict opening closure|入口較快成長可能留下隱藏空洞。~Faster entrance growth can trap hidden voids.
回蝕選擇性~Check etchback selectivity|需去除外部材料而保留凹槽中的內間隔。~External material must be removed while retaining recessed spacers.
片端殘留~Inspect sheet-end residue|端點殘留可阻礙源汲極磊晶成長。~Endpoint residues can obstruct source-drain epitaxy.
介電針孔~Locate dielectric pinholes|單一缺口可能成為後續蝕刻侵入路徑。~A single opening can become a later etchant-access path.
犧牲層釋放~Assess release survival|內間隔需承受犧牲層移除的化學環境。~Inner spacers must survive sacrificial-layer removal.
源汲極侵蝕~Detect source-drain attack|源汲極縮減可反映內間隔保護失效。~Source-drain loss can indicate failed spacer protection.
電容量測~Measure coupling capacitance|比較需控制重疊面積及電性偏壓。~Comparisons need matched overlap area and bias.
存取電阻~Assess access resistance|降低電容的改動可能增加非閘控區電阻。~Capacitance reduction can increase ungated access resistance.
逐層截面~Inspect every sheet level|單一中層截面不能代表整個堆疊。~One middle-level section cannot represent the full stack.
間隔模組放行~Release the spacer module|尺寸、覆蓋、低電容及釋放後存活須共同成立。~Dimensions, coverage, capacitance and post-release survival must all hold.
''')
add('a029','電阻分解~Resistance decomposition|界面與摻雜~Interface and doping|幾何及量測~Geometry and measurement|整合及壽命~Integration and lifetime','sige scaling epi','a020 a030',r'''
電阻與比接觸電阻~Separate resistance and resistivity|接觸電阻與比接觸電阻的單位不同。~Contact resistance and specific contact resistivity have different units.
通道與存取路徑~Separate channel and access paths|總電阻包含通道、源汲極、界面及金屬。~Total resistance includes channel, source-drain, interfaces and metal.
電流擁擠~Draw current crowding|電流未必均勻穿過整個幾何接觸面積。~Current need not cross the geometric contact area uniformly.
傳輸長度~Interpret transfer length|接觸長度超過傳輸長度後收益可能減弱。~Benefits can diminish when contact length exceeds transfer length.
接觸能障~Draw contact barriers|能障高度與穿隧機制共同影響接觸電性。~Barrier height and tunneling jointly affect contact behavior.
公平基準~Choose comparison baselines|比較需使用相同面積定義與摻雜狀態。~Comparisons need matching area definitions and doping conditions.
表面氧化殘留~Assess residual oxide|薄殘留層也可能顯著增加界面電阻。~Even thin residual layers can significantly increase interface resistance.
活化載子~Measure active carriers|高化學濃度不保證高活化載子濃度。~High chemical doping does not guarantee high active carrier density.
界面反應相~Inspect reacted phases|反應後相組成會改變電阻與材料消耗。~Reacted phases alter resistance and material consumption.
金屬選擇~Compare contact metals|低塊材電阻率不保證低半導體接觸電阻。~Low bulk metal resistivity does not ensure low semiconductor contact resistance.
界面清潔等待~Track clean-to-metal delay|清潔後再氧化會改變接觸前的界面狀態。~Reoxidation after cleaning changes the pre-metal interface.
退火窗口~Assess contact annealing|接觸改善需與擴散、粗糙化及相變權衡。~Contact improvement must be balanced against diffusion, roughening and phase changes.
TLM 長度陣列~Lay out a TLM array|不同間距的電阻斜率與截距提供不同資訊。~Resistance slope and intercept across spacings provide different information.
四端 Kelvin~Design Kelvin measurements|四端配置可降低探針及引線電阻干擾。~Four-terminal configurations reduce probe and lead resistance influence.
CTLM 幾何修正~Inspect circular TLM geometry|圓形電流展開不能直接套用直線幾何公式。~Radial current spreading needs geometry-specific treatment.
面積抽取誤差~Propagate area error|面積誤差可直接污染比接觸電阻判讀。~Area errors directly affect extracted specific contact resistivity.
邊緣與側壁~Include sidewall contacts|環繞接觸的有效面積不只頂面投影。~Wraparound contact area exceeds top-view projection alone.
低值量測極限~Assess low-resistance limits|儀器零點及寄生可能主導極低電阻讀值。~Offsets and parasitics can dominate very low resistance readings.
溫度依賴~Measure temperature dependence|溫度趨勢可協助辨識不同傳輸機制。~Temperature trends can help distinguish transport mechanisms.
電流非線性~Inspect current nonlinearity|單點電阻可能掩蓋非歐姆接觸。~A single resistance value can hide non-ohmic behavior.
分布與尾端~Report distributions and tails|少數高電阻接觸可能限制整體良率。~A small high-resistance tail can limit overall yield.
熱與電流老化~Assess thermal and current aging|初始低阻不能替代長時間穩定性驗證。~Initially low resistance cannot replace long-term stability checks.
元件效能歸因~Attribute device gains|需把接觸改變與通道遷移率改變分開。~Separate contact changes from channel-mobility changes.
接觸改善報告~Report contact improvement|方法、幾何、活化、分布及可靠度都需可追溯。~Method, geometry, activation, distributions and reliability must be traceable.
''')
add('a030','接觸與套刻~Contacts and overlay|選擇性蝕刻~Selective etching|清潔及填充~Cleaning and fill|電性與缺陷~Electrical behavior and defects','ale selective sparc','a029 a018',r'''
自對準的含義~Define self-alignment|自對準利用材料或結構邊界而非完全取消套刻。~Self-alignment uses material or structural boundaries rather than eliminating overlay.
接觸目標區~Mark contact targets|接觸需連到源汲極且避開閘金屬。~Contacts must reach source-drain while avoiding gate metal.
閘帽與間隔層~Assign caps and spacers|閘帽與間隔層共同提供蝕刻保護。~Gate caps and spacers jointly provide etch protection.
套刻容忍圖~Draw overlay-tolerance maps|幾何容忍需同時計入孔寬與保護層剩餘量。~Tolerance includes opening width and remaining protective material.
縱橫比~Assess aspect ratio|深窄孔的傳輸與底部去除不同於平面。~Transport and bottom removal in deep holes differ from planar surfaces.
材料選擇比~Define material selectivity|高選擇比仍需知道保護層可接受損失。~High selectivity still requires an allowable protection-layer loss.
離子方向性~Assess ion directionality|方向性有助向下去除但仍可能傷害角落。~Directionality helps downward removal but can still damage corners.
原子層蝕刻循環~Decompose an ALE cycle|表面改質與移除需作為分開的作用理解。~Surface modification and removal are distinct operations.
底部殘留~Inspect bottom residue|孔已打開不代表接觸界面完全清潔。~An open hole does not prove a clean contact interface.
角落保護~Measure corner loss|平均間隔厚度不能代表最薄角落。~Mean spacer thickness does not represent the thinnest corner.
微負載~Compare microloading|不同孔密度及尺寸可能有不同清除時間。~Hole density and size can cause different clearing times.
終點與過蝕~Separate endpoint and overetch|最慢孔清除所需過蝕會消耗其他位置保護層。~Overetch for slow holes consumes protection elsewhere.
蝕刻後殘留~Classify post-etch residues|聚合物與金屬殘留可能需要不同判讀。~Polymer and metal residues need different interpretation.
源汲極損失~Measure source-drain loss|底部清潔不能以過度消耗目標材料為代價。~Bottom cleaning must not excessively consume target material.
襯層厚度預算~Budget liner thickness|襯層會消耗孔內可用導體截面。~Liners consume available conductor cross-section.
接觸填充~Inspect contact fill|早期封口可留下中空接觸。~Premature closure can leave hollow contacts.
平坦化隔離~Assess planarization isolation|表面殘金屬可能連接原本分開的接觸。~Residual surface metal can bridge separate contacts.
阻障完整性~Assess barrier continuity|低電阻填充仍需防止材料向鄰近區擴散。~Low-resistance fill still needs diffusion containment.
開路與高阻~Separate opens and high resistance|完全開路與部分接觸不良需要不同診斷。~Complete opens and partial contact failure need different diagnosis.
閘接觸短路~Test gate-contact shorts|源汲極導通不代表與閘保持隔離。~Source-drain continuity does not prove gate isolation.
接觸鏈統計~Analyze contact-chain statistics|長鏈失效機率與單接點良率相關。~Chain failure probability depends on individual contact yield.
截面與電性對照~Correlate sections and electrical data|截面位置需與實際失效位置匹配。~Cross-sections must match actual electrical failure locations.
設計窗口~Build a design-process window|孔寬、套刻及保護層損失需共同取交集。~Opening width, overlay and protection loss define a joint window.
SAC 放行~Accept self-aligned contacts|導通、隔離、填充及套刻裕度必須一起驗證。~Continuity, isolation, fill and overlay margin need joint validation.
''')
add('a031','光阻與基板~Resist and substrate|塗佈流動~Coating flow|缺陷及膜厚~Defects and thickness|曝光交接~Exposure handoff','spin resist antireflect car','a032 a033',r'''
曝光波長匹配~Match exposure wavelength|DUV 光阻須以相應波長資料選擇，不能以外觀判斷。~DUV resist selection needs wavelength-specific data, not appearance.
樹脂溶劑分工~Separate resin and solvent|溶劑影響流動與乾燥，樹脂影響成膜及顯影。~Solvent affects flow and drying; resin affects film formation and development.
黏度與固含量~Compare viscosity and solids|相同黏度不保證乾膜厚度相同。~Equal viscosity does not guarantee equal dry thickness.
基板濕潤性~Assess substrate wetting|表面能不匹配可能造成退潤與露底。~Surface-energy mismatch can cause dewetting and bare patches.
附著促進~Assess adhesion promotion|附著處理要與基板材料及光阻化學相容。~Adhesion treatment must match substrate and resist chemistry.
塗佈前溫度~Record precoat temperature|材料溫度改變黏度與揮發。~Material temperature changes viscosity and evaporation.
滴液位置~Assess dispense position|偏心滴液可造成初始覆蓋不均。~Off-center dispensing can cause uneven initial coverage.
靜態與動態滴液~Compare static and dynamic dispense|兩種滴液方式改變鋪展與材料利用率。~The two dispense modes alter spreading and material utilization.
加速度歷程~Design acceleration comparisons|轉速終值相同不代表鋪展歷程相同。~Equal final speed does not imply equal spreading history.
旋轉與膜厚~Analyze spin-thickness trends|經驗膜厚關係僅在指定材料與範圍內適用。~Empirical spin-thickness relations apply only within specified materials and ranges.
揮發與排風~Assess evaporation and exhaust|氣流改變溶劑蒸發並可能形成徑向差異。~Airflow changes solvent evaporation and can produce radial differences.
邊珠形成~Inspect edge-bead formation|邊緣厚膜會影響後續接觸、污染及曝光可用區。~Edge beads affect downstream contact, contamination and usable exposure area.
邊珠去除~Define edge-bead removal evidence|去除寬度需兼顧邊緣潔淨與有效面積。~Removal width balances edge cleanliness and usable area.
背面污染~Inspect backside contamination|背面光阻可轉移到吸盤與後續晶圓。~Backside resist can transfer to chucks and later wafers.
氣泡缺陷~Identify bubbles|氣泡與固體粒子需分開建立缺陷類別。~Bubbles and solid particles require separate defect classes.
放射條紋~Interpret radial striations|條紋應與旋轉、氣流及乾燥條件對照。~Striations should be compared with rotation, airflow and drying conditions.
台階覆蓋~Assess topographic coverage|平面均勻膜不保證台階角落也有足夠厚度。~Uniform planar films do not guarantee sufficient corner coverage.
膜厚地圖~Construct thickness maps|平均膜厚與片內非均勻性須同時報告。~Report mean thickness and within-wafer nonuniformity together.
光學常數~Check optical constants|膜厚反演需要適用波長的折射率模型。~Thickness extraction needs refractive-index models valid at the measurement wavelength.
反射與底層~Assess substrate reflectivity|基板反射會改變光阻內部曝光分布。~Substrate reflection changes exposure distribution within resist.
底部抗反射層~Assess bottom antireflection layers|抗反射層需與光阻及後續蝕刻相容。~Antireflection layers must match resist and subsequent etching.
軟烤前等待~Assess delay before softbake|等待會改變溶劑殘留及流動。~Delay changes solvent content and flow.
膜厚與焦深~Connect thickness and focus budget|過厚或不均勻的膜會增加圖案轉移的不確定度。~Excessive or uneven thickness increases pattern-transfer uncertainty.
DUV 塗佈交接~Release the DUV coating|膜厚、邊緣、背面及缺陷證據須一起交給曝光端。~Thickness, edge, backside and defect evidence must accompany exposure handoff.
''')
add('a032','烘烤機制~Bake mechanisms|曝光後反應~Post-exposure reaction|顯影傳輸~Development transport|圖案驗收~Pattern acceptance','softbake peb develop acid','a031 a033',r'''
軟烤與 PEB~Separate softbake and PEB|除溶劑與曝光後反應是不同功能。~Solvent removal and post-exposure reaction serve different functions.
熱板與片溫~Separate hotplate and wafer temperature|設定溫度不能等同於光阻瞬間溫度。~Setpoint does not equal instantaneous resist temperature.
殘留溶劑~Assess residual solvent|溶劑殘留會影響顯影與材料力學行為。~Residual solvent affects development and mechanical behavior.
接觸熱阻~Assess thermal contact|晶圓翹曲與背面污染會改變熱接觸。~Wafer bow and backside contamination alter thermal contact.
升溫與冷卻~Include heating and cooling|化學反應不一定只發生在名義保溫時間內。~Chemical reaction need not occur only during nominal dwell.
烘烤均勻性~Map bake uniformity|微小溫差可能經反應敏感度放大為尺寸差。~Small temperature differences can amplify into dimensional variation.
曝光後等待~Track post-exposure delay|等待時間會改變酸遷移及污染中和機會。~Delay changes acid transport and opportunities for contaminant neutralization.
化學放大反應~Trace chemical amplification|光生酸可催化多次反應而非只對應單一光子事件。~Photoacid can catalyze multiple reactions rather than one event per photon.
酸擴散長度~Assess acid diffusion length|更長反應時間也可能增加影像模糊。~Longer reaction time can also increase image blur.
表面中和~Assess surface neutralization|空氣鹼性污染可能改變上表面反應。~Airborne bases can change reactions near the top surface.
基底界面反應~Inspect substrate-interface reaction|底層化學狀態會影響底部光阻輪廓。~Underlying chemistry affects the resist profile near the bottom.
PEB 視窗~Build a PEB window|反應完成度、尺寸及粗糙度需共同取捨。~Reaction completion, dimensions and roughness need joint tradeoffs.
正負型溶解~Separate positive and negative tone|顯影保留區由材料反應與顯影化學共同決定。~Remaining regions depend on both resist chemistry and developer.
顯影液相容~Review developer compatibility|不同光阻不能直接共用同一顯影條件。~Different resists cannot automatically share developer conditions.
溶解速率~Compare dissolution rates|曝光與未曝光區速率差決定圖案對比。~Rate contrast between exposed and unexposed regions determines image contrast.
液膜更新~Assess puddle renewal|顯影產物累積會改變局部傳輸。~Accumulated dissolution products change local transport.
暗蝕損失~Measure dark erosion|未曝光保留區也可能在顯影中變薄。~Unexposed retained regions can also thin during development.
沖洗終止~Define rinse termination|沖洗改變反應與溶解產物移除，需納入時間線。~Rinsing affects reaction termination and product removal and belongs in the timeline.
底部殘膠~Identify scum|上方開口不代表底部已完全清除。~An opening at the top does not prove complete bottom clearance.
側壁角度~Measure sidewall angle|頂視尺寸相同可能有不同底部尺寸。~Equal top-view dimensions can hide different bottom dimensions.
圖案倒塌~Assess pattern collapse|高細長圖案在乾燥中可能受毛細力破壞。~Slender patterns can fail under capillary forces during drying.
尺寸偏差歸因~Attribute CD bias|曝光、PEB 與顯影都可能造成最終尺寸偏差。~Exposure, PEB and development can all cause final CD bias.
曝光烘烤矩陣~Design a dose-bake matrix|交叉實驗可辨識劑量與熱歷程交互作用。~A crossed study can identify dose-thermal-history interactions.
光阻圖案交接~Release the resist pattern|線寬、輪廓、殘膠及薄膜損失需共同符合要求。~Width, profile, scum and retained-film loss must jointly meet requirements.
''')
add('a033','配方功能分工~Formulation functions|光化學及擴散~Photochemistry and diffusion|圖案與隨機性~Patterning and stochasticity|整合及材料評估~Integration and material assessment','car acid pag resist peb develop','a031 a032',r'''
放大機制定義~Define amplification|光生催化劑可啟動多次溶解度改變反應。~A photogenerated catalyst can initiate multiple solubility-changing reactions.
樹脂保護基~Assign protecting groups|保護基轉換使樹脂對顯影液的親和改變。~Protecting-group conversion changes resin affinity to developer.
光酸產生劑~Assign photoacid generators|PAG 吸收、產酸與相容性須同時評估。~PAG absorption, acid generation and compatibility need joint evaluation.
淬熄劑作用~Assign quencher functions|淬熄劑限制酸反應也可能降低感度。~Quenchers limit acid activity but can reduce sensitivity.
溶劑與成膜~Choose film-formation evidence|溶液均勻不保證乾膜成分分布均勻。~A uniform solution does not guarantee uniform dry-film composition.
波長相容~Assess wavelength compatibility|材料吸收需配合目標曝光波長與膜厚。~Absorption must match exposure wavelength and film thickness.
吸收深度~Estimate absorption depth|過強吸收可能造成上下層反應不均。~Excessive absorption can produce through-film reaction gradients.
酸產生統計~Assess acid-generation statistics|微小區域的光子與分子事件具有隨機性。~Photon and molecular events are stochastic in small volumes.
反應與擴散~Separate reaction and diffusion|反應速率與擴散係數控制不同影像特徵。~Reaction rate and diffusivity control different image characteristics.
PEB 敏感度~Measure PEB sensitivity|高溫敏感度可能放大熱板不均造成的尺寸差。~Strong temperature sensitivity can amplify hotplate-related CD variation.
酸中和競爭~Analyze acid-neutralization competition|淬熄與去保護反應競爭決定有效反應範圍。~Quenching competes with deprotection to set the effective reaction region.
自由體積影響~Assess free-volume effects|材料狀態會影響分子擴散而非只有溫度。~Material state influences molecular diffusion beyond temperature alone.
感度解析度粗糙度~Compare sensitivity-resolution-roughness|降低曝光劑量不保證同時提升解析度與粗糙度。~Lower dose does not guarantee better resolution and roughness together.
溶解對比~Measure dissolution contrast|去保護比例與實際溶解速率需以資料連結。~Deprotection fraction needs empirical connection to dissolution rate.
線邊粗糙~Assess line-edge roughness|粗糙度需指定量測長度、濾波及取樣。~Roughness requires specified evaluation length, filtering and sampling.
缺孔與橋接~Classify missing and bridged features|平均線寬可能掩蓋離散圖案失效。~Mean linewidth can conceal discrete pattern failures.
配方相分離~Inspect phase separation|添加物分布不均可形成局部反應差異。~Nonuniform additive distribution can create local reaction differences.
顯影膨潤~Assess development swelling|溶劑進入膜內可能先改變形貌再溶解。~Solvent ingress can change morphology before dissolution.
蝕刻耐受~Assess etch resistance|高感度材料仍需要足夠圖案轉移耐受。~Sensitive materials still need sufficient pattern-transfer durability.
逸氣與殘留~Review outgassing and residue|曝光或加熱釋出物可能影響設備與介面。~Exposure or thermal outgassing can affect equipment and interfaces.
保存與老化~Assess storage aging|配方性能需附批次、儲存條件及使用時點。~Performance needs lot, storage conditions and time-of-use metadata.
組成實驗設計~Design mixture experiments|配方比例互相耦合，不能當作完全獨立變數。~Composition fractions are coupled rather than fully independent variables.
資料與配方邊界~Distinguish model from proprietary recipe|公開原理能支持假說，但不能補出未公開配方。~Public principles support hypotheses but do not reveal proprietary formulations.
光阻材料評估~Deliver a resist assessment|需用相同曝光、顯影及蝕刻基準比較候選材料。~Compare candidate materials with matched exposure, development and etch baselines.
''')

SOURCES={}
def source(key,title,en,publisher,url,scope,en_scope):
    SOURCES[key]=dict(id='v8a-'+key,title=title,titleEn=en,publisher=publisher,url=url,scope=scope,scopeEn=en_scope,accessedAt='2026-10-14',sourceType='primary',category='semiconductor')
source('sumco','矽晶圓製造流程','Silicon wafer production processes','SUMCO','https://www.sumcosi.com/english/products/process/','晶棒、切片、研磨、磊晶與 SOI 概念。','Ingot, slicing, finishing, epitaxy and SOI concepts.')
source('wafer','矽晶圓生產與規格','Silicon wafer production and specifications','MicroChemicals','https://www.microchemicals.com/dokumente/application_notes/silicon_wafer_production_specification.pdf','線鋸、材料移除與晶圓形貌；教學任務為原創。','Wire sawing, removal and wafer geometry; learning exercises are original.')
source('soitec','Smart Cut 層轉移技術','Smart Cut layer-transfer technology','Soitec','https://www.soitec.com/home/technology/innovation/smart-cut','離子弱化層、鍵合、分裂與供體再利用。','Implanted weak layers, bonding, splitting and donor reuse.')
source('epi','磊晶的製程用途','Epitaxy process applications','Applied Materials','https://www.appliedmaterials.com/us/en/semiconductor/products/processes/epitaxy.html','晶體層、摻雜與應變工程。','Crystalline layers, doping and strain engineering.')
source('mit','微奈米加工：元件與製程概觀','Micro/nano processing: device and process overview','MIT OpenCourseWare','https://ocw.mit.edu/courses/6-152j-micro-nano-processing-technology-fall-2005/9878a7acdd9632caa5afb8b4b96a6f39_lecture2.pdf','CMOS 與基礎加工的教育背景；非先進節點配方。','Educational background for CMOS and basic processing; not a leading-edge recipe.')
source('frontend','微製造前段物理課程','Physics of Microfabrication: Front End Processing','MIT OpenCourseWare','https://ocw.mit.edu/courses/6-774-physics-of-microfabrication-front-end-processing-fall-2004/','氧化、擴散、佈植、磊晶、量測與材料關聯。','Connections among oxidation, diffusion, implantation, epitaxy, metrology and materials.')
source('clean','濕式蝕刻與清洗','Wet etch and clean','Entegris','https://www.entegris.com/en/home/our-science/by-industry/microelectronics/semiconductor/wet-etch-clean.html','殘留、粒子、材料損失與流體管理。','Residues, particles, material loss and fluid management.')
source('purity','超純化學品與水的污染控制','Contamination control in ultrapure chemicals and water','Entegris','https://www.entegris.com/en/home/resources/technical-information/faq/contamination-control-in-ultrapure-chemicals-and-water.html','過濾、截留、流量、相容與污染種類。','Filtration, retention, flow, compatibility and contaminant classes.')
source('filtration','液體過濾方案','Liquid filtration solutions','Entegris','https://www.entegris.com/en/home/resources/reference-materials/brochures/liquid-filtration-solutions-8600.html','超純水、使用點純化及材料接觸鏈。','Ultrapure water, point-of-use purification and wetted-material chains.')
source('contam','目標污染物去除','Targeted contaminant removal','Entegris','https://www.entegris.com/en/home/resources/industry-insights/targeted-contaminant-removal.html','液體、氣體與空氣分子污染的不同機制。','Different liquid, gas and airborne molecular contamination mechanisms.')
source('amhs','無塵室自動搬運與控制影片','Cleanroom transport and controller videos','Daifuku','https://www.daifuku.com/pro/cr/','AMHS、MCS、OHT 及供應商公開概念影片；不保證外部播放可用。','AMHS, MCS, OHT and supplier concept videos; external playback availability is not guaranteed.')
source('daifuku','大福公司與大阪代表據點','Daifuku and Osaka representative location','Daifuku','https://www.daifuku.com/de/company/summary/','官方公司與地址資料、嵌入地圖；不是廠內軌道圖。','Official organization, address and embedded map; not an internal track layout.')
source('oxide','矽晶圓氧化與薄膜','Silicon wafer oxidation and coatings','MicroChemicals','https://www.microchemicals.com/dokumente/application_notes/silicon_wafer_sio2_si3n4_metallization_epitaxy_soi.pdf','熱氧化、材料消耗、薄膜與基板關係。','Thermal oxidation, material consumption and substrate-film relationships.')
source('ald','原子層沉積概觀','A look at atomic layer deposition','Lam Research','https://newsroom.lamresearch.com/Tech-Brief-A-Look-at-Atomic-Layer-Deposition-ALD','表面循環與三維共形薄膜。','Surface cycling and conformal films on three-dimensional structures.')
source('highk','高介電常數與金屬閘極整合','Integrated high-k and metal-gate technology','Applied Materials','https://ir.appliedmaterials.com/news-releases/news-release-details/applied-materials-makes-transistor-cool-again-integrated-high','2007 年公開整合方案；歷史背景，不是現今量產規格。','Historical 2007 integration announcement, not current production specifications.')
source('implant','擴散與離子佈植講義','Diffusion and ion implantation lecture','MIT OpenCourseWare','https://ocw.mit.edu/courses/6-152j-micro-nano-processing-technology-fall-2005/fa6170fba10bd1341251791563a18fc2_lecture6.pdf','劑量、射程、損傷、遮罩與擴散模型。','Dose, range, damage, masks and diffusion models.')
source('implantmask','佈植的光阻遮罩','Photoresist masks for ion implantation','MicroChemicals','https://www.microchemicals.com/dokumente/application_notes/ion_implantation_photoresist.pdf','遮罩、熱與光阻去除注意事項。','Masking, heating and resist-removal considerations.')
source('rtp','快速熱處理','Rapid thermal processing and treatments','Applied Materials','https://www.appliedmaterials.com/us/en/semiconductor/products/processes/rapid-thermal-processing-treatments.html','燈式、雷射式與加熱器式熱處理及熱預算。','Lamp, laser and heater processing and thermal budgets.')
source('laser','先進邏輯的雷射退火系統公告','Laser-annealing systems for advanced logic','Veeco','https://ir.veeco.com/news-and-events/news-details/2024/Leading-Edge-Semiconductor-Company-Places-Multi-System-Laser-Annealing-Order-Including-First-Nanosecond-Annealing-System/default.aspx','毫秒 LSA 與奈秒系統的用途差異；不引用供應商優越性宣稱。','Different roles for millisecond LSA and nanosecond systems; vendor superiority claims are not adopted.')
source('legacy','單晶圓前段熱製程','Single-wafer front-end thermal processes','Applied Materials','https://ir.appliedmaterials.com/news-releases/news-release-details/lucent-technologies-and-applied-materials-cooperate-single-wafer/','歷史 STI 襯層、氧化與退火整合背景。','Historical context for STI liners, oxidation and anneal integration.')
source('strain','半導體技術詞彙','Semiconductor technical glossary','Applied Materials','https://www.appliedmaterials.com/us/en/glossary.html','應變工程及半導體基本術語；另搭配磊晶來源。','Strain engineering and basic semiconductor terminology alongside the epitaxy source.')
source('sige','奈米片 CFET 源汲極磊晶','Source/drain epitaxy for nanosheet-based CFET devices','Electrochemical Society / contributing researchers','https://ecs.confex.com/ecs/prime2024/meetingapp.cgi/Paper/195397','公開會議摘要：選擇性磊晶、活化、CTLM 接觸評估；未取得完整論文。','Public conference abstract: selective epitaxy, activation and CTLM contact assessment; full paper was not retrieved.')
source('selective','選擇性蝕刻技術','Selective etch technology','Lam Research','https://www.lamresearch.com/product/selective-etch-product-family/','SiGe 釋放、選擇性與表面保護。','SiGe release, selectivity and surface protection.')
source('scaling','從 FinFET 到奈米片與 CFET','Scaling from FinFETs to nanosheets and CFETs','imec','https://www.imec-int.com/en/imec-magazine/imec-magazine-december-2019/scaling-cmos-beyond-finfets-from-nanosheets-and-forksheets-to-cfets','2019 研究架構比較；預測與示範分開。','2019 research architecture comparisons; projections are distinguished from demonstrations.')
source('sparc','低介電間隔層與 GAA','Low-k spacers and GAA applications','Lam Research','https://newsroom.lamresearch.com/SPARC-a-new-deposition-technology-for-advanced-logic-and-DRAM','內間隔層的共形、選擇性及源汲極保護需求。','Inner-spacer conformality, selectivity and source-drain protection requirements.')
source('cfet','功能性單體 CFET 研究展示','Functional monolithic CFET research demonstration','imec','https://www.imec-int.com/en/press/imec-demonstrates-functional-monolithic-cfet-devices-stacked-bottom-and-top-contacts','2024 展示的中介隔離與上下接觸，不等於量產配方。','Middle isolation and stacked contacts in a 2024 demonstration, not a production recipe.')
source('backside','由背面為晶片供電','Powering chips from the backside','imec','https://www.imec-int.com/en/articles/how-power-chips-backside','背面供電、埋入軌、薄化與奈米通孔。','Backside power, buried rails, thinning and nanoscale vias.')
source('bpr','背面供電的設計技術協同','Backside power delivery options: a DTCO study','imec','https://www.imec-int.com/en/articles/backside-power-delivery-options-dtco-study','電源位置、元件配線與電路層次的權衡。','Tradeoffs in rail position, cell routing and circuits.')
source('ale','原子層蝕刻與自對準接觸','Atomic layer etching and self-aligned contacts','Lam Research','https://newsroom.lamresearch.com/Tech-Brief-All-About-ALE','改質移除循環、選擇性及間隔層角落保護。','Modification-removal cycles, selectivity and spacer-corner protection.')
source('spin','光阻旋轉塗佈','Spin coating of photoresists','MicroChemicals','https://www.microchemicals.com/dokumente/application_notes/spin_coating_photoresist.pdf','流動、膜厚、邊珠與缺陷原理；不得當作 DUV 個別產品配方。','Flow, thickness, edge-bead and defect principles, not a particular DUV product recipe.')
source('resist','光阻組成及特性','Composition and properties of photoresists','MicroChemicals','https://www.microchemicals.com/dokumente/application_notes/photoresists_composition_properties.pdf','樹脂、感光成分、溶劑與材料分類。','Resins, photosensitive components, solvents and material classes.')
source('antireflect','光阻抗反射層','Antireflective coatings for photoresists','MicroChemicals','https://www.microchemicals.com/dokumente/application_notes/anti_reflective_coating_photoresist.pdf','基板反射與塗層光學堆疊。','Substrate reflection and coating optical stacks.')
source('softbake','光阻軟烤','Softbake of photoresists','MicroChemicals','https://www.microchemicals.com/dokumente/application_notes/softbake_photoresist.pdf','溶劑移除及熱板與晶圓狀態。','Solvent removal and hotplate-wafer conditions.')
source('peb','曝光後烘烤','Post-exposure bake','MicroChemicals','https://www.microchemicals.com/dokumente/application_notes/photoresist_post_exposure_bake_peb.pdf','曝光後化學反應、擴散與圖案輪廓。','Post-exposure reaction, diffusion and pattern profiles.')
source('develop','光阻顯影','Development of photoresists','MicroChemicals','https://www.microchemicals.com/dokumente/application_notes/development_photoresist.pdf','溶解、相容性、暗蝕與圖案驗證。','Dissolution, compatibility, dark erosion and pattern validation.')
source('imecplace','imec 魯汶總部與官方地圖','imec Leuven headquarters and official map','imec','https://www.imec-int.com/en/connect-with-us/imec-belgium','1984 起源、訪客地址及研究園區代表地點。','1984 origins, visitor address and representative research-campus location.')
source('sumcoplace','SUMCO 東京總部與官方地圖','SUMCO Tokyo headquarters and map','SUMCO','https://www.sumcosi.com/english/corporate/offices/tokyo.html','地址與官方嵌入地圖中心，非切片機位置。','Address and official embedded-map center, not sawing-equipment coordinates.')
source('sumcohistory','SUMCO 沿革','SUMCO history','SUMCO','https://www.sumcosi.com/english/corporate/history.html','1999 公司設立與 2005 更名之公開沿革。','Public 1999 establishment and 2005 renaming milestones.')
source('car','化學放大光阻的發展','Chemical amplification resists: laboratory curiosity to paradigm','Hiroshi Ito / IBM Research','https://research.ibm.com/publications/chemical-amplification-resists-laboratory-curiosity-to-paradigm','原作者回顧之摘要：光酸催化與 DUV 材料發展。','Author review abstract: photoacid catalysis and DUV resist development.')
source('acid','分開量測酸擴散與去保護反應','Decoupling acid diffusion and deprotection','Wallraff et al. / IBM Research','https://research.ibm.com/publications/experimental-method-for-quantifying-acid-diffusion-in-chemically-amplified-resists','原研究摘要：反應與傳輸需以不同觀察區分。','Original research abstract: reaction and transport need distinct observations.')
source('pag','先進圖案化的光酸產生劑','Photoacid generators for advanced patterning','Pandey et al. / IBM Research','https://research.ibm.com/publications/new-photoacid-generators-designed-for-advanced-euv-patterning','2025 摘要：溶解度、酸擴散、感度、粗糙度及隨機缺陷。','2025 abstract: solubility, acid diffusion, sensitivity, roughness and stochastic defects.')
source('upw','電子產業超純水系統','Ultrapure-water systems for electronics','Veolia Water Technologies','https://www.veoliawatertechnologies.com/en/core-markets/electronics-and-photovoltaics','官方搜尋摘錄列出 RO、脫氣、離子交換與 UV；頁面直接讀取回應 403，細節另由 Organo 來源核對。','Official indexed excerpt lists RO, degassing, ion exchange and UV; direct retrieval returned 403, so details are cross-checked against Organo.')
source('upworgano','純水及超純水精製技術','Pure- and ultrapure-water purification technology','Organo','https://product.organo.co.jp/about/strengths/pure-water','不同污染物需要多種分離純化方法；供水與分析共同驗證。','Different contaminants need multiple purification mechanisms; supply and analysis require joint verification.')
COURSES['a008']['sources'] += ['upw','upworgano']

# A second technical teaching point for each stage, separate from the generic evidence-work method.
STAGE_KNOWLEDGE={
'a003':[
'可用片數的理想上限為可用長度除以每片厚度加切縫，實際還須扣除端損及不良片。~Ideal slice count divides usable length by thickness plus kerf; real yield additionally loses end material and rejects.',
'線網的機械耦合使單條線受力改變可能影響相鄰切面，進給穩定性需與導輪狀態一起看。~Mechanical coupling in a wire web means one load change can affect neighboring cuts; inspect feed stability with guide condition.',
'TTV 用兩面的局部間距計算；弓形用中面相對參考面計算，因此厚度均勻的片仍可能彎曲。~TTV measures local separation of both faces while bow describes the median surface; uniform thickness can coexist with curvature.',
'切片端減少切縫的收益，若被後段新增的損傷移除量抵銷，整體矽利用率可能沒有增加。~A smaller kerf may not improve overall silicon utilization if it requires more downstream damage removal.'],
'a005':[
'基板提供晶格模板，但摻雜、殘留氧化物與缺陷會改變新生晶層的電性與完整性。~The substrate provides lattice registry, but doping, oxide and defects affect the new layer’s electrical and structural quality.',
'表面反應與邊界層傳質是串聯的限制；改善其中較快一項可能無法增加總成長速率。~Surface reaction and boundary-layer transport impose serial limits; accelerating the faster process may not raise growth rate.',
'電阻率近似由載子濃度與遷移率乘積決定，因此只量電阻率無法唯一重建深度摻雜輪廓。~Resistivity depends approximately on carrier density times mobility, so resistivity alone cannot reconstruct a unique doping profile.',
'磊晶層的初始缺陷、後段擴散及接觸加工會共同決定元件結果，材料放行需保留熱歷程版本。~Initial epitaxial defects, subsequent diffusion and contact processing jointly determine device outcomes; retain thermal-history versions.'],
'a006':[
'SOI 的支撐晶圓承擔機械功能，埋氧切斷直流通路，頂層提供通道；三者厚度不能只按總厚度驗收。~SOI handle, oxide and top silicon provide support, insulation and channels; total thickness alone cannot accept the stack.',
'分裂深度由佈植輪廓及後續演化共同決定；能量設定是輸入，而完成轉移後的厚度圖才是輸出證據。~Splitting depends on implant profiles and later evolution; implant energy is an input while transferred-thickness maps are output evidence.',
'鍵合空洞改變局部機械支撐與熱路徑；即使頂矽厚度正常，局部空洞仍可能影響後續加工。~Bond voids alter support and heat paths, so normal top-silicon thickness does not eliminate void-related processing risks.',
'埋氧抑制電性耦合的同時也增加垂直熱阻，薄體電晶體的電性比較應包含自熱條件。~Buried oxide reduces electrical coupling while adding vertical thermal resistance; thin-body comparisons should include self-heating.'],
'a007':[
'去除目標可能是表面粒子、溶解金屬或反應殘留；同一粒子掃描器不能提供這三者完整證據。~Targets may be particles, dissolved metals or reaction residues; one particle scanner cannot fully characterize all three.',
'表面反應後的產物仍須移出邊界層；化學反應完成不代表表面已沒有可再沉積物。~Reaction products must leave the boundary layer; completed chemistry does not imply no redepositable material remains.',
'乾燥時液體體積下降會濃縮不揮發物，毛細力又可能使細長結構變形，兩種失效需分開觀察。~Drying concentrates nonvolatile residues and generates capillary deformation; these failure mechanisms need separate observations.',
'清潔驗收要比較污染減少與基底消耗，並確認搬運及排隊後的表面仍符合下一模組要求。~Cleaning acceptance balances contaminant removal against substrate consumption and verifies the surface after transport and queueing.'],
'a008':[
'污染物質量流率為濃度乘流量；濃度相同時，大流量使用點可能接收更大的污染總量。~Contaminant mass flow is concentration times flow, so a high-flow outlet can receive more contaminant at equal concentration.',
'反滲透、離子交換與終端過濾針對不同物種；串聯設計需要追蹤每段去除及新引入的污染。~Reverse osmosis, ion exchange and final filtration target different species; track both removal and added contamination at every stage.',
'循環管內停留時間會把源頭事件延遲至使用點，警報回溯須把管內容積與流量納入。~Pipe residence time delays source events at outlets; excursion tracing needs pipe volume and flow.',
'回收率提高通常降低排放體積，卻可能增加濃水負荷與純化難度，因此水量與品質需共同平衡。~Higher recovery reduces discharge volume but can increase concentrate burden and purification difficulty, requiring joint quantity-quality balancing.'],
'a009':[
'污染控制是來源、傳輸、表面沉積與器件敏感度的串聯問題；控制來源並不自動證明所有傳輸路徑已封閉。~Contamination links sources, transport, deposition and device sensitivity; source control does not prove all transport paths are closed.',
'粒子依慣性、擴散與重力等機制移動，分子污染則另受吸附平衡與化學反應影響。~Particles move through inertia, diffusion and gravity, while molecular contamination also involves adsorption equilibria and reactions.',
'接液材料可能釋出原有污染或吸附後再釋放；材料名稱相同仍需比較潔淨處理與接觸歷史。~Wetted materials can release inherent or previously adsorbed contamination; identical material names do not establish equal cleaning or contact histories.',
'一個缺陷熱點可由局部來源或流場集中造成；排查須把空間分布與事件時間線一起對照。~A defect hotspot can reflect a local source or flow concentration; compare spatial patterns with event timelines.'],
'a010':[
'晶圓製程會反覆回到同類設備，搬運需求因此是有回路的網路問題，而非單向生產線的距離最小化。~Wafers revisit equipment types, making transport a reentrant network problem rather than one-way line-distance minimization.',
'物理移動與資訊確認可能不同步；任務識別碼及冪等重試能避免遺失回覆導致重複搬運。~Physical movement and acknowledgement may differ in time; unique task IDs and idempotent retries prevent duplicate transport after lost replies.',
'路段利用率接近滿載時，微小到達波動可能形成長隊列；提高全廠平均車速不一定解除局部合流瓶頸。~Near-capacity segments can develop long queues under small arrival variations; faster average travel may not resolve a local merging bottleneck.',
'設備吞吐量、尾端等待、錯送率、振動與污染是不同驗收維度，必須在同一代表性工作負載下比較。~Throughput, tail waits, misdelivery, vibration and contamination are distinct acceptance dimensions needing the same representative workload.'],
'a011':[
'熱氧化形成的氧化物同時向原表面上下延伸；截面預算需分開記錄矽消耗與外部厚度增加。~Thermal oxide extends above and below the original surface; separate silicon consumption from outward thickness increase.',
'Deal–Grove 型關係把界面反應與氧化劑穿越氧化層的傳輸串接；極薄層需另檢查模型偏差。~Deal–Grove-type relations combine interface reaction and oxidant transport through oxide; ultrathin films require additional model checks.',
'電容量測反映電性有效堆疊，光學量測依賴折射率模型，兩者一致性可用來檢查介面層假設。~Capacitance reflects an electrical stack while optical measurements depend on refractive-index models; agreement can test interfacial-layer assumptions.',
'氧化也消耗熱預算並改變摻雜輪廓，因此合格氧化層仍可能造成鄰近接面或短通道指標變差。~Oxidation consumes thermal budget and alters dopant profiles, so an acceptable oxide can coexist with degraded junction or short-channel behavior.'],
'a012':[
'串聯介電層滿足電容倒數相加；若介面層電容較小，單純提高上層介電常數的整體收益有限。~Series capacitances add inversely; a small interfacial capacitance limits benefits from raising the upper-layer permittivity.',
'ALD 的自限制反應需以暴露飽和證據確認；觀察到循環成長不等於已排除氣相 CVD 成分。~ALD self-limitation needs exposure-saturation evidence; cyclic growth alone does not rule out a gas-phase CVD contribution.',
'狹窄特徵增加表面積與反應物消耗，入口暴露充分時，深處仍可能需要更長的傳輸時間。~Narrow features increase surface area and reactant demand, so deep regions can require longer transport even with adequate entrance exposure.',
'低 EOT、低漏電及低陷阱密度是不同目標；改變介面處理可能改善其中一項卻犧牲另一項。~Low EOT, leakage and trap density are distinct objectives; an interface treatment may improve one while compromising another.'],
'a013':[
'平帶及閾值由金屬、介電層、半導體與電荷共同決定，不能用單一金屬真空功函數直接替代整個堆疊。~Flat-band and threshold depend on metal, dielectric, semiconductor and charge; vacuum work function cannot replace the whole stack.',
'超薄功函數層可能受成核、晶粒及介面反應影響；材料化學式相同不代表局部有效功函數相同。~Ultrathin work-function layers depend on nucleation, grains and reactions; equal formulas do not ensure equal local effective work function.',
'狹窄閘腔的厚度總和受幾何約束，增加一層材料會減少其他層可用空間並可能形成空洞。~A narrow gate cavity limits total stack thickness; adding one layer reduces space for others and can promote voids.',
'製程造成的初始閾值偏移與偏壓老化漂移需分開記錄，才能判斷改良來自材料設定還是可靠度變化。~Separate initial process-induced threshold shifts from bias-aging drift to distinguish material tuning from reliability changes.'],
'a014':[
'面劑量是深度濃度的積分；相同劑量可透過不同射程展寬形成不同峰值濃度。~Areal dose is the depth integral of concentration; equal doses can have different peaks because of range spread.',
'晶體通道效應與圖案遮蔽是不同方向性問題；改變佈植角度時需同時檢查兩者。~Crystal channeling and pattern shadowing are different directional problems; changing implant angle requires evaluating both.',
'佈植造成的空位及間隙原子會在退火中演化，活化與暫態擴散不能只由初始化學濃度預測。~Implant vacancies and interstitials evolve during annealing; activation and transient diffusion cannot follow from initial chemical concentration alone.',
'SIMS 提供化學輪廓，電性量測反映活化載子與遷移率；兩種資料的深度及面積需一致才能比較。~SIMS gives chemical profiles while electrical measurements reflect active carriers and mobility; align depth and area before comparing.'],
'a015':[
'擴散長度與時間積分的擴散係數相關，因此短而熱與長而冷的處理不能只用最高溫度排序。~Diffusion length relates to integrated diffusivity, so short-hot and long-cool cycles cannot be ranked by peak temperature alone.',
'高溫計將光輻射轉為溫度時需要發射率模型；表面堆疊不同會改變同一訊號的解釋。~Pyrometry converts radiance to temperature using emissivity; different surface stacks change interpretation of the same signal.',
'活化改善可降低片電阻，但缺陷引起的接面漏電可能仍存在；兩者需以獨立結構量測。~Activation can reduce sheet resistance while defect-induced junction leakage remains; measure both using independent structures.',
'退火窗口是活化、擴散及材料耐受的交集，不能只選片電阻最低的條件當作整合最佳值。~The anneal window intersects activation, diffusion and material survival; minimum sheet resistance alone is not an integrated optimum.'],
'a016':[
'熱擴散尺度約與時間平方根成正比；縮短熱脈衝可減少深部受熱，但表面溫度仍需量測。~Thermal diffusion length scales roughly with square-root time; shorter pulses reduce deep heating but still require surface thermometry.',
'固定光斑寬度時，停留時間約為寬度除以掃速；重疊區的累積歷程還需把相鄰掃描相加。~For a fixed beam width, dwell is roughly width divided by speed; overlap history also includes adjacent scans.',
'吸收能量轉為溫升要考慮熱容量、熱擴散與可能相變，因此入射能量不能直接當作局部最高溫。~Temperature rise depends on heat capacity, diffusion and possible phase changes; incident energy is not local peak temperature.',
'金屬與介電圖案的反射及吸收不同，代表性驗證應包含圖案晶圓而非僅有裸矽校準片。~Metal and dielectric patterns differ optically, so representative validation needs patterned wafers beyond bare-silicon calibration.'],
'a017':[
'有限源保持總劑量，固定表面源持續補充摻雜；兩種擴散模型採用不同守恆及邊界條件。~Finite sources conserve dose while fixed-surface sources replenish dopants; the models have different conservation and boundary conditions.',
'晶舟和晶圓增加熱容量，也改變氣流與熱輻射遮蔽，因此空爐校準須經負載條件驗證。~Boats and wafers add thermal mass and change flow and radiation shielding; empty-furnace calibration needs loaded verification.',
'Fick 模型的通量取決於梯度，均勻高濃度區可有低通量，而低濃度但陡梯度區可有顯著通量。~Fickian flux follows gradients: uniform high concentration can have little flux while a low but steep profile can have substantial flux.',
'爐管軸向變異與片內徑向變異對應不同邊界，將兩者混成單一標準差可能遮蔽故障來源。~Axial furnace and radial wafer variation reflect different boundaries; merging them into one deviation can hide fault causes.'],
'a018':[
'隔離必須在截面上切斷非預期導通路徑，溝槽名稱或深度單一數值無法完整描述電性隔離。~Isolation must interrupt unintended conduction paths in section; a trench label or single depth cannot fully describe it.',
'側壁形狀與襯層消耗會改變填充前的實際開口，所以設計圖寬度不能直接代替沉積入口寬度。~Sidewall shape and liner consumption change the prefill opening, so layout width is not necessarily deposition-entry width.',
'填充空洞是內部缺陷，CMP 凹陷是表面形貌；兩者可同時存在，需截面與表面量測各自確認。~Fill voids are internal defects while CMP recess is surface topography; both may coexist and need separate measurements.',
'STI 應力可依主動區到隔離邊界的距離改變元件特性，因此驗收需涵蓋版圖而不只是材料樣片。~STI stress can change devices with distance to isolation; acceptance therefore needs layout coverage beyond material coupons.'],
'a019':[
'應變對輸運的作用依賴方向、載子及能帶；「增加應力」沒有脫離方向與材料的普遍正面意義。~Strain effects depend on direction, carriers and bands; increasing stress has no universal benefit independent of material and direction.',
'晶格失配可先以彈性形變承受，超出可維持範圍後可能藉位錯鬆弛，必須同看應變與缺陷。~Lattice mismatch can remain elastic before relaxing through dislocations; inspect strain and defects together.',
'實際量測具有有限空間平均範圍，模擬的單點峰值需經相同空間平均才適合與量測比較。~Measurements have finite spatial averaging; simulated point peaks need equivalent averaging before comparison.',
'遷移率提高的收益會受接觸及互連限制；元件電流與電路延遲應分層驗證而非直接同比換算。~Contact and interconnect limits constrain mobility gains; validate device current and circuit delay separately rather than scaling them proportionally.'],
'a020':[
'選擇性磊晶同時追求目標表面成長及非目標表面不成核，必須報告兩種表面的結果。~Selective epitaxy requires growth on target surfaces and suppressed nucleation elsewhere; report both surface outcomes.',
'晶面速度不同造成外形演化，圖案密度又改變局部供料，因此截面形貌不能只由沉積時間決定。~Facet-dependent rates and pattern-dependent supply govern shape, so deposition time alone cannot determine the section.',
'鍺比例、活化與晶格鬆弛相互耦合；更高名義摻雜或成分不保證更低接觸電阻及更低漏電。~Germanium fraction, activation and relaxation interact; higher nominal doping or composition does not guarantee lower contact resistance or leakage.',
'奈米片源汲極不只提供載子，也把機械應力與電流接入多層通道，需檢查逐層端點連接。~Nanosheet source-drain provides carriers, stress and current to several channels, requiring per-layer endpoint connectivity checks.'],
'a021':[
'反相器功能來自互補拉高與拉低路徑，井與本體接點則協助維持電位及抑制寄生作用。~An inverter uses complementary pull-up and pull-down paths, while wells and body ties maintain potentials and suppress parasitics.',
'側壁間隔使源汲極處理與閘邊緣形成幾何關聯，但橫向擴散仍會改變電性有效通道長度。~Spacers geometrically relate junction processing to gate edges, but lateral diffusion still changes electrical channel length.',
'接觸與互連把元件接成電路；元件 I-V 合格仍可能因開路、短路或過高寄生而無法工作。~Contacts and interconnects form the circuit; good device I-V can coexist with circuit failure from opens, shorts or parasitics.',
'負載電容充放電需要有限電流；延遲改善須同時考慮驅動、負載、電壓及切換條件。~Finite current charges load capacitance; delay improvements depend on drive, load, voltage and switching conditions.'],
'a022':[
'對近矩形鰭，三面控制的幾何寬度約隨兩倍鰭高加鰭寬改變；實際電性還受各面遷移率影響。~For a near-rectangular fin, geometric gated width scales roughly as twice height plus width; face-dependent mobility also matters.',
'鰭寬、側壁角與隔離回蝕高度共同定義通道截面，三者量測應配準到同一位置。~Fin width, taper and isolation recess jointly define the channel section and need co-registered measurements.',
'三維閘堆疊增加側壁及角落界面，單一平面監控片不能完全代表成核、覆蓋與填充。~Three-dimensional gates add sidewall and corner interfaces; one planar monitor cannot fully represent nucleation, coverage and fill.',
'鰭數是整數，所以標準元件驅動尺寸不是任意連續變數；元件庫需把此量化與配線限制一起設計。~Fin count is integer, so cell drive is not continuously adjustable; libraries must combine this quantization with routing constraints.'],
'a023':[
'奈米片有效通道寬與片周長及片數相關，但片間空間同時限制閘金屬體積。~Effective channel width relates to sheet perimeter and count, while inter-sheet spacing limits gate-metal volume.',
'內間隔在源汲極與可移除犧牲層間提供保護，使後續釋放能避免破壞電流進入端。~Inner spacers protect the source-drain from removable sacrificial layers, preserving current-entry regions during release.',
'釋放讓通道失去原先的連續支撐，也暴露更多表面；機械穩定與表面損傷需要同步驗證。~Release removes continuous support and exposes more surface, requiring simultaneous checks of mechanical stability and surface damage.',
'總電流是多片通道貢獻之和，因此單片退化可能被其他通道遮蔽；需要逐層或敏感測試結構。~Total current sums sheet contributions, so other sheets can mask one degraded channel; use per-layer or sensitive test structures.'],
'a024':[
'CFET 以垂直方向取代部分平面 n-p 間距，但其面積收益取決於可實現的接觸與標準元件佈線。~CFET replaces some lateral n-p spacing vertically, but area benefits depend on realizable contacts and cell routing.',
'中介隔離讓上下閘可具有不同材料與閾值設定；其形成順序又會影響後續源汲極的可達性。~Middle isolation supports different tier-gate materials and thresholds; its sequence also affects source-drain accessibility.',
'底層前側接觸與背側接觸各有不同加工模組，不能只比較導線長度而忽略隔離及薄化成本。~Frontside and backside bottom contacts need different modules; wire-length comparisons alone miss isolation and thinning costs.',
'研究測試車展示功能後，仍需更多樣本驗證變異、存活率與可靠度，才能建立製造成熟度證據。~After functional test-vehicle demonstrations, further samples are needed for variability, survival and reliability evidence.'],
'a026':[
'埋入軌是一種局部供電結構；電源從正面或背面進入是另一個設計維度，需以完整回路判定。~A buried rail is a local power structure; frontside or backside entry is a separate design dimension requiring a complete loop.',
'金屬截面縮小提高電流密度，襯層則減少可用導體面積；幾何與隔離預算需聯合評估。~Smaller metal cross-sections increase current density, while liners reduce usable conductor area; assess geometry and isolation together.',
'埋在前段的金屬會遭遇後續熱處理，選材需同時考慮擴散、應力及介電相容而非只看低電阻。~Metal buried early encounters later heating, so selection needs diffusion, stress and dielectric compatibility beyond low resistance.',
'壓降減少可能釋出電壓裕度，但電流密度、熱點及電遷移仍需獨立驗證長期穩定性。~Reduced drop can free voltage margin, but current density, hotspots and electromigration need separate lifetime validation.'],
'a027':[
'節點比較需要明確 PPA、工作負載及幾何基準，商業名稱與研究預測不可直接充當性能證據。~Node comparisons require explicit PPA, workload and geometry baselines; commercial names and projections are not performance evidence.',
'架構改變會同時影響靜電、電容與加工可達性，單項通道指標的改善不等於整合方案更優。~Architecture changes electrostatics, capacitance and process access; improving one channel metric does not prove a better integrated solution.',
'當接觸與互連占比增加，通道縮放對電路效能的改善可能遞減，需要由元件跨到配線協同設計。~As contacts and interconnects contribute more, channel-scaling gains can diminish, requiring device-routing co-design.',
'模擬、測試結構與量產資料的抽樣範圍不同，研究結論應附樣本、偏壓、模型假設及可重現條件。~Simulations, test structures and production data sample different scopes; state samples, bias, model assumptions and reproducibility conditions.'],
'a028':[
'內間隔在閘與源汲極間提供電性及化學屏障，其長度與介電常數共同影響寄生電容。~Inner spacers form electrical and chemical barriers between gate and source-drain; length and permittivity jointly affect parasitic capacitance.',
'各層凹蝕的平均深度及最差偏差都重要，局部過深會改變存取長度，過淺則減少保護裕度。~Mean and worst-layer recess matter: excessive recess alters access length while shallow recess reduces protection margin.',
'沉積與回蝕必須形成內部保留、外部清除的幾何選擇性，不能只憑全面膜厚判定成功。~Deposition and etchback must retain recessed material while clearing exposed surfaces; blanket thickness cannot establish success.',
'低介電常數材料若在釋放中受損，可能形成源汲極侵蝕路徑，因此電容收益需以化學存活為前提。~A low-k material damaged during release may expose source-drain to attack, so capacitance benefits require chemical survival.'],
'a029':[
'接觸電流可集中在入口附近，傳輸長度將片電阻與界面電阻相連，幾何面積不一定全都有效。~Contact current can crowd near edges; transfer length connects sheet and interface resistance, so not all geometric area is effective.',
'高活化濃度可縮窄能障，但界面氧化、反應相與粗糙度仍可能主導接觸傳輸。~High active doping can narrow barriers while oxide, reacted phases and roughness can still dominate transport.',
'TLM 的斜率與截距需在適當模型下分離片電阻及接觸貢獻，短接觸與有限幾何會改變抽取。~TLM slope and intercept separate sheet and contact contributions within an appropriate model; finite and short contacts affect extraction.',
'低阻尾端與高阻尾端對統計的影響不同，報告中位數、分布及失效比例比只展示最低值更能描述批次。~Distribution tails matter differently; median, spread and failure fraction characterize a lot better than its minimum resistance alone.'],
'a030':[
'自對準保護來自材料選擇性及結構重疊，套刻偏移仍可能縮小落點或增加角落暴露。~Self-alignment relies on material selectivity and overlap; overlay shifts can still reduce landing area or expose corners.',
'方向性蝕刻控制形狀，材料選擇性控制保護層損失，兩種能力需要分開量化。~Directional etching controls shape while selectivity controls protective-layer loss; quantify these capabilities separately.',
'接觸襯層可保護界面卻消耗導體截面，填充完成後仍需檢查空洞與實際連通面積。~Contact liners protect interfaces but consume conductor area; inspect voids and actual connected area after filling.',
'導通、閘隔離及鄰孔隔離是不同電路條件；一種接觸鏈測試不能取代所有漏電與短路檢查。~Continuity, gate isolation and neighbor isolation are different conditions; one chain test cannot replace all leakage and short checks.'],
'a031':[
'旋塗的流動受黏度、離心效應與溶劑揮發共同影響，材料換批後應重新確認曲線而非只沿用轉速。~Spin flow depends on viscosity, centrifugal effects and evaporation; a material-lot change requires curve verification beyond reusing speed.',
'液膜在鋪展與乾燥間轉換，前段加速度及排風因此可能改變最終厚度，即使終轉速不變。~The film transitions from spreading to drying, so acceleration and exhaust can alter final thickness even at fixed final speed.',
'邊珠、背面殘留與氣泡具有不同空間形態，缺陷分類應保留位置而不只計算總數。~Edge beads, backside residues and bubbles have different spatial signatures; retain locations rather than only total defect counts.',
'光阻膜厚與底層反射共同決定內部光場，塗佈端與曝光端需要共用光學堆疊版本。~Resist thickness and underlying reflection determine the internal optical field; coating and exposure should share the stack version.'],
'a032':[
'軟烤調整溶劑與薄膜狀態，PEB 驅動曝光後反應；兩者的合格結果應以各自的物理目的定義。~Softbake adjusts solvent and film state while PEB drives post-exposure reaction; accept each against its own physical purpose.',
'酸催化與酸擴散同時發生，較完全的去保護可能伴隨較大的影像模糊，需要聯合量測。~Acid catalysis and diffusion occur together; more complete deprotection can accompany more blur, requiring joint measurements.',
'顯影產物移除受局部傳質限制，厚膜或細孔的清除不能由平面大開口結果直接預測。~Product removal depends on local transport, so thick-film or small-hole clearance cannot follow directly from large planar openings.',
'尺寸、底部殘膠與側壁角是互補圖案指標；頂視 CD 合格仍可能無法完成後續蝕刻轉移。~CD, bottom scum and sidewall angle are complementary; acceptable top-view CD can still fail later etch transfer.'],
'a033':[
'化學放大將光吸收與多次催化轉換連起來，但產酸效率、淬熄及溶解反應決定有效增益。~Chemical amplification links absorption to multiple catalytic conversions, while acid yield, quenching and dissolution set effective gain.',
'擴散長度與反應速率是不同參數，藉獨立圖案或時間實驗才能避免把反應加快誤判為酸移動更遠。~Diffusion length and reaction rate are different parameters; independent spatial or time experiments avoid confusing faster reaction with farther transport.',
'平均化學反應與少量事件的隨機分布需分開看，低曝光劑量可能增加局部缺陷的不確定度。~Separate average chemistry from sparse-event statistics; low dose can increase uncertainty in local defect formation.',
'候選配方的解析度、粗糙度、感度及蝕刻耐受需在同一基準下比較，不能混用不同最佳條件宣稱全面勝出。~Compare resolution, roughness, sensitivity and etch resistance on the same baseline rather than mixing best conditions to claim universal superiority.']}

# Course-specific engineering handoff: emphasis differs even when two courses share a facility.
FOCUS={
'a003':'切縫、TTV、次表面損傷~Kerf, TTV and subsurface damage',
'a005':'膜厚、摻雜階梯、晶體缺陷~Thickness, doping transitions and crystalline defects',
'a006':'頂矽均勻性、埋氧、鍵合空洞~Top-silicon uniformity, buried oxide and bond voids',
'a007':'去污效果、材料損失、再污染~Removal, material loss and recontamination',
'a008':'水質多指標、使用點、滯留~Water-quality indicators, points of use and stagnation',
'a009':'來源、傳輸與缺陷地圖~Sources, transport and defect maps',
'a010':'載具交握、尾端延遲、故障恢復~Carrier handshakes, tail latency and recovery',
'a011':'氧化消耗、界面陷阱、漏電~Oxidation consumption, interface traps and leakage',
'a012':'EOT、飽和循環、三維覆蓋~EOT, saturated cycles and 3D coverage',
'a013':'有效功函數、閾值分布、閘填充~Effective work function, threshold distribution and gate fill',
'a014':'劑量、射程、損傷及活化~Dose, range, damage and activation',
'a015':'溫度時間軌跡、擴散、片電阻~Temperature-time history, diffusion and sheet resistance',
'a016':'光斑掃描、局部熱峰、圖案吸收~Beam scanning, local thermal peaks and patterned absorption',
'a017':'片位熱場、邊界條件、擴散輪廓~Slot thermal fields, boundary conditions and diffusion profiles',
'a018':'溝槽填充、隔離漏電、應力~Trench fill, isolation leakage and stress',
'a019':'應變張量、載子輸運、鬆弛~Strain tensors, carrier transport and relaxation',
'a020':'選擇性磊晶、晶面、活化接觸~Selective epitaxy, facets and activated contacts',
'a021':'井區、接面及互補電路連通~Wells, junctions and complementary-circuit connectivity',
'a022':'鰭形貌、三面閘及量化驅動~Fin geometry, three-sided gates and quantized drive',
'a023':'片間釋放、環繞閘及逐層差異~Inter-sheet release, wraparound gates and layer variation',
'a024':'上下互補層、中介隔離及分層接觸~Complementary tiers, middle isolation and tier contacts',
'a026':'埋軌隔離、熱相容及壓降~Rail isolation, thermal compatibility and voltage drop',
'a027':'比較基準、架構權衡及證據成熟度~Comparison baselines, architecture tradeoffs and evidence maturity',
'a028':'側向凹蝕、低介電填充及釋放保護~Lateral recess, low-k fill and release protection',
'a029':'活化、界面及比接觸電阻抽取~Activation, interfaces and specific contact-resistivity extraction',
'a030':'套刻容忍、間隔保護及接觸導通~Overlay tolerance, spacer protection and contact continuity',
'a031':'塗佈流動、邊珠、膜厚與缺陷~Coating flow, edge bead, thickness and defects',
'a032':'軟烤、酸擴散、溶解與輪廓~Softbake, acid diffusion, dissolution and profiles',
'a033':'PAG、淬熄、反應擴散與隨機性~PAG, quenching, reaction-diffusion and stochasticity',
}

WRONG={
'wafer':[
'TTV 與表面粗糙度可以互換。~TTV and surface roughness are interchangeable.',
'只量中心厚度即可代表全片形貌。~Center thickness alone represents full-wafer geometry.',
'晶圓表面外觀平整就可排除次表面裂紋。~A flat-looking surface rules out subsurface cracks.',
'切片厚度就是最終成品厚度。~Sliced thickness equals final finished thickness.',
'平均值相同就不必檢查片間分布。~Equal averages eliminate the need to inspect wafer distributions.',
'材料移除量不會影響可用晶圓數。~Material removal cannot affect usable wafer count.',
'局部截面合格就能取代整片量測。~One acceptable section replaces full-wafer measurement.',
'所有表面缺陷都能由後段拋光無代價消除。~All surface defects can be removed by later polishing without cost.'],
'clean':[
'粒子數低就證明金屬離子濃度低。~Low particle counts prove low metal-ion concentration.',
'未檢出代表污染濃度精確為零。~Nondetection means exactly zero contamination.',
'高電阻率足以排除所有有機污染。~High resistivity rules out every organic contaminant.',
'中央站合格即可省略使用點採樣。~Central-system acceptance eliminates point-of-use sampling.',
'濾膜截留尺寸等同所有污染物去除率。~Membrane retention size equals removal efficiency for every contaminant.',
'加強清洗不可能改變基底表面。~Stronger cleaning cannot change the substrate surface.',
'低壓差證明濾芯不存在任何旁通。~Low pressure drop proves no filtration bypass exists.',
'清洗後等待時間不影響再污染。~Queue time after cleaning cannot affect recontamination.'],
'device':[
'總電流合格就證明每個通道都完整。~Acceptable total current proves every channel is intact.',
'頂面膜厚代表所有側壁與底部厚度。~Top thickness represents all sidewall and bottom thicknesses.',
'幾何完整即可省略漏電量測。~Geometric integrity eliminates the need for leakage measurements.',
'接觸面積加倍必定使全部串聯電阻減半。~Doubling contact area must halve all series resistance.',
'節點名稱就是實體閘長的量測值。~The node name is a measured physical gate length.',
'模擬最佳值可直接當成量產良率。~The best simulation value directly represents production yield.',
'單一中層截面可代表所有堆疊層。~One middle-layer section represents every stacked layer.',
'低電阻可自動證明介電隔離完整。~Low resistance automatically proves dielectric isolation.'],
'thermal':[
'峰值溫度相同便有相同擴散預算。~Equal peak temperatures imply equal diffusion budgets.',
'化學摻雜濃度就是活化載子濃度。~Chemical dopant concentration equals active carrier concentration.',
'片電阻下降就證明接面完全無損傷。~Lower sheet resistance proves a damage-free junction.',
'爐壁設定溫度等於晶圓瞬時溫度。~Wall setpoint equals instantaneous wafer temperature.',
'降溫期間不可能再發生擴散。~No diffusion can occur during cooling.',
'所有光學表面可共用不變發射率。~Every optical surface shares one constant emissivity.',
'空載均溫就證明滿載各片均勻。~Empty-furnace uniformity proves loaded-wafer uniformity.',
'相同雷射能量必定產生相同熱峰值。~Equal laser energy must produce equal thermal peaks.'],
'film':[
'沉積循環數總能從第一循環精確線性外推。~Thickness always extrapolates linearly from the first cycle.',
'厚度相同就代表介面電性相同。~Equal thickness implies equal interface electrical quality.',
'入口飽和就證明深槽底部已飽和。~Entrance saturation proves deep-feature bottom saturation.',
'平均成分足以排除局部相分離。~Mean composition rules out local phase separation.',
'高介電常數保證沒有漏電及陷阱。~High permittivity guarantees no leakage or traps.',
'去除上層材料不需檢查下層損失。~Removing an upper layer needs no lower-layer loss check.',
'低塊材電阻率保證低界面接觸電阻。~Low bulk resistivity guarantees low interface contact resistance.',
'較快成長永遠改善圖案選擇性。~Faster growth always improves pattern selectivity.'],
'resist':[
'相同最終轉速一定得到相同膜厚分布。~Equal final spin speed always gives equal thickness maps.',
'軟烤與 PEB 可視為相同化學步驟。~Softbake and PEB are the same chemical step.',
'曝光劑量相同就能排除所有尺寸差。~Equal dose rules out every dimensional difference.',
'頂視開口就證明孔底完全沒有殘膠。~A top-view opening proves no bottom scum.',
'較低劑量必定同時改善解析度與粗糙度。~Lower dose must improve resolution and roughness together.',
'平均線寬合格即可忽略橋接與缺孔。~Acceptable mean width permits ignoring bridges and missing holes.',
'顯影液相容性可由顏色直接判斷。~Developer compatibility follows directly from color.',
'增加酸擴散永遠只會改善圖案。~More acid diffusion can only improve patterns.'],
'amhs':[
'平均車速較快就保證所有任務延遲下降。~Higher mean speed guarantees lower delay for every task.',
'交握超時就代表載具尚未移動。~Handshake timeout means the carrier has not moved.',
'任務重試可以建立新的實體取貨而不核對狀態。~Retries can start another pickup without state reconciliation.',
'最短路徑自動保證沒有資源死鎖。~Shortest paths automatically prevent resource deadlock.',
'已派工與已送達可使用同一狀態。~Assigned and delivered can share one state.',
'只需驗證產能，不必量測搬運潔淨度。~Throughput alone suffices without transport cleanliness checks.',
'中位延遲合格就不會有嚴重逾時。~An acceptable median excludes severe timeouts.',
'系統重啟可以跳過實體位置核對。~Restart can skip verification of physical positions.']}

def split(s):
    a,b=s.split('~',1); return a,b
def family(cid):
    n=int(cid[1:])
    if n<=6:return 'wafer'
    if n<=9:return 'clean'
    if n==10:return 'amhs'
    if n in (14,15,16,17):return 'thermal'
    if n in (5,11,12,13,19,20,28,29,30):return 'film'
    if n>=31:return 'resist'
    return 'device'

METHODS=[
('因果圖','Causal diagram','畫一張含作用前後狀態的原創圖；以箭頭標出本步原理中的因果關係；圈出一項仍需量測的未知量。','Draw an original before/after diagram; mark the causal relationship in this step; circle one quantity still requiring measurement.','圖中要有邊界、輸入、輸出與一項不能僅由圖決定的量。','Show boundaries, inputs, outputs and one quantity that the diagram alone cannot determine.','只有外觀相似不能證明材料狀態或連通性相同。','Similar appearance does not prove equal material state or connectivity.'),
('對照表','Controlled comparison','建立兩個只改一項條件的假想案例；分開記錄可觀察差異與推測原因；說明如何用本步原理區分兩者。','Create two hypothetical cases differing in one condition; separate observations from proposed causes; use this step’s principle to distinguish them.','交出兩案例、固定條件、預期差異及一項可能混淆因素。','Submit both cases, fixed conditions, predicted difference and one confounder.','比較時改變多項條件會使因果結論不唯一。','Changing several conditions makes causal interpretation nonunique.'),
('敏感度草圖','Sensitivity sketch','選出本步的一項輸入及一項輸出；以自訂低、中、高三點畫趨勢；逐點標註假設，並寫出趨勢可能失效的條件。','Select one input and output for this step; sketch a hypothetical low/mid/high trend; label assumptions and state when the trend may fail.','圖須有變數、單位或無因次定義、三個假設點及適用範圍。','Include variables, units or dimensionless definitions, three hypothetical points and validity limits.','自行設定的數值只用於檢查模型，不能當作廠商規格。','Chosen values test a model; they are not manufacturer specifications.'),
('故障判別表','Fault-discrimination table','假設本步預期結果未出現；提出兩個不同機制；為各機制選一個能支持或否定的觀察，避免只重複同一量測。','Assume the expected result fails; propose two distinct mechanisms; choose an observation that supports or rejects each rather than repeating one measurement.','至少列出兩個假說、各自的辨別證據及先檢查順序。','List two hypotheses, discriminating evidence for each and a check order.','相關性可縮小排查範圍，但須獨立證據才能建立因果。','Correlation narrows diagnosis; causal claims need independent evidence.'),
('量測規劃','Measurement plan','針對本步定義待測量及採樣位置；列出解析度、背景與重複性；設計一個見證或空白，並說明檢出限如何限制結論。','Define the measurand and sampling locations; list resolution, background and repeatability; design a witness or blank and explain detection-limit constraints.','提供採樣座標、量測單位、對照與不確定度來源。','Provide sampling coordinates, units, controls and uncertainty sources.','未檢出或平均合格不能排除低於解析度或局部的異常。','Nondetection or an acceptable mean cannot exclude unresolved or local anomalies.'),
('工程驗收單','Engineering acceptance sheet','整合本步及本階段先前證據；提出兩項彼此不同的接受條件；再列一個會讓你暫緩放行的結果及下一個確認動作。','Combine this step with earlier stage evidence; propose two independent acceptance criteria; name one hold condition and the next confirming action.','驗收單需有原理、兩項證據、保留疑問及前後模組交接。','The sheet needs the principle, two evidence items, open questions and module handoff.','幾何、材料與電性是互補證據，不能任選一項代表全部。','Geometry, materials and electrical behavior are complementary evidence, not interchangeable substitutes.')]

STEP_MISCONCEPTIONS={
    ('a003',20):[
        '只要每批總線耗下降，即使合格片數下降更多，也可判定單位合格片的線耗改善。~Lower total wire use per batch proves better wire use per accepted wafer even if accepted output falls by a larger fraction.',
        '比較線耗時只需計入切出的片數，不必區分後續判退與合格片。~Wire-use comparisons need only the number of sliced wafers, without separating subsequent rejects from accepted wafers.'],
    ('a012',20):[
        '閘極電容提高就足以證明載子遷移率提高，不必檢查散射或陷阱。~Higher gate capacitance alone proves higher carrier mobility without checking scattering or traps.',
        '兩種介電堆疊只要 EOT 相同，其介面散射與有效遷移率就必定相同。~Two dielectric stacks with equal EOT must have identical interface scattering and effective mobility.'],
    ('a024',20):[
        '上下層各自都有正常的電晶體電流曲線，就足以證明接成反相器後的轉移曲線正確。~Valid transistor current curves for both tiers alone prove that the connected inverter has a correct transfer curve.',
        '轉移曲線只要穿過輸入與輸出皆為 VDD/2 的點，就不必再檢查轉換斜率或雜訊容限。~A transfer curve crossing the point where input and output both equal VDD/2 needs no further slope or noise-margin assessment.']}

def build_step(cid,row,index,keys):
    ti,pr=row.split('|');z,e=split(ti);k,ke=split(pr)
    mid=index%6; typ,tye,act,acte,accept,accepte,method_boundary,method_boundary_en=METHODS[mid]
    k2,k2e=split(STAGE_KNOWLEDGE[cid][index//6])
    fam=WRONG[family(cid)]; bad=[split(fam[(index//6*2)%len(fam)]),split(fam[(index//6*2+1)%len(fam)])]
    if (cid,index+1) in STEP_MISCONCEPTIONS:
        bad=[split(x) for x in STEP_MISCONCEPTIONS[(cid,index+1)]]
    if cid=='a024' and index==19:
        act+='本步反相器轉移曲線一律為自訂教學模型；在圖上標示假想 VDD 與輸入輸出，不將曲線歸屬為 imec 實測資料。'
        acte+=' All inverter transfer curves in this exercise are hypothetical teaching models. Label the assumed VDD, input and output; do not attribute these curves to imec measurements.'
    a=index%3;opts=[x[0] for x in bad];optsen=[x[1] for x in bad];opts.insert(a,k);optsen.insert(a,ke)
    sid=f'{cid}-v8-{index+1:02d}'
    focusz,focuse=split(FOCUS[cid])
    return dict(id=sid,order=index+1,sequence=index+1,estimatedMinutes=30,simulationOnly=True,
        sourceIds=['v8a-'+x for x in keys],prerequisiteIds=[] if index==0 else [f'{cid}-v8-{index:02d}'],
        title=z,titleEn=e,objective=f'完成「{z}」的{typ}，把{focusz}中的相關限制連到可觀察證據。',objectiveEn=f'Complete a {tye.lower()} for {e.lower()}, connecting relevant limits in {focuse.lower()} to observable evidence.',
        instruction=f'本步問題：{z}。{act}判讀依據：{k}引用列出的原始資料；若使用數值，清楚標成自訂教學假設。',
        instructionEn=f'Question for this step: {e}. {acte} Interpretation: {ke} Cite the listed primary material; label any chosen numbers as hypothetical educational inputs.',
        observation=f'檢查結果是否能支持「{k}」；若證據不足，標記尚未確定並寫出缺少的量測。',observationEn=f'Check whether the evidence supports: {ke} If insufficient, mark the conclusion unresolved and name the missing measurement.',
        failure=f'常見錯判：{bad[0][0]} 應回到「{z}」的假設與採樣範圍，補足能區分機制的證據。',failureEn=f'Common misinterpretation: {bad[0][1]} Revisit assumptions and sampling for {e.lower()} and add discriminating evidence.',
        check=f'交付「{z}」{typ}：{accept}',checkEn=f'Submit the {tye.lower()} for {e.lower()}: {accepte}',
        knowledge=[dict(id=sid+'-k1',title=z+'的原理',titleEn=e+' principle',text=k,textEn=ke),dict(id=sid+'-k2',title='本階段的機制與工程權衡',titleEn='Stage mechanisms and engineering tradeoffs',text=k2,textEn=k2e)],
        quiz=dict(question=f'評估「{z}」時，哪項敘述可以採用？',questionEn=f'Which statement is valid when evaluating {e.lower()}?',options=opts,optionsEn=optsen,answer=a,explanation=f'{k} {k2}',explanationEn=f'{ke} {k2e}'))

def ref(key):
    s=SOURCES[key];return {k:s[k] for k in ('title','titleEn','publisher','url')}

# Explicit original exercises deepen one key measurement or engineering decision in every course.
# These data are invented for teaching and never represented as fab or supplier measurements.
WORKED={
'a003':(3,'自訂算例：可用晶棒長 100 mm、切片厚 0.8 mm、切縫 0.2 mm；先求理想片數，再將切縫改為 0.25 mm 比較整數片數，列出尚未納入的端損與不良片。','Hypothetical exercise: usable ingot length 100 mm, slice thickness 0.8 mm and kerf 0.2 mm. Calculate ideal integer count, change kerf to 0.25 mm and list excluded end losses and rejects.'),
'a005':(15,'自訂算例：假設同一材料的活化載子濃度加倍、遷移率降為原來的 0.8；以電導率與兩者乘積成正比估算變化，再說明為何仍需深度輪廓。','Hypothetical exercise: active carrier density doubles while mobility becomes 0.8 of its original value. Estimate conductivity change from their product and explain why a depth profile is still needed.'),
'a006':(3,'自訂厚度帳：頂矽轉移後 120 個任意厚度單位、修整消耗 15、後續氧化消耗矽 5；求剩餘量，再檢查是否有把氧化物厚度誤當成矽消耗。','Hypothetical thickness ledger: transferred top silicon 120 arbitrary units, finishing consumes 15 and later oxidation consumes 5 silicon units. Compute the remainder and check that oxide thickness was not confused with silicon consumption.'),
'a007':(19,'自訂缺陷圖：同一掃描區清洗前 40 顆、後 18 顆，其中 10 顆位置重合。分開計算留存、移除與新生顆粒；說明為何只相減會漏掉新增污染。','Hypothetical matched defect maps: 40 particles before, 18 after, with 10 co-located. Separate retained, removed and added particles and explain why simple subtraction hides new contamination.'),
'a008':(8,'自訂守恆題：進水 100 L/min、產水 75 L/min、濃水 25 L/min；在無其他支流假設下檢查流量守恆及回收率，另列污染濃度資料才能求質量流率。','Hypothetical balance: feed 100 L/min, permeate 75 L/min and concentrate 25 L/min. Check flow conservation and recovery assuming no other streams; list concentration data needed for contaminant mass balance.'),
'a009':(4,'自訂暴露模型：先假設沉積通量與濃度成正比。案例甲濃度 2、時間 3，案例乙濃度 1、時間 8；比較相對暴露，再列使此線性模型失效的吸附飽和情況。','Hypothetical exposure model: deposition flux is proportional to concentration. Compare relative exposures for concentration/time pairs (2,3) and (1,8), then state how adsorption saturation could invalidate linearity.'),
'a010':(21,'自訂延遲資料：九次任務均 20 s，一次 200 s；計算平均與中位數，保留最大值，再設計會揭露尾端問題的報表欄位。','Hypothetical latency data: nine tasks take 20 s and one takes 200 s. Compute mean and median, retain the maximum, and design a report exposing tail delays.'),
'a011':(2,'自訂幾何模型：假設氧化物厚度 100 個單位、矽消耗為其 0.44 倍；以原表面為零畫出新界面與外表面。0.44 是近似體積換算，非本課量測值。','Hypothetical geometry: oxide thickness 100 units and silicon consumption 0.44 times that thickness. Mark the new interface and outer surface relative to the original surface. The 0.44 is an approximate volume conversion, not course measurement data.'),
'a012':(2,'自訂電容模型：令介面與上層電容分別為 2 與 8 個單位；算串聯總電容，再將上層增為 16。比較收益並說明瓶頸。','Hypothetical capacitance model: interface and upper-layer capacitances are 2 and 8 units. Calculate series capacitance, increase the upper layer to 16 and identify the limiting contribution.'),
'a013':(18,'做一張閾值歸因表：列金屬功函數、介面電荷及通道摻雜三個可能原因；為各原因分別指定材料分析、C-V 或摻雜輪廓的辨別證據。','Build a threshold-attribution table for metal work function, interface charge and channel doping. Assign discriminating materials, C-V or doping-profile evidence to each.'),
'a014':(1,'自訂積分題：假設一段厚 10 nm 的均勻區濃度為 10^19 cm^-3；先把厚度換成 cm，再求面劑量，並解釋此方盒輪廓不是實際佈植高斯輪廓。','Hypothetical integral: a uniform 10 nm region has concentration 10^19 cm^-3. Convert thickness to cm and compute areal dose; explain why this box profile is not a real implantation Gaussian.'),
'a015':(3,'自訂兩段熱歷程：用任意擴散係數 D1=1、D2=4 與時間 t1=4、t2=1 比較 D×t；說明同一擴散積分仍不證明活化或缺陷演化相同。','Hypothetical thermal histories: compare D×t for arbitrary diffusivities D1=1, D2=4 and times t1=4, t2=1. Explain why equal integrated diffusion does not prove equal activation or defect evolution.'),
'a016':(8,'自訂掃描幾何：光斑寬 0.1 mm、掃速 100 mm/s；求單點名義停留時間，再把掃速加倍，並列出需另外處理的重疊與光斑非均勻。','Hypothetical scan: beam width 0.1 mm and speed 100 mm/s. Compute nominal dwell, double the speed, and list overlap and beam nonuniformity effects requiring separate treatment.'),
'a017':(14,'自訂有限源擴散：總劑量固定時，將高斯標準差加倍；推導峰值應如何變化，並用積分面積檢查。','Hypothetical finite-source diffusion: double Gaussian standard deviation at fixed total dose. Derive the peak change and verify by integrated area.'),
'a018':(15,'畫四張原創截面：完整填充、內部空洞、表面碟形凹陷、兩者同時存在；為每張安排截面及表面量測，不能只憑頂視放行。','Draw four original sections: sound fill, internal void, surface dishing, and both. Assign cross-sectional and surface measurements without accepting from top view alone.'),
'a019':(1,'自訂小應變：長度由 100.00 變為 100.10 單位；計算軸向應變，再說明為何缺少彈性常數及邊界條件時不能唯一求應力。','Hypothetical small strain: length changes from 100.00 to 100.10 units. Calculate axial strain and explain why stress is not uniquely known without elastic constants and boundaries.'),
'a020':(13,'設計兩張同平均鍺比例、不同深度梯度的示意圖；指出平均成分量測無法區分之處，再選深度或繞射證據進行辨別。','Sketch two depth profiles with equal mean germanium fraction but different gradients. Identify what average composition cannot distinguish and choose depth-resolved or diffraction evidence.'),
'a021':(21,'用簡化充電模型 t≈CΔV/I 比較相同電流下負載電容加倍的延遲；再列實際反相器中電流不是常數的限制。','Use t≈CΔV/I to compare delay when capacitance doubles at fixed current. Then state the limitation that current is not constant in a real inverter.'),
'a022':(2,'自訂矩形鰭：高 30、寬 8 個單位。用 2H+W 比較一鰭與二鰭幾何有效寬度，再列各面遷移率、接觸及電容使電流不等比例的原因。','Hypothetical rectangular fin: height 30 and width 8 units. Use 2H+W to compare one and two fins, then explain nonproportional current from face mobility, contacts and capacitance.'),
'a023':(4,'自訂間隙預算：片間距 20 個單位，兩側各需介電 2、功函數層 3；算中間剩餘填充空間，再讓每側功函數層各增加 1 單位檢查裕度。','Hypothetical gap budget: spacing 20 units, each face needs dielectric 2 and work-function metal 3. Calculate remaining fill space and test margin after increasing each face’s work-function layer by 1 unit.'),
'a024':(3,'畫平面互補元件與 CFET 兩個相同輸入輸出的反相器；在每圖標出上下或左右源汲極、閘、VDD、VSS 與輸出。用連通性而非外形證明功能一致。','Draw planar and CFET inverters with identical inputs and outputs. Mark source-drain, gates, VDD, VSS and output on each. Establish equivalent function through connectivity rather than shape.'),
'a026':(19,'自訂串聯供電：三段電阻 1、3、6 個單位且電流為 2；逐段算 I×R，再比較只把最小段與最大段各減半的總改善。','Hypothetical series supply: resistances 1,3,6 units and current 2. Calculate each I×R drop and compare halving only the smallest versus largest segment.'),
'a027':(4,'自行建立三個候選架構的正規化 PPA 表，包含一個低功耗但面積較大方案；標明全部是假設，找出 Pareto 不被支配集合而非加總不相容單位。','Create hypothetical normalized PPA data for three architectures including a low-power, larger-area option. Identify the nondominated Pareto set rather than adding incompatible units.'),
'a028':(3,'以平行板近似 C∝kA/d 做相對比較：固定面積，將 k 降為 0.8、間距降為 0.8；求電容比，說明低 k 與幾何縮放可能互相抵銷。','Use relative C∝kA/d at fixed area: both k and spacing become 0.8 of their initial values. Compute the ratio and explain cancellation between lower k and geometric scaling.'),
'a029':(13,'自訂長接觸 TLM：總電阻對間距的直線截距為 20 Ω。於兩接觸相同且寄生已去除假設下，求單接觸電阻；說明未有寬度與片電阻時不能直接得到比接觸電阻。','Hypothetical long-contact TLM: resistance-versus-spacing intercept is 20 Ω. With equal contacts and removed parasitics, find one contact resistance; explain why width and sheet resistance are still needed for specific contact resistivity.'),
'a030':(4,'自訂一維落點：目標區寬 40、孔寬 20 單位；先求完全落入的中心偏移上限，再討論為何選擇性保護只能改變部分失效邊界。','Hypothetical 1D landing: target width 40 and opening width 20 units. Find the center-offset limit for full landing, then explain why selective protection changes only some failure boundaries.'),
'a031':(10,'僅作經驗模型練習：假設 h∝ω^-1/2；把轉速加倍，求相對膜厚，再列黏度、揮發及加速度改變時必須重新校準的原因。','Empirical model exercise only: assume h∝ω^-1/2. Double speed and calculate relative thickness, then state why viscosity, evaporation and acceleration changes require recalibration.'),
'a032':(9,'自訂一維擴散模型 L=√(2Dt)，固定 D 且時間增加四倍；求 L 的比例，再說明實際 PEB 中反應及淬熄為何使此模型不完整。','Hypothetical 1D diffusion L=√(2Dt): hold D fixed and quadruple time. Find the L ratio and explain why reaction and quenching make this incomplete for actual PEB.'),
'a033':(13,'以理想 Poisson 事件模型比較平均事件數 100 與 25 的相對波動 1/√N；說明這是光子統計類比，不能直接當成實際缺陷率。','Use an ideal Poisson model to compare relative fluctuation 1/√N for mean counts 100 and 25. Explain that this photon-statistics analogy is not an actual defect-rate prediction.')}

def place_for(cid):
    # Reuse the previously validated official imec visitor-map point, with a new explicit scope.
    template=json.loads((ROOT/'tools/expansion-v7/technology.json').read_text())['places'][0]['place']
    p=copy.deepcopy(template)
    p['name']='imec 魯汶研究園區（半導體研究代表點）';p['nameEn']='imec Leuven campus (representative semiconductor research location)'
    p['coordinateScope']='官方訪客地圖的約略園區代表點；僅提供半導體研究的地理背景，不表示本課每項製程在此量產，也不是設備位置。'
    p['coordinateScopeEn']='Approximate campus reference from the official visitor map; geographic context for semiconductor research, not a claim that every course process is manufactured here or an equipment location.'
    history=[dict(year='1984',title='imec 的魯汶起點',titleEn='imec begins in Leuven',text='官方總部介紹將 1984 年列為魯汶研究園區故事的起點。',textEn='The headquarters page identifies 1984 as the beginning of imec in Leuven.',sourceIds=['v8a-imecplace']),dict(year='2019',title='公開元件縮放研究',titleEn='Public device-scaling research',text='imec 公開比較 FinFET、奈米片及 CFET 的研究路徑；此時間點屬研究歷程，非本課全部工法的發明日期。',textEn='imec published comparisons of FinFET, nanosheet and CFET research paths; this is a research milestone, not the invention date of every process in this course.',sourceIds=['v8a-scaling'])]
    keys=['imecplace','scaling']
    if cid in ('a003','a005','a006'):
        p=dict(name='SUMCO 東京總部（晶圓供應商代表點）',nameEn='SUMCO Tokyo headquarters (wafer-supplier reference)',city='東京',cityEn='Tokyo',country='日本',countryEn='Japan',lat=35.649972,lng=139.746491,address='日本東京都港區芝浦 1-2-1 Seavance North，105-8634',addressEn='Seavance North, 1-2-1 Shibaura, Minato-ku, Tokyo 105-8634, Japan',mapQuery='SUMCO Seavance North, 1-2-1 Shibaura, Tokyo',coordinateScope='官方聯絡頁嵌入地圖的約略中心；是總部與供應鏈代表點，不是實際切片、磊晶或 SOI 生產設備座標。',coordinateScopeEn='Approximate center of the official embedded map; headquarters and supply-chain reference, not sawing, epitaxy or SOI equipment coordinates.')
        history=[dict(year='1999',title='300 mm 晶圓事業公司成立',titleEn='A 300 mm wafer company is established',text='官方沿革記載合資公司在 1999 年成立以開發及生產 300 mm 矽晶圓。',textEn='The official history records the 1999 formation of a joint venture for 300 mm wafer development and manufacturing.',sourceIds=['v8a-sumcohistory']),dict(year='2005',title='更名 SUMCO',titleEn='Renamed SUMCO',text='官方沿革列示 2005 年更名；此為供應商歷史，不是切片或 SOI 技術起源。',textEn='The history records the 2005 renaming; this is supplier history, not the origin of slicing or SOI.',sourceIds=['v8a-sumcohistory'])]
        keys=['sumcoplace','sumcohistory','sumco']
    if cid=='a010':
        p=dict(name='Daifuku 大阪總部（搬運系統供應商代表點）',nameEn='Daifuku Osaka headquarters (transport-system supplier reference)',city='大阪',cityEn='Osaka',country='日本',countryEn='Japan',lat=34.715738,lng=135.457823,address='日本大阪市西淀川區御幣島 3-2-11，555-0012',addressEn='3-2-11 Mitejima, Nishiyodogawa-ku, Osaka 555-0012, Japan',mapQuery='Daifuku, 3-2-11 Mitejima, Osaka',coordinateScope='座標採官方頁嵌入地圖的約略代表點；是公司總部，不是公開可操作的晶圓廠搬運軌道。',coordinateScopeEn='Approximate reference from the official embedded map; corporate headquarters, not publicly operable wafer-fab tracks.')
        history=[dict(year='1937',title='公司成立',titleEn='Company establishment',text='官方公司資料列示成立於 1937 年；半導體自動搬運是其後發展的應用。',textEn='Official corporate data records establishment in 1937; semiconductor transport is a later application.',sourceIds=['v8a-daifuku']),dict(year='公開技術資料',title='從搬運設備到控制系統',titleEn='From transport equipment to control systems',text='官方無塵室頁分別展示 AMHS、MCS 與 OHT 控制影片，提示物理搬運與資訊協調必須共同設計；此項不指定未查證發明年份。',textEn='The official cleanroom page presents AMHS, MCS and OHT controller videos, showing the need to co-design transport and information coordination; no unverified invention year is assigned.',sourceIds=['v8a-amhs'])]
        keys=['daifuku','amhs']
    f,fe=split(FOCUS[cid]);name=CAT[cid]['title'];en=CAT[cid]['titleEn']
    return dict(courseId=cid,place=p,summary=f'以{name}為入口，追蹤{f}。地圖定位公開機構的代表據點，幫助理解研究與供應鏈分工；課程取材跨多個原始來源，不主張此處是唯一發明地或實際量產現場。',summaryEn=f'{en} explores {fe.lower()}. The map locates a public institutional reference to explain research and supply-chain roles. This course draws on multiple original sources and does not claim an exclusive invention site or actual production location.',connection=f'相近課程可轉移的是{f}的證據推理；各材料、幾何與熱限制仍需重新設定。',connectionEn=f'Transfer the evidence reasoning around {fe.lower()} to related courses while redefining material, geometry and thermal constraints.',history=history,references=[ref(x) for x in keys],sourceIds=['v8a-'+x for x in keys])

RELATED_NOTES={
'a003':'切片留下的損傷與形貌會成為拋光及磊晶的來料條件。~Slicing damage and geometry become incoming conditions for polishing and epitaxy.',
'a005':'磊晶成長與選擇性 SiGe 共用表面成核及傳質問題，並連到應變設計。~Epitaxy and selective SiGe share nucleation and transport questions and connect to strain design.',
'a006':'SOI 層轉移結合佈植定位及薄化表面品質。~SOI layer transfer combines implant-depth placement with thinning and surface quality.',
'a007':'清洗效果同時受超純水品質與環境再污染限制。~Cleaning is limited by ultrapure-water quality and environmental recontamination.',
'a008':'使用點水質會直接影響清洗末段與晶圓污染。~Point-of-use water quality directly affects final cleaning and wafer contamination.',
'a009':'清洗移除污染，搬運則決定再暴露及傳播路徑。~Cleaning removes contamination while transport determines re-exposure and spreading.',
'a010':'自動搬運把污染暴露與製程排程等待時間連在一起。~Automated transport connects contamination exposure with process queue time.',
'a011':'氧化成長提供介電界面，也受到爐內熱場均勻性限制。~Oxidation creates dielectric interfaces and depends on furnace thermal uniformity.',
'a012':'介面層與金屬閘共同決定電容、閾值及漏電。~Interfacial layers and metal gates jointly set capacitance, threshold and leakage.',
'a013':'功函數材料需同時適合高介電界面及奈米片狹窄空間。~Work-function materials must suit high-k interfaces and narrow nanosheet gaps.',
'a014':'佈植既可設定摻雜輪廓，也可在 SOI 層轉移中形成弱化深度。~Implantation can set dopant profiles or define weakening depth for SOI transfer.',
'a015':'快速熱與雷射退火共用活化、擴散及熱不確定度的判讀。~Rapid thermal and laser anneals share activation, diffusion and thermal-uncertainty reasoning.',
'a016':'雷射局部熱歷程可用於活化及接觸工程，均需檢查下層相容性。~Localized laser heating can support activation and contacts, with buried-layer compatibility checks.',
'a017':'爐內均勻性影響氧化及擴散；快速熱處理改變時間尺度而非取消熱物理。~Furnace uniformity affects oxidation and diffusion; rapid processing changes timescales rather than removing thermal physics.',
'a018':'隔離區形貌與應力會傳入平面 CMOS 的閘與接面。~Isolation geometry and stress propagate into planar CMOS gates and junctions.',
'a019':'SiGe 源汲極與 FinFET 幾何共同決定應變如何傳入通道。~SiGe source-drain and FinFET geometry jointly determine strain transfer to the channel.',
'a020':'選擇性源汲極磊晶把應變工程與內間隔保護連在一起。~Selective source-drain epitaxy connects strain engineering to inner-spacer protection.',
'a021':'平面與鰭式 CMOS 共用互補功能及隔離需求，但電場與三維加工不同。~Planar and fin CMOS share complementary function and isolation needs but differ in fields and 3D processing.',
'a022':'從平面到 FinFET 再到 GAA，閘控制面數、有效寬度與加工可達性一起改變。~From planar to FinFET to GAA, gate coverage, effective width and process access change together.',
'a023':'GAA 依靠內間隔及釋放；CFET 再加入互補元件的垂直隔離。~GAA depends on inner spacers and release; CFET adds vertical isolation between complementary devices.',
'a024':'CFET 把奈米片元件與背面接觸需求連在一起。~CFET connects nanosheet devices with backside-contact requirements.',
'a026':'埋入軌與背面供電需共同控制電源接觸及電阻預算。~Buried rails and backside power share power-contact and resistance-budget requirements.',
'a027':'次二奈米研究需比較元件、供電及 CFET 架構的整合證據。~Sub-2-nm research compares integration evidence for devices, power and CFET architectures.',
'a028':'內間隔保護源汲極，使 GAA 犧牲層能在保留通道下移除。~Inner spacers protect source-drain during sacrificial-layer removal while preserving GAA channels.',
'a029':'源汲極磊晶與接觸孔形成共同限制有效接觸面積及界面。~Source-drain epitaxy and contact openings jointly constrain contact area and interfaces.',
'a030':'接觸孔需要低阻連通，也須像隔離模組一樣防止非預期短路。~Contacts need low-resistance connectivity and isolation against unintended shorts.',
'a031':'旋塗初始膜厚會影響後續烘烤、顯影與光阻反應。~Initial spin-coated thickness affects later baking, development and resist reaction.',
'a032':'烘烤顯影把塗佈膜與化學放大配方轉成可轉移圖案。~Bake and development convert coated films and amplified chemistry into transferable patterns.',
'a033':'光阻配方的反應擴散必須與塗佈、烘烤及顯影共同驗證。~Resist reaction-diffusion must be validated with coating, baking and development.'}

def related_for(cid,cfg):
    z,e=split(RELATED_NOTES[cid]); ownz,owne=split(FOCUS[cid]);items=[]
    for j,target in enumerate(cfg['related']):
        assert target in CAT,(cid,target)
        tz,te=CAT[target]['title'],CAT[target]['titleEn'];targetf=FOCUS.get(target,tz+'~'+te);tf,tfe=split(targetf)
        keys=list(dict.fromkeys(cfg['sources']+(COURSES.get(target,{}).get('sources',[]))))
        items.append(dict(id=target,transfer=z,transferEn=e,difference=f'本課驗收重點是{ownz}；「{tz}」則以{tf}為另一個工作包。共用原理不代表可照搬尺寸、材料或接受門檻。',differenceEn=f'This course emphasizes {owne.lower()}; {te} treats {tfe.lower()} as a different work package. Shared principles do not justify copying dimensions, materials or acceptance limits.',practice=[f'畫出{CAT[cid]["title"]}與{tz}之間的材料或資料交接',f'用「{split(cfg["rows"][j*6].split("|")[0])[0]}」作為兩課比較起點，列出一項相同與一項不同邊界',f'選一項{ownz}的觀察，說明還需哪個{tz}證據才可放行'],practiceEn=[f'Draw the material or data handoff between {CAT[cid]["titleEn"]} and {te}',f'Use {split(cfg["rows"][j*6].split("|")[0])[1].lower()} to identify one shared and one different boundary',f'Choose an observation from {owne.lower()} and state which additional {te} evidence is needed for acceptance'],referenceUrls=[SOURCES[x]['url'] for x in keys[:5]]))
    return dict(courseId=cid,related=items,references=[ref(x) for x in cfg['sources']])

def build():
    result=dict(courses=[],sources=[],places=[],related=[],media=[])
    for cid,cfg in COURSES.items():
        c=copy.deepcopy(CAT[cid]);c.pop('researchPlan',None)
        focus,enfocus=split(FOCUS[cid])
        c.update(status='guided',contentStatus='reviewable-educational-curriculum',curriculumVersion=8,depth=4,stepCount=24,estimatedMinutes=720,simulationOnly=True,languageCoverage=['zh-TW','en'],sourceIds=['v8a-'+x for x in cfg['sources']],
            summary=f'以 4 階段、24 個工程工作包拆解{focus}，完成圖解、對照、敏感度分析、故障判別、量測規劃與驗收。',summaryEn=f'Four stages and 24 work packages explore {enfocus.lower()} through diagrams, comparisons, sensitivity studies, fault diagnosis, measurement plans and acceptance reviews.',
            scope='依公開原理編寫的雙語概念實作課；每步交付可審查的工程證據。24 步是學習拆解，不代表晶圓廠的完整配方。自行設定的數值須標為假設。題目不含可直接操作的化學混配、設備設定或量產公差；照片與外部影片為代表媒體，不是假稱每步實拍。',
            scopeEn='Bilingual conceptual exercises based on public principles, with reviewable evidence at each step. The 24 steps are a learning decomposition, not a complete fab recipe. Chosen numerical inputs must be labeled hypothetical. No directly operable chemical mixtures, equipment settings or production tolerances are supplied. Photos and external videos are representative media, not claimed as recordings of every step.',
            diagram=dict(type='wafer',labels=[split(x)[0] for x in cfg['stages']],labelsEn=[split(x)[1] for x in cfg['stages']],original=True,notToScale=True),stages=[])
        steps=[build_step(cid,r,i,cfg['sources']) for i,r in enumerate(cfg['rows'])]
        wi,wz,we=WORKED[cid]
        steps[wi-1]['instruction']+=' '+wz
        steps[wi-1]['instructionEn']+=' '+we
        steps[wi-1]['check']+=' 同時交付算例的中間步驟或比較圖，並標示假設與模型限制。'
        steps[wi-1]['checkEn']+=' Also submit intermediate calculations or comparison diagrams with assumptions and model limits.'
        for n,stage in enumerate(cfg['stages']):
            z,e=split(stage)
            c['stages'].append(dict(id=f'{cid}-stage{n+1:02d}',order=n+1,title=z,titleEn=e,description=f'在「{z}」建立六項互補證據，逐一檢查材料、幾何、物理機制與適用限制。',descriptionEn=f'Build six complementary evidence items for {e.lower()}, checking materials, geometry, mechanisms and validity limits.',steps=steps[n*6:n*6+6]))
        result['courses'].append(c); result['places'].append(place_for(cid));result['related'].append(related_for(cid,cfg))
    result['sources']=list(SOURCES.values())
    # Protect script edits from silently changing course IDs or schema completeness.
    expected={f'a{n:03d}' for n in range(3,34)}-{'a004','a025'}
    assert {c['id'] for c in result['courses']}==expected
    ids={s['id'] for s in result['sources']};instructions=set();answers=[0,0,0]
    for c in result['courses']:
        assert c['title']==CAT[c['id']]['title'] and c['titleEn']==CAT[c['id']]['titleEn']
        assert len(c['stages'])==4 and len(c['sourceIds'])>=2
        seen=set()
        for st in c['stages']:
            assert len(st['steps'])==6
            for x in st['steps']:
                assert x['id'] not in seen and all(i in seen for i in x['prerequisiteIds']);seen.add(x['id'])
                assert set(x['sourceIds'])<=ids and len(x['knowledge'])==2
                assert x['instruction'] not in instructions;instructions.add(x['instruction'])
                for key in ('title','objective','instruction','observation','failure','check'):
                    assert x[key] and x[key+'En']
                assert len(x['quiz']['options'])==3 and len(set(x['quiz']['options']))==3
                assert len(x['quiz']['optionsEn'])==3 and 0<=x['quiz']['answer']<3
                answers[x['quiz']['answer']]+=1
        assert len(seen)==24
    assert answers==[232,232,232],answers
    assert len({split(v)[0] for arr in STAGE_KNOWLEDGE.values() for v in arr})==116
    for p in result['places']:
        assert len(p['history'])==2 and len(p['references'])>=2
        assert -90<=p['place']['lat']<=90 and -180<=p['place']['lng']<=180
    for r in result['related']:
        assert len(r['related'])==2
        for x in r['related']:assert len(x['practice'])==3 and len(x['practiceEn'])==3 and len(x['referenceUrls'])>=2
    out=Path(__file__).with_name('group_a.json');out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(dict(courses=len(result['courses']),steps=len(instructions),knowledge=2*len(instructions),sources=len(ids),places=len(result['places']),related=2*len(result['related']),quizAnswers=answers),ensure_ascii=False))

if __name__=='__main__':build()
