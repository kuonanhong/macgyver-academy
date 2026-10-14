"""Primary-source and contextual metadata; no source images are republished here."""
SOURCES={}
def S(key,zh,en,publisher,url,scope,scope_en):
    SOURCES[key]=dict(id='v10b-'+key,title=zh,titleEn=en,publisher=publisher,url=url,scope=scope,scopeEn=scope_en,accessedAt='2026-10-14',sourceType='primary',category='electronics',imageReuse='link-only; no image republication permission implied')
S('wind15','IEA 15 MW 海上參考風機','IEA 15-MW offshore reference turbine','NREL / DTU','https://research-hub.nlr.gov/en/publications/iea-wind-tcp-task-37-definition-of-the-iea-15-megawatt-offshore-r/','公開參考模型與研究假設，非商用製造圖。','Public reference model and research assumptions, not commercial fabrication drawings.')
S('wind5','5 MW 海上參考風機定義','Definition of a 5-MW offshore reference turbine','NREL','https://research-hub.nlr.gov/en/publications/definition-of-a-5-mw-reference-wind-turbine-for-offshore-system-d/','公開氣動、機械與控制模型的邊界。','Scope of an open aerodynamic, mechanical and control model.')
S('windcollection','海上風場集電與輸電研究','Electrical collection and transmission for offshore wind','NREL','https://research-hub.nlr.gov/en/publications/electrical-collection-and-transmission-systems-for-offshore-wind--2/','集電拓樸、電纜和輸送成本模型的研究背景。','Research context for collection topology, cables and transmission models.')
S('windconverter','公用級風機變流器','Utility-scale wind-turbine converters','ABB','https://new.abb.com/power-converters-inverters/wind-turbines/utility-scale','雙饋與全功率風機變流器的產品角色；非通用額定值。','Product roles for doubly-fed/full-power converters, not universal ratings.')
S('pumped','抽蓄水力儲能概述','Pumped-storage hydropower overview','US Department of Energy','https://www.energy.gov/cmei/water/pumped-storage-hydropower','抽蓄的水能、儲能及電網服務背景。','Hydraulic, storage and grid-service context for pumped hydro.')
S('pumpedchapter','儲能手冊第9章：抽蓄','Energy Storage Handbook Chapter 9: pumped hydro','DOE / Sandia','https://www.sandia.gov/app/uploads/sites/163/2024/08/ESHB_Ch9_PHS_Bera.pdf','固定速與可變速抽蓄機組；學習模型不能當現場啟停程序。','Fixed/variable-speed pumped storage; educational models are not operating procedures.')
S('storage','美國能源部儲能手冊','US DOE Energy Storage Handbook','DOE / Sandia','https://www.sandia.gov/ess/publications/eshb','電網儲能技术、轉換、管理及驗證的章節入口。','Chapter portal for grid storage, conversion, management and validation.')
S('storageperformance','儲能性能測試','Energy-storage performance testing','DOE / Sandia','https://www.sandia.gov/app/uploads/sites/163/2021/09/ESHB_Ch16_Testing_Rosewater.pdf','量測邊界、性能定義與試驗證據的閱讀。','Reading on metering boundaries, performance definitions and test evidence.')
S('flow','氧化還原液流電池','Redox flow batteries','DOE / Sandia','https://www.sandia.gov/app/uploads/sites/163/2022/03/ESHB_Ch6_RedoxFlow_Small.pdf','電解液、堆疊與系統介面；不複製化學配方。','Electrolytes, stacks and system interfaces without reproducing chemical recipes.')
S('flywheel','飛輪儲能','Flywheel energy storage','DOE / Sandia','https://www.sandia.gov/app/uploads/sites/163/2022/03/ESHB_Ch07_Flywheels_Bender.pdf','旋轉能量、電機與儲能應用的原理參考。','Principles of rotational energy, machinery and storage applications.')
S('hydrogen','氫能儲存','Hydrogen energy storage','DOE / Sandia','https://www.sandia.gov/app/uploads/sites/163/2022/03/ESHB_Ch11_Hydrogen_Headley.pdf','能源鏈與電力介面背景，不作氫氣操作指南。','Energy-chain and electrical-interface context, not hydrogen handling guidance.')
S('supercap','超級電容應用指南','Supercapacitor application guidelines','Eaton','https://www.eaton.com/content/dam/eaton/products/electronic-components/resources/technical/eaton-supercapacitor-application-guidelines.pdf','電容量、ESR、均壓與壽命的元件條件。','Component conditions for capacitance, ESR, balancing and life.')
S('bms','BQ76952 監測與保護文件','BQ76952 monitoring and protection documentation','Texas Instruments','https://www.ti.com/product/BQ76952','單體監測、保護和均衡的文件入口；不可照抄門檻。','Documentation portal for cell monitoring, protection and balancing; thresholds are not transferable.')
S('ups','UPS 基礎手冊','UPS fundamentals handbook','Eaton','https://www.eaton.com/content/dam/eaton/products/backup-power-ups-surge-it-power-distribution/backup-power-ups/eaton-ups-fundamentals-handbook-en-us-2025.pdf','UPS 拓樸、負載和電力路徑的系統背景。','System context for UPS topology, loads and power paths.')
S('upstopology','選擇 UPS 拓樸','Choosing a UPS topology','Eaton','https://www.eaton.com/us/en-us/products/backup-power-ups-surge-it-power-distribution/backup-power-ups/choosing-the-optimal-ups-topology-.html','不同 UPS 正常路徑與轉移行為的比較。','Comparison of normal paths and transfers in UPS topologies.')
S('datacenter','備援與緊急配電設計','Emergency and standby power distribution','Schneider Electric','https://productinfo.se.com/0100db2301_elecdistfunddesignguide/0100db2301-electrical-distribution-fundamentals-design-guide/English/0100DB2301%20Electrical%20Distribution%20Fundamentals%20Design%20Guide%20%28bookmap%29_DD00648155.xml/%24/EmergencyAndStandbyPowerSystems-A64217F8','N、N+1、2N 與備援配電閱讀，非特定場址操作規範。','Reading on N, N+1, 2N and backup distribution, not site procedures.')
S('datacenterdc','資料中心 DC 架構設計考量','DC-architecture considerations for data centers','Schneider Electric','https://www.se.com/ww/en/download/document/SPD_WP47_EN/','DC 配電的轉換、故障、接地與旁路差異。','Differences in conversion, faults, grounding and bypass for DC distribution.')
S('fuelcell','燃料電池控制器與 DC 介面','Fuel-cell control and DC interfaces','Texas Instruments','https://www.ti.com/solution/fuel-cell-control-unit-fccu','單向 DC/DC、監測及控制角色；不代表完整燃料系統。','Roles of unidirectional DC/DC, monitoring and control, not a complete fuel system.')
S('electrolysis','電解槽電源產品介面','Electrolyzer power-supply interfaces','ABB','https://www.abb.com/global/en/areas/renewable-power/electrolyzer-power-supplies','電解用整流器與電網介面產品背景。','Product context for electrolyzer rectifiers and grid interfaces.')
S('electrolysistop','電解槽電源拓樸比較','Electrolyzer power-supply topology comparison','ABB','https://www.abb.com/global/en/company/innovation/news/hydrogen-production','多脈波、主動整流和兩級轉換的取捨。','Tradeoffs in multipulse, active-rectifier and two-stage conversion.')
S('shore','岸船電力變頻器','Shore-to-ship power converters','ABB','https://new.abb.com/power-converters-inverters/grid-interconnections/shore-to-ship-converters','岸網和船網間的頻率轉換與供電介面。','Frequency conversion and power interfaces between shore and ship grids.')
S('induction','高壓感應馬達','High-voltage induction motors','ABB','https://www.abb.com/global/en/areas/motion/motors-generators/mv-hv-motors/induction-motors','工業感應馬達設計與驗證的產品背景。','Product context for industrial induction-machine design and validation.')
S('motorassembly','電動馬達組裝自動化','Electric-motor assembly automation','ABB','https://www.abb.com/global/en/areas/robotics/industries/automotive/assembly/e-motor','轉子、定子組装與品質檢測的設備角色。','Equipment roles in rotor/stator assembly and quality inspection.')
S('motorcontrol','馬達控制技術資源','Motor-control technology resources','Texas Instruments','https://www.ti.com/technologies/motor-control.html','FOC、感測、估測和即時控制的技術入口。','Technical portal for FOC, feedback, estimation and real-time control.')
S('observers','AM263x 馬達控制觀測器','AM263x motor-control observers','Texas Instruments','https://software-dl.ti.com/processor-industrial-sw/esd/motor_control_sdk/am263x/latest/docs/api_guide_am263x/OBSERVERS.html','編碼器、Hall 和 eSMO 觀測器的官方軟體文件。','Official software documentation for encoder, Hall and eSMO observers.')
S('srm','開關磁阻馬達控制','Switched-reluctance motor control','Microchip Technology','https://www.microchip.com/en-us/solutions/technologies/motor-control-and-drive/motor-types/switched-reluctance-motors','SR 機電結構與相電流控制的原理入口。','Principles portal for SR geometry and phase-current control.')
S('bldc','BLDC 與馬達控制資源','BLDC and motor-control resources','Microchip Technology','https://www.microchip.com/en-us/solutions/technologies/motor-control-and-drive','BLDC、感應機及無感測控制應用文件入口。','Application-document portal for BLDC, induction and sensorless control.')
S('linear','直驅線性馬達選型指南','Direct-drive linear-motor selection guide','Kollmorgen','https://www.kollmorgen.com/en-us/products/catalogs/kollmorgen-direct-drive-linear-motor-selection-guide','力、熱條件、行程及選型背景；不照搬某系列溫度限值。','Force, thermal, travel and selection context without universalizing one series limit.')
S('encoder','光學編碼器原理','How optical encoders work','Renishaw','https://www.renishaw.com/en/how-optical-encoders-work--36979','碼尺、內插、位置資料與錯誤偵測原理。','Scale, interpolation, position-data and error-detection principles.')
S('encoderfaq','編碼器解析度與誤差','Encoder resolution and errors','Renishaw','https://www.renishaw.com/en/optical-encoders-frequently-asked-questions--34674','解析度、重複性、抖動與週期誤差的區分。','Distinguishing resolution, repeatability, jitter and cyclic error.')
S('magnetic','磁浮軸承與高速電機系統','Magnetic bearings and high-speed motor systems','SKF','https://cdn.skfmediahub.skf.com/api/public/0901d196803ace45/pdf_preview_medium/0901d196803ace45_pdf_preview_medium.pdf','磁浮位置回授、電機與軸承控制的系統角色。','System roles of magnetic position feedback, motors and bearing control.')
S('magneticmotor','高速永磁電機與磁浮系統','High-speed permanent-magnet systems','SKF','https://cdn.skfmediahub.skf.com/api/public/0901d1968027e056/pdf_preview_medium/0901d1968027e056_pdf_preview_medium.pdf','高速機、磁浮與變頻驅動的整合背景。','Integration context for high-speed machines, magnetic bearings and drives.')
S('traction','牽引逆變器與隔離驅動','Traction inverters and isolated driving','Infineon Technologies','https://www.infineon.com/technology-news/2026/infatv202606-106','SiC 牽引功率級、控制及隔離驅動器的廠商角色。','Vendor roles in SiC traction power stages, controls and isolated drivers.')
S('sicdriver','SiC MOSFET 門極驅動','SiC MOSFET gate drivers','Infineon Technologies','https://www.infineon.com/products/power/gate-driver-ics/eicedriver-for-sic-mosfets','Miller 抑制、共模暫態及驅動器產品條件。','Miller suppression, common-mode transients and driver-specific conditions.')
S('gate','具主動保護的隔離門極驅動器','Isolated gate driver with active protection','Texas Instruments','https://www.ti.com/lit/ds/symlink/ucc21759-q1.pdf','Miller 夾位、CMTI、保護與驅動時序；限制屬特定器件。','Miller clamping, CMTI, protection and timing; limits are device-specific.')
S('isolatedgate','隔離閘極驅動器技術','Isolated gate-driver technology','Infineon Technologies','https://www.infineon.com/products/power/gate-driver-ics/galvanic-isolated-gate-driver','隔離驅動、CMTI 和故障保護功能的產品背景。','Product context for isolation, CMTI and fault-protection features.')
S('gan','GaN 功率器件技術文件','GaN power-device technical documentation','Infineon Technologies','https://www.infineon.com/products/power/gallium-nitride/gallium-nitride-transistor','GaN 門極、寄生與量測文件入口；部分下載可能需廠商登入。','GaN gate, parasitic and measurement document portal; some downloads may require vendor login.')
S('pfc','圖騰柱 PFC 參考設計','Totem-pole PFC reference design','Texas Instruments','https://www.ti.com/tool/TIDM-02008','PFC 控制、過零、相位裁切與公開設計證據。','PFC control, zero crossing, phase shedding and public design evidence.')
S('llc','LLC 控制器文件','LLC controller documentation','Texas Instruments','https://www.ti.com/product/UCC256404','LLC、突發模式與控制器文件入口。','Portal for LLC, burst operation and controller documents.')
S('llcfaq','LLC 控制器常見工程問題','LLC-controller engineering questions','Texas Instruments','https://www.ti.com/tw/lit/pdf/sluaal2','諧振槽、控制與驗證限制的補充閱讀。','Supplementary reading on resonant tanks, control and validation limits.')
S('psfbfund','移相全橋原理及拓樸比較','PSFB principles and topology comparison','Texas Instruments','https://www.ti.com/document-viewer/lit/html/SLUP414/GUID-612666D6-38F9-48F4-B001-0BB34FAB6694','PSFB、LLC 與 DAB 軟切換和控制的差異。','Differences in PSFB, LLC and DAB soft switching/control.')
S('psfb','數位峰值電流模式移相全橋','Digital peak-current-mode PSFB','Texas Instruments','https://www.ti.com/tool/TIDM-02000','公開 PSFB 設計、時序與測試資料入口。','Portal for public PSFB design, timing and test data.')
S('psfbsdk','PSFB 數位控制 SDK 文件','PSFB digital-control SDK documentation','Texas Instruments','https://software-dl.ti.com/C2000/c2000_apps_public_sw/c2000ware_sdk/digitalpowersdk/5_03_00_00/html_guide/TIDM-02000.html','特定參考設計的控制實作與條件，不是通用性能。','Control implementation and conditions of a specific design, not universal performance.')
S('dab','雙主動橋雙向轉換參考設計','Bidirectional dual-active-bridge reference design','Texas Instruments','https://www.ti.com/tool/TIDA-010054','DAB 相移、電流、軟切換與隔離的公開設計背景。','Public design context for phase shift, current, soft switching and isolation.')
S('dabsdk','C2000 數位電源 SDK','C2000 digital-power SDK','Texas Instruments','https://software-dl.ti.com/C2000/docs/software_guide/dpsdk.html','數位電源參考設計索引和控制軟體文件。','Digital-power reference-design index and control-software documentation.')
S('current','電流感測工程指南','An engineer’s guide to current sensing','Texas Instruments','https://www.ti.com/lit/pdf/SLYY154','分流、共模、誤差、取樣和保護的原理參考。','Principles of shunts, common mode, errors, sampling and protection.')
S('currentproduct','INA240 PWM 電流感測器','INA240 PWM current sensing','Texas Instruments','https://www.ti.com/product/INA240','量測放大器的偏移、增益和 PWM 恢復條件；非隔離器。','Offset, gain and PWM recovery conditions for a sensing amplifier; not an isolator.')
S('emectidal','EMEC 併網潮流測試場','EMEC grid-connected tidal test site','European Marine Energy Centre','https://www.emec.org.uk/facilities/tidal-test-site/','潮流測試、海纜及岸端電力調節的場址背景。','Site context for tidal testing, subsea cables and onshore conditioning.')
S('emechistory','EMEC 歷史','EMEC history','European Marine Energy Centre','https://www.emec.org.uk/about-us/emec-history/','2003 設立、2006 潮流場開放及後續併網的歷史。','History of 2003 establishment, 2006 tidal-site opening and later grid connection.')
S('dtuplace','DTU Risø 園區與歷史','DTU Risø campus and history','Technical University of Denmark','https://www.dtu.dk/english/about/campuses/dtu-risoe-campus','園區地址、1958 啟用及能源研究背景。','Campus address, 1958 inauguration and energy-research context.')
S('dtutest','DTU 風機測試設施','DTU wind-turbine test facilities','Technical University of Denmark','https://wind.dtu.dk/research/research-divisions/wind-turbine-design/test-centres','Risø、Høvsøre 和 Østerild 的測試研究角色。','Test-research roles of Risø, Høvsøre and Østerild.')
S('pnnlplace','PNNL 園區地址','PNNL campus addresses','Pacific Northwest National Laboratory','https://www.pnnl.gov/contact','Richland 主要園區和儲能設施公開地址。','Public Richland campus and storage-facility addresses.')
S('pnnlhistory','Grid Storage Launchpad 2024 啟用','Grid Storage Launchpad opens in 2024','Pacific Northwest National Laboratory','https://www.pnnl.gov/news-media/grid-storage-launchpad-pnnl-opens-new-era-energy-storage','PNNL 1965 成立及儲能整合研究設施背景。','PNNL’s 1965 founding and integrated energy-storage research context.')
S('tiplace','TI 達拉斯總部地址','TI Dallas headquarters address','Texas Instruments','https://education.ti.com/en/customer-support/knowledge-base/all-other-products/general-information/10626','官方總部地址，只作電子控制產業代表點。','Official headquarters address, used only as an electronics-industry reference.')
S('tihistory','TI 技術與公司歷史','TI technology and company history','Texas Instruments','https://www.ti.com/about-ti.html','類比、嵌入式與 1958 積體電路歷史背景。','Context for analog, embedded processing and the 1958 integrated circuit.')
S('tifaq','TI 企業沿革問答','TI corporate-history FAQ','Texas Instruments','https://ti.gcs-web.com/resources/frequently-asked-questions','1930 GSI 起源與 1951 更名的官方記錄。','Official record of GSI origins in 1930 and TI renaming in 1951.')
S('voith','可變速抽蓄系統','Variable-speed pumped-storage systems','Voith','https://www.voith.com/corp-en/industry-solutions/hydropower/pumped-storage-plants.html','抽蓄機組與控制的供應商角色。','Supplier roles in pumped-storage machinery and control.')
S('sumitomo','釩液流電池系統','Vanadium redox-flow battery systems','Sumitomo Electric','https://sumitomoelectric.com/products/flow-batteries','液流電池、電解液與系統供應的業務背景。','Business context for flow batteries, electrolytes and systems.')
S('orbital','Orbital 潮流機技術','Orbital tidal-turbine technology','Orbital Marine Power','https://www.orbitalmarine.com/technology/','浮式潮流機及 Orkney 公開示範案例。','Floating tidal machines and a public Orkney demonstrator.')
ALIASES={'bmsbalance':'bms','shoreguide':'shore','foc':'motorcontrol','ganpfc':'pfc','pfcguide':'pfc'}
def source(key): return SOURCES[ALIASES.get(key,key)]

def V(name,key,role,role_en,ticker=None,exchange=None):
    s=source(key)
    v=dict(name=name,url=s['url'],productUrl=s['url'],role=role,roleEn=role_en,sourceIds=[s['id']],relationship='educational-example-not-endorsement',relationshipEn='Educational example, not an endorsement')
    if ticker: v.update(ticker=ticker,exchange=exchange)
    return v
VENDORS={
'a236':[V('ABB','windconverter','風機全功率與雙饋變流器','Full-power and doubly-fed wind converters','ABBN','SIX')],
'a237':[V('ABB','windconverter','風機電力變換與電網介面','Wind power conversion and grid interfaces','ABBN','SIX')],
'a238':[V('ABB','windconverter','發電端變流與集電介面需求','Turbine conversion and collector-interface requirements','ABBN','SIX')],
'a239':[V('Voith','voith','抽蓄電機、水輪機與控制整合','Pumped-storage machines, turbines and control integration')],
'a240':[V('Orbital Marine Power','orbital','浮式潮流發電機組與電網示範','Floating tidal machines and grid demonstration')],
'a241':[V('Texas Instruments','bms','電池監測與保護晶片','Battery-monitoring and protection ICs','TXN','NASDAQ')],
'a242':[V('Texas Instruments','bms','BMS 監測、均衡與保護','BMS monitoring, balancing and protection','TXN','NASDAQ')],
'a243':[V('Sumitomo Electric','sumitomo','釩液流電池堆疊與儲能系統','Vanadium flow-battery stacks and storage systems','5802','TSE')],
'a244':[V('Eaton','supercap','超級電容元件與應用資料','Supercapacitor components and application data','ETN','NYSE')],
'a245':[V('SKF','magnetic','高速電機及磁浮軸承系統','High-speed motors and magnetic-bearing systems','SKF-B','NASDAQ Stockholm')],
'a246':[V('Eaton','ups','UPS 和備援供電設備','UPS and backup-power equipment','ETN','NYSE')],
'a247':[V('Schneider Electric','datacenterdc','資料中心配電與電力架構','Data-center distribution and power architectures','SU','Euronext Paris')],
'a248':[V('Texas Instruments','fuelcell','燃料電池 DC 介面與控制半導體','Fuel-cell DC-interface and control semiconductors','TXN','NASDAQ')],
'a249':[V('ABB','electrolysis','電解槽整流及電力品質介面','Electrolyzer rectification and power-quality interfaces','ABBN','SIX')],
'a250':[V('ABB','shore','岸船頻率轉換與供電設備','Shore-to-ship frequency conversion and supply','ABBN','SIX')],
'a251':[V('ABB','induction','工業感應馬達','Industrial induction motors','ABBN','SIX')],
'a252':[V('ABB','motorassembly','定子、磁轉子與電機組裝自動化','Stator, magnetic-rotor and motor-assembly automation','ABBN','SIX')],
'a253':[V('Microchip Technology','srm','SR 馬達控制 MCU 與驅動方案','SR motor-control MCUs and drive solutions','MCHP','NASDAQ')],
'a254':[V('Kollmorgen','linear','直驅線性馬達與選型','Direct-drive linear motors and sizing'),V('Renishaw','encoder','線性位置編碼器','Linear position encoders','RSW','LSE')],
'a255':[V('Texas Instruments','motorcontrol','BLDC 控制與功率級晶片','BLDC control and power-stage ICs','TXN','NASDAQ')],
'a256':[V('Renishaw','encoder','光學編碼器與位置量測','Optical encoders and position measurement','RSW','LSE')],
'a257':[V('Texas Instruments','motorcontrol','即時 FOC 控制處理器','Real-time FOC processors','TXN','NASDAQ')],
'a258':[V('Texas Instruments','observers','無感測觀測器軟體與控制器','Sensorless-observer software and controllers','TXN','NASDAQ')],
'a259':[V('Infineon Technologies','traction','牽引與回生逆變功率半導體','Traction and regenerative inverter semiconductors','IFX','XETRA')],
'a260':[V('SKF','magnetic','磁浮軸承、位置控制與高速電機','Magnetic bearings, position control and high-speed motors','SKF-B','NASDAQ Stockholm')],
'a261':[V('Infineon Technologies','traction','SiC 牽引模組與驅動器','SiC traction modules and drivers','IFX','XETRA')],
'a262':[V('Infineon Technologies','gan','GaN 功率電晶體','GaN power transistors','IFX','XETRA')],
'a263':[V('Texas Instruments','llc','LLC 諧振控制器','LLC resonant controllers','TXN','NASDAQ')],
'a264':[V('Texas Instruments','psfb','移相全橋數位控制參考設計','Digital PSFB reference designs','TXN','NASDAQ')],
'a265':[V('Texas Instruments','dab','雙向 DAB 控制及閘極驅動方案','Bidirectional DAB control and gate-drive solutions','TXN','NASDAQ')],
'a266':[V('Texas Instruments','pfc','PFC 控制與 GaN 參考設計','PFC control and GaN reference designs','TXN','NASDAQ')],
'a267':[V('Texas Instruments','gate','隔離閘極驅動與故障保護','Isolated gate driving and fault protection','TXN','NASDAQ')],
'a268':[V('Texas Instruments','currentproduct','分流電流感測放大器','Shunt current-sense amplifiers','TXN','NASDAQ')]
}
S('abbhistory','ABB 企業歷史','ABB corporate history','ABB','https://www.abb.com/global/en/company/about/history','1988 合併成立與蘇黎世總部的官方沿革。','Official history of the 1988 merger and Zurich headquarters.')
S('abbheritage','BBC 電機工程沿革','BBC electrical-engineering heritage','ABB','https://www.abb.com/global/en/company/about/history/heritage-brands/brown-boveri-cie-bbc','1891 Baden 起源與 1988 合併的官方背景。','Official context for Baden origins in 1891 and the 1988 merger.')
