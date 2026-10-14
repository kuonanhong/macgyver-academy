"""Original, bilingual educational operations; no production recipe or universal sequence."""
import json
from pathlib import Path
from collections import Counter

ROOT=Path(__file__).parent
BLOCKS={}
# Each authored row: operation ZH | EN | manipulation ZH | EN | acceptance evidence ZH | EN
BLOCKS[1]='''
建立 CMOS 剖面層序|Build the CMOS cross-section stack|將基板、隔離、井區、閘極與接觸層拖入剖面，標出導電及絕緣區域。|Place substrate, isolation, wells, gate and contact layers in a cross-section; mark conducting and insulating regions.|閘極與通道之間保留介電層，接觸孔只連接指定節點。|A dielectric separates gate and channel; contacts connect only their assigned nodes.
分配光罩圖層|Assign mask layers|把主動區、井區、閘極及接觸的平面圖分開，再疊回同一座標。|Separate active-area, well, gate and contact layouts, then overlay them in one coordinate frame.|每一圖層的用途、極性與參考原點可追溯。|Every layer has a traceable purpose, tone and reference origin.
辨識製程路線分支|Identify process-route branches|並排平面 CMOS、FinFET 與奈米片剖面，圈出不可直接沿用的幾何。|Compare planar CMOS, FinFET and nanosheet cross-sections; flag geometry that cannot be transferred unchanged.|不同路線的隔離高度與閘極包覆方式分別標示。|Isolation height and gate enclosure are labeled separately for each route.
核對基板種類|Verify substrate type|比對塊材矽、磊晶矽與 SOI 的來料截面，選擇與教材路線相符者。|Compare incoming bulk, epitaxial and SOI wafers and select the substrate matching the exercise route.|埋氧層或磊晶層沒有被誤當成裸矽厚度。|Buried oxide and epitaxial layers are not mistaken for bulk silicon thickness.
比對導電型態|Check conductivity type|用來料證明及示意電性量測判斷 p 型或 n 型，與井區設計交叉核對。|Use the supplier record and schematic electrical measurements to distinguish p-type and n-type material; cross-check the well design.|基板導電型態與井區反向接面的安排相符。|Substrate conductivity is consistent with the intended reverse-biased well junctions.
量測晶圓直徑|Measure wafer diameter|在虛擬邊緣掃描圖取多方向直徑，將缺口區排除後檢查圓度。|Measure multiple diameters on an edge-scan map and evaluate roundness while excluding the notch.|直徑變化與局部缺口分開記錄，沒有只採單一方向。|Diameter variation is reported separately from the notch rather than from one direction alone.
量測總厚度變化|Measure total thickness variation|從前後表面量測算出局部厚度，製作 TTV 圖並找出極值位置。|Subtract front and back surface maps to obtain local thickness; map TTV and locate its extrema.|厚度差使用同一座標及單位，未混入整片彎曲。|Thickness differences use consistent coordinates and units without conflating whole-wafer bow.
區分晶圓彎曲與翹曲|Separate wafer bow from warp|比較中心偏移與去除參考平面後的全片形貌，切換支撐條件。|Compare center deflection with full-wafer shape after reference-plane removal and change the support condition.|報告說明支撐方式與參考面，不把 bow 和 warp 當同一量。|The report states support conditions and reference planes and distinguishes bow from warp.
檢查局部平坦度|Inspect local flatness|以曝光場大小的視窗掃描高度圖，比較全片平坦與局部傾斜。|Scan the height map with exposure-field-sized windows and compare global flatness with local slope.|最差曝光場被保留，平均值不掩蓋局部失焦區。|The worst exposure field is retained; averaging does not hide local defocus.
校核晶向與缺口|Verify crystal orientation and notch|把 X 光晶向報告與缺口方位一起放入晶圓座標，標註表面法向。|Place the X-ray orientation report and notch direction in wafer coordinates and label the surface normal.|表面晶面與平面內方向分開，缺口不被當作完整晶向證據。|Surface plane and in-plane direction are distinguished; the notch alone is not treated as complete orientation evidence.
檢查晶圓邊緣輪廓|Inspect wafer edge profile|放大邊緣截面，標出倒角、崩角與背面磨痕，模擬夾持接觸位置。|Magnify the edge section, identify bevels, chips and backside grinding marks, and overlay clamp contact locations.|夾持點不落在崩角區，邊緣缺陷有位置紀錄。|Clamp contacts avoid chipped regions and edge defects have recorded positions.
繪製來料粒子圖|Map incoming particles|比較明場與散射影像，按大小級距標記粒子並保留檢出門檻。|Compare bright-field and scattering images, bin particles by size and retain the detection threshold.|粒子數附帶有效面積及門檻，不能脫離偵測條件比較。|Particle counts include inspected area and threshold, enabling valid comparison.
區分刮傷與粒子|Distinguish scratches from particles|沿缺陷長軸查看連續影像，再與孤立亮點比對。|Follow the major axis of a defect across images and compare it with isolated bright spots.|線狀刮傷與可移除粒子的分類依形貌證據完成。|Scratch and removable-particle classes are supported by morphology.
檢查表面粗糙度|Inspect surface roughness|比較不同掃描尺度的 AFM 高度圖，去除傾斜後再估算粗糙度。|Compare AFM maps at different scan sizes and estimate roughness after tilt removal.|粗糙度數值同時附掃描範圍與去背景方法。|Roughness is accompanied by scan area and background-removal method.
擬合原生氧化層|Fit native oxide thickness|對光學量測分別使用裸矽及矽加氧化層模型，比較殘差。|Fit optical data with bare-silicon and silicon-plus-oxide models and compare residuals.|模型選擇有殘差支持，薄膜厚度與折射率不被任意互換。|Residuals support the model choice; thickness and refractive index are not exchanged arbitrarily.
檢查表面金屬污染|Inspect surface metal contamination|比對表面分析空白樣與來料樣訊號，把背景和元素峰分開。|Compare a surface-analysis blank with the incoming sample and separate background from elemental peaks.|低於定量能力的結果標示為未能定量，未宣稱絕對零污染。|Signals below quantification capability are reported as unquantified, not absolute zero contamination.
映射晶圓電阻率|Map wafer resistivity|在模擬四點探針地圖上比較中心與邊緣，檢查厚度修正。|Compare center and edge values on a simulated four-point-probe map and check thickness corrections.|電阻率與片電阻分清，邊界修正及接觸異常另列。|Resistivity is distinguished from sheet resistance; edge corrections and contact artifacts are documented.
評估磊晶厚度|Evaluate epitaxial thickness|將磊晶厚度量測與基板剖面對齊，查找徑向不均勻。|Align epitaxial thickness measurements with the substrate cross-section and identify radial nonuniformity.|比較的是磊晶層厚度，非整片晶圓總厚度。|The comparison concerns epitaxial-layer thickness rather than total wafer thickness.
檢查 SOI 埋氧層|Inspect buried oxide in SOI|在 SOI 分支讀取頂矽、埋氧與支撐晶圓的獨立量測。|In the SOI branch, inspect separate measurements for top silicon, buried oxide and handle wafer.|三層厚度各有量測依據，絕緣層連續性另行檢查。|Each layer has measurement evidence and oxide continuity is evaluated separately.
分類晶體缺陷|Classify crystal defects|比較點狀、線狀及堆疊缺陷示意，追蹤其與表面缺陷圖的關係。|Compare point, line and stacking-defect representations and relate them to the surface-defect map.|晶格缺陷與外來粒子未合併計數。|Lattice defects are not pooled with external particles.
建立潔淨搬運接觸面|Define clean handling contacts|在搬運模型上標註吸盤、邊緣支撐與感測位置，查看與有效區的交疊。|Mark chuck, edge-support and sensor positions on the handling model and check overlap with the active surface.|搬運接觸面與產品正面敏感區明確分離。|Handling contact surfaces are explicitly separated from sensitive product-face areas.
比對 FOUP 槽位圖|Reconcile the FOUP slot map|把晶圓 ID 與槽位讀值配對，模擬一次換槽後重新核對。|Match wafer IDs to slot readings and reconcile the map after a simulated slot change.|每片晶圓有唯一位置，空槽不被填成缺失 ID。|Each wafer has one unique location; empty slots are not replaced with missing IDs.
檢查量測重複性|Check measurement repeatability|對同一來料點重複讀值，將儀器散布與晶圓位置差分開。|Repeat measurements at one incoming location and separate instrument scatter from spatial variation.|同點重複與異點變化用不同統計量表示。|Same-point repeatability and between-point variation use separate statistics.
建立前後測基準對位|Register before-and-after baselines|以缺口及固定測點對準來料圖與後續清洗圖，再比較新增缺陷。|Register incoming and post-clean maps using the notch and fixed sites before comparing added defects.|新增缺陷以相同位置與門檻判定，而非總數直接相減。|Added defects are determined with matching locations and thresholds, not simple total-count subtraction.
分配監控晶圓|Allocate monitor wafers|將破壞性截面、表面檢測及產品晶圓分開，安排可追溯的陪片。|Separate destructive cross-sections, surface tests and product wafers and assign traceable monitor wafers.|監控片的膜層及熱歷史差異被列出。|Differences in monitor-film stacks and thermal history are disclosed.
判定來料放行|Decide incoming-lot disposition|把尺寸、污染與電性證據放在同一批次卡，比較示範規格內與規格外樣本。|Combine dimensional, contamination and electrical evidence on one lot card and compare examples inside and outside the exercise specification.|不合格項有隔離與複測依據，未知值不當成通過。|Nonconformities have segregation and retest evidence; unknown values do not count as passes.
'''

BLOCKS[2]='''
辨識多晶矽原料品質|Inspect polysilicon feedstock quality|比较原料純度證明與雜質譜，找出可能影響電性或晶體生長的元素。|Compare feedstock certificates and impurity spectra to identify species affecting electrical properties or crystal growth.|原料總純度與各關鍵金屬含量分開檢核。|Bulk purity and critical metal concentrations are checked separately.
配置直拉晶體熱場|Configure the CZ thermal field|在熔體剖面調整示意加熱區，觀察固液界面形狀的變化。|Adjust schematic heating zones in a melt cross-section and observe the solid-liquid interface.|界面形貌與徑向溫差共同記錄，不只看平均溫度。|Interface shape and radial temperature differences are recorded together.
放置籽晶晶向|Orient the seed crystal|旋轉籽晶晶格，使目標成長方向與拉引軸對準。|Rotate the seed lattice to align the intended growth direction with the pulling axis.|晶棒軸向與選定晶向一致。|The ingot axis matches the selected crystal direction.
模擬縮頸排除位錯|Model necking for dislocation control|比較有縮頸與無縮頸的位錯路徑示意，追蹤位錯是否延續至肩部。|Compare dislocation paths with and without necking and track their propagation toward the shoulder.|判讀包含位錯路徑，不能僅憑外徑變小宣稱無缺陷。|The interpretation uses dislocation paths rather than equating a narrower diameter with defect-free material.
控制晶肩展開|Control shoulder growth|調整晶肩展開形狀，檢查過渡處的熱梯度與直徑連續性。|Adjust the shoulder profile and inspect thermal gradients and diameter continuity at the transition.|肩部至等徑段沒有不合理幾何跳變。|The shoulder-to-body transition has no implausible geometric discontinuity.
維持晶棒等徑段|Maintain constant-diameter growth|比較拉速變化與直徑監測曲線，辨識延遲控制造成的振盪。|Compare pull-rate changes with diameter traces and identify oscillations caused by control delay.|直徑偏差與控制反應的先後順序相符。|The timing of diameter errors and control responses is consistent.
追蹤摻雜偏析|Track dopant segregation|沿晶棒長度繪出示意摻雜濃度，與熔體剩餘比例比較。|Plot schematic dopant concentration along the ingot and compare it with remaining melt fraction.|軸向不均勻以偏析及熔體演變解釋，而非假設全棒同值。|Axial variation is interpreted through segregation and melt evolution rather than a uniform-ingot assumption.
比較 CZ 與浮區路線|Compare CZ and float-zone routes|並排坩堝拉晶與移動熔區模型，標出容器接觸與供料途徑。|Compare crucible pulling with a moving molten zone and mark container contact and feed paths.|低氧的浮區特徵不被推廣成所有應用都優於 CZ。|The low-oxygen character of float-zone growth is not generalized into universal superiority over CZ.
模擬磁場拉晶作用|Model magnetic CZ effects|切換磁場作用的熔體流動示意，比較混合強度及熱場穩定性。|Toggle magnetic-field effects in the melt-flow model and compare mixing and thermal stability.|磁場改變流動的效果與單纯降低溫度區分。|Magnetic modification of flow is distinguished from merely lowering temperature.
修整晶棒外徑|Grind the ingot diameter|用圓柱量測圖設定修整包絡，估算移除層與剩餘可用半徑。|Set a grinding envelope from cylindrical metrology and estimate removed stock and usable radius.|修整後的直徑與同軸性分別檢查。|Final diameter and coaxiality are checked separately.
加工定位缺口|Machine the orientation notch|把缺口放到指定晶向參考，檢查缺口深度與邊缘裂紋示意。|Place the notch relative to the crystallographic reference and inspect notch depth and edge-crack indicators.|缺口定位可追溯至晶向量測，無未評估裂紋。|Notch orientation is traceable to crystallographic measurement and cracks are not left unevaluated.
規劃晶棒切片|Plan ingot slicing|在晶棒模型排列切割面，將鋸縫損耗、成品厚度與後續研磨量分開。|Place slicing planes in the ingot model and separate kerf loss, final thickness and finishing allowance.|切片厚度保留後續移除量，不把鋸縫當成產品厚度。|Slice thickness includes finishing allowance and excludes kerf loss from product thickness.
判讀線鋸切痕|Interpret wire-saw marks|對比切痕方向與線鋸移動軌跡，標記局部週期紋路。|Compare saw-mark direction with wire motion and mark local periodic patterns.|切痕方向、週期與機械運動有一致解釋。|Mark direction and periodicity have an explanation consistent with machine motion.
改善切片平行度|Improve slice parallelism|比較雙面研磨前後的厚度圖，調整示意壓力分布。|Compare thickness maps before and after double-sided lapping and adjust the schematic pressure distribution.|兩面平行度改善，同時保留足夠成品厚度。|Parallelism improves while sufficient final thickness remains.
修整晶圓倒角|Shape wafer edge bevels|比較尖角及圓滑倒角的應力集中圖，將倒角延伸至完整圓周。|Compare stress concentrations at sharp and rounded edges and extend the bevel around the circumference.|倒角連續且不侵入規劃有效區。|The bevel is continuous and does not invade the planned usable area.
去除切割損傷層|Remove slicing damage|在示意截面逐步移除表層，觀察微裂紋深度與剩餘基板。|Remove the surface layer incrementally in a schematic section and track microcrack depth and remaining substrate.|被移除範圍涵蓋示範損傷層，未僅消除可見切痕。|The removal covers the demonstrated damage layer rather than only visible saw marks.
執行晶圓精拋模型|Model final wafer polishing|對比不同局部接觸壓力下的表面高點移除，觀察微刮傷和邊緣塌陷。|Compare high-point removal under different local contact pressures and inspect microscratches and edge roll-off.|表面改善兼顧粗糙度與邊缘形貌。|Surface improvement accounts for both roughness and edge shape.
分離有機與無機污染|Separate organic and inorganic contamination|將示意分析峰分配到有機物、金屬與粒子三類，再選對應清洗功能。|Sort schematic analytical peaks into organic, metallic and particulate contamination before selecting a cleaning function.|清洗選擇針對污染類別，不以單一程序宣稱去除全部。|The cleaning choice targets the contamination class without claiming one process removes everything.
檢查清洗潤濕性|Inspect cleaning wettability|比較不同表面狀態的接觸角圖，檢查液體是否覆蓋圖案凹處。|Compare contact-angle images for different surface states and inspect wetting inside patterned recesses.|接觸角與覆蓋行為一起判讀，未將小角度當成所有污染已清除。|Contact angle and coverage are interpreted together rather than as proof of complete decontamination.
模擬粒子去除|Model particle removal|在虛擬清洗前後定位相同粒子，分辨脫附、搬移與新沉積。|Locate identical particles before and after virtual cleaning and distinguish detachment, relocation and new deposition.|移走的粒子與重新落回的粒子分開追蹤。|Removed particles and redeposited particles are tracked separately.
比較金屬污染清除|Compare metallic-contamination removal|對照表面分析的空白、處理前與處理後資料，檢查背景是否漂移。|Compare blank, pre-treatment and post-treatment surface analyses and inspect background drift.|污染降低有同一分析條件下的證據。|Contamination reduction is supported under consistent analytical conditions.
處理原生氧化層分支|Handle native-oxide removal branches|對比需要親水氧化表面與需要暴露矽表面的後續製程，選擇保留或移除氧化層。|Compare downstream processes requiring oxidized hydrophilic surfaces or exposed silicon and choose oxide retention or removal.|表面終態由下一製程需求決定，沒有一律去氧化。|The final surface state follows the next process requirement rather than universal oxide removal.
檢查沖洗置換|Inspect rinse displacement|在流場示意追蹤殘留液體，比較流動死角與有效置換區。|Track residual liquid in a flow model and compare stagnant regions with effective displacement.|殘留集中區被辨識，出口讀值不等同所有表面都已乾淨。|Residual pockets are identified; an outlet reading is not treated as proof of a clean entire surface.
抑制乾燥水痕|Limit drying marks|比較液滴滯留與均勻退液的乾燥影像，把水痕位置疊在污染圖上。|Compare retained-droplet and uniform-meniscus drying images and overlay watermark locations on the contamination map.|乾燥後沒有新增局部殘留圈，表面缺陷圖可前後對位。|Drying adds no unexplained residue rings and defect maps can be registered before and after.
驗證清洗新增缺陷|Verify cleaning-added defects|把相同測點的清洗前後圖相減，對新增亮點再分類。|Compare registered pre-clean and post-clean maps and classify newly appearing bright points.|新增缺陷不是由檢出門檻改變或錯位造成。|Added defects are not artifacts of changed detection thresholds or misregistration.
限制潔淨表面等待|Control clean-surface queue exposure|在等待時間軸上比較表面氧化與吸附指標，對接下一製程的接收條件。|Compare oxidation and adsorption indicators over queue time against the receiving conditions of the next process.|交接依據包含表面狀態及等待歷史，而非僅清洗完成時間。|Handoff evidence includes surface state and queue history, not only the cleaning completion time.
'''

BLOCKS[3]='''
定位主動區與隔離區|Locate active and isolation regions|把相鄰電晶體平面圖投影至剖面，標出需要電性分隔的位置。|Project adjacent transistor layouts into a cross-section and mark locations requiring electrical separation.|隔離區位於預定邊界，不切斷有效通道。|Isolation occupies intended boundaries without cutting active channels.
比較 STI 與 LOCOS 分支|Compare STI and LOCOS branches|並排溝槽填充與局部氧化剖面，觀察邊緣侵入及表面形貌。|Compare trench-fill and local-oxidation cross-sections and inspect lateral encroachment and topography.|鳥嘴效應只用於對應局部氧化情境，未套用成 STI 的相同機制。|Bird's-beak behavior is assigned to the appropriate local-oxidation context rather than identical STI physics.
配置墊氧化層|Configure pad oxide|在矽與氮化層之間插入緩衝氧化層，比較界面應力示意。|Insert a buffer oxide between silicon and nitride and compare interface-stress maps.|墊氧化層的位置及缓衝作用與閘極氧化層區分。|Pad-oxide location and buffering function are distinguished from gate oxide.
沉積隔離硬遮罩|Deposit the isolation hard mask|選擇示範氮化層覆蓋矽面，查看後續蝕刻及研磨會接觸哪一層。|Cover the surface with the example nitride layer and identify which layer later etch and polishing encounter.|硬遮罩厚度同時考慮圖案轉移與研磨停止用途。|Hard-mask thickness considers both pattern transfer and polishing-stop roles.
量測硬遮罩膜厚|Measure isolation-mask thickness|把多點膜厚放回晶圓圖，比較薄區與預計蝕刻負荷。|Map multipoint thickness readings and compare thin areas with expected etch loading.|最薄區仍納入遮罩消耗估算。|The thinnest region is included in mask-consumption estimates.
塗佈主動區光阻|Coat the active-area resist|在硬遮罩上覆蓋光阻，查看臺階附近的局部薄化。|Coat resist over the hard mask and inspect local thinning near topographic steps.|需要保護的位置沒有局部露底。|Regions requiring protection have no exposed underlying surface.
對準隔離光罩|Align the isolation mask|將隔離光罩對準基準記號，分別調整平移及旋轉。|Align the isolation mask to reference marks with separate translation and rotation adjustments.|殘差在多個記號上檢查，並非只讓中心對準。|Residuals are checked across multiple marks rather than only at the center.
顯影隔離開口|Develop isolation openings|比較曝光前後光阻極性，移除指定區並查看主動區是否保留。|Apply the selected resist tone after exposure, remove intended regions and inspect active-area retention.|開口與隔離版圖一致，沒有將圖案正負相反。|Openings match the isolation layout without tone reversal.
量測隔離開口 CD|Measure isolation-opening CD|在密集與孤立區量測相同定義的線寬，標出角部圓化。|Measure identically defined widths in dense and isolated regions and mark corner rounding.|CD 比較使用相同量測高度與邊缘定義。|CD comparisons use the same measurement height and edge definition.
轉移氮化硬遮罩|Transfer the nitride hard mask|將光阻開口轉到硬遮罩，逐層查看墊氧化層是否被過度消耗。|Transfer resist openings into the hard mask and inspect pad-oxide consumption layer by layer.|遮罩開口形成時，非目標層仍符合示範保護需求。|Mask openings form while non-target layers retain the exercise's required protection.
去除圖案化光阻|Remove isolation-patterning resist|模擬去膠後檢查硬遮罩側壁，分辨光阻殘留與氮化層輪廓。|Inspect hard-mask sidewalls after simulated resist removal and distinguish residue from nitride geometry.|去膠沒有被誤判為硬遮罩圖案消失。|Resist removal is not confused with removal of the hard-mask pattern.
開啟墊氧化層窗口|Open the pad-oxide window|沿氮化層窗口移除墊氧化層，觀察暴露矽的位置。|Remove pad oxide through nitride windows and inspect exposed-silicon locations.|矽暴露範圍受硬遮罩約束。|Exposed silicon remains bounded by the hard-mask opening.
蝕刻 STI 溝槽深度|Etch STI trench depth|在剖面模型增加矽移除量，將最深與最淺溝槽分開標示。|Increase silicon removal in the cross-section and label the deepest and shallowest trenches separately.|隔離深度以全片分布評估，而非單點最深值。|Isolation depth is assessed as a wafer-wide distribution rather than the deepest single point.
調整 STI 側壁角度|Adjust STI sidewall angle|比較垂直與略傾斜溝槽，觀察後續填充入口寬度。|Compare vertical and slightly tapered trenches and inspect the opening available for later fill.|側壁形狀與填充可達性一起評估。|Sidewall profile and fill accessibility are evaluated together.
檢查溝槽底角|Inspect trench bottom corners|放大底角截面，找出尖角、微溝與局部殘留。|Magnify trench-bottom corners and identify sharp edges, microtrenches and residues.|底角異常有局部形貌證據，未以平均深度代替。|Corner anomalies have local-profile evidence rather than only average-depth data.
移除溝槽蝕刻殘留|Remove trench-etch residues|比較清洗前後側壁訊號，確認殘留減少時矽輪廓沒有明顯侵蝕。|Compare sidewall signals before and after cleaning and check that residue removal does not unduly erode silicon.|殘留去除與尺寸保留同時成立。|Residue removal and dimensional preservation are demonstrated together.
形成溝槽襯氧化層|Form the trench liner oxide|在溝槽表面加入氧化襯層，追蹤矽消耗與角部圓化。|Add an oxide liner to trench surfaces and track silicon consumption and corner rounding.|襯層連續性與通道側有效寬度均被保留於報告。|Liner continuity and remaining active-region width are both reported.
選擇隔離填充路線|Select the isolation-fill route|比較共形沉積與改善間隙填充的示意路線，檢查入口提前封閉。|Compare conformal deposition with gap-fill-oriented routes and inspect premature closure of the opening.|填充方案不能只靠總沉積厚度判定。|Fill feasibility is not judged from total deposited thickness alone.
追蹤溝槽填充接縫|Track trench-fill seams|逐層增加填充材料，觀察两側成長前緣何處相遇。|Add fill material in stages and locate where opposing growth fronts meet.|接縫位置與可能封存空洞分開標記。|Seam locations and potentially trapped voids are labeled separately.
檢查隔離層緻密化|Inspect isolation-film densification|比较緻密化前後膜厚、折射率與應力示意，追蹤收縮。|Compare thickness, refractive index and stress before and after densification and track shrinkage.|膜厚收縮不直接等同材料遺失或蝕刻。|Film shrinkage is not automatically interpreted as material removal or etching.
建立 STI 研磨停止面|Establish the STI polish-stop plane|設定氮化層作為示範停止層，觀察凸起氧化層逐步移除。|Use nitride as the example stop layer and observe gradual removal of protruding oxide.|停止判據包含剩餘氮化層與區域高度差。|The stop criterion includes remaining nitride and regional height differences.
診斷隔離凹陷與侵蝕|Diagnose isolation dishing and erosion|對照寬隔離區和密集小區的研磨後形貌，分別標註凹陷及區域侵蝕。|Compare polished wide-isolation and dense-pattern regions and label dishing and regional erosion separately.|兩種形貌效應未用同一單點厚度混合描述。|The two topographic effects are not conflated into one point-thickness value.
去除 STI 停止層|Remove the STI stop layer|在模擬截面選擇性移除氮化層，檢查填充氧化層邊缘。|Selectively remove nitride in the model and inspect fill-oxide edges.|停止層去除後的氧化層損耗有記錄。|Oxide loss during stop-layer removal is recorded.
控制隔離表面回蝕|Control isolation recess|逐步回蝕填充氧化層，比較平面元件和鰭式元件所需的暴露高度。|Recess fill oxide incrementally and compare exposure-height needs for planar and fin-based devices.|回蝕目標明確標路線，未對所有元件使用同一高度。|The recess target is route-specific rather than shared blindly across device types.
量測隔離邊緣漏電|Measure isolation-edge leakage|比較示意隔離測試結構的電流曲線，將邊缘長度與面積正規化分開。|Compare leakage curves from isolation test structures and distinguish perimeter normalization from area normalization.|邊缘主導與面積主導漏電的解釋符合結構尺度。|Perimeter-dominated and area-dominated leakage interpretations match structural scaling.
交接隔離後表面|Handoff the post-isolation surface|疊合隔離深度、表面高度與缺陷圖，確認下一層微影的輸入。|Overlay isolation depth, surface height and defect maps to establish inputs for the next lithography level.|交接包含主動區有效尺寸與隔離邊界，而不只填充完成。|Handoff includes active dimensions and isolation boundaries, not merely fill completion.
'''

BLOCKS[4]='''
標示 n 井與 p 井|Label n-wells and p-wells|在 CMOS 截面把 PMOS 與 NMOS 所需井區配對，追蹤接面極性。|Match PMOS and NMOS devices to their wells in a CMOS section and track junction polarity.|井區型態與元件本體電位安排一致。|Well type is consistent with device-body biasing.
配置深井隔離分支|Configure a deep-well branch|在三重井示意加入深井，畫出隔離邊界及基板耦合路徑。|Add a deep well to a triple-well model and draw isolation boundaries and substrate-coupling paths.|深井形成的隔離路徑可在剖面連續追蹤。|The isolation path created by the deep well can be followed continuously in the section.
建立井區植入遮罩|Build the well-implant mask|把井區版圖轉為遮罩開口，檢查鄰近器件與重疊裕量。|Convert well layouts into mask openings and inspect adjacent devices and overlap margins.|未植入區有連續遮蔽，開口與井區對齊。|Protected regions have continuous masking and openings align with the well layout.
核對遮罩阻擋能力|Check implant-mask stopping capability|比較植入深度分布與遮罩等效阻擋厚度，觀察穿透尾端。|Compare implant-depth distributions with effective mask stopping thickness and inspect penetration tails.|遮罩下的尾端分布納入評估，不能只看平均射程。|The under-mask tail is evaluated rather than only mean projected range.
選擇植入離子種類|Select implantation species|對比示意施體和受體的活化後電性，區分化學元素與電荷狀態。|Compare activated donor and acceptor behavior and distinguish chemical species from ion charge state.|所選離子造成的摻雜型態與目標井區相符。|The dopant type associated with the species matches the intended well.
設定植入能量比較|Compare implantation energy|在教材模型提高或降低能量，觀察投影射程與分布寬度。|Vary energy in the educational model and observe projected range and distribution width.|深度趨勢由分布判讀，沒有把能量當作劑量。|Depth trends are interpreted from the distribution without confusing energy with dose.
積分植入劑量|Integrate implant dose|把離子流訊號沿時間積分，再與暴露面積的變化比較。|Integrate the ion-current signal over time and compare changes in exposed area.|面劑量與總離子數區分，電荷態假設有標示。|Areal dose is distinguished from total ion count and charge-state assumptions are stated.
分析多能量井區植入|Analyze multi-energy well implants|疊合數個示意深度分布，查看合成剖面如何覆蓋目標井區。|Superpose several illustrative depth distributions and inspect coverage of the target well.|合成濃度以分布相加，非取各次峰值最大者。|The combined profile sums distributions rather than taking only the largest peak.
辨識晶格通道效應|Identify channeling|比較沿晶軸與偏離晶軸的植入尾端，圈出深層通道化區。|Compare implantation tails along and away from crystal axes and mark deep channeling regions.|通道化判斷來自尾端差異，未假設高斯分布永遠成立。|Channeling is diagnosed from tails without assuming every profile is Gaussian.
調整植入傾角|Adjust implant tilt|在晶格模型改變束流傾角，同時觀察溝槽或遮罩造成的陰影。|Change beam tilt in the lattice model while observing shadowing from trenches or masks.|降低通道化的設定仍須檢查幾何遮蔽。|A channeling-reduction choice is also checked for geometric shadowing.
調整植入旋轉角|Adjust implant twist angle|固定傾角後旋轉晶圓方位，對照晶向與圖案方向。|Hold tilt fixed while rotating wafer azimuth and compare crystal and pattern directions.|傾角與旋轉角分開記錄，遮蔽方向能被重現。|Tilt and twist are recorded separately and shadowing direction is reproducible.
均化植入掃描|Equalize implant scanning|把束流掃描軌跡疊在面劑量圖，找出轉向及邊緣累積。|Overlay beam-scan trajectories on the dose map and identify turnaround and edge accumulation.|掃描均勻性按有效面積評估且保留邊緣異常。|Uniformity is assessed over the usable area while retaining edge anomalies.
診斷植入充電|Diagnose implant charging|比較有無中和作用的表面電位示意，查看介電區和導電區差異。|Compare surface-potential maps with and without neutralization and inspect dielectric and conducting regions.|充電風險以局部電位差判讀，未只看平均束流。|Charging risk is assessed through local potential differences rather than average beam current.
區分植入損傷與摻雜|Separate implant damage from doping|將缺陷密度與化學濃度畫在同一深度軸，檢查峰值是否重合。|Plot damage density and chemical concentration on the same depth axis and compare their peaks.|化學摻雜濃度不被直接當成活性載子濃度。|Chemical dopant concentration is not treated as active-carrier concentration.
剝除植入後光阻|Strip post-implant resist|查看植入後表層硬化示意，比較去除前後残留與基板變化。|Inspect an implantation-hardened resist surface and compare residues and substrate changes before and after stripping.|去膠證據包含硬化殘層與表面損傷。|Strip verification includes hardened residue and surface damage.
清除植入後殘留|Clean post-implant residues|對照元素圖和粒子圖，判別需處理的遮罩殘留或再沉積。|Compare elemental and particle maps to distinguish mask residue from redeposition.|清潔結果不以外觀透明代替化學分析。|Visual transparency does not substitute for chemical evidence of cleanliness.
模擬井區驅入|Model well drive-in|對示意濃度剖面施加扩散演化，查看井深與側向邊界移動。|Apply diffusion evolution to an illustrative concentration profile and track well depth and lateral movement.|垂直和側向扩散一起納入井區邊界。|Both vertical and lateral diffusion are included in the well boundary.
比較快速與爐管退火|Compare rapid and furnace annealing|用两種時間溫度軌跡驅動同一示意模型，觀察活化及擴散取捨。|Apply two time-temperature histories to the same illustrative model and compare activation with diffusion.|比較完整熱歷史，不僅比較最高溫度。|Complete thermal histories are compared rather than peak temperatures alone.
檢查退火溫度均勻性|Inspect anneal temperature uniformity|比較晶圓徑向溫度圖與片電阻圖，辨識可能的發射率量測誤差。|Compare radial temperature and sheet-resistance maps and consider emissivity-related measurement error.|溫度偏差與電性散布的相關性有空間對位。|Temperature deviations and electrical variation are spatially registered before correlation.
評估摻雜活化|Evaluate dopant activation|將化學剖面積分與電性載子估計對照，判斷活化比例不能超出模型意義。|Compare integrated chemical profiles with electrically inferred carriers and evaluate the meaning of activation estimates.|活化估計註明量測方法及補償摻雜假設。|Activation estimates state measurement methods and compensation assumptions.
量測接面深度|Measure junction depth|將施體與受體剖面畫在同一圖，以淨摻雜轉換位置辨識接面。|Plot donor and acceptor profiles together and locate the change in net doping.|接面深度由淨濃度判定，不等同植入濃度峰值。|Junction depth follows net doping rather than the implant-concentration peak.
檢查井區片電阻|Inspect well sheet resistance|比較同批多點片電阻與植入、退火履歷，排除探針接觸不良。|Compare within-lot sheet resistance against implant and anneal histories and exclude poor probe contacts.|异常點複測後再決定是否屬製程偏差。|Outliers are remeasured before being classified as process shifts.
量測井區接面漏電|Measure well-junction leakage|比較反向偏壓下的示意 I-V，將破壞性崩潰與低場漏電分開。|Compare illustrative reverse-bias I-V curves and distinguish breakdown from low-field leakage.|不同電場區間使用對應失效解釋。|Different field regimes are interpreted using their appropriate failure mechanisms.
建立通道調整植入分支|Build a channel-adjust implant branch|在平面 CMOS 分支加入通道調整層，查看閾值與遷移率的取捨。|Add a channel-adjust layer to the planar CMOS branch and compare threshold and mobility trade-offs.|傳統通道植入未被當成低摻雜奈米片的必經步驟。|Conventional channel implantation is not presented as mandatory for lightly doped nanosheets.
評估井區與隔離交互作用|Evaluate well-isolation interaction|把井區擴散邊界疊在 STI 側壁，檢查角部電場與漏電位置。|Overlay diffused well boundaries on STI sidewalls and inspect corner fields and leakage locations.|漏電位置與接面、隔離幾何的交集相符。|Leakage locations are consistent with the intersection of junction and isolation geometry.
交接井區電性地圖|Handoff the well electrical map|彙整濃度剖面、片電阻與漏電三種證據，標出後續熱步驟還會改變的部分。|Combine concentration, sheet-resistance and leakage evidence and mark features affected by later thermal steps.|井區驗證保留後續熱預算依賴，未宣稱當下剖面永久固定。|Well verification retains dependence on later thermal budget rather than freezing the current profile permanently.
'''

BLOCKS[5]='''
選擇閘極介電路線|Select the gate-dielectric route|比較熱氧化矽閘極與高介電常數堆疊，標出各自適用的示範元件。|Compare thermal-silica gates with high-k stacks and label the example devices used for each.|高 k 與傳統厚氧化層是明示分支，不是依序必做的同一堆疊。|High-k and conventional thick-oxide routes are explicit branches, not mandatory sequential layers.
核對前清洗終態|Verify the pre-gate surface state|比較表面氧化、碳殘留與等待時間，選取可供閘極形成的起始表面。|Compare surface oxidation, carbon residue and queue time to select a starting surface for gate formation.|起始表面狀態能連結到前清洗紀錄。|The initial surface state is traceable to pre-clean records.
映射既有氧化層|Map pre-existing oxide|用多點薄膜模型估計原始氧化層，作為新增成長的初值。|Estimate initial oxide with multipoint film models and use it as the initial condition for growth.|初始氧化層未被重複加算或假設為零。|Initial oxide is neither double-counted nor assumed zero without evidence.
比較乾式與濕式氧化|Compare dry and wet oxidation|保持模型其他假設一致，切換氧化物種並比較厚度對時間的曲線。|Keep other assumptions fixed while switching oxidizing species and comparing thickness-time curves.|成長速率差異不被誤解為相同品質或相同用途。|Growth-rate differences are not equated with identical film quality or use.
識別氧化控制區域|Identify oxidation-rate regimes|在薄膜與厚膜區分別查看成長曲線斜率，判讀界面反應或擴散限制。|Inspect growth-curve slopes in thin and thick regimes and identify interface-reaction or diffusion limitations.|同一常數速率未被套用到全部厚度範圍。|One constant rate is not applied across the entire thickness range.
選擇氧化模型範圍|Choose the oxidation-model range|將示意薄氧化層資料與 Deal-Grove 型擬合比較，圈出系統性偏離。|Compare illustrative thin-oxide data with a Deal-Grove-type fit and flag systematic deviations.|模型失配有標記，未把外推值當成量測真值。|Model mismatch is flagged rather than treating extrapolation as measured truth.
追蹤氧化消耗矽|Track silicon consumption during oxidation|在剖面同時移動氧化層外表面與矽界面，檢查體積成長。|Move both the oxide outer surface and silicon interface in a cross-section to track volume growth.|新增氧化層不被畫成全部位於原始矽表面之上。|New oxide is not drawn entirely above the original silicon surface.
比較晶面氧化差異|Compare orientation-dependent oxidation|在相同模型條件比較不同晶面，觀察成長曲線差異。|Compare crystal orientations under the same model conditions and inspect growth-curve differences.|晶向效果與溫度、初始膜厚變化分開。|Orientation effects are separated from temperature and initial-thickness changes.
評估摻雜對氧化影響|Evaluate doping effects on oxidation|比較高摻雜和低摻雜區的示意成長行為，查看模型適用限制。|Compare illustrative growth behavior in heavily and lightly doped regions and inspect model limitations.|不以單一裸矽模型保證所有摻雜區相同成長。|One bare-silicon model is not assumed to guarantee identical growth across doped regions.
檢查爐管軸向均勻性|Inspect furnace axial uniformity|把陪片位置與膜厚串成軸向圖，分辨裝載位置效應。|Plot monitor positions and oxide thickness along the furnace axis to identify loading-position effects.|前、中、後位置分別保留，不只報整批平均。|Front, middle and rear positions remain visible rather than only a batch average.
檢查徑向氧化均勻性|Inspect radial oxidation uniformity|在同一晶圓比較中心與邊緣膜厚，對照熱場和流場示意。|Compare center and edge oxide thickness on one wafer against thermal and flow models.|徑向趨勢有空間證據且不與晶圓間差異混合。|Radial trends have spatial evidence and are not pooled with wafer-to-wafer differences.
記錄氧化升降溫貢獻|Account for oxidation during ramps|將升溫、保持與降溫段的成長貢獻分開積算。|Separate growth contributions during heating, hold and cooling portions of the trajectory.|總膜厚模型包含適用的過渡段，未只取保持時間。|The thickness model includes relevant transitions rather than hold time alone.
檢查氧化層表面形貌|Inspect oxide surface morphology|比較氧化前後 AFM 圖及局部突點，將粒子與粗糙度分开。|Compare pre- and post-oxidation AFM maps and separate particles from roughness.|粗糙度評估未被少數異物完全主導。|Roughness evaluation is not dominated unknowingly by a few foreign objects.
量測氧化層光學厚度|Measure oxide optical thickness|對不同波長的反射資料擬合氧化層厚度，檢查擬合残差。|Fit oxide thickness to multiwavelength reflection data and inspect residuals.|厚度估計伴隨模型與擬合品質。|Thickness estimates include the optical model and fit quality.
建立 MOS 電容測試結構|Build a MOS capacitor test structure|在示意氧化層上放置閘極與背接觸，確認量測電場穿過介電層。|Place a gate and backside contact on the modeled oxide and verify the measurement field crosses the dielectric.|測試面積與電極接觸路徑已定義。|Test area and electrode contact paths are defined.
辨識 MOS 電容區域|Identify MOS capacitance regimes|在 C-V 圖依序標記累積、空乏與反轉，與基板型態交叉核對。|Label accumulation, depletion and inversion on a C-V curve and cross-check substrate type.|電壓極性依基板型態判讀，而非死記曲線左右。|Voltage polarity follows substrate type rather than a memorized left-right curve pattern.
萃取等效氧化厚度|Extract equivalent oxide thickness|用面積正規化電容比較不同介電堆疊，區分電性等效與實體厚度。|Compare area-normalized capacitance across stacks and distinguish electrical equivalence from physical thickness.|EOT 不被當成高 k 薄膜的幾何厚度。|EOT is not interpreted as the high-k film's geometric thickness.
分析串聯介電層|Analyze series dielectric layers|把界面氧化層與高 k 層拆成串聯電容，調整其中一層查看總電容。|Represent interfacial oxide and high-k material as series capacitors and vary one layer to inspect total capacitance.|最薄幾何層不必然對等效厚度貢獻最小。|The thinnest geometric layer is not automatically the smallest contributor to equivalent thickness.
形成高 k 界面層分支|Form the high-k interfacial-layer branch|在高 k 分支插入受控界面層，觀察表面鈍化和 EOT 的取捨。|Insert a controlled interface layer in the high-k branch and compare passivation with EOT trade-offs.|界面品質改善與電容代價同時呈現。|Interface-quality improvement and capacitance cost are shown together.
檢查介面電荷位移|Inspect interface-charge shifts|比較處理前後 C-V 橫向位移，區分功函數改變與固定電荷可能性。|Compare horizontal C-V shifts and distinguish possible work-function changes from fixed charge.|僅憑平帶位移不唯一認定某一類電荷來源。|A flat-band shift alone is not treated as unique identification of one charge source.
診斷介面態響應|Diagnose interface-state response|比較不同量測頻率下的 C-V 或導納變化，標記頻率相依區。|Compare C-V or admittance across measurement frequencies and mark frequency-dependent regions.|介面態判讀包含頻率及量測條件。|Interface-state interpretation includes frequency and measurement conditions.
檢查閘極漏電|Inspect gate leakage|將閘極電流按面積正規化，比較不同電場而非直接比較相同端電壓。|Normalize gate current by area and compare electric fields rather than identical terminal voltages alone.|漏電比較交代有效面積、厚度及場強假設。|Leakage comparisons state effective area, thickness and field assumptions.
辨識局部介電弱點|Identify local dielectric weak spots|把局部缺陷圖與多顆 MOS 電容的漏電分布對照，尋找位置群聚。|Compare local defect maps with leakage distributions from multiple MOS capacitors and identify spatial clusters.|異常群聚與孤立離群值分開分析。|Spatial clusters and isolated outliers are analyzed separately.
比較介電崩潰分布|Compare dielectric-breakdown distributions|比較相同應力定義下的樣本分布，保留未失效樣本的截尾資訊。|Compare sample distributions under a consistent stress definition and retain censoring for unfailed samples.|未失效樣本不被刪除或當作零壽命。|Unfailed samples are neither discarded nor assigned zero lifetime.
核對介電層熱歷史|Check dielectric thermal history|將後續沉積與退火的示意熱歷程加到介電層紀錄，查看界面變化風險。|Add downstream deposition and anneal histories to the dielectric record and inspect possible interface changes.|電性驗證狀態對應正確熱歷史。|Electrical verification is associated with the correct thermal history.
交接閘極介電證據|Handoff gate-dielectric evidence|整合實體厚度、EOT、漏電與缺陷四種資料，標明分支及模型。|Combine physical thickness, EOT, leakage and defect data and label the route and model.|幾何、電性與可靠度證據互相一致，缺測項保留未決。|Geometric, electrical and reliability evidence are consistent; missing measurements remain unresolved.
'''

BLOCKS[6]='''
選擇沉積機制|Select a deposition mechanism|對同一溝槽比較 PVD、CVD 與 ALD 成長示意，標示方向性與表面反應。|Compare PVD, CVD and ALD growth in the same trench and label directionality and surface reactions.|選型根據覆蓋需求與材料限制，不只看沉積速度。|Selection follows coverage and material constraints, not deposition speed alone.
核對沉積表面終態|Verify deposition surface termination|比較氧化表面、氫終止與污染表面的示意成核行為。|Compare schematic nucleation on oxidized, hydrogen-terminated and contaminated surfaces.|表面終態差異列入成核解釋。|Surface-termination differences are included in nucleation interpretation.
檢查真空背景|Inspect vacuum background|比對腔體空白壓力曲線與進氣曲線，辨識洩漏及放氣的可能訊號。|Compare blank-chamber and process-gas pressure traces to identify possible leaks and outgassing.|基壓與製程壓力分開，不以總壓力唯一判定氣體成分。|Base and process pressures are separated; total pressure alone does not identify gas composition.
校核氣流分配|Check gas-flow distribution|將入口流量與晶圓上方流場示意連接，查看邊緣滯流區。|Relate inlet flows to the wafer-level flow model and inspect stagnant edge regions.|入口流量均衡不被直接等同表面供料均勻。|Balanced inlet flow is not automatically equated with uniform surface delivery.
評估沉積熱預算|Evaluate deposition thermal budget|比較不同沉積路線的熱歷史，與已形成接面及膜層的限制配對。|Compare thermal histories of deposition routes against constraints from existing junctions and films.|路線可行性包含既有結構的熱相容性。|Route feasibility includes thermal compatibility with existing structures.
模擬 ALD 首半反應|Model the first ALD half-reaction|在表面位點模型加入第一反應物，查看覆蓋度隨暴露增加的變化。|Introduce the first reactant to surface sites and inspect coverage versus exposure.|自限飽和以曲線趨勢判定，不假定每脈衝恰為完整單原子層。|Self-limiting saturation follows the curve rather than assuming one complete atomic layer per pulse.
檢查 ALD 第一吹掃|Inspect the first ALD purge|追蹤多餘反應物與副產物從腔體退出，觀察死角殘留。|Track excess reactant and byproducts leaving the chamber and inspect residual material in dead zones.|下一反應物進入前的重疊程度被評估。|Overlap with the next reactant is evaluated before its introduction.
模擬 ALD 次半反應|Model the second ALD half-reaction|讓第二反應物與已吸附表面作用，比較完成反應與未完成區。|Let the second reactant interact with the adsorbed surface and compare completed and incomplete regions.|新表面終態可支持下一循環，殘留配基另列。|The resulting surface supports the next cycle and remaining ligands are recorded separately.
檢查 ALD 次吹掃|Inspect the second ALD purge|在循環結束追蹤氣相殘留，對照重新開始首反應物的時點。|Track gas-phase residue at cycle end against the restart of the first reactant.|兩個半反應在時間上有足夠分離的示意證據。|The model provides evidence of temporal separation between half-reactions.
擬合 ALD 每循環成長|Fit ALD growth per cycle|用厚度對循環數資料分辨初期成核延遲與穩定成長斜率。|Use thickness versus cycle count to separate nucleation delay from steady growth per cycle.|斜率擬合不強迫通過原點。|The slope fit is not forced through the origin.
分析 ALD 溫度視窗|Analyze the ALD temperature window|比較覆蓋、成長率及殘留隨溫度的示意資料，找出相對穩定區。|Compare schematic coverage, growth-rate and residue data versus temperature to identify a stable region.|穩定成長區還須檢查膜質，不能只靠厚度斜率。|A stable growth region is also checked for film quality, not thickness slope alone.
量測 ALD 深孔共形性|Measure ALD high-aspect-ratio conformality|在孔口、中段及底部取截面膜厚，對照反應物耗盡趨勢。|Measure thickness at the entrance, middle and bottom of a feature and compare reactant-depletion trends.|共形性由深度分布評估而非平面陪片厚度。|Conformality follows the depth profile rather than planar-monitor thickness alone.
比較熱式與電漿 ALD|Compare thermal and plasma ALD|對同材料目標比較反應活性、方向性與敏感下層的示意影響。|Compare reactivity, directionality and effects on sensitive underlying layers for the same material target.|電漿增強的優勢與可能損傷同時說明。|Plasma-enhanced benefits and potential damage are discussed together.
診斷 ALD 成核島|Diagnose ALD nucleation islands|把早期循環表面影像按時間排列，追蹤島狀區合併為連續膜。|Order early-cycle surface images and track island coalescence into a continuous film.|名義厚度增加不被當作膜已連續的充分證據。|Increasing nominal thickness is not sufficient evidence of film continuity.
模擬 CVD 表面反應|Model CVD surface reactions|比較供料固定下不同表面反應速率，追蹤膜厚與前驅物消耗。|Compare surface-reaction rates under fixed delivery and track thickness and precursor consumption.|表面反應變化與氣相供料變化有分離比較。|Surface-reaction changes are compared separately from gas-delivery changes.
區分 CVD 傳質限制|Distinguish CVD mass-transfer limitation|對比提高供料及改變反應活性的兩組結果，判斷限制來源。|Compare increased delivery with changed reaction activity to diagnose the limiting mechanism.|限制機制由敏感度差異判讀，非只憑溫度高低。|The limitation is inferred from sensitivity differences rather than temperature alone.
檢查 LPCVD 裝載效應|Inspect LPCVD loading effects|比較不同晶舟位置與圖案表面積的膜厚，標註反應物耗用。|Compare thickness across boat positions and patterned surface areas and mark reactant consumption.|晶舟位置與總反應面積都列入解釋。|Both boat position and total reactive area are included in the explanation.
調整 PECVD 膜應力|Compare PECVD film stress|比較示意電漿條件下的膜厚、曲率與膜質資料，選擇滿足多目標的狀態。|Compare thickness, curvature and film-quality data under illustrative plasma conditions and choose a multi-criterion outcome.|低應力方案沒有忽略組成或電性劣化。|A low-stress choice does not ignore degraded composition or electrical behavior.
檢查 CVD 間隙填充|Inspect CVD gap fill|沿沉積過程觀察入口堆積與底部填充，標示可能的封口空洞。|Observe entrance buildup and bottom fill during deposition and mark possible pinch-off voids.|填充結論有截面連續性證據。|The fill conclusion is supported by cross-sectional continuity.
模擬 PVD 入射分布|Model PVD arrival-angle distribution|改變靶材與晶圓相對幾何，觀察沉積粒子的角度分布。|Change target-wafer geometry and inspect the arrival-angle distribution of deposited species.|視線遮蔽對側壁與底部的影響分開評估。|Line-of-sight shadowing is evaluated separately for sidewalls and bottoms.
檢查濺鍍靶材狀態|Inspect sputtering-target condition|比較靶材侵蝕溝槽與沉積均勻性圖，追蹤使用歷史。|Compare target erosion tracks with deposition-uniformity maps and track usage history.|靶材壽命與膜厚趨勢有可追溯關聯。|Target history and thickness trends have traceable links.
控制反應式濺鍍分支|Analyze reactive sputtering branches|比較金屬態與反應覆蓋靶面的示意訊號，觀察遲滯及膜組成。|Compare signals from metallic and compound-covered target states and inspect hysteresis and film composition.|相同氣體設定可能對應不同歷史狀態。|The same gas setting may correspond to different history-dependent states.
量測薄膜階梯覆蓋|Measure thin-film step coverage|在平面、側壁與底部採相同膜厚定義，計算相對覆蓋。|Use a consistent thickness definition on horizontal, sidewall and bottom surfaces and compare relative coverage.|覆蓋比的分子與分母位置標示清楚。|The numerator and denominator locations for coverage ratios are explicitly labeled.
量測薄膜應力與翹曲|Measure film stress and curvature|比較沉積前後晶圓曲率，檢查所用薄膜應力模型的幾何假設。|Compare wafer curvature before and after deposition and inspect assumptions in the film-stress model.|彎曲變化未在厚膜或多層情況下盲目套用簡化公式。|Curvature changes are not blindly inserted into simplified formulas for thick or multilayer films.
分析膜組成與密度|Analyze film composition and density|將光學常數、元素分析與厚度資料交叉比對，辨識不同解釋。|Cross-check optical constants, elemental analysis and thickness to distinguish competing interpretations.|單一折射率變化不足以唯一認定某種雜質。|A refractive-index change alone does not uniquely identify an impurity.
放行沉積膜層|Release the deposited film|整合連續性、厚度、應力及缺陷證據，檢查對下游蝕刻的影響。|Combine continuity, thickness, stress and defect evidence and inspect downstream etch implications.|放行判據同時包含膜層本身與下游相容性。|Release criteria include both film properties and downstream compatibility.
'''

BLOCKS[7]='''
選擇光阻極性|Select resist tone|將同一光罩分別套用正性與負性反應，畫出顯影後保留區。|Apply positive and negative responses to the same mask and draw the retained regions after development.|曝光區與溶解區的對應符合所選極性。|The relationship between exposure and dissolution matches the chosen tone.
核對光阻適用光譜|Check resist spectral compatibility|比較光源波段與光阻吸收示意，選出可對應的材料組合。|Compare source spectrum with resist absorption and select a compatible material pairing.|不同曝光波段未被假定能共用任意光阻。|Different exposure bands are not assumed to work with arbitrary resists.
檢查光阻批次與老化|Inspect resist batch and aging|比較同一材料的新舊批次黏度、粒子與塗膜資料，追蹤保存歷史。|Compare viscosity, particles and coating data across fresh and aged batches while tracking storage history.|批次差異有量測支持，未單憑日期推定可用性。|Batch differences are supported by measurements rather than date alone.
配置抗反射底層|Configure the antireflective underlayer|在高反射基底上加入示意 BARC，對照光場駐波與膜厚。|Add a schematic BARC to a reflective substrate and compare standing-wave fields and thickness.|反射抑制與後續底層開口蝕刻需求一起考慮。|Reflection suppression and later underlayer-opening requirements are considered together.
核對塗佈前潔淨度|Verify pre-coat cleanliness|把有機殘留與粒子圖疊在即將塗膜的位置，預測局部缺陷。|Overlay organic-residue and particle maps on the coating surface and predict local defects.|針孔或凸點的預測可追溯至具體污染位置。|Predicted pinholes or bumps are traceable to specific contamination sites.
處理基板脫水|Assess substrate dehydration|比較表面含水狀態與光阻附著影像，觀察等待後再吸附。|Compare surface-water state with adhesion images and inspect re-adsorption during waiting.|脫水後表面狀態包含等待歷史。|Post-dehydration surface state includes queue history.
比較附著促進層|Compare adhesion-promotion layers|在適用基底分支加入示意促進層，對照塗膜完整性與顯影後剝離。|Add an illustrative adhesion promoter on a compatible-substrate branch and compare coating integrity and post-develop lifting.|促進層使用與材料相容，不把過量塗佈當作附著更強。|Promoter use is material-compatible and excess application is not equated with stronger adhesion.
定位光阻滴注|Position resist dispensing|比較中心滴注與偏心滴注後的覆蓋，追蹤初始氣泡。|Compare coverage after centered and off-center dispensing and track initial bubbles.|有效區覆蓋及氣泡位置有影像證據。|Coverage of the usable area and bubble locations are supported by images.
建立旋塗加速段|Construct the spin-acceleration segment|比較不同示意加速曲線下的初始展膜，觀察條紋起點。|Compare initial spreading under different acceleration profiles and inspect where streaks begin.|加速段效應與最終轉速效應分開比較。|Acceleration effects are compared separately from final-speed effects.
調整旋塗穩態厚度|Compare steady spin-coated thickness|在相同材料與環境假設下改變示意轉速，查看厚度和均勻性。|Vary illustrative spin speed under fixed material and ambient assumptions and inspect thickness and uniformity.|比較註明黏度及溶劑條件，不把經驗曲線當普適定律。|The comparison states viscosity and solvent assumptions rather than treating an empirical curve as universal.
觀察溶劑揮發效應|Observe solvent-evaporation effects|比較相同旋塗曲線但不同揮發程度的膜形，查看乾燥前緣。|Compare film profiles with the same spin trajectory but different evaporation and inspect drying fronts.|厚度差異不全歸因於離心流動。|Thickness differences are not attributed entirely to centrifugal flow.
移除邊緣厚珠|Remove the edge bead|在旋塗截面辨識邊缘厚珠，設定示意去除區並檢查有效版圖。|Identify edge beads in the coating section, define a removal band and check usable layout coverage.|去邊範圍不侵入允許的曝光區。|The edge-removal band does not invade the permitted exposure region.
檢查背面光阻污染|Inspect backside resist contamination|查看晶圓背面與夾盤接觸圖，追蹤光阻殘留造成的高度偏差。|Inspect the wafer backside and chuck-contact map and track height errors from resist residue.|背面殘留的機械影響與正面膜厚區分。|Mechanical effects of backside residue are distinguished from frontside film thickness.
量測軟烤前膜厚|Measure pre-bake film thickness|選擇相同測點建立濕膜基準，記錄量測時距以比較後續收縮。|Establish a pre-bake film baseline at matching sites and record elapsed time for later shrinkage comparison.|軟烤前後數據有一致測點與時間定義。|Pre- and post-bake data share consistent sites and timing definitions.
比較熱板接觸|Compare hotplate contact|在示意熱傳模型改變晶圓與熱板接觸狀態，觀察局部升溫。|Vary wafer-to-hotplate contact in a heat-transfer model and observe local heating.|熱板設定值不被直接當成每點光阻溫度。|Hotplate setpoint is not equated with resist temperature at every location.
模擬軟烤溶劑移除|Model soft-bake solvent removal|沿膜厚方向追蹤溶劑分布，比較表面乾燥與底部殘留。|Track solvent concentration through the film and compare surface drying with bottom residue.|表面看似乾燥不代表整層溶劑已均勻移除。|A dry-looking surface does not prove uniform solvent removal through the film.
檢查軟烤後收縮|Inspect post-bake shrinkage|對位烘烤前後膜厚圖，辨識均勻收縮與局部裂紋。|Register thickness maps before and after baking and distinguish uniform shrinkage from local cracks.|厚度收縮和裂紋缺陷分別記錄。|Thickness shrinkage and cracking defects are recorded separately.
冷卻及等待控制|Control cooling and queue time|比較相同材料在不同等待歷史下的曝光起始狀態，標示適用的再吸水分支。|Compare exposure starting states after different queue histories and label any material-specific rehydration branch.|再吸水只限需要的光阻體系，未當作所有光阻必做。|Rehydration applies only to compatible resist systems rather than all resists.
交接已校核曝光結果|Receive verified exposure results|把第八模組的曝光圖與本模組光阻極性結合，確認 PEB 或顯影的輸入。|Combine the exposure map from module eight with resist tone to establish the input for PEB or development.|實際順序標為塗佈、曝光、適用 PEB、顯影。|The physical sequence is explicitly coating, exposure, applicable PEB, then development.
控制曝光後烘烤分支|Analyze the post-exposure-bake branch|在需要 PEB 的材料模型中比較反應擴散長度與線緣變化。|For a resist requiring PEB, compare reaction-diffusion length with line-edge changes.|PEB 需求依材料機制決定，不與軟烤混淆。|PEB requirements follow material chemistry and are not confused with soft baking.
核對顯影液相容性|Check developer compatibility|將光阻體系與供應商指定顯影類別配對，比較未曝光區溶失。|Match the resist system to its specified developer class and compare loss from unexposed regions.|相容性同時檢查目標溶解與非目標膜損耗。|Compatibility considers intended dissolution and unwanted film loss together.
模擬顯影溶解前緣|Model the development front|觀察開口從表面向下形成，對比線端與密集區溶解差異。|Observe openings forming downward from the surface and compare line ends with dense regions.|清底程度與保留光阻尺寸共同評估。|Opening clearance and retained-resist dimensions are evaluated together.
檢查顯影後沖洗|Inspect post-development rinsing|追蹤圖案間殘留顯影液，比較及時終止與持續溶解的示意結果。|Track developer retained between features and compare timely termination with continued dissolution.|沖洗效果以残留和尺寸變化確認。|Rinse performance is checked through residue and dimensional change.
診斷光阻圖案倒塌|Diagnose resist-pattern collapse|比較細高線條在乾燥前後的位置，檢查毛細作用與附著因素。|Compare tall slender lines before and after drying and inspect capillary and adhesion effects.|倒塌與未曝光橋接在形貌上分开辨識。|Collapse is distinguished morphologically from exposure-related bridging.
執行顯影後檢查|Perform after-development inspection|比較線寬、殘膠、橋接與缺口地圖，選出需返工的示意區。|Compare CD, scum, bridges and missing-feature maps and identify illustrative rework regions.|圖案通過需同時滿足尺寸與完整性，而非僅平均線寬。|Passing patterns satisfy both dimensions and integrity, not average CD alone.
判定硬烤或直接轉移|Choose hard bake or direct transfer|依下一蝕刻或其他轉移需求比較硬烤前後輪廓，保留可剝除性資訊。|Compare pre- and post-hard-bake profiles for the next transfer step and retain stripability information.|硬烤是相容性分支，非所有先進光阻的必要固定步驟。|Hard bake is a compatibility branch rather than a mandatory step for every advanced resist.
'''

BLOCKS[8]='''
配置曝光座標系|Configure exposure coordinates|把光罩、平台及晶圓座標箭頭並排，檢查翻轉與縮小倍率方向。|Compare mask, stage and wafer coordinate axes and inspect inversion and reduction directions.|平面鏡像及坐標轉換有一致定義。|Image inversion and coordinate transformations have consistent definitions.
核對光罩版本與極性|Verify reticle revision and tone|疊合光罩圖案與設計版次，查找版本差異及遮光區。|Overlay reticle patterns with the design revision and inspect differences and opaque regions.|使用圖案能追溯至正確版次與曝光極性。|The pattern is traceable to the correct revision and exposure tone.
辨識光罩缺陷|Identify reticle defects|比較光罩檢查圖與預期晶圓重複圖案，追蹤缺陷在曝光場中的固定位置。|Compare reticle inspection with expected repeated wafer patterns and track fixed within-field defects.|場內重複缺陷與隨機晶圓污染分開。|Repeated within-field defects are distinguished from random wafer contamination.
比較光源波長|Compare exposure wavelengths|在相同 NA 與示意 k1 下切換波長，比較可分辨特徵尺度。|Vary wavelength with fixed NA and illustrative k1 and compare resolvable feature scales.|比較控制其他變數，沒有把節點名稱當成波長。|Other variables are controlled and a technology-node name is not treated as a wavelength.
調整數值孔徑|Vary numerical aperture|比較 NA 變化對示意解析度和焦深的相反趨勢。|Compare how changing NA affects illustrative resolution and depth of focus.|解析度改善與焦深代價同時呈現。|Resolution improvement and depth-of-focus cost are shown together.
區分 DUV 透射與 EUV 反射|Separate DUV transmission from EUV reflection|把透鏡路徑與多鏡反射路徑分開拼裝，標出光罩型態。|Build lens-based and multiple-mirror optical paths separately and label reticle types.|EUV 路徑沒有插入當作主投影元件的普通透射玻璃透鏡。|The EUV path does not use ordinary transmissive glass lenses as its main projection optics.
分析浸潤微影分支|Analyze the immersion branch|在 DUV 末端加入示意液層，比較折射率對 NA 的影響及液體缺陷。|Add an illustrative liquid layer to the DUV image space and compare refractive-index effects on NA with liquid-related defects.|浸潤路線明示為 DUV 情境，不套用到真空 EUV。|Immersion is explicitly a DUV context rather than a vacuum-EUV step.
檢查曝光真空相容性|Inspect exposure-vacuum compatibility|比較空氣吸收與真空傳播示意，查看 EUV 光路的表面污染。|Compare air absorption with vacuum propagation and inspect contamination along EUV optical surfaces.|光路傳輸損失與鏡面反射損失分開估算。|Propagation loss and mirror-reflection loss are estimated separately.
定位晶圓對準記號|Locate wafer alignment marks|把記號影像與背景膜層分開，找出對比不足或被覆蓋的記號。|Separate alignment-mark signals from film background and locate low-contrast or covered marks.|記號位置品質有訊號證據，未用不可辨識記號硬對準。|Mark-position quality has signal evidence and unresolved marks are not forced into alignment.
校正平移誤差|Correct translation error|以多個對準記號估計整體位移，再查看修正後的殘差向量。|Estimate global shift from multiple marks and inspect residual vectors after correction.|修正後殘差不再包含一致方向的整體偏移。|Corrected residuals no longer contain a common global translation.
校正旋轉誤差|Correct rotational error|比較晶圓兩側方向相反的殘差，調整小角度旋轉模型。|Compare opposing residual directions at wafer edges and adjust a small-angle rotation model.|旋轉修正以全片向量模式驗證。|Rotation correction is verified from the full-wafer vector pattern.
校正倍率誤差|Correct magnification error|辨識隨位置半徑放大的殘差，比較 isotropic 與分軸倍率模型。|Identify residuals growing with position and compare isotropic with axis-dependent scaling models.|倍率項與平移項未互相代替。|Magnification terms are not substituted for translation terms.
建立晶圓高度圖|Build the wafer height map|把測高點插值為曝光場高度，保留局部臺階與邊緣。|Interpolate height samples into field-height estimates while retaining local steps and edges.|插值沒有平滑掉會造成失焦的實際突起。|Interpolation does not erase protrusions that cause defocus.
校正焦平面與傾斜|Correct focus plane and tilt|對單一曝光場調整焦平面與兩軸傾斜，觀察最差位置的離焦量。|Adjust focus and two-axis tilt for one exposure field and inspect the worst residual defocus.|最佳平均焦點不掩蓋局部超出示範焦深的區域。|The best average focus does not hide regions outside the exercise depth of focus.
建立焦距劑量矩陣|Build a focus-exposure matrix|排列不同焦距與曝光量的虛擬小區，量測每格線寬和缺陷。|Arrange virtual fields across focus and dose and measure CD and defects in each cell.|兩個控制軸獨立標示，沒有把焦距與劑量混成一軸。|The two control axes are labeled independently rather than merged.
判定共同製程視窗|Determine a common process window|疊合線寬、橋接及缺口可接受區，找出共同交集。|Overlay acceptable regions for CD, bridges and missing features to find their intersection.|視窗是多條件交集，不是某一圖案的最佳點。|The window is an intersection of criteria rather than one pattern's optimum.
比較密集與孤立成像|Compare dense and isolated imaging|以相同設定曝光密集線與孤立線，觀察尺寸偏移。|Expose dense and isolated lines under the same settings and inspect dimensional bias.|兩種圖案都在驗證集合中，不能只挑容易成像者。|Both pattern classes remain in the verification set rather than selecting only easy cases.
分析照明形狀|Analyze illumination shape|比較示意環形、傳統及多極照明對不同方向圖案的光場。|Compare schematic annular, conventional and multipole illumination for differently oriented patterns.|照明優化效果連結到圖案方向與週期。|Illumination benefits are linked to pattern orientation and pitch.
套用光學鄰近修正|Apply optical proximity correction|比較未修正與加上修正結構的光罩，查看晶圓目標輪廓誤差。|Compare uncorrected and corrected masks and inspect wafer-contour error relative to target.|光罩外形可偏離目標，但晶圓輪廓需更接近目標。|The mask may differ from the target while the wafer contour should approach it.
檢查圖案邊缘位置|Inspect pattern edge placement|把設計輪廓、印出輪廓與下層圖案疊合，分開 CD 與位置誤差。|Overlay design, printed contour and the underlying layer and separate CD from placement error.|邊緣位置誤差同時考慮尺寸與對位。|Edge-placement error accounts for both size and alignment.
量測層間套刻|Measure interlayer overlay|用上層與下層專用標靶求偏移，對照實際器件敏感位置。|Measure upper-to-lower-layer offsets with overlay targets and compare device-sensitive locations.|標靶套刻與器件內套刻的差異有保留。|Differences between target overlay and in-device overlay are retained.
分析場內與場間誤差|Separate intra-field and inter-field error|將套刻向量依曝光場分組，再比較場內重複模式與全片漂移。|Group overlay vectors by exposure field and compare repeating field patterns with wafer-wide drift.|場內與全片誤差使用對應座標和模型。|Intra-field and wafer-level errors use appropriate coordinates and models.
診斷 EUV 隨機缺陷|Diagnose EUV stochastic defects|比較相同名義圖案多次曝光的缺口、橋接與線緣分布。|Compare missing features, bridges and edge variation across repeated nominally identical EUV patterns.|平均線寬相同不能排除尾端缺陷風險。|Identical mean CD does not rule out tail-related defect risk.
比較雙重圖案化分支|Compare double-patterning branches|把一組密集圖案拆成兩次曝光或間隔層路線，追蹤額外對位需求。|Decompose a dense pattern into two exposures or a spacer-based route and track added alignment needs.|替代路線明示，不把不同雙圖案化方法混為同一工序。|Alternative routes are labeled rather than merged into one universal double-patterning sequence.
分析高 NA 視場取捨|Analyze high-NA field trade-offs|比較示意高 NA 光學與曝光場安排，檢查分場及接縫需求。|Compare schematic high-NA optics with field placement and inspect partitioning and stitching needs.|視場與掩模成像限制依選定架構討論，不只標解析度更高。|Field and mask-imaging constraints are discussed for the selected architecture, not only better resolution.
回傳曝光校正資料|Return exposure-correction data|把焦距、劑量及套刻殘差回傳至虛擬配方卡，標示適用圖層與版次。|Return focus, dose and overlay residuals to the virtual process card and label applicable layer and revision.|校正只套用到相容條件，並保留未改善的殘差。|Corrections apply only to compatible conditions and unresolved residuals remain visible.
'''

BLOCKS[9]='''
讀取待蝕刻堆疊|Read the etch target stack|在剖面指定目標膜、遮罩及停止層，標出暴露方向。|Identify target film, mask and stop layer in the section and mark exposed directions.|目標層與保護層角色清楚，不因顏色相同而混淆材料。|Target and protected-layer roles are clear and materials are not confused by display color.
選擇濕式或乾式路線|Select wet or dry etching|比較化學移除及電漿移除的輪廓示意，依材料和方向性需求選路線。|Compare chemical and plasma-removal profiles and choose a route for material and directionality needs.|濕蝕刻不被一律宣稱等向性，晶向選擇性分支另列。|Wet etching is not universally called isotropic; crystallographic branches are labeled separately.
估算遮罩消耗預算|Estimate mask-consumption budget|以示意選擇比把目標移除量換算成遮罩損失，納入不均勻區。|Use illustrative selectivity to estimate mask loss from target removal and include nonuniform regions.|預算保留最薄遮罩區及額外清底需求。|The budget includes the thinnest mask and additional clearing requirements.
核對蝕刻前圖案|Verify the pre-etch pattern|將顯影後 CD 圖與目标截面對齊，標記橋接與未清底開口。|Register after-development CD data to the target section and mark bridges and uncleared openings.|已存在的光阻缺陷先記錄，未在蝕刻後才全歸咎蝕刻。|Pre-existing resist defects are recorded rather than all blamed on etching afterward.
執行底層開口分支|Open the underlayer branch|有抗反射底層時先轉移開口，觀察剩餘光阻和下層。|When an antireflective underlayer is present, open it first and inspect remaining resist and substrate layers.|開口完成但未過度消耗主要蝕刻遮罩。|The underlayer is opened without excessive loss of the main etch mask.
比較電漿密度與偏壓|Separate plasma density from bias|在示意模型分别變動離子供給與入射能量，對比移除率與損傷。|Vary ion supply and incident energy separately in the model and compare removal with damage.|電漿密度與基板偏壓未當成同一控制量。|Plasma density and substrate bias are not treated as the same control variable.
觀察離子入射方向|Observe ion-arrival direction|比較寬與窄角度分布，查看側壁侵蝕及底部移除。|Compare broad and narrow arrival-angle distributions and inspect sidewall erosion and bottom removal.|方向性結論由輪廓變化支持。|Profile changes support conclusions about directionality.
檢查中性反應物供應|Inspect neutral-reactant delivery|在深孔模型追蹤中性物種到達底部的比例，與表面耗用比較。|Track the fraction of neutral species reaching feature bottoms and compare surface consumption.|深孔底部供料不足與離子能量不足分開診斷。|Bottom reactant starvation is distinguished from insufficient ion energy.
平衡側壁鈍化|Balance sidewall passivation|比較鈍化較強與較弱的剖面，觀察側蝕、頸縮及底部阻塞。|Compare stronger and weaker passivation and inspect undercut, necking and bottom blockage.|最佳方案兼顧側壁保護與底部開通。|The selected outcome balances sidewall protection with bottom clearance.
調整反應物停留示意|Compare reactant residence time|改變示意抽氣和供料平衡，觀察副產物殘留與反應物利用。|Change schematic pumping and delivery balance and inspect byproduct retention and reactant utilization.|停留時間效果與總壓力讀值不直接等同。|Residence-time effects are not equated directly with total-pressure readings.
檢查晶圓溫度作用|Inspect wafer-temperature effects|比較不同表面溫度下的示意吸附與揮發，追蹤殘留及輪廓。|Compare adsorption and volatility at different surface temperatures and track residue and profile changes.|溫度變化對表面化學的影響有記錄。|Temperature effects on surface chemistry are documented.
評估深寬比相依蝕刻|Evaluate aspect-ratio-dependent etching|同時蝕刻不同寬度但相同起始深度的開口，量測完成深度。|Etch openings of different widths from the same starting depth and measure resulting depths.|深度差異與開口深寬比相連，不只平均整片速率。|Depth variation is linked to feature aspect ratio rather than only average wafer etch rate.
評估圖案密度負載|Evaluate pattern-density loading|比較相同線寬在密集與稀疏區的蝕刻深度，保持其他條件一致。|Compare etch depth at equal widths in dense and sparse regions while holding other conditions fixed.|負載效應與單一特徵深寬比效應分開。|Loading effects are distinguished from individual-feature aspect-ratio effects.
量測側壁錐度|Measure sidewall taper|在顶部、中段與底部量測寬度，以輪廓定義側壁角度。|Measure widths at top, middle and bottom and define sidewall angle from the profile.|錐度採完整剖面判定，非只用頂部 CD。|Taper is determined from the section rather than top CD alone.
診斷側壁弓形|Diagnose sidewall bowing|放大中段寬度異常的截面，對照側壁保護與入射分布。|Magnify a section with abnormal middle width and compare passivation with arrival-angle distribution.|中段外擴與整體錐度分開分類。|Mid-depth widening is classified separately from overall taper.
診斷底部微溝|Diagnose microtrenching|查看底角局部加深區，對照離子反射及側壁幾何示意。|Inspect locally deepened bottom corners against ion-reflection and sidewall-geometry models.|局部微溝未被平均深度掩蓋。|Local microtrenches are not hidden by average depth.
分析停止層選擇比|Analyze selectivity to the stop layer|比較目標層清除後停止層的消耗，增加示意清底時間查看代價。|Compare stop-layer loss after target clearance and extend illustrative overetch to inspect its cost.|停止層剩餘量與最慢清底區共同決定可用區間。|Remaining stop material and the slowest-clearing region jointly define the feasible interval.
判讀光學端點訊號|Interpret optical endpoint signals|將發光訊號轉折與材料界面到達時間對照，檢查雜訊和延遲。|Relate emission-signal changes to interface arrival and inspect noise and delay.|訊號轉折需與材料轉換一致，不能只用任意峰值。|The signal change must match a material transition rather than an arbitrary peak.
比較時間式與端點式控制|Compare timed and endpoint control|對厚度偏差的兩片虛擬晶圓使用不同停止方式，查看清底與損耗。|Apply different stopping methods to two virtual wafers with thickness variation and inspect clearing and loss.|控制方式的選擇能解釋厚度變化下的結果。|The control-method choice explains outcomes under thickness variation.
配置有限過蝕刻|Allocate limited overetch|以最慢清除區為基準增加示意餘裕，同時查看遮罩與停止層餘量。|Add illustrative margin based on the slowest-clearing region while inspecting mask and stop-layer reserves.|過蝕刻不是越長越好，清底與損傷有共同限制。|Overetch is not maximized; clearance and damage impose joint constraints.
模擬原子層蝕刻循環|Model atomic-layer etch cycles|把表面改質與移除分為兩段，觀察循環間反應是否趨於自限。|Separate surface modification from removal and inspect whether each cycle tends toward self-limitation.|每循環移除量由材料與條件決定，非保證一完整原子層。|Removal per cycle depends on material and conditions rather than guaranteeing a whole atomic layer.
分析選擇性蝕刻分支|Analyze selective-etch branches|在兩種材料相鄰模型中比較移除率，查看高選擇比的有限損耗。|Compare removal rates in adjacent materials and inspect finite loss even at high selectivity.|高選擇比不被當作保護材料完全零損耗。|High selectivity is not interpreted as zero loss of the protected material.
診斷電漿充電損傷|Diagnose plasma charging damage|比較連接與浮接圖案的電位示意，定位薄介電層風險。|Compare potentials in connected and floating patterns and locate thin-dielectric risk areas.|損傷位置與電荷累積路徑有對應。|Damage locations correspond to charge-accumulation paths.
清除蝕刻聚合殘留|Remove etch-polymer residues|比較清理前後開口及側壁影像，避免把殘留當成目標膜。|Compare opening and sidewall images before and after cleaning without confusing residue with target film.|殘留降低且圖案尺寸保留有雙重證據。|Both residue reduction and dimensional retention are evidenced.
量測蝕刻偏差|Measure etch bias|用相同位置的顯影後及蝕刻後 CD 求變化，保留量測高度差異。|Compare after-development and after-etch CD at matching sites and retain measurement-height differences.|CD 差異在一致邊缘定義下才作為蝕刻偏差。|CD differences are called etch bias only under consistent edge definitions.
交接轉移後圖案|Handoff the transferred pattern|結合深度、輪廓、缺陷及材料殘留圖，將異常連結到下游風險。|Combine depth, profile, defect and residue maps and connect anomalies to downstream risks.|圖案轉移驗證涵蓋三維輪廓，不僅俯視影像。|Pattern-transfer verification covers three-dimensional profiles rather than top views alone.
'''

BLOCKS[10]='''
選定先閘或後閘分支|Select gate-first or gate-last branch|並排最終閘極先形成與替代閘極路線，標出各自後續高溫步驟。|Compare gate-first and replacement-gate routes and mark later high-temperature steps.|犧牲閘極與最終金屬閘極明確區分。|Dummy gates and final metal gates are clearly distinguished.
配置閘極導體堆疊|Configure the gate-conductor stack|把教材分支所需導體及介電層依序放入剖面，查看接觸界面。|Place conductors and dielectrics for the selected educational branch in the section and inspect interfaces.|堆疊符合所選路線，未同時混用互斥材料安排。|The stack matches the selected route without combining incompatible alternatives.
配置閘極頂蓋|Configure the gate cap|在導體上放置頂蓋或硬遮罩，觀察後續閘極蝕刻的保護作用。|Place a cap or hard mask above the conductor and inspect its protection during gate etching.|頂蓋功能與閘極介電功能分開。|Gate-cap function is separated from gate-dielectric function.
建立閘極光阻圖案|Build the gate-resist pattern|將閘極線對準主動區，查看線條是否跨越所需通道。|Align gate lines to active areas and inspect whether they cross the intended channels.|閘極與主動區的交集形成正確通道位置。|Gate-active intersections form the intended channel locations.
檢查閘長與線端|Inspect gate length and line ends|分別量測線條中段 CD 與端部縮短，對照器件有效區。|Measure mid-line CD and line-end shortening separately against the active device area.|線端失效未被中段正常 CD 掩蓋。|Normal mid-line CD does not hide line-end failures.
轉移閘極硬遮罩|Transfer the gate hard mask|把光阻線轉入硬遮罩，檢查側壁粗糙及頂部消耗。|Transfer resist lines into the hard mask and inspect sidewall roughness and top loss.|硬遮罩保留所需閘線輪廓及餘量。|The hard mask retains required gate-line contours and reserve thickness.
選擇性蝕刻閘極導體|Selectively etch the gate conductor|在目標導體逐步移除時追蹤底部介電層，查看最慢清底區。|Track the underlying dielectric while removing the conductor and inspect the slowest-clearing region.|导體清除與介電層保護同時達成。|Conductor clearance and dielectric protection are achieved together.
判讀閘極蝕刻端點|Read the gate-etch endpoint|把材料轉換訊號與截面清底情形對照，檢查訊號延遲。|Compare material-transition signals with cross-sectional clearing and inspect signal delay.|端點判斷對應实际界面，而非僅某個時間戳。|Endpoint judgment corresponds to the actual interface rather than a timestamp alone.
控制閘極底部殘腳|Control gate-foot residues|放大閘極底角，分辨導體殘腳、聚合物及介電層。|Magnify gate-bottom corners and distinguish conductor feet, polymer and dielectric.|不同材料造成的殘腳使用不同診斷，不以外形一概分類。|Similar-looking feet are diagnosed by material rather than appearance alone.
檢查閘極側壁斜率|Inspect gate sidewall slope|比較上、中、下閘寬，估計輪廓對後續間隔層的影響。|Compare upper, middle and lower gate widths and assess effects on later spacers.|閘極輪廓以高度相關 CD 表示。|Gate profile is represented with height-dependent CD.
量測閘極線緣粗糙|Measure gate line-edge roughness|沿閘邊追蹤位置變化，區分整體偏移與局部起伏。|Track edge position along the gate and separate global shift from local fluctuations.|粗糙度估計包含取樣長度與去趨勢方法。|Roughness estimates include sampling length and detrending method.
檢查閘極下介電損傷|Inspect under-gate dielectric damage|對比閘極加工前後測試結構的漏電與 C-V，定位損傷分支。|Compare leakage and C-V of test structures before and after gate processing and locate possible damage.|幾何完整不被當作介電電性完好的保證。|Geometric integrity is not treated as proof of intact dielectric behavior.
清除閘極加工殘留|Clean gate-processing residues|將去膠與聚合残留清理分開觀察，檢查導體及介電層損失。|Observe resist stripping and polymer cleaning separately and inspect conductor and dielectric loss.|残留清除沒有掩蓋有效閘長或介電層改變。|Residue removal does not conceal changes in effective gate length or dielectric thickness.
形成側壁襯層分支|Form a sidewall-liner branch|在需要襯層的路線包覆閘極側壁，與不加襯層的剖面对照。|Wrap gate sidewalls with a liner where the route requires it and compare with the unlined section.|襯層只在適用路線存在，厚度計入側向尺寸。|The liner appears only in applicable routes and its thickness enters lateral dimensions.
沉積外間隔層薄膜|Deposit the outer-spacer film|以示意共形薄膜覆蓋閘頂、側壁與平面，比較各處厚度。|Cover gate tops, sidewalls and horizontal surfaces with a schematic conformal film and compare thicknesses.|側壁覆蓋由截面確認，而非只用平面膜厚。|Sidewall coverage is verified in section rather than inferred only from planar thickness.
建立間隔層回蝕|Form spacers by etch-back|逐步移除水平面的薄膜，觀察側壁材料如何留下。|Remove film from horizontal surfaces incrementally and observe retention on sidewalls.|水平開通時側壁仍保留所需間隔層。|Horizontal surfaces clear while required sidewall spacers remain.
控制間隔層肩部|Control spacer shoulders|比较不同回蝕程度的頂部肩形與下方隔離距離。|Compare top-shoulder shapes and lower isolation distances at different etch-back extents.|肩部縮小未造成關鍵側壁隔離消失。|Shoulder reduction does not eliminate critical sidewall isolation.
量測間隔層底部寬度|Measure spacer base width|在閘底與中段分别量測間隔層，確認與源汲極邊界的關係。|Measure spacers at gate base and mid-height and relate them to source-drain boundaries.|有效隔離寬度的取樣高度明確。|The sampling height for effective isolation width is explicit.
診斷間隔層殘留薄膜|Diagnose spacer-film residues|查看應暴露的源汲極平面，分辨連續薄膜與孤立殘粒。|Inspect source-drain surfaces that should be exposed and distinguish continuous film from isolated particles.|平面清除與側壁保留不是同一影像判據。|Horizontal clearance and sidewall retention use different image criteria.
比較間隔層材料電性|Compare spacer dielectric behavior|用示意低 k 與較高 k 材料比較寄生電容，同時查看機械及蝕刻相容性。|Compare parasitic capacitance for illustrative lower-k and higher-k spacers while checking mechanical and etch compatibility.|低介電常數選擇沒有忽略尺寸或可靠度代價。|A lower-k choice does not ignore dimensional or reliability costs.
配置 FinFET 三維間隔層分支|Configure the FinFET spacer branch|讓間隔層包覆鰭與閘極交會的三維角落，檢查盲區。|Wrap spacers around three-dimensional fin-gate intersections and inspect hidden corners.|三維角部完整性不能由單一平面截面代替。|One planar section does not substitute for three-dimensional corner integrity.
核對奈米片犧牲層分支|Verify the nanosheet sacrificial-layer branch|在奈米片路線辨識 Si 與 SiGe 疊層，標示稍後需保留和移除者。|Identify silicon and silicon-germanium layers in the nanosheet route and label retained and sacrificial layers.|犧牲層與通道層角色清楚，非將所有層都當成通道。|Sacrificial and channel-layer roles are clear rather than treating every layer as a channel.
形成內間隔層凹槽概念|Form the inner-spacer recess concept|在奈米片分支於源汲極切面側向回縮犧牲層，追蹤各層均勻性。|In the nanosheet branch, recess sacrificial layers laterally from the source-drain cut face and track uniformity among layers.|內間隔凹槽的深度按各層驗證，且通道未被過度損耗。|Recess depth is checked layer by layer without excessive channel loss.
填充奈米片內間隔層|Fill nanosheet inner spacers|在側向凹槽放入絕緣材料並移除外部多餘材料，查看凹槽殘留。|Fill lateral recesses with dielectric, remove external excess and inspect retained material inside the recesses.|內間隔層封住預定區域但未堵住保留通道。|Inner spacers occupy intended regions without obstructing retained channels.
驗證內外間隔層隔離|Verify inner and outer spacer isolation|沿源汲極至未來閘極的可能路徑追蹤，檢查是否有未隔離缺口。|Trace potential paths from source-drain regions to the future gate and inspect unisolated gaps.|內外間隔層的不同位置及隔離功能均被說明。|The distinct locations and isolation functions of inner and outer spacers are explained.
交接閘極與間隔層幾何|Handoff gate and spacer geometry|整合閘長、線緣、間隔寬度及介電證據，註明源汲極和替代閘極仍待後續完成。|Combine gate length, edge, spacer-width and dielectric evidence and note that source-drain and replacement-gate work follows later.|完成的是本模組幾何，不誤稱整個電晶體已可運作。|Completion refers to this module's geometry rather than a fully functioning transistor.
'''

DIAG={
1:'''介電層遺漏或接觸節點放錯|Missing dielectric or misassigned contact nodes
圖層極性、原點或版次混用|Mixed layer tones, origins or revisions
把平面尺寸沿用到三維結構|Planar dimensions carried into three-dimensional structures
基板產品型號與截面對不上|Substrate product type mismatches the section
把導電型態與離子電荷混淆|Conductivity type confused with ionic charge
量測跨過缺口或尺度校正錯誤|Measurement crossing the notch or incorrect scale calibration
前後面未對位或彎曲未分離|Unregistered surfaces or unseparated bending
支撐方式不同或參考面不一致|Changed support conditions or inconsistent reference planes
平均化視窗太大而掩蓋局部臺階|An averaging window hiding local steps
表面晶面與晶圓方位標籤互換|Swapped surface-plane and wafer-azimuth labels
夾持位置與崩角重疊|Clamping positions overlapping chipped edges
粒子門檻、有效面積或照明改變|Changed particle threshold, inspected area or illumination
線状缺陷被切成多個粒子|A line defect split into several particle detections
掃描尺度或傾斜去除方式不同|Different scan scales or tilt-removal methods
光學模型簡化過度或參數相關|Oversimplified optical model or correlated parameters
分析空白污染或量測能力不足|Contaminated blanks or insufficient measurement capability
厚度修正、邊緣修正或接觸失效|Thickness corrections, edge effects or bad contacts
把總厚度當作磊晶厚度|Total thickness mistaken for epitaxial thickness
頂矽與埋氧光學參數互相補償|Compensating optical parameters for top silicon and buried oxide
外來粒子與內部晶體缺陷混類|External particles mixed with crystal defects
搬運模型未標出實際接觸面|Handling model omits actual contact surfaces
換槽後的 ID 與位置未更新|Wafer IDs and positions not updated after slot changes
空間變異混入同點重複測試|Spatial variation included in same-point repeats
座標方向、缺口定位或門檻不一致|Inconsistent axes, notch registration or thresholds
監控片與產品片熱歷史不同|Monitor and product wafers have different thermal histories
缺測項被默認為合格|Missing evidence silently treated as passing''',
2:'''總純度標示掩蓋關鍵雜質|Bulk purity conceals critical impurities
局部熱梯度被平均溫度遮蔽|Local gradients hidden by average temperature
籽晶方向與拉引軸誤配|Seed direction mismatched to pulling axis
僅用外徑判斷位錯是否消失|Using diameter alone to judge dislocation elimination
展肩變化過快或熱場不連續|Abrupt shoulder growth or discontinuous thermal field
回授延遲或直徑感測雜訊|Feedback delay or noisy diameter sensing
忽略熔體耗用及偏析|Ignored melt consumption and segregation
坩堝接觸差異被遺漏|Omitted differences in crucible contact
把流動控制誤當單純溫度控制|Flow control mistaken for temperature adjustment
偏心修磨造成同軸性不足|Eccentric grinding compromises coaxiality
缺口未依晶向校核或引入裂紋|Unverified notch orientation or introduced cracks
忘記鋸縫及精加工餘量|Omitted kerf and finishing allowances
線鋸振動與進給痕混淆|Wire vibration confused with feed marks
局部移除不均造成楔形厚度|Uneven removal creates a wedge-shaped thickness profile
倒角不連續或邊缘過度移除|Discontinuous bevel or excessive edge removal
可見切痕消失但次表面損傷仍在|Visible marks removed while subsurface damage remains
壓力集中造成微刮傷或邊緣塌陷|Pressure concentration causes scratches or edge roll-off
清洗功能與污染類型不符|Cleaning function mismatches contamination class
把潤濕性當作全面潔淨指標|Wettability used as a complete cleanliness proxy
粒子搬移或再沉積誤算為去除|Particle relocation or redeposition counted as removal
空白或背景漂移造成假下降|Blank or background drift creates a false decrease
未考慮下游要求的表面終態|Downstream surface-state requirements ignored
流動死角留下殘液|Stagnant flow regions retain liquid
液滴殘留乾燥成局部沉積|Retained droplets dry into localized deposits
前後圖未對位或偵測設定不同|Unregistered maps or changed detection settings
表面再氧化或吸附未被追蹤|Untracked reoxidation or adsorption''',
3:'''隔離邊界侵入通道|Isolation boundaries intrude into channels
混用 LOCOS 與 STI 的幾何機制|LOCOS and STI geometrical mechanisms are mixed
緩衝層位置或材料角色誤標|Buffer location or material role mislabeled
硬遮罩未兼顧研磨停止需求|Hard mask ignores polishing-stop requirements
以平均膜厚忽略最薄區|Average thickness hides the thinnest region
臺階薄膜局部露底|Local coating breakthrough at topographic steps
只校中心而忽略旋轉|Center-only alignment ignores rotation
曝光極性與保留區相反|Exposure tone reverses retained regions
不同高度的 CD 被直接比較|CD values at different heights are compared directly
硬遮罩開口伴隨過度底層消耗|Mask opening excessively consumes the underlayer
去膠殘留與硬遮罩混判|Resist residue mistaken for hard mask
墊氧化開口超出遮罩邊界|Pad-oxide opening extends beyond mask boundaries
深度分布被單點數據取代|Depth distribution replaced by one point
入口輪廓造成填充提早封口|Entrance profile causes premature fill closure
平均深度掩蓋角部微溝|Average depth hides corner microtrenches
殘留清洗侵蝕矽側壁|Residue cleaning erodes silicon sidewalls
襯氧化的矽消耗未計入|Silicon consumption by liner oxidation omitted
把共形覆蓋直接等同無空洞填充|Conformal coverage equated with void-free fill
兩側生長前緣封住入口|Opposing growth fronts close the entrance
膜收縮與材料移除混淆|Film shrinkage confused with removal
研磨端點與停止層餘量不符|Polish endpoint conflicts with stop-layer reserve
寬圖案凹陷與密集區侵蝕混合|Wide-feature dishing mixed with dense-region erosion
去停止層損耗填充氧化物|Stop-layer removal also consumes fill oxide
對不同元件強制同一回蝕高度|One recess height imposed on different devices
面積與周長正規化混用|Area and perimeter normalization mixed
隔離完成但表面高度仍不合需求|Isolation complete but surface height remains unsuitable''',
4:'''井区型態或本體偏壓極性錯誤|Wrong well type or body-bias polarity
深井邊界沒有形成連續隔離|Deep-well boundaries fail to form continuous isolation
植入窗口重疊或保護區缺口|Overlapping implant windows or gaps in protected areas
只看平均射程而漏掉穿透尾端|Mean range hides penetration tails
摻雜元素與離子電荷態混淆|Dopant species confused with ion charge state
把能量變化當成劑量變化|Energy variation mistaken for dose variation
積分單位、面積或電荷態錯誤|Incorrect integration units, area or charge state
把多次分布取最大而非相加|Taking the maximum rather than summing profiles
高斯近似忽略晶向通道化|Gaussian approximation ignores channeling
抑制通道化卻加重幾何遮蔽|Channeling reduction worsens geometric shadowing
傾角与方位角紀錄混用|Tilt and azimuth records mixed
轉向停留造成邊緣劑量異常|Turnaround dwell creates edge-dose anomalies
局部充電被平均束流掩蓋|Local charging hidden by average beam current
化學濃度直接當成載子濃度|Chemical concentration treated as carrier concentration
硬化光阻外觀清除但底層殘留|Hardened resist appears cleared but residue remains
透明表面被誤判沒有化學殘留|Transparent surface misread as chemically clean
忽略井區側向擴散|Lateral well diffusion omitted
僅比較最高溫而忽略時間|Peak temperatures compared without duration
發射率差異造成假溫差|Emissivity differences create apparent temperature variation
活化估計未納入補償與方法差異|Activation estimate omits compensation and method differences
植入峰值被當作接面位置|Implant peak mistaken for junction position
探針接觸異常未複測|Probe-contact outliers not remeasured
低場漏電與崩潰機制混判|Low-field leakage confused with breakdown
將平面通道植入強套奈米片|Planar channel implantation imposed on nanosheets
井區邊界與 STI 角部未對位|Well boundaries not registered to STI corners
後續熱歷史造成剖面繼續改變|Later thermal history continues changing the profile''',
5:'''傳統氧化與高 k 路線混接|Conventional oxide and high-k routes mixed
清洗終態與介電需求不符|Cleaned surface state mismatches dielectric requirements
初始氧化厚度漏算或重算|Initial oxide omitted or double-counted
以生長速度推斷相同品質|Growth speed used to infer identical quality
常數速率外推超出適用區|Constant rate extrapolated beyond its regime
薄氧化層超出簡化模型有效範圍|Thin oxide outside simplified-model validity
未計入被氧化消耗的矽|Oxidation-consumed silicon omitted
比較晶向時其他條件同時改變|Other conditions change during orientation comparison
忽略摻雜對成長動力學影響|Doping effects on growth kinetics ignored
批次平均掩蓋晶舟位置差異|Batch average hides boat-position differences
徑向變化與晶圓間差異混合|Radial variation pooled with wafer-to-wafer differences
升降溫期間成長貢獻漏算|Growth during heating and cooling omitted
少量粒子支配粗糙度數值|A few particles dominate roughness statistics
厚度與光學常數參數互補|Compensating thickness and optical-constant parameters
電極有效面積或背接觸不明|Unclear effective area or backside contact
未依基板型態判讀電壓極性|Voltage polarity interpreted without substrate type
EOT 與實體厚度混用|EOT confused with physical thickness
串聯電容被誤算成並聯|Series capacitors treated as parallel
只看鈍化改善而漏掉電容代價|Passivation improvement hides capacitance cost
把平帶位移唯一歸因於固定電荷|Flat-band shift uniquely assigned to fixed charge
未控制頻率與量測條件|Frequency and measurement conditions uncontrolled
相同電壓被當成相同電場|Same voltage mistaken for the same field
空間群聚與孤立離群值混合|Spatial clusters mixed with isolated outliers
未失效樣本遭刪除或錯誤編碼|Unfailed samples deleted or miscoded
電性資料對應錯誤熱歷史|Electrical data paired with wrong thermal history
單一厚度合格掩蓋漏電或缺陷|Passing thickness hides leakage or defects''',
6:'''沉積機制不符合覆蓋幾何|Deposition mechanism incompatible with coverage geometry
成核差異源於表面終態|Nucleation differences arise from surface termination
總壓力未揭示氣體來源|Total pressure does not reveal gas origin
入口流量未反映表面耗用|Inlet flow does not reflect surface consumption
沉積熱歷史超出下層相容範圍|Deposition thermal history incompatible with underlying layers
未達表面飽和或誤認單層成長|Surface not saturated or monolayer growth assumed
反應物與副產物吹掃不完全|Incomplete purge of reactant and byproducts
表面反應未完成或殘留配基|Incomplete surface reaction or residual ligands
循環間反應物重疊|Reactant overlap between cycles
成核延遲被強制過原點擬合掩蓋|Nucleation delay hidden by a forced-origin fit
只看成長率而忽略膜質|Growth rate considered without film quality
孔底反應物不足而陪片正常|Bottom reactant starvation despite normal planar monitors
電漿反應改善伴隨下層損傷|Improved plasma reaction accompanies underlayer damage
島狀膜被名義厚度誤判成連續|Nominal thickness masks discontinuous islands
表面反應與供料限制混判|Surface-reaction and delivery limitations mixed
未用獨立變量比較限制機制|Limiting mechanism inferred without independent variables
裝載面積或晶舟位置改變|Changed reactive area or boat position
膜應力改善犧牲組成或電性|Stress improvement sacrifices composition or electrical quality
入口封閉留下内部空洞|Entrance closure traps internal voids
視線遮蔽造成側壁或底部薄化|Line-of-sight shadowing thins sidewalls or bottoms
靶材侵蝕歷史影響沉積分布|Target erosion history changes deposition distribution
反應式濺鍍存在歷史遲滯|Reactive sputtering exhibits history-dependent hysteresis
覆蓋比分母位置未一致|Coverage-ratio reference locations differ
曲率公式超出薄膜假設|Curvature formula used outside thin-film assumptions
單一光學量有多種成分解釋|One optical measurement permits multiple composition interpretations
膜層局部合格但下游不相容|Local film acceptance hides downstream incompatibility''',
7:'''光阻極性與圖案保留區相反|Resist tone reverses intended retained regions
光源與材料吸收波段不匹配|Source and material absorption bands mismatch
保存及批次差異未被追蹤|Storage and batch differences untracked
抗反射層優化忽略後續開口|Antireflective optimization ignores later opening
基底污染造成針孔或凸點|Substrate contamination produces pinholes or bumps
脫水後再吸附改變表面|Re-adsorption changes the dehydrated surface
促進層過量或材料不相容|Excess promoter or incompatible material
偏心滴注或氣泡造成缺膜|Off-center dispensing or bubbles cause missing coverage
初始展膜缺陷被歸咎最終轉速|Initial spreading defects blamed on final speed
黏度或溶劑變化使經驗曲線失效|Viscosity or solvent changes invalidate an empirical curve
揮發及乾燥前緣影響膜厚|Evaporation and drying fronts affect thickness
去邊範圍侵入有效圖案|Edge removal invades usable patterns
背面殘留造成夾盤高度誤差|Backside residue creates chucking-height errors
量測時距不同造成表觀厚度差|Different timing creates apparent thickness changes
接觸熱阻造成局部升溫差|Contact resistance produces local heating differences
表面乾燥掩蓋底部溶劑|Surface dryness hides retained bottom solvent
局部裂紋被平均收縮掩蓋|Local cracks hidden by average shrinkage
錯將材料專屬再吸水套用全部|Material-specific rehydration imposed universally
教學模組順序誤當生產順序|Teaching-module order mistaken for production order
PEB 與軟烤機制混淆|PEB mechanism confused with soft baking
顯影過度或非目標區溶失|Overdevelopment or unintended film loss
開口未清底或保留線條過度溶解|Uncleared openings or excessive retained-line dissolution
殘留顯影液使反應繼續|Retained developer allows continued dissolution
毛細倒塌誤判為曝光橋接|Capillary collapse mistaken for exposure bridging
平均 CD 掩蓋缺口及殘膠|Mean CD hides missing features and scum
硬烤改變輪廓或降低可剝除性|Hard bake changes profile or reduces stripability''',
8:'''鏡像、倍率或座標方向混淆|Confused inversion, reduction or coordinate directions
使用舊版光罩或錯誤極性|Wrong reticle revision or tone
光罩重複缺陷被當成隨機粒子|Repeating mask defect mistaken for random particles
波長比較同時改變其他參數|Other parameters changed during wavelength comparison
只看解析度忽略焦深|Resolution considered without depth of focus
將 DUV 透鏡模型套到 EUV|DUV lens model incorrectly applied to EUV
把浸潤液路線帶入真空 EUV|Immersion-fluid route carried into vacuum EUV
傳輸損失與反射損失混計|Propagation and reflection losses conflated
標記被覆蓋或對比不足|Marks covered or lacking contrast
平移殘差仍有共同方向|Translation residuals retain a common direction
旋轉錯誤被平移勉強補償|Rotation error forced into translation correction
倍率項與平移項互相代償|Magnification and translation compensate incorrectly
插值平滑掉局部臺階|Interpolation smooths away local steps
最佳平均焦點掩蓋最差位置|Best average focus hides the worst location
焦距與劑量變數未独立|Focus and dose variables are not independent
單一特徵最佳點取代共同視窗|One feature optimum replaces the common window
只採密集或孤立的一類圖案|Only dense or isolated patterns sampled
照明優化與圖案方向不匹配|Illumination optimization mismatches pattern orientation
只看光罩像不像目標而不看成像|Mask resemblance judged instead of wafer imaging
CD 與位置誤差未合併判讀|CD and placement errors not interpreted together
標靶套刻代表性不足|Overlay target lacks device representativeness
場內模式與全片模式混合|Intra-field and wafer-level patterns mixed
平均 CD 掩蓋隨機尾端缺陷|Mean CD hides stochastic tail defects
替代圖案化路線的依賴混用|Dependencies from alternative patterning routes mixed
忽略視場、分場與接縫限制|Field, partitioning and stitching limits omitted
校正資料套用到不同圖層條件|Corrections applied to incompatible layers or conditions''',
9:'''目標材料與停止層標錯|Target material or stop layer mislabeled
忽略晶向選擇性或輪廓需求|Crystallographic selectivity or profile requirements ignored
最薄遮罩或清底餘量未納入|Thinnest mask or clearing margin omitted
前段圖案缺陷誤歸因蝕刻|Upstream pattern defects blamed on etching
底層開口過度消耗光阻|Underlayer opening excessively consumes resist
離子供給與入射能量混為一談|Ion supply confused with incident energy
方向分布改變造成側壁損失|Changed angular distribution causes sidewall loss
深孔供料不足被誤診能量不足|Deep-feature starvation misdiagnosed as insufficient energy
側壁保護過強堵底或過弱側蝕|Passivation blocks bottoms or permits undercut
用總壓力直接推定停留時間|Residence time inferred directly from total pressure
溫度改變吸附及副產物揮發|Temperature changes adsorption and byproduct volatility
窄孔清除落後被平均速率掩蓋|Narrow-feature lag hidden by average etch rate
圖案密度與深寬比效應混合|Pattern-density effects mixed with aspect-ratio effects
只有頂部 CD 缺少深度輪廓|Top CD available without depth-resolved profile
中段弓形被當成單純錐度|Mid-depth bowing treated as simple taper
底角微溝被平均深度隱藏|Corner microtrenches hidden by average depth
忽略保護層也有有限移除率|Finite removal of the protected layer ignored
雜訊峰或感測延遲被當真端點|Noise peaks or sensor delay mistaken for endpoint
厚度差異使固定時間失效|Thickness variation invalidates fixed timing
過長過蝕刻損耗遮罩及停止層|Excess overetch consumes mask and stop layers
將每循環移除量當固定整原子層|Per-cycle removal assumed to equal a whole atomic layer
高選擇比被誤當無限選擇比|High selectivity mistaken for infinite selectivity
浮接圖案局部累積電荷|Local charge accumulates on floating patterns
聚合殘留與材料本體混淆|Polymer residue confused with the material itself
CD 的高度或邊缘定義不同|Different CD heights or edge definitions
俯視正常但三維輪廓異常|Normal top view hides abnormal three-dimensional profiles''',
10:'''犧牲閘極與最終金屬閘混淆|Dummy gate confused with final metal gate
堆疊組合不屬同一路線|Stack elements belong to incompatible routes
頂蓋與閘介電層功能混用|Gate cap and dielectric functions mixed
閘線未跨越預期主動區|Gate line does not cross the intended active area
線端縮短被中段 CD 掩蓋|Line-end shortening hidden by mid-line CD
硬遮罩粗糙或餘量不足|Rough hard mask or insufficient thickness reserve
清底過程損伤下方介電層|Clearing damages the underlying dielectric
端點延遲或材料訊號辨識錯誤|Endpoint delay or misidentified material signal
不同材料殘腳被相同處理|Feet of different materials treated identically
側壁角度變化影響間隔層|Sidewall-angle changes affect spacer formation
整體偏移混入局部粗糙統計|Global shift included in local roughness statistics
外觀完整掩蓋介電電性損傷|Intact appearance hides dielectric electrical damage
清理造成有效尺寸或介電損耗|Cleaning causes dimensional or dielectric loss
襯層厚度未計入側向尺寸|Liner thickness omitted from lateral dimensions
平面膜厚代表不了角部覆蓋|Planar thickness does not represent corner coverage
水平清除時側壁也被過度移除|Sidewalls over-etched during horizontal clearance
肩部修整破壞隔離連續性|Shoulder trimming breaks isolation continuity
不同高度的間隔寬度混用|Spacer widths at different heights mixed
源汲極平面仍有連續残膜|Continuous residual film remains on source-drain surfaces
低 k 選材忽略結構或可靠度|Low-k selection ignores structural or reliability costs
二維截面漏掉三維交會盲區|Two-dimensional section misses hidden three-dimensional intersections
把犧牲 SiGe 層當保留通道|Sacrificial SiGe mistaken for retained channels
各層回縮不均或通道侵蝕|Unequal recess among layers or channel erosion
填充材料殘留堵塞保留通道|Fill residue obstructs retained channels
內外間隔層之間存在未隔離缺口|An unisolated gap exists between inner and outer spacers
把模組幾何完成誤當電晶體功能完成|Module geometry completion mistaken for transistor functionality'''
}

SOURCEROWS=[
('sc-sumco','SUMCO','Production Processes','https://www.sumcosi.com/english/products/process/','turn42view0','矽晶體生長、切片、研磨、拋光與特殊晶圓的公開原理。','Public principles of crystal growth, slicing, lapping, polishing and specialized wafers.'),
('sc-kla-metrology','KLA','Metrology — Certified and Remanufactured','https://www.spts.com/products/certified-remanufactured/cr-metrology','turn37search34','薄膜、套刻與線寬量測方法的設備商公開說明。','Manufacturer overview of film, overlay and critical-dimension metrology.'),
('sc-lam-process','Lam Research','Our Processes','https://www.lamresearch.com/products/our-processes/','turn37search1','沉積、蝕刻、去膠、清洗及製程監控的功能。','Roles of deposition, etching, stripping, cleaning and process monitoring.'),
('sc-lam-deposition','Lam Research','Deposition','https://www.lamresearch.com/products/our-processes/deposition/','turn42view1','薄膜沉積類型與介電、導體薄膜用途。','Deposition families and uses of dielectric and conducting films.'),
('sc-lam-etch','Lam Research','Etch','https://www.lamresearch.com/products/our-processes/etch/','turn42view2','圖案蝕刻、選擇性移除與原子層蝕刻的公開原理。','Public principles of pattern etching, selective removal and atomic-layer etching.'),
('sc-applied-implant','Applied Materials','Materials Modification','https://www.appliedmaterials.com/us/en/semiconductor/products/modify.html','turn42view3','植入摻雜與材料改質的基本機制，非植入配方。','Basic mechanisms of implantation and materials modification, not implant recipes.'),
('sc-ualberta-oxidation','University of Alberta nanoFAB','Silicon Thermal Oxidation Calculator — Model Notes','https://toolbox.nanofab.ualberta.ca/sithox/','turn42view4','熱氧化模型、初始氧化層、晶向及模型適用範圍。','Oxidation models, initial oxide, crystal orientation and model validity.'),
('sc-mc-index','MicroChemicals','Application Notes','https://www.microchemicals.com/DOWNLOADS/Application-Notes/','turn42view5','製造商原創微影、晶圓、植入與乾濕蝕刻技術文件入口。','Manufacturer-authored technical notes on lithography, wafers, implantation and etching.'),
('sc-mc-spin','MicroChemicals','Spin-coating of Photoresists','https://www.microchemicals.com/dokumente/application_notes/spin_coating_photoresist.pdf','turn42view6','旋塗、膜厚與溶劑/流動因素；本文未採用其中配方參數。','Spin coating, thickness and solvent/flow effects; the course does not adopt the recipe parameters.'),
('sc-mc-softbake','MicroChemicals','Softbake of Photoresists','https://www.microchemicals.com/dokumente/application_notes/softbake_photoresist.pdf','turn42view7','軟烤的溶劑移除、熱傳與膜層變化原理。','Soft-bake solvent removal, heat transfer and film changes.'),
('sc-mc-develop','MicroChemicals','Development of Photoresists','https://www.microchemicals.com/dokumente/application_notes/development_photoresist.pdf','turn42view8','光阻顯影機制、相容性與非目標膜損耗。','Resist development mechanisms, compatibility and unwanted film loss.'),
('sc-mc-prep','MicroChemicals','Substrate Preparation: Cleaning and Adhesion Promotion','https://www.microchemicals.com/dokumente/application_notes/substrate_cleaning_adhesion_photoresist.pdf','turn42view9','表面清潔、脫水與附著促進的原理。','Principles of surface cleaning, dehydration and adhesion promotion.'),
('sc-imec-nanosheet','imec','Entering the Nanosheet Transistor Era','https://www.imec-int.com/en/articles/entering-nanosheet-transistor-era-0','turn42view10','奈米片及內間隔層整合挑戰；屬研究案例，非完整代工廠流程。','Nanosheet and inner-spacer integration challenges; research context rather than a complete foundry flow.'),
('sc-asml-metrology','ASML','Measuring Accuracy','https://www.asml.com/en/technology/lithography-principles/measuring-accuracy','turn42view11','微影對準、套刻、焦距及檢測原理。','Lithographic alignment, overlay, focus and inspection principles.'),
('sc-asml-optics','ASML','Lenses and Mirrors','https://www.asml.com/en/technology/lithography-principles/lenses-and-mirrors','turn42view12','DUV 與 EUV 成像光學、數值孔徑及浸潤原理。','DUV/EUV imaging optics, numerical aperture and immersion principles.'),
('sc-asml-light','ASML','Light and Lasers','https://www.asml.com/en/technology/lithography-principles/light-and-lasers','turn42view13','微影波長及 EUV 光源與傳播的背景原理。','Background principles of lithographic wavelength and EUV generation and propagation.')
]

META={
1:('製程整合與來料品質','Process integration and incoming quality',
'建立能連結材料、座標、量測與元件路線的來料證據。26 個操作包含剖面建模與真實量測方法的判讀。',
'Build incoming evidence connecting material, coordinates, metrology and device routes. The 26 operations combine cross-section modeling with interpretation of real measurement methods.',
['sc-sumco','sc-kla-metrology'],
'量測數字只有在量測位置、參考面、單位與方法一致時才可比較；示範驗收界線由課程情境提供，不是通用產業規格。',
'Measurements are comparable only with consistent locations, reference planes, units and methods. Exercise acceptance limits are scenario inputs, not universal industry specifications.'),
2:('晶體、晶圓製備與清洗','Crystal growth, wafer preparation and cleaning',
'從晶棒生長到潔淨表面交接，分開材料去除、晶格品質、污染移除與再污染。',
'Follow ingot growth through clean-surface handoff while separating stock removal, crystal quality, decontamination and recontamination.',
['sc-sumco','sc-mc-prep','sc-lam-process'],
'表面製備會改變幾何、化學終態與缺陷；清除一種污染不保證其他類別也已移除，必須以對應量測確認。',
'Surface preparation changes geometry, termination and defects. Removing one contaminant class does not prove removal of others; corresponding measurements are needed.'),
3:('淺溝槽隔離 STI','Shallow-trench isolation',
'以隔離截面串連硬遮罩、溝槽蝕刻、襯層、填充、研磨與回蝕，保留平面與鰭式元件分支。',
'Link hard masks, trench etching, liners, fill, polishing and recess through isolation sections, with separate planar and fin-device branches.',
['sc-lam-deposition','sc-lam-etch','sc-mc-index'],
'隔離品質同時受幾何、材料連續性及局部電場影響。俯視開口合格不代表深槽填充、角部或電性也合格。',
'Isolation quality depends on geometry, material continuity and local fields. A passing top-view opening does not establish acceptable deep fill, corners or electrical behavior.'),
4:('井區、通道植入與退火','Well and channel implantation and annealing',
'以濃度剖面、損傷圖與電性地圖區分植入、活化及擴散；通道調整列為傳統平面元件分支。',
'Use concentration profiles, damage maps and electrical maps to distinguish implantation, activation and diffusion; channel adjustment is a conventional planar-device branch.',
['sc-applied-implant','sc-mc-index','sc-imec-nanosheet'],
'植入面劑量、深度分布、化學濃度與活性載子濃度是不同量。退火可能修復損傷並活化摻雜，也會改變擴散剖面。',
'Implanted areal dose, depth distribution, chemical concentration and active-carrier concentration are different quantities. Annealing can repair damage and activate dopants while also changing diffusion profiles.'),
5:('閘極介電層與熱氧化','Gate dielectrics and thermal oxidation',
'分開傳統氧化與高 k 分支，以物理厚度、等效氧化厚度、C-V、漏電及失效分布驗證介電層。',
'Separate conventional oxide and high-k branches and evaluate them with physical thickness, EOT, C-V, leakage and failure distributions.',
['sc-ualberta-oxidation','sc-lam-deposition','sc-kla-metrology'],
'介電堆疊的幾何厚度與電性等效厚度不同。光學、電容及漏電各自對材料的不同特性敏感，不能互相完全替代。',
'Geometric thickness differs from electrical equivalent thickness. Optical, capacitance and leakage measurements probe different material properties and are not interchangeable.'),
6:('ALD、CVD 與 PVD 薄膜','ALD, CVD and PVD films',
'拆解成核、供料、表面反應、覆蓋、應力與膜質量測；三種沉積技術是依目的選用的分支。',
'Decompose nucleation, delivery, surface reactions, coverage, stress and film metrology; deposition families are purpose-dependent alternatives.',
['sc-lam-deposition','sc-mc-index','sc-kla-metrology'],
'名義膜厚不足以決定共形性、連續性或材料品質。ALD 的自限半反應可改善控制，但每循環成長量依材料及條件而變。',
'Nominal thickness does not determine conformality, continuity or material quality. Self-limiting ALD half-reactions improve control, but growth per cycle depends on material and conditions.'),
7:('光阻塗佈、烘烤與顯影','Resist coating, baking and development',
'以光阻材料相容性串連塗佈至圖案驗收；曝光結果在本模組作為已校核輸入，下一模組深入曝光機制。',
'Connect coating through pattern acceptance using material compatibility. Verified exposure is an input here; the next module examines exposure mechanisms in depth.',
['sc-mc-prep','sc-mc-spin','sc-mc-softbake','sc-mc-develop'],
'光阻極性、吸收、烘烤與顯影彼此耦合。實際先後為塗佈、適用前烤、曝光、適用曝光後烤、顯影；教學模組排序不是生產路由。',
'Resist tone, absorption, baking and development are coupled. Physical order is coating, applicable pre-bake, exposure, applicable post-exposure bake and development; teaching-module order is not a production route.'),
8:('曝光、對準、套刻與 EUV','Exposure, alignment, overlay and EUV',
'用光路、座標、焦距劑量矩陣與誤差向量理解曝光；DUV、浸潤、EUV 與多重圖案化均標為替代情境。',
'Use optical paths, coordinates, focus-exposure matrices and error vectors to understand exposure, with explicit DUV, immersion, EUV and multipatterning alternatives.',
['sc-asml-metrology','sc-asml-optics','sc-asml-light'],
'解析度、焦深、劑量、套刻與隨機缺陷是不同的成像限制。校正平均偏差不能自動消除局部或隨機尾端缺陷。',
'Resolution, depth of focus, dose, overlay and stochastic defects impose different imaging limits. Correcting a mean bias does not automatically eliminate local or stochastic-tail defects.'),
9:('蝕刻與圖案轉移','Etching and pattern transfer',
'從遮罩預算到三維剖面驗收，分開反應物供應、離子作用、鈍化、端點及選擇比。',
'Follow mask budgeting through three-dimensional acceptance while separating reactant supply, ion effects, passivation, endpoint and selectivity.',
['sc-lam-etch','sc-mc-index','sc-lam-process'],
'蝕刻速率、方向性與選擇比不是同一性能。材料、尺寸、圖案密度及深寬比會讓同一批次出現不同局部結果。',
'Etch rate, directionality and selectivity are distinct properties. Material, size, pattern density and aspect ratio can produce different local outcomes within one batch.'),
10:('閘極圖案與內外間隔層','Gate patterning and inner/outer spacers',
'建立閘極與外間隔層幾何，再比較 FinFET 與奈米片內間隔層分支；不取代後續源汲極及替代閘極模組。',
'Build gate and outer-spacer geometry and compare FinFET and nanosheet inner-spacer branches; later source-drain and replacement-gate modules remain necessary.',
['sc-imec-nanosheet','sc-lam-etch','sc-lam-deposition'],
'間隔層提供特定位置的電性隔離與幾何間距。奈米片內間隔層位於層間端部，不能用外側側壁間隔層的二維圖替代。',
'Spacers provide electrical isolation and geometric separation at specific locations. Nanosheet inner spacers occupy interlayer ends and cannot be represented by a two-dimensional outer-spacer diagram.')
}

def normalize(s):
    replacements={'比较':'比較','单纯':'單純','边缘':'邊緣','邊缘':'邊緣','缓衝':'緩衝','两側':'兩側','两種':'兩種','分别':'分別','分开':'分開','扩散':'擴散','异常':'異常','残留':'殘留','残差':'殘差','残層':'殘層','残膜':'殘膜','线状':'線狀','線状':'線狀','井区':'井區','与':'與','独立':'獨立','导體':'導體','实际':'實際','損伤':'損傷','顶部':'頂部','内部':'內部','剖面对':'剖面對','坐標':'座標','isotropic':'等向'}
    for a,b in replacements.items(): s=s.replace(a,b)
    return s

stages=[]
for number in range(1,11):
    rows=[r.split('|') for r in BLOCKS[number].strip().splitlines()]
    diagnoses=[r.split('|') for r in DIAG[number].strip().splitlines()]
    assert len(rows)==len(diagnoses)==26
    assert all(len(r)==6 for r in rows)
    zh,en,desc,desc_en,sources,principle,principle_en=META[number]
    stage={'id':f'sc-m{number:02d}','order':number,'title':zh,'titleEn':en,'description':desc,'descriptionEn':desc_en,
      'route':'教育模組；替代技術依步驟明示為分支，不代表同一片晶圓必須全部依序加工。',
      'routeEn':'Educational module; alternatives are labeled as branches and are not mandatory sequential operations on one wafer.',
      'sourceIds':sources,'steps':[]}
    for local,row in enumerate(rows,1):
        index=(number-1)*26+local
        sid=f'sc-{index:03d}'
        title,title_en,instruction,instruction_en,criterion,criterion_en=row
        diag,diag_en=diagnoses[local-1]
        # Distractors are authentic evidence for different operations within this module.
        # All are valid engineering statements, but only one directly verifies this step.
        options=[criterion,rows[(local+4)%26][4],rows[(local+12)%26][4]]
        options_en=[criterion_en,rows[(local+4)%26][5],rows[(local+12)%26][5]]
        shift=index%3
        options=options[shift:]+options[:shift]
        options_en=options_en[shift:]+options_en[:shift]
        answer=(3-shift)%3
        step={
          'id':sid,'order':local,'sequence':index,'title':normalize(title),'titleEn':title_en,
          'objective':normalize(criterion),'objectiveEn':criterion_en,
          'instruction':normalize('依示意模型，以自行準備或從參考來源取得的圖、量測資料或試算表進行：'+instruction),
          'instructionEn':'Use schematic models and diagrams, measurement data or worksheets you supply or obtain from referenced sources. '+instruction_en,
          'observation':normalize('保存本步操作前後的對照證據。判讀重點：'+criterion),
          'observationEn':'Keep before-and-after evidence for this operation. Interpret it against this criterion: '+criterion_en,
          'failure':normalize('若未符合判據，優先檢查：'+diag+'。這是待驗證的原因；回到相同測點或剖面比對，不能僅據異常外觀定因。'),
          'failureEn':'If the criterion is not met, investigate: '+diag_en+'. This is a hypothesis; compare matching sites or cross-sections before assigning a cause.',
          'check':normalize(criterion),'checkEn':criterion_en,
          'knowledge':[
            {'id':sid+'-k1','title':'本步的可檢核證據','titleEn':'Evidence for this operation','text':normalize(criterion+' 對應操作：'+instruction),'textEn':criterion_en+' Corresponding operation: '+instruction_en},
            {'id':sid+'-k2','title':'機制與診斷邊界','titleEn':'Mechanism and diagnostic limits','text':normalize(principle+' 本步特別排查：'+diag+'。'),'textEn':principle_en+' Specifically examine: '+diag_en+'.'}
          ],
          'quiz':{'question':f'哪一項證據最直接支持「{normalize(title)}」這一步的完成？','questionEn':f'Which evidence most directly supports completion of "{title_en}"?',
                  'options':[normalize(x) for x in options],'optionsEn':options_en,'answer':answer,
                  'explanation':normalize('本步驗收的是：'+criterion+' 其他選項雖可能是有效工程檢查，但不能取代本步證據。'),
                  'explanationEn':'This operation is accepted against: '+criterion_en+' The other options may be valid engineering checks but do not replace this evidence.'},
          'sourceIds':sources,'simulationOnly':True,'estimatedMinutes':8+(local%3)*2,
          'prerequisiteIds':[] if index==1 else [f'sc-{index-1:03d}'],
          'prerequisiteScope':'learning-sequence','activityMode':'guided-worksheet-and-evidence-review',
          'photoTopic':'semiconductor-cleanroom' if number in [2,6,7,8,9] else 'silicon-wafer',
          'sourceScope':'Principle-level references; exercises and qualitative checks are original educational subdivisions, not vendor recipes.'}
        stage['steps'].append(step)
    stages.append(stage)

data={
 'id':'semiconductor','part':'a','partTitle':'半導體製造教育工序 1–260','partTitleEn':'Semiconductor manufacturing learning operations 1–260',
 'contentStatus':'authored-educational-curriculum','stepCount':260,'moduleCount':10,
 'scope':'260 個原創雙語學習工序，為 520 步教材前半。以文件、剖面圖、示意資料及可選的自備試算表進行比對；網站並未因此具備每一工序的物理求解器。數目代表教學拆分，不是單一晶圓廠的通用製造配方。',
 'scopeEn':'260 original bilingual learning operations forming the first half of a 520-step curriculum. Use documents, cross-sections, illustrative data and optional external worksheets for comparison; this does not imply the website has a physical solver for every operation. The count represents educational subdivision, not a universal foundry recipe.',
 'sequenceNote':'prerequisiteIds 表示學習進度。量產路由需另依選定材料、元件、設備與經驗證程序建立；製程回圈及互斥分支不能直接按模組序號串成生產指令。',
 'sequenceNoteEn':'Prerequisites express learning progression. A manufacturing route must separately follow selected materials, devices, tools and qualified procedures; process loops and mutually exclusive branches cannot be concatenated by module number into production instructions.',
 'estimateNote':'estimatedMinutes 為單一閱讀/推演任務的規劃值，不是設備加工時間或保證完成時間。',
 'estimateNoteEn':'Estimated minutes are planning estimates for reading or analysis, not equipment cycle times or guaranteed completion times.',
 'materialContext':{'usage':'使用者提供內容僅供主題及術語對照；未複製課堂圖片、配方或長段文字。'},
 'stages':stages
}

sources=[]
for sid,publisher,title,url,ref,summary,summary_en in SOURCEROWS:
    sources.append({'id':sid,'publisher':publisher,'title':title,'titleEn':title,'url':url,
                    'summary':summary,'summaryEn':summary_en,'scope':'支援公開機制及量測概念；不逐字提供本教材工序，不背書教材驗收或代工配方。',
                    'scopeEn':'Supports public mechanisms and measurement concepts; does not supply these exercises verbatim or endorse their acceptance criteria or foundry recipes.',
                    'sourceType':'primary','retrievalRef':ref,'accessed':'2026-10-12',
                    'imageReuse':'Reference only; no image-reuse permission is implied.'})

allsteps=[step for stage in stages for step in stage['steps']]
assert len(allsteps)==260
assert [s['id'] for s in allsteps]==[f'sc-{i:03d}' for i in range(1,261)]
assert len({s['title'] for s in allsteps})==260
assert len({s['titleEn'] for s in allsteps})==260
assert len({s['instruction'] for s in allsteps})==260
assert len({s['check'] for s in allsteps})==260
assert len({s['failure'] for s in allsteps})==260
assert all(len(s['knowledge'])==2 for s in allsteps)
assert all(len(s['quiz']['options'])==3 and s['quiz']['options'][s['quiz']['answer']]==s['check'] for s in allsteps)
assert all(s['sourceIds'] and set(s['sourceIds'])<=set(x['id'] for x in sources) for s in allsteps)
for step in allsteps:
    for field in ['title','objective','instruction','observation','failure','check']:
        assert step[field] and step[field+'En'], (step['id'],field)

(ROOT/'semiconductor_a.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
(ROOT/'sources_semiconductor_a.json').write_text(json.dumps(sources,ensure_ascii=False,indent=2)+'\n')
validation={'steps':len(allsteps),'modules':len(stages),'stepsPerModule':[len(s['steps']) for s in stages],
            'uniqueTitles':len({s['title'] for s in allsteps}),'uniqueInstructions':len({s['instruction'] for s in allsteps}),
            'uniqueAcceptanceChecks':len({s['check'] for s in allsteps}),'uniqueDiagnosticPrompts':len({s['failure'] for s in allsteps}),
            'knowledgeItems':sum(len(s['knowledge']) for s in allsteps),'quizAnswers':dict(Counter(s['quiz']['answer'] for s in allsteps)),
            'primarySources':len(sources),'firstId':allsteps[0]['id'],'lastId':allsteps[-1]['id'],
            'limitations':['Principle-level source checking; original exercises are not independently validated production instructions.','Worksheets and evidence review, not 260 independently implemented physical simulators.','Branch and learning-order annotations must be preserved during integration.']}
(ROOT/'semiconductor_a_validation.json').write_text(json.dumps(validation,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(validation,ensure_ascii=False,indent=2))
