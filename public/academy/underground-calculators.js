/* V14 transparent educational models; all defaults are synthetic. */
export const UNDERGROUND_LABS = {
  "ugEffective": {
    "title": [
      "有效應力與水頭",
      "Effective stress and water head"
    ],
    "formula": "σ′ = γ z − γw h",
    "unit": "kPa",
    "note": [
      "均勻總單位重與靜水假設，γw=9.81 kN/m³，h為計算點以上水頭。只算垂直一維應力，不代表側壓或掌子面支撐壓力。",
      "Uniform total unit weight and hydrostatic water with γw=9.81 kN/m³; h is head above the point. This is one-dimensional vertical stress, not lateral or face-support pressure."
    ],
    "question": [
      "水頭增加10 m，有效應力減少多少？分層土應如何修改總應力積分？",
      "How much does effective stress fall when head increases by 10 m? How would layered soil change total stress?"
    ],
    "params": [
      [
        "gamma",
        [
          "總單位重 γ",
          "Total unit weight γ"
        ],
        18,
        26,
        0.1,
        22,
        "kN/m³"
      ],
      [
        "depth",
        [
          "埋深 z",
          "Depth z"
        ],
        5,
        100,
        1,
        30,
        "m"
      ],
      [
        "head",
        [
          "水頭 h",
          "Water head h"
        ],
        0,
        100,
        1,
        20,
        "m"
      ]
    ],
    "source": "https://www.fhwa.dot.gov/bridge/tunnel/library.cfm"
  },
  "ugHydro": {
    "title": [
      "靜水壓力",
      "Hydrostatic pressure"
    ],
    "formula": "p = ρ g h = 9.81 h",
    "unit": "kPa",
    "note": [
      "淡水密度1000 kg/m³、重力9.81 m/s²。計算表壓，不包括湧水動壓、潮汐變動或瞬變壓力。",
      "Freshwater density 1000 kg/m³ and gravity 9.81 m/s². Gauge pressure excludes dynamic inflow, tidal variation and transient pressure."
    ],
    "question": [
      "相同水頭下，隧道直徑會改變局部靜水壓力嗎？",
      "At fixed head, does tunnel diameter change local hydrostatic pressure?"
    ],
    "params": [
      [
        "head",
        [
          "水頭 h",
          "Water head h"
        ],
        0,
        150,
        1,
        30,
        "m"
      ]
    ],
    "source": "https://www.fhwa.dot.gov/bridge/tunnel/library.cfm"
  },
  "ugThrust": {
    "title": [
      "均布面壓的合力",
      "Resultant of uniform face pressure"
    ],
    "formula": "F = p π D² / 4",
    "unit": "MN",
    "note": [
      "只積分均勻法向壓力，不含刀具切削、盾殼摩擦、曲線導向或管片容許推力。輸入不是TBM運轉設定。",
      "Integrates uniform normal pressure only. Cutting, shield friction, steering and segment capacity are excluded. Inputs are not TBM operating settings."
    ],
    "question": [
      "面壓不變，直徑加倍為何合力變成四倍？",
      "Why does doubling diameter quadruple force at fixed pressure?"
    ],
    "params": [
      [
        "pressure",
        [
          "均布壓力 p",
          "Uniform pressure p"
        ],
        10,
        1000,
        10,
        300,
        "kPa"
      ],
      [
        "diameter",
        [
          "開挖直徑 D",
          "Excavation diameter D"
        ],
        2,
        16,
        0.1,
        6,
        "m"
      ]
    ],
    "source": "https://www.fhwa.dot.gov/bridge/tunnel/library.cfm"
  },
  "ugAdvance": {
    "title": [
      "掘進時間預算",
      "Advance time budget"
    ],
    "formula": "L = penetration × rpm × 60 × hours × utilization / 1000",
    "unit": "m/day",
    "note": [
      "貫入度為mm/rev，利用率只乘一次；假設工作時段內轉速與貫入度固定。忽略換刀、運碴、管片供應等耦合，不是工期保證。",
      "Penetration is mm/rev; utilization is applied once. Rotation and penetration are constant during active cutting. Coupled maintenance, mucking and segment supply are excluded; this is not a schedule guarantee."
    ],
    "question": [
      "若停機使利用率由0.5變成0.25，日進尺如何變化？",
      "If downtime changes utilization from 0.5 to 0.25, what happens to daily advance?"
    ],
    "params": [
      [
        "penetration",
        [
          "每轉貫入",
          "Penetration per revolution"
        ],
        1,
        15,
        0.1,
        5,
        "mm/rev"
      ],
      [
        "rpm",
        [
          "轉速",
          "Rotation"
        ],
        0.2,
        10,
        0.1,
        2,
        "rev/min"
      ],
      [
        "hours",
        [
          "排定工時",
          "Scheduled hours"
        ],
        1,
        24,
        1,
        20,
        "h/day"
      ],
      [
        "utilization",
        [
          "有效掘進比例",
          "Cutting utilization"
        ],
        0.05,
        1,
        0.01,
        0.5,
        ""
      ]
    ],
    "source": "https://www.fhwa.dot.gov/bridge/tunnel/library.cfm"
  },
  "ugSettlement": {
    "title": [
      "高斯沉陷槽的體積守恆",
      "Gaussian settlement volume balance"
    ],
    "formula": "Smax = VL × (πD²/4) / (√(2π) i)",
    "unit": "mm",
    "note": [
      "VL以百分比輸入。假設橫向高斯沉陷槽、單位長度土體體積損失等於沉陷槽面積；不包括建築剛度、地下水沉降或分層剪脹。",
      "VL is entered as percent. A transverse Gaussian trough conserves lost ground volume per unit length. Building stiffness, groundwater drawdown settlement and layered dilation are excluded."
    ],
    "question": [
      "相同損失體積，槽寬i加倍，最大沉陷會怎樣？",
      "At fixed loss volume, how does doubling trough width i change maximum settlement?"
    ],
    "params": [
      [
        "loss",
        [
          "體積損失 VL",
          "Volume loss VL"
        ],
        0.1,
        5,
        0.1,
        1,
        "%"
      ],
      [
        "diameter",
        [
          "隧道直徑 D",
          "Tunnel diameter D"
        ],
        2,
        15,
        0.1,
        6,
        "m"
      ],
      [
        "width",
        [
          "槽寬參數 i",
          "Trough width i"
        ],
        2,
        40,
        0.5,
        10,
        "m"
      ]
    ],
    "source": "https://www.fhwa.dot.gov/bridge/tunnel/library.cfm"
  },
  "ugDarcy": {
    "title": [
      "Darcy一維滲流",
      "One-dimensional Darcy flow"
    ],
    "formula": "Q = k A Δh / L",
    "unit": "m³/h",
    "note": [
      "均勻飽和介質、穩態層流與一維流線；水頭差取非負大小。不適用裂隙集中湧水、紊流或真實三維開挖湧水預測。",
      "Uniform saturated medium, steady laminar flow and one-dimensional streamlines. Head difference is a nonnegative magnitude. This excludes concentrated fracture inflow, turbulence and real three-dimensional excavation inflow."
    ],
    "question": [
      "滲透係數增加10倍，而幾何不變，流量如何變化？",
      "If permeability increases tenfold at unchanged geometry, how does flow change?"
    ],
    "params": [
      [
        "k",
        [
          "滲透係數 k",
          "Hydraulic conductivity k"
        ],
        1e-06,
        0.001,
        1e-06,
        0.0001,
        "m/s"
      ],
      [
        "area",
        [
          "流通面積 A",
          "Flow area A"
        ],
        1,
        100,
        1,
        20,
        "m²"
      ],
      [
        "head",
        [
          "水頭差 Δh",
          "Head difference Δh"
        ],
        0,
        50,
        1,
        10,
        "m"
      ],
      [
        "length",
        [
          "流徑 L",
          "Flow path L"
        ],
        1,
        100,
        1,
        20,
        "m"
      ]
    ],
    "source": "https://www.fhwa.dot.gov/bridge/tunnel/library.cfm"
  },
  "ugRing": {
    "title": [
      "薄圓環的膜力應力",
      "Thin circular ring membrane stress"
    ],
    "formula": "σθ = p R / t",
    "unit": "MPa",
    "note": [
      "均勻外壓、薄圓環膜力近似，限定t/R≤0.1。未檢核接縫、彎矩、屈曲、裂縫或土壤互制，不能當作管片設計驗算。",
      "Uniform external pressure and thin-ring membrane approximation, limited to t/R≤0.1. Joints, bending, buckling, cracks and soil interaction are excluded; this is not a segment design check."
    ],
    "question": [
      "厚度增為兩倍會降低膜力應力，但能否因此推論接縫安全？",
      "Doubling thickness lowers membrane stress; does that establish joint safety?"
    ],
    "params": [
      [
        "pressure",
        [
          "外壓 p",
          "External pressure p"
        ],
        0.01,
        1,
        0.01,
        0.3,
        "MPa"
      ],
      [
        "radius",
        [
          "平均半徑 R",
          "Mean radius R"
        ],
        2,
        8,
        0.1,
        3,
        "m"
      ],
      [
        "thickness",
        [
          "厚度 t",
          "Thickness t"
        ],
        0.1,
        1,
        0.01,
        0.3,
        "m"
      ]
    ],
    "source": "https://www.fhwa.dot.gov/bridge/tunnel/library.cfm"
  },
  "ugBolts": {
    "title": [
      "理想支護力分配",
      "Ideal support force allocation"
    ],
    "formula": "N = ceil(q A / (C η))",
    "unit": "bolts",
    "note": [
      "q為假設均布需求，C為已提供的單支容許容量，η為假設分配效率。忽略岩楔幾何、拔出、剪斷與錨固品質；不是錨栓間距處方。",
      "q is assumed distributed demand, C is a supplied allowable capacity per bolt and η is an assumed allocation efficiency. Wedge geometry, pullout, shear and bond quality are excluded; this is not a bolt-spacing prescription."
    ],
    "question": [
      "容量不變而效率減半，需要的整數支數是否恰好加倍？為何取整會影響答案？",
      "At unchanged capacity, does halving efficiency exactly double the integer count? How does rounding matter?"
    ],
    "params": [
      [
        "pressure",
        [
          "需求 q",
          "Demand q"
        ],
        1,
        200,
        1,
        30,
        "kPa"
      ],
      [
        "area",
        [
          "受力面積 A",
          "Loaded area A"
        ],
        1,
        100,
        1,
        20,
        "m²"
      ],
      [
        "capacity",
        [
          "容許容量 C",
          "Allowable capacity C"
        ],
        10,
        500,
        10,
        150,
        "kN"
      ],
      [
        "efficiency",
        [
          "分配效率 η",
          "Allocation efficiency η"
        ],
        0.1,
        1,
        0.05,
        0.8,
        ""
      ]
    ],
    "source": "https://www.fhwa.dot.gov/bridge/tunnel/library.cfm"
  },
  "ugBuoyancy": {
    "title": [
      "浮力與自重比值",
      "Weight to buoyancy ratio"
    ],
    "formula": "ratio = W / (γw V)",
    "unit": "",
    "note": [
      "V為封閉不透水體排開的水體積，W為已指定抗浮自重。忽略錨固、側摩擦、覆土與水壓分布變化；結果不是法規安全係數驗收。",
      "V is water displaced by a closed impermeable body and W is specified resisting self-weight. Anchors, side friction, overburden and variable water pressure are excluded. The result is not a code acceptance check."
    ],
    "question": [
      "如果結構內部進水，仍可直接使用封閉排水體積嗎？",
      "If water enters the structure, can the closed displaced volume still be used directly?"
    ],
    "params": [
      [
        "weight",
        [
          "抗浮自重 W",
          "Resisting weight W"
        ],
        100,
        50000,
        100,
        12000,
        "kN"
      ],
      [
        "volume",
        [
          "排水體積 V",
          "Displaced volume V"
        ],
        10,
        5000,
        10,
        1000,
        "m³"
      ]
    ],
    "source": "https://www.fhwa.dot.gov/bridge/tunnel/library.cfm"
  },
  "ugConsolidation": {
    "title": [
      "一維固結90%時間",
      "Time to 90% one-dimensional consolidation"
    ],
    "formula": "t90 = 0.848 Hdr² / cv",
    "unit": "days",
    "note": [
      "Terzaghi一維理想固結，初始超額孔壓均勻；Hdr是最大排水距離，雙向排水為層厚的一半。忽略次壓密與cv隨應力改變。",
      "Ideal Terzaghi one-dimensional consolidation with uniform initial excess pore pressure. Hdr is maximum drainage path, half the layer thickness for double drainage. Secondary compression and stress-dependent cv are excluded."
    ],
    "question": [
      "改成雙向排水使最大排水距離減半，時間變成幾分之一？",
      "When double drainage halves maximum drainage path, what fraction of the time remains?"
    ],
    "params": [
      [
        "drainage",
        [
          "最大排水距離 Hdr",
          "Maximum drainage path Hdr"
        ],
        0.5,
        20,
        0.5,
        5,
        "m"
      ],
      [
        "cv",
        [
          "固結係數 cv",
          "Consolidation coefficient cv"
        ],
        0.001,
        0.1,
        0.001,
        0.01,
        "m²/day"
      ]
    ],
    "source": "https://environment.uwe.ac.uk/geocal/soilmech/consol/soilcons.htm"
  },
  "ugVent": {
    "title": [
      "通風系統平方阻力與功率",
      "Ventilation system resistance and power"
    ],
    "formula": "Δp = R Q²; P = R Q³ / η",
    "unit": "kW",
    "note": [
      "R為固定系統阻力係數，η為總效率。假設不可壓縮穩態；不求風機曲線交點、不含火災煙控或污染物暴露判定。",
      "R is fixed system resistance and η is total efficiency. Incompressible steady flow is assumed. This does not solve fan-curve intersection, fire smoke control or contaminant exposure."
    ],
    "question": [
      "固定R與效率時，風量加倍，所需功率為幾倍？",
      "At fixed R and efficiency, how much does required power rise when flow doubles?"
    ],
    "params": [
      [
        "flow",
        [
          "體積風量 Q",
          "Volumetric flow Q"
        ],
        5,
        150,
        1,
        50,
        "m³/s"
      ],
      [
        "resistance",
        [
          "系統阻力 R",
          "System resistance R"
        ],
        0.01,
        1,
        0.01,
        0.2,
        "Pa/(m³/s)²"
      ],
      [
        "efficiency",
        [
          "總效率 η",
          "Total efficiency η"
        ],
        0.2,
        0.95,
        0.01,
        0.7,
        ""
      ]
    ],
    "source": "https://www.energy.gov/cmei/ito/fan-systems"
  },
  "ugSurvey": {
    "title": [
      "獨立量測不確定度",
      "Independent measurement uncertainty"
    ],
    "formula": "σtotal = √(σ1² + σ2² + σ3²)",
    "unit": "mm",
    "note": [
      "三項獨立零均值一維標準不確定度。若有共變異數或系統偏差就不能直接平方和；不代表隧道貫通誤差的完整傳播。",
      "Three independent zero-mean one-dimensional standard uncertainties. Covariance and systematic bias invalidate simple root-sum-square; this is not full tunnel breakthrough error propagation."
    ],
    "question": [
      "若三次量測共用同一偏差，增加次數是否能消除它？",
      "If three measurements share a bias, can more repetitions eliminate it?"
    ],
    "params": [
      [
        "one",
        [
          "控制網 σ1",
          "Control network σ1"
        ],
        0,
        20,
        0.1,
        3,
        "mm"
      ],
      [
        "two",
        [
          "設站 σ2",
          "Station setup σ2"
        ],
        0,
        20,
        0.1,
        4,
        "mm"
      ],
      [
        "three",
        [
          "讀數 σ3",
          "Reading σ3"
        ],
        0,
        20,
        0.1,
        0,
        "mm"
      ]
    ],
    "source": "https://www.fhwa.dot.gov/bridge/tunnel/library.cfm"
  },
  "ugGrout": {
    "title": [
      "環狀空隙的幾何用量",
      "Geometric annular void volume"
    ],
    "formula": "V = π (Do² − Di²) L f / 4",
    "unit": "m³",
    "note": [
      "外徑必須大於內徑；f為明確假設的用量倍率。只算幾何體積，不預測裂隙吸漿、壓力、凝結時間或現場注漿配方。",
      "Outer diameter must exceed inner diameter; f is an explicitly assumed quantity multiplier. Geometry alone does not predict fracture take, pressure, setting time or field grout recipes."
    ],
    "question": [
      "外徑與內徑接近時，量測誤差為何對用量比例特別敏感？",
      "Why does measurement uncertainty strongly affect volume when outer and inner diameters are close?"
    ],
    "params": [
      [
        "outer",
        [
          "開挖外徑 Do",
          "Excavated outer diameter Do"
        ],
        3,
        12,
        0.01,
        6.4,
        "m"
      ],
      [
        "inner",
        [
          "襯砌外徑 Di",
          "Lining outer diameter Di"
        ],
        2,
        11.9,
        0.01,
        6,
        "m"
      ],
      [
        "length",
        [
          "環寬 L",
          "Ring width L"
        ],
        0.5,
        3,
        0.1,
        1.5,
        "m"
      ],
      [
        "factor",
        [
          "假設用量倍率 f",
          "Assumed quantity factor f"
        ],
        1,
        2,
        0.05,
        1.2,
        ""
      ]
    ],
    "source": "https://www.fhwa.dot.gov/bridge/tunnel/library.cfm"
  }
};
const isUnderground = (course,step) => course.category==='underground' && (course.educationEdition===14 || (course.v14Extension && String(step?.id||'').includes('-v14-')));
export function undergroundLabKind(course,step={}) {
 if(!isUnderground(course,step))return '';
 const text=`${step.titleEn||''} ${step.detailEn||''} ${step.summaryEn||''}`.toLowerCase();
 const choices=[[/consolidat|drainage path/,'ugConsolidation'],[/ventilat|airflow|fan power/,'ugVent'],[/buoyan|uplift|float/,'ugBuoyancy'],[/grout|annular/,'ugGrout'],[/settlement trough|gaussian|volume loss/,'ugSettlement'],[/darcy|permeabil|seepage/,'ugDarcy'],[/hoop|thin.ring/,'ugRing'],[/bolt|anchor capacity/,'ugBolts'],[/advance|penetration|utilization/,'ugAdvance'],[/thrust|face pressure/,'ugThrust'],[/hydrostatic|water pressure/,'ugHydro'],[/survey|uncertainty|alignment/,'ugSurvey']];
 for(const [pattern,kind] of choices)if(pattern.test(text))return kind;
 const id=Number(String(course.id).slice(1));
 if(id>=135&&id<=147)return 'ugAdvance';
 if(id>=151&&id<=162)return 'ugRing';
 if(id>=163&&id<=165)return 'ugDarcy';
 return 'ugEffective';
}
export function calculateUndergroundLab(kind,v) {
 const lab=UNDERGROUND_LABS[kind];if(!lab)return null;
 for(const [key,label,min,max] of lab.params)if(!Number.isFinite(v[key]) || v[key]<min-1e-12 || v[key]>max+1e-12)throw new RangeError(`${key}: ${min} ≤ value ≤ ${max}`);
 const pi=Math.PI;
 if(kind==='ugEffective'){if(v.head>v.depth)throw new RangeError('h ≤ z required in this simplified ground model / 本簡化模型要求水頭不高於地表');return v.gamma*v.depth-9.81*v.head;}
 if(kind==='ugHydro')return 9.81*v.head;
 if(kind==='ugThrust')return v.pressure*pi*v.diameter**2/4000;
 if(kind==='ugAdvance')return v.penetration*v.rpm*60*v.hours*v.utilization/1000;
 if(kind==='ugSettlement')return v.loss/100*pi*v.diameter**2/4/(Math.sqrt(2*pi)*v.width)*1000;
 if(kind==='ugDarcy')return 3600*v.k*v.area*v.head/v.length;
 if(kind==='ugRing'){if(v.thickness/v.radius>.1+1e-12)throw new RangeError('t/R ≤ 0.1 required / 薄環模型要求厚徑比≤0.1');return v.pressure*v.radius/v.thickness;}
 if(kind==='ugBolts')return Math.ceil(v.pressure*v.area/(v.capacity*v.efficiency));
 if(kind==='ugBuoyancy')return v.weight/(9.81*v.volume);
 if(kind==='ugConsolidation')return .848*v.drainage**2/v.cv;
 if(kind==='ugVent')return v.resistance*v.flow**3/v.efficiency/1000;
 if(kind==='ugSurvey')return Math.hypot(v.one,v.two,v.three);
 if(kind==='ugGrout'){if(v.outer<=v.inner)throw new RangeError('Do > Di required / 開挖外徑必須大於襯砌外徑');return pi*(v.outer**2-v.inner**2)*v.length*v.factor/4;}
 return null;
}
export function undergroundLabDetail(kind,v,zh=true){
 if(!UNDERGROUND_LABS[kind])return '';
 if(kind==='ugVent')return `Δp = ${(v.resistance*v.flow**2).toFixed(1)} Pa`;
 if(kind==='ugSettlement')return `VL × A = ${(v.loss/100*Math.PI*v.diameter**2/4).toFixed(4)} m²`;
 return zh?'合成教學輸入；請同時閱讀適用範圍。':'Synthetic teaching inputs; read the applicability limits.';
}
