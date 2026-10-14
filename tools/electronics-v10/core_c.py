"""Independently authored V10 electronics units. No mutable public dataset inputs."""
COURSES=[]
def course(n,lens,en,stage,formula,example,example_en,bounds,bounds_en,sources,place,related,vendor,units):
    assert len(formula.split('|'))==2,(n,formula)
    rows=[r.split('|') for r in units.strip().splitlines() if r.strip()]
    assert len(rows)==12,(n,len(rows))
    assert all(len(r)==8 for r in rows),(n,[(i,len(r)) for i,r in enumerate(rows) if len(r)!=8])
    COURSES.append(dict(id=f'a{n}',lens=lens,lensEn=en,stages=[s.split('|') for s in stage.split(';')],formula=formula.split('|'),example=[example,example_en],bounds=[bounds,bounds_en],sourceKeys=sources.split(),placeKey=place,relatedIds=related.split(),vendorKey=vendor,units=rows))

course(269,'損耗、熱阻網路與暫態熱容量','losses, thermal networks and transient heat capacity',
'損耗與邊界|Losses and boundaries;熱路與界面|Thermal paths and interfaces;暫態與量測|Transients and measurement;可靠度與決策|Reliability and decisions',
'ΔT=P·Rθ；一階暫態 ΔT(t)=P·Rθ(1−exp(−t/τ))。|ΔT=P·Rθ; first-order transient ΔT(t)=P·Rθ(1−exp(−t/τ)).',
'假設元件損耗 20 W，接面至冷卻液總熱阻 1.8 K/W，冷卻液 35°C，穩態接面估計 71°C；若損耗 30 W，估計 89°C。',
'Assume 20 W device loss, 1.8 K/W total junction-to-coolant resistance and 35°C coolant: steady junction temperature is 71°C; 30 W gives 89°C.',
'線性穩態近似，熱阻依安裝、流量與溫度而變；不把資料表 RθJA 當成任意機箱熱阻。','Linear steady approximation; resistance depends on mounting, flow and temperature. Datasheet RθJA is not arbitrary enclosure resistance.',
 'thermal ti-place','ti','a270 a261','ti', '''
損耗分解|Loss decomposition|導通 I²R 與每次開關能量乘頻率是不同熱源；R 隨溫度改變。|Conduction I²R and switching energy times frequency are distinct heat sources; R changes with temperature.|分別掃描電流和頻率，判別平方電流與頻率相關項。|Sweep current and frequency separately to distinguish quadratic-current and frequency-dependent terms.|只有輸出功率決定晶片損耗。|Output power alone determines die loss.
系統熱邊界|System thermal boundaries|冷卻液入口溫度、空氣回流和機箱表面都可能成為邊界。|Coolant inlet temperature, recirculated air and enclosure surfaces can all form boundaries.|更換環境溫度定義，檢查熱預算是否重複計算散熱器。|Change the ambient definition and check for double-counted heat-sink resistance.|室溫一定等於散熱器入口空氣溫度。|Room temperature always equals heat-sink inlet air temperature.
熱阻參數辨識|Thermal metric identification|RθJC 是指定熱流路的熱阻，ψJT 是特定條件的特性參數，兩者用途不同。|RθJC describes a specified heat-flow path; ψJT is a characterization parameter under specified conditions.|在資料表中標記測試板與冷板條件，選擇與量測位置相符的參數。|Annotate test-board and cold-plate conditions and choose a metric matching the measurement location.|ψJT 可當作任何上蓋散熱器的串聯熱阻。|ψJT is a series resistance for any top-mounted heat sink.
導熱與擴散|Conduction and spreading|一維 R=L/(kA) 忽略從小晶片向大底板的三維擴散。|One-dimensional R=L/(kA) omits three-dimensional spreading from a small die into a larger baseplate.|固定厚度與材料，只改熱源面積，比較一維預測與網格模型。|Hold thickness and material fixed, vary source area and compare one-dimensional and meshed models.|底板面積加倍必然使所有熱阻減半。|Doubling baseplate area necessarily halves every thermal resistance.
界面材料|Interface materials|界面厚度、導熱係數與接觸空隙共同決定溫差；薄不代表接觸完整。|Interface thickness, conductivity and contact voids jointly set temperature drop; thin does not mean complete contact.|以兩種厚度和接觸面積假設作敏感度表，區分材料與接觸限制。|Build a sensitivity table for two thicknesses and contact areas to distinguish bulk and contact limits.|材料標稱導熱係數可完全預測安裝後熱阻。|Nominal conductivity completely predicts installed resistance.
平行散熱路|Parallel heat paths|晶片經基板與上蓋的熱路並聯，不應直接把兩路熱阻相加。|Die-to-board and die-to-lid paths are parallel, not simply series resistances.|用熱流守恆驗證分流之和等於總損耗。|Use heat conservation to verify branch heat flows sum to total loss.|所有接面至環境參數都可直接串聯。|All junction-to-environment metrics can be directly placed in series.
暫態熱阻|Transient impedance|短脈衝溫升取決於 Zθ(t)，不是只靠穩態 Rθ。|Short-pulse rise depends on Zθ(t), not only steady Rθ.|比較相同平均功率、不同占空比的峰值溫度。|Compare peak temperature at equal average power and different duty cycles.|平均功率相同便保證峰值接面溫度相同。|Equal average power guarantees equal peak junction temperature.
熱網路辨識|Thermal-network fitting|多個時間常數可描述不同熱容量；擬合曲線不保證每個 RC 對应真實層。|Multiple time constants describe different capacities; a fitted RC need not correspond to a physical layer.|以未參與擬合的脈衝寬度驗證模型。|Validate with pulse widths excluded from fitting.|任意 Foster RC 節點都代表可量測實體表面。|Every Foster RC node is a measurable physical surface.
接面測溫|Junction thermometry|表面紅外溫度受發射率影響；電性溫敏參數需要校準。|Infrared surface readings depend on emissivity; electrical temperature-sensitive parameters require calibration.|比較貼片熱電偶、紅外與已校準電性讀值的時間響應。|Compare response times of a surface thermocouple, infrared sensing and a calibrated electrical reading.|紅外相機看到的表面就是晶片接面。|The infrared-visible surface is the semiconductor junction.
熱循環疲勞|Thermal cycling fatigue|接合層受溫差幅度和循環次數影響，平均溫度不足以描述疲勞。|Joint fatigue depends on temperature swing and cycle count; mean temperature is insufficient.|整理任務剖面的溫度轉折與停留時間，避免把功率循環等同環境循環。|Tabulate mission-profile reversals and dwell times; distinguish power from environmental cycling.|相同平均溫度的兩個任務必有相同疲勞。|Two missions with equal mean temperature have equal fatigue.
降額與容差|Derating and tolerances|損耗和熱阻的不確定度會使接面溫度範圍擴大。|Uncertainty in loss and thermal resistance widens the junction-temperature range.|以上下界組合重算最熱情境，列出測不到的熱阻。|Recompute the hottest combination of bounds and list unmeasured resistances.|典型值相加就等於最差條件。|Adding typical values gives the worst case.
冷卻失效驗證|Cooling-failure verification|風扇退化與流路堵塞改變邊界；保護需由感測延遲和熱慣性評估。|Fan degradation and blockage change boundaries; protection depends on sensor delay and thermal inertia.|在模擬中中斷冷卻，檢查告警至降額的時間與峰值溫度。|Interrupt cooling in simulation and examine alarm-to-derating delay and peak temperature.|慢速外殼感測必能捕捉每個晶片熱峰。|A slow case sensor necessarily catches every die-temperature peak.
''')

course(270,'共模、差模與阻抗交互作用','common mode, differential mode and impedance interactions',
'噪聲與頻譜|Noise and spectra;濾波拓撲|Filter topology;寄生與穩定|Parasitics and stability;量測與判讀|Measurement and interpretation',
'f₀=1/(2π√LC)；理想二階低通高頻衰減約 40 dB/dec。|f₀=1/(2π√LC); an ideal second-order low-pass asymptote falls about 40 dB/dec.',
'教學 L=10 µH、C=1 µF 得 f₀≈50.3 kHz；僅在理想漸近區，頻率提高十倍多約 40 dB 衰減。',
'Teaching values L=10 µH and C=1 µF give f₀≈50.3 kHz; only in the ideal asymptotic region does a tenfold frequency rise add about 40 dB attenuation.',
'未包含來源與負載阻抗、ESR/ESL 或寄生共振；不得用此算例宣稱符合 EMC。','Excludes source/load impedance, ESR/ESL and parasitic resonances; the example does not establish EMC compliance.',
'emi emi-video ti-place','ti','a269 a297','ti', '''
差模電流|Differential-mode current|去回導線中的等量反向高頻電流產生差模噪聲。|Equal and opposite high-frequency currents in supply and return form differential-mode noise.|對同一波形做和差分解，標記差模分量。|Compute sum and difference of the same current waveforms and identify differential mode.|兩條線同方向的電流是純差模。|Currents flowing in the same direction on both wires are purely differential mode.
共模回路|Common-mode loop|寄生電容把高 dv/dt 節點耦合到機殼，回流可能經地或纜線。|Parasitic capacitance couples high-dv/dt nodes to the chassis, returning through ground or cables.|在示意圖閉合共模回路，改電容後比較 i=C·dv/dt。|Close the common-mode loop on a diagram and compare i=C·dv/dt after changing capacitance.|沒有接地線就沒有共模回流路。|Without a ground wire there is no common-mode return path.
諧波與邊緣|Harmonics and edges|開關頻率設定諧波間距，邊緣速度影響高頻包絡。|Switching frequency sets harmonic spacing while edge speed shapes the high-frequency envelope.|固定頻率只延長上升時間，查看高頻頻譜變化。|Hold frequency fixed and lengthen rise time to inspect high-frequency changes.|只降低開關频率必然消除所有高頻噪聲。|Reducing switching frequency necessarily eliminates all high-frequency noise.
LC 差模濾波|LC differential filtering|電感和並聯電容形成低通，但实际插入損耗依兩端阻抗。|An inductor and shunt capacitor form a low-pass; actual insertion loss depends on terminal impedances.|重算 50 Ω 與低阻電源兩種終端的傳遞函數。|Recompute transfer functions for 50 Ω and low-impedance supply terminations.|50 Ω 測試插損可原封不動用於任何電源。|50 Ω insertion loss applies unchanged to any power supply.
共模扼流圈|Common-mode choke|理想耦合磁芯讓差模磁通抵銷、共模磁通相加，漏感仍影響差模。|An ideal coupled core cancels differential flux and adds common-mode flux; leakage still affects differential mode.|把兩繞組電流方向畫出，辨識飽和與漏感條件。|Draw winding-current directions and identify saturation and leakage conditions.|共模電感的差模阻抗永遠為零。|A common-mode choke always has zero differential impedance.
電容與隔離|Capacitance and isolation|跨隔離電容兼顧高頻回流與漏電；類別和額定不能互換。|Barrier-crossing capacitance trades high-frequency return against leakage; classes and ratings are not interchangeable.|計算假設電容的工頻電流並列出尚需專業認證的條件。|Calculate line-frequency current for an assumed capacitance and list conditions requiring professional certification.|任意高容值电容都適合跨隔離使用。|Any large capacitor is suitable across an isolation barrier.
阻尼設計|Damping|LC 共振可能放大某頻帶；阻尼改變尖峰但增加耗能。|LC resonance can amplify a band; damping alters peaking and dissipates energy.|掃描阻尼電阻，比較共振峰與直流損失。|Sweep damping resistance and compare resonance peak with DC losses.|濾波級數增加必然降低所有頻率的噪聲。|Adding filter stages necessarily reduces noise at every frequency.
輸入穩定性|Input stability|受控變換器在某頻帶呈負增量阻抗，輸入濾波會與控制迴路耦合。|A regulated converter can exhibit negative incremental input impedance over a band and interact with its filter.|比較濾波器輸出阻抗與變換器輸入阻抗的幅相。|Compare magnitude and phase of filter output and converter input impedances.|輸入濾波與變換器控制完全無關。|Input filtering is completely independent of converter control.
寄生旁路|Parasitic bypass|輸入與輸出走線的電容耦合可繞過濾波器。|Capacitive coupling between input and output routing can bypass a filter.|保持零件不變，對照遠離和貼近走線的等效電容模型。|Hold components fixed and compare capacitance models for separated and adjacent routing.|原理圖相同便保證相同高頻濾波結果。|Identical schematics guarantee identical high-frequency filtering.
LISN 與參考面|LISN and reference plane|LISN 提供規定的測試阻抗，量測配置是結果的一部分。|A LISN supplies a defined test impedance; setup is part of the result.|對照既有測試資料的纜線、接地面與負載條件。|Compare cable, ground-plane and load conditions in existing test records.|不同測試佈置的數字可無條件直接比較。|Numbers from different setups are unconditionally comparable.
峰值與準峰值|Peak and quasi-peak|檢波器的時間加權不同；單次峰值不等於準峰值讀值。|Detectors apply different time weighting; one peak is not a quasi-peak reading.|在模擬脈衝列上比較重複率改變而峰值不變的情境。|Compare pulse trains with changed repetition rate but equal peak amplitude.|準峰值永遠等於最大示波器電壓。|Quasi-peak always equals maximum oscilloscope voltage.
證據與餘裕|Evidence and margin|量測不確定度、工作模式與線路變異都影響合規餘裕。|Measurement uncertainty, operating mode and line variation affect compliance margin.|做模式矩陣並標記哪個頻點限制餘裕，保存原始頻譜。|Build a mode matrix, mark margin-limiting frequencies and retain raw spectra.|單一空載頻譜可代表所有產品模式。|One no-load spectrum represents all product modes.
''')

course(271,'微弱訊號、誤差預算與校準','small signals, error budgets and calibration',
'訊號需求|Signal requirements;放大與濾波|Amplification and filtering;轉換與佈局|Conversion and layout;校準與可信度|Calibration and confidence',
'Vout=G·Vdiff+Vref；輸入等效誤差須先換回相同基準才可相加。|Vout=G·Vdiff+Vref; refer errors to a common input basis before combining.',
'假設感測器滿刻度 20 mV、G=100，輸出跨度 2 V；輸入失調 10 µV 對應輸出 1 mV，為滿刻度 0.05%。',
'Assume a 20 mV sensor span and G=100: output span is 2 V; 10 µV input offset becomes 1 mV output error, or 0.05% of span.',
'線性小訊號且未飽和；固定誤差用界限和、獨立隨機誤差才可用均方根。','Linear small-signal operation without saturation; bound systematic errors and use root-sum-square only for independent random errors.',
'precision precision-layout ti-place','ti','a274 a275','ti', '''
訊號與共模|Signal and common mode|差動毫伏訊號可以疊加在較大的共模電壓上。|A millivolt differential signal can sit on a much larger common-mode voltage.|分別列出差模、共模與供應軌，不把輸出範圍當輸入範圍。|List differential, common-mode and supply ranges separately.|輸出未飽和就表示輸入共模一定合法。|Unsaturated output guarantees a valid input common-mode level.
感測器負載|Sensor loading|輸入電流與源阻抗形成附加誤差，兩端阻抗不平衡會轉換共模。|Input current times source impedance adds error; imbalance converts common mode.|交換兩側源阻抗，觀察偏移符號與共模抑制的改變。|Swap source impedances and inspect offset sign and common-mode rejection.|高輸入電阻表示輸入偏置電流完全沒有影響。|High input resistance makes bias current irrelevant.
誤差預算|Error budgeting|失調、增益、参考、非線性和漂移需換算到同一滿刻度。|Offset, gain, reference, nonlinearity and drift need a common full-scale basis.|建立 µV、ppm、%FS 換算表，區分可校準與不可校準項。|Build a µV/ppm/%FS conversion table and separate calibratable terms.|不同基準的 ppm 可以直接相加。|ppm terms with different references can be added directly.
儀表放大器|Instrumentation amplifier|高 CMRR 仍依頻率、增益與源阻抗對稱性而變。|High CMRR still varies with frequency, gain and source-impedance symmetry.|在固定差模下掃描共模頻率，檢查輸出誤差斜率。|Sweep common-mode frequency at fixed differential input and inspect output-error slope.|直流 CMRR 規格保證所有頻率的抑制。|DC CMRR guarantees rejection at every frequency.
噪聲積分|Noise integration|白雜訊密度要經等效噪聲頻寬積分，1/f 噪聲另有低頻貢獻。|White-noise density integrates over equivalent noise bandwidth; 1/f noise adds low-frequency contribution.|將兩種濾波頻寬的 RMS 雜訊比值與平方根比例比較。|Compare RMS-noise ratios for two bandwidths with the square-root law.|nV/√Hz 可直接當成輸出 RMS 電壓。|nV/√Hz is directly an output RMS voltage.
抗混疊濾波|Anti-alias filtering|取樣前的頻帶外訊號可能摺回，取樣後無法分辨其來源。|Out-of-band input can alias and become indistinguishable after sampling.|讓輸入跨越 Nyquist 邊界，列出摺回頻率。|Move an input across Nyquist and tabulate its aliases.|數位低通一定能移除已摺回的干擾。|A digital low-pass always removes already aliased interference.
ADC 驅動穩定|ADC-driver settling|開關電容輸入在取樣窗中抽取電荷，驅動器必須及時建立。|A switched-capacitor input draws charge during acquisition and must settle in time.|比較取樣率和源阻抗改變時的碼值偏移。|Compare code shifts as sample rate and source impedance change.|直流增益正確便保證 ADC 取樣時準確。|Correct DC gain guarantees accurate ADC acquisition.
參考與回流|Reference and return|理想比例量測可抵銷共用激勵與參考的相關變動；未相關雜訊、頻寬差和回流壓降仍留誤差。|Ideal ratiometric conversion cancels correlated excitation/reference changes; uncorrelated noise, bandwidth mismatch and return drops still cause errors.|分開繪製訊號、參考與大電流回路，找共同阻抗。|Draw signal, reference and high-current returns separately and find shared impedance.|所有標成 GND 的位置都具有完全相同電位。|All points labeled GND have exactly the same potential.
佈局與熱電勢|Layout and thermoelectric effects|不對稱溫度梯度可在異種金屬接點產生微伏級偏差。|Asymmetric thermal gradients can create microvolt offsets at dissimilar-metal junctions.|反轉訊號並改變氣流，區分真訊號與熱電勢漂移。|Reverse the signal and vary airflow to distinguish signal from thermoelectric drift.|只有電性元件容差會造成直流偏移。|Only electrical component tolerance causes DC offset.
兩點校準|Two-point calibration|兩點可估算線性增益和失調，不能消除所有非線性。|Two points estimate linear gain and offset but cannot remove all nonlinearity.|用第三個未校準中點檢查殘差。|Use a third, unfitted midpoint to check residual error.|兩點校準能保證整個範圍零誤差。|Two-point calibration guarantees zero error across the range.
溫漂驗證|Temperature-drift validation|校準係數隨溫度改變時，需要跨溫資料與回溫檢查。|Temperature-dependent calibration requires cross-temperature data and return checks.|比較升溫和降溫的殘差，辨識遲滯而非硬套直線。|Compare heating and cooling residuals to detect hysteresis instead of forcing a line.|室溫校準係數適用所有環境溫度。|Room-temperature calibration coefficients apply at every temperature.
量測不確定度|Measurement uncertainty|參考儀器、重複性與校準模型皆限制結論的可信度。|Reference instrument, repeatability and calibration model limit confidence.|寫出原始量、追溯鏈、涵蓋因子和無法判定區間。|Record raw readings, traceability, coverage factor and inconclusive intervals.|顯示更多小數位就提高量測準確度。|More displayed decimals increase accuracy.
''')

course(272,'雜訊匹配、增益與穩定性','noise matching, gain and stability',
'接收機預算|Receiver budgets;匹配與偏壓|Matching and bias;線性與穩定|Linearity and stability;量測與選型|Measurement and selection',
'Ftotal=F₁+(F₂−1)/G₁；F 與 G 必須使用線性值。|Ftotal=F₁+(F₂−1)/G₁; use linear F and G.',
'假設第一級 NF=1 dB、增益 15 dB，第二級 NF=8 dB，Ftotal≈1.427，總 NF≈1.54 dB。',
'Assume first-stage NF=1 dB and gain=15 dB, followed by NF=8 dB: Ftotal≈1.427 and total NF≈1.54 dB.',
'級聯公式以匹配、未壓縮的線性級為假設；輸入濾波損失需另列在第一級前。','Cascade calculation assumes matched, uncompressed linear stages; add input-filter loss ahead of stage one.',
'lna lna-select adi-place','adi','a276 a280','adi', '''
熱雜訊底限|Thermal-noise floor|可用熱雜訊功率為 kTB，頻寬增加會提高整合雜訊。|Available thermal-noise power is kTB; wider bandwidth increases integrated noise.|將頻寬加倍，檢查功率噪聲約增加 3 dB。|Double bandwidth and check for about 3 dB more noise power.|相同溫度下雜訊功率與頻寬無關。|Noise power at fixed temperature is independent of bandwidth.
級聯雜訊|Cascaded noise|前級增益降低後級對輸入等效雜訊的貢獻。|Early gain reduces later stages' input-referred noise contribution.|把衰減器放在 LNA 前後各算一次 NF。|Calculate NF with an attenuator before and after the LNA.|相同衰減量放在哪一級都不影響總 NF。|An attenuator has the same NF effect at every position.
動態範圍|Dynamic range|低雜訊與抗大訊號能力分別限制弱訊號與強阻塞。|Low noise and large-signal handling limit weak signals and strong blockers separately.|用弱訊號加強阻塞的假想輸入檢查兩個預算。|Check separate budgets for a weak signal plus a strong blocker.|最低 NF 元件必然有最佳阻塞容忍。|The lowest-NF device necessarily has the best blocker tolerance.
雜訊匹配|Noise matching|最佳雜訊源阻抗通常不等於最大增益共軛匹配。|The optimum noise source impedance generally differs from maximum-gain conjugate matching.|在同一頻率比較雜訊圈與增益圈可交集區。|Compare feasible intersections of noise and gain circles at one frequency.|最小 S11 必然得到最小 NF。|Minimum S11 necessarily gives minimum NF.
偏壓與功耗|Bias and power|偏壓改變跨導、雜訊、壓縮和熱條件。|Bias changes transconductance, noise, compression and temperature.|在資料表可比條件下整理 NF、增益、電流三軸取捨。|Tabulate NF, gain and current trade-offs under comparable datasheet conditions.|提高偏壓電流總能改善所有指標。|Increasing bias current always improves every metric.
回授與寄生|Feedback and parasitics|反向傳输與接地寄生讓輸出負載影響輸入。|Reverse transmission and ground parasitics let the output load affect the input.|改變負載相位，觀察模型中的輸入反射與增益。|Vary load phase and observe input reflection and gain in the model.|S12 永遠是零，因此輸入輸出完全獨立。|S12 is always zero, making input and output independent.
小訊號穩定|Small-signal stability|穩定判斷須考慮頻率與源負載區域，單一工作點增益不足。|Stability requires frequency and source/load regions, not merely gain at one point.|掃描 S 參數模型並標記潛在不穩定頻帶。|Sweep an S-parameter model and mark potentially unstable bands.|工作頻帶內增益平坦就證明全頻穩定。|Flat in-band gain proves stability at all frequencies.
壓縮|Gain compression|1 dB 壓縮是增益偏離小訊號外推 1 dB，不是輸出下降到 1 dBm。|1 dB compression is a 1 dB departure from extrapolated small-signal gain, not 1 dBm output.|畫出輸入輸出功率與線性外推線的差。|Plot input/output power and departure from the linear extrapolation.|P1dB 代表輸出只能有 1 dBm。|P1dB means output is limited to 1 dBm.
互調|Intermodulation|兩音三階產物可能落入通帶；IP3 是外推交點。|Two-tone third-order products can fall in-band; IP3 is an extrapolated intercept.|確認基波與 IM3 小訊號斜率約為 1 與 3。|Check fundamental and IM3 slopes near 1 and 3 in the small-signal region.|IP3 是可連續輸出的額定功率。|IP3 is a rated continuous output power.
去嵌入|De-embedding|纜線與治具損失會改變量得的 NF 和增益參考面。|Cable and fixture losses alter NF and gain reference planes.|列出校準面到器件面的損耗及溫度。|List loss and temperature between calibration and device planes.|移動參考面不需改變雜訊修正。|Moving the reference plane requires no noise correction.
雜訊量測|Noise measurement|噪聲源 ENR、匹配和儀器本底影響 NF 不確定度。|Noise-source ENR, mismatch and instrument floor affect NF uncertainty.|比較不同平均次數與校準檔，觀察隨機與系統誤差。|Compare averaging counts and calibration files to distinguish random and systematic errors.|只增加平均次數就能消除所有系統誤差。|More averaging removes all systematic errors.
選型放行|Selection and acceptance|元件比較必須使用相同頻率、增益、偏壓與溫度條件。|Device comparisons need equal frequency, gain, bias and temperature conditions.|將不同比較條件標記為不可直接排名。|Flag incomparable conditions rather than assigning a direct ranking.|資料表首頁最低 NF 可直接作跨頻帶排名。|Headline minimum NF directly ranks devices across different bands.
''')

course(273,'相位回授、雜訊整形與鎖定','phase feedback, noise shaping and lock acquisition',
'頻率規劃|Frequency planning;迴路動態|Loop dynamics;雜訊與雜散|Noise and spurs;鎖定與驗證|Lock and validation',
'fout=N·fPFD；相位誤差經迴路濾波控制 VCO。|fout=N·fPFD; phase error controls the VCO through a loop filter.',
'假設 fPFD=25 MHz、N=96，輸出 2.4 GHz；整數 N 改為 97，頻率變為 2.425 GHz。',
'Assume fPFD=25 MHz and N=96: output is 2.4 GHz; N=97 gives 2.425 GHz.',
'整數 N 且鎖定的理想關係；分頻器、VCO 範圍與參考相噪另行限制。','Ideal locked integer-N relation; divider limits, VCO range and reference phase noise impose additional constraints.',
'pll pll-debug adi-place','adi','a274 a280','adi', '''
頻率格點|Frequency grid|整數 N 合成器的頻率步距由相位偵測頻率決定。|Integer-N frequency spacing is set by the phase-detector frequency.|列出相鄰 N 值的可達頻率並找不可達頻點。|List frequencies at adjacent N values and identify unreachable targets.|整數 N 可在固定參考下連續調頻。|Integer-N permits continuous tuning at a fixed reference.
參考分頻|Reference division|參考分頻影響 PFD 頻率、所需 N 和帶內相噪。|Reference division affects PFD frequency, required N and in-band phase noise.|保持輸出相同，比較兩種 R 與 N 組合。|Hold output fixed and compare two R/N combinations.|增加參考分頻永遠改善相噪。|More reference division always improves phase noise.
VCO 調諧|VCO tuning|VCO 增益 Kv 以 Hz/V 或 rad/s/V 表示，單位不可混用。|VCO gain Kv can be in Hz/V or rad/s/V; units are not interchangeable.|將 Hz/V 轉為 rad/s/V 後重算模型。|Convert Hz/V to rad/s/V before recalculating the model.|Hz/V 和 rad/s/V 的數值完全相同。|Hz/V and rad/s/V have identical numeric values.
相位偵測器|Phase detector|PFD 與充電泵把相位差轉為平均電流，但存在非理想死區和不匹配。|PFD and charge pump convert phase error to average current, with dead zone and mismatch nonidealities.|比較正負相位差的電流曲線對稱性。|Compare current-curve symmetry for positive and negative phase errors.|充電泵上拉下拉不匹配不影響鎖定頻譜。|Charge-pump mismatch cannot affect the locked spectrum.
迴路濾波|Loop filter|零極點塑造開迴路幅相，濾波器不是單純平滑器。|Poles and zeros shape open-loop magnitude and phase; the filter is not merely a smoother.|畫出交越處相位餘裕並對照步階超越量。|Plot crossover phase margin and compare step overshoot.|濾波電容越大迴路一定越穩且越快。|Larger filter capacitance always makes the loop both faster and more stable.
鎖定時間|Lock time|頻率跨步後要到指定誤差帶並持續停留才算建立。|After a frequency step, settling means entering and remaining in a specified error band.|分別使用寬窄誤差帶量測同一模擬波形。|Measure the same simulated waveform with wide and narrow tolerance bands.|首次穿越目標頻率就代表完全鎖定。|The first target-frequency crossing means complete lock.
相噪交接|Noise crossover|參考與 VCO 雜訊經不同閉迴路傳遞函數到輸出。|Reference and VCO noise reach output through different closed-loop transfer functions.|掃描迴路頻寬，找交接區的總雜訊變化。|Sweep loop bandwidth and examine total noise around crossover.|PLL 對所有雜訊都是同一個低通。|A PLL applies the same low-pass response to every noise source.
抖動積分|Jitter integration|相噪積分需指明偏移頻率範圍，抖動比較才有意義。|Integrated phase noise needs stated offset-frequency limits for meaningful jitter comparison.|使用相同積分上下限比較两條相噪曲線。|Compare two phase-noise curves with identical integration limits.|不同積分頻帶的抖動可直接排名。|Jitter integrated over different bands can be directly ranked.
分數雜散|Fractional spurs|分數分頻的周期或量化行為可能形成雜散，不能只看平均 N。|Fractional division can create periodic or quantization spurs; average N is insufficient.|比較鄰近分數比的窄頻頻譜與平均頻率。|Compare narrowband spectra and mean frequency for adjacent fractional ratios.|分數 N 平均頻率正確便沒有雜散。|Correct fractional-N mean frequency means no spurs.
電源耦合|Supply coupling|電源紋波可經 VCO 推頻與數位耦合產生旁帶。|Supply ripple can create sidebands through VCO pushing and digital coupling.|改變假想紋波頻率，追蹤旁帶偏移是否跟隨。|Change simulated ripple frequency and check whether sideband offsets follow.|參考乾淨即可保證輸出沒有電源旁帶。|A clean reference guarantees no supply sidebands.
鎖定偵測|Lock detection|數位 lock flag 與實際相位、頻率精度是不同證據。|A digital lock flag is different evidence from phase and frequency accuracy.|同時保存旗標、控制電壓與頻率誤差。|Record lock flag, control voltage and frequency error together.|鎖定旗標足以證明所有相噪規格。|A lock flag proves every phase-noise specification.
可重現頻率切換|Repeatable hopping|初始條件、校準與溫度使重複切頻時間分布變化。|Initial conditions, calibration and temperature affect repeated frequency-hop timing.|報告多次切換分布而非只選最快波形。|Report repeated-hop distributions rather than selecting the fastest trace.|最快一次鎖定時間代表最差情境。|The fastest lock event represents the worst case.
''')

course(274,'取樣、量化、時鐘與高速介面','sampling, quantization, clocks and high-speed interfaces',
'取樣規劃|Sampling plan;類比輸入|Analog input;時鐘與數位|Clock and digital path;動態驗收|Dynamic acceptance',
'SNRjitter=−20log₁₀(2πfin·σt)；理想正弦量化 SNR≈6.02N+1.76 dB。|SNRjitter=−20log₁₀(2πfin·σt); ideal sine-wave quantization SNR≈6.02N+1.76 dB.',
'假設 fin=100 MHz、總 RMS 抖動 100 fs，抖動限制 SNR≈84.0 dB；fin 增至 200 MHz 降至約 78.0 dB。',
'With fin=100 MHz and total RMS jitter of 100 fs, jitter-limited SNR≈84.0 dB; fin=200 MHz reduces it to about 78.0 dB.',
'正弦、小時間誤差、抖動與輸入不相關；此值未包含量化、熱雜訊與失真。','Sinusoidal input, small timing errors and uncorrelated jitter; excludes quantization, thermal noise and distortion.',
'adc adc-test adi-place','adi','a271 a273','adi', '''
Nyquist 區帶|Nyquist zones|不同頻率可在取樣後映射到同一離散頻率。|Different analog frequencies can map to the same sampled frequency.|用 fs=100 MHz 比較 20 和 80 MHz 的混疊位置。|At fs=100 MHz compare aliases of 20 and 80 MHz.|高取樣率 ADC 永遠不需要頻帶規劃。|A high-speed ADC never needs frequency planning.
解析度與範圍|Resolution and range|LSB 由全幅範圍除以 2ᴺ 決定，位數不是準確度。|LSB is full-scale span divided by 2ᴺ; bit count is not accuracy.|把同一電壓雜訊換成不同輸入範圍的 LSB。|Express the same voltage noise in LSBs for different input spans.|增加標称位數必定等比例改善準確度。|More nominal bits always improve accuracy proportionally.
架構與延遲|Architecture and latency|管線、SAR 與時間交錯具有不同延遲和驅動需求。|Pipeline, SAR and time-interleaved architectures differ in latency and drive requirements.|比較資料表的 acquisition、latency 和 throughput。|Compare acquisition, latency and throughput in datasheets.|取樣間隔與資料延遲一定相同。|Sampling interval and data latency are always equal.
輸入驅動|Input drive|全差動驅動器的共模與線性擺幅必须兼容 ADC。|A differential driver's common mode and linear swing must match the ADC.|畫出兩輸入腳的瞬時峰值而非只看差動幅度。|Plot instantaneous peaks at both input pins, not just differential amplitude.|差動幅度合法就能忽略每腳對地電壓。|Valid differential amplitude permits ignoring pin-to-ground voltage.
取樣回踢|Sampling kickback|取樣開關的電荷回踢透過源阻抗造成建立誤差。|Sampling-switch charge kickback causes settling error through source impedance.|掃描 RC 隔離網路與取樣窗，找殘餘誤差。|Sweep the isolating RC network and acquisition window to find residual error.|任何加大的輸入電容都能無代價改善建立。|Any larger input capacitor improves settling without cost.
抗混疊頻譜|Anti-alias spectrum|頻带外強訊號即使不壓縮 ADC，也可能摺回通帶。|A strong out-of-band signal can alias in-band without compressing the ADC.|將濾波器阻帶和 ADC 頻率映射疊合。|Overlay filter stopband attenuation and ADC alias mapping.|不過載便保證沒有帶內混疊。|Avoiding overload guarantees no in-band aliases.
時鐘孔徑|Clock aperture|孔徑延遲是平均時間偏移，孔徑抖動是取樣時間變動。|Aperture delay is mean timing offset; aperture jitter is sampling-time variation.|分開校正固定延遲和計算 RMS 時間變異。|Correct fixed delay separately from computing RMS timing variation.|固定孔徑延遲直接等於隨機抖動。|Fixed aperture delay directly equals random jitter.
介面吞吐|Interface throughput|原始資料率還需加上編碼、框架和通道開銷。|Raw sample throughput must include encoding, framing and lane overhead.|計算通道×位數×取樣率，再列出介面額外比率。|Compute channels×bits×sample rate, then add interface overhead ratios.|串列鏈路速度只需等於取樣頻率。|Serial line rate only needs to equal sample rate.
交錯失配|Interleaving mismatch|多 ADC 交錯的增益、失調和時序失配形成特徵雜散。|Interleaved gain, offset and timing mismatch create characteristic spurs.|單獨注入一種失配，比對雜散對輸入頻率的依賴。|Inject one mismatch at a time and compare spur dependence on input frequency.|時間交錯只增加速度，不會引入額外失配。|Interleaving only increases speed and adds no mismatch.
FFT 測試|FFT testing|非相干取樣引起洩漏，窗函數改變主瓣與噪聲頻寬。|Noncoherent sampling causes leakage; windows change main-lobe width and noise bandwidth.|比較相干正弦與加窗非相干資料的功率積分。|Compare integrated power for coherent and windowed noncoherent records.|任意 FFT 最大格點就是精確的訊號功率。|The largest FFT bin always equals accurate signal power.
ENOB 與 SFDR|ENOB and SFDR|ENOB 由 SINAD 推算，SFDR 著重最大雜散，兩者不能互換。|ENOB derives from SINAD; SFDR concerns the largest spur and is not interchangeable.|對同一頻譜分別計算噪聲失真總和及最大雜散。|Compute total noise-plus-distortion and the largest spur separately.|SFDR 高就代表 ENOB 必然同樣高。|High SFDR necessarily means equally high ENOB.
多條件驗收|Multi-condition acceptance|輸入頻率、振幅和溫度必須與規格的測試條件對應。|Input frequency, amplitude and temperature must match specification conditions.|建立頻率與振幅矩陣，保存時域檔和時鐘來源。|Build a frequency/amplitude matrix and retain time records and clock-source details.|單一低頻正弦測試能代表全頻帶性能。|One low-frequency sine test represents full-band performance.
''')

course(275,'靜態線性、參考與動態建立','static linearity, references and dynamic settling',
'碼值與輸出|Codes and outputs;誤差與參考|Errors and reference;動態行為|Dynamic behavior;校準與驗證|Calibration and validation',
'理想單極 DAC：Vout=Vref·D/2ᴺ；D=0…2ᴺ−1。|Ideal unipolar DAC: Vout=Vref·D/2ᴺ; D=0…2ᴺ−1.',
'假設 16 位、Vref=4.096 V，LSB=62.5 µV；碼 32768 為 2.048 V，滿碼 65535 為 4.0959375 V。',
'For a 16-bit DAC with Vref=4.096 V, LSB=62.5 µV; code 32768 gives 2.048 V and 65535 gives 4.0959375 V.',
'理想直二進制單極傳遞；真實產品可能有增益、雙極映射、输出緩衝和保留碼。','Ideal straight-binary unipolar transfer; real products may include gain, bipolar mapping, buffering and reserved codes.',
'dac dac-glitch adi-place','adi','a271 a274','adi', '''
碼制與端點|Coding and endpoints|2ᴺ 個碼的最高碼是 2ᴺ−1，因此理想滿碼低於 Vref 一個 LSB。|With 2ᴺ codes the highest is 2ᴺ−1, so ideal full-scale code is one LSB below Vref.|檢查零碼、中碼與滿碼的期望值。|Check expected zero, midscale and full-scale-code values.|16 位滿碼等於 65536。|The largest 16-bit code is 65536.
輸出形式|Output architecture|電壓輸出與電流輸出 DAC 對負載與順從範圍要求不同。|Voltage- and current-output DACs impose different load and compliance requirements.|畫出輸出級及回授轉阻路，標記順從電壓。|Draw output and transimpedance paths and mark compliance limits.|電流輸出 DAC 對端點電壓沒有任何限制。|A current-output DAC has no terminal-voltage limit.
單調性|Monotonicity|單調代表碼增加時輸出不反向，並不代表每一步都等大。|Monotonicity means output does not reverse as code increases, not equal step sizes.|掃描相鄰碼增量的最小值。|Scan minimum adjacent-code increments.|單調就表示 INL 等於零。|Monotonicity implies zero INL.
DNL 與 INL|DNL and INL|DNL 比較步距，INL 比較相對選定參考直線的偏差。|DNL compares step size; INL compares deviation from a chosen reference line.|用同一資料分別做端點線和最佳擬合線。|Apply endpoint and best-fit lines to the same data.|不同參考線的 INL 可以不註明就直接比較。|INL with different reference lines can be compared without disclosure.
參考負載|Reference loading|DAC 碼切換可能使参考輸入動態電流改變。|Code switching can alter dynamic reference-input current.|比較参考緩衝前後的波形與輸出殘差。|Compare reference waveforms and output residuals before and after buffering.|直流參考準確便完全不需要動態分析。|An accurate DC reference eliminates the need for dynamic analysis.
熱漂與增益|Thermal drift and gain|參考與電阻比溫漂可同時改變輸出增益。|Reference and resistor-ratio drift can both change output gain.|跨溫分別觀察零點和跨度，避免混成一個偏移。|Track zero and span across temperature rather than mixing them into one offset.|所有溫漂都可用單一零點校準消除。|A single zero calibration removes all thermal drift.
建立時間|Settling time|建立時間須附誤差帶、負載與碼步距。|Settling time requires a tolerance band, load and code-step definition.|比較大跨步與小跨步進入同一 µV 誤差帶的時間。|Compare large and small steps entering the same µV band.|輸出初次抵達目標就是建立完成。|First arrival at target means settling is complete.
碼轉換毛刺|Code-transition glitch|多位同時切換的不一致時序形成短脈衝，面積通常用 V·s 表示。|Unequal switching timing during multibit transitions produces an impulse commonly measured in V·s.|比較中碼進位與單位碼跨步，固定示波器頻寬。|Compare major-carry and single-bit steps at fixed oscilloscope bandwidth.|毛刺的 V·s 面積本身就是焦耳。|Glitch area in V·s is itself energy in joules.
輸出緩衝|Output buffer|緩衝器的擺幅、輸出電流與容性負載穩定性限制 DAC 使用。|Buffer swing, current and capacitive-load stability limit DAC operation.|在模型中掃描負載電容與輸出電壓接近電源軌的情境。|Sweep load capacitance and near-rail output in the model.|rail-to-rail 名稱保證所有負載下完全到達電源軌。|Rail-to-rail guarantees reaching the rails under every load.
數位更新|Digital update|同步更新暫存器與串列寫入順序決定多通道時間偏差。|Synchronous update registers and serial-write order determine channel skew.|畫出寫入、鎖存與類比建立三段時序。|Draw write, latch and analog-settling timing separately.|SPI 傳完最後一位時類比輸出必已建立。|Analog output is settled when the last SPI bit is sent.
校準殘差|Calibration residuals|校準增益和失調後，非線性和動態誤差仍存在。|Nonlinearity and dynamic error remain after gain/offset calibration.|保留未參與擬合碼值作交叉檢查。|Reserve unfitted codes for cross-checking.|兩點校準能修正任意碼轉換毛刺。|Two-point calibration corrects arbitrary transition glitches.
量測解析力|Measurement resolution|驗證微伏步階需要比被測誤差更低的儀器噪聲與穩定性。|Microvolt-step verification requires instrument noise and drift below the target error.|測短路本底與長時間漂移，再報可分辨範圍。|Measure shorted-input noise and long-term drift before reporting resolvable limits.|更多平均必能消除長期參考漂移。|More averaging necessarily removes long-term reference drift.
''')

course(276,'射頻功率、效率與線性','RF power, efficiency and linearity',
'功率需求|Power requirements;偏壓與匹配|Bias and matching;調變失真|Modulation distortion;熱與量測|Heat and measurement',
'PAE=(Pout−Pin)/PDC；所有功率先轉瓦特。|PAE=(Pout−Pin)/PDC; convert all powers to watts.',
'假設輸出 10 W、輸入 0.1 W、直流輸入 25 W，PAE=39.6%；汲極效率為 40%，兩者不同。',
'Assume 10 W output, 0.1 W input and 25 W DC input: PAE=39.6%; drain efficiency is 40%, a different metric.',
'同時刻平均實功率，未含外部供電轉換損耗；不等於整機效率。','Average real powers measured consistently; excludes external supply-conversion losses and is not complete-system efficiency.',
'pa evm adi-place','adi','a272 a277','adi', '''
功率與 dBm|Power and dBm|dBm 是相對 1 mW 的對數功率，不可直接當瓦相減。|dBm is logarithmic power relative to 1 mW and cannot be subtracted as watts.|把 30 dBm、20 dBm 轉成瓦再算效率。|Convert 30 and 20 dBm to watts before calculating efficiency.|PAE 可用 dBm 差值除以直流瓦數。|PAE can divide a dBm difference by DC watts.
峰均比|Peak-to-average ratio|高峰均比調變需要相對平均功率保留峰值餘裕。|High-PAPR modulation requires peak headroom above average power.|以相同平均功率比較正弦與多載波包絡峰值。|Compare sine and multicarrier peaks at equal average power.|平均功率未超限就不可能削峰。|Below-limit average power makes clipping impossible.
鏈路需求|Link requirements|輸出功率需求須連同線損、天線和法規限制評估。|Output requirement includes feeder losses, antenna effects and regulatory constraints.|建立純計算鏈路預算，分清 conducted power 和 EIRP。|Build a calculation-only budget distinguishing conducted power and EIRP.|天線增益與發射機輸出瓦數是同一數量。|Antenna gain and transmitter output watts are the same quantity.
偏壓類別|Bias classes|導通角影響效率與線性；真實器件仍受寄生與負載限制。|Conduction angle influences efficiency and linearity; real devices remain limited by parasitics and load.|比較理想波形與含輸出電容模型。|Compare ideal waveforms with a model including output capacitance.|理想類別效率就是實際器件必達效率。|Ideal class efficiency is guaranteed device efficiency.
負載線|Load line|電壓電流擺幅受擊穿、電流和耗散限制。|Voltage/current swing is constrained by breakdown, current and dissipation.|在假想特性圖標示允許區域與負載線。|Mark permitted regions and a load line on hypothetical characteristics.|只要增益足夠就不需檢查輸出擺幅。|Enough gain eliminates the need to check output swing.
阻抗匹配|Impedance matching|最大輸出、最佳效率與最小失真可能要求不同最佳負載。|Maximum output, optimum efficiency and minimum distortion can require different loads.|比較三種目標的等值輪廓而非只找 S11 最小。|Compare contours for three objectives rather than minimizing S11 alone.|最佳小訊號匹配必是最佳大訊號負載。|Best small-signal match is necessarily the best large-signal load.
AM-AM 與 AM-PM|AM-AM and AM-PM|振幅壓縮與振幅相關相位旋轉都會扭曲星座。|Amplitude compression and amplitude-dependent phase rotation both distort constellations.|分別啟用兩種模型，觀察徑向和旋轉誤差。|Enable each model separately and inspect radial and rotational errors.|只有幅度誤差會影響 EVM。|Only amplitude errors affect EVM.
鄰道洩漏|Adjacent-channel leakage|非線性可產生頻譜再生，需以指定頻帶積分。|Nonlinearity can cause spectral regrowth measured over specified integration bands.|固定頻寬與偏移量比較回退前後 ACLR。|Compare ACLR with fixed bandwidth and offsets before and after backoff.|單一最大雜散等同所有鄰道整合功率。|One maximum spur equals all integrated adjacent-channel power.
預失真|Predistortion|預失真需對器件非線性和記憶效應辨識，不能恢復硬削峰資訊。|Predistortion identifies nonlinearity and memory; it cannot restore information lost to hard clipping.|用未訓練的波形驗證模型和頻譜。|Validate the model and spectrum with an untrained waveform.|任何硬削峰都可由線性增益補回。|Any hard clipping can be undone by linear gain.
熱效應|Thermal effects|溫度改變偏壓與增益，脈衝測試與連續輸出可能不同。|Temperature changes bias and gain; pulsed and continuous results can differ.|比較短脈衝與熱穩態的增益曲線。|Compare short-pulse and thermally settled gain curves.|短脈衝額定可直接視為連續額定。|A short-pulse rating directly equals a continuous rating.
失配容忍|Mismatch tolerance|反射功率與相位共同決定端點電壓電流壓力。|Reflected-power magnitude and phase jointly determine terminal stress.|在模擬中掃描同一 VSWR 的反射相位。|Sweep reflection phase at fixed VSWR in simulation.|同一 VSWR 下所有反射相位壓力相同。|All reflection phases create identical stress at a fixed VSWR.
量測閉合|Measurement closure|功率計、頻譜分析與直流量測須在一致參考面閉合能量帳。|RF power, spectral and DC measurements need consistent reference planes to close the energy balance.|核對 Pin、Pout、PDC 和散熱估計的總和。|Cross-check Pin, Pout, PDC and estimated dissipation.|效率超過 100% 只是高性能的表現。|Efficiency above 100% simply indicates high performance.
''')

course(277,'聲學濾波、損失與收發隔離','acoustic filtering, loss and transmit/receive isolation',
'頻帶規格|Band specification;諧振器模型|Resonator model;雙工整合|Duplexer integration;環境與驗證|Environment and validation',
'Qloaded=f₀/BW₃dB；插入損耗 IL=−20log₁₀abs(S21)。|Qloaded=f₀/BW₃dB; insertion loss IL=−20log₁₀abs(S21).',
'教學通帶中心 2 GHz、3 dB 頻寬 100 MHz，載入 Q≈20；若 abs(S21)=0.794，插入損耗約 2.00 dB。',
'A teaching passband at 2 GHz with 100 MHz 3 dB bandwidth has loaded Q≈20; abs(S21)=0.794 corresponds to about 2.00 dB insertion loss.',
'單一近似帶通的載入 Q；不可等同材料本徵 Q，也不是特定商用品數據。','Loaded Q of an approximate single bandpass; not intrinsic material Q or a commercial product specification.',
'rf-filter lna adi-place','adi','a272 a276','murata', '''
頻帶遮罩|Band mask|通帶漣波、阻帶衰減與過渡帶共同約束濾波器。|Passband ripple, rejection and transition width jointly constrain a filter.|標示訊號帶寬與鄰近阻塞所在頻帶。|Mark signal bandwidth and adjacent blockers.|只有中心頻率相同即可替換濾波器。|Matching center frequency alone permits replacement.
插入損耗|Insertion loss|前置被動損耗降低送入接收器的訊號並增加系統 NF。|Passive front-end loss reduces receiver input signal and raises system NF.|將濾波器放到級聯雜訊模型第一級。|Place the filter first in a cascade-noise model.|接收器前的被動濾波器完全不影響 NF。|A passive pre-receiver filter has no effect on NF.
阻抗終端|Termination|S 參數和濾波響應依指定的參考阻抗。|S parameters and filter response depend on reference impedance.|比較匹配終端與複數終端下的通帶。|Compare matched and complex terminations.|濾波器響應與前後電路阻抗無關。|Response is independent of adjacent impedances.
SAW 波長|SAW wavelength|表面聲波器件的電極週期與聲速連結工作頻率。|Electrode periodicity and acoustic velocity relate to SAW operating frequency.|使用 f≈v/λ 檢查幾何縮放趨勢。|Use f≈v/λ to check geometric scaling.|聲波頻率由自由空間光速決定。|Acoustic frequency is set by free-space light speed.
BAW 厚度|BAW thickness|體聲波厚度模態依材料和膜厚，與表面傳播路徑不同。|Bulk thickness modes depend on material and film thickness, unlike surface propagation.|比較表面週期和厚度縮放的等效模型。|Compare surface-period and thickness scaling models.|SAW 與 BAW 的幾何控制參數必然相同。|SAW and BAW necessarily have identical geometric controls.
諧振與反諧振|Resonance and antiresonance|運動支路和靜態電容使串並聯諧振頻率不同。|A motional branch and static capacitance separate series and parallel resonances.|掃描 BVD 等效阻抗的峰谷。|Sweep peaks and valleys of BVD equivalent impedance.|壓電諧振器只有一個無損電容。|A piezoelectric resonator is only one lossless capacitor.
雙工路徑|Duplex paths|雙工器將收發頻帶連到共同天線端，需要交叉隔離。|A duplexer joins transmit and receive bands to a common antenna and needs cross isolation.|畫出三埠 S 參數並分開檢查收發傳輸。|Draw three-port S parameters and separately check TX/RX transfer.|兩個二埠濾波器任意並聯即可成為理想雙工器。|Any two parallel two-port filters form an ideal duplexer.
接收去敏|Receiver desensitization|發射洩漏可能壓縮 LNA 或與相噪混頻。|TX leakage can compress the LNA or mix with phase noise.|估算洩漏到 RX 埠的功率，再對照阻塞預算。|Estimate RX leakage power and compare the blocker budget.|收發載波不同頻率就完全不會互相干擾。|Different carrier frequencies eliminate all mutual interference.
功率承受|Power handling|聲學器件的熱與非線性限制大訊號操作。|Thermal and nonlinear behavior limit acoustic-device large-signal operation.|比較小訊號插損與高功率下的漂移記錄。|Compare small-signal loss with high-power drift records.|低功率 VNA 曲線足以證明任意發射功率適用。|A low-power VNA curve proves suitability at any TX power.
溫度係數|Temperature coefficient|中心頻率與材料溫度係數相關，補償結構仍有剩餘誤差。|Center frequency follows material temperature coefficients; compensated structures retain residuals.|繪製頻帶邊界跨溫位移。|Plot band-edge movement across temperature.|溫度補償表示所有溫度完全零漂移。|Temperature compensation means zero drift at every temperature.
封裝寄生|Package parasitics|封裝和接地導通可形成額外耦合與寄生諧振。|Package and grounding paths can create coupling and parasitic resonances.|比較器件模型與含焊墊、走線模型。|Compare device-only and pad/routing-inclusive models.|封裝不會影響射頻濾波曲線。|Packaging cannot affect RF filtering.
量產判據|Production criteria|通帶、阻帶、相位和溫漂須共同建立容差遮罩。|Passband, stopband, phase and drift need a joint tolerance mask.|保存校準面與溫度條件下的完整掃頻。|Retain full sweeps with calibration-plane and temperature conditions.|只量一個中心頻點可代表全部通帶。|One center-frequency measurement represents the entire passband.
''')

course(278,'阻抗、輻射效率與環境失諧','impedance, radiation efficiency and environmental detuning',
'天線邊界|Antenna boundaries;匹配網路|Matching networks;整機耦合|Product coupling;量測證據|Measurement evidence',
'Γ=(ZL−Z₀)/(ZL+Z₀)；VSWR=(1+abs(Γ))/(1−abs(Γ))。|Γ=(ZL−Z₀)/(ZL+Z₀); VSWR=(1+abs(Γ))/(1−abs(Γ)).',
'假設 50 Ω 系統接 100 Ω 純電阻，Γ=1/3，VSWR=2，反射功率比 1/9≈11.1%。',
'A 100 Ω resistive load in a 50 Ω system gives Γ=1/3, VSWR=2 and reflected-power fraction 1/9≈11.1%.',
'單頻、實數參考阻抗；良好匹配不表示高輻射效率。','Single frequency and real reference impedance; good matching does not imply high radiation efficiency.',
'antenna rf-filter ti-place','ti','a277 a279','ti', '''
輸入阻抗|Input impedance|天線阻抗含輻射、損耗與儲能成分。|Antenna impedance contains radiation, loss and stored-energy components.|分開電阻與電抗並標示頻率。|Separate resistance and reactance with frequency labels.|實部全部都是有用輻射電阻。|All real impedance is useful radiation resistance.
參考面|Reference plane|饋線將負載阻抗轉換到量測面。|A feedline transforms load impedance to the measurement plane.|移動參考面並比較 Smith 圖旋轉。|Move the reference plane and compare Smith-chart rotation.|纜線長度不影響看到的複數阻抗。|Cable length cannot affect observed complex impedance.
反射與效率|Reflection and efficiency|失配效率 1−abs(Γ)² 只是總效率的一部分。|Mismatch efficiency 1−abs(Γ)² is only part of total efficiency.|把吸收損耗與反射損耗分開記帳。|Account separately for dissipative and reflection loss.|S11 很小就保證所有功率都被輻射。|Small S11 guarantees all power is radiated.
L 型匹配|L matching|串聯與並聯電抗可在單頻轉換阻抗。|Series and shunt reactance transform impedance at one frequency.|在 Smith 圖依次移動兩個電抗。|Apply two reactance movements successively on a Smith chart.|單頻完美匹配自動保證寬頻匹配。|Perfect single-frequency matching guarantees broadband matching.
零件 Q|Component Q|電感電容損耗會降低匹配網路效率。|Inductor and capacitor losses reduce matching-network efficiency.|比較理想與有限 Q 元件的傳輸功率。|Compare transmitted power with ideal and finite-Q components.|匹配器件永遠不消耗實功率。|Matching components never dissipate real power.
容差與帶寬|Tolerance and bandwidth|高 Q 窄帶匹配對零件與環境偏移更敏感。|High-Q narrowband matching is more sensitive to component and environmental shifts.|掃描元件上下限看可用頻帶交集。|Sweep component bounds and inspect usable-band intersection.|高 Q 一定同時帶來更寬頻帶。|Higher Q always produces wider bandwidth.
地平面|Ground plane|小型天線的地平面與整機導體是輻射系統一部分。|Ground planes and product conductors are part of a small antenna's radiating system.|改地平面尺寸而維持天線圖形，觀察共振移動。|Change ground-plane size while holding antenna shape fixed and observe resonance.|天線周圍任何地平面都不影響性能。|Surrounding ground planes never affect performance.
外殼介電|Enclosure dielectric|外殼和人體改變近場負載，造成失諧與吸收。|Enclosures and bodies load the near field, causing detuning and absorption.|比較自由空間、裝殼與握持的模型狀態。|Compare free-space, enclosed and hand-loaded model states.|裸板匹配可直接代表最終外殼產品。|Bare-board matching directly represents the enclosed product.
饋線共模|Feedline common mode|不平衡饋電可能讓量測纜線參與輻射。|Unbalanced feeding can make the measurement cable radiate.|改纜線走向，觀察方向圖與阻抗是否一起改變。|Change cable routing and inspect pattern/impedance changes.|測試纜線不可能成為天線的一部分。|A test cable cannot become part of the antenna.
VNA 校準|VNA calibration|開短負載校準將系統誤差移到定義參考面。|Open/short/load calibration transfers systematic errors to a defined plane.|使用已知驗證件檢查校準而非再用同組標準自證。|Check calibration with an independent known verification device.|校準一次之後更换纜線也無需重查。|Changing cables never requires rechecking calibration.
輻射量測|Radiation measurement|增益、方向性和效率不同；方向圖需指定偏振與環境。|Gain, directivity and efficiency differ; patterns need polarization and environment definitions.|比較同功率下不同角度與交叉偏振資料。|Compare angle and cross-polarization data at equal power.|峰值方向增益就是全空間平均效率。|Peak directional gain is all-space average efficiency.
設計驗收|Design acceptance|匹配、效率、頻帶和使用情境要共同決定放行。|Matching, efficiency, bandwidth and use cases jointly determine acceptance.|建立情境矩陣並指出最差的可用頻段。|Build a use-case matrix and identify the worst usable band.|單一最佳方向圖足以通過全部使用情境。|One best-case pattern validates every use case.
''')

course(279,'相位排列、空間取樣與校準','phase progression, spatial sampling and calibration',
'陣列幾何|Array geometry;波束合成|Beam synthesis;寬頻與校準|Bandwidth and calibration;量測與限制|Measurement and limits',
'Δφ=−2π(d/λ)sinθ；θ 自正前方量起，符號依座標約定。|Δφ=−2π(d/λ)sinθ; θ is from broadside and sign depends on convention.',
'教學間距 d=λ/2、指向 θ=30°，相鄰單元相位差 −90°；座標反向則符號反轉。',
'For d=λ/2 and steering angle θ=30°, adjacent elements need −90° phase difference; reversing coordinates reverses the sign.',
'遠場、均勻直線陣列和窄頻近似；不含互耦或單元方向圖。','Far-field uniform linear array, narrowband approximation; excludes mutual coupling and element patterns.',
'array antenna adi-place','adi','a278 a273','adi', '''
座標與波前|Coordinates and wavefront|入射角決定相鄰單元路徑差，角度基準需一致。|Arrival angle sets adjacent-element path difference and requires a consistent reference.|以正負角度檢查延遲及相位符號。|Check delay and phase signs for positive and negative angles.|從端射與正前方量角可不換公式。|Endfire and broadside angles use the same formula unchanged.
單元間距|Element spacing|過大間距造成可見空間混疊，掃描範圍會改變限制。|Excess spacing creates visible spatial aliases; scan range changes the limit.|掃描 d/λ 和角度，找額外陣列峰值。|Sweep d/λ and angle to find additional array peaks.|任何間距只要校準相位就沒有柵瓣。|Phase calibration eliminates grating lobes at any spacing.
單元方向圖|Element pattern|總方向圖包含單元方向圖與陣列因子，不能只看理想點源。|Total pattern includes element pattern and array factor, not only ideal point sources.|將單元方向圖與陣列因子相乘比較掃描損失。|Multiply element pattern and array factor to compare scan loss.|陣列因子就是完整實體天線方向圖。|The array factor is the complete physical antenna pattern.
相位移器|Phase shifter|有限位數將理想相位量化，造成指向與旁瓣誤差。|Finite bits quantize ideal phase, creating pointing and sidelobe errors.|比較連續相位與量化相位的峰值和旁瓣。|Compare peak and sidelobes for continuous and quantized phase.|相位位數只影響數位控制，不影響方向圖。|Phase bits affect only digital control, not patterns.
振幅加權|Amplitude taper|振幅窗可降低旁瓣，但會犧牲主瓣寬度或效率。|Amplitude taper reduces sidelobes at a cost in beamwidth or efficiency.|保持總功率相同比較均勻與漸縮加權。|Compare uniform and tapered weights at equal total power.|旁瓣降低必然不改變主瓣寬度。|Lower sidelobes never change main-lobe width.
相干合成|Coherent combining|各通道相位一致時電場相加，功率尺度需固定總輸入條件。|Aligned channels add fields coherently; power scaling requires fixed input assumptions.|區分固定每單元功率與固定總功率的增益比較。|Distinguish fixed per-element and fixed total power comparisons.|新增單元可在零新增功率下無限制提升總輻射功率。|More elements increase total radiated power without limit at zero added power.
波束斜視|Beam squint|固定相位對不同頻率不等於固定時間延遲。|Fixed phase is not fixed time delay across frequency.|保持相位設定、掃頻觀察指向偏移。|Hold phase settings and sweep frequency to observe pointing drift.|相位移波束在任意寬頻都維持同角度。|Phase-steered beams retain angle at any bandwidth.
真時延|True time delay|真時延令相位隨頻率線性變化，可抑制理想波束斜視。|True delay gives phase linear in frequency and suppresses ideal beam squint.|比較相位移與時延兩種模型的頻率角度圖。|Compare angle-frequency maps for phase and delay models.|真時延能消除所有互耦與增益誤差。|True delay eliminates all coupling and gain errors.
通道校準|Channel calibration|通道增益相位誤差需在共同參考面估算。|Channel gain/phase errors need estimation at a common plane.|以獨立驗證方向檢查校準後殘差。|Check post-calibration residuals at an independent validation angle.|單一通道校準代表全陣列校準完成。|Calibrating one channel calibrates the entire array.
互耦|Mutual coupling|其他單元的負載影響有效輸入阻抗及單元響應。|Other elements' loading affects active impedance and element response.|比較孤立單元與嵌入陣列單元模型。|Compare isolated and embedded-element models.|孤立單元 S11 可完全代表掃描中的陣列單元。|Isolated S11 completely represents a scanning array element.
遠近場|Near and far field|有限量測距離可能不滿足平面波與遠場近似。|Finite distance may violate plane-wave and far-field assumptions.|按孔徑與波長估算距離尺度並標記近場資料。|Estimate distance scale from aperture/wavelength and label near-field data.|任何距離量到的方向圖都直接等於遠場圖。|A pattern measured at any distance is directly a far-field pattern.
失效通道|Failed elements|失效單元位置決定旁瓣與指向惡化，數量不是唯一因素。|Failed-element positions determine sidelobe and pointing degradation; count is not enough.|比較同數量的集中失效與分散失效。|Compare clustered and distributed failures at equal count.|相同失效數必有完全相同方向圖。|Equal failed-element counts imply identical patterns.
''')

course(280,'混頻、IQ 誤差與數位射頻協同','mixing, IQ errors and analog/digital co-design',
'接收架構|Receiver architecture;增益與濾波|Gain and filtering;校準與介面|Calibration and interfaces;重現與驗收|Reproducibility and acceptance',
'fIF=abs(fRF−fLO)；複數 IQ 保留正負頻率方向。|fIF=abs(fRF−fLO); complex IQ preserves positive/negative frequency orientation.',
'教學 RF=915 MHz、LO=910 MHz，差頻 5 MHz；若 LO 改 920 MHz，實數頻差仍 5 MHz，但理想 IQ 的頻率符號相反。',
'For RF=915 MHz and LO=910 MHz the difference is 5 MHz; LO=920 MHz also gives a 5 MHz real difference but reverses the ideal IQ frequency sign.',
'理想混頻與固定 IQ 符號約定；真實系統含鏡像、直流偏移及 LO 洩漏。','Ideal mixing with a fixed IQ sign convention; real systems contain images, DC offsets and LO leakage.',
'sdr sdr-agc adi-place','adi','a272 a273','adi', '''
零中頻與低中頻|Zero and low IF|零中頻簡化濾波但直流與 1/f 更接近訊號；低中頻需鏡像規劃。|Zero IF simplifies filtering but brings DC and 1/f close to signal; low IF needs image planning.|比較同訊號在兩種架構中的干擾位置。|Compare interference locations in both architectures.|零中頻完全不需處理直流偏移。|Zero IF needs no DC-offset treatment.
IQ 定義|IQ convention|複數訊號的 I+jQ 或 I−jQ 約定改變頻率方向。|I+jQ versus I−jQ reverses complex frequency direction.|輸入已知偏移正弦，確認頻譜方向。|Use a known-offset tone to verify spectral orientation.|IQ 頻率符號與資料排列無關。|IQ frequency sign is independent of data ordering.
取樣鏈|Sampling chain|類比濾波、ADC 取樣與數位抽取需共同配置。|Analog filtering, ADC sampling and digital decimation need joint configuration.|逐級標示可用頻寬與混疊區域。|Mark usable bandwidth and alias zones at each stage.|抽取倍數可任意增加且永不混疊。|Decimation can increase arbitrarily without aliasing.
增益預算|Gain budget|前端增益提高弱訊號 SNR，但縮小強阻塞餘裕。|Front-end gain improves weak-signal SNR but reduces blocker headroom.|以同一弱訊號掃描阻塞強度並觀察 clipping。|Sweep blocker strength with a fixed weak signal and inspect clipping.|最大接收增益永遠是最佳設定。|Maximum receive gain is always optimal.
AGC 時序|AGC timing|增益變動後需等類比路徑建立，過快追蹤可能破壞包絡。|After a gain change the analog path must settle; overly fast tracking can distort envelopes.|對照突發訊號前導與 AGC 穩定時間。|Compare burst preamble duration and AGC settling.|AGC 只需越快越好，不需考慮訊號格式。|AGC should simply be as fast as possible regardless of waveform.
通道濾波|Channel filtering|通帶與群延遲需兼顧調變帶寬和鄰道阻塞。|Passband and group delay balance modulation bandwidth and adjacent blockers.|比較振幅平坦但相位不同的兩個濾波器。|Compare filters with similar amplitude but different phase.|通帶振幅平坦就保證零調變失真。|Flat passband amplitude guarantees zero modulation distortion.
IQ 失衡|IQ imbalance|增益和正交相位誤差產生鏡像。|Gain and quadrature phase errors create images.|單獨注入增益或相位誤差，觀察影像抑制。|Inject gain or phase error separately and observe image rejection.|I 與 Q 增益相同便保證完美正交。|Equal I/Q gain guarantees perfect quadrature.
直流校準|DC calibration|直流校準可能同時影響真正接近零頻率的訊號。|DC calibration can affect legitimate near-zero-frequency signal content.|比較啟用和關閉追蹤時的低頻資料。|Compare low-frequency data with tracking enabled and disabled.|移除 DC 永遠不會損失有用訊號。|Removing DC never removes useful signal.
時鐘同步|Clock synchronization|共用參考頻率不保證多裝置的啟動相位相同。|A shared frequency reference does not guarantee equal startup phase across devices.|分別驗證頻率一致、時間戳與相位重複性。|Verify frequency, timestamps and phase repeatability separately.|共用晶振即表示所有通道天生同相。|A shared oscillator makes every channel inherently phase aligned.
資料吞吐|Data throughput|IQ 每樣本兩個數值，主機緩衝與傳輸可成為瓶頸。|IQ contains two values per sample; host buffering and transport can bottleneck.|計算 I/Q 位寬、通道數與取樣率，再核對掉樣計數。|Calculate IQ width, channels and sample rate, then check dropped-sample counters.|RF 波形良好就代表主機沒有掉樣。|A good RF waveform proves the host drops no samples.
校準版本|Calibration provenance|頻率、溫度與增益改變後，舊校準可能不再合用。|Old calibration may not remain valid after frequency, temperature or gain changes.|保存校準版本與條件，對未校準頻點驗證。|Save calibration versions/conditions and validate at an unfitted frequency.|一次校準可無條件覆蓋全部射頻範圍。|One calibration unconditionally covers the entire RF range.
封閉測試|Contained testing|有線衰減與封閉模擬可驗證訊號鏈而不任意發射。|Attenuated cabled tests and contained simulation validate chains without uncontrolled transmission.|用已知檔案和迴路保存 EVM、頻譜及版本。|Use known files and a contained loop to retain EVM, spectra and versions.|能產生波形就自動取得任意頻段發射權。|Generating a waveform automatically grants transmission rights in any band.
''')

course(281,'多層堆疊、回流路徑與製造驗證','multilayer stackup, return paths and manufacturing verification',
'堆疊定義|Stackup definition;圖形與連通|Pattern and connectivity;訊號與電源|Signal and power;製造與驗收|Fabrication and acceptance',
'平行板近似 C=ε₀εrA/d；銅線直流 R=ρL/(wt)。|Parallel-plate approximation C=ε₀εrA/d; copper-trace DC R=ρL/(wt).',
'假設銅線 L=0.10 m、w=0.5 mm、t=35 µm、ρ=1.72×10⁻⁸ Ω·m，R≈0.0983 Ω，1 A 時直流損耗約 0.0983 W。',
'For L=0.10 m, w=0.5 mm, t=35 µm and copper ρ=1.72×10⁻⁸ Ω·m, R≈0.0983 Ω; at 1 A the DC loss is about 0.0983 W.',
'均勻截面、固定電阻率；忽略溫升、電鍍變異與集膚效應。','Uniform cross section and fixed resistivity; excludes heating, plating variation and skin effect.',
'pcb hdi euro-place','euro','a282 a283','euro', '''
層疊材料|Stack materials|核心板、半固化片與銅箔扮演不同結構角色。|Cores, prepreg and copper foil have different structural roles.|逐層標出固化前後材料及銅層編號。|Label before/after-cure materials and copper-layer numbers.|半固化片與已固化核心板可完全互換。|Prepreg and cured core are fully interchangeable.
對稱堆疊|Symmetric stackup|厚度和銅分布不對稱可加劇翹曲。|Asymmetric thickness and copper distribution can worsen warp.|比較兩種堆疊的鏡像對稱與銅密度。|Compare mirror symmetry and copper density of two stacks.|只要層數偶數就必然沒有翹曲。|An even layer count guarantees no warp.
材料頻率性|Frequency-dependent material|介電常數和耗散因子依頻率、方向及測試法而變。|Permittivity and loss depend on frequency, direction and test method.|核對材料表的頻率和測試條件再建模型。|Check test frequency and method before modeling.|資料表單一 Dk 可無條件用於全頻帶。|A single datasheet Dk applies unconditionally at all frequencies.
內層圖形|Inner-layer pattern|蝕刻補償與實際線寬偏差影響阻抗和間距。|Etch compensation and actual width variation affect impedance and spacing.|比較設計線寬、製造補償值與截面實測。|Compare design, compensated and cross-section widths.|Gerber 線寬一定等於完成銅線寬。|Gerber width always equals finished copper width.
孔與鍍銅|Holes and plating|完成孔徑、鑽孔徑與孔壁鍍層是不同尺寸。|Finished hole, drill diameter and barrel plating are different dimensions.|用截面標注最薄鍍層及環寬。|Annotate minimum plating and annular ring on a section.|鑽頭直徑就是完成孔內徑。|Drill diameter is the finished hole diameter.
層間對位|Layer registration|累積對位偏差會侵蝕環寬及介電間隙。|Accumulated registration error consumes annular ring and dielectric clearance.|疊合最大偏移情境並檢查局部最小距離。|Overlay worst offsets and check local minimum separation.|各層單独合格就保證疊合一定合格。|Each layer passing alone guarantees assembly registration.
回流連續|Return continuity|高速回流傾向靠近訊號路徑，跨參考平面裂縫會擴大迴路。|High-frequency returns stay near signals; crossing reference splits enlarges loops.|在走線上逐段畫出對應回流。|Draw the return path along each trace segment.|所有地平面裂縫對高速訊號都沒有影響。|Ground-plane splits never affect high-speed signals.
阻抗控制|Controlled impedance|阻抗同時受寬厚、介電距離和材料影響。|Impedance depends on width, thickness, dielectric spacing and material.|對幾何容差做敏感度掃描，不只調線寬。|Sweep geometric tolerances rather than adjusting only width.|只指定 50 Ω 就足夠讓工廠知道完整堆疊。|Specifying 50 Ω fully defines the manufacturing stack.
電源分配|Power distribution|平面、過孔及去耦形成頻率相關 PDN 阻抗。|Planes, vias and decoupling form frequency-dependent PDN impedance.|比較目標阻抗與多頻率共振峰。|Compare target impedance with resonance peaks across frequency.|電容總容量大就保證所有頻率低阻抗。|Large total capacitance guarantees low impedance at every frequency.
可製造檢查|Manufacturability review|阻焊、銅到板邊和可測性都需隨製程能力確認。|Solder mask, copper-to-edge distance and testability need process-capability review.|列出工廠回覆的例外及圖面版本。|Record supplier exceptions and drawing revisions.|通過電氣 DRC 就保證所有製造條件合格。|Electrical DRC guarantees all fabrication conditions pass.
試片驗證|Coupon verification|阻抗試片需代表板內堆疊與同批加工。|Impedance coupons must represent the board stack and same-lot processing.|比較試片走線與真正關鍵線的層位和幾何。|Compare coupon and critical-trace layer/geometric conditions.|任意外加測試線都能代表板上所有線。|Any added test trace represents every board trace.
失效截面|Failure cross-section|連通測試只能找部分缺陷，截面能補充內部形貌證據。|Connectivity tests find only some defects; sections add internal morphology evidence.|將電測異常與孔壁截面位置對照。|Correlate electrical failures with barrel cross-section locations.|直流導通就證明孔壁不存在可靠度風險。|DC continuity proves the barrel has no reliability risk.
''')

course(282,'微孔、增層與高密度逃線','microvias, buildup and dense escape routing',
'逃線與結構|Escape and structure;微孔與增層|Microvias and buildup;訊號與可靠度|Signals and reliability;驗證与交付|Verification and release',
'孔深徑比 AR=h/d；幾何定義須指明入口或底部孔徑。|Via aspect ratio AR=h/d; specify whether d is entry or bottom diameter.',
'教學微孔介電深度 60 µm、入口直徑 100 µm，AR=0.60；此比值是幾何比較，不是通用合格門檻。',
'A teaching microvia 60 µm deep with 100 µm entry diameter has AR=0.60; this is a geometric comparison, not a universal acceptance limit.',
'錐形微孔、鍍填和材料可靠度需另外驗證；所有尺寸為假設。','Taper, fill plating and material reliability need separate verification; all dimensions are assumed.',
'hdi pcb euro-place','euro','a281 a287','euro', '''
BGA 逃線|BGA escape|焊墊節距、通道寬度及孔盤共同限制逃線。|Pad pitch, channel width and via lands constrain escape routing.|為內外兩圈焊墊畫可用路徑與瓶頸。|Map paths and bottlenecks for inner and outer pad rings.|只縮線寬就一定解決任何 BGA 逃線。|Narrower traces always solve any BGA escape.
增層配置|Buildup configuration|不同增層次數影響孔可達層與壓合成本。|Buildup count affects reachable layers and lamination cost.|畫出每次壓合後才能形成的連接。|Draw connections enabled after each lamination.|任意層對都能用一次雷射形成微孔。|Any layer pair can be connected by one laser step.
微孔定義|Microvia definition|盲孔、埋孔、微孔與通孔有不同幾何和製程意義。|Blind, buried, micro and through vias have distinct geometry and process meanings.|用截面指出每種孔的起終層。|Identify each via's start/end layers on a section.|所有盲孔都必然是雷射微孔。|Every blind via is necessarily a laser microvia.
雷射成孔|Laser via formation|介電吸收、銅停層與碎屑影響底部形貌。|Dielectric absorption, copper stops and debris affect bottom morphology.|比較截面的底部殘渣與側壁錐度。|Compare bottom residue and wall taper in sections.|入口外觀光滑就證明孔底潔淨。|A smooth entry proves a clean via bottom.
清潔與金屬化|Cleaning and metallization|孔底界面品質影響種子層與電鍍連續性。|Bottom-interface quality affects seed and plating continuity.|以界面缺口和導通資料交叉判讀。|Correlate interface gaps with continuity data.|外層銅厚足夠就保證孔底界面良好。|Enough outer copper guarantees a sound bottom interface.
填孔與凹陷|Fill and dimples|填孔空洞及頂部凹陷會影响後续堆疊與焊墊平坦度。|Fill voids and top dimples affect stacking and pad planarity.|比較截面、表面高度與電阻三種證據。|Compare sections, surface height and resistance.|表面封口就代表孔內完全無空洞。|A closed surface proves a void-free fill.
堆疊和錯位|Stacked and staggered vias|堆疊節省面積但界面受力路徑不同於錯位微孔。|Stacking saves area but changes stress paths relative to staggered vias.|畫出熱膨脹應變如何穿越各孔底界面。|Draw thermal-strain paths across each bottom interface.|堆疊和錯位微孔有完全相同的可靠度機制。|Stacked and staggered vias have identical reliability mechanisms.
孔樁與高速|Stubs and high speed|未使用孔段產生寄生，短微孔可減少但不能消除所有不連續。|Unused via sections add parasitics; short microvias reduce but do not remove discontinuities.|比較不同孔長的時域阻抗與頻域損耗。|Compare time-domain impedance and loss for different via lengths.|只要使用微孔就沒有任何高速寄生。|Microvias eliminate all high-speed parasitics.
熱機械載荷|Thermomechanical load|銅和介電材料熱膨脹差使界面循環受力。|Copper/dielectric expansion mismatch cyclically loads interfaces.|比較溫循前後電阻變化而非只做初測。|Compare resistance before/after cycling, not only initially.|初始電阻合格代表永不產生界面裂縫。|Initial resistance passing prevents any later interface crack.
對位預算|Registration budget|微孔底盤的可用重疊面積受多層誤差限制。|Useful bottom-land overlap is limited by multilayer misregistration.|在最大偏移下重算剩餘接觸面積。|Recalculate remaining contact area at maximum offset.|較大的入口孔保證任意對位都安全。|A larger via entry guarantees safe registration at any offset.
驗證取樣|Validation sampling|切片位置與樣本數限制看到空洞和裂縫的機率。|Section position and sample count limit detection probability of voids/cracks.|比較不同切片方向，列出未觀測區域。|Compare section directions and list unobserved regions.|一張無缺陷截面可證明全批完全無缺陷。|One defect-free section proves the entire lot defect-free.
供應商交付|Supplier release|層疊、孔結構、檢验與變更控制需一同凍結。|Stackup, via structure, inspection and change control must be frozen together.|整理能力確認、試片與圖版追溯表。|Compile capability confirmation, coupons and drawing traceability.|只傳成品 Gerber 就不需說明增層結構。|Gerber alone removes the need to define buildup.
''')

course(283,'彎曲應變、材料與剛柔交界','bending strain, materials and rigid-flex transitions',
'機構與層疊|Mechanics and stackup;彎曲區設計|Bend-region design;製造與組裝|Fabrication and assembly;耐久驗證|Durability validation',
'簡化彎曲應變 ε≈y/R；均質對稱薄片外表面 y≈t/2。|Simplified bending strain ε≈y/R; for a homogeneous symmetric sheet the outer surface has y≈t/2.',
'假設均質薄片 t=0.10 mm、R=10 mm，外表面應變約 0.5%；真實多層銅與膠的中性軸需重算。',
'For a homogeneous sheet t=0.10 mm and R=10 mm, outer-surface strain is about 0.5%; real copper/adhesive multilayers need a recalculated neutral axis.',
'小應變幾何近似，不是銅疲勞壽命或允許彎曲半徑規格。','Small-strain geometric approximation, not a copper fatigue-life or allowable-radius specification.',
'flex pcb euro-place','euro','a281 a289','ttm', '''
固定與動態彎曲|Static versus dynamic flex|裝配時彎一次與使用中反覆彎曲需要不同壽命要求。|One-time installation bends and repeated operational flexing need different life requirements.|明確列出預計彎曲次數與角度分布。|List expected bend count and angle distribution.|可折一次就表示可無限次動態彎折。|One successful bend proves unlimited dynamic flex.
材料選擇|Material selection|聚醯亞胺、膠與銅箔共同決定柔性和吸濕行為。|Polyimide, adhesive and copper jointly determine flexibility and moisture behavior.|比較層疊的厚度及材料模數而非只看基膜。|Compare stack thickness/moduli, not just base film.|柔性板機械性能只由基膜決定。|Flex mechanics depend only on base film.
中性軸|Neutral axis|不同彈性模數和厚度使中性軸偏離幾何中心。|Different moduli and thicknesses shift the neutral axis from geometric center.|以轉換截面估算銅層到中性軸距離。|Estimate copper-to-neutral-axis distance using a transformed section.|多層板中性軸永遠位於幾何正中央。|A multilayer neutral axis is always at the geometric center.
走線方向|Trace direction|跨越彎曲軸的走線受彎曲應變，轉角與寬度變化易集中應力。|Traces crossing a bend axis experience strain; corners and width changes concentrate stress.|標記彎曲帶內的幾何突變。|Mark geometric discontinuities within the bend zone.|在彎曲區增加尖角能分散應力。|Sharp corners in a bend distribute stress.
銅层配置|Copper arrangement|多層重疊銅增加局部剛度與應力集中。|Overlapping multilayer copper raises local stiffness and stress concentration.|比較上下層對齊和错開走線。|Compare aligned and staggered opposing-layer traces.|柔性區所有層完整鋪銅總是最佳。|Solid copper on every flex layer is always best.
覆蓋膜開窗|Coverlay openings|覆蓋膜與焊墊的交界需容納對位並防剝離。|Coverlay/pad transitions need registration allowance and peel resistance.|疊合開窗公差和補強位置。|Overlay opening tolerances and stiffener positions.|覆蓋膜開口可與焊墊做完全零容差。|Coverlay openings can use zero tolerance to pads.
剛柔交界|Rigid-flex transition|剛度跳變處會集中彎曲應力，不能把活動彎折點壓在交界。|Stiffness transitions concentrate bending stress; active bending should not be forced at the boundary.|畫機構裝配後的實際彎曲曲率。|Draw actual installed curvature.|剛柔交界一定是最佳反覆折點。|The rigid-flex boundary is always the best repeated bend point.
孔和補強|Vias and stiffeners|孔與焊點適合放在受支撐區，補強會改變應變分布。|Vias and joints belong in supported regions; stiffeners alter strain distribution.|比較支撐邊緣與孔的位置。|Compare support edges and via positions.|補強片越多就保證所有區域應力越低。|More stiffeners guarantee lower stress everywhere.
組裝熱歷程|Assembly thermal history|薄柔性材料的吸濕與熱歷程影響平整和界面。|Moisture and thermal history of thin flex affect flatness and interfaces.|對照材料規範與實際受熱紀錄，不套用任意烘烤配方。|Compare material requirements with recorded heating; do not invent bake recipes.|所有柔性材料可共用同一熱處理參數。|All flex materials can use identical thermal treatment.
動態導通|Dynamic continuity|裂紋可能只在特定彎角張開，靜態電測會漏掉。|Cracks may open only at particular angles and evade static tests.|在模擬測試資料中對齊角度與電阻瞬變。|Align angle and resistance transients in simulated test data.|攤平時導通就代表彎曲時永遠導通。|Flat continuity guarantees continuity while bent.
環境交互|Environmental interaction|溫濕、化學暴露與彎折可共同改變疲勞。|Temperature, humidity, exposure and flexing can jointly change fatigue.|將使用環境與彎曲剖面組成測試矩陣。|Combine environment and flex profile into a test matrix.|室溫乾燥彎折試驗代表所有環境。|Dry room-temperature flex testing represents every environment.
失效定位|Failure localization|走線裂紋、膠分層和連接器失效需不同證據。|Trace cracks, adhesive delamination and connector failures need different evidence.|對照動態電測、外觀與截面後才提出修正。|Correlate dynamic electrical, visual and sectional evidence before proposing changes.|所有間歇斷路都只能由連接器造成。|Every intermittent open can only come from a connector.
''')

course(284,'錫膏、貼裝與生產線資料閉環','paste, placement and production-line feedback',
'資料與印刷|Data and printing;貼裝與供料|Placement and feeding;回焊與檢測|Reflow and inspection;產線與追溯|Line and traceability',
'理論印刷體積 V=Aaperture·t；轉移效率 η=Vactual/Vtheoretical。|Theoretical print volume V=Aaperture·t; transfer efficiency η=Vactual/Vtheoretical.',
'教學開口 0.30×0.40 mm、鋼網厚 0.10 mm，理論體積 0.012 mm³；量得 0.0096 mm³ 則轉移效率 80%。',
'A teaching aperture 0.30×0.40 mm with 0.10 mm stencil gives 0.012 mm³ theoretical volume; 0.0096 mm³ measured means 80% transfer efficiency.',
'矩形幾何近似，不含壁錐、錫膏流變和量測不確定度；不是製程目標值。','Rectangular geometry excludes wall taper, paste rheology and measurement uncertainty; not a process target.',
'smt smt-loop euro-place','euro','a285 a286','asmpt', '''
BOM 與座標|BOM and coordinates|元件料號、方向和貼裝座標需對同一圖版。|Part numbers, orientation and placement coordinates must use the same revision.|交叉核對 BOM、封裝和極性標記。|Cross-check BOM, footprints and polarity marks.|相同封裝名稱表示所有腳位功能相同。|Identical package names imply identical pin functions.
鋼網開口|Stencil apertures|開口面積與壁面積比影響脫模，不能只看體積。|Aperture area-to-wall ratio affects release, not just volume.|比較同體積的不同長寬開口。|Compare aperture shapes with equal volume.|相同理論體積必有相同轉移效率。|Equal theoretical volume guarantees equal transfer efficiency.
錫膏狀態|Paste condition|黏度、使用時間與溫度影響印刷，需依材料指引追溯。|Viscosity, exposure time and temperature affect printing and need material-guided traceability.|對照批號與環境紀錄的體積趨勢。|Compare volume trends with lot/environment records.|錫膏材料狀態不會影響印刷一致性。|Paste condition cannot affect printing consistency.
SPI 量測|Solder-paste inspection|高度、面積和體積揭示不同印刷異常。|Height, area and volume reveal different print defects.|對照同體積但形狀不同的兩份假想資料。|Compare two hypothetical deposits with equal volume but different shape.|只量面積即可完全替代體積量測。|Area alone completely replaces volume measurement.
供料與追溯|Feeding and traceability|料站、捲帶及替代料映射錯誤可能產生外觀相同的錯料。|Feeder, reel and substitute mappings can produce visually identical wrong parts.|核對料卷條碼、站位與替代料批准。|Check reel barcode, station and substitute approval.|外觀相同就能保證元件電性相同。|Identical appearance guarantees identical electrical behavior.
視覺對位|Vision alignment|板基準點修正整體姿態，局部翹曲仍可能留下位置誤差。|Board fiducials correct global pose while local warp can leave placement errors.|分離全板平移旋轉和局部殘差。|Separate global translation/rotation from local residuals.|三點對位消除所有板材局部形變。|Three-point alignment removes every local deformation.
吸嘴與元件|Nozzle and component|吸取成功率與元件質量、表面及吸嘴狀態相關。|Pickup success depends on mass, surface and nozzle condition.|依吸嘴、料站與元件分類失敗資料。|Group failures by nozzle, feeder and component.|提高吸取速度一定同時提高良率。|Higher pickup speed always improves yield.
回焊交接|Reflow handoff|元件受熱曲線與爐設定不同，熱容量差使溫度不均。|Component temperature differs from oven settings; thermal-mass differences create nonuniformity.|把輕重元件的量測曲線放在同一時間軸。|Overlay measured light/heavy-component profiles.|爐區設定温度就是每個焊點溫度。|Zone setpoint equals every joint temperature.
檢測關聯|Inspection correlation|SPI、貼裝和 AOI 同座標資料可幫助定位來源。|Registered SPI, placement and AOI data help locate defect origins.|追蹤同一焊墊跨三站的變化。|Track one pad across three stations.|回焊後缺陷都只能由爐子造成。|All post-reflow defects can only originate in the oven.
節拍平衡|Takt balancing|最慢有效工站限制產出，標稱速度不含换線與停機。|The slowest effective station limits output; nominal speed excludes changeover/downtime.|用假想運行與停機時間計算實際吞吐。|Compute effective throughput from assumed run/downtime.|把各機器最高速度相加就是產線產量。|Summing machine peak speeds gives line output.
製程能力|Process capability|能力指標需穩定分布與合適量測系統，不能掩蓋漂移。|Capability indices require stable distributions and adequate metrology, not hidden drift.|先畫時間趨勢再比較規格分布。|Plot time trends before comparing specification distributions.|任何混合批資料都能直接計算有意義 Cpk。|Any mixed-lot data yields meaningful Cpk directly.
變更控制|Change control|料替、程式與檢測門檻變更都應連到序號。|Substitutions, programs and thresholds must be linked to serial numbers.|建立某板可重建的材料與程式版本清單。|Build a reconstructable material/program version list for a board.|只記成品序號就足以重建所有製程條件。|A finished serial number alone reconstructs all process conditions.
''')

course(285,'潤濕、熱曲線與焊點形成','wetting, thermal profiles and joint formation',
'材料與界面|Materials and interfaces;回焊曲線|Reflow profile;選焊路徑|Selective solder path;焊點驗證|Joint verification',
'簡化熱量 Q=mcpΔT；實際相變另需潜熱。|Simplified sensible heat Q=mcpΔT; phase change additionally needs latent heat.',
'假設 2 g 銅件、cp=385 J/(kg·K)、升溫 150 K，顯熱約 115.5 J；不含焊料熔化和散熱。',
'For 2 g of copper, cp=385 J/(kg·K) and a 150 K rise, sensible heat is about 115.5 J; solder melting and losses are excluded.',
'定比熱與均溫假設；不可作為實際爐溫或焊接時間配方。','Constant heat capacity and uniform temperature; not an oven-temperature or soldering-time recipe.',
'solder smt euro-place','euro','a284 a289','ersa', '''
合金與液相|Alloy and liquidus|固相線和液相線與合金有關，不能把所有焊料視為同一熔點。|Solidus and liquidus depend on alloy; solders do not share one melting point.|對照材料證明中的合金與相變範圍。|Check alloy and phase-change range in material records.|所有無鉛焊料具有完全相同熔點。|All lead-free solders have identical melting points.
氧化與助焊|Oxides and flux|助焊劑處理氧化界面，活性與殘留需配合材料和熱歷程。|Flux addresses oxide interfaces; activity/residue depend on materials and thermal history.|對照潤濕差與助焊劑批次、保存紀錄。|Correlate poor wetting with flux lot and storage records.|增加助焊劑量永遠沒有副作用。|Adding more flux never has side effects.
潤濕與幾何|Wetting and geometry|接觸角、表面能和焊墊幾何影響焊料分布。|Contact angle, surface energy and pad geometry affect solder distribution.|比較相同體積在不同表面狀態的形狀。|Compare equal volume on different surface conditions.|焊料體積相同就保證焊點形狀相同。|Equal solder volume guarantees identical joint shape.
預熱均衡|Preheat balance|不同熱容量元件升溫速率不同，預熱用於管理溫差和揮發。|Different thermal masses heat differently; preheat manages gradients and volatiles.|比較重元件與薄焊墊的溫升斜率。|Compare temperature-rise slopes of heavy components and thin pads.|最快升溫一定能改善所有焊點。|Fastest heating necessarily improves every joint.
液相以上時間|Time above liquidus|液相以上停留影響界面反應，但要與材料要求一起解讀。|Time above liquidus affects interface reactions and needs material-specific interpretation.|由實測曲線積出各焊點的停留時間。|Extract dwell above liquidus from each measured joint profile.|爐帶速度單獨即可決定所有焊點的液相時間。|Conveyor speed alone determines every joint's liquidus time.
冷卻與組織|Cooling and microstructure|冷卻歷程影響凝固與熱應力，外觀不能單獨判定組織。|Cooling affects solidification and stress; appearance alone cannot determine microstructure.|把冷卻曲線與截面觀察對照。|Correlate cooling profiles and cross sections.|光亮外觀必代表最佳冶金組織。|A shiny surface necessarily means optimal metallurgy.
通孔毛細填充|Through-hole capillary fill|孔壁潤濕、間隙和熱容量共同控制通孔填充。|Barrel wetting, gap and thermal mass jointly control through-hole fill.|比較相同接觸時間不同熱負載的填孔資料。|Compare fill at equal contact time with different thermal loads.|填孔高度只由焊錫波高度決定。|Fill height depends only on solder-wave height.
選焊可達性|Selective-solder access|噴嘴路徑、周邊元件和熱敏區決定可達性。|Nozzle path, adjacent components and heat-sensitive zones determine access.|以三維包絡檢查噴嘴與元件干涉。|Check nozzle/component interference using envelopes.|任何通孔都可在完成組裝後直接選焊。|Every through-hole joint remains accessible after assembly.
橋接與拉尖|Bridges and icicles|退出方向、潤濕與流動可改變多餘焊料分離。|Withdrawal direction, wetting and flow affect excess-solder separation.|以方向與缺陷位置對照表找關聯。|Correlate travel direction and defect locations.|所有橋接都只由鋼網厚度造成。|Every bridge is caused only by stencil thickness.
金屬間化合物|Intermetallics|界面化合物是接合一部分，過厚或脆化需結合材料判斷。|Intermetallics are part of joining; excess growth or brittleness need material context.|比較老化前後界面厚度與破壞位置。|Compare interface thickness and fracture location before/after aging.|焊點中任何金屬間化合物都代表失敗。|Any intermetallic in a joint means failure.
空洞與裂縫|Voids and cracks|空洞比例、位置和用途共同決定影響。|Void amount, location and application jointly determine impact.|將 X 光投影與截面對照避免把重疊當單一缺陷。|Compare X-ray projections with sections to avoid overlap misinterpretation.|相同空洞面積必然有相同可靠度影響。|Equal void area always has equal reliability impact.
檢驗與追溯|Inspection and traceability|外觀、X 光與機械測試互補，不能互相完全替代。|Visual, X-ray and mechanical tests complement rather than fully replace each other.|保存材料版次、曲線與檢验判據的交叉索引。|Index material revision, profile and acceptance criteria together.|外觀合格就等於全部長期可靠度合格。|Visual acceptance equals complete lifetime reliability acceptance.
''')

course(286,'三維量測、誤報與缺陷回饋','3D measurement, false calls and defect feedback',
'光學與資料|Optics and data;缺陷判別|Defect discrimination;量測能力|Metrology capability;回饋與治理|Feedback and governance',
'precision=TP/(TP+FP)；recall=TP/(TP+FN)。|Precision=TP/(TP+FP); recall=TP/(TP+FN).',
'假想 100 個真正缺陷中找出 95 個，另誤報 20 個：recall=95%，precision=95/115≈82.6%。',
'Of 100 hypothetical true defects, 95 are found with 20 false calls: recall=95%, precision=95/115≈82.6%.',
'需有獨立真值標記；不把此示例當任何檢測設備性能。','Requires independent ground truth; these values do not represent any inspection machine.',
'aoi aoi-loop euro-place','euro','a284 a287','kohyoung', '''
照明與反射|Lighting and reflection|金屬高反射使亮度不直接等於高度。|Specular metal brightness is not directly height.|比較多角度照明下同一焊點外觀。|Compare one joint under multiple illumination angles.|最亮的區域必然最高。|The brightest region must be highest.
三維重建|3D reconstruction|結構光或多視角高度需校準幾何，遮蔽會留缺測。|Structured-light or multiview height requires geometry calibration; occlusion leaves gaps.|標出重建置信度及無資料區域。|Mark reconstruction confidence and missing-data regions.|所有可見像素都自動具有可靠高度。|Every visible pixel automatically has reliable height.
座標配準|Registration|全板位置和局部翹曲需分離，否則偏移會被誤判。|Global pose and local warp need separation to avoid false offset calls.|先消除全局變換再看局部殘差。|Remove global transformation before examining local residuals.|板翹完全不會影響高度門檻。|Board warp cannot affect height thresholds.
缺件與錯件|Missing and wrong parts|外形辨識與料號辨識是不同任務。|Shape detection and part-number identification are different tasks.|將同封裝不同料號納入驗證集。|Include different part numbers sharing a package in validation.|輪廓相同就能排除所有錯料。|Identical outlines exclude all wrong components.
極性與文字|Polarity and text|OCR 與極性標記需搭配旋轉和反光容差。|OCR and polarity marks need rotation and glare tolerance.|檢查反轉、模糊與低對比樣本。|Check reversed, blurred and low-contrast samples.|讀得到文字就能保證元件方向正確。|Readable text guarantees correct orientation.
焊點形貌|Joint morphology|橋接、少錫與抬腳對高度和連通有不同特徵。|Bridges, insufficient solder and lifted leads have different height/connectivity features.|為三種缺陷分開定義量測證據。|Define separate evidence for three defect classes.|單一亮度門檻可無條件辨認所有焊接缺陷。|One brightness threshold identifies every solder defect unconditionally.
誤報與漏報|False calls and escapes|降低誤報可能增加漏報，需看完整混淆矩陣。|Reducing false calls can increase escapes; use the full confusion matrix.|掃描門檻並畫 precision-recall 取捨。|Sweep thresholds and plot precision-recall trade-offs.|零誤報就表示沒有漏檢。|Zero false calls means zero escapes.
量測重複性|Measurement repeatability|同件重掃與跨機台差異可超過決策餘裕。|Repeat scans and cross-machine differences can exceed decision margin.|對相同工件做重複掃描資料分析。|Analyze repeated scans of the same sample.|一次量得的高度就是毫無誤差真值。|One height reading is error-free ground truth.
真值建構|Ground truth|人工復判也可能不一致，需要獨立證據與衝突仲裁。|Human review can disagree and needs independent evidence and adjudication.|將有爭議案例交由截面或電測資料對照。|Compare disputed cases with sections or electrical evidence.|人工標籤永遠不需要品質審查。|Human labels never need quality review.
SPI 到 AOI|SPI-to-AOI correlation|同位置前後資料能找缺陷來源，但相關不等於因果。|Registered before/after data helps find origins, but correlation is not causation.|控制材料批次後再比較印刷與焊點關係。|Control material lot before comparing print and joint relationships.|有統計相關就可直接斷言根因。|Statistical correlation proves root cause directly.
模型漂移|Model drift|新料、光源老化與圖版改動可使既有模型失效。|New components, light aging and revisions can invalidate an existing model.|追蹤分布漂移並使用固定驗證集。|Track distribution shifts and use a fixed validation set.|訓練完成的模型永遠不需再驗證。|A trained model never needs revalidation.
生產回饋|Production feedback|自動回饋需限幅、版本與回滾，避免誤判放大製程偏移。|Automatic feedback needs limits, versions and rollback to avoid amplifying misclassification.|用回放資料驗證更新前後缺陷與誤報。|Replay data to compare defects and false calls before/after updates.|檢測器的任何建議都應立即無限幅套用。|Every inspection suggestion should be applied immediately without limits.
''')

course(287,'TAP 狀態、結構測試與覆蓋邊界','TAP states, structural tests and coverage limits',
'可測性資料|Testability data;掃描控制|Scan control;網路測試|Net testing;覆蓋與交付|Coverage and release',
'理想單次移位時間 t≈Nbits/fTCK；還需加入狀態切換。|Ideal shift time t≈Nbits/fTCK, plus state transitions.',
'假設總掃描鏈 1,200 bit、TCK=5 MHz，一次移位約 240 µs；100 個向量純移位時間約 24 ms。',
'For a 1,200-bit chain at 5 MHz TCK, one shift takes about 240 µs; 100 vectors require about 24 ms of shifting alone.',
'忽略 TAP 切換和等待；時鐘速率必須受所有鏈上元件規格限制。','Excludes TAP transitions and waits; clock rate must satisfy every device in the chain.',
'boundary boundary-standard euro-place','euro','a281 a286','keysight', '''
結構與功能|Structural versus functional|邊界掃描主要驗證可控制可觀察的連接，不等於完整功能測試。|Boundary scan verifies controllable/observable connections, not complete functional behavior.|把連通故障與演算法故障分開列表。|Separate interconnect and algorithmic faults.|邊界掃描通過就代表韌體所有功能正確。|Passing boundary scan proves all firmware functions.
BSDL 對應|BSDL matching|BSDL 必須對應器件、封裝與版次的掃描結構。|BSDL must match device, package and revision scan structure.|核對腳位映射、指令長度與 ID。|Check pin mapping, instruction length and ID.|相同系列的任意 BSDL 都可互換。|Any BSDL in a product family is interchangeable.
鏈路拓撲|Chain topology|TDI/TDO 順序和 bypass 路徑決定移位資料對齊。|TDI/TDO order and bypass paths determine data alignment.|將掃描鏈與原理圖逐器件對照。|Compare the chain with the schematic device by device.|交換兩器件順序不影響向量解讀。|Swapping device order does not affect vector interpretation.
TAP 狀態機|TAP state machine|TMS 在 TCK 邊緣控制狀態，移位與更新是不同動作。|TMS controls states at TCK edges; shifting and updating differ.|追蹤一段 TMS 序列的狀態路徑。|Trace the state path for a TMS sequence.|Shift-DR 的每一位都立即改變所有輸出腳。|Every Shift-DR bit immediately changes all outputs.
安全預載|Safe preload|測試前需要已知輸出和三態設定避免匯流排衝突。|Known output/tri-state settings are needed before tests to avoid contention.|在離線向量中檢查兩驅動器同時使能的組合。|Check offline vectors for simultaneous driver enables.|EXTEST 可忽略板上其他主動驅動器。|EXTEST can ignore other active board drivers.
指令範圍|Instruction scope|BYPASS、SAMPLE 與 EXTEST 使用的資料路徑和影響不同。|BYPASS, SAMPLE and EXTEST use different paths and effects.|對每指令列出哪些腳被觀察或控制。|List observed/controlled pins for each instruction.|所有 JTAG 指令都會強制改變外部腳位。|Every JTAG instruction forces external pin changes.
開短路向量|Open/short vectors|向量需使可疑網路產生可區分的響應。|Vectors must produce distinguishable responses for suspected nets.|比較單一固定值與 walking-pattern 的故障區別力。|Compare fixed values and walking patterns for fault discrimination.|全部腳都輸出零即可找出任何短路。|Driving every pin low detects any short.
非掃描元件|Non-scan devices|中間被動或非掃描元件可能降低控制觀察能力。|Passive and non-scan intermediate components can limit controllability/observability.|逐網路標示可觀察端點與盲區。|Mark observable endpoints and blind spots for each net.|只要兩端有 JTAG 就能看見所有類比特性。|JTAG at both ends reveals every analog property.
AC 耦合網路|AC-coupled nets|直流邊界測試與差動 AC 網路需不同測試能力。|DC boundary tests and differential AC networks require different capabilities.|查核器件是否支援適用擴充與向量方法。|Check support for applicable extensions and vector methods.|標準直流 EXTEST 可無條件測所有 AC 耦合鏈路。|DC EXTEST tests every AC-coupled link unconditionally.
時脈訊號完整性|TCK integrity|TCK 反射或偏斜可能使測試鏈誤移位。|TCK reflection or skew can cause scan-chain misalignment.|比較不同 TCK 速率下失敗位置是否改變。|Compare failure positions at different TCK rates.|鏈路錯位只能是邏輯向量錯誤。|Chain misalignment can only be a vector-logic error.
覆蓋指標|Coverage metrics|網路覆蓋、腳位覆蓋與故障覆蓋不是相同分母。|Net, pin and fault coverage use different denominators.|報告可測、不可測及部分可測網路。|Report testable, untestable and partially testable nets.|99% 腳位覆蓋就保證 99% 所有故障。|99% pin coverage guarantees 99% of all faults.
生產紀錄|Production records|BSDL、網表、向量與板版次需一同保存。|BSDL, netlist, vectors and board revision must be retained together.|重建一筆測試所用的完整版本集合。|Reconstruct all versions for one test record.|只存 PASS 字串就足以追溯任何失效。|Saving only PASS is sufficient for any failure trace.
''')

course(288,'帶電、放電路徑與防護稽核','charging, discharge paths and control audits',
'靜電機制|Electrostatic mechanisms;受控區域|Protected areas;材料與器件|Materials and devices;驗證與稽核|Verification and audits',
'Q=C·V；儲能 E=½CV²。|Q=C·V; stored energy E=½CV².',
'教學 C=100 pF、V=1 kV，Q=100 nC，E=50 µJ；這僅示範電容儲能，不是完整 ESD 波形。',
'For teaching C=100 pF and V=1 kV, Q=100 nC and E=50 µJ; this illustrates capacitor energy, not a complete ESD waveform.',
'集中電容近似；峰值電流還取決於放電路徑 R、L 和事件模型。','Lumped-capacitance approximation; peak current also depends on discharge-path R/L and event model.',
'esd esd-control euro-place','euro','a284 a289','ti', '''
摩擦帶電|Triboelectric charging|接觸分離可轉移電荷，材料及濕度影響程度。|Contact/separation transfers charge; materials and humidity influence magnitude.|比較相同動作在不同材料上的場強資料。|Compare field data for the same action on different materials.|沒有摩擦聲就不會產生靜電。|No audible rubbing means no static charge.
電容與電位|Capacitance and potential|相同電荷在不同電容上呈不同電壓。|Equal charge produces different voltage on different capacitance.|固定 Q 比較 V=Q/C 的兩種幾何。|Compare V=Q/C for two geometries at fixed Q.|帶電物體電壓不受周邊幾何影響。|Charged-object voltage is independent of geometry.
場感應|Field induction|外部帶電物可在孤立導體重分配電荷。|An external charged object redistributes charge in an isolated conductor.|画出靠近、接地、移走的概念電荷序列。|Draw conceptual charge states for approach, grounding and removal.|未直接接觸元件就不可能造成靜電風險。|No direct component contact means no electrostatic risk.
等電位與接地|Equipotential bonding|等電位可降低電位差，絕緣物無法像導體直接接地消荷。|Bonding reduces potential differences; insulators cannot discharge like grounded conductors.|將工作區物品分類為導電、耗散與絕緣。|Classify objects as conductive, dissipative or insulating.|把任何絕緣塑膠接地就能立即完全消荷。|Grounding any insulating plastic instantly removes all charge.
人員系統|Personnel system|鞋地板或腕帶效果取決於完整路徑，不是單一零件。|Footwear/floor or wrist-strap performance depends on the complete path.|檢查系統量測紀錄與失效處置。|Review system measurements and failure response records.|購買合格腕帶後永不需要定期檢查。|A qualified wrist strap never needs periodic checking.
離子中和|Ion neutralization|離子器用於無法接地的絕緣物，平衡和衰減時間都重要。|Ionizers address ungroundable insulators; balance and decay time both matter.|比较正負兩種初始電位的衰減紀錄。|Compare decay records from positive and negative initial voltages.|離子器只要有風就代表中和有效。|Airflow alone proves effective ion neutralization.
HBM 與 CDM|HBM and CDM|人體模型與器件帶電模型代表不同放電條件。|HBM and CDM represent different discharge conditions.|將分類電壓與各自模型配對，避免混比。|Pair ratings with their models and avoid mixing them.|相同 HBM 和 CDM 電壓代表相同波形。|Equal HBM and CDM voltage means identical waveforms.
器件與系統|Device versus system ESD|器件級耐受不能直接代替產品級端口試驗。|Device-level withstand cannot directly replace product-port testing.|分開記錄元件、組件與整機證據。|Record component, assembly and product evidence separately.|晶片 HBM 合格就證明整機所有端口免疫。|A chip passing HBM proves immunity at all product ports.
運送包裝|Transport packaging|低起電、耗散與屏蔽是不同功能，區域外運送需考慮外部放電。|Low charging, dissipation and shielding differ; transport outside EPA must address external discharge.|把包裝功能與運送路徑風險對照。|Match packaging functions with transport-path risks.|任何粉紅色塑膠袋都提供完整放電屏蔽。|Any pink plastic bag provides complete discharge shielding.
量測條件|Measurement conditions|電阻、場強與衰減測試需指定幾何、接觸和環境。|Resistance, field and decay tests need geometry, contact and environment conditions.|核對量測方法及儀器校準，避免混用單位。|Check method/calibration and avoid mixing units.|場強讀值可無幾何條件直接當電荷量。|Field strength directly gives charge without geometry.
潛在損傷|Latent damage|功能初測通過不排除漏電增加或可靠度退化。|Passing initial function does not exclude increased leakage or reliability degradation.|比较處理前後漏電和長期資料。|Compare leakage and longer-term records before/after handling.|ESD 損傷一定立即造成完全不工作。|ESD damage always immediately causes total failure.
稽核閉環|Audit loop|控制方案需訓練、量測、例外與改正追溯。|Control programs need training, measurements, exceptions and corrective traceability.|以一個失效檢查結果追蹤隔離和改正。|Trace containment/correction from one failed check.|牆上貼有 ESD 標誌就等同完整控制方案。|An ESD wall sign equals a complete control program.
''')

course(289,'任務剖面、加速模型與失效分析','mission profiles, acceleration models and failure analysis',
'需求與機制|Requirements and mechanisms;環境應力|Environmental stresses;加速與樣本|Acceleration and samples;失效與放行|Failure and release',
'Arrhenius AF=exp[(Ea/k)(1/Tuse−1/Tstress)]；溫度用 K。|Arrhenius AF=exp[(Ea/k)(1/Tuse−1/Tstress)]; use kelvin.',
'假設 Ea=0.7 eV、使用 85°C、應力 125°C，k=8.617×10⁻⁵ eV/K，AF≈9.8；僅對相同主導機制的模型成立。',
'Assuming Ea=0.7 eV, use at 85°C, stress at 125°C and k=8.617×10⁻⁵ eV/K gives AF≈9.8, only for the same dominant mechanism.',
'示例 Ea 並非通用常數；不可把此倍率直接轉成汽車電子壽命保證。','Example Ea is not universal; do not turn this factor directly into an automotive lifetime guarantee.',
'auto auto-report euro-place','euro','a269 a285','renesas', '''
任務剖面|Mission profile|通電時間、溫度分布與停機環境共同決定應力。|Powered time, temperature distribution and storage environment determine stress.|把產品一年假想使用拆成各溫度停留時間。|Break a hypothetical year into temperature/dwell intervals.|只知道最高環境溫度就足够估計所有壽命。|Maximum ambient temperature alone predicts all life.
元件與整機|Component versus product|AEC 元件資格與整車或 ECU 的驗證範圍不同。|AEC component qualification differs from vehicle/ECU validation scope.|列出元件證據未覆蓋的連接器、板材和軟體。|List connectors, boards and software not covered by component evidence.|AEC-Q100 元件自動使整個 ECU 認證通過。|AEC-Q100 parts automatically certify a complete ECU.
機制選擇|Mechanism selection|腐蝕、焊點疲勞和介電退化需要不同應力模型。|Corrosion, joint fatigue and dielectric degradation need different models.|為每種失效指定可區分的觀測量。|Assign a discriminating observable to each failure type.|所有可靠度都能用一個溫度加速公式描述。|One thermal acceleration formula describes all reliability.
溫度循環|Temperature cycling|循環幅度、停留和升降速率影響熱機械應變。|Swing, dwell and ramp rate affect thermomechanical strain.|比较相同最高温但不同幅度的剖面。|Compare equal maxima with different temperature swings.|相同最高温度代表相同疲勞應力。|Equal maximum temperature means equal fatigue stress.
濕度與偏壓|Humidity and bias|水氣、離子污染與電場可促進不同電化學失效。|Moisture, ionic contamination and fields can drive electrochemical failures.|分開比較有無偏壓下漏電和腐蝕形貌。|Compare leakage/corrosion with and without bias.|濕度試驗是否通電完全不影響失效機制。|Bias has no effect on humidity-test mechanisms.
振動與共振|Vibration and resonance|輸入加速度與板上應變由固定和共振共同決定。|Mounting and resonances link input acceleration to board strain.|比較掃頻響應峰與固定位置。|Compare response peaks and mounting positions.|外殼相同加速度保證所有焊點相同應力。|Equal case acceleration guarantees equal joint stress.
加速模型|Acceleration models|過高應力可能引入使用中不存在的新機制。|Excess stress can introduce mechanisms absent in service.|比較加速前後破壞形貌確認機制一致。|Compare failure morphology to check mechanism consistency.|應力越高就永遠越能正確預測正常壽命。|Higher stress always predicts normal life more accurately.
樣本與信心|Samples and confidence|零失效不是零失效率，樣本和時間限定信心。|Zero observed failures is not zero failure rate; sample/time limit confidence.|寫出樣本數、停止規則與未發現失效的界限。|Record sample count, stopping rule and limits of zero-failure evidence.|十個樣本沒壞就證明全產品永不失效。|Ten passing samples prove all products never fail.
量測節點|Read points|中途量測能看到參數漂移，只有終點可能漏掉暫態。|Interim reads reveal drift; endpoint-only checks can miss transient failures.|比較漏電、電阻、功能三種時間趨勢。|Compare leakage, resistance and functional trends over time.|測試末端功能正常就表示中途從未失效。|Normal final function proves no failure occurred during testing.
失效分析|Failure analysis|先保留失效現象再做破壞性分析，避免證據被移除。|Preserve symptoms before destructive analysis to avoid losing evidence.|安排非破壞與截面分析的證據順序。|Order nondestructive and sectional evidence collection.|任何失效都應先拆到最小零件再記錄。|Every failure should be fully dismantled before recording.
變更重驗|Change requalification|材料、製程和廠址改變可能改變失效機制。|Material, process and site changes can alter failure mechanisms.|對變更項目做影響矩陣和重驗理由。|Create an impact matrix and requalification rationale.|料號未變就永遠不需要重新驗證。|An unchanged part number never needs requalification.
放行主張|Release claims|驗證報告須限定產品版次、應力和觀察範圍。|Reports must bound product revision, stresses and observations.|分開列已證明、未覆蓋與待追蹤項目。|Separate demonstrated, uncovered and follow-up items.|一份通過報告可適用所有未來修改版本。|One passing report applies to all future revisions.
''')

course(290,'隔離屏障、漏電與系統安全證據','isolation barriers, leakage and system safety evidence',
'使用情境|Use context;隔離與功率|Isolation and power;寄生與性能|Parasitics and performance;驗證與文件|Validation and records',
'電容正弦電流 Irms=2πfCVrms。|Sinusoidal capacitive current Irms=2πfCVrms.',
'假設隔離電容 100 pF、230 Vrms、50 Hz，理想電容電流約 7.23 µA；它不是完整產品患者漏電結果。',
'For 100 pF across 230 Vrms at 50 Hz, ideal capacitive current is about 7.23 µA; this is not a complete product patient-leakage result.',
'單一理想電容與正弦電压；實際測試需適用標準、設備分類與合格實驗室。','One ideal capacitor and sinusoidal voltage; actual testing needs applicable standards, equipment classification and a qualified lab.',
'medical isolation ti-place','ti','a297 a270','ti', '''
設備與患者界面|Equipment and patient interface|隔離要求取決於使用情境及患者連接，不能只看電源瓦數。|Isolation depends on use and patient connection, not merely supply wattage.|畫出患者、操作者、外接設備與市電邊界。|Map patient, operator, peripherals and mains boundaries.|低功率醫療設備自然不需隔離分析。|Low-power medical equipment needs no isolation analysis.
保護措施|Means of protection|操作人員與患者保護概念不同，必須使用適用分類。|Operator and patient protection concepts differ and require applicable classifications.|從官方文件建立分類問題清單交由合格評估。|Build a classification checklist from official documentation for qualified review.|所有隔離額定都自動等於患者保護。|Every isolation rating automatically equals patient protection.
系統屏障|System barrier|電源、資料、屏蔽和接地都可能跨越屏障。|Power, data, shields and grounds can all cross the barrier.|逐條標記跨屏障路徑和寄生電容。|Mark every barrier-crossing path and capacitance.|只隔離電源就保證整個系統完全隔離。|Isolating power alone fully isolates the system.
變壓器耦合|Transformer coupling|磁耦合傳輸能量，繞組間仍有寄生電容。|Magnetic coupling transfers energy while interwinding capacitance remains.|比較能量路徑和共模位移電流路徑。|Compare energy and common-mode displacement-current paths.|變壓器兩側之間沒有任何高頻耦合。|There is no high-frequency coupling across a transformer.
間距概念|Spacing concepts|爬電沿表面、電氣間隙穿空氣，材料和環境影響要求。|Creepage follows surfaces; clearance crosses air; material/environment affect requirements.|在概念板圖分別畫最短表面與空氣路徑。|Draw shortest surface and air paths on a conceptual board.|爬電距離與空氣間隙總是同一條路徑。|Creepage and clearance always follow the same path.
耐壓與工作電壓|Withstand versus working voltage|短時間耐壓值不等於可長期施加的工作電壓。|Short-duration withstand is not continuous working voltage.|把資料表耐壓、工作與突波額定分欄。|Separate withstand, working and surge ratings.|通過高壓一分鐘就可終生使用相同電壓。|Passing one minute at high voltage permits lifetime operation there.
漏電路徑|Leakage paths|多個電容與附件可使系統漏電不同於單一電源。|Multiple capacitors and accessories make system leakage differ from one supply.|對照最終配置中的所有跨屏障路徑。|Check all crossing paths in the final configuration.|電源模組漏電低就保證所有附件組合都低。|Low module leakage guarantees every accessory configuration is low.
調節與負載|Regulation and load|隔離回授與負載變化影響穩定和供電準確。|Isolated feedback and load variation affect stability and supply accuracy.|比較開環、閉環及最小負載的概念響應。|Compare conceptual open/closed-loop and minimum-load responses.|隔離本身可保證完美穩壓。|Isolation itself guarantees perfect regulation.
低雜訊供電|Low-noise supply|開關紋波和共模干擾可能進入敏感感測前端。|Switching ripple and common-mode interference can enter sensitive front ends.|分開電源頻譜與生理訊號帶內雜訊預算。|Separate supply spectrum and sensing-band noise budgets.|符合隔離要求就代表訊號完全沒有電源噪聲。|Meeting isolation requirements means no supply noise in signals.
單一故障分析|Single-fault analysis|安全判斷需要指定故障情境，而非只看正常工作。|Safety assessment needs specified fault cases, not only normal operation.|在文件中分析一條屏障或保護失效的影響。|Analyze a barrier/protection failure in documentation.|正常模式量測合格等於所有故障模式安全。|Normal-mode passing means every fault mode is safe.
整機測試|Equipment testing|模組證書支援整機評估，但不能替代最終產品測試。|Module certification supports but does not replace final equipment assessment.|建立模組證据與整機待驗項目對應。|Map module evidence to remaining equipment tests.|使用有證書模組便不需整機驗證。|Certified modules eliminate equipment validation.
風險與版本|Risk and versions|使用限制、變更和殘餘風險需與工程記錄連結。|Use limits, changes and residual risk need linked engineering records.|保存適用標準版本、分類與評估負責人角色。|Retain standard revision, classification and assessor roles.|相同外殼產品改資料介面不影響隔離風險。|Changing a data port cannot affect isolation risk if the case is unchanged.
''')

course(291,'恆流、調光與熱光耦合','constant current, dimming and electrothermal coupling',
'光電需求|Optical/electrical needs;功率與恆流|Power and current;調光與故障|Dimming and faults;熱與驗證|Heat and validation',
'Iset≈Vsense/Rsense；線性調節器損耗 P≈(Vin−VLED)I。|Iset≈Vsense/Rsense; linear-regulator loss P≈(Vin−VLED)I.',
'教學感測基準 0.10 V、電阻 0.286 Ω，電流約 0.350 A；電阻耗散約 0.035 W，仍須查容差和降額。',
'For an assumed 0.10 V sense reference and 0.286 Ω resistor, current is about 0.350 A; resistor dissipation is about 0.035 W, before tolerance/derating checks.',
'理想穩態恆流近似；實際基準、峰值／平均控制定義依器件資料表。','Ideal steady current approximation; actual reference and peak/average control depend on the device.',
'led led-driver ti-place','ti','a269 a266','ti', '''
電流與光通|Current and flux|LED 光輸出受電流、溫度與器件差異共同影響。|LED light output depends on current, temperature and device variation.|比較相同電流不同溫度的假想光通曲線。|Compare hypothetical flux curves at equal current and different temperatures.|相同電流永遠代表相同光通量。|Equal current always means equal luminous flux.
串並聯配置|Series/parallel strings|串聯共用電流，並聯可能因正向壓降差而分流不均。|Series LEDs share current; parallel strings may split unevenly due to forward-voltage variation.|對两串不同 Vf 建立電流分配模型。|Model current sharing between two strings with different Vf.|直接並聯 LED 永遠自動均流。|Directly paralleled LEDs always share evenly.
順向壓降|Forward voltage|冷態和熱態 Vf 影響驅動餘裕和耗散。|Cold/hot Vf affects headroom and dissipation.|以最低和最高串壓檢查供電範圍。|Check supply range against minimum/maximum string voltage.|只看典型 Vf 就足以定義所有工作條件。|Typical Vf alone defines all operating conditions.
拓撲選擇|Topology selection|buck、boost 與 buck-boost 的可調電壓區不同。|Buck, boost and buck-boost have different regulation regions.|比較輸入範圍和串壓範圍是否交疊。|Compare overlap of input and string-voltage ranges.|升壓拓撲可無條件穩壓到低於輸入。|Boost topology regulates below input unconditionally.
電流感測|Current sensing|感測電阻容差、熱漂與走線壓降影響電流。|Sense tolerance, drift and trace drops affect current.|對照 Kelvin 感測與共同回流的誤差。|Compare Kelvin sensing and shared-return error.|只要電阻標稱相同電流就絕對相同。|Equal nominal resistors give exactly equal current.
控制迴路|Control loop|LED 動態阻抗與輸出電容改變迴路響應。|LED dynamic resistance and output capacitance change loop response.|在模擬中檢查負載階躍與輸入改變。|Check load-step and input-change responses in simulation.|恆流控制不需要任何穩定性分析。|Constant-current control needs no stability analysis.
PWM 調光|PWM dimming|PWM 改平均亮度但峰值電流和邊緣仍影響熱和噪聲。|PWM changes average brightness while peak current/edges affect heat and noise.|比較相同平均電流不同占空比的峰值。|Compare peaks at equal average current and different duty cycles.|低占空比就允許無限制峰值電流。|Low duty cycle permits unlimited peak current.
類比調光|Analog dimming|改電流可改光色與低電流精度，不等於 PWM 的完全替代。|Changing current can affect color and low-current accuracy; it is not identical to PWM.|比較兩種調光在低亮度的色度與線性。|Compare chromaticity/linearity at low brightness.|所有調光方式具有完全相同光色。|All dimming methods have identical color.
開短路診斷|Open/short diagnosis|開路可使輸出上升，短路改變串壓和熱分配。|An open can raise output voltage; a short changes string voltage and heat distribution.|在模型中分開觀察開路、短路和供電不足。|Distinguish open, short and undervoltage in a model.|所有熄燈都必然是 LED 開路。|Every dark LED must be open-circuit.
結溫與散熱|Junction temperature|電能中未轉成光的部分變熱，光效隨溫度變化。|Electrical energy not emitted as light becomes heat; efficacy varies with temperature.|閉合輸入、光功率和熱的能量帳。|Close the electrical, optical and heat balance.|全部輸入瓦數都變成可見光。|All input watts become visible light.
閃爍與頻譜|Flicker and spectrum|低頻紋波與 PWM 會造成不同時間調變特徵。|Low-frequency ripple and PWM create different temporal-modulation features.|分析亮度時域及頻谱，而非只量平均光通。|Analyze light waveforms/spectra rather than mean flux alone.|平均亮度相同代表完全相同閃爍。|Equal mean brightness means identical flicker.
壽命與驗收|Life and acceptance|流明維持與驅動可靠度是不同驗證項。|Lumen maintenance and driver reliability require separate validation.|記錄環境、結溫估計、電流與光輸出隨時間變化。|Record environment, junction estimate, current and light versus time.|LED 額定壽命自動等於整盞燈壽命。|LED-rated life automatically equals luminaire life.
''')

course(292,'電泳、雙穩態與更新波形','electrophoresis, bistability and update waveforms',
'顯示原理|Display principles;驅動與更新|Drive and update;影像與溫度|Image and temperature;耗能與驗收|Energy and acceptance',
'Eupdate=∫V(t)I(t)dt；Pavg≈Eupdate·update rate+Pidle。|Eupdate=∫V(t)I(t)dt; Pavg≈Eupdate·update rate+Pidle.',
'假設每次更新 0.20 J、每分鐘一次，平均更新功率約 3.33 mW；若其餘電路待機 1 mW，總平均約 4.33 mW。',
'At an assumed 0.20 J/update and one update/minute, average update power is about 3.33 mW; adding 1 mW electronics standby gives about 4.33 mW.',
'能量為假設，需按實際顯示尺寸、內容、波形與溫度量測；雙穩態不表示整機零待機。','Assumed energy; measure actual size, content, waveform and temperature. Bistability does not imply zero whole-device standby.',
'epaper epaper-faq eink-place','eink','a293 a294','eink', '''
電泳粒子|Electrophoretic particles|電場推動帶電顏料改變可見反射狀態，粒子配置依平台不同。|Electric fields move charged pigments to change reflection; particle arrangements vary by platform.|畫出兩種極性電場下的概念粒子分布。|Draw conceptual particle distributions under opposite fields.|電子紙必須以背光讓每個像素發光。|Electronic paper requires a backlight to make each pixel emit.
雙穩態|Bistability|部分電子紙可在移除驅動後保留影像，周邊電路仍可能耗電。|Some e-paper retains images after drive removal while peripheral circuitry may consume power.|分開量測顯示更新和控制器待機。|Measure display-update and controller-standby energy separately.|雙穩態代表整個裝置永遠不耗電。|Bistability means the entire device never consumes energy.
TFT 定址|TFT addressing|列掃描與像素電極把更新電壓分配到指定像素。|Row scanning and pixel electrodes distribute update voltages to selected pixels.|畫出行列、像素儲存與時序的關係。|Map rows, columns, pixel storage and timing.|每個像素都可完全忽略列掃描時序。|Every pixel can ignore row-scan timing.
驅動電源|Drive supplies|多電位驅動需要正確上電順序和器件特定限制。|Multilevel driving needs correct sequencing and device-specific limits.|依公開模組資料畫狀態順序，不任意指定電壓。|Draw states from public module documentation without inventing voltages.|所有電子紙模組可共用相同驅動電壓。|All e-paper modules use identical drive voltages.
波形查表|Waveform tables|灰階與轉態依前後狀態、溫度及材料波形表。|Grayscale/transitions depend on old/new state, temperature and material waveform tables.|把舊像素值和新像素值列成轉態矩陣。|Build an old/new pixel-state transition matrix.|只知道目標灰階就能決定所有脈衝。|Target grayscale alone determines every pulse.
局部與全更|Partial and full update|局部更新降低某些工作量，但歷史殘影可能需要全更管理。|Partial update can reduce work, but ghost history may need full-update management.|比較相同圖案多次局更和一次全更後的殘差。|Compare residuals after repeated partial and one full update.|局部更新與全更新永遠有相同影像品質。|Partial and full updates always have identical quality.
溫度依賴|Temperature dependence|流體和粒子運動隨溫度改變，更新時間不可固定套用。|Fluid/particle motion changes with temperature; update time is not universally fixed.|使用溫度分箱比較轉態曲線。|Compare transition curves by temperature bins.|室溫波形能無條件套用所有低溫情境。|Room-temperature waveforms apply unconditionally at all low temperatures.
殘影|Ghosting|先前像素狀態與更新歷史可影響當前反射。|Previous states and update history can affect current reflectance.|用棋盤、全白與文字序列區分歷史效應。|Use checkerboard, white and text sequences to identify history effects.|相同最終圖檔保證完全相同反射分布。|Identical final image files guarantee identical reflectance.
灰階與抖色|Grayscale and dithering|空間抖色與實體灰階不同，觀察距離影響感受。|Spatial dithering differs from physical grayscale; viewing distance matters.|比較相同平均反射的棋盤與均勻灰。|Compare checkerboard and uniform gray at equal mean reflectance.|抖色像素本身一定具有中間灰階。|Dithered pixels themselves necessarily have intermediate gray.
反射量測|Reflectance measurement|環境照明與角度影響閱讀對比，不能用發光亮度概念直接替代。|Illumination/angle affect readable contrast; emissive luminance concepts cannot directly substitute.|固定照明幾何比較黑白反射比。|Compare black/white reflectance at fixed illumination geometry.|黑暗中反射式顯示會自行產生同樣亮度。|Reflective displays produce equal brightness by themselves in darkness.
能量預算|Energy budget|更新頻率、無線傳輸和待機共同决定電池壽命。|Update rate, radio transfer and standby jointly determine battery life.|分開列出每次更新能量與每日固定耗能。|Separate per-update energy and daily fixed consumption.|顯示雙穩態使無線通訊耗能可以忽略。|Display bistability makes radio energy negligible.
模組相容|Module compatibility|尺寸相同不代表驅動、波形或接腳相容。|Equal size does not imply driver, waveform or pin compatibility.|核對料號、控制器、波形版本與溫度範圍。|Check part, controller, waveform revision and temperature range.|同解析度模組必可直接互換。|Equal-resolution modules are necessarily interchangeable.
''')

course(293,'自發光像素、供電與顯示補償','emissive pixels, power and display compensation',
'像素與面板|Pixels and panel;驅動與傳輸|Drive and transport;光學與熱|Optics and heat;壽命與驗收|Life and validation',
'未壓縮有效畫面資料率=NxNy·fps·bits/pixel，尚未含消隱或傳輸開銷。|Uncompressed active-pixel rate=NxNy·fps·bits/pixel, before blanking/transport overhead.',
'教學 1920×1080、60 fps、24 bit/pixel，有效畫面資料率約 2.986 Gbit/s；實際介面需求還需額外開銷。',
'For 1920×1080 at 60 fps and 24 bits/pixel, active-image data rate is about 2.986 Gbit/s; real interfaces need additional overhead.',
'未壓縮 RGB 示例；實際面板可能壓縮、變動刷新或不同子像素排列。','Uncompressed RGB example; panels may use compression, variable refresh or different subpixel arrangements.',
'oled oled-place','samsung','a292 a291','samsung', '''
自發光結構|Emissive structure|OLED 以有機層中的電荷注入和復合產光，不需 LCD 式背光。|OLED produces light through charge injection/recombination in organic layers, without an LCD backlight.|畫出電極、發光層和封裝的概念剖面。|Draw an electrode/emitter/encapsulation section.|OLED 的黑畫面仍必須由背光透過液晶形成。|OLED black necessarily comes from a backlight through liquid crystal.
主動矩陣|Active matrix|TFT 像素電路控制電流，器件差異影響均勻性。|TFT pixel circuits control current; variation affects uniformity.|比較相同資料值、不同驅動 TFT 偏移。|Compare equal code with different drive-TFT offset.|相同碼值必然使所有像素電流完全相同。|Equal code necessarily gives exactly equal current in every pixel.
子像素映射|Subpixel mapping|RGB 排列與子像素幾何影響渲染和視覺細節。|RGB arrangement and geometry affect rendering/detail.|對照邏輯像素與實體子像素。|Map logical pixels to physical subpixels.|所有 OLED 必有相同 RGB 條紋排列。|All OLEDs have the same RGB stripe layout.
供電排序|Power sequencing|面板電源、控制訊號與復位需依模組規定協調。|Panel rails, control signals and reset need module-specific coordination.|由公開模組規格建立狀態圖，不猜測電壓。|Build a state diagram from public module specifications, without guessing voltage.|任何 OLED 面板可共用相同上電時序。|Any OLED panel uses the same power sequence.
資料介面|Data interface|畫面位元率不是實體串列線速率，需算編碼和消隱。|Image bit rate is not physical line rate; include coding and blanking.|建立像素率到每通道線速率的換算。|Convert pixel rate to per-lane line rate.|有效畫面資料率就是全部介面需求。|Active-image data rate is the entire interface requirement.
刷新與保持|Refresh and hold|刷新率與發光時間控制影響動態清晰度和閃爍。|Refresh and emission timing affect motion clarity and flicker.|比較相同刷新率、不同發光占空的時序。|Compare different emission duty cycles at equal refresh.|刷新率相同就表示完全相同動態顯示效果。|Equal refresh means identical motion presentation.
色彩校準|Color calibration|碼值、電流和亮度不必線性，需定義白點與轉移函數。|Code, current and luminance need not be linear; define white point and transfer function.|用未參與擬合色塊檢查校準誤差。|Check calibration with unfitted color patches.|三色碼值相同就保證任何面板都是標準白。|Equal RGB codes guarantee standard white on every panel.
亮度與功耗|Brightness and power|自發光顯示功耗依畫面內容及亮度分布改變。|Emissive-display power varies with image content and luminance distribution.|比較同峰值亮度的全白和小白窗。|Compare full white and a small white window at equal peak luminance.|OLED 功耗只由解析度决定。|OLED power depends only on resolution.
熱均勻|Thermal uniformity|區域溫度可影響發光效率、壽命與補償。|Local temperature affects efficacy, life and compensation.|疊合長時間圖案的熱圖與亮度圖。|Overlay thermal and luminance maps after sustained patterns.|顯示模組不需要考慮局部熱點。|Display modules need no local-hotspot analysis.
差異老化|Differential aging|不同像素使用歷程可造成不均勻老化。|Different usage histories can cause differential aging.|比較靜態標誌與輪替圖案的累積負載。|Compare accumulated load of static logos and rotating images.|自發光像素永遠不會隨使用退化。|Emissive pixels never degrade with use.
補償與限制|Compensation and limits|補償可改善均勻性但受量測、電流和老化範圍限制。|Compensation improves uniformity within sensing/current/aging limits.|區分補償前後資料和不可恢復的老化。|Separate before/after compensation from irreversible degradation.|補償可無限制恢复所有材料老化。|Compensation reverses all material aging without limit.
模組驗收|Module acceptance|色彩、均勻性、缺陷和時間行為需分項判據。|Color, uniformity, defects and temporal behavior need separate criteria.|記錄亮度設定、圖案、溫度及量測幾何。|Record brightness, pattern, temperature and measurement geometry.|一張漂亮照片即可證明顯示所有性能。|One attractive photo proves every display metric.
''')

course(294,'自容、互容與抗干擾判讀','self/mutual capacitance and interference discrimination',
'電場與電極|Fields and electrodes;掃描與基線|Scanning and baseline;干擾與水滴|Interference and water;辨識與驗收|Recognition and validation',
'Q=C·V；簡化 SNR=touch delta/RMS noise。|Q=C·V; simplified SNR=touch delta/RMS noise.',
'假想觸摸差值 120 count、未觸摸 RMS 雜訊 10 count，SNR=12（約 21.6 dB）；仍需指定頻寬與資料窗。',
'Assumed touch delta 120 counts and untouched RMS noise 10 counts give SNR=12, about 21.6 dB; bandwidth and record window still need definition.',
'控制器計數只是相對量，不能跨裝置直接當皮法；範例不是辨識門檻。','Controller counts are relative and not directly picofarads across devices; this example is not a detection threshold.',
'touch touch-sdk inf-place','infineon','a292 a297','infineon', '''
自電容|Self capacitance|自容感測觀察電極對環境的電容改變。|Self-capacitance senses electrode-to-environment change.|畫出手指、地與電極的等效電容。|Draw finger/ground/electrode capacitances.|自容測量完全不受使用者接地狀態影響。|Self capacitance is unaffected by user grounding.
互電容|Mutual capacitance|互容觀察 Tx 與 Rx 之間耦合，與自容方向不必相同。|Mutual sensing observes Tx/Rx coupling; change need not match self-capacitance direction.|比較手指介入前後場線和耦合。|Compare fields/coupling before and after touch.|觸摸一定讓任何感測法的原始值增加。|Touch necessarily increases every sensing method's raw value.
覆蓋層|Overlay|厚度、介電常數和空隙影響手指耦合。|Thickness, permittivity and gaps affect finger coupling.|比較固定電極在不同覆蓋層的差值。|Compare touch delta for one electrode under different overlays.|所有玻璃厚度都有相同靈敏度。|All glass thicknesses give equal sensitivity.
寄生電容|Parasitics|長走線和邻近接地增加背景電容或耦合。|Long traces and nearby grounds add background capacitance/coupling.|對照不同走線長度的基線與噪聲。|Compare baseline/noise for different trace lengths.|電極外的走線永遠不參與感測。|Routing outside the electrode never participates in sensing.
掃描整合|Scan integration|較長整合可能降低雜訊但增加延遲與耗能。|Longer integration can reduce noise but increases latency/energy.|比較三種掃描時間的 SNR 和回應延遲。|Compare SNR/latency at three scan durations.|增加整合時間沒有延遲代價。|Longer integration has no latency cost.
基線追蹤|Baseline tracking|基線需追慢漂移但避免把持續觸摸吞掉。|Baseline tracking should follow slow drift without absorbing sustained touch.|比較慢溫漂與長按兩種時間序列。|Compare slow thermal drift and long-press records.|任何原始值變化都應立即寫成新基線。|Every raw change should instantly become a new baseline.
門檻與遲滯|Threshold and hysteresis|不同按下釋放門檻可降低閾值附近抖動。|Different press/release thresholds reduce chatter near a boundary.|給定接近閾值的雜訊序列計算狀態轉換。|Compute state transitions for noisy near-threshold data.|按下和釋放門檻必須永遠完全相同。|Press and release thresholds must always be identical.
水滴判別|Water discrimination|導電液體可橋接電極或改變場分布，不能視為普通手指。|Conductive liquid can bridge electrodes/change fields and is not simply a finger.|比較滴水、流水與手指的多電極空間模式。|Compare droplet, stream and finger spatial patterns.|任何電容變化都等同使用者按下。|Every capacitance change means a user press.
抗擾與頻率|Interference and frequency|充電器與顯示驅動噪聲可接近掃描頻率。|Charger/display noise may lie near scan frequencies.|比較有無噪聲源和不同掃頻的計數頻譜。|Compare count spectra with/without noise and at different scan rates.|差值大就可忽略全部頻域干擾。|A large delta permits ignoring all spectral interference.
多點辨識|Multi-touch|感測矩陣的幽靈點和鄰近觸摸需以空間資料處理。|Ghost points and nearby touches require spatial matrix analysis.|比較單指和雙指原始矩陣而非只看最後座標。|Compare raw single-/dual-touch matrices, not only coordinates.|輸出兩個座標就證明任何雙指都可分辨。|Two output coordinates prove every pair of touches is distinguishable.
低功耗喚醒|Low-power wake|低功耗掃描與完整追蹤有不同延遲和誤觸取捨。|Low-power scanning and full tracking trade latency and false triggers differently.|計算待機掃描間隔對最差喚醒時間的影響。|Calculate worst wake latency from standby scan interval.|降低掃描頻率不會影響使用者感受。|Lower scan rate cannot affect user experience.
情境驗收|Use-case acceptance|手套、濕手、充電與環境漂移需代表性樣本。|Gloves, wet fingers, charging and drift need representative samples.|建立誤觸、漏觸與延遲的情境矩陣。|Build a case matrix of false touches, misses and latency.|單一乾燥裸指測試代表所有操作條件。|One dry bare-finger test represents all use conditions.
''')

course(295,'電容負載、機械共振與位移回授','capacitive loading, mechanical resonance and displacement feedback',
'壓電與負載|Piezoelectric load;驅動與能量|Drive and energy;動態與回授|Dynamics and feedback;驗證與保護|Validation and protection',
'電容正弦峰值電流 Ipk=2πfC·Vpk；儲能 E=½CV²。|Capacitive sine peak current Ipk=2πfC·Vpk; stored energy E=½CV².',
'假設 C=1 µF、f=1 kHz、Vpk=10 V，Ipk≈62.8 mA；這只是電容電流，未包含機械負載。',
'For C=1 µF, f=1 kHz and Vpk=10 V, Ipk≈62.8 mA; this is capacitive current only, excluding mechanical load.',
'小訊號線性電容近似；真實壓電電容、位移與耗損隨偏壓和頻率變化。','Small-signal linear-capacitance approximation; actual capacitance, displacement and loss vary with bias/frequency.',
'piezo piezo-position piezo-force ultrasound-tuning ti-place','ti','a296 a256','ti', '''
壓電轉換|Piezoelectric conversion|電場引起應變，方向和材料極化決定位移。|Electric field creates strain; direction and polarization determine displacement.|標記極化方向、施力和位移座標。|Mark polarization, force and displacement coordinates.|任何方向的電場都產生相同位移。|Fields in all directions cause identical displacement.
自由行程與阻擋力|Free stroke and blocked force|無負載行程與阻擋力是負載線的不同端點。|Free stroke and blocked force are different load-line endpoints.|畫出致動器與負載剛度的交點。|Draw the intersection of actuator and load stiffness.|可同時取得完整自由行程和完整阻擋力。|Full free stroke and full blocked force occur simultaneously.
電容模型|Capacitive model|離機械共振較遠時可用電容近似，近共振需運動支路。|A capacitance approximation works away from resonance; near resonance needs a motional branch.|比較純 C 與 BVD 模型的阻抗掃頻。|Compare pure-C and BVD impedance sweeps.|壓電致動器在任何頻率都只是理想電容。|A piezo actuator is an ideal capacitor at every frequency.
電流需求|Current demand|電流與電壓变化率成正比，方波邊緣可要求高瞬時電流。|Current follows voltage slew rate; square-wave edges can demand high transient current.|對相同幅度比較正弦和有限斜率階躍。|Compare a sine and slew-limited step of equal amplitude.|只按平均功率選驅動器就足够。|Average power alone is enough to select a driver.
能量回收|Energy recovery|容性負載存放能量，驅動拓撲决定返回或耗散。|A capacitive load stores energy; topology determines recovery or dissipation.|比較充放電一週期的來源與負載能量。|Compare source/load energy over a charge/discharge cycle.|電容放電的能量必然全部回到電源。|All discharged energy necessarily returns to the supply.
電壓與極化限制|Voltage and polarization limits|反向電場、溫度和機械載荷可能改變極化與壽命。|Reverse field, temperature and mechanical load can affect polarization/life.|依材料公開額定建立界限表，不任意給高壓指令。|Build bounds from published ratings without inventing high-voltage commands.|任何壓電材料都允許無限制雙極驅動。|Any piezo material permits unlimited bipolar drive.
遲滯|Hysteresis|同一電壓在升降掃描可能對應不同位移。|One voltage can produce different displacement on rising/falling sweeps.|繪出電壓位移閉合迴線。|Plot a voltage/displacement hysteresis loop.|開環電壓與位移永遠一對一。|Open-loop voltage and displacement are always one-to-one.
蠕變|Creep|階躍後位移可持續緩慢改變，不能只量立即反應。|Displacement can drift after a step; immediate response is insufficient.|使用對數時間軸比較短期和長期位移。|Compare short/long-term displacement on a logarithmic time axis.|電壓維持不變就保證位移完全不變。|Constant voltage guarantees constant displacement.
機械共振|Mechanical resonance|負載質量和固定條件改變共振與可控頻寬。|Load mass and mounting change resonance and usable control bandwidth.|比較空載與負載的頻率響應。|Compare unloaded and loaded frequency responses.|資料表空載共振適用任何安裝負載。|Unloaded resonance applies to every mounted load.
位移回授|Displacement feedback|感測器帶寬、噪聲與延遲限制閉迴路改善。|Sensor bandwidth, noise and delay limit closed-loop improvement.|在模型加入量測延遲檢查相位餘裕。|Add measurement delay and check phase margin.|提高回授增益總能無限制提升定位精度。|Increasing feedback gain improves precision without limit.
熱與損耗|Heat and loss|介電損耗和驅動器耗散隨頻率及幅度變化。|Dielectric loss and driver dissipation vary with frequency/amplitude.|比較電容無功電流與實際輸入實功率。|Compare reactive current and measured real input power.|容性負載完全不產生任何實功耗。|A capacitive load never dissipates real power.
負載驗證|Loaded validation|實際位移要在指定力、溫度和行程內驗證。|Displacement must be checked at defined force, temperature and stroke.|保存負載、位移感測和驅動波形同步記錄。|Retain synchronized load, position and drive records.|空載照片可以證明所有受力定位性能。|An unloaded photo proves all loaded positioning performance.
''')

course(296,'聲電諧振、回波與飛行時間','electroacoustic resonance, echoes and time of flight',
'傳播與換能|Propagation and transduction;激發與接收|Excitation and reception;回波判別|Echo discrimination;校準與驗收|Calibration and acceptance',
'單站脈衝回波距離 d=c·Δt/2。|Monostatic pulse-echo distance d=c·Δt/2.',
'假設空氣聲速 343 m/s、往返時間 2.0 ms，距離 0.343 m；若誤忘除 2，結果會大一倍。',
'Assuming air sound speed 343 m/s and round-trip time 2.0 ms, distance is 0.343 m; omitting division by two doubles the result.',
'單一反射路徑與固定聲速近似；溫度、濕度、氣流和多路徑需另外評估。','Single reflection path and fixed sound speed; temperature, humidity, flow and multipath require additional assessment.',
'ultrasound ultrasound-tuning ti-place','ti','a295 a271','ti', '''
聲速與環境|Sound speed and environment|聲速隨介質和環境改變，不可把空氣值用於液體。|Sound speed changes with medium/environment; air values do not apply to liquids.|比较不同假設聲速造成的距離偏差。|Compare distance bias under different assumed sound speeds.|所有介質的聲速相同。|Sound speed is identical in all media.
換能器等效|Transducer equivalent|BVD 模型把機械模態轉成電性運動支路。|BVD models map mechanical modes to electrical motional branches.|找阻抗掃頻中的諧振與反諧振。|Locate resonance/antiresonance in impedance sweeps.|換能器頻率響應只由靜態電容決定。|Transducer response depends only on static capacitance.
方向與目標|Beam and target|波束角、目標面積和傾角決定回波能量。|Beam angle, target area and tilt determine echo energy.|比較平面正對與傾斜目標的反射路徑。|Compare normal and tilted target reflection paths.|相同距離的所有物體必有相同回波強度。|All targets at equal distance produce equal echoes.
激發週期|Burst cycles|較長突發增加能量但擴大盲區和時間寬度。|Longer bursts add energy but widen blind zone/time extent.|比較不同週期數的包絡與最近可分辨目標。|Compare envelope and nearest resolvable target across burst lengths.|增加激發週期只會改善所有測距性能。|More burst cycles improve every ranging metric.
振鈴與阻尼|Ringing and damping|殘留振鈴會遮蔽近距回波；阻尼也可降低靈敏度。|Residual ringing masks near echoes; damping can reduce sensitivity.|比較衰減時間與遠距回波幅度。|Compare decay time and far-echo amplitude.|最大阻尼永遠是最佳測距設定。|Maximum damping is always optimal for ranging.
接收保護|Receive protection|發射後接收前端需要恢復時間，飽和會造成假訊號。|The receiver needs recovery after transmission; saturation can create false signals.|標示發射、保護、恢復和有效接收窗口。|Mark transmit, protection, recovery and valid-receive windows.|發射結束的同一瞬間接收器必已完全恢復。|The receiver is fully recovered the instant transmission ends.
時變增益|Time-varying gain|較晚回波可能更弱，增益曲線需兼顧近距飽和。|Later echoes may be weaker; gain profiles must also avoid near saturation.|比較固定增益與時變增益下的回波序列。|Compare echo trains with fixed and time-varying gain.|接收增益越高就永不漏檢。|Higher receive gain prevents all missed detections.
閾值與包絡|Threshold and envelope|噪聲和振鈴使固定閾值不一定適合所有時間。|Noise/ringing can make one threshold unsuitable across time.|對假想包絡標出誤觸和漏檢區域。|Mark false triggers and misses on hypothetical envelopes.|第一個過閾值峰必定是真正最近物體。|The first threshold crossing is always the nearest real target.
多路徑|Multipath|牆面和結構產生額外反射，延遲不一定對應直達距離。|Walls/structures create extra echoes whose delay need not reflect direct range.|畫出直達與反射路徑長度。|Draw direct and reflected path lengths.|每個回波都代表獨立直線目標。|Every echo represents a separate line-of-sight target.
時間校準|Timing calibration|電子延遲與閾值時間游走會偏移飛行時間。|Electronic delay and threshold time walk bias flight time.|用多個已知距離分離固定延遲與比例誤差。|Use several known distances to separate fixed delay and scale error.|單一距離校準可分開所有時間偏差。|One distance calibration separates every timing error.
聲速補償|Sound-speed compensation|溫度感測位置不一定代表整個聲路。|Temperature-sensor location may not represent the whole acoustic path.|比較均溫與梯度條件下距離殘差。|Compare residuals in uniform and gradient conditions.|一個晶片溫度感測值等於全部聲路溫度。|One chip-temperature value equals the whole path temperature.
可偵測範圍|Detection envelope|有效距離取決於目標、環境、波束和誤報要求。|Useful range depends on target, environment, beam and false-alarm requirements.|用目標種類×角度×距離矩陣描述結果。|Report target×angle×distance results.|最遠一次成功回波就是所有目標額定距離。|One farthest successful echo is rated range for every target.
''')

course(297,'差動匯流排、隔離與故障診斷','differential buses, isolation and fault diagnosis',
'網路與訊號|Network and signal;隔離與供電|Isolation and power;時序與干擾|Timing and interference;診斷與驗證|Diagnosis and validation',
'傳輸延遲 t=L/v；終端反射 Γ=(ZL−Z₀)/(ZL+Z₀)。|Propagation delay t=L/v; terminal reflection Γ=(ZL−Z₀)/(ZL+Z₀).',
'假設纜線 100 m、速度 2×10⁸ m/s，單程延遲 0.5 µs；1 Mbit/s 的 bit 時間 1 µs，不能忽略往返反射。',
'Assuming 100 m cable at 2×10⁸ m/s, one-way delay is 0.5 µs; at 1 Mbit/s a bit lasts 1 µs, so round-trip reflections cannot be ignored.',
'均勻傳輸線估算；可用速率還受上升時間、拓撲、收發器和協定限制。','Uniform-line estimate; usable rate also depends on rise time, topology, transceiver and protocol.',
'isolation isolated-rs485 ti-place','ti','a270 a290','ti', '''
差動與共模|Differential and common mode|差動接收仍有有限共模範圍。|Differential reception still has a finite common-mode range.|分別畫 A−B 和 (A+B)/2 的波形。|Plot A−B and (A+B)/2 separately.|差動通訊完全不需要考慮地電位差。|Differential communication never needs ground-potential analysis.
匯流排拓撲|Bus topology|長分支會形成反射，星形與線形的限制不同。|Long stubs create reflections; star and linear topologies differ.|在圖上標示主幹、分支和傳播時間。|Mark trunk, stubs and delays.|任何線長的星形都可直接視為理想單線。|Any star topology is an ideal single line regardless of length.
終端匹配|Termination|終端需對應傳輸線及位置，過多終端加重負載。|Termination must match line/location; too many terminations increase loading.|比較兩端終端與每節點都終端的等效負載。|Compare endpoint termination and every-node termination loads.|每個節點都加終端電阻一定最佳。|A terminator at every node is always best.
隔離屏障|Isolation barrier|資料隔離和供電隔離需共同構成完整路徑。|Data and power isolation jointly form a complete boundary.|查找跨屏障地線、屏蔽和供電旁路。|Find ground, shield and power bypasses across the barrier.|只隔離資料腳就保證整個節點隔離。|Isolating data pins fully isolates the node.
工作額定|Working ratings|隔離耐壓、連續工作與突波不是同一規格。|Withstand, continuous working and surge ratings differ.|將三種額定及認證條件分欄。|Separate the three ratings and certification conditions.|一分钟耐壓就是終生連續工作電壓。|One-minute withstand is lifetime working voltage.
隔離電源 EMI|Isolated-power EMI|小型隔離電源的高頻磁耦合和寄生可能成為輻射源。|High-frequency magnetic coupling/parasitics in compact isolated supplies can radiate.|分開電源和資料切換頻譜定位來源。|Separate power and data switching spectra.|整合隔離電源一定完全沒有 EMI。|Integrated isolated power necessarily has no EMI.
CMTI|Common-mode transient immunity|CMTI 描述快速共模變化下的邏輯可靠性，不等同耐壓。|CMTI describes logic integrity during fast common-mode transitions, not withstand voltage.|把 dv/dt 條件與靜態電压額定分開檢查。|Check dv/dt conditions separately from static voltage ratings.|CMTI 數值可直接當成隔離電壓。|CMTI can be directly treated as isolation voltage.
方向切換|Direction turnaround|半雙工使能、線路延遲和等待時間影響碰撞。|Half-duplex enables, delay and turnaround affect collisions.|畫出兩節點傳送使能與最後一位時間。|Draw enables and last-bit timing for two nodes.|軟體送完資料就表示線上最後一位已結束。|Software send completion means the last line bit has ended.
失效安全|Failsafe|開路、短路與空閒輸入的接收狀態依器件定義。|Receiver states for open, short and idle depend on device definitions.|在概念模型中逐一標記三種狀態。|Mark all three states in a conceptual model.|failsafe 標示代表所有故障都會自動修復。|Failsafe means every fault is automatically repaired.
隔離與協定|Isolation versus protocol|電氣隔離不提供身份驗證或資料完整性保證。|Galvanic isolation does not provide authentication or data integrity guarantees.|分開列出 CRC、重試和存取控制需求。|List CRC, retry and access-control needs separately.|隔離收發器自動加密並驗證所有資料。|An isolated transceiver automatically encrypts/authenticates all data.
故障定位|Fault localization|反射、地偏移與軟體超時可能產生相似遺失封包症狀。|Reflections, ground shifts and software timeouts can all cause packet loss.|同步對照差動波形、共模和協定日誌。|Correlate differential/common-mode waveforms and protocol logs.|所有 CRC 錯誤都一定是程式寫錯。|All CRC errors necessarily come from software bugs.
環境驗證|Environmental validation|線長、節點數、干擾與供電組合需建立邊界。|Length, node count, interference and supply combinations define boundaries.|保存可重現拓撲及失敗率統計。|Retain reproducible topology and failure-rate statistics.|短線桌上通過就代表最長工廠網路通過。|A short bench cable passing proves the longest plant network passes.
''')

course(298,'島嶼互聯、VSC 增建與韌性規劃','island interconnection, a VSC addition and resilience planning',
'案例與需求|Case and requirements;換流與線路|Conversion and line;控制與韌性|Control and resilience;驗證與比較|Validation and comparison',
'直流實功率 P≈Vdc·Idc；單極與雙極電壓定義不能混用。|DC power P≈Vdc·Idc; do not mix monopole and bipole voltage definitions.',
'以 2019 年公開新連線額定 250 kVdc、1,200 Adc 作端口核算，P=300 MW；此乘法未計換流與線路損耗。',
'Using published 2019 new-link ratings of 250 kVdc and 1,200 Adc gives P=300 MW; this terminal calculation omits conversion and line losses.',
'本例引用 2019 新北本 VSC 的歷史額定，不表示全部北海道本州連線現況或可用容量。','Uses historical ratings of the 2019 New Hokkaido-Honshu VSC link, not all current interconnection capacity or availability.',
'hokkaido hokkaido-operator','hokkaido','a211 a212','toshiba', '''
案例邊界|Case boundary|2019 新增 300 MW VSC 與既有 600 MW LCC 是不同設備。|The 2019 300 MW VSC addition and existing 600 MW LCC are distinct assets.|把來源年份、拓撲及容量分欄，不合併成同一設備。|Separate source year, topology and capacity rather than merging assets.|2019 新設備就是原有 600 MW LCC 的同一套裝置。|The 2019 unit is the same equipment as the older 600 MW LCC.
島嶼供需|Island supply/demand|互聯提供電力調度選項，但受本地網架和資源限制。|Interconnection adds dispatch options within local-network and resource limits.|用假想負載與發電情境檢查進出口需求。|Check import/export needs in hypothetical load/generation cases.|有互聯就不再需要任何本地備援。|Interconnection removes all need for local reserves.
容量與可用性|Capacity and availability|額定容量不等於每時每刻可用的輸送量。|Rated capacity is not continuously available transfer.|區分額定、停機、網路限額和實際潮流。|Separate rating, outages, network limits and actual flow.|銘牌容量就是每小時必然輸送的電力。|Nameplate capacity is necessarily delivered every hour.
LCC 與 VSC|LCC versus VSC|換流技術對無功需求、交流系統依賴和控制方式不同。|Converter types differ in reactive needs, AC-system dependence and control.|比較公開原理下兩種方塊圖。|Compare block diagrams based on public principles.|所有 HVDC 換流器具有完全相同無功行為。|All HVDC converters have identical reactive behavior.
端口功率帳|Terminal power balance|P=VI 的端口額定須分清電壓參考和電流。|P=VI ratings need consistent voltage reference and current.|重算 250 kV×1,200 A 並標出損耗位置。|Recompute 250 kV×1,200 A and mark loss locations.|將所有極電壓再加倍一定更準確。|Doubling every pole voltage is always more accurate.
線路路徑|Route composition|新連線採青函隧道相關路徑；不可把所有段都叫同一海纜。|The new route includes the Seikan Tunnel context; not every segment is the same submarine cable.|依營運者公開圖分類架空、隧道與換流端。|Classify overhead, tunnel and converter segments using public operator diagrams.|每種跨海連線都全程是海底電纜。|Every sea-crossing link consists entirely of submarine cable.
有功無功邊界|P/Q capability|變流器能力受電流和電壓限制，P 與 Q 不可任意同時最大。|Converter capability is current/voltage limited; P and Q cannot be arbitrarily maximized together.|用假想視在功率圓辨識能力邊界。|Use a hypothetical apparent-power circle to identify limits.|有功與無功額定總可同時無限制加總。|Active/reactive ratings can always be added without limits.
擾動與控制|Disturbance and control|控制可調節功率但速度與電流限幅需協調。|Control adjusts power within dynamic and current limits.|在非實網模擬中比較有無電流限幅的恢復。|Compare recovery with/without current limits in a non-operational model.|任意快的功率階躍都不會影響交流端。|Arbitrarily fast power steps never affect AC terminals.
停機情境|Outage scenarios|新增通道可增加選項，但共因失效需獨立評估。|Additional paths add options but require common-cause failure assessment.|以抽象 N−1 表比較單通道停機後剩餘容量。|Use an abstract N−1 table to compare remaining capacity after one outage.|兩條線路永遠完全獨立且不會共因失效。|Two links are always fully independent with no common-cause failure.
工程介面|Engineering interfaces|電網、土木、隧道和環境介面需要跨團隊證據。|Grid, civil, tunnel and environmental interfaces need cross-team evidence.|建立責任和交付物矩陣，不推測敏感設備位置。|Build a responsibility/deliverable matrix without inferring sensitive equipment positions.|換流器完成就等於整條互聯工程完成。|Completing converters completes the entire interconnector.
試驗與歷史|Tests and history|2019 營運公告可證明投運事件，不等於今日的即時狀態。|The 2019 operator notice supports commissioning history, not today's live status.|為每個容量與日期主張加上來源日期。|Attach source dates to every capacity/date claim.|歷史新聞足以證明現在全部設備可用。|Historical news proves every asset is available now.
可移轉工法|Transferable methods|島嶼互聯方法可比較其他 HVDC，但網路強度和路徑不同。|Island-link methods transfer to other HVDC cases, but network strength/routes differ.|與紐西蘭案例比較需求、路徑和技術年代。|Compare needs, routes and technology eras with New Zealand.|不同國家 HVDC 可直接複製全部設定。|HVDC settings can be copied wholesale between countries.
''')

course(299,'跨國互聯、海纜與容量交易','cross-border interconnection, subsea cables and capacity exchange',
'歷史與系統|History and system;換流與海纜|Converters and cable;市場與韌性|Market and resilience;證據與比較|Evidence and comparison',
'E=Pavg·t；負載率=E/(Prated·t)，兩者需同一時段。|E=Pavg·t; utilization=E/(Prated·t), using the same period.',
'假想 2 GW 連線一天平均輸送 1 GW，電量 24 GWh、以額定為分母的利用率 50%；不是 IFA 的實際調度資料。',
'A hypothetical 2 GW link averaging 1 GW over a day transfers 24 GWh, or 50% rated-capacity utilization; this is not actual IFA dispatch data.',
'示例不含雙向交換與損耗；真實利用率需說明方向、淨額或絕對流量定義。','Excludes bidirectional exchange and losses; real utilization needs direction and net-versus-absolute-flow definitions.',
'ifa ifa-history ifa-operator ifa-recovery','ifa','a208 a300','nationalgrid', '''
歷史辨識|Historical identity|IFA 在 1986 年投運；更早 1961 年連線和 IFA2 是不同歷史階段。|IFA entered service in 1986; the earlier 1961 link and IFA2 are distinct stages.|建立含名稱與年份的對照表。|Build a name/year comparison table.|IFA、1961 年連線和 IFA2 都是同一項目。|IFA, the 1961 link and IFA2 are one project.
兩端系統|Two-end systems|直流互聯可交換功率而不使兩個交流網強制同步。|DC exchange transfers power without forcing AC systems into synchronism.|畫出兩端頻率和受控直流功率的關係。|Draw both AC frequencies and controlled DC power.|HVDC 互聯要求兩國交流相角永遠相同。|HVDC requires both countries' AC phase angles to be identical.
額定與路線|Rating and route|營運者列 IFA 2,000 MW、約 70 km，其中約 45 km 海底。|The operator lists IFA as 2,000 MW and about 70 km, including about 45 km subsea.|將总長與海底段分開，保留「約」的精度。|Separate total and subsea length, preserving approximation.|70 km 全部都是海底段。|All 70 km is subsea.
換流站角色|Converter role|換流站連接交流網和直流電纜，變壓與濾波是系統部分。|Stations link AC networks and DC cables; transformers/filtering are system elements.|畫出能量與無功的不同路徑。|Draw distinct energy/reactive-power paths.|海纜兩端只接變壓器就能交換直流功率。|Transformers alone at cable ends enable DC exchange.
海纜熱限制|Cable thermal limits|載流量依海床熱條件、埋設和相鄰熱源變化。|Ampacity depends on seabed thermal conditions, burial and nearby heat sources.|比較假想熱阻上下界下的溫升。|Compare rise under assumed thermal-resistance bounds.|所有海域相同電纜都有同一載流能力。|The same cable has equal ampacity in every seabed.
登陸與路由|Landing and routing|海纜、陸纜與站址形成不同施工和維護介面。|Subsea cable, land cable and stations create different construction/maintenance interfaces.|依公開路線區分段落及權責。|Separate segments/responsibility from public routes.|跨海工程只有海上鋪纜一個工作包。|A sea link has only one offshore-laying work package.
容量與能源|Capacity versus energy|MW 是可交換功率能力，MWh 是某時段交換能量。|MW is transfer-power capability; MWh is exchanged energy over time.|用一天假想流量曲線積分電量。|Integrate a hypothetical daily flow curve.|2,000 MW 就等於每天 2,000 MWh。|2,000 MW equals 2,000 MWh per day.
市場與技術|Market and engineering|容量分配與實際潮流受商業及物理約束共同影響。|Capacity allocation and actual flows face both market and physical constraints.|分開記錄可售容量、預約和實際輸送。|Separate offered capacity, nominations and actual transfer.|售出容量必然等於每小時實际潮流。|Sold capacity necessarily equals each hour's actual flow.
可用性與共因|Availability and common causes|站內火災等事件說明額定和韌性要分開評估。|Events such as station fire show rating and resilience need separate assessment.|用已公開歷史事件建立功能層級恢復表。|Use public historical events to create a functional recovery table.|雙極設計意味任何站內事件都不會損失容量。|Bipolar design means no station event can reduce capacity.
維護窗口|Maintenance windows|線路與換流設備維護需協調兩端供需和備援。|Cable/converter maintenance needs coordination of two-end demand and reserves.|比較假想低負載與高負載停機影響。|Compare hypothetical low/high-demand outage effects.|只要機器需要維護就可忽略電網時段。|Maintenance timing can ignore grid conditions.
資料時效|Data freshness|歷史容量、當前可用性和未來計畫需不同來源日期。|Historical rating, current availability and future plans need dated sources.|對各表格加發布時間及非即時標籤。|Date each table and label non-live information.|任意官方舊網頁都等於即時潮流。|Any old official webpage equals live flow.
跨案例比較|Cross-case comparison|與紐西蘭相比都含海纜，但市場制度和水力角色不同。|Both IFA and New Zealand include subsea cable, but market structure and hydro roles differ.|比較技術可移轉項與制度不可直接複製項。|Compare transferable technology and nontransferable institutional assumptions.|相同海纜技術代表相同市場和備援需求。|Same cable technology means identical market/reserve needs.
''')

course(300,'南北島能源互補與資產更新','island energy complementarity and asset renewal',
'歷史與水力|History and hydro;线路與換流|Line and conversion;調度與更新|Dispatch and renewal;風險與證據|Risk and evidence',
'能源不足量 ΔE=(需求−可用發電)·持續時間；需與互聯可用功率共同核算。|Energy shortfall ΔE=(demand−available generation)·duration, checked against available link power.',
'教學某島需額外 300 MW 持續 4 小時，缺口 1.2 GWh；互聯是否可補足還取決於對端餘裕與剩餘容量。',
'If an island hypothetically needs an extra 300 MW for 4 hours, the gap is 1.2 GWh; filling it also requires exporting-island surplus and available link capacity.',
'完全是假想調度練習，並非紐西蘭電網當前負載、備援或操作指令。','Entirely hypothetical dispatch exercise, not current New Zealand load, reserve or operating instructions.',
'nz-history nz-upgrade nz-contract','nz','a298 a299','transpower', '''
1965 起點|1965 beginning|南北島 HVDC 初次投運於 1965 年，其後多次更新。|The inter-island HVDC link first entered service in 1965 and has been renewed repeatedly.|將最初系統與後續極線年代分開。|Separate the initial system from later pole eras.|1965 年的所有硬體至今完全未變。|All 1965 hardware remains entirely unchanged.
水力互補|Hydro complementarity|南島水力與北島資源可隨水文與需求互補。|South Island hydro and North Island resources can complement each other as hydrology/demand change.|比較濕年與乾年假想能源平衡。|Compare hypothetical wet-/dry-year energy balances.|互聯永遠只能把電從南島送到北島。|The link can only ever transfer south-to-north.
功率與能量限制|Power and energy limits|互聯解決輸送能力但不創造儲水或燃料。|A link provides transfer capacity but creates no stored water or fuel.|同時計算 MW 限額與 GWh 資源需求。|Calculate MW limits and GWh resource needs together.|增加互聯額定即可無限制消除缺水能源問題。|Higher link rating eliminates water-related energy shortages without limit.
陸線與海纜|Overhead and subsea segments|Benmore 到 Haywards 同時含架空與庫克海峽海纜。|Benmore–Haywards includes overhead line and Cook Strait submarine cable.|分段標示資產型態與環境限制。|Label asset types and environmental constraints by segment.|整條南北島連線全部位於海底。|The entire inter-island link is submarine.
極線年代|Pole eras|Pole 1 退役、Pole 3 在 2013 年替代的歷史不能與原始系統混同。|Pole 1 retirement and Pole 3 replacement in 2013 must be distinguished from the original system.|以來源年份核對極線名稱與事件。|Check pole names/events against dated sources.|Pole 3 就是 1965 年原封不動的 Pole 1。|Pole 3 is the unchanged 1965 Pole 1.
損耗與方向|Loss and direction|雙向輸送的損耗和限制需按方向、電流與交流邊界分析。|Bidirectional losses/limits depend on direction, current and AC boundaries.|以假想損耗曲線重算送端與受端功率。|Use hypothetical loss curves to recalculate sent/received power.|送端和受端功率永遠完全相同。|Sending and receiving powers are always identical.
備援共享|Reserve sharing|互聯可協助區域支援，但須預留容量與動態能力。|Interconnection can support regions but needs headroom and dynamic capability.|將商業輸送與支援餘裕分開記帳。|Account separately for scheduled transfer and support headroom.|滿載輸送仍可額外無限制提供支援。|A fully loaded link provides unlimited additional support.
停機規劃|Outage planning|維護安排需考慮季節負載與發電可用性。|Maintenance planning considers seasonal load and generation availability.|比較單極與全連線假想停機對能源平衡的影響。|Compare hypothetical single-pole and full-link outage balances.|低需求季節就不需要任何停機風險分析。|Low-demand season removes all outage-analysis needs.
海纜老化|Cable aging|原有海纜安裝年代與剩餘壽命假設決定更新規劃。|Installation era and remaining-life assumptions inform renewal planning.|分開歷史投運年、設計假設與實測狀態。|Separate commissioning history, design assumptions and observed condition.|到某年份所有海纜必定在同一天失效。|All cables necessarily fail on one date at a given age.
計畫版本|Plan versions|2026 合約公告與較早升級頁面時程不同時，應保留版本。|If a 2026 contract notice and an earlier upgrade page differ in schedule, preserve their versions.|用較新公告標示計畫日期，保留未完成的未來式。|Use the newer notice for planned dates and retain future tense.|尚未建成的計畫容量可寫成現在已投運。|Planned capacity can be described as already operational.
環境與退役|Environment and retirement|新纜安裝和舊纜留置或移除需環境、成本與可靠度比較。|New cable installation and old-cable retention/removal need environmental, cost and reliability comparison.|列出已公開選項與尚待決策項目。|List public options and undecided items.|技術可行就代表所有環境決策已獲准。|Technical feasibility means all environmental decisions are approved.
案例綜合|Case synthesis|更新工程需在服務持續、容量與資產風險間取捨。|Renewal trades service continuity, capacity and asset risk.|與 IFA、新北本比較既有資產與新增容量的角色。|Compare old/new asset roles with IFA and New Hokkaido-Honshu.|三個 HVDC 案例的更新策略應完全相同。|All three HVDC cases should have identical renewal strategies.
''')
