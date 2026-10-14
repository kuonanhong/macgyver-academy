#!/usr/bin/env python3
"""Build the V9 media supplement from verified Commons/oEmbed snapshots.
Network access is optional: bundled media.json and local photos are the deployable inputs.
This authoring tool uses bundled research metadata for provenance rebuilding; the local licensed photos must be present.
"""
import json,re,html,hashlib,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; OUT=ROOT/'tools/packaging-v9'; CACHE=OUT/'media-research'; ASSETS=ROOT/'public/academy/assets/photos/packaging-v9'
D=lambda p:json.loads(p.read_text())
metadata={p['title'][5:]:p['imageinfo'][0] for fn in ['selected.json','selected-more.json'] for p in D(CACHE/fn)['query']['pages'].values() if p.get('imageinfo')}
# filename | short id | Chinese title | English title | specific reading limit (zh~en)
photo_specs='''3D Orthogonal Quilt Packaging.jpg|quilt-3d|垂直排列的 Quilt Packaging 多晶片組合|Orthogonal multi-chip assembly using Quilt Packaging|以實際多晶片排列比較封裝幾何；不是 Foveros、SoIC 或混合接合剖面。~Compare physical multi-chip geometry; this is not a Foveros, SoIC or hybrid-bond cross-section.
3x3 Quilt Packaging Chip Array.jpg|quilt-array|Quilt Packaging 的 3 × 3 晶片陣列|A 3 × 3 Quilt Packaging chip array|觀察橫向多晶片互連；這是 Quilt Packaging 實例，不是 CoWoS 或 EMIB 實物。~Observe lateral multi-chip assembly; this is Quilt Packaging, not a CoWoS or EMIB specimen.
Quilt Packaging Nodules with Reflowed Solder.jpg|quilt-solder|Quilt Packaging 接點及回焊焊料顯微影像|Microscopy of Quilt Packaging nodules and reflowed solder|觀察接點及焊料形貌；不可從灰階判定銅柱材料、界面反應或機械可靠度。~Inspect joints and solder morphology; greyscale alone cannot identify copper-pillar composition, interfacial reactions or mechanical reliability.
CMI 300301.jpg|power-package|CMI 300301 三相 MOSFET 功率模組外觀|Exterior of a CMI 300301 three-phase MOSFET power module|辨認功率模組外殼與引腳；封裝內部陶瓷、銀燒結及雙面冷卻結構沒有顯露。~Identify housing and pins; internal ceramics, silver sintering and double-sided cooling are not visible.
FMN Lab electro-optical integrated modulator.jpg|eo-modulator|FMN Lab 電光調變晶片的電接點接線|Electrical bonding of an FMN Lab electro-optic modulator chip|實體電光晶片與電接點接線；照片不足以辨別波導材料、調變頻寬或確定其為矽 PN 調變器。~Physical electro-optic chip and electrical bonding; this photograph does not establish waveguide material, bandwidth or a silicon PN-modulator architecture.
Laser diode chip.jpg|laser-chip|放在針眼旁的 JPL 可調式雷射裸晶|JPL tunable laser die beside a needle eye|辨認雷射裸晶尺度；這不是矽上量子點雷射或微轉印製程的實拍。~Orient laser-die scale; this is not a quantum-dot-on-silicon laser or a micro-transfer-printing process photograph.
Laser diode with the case and window removed-powered off.jpg|laser-can|移除外殼且未通電的 TO-18 雷射二極體|Unpowered TO-18 laser diode with its cap removed|觀察晶粒、接線與封裝；不應模仿拆殼通電，照片沒有提供雷射安全分類的量測。~Observe die, wires and package; do not infer laser classification from the photograph or reproduce powered operation of a decapped laser.
Nortel Networks AA1419001 GBIC transceiver laser diode tear down.jpg|gbic-die|GBIC 光收發器內的雷射與監測光二極體|Laser and monitor photodiode in a dismantled GBIC transceiver|右側為雷射小晶粒，左側較大晶粒為監測光二極體；不是整合鍺光偵測器的材料證據。~The smaller right-hand die is the laser and the larger left-hand die the monitor photodiode; this does not establish an integrated germanium detector.
Photonics chip 1.png|photonic-assembly|光子晶片與光纖連接的實體裝置|A physical photonic-chip and fiber assembly|來源標示為光子晶片；不把未公開的材料、光源形式或電路功能當作照片可證明的事實。~The source identifies a photonic chip; undisclosed materials, source architecture and circuit function cannot be inferred from appearance.
Синтез фотонных материалов для Индустрии 4.0.jpg|photonics-lab|FMN Lab 光子材料製備實驗室|Photonics materials preparation at FMN Lab|作為光子材料製備設備及無塵操作情境；不代表特定 SiN、SOI 或量產配方。~Context for photonics material preparation and clean handling, not a particular SiN, SOI or production recipe.
Thermal Paste 9648.jpg|tim-cooler|散熱器接觸面的預塗熱介面材料|Pre-applied thermal-interface material on a cooler|觀察接觸面覆蓋；照片不能測出接觸熱阻，也不是液態金屬或先進封裝專用 TIM。~Observe interface coverage; the image cannot measure contact resistance and is not evidence of liquid-metal or advanced-package-specific TIM.
Watercool Heatkiller IV GPU waterblock Fins.jpg|coldplate|鎳鍍銅 GPU 水冷板的細鰭片|Fine fins of a nickel-plated copper GPU cold plate|用外置冷板比較對流表面與流阻；不是蝕刻在晶片內部的微流道。~Compare convective area and flow restriction in an external cold plate; these are not microchannels etched inside a chip.
Optical table - Up view.jpg|optical-table|光學平台、光路與量測設備俯視|Optical table, beam paths and measurement equipment|觀察光學平台和量測鏈的組織；不是某一課的同調接收器、光達或頻率梳實測。~Observe the organization of an optical bench and measurement chain; not a measured coherent receiver, lidar or frequency-comb dataset for this course.
Green fiber, optical table and microscope.jpg|biosensor-lab|IPAS 光纖生物感測實驗展示|Optical-fiber biosensor demonstration at IPAS|這是光纖感測研究情境；不是矽光子微環生物感測器，不能直接推論檢出極限。~This is fiber-sensing research context, not a silicon microring biosensor; no detection limit follows from the image.'''
photos=[]
for row in photo_specs.splitlines():
 filename,slug,zh,en,notes=row.split('|'); note,noteEn=notes.split('~');m=metadata[filename];em=m['extmetadata'];author=html.unescape(re.sub('<[^>]+>','',em.get('Artist',{}).get('value','NASA / JPL'))).strip();lic=em['LicenseShortName']['value'];licenseurl=em.get('LicenseUrl',{}).get('value','https://www.jpl.nasa.gov/jpl-image-use-policy/')
 ext=Path(filename).suffix.lower();target=ASSETS/(slug+ext);target.parent.mkdir(exist_ok=True,parents=True);
 if (CACHE/filename).exists(): shutil.copyfile(CACHE/filename,target)
 assert target.is_file(), f'Missing licensed asset: {target}'
 photos.append(dict(id='v9-'+slug,title=zh,titleEn=en,author=author,license=lic,licenseUrl=licenseurl,sourceUrl=m['descriptionurl'],categories=['packaging'],courseIds=[],courseContext={},note=note,noteEn=noteEn,path='assets/photos/packaging-v9/'+target.name,downloadUrl=m.get('thumburl',m['url']).split('?')[0],changes='Wikimedia thumbnail or original copy; no scene edits. Responsive layout may crop display; open the file for its full frame.',changesZh='使用 Wikimedia 縮圖或原檔；未修改場景。響應式版面可能裁切顯示，可開啟完整圖片。',attribution=author+' — '+en+' — '+lic,representative=True,verifiedAt='2026-10-14',sha256=hashlib.sha256(target.read_bytes()).hexdigest(),mediaType='micrograph' if slug=='quilt-solder' else 'photograph',verification=dict(method='Commons file page/imageinfo checked for license and attribution. Downloaded image visually inspected; SHA-256 records exact file.',playbackTested=False)))
for photo in photos:
 if photo['id']=='v9-biosensor-lab':
  photo['author']='Jennie Groom / Institute for Photonics and Advanced Sensing, University of Adelaide'
  photo['attribution']='Jennie Groom — image courtesy of Professor Andre Luiten / IPAS, University of Adelaide — CC BY 2.0'
  photo['originalSourceUrl']='https://www.flickr.com/photos/ipasadelaide/14470573639/'
# Existing representative images are expanded without losing previous assignments.
existing=D(ROOT/'public/academy/data/photos.json')
for pid in ['v3-photonics-wafer','v8-hbm-die','bga-section','v8-wafer','v8-drie-failure','v8-micro-pillars']:
 p=next(p for p in existing if p['id']==pid);p.setdefault('courseContext',{});p.setdefault('courseIds',[]);photos.append(p)
photo_byid={p['id']:p for p in photos}
# Each topic has a specific visual question, a relevant observable and a limitation.
# id | photo id | focus zh~en | observable zh~en
TOPICS='''packaging|v9-quilt-array|將晶粒、互連、基板與散熱責任分開~Separate die, interconnect, substrate and cooling responsibilities|以功耗、頻寬及接點數建立介面表~Build an interface table with power, bandwidth and connection count
a103|v9-quilt-solder|銅柱、焊帽及金屬間化合物不是同一層~Distinguish copper pillar, solder cap and intermetallic layers|需要截面元素分析與高度分布才能確認組成和共面性~Composition and coplanarity require cross-sectional composition and height data
a104|v9-quilt-solder|壓力、溫度與接合時間共同影響接點~Pressure, temperature and time jointly affect a joint|比較接合前後的接點高度與四線電阻~Compare joint height and four-wire resistance before and after bonding
a105|v9-quilt-solder|銅對銅接合不依賴回焊焊料~Copper-to-copper bonding is distinct from solder reflow|以界面空洞和接觸電阻檢查真正接合面~Inspect actual bonded area with interface-void and contact-resistance evidence
a106|v8-wafer|整片接合要同時管理局部對準及全域形變~Whole-wafer bonding combines local alignment and global deformation|繪出中心至邊緣的套刻誤差向量~Plot overlay-error vectors from center to edge
a107|v9-quilt-3d|已知良品晶粒的選擇不能取代接合後檢查~Known-good die selection does not replace post-bond inspection|比較放置誤差、接合空洞及鏈路導通率~Compare placement error, bond voids and daisy-chain continuity
a108|v9-quilt-3d|垂直晶粒堆疊改變熱路徑與可測性~Vertical die stacking changes heat paths and test access|標示每一層的電源、訊號、熱及測試連接~Mark power, signal, heat and test paths for each layer
a109|v8-wafer|暫時膠層提供機械支撐但必須能移除~A temporary adhesive supports a wafer but must be removable|用薄化前後翹曲及解接合後殘膠量評估~Evaluate warpage around thinning and residue after debonding
a110|v8-wafer|背磨厚度與次表面損傷要分開管理~Control remaining thickness separately from subsurface damage|需要厚度圖、邊緣缺口檢查及強度抽樣~Use thickness maps, edge-chip inspection and sampled strength evidence
a111|v8-wafer|隱形切割的改質層在晶片內部~Stealth dicing modifies material inside the wafer|外觀切縫不足以證明內部裂縫路徑~Visible kerfs alone do not establish the internal fracture path
a112|v8-drie-failure|電漿切割需要側壁、遮罩與終點協同~Plasma dicing couples sidewalls, mask and endpoint|以側壁殘留、崩角及切穿均勻性比較方法~Compare sidewall residue, chipping and through-cut uniformity
a113|v9-quilt-array|拾取釋放與光學對準誤差分開~Separate pickup/release error from optical registration error|使用放置後位置分布與晶粒損傷率~Use post-placement position distributions and die-damage rate
a114|bga-section|毛細填膠的流動前緣可能包住空氣~An underfill flow front can trap air|比較流前緣時間序列、空洞圖及固化翹曲~Compare flow-front time series, void maps and cure warpage
a115|bga-section|模封後曲率反映材料與固化歷史~Post-mold curvature depends on material and cure history|量測室溫及升溫翹曲而非只看平面外觀~Measure room- and elevated-temperature warpage rather than appearance
a116|v9-quilt-array|扇出封裝的 RDL 超出晶粒邊界~Fan-out RDL extends beyond the die boundary|建立晶粒位移到 RDL 對準殘差的關聯~Relate die shift to residual RDL overlay
a117|v8-wafer|面板尺度的形變不能直接套用晶圓補償~Panel deformation is not automatically corrected by wafer models|比較全域尺度、局部形變及邊緣區良率~Compare global scale, local deformation and edge-region yield
a118|v9-quilt-solder|種子層、電鍍及去種子層共同決定線路~Seed, plating and seed removal jointly define routing|以線寬、厚度及隔離電阻形成三維驗收~Accept against width, thickness and isolation resistance
a119|bga-section|嵌入晶粒的接觸開口與樹脂層要可追溯~Trace contact openings and resin layers in embedded die|查對晶粒傾斜、覆蓋厚度與導通圖~Check die tilt, cover thickness and continuity maps
a120|v9-quilt-array|異質系統的介面不只有電訊號~Heterogeneous-system interfaces include more than signals|記錄接地、功耗、時序及材料相容性~Record grounds, power, timing and material compatibility
a121|v8-drie-failure|TSV 蝕刻側壁與介電覆蓋相互影響~TSV sidewalls influence dielectric coverage|用截面深寬比與漏電對照蝕刻缺陷~Relate cross-sectional aspect ratio and leakage to etch defects
a122|v9-quilt-solder|TSV 金屬填充不能由表面封口判斷~A sealed TSV top does not prove void-free fill|用內部空洞分布、電阻及熱循環資料~Use internal void distributions, resistance and cycling data
a123|v8-wafer|背面露出有矽殘留與過度去除兩種風險~Backside reveal risks both silicon residue and over-removal|比較晶圓厚度圖與每區露出高度~Compare wafer thickness maps and local reveal height
a124|v8-micro-pillars|玻璃通孔與矽通孔的材料破壞不同~Glass and silicon vias have different fracture behavior|以裂紋、錐角及金屬附著力驗證~Verify cracks, taper and metal adhesion
a125|v9-quilt-array|中介層提供細間距佈線但增加界面~An interposer adds fine routing and additional interfaces|標示水平配線、垂直通孔與返回路徑~Mark horizontal routing, vertical vias and return paths
a126|bga-section|有機中介層的材料各向異性不可忽略~Organic-interposer anisotropy matters|檢查走線方向、堆疊及溫度對幾何的影響~Check routing direction, stack-up and temperature effects on geometry
a127|bga-section|玻璃核心的平坦度與通孔可靠度需共同驗證~Glass-core flatness and via reliability need joint verification|將核心翹曲、通孔裂紋和增層界面分開~Separate core warpage, via cracks and build-up interfaces
a128|bga-section|ABF 增層依賴介電層及微孔的連續品質~ABF build-up depends on dielectric and microvia quality|用逐層厚度、孔填充與導通資料追溯~Trace layer thickness, via fill and continuity data
a129|v9-quilt-array|局部互連橋不等於完整矽中介層~A local bridge is not a full silicon interposer|畫出橋區與有機基板區的訊號邊界~Draw the signal boundaries of bridge and organic regions
a130|v9-quilt-array|實體層通道必須包含封裝返回路徑~A physical-layer channel includes the package return path|用眼圖、BER 與通道 S 參數連結驗證~Link eye, BER and channel S-parameter evidence
a131|v8-hbm-die|HBM 堆疊中的熱、供電及測試路徑不同~HBM heat, power and test paths differ|逐層標出可測接點與資料通道~Mark test-access points and data channels layer by layer
a132|v9-coldplate|3D 堆疊的熱點不一定靠近散熱面~A 3D-stack hotspot need not lie next to its cooling surface|以分層熱阻模型對照埋藏接面溫度~Compare a layered thermal-resistance model with buried-junction temperature
a133|bga-section|封裝供電完整性包含頻率相關阻抗~Package power integrity involves frequency-dependent impedance|把 DC 壓降與瞬時壓降頻譜分開~Separate DC voltage drop from transient-droop spectra
a134|bga-section|訊號完整性包含串音與返回電流~Signal integrity includes crosstalk and return current|比較插入損耗、反射與近遠端串音~Compare insertion loss, reflection and near/far-end crosstalk
a135|v9-power-package|金屬外殼不自動形成完整射頻屏蔽~A metal enclosure does not automatically provide RF shielding|辨認縫隙、接地阻抗及共模路徑~Identify apertures, ground impedance and common-mode paths
a136|bga-section|寄生參數與激發頻率及參考平面有關~Parasitics depend on frequency and reference planes|以被動性、互易性和網格收斂檢查模型~Check passivity, reciprocity and mesh convergence
a137|bga-section|去耦電容的 ESL 與放置路徑影響有效性~ESL and placement paths limit decoupling effectiveness|觀察阻抗最低點及反共振峰而不只容量~Inspect impedance minima and antiresonance peaks, not only capacitance
a138|v9-power-package|封裝內轉換器同時帶來熱及電磁耦合~In-package converters add thermal and electromagnetic coupling|分離開關損耗、導通損耗及雜訊回路~Separate switching loss, conduction loss and noise loops
a139|v9-tim-cooler|TIM 覆蓋不等於低接觸熱阻~TIM coverage does not establish low contact resistance|比較厚度、接觸壓力及功率溫升~Compare thickness, contact pressure and power-induced temperature rise
a140|v9-coldplate|冷卻效果須與泵功及壓降一起評估~Evaluate cooling with pump power and pressure drop|用熱阻及壓降兩張曲線找折衷~Use thermal-resistance and pressure-drop curves to identify trade-offs
a141|v9-laser-can|氣密封裝的外觀不能證明漏率~Appearance cannot establish package leak rate|區分粗漏、細漏與水氣侵入測試~Distinguish gross-leak, fine-leak and moisture-ingress tests
a142|v9-power-package|真空封裝同時受漏氣及放氣影響~Vacuum packages are affected by leakage and outgassing|比較封裝壓力隨時間及溫度的變化~Compare pressure versus time and temperature
a143|v9-power-package|銀燒結接合層的孔隙不能由外殼觀察~Silver-sinter joint porosity is hidden by the housing|需要孔隙率、剪切強度及熱阻的對照~Correlate porosity, shear strength and thermal resistance
a144|v9-coldplate|雙面散熱必須兼顧電絕緣與平坦度~Double-sided cooling must preserve insulation and flatness|建立上下兩條熱路與接觸邊界~Model both heat paths and their contact boundaries
a145|v9-power-package|DBC 陶瓷提供絕緣也參與熱機應力~DBC ceramic provides insulation and thermomechanical constraint|比較剝離、熱阻與絕緣測試而非只看銅色~Compare delamination, thermal resistance and insulation tests
a146|bga-section|溫度循環的失效機制不等同恆溫老化~Temperature cycling does not reproduce constant-temperature aging|記錄溫差、停留、升降速率及失效位置~Record range, dwell, ramp rate and failure location
a147|bga-section|吸濕量與回焊中的內部壓力是不同觀察~Moisture uptake and reflow-induced pressure are different observations|以重量變化、分層圖及回焊條件串起因果~Link mass change, delamination maps and reflow conditions
a148|v9-quilt-solder|焊點壽命模型必須對應正確應變指標~Solder-life models require the appropriate strain metric|用多個負載條件擬合並保留驗證組~Fit several load conditions and retain a validation set
a149|bga-section|聲學回波受界面與閘門深度影響~Acoustic echoes depend on interfaces and gate depth|比較 A-scan、C-scan 與截面確認缺陷~Compare A-scans, C-scans and sections to verify a defect
a150|v9-quilt-solder|X 光投影重疊不能當作三維斷層~Overlapping X-ray projections are not 3D tomography|比較體素大小、偽影及已知幾何驗證~Compare voxel size, artifacts and known-geometry checks
a151|v3-photonics-wafer|SOI 截面的芯層與埋氧層無法從晶圓色彩辨認~SOI core and buried oxide are not identified by wafer colour|以截面厚度、側壁粗糙度及傳播損耗連結~Relate cross-sectional thickness, roughness and propagation loss
a152|v9-photonics-lab|SiN 低損耗需要分開吸收與散射~Low-loss SiN requires separating absorption and scattering|用波長與長度掃描找出損耗來源~Use wavelength and length sweeps to investigate loss origin
a153|v3-photonics-wafer|次波長單元的有效介質近似有適用條件~An effective-medium approximation has limits for subwavelength cells|檢查週期、占空比及波長的比例~Check ratios of period, duty cycle and wavelength
a154|v9-photonic-assembly|光柵耦合的角度、偏振與波長交互影響~Grating coupling couples angle, polarization and wavelength|比較波長角度二維效率圖~Compare two-dimensional wavelength-angle efficiency maps
a155|v9-photonic-assembly|邊緣模式轉換與端面品質共同決定耦合~Mode conversion and facet quality jointly set edge coupling|掃描橫向偏移與端面間隙的插入損耗~Scan insertion loss against lateral offset and facet gap
a156|v9-photonic-assembly|主動對準尋找光功率最大值而非影像中心~Active alignment maximizes optical power, not image centering|保留搜尋軌跡、多通道功率及固定後損失~Record search trajectories, channel powers and post-fixation loss
a157|v9-photonic-assembly|被動對準依靠機械基準與統計容差~Passive alignment depends on datums and statistical tolerances|量測裝配後分布並与耦合容差窗口比較~Compare assembly distributions with coupling tolerance windows
a158|v9-photonic-assembly|固化收縮及熱膨脹會讓最佳對準點漂移~Cure shrinkage and thermal expansion shift the optimum alignment|量測固化前後與熱循環後的光功率~Measure power before/after cure and after thermal cycling
a159|v9-eo-modulator|偏振分光與偏振旋轉是兩種功能~Polarization splitting and rotation are distinct functions|建立 TE/TM 輸入與兩個輸出的功率矩陣~Build a power matrix for TE/TM inputs and both outputs
a160|v9-eo-modulator|MMI 自成像不是任意長度都能成立~MMI self-imaging requires suitable geometry|比較分光比、相位與波長漂移~Compare splitting ratio, phase and wavelength dependence
a161|v9-eo-modulator|方向耦合器間隙與耦合長度相互關聯~Gap and coupling length are linked in directional couplers|對製程偏差做參數掃描而非只驗證標稱點~Sweep process deviations rather than only the nominal point
a162|v9-eo-modulator|MZM 的光學相位與電極傳播都影響頻寬~Optical phase and electrode propagation both affect MZM bandwidth|分別驗證 VπL、插入損耗及電光 S21~Validate VπL, insertion loss and electro-optic S21 separately
a163|v9-eo-modulator|微環小尺寸以窄頻及熱敏感性為代價~A compact microring trades against bandwidth and thermal sensitivity|用透射頻譜、線寬及溫度漂移評估~Evaluate transmission spectrum, linewidth and temperature drift
a164|v9-gbic-die|光偵測器材料要由來源與結構確認~Detector material requires provenance and structure evidence|分別量測響應度、暗電流與頻寬~Measure responsivity, dark current and bandwidth separately
a165|v9-gbic-die|雪崩增益伴隨雜訊與偏壓依賴~Avalanche gain brings noise and bias dependence|用增益、過量雜訊及崩潰電壓共同驗證~Jointly validate gain, excess noise and breakdown voltage
a166|v9-eo-modulator|熱光調相效率與熱串擾要一起評估~Thermo-optic efficiency and thermal crosstalk must be assessed together|比較 Pπ、響應時間及鄰近光路漂移~Compare Pπ, response time and neighboring-path drift
a167|v9-eo-modulator|載子耗盡調變同時改變相位與損耗~Carrier-depletion modulation changes phase and loss|以偏壓掃描相位、吸收與接面電容~Sweep phase, absorption and junction capacitance versus bias
a168|v9-eo-modulator|異質薄膜鈮酸鋰需處理材料軸向與界面~Heterogeneous lithium niobate requires crystal-axis and interface control|查對光模態重疊、電極方向及接合空洞~Check mode overlap, electrode orientation and bond voids
a169|v9-laser-chip|III-V 增益區與矽波導的光轉接不可省略~III-V gain-to-silicon optical transfer is an essential interface|比較接合層厚度、耦合損耗及熱阻~Compare bonding-layer thickness, coupling loss and thermal resistance
a170|v9-laser-chip|微轉印的拾取、釋放與鍵合要各有證據~Micro-transfer pickup, release and bonding require separate evidence|追蹤印章接觸、晶粒位置及最終導通~Track stamp contact, die position and final continuity
a171|v9-laser-chip|量子點雷射研究成果要區分材料和系統層級~Distinguish material- and system-level quantum-dot laser results|比較閾值、斜率效率與老化條件~Compare threshold, slope efficiency and aging conditions
a172|v9-laser-can|外接雷射移出熱源但增加光路與連接損失~An external laser moves heat but adds optical and connector loss|列出連接器、分光器及冗餘光源的功率預算~Budget connector, splitter and redundant-source power
a173|v9-laser-chip|SOA 增益會飽和並引入放大自發輻射~SOA gain saturates and introduces amplified spontaneous emission|量測增益對輸入功率與光學雜訊密度~Measure gain versus input power and optical noise density
a174|v9-optical-table|AWG 波長分路依靠受控路徑差~AWG wavelength routing relies on controlled path differences|檢查通帶、串音及偏振依賴~Inspect passbands, crosstalk and polarization dependence
a175|v9-eo-modulator|微環濾波器通道需對應熱調諧範圍~Ring-filter channels must match available thermal tuning|比較 FSR、線寬及相鄰通道隔離~Compare FSR, linewidth and adjacent-channel isolation
a176|v9-photonic-assembly|光開關矩陣的路徑數增加累積損耗~More switch stages accumulate path loss|針對每條路徑記錄插入損耗與串音~Record insertion loss and crosstalk for each route
a177|v9-photonic-assembly|可程式光路需要校準而非只改控制字~Programmable photonics requires calibration, not just control words|量測相位控制矩陣與漂移後誤差~Measure the phase-control matrix and post-drift error
a178|v9-optical-table|同調接收要同時維持振幅、相位及偏振資訊~Coherent receivers preserve amplitude, phase and polarization|比較 I/Q 不平衡、雜訊與星座圖~Compare I/Q imbalance, noise and constellations
a179|v9-photonic-assembly|OPA 光束方向由相位斜率與取樣間距決定~OPA steering depends on phase slope and element spacing|量測主瓣角度、旁瓣及柵瓣~Measure main-lobe angle, sidelobes and grating lobes
a180|v9-optical-table|FMCW 拍頻需要區分距離與都卜勒~FMCW beat frequencies mix range and Doppler|以已知目標距離與速度驗證掃頻模型~Validate the chirp model with known target range and velocity
a181|v9-biosensor-lab|光學生物感測必須控制非特異吸附與背景~Optical biosensing requires nonspecific-binding and background controls|以空白、參考通道及濃度序列估計檢出能力~Use blanks, reference channels and concentration series to estimate detectability
a182|v9-laser-chip|中紅外材料吸收窗口與感測波段相匹配~Mid-IR transparency must match the sensing band|比較樣品吸收、背景水氣及光路基線~Compare sample absorption, background water vapor and optical baseline
a183|v9-optical-table|頻率梳的光譜線存在不代表相位鎖定~Comb lines alone do not establish phase locking|使用射頻拍頻與相干性證據輔助光譜~Add RF beat and coherence evidence to optical spectra
a184|v9-photonic-assembly|量子光源要驗證光子統計與多光子機率~Quantum sources require photon-statistics and multiphoton checks|量測符合計數、背景與 g² 及不確定度~Measure coincidences, background and g² with uncertainties
a185|v3-photonics-wafer|晶圓光測試要分離耦合器與元件損耗~Wafer optical tests must separate coupler and device loss|使用參考結構、重複探測及晶圓位置圖~Use reference structures, repeated probing and wafer-position maps
a186|v9-photonic-assembly|熱機形變會同時改變對準與有效折射率~Thermomechanical deformation changes alignment and effective index|結合位移量測、溫度場及光譜漂移~Combine displacement, temperature and spectral-drift evidence
a187|v9-eo-modulator|漂移補償必須考慮感測雜訊及控制穩定度~Drift compensation includes sensor noise and loop stability|對照開迴路漂移及閉迴路殘差~Compare open-loop drift with closed-loop residuals
a188|v9-photonic-assembly|失效重路由要重新評估功率及相位裕度~Failure rerouting changes power and phase margins|逐一移除路徑元素並驗證剩餘路徑~Remove one path element at a time and verify remaining routes
a189|v9-eo-modulator|應力致相位包含幾何變化及光彈效應~Stress-induced phase includes geometry and photoelasticity|使用應變、偏振及相位差量測分離機制~Separate mechanisms using strain, polarization and phase measurements
a190|v3-photonics-wafer|PDK 模型須對應製程版本與統計角落~PDK models must match process versions and statistical corners|以版圖規則、測試結構及模型版本驗證~Verify layout rules, test structures and model versions
a191|v9-photonic-assembly|CPO 光引擎靠近熱源也靠近短電通道~CPO optics approach both heat sources and shorter electrical channels|共同配置電通道、雷射路徑及可維修性~Co-plan electrical channels, laser paths and serviceability
a192|v9-photonic-assembly|光學 I/O 小晶片需有可比較的系統邊界~Optical-I/O chiplets need comparable system boundaries|標示是否計入雷射、驅動器及接收器功率~State whether laser, driver and receiver power are included
a193|v9-eo-modulator|電子與光子共同設計需要一致參考平面~Electronic-photonic co-design needs consistent reference planes|連接電驅動、電光模型與光鏈路雜訊~Connect electrical drive, electro-optic models and link noise
a194|v9-power-package|光模組仍具有高速電路與共模輻射~Optical modules still contain high-speed circuits and common-mode emissions|分離傳導、輻射及光學功能測試~Separate conducted, radiated and optical functional tests
a195|v9-laser-can|雷射安全必須依設備條件和聯鎖狀態驗證~Laser safety depends on equipment conditions and interlock state|以故障注入表檢查開蓋、斷線與失電的安全狀態~Use a fault-injection table for cover opening, broken wires and power loss
a196|v9-quilt-array|CoWoS 案例的結構與其他橫向互連不同~CoWoS architecture differs from other lateral-interconnect examples|查對官方 CoWoS 變體與對應的中介層形式~Check official CoWoS variants against their interposer approaches
a197|v9-quilt-3d|SoIC 案例不能以普通堆疊照片推定接合界面~An ordinary stacked assembly cannot establish a SoIC bond interface|以公開平台資料標示接合、測試及熱邊界~Annotate bonding, testing and thermal boundaries from public platform sources
a198|v9-quilt-3d|Foveros 公開平台描述與產品結構要對照~Match Foveros platform descriptions to the specific product|記下基底晶粒、上層晶粒及電源路徑~Record base die, top die and power paths
a199|v9-quilt-array|EMIB 的局部橋接與整片中介層需分清~Distinguish EMIB local bridging from a full interposer|比較橋的位置、互連距離與基板區域~Compare bridge location, interconnect distance and substrate regions
a200|v3-photonics-wafer|iSiPP 平台可用元件與服務版本需一致~iSiPP components must match the service/platform version|查對官方元件清單、封裝介面及測試途徑~Check official component lists, packaging interfaces and test paths
silicon-photonics|v9-photonic-assembly|光引擎由光源、調變、偵測、封裝與控制共同構成~An optical engine combines source, modulation, detection, packaging and control|建立端到端功率、頻寬、溫度與失效預算~Build end-to-end power, bandwidth, thermal and failure budgets'''
source_records=[]
def source(sid,title,url,publisher,scope):
 rec=dict(id=sid,title=title,url=url,publisher=publisher,scope=scope+' 原創觀察作業以此為背景；並非原作者的完整實驗步驟。',sourceType='primary technical reference',accessed='2026-10-14',imageReuse='Link only. Photos redistributed only under separately recorded licenses.');source_records.append(rec);return rec
pi=source('v9-media-pi','PI photonics alignment: test and assembly','https://www.pi-usa.us/en/applications/photonics-alignment-fiber-alignment-siph','Physik Instrumente','主動光學對準、探測及封裝介面的官方說明。')
tap=source('v9-media-aim-tap','AIM Photonics: Test, Assembly and Packaging','https://www.aimphotonics.com/tap','AIM Photonics','光電測試、晶圓組裝及封裝服務範圍。')
sim=source('v9-media-aim-sims','AIM Photonics: Virtual Lab Simulation Library','https://www.aimphotonics.com/simulation-library','AIM Photonics','公開波導、耦合器、微環與干涉器學習工具。')
pdk=source('v9-media-aim-pdk','AIM Photonics: Process Design Kits','https://www.aimphotonics.com/pdk','AIM Photonics','PDK 與組裝設計套件的公開說明；實際套件依原機構申請及授權。')
imec=source('v9-media-imec','imec: Next-generation silicon photonics','https://www.imec-int.com/en/next-generation-silicon-photonics','imec','光學 I/O、光電整合、封裝與系統驗證之研究範圍。')
ozen=source('v9-media-ozen','Introduction to silicon photonic (Part 1)','https://ozeninc.com/videos/fCBlXMDpa2I/introduction-to-silicon-photonic-part1/','Ozen Engineering','出版者自己的光子設計教學；軟體示範不等於實測。')
pi_videos=source('v9-media-pi-video-library','PI official video library','https://www.pi-usa.us/en/knowledge-center/resources/videos-animations','Physik Instrumente','官方對準與晶圓光探測示範的來源頁。')
aimtalk=source('v9-media-aim-talk','AIM Photonics and NY Creates capabilities presentation','https://www.aimphotonics.com/news/aim-photonics-and-ny-creates-pic-and-packaging-capabilities-shared-with-california-dreams','AIM Photonics / CA DREAMS','由 AIM 官方頁面連結的機構平台與封裝演講。')
existing_sources={s['id']:s for s in D(ROOT/'public/academy/data/sources.json')}
refs={**existing_sources,**{s['id']:s for s in source_records}}
def subset(sids):return [{k:refs[s][k] for k in ['id','title','url']} for s in sids]
video_specs=[
('78Z5nkh_m-0','Intel：先進封裝的整合角色','廠商概覽；觀察工廠與架構的責任邊界，並非製程配方。','Vendor overview: inspect manufacturing and architectural responsibilities, not process recipes.','v3-media-698d26511517',2023,['packaging','a120','a125','a130','a131','a132','a196','a197','a198','a199']),
('HEyW9ox9Ne0','Intel 封裝工作坊：多晶粒互連','2019 年架構與平台背景；不把當時路線圖視為今日產品規格。','2019 architecture and platform context; do not treat that roadmap as current product specifications.','intel-packaging',2019,['packaging','a108','a129','a198','a199']),
('-egYoxajTz0','Applied Materials：先進封裝世界','材料與製程概覽；動畫中的幾何和尺度經過簡化。','Materials and process overview; animation geometry and scale are simplified.','pkb-amkor-characterization',None,['packaging','a103','a116','a117','a118','a119','a121','a122','a123','a124','a126','a127','a128']),
('wJVDpclyG6A','Applied Materials：Kinex 混合接合整合系統','廠商系統動畫；辨認表面準備、轉移及接合介面，不當作通用量產配方。','Vendor system animation: identify surface preparation, transfer and bonding interfaces; not a universal production recipe.','pkb-evg-hybrid',None,['a105','a106','a107','a108','a113','a197']),
('hksKKrkcAJg','PI：光子對準機構與控制解說','2023 年展場設備解說；性能屬原設備與測試條件。','2023 exhibition demonstration; performance belongs to the original equipment and test conditions.','v9-media-pi',2023,['a154','a155','a156','a157','a158','a186']),
('haYFixYgrHM','PI：2026 光子測試與生產對準','2026 年供應商設備演示；用以比較對準自由度和測试流程。','2026 supplier demonstration for comparing alignment degrees of freedom and test workflows.','v9-media-pi',2026,['a156','a157','a185','a191','a192']),
('stvB1MPTF-c','AIM Photonics 與 NY Creates 光子及封裝能力','AIM 官方頁連至 CA DREAMS 發表的機構演講；平台能力不等於開放製程配方。','Institutional presentation published by CA DREAMS and linked from AIM; platform capability is not an open process recipe.','v9-media-aim-talk',2026,['silicon-photonics','a168','a169','a170','a171','a172','a184','a190','a191','a192','a193','a200']),
('fCBlXMDpa2I','Ozen Engineering：矽光子入門','出版者自己的設計教學；區分波導模型、模擬和實測證據。','Publisher-authored design tutorial; distinguish waveguide models, simulations and measured evidence.','v9-media-ozen',2022,['silicon-photonics','a151','a152','a153','a159','a160','a161','a162','a163','a164','a166','a167','a174','a175','a176','a177']),
('e2DYwblIr-E','PI：光纖及矽光子主動對準組裝站','自動化設備展示；觀察搜尋和定位順序，不保證能看清實際光路內部。','Automation demonstration: observe search and positioning order; internal optical paths may not be visible.','v9-media-pi-video-library',None,['a113','a155','a156','a158']),
('_TG3lUu-k0k','PI：晶圓光探測對準示範','2016 年探測示範；辨認晶圓、探頭與光功率回授，不套用為現行量產節拍。','2016 probing demonstration: identify wafer, probe and optical-power feedback, not current production throughput.','v9-media-pi-video-library',2016,['a154','a185','a190','a200']),
('Skdf8ekrHbU','PI：多通道光子對準測試平台','多自由度及多通道對準展示；單通道峰值不等於所有通道同時最佳。','Multi-axis and multichannel alignment demonstration; a peak on one channel does not establish the optimum for all channels.','v9-media-pi-video-library',None,['a156','a157','a185','a186'])]
videos_bycourse={}
for vid,zh,scope,scopeEn,sourceid,year,ids in video_specs:
 d=D(CACHE/f'video-{vid}.json');url='https://www.youtube.com/watch?v='+vid
 video=dict(id='v9-video-'+vid,youtubeId=vid,title=zh,titleEn=d['title'],originalTitle=d['title'],url=url,embedUrl='https://www.youtube-nocookie.com/embed/'+vid,sourcePage=(refs[sourceid]['url'] if sourceid in ['v9-media-aim-talk','v9-media-pi','v9-media-pi-video-library','v9-media-ozen','v3-media-698d26511517'] else url),fallbackUrl=url,publisher=d['author_name'],author=d['author_name'],authorUrl=d['author_url'],language='en',publicationYear=year,scope=scope,scopeEn=scopeEn,captionNote='字幕與翻譯依原平台提供；未保證完整繁體中文字幕。',captionNoteEn='Captions and translations depend on the original platform; complete Traditional Chinese captions are not guaranteed.',rights='Official/publisher external embed and link only. Copyright remains with its owner; no download or rehosting license is claimed.',verification=dict(checkedAt='2026-10-14',method='Exact title/channel/embed metadata verified through YouTube oEmbed; official publisher page or channel checked. Playback was not exercised.',oembedVerified=True,playbackTested=False,availabilityNote='YouTube can require sign-in or block embedding by region, policy, browser or network. Use the external source link or the bundled reading guide; no restriction bypass is provided.'),sources=subset([sourceid]))
 for cid in ids:videos_bycourse.setdefault(cid,[]).append(video.copy())
# Explicit per-course modality/material limitations from independent media audit.
COURSE_IMAGE_LIMITS = {
 'a105': ('圖中為 Quilt Packaging 焊料互連的比較照片，不是直接 Cu-Cu 或介電／銅混合接合界面。', 'This Quilt Packaging solder interconnect is a comparison image, not a direct Cu-Cu or dielectric/Cu hybrid-bond interface.'),
 'a118': ('圖中為 Quilt Packaging 焊料互連，不是 RDL 金屬線的截面。', 'This shows Quilt Packaging solder interconnects, not an RDL metal-line cross-section.'),
 'a122': ('圖中為外露焊料互連，不顯示 TSV 孔內部或其填充完整性。', 'Exposed solder interconnects do not show TSV interiors or fill integrity.'),
 'a124': ('圖中為矽微柱，不是玻璃通孔 TGV，也不能據此推定玻璃加工形貌。', 'These are silicon micropillars, not through-glass vias, and do not establish glass-processing morphology.'),
 'a117': ('晶圓照片只供圓形基材與尺度比較，不是面板級封裝製程的實拍。', 'The wafer photo provides circular-substrate/scale context, not footage of panel-level packaging.'),
 'a127': ('此 BGA 截面僅示意接點與基板位置，不能確認其核心材料是玻璃。', 'This BGA section locates joints and substrate but does not establish a glass-core material.'),
 'a128': ('此 BGA 截面不能辨識樹脂化學成分，也不能確認使用 ABF 材料。', 'This BGA section does not identify resin chemistry or establish the use of ABF.'),
 'a149': ('此為實體 BGA 截面的光學照片，不是超音波 A-scan 或 C-scan 檢測資料。', 'This optical photograph of a physical BGA section is not ultrasonic A-scan or C-scan data.'),
 'a150': ('此為 Quilt Packaging 的顯微照片，不是 X 光 CT 切片或斷層重建。', 'This Quilt Packaging microscopy image is not an X-ray CT slice or tomographic reconstruction.'),
 'a165': ('此 GBIC 監測光二極體照片不能證明 Ge-Si 材料、APD 結構或雪崩倍增。', 'This GBIC monitor-photodiode photo does not establish Ge-Si material, APD structure or avalanche gain.')
}

# Media captions and viewing guides are authored independently, not copied source prose.
catalog={c['id']:c for c in D(ROOT/'public/academy/data/catalog.json')};media=[];primary={}
for row in TOPICS.splitlines():
 cid,pid,foc,obs=row.split('|');zh,en=foc.split('~');obz,obe=obs.split('~');course=catalog[cid];p=photo_byid[pid]
 primary[cid]=pid
 if cid not in p['courseIds']:p['courseIds'].append(cid)
 limit=p.get('note','代表性照片；不是本課量產配方或驗收資料。');limiten=p.get('noteEn','Representative photograph, not production instructions or acceptance data for this course.')
 if cid in COURSE_IMAGE_LIMITS:
  specific,specificen=COURSE_IMAGE_LIMITS[cid];limit=specific+' '+limit;limiten=specificen+' '+limiten
 p['courseContext'][cid]=dict(note=zh+'。'+limit,noteEn=en+'. '+limiten)
 num=int(cid[1:]) if cid.startswith('a') else 0
 if cid=='a196':sids=['pkb-tsmc-cowos','pkb-amkor-characterization']
 elif cid=='a197':sids=['pkb-tsmc-soic','pkb-evg-hybrid']
 elif cid in ['a198','a199']:sids=['intel-packaging','v3-media-41b8e80cea95']
 elif cid=='a200':sids=['v4-related-a0c006a2474d','v9-media-aim-pdk']
 elif 103<=num<=108:sids=['pkb-evg-hybrid','pk-besi-dieattach']
 elif 109<=num<=110:sids=['pk-evg-tbdb-flow','v4-related-a26c1d4a65a6']
 elif 146<=num<=150:sids=['pkb-amkor-characterization','v4-related-aa5a5e075b3b','v9-media-aim-tap']
 elif 132<=num<=145:sids=['pkb-amkor-characterization','v4-related-ebcc0a3ee20f']
 elif 154<=num<=158:sids=['v9-media-pi','v9-media-aim-tap']
 elif num==190:sids=['v9-media-aim-pdk','v9-media-aim-tap']
 elif 151<=num<=167:sids=['v9-media-aim-sims','v9-media-aim-tap']
 elif num>=168 or cid=='silicon-photonics':sids=['v9-media-imec','v9-media-aim-tap']
 else:sids=['pkb-amkor-characterization','v9-media-aim-tap']
 guide=dict(id='v9-guide-'+cid,title=course['title']+'：從圖像建立驗證證據',titleEn=course['titleEn']+': from visual context to verification evidence',concept=zh+'。照片能幫助定位元件和界面，但功能與可靠度需要可重複的量測。本工作單把「看見的物件」、「推論的機制」及「尚缺的證據」分成三欄，再與課內原創架構圖核對。',conceptEn=en+'. A photograph locates components and interfaces; function and reliability require repeatable measurements. This worksheet separates visible objects, inferred mechanisms and missing evidence before comparing the original course diagram.',procedure=[
 '開啟圖片原檔及其授權來源，記錄作者、日期與是否有比例尺。'+limit,
 '在自己的架構圖標出這個觀察問題：'+zh+'。把確實可見的邊界畫實線，推定結構畫虛線；保留未知標籤。',
 '建立量測計畫：'+obz+'。每一項都填入量測單位、儀器解析度、基準與重複次數；沒有資料就列為待量測。',
 '選一個你可控制的因素，做標稱、偏低與偏高三種模擬情境。預先寫出哪些觀察可推翻你的解釋，再與課程算例或你自行提供的資料比較；示範數值一律標為假設。',
 '回到所列的官方來源，確認原文描述的是平台能力、模擬範例、實測結果或驗收標準。交付一頁含來源、架構圖、觀察矩陣與未解問題的工程筆記。'],procedureEn=[
 'Open the full image and license source; record author, date and whether a scale is provided. '+limiten,
 'Mark this question on your own diagram: '+en+'. Draw visible boundaries as solid lines and inferred structures as dashed lines; retain unknown labels.',
 'Build a measurement plan: '+obe+'. Specify units, instrument resolution, baseline and repetitions for each quantity; mark missing data as not yet measured.',
 'Choose one controllable factor and model nominal, lower and higher cases. State in advance which observations would falsify your explanation. Compare with the course example or data you supply; label all illustrative numbers as assumptions.',
 'Return to the official references and identify whether each statement describes platform capability, simulation, measurement or acceptance criteria. Deliver a one-page engineering note containing provenance, a diagram, observation matrix and unresolved questions.'],evidence=['可見結構與原創架構圖之間的對照表；不以漂亮圖片代替量測。','針對「'+obz+'」列出的可執行量測計畫、單位與不確定度來源。'],evidenceEn=['A cross-reference between visible structure and the original diagram; attractive images do not substitute for measurement.','An actionable measurement plan for: '+obe+', including units and sources of uncertainty.'],pitfalls=['把代表性照片標成某廠商專有製程的實拍。','由單張外觀圖推論材料、內部結構或合格與否。'],pitfallsEn=['Relabeling a representative photograph as a proprietary vendor process.','Inferring materials, internal structure or acceptance from one exterior image.'],sources=subset(sids),simulationOnly=True,scope='原創觀察與驗證工作單，可離線閱讀。照片為代表性情境；未附本題專屬實測資料或生產配方。',scopeEn='Original observation and verification worksheet readable offline. Photos provide representative context; no dedicated measured dataset or production recipe is bundled.')
 videos=videos_bycourse.get(cid,[])
 for v in videos:
  v.update(watchFor=[zh+'。',obz+'。','標記畫面中未展示、仍需額外量測的界面。'],watchForEn=[en+'.',obe+'.','Identify interfaces not shown that still require measurement.'],before='先寫下本課的圖像判讀問題：'+zh+'。',beforeEn='Write the visual-reading question for this course: '+en+'.',after='完成觀察工作單，列出影片未能證明的三件事，並為每一件指定量測或來源。',afterEn='Complete the worksheet. List three claims not established by the video and specify a measurement or source for each.')
 media.append(dict(courseId=cid,title=course['title'],titleEn=course['titleEn'],videos=videos,guides=[guide],primaryPhotoId=pid))
assert len(media)==100 and len({c['courseId'] for c in media})==100
assert {c['courseId'] for c in media}=={c['id'] for c in catalog.values() if c['category']=='packaging'}
for p in photos:p['courseIds']=sorted(set(p['courseIds']))
manifest=dict(version=9,photos=photos,media=media,sources=source_records,primaryPhotos=primary,verification=dict(checkedAt='2026-10-14',newPhotoCount=14,existingPhotoRecordsUpdated=6,uniqueNewYoutubeVideos=len(video_specs),videoAssignments=sum(len(c['videos']) for c in media),guidedReadingCount=len(media),all100HaveRepresentativePhotos=True,all100HaveGuides=True,playbackTested=False,scope='Licensed photos and original viewing exercises; not 100 distinct manufacturing videos or per-step actual factory photographs.'))
(OUT/'media.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
# Small replayable proof of API verification; no copyrighted source-page body or video bytes.
proof={'checkedAt':'2026-10-14','photos':[{k:p[k] for k in ['id','author','license','licenseUrl','sourceUrl','downloadUrl','sha256']} for p in photos if p['id'].startswith('v9-')], 'videos':[{k:D(CACHE/f'video-{v[0]}.json')[k] for k in ['title','author_name','author_url','type','provider_name']}|{'youtubeId':v[0]} for v in video_specs]}
(OUT/'media-verification.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(manifest['verification'],ensure_ascii=False));print('new_photo_bytes',sum(f.stat().st_size for f in ASSETS.iterdir()))
