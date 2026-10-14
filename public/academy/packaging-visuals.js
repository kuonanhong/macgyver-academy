// Original educational SVG. Device topologies are schematic, not dimensions or proprietary product drawings.
export const PACKAGING_SUBJECTS = Object.freeze({
  "packaging": {
    "family": "package",
    "title": "先進封裝共同設計",
    "titleEn": "Advanced Packaging Co-Design",
    "focus": "晶粒、互連與熱路徑",
    "focusEn": "Dies, interconnects and heat paths"
  },
  "silicon-photonics": {
    "family": "cpo",
    "title": "矽光子與 CPO 光引擎",
    "titleEn": "Silicon Photonics and CPO Optical Engines",
    "focus": "電光介面與封裝分工",
    "focusEn": "Electrical/optical interfaces and package partitioning"
  },
  "a103": {
    "family": "pillar",
    "title": "銅柱微凸塊製作",
    "titleEn": "Copper-pillar microbump fabrication",
    "focus": "銅柱與焊帽；介面不是同一種材料",
    "focusEn": "Copper pillar and solder cap are different materials"
  },
  "a104": {
    "family": "bond",
    "title": "熱壓接合",
    "titleEn": "Thermocompression bonding",
    "focus": "熱與力施加於接合界面",
    "focusEn": "Heat and force at the bonding interface"
  },
  "a105": {
    "family": "directbond",
    "title": "直接銅對銅接合",
    "titleEn": "Direct copper-to-copper bonding",
    "focus": "銅表面直接接合；無焊帽",
    "focusEn": "Direct copper surfaces without solder caps"
  },
  "a106": {
    "family": "waferbond",
    "title": "晶圓對晶圓混合接合",
    "titleEn": "Wafer-to-wafer hybrid bonding",
    "focus": "兩片晶圓的介電層與銅墊共同接合",
    "focusEn": "Dielectric and copper contacts bond across two wafers"
  },
  "a107": {
    "family": "diebond",
    "title": "晶粒對晶圓混合接合",
    "titleEn": "Die-to-wafer hybrid bonding",
    "focus": "已知良晶粒對晶圓對準",
    "focusEn": "Known-good die aligns to a wafer"
  },
  "a108": {
    "family": "stack",
    "title": "晶粒對晶粒堆疊",
    "titleEn": "Die-to-die stacking",
    "focus": "垂直晶粒堆疊與逐層連通",
    "focusEn": "Vertical die stack and layer-by-layer continuity"
  },
  "a109": {
    "family": "temporary",
    "title": "晶圓暫時接合與解接合",
    "titleEn": "Temporary wafer bonding and debonding",
    "focus": "載板、暫黏層與產品晶圓",
    "focusEn": "Carrier, temporary adhesive and device wafer"
  },
  "a110": {
    "family": "grind",
    "title": "晶圓薄化與背面研磨",
    "titleEn": "Wafer thinning and backside grinding",
    "focus": "背面移除量與剩餘厚度",
    "focusEn": "Backside material removal and residual thickness"
  },
  "a111": {
    "family": "laserdice",
    "title": "雷射隱形切割",
    "titleEn": "Laser stealth dicing",
    "focus": "內部改質層與裂紋延伸",
    "focusEn": "Internal modified layer and crack propagation"
  },
  "a112": {
    "family": "plasmadice",
    "title": "電漿晶圓切割",
    "titleEn": "Plasma wafer dicing",
    "focus": "遮罩開口與電漿切割槽",
    "focusEn": "Mask openings and plasma dicing trenches"
  },
  "a113": {
    "family": "pick",
    "title": "晶粒拾取與精密放置",
    "titleEn": "Die picking and precision placement",
    "focus": "吸嘴、晶粒與視覺定位",
    "focusEn": "Nozzle, die and vision registration"
  },
  "a114": {
    "family": "underfill",
    "title": "底部填膠流動控制",
    "titleEn": "Underfill flow control",
    "focus": "毛細前緣、凸塊與排氣路徑",
    "focusEn": "Capillary front, bumps and vent path"
  },
  "a115": {
    "family": "warpage",
    "title": "模封材料與翹曲控制",
    "titleEn": "Molding compounds and warpage control",
    "focus": "材料熱膨脹差與曲率",
    "focusEn": "CTE mismatch and curvature"
  },
  "a116": {
    "family": "fanout",
    "title": "扇出型晶圓級封裝",
    "titleEn": "Fan-out wafer-level packaging",
    "focus": "重組晶圓與扇出佈線",
    "focusEn": "Reconstituted wafer and fan-out routing"
  },
  "a117": {
    "family": "panel",
    "title": "扇出型面板級封裝",
    "titleEn": "Fan-out panel-level packaging",
    "focus": "面板分區、晶粒偏移與佈線",
    "focusEn": "Panel zones, die shift and routing"
  },
  "a118": {
    "family": "rdl",
    "title": "重佈線層微影與電鍍",
    "titleEn": "Redistribution-layer lithography and plating",
    "focus": "介電層開口與重佈金屬",
    "focusEn": "Dielectric openings and redistributed metal"
  },
  "a119": {
    "family": "embed",
    "title": "嵌入式晶粒封裝",
    "titleEn": "Embedded-die packaging",
    "focus": "晶粒埋入基板並垂直連通",
    "focusEn": "Die embedded in a substrate with vertical access"
  },
  "a120": {
    "family": "sip",
    "title": "系統級封裝異質整合",
    "titleEn": "System-in-package heterogeneous integration",
    "focus": "感測、邏輯與被動件整合",
    "focusEn": "Sensors, logic and passives integrated together"
  },
  "a121": {
    "family": "viaetch",
    "title": "矽穿孔蝕刻與絕緣",
    "titleEn": "Through-silicon-via etching and insulation",
    "focus": "孔洞側壁絕緣；尚未填銅",
    "focusEn": "Via sidewall insulation before metal filling"
  },
  "a122": {
    "family": "viafill",
    "title": "矽穿孔金屬填充",
    "titleEn": "Through-silicon-via metal filling",
    "focus": "阻障、種子與金屬填充",
    "focusEn": "Barrier, seed and metal fill"
  },
  "a123": {
    "family": "viareveal",
    "title": "矽穿孔背面露出",
    "titleEn": "Through-silicon-via backside reveal",
    "focus": "背面薄化露出已填通孔",
    "focusEn": "Backside thinning reveals filled vias"
  },
  "a124": {
    "family": "glassvia",
    "title": "玻璃穿孔製作",
    "titleEn": "Through-glass-via fabrication",
    "focus": "玻璃核心中的金屬通孔",
    "focusEn": "Metal through-vias in a glass core"
  },
  "a125": {
    "family": "interposer",
    "title": "矽中介層佈線",
    "titleEn": "Silicon-interposer routing",
    "focus": "矽中介層與垂直通孔",
    "focusEn": "Silicon interposer and vertical vias"
  },
  "a126": {
    "family": "organic",
    "title": "有機中介層製作",
    "titleEn": "Organic-interposer fabrication",
    "focus": "有機多層佈線與微通孔",
    "focusEn": "Organic multilayer routing and microvias"
  },
  "a127": {
    "family": "glasscore",
    "title": "玻璃核心封裝基板",
    "titleEn": "Glass-core package substrates",
    "focus": "玻璃核心與上下增層",
    "focusEn": "Glass core with build-up on both sides"
  },
  "a128": {
    "family": "build-up",
    "title": "ABF 增層封裝基板",
    "titleEn": "ABF build-up package substrates",
    "focus": "交錯微通孔與增層介電質",
    "focusEn": "Staggered microvias and build-up dielectric"
  },
  "a129": {
    "family": "bridge",
    "title": "嵌入式互連橋整合",
    "titleEn": "Embedded interconnect-bridge integration",
    "focus": "局部互連橋連接相鄰晶粒",
    "focusEn": "Local bridge links adjacent dies"
  },
  "a130": {
    "family": "chiplet",
    "title": "小晶片互連實體層",
    "titleEn": "Chiplet-interconnect physical layers",
    "focus": "晶粒間傳送、接收與時序",
    "focusEn": "Die-to-die transmit, receive and timing"
  },
  "a131": {
    "family": "hbm",
    "title": "高頻寬記憶體堆疊整合",
    "titleEn": "High-bandwidth-memory stack integration",
    "focus": "記憶體堆疊、基底晶粒與控制器",
    "focusEn": "Memory stack, base die and controller"
  },
  "a132": {
    "family": "thermal",
    "title": "3D 邏輯堆疊熱管理",
    "titleEn": "Thermal management for 3D logic stacks",
    "focus": "堆疊晶粒的串並聯熱路徑",
    "focusEn": "Series and parallel heat paths in stacked dies"
  },
  "a133": {
    "family": "pdn",
    "title": "封裝供電完整性設計",
    "titleEn": "Package power-integrity design",
    "focus": "供電、回流與局部去耦",
    "focusEn": "Supply, return and local decoupling"
  },
  "a134": {
    "family": "signal",
    "title": "封裝訊號完整性設計",
    "titleEn": "Package signal-integrity design",
    "focus": "差分線與連續參考平面",
    "focusEn": "Differential traces and continuous reference plane"
  },
  "a135": {
    "family": "shield",
    "title": "封裝射頻遮蔽",
    "titleEn": "Package RF shielding",
    "focus": "遮罩接地與回流連續性",
    "focusEn": "Shield grounding and continuous return"
  },
  "a136": {
    "family": "rlc",
    "title": "封裝寄生參數萃取",
    "titleEn": "Package parasitic extraction",
    "focus": "等效 R、L、C 與量測埠",
    "focusEn": "Equivalent R, L, C and measurement ports"
  },
  "a137": {
    "family": "decap",
    "title": "封裝內去耦電容整合",
    "titleEn": "In-package decoupling-capacitor integration",
    "focus": "去耦電容與連接電感",
    "focusEn": "Decoupling capacitor and connection inductance"
  },
  "a138": {
    "family": "converter",
    "title": "共封裝電源轉換器",
    "titleEn": "Co-packaged power converters",
    "focus": "轉換器、電感與負載",
    "focusEn": "Converter, inductor and load"
  },
  "a139": {
    "family": "tim",
    "title": "散熱蓋與熱介面材料",
    "titleEn": "Heat spreaders and thermal-interface materials",
    "focus": "晶粒、熱介面層與散熱蓋",
    "focusEn": "Die, thermal interface and heat spreader"
  },
  "a140": {
    "family": "cooling",
    "title": "微流道晶片冷卻",
    "titleEn": "Microchannel chip cooling",
    "focus": "進出口、流道與壓降",
    "focusEn": "Inlet, channels and pressure drop"
  },
  "a141": {
    "family": "hermetic",
    "title": "氣密封裝與漏率檢測",
    "titleEn": "Hermetic packaging and leak testing",
    "focus": "密封環與示蹤氣體檢測",
    "focusEn": "Seal ring and tracer-gas detection"
  },
  "a142": {
    "family": "vacuum",
    "title": "晶圓級真空封裝",
    "titleEn": "Wafer-level vacuum packaging",
    "focus": "封帽、吸氣劑與低壓腔體",
    "focusEn": "Cap, getter and low-pressure cavity"
  },
  "a143": {
    "family": "sinter",
    "title": "功率模組銀燒結接合",
    "titleEn": "Silver-sintered power-module bonding",
    "focus": "銀顆粒頸部成長與殘孔",
    "focusEn": "Silver-particle neck growth and residual pores"
  },
  "a144": {
    "family": "doublecool",
    "title": "功率模組雙面散熱",
    "titleEn": "Double-sided cooling of power modules",
    "focus": "功率晶粒的上下散熱面",
    "focusEn": "Top and bottom cooling faces of a power die"
  },
  "a145": {
    "family": "ceramic",
    "title": "陶瓷直接覆銅基板",
    "titleEn": "Direct-bonded-copper ceramic substrates",
    "focus": "銅／陶瓷／銅三層結構",
    "focusEn": "Copper / ceramic / copper layers"
  },
  "a146": {
    "family": "cycling",
    "title": "封裝溫度循環可靠度",
    "titleEn": "Package thermal-cycling reliability",
    "focus": "溫度循環歷程與電性檢查",
    "focusEn": "Temperature cycle and electrical inspection"
  },
  "a147": {
    "family": "moisture",
    "title": "封裝濕氣敏感度分析",
    "titleEn": "Package moisture-sensitivity analysis",
    "focus": "水分擴散、介面與脫層",
    "focusEn": "Moisture diffusion, interface and delamination"
  },
  "a148": {
    "family": "fatigue",
    "title": "焊點疲勞壽命建模",
    "titleEn": "Solder-joint fatigue-life modeling",
    "focus": "焊點剪應變與循環損傷",
    "focusEn": "Solder-joint shear strain and cyclic damage"
  },
  "a149": {
    "family": "acoustic",
    "title": "封裝聲學顯微檢測",
    "titleEn": "Acoustic microscopy for package inspection",
    "focus": "入射超音波與界面回波",
    "focusEn": "Incident ultrasound and interface echoes"
  },
  "a150": {
    "family": "ct",
    "title": "封裝 X 光電腦斷層檢測",
    "titleEn": "Package X-ray computed-tomography inspection",
    "focus": "旋轉投影與重建切片",
    "focusEn": "Rotating projections and reconstructed slices"
  },
  "a151": {
    "family": "soiwave",
    "title": "矽光子 SOI 波導製作",
    "titleEn": "SOI waveguide fabrication for silicon photonics",
    "focus": "矽核心、埋氧與矽基板",
    "focusEn": "Silicon core, buried oxide and silicon substrate"
  },
  "a152": {
    "family": "sinwave",
    "title": "氮化矽低損耗波導",
    "titleEn": "Low-loss silicon-nitride waveguides",
    "focus": "氮化矽核心與氧化物包覆",
    "focusEn": "Silicon-nitride core and oxide cladding"
  },
  "a153": {
    "family": "swg",
    "title": "次波長光柵波導",
    "titleEn": "Subwavelength-grating waveguides",
    "focus": "次波長分段與等效光學傳播",
    "focusEn": "Subwavelength segmentation and effective propagation"
  },
  "a154": {
    "family": "grating",
    "title": "光柵耦合器設計",
    "titleEn": "Grating-coupler design",
    "focus": "表面光柵與傾斜入射光纖",
    "focusEn": "Surface grating and tilted input fiber"
  },
  "a155": {
    "family": "edge",
    "title": "晶片邊緣耦合器設計",
    "titleEn": "Edge-coupler design",
    "focus": "逆錐形波導與端面模式轉換",
    "focusEn": "Inverse taper and facet mode conversion"
  },
  "a156": {
    "family": "activealign",
    "title": "光纖陣列主動對準",
    "titleEn": "Active alignment of fiber arrays",
    "focus": "光功率回饋與多軸對準",
    "focusEn": "Optical-power feedback and multiaxis alignment"
  },
  "a157": {
    "family": "passivealign",
    "title": "光纖陣列被動對準",
    "titleEn": "Passive alignment of fiber arrays",
    "focus": "V 溝、止擋與機械公差",
    "focusEn": "V-grooves, stops and mechanical tolerance"
  },
  "a158": {
    "family": "adhesive",
    "title": "光纖黏著固定與熱漂移",
    "titleEn": "Fiber adhesive attachment and thermal drift",
    "focus": "黏著點、固化收縮與端面位移",
    "focusEn": "Adhesive spots, cure shrinkage and facet motion"
  },
  "a159": {
    "family": "polarization",
    "title": "偏振分光旋轉器",
    "titleEn": "Polarization splitter-rotators",
    "focus": "偏振旋轉與兩路分離",
    "focusEn": "Polarization rotation and two-path separation"
  },
  "a160": {
    "family": "mmi",
    "title": "多模干涉分光器",
    "titleEn": "Multimode-interference splitters",
    "focus": "多模區中的自成像與分光",
    "focusEn": "Self-imaging and splitting in a multimode region"
  },
  "a161": {
    "family": "directional",
    "title": "方向耦合器製作",
    "titleEn": "Directional-coupler fabrication",
    "focus": "相鄰波導倏逝場能量交換",
    "focusEn": "Evanescent coupling between neighboring guides"
  },
  "a162": {
    "family": "mzi",
    "title": "馬赫曾德爾調變器",
    "titleEn": "Mach-Zehnder modulators",
    "focus": "分光、兩臂相位差與干涉",
    "focusEn": "Split, differential phase and interference"
  },
  "a163": {
    "family": "ring",
    "title": "微環調變器",
    "titleEn": "Microring modulators",
    "focus": "總線、微環與共振調變",
    "focusEn": "Bus, microring and resonant modulation"
  },
  "a164": {
    "family": "detector",
    "title": "鍺光偵測器整合",
    "titleEn": "Germanium photodetector integration",
    "focus": "鍺吸收區、載子與讀出",
    "focusEn": "Germanium absorber, carriers and readout"
  },
  "a165": {
    "family": "avalanche",
    "title": "鍺矽雪崩光偵測器",
    "titleEn": "Germanium-silicon avalanche photodetectors",
    "focus": "吸收區與倍增區分開設計",
    "focusEn": "Separate absorption and multiplication regions"
  },
  "a166": {
    "family": "heater",
    "title": "矽光子熱光相移器",
    "titleEn": "Silicon-photonic thermo-optic phase shifters",
    "focus": "電阻加熱器與熱光相位",
    "focusEn": "Resistive heater and thermo-optic phase"
  },
  "a167": {
    "family": "junction",
    "title": "載子耗盡相位調變",
    "titleEn": "Carrier-depletion phase modulation",
    "focus": "反向偏壓 PN 接面與耗盡區",
    "focusEn": "Reverse-biased PN junction and depletion region"
  },
  "a168": {
    "family": "ln",
    "title": "薄膜鈮酸鋰異質整合",
    "titleEn": "Heterogeneous thin-film lithium-niobate integration",
    "focus": "鈮酸鋰薄膜、波導與電極",
    "focusEn": "Lithium-niobate film, waveguide and electrodes"
  },
  "a169": {
    "family": "iiivlaser",
    "title": "III-V 雷射與矽晶片接合",
    "titleEn": "III-V laser bonding to silicon chips",
    "focus": "III-V 增益層與矽波導接合",
    "focusEn": "III-V gain layer bonded to a silicon waveguide"
  },
  "a170": {
    "family": "transferlaser",
    "title": "微轉印雷射晶粒整合",
    "titleEn": "Micro-transfer-printed laser integration",
    "focus": "彈性印章轉移微型雷射",
    "focusEn": "Elastomeric stamp transfers micro-lasers"
  },
  "a171": {
    "family": "qdlaser",
    "title": "矽上量子點雷射研究",
    "titleEn": "Quantum-dot lasers on silicon research",
    "focus": "量子點增益層與缺陷隔離",
    "focusEn": "Quantum-dot gain layers and defect isolation"
  },
  "a172": {
    "family": "external",
    "title": "外接光源光引擎",
    "titleEn": "External-laser optical engines",
    "focus": "外接雷射與封裝光分配",
    "focusEn": "External laser and package optical distribution"
  },
  "a173": {
    "family": "soa",
    "title": "半導體光放大器整合",
    "titleEn": "Semiconductor optical-amplifier integration",
    "focus": "行波增益區、輸入與輸出",
    "focusEn": "Traveling-wave gain region, input and output"
  },
  "a174": {
    "family": "awg",
    "title": "波分多工陣列波導光柵",
    "titleEn": "Arrayed-waveguide gratings for wavelength multiplexing",
    "focus": "固定臂長差與兩端自由傳播區",
    "focusEn": "Incremental arm length and free-propagation regions"
  },
  "a175": {
    "family": "ringfilter",
    "title": "微環波分多工濾波器",
    "titleEn": "Microring wavelength-multiplexing filters",
    "focus": "多環濾波與通道丟取",
    "focusEn": "Multiple rings and wavelength drop channels"
  },
  "a176": {
    "family": "switch",
    "title": "光子晶片光開關矩陣",
    "titleEn": "Photonic-chip optical-switch matrices",
    "focus": "交叉點或干涉式開關路由",
    "focusEn": "Crosspoint or interferometric switch routing"
  },
  "a177": {
    "family": "mesh",
    "title": "可程式化光子電路",
    "titleEn": "Programmable photonic circuits",
    "focus": "可調干涉單元形成可程式網格",
    "focusEn": "Tunable interferometers form a programmable mesh"
  },
  "a178": {
    "family": "coherent",
    "title": "相干光接收器整合",
    "titleEn": "Coherent optical-receiver integration",
    "focus": "訊號、本地振盪器與平衡偵測",
    "focusEn": "Signal, local oscillator and balanced detection"
  },
  "a179": {
    "family": "opa",
    "title": "光子相位陣列",
    "titleEn": "Optical phased arrays",
    "focus": "相位控制陣列與遠場波束",
    "focusEn": "Phase-controlled array and far-field beam"
  },
  "a180": {
    "family": "lidar",
    "title": "FMCW 光達光子晶片",
    "titleEn": "FMCW lidar photonic chips",
    "focus": "掃頻、目標回波與拍頻",
    "focusEn": "Frequency sweep, target return and beat frequency"
  },
  "a181": {
    "family": "biosensor",
    "title": "矽光子生物感測器",
    "titleEn": "Silicon-photonic biosensors",
    "focus": "表面結合、參考通道與光學讀出",
    "focusEn": "Surface binding, reference and optical readout"
  },
  "a182": {
    "family": "midinfrared",
    "title": "中紅外積體光子感測",
    "titleEn": "Mid-infrared integrated-photonic sensing",
    "focus": "分子吸收、窗口與背景參考",
    "focusEn": "Molecular absorption, window and reference background"
  },
  "a183": {
    "family": "comb",
    "title": "矽光子頻率梳",
    "titleEn": "Silicon-photonic frequency combs",
    "focus": "泵浦、共振腔與等距頻率線",
    "focusEn": "Pump, resonator and evenly spaced spectral lines"
  },
  "a184": {
    "family": "quantum",
    "title": "光子晶片量子光源",
    "titleEn": "Quantum light sources on photonic chips",
    "focus": "泵浦、成對光子與巧合計數",
    "focusEn": "Pump, photon pairs and coincidence counts"
  },
  "a185": {
    "family": "opticalprobe",
    "title": "光子晶片晶圓級光測試",
    "titleEn": "Wafer-level optical testing of photonic chips",
    "focus": "光纖探針、晶圓與電性探針",
    "focusEn": "Optical probe, wafer and electrical probes"
  },
  "a186": {
    "family": "thermomech",
    "title": "光子封裝熱機耦合分析",
    "titleEn": "Thermomechanical analysis of photonic packages",
    "focus": "溫度場→變形→光學耦合",
    "focusEn": "Temperature field → deformation → optical coupling"
  },
  "a187": {
    "family": "feedback",
    "title": "光路溫度漂移補償",
    "titleEn": "Optical-path thermal-drift compensation",
    "focus": "監測器、控制器與相位補償",
    "focusEn": "Monitor, controller and phase correction"
  },
  "a188": {
    "family": "reroute",
    "title": "光子封裝失效重路由",
    "titleEn": "Failure rerouting in photonic packages",
    "focus": "失效支路與備援光路",
    "focusEn": "Failed branch and backup optical path"
  },
  "a189": {
    "family": "stressphase",
    "title": "封裝應力對光學相位的影響",
    "titleEn": "Package-stress effects on optical phase",
    "focus": "應力、折射率張量與相位",
    "focusEn": "Stress, index tensor and optical phase"
  },
  "a190": {
    "family": "pdk",
    "title": "光子晶片製程設計套件",
    "titleEn": "Photonic process-design kits",
    "focus": "元件模型、版圖、規則與驗證",
    "focusEn": "Device models, layout, rules and verification"
  },
  "a191": {
    "family": "cpo",
    "title": "共封裝光學交換器整合",
    "titleEn": "Co-packaged-optics switch integration",
    "focus": "交換晶片周邊的封裝光引擎",
    "focusEn": "Packaged optical engines around a switch die"
  },
  "a192": {
    "family": "opticalio",
    "title": "光學輸入輸出小晶片",
    "titleEn": "Optical I/O chiplets",
    "focus": "運算小晶片與光學 I/O 介面",
    "focusEn": "Compute chiplet and optical-I/O interface"
  },
  "a193": {
    "family": "codesign",
    "title": "光子與電子晶片共同設計",
    "titleEn": "Photonic-electronic co-design",
    "focus": "驅動、光子元件與熱共同迭代",
    "focusEn": "Driver, photonic device and thermal iteration"
  },
  "a194": {
    "family": "emc",
    "title": "高速光模組電磁相容性",
    "titleEn": "Electromagnetic compatibility of high-speed optical modules",
    "focus": "高速回流、屏蔽與共模耦合",
    "focusEn": "High-speed return, shielding and common-mode coupling"
  },
  "a195": {
    "family": "interlock",
    "title": "光收發器雷射安全與互鎖",
    "titleEn": "Optical-transceiver laser safety and interlocks",
    "focus": "互鎖狀態、光路封閉與發光許可",
    "focusEn": "Interlock state, enclosed path and emission permission"
  },
  "a196": {
    "family": "cowos",
    "title": "台積電 CoWoS 整合案例",
    "titleEn": "TSMC CoWoS integration case study",
    "focus": "邏輯、HBM 與中介層整合概念",
    "focusEn": "Logic, HBM and interposer integration concept"
  },
  "a197": {
    "family": "soic",
    "title": "台積電 SoIC 堆疊整合案例",
    "titleEn": "TSMC SoIC stacking case study",
    "focus": "垂直細間距接合的概念",
    "focusEn": "Concept of fine-pitch vertical bonding"
  },
  "a198": {
    "family": "foveros",
    "title": "Intel Foveros 封裝案例",
    "titleEn": "Intel Foveros packaging case study",
    "focus": "基底晶粒與上層晶粒堆疊概念",
    "focusEn": "Concept of base die and stacked top die"
  },
  "a199": {
    "family": "emib",
    "title": "Intel EMIB 互連橋案例",
    "titleEn": "Intel EMIB bridge case study",
    "focus": "封裝內局部互連橋概念",
    "focusEn": "Concept of local embedded interconnect bridge"
  },
  "a200": {
    "family": "isipp",
    "title": "imec iSiPP 矽光子平台",
    "titleEn": "imec iSiPP silicon-photonics platform",
    "focus": "被動光路、調變、偵測與封裝介面",
    "focusEn": "Passive paths, modulation, detection and package interface"
  }
});
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const C={ink:'#17384a',blue:'#4d85a4',light:'#dce9ec',gold:'#ddb15d',si:'#adc0cb',oxide:'#e8d7b1',green:'#6eaea1',red:'#c86e70',pale:'#f1f6f3',violet:'#9a82ae'};
const rect=(x,y,w,h,f=C.si,rx=3)=>`<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${rx}" fill="${f}" stroke="${C.ink}" stroke-width="1.4"/>`;
const path=(d,f='none',s=C.ink,w=2)=>`<path d="${d}" fill="${f}" stroke="${s}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"/>`;
const line=(x,y,a,b,c=C.ink,w=2)=>path(`M${x} ${y}L${a} ${b}`,'none',c,w);
const circle=(x,y,r,f=C.gold)=>`<circle cx="${x}" cy="${y}" r="${r}" fill="${f}" stroke="${C.ink}" stroke-width="1.5"/>`;
const text=(x,y,s,size=13,c=C.ink,anchor='middle')=>`<text x="${x}" y="${y}" text-anchor="${anchor}" font-family="system-ui,sans-serif" font-size="${size}" fill="${c}">${esc(s)}</text>`;
const arrow=(x,y,a,b,c=C.blue)=>{const t=Math.atan2(b-y,a-x),r=8;return line(x,y,a,b,c,2.5)+path(`M${a-r*Math.cos(t-.5)} ${b-r*Math.sin(t-.5)}L${a} ${b}L${a-r*Math.cos(t+.5)} ${b-r*Math.sin(t+.5)}`,'none',c,2.5)};
const many=(n,fn)=>Array.from({length:n},(_,i)=>fn(i)).join('');
const layer=(y,h=20,f=C.si)=>rect(132,y,336,h,f);
const bumps=(y,count=8)=>many(count,i=>circle(159+i*282/(count-1),y,6,C.gold));
const die=(x,y,w=120,h=40)=>rect(x,y,w,h,C.blue)+many(4,i=>rect(x+8+i*(w-20)/4,y+9,(w-28)/4,12,C.light));
const wafer=(x,y,rx=160,ry=28)=>`<ellipse cx="${x}" cy="${y}" rx="${rx}" ry="${ry}" fill="${C.si}" stroke="${C.ink}" stroke-width="2"/>`+many(7,i=>line(x-rx*.75+i*rx*.25,y-ry*.55,x-rx*.75+i*rx*.25,y+ry*.55,C.light,1));
const via=(x,y,h=76,filled=true)=>rect(x,y,28,h,C.oxide)+rect(x+5,y,18,h,filled?C.gold:C.pale);
const fiber=(x,y,w=100)=>rect(x,y,w,14,C.light,7)+line(x,y+7,x+w,y+7,C.red,3);
const guide=(d,c=C.blue,w=7)=>path(d,'none',c,w);
const ring=(x,y,r=43)=>`<circle cx="${x}" cy="${y}" r="${r}" fill="none" stroke="${C.blue}" stroke-width="7"/>`;
const mzi=(x=165,y=170,w=270)=>guide(`M${x-55} ${y}H${x}Q${x+20} ${y} ${x+35} ${y-35}H${x+w-35}Q${x+w-20} ${y} ${x+w} ${y}H${x+w+35}`)+guide(`M${x} ${y}Q${x+20} ${y} ${x+35} ${y+35}H${x+w-35}Q${x+w-20} ${y} ${x+w} ${y}`);
const heat=(x,y)=>path(`M${x} ${y}q-12-12 0-24t0-24`,'none',C.red,3)+arrow(x,y-38,x,y-61,C.red);
const bond=(hybrid=false)=>layer(118,36)+layer(219,36)+many(6,i=>rect(160+i*50,154,22,hybrid?7:20,C.gold)+rect(160+i*50,hybrid?212:199,22,hybrid?7:20,C.gold))+many(3,i=>arrow(204+i*96,174,204+i*96,195,C.red));
const interposer=(isBridge=false)=>layer(229,23,C.green)+die(144,124,134)+die(331,124,134)+bumps(180,10)+rect(isBridge?255:140,190,isBridge?90:324,25,C.si)+many(isBridge?3:8,i=>via((isBridge?270:155)+i*(isBridge?22:40),210,18))+bumps(269,9);
export function packagingGeometry(f,{zh=true,labels=true}={}){
 const t=(a,b)=>zh?a:b, tx=(x,y,a,b,size=13)=>labels?text(x,y,t(a,b),size):'';
 switch(f){
 case 'pillar':return layer(237)+layer(218,18,C.oxide)+many(5,i=>rect(159+i*65,157,22,61,C.gold)+path(`M${159+i*65} 157Q${170+i*65} 131 ${181+i*65} 157`,C.si))+tx(300,110,'銅柱上方的焊帽','Solder caps above copper pillars');
 case 'bond':return bond()+rect(203,91,194,13,C.red)+arrow(300,76,300,111,C.red)+tx(488,143,'力／熱','Force / heat');
 case 'directbond':return bond()+tx(300,103,'銅表面活化與接觸','Copper activation and contact')+tx(300,283,'界面連續性需量測','Measure interface continuity');
 case 'waferbond':return wafer(300,126)+wafer(300,241)+many(8,i=>rect(170+i*36,143,12,6,C.gold)+rect(170+i*36,218,12,6,C.gold))+arrow(300,166,300,197)+tx(300,88,'晶圓對晶圓','Wafer to wafer');
 case 'diebond':return wafer(300,244)+die(230,110,140)+many(5,i=>rect(242+i*27,150,10,7,C.gold))+arrow(300,169,300,208)+tx(452,155,'已知良晶粒','Known-good die');
 case 'stack':return many(3,i=>die(190,117+i*57,220,30)+many(5,j=>via(209+j*39,147+i*57,16)))+tx(300,98,'逐層接合與測試','Bond and test each layer');
 case 'temporary':return layer(215,30)+layer(197,18,C.violet)+layer(175,22,C.blue)+path('M135 173Q239 127 354 148L467 174','none',C.blue,5)+arrow(377,161,403,124)+tx(300,278,'暫黏層 ≠ 永久接合界面','Temporary adhesive ≠ permanent bond');
 case 'grind':return wafer(300,240)+rect(209,99,179,22,C.ink)+rect(230,121,137,41,C.si)+many(8,i=>path(`M${231+i*17} 162v15`))+arrow(300,177,300,204)+tx(300,283,'背面研磨後量測厚度與損傷','Measure thickness and damage after grinding');
 case 'laserdice':return layer(190,64)+rect(283,85,35,42,C.red)+path('M286 127L300 212L314 127',C.gold)+many(8,i=>circle(164+i*39,218,3,C.red))+path('M302 191l-9 17 11 20-8 25','none',C.red)+tx(467,150,'內部焦點','Internal focus');
 case 'plasmadice':return layer(170,85)+many(3,i=>rect(204+i*90,170,16,85,C.pale)+arrow(212+i*90,96,212+i*90,156,C.violet))+many(4,i=>rect(136+i*90,155,64,15,C.gold))+tx(300,281,'深溝槽穿透薄化晶圓','Deep trenches through the thinned wafer');
 case 'pick':return wafer(300,250)+rect(280,82,40,55,C.si)+path('M280 137L265 157H335L320 137Z',C.blue)+die(270,168,60,22)+arrow(360,203,418,156)+rect(393,111,64,33,C.light)+tx(425,102,'視覺','Vision');
 case 'underfill':return layer(241,19)+die(155,140,290,55)+bumps(218)+path('M137 195H311Q331 218 311 240H137Z',C.green)+arrow(200,220,288,220)+tx(468,216,'排氣','Vent')+tx(300,113,'未固化液體毛細前緣','Capillary front before curing');
 case 'warpage':return path('M126 161Q300 93 474 161L474 193Q300 125 126 193Z',C.blue)+path('M126 194Q300 126 474 194L474 219Q300 151 126 219Z',C.gold)+arrow(158,253,443,253)+tx(300,281,'變形不等於材料自由膨脹差','Deformation is not free expansion mismatch');
 case 'fanout':return wafer(300,185,177,89)+many(6,i=>die(182+i%3*86,131+Math.floor(i/3)*65,65,38))+many(3,i=>path(`M${212+i*86} 170V255H${190+i*104}`,'none',C.gold,4));
 case 'panel':return rect(120,99,360,168,C.green)+many(12,i=>die(139+i%4*87,118+Math.floor(i/4)*48,59,28))+path('M210 99v168m90-168v168m90-168v168M120 154h360m-360 57h360','none',C.light,1)+tx(300,291,'分區畸變需量測','Measure distortion by region');
 case 'rdl':return layer(242,20)+layer(192,50,C.oxide)+rect(145,176,135,15,C.gold)+rect(330,220,130,15,C.gold)+rect(268,188,18,47,C.gold)+path('M280 185H380V224','none',C.gold,8)+tx(300,133,'金屬走線與介電開口','Metal routing and dielectric openings');
 case 'embed':return layer(135,114,C.green)+die(228,165,145,45)+many(4,i=>via(242+i*34,136,29))+path('M140 134H450M160 250H436','none',C.gold,7)+tx(300,283,'埋入晶粒的兩側互連','Connections around the embedded die');
 case 'sip':return layer(244,22,C.green)+die(137,176,104)+die(258,142,125,74)+rect(403,194,51,22,C.gold)+bumps(229,9)+tx(189,158,'感測','Sensor')+tx(319,124,'邏輯','Logic')+tx(429,182,'被動件','Passive');
 case 'viaetch':case 'viafill':case 'viareveal':case 'glassvia':return layer(142,f==='viareveal'?75:115,f==='glassvia'?C.light:C.si)+many(4,i=>via(175+i*77,142,115,f!=='viaetch'))+(f==='viareveal'?path('M121 221H480','none',C.red,2)+arrow(494,261,494,222):'')+tx(300,114,f==='viaetch'?'側壁絕緣包覆開口':f==='viafill'?'金屬芯與周圍絕緣':f==='glassvia'?'玻璃基底穿孔':'背面露出與隔離','Via cross section; sidewall and fill differ');
 case 'interposer':case 'package':return interposer()+tx(300,102,'晶粒－中介層－基板','Dies — interposer — substrate');
 case 'bridge':case 'emib':return interposer(true)+tx(300,103,'局部橋；並非全面中介層','Local bridge, not a full-area interposer');
 case 'organic':case 'build-up':case 'glasscore':return layer(167,50,f==='glasscore'?C.light:C.green)+many(4,i=>layer(117+i*34,12,C.oxide))+many(4,i=>rect(159+i*68,130+i*17,17,20,C.gold)+path(`M${159+i*68} ${129+i*17}h55`,'none',C.gold,6))+tx(300,273,f==='glasscore'?'玻璃核心與微通孔增層':f==='organic'?'有機介電層中的多層走線':'增層介電質與交錯微通孔','Core and staggered build-up interconnects');
 case 'chiplet':return die(128,148,134,73)+die(351,148,134,73)+many(4,i=>arrow(267,163+i*14,342,163+i*14,i%2?C.blue:C.gold))+tx(195,132,'傳送／接收','TX / RX')+tx(418,132,'傳送／接收','TX / RX')+tx(300,262,'通道、時脈與錯誤檢查','Channel, clock and error checking');
 case 'hbm':case 'cowos':return layer(246,24)+die(132,169,170,48)+many(4,i=>die(354,113+i*28,114,20))+many(3,i=>via(367+i*34,226,18))+tx(216,150,'邏輯','Logic')+tx(410,91,'記憶體堆疊','Memory stack');
 case 'thermal':return many(3,i=>die(217,144+i*37,166,25))+layer(107,20,C.gold)+many(3,i=>heat(249+i*48,101))+arrow(190,240,146,153,C.red)+arrow(409,240,455,153,C.red)+tx(300,293,'共享散熱路徑與熱耦合','Shared heat paths and thermal coupling');
 case 'pdn':return die(335,143,137,82)+rect(128,135,87,100,C.green)+path('M216 158H334M216 211H334','none',C.gold,7)+line(275,158,275,178)+line(263,178,287,178,C.blue,4)+line(263,190,287,190,C.blue,4)+line(275,190,275,211)+tx(300,280,'電流迴路與阻抗','Current loop and impedance');
 case 'signal':return layer(222,25,C.green)+path('M127 148H260Q290 148 300 166T342 184H477M127 173H249Q279 173 289 191T338 209H477','none',C.gold,6)+tx(300,111,'差分對與連續回流面','Differential pair and continuous return');
 case 'shield':case 'emc':return layer(250,20,C.green)+die(216,175,168,52)+path('M141 246V126H461V246','none',C.si,12)+many(4,i=>via(149+i*100,247,20))+arrow(487,120,530,86,C.red)+(f==='emc'?path('M193 237H410V281H190Z','none',C.red,3):'')+tx(300,108,'屏蔽罩與接地邊界','Shield enclosure and ground boundary');
 case 'rlc':return path('M111 185H178l8-14 13 28 13-28 13 28 8-14H258q7-26 14 0q7-26 14 0q7-26 14 0H339M339 163v45m14-45v45M353 185H488')+text(201,139,'R')+text(280,139,'L')+text(347,139,'C')+circle(111,185,5)+circle(488,185,5)+tx(300,251,'頻率範圍決定模型有效性','Frequency range bounds model validity');
 case 'decap':return layer(252,18,C.green)+die(367,169,107,54)+rect(175,175,92,31,C.light)+line(196,145,196,175)+line(240,206,240,251)+path('M196 145H409V169M409 223V252','none',C.gold,5)+tx(220,127,'低迴路電感','Low loop inductance');
 case 'converter':return rect(112,148,105,71,C.green)+path('M217 182H245q8-28 16 0q8-28 16 0q8-28 16 0H376')+die(376,148,116,71)+tx(164,188,'轉換器','Converter')+tx(285,144,'L','L')+tx(300,271,'局部供電減少路徑損失','Local delivery reduces path loss');
 case 'tim':return layer(121,28,C.si)+layer(167,18,C.gold)+die(215,197,170,44)+many(3,i=>arrow(253+i*48,192,253+i*48,93,C.red))+tx(490,180,'TIM','TIM');
 case 'cooling':return rect(139,112,322,142,C.blue)+many(5,i=>rect(170,126+i*24,260,13,C.light,6))+path('M149 130V235M451 130V235','none',C.light,12)+arrow(90,143,137,143)+arrow(464,228,516,228)+tx(300,285,'熱移除與壓降一起評估','Evaluate heat removal and pressure drop');
 case 'hermetic':return layer(248,22)+path('M151 242V126H449V242','none',C.si,15)+die(220,194,160,42)+many(4,i=>circle(182+i*72,101,5,C.gold))+arrow(480,170,526,170)+tx(300,283,'漏率量測不等於目視密封','Leak measurement differs from visual closure');
 case 'vacuum':return layer(249,19)+path('M150 243V123H450V243','none',C.blue,13)+rect(189,134,54,12,C.gold)+rect(256,209,95,28,C.green)+tx(220,176,'吸氣劑','Getter')+tx(333,174,'低壓腔','Low-pressure cavity');
 case 'sinter':return layer(239,20)+layer(120,20,C.blue)+many(18,i=>circle(165+i%6*53,166+Math.floor(i/6)*26,16,C.si))+tx(300,102,'頸部成長與孔隙率','Neck growth and porosity');
 case 'doublecool':return layer(99,22,C.blue)+layer(141,13,C.gold)+die(214,174,173,40)+layer(233,13,C.gold)+layer(269,22,C.blue)+many(3,i=>arrow(247+i*53,165,247+i*53,124,C.red)+arrow(247+i*53,219,247+i*53,263,C.red));
 case 'ceramic':return layer(139,24,C.gold)+layer(163,63,C.oxide)+layer(226,24,C.gold)+tx(300,201,'AlN / Al₂O₃ / Si₃N₄','AlN / Al₂O₃ / Si₃N₄')+tx(300,280,'材料等級與製程需分別驗證','Verify material grade and process separately');
 case 'cycling':return path('M118 103V256H479')+path('M132 228H174V132H237V228H301V132H365V228H429V132H474','none',C.red,3)+tx(300,290,'循環時間、停留與量測點','Cycle timing, dwell and measurement points');
 case 'moisture':return layer(149,92,C.green)+die(233,174,134,36)+many(6,i=>arrow(153+i*57,88,165+i*50,136,C.blue))+path('M237 216Q300 240 367 216','none',C.red,5)+tx(300,280,'吸水與界面脫層需分別檢查','Separate moisture uptake from delamination');
 case 'fatigue':return layer(125,25,C.blue)+layer(242,24,C.green)+many(4,i=>path(`M${171+i*75} 159q-22 38 0 71h27q22-33 0-71Z`,C.gold))+path('M268 211l-12 5 11 7-10 8','none',C.red,3)+arrow(160,104,276,104)+arrow(436,287,320,287);
 case 'acoustic':return layer(212,43,C.green)+rect(177,112,59,40,C.blue)+path('M189 156L217 211L246 156','none',C.blue)+path('M315 248V116M315 248H493M325 240H349V188H357V240H408V148H415V240H484','none',C.red)+tx(390,281,'飛行時間與回波','Time of flight and echo');
 case 'ct':return rect(106,164,42,45,C.gold)+rect(450,130,35,112,C.blue)+rect(270,151,71,68,C.green)+path('M148 187L451 132M148 187L451 242','none',C.gold)+path('M263 260Q365 270 376 179','none',C.red)+arrow(376,179,367,156,C.red)+tx(300,104,'旋轉物體與多角度投影','Rotation and angular projections');
 case 'soiwave':case 'sinwave':return layer(230,24,C.si)+layer(155,75,C.oxide)+rect(250,155,100,38,f==='sinwave'?C.green:C.blue)+path('M212 174Q300 115 388 174Q300 241 212 174Z','none',C.red,2)+tx(300,112,f==='sinwave'?'氮化矽核心':'矽核心',f==='sinwave'?'Silicon nitride core':'Silicon core');
 case 'swg':return layer(216,28,C.oxide)+many(12,i=>rect(147+i*27,158,15,57,C.blue))+arrow(120,139,478,139,C.red)+tx(300,282,'週期需小於適用的繞射尺度','Period below the applicable diffraction scale');
 case 'grating':return layer(241,22,C.oxide)+rect(306,218,173,21,C.blue)+many(7,i=>rect(136+i*24,219,14,21,C.blue))+path('M178 95L252 211M190 88L264 204','none',C.si,6)+arrow(207,126,257,206,C.red)+tx(300,286,'光纖角度與繞射耦合','Fiber angle and diffractive coupling');
 case 'edge':return fiber(98,187,115)+path('M219 192L444 161V227L219 200Z',C.blue)+line(215,155,215,243,C.ink,1)+path('M151 194Q208 163 285 194Q208 225 151 194Z','none',C.red)+tx(300,113,'端面與逆錐形模式轉換','Facet and inverse-taper mode conversion');
 case 'activealign':return fiber(97,176,140)+die(305,157,135,60)+arrow(216,142,265,142)+arrow(260,128,260,168)+path('M435 187H499V255H177V207','none',C.green,3)+tx(328,281,'量測功率回饋','Measured-power feedback');
 case 'passivealign':return path('M113 216L163 261L213 216L263 261L313 216L363 261L413 216L463 261L491 216V285H113Z',C.si)+many(4,i=>circle(163+i*100,216,27,C.light))+rect(158,101,297,35,C.blue)+tx(300,173,'幾何基準與公差鏈','Mechanical datums and tolerance chain');
 case 'adhesive':return fiber(103,180,159)+die(319,159,138,60)+many(3,i=>circle(178+i*104,237,14,C.violet))+arrow(275,147,312,175,C.red)+tx(300,108,'固化與溫變後重新量測','Re-measure after cure and temperature change');
 case 'polarization':return guide('M101 183H229Q276 183 310 142H492')+guide('M229 183Q276 183 310 227H492')+arrow(135,148,135,171,C.red)+arrow(428,120,458,120,C.red)+arrow(444,238,444,267,C.red)+tx(300,104,'TE / TM 轉換及分路','TE / TM conversion and separation');
 case 'mmi':return guide('M103 190H204')+rect(204,136,194,108,C.blue)+guide('M398 161H497M398 219H497')+path('M205 190Q278 120 395 161M205 190Q278 263 395 219','none',C.gold,3)+tx(300,105,'多模干涉區','Multimode interference region');
 case 'directional':return guide('M113 121Q204 121 235 169H377Q408 121 495 121M113 267Q204 267 235 219H377Q408 267 495 267')+many(3,i=>arrow(266+i*45,182,266+i*45,207,C.gold))+tx(300,103,'間隙與耦合長度','Gap and coupling length');
 case 'mzi':return mzi()+rect(225,121,153,10,C.gold)+tx(300,104,'差動相位 Δφ','Differential phase Δφ')+tx(300,269,'兩臂干涉改變輸出強度','Interference changes output intensity');
 case 'ring':return guide('M109 246H492')+ring(300,192,46)+rect(268,109,64,16,C.gold)+line(278,125,278,145)+line(320,125,320,145)+tx(300,90,'調變接面與共振環','Modulation junction and resonant ring');
 case 'detector':case 'avalanche':return guide('M106 220H490')+rect(222,175,154,34,C.violet)+rect(222,157,28,18,C.gold)+rect(348,157,28,18,C.gold)+arrow(264,128,284,163,C.red)+arrow(316,130,335,163,C.red)+(f==='avalanche'?rect(299,175,23,34,C.gold)+tx(300,115,'吸收區／倍增區','Absorber / multiplier'):tx(300,116,'光子 → 電子與電洞','Photons → electrons and holes'));
 case 'heater':return guide('M119 227H483')+path('M169 145h33v40h32v-40h32v40h32v-40h32v40h32v-40h49','none',C.gold,7)+many(4,i=>arrow(209+i*61,197,209+i*61,216,C.red))+tx(300,115,'熱場改變有效折射率','Temperature changes effective index');
 case 'junction':return layer(238,22,C.oxide)+rect(144,173,313,50,C.blue)+rect(144,173,126,50,C.red)+rect(282,173,175,50,C.green)+rect(270,165,12,66,C.light)+text(208,205,'p')+text(372,205,'n')+path('M175 173V121H253M413 173V121H302')+text(278,126,'− / +');
 case 'ln':return layer(238,22)+layer(210,28,C.oxide)+layer(177,33,C.violet)+rect(267,147,66,30,C.violet)+rect(161,146,80,22,C.gold)+rect(359,146,80,22,C.gold)+arrow(245,160,351,160,C.blue)+tx(300,111,'電場與光場重疊','Electrical and optical mode overlap');
 case 'iiivlaser':return layer(239,22,C.oxide)+guide('M120 226H483')+rect(210,188,184,17,C.violet)+rect(210,162,184,25,C.green)+rect(243,140,118,22,C.gold)+tx(300,110,'III-V 增益區 / 矽導波','III-V gain / silicon guiding');
 case 'transferlaser':return rect(197,98,208,31,C.violet)+many(3,i=>die(219+i*57,134,43,21))+arrow(300,171,300,211)+layer(242,21,C.oxide)+many(3,i=>rect(219+i*57,223,43,19,C.green))+tx(300,280,'轉印位置與耦合界面','Transfer position and coupling interface');
 case 'qdlaser':return layer(236,23,C.si)+layer(200,35,C.oxide)+many(3,j=>layer(146+j*18,13,C.violet)+many(9,i=>circle(157+i*35,149+j*18,3,C.gold)))+tx(300,109,'點狀增益層；非晶格比例圖','Dot gain layers; not a scaled lattice');
 case 'external':return rect(112,140,106,69,C.red)+fiber(218,167,120)+rect(338,113,147,131,C.light)+guide('M339 174H370L418 135M370 174L418 215')+tx(163,182,'雷射','Laser')+tx(412,271,'光分配','Light distribution');
 case 'soa':return guide('M105 192H494')+rect(215,162,178,61,C.violet)+arrow(134,155,190,155,C.red)+arrow(415,145,490,145,C.red)+arrow(415,160,490,160,C.red)+tx(300,125,'受激放大與雜訊','Stimulated amplification and noise');
 case 'awg':return path('M148 184L225 130V242Z',C.light)+path('M451 184L377 130V242Z',C.light)+guide('M98 184H148M451 184H505')+many(5,i=>guide(`M225 ${144+i*21}C${255-i*20} ${54+i*37} ${347+i*20} ${54+i*37} 377 ${144+i*21}`,C.blue,3))+tx(300,282,'相鄰臂長差 ΔL','Adjacent-arm length increment ΔL');
 case 'ringfilter':return guide('M111 229H496')+many(3,i=>ring(198+i*107,189,32)+guide(`M${160+i*107} 150H${237+i*107}`,C.green,4))+tx(300,109,'λ₁ / λ₂ / λ₃ 分波','λ₁ / λ₂ / λ₃ wavelength channels');
 case 'switch':return many(3,i=>guide(`M125 ${136+i*52}H470`,C.blue,3)+guide(`M${204+i*91} 107V279`,C.green,3))+many(9,i=>circle(204+i%3*91,136+Math.floor(i/3)*52,8,i===4?C.gold:C.light))+tx(300,300,'交叉點可選路由','Selectable crosspoints');
 case 'mesh':return many(3,i=>many(2,j=>path(`M${127+i*124} ${137+j*86}l37-27 37 27-37 27Z`,C.light)+rect(150+i*124,128+j*86,28,18,C.gold)))+many(2,i=>many(2,j=>line(201+i*124,137+j*86,251+i*124,137+j*86,C.blue,4)))+tx(300,295,'可調單元與校準矩陣','Tunable cells and calibration matrix');
 case 'coherent':return guide('M108 143H234M108 242H234')+rect(234,116,141,151,C.light)+many(4,i=>guide(`M375 ${140+i*34}H426`,C.blue,3)+rect(431,130+i*34,48,19,C.violet))+text(304,193,'90°')+tx(165,124,'訊號','Signal')+tx(165,272,'本地振盪器','Local oscillator');
 case 'opa':return many(6,i=>guide(`M140 ${121+i*27}H339`,C.blue,3)+rect(219,113+i*27,48,16,C.gold)+path(`M343 ${121+i*27}L365 ${114+i*27}L365 ${128+i*27}Z`,C.blue)+arrow(374,121+i*27,462,99+i*19,C.red))+tx(300,301,'單元相位控制遠場方向','Element phases set the far-field direction');
 case 'lidar':return rect(105,147,103,61,C.red)+rect(283,126,108,95,C.light)+path('M208 175H283M391 159H486V192H391','none',C.blue,4)+rect(488,113,25,133,C.si)+path('M337 222V272H217')+tx(156,178,'掃頻光','Chirp')+tx(336,180,'混頻','Mix')+tx(286,295,'拍頻 → 距離（需校準）','Beat → range (calibrated)');
 case 'biosensor':return guide('M109 235H491')+ring(300,179,47)+many(7,i=>circle(265+i*11,122+(i%2)*9,5,C.gold))+tx(300,97,'表面結合與參考測量','Surface binding and reference measurement');
 case 'midinfrared':return guide('M110 236H489')+rect(194,107,215,111,C.light)+many(8,i=>circle(222+i%4*52,143+Math.floor(i/4)*41,6,C.gold)+circle(234+i%4*52,143+Math.floor(i/4)*41,5,C.red))+arrow(139,235,175,235,C.red)+tx(300,282,'吸收譜須扣除背景','Subtract background from absorption spectra');
 case 'comb':return ring(205,176,44)+guide('M116 229H282')+arrow(277,176,323,176)+path('M346 243V115M346 243H504')+many(9,i=>line(357+i*16,242,357+i*16,218-Math.sin(i/8*Math.PI)*76,C.red,3))+tx(427,277,'頻率 comb','Frequency comb');
 case 'quantum':return rect(203,151,164,61,C.light)+arrow(104,181,199,181,C.red)+arrow(371,166,463,127,C.blue)+arrow(371,196,463,242,C.green)+circle(477,123,16,C.blue)+circle(477,248,16,C.green)+tx(288,185,'非線性','Nonlinear')+tx(300,279,'巧合計數不是兩束經典光','Coincidence counts, not two classical beams');
 case 'opticalprobe':return wafer(300,244,172,48)+fiber(131,126,97)+path('M228 133L285 210','none',C.red,5)+rect(374,108,56,24,C.gold)+many(3,i=>path(`M${382+i*17} 132v47l-13 39`))+tx(300,291,'光與電量測座標需共註冊','Register optical and electrical coordinates');
 case 'thermomech':return rect(114,141,103,100,C.red)+path('M245 184Q297 142 343 183L343 220Q297 178 245 220Z',C.si)+guide('M389 180Q427 153 485 180')+arrow(220,194,237,194)+arrow(347,194,380,194)+text(164,198,'T(x,y,z)')+tx(303,260,'變形','Deformation')+tx(433,230,'耦合','Coupling');
 case 'feedback':return rect(128,121,131,51,C.blue)+rect(354,121,119,51,C.green)+rect(245,239,133,37,C.gold)+arrow(262,146,350,146)+path('M411 174V257H380M242 257H191V178','none',C.ink,2)+tx(193,153,'相移器','Phase actuator')+tx(413,153,'監測器','Monitor')+tx(309,263,'控制器','Controller');
 case 'reroute':return circle(135,185,15,C.blue)+circle(466,185,15,C.blue)+path('M151 182L254 123H361L451 182','none',C.red,4)+path('M151 188L254 245H361L451 188','none',C.green,5)+path('M289 109l27 27m-27 0 27-27','none',C.red,5)+arrow(270,245,339,245,C.green)+tx(300,287,'備援容量與切換時間皆需驗證','Verify spare capacity and switching time');
 case 'stressphase':return guide('M125 189Q300 159 479 189')+many(4,i=>arrow(192+i*72,105,192+i*72,153,C.red))+path('M136 229Q301 206 469 229','none',C.si,13)+tx(300,279,'應力張量 → Δn_eff → Δφ','Stress tensor → Δn_eff → Δφ');
 case 'pdk':return many(4,i=>rect(131+i%2*192,108+Math.floor(i/2)*95,154,66,i===0?C.blue:i===1?C.gold:i===2?C.green:C.light))+tx(208,145,'模型','Models')+tx(400,145,'版圖','Layout')+tx(208,240,'規則','Rules')+tx(400,240,'驗證','Validation')+arrow(288,141,319,141)+arrow(397,178,397,197)+arrow(320,236,291,236);
 case 'cpo':return rect(108,92,385,202,C.green)+die(228,155,151,85)+many(4,i=>rect(142+i%2*276,121+Math.floor(i/2)*111,49,41,C.blue)+fiber(i%2?467:75,135+Math.floor(i/2)*111,65))+many(2,i=>arrow(197,143+i*111,224,174+i*34)+arrow(383,175+i*34,413,143+i*111))+tx(300,131,'交換晶片','Switch die');
 case 'opticalio':return layer(244,26,C.green)+die(138,147,159,81)+die(344,164,109,64)+many(3,i=>line(299,180+i*13,342,180+i*13,C.gold,3))+fiber(454,182,75)+tx(219,128,'運算','Compute')+tx(396,145,'光學 I/O','Optical I/O');
 case 'codesign':return rect(108,139,113,58,C.gold)+rect(345,139,145,58,C.blue)+rect(244,237,125,39,C.red)+arrow(226,154,339,154)+arrow(339,179,226,179)+path('M166 201V256H238M371 256H418V201','none',C.ink,2)+tx(164,174,'驅動','Driver')+tx(418,173,'光子元件','Photonics')+tx(305,264,'熱模型','Thermal');
 case 'interlock':return rect(112,128,102,57,C.red)+rect(317,123,156,116,C.light)+line(215,156,304,156,C.red,5)+rect(259,137,14,40,C.ink)+path('M267 135V101H390V123','none',C.green,3)+tx(164,162,'發光源','Emitter')+tx(395,183,'封閉光路','Enclosure')+tx(300,278,'開啟保護罩 → 禁止發光','Open enclosure → emission inhibited');
 case 'soic':return bond(true)+many(5,i=>via(159+i*59,123,24))+tx(300,284,'細間距堆疊概念；非產品剖面','Fine-pitch stacking concept; not a product cross section');
 case 'foveros':return layer(247,22,C.green)+die(179,193,242,29)+die(203,126,194,37)+bumps(180,7)+many(4,i=>via(206+i*57,222,24))+tx(300,105,'主動基底與上層晶粒的概念','Concept of active base and upper dies');
 case 'isipp':return guide('M110 193H171Q204 193 222 157H291Q315 193 333 193H488')+guide('M171 193Q204 193 222 229H291Q315 193 333 193')+ring(373,153,32)+rect(438,178,30,30,C.violet)+rect(221,133,72,10,C.gold)+tx(300,283,'PDK 元件、測試與封裝介面','PDK components, test and package interface');
 default:return '';
 }
}
export function renderPackagingVisual(courseId,{zh=true,mode='full'}={}){
 const s=PACKAGING_SUBJECTS[courseId];if(!s)return '';
 const title=zh?s.title:s.titleEn,focus=zh?s.focus:s.focusEn,desc=focus+(zh?'。原創原理示意；非比例、非實物剖面或施工圖。':' — Original principle diagram; not to scale, an actual product section or a fabrication drawing.');
 return `<svg xmlns="http://www.w3.org/2000/svg" class="packaging-subject-visual" viewBox="0 0 600 370" role="img" aria-label="${esc(title+' — '+desc)}" data-course="${esc(courseId)}" data-family="${s.family}" data-original="true"><title>${esc(title)}</title><desc>${esc(desc)}</desc><rect width="600" height="370" rx="20" fill="${C.pale}"/>${text(23,29,courseId.toUpperCase(),11,C.blue,'start')}${text(577,29,zh?'原創原理圖 · 非比例':'ORIGINAL CONCEPT · NOT TO SCALE',10,C.blue,'end')}${text(300,58,title,zh?17:12)}<g data-geometry="${s.family}">${packagingGeometry(s.family,{zh,labels:mode!=='icon'})}</g>${mode==='icon'?'':text(300,335,focus,zh?13:10.5)}</svg>`;
}
export function packagingVisualFamily(courseId){return PACKAGING_SUBJECTS[courseId]?.family??null;}
