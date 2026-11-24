/* Public bilingual process atlas. Production status is per verified process film. */
window.MACGYVER_PACKAGING_PROCESS_ROADMAP = {
  "schemaVersion": 1,
  "version": "34.0.1",
  "title": {
    "zh-TW": "先進半導體封裝：120項工序與工程活動路線圖",
    "en": "Advanced semiconductor packaging: 120 process and engineering activities"
  },
  "updatedOn": "2026-11-24",
  "languages": [
    "zh-TW",
    "en"
  ],
  "catalogueCount": 120,
  "activityCounts": {
    "design": 22,
    "inspection_test": 30,
    "manufacturing": 68
  },
  "durationPerPlannedFilmSeconds": 300,
  "plannedTotalDurationSeconds": 36000,
  "productionStatus": {
    "index": "complete",
    "bilingualSummaries": "complete",
    "fullNarrationScripts": "in_progress",
    "fiveMinuteProcessFilmsProduced": 4,
    "fiveMinuteProcessFilmsPlanned": 120,
    "existingOverviewFilms": 6,
    "existingOverviewsAreProcessFilms": false,
    "fullNarrationScriptsWritten": 4,
    "fifteenMinuteProcessFilmsLocallyVerified": 4
  },
  "scope": {
    "zh-TW": "這是120項不重複的教學工序與工程活動目錄，含設計、製造操作和檢驗測試；不是聲稱某條產線恰好有120個製造站。已公開C01、C02、C03、C04共4部五分鐘五語影片，其餘116項尚未連結公開完成片。十五分鐘長片的本機驗證與公開方式依各項標示；六部架構總覽另列。",
    "en": "This catalogue contains 120 distinct teaching processes and engineering activities, not a claim that one factory route has exactly 120 stations. C01, C02, C03, C04 provide 4 published five-minute films in five languages; the remaining 116 entries do not yet link to completed published films. Each item identifies its fifteen-minute lesson verification and distribution. The six architecture overviews are separate."
  },
  "routing": {
    "commonBranch": "common",
    "architectureChoiceBranches": [
      "interposer",
      "fanout",
      "hybrid",
      "bridge-chiplet"
    ],
    "finishBranch": "finish-test",
    "alternativesAreNotMandatorySerialSteps": true,
    "qualificationTestsUseSeparateCohorts": true,
    "prerequisiteMeaning": {
      "zh-TW": "前置ID是教學依賴與路線關係，不是可直接執行的批次製造旅程卡。跨分支anyOf表示擇一完成；可組合的3D與2.5D方案需另做產品流程。",
      "en": "Prerequisite IDs express learning and route relationships, not an executable lot traveler. Cross-branch anyOf means one selected route. Combined 3D/2.5D products require a separately qualified flow."
    },
    "recommendedLearningPaths": [
      {
        "architectureBranch": "interposer",
        "segments": [
          "C01–C20",
          "I01–I20",
          "V01–V20"
        ],
        "catalogueActivities": 60,
        "qualificationAndOptionalStepsRemainConditional": true
      },
      {
        "architectureBranch": "fanout",
        "segments": [
          "C01–C20",
          "F01–F20",
          "V01–V20"
        ],
        "catalogueActivities": 60,
        "qualificationAndOptionalStepsRemainConditional": true
      },
      {
        "architectureBranch": "hybrid",
        "segments": [
          "C01–C20",
          "H01–H20",
          "V01–V20"
        ],
        "catalogueActivities": 60,
        "qualificationAndOptionalStepsRemainConditional": true
      },
      {
        "architectureBranch": "bridge-chiplet",
        "segments": [
          "C01–C20",
          "B01–B20",
          "V01–V20"
        ],
        "catalogueActivities": 60,
        "qualificationAndOptionalStepsRemainConditional": true
      }
    ]
  },
  "activityTypes": {
    "design": {
      "zh-TW": "設計活動",
      "en": "Design activity"
    },
    "manufacturing": {
      "zh-TW": "製造操作",
      "en": "Manufacturing operation"
    },
    "inspection_test": {
      "zh-TW": "檢驗／測試",
      "en": "Inspection / test"
    }
  },
  "evidencePolicy": {
    "primarySourcesOnly": true,
    "directQuotations": false,
    "sourceScope": {
      "zh-TW": "來源支持公開技術概念、能力或量測方法；各課的前置、輸入輸出、失效討論與教學排序是綜合設計，不宣稱逐字轉錄任何廠商SOP。",
      "en": "Sources support public concepts, capabilities or measurement methods. Prerequisites, inputs/outputs, failure discussions and teaching order are synthesized educational design, not a verbatim supplier SOP."
    },
    "parameters": {
      "zh-TW": "不指定通用溫度、壓力、化學配方、膜厚、允收界線或良率；需依產品與供應商核准條件另行驗證。",
      "en": "No universal temperatures, pressures, chemical recipes, thicknesses, acceptance limits or yields are specified. Product- and supplier-qualified conditions are required."
    }
  },
  "branches": [
    {
      "id": "common",
      "prefix": "C",
      "title": {
        "zh-TW": "共同設計與晶圓來料",
        "en": "Shared design and incoming wafers"
      },
      "role": "common",
      "itemCount": 20,
      "overviewTourId": "interposer",
      "notes": {
        "zh-TW": "先把需求、互連、材料、測試與追溯定義清楚，再放行選定架構。",
        "en": "Define requirements, interconnects, materials, test and traceability before releasing a selected architecture."
      },
      "itemIds": [
        "C01",
        "C02",
        "C03",
        "C04",
        "C05",
        "C06",
        "C07",
        "C08",
        "C09",
        "C10",
        "C11",
        "C12",
        "C13",
        "C14",
        "C15",
        "C16",
        "C17",
        "C18",
        "C19",
        "C20"
      ]
    },
    {
      "id": "interposer",
      "prefix": "I",
      "title": {
        "zh-TW": "2.5D 矽中介層與 HBM",
        "en": "2.5D silicon interposer and HBM"
      },
      "role": "alternative",
      "itemCount": 20,
      "overviewTourId": "interposer",
      "notes": {
        "zh-TW": "本例由已含盲孔TSV的中介層進入後段加工；HBM以已測堆疊進料，不假稱涵蓋DRAM製造。",
        "en": "This route starts with preformed blind TSVs and tested HBM stacks. It does not teach DRAM fabrication or every CoWoS variant."
      },
      "itemIds": [
        "I01",
        "I02",
        "I03",
        "I04",
        "I05",
        "I06",
        "I07",
        "I08",
        "I09",
        "I10",
        "I11",
        "I12",
        "I13",
        "I14",
        "I15",
        "I16",
        "I17",
        "I18",
        "I19",
        "I20"
      ]
    },
    {
      "id": "fanout",
      "prefix": "F",
      "title": {
        "zh-TW": "RDL-first 扇出封裝",
        "en": "RDL-first fan-out packaging"
      },
      "role": "alternative",
      "itemCount": 20,
      "overviewTourId": "fanout",
      "notes": {
        "zh-TW": "此路徑先製作RDL再接合晶粒；chip-first與面板化是不同分支，不與本例混串。",
        "en": "RDL is built before die attachment. Chip-first and panel-level variants are different routes, not extra mandatory steps."
      },
      "itemIds": [
        "F01",
        "F02",
        "F03",
        "F04",
        "F05",
        "F06",
        "F07",
        "F08",
        "F09",
        "F10",
        "F11",
        "F12",
        "F13",
        "F14",
        "F15",
        "F16",
        "F17",
        "F18",
        "F19",
        "F20"
      ]
    },
    {
      "id": "hybrid",
      "prefix": "H",
      "title": {
        "zh-TW": "晶粒對晶圓混合鍵合",
        "en": "Die-to-wafer hybrid bonding"
      },
      "role": "alternative",
      "itemCount": 20,
      "overviewTourId": "hybrid",
      "notes": {
        "zh-TW": "示範直接D2W的表面、銅接點與介電鍵合；不是所有W2W或集體轉印流程。",
        "en": "A direct D2W teaching route covering copper/dielectric surfaces. W2W and collective transfer use different sequences."
      },
      "itemIds": [
        "H01",
        "H02",
        "H03",
        "H04",
        "H05",
        "H06",
        "H07",
        "H08",
        "H09",
        "H10",
        "H11",
        "H12",
        "H13",
        "H14",
        "H15",
        "H16",
        "H17",
        "H18",
        "H19",
        "H20"
      ]
    },
    {
      "id": "bridge-chiplet",
      "prefix": "B",
      "title": {
        "zh-TW": "局部矽橋與小晶片整合",
        "en": "Local bridges and chiplet integration"
      },
      "role": "alternative",
      "itemCount": 20,
      "overviewTourId": "bridge",
      "notes": {
        "zh-TW": "局部矽橋嵌入有機基板；UCIe屬介面與驗證活動，不是製造站。EMIB-T等變體需另設路線。",
        "en": "Local silicon bridges sit in organic substrates. UCIe is an interface/test topic, not a fabrication station. Variants such as EMIB-T require separate routes."
      },
      "itemIds": [
        "B01",
        "B02",
        "B03",
        "B04",
        "B05",
        "B06",
        "B07",
        "B08",
        "B09",
        "B10",
        "B11",
        "B12",
        "B13",
        "B14",
        "B15",
        "B16",
        "B17",
        "B18",
        "B19",
        "B20"
      ]
    },
    {
      "id": "finish-test",
      "prefix": "V",
      "title": {
        "zh-TW": "散熱組裝、測試與可靠度",
        "en": "Thermal assembly, test and reliability"
      },
      "role": "shared-with-conditions",
      "itemCount": 20,
      "overviewTourId": "thermal",
      "notes": {
        "zh-TW": "依前段架構跳過已完成步驟；可靠度使用獨立樣本分組，失效分析依症狀觸發。",
        "en": "Bypass operations already completed upstream. Reliability tests use separate cohorts; failure analysis is symptom-triggered."
      },
      "itemIds": [
        "V01",
        "V02",
        "V03",
        "V04",
        "V05",
        "V06",
        "V07",
        "V08",
        "V09",
        "V10",
        "V11",
        "V12",
        "V13",
        "V14",
        "V15",
        "V16",
        "V17",
        "V18",
        "V19",
        "V20"
      ]
    }
  ],
  "sources": [
    {
      "id": "tsmc-cowos",
      "publisher": "TSMC",
      "title": "CoWoS technology overview",
      "url": "https://3dfabric.tsmc.com/english/dedicatedFoundry/technology/cowos.htm",
      "sourceType": "primary",
      "checkedOn": "2026-11-24",
      "supports": "Architecture family context; CoWoS variants must not be treated as identical process flows.",
      "verification": "public page or primary document excerpt read; no private process recipe accessed"
    },
    {
      "id": "tsmc-info",
      "publisher": "TSMC",
      "title": "Integrated Fan-Out wafer-level packaging",
      "url": "https://3dfabric.tsmc.com/english/dedicatedFoundry/technology/InFO.htm",
      "sourceType": "primary",
      "checkedOn": "2026-11-24",
      "supports": "Fan-out architecture context, not the detailed recipe of the teaching RDL-first flow.",
      "verification": "public page or primary document excerpt read; no private process recipe accessed"
    },
    {
      "id": "tsmc-soic",
      "publisher": "TSMC",
      "title": "TSMC-SoIC",
      "url": "https://3dfabric.tsmc.com/english/dedicatedFoundry/technology/SoIC.htm",
      "sourceType": "primary",
      "checkedOn": "2026-11-24",
      "supports": "3D integration context; teaching hybrid-bond flow is not a TSMC SOP.",
      "verification": "public page or primary document excerpt read; no private process recipe accessed"
    },
    {
      "id": "amkor-tsv",
      "publisher": "Amkor",
      "title": "2.5D/3D TSV Packaging",
      "url": "https://amkor.com/technology/25d-3d-tsv/",
      "sourceType": "primary",
      "checkedOn": "2026-11-24",
      "supports": "Incoming blind-TSV wafers, temporary support, thinning, reveal, passivation, backside metallization and bumping; Amkor does not form the incoming foundry TSVs.",
      "verification": "public page or primary document excerpt read; no private process recipe accessed"
    },
    {
      "id": "amkor-tsv-sheet",
      "publisher": "Amkor",
      "title": "Through Silicon Via data sheet",
      "url": "https://amkor.com/kr/wp-content/uploads/2018/02/TSV_TS107.pdf",
      "sourceType": "primary",
      "checkedOn": "2026-11-24",
      "supports": "Chip-on-wafer attachment, functional die microbumps, molding/thinning, module-to-substrate integration and intermediate test capabilities.",
      "verification": "public page or primary document excerpt read; no private process recipe accessed"
    },
    {
      "id": "amkor-bumping",
      "publisher": "Amkor",
      "title": "Wafer Bumping Services",
      "url": "https://amkor.com/services/wafer-bumping/",
      "sourceType": "primary",
      "checkedOn": "2026-11-24",
      "supports": "Electroplated solder/Cu pillars, repassivation, redistribution and co-located probe/assembly/test.",
      "verification": "public page or primary document excerpt read; no private process recipe accessed"
    },
    {
      "id": "amkor-chiplets",
      "publisher": "Amkor",
      "title": "Readying the supply chain for chiplets and heterogeneous IC packaging",
      "url": "https://amkormarcomexternal.blob.core.windows.net/amkordotcom/wp-content/uploads/2024/03/Readying-the-supply-chain-for-chiplets-and-heterogeneous-integration_EN.pdf",
      "sourceType": "primary",
      "checkedOn": "2026-11-24",
      "supports": "Distinct silicon-interposer, high-density fan-out and bridge packaging routes; TSV reveal and backside finishing.",
      "verification": "public page or primary document excerpt read; no private process recipe accessed"
    },
    {
      "id": "ase-fanout",
      "publisher": "ASE",
      "title": "Fan-Out Packaging",
      "url": "https://ase.aseglobal.com/fan-out-packaging/",
      "sourceType": "primary",
      "checkedOn": "2026-11-24",
      "supports": "Chip-first versus chip-last/RDL-first ordering; die shift, mold, warpage and RDL integration trade-offs.",
      "verification": "public page or primary document excerpt read; no private process recipe accessed"
    },
    {
      "id": "applied-fanout",
      "publisher": "Applied Materials",
      "title": "Fan Out",
      "url": "https://www.appliedmaterials.com/il/en/semiconductor/markets-and-inflections/heterogeneous-integration/fan-out.html",
      "sourceType": "primary",
      "checkedOn": "2026-11-24",
      "supports": "Fan-out redistribution, molding, PVD barrier/seed and electrochemical metal deposition.",
      "verification": "public page or primary document excerpt read; no private process recipe accessed"
    },
    {
      "id": "lam-flow",
      "publisher": "Lam Research",
      "title": "The AI Revolution Depends on Advanced Packaging",
      "url": "https://newsroom.lamresearch.com/the-ai-revolution-relies-on-advanced-packaging",
      "sourceType": "primary",
      "checkedOn": "2026-11-24",
      "supports": "Barrier/seed, lithographic patterning, plating and TSV/RDL process families.",
      "verification": "public page or primary document excerpt read; no private process recipe accessed"
    },
    {
      "id": "lam-electrofill",
      "publisher": "Lam Research",
      "title": "SABRE 3D Product Family",
      "url": "https://www.lamresearch.com/product/sabre-3d/",
      "sourceType": "primary",
      "checkedOn": "2026-11-24",
      "supports": "Electrochemical deposition for wafer-level packaging and TSV interconnect structures.",
      "verification": "public page or primary document excerpt read; no private process recipe accessed"
    },
    {
      "id": "lam-etch",
      "publisher": "Lam Research",
      "title": "DSiE Product Family",
      "url": "https://www.lamresearch.com/product/dsie-product-family/",
      "sourceType": "primary",
      "checkedOn": "2026-11-24",
      "supports": "Silicon etch profile and depth uniformity for TSV structures.",
      "verification": "public page or primary document excerpt read; no private process recipe accessed"
    },
    {
      "id": "kla-deposition",
      "publisher": "KLA/SPTS",
      "title": "Wafer Processing Systems for Advanced Packaging",
      "url": "https://www.spts.com/products/packaging-manufacturing/wafer-processing-systems-for-advanced-packaging",
      "sourceType": "primary",
      "checkedOn": "2026-11-24",
      "supports": "Packaging etch/deposition, dielectrics for hybrid bonding, gap fill and interconnect processing.",
      "verification": "public page or primary document excerpt read; no private process recipe accessed"
    },
    {
      "id": "kla-metrology",
      "publisher": "KLA",
      "title": "Wafer Inspection and Metrology for Advanced Packaging",
      "url": "https://ask.kla-tencor.com/products/packaging-manufacturing/wafer-inspection-and-metrology-for-advanced-packaging",
      "sourceType": "primary",
      "checkedOn": "2026-11-24",
      "supports": "Bump height, RDL CD, UBM height, thickness, bow, defects, overlay and traceability metrology.",
      "verification": "public page or primary document excerpt read; no private process recipe accessed"
    },
    {
      "id": "imec-w2w",
      "publisher": "imec",
      "title": "Wafer-to-wafer hybrid bonding: pushing the boundaries",
      "url": "https://www.imec-int.com/en/articles/wafer-wafer-hybrid-bonding-pushing-boundaries-400nm-interconnect-pitch",
      "sourceType": "primary",
      "checkedOn": "2026-11-24",
      "supports": "Bond dielectric cavities, barrier/seed/Cu, CMP, copper recess, alignment, prebond and anneal sequence.",
      "verification": "public page or primary document excerpt read; no private process recipe accessed"
    },
    {
      "id": "imec-d2w",
      "publisher": "imec",
      "title": "Die-to-wafer hybrid bonding demonstration",
      "url": "https://www.imec-int.com/en/press/imec-demonstrates-die-wafer-hybrid-bonding-cu-interconnect-pad-pitch-2mm",
      "sourceType": "primary",
      "checkedOn": "2026-11-24",
      "supports": "D2W surface preparation, placement/alignment and electrical evaluation; research results are not universal production limits.",
      "verification": "public page or primary document excerpt read; no private process recipe accessed"
    },
    {
      "id": "evg-d2w",
      "publisher": "EV Group",
      "title": "Die-to-Wafer Bonding Steps into the Spotlight",
      "url": "https://www.evgroup.com/fileadmin/media/products/bonding/Die_to_Wafer_bonding_systems/White_Paper_D2W_Bonding.pdf",
      "sourceType": "primary",
      "checkedOn": "2026-11-24",
      "supports": "Protection, die/carrier preparation, activation, cleaning, transfer, bonding and metrology. Direct and collective transfer routes differ.",
      "verification": "public page or primary document excerpt read; no private process recipe accessed"
    },
    {
      "id": "evg-activation",
      "publisher": "EV Group",
      "title": "EVG320 D2W preparation and activation announcement",
      "url": "https://www.evgroup.com/fileadmin/media/company/news/2020/2020_12_10_EVG320_D2W/Press_Release_EVG320_D2W_2012_12_10_EN.pdf",
      "sourceType": "primary",
      "checkedOn": "2026-11-24",
      "supports": "Cleaning, plasma activation, die alignment verification and prebond metrology.",
      "verification": "public page or primary document excerpt read; no private process recipe accessed"
    },
    {
      "id": "evg-process",
      "publisher": "EV Group",
      "title": "Process Services portfolio",
      "url": "https://www.evgroup.com/fileadmin/media/company/service/Process_Services_Flyer_24_04.pdf",
      "sourceType": "primary",
      "checkedOn": "2026-11-24",
      "supports": "Resist coating, exposure/develop, lift-off, temporary bonding, bond alignment and wafer processing capabilities.",
      "verification": "public page or primary document excerpt read; no private process recipe accessed"
    },
    {
      "id": "bruker-bond",
      "publisher": "Bruker",
      "title": "Surface Metrology for Hybrid Bonding in Advanced Semiconductor Packaging",
      "url": "https://www.bruker.com/en/products-and-solutions/semiconductor-solutions/automated-afm-and-cipt-systems/resource-library/an-5001-surface-metrology-for-hybrid-bonding-in-advanced-semiconductor-packaging.html",
      "sourceType": "primary",
      "checkedOn": "2026-11-24",
      "supports": "AFM/AFP checks of copper recess, dielectric roughness and long-range topography; no numeric acceptance limit copied into this curriculum.",
      "verification": "public page or primary document excerpt read; no private process recipe accessed"
    },
    {
      "id": "intel-emib",
      "publisher": "Intel",
      "title": "EMIB Technology Brief",
      "url": "https://www.intel.com/content/dam/www/central-libraries/us/en/documents/2025-07/emib-product-brief.pdf",
      "sourceType": "primary",
      "checkedOn": "2026-11-24",
      "supports": "Local bridge in substrate cavity, adhesive, dielectric/metal build-up and fine/coarse bump regions; not a full silicon interposer.",
      "verification": "public page or primary document excerpt read; no private process recipe accessed"
    },
    {
      "id": "intel-packaging",
      "publisher": "Intel",
      "title": "Advanced Packaging Innovations",
      "url": "https://www.intel.com/content/www/us/en/foundry/packaging.htm",
      "sourceType": "primary",
      "checkedOn": "2026-11-24",
      "supports": "Bridge and hybrid-bond architecture context, known-good die, ATE and system-level test. EMIB-T variants can contain TSVs.",
      "verification": "public page or primary document excerpt read; no private process recipe accessed"
    },
    {
      "id": "intel-design-flow",
      "publisher": "Intel / Siemens EDA",
      "title": "EMIB-based advanced packaging flow — Intel Foundry presentation",
      "url": "https://blogs.sw.siemens.com/semiconductor-packaging/2024/08/12/user2user-2024-emib-based-advanced-packaging-flow-intel-foundry/",
      "sourceType": "primary",
      "checkedOn": "2026-11-24",
      "supports": "Die data integration, bump management and simultaneous bridge/substrate co-design.",
      "verification": "public page or primary document excerpt read; no private process recipe accessed"
    },
    {
      "id": "cadence-3dic",
      "publisher": "Cadence",
      "title": "3D-IC Design Challenges and Requirements",
      "url": "https://www.cadence.com/en_US/home/resources/white-papers/3d-ic-design-wp.html",
      "sourceType": "primary",
      "checkedOn": "2026-11-24",
      "supports": "Cross-die signal/power/thermal analysis, DFT access and known-good-die/stack test planning.",
      "verification": "public page or primary document excerpt read; no private process recipe accessed"
    },
    {
      "id": "cadence-integrity",
      "publisher": "Cadence",
      "title": "Integrity 3D-IC Platform Datasheet",
      "url": "https://www.cadence.com/content/dam/cadence-www/global/en_US/documents/tools/digital-design-signoff/Integrity-3D-IC-DS-v1.pdf",
      "sourceType": "primary",
      "checkedOn": "2026-11-24",
      "supports": "Implementation, manufacturing awareness, timing, signal integrity and thermal co-analysis.",
      "verification": "public page or primary document excerpt read; no private process recipe accessed"
    },
    {
      "id": "ucie",
      "publisher": "UCIe Consortium",
      "title": "UCIe specifications overview",
      "url": "https://www.uciexpress.org/specifications",
      "sourceType": "primary",
      "checkedOn": "2026-11-24",
      "supports": "Die-to-die physical/protocol/management interfaces and compliance context; UCIe is not a manufacturing operation.",
      "verification": "public page or primary document excerpt read; no private process recipe accessed"
    },
    {
      "id": "disco-solutions",
      "publisher": "DISCO",
      "title": "Dicing, grinding and polishing solutions",
      "url": "https://www.disco.co.jp/eg/solution/",
      "sourceType": "primary",
      "checkedOn": "2026-11-24",
      "supports": "Distinct singulation, thinning and damage-removal techniques; order depends on selected route.",
      "verification": "public page or primary document excerpt read; no private process recipe accessed"
    },
    {
      "id": "disco-taiko",
      "publisher": "DISCO",
      "title": "TAIKO Process",
      "url": "https://www-hq.disco.co.jp/eg/solution/library/grinder/taiko_process.html",
      "sourceType": "primary",
      "checkedOn": "2026-11-24",
      "supports": "Alternative thin-wafer handling using an unground edge; not combined as a mandatory step with carrier-supported thinning.",
      "verification": "public page or primary document excerpt read; no private process recipe accessed"
    },
    {
      "id": "besi-tcb",
      "publisher": "Besi",
      "title": "Thermo Compression Bonding",
      "url": "https://www.besi.com/products-technology/product-details/productgroup/thermo-compression-bonding/",
      "sourceType": "primary",
      "checkedOn": "2026-11-24",
      "supports": "Precision placement and thermocompression joining equipment family.",
      "verification": "public page or primary document excerpt read; no private process recipe accessed"
    },
    {
      "id": "nordson-underfill",
      "publisher": "Nordson",
      "title": "Underfill",
      "url": "https://www.nordson.com/en/divisions/electronics-solutions/your-process/fluid-types/underfill",
      "sourceType": "primary",
      "checkedOn": "2026-11-24",
      "supports": "Capillary and no-flow underfill are different sequences; capillary filling and thermo-mechanical joint reinforcement.",
      "verification": "public page or primary document excerpt read; no private process recipe accessed"
    },
    {
      "id": "nordson-tim",
      "publisher": "Nordson",
      "title": "PCB and SMT assembly fluid applications",
      "url": "https://www.nordson.com/en/divisions/electronics-solutions/your-process/industries/pcb-and-smt-assembly",
      "sourceType": "primary",
      "checkedOn": "2026-11-24",
      "supports": "TIM transfers heat to a heat sink or case; dispensing and assembly context.",
      "verification": "public page or primary document excerpt read; no private process recipe accessed"
    },
    {
      "id": "ase-thermal",
      "publisher": "ASE",
      "title": "Stress and Thermal Lab",
      "url": "https://ase.aseglobal.com/lab-services/stress-and-thermal-lab/",
      "sourceType": "primary",
      "checkedOn": "2026-11-24",
      "supports": "Thermal/stress/warpage models, materials selection, mechanical tests, thermal measurements and board-level reliability.",
      "verification": "public page or primary document excerpt read; no private process recipe accessed"
    },
    {
      "id": "ase-fa",
      "publisher": "ASE",
      "title": "Failure Analysis Lab",
      "url": "https://ase.aseglobal.com/lab-services/failure-analysis-lab/",
      "sourceType": "primary",
      "checkedOn": "2026-11-24",
      "supports": "Nondestructive X-ray/SAT/electrical localization before cross-section/FIB analysis; packaging failure categories.",
      "verification": "public page or primary document excerpt read; no private process recipe accessed"
    },
    {
      "id": "amkor-test",
      "publisher": "Amkor",
      "title": "IC Semiconductor Test Services",
      "url": "https://amkor.com/test-services/",
      "sourceType": "primary",
      "checkedOn": "2026-11-24",
      "supports": "Wafer, package and system-level test, temperature control, handling and yield analysis.",
      "verification": "public page or primary document excerpt read; no private process recipe accessed"
    },
    {
      "id": "advantest-ate",
      "publisher": "Advantest",
      "title": "What Is ATE?",
      "url": "https://www.advantest.com/en/semiconductor-basics/automated-test-equipment/",
      "sourceType": "primary",
      "checkedOn": "2026-11-24",
      "supports": "Wafer/die/package/system test, known-good-die screening and ATE measurement roles.",
      "verification": "public page or primary document excerpt read; no private process recipe accessed"
    },
    {
      "id": "ieee-test",
      "publisher": "IEEE EPS Test Technical Committee",
      "title": "Heterogeneous Integration Product Testability Best Known Methods",
      "url": "https://cmte.ieee.org/eps-test/wp-content/uploads/sites/132/2022/01/IEEE_EPS_Test_Het_Int_Product_Testability_BKM_Final_v1_0-1-14-22-1.pdf",
      "sourceType": "primary",
      "checkedOn": "2026-11-24",
      "supports": "Die, stack and package testability planning; KGD does not eliminate package-induced faults.",
      "verification": "public page or primary document excerpt read; no private process recipe accessed"
    },
    {
      "id": "amkor-quality",
      "publisher": "Amkor",
      "title": "Quality Brochure",
      "url": "https://amkor.com/wp-content/uploads/2019/08/Quality_Brochure-BR206.pdf",
      "sourceType": "primary",
      "checkedOn": "2026-11-24",
      "supports": "Reliability testing, qualification evidence and failure-analysis instrumentation.",
      "verification": "public page or primary document excerpt read; no private process recipe accessed"
    },
    {
      "id": "amkor-mechanical",
      "publisher": "Amkor",
      "title": "Mechanical Package Characterization",
      "url": "https://amkor.com/kr/wp-content/uploads/2018/02/Mechanical_Package_Characterization_SS23.pdf",
      "sourceType": "primary",
      "checkedOn": "2026-11-24",
      "supports": "Warpage prediction, thermal cycling, temperature storage and humidity reliability context.",
      "verification": "public page or primary document excerpt read; no private process recipe accessed"
    }
  ],
  "items": [
    {
      "id": "C01",
      "catalogueOrder": 1,
      "branchId": "common",
      "branchOrder": 1,
      "activityType": "design",
      "title": {
        "zh-TW": "定義系統任務與封裝需求",
        "en": "Define system and package requirements"
      },
      "summary": {
        "zh-TW": "以工作負載、介面與外形限制為起點，建立功率、頻寬與可測試性需求表。交付可追溯需求基線，以需求對應量測指標與責任人判讀結果；重點辨識只追峰值頻寬而漏掉持續功率。",
        "en": "Start with workloads, interfaces and envelope constraints; define power, bandwidth and testability requirements to obtain a traceable requirements baseline. Assess the result using requirement-to-metric and ownership review, with particular attention to a peak-bandwidth target that ignores sustained power."
      },
      "input": {
        "zh-TW": "工作負載、介面與外形限制",
        "en": "workloads, interfaces and envelope constraints"
      },
      "operation": {
        "zh-TW": "建立功率、頻寬與可測試性需求表",
        "en": "define power, bandwidth and testability requirements"
      },
      "output": {
        "zh-TW": "可追溯需求基線",
        "en": "a traceable requirements baseline"
      },
      "qualityEvidence": {
        "zh-TW": "需求對應量測指標與責任人",
        "en": "requirement-to-metric and ownership review"
      },
      "failureMode": {
        "zh-TW": "只追峰值頻寬而漏掉持續功率",
        "en": "a peak-bandwidth target that ignores sustained power"
      },
      "prerequisiteIds": [],
      "prerequisiteAnyOf": [],
      "overviewTourId": "interposer",
      "sourceIds": [
        "cadence-3dic",
        "amkor-chiplets"
      ],
      "sourceUrls": [
        "https://www.cadence.com/en_US/home/resources/white-papers/3d-ic-design-wp.html",
        "https://amkormarcomexternal.blob.core.windows.net/amkordotcom/wp-content/uploads/2024/03/Readying-the-supply-chain-for-chiplets-and-heterogeneous-integration_EN.pdf"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "produced",
      "videoUrl": "assets/packaging-process-v34/C01/C01.mp4",
      "scriptStatus": "complete",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      },
      "playerUrl": "packaging-process-film-v34.html",
      "filmLanguages": [
        "zh-TW",
        "zh-CN",
        "en",
        "ja",
        "ko"
      ],
      "longLesson": {
        "status": "local_verified",
        "durationSeconds": 900,
        "youtubeId": null,
        "youtubeStatus": "pending_quota",
        "bundleStatus": "PUBLIC_VERIFIED",
        "bundleUrl": "https://github.com/kuonanhong/macgyver-academy/releases/download/packaging-process-v35/C01-long_15min_V34.zip",
        "bundleSha256": "a6c9f88d1c710dd1cc579443b3a965b1783bc7fa7b116a591b6bb192775a7178",
        "bundleBytes": 181611331
      },
      "filmVerification": {
        "status": "PASS",
        "durationSeconds": 300,
        "frames": 7200,
        "sha256": "fee6ec0dc01d40b16c646d1b00609296ecf7612df43dd29b347fec3a5d099f66",
        "bytes": 52549959,
        "manifestUrl": "assets/packaging-process-v34/C01/manifest.json",
        "audioTracks": 5,
        "subtitleTracks": 5,
        "speechAlignedSentences": 248
      }
    },
    {
      "id": "C02",
      "catalogueOrder": 2,
      "branchId": "common",
      "branchOrder": 2,
      "activityType": "design",
      "title": {
        "zh-TW": "劃分運算、記憶體與I/O晶粒",
        "en": "Partition compute, memory and I/O"
      },
      "summary": {
        "zh-TW": "以系統功能圖與製程選項為起點，決定功能留在單晶粒或分拆為小晶片。交付功能分割與跨晶粒流量表，以跨界資料量與時序預算判讀結果；重點辨識過度分割造成互連能耗上升。",
        "en": "Start with system functions and technology options; allocate functions to monolithic dies or chiplets to obtain a partition and cross-die traffic map. Assess the result using traffic across boundaries and timing budgets, with particular attention to over-partitioning that increases link energy."
      },
      "input": {
        "zh-TW": "系統功能圖與製程選項",
        "en": "system functions and technology options"
      },
      "operation": {
        "zh-TW": "決定功能留在單晶粒或分拆為小晶片",
        "en": "allocate functions to monolithic dies or chiplets"
      },
      "output": {
        "zh-TW": "功能分割與跨晶粒流量表",
        "en": "a partition and cross-die traffic map"
      },
      "qualityEvidence": {
        "zh-TW": "跨界資料量與時序預算",
        "en": "traffic across boundaries and timing budgets"
      },
      "failureMode": {
        "zh-TW": "過度分割造成互連能耗上升",
        "en": "over-partitioning that increases link energy"
      },
      "prerequisiteIds": [
        "C01"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "interposer",
      "sourceIds": [
        "cadence-3dic",
        "amkor-chiplets"
      ],
      "sourceUrls": [
        "https://www.cadence.com/en_US/home/resources/white-papers/3d-ic-design-wp.html",
        "https://amkormarcomexternal.blob.core.windows.net/amkordotcom/wp-content/uploads/2024/03/Readying-the-supply-chain-for-chiplets-and-heterogeneous-integration_EN.pdf"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "produced",
      "videoUrl": "https://github.com/kuonanhong/macgyver-academy/releases/download/packaging-process-v35/C02.mp4",
      "scriptStatus": "complete",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      },
      "playerUrl": "packaging-film-v35.html?film=C02",
      "filmLanguages": [
        "zh-TW",
        "zh-CN",
        "en",
        "ja",
        "ko"
      ],
      "filmVerification": {
        "status": "PASS",
        "id": "C02",
        "durationSeconds": 300,
        "frames": 7200,
        "sha256": "c2252c8341baea594b2b12788305f5b22fb9d78b753c1cf85a8eb2e3d75dd35f",
        "bytes": 52504573,
        "audioTracks": 5,
        "subtitleTracks": 5,
        "speechAlignedSentences": 200,
        "scriptSha256": "79ef6e9d59087beec8d1a3b56826d3117a11590d9c40e940608464859313af88",
        "hostVerification": {
          "status": "PUBLIC_VERIFIED",
          "method": "Parent verified GitHub Release asset API digest/size against local final files; this builder independently checks the proof against those exact files."
        },
        "endCard": {
          "url": "https://line.me/R/ti/p/%40530pgchc",
          "startSeconds": 290,
          "endSeconds": 300,
          "rectangle": {
            "x": 1038,
            "y": 246,
            "width": 210,
            "height": 289
          },
          "verified": true,
          "method": "Actual encoded frames decoded by OpenCV QRCodeDetector"
        },
        "manifestUrl": "assets/packaging-films-v35/C02/verification.json"
      },
      "longLesson": {
        "status": "local_verified",
        "durationSeconds": 900,
        "sha256": "2e8e5c6383853c5483daf5fda6d926123ebd2ef2ada9a7d0810d9ead3498f5c4",
        "bytes": 157128810,
        "publicationStatus": "not_published",
        "youtubeStatus": "pending",
        "youtubeId": null
      }
    },
    {
      "id": "C03",
      "catalogueOrder": 3,
      "branchId": "common",
      "branchOrder": 3,
      "activityType": "design",
      "title": {
        "zh-TW": "選擇封裝架構分支",
        "en": "Select the packaging architecture"
      },
      "summary": {
        "zh-TW": "以功能分割、成本與供應鏈條件為起點，比較矽中介層、扇出、混合鍵合與局部矽橋。交付具取捨理由的架構決策，以需求涵蓋率與供應可行性判讀結果；重點辨識把所有替代架構誤串成同一條線。",
        "en": "Start with partitioning, cost and supply constraints; compare interposer, fan-out, hybrid-bond and local-bridge routes to obtain an architecture decision with trade-offs. Assess the result using requirement coverage and supplier feasibility, with particular attention to treating alternative architectures as one mandatory process."
      },
      "input": {
        "zh-TW": "功能分割、成本與供應鏈條件",
        "en": "partitioning, cost and supply constraints"
      },
      "operation": {
        "zh-TW": "比較矽中介層、扇出、混合鍵合與局部矽橋",
        "en": "compare interposer, fan-out, hybrid-bond and local-bridge routes"
      },
      "output": {
        "zh-TW": "具取捨理由的架構決策",
        "en": "an architecture decision with trade-offs"
      },
      "qualityEvidence": {
        "zh-TW": "需求涵蓋率與供應可行性",
        "en": "requirement coverage and supplier feasibility"
      },
      "failureMode": {
        "zh-TW": "把所有替代架構誤串成同一條線",
        "en": "treating alternative architectures as one mandatory process"
      },
      "prerequisiteIds": [
        "C02"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "interposer",
      "sourceIds": [
        "tsmc-cowos",
        "tsmc-info",
        "tsmc-soic",
        "intel-packaging"
      ],
      "sourceUrls": [
        "https://3dfabric.tsmc.com/english/dedicatedFoundry/technology/cowos.htm",
        "https://3dfabric.tsmc.com/english/dedicatedFoundry/technology/InFO.htm",
        "https://3dfabric.tsmc.com/english/dedicatedFoundry/technology/SoIC.htm",
        "https://www.intel.com/content/www/us/en/foundry/packaging.htm"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "produced",
      "videoUrl": "https://github.com/kuonanhong/macgyver-academy/releases/download/packaging-process-v35/C03.mp4",
      "scriptStatus": "complete",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      },
      "playerUrl": "packaging-film-v35.html?film=C03",
      "filmLanguages": [
        "zh-TW",
        "zh-CN",
        "en",
        "ja",
        "ko"
      ],
      "filmVerification": {
        "status": "PASS",
        "id": "C03",
        "durationSeconds": 300,
        "frames": 7200,
        "sha256": "f166e7395a9dd0cdb063f1cd4349e6473f5ea254101980b6ea93e33973c7f881",
        "bytes": 52601179,
        "audioTracks": 5,
        "subtitleTracks": 5,
        "speechAlignedSentences": 200,
        "scriptSha256": "c6f0db1ec0f96e9e52acaa5d51a5dc683c64424ea9bdf1fb218616ca5af63743",
        "hostVerification": {
          "status": "PUBLIC_VERIFIED",
          "method": "Parent verified GitHub Release asset API digest/size against local final files; this builder independently checks the proof against those exact files."
        },
        "endCard": {
          "url": "https://line.me/R/ti/p/%40530pgchc",
          "startSeconds": 290,
          "endSeconds": 300,
          "rectangle": {
            "x": 1038,
            "y": 246,
            "width": 210,
            "height": 289
          },
          "verified": true,
          "method": "Actual encoded frames decoded by OpenCV QRCodeDetector"
        },
        "manifestUrl": "assets/packaging-films-v35/C03/verification.json"
      },
      "longLesson": {
        "status": "local_verified",
        "durationSeconds": 900,
        "sha256": "c27d9a57276056429864ff0bab4a84eb797ab46111af8a89ffc74ae034875ff6",
        "bytes": 157623868,
        "publicationStatus": "not_published",
        "youtubeStatus": "pending",
        "youtubeId": null
      }
    },
    {
      "id": "C04",
      "catalogueOrder": 4,
      "branchId": "common",
      "branchOrder": 4,
      "activityType": "design",
      "title": {
        "zh-TW": "建立晶粒接點與電源網表",
        "en": "Create bump and power-net maps"
      },
      "summary": {
        "zh-TW": "以晶粒介面文件與腳位命名為起點，統一接點方向、訊號與電源對應。交付具版本的封裝接點網表，以旋轉鏡射與網路一致性檢查判讀結果；重點辨識接點鏡射或電源接錯。",
        "en": "Start with die interface files and net naming; normalize orientation, signal and power assignments to obtain a versioned package connectivity map. Assess the result using rotation, mirroring and net-consistency checks, with particular attention to mirrored pads or incorrect power assignment."
      },
      "input": {
        "zh-TW": "晶粒介面文件與腳位命名",
        "en": "die interface files and net naming"
      },
      "operation": {
        "zh-TW": "統一接點方向、訊號與電源對應",
        "en": "normalize orientation, signal and power assignments"
      },
      "output": {
        "zh-TW": "具版本的封裝接點網表",
        "en": "a versioned package connectivity map"
      },
      "qualityEvidence": {
        "zh-TW": "旋轉鏡射與網路一致性檢查",
        "en": "rotation, mirroring and net-consistency checks"
      },
      "failureMode": {
        "zh-TW": "接點鏡射或電源接錯",
        "en": "mirrored pads or incorrect power assignment"
      },
      "prerequisiteIds": [
        "C03"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "interposer",
      "sourceIds": [
        "intel-design-flow",
        "cadence-integrity"
      ],
      "sourceUrls": [
        "https://blogs.sw.siemens.com/semiconductor-packaging/2024/08/12/user2user-2024-emib-based-advanced-packaging-flow-intel-foundry/",
        "https://www.cadence.com/content/dam/cadence-www/global/en_US/documents/tools/digital-design-signoff/Integrity-3D-IC-DS-v1.pdf"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "produced",
      "videoUrl": "https://github.com/kuonanhong/macgyver-academy/releases/download/packaging-process-v35/C04.mp4",
      "scriptStatus": "complete",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      },
      "playerUrl": "packaging-film-v35.html?film=C04",
      "filmLanguages": [
        "zh-TW",
        "zh-CN",
        "en",
        "ja",
        "ko"
      ],
      "filmVerification": {
        "status": "PASS",
        "id": "C04",
        "durationSeconds": 300,
        "frames": 7200,
        "sha256": "d347968bf1864c67ab6bd790274284a6ed0996359d6ba17f8fd2c72321222207",
        "bytes": 52686385,
        "audioTracks": 5,
        "subtitleTracks": 5,
        "speechAlignedSentences": 200,
        "scriptSha256": "e73ce258d61f8716e41bd26db00e726f9ec0a7d9ac8b2e6a144f6a5afec2161d",
        "hostVerification": {
          "status": "PUBLIC_VERIFIED",
          "method": "Parent verified GitHub Release asset API digest/size against local final files; this builder independently checks the proof against those exact files."
        },
        "endCard": {
          "url": "https://line.me/R/ti/p/%40530pgchc",
          "startSeconds": 290,
          "endSeconds": 300,
          "rectangle": {
            "x": 1038,
            "y": 246,
            "width": 210,
            "height": 289
          },
          "verified": true,
          "method": "Actual encoded frames decoded by OpenCV QRCodeDetector"
        },
        "manifestUrl": "assets/packaging-films-v35/C04/verification.json"
      },
      "longLesson": {
        "status": "local_verified",
        "durationSeconds": 900,
        "sha256": "477878d0030f522cf805f54c594419ddf93fd9bfde5dd0e5414e7806013e81db",
        "bytes": 157843327,
        "publicationStatus": "not_published",
        "youtubeStatus": "pending",
        "youtubeId": null
      }
    },
    {
      "id": "C05",
      "catalogueOrder": 5,
      "branchId": "common",
      "branchOrder": 5,
      "activityType": "design",
      "title": {
        "zh-TW": "配置晶粒位置與可組裝間距",
        "en": "Place dies and reserve assembly access"
      },
      "summary": {
        "zh-TW": "以晶粒尺寸、接點圖與工具限制為起點，安排位置並保留貼裝、填膠與散熱空間。交付可組裝的初步平面配置，以邊界碰撞與工具可達性檢查判讀結果；重點辨識電路可連但工具無法進入。",
        "en": "Start with die outlines, bump maps and tool constraints; place dies with access for placement, underfill and cooling to obtain an assembly-aware floorplan. Assess the result using keep-out and tool-access review, with particular attention to a routable layout that cannot be assembled."
      },
      "input": {
        "zh-TW": "晶粒尺寸、接點圖與工具限制",
        "en": "die outlines, bump maps and tool constraints"
      },
      "operation": {
        "zh-TW": "安排位置並保留貼裝、填膠與散熱空間",
        "en": "place dies with access for placement, underfill and cooling"
      },
      "output": {
        "zh-TW": "可組裝的初步平面配置",
        "en": "an assembly-aware floorplan"
      },
      "qualityEvidence": {
        "zh-TW": "邊界碰撞與工具可達性檢查",
        "en": "keep-out and tool-access review"
      },
      "failureMode": {
        "zh-TW": "電路可連但工具無法進入",
        "en": "a routable layout that cannot be assembled"
      },
      "prerequisiteIds": [
        "C04"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "interposer",
      "sourceIds": [
        "intel-design-flow",
        "cadence-integrity"
      ],
      "sourceUrls": [
        "https://blogs.sw.siemens.com/semiconductor-packaging/2024/08/12/user2user-2024-emib-based-advanced-packaging-flow-intel-foundry/",
        "https://www.cadence.com/content/dam/cadence-www/global/en_US/documents/tools/digital-design-signoff/Integrity-3D-IC-DS-v1.pdf"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "C06",
      "catalogueOrder": 6,
      "branchId": "common",
      "branchOrder": 6,
      "activityType": "design",
      "title": {
        "zh-TW": "分析晶粒間訊號完整性",
        "en": "Analyze die-to-die signal integrity"
      },
      "summary": {
        "zh-TW": "以初步走線與接點模型為起點，檢查損耗、反射與串擾。交付附假設的通道裕量報告，以S參數與眼圖的模型一致性判讀結果；重點辨識忽略返回路徑導致模型過度樂觀。",
        "en": "Start with initial routes and interconnect models; evaluate loss, reflections and crosstalk to obtain a channel-margin report with assumptions. Assess the result using consistent S-parameters and eye analysis, with particular attention to optimistic models that omit return paths."
      },
      "input": {
        "zh-TW": "初步走線與接點模型",
        "en": "initial routes and interconnect models"
      },
      "operation": {
        "zh-TW": "檢查損耗、反射與串擾",
        "en": "evaluate loss, reflections and crosstalk"
      },
      "output": {
        "zh-TW": "附假設的通道裕量報告",
        "en": "a channel-margin report with assumptions"
      },
      "qualityEvidence": {
        "zh-TW": "S參數與眼圖的模型一致性",
        "en": "consistent S-parameters and eye analysis"
      },
      "failureMode": {
        "zh-TW": "忽略返回路徑導致模型過度樂觀",
        "en": "optimistic models that omit return paths"
      },
      "prerequisiteIds": [
        "C05"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "interposer",
      "sourceIds": [
        "cadence-3dic",
        "cadence-integrity"
      ],
      "sourceUrls": [
        "https://www.cadence.com/en_US/home/resources/white-papers/3d-ic-design-wp.html",
        "https://www.cadence.com/content/dam/cadence-www/global/en_US/documents/tools/digital-design-signoff/Integrity-3D-IC-DS-v1.pdf"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "C07",
      "catalogueOrder": 7,
      "branchId": "common",
      "branchOrder": 7,
      "activityType": "design",
      "title": {
        "zh-TW": "設計封裝供電與去耦網路",
        "en": "Design package power delivery"
      },
      "summary": {
        "zh-TW": "以電源軌、負載變動與佈局為起點，配置供電回路與去耦位置。交付供電網路與壓降預算，以阻抗、壓降與電流密度檢查判讀結果；重點辨識去耦位置不當或局部電流擁擠。",
        "en": "Start with power rails, load transients and layout; allocate power paths and decoupling to obtain a PDN and voltage-drop budget. Assess the result using impedance, drop and current-density checks, with particular attention to poor decoupling placement or current crowding."
      },
      "input": {
        "zh-TW": "電源軌、負載變動與佈局",
        "en": "power rails, load transients and layout"
      },
      "operation": {
        "zh-TW": "配置供電回路與去耦位置",
        "en": "allocate power paths and decoupling"
      },
      "output": {
        "zh-TW": "供電網路與壓降預算",
        "en": "a PDN and voltage-drop budget"
      },
      "qualityEvidence": {
        "zh-TW": "阻抗、壓降與電流密度檢查",
        "en": "impedance, drop and current-density checks"
      },
      "failureMode": {
        "zh-TW": "去耦位置不當或局部電流擁擠",
        "en": "poor decoupling placement or current crowding"
      },
      "prerequisiteIds": [
        "C06"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "interposer",
      "sourceIds": [
        "cadence-3dic",
        "cadence-integrity"
      ],
      "sourceUrls": [
        "https://www.cadence.com/en_US/home/resources/white-papers/3d-ic-design-wp.html",
        "https://www.cadence.com/content/dam/cadence-www/global/en_US/documents/tools/digital-design-signoff/Integrity-3D-IC-DS-v1.pdf"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "C08",
      "catalogueOrder": 8,
      "branchId": "common",
      "branchOrder": 8,
      "activityType": "design",
      "title": {
        "zh-TW": "建立穩態與瞬態熱模型",
        "en": "Build steady and transient thermal models"
      },
      "summary": {
        "zh-TW": "以功率地圖、材料與邊界條件為起點，模擬熱點及脈衝負載升溫。交付可追溯的溫度場預測，以能量平衡與邊界敏感度判讀結果；重點辨識用不同環境條件比較散熱方案。",
        "en": "Start with power maps, materials and boundary conditions; simulate hotspots and transient heating to obtain a traceable temperature-field prediction. Assess the result using energy balance and boundary sensitivity, with particular attention to comparing coolers under unequal ambient conditions."
      },
      "input": {
        "zh-TW": "功率地圖、材料與邊界條件",
        "en": "power maps, materials and boundary conditions"
      },
      "operation": {
        "zh-TW": "模擬熱點及脈衝負載升溫",
        "en": "simulate hotspots and transient heating"
      },
      "output": {
        "zh-TW": "可追溯的溫度場預測",
        "en": "a traceable temperature-field prediction"
      },
      "qualityEvidence": {
        "zh-TW": "能量平衡與邊界敏感度",
        "en": "energy balance and boundary sensitivity"
      },
      "failureMode": {
        "zh-TW": "用不同環境條件比較散熱方案",
        "en": "comparing coolers under unequal ambient conditions"
      },
      "prerequisiteIds": [
        "C07"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "interposer",
      "sourceIds": [
        "ase-thermal",
        "cadence-integrity"
      ],
      "sourceUrls": [
        "https://ase.aseglobal.com/lab-services/stress-and-thermal-lab/",
        "https://www.cadence.com/content/dam/cadence-www/global/en_US/documents/tools/digital-design-signoff/Integrity-3D-IC-DS-v1.pdf"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "C09",
      "catalogueOrder": 9,
      "branchId": "common",
      "branchOrder": 9,
      "activityType": "design",
      "title": {
        "zh-TW": "預測熱機應力與翹曲",
        "en": "Predict stress and warpage"
      },
      "summary": {
        "zh-TW": "以堆疊、熱膨脹與彈性資料為起點，分析溫度變化下的變形與界面應力。交付翹曲與高應力位置圖，以材料資料與量測形變的對照判讀結果；重點辨識使用不相容材料參數掩蓋裂紋風險。",
        "en": "Start with stack-up, expansion and elastic data; analyze deformation and interface stress versus temperature to obtain warpage and stress-concentration maps. Assess the result using material-input and measured-shape correlation, with particular attention to incompatible material assumptions hiding crack risk."
      },
      "input": {
        "zh-TW": "堆疊、熱膨脹與彈性資料",
        "en": "stack-up, expansion and elastic data"
      },
      "operation": {
        "zh-TW": "分析溫度變化下的變形與界面應力",
        "en": "analyze deformation and interface stress versus temperature"
      },
      "output": {
        "zh-TW": "翹曲與高應力位置圖",
        "en": "warpage and stress-concentration maps"
      },
      "qualityEvidence": {
        "zh-TW": "材料資料與量測形變的對照",
        "en": "material-input and measured-shape correlation"
      },
      "failureMode": {
        "zh-TW": "使用不相容材料參數掩蓋裂紋風險",
        "en": "incompatible material assumptions hiding crack risk"
      },
      "prerequisiteIds": [
        "C08"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "interposer",
      "sourceIds": [
        "ase-thermal",
        "amkor-mechanical"
      ],
      "sourceUrls": [
        "https://ase.aseglobal.com/lab-services/stress-and-thermal-lab/",
        "https://amkor.com/kr/wp-content/uploads/2018/02/Mechanical_Package_Characterization_SS23.pdf"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "C10",
      "catalogueOrder": 10,
      "branchId": "common",
      "branchOrder": 10,
      "activityType": "design",
      "title": {
        "zh-TW": "規劃晶粒與封裝測試存取",
        "en": "Plan die and package test access"
      },
      "summary": {
        "zh-TW": "以分割架構與故障覆蓋目標為起點，設計可觀測與可控制的測試路徑。交付DFT與測試模式清單，以每個互連的測試可達性判讀結果；重點辨識堆疊完成後無法定位故障晶粒。",
        "en": "Start with partitioned architecture and fault targets; design controllable and observable test paths to obtain a DFT and test-mode plan. Assess the result using test access to individual interconnects, with particular attention to inability to isolate a faulty die after stacking."
      },
      "input": {
        "zh-TW": "分割架構與故障覆蓋目標",
        "en": "partitioned architecture and fault targets"
      },
      "operation": {
        "zh-TW": "設計可觀測與可控制的測試路徑",
        "en": "design controllable and observable test paths"
      },
      "output": {
        "zh-TW": "DFT與測試模式清單",
        "en": "a DFT and test-mode plan"
      },
      "qualityEvidence": {
        "zh-TW": "每個互連的測試可達性",
        "en": "test access to individual interconnects"
      },
      "failureMode": {
        "zh-TW": "堆疊完成後無法定位故障晶粒",
        "en": "inability to isolate a faulty die after stacking"
      },
      "prerequisiteIds": [
        "C09"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "interposer",
      "sourceIds": [
        "ieee-test",
        "cadence-3dic"
      ],
      "sourceUrls": [
        "https://cmte.ieee.org/eps-test/wp-content/uploads/sites/132/2022/01/IEEE_EPS_Test_Het_Int_Product_Testability_BKM_Final_v1_0-1-14-22-1.pdf",
        "https://www.cadence.com/en_US/home/resources/white-papers/3d-ic-design-wp.html"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "C11",
      "catalogueOrder": 11,
      "branchId": "common",
      "branchOrder": 11,
      "activityType": "design",
      "title": {
        "zh-TW": "制定已知良品晶粒策略",
        "en": "Define the known-good-die strategy"
      },
      "summary": {
        "zh-TW": "以晶粒測試能力與組裝成本為起點，分配組裝前後的篩選與重測內容。交付KGD覆蓋率與追溯規則，以漏失風險與組裝後故障覆蓋判讀結果；重點辨識把KGD標籤當成終身無故障保證。",
        "en": "Start with die-test capability and assembly cost; allocate prebond screening and postbond retest to obtain KGD coverage and traceability rules. Assess the result using escape risk and post-assembly fault coverage, with particular attention to treating KGD as a lifetime defect-free guarantee."
      },
      "input": {
        "zh-TW": "晶粒測試能力與組裝成本",
        "en": "die-test capability and assembly cost"
      },
      "operation": {
        "zh-TW": "分配組裝前後的篩選與重測內容",
        "en": "allocate prebond screening and postbond retest"
      },
      "output": {
        "zh-TW": "KGD覆蓋率與追溯規則",
        "en": "KGD coverage and traceability rules"
      },
      "qualityEvidence": {
        "zh-TW": "漏失風險與組裝後故障覆蓋",
        "en": "escape risk and post-assembly fault coverage"
      },
      "failureMode": {
        "zh-TW": "把KGD標籤當成終身無故障保證",
        "en": "treating KGD as a lifetime defect-free guarantee"
      },
      "prerequisiteIds": [
        "C10"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "interposer",
      "sourceIds": [
        "ieee-test",
        "advantest-ate"
      ],
      "sourceUrls": [
        "https://cmte.ieee.org/eps-test/wp-content/uploads/sites/132/2022/01/IEEE_EPS_Test_Het_Int_Product_Testability_BKM_Final_v1_0-1-14-22-1.pdf",
        "https://www.advantest.com/en/semiconductor-basics/automated-test-equipment/"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "C12",
      "catalogueOrder": 12,
      "branchId": "common",
      "branchOrder": 12,
      "activityType": "design",
      "title": {
        "zh-TW": "比較良率、重工與測試成本",
        "en": "Compare yield and test-cost scenarios"
      },
      "summary": {
        "zh-TW": "以晶粒良率、模組數與測試估計為起點，比較中途測試與一次整合的成本風險。交付具敏感度的成本情境表，以假設來源與結果範圍判讀結果；重點辨識把獨立缺陷假設當成量產事實。",
        "en": "Start with die yield, module counts and test estimates; compare intermediate test and late-integration risk to obtain cost scenarios with sensitivity analysis. Assess the result using assumption provenance and outcome ranges, with particular attention to assuming independent defects without evidence."
      },
      "input": {
        "zh-TW": "晶粒良率、模組數與測試估計",
        "en": "die yield, module counts and test estimates"
      },
      "operation": {
        "zh-TW": "比較中途測試與一次整合的成本風險",
        "en": "compare intermediate test and late-integration risk"
      },
      "output": {
        "zh-TW": "具敏感度的成本情境表",
        "en": "cost scenarios with sensitivity analysis"
      },
      "qualityEvidence": {
        "zh-TW": "假設來源與結果範圍",
        "en": "assumption provenance and outcome ranges"
      },
      "failureMode": {
        "zh-TW": "把獨立缺陷假設當成量產事實",
        "en": "assuming independent defects without evidence"
      },
      "prerequisiteIds": [
        "C11"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "interposer",
      "sourceIds": [
        "amkor-chiplets",
        "ieee-test"
      ],
      "sourceUrls": [
        "https://amkormarcomexternal.blob.core.windows.net/amkordotcom/wp-content/uploads/2024/03/Readying-the-supply-chain-for-chiplets-and-heterogeneous-integration_EN.pdf",
        "https://cmte.ieee.org/eps-test/wp-content/uploads/sites/132/2022/01/IEEE_EPS_Test_Het_Int_Product_Testability_BKM_Final_v1_0-1-14-22-1.pdf"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "C13",
      "catalogueOrder": 13,
      "branchId": "common",
      "branchOrder": 13,
      "activityType": "design",
      "title": {
        "zh-TW": "審查材料與製程相容性",
        "en": "Review materials and process compatibility"
      },
      "summary": {
        "zh-TW": "以介電層、黏著劑與金屬材料資料為起點，檢查熱預算、附著與後續製程限制。交付材料相容性矩陣，以供應商資料與試片結果判讀結果；重點辨識前段材料無法承受後續熱處理。",
        "en": "Start with dielectric, adhesive and metallization data; review thermal budget, adhesion and downstream compatibility to obtain a materials-compatibility matrix. Assess the result using supplier data and coupon results, with particular attention to materials that cannot survive later thermal steps."
      },
      "input": {
        "zh-TW": "介電層、黏著劑與金屬材料資料",
        "en": "dielectric, adhesive and metallization data"
      },
      "operation": {
        "zh-TW": "檢查熱預算、附著與後續製程限制",
        "en": "review thermal budget, adhesion and downstream compatibility"
      },
      "output": {
        "zh-TW": "材料相容性矩陣",
        "en": "a materials-compatibility matrix"
      },
      "qualityEvidence": {
        "zh-TW": "供應商資料與試片結果",
        "en": "supplier data and coupon results"
      },
      "failureMode": {
        "zh-TW": "前段材料無法承受後續熱處理",
        "en": "materials that cannot survive later thermal steps"
      },
      "prerequisiteIds": [
        "C12"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "interposer",
      "sourceIds": [
        "ase-thermal",
        "evg-d2w"
      ],
      "sourceUrls": [
        "https://ase.aseglobal.com/lab-services/stress-and-thermal-lab/",
        "https://www.evgroup.com/fileadmin/media/products/bonding/Die_to_Wafer_bonding_systems/White_Paper_D2W_Bonding.pdf"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "C14",
      "catalogueOrder": 14,
      "branchId": "common",
      "branchOrder": 14,
      "activityType": "design",
      "title": {
        "zh-TW": "完成封裝設計規則檢查",
        "en": "Complete package design-rule checks"
      },
      "summary": {
        "zh-TW": "以版圖、層疊與供應商規則為起點，核對線寬、間距、孔與邊界條件。交付有簽核記錄的設計資料，以DRC、網表對照與例外清單判讀結果；重點辨識將教學圖直接當作可製造版圖。",
        "en": "Start with layout, stack-up and supplier rules; check lines, spacing, vias and keep-outs to obtain signed-off design data. Assess the result using DRC, connectivity comparison and waivers, with particular attention to using a teaching drawing as manufacturing artwork."
      },
      "input": {
        "zh-TW": "版圖、層疊與供應商規則",
        "en": "layout, stack-up and supplier rules"
      },
      "operation": {
        "zh-TW": "核對線寬、間距、孔與邊界條件",
        "en": "check lines, spacing, vias and keep-outs"
      },
      "output": {
        "zh-TW": "有簽核記錄的設計資料",
        "en": "signed-off design data"
      },
      "qualityEvidence": {
        "zh-TW": "DRC、網表對照與例外清單",
        "en": "DRC, connectivity comparison and waivers"
      },
      "failureMode": {
        "zh-TW": "將教學圖直接當作可製造版圖",
        "en": "using a teaching drawing as manufacturing artwork"
      },
      "prerequisiteIds": [
        "C13"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "interposer",
      "sourceIds": [
        "cadence-integrity",
        "intel-design-flow"
      ],
      "sourceUrls": [
        "https://www.cadence.com/content/dam/cadence-www/global/en_US/documents/tools/digital-design-signoff/Integrity-3D-IC-DS-v1.pdf",
        "https://blogs.sw.siemens.com/semiconductor-packaging/2024/08/12/user2user-2024-emib-based-advanced-packaging-flow-intel-foundry/"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "C15",
      "catalogueOrder": 15,
      "branchId": "common",
      "branchOrder": 15,
      "activityType": "design",
      "title": {
        "zh-TW": "制定量測與抽樣控制計畫",
        "en": "Define metrology and sampling controls"
      },
      "summary": {
        "zh-TW": "以關鍵尺寸與失效風險清單為起點，選擇量測點、取樣頻率與升級規則。交付各站點的證據與處置要求，以量測能力與重複性評估判讀結果；重點辨識量測工具解析度不足卻判定合格。",
        "en": "Start with critical dimensions and failure risks; select measurement sites, sampling and escalation rules to obtain station-specific evidence and disposition rules. Assess the result using measurement capability and repeatability, with particular attention to acceptance using insufficient measurement resolution."
      },
      "input": {
        "zh-TW": "關鍵尺寸與失效風險清單",
        "en": "critical dimensions and failure risks"
      },
      "operation": {
        "zh-TW": "選擇量測點、取樣頻率與升級規則",
        "en": "select measurement sites, sampling and escalation rules"
      },
      "output": {
        "zh-TW": "各站點的證據與處置要求",
        "en": "station-specific evidence and disposition rules"
      },
      "qualityEvidence": {
        "zh-TW": "量測能力與重複性評估",
        "en": "measurement capability and repeatability"
      },
      "failureMode": {
        "zh-TW": "量測工具解析度不足卻判定合格",
        "en": "acceptance using insufficient measurement resolution"
      },
      "prerequisiteIds": [
        "C14"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "interposer",
      "sourceIds": [
        "kla-metrology",
        "bruker-bond"
      ],
      "sourceUrls": [
        "https://ask.kla-tencor.com/products/packaging-manufacturing/wafer-inspection-and-metrology-for-advanced-packaging",
        "https://www.bruker.com/en/products-and-solutions/semiconductor-solutions/automated-afm-and-cipt-systems/resource-library/an-5001-surface-metrology-for-hybrid-bonding-in-advanced-semiconductor-packaging.html"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "C16",
      "catalogueOrder": 16,
      "branchId": "common",
      "branchOrder": 16,
      "activityType": "design",
      "title": {
        "zh-TW": "建立批次與晶粒座標追溯",
        "en": "Establish lot and die-coordinate traceability"
      },
      "summary": {
        "zh-TW": "以晶圓ID、晶粒圖與路線版本為起點，連接來料、加工、檢測與模組序號。交付可查詢的製造履歷，以抽查座標轉換與批次連結判讀結果；重點辨識晶粒座標與測試資料錯配。",
        "en": "Start with wafer IDs, die maps and route versions; link incoming lots, operations, tests and module IDs to obtain a queryable manufacturing genealogy. Assess the result using coordinate-transform and lot-link audits, with particular attention to mismatched die coordinates and test records."
      },
      "input": {
        "zh-TW": "晶圓ID、晶粒圖與路線版本",
        "en": "wafer IDs, die maps and route versions"
      },
      "operation": {
        "zh-TW": "連接來料、加工、檢測與模組序號",
        "en": "link incoming lots, operations, tests and module IDs"
      },
      "output": {
        "zh-TW": "可查詢的製造履歷",
        "en": "a queryable manufacturing genealogy"
      },
      "qualityEvidence": {
        "zh-TW": "抽查座標轉換與批次連結",
        "en": "coordinate-transform and lot-link audits"
      },
      "failureMode": {
        "zh-TW": "晶粒座標與測試資料錯配",
        "en": "mismatched die coordinates and test records"
      },
      "prerequisiteIds": [
        "C15"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "interposer",
      "sourceIds": [
        "kla-metrology",
        "amkor-test"
      ],
      "sourceUrls": [
        "https://ask.kla-tencor.com/products/packaging-manufacturing/wafer-inspection-and-metrology-for-advanced-packaging",
        "https://amkor.com/test-services/"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "C17",
      "catalogueOrder": 17,
      "branchId": "common",
      "branchOrder": 17,
      "activityType": "inspection_test",
      "title": {
        "zh-TW": "檢驗來料晶圓身分與表面",
        "en": "Inspect incoming wafer identity and surfaces"
      },
      "summary": {
        "zh-TW": "以待投產晶圓與供應證明為起點，核對標記並掃描刮傷與顆粒。交付隔離異常的來料檢驗表，以正背面影像與缺陷座標判讀結果；重點辨識混料或顆粒帶入關鍵接合站。",
        "en": "Start with incoming wafers and supplier records; verify markings and screen scratches or particles to obtain an incoming inspection record with quarantines. Assess the result using front/back images and defect coordinates, with particular attention to mixed lots or particles entering bonding."
      },
      "input": {
        "zh-TW": "待投產晶圓與供應證明",
        "en": "incoming wafers and supplier records"
      },
      "operation": {
        "zh-TW": "核對標記並掃描刮傷與顆粒",
        "en": "verify markings and screen scratches or particles"
      },
      "output": {
        "zh-TW": "隔離異常的來料檢驗表",
        "en": "an incoming inspection record with quarantines"
      },
      "qualityEvidence": {
        "zh-TW": "正背面影像與缺陷座標",
        "en": "front/back images and defect coordinates"
      },
      "failureMode": {
        "zh-TW": "混料或顆粒帶入關鍵接合站",
        "en": "mixed lots or particles entering bonding"
      },
      "prerequisiteIds": [
        "C16"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "interposer",
      "sourceIds": [
        "kla-metrology",
        "ase-fa"
      ],
      "sourceUrls": [
        "https://ask.kla-tencor.com/products/packaging-manufacturing/wafer-inspection-and-metrology-for-advanced-packaging",
        "https://ase.aseglobal.com/lab-services/failure-analysis-lab/"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "C18",
      "catalogueOrder": 18,
      "branchId": "common",
      "branchOrder": 18,
      "activityType": "inspection_test",
      "title": {
        "zh-TW": "量測來料厚度、平坦度與翹曲",
        "en": "Measure incoming thickness and wafer shape"
      },
      "summary": {
        "zh-TW": "以通過身分檢查的晶圓為起點，建立厚度、弓形與翹曲地圖。交付機台搬運與加工適用性資料，以全片量測圖與校正紀錄判讀結果；重點辨識只量中心而漏掉邊緣變形。",
        "en": "Start with identity-verified wafers; map thickness, bow and warpage to obtain handling and process-compatibility data. Assess the result using full-wafer maps and calibration records, with particular attention to center-only measurement missing edge deformation."
      },
      "input": {
        "zh-TW": "通過身分檢查的晶圓",
        "en": "identity-verified wafers"
      },
      "operation": {
        "zh-TW": "建立厚度、弓形與翹曲地圖",
        "en": "map thickness, bow and warpage"
      },
      "output": {
        "zh-TW": "機台搬運與加工適用性資料",
        "en": "handling and process-compatibility data"
      },
      "qualityEvidence": {
        "zh-TW": "全片量測圖與校正紀錄",
        "en": "full-wafer maps and calibration records"
      },
      "failureMode": {
        "zh-TW": "只量中心而漏掉邊緣變形",
        "en": "center-only measurement missing edge deformation"
      },
      "prerequisiteIds": [
        "C17"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "interposer",
      "sourceIds": [
        "kla-metrology",
        "disco-taiko"
      ],
      "sourceUrls": [
        "https://ask.kla-tencor.com/products/packaging-manufacturing/wafer-inspection-and-metrology-for-advanced-packaging",
        "https://www-hq.disco.co.jp/eg/solution/library/grinder/taiko_process.html"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "C19",
      "catalogueOrder": 19,
      "branchId": "common",
      "branchOrder": 19,
      "activityType": "inspection_test",
      "title": {
        "zh-TW": "執行晶圓電測與晶粒分選",
        "en": "Probe wafers and bin dies"
      },
      "summary": {
        "zh-TW": "以晶圓與核准測試程式為起點，量測電性並輸出可用晶粒座標。交付具測試版本的晶粒分選圖，以重測一致性與失效分布判讀結果；重點辨識接觸不良被誤判為晶粒失效。",
        "en": "Start with wafers and approved test programs; measure electrical behavior and map usable dies to obtain a die-bin map with test-program revision. Assess the result using retest consistency and failure distribution, with particular attention to probe-contact faults misclassified as die defects."
      },
      "input": {
        "zh-TW": "晶圓與核准測試程式",
        "en": "wafers and approved test programs"
      },
      "operation": {
        "zh-TW": "量測電性並輸出可用晶粒座標",
        "en": "measure electrical behavior and map usable dies"
      },
      "output": {
        "zh-TW": "具測試版本的晶粒分選圖",
        "en": "a die-bin map with test-program revision"
      },
      "qualityEvidence": {
        "zh-TW": "重測一致性與失效分布",
        "en": "retest consistency and failure distribution"
      },
      "failureMode": {
        "zh-TW": "接觸不良被誤判為晶粒失效",
        "en": "probe-contact faults misclassified as die defects"
      },
      "prerequisiteIds": [
        "C18"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "interposer",
      "sourceIds": [
        "advantest-ate",
        "amkor-test"
      ],
      "sourceUrls": [
        "https://www.advantest.com/en/semiconductor-basics/automated-test-equipment/",
        "https://amkor.com/test-services/"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "C20",
      "catalogueOrder": 20,
      "branchId": "common",
      "branchOrder": 20,
      "activityType": "design",
      "title": {
        "zh-TW": "放行指定架構的製程路線",
        "en": "Release the selected architecture route"
      },
      "summary": {
        "zh-TW": "以設計簽核、來料與晶粒圖為起點，確認分支、關卡及不適用步驟。交付具適用條件的教學流程卡，以需求、材料與路線版本交叉檢查判讀結果；重點辨識把分支目錄誤作同批料的單一路線。",
        "en": "Start with design sign-off, incoming records and die maps; confirm the branch, gates and inapplicable operations to obtain a route card with applicability conditions. Assess the result using cross-check of requirements, materials and revisions, with particular attention to mistaking the catalogue for one lot traveler."
      },
      "input": {
        "zh-TW": "設計簽核、來料與晶粒圖",
        "en": "design sign-off, incoming records and die maps"
      },
      "operation": {
        "zh-TW": "確認分支、關卡及不適用步驟",
        "en": "confirm the branch, gates and inapplicable operations"
      },
      "output": {
        "zh-TW": "具適用條件的教學流程卡",
        "en": "a route card with applicability conditions"
      },
      "qualityEvidence": {
        "zh-TW": "需求、材料與路線版本交叉檢查",
        "en": "cross-check of requirements, materials and revisions"
      },
      "failureMode": {
        "zh-TW": "把分支目錄誤作同批料的單一路線",
        "en": "mistaking the catalogue for one lot traveler"
      },
      "prerequisiteIds": [
        "C19"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "interposer",
      "sourceIds": [
        "amkor-chiplets",
        "intel-packaging"
      ],
      "sourceUrls": [
        "https://amkormarcomexternal.blob.core.windows.net/amkordotcom/wp-content/uploads/2024/03/Readying-the-supply-chain-for-chiplets-and-heterogeneous-integration_EN.pdf",
        "https://www.intel.com/content/www/us/en/foundry/packaging.htm"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "I01",
      "catalogueOrder": 21,
      "branchId": "interposer",
      "branchOrder": 1,
      "activityType": "inspection_test",
      "title": {
        "zh-TW": "核對已製成盲孔TSV的中介層",
        "en": "Verify incoming blind-TSV interposers"
      },
      "summary": {
        "zh-TW": "以已含TSV的代工晶圓與測試資料為起點，確認TSV方向、深度資料與正面保護需求。交付可進行背面加工的中介層批次，以來料結構文件與電測紀錄判讀結果；重點辨識誤認後段封裝廠會補做全部TSV。",
        "en": "Start with foundry wafers with preformed TSVs and test data; review TSV orientation, depth data and frontside protection to obtain interposers released for backside processing. Assess the result using incoming structure documentation and electrical records, with particular attention to assuming backend assembly forms all incoming TSVs."
      },
      "input": {
        "zh-TW": "已含TSV的代工晶圓與測試資料",
        "en": "foundry wafers with preformed TSVs and test data"
      },
      "operation": {
        "zh-TW": "確認TSV方向、深度資料與正面保護需求",
        "en": "review TSV orientation, depth data and frontside protection"
      },
      "output": {
        "zh-TW": "可進行背面加工的中介層批次",
        "en": "interposers released for backside processing"
      },
      "qualityEvidence": {
        "zh-TW": "來料結構文件與電測紀錄",
        "en": "incoming structure documentation and electrical records"
      },
      "failureMode": {
        "zh-TW": "誤認後段封裝廠會補做全部TSV",
        "en": "assuming backend assembly forms all incoming TSVs"
      },
      "prerequisiteIds": [
        "C20"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "interposer",
      "sourceIds": [
        "amkor-tsv"
      ],
      "sourceUrls": [
        "https://amkor.com/technology/25d-3d-tsv/"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "本分支不包含代工廠製作盲孔TSV，也不包含HBM內部DRAM製程。",
        "en": "Foundry formation of the incoming blind TSVs and internal HBM DRAM fabrication are outside this branch."
      }
    },
    {
      "id": "I02",
      "catalogueOrder": 22,
      "branchId": "interposer",
      "branchOrder": 2,
      "activityType": "manufacturing",
      "title": {
        "zh-TW": "貼合薄晶圓暫時支撐載板",
        "en": "Bond a temporary thin-wafer support"
      },
      "summary": {
        "zh-TW": "以中介層晶圓、載板與核准黏著系統為起點，保護正面並完成暫時載板貼合。交付具機械支撐的加工晶圓，以貼合空洞與厚度均勻性判讀結果；重點辨識載板空洞造成研磨時局部破片。",
        "en": "Start with interposer wafer, carrier and qualified adhesive; protect the frontside and bond temporary support to obtain a mechanically supported wafer. Assess the result using bond-void and thickness-uniformity checks, with particular attention to carrier voids causing local breakage during grinding."
      },
      "input": {
        "zh-TW": "中介層晶圓、載板與核准黏著系統",
        "en": "interposer wafer, carrier and qualified adhesive"
      },
      "operation": {
        "zh-TW": "保護正面並完成暫時載板貼合",
        "en": "protect the frontside and bond temporary support"
      },
      "output": {
        "zh-TW": "具機械支撐的加工晶圓",
        "en": "a mechanically supported wafer"
      },
      "qualityEvidence": {
        "zh-TW": "貼合空洞與厚度均勻性",
        "en": "bond-void and thickness-uniformity checks"
      },
      "failureMode": {
        "zh-TW": "載板空洞造成研磨時局部破片",
        "en": "carrier voids causing local breakage during grinding"
      },
      "prerequisiteIds": [
        "I01"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "interposer",
      "sourceIds": [
        "amkor-tsv",
        "evg-process"
      ],
      "sourceUrls": [
        "https://amkor.com/technology/25d-3d-tsv/",
        "https://www.evgroup.com/fileadmin/media/company/service/Process_Services_Flyer_24_04.pdf"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "I03",
      "catalogueOrder": 23,
      "branchId": "interposer",
      "branchOrder": 3,
      "activityType": "manufacturing",
      "title": {
        "zh-TW": "背面粗研磨移除主要矽厚度",
        "en": "Coarse-grind the interposer backside"
      },
      "summary": {
        "zh-TW": "以暫時支撐的中介層晶圓為起點，按核准目標移除大部分背面矽。交付保留精修餘量的薄化晶圓，以厚度地圖與研磨負載記錄判讀結果；重點辨識過磨導致TSV或正面結構受損。",
        "en": "Start with carrier-supported interposer wafer; remove bulk backside silicon toward the qualified target to obtain a thinned wafer with finishing allowance. Assess the result using thickness maps and grinding-load records, with particular attention to over-grinding that damages TSVs or frontside structures."
      },
      "input": {
        "zh-TW": "暫時支撐的中介層晶圓",
        "en": "carrier-supported interposer wafer"
      },
      "operation": {
        "zh-TW": "按核准目標移除大部分背面矽",
        "en": "remove bulk backside silicon toward the qualified target"
      },
      "output": {
        "zh-TW": "保留精修餘量的薄化晶圓",
        "en": "a thinned wafer with finishing allowance"
      },
      "qualityEvidence": {
        "zh-TW": "厚度地圖與研磨負載記錄",
        "en": "thickness maps and grinding-load records"
      },
      "failureMode": {
        "zh-TW": "過磨導致TSV或正面結構受損",
        "en": "over-grinding that damages TSVs or frontside structures"
      },
      "prerequisiteIds": [
        "I02"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "interposer",
      "sourceIds": [
        "amkor-tsv",
        "disco-solutions"
      ],
      "sourceUrls": [
        "https://amkor.com/technology/25d-3d-tsv/",
        "https://www.disco.co.jp/eg/solution/"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "I04",
      "catalogueOrder": 24,
      "branchId": "interposer",
      "branchOrder": 4,
      "activityType": "manufacturing",
      "title": {
        "zh-TW": "精研磨與損傷層移除",
        "en": "Finish thinning and relieve grinding damage"
      },
      "summary": {
        "zh-TW": "以粗磨後晶圓與剩餘厚度資料為起點，精修厚度並移除研磨損傷。交付適合後續TSV露出的背面，以厚度均勻性、表面與強度試片判讀結果；重點辨識殘留微裂紋在後段擴展。",
        "en": "Start with coarse-ground wafer and remaining-thickness data; finish thickness and remove grinding damage to obtain a backside ready for controlled TSV reveal. Assess the result using uniformity, surface and strength-coupon evidence, with particular attention to residual microcracks propagating downstream."
      },
      "input": {
        "zh-TW": "粗磨後晶圓與剩餘厚度資料",
        "en": "coarse-ground wafer and remaining-thickness data"
      },
      "operation": {
        "zh-TW": "精修厚度並移除研磨損傷",
        "en": "finish thickness and remove grinding damage"
      },
      "output": {
        "zh-TW": "適合後續TSV露出的背面",
        "en": "a backside ready for controlled TSV reveal"
      },
      "qualityEvidence": {
        "zh-TW": "厚度均勻性、表面與強度試片",
        "en": "uniformity, surface and strength-coupon evidence"
      },
      "failureMode": {
        "zh-TW": "殘留微裂紋在後段擴展",
        "en": "residual microcracks propagating downstream"
      },
      "prerequisiteIds": [
        "I03"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "interposer",
      "sourceIds": [
        "disco-solutions",
        "amkor-tsv"
      ],
      "sourceUrls": [
        "https://www.disco.co.jp/eg/solution/",
        "https://amkor.com/technology/25d-3d-tsv/"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "I05",
      "catalogueOrder": 25,
      "branchId": "interposer",
      "branchOrder": 5,
      "activityType": "manufacturing",
      "title": {
        "zh-TW": "選擇性露出TSV端點",
        "en": "Reveal TSV ends selectively"
      },
      "summary": {
        "zh-TW": "以已薄化但尚未完全露出的TSV晶圓為起點，以核准選擇性移除步驟露出端點。交付露出高度受控的TSV表面，以端點高度與矽殘留檢查判讀結果；重點辨識露出不足或過度侵蝕。",
        "en": "Start with thinned wafers with buried TSV ends; use qualified selective removal to expose via ends to obtain TSV ends with controlled reveal height. Assess the result using via-height and residual-silicon checks, with particular attention to incomplete reveal or excessive erosion."
      },
      "input": {
        "zh-TW": "已薄化但尚未完全露出的TSV晶圓",
        "en": "thinned wafers with buried TSV ends"
      },
      "operation": {
        "zh-TW": "以核准選擇性移除步驟露出端點",
        "en": "use qualified selective removal to expose via ends"
      },
      "output": {
        "zh-TW": "露出高度受控的TSV表面",
        "en": "TSV ends with controlled reveal height"
      },
      "qualityEvidence": {
        "zh-TW": "端點高度與矽殘留檢查",
        "en": "via-height and residual-silicon checks"
      },
      "failureMode": {
        "zh-TW": "露出不足或過度侵蝕",
        "en": "incomplete reveal or excessive erosion"
      },
      "prerequisiteIds": [
        "I04"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "interposer",
      "sourceIds": [
        "amkor-tsv",
        "lam-etch"
      ],
      "sourceUrls": [
        "https://amkor.com/technology/25d-3d-tsv/",
        "https://www.lamresearch.com/product/dsie-product-family/"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "I06",
      "catalogueOrder": 26,
      "branchId": "interposer",
      "branchOrder": 6,
      "activityType": "manufacturing",
      "title": {
        "zh-TW": "形成背面絕緣鈍化層",
        "en": "Deposit backside passivation"
      },
      "summary": {
        "zh-TW": "以露出TSV的晶圓背面為起點，覆蓋絕緣介電層並保護矽表面。交付受保護且可再開孔的背面，以膜厚、覆蓋性與缺陷檢查判讀結果；重點辨識薄膜針孔造成漏電。",
        "en": "Start with a backside with exposed TSVs; deposit an insulating film over the silicon surface to obtain a passivated backside ready for contact opening. Assess the result using film thickness, coverage and defect checks, with particular attention to passivation pinholes causing leakage."
      },
      "input": {
        "zh-TW": "露出TSV的晶圓背面",
        "en": "a backside with exposed TSVs"
      },
      "operation": {
        "zh-TW": "覆蓋絕緣介電層並保護矽表面",
        "en": "deposit an insulating film over the silicon surface"
      },
      "output": {
        "zh-TW": "受保護且可再開孔的背面",
        "en": "a passivated backside ready for contact opening"
      },
      "qualityEvidence": {
        "zh-TW": "膜厚、覆蓋性與缺陷檢查",
        "en": "film thickness, coverage and defect checks"
      },
      "failureMode": {
        "zh-TW": "薄膜針孔造成漏電",
        "en": "passivation pinholes causing leakage"
      },
      "prerequisiteIds": [
        "I05"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "interposer",
      "sourceIds": [
        "amkor-tsv",
        "kla-deposition"
      ],
      "sourceUrls": [
        "https://amkor.com/technology/25d-3d-tsv/",
        "https://www.spts.com/products/packaging-manufacturing/wafer-processing-systems-for-advanced-packaging"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "I07",
      "catalogueOrder": 27,
      "branchId": "interposer",
      "branchOrder": 7,
      "activityType": "manufacturing",
      "title": {
        "zh-TW": "平坦化鈍化層並開出TSV接觸",
        "en": "Planarize passivation and open TSV contacts"
      },
      "summary": {
        "zh-TW": "以已鈍化的TSV背面為起點，控制平坦化與接觸開口。交付可金屬化的TSV端面，以殘膜與端面高度量測判讀結果；重點辨識接點殘膜造成高阻抗。",
        "en": "Start with passivated TSV backside; control planarization and contact opening to obtain accessible TSV surfaces for metallization. Assess the result using residual-film and contact-height measurements, with particular attention to residual dielectric causing resistive contacts."
      },
      "input": {
        "zh-TW": "已鈍化的TSV背面",
        "en": "passivated TSV backside"
      },
      "operation": {
        "zh-TW": "控制平坦化與接觸開口",
        "en": "control planarization and contact opening"
      },
      "output": {
        "zh-TW": "可金屬化的TSV端面",
        "en": "accessible TSV surfaces for metallization"
      },
      "qualityEvidence": {
        "zh-TW": "殘膜與端面高度量測",
        "en": "residual-film and contact-height measurements"
      },
      "failureMode": {
        "zh-TW": "接點殘膜造成高阻抗",
        "en": "residual dielectric causing resistive contacts"
      },
      "prerequisiteIds": [
        "I06"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "interposer",
      "sourceIds": [
        "amkor-tsv",
        "kla-metrology"
      ],
      "sourceUrls": [
        "https://amkor.com/technology/25d-3d-tsv/",
        "https://ask.kla-tencor.com/products/packaging-manufacturing/wafer-inspection-and-metrology-for-advanced-packaging"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "I08",
      "catalogueOrder": 28,
      "branchId": "interposer",
      "branchOrder": 8,
      "activityType": "manufacturing",
      "title": {
        "zh-TW": "沉積背面阻障與種子層",
        "en": "Deposit backside barrier and seed layers"
      },
      "summary": {
        "zh-TW": "以已開口的背面接觸區為起點，建立後續電鍍所需的連續金屬基底。交付可導電的背面種子層，以片電阻與階差覆蓋檢查判讀結果；重點辨識種子層中斷造成電鍍缺口。",
        "en": "Start with opened backside contacts; form continuous films for later electroplating to obtain a conductive backside seed layer. Assess the result using sheet resistance and step-coverage checks, with particular attention to seed discontinuity causing plating gaps."
      },
      "input": {
        "zh-TW": "已開口的背面接觸區",
        "en": "opened backside contacts"
      },
      "operation": {
        "zh-TW": "建立後續電鍍所需的連續金屬基底",
        "en": "form continuous films for later electroplating"
      },
      "output": {
        "zh-TW": "可導電的背面種子層",
        "en": "a conductive backside seed layer"
      },
      "qualityEvidence": {
        "zh-TW": "片電阻與階差覆蓋檢查",
        "en": "sheet resistance and step-coverage checks"
      },
      "failureMode": {
        "zh-TW": "種子層中斷造成電鍍缺口",
        "en": "seed discontinuity causing plating gaps"
      },
      "prerequisiteIds": [
        "I07"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "interposer",
      "sourceIds": [
        "lam-flow",
        "amkor-tsv"
      ],
      "sourceUrls": [
        "https://newsroom.lamresearch.com/the-ai-revolution-relies-on-advanced-packaging",
        "https://amkor.com/technology/25d-3d-tsv/"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "I09",
      "catalogueOrder": 29,
      "branchId": "interposer",
      "branchOrder": 9,
      "activityType": "manufacturing",
      "title": {
        "zh-TW": "圖案化背面RDL光阻",
        "en": "Pattern backside RDL resist"
      },
      "summary": {
        "zh-TW": "以種子層晶圓與RDL版圖為起點，塗佈、曝光與顯影形成鍍銅窗口。交付背面RDL電鍍模版，以開口尺寸與TSV套準量測判讀結果；重點辨識偏移的RDL接不到TSV。",
        "en": "Start with seeded wafer and backside routing artwork; coat, expose and develop plating windows to obtain a backside RDL plating mold. Assess the result using opening dimensions and TSV overlay measurements, with particular attention to misregistered routes missing TSV contacts."
      },
      "input": {
        "zh-TW": "種子層晶圓與RDL版圖",
        "en": "seeded wafer and backside routing artwork"
      },
      "operation": {
        "zh-TW": "塗佈、曝光與顯影形成鍍銅窗口",
        "en": "coat, expose and develop plating windows"
      },
      "output": {
        "zh-TW": "背面RDL電鍍模版",
        "en": "a backside RDL plating mold"
      },
      "qualityEvidence": {
        "zh-TW": "開口尺寸與TSV套準量測",
        "en": "opening dimensions and TSV overlay measurements"
      },
      "failureMode": {
        "zh-TW": "偏移的RDL接不到TSV",
        "en": "misregistered routes missing TSV contacts"
      },
      "prerequisiteIds": [
        "I08"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "interposer",
      "sourceIds": [
        "evg-process",
        "kla-metrology"
      ],
      "sourceUrls": [
        "https://www.evgroup.com/fileadmin/media/company/service/Process_Services_Flyer_24_04.pdf",
        "https://ask.kla-tencor.com/products/packaging-manufacturing/wafer-inspection-and-metrology-for-advanced-packaging"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "I10",
      "catalogueOrder": 30,
      "branchId": "interposer",
      "branchOrder": 10,
      "activityType": "manufacturing",
      "title": {
        "zh-TW": "電鍍背面銅重佈線",
        "en": "Electroplate backside copper redistribution"
      },
      "summary": {
        "zh-TW": "以具光阻窗口的種子層為起點，在窗口中形成所需銅連線。交付已成形但待隔離的RDL，以銅厚與局部填充完整性判讀結果；重點辨識厚度不均或鍍層空洞。",
        "en": "Start with seed layer with patterned resist windows; deposit copper routing inside the windows to obtain formed RDL awaiting electrical isolation. Assess the result using copper thickness and local fill integrity, with particular attention to nonuniform thickness or plated voids."
      },
      "input": {
        "zh-TW": "具光阻窗口的種子層",
        "en": "seed layer with patterned resist windows"
      },
      "operation": {
        "zh-TW": "在窗口中形成所需銅連線",
        "en": "deposit copper routing inside the windows"
      },
      "output": {
        "zh-TW": "已成形但待隔離的RDL",
        "en": "formed RDL awaiting electrical isolation"
      },
      "qualityEvidence": {
        "zh-TW": "銅厚與局部填充完整性",
        "en": "copper thickness and local fill integrity"
      },
      "failureMode": {
        "zh-TW": "厚度不均或鍍層空洞",
        "en": "nonuniform thickness or plated voids"
      },
      "prerequisiteIds": [
        "I09"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "interposer",
      "sourceIds": [
        "lam-electrofill",
        "amkor-tsv"
      ],
      "sourceUrls": [
        "https://www.lamresearch.com/product/sabre-3d/",
        "https://amkor.com/technology/25d-3d-tsv/"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "I11",
      "catalogueOrder": 31,
      "branchId": "interposer",
      "branchOrder": 11,
      "activityType": "manufacturing",
      "title": {
        "zh-TW": "去除RDL光阻與多餘種子層",
        "en": "Remove RDL resist and excess seed"
      },
      "summary": {
        "zh-TW": "以已電鍍的背面RDL為起點，剝除光阻並隔離各條金屬線。交付彼此絕緣的銅走線，以殘留、線寬損失與短路檢查判讀結果；重點辨識殘餘種子層橋接相鄰走線。",
        "en": "Start with electroplated backside routing; strip resist and isolate individual routes to obtain electrically isolated copper routes. Assess the result using residue, line-loss and short checks, with particular attention to residual seed bridging adjacent traces."
      },
      "input": {
        "zh-TW": "已電鍍的背面RDL",
        "en": "electroplated backside routing"
      },
      "operation": {
        "zh-TW": "剝除光阻並隔離各條金屬線",
        "en": "strip resist and isolate individual routes"
      },
      "output": {
        "zh-TW": "彼此絕緣的銅走線",
        "en": "electrically isolated copper routes"
      },
      "qualityEvidence": {
        "zh-TW": "殘留、線寬損失與短路檢查",
        "en": "residue, line-loss and short checks"
      },
      "failureMode": {
        "zh-TW": "殘餘種子層橋接相鄰走線",
        "en": "residual seed bridging adjacent traces"
      },
      "prerequisiteIds": [
        "I10"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "interposer",
      "sourceIds": [
        "lam-flow",
        "kla-metrology"
      ],
      "sourceUrls": [
        "https://newsroom.lamresearch.com/the-ai-revolution-relies-on-advanced-packaging",
        "https://ask.kla-tencor.com/products/packaging-manufacturing/wafer-inspection-and-metrology-for-advanced-packaging"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "I12",
      "catalogueOrder": 32,
      "branchId": "interposer",
      "branchOrder": 12,
      "activityType": "manufacturing",
      "title": {
        "zh-TW": "形成中介層外部接合端點",
        "en": "Form interposer backside joining terminals"
      },
      "summary": {
        "zh-TW": "以已隔離RDL與端點金屬規格為起點，製作選定的UBM與凸塊結構。交付可接到基板的中介層端點，以端點材料、形貌與連通性判讀結果；重點辨識潤濕不良或接點高度不齊。",
        "en": "Start with isolated RDL and terminal metallurgy requirements; form the selected UBM and bump structure to obtain interposer terminals for substrate connection. Assess the result using terminal metallurgy, shape and continuity, with particular attention to poor wetting or uneven terminal height."
      },
      "input": {
        "zh-TW": "已隔離RDL與端點金屬規格",
        "en": "isolated RDL and terminal metallurgy requirements"
      },
      "operation": {
        "zh-TW": "製作選定的UBM與凸塊結構",
        "en": "form the selected UBM and bump structure"
      },
      "output": {
        "zh-TW": "可接到基板的中介層端點",
        "en": "interposer terminals for substrate connection"
      },
      "qualityEvidence": {
        "zh-TW": "端點材料、形貌與連通性",
        "en": "terminal metallurgy, shape and continuity"
      },
      "failureMode": {
        "zh-TW": "潤濕不良或接點高度不齊",
        "en": "poor wetting or uneven terminal height"
      },
      "prerequisiteIds": [
        "I11"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "interposer",
      "sourceIds": [
        "amkor-bumping",
        "amkor-tsv-sheet"
      ],
      "sourceUrls": [
        "https://amkor.com/services/wafer-bumping/",
        "https://amkor.com/kr/wp-content/uploads/2018/02/TSV_TS107.pdf"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "I13",
      "catalogueOrder": 33,
      "branchId": "interposer",
      "branchOrder": 13,
      "activityType": "inspection_test",
      "title": {
        "zh-TW": "量測背面凸塊與共面度",
        "en": "Measure backside bumps and coplanarity"
      },
      "summary": {
        "zh-TW": "以完成凸塊的中介層晶圓為起點，掃描高度、直徑與缺球缺陷。交付接合前的三維凸塊地圖，以跨晶圓與局部共面度統計判讀結果；重點辨識平均值合格但局部接點過低。",
        "en": "Start with bumped interposer wafers; scan height, diameter and missing terminals to obtain a pre-assembly 3D bump map. Assess the result using wafer-wide and local coplanarity statistics, with particular attention to acceptable averages hiding low individual bumps."
      },
      "input": {
        "zh-TW": "完成凸塊的中介層晶圓",
        "en": "bumped interposer wafers"
      },
      "operation": {
        "zh-TW": "掃描高度、直徑與缺球缺陷",
        "en": "scan height, diameter and missing terminals"
      },
      "output": {
        "zh-TW": "接合前的三維凸塊地圖",
        "en": "a pre-assembly 3D bump map"
      },
      "qualityEvidence": {
        "zh-TW": "跨晶圓與局部共面度統計",
        "en": "wafer-wide and local coplanarity statistics"
      },
      "failureMode": {
        "zh-TW": "平均值合格但局部接點過低",
        "en": "acceptable averages hiding low individual bumps"
      },
      "prerequisiteIds": [
        "I12"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "interposer",
      "sourceIds": [
        "kla-metrology",
        "amkor-bumping"
      ],
      "sourceUrls": [
        "https://ask.kla-tencor.com/products/packaging-manufacturing/wafer-inspection-and-metrology-for-advanced-packaging",
        "https://amkor.com/services/wafer-bumping/"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "I14",
      "catalogueOrder": 34,
      "branchId": "interposer",
      "branchOrder": 14,
      "activityType": "manufacturing",
      "title": {
        "zh-TW": "移除暫時載板與殘膠",
        "en": "Debond the temporary carrier and remove residue"
      },
      "summary": {
        "zh-TW": "以背面完成且可轉移的薄晶圓為起點，依相容路線解鍵合並清除殘膠。交付無載板的可搬運中介層晶圓，以殘膠、顆粒與晶圓完整性判讀結果；重點辨識解鍵合應力造成裂片。",
        "en": "Start with backside-finished wafer ready for transfer; debond and remove adhesive using a compatible route to obtain a transferable interposer wafer without the carrier. Assess the result using residue, particle and wafer-integrity checks, with particular attention to debond stress cracking the wafer."
      },
      "input": {
        "zh-TW": "背面完成且可轉移的薄晶圓",
        "en": "backside-finished wafer ready for transfer"
      },
      "operation": {
        "zh-TW": "依相容路線解鍵合並清除殘膠",
        "en": "debond and remove adhesive using a compatible route"
      },
      "output": {
        "zh-TW": "無載板的可搬運中介層晶圓",
        "en": "a transferable interposer wafer without the carrier"
      },
      "qualityEvidence": {
        "zh-TW": "殘膠、顆粒與晶圓完整性",
        "en": "residue, particle and wafer-integrity checks"
      },
      "failureMode": {
        "zh-TW": "解鍵合應力造成裂片",
        "en": "debond stress cracking the wafer"
      },
      "prerequisiteIds": [
        "I13"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "interposer",
      "sourceIds": [
        "amkor-tsv",
        "evg-d2w"
      ],
      "sourceUrls": [
        "https://amkor.com/technology/25d-3d-tsv/",
        "https://www.evgroup.com/fileadmin/media/products/bonding/Die_to_Wafer_bonding_systems/White_Paper_D2W_Bonding.pdf"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "I15",
      "catalogueOrder": 35,
      "branchId": "interposer",
      "branchOrder": 15,
      "activityType": "inspection_test",
      "title": {
        "zh-TW": "建立中介層貼裝基準與良區圖",
        "en": "Establish interposer placement references"
      },
      "summary": {
        "zh-TW": "以中介層正面、KGD圖與對位標記為起點，檢查接合面並轉換貼裝座標。交付可用中介層區與貼裝座標，以標記位置、表面潔淨與座標驗證判讀結果；重點辨識載板移除後的座標轉換錯誤。",
        "en": "Start with interposer frontside, KGD maps and fiducials; inspect joining surfaces and transform placement coordinates to obtain usable interposer sites and placement coordinates. Assess the result using fiducial, cleanliness and coordinate verification, with particular attention to incorrect coordinates after carrier transfer."
      },
      "input": {
        "zh-TW": "中介層正面、KGD圖與對位標記",
        "en": "interposer frontside, KGD maps and fiducials"
      },
      "operation": {
        "zh-TW": "檢查接合面並轉換貼裝座標",
        "en": "inspect joining surfaces and transform placement coordinates"
      },
      "output": {
        "zh-TW": "可用中介層區與貼裝座標",
        "en": "usable interposer sites and placement coordinates"
      },
      "qualityEvidence": {
        "zh-TW": "標記位置、表面潔淨與座標驗證",
        "en": "fiducial, cleanliness and coordinate verification"
      },
      "failureMode": {
        "zh-TW": "載板移除後的座標轉換錯誤",
        "en": "incorrect coordinates after carrier transfer"
      },
      "prerequisiteIds": [
        "I14"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "interposer",
      "sourceIds": [
        "kla-metrology",
        "besi-tcb"
      ],
      "sourceUrls": [
        "https://ask.kla-tencor.com/products/packaging-manufacturing/wafer-inspection-and-metrology-for-advanced-packaging",
        "https://www.besi.com/products-technology/product-details/productgroup/thermo-compression-bonding/"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "I16",
      "catalogueOrder": 36,
      "branchId": "interposer",
      "branchOrder": 16,
      "activityType": "manufacturing",
      "title": {
        "zh-TW": "貼裝並接合運算晶粒",
        "en": "Place and join the compute die"
      },
      "summary": {
        "zh-TW": "以已放行中介層與運算KGD為起點，對準微凸塊並完成選定熱壓接合。交付已接合的運算晶粒，以貼裝偏移、接合高度與接點電測判讀結果；重點辨識微凸塊偏移或接合不足。",
        "en": "Start with released interposer sites and compute KGD; align microbumps and perform selected thermocompression joining to obtain a joined compute die. Assess the result using placement error, bond height and contact tests, with particular attention to microbump misalignment or incomplete joining."
      },
      "input": {
        "zh-TW": "已放行中介層與運算KGD",
        "en": "released interposer sites and compute KGD"
      },
      "operation": {
        "zh-TW": "對準微凸塊並完成選定熱壓接合",
        "en": "align microbumps and perform selected thermocompression joining"
      },
      "output": {
        "zh-TW": "已接合的運算晶粒",
        "en": "a joined compute die"
      },
      "qualityEvidence": {
        "zh-TW": "貼裝偏移、接合高度與接點電測",
        "en": "placement error, bond height and contact tests"
      },
      "failureMode": {
        "zh-TW": "微凸塊偏移或接合不足",
        "en": "microbump misalignment or incomplete joining"
      },
      "prerequisiteIds": [
        "I15"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "interposer",
      "sourceIds": [
        "besi-tcb",
        "amkor-tsv-sheet"
      ],
      "sourceUrls": [
        "https://www.besi.com/products-technology/product-details/productgroup/thermo-compression-bonding/",
        "https://amkor.com/kr/wp-content/uploads/2018/02/TSV_TS107.pdf"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "I17",
      "catalogueOrder": 37,
      "branchId": "interposer",
      "branchOrder": 17,
      "activityType": "manufacturing",
      "title": {
        "zh-TW": "貼裝並接合已測HBM堆疊",
        "en": "Place and join tested HBM stacks"
      },
      "summary": {
        "zh-TW": "以通過測試的HBM堆疊與中介層為起點，逐顆對位並接合記憶體堆疊。交付運算與HBM整合模組，以堆疊身分、共面度與連通性判讀結果；重點辨識混用堆疊版本或局部未接合。",
        "en": "Start with tested HBM stacks and an interposer; align and join the memory stacks to obtain an integrated compute-and-HBM module. Assess the result using stack identity, coplanarity and continuity, with particular attention to mixed stack revisions or local non-bonds."
      },
      "input": {
        "zh-TW": "通過測試的HBM堆疊與中介層",
        "en": "tested HBM stacks and an interposer"
      },
      "operation": {
        "zh-TW": "逐顆對位並接合記憶體堆疊",
        "en": "align and join the memory stacks"
      },
      "output": {
        "zh-TW": "運算與HBM整合模組",
        "en": "an integrated compute-and-HBM module"
      },
      "qualityEvidence": {
        "zh-TW": "堆疊身分、共面度與連通性",
        "en": "stack identity, coplanarity and continuity"
      },
      "failureMode": {
        "zh-TW": "混用堆疊版本或局部未接合",
        "en": "mixed stack revisions or local non-bonds"
      },
      "prerequisiteIds": [
        "I16"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "interposer",
      "sourceIds": [
        "amkor-tsv-sheet",
        "besi-tcb"
      ],
      "sourceUrls": [
        "https://amkor.com/kr/wp-content/uploads/2018/02/TSV_TS107.pdf",
        "https://www.besi.com/products-technology/product-details/productgroup/thermo-compression-bonding/"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "I18",
      "catalogueOrder": 38,
      "branchId": "interposer",
      "branchOrder": 18,
      "activityType": "manufacturing",
      "title": {
        "zh-TW": "填入並固化晶粒下方底填膠",
        "en": "Dispense and cure die underfill"
      },
      "summary": {
        "zh-TW": "以已接合晶粒與核准底填膠為起點，以毛細流動填滿接點間隙並固化。交付受機械保護的接合區，以填充前緣、空洞與固化紀錄判讀結果；重點辨識空洞集中在狹窄晶粒間隙。",
        "en": "Start with joined dies and qualified underfill; fill joint gaps by capillary flow and cure to obtain mechanically reinforced joint regions. Assess the result using flow-front, void and cure records, with particular attention to voids trapped in narrow die gaps."
      },
      "input": {
        "zh-TW": "已接合晶粒與核准底填膠",
        "en": "joined dies and qualified underfill"
      },
      "operation": {
        "zh-TW": "以毛細流動填滿接點間隙並固化",
        "en": "fill joint gaps by capillary flow and cure"
      },
      "output": {
        "zh-TW": "受機械保護的接合區",
        "en": "mechanically reinforced joint regions"
      },
      "qualityEvidence": {
        "zh-TW": "填充前緣、空洞與固化紀錄",
        "en": "flow-front, void and cure records"
      },
      "failureMode": {
        "zh-TW": "空洞集中在狹窄晶粒間隙",
        "en": "voids trapped in narrow die gaps"
      },
      "prerequisiteIds": [
        "I17"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "interposer",
      "sourceIds": [
        "nordson-underfill",
        "ase-fa"
      ],
      "sourceUrls": [
        "https://www.nordson.com/en/divisions/electronics-solutions/your-process/fluid-types/underfill",
        "https://ase.aseglobal.com/lab-services/failure-analysis-lab/"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "I19",
      "catalogueOrder": 39,
      "branchId": "interposer",
      "branchOrder": 19,
      "activityType": "manufacturing",
      "title": {
        "zh-TW": "切割晶片在晶圓上的模組",
        "en": "Singulate chip-on-wafer modules"
      },
      "summary": {
        "zh-TW": "以已保護的晶片在晶圓上組件為起點，依選定街道切割並維持模組追溯。交付獨立的2.5D模組，以切邊影像與模組座標對照判讀結果；重點辨識切割崩邊延伸至細密走線。",
        "en": "Start with protected chip-on-wafer assemblies; singulate along defined streets while retaining identity to obtain individual 2.5D modules. Assess the result using edge images and module-coordinate correlation, with particular attention to edge chipping reaching fine interconnects."
      },
      "input": {
        "zh-TW": "已保護的晶片在晶圓上組件",
        "en": "protected chip-on-wafer assemblies"
      },
      "operation": {
        "zh-TW": "依選定街道切割並維持模組追溯",
        "en": "singulate along defined streets while retaining identity"
      },
      "output": {
        "zh-TW": "獨立的2.5D模組",
        "en": "individual 2.5D modules"
      },
      "qualityEvidence": {
        "zh-TW": "切邊影像與模組座標對照",
        "en": "edge images and module-coordinate correlation"
      },
      "failureMode": {
        "zh-TW": "切割崩邊延伸至細密走線",
        "en": "edge chipping reaching fine interconnects"
      },
      "prerequisiteIds": [
        "I18"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "interposer",
      "sourceIds": [
        "disco-solutions",
        "amkor-tsv-sheet"
      ],
      "sourceUrls": [
        "https://www.disco.co.jp/eg/solution/",
        "https://amkor.com/kr/wp-content/uploads/2018/02/TSV_TS107.pdf"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "I20",
      "catalogueOrder": 40,
      "branchId": "interposer",
      "branchOrder": 20,
      "activityType": "inspection_test",
      "title": {
        "zh-TW": "放行已知良品2.5D模組",
        "en": "Release known-good 2.5D modules"
      },
      "summary": {
        "zh-TW": "以切割模組與中途測試結構為起點，檢查外觀並測試可存取的互連。交付附限制說明的模組放行資料，以中途測試、外觀與批次履歷判讀結果；重點辨識把可測部分通過當作全功能保證。",
        "en": "Start with singulated modules and accessible test structures; inspect modules and test accessible interconnects to obtain module-release records with coverage limits. Assess the result using intermediate test, inspection and genealogy, with particular attention to mistaking partial test coverage for full functionality."
      },
      "input": {
        "zh-TW": "切割模組與中途測試結構",
        "en": "singulated modules and accessible test structures"
      },
      "operation": {
        "zh-TW": "檢查外觀並測試可存取的互連",
        "en": "inspect modules and test accessible interconnects"
      },
      "output": {
        "zh-TW": "附限制說明的模組放行資料",
        "en": "module-release records with coverage limits"
      },
      "qualityEvidence": {
        "zh-TW": "中途測試、外觀與批次履歷",
        "en": "intermediate test, inspection and genealogy"
      },
      "failureMode": {
        "zh-TW": "把可測部分通過當作全功能保證",
        "en": "mistaking partial test coverage for full functionality"
      },
      "prerequisiteIds": [
        "I19"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "interposer",
      "sourceIds": [
        "amkor-tsv-sheet",
        "ieee-test"
      ],
      "sourceUrls": [
        "https://amkor.com/kr/wp-content/uploads/2018/02/TSV_TS107.pdf",
        "https://cmte.ieee.org/eps-test/wp-content/uploads/sites/132/2022/01/IEEE_EPS_Test_Het_Int_Product_Testability_BKM_Final_v1_0-1-14-22-1.pdf"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "F01",
      "catalogueOrder": 41,
      "branchId": "fanout",
      "branchOrder": 1,
      "activityType": "manufacturing",
      "title": {
        "zh-TW": "準備RDL-first載板與釋放層",
        "en": "Prepare an RDL-first carrier and release layer"
      },
      "summary": {
        "zh-TW": "以載板、釋放材料與路線條件為起點，塗佈可相容後段製程的釋放層。交付可建構RDL的暫時載板，以膜厚、顆粒與附著均勻性判讀結果；重點辨識太早脫離或最後無法解鍵合。",
        "en": "Start with carrier, release material and route requirements; apply a release layer compatible with later processing to obtain a temporary carrier for RDL build-up. Assess the result using thickness, particles and adhesion uniformity, with particular attention to premature release or failed final debond."
      },
      "input": {
        "zh-TW": "載板、釋放材料與路線條件",
        "en": "carrier, release material and route requirements"
      },
      "operation": {
        "zh-TW": "塗佈可相容後段製程的釋放層",
        "en": "apply a release layer compatible with later processing"
      },
      "output": {
        "zh-TW": "可建構RDL的暫時載板",
        "en": "a temporary carrier for RDL build-up"
      },
      "qualityEvidence": {
        "zh-TW": "膜厚、顆粒與附著均勻性",
        "en": "thickness, particles and adhesion uniformity"
      },
      "failureMode": {
        "zh-TW": "太早脫離或最後無法解鍵合",
        "en": "premature release or failed final debond"
      },
      "prerequisiteIds": [
        "C20"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "fanout",
      "sourceIds": [
        "ase-fanout",
        "evg-process"
      ],
      "sourceUrls": [
        "https://ase.aseglobal.com/fan-out-packaging/",
        "https://www.evgroup.com/fileadmin/media/company/service/Process_Services_Flyer_24_04.pdf"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "F02",
      "catalogueOrder": 42,
      "branchId": "fanout",
      "branchOrder": 2,
      "activityType": "manufacturing",
      "title": {
        "zh-TW": "塗佈並固化首層RDL介電膜",
        "en": "Coat and cure the first RDL dielectric"
      },
      "summary": {
        "zh-TW": "以已準備載板與介電材料為起點，形成首層絕緣膜並完成核准固化。交付可圖案化的介電底層，以膜厚、應力與殘留溶劑證據判讀結果；重點辨識膜厚起伏使後續開孔不一致。",
        "en": "Start with prepared carrier and dielectric material; form the first insulating film and apply the qualified cure to obtain a dielectric base for patterning. Assess the result using thickness, stress and solvent-residue evidence, with particular attention to thickness variation causing uneven via opening."
      },
      "input": {
        "zh-TW": "已準備載板與介電材料",
        "en": "prepared carrier and dielectric material"
      },
      "operation": {
        "zh-TW": "形成首層絕緣膜並完成核准固化",
        "en": "form the first insulating film and apply the qualified cure"
      },
      "output": {
        "zh-TW": "可圖案化的介電底層",
        "en": "a dielectric base for patterning"
      },
      "qualityEvidence": {
        "zh-TW": "膜厚、應力與殘留溶劑證據",
        "en": "thickness, stress and solvent-residue evidence"
      },
      "failureMode": {
        "zh-TW": "膜厚起伏使後續開孔不一致",
        "en": "thickness variation causing uneven via opening"
      },
      "prerequisiteIds": [
        "F01"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "fanout",
      "sourceIds": [
        "kla-deposition",
        "evg-process"
      ],
      "sourceUrls": [
        "https://www.spts.com/products/packaging-manufacturing/wafer-processing-systems-for-advanced-packaging",
        "https://www.evgroup.com/fileadmin/media/company/service/Process_Services_Flyer_24_04.pdf"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "F03",
      "catalogueOrder": 43,
      "branchId": "fanout",
      "branchOrder": 3,
      "activityType": "manufacturing",
      "title": {
        "zh-TW": "開出介電層連接窗口",
        "en": "Open dielectric connection windows"
      },
      "summary": {
        "zh-TW": "以介電膜與接點圖案為起點，以相容光刻或蝕刻形成開口。交付露出目標接觸區的窗口，以孔徑、殘膜與位置量測判讀結果；重點辨識孔底殘膜造成高電阻。",
        "en": "Start with dielectric film and contact patterns; form openings by compatible lithography or etching to obtain windows exposing intended contact regions. Assess the result using opening size, residual film and position measurements, with particular attention to residual film at via bottoms causing resistance."
      },
      "input": {
        "zh-TW": "介電膜與接點圖案",
        "en": "dielectric film and contact patterns"
      },
      "operation": {
        "zh-TW": "以相容光刻或蝕刻形成開口",
        "en": "form openings by compatible lithography or etching"
      },
      "output": {
        "zh-TW": "露出目標接觸區的窗口",
        "en": "windows exposing intended contact regions"
      },
      "qualityEvidence": {
        "zh-TW": "孔徑、殘膜與位置量測",
        "en": "opening size, residual film and position measurements"
      },
      "failureMode": {
        "zh-TW": "孔底殘膜造成高電阻",
        "en": "residual film at via bottoms causing resistance"
      },
      "prerequisiteIds": [
        "F02"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "fanout",
      "sourceIds": [
        "kla-deposition",
        "evg-process"
      ],
      "sourceUrls": [
        "https://www.spts.com/products/packaging-manufacturing/wafer-processing-systems-for-advanced-packaging",
        "https://www.evgroup.com/fileadmin/media/company/service/Process_Services_Flyer_24_04.pdf"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "F04",
      "catalogueOrder": 44,
      "branchId": "fanout",
      "branchOrder": 4,
      "activityType": "manufacturing",
      "title": {
        "zh-TW": "建立RDL阻障與銅種子層",
        "en": "Form the RDL barrier and copper seed"
      },
      "summary": {
        "zh-TW": "以已開孔介電層為起點，沉積連續阻障與導電種子膜。交付可進行電鍍的基底，以片電阻及孔側壁覆蓋判讀結果；重點辨識側壁種子層不連續。",
        "en": "Start with a patterned dielectric layer; deposit continuous barrier and conductive seed films to obtain a surface ready for electroplating. Assess the result using sheet resistance and via-sidewall coverage, with particular attention to discontinuous seed on via sidewalls."
      },
      "input": {
        "zh-TW": "已開孔介電層",
        "en": "a patterned dielectric layer"
      },
      "operation": {
        "zh-TW": "沉積連續阻障與導電種子膜",
        "en": "deposit continuous barrier and conductive seed films"
      },
      "output": {
        "zh-TW": "可進行電鍍的基底",
        "en": "a surface ready for electroplating"
      },
      "qualityEvidence": {
        "zh-TW": "片電阻及孔側壁覆蓋",
        "en": "sheet resistance and via-sidewall coverage"
      },
      "failureMode": {
        "zh-TW": "側壁種子層不連續",
        "en": "discontinuous seed on via sidewalls"
      },
      "prerequisiteIds": [
        "F03"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "fanout",
      "sourceIds": [
        "applied-fanout",
        "lam-flow"
      ],
      "sourceUrls": [
        "https://www.appliedmaterials.com/il/en/semiconductor/markets-and-inflections/heterogeneous-integration/fan-out.html",
        "https://newsroom.lamresearch.com/the-ai-revolution-relies-on-advanced-packaging"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "F05",
      "catalogueOrder": 45,
      "branchId": "fanout",
      "branchOrder": 5,
      "activityType": "manufacturing",
      "title": {
        "zh-TW": "塗佈RDL電鍍光阻",
        "en": "Coat the RDL plating resist"
      },
      "summary": {
        "zh-TW": "以帶種子層的載板為起點，形成適合目標銅厚的光阻膜。交付均勻的電鍍光阻層，以光阻厚度與邊緣積膠檢查判讀結果；重點辨識局部光阻薄化使銅溢鍍。",
        "en": "Start with a seeded carrier; apply resist suited to the intended copper thickness to obtain a uniform plating-resist layer. Assess the result using resist-thickness and edge-bead checks, with particular attention to thin resist regions allowing copper overgrowth."
      },
      "input": {
        "zh-TW": "帶種子層的載板",
        "en": "a seeded carrier"
      },
      "operation": {
        "zh-TW": "形成適合目標銅厚的光阻膜",
        "en": "apply resist suited to the intended copper thickness"
      },
      "output": {
        "zh-TW": "均勻的電鍍光阻層",
        "en": "a uniform plating-resist layer"
      },
      "qualityEvidence": {
        "zh-TW": "光阻厚度與邊緣積膠檢查",
        "en": "resist-thickness and edge-bead checks"
      },
      "failureMode": {
        "zh-TW": "局部光阻薄化使銅溢鍍",
        "en": "thin resist regions allowing copper overgrowth"
      },
      "prerequisiteIds": [
        "F04"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "fanout",
      "sourceIds": [
        "evg-process",
        "lam-flow"
      ],
      "sourceUrls": [
        "https://www.evgroup.com/fileadmin/media/company/service/Process_Services_Flyer_24_04.pdf",
        "https://newsroom.lamresearch.com/the-ai-revolution-relies-on-advanced-packaging"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "F06",
      "catalogueOrder": 46,
      "branchId": "fanout",
      "branchOrder": 6,
      "activityType": "manufacturing",
      "title": {
        "zh-TW": "曝光顯影RDL線路圖案",
        "en": "Expose and develop RDL routing"
      },
      "summary": {
        "zh-TW": "以光阻層與線路版圖為起點，對位曝光並顯影線路窗口。交付可鍍出細線的光阻模版，以線寬、間距與套準量測判讀結果；重點辨識開口橋接或細線窗口斷裂。",
        "en": "Start with resist layer and routing artwork; align, expose and develop route windows to obtain a resist mold for fine copper routes. Assess the result using line, space and overlay measurements, with particular attention to bridged openings or broken fine-line windows."
      },
      "input": {
        "zh-TW": "光阻層與線路版圖",
        "en": "resist layer and routing artwork"
      },
      "operation": {
        "zh-TW": "對位曝光並顯影線路窗口",
        "en": "align, expose and develop route windows"
      },
      "output": {
        "zh-TW": "可鍍出細線的光阻模版",
        "en": "a resist mold for fine copper routes"
      },
      "qualityEvidence": {
        "zh-TW": "線寬、間距與套準量測",
        "en": "line, space and overlay measurements"
      },
      "failureMode": {
        "zh-TW": "開口橋接或細線窗口斷裂",
        "en": "bridged openings or broken fine-line windows"
      },
      "prerequisiteIds": [
        "F05"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "fanout",
      "sourceIds": [
        "evg-process",
        "kla-metrology"
      ],
      "sourceUrls": [
        "https://www.evgroup.com/fileadmin/media/company/service/Process_Services_Flyer_24_04.pdf",
        "https://ask.kla-tencor.com/products/packaging-manufacturing/wafer-inspection-and-metrology-for-advanced-packaging"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "F07",
      "catalogueOrder": 47,
      "branchId": "fanout",
      "branchOrder": 7,
      "activityType": "manufacturing",
      "title": {
        "zh-TW": "電鍍銅線與介層連接",
        "en": "Electroplate copper lines and vias"
      },
      "summary": {
        "zh-TW": "以已顯影的RDL光阻模版為起點，填充窗口及介層開口。交付連續銅RDL與介層連接，以厚度分布與填孔截面試片判讀結果；重點辨識填孔空洞或局部過鍍。",
        "en": "Start with developed RDL resist mold; fill routing windows and interlayer openings to obtain continuous copper RDL and via connections. Assess the result using thickness distribution and via-fill coupons, with particular attention to via voids or localized overplating."
      },
      "input": {
        "zh-TW": "已顯影的RDL光阻模版",
        "en": "developed RDL resist mold"
      },
      "operation": {
        "zh-TW": "填充窗口及介層開口",
        "en": "fill routing windows and interlayer openings"
      },
      "output": {
        "zh-TW": "連續銅RDL與介層連接",
        "en": "continuous copper RDL and via connections"
      },
      "qualityEvidence": {
        "zh-TW": "厚度分布與填孔截面試片",
        "en": "thickness distribution and via-fill coupons"
      },
      "failureMode": {
        "zh-TW": "填孔空洞或局部過鍍",
        "en": "via voids or localized overplating"
      },
      "prerequisiteIds": [
        "F06"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "fanout",
      "sourceIds": [
        "lam-electrofill",
        "applied-fanout"
      ],
      "sourceUrls": [
        "https://www.lamresearch.com/product/sabre-3d/",
        "https://www.appliedmaterials.com/il/en/semiconductor/markets-and-inflections/heterogeneous-integration/fan-out.html"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "F08",
      "catalogueOrder": 48,
      "branchId": "fanout",
      "branchOrder": 8,
      "activityType": "manufacturing",
      "title": {
        "zh-TW": "剝除電鍍光阻",
        "en": "Strip the plating resist"
      },
      "summary": {
        "zh-TW": "以完成電鍍的銅線為起點，移除光阻而保留金屬形貌。交付露出多餘種子層的銅圖案，以有機殘留與銅線損傷檢查判讀結果；重點辨識殘膠阻擋後續種子層移除。",
        "en": "Start with electroplated copper routes; remove resist while preserving metal geometry to obtain copper patterns with exposed excess seed. Assess the result using organic-residue and copper-damage checks, with particular attention to residue obstructing later seed removal."
      },
      "input": {
        "zh-TW": "完成電鍍的銅線",
        "en": "electroplated copper routes"
      },
      "operation": {
        "zh-TW": "移除光阻而保留金屬形貌",
        "en": "remove resist while preserving metal geometry"
      },
      "output": {
        "zh-TW": "露出多餘種子層的銅圖案",
        "en": "copper patterns with exposed excess seed"
      },
      "qualityEvidence": {
        "zh-TW": "有機殘留與銅線損傷檢查",
        "en": "organic-residue and copper-damage checks"
      },
      "failureMode": {
        "zh-TW": "殘膠阻擋後續種子層移除",
        "en": "residue obstructing later seed removal"
      },
      "prerequisiteIds": [
        "F07"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "fanout",
      "sourceIds": [
        "lam-flow",
        "evg-process"
      ],
      "sourceUrls": [
        "https://newsroom.lamresearch.com/the-ai-revolution-relies-on-advanced-packaging",
        "https://www.evgroup.com/fileadmin/media/company/service/Process_Services_Flyer_24_04.pdf"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "F09",
      "catalogueOrder": 49,
      "branchId": "fanout",
      "branchOrder": 9,
      "activityType": "manufacturing",
      "title": {
        "zh-TW": "蝕除多餘種子層並隔離線路",
        "en": "Etch excess seed and isolate RDL routes"
      },
      "summary": {
        "zh-TW": "以去光阻後銅圖案為起點，移除線間種子層並控制側向損失。交付已電性隔離的RDL網路，以線間絕緣與側蝕量判讀結果；重點辨識殘銅短路或線寬過度損失。",
        "en": "Start with copper patterns after resist strip; remove interline seed while limiting lateral loss to obtain electrically isolated RDL nets. Assess the result using interline isolation and undercut evidence, with particular attention to copper shorts or excessive line-width loss."
      },
      "input": {
        "zh-TW": "去光阻後銅圖案",
        "en": "copper patterns after resist strip"
      },
      "operation": {
        "zh-TW": "移除線間種子層並控制側向損失",
        "en": "remove interline seed while limiting lateral loss"
      },
      "output": {
        "zh-TW": "已電性隔離的RDL網路",
        "en": "electrically isolated RDL nets"
      },
      "qualityEvidence": {
        "zh-TW": "線間絕緣與側蝕量",
        "en": "interline isolation and undercut evidence"
      },
      "failureMode": {
        "zh-TW": "殘銅短路或線寬過度損失",
        "en": "copper shorts or excessive line-width loss"
      },
      "prerequisiteIds": [
        "F08"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "fanout",
      "sourceIds": [
        "lam-flow",
        "kla-metrology"
      ],
      "sourceUrls": [
        "https://newsroom.lamresearch.com/the-ai-revolution-relies-on-advanced-packaging",
        "https://ask.kla-tencor.com/products/packaging-manufacturing/wafer-inspection-and-metrology-for-advanced-packaging"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "F10",
      "catalogueOrder": 50,
      "branchId": "fanout",
      "branchOrder": 10,
      "activityType": "inspection_test",
      "title": {
        "zh-TW": "檢查RDL並核准多層循環",
        "en": "Inspect RDL and authorize layer repetition"
      },
      "summary": {
        "zh-TW": "以單層RDL及下一層設計為起點，量測線路並決定是否重複介電與金屬循環。交付具逐層證據的多層RDL，以開短路、線寬與層間套準判讀結果；重點辨識上層覆蓋後才發現底層缺陷。",
        "en": "Start with a completed RDL layer and next-layer design; measure routes and release repeated dielectric/metal cycles to obtain multilayer RDL with layer-by-layer evidence. Assess the result using opens/shorts, dimensions and interlayer overlay, with particular attention to discovering buried defects after subsequent layers."
      },
      "input": {
        "zh-TW": "單層RDL及下一層設計",
        "en": "a completed RDL layer and next-layer design"
      },
      "operation": {
        "zh-TW": "量測線路並決定是否重複介電與金屬循環",
        "en": "measure routes and release repeated dielectric/metal cycles"
      },
      "output": {
        "zh-TW": "具逐層證據的多層RDL",
        "en": "multilayer RDL with layer-by-layer evidence"
      },
      "qualityEvidence": {
        "zh-TW": "開短路、線寬與層間套準",
        "en": "opens/shorts, dimensions and interlayer overlay"
      },
      "failureMode": {
        "zh-TW": "上層覆蓋後才發現底層缺陷",
        "en": "discovering buried defects after subsequent layers"
      },
      "prerequisiteIds": [
        "F09"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "fanout",
      "sourceIds": [
        "kla-metrology",
        "ase-fanout"
      ],
      "sourceUrls": [
        "https://ask.kla-tencor.com/products/packaging-manufacturing/wafer-inspection-and-metrology-for-advanced-packaging",
        "https://ase.aseglobal.com/fan-out-packaging/"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      },
      "repeatLoop": {
        "itemIds": [
          "F02",
          "F03",
          "F04",
          "F05",
          "F06",
          "F07",
          "F08",
          "F09"
        ],
        "condition": {
          "zh-TW": "僅依設計層數重複並逐層檢驗，不增加虛構的課程數。",
          "en": "Repeat only for designed layers with per-layer inspection; repetition does not inflate the course count."
        }
      }
    },
    {
      "id": "F11",
      "catalogueOrder": 51,
      "branchId": "fanout",
      "branchOrder": 11,
      "activityType": "manufacturing",
      "title": {
        "zh-TW": "形成最上層保護與接合開口",
        "en": "Form top passivation and bond openings"
      },
      "summary": {
        "zh-TW": "以通過檢查的RDL疊層為起點，保護走線並打開晶粒接合區。交付具有接合窗口的RDL表面，以開口對位與保護膜完整性判讀結果；重點辨識保護膜覆蓋接點或邊緣裂開。",
        "en": "Start with inspected multilayer RDL; protect routing and expose die-joining sites to obtain a passivated RDL surface with joining windows. Assess the result using opening alignment and passivation integrity, with particular attention to covered contacts or cracked passivation edges."
      },
      "input": {
        "zh-TW": "通過檢查的RDL疊層",
        "en": "inspected multilayer RDL"
      },
      "operation": {
        "zh-TW": "保護走線並打開晶粒接合區",
        "en": "protect routing and expose die-joining sites"
      },
      "output": {
        "zh-TW": "具有接合窗口的RDL表面",
        "en": "a passivated RDL surface with joining windows"
      },
      "qualityEvidence": {
        "zh-TW": "開口對位與保護膜完整性",
        "en": "opening alignment and passivation integrity"
      },
      "failureMode": {
        "zh-TW": "保護膜覆蓋接點或邊緣裂開",
        "en": "covered contacts or cracked passivation edges"
      },
      "prerequisiteIds": [
        "F10"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "fanout",
      "sourceIds": [
        "amkor-bumping",
        "kla-deposition"
      ],
      "sourceUrls": [
        "https://amkor.com/services/wafer-bumping/",
        "https://www.spts.com/products/packaging-manufacturing/wafer-processing-systems-for-advanced-packaging"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "F12",
      "catalogueOrder": 52,
      "branchId": "fanout",
      "branchOrder": 12,
      "activityType": "manufacturing",
      "title": {
        "zh-TW": "製作RDL晶粒端接合金屬",
        "en": "Form die-side joining metallurgy on RDL"
      },
      "summary": {
        "zh-TW": "以RDL接合窗口與金屬規格為起點，形成選定的接合墊或微凸塊。交付可連接KGD的RDL端點，以金屬厚度與接合面形貌判讀結果；重點辨識接合金屬不相容或氧化。",
        "en": "Start with RDL joining windows and metallurgy specification; form the selected joining pads or microbumps to obtain RDL terminals ready for KGD attachment. Assess the result using metal thickness and joining-surface morphology, with particular attention to incompatible or oxidized joining metal."
      },
      "input": {
        "zh-TW": "RDL接合窗口與金屬規格",
        "en": "RDL joining windows and metallurgy specification"
      },
      "operation": {
        "zh-TW": "形成選定的接合墊或微凸塊",
        "en": "form the selected joining pads or microbumps"
      },
      "output": {
        "zh-TW": "可連接KGD的RDL端點",
        "en": "RDL terminals ready for KGD attachment"
      },
      "qualityEvidence": {
        "zh-TW": "金屬厚度與接合面形貌",
        "en": "metal thickness and joining-surface morphology"
      },
      "failureMode": {
        "zh-TW": "接合金屬不相容或氧化",
        "en": "incompatible or oxidized joining metal"
      },
      "prerequisiteIds": [
        "F11"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "fanout",
      "sourceIds": [
        "amkor-bumping",
        "lam-electrofill"
      ],
      "sourceUrls": [
        "https://amkor.com/services/wafer-bumping/",
        "https://www.lamresearch.com/product/sabre-3d/"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "F13",
      "catalogueOrder": 53,
      "branchId": "fanout",
      "branchOrder": 13,
      "activityType": "inspection_test",
      "title": {
        "zh-TW": "篩選良品RDL載體",
        "en": "Screen known-good RDL carriers"
      },
      "summary": {
        "zh-TW": "以完成接點的RDL載體為起點，在投入昂貴晶粒前測試可達網路。交付可用RDL區與排除區地圖，以線路連通與絕緣測試判讀結果；重點辨識未篩選RDL造成昂貴晶粒損失。",
        "en": "Start with RDL carriers with finished terminals; test accessible networks before committing expensive dies to obtain usable and excluded RDL-site maps. Assess the result using routing continuity and insulation tests, with particular attention to untested RDL consuming expensive good dies."
      },
      "input": {
        "zh-TW": "完成接點的RDL載體",
        "en": "RDL carriers with finished terminals"
      },
      "operation": {
        "zh-TW": "在投入昂貴晶粒前測試可達網路",
        "en": "test accessible networks before committing expensive dies"
      },
      "output": {
        "zh-TW": "可用RDL區與排除區地圖",
        "en": "usable and excluded RDL-site maps"
      },
      "qualityEvidence": {
        "zh-TW": "線路連通與絕緣測試",
        "en": "routing continuity and insulation tests"
      },
      "failureMode": {
        "zh-TW": "未篩選RDL造成昂貴晶粒損失",
        "en": "untested RDL consuming expensive good dies"
      },
      "prerequisiteIds": [
        "F12"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "fanout",
      "sourceIds": [
        "ase-fanout",
        "ieee-test"
      ],
      "sourceUrls": [
        "https://ase.aseglobal.com/fan-out-packaging/",
        "https://cmte.ieee.org/eps-test/wp-content/uploads/sites/132/2022/01/IEEE_EPS_Test_Het_Int_Product_Testability_BKM_Final_v1_0-1-14-22-1.pdf"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "F14",
      "catalogueOrder": 54,
      "branchId": "fanout",
      "branchOrder": 14,
      "activityType": "manufacturing",
      "title": {
        "zh-TW": "將KGD貼裝至預製RDL",
        "en": "Attach KGD to preformed RDL"
      },
      "summary": {
        "zh-TW": "以良品RDL與已測晶粒為起點，對準端點並完成晶粒接合。交付RDL-first晶粒組件，以接合偏移與可測接點電性判讀結果；重點辨識晶粒偏移造成接點短接。",
        "en": "Start with known-good RDL and tested dies; align terminals and join the dies to obtain an RDL-first die assembly. Assess the result using bond placement and accessible contact tests, with particular attention to die misplacement shorting neighboring terminals."
      },
      "input": {
        "zh-TW": "良品RDL與已測晶粒",
        "en": "known-good RDL and tested dies"
      },
      "operation": {
        "zh-TW": "對準端點並完成晶粒接合",
        "en": "align terminals and join the dies"
      },
      "output": {
        "zh-TW": "RDL-first晶粒組件",
        "en": "an RDL-first die assembly"
      },
      "qualityEvidence": {
        "zh-TW": "接合偏移與可測接點電性",
        "en": "bond placement and accessible contact tests"
      },
      "failureMode": {
        "zh-TW": "晶粒偏移造成接點短接",
        "en": "die misplacement shorting neighboring terminals"
      },
      "prerequisiteIds": [
        "F13"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "fanout",
      "sourceIds": [
        "ase-fanout",
        "besi-tcb"
      ],
      "sourceUrls": [
        "https://ase.aseglobal.com/fan-out-packaging/",
        "https://www.besi.com/products-technology/product-details/productgroup/thermo-compression-bonding/"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "F15",
      "catalogueOrder": 55,
      "branchId": "fanout",
      "branchOrder": 15,
      "activityType": "manufacturing",
      "title": {
        "zh-TW": "填充RDL-first接合間隙",
        "en": "Underfill RDL-first die joints"
      },
      "summary": {
        "zh-TW": "以已接合晶粒與RDL載體為起點，沿核准流路填膠並固化。交付受保護的晶粒接合間隙，以填充覆蓋、氣泡與固化紀錄判讀結果；重點辨識填膠流路堵塞或濕潤不良。",
        "en": "Start with joined dies on the RDL carrier; dispense along qualified flow paths and cure to obtain reinforced die-joint gaps. Assess the result using fill coverage, bubbles and cure records, with particular attention to blocked flow paths or poor wetting."
      },
      "input": {
        "zh-TW": "已接合晶粒與RDL載體",
        "en": "joined dies on the RDL carrier"
      },
      "operation": {
        "zh-TW": "沿核准流路填膠並固化",
        "en": "dispense along qualified flow paths and cure"
      },
      "output": {
        "zh-TW": "受保護的晶粒接合間隙",
        "en": "reinforced die-joint gaps"
      },
      "qualityEvidence": {
        "zh-TW": "填充覆蓋、氣泡與固化紀錄",
        "en": "fill coverage, bubbles and cure records"
      },
      "failureMode": {
        "zh-TW": "填膠流路堵塞或濕潤不良",
        "en": "blocked flow paths or poor wetting"
      },
      "prerequisiteIds": [
        "F14"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "fanout",
      "sourceIds": [
        "nordson-underfill",
        "ase-fanout"
      ],
      "sourceUrls": [
        "https://www.nordson.com/en/divisions/electronics-solutions/your-process/fluid-types/underfill",
        "https://ase.aseglobal.com/fan-out-packaging/"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "F16",
      "catalogueOrder": 56,
      "branchId": "fanout",
      "branchOrder": 16,
      "activityType": "manufacturing",
      "title": {
        "zh-TW": "壓縮模封RDL-first組件",
        "en": "Compression-mold the RDL-first assembly"
      },
      "summary": {
        "zh-TW": "以晶粒組件與模封材料為起點，包覆晶粒並控制材料流動。交付重組的模封載體，以填充完整性與晶粒位置變化判讀結果；重點辨識模封空洞或應力引起位移。",
        "en": "Start with die assembly and molding compound; encapsulate dies while controlling material flow to obtain a reconstituted molded carrier. Assess the result using fill integrity and die-position change, with particular attention to mold voids or stress-induced displacement."
      },
      "input": {
        "zh-TW": "晶粒組件與模封材料",
        "en": "die assembly and molding compound"
      },
      "operation": {
        "zh-TW": "包覆晶粒並控制材料流動",
        "en": "encapsulate dies while controlling material flow"
      },
      "output": {
        "zh-TW": "重組的模封載體",
        "en": "a reconstituted molded carrier"
      },
      "qualityEvidence": {
        "zh-TW": "填充完整性與晶粒位置變化",
        "en": "fill integrity and die-position change"
      },
      "failureMode": {
        "zh-TW": "模封空洞或應力引起位移",
        "en": "mold voids or stress-induced displacement"
      },
      "prerequisiteIds": [
        "F15"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "fanout",
      "sourceIds": [
        "ase-fanout",
        "ase-thermal"
      ],
      "sourceUrls": [
        "https://ase.aseglobal.com/fan-out-packaging/",
        "https://ase.aseglobal.com/lab-services/stress-and-thermal-lab/"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "F17",
      "catalogueOrder": 57,
      "branchId": "fanout",
      "branchOrder": 17,
      "activityType": "manufacturing",
      "title": {
        "zh-TW": "研磨模封面並控制高度",
        "en": "Grind mold surfaces to controlled height"
      },
      "summary": {
        "zh-TW": "以模封後載體為起點，整平模封面並維持晶粒保護餘量。交付高度受控的模封組件，以厚度、翹曲與露晶狀態判讀結果；重點辨識過磨傷及晶粒或產生薄弱區。",
        "en": "Start with a molded carrier; planarize the mold while retaining required protection to obtain a molded assembly with controlled height. Assess the result using thickness, warpage and die-exposure checks, with particular attention to over-grinding that damages dies or weakens mold."
      },
      "input": {
        "zh-TW": "模封後載體",
        "en": "a molded carrier"
      },
      "operation": {
        "zh-TW": "整平模封面並維持晶粒保護餘量",
        "en": "planarize the mold while retaining required protection"
      },
      "output": {
        "zh-TW": "高度受控的模封組件",
        "en": "a molded assembly with controlled height"
      },
      "qualityEvidence": {
        "zh-TW": "厚度、翹曲與露晶狀態",
        "en": "thickness, warpage and die-exposure checks"
      },
      "failureMode": {
        "zh-TW": "過磨傷及晶粒或產生薄弱區",
        "en": "over-grinding that damages dies or weakens mold"
      },
      "prerequisiteIds": [
        "F16"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "fanout",
      "sourceIds": [
        "disco-solutions",
        "ase-fanout"
      ],
      "sourceUrls": [
        "https://www.disco.co.jp/eg/solution/",
        "https://ase.aseglobal.com/fan-out-packaging/"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "F18",
      "catalogueOrder": 58,
      "branchId": "fanout",
      "branchOrder": 18,
      "activityType": "manufacturing",
      "title": {
        "zh-TW": "解鍵合並露出RDL背面",
        "en": "Debond and expose the RDL backside"
      },
      "summary": {
        "zh-TW": "以可自支撐的模封組件與載板為起點，依釋放層路線移除載板與殘留。交付可進行外部端點加工的RDL背面，以剝離完整性與表面殘留判讀結果；重點辨識RDL剝離或殘膠遮蔽接點。",
        "en": "Start with self-supporting molded assembly and carrier; remove carrier and residue using the release-layer route to obtain an RDL backside accessible for external termination. Assess the result using release integrity and surface-residue checks, with particular attention to RDL delamination or adhesive-covered contacts."
      },
      "input": {
        "zh-TW": "可自支撐的模封組件與載板",
        "en": "self-supporting molded assembly and carrier"
      },
      "operation": {
        "zh-TW": "依釋放層路線移除載板與殘留",
        "en": "remove carrier and residue using the release-layer route"
      },
      "output": {
        "zh-TW": "可進行外部端點加工的RDL背面",
        "en": "an RDL backside accessible for external termination"
      },
      "qualityEvidence": {
        "zh-TW": "剝離完整性與表面殘留",
        "en": "release integrity and surface-residue checks"
      },
      "failureMode": {
        "zh-TW": "RDL剝離或殘膠遮蔽接點",
        "en": "RDL delamination or adhesive-covered contacts"
      },
      "prerequisiteIds": [
        "F17"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "fanout",
      "sourceIds": [
        "evg-process",
        "ase-fanout"
      ],
      "sourceUrls": [
        "https://www.evgroup.com/fileadmin/media/company/service/Process_Services_Flyer_24_04.pdf",
        "https://ase.aseglobal.com/fan-out-packaging/"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "F19",
      "catalogueOrder": 59,
      "branchId": "fanout",
      "branchOrder": 19,
      "activityType": "manufacturing",
      "title": {
        "zh-TW": "完成扇出模組外部端點",
        "en": "Finish fan-out external terminals"
      },
      "summary": {
        "zh-TW": "以露出背面的扇出組件為起點，依產品接口形成背面接合金屬與端點。交付具有外部端點的扇出組件，以端點形貌、連通性與共面度判讀結果；重點辨識端點表面污染或高度不一致。",
        "en": "Start with fan-out assemblies with accessible backsides; form backside joining metallurgy and terminals for the product interface to obtain fan-out assemblies with external terminals. Assess the result using terminal morphology, continuity and coplanarity, with particular attention to contaminated terminal surfaces or inconsistent height."
      },
      "input": {
        "zh-TW": "露出背面的扇出組件",
        "en": "fan-out assemblies with accessible backsides"
      },
      "operation": {
        "zh-TW": "依產品接口形成背面接合金屬與端點",
        "en": "form backside joining metallurgy and terminals for the product interface"
      },
      "output": {
        "zh-TW": "具有外部端點的扇出組件",
        "en": "fan-out assemblies with external terminals"
      },
      "qualityEvidence": {
        "zh-TW": "端點形貌、連通性與共面度",
        "en": "terminal morphology, continuity and coplanarity"
      },
      "failureMode": {
        "zh-TW": "端點表面污染或高度不一致",
        "en": "contaminated terminal surfaces or inconsistent height"
      },
      "prerequisiteIds": [
        "F18"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "fanout",
      "sourceIds": [
        "amkor-bumping",
        "kla-metrology"
      ],
      "sourceUrls": [
        "https://amkor.com/services/wafer-bumping/",
        "https://ask.kla-tencor.com/products/packaging-manufacturing/wafer-inspection-and-metrology-for-advanced-packaging"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "F20",
      "catalogueOrder": 60,
      "branchId": "fanout",
      "branchOrder": 20,
      "activityType": "manufacturing",
      "title": {
        "zh-TW": "切割扇出模組並檢查邊緣",
        "en": "Singulate fan-out modules and inspect edges"
      },
      "summary": {
        "zh-TW": "以完成外部端點的重組組件為起點，沿核准街道分割並維持模組身分。交付可交接終封裝的獨立扇出模組，以切邊影像、翹曲與座標追溯判讀結果；重點辨識切割裂紋延伸至RDL或模組混料。",
        "en": "Start with reconstituted assemblies with finished terminals; singulate along qualified streets while retaining module identity to obtain individual fan-out modules for final integration. Assess the result using edge images, warpage and coordinate traceability, with particular attention to singulation cracks reaching RDL or mixed module identities."
      },
      "input": {
        "zh-TW": "完成外部端點的重組組件",
        "en": "reconstituted assemblies with finished terminals"
      },
      "operation": {
        "zh-TW": "沿核准街道分割並維持模組身分",
        "en": "singulate along qualified streets while retaining module identity"
      },
      "output": {
        "zh-TW": "可交接終封裝的獨立扇出模組",
        "en": "individual fan-out modules for final integration"
      },
      "qualityEvidence": {
        "zh-TW": "切邊影像、翹曲與座標追溯",
        "en": "edge images, warpage and coordinate traceability"
      },
      "failureMode": {
        "zh-TW": "切割裂紋延伸至RDL或模組混料",
        "en": "singulation cracks reaching RDL or mixed module identities"
      },
      "prerequisiteIds": [
        "F19"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "fanout",
      "sourceIds": [
        "disco-solutions",
        "ase-fanout"
      ],
      "sourceUrls": [
        "https://www.disco.co.jp/eg/solution/",
        "https://ase.aseglobal.com/fan-out-packaging/"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "H01",
      "catalogueOrder": 61,
      "branchId": "hybrid",
      "branchOrder": 1,
      "activityType": "inspection_test",
      "title": {
        "zh-TW": "確認混合鍵合面與接點配對",
        "en": "Verify hybrid-bond surfaces and pad pairing"
      },
      "summary": {
        "zh-TW": "以上下層晶粒設計與接合面為起點，核對面向、接點及介電材料相容性。交付可進行鍵合層製作的配對，以接點映射與材料相容性紀錄判讀結果；重點辨識面向或接點配對錯誤。",
        "en": "Start with top/bottom die designs and bonding surfaces; verify orientation, pad pairing and dielectric compatibility to obtain matched surfaces ready for bonding-layer preparation. Assess the result using pad mapping and compatibility records, with particular attention to incorrect facing orientation or pad pairing."
      },
      "input": {
        "zh-TW": "上下層晶粒設計與接合面",
        "en": "top/bottom die designs and bonding surfaces"
      },
      "operation": {
        "zh-TW": "核對面向、接點及介電材料相容性",
        "en": "verify orientation, pad pairing and dielectric compatibility"
      },
      "output": {
        "zh-TW": "可進行鍵合層製作的配對",
        "en": "matched surfaces ready for bonding-layer preparation"
      },
      "qualityEvidence": {
        "zh-TW": "接點映射與材料相容性紀錄",
        "en": "pad mapping and compatibility records"
      },
      "failureMode": {
        "zh-TW": "面向或接點配對錯誤",
        "en": "incorrect facing orientation or pad pairing"
      },
      "prerequisiteIds": [
        "C20"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "hybrid",
      "sourceIds": [
        "tsmc-soic",
        "imec-d2w"
      ],
      "sourceUrls": [
        "https://3dfabric.tsmc.com/english/dedicatedFoundry/technology/SoIC.htm",
        "https://www.imec-int.com/en/press/imec-demonstrates-die-wafer-hybrid-bonding-cu-interconnect-pad-pitch-2mm"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "H02",
      "catalogueOrder": 62,
      "branchId": "hybrid",
      "branchOrder": 2,
      "activityType": "manufacturing",
      "title": {
        "zh-TW": "沉積混合鍵合介電層",
        "en": "Deposit the hybrid-bond dielectric"
      },
      "summary": {
        "zh-TW": "以已完成電路的晶圓與選定介電材料為起點，形成可平坦化的接合介電膜。交付待製作銅接點的介電層，以膜厚、應力與均勻性判讀結果；重點辨識薄膜缺陷阻礙直接鍵合。",
        "en": "Start with processed circuit wafers and selected dielectric; deposit a bond dielectric suitable for planarization to obtain a dielectric layer for copper-contact formation. Assess the result using film thickness, stress and uniformity, with particular attention to film defects preventing direct bonding."
      },
      "input": {
        "zh-TW": "已完成電路的晶圓與選定介電材料",
        "en": "processed circuit wafers and selected dielectric"
      },
      "operation": {
        "zh-TW": "形成可平坦化的接合介電膜",
        "en": "deposit a bond dielectric suitable for planarization"
      },
      "output": {
        "zh-TW": "待製作銅接點的介電層",
        "en": "a dielectric layer for copper-contact formation"
      },
      "qualityEvidence": {
        "zh-TW": "膜厚、應力與均勻性",
        "en": "film thickness, stress and uniformity"
      },
      "failureMode": {
        "zh-TW": "薄膜缺陷阻礙直接鍵合",
        "en": "film defects preventing direct bonding"
      },
      "prerequisiteIds": [
        "H01"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "hybrid",
      "sourceIds": [
        "kla-deposition",
        "imec-w2w"
      ],
      "sourceUrls": [
        "https://www.spts.com/products/packaging-manufacturing/wafer-processing-systems-for-advanced-packaging",
        "https://www.imec-int.com/en/articles/wafer-wafer-hybrid-bonding-pushing-boundaries-400nm-interconnect-pitch"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "H03",
      "catalogueOrder": 63,
      "branchId": "hybrid",
      "branchOrder": 3,
      "activityType": "manufacturing",
      "title": {
        "zh-TW": "圖案化混合鍵合接點開口",
        "en": "Pattern hybrid-bond contact openings"
      },
      "summary": {
        "zh-TW": "以接合介電膜與接點版圖為起點，以光刻定義銅接點腔體位置。交付接點蝕刻圖案，以臨界尺寸與電路層套準判讀結果；重點辨識接點位置偏離下方導線。",
        "en": "Start with bond dielectric and contact artwork; lithographically define copper-contact cavities to obtain a contact-etch pattern. Assess the result using critical dimensions and circuit-layer overlay, with particular attention to contacts misaligned to underlying conductors."
      },
      "input": {
        "zh-TW": "接合介電膜與接點版圖",
        "en": "bond dielectric and contact artwork"
      },
      "operation": {
        "zh-TW": "以光刻定義銅接點腔體位置",
        "en": "lithographically define copper-contact cavities"
      },
      "output": {
        "zh-TW": "接點蝕刻圖案",
        "en": "a contact-etch pattern"
      },
      "qualityEvidence": {
        "zh-TW": "臨界尺寸與電路層套準",
        "en": "critical dimensions and circuit-layer overlay"
      },
      "failureMode": {
        "zh-TW": "接點位置偏離下方導線",
        "en": "contacts misaligned to underlying conductors"
      },
      "prerequisiteIds": [
        "H02"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "hybrid",
      "sourceIds": [
        "imec-w2w",
        "evg-process"
      ],
      "sourceUrls": [
        "https://www.imec-int.com/en/articles/wafer-wafer-hybrid-bonding-pushing-boundaries-400nm-interconnect-pitch",
        "https://www.evgroup.com/fileadmin/media/company/service/Process_Services_Flyer_24_04.pdf"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "H04",
      "catalogueOrder": 64,
      "branchId": "hybrid",
      "branchOrder": 4,
      "activityType": "manufacturing",
      "title": {
        "zh-TW": "蝕刻接合介電層腔體",
        "en": "Etch cavities in the bond dielectric"
      },
      "summary": {
        "zh-TW": "以完成圖案化的介電層為起點，形成受控深度的接點腔體。交付可填入金屬的介電腔體，以深度、側壁與底部殘留判讀結果；重點辨識孔底殘留或輪廓失控。",
        "en": "Start with patterned bonding dielectric; form contact cavities with controlled depth to obtain dielectric cavities ready for metallization. Assess the result using depth, sidewall and bottom-residue checks, with particular attention to bottom residue or uncontrolled cavity profiles."
      },
      "input": {
        "zh-TW": "完成圖案化的介電層",
        "en": "patterned bonding dielectric"
      },
      "operation": {
        "zh-TW": "形成受控深度的接點腔體",
        "en": "form contact cavities with controlled depth"
      },
      "output": {
        "zh-TW": "可填入金屬的介電腔體",
        "en": "dielectric cavities ready for metallization"
      },
      "qualityEvidence": {
        "zh-TW": "深度、側壁與底部殘留",
        "en": "depth, sidewall and bottom-residue checks"
      },
      "failureMode": {
        "zh-TW": "孔底殘留或輪廓失控",
        "en": "bottom residue or uncontrolled cavity profiles"
      },
      "prerequisiteIds": [
        "H03"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "hybrid",
      "sourceIds": [
        "imec-w2w",
        "kla-deposition"
      ],
      "sourceUrls": [
        "https://www.imec-int.com/en/articles/wafer-wafer-hybrid-bonding-pushing-boundaries-400nm-interconnect-pitch",
        "https://www.spts.com/products/packaging-manufacturing/wafer-processing-systems-for-advanced-packaging"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "H05",
      "catalogueOrder": 65,
      "branchId": "hybrid",
      "branchOrder": 5,
      "activityType": "manufacturing",
      "title": {
        "zh-TW": "沉積混合鍵合阻障與種子膜",
        "en": "Deposit hybrid-bond barrier and seed films"
      },
      "summary": {
        "zh-TW": "以已蝕刻的接點腔體為起點，覆蓋阻障與連續導電種子層。交付可填銅的接點腔體，以覆蓋性與導電連續性判讀結果；重點辨識金屬擴散或不完整種子覆蓋。",
        "en": "Start with etched contact cavities; coat barriers and a continuous conductive seed to obtain contact cavities ready for copper fill. Assess the result using coverage and electrical continuity, with particular attention to metal diffusion or incomplete seed coverage."
      },
      "input": {
        "zh-TW": "已蝕刻的接點腔體",
        "en": "etched contact cavities"
      },
      "operation": {
        "zh-TW": "覆蓋阻障與連續導電種子層",
        "en": "coat barriers and a continuous conductive seed"
      },
      "output": {
        "zh-TW": "可填銅的接點腔體",
        "en": "contact cavities ready for copper fill"
      },
      "qualityEvidence": {
        "zh-TW": "覆蓋性與導電連續性",
        "en": "coverage and electrical continuity"
      },
      "failureMode": {
        "zh-TW": "金屬擴散或不完整種子覆蓋",
        "en": "metal diffusion or incomplete seed coverage"
      },
      "prerequisiteIds": [
        "H04"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "hybrid",
      "sourceIds": [
        "imec-w2w",
        "lam-flow"
      ],
      "sourceUrls": [
        "https://www.imec-int.com/en/articles/wafer-wafer-hybrid-bonding-pushing-boundaries-400nm-interconnect-pitch",
        "https://newsroom.lamresearch.com/the-ai-revolution-relies-on-advanced-packaging"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "H06",
      "catalogueOrder": 66,
      "branchId": "hybrid",
      "branchOrder": 6,
      "activityType": "manufacturing",
      "title": {
        "zh-TW": "電鍍填充混合鍵合銅接點",
        "en": "Electrofill hybrid-bond copper contacts"
      },
      "summary": {
        "zh-TW": "以具種子層的腔體為起點，填入銅並保留後續CMP餘量。交付待平坦化的銅與介電表面，以填充截面與銅厚均勻性判讀結果；重點辨識接點內空洞或鍍層不均。",
        "en": "Start with seeded contact cavities; fill with copper while retaining CMP overburden to obtain copper/dielectric surfaces awaiting planarization. Assess the result using fill cross-sections and copper-thickness uniformity, with particular attention to internal contact voids or uneven plating."
      },
      "input": {
        "zh-TW": "具種子層的腔體",
        "en": "seeded contact cavities"
      },
      "operation": {
        "zh-TW": "填入銅並保留後續CMP餘量",
        "en": "fill with copper while retaining CMP overburden"
      },
      "output": {
        "zh-TW": "待平坦化的銅與介電表面",
        "en": "copper/dielectric surfaces awaiting planarization"
      },
      "qualityEvidence": {
        "zh-TW": "填充截面與銅厚均勻性",
        "en": "fill cross-sections and copper-thickness uniformity"
      },
      "failureMode": {
        "zh-TW": "接點內空洞或鍍層不均",
        "en": "internal contact voids or uneven plating"
      },
      "prerequisiteIds": [
        "H05"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "hybrid",
      "sourceIds": [
        "lam-electrofill",
        "imec-w2w"
      ],
      "sourceUrls": [
        "https://www.lamresearch.com/product/sabre-3d/",
        "https://www.imec-int.com/en/articles/wafer-wafer-hybrid-bonding-pushing-boundaries-400nm-interconnect-pitch"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "H07",
      "catalogueOrder": 67,
      "branchId": "hybrid",
      "branchOrder": 7,
      "activityType": "manufacturing",
      "title": {
        "zh-TW": "以CMP形成平坦鍵合表面",
        "en": "CMP-planarize the bonding surface"
      },
      "summary": {
        "zh-TW": "以含多餘銅的接合層為起點，共同控制介電平坦度與銅凹陷。交付可直接接觸的平坦表面，以局部與跨片形貌分布判讀結果；重點辨識過度凹陷、侵蝕或銅凸起。",
        "en": "Start with a bonding layer with excess copper; control dielectric planarity and copper recess by CMP to obtain a planar surface for direct contact. Assess the result using local and wafer-scale topography maps, with particular attention to excess recess, erosion or copper protrusion."
      },
      "input": {
        "zh-TW": "含多餘銅的接合層",
        "en": "a bonding layer with excess copper"
      },
      "operation": {
        "zh-TW": "共同控制介電平坦度與銅凹陷",
        "en": "control dielectric planarity and copper recess by CMP"
      },
      "output": {
        "zh-TW": "可直接接觸的平坦表面",
        "en": "a planar surface for direct contact"
      },
      "qualityEvidence": {
        "zh-TW": "局部與跨片形貌分布",
        "en": "local and wafer-scale topography maps"
      },
      "failureMode": {
        "zh-TW": "過度凹陷、侵蝕或銅凸起",
        "en": "excess recess, erosion or copper protrusion"
      },
      "prerequisiteIds": [
        "H06"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "hybrid",
      "sourceIds": [
        "imec-w2w",
        "bruker-bond"
      ],
      "sourceUrls": [
        "https://www.imec-int.com/en/articles/wafer-wafer-hybrid-bonding-pushing-boundaries-400nm-interconnect-pitch",
        "https://www.bruker.com/en/products-and-solutions/semiconductor-solutions/automated-afm-and-cipt-systems/resource-library/an-5001-surface-metrology-for-hybrid-bonding-in-advanced-semiconductor-packaging.html"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "H08",
      "catalogueOrder": 68,
      "branchId": "hybrid",
      "branchOrder": 8,
      "activityType": "inspection_test",
      "title": {
        "zh-TW": "量測銅凹陷與介電粗糙度",
        "en": "Measure copper recess and dielectric roughness"
      },
      "summary": {
        "zh-TW": "以CMP後的混合鍵合表面為起點，以AFM等方法量測局部與長程形貌。交付可追溯的鍵合面形貌報告，以銅接點剖線與跨區掃描判讀結果；重點辨識局部合格但長程高低差過大。",
        "en": "Start with hybrid-bond surfaces after CMP; measure local and long-range topography with suitable metrology to obtain a traceable bonding-topography report. Assess the result using copper-contact profiles and large-area scans, with particular attention to local compliance hiding long-range topography."
      },
      "input": {
        "zh-TW": "CMP後的混合鍵合表面",
        "en": "hybrid-bond surfaces after CMP"
      },
      "operation": {
        "zh-TW": "以AFM等方法量測局部與長程形貌",
        "en": "measure local and long-range topography with suitable metrology"
      },
      "output": {
        "zh-TW": "可追溯的鍵合面形貌報告",
        "en": "a traceable bonding-topography report"
      },
      "qualityEvidence": {
        "zh-TW": "銅接點剖線與跨區掃描",
        "en": "copper-contact profiles and large-area scans"
      },
      "failureMode": {
        "zh-TW": "局部合格但長程高低差過大",
        "en": "local compliance hiding long-range topography"
      },
      "prerequisiteIds": [
        "H07"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "hybrid",
      "sourceIds": [
        "bruker-bond"
      ],
      "sourceUrls": [
        "https://www.bruker.com/en/products-and-solutions/semiconductor-solutions/automated-afm-and-cipt-systems/resource-library/an-5001-surface-metrology-for-hybrid-bonding-in-advanced-semiconductor-packaging.html"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "H09",
      "catalogueOrder": 69,
      "branchId": "hybrid",
      "branchOrder": 9,
      "activityType": "inspection_test",
      "title": {
        "zh-TW": "檢查鍵合面顆粒與缺陷",
        "en": "Inspect bond-surface particles and defects"
      },
      "summary": {
        "zh-TW": "以形貌合格的鍵合面為起點，定位顆粒、刮傷與孔洞。交付可用接合區與缺陷地圖，以對位至版圖的缺陷座標判讀結果；重點辨識單一顆粒造成大面積未接合。",
        "en": "Start with topographically accepted bonding surfaces; locate particles, scratches and pits to obtain usable bond areas and defect maps. Assess the result using defect coordinates registered to layout, with particular attention to a single particle causing extended non-bonding."
      },
      "input": {
        "zh-TW": "形貌合格的鍵合面",
        "en": "topographically accepted bonding surfaces"
      },
      "operation": {
        "zh-TW": "定位顆粒、刮傷與孔洞",
        "en": "locate particles, scratches and pits"
      },
      "output": {
        "zh-TW": "可用接合區與缺陷地圖",
        "en": "usable bond areas and defect maps"
      },
      "qualityEvidence": {
        "zh-TW": "對位至版圖的缺陷座標",
        "en": "defect coordinates registered to layout"
      },
      "failureMode": {
        "zh-TW": "單一顆粒造成大面積未接合",
        "en": "a single particle causing extended non-bonding"
      },
      "prerequisiteIds": [
        "H08"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "hybrid",
      "sourceIds": [
        "kla-metrology",
        "evg-activation"
      ],
      "sourceUrls": [
        "https://ask.kla-tencor.com/products/packaging-manufacturing/wafer-inspection-and-metrology-for-advanced-packaging",
        "https://www.evgroup.com/fileadmin/media/company/news/2020/2020_12_10_EVG320_D2W/Press_Release_EVG320_D2W_2012_12_10_EN.pdf"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "H10",
      "catalogueOrder": 70,
      "branchId": "hybrid",
      "branchOrder": 10,
      "activityType": "manufacturing",
      "title": {
        "zh-TW": "施加切割用鍵合面保護層",
        "en": "Protect bonding surfaces before die singulation"
      },
      "summary": {
        "zh-TW": "以待切割上層晶圓為起點，施加可移除且相容的表面保護。交付受保護的D2W來源晶圓，以覆蓋完整性與移除相容性判讀結果；重點辨識保護材料無法乾淨移除。",
        "en": "Start with top-die wafers awaiting singulation; apply removable, compatible surface protection to obtain a protected source wafer for D2W. Assess the result using coverage and removal-compatibility evidence, with particular attention to protection that cannot be removed cleanly."
      },
      "input": {
        "zh-TW": "待切割上層晶圓",
        "en": "top-die wafers awaiting singulation"
      },
      "operation": {
        "zh-TW": "施加可移除且相容的表面保護",
        "en": "apply removable, compatible surface protection"
      },
      "output": {
        "zh-TW": "受保護的D2W來源晶圓",
        "en": "a protected source wafer for D2W"
      },
      "qualityEvidence": {
        "zh-TW": "覆蓋完整性與移除相容性",
        "en": "coverage and removal-compatibility evidence"
      },
      "failureMode": {
        "zh-TW": "保護材料無法乾淨移除",
        "en": "protection that cannot be removed cleanly"
      },
      "prerequisiteIds": [
        "H09"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "hybrid",
      "sourceIds": [
        "evg-d2w",
        "disco-solutions"
      ],
      "sourceUrls": [
        "https://www.evgroup.com/fileadmin/media/products/bonding/Die_to_Wafer_bonding_systems/White_Paper_D2W_Bonding.pdf",
        "https://www.disco.co.jp/eg/solution/"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "H11",
      "catalogueOrder": 71,
      "branchId": "hybrid",
      "branchOrder": 11,
      "activityType": "manufacturing",
      "title": {
        "zh-TW": "低污染切割上層鍵合晶粒",
        "en": "Singulate upper bonding dies with contamination control"
      },
      "summary": {
        "zh-TW": "以已保護的來源晶圓為起點，選擇相容切割路線並保護接合面。交付可挑選的上層鍵合晶粒，以邊緣損傷與鍵合面顆粒判讀結果；重點辨識切割碎屑污染高平坦度表面。",
        "en": "Start with a protected source wafer; singulate using a compatible surface-protecting route to obtain pickable upper dies for bonding. Assess the result using edge damage and bond-surface particles, with particular attention to dicing debris contaminating planar bond surfaces."
      },
      "input": {
        "zh-TW": "已保護的來源晶圓",
        "en": "a protected source wafer"
      },
      "operation": {
        "zh-TW": "選擇相容切割路線並保護接合面",
        "en": "singulate using a compatible surface-protecting route"
      },
      "output": {
        "zh-TW": "可挑選的上層鍵合晶粒",
        "en": "pickable upper dies for bonding"
      },
      "qualityEvidence": {
        "zh-TW": "邊緣損傷與鍵合面顆粒",
        "en": "edge damage and bond-surface particles"
      },
      "failureMode": {
        "zh-TW": "切割碎屑污染高平坦度表面",
        "en": "dicing debris contaminating planar bond surfaces"
      },
      "prerequisiteIds": [
        "H10"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "hybrid",
      "sourceIds": [
        "disco-solutions",
        "evg-d2w"
      ],
      "sourceUrls": [
        "https://www.disco.co.jp/eg/solution/",
        "https://www.evgroup.com/fileadmin/media/products/bonding/Die_to_Wafer_bonding_systems/White_Paper_D2W_Bonding.pdf"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "H12",
      "catalogueOrder": 72,
      "branchId": "hybrid",
      "branchOrder": 12,
      "activityType": "manufacturing",
      "title": {
        "zh-TW": "移除晶粒鍵合面保護材料",
        "en": "Remove die bonding-surface protection"
      },
      "summary": {
        "zh-TW": "以切割後的受保護晶粒為起點，去除保護層而不損傷銅與介電面。交付露出的混合鍵合表面，以有機殘留與表面形貌判讀結果；重點辨識不可見殘膜削弱鍵合。",
        "en": "Start with protected dies after singulation; remove protection without damaging copper or dielectric to obtain exposed hybrid-bonding surfaces. Assess the result using organic residue and surface-topography checks, with particular attention to invisible residue weakening the bond."
      },
      "input": {
        "zh-TW": "切割後的受保護晶粒",
        "en": "protected dies after singulation"
      },
      "operation": {
        "zh-TW": "去除保護層而不損傷銅與介電面",
        "en": "remove protection without damaging copper or dielectric"
      },
      "output": {
        "zh-TW": "露出的混合鍵合表面",
        "en": "exposed hybrid-bonding surfaces"
      },
      "qualityEvidence": {
        "zh-TW": "有機殘留與表面形貌",
        "en": "organic residue and surface-topography checks"
      },
      "failureMode": {
        "zh-TW": "不可見殘膜削弱鍵合",
        "en": "invisible residue weakening the bond"
      },
      "prerequisiteIds": [
        "H11"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "hybrid",
      "sourceIds": [
        "evg-d2w",
        "evg-activation"
      ],
      "sourceUrls": [
        "https://www.evgroup.com/fileadmin/media/products/bonding/Die_to_Wafer_bonding_systems/White_Paper_D2W_Bonding.pdf",
        "https://www.evgroup.com/fileadmin/media/company/news/2020/2020_12_10_EVG320_D2W/Press_Release_EVG320_D2W_2012_12_10_EN.pdf"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "H13",
      "catalogueOrder": 73,
      "branchId": "hybrid",
      "branchOrder": 13,
      "activityType": "manufacturing",
      "title": {
        "zh-TW": "清潔上下層鍵合表面",
        "en": "Clean both hybrid-bonding surfaces"
      },
      "summary": {
        "zh-TW": "以已露出的晶粒與目標晶圓表面為起點，使用相容清潔步驟移除污染。交付可活化的潔淨接合面，以顆粒與殘留污染量測判讀結果；重點辨識清潔再污染或銅表面劣化。",
        "en": "Start with exposed die and target-wafer surfaces; remove contamination with a compatible cleaning sequence to obtain clean bonding surfaces ready for activation. Assess the result using particle and residual-contamination measurements, with particular attention to recontamination or copper-surface degradation."
      },
      "input": {
        "zh-TW": "已露出的晶粒與目標晶圓表面",
        "en": "exposed die and target-wafer surfaces"
      },
      "operation": {
        "zh-TW": "使用相容清潔步驟移除污染",
        "en": "remove contamination with a compatible cleaning sequence"
      },
      "output": {
        "zh-TW": "可活化的潔淨接合面",
        "en": "clean bonding surfaces ready for activation"
      },
      "qualityEvidence": {
        "zh-TW": "顆粒與殘留污染量測",
        "en": "particle and residual-contamination measurements"
      },
      "failureMode": {
        "zh-TW": "清潔再污染或銅表面劣化",
        "en": "recontamination or copper-surface degradation"
      },
      "prerequisiteIds": [
        "H12"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "hybrid",
      "sourceIds": [
        "evg-activation",
        "imec-d2w"
      ],
      "sourceUrls": [
        "https://www.evgroup.com/fileadmin/media/company/news/2020/2020_12_10_EVG320_D2W/Press_Release_EVG320_D2W_2012_12_10_EN.pdf",
        "https://www.imec-int.com/en/press/imec-demonstrates-die-wafer-hybrid-bonding-cu-interconnect-pad-pitch-2mm"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "H14",
      "catalogueOrder": 74,
      "branchId": "hybrid",
      "branchOrder": 14,
      "activityType": "manufacturing",
      "title": {
        "zh-TW": "活化鍵合介電表面",
        "en": "Activate the bonding dielectric surfaces"
      },
      "summary": {
        "zh-TW": "以通過清潔檢查的接合面為起點，依核准路線進行表面活化。交付適合預鍵合的表面狀態，以活化紀錄與表面狀態試片判讀結果；重點辨識活化不足或過度處理損傷。",
        "en": "Start with clean, inspected bonding surfaces; activate surfaces using the qualified route to obtain a surface condition suitable for prebonding. Assess the result using activation records and surface-state coupons, with particular attention to insufficient activation or treatment damage."
      },
      "input": {
        "zh-TW": "通過清潔檢查的接合面",
        "en": "clean, inspected bonding surfaces"
      },
      "operation": {
        "zh-TW": "依核准路線進行表面活化",
        "en": "activate surfaces using the qualified route"
      },
      "output": {
        "zh-TW": "適合預鍵合的表面狀態",
        "en": "a surface condition suitable for prebonding"
      },
      "qualityEvidence": {
        "zh-TW": "活化紀錄與表面狀態試片",
        "en": "activation records and surface-state coupons"
      },
      "failureMode": {
        "zh-TW": "活化不足或過度處理損傷",
        "en": "insufficient activation or treatment damage"
      },
      "prerequisiteIds": [
        "H13"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "hybrid",
      "sourceIds": [
        "evg-activation",
        "evg-d2w"
      ],
      "sourceUrls": [
        "https://www.evgroup.com/fileadmin/media/company/news/2020/2020_12_10_EVG320_D2W/Press_Release_EVG320_D2W_2012_12_10_EN.pdf",
        "https://www.evgroup.com/fileadmin/media/products/bonding/Die_to_Wafer_bonding_systems/White_Paper_D2W_Bonding.pdf"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "H15",
      "catalogueOrder": 75,
      "branchId": "hybrid",
      "branchOrder": 15,
      "activityType": "inspection_test",
      "title": {
        "zh-TW": "管制活化後待機與表面狀態",
        "en": "Control post-activation queue time and surface state"
      },
      "summary": {
        "zh-TW": "以已活化晶粒與鍵合排程為起點，核對待機暴露、潔淨與搬運條件。交付可立即鍵合的放行狀態，以時間戳、顆粒與表面監測判讀結果；重點辨識表面老化或搬運再污染。",
        "en": "Start with activated dies and the bonding schedule; review exposure time, cleanliness and handling to obtain release for immediate bonding. Assess the result using timestamps, particles and surface monitoring, with particular attention to surface aging or handling recontamination."
      },
      "input": {
        "zh-TW": "已活化晶粒與鍵合排程",
        "en": "activated dies and the bonding schedule"
      },
      "operation": {
        "zh-TW": "核對待機暴露、潔淨與搬運條件",
        "en": "review exposure time, cleanliness and handling"
      },
      "output": {
        "zh-TW": "可立即鍵合的放行狀態",
        "en": "release for immediate bonding"
      },
      "qualityEvidence": {
        "zh-TW": "時間戳、顆粒與表面監測",
        "en": "timestamps, particles and surface monitoring"
      },
      "failureMode": {
        "zh-TW": "表面老化或搬運再污染",
        "en": "surface aging or handling recontamination"
      },
      "prerequisiteIds": [
        "H14"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "hybrid",
      "sourceIds": [
        "evg-activation",
        "bruker-bond"
      ],
      "sourceUrls": [
        "https://www.evgroup.com/fileadmin/media/company/news/2020/2020_12_10_EVG320_D2W/Press_Release_EVG320_D2W_2012_12_10_EN.pdf",
        "https://www.bruker.com/en/products-and-solutions/semiconductor-solutions/automated-afm-and-cipt-systems/resource-library/an-5001-surface-metrology-for-hybrid-bonding-in-advanced-semiconductor-packaging.html"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "H16",
      "catalogueOrder": 76,
      "branchId": "hybrid",
      "branchOrder": 16,
      "activityType": "manufacturing",
      "title": {
        "zh-TW": "精密對準晶粒與目標晶圓",
        "en": "Precisely align dies to the target wafer"
      },
      "summary": {
        "zh-TW": "以待鍵合晶粒與目標標記為起點，量測並修正位置與角度。交付對準的晶粒與目標接點，以光學對準殘差與工具校正判讀結果；重點辨識局部畸變無法由剛體校正補償。",
        "en": "Start with bond-ready dies and target fiducials; measure and correct position and rotation to obtain aligned dies and target contacts. Assess the result using optical alignment residuals and tool calibration, with particular attention to local distortion not corrected by rigid alignment."
      },
      "input": {
        "zh-TW": "待鍵合晶粒與目標標記",
        "en": "bond-ready dies and target fiducials"
      },
      "operation": {
        "zh-TW": "量測並修正位置與角度",
        "en": "measure and correct position and rotation"
      },
      "output": {
        "zh-TW": "對準的晶粒與目標接點",
        "en": "aligned dies and target contacts"
      },
      "qualityEvidence": {
        "zh-TW": "光學對準殘差與工具校正",
        "en": "optical alignment residuals and tool calibration"
      },
      "failureMode": {
        "zh-TW": "局部畸變無法由剛體校正補償",
        "en": "local distortion not corrected by rigid alignment"
      },
      "prerequisiteIds": [
        "H15"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "hybrid",
      "sourceIds": [
        "imec-d2w",
        "evg-activation"
      ],
      "sourceUrls": [
        "https://www.imec-int.com/en/press/imec-demonstrates-die-wafer-hybrid-bonding-cu-interconnect-pad-pitch-2mm",
        "https://www.evgroup.com/fileadmin/media/company/news/2020/2020_12_10_EVG320_D2W/Press_Release_EVG320_D2W_2012_12_10_EN.pdf"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "H17",
      "catalogueOrder": 77,
      "branchId": "hybrid",
      "branchOrder": 17,
      "activityType": "manufacturing",
      "title": {
        "zh-TW": "建立直接接觸的預鍵合",
        "en": "Create the direct-contact prebond"
      },
      "summary": {
        "zh-TW": "以已對準且潔淨的兩接合面為起點，使介電面受控接觸並建立初始鍵合。交付可送後續熱處理的預鍵合組件，以接觸前緣與初始未接合區判讀結果；重點辨識顆粒或表面形變阻斷接觸。",
        "en": "Start with aligned and clean bonding surfaces; bring dielectric surfaces into controlled initial contact to obtain a prebonded assembly for subsequent heat treatment. Assess the result using contact-front and initial non-bond area evidence, with particular attention to particles or topography interrupting contact."
      },
      "input": {
        "zh-TW": "已對準且潔淨的兩接合面",
        "en": "aligned and clean bonding surfaces"
      },
      "operation": {
        "zh-TW": "使介電面受控接觸並建立初始鍵合",
        "en": "bring dielectric surfaces into controlled initial contact"
      },
      "output": {
        "zh-TW": "可送後續熱處理的預鍵合組件",
        "en": "a prebonded assembly for subsequent heat treatment"
      },
      "qualityEvidence": {
        "zh-TW": "接觸前緣與初始未接合區",
        "en": "contact-front and initial non-bond area evidence"
      },
      "failureMode": {
        "zh-TW": "顆粒或表面形變阻斷接觸",
        "en": "particles or topography interrupting contact"
      },
      "prerequisiteIds": [
        "H16"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "hybrid",
      "sourceIds": [
        "imec-w2w",
        "imec-d2w"
      ],
      "sourceUrls": [
        "https://www.imec-int.com/en/articles/wafer-wafer-hybrid-bonding-pushing-boundaries-400nm-interconnect-pitch",
        "https://www.imec-int.com/en/press/imec-demonstrates-die-wafer-hybrid-bonding-cu-interconnect-pad-pitch-2mm"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "H18",
      "catalogueOrder": 78,
      "branchId": "hybrid",
      "branchOrder": 18,
      "activityType": "manufacturing",
      "title": {
        "zh-TW": "退火完成銅與介電層鍵合",
        "en": "Anneal copper and dielectric hybrid bonds"
      },
      "summary": {
        "zh-TW": "以預鍵合組件與核准熱預算為起點，完成相容的熱處理以穩定界面。交付永久混合鍵合組件，以熱歷程與試片鍵合強度判讀結果；重點辨識熱預算失配或接點未閉合。",
        "en": "Start with prebonded assemblies and a qualified thermal budget; apply compatible thermal treatment to stabilize interfaces to obtain a permanent hybrid-bonded assembly. Assess the result using thermal history and bond-strength coupons, with particular attention to thermal-budget mismatch or unclosed contacts."
      },
      "input": {
        "zh-TW": "預鍵合組件與核准熱預算",
        "en": "prebonded assemblies and a qualified thermal budget"
      },
      "operation": {
        "zh-TW": "完成相容的熱處理以穩定界面",
        "en": "apply compatible thermal treatment to stabilize interfaces"
      },
      "output": {
        "zh-TW": "永久混合鍵合組件",
        "en": "a permanent hybrid-bonded assembly"
      },
      "qualityEvidence": {
        "zh-TW": "熱歷程與試片鍵合強度",
        "en": "thermal history and bond-strength coupons"
      },
      "failureMode": {
        "zh-TW": "熱預算失配或接點未閉合",
        "en": "thermal-budget mismatch or unclosed contacts"
      },
      "prerequisiteIds": [
        "H17"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "hybrid",
      "sourceIds": [
        "imec-w2w",
        "tsmc-soic"
      ],
      "sourceUrls": [
        "https://www.imec-int.com/en/articles/wafer-wafer-hybrid-bonding-pushing-boundaries-400nm-interconnect-pitch",
        "https://3dfabric.tsmc.com/english/dedicatedFoundry/technology/SoIC.htm"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "H19",
      "catalogueOrder": 79,
      "branchId": "hybrid",
      "branchOrder": 19,
      "activityType": "inspection_test",
      "title": {
        "zh-TW": "檢測鍵合空洞與後鍵合套準",
        "en": "Inspect bond voids and postbond overlay"
      },
      "summary": {
        "zh-TW": "以退火後的鍵合組件為起點，以相容非破壞方法檢查界面與偏移。交付空洞與偏移量測地圖，以影像、套準統計與基準對照判讀結果；重點辨識只看外觀漏掉內部未鍵合區。",
        "en": "Start with annealed bonded assemblies; inspect interfaces and alignment nondestructively to obtain bond-void and overlay maps. Assess the result using imaging, overlay statistics and reference comparison, with particular attention to external inspection missing internal non-bonds."
      },
      "input": {
        "zh-TW": "退火後的鍵合組件",
        "en": "annealed bonded assemblies"
      },
      "operation": {
        "zh-TW": "以相容非破壞方法檢查界面與偏移",
        "en": "inspect interfaces and alignment nondestructively"
      },
      "output": {
        "zh-TW": "空洞與偏移量測地圖",
        "en": "bond-void and overlay maps"
      },
      "qualityEvidence": {
        "zh-TW": "影像、套準統計與基準對照",
        "en": "imaging, overlay statistics and reference comparison"
      },
      "failureMode": {
        "zh-TW": "只看外觀漏掉內部未鍵合區",
        "en": "external inspection missing internal non-bonds"
      },
      "prerequisiteIds": [
        "H18"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "hybrid",
      "sourceIds": [
        "kla-metrology",
        "ase-fa"
      ],
      "sourceUrls": [
        "https://ask.kla-tencor.com/products/packaging-manufacturing/wafer-inspection-and-metrology-for-advanced-packaging",
        "https://ase.aseglobal.com/lab-services/failure-analysis-lab/"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "H20",
      "catalogueOrder": 80,
      "branchId": "hybrid",
      "branchOrder": 20,
      "activityType": "inspection_test",
      "title": {
        "zh-TW": "測試混合鍵合互連與分選",
        "en": "Test and bin hybrid-bond interconnects"
      },
      "summary": {
        "zh-TW": "以已檢查的鍵合晶圓或模組為起點，量測可存取接點鏈與功能。交付附晶粒位置的鍵合良品資料，以鏈電阻、開短路與功能測試判讀結果；重點辨識少量高阻接點被總平均掩蓋。",
        "en": "Start with inspected bonded wafers or modules; test accessible contact chains and functions to obtain bonded-good-die records with coordinates. Assess the result using chain resistance, opens/shorts and functional results, with particular attention to isolated resistive contacts hidden by averages."
      },
      "input": {
        "zh-TW": "已檢查的鍵合晶圓或模組",
        "en": "inspected bonded wafers or modules"
      },
      "operation": {
        "zh-TW": "量測可存取接點鏈與功能",
        "en": "test accessible contact chains and functions"
      },
      "output": {
        "zh-TW": "附晶粒位置的鍵合良品資料",
        "en": "bonded-good-die records with coordinates"
      },
      "qualityEvidence": {
        "zh-TW": "鏈電阻、開短路與功能測試",
        "en": "chain resistance, opens/shorts and functional results"
      },
      "failureMode": {
        "zh-TW": "少量高阻接點被總平均掩蓋",
        "en": "isolated resistive contacts hidden by averages"
      },
      "prerequisiteIds": [
        "H19"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "hybrid",
      "sourceIds": [
        "imec-d2w",
        "ieee-test"
      ],
      "sourceUrls": [
        "https://www.imec-int.com/en/press/imec-demonstrates-die-wafer-hybrid-bonding-cu-interconnect-pad-pitch-2mm",
        "https://cmte.ieee.org/eps-test/wp-content/uploads/sites/132/2022/01/IEEE_EPS_Test_Het_Int_Product_Testability_BKM_Final_v1_0-1-14-22-1.pdf"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      },
      "handoffNote": {
        "zh-TW": "若輸出仍為鍵合晶圓，需在產品終封裝路線補上經核准的背面加工與分割；本20項不是完整代工廠SOP。",
        "en": "If output remains a bonded wafer, add qualified backside finishing and singulation in the product route; these 20 topics are not a complete foundry SOP."
      }
    },
    {
      "id": "B01",
      "catalogueOrder": 81,
      "branchId": "bridge-chiplet",
      "branchOrder": 1,
      "activityType": "design",
      "title": {
        "zh-TW": "定義小晶片互連契約",
        "en": "Define the chiplet interconnect contract"
      },
      "summary": {
        "zh-TW": "以晶粒介面與系統協定需求為起點，明定實體連線、協定及測試責任。交付跨供應商互連契約，以版本、功能與相容性矩陣判讀結果；重點辨識機械可接但協定不相容。",
        "en": "Start with die interfaces and system protocol needs; define physical links, protocols and test responsibilities to obtain an interconnect contract across suppliers. Assess the result using version, feature and compatibility matrices, with particular attention to physically connected but protocol-incompatible dies."
      },
      "input": {
        "zh-TW": "晶粒介面與系統協定需求",
        "en": "die interfaces and system protocol needs"
      },
      "operation": {
        "zh-TW": "明定實體連線、協定及測試責任",
        "en": "define physical links, protocols and test responsibilities"
      },
      "output": {
        "zh-TW": "跨供應商互連契約",
        "en": "an interconnect contract across suppliers"
      },
      "qualityEvidence": {
        "zh-TW": "版本、功能與相容性矩陣",
        "en": "version, feature and compatibility matrices"
      },
      "failureMode": {
        "zh-TW": "機械可接但協定不相容",
        "en": "physically connected but protocol-incompatible dies"
      },
      "prerequisiteIds": [
        "C20"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "bridge",
      "sourceIds": [
        "ucie",
        "cadence-3dic"
      ],
      "sourceUrls": [
        "https://www.uciexpress.org/specifications",
        "https://www.cadence.com/en_US/home/resources/white-papers/3d-ic-design-wp.html"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "B02",
      "catalogueOrder": 82,
      "branchId": "bridge-chiplet",
      "branchOrder": 2,
      "activityType": "design",
      "title": {
        "zh-TW": "配置矽橋岸線與雙節距接點",
        "en": "Plan bridge shorelines and dual-pitch contacts"
      },
      "summary": {
        "zh-TW": "以晶粒接點圖與橋接需求為起點，將密集互連集中於需要的晶粒邊緣。交付細密與較粗接點的區域配置，以岸線長度、接點對位與工具間距判讀結果；重點辨識密集接點擠入不可接合區。",
        "en": "Start with die bump maps and bridge connectivity needs; concentrate dense links along required die edges to obtain fine/coarse contact regions. Assess the result using shoreline, pad registration and tool-clearance checks, with particular attention to dense terminals placed in inaccessible regions."
      },
      "input": {
        "zh-TW": "晶粒接點圖與橋接需求",
        "en": "die bump maps and bridge connectivity needs"
      },
      "operation": {
        "zh-TW": "將密集互連集中於需要的晶粒邊緣",
        "en": "concentrate dense links along required die edges"
      },
      "output": {
        "zh-TW": "細密與較粗接點的區域配置",
        "en": "fine/coarse contact regions"
      },
      "qualityEvidence": {
        "zh-TW": "岸線長度、接點對位與工具間距",
        "en": "shoreline, pad registration and tool-clearance checks"
      },
      "failureMode": {
        "zh-TW": "密集接點擠入不可接合區",
        "en": "dense terminals placed in inaccessible regions"
      },
      "prerequisiteIds": [
        "B01"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "bridge",
      "sourceIds": [
        "intel-emib",
        "intel-design-flow"
      ],
      "sourceUrls": [
        "https://www.intel.com/content/dam/www/central-libraries/us/en/documents/2025-07/emib-product-brief.pdf",
        "https://blogs.sw.siemens.com/semiconductor-packaging/2024/08/12/user2user-2024-emib-based-advanced-packaging-flow-intel-foundry/"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "B03",
      "catalogueOrder": 83,
      "branchId": "bridge-chiplet",
      "branchOrder": 3,
      "activityType": "design",
      "title": {
        "zh-TW": "共同設計局部矽橋與有機基板",
        "en": "Co-design local bridges and the organic substrate"
      },
      "summary": {
        "zh-TW": "以岸線配置與電源訊號需求為起點，同時規劃橋內走線與基板連線。交付對齊的橋與基板設計資料，以網表與封裝設計規則對照判讀結果；重點辨識矽橋與基板版本不一致。",
        "en": "Start with shoreline placement and signal/power needs; co-design bridge routing and substrate connections to obtain matched bridge and substrate design data. Assess the result using connectivity and package-design-rule checks, with particular attention to mismatched bridge and substrate revisions."
      },
      "input": {
        "zh-TW": "岸線配置與電源訊號需求",
        "en": "shoreline placement and signal/power needs"
      },
      "operation": {
        "zh-TW": "同時規劃橋內走線與基板連線",
        "en": "co-design bridge routing and substrate connections"
      },
      "output": {
        "zh-TW": "對齊的橋與基板設計資料",
        "en": "matched bridge and substrate design data"
      },
      "qualityEvidence": {
        "zh-TW": "網表與封裝設計規則對照",
        "en": "connectivity and package-design-rule checks"
      },
      "failureMode": {
        "zh-TW": "矽橋與基板版本不一致",
        "en": "mismatched bridge and substrate revisions"
      },
      "prerequisiteIds": [
        "B02"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "bridge",
      "sourceIds": [
        "intel-design-flow",
        "intel-emib"
      ],
      "sourceUrls": [
        "https://blogs.sw.siemens.com/semiconductor-packaging/2024/08/12/user2user-2024-emib-based-advanced-packaging-flow-intel-foundry/",
        "https://www.intel.com/content/dam/www/central-libraries/us/en/documents/2025-07/emib-product-brief.pdf"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "B04",
      "catalogueOrder": 84,
      "branchId": "bridge-chiplet",
      "branchOrder": 4,
      "activityType": "manufacturing",
      "title": {
        "zh-TW": "製作基板中的局部橋接凹槽",
        "en": "Form local bridge cavities in the substrate"
      },
      "summary": {
        "zh-TW": "以核准的有機基板疊層為起點，形成適合局部矽橋的容納區。交付具有橋接容納區的基板，以凹槽深度、位置與潔淨度判讀結果；重點辨識凹槽不平或位置偏移。",
        "en": "Start with an approved organic-substrate build-up; form cavities for the selected local bridges to obtain a substrate with bridge cavities. Assess the result using cavity depth, position and cleanliness, with particular attention to nonplanar or mispositioned cavities."
      },
      "input": {
        "zh-TW": "核准的有機基板疊層",
        "en": "an approved organic-substrate build-up"
      },
      "operation": {
        "zh-TW": "形成適合局部矽橋的容納區",
        "en": "form cavities for the selected local bridges"
      },
      "output": {
        "zh-TW": "具有橋接容納區的基板",
        "en": "a substrate with bridge cavities"
      },
      "qualityEvidence": {
        "zh-TW": "凹槽深度、位置與潔淨度",
        "en": "cavity depth, position and cleanliness"
      },
      "failureMode": {
        "zh-TW": "凹槽不平或位置偏移",
        "en": "nonplanar or mispositioned cavities"
      },
      "prerequisiteIds": [
        "B03"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "bridge",
      "sourceIds": [
        "intel-emib"
      ],
      "sourceUrls": [
        "https://www.intel.com/content/dam/www/central-libraries/us/en/documents/2025-07/emib-product-brief.pdf"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "B05",
      "catalogueOrder": 85,
      "branchId": "bridge-chiplet",
      "branchOrder": 5,
      "activityType": "inspection_test",
      "title": {
        "zh-TW": "檢驗來料矽橋尺寸與連通性",
        "en": "Inspect incoming bridge dimensions and continuity"
      },
      "summary": {
        "zh-TW": "以外部製成的局部矽橋為起點，核對版次、尺寸及可測走線。交付已知狀態的可用矽橋，以尺寸、邊緣與電測記錄判讀結果；重點辨識有裂紋或錯版橋片進入基板。",
        "en": "Start with externally fabricated local silicon bridges; verify revision, dimensions and accessible routing to obtain bridges with known incoming condition. Assess the result using dimensional, edge and electrical records, with particular attention to cracked or wrong-revision bridges entering the substrate."
      },
      "input": {
        "zh-TW": "外部製成的局部矽橋",
        "en": "externally fabricated local silicon bridges"
      },
      "operation": {
        "zh-TW": "核對版次、尺寸及可測走線",
        "en": "verify revision, dimensions and accessible routing"
      },
      "output": {
        "zh-TW": "已知狀態的可用矽橋",
        "en": "bridges with known incoming condition"
      },
      "qualityEvidence": {
        "zh-TW": "尺寸、邊緣與電測記錄",
        "en": "dimensional, edge and electrical records"
      },
      "failureMode": {
        "zh-TW": "有裂紋或錯版橋片進入基板",
        "en": "cracked or wrong-revision bridges entering the substrate"
      },
      "prerequisiteIds": [
        "B04"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "bridge",
      "sourceIds": [
        "intel-emib",
        "kla-metrology"
      ],
      "sourceUrls": [
        "https://www.intel.com/content/dam/www/central-libraries/us/en/documents/2025-07/emib-product-brief.pdf",
        "https://ask.kla-tencor.com/products/packaging-manufacturing/wafer-inspection-and-metrology-for-advanced-packaging"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "B06",
      "catalogueOrder": 86,
      "branchId": "bridge-chiplet",
      "branchOrder": 6,
      "activityType": "manufacturing",
      "title": {
        "zh-TW": "點膠建立矽橋固定介面",
        "en": "Dispense bridge-attachment adhesive"
      },
      "summary": {
        "zh-TW": "以已檢驗凹槽與核准黏著材料為起點，定量佈膠並保留設計位置。交付可接納矽橋的固定介面，以膠量、覆蓋與污染檢查判讀結果；重點辨識溢膠污染微連接區。",
        "en": "Start with inspected cavities and qualified adhesive; dispense controlled adhesive at defined locations to obtain an adhesive interface ready for the bridge. Assess the result using volume, coverage and contamination checks, with particular attention to adhesive overflow contaminating microconnections."
      },
      "input": {
        "zh-TW": "已檢驗凹槽與核准黏著材料",
        "en": "inspected cavities and qualified adhesive"
      },
      "operation": {
        "zh-TW": "定量佈膠並保留設計位置",
        "en": "dispense controlled adhesive at defined locations"
      },
      "output": {
        "zh-TW": "可接納矽橋的固定介面",
        "en": "an adhesive interface ready for the bridge"
      },
      "qualityEvidence": {
        "zh-TW": "膠量、覆蓋與污染檢查",
        "en": "volume, coverage and contamination checks"
      },
      "failureMode": {
        "zh-TW": "溢膠污染微連接區",
        "en": "adhesive overflow contaminating microconnections"
      },
      "prerequisiteIds": [
        "B05"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "bridge",
      "sourceIds": [
        "intel-emib",
        "nordson-underfill"
      ],
      "sourceUrls": [
        "https://www.intel.com/content/dam/www/central-libraries/us/en/documents/2025-07/emib-product-brief.pdf",
        "https://www.nordson.com/en/divisions/electronics-solutions/your-process/fluid-types/underfill"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "B07",
      "catalogueOrder": 87,
      "branchId": "bridge-chiplet",
      "branchOrder": 7,
      "activityType": "manufacturing",
      "title": {
        "zh-TW": "將局部矽橋置入基板凹槽",
        "en": "Place local bridges into substrate cavities"
      },
      "summary": {
        "zh-TW": "以已點膠基板與可用矽橋為起點，精密放置並控制旋轉角度。交付已定位的局部矽橋，以位置、角度與上表面高度判讀結果；重點辨識橋片偏斜導致後續開孔偏移。",
        "en": "Start with adhesive-prepared substrates and accepted bridges; place bridges with controlled position and rotation to obtain positioned local silicon bridges. Assess the result using position, rotation and top-height checks, with particular attention to bridge tilt causing later via misregistration."
      },
      "input": {
        "zh-TW": "已點膠基板與可用矽橋",
        "en": "adhesive-prepared substrates and accepted bridges"
      },
      "operation": {
        "zh-TW": "精密放置並控制旋轉角度",
        "en": "place bridges with controlled position and rotation"
      },
      "output": {
        "zh-TW": "已定位的局部矽橋",
        "en": "positioned local silicon bridges"
      },
      "qualityEvidence": {
        "zh-TW": "位置、角度與上表面高度",
        "en": "position, rotation and top-height checks"
      },
      "failureMode": {
        "zh-TW": "橋片偏斜導致後續開孔偏移",
        "en": "bridge tilt causing later via misregistration"
      },
      "prerequisiteIds": [
        "B06"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "bridge",
      "sourceIds": [
        "intel-emib",
        "besi-tcb"
      ],
      "sourceUrls": [
        "https://www.intel.com/content/dam/www/central-libraries/us/en/documents/2025-07/emib-product-brief.pdf",
        "https://www.besi.com/products-technology/product-details/productgroup/thermo-compression-bonding/"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "B08",
      "catalogueOrder": 88,
      "branchId": "bridge-chiplet",
      "branchOrder": 8,
      "activityType": "manufacturing",
      "title": {
        "zh-TW": "固化橋接黏著並確認平坦度",
        "en": "Cure bridge adhesive and stabilize planarity"
      },
      "summary": {
        "zh-TW": "以已置入的橋片與黏著介面為起點，完成相容固化並穩定橋片高度。交付可進行增層的固定橋片，以固化履歷與橋片高度圖判讀結果；重點辨識固化收縮造成橋片移動。",
        "en": "Start with placed bridges and adhesive interfaces; cure compatibly and stabilize bridge height to obtain fixed bridges ready for build-up. Assess the result using cure history and bridge-height maps, with particular attention to cure shrinkage shifting the bridge."
      },
      "input": {
        "zh-TW": "已置入的橋片與黏著介面",
        "en": "placed bridges and adhesive interfaces"
      },
      "operation": {
        "zh-TW": "完成相容固化並穩定橋片高度",
        "en": "cure compatibly and stabilize bridge height"
      },
      "output": {
        "zh-TW": "可進行增層的固定橋片",
        "en": "fixed bridges ready for build-up"
      },
      "qualityEvidence": {
        "zh-TW": "固化履歷與橋片高度圖",
        "en": "cure history and bridge-height maps"
      },
      "failureMode": {
        "zh-TW": "固化收縮造成橋片移動",
        "en": "cure shrinkage shifting the bridge"
      },
      "prerequisiteIds": [
        "B07"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "bridge",
      "sourceIds": [
        "intel-emib",
        "ase-thermal"
      ],
      "sourceUrls": [
        "https://www.intel.com/content/dam/www/central-libraries/us/en/documents/2025-07/emib-product-brief.pdf",
        "https://ase.aseglobal.com/lab-services/stress-and-thermal-lab/"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "B09",
      "catalogueOrder": 89,
      "branchId": "bridge-chiplet",
      "branchOrder": 9,
      "activityType": "manufacturing",
      "title": {
        "zh-TW": "覆蓋橋片周圍介電增層",
        "en": "Build dielectric layers around the bridge"
      },
      "summary": {
        "zh-TW": "以固定橋片的有機基板為起點，形成後續互連需要的介電增層。交付包覆局部橋片的介電結構，以覆蓋性、空洞與厚度判讀結果；重點辨識橋片邊緣空洞或介電裂紋。",
        "en": "Start with organic substrates with fixed bridges; form dielectric build-up for later interconnects to obtain dielectric structures surrounding local bridges. Assess the result using coverage, void and thickness checks, with particular attention to voids or cracks around bridge edges."
      },
      "input": {
        "zh-TW": "固定橋片的有機基板",
        "en": "organic substrates with fixed bridges"
      },
      "operation": {
        "zh-TW": "形成後續互連需要的介電增層",
        "en": "form dielectric build-up for later interconnects"
      },
      "output": {
        "zh-TW": "包覆局部橋片的介電結構",
        "en": "dielectric structures surrounding local bridges"
      },
      "qualityEvidence": {
        "zh-TW": "覆蓋性、空洞與厚度",
        "en": "coverage, void and thickness checks"
      },
      "failureMode": {
        "zh-TW": "橋片邊緣空洞或介電裂紋",
        "en": "voids or cracks around bridge edges"
      },
      "prerequisiteIds": [
        "B08"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "bridge",
      "sourceIds": [
        "intel-emib",
        "kla-deposition"
      ],
      "sourceUrls": [
        "https://www.intel.com/content/dam/www/central-libraries/us/en/documents/2025-07/emib-product-brief.pdf",
        "https://www.spts.com/products/packaging-manufacturing/wafer-processing-systems-for-advanced-packaging"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "B10",
      "catalogueOrder": 90,
      "branchId": "bridge-chiplet",
      "branchOrder": 10,
      "activityType": "manufacturing",
      "title": {
        "zh-TW": "開出通往橋片端點的微孔",
        "en": "Open microvias to bridge terminals"
      },
      "summary": {
        "zh-TW": "以橋片上方介電增層為起點，以適用開孔製程連到橋片接點。交付露出局部橋片端點的微孔，以微孔位置、孔底與深度判讀結果；重點辨識孔偏移或未穿透介電層。",
        "en": "Start with dielectric build-up above bridge terminals; open suitable vias to the bridge contacts to obtain microvias exposing bridge terminals. Assess the result using via placement, bottoms and depth, with particular attention to misaligned or incompletely opened vias."
      },
      "input": {
        "zh-TW": "橋片上方介電增層",
        "en": "dielectric build-up above bridge terminals"
      },
      "operation": {
        "zh-TW": "以適用開孔製程連到橋片接點",
        "en": "open suitable vias to the bridge contacts"
      },
      "output": {
        "zh-TW": "露出局部橋片端點的微孔",
        "en": "microvias exposing bridge terminals"
      },
      "qualityEvidence": {
        "zh-TW": "微孔位置、孔底與深度",
        "en": "via placement, bottoms and depth"
      },
      "failureMode": {
        "zh-TW": "孔偏移或未穿透介電層",
        "en": "misaligned or incompletely opened vias"
      },
      "prerequisiteIds": [
        "B09"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "bridge",
      "sourceIds": [
        "intel-emib",
        "kla-metrology"
      ],
      "sourceUrls": [
        "https://www.intel.com/content/dam/www/central-libraries/us/en/documents/2025-07/emib-product-brief.pdf",
        "https://ask.kla-tencor.com/products/packaging-manufacturing/wafer-inspection-and-metrology-for-advanced-packaging"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "B11",
      "catalogueOrder": 91,
      "branchId": "bridge-chiplet",
      "branchOrder": 11,
      "activityType": "manufacturing",
      "title": {
        "zh-TW": "去除微孔殘渣並準備金屬化",
        "en": "Remove microvia residue for metallization"
      },
      "summary": {
        "zh-TW": "以已開出的基板微孔為起點，清除孔壁與孔底殘留。交付可可靠金屬化的微孔，以孔底潔淨與表面狀態判讀結果；重點辨識孔底殘渣造成間歇性接觸。",
        "en": "Start with opened substrate microvias; remove sidewall and bottom residue to obtain microvias ready for reliable metallization. Assess the result using via-bottom cleanliness and surface condition, with particular attention to bottom residue causing intermittent contacts."
      },
      "input": {
        "zh-TW": "已開出的基板微孔",
        "en": "opened substrate microvias"
      },
      "operation": {
        "zh-TW": "清除孔壁與孔底殘留",
        "en": "remove sidewall and bottom residue"
      },
      "output": {
        "zh-TW": "可可靠金屬化的微孔",
        "en": "microvias ready for reliable metallization"
      },
      "qualityEvidence": {
        "zh-TW": "孔底潔淨與表面狀態",
        "en": "via-bottom cleanliness and surface condition"
      },
      "failureMode": {
        "zh-TW": "孔底殘渣造成間歇性接觸",
        "en": "bottom residue causing intermittent contacts"
      },
      "prerequisiteIds": [
        "B10"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "bridge",
      "sourceIds": [
        "intel-emib",
        "lam-flow"
      ],
      "sourceUrls": [
        "https://www.intel.com/content/dam/www/central-libraries/us/en/documents/2025-07/emib-product-brief.pdf",
        "https://newsroom.lamresearch.com/the-ai-revolution-relies-on-advanced-packaging"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "B12",
      "catalogueOrder": 92,
      "branchId": "bridge-chiplet",
      "branchOrder": 12,
      "activityType": "manufacturing",
      "title": {
        "zh-TW": "金屬化橋片微孔與增層連線",
        "en": "Metallize bridge microvias and build-up links"
      },
      "summary": {
        "zh-TW": "以已清潔微孔與線路窗口為起點，形成連續的微孔及線路金屬。交付橋片連到基板表面的導電路徑，以填孔完整性與導通測試判讀結果；重點辨識微孔鍍層空洞或頸縮。",
        "en": "Start with clean microvias and routing openings; form continuous via and routing metallization to obtain conductive paths from bridge to substrate surface. Assess the result using via-fill integrity and continuity tests, with particular attention to voided or necked microvia metal."
      },
      "input": {
        "zh-TW": "已清潔微孔與線路窗口",
        "en": "clean microvias and routing openings"
      },
      "operation": {
        "zh-TW": "形成連續的微孔及線路金屬",
        "en": "form continuous via and routing metallization"
      },
      "output": {
        "zh-TW": "橋片連到基板表面的導電路徑",
        "en": "conductive paths from bridge to substrate surface"
      },
      "qualityEvidence": {
        "zh-TW": "填孔完整性與導通測試",
        "en": "via-fill integrity and continuity tests"
      },
      "failureMode": {
        "zh-TW": "微孔鍍層空洞或頸縮",
        "en": "voided or necked microvia metal"
      },
      "prerequisiteIds": [
        "B11"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "bridge",
      "sourceIds": [
        "intel-emib",
        "lam-electrofill"
      ],
      "sourceUrls": [
        "https://www.intel.com/content/dam/www/central-libraries/us/en/documents/2025-07/emib-product-brief.pdf",
        "https://www.lamresearch.com/product/sabre-3d/"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "B13",
      "catalogueOrder": 93,
      "branchId": "bridge-chiplet",
      "branchOrder": 13,
      "activityType": "manufacturing",
      "title": {
        "zh-TW": "圖案化細密橋接端線路",
        "en": "Pattern fine bridge-side routing"
      },
      "summary": {
        "zh-TW": "以已金屬化的橋接增層為起點，定義密集接點區的線路與隔離。交付可連接細節距晶粒的端線路，以線寬、間距與橋片套準判讀結果；重點辨識細線橋接或局部斷路。",
        "en": "Start with metallized bridge build-up layers; define routing and isolation in dense contact regions to obtain routing for fine-pitch die attachment. Assess the result using line/space and bridge-overlay checks, with particular attention to fine-line shorts or local opens."
      },
      "input": {
        "zh-TW": "已金屬化的橋接增層",
        "en": "metallized bridge build-up layers"
      },
      "operation": {
        "zh-TW": "定義密集接點區的線路與隔離",
        "en": "define routing and isolation in dense contact regions"
      },
      "output": {
        "zh-TW": "可連接細節距晶粒的端線路",
        "en": "routing for fine-pitch die attachment"
      },
      "qualityEvidence": {
        "zh-TW": "線寬、間距與橋片套準",
        "en": "line/space and bridge-overlay checks"
      },
      "failureMode": {
        "zh-TW": "細線橋接或局部斷路",
        "en": "fine-line shorts or local opens"
      },
      "prerequisiteIds": [
        "B12"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "bridge",
      "sourceIds": [
        "intel-emib",
        "kla-metrology"
      ],
      "sourceUrls": [
        "https://www.intel.com/content/dam/www/central-libraries/us/en/documents/2025-07/emib-product-brief.pdf",
        "https://ask.kla-tencor.com/products/packaging-manufacturing/wafer-inspection-and-metrology-for-advanced-packaging"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "B14",
      "catalogueOrder": 94,
      "branchId": "bridge-chiplet",
      "branchOrder": 14,
      "activityType": "manufacturing",
      "title": {
        "zh-TW": "完成細粗雙節距接合墊",
        "en": "Finish fine- and coarse-pitch joining pads"
      },
      "summary": {
        "zh-TW": "以橋接細線與有機基板走線為起點，依不同接點區完成表面接合金屬。交付雙節距接合表面，以墊高、表面金屬與共面度判讀結果；重點辨識兩種接點區的高度不匹配。",
        "en": "Start with bridge fine routing and organic-substrate routes; finish joining metallurgy for each contact region to obtain a dual-pitch joining surface. Assess the result using pad height, metallurgy and coplanarity, with particular attention to height mismatch between contact regions."
      },
      "input": {
        "zh-TW": "橋接細線與有機基板走線",
        "en": "bridge fine routing and organic-substrate routes"
      },
      "operation": {
        "zh-TW": "依不同接點區完成表面接合金屬",
        "en": "finish joining metallurgy for each contact region"
      },
      "output": {
        "zh-TW": "雙節距接合表面",
        "en": "a dual-pitch joining surface"
      },
      "qualityEvidence": {
        "zh-TW": "墊高、表面金屬與共面度",
        "en": "pad height, metallurgy and coplanarity"
      },
      "failureMode": {
        "zh-TW": "兩種接點區的高度不匹配",
        "en": "height mismatch between contact regions"
      },
      "prerequisiteIds": [
        "B13"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "bridge",
      "sourceIds": [
        "intel-emib",
        "amkor-bumping"
      ],
      "sourceUrls": [
        "https://www.intel.com/content/dam/www/central-libraries/us/en/documents/2025-07/emib-product-brief.pdf",
        "https://amkor.com/services/wafer-bumping/"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "B15",
      "catalogueOrder": 95,
      "branchId": "bridge-chiplet",
      "branchOrder": 15,
      "activityType": "inspection_test",
      "title": {
        "zh-TW": "檢驗嵌橋基板互連",
        "en": "Inspect embedded-bridge substrate interconnects"
      },
      "summary": {
        "zh-TW": "以完成接合面的嵌橋基板為起點，驗證橋內、微孔與基板網路。交付可貼裝晶粒的良品基板圖，以連通、絕緣與形貌量測判讀結果；重點辨識橋內良好但轉接微孔失效。",
        "en": "Start with embedded-bridge substrates with finished contacts; verify bridge, via and substrate networks to obtain known-good substrate sites for die attachment. Assess the result using continuity, isolation and topography measurements, with particular attention to good bridge routing with failed transition vias."
      },
      "input": {
        "zh-TW": "完成接合面的嵌橋基板",
        "en": "embedded-bridge substrates with finished contacts"
      },
      "operation": {
        "zh-TW": "驗證橋內、微孔與基板網路",
        "en": "verify bridge, via and substrate networks"
      },
      "output": {
        "zh-TW": "可貼裝晶粒的良品基板圖",
        "en": "known-good substrate sites for die attachment"
      },
      "qualityEvidence": {
        "zh-TW": "連通、絕緣與形貌量測",
        "en": "continuity, isolation and topography measurements"
      },
      "failureMode": {
        "zh-TW": "橋內良好但轉接微孔失效",
        "en": "good bridge routing with failed transition vias"
      },
      "prerequisiteIds": [
        "B14"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "bridge",
      "sourceIds": [
        "intel-emib",
        "kla-metrology"
      ],
      "sourceUrls": [
        "https://www.intel.com/content/dam/www/central-libraries/us/en/documents/2025-07/emib-product-brief.pdf",
        "https://ask.kla-tencor.com/products/packaging-manufacturing/wafer-inspection-and-metrology-for-advanced-packaging"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "B16",
      "catalogueOrder": 96,
      "branchId": "bridge-chiplet",
      "branchOrder": 16,
      "activityType": "manufacturing",
      "title": {
        "zh-TW": "準備晶粒的雙節距凸塊",
        "en": "Prepare dual-pitch die bumps"
      },
      "summary": {
        "zh-TW": "以相容晶粒與核准凸塊規格為起點，製作適合岸線與核心區的凸塊。交付可匹配嵌橋基板的晶粒端點，以凸塊高度與分區共面度判讀結果；重點辨識不同區域接合窗口無法同時滿足。",
        "en": "Start with compatible dies and approved bump specifications; form bumps for shoreline and core regions to obtain die terminals matching the bridge substrate. Assess the result using bump height and regional coplanarity, with particular attention to incompatible joining windows across regions."
      },
      "input": {
        "zh-TW": "相容晶粒與核准凸塊規格",
        "en": "compatible dies and approved bump specifications"
      },
      "operation": {
        "zh-TW": "製作適合岸線與核心區的凸塊",
        "en": "form bumps for shoreline and core regions"
      },
      "output": {
        "zh-TW": "可匹配嵌橋基板的晶粒端點",
        "en": "die terminals matching the bridge substrate"
      },
      "qualityEvidence": {
        "zh-TW": "凸塊高度與分區共面度",
        "en": "bump height and regional coplanarity"
      },
      "failureMode": {
        "zh-TW": "不同區域接合窗口無法同時滿足",
        "en": "incompatible joining windows across regions"
      },
      "prerequisiteIds": [
        "B15"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "bridge",
      "sourceIds": [
        "intel-emib",
        "amkor-bumping"
      ],
      "sourceUrls": [
        "https://www.intel.com/content/dam/www/central-libraries/us/en/documents/2025-07/emib-product-brief.pdf",
        "https://amkor.com/services/wafer-bumping/"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "B17",
      "catalogueOrder": 97,
      "branchId": "bridge-chiplet",
      "branchOrder": 17,
      "activityType": "inspection_test",
      "title": {
        "zh-TW": "核對小晶片KGD與介面版本",
        "en": "Verify chiplet KGD and interface revisions"
      },
      "summary": {
        "zh-TW": "以多來源晶粒與測試履歷為起點，核對功能分選及互連相容性。交付可配對的晶粒組合，以KGD紀錄、版本與測試覆蓋判讀結果；重點辨識電性良品卻無法跨晶粒協作。",
        "en": "Start with multi-source dies and test histories; check functional bins and interface compatibility to obtain compatible die combinations. Assess the result using KGD records, revisions and test coverage, with particular attention to individually good dies failing to interoperate."
      },
      "input": {
        "zh-TW": "多來源晶粒與測試履歷",
        "en": "multi-source dies and test histories"
      },
      "operation": {
        "zh-TW": "核對功能分選及互連相容性",
        "en": "check functional bins and interface compatibility"
      },
      "output": {
        "zh-TW": "可配對的晶粒組合",
        "en": "compatible die combinations"
      },
      "qualityEvidence": {
        "zh-TW": "KGD紀錄、版本與測試覆蓋",
        "en": "KGD records, revisions and test coverage"
      },
      "failureMode": {
        "zh-TW": "電性良品卻無法跨晶粒協作",
        "en": "individually good dies failing to interoperate"
      },
      "prerequisiteIds": [
        "B16"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "bridge",
      "sourceIds": [
        "ucie",
        "ieee-test"
      ],
      "sourceUrls": [
        "https://www.uciexpress.org/specifications",
        "https://cmte.ieee.org/eps-test/wp-content/uploads/sites/132/2022/01/IEEE_EPS_Test_Het_Int_Product_Testability_BKM_Final_v1_0-1-14-22-1.pdf"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "B18",
      "catalogueOrder": 98,
      "branchId": "bridge-chiplet",
      "branchOrder": 18,
      "activityType": "manufacturing",
      "title": {
        "zh-TW": "跨局部矽橋接合小晶片",
        "en": "Join chiplets across local bridges"
      },
      "summary": {
        "zh-TW": "以良品嵌橋基板與配對晶粒為起點，對準兩種接點區並完成接合。交付具有局部橋接的晶粒組件，以貼裝偏差與區域接點連通判讀結果；重點辨識細節距區接好但粗節距區浮接。",
        "en": "Start with good bridge substrates and matched dies; align both contact regions and complete joining to obtain a die assembly connected through local bridges. Assess the result using placement error and regional contact continuity, with particular attention to fine contacts joining while coarse contacts remain open."
      },
      "input": {
        "zh-TW": "良品嵌橋基板與配對晶粒",
        "en": "good bridge substrates and matched dies"
      },
      "operation": {
        "zh-TW": "對準兩種接點區並完成接合",
        "en": "align both contact regions and complete joining"
      },
      "output": {
        "zh-TW": "具有局部橋接的晶粒組件",
        "en": "a die assembly connected through local bridges"
      },
      "qualityEvidence": {
        "zh-TW": "貼裝偏差與區域接點連通",
        "en": "placement error and regional contact continuity"
      },
      "failureMode": {
        "zh-TW": "細節距區接好但粗節距區浮接",
        "en": "fine contacts joining while coarse contacts remain open"
      },
      "prerequisiteIds": [
        "B17"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "bridge",
      "sourceIds": [
        "besi-tcb",
        "intel-emib"
      ],
      "sourceUrls": [
        "https://www.besi.com/products-technology/product-details/productgroup/thermo-compression-bonding/",
        "https://www.intel.com/content/dam/www/central-libraries/us/en/documents/2025-07/emib-product-brief.pdf"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "B19",
      "catalogueOrder": 99,
      "branchId": "bridge-chiplet",
      "branchOrder": 19,
      "activityType": "manufacturing",
      "title": {
        "zh-TW": "底填並固化嵌橋晶粒組件",
        "en": "Underfill and cure the bridge assembly"
      },
      "summary": {
        "zh-TW": "以已接合的小晶片基板為起點，控制狹縫流動並保護細粗接點。交付受機械保護的橋接組件，以填膠空洞與熱機相容性判讀結果；重點辨識細粗節距交界困住空氣。",
        "en": "Start with joined chiplets on the bridge substrate; control gap filling around fine and coarse joints to obtain a mechanically reinforced bridge assembly. Assess the result using underfill voids and thermo-mechanical compatibility, with particular attention to air trapped at transitions between contact regions."
      },
      "input": {
        "zh-TW": "已接合的小晶片基板",
        "en": "joined chiplets on the bridge substrate"
      },
      "operation": {
        "zh-TW": "控制狹縫流動並保護細粗接點",
        "en": "control gap filling around fine and coarse joints"
      },
      "output": {
        "zh-TW": "受機械保護的橋接組件",
        "en": "a mechanically reinforced bridge assembly"
      },
      "qualityEvidence": {
        "zh-TW": "填膠空洞與熱機相容性",
        "en": "underfill voids and thermo-mechanical compatibility"
      },
      "failureMode": {
        "zh-TW": "細粗節距交界困住空氣",
        "en": "air trapped at transitions between contact regions"
      },
      "prerequisiteIds": [
        "B18"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "bridge",
      "sourceIds": [
        "nordson-underfill",
        "ase-thermal"
      ],
      "sourceUrls": [
        "https://www.nordson.com/en/divisions/electronics-solutions/your-process/fluid-types/underfill",
        "https://ase.aseglobal.com/lab-services/stress-and-thermal-lab/"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "B20",
      "catalogueOrder": 100,
      "branchId": "bridge-chiplet",
      "branchOrder": 20,
      "activityType": "inspection_test",
      "title": {
        "zh-TW": "驗證小晶片鏈路與管理存取",
        "en": "Verify chiplet links and management access"
      },
      "summary": {
        "zh-TW": "以完成接合的橋接組件為起點，測試鏈路訓練與可用管理通道。交付可辨識互連健康狀態的測試紀錄，以協定一致性、錯誤統計與可診斷性判讀結果；重點辨識連通通過但鏈路無法可靠訓練。",
        "en": "Start with joined bridge assemblies; test link training and available management channels to obtain link-health and access test records. Assess the result using protocol consistency, error statistics and diagnosability, with particular attention to continuity passing while link training is unreliable."
      },
      "input": {
        "zh-TW": "完成接合的橋接組件",
        "en": "joined bridge assemblies"
      },
      "operation": {
        "zh-TW": "測試鏈路訓練與可用管理通道",
        "en": "test link training and available management channels"
      },
      "output": {
        "zh-TW": "可辨識互連健康狀態的測試紀錄",
        "en": "link-health and access test records"
      },
      "qualityEvidence": {
        "zh-TW": "協定一致性、錯誤統計與可診斷性",
        "en": "protocol consistency, error statistics and diagnosability"
      },
      "failureMode": {
        "zh-TW": "連通通過但鏈路無法可靠訓練",
        "en": "continuity passing while link training is unreliable"
      },
      "prerequisiteIds": [
        "B19"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "bridge",
      "sourceIds": [
        "ucie",
        "intel-packaging"
      ],
      "sourceUrls": [
        "https://www.uciexpress.org/specifications",
        "https://www.intel.com/content/www/us/en/foundry/packaging.htm"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "V01",
      "catalogueOrder": 101,
      "branchId": "finish-test",
      "branchOrder": 1,
      "activityType": "design",
      "title": {
        "zh-TW": "確認終封裝交接與適用工序",
        "en": "Confirm final-package handoff and applicability"
      },
      "summary": {
        "zh-TW": "以任一分支的放行模組或晶圓為起點，核對切割、端點與基板是否已完成。交付不重複加工的終封裝路線，以分支交接記錄與跳站理由判讀結果；重點辨識對已在基板上的橋接組件再次貼板。",
        "en": "Start with released modules or wafers from one architecture branch; review completed singulation, termination and substrate work to obtain a final-integration route without duplicate operations. Assess the result using handoff records and justified bypasses, with particular attention to reattaching bridge assemblies already on their substrate."
      },
      "input": {
        "zh-TW": "任一分支的放行模組或晶圓",
        "en": "released modules or wafers from one architecture branch"
      },
      "operation": {
        "zh-TW": "核對切割、端點與基板是否已完成",
        "en": "review completed singulation, termination and substrate work"
      },
      "output": {
        "zh-TW": "不重複加工的終封裝路線",
        "en": "a final-integration route without duplicate operations"
      },
      "qualityEvidence": {
        "zh-TW": "分支交接記錄與跳站理由",
        "en": "handoff records and justified bypasses"
      },
      "failureMode": {
        "zh-TW": "對已在基板上的橋接組件再次貼板",
        "en": "reattaching bridge assemblies already on their substrate"
      },
      "prerequisiteIds": [
        "C20"
      ],
      "prerequisiteAnyOf": [
        "I20",
        "F20",
        "H20",
        "B20"
      ],
      "overviewTourId": "thermal",
      "sourceIds": [
        "amkor-chiplets",
        "amkor-tsv-sheet"
      ],
      "sourceUrls": [
        "https://amkormarcomexternal.blob.core.windows.net/amkordotcom/wp-content/uploads/2024/03/Readying-the-supply-chain-for-chiplets-and-heterogeneous-integration_EN.pdf",
        "https://amkor.com/kr/wp-content/uploads/2018/02/TSV_TS107.pdf"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "V02",
      "catalogueOrder": 102,
      "branchId": "finish-test",
      "branchOrder": 2,
      "activityType": "manufacturing",
      "title": {
        "zh-TW": "將獨立模組接合至封裝基板",
        "en": "Join standalone modules to the package substrate"
      },
      "summary": {
        "zh-TW": "以需要貼板的模組與良品基板為起點，依選定端點結構對位並接合。交付模組在基板上的組件，以模組位移與可測接點判讀結果；重點辨識大型模組翹曲造成接點未接合。",
        "en": "Start with standalone modules requiring substrate attachment; align and join the selected terminal structure to obtain a module-on-substrate assembly. Assess the result using module placement and accessible joint tests, with particular attention to large-module warpage causing non-joints."
      },
      "input": {
        "zh-TW": "需要貼板的模組與良品基板",
        "en": "standalone modules requiring substrate attachment"
      },
      "operation": {
        "zh-TW": "依選定端點結構對位並接合",
        "en": "align and join the selected terminal structure"
      },
      "output": {
        "zh-TW": "模組在基板上的組件",
        "en": "a module-on-substrate assembly"
      },
      "qualityEvidence": {
        "zh-TW": "模組位移與可測接點",
        "en": "module placement and accessible joint tests"
      },
      "failureMode": {
        "zh-TW": "大型模組翹曲造成接點未接合",
        "en": "large-module warpage causing non-joints"
      },
      "prerequisiteIds": [
        "V01"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "thermal",
      "sourceIds": [
        "amkor-tsv-sheet",
        "besi-tcb"
      ],
      "sourceUrls": [
        "https://amkor.com/kr/wp-content/uploads/2018/02/TSV_TS107.pdf",
        "https://www.besi.com/products-technology/product-details/productgroup/thermo-compression-bonding/"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "僅在前段輸出尚需貼到封裝基板時執行；B分支通常跳過，已完成此層接合的產品不得重複加工。",
        "en": "Only for upstream modules that still require package-substrate attachment. The B branch normally bypasses these steps."
      }
    },
    {
      "id": "V03",
      "catalogueOrder": 103,
      "branchId": "finish-test",
      "branchOrder": 3,
      "activityType": "manufacturing",
      "title": {
        "zh-TW": "保護模組與基板之間的接點",
        "en": "Reinforce module-to-substrate joints"
      },
      "summary": {
        "zh-TW": "以已貼板模組與核准底填材料為起點，填充模組下方間隙並固化。交付受保護的模組底部接合區，以膠流、空洞及固化結果判讀結果；重點辨識長流路造成未填滿區。",
        "en": "Start with substrate-attached modules and qualified underfill; fill the module-to-substrate gap and cure to obtain reinforced module-to-substrate joints. Assess the result using flow, void and cure evidence, with particular attention to long flow paths leaving unfilled regions."
      },
      "input": {
        "zh-TW": "已貼板模組與核准底填材料",
        "en": "substrate-attached modules and qualified underfill"
      },
      "operation": {
        "zh-TW": "填充模組下方間隙並固化",
        "en": "fill the module-to-substrate gap and cure"
      },
      "output": {
        "zh-TW": "受保護的模組底部接合區",
        "en": "reinforced module-to-substrate joints"
      },
      "qualityEvidence": {
        "zh-TW": "膠流、空洞及固化結果",
        "en": "flow, void and cure evidence"
      },
      "failureMode": {
        "zh-TW": "長流路造成未填滿區",
        "en": "long flow paths leaving unfilled regions"
      },
      "prerequisiteIds": [
        "V02"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "thermal",
      "sourceIds": [
        "nordson-underfill",
        "ase-fa"
      ],
      "sourceUrls": [
        "https://www.nordson.com/en/divisions/electronics-solutions/your-process/fluid-types/underfill",
        "https://ase.aseglobal.com/lab-services/failure-analysis-lab/"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "僅在前段輸出尚需貼到封裝基板時執行；B分支通常跳過，已完成此層接合的產品不得重複加工。",
        "en": "Only for upstream modules that still require package-substrate attachment. The B branch normally bypasses these steps."
      }
    },
    {
      "id": "V04",
      "catalogueOrder": 104,
      "branchId": "finish-test",
      "branchOrder": 4,
      "activityType": "manufacturing",
      "title": {
        "zh-TW": "形成板端焊球與外部接點",
        "en": "Form board-side balls and external terminals"
      },
      "summary": {
        "zh-TW": "以完成內部互連的封裝基板為起點，依產品規格形成板端接合結構。交付可連接主板的封裝端點，以缺球、橋接與共面度量測判讀結果；重點辨識外部接點缺失或高度離群。",
        "en": "Start with package substrates with completed internal interconnects; form board-level terminals to the product specification to obtain package terminals for board attachment. Assess the result using missing-ball, bridge and coplanarity checks, with particular attention to missing or outlying external terminals."
      },
      "input": {
        "zh-TW": "完成內部互連的封裝基板",
        "en": "package substrates with completed internal interconnects"
      },
      "operation": {
        "zh-TW": "依產品規格形成板端接合結構",
        "en": "form board-level terminals to the product specification"
      },
      "output": {
        "zh-TW": "可連接主板的封裝端點",
        "en": "package terminals for board attachment"
      },
      "qualityEvidence": {
        "zh-TW": "缺球、橋接與共面度量測",
        "en": "missing-ball, bridge and coplanarity checks"
      },
      "failureMode": {
        "zh-TW": "外部接點缺失或高度離群",
        "en": "missing or outlying external terminals"
      },
      "prerequisiteIds": [
        "V01"
      ],
      "prerequisiteAnyOf": [
        "V03",
        "B20"
      ],
      "overviewTourId": "thermal",
      "sourceIds": [
        "amkor-bumping",
        "kla-metrology"
      ],
      "sourceUrls": [
        "https://amkor.com/services/wafer-bumping/",
        "https://ask.kla-tencor.com/products/packaging-manufacturing/wafer-inspection-and-metrology-for-advanced-packaging"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      },
      "flowRelation": "architecture_conditioned_join"
    },
    {
      "id": "V05",
      "catalogueOrder": 105,
      "branchId": "finish-test",
      "branchOrder": 5,
      "activityType": "manufacturing",
      "title": {
        "zh-TW": "安裝補強框與機械支撐",
        "en": "Attach stiffeners and mechanical supports"
      },
      "summary": {
        "zh-TW": "以需要補強的封裝與設計圖為起點，定位並固定設計要求的補強件。交付具受控機械邊界的封裝，以框位、平坦度與黏著證據判讀結果；重點辨識補強件反而引入局部應力。",
        "en": "Start with packages requiring reinforcement and their drawings; position and fix the required reinforcement to obtain a package with controlled mechanical support. Assess the result using frame placement, planarity and adhesion evidence, with particular attention to reinforcement introducing local stress."
      },
      "input": {
        "zh-TW": "需要補強的封裝與設計圖",
        "en": "packages requiring reinforcement and their drawings"
      },
      "operation": {
        "zh-TW": "定位並固定設計要求的補強件",
        "en": "position and fix the required reinforcement"
      },
      "output": {
        "zh-TW": "具受控機械邊界的封裝",
        "en": "a package with controlled mechanical support"
      },
      "qualityEvidence": {
        "zh-TW": "框位、平坦度與黏著證據",
        "en": "frame placement, planarity and adhesion evidence"
      },
      "failureMode": {
        "zh-TW": "補強件反而引入局部應力",
        "en": "reinforcement introducing local stress"
      },
      "prerequisiteIds": [
        "V04"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "thermal",
      "sourceIds": [
        "amkor-tsv-sheet",
        "ase-thermal"
      ],
      "sourceUrls": [
        "https://amkor.com/kr/wp-content/uploads/2018/02/TSV_TS107.pdf",
        "https://ase.aseglobal.com/lab-services/stress-and-thermal-lab/"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "依成品機構與冷卻設計選用；無補強框、無蓋或不同冷卻方案不必強制加裝。",
        "en": "Selected by the mechanical/cooling design; stiffener-free, lidless or different cooling designs do not require this hardware."
      }
    },
    {
      "id": "V06",
      "catalogueOrder": 106,
      "branchId": "finish-test",
      "branchOrder": 6,
      "activityType": "manufacturing",
      "title": {
        "zh-TW": "塗佈導熱介面材料",
        "en": "Apply thermal interface material"
      },
      "summary": {
        "zh-TW": "以晶粒背面、散熱面與核准TIM為起點，定量佈料並控制界面覆蓋。交付可組裝的導熱介面，以膠量、覆蓋與界面厚度判讀結果；重點辨識氣泡或過厚界面增加熱阻。",
        "en": "Start with die backsides, cooling surfaces and qualified TIM; dispense controlled material coverage to obtain a thermal interface ready for assembly. Assess the result using volume, coverage and bond-line thickness, with particular attention to voids or thick bond lines increasing thermal resistance."
      },
      "input": {
        "zh-TW": "晶粒背面、散熱面與核准TIM",
        "en": "die backsides, cooling surfaces and qualified TIM"
      },
      "operation": {
        "zh-TW": "定量佈料並控制界面覆蓋",
        "en": "dispense controlled material coverage"
      },
      "output": {
        "zh-TW": "可組裝的導熱介面",
        "en": "a thermal interface ready for assembly"
      },
      "qualityEvidence": {
        "zh-TW": "膠量、覆蓋與界面厚度",
        "en": "volume, coverage and bond-line thickness"
      },
      "failureMode": {
        "zh-TW": "氣泡或過厚界面增加熱阻",
        "en": "voids or thick bond lines increasing thermal resistance"
      },
      "prerequisiteIds": [
        "V05"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "thermal",
      "sourceIds": [
        "nordson-tim",
        "ase-thermal"
      ],
      "sourceUrls": [
        "https://www.nordson.com/en/divisions/electronics-solutions/your-process/industries/pcb-and-smt-assembly",
        "https://ase.aseglobal.com/lab-services/stress-and-thermal-lab/"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "V07",
      "catalogueOrder": 107,
      "branchId": "finish-test",
      "branchOrder": 7,
      "activityType": "manufacturing",
      "title": {
        "zh-TW": "裝配均熱蓋並完成固定",
        "en": "Attach and secure the heat spreader"
      },
      "summary": {
        "zh-TW": "以已塗TIM的封裝與均熱蓋為起點，控制壓合、位置與相容固化。交付具有均熱蓋的封裝，以蓋高、傾斜與接觸證據判讀結果；重點辨識蓋子偏斜造成不均勻熱接觸。",
        "en": "Start with TIM-prepared packages and heat spreaders; control placement, compression and compatible curing to obtain a lidded package. Assess the result using lid height, tilt and contact evidence, with particular attention to lid tilt causing uneven thermal contact."
      },
      "input": {
        "zh-TW": "已塗TIM的封裝與均熱蓋",
        "en": "TIM-prepared packages and heat spreaders"
      },
      "operation": {
        "zh-TW": "控制壓合、位置與相容固化",
        "en": "control placement, compression and compatible curing"
      },
      "output": {
        "zh-TW": "具有均熱蓋的封裝",
        "en": "a lidded package"
      },
      "qualityEvidence": {
        "zh-TW": "蓋高、傾斜與接觸證據",
        "en": "lid height, tilt and contact evidence"
      },
      "failureMode": {
        "zh-TW": "蓋子偏斜造成不均勻熱接觸",
        "en": "lid tilt causing uneven thermal contact"
      },
      "prerequisiteIds": [
        "V06"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "thermal",
      "sourceIds": [
        "amkor-tsv-sheet",
        "nordson-tim"
      ],
      "sourceUrls": [
        "https://amkor.com/kr/wp-content/uploads/2018/02/TSV_TS107.pdf",
        "https://www.nordson.com/en/divisions/electronics-solutions/your-process/industries/pcb-and-smt-assembly"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "依成品機構與冷卻設計選用；無補強框、無蓋或不同冷卻方案不必強制加裝。",
        "en": "Selected by the mechanical/cooling design; stiffener-free, lidless or different cooling designs do not require this hardware."
      }
    },
    {
      "id": "V08",
      "catalogueOrder": 108,
      "branchId": "finish-test",
      "branchOrder": 8,
      "activityType": "manufacturing",
      "title": {
        "zh-TW": "整合散熱器或冷板",
        "en": "Integrate a heat sink or cold plate"
      },
      "summary": {
        "zh-TW": "以已封裝元件與系統冷卻設計為起點，建立受控機械接觸與冷卻邊界。交付可供系統測試的冷卻組件，以接觸壓力與冷卻條件紀錄判讀結果；重點辨識裝配負載壓裂封裝或接觸不足。",
        "en": "Start with packaged devices and the cooling design; establish controlled contact and cooling boundaries to obtain a cooled assembly ready for system tests. Assess the result using contact-pressure and cooling-condition records, with particular attention to assembly load cracking the package or weak contact."
      },
      "input": {
        "zh-TW": "已封裝元件與系統冷卻設計",
        "en": "packaged devices and the cooling design"
      },
      "operation": {
        "zh-TW": "建立受控機械接觸與冷卻邊界",
        "en": "establish controlled contact and cooling boundaries"
      },
      "output": {
        "zh-TW": "可供系統測試的冷卻組件",
        "en": "a cooled assembly ready for system tests"
      },
      "qualityEvidence": {
        "zh-TW": "接觸壓力與冷卻條件紀錄",
        "en": "contact-pressure and cooling-condition records"
      },
      "failureMode": {
        "zh-TW": "裝配負載壓裂封裝或接觸不足",
        "en": "assembly load cracking the package or weak contact"
      },
      "prerequisiteIds": [
        "V07"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "thermal",
      "sourceIds": [
        "ase-thermal",
        "nordson-tim"
      ],
      "sourceUrls": [
        "https://ase.aseglobal.com/lab-services/stress-and-thermal-lab/",
        "https://www.nordson.com/en/divisions/electronics-solutions/your-process/industries/pcb-and-smt-assembly"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "依成品機構與冷卻設計選用；無補強框、無蓋或不同冷卻方案不必強制加裝。",
        "en": "Selected by the mechanical/cooling design; stiffener-free, lidless or different cooling designs do not require this hardware."
      }
    },
    {
      "id": "V09",
      "catalogueOrder": 109,
      "branchId": "finish-test",
      "branchOrder": 9,
      "activityType": "inspection_test",
      "title": {
        "zh-TW": "以X光與聲學檢查內部界面",
        "en": "Inspect internal interfaces by X-ray and acoustics"
      },
      "summary": {
        "zh-TW": "以終封裝組件與待檢缺陷類型為起點，選擇相容非破壞影像方法。交付內部接點與分層證據，以影像位置、解析度與參考樣本判讀結果；重點辨識把影像漂亮當成電性正常。",
        "en": "Start with final assemblies and target defect classes; select compatible nondestructive imaging methods to obtain evidence on internal joints and delamination. Assess the result using image registration, resolution and references, with particular attention to treating clean images as proof of electrical function."
      },
      "input": {
        "zh-TW": "終封裝組件與待檢缺陷類型",
        "en": "final assemblies and target defect classes"
      },
      "operation": {
        "zh-TW": "選擇相容非破壞影像方法",
        "en": "select compatible nondestructive imaging methods"
      },
      "output": {
        "zh-TW": "內部接點與分層證據",
        "en": "evidence on internal joints and delamination"
      },
      "qualityEvidence": {
        "zh-TW": "影像位置、解析度與參考樣本",
        "en": "image registration, resolution and references"
      },
      "failureMode": {
        "zh-TW": "把影像漂亮當成電性正常",
        "en": "treating clean images as proof of electrical function"
      },
      "prerequisiteIds": [
        "V08"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "thermal",
      "sourceIds": [
        "ase-fa"
      ],
      "sourceUrls": [
        "https://ase.aseglobal.com/lab-services/failure-analysis-lab/"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "V10",
      "catalogueOrder": 110,
      "branchId": "finish-test",
      "branchOrder": 10,
      "activityType": "inspection_test",
      "title": {
        "zh-TW": "量測成品翹曲與焊球共面度",
        "en": "Measure package warpage and ball coplanarity"
      },
      "summary": {
        "zh-TW": "以完成機械組裝的封裝為起點，在定義條件下量測形狀與端點高度。交付可用於主板接合的幾何報告，以溫度條件與局部共面度圖判讀結果；重點辨識室溫合格卻在後續熱循環翹曲。",
        "en": "Start with mechanically completed packages; measure package shape and terminal height under defined conditions to obtain a geometry report for board assembly. Assess the result using temperature conditions and local coplanarity maps, with particular attention to room-temperature acceptance hiding thermal warpage."
      },
      "input": {
        "zh-TW": "完成機械組裝的封裝",
        "en": "mechanically completed packages"
      },
      "operation": {
        "zh-TW": "在定義條件下量測形狀與端點高度",
        "en": "measure package shape and terminal height under defined conditions"
      },
      "output": {
        "zh-TW": "可用於主板接合的幾何報告",
        "en": "a geometry report for board assembly"
      },
      "qualityEvidence": {
        "zh-TW": "溫度條件與局部共面度圖",
        "en": "temperature conditions and local coplanarity maps"
      },
      "failureMode": {
        "zh-TW": "室溫合格卻在後續熱循環翹曲",
        "en": "room-temperature acceptance hiding thermal warpage"
      },
      "prerequisiteIds": [
        "V09"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "thermal",
      "sourceIds": [
        "ase-thermal",
        "kla-metrology"
      ],
      "sourceUrls": [
        "https://ase.aseglobal.com/lab-services/stress-and-thermal-lab/",
        "https://ask.kla-tencor.com/products/packaging-manufacturing/wafer-inspection-and-metrology-for-advanced-packaging"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "V11",
      "catalogueOrder": 111,
      "branchId": "finish-test",
      "branchOrder": 11,
      "activityType": "inspection_test",
      "title": {
        "zh-TW": "執行封裝直流開短路測試",
        "en": "Run package DC opens-and-shorts tests"
      },
      "summary": {
        "zh-TW": "以終封裝產品與測試接觸介面為起點，檢查基本供電、漏電及互連狀態。交付直流測試與分選紀錄，以接觸重複性與失效腳位判讀結果；重點辨識測試插座接觸問題被當成產品缺陷。",
        "en": "Start with finished packages and test contacts; check basic supply, leakage and interconnect behavior to obtain DC test and binning records. Assess the result using contact repeatability and failed-pin evidence, with particular attention to socket contact problems mistaken for product defects."
      },
      "input": {
        "zh-TW": "終封裝產品與測試接觸介面",
        "en": "finished packages and test contacts"
      },
      "operation": {
        "zh-TW": "檢查基本供電、漏電及互連狀態",
        "en": "check basic supply, leakage and interconnect behavior"
      },
      "output": {
        "zh-TW": "直流測試與分選紀錄",
        "en": "DC test and binning records"
      },
      "qualityEvidence": {
        "zh-TW": "接觸重複性與失效腳位",
        "en": "contact repeatability and failed-pin evidence"
      },
      "failureMode": {
        "zh-TW": "測試插座接觸問題被當成產品缺陷",
        "en": "socket contact problems mistaken for product defects"
      },
      "prerequisiteIds": [
        "V10"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "thermal",
      "sourceIds": [
        "advantest-ate",
        "amkor-test"
      ],
      "sourceUrls": [
        "https://www.advantest.com/en/semiconductor-basics/automated-test-equipment/",
        "https://amkor.com/test-services/"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "V12",
      "catalogueOrder": 112,
      "branchId": "finish-test",
      "branchOrder": 12,
      "activityType": "inspection_test",
      "title": {
        "zh-TW": "執行運算與記憶體功能測試",
        "en": "Test compute and memory functions"
      },
      "summary": {
        "zh-TW": "以通過基本電測的產品為起點，執行核准邏輯與記憶體圖樣。交付功能覆蓋與失效記錄，以測試版本、溫度與覆蓋範圍判讀結果；重點辨識圖樣不足漏掉組裝誘發故障。",
        "en": "Start with products passing basic electrical tests; run approved logic and memory patterns to obtain functional coverage and failure records. Assess the result using test revision, temperature and coverage, with particular attention to insufficient patterns missing assembly-induced faults."
      },
      "input": {
        "zh-TW": "通過基本電測的產品",
        "en": "products passing basic electrical tests"
      },
      "operation": {
        "zh-TW": "執行核准邏輯與記憶體圖樣",
        "en": "run approved logic and memory patterns"
      },
      "output": {
        "zh-TW": "功能覆蓋與失效記錄",
        "en": "functional coverage and failure records"
      },
      "qualityEvidence": {
        "zh-TW": "測試版本、溫度與覆蓋範圍",
        "en": "test revision, temperature and coverage"
      },
      "failureMode": {
        "zh-TW": "圖樣不足漏掉組裝誘發故障",
        "en": "insufficient patterns missing assembly-induced faults"
      },
      "prerequisiteIds": [
        "V11"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "thermal",
      "sourceIds": [
        "ieee-test",
        "amkor-test"
      ],
      "sourceUrls": [
        "https://cmte.ieee.org/eps-test/wp-content/uploads/sites/132/2022/01/IEEE_EPS_Test_Het_Int_Product_Testability_BKM_Final_v1_0-1-14-22-1.pdf",
        "https://amkor.com/test-services/"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "V13",
      "catalogueOrder": 113,
      "branchId": "finish-test",
      "branchOrder": 13,
      "activityType": "inspection_test",
      "title": {
        "zh-TW": "驗證高速互連裕量",
        "en": "Validate high-speed link margins"
      },
      "summary": {
        "zh-TW": "以可操作鏈路與定義測試條件為起點，評估誤碼、時序與通道裕量。交付可比較的高速鏈路測試結果，以儀器校正、測試時間與邊界條件判讀結果；重點辨識只測單一負載或角落造成假安心。",
        "en": "Start with operating links and defined test conditions; evaluate errors, timing and channel margin to obtain comparable high-speed link results. Assess the result using calibration, observation time and test boundaries, with particular attention to testing only one load or corner giving false confidence."
      },
      "input": {
        "zh-TW": "可操作鏈路與定義測試條件",
        "en": "operating links and defined test conditions"
      },
      "operation": {
        "zh-TW": "評估誤碼、時序與通道裕量",
        "en": "evaluate errors, timing and channel margin"
      },
      "output": {
        "zh-TW": "可比較的高速鏈路測試結果",
        "en": "comparable high-speed link results"
      },
      "qualityEvidence": {
        "zh-TW": "儀器校正、測試時間與邊界條件",
        "en": "calibration, observation time and test boundaries"
      },
      "failureMode": {
        "zh-TW": "只測單一負載或角落造成假安心",
        "en": "testing only one load or corner giving false confidence"
      },
      "prerequisiteIds": [
        "V12"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "thermal",
      "sourceIds": [
        "ucie",
        "cadence-3dic",
        "amkor-test"
      ],
      "sourceUrls": [
        "https://www.uciexpress.org/specifications",
        "https://www.cadence.com/en_US/home/resources/white-papers/3d-ic-design-wp.html",
        "https://amkor.com/test-services/"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "V14",
      "catalogueOrder": 114,
      "branchId": "finish-test",
      "branchOrder": 14,
      "activityType": "inspection_test",
      "title": {
        "zh-TW": "以系統負載進行SLT",
        "en": "Run system-level workload tests"
      },
      "summary": {
        "zh-TW": "以具散熱條件的可用封裝為起點，執行代表性系統負載與啟動情境。交付系統層故障與性能紀錄，以負載版本、監測資料與重現條件判讀結果；重點辨識ATE通過但整機負載暴露問題。",
        "en": "Start with functional packages with defined cooling; run representative workloads and startup scenarios to obtain system-level failure and performance records. Assess the result using workload revision, telemetry and reproducibility, with particular attention to passing ATE while failing realistic workloads."
      },
      "input": {
        "zh-TW": "具散熱條件的可用封裝",
        "en": "functional packages with defined cooling"
      },
      "operation": {
        "zh-TW": "執行代表性系統負載與啟動情境",
        "en": "run representative workloads and startup scenarios"
      },
      "output": {
        "zh-TW": "系統層故障與性能紀錄",
        "en": "system-level failure and performance records"
      },
      "qualityEvidence": {
        "zh-TW": "負載版本、監測資料與重現條件",
        "en": "workload revision, telemetry and reproducibility"
      },
      "failureMode": {
        "zh-TW": "ATE通過但整機負載暴露問題",
        "en": "passing ATE while failing realistic workloads"
      },
      "prerequisiteIds": [
        "V13"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "thermal",
      "sourceIds": [
        "intel-packaging",
        "advantest-ate"
      ],
      "sourceUrls": [
        "https://www.intel.com/content/www/us/en/foundry/packaging.htm",
        "https://www.advantest.com/en/semiconductor-basics/automated-test-equipment/"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "V15",
      "catalogueOrder": 115,
      "branchId": "finish-test",
      "branchOrder": 15,
      "activityType": "inspection_test",
      "title": {
        "zh-TW": "實測熱阻、熱點與暫態響應",
        "en": "Measure thermal resistance, hotspots and transients"
      },
      "summary": {
        "zh-TW": "以定義功率與冷卻條件的產品為起點，校正溫度量測並辨識熱路徑。交付可與模擬對照的熱性能資料，以功率、環境、接觸與誤差記錄判讀結果；重點辨識把表面溫度誤當晶粒接面溫度。",
        "en": "Start with products under defined power and cooling; calibrate temperature measurements and characterize heat paths to obtain thermal data that can be compared with simulation. Assess the result using power, ambient, contact and uncertainty records, with particular attention to confusing surface and junction temperature."
      },
      "input": {
        "zh-TW": "定義功率與冷卻條件的產品",
        "en": "products under defined power and cooling"
      },
      "operation": {
        "zh-TW": "校正溫度量測並辨識熱路徑",
        "en": "calibrate temperature measurements and characterize heat paths"
      },
      "output": {
        "zh-TW": "可與模擬對照的熱性能資料",
        "en": "thermal data that can be compared with simulation"
      },
      "qualityEvidence": {
        "zh-TW": "功率、環境、接觸與誤差記錄",
        "en": "power, ambient, contact and uncertainty records"
      },
      "failureMode": {
        "zh-TW": "把表面溫度誤當晶粒接面溫度",
        "en": "confusing surface and junction temperature"
      },
      "prerequisiteIds": [
        "V14"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "thermal",
      "sourceIds": [
        "ase-thermal"
      ],
      "sourceUrls": [
        "https://ase.aseglobal.com/lab-services/stress-and-thermal-lab/"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "按本教學分支與核准產品路線適用。",
        "en": "Applicable within this teaching branch and the qualified product route."
      }
    },
    {
      "id": "V16",
      "catalogueOrder": 116,
      "branchId": "finish-test",
      "branchOrder": 16,
      "activityType": "inspection_test",
      "title": {
        "zh-TW": "以獨立樣本進行溫度循環",
        "en": "Temperature-cycle a dedicated sample cohort"
      },
      "summary": {
        "zh-TW": "以通過基線測試的專用樣本為起點，執行核准循環並追蹤電性變化。交付熱疲勞與界面穩定性證據，以前後電測、失效時間與物理檢查判讀結果；重點辨識循環條件與用途不匹配。",
        "en": "Start with dedicated samples with passing baseline tests; run qualified cycling and monitor electrical changes to obtain thermal-fatigue and interface-stability evidence. Assess the result using pre/post tests, failure timing and physical inspection, with particular attention to cycling conditions mismatched to the use case."
      },
      "input": {
        "zh-TW": "通過基線測試的專用樣本",
        "en": "dedicated samples with passing baseline tests"
      },
      "operation": {
        "zh-TW": "執行核准循環並追蹤電性變化",
        "en": "run qualified cycling and monitor electrical changes"
      },
      "output": {
        "zh-TW": "熱疲勞與界面穩定性證據",
        "en": "thermal-fatigue and interface-stability evidence"
      },
      "qualityEvidence": {
        "zh-TW": "前後電測、失效時間與物理檢查",
        "en": "pre/post tests, failure timing and physical inspection"
      },
      "failureMode": {
        "zh-TW": "循環條件與用途不匹配",
        "en": "cycling conditions mismatched to the use case"
      },
      "prerequisiteIds": [
        "V11",
        "V12"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "thermal",
      "sourceIds": [
        "amkor-mechanical",
        "ase-thermal"
      ],
      "sourceUrls": [
        "https://amkor.com/kr/wp-content/uploads/2018/02/Mechanical_Package_Characterization_SS23.pdf",
        "https://ase.aseglobal.com/lab-services/stress-and-thermal-lab/"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "依核准資格試驗矩陣使用獨立樣本；不可把全部應力順序施加在同一批樣本。",
        "en": "Use a separate cohort selected by the qualification matrix; do not serially apply every stress to one cohort."
      },
      "flowRelation": "parallel_qualification_cohort"
    },
    {
      "id": "V17",
      "catalogueOrder": 117,
      "branchId": "finish-test",
      "branchOrder": 17,
      "activityType": "inspection_test",
      "title": {
        "zh-TW": "以專用樣本進行濕氣與回焊預處理",
        "en": "Moisture-condition and reflow dedicated samples"
      },
      "summary": {
        "zh-TW": "以指定濕敏條件與未混用的樣本為起點，模擬吸濕後的裝板熱歷程。交付裝板前處理後的完整性資料，以吸濕、回焊紀錄與界面檢查判讀結果；重點辨識吸濕膨脹導致分層或裂紋。",
        "en": "Start with defined moisture conditions and separate samples; simulate assembly thermal exposure after moisture conditioning to obtain integrity data after assembly preconditioning. Assess the result using conditioning/reflow records and interface inspection, with particular attention to moisture-driven delamination or cracking."
      },
      "input": {
        "zh-TW": "指定濕敏條件與未混用的樣本",
        "en": "defined moisture conditions and separate samples"
      },
      "operation": {
        "zh-TW": "模擬吸濕後的裝板熱歷程",
        "en": "simulate assembly thermal exposure after moisture conditioning"
      },
      "output": {
        "zh-TW": "裝板前處理後的完整性資料",
        "en": "integrity data after assembly preconditioning"
      },
      "qualityEvidence": {
        "zh-TW": "吸濕、回焊紀錄與界面檢查",
        "en": "conditioning/reflow records and interface inspection"
      },
      "failureMode": {
        "zh-TW": "吸濕膨脹導致分層或裂紋",
        "en": "moisture-driven delamination or cracking"
      },
      "prerequisiteIds": [
        "V11",
        "V12"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "thermal",
      "sourceIds": [
        "amkor-quality",
        "ase-fa"
      ],
      "sourceUrls": [
        "https://amkor.com/wp-content/uploads/2019/08/Quality_Brochure-BR206.pdf",
        "https://ase.aseglobal.com/lab-services/failure-analysis-lab/"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "依核准資格試驗矩陣使用獨立樣本；不可把全部應力順序施加在同一批樣本。",
        "en": "Use a separate cohort selected by the qualification matrix; do not serially apply every stress to one cohort."
      },
      "flowRelation": "parallel_qualification_cohort"
    },
    {
      "id": "V18",
      "catalogueOrder": 118,
      "branchId": "finish-test",
      "branchOrder": 18,
      "activityType": "inspection_test",
      "title": {
        "zh-TW": "以獨立樣本進行濕熱偏壓試驗",
        "en": "Run humidity-bias tests on a separate cohort"
      },
      "summary": {
        "zh-TW": "以有基線資料的可靠度樣本為起點，依核准條件施加濕熱與偏壓。交付抗腐蝕與漏電穩定性證據，以條件履歷、漏電趨勢與失效定位判讀結果；重點辨識腐蝕或離子污染引發漏電。",
        "en": "Start with reliability samples with baseline records; apply humidity, heat and bias under qualified conditions to obtain corrosion and leakage-stability evidence. Assess the result using condition history, leakage trends and failure localization, with particular attention to corrosion or ionic contamination causing leakage."
      },
      "input": {
        "zh-TW": "有基線資料的可靠度樣本",
        "en": "reliability samples with baseline records"
      },
      "operation": {
        "zh-TW": "依核准條件施加濕熱與偏壓",
        "en": "apply humidity, heat and bias under qualified conditions"
      },
      "output": {
        "zh-TW": "抗腐蝕與漏電穩定性證據",
        "en": "corrosion and leakage-stability evidence"
      },
      "qualityEvidence": {
        "zh-TW": "條件履歷、漏電趨勢與失效定位",
        "en": "condition history, leakage trends and failure localization"
      },
      "failureMode": {
        "zh-TW": "腐蝕或離子污染引發漏電",
        "en": "corrosion or ionic contamination causing leakage"
      },
      "prerequisiteIds": [
        "V11",
        "V12"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "thermal",
      "sourceIds": [
        "amkor-quality",
        "amkor-mechanical"
      ],
      "sourceUrls": [
        "https://amkor.com/wp-content/uploads/2019/08/Quality_Brochure-BR206.pdf",
        "https://amkor.com/kr/wp-content/uploads/2018/02/Mechanical_Package_Characterization_SS23.pdf"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "依核准資格試驗矩陣使用獨立樣本；不可把全部應力順序施加在同一批樣本。",
        "en": "Use a separate cohort selected by the qualification matrix; do not serially apply every stress to one cohort."
      },
      "flowRelation": "parallel_qualification_cohort"
    },
    {
      "id": "V19",
      "catalogueOrder": 119,
      "branchId": "finish-test",
      "branchOrder": 19,
      "activityType": "inspection_test",
      "title": {
        "zh-TW": "定位失效並進行破壞性分析",
        "en": "Localize failures before destructive analysis"
      },
      "summary": {
        "zh-TW": "以有重現條件的失效樣本為起點，先非破壞定位，再選擇截面或FIB。交付連結症狀與物理機制的證據，以樣本履歷、定位與截面對照判讀結果；重點辨識過早切片破壞原始失效證據。",
        "en": "Start with failed samples with reproducible symptoms; localize nondestructively before sectioning or FIB to obtain evidence linking symptoms and physical mechanisms. Assess the result using sample history, localization and cross-section correlation, with particular attention to premature sectioning destroying failure evidence."
      },
      "input": {
        "zh-TW": "有重現條件的失效樣本",
        "en": "failed samples with reproducible symptoms"
      },
      "operation": {
        "zh-TW": "先非破壞定位，再選擇截面或FIB",
        "en": "localize nondestructively before sectioning or FIB"
      },
      "output": {
        "zh-TW": "連結症狀與物理機制的證據",
        "en": "evidence linking symptoms and physical mechanisms"
      },
      "qualityEvidence": {
        "zh-TW": "樣本履歷、定位與截面對照",
        "en": "sample history, localization and cross-section correlation"
      },
      "failureMode": {
        "zh-TW": "過早切片破壞原始失效證據",
        "en": "premature sectioning destroying failure evidence"
      },
      "prerequisiteIds": [
        "V11"
      ],
      "prerequisiteAnyOf": [
        "V09",
        "V10",
        "V12",
        "V13",
        "V14",
        "V15",
        "V16",
        "V17",
        "V18"
      ],
      "overviewTourId": "thermal",
      "sourceIds": [
        "ase-fa",
        "amkor-quality"
      ],
      "sourceUrls": [
        "https://ase.aseglobal.com/lab-services/failure-analysis-lab/",
        "https://amkor.com/wp-content/uploads/2019/08/Quality_Brochure-BR206.pdf"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "有失效或需確認物理機制時執行；破壞性分析不是每件出貨品的例行站。",
        "en": "Triggered by failures or a need to establish a physical mechanism; destructive analysis is not a routine station for every shipped unit."
      },
      "flowRelation": "failure_triggered"
    },
    {
      "id": "V20",
      "catalogueOrder": 120,
      "branchId": "finish-test",
      "branchOrder": 20,
      "activityType": "design",
      "title": {
        "zh-TW": "整合證據並放行產品版本",
        "en": "Integrate evidence and release the product revision"
      },
      "summary": {
        "zh-TW": "以已完成的必需測試與異常處置為起點，審查適用試驗、覆蓋缺口與改善閉環。交付可追溯的資格與放行決策，以測試矩陣、例外理由與簽核判讀結果；重點辨識把未執行的試驗寫成已通過。",
        "en": "Start with required test results and anomaly dispositions; review applicable tests, coverage gaps and corrective actions to obtain a traceable qualification and release decision. Assess the result using test matrix, waiver rationale and sign-off, with particular attention to recording unperformed tests as passed."
      },
      "input": {
        "zh-TW": "已完成的必需測試與異常處置",
        "en": "required test results and anomaly dispositions"
      },
      "operation": {
        "zh-TW": "審查適用試驗、覆蓋缺口與改善閉環",
        "en": "review applicable tests, coverage gaps and corrective actions"
      },
      "output": {
        "zh-TW": "可追溯的資格與放行決策",
        "en": "a traceable qualification and release decision"
      },
      "qualityEvidence": {
        "zh-TW": "測試矩陣、例外理由與簽核",
        "en": "test matrix, waiver rationale and sign-off"
      },
      "failureMode": {
        "zh-TW": "把未執行的試驗寫成已通過",
        "en": "recording unperformed tests as passed"
      },
      "prerequisiteIds": [
        "V11",
        "V12",
        "V15"
      ],
      "prerequisiteAnyOf": [],
      "overviewTourId": "thermal",
      "sourceIds": [
        "amkor-quality",
        "ieee-test"
      ],
      "sourceUrls": [
        "https://amkor.com/wp-content/uploads/2019/08/Quality_Brochure-BR206.pdf",
        "https://cmte.ieee.org/eps-test/wp-content/uploads/sites/132/2022/01/IEEE_EPS_Test_Het_Int_Product_Testability_BKM_Final_v1_0-1-14-22-1.pdf"
      ],
      "plannedDurationSeconds": 300,
      "videoStatus": "not_produced",
      "videoUrl": null,
      "scriptStatus": "summary_only",
      "applicability": {
        "zh-TW": "由產品資格矩陣指定哪些結果為必要；不適用的試驗需記錄理由，未執行不得標示通過。",
        "en": "The product qualification matrix selects required results. Record justified exclusions; unperformed tests must never be marked passed."
      },
      "flowRelation": "qualification_matrix_gate",
      "requiredEvidenceFromSelectedTests": [
        "V09",
        "V10",
        "V13",
        "V14",
        "V16",
        "V17",
        "V18",
        "V19"
      ]
    }
  ]
};
