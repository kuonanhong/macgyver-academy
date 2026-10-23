/* Original V17 scene state and projection. No DOM, network or animation on import. */
import {SCENE_MODELS, sceneModelFor, sceneDefaults, calculateSceneModel, projectArchitecture, resolveScenePhoto} from './immersive-v16.js';

export const text=(value,en=false)=>Array.isArray(value)?String(value[en?1:0]??value[0]??''):String(value??'');
export const clamp=(v,a,b)=>Math.max(a,Math.min(b,v));
export const CATEGORIES={
 semiconductor:{title:['晶圓製程實驗室','Wafer process laboratory'],shape:'wafer',color:'#74d6e8',instrument:['晶圓與製程腔體','Wafer and process chamber'],sensor:['溫度與膜厚量測站','Temperature and film metrology']},
 packaging:{title:['先進封裝整合實驗室','Advanced packaging laboratory'],shape:'package',color:'#efb377',instrument:['封裝剖面與互連載台','Package section and interconnect stage'],sensor:['熱像與接點量測站','Thermal and joint metrology']},
 electronics:{title:['電子電路量測台','Electronics test bench'],shape:'circuit',color:'#c4a5ff',instrument:['低壓電路與負載板','Low-voltage circuit and load board'],sensor:['電壓電流量測站','Voltage and current meters']},
 computing:{title:['運算與資訊系統實驗室','Computing and information laboratory'],shape:'rack',color:'#6dc3f2',instrument:['運算節點與網路機櫃','Compute nodes and network rack'],sensor:['時間戳與吞吐量探針','Timestamp and throughput probes']},
 structures:{title:['橋梁與結構試驗場','Bridge and structure test yard'],shape:'bridge',color:'#edc97b',instrument:['橋梁縮尺構架','Scale bridge frame'],sensor:['荷重元與位移量測站','Load cells and displacement station']},
 underground:{title:['地下工程觀測站','Underground engineering station'],shape:'tunnel',color:'#b9c2cc',instrument:['隧道襯砌與支撐模型','Tunnel lining and support model'],sensor:['收斂與應變觀測點','Convergence and strain observations']},
 water:{title:['水工與海岸水槽','Hydraulics and coastal flume'],shape:'dam',color:'#5bd5dd',instrument:['水槽、閘門與水輪機','Flume, gate and turbine'],sensor:['流量與水頭測點','Discharge and head measurements']},
 rail:{title:['鐵道與交通試驗線','Rail and transport test track'],shape:'train',color:'#f3ad65',instrument:['軌道與試驗車','Track and test vehicle'],sensor:['輪速與位置感測器','Wheel speed and position sensors']},
 environment:{title:['環境與城市實驗場','Environment and urban laboratory'],shape:'tanks',color:'#64d9af',instrument:['水處理與資源循環流程','Treatment and resource recovery process'],sensor:['流量與濃度監測站','Flow and concentration station']},
 aerospace:{title:['航空與風洞實驗室','Aerospace and wind tunnel laboratory'],shape:'aircraft',color:'#8ed4b4',instrument:['機翼與風洞測試段','Wing and wind-tunnel section'],sensor:['氣流探針與六分力天平','Flow probes and force balance']},
 space:{title:['太空載荷與光學實驗室','Space payload and optics laboratory'],shape:'satellite',color:'#acafff',instrument:['太空載荷與展開結構','Space payload and deployed structure'],sensor:['光譜與姿態量測站','Spectral and attitude metrology']},
 instruments:{title:['精密儀器與光學實驗室','Precision instrumentation and optics'],shape:'optical',color:'#bda6fa',instrument:['光學平台與對準組件','Optical bench and alignment modules'],sensor:['光譜與位置探測器','Spectrum and position detectors']},
 materials:{title:['材料與力學試驗室','Materials and mechanics laboratory'],shape:'frame',color:'#e7c578',instrument:['材料試件與負載框架','Specimen and loading frame'],sensor:['應變規與荷重元','Strain gauges and load cells']},
 energy:{title:['能源轉換與熱管理站','Energy conversion and heat station'],shape:'turbine',color:'#f2be66',instrument:['能源轉換試驗機組','Energy conversion test unit'],sensor:['功率與溫度量測站','Power and temperature station']},
 process:{title:['化工與程序工程教學台','Process engineering teaching plant'],shape:'reactor',color:'#efa899',instrument:['反應槽與換熱流程','Vessels and heat exchange process'],sensor:['溫度與物料流監測','Temperature and material-flow station']},
 marine:{title:['船舶與海洋工程水槽','Marine and ocean engineering basin'],shape:'ship',color:'#61bcd6',instrument:['船體與推進試驗模型','Hull and propulsion model'],sensor:['流速與水頭量測站','Flow speed and head station']},
 manufacturing:{title:['製造與機械實作場','Manufacturing and machinery workshop'],shape:'robot',color:'#eaa588',instrument:['工具機與機械臂教具','Machine tool and robotic teaching rig'],sensor:['溫度與定位量測站','Temperature and positioning station']},
 automotive:{title:['車輛與底盤試驗場','Vehicle and chassis test yard'],shape:'car',color:'#f39b77',instrument:['車體與制動台架','Vehicle and braking rig'],sensor:['速度與位移感測器','Speed and displacement sensors']},
 biomedical:{title:['生醫與微流體實驗室','Biomedical and microfluidics laboratory'],shape:'microfluidic',color:'#b2ddd1',instrument:['微流道與透明流體教具','Microchannels and transparent flow rig'],sensor:['壓差與流量量測站','Pressure and flow station']},
 megascience:{title:['大型科學設施觀測台','Large science facility station'],shape:'ring',color:'#afaafa',instrument:['環形光束線與探測器模型','Ring beamline and detector model'],sensor:['光譜與訊號量測站','Spectrum and signal station']}
};
const p=(id,zh,en,min,max,step,value,unit)=>({id,label:[zh,en],min,max,step,value,unit});
export const ENVIRONMENT_MODELS={
 removal:{title:['水處理質量守恆','Treatment mass balance'],formula:'Lᵢₙ = Q Cᵢₙ / 1000; Cₒᵤₜ = Cᵢₙ(1 − η/100)',unit:'kg/d',result:['去除污染物負荷','Removed constituent load'],params:[p('flow','流量','Flow',100,20000,100,5000,'m³/d'),p('concentration','進流濃度','Influent concentration',10,500,5,200,'mg/L'),p('removal','假設去除率','Assumed removal',0,100,1,80,'%')],scope:['穩態、等進出流量、單一組分，去除率是教學假設，未描述反應動力學或保證水質。','Steady equal inlet/outlet flows for one constituent. Removal is a teaching assumption, not reaction kinetics or a water-quality guarantee.'],challenge:['保持流量與濃度，只提高去除率；檢查去除量與排出量之和是否等於進流量。','Keep flow and concentration fixed and increase removal. Check that removed plus discharged load equals incoming load.'],source:'https://www.epa.gov/npdes/municipal-wastewater'},
 runoff:{title:['降雨逕流與滯留體積','Rainfall runoff and storage'],formula:'V = P A C / 1000; Vₒᵥₑᵣ = max(V − S, 0)',unit:'m³',result:['事件溢流體積','Event overflow volume'],params:[p('rain','事件雨深','Event rainfall',5,200,5,50,'mm'),p('area','集水面積','Catchment area',100,10000,100,2000,'m²'),p('coefficient','逕流係數','Runoff coefficient',.1,1,.05,.7,''),p('storage','可用滯留空間','Available storage',0,1000,10,40,'m³')],scope:['單一事件體積預算；忽略時間分布、排水過程與入滲動態，不能預測洪峰、水位或真實淹水。','Single-event volume budget. Rainfall timing, routing and infiltration dynamics are omitted; this does not predict peak flow, water level or actual flooding.'],challenge:['固定降雨與面積，增加滯留體積；觀察溢流何時降到零及零以下為何不合理。','Keep rainfall and area fixed and increase storage. Find when overflow reaches zero and why negative overflow is invalid.'],source:'https://www.epa.gov/green-infrastructure'},
 sorting:{title:['資源分選的回收與純度','Resource recovery and purity'],formula:'Mᵣ = M f r/10000; M꜀ = M(1−f/100)c/100; purity = Mᵣ/(Mᵣ+M꜀)',unit:'%',result:['產品純度','Product purity'],params:[p('feed','進料總質量','Feed mass',100,10000,100,1000,'kg'),p('fraction','目標材料比例','Target material fraction',5,95,5,40,'%'),p('recovery','目標回收率','Target recovery',10,100,5,80,'%'),p('carryover','非目標夾帶率','Non-target carryover',0,50,1,5,'%')],scope:['兩種組分、一次分選、固定回收與夾帶比例；未含含水率、細粒、品質分級與循環回料。','Two constituents, one separation pass and fixed recovery/carryover fractions. Moisture, fines, product grades and recirculation are omitted.'],challenge:['只降低非目標夾帶率，分辨純度提升與目標回收量是否為同一件事。','Reduce only non-target carryover. Distinguish increased purity from increased recovered target mass.'],source:'https://www.epa.gov/recycle'},
 emission:{title:['排氣流量與去除質量','Gas flow and removed mass'],formula:'mᵣ = Q C η / 10⁸; mₒᵤₜ = Q C(1−η/100)/10⁶',unit:'kg/h',result:['污染物去除質量率','Constituent removal rate'],params:[p('gasflow','排氣體積流量','Gas volumetric flow',1000,100000,1000,20000,'m³/h'),p('concentration','入口質量濃度','Inlet mass concentration',10,1000,10,100,'mg/m³'),p('efficiency','假設去除效率','Assumed removal efficiency',0,100,1,90,'%')],scope:['流量與濃度必須採相同溫壓與乾濕基準；簡化質量收支不是排放合規判定，未含氧校正與設備動態。','Flow and concentration must share temperature, pressure and dry/wet basis. This mass balance is not a compliance determination; oxygen correction and device dynamics are omitted.'],challenge:['保持流量與效率，把入口濃度加倍；檢查去除與出口質量率都如何改變。','Keep flow and efficiency fixed and double inlet concentration. Compare the removed and discharged mass rates.'],source:'https://www.epa.gov/air-emissions-monitoring-knowledge-base'},
 acoustic:{title:['屏障衰減與背景噪音','Barrier attenuation and background sound'],formula:'L = 10 log₁₀[10^((Lₛ−IL)/10) + 10^(Lᵦ/10)]',unit:'dB',result:['合成聲級','Combined sound level'],params:[p('source','目標源接收聲級','Target-source received level',40,100,1,75,'dB'),p('background','背景聲級','Background level',30,80,1,50,'dB'),p('loss','假想插入損失','Assumed insertion loss',0,25,1,10,'dB')],scope:['兩個互不相干聲源且聲級採相同頻帶與時間基準；插入損失是教學輸入，未從屏障幾何或繞射計算。','Two incoherent sources on identical frequency and time bases. Insertion loss is a teaching input, not a prediction from barrier geometry or diffraction.'],challenge:['增加目標源衰減，觀察總聲級為何逐漸受到背景聲級限制。','Increase target-source attenuation and observe the floor imposed by background sound.'],source:'https://www.fhwa.dot.gov/environment/noise/noise_barriers/'},
 heatflow:{title:['顯熱流與溫差收支','Sensible-heat flow and temperature difference'],formula:'P = ṁ cₚ ΔT',unit:'kW',result:['顯熱傳遞率','Sensible-heat transfer rate'],params:[p('massflow','質量流率','Mass flow',.1,20,.1,2,'kg/s'),p('capacity','假設比熱','Assumed specific heat',.5,5,.1,4.2,'kJ/(kg·K)'),p('difference','進出口溫差大小','Inlet/outlet temperature difference',1,100,1,10,'K')],scope:['穩態、固定比熱、單一流體、只計顯熱；不含相變、燃燒、生物反應、散熱或設備效率，不能據此推算蒸汽產量或生物處理性能。','Steady single-fluid sensible heat with fixed specific heat. Phase change, combustion, biological reactions, heat loss and equipment efficiency are excluded; this cannot predict steam production or treatment performance.'],challenge:['保持流率與比熱，將溫差加倍；核對熱流率與 kJ/s = kW。','Keep mass flow and specific heat fixed, double the temperature difference, and check kJ/s = kW.'],source:'https://openstax.org/books/university-physics-volume-2/pages/1-4-heat-transfer-specific-heat-and-calorimetry'},
 fluidpower:{title:['低壓差輸送與輸入功率','Low-pressure fluid transport and input power'],formula:'Pᵢₙ = Δp Q /(1000 η)',unit:'kW',result:['假想輸入功率','Assumed input power'],params:[p('pressure','壓差','Pressure difference',100,5000,100,2000,'Pa'),p('flow','工作狀態體積流率','Operating volumetric flow',.01,2,.01,.2,'m³/s'),p('efficiency','假設總效率','Assumed total efficiency',.1,1,.05,.7,'')],scope:['小壓差、密度近似固定，流量與壓力為同一工作點，效率是外加教學輸入；不含氣體壓縮、大真空、固體堵塞、風機曲線或水擊，也不預測實際輸送能力。','Small pressure differences and approximately constant density, with pressure and flow at one operating point. Efficiency is an assumed input. Gas compression, deep vacuum, solids blockage, fan curves and water hammer are excluded; conveying capacity is not predicted.'],challenge:['保持壓差與流量，降低效率；比較流體功率 ΔpQ 與輸入功率的差異。','Keep pressure difference and flow fixed and lower efficiency. Distinguish fluid power ΔpQ from input power.'],source:'https://openstax.org/books/university-physics-volume-1/pages/14-6-bernoullis-equation'},
 calibration:{title:['線性量測偏差與校正','Linear measurement bias and correction'],formula:'y = a x + b; x = (y − b)/a',unit:'a.u.',result:['校正後讀值','Corrected reading'],params:[p('reading','儀器原始讀值','Raw instrument reading',0,100,1,50,'a.u.'),p('gain','斜率／增益','Slope / gain',.5,1.5,.05,1.1,''),p('offset','零點偏差','Zero offset',-10,10,1,2,'a.u.')],scope:['任意單位的線性量測鏈，斜率與偏差是假想獨立校正結果；不含交互干擾、非線性、偵測極限或長期漂移，不能證明排放、水質或場址風險合格。','A linear measurement chain in arbitrary units; gain and offset are hypothetical independent calibration results. Interference, nonlinearity, detection limits and long-term drift are omitted. This does not certify emissions, water quality or site risk.'],challenge:['保持原始讀值，分別改變零點偏差與增益；核對校正後的值是否滿足原量測方程。','Keep the raw reading fixed and vary offset and gain separately. Check the corrected value against the measurement equation.'],source:'https://www.nist.gov/pml/weights-and-measures'}
};
// Explicitly reviewed course-to-warm-up mapping. A warm-up illustrates one
// transferable balance, not the full named facility or every authored unit.
export const ENVIRONMENT_COURSE_MODELS={
 b401:'removal',b402:'fluidpower',b403:'removal',b404:'runoff',b405:'runoff',b406:'heatflow',b407:'heatflow',b408:'removal',b409:'removal',b410:'removal',
 b411:'removal',b412:'removal',b413:'heatflow',b414:'heatflow',b415:'runoff',b416:'runoff',b417:'sorting',b418:'runoff',b419:'removal',b420:'runoff',
 b421:'removal',b422:'removal',b423:'removal',b424:'removal',b425:'removal',b426:'removal',b427:'removal',b428:'removal',b429:'removal',b430:'removal',
 b431:'heatflow',b432:'heatflow',b433:'sorting',b434:'sorting',b435:'heatflow',b436:'emission',b437:'fluidpower',b438:'removal',b439:'removal',b440:'runoff',
 b441:'fluidpower',b442:'emission',b443:'removal',b444:'removal',b445:'removal',b446:'fluidpower',b447:'removal',b448:'removal',b449:'removal',b450:'removal',
 b451:'removal',b452:'removal',b453:'removal',b454:'calibration',b455:'removal',b456:'runoff',b457:'runoff',b458:'runoff',b459:'runoff',b460:'runoff',
 b461:'heatflow',b462:'fluidpower',b463:'heatflow',b464:'heatflow',b465:'heatflow',b466:'fluidpower',b467:'sorting',b468:'sorting',b469:'sorting',b470:'sorting',
 b471:'sorting',b472:'sorting',b473:'sorting',b474:'sorting',b475:'sorting',b476:'heatflow',b477:'heatflow',b478:'fluidpower',b479:'heatflow',b480:'heatflow',
 b481:'sorting',b482:'sorting',b483:'emission',b484:'emission',b485:'emission',b486:'runoff',b487:'removal',b488:'emission',b489:'runoff',b490:'sorting',
 b491:'emission',b492:'removal',b493:'removal',b494:'removal',b495:'calibration',b496:'calibration',b497:'calibration',b498:'acoustic',b499:'emission',b500:'sorting'
};
const ENVIRONMENT_WARMUP_NOTES={
 removal:['此課先練習單一成分的進出質量收支；假定效率不等於已驗證的消毒、膜阻隔或生物反應能力。','Begin with an inlet/outlet mass balance for one constituent; assumed efficiency does not establish disinfection, membrane-barrier or biological performance.'],
 runoff:['此課先估計入水與儲存的事件體積；不是管網水力、滲流、防水層完整性或都市淹水模擬。','Begin with event inflow and storage volume; this is not sewer hydraulics, seepage, liner integrity or an urban flood simulation.'],
 sorting:['此課先比較目標成分回收率與產品純度；目標成分為假想材料，不代表已驗證污染物消除、洗滌品質、穩定化或完整生命週期。','Begin by comparing hypothetical target recovery and product purity; this does not validate contaminant destruction, washing quality, stabilization or a complete life cycle.'],
 emission:['此課先核對氣流中的單一成分質量率；成分去向需另行追蹤，不能把移除量等同於反應、燃燒、破壞或安全釋放。','Begin with the mass rate of one constituent in a gas stream; track its destination separately. Removal does not establish reaction, combustion, destruction or safe release.'],
 heatflow:['此課僅以假想流體比較供熱或取熱量；不是熱泵COP、沸騰／蒸汽、厭氧消化、堆肥、焚化反應或負載預測模型。','Compare heating or cooling of a hypothetical fluid only; this is not a heat-pump COP, boiling/steam, digestion, composting, incineration or load-forecast model.'],
 fluidpower:['此課只練習壓差、流率與功率的關係；空氣／水輸送能力、都市風場、曝氣傳氧及固體移動仍需各自模型。','Practice the pressure-flow-power relationship only; air/water conveying capacity, urban wind fields, oxygen transfer and solids transport need their own models.'],
 calibration:['此課先拆分增益與零點偏差；風險、品質與合規還需要代表採樣、量測不確定度及適用判準。','Separate gain from zero offset first; risk, quality and compliance also require representative samples, uncertainty and applicable criteria.'],
 acoustic:['此課先比較目標源衰減與背景聲級；不從真實屏障幾何計算繞射。','Compare target-source attenuation with background level first; actual barrier geometry and diffraction are not calculated.']
};
export function modelKind(course={}){
 if(course.category!=='environment')return sceneModelFor(course);
 return ENVIRONMENT_COURSE_MODELS[course.id]||'removal';
}
export function getModel(course={}){
 const kind=modelKind(course),base=ENVIRONMENT_MODELS[kind]||SCENE_MODELS[kind];
 if(course.category!=='environment')return {kind,...base};
 const note=ENVIRONMENT_WARMUP_NOTES[kind]||['',''];
 return {kind,...base,title:['本課暖身：'+base.title[0],'Course warm-up: '+base.title[1]],scope:[note[0]+' '+base.scope[0]+' 各單元的專屬算例請進入逐步工作台。',note[1]+' '+base.scope[1]+' Open the workbench for each unit’s dedicated calculation.']};
}
export function defaults(course={}){return Object.fromEntries(getModel(course).params.map(p=>[p.id,p.value]));}
export function calculate(course,values){
 const m=getModel(course);if(!ENVIRONMENT_MODELS[m.kind])return calculateSceneModel(m.kind,values);
 for(const p of m.params)if(!Number.isFinite(values[p.id])||values[p.id]<p.min-1e-9||values[p.id]>p.max+1e-9)throw new RangeError(p.id+' outside teaching range');
 let value,detail={};
 if(m.kind==='removal'){const incoming=values.flow*values.concentration/1000;value=incoming*values.removal/100;detail={incomingLoad:incoming,dischargedLoad:incoming-value,outletConcentration:values.concentration*(1-values.removal/100)};}
 if(m.kind==='runoff'){const runoff=values.rain*values.area*values.coefficient/1000;value=Math.max(0,runoff-values.storage);detail={runoffVolume:runoff,retainedVolume:Math.min(runoff,values.storage)};}
 if(m.kind==='sorting'){const recovered=values.feed*values.fraction*values.recovery/10000,contamination=values.feed*(1-values.fraction/100)*values.carryover/100;value=100*recovered/(recovered+contamination);detail={recoveredTarget:recovered,nonTargetCarryover:contamination,rejectMass:values.feed-recovered-contamination};}
 if(m.kind==='emission'){const incoming=values.gasflow*values.concentration/1e6;value=incoming*values.efficiency/100;detail={incomingMassRate:incoming,dischargedMassRate:incoming-value};}
 if(m.kind==='heatflow'){value=values.massflow*values.capacity*values.difference;detail={heatCapacityRate:values.massflow*values.capacity};}
 if(m.kind==='fluidpower'){const fluidPower=values.pressure*values.flow/1000;value=fluidPower/values.efficiency;detail={fluidPower,assumedLoss:value-fluidPower};}
 if(m.kind==='calibration'){value=(values.reading-values.offset)/values.gain;detail={rawReading:values.reading,reconstructedReading:values.gain*value+values.offset};}
 if(m.kind==='acoustic'){value=10*Math.log10(10**((values.source-values.loss)/10)+10**(values.background/10));detail={attenuatedSource:values.source-values.loss,backgroundLevel:values.background};}
 return {kind:m.kind,value,unit:m.unit,detail};
}
export function profile(course={}){
 const c=CATEGORIES[course.category]||CATEGORIES.manufacturing,m=getModel(course);
 if(course.category!=='environment')return {...c};
 const variants={
  removal:{shape:'tanks',instrument:['水處理質量收支教具','Water-treatment mass-balance rig'],sensor:['流量與濃度監測站','Flow and concentration station']},
  runoff:{shape:'park',instrument:['集水面與滯留設施模型','Catchment and storage model'],sensor:['雨量、體積與水位紀錄','Rainfall, volume and level records']},
  sorting:{shape:'recycler',instrument:['材料分選與回收教具','Material separation and recovery rig'],sensor:['秤重與組成抽樣站','Weighing and composition sampling']},
  emission:{shape:'stack',instrument:['氣流成分收支教具','Gas-stream constituent balance rig'],sensor:['氣體流量與濃度量測','Gas flow and concentration measurements']},
  heatflow:{shape:'reactor',instrument:['顯熱交換與流體迴路','Sensible-heat exchange and fluid loop'],sensor:['質量流率與溫差量測','Mass-flow and temperature-difference measurements']},
  fluidpower:{shape:'tanks',instrument:['低壓差輸送試驗迴路','Low-pressure transport test loop'],sensor:['壓差、流量與功率量測','Pressure, flow and power measurements']},
  calibration:{shape:'optical',instrument:['參考樣本與量測校正台','Reference and instrument calibration bench'],sensor:['參考值與原始讀值比較','Reference and raw-reading comparison']},
  acoustic:{shape:'frame',instrument:['聲源與屏障框架教具','Sound-source and barrier-frame rig'],sensor:['同頻帶與時間基準聲級','Sound levels on a common band/time basis']}
 };
 return {...c,...variants[m.kind]};
}
export function courseNodes(course={}){
 // V17 authors may use a bilingual ~ string; normalize before legacy parsing.
 const source=course.v17Architecture||course.v16Architecture||course;
 const nodes=(source.architectureNodes||[]).map(n=>typeof n==='string'&&n.includes('~')?n.split('~',2):n);
 return projectArchitecture({...course,v16Architecture:{...source,architectureNodes:nodes}});
}
export function safeAssetPath(value){return typeof value==='string'&&/^(?:\.\/)?assets\/[A-Za-z0-9_./-]+$/.test(value)&&!value.split('/').includes('..')?value:'';}
export function safeHttps(value){try{const u=new URL(value);return u.protocol==='https:'?u.href:'';}catch{return '';}}
export function assetChoices(course={},options={}){
 const a=options.sceneAssets||{},all=a.assets||[],ids=[];
 const exact=a.courses?.[course.id];if(exact?.assetIds)ids.push(...exact.assetIds);
 const def=a.categoryDefaults?.[course.category];if(typeof def==='string')ids.push(def);
 ids.push(...(a.categoryPhotoSets?.[course.category]||[]));
 ids.push(...(a.panoramaSets?.[course.category]||[]));
 all.filter(x=>x.courseIds?.includes(course.id)).forEach(x=>ids.push(x.id));
 if(!ids.length)all.filter(x=>x.categories?.includes(course.category)).forEach(x=>ids.push(x.id));
 const chosen=[...new Set(ids)].map(id=>all.find(x=>x.id===id)).filter(Boolean).filter(x=>safeAssetPath(x.path||x.src)||(x.remoteOnly&&safeHttps(x.src)));
 if(!chosen.length){const old=resolveScenePhoto(course,options.photos,options.scenePhotos);if(old)chosen.push({...old.photo,projection:'flat',match:old.match,note:old.note,noteEn:old.noteEn});}
 return chosen;
}
export function isPanorama(asset){return asset?.projection==='equirectangular'&&asset?.photoType==='real-panorama'&&asset.width>0&&asset.height>0&&Math.abs(asset.width/asset.height-2)<.03;}
export function panoramaUV(yaw,pitch){return {u:((yaw/(2*Math.PI)+.5)%1+1)%1,v:clamp(.5-pitch/Math.PI,0,1)};}
const sub=(a,b)=>a.map((v,i)=>v-b[i]),dot=(a,b)=>a.reduce((v,x,i)=>v+x*b[i],0),norm=a=>{const n=Math.hypot(...a);return a.map(v=>v/n);},cross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]];
export function camera(view='third',yaw=.5,pitch=.45,zoom=1,target=[0,.8,0]){
 zoom=clamp(zoom,.5,2);let position,forward;
 if(view==='first'){position=[0,1.55,4.6];forward=norm([Math.sin(yaw)*Math.cos(pitch),Math.sin(pitch),-Math.cos(yaw)*Math.cos(pitch)]);}
 else {const d=(view==='second'?6:11.8)/zoom;position=[target[0]+Math.sin(yaw)*Math.cos(pitch)*d,target[1]+Math.sin(pitch)*d,target[2]+Math.cos(yaw)*Math.cos(pitch)*d];forward=norm(sub(target,position));}
 const right=norm(cross(forward,[0,1,0])),up=cross(right,forward);return {position,forward,right,up,fov:view==='first'?75/zoom:65};
}
export function project(point,camera,width,height){const d=sub(point,camera.position),depth=dot(d,camera.forward);if(depth<=.08)return null;const scale=height/(2*Math.tan(camera.fov*Math.PI/360)*depth);return {x:width/2+dot(d,camera.right)*scale,y:height*.54-dot(d,camera.up)*scale,depth,scale};}
export function newProgress(){return {observed:false,selected:false,changed:false,recorded:false,assisted:[],history:[]};}
export function nextPhase(p){return !p.observed?'observe':!p.selected?'select':!p.changed?'adjust':!p.recorded?'record':'complete';}
export function completePhase(progress,phase,assisted=false){const next={...progress,assisted:[...(progress.assisted||[])]};const field={observe:'observed',select:'selected',adjust:'changed',record:'recorded'}[phase];if(!field)return next;if(phase==='record'&&(!progress.observed||!progress.selected||!progress.changed))return next;next[field]=true;if(assisted&&!next.assisted.includes(phase))next.assisted.push(phase);return next;}
export function restoreProgress(value,course){const p=newProgress();if(!value||typeof value!=='object')return p;for(const k of ['observed','selected','changed','recorded'])p[k]=value[k]===true;p.assisted=Array.isArray(value.assisted)?value.assisted.filter(x=>['observe','select','adjust','record'].includes(x)):[];p.history=Array.isArray(value.history)?value.history.filter(h=>h&&typeof h.at==='string'&&Number.isFinite(h.value)&&h.kind===modelKind(course)).slice(-20):[];return p;}
