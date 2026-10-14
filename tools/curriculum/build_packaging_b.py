from pathlib import Path
import json

ROOT=Path(__file__).parent
# Each row is an independently authored learning operation:
# title ZH/EN | action ZH/EN | observable criterion ZH/EN | fault diagnosis ZH/EN.
# The execution environment is a simulator, never a production tool recipe.
MODULES=[
dict(n=11,title='TSV 成孔、襯層、阻障與填孔',titleEn='TSV formation, liner, barrier, and fill',
route='TSV 支線；依 via-middle、via-last 與中介層結構選用，並非所有封裝都有 TSV。',
routeEn='TSV branch: select for via-middle, via-last, or interposer structures; many packages have no TSVs.',
principle='深孔的幾何、絕緣連續性與金屬覆蓋共同決定填孔與電性；入口外觀不能代替孔底證據。',
principleEn='Via geometry, dielectric continuity, and metal coverage jointly govern fill and electrical behavior; the entrance cannot establish bottom quality.',
sources=['pkb-lam-tsv','pkb-nordson-wafer'],rows='''
TSV 深寬比核對|Check TSV aspect ratio|由剖面資料計算孔深與最小孔寬比|Calculate depth divided by minimum width from cross sections|幾何位於已核准設備能力範圍|Geometry falls within the approved tool capability|入口寬度代替最窄處會低估填孔難度|Using entrance width hides the narrowest fill restriction
硬遮罩厚度分布|Map hard mask thickness|疊合遮罩厚度圖與預期蝕刻損耗圖|Overlay mask thickness and predicted erosion maps|各區域仍保有核准的遮罩餘量|Every region retains its approved mask allowance|局部遮罩耗盡可造成孔口擴張|Local mask exhaustion can enlarge the via mouth
TSV 光阻開口殘留|Inspect TSV resist openings|比較顯影前後孔口影像與底部殘留訊號|Compare opening images and residual-film signals|孔口開放且無可辨識阻塞膜|Openings are clear without detectable blocking film|孔底殘膠會抑制起始蝕刻|Residual resist inhibits initial etching
成孔光罩套準|Check via-mask overlay|把孔位與禁佈區邊界共同套圖|Overlay via locations with keep-out boundaries|套準誤差未侵入設計保留區|Overlay errors do not enter design keep-out zones|孔位偏移可侵入元件或金屬|Misplaced vias can intrude into devices or metal
深矽蝕刻剖面|Inspect deep silicon etch profile|在模擬剖面量測側壁斜率|Measure sidewall taper on simulated cross sections|斜率符合選定填孔路線的規範|Taper meets the selected fill route specification|反入射輪廓可使上緣先封口|Reentrant profiles can close at the top prematurely
孔深均勻性|Map via-depth uniformity|比較中心中圈與邊緣孔深分布|Compare center, middle, and edge depth distributions|最深與最淺孔均在規格窗內|Deepest and shallowest vias meet the specification window|只看平均孔深會漏掉邊緣異常|Average depth can conceal edge excursions
側壁扇貝紋判讀|Assess sidewall scalloping|比較側壁輪廓與襯層覆蓋模型|Compare sidewall profiles with liner coverage models|局部曲率未造成預測覆蓋中斷|Local curvature does not interrupt predicted coverage|尖銳凹槽會增加薄膜薄弱點|Sharp recesses create vulnerable coating regions
孔底停止層判讀|Assess via-bottom stop layer|分辨孔底殘矽與停止層受損訊號|Distinguish residual silicon from damaged stop layers|停止層完整且孔底已到設計深度|Stop layer is intact at the designed via depth|過蝕刻可損傷底部互連|Overetch can damage underlying interconnects
蝕刻側壁殘留清除驗證|Verify etch-residue removal|比較清洗前後表面分析資料|Compare surface-analysis data before and after cleaning|殘留降至核准門檻且輪廓未改變|Residues meet approved limits without profile damage|殘留物可降低襯層附著|Residues can weaken liner adhesion
孔口缺口與崩裂|Inspect via-mouth notching and chips|放大孔口與遮罩交界影像|Inspect enlarged via-mouth and mask-edge images|缺口與裂紋未越過允收界線|Notches and cracks remain within acceptance boundaries|邊緣缺口可成為應力集中處|Edge notches can concentrate stress
TSV 絕緣襯層覆蓋|Assess dielectric liner coverage|讀取孔頂中段孔底膜厚資料|Read liner thickness at top, middle, and bottom|最薄區仍符合絕緣設計要求|The thinnest region meets insulation requirements|平均膜厚合格不代表底部連續|Mean thickness does not establish bottom continuity
襯層針孔電性篩選|Screen liner pinholes electrically|比對漏電分布與對照試片|Compare leakage distributions with control coupons|漏電尾端未超過核准限制|Leakage tails remain within approved limits|少量針孔可主導漏電尾端|Sparse pinholes can dominate leakage tails
襯層薄膜應力|Evaluate liner film stress|將晶圓曲率與膜厚共同代入模型|Combine wafer curvature and film thickness in the model|應力與翹曲符合整合預算|Stress and bow remain within integration budgets|應力偏高可促進薄化後翹曲|High stress can promote bow after thinning
底部接觸開口支線|Evaluate via-last bottom-contact opening|在 via-last 案例檢查孔底介電開口|Inspect bottom dielectric openings in a via-last case|接觸區開啟而側壁絕緣保持|Contact opens while sidewall insulation remains|側壁同步移除會增加短路風險|Sidewall removal increases shorting risk
金屬阻障層連續性|Check barrier continuity|讀取截面成分圖與厚度圖|Read cross-sectional composition and thickness maps|孔底與轉角沒有阻障中斷|Barrier remains continuous at bottoms and corners|阻障破口可能允許銅擴散|Barrier breaks can permit copper diffusion
種子層孔底覆蓋|Check seed coverage at via bottoms|比較孔底與平面種子導電性|Compare bottom and field seed conductivity|種子形成可連續供電路徑|Seed provides a continuous current path|不連續種子可留下未鍍區|Discontinuous seed can leave unplated regions
種子層片電阻分布|Map seed sheet resistance|套合片電阻圖與接點位置|Overlay sheet resistance and contact locations|分布與連通性符合電鍍規劃|Distribution and continuity support the plating plan|局部高阻會扭曲電流分配|Local high resistance distorts current distribution
鍍前潤濕模擬|Simulate preplating wetting|觀察透明孔模型中的氣泡排出|Observe bubble release in a transparent via model|孔腔完全潤濕且無滯留氣泡|Via cavities are wetted without trapped bubbles|困氣會阻擋局部金屬成核|Trapped gas blocks local metal nucleation
電鍍添加劑分析判讀|Interpret plating-additive monitoring|比較槽液分析趨勢與核准控制窗|Compare bath-analysis trends with approved control windows|各分析指標均保持受控|Each analytical indicator remains controlled|補充量正常仍可能存在分析漂移|Normal replenishment does not exclude analysis drift
TSV 底向上填孔|Interpret bottom-up TSV filling|比較不同填孔進度的剖面序列|Compare cross sections across fill progression|填孔前緣未在孔口提前閉合|Fill front avoids premature mouth closure|入口先閉合會封住內部空隙|Early mouth closure traps internal voids
鍍銅過鍍層分布|Map copper overburden|將過鍍厚度圖傳入平坦化模型|Feed overburden maps into the planarization model|過鍍可在核准移除預算內清除|Overburden fits the approved removal budget|厚度不均會拉大拋光終點差異|Uneven overburden spreads polishing endpoints
填孔空洞斷層檢測|Inspect filled-via voids by tomography|追蹤斷層切片中的低密度區|Track low-density regions through tomographic slices|空洞尺寸位置符合允收規則|Void size and location meet acceptance rules|單張投影可把重疊結構誤判空洞|One projection can confuse overlap with voiding
填銅熱處理尺寸穩定|Assess filled-copper thermal stability|比較熱歷程前後表面凸起量|Compare surface protrusion before and after thermal history|凸起與內應力位於整合限制內|Protrusion and stress remain within integration limits|銅與矽熱膨脹差可推升孔頂|Copper-silicon expansion mismatch can raise via tops
TSV 銅 CMP 終點|Determine TSV copper CMP endpoint|同步讀取金屬移除與停止層訊號|Read metal removal and stop-layer signals together|過鍍去除且停止層損失受控|Overburden clears while stop-layer loss stays controlled|過拋光可產生凹陷與介電侵蝕|Overpolish can produce dishing and dielectric erosion
孔頂凹陷與侵蝕|Measure TSV dishing and erosion|跨越孔頂與鄰近介電區量測高度|Measure heights across via tops and neighboring dielectric|局部與全域高度誤差均達標|Local and global height errors meet requirements|只量銅凹陷會漏看介電侵蝕|Measuring copper alone misses dielectric erosion
TSV 鏈結與隔離驗證|Verify TSV chains and isolation|聯合判讀鏈結電阻與對矽漏電|Interpret chain resistance and leakage to silicon together|導通及隔離兩種證據同時合格|Continuity and isolation evidence both pass|低鏈阻不能排除對基體漏電|Low chain resistance does not exclude substrate leakage
'''),
dict(n=12,title='TSV 顯露、背面鈍化與重布線',titleEn='TSV reveal, backside passivation, and redistribution',
route='已填 TSV 晶圓的背面支線；載板、去黏方式與背面金屬順序依材料系統選用。',
routeEn='Backside branch for filled-TSV wafers; carrier, debond method, and backside metal sequence depend on the material system.',
principle='背磨控制厚度，選擇性顯露建立導通端點；機械支撐與後續介電完整性必须一起檢查。',
principleEn='Grinding sets thickness and selective reveal exposes contacts; mechanical support and subsequent dielectric integrity require joint checks.',
sources=['pkb-disco-thin','pkb-lam-tsv'],rows='''
暫時載板平整度|Check temporary-carrier flatness|比較載板厚度及平面度地圖|Compare carrier thickness and flatness maps|載板誤差不耗盡薄化公差|Carrier errors do not exhaust thinning tolerance|載板楔角會轉移為晶圓厚度梯度|Carrier wedge transfers into wafer thickness gradients
前表面保護層覆蓋|Inspect front-side protection|把保護層剖面與最高凸塊疊合|Overlay protection cross sections with tallest bumps|凸塊完全受保護且無局部空腔|Bumps are protected without local cavities|凸塊上方支撐不足易壓傷|Insufficient support above bumps permits damage
暫時黏著層均勻性|Map temporary-bond adhesive uniformity|量測黏著層厚度及空洞區域|Measure adhesive thickness and void regions|支撐層厚度與空洞均達標|Support-layer thickness and voiding meet criteria|黏著層厚差會影響最終總厚度變異|Bondline variation affects final thickness variation
載板鍵合空洞|Inspect carrier-bond voids|判讀紅外或聲學黏著介面影像|Interpret infrared or acoustic bond-interface images|承載區無超出規則的未黏合區|Load-bearing regions lack unacceptable unbonded areas|未黏區在背磨時可局部彎曲|Unbonded regions can flex during grinding
晶圓邊緣修整|Evaluate wafer-edge trimming|比較薄化前後邊緣幾何模型|Compare edge geometry before and after thinning|保留邊緣不形成脆弱刀口|Remaining edge avoids a fragile knife shape|尖薄邊緣易崩裂並傳播裂紋|Sharp thin edges chip and propagate cracks
粗磨剩餘矽厚|Control silicon remaining after coarse grind|追蹤厚度計訊號與移除量|Track thickness-gauge signals and removal amount|保留足夠後續精磨餘量|Sufficient allowance remains for fine grinding|粗磨直接到終厚會保留深損傷|Coarse grinding to final thickness retains deep damage
精磨磨痕方向|Assess fine-grind marks|比較粗糙度地圖與磨痕分布|Compare roughness maps with grind-mark patterns|磨痕及粗糙度符合後續移除能力|Marks and roughness fit downstream removal capability|局部深痕可能超過應力消除深度|Deep marks can exceed stress-relief removal depth
總厚度變異量測|Measure total thickness variation|用共同座標比較多點厚度|Compare multipoint thicknesses in a common frame|最大與最小厚度均達標|Maximum and minimum thicknesses meet limits|中心單点合格不能代表全片|A center-only pass does not represent the wafer
背磨損傷層消除|Evaluate grinding damage removal|比較處理前後表面裂紋與強度資料|Compare crack and strength data before and after treatment|損傷訊號下降且剩餘厚度合格|Damage decreases while remaining thickness passes|只降低粗糙度未必消除亞表面裂紋|Lower roughness need not remove subsurface cracks
TSV 顯露終點模擬|Simulate TSV reveal endpoint|讀取矽移除量與孔端高度|Read silicon removal and via-tip height together|孔端露出但未超出支撐容許量|Tips are exposed within supported-height limits|過度顯露會削弱孔端機械支撐|Excessive reveal weakens mechanical tip support
背面顯露高度分布|Map backside reveal height|建立全片 TSV 突出高度圖|Map TSV protrusion heights across the wafer|最矮孔可接觸且最高孔不過凸|Shortest tips contact while tallest avoid excessive protrusion|孔深差異會轉換成顯露高度差|Via-depth variation becomes reveal-height variation
背面殘矽辨識|Identify residual backside silicon|疊合元素分析與孔端影像|Overlay composition data with via-tip images|接觸區未殘留阻斷導通的矽|Contact regions lack silicon blocking continuity|外觀露孔不代表金屬接觸完全開放|Visible tips do not guarantee exposed metal contacts
背面介電鈍化|Evaluate backside dielectric passivation|比較介電膜跨孔端的覆蓋|Compare dielectric coverage around exposed tips|矽表面連續隔離且無破口|Silicon surface is continuously insulated|孔根陰影區可能留下薄膜缺口|Tip-base shadow regions can leave film gaps
背面介電開窗套準|Align backside dielectric openings|把開窗輪廓與孔端座標套圖|Overlay opening contours and via-tip coordinates|開窗落在導電端面且保留隔離|Openings reach contacts while preserving isolation|偏移開窗可能露出鄰近矽|Shifted openings can expose adjacent silicon
孔端殘氧化物判讀|Assess oxide residue on via tips|比較表面分析與接觸電阻|Compare surface analysis with contact resistance|殘膜受控且電阻符合接觸預算|Residual film and resistance fit contact budgets|氧化殘膜可使接觸電阻升高|Oxide residue can increase contact resistance
背面阻障種子沉積|Assess backside barrier and seed deposition|檢查跨越孔端台階的金屬覆蓋|Inspect metal coverage across via-tip steps|導電層跨越台階仍保持連續|Conductive film remains continuous across steps|台階遮蔽可造成金屬斷裂|Step shadowing can break metal continuity
背面 RDL 光阻模壁|Inspect backside RDL resist molds|量測開口底寬及模壁傾斜|Measure opening bottom width and mold-wall slope|模腔可形成設計線寬與間距|Mold cavities support designed width and spacing|模壁倒塌會導致橋接|Collapsed resist walls can cause bridges
背面 RDL 電鍍厚度|Map backside RDL plated thickness|比較寬線與窄線的金屬高度|Compare metal heights on wide and narrow traces|圖形密度區域皆在厚度窗內|All pattern-density regions meet thickness windows|密度效應會造成局部過鍍|Pattern-density effects can cause local overplating
背面去光阻殘留|Inspect backside resist stripping|追蹤線間殘膠與金屬表面變化|Track intertrace residue and metal-surface changes|線間清潔且金屬未明顯侵蝕|Spaces are clean without excessive metal attack|殘膠會遮蔽後續種子層去除|Resist residue masks later seed removal
背面種子層隔離|Verify backside seed isolation|將種子蝕刻影像與絕緣測試比對|Compare seed-removal images with insulation tests|線間種子移除且細線保留|Intertrace seed clears while fine traces remain|過蝕刻會縮窄有效導線|Overetch narrows effective conductor widths
背面 RDL 鏈阻|Measure backside RDL chain resistance|比較四端量測與幾何預測|Compare four-terminal measurements with geometry predictions|鏈阻與設計分布相容|Chain resistance agrees with design distributions|高阻需區分線損與接點異常|High resistance requires separating trace and contact causes
背面保護層邊緣覆蓋|Inspect backside protective-layer edges|檢查金屬角落與保護層邊界|Inspect metal corners and protective-layer boundaries|金屬受保護且接點開放正確|Metal is protected with correct contact openings|角落裂縫可成為水分進入路徑|Corner cracks can admit moisture
背面焊墊金屬介面|Assess backside pad metallurgy|比較焊墊層序與組裝介面要求|Compare pad-layer sequence with assembly requirements|層序與接合材料相容|Layer sequence is compatible with bonding materials|不相容表面可造成潤濕或擴散問題|Incompatible finishes cause wetting or diffusion issues
去黏方式支線選擇|Select carrier-debond branch|依材料相容性比較熱滑移與光解案例|Compare thermal-slide and optical-release compatibility|選用方法不超出晶圓材料限制|Selected method respects wafer material limits|照搬另一載板方法可損傷黏著介面|Transferring another carrier method can damage interfaces
去黏後清潔與翹曲|Inspect post-debond residue and bow|聯合判讀殘膠影像及自由翹曲圖|Review residual adhesive images and free-wafer bow|清潔度及自由形貌皆滿足搬運要求|Cleanliness and free shape meet handling requirements|載板時平坦不表示去黏後平坦|Flatness on a carrier does not prove free-wafer flatness
薄晶圓轉移完整性|Verify thin-wafer transfer integrity|比較轉移前後裂紋與電性座標圖|Compare crack and electrical maps before and after transfer|未新增裂紋或開路群聚|No new cracks or open-circuit clusters appear|局部吸持載荷可誘發延遲破裂|Localized pickup loads can initiate delayed fracture
'''),
]

MODULES += [
dict(n=19,title='封裝可靠度與失效分析',titleEn='Package reliability and failure analysis',
route='可靠度評估為抽樣與破壞性分析支線，並非所有成品都依次接受所有應力試驗；條件依適用規格訂定。',
routeEn='Reliability uses sampling and destructive-analysis branches; not every unit receives every stress test, and conditions follow the applicable specification.',
principle='加速應力必須連結到使用失效機制；測試時間、失效定義與樣本分母不完整時，不能宣稱壽命。',
principleEn='Accelerated stress must connect to service failure mechanisms; lifetime claims require complete duration, failure definitions, and sample denominators.',
sources=['pkb-ti-reliability','pkb-ti-qualification','pkb-amkor-failure','pkb-amkor-characterization'],rows='''
使用任務剖面|Build a service mission profile|將溫度功率濕度與開關循環分開建模|Model temperature, power, humidity, and switching cycles separately|任務載荷與預期失效機制有對應|Mission loads map to expected failure mechanisms|用單一最高溫度代表全壽命會失真|One maximum temperature misrepresents lifetime exposure
可靠度抽樣矩陣|Construct a reliability sampling matrix|分配批次製程角落與對照樣本|Allocate lots, process corners, and control specimens|樣本來源與試驗分母完整|Sample origins and test denominators are complete|只挑外觀最佳樣本會造成選樣偏差|Selecting only best-looking units creates sampling bias
應力前基準電測|Establish prestress electrical baselines|保存每顆樣本的初始參數向量|Save each sample's initial parameter vector|基準值及量測條件可重現|Baseline values and conditions are reproducible|僅保存通過標記無法分析後續漂移|Pass-only records cannot support drift analysis
應力前声學影像|Establish prestress acoustic images|以固定介面深度保存初始影像|Store baseline images at fixed interface depths|影像深度座標與樣本識別完整|Depth coordinates and sample identities are complete|無基準影像易把原有特徵誤當新裂紋|Without baselines, native features may appear to be new cracks
濕敏預處理支線|Assess moisture-preconditioning branch|核對吸濕曝露與回焊模擬紀錄|Review moisture exposure and reflow-simulation records|歷程符合選定分類與試驗計畫|History matches the selected classification and test plan|不同預處理條件不可直接合併比较|Different preconditioning conditions cannot be pooled blindly
溫度循環負載|Interpret temperature-cycling loads|比較樣本實際溫度與箱體設定|Compare specimen temperatures with chamber settings|樣本達成計畫的循環與停留定義|Specimens meet planned cycle and dwell definitions|箱溫達標不等於樣品已達溫|Chamber temperature does not prove specimen equilibration
功率循環熱梯度|Interpret power-cycling gradients|讀取通電加熱期間晶粒與基板溫差|Read die-substrate differences during powered heating|熱梯度與任務機制具有關聯|Thermal gradients relate to the mission mechanism|功率循環不能等同均溫箱體循環|Power cycling is not equivalent to uniform chamber cycling
高溫儲存漂移|Assess high-temperature storage drift|比較無偏壓老化前後接點電阻|Compare contact resistance before and after unbiased aging|漂移依預定失效定義判定|Drift is judged against predefined failure definitions|無偏壓結果不能代表帶電遷移風險|Unbiased results do not represent biased migration risk
高溫操作壽命支線|Assess high-temperature operating-life branch|核對偏壓功耗與實際接面溫度|Verify bias, power, and actual junction temperature|電熱應力符合已核准的操作試驗|Electrical and thermal stress match the qualified test|只記箱溫會漏掉自發熱效應|Chamber temperature alone misses self-heating
溫濕偏壓失效|Assess temperature-humidity-bias failures|比較漏電隨時間與偏壓極性|Compare leakage over time and bias polarity|漏電及功能依計畫讀取點完整|Leakage and function are recorded at planned readouts|離箱乾燥可能暫時掩蓋濕氣失效|Drying outside the chamber can temporarily hide moisture failures
加速濕熱支線|Assess accelerated humidity-test branch|檢查壓力濕度溫度與材料相容性|Check pressure, humidity, temperature, and material compatibility|試验機制與目標使用環境可合理連結|Test mechanisms can reasonably connect to target service|過激條件可能產生非使用失效機制|Excessive stress can create irrelevant failure mechanisms
導體電遷移評估|Assess conductor electromigration|比較電流密度溫度與電阻時間曲線|Compare current density, temperature, and resistance history|失效判據與受測導體截面明確|Failure criteria and conductor cross sections are explicit|不計電流擁擠會低估局部應力|Ignoring current crowding underestimates local stress
介電時間依賴失效|Assess time-dependent dielectric failure|分析偏壓下漏電與失效時間|Analyze leakage and failure times under bias|介電受力與電極幾何均可追溯|Dielectric stress and electrode geometry are traceable|接觸短路不能誤歸為介電崩潰|Contact shorts must not be mislabeled dielectric breakdown
板級彎曲支線|Assess board-level bend branch|比對板應變與封裝接點開路事件|Compare board strain with joint-open events|失效事件具有同步應變證據|Failures have synchronized strain evidence|機台位移不能直接代表封裝附近應變|Machine travel does not directly represent local board strain
板級跌落支線|Assess board-level drop branch|同步讀取加速度與高速導通資料|Read acceleration and high-speed continuity together|瞬斷事件与實際衝擊時間對得上|Transient opens align with measured impact timing|事後直流量測可能漏掉短暫斷路|Posttest DC measurements can miss transient opens
機械振動共振|Assess vibration resonance|比較加速度傳遞率與夾具模態|Compare acceleration transmissibility and fixture modes|樣本負載可與夾具影響分離|Specimen loads can be separated from fixture effects|夾具共振可能被誤判為產品弱點|Fixture resonance can be mistaken for a product weakness
焊接界面老化|Assess solder-interface aging|比較介金屬層形貌及破面變化|Compare intermetallic morphology and fracture changes|組織變化與機械結果有一致證據|Microstructural changes agree with mechanical evidence|單一層厚數值不能代表全部脆化風險|One layer thickness cannot represent all embrittlement risks
非破壞電性定位|Localize faults electrically before sectioning|用網路對映比較開路與短路位置|Compare open and short locations through net mapping|失效定位保留多個可能原因|Localization retains plausible competing causes|過早鎖定單一原因會誤導切片|Premature commitment to one cause misdirects sectioning
時間域反射定位|Localize discontinuities with reflectometry|比較故障與良品反射波形|Compare failing and good-unit reflection traces|異常延遲與候選界面距離一致|Anomaly delay agrees with candidate interface distance|治具反射未去除會產生虛假定位|Unremoved fixture reflections create false localization
三維 X 光追蹤|Track defects with three-dimensional X-ray|沿互連方向追蹤疑似空隙或裂縫|Trace suspected voids or cracks along interconnects|缺陷在相鄰切片有連續證據|Defects have coherent evidence across adjacent slices|重建偽影不可當成真實裂紋|Reconstruction artifacts must not be treated as cracks
聲學分層定位|Localize delamination acoustically|把回波時間與材料層序對照|Compare echo timing with the material stack|分層介面定位有聲程依據|Delamination location is supported by acoustic path lengths|反射相位改變需排除材料差異|Phase changes require excluding material differences
截面製樣定位|Plan a failure-analysis cross section|以電性與非破壞影像決定截面位置|Choose section location using electrical and nondestructive data|截面穿過疑似缺陷且有方向記錄|Section crosses the suspected defect with recorded orientation|盲目切片可能錯過微小失效區|Unguided sectioning can miss small failure regions
截面 SEM 與元素判讀|Interpret cross-sectional SEM and composition|共同檢視形貌與元素分布|Review morphology and elemental distributions together|成分與幾何證據支持相同假說|Composition and geometry support the same hypothesis|研磨拖抹可能看似材料橋接|Polishing smear can resemble a material bridge
FIB 局部介面分析|Assess targeted FIB interface analysis|比較局部薄片與原始缺陷座標|Compare targeted sections with original defect coordinates|製樣位置及加工影響有記錄|Section location and preparation effects are recorded|離子加工再沉積可能製造假缺陷|Ion-beam redeposition can create apparent defects
壽命模型適用性|Check lifetime-model applicability|把失效機制與加速模型假設逐項對照|Match mechanisms against acceleration-model assumptions|外推範圍與信賴限制完整揭露|Extrapolation scope and confidence limits are explicit|跨機制套用加速因子會產生虛假壽命|Cross-mechanism acceleration factors produce false lifetime estimates
失效原因與改善驗證|Verify corrective-action causality|用對照批次確認改善前後相同失效機制|Use controlled lots to compare the same failure mechanism|改善效果可重現且未引入新失效|Improvement repeats without introducing new failures|良率上升本身不能證明根因已消除|Yield improvement alone does not prove root-cause removal
'''),
dict(n=20,title='終測、系統驗證與良率移交',titleEn='Final test, system validation, and yield handoff',
route='依邏輯、記憶體或 CPO 產品選測試支線；光學步驟只適用含光子元件的組件。',
routeEn='Select logic, memory, or CPO testing branches; optical steps apply only to photonic assemblies.',
principle='終測判斷當下功能，系統驗證判斷介面與任務行為；兩者均不等同完整壽命認證。',
principleEn='Final test assesses present function and system validation assesses interfaces and mission behavior; neither alone establishes full lifetime qualification.',
sources=['pkb-formfactor-packaging','pkb-amkor-characterization','pkb-keysight-optical','pkb-keysight-cpo'],rows='''
終測治具接點校驗|Validate final-test fixture contacts|比较參考樣本重複插拔的接觸電阻|Compare contact resistance across reference-unit insertions|治具接觸變異小於測試判定餘量|Fixture variability stays below decision margin|治具高阻可被誤判成封裝開路|Fixture resistance can mimic package opens
電源與地腳短路篩選|Screen power-ground shorts|在功能上電前判讀受限量測的電阻圖|Review constrained resistance maps before functional power-up|供電網路無非預期低阻路徑|Power nets have no unintended low-resistance paths|直接功能上電可能掩蓋初始短路來源|Immediate functional powering can obscure initial short origins
腳位導通覆蓋|Verify pin-continuity coverage|將測試項目覆蓋到每個設計腳位|Map test items to every designed pin|每種必要腳位有對應量測策略|Every required pin class has a measurement strategy|共用電源腳需要避免虛假的覆蓋宣稱|Shared power pins require avoiding false coverage claims
漏電與待機電流|Assess leakage and standby current|比較電壓溫度條件下的電流分布|Compare currents across voltage and temperature conditions|測試狀態明確且尾端分布達標|Test states are explicit and distribution tails pass|未固定邏輯狀態會混入動態電流|Uncontrolled logic states mix in dynamic current
掃描鏈測試對映|Map scan-chain failures|將掃描失效位置對映到實體晶粒|Map scan failures to physical dies|失效位址與測試版本可追溯|Failing addresses and test revisions are traceable|錯用測試版本可能造成全面假失敗|Wrong test revisions can cause widespread false failures
記憶體功能圖樣|Assess memory functional patterns|比較位址資料及保持類測試的覆蓋|Compare address, data, and retention-test coverage|目標故障類別都有可追溯測試|Target fault classes have traceable tests|單一讀寫圖樣不能覆蓋所有記憶體故障|One read-write pattern cannot cover all memory faults
晶粒間鏈路訓練|Validate die-to-die link training|追蹤每條通道訓練結果與補償量|Track training results and compensation per lane|所有必要通道在允許補償內收斂|Required lanes converge within allowed compensation|訓練成功仍可能只有很小時序餘量|Successful training can retain little timing margin
高速眼圖量測|Measure high-speed eye diagrams|比較去嵌入前後的眼高與眼寬|Compare eye height and width before and after de-embedding|採用指定參考平面與測試負載|Specified reference planes and loads are used|治具損耗未分離會低估封裝性能|Unseparated fixture loss can understate package performance
誤碼率與觀察時間|Assess bit error rate and observation duration|將錯誤數除以實際觀察位元數|Divide error count by actually observed bit count|報告包含位元分母與信賴限制|Reports include bit-count denominator and confidence limits|零錯誤不代表真實誤碼率為零|Zero observed errors do not establish zero true BER
供電瞬變響應|Measure power-delivery transients|比較負載階躍與晶粒端電壓波形|Compare load steps and die-side voltage waveforms|壓降及振鈴在供電容限內|Droop and ringing remain within supply tolerances|電源端穩定不代表晶粒端穩定|A stable source does not establish stable die-side voltage
溫度電壓性能邊界|Map performance across temperature and voltage|以一致測試版本比較條件矩陣|Compare a condition matrix using one test revision|功能及餘量覆蓋產品指定範圍|Function and margin cover specified product ranges|只在典型條件通過不能代表全範圍|Typical-condition passing does not cover the full range
系統工作負載熱點|Locate workload-driven system hotspots|比較多種代表工作負載的功耗地圖|Compare power maps for representative workloads|最高熱點與散熱設計限制相容|Hottest regions meet thermal design limits|總功耗相同不代表熱點相同|Equal total power does not imply equal hotspots
系統級間歇故障|Diagnose intermittent system faults|同步比對溫度鏈路錯誤與電源事件|Correlate temperature, link errors, and supply events|故障具有時間一致的診斷證據|Faults have time-consistent diagnostic evidence|未同步的紀錄可能造成假相關|Unsynchronized logs can produce spurious correlations
CPO 光纖端面檢查|Inspect CPO fiber end faces|在模擬影像中分類刮痕及污染|Classify scratches and contamination in simulated images|端面狀態符合連接器驗收規則|End faces meet connector acceptance rules|污染可能同時影響損耗與反射|Contamination can affect both loss and reflection
CPO 光耦合位置|Evaluate CPO optical coupling alignment|比較橫向軸向位移與耦合功率地圖|Compare lateral and axial offsets with coupling-power maps|耦合位置有足夠裝配誤差餘量|Coupling location retains assembly-error margin|只找最高點可能忽略極窄容差|Peak-only alignment can overlook narrow tolerance
CPO 固化位移|Measure CPO adhesive-cure shift|比較固定前後光功率與對位標記|Compare optical power and alignment marks before and after fixation|固化位移與功率變化符合介面預算|Cure shift and power change meet interface budgets|初始最佳對位不保證固化後最佳|Optimal initial alignment need not remain optimal after cure
CPO 插入損耗校準|Calibrate CPO insertion loss|比較參考路徑與待測路徑光功率|Compare reference-path and device-path optical power|連接器及線纜參考面定義一致|Connector and cable reference planes are consistent|未扣除治具損耗會誤估元件損耗|Unaccounted fixture loss biases device loss estimates
CPO 波長與偏振支線|Evaluate wavelength and polarization response|在規定範圍比較光功率響應|Compare optical responses over the specified ranges|最差波長與偏振仍符合規範|Worst-case wavelength and polarization meet criteria|單一波長功率合格不能代表全頻帶|Single-wavelength passing does not establish full-band performance
CPO 光電頻率響應|Measure CPO electro-optic response|以校正參考面比較幅相頻率曲線|Compare magnitude and phase against calibrated reference planes|量測涵蓋所需頻帶與動態範圍|Measurements cover required bandwidth and dynamic range|光功率穩定不能證明高速頻寬合格|Stable optical power does not prove high-speed bandwidth
CPO 光鏈路誤碼|Evaluate CPO optical-link errors|同步記錄光衰減與錯誤位元|Record optical attenuation and bit errors together|指定接收條件下誤碼證據完整|Error evidence is complete at specified receiver conditions|只量平均光功率無法識別時序錯誤|Average optical power cannot identify timing errors
CPO 溫漂與熱串擾|Assess CPO thermal drift and crosstalk|切換鄰近電子負載並追蹤光譜位移|Switch neighboring electrical loads and track spectral shifts|補償範圍涵蓋最差熱耦合狀態|Compensation covers worst thermal-coupling states|固定環境溫度仍可能有局部熱漂移|Fixed ambient temperature can coexist with local thermal drift
CPO 光纖應變釋放|Inspect CPO fiber strain relief|比較彎曲與拉力模型對耦合點位移|Compare bend and pull models at coupling points|機械擾動未耗盡光耦合餘量|Mechanical disturbance preserves coupling margin|封裝固定不等於光纖接頭無受力|A fixed package does not mean an unloaded fiber joint
多通道良率分解|Decompose multi-channel yield|把單晶粒堆疊封裝及通道良率分開計算|Separate die, stack, package, and channel yields|各良率分母與重測規則明確|Denominators and retest rules are explicit|直接相乘相關良率可能產生偏差|Multiplying correlated yields can bias estimates
測試再現性與誤判|Assess test repeatability and false calls|比較跨治具與跨時間的同樣本量測|Compare identical samples across fixtures and times|量測變異與產品變異可分離|Measurement variation separates from product variation|無限制重測會把真失效洗成通過|Unlimited retest can turn real failures into apparent passes
良率異常批次隔離|Isolate anomalous yield lots|以失效腳位空間圖定位共同製程因素|Use spatial failing-pin maps to locate shared process factors|隔離範圍有可追溯資料支持|Containment scope has traceable data support|僅按總良率隔離可能漏掉局部失效群|Total-yield containment can miss localized clusters
產品測試與譜系移交|Handoff product test and genealogy|封存材料版本晶粒來源測試與修復對映|Archive material revisions, die origins, tests, and repair maps|交付狀態與所有識別資料一致|Delivery status agrees with all identifiers|測試通過不能替代缺失的可靠度資格|Test passing cannot replace missing reliability qualification
'''),
]

MODULES += [
dict(n=17,title='底部填膠、上蓋與散熱整合',titleEn='Underfill, lid, and thermal integration',
route='依封裝選毛細充填、模封充填或預施膠；有蓋、無蓋及液冷介面是替代結構。',
routeEn='Select capillary, molded, or preapplied underfill; lidded, lidless, and liquid-cooled interfaces are alternative structures.',
principle='膠材承擔熱機械應力轉移，導熱介面承擔熱流；兩者功能不同，必須共同評估翹曲與熱阻。',
principleEn='Adhesives transfer thermomechanical stress while thermal interfaces carry heat; their different functions require joint warpage and thermal-resistance evaluation.',
sources=['pkb-henkel-underfill','pkb-henkel-lid','pkb-amkor-characterization'],rows='''
充填間隙流阻|Evaluate underfill gap-flow resistance|比較不同晶粒間隙的充填時間模型|Compare fill-time models for different die gaps|預期流動能在已驗證作業窗內完成|Predicted flow completes within the validated working window|間隙變小會顯著增加流動阻力|Smaller gaps substantially increase flow resistance
填膠材料可用狀態|Check underfill material working state|比對儲存解凍及可使用時間紀錄|Compare storage, thaw, and working-time records|材料狀態符合供應商核准要求|Material condition meets approved supplier requirements|外觀正常仍可能已超出可用時間|Normal appearance can conceal expired working time
填膠黏度溫度關係|Interpret underfill viscosity versus temperature|讀取材料流變曲線並與模型匹配|Match material rheology curves to the model|使用黏度對應實際溫度及剪切條件|Viscosity matches actual temperature and shear conditions|常溫單點黏度不能代表充填流動|One room-temperature viscosity cannot represent filling
焊點殘留與潤濕|Assess joint residue and underfill wetting|比較清潔狀態下的潤濕前緣|Compare wetting fronts for different cleanliness states|流前緣連續且無污染引起的停滯|Fronts remain continuous without contamination-induced arrest|助焊殘留可使局部拒膠|Flux residue can locally inhibit wetting
填膠點位設計|Plan underfill dispense locations|模擬不同邊緣點位的排氣路徑|Simulate venting for alternative edge dispense locations|點位保留連續排氣出口|Dispense locations preserve continuous vent outlets|多邊同時點膠可包圍未排出的氣體|Simultaneous multiedge dispensing can enclose air
點膠質量校準|Calibrate dispensed underfill mass|比較重量與光學體積估計|Compare mass with optical volume estimates|兩種估計在量測不確定度內一致|Estimates agree within measurement uncertainty|針頭拉絲會使重量與落點不一致|Needle stringing can separate dispensed mass from intended placement
晶粒邊緣膠前緣|Track the die-edge underfill front|讀取透明模型的時間序列|Read time-series images from the transparent model|前緣到達遠端且未留未填區|Front reaches the far side without unfilled regions|可見邊緣濕潤不代表底部已充滿|Visible edge wetting does not prove complete bottom filling
充填膠圓角|Measure underfill fillets|量測四邊膠圓角高度與延伸距離|Measure fillet height and extension on all sides|圓角不侵入接點或光學保留區|Fillets avoid contact and optical keep-out regions|過大圓角可增加局部剛性或污染|Excessive fillets can increase stiffness or contaminate adjacent regions
固化反應程度|Assess underfill cure state|比較殘餘反應熱與參考樣本|Compare residual reaction heat with reference samples|反應程度與核准固化狀態一致|Cure state agrees with the qualified reference|爐內溫度紀錄不能直接證明膠體固化|Oven temperature records alone do not prove adhesive cure
填膠玻璃轉移行為|Interpret underfill glass transition|比較模數隨溫度曲線與使用範圍|Compare modulus-temperature curves with service range|模型涵蓋轉移區前後的材料變化|Models cover material changes across the transition|單一常數模數可低估溫度依賴應力|Constant modulus can underestimate temperature-dependent stress
填膠空洞聲學檢查|Inspect underfill voids acoustically|判讀不同焦深的介面回波|Interpret interface echoes at multiple focal depths|空洞位置與面積符合允收規則|Void location and area meet acceptance rules|反射差異需先排除幾何與耦合因素|Contrast requires excluding geometry and coupling effects
晶粒角落應力|Evaluate die-corner stress|比較角落網格收斂後的應力指標|Compare converged stress measures near die corners|設計指標對網格細化已穩定|Design indicators stabilize with mesh refinement|奇異點峰值不能直接當材料失效值|Singular peak stress cannot directly represent material failure
上蓋接觸面平整度|Measure lid contact-face flatness|比較上蓋內表面與晶粒高度圖|Compare lid inner surface and die-height maps|接觸面幾何允許目標介面厚度|Contact geometry permits the target bondline thickness|上蓋外表面平坦不代表內面平坦|Flat outer surfaces do not establish inner-face flatness
多晶粒高度補償|Plan multi-die height compensation|比較不同晶粒頂面與上蓋台階|Compare die tops and lid pedestal heights|各晶粒可在容許厚度內接觸導熱層|All dies contact thermal layers within allowed thickness|最高晶粒可能承受過多裝配載荷|The tallest die can carry excessive assembly load
導熱介面材料選擇|Compare thermal-interface material branches|比較接觸熱阻及機械順應性|Compare contact resistance and mechanical compliance|材料兼顧熱阻與封裝應變需求|Material meets thermal resistance and strain needs|高本體導熱率不保證低接觸熱阻|High bulk conductivity does not ensure low contact resistance
導熱層塗佈覆蓋|Inspect thermal-interface coverage|比較塗佈圖形與實際發熱區|Compare deposited patterns with heat-producing regions|目標熱區連續覆蓋且不污染保留區|Hot regions are covered without contaminating keep-outs|只看總塗佈量會漏掉熱點缺膠|Total deposited mass can hide uncovered hotspots
導熱層厚度控制|Control thermal-interface thickness|以支撐幾何推算壓合後厚度|Infer compressed thickness from support geometry|厚度與接觸壓力均在材料工作窗內|Thickness and pressure meet material operating windows|過薄層可能無法吸收翹曲間隙|An overly thin layer may not accommodate warpage gaps
上蓋膠路點膠|Inspect lid-adhesive dispense paths|檢查膠路連續性與排氣設計|Inspect adhesive-path continuity and vent design|膠路符合結構需求且未封堵必要排氣|Paths meet structural needs without blocking required vents|連續封閉膠環未必適合所有封裝|A closed adhesive ring is not suitable for every package
補強環放置|Place a stiffener ring virtually|比較補強環與基板邊界位置|Compare stiffener positions with substrate boundaries|對位及接觸不干涉焊墊與元件|Alignment and contact avoid pads and components|偏移補強環可改變局部翹曲約束|Shifted stiffeners alter local warpage constraints
上蓋壓合載荷分布|Assess lid-attach load distribution|比較載荷圖與晶粒支撐點|Compare load maps and die support locations|局部壓力不超過核准機械限制|Local pressure remains within approved mechanical limits|總載荷合格仍可能有局部過壓|Acceptable total load can hide local overpressure
上蓋固化後翹曲|Map postcure package warpage|在共同溫度下量測上蓋與基板曲面|Measure lid and substrate shape at a common temperature|整體翹曲保留板級組裝餘量|Package warpage preserves board-assembly allowance|固化收縮可使上蓋與基板相互拉彎|Cure shrinkage can bow lid and substrate together
介面泵出支線|Assess thermal-interface pump-out|比較熱循環前後材料邊界與熱阻|Compare material edges and thermal resistance after cycling|邊界遷移與熱阻變化符合耐久目標|Migration and resistance change meet durability targets|初始熱阻低仍可能有長期材料泵出|Low initial resistance does not exclude long-term pump-out
封裝熱阻量測|Measure package thermal resistance|用已校正溫感與功耗計算溫升|Calculate temperature rise using calibrated sensors and power|測試邊界及功耗定義完整可重現|Boundary conditions and power definitions are reproducible|未定義冷卻邊界無法比較熱阻|Undefined cooling boundaries invalidate thermal comparisons
瞬態熱路分析|Interpret transient thermal paths|比較熱階躍響應與結構模型|Compare thermal-step responses with structure models|主要時間常數與模型界面一致|Major time constants agree with modeled interfaces|單一穩態值可能掩蓋介面分層|A steady-state value can hide interface separation
液冷冷板支線|Assess a liquid-cold-plate branch|比對接觸壓力流量及洩漏測試紀錄|Compare contact pressure, flow, and leak-test records|熱與機械介面均滿足系統規範|Thermal and mechanical interfaces meet system criteria|增加流量不能補救不良固體接觸|Increasing flow cannot remedy poor solid contact
熱機耦合介面放行|Release coupled thermal-mechanical interfaces|同時檢視熱阻翹曲與介面完整性|Review thermal resistance, bow, and interface integrity together|三者均達標且使用相同樣品識別|All pass with consistent specimen identity|混用不同樣品資料會形成虛假通過|Mixing specimens can produce a false combined pass
'''),
dict(n=18,title='植球、基板組裝與外觀終檢',titleEn='Ball attach, substrate assembly, and final inspection',
route='BGA 對外焊球支線；LGA、裸晶模組與光學連接器採其他端接形式。',
routeEn='External BGA solder-ball branch; LGA, bare-die modules, and optical connectors use other terminations.',
principle='對外焊球的數量、共平面度與潤濕品質連接封裝與板級製造，必須區分封裝缺陷與後續貼板缺陷。',
principleEn='Ball count, coplanarity, and wetting connect package and board assembly; package defects must be distinguished from later board-attach defects.',
sources=['pkb-nordson-axi','pkb-nordson-wafer','pkb-amkor-characterization'],rows='''
基板焊墊清潔度|Inspect substrate-pad cleanliness|比較焊墊表面影像與污染指標|Compare pad images and contamination indicators|可焊表面無阻礙潤濕的污染|Solderable surfaces lack wetting-blocking contamination|外觀明亮不一定代表無有機殘留|Bright appearance does not exclude organic residue
植球焊墊定義|Verify ball-pad definition|區分防焊定義與非防焊定義焊墊|Distinguish solder-mask-defined and nonsolder-mask-defined pads|焊墊形態與設計資料一致|Pad geometry matches the design definition|使用錯誤焊墊模型會誤估應力|Wrong pad models misestimate stress
焊球合金版本|Verify solder-ball alloy revision|核對球材識別與接合材料清單|Match ball identity to joining material lists|合金版本與核准熱歷程相容|Alloy revision matches the qualified thermal history|外形相同的合金可能有不同接合需求|Identical ball geometry can hide different joining needs
焊球尺寸分布|Measure solder-ball size distribution|比較抽樣直徑與體積統計|Compare sampled diameter and volume statistics|尺寸尾端符合規定的批次限制|Distribution tails meet lot limits|只報平均直徑會漏掉過大過小球|Mean diameter hides oversized and undersized balls
助焊劑塗佈厚度|Inspect flux-coating thickness|量測印刷或轉印後膜厚地圖|Measure printed or transferred flux-thickness maps|每個焊墊覆蓋量在核准窗內|Coverage per pad remains within approved windows|局部缺膠可造成球材暫時固定不足|Insufficient flux can weaken temporary ball retention
植球模板孔位|Verify ball-placement stencil apertures|將模板孔座標與基板焊墊重疊|Overlay stencil apertures with substrate pads|孔位與避讓區對應正確|Apertures and exclusion zones map correctly|模板方向反置會造成系統性漏球|Reversed stencils cause systematic missing balls
單球落位|Inspect individual ball seating|觀察每個孔位的球數與偏心|Inspect ball count and eccentricity at each site|每個指定焊墊恰有一顆球|Each specified pad carries exactly one ball|雙球或偏球可能在回焊後橋接|Double or off-center balls can bridge after reflow
植球後漏球檢測|Detect missing balls after placement|比對實際球圖與設計球圖|Compare actual and designed ball maps|所有應植位置都有可辨識球體|Every populated position contains a detectable ball|設計空位不可被誤判成漏球|Intentional vacancies must not be labeled missing balls
焊球暫固定搬運|Evaluate ball retention during transfer|比較搬運前後球心座標|Compare ball centers before and after transfer|球體未滑移或脫落|Balls neither slip nor detach|搬運振動可能改變未回焊球位|Transfer vibration can move unreflowed balls
回焊熱電偶位置|Plan reflow temperature sensing|選取熱容量差異最大的監測位置|Select monitoring locations with contrasting thermal mass|最冷及最熱位置都有量測代表|Cold and hot locations are represented|只放中央感測器會漏掉邊緣差異|Center-only sensing misses edge differences
回焊熱歷程核對|Verify ball-attach reflow history|將球材與封裝限制共同套用到溫度曲線|Apply alloy and package limits to temperature histories|接點與封裝材料限制同時满足|Joint and package material limits both pass|焊料達成接合不代表封裝未受熱傷害|Joined solder does not prove an undamaged package
回焊時翹曲|Assess warpage during reflow|比较加熱與冷卻中的共平面度|Compare coplanarity during heating and cooling|高溫接觸幾何仍符合接合預算|Hot contact geometry still fits joining budgets|室溫平坦不能排除高溫翹曲|Room-temperature flatness does not exclude hot warpage
焊球自對準判讀|Interpret solder-ball self-alignment|比較回焊前後球心與焊墊中心|Compare ball and pad centers before and after reflow|球心偏差收斂且未發生鄰球接觸|Offsets converge without contacting adjacent balls|表面張力不能修正任意大的初始偏位|Surface tension cannot correct arbitrary initial offsets
潤濕角與球高|Measure wetting shape and ball height|由側視輪廓量測球高與接觸區|Measure ball height and contact region from profiles|幾何與核准焊墊及球體組合相容|Geometry matches the qualified pad-ball combination|球高異常可能來自體積或潤濕差異|Height anomalies can reflect volume or wetting differences
焊球橋接判讀|Inspect solder-ball bridges|比較相鄰球之間的三維分離|Inspect three-dimensional separation between neighbors|不同網路焊球保持分離|Balls on different nets remain separate|二維投影重疊不一定是真實橋接|Projection overlap is not always a physical bridge
焊球空洞分析|Assess solder-ball voids|分離投影面積與三維空洞體積|Separate projected area from three-dimensional void volume|採用與規格相符的空洞定義|Void metrics use the definition required by specification|混用面積率與體積率會誤判|Mixing area and volume fractions misclassifies voiding
回焊殘留清潔|Verify postreflow residue cleaning|檢查球根與防焊邊界殘留|Inspect residue around ball roots and mask edges|清潔後無超規殘留或侵蝕|No out-of-limit residue or attack remains|球頂潔淨可能掩蓋球根殘留|Clean ball tops can hide residues at their bases
焊球共平面度|Measure final ball coplanarity|擬合基準平面後量測各球最低點|Measure ball lowest points against a fitted reference plane|所有端點符合組裝共平面規範|All terminals meet assembly coplanarity criteria|基準平面選錯會系統性低估偏差|Wrong reference planes systematically understate variation
焊球剪切破面|Interpret ball-shear fracture surfaces|聯合比較剪切載荷與界面破面|Compare shear load and interface fracture surfaces|破壞模式及載荷均符合評估規則|Failure mode and load both meet evaluation rules|高剪力仍可能伴隨脆性介面破壞|High force can coexist with brittle interface fracture
封裝外形尺寸|Verify package outline dimensions|比較外形高度與圖面公差|Compare outline and height with drawing tolerances|外形及高度滿足系統裝配限制|Outline and height meet system assembly limits|局部毛邊可超出整體外形平均值|Local flash can exceed average outline dimensions
基板去框分離|Assess substrate singulation|檢查分離面與焊球鄰近區域|Inspect singulated edges and nearby ball regions|無超規裂紋毛邊及焊球損傷|No unacceptable cracks, burrs, or ball damage|分離應力可能傳入內部接點|Singulation stress can reach internal joints
頂面標記辨識|Validate package marking readability|比對光學讀碼與實際產品識別|Compare optical decoding and actual product identity|標記清晰且識別內容完全一致|Marks are readable and match product identity|可讀取的錯誤標記仍屬追溯失效|Readable but incorrect marks still break traceability
封裝表面異物|Inspect package surface foreign material|區分刮痕纖維與材料原有紋理|Distinguish scratches, fibers, and native texture|異物及刮痕依各自規則判讀|Foreign matter and scratches use their own criteria|把原有紋理當異物會增加誤判|Native texture mistaken for debris increases false calls
托盤接觸與方向|Verify tray support and orientation|檢查支撐點與球體避讓|Inspect tray supports and ball clearance|托盤不對焊球施加不當載荷|Trays avoid inappropriate ball loading|方向錯誤可使焊球承受機械壓力|Wrong orientation can place load on solder balls
防潮包裝狀態|Verify moisture-protective packing state|核對乾燥劑指示卡封口與曝露紀錄|Check desiccant, indicator, seal, and exposure records|記錄與所選防潮分類相容|Records agree with the selected moisture classification|封袋完整不代表封袋前曝露合格|An intact bag does not prove acceptable prior exposure
外觀電性關聯終檢|Correlate final appearance and electrical defects|將缺球偏球與失效腳位共同套圖|Overlay missing or shifted balls with failing pins|缺陷與腳位對應可追溯|Defects and pin mappings are traceable|外觀正常不能排除隱藏開路|Normal appearance does not exclude hidden opens
'''),
]

MODULES += [
dict(n=13,title='矽中介層與 2.5D 系統整合',titleEn='Silicon interposers and 2.5D system integration',
route='矽中介層支線；RDL 中介層與局部矽橋是另類架構，需另選介面與製程。',
routeEn='Silicon-interposer branch; RDL interposers and local silicon bridges use different interfaces and flows.',
principle='中介層連接多顆晶粒；互連拓撲、機械變形與良品晶粒選擇共同影響組裝結果。',
principleEn='Interposers connect multiple dies; interconnect topology, deformation, and known-good-die selection jointly affect assembly.',
sources=['pkb-tsmc-cowos','pkb-amkor-characterization','pkb-formfactor-kgd'],rows='''
中介層晶粒腳位對映|Map die pins onto the interposer|把晶粒焊墊網表與中介層接點逐一比對|Compare die-pad netlists with interposer contacts|電源地與訊號對映沒有衝突|Power, ground, and signal mappings have no conflicts|鏡射座標錯誤可對接到錯誤網路|Mirrored coordinates can connect the wrong nets
中介層尺寸與曝光邊界|Check interposer size and exposure boundaries|標記拼接邊界及跨界金屬路徑|Mark stitching boundaries and crossing metal routes|跨界互連有對應的套準驗證|Boundary-crossing interconnects have overlay verification|拼接偏移可能在長線形成頸縮|Stitching offsets can neck long conductors
介層金屬導通鏈|Test interposer metal chains|對不同線長比較四端鏈阻|Compare four-terminal chain resistance across lengths|電阻隨長度變化符合結構模型|Resistance versus length agrees with structural models|截距異常可能來自接點而非線寬|An abnormal intercept may indicate contacts rather than width
中介層層間短路|Screen interposer interlayer shorts|比較相鄰金屬層測試梳狀結構|Evaluate comb structures between adjacent metal layers|非相連網路保持規定隔離|Unconnected nets maintain specified isolation|介電缺陷可在層間形成漏電|Dielectric defects can create interlayer leakage
中介層 TSV 端點對映|Map interposer TSV endpoints|追蹤上層網路穿越 TSV 到下層焊墊|Trace upper nets through TSVs to lower pads|端點及極性與設計資料一致|Endpoints and polarities match design data|僅查頂層可能漏掉底層換位|Top-only review can miss backside swaps
介層微凸塊共平面度|Measure interposer microbump coplanarity|比較每顆晶粒區域的凸塊高度分布|Compare bump heights within each die footprint|局部共平面度符合接合行程預算|Local coplanarity fits the bonding stroke budget|全片平均會掩蓋單顆晶粒區傾斜|Wafer averages hide local footprint tilt
中介層切割道保護|Inspect interposer dicing streets|疊合切割軌跡與金屬保護邊界|Overlay cutting paths and protected metal boundaries|切割侵入量未接近有效互連|Cut encroachment avoids functional interconnects|邊緣裂縫可沿介電層擴展|Edge cracks can extend along dielectric layers
中介層切割後邊緣|Inspect singulated interposer edges|量測角落崩角及裂紋方向|Measure corner chips and crack directions|崩角未越過核准保留區|Chipping remains outside protected regions|只量崩角面積會漏看長裂紋|Chip area alone can miss long cracks
中介層載台支撐|Evaluate interposer assembly support|檢查支撐點與薄區變形模型|Inspect support positions and thin-region deformation|放晶時局部撓度符合對位預算|Local deflection fits placement alignment budgets|支撐空窗可導致放晶位置漂移|Unsupported spans can shift placement positions
邏輯晶粒良品對位|Match known-good logic dies|以晶圓座標與測試狀態核對取晶清單|Match wafer coordinates and test states to pickup lists|只選取狀態有效的指定晶粒|Only specified dies with valid status are selected|座標旋轉錯誤會取到鄰近失效晶粒|Coordinate rotation errors select adjacent failing dies
記憶體堆疊入料匹配|Match incoming memory stacks|比對堆疊版本與介層介面需求|Compare stack revisions with interposer interface requirements|電性介面與尺寸版本皆相容|Electrical interfaces and geometry revisions are compatible|相同外形不保證介面版本一致|Identical outlines do not establish interface compatibility
中介層助焊材圖形|Inspect interposer flux patterns|比較轉印覆蓋與晶粒間禁沾區|Compare transferred coverage and interdie exclusion zones|焊墊覆蓋足夠且禁沾區清潔|Pads have coverage while exclusion zones stay clean|過量助焊材可困在細間距縫隙|Excess flux can become trapped in fine gaps
第一顆邏輯晶粒放置|Place the first logic die virtually|以雙視野標記求解平移與轉角|Solve translation and rotation from dual-field marks|各角落偏差均在核准範圍|All corner offsets remain within approved limits|中心對準仍可能有角度誤差|Center alignment can coexist with rotation error
第二晶粒相對位置|Check relative position of neighboring dies|量測兩晶粒間距及相互傾斜|Measure interdie spacing and relative tilt|間隙滿足點膠與散熱結構需求|Clearance supports dispense and thermal structures|間距不足可阻斷後續充填流道|Insufficient spacing can block underfill paths
記憶體堆疊放置|Place memory stacks virtually|比對堆疊重心與支撐區域|Compare stack centers of mass with support regions|堆疊位置及傾斜符合組裝規範|Stack position and tilt meet assembly specifications|較高堆疊易受工具偏載影響|Tall stacks are sensitive to uneven tool loading
多晶粒共同回焊支線|Evaluate a collective-reflow branch|比較多晶粒區的熱歷程與焊點收縮|Compare thermal histories and joint collapse across dies|所有接點皆進入合格的熱歷程窗|All joints meet qualified thermal-history windows|熱容量差異可造成局部未充分接合|Thermal-mass differences can leave incomplete joints
逐晶粒熱壓接合支線|Evaluate sequential thermocompression bonding|追蹤單顆熱壓對鄰近已接晶粒的影響|Track local bonding effects on previously attached neighbors|新接點合格且既有接點未劣化|New joints pass without degrading existing joints|重複熱負載可能改變先前接點|Repeated thermal loads can alter earlier joints
互連塌陷高度|Measure interconnect collapse height|比較接合前後間隙與凸塊高度|Compare gap and bump height before and after joining|塌陷量與最終間隙均符合設計|Collapse and final gap both meet design requirements|塌陷不足與過度塌陷都有風險|Both insufficient and excessive collapse are problematic
中介層接合後翹曲|Map postbond interposer warpage|在同一溫度基準比較接合前後曲面|Compare prebond and postbond shapes at one temperature|曲面變形未耗盡後續基板接合餘量|Deformation preserves downstream substrate bonding allowance|不同量測溫度會混淆製程效應|Different measurement temperatures confound process effects
中介層充填流道|Inspect interposer underfill flow paths|在模型追蹤多晶粒下方充填前緣|Track underfill fronts beneath multiple dies|流道連通且未封住中央排氣路徑|Paths remain connected without trapping central air|相向流前緣可包圍氣泡|Opposing fronts can enclose bubbles
介層至基板凸塊檢查|Inspect interposer-to-substrate bumps|比對底部凸塊地圖與基板焊墊|Compare bottom-bump maps with substrate pads|凸塊位置高度與焊墊相容|Bump position and height match substrate pads|中介層頂部合格不等於底部合格|A passing top interface does not establish bottom quality
矽中介層基板放置|Place the silicon interposer on substrate|模擬補償基板膨脹後的標記對準|Simulate fiducial alignment with substrate expansion compensation|各區域接點重疊符合接合需求|Contact overlap meets bonding needs across regions|僅補償平移無法修正尺寸伸縮|Translation correction cannot fix scale changes
基板接合熱歷程|Verify substrate-attach thermal history|比較晶粒頂面與底部焊點的模擬溫度|Compare die-top and bottom-joint temperatures|焊點合格且晶粒不超過材料限制|Joints qualify without exceeding die material limits|底面達溫不能保證頂部材料安全|Bottom temperature does not establish top-material compatibility
介層電源回路阻抗|Inspect interposer power-loop impedance|比较電源與回流路徑的阻抗曲線|Compare power and return-path impedance curves|峰值與低頻壓降符合供電預算|Peaks and low-frequency drop fit power budgets|良好直流電阻不代表高頻低阻抗|Good DC resistance does not establish low high-frequency impedance
中介層訊號串擾|Evaluate interposer signal crosstalk|比較相鄰通道的耦合響應|Compare coupling responses between neighboring channels|耦合干擾未超過通道預算|Coupled interference stays within channel budgets|只看單線損耗會漏掉相鄰干擾|Single-line loss misses neighboring interference
2.5D 整合缺陷關聯|Correlate 2.5D integration defects|疊合晶粒位置接合影像及失效網路|Overlay placement, joint images, and failing nets|缺陷定位有跨資料證據支持|Defect location is supported by multiple data types|只靠一張影像可能誤歸因|A single image can support a false attribution
'''),
dict(n=14,title='有機與玻璃載板增層製作',titleEn='Organic and glass substrate build-up',
route='有機芯或玻璃芯支線；玻璃通孔與有機鑽孔各用其合格路線，不可互換製程參數。',
routeEn='Organic-core or glass-core branch; glass vias and organic drilling use separately qualified routes.',
principle='增層介電、微孔與金屬圖形共同建立多層載板；粗糙度、附著與電損耗具有取捨。',
principleEn='Build-up dielectrics, microvias, and metal patterns form multilayer substrates; roughness, adhesion, and electrical loss trade off.',
sources=['pkb-dupont-substrate','pkb-atotech-glass','pkb-atotech-sap'],rows='''
載板芯材平面度|Map substrate-core flatness|比較入料芯材的厚度及翹曲分布|Compare incoming core thickness and warpage distributions|幾何誤差在增層與搬運公差內|Geometry fits build-up and handling tolerances|芯材彎曲可累積為套準誤差|Core bow can accumulate into registration error
有機芯材含水判讀|Assess organic-core moisture|比較材料調理紀錄與含水代理量測|Compare conditioning records and moisture proxies|材料狀態符合核准壓合前要求|Material condition meets approved prelamination needs|受潮會改變尺寸與介電表現|Moisture changes dimensions and dielectric behavior
玻璃芯邊緣裂紋|Inspect glass-core edge cracks|用偏光與顯微影像定位邊緣缺陷|Locate edge defects using polarized and microscopic images|裂紋未侵入機械保留區|Cracks do not enter protected mechanical regions|細小邊裂可能於後續熱循環擴展|Small edge cracks can grow during thermal cycling
有機芯通孔鑽孔支線|Inspect organic-core drilled holes|比較孔壁粗糙與樹脂拖抹影像|Compare hole-wall roughness and resin-smear images|孔形及孔壁可接受後續金屬化|Hole geometry supports subsequent metallization|樹脂拖抹會遮住內層銅接點|Resin smear can cover inner-layer copper contacts
玻璃通孔成孔支線|Inspect through-glass via formation|量測玻璃孔錐度與出口崩角|Measure glass-via taper and exit chipping|孔形及崩角符合金屬化能力|Geometry and chipping fit metallization capability|出口裂紋可降低熱循環耐受|Exit cracks can reduce thermal-cycle endurance
孔壁去污判讀|Verify hole-wall desmear|比較孔內殘留與內層銅露出|Compare hole residue and exposed inner copper|殘留受控且內層接點未被侵蝕|Residue is controlled without attacking inner contacts|過度處理可損傷介電與銅界面|Excess treatment can damage dielectric-copper interfaces
玻璃附著促進支線|Evaluate glass adhesion promotion|比對處理前後附著試片結果|Compare adhesion coupon results before and after treatment|金屬附著經環境考驗仍達標|Metal adhesion passes after environmental exposure|表面導電不等於金屬牢固附著|Surface conductivity does not establish robust adhesion
化學銅種子覆蓋|Inspect electroless copper seed coverage|查看孔壁及孔口種子連續性|Inspect seed continuity on via walls and mouths|孔壁形成連通導電層|Via walls form a connected conductive film|局部種子缺口會形成電鍍空區|Seed gaps cause unplated regions
芯材通孔銅鍍層|Measure core through-hole copper|比較孔口孔腰與孔底鍍層|Compare copper at mouths, waists, and bottoms|最薄孔壁符合可靠度設計要求|Thinnest wall meets reliability design requirements|平面鍍層合格可能掩蓋孔腰不足|Passing surface copper can hide a thin via waist
芯材表面銅圖形|Inspect core copper patterns|疊合導線輪廓與設計網表|Overlay conductor contours and design netlists|連線正確且無線間銅殘留|Connections are correct without intertrace copper residue|局部殘銅可形成高阻短路|Residual copper can create resistive shorts
增層膜貼合氣泡|Inspect build-up-film lamination bubbles|沿導線台階觀察膜下氣泡|Inspect trapped bubbles near conductor steps|台階周圍填實且無未黏合空區|Steps are filled without unbonded cavities|導線旁困氣可轉變成層間空洞|Trapped air near traces becomes interlayer voids
增層介電厚度|Measure build-up dielectric thickness|比較銅線頂部與線間介電厚度|Compare dielectric above traces and between traces|最薄區仍符合絕緣與阻抗要求|Thinnest regions meet insulation and impedance needs|名義膜厚不代表銅頂剩餘厚度|Nominal film thickness is not the remaining thickness above copper
介電固化收縮|Evaluate dielectric cure shrinkage|比較壓合前後標記座標距離|Compare fiducial distances before and after lamination|尺寸變化可被既定套準策略補償|Dimensional change fits the registration strategy|各方向收縮不同不能以單一比例修正|Anisotropic shrinkage resists one-factor scale correction
微孔雷射位置|Check laser microvia registration|疊合微孔中心與埋藏銅墊|Overlay microvia centers and buried capture pads|孔中心保留足夠落墊邊界|Centers retain sufficient capture-pad margin|偏孔可在接點邊緣造成弱連接|Offset vias create weak edge connections
微孔底殘留|Inspect microvia-bottom residue|比較孔底反射影像與剖面|Compare bottom reflectance images and cross sections|目標銅墊有完整可金屬化表面|Capture pads expose metallizable surfaces|孔底殘膠可能造成間歇開路|Bottom residue can produce intermittent opens
增層介電表面粗糙度|Assess build-up dielectric surface roughness|比較附著力與高頻損耗的對照資料|Compare adhesion and high-frequency loss data|粗糙度同時滿足附著及損耗目標|Roughness meets adhesion and loss targets|單純提高粗糙度可能增加傳輸損耗|Increasing roughness can increase transmission loss
乾膜光阻貼合|Inspect dry-film resist lamination|檢查微孔附近光阻架橋與空氣夾入|Inspect resist tenting and trapped air near microvias|光阻貼合完整且開孔區可圖形化|Resist adheres and openings remain patternable|光阻懸空可導致顯影形狀失真|Unsupported resist can distort developed shapes
雷射直寫套準|Verify laser direct-imaging registration|以分區標記修正面板尺寸變化|Use regional fiducials to correct panel distortion|局部殘差低於圖形套準容許量|Local residuals meet pattern-registration allowance|全板剛體修正可能不足以補償變形|Rigid correction can miss panel distortion
細線光阻側壁|Inspect fine-line resist walls|量測底部開口及相鄰牆體完整性|Measure bottom openings and neighboring wall integrity|光阻壁可分隔目標導線|Resist walls separate the intended conductors|過薄光阻牆容易在電鍍時失穩|Thin resist walls can destabilize during plating
盲微孔填銅|Assess blind-microvia copper filling|比較孔底填充與上方鍍層成長|Compare bottom fill with top copper growth|孔內填實且表面凹陷受控|Vias fill while surface dimples remain controlled|頂部先封閉會留下隱藏接縫|Early top closure leaves hidden seams
圖形電鍍線高|Map pattern-plated trace height|比較密集與孤立導線的高度|Compare dense and isolated trace heights|不同密度線高都在規格範圍|Trace heights pass across pattern densities|電流集中可使孤立線過高|Current crowding can overplate isolated lines
種子蝕刻側蝕|Measure seed-etch undercut|比較去種子前後導線底寬|Compare trace-foot widths before and after seed removal|底寬保留符合導通與附著需求|Retained foot width supports conduction and adhesion|過大側蝕會削弱細線支撐|Excess undercut weakens fine-trace support
增層微孔堆疊支線|Inspect stacked-microvia interfaces|在堆疊孔截面追蹤界面接觸|Trace interface contact in stacked-via cross sections|上下微孔介面接觸連續|Stacked-via interfaces maintain continuous contact|介面凹陷可成為疲勞弱點|Interface dimples can become fatigue weak points
防焊層開口|Inspect solder-mask openings|比對防焊邊界與焊墊設計|Compare mask boundaries and pad designs|開口保留所選焊墊定義方式|Openings preserve the chosen pad-definition scheme|開口偏移可改變有效潤濕面積|Misregistration changes effective wettable area
表面處理可焊性|Assess final-finish solderability|比較表面成分與潤濕試片|Compare finish composition and wetting coupons|表面處理與接合合金相容|Finish is compatible with the joining alloy|局部污染可造成不潤濕|Local contamination can cause nonwetting
載板電測與尺寸放行|Release substrate electrical and dimensional data|聯合判讀開短路結果與焊墊位置圖|Review continuity tests and pad-coordinate maps together|電性與尺寸兩項均符合組裝介面|Electrical and dimensional results meet assembly interfaces|僅電測合格不保證可正確貼裝|Electrical passing alone does not establish mountability
'''),
]

MODULES += [
dict(n=15,title='混合鍵合與直接接合對準',titleEn='Hybrid bonding and direct-bond alignment',
route='晶圓對晶圓、直接晶粒對晶圓及集合轉移為替代支線；混合鍵合不能視為微凸塊回焊。',
routeEn='Wafer-to-wafer, direct die-to-wafer, and collective transfer are alternative branches; hybrid bonding is not microbump reflow.',
principle='混合鍵合同時依靠介電與金屬介面；顆粒、局部平坦度、銅高度差與對位都必須受控。',
principleEn='Hybrid bonding combines dielectric and metal interfaces; particles, local flatness, copper height, and alignment must all be controlled.',
sources=['pkb-evg-hybrid','pkb-besi-hybrid','pkb-tsmc-soic'],rows='''
鍵合路線幾何匹配|Match geometry to a bonding route|比較晶粒尺寸與晶圓良率分布案例|Compare die-size and wafer-yield cases|所選路線能容納尺寸與良品分布|The selected route accommodates geometry and good-die distribution|相同流程不適合所有異尺寸晶粒|One flow does not suit all unequal die sizes
混合鍵合層序核對|Check hybrid-bond layer sequence|比對兩側銅墊與介電層剖面|Compare copper-pad and dielectric cross sections on both sides|材料配對與層序符合核准介面|Materials and layers match the approved interface|金屬相接不能補救介電不相容|Metal contact cannot remedy incompatible dielectric bonding
CMP 局部平坦度|Measure local CMP flatness|在銅墊群與介電區量測形貌|Measure topography across pad groups and dielectric regions|局部起伏符合接合表面規範|Local topography meets bonding-surface criteria|整片平坦仍可能有局部凹凸|Global flatness can hide local topography
銅墊凹入深度|Measure copper-pad recess|比較銅與相鄰介電表面高度|Compare copper and neighboring dielectric heights|高度差符合所選熱歷程設計|Height difference fits the selected thermal-history design|凹入太深可能無法形成金屬接觸|Excess recess can prevent metal contact
鍵合介電表面粗糙度|Measure bonding-dielectric roughness|比較不同掃描範圍的表面統計|Compare surface statistics at multiple scan scales|粗糙度與局部缺陷均受控|Roughness and local defects are controlled|只看單一均方根值會漏掉顆粒|A single RMS value can miss particles
銅墊腐蝕檢查|Inspect copper-pad corrosion|對照表面影像與元素訊號|Compare surface images and elemental signals|銅墊無超出規則的腐蝕區|Pads lack corrosion beyond acceptance rules|腐蝕可使墊面凹入且增加接觸阻抗|Corrosion recesses pads and raises contact impedance
晶粒切割污染路徑|Map singulation contamination paths|比較保護前後接合面的顆粒地圖|Compare bonding-surface particle maps across protection cases|切割污染未進入有效接合區|Singulation contamination stays outside active bond areas|切割邊緣潔淨不代表面內潔淨|Clean edges do not establish a clean bonding face
接合面清洗驗證|Verify bonding-surface cleaning|比對顆粒數與有機殘留訊號|Compare particle counts and organic-residue signals|兩種污染指標均符合接合規範|Both contamination indicators meet bonding criteria|去除顆粒後仍可能殘留有機物|Particle removal can leave organic residues
表面活化狀態|Assess surface activation state|比較接觸角與參考接合強度資料|Compare contact angle and reference bond-strength data|表面狀態落在核准活化窗口|Surface state lies in the approved activation window|低接觸角單獨不能證明接合強度|Low contact angle alone does not prove bond strength
活化後等待時間|Evaluate postactivation queue time|將等待時間與顆粒及表面狀態對照|Correlate queue time with particles and surface state|等候未超出已驗證可接合時窗|Queue time stays within the validated bonding window|等待造成再污染或表面狀態改變|Waiting permits contamination or surface-state change
晶粒背面吸持|Evaluate backside die pickup|檢查吸持區與薄晶粒撓度模型|Inspect pickup regions and thin-die deflection models|取晶不接觸接合面且形變受控|Pickup avoids the bonding face and controls deformation|局部吸持會使薄晶粒彎曲|Localized suction can bend thin dies
晶粒工具潔淨度|Inspect bonding-tool cleanliness|比對工具接觸印痕與污染轉移圖|Compare tool imprints and contamination-transfer maps|工具未引入可辨識接合區污染|Tools introduce no detectable bond-area contamination|清洗過的晶粒可能被工具再污染|Cleaned dies can be recontaminated by tools
對位標記辨識|Validate alignment-mark recognition|在不同照明下比較標記中心估計|Compare mark-center estimates under varied illumination|中心估計穩定且可重複|Center estimates remain stable and repeatable|不對稱反光會偏移視覺中心|Asymmetric reflections bias the optical center
座標鏡射與轉換|Verify bonding coordinate transforms|把上下相機座標轉為共同接合座標|Transform upper and lower camera data to one bond frame|各角落對映與設計座標一致|Corner mappings match design coordinates|少一次鏡射會造成系統性反向偏移|Missing a mirror transform causes systematic reversed offsets
晶粒尺度與正交誤差|Separate die scale and orthogonality error|擬合多標記座標的仿射殘差|Fit affine residuals from multiple fiducials|尺度及正交分量分別有量測證據|Scale and orthogonality components are independently measured|剛體對位不能修正晶粒尺度誤差|Rigid alignment cannot correct die-scale error
接合頭傾斜校正|Assess bond-head tilt correction|比較多角落接近曲線與間隙|Compare corner approach curves and gaps|接觸順序符合計畫且傾斜受控|Contact order follows the plan with controlled tilt|單邊先壓實可能導致側向滑移|Early one-sided contact can induce lateral slip
接觸瞬間位移|Measure placement shift at contact|比較接触前後原位標記位置|Compare in-situ marks before and after contact|接觸造成的位移在對位預算內|Contact-induced shift stays within alignment budget|自由空間對準不等於接觸後對準|Free-space alignment does not prove postcontact alignment
介電預接合波前|Observe dielectric prebond propagation|追蹤紅外影像中的接合前緣|Track bonding fronts in infrared image sequences|前緣連續且未包圍大面積未接區|Fronts remain continuous without enclosing large unbonded areas|前緣分叉可能圍住顆粒或氣體|Split fronts can trap particles or gas
集合轉移載板支線|Assess a collective-transfer carrier branch|累加放晶及晶圓鍵合套準誤差|Combine placement and wafer-bond overlay errors|兩段誤差的合成值仍符合介面|Combined errors meet interface requirements|各段個別合格不保證總誤差合格|Each stage passing does not guarantee total overlay passes
直接放晶支線|Assess direct die-placement bonding|比較逐晶粒活化搬運與接觸紀錄|Compare activation, transfer, and contact records per die|各晶粒清潔與等待時間均受控|Each die has controlled cleanliness and queue time|批次首尾晶粒可能經歷不同等待|First and last dies can experience different queue times
晶圓對晶圓配對支線|Assess wafer-to-wafer pairing|疊合上下晶圓良品圖與旋轉標記|Overlay good-die maps and rotation marks|有效重疊與預期良品配對一致|Effective overlap matches expected good-die pairs|只用平均良率會忽略空間相關缺陷|Mean yield misses spatially correlated defects
鍵合後熱處理判讀|Assess postbond thermal treatment|比較熱歷程前後鏈阻及界面影像|Compare chain resistance and interfaces across thermal history|金屬接觸改善且介電未劣化|Metal contact improves without dielectric degradation|提高溫度不能無限制補償表面缺陷|Higher temperature cannot indefinitely compensate surface defects
鍵合空洞定位|Locate hybrid-bond voids|把原位對準與接合影像共同定位|Co-register alignment data and bond images|空洞位置及尺寸可追溯到介面|Void position and size are traceable to the interface|影像亮暗變化不全等同空洞|Image contrast changes are not always voids
銅接點鏈阻分離|Separate copper-contact chain resistance|利用不同接點數鏈結分離線阻及接點阻|Use varied contact-count chains to separate line and contact resistance|接點電阻分布符合介面預算|Contact resistance distribution fits the interface budget|長導線電阻可掩蓋個別接點異常|Long-line resistance can mask contact anomalies
接合強度與破面|Interpret bond strength and fracture surfaces|把破壞載荷與破面位置共同判讀|Interpret failure load with fracture location|破壞模式符合已核准接合評估|Failure mode agrees with the qualified bond evaluation|高載荷也可能伴隨不期望材料破壞|High load can coexist with undesirable material fracture
混合鍵合證據放行|Release hybrid-bond evidence|聯合檢視空洞對位電性與強度記錄|Review void, overlay, electrical, and strength records together|所有介面證據達標且可追溯|All interface evidence meets criteria and is traceable|單獨電性通過不能保證長期接合可靠|Electrical passing alone does not prove durable bonding
'''),
dict(n=16,title='HBM 與晶粒堆疊組裝',titleEn='HBM and chiplet stack assembly',
route='依產品採微凸塊熱壓、回焊或混合鍵合；本模組比較支線，不宣稱任何供應商固定堆疊配方。',
routeEn='Products may use microbump thermocompression, reflow, or hybrid bonding; these are alternatives, not a supplier recipe.',
principle='堆疊放大單層缺陷的成本，必須維持晶粒譜系、逐層幾何與測試可達性。',
principleEn='Stacking magnifies the cost of individual defects and requires die genealogy, layer geometry, and test access.',
sources=['pkb-formfactor-kgd','pkb-formfactor-packaging','pkb-tsmc-soic'],rows='''
HBM 基底晶粒驗證|Verify an HBM base die|核對基底晶粒測試記錄與堆疊版本|Match base-die test records and stack revisions|基底狀態及介面版本皆有效|Base status and interface revision are valid|基底失效會使上層良品晶粒一同損失|A failing base wastes otherwise good upper dies
記憶體晶粒分檔|Bin memory dies for stacking|比較功能測試與速度分檔資料|Compare functional results and speed-bin data|選用晶粒符合堆疊目標分檔|Selected dies meet the target stack bin|不同速度分檔混入會限制整體性能|Mixed speed bins can limit stack performance
堆疊層序核對|Verify stack layer order|以晶粒識別與接面朝向建立層序圖|Build a layer map from die identity and face orientation|每層朝向與通道對應正確|Every layer has correct orientation and channel mapping|層序錯置可能無法在後段修復|Incorrect ordering may be irreparable downstream
薄晶粒厚度分布|Map thinned-die thickness|比較每顆晶粒厚度及局部楔角|Compare individual die thickness and wedge|累計厚度與楔角保留堆疊餘量|Accumulated thickness and wedge preserve stack allowance|微小楔角可逐層累積成傾斜|Small wedges can accumulate into stack tilt
晶粒邊緣機械完整性|Inspect stack-die edge integrity|追蹤崩角位置與 TSV 保留區|Relate edge chips to TSV keep-out regions|裂紋未靠近有效互連區|Cracks remain away from functional interconnects|邊裂可在堆疊載荷下擴展|Edge cracks can extend under stacking loads
背面接點共平面度|Inspect backside stack-contact coplanarity|比較單顆晶粒背面接點高度|Compare backside contact heights per die|接點高度落在鍵合可補償範圍|Contact heights fit bonding compensation capability|晶粒總厚度合格仍可能有局部墊差|Passing die thickness can hide local pad-height variation
微凸塊體積分布|Map stack microbump volume|由三維影像估計凸塊體積|Estimate bump volume from three-dimensional images|体積與高度分布符合接合需求|Volume and height distributions fit joining needs|僅看直徑無法識別不同體積|Diameter alone cannot establish equal volume
非導電膜支線|Inspect a nonconductive-film branch|比較膜厚與凸塊穿透接合模擬|Compare film thickness and bump-penetration simulations|膜可填隙且不妨礙金屬接觸|Film fills gaps without preventing metal contact|膜殘留於接點可造成高阻|Film trapped at contacts can cause high resistance
非導電膠支線|Inspect a nonconductive-paste branch|觀察壓合時膠流與排氣路径|Observe paste flow and venting during simulated compression|膠流未封住排氣且接點乾淨|Flow preserves venting and clean contacts|局部膠量過多可困氣或推移晶粒|Excess paste can trap air or shift dies
薄晶粒取放載荷|Assess thin-die pickup loading|比較多點支撐與局部頂針撓曲|Compare distributed support and localized ejector deflection|模擬拉應力低於核准設計限制|Simulated tensile stress stays within approved design limits|單點頂起容易誘發薄晶粒裂紋|Point lifting can crack thin dies
首層記憶體對位|Align the first memory layer|把首層標記與基底接點套準|Align first-layer marks to base contacts|各角落接點重疊符合規範|Corner contact overlap meets specifications|首層系統偏移會影響全部上層|First-layer systematic offset affects all upper layers
熱壓接合位移曲線|Interpret thermocompression displacement curves|比較壓合位移及接點高度變化|Compare compression displacement and contact-height changes|位移變化與預期接觸事件一致|Displacement changes match expected contact events|載具順應性可能誤當焊點塌陷|Fixture compliance can be mistaken for joint collapse
局部熱歷程梯度|Assess local bonding thermal gradients|比較晶粒中心與四角溫度軌跡|Compare center and corner temperature histories|全部接點經歷合格熱歷程|All contacts experience a qualified thermal history|中央達溫不能代表角落接合充分|Center temperature does not establish corner joining
堆疊層間間隙|Measure interlayer gaps|由側視量測分離各層間距|Resolve individual interlayer gaps from side views|間隙與填膠層設計相容|Gaps agree with adhesive-layer design|平均堆疊高度可能掩蓋局部薄間隙|Average stack height can conceal thin local gaps
層間傾斜累積|Track cumulative stack tilt|逐層擬合頂面傾斜向量|Fit top-surface tilt vectors after each layer|累積傾斜未超過下一層對位預算|Cumulative tilt fits next-layer alignment budgets|相同方向小偏差可逐層累積|Small same-direction errors accumulate layer by layer
層間連通抽測|Sample interlayer continuity|比較新加層前後測試鏈電阻|Compare test-chain resistance before and after adding a layer|新增電阻與預期接點數一致|Added resistance agrees with expected contact count|總阻增加異常可能定位新層接點|Abnormal resistance increment can identify new-layer contacts
堆疊內部空洞|Inspect internal stack voids|比較不同焦深的聲學或斷層影像|Compare acoustic or tomographic images at multiple depths|異常可定位至特定層間介面|Anomalies can be assigned to a specific interface|重疊回波容易混淆缺陷深度|Overlapping echoes can confuse defect depth
上層晶粒偏移|Measure upper-layer displacement|以基底座標比較各層角落位置|Compare layer corners in the base coordinate frame|每層相對與絕對偏移皆達標|Relative and absolute layer offsets meet limits|僅逐層比對可漏掉總體漂移|Adjacent-layer checks can miss total drift
上蓋晶粒支線|Evaluate a top-cap die branch|比較上蓋平整度與機械支撐面|Compare cap flatness and mechanical support surfaces|上蓋接觸不造成局部集中載荷|Cap contact avoids concentrated local loads|凸起缺陷可把載荷傳入記憶體薄晶粒|Protrusions can transfer load into thin memory dies
堆疊封膠流動|Evaluate stack molding flow|觀察狹縫填膠前緣與模流壓力|Observe gap-filling fronts and mold-flow pressure|流動可填滿狹縫且晶粒位移受控|Flow fills gaps with controlled die displacement|高速流前緣可能推移或困氣|Fast flow fronts can displace dies or trap air
堆疊固化形變|Assess stack cure deformation|比較固化前後層序與外形|Compare layer alignment and shape before and after cure|收縮未造成不可接受翹曲|Shrinkage does not produce unacceptable warpage|固化收縮可改變層間剪應力|Cure shrinkage changes interlayer shear stress
堆疊切割邊界|Inspect stack singulation boundaries|追蹤切割面穿越不同材料位置|Trace cuts through different materials|切割面無跨層延伸裂縫|Cut faces lack cracks propagating across layers|材料硬度差可能使裂紋偏折|Hardness differences can deflect cracks
完整堆疊電測|Test a completed stack|聯合讀取基底控制與上層記憶體測試|Read base-control and upper-memory tests together|所有目標層均有可追溯測試結果|Every target layer has traceable test results|只測基底功能會漏掉上層記憶體失效|Base-only testing misses upper-memory faults
冗餘通道修復驗證|Verify redundant-channel repair|比較修復對映前後的故障位置|Compare fault maps before and after repair mapping|修復後功能合格且映射可追溯|Function passes with a traceable repair map|未保存映射會使後段診斷失真|Missing repair maps distort downstream diagnosis
堆疊散熱路徑|Evaluate stack thermal paths|比較各層功耗與通往散熱面的熱阻|Compare layer power with resistance to cooling surfaces|最高溫層符合設計限制|The hottest layer meets design limits|只看上表面溫度會低估內層熱點|Top-surface temperature can underestimate internal hotspots
堆疊良品移交|Transfer known-good stacks|封存晶粒譜系修復圖與整疊測試結果|Archive die genealogy, repair maps, and stack results|移交記錄完整且對應實體識別|Handoff records match physical identifiers|混批或識別失配會破壞良品可信度|Lot mixing or ID mismatch invalidates good-stack evidence
'''),
]

SOURCES=[
('pkb-lam-tsv','The AI Revolution Depends on Advanced Packaging','https://newsroom.lamresearch.com/the-ai-revolution-relies-on-advanced-packaging','Lam Research','TSV、RDL、填孔、顯露與介電等公開製程概念。'),
('pkb-nordson-wafer','Wafer Inspection and Metrology','https://www.nordson.com/en/divisions/test-and-inspection/our-technologies---semiconductor-metrology','Nordson','TSV、凸塊與堆疊封裝 X 光檢測種類及量測限制。'),
('pkb-disco-thin','Ultra-Thin Grinding','https://www-hq.disco.co.jp/eg/solution/library/grinder/thin.html','DISCO','薄晶圓支撐、研磨損傷與應力消除公開概念。'),
('pkb-tsmc-cowos','CoWoS','https://3dfabric.tsmc.com/english/dedicatedFoundry/technology/cowos.htm','TSMC','矽中介層、RDL 中介層與局部矽互連的架構區分；不引用未公開配方。'),
('pkb-amkor-characterization','Package Characterization','https://amkor.com/services/package-characterization/','Amkor Technology','機械、熱與電性量測和模型共同驗證。'),
('pkb-formfactor-kgd','How FormFactor’s Known Good Die Test Enables Advanced Packaging for High Bandwidth Memory','https://www.formfactor.com/blog/2024/known-good-die-test-enables-advanced-packaging-high-bandwidth-memory/','FormFactor','HBM 良品晶粒與堆疊測試策略；未採用產品宣傳數字作為通用規格。'),
('pkb-dupont-substrate','DuPont Material Solutions for IC Substrates','https://www.dupont.com/content/dam/electronics/amer/us/en/electronics/public/documents/en/Fine-Line-IC-Substrate-Total-Solution.pdf','DuPont','公開增層、微孔、金屬化、圖形與表面處理的材料流程類型；僅原創改寫。'),
('pkb-atotech-glass','MKS Atotech introduces integrated wet metallization process for glass substrates','https://www.atotech.com/mks-atotech-introduces-integrated-wet-metallization-process-for-glass-substrates/','MKS Atotech','玻璃附著、孔內種子連續性與填銅挑戰；不轉載商業配方。'),
('pkb-atotech-sap','InPro SAP3','https://www.atotech.com/products/electronics/electrolytic-plating/inpro-sap3/','MKS Atotech','IC 載板盲孔填銅、鍍層均勻性與添加劑監測概念。'),
('pkb-evg-hybrid','Die-to-Wafer Fusion and Hybrid Bonding','https://www.evgroup.com/technologies/die-to-wafer-fusion-and-hybrid-bonding/','EV Group','直接與集合晶粒轉移的替代路線、表面處理和套準誤差來源。'),
('pkb-besi-hybrid','Datacon 8800 CHAMEO ultra plus AC','https://www.besi.com/products-technology/product-details/product/datacon-8800-chameo-ultra-plus-ac/','Besi','公開的薄晶粒處理、潔淨、視覺對準及原位紅外檢測功能；不採產品數值為通用門檻。'),
('pkb-tsmc-soic','TSMC-SoIC','https://3dfabric.tsmc.com/english/dedicatedFoundry/technology/SoIC.htm','TSMC','晶圓與晶粒堆疊架構的公開脈絡；不表示課程為 TSMC 實際製造程序。'),
('pkb-formfactor-packaging','Advanced Packaging Raises the Bar for Wafer Test','https://www.formfactor.com/applications/high-volume-test-on-wafer/advanced-packaging/','FormFactor','組裝前後測試、微凸塊探測與高頻介面測試的技術動機。'),
('pkb-henkel-underfill','High-tech underfill solutions open up new design possibilities for computer chips','https://www.henkel.com/our-businesses/adhesive-technologies/about-us/high-tech-underfill-solutions-2022294','Henkel','充填膠、模封膠與導熱介面材料的不同功能；不宣稱所有材料可互換。'),
('pkb-henkel-lid','Lid and stiffener attach adhesives','https://next.henkel-adhesives.com/us/en/applications/advanced-semiconductor-packaging/lid-and-stiffener-attach-adhesives.html','Henkel','上蓋、補強環、共平面度、固化與黏著介面的公開材料需求。'),
('pkb-nordson-axi','Solder Joint Inspection','https://www.nordson.com/en/divisions/test-and-inspection/our-technologies---automatic-x-ray-inspection/axi-applications','Nordson','隱藏焊點、空洞、橋接及投影／三維檢測差異。'),
('pkb-ti-reliability','Reliability','https://www.ti.com/quality-reliability/reliability.html','Texas Instruments','以使用情境、加速試驗、模型與量產監測串接可靠度。'),
('pkb-ti-qualification','Quality and Reliability FAQs','https://www.ti.com/quality-reliability/faqs.html','Texas Instruments','產品資格、標準適用性與操作壽命試驗的公開概念；實際條件須依適用版本核對。'),
('pkb-amkor-failure','Amkor Quality Brochure','https://amkor.com/wp-content/uploads/2019/08/Quality_Brochure-BR206.pdf','Amkor Technology','電性定位、X 光、聲學、截面與顯微失效分析方法；原創教學改寫。'),
('pkb-keysight-optical','Photonic and Optical Test','https://www.keysight.com/content/keysight/zz/en/products/photonic-and-optical-test.html','Keysight Technologies','光功率、波長、偏振與光電元件量測儀器的公開用途。'),
('pkb-keysight-cpo','1.6T for AI Infrastructure','https://www.keysight.com/zz/en/industry-solutions/artificial-intelligence/1-6-t.html','Keysight Technologies','CPO 與高速光電測試的公開測項類型；不把任何速率或儀器性能當作課程合格門檻。'),
]

def zh_clean(s):
    for a,b in {'必须':'必須','比较':'比較','單点':'單點','接触':'接觸','路径':'路徑','满足':'滿足','验':'驗','测':'測','图':'圖','层':'層','导':'導','传':'傳','单':'單','实':'實','应':'應','标':'標','与':'與','声':'聲','温':'溫','压':'壓','体':'體','试':'試'}.items():
        s=s.replace(a,b)
    return s

def build():
    stages=[]
    for m in sorted(MODULES,key=lambda item:item['n']):
        n=m['n']; stageid=f'pk-m{n:02d}'
        rows=[x.strip() for x in m['rows'].strip().splitlines() if x.strip()]
        assert len(rows)==26,(n,len(rows))
        stage={
            'id':stageid,'title':m['title'],'titleEn':m['titleEn'],
            'description':zh_clean(m['principle'])+'本模組為 26 個可分支的判讀作業，課程順序不代表量產配方。網站提供原創示意模型；本模組未隨附逐步實測資料或商用允收門檻。',
            'descriptionEn':m['principleEn']+' These 26 branching interpretation exercises are a learning sequence, not a production recipe. The site supplies original schematic models, not per-step measured datasets or commercial acceptance limits.',
            'route':m['route'],'routeEn':m['routeEn'],'order':n,'sequence':n,
            'sourceIds':m['sources'],'simulationOnly':True,'steps':[]}
        for local,row in enumerate(rows,1):
            v=row.split('|');assert len(v)==8,(n,local,len(v))
            title,titleEn,act,actEn,criterion,criterionEn,fault,faultEn=v
            title,act,criterion,fault=map(zh_clean,(title,act,criterion,fault))
            number=(n-1)*26+local;sid=f'pk-{number:03d}'
            # Alternatives intentionally remain tied to their own module, with no
            # manufactured dependency on a mutually exclusive earlier module.
            prerequisites=[] if local==1 else [f'pk-{number-1:03d}']
            options=[criterion,
                '只完成操作或讀入影像，尚未檢查其是否符合判準。',
                '忽略此失效線索：'+fault+'。',
                '以全批平均值取代這一步所需的局部或個別證據。']
            optionsEn=[criterionEn,
                'Complete the action or load the image without checking the criterion.',
                'Ignore this failure clue: '+faultEn+'.',
                'Replace the required local or individual evidence with a lot average.']
            answer=number%4
            options=options[-answer:]+options[:-answer] if answer else options
            optionsEn=optionsEn[-answer:]+optionsEn[:-answer] if answer else optionsEn
            optional=any(x in title for x in ['支線','CPO'])
            step={
                'id':sid,'stageId':stageid,'title':title,'titleEn':titleEn,
                'objective':'判斷「'+title+'」是否滿足此具體條件：'+criterion+'。',
                'objectiveEn':'Determine whether '+titleEn+' meets this specific condition: '+criterionEn+'.',
                'instruction':'以示意模型練習，並在需要量測時使用你自行提供或從所列來源取得的可用資料：'+act+'。保存資料來源與樣本識別；依有來源的設計或材料規範判讀。缺少資料或門檻時標記待驗證。',
                'instructionEn':'Practice with the schematic model and, where measurements are needed, use data you supply or obtain from the listed sources: '+actEn+'. Preserve provenance and specimen identity, and use documented design or material criteria. Mark the result unverified when data or limits are missing.',
                'observation':'觀察重點：'+criterion+'；保留局部異常，勿只抄錄平均結果。',
                'observationEn':'Observable evidence: '+criterionEn+'. Retain local anomalies instead of reporting only averages.',
                'failure':fault+'。應先回看此步的原始資料及對照樣本，不能用後段通過結果直接排除此原因。',
                'failureEn':faultEn+'. Revisit raw data and controls for this step; a later passing result alone does not exclude this cause.',
                'check':criterion+'；提交與判斷相符的圖、曲線或紀錄。',
                'checkEn':criterionEn+'. Submit the image, curve, or record supporting the judgment.',
                'knowledge':[
                    {'id':sid+'-k1','title':title+'的驗證依據','titleEn':'Evidence for '+titleEn,
                     'text':'可檢驗條件為「'+criterion+'」。可藉由「'+act+'」建立證據；資料須自行提供或查證取得，完成動作與結果合格是兩個不同問題。',
                     'textEn':'The testable condition is: '+criterionEn+'. Evidence can be developed through this action: '+actEn+'. Supply or verify the data; performing an action and obtaining an acceptable result are separate questions.'},
                    {'id':sid+'-k2','title':title+'的失效線索','titleEn':'Failure clues for '+titleEn,
                     'text':fault+'。將此線索與本步量測位置、材料狀態及前後差異交叉比對，保留其他合理原因直到證據足夠。',
                     'textEn':faultEn+'. Cross-check this clue against measurement location, material state, and before-and-after differences; retain alternative explanations until the evidence distinguishes them.'}
                ],
                'quiz':{'question':'完成「'+title+'」時，哪項證據最直接支持通過？',
                        'questionEn':'Which evidence most directly supports passing '+titleEn+'?',
                        'options':options,'optionsEn':optionsEn,'answer':answer,
                        'explanation':'應確認「'+criterion+'」。'+fault+'，因此僅完成操作或忽略局部異常不能作為通過依據。',
                        'explanationEn':'Confirm: '+criterionEn+'. '+faultEn+', so performing the action or ignoring local anomalies cannot establish a pass.'},
                'sourceIds':m['sources'],'simulationOnly':True,'estimatedMinutes':10,
                'sequence':number,'order':number,'localOrder':local,
                'prerequisiteIds':prerequisites,'prerequisiteMeaning':'learning-sequence',
                'optionalBranch':optional,
            }
            if title.startswith('CPO'):
                step['route']='CPO 光學支線；只用於具有光纖／光子元件的封裝。'
                step['routeEn']='CPO optical branch; only for packages containing fiber or photonic components.'
            else:
                step['route']=m['route'];step['routeEn']=m['routeEn']
            stage['steps'].append(step)
        stages.append(stage)
    sources=[dict(id=i,title=t,url=u,publisher=p,scope=scope+' 已瀏覽官方公開頁面。連結支持技術背景，課程中的判讀作業為原創教育設計，並非廠商 SOP、參數配方或標準全文；照片權利另行查核。') for i,t,u,p,scope in SOURCES]
    sourceids={s['id'] for s in sources}
    steps=[s for m in stages for s in m['steps']]
    assert len(stages)==10 and len(steps)==260
    assert [s['id'] for s in steps]==[f'pk-{i:03d}' for i in range(261,521)]
    assert len({s['title'] for s in steps})==260
    assert len({s['titleEn'].lower() for s in steps})==260
    assert all(len(s['knowledge'])==2 and len(s['quiz']['options'])==4 for s in steps)
    assert all(set(s['sourceIds'])<=sourceids for s in steps)
    assert all(s['quiz']['options'][s['quiz']['answer']]==s['check'].split('；')[0] for s in steps)
    seen=set()
    for s in steps:
        assert set(s['prerequisiteIds'])<=seen,(s['id'],s['prerequisiteIds'])
        seen.add(s['id'])
    (ROOT/'packaging_b.json').write_text(json.dumps(stages,ensure_ascii=False,indent=2)+'\n')
    (ROOT/'sources_packaging_b.json').write_text(json.dumps(sources,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'stages':len(stages),'steps':len(steps),'knowledge':sum(len(s['knowledge']) for s in steps),'sources':len(sources),'first':steps[0]['id'],'last':steps[-1]['id']},ensure_ascii=False))

if __name__=='__main__':build()

