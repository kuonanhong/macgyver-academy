/* Original V22 walkable teaching facilities. Geometry is an illustrative model;
 * credited photographs remain reference evidence, not photogrammetric geometry.
 * Coordinates are metres in the teaching world, not dimensions of an actual site.
 */

const station = (kind, name, nameEn, x, z) => ({kind, equipmentTitle:name, equipmentTitleEn:nameEn, x, z});
const profile = (layout, color, width, depth, stations) => ({layout,color,bounds:{width,depth},stations});

export const DOMAIN_PROFILES_V22 = Object.freeze({
  semiconductor: profile('cleanroom','#55d5e3',30,38,[
    station('instrument','元件與晶圓量測平台','Device and wafer metrology',-8,11),
    station('tank','濕式清洗站','Wet cleaning station',8,11),
    station('lithography','微影曝光模組','Lithography exposure module',8,1),
    station('lithography','薄膜與蝕刻腔體','Thin-film and etch chamber',-8,1),
    station('robot','互連與搬送站','Interconnect and transfer station',-8,-10),
    station('instrument','探針與電性驗證台','Probe and electrical validation',8,-10)
  ]),
  packaging: profile('cleanroom','#ba9aff',34,36,[
    station('bench','晶粒與載具工作台','Die and carrier workbench',-10,10),
    station('instrument','對準與介面量測','Alignment and interface metrology',9,11),
    station('bench','載板與訊號路徑台','Substrate and signal-path bench',10,1),
    station('robot','精密接合工作站','Precision bonding workstation',-9,0),
    station('tank','熱管理試驗站','Thermal-management test station',-10,-10),
    station('rack','系統測試機櫃','System test rack',9,-9)
  ]),
  electronics: profile('lab','#f3c66b',30,34,[
    station('bench','材料與電路工作台','Materials and circuit workbench',-8,9),
    station('robot','製作與加工站','Fabrication and machining station',8,10),
    station('bench','繞組與組裝台','Winding and assembly bench',8,0),
    station('instrument','訊號與平衡量測','Signal and balance measurement',-8,-1),
    station('tank','熱與冷卻驗證','Thermal and cooling validation',-8,-10),
    station('rack','上電與負載試驗','Power-up and load testing',8,-9)
  ]),
  computing: profile('lab','#65aaff',32,40,[
    station('bench','系統邊界工作台','System-boundary workbench',-9,12),
    station('rack','分區網路機櫃','Segmented network rack',9,12),
    station('rack','運算與存取節點','Compute and access node',-9,1),
    station('rack','日誌與觀測節點','Logging and observability node',9,1),
    station('rack','備援與復原機櫃','Backup and recovery rack',9,-11),
    station('instrument','結果與證據檢查台','Results and evidence review',-9,-11)
  ]),
  instruments: profile('lab','#94e0c3',28,36,[
    station('bench','規格與參考標準台','Specification and reference bench',-7,10),
    station('instrument','光學路徑平台','Optical-path platform',7,10),
    station('instrument','定位與運動平台','Positioning and motion stage',7,0),
    station('instrument','對準與感測台','Alignment and sensing bench',-7,0),
    station('tank','溫度與振動試驗','Temperature and vibration testing',-7,-10),
    station('bench','誤差與校準工作台','Error and calibration workbench',7,-10)
  ]),
  structures: profile('outdoor','#e5bf73',42,42,[
    station('instrument','基地與高程量測','Site and elevation survey',-13,12),
    station('crane','基礎施工示意站','Foundation construction station',12,12),
    station('bridge','梁段與承載路徑','Girder and load-path model',12,1),
    station('crane','吊裝與纜索示意站','Lifting and cable station',-12,1),
    station('bridge','節段接合工作區','Segment joining work area',-13,-12),
    station('instrument','應變與位移觀測','Strain and displacement monitoring',12,-12)
  ]),
  underground: profile('yard','#d4a37a',36,44,[
    station('instrument','路線與地表調查','Alignment and surface survey',-10,14),
    station('bench','地層與岩芯工作台','Geology and core workbench',10,13),
    station('tank','湧水與排水試驗','Ingress and drainage testing',10,2),
    station('robot','開挖與支撐示意機','Excavation and support model',-10,1),
    station('instrument','收斂與沉陷觀測','Convergence and settlement monitoring',-10,-12),
    station('turbine','通風與維護站','Ventilation and maintenance station',10,-12)
  ]),
  water: profile('outdoor','#5ebfe0',40,44,[
    station('instrument','流域流量觀測','Catchment flow monitoring',-12,14),
    station('tank','儲水與水位示意槽','Storage and level model tank',12,13),
    station('bridge','水工構造示意台','Hydraulic structure model',12,2),
    station('tank','泄流與消能試驗','Discharge and energy-dissipation test',-12,1),
    station('turbine','水輪與能量轉換','Hydraulic turbine and conversion',-12,-12),
    station('instrument','下游水文觀測','Downstream hydrological monitoring',12,-12)
  ]),
  rail: profile('hangar','#d9a45b',40,46,[
    station('tank','能源與流體供應','Energy and fluid supply',-12,15),
    station('turbine','動力與能量轉換','Traction energy conversion',12,14),
    station('train','傳動與走行部','Transmission and running gear',12,2),
    station('train','輪軌接觸示意台','Wheel–rail contact model',-12,2),
    station('bench','制動與控制介面','Braking and control interfaces',-12,-13),
    station('instrument','車輛檢查與量測','Vehicle inspection and measurement',12,-13)
  ]),
  environment: profile('outdoor','#88c790',38,42,[
    station('instrument','環境與來水採樣','Environment and influent sampling',-11,12),
    station('tank','前處理示意槽','Pretreatment model vessel',11,13),
    station('tank','分離與處理模組','Separation and treatment module',11,1),
    station('bench','屏障與再利用工作台','Barrier and reuse workbench',-11,0),
    station('instrument','品質與排放量測','Quality and discharge measurement',-11,-11),
    station('rack','城市系統資料台','Urban-system data station',11,-12)
  ]),
  aerospace: profile('hangar','#a3c8f2',44,46,[
    station('bench','任務規格工作台','Mission specification workbench',-14,15),
    station('aircraft','氣動與外形示意機','Aerodynamic configuration model',14,14),
    station('aircraft','機體結構與介面','Airframe structure and interfaces',14,2),
    station('robot','航空製造與接合','Aerospace fabrication and joining',-14,1),
    station('turbine','推進與系統整合','Propulsion and systems integration',-14,-13),
    station('instrument','驗證與感測試驗台','Validation and sensing bench',14,-13)
  ]),
  marine: profile('yard','#63c1c3',44,44,[
    station('instrument','海況與水深觀測','Sea-state and depth observation',-14,13),
    station('tank','浮力與配重試驗','Buoyancy and ballast test',14,12),
    station('ship','船體與耐壓殼示意','Hull and pressure-vessel model',14,1),
    station('turbine','推進與能源站','Propulsion and energy station',-14,0),
    station('dish','海洋定位與通訊','Ocean positioning and communications',-14,-12),
    station('instrument','航行與任務驗證','Navigation and mission validation',14,-12)
  ]),
  automotive: profile('factory','#efaa65',40,42,[
    station('vehicle','需求與整車參考','Requirements and vehicle reference',-12,12),
    station('robot','車體加工與焊裝','Body fabrication and joining',12,12),
    station('tank','冷卻與儲能系統','Cooling and energy-storage system',12,0),
    station('vehicle','底盤與裝配工位','Chassis and assembly bay',-12,1),
    station('instrument','尺寸與品質檢查','Dimensional and quality inspection',-12,-12),
    station('vehicle','車輛驗證工作站','Vehicle validation workstation',12,-12)
  ]),
  space: profile('cleanroom','#aba5e9',38,40,[
    station('bench','任務與服務工作台','Mission and service workbench',-11,12),
    station('dish','軌道與覆蓋示意台','Orbit and coverage demonstrator',11,12),
    station('satellite','衛星載荷與平台','Spacecraft payload and bus',11,1),
    station('dish','星地通訊介面','Space-to-ground communication',-11,0),
    station('rack','時間與控制系統','Timing and control systems',-11,-11),
    station('vacuum','太空環境與效能驗證','Space environment and performance validation',11,-12)
  ]),
  manufacturing: profile('factory','#eebf6c',38,40,[
    station('bench','製程與工件工作台','Process and workpiece bench',-11,12),
    station('robot','機構與致動單元','Mechanism and actuation unit',11,11),
    station('robot','加工與協作單元','Machining and collaboration unit',11,0),
    station('rack','控制與紀錄機櫃','Control and logging rack',-11,0),
    station('crane','搬運與治具工作區','Handling and fixture work area',-11,-12),
    station('instrument','製程品質與驗證','Process quality and validation',11,-11)
  ]),
  energy: profile('outdoor','#e6cf6b',42,46,[
    station('tank','能源輸入與儲存','Energy input and storage',-13,15),
    station('bench','輸送與損失工作台','Conveyance and losses bench',13,14),
    station('turbine','一次能源轉換機組','Primary energy converter',13,2),
    station('turbine','旋轉電機示意站','Rotating electrical machine model',-13,1),
    station('rack','電網與保護介面','Grid and protection interface',-13,-13),
    station('instrument','能量收支量測','Energy balance measurement',13,-13)
  ]),
  materials: profile('factory','#e59a75',36,42,[
    station('bench','原料與試片工作台','Feedstock and specimen workbench',-10,13),
    station('furnace','爐體與加熱示意機','Furnace and heating model',10,13),
    station('tank','反應與成形單元','Reaction and forming unit',10,1),
    station('furnace','熱處理與冷卻單元','Heat treatment and cooling unit',-10,1),
    station('instrument','取樣與顯微檢查','Sampling and microscopy',-10,-12),
    station('bench','材料履歷與測試','Material traceability and testing',10,-12)
  ]),
  biomedical: profile('lab','#7cd5c2',32,38,[
    station('instrument','成像與感測幾何','Imaging and sensing geometry',-9,11),
    station('instrument','光源與偵測器模組','Source and detector module',9,11),
    station('rack','資料擷取與重建','Data acquisition and reconstruction',9,0),
    station('bench','定位與校準物件','Positioning and calibration objects',-9,0),
    station('rack','訊號與品質分析','Signal and quality analysis',-9,-11),
    station('instrument','假體與工程驗證','Phantom and engineering validation',9,-11)
  ]),
  process: profile('factory','#6cc6b0',40,44,[
    station('bench','物料與需求工作台','Material and requirements bench',-12,14),
    station('tank','容器與覆蓋介面','Vessel and enclosure interfaces',12,13),
    station('tank','流體與輸送單元','Fluid and conveyance unit',12,1),
    station('furnace','熱量與環境控制','Heat and environment control',-12,1),
    station('instrument','製程感測與採樣','Process sensing and sampling',-12,-12),
    station('rack','物料與資源盤點','Material and resource accounting',12,-12)
  ]),
  megascience: profile('lab','#9eaff0',46,44,[
    station('bench','科學目標與介面台','Science goals and interface bench',-15,13),
    station('instrument','激發與束流準備','Excitation and beam preparation',15,13),
    station('dish','傳輸與導引示意站','Transport and guidance model',15,1),
    station('instrument','偵測器與樣品站','Detector and sample station',-15,1),
    station('rack','同步與資料擷取','Timing and data acquisition',-15,-12),
    station('instrument','校準與交叉驗證','Calibration and cross-validation',15,-12)
  ])
});

const spaceEquipment = {
  1: ['bench','rack','satellite','bench','dish','rack'],
  2: ['rack','dish','satellite','rack','dish','instrument'],
  3: ['bench','rocket','tank','rocket','instrument','rack'],
  4: ['bench','satellite','robot','crane','instrument','vacuum'],
  5: ['bench','satellite','vacuum','rack','tank','instrument'],
  6: ['rack','instrument','satellite','robot','rack','vacuum'],
  7: ['rack','dish','satellite','dish','instrument','rack'],
  8: ['bench','instrument','satellite','rack','vacuum','dish'],
  9: ['bench','crane','satellite','vacuum','instrument','rack'],
  10: ['bench','rocket','robot','satellite','dish','vacuum'],
};
const spaceEquipmentNames = {
  bench: ['系統工程台','Systems workbench'], rack: ['任務控制與資料機櫃','Mission control and data rack'],
  satellite: ['衛星平台與展開式太陽能板','Spacecraft bus and deployable solar arrays'],
  dish: ['地面站天線與饋源','Ground-station antenna and feed'], instrument: ['量測與校準台','Measurement and calibration bench'],
  vacuum: ['熱真空驗證艙','Thermal vacuum chamber'], rocket: ['推進與分離示意台','Propulsion and separation demonstrator'],
  tank: ['流體與熱控示意槽','Fluid and thermal-control model'], robot: ['整合與載荷操作機械臂','Integration and payload handling robot'],
  crane: ['衛星搬運與吊裝平台','Spacecraft handling and lift fixture'],
};

/** Accept only bundled relative image paths. Blob/remote imports belong to their
 * existing dedicated viewer and must not initiate requests in this module. */
export function safePhotoPath(value) {
  if (typeof value !== 'string' || !/^assets\/[a-zA-Z0-9_./-]+\.(?:jpe?g|png|webp)$/i.test(value)) return '';
  if (value.split('/').some(part => !part || part === '.' || part === '..')) return '';
  return value;
}

function usablePhoto(asset) {
  return !!asset && !!safePhotoPath(asset.src || asset.path) && asset.projection !== 'equirectangular';
}

/** Build a fresh, mutable renderer configuration without changing the V21
 * catalogue. Existing chapter IDs remain the interaction/progress identities. */
export function buildWorldConfig(scene, assets = [], language = 'en') {
  if (!scene || typeof scene !== 'object') throw new TypeError('A journey is required.');
  const source = DOMAIN_PROFILES_V22[scene.category];
  if (!source) throw new RangeError('Unsupported engineering domain: ' + String(scene.category));
  const chapters = Array.isArray(scene.chapters) ? scene.chapters : [];
  if (!chapters.length || chapters.length > source.stations.length) throw new RangeError('A journey needs one to six chapters.');
  const assetList = Array.isArray(assets) ? assets : [];
  const spaceModule = scene.category === 'space' && Number.isInteger(scene.spaceModule) ? scene.spaceModule : 0;
  const moduleEquipment = spaceEquipment[spaceModule];
  const byId = new Map(assetList.filter(a => a && typeof a.id === 'string').map(a => [a.id,a]));
  const routePhotos = (Array.isArray(scene.assetIds) ? scene.assetIds : []).map(id => byId.get(id)).filter(usablePhoto);
  const stations = chapters.map((chapter, chapterIndex) => {
    const base = source.stations[chapterIndex];
    const kind = moduleEquipment?.[chapterIndex] || base.kind;
    const names = moduleEquipment ? spaceEquipmentNames[kind] : null;
    const exactPhoto = byId.get(chapter.assetId);
    const photo = usablePhoto(exactPhoto) ? exactPhoto : routePhotos[chapterIndex % Math.max(1,routePhotos.length)];
    return {
      ...base,
      kind,
      equipmentTitle: names?.[0] || base.equipmentTitle,
      equipmentTitleEn: names?.[1] || base.equipmentTitleEn,
      id: String(chapter.id || scene.id + '-chapter-' + (chapterIndex + 1)),
      chapterIndex,
      title: String(chapter.title || chapter.titleEn || ''),
      titleEn: String(chapter.titleEn || chapter.title || ''),
      // The process label is authoritative; the machinery is representative.
      photoSrc: photo ? safePhotoPath(photo.src || photo.path) : '',
      photoAssetId: photo?.id || '',
      photoMatch: photo ? (photo === exactPhoto ? 'chapter-reference' : 'journey-reference') : 'none',
      photoCredit: photo ? {title:photo.title || '',titleEn:photo.titleEn || '',author:photo.author || '',license:photo.license || '',sourceUrl:photo.sourceUrl || '',licenseUrl:photo.licenseUrl || ''} : null,
      approach: {x:base.x - Math.sign(base.x)*2.9,z:base.z}
    };
  });
  return {
    id:String(scene.id || scene.category),
    domainId:scene.category,
    title:String(scene.title || scene.titleEn || ''),
    titleEn:String(scene.titleEn || scene.title || ''),
    language,
    color:source.color,
    layout:spaceModule === 3 || spaceModule === 10 ? 'hangar' : source.layout,
    bounds:{...source.bounds},
    stations,
    scope:'illustrative-engineering-world-with-credited-photo-references'
  };
}
