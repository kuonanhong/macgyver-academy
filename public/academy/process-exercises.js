import { COMPUTING_SUBJECTS, renderComputingVisual, computingVisualFamily } from './computing-visuals.js';
import { hasWorldVisual, renderWorldVisual, worldVisualFamily } from './world-project-visuals.js';
import {renderPackagingVisual,packagingVisualFamily} from './packaging-visuals.js';
import {V7_STAGE_FAMILIES,V7_CONTEXT_FAMILIES,renderV7Context} from './v7-contexts.js';
import {renderSemiconductorVisual,semiconductorVisualFamily} from './semiconductor-visuals.js';
import {ELECTRONICS_SUBJECTS,renderElectronicsVisual,electronicsVisualFamily} from './electronics-visuals.js';
import {EXPANSION_STAGE_FAMILIES,EXPANSION_CONTEXT_FAMILIES,renderExpansionContext} from './expansion-contexts.js';
/** Original, source-led educational exercises. Numerical specimens are synthetic;
 * they are not factory recipes, OEM drawings, acceptance specifications or CAD.
 * Explicit tasks are authored; remaining curricula select shared semantic models.
 */
import {resolveExpansionExercise,renderExpansionScene} from './expansion-exercises.js';
const bi=(zh,en)=>({zh,en});
const ctl=(id,zh,en,min,max,step,initial,target,unit='',tolerance=step/2)=>({id,label:bi(zh,en),min,max,step,initial,target,unit,tolerance});
const opt=(id,zh,en)=>({id,label:bi(zh,en)});
const esc=value=>String(value??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const clamp=(x,a,b)=>Math.max(a,Math.min(b,Number.isFinite(Number(x))?Number(x):a));
const TARGET={x:0,y:0,z:8,rotation:0};
function make(id,mode,scene,object,instruction,tool,evidence,extra={}){
 const spec={id,mode,scene,object,instruction,tool,evidence,controls:[],choices:[],expectedChoice:null,target:{...TARGET},provenance:'authored',coverage:bi('此工序有專屬教學任務；示例數值不代表量產規格。','A task authored for this step; specimen values are not production limits.'),...extra};
 spec.initialState={values:Object.fromEntries(spec.controls.map(c=>[c.id,c.initial])),choice:null,observed:false,performed:false};
 return spec;
}
const first26={
'sc-001':()=>make('cmos-layer-stack','assembly','cmos',bi('CMOS 剖面層堆疊','CMOS cross-section stack'),bi('依序加入基板、隔離／介電層、閘極、接觸孔與金屬互連，再對位最上層互連。','Add substrate, isolation/dielectric, gate, contact and metal; then align the final interconnect.'),bi('剖面圖層堆疊器','Cross-section layer builder'),bi('閘極控制通道；接觸孔把局部元件連到金屬層，兩者不是同一層。','The gate controls the channel; contacts connect local devices to metal routing.'),{controls:[ctl('phase','已建立的圖層','Layers built',0,5,1,0,5,'layers',0)],layers:['Si substrate','Isolation / oxide','Gate','Contacts','Metal routing']}),
'sc-002':()=>make('mask-layer-map','inspect','mask-map',bi('光罩圖層與元件平面圖','Mask layers and device layout'),bi('觀察三個圖層的疊合。選出連接接觸孔、形成跨元件配線的圖層，並記錄觀察。','Inspect the three overlaid layers. Identify the layer that connects contact openings into inter-device routing.'),bi('圖層檢視器','Layer inspector'),bi('A 為主動區，B 為接觸開口，C 為金屬配線；圖層名稱需與設計資料一致。','A is active area, B contact openings, C metal routing; layer assignments follow design data.'),{choices:[opt('active','A 主動區','A Active'),opt('contact','B 接觸孔','B Contacts'),opt('metal','C 金屬互連','C Metal')],expectedChoice:'metal'}),
'sc-003':()=>make('process-route-branch','process','route',bi('閘極製程的互斥路線','Alternative gate-process routes'),bi('圖中已有犧牲閘極。選擇其後的替換閘極路線，再執行流程檢查；不要把兩條路線串成一條。','A sacrificial gate is present. Select replacement-gate continuation, then run the route check; do not chain both alternatives.'),bi('製程依賴檢查器','Process dependency checker'),bi('Gate-first 與 replacement-gate 是替代架構。圖示只是依賴關係，不是完整製程配方。','Gate-first and replacement-gate are alternatives. The diagram shows dependencies, not a full recipe.'),{choices:[opt('gate-first','直接形成最終閘極','Form final gate first'),opt('replacement','移除犧牲閘極 → 形成替換閘極','Remove dummy gate → replacement gate')],expectedChoice:'replacement'}),
'sc-004':()=>make('substrate-identification','inspect','soi',bi('三層基板樣本','Three-layer substrate specimen'),bi('辨識圖中的薄矽、埋氧與支撐矽三層，選出相符的基板類型。','Identify device silicon, buried oxide and handle silicon; classify the substrate.'),bi('基板剖面判讀器','Substrate cross-section viewer'),bi('SOI 含連續埋氧層；不要把表面原生氧化層誤認為埋氧。','SOI contains a continuous buried oxide; surface native oxide is not a buried oxide.'),{choices:[opt('bulk','體矽','Bulk Si'),opt('soi','絕緣層上矽 SOI','Silicon on insulator'),opt('glass','均質玻璃','Homogeneous glass')],expectedChoice:'soi'}),
'sc-005':()=>make('conductivity-sign','measure','hall',bi('霍爾訊號與載子極性','Hall sign and carrier type'),bi('此示例固定電流與磁場的正方向；讀取標示的霍爾係數符號，再選主要載子。','Current and field directions are fixed in this specimen. Read the Hall coefficient sign and identify the majority carrier.'),bi('極性對照量測器','Polarity measurement bench'),bi('在單一主導載子且符號約定固定的簡化模型中，負霍爾係數對應電子。','With one dominant carrier and a fixed sign convention, a negative Hall coefficient corresponds to electrons.'),{choices:[opt('electron','電子 / n 型','Electrons / n type'),opt('hole','電洞 / p 型','Holes / p type')],expectedChoice:'electron',controls:[ctl('reading','讀到的規一化係數','Measured normalized coefficient',-2,2,.1,0,-1,'a.u.',.05)]}),
'sc-006':()=>make('wafer-diameter','measure','diameter',bi('晶圓兩端點與直徑','Wafer endpoints and diameter'),bi('使用跨越圓心的卡尺讀數，輸入本教學樣本的直徑；不要讀成半徑。','Read caliper endpoints across the center and enter the specimen diameter, not radius.'),bi('直徑卡尺','Diameter caliper'),bi('本示例左右端點相差 300 mm。這是樣本尺寸，非全部晶圓的通用規格。','The example endpoints are 300 mm apart; this is a specimen dimension, not a universal wafer specification.'),{controls:[ctl('reading','直徑','Diameter',100,450,1,150,300,'mm',.5)]}),
'sc-007':()=>make('wafer-ttv','measure','ttv',bi('多點厚度剖面','Multi-point thickness profile'),bi('讀取五點厚度 775、772、778、774、776 µm，輸入最大值減最小值。','Read thicknesses 775, 772, 778, 774, 776 µm and enter max minus min.'),bi('雙面厚度探頭','Opposed thickness probes'),bi('TTV = 778 − 772 = 6 µm；不可由單面高度直接當作總厚度變化。','TTV = 778 − 772 = 6 µm; one-sided surface height alone does not determine thickness variation.'),{controls:[ctl('reading','總厚度變化 TTV','Total thickness variation',0,12,.1,0,6,'µm',.05)],sample:[775,772,778,774,776]}),
'sc-008':()=>make('bow-versus-warp','inspect','warp',bi('中點彎曲與全域翹曲','Center bow and global warp'),bi('比較兩條剖面。選出具有正負偏移、無法僅用中點值描述的翹曲剖面 B。','Compare profiles. Select B, which has positive and negative deviations and cannot be described by center bow alone.'),bi('非接觸形貌比對','Non-contact shape comparator'),bi('Bow 與 warp 使用不同形狀指標；此示意未替代標準規定的支撐與參考面。','Bow and warp describe different metrics; reference planes and support conditions require a specified standard.'),{choices:[opt('a','A 單一平滑弓形','A Smooth bowed profile'),opt('b','B 同時出現高點與低點','B Peaks and valleys')],expectedChoice:'b'}),
'sc-009':()=>make('local-flatness','measure','flatness',bi('曝光場域的局部平坦度','Local field flatness'),bi('以已扣除最佳擬合平面的局部殘差 +0.8 與 −1.0 µm，求峰谷差。','For plane-removed residuals +0.8 and −1.0 µm, compute the peak-to-valley range.'),bi('局部場域平面擬合','Local-field plane fit'),bi('局部殘差 PV = 1.8 µm；全晶圓彎曲量不能直接替代場域平坦度。','Local residual PV = 1.8 µm; global bow does not replace field flatness.'),{controls:[ctl('reading','局部殘差 PV','Local residual PV',0,4,.1,0,1.8,'µm',.05)]}),
'sc-010':()=>make('notch-orientation','inspect','notch',bi('定位缺口與晶向紀錄','Notch and orientation record'),bi('找出缺口，並選擇由證書核對晶向的流程；缺口圖形本身不能保證晶向。','Locate the notch and choose certificate-based orientation verification; the notch picture alone is insufficient.'),bi('缺口定位與批次紀錄','Notch locator and lot record'),bi('幾何定位、晶面／晶向與供應商證書必須共同核對。','Geometric indexing, crystal orientation and supplier documentation must agree.'),{choices:[opt('shape','只憑缺口形狀決定晶向','Infer orientation from notch shape only'),opt('certificate','缺口定位 + 證書晶向核對','Locate notch + verify certified orientation')],expectedChoice:'certificate'}),
'sc-011':()=>make('edge-profile','inspect','edge',bi('晶圓倒角與缺角','Wafer bevel and edge chip'),bi('比較完整倒角與局部缺口。選出需要隔離複判的樣本 B。','Compare the intact bevel and local chip; identify specimen B for hold and review.'),bi('邊緣剖面檢查','Edge cross-section inspection'),bi('缺角可能成為裂紋起始點；示圖不提供產品放行尺寸界限。','An edge chip can initiate cracking; no production acceptance threshold is implied.'),{choices:[opt('a','A 連續倒角','A Continuous bevel'),opt('b','B 局部缺角','B Local edge chip')],expectedChoice:'b'}),
'sc-012':()=>make('particle-wafer-map','inspect','particle-map',bi('來料粒子座標圖','Incoming particle coordinate map'),bi('找出圖中右上方集中出現的粒子群，保留其空間分布證據。','Locate the upper-right particle cluster and preserve its spatial pattern.'),bi('晶圓缺陷座標檢视','Wafer defect-map inspector'),bi('聚集、邊緣與隨機分布有不同追查方向；點數本身不揭露污染來源。','Cluster, edge and random patterns suggest different investigations; count alone does not establish a source.'),{choices:[opt('upper-right','右上方群聚','Upper-right cluster'),opt('center','中心均勻分布','Uniform center'),opt('edge','整圈邊緣','Complete edge ring')],expectedChoice:'upper-right'}),
'sc-013':()=>make('scratch-particle-classification','inspect','scratch',bi('長條刮傷與離散粒子','Scratch versus discrete particles'),bi('比較長條連續缺陷 A 與孤立亮點 B；選出較符合刮傷形貌的 A。','Compare continuous elongated feature A with isolated spots B; identify the scratch-like morphology.'),bi('形貌分類顯微鏡','Morphology classifier'),bi('這只是形貌分類；還需複查對焦、影像與量測證據，不能由單張圖直接斷定原因。','This is a morphology classification, not a root-cause diagnosis.'),{choices:[opt('a','A 連續線形缺陷','A Continuous linear defect'),opt('b','B 離散點狀缺陷','B Isolated spots')],expectedChoice:'a'}),
'sc-014':()=>make('surface-rms','measure','roughness',bi('去除平均值的表面高度','Mean-removed surface heights'),bi('四點殘差為 +0.6、−0.6、+0.6、−0.6 nm。計算 RMS，不要用峰谷值代替。','Residuals are +0.6, −0.6, +0.6, −0.6 nm. Compute RMS, not peak-to-valley.'),bi('表面輪廓量測','Surface profiler'),bi('Rq = √mean(z²) = 0.6 nm；此四點樣本不代表實際 AFM 掃描完整統計。','Rq = √mean(z²) = 0.6 nm; four points do not replace a real AFM scan.'),{controls:[ctl('reading','Rq','Rq',0,2,.1,1.2,.6,'nm',.05)]}),
'sc-015':()=>make('oxide-model-fit','measure','spectrum',bi('氧化層模型與量測匹配','Oxide model and measurement fit'),bi('調整膜厚，使簡化量測標記與模型曲線匹配。樣本最佳匹配位於 2.0 nm。','Adjust thickness to match the synthetic model curve to observed markers; this specimen matches at 2.0 nm.'),bi('薄膜模型擬合器','Thin-film model fitter'),bi('擬合依賴折射率模型、基板與波長範圍；圖中曲線不是商用橢偏儀校正資料。','A fit depends on optical constants, substrate and wavelength range; this is not calibrated ellipsometry data.'),{controls:[ctl('reading','模型膜厚','Model thickness',.5,5,.1,1,2,'nm',.05)]}),
'sc-016':()=>make('surface-metals','inspect','contamination',bi('痕量金屬與空白樣本','Trace metals and analytical blank'),bi('比較樣本與空白的相對訊號；選出超過空白且需複判的 Fe 通道。','Compare sample and blank signals; identify the Fe channel elevated above the blank.'),bi('污染訊號對照表','Contamination-signal comparator'),bi('相對訊號不能未經校正便寫成面密度；需檢查空白、檢出限與回收率。','Relative signal is not surface concentration without calibration, blank and detection-limit checks.'),{choices:[opt('fe','Fe 訊號','Fe signal'),opt('cu','Cu 訊號','Cu signal'),opt('blank','空白即樣本濃度','Blank equals concentration')],expectedChoice:'fe'}),
'sc-017':()=>make('resistivity-map','measure','resistivity',bi('電阻率徑向分布','Radial resistivity distribution'),bi('樣本最小值 9.5、最大值 10.5 Ω·cm；以平均值 10 為分母求全幅百分比。','Specimen minimum 9.5, maximum 10.5 Ω·cm; calculate full-range percentage using mean 10.'),bi('四點探針地圖讀值','Four-point-probe map reader'),bi('(10.5−9.5)/10 ×100%=10%。需明示均勻度定義與厚度／邊界修正。','(10.5−9.5)/10 ×100%=10%; state the metric and thickness/edge corrections.'),{controls:[ctl('reading','相對全幅','Relative full range',0,30,1,0,10,'%',.1)]}),
'sc-018':()=>make('epitaxy-thickness','measure','epi',bi('磊晶層與基板界面','Epitaxial layer and substrate'),bi('由示例剖面標尺讀取兩條界面之間的 5 µm 厚度。','Read 5 µm between the indicated specimen interfaces.'),bi('界面厚度標尺','Interface thickness scale'),bi('磊晶厚度、摻雜分布與缺陷是不同驗證項目，不因厚度正確而全部通過。','Thickness, doping profile and defects are separate qualification items.'),{controls:[ctl('reading','磊晶厚度','Epitaxial thickness',0,12,.5,0,5,'µm',.1)]}),
'sc-019':()=>make('buried-oxide-identification','inspect','soi',bi('SOI 埋氧層辨識','SOI buried oxide identification'),bi('選出裝置矽與支撐矽之間的 B 層；它是埋氧層。','Identify layer B between device and handle silicon as buried oxide.'),bi('多材料剖面辨識','Multimaterial cross-section inspector'),bi('埋氧提供電性隔離，亦改變散熱路徑；圖中比例為教學放大。','Buried oxide provides isolation and changes the heat path; proportions are exaggerated.'),{choices:[opt('a','A 裝置矽','A Device silicon'),opt('b','B 埋氧 BOX','B Buried oxide'),opt('c','C 支撐矽','C Handle silicon')],expectedChoice:'b'}),
'sc-020':()=>make('crystal-defect-classification','inspect','crystal-defect',bi('晶格終止與位錯示意','Lattice termination and dislocation'),bi('找到多出半平面在晶格中終止的位置，選擇位錯類型。','Locate the terminating extra half-plane and classify the dislocation schematic.'),bi('晶格缺陷示意檢查','Crystal-defect viewer'),bi('示意的半平面終止對應刃位錯；真實缺陷需適當顯微與繞射分析。','The terminating half-plane depicts an edge dislocation; real defects require appropriate microscopy/diffraction.'),{choices:[opt('dislocation','刃位錯','Edge dislocation'),opt('particle','表面粒子','Surface particle'),opt('oxide','均勻氧化層','Uniform oxide')],expectedChoice:'dislocation'}),
'sc-021':()=>make('clean-handling-contact','assembly','handling',bi('背面支撐與前面禁觸區','Backside support and front-side keep-clear zone'),bi('把支撐放到晶圓背面接觸區，並選擇不接觸有效正面的搬運方式。','Align the support beneath the wafer and select handling that avoids the active front surface.'),bi('潔淨接觸配置','Clean-contact fixture'),bi('背面或邊緣接觸仍須符合載具與潔淨要求；不是裸手搬運指引。','Backside/edge handling still requires validated tooling and cleanliness; this is not bare-hand handling guidance.'),{choices:[opt('front','接觸元件正面','Contact active front side'),opt('back','使用合規背面／邊緣支撐','Use validated backside/edge support')],expectedChoice:'back'}),
'sc-022':()=>make('foup-slot-map','inspect','foup',bi('載具槽位與批次紀錄','Carrier slots and lot record'),bi('比較記錄與光學槽位讀取：本示例第 4 槽記錄有片、實測空槽。','Compare record and optical slot reading: slot 4 is recorded occupied but detected empty.'),bi('槽位核對器','Slot-map reconciler'),bi('需先解決缺片／雙片／跨槽與批次身分差異，再交接；圖示只有 6 槽教學載具。','Resolve slot and identity discrepancies before handoff; this is a six-slot teaching carrier.'),{choices:[opt('2','第 2 槽','Slot 2'),opt('4','第 4 槽','Slot 4'),opt('6','第 6 槽','Slot 6')],expectedChoice:'4'}),
'sc-023':()=>make('measurement-repeatability','measure','repeatability',bi('重複量測數列','Repeated readings'),bi('同一位置讀到 100.0、100.2、100.4。輸入平均值及全幅；全幅不是標準差。','At one site, readings are 100.0, 100.2, 100.4. Enter mean and full range; range is not standard deviation.'),bi('重複性統計工作台','Repeatability bench'),bi('平均 100.2、全幅 0.4。三點只供計算教學，不足以完成 GR&R。','Mean 100.2 and range 0.4; three points do not constitute a full GR&R study.'),{controls:[ctl('mean','平均值','Mean',99,102,.1,99,100.2,'a.u.',.05),ctl('range','全幅','Range',0,2,.1,0,.4,'a.u.',.05)]}),
'sc-024':()=>make('baseline-registration','process','registration',bi('前後測座標對位','Before/after coordinate registration'),bi('後測圖相對基準向右 3、向下 2 個示意單位。套用 −3、−2 的平移修正，再執行對位。','The after-map is displaced +3 horizontally and +2 vertically. Apply corrections −3 and −2, then register.'),bi('基準標記配準','Fiducial registration'),bi('此處只示範平移；實際配準還可能需要旋轉、縮放與畸變模型。','Only translation is modeled; real registration may require rotation, scale and distortion.'),{controls:[ctl('dx','水平修正','Horizontal correction',-6,6,1,0,-3,'a.u.',0),ctl('dy','垂直修正','Vertical correction',-6,6,1,0,-2,'a.u.',0)]}),
'sc-025':()=>make('monitor-wafer-allocation','process','monitor',bi('監控片與產品片分流','Monitor and product wafer allocation'),bi('選擇獨立監控片＋產品抽樣策略，將材料／設備趨勢與產品量測分開記錄。','Select separate monitor wafers plus product sampling, with separate trend and product records.'),bi('抽樣路線配置','Sampling-route planner'),bi('監控片與產品片不能未經相關性驗證就互相替代；本例不指定量產抽樣數。','Monitor and product data are not interchangeable without correlation; no production sample count is prescribed.'),{choices:[opt('mixed','全部合併成一個無標籤批次','Merge into one unlabeled batch'),opt('separate','監控片與產品抽樣分開標示','Label monitor and product samples separately')],expectedChoice:'separate'}),
'sc-026':()=>make('incoming-disposition','inspect','disposition',bi('來料證據與放行矩陣','Incoming evidence and disposition matrix'),bi('圖中身分與尺寸通過，但污染複判未完成。選擇暫停放行並保留待辦證據。','Identity and dimensions pass, but contamination review is incomplete. Hold the lot pending evidence.'),bi('批次證據審查','Lot-evidence review'),bi('未知項不能自動當成通過；放行須依批准規格與授權流程。','Unknown is not pass; release requires approved specifications and authorization.'),{choices:[opt('release','直接放行','Release now'),opt('hold','隔離／待複判','Hold for review'),opt('hide','刪除未完成紀錄','Delete incomplete record')],expectedChoice:'hold'})
};

const families={
 integration:{scene:'interface',name:bi('系統依賴與證據','System dependencies and evidence'),tool:bi('路線／界面審查','Route and interface review'),metric:bi('已驗證界面','Verified interfaces'),unit:' / 4',initial:0,target:4,max:4,phase:bi('需求 → 模組 → 界面 → 驗證','Requirements → modules → interfaces → verification')},
 growth:{scene:'growth',name:bi('籽晶、熔體與晶棒','Seed, melt and crystal'),tool:bi('晶體成長階段模型','Crystal-growth phase model'),metric:bi('相對截面均勻度','Relative section uniformity'),unit:'%',initial:70,target:90,max:100,phase:bi('籽晶 → 縮頸 → 晶肩 → 等徑段','Seed → neck → shoulder → constant diameter')},
 cleaning:{scene:'cleaning',name:bi('表面污染與清洗前後','Surface contamination before/after'),tool:bi('污染分類與比較器','Contamination classifier'),metric:bi('示例粒子移除率','Example particle removal'),unit:'%',initial:20,target:80,max:100,phase:bi('基準 → 分類 → 示意移除 → 複查','Baseline → classify → conceptual removal → recheck')},
 trench:{scene:'trench',name:bi('溝槽、襯層與填充','Trench, liner and fill'),tool:bi('溝槽剖面工作台','Trench cross-section bench'),metric:bi('剖面深寬比','Section aspect ratio'),unit:'a.u.',initial:1,target:3,max:6,phase:bi('遮罩 → 溝槽 → 襯層 → 填充','Mask → trench → liner → fill')},
 implantation:{scene:'implantation',name:bi('離子入射與深度分布','Ion incidence and depth profile'),tool:bi('規一化深度分布模型','Normalized depth-profile model'),metric:bi('規一化峰值位置','Normalized peak position'),unit:'a.u.',initial:.2,target:.6,max:1,phase:bi('遮罩 → 入射 → 損傷示意 → 活化比較','Mask → incidence → damage schematic → activation comparison')},
 oxide:{scene:'oxide',name:bi('矽與氧化／介電界面','Silicon and dielectric interface'),tool:bi('介電層剖面檢查','Dielectric-interface viewer'),metric:bi('相對膜厚','Relative film thickness'),unit:'a.u.',initial:.3,target:.8,max:1.5,phase:bi('表面 → 界面 → 介電層 → 缺陷檢查','Surface → interface → dielectric → defect check')},
 deposition:{scene:'deposition',name:bi('薄膜與高低差表面','Film on stepped topography'),tool:bi('共形性對照模型','Conformality comparison'),metric:bi('側壁／頂面厚度比','Sidewall/top thickness ratio'),unit:'ratio',initial:.3,target:.8,max:1,phase:bi('基板 → 表面作用 → 覆蓋 → 剖面比較','Substrate → surface reaction → coverage → section comparison')},
 lithography:{scene:'lithography',name:bi('光罩、曝光與光阻圖案','Mask, exposure and resist pattern'),tool:bi('圖案轉移光學工作台','Pattern-transfer optics bench'),metric:bi('規一化圖案誤差','Normalized pattern error'),unit:'a.u.',initial:.8,target:.2,max:1,phase:bi('塗阻 → 光罩／曝光 → 顯影 → 比對','Coat → mask/exposure → develop → compare')},
 etch:{scene:'etch',name:bi('遮罩、開口與蝕刻輪廓','Mask, opening and etched profile'),tool:bi('選擇比與輪廓示意','Selectivity/profile demonstrator'),metric:bi('目標／遮罩移除量比','Target/mask removal ratio'),unit:'ratio',initial:1,target:4,max:8,phase:bi('遮罩 → 選擇性移除 → 剖面 → 殘留檢查','Mask → selective removal → profile → residue check')},
 gate:{scene:'gate',name:bi('通道、閘極與間隙壁','Channel, gate and spacers'),tool:bi('閘極整合剖面圖','Gate-integration section'),metric:bi('左右間隙壁厚度差','Left/right spacer difference'),unit:'a.u.',initial:4,target:1,max:6,phase:bi('通道 → 閘極 → 間隙壁 → 接面界面','Channel → gate → spacers → junction interface')},
 contact:{scene:'contact',name:bi('接觸開口與導電填充','Contact opening and conductor fill'),tool:bi('接點連續性剖面','Contact continuity section'),metric:bi('示例串聯電阻','Example series resistance'),unit:'a.u.',initial:6,target:3,max:8,phase:bi('介電開口 → 界面 → 阻障 → 導電填充','Opening → interface → barrier → conductor fill')},
 cmp:{scene:'cmp',name:bi('研磨前後與停止面','Before/after planarization and stop plane'),tool:bi('平坦化剖面比較','Planarization section comparator'),metric:bi('研磨後峰谷差','Post-polish peak-to-valley'),unit:'a.u.',initial:6,target:2,max:10,phase:bi('凸起 → 接觸 → 去除 → 凹陷複查','Topography → contact → removal → dishing review')},
 interconnect:{scene:'interconnect',name:bi('多層金屬、通孔與網路','Metal levels, vias and nets'),tool:bi('配線連續性檢視','Routing-continuity viewer'),metric:bi('已驗證連通支路','Verified connected branches'),unit:' / 4',initial:0,target:4,max:4,phase:bi('線槽 → 通孔 → 填充 → 網路比對','Trenches → vias → fill → net comparison')},
 thinning:{scene:'thinning',name:bi('載板支撐與背面薄化','Carrier support and backside thinning'),tool:bi('薄化與支撐剖面','Thinning/support section'),metric:bi('規一化剩餘厚度','Normalized remaining thickness'),unit:'ratio',initial:.9,target:.4,max:1,phase:bi('保護 → 支撐 → 背面去除 → 應力複查','Protect → support → backside removal → stress review')},
 metrology:{scene:'repeatability',name:bi('量測鏈與重複性','Measurement chain and repeatability'),tool:bi('基準與量測數列','Reference and repeated readings'),metric:bi('三次讀值的平均','Mean of three readings'),unit:'a.u.',initial:99,target:100.2,max:102,min:99,phase:bi('參考 → 量測 → 重複 → 偏差／變異','Reference → measure → repeat → bias/variation')},
 electrical:{scene:'electrical',name:bi('電源、元件與量測路徑','Power, device and measurement path'),tool:bi('規一化電性測試','Normalized electrical test'),metric:bi('兩個串聯元件的總值 1+2','Series total for elements 1+2'),unit:'a.u.',initial:0,target:3,max:6,phase:bi('界面 → 激勵 → 量測 → 斷言','Interface → stimulus → measurement → assertion')},
 statistics:{scene:'quality-chart',name:bi('良率、分群與證據','Yield, grouping and evidence'),tool:bi('示例資料統計工作台','Illustrative statistics bench'),metric:bi('80 件中 60 件通過的比例','Pass fraction: 60 out of 80'),unit:'%',initial:0,target:75,max:100,phase:bi('分母 → 去重 → 分群 → 結論','Denominator → deduplicate → group → conclusion')},
 nanosheet:{scene:'nanosheet',name:bi('堆疊通道與環繞閘極','Stacked channels and surrounding gate'),tool:bi('奈米片元件示意','Nanosheet device schematic'),metric:bi('圖中分離通道層数','Distinct channels shown'),unit:'layers',initial:1,target:3,max:5,phase:bi('異質層 → 選擇性釋放 → 閘介電 → 環繞閘極','Heterolayers → selective release → dielectric → surrounding gate')},
 wafermap:{scene:'particle-map',name:bi('晶圓地圖與位置追蹤','Wafer map and location tracking'),tool:bi('座標分群檢視','Coordinate-cluster viewer'),metric:bi('標示區域內的缺陷數','Defects in highlighted region'),unit:'count',initial:0,target:5,max:10,phase:bi('身分 → 座標 → 分群 → 複核','Identity → coordinates → group → review')},
 dicing:{scene:'dicing',name:bi('切割道、晶粒與膠膜','Streets, dies and support tape'),tool:bi('分割路線示意','Singulation-route viewer'),metric:bi('示例完整晶粒數','Intact dies in specimen'),unit:'count',initial:0,target:6,max:9,phase:bi('街道確認 → 支撐 → 分割示意 → 邊緣檢查','Street check → support → singulation schematic → edge check')},
 dieattach:{scene:'dieattach',name:bi('晶粒、黏著層與載體','Die, attachment layer and carrier'),tool:bi('晶粒貼裝剖面','Die-attachment section'),metric:bi('覆蓋區域比例','Covered area fraction'),unit:'%',initial:30,target:80,max:100,phase:bi('載體 → 接合層 → 晶粒 → 空洞複查','Carrier → attachment → die → void review')},
 wirebond:{scene:'wirebond',name:bi('焊墊、線弧與第二焊點','Pad, wire loop and second bond'),tool:bi('線弧與接點檢查','Wire-loop and bond inspection'),metric:bi('圖中連續線弧','Continuous wire loops shown'),unit:'count',initial:0,target:3,max:4,phase:bi('第一焊点 → 線弧 → 第二焊点 → 界面檢查','First bond → loop → second bond → interface check')},
 bump:{scene:'bump',name:bi('焊墊、UBM 與凸塊','Pad, UBM and bump'),tool:bi('凸塊陣列剖面','Bump-array section'),metric:bi('完好示例凸塊','Intact specimen bumps'),unit:'count',initial:0,target:4,max:6,phase:bi('焊墊 → UBM → 凸塊 → 接點檢查','Pad → UBM → bump → joint inspection')},
 fanout:{scene:'fanout',name:bi('重組晶粒與扇出配線','Reconstituted dies and fan-out routing'),tool:bi('重組位移對照','Reconstitution shift comparator'),metric:bi('需要補償的平移量','Translation to compensate'),unit:'a.u.',initial:0,target:3,max:6,phase:bi('載板 → 重組晶粒 → 塑封 → 扇出配線','Carrier → reconstituted dies → mold → fan-out routing')},
 molding:{scene:'molding',name:bi('模封、晶粒與材料界面','Mold, die and material interfaces'),tool:bi('模封填充與空洞檢查','Mold-fill and void inspection'),metric:bi('示意填充比例','Schematic filled fraction'),unit:'%',initial:20,target:90,max:100,phase:bi('預備 → 示意流動 → 包覆 → 空洞／翹曲檢查','Prepare → schematic flow → encapsulate → void/warp review')},
 rdl:{scene:'rdl',name:bi('介電層與重布線','Dielectric and redistribution layer'),tool:bi('RDL 圖層對位','RDL layer alignment'),metric:bi('可見連通路徑','Visible connected routes'),unit:'count',initial:0,target:3,max:5,phase:bi('介電 → 開口 → 金屬 → 連通檢查','Dielectric → openings → metal → connectivity')},
 tsv:{scene:'tsv',name:bi('穿矽孔、襯層與填充','Through-silicon via, liner and fill'),tool:bi('TSV 多材料剖面','TSV multimaterial section'),metric:bi('示例深寬比 6/2','Example aspect ratio 6/2'),unit:'ratio',initial:0,target:3,max:6,phase:bi('孔洞 → 絕緣襯層 → 阻障 → 金屬填充','Via → isolation liner → barrier → metal fill')},
 interposer:{scene:'interposer',name:bi('異質晶粒與中介層','Heterogeneous dies and interposer'),tool:bi('2.5D 層間界面','2.5D interface viewer'),metric:bi('主要晶粒模組數','Main die modules shown'),unit:'count',initial:0,target:3,max:5,phase:bi('中介層 → 互連 → 晶粒 → 系統界面','Interposer → interconnects → dies → system interfaces')},
 substrate:{scene:'substrate',name:bi('核心板與增層介電／金屬','Core and dielectric/metal build-up'),tool:bi('封裝基板剖面','Package-substrate section'),metric:bi('圖中金屬層數','Metal layers shown'),unit:'layers',initial:0,target:4,max:6,phase:bi('核心 → 介電增層 → 導通孔 → 配線','Core → dielectric build-up → vias → routing')},
 hybrid:{scene:'hybrid',name:bi('介電與銅的混合接合界面','Dielectric and copper hybrid interface'),tool:bi('雙表面對位比較','Dual-surface alignment comparison'),metric:bi('示例對位殘差','Example overlay residual'),unit:'a.u.',initial:4,target:0,max:6,phase:bi('表面 → 對準 → 接合示意 → 連通檢查','Surfaces → align → bonding schematic → continuity')},
 hbm:{scene:'hbm',name:bi('記憶體堆疊與底層晶粒','Memory stack and base die'),tool:bi('堆疊層次檢視','Stack-level inspection'),metric:bi('示意記憶體層數','Memory levels shown'),unit:'layers',initial:0,target:4,max:6,phase:bi('底層晶粒 → 分層 → 互連 → 熱路徑','Base die → levels → interconnect → heat path')},
 underfill:{scene:'underfill',name:bi('晶粒間隙、填膠與熱路徑','Die gap, underfill and heat path'),tool:bi('間隙填充剖面','Gap-fill cross-section'),metric:bi('示意流動前緣比例','Schematic flow-front fraction'),unit:'%',initial:20,target:80,max:100,phase:bi('間隙 → 前緣 → 填充 → 空洞複查','Gap → front → filling → void inspection')},
 thermal:{scene:'thermal',name:bi('熱源、熱阻與環境','Heat source, resistance and ambient'),tool:bi('規一化熱阻網路','Normalized thermal network'),metric:bi('R=2 與 Q=3 的溫差乘積','Temperature-rise product: R=2, Q=3'),unit:'a.u.',initial:0,target:6,max:10,phase:bi('熱源 → 接觸 → 散熱路 → 邊界條件','Source → contacts → heat path → boundary conditions')},
 optics:{scene:'optics',name:bi('光束、光學介面與像面','Beam, optical interfaces and image plane'),tool:bi('光路與焦點比較','Optical-path and focus comparator'),metric:bi('規一化焦平面偏移','Normalized focal-plane offset'),unit:'a.u.',initial:3,target:0,max:5,phase:bi('來源 → 光學作用 → 光程 → 像面','Source → optical interaction → path → image plane')},
 reflective:{scene:'reflective',name:bi('反射式極紫外光路','Reflective EUV optical path'),tool:bi('反射鏡光路追蹤','Reflective-path tracer'),metric:bi('示意反射界面數','Reflective interfaces shown'),unit:'count',initial:0,target:3,max:5,phase:bi('來源 → 多層反射鏡 → 光罩 → 像面','Source → multilayer mirrors → reticle → image plane')},
 photonics:{scene:'photonics',name:bi('波導、環與耦合介面','Waveguide, ring and coupling interface'),tool:bi('積體光路示意','Integrated optical-circuit viewer'),metric:bi('串接損耗 1+2 的總和','Sum of sequential losses 1+2'),unit:'dB (example)',initial:0,target:3,max:6,phase:bi('導波 → 耦合 → 調制／偵測 → 鏈路','Guiding → coupling → modulation/detection → link')},
 aircraft:{scene:'aircraft',name:bi('公開航空結構與界面','Public aircraft structure and interfaces'),tool:bi('結構載荷路徑辨識','Structural load-path inspection'),metric:bi('已列出的證據類別','Evidence categories documented'),unit:' / 4',initial:0,target:4,max:4,phase:bi('功能 → 結構 → 界面 → 民用原理驗證','Function → structure → interfaces → civilian principle review')},
 rotor:{scene:'rotor',name:bi('旋翼、機身與振動概念','Rotor, fuselage and vibration concepts'),tool:bi('旋轉機械原理檢視','Rotating-machinery principle viewer'),metric:bi('示意振動峰數','Illustrative vibration peaks'),unit:'count',initial:0,target:2,max:4,phase:bi('能量 → 旋轉 → 量測 → 原理驗證','Energy → rotation → measurement → principle review')},
 buoyancy:{scene:'buoyancy',name:bi('民用浮體與浮力原理','Civilian body and buoyancy principles'),tool:bi('力的方向對照','Force-direction comparison'),metric:bi('規一化浮力與重量差','Normalized buoyancy minus weight'),unit:'a.u.',initial:3,target:0,max:5,phase:bi('排水 → 浮力 → 重心／浮心 → 平衡','Displacement → buoyancy → centers → balance')},
 bridge:{scene:'bridge',name:bi('橋塔、斜索與橋面載荷路徑','Pylon, stays and deck load paths'),tool:bi('概念載荷路徑模型','Conceptual load-path model'),metric:bi('示意檢查點數','Illustrative inspection points'),unit:'count',initial:0,target:4,max:6,phase:bi('地盤 → 基礎 → 塔／梁 → 監測','Ground → foundation → pylon/deck → monitoring')},
 tunnel:{scene:'tunnel',name:bi('地層、開挖面與支撐','Ground, excavation face and support'),tool:bi('隧道剖面風險模型','Tunnel-section risk viewer'),metric:bi('示例兩側位移總和 2+3','Example convergence from 2+3'),unit:'a.u.',initial:0,target:5,max:8,phase:bi('地質 → 面穩定 → 支撐 → 監測','Geology → face stability → support → monitoring')},
 network:{scene:'network',name:bi('信任區、身分與資料流','Trust zones, identity and data flows'),tool:bi('防禦架構與權限檢查','Defensive architecture/access review'),metric:bi('需要驗證的授權邊界','Authorization boundaries to verify'),unit:'count',initial:0,target:3,max:5,phase:bi('資產 → 身分 → 最小權限 → 驗證','Assets → identity → least privilege → verification')},
 piston:{scene:'piston',name:bi('汽缸、連桿與曲柄','Cylinder, rod and crank'),tool:bi('運動學示意模型','Kinematic demonstrator'),metric:bi('規一化曲柄半徑 1 的行程','Stroke for normalized crank radius 1'),unit:'a.u.',initial:0,target:2,max:4,phase:bi('能量 → 活塞 → 連桿 → 輪軸','Energy → piston → rod → wheel axle')},
 vehicle:{scene:'vehicle',name:bi('車體、懸吊與能量系統','Body, suspension and energy systems'),tool:bi('民用車輛系統界面','Civilian vehicle interface model'),metric:bi('已定義的功能介面','Defined functional interfaces'),unit:' / 4',initial:0,target:4,max:4,phase:bi('車體 → 底盤 → 動力／熱路 → 驗證','Body → chassis → power/heat paths → verification')},
 battery:{scene:'battery',name:bi('電池、BMS 與低壓模型','Battery, BMS and low-voltage model'),tool:bi('非帶電電池架構示意','De-energized battery architecture viewer'),metric:bi('三個相同單元的規一化串聯值','Normalized series sum of three equal cells'),unit:'a.u.',initial:0,target:3,max:5,phase:bi('單元 → 監测 → 隔離 → 系統驗證','Cells → monitoring → isolation → system review')},
 satellite:{scene:'satellite',name:bi('衛星平台、鏈路與地面站','Satellite bus, link and ground station'),tool:bi('公開通訊系統概念模型','Public communication-system model'),metric:bi('鏈路圖中節點數','Nodes in the link diagram'),unit:'count',initial:0,target:3,max:5,phase:bi('平台 → 供電／熱控 → 鏈路 → 地面介面','Bus → power/thermal → link → ground interface')},
 dam:{scene:'dam',name:bi('重力壩、基礎與水力轉換','Gravity dam, foundation and hydropower'),tool:bi('民用水工原理檢視','Civil hydraulic principles viewer'),metric:bi('規一化輸入 4、效率 0.75 的輸出','Output for normalized input 4 and efficiency .75'),unit:'a.u.',initial:0,target:3,max:5,phase:bi('流域 → 地基／壩體 → 水路 → 監測','Basin → foundation/dam → waterway → monitoring')},
 rail:{scene:'rail',name:bi('車體、轉向架與功能界面','Body, bogie and functional interfaces'),tool:bi('民用軌道系統原理','Civil rail-system principles'),metric:bi('需相互驗證的功能群','Functional groups requiring integration'),unit:' / 4',initial:0,target:4,max:4,phase:bi('車體 → 走行 → 牽引／煞車 → 功能驗證','Body → running gear → traction/braking → functional review')},
};
// Additional stage-specific public engineering contexts. No product-specific CAD.
const contextFamilies={
 materials:['材料結構與品質','Material structure and quality','materials'],
 maintenance:['維護可達性與檢查證據','Maintenance access and inspection evidence','inspection-plan'],
 vibration:['振動峰、量測與共振','Vibration peaks, sensing and resonance','vibration'],
 powertrain:['能量、齒輪與傳動界面','Energy, gears and drivetrain interfaces','powertrain'],
 safety:['危害、隔離與驗證','Hazards, isolation and verification','safety'],
 pressure:['外部壓力與受力方向','External pressure and force directions','pressure'],
 site:['場址、地形與環境需求','Site, terrain and environmental needs','site'],
 ground:['地層、地下水與支撐','Ground layers, groundwater and support','geology'],
 groundwater:['滲流與水壓概念','Seepage and pore-pressure concepts','groundwater'],
 corrosion:['防護層與腐蝕路徑','Protective layers and corrosion paths','corrosion'],
 ventilation:['空氣流路與量測點','Airflow paths and sensing points','ventilation'],
 assets:['受管理資產與資料流','Managed assets and data flows','asset-map'],
 identity:['使用者、因素與授權','Users, factors and authorization','identity'],
 software:['軟體版本、驗證與回復','Software versions, validation and recovery','software'],
 monitoring:['事件、時間序列與複判','Events, time series and review','monitoring'],
 backup:['備份、隔離與還原驗證','Backup, isolation and restore verification','backup'],
 boiler:['熱交換、相變與能量守恆','Heat exchange, phase change and energy balance','boiler'],
 braking:['動能、摩擦與回收路徑','Kinetic energy, friction and recovery','braking'],
 suspension:['彈簧、阻尼與載荷路徑','Springs, dampers and load paths','suspension'],
 finish:['表面形貌、塗層與外觀檢查','Surface topography, coating and appearance','roughness'],
 orbit:['軌道幾何、覆蓋與地面站','Orbit geometry, coverage and ground stations','orbit'],
 antenna:['陣列相位與方向圖','Array phase and radiation pattern','antenna'],
 hydrology:['流域、流入與蓄水收支','Catchment, inflow and storage balance','hydrology'],
 turbine:['水力、轉軸與發電界面','Hydraulic, shaft and generator interfaces','turbine'],
 lock:['船閘水位與航行界面','Lock water levels and navigation interfaces','lock'],
 doors:['車門狀態與功能互鎖','Door state and functional interlocks','doors'],
 coupling:['模態形狀與光學耦合','Mode shapes and optical coupling','coupling'],
 resonator:['環形共振器與量測頻譜','Ring resonator and measured spectrum','resonator'],
 backside:['正面訊號與背面供電','Front-side signals and backside power','backside-power']
};
for(const [id,[zh,en,scene]]of Object.entries(contextFamilies))families[id]={scene,name:bi(zh,en),tool:bi('界面與證據的示意檢視','Schematic interface/evidence viewer'),metric:bi('圖中標示的示例檢查點','Illustrative checks indicated in the diagram'),unit:' / 4',initial:0,target:4,max:4,phase:bi('輸入 → 界面 → 狀態 → 驗證','Input → interface → state → verification')};
const courseStageFamilies={
 sub2nm:['integration','nanosheet','gate','backside','metrology','statistics'],
 asml:['optics','reflective','optics','reflective','lithography','metrology','thermal','statistics'],
 idf:['integration','aircraft','materials','electrical','safety','maintenance'],
 apache:['rotor','rotor','powertrain','vibration','safety','integration'],
 submarine:['buoyancy','buoyancy','pressure','thermal','safety','integration'],
 danjiang:['site','ground','bridge','bridge','corrosion','maintenance'],
 hsuehshan:['ground','groundwater','tunnel','tunnel','ventilation','integration'],
 cybersecurity:['assets','identity','network','software','monitoring','backup'],
 'silicon-photonics':['integration','photonics','coupling','resonator','lithography','thermal','hybrid','electrical'],
 'steam-locomotive':['thermal','boiler','piston','rail','braking','integration'],
 ferrari:['integration','materials','powertrain','suspension','finish','electrical'],
 tesla:['electrical','battery','powertrain','thermal','software','safety'],
 starlink:['orbit','satellite','antenna','network','statistics','orbit'],
 'three-gorges':['hydrology','dam','materials','turbine','lock','maintenance'],
 metro:['integration','rail','powertrain','doors','network','maintenance']
};
Object.assign(families,EXPANSION_CONTEXT_FAMILIES,V7_CONTEXT_FAMILIES);
Object.assign(courseStageFamilies,EXPANSION_STAGE_FAMILIES,V7_STAGE_FAMILIES);
const semiconductorModules=['integration','growth','trench','implantation','oxide','deposition','lithography','lithography','etch','gate','implantation','contact','cmp','interconnect','interconnect','thinning','metrology','electrical','statistics','nanosheet'];
const packageModules=['integration','wafermap','thinning','dicing','dieattach','wirebond','bump','fanout','molding','rdl','tsv','tsv','interposer','substrate','hybrid','hbm','underfill','bump','statistics','electrical'];
const courseFamilies={'sub2nm':'nanosheet',asml:'optics',idf:'aircraft',apache:'rotor',submarine:'buoyancy',danjiang:'bridge',hsuehshan:'tunnel',cybersecurity:'network','silicon-photonics':'photonics','steam-locomotive':'piston',ferrari:'vehicle',tesla:'battery',starlink:'satellite','three-gorges':'dam',metro:'rail'};
Object.assign(courseFamilies,Object.fromEntries(Object.entries(EXPANSION_STAGE_FAMILIES).map(([id,list])=>[id,list[0]])));
const categoryFamilies={semiconductor:'growth',packaging:'interposer',electronics:'electrical',computing:'network',instruments:'metrology',structures:'site',underground:'ground',water:'hydrology',rail:'rail',environment:'resourcenetwork',aerospace:'aircraft',marine:'buoyancy',automotive:'vehicle',space:'satellite',manufacturing:'materials',energy:'thermal',materials:'materials',biomedical:'ctphantom',process:'reduction',megascience:'beamring'};
function familyFor(course,step){
 const text=`${step.titleEn||''} ${step.title||''}`.toLowerCase();
 const id=course.id||(/^(sc)-/.test(step.id||'')?'semiconductor':/^pk-/.test(step.id||'')?'packaging':'');
 if(!['semiconductor','packaging'].includes(id)){
  if(id==='asml'&&/euv|reflect|multilayer|極紫外|反射/.test(text+' '+(step.stage?.titleEn||'').toLowerCase()))return 'reflective';
  if(id==='silicon-photonics'&&/thermal|heat|stress|熱/.test(text))return 'thermal';
  if(['tesla','ferrari','steam-locomotive'].includes(id)&&/thermal|cool|heat|熱/.test(text))return 'thermal';
  const stageNumber=Number(step.stage?.order)||Number((step.stage?.id||'').match(/(?:^|-)(?:stage|s)(\d+)(?:$|-)/)?.[1])||Number(step.stageIndex??0)+1;
  return courseStageFamilies[id]?.[stageNumber-1]||courseFamilies[id]||categoryFamilies[course.category]||'integration';
 }
 // Topic-specific overrides precede the module family; no ID hash or random geometry.
 if(/bow|warp|flatness|翹曲|平坦度/.test(text))return 'molding';
 if(/repeatability|reference.*bias|reproducib|重複性/.test(text))return 'metrology';
 if(/yield|pareto|sampling|confidence|cpk|良率|抽樣/.test(text))return 'statistics';
 if(/particle|scratch|wafer.map|bin.map|粒子|刮傷|晶圓地圖/.test(text))return 'wafermap';
 if(/thermal|temperature|heat.path|散熱|熱阻/.test(text))return 'thermal';
 if(/overlay|align|registration|對準|對位/.test(text)&&id==='semiconductor')return 'lithography';
 if(/electrical|resistance|leakage|continuity|電阻|漏電|導通/.test(text))return 'electrical';
 const n=Number((step.stage?.id||'').match(/m(\d+)/)?.[1])||Math.ceil((Number((step.id||'').match(/-(\d+)/)?.[1])||1)/26);
 return (id==='packaging'?packageModules:semiconductorModules)[Math.max(0,Math.min(19,n-1))]||'integration';
}
function modeFor(course,step){
 const title=(step.titleEn||'').toLowerCase();
 if(V7_STAGE_FAMILIES[course.id])return 'inspect';
 if(EXPANSION_STAGE_FAMILIES[course.id]&&/^assemble.*(?:acceptance|traceability|dossier|evidence|report)/.test(title))return 'inspect';
 if(['idf','apache','submarine','cybersecurity','starlink'].includes(course.id))return /calculate|budget|sum|measure|compare delay/.test(title)?'measure':'inspect';
 if(/^(measure|calculate|integrate|quantify|fit|sum|add |budget|estimate|evaluate.*thickness|map.*resistivity)/.test(title))return 'measure';
 if(/^(align|place|position|attach|stack|bond|mount|assemble|land|join)/.test(title))return 'assembly';
 if(/^(deposit|etch|coat|develop|polish|grind|thin|plate|fill|mold|reflow|form |remove |strip |release |implant|anneal|cure|rinse|dry|grow|oxidize|sputter|transfer|clean |reveal|open |simulate)/.test(title))return 'process';
 return 'inspect';
}
const observations={
 growth:[bi('籽晶、晶肩、等徑晶棒與熔體具有先後及界面關係','Seed, shoulder, constant-diameter body and melt have ordered interfaces'),bi('晶棒形貌完全不受熱場與界面影響','Crystal shape is independent of field and interface')],
 cleaning:[bi('須使用一致量測基準比較移除前後的污染','Compare before and after contamination using the same measurement baseline'),bi('清洗後外觀變亮就可視為所有污染通過','A brighter appearance proves all contaminants passed')],
 trench:[bi('溝槽、襯層與填充接縫需要分別檢查','Inspect trench, liner and fill seam separately'),bi('頂面平坦就證明內部沒有接縫','A flat top proves no internal seam')],
 implantation:[bi('入射條件、濃度深度分布與活化結果是不同觀察量','Incidence, concentration profile and activation are different observables'),bi('摻雜濃度就是已活化載子濃度','Dopant concentration always equals active carrier concentration')],
 oxide:[bi('介電界面、膜厚與缺陷需要獨立核對','Verify dielectric interface, thickness and defects separately'),bi('只確認介電材料名稱便可放行','The dielectric material name alone permits release')],
 deposition:[bi('側壁與頂面厚度比是共形性指標之一','Sidewall-to-top thickness ratio is one conformality metric'),bi('只量頂面即可得到側壁厚度','Top thickness alone determines sidewall thickness')],
 lithography:[bi('光罩、光阻圖案與下層圖案需在共同座標比較','Compare mask, resist and underlying pattern in a common frame'),bi('曝光圖案位置與下層圖案無須相關','The exposure pattern need not relate to underlying layers')],
 etch:[bi('深度、側壁與遮罩消耗是不同驗收量','Depth, sidewall and mask consumption are separate checks'),bi('只確認有開口即可證明蝕刻全部合格','An opening proves every etch requirement passed')],
 gate:[bi('閘極、間隙壁、通道及接面有不同角色','Gate, spacer, channel and junction have distinct roles'),bi('間隙壁即為導電通道','The spacer is the conductive channel')],
 contact:[bi('導電連續性依賴開口、界面與填充品質','Continuity depends on opening, interface and fill quality'),bi('開口上方有金屬就保證界面電阻合格','Metal above an opening guarantees acceptable contact resistance')],
 cmp:[bi('去除凸起後仍需查凹陷、侵蝕與停止層','After removing peaks, check dishing, erosion and stop layer'),bi('研磨時間足夠就一定得到平面','Sufficient polishing time always produces a plane')],
 interconnect:[bi('金屬層需經通孔形成指定網路','Vias connect metal levels into the specified network'),bi('相鄰金屬外觀接近就表示已連通','Nearby metal appearance proves electrical continuity')],
 thinning:[bi('支撐、殘留厚度與應力需要共同驗證','Support, remaining thickness and stress need joint verification'),bi('厚度愈薄就愈容易搬運且不會破裂','Thinner wafers are always easier to handle and never fracture')],
 metrology:[bi('重複性描述讀值離散，不單獨證明準確度','Repeatability describes spread, not accuracy by itself'),bi('三次读值接近就保證無偏差','Three similar readings guarantee no bias')],
 electrical:[bi('激勵、接觸條件與量測回路需明確定義','Specify stimulus, contact conditions and measurement loop'),bi('量測線路接觸不影響數據','Measurement contact does not affect readings')],
 statistics:[bi('樣本分母、重測去重與分群須先定義','Define denominator, retest deduplication and grouping first'),bi('只累加通過次數即可計算良率','Counting pass events alone determines yield')],
 nanosheet:[bi('圖中三層通道需與環繞閘極區分','Distinguish three channels from the surrounding gate'),bi('製程節點名稱等於全部實體尺寸','The node name equals every physical dimension')],
 wafermap:[bi('右上群聚與其他孤立點的空間分布不同','The upper-right cluster differs spatially from isolated points'),bi('只保存缺陷總數，不需位置與分類','Save only total count, with no position or classification')],
 dicing:[bi('切割街道、支撐與晶粒邊緣需一併核對','Check streets, support and die edges together'),bi('分離出晶粒就代表沒有隱裂','A separated die proves no hidden crack')],
 dieattach:[bi('接合層、晶粒與載體形成熱及機械界面','The attachment layer joins thermal and mechanical interfaces'),bi('表面位置對準即可排除所有空洞','Position alignment excludes all voids')],
 wirebond:[bi('第一焊點、線弧與第二焊點分別需要證據','First bond, loop and second bond each need evidence'),bi('線弧外觀相似即證明接點強度相同','Similar loop appearance proves equal joint strength')],
 bump:[bi('焊墊、UBM、凸塊與接合界面是不同層次','Pad, UBM, bump and bonded interface are different levels'),bi('凸塊存在就保證下方介面導通','A visible bump guarantees its underlying interface conducts')],
 fanout:[bi('配線及端點延伸超出裸晶投影','Routing and terminals extend beyond the die footprint'),bi('扇出表示所有訊號必須走同一條線','Fan-out means every signal uses one wire')],
 molding:[bi('填充、空洞與翹曲需分別觀察','Observe fill, voids and warpage separately'),bi('外觀包覆完整即可排除內部缺陷','Complete outer coverage excludes internal defects')],
 rdl:[bi('重布線開口與導電路徑需要對位和連通驗證','RDL openings and routes require alignment and connectivity checks'),bi('介電層可直接當作金屬導線使用','Dielectric can serve directly as a metal wire')],
 tsv:[bi('絕緣襯層、阻障與金屬填充具有不同功能','Isolation liner, barrier and conductor fill serve different functions'),bi('只要挖出孔洞就已形成導电互連','Making a hole completes a conducting interconnect')],
 interposer:[bi('多晶粒透過中介層的互連與系統界面整合','Multiple dies integrate through interposer routing and interfaces'),bi('晶粒放在一起即自動具備正確連接','Placing dies together automatically connects them correctly')],
 substrate:[bi('金屬層透過導通孔跨越介電層連接','Vias join metal levels across dielectrics'),bi('每一介電層都可省略絕緣驗證','Every dielectric layer may skip insulation checks')],
 hybrid:[bi('介電與銅的雙界面都必須滿足接合條件','Both dielectric and copper interfaces must meet bonding conditions'),bi('只看金屬對準即可排除表面污染影響','Metal alignment alone excludes surface-contamination effects')],
 hbm:[bi('分層互連、底層晶粒與熱路徑各有驗證需求','Level interconnects, base die and heat paths need separate checks'),bi('層數愈多就必然有更低的溫度','More levels necessarily produce lower temperature')],
 underfill:[bi('填充前緣與殘留空洞是不同觀察量','Flow front and residual voids are different observables'),bi('看到膠流入就證明沒有未填區','Seeing flow proves no unfilled region remains')],
 thermal:[bi('熱源、接觸熱阻與邊界條件共同決定溫升','Heat source, contact resistance and boundary conditions determine temperature rise'),bi('只更改材料名稱即可保證相同熱效果','Changing only a material name guarantees the same thermal result')],
 optics:[bi('焦平面、像差與波長依賴需要分別核對','Check focal plane, aberrations and wavelength dependence separately'),bi('所有顏色一定在相同位置聚焦','Every color always focuses at exactly the same position')],
 reflective:[bi('光路使用反射鏡而非透射式玻璃鏡片','The optical path uses mirrors rather than transmissive glass lenses'),bi('此極紫外示意可直接改用普通玻璃透鏡','Ordinary glass lenses can replace the depicted EUV mirrors')],
 photonics:[bi('波導、耦合與偵測需以鏈路損耗共同評估','Evaluate guiding, coupling and detection with a link budget'),bi('只有導波便保證端到端鏈路可用','Guiding alone guarantees the complete link works')],
 aircraft:[bi('辨識公開結構載荷路徑並保留驗證界限','Identify public structural load paths and retain verification limits'),bi('此圖可直接當作真機製造圖','This schematic is a real-aircraft manufacturing drawing')],
 rotor:[bi('旋轉機械的能量、振動與量測須分開分析','Analyze rotating-machine energy, vibration and measurements separately'),bi('示意旋翼可直接推導真機操作參數','A schematic rotor directly determines real operating settings')],
 buoyancy:[bi('浮力、重量與作用位置共同決定平衡','Buoyancy, weight and their action points determine equilibrium'),bi('只有重量就可決定所有浮體穩定性','Weight alone determines all floating-body stability')],
 bridge:[bi('橋面載荷經斜索、塔與基礎傳遞','Deck loads transfer through stays, pylon and foundation'),bi('此圖比例可直接用於橋梁施工','These proportions can be used directly for bridge construction')],
 tunnel:[bi('地層、開挖面、支撐與監測必須連同判讀','Interpret geology, excavation face, support and monitoring together'),bi('拱形外觀即證明所有地層下都穩定','An arch shape proves stability in every ground condition')],
 network:[bi('每個信任邊界都需身分與授權檢查','Every trust boundary needs identity and authorization checks'),bi('位於內網就能跳過授權','Being on an internal network permits skipping authorization')],
 piston:[bi('活塞、連桿與曲柄把往復位移轉成旋轉','Piston, rod and crank convert reciprocation to rotation'),bi('曲柄半徑與活塞行程完全無關','Crank radius has no relation to piston stroke')],
 vehicle:[bi('車體、底盤、動力與散熱有相互界面','Body, chassis, power and cooling have interacting interfaces'),bi('單一零件合格就表示整車合格','One passing part proves the complete vehicle passes')],
 battery:[bi('電芯、監測與隔離需以系統觀點驗證','Verify cells, monitoring and isolation as a system'),bi('此圖是帶電高壓電池接線指引','This is an energized high-voltage wiring guide')],
 satellite:[bi('平台、鏈路與地面站的功能證據需連貫','Functional evidence must connect bus, link and ground station'),bi('單一衛星圖可保證任何地點連線品質','One satellite picture guarantees service quality everywhere')],
 dam:[bi('水頭、流量、轉換效率與結構條件不同','Head, flow, conversion efficiency and structural conditions differ'),bi('水位愈高便可忽略其他工程條件','Higher water alone permits ignoring all other conditions')],
 rail:[bi('車體、走行、牽引與煞車必須界面驗證','Verify interfaces across body, running gear, traction and braking'),bi('畫出列車就表示運控已經通過驗證','Drawing a train proves its control system is validated')]
};
Object.assign(observations,{
 materials:[bi('材料微結構、製程紀錄與品質證據須互相對照','Correlate material structure, processing records and quality evidence'),bi('材料名稱相同便保證微結構與性能完全相同','Equal material names guarantee identical microstructure and performance')],
 maintenance:[bi('可達性、檢查位置與紀錄應在設計時定義','Define access, inspection locations and records during design'),bi('封閉界面不需考慮後續檢查','A closed interface never needs later inspection')],
 vibration:[bi('振動頻谱峰值與激勵、結構及取樣条件共同解讀','Interpret spectral peaks with excitation, structure and sampling'),bi('一個頻率峰值必然代表同一種故障','One frequency peak always identifies a single fault')],
 powertrain:[bi('轉矩、轉速與能量流在傳動界面相關','Torque, speed and energy flow interact across a drivetrain'),bi('提高轉速必然同時無限提高轉矩','Increasing speed always increases torque without limit')],
 safety:[bi('未驗證的隔離或保護不能視為已完成','Unverified isolation or protection is not complete'),bi('畫出保護元件就表示功能已驗證','Drawing a protective component proves it was validated')],
 pressure:[bi('壓力法向作用於表面，穩定性還取決於形狀和材料','Pressure acts normal to surfaces; stability also depends on shape and material'),bi('只有平面面積即可判定外壓結構不會失穩','Area alone proves an externally pressured structure cannot buckle')],
 site:[bi('地形、環境及交通需求須有共同場址基準','Relate terrain, environment and transport needs in a common site frame'),bi('只看一張照片即可決定基礎位置','One photograph determines foundation locations')],
 ground:[bi('地層界面、地下水與不確定性需一起標示','Show strata, groundwater and uncertainty together'),bi('同一顏色地層必然處處相同','A same-color layer is necessarily uniform everywhere')],
 groundwater:[bi('水頭差與介質條件影響滲流方向','Head differences and medium properties affect seepage direction'),bi('地下水永遠與地表平行流動','Groundwater always flows parallel to the ground surface')],
 corrosion:[bi('防護層破口會改變局部暴露條件','A coating breach changes local exposure conditions'),bi('完整外觀可證明保護層內無任何缺陷','Good appearance proves no concealed coating defect')],
 ventilation:[bi('流路、方向與量測位置需相互核對','Correlate flow paths, direction and measurement locations'),bi('只要有風機就代表所有區域通風相同','One fan guarantees equal ventilation everywhere')],
 assets:[bi('資料流需要對應明確的資產與責任邊界','Map data flows to identified assets and responsibility boundaries'),bi('未知設備可以預設為可信任','Unknown devices may be trusted by default')],
 identity:[bi('身分驗證與權限授與是不同檢查','Authentication and authorization are distinct checks'),bi('登入成功即有全部資料的權限','A successful login grants access to all data')],
 software:[bi('版本、驗證證據與可回復路線需一併保留','Preserve version, verification evidence and recovery path'),bi('更新成功下載即表示全部功能已通過','Downloading an update proves all functions passed')],
 monitoring:[bi('告警需以時間、上下文與複判證據解讀','Interpret an alert with time, context and review evidence'),bi('所有告警都可不經判讀自動忽略','Every alert may be ignored without review')],
 backup:[bi('完成還原並核對資料才構成可用性證據','Restore and verify data to demonstrate backup usability'),bi('檔名出現在備份清單即表示還原一定成功','A filename in a backup list guarantees successful restore')],
 boiler:[bi('熱輸入、相變與熱損失必須守恆核算','Account for heat input, phase change and losses'),bi('加熱即可忽略壓力與材料限制','Heating permits ignoring pressure and material limits')],
 braking:[bi('動能須轉成熱或被回收，且兩者有條件限制','Kinetic energy becomes heat or recovered energy under defined limits'),bi('煞車使能量直接消失','Braking makes energy disappear')],
 suspension:[bi('彈簧儲能與阻尼耗能具有不同角色','Spring energy storage and damping dissipation have different roles'),bi('彈簧與阻尼器功能完全相同','Springs and dampers have identical functions')],
 finish:[bi('表面粗糙度與外觀缺陷需使用明確量測條件','Define measurement conditions for roughness and appearance defects'),bi('光澤較高就代表所有尺寸及結構品質較好','More gloss proves every dimensional and structural property is better')],
 orbit:[bi('地面站、可視範圍與軌道位置共同影響幾何','Ground station, visibility and orbital position jointly set geometry'),bi('一顆低軌衛星可永遠靜止覆蓋同一地點','One low-orbit satellite stays fixed over one site forever')],
 antenna:[bi('陣列相位差影響疊加方向，不是改變光速','Array phase differences change interference direction, not propagation speed'),bi('調相等同讓傳播速度任意改變','Phase adjustment arbitrarily changes propagation speed')],
 hydrology:[bi('蓄水變化需核算流入、流出與其他收支','Storage change needs inflow, outflow and other balance terms'),bi('只看流入就能知道水位永遠上升','Inflow alone proves water level always rises')],
 turbine:[bi('水力能、轉軸機械能與電能有轉換及損失','Hydraulic, shaft and electrical energy include conversion and losses'),bi('輸出電能可以無條件超過輸入能量','Electrical output can exceed input energy without conditions')],
 lock:[bi('閘室水位與上下游界面狀態需協調','Coordinate chamber level with upstream and downstream interface states'),bi('任何水位下均可同時任意開啟全部閘門','All gates may be opened arbitrarily at any water level')],
 doors:[bi('車門狀態需與功能允許條件分別驗證','Verify door state and functional permission conditions separately'),bi('畫面顯示關閉就可省略狀態驗證','A closed icon permits skipping state verification')],
 coupling:[bi('光斑形狀、位置與角度共同影響耦合','Mode shape, position and angle affect coupling'),bi('光源較亮就能補救所有模態不匹配','A brighter source fixes all mode mismatch')],
 resonator:[bi('共振頻譜需與溫度、耦合及損耗一起解讀','Interpret resonance with temperature, coupling and loss'),bi('共振峰位置與環境完全無關','Resonance position is independent of environment')],
 backside:[bi('正面訊號与背面供電仍需介面及隔離驗證','Front-side signals and backside power need interface/isolation checks'),bi('背面供電會自動消除所有電壓降','Backside power automatically eliminates every voltage drop')]
});
export function resolveExercise(course={},step={}){
 // Extension-only architecture: preserve every original course step and scene.
 if(String(step.id).includes('-v15-')&&course.v15Architecture)course={...course,...course.v15Architecture};
 if(String(step.id).includes('-v14-')&&course.v14Architecture)course={...course,...course.v14Architecture};
 // V13: extended courses keep their own artwork; their new steps use the V13 architecture.
 if(String(step.id).includes('-v13-')&&!course.architectureFamily&&course.v13Architecture)course={...course,...course.v13Architecture};
 const expansion=resolveExpansionExercise(course,step);if(expansion)return expansion;
 if(first26[step.id])return first26[step.id]();
 if(firstPackage[step.id])return firstPackage[step.id]();
 if((String(step.id).includes('-v17-') && hasWorldVisual(course)) || ((course.educationEdition===11 && (course.curriculumVersion>=11 || String(step.id).includes('-v11-')) && (COMPUTING_SUBJECTS[course.id] || hasWorldVisual(course))) || String(step.id).includes('-v12-') || (String(step.id).includes('-v13-') && hasWorldVisual(course)) || (String(step.id).includes('-v14-') && hasWorldVisual(course)) || (String(step.id).includes('-v15-') && hasWorldVisual(course)))){
  const n=Number(step.sequence)||1,quiz=step.quiz,validQuiz=quiz&&Array.isArray(quiz.options)&&Array.isArray(quiz.optionsEn)&&quiz.options.length===quiz.optionsEn.length&&Number.isInteger(quiz.answer)&&quiz.answer>=0&&quiz.answer<quiz.options.length;
  const decisions=validQuiz?quiz.options.map((v,i)=>opt('answer-'+i,v,quiz.optionsEn[i])):[opt('evidence',step.check,step.checkEn),opt('guess','未核對模型邊界便沿用另一個案例','Reuse a case without checking model boundaries'),opt('omit','跳過本步所需的證據','Skip the required evidence')];
  const offset=n%decisions.length,computing=!!COMPUTING_SUBJECTS[course.id];
  return make(`${step.id}-evidence`,'inspect',`${computing?'itv11':'worldv11'}:${course.id}`,bi(course.title,course.titleEn),bi(validQuiz?`${step.instruction}\n判讀：${quiz.question}`:step.instruction,validQuiz?`${step.instructionEn}\nReview: ${quiz.questionEn}`:step.instructionEn),bi('架構與證據的工程判讀','Engineering review of architecture and evidence'),bi(validQuiz?`${step.check} ${quiz.explanation||''}`:step.check,validQuiz?`${step.checkEn} ${quiz.explanationEn||''}`:step.checkEn),{choices:[...decisions.slice(offset),...decisions.slice(0,offset)],expectedChoice:validQuiz?'answer-'+quiz.answer:'evidence',provenance:'semantic-template',family:computing?computingVisualFamily(course.id):worldVisualFamily(course),visualFocus:(n-1)%(computing?COMPUTING_SUBJECTS[course.id].nodes.length:Math.max(1,Math.min(6,course.architectureNodes?.length||1))),worldCourse:computing||!hasWorldVisual(course)?null:{id:course.id,title:course.title,titleEn:course.titleEn,architectureFamily:course.architectureFamily,architectureNodes:course.architectureNodes,architectureEdges:course.architectureEdges},coverage:bi('專屬功能架構配合本步證據題與雙手概念操作；高亮是功能導讀，不是實體元件位置或設備運轉程序。詳細算例與理想量子模擬另行標示。','Subject-specific architecture with this step’s evidence question and two-hand conceptual interaction. Highlights are functional guidance, not physical component positions or operating procedures. Calculators and ideal quantum models are separately labeled.')});
 }
 if(ELECTRONICS_SUBJECTS[course.id] && (course.curriculumVersion>=10 || String(step.id).includes('-v10-'))){
  const n=Number(step.sequence)||Number(String(step.id).match(/(\d+)$/)?.[1])||1;
  const quiz=step.quiz,validQuiz=quiz&&Array.isArray(quiz.options)&&Array.isArray(quiz.optionsEn)&&quiz.options.length===quiz.optionsEn.length&&Number.isInteger(quiz.answer)&&quiz.answer>=0&&quiz.answer<quiz.options.length;
  const decisions=validQuiz?quiz.options.map((v,i)=>opt('answer-'+i,v,quiz.optionsEn[i])):[opt('evidence',step.observation||step.check,step.observationEn||step.checkEn),opt('skip','只憑外觀跳過量測與界面查核','Skip measurements and interface review based on appearance'),opt('transfer','未核對模型邊界就套用其他設備結果','Transfer another device result without checking model boundaries')];
  const offset=n%decisions.length;
  return make(`${step.id}-evidence`,'inspect',`elev10:${course.id}`,bi(course.title,course.titleEn),bi(validQuiz?`${step.instruction}\n判讀：${quiz.question}`:step.instruction,validQuiz?`${step.instructionEn}\nReview: ${quiz.questionEn}`:step.instructionEn),bi('電機電子的功能界面證據檢視','Electrical/electronic functional-interface review'),bi(validQuiz?`${step.check} ${quiz.explanation||''}`:step.check,validQuiz?`${step.checkEn} ${quiz.explanationEn||''}`:step.checkEn),{choices:[...decisions.slice(offset),...decisions.slice(0,offset)],expectedChoice:validQuiz?'answer-'+quiz.answer:'evidence',provenance:'semantic-template',family:electronicsVisualFamily(course.id),visualFocus:(n-1)%3,coverage:bi('本主題專屬功能圖搭配本工序證據判讀；高亮輪流提醒三個功能界面，不代表本步實物位置。不是接線指南、帶電作業或完整設備數位分身。','A topic-specific functional diagram accompanies this step’s evidence review. The highlight cycles through three functional interfaces, not the physical location of this operation. It is not wiring, energized work or a complete equipment digital twin.')});
 }
 if(course.curriculumVersion>=9 && course.category==='packaging' && !['packaging','silicon-photonics','a106'].includes(course.id)){
  const n=Number(step.sequence)||Number(String(step.id).match(/(\d+)$/)?.[1])||1;
  // Step-authored questions provide domain-specific alternatives when available.
  const quiz=step.quiz,validQuiz=quiz&&Array.isArray(quiz.options)&&Array.isArray(quiz.optionsEn)&&quiz.options.length===quiz.optionsEn.length&&Number.isInteger(quiz.answer)&&quiz.answer>=0&&quiz.answer<quiz.options.length;
  const decisions=validQuiz?quiz.options.map((v,i)=>opt('answer-'+i,v,quiz.optionsEn[i])):[opt('evidence',step.observation||step.check,step.observationEn||step.checkEn),opt('skip','只憑外觀跳過量測與界面查核','Skip measurements and interface review based on appearance'),opt('transfer','未核對材料與邊界就移用其他工法結果','Transfer another process result without checking materials or boundaries')];
  const offset=n%decisions.length;
  return make(`${step.id}-evidence`,'inspect',`packv9:${course.id}`,bi(course.title,course.titleEn),bi(validQuiz?`${step.instruction}\n判讀：${quiz.question}`:step.instruction,validQuiz?`${step.instructionEn}\nReview: ${quiz.questionEn}`:step.instructionEn),bi('封裝與光子介面證據檢視','Packaging and photonic interface evidence review'),bi(validQuiz?`${step.check} ${quiz.explanation||''}`:step.check,validQuiz?`${step.checkEn} ${quiz.explanationEn||''}`:step.checkEn),{choices:[...decisions.slice(offset),...decisions.slice(0,offset)],expectedChoice:validQuiz?'answer-'+quiz.answer:'evidence',provenance:'semantic-template',family:packagingVisualFamily(course.id),coverage:bi('本主題專屬原理圖搭配本工序判讀；可觀察界面與驗證證據，並非逐步真實設備或全物理量產模擬。','A topic-specific principle diagram with this step’s evidence review; it supports interface reasoning, not a real-tool or full-physics production simulation.'),focus:focusFor(step,packagingVisualFamily(course.id))});
 }
 if(course.curriculumVersion===8 && course.category==='semiconductor'){
  const n=Number(step.sequence)||Number(String(step.id).match(/(\d+)$/)?.[1])||1;
  const decisions=[opt('evidence',step.observation||step.check,step.observationEn||step.checkEn),opt('skip','不檢查資料，僅凭外觀接受本步結果','Accept by appearance without checking the data'),opt('transfer','把其他材料或設備的結果直接視為本步驗證','Treat results from another material or tool as verification of this step')];
  const offset=n%decisions.length;
  return make(`${step.id}-evidence`,'inspect',`semiv8:${course.id}`,bi(course.title,course.titleEn),bi(step.instruction,step.instructionEn),bi('本工序的介面與證據檢視','Step interface and evidence review'),bi(step.check,step.checkEn),{choices:[...decisions.slice(offset),...decisions.slice(0,offset)],expectedChoice:'evidence',provenance:'semantic-template',family:semiconductorVisualFamily(course.id),coverage:bi('依本工序教材編排的證據檢視；圖為共用原理教具，不是逐道量產模擬。','Evidence review grounded in this lesson. The diagram is a shared principle model, not a simulation of each production operation.'),focus:focusFor(step,semiconductorVisualFamily(course.id))});
 }
 const family=familyFor(course,step),f=families[family],mode=modeFor(course,step);
 const controls=mode==='measure'?[ctl('reading',f.metric.zh,f.metric.en,f.min??0,f.max,Number.isInteger(f.target)?(f.max<=2?.05:f.max<=12?.1:1):.1,f.initial,f.target,f.unit,f.max<=2?.026:.051)]:mode==='process'?[ctl('phase','製程示意階段','Schematic process stage',0,4,1,0,4,' / 4',0)]:[];
 const observation=f.observation||observations[family]||[bi('保留需求、界面與驗收證據','Preserve requirements, interfaces and acceptance evidence'),bi('只憑外觀即可跳過界面驗證','Appearance alone permits skipping interface verification')];
 let choices=mode==='inspect'?[{id:'evidence',label:observation[0]},{id:'appearance',label:observation[1]},opt('skip','沒有量測也視為全部通過','Treat missing measurements as passing')]:[];
 if(choices.length){const offset=(Number((step.id||'').match(/(\d+)$/)?.[1])||0)%choices.length;choices=[...choices.slice(offset),...choices.slice(0,offset)];}
 const scope=bi('共用工程模型依本工序主題選用；不是此製程的完整數位分身。','A shared engineering model selected for this topic, not a complete digital twin of the process.');
 const action=mode==='measure'?bi('根據圖中的明示教學樣本，計算並輸入讀值；再以本工序文字查核適用條件。','Calculate the explicitly labeled teaching specimen, enter the reading, then check applicability against the step text.'):mode==='process'?bi('逐段調整示意階段，觀察介面變化，再按執行以記錄結果；此控制不是設備配方。','Advance the schematic phases, inspect interface changes, then run to record; this is not an equipment recipe.'):mode==='assembly'?bi('將此工序的實體示意件對準相應界面，放開後提交；其外觀不是原廠 CAD。','Align the depicted component with its interface, release and submit; this is not OEM CAD.'):bi('檢查此工序對應的界面與證據，選擇判讀原則，並記錄觀察。','Inspect relevant interfaces and evidence, choose the review principle and record the observation.');
 const evidence=bi(`${f.phase.zh}。${step.check||step.objective||'請以來源核對假設與限制。'}`,`${f.phase.en}. ${step.checkEn||step.objectiveEn||'Verify assumptions and limits against sources.'}`);
 return make(`${family}-${mode}-shared`,mode,f.scene,f.name,action,f.tool,evidence,{controls,choices,expectedChoice:mode==='inspect'?'evidence':null,provenance:'semantic-template',coverage:scope,family,phaseLabels:f.phase,sampleMetric:f.metric,sampleTarget:f.target,sampleUnit:f.unit,focus:focusFor(step,family)});
}
function focusFor(step,family){
 const title=`${step.titleEn||''} ${step.title||''}`.toLowerCase();
 const type=/thermal|temperature|heat|熱/.test(title)?'thermal':/vibrat|frequency|resonan|振動|頻率/.test(title)?'wave':/current|voltage|resistance|electrical|電性|電阻|漏電/.test(title)?'circuit':/layer|film|coat|thickness|dielectric|膜厚|介電|圖層/.test(title)?'layers':/load|force|pressure|stress|stress|力|壓/.test(title)?'force':/flow|fluid|water|rins|clean|流|水|清洗/.test(title)?'flow':/align|position|register|overlay|對準|對位/.test(title)?'alignment':/inspect|defect|classify|contamin|檢查|缺陷|分類/.test(title)?'inspect':/data|identity|permission|software|record|資料|軟體|權限/.test(title)?'data':'interface';
 return {type,title:bi(step.title||'工序介面',step.titleEn||'Process interface'),family};
}
export function evaluateExercise(spec,state={}){
 const values=state?.values&&typeof state.values==='object'?state.values:{};
 const numbers=spec.controls.every(c=>Number.isFinite(Number(values[c.id]))&&Math.abs(Number(values[c.id])-c.target)<=c.tolerance+1e-8);
 const choice=!spec.expectedChoice||state.choice===spec.expectedChoice;
 const action=spec.mode==='inspect'?state.observed===true:spec.mode==='process'?state.performed===true:true;
 const passed=numbers&&choice&&action;
 const readout=bi(spec.controls.map(c=>`${c.label.zh}: ${Number.isFinite(Number(values[c.id]))?Number(values[c.id]).toFixed(c.step<1?2:0):'—'} ${c.unit}`).join(' · ')||((spec.choices.find(c=>c.id===state.choice)||{}).label?.zh||(spec.mode==='assembly'?'對位後放開零件並提交':'尚未選擇判讀')),spec.controls.map(c=>`${c.label.en}: ${Number.isFinite(Number(values[c.id]))?Number(values[c.id]).toFixed(c.step<1?2:0):'—'} ${c.unit}`).join(' · ')||((spec.choices.find(c=>c.id===state.choice)||{}).label?.en||(spec.mode==='assembly'?'Align, release and submit the component':'No review selection')));
 return {passed,readout,evidence:passed?spec.evidence:bi(!numbers?'讀值／階段尚未與本示例一致。':!choice?'請重新檢查剖面、圖層或路線選擇。':spec.mode==='process'?'請執行並記錄此示意製程。':'請記錄本次觀察。',!numbers?'Reading/phase does not yet match this specimen.':!choice?'Recheck the cross-section, layers or route.':spec.mode==='process'?'Run and record this schematic process.':'Record your observation.')};
}

const firstPackage={
'pk-001':()=>make('package-functions','inspect','package-functions',bi('封裝的電、熱、機械與保護界面','Electrical, thermal, mechanical and protective interfaces'),bi('追蹤剖面中的四條功能路徑。選擇同時涵蓋連接、散熱、保護及機械支撐的需求邊界。','Trace four functional paths. Select a boundary covering interconnect, heat removal, protection and mechanical support.'),bi('封裝功能剖面審查','Package-function section review'),bi('封裝不是只有外殼：不同功能之間也可能有熱膨脹、寄生參數與維修性取捨。','Packaging is more than a shell: functions trade off thermal expansion, parasitics and serviceability.'),{choices:[opt('all','電性＋熱＋保護＋機械界面','Electrical + thermal + protection + mechanical'),opt('shell','只有外觀與外殼','Appearance and shell only'),opt('pins','只計算接腳數','Pin count only')],expectedChoice:'all'}),
'pk-002':()=>make('package-io-table','measure','io-map',bi('訊號與電源 I/O 需求','Signal and power I/O requirements'),bi('教學樣本有 64 個訊號、16 個電源、16 個接地端，計算端點總數；不要把電源與接地省略。','A specimen has 64 signal, 16 power and 16 ground terminals. Sum all categories.'),bi('I/O 分配矩陣','I/O allocation matrix'),bi('總數為 96；數目相同不代表電流、訊號完整性與實體排布均滿足。','Total = 96; matching count does not prove current capacity, signal integrity or physical layout.'),{controls:[ctl('reading','需求端點總數','Required terminal count',0,160,1,64,96,'terminals',0)]}),
'pk-003':()=>make('package-height-budget','measure','package-height',bi('封裝堆疊高度與餘裕','Package-stack height and margin'),bi('示例基板 0.5、互連 0.1、晶粒 0.2、上方保護 0.3 mm。求總高度；1.2 mm 外形預算還剩多少？','Example substrate .5, interconnect .1, die .2 and protection .3 mm. Compute stack height and remaining margin to 1.2 mm.'),bi('層次高度預算器','Stack-height budget calculator'),bi('總高 1.1 mm、餘裕 0.1 mm。實際仍需累計公差、翹曲與量測定義。','Total 1.1 mm, margin .1 mm; real budgets include tolerances, warpage and measurement definitions.'),{controls:[ctl('height','總高度','Total height',0,2,.1,0,1.1,'mm',.025),ctl('margin','高度餘裕','Height margin',0,.5,.1,0,.1,'mm',.025)]}),
'pk-004':()=>make('wirebond-flipchip-route','process','package-route',bi('打線與覆晶的替代路線','Wirebond and flipchip alternatives'),bi('案例晶粒正面朝下、使用面陣列接點。選覆晶路線並執行依賴檢查，不加入線弧工序。','The specimen is face-down with an area-array interface. Select flipchip and check dependencies; do not insert wire-loop steps.'),bi('封裝路線依賴圖','Package-route dependency graph'),bi('打線通常使用朝上的可接近焊墊；覆晶以翻轉晶粒的面陣列接點互連。這些是概念路線。','Wirebond accesses face-up pads; flipchip uses a face-down array. These are conceptual routes.'),{choices:[opt('wire','朝上打線','Face-up wirebond'),opt('flip','朝下面陣列覆晶','Face-down array flipchip')],expectedChoice:'flip'}),
'pk-005':()=>make('fanin-fanout-footprint','inspect','fanout',bi('晶粒投影與外擴接點','Die footprint and expanded terminals'),bi('图中部分外部接點已超出裸晶投影。選擇扇出架構，並記錄投影邊界證據。','Some external terminals lie outside the die footprint. Identify fan-out and record the footprint evidence.'),bi('投影邊界比較器','Footprint-boundary comparator'),bi('Fan-out 的配線／端點可伸出裸晶投影；不能僅因封裝外形大於晶粒就判斷技術路線。','Fan-out routing/terminals may extend beyond the die footprint; package size alone does not prove the route.'),{choices:[opt('in','扇入：端點均在裸晶投影內','Fan-in: terminals within die footprint'),opt('out','扇出：端點延伸至投影外','Fan-out: terminals beyond footprint')],expectedChoice:'out'}),
'pk-006':()=>make('leadframe-substrate-choice','inspect','substrate-choice',bi('導線架與有機多層基板','Leadframe and organic multilayer substrate'),bi('案例需多層訊號交叉與多個介電／金屬層。辨識右側有機基板剖面。','The specimen needs multilayer signal crossings and dielectric/metal levels. Identify the organic substrate section at right.'),bi('載體架構比對','Carrier architecture comparator'),bi('架構選擇還須考慮 I/O、熱與成本；此例只用多層配線需求作判斷。','I/O, heat and cost also matter; this example isolates the multilayer-routing requirement.'),{choices:[opt('leadframe','A 單片式金屬導線架','A Monolithic leadframe'),opt('organic','B 有機多層基板','B Organic multilayer substrate')],expectedChoice:'organic'})
};
// Explicit packaging entries are checked by resolveExercise via this hoisted registry.

const colors={ink:'#163d38',si:'#638b89',oxide:'#a4cdd6',metal:'#d8a84e',poly:'#a2799c',resist:'#df8c77',glass:'#c9ddd2',red:'#c06459',green:'#4d9471',paper:'#f2f6ec'};
const line=(x1,y1,x2,y2,color=colors.ink,width=1.5,dash='')=>`<path d="M${x1} ${y1}L${x2} ${y2}" stroke="${color}" stroke-width="${width}" fill="none" ${dash?`stroke-dasharray="${dash}"`:''}/>`;
const rect=(x,y,w,h,fill=colors.si,rx=0,stroke=colors.ink)=>`<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${rx}" fill="${fill}" stroke="${stroke}" stroke-width="1.1"/>`;
const text=(x,y,value,size=10,color=colors.ink,anchor='start')=>`<text x="${x}" y="${y}" fill="${color}" font-size="${size}" text-anchor="${anchor}" font-family="system-ui,sans-serif">${esc(value)}</text>`;
const circle=(x,y,r,fill=colors.metal,stroke=colors.ink)=>`<circle cx="${x}" cy="${y}" r="${r}" fill="${fill}" stroke="${stroke}" stroke-width="1.1"/>`;
const path=(d,fill='none',stroke=colors.ink,w=1.5)=>`<path d="${d}" fill="${fill}" stroke="${stroke}" stroke-width="${w}"/>`;
function block(x,y,w,h,fill){return rect(x,y,w,h,fill)+path(`M${x} ${y}l12-8h${w}l-12 8z`,fill)+path(`M${x+w} ${y}l12-8v${h}l-12 8z`,fill)}
function dimension(x1,y1,x2,y2,label){return line(x1,y1,x2,y2,colors.red)+line(x1-4,y1-4,x1+4,y1+4,colors.red)+line(x2-4,y2-4,x2+4,y2+4,colors.red)+text((x1+x2)/2,(y1+y2)/2-6,label,10,colors.red,'middle')}
function waferBase(){return circle(195,137,79,'#c4d5d7')+path('M185 214l10-8 10 8',colors.paper,colors.ink)+line(105,137,285,137,'#809d9c',1,'3 4')+line(195,48,195,219,'#809d9c',1,'3 4')}
function dots(points,color=colors.red){return points.map(([x,y],i)=>circle(x,y,2.5+(i%2),color)).join('')}
function crossSection(kind,phase=4){
 let out=block(70,169,260,39,colors.si)+text(84,193,'Si / support',11,'#fff');
 if(kind==='cmos'){
  out=phase>=1?out:rect(70,206,260,2,'#bdc9c4');
  if(phase>=2)out+=rect(70,152,260,17,colors.oxide)+rect(94,160,44,18,colors.oxide)+rect(270,160,34,18,colors.oxide);
  if(phase>=3)out+=rect(174,117,49,34,colors.poly)+rect(162,128,12,25,colors.oxide)+rect(223,128,12,25,colors.oxide)+text(198,111,'Gate',10,colors.ink,'middle');
  if(phase>=4)out+=rect(135,128,17,41,colors.metal)+rect(249,128,17,41,colors.metal);
  if(phase>=5)out+=rect(98,116,57,11,colors.metal)+rect(244,116,54,11,colors.metal);
  out+=text(83,228,'Substrate → oxide → gate → contacts → metal',9);
 }else if(['soi','epi','oxide'].includes(kind)){
  out+=rect(70,136,260,32,kind==='epi'?'#7bab92':colors.oxide)+rect(70,116,260,20,colors.si);
  out+=text(90,130,'A  Device Si',10,'white')+text(90,157,kind==='epi'?'Epitaxial layer':'B  BOX / dielectric',11)+text(90,195,'C  Handle Si',11,'white');
  if(kind==='epi')out+=dimension(343,136,343,168,'5 µm');
 }else if(['trench','etch','deposition','gate','contact','interconnect','nanosheet','tsv'].includes(kind)){
  if(kind==='nanosheet'){
   out+=rect(124,77,148,87,'#c7acd5');
   for(let i=0;i<3;i++)out+=rect(130,86+i*26,134,12,colors.si,3)+text(282,96+i*26,`Si ${i+1}`,10);
   out+=text(198,62,'Surrounding gate / 3 channels',11,colors.ink,'middle');
  }else if(kind==='tsv'){
   out=block(70,83,260,125,colors.si);
   [128,222].forEach(x=>{out+=rect(x,80,43,130,colors.oxide)+rect(x+7,80,29,130,'#876777')+rect(x+11,80,21,130,phase>=3?colors.metal:'#f2f6ec')});
   out+=text(85,231,'Si | liner | barrier | Cu',10)+dimension(348,84,348,208,'6 / 2 = 3');
  }else{
   out+=rect(70,112,260,57,colors.oxide);
   const depth=phase===0?7:12+phase*9;
   [118,237].forEach(x=>{out+=rect(x,108,43,depth,colors.paper);if(['deposition','contact','interconnect'].includes(kind)&&phase>1)out+=path(`M${x+4} 108v${depth-4}h35V108`,'none',kind==='deposition'?colors.poly:colors.metal,5)});
   if(kind==='gate')out+=rect(175,91,45,61,colors.poly)+rect(164,108,11,44,colors.oxide)+rect(220,108,11,44,colors.oxide);
   if(kind==='interconnect')out+=rect(91,94,85,14,colors.metal)+rect(222,94,85,14,colors.metal)+rect(70, 67,260,12,colors.oxide);
   if(kind==='etch')out+=path('M118 112h43m76 0h43','none',colors.resist,7)+[130,148,250,268].map(x=>path(`M${x} 68v31m-4-7l4 7 4-7`,'none',colors.red,1.5)).join('');
   out+=text(78,226,kind==='deposition'?'Sidewall / top thickness = 0.8':kind==='contact'?'Interface → barrier → conductor':kind==='gate'?'Gate / spacers / channel':kind==='trench'?'Mask / trench / liner / fill':'Pattern / depth / interface',10);
  }
 }else if(kind==='cmp'){
  out+=path('M70 166v-22h55v-31h63v26h60v-34h82v61z',colors.oxide);
  if(phase>1)out+=rect(70,105,260,31,colors.paper,0,colors.paper)+line(70,139,330,139,colors.red,2,'5 4');
  out+=`<ellipse cx="201" cy="80" rx="94" ry="17" fill="#819b92" stroke="${colors.ink}"/>`+rect(175,47,52,18,colors.glass)+text(82,226,'Stop plane / residual topography',10);
 }
 return out;
}

function packageSection(kind,phase=4){
 let out=block(62,189,278,27,'#809870')+text(76,207,'substrate',10,'#fff');
 if(['dieattach','underfill','package-functions','package-height','hybrid','interposer','fanout','molding','hbm','bump','substrate','rdl','wirebond','handling','thinning'].includes(kind)){
  if(kind==='substrate'){
   out='';for(let i=0;i<4;i++)out+=rect(65,83+i*31,270,23,i%2?colors.glass:'#9bad7c')+path(`M76 ${94+i*31}h68l22 6h75l20-6h63`,'none',colors.metal,5);
   out+=rect(128,100,8,78,colors.metal)+rect(263,130,8,47,colors.metal)+text(84,223,'4 metal levels / dielectric / vias',10);return out;
  }
  if(kind==='wirebond'){
   out+=rect(139,145,124,34,colors.si)+rect(137,178,128,11,colors.metal);
   [0,1,2].forEach(i=>out+=path(`M${159+i*35} 145Q${126+i*28} ${63-i*9} ${84+i*12} 185`,'none',colors.metal,3)+circle(159+i*35,145,3,colors.metal));
   out+=text(267,145,'Die',10)+text(69,61,'Loop / first bond / second bond',10);return out;
  }
  if(kind==='hbm'){
   for(let i=0;i<4;i++)out+=block(127,157-i*23,147,17,i%2?colors.si:'#81a3b7');
   [149,194,239].forEach(x=>out+=line(x,77,x,182,colors.metal,4,'3 3'));
   out+=text(290,103,'4 levels',10)+text(285,181,'Base die',10);return out;
  }
  if(kind==='hybrid'){
   out+=rect(83,99,233,40,colors.si)+rect(83,151,233,33,colors.si)+rect(83,139,233,12,colors.oxide);
   [109,162,215,269].forEach(x=>out+=rect(x,127,20,36,colors.metal));
   out+=line(73,145,330,145,colors.red,1.5,'5 4')+text(98,78,'Cu / dielectric mating surfaces',10);return out;
  }
  if(kind==='interposer'){
   out+=rect(80,159,239,20,colors.oxide);[87,165,245].forEach((x,i)=>{out+=block(x,106+i*8,63,40,colors.si);[x+10,x+29,x+48].forEach(z=>out+=circle(z,155,4,colors.metal))});
   out+=path('M97 176h196M126 174v16m55-16v16m90-16v16','none',colors.metal,2)+text(91,76,'Compute / memory / I/O',11);return out;
  }
  if(kind==='fanout'||kind==='rdl'){
   out+=rect(80,108,237,58,'#c9bead')+rect(151,109, 97,35,colors.si)+line(151,88,151,181,colors.red,1,'4 4')+line(248,88,248,181,colors.red,1,'4 4');
   [104,164,228,294].forEach((x,i)=>out+=path(`M${165+i*20} 145v15H${x}v21`,'none',colors.metal,3)+circle(x,184,5,colors.metal));
   out+=text(91,73,'Die footprint / expanded routing',10);return out;
  }
  if(kind==='handling'){
   out+=`<ellipse cx="198" cy="112" rx="123" ry="37" fill="${colors.si}" stroke="${colors.ink}"/>`+path('M77 111v11q120 75 243 0v-11','none',colors.ink)+text(123,92,'FRONT: keep clear',11,'#fff')+text(151,162,'Backside support',10);return out;
  }
  if(kind==='thinning'){
   out+=rect(80,168,237,14,colors.oxide)+rect(80,117,237,50-phase*8,colors.si)+path('M111 70h172l-18 22H129z',colors.glass)+line(198,49,198,68,colors.ink,4)+text(95,231,'Carrier / protection / remaining Si',10);return out;
  }
  out+=rect(122,138,153,37,colors.si)+rect(120,174,157,10,kind==='underfill'?'#d19c78':colors.metal);
  [137,177,217,257].forEach(x=>out+=circle(x,182,5,colors.metal));
  if(kind==='molding'||kind==='package-functions'||kind==='package-height')out+=path('M95 185V126Q95 116 105 116H291Q303 116 303 126V185h-28v-48H123v48z','#cfbd9566');
  if(kind==='underfill')out+=rect(118,175,clamp(phase,0,4)*40,13,'#dbb88888',0,'none');
  if(kind==='package-functions')out+=path('M199 114V76m-6 7 6-7 6 7','none',colors.red,3)+text(221,76,'Heat',10)+path('M280 169h58v36','none',colors.metal,3)+text(304,224,'I/O',10)+text(84,103,'Protection',10);
  if(kind==='package-height')out+=dimension(352,117,352,216,'1.1 mm')+text(73,71,'.3 + .2 + .1 + .5 = 1.1 mm',11);
  if(kind==='bump')out+=text(112,85,'Pad → UBM → bump → joint',10);
 }return out;
}

function routeScene(spec,choice,done,lang){
 const l=v=>v[lang];const isPackage=spec.scene==='package-route';
 let out=rect(137,61,127,32,colors.glass,6)+text(200,81,isPackage?'Die + interfaces':'Integration requirements',10,colors.ink,'middle');
 out+=path('M200 93v19H94v18m106-18h106v18','none',colors.ink,2);
 const labels=isPackage?['Face-up / wirebond','Face-down / flipchip']:['Gate-first','Dummy → replacement'];
 [54,224].forEach((x,i)=>{const selected=choice===(isPackage?(i?'flip':'wire'):(i?'replacement':'gate-first'));out+=rect(x,131,125,43,selected?colors.green:colors.oxide,6)+text(x+62,157,labels[i],10,selected?'white':colors.ink,'middle')});
 out+=path('M115 176v27h84m84-27v27h-84','none',done?colors.green:'#9caea8',2,'4 3')+text(200,225,l(bi('只選一條相容路線；勿串接替代分支','Select a compatible branch; do not chain alternatives')),9,colors.ink,'middle');return out;
}
function sceneDrawing(spec,values,choice,phase,lang){
 if(spec.expansion)return renderExpansionScene(spec,values,choice,phase,lang);
 if(spec.scene.startsWith('itv11:'))return renderComputingVisual(spec.scene.slice(6),{zh:lang==='zh',focus:spec.visualFocus}).replace('<svg ','<svg x="16" y="40" width="368" height="219" ');
 if(spec.scene.startsWith('worldv11:')&&spec.worldCourse)return renderWorldVisual(spec.worldCourse,{zh:lang==='zh',focus:spec.visualFocus}).replace('<svg ','<svg x="16" y="40" width="368" height="219" ');
 if(spec.scene.startsWith('elev10:'))return renderElectronicsVisual(spec.scene.slice(7),{zh:lang==='zh',focus:spec.visualFocus}).replace('<svg ','<svg x="16" y="40" width="368" height="219" ');
 if(spec.scene.startsWith('packv9:'))return renderPackagingVisual(spec.scene.slice(7),{zh:lang==='zh'}).replace('<svg ','<svg x="16" y="39" width="368" height="219" ');
 if(spec.scene.startsWith('semiv8:'))return renderSemiconductorVisual(spec.scene.slice(7),{zh:lang==='zh'}).replace('<svg ','<svg x="16" y="48" width="368" height="198" ');
 const v7context=renderV7Context(spec.scene,phase,lang);if(v7context)return v7context;
 const context=renderExpansionContext(spec.scene,phase,lang);if(context)return context;
 const kind=spec.scene,zh=lang==='zh',label=v=>v[lang];let out='';
 if(['cmos','soi','epi','oxide','trench','etch','deposition','gate','contact','interconnect','nanosheet','tsv','cmp'].includes(kind))return crossSection(kind,phase);
 if(['dieattach','underfill','package-functions','package-height','hybrid','interposer','fanout','molding','hbm','bump','substrate','rdl','wirebond','handling','thinning'].includes(kind))return packageSection(kind,phase);
 if(kind==='route'||kind==='package-route')return routeScene(spec,choice,phase>=4,lang);
 if(kind==='mask-map'){
  out=waferBase();for(let a=0;a<4;a++)for(let b=0;b<3;b++){const x=137+a*33,y=91+b*38;out+=rect(x,y,23,18,'#87b89b')+rect(x+8,y-6,5,29,colors.poly)+rect(x-4,y+7,30,4,colors.metal)+circle(x+9,y+8,2,colors.ink)}
  out+=rect(302,89,14,11,'#87b89b')+text(322,99,'A Active',9)+rect(302,119,14,11,colors.ink)+text(322,129,'B Contact',9)+rect(302,149,14,11,colors.metal)+text(322,159,'C Metal',9)+text(82,234,zh?'同一座標系的圖層疊合':'Layer overlays in one coordinate frame',10);return out;
 }
 if(['particle-map','resistivity','notch','monitor','diameter','scratch'].includes(kind)){
  out=waferBase();
  if(kind==='particle-map'){out+=rect(212,74,45,47,'#df8c7733',3,colors.red)+dots([[219,87],[233,81],[228,100],[246,94],[239,110],[147,163],[173,116],[178,185]])+text(288,91,zh?'群聚':'Cluster',10)+line(258,99,285,92);}
  if(kind==='resistivity'){[0,1,2,3,4].forEach(i=>out+=circle(195,137,75-i*14,`rgba(74,133,163,${.08+i*.02})`,'#89a9b3'));out+=text(195,132,'10.0',13,colors.ink,'middle')+text(137,104,'9.5',10)+text(232,163,'10.5',10)+text(113,235,'(10.5 − 9.5) / 10 = 10%',11);}
  if(kind==='notch')out+=path('M195 208v20h92','none',colors.red,2)+text(296,232,'Notch',10)+rect(30,69,84,60,colors.paper,4)+text(39,87,'LOT RECORD',8)+text(39,105,'orientation',9)+text(39,120,'certificate ✓',9);
  if(kind==='diameter')out+=path('M112 73v124m166-124v124M112 81h166','none',colors.ink,4)+rect(157,61,76,22,'#294d4b',3)+text(195,77,'300 mm',13,'#fff','middle')+dimension(116,230,274,230,'Diameter = 300 mm');
  if(kind==='scratch')out+=path('M144 82L239 182M147 82L242 182','none',colors.red,2)+dots([[232,91],[152,183],[173,164],[250,125]])+text(148,75,'A',13,colors.red)+text(254,112,'B',13,colors.red);
  if(kind==='monitor')out+=rect(40, 66,87,37,colors.glass,5)+text(82,89,'Monitor',10,colors.ink,'middle')+rect(281,66,87,37,colors.oxide,5)+text(325,89,'Product',10,colors.ink,'middle')+path('M126 87l27 24m96 0 33-24','none',colors.ink,2)+text(85,238,'Separate labels / correlated evidence',10);
  return out;
 }
 if(['ttv','warp','flatness','roughness','edge'].includes(kind)){
  out=line(47,199,357,199,'#9fb1a9')+line(47,65,47,209,'#9fb1a9');
  if(kind==='ttv'){
   const sample=[775,772,778,774,776];out+=path('M66 145L126 153L187 137L247 148L309 141V180H66z',colors.si)+line(60,180,322,180,colors.ink,2);
   sample.forEach((v,i)=>out+=line(67+i*60, 87,67+i*60,132,colors.red,1,'3 3')+text(67+i*60,76,String(v),10,colors.ink,'middle'));
   out+=text(103,228,'max 778 − min 772 = 6 µm',11);
  }else if(kind==='warp'){
   out+=path('M66 110Q195 49 331 110','none',colors.si,5)+path('M66 163Q127 111 194 163T331 162','none',colors.poly,5)+text(60,92,'A  Bow',11)+text(60,143,'B  Warp',11)+line(60,111,335,111,colors.red,1,'4 4')+line(60,164,335,164,colors.red,1,'4 4');
  }else if(kind==='flatness'){
   out+=rect(83,87,234,95,'#b8d4cf55')+path('M84 147L118 121L151 139L187 111L220 159L253 122L282 135L316 127','none',colors.si,4)+line(80,136,325,136,colors.red,1,'4 3')+text(189,102,'+0.8',10,colors.red)+text(220,175,'−1.0',10,colors.red)+text(99,228,'PV = 0.8 − (−1.0) = 1.8 µm',10);
  }else if(kind==='roughness'){
   out+=path('M70 137l29-36 29 72 29-72 29 72 29-72 29 72 29-72 29 36','none',colors.si,3)+line(61,137,334,137,colors.red,1,'4 4')+text(79,84,'+0.6 nm',10)+text(91,194,'−0.6 nm',10)+text(208,229,'Rq = 0.6 nm',11);
  }else{
   out+=path('M64 111q13-15 34-15h75v53H98q-23 0-34-15z',colors.si)+path('M228 96h74q20 0 31 15l-18 10 17 13q-11 15-32 15h-72z',colors.si)+circle(320,122,24,'none',colors.red)+text(91,175,'A  intact',11)+text(255,175,'B  chip',11);
  }return out;
 }
 if(['spectrum','contamination','repeatability','quality-chart','hall'].includes(kind)){
  if(kind==='hall')return rect(131,105,139,58,colors.si)+path('M77 134h53m140 0h55M199 59v43m-9-11 9 11 9-11','none',colors.ink,3)+text(83,124,'I →',13)+text(215,74,'B',14)+text(195,201,'R_H = −1 (normalized)',12,colors.ink,'middle')+line(144,102,144,75,colors.red)+line(252,103,252,75,colors.red)+text(199,80,'Hall sign',9,colors.red,'middle');
  out=line(55,195,346,195)+line(55,70,55,195);
  if(kind==='spectrum'){
   const shift=(Number(values.reading??1)-2)*14;
   out+=path(`M66 ${173+shift}Q116 ${84+shift} 169 ${126+shift}T328 ${96+shift}`,'none',colors.si,3)+[[80,151],[130,121],[177,130],[230,139],[284,120],[323,99]].map(([x,y])=>circle(x,y,3,'none',colors.red)).join('')+text(78,225,'Model thickness / illustrative signals',10);
  }else if(kind==='contamination'){
   ['Fe','Cu','Ni'].forEach((v,i)=>{const x=97+i*85;out+=rect(x,183,18,12,colors.oxide)+rect(x+22,i?178:102,18,i?17:93,colors.red)+text(x+18,214,v,11,colors.ink,'middle')});out+=text(221,77,'Blank / sample',10);
  }else if(kind==='repeatability'){
   [100,100.2,100.4].forEach((v,i)=>{const x=106+i*82,y=164-i*27;out+=circle(x,y,6,colors.si)+text(x,y-13,v.toFixed(1),11,colors.ink,'middle')});out+=line(78,137,326,137,colors.red,1,'5 3')+text(87,225,'mean 100.2 / range 0.4',11);
  }else{
   [120,60,35,16].forEach((v,i)=>out+=rect(80+i*61,195-v,39,v,i?colors.si:colors.red)+text(100+i*61,212,['A','B','C','D'][i],10,colors.ink,'middle'));
   out+=text(94,66,'Pass: 60 / total: 80 = 75%',11);
  }return out;
 }
 if(kind==='crystal-defect'){
  for(let y=0;y<6;y++)for(let x=0;x<9;x++){const xx=89+x*27+(y>2&&x>4?10:0);out+=circle(xx,75+y*24,3.5,colors.si)}
  out+=path('M207 64v64m-16 0h32','none',colors.red,3)+circle(207,134,22,'none',colors.red)+text(227,130,'⊥',19,colors.red)+text(85,231,'Extra half-plane termination',11);return out;
 }
 if(kind==='foup'){
  out=rect(80,64,132,164,'#bad0c455',12)+rect( 91,74,110,141,colors.paper,4);
  for(let i=0;i<6;i++){const y=91+i*22;out+=line(98,y,190,y,colors.ink,1.5)+text(72,y+4,String(i+1),11,colors.ink,'end')+(i===3?path(`M112 ${y-5}h70`,'none',colors.red,1.5):rect(105,y-5, 81,5,colors.si))}
  out+=text(233,92,'Record / sensed',11)+[1,2,3,4,5,6].map((n,i)=>text(242,116+i*18,`${n}:  1 / ${n===4?'0   !':'1'}`,11,n===4?colors.red:colors.ink)).join('');return out;
 }
 if(kind==='registration'){
  const dx=3+Number(values.dx??0),dy=2+Number(values.dy??0);
  out=rect(73,73,250,143,colors.paper,5)+line(87,93,309,93,'#b7c8bb',1,'3 3')+line(87,194,309,194,'#b7c8bb',1,'3 3');
  [[115,106],[277,106],[115,180],[277,180]].forEach(([x,y])=>{out+=path(`M${x-8} ${y}h16M${x} ${y-8}v16`,'none',colors.si,2)+path(`M${x-8+dx*7} ${y+dy*7}h16M${x+dx*7} ${y-8+dy*7}v16`,'none',colors.red,2)});
  out+=text(88,236,zh?'綠：基準；橘：經修正後的量測':'Green: reference; orange: corrected measurement',9);return out;
 }
 if(kind==='disposition'){
  ['Identity','Dimensions','Contamination','Documentation'].forEach((v,i)=>out+=rect(73,66+i*38,251,30,i===2?'#e6c48e':'#c7ddcb',4)+text(87,86+i*38,v,11)+text(298,86+i*38,i===2?'?':'✓',15,i===2?colors.red:colors.green,'middle'));
  return out+text(83,239,'Unknown ≠ pass / hold for evidence',10);
 }
 if(kind==='io-map'){
  out=rect(145,92,111,94,colors.si,3)+text(201,137,'DIE',14,'#fff','middle');
  for(let i=0;i<8;i++){out+=rect(155+i*12,79,7,10,colors.metal)+rect(155+i*12,188,7,10,colors.metal);if(i<6)out+=rect(132,103+i*12,10,7,colors.metal)+rect(258,103+i*12,10,7,colors.metal)}
  return out+text(61,61,'Signal 64 + power 16 + ground 16',11)+text(201,226,'96 terminals (example)',13,colors.ink,'middle');
 }
 if(kind==='substrate-choice')return block(52,149,117,24,colors.metal)+path('M52 149H35m134 0h17','none',colors.metal,9)+[0,1,2,3].map(i=>rect(218,105+i*22,135,18,i%2?colors.glass:colors.oxide)+line(225,113+i*22,345,113+i*22,colors.metal,3)).join('')+text(55,210,'A Leadframe',11)+text(235,210,'B Build-up',11);
 if(kind==='growth')return path('M121 167q76 54 158 0v-30H121z','#b78766')+path('M132 140q68-25 136 0q-60 20-136 0',colors.resist)+rect(174,85,54,52,colors.si)+path('M174 85l15-25h24l15 25z',colors.si)+rect(196, 42,12,19,colors.si)+line(202,26,202,41,colors.ink,3)+path('M309 96v73m-6-10 6 10 6-10','none',colors.red,2)+text(73,221,'Seed / neck / shoulder / crystal / melt',10);
 if(kind==='cleaning')return rect(72,116,253,95,colors.oxide,6)+path('M84 131h229','none',colors.si,2)+path('M131 178l90-46 54 22-90 46z',colors.si)+dots(phase<3?[[147,167],[174,165],[198,146],[224,161],[181,183]]:[[147,167]])+path('M105 86l17 25m16-33 16 32m101-30-12 32m40-24-17 25','none',colors.oxide,3)+text(83,236,zh?'移除前後應使用同一量測基準':'Compare before/after on the same measurement baseline',9);
 if(kind==='implantation')return crossSection('oxide',phase)+[112,152,192,232,272].map(x=>path(`M${x} 63l16 42m-7-5 7 5 1-9`,'none',colors.red,2)).join('')+path('M100 193q55 0 75-25q21-34 45 0q20 25 78 25','none',colors.metal,3)+text(103, 80,'Normalized profile; no implant recipe',9);
 if(kind==='dicing'){
  out=rect( 80, 75,240,137,colors.oxide,5);for(let i=0;i<3;i++)for(let j=0;j<2;j++)out+=rect(91+i*77,88+j*57, 65,45,colors.si,2);
  return out+line(165,65,165,224,colors.red,2,'5 4')+text( 80,240,'Streets / 6 dies / support tape',10);
 }
 if(kind==='lithography'){
  out=rect(76,179,250,27,colors.si)+rect(76,162,250,17,colors.resist)+rect(107,66,188,14,colors.ink)+[130,179,228,270].map(x=>rect(x,65,15,16,colors.paper)).join('');
  if(phase>0)out+=[137,186,235,277].map(x=>path(`M${x} 84l-14 70h28z`,'#d6b66450',colors.metal,1)).join('');
  if(phase>=3)out+=[125,175,225,275].map(x=>rect(x,160,18,19,colors.paper,0,colors.paper)).join('');
  return out+text(105,51,'Mask openings',11)+text(86,228,'Mask → exposure → resist image',10);
 }
 if(['optics','reflective','photonics'].includes(kind)){
  if(kind==='reflective')return rect(37,111,36,34,colors.metal,5)+text(55,161,'EUV',10,colors.ink,'middle')+path('M74 129L141 80L215 161L294 89L348 152','none',colors.poly,3)+[ [141,80,-35],[215,161,35],[294,89,-35] ].map(([x,y,r])=>`<g transform="translate(${x} ${y}) rotate(${r})">${rect(-22,-3,44,6,colors.si,2)}${line(-22,6,22,6,colors.metal,2)}</g>`).join('')+line(350,128,350,183,colors.ink,3)+text(117,224,'Reflective interfaces, not transmissive lenses',10);
  if(kind==='photonics')return rect(60, 80,285,121,colors.si,7)+path('M76 160h251M77 124h101m41 0h108','none',colors.metal,4)+circle(200,122,28,'none',colors.metal)+rect(88,146,41,28,colors.poly,4)+rect(278,146,32,28,colors.resist,4)+text(81,228,'Waveguide / ring / modulator / detector',10);
  return rect(41,113,33,34,colors.metal,4)+path('M178  70q-25 58 0 119q25-61 0-119z','#a3ced780')+line(308,69,308,210,colors.ink,3)+path('M76 129L175 93L308 143M76 129H308M76 129L175 173L308 143','none',colors.red,2)+text(88,234,'Illustrative rays / object / image plane',10);
 }
 if(kind==='electrical')return line(84,153,84, 93,colors.ink,2)+line(75,126,93,126,colors.ink,4)+line(79,136,89,136,colors.ink,2)+path('M84 93h49m63 0h42m63 0h23v90H84v-30','none',colors.ink,2)+rect(134,82,61,22,colors.metal,3)+rect(239,82,61,22,colors.metal,3)+text(165, 72,'1 a.u.',11,colors.ink,'middle')+text(269,72,'2 a.u.',11,colors.ink,'middle')+circle(199,183,20,colors.paper)+text(199,189,'Σ = 3',11,colors.ink,'middle');
 if(kind==='thermal')return rect(60,143,68, 50,colors.resist,6)+text(94,173,'Q = 3',11,colors.ink,'middle')+line(129,166,168,166,colors.red,4)+rect(169,139, 70, 50,colors.glass,5)+text(204,169,'R = 2',11,colors.ink,'middle')+line(240,166,277,166,colors.red,4)+rect(278,112,45, 90,colors.si)+[0,1,2,3].map(i=>rect(325,119+i*20, 30,7,colors.si)).join('')+text(116,87,'ΔT = Q · R = 6 a.u.',13)+text(112,227,'Defined ambient boundary required',10);
 return infrastructureScene(kind,phase,lang);
}


function infrastructureScene(kind,phase,lang){
 const zh=lang==='zh';let out='';
 if(kind==='bridge'){
  out=path('M25 217q80-23 161-4t190-4','none','#9bbcb9',16)+rect(47,174,307,13,colors.si)+path('M173 174L190 68l20 106M186 186v42m21-42v42','none',colors.ink,9);
  [70,110,150,241,282,324].forEach(x=>out+=line(195,82,x,173,colors.metal,2));
  return out+path('M284 106v39m-5-8 5 8 5-8','none',colors.red,3)+text(240, 89,'Deck load',11)+text(42,247,'Deck → stays → pylon → foundation',10);
 }
 if(kind==='tunnel'){
  out=path('M36 80h332v135H36z','#cfc2a3')+path('M36 113h332M36 151h332','none','#a19578',5)+path('M92 215v-79a107  70 0 0 1 215 0v79',colors.paper,colors.si,17)+path('M102 216v-79a98  62 0 0 1 195 0v79','none',colors.ink,2);
  out+=path('M126 150h44m-9-5 9 5-9 5M270 150h-44m9-5-9 5 9 5','none',colors.red,2)+text(121,178,'2',12)+text(264,178,'3',12)+text(159,236,'Convergence = 5 a.u.',10);return out;
 }
 if(kind==='network'){
  out=rect(43, 83,97,117,'#b9d4c360',7)+rect(258,83,99,117,'#dccbb760',7)+rect(166,112,68,63,colors.si,6)+text(200,147,'POLICY',10,'#fff','middle');
  [[63,98,'Client'],[63,155,'Identity'],[275,98,'Service'],[275,155,'Data']].forEach(([x,y,v])=>out+=rect(x,y, 63,29,colors.glass,4)+text(x+31,y+19,v,10,colors.ink,'middle'));
  return out+path('M126 112h39m69 0h40M126 172h39m69 0h40','none',colors.metal,3)+text(70,229,zh?'驗證每次存取；沒有隱含信任':'Verify each access; no implicit trust',11);
 }
 if(kind==='aircraft'){
  out=path('M55 138l89-18 57-64h24l-17 68 133 15-132 16 31 58h-24l-72-57-89-7z','#82a496')+path('M147 135l153 8M173 117l27-33M184 158l25 34','none',colors.ink,3);
  out+=path('M196 92l-24 43M297 143l-43-4M195 192l-26-40','none',colors.red,2);
  return out+text(78,236,'Public load-path principles only',11);
 }
 if(kind==='rotor'){
  out=rect(151,128,119,58,'#91ac9d',19)+path('M150 145l-64-5-24-20h-10l14 44 85 3','none',colors.ink,4)+line(209,128,209,93,colors.ink,6)+line(88,89,332,89,colors.si,9)+path('M154 197h104M168 183l-8 14m87-14 9 14','none',colors.ink,4);
  return out+path('M55  52q45-30  90 0t90 0t90 0','none',colors.red,2)+text( 80,237,'Energy / rotor / vibration sensing',11);
 }
 if(kind==='buoyancy'){
  out=rect(30,88,342,137,'#b3d1d965',0,'none')+path('M32 91q42-12 84 0t84 0t84 0t84 0','none',colors.si,2)+`<ellipse cx="200" cy="153" rx="101" ry="45" fill="#91a9a5" stroke="${colors.ink}" stroke-width="2"/>`;
  out+=path('M192 151v-50m-6 10 6-10 6 10M209 155v49m-6-10 6 10 6-10','none',colors.red,3)+circle(193,151,4,colors.oxide)+circle(209,154,4,colors.metal)+text(226,118,'B',13)+text(225,200,'W',13);
  return out+text(86,244,'Civilian buoyancy model / B − W = 0',10);
 }
 if(kind==='piston'){
  out=rect(44,102,134,80,colors.glass,5)+rect(62+phase*8,112,22, 60,colors.si)+path(`M${84+phase*8} 141h67l126 26`,'none',colors.metal,8)+circle(289,169,45,'none',colors.si)+line(289,169,277,167,colors.ink,5)+circle(277,167,7,colors.red)+circle(289,169,5,colors.ink);
  return out+dimension( 60,212,167,212,'stroke = 2r')+text(64, 70,'Cylinder → connecting rod → crank',11);
 }
 if(kind==='battery'){
  out=rect(61, 100,222, 90,colors.glass,7);
  [81,146,211].forEach((x,i)=>out+=rect(x,116,49, 60,colors.si,5)+rect(x+15,109,19,7,colors.metal)+text(x+25,151,'1',13,'white','middle')+line(x+25,104,x+25, 70,colors.red,1,'3 3'));
  out+=rect(296,119, 63,55,colors.poly,5)+text(328,150,'BMS',12,'#fff','middle')+path('M106  70h222v48','none',colors.red,1.5)+text(78,229,'Normalized cells / monitoring / isolation',10);return out;
 }
 if(kind==='satellite'){
  out=rect(166,91,74,64,colors.metal,2)+path('M166 91l19-13h75l-20 13M240 91l20-13v64l-20 13',colors.metal)+rect( 80, 95, 60,55,colors.si)+rect(272,95,60,55,colors.si)+line(140,121,166,121,colors.ink,4)+line(240,121,272,121,colors.ink,4);
  [91,104,117,283,296,309].forEach(x=>out+=line(x,98,x,148,colors.oxide));
  out+=path('M189 159L114 214M220 159l75  50','none',colors.red,2,'4 3')+rect(79,214, 65,17,colors.glass)+rect(270,211,65,17,colors.glass)+text( 91,250,'Ground A',9)+text(282,246,'Ground B',9);return out;
 }
 if(kind==='dam'){
  out=rect(37,105,126,102,'#a3c8d4',0,'none')+path('M162  75h35l70 137H138z','#a7ad9b')+path('M33 214h338','none','#9e9275',9)+path('M114 172h129q34 0 34  30','none',colors.si,10)+circle(283,191,23,colors.metal)+path('M283 174v34m-17-17h34','none',colors.ink,2)+text(53, 91,'Head',12)+text(271,235,'Turbine',11);
  return out+path('M71 139h52m-8-5 8 5-8 5','none',colors.red,2);
 }
 if(kind==='vehicle'||kind==='rail'){
  out=path(kind==='rail'?'M65 155V 95q0-14 16-14h251v74z':'M 60 160v-40l55-15 35-38h116l39 40 34 15v38z',colors.si)+rect(132, 83,117,38,colors.oxide,3)+line(196,83,196,160,colors.ink,2)+circle(115,169,26,'#365650')+circle(289,169,26,'#365650')+circle(115,169,13,colors.glass)+circle(289,169,13,colors.glass)+rect(155,170,92,20,colors.metal,4)+line(43,201,357,201,colors.ink,3);
  return out+text( 80,234,kind==='rail'?'Body / bogies / traction / braking':'Body / suspension / power / cooling',10);
 }
 const contextual=extendedContextScene(kind,phase,lang);if(contextual)return contextual;
 // Functional fallback is a requirements/interface diagram, never a generic part.
 return rect(49,98, 90, 60,colors.glass,5)+rect(159,98,90,60,colors.oxide,5)+rect(269,98, 90,60,colors.metal,5)+text(94,132,'Input',12,colors.ink,'middle')+text(204,132,'Interface',12,colors.ink,'middle')+text(314,132,'Evidence',12,colors.ink,'middle')+line(139,129,159,129,colors.ink,2)+line(249,129,269,129,colors.ink,2)+text(72,216,'Requirements / dependencies / acceptance',11);
}

function assemblyPiece(scene){
 if(scene==='cmos')return rect(-30,-5,60,10,colors.metal)+rect(-20,5,10,17,colors.metal)+rect(10,5,10,17,colors.metal);
 if(scene==='handling')return path('M-49 0h31v8h36V0h31v14H-49z',colors.metal);
 if(scene==='wirebond')return path('M-40 6Q0-60 40 6','none',colors.metal,5);
 if(scene==='bridge')return block(-40,-7,80,14,colors.si);
 if(scene==='tunnel')return path('M-31 16V0a31 25 0 0 1 62 0v16h-7V0a24 18 0 0 0-48 0v16z',colors.si);
 if(scene==='optics'||scene==='reflective')return path('M-31 9l 50-25 8 10-50 25z',colors.si);
 if(scene==='piston')return line(-30,0,30,0,colors.metal,8)+circle(-30,0,8,colors.metal)+circle(30,0,8,colors.metal);
 if(scene==='bump')return [ -24,0,24 ].map(x=>circle(x,0,8,colors.metal)).join('');
 if(scene==='interconnect'||scene==='rdl')return path('M-35-10h25v20h20v-20h25','none',colors.metal,6);
 return block(-30,-13,60,26,colors.si)+[ -20,0,20 ].map(x=>circle(x,17,3,colors.metal)).join('');
}
export function renderExerciseSvg({course={},step={},state={},mentor=false,labels={}}={}){
 const spec=resolveExercise(course,step);
 const lang=String(labels.language||'').startsWith('zh')||(!labels.language&&/[\u3400-\u9fff]/.test(labels.aria||''))?'zh':'en';
 const exercise=state.exercise||state||{};
 const values=Object.fromEntries(spec.controls.map(c=>[c.id,mentor&&!labels.demoState?c.target:clamp(exercise.values?.[c.id]??c.initial,c.min,c.max)]));
 const choice=mentor&&!labels.demoState?spec.expectedChoice:exercise.choice;
 const phase=spec.controls.some(c=>c.id==='phase')?Number(values.phase):(mentor&&!labels.demoState)||spec.mode!=='process'?4:exercise.performed?4:0;
 const uid=`scene-${String(step.id||spec.id).replace(/[^a-zA-Z0-9_-]/g,'')}-${mentor?'reference':'learner'}`;
 let drawing=sceneDrawing(spec,values,choice,phase,lang);
 if(spec.focus)drawing+=focusInset(spec.focus,lang);
 const pose=state.pose||{};
 if(spec.mode==='assembly'){
  const position=mentor&&!labels.demoState?spec.target:pose;
  const x=200+clamp(position.x??-86,-130,130)+clamp(position.y??50,-80,80)*.42;
  const y=181+clamp(position.y??50,-80,80)*.43-(clamp(position.z??30,0,65)-8)*1.3;
  drawing+=`<g transform="translate(200 181)" opacity=".35" stroke-dasharray="3 3">${assemblyPiece(spec.scene)}</g><g id="${mentor?'mentorTool':'activePiece'}" transform="translate(${x} ${y}) rotate(${clamp(position.rotation??-24,-180,180)})" style="cursor:${mentor?'default':pose.grabbed?'grabbing':'grab'}">${assemblyPiece(spec.scene)}</g>`;
 }else if(!mentor||labels.demoState){
  // Tool motion is visible, but evidence is checked by the task-specific controls.
  const x=200+clamp(pose.x??-86,-130,130)+clamp(pose.y??50,-80,80)*.42,y=144+clamp(pose.y??50,-80,80)*.43-(clamp(pose.z??30,0,65)-8)*1.3;
  drawing+=`<g id="${mentor?'mentorTool':'activePiece'}" transform="translate(${x} ${y}) rotate(${clamp(pose.rotation??0,-180,180)})" style="cursor:${pose.grabbed?'grabbing':'grab'}">${circle(0,0,13,'#ffffffa8',colors.red)}${line(-20,0,20,0,colors.red)}${line(0,-20,0,20,colors.red)}${line(13,-13,29,-29,colors.red,3)}</g>`;
 }
 const badge=spec.mode.toUpperCase();
 const modeLabel=mentor?(labels.demoState?(lang==='zh'?'師傅：逐步示範':'MENTOR: DEMONSTRATION'):(lang==='zh'?'師傅：驗證目標':'MENTOR: TARGET')):(lang==='zh'?'學徒：操作與證據':'LEARNER: ACTION + EVIDENCE');
 let footer=spec.sampleMetric?`${spec.sampleMetric[lang]} = ${spec.sampleTarget} ${spec.sampleUnit}`:mentor?spec.evidence[lang]:spec.tool[lang];
 const footerLimit=lang==='zh'?40:72;
 if(footer.length>footerLimit)footer=footer.slice(0,footerLimit-2)+'…';
 const phasebar=spec.mode==='process'||spec.controls.some(c=>c.id==='phase')?Array.from({length:spec.controls.find(c=>c.id==='phase')?.max||4},(_,i)=>rect(81+i* 40,276,32,5,i<phase?colors.green:'#cfdbd2',2,'none')).join(''):'';
 return `<svg viewBox="0 0 400 304" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="${esc(`${modeLabel}: ${spec.object[lang]}`)}" data-exercise="${esc(spec.id)}" data-scene="${esc(spec.scene)}"><defs><linearGradient id="${uid}" x2="0" y2="1"><stop stop-color="#f5f8ee"/><stop offset="1" stop-color="#e7efe2"/></linearGradient></defs>${rect(0,0,400,304,`url(#${uid})`,8,'none')}${text(15, 19,modeLabel,9,'#64826c')}${text(385,19,badge,9,'#64826c','end')}${text(15,39,spec.object[lang],12,colors.ink)}${drawing}${rect(0,255,400, 49,'#edf3e6',0,'none')}${text(12,270,footer,8.5)}${phasebar}${text(12,296,lang==='zh'?'原創教學示意 · 數值為示例，非量產規格':'ORIGINAL TEACHING SCHEMATIC · EXAMPLE VALUES, NOT FACTORY LIMITS',7.5,'#738471')}</svg>`;
}


function extendedContextScene(kind,phase,lang){
 let out='';
 if(kind==='materials'){
  out=rect( 45,81, 90,115,'#bfc9b5',4)+rect(156,81,90,115,'#c0d3d5',4)+rect(266,81,90,115,'#d2beaa',4);
  [[54,95],[80,98],[108,113],[ 63,142],[ 95,170]].forEach(([x,y])=>out+=path(`M${x} ${y}l18-8 13 19-20 17-11-28z`,'none',colors.si));
  for(let i=0;i<7;i++)out+=line(162,92+i*13,240,92+i*13,colors.si,3)+line(275+i*11,88,275+i*11,189,colors.oxide,2);
  return out+text(51,220,'Grains',11)+text(168,220,'Fibers',11)+text(277,220,'Laminate',11);
 }
 if(kind==='inspection-plan')return rect(65,91,267,116,colors.glass,8)+[ [93,117],[297,119],[113,179],[286,183] ].map(([x,y],i)=>circle(x,y,15,'#f2f6ec',colors.red)+text(x,y+4,String(i+1),12,colors.red,'middle')).join('')+path('M111 117h169M112 134v27m17 19h139','none',colors.si,2)+text(79, 70,'Access → inspect → record → compare',11);
 if(kind==='vibration'||kind==='monitoring')return line(60,200,349,200)+line(60,70,60,200)+path(kind==='vibration'?'M67 194h55l14-104 14 104h65l13-60 13 60h98':'M65 168l 22-7 20 10 22-6 22 5 23-84 23 85 22-11 22 13 22-10 22 5','none',kind==='vibration'?colors.si:colors.red,3)+text(89,230,kind==='vibration'?'Frequency / amplitude / sampling':'Time / event / alert context',11);
 if(kind==='powertrain'){
  out=line( 60,149,105,149,colors.ink,5)+line(278,149,340,149,colors.ink,5);
  [[143,149,40],[235,149,52]].forEach(([x,y,r])=>{out+=circle(x,y,r,'#b9cba6')+circle(x,y,12,colors.metal);for(let i=0;i<12;i++){const a=i*Math.PI/6;out+=line(x+Math.cos(a)*(r-7),y+Math.sin(a)*(r-7),x+Math.cos(a)*(r+6),y+Math.sin(a)*(r+6),colors.ink,5)}});
  return out+text(65,79,'Torque / speed / transfer efficiency',11)+text(75,233,'Input → gears → output / losses',11);
 }
 if(kind==='safety')return rect( 60,95, 90, 70,'#e6b9a3',6)+rect(176,95,55,70,colors.metal,3)+rect(257,95,90,70,colors.glass,6)+text(105,134,'Hazard',12,colors.ink,'middle')+text(204,134,'STOP',11,colors.ink,'middle')+text(302,134,'Protected',11,colors.ink,'middle')+line(150,130,176,130,colors.red,3)+line(231,130,257,130,colors.green,3)+text(65,214,'Detect → isolate → verify / unknown ≠ pass',10);
 if(kind==='pressure'){
  out=`<ellipse cx="200" cy="145" rx="95" ry="65" fill="#c1d5d4" stroke="${colors.ink}" stroke-width="8"/>`;
  [[200,58,200, 80],[200,235,200,210],[66,145,103,145],[334,145,296,145]].forEach(([x,y,a,b])=>out+=line(x,y,a,b,colors.red,3)+circle(a,b,3,colors.red));
  return out+text(138,143,'External pressure',11)+text(116,254,'Direction ≠ structural qualification',10);
 }
 if(kind==='site'||kind==='geology'||kind==='groundwater'){
  for(let i=0;i<4;i++)out+=path(`M42 ${87+i* 30}q 80-22 155 0t160 0v 30q-80 22-160 0t-155 0z`,['#c2d5ad','#d6c899','#bca68f','#9caaa1'][i]);
  if(kind==='site')out+=path('M91 90l190 86','none',colors.red,3)+circle(91,90,8,colors.glass)+circle(281,176,8,colors.glass)+text(110,232,'Site alternatives / terrain / constraints',10);
  else out+=path('M217  70l-60 155','none',colors.red,3)+path('M57 127q100-20 285 3','none',colors.oxide,5)+text( 80,233,'Strata / discontinuity / groundwater',10);
  if(kind==='groundwater')out+=path('M117 114l42 28 47-13 58  30','none','#467f9c',3);
  return out;
 }
 if(kind==='corrosion')return rect(65,161,270, 40,colors.si)+rect(65,146,270,15,colors.metal)+path('M65 146v-22h105l15 22 14-22h136v22z',colors.oxide)+path('M184  90v 40m-7-9 7 9 7-9','none',colors.red,3)+dots([[185,153],[177,163],[196,170],[202,154]])+text(99,225,'Coating breach / exposed interface',11);
 if(kind==='ventilation')return path('M56 210v-90a144  60 0 0 1 288 0v90',colors.paper,colors.si,12)+circle(104,125,20,colors.glass)+circle(296,125,20,colors.glass)+path('M84 125h40m-20-20v40m172-20h40m-20-20v40','none',colors.ink,3)+path('M128 137h 80m-10-6 10 6-10 6m25-6h39','none',colors.oxide,5)+line(76,206,325,206,colors.ink,3)+text(85,241,'Flow direction / sensors / operational states',10);
 if(['asset-map','identity','software','backup'].includes(kind)){
  const labels={ 'asset-map':['Device','Service','Data'],identity:['User + MFA','Policy','Resource'],software:['Version A','Validate','Version B'],backup:['Source','Isolated copy','Restore + check']}[kind];
  [42,158,274].forEach((x,i)=>out+=rect(x,104,89,72,[colors.glass,colors.oxide,colors.metal][i],7)+text(x+45,145,labels[i],i===2&&kind==='backup'?9:10,colors.ink,'middle'));
  out+=line(131,140,158,140,colors.ink,2)+line(247,140,274,140,colors.ink,2);
  if(kind==='software'||kind==='backup')out+=path('M320 178v34H 80v-32','none',colors.green,2)+text(158,235,kind==='software'?'Recovery path':'Verify recovered data',10);
  else out+=text(79,220,kind==='identity'?'Authentication ≠ authorization':'Ownership / boundary / information class',10);return out;
 }
 if(kind==='boiler')return rect(91,89,205,113,colors.glass, 22)+path('M109 137h167v48H109z','#b5d6df')+path('M117 173h20v-52h24v52h24v-52h24v52h24v-52h24v52','none',colors.metal,4)+path('M274 89V 60h47','none',colors.si,9)+text(112,230,'Heat → phase change + losses',11);
 if(kind==='braking')return circle(125,145,51,colors.si)+circle(125,145,25,colors.metal)+rect(71,132,22,26,colors.red)+path('M178 132l73-43m-73  70 73 43','none',colors.ink,3)+text(259,92,'Heat',12,colors.red)+rect(256,177,77,31,colors.green,4)+text(295,198,'Recovery',10,'#fff','middle')+text(82,239,'Kinetic energy → conversion',11);
 if(kind==='suspension')return rect( 70, 70,260, 30,colors.si,7)+line( 70,214,330,214,colors.ink,5)+path('M126  100v12l-15 10 30 13-30 13 30 13-30 13 30 13-15 10v17','none',colors.metal,3)+rect(242,126,22,60,colors.glass)+line(253,100,253,155,colors.ink,5)+line(253,186,253,214,colors.ink,5)+text(85,239,'Spring: store / damper: dissipate',11);
 if(kind==='orbit')return circle(200,156, 60,'#97c1bd')+path('M151 112l28 12-7 27 27 7 11 39 29-14 14-40-36-19z','#72977c')+`<ellipse cx="200" cy="156" rx="148" ry=" 75" transform="rotate(-22 200 156)" fill="none" stroke="${colors.ink}" stroke-dasharray="5 4"/>`+rect(302,82,26,22,colors.metal)+path('M303  100l-87  22','none',colors.red,2)+text( 60,250,'Orbit / line of sight / ground location',10);
 if(kind==='antenna'){
  out=line( 60,188,334,188,colors.ink,3);for(let i=0;i<5;i++){const x=91+i*48;out+=line(x,188,x,148,colors.si,5)+path(`M${x-8} 139q8-10 16 0M${x-15} 132q15-20 30 0`,'none',colors.oxide,2)}
  return out+path('M94 120Q190 45 325 111','none',colors.red,3)+text(82, 70,'Relative phase → interference pattern',10)+text(85,232,'Array geometry / phase / amplitude',10);
 }
 if(kind==='hydrology')return path('M 40 128l60-63 42 47 52-72 61 96 41-47  60 54v 50H40z','#b4c2a3')+path('M101 82l19 58 65 25  70-24 51  30','none',colors.oxide,9)+rect(153,180,120,36,'#7facbd',8)+path('M218 180v-40m-6 10 6-10 6 10','none',colors.red,2)+text(79,244,'Storage change = inflow − outflow (+ other terms)',9);
 if(kind==='turbine')return path('M45 105h123v80h 90','none',colors.oxide,18)+circle(258,185, 40,colors.si)+[0,1,2,3,4,5].map(i=>{const a=i*Math.PI/3;return line(258,185,258+Math.cos(a)*31,185+Math.sin(a)*31,colors.metal,8)}).join('')+line(298,185,341,185,colors.ink,6)+rect(329,165, 40,40,colors.glass,5)+text(75,234,'Hydraulic → mechanical → electrical',11);
 if(kind==='lock')return rect( 40, 90,320,115,colors.glass)+rect( 40,121, 90,84,colors.oxide)+rect(145,151,110,54,colors.oxide)+rect(270,177, 90,28,colors.oxide)+rect(130, 80,15,125,colors.si)+rect(255, 80,15,125,colors.si)+path('M163 132h69l-13 15h-43z',colors.metal)+text(68,240,'Upstream / chamber / downstream',11);
 if(kind==='doors')return rect(83, 70,235,144,colors.si,9)+rect(120,91, 60,113,colors.glass,4)+rect(221,91, 60,113,colors.glass,4)+rect(130,106,40,42,colors.oxide)+rect(231,106,40,42,colors.oxide)+path('M171 169h-28m10-6-10 6 10 6M229 169h28m-10-6 10 6-10 6','none',colors.red,2)+text(83,239,'Physical state / sensed state / permission',10);
 if(kind==='coupling')return rect(49,129,106,32,colors.oxide)+rect(257,129,95,32,colors.si)+path('M94 184q49 0 69-81q22-72 48 8q23 74 80 74','none',colors.red,3)+path('M94 184q49 0 73-60q31-52 55 10q24 50  70 50','none',colors.metal,2)+text(69,226,'Mode overlap / position / angle / shape',10);
 if(kind==='resonator')return circle(153,136, 50,'none',colors.metal)+line( 50,196, 250,196,colors.metal,4)+path('M278  80v114h88M284 118h21q9  70 17 0h34','none',colors.si,2)+text( 90,239,'Ring coupling / spectral response',10);
 if(kind==='backside-power')return rect(66, 90,271,113,colors.si)+rect(66,78,271,12,colors.metal)+rect(66,204,271,17,colors.metal)+[113,195,278].map(x=>rect(x,126, 14,78,colors.oxide)+rect(x+4,130,6,78,colors.metal)).join('')+text( 90, 66,'Front-side signal routing',11)+text( 90,244,'Backside power delivery / isolation',11);
 return '';
}
function focusInset(focus,lang){
 const type=focus.type;let drawing='';
 if(type==='layers')drawing=[0,1,2].map(i=>rect(9,10+i*8, 60,6,[colors.si,colors.oxide,colors.metal][i])).join('');
 else if(type==='wave')drawing=path('M5 23q8-22 16 0t16 0t16 0t16 0','none',colors.red,2);
 else if(type==='force')drawing=rect( 22,7, 30, 30,colors.glass)+path('M5  22h14m37 0h 14M37 1v6m0 30v6','none',colors.red,2);
 else if(type==='alignment')drawing=path('M13 23h49M37 6v 30','none',colors.si,2)+path('M19 27h49M43 10v30','none',colors.red,2);
 else if(type==='thermal')drawing=rect(5,15,16,16,colors.resist)+rect(31,15,16,16,colors.glass)+rect(57,15,16,16,colors.si)+line(21,23,31,23,colors.red,2)+line(47,23,57,23,colors.red,2);
 else if(type==='flow')drawing=path('M5 23h58m-11-7 11 7-11 7','none',colors.oxide,5)+line(9,8,67,8,colors.si)+line(9,38,67,38,colors.si);
 else if(type==='circuit')drawing=path('M5 23h17m24 0h27','none',colors.ink,2)+rect( 22,16, 24, 14,colors.metal);
 else if(type==='data')drawing=[8,32, 56].map((x,i)=>rect(x, 14,18,20,[colors.glass,colors.oxide,colors.metal][i],3)).join('')+line(26,23,32,23)+line(50,23,56,23);
 else if(type==='inspect')drawing=circle(35, 22,16,'none',colors.red)+line(45,34, 60,43,colors.red,3)+dots([[27,18],[ 41, 25]]);
 else drawing=rect(9,8, 60, 14,colors.si)+rect(9,24, 60,14,colors.oxide)+line(15,23,65,23,colors.red,1,'3 3');
 const label={layers:'LAYER',wave:'SIGNAL',force:'LOAD',alignment:'OVERLAY',thermal:'HEAT',flow:'FLOW',circuit:'CIRCUIT',data:'DATA',inspect:'INSPECT',interface:'INTERFACE'}[type];
 return `<g transform="translate(298  50)">${rect(-3,-4, 98,58,'#ffffffdc',6,'#a5b9a7')}${text(6,5,label,7,'#668069')}<g transform="translate(7 7) scale(.85)">${drawing}</g></g>`;
}
