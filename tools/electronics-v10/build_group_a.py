"""Original V10 power engineering teaching cases. No energization procedures.
Reproduce with Python 3.10+: python3 tools/electronics-v10/build_group_a.py
Inputs are the immutable group_a_snapshot.json and authored records in this file.
"""
import copy,json,pathlib,math
P=pathlib.Path(__file__).resolve().parent
SNAP=json.loads((P/'group_a_snapshot.json').read_text())
CAT={x['id']:x for x in SNAP['catalog']}
OLD={x['id']:x for x in SNAP['existing']}
S={}
def source(k,zh,en,pub,url):
 S[k]={'id':'v10a-'+k,'title':zh,'titleEn':en,'publisher':pub,'url':url,'category':'electronics','sourceType':'primary','accessedAt':'2026-10-14','imageReuse':'僅連結；未複製原圖','imageReuseEn':'Link only; no source artwork reproduced.','scope':'官方領域背景與產品角色；本課模型及假想數字為獨立編寫，不是製造配方或產品保證。','scopeEn':'Official context and product role; models and hypothetical inputs are independently authored, not manufacturing recipes or product guarantees.'}
source('gen','汽輪機配套發電機','Turbine-coupled generators','Siemens Energy','https://www.siemens-energy.com/global/en/home/products-services/product/sgen-100a.html')
source('hydro','水力發電機','Hydropower generators','Voith','https://www.voith.com/corp-en/hydropower-components/generators.html')
source('hydrocontrol','水力自動化與勵磁','Hydropower automation and excitation','Voith','https://www.voith.com/corp-en/hydropower-components/automation.html')
source('transformer','變壓器產品與功能','Transformer products and functions','Hitachi Energy','https://www.hitachienergy.com/products-and-solutions/transformers')
source('dry','乾式配電變壓器','Dry-type distribution transformers','Hitachi Energy','https://www.hitachienergy.com/products-and-solutions/transformers/distribution-transformers/dry-type-transformers')
source('gis','高壓開關設備','High-voltage switchgear','Hitachi Energy','https://www.hitachienergy.com/in/en/products-and-solutions/high-voltage-switchgear-and-breakers')
source('vacuum','真空斷路器技術','Vacuum circuit-breaker technology','Siemens','https://www.siemens.com/en-us/products/vacuum-switching-technology/')
source('cable','高壓輸電電纜系統','High-voltage transmission cable systems','Nexans','https://www.nexans.com/electrification-solutions/markets/transmission/')
source('line','輸電容量與氣象','Transmission capacity and weather','U.S. Department of Energy','https://www.energy.gov/cmei/systems/articles/smart-transmission-tools-modernize-americas-power-grid')
source('get','強化既有輸電的技術','Grid-enhancing technologies','U.S. Department of Energy','https://www.energy.gov/oe/grid-enhancing-technologies-improve-existing-power-lines')
source('arrester','高壓避雷器','High-voltage surge arresters','Hitachi Energy','https://www.hitachienergy.com/ca/en/products-and-solutions/surge-arresters/high-voltage-surge-arresters')
source('hvdc','高壓直流輸電','High-voltage direct-current transmission','Hitachi Energy','https://www.hitachienergy.com/products-and-solutions/hvdc')
source('hvdcxf','換流變壓器','HVDC converter transformers','Hitachi Energy','https://www.hitachienergy.com/products-and-solutions/transformers/power-transformers/hvdc-converter-transformers')
source('facts','柔性交流輸電','Flexible AC transmission systems','Hitachi Energy','https://www.hitachienergy.com/products-and-solutions/facts')
source('svc','靜態虛功補償','Static var compensation','Hitachi Energy','https://www.hitachienergy.com/us/en/products-and-solutions/facts/static-var-compensation-svc')
source('forming','構網技術','Grid-forming technology','Hitachi Energy','https://www.hitachienergy.com/us/en/products-and-solutions/facts/statcom/grid-forming-technology')
source('cond','同步調相機與飛輪','Synchronous condensers and flywheels','Siemens Energy','https://www.siemens-energy.com/global/en/home/products-services/product/synchronous-condenser.html')
source('pmu','同步相量應用','Synchrophasor applications','Schweitzer Engineering Laboratories','https://selinc.com/solutions/synchrophasors/')
source('relay','線路差動與距離保護','Line differential and distance protection','Schweitzer Engineering Laboratories','https://selinc.com/products/411l/')
source('distance','距離保護與程序匯流排','Distance protection and process buses','Schweitzer Engineering Laboratories','https://selinc.com/products/421/')
source('flisr','故障隔離與供電復原','Fault isolation and service restoration','Schweitzer Engineering Laboratories','https://selinc.com/solutions/software/flisr/')
source('black','構網型黑啟動研究','Grid-forming black-start research','National Laboratory of the Rockies','https://www.nlr.gov/grid/black-start')
source('transition','微電網平順轉換研究','Seamless microgrid transition study','National Laboratory of the Rockies','https://research-hub.nlr.gov/en/publications/study-of-seamless-microgrid-transition-operation-using-grid-formi/')
source('psse','輸電動態模擬','Transmission dynamics simulation','Siemens','https://www.siemens.com/en-us/products/pss-software/psse/')
source('sincal','網路模型與分析','Network modeling and analysis','Siemens','https://www.siemens.com/en-gb/products/pss-software/pss-sincal/')
source('demand','需量反應與儲能研究','Demand response and storage integration','U.S. Department of Energy','https://www.energy.gov/cmei/demand-response-and-energy-storage-integration-study')
source('meter','三相電能計量參考設計','Three-phase energy metrology reference design','Texas Instruments','https://www.ti.com/tool/TIDA-010244')
source('meter1','單相電能計量參考設計','Single-phase energy metrology reference design','Texas Instruments','https://www.ti.com/tool/TIDA-010036')
source('harmonic','主動諧波濾波','Active harmonic filtering','Schneider Electric','https://www.se.com/us/en/download/document/5820CT2001/')
source('twin','電網數位分身實例','Grid digital-twin reference','Siemens','https://press.siemens.com/global/en/pressrelease/siemens-grid-protection-software-expertise-enable-unified-digital-model-aep-network')
source('pv','太陽電池模組製造背景','PV module manufacturing context','U.S. Department of Energy','https://www.energy.gov/cmei/systems/solar-photovoltaic-manufacturing-basics')
source('pvcell','太陽電池吸收與材料','Photovoltaic absorption and materials','U.S. Department of Energy','https://www.energy.gov/cmei/systems/solar-photovoltaic-cell-basics')
source('film','薄膜模組製造','Thin-film module manufacturing','First Solar','https://www.firstsolar.com/en/Technology/Manufacturing')
source('string','串列型逆變器設計資源','String-inverter design resources','Texas Instruments','https://www.ti.com/solution/string-inverter')
source('micro','微型逆變器參考設計','Microinverter reference design','Texas Instruments','https://www.ti.com/tool/TIDM-SOLARUINV')
source('inv','單相逆變器參考設計','Single-phase inverter reference design','Texas Instruments','https://www.ti.com/tool/TIDM-SOLAR-ONEPHINV')
source('tracker','工業太陽感測器','Industrial sun sensors','Solar MEMS','https://solar-mems.com/products/')
source('pvchain','太陽能供應鏈與追蹤架','PV supply chain and tracking structures','U.S. Department of Energy','https://www.energy.gov/cmei/systems/overview-trade-and-policy-measures-us-solar-manufacturing')
D={}
def add(n,focus,stages,src,example,units,related):
 rows=[]
 for row in units.strip().splitlines():
  f=[x.strip().split('~',1) for x in row.split('|')]
  assert len(f)==3 and all(len(x)==2 for x in f),(n,row)
  rows.append(f)
 assert len(rows)==12,(n,len(rows))
 D[f'a{n}']={'focus':focus.split('~'),'stages':[x.split('~') for x in stages.split('|')],'src':src.split(),'example':example.split('~'),'units':rows,'related':related}
add(201,'轉速、電磁負載與轉子熱機械限制~Speed, electromagnetic loading and rotor thermomechanical limits','額定與磁路~Rating and magnetics|轉子與定子~Rotor and stator|冷卻與控制~Cooling and control|驗證與交接~Validation and handoff','gen hydro',
'教學假設二極同步機接 60 Hz：n=120f/p=3600 rpm；若輸出 100 MW、效率 98%，輸入 102.041 MW、損失 2.041 MW。效率為假設且未含汽輪機熱效率。~Assume a two-pole synchronous machine at 60 Hz: n=120f/p=3600 rpm. At 100 MW output and assumed 98% efficiency, input is 102.041 MW and loss 2.041 MW; turbine thermal efficiency is excluded.', '''
極數與轉速~Poles and speed|同步轉速由頻率與極數共同決定。~Frequency and pole count jointly determine synchronous speed.|比較二極與四極的轉速表。~Compare two- and four-pole speed tables.
磁通與端電壓~Flux and voltage|感應電壓隨頻率、匝數與每極磁通變化。~Induced voltage depends on frequency, turns and pole flux.|固定頻率檢查匝數變更的比例。~Check turn-ratio scaling at fixed frequency.
額定能力曲線~Capability envelope|定子電流、勵磁與端部加熱限制不同區域。~Stator current, excitation and end heating bound different regions.|在 P–Q 圖分別標示限制來源。~Label each constraint on a P–Q diagram.
轉子圓周應力~Rotor hoop stress|轉速提高使離心應力約隨轉速平方增加。~Centrifugal stress scales approximately with squared speed.|比較相同幾何的 1.0 與 1.1 倍轉速。~Compare equal geometry at 1.0 and 1.1 speed.
定子疊片~Stator laminations|疊片絕緣抑制穿越片間的渦電流路徑。~Interlaminar insulation interrupts cross-sheet eddy-current paths.|以局部熱點和鐵耗定位短片。~Correlate hot spots and core loss.
端繞組支撐~End-winding supports|故障電流造成瞬時電磁力與支撐振動。~Fault currents create transient forces and support vibration.|比對模態頻率及力的頻譜。~Compare modal frequencies with force spectra.
槽絕緣與局放~Slot insulation and PD|空隙電場可引起局放而非立即擊穿。~Void fields can cause partial discharge before breakdown.|比較相位分布與環境雜訊。~Compare phase patterns against ambient noise.
冷卻熱路~Cooling paths|銅耗與鐵耗經不同熱阻流向冷卻介質。~Copper and core losses follow different cooling resistances.|以熱平衡區分入口溫度與熱點。~Separate inlet temperature from hot spots by heat balance.
軸系臨界轉速~Shaft critical speeds|軸承剛性影響軸系固有頻率和振型。~Bearing stiffness changes shaft natural frequencies and modes.|比較升降速模擬的振幅相位。~Compare amplitude and phase during simulated run-up/down.
勵磁動態~Excitation dynamics|勵磁改變內部電勢但不直接供應軸功率。~Excitation changes internal EMF, not shaft power directly.|分別施加電壓與機械功率模型擾動。~Apply separate voltage and mechanical-power model disturbances.
損失分離~Loss segregation|單一效率數字不能定位銅耗與通風損失。~One efficiency value cannot separate copper and ventilation losses.|以負載平方與轉速趨勢擬合損失。~Fit losses against squared load and speed.
出廠證據鏈~Factory evidence|絕緣、振動和熱報告需對應同一序號版本。~Insulation, vibration and thermal reports need matching asset revisions.|建立量測不確定度及報告索引。~Build an uncertainty and report index.
''',[(202,'同步感應與絕緣共同~Shared synchronous induction and insulation','水輪機通常低速多極，軸向推力不同~Hydro machines are often slower and multipolar with different thrust'),(215,'同一同步機可供無功~A synchronous machine can supply reactive power','調相機沒有持續機械發電輸入~A condenser has no sustained mechanical generation input')])
add(202,'多極磁路、氣隙偏心與垂直軸承~Multipolar magnetics, air-gap eccentricity and vertical bearings','水力與額定~Hydraulics and rating|磁路與機構~Magnetics and mechanics|控制與熱路~Controls and heat paths|狀態與驗收~Condition and acceptance','hydro hydrocontrol',
'假設 60 Hz、40 極，n=180 rpm；水頭 50 m、流量 100 m³/s、整體效率 0.90，P=ρgQHη≈44.145 MW（ρ=1000 kg/m³，g=9.81 m/s²）。未含水頭隨流量變動。~For 60 Hz and 40 poles, n=180 rpm. With head 50 m, flow 100 m³/s and overall efficiency 0.90, P=ρgQHη≈44.145 MW using ρ=1000 kg/m³ and g=9.81 m/s²; flow-dependent head is omitted.', '''
水頭與功率~Head and power|水力輸入由有效水頭及流量共同決定。~Effective head and flow jointly determine hydraulic input.|區分淨水頭與地形高差。~Distinguish net head from elevation difference.
極數選擇~Pole selection|低轉速需較多磁極以維持電網頻率。~Low speed requires more poles for grid frequency.|由額定轉速反算整數極數。~Infer an integer pole count from rated speed.
功率因數~Power factor|相同 MW 在較低功率因數需要較大 MVA。~Equal MW needs more MVA at lower power factor.|用 S²=P²+Q² 核對容量。~Check rating with S²=P²+Q².
凸極磁路~Salient-pole magnetics|直軸與交軸磁阻不同使電抗不相等。~Unequal axis reluctances produce unequal reactances.|比較 d、q 軸擾動模型。~Compare d- and q-axis perturbation models.
氣隙偏心~Air-gap eccentricity|非均勻氣隙造成不平衡磁拉力。~Nonuniform gaps create unbalanced magnetic pull.|配對圓周氣隙圖和振動方向。~Pair circumferential gap maps with vibration direction.
推力軸承~Thrust bearing|軸承承受轉動件重量與水力推力。~The bearing carries rotor weight and hydraulic thrust.|分開靜重與運轉推力邊界。~Separate dead weight from operating thrust.
定子接頭~Stator joints|接頭接觸電阻造成集中熱源。~Joint contact resistance creates concentrated heating.|比較四端電阻和局部熱像。~Compare four-terminal resistance with thermal maps.
冷卻迴路~Cooling circuit|流量不足與污垢增加不同熱阻。~Low flow and fouling change different thermal resistances.|同時核對流量、溫差與壓差。~Check flow, temperature rise and pressure drop together.
調速器耦合~Governor coupling|水路慣性使閘門與電功率不同步。~Water inertia delays power after gate changes.|比較閘門、流量和轉速時間序列。~Compare gate, flow and speed time series.
勵磁與無功~Excitation and vars|無功控制受勵磁與定子熱限制。~Var control is bounded by excitation and stator heating.|畫欠勵與過勵限制曲線。~Plot under- and over-excitation limits.
甩負載模型~Load rejection model|電負載驟減會暫時留下正加速功率。~Electrical load rejection briefly leaves positive accelerating power.|檢查機械與電功率差的積分。~Inspect the integral of mechanical/electrical power imbalance.
狀態交接~Condition handoff|振動基準須記錄水頭與負載條件。~Vibration baselines require head and load conditions.|以相同工況比較趨勢而非單點。~Compare matched operating conditions, not isolated values.
''',[(201,'同為同步電機與三相熱設計~Both use synchronous machines and three-phase thermal design','汽輪發電機的高速圓筒轉子不同~Steam generators use different high-speed cylindrical rotors'),(215,'勵磁及無功能力可互相比較~Excitation and reactive capability are comparable','水輪機持續提供軸功率而調相機主要吸收損失~Hydro supplies shaft power while a condenser mainly absorbs losses')])
add(203,'頻率響應、含水絕緣與短路力的進階診斷~Advanced diagnosis of frequency response, moist insulation and short-circuit forces','電磁模型延伸~Extended magnetic model|絕緣與熱壽命~Insulation and thermal life|機械與頻率證據~Mechanical and frequency evidence|聯合驗收~Joint acceptance','transformer hvdcxf',
'假設 100 MVA、線電壓 230 kV，額定線電流 I=S/(√3V)=251.0 A；若等效阻抗 0.10 pu 且忽略上游阻抗，三相短路電流約 10 pu。僅為模型，不是保護整定。~Assume 100 MVA at line voltage 230 kV: rated line current I=S/(√3V)=251.0 A. An equivalent 0.10 pu impedance gives about 10 pu three-phase fault current when upstream impedance is omitted; this is not a protection setting.', '''
標么基準~Per-unit bases|阻抗百分比需使用一致容量及電壓基準。~Impedance percentages require consistent power and voltage bases.|以實際歐姆值交叉換算。~Cross-check by converting through ohms.
磁通積分~Flux integration|磁通由電壓時間積分決定而非瞬時電壓。~Flux follows voltage-time integral, not instantaneous voltage.|比較同峰值不同波形的積分。~Compare integrals of equal-peak waveforms.
剩磁與湧流~Remanence and inrush|初始剩磁改變暫態飽和程度。~Initial remanence changes transient saturation.|掃描模型初始磁通與合閘相位。~Sweep initial model flux and closing phase.
紙油含水~Paper-oil moisture|紙與油之間的水分分配隨溫度改變。~Moisture partition between paper and oil changes with temperature.|同溫度比較含水與介電資料。~Compare moisture and dielectric data at matched temperatures.
熱點與平均~Hot spot versus mean|平均繞組溫度不能代替局部熱點。~Mean winding temperature cannot replace local hot spots.|比較熱模型節點與感測位置。~Compare thermal nodes with sensor locations.
老化加速~Aging acceleration|熱老化對溫度呈非線性敏感。~Thermal aging is nonlinear in temperature.|以相同平均溫度比較不同波動。~Compare different fluctuations at equal mean temperature.
軸向短路力~Axial fault force|漏磁與電流耦合產生軸向壓縮或拉力。~Leakage flux and current generate axial compression or tension.|標示端部磁通與支撐反力。~Map end flux and support reactions.
徑向屈曲~Radial buckling|內繞組受壓的穩定性取決於支撐與缺陷。~Inner-winding buckling depends on support and imperfections.|比較完美圓環與偏心模型。~Compare ideal-ring and eccentric models.
掃頻響應~Frequency response|FRA 變化可能來自幾何、引線或接地差異。~FRA changes can reflect geometry, leads or grounding.|固定接線後比較重複性與基準。~Fix connections before comparing repeatability and baseline.
氣體趨勢~Gas trends|溶解氣體需結合生成速率與設備歷史。~Dissolved gases require rates and asset history.|把取樣間隔及補油事件列入。~Include sampling intervals and oil-addition events.
分接切換~Tap transitions|分接位置改變變比亦改變局部接觸條件。~Tap position changes both ratio and contact conditions.|按位置比較電阻與變比一致性。~Compare resistance and ratio across positions.
交叉診斷~Cross-diagnosis|單項異常不足以唯一確定失效機制。~One abnormal metric cannot uniquely identify a failure.|用熱、電、機械證據建立假說表。~Build hypotheses from thermal, electrical and mechanical evidence.
''',[(204,'磁路及熱阻預算相通~Magnetic and thermal budgets transfer','乾式沒有油紙分配與溶解氣體模型~Dry types lack oil-paper partition and dissolved-gas models'),(211,'換流站需要變壓器絕緣及漏抗模型~Converter stations need transformer insulation and leakage models','換流諧波與直流偏壓需另加邊界~Converter harmonics and DC bias require extra boundaries')])
add(204,'樹脂絕緣、通風與非線性負載降額~Resin insulation, ventilation and nonlinear-load derating','磁路與負載~Magnetics and load|固體絕緣~Solid insulation|散熱與結構~Heat and structure|性能驗證~Performance verification','dry transformer',
'假設損失 2 kW、等效熱阻 0.025 K/W，穩態平均溫升 50 K。熱阻增加 20% 時為 60 K；集中參數模型不預測樹脂內局部熱點。~Assume loss 2 kW and equivalent thermal resistance 0.025 K/W: steady mean rise is 50 K. A 20% resistance increase gives 60 K; this lumped model does not predict local resin hot spots.', '''
磁路截面~Core section|降低頻率但維持電壓會提高峰值磁通。~Lower frequency at fixed voltage increases peak flux.|比較 V/f 相同與不同兩種情境。~Compare equal and unequal V/f cases.
繞組電流~Winding current|繞組導體損失以電流平方加權。~Conductor loss scales with squared current.|按負載時間積分 I²R。~Integrate I²R over the load profile.
非線性負載~Nonlinear load|諧波使渦流及集膚損失增大。~Harmonics increase eddy-current and skin-effect losses.|比較同 RMS 不同頻譜的模型。~Compare equal-RMS models with different spectra.
樹脂收縮~Resin shrinkage|固化與熱膨脹差會產生殘應力。~Cure shrinkage and expansion mismatch create residual stress.|畫金屬與樹脂的自由應變差。~Plot free-strain mismatch of metal and resin.
空隙電場~Void fields|串聯介質中低介電常數區承受較高場。~Low-permittivity regions carry higher fields in series dielectrics.|用位移連續條件比較場強。~Compare fields using displacement continuity.
表面爬電~Surface creepage|潮濕污染改變表面漏電路徑。~Moist contamination alters surface leakage paths.|分開表面與體積絕緣證據。~Separate surface from bulk-insulation evidence.
自然對流~Natural convection|通風道幾何影響浮力流與熱阻。~Duct geometry affects buoyancy flow and thermal resistance.|比較堵塞與通暢的熱網路。~Compare obstructed and open thermal networks.
強制風冷~Forced air|風扇額定風量不等於實際通道流量。~Rated fan flow is not actual duct flow.|疊合風扇與系統壓降曲線。~Overlay fan and system-pressure curves.
聲振來源~Noise and vibration|磁致伸縮與結構共振共同決定聲音。~Magnetostriction and structural resonance jointly shape noise.|比較頻譜與固定條件。~Compare spectra and mounting conditions.
局放報告~PD report|局放讀值受量測帶寬與背景噪聲影響。~PD readings depend on bandwidth and background noise.|核對校正脈波及噪聲底。~Check calibration pulses and noise floor.
溫升試驗判讀~Thermal-test interpretation|環境溫度變化會污染溫升比較。~Ambient changes confound temperature-rise comparisons.|使用同步環境與繞組時間軸。~Use synchronized ambient and winding traces.
降額交接~Derating handoff|海拔、箱體及負載頻譜需聯合評估。~Altitude, enclosure and load spectrum require joint assessment.|列工況矩陣與未驗證區域。~List operating cases and unverified regions.
''',[(203,'匝比、漏抗與热預算相通~Turns ratio, leakage and thermal budgets transfer','固體絕緣散熱路徑不同於液體循環~Solid insulation cools differently from liquid circulation'),(229,'非線性電流決定額外損失~Nonlinear current determines extra loss','濾波器降低部分諧波但不能替代熱驗證~Filtering cannot replace thermal verification')])
add(205,'同軸電場、隔室密封與開關暫態~Coaxial fields, compartment sealing and switching transients','電場與配置~Fields and layout|氣體與隔室~Gas and compartments|開關與量測~Switching and sensing|驗收與維護~Acceptance and maintenance','gis arrester',
'理想同軸導體半徑 a=20 mm、外殼內半徑 b=80 mm，瞬時電壓 V=100 kV，導體表面 E=V/[a ln(b/a)]≈3.61 MV/m；忽略端部與顆粒，不是絕緣耐壓。~For ideal coaxial radii a=20 mm and b=80 mm at instantaneous V=100 kV, conductor-surface E=V/[a ln(b/a)]≈3.61 MV/m. End effects and particles are omitted; this is not a withstand rating.', '''
同軸電場~Coaxial field|場強在內導體表面最大而非均勻。~Field peaks at the inner conductor, not uniformly.|比較解析徑向曲線與網格結果。~Compare analytic radial fields with mesh results.
三相配置~Phase layout|共箱與分箱具有不同耦合電容。~Common and separate enclosures have different coupling capacitances.|建立導體間電容矩陣。~Build an interconductor capacitance matrix.
支撑絕緣子~Support insulators|三接點附近介電常數突變使場集中。~Permittivity discontinuities concentrate fields near triple junctions.|加密局部網格並檢查收斂。~Refine local meshes and check convergence.
氣體密度~Gas density|壓力讀值需溫度補償才可比較密度。~Pressure needs temperature compensation to compare density.|固定氣體組成與理想氣體近似下，用絕對壓力 p 及 Kelvin 溫度 T 比較 p/T；不可用表壓或攝氏溫度。~At fixed composition under the ideal-gas approximation, compare p/T using absolute pressure and kelvin, never gauge pressure or Celsius.
材料相容性~Material compatibility|替代氣體需重新核對密封與介電系統。~Alternative gases require sealing and dielectric requalification.|列材料、氣體與溫度矩陣。~List material, gas and temperature combinations.
隔室邊界~Compartment boundaries|分隔能限制洩漏影響但增加界面。~Compartments limit leak consequences but add interfaces.|畫隔室圖與偵測覆蓋。~Map compartments and detection coverage.
顆粒敏感性~Particle sensitivity|金屬顆粒可局部放大場強。~Metallic particles can amplify local fields.|比較位置與方向的場增強。~Compare field enhancement by position and orientation.
快速暫態~Fast transients|快速開關波需考慮傳播與反射。~Fast switching waves require propagation and reflection models.|比較集總與分布參數模型。~Compare lumped and distributed models.
接地回流~Ground return|外殼連接阻抗影響暫態電位分布。~Enclosure bond impedance affects transient potentials.|標示高頻回流路徑及迴路面積。~Mark high-frequency return paths and loop areas.
局放定位~PD localization|到達時間差須扣除傳播速度與感測延遲。~Arrival differences include propagation speed and sensor delay.|用已知位置模擬訊號校核。~Validate using simulated known-source positions.
連鎖狀態~Interlock states|安全狀態由完整設備位置組合決定。~Safe states depend on complete device-position combinations.|用離線狀態表找不允許轉移。~Find forbidden transitions in an offline state table.
驗收證據~Acceptance evidence|氣密、介電與機械報告互不替代。~Leak, dielectric and mechanical reports are not interchangeable.|逐隔室建立報告與版本關聯。~Link reports and revisions per compartment.
''',[(206,'都需分斷與絕緣恢復證據~Both need interruption and dielectric-recovery evidence','GIS 是系統隔室，真空斷路器聚焦滅弧室~GIS covers compartments; vacuum breakers focus on interrupters'),(210,'均需過電壓保護協調~Both need overvoltage coordination','避雷器限制波峰而 GIS 定義承受系統~Arresters limit surges while GIS defines the withstand system')])
add(206,'真空滅弧、接點運動與恢復電壓~Vacuum interruption, contact motion and recovery voltage','額定與電弧~Rating and arc|機構與密封~Mechanism and seal|電路與協調~Circuit coordination|壽命證據~Lifetime evidence','vacuum gis',
'假設接點平均速度 1 m/s，10 mm 行程需 10 ms；50 Hz 的半週期也為 10 ms，但相等不代表可可靠分斷，還需電流零點與暫態恢復電壓分析。~At assumed mean contact speed 1 m/s, 10 mm travel takes 10 ms, equal to a 50 Hz half-cycle. Equality does not prove interruption: current zero and transient recovery voltage still matter.', '''
額定量分離~Separate ratings|連續電流、短時耐受與分斷電流是不同額定。~Continuous, short-time withstand and interrupting currents differ.|將負載與故障情境分別對應額定。~Map load and fault cases to separate ratings.
真空電弧~Vacuum arc|電弧由接點金屬蒸氣供應載流粒子。~Contact metal vapor supplies charge carriers to the arc.|區分真空背景與弧柱粒子來源。~Separate vacuum background from arc-particle sources.
電流零點~Current zero|自然電流零點後需迅速恢復介電強度。~Dielectric strength must recover after natural current zero.|疊合恢復強度及外加電壓曲線。~Overlay recovered strength and applied-voltage curves.
接點材料~Contact materials|材料同時影響侵蝕、熔焊與截流特性。~Materials affect erosion, welding and current chopping.|用多目標表比較而非只比導電率。~Use multiple criteria rather than conductivity alone.
磁場控弧~Magnetic arc control|接點幾何改變磁場及電弧分布。~Contact geometry alters magnetic fields and arc distribution.|比較軸向與徑向控弧示意。~Compare axial and radial arc-control diagrams.
波紋管~Bellows|波紋管需同時維持真空與機械疲勞能力。~Bellows must maintain vacuum and fatigue capability.|配對洩漏趨勢與操作循環數。~Pair leak trends with operation cycles.
接點行程~Contact travel|相同終點不代表相同速度與彈跳。~Equal final travel does not imply equal speed or bounce.|比較完整位移時間曲線。~Compare complete displacement-time traces.
三極同步~Pole synchronism|極間時間差改變不平衡與故障清除。~Pole timing differences affect unbalance and fault clearing.|以共同時間基準比較三極曲線。~Compare three poles on a common clock.
截流過電壓~Chopping overvoltage|電感儲能可轉為寄生電容電壓。~Inductor energy can transfer to parasitic capacitance voltage.|用能量守恆估計暫態上界。~Estimate a transient bound from energy conservation.
恢復電壓~Recovery voltage|TRV 峰值與上升率共同影響分斷難度。~TRV peak and rate jointly affect interruption difficulty.|比較同峰值不同斜率案例。~Compare equal peaks with different slopes.
侵蝕與阻值~Erosion and resistance|接點磨耗與接觸壓力共同影響電阻。~Wear and contact pressure jointly affect resistance.|同溫度比較行程與四端電阻。~Compare travel and four-terminal resistance at matched temperature.
機構驗收~Mechanism acceptance|輔助接點時間不能直接代表主接點位置。~Auxiliary timing does not directly establish main-contact position.|對照位置回授與主回路離線報告。~Cross-check position feedback and offline main-circuit reports.
''',[(205,'開關功能與介電協調相連~Switching and dielectric coordination connect','真空為滅弧介質而 GIS 氣體主要提供外部絕緣~Vacuum interrupts; GIS gas mainly provides external insulation'),(210,'截流暫態需要保護協調~Chopping transients need protective coordination','避雷器吸能額定不能當成斷路器分斷額定~Arrester energy rating is not breaker interrupting rating')])
add(207,'徑向電場、熱阻與接頭界面控制~Radial fields, thermal resistance and joint interfaces','電纜模型~Cable model|接頭界面~Joint interfaces|熱與護套~Heat and sheaths|證據與放行~Evidence and release','cable arrester',
'理想同軸 a=10 mm、b=30 mm、瞬時 V=50 kV，E(a)=V/[a ln(b/a)]≈4.55 MV/m。若單位長度熱損失 20 W/m、等效熱阻 2 K·m/W，溫升 40 K；兩式皆忽略界面缺陷。~For ideal coaxial a=10 mm, b=30 mm and instantaneous V=50 kV, E(a)≈4.55 MV/m. With linear heat loss 20 W/m and thermal resistance 2 K·m/W, rise is 40 K; interface defects are omitted.', '''
導體電阻~Conductor resistance|導體溫度與集膚效應改變交流電阻。~Temperature and skin effect alter AC resistance.|比較直流與頻率相關電阻模型。~Compare DC and frequency-dependent resistance.
絕緣徑向場~Radial insulation field|同軸場隨半徑反比下降。~Coaxial field decreases inversely with radius.|核對內外界面電場及電位積分。~Check interface fields and potential integral.
半導電屏蔽~Semiconductive screens|平滑屏蔽界面減少幾何場集中。~Smooth screen interfaces reduce geometric field concentration.|比較粗糙度與局部場模型。~Compare roughness and local-field models.
屏蔽截斷~Screen cutback|屏蔽結束處需要重新分配軸向電場。~Screen termination requires axial field redistribution.|對照應力控制前後等位線。~Compare equipotentials with and without stress control.
界面壓力~Interface pressure|接觸壓力影響微空隙及熱接觸。~Contact pressure affects microvoids and thermal contact.|將壓縮鬆弛與局放跡象配對。~Pair compression relaxation with PD indications.
材料膨脹~Material expansion|熱循環使不同材料產生相對位移。~Thermal cycling creates differential material displacement.|計算自由應變差並畫約束。~Calculate free-strain mismatch and constraints.
護套電流~Sheath currents|護套接地配置改變循環電流與損耗。~Sheath bonding changes circulating current and loss.|比較單點與交叉接地的等效圖。~Compare single-point and cross-bonded models.
敷設熱阻~Installation thermal resistance|土壤乾燥與鄰近熱源可降低散熱能力。~Soil drying and nearby heat reduce cooling capacity.|對土壤熱阻做敏感度分析。~Sweep soil thermal resistance.
彎曲界面~Bending interfaces|彎曲會使絕緣及屏蔽產生不均勻應變。~Bending creates unequal strain in insulation and screens.|比較中性軸兩侧應變。~Compare strains around the neutral axis.
局放定位~PD localization|反射與衰減可能使脈波位置判讀偏差。~Reflection and attenuation can bias pulse localization.|用已知長度模型校驗到達時間。~Validate arrivals with a known-length model.
介質損耗~Dielectric loss|損耗角資料需頻率與溫度條件。~Loss-angle data require frequency and temperature context.|比較頻譜而非單點百分比。~Compare spectra rather than one percentage.
接頭追溯~Joint traceability|材料批次與幾何檢查需連到同一接頭。~Material lots and geometric checks must identify one joint.|建立離線接頭護照和量測索引。~Build an offline joint passport and measurement index.
''',[(208,'共用絕緣與接頭熱電模型~Insulation and joint thermal/electrical models transfer','海纜增加水深、張力與海床條件~Subsea adds depth, tension and seabed conditions'),(210,'電纜端點需要絕緣協調~Cable endpoints need insulation coordination','電纜分布參數不能縮成單一耐壓值~Distributed cable behavior is not one withstand value')])
add(208,'海床路由、機械張力與海纜熱可靠度~Seabed routing, mechanical tension and cable thermal reliability','需求與路由~Needs and routing|電熱選型~Electrothermal selection|施工模型~Installation models|監測與復原~Monitoring and recovery','cable hvdc',
'假設導體回路總電阻 4 Ω，直流 1000 A 時損失 I²R=4 MW。若傳送 500 MW，線路電阻損失為 0.8%；未含換流、護套或介電損失。~For an assumed total DC conductor-loop resistance 4 Ω at 1000 A, I²R=4 MW, or 0.8% of 500 MW transmitted. Conversion, sheath and dielectric losses are excluded.', '''
交流與直流~AC versus DC|長交流海纜的充電電流佔用載流容量。~Long AC cable charging consumes current capacity.|比較 I=ωCV 與負載電流。~Compare I=ωCV with load current.
路由調查~Route survey|地形與人類活動形成不同失效風險。~Seabed terrain and human activity create different risks.|疊合地質、航道及禁入區圖層。~Overlay geology, shipping and exclusion layers.
跨越界面~Crossings|跨越既有管線需處理支撐及熱瓶頸。~Existing-line crossings introduce support and thermal bottlenecks.|建立局部跨距及熱阻模型。~Build local span and thermal-resistance models.
埋深與溫升~Burial and heating|更深埋設可能增加熱阻與保護程度。~Deeper burial can increase both protection and thermal resistance.|比較埋深對溫升與外力暴露。~Compare depth effects on heating and exposure.
護鎧損失~Armor losses|磁性護鎧在交流磁場下可能產生額外損耗。~Magnetic armor can add losses in AC fields.|分開導體、護套和護鎧熱源。~Separate conductor, sheath and armor heat sources.
水壓與密封~Pressure and sealing|水壓隨深度增加而接頭需維持密封。~Hydrostatic pressure rises with depth while joints must seal.|用 p=ρgh 比較設計水深。~Compare depths using p=ρgh.
懸鏈線張力~Catenary tension|船端到觸底點的幾何決定張力分布。~Vessel-to-touchdown geometry determines tension distribution.|比較水深、船位與彎曲曲率。~Compare depth, vessel position and curvature.
最小彎曲~Minimum curvature|張力與彎曲共同作用於多層結構。~Tension and bending jointly load multilayer structures.|列組合載荷而非只看彎曲半徑。~List combined loads, not bend radius alone.
接續與備品~Joints and spares|修復接頭相容性決定備品策略。~Repair-joint compatibility shapes spares strategy.|核對電壓、導體與絕緣組合。~Check voltage, conductor and insulation combinations.
溫度感測~Temperature sensing|分布式感測讀到的是光纖所在位置溫度。~Distributed sensing measures temperature at the fiber location.|用徑向熱模型估計導體溫度差。~Use radial models to estimate conductor/fiber differences.
故障定位~Fault location|傳播速度不確定度會放大距離誤差。~Propagation-speed uncertainty amplifies distance error.|計算位置對時間及速度的敏感度。~Calculate position sensitivity to time and speed.
修復可用率~Repair availability|天候、船期及備品使停機時間非固定。~Weather, vessels and spares make downtime variable.|比較樂觀、中位與保守停機情境。~Compare optimistic, median and conservative downtime cases.
''',[(207,'電纜本體與接頭模型相通~Cable-body and joint models transfer','海床熱土與海事載荷需另行取證~Seabed thermal and marine loads need separate evidence'),(211,'長距離海纜常與換流站配套~Long subsea links often pair with converters','換流控制與海纜修復有不同時間尺度~Converter control and repair act on different timescales')])
add(209,'弧垂、風冰載荷與動態熱額定~Sag, wind/ice loads and dynamic thermal ratings','導線與跨距~Conductor and span|風冰與結構~Wind, ice and structure|熱額定~Thermal rating|監測與風險~Monitoring and risk','line get',
'小弧垂拋物線假設：均布重量 w=15 N/m、跨距 L=300 m、水平張力 H=30 kN，弧垂 f=wL²/(8H)=5.625 m。風、覆冰及高差未納入，不能用於現場淨空放行。~Under a small-sag parabolic model with w=15 N/m, L=300 m and horizontal tension H=30 kN, f=wL²/(8H)=5.625 m. Wind, ice and elevation difference are omitted; this cannot authorize clearance.', '''
導線複合~Composite conductor|鋼芯與導體層共同承擔拉力和熱伸長。~Core and conductor layers share tension and thermal expansion.|比較各材料面積與應變相容。~Compare areas and strain compatibility.
跨距幾何~Span geometry|支點高差使最低點偏離跨距中央。~Unequal support heights shift the low point off-center.|比較等高與不等高懸鏈線。~Compare equal- and unequal-height catenaries.
張力弧垂~Tension and sag|張力提高降低弧垂但增加結構負載。~Greater tension reduces sag but increases structural loading.|用張力掃描繪製兩種限制。~Sweep tension to plot both constraints.
風載分量~Wind components|橫風使導線位移與支架受力方向改變。~Crosswind changes conductor displacement and support forces.|以向量合成重力與風載。~Combine gravity and wind vectors.
覆冰重量~Ice loading|冰層增加重量亦改變迎風直徑。~Ice increases weight and exposed diameter.|同時計算重量及投影面積變化。~Calculate weight and projected-area changes together.
舞動與渦振~Galloping and vortex vibration|低頻舞動與高頻渦振是不同機制。~Low-frequency galloping differs from vortex-driven vibration.|比較頻率、振幅與氣象條件。~Compare frequency, amplitude and weather conditions.
電流熱平衡~Current heat balance|焦耳熱與日照需由對流輻射帶走。~Joule and solar heat require convection and radiation removal.|檢查輸入與輸出熱量殘差。~Check the heat-balance residual.
風向敏感度~Wind-direction sensitivity|同風速但不同夾角可有不同冷卻。~Equal wind speed can cool differently at different angles.|固定風速掃描相對風向。~Sweep relative angle at fixed wind speed.
蠕變與長期~Creep and time|長期蠕變改變永久伸長和淨空。~Creep changes permanent elongation and clearance.|區分可逆熱伸長與殘留伸長。~Separate reversible thermal and residual elongation.
感測代表性~Sensor representativeness|一處氣象站不能保證全線最差條件。~One weather station may miss the limiting span.|比較沿線風場及缺測情境。~Compare along-line wind and missing-data cases.
動態額定~Dynamic rating|即時熱容量估計仍受淨空及設備限制。~Dynamic thermal ratings remain bounded by clearance and equipment.|取多項限制的最小值。~Take the minimum of independent limits.
告警回退~Alarm fallback|感測失效時需回到已驗證保守容量。~Sensor failure needs a validated conservative fallback.|在離線回放中移除關鍵資料。~Remove key data in offline replay.
''',[(210,'雷擊與氣象共同影響線路~Lightning and weather jointly affect lines','熱額定不能取代雷電絕緣協調~Thermal ratings cannot replace lightning coordination'),(230,'動態資料需與拓撲模型相連~Dynamic data must connect to topology','數位模型需保留天候缺測不確定度~Digital models must retain missing-weather uncertainty')])
add(210,'避雷器能量、保護距離與絕緣裕度~Arrester energy, protective distance and insulation margins','波與絕緣~Waves and insulation|非線性元件~Nonlinear devices|配置與能量~Layout and energy|驗證與狀態~Verification and condition','arrester gis',
'教學矩形脈波假設電流 5 kA、避雷器電壓 100 kV、持續 20 μs，能量 W=∫vi dt=10 kJ。真實波形須積分且多次衝擊需熱恢復模型，不能由此挑選額定。~For an illustrative rectangular 5 kA pulse at 100 kV lasting 20 μs, W=∫vi dt=10 kJ. Real waveforms need integration and repeated surges need thermal recovery; this does not select a rating.', '''
過電壓種類~Overvoltage types|雷擊、開關與暫時過電壓有不同時間尺度。~Lightning, switching and temporary overvoltages differ in duration.|依持續時間分類測試波形。~Classify waveforms by duration.
進行波阻抗~Traveling-wave impedance|波阻抗及端點反射決定端電壓。~Surge impedance and terminal reflection shape voltage.|用反射係數比較開路與匹配。~Compare open and matched reflection coefficients.
耐受統計~Withstand statistics|耐壓具有波形、極性與統計依存。~Withstand depends on waveform, polarity and statistics.|核對試驗條件及樣本範圍。~Check test conditions and sample range.
氧化鋅非線性~Zinc-oxide nonlinearity|強非線性伏安使大電流時電壓受限。~Strong nonlinear I–V behavior limits surge voltage.|比較線性電阻與非線性曲線。~Compare linear and nonlinear I–V curves.
持續運轉電壓~Continuous voltage|正常電壓需低於適用連續承受條件。~Normal voltage must fit the applicable continuous-duty envelope.|區分 RMS 系統量及衝擊峰值。~Separate RMS system values from impulse peaks.
暫時過壓~Temporary overvoltage|較長過壓可能在小電流下累積大量熱。~Long overvoltages can accumulate heat at modest current.|比較等峰值不同持續時間能量。~Compare equal peaks with different durations.
引線電感~Lead inductance|引線產生 L di/dt 額外電壓。~Leads add L di/dt voltage.|將引線電壓加到殘壓預算。~Add lead voltage to the residual-voltage budget.
保護距離~Protection distance|設備與避雷器距離使傳播延遲不可忽略。~Arrester-to-equipment distance creates propagation delay.|比較共點與有距離模型。~Compare colocated and separated models.
能量與電荷~Energy and charge|吸收能量與轉移電荷是不同壓力量。~Absorbed energy and transferred charge are distinct stresses.|分別計算 ∫vi dt 與 ∫i dt。~Calculate ∫vi dt and ∫i dt separately.
熱穩定~Thermal stability|發熱大於散熱會導致熱失控。~Heat generation above dissipation can cause thermal runaway.|找發熱與散熱曲線交點穩定性。~Assess stability of heating/cooling intersections.
洩漏電流~Leakage current|容性與阻性電流需分離才能判讀劣化。~Capacitive and resistive leakage need separation for diagnosis.|比較相位及溫度補償趨勢。~Compare phase and temperature-corrected trends.
協調文件~Coordination record|保護裕度需記錄設備波形與配置版本。~Protection margin needs waveform and layout revisions.|逐設備建立裕度及未決假設表。~Record margins and unresolved assumptions per asset.
''',[(205,'介電承受與保護電壓需匹配~Withstand and protection levels must match','GIS 的快速暫態有額外傳播效應~GIS fast transients add propagation effects'),(207,'電纜端接需限制過電壓~Cable terminations need surge limitation','電纜反射與護套回路改變端點波形~Cable reflections and sheath loops change terminal waves')])
add(211,'換流站多時間尺度、能量失衡與保護協調~Converter-station timescales, energy imbalance and protection coordination','系統等值深化~System equivalents|閥與直流能量~Valves and DC energy|多迴路控制~Multiple control loops|事件與恢復~Events and recovery','hvdc hvdcxf forming',
'假設直流等效 C=100 μF，電壓由 300 kV 升到 330 kV，儲能增加 ΔE=C(V₂²−V₁²)/2=945 kJ。若暫時多餘功率 100 MW，理想需 9.45 ms；忽略控制與損失，不能當保護延時。~For assumed DC equivalent C=100 μF rising from 300 to 330 kV, ΔE=C(V₂²−V₁²)/2=945 kJ. At 100 MW surplus, ideal time is 9.45 ms; controls and losses are omitted, so this is not a protection delay.', '''
短路比邊界~Short-circuit ratio|短路比只描述部分網強特性。~Short-circuit ratio describes only part of grid strength.|比較同 SCR 不同阻抗相角。~Compare equal SCR with different impedance angles.
阻抗掃頻~Impedance scan|控制互動可在非基頻處失穩。~Control interactions can destabilize nonfundamental frequencies.|比較設備及電網頻率響應。~Compare device and grid frequency responses.
模型降階~Model reduction|平均模型忽略開關波紋與部分故障路徑。~Averaged models omit ripple and some fault paths.|與開關模型比較指定事件。~Compare selected events against a switching model.
直流能量~DC energy|功率不平衡改變電容儲能和電壓。~Power imbalance changes capacitor energy and voltage.|核對 ∫ΔPdt 與 Δ(CV²/2)。~Check ∫ΔPdt against Δ(CV²/2).
閥損失分布~Valve loss distribution|開關及導通損失分配依工作點改變。~Switching and conduction losses vary by operating point.|繪製 P–Q 工作點熱分布。~Map thermal loss over P–Q operating points.
冷卻冗餘~Cooling redundancy|剩餘冷卻能力限制故障後功率。~Remaining cooling capacity limits post-fault power.|比較單泵失效的熱暫態。~Compare thermal transients after one pump fails.
限流優先序~Current priorities|限流時有功與無功不能同時任意維持。~Current limits constrain simultaneous active and reactive support.|畫電流圓與優先序切換。~Plot current circles and priority changes.
站間下垂~Interstation droop|下垂可分攤功率但保留電壓偏差。~Droop shares power while retaining voltage deviation.|比較兩站不同下垂係數。~Compare unequal droop gains at two stations.
頻率支援能量~Frequency-support energy|短暫支援需可用能源與功率通道。~Transient support needs available energy and a power path.|列來源、持續時間及復原需求。~List source, duration and recovery requirements.
交流故障回放~AC-fault replay|電壓不平衡引入負序及雙頻功率。~Unbalance introduces negative sequence and double-frequency power.|分解正負序與直流波紋。~Separate sequences and DC ripple.
直流故障路徑~DC-fault paths|閉鎖閥不保證所有拓撲都阻斷故障電流。~Valve blocking does not stop every topology's fault current.|標出二極體及交流供電路徑。~Mark diode and AC-feed paths.
控制版本驗收~Control-version acceptance|相同硬體不同韌體可能改變故障動態。~Different firmware can change faults on identical hardware.|保留參數雜湊及事件回放集。~Retain parameter hashes and replay cases.
''',[(212,'MMC 子模組能量構成站級能量~MMC submodule energy builds station-level energy','站級包含電網與保護邊界~Station studies include grid and protection boundaries'),(223,'弱網互動及限流需共同分析~Weak-grid interaction and limiting need joint analysis','構網不是每一台 VSC 的預設能力~Grid forming is not every VSC default')])
add(212,'子模組能量、環流及電容均壓~Submodule energy, circulating current and capacitor balancing','拓撲與額定~Topology and rating|能量與調變~Energy and modulation|環流與控制~Circulating-current control|失效與驗證~Faults and verification','hvdc forming',
'假設每子模組電容 2 mF、電壓 2 kV，能量為 4 kJ；一臂 100 個為 400 kJ。若每臂需合成 200 kV，少一顆旁路後理想平均需 200/99≈2.0202 kV，仍須驗證額定及動態。~At 2 mF and 2 kV each submodule stores 4 kJ; 100 per arm store 400 kJ. Synthesizing 200 kV with one bypassed module ideally needs 200/99≈2.0202 kV each, subject to ratings and dynamics.', '''
半橋與全橋~Half and full bridges|全橋可提供負電壓但增加元件及損失。~Full bridges provide negative voltage but add devices and losses.|比較可合成電壓集合。~Compare achievable voltage sets.
臂電壓分配~Arm voltage allocation|上下臂電壓共同決定交流端與內部環流。~Upper/lower voltages set AC output and internal current.|寫和模與差模方程。~Write common- and differential-mode equations.
子模組額定~Submodule rating|串聯數量需考慮動態波紋及備援。~Series count must include ripple and redundancy.|區分平均、峰值及故障後電壓。~Separate mean, peak and post-fault voltage.
電容能量~Capacitor energy|電容能量與電壓平方成正比。~Capacitor energy scales with squared voltage.|用充放電積分交叉驗證。~Cross-check against charge/discharge integration.
排序均壓~Sorting balance|插入選擇需依電流方向判斷充放電。~Insertion choices depend on charging current direction.|用正負電流各回放一次排序。~Replay sorting under both current signs.
階梯調變~Staircase modulation|階數增加改善波形但不消除所有諧波。~More levels improve waveforms without eliminating all harmonics.|比較電壓頻譜與取樣誤差。~Compare voltage spectra and sampling error.
二倍頻環流~Double-frequency circulation|交流功率波動會在臂間交換能量。~AC power oscillation exchanges energy between arms.|比較臂電流和子模組能量頻譜。~Compare arm-current and energy spectra.
臂電感~Arm inductance|較大電感限制 di/dt 也改變控制頻寬。~Larger inductance limits di/dt and alters bandwidth.|掃描電感與暫態響應。~Sweep inductance and transient response.
取樣與延遲~Sampling and delay|延遲侵蝕均壓及電流迴路相位裕度。~Delay erodes balancing and current-loop phase margins.|加入離散延遲比較根軌跡。~Compare poles with discrete delay.
模組旁路~Module bypass|旁路改變可用電壓與能量分布。~Bypass changes available voltage and stored-energy distribution.|檢查失效後各臂峰值。~Check post-fault peaks in every arm.
電容老化~Capacitor aging|電容下降使同電荷波動產生更大電壓波紋。~Lower capacitance increases voltage ripple for equal charge variation.|固定電流積分比較不同電容。~Compare capacitances at equal current integral.
多尺度驗證~Multiscale verification|平均模型與開關模型需在共同指標上對齊。~Averaged and switching models need shared validation metrics.|核對能量、峰值及諧波誤差。~Check energy, peaks and harmonic error.
''',[(211,'子模組是換流閥的基礎~Submodules form converter valves','換流站多了變壓器、電網及輔助系統~Stations add transformers, grid and auxiliaries'),(213,'電壓源與電流迴路可遷移~Voltage-source and current loops transfer','STATCOM 不一定提供持續有功輸出~STATCOM need not provide sustained active power')])
add(213,'無功電流、電壓支援與換流器限流~Reactive current, voltage support and converter current limits','電網需求~Grid needs|換流與能量~Conversion and energy|控制與限制~Control and limits|擾動驗證~Disturbance validation','facts forming',
'三相假設線電壓 33 kV、純無功線電流 1000 A，Q=√3VI≈57.16 MVAr。電壓降為 0.8 pu、同電流上限時 Q≈45.73 MVAr；未含變壓器及動態限制。~For three-phase line voltage 33 kV and pure reactive line current 1000 A, Q=√3VI≈57.16 MVAr. At 0.8 pu voltage with the same current cap, Q≈45.73 MVAr; transformer and dynamic constraints are omitted.', '''
無功符號~Var sign|感性與容性符號需全案一致。~Inductive and capacitive signs need consistent convention.|用相位圖核對電流方向。~Check current direction with phasors.
併聯位置~Shunt location|接入母線強度影響電壓支援效率。~Bus strength affects voltage-support effectiveness.|比較不同母線的電壓敏感度。~Compare voltage sensitivity at different buses.
PQ 能力~PQ capability|固定電流圓限制可用無功。~A fixed current circle bounds available reactive power.|在不同電壓畫能力曲線。~Plot capability at different voltages.
直流電容~DC capacitor|直流電容供暫態能量而非無限有功。~DC capacitance supplies transient, not unlimited, active energy.|核對損耗補償及電壓恢復。~Check loss replenishment and voltage recovery.
濾波電抗~Filter reactance|耦合電抗連結換流電壓差與電流。~Coupling reactance links voltage difference to current.|比較固定電壓差的電流響應。~Compare current at fixed voltage difference.
換流熱限制~Converter thermal limits|RMS 與脈衝電流造成不同熱累積。~RMS and pulse currents create different thermal accumulation.|把功率循環映射到結溫。~Map duty cycles into junction temperature.
電壓下垂~Voltage droop|下垂降低多設備爭奪同一電壓目標。~Droop reduces competition over one voltage target.|比較雙機不同下垂配比。~Compare unequal droop sharing between two units.
電流解耦~Current decoupling|dq 軸交叉項隨電網頻率與電感變化。~dq coupling depends on frequency and inductance.|在模型中移除解耦觀察交互響應。~Remove model decoupling and inspect cross-responses.
弱網互動~Weak-grid interaction|控制器與電網阻抗可形成振盪。~Control and grid impedance can create oscillation.|用阻抗掃頻而非只測穩態。~Use impedance scans, not steady-state checks alone.
電壓驟降~Voltage sag|降壓時固定電流不等於固定 MVAr。~Fixed current during sag does not mean fixed MVAr.|重算電壓相依無功能力。~Recalculate voltage-dependent reactive capability.
故障恢復~Fault recovery|解除限流時積分狀態會影響過衝。~Integrator state affects overshoot when limiting ends.|比較有無抗飽和回放。~Compare replay with and without anti-windup.
性能交接~Performance handoff|響應速度需定義擾動、量測及容差帶。~Response time needs defined disturbance, measurement and band.|報告上升、整定與過衝三指標。~Report rise, settling and overshoot.
''',[(214,'皆藉無功調節電壓~Both regulate voltage with vars','SVC 的固定電納能力隨 V² 變化~Fixed-susceptance SVC capability varies with V²'),(215,'均支援電壓與故障期間需求~Both support voltage and disturbance needs','調相機具有旋轉慣量與不同短路特性~Condensers add rotating inertia and different fault behavior')])
add(214,'可控電納、諧波濾波與低電壓能力~Controlled susceptance, harmonic filtering and low-voltage capability','電納與需求~Susceptance and needs|閥與濾波~Valves and filtering|調節與共振~Regulation and resonance|驗證與老化~Verification and aging','svc facts',
'假設額定電壓下固定容性電納提供 100 MVAr；電壓 0.8 pu 時 Q=V²B 變為 64 MVAr。這是假設電納固定的比較，不包括 TCR 動作與限流。~Assume fixed capacitive susceptance supplies 100 MVAr at rated voltage. At 0.8 pu, Q=V²B gives 64 MVAr. This fixed-susceptance comparison excludes TCR action and current limits.', '''
電納模型~Susceptance model|並聯電納的無功與電壓平方相關。~Shunt-susceptance reactive power scales with voltage squared.|在三種電壓重算相同電納。~Recalculate one susceptance at three voltages.
TCR 支路~TCR branch|控制導通角改變電抗器基頻電流。~Conduction angle changes reactor fundamental current.|比較全導通及部分導通波形。~Compare full and partial conduction waveforms.
TSC 支路~TSC branch|電容支路切換形成離散電納級距。~Capacitor switching creates discrete susceptance steps.|畫支路組合及級距表。~Map branch combinations and steps.
閥散熱~Valve cooling|閥損失與導通角及電流波形相關。~Valve loss depends on conduction angle and waveform.|依波形积分導通損失。~Integrate conduction loss over waveforms.
諧波產生~Harmonic production|非正弦電流形成多次諧波。~Nonsinusoidal current contains multiple harmonics.|用傅立葉分量檢查模型。~Inspect Fourier components of the model.
濾波調諧~Filter tuning|LC 支路共振頻率受元件偏差改變。~LC resonant frequency changes with component tolerance.|掃描 L、C 偏差的阻抗最低點。~Sweep L/C tolerance and impedance minima.
電網共振~Grid resonance|電容與上游電感可能放大部分諧波。~Capacitance and upstream inductance may amplify harmonics.|比較投入前後全網阻抗頻譜。~Compare network impedance before and after connection.
電壓調節~Voltage regulation|控制增益需配合母線短路容量。~Control gain must match bus short-circuit strength.|比較強網與弱網階躍響應。~Compare strong- and weak-grid step responses.
支路協調~Branch coordination|連續 TCR 與離散 TSC 需避免反覆切換。~Continuous TCR and discrete TSC need anti-chatter coordination.|檢查遲滯及最短駐留模型。~Inspect hysteresis and dwell models.
低壓能力~Low-voltage capability|電壓降低會削弱電納型無功支援。~Low voltage weakens susceptance-based var support.|與固定電流 STATCOM 曲線對照。~Compare against a current-limited STATCOM curve.
電容劣化~Capacitor degradation|電容偏移會改變無功及調諧頻率。~Capacitance drift changes vars and tuning frequency.|將容量趨勢與諧波熱點配對。~Pair capacitance trends with harmonic hot spots.
放行邊界~Release boundaries|穩態無功達標不能證明所有故障穩定。~Steady var compliance cannot prove all-fault stability.|交付多工況與設備退出矩陣。~Deliver operating and outage scenario matrices.
''',[(213,'電壓支援目標相同~The voltage-support goal is shared','電流源能力與電納型能力不同~Current-limited and susceptance-limited capabilities differ'),(229,'濾波都需考慮共振與量測~Both filtering tasks need resonance and measurement','SVC 濾波須配合電抗器諧波~SVC filters must accommodate reactor harmonics')])
add(215,'旋轉慣量、勵磁及短路支援~Rotating inertia, excitation and fault support','需求與能力~Needs and capability|轉子與起動~Rotor and starting|勵磁及熱~Excitation and heat|動態與驗收~Dynamics and acceptance','cond gen',
'假設慣性常數 H=4 s、額定 S=100 MVA，轉動能量 E=HS=400 MJ。若頻率從 50 降到 49 Hz 且轉速同比變化，可釋能 400[1−(49/50)²]=15.84 MJ；未含控制及損失。~Assume inertia constant H=4 s and rating S=100 MVA: rotating energy E=HS=400 MJ. A proportional speed drop from 50 to 49 Hz releases 400[1−(49/50)²]=15.84 MJ, before controls and losses.', '''
無軸功輸入~No shaft-power input|調相機從電網吸收功率補償損失。~A condenser draws grid power to cover losses.|畫有功及無功分離的能流圖。~Draw separate active and reactive flows.
短路容量~Fault contribution|次暫態電抗影響初期故障電流。~Subtransient reactance affects initial fault current.|比較同 MVA 不同 X″ 的模型。~Compare equal MVA with different X″.
慣性常數~Inertia constant|H 是額定容量基準下的儲能時間比。~H is stored energy divided by rating.|將不同基準 H 換成 MJ 比較。~Convert different H bases to MJ.
飛輪選擇~Flywheel choice|飛輪增加慣量亦增加軸系應力。~Flywheels add inertia and shaft stress.|比較能量、臨界轉速及支撐。~Compare energy, critical speed and support.
起動系統~Starting system|起動變頻器需跨越加速及同步階段。~A starter must cover acceleration and synchronization.|以離線功率積分估計加速時間。~Estimate acceleration time by offline power integration.
軸承損失~Bearing losses|軸承及風摩損失影响待機耗電。~Bearing and windage losses affect standby consumption.|分解轉速相關損失項。~Separate speed-dependent losses.
勵磁能力~Excitation capability|過勵供無功但受轉子熱限制。~Overexcitation supplies vars but is rotor-heat limited.|標示持續與短時能力區。~Mark continuous and short-time capability.
欠勵邊界~Underexcitation limits|欠勵吸收無功可能受端部熱與穩定限制。~Underexcitation can be limited by end heating and stability.|比較端部熱圖與功角模型。~Compare end heating with angle stability.
冷卻需求~Cooling demand|零 MW 輸出仍可能有顯著熱損失。~Zero MW output can still involve substantial loss.|核對電輸入與冷卻熱量。~Check electrical input against rejected heat.
頻率擾動~Frequency disturbance|慣量响應取決於頻率變化率。~Inertial response depends on rate of frequency change.|比較相同頻差不同斜率。~Compare equal deviations with different slopes.
勵磁調速分離~Excitation-speed separation|電壓與頻率支援有不同能量來源。~Voltage and frequency support have different energy sources.|分開磁場與轉動儲能。~Separate field and rotational energy.
系統聯合驗收~System acceptance|設備能力需放回電網故障及維護情境。~Equipment capability needs grid-fault and maintenance context.|比較調相機退出後的網強。~Compare grid strength with the condenser unavailable.
''',[(201,'共用同步機與絕緣原理~Synchronous-machine and insulation principles transfer','發電機供有功而調相機主要耗損補償~Generators supply active power; condensers mainly cover losses'),(213,'兩者可供動態無功~Both can supply dynamic vars','旋轉慣量與半導體電流限制不可等同~Rotating inertia differs from semiconductor current limits')])
add(216,'功角、串並聯補償與控制互動~Power angle, series/shunt compensation and control interaction','潮流機制~Power-flow mechanisms|補償拓撲~Compensation topologies|動態控制~Dynamic control|系統驗證~System verification','facts get psse',
'無損單線教學模型：V₁=V₂=1 pu、X=0.5 pu、δ=30°，P=V₁V₂ sinδ/X=1 pu。X 降到 0.4 pu 時得 1.25 pu；不代表熱容量或穩定限制也提高 25%。~For a lossless teaching line V₁=V₂=1 pu, X=0.5 pu and δ=30°, P=V₁V₂ sinδ/X=1 pu. Reducing X to 0.4 gives 1.25 pu, not an automatic 25% thermal or stability increase.', '''
功角關係~Power-angle relation|傳輸功率取決於電壓、電抗及相角。~Power transfer depends on voltage, reactance and angle.|逐變數掃描並標示無損假設。~Sweep variables while marking the lossless assumption.
無功位置~Var location|就地無功可減少遠距離無功流。~Local vars can reduce long-distance reactive flow.|比較線損與母線電壓。~Compare losses and bus voltages.
網路迴路~Network loops|迴路阻抗改變會重新分配平行線潮流。~Loop impedance changes redistribute parallel-line flow.|以兩路線模型檢查負載轉移。~Check load transfer in a two-path model.
串聯補償~Series compensation|串聯電容降低基頻等效電抗。~Series capacitance reduces fundamental effective reactance.|重算潮流及故障阻抗。~Recalculate flow and fault impedance.
並聯補償~Shunt compensation|並聯設備主要調節母線無功平衡。~Shunt devices primarily regulate bus reactive balance.|對比相同 Mvar 不同位置。~Compare equal Mvar at different locations.
移相控制~Phase-shift control|相移可改變潮流而非增加導線熱額定。~Phase shift redirects flow without raising conductor thermal rating.|列潮流改善與熱限制的交集。~Intersect flow benefits with thermal limits.
阻尼迴路~Damping loops|附加控制需對目標模態有正阻尼。~Supplementary control must damp the target mode.|比較特徵值與環路相位。~Compare eigenvalues and loop phase.
次同步互動~Subsynchronous interaction|補償網路可能與機械扭振或控制互動。~Compensation may interact with torsional or control modes.|掃描電氣及機械模態接近區。~Scan nearby electrical and mechanical modes.
飽和與延遲~Saturation and delay|執行器限制使線性控制預測失準。~Actuator limits invalidate some linear predictions.|比較大擾動和小擾動模型。~Compare large- and small-disturbance models.
設備退出~Device outage|補償退出可突然改變網路阻抗。~Compensator outage can abruptly change network impedance.|模擬 N−1 並檢查其他線路。~Simulate N−1 and inspect remaining lines.
保護相容~Protection compatibility|改變阻抗會影響距離保護的量測。~Impedance changes affect distance-protection measurements.|在 R–X 平面重畫故障軌跡。~Replot fault trajectories on the R–X plane.
收益邊界~Benefit boundaries|潮流可控不等於所有故障下均穩定。~Controllable flow does not imply stability for every fault.|分開容量、損失及穩定驗收。~Separate capacity, loss and stability acceptance.
''',[(213,'並聯無功是 FACTS 一條路徑~Shunt vars form one FACTS route','整網控制還含串聯及移相作用~Network control also includes series and phase-shift effects'),(218,'補償改變保護所見阻抗~Compensation changes relay-seen impedance','潮流調節目標不等於故障辨識目標~Flow regulation differs from fault discrimination')])
add(217,'時間同步、相量誤差與廣域資料品質~Time synchronization, phasor error and wide-area data quality','相量與時間~Phasors and time|量測鏈~Measurement chain|集中與分析~Aggregation and analysis|失效與驗證~Failures and verification','pmu meter',
'假設頻率 60 Hz，時間偏差 Δt=1 μs，純相位誤差 Δθ=2πfΔt=0.000377 rad≈0.0216°。小角度且幅值無誤差時 TVE≈0.0377%；這不含感測器或動態誤差。~At 60 Hz and Δt=1 μs, phase error Δθ=2πfΔt=0.000377 rad≈0.0216°. With no amplitude error and small angle, TVE≈0.0377%; sensor and dynamic errors are excluded.', '''
相量定義~Phasor definition|相量把近似正弦訊號映射成複數幅角。~Phasors map approximately sinusoidal signals to complex amplitude.|寫明 RMS 或峰值慣例。~State RMS or peak convention.
共同時間~Common time|跨站相角需共用時間參考。~Interstation angles need a common time reference.|比較時間偏差造成的角度誤差。~Compare angle errors from timing offsets.
頻率估計~Frequency estimation|相角斜率與頻率偏差相關。~Angle slope relates to frequency deviation.|由展相後角度求導並比較。~Differentiate unwrapped angle and compare.
感測器鏈~Sensor chain|CT/PT 相移與頻率響應會污染相量。~CT/PT phase and frequency response affect phasors.|分開儀表誤差及估計器誤差。~Separate instrument and estimator errors.
取樣窗口~Sampling window|長窗口降噪但延遲動態響應。~Long windows reduce noise but delay response.|比較階躍的誤差與延遲。~Compare step error and delay.
總向量誤差~Total vector error|TVE 同時包含幅值及相位誤差。~TVE includes magnitude and phase errors.|以複數差值核對百分比。~Check percentages using complex differences.
相量集中~Phasor concentration|資料需依時間戳而非到達順序對齊。~Data align by timestamp, not arrival order.|打亂封包順序檢查重排。~Shuffle packets and inspect reordering.
延遲與丟包~Latency and loss|插值資料不能冒充實際觀測。~Interpolated data are not actual observations.|保留缺測遮罩與插值旗標。~Retain missing-data and interpolation flags.
振盪模態~Oscillation modes|多站振盪相位有助判斷模態形狀。~Multisite oscillation phase informs mode shapes.|比較共同振盪與本地噪聲。~Compare shared oscillations with local noise.
時鐘異常~Clock anomalies|時間跳變可偽裝成電網相角事件。~Clock jumps can resemble grid-angle events.|對照時鐘品質與頻率一致性。~Cross-check clock quality and frequency consistency.
資料追溯~Data provenance|校正與韌體版本會改變估計行為。~Calibration and firmware can alter estimation behavior.|保留訊號、時鐘及演算法版本。~Retain signal, clock and algorithm revisions.
動態驗證~Dynamic validation|靜態精度不能代表快速事件性能。~Static accuracy cannot establish fast-event performance.|分別評估穩態、斜坡及階躍。~Assess steady, ramp and step cases separately.
''',[(220,'同步與資料品質共同重要~Synchronization and data quality matter in both','程序匯流排傳瞬時取樣而 PMU 傳相量~Process buses carry samples while PMUs carry phasors'),(226,'廣域量測可驗證模態模型~Wide-area measurements can validate modal models','量測的模式辨識仍受噪聲與觀測性限制~Measured mode identification still faces noise and observability limits')])
add(218,'視在阻抗、故障回路與動作區辨識~Apparent impedance, fault loops and zone discrimination','回路與阻抗~Loops and impedance|區域與偏差~Zones and bias|暫態與閉鎖~Transients and blocking|回放與交接~Replay and handoff','distance relay',
'離線示例同一回路相量 V=20 kV∠30°、I=1 kA∠0°，Z=V/I=20∠30° Ω=17.32+j10 Ω。這是回路示意，接地故障需補償，不能直接作保護整定。~For one offline loop V=20 kV∠30° and I=1 kA∠0°, Z=20∠30° Ω=17.32+j10 Ω. Ground faults need compensation; this is not a protection setting.', '''
故障回路~Fault loops|相間與接地故障使用不同電壓電流組合。~Phase and ground faults use different V/I combinations.|逐回路寫出量測相量。~Write measured phasors for each loop.
序網補償~Sequence compensation|零序路徑會改變接地故障視在阻抗。~Zero-sequence paths alter apparent ground-fault impedance.|比較補償前後 R–X 軌跡。~Compare compensated and uncompensated R–X trajectories.
R–X 平面~R–X plane|阻抗大小相同不代表落在同一動作區。~Equal magnitude does not imply the same operating zone.|用複數坐標而非僅距離排序。~Use complex coordinates rather than magnitude ordering.
故障電阻~Fault resistance|電弧及接地電阻會使量測點偏移。~Arc and grounding resistance shift measurements.|掃描故障電阻與故障位置。~Sweep fault resistance and location.
遠端饋入~Remote infeed|遠端電流可增加本端所見阻抗偏差。~Remote infeed can bias locally seen impedance.|比較單端及雙端供電模型。~Compare one- and two-end source models.
負載侵入~Load encroachment|重載軌跡可能接近保護區。~Heavy-load trajectories can approach operating zones.|疊合負載與故障案例。~Overlay load and fault cases.
互感耦合~Mutual coupling|平行線零序互感影響接地故障量測。~Parallel-line zero-sequence coupling affects ground loops.|比較鄰線運行與退出狀態。~Compare adjacent-line in-service and outage states.
CVT 暫態~CVT transients|電壓量測暫態可造成短時間阻抗偏差。~Voltage-transformer transients can briefly bias impedance.|在回放中加入感測暫態模型。~Add sensor transients to replay.
功率擺動~Power swings|穩定擺動也能穿越部分阻抗區域。~Stable swings can cross some impedance regions.|比較軌跡速度與故障突變。~Compare trajectory speed with fault discontinuities.
通訊協調~Communication coordination|通道延遲與失效會改變端間協調。~Channel delay and failure affect end-to-end coordination.|用訊息延遲及失聯情境回放。~Replay delay and loss-of-channel cases.
時限分級~Time grading|後備時限需與相鄰保護及斷路器配合。~Backup timing must coordinate with neighboring protection and breakers.|建立假想事件時間線。~Build a hypothetical event timeline.
測試矩陣~Test matrix|通過內部故障測試不等於外部不誤動。~Internal-fault success does not prove external-fault security.|同時列應動與不應動案例。~List both operate and restrain cases.
''',[(219,'均需量測及故障辨識~Both need measurement and fault discrimination','差動比較邊界電流而距離比較視在阻抗~Differential compares boundary currents; distance uses impedance'),(216,'補償設備改變阻抗軌跡~Compensators change impedance trajectories','潮流控制穩定不代表保護設定相容~Stable flow control does not ensure relay compatibility')])
add(219,'邊界電流、CT 飽和與差動制動~Boundary currents, CT saturation and differential restraint','保護邊界~Protection boundaries|量測匹配~Measurement matching|制動與分類~Restraint and classification|通訊與回放~Communication and replay','relay distance',
'以流入區域為正，假設兩端相量 +1000 A 與 −980 A，差流為 20 A；定義制動電流 (|I₁|+|I₂|)/2=990 A，差流比約 2.02%。這只是教學判讀，實際算法和門檻依裝置而異。~With currents positive into a zone, +1000 A and −980 A give differential 20 A. Defining restraint as (|I₁|+|I₂|)/2 gives 990 A and ratio 2.02%; actual algorithms and thresholds are device-specific.', '''
區域邊界~Zone boundary|差動保護比較穿越明確邊界的電流。~Differential protection compares currents across defined boundaries.|畫 CT 位置及未覆蓋區。~Mark CT locations and uncovered regions.
極性慣例~Polarity convention|錯誤極性會使穿越電流變成差流。~Wrong polarity turns through current into differential current.|以外部負載案例核對符號。~Check signs with an external-load case.
變比歸一~Ratio normalization|不同 CT 變比需換算到同一基準。~Different CT ratios need a common base.|用一次電流重建各端值。~Reconstruct primary currents at each end.
向量組補償~Vector-group compensation|變壓器相移需在電流比較前補償。~Transformer phase shifts need compensation before comparison.|比較補償前後平衡三相。~Compare balanced currents before/after compensation.
CT 飽和~CT saturation|外部大故障的 CT 飽和可產生虛假差流。~CT saturation on external faults can create false differential.|比較磁通積分與波形削頂。~Compare flux integral with waveform clipping.
直流偏移~DC offset|非對稱故障使 CT 磁通偏移累積。~Asymmetric faults accumulate CT flux offset.|掃描故障初相與 X/R。~Sweep inception angle and X/R.
制動特性~Restraint characteristic|制動需兼顧內部靈敏度及外部安全性。~Restraint balances internal sensitivity and external security.|以差流—制動平面畫案例。~Plot cases on differential/restraint axes.
湧流辨識~Inrush discrimination|勵磁湧流與故障可能有重疊特徵。~Inrush and faults can share features.|比較多種波形證據而非單一比例。~Compare multiple features, not one ratio.
充電電流~Charging current|長線路充電電流不會由負載端完全抵消。~Long-line charging does not fully cancel at the load end.|將分布電容納入區域電流平衡。~Include distributed capacitance in current balance.
時間偏差~Timing skew|兩端取樣偏差會形成相位性差流。~End-to-end sampling skew creates phase-related differential.|對時間偏差做靈敏度掃描。~Sweep sensitivity to timing skew.
通道失效~Channel failure|資料中斷需明確降階和後備邏輯。~Data interruption needs explicit fallback logic.|用失聯及恢復回放檢查狀態。~Replay channel loss and recovery states.
端到端驗收~End-to-end acceptance|單機測試無法覆蓋跨端時間和接線。~Single-device tests miss inter-end timing and wiring.|以相同事件檔核對兩端輸出。~Compare both ends using one event file.
''',[(218,'都需驗證外部故障不誤動~Both require external-fault security','距離不必依賴同樣的端間電流比較~Distance need not use the same inter-end current comparison'),(220,'數位取樣可供差動演算法~Digital samples can feed differential algorithms','資料傳輸正確不代表極性與變比正確~Correct transport does not prove polarity or ratio')])
add(220,'取樣值、精準時鐘與程序匯流排可靠度~Sampled values, precise clocks and process-bus reliability','資料與語義~Data and semantics|網路與同步~Network and synchronization|冗餘與保護~Redundancy and protection|配置與驗收~Configuration and acceptance','distance relay pmu',
'假設 8 串資料流，每串 4800 frame/s，每 frame 線上佔 160 byte，原始負載 8×4800×160×8=49.152 Mbit/s。未計其他流量與突發緩衝；不能只用平均速率證明無丟包。~For eight streams, 4800 frames/s each and 160 on-wire bytes/frame, raw load is 49.152 Mbit/s. Other traffic and burst buffers are excluded; mean rate alone cannot prove lossless transport.', '''
程序與站控~Process versus station bus|瞬時量測與站級命令具有不同時效。~Instantaneous samples and station commands have different deadlines.|分類資料來源與使用者。~Classify data producers and consumers.
取樣值語義~Sample semantics|同一數值需附通道、比例與品質。~A value needs channel, scale and quality metadata.|核對配置檔與實際通道。~Compare configuration with actual channels.
合併單元~Merging units|類比前端誤差仍會進入數位取樣。~Analog-front-end errors remain in digital samples.|把 ADC 與感測器誤差分列。~Separate ADC and sensor errors.
封包預算~Packet budget|頻寬計算需包含線上開銷。~Bandwidth calculations need on-wire overhead.|以封包率乘實際線上長度。~Multiply packet rate by on-wire length.
優先序~Traffic priority|高優先權不能消除所有排隊延遲。~High priority does not eliminate all queue delay.|注入假想競爭流量比較尾延遲。~Compare tail delay under synthetic competing traffic.
時鐘路徑~Clock paths|非對稱網路延遲會偏移時間估計。~Asymmetric network delay biases time estimates.|比較對稱與不對稱鏈路。~Compare symmetric and asymmetric links.
冗餘網路~Redundant networks|雙路徑需避免共因失效。~Dual paths must avoid common-cause failure.|標示共用交換器與電源。~Mark shared switches and power supplies.
重複封包~Duplicate packets|冗餘接收需辨識重複而不漏掉新取樣。~Redundant reception must discard duplicates without losing samples.|回放序號重複與跳號。~Replay duplicate and missing sequence numbers.
GOOSE 狀態~GOOSE states|事件訊息需檢查狀態號、序號及時效。~Event messages need state, sequence and freshness checks.|比較新事件及逾時訊息。~Compare new events with expired messages.
配置一致性~Configuration consistency|配置錯配可能傳輸正常但功能錯誤。~Configuration mismatch can preserve transport but break function.|核對版本雜湊及訂閱關係。~Check revision hashes and subscriptions.
資料失真~Invalid data|品質不良取樣不能無條件供保護動作。~Invalid samples must not unconditionally drive protection.|測試品質旗標與降階處置。~Test quality flags and fallback handling.
系統回放~System replay|網路、時鐘與保護需共同回放驗證。~Network, clock and protection need joint replay.|同時記錄封包及保護決策時間。~Log packets and decision times together.
''',[(217,'皆仰賴時間品質~Both depend on timing quality','相量是衍生量，程序匯流排運送即時樣本~Phasors are derived quantities; process buses transport samples'),(219,'差動依賴資料相位一致~Differential protection depends on phase-consistent data','網路驗收之外還需 CT 與極性驗證~CT and polarity checks remain beyond network acceptance')])
add(221,'故障區段辨識、拓撲推理與復電容量~Fault-section identification, topology reasoning and restoration capacity','網路模型~Network model|故障判讀~Fault interpretation|復電規劃~Restoration planning|事件驗證~Event validation','flisr sincal',
'假想故障使 1000 戶停電 60 min，客戶停電時間為 60000 戶·min；若 700 戶在 5 min 復電，其餘 300 戶仍 60 min，合計 21500 戶·min，降低約 64.17%。不是任何真實配電網績效。~A hypothetical outage of 1000 customers for 60 min gives 60000 customer-minutes. Restoring 700 at 5 min while 300 remain out for 60 min gives 21500 customer-minutes, a 64.17% reduction; no real feeder performance is claimed.', '''
拓撲圖~Topology graph|開關狀態決定電氣連通而非地理接近。~Switch states determine electrical connectivity, not proximity.|由節點邊表重建供電路徑。~Reconstruct supply paths from nodes and edges.
相別映射~Phase mapping|單相支線需正確相別才能計算不平衡。~Single-phase branches need correct phase assignments.|檢查相別與量測相角一致性。~Check phase labels against measured angles.
負載估計~Load estimates|缺少即時量測時需保留估計不確定度。~Missing live measurements require uncertainty in load estimates.|用上限負載重算備援能力。~Recalculate backup capacity at upper-bound load.
故障指示~Fault indicators|故障電流通過不代表指示器就在故障點。~Fault-current passage does not locate the fault at the indicator.|沿拓撲比較上下游指示。~Compare upstream/downstream indications along topology.
暫態與永久~Temporary versus permanent|暫態故障與持續故障需不同事件分類。~Transient and persistent faults need different classification.|比較事件持續性與重複模式。~Compare persistence and repetition patterns.
量測陳舊~Stale measurements|過時開關狀態可能導致錯誤連通推論。~Stale switch states can cause false connectivity inference.|以時間戳建立資料有效區間。~Define validity intervals from timestamps.
隔離集合~Isolation set|隔離需切斷所有可能供電路徑。~Isolation must account for every possible feed path.|在離線圖上搜尋割集。~Find cut sets in an offline graph.
備援潮流~Backup load flow|復電路徑仍受熱容量及電壓限制。~Restoration paths remain bounded by thermal and voltage limits.|逐候選拓撲重算潮流。~Recalculate each candidate topology.
分散電源~Distributed generation|反向潮流可改變故障方向與隔離範圍。~Reverse flow changes fault direction and isolation needs.|比較發電高低兩種情境。~Compare high- and low-generation scenarios.
冷負載回復~Cold-load pickup|復電瞬間需求可能高於停電前負載。~Pickup demand can exceed pre-outage demand.|掃描回復倍數與衰減時間。~Sweep pickup multiplier and decay time.
指令回授~Command feedback|命令送出不代表設備已到指定狀態。~Sending a command does not prove the requested state.|檢查確認、逾時及衝突回授。~Check confirmation, timeout and conflicting feedback.
績效與限制~Performance and limits|復電比例需同時報時間及未復電客群。~Restoration fraction needs time and remaining-customer context.|以戶分鐘及失敗案例共同報告。~Report customer-minutes and failed cases together.
''',[(220,'自動化依賴可信資料與時效~Automation depends on trustworthy, timely data','FLISR 加入全網拓撲及負載約束~FLISR adds network topology and load constraints'),(222,'供電分區與復原邏輯相關~Supply zones and restoration logic relate','孤島還需自行建立頻率及電壓~Islands must also establish frequency and voltage')])
add(222,'孤島功率平衡、同步條件與轉換動態~Island power balance, synchronization and transition dynamics','資源與邊界~Resources and boundaries|孤島控制~Island control|同步與切換~Synchronization and transition|擾動驗證~Disturbance verification','transition black forming',
'假設孤島負載 500 kW，持續發電 300 kW，電池需補 200 kW；支撐 30 min 的交流能量為 100 kWh。若放電效率 0.90，需可用直流能量 111.11 kWh，未計備援 SOC 或老化。~For island load 500 kW and generation 300 kW, a battery supplies 200 kW. Thirty minutes requires 100 kWh AC, or 111.11 kWh available DC at 0.90 discharge efficiency, before SOC reserve and aging.', '''
邊界定義~Boundary definition|公共連接點決定孤島的功率邊界。~The common coupling point defines island power boundaries.|畫輸入、負載及不可中斷支路。~Map inputs, loads and critical branches.
資源類型~Resource types|跟網型資源不能假定獨立建立電壓。~Grid-following resources cannot be assumed to establish voltage alone.|區分構網與跟網角色。~Separate grid-forming and following roles.
能量需求~Energy needs|功率餘額與可持續時間需分別驗算。~Power margin and duration require separate checks.|計算 kW 和 kWh 雙預算。~Calculate both kW and kWh budgets.
頻率下垂~Frequency droop|下垂分攤功率但留下穩態頻差。~Droop shares power while retaining steady frequency deviation.|比較一次下垂與二次恢復。~Compare primary droop and secondary restoration.
無功分攤~Var sharing|不同線阻抗可造成無功分攤誤差。~Unequal line impedance can bias var sharing.|以不同 R/X 模型比較。~Compare different R/X models.
負載優先序~Load priorities|卸載需依關鍵度與電力約束規劃。~Load shedding needs criticality and electrical constraints.|在模型中比較不同卸載集合。~Compare shedding sets in simulation.
電壓匹配~Voltage matching|再併網需同時核對幅值、頻率與相位。~Reconnection needs magnitude, frequency and phase agreement.|建立三條獨立容差曲線。~Create three independent tolerance traces.
相位漂移~Phase drift|微小頻差會累積成大相位差。~Small frequency error accumulates large phase error.|用 Δθ=2πΔft 預估漂移。~Estimate drift with Δθ=2πΔft.
切換延遲~Switching delay|機構延遲使預測閉合時相位不同。~Mechanical delay changes predicted closing phase.|將延遲及不確定度納入預測。~Include delay and uncertainty in prediction.
控制無擾轉換~Bumpless transition|切換模式需處理控制器積分狀態。~Mode changes must handle controller integral states.|比較有無狀態跟蹤的過衝。~Compare overshoot with/without state tracking.
不平衡負載~Unbalanced load|三相不平衡可造成負序與零序限制。~Unbalance can create negative- and zero-sequence limits.|分解相電流與中性線電流。~Separate phase and neutral currents.
復原驗收~Recovery acceptance|成功併網不能只看開關狀態。~Successful reconnection needs more than switch status.|核對電流峰值及穩定恢復時間。~Check current peaks and settling time.
''',[(223,'構網控制提供孤島參考~Grid-forming control provides island reference','微電網還需負載優先序與能源排程~Microgrids also need load priority and energy scheduling'),(225,'都需從有限資源恢復供電~Both restore supply from finite resources','孤島切換可能已有電壓，黑啟動起點不同~Island transition may already be energized; black start differs')])
add(223,'電壓成形、下垂與限流穩定性~Voltage formation, droop and current-limit stability','角色與模型~Roles and models|控制內部~Internal controls|限流與能源~Current and energy limits|網路驗證~Network verification','forming transition black',
'假想下垂係數 m=0.05 Hz/kW，新增有功 10 kW 導致一次控制頻率變化 Δf=−mΔP=−0.5 Hz。此斜率只供小型模型，未定義實際並網規範，二次控制可另行恢復頻率。~With hypothetical droop m=0.05 Hz/kW and +10 kW load, primary Δf=−mΔP=−0.5 Hz. This small-model slope is not a grid requirement; secondary control can restore frequency.', '''
成形與跟隨~Forming versus following|構網控制維持內部電壓相位狀態。~Grid-forming control maintains an internal voltage-phase state.|畫兩類控制的訊號依存圖。~Draw signal-dependency diagrams for both roles.
振盪器狀態~Oscillator state|內部相位積分頻率而非瞬間跳變。~Internal phase integrates frequency rather than jumping instantly.|檢查角度連續性及初始條件。~Check phase continuity and initial conditions.
等效阻抗~Virtual impedance|虛擬阻抗改變電壓下垂及分攤。~Virtual impedance changes voltage drop and sharing.|比較軟體阻抗與物理損耗差異。~Distinguish software impedance from physical loss.
有功下垂~Active-power droop|有功增量透過下垂改變頻率參考。~Active-power increments change frequency through droop.|核對斜率的 Hz/kW 單位。~Check slope units in Hz/kW.
無功下垂~Reactive-power droop|無功及線阻抗共同影響端電壓。~Vars and line impedance jointly affect terminal voltage.|比較感性與電阻性網路。~Compare inductive and resistive networks.
內迴路頻寬~Inner-loop bandwidth|迴路時間尺度需與取樣及濾波相容。~Loop timescales must fit sampling and filtering.|疊合各迴路頻率響應。~Overlay loop frequency responses.
限流模式~Current-limiting mode|電流飽和改變原本的電壓源行為。~Current saturation changes voltage-source behavior.|比較限流前後等效特性。~Compare characteristics before and during limiting.
能源可用性~Energy availability|虛擬慣量不能憑空提供實際能量。~Virtual inertia cannot create real energy.|對照能量來源與控制請求。~Match control requests to energy sources.
多機耦合~Multiple units|並聯構網機會透過線路耦合。~Parallel grid-forming units couple through lines.|比較同參數與不匹配控制。~Compare matched and mismatched controls.
弱網測試~Weak-grid tests|低短路比不足以唯一指定穩定程度。~Low SCR alone does not specify stability.|掃描阻抗角與控制延遲。~Sweep impedance angle and control delay.
故障後重同步~Post-fault resynchronization|故障期間角度漂移影響恢复穩定。~Fault-period phase drift affects recovery stability.|記錄限流解除時的功角。~Record angle when current limiting ends.
模型驗證~Model validation|模型需包含保護、限幅及控制切換。~Models need protection, saturation and control transitions.|用多種擾動驗證同一參數集。~Validate one parameter set against varied disturbances.
''',[(222,'兩課皆處理孤島電壓與頻率~Both address island voltage and frequency','單台控制器不是完整微電網能源管理~One controller is not full microgrid energy management'),(213,'可共享換流器與電流迴路~Converter and current-loop structures can transfer','無功補償不自动代表黑啟動能力~Var compensation does not automatically imply black start')])
add(224,'併網邊界、故障穿越與孤島辨識~Interconnection boundaries, ride-through and island detection','要求與模型~Requirements and models|量測與故障~Measurements and faults|控制與保護~Control and protection|驗證與協調~Verification and coordination','forming relay string',
'假設 1 MVA 逆變器、線電壓 400 V，額定 I=S/(√3V)=1443.4 A。若短時限流為假設的 1.2 pu，短時 RMS 電流上限 1732.1 A；這不是實際產品或標準限值。~For an assumed 1 MVA inverter at line voltage 400 V, rated I=S/(√3V)=1443.4 A. An illustrative 1.2 pu short-term RMS limit is 1732.1 A, not a product or standards limit.', '''
連接點~Connection point|合規量測位置需與設備端分清。~Compliance measurement points may differ from device terminals.|標示變壓器及線路壓降。~Mark transformer and line drops.
適用要求~Applicable requirements|電壓級別與管轄區決定適用規則版本。~Voltage level and jurisdiction determine applicable rule revisions.|建立要求來源與測試項目對照。~Map requirement sources to test items.
額定基準~Rating bases|pu 值需標明容量及電壓基準。~Per-unit values need power and voltage bases.|以安培及伏特回算交叉檢查。~Cross-check by converting to amperes and volts.
故障電流~Fault current|逆變器故障電流受控制與限流影響。~Inverter fault current depends on controls and limiting.|比較旋轉機與換流器波形。~Compare rotating-machine and converter waveforms.
方向判讀~Directional interpretation|分散發電可使故障電流方向反轉。~Distributed generation can reverse fault-current direction.|比較發電最大及最小工況。~Compare maximum and minimum generation.
感測暫態~Measurement transients|濾波延遲會影響欠壓與頻率判斷。~Filter delay affects undervoltage and frequency decisions.|掃描視窗長度與事件延遲。~Sweep window length and decision delay.
故障穿越~Ride-through|穿越功能需與設備熱限制及保護協調。~Ride-through needs coordination with heat limits and protection.|比較電壓時間軌跡與要求區域。~Compare voltage-time traces with required regions.
孤島偵測~Island detection|發用電接近平衡時被動偵測可能較難。~Passive detection can struggle near power balance.|掃描有功及無功不匹配量。~Sweep active and reactive mismatch.
再連接條件~Reconnection conditions|再連接需穩定確認及同步條件。~Reconnection needs stability confirmation and synchronism.|建立離線狀態與計時器圖。~Build offline state and timer diagrams.
保護選擇性~Protection selectivity|局部快速退出可能擴大電網擾動。~Fast local trips can worsen grid-wide disturbances.|比較設備與系統目標衝突。~Compare device and system objectives.
韌體設定~Firmware settings|設定更新需追溯適用測試證據。~Setting updates need traceable test evidence.|保存設定版本與驗證矩陣。~Keep setting revisions and validation matrices.
事件交付~Event handoff|宣稱符合要求須對應完整情境集。~Compliance claims need the full applicable scenario set.|分開已測、未測及不適用項。~Separate tested, untested and inapplicable cases.
''',[(223,'限流與弱網行為共同影響~Current limits and weak-grid behavior affect both','保護課著重動作條件而構網課著重控制狀態~Protection focuses on decisions; grid forming on control states'),(218,'需核對故障量測與外部安全性~Fault measurement and external security matter in both','逆變器限流會改變傳統距離假設~Inverter limiting changes conventional distance assumptions')])
add(225,'啟動能源、復電路徑與動態負載~Starting energy, restoration paths and dynamic loads','資源盤點~Resource inventory|路徑與熱備~Paths and readiness|動態恢復~Dynamic restoration|演練與證據~Rehearsal and evidence','black transition psse',
'假設站用負載 100 kW 持續 2 h，加一次馬達起動交流能量 10 kWh，總交流需求 210 kWh；效率 0.9 需 233.33 kWh 可用直流能量。能量足夠仍不能證明瞬時起動電流能力。~Assume auxiliaries draw 100 kW for 2 h plus one motor start requiring 10 kWh AC: total is 210 kWh AC, or 233.33 kWh available DC at 0.9 efficiency. Energy sufficiency does not prove starting-current capability.', '''
黑啟動定義~Black-start definition|黑啟動資源需在無外部交流供電時建立電源。~A black-start resource establishes supply without external AC.|列不能依賴的外部輔助系統。~List unavailable external auxiliaries.
站用電源~Auxiliary supplies|控制、潤滑與冷卻消耗啟動能源。~Control, lubrication and cooling consume startup energy.|逐時間段建立輔助負載表。~Build auxiliary loads by time interval.
可用能源~Available energy|燃料或 SOC 限制復原持續時間。~Fuel or SOC limits restoration duration.|計算保留量及效率敏感度。~Calculate reserves and efficiency sensitivity.
起動路徑~Cranking paths|復電路徑需連到可啟動的資源及關鍵負載。~Restoration paths must reach startable resources and critical loads.|以圖論比較可行路徑。~Compare feasible graph paths.
變壓器勵磁~Transformer magnetization|磁化湧流可能超過小電源能力。~Magnetizing inrush may exceed small-source capability.|比較剩磁與電壓斜升模型。~Compare remanence and voltage-ramp models.
線路充電~Line charging|輕載長線的容性無功可能升高電壓。~Lightly loaded long lines can raise voltage through charging vars.|以分布模型檢查末端電壓。~Check receiving voltage with distributed models.
馬達起動~Motor starting|馬達起動同時需要無功及轉動加速能量。~Motor starts need vars and acceleration energy.|比較直接起動與受控模型。~Compare direct and controlled model starts.
負載步階~Load steps|負載加入速度影響頻率最低點。~Load pickup speed affects frequency nadir.|掃描步階幅度及間隔。~Sweep step magnitude and spacing.
電壓頻率平衡~Voltage-frequency balance|有功與無功約束不能互相替代。~Active and reactive constraints are not interchangeable.|分開頻率及電壓餘量。~Separate frequency and voltage margins.
分區同步~Island synchronization|多個復電區域需對齊相角與頻率。~Restored islands need aligned angle and frequency.|計算預期閉合時相位差。~Calculate predicted phase difference at closure.
通訊失效~Communication failure|復原計畫需包含通訊及量測不可用情境。~Restoration plans need missing-communication/measurement cases.|檢查依賴鏈與保守退出條件。~Check dependencies and conservative abort conditions.
演練驗收~Rehearsal acceptance|離線演練需記錄假設及每次狀態轉換。~Offline rehearsals need assumptions and every transition logged.|以可重播事件檔覆核能源與穩定。~Replay event files to audit energy and stability.
''',[(222,'負載及能源平衡是共同核心~Load and energy balance are shared','黑啟動需處理無電壓起點及輔助電源~Black start adds a dead-bus origin and auxiliaries'),(223,'構網控制可提供復電參考~Grid-forming control can provide restoration reference','可構網不代表已驗證所有黑啟動負載~Grid-forming capability does not qualify all black-start loads')])
add(226,'模態、暫態功角與頻率動態~Modes, transient rotor angle and frequency dynamics','模型與初始值~Models and initialization|小擾動~Small disturbances|大擾動~Large disturbances|校驗與邊界~Validation and limits','psse pmu',
'假設線性特徵值 λ=−0.5 s⁻¹ ± j6 rad/s，振盪頻率 6/(2π)=0.955 Hz，阻尼比 ζ=0.5/√(0.5²+6²)=0.0830。此線性模態只適用給定工作點附近。~For λ=−0.5 s⁻¹ ± j6 rad/s, oscillation frequency is 6/(2π)=0.955 Hz and damping ratio ζ=0.5/√(0.5²+6²)=0.0830. This linear mode applies only near the chosen operating point.', '''
潮流初始值~Load-flow initial state|動態模型需從一致的穩態開始。~Dynamic models need a consistent steady initial state.|檢查初始導數及功率殘差。~Check initial derivatives and power residuals.
模型階數~Model order|省略勵磁或負載動態會改變模態。~Omitting excitation or load dynamics changes modes.|比較逐項加入的特徵值。~Compare eigenvalues as models are added.
參數基準~Parameter bases|慣量及阻抗需換到一致系統基準。~Inertia and impedance need consistent system bases.|用實際能量與歐姆值核對。~Cross-check physical energy and ohms.
線性化~Linearization|雅可比只描述工作點附近擾動。~A Jacobian describes perturbations near one operating point.|比較不同擾動幅度的誤差。~Compare error across perturbation magnitudes.
阻尼比~Damping ratio|負實部代表衰減但不保證足夠阻尼。~Negative real parts imply decay, not adequate damping.|同時報頻率及阻尼比。~Report both frequency and damping ratio.
參與因子~Participation factors|模態形狀與參與因子有不同含義。~Mode shapes and participation factors mean different things.|分別檢查右與左特徵向量。~Inspect right and left eigenvectors separately.
故障切除~Fault clearing|故障持續時間影響功角加速累積。~Fault duration affects accumulated rotor-angle acceleration.|掃描切除時間找穩定轉折。~Sweep clearing time for stability transitions.
頻率最低點~Frequency nadir|慣量、一次調頻及負載阻尼共同影響最低點。~Inertia, primary response and load damping shape nadir.|分別改動三類參數比較。~Vary the three parameter classes separately.
電壓恢復~Voltage recovery|馬達及換流器動態影响故障後電壓。~Motors and converters affect post-fault voltage recovery.|比較靜態及動態負載模型。~Compare static and dynamic loads.
量測校驗~Measurement validation|同一模型應解釋多個事件而非只擬合一次。~One model should explain multiple events, not one fit.|用未參與估計的事件驗證。~Validate with withheld events.
數值收斂~Numerical convergence|不穩定可能源自步長或求解器選擇。~Apparent instability can reflect timestep or solver choice.|減半步長並比較關鍵軌跡。~Halve timestep and compare key traces.
不確定度~Uncertainty|單一參數組不能涵蓋所有電網狀態。~One parameter set cannot cover all grid conditions.|對負載、拓撲及控制做情境包絡。~Envelope load, topology and control scenarios.
''',[(217,'相量量測可觀察低頻振盪~Phasors can observe low-frequency oscillations','觀測模態不等於已知全部狀態~Observing modes does not reveal all states'),(223,'換流器控制改變動態模型~Converter controls change dynamic models','構網限流需要非線性模型另行驗證~Grid-forming limits need nonlinear verification')])
add(227,'基線、可調負載與需量反應驗證~Baselines, flexible loads and demand-response verification','資源與基線~Resources and baseline|調度與舒適~Dispatch and comfort|通訊與履約~Communication and delivery|量測與評估~Measurement and evaluation','demand flisr meter',
'假設反事實基線 100 kW，事件平均實測 70 kW、持續 2 h，估计降低能量 60 kWh。若基線可能偏差 ±10 kW，僅此項造成 ±20 kWh 範圍；不等於直接量得節能量。~Assume a counterfactual baseline 100 kW and measured event mean 70 kW for 2 h: estimated reduction is 60 kWh. Baseline error ±10 kW alone gives ±20 kWh; savings are not directly measured.', '''
資源分類~Resource classes|可移時負載與可永久削減負載不同。~Shiftable and permanently reducible loads differ.|以能量守恆分類負載行為。~Classify behavior using energy balance.
反事實基線~Counterfactual baseline|事件未發生的用電量無法直接觀測。~No-event consumption is not directly observable.|比較多種相似日基線。~Compare several matched-day baselines.
氣象校正~Weather adjustment|溫度與日型變化會造成基線偏差。~Temperature and day type can bias baselines.|用留出日檢驗校正誤差。~Test adjustment error on withheld days.
舒適限制~Comfort constraints|空調調節受室溫與設備循環限制。~HVAC flexibility is bounded by temperature and cycling.|把舒適帶加入熱容模型。~Add comfort bands to thermal-capacitance models.
儲能等效~Storage equivalence|熱儲能與電池的可用量有不同邊界。~Thermal storage and batteries have different availability limits.|比較功率、時間及恢復需求。~Compare power, duration and recovery needs.
排程最佳化~Scheduling|同時削峰可能在事件後形成反彈。~Coordinated curtailment may create post-event rebound.|延長模擬至事件後恢复完成。~Extend simulation through full recovery.
聚合多樣性~Aggregation diversity|資源可用性相關時不能直接相加保證量。~Correlated availability prevents naive guaranteed summation.|比較獨立與共因缺席情境。~Compare independent and correlated unavailability.
指令時效~Command freshness|延遲或重播命令不可當新調度。~Delayed or replayed commands must not count as new dispatch.|檢查時間戳及冪等識別碼。~Check timestamps and idempotency identifiers.
退出機制~Opt-out mechanism|用戶退出需即時降低可承諾容量。~User opt-outs reduce committed available capacity.|回放退出與補位資源。~Replay opt-outs and replacement resources.
量測分辨率~Measurement resolution|長時間平均可能隱藏短暫履約缺口。~Long averages can hide brief delivery gaps.|比較不同聚合視窗的結果。~Compare different aggregation windows.
績效歸因~Performance attribution|天氣及自然停機不應全歸因於控制。~Weather and natural outages are not all control effects.|用對照組及不確定度解釋結果。~Use controls and uncertainty to interpret results.
隱私最小化~Data minimization|細粒度用電可能透露個人活動。~Fine-grained usage can reveal personal activity.|只保留履約必要資料與期限。~Retain only necessary delivery data and duration.
''',[(228,'可信電能計量是履約基礎~Trustworthy metering underpins delivery','需量反應還需估計反事實基線~Demand response additionally needs counterfactual baselines'),(222,'皆需時間尺度化的能量排程~Both need energy scheduling across timescales','需求反應通常不負責建立孤島電壓~Demand response usually does not establish island voltage')])
add(228,'同步取樣、功率積分與計量不確定度~Synchronous sampling, power integration and metrology uncertainty','量測前端~Measurement front end|數位估計~Digital estimation|校正與驗證~Calibration and validation|資料與通訊~Data and communication','meter meter1',
'假設正弦 230 V RMS、10 A RMS、功率因數 0.8，P=VI cosφ=1840 W，2 h 電能 3.68 kWh。若電壓、電流各有獨立 0.1% 相對標準不確定度且相位準確，功率約 0.141%（未含其他項）。~For sinusoidal 230 V RMS, 10 A RMS and power factor 0.8, P=1840 W and 2 h energy is 3.68 kWh. Independent 0.1% voltage/current standard uncertainties give about 0.141% power uncertainty with exact phase, excluding other terms.', '''
感測選擇~Sensor selection|分流器與 CT 具有不同隔離及頻響。~Shunts and CTs differ in isolation and frequency response.|比較負載、頻率及相位誤差。~Compare loading, bandwidth and phase error.
抗混疊~Antialiasing|超過 Nyquist 的訊號會折疊成假頻率。~Above-Nyquist signals alias into false frequencies.|以已知高頻模型檢查混疊。~Check aliasing using known high-frequency models.
同步通道~Synchronous channels|電壓電流時間偏移會產生功率誤差。~V/I timing skew creates power error.|掃描取樣延遲及功率因數。~Sweep sample delay and power factor.
RMS 計算~RMS calculation|RMS 是平方平均根而非平均絕對值。~RMS is root mean square, not mean absolute value.|比較正弦與尖峰電流。~Compare sine and pulsed current.
有功積分~Active-power integration|瞬時乘積平均包含諧波有功。~Mean instantaneous products include harmonic active power.|比對時域與頻域功率。~Compare time- and frequency-domain power.
電能累加~Energy accumulation|能量累加需正確時間尺度及溢位處理。~Energy accumulation needs correct timebase and overflow handling.|用長時序及中斷恢復測試。~Test long traces and interrupted recovery.
增益校正~Gain calibration|單點校正不能保證整個動態範圍。~One calibration point cannot prove the full range.|比較低、中、高電流殘差。~Compare low, medium and high-current residuals.
相位校正~Phase calibration|低功率因數時小相位誤差影響較大。~Small phase errors matter more at low power factor.|繪製誤差對相位的敏感度。~Plot error sensitivity to phase.
溫漂預算~Thermal drift budget|電阻與參考源漂移可共同改變讀值。~Resistor and reference drift jointly alter readings.|建立元件溫漂不確定度表。~Build a component drift uncertainty table.
雙向計量~Bidirectional metering|輸入與輸出符號需同通訊定義一致。~Import/export signs must match communication semantics.|以反向功率模型核對登錄。~Check registers with reverse-power models.
時間與費率~Time and tariffs|計費區間需處理時區及時鐘校正。~Billing intervals need timezone and clock-correction handling.|測試跨日及重複時間戳。~Test day boundaries and duplicate timestamps.
資料完整性~Data integrity|遺失資料不能無標記地填成零。~Missing data must not silently become zero.|保留缺測、估算及實測旗標。~Retain missing, estimated and measured flags.
''',[(217,'兩者需要相位及同步量測~Both need phase and synchronized measurement','電表重視累積電能，PMU 重視共同時間相量~Meters emphasize energy; PMUs emphasize synchronized phasors'),(227,'需量反應使用計量資料驗證~Demand response uses metrology for verification','計量準確不能消除基線估計偏差~Accurate metering does not remove baseline bias')])
add(229,'諧波頻譜、共振及主動補償容量~Harmonic spectra, resonance and active compensation capacity','量測與指標~Measurement and metrics|被動與主動~Passive and active|控制與容量~Control and capacity|驗證與退化~Verification and degradation','harmonic meter facts',
'假設基頻電流 100 A RMS，5、7 次各 10 A 及 5 A，THD=√(10²+5²)/100=11.18%；總 RMS=√10125≈100.62 A。僅兩次諧波，不代表電壓 THD。~Assume fundamental 100 A RMS with fifth/seventh harmonics 10 and 5 A. THD=√(10²+5²)/100=11.18%; total RMS=√10125≈100.62 A. Only two harmonics are included, not voltage THD.', '''
THD 與 TDD~THD versus TDD|不同分母會使失真指標意義不同。~Different denominators change distortion-metric meaning.|在低負載與高負載重算兩指標。~Recalculate both metrics at low/high load.
電壓與電流~Voltage and current|電流諧波透過電網阻抗產生電壓失真。~Current harmonics produce voltage distortion through grid impedance.|逐頻率計算 Vh=ZhIh。~Calculate Vh=ZhIh by frequency.
取樣窗口~Sampling window|非整週期窗口可能造成頻譜洩漏。~Noninteger-cycle windows can cause spectral leakage.|比較同步與非同步窗口。~Compare synchronized and unsynchronized windows.
被動濾波~Passive filtering|被動支路以頻率相依阻抗分流。~Passive branches divert current through frequency-dependent impedance.|畫頻率掃描及元件容差。~Plot scans with component tolerances.
主動注入~Active injection|主動濾波以反向諧波電流減少源端失真。~Active filters reduce source distortion with opposing harmonics.|比較負載、補償及源電流總和。~Compare load, compensation and source-current sums.
中性線諧波~Neutral harmonics|三次倍數零序電流可在中性線相加。~Triplen zero-sequence currents can add in neutral conductors.|以三相瞬時波形相加驗證。~Verify by summing instantaneous phase waveforms.
感測位置~Sensor placement|CT 位置決定閉環補償看到的電流。~CT location determines the current seen by feedback.|比較源側與負載側拓撲。~Compare source- and load-side topologies.
延遲補償~Delay compensation|延遲讓高次諧波相位誤差更大。~Delay produces larger phase errors at higher harmonics.|計算每次諧波相位滯後。~Calculate lag at each harmonic.
補償容量~Compensation rating|無功、諧波及不平衡共享電流容量。~Vars, harmonics and unbalance share current capacity.|建立 RMS 容量分配預算。~Build an RMS capacity-allocation budget.
網路共振~Network resonance|補償後網路阻抗仍可能放大未補償頻率。~Post-compensation impedance may amplify remaining frequencies.|比較補償前後阻抗與頻譜。~Compare impedance and spectra before/after compensation.
熱效應~Thermal effects|降低 THD 不必然按同比例降低所有損失。~Lower THD need not proportionally reduce every loss.|使用頻率相關電阻計算熱量。~Calculate heating using frequency-dependent resistance.
驗收範圍~Acceptance scope|單一負載點不能證明全運行範圍改善。~One load point cannot prove all-range improvement.|掃描負載與設備退出工況。~Sweep loads and device-outage cases.
''',[(214,'濾波與共振分析共通~Filtering and resonance analysis transfer','SVC 兼具電納控制，主動濾波著重電流波形~SVC controls susceptance; active filtering targets waveforms'),(204,'諧波直接影響變壓器損耗~Harmonics affect transformer losses','變壓器降額仍需獨立熱證據~Transformer derating still needs thermal evidence')])
add(230,'拓撲、狀態估計與模型版本一致性~Topology, state estimation and model revision consistency','資產與拓撲~Assets and topology|狀態與不確定度~State and uncertainty|模擬與同步~Simulation and synchronization|治理與驗證~Governance and validation','twin sincal psse',
'兩個獨立電壓估計 1.00±0.01 pu 與 1.04±0.02 pu（標準不確定度），逆變異數加權平均為 (10000×1.00+2500×1.04)/12500=1.008 pu，標準不確定度 1/√12500≈0.00894 pu；共同偏差不適用此簡式。~Independent estimates 1.00±0.01 pu and 1.04±0.02 pu give inverse-variance mean 1.008 pu and standard uncertainty 1/√12500≈0.00894 pu. Common bias invalidates this simple uncertainty result.', '''
資產識別~Asset identity|同一設備需跨 GIS、SCADA 和模型一致識別。~One asset needs consistent GIS, SCADA and model identity.|建立不靠名稱猜測的 ID 對照。~Build ID mappings without name guessing.
拓撲版本~Topology revision|開關狀態改變連通及方程結構。~Switch states change connectivity and equation structure.|比較版本差異及孤立節點。~Compare revisions and isolated nodes.
座標與基準~Coordinates and bases|地理座標不等於電氣節點基準。~Geographic coordinates differ from electrical-node references.|分開座標、電壓及容量欄位。~Separate location, voltage and power-base fields.
可觀測性~Observability|量測數量多不保證獨立資訊足夠。~Many measurements do not guarantee independent information.|檢查量測雅可比秩。~Check measurement-Jacobian rank.
加權估計~Weighted estimation|較低不確定度量測通常給較高權重。~Lower-uncertainty measurements normally receive higher weight.|比較等權及逆變異數估計。~Compare equal and inverse-variance weights.
壞資料~Bad data|異常殘差可能是感測錯誤或模型錯配。~Large residuals may reflect sensor errors or model mismatch.|分別測試拓撲及感測假說。~Test topology and sensor hypotheses separately.
資料時效~Data freshness|不同更新速率會形成不一致狀態快照。~Different update rates can create inconsistent snapshots.|以時間窗標記同步程度。~Mark synchronization within time windows.
動態模型~Dynamic models|靜態潮流不能回答所有故障動態問題。~Static flow cannot answer every fault-dynamics question.|依問題選擇 RMS 或 EMT 模型。~Select RMS or EMT models by question.
反事實比較~Counterfactual comparison|假想改造需保留同一基準情境。~Hypothetical modifications need a common baseline.|固定負載及天候比較改造效果。~Hold load and weather fixed for comparisons.
參數更新~Parameter updates|自動校參需避免把異常故障學成正常。~Automatic tuning must not learn faults as normal behavior.|設定可信資料與凍結規則。~Define trusted data and freeze rules.
版本稽核~Revision audit|每個結果需可追溯資料、模型與求解器。~Results need traceable data, model and solver versions.|保存雜湊及可重跑設定。~Save hashes and reproducible configurations.
決策邊界~Decision boundaries|模型預測需附不確定度及適用工況。~Predictions need uncertainty and applicable operating conditions.|在未訓練情境檢查失配。~Inspect mismatch in withheld scenarios.
''',[(217,'同步量測可更新模型狀態~Synchronized measurements can update model state','數位分身還需資產版本與拓撲治理~Digital twins also need asset and topology governance'),(226,'動態分析可成為分身的一部分~Dynamic analysis can form part of a twin','數位分身需持續資料關聯而非一次模擬~A twin needs ongoing data association beyond one simulation')])
add(231,'晶矽電池互連、封裝應力及模組失效~Crystalline-silicon interconnection, package stress and module failures','電池與配組~Cells and binning|互連與封裝~Interconnection and encapsulation|電性與缺陷~Electrical and defects|可靠度交接~Reliability handoff','pv pvcell pvchain',
'假設 60 個相同電池串聯，各 Vmp=0.60 V、Imp=10 A，理想模組 Pmp=360 W；總串聯電阻 0.10 Ω 在 10 A 時損失 10 W。此固定工作點估算忽略互連後最佳功率點移動。~Assume 60 identical series cells, each Vmp=0.60 V and Imp=10 A: ideal Pmp=360 W. Total series resistance 0.10 Ω loses 10 W at 10 A. This fixed-point estimate omits the shifted maximum-power point.', '''
電池架構~Cell architecture|接面與鈍化結構影響復合及接觸損失。~Junction and passivation structure affect recombination and contact loss.|比較不同架構的損失項。~Compare loss terms across architectures.
IV 配組~IV binning|串聯鏈電流受較弱電池制約。~Weaker cells constrain series-string current.|比較平均及分布式電池模型。~Compare mean and distributed cell models.
光譜與溫度~Spectrum and temperature|相同輻照度（W/m²）下光譜與溫度仍影響功率。~Spectrum and temperature affect power at equal irradiance.|固定光譜再比較溫度係數。~Hold spectrum fixed when comparing thermal coefficients.
焊帶電阻~Ribbon resistance|互連截面和路徑長度決定部分串阻。~Interconnect area and length determine part of series resistance.|計算 I²R 並區分接點項。~Calculate I²R and separate contact terms.
焊接應力~Interconnect stress|矽與金屬膨脹差造成循環剪切。~Silicon/metal expansion mismatch causes cyclic shear.|畫冷卻及熱循環應變差。~Plot cooling and cyclic strain mismatch.
層壓氣泡~Lamination voids|空隙可能削弱絕緣、光學及黏著。~Voids can weaken insulation, optics and adhesion.|配對影像位置與電性異常。~Pair image locations with electrical anomalies.
旁路二極體~Bypass diodes|遮蔭下旁路可限制局部反向負載。~Bypass paths limit local reverse stress under shading.|比較不同遮蔭位置的 IV。~Compare IV curves at different shadow locations.
電致發光~Electroluminescence|EL 暗區可能來自裂紋或接觸問題。~Dark EL regions may reflect cracks or contacts.|對照 IV、EL 及機械載荷歷史。~Compare IV, EL and load history.
熱點判讀~Hot-spot interpretation|熱點需聯合電流路徑及照射條件解釋。~Hot spots need current-path and illumination context.|用匹配輻照度（W/m²）比較熱圖。~Compare thermal maps at matched irradiance.
濕熱與滲透~Damp heat and ingress|水汽進入速率與邊封及材料相容性相關。~Moisture ingress depends on edge seal and compatibility.|比較邊緣與中心缺陷演化。~Compare edge and center defect evolution.
機械負載~Mechanical loading|載荷造成的裂紋不一定立即電性失效。~Load-induced cracks may not immediately fail electrically.|比較載荷前後及熱循環後證據。~Compare before load, after load and after cycling.
額定及追溯~Rating and traceability|功率標示需對應量測條件及校正。~Power labels need measurement conditions and calibration.|保留電池批次至模組的追溯鏈。~Retain cell-to-module lot traceability.
''',[(232,'模組皆需封裝及環境可靠度~Both modules need packaging and environmental reliability','薄膜以單片整合互連而非離散矽電池焊帶~Thin films use monolithic interconnection rather than discrete-cell ribbons'),(233,'模組 IV 是逆變器的輸入~Module IV is the inverter input','模組額定功率不等於逆變後年發電量~Module rating is not post-inverter annual yield')])
add(232,'薄膜吸收層、單片互連與長期穩定~Thin-film absorbers, monolithic interconnects and durability','材料與基板~Materials and substrate|薄膜與互連~Films and interconnects|電性與封裝~Electrical and packaging|均勻性與可靠度~Uniformity and reliability','film pv pvcell',
'假設吸收係數 α=10⁶ m⁻¹、厚度 d=2 μm，理想無反射單程吸收 1−exp(−αd)=86.47%；d=3 μm 時為 95.02%。未包含載子收集及前後電極損失，因此不是效率。~Assume α=10⁶ m⁻¹ and d=2 μm: ideal reflection-free single-pass absorption 1−exp(−αd)=86.47%; at 3 μm it is 95.02%. Collection and electrode losses are omitted, so this is not efficiency.', '''
材料選擇~Material selection|CdTe、CIGS 與非晶矽不能共用所有參數。~CdTe, CIGS and amorphous Si cannot share all parameters.|列能隙、吸收與穩定差異。~List bandgap, absorption and stability differences.
基板平整~Substrate flatness|基板缺陷可延伸成薄膜局部短路。~Substrate defects can become local film shunts.|比較缺陷座標與電性地圖。~Compare defect coordinates with electrical maps.
透明電極~Transparent electrode|導電率與透光率形成設计權衡。~Conductivity and transmission create a design trade-off.|比較片電阻與光譜透射。~Compare sheet resistance and spectral transmission.
吸收厚度~Absorber thickness|吸收增加不保證載子可被收集。~More absorption does not guarantee carrier collection.|比較吸收長度與收集長度。~Compare absorption and collection lengths.
接面界面~Junction interface|界面缺陷可提高復合而壓低開路電壓。~Interface defects can increase recombination and lower Voc.|比較暗態與照光 IV。~Compare dark and illuminated IV.
背接觸~Back contact|接觸障壁可能使 IV 高電壓端彎折。~Contact barriers can cause high-voltage IV rollover.|比較溫度相依 IV 特徵。~Compare temperature-dependent IV features.
P1 分隔~P1 isolation|前電極分隔需避免殘留導電橋。~Front-electrode isolation must avoid conductive bridges.|用跨溝電阻及顯微形貌交查。~Cross-check trench resistance and morphology.
P2 互連~P2 interconnect|中間開口需形成低阻串聯接觸。~Intermediate openings need low-resistance series contact.|將接觸阻值與有效接触寬度配對。~Pair contact resistance with effective width.
P3 隔離~P3 separation|最後隔離同時决定死區及短路風險。~Final isolation affects dead area and shunt risk.|比較幾何利用率與漏電。~Compare geometric utilization and leakage.
封邊可靠度~Edge-seal reliability|封邊失效可能從邊緣擴散至有效區。~Edge-seal failure can progress into the active area.|追蹤缺陷隨時間的空間前沿。~Track spatial defect fronts over time.
均勻性地圖~Uniformity maps|面積平均值會掩蓋低效率區。~Area averages hide low-performing regions.|比較厚度、光學及電性同位圖。~Compare registered thickness, optical and electrical maps.
材料回收~Material recovery|材料追溯影響報廢回收與環境管理。~Material traceability affects recycling and environmental management.|建立組成清單和合格回收去向。~Build composition records and qualified recovery routes.
''',[(231,'皆需 IV、熱及封裝驗證~Both require IV, thermal and packaging validation','單片劃線串聯取代矽電池焊帶~Monolithic scribes replace silicon-cell ribbons'),(234,'模組失配可與模組級轉換器耦合~Module mismatch can couple with module-level conversion','電子補償不能修復材料吸收或接面缺陷~Electronics cannot repair absorber or junction defects')])
add(233,'MPPT、直流鏈與三相併網控制~MPPT, DC links and three-phase interconnection control','輸入與拓撲~Inputs and topology|追蹤與轉換~Tracking and conversion|併網與熱~Interconnection and heat|驗證與監測~Verification and monitoring','string inv pv',
'假設太陽能輸入 10 kW、效率 97%，交流輸出 9.7 kW、損失 300 W；若散熱等效 0.10 K/W，平均溫升 30 K。效率及熱阻僅為教學值，未含局部結溫與環境變化。~For assumed 10 kW PV input at 97% efficiency, AC output is 9.7 kW and loss 300 W. At equivalent thermal resistance 0.10 K/W, mean rise is 30 K; junction hot spots and environment variation are omitted.', '''
串列電壓~String voltage|低溫開路電壓可能高於額定工作電壓。~Cold open-circuit voltage may exceed rated operating voltage.|用溫度係數估计電壓包絡。~Estimate voltage envelopes with temperature coefficients.
失配與遮蔭~Mismatch and shading|旁路動作可產生多個局部功率峰。~Bypass action can create multiple local power peaks.|比較均匀與部分遮蔭 P–V。~Compare uniform and shaded P–V curves.
輸入保護~Input protection|反接及接地狀態需納入系統邊界。~Polarity and ground faults belong in system boundaries.|用離線故障樹標出偵測功能。~Mark detection functions in an offline fault tree.
MPPT 擾動~MPPT perturbation|擾動步長在追蹤速度與穩態擺動間取捨。~MPPT step size trades speed against steady oscillation.|比較日照斜坡與靜態追蹤。~Compare irradiance ramps and static tracking.
升壓電感~Boost inductance|伏秒平衡决定理想占空比關係。~Volt-second balance sets ideal duty relationships.|以電感波形核對平均電壓。~Check mean voltage using inductor waveforms.
直流鏈電容~DC-link capacitor|功率波动由電容及控制共同吸收。~Capacitance and controls jointly absorb power ripple.|對照電壓波紋與能量平衡。~Compare voltage ripple with energy balance.
調變飽和~Modulation saturation|直流電壓不足會限制可合成交流電壓。~Low DC voltage limits achievable AC voltage.|比較線性調變區與飽和區。~Compare linear and saturated modulation regions.
併網電流~Grid current|LCL 濾波器需處理共振和控制延遲。~LCL filters require resonance and delay treatment.|比較有無阻尼的頻率響應。~Compare damped and undamped responses.
漏電流~Leakage current|寄生對地電容連結共模電壓及漏電流。~Ground capacitance links common-mode voltage to leakage.|用 i=C dv/dt 解釋波形差異。~Explain waveform changes with i=C dv/dt.
熱降額~Thermal derating|高溫降低可持續功率不等於即時故障。~High temperature can reduce continuous power without immediate failure.|比較效率曲線及冷卻能力。~Compare efficiency curves with cooling capacity.
故障穿越~Ride-through|電壓擾動時有功及無功請求受限流约束。~During voltage events, active/var requests face current limits.|畫限流圓與優先序。~Plot current limits and priorities.
產能監測~Yield monitoring|發電降低可能來自天候、污損或限功率。~Yield decline may reflect weather, soiling or curtailment.|用氣象歸一化與狀態碼歸因。~Attribute using weather normalization and status codes.
''',[(231,'IV 曲線提供 MPPT 工作點~IV curves supply MPPT operating points','逆變器不會消除電池本體損失~Inverters do not remove intrinsic cell loss'),(234,'皆需 MPPT 與併網控制~Both need MPPT and grid control','串列型共用輸入而微型分散到模組~String inputs are shared; microinverters distribute per module')])
add(234,'模組級 MPPT、功率解耦與屋頂熱可靠度~Module-level MPPT, power decoupling and rooftop thermal reliability','模組與輸入~Module and input|轉換與解耦~Conversion and decoupling|控制與可靠度~Control and reliability|系統驗證~System validation','micro inv string',
'假設單相輸出 300 W、50 Hz，直流鏈 Vdc=400 V、C=100 μF；小波紋且無其他解耦時，雙頻電壓波紋峰值約 ΔV=P/(2ωCV)=11.94 V，ω=2π×50。峰對峰約 23.87 V，不是設計規格。~For single-phase 300 W at 50 Hz with Vdc=400 V and C=100 μF, small-ripple double-frequency voltage amplitude is ΔV≈P/(2ωCV)=11.94 V, ω=2π×50; peak-to-peak≈23.87 V without other decoupling. This is not a design specification.', '''
模組級控制~Module-level control|獨立 MPPT 可減少模組間失配耦合。~Independent MPPT reduces intermodule mismatch coupling.|比較同一遮蔭圖的兩種架構。~Compare architectures with identical shading maps.
低壓輸入~Low-voltage input|低輸入電壓下同功率需較高電流。~Low input voltage requires higher current at equal power.|計算輸入銅耗随電壓變化。~Calculate copper-loss changes with voltage.
升壓隔離~Step-up and isolation|變比及漏感同時影響升壓和暫態。~Turns ratio and leakage affect step-up and transients.|比較理想變壓器及漏感模型。~Compare ideal and leakage models.
單相功率脈動~Single-phase pulsation|瞬時交流功率包含兩倍電網頻率成分。~Instantaneous AC power includes twice-line-frequency pulsation.|乘正弦電壓電流並分離直流項。~Multiply sine voltage/current and separate DC terms.
被動解耦~Passive decoupling|電容儲能抑制直流端波紋。~Capacitor energy buffers DC-side ripple.|核對電壓平方與能量變動。~Check squared voltage against energy variation.
主動解耦~Active decoupling|額外控制通道搬移波紋但增加損失。~Extra control paths move ripple but add loss.|比較電容需求和開關損耗。~Compare capacitance needs and switching losses.
追蹤與波紋~Tracking and ripple|雙頻波紋可能干扰 MPPT 估計。~Double-frequency ripple can disturb MPPT estimates.|比較瞬時及濾波後功率判斷。~Compare instantaneous and filtered power decisions.
屋頂熱境~Rooftop thermal environment|背板熱與日照使環境邊界不同於室內。~Backsheet heat and sun differ from indoor ambient boundaries.|以時變溫度推估熱循環。~Estimate cycling with time-varying temperature.
封裝與濕氣~Packaging and humidity|灌封材料需平衡散熱與熱應力。~Potting balances cooling and thermal stress.|比較材料熱阻與膨脹差。~Compare thermal resistance and expansion mismatch.
通信品質~Communication quality|通訊缺測不等於逆變器停止發電。~Missing communication does not prove stopped generation.|分開資料可用率與電力可用率。~Separate data and power availability.
多機互動~Multiple-unit interaction|大量並聯設備需檢查頻率響應與保護協調。~Many parallel devices need response and protection coordination.|比較單機與聚合阻抗。~Compare single and aggregate impedance.
失效可維修~Failure serviceability|分散故障降低單點影響但增加屋頂維修。~Distributed failures reduce impact but add rooftop service needs.|用能源損失及維修時間共同評估。~Assess energy loss and repair time together.
''',[(233,'逆變與 MPPT 物理一致~Inversion and MPPT physics transfer','單相雙頻脈動及分散散熱條件不同~Single-phase ripple and distributed cooling differ'),(232,'可針對模組 IV 個別追蹤~Individual module IV curves can be tracked','材料與封裝劣化仍需獨立處理~Material and encapsulation degradation remain separate')])
add(235,'太陽方位、雙軸運動學與風載退避~Sun position, dual-axis kinematics and wind stow','座標與感測~Coordinates and sensing|機構與受力~Mechanics and loading|追蹤控制~Tracking control|收益與可靠度~Yield and reliability','tracker pvchain',
'平面接收器僅考慮直射光的余弦因子，偏角 20° 得 cos20°≈0.9397，即直射分量少約 6.03%。若 500 W/m² 入射、面積 2 m²，理想接收 939.69 W；不含散射、溫度或發電效率。~For direct light only, a flat receiver at 20° error has cos20°≈0.9397, a 6.03% direct-component reduction. At 500 W/m² over 2 m², ideal received power is 939.69 W, excluding diffuse light, temperature and conversion.', '''
太陽座標~Solar coordinates|方位角與高度角需明確方位及時間慣例。~Azimuth and elevation need direction and time conventions.|核對正午、東西與時區案例。~Check noon, east/west and timezone cases.
平面法向~Panel normal|入射角由太陽向量與面板法向內積決定。~Incidence follows the dot product of sun and panel normals.|比較向量法與單軸角度近似。~Compare vector and single-axis approximations.
感測校正~Sensor calibration|感測器零位不等於面板機械零位。~Sensor zero need not equal mechanical panel zero.|建立感測到機構的旋轉變換。~Build the sensor-to-mechanism rotation.
雙軸機構~Dual-axis mechanism|軸順序影響旋轉組合及奇異位置。~Axis order affects rotations and singular positions.|比較兩種旋轉矩陣順序。~Compare rotation-matrix orders.
致動器扭矩~Actuator torque|重心偏移與風壓共同決定扭矩。~Mass offset and wind pressure jointly set torque.|分别計算靜重與風載力矩。~Calculate gravity and wind moments separately.
齒隙與柔性~Backlash and flexibility|齒隙造成方向相關定位誤差。~Backlash causes direction-dependent positioning error.|比較正反向到達同角度的偏差。~Compare approaching one angle from both directions.
開環天文追蹤~Ephemeris tracking|天文算法依位置與時間而非即時光強。~Ephemeris control uses location/time, not instantaneous brightness.|注入時鐘偏差觀察指向誤差。~Inject clock errors and inspect pointing.
閉環修正~Closed-loop correction|雲影會使光感測短時失去可靠方向。~Cloud shadows can temporarily corrupt optical direction cues.|以品質旗標切換感測權重。~Change sensor weighting using quality flags.
風載退避~Wind stow|退避角需依結構風洞或正式工程證據。~Stow angles need wind-tunnel or qualified structural evidence.|用假想載荷比較而不設定現場門檻。~Compare hypothetical loads without field thresholds.
遮蔭與間距~Shading and spacing|追蹤最佳入射角可能增加陣列互遮。~Best incidence can increase mutual array shading.|比較單面板及全陣列收益。~Compare single-panel and whole-array yield.
寄生耗能~Parasitic energy|驅動耗能及維護需从新增發電中扣除。~Drive energy and maintenance offset added generation.|計算淨能量而非只報光學增益。~Calculate net energy, not only optical gain.
失效回復~Failure recovery|停電及限位失效需有已驗證安全狀態。~Power and limit failures need validated safe states.|在離線狀態圖檢查恢復轉移。~Check recovery transitions in offline state diagrams.
''',[(231,'模組效能受入射與溫度影響~Module performance depends on incidence and temperature','機械追蹤不能改善電池内部效率~Mechanical tracking cannot improve intrinsic cell efficiency'),(233,'兩者都影响整體太陽能產出~Both affect overall solar yield','追蹤控制移動機構，MPPT 改變電氣工作點~Tracking moves structures; MPPT moves electrical operating points')])
source('place-voith','Voith 海登海姆據點','Voith Heidenheim location','Voith','https://www.voith.com/corp-en/about-us/markets-locations/germany/heidenheim.html')
source('place-sel','SEL 官方總部地址','SEL corporate address','Schweitzer Engineering Laboratories','https://selinc.com/company/contact/')
source('place-ti','TI 官方總部地址','TI corporate address','Texas Instruments','https://education.ti.com/en/customer-support/knowledge-base/all-other-products/general-information/10626')
source('place-nlr','NLR 實驗室地址','NLR laboratory addresses','National Laboratory of the Rockies','https://www.nlr.gov/about/phone')
source('place-hitachi','Hitachi Energy 官方總部','Hitachi Energy headquarters','Hitachi Energy','https://www.hitachienergy.com/in/en/company/company-profile/country-and-regional-information/group-headquarters')
source('place-nexans','Nexans 官方地址','Nexans official address','Nexans','https://www.nexans.fr/fr/misc/legal_notice.html')
source('place-film','First Solar 官方地址','First Solar official address','First Solar','https://www.firstsolar.com/en/Policies/Imprint')
source('place-erfurt','埃爾福特發電機廠歷史','Erfurt generator works history','Siemens Energy','https://www.siemens-energy.com/de/de/home/press-releases/strom-fuer-80-millionen-menschen-das-generatorenwerk-erfurt-wird-75-jahre-alt.html')
source('place-siemens','Siemens AG 慕尼黑總部','Siemens AG Munich headquarters','Siemens','https://www.siemens.com/en-gb/company/global-locations/germany/munich-corporate-headquarters/')
source('place-schneider','Schneider Electric 官方地址','Schneider Electric official address','Schneider Electric','https://www.se.com/ww/en/about-us/legal/legal-information/')
source('place-tracker','Solar MEMS 官方據點','Solar MEMS official location','Solar MEMS','https://solar-mems.com/contact/')
source('longi','晶矽太陽電池模組产品','Crystalline-silicon PV modules','LONGi','https://www.longi.com/us/products/modules/')
source('overhead','架空線導體結構','Overhead conductor structures','Nexans','https://www.nexans.us/en/Product-Datasheets/Utility-Transmission-Distribution/Bare-Overhead-Conductors.html')
D['a231']['src'].append('longi')
D['a209']['src'].append('overhead')

# Public representative institutions/cities, never operational equipment coordinates.
PL={
 'erfurt':('Siemens Energy 發電機製造城市代表點','Siemens Energy generator manufacturing city reference','埃爾福特','Erfurt','德國','Germany',50.9787,11.0328,'Erfurt, Thuringia, Germany','place-erfurt'),
 'voith':('Voith 海登海姆供應鏈據點','Voith Heidenheim supply-chain reference','海登海姆','Heidenheim','德國','Germany',48.676,10.153,'Sankt Pöltener Straße 43, 89522 Heidenheim, Germany','place-voith'),
 'hitachi':('Hitachi Energy 全球總部代表點','Hitachi Energy global-headquarters reference','蘇黎世','Zurich','瑞士','Switzerland',47.411,8.543,'Brown-Boveri Strasse 5, 8050 Zurich, Switzerland','place-hitachi'),
 'nexans':('Nexans 供應鏈總部代表點','Nexans supply-chain headquarters reference','庫爾布瓦','Courbevoie','法國','France',48.896,2.240,'4 Allée de l’Arche, 92400 Courbevoie, France','place-nexans'),
 'sel':('SEL 保護與自動化供應鏈據點','SEL protection and automation reference','普爾曼','Pullman','美國','United States',46.750,-117.171,'2350 NE Hopkins Court, Pullman, WA 99163, USA','place-sel'),
 'nlr':('NLR 能源系統研究據點','NLR energy-systems research reference','戈爾登','Golden','美國','United States',39.741,-105.171,'15013 Denver West Parkway, Golden, CO 80401, USA','place-nlr'),
 'ti':('Texas Instruments 電子供應鏈總部','Texas Instruments electronics supply-chain headquarters','達拉斯','Dallas','美國','United States',32.911,-96.752,'12500 TI Boulevard, Dallas, TX 75243, USA','place-ti'),
 'film':('First Solar 供應鏈總部代表點','First Solar supply-chain headquarters reference','坦佩','Tempe','美國','United States',33.440,-111.944,'350 West Washington Street, Suite 600, Tempe, AZ 85281, USA','place-film'),
 'siemens':('Siemens AG 電網與開關供應鏈總部','Siemens AG grid and switching supply-chain headquarters','慕尼黑','Munich','德國','Germany',48.145,11.574,'Werner-von-Siemens-Straße 1, 80333 Munich, Germany','place-siemens'),
 'schneider':('Schneider Electric 電力品質供應鏈總部','Schneider Electric power-quality supply-chain headquarters','呂埃馬爾梅松','Rueil-Malmaison','法國','France',48.891,2.179,'35 rue Joseph Monier, 92500 Rueil Malmaison, France','place-schneider'),
 'tracker':('Solar MEMS 光方向感測供應鏈據點','Solar MEMS solar-direction sensing reference','塞維亞地區','Seville area','西班牙','Spain',37.443,-5.879,'C/ Early Ovington 24, nv 01, Aerópolis, 41300 Seville, Spain','place-tracker'),
}
PM={201:'erfurt',202:'voith',203:'hitachi',204:'hitachi',205:'hitachi',206:'erfurt',207:'nexans',208:'nexans',209:'nlr',210:'hitachi',211:'hitachi',212:'hitachi',213:'hitachi',214:'hitachi',215:'erfurt',216:'hitachi',217:'sel',218:'sel',219:'sel',220:'sel',221:'sel',222:'nlr',223:'nlr',224:'hitachi',225:'nlr',226:'nlr',227:'nlr',228:'ti',229:'ti',230:'sel',231:'nlr',232:'film',233:'ti',234:'ti',235:'nlr'}
PM.update({206:'siemens',226:'siemens',229:'schneider',230:'siemens',235:'tracker'})
# Context is deliberately identified as context, not invented invention dates.
CONTEXT={
 'gen':('從高速同步機到模組化冷卻','From high-speed machines to modular cooling','官方發電機頁將汽輪機介面、勵磁及冷卻列為產品整合議題。','The generator page treats turbine interfaces, excitation and cooling as integration topics.'),
 'hydro':('水力機組的尺度與轉速','Hydropower scale and speed','Voith 說明水平、垂直、定速及變速發電機路線。','Voith describes horizontal, vertical, fixed- and variable-speed generator routes.'),
 'transformer':('電力轉換設備家族','A family of power conversion equipment','官方產品分開列出變壓器及其絕緣組件。','The product portfolio separates transformers and insulation components.'),
 'dry':('從液體散熱轉向固體絕緣','From liquid cooling to solid insulation','乾式產品資料展示固體絕緣的配電應用。','Dry-type product information illustrates solid-insulation distribution applications.'),
 'gis':('開關與外部絕緣整合','Switching and external-insulation integration','官方高壓開關目錄包含氣體絕緣及替代介質設備。','The official switchgear portfolio includes gas-insulated and alternative-medium equipment.'),
 'vacuum':('真空開關的設備邊界','Vacuum-switching equipment boundaries','Siemens 公開真空開關產品家族及應用範圍。','Siemens publishes vacuum-switching product families and application scope.'),
 'cable':('從電纜到全路徑工程','From cables to route-wide engineering','Nexans 將電纜、路由工程及海事安裝列為相連服務。','Nexans connects cables, route engineering and marine installation in its services.'),
 'line':('天候進入輸電容量估計','Weather enters line-rating estimates','DOE 介紹動態線路容量如何利用天候及運行資料。','DOE explains dynamic line ratings using weather and operating data.'),
 'arrester':('過電壓保護的元件層','The component layer of surge protection','官方避雷器資料涵蓋交流與直流設備保護。','Official arrester information covers AC and DC equipment protection.'),
 'hvdc':('跨網路直流互連','DC interconnection between networks','官方 HVDC 資料區分 VSC 與 LCC 技術路線。','Official HVDC information distinguishes VSC and LCC routes.'),
 'facts':('既有網路的可控補償','Controllable compensation for existing grids','FACTS 目錄同時介紹並聯補償及其他電網支援方案。','The FACTS portfolio presents shunt compensation and other grid-support approaches.'),
 'svc':('電納調節的技術路線','The susceptance-control route','官方 SVC 資料將可調無功連結到母線電壓調節。','Official SVC material links variable vars to bus-voltage regulation.'),
 'cond':('旋轉設備支援現代電網','Rotating equipment supporting modern grids','官方調相機資料分別說明無功、短路支援及慣量。','Official condenser material distinguishes vars, fault support and inertia.'),
 'pmu':('跨站量測的共同時基','A shared clock for multisite measurements','SEL 將同步相量連結到廣域監測與事件分析。','SEL connects synchrophasors to wide-area monitoring and event analysis.'),
 'distance':('保護與數位量測交會','Protection meets digital measurements','SEL 距離保護產品頁同時列出量測、通訊與程序匯流排選項。','The SEL distance-relay page includes measurement, communication and process-bus options.'),
 'relay':('跨端故障辨識','Inter-end fault discrimination','SEL 線路差動頁呈現差動與距離功能的協同。','The SEL line-differential page combines differential and distance functions.'),
 'flisr':('從故障清除到供電恢復','From fault clearing to service restoration','SEL 的 FLISR 資料把定位、隔離及健康區復電分開描述。','SEL FLISR material separates location, isolation and restoration of healthy sections.'),
 'transition':('微電網轉換的研究脈絡','Research context for microgrid transitions','研究條目探討構網逆變器的微電網模式轉換。','The research entry investigates microgrid transitions using grid-forming inverters.'),
 'forming':('電壓參考由控制器建立','Controllers establishing voltage references','官方技術資料說明構網功能與換流器電網支援。','Official technology material explains grid-forming functions and converter grid support.'),
 'black':('從逆變器研究到復原驗證','From inverter research to restoration validation','實驗室黑啟動頁列出構網與多微電網復原研究。','The laboratory black-start page lists grid-forming and multi-microgrid restoration research.'),
 'psse':('從穩態潮流到動態分析','From steady flow to dynamic analysis','Siemens 模擬平台涵蓋潮流與動態分析。','Siemens simulation software covers power flow and dynamic analysis.'),
 'demand':('需求端成為可調資源','Demand becomes a flexible resource','DOE 研究將需量反應與儲能放在電力系統整合問題中。','DOE studies place demand response and storage within system-integration questions.'),
 'meter':('數位前端與電能計量','Digital front ends and energy metrology','TI 三相參考設計呈現感測、ADC 與運算鏈。','TI three-phase reference designs illustrate sensing, ADC and processing chains.'),
 'harmonic':('主動電流補償','Active-current compensation','Schneider Electric 目錄介紹主動諧波濾波設備。','Schneider Electric catalogs describe active harmonic filtering equipment.'),
 'twin':('跨系統一致的電網模型','Consistent grid models across systems','Siemens 的 AEP 案例說明電網模型及保護模擬的整合。','The Siemens AEP case describes integrated grid modeling and protection simulation.'),
 'pv':('從離散電池到戶外模組','From discrete cells to outdoor modules','DOE 將晶矽電池製作與模組組裝分成不同環節。','DOE distinguishes crystalline-cell fabrication from module assembly.'),
 'film':('薄膜的整合製造路徑','An integrated thin-film manufacturing route','First Solar 官方資料描述薄膜模組的一體化製造路線。','First Solar describes an integrated thin-film module manufacturing route.'),
 'string':('從直流模組到電網','From DC modules to the grid','TI 串列型逆變器資源提供轉換及控制的功能分解。','TI string-inverter resources break down conversion and control functions.'),
 'micro':('轉換器分散到模組','Conversion distributed to modules','TI 微型逆變器參考設計包含 MPPT 與並網轉換。','The TI microinverter reference design includes MPPT and grid conversion.'),
 'tracker':('光方向量測與機械追蹤','Optical direction sensing and mechanical tracking','Solar MEMS 產品頁包含工業追蹤用太陽感測器。','Solar MEMS lists industrial sun sensors for tracking.'),
}

def ref(s): return {k:s[k] for k in ['title','titleEn','publisher','url']}
def ids(keys): return [S[k]['id'] for k in keys]
def make_step(cid,d,u,index,offset,previous):
 (zh,en),(mechanism,mechanismEn),(test,testEn)=u
 model=(index%2==0);number=offset+index+1;sid=f'{cid}-v10-{index+1:02d}'
 title=zh+('：模型與設計' if model else '：量測與判讀')
 titleEn=en+(': model and design' if model else ': measurement and diagnosis')
 instruction=(f'先觀看師傅示意，標出「{zh}」的輸入、輸出及量測基準，再在學徒工作台排列對應元件或資料流。{mechanism} 在離線草圖或試算表建立基準與擾動兩種情境，寫出因果預測；用「{test}」規劃如何反駁模型。把未知參數、單位與邊界記錄在學習筆記。' if model else f'先重播本單元模型，讀取兩種假想情境而不接觸真實帶電設備。{test} 比較差異是否符合「{mechanism}」；列出至少兩個競爭原因，指定能區分原因的新增量測。先依專案規格訂接受條件，再納入量測不確定度，將未驗證項保持為未決。')
 instructionEn=(f'Watch the mentor diagram, identify inputs, outputs and references for {en.lower()}, then arrange components or data flows in the apprentice workspace. {mechanismEn} Build baseline and perturbed cases offline and predict causality. Plan a falsification using: {testEn} Record unknown parameters, units and boundaries in your learning notes.' if model else f'Replay the unit model and inspect two hypothetical cases without accessing energized equipment. {testEn} Compare the result against: {mechanismEn} List at least two competing causes and select an additional discriminating measurement. Define acceptance from project requirements before observing results, include uncertainty and retain unverified items as unresolved.')
 check=(f'提交「{zh}」的兩情境模型、單位表及可反駁預測；說明「{test}」如何區分情境。' if model else f'提交「{zh}」的量測比較、誤差來源及放行／保留理由；不能用單一平均值掩蓋最差條件。')
 checkEn=(f'Submit a two-case model, units and a falsifiable prediction for {en.lower()}; explain how the proposed check distinguishes cases.' if model else f'Submit the measurement comparison, error sources and accept/hold rationale for {en.lower()}; do not hide limiting conditions behind one average.')
 correct=mechanism if model else test;correctEn=mechanismEn if model else testEn
 bad1=f'只要名義額定值相同，就可略過「{zh}」的驗證。';bad1En=f'Equal nominal ratings justify skipping {en.lower()} verification.'
 bad2=f'只調整「{zh}」的顯示結果吻合，便可當作獨立量測證據。';bad2En=f'Tuning the displayed {en.lower()} result to match counts as independent measurement evidence.'
 ans=index%3;opts=[bad1,bad2];optsEn=[bad1En,bad2En];opts.insert(ans,correct);optsEn.insert(ans,correctEn)
 ks=[{'id':sid+'-k1','title':'本單元機制','titleEn':'Unit mechanism','text':mechanism,'textEn':mechanismEn,'sourceIds':ids(d['src'])}, {'id':sid+'-k2','title':'可區分原因的證據','titleEn':'Discriminating evidence','text':test+' 必須保留基準、單位及不確定度，未有實測資料時只做假想案例判讀。','textEn':testEn+' Retain references, units and uncertainty; without measured data, interpret hypothetical cases only.','sourceIds':ids(d['src'])}]
 if index in [0,1,10,11,22,23]:ks.append({'id':sid+'-k3','title':'本課量化連結','titleEn':'Course quantitative connection','text':d['example'][0],'textEn':d['example'][1],'sourceIds':ids(d['src']),'authorship':'original-hypothetical-exercise'})
 return {'id':sid,'order':number,'sequence':number,'estimatedMinutes':35,'simulationOnly':True,'sourceIds':ids(d['src']),'prerequisiteIds':[previous] if previous else [],'title':title,'titleEn':titleEn,'objective':f'針對「{zh}」建立可重算、可檢查的工程紀錄。','objectiveEn':f'Produce a reproducible, reviewable engineering record for {en.lower()}.','instruction':instruction,'instructionEn':instructionEn,'observation':test,'observationEn':testEn,'failure':'常見誤判：'+bad1+' 應先核對量測基準、模型邊界及競爭失效原因。','failureEn':'Common mistake: '+bad1En+' Check references, model boundaries and competing failure causes first.','check':check,'checkEn':checkEn,'knowledge':ks,'quiz':{'question':f'審查「{zh}」時，哪個判斷或驗證方法成立？','questionEn':f'Which claim or check is justified for {en.lower()}?','options':opts,'optionsEn':optsEn,'answer':ans,'explanation':mechanism+' '+test,'explanationEn':mechanismEn+' '+testEn}}

def build():
 courses=[];places=[];related=[]
 assert set(D)=={f'a{i}' for i in range(201,236)}
 for cid,d in D.items():
  n=int(cid[1:]);c=copy.deepcopy(OLD.get(cid,CAT[cid]));original=copy.deepcopy(c.get('stages',[]));oldsteps=[x for stage in original for x in stage['steps']];offset=len(oldsteps);prev=oldsteps[-1]['id'] if oldsteps else None
  newstages=[]
  for si,(st,ste) in enumerate(d['stages']):
   steps=[]
   for local in range(6):
    index=si*6+local;step=make_step(cid,d,d['units'][index//2],index,offset,prev);steps.append(step);prev=step['id']
   newstages.append({'id':f'{cid}-v10-stage{si+1:02d}','order':len(original)+si+1,'title':st,'titleEn':ste,'description':f'以三個技術單元完成「{st}」的模型及判讀，共六項獨立保存的作業。','descriptionEn':f'Three technical units develop {ste.lower()} through six separately saved modeling and interpretation tasks.','steps':steps})
  c.update({'kind':'course','status':'guided','contentStatus':'reviewable-educational-curriculum','depth':4,'stepCount':offset+24,'estimatedMinutes':sum(x.get('estimatedMinutes',35) for x in oldsteps)+840,'simulationOnly':True,'languageCoverage':['zh-TW','en'],'stages':original+newstages,'sourceIds':list(dict.fromkeys(c.get('sourceIds',[])+ids(d['src']))),'summary':f'以{d["focus"][0]}串連 12 個技術單元；新增 24 步，包含原理、假想算例、量測設計、失效辨識與驗收證據。'+(' 原有步驟完整保留。' if offset else ''),'summaryEn':f'Twelve technical units connect {d["focus"][1].lower()} through 24 new tasks with principles, hypothetical calculations, measurement design, failure discrimination and acceptance evidence.'+(' Existing tasks are preserved.' if offset else ''),'scope':'公開原理的離線工程教育與報告判讀。數值為自行設定的教學假設，非產品保證、現場整定、製造配方或帶電操作程序；高壓、旋轉與大型設備實務由合格團隊依正式規格驗證。完成課程不是專業執照。','scopeEn':'Offline engineering education and report interpretation from public principles. Inputs are independently chosen teaching assumptions, not product guarantees, field settings, recipes or live-work procedures. Qualified teams validate high-voltage, rotating and large equipment under formal requirements. Course completion is not professional licensure.','workedExample':{'title':'含假設的可重算例','titleEn':'Reproducible assumed case','text':d['example'][0],'textEn':d['example'][1],'assumptions':'算例內列出的參數及理想化條件；更改波形、材料、溫度、拓撲或模型邊界後須重算。','assumptionsEn':'Use the stated parameters and idealizations; recalculate after changing waveforms, materials, temperature, topology or boundaries.','sourceScope':'作者原創的假想數值題；官方資料支援領域脈絡，並非這組數字的實測來源。','sourceScopeEn':'Original hypothetical numerical exercise; official sources support context, not measurements of these inputs.'}})
  if offset:c['enrichmentVersion']=10
  else:c['curriculumVersion']=10
  c['diagram']={'type':'power','labels':[x[0] for x in d['stages']],'labelsEn':[x[1] for x in d['stages']],'original':True,'notToScale':True}
  vendors=[];seen=set()
  for k in d['src']:
   s=S[k];pub=s['publisher']
   if pub in ['U.S. Department of Energy','National Laboratory of the Rockies'] or pub in seen:continue
   seen.add(pub);vendors.append({'name':pub,'nameEn':pub,'url':s['url'],'role':s['title']+'：可用來比較本課的設備／元件／設計工具角色；不代表本網站推薦或廠商授課。','roleEn':s['titleEn']+': compare the equipment, component or design-tool role in this course; no endorsement or vendor teaching is implied.','sourceIds':[s['id']]})
  # Pure research-source courses retain a relevant commercial design-tool reference.
  if not vendors:
   k='psse' if n<231 else 'film';s=S[k];vendors=[{'name':s['publisher'],'nameEn':s['publisher'],'url':s['url'],'role':s['title']+'供應鏈參考；未主張同一實驗室或製造地點。','roleEn':s['titleEn']+' supply-chain reference; no shared laboratory or manufacturing location is claimed.','sourceIds':[s['id']]}];c['sourceIds'].append(s['id'])
  c['vendorHints']=vendors[:2]
  courses.append(c)
  pl=PL[PM[n]];p={'name':pl[0],'nameEn':pl[1],'city':pl[2],'cityEn':pl[3],'country':pl[4],'countryEn':pl[5],'lat':pl[6],'lng':pl[7],'address':pl[8],'addressEn':pl[8],'mapQuery':pl[8],'coordinateScope':'公開機構／城市的近似代表座標，非設備或可進入的施工位置；總部不表示本課所有製程在該處進行。','coordinateScopeEn':'Approximate public institutional/city coordinates, not equipment or accessible worksites; headquarters does not imply all processes occur there.'}
  ctx=CONTEXT[d['src'][0]];references=[ref(S[k]) for k in d['src']+[pl[9]]]
  place={'courseId':cid,'place':p,'summary':f'{c["title"]}以{d["focus"][0]}連結材料、元件與系統層。地圖顯示可追溯的供應鏈或研究代表點，並非宣稱發明地。','summaryEn':f'{c["titleEn"]} connects materials, components and systems through {d["focus"][1].lower()}. The map marks a traceable supply-chain or research reference, not a claimed invention site.','connection':f'由{d["units"][0][0][0]}走到{d["units"][-1][0][0]}，比較理想模型與實際驗證的交接。','connectionEn':f'Connect {d["units"][0][0][1].lower()} to {d["units"][-1][0][1].lower()}, comparing ideal models with verification handoff.','history':[{'year':'技術脈絡 / Technical context','title':ctx[0],'titleEn':ctx[1],'text':ctx[2],'textEn':ctx[3],'sourceIds':[S[d['src'][0]]['id']]},{'year':'供應鏈與研究 / Ecosystem','title':'公開機構與工程角色','titleEn':'Public institution and engineering role','text':f'{pl[0]}提供本課相關領域的地理參照；地址以官方資料為準。課程引用多個機構的資料，不表示地圖位置同時製造全部元件或具備全部測試能力。','textEn':f'{pl[1]} supplies a geographic reference; its address follows official information. The course cites several institutions, not a claim that this location manufactures every component or performs every test.','sourceIds':[S[pl[9]]['id']]}],'references':references,'sourceIds':ids(d['src']+[pl[9]])}
  places.append(place)
  ritems=[]
  for target,why,diff in d['related']:
   tid=f'a{target}';t=CAT[tid];w,we=why.split('~');df,dfe=diff.split('~')
   ritems.append({'id':tid,'title':t['title'],'titleEn':t['titleEn'],'why':w,'whyEn':we,'transfer':w,'transferEn':we,'difference':df,'differenceEn':dfe,'practice':[f'以「{d["units"][0][0][0]}」為起點，畫出本課與「{t["title"]}」可共用及須重畫的系統邊界。',f'針對「{df}」各選一項能區分兩課的量測。','將本課算例移植到新情境：保留方程依據，重新指定單位、材料或拓撲，並標示無法沿用的數值。'],'practiceEn':[f'Start from {d["units"][0][0][1].lower()} and mark shared/redefined boundaries with {t["titleEn"].lower()}.',f'For the difference "{dfe}", choose discriminating measurements for both courses.','Transfer the worked example: retain justified equations, respecify units, materials or topology and identify values that cannot transfer.'],'referenceUrls':[S[k]['url'] for k in d['src']]})
  related.append({'courseId':cid,'overview':f'從{d["focus"][0]}延伸至相近領域；相似物理不代表同一設備規格或驗收程序。','overviewEn':f'Extend {d["focus"][1].lower()} to neighboring domains; shared physics does not imply identical equipment requirements or acceptance procedures.','related':ritems,'references':[ref(S[k]) for k in d['src']]})
  assert len(ritems)==2 and len(c['stages'])==len(original)+4
  if offset:
   assert c['stages'][:len(original)]==original
   assert c['curriculumVersion']==OLD[cid]['curriculumVersion']
  assert len([x for st in c['stages'] for x in st['steps']])==offset+24
 out={'version':10,'scope':'Original bilingual offline educational engineering cases; no operational live-work instructions. Existing step IDs preserved.','courses':courses,'sources':list(S.values()),'places':places,'related':related}
 (P/'group_a.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
 stats={'courses':len(courses),'newCourses':33,'enrichedCourses':2,'technicalUnits':420,'addedSteps':840,'totalSteps':sum(c['stepCount'] for c in courses),'knowledgeRecords':sum(len(s['knowledge']) for c in courses for st in c['stages'] for s in st['steps']),'sources':len(S),'places':len(places),'relatedComparisons':sum(len(r['related']) for r in related)}
 print(json.dumps(stats,ensure_ascii=False))
 return out
if __name__=='__main__':build()
