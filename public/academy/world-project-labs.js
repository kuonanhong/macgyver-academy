/* Original bounded, steady-state educational balances, not operating settings. */
const lab=(title,formula,unit,params,note,question,source='')=>({title,formula,unit,params,note,question,source});
const p=(key,zh,en,min,max,step,value,unit)=>[key,[zh,en],min,max,step,value,unit];
export const WORLD_LABS={
 worldCarnot:lab(['熱機效率的理想上界','An ideal bound on heat-engine efficiency'],'η_C = 1 − T_cold / T_hot','%',[
 p('hot','熱源絕對溫度','Hot-reservoir temperature',400,1200,10,600,'K'),p('cold','冷源絕對溫度','Cold-reservoir temperature',280,350,1,300,'K')
 ],['可逆、兩熱庫熱機上界；不是核電或融合電廠實際效率。未含蒸汽循環、泵功、熱交換、冷卻條件與安全限制。','Reversible two-reservoir heat-engine bound, not nuclear or fusion plant efficiency. Steam-cycle details, pumping, heat exchangers, cooling and safety limits are excluded.'],['為何必须使用 Kelvin？同一理想上界下，實際淨發電仍需核算哪些耗能？','Why must temperature be in kelvin? What losses still determine net plant output at the same ideal bound?']),
 worldHeat:lab(['熱輸入與淨電力','Heat input and net electricity'],'P_net = Q_thermal × η_cycle − P_aux','MW',[
 p('heat','假想熱輸入','Assumed thermal input',100,4000,100,1000,'MW'),p('efficiency','假想循環效率','Assumed cycle efficiency',.20,.50,.01,.35,''),p('aux','輔助設備功率','Auxiliary consumption',0,150,5,20,'MW')
 ],['僅為穩態能量帳；效率與輔助耗能是教學假設，不是指定電廠的參數。負淨輸出表示此假設未達自供能，不能自動把負值截掉。','Steady-state energy accounting only. Efficiency and auxiliaries are teaching inputs, not plant specifications. Negative net output means the assumed system is not self-powered and must not be silently clipped.'],['電漿增益 Q、熱功率與淨電力有何不同？為何高熱輸出不保證正淨發電？','How do plasma gain Q, thermal power and net electricity differ? Why does large heat output not ensure net generation?']),
 worldWind:lab(['風輪掃掠面積與可用風能','Rotor swept area and available wind energy'],'P = ½ ρ πR² v³ C_p η','MW',[
 p('radius','風輪半徑','Rotor radius',10,150,5,80,'m'),p('speed','均勻來流速度','Uniform wind speed',3,20,.5,10,'m/s'),p('density','空氣密度','Air density',1,1.3,.001,1.225,'kg/m³'),p('cp','假想功率係數','Assumed power coefficient',.15,.59,.01,.45,''),p('eta','傳動與發電效率','Drive/generator efficiency',.8,.99,.01,.95,'')
 ],['均勻、穩態來流的氣動比例模型，C_p 不超過 Betz 上界16/27。不含尾流、湍流、額定功率封頂或切入／切出，不能用平均風速的立方直接預測年發電。','Uniform steady inflow scaling; C_p stays below the Betz bound 16/27. Wakes, turbulence, rated-power capping and cut-in/cut-out are absent. Cubing mean speed does not predict annual energy.'],['風速與半徑各增加10%，理想功率分別變多少？為何真實風場未必有同樣增幅？','What are the ideal effects of 10% more wind speed or radius? Why might a real wind farm differ?'],'https://www.energy.gov/cmei/systems/windexchange/small-wind-guidebook'),
 worldHydro:lab(['淨水頭、流量與電力','Net head, flow and electricity'],'P = ρgQHη','MW',[
 p('head','淨水頭','Net head',5,400,5,50,'m'),p('flow','流量','Flow',1,500,1,100,'m³/s'),p('eta','整體轉換效率','Overall efficiency',.5,.95,.01,.90,'')
 ],['取水密度1000kg/m³、g=9.81m/s²。水頭為扣除損失後的淨水頭；固定效率是假設，不含流量限制、水文變動、空蝕與結構分析。','Water density is 1000 kg/m³ and g=9.81 m/s². Head is net of hydraulic losses. Constant efficiency is assumed; flow restrictions, hydrology, cavitation and structural analysis are omitted.'],['同樣額定功率，高水頭與大流量機組的設計負擔有何不同？','At equal output, how do high-head and high-flow designs differ?'],'https://www.energy.gov/cmei/water/how-hydropower-works'),
 worldGeothermal:lab(['地熱流體可抽取的顯熱','Sensible heat available from geothermal fluid'],'Q = ṁ c_p ΔT','MW',[
 p('flow','假想質量流率','Assumed mass flow',10,200,5,50,'kg/s'),p('drop','假想溫差','Assumed temperature drop',10,150,5,80,'K'),p('cp','假想定壓比熱','Assumed specific heat',3.5,4.5,.1,4.2,'kJ/(kg·K)')
 ],['單相流體定比熱顯熱帳；這是熱功率，不是電功率。未含相變、地層壓力、流體化學、回注與儲層長期衰退。','Single-phase constant-specific-heat sensible balance. This is thermal, not electrical, power. Phase change, reservoir pressure, chemistry, reinjection and long-term depletion are excluded.'],['增加抽取流量為何不等於長期可持續發電必然提高？','Why does higher extraction flow not ensure more sustainable generation?']),
 worldPue:lab(['伺服器與機房總能耗','IT and total facility energy'],'P_total = P_IT × PUE','MW',[
 p('it','IT負載','IT load',1,100,1,20,'MW'),p('pue','假想PUE','Assumed PUE',1,2.5,.05,1.25,'')
 ],['PUE 是相同時間及邊界的設施能源／IT能源比。此式假定穩態功率；不推論碳排、水用量、可靠度或運算產出，實際能源需積分時變負載。','PUE is facility energy divided by IT energy over matching time and boundaries. This assumes steady power. It does not infer emissions, water use, reliability or useful compute; real energy requires time integration.'],['降低PUE但增加IT功率，總能耗可能升高嗎？應如何比較不同機房？','Can lower PUE with higher IT power raise total energy? How should facilities be compared?']),
 worldOre:lab(['礦石品位與金屬回收量','Ore grade and recovered metal'],'m_recovered = m_ore × grade × recovery','kg',[
 p('ore','假想乾礦石質量','Assumed dry ore mass',100,10000,100,1000,'t'),p('grade','假想金品位','Assumed gold grade',.1,10,.1,2,'g/t'),p('recovery','假想回收率','Assumed recovery',.4,.95,.01,.8,'')
 ],['乾礦質量平衡，g/t×t後轉kg。未含取樣誤差、品位空間分布、稀釋、成本、水或尾礦；不是採礦、爆破或化學提煉配方。','Dry-ore mass balance: g/t times tonnes converts to kilograms. Sampling error, spatial grade, dilution, costs, water and tailings are omitted. This is not an extraction, blasting or chemical-processing recipe.'],['品位估計偏差和回收率不確定度，如何共同影響預測？','How do grade bias and recovery uncertainty affect the estimate together?']),
 worldFlow:lab(['流量與累計產量','Flow and cumulative volume'],'V = q × Δt','m³',[
 p('flow','假想穩態流量','Assumed steady flow',10,1000,10,100,'m³/day'),p('days','時間','Duration',1,365,1,30,'day')
 ],['固定流量的體積帳。實際油氣產量需考慮流量衰退、相態、標準溫壓換算與量測不確定度；此模型不提供鑽井或井控操作。','Constant-flow volume accounting. Oil/gas production also requires decline, phases, standard-condition conversion and measurement uncertainty. No drilling or well-control operations are supplied.'],['若每日流量下降，使用初始流量乘以天數會產生何種偏差？','What bias results from multiplying initial flow by duration when flow declines?'])
};
export function worldLabKind(course={}){
 if(course.educationEdition!==11||!course.architectureFamily)return '';
 const family=course.architectureFamily;
 if(family==='wind')return 'worldWind';if(family==='hydro')return 'worldHydro';if(family==='geothermal')return 'worldGeothermal';if(family==='mining')return 'worldOre';if(family==='oil')return 'worldFlow';if(family==='server'||family==='ai')return 'worldPue';if(family==='fusion')return 'worldHeat';if(family==='thermal'||family==='nuclear'||family==='smr')return 'worldCarnot';return '';
}
export function calculateWorldLab(kind,values){
 const spec=WORLD_LABS[kind];if(!spec)return null;
 for(const [id,,min,max] of spec.params){const v=Number(values[id]);if(!Number.isFinite(v)||v<min||v>max)throw new RangeError('Input outside educational model range: '+id);}
 const v=Object.fromEntries(spec.params.map(([id])=>[id,Number(values[id])]));
 if(kind==='worldCarnot')return 100*(1-v.cold/v.hot);
 if(kind==='worldHeat')return v.heat*v.efficiency-v.aux;
 if(kind==='worldWind')return .5*v.density*Math.PI*v.radius**2*v.speed**3*v.cp*v.eta/1e6;
 if(kind==='worldHydro')return 1000*9.81*v.flow*v.head*v.eta/1e6;
 if(kind==='worldGeothermal')return v.flow*v.cp*v.drop/1000;
 if(kind==='worldPue')return v.it*v.pue;
 if(kind==='worldOre')return v.ore*v.grade*v.recovery/1000;
 if(kind==='worldFlow')return v.flow*v.days;
 return null;
}
export function worldLabDetail(kind,v,zh=true){return kind==='worldPue'?(zh?'非IT功率':'Non-IT power')+' = '+(v.it*(v.pue-1)).toFixed(2)+' MW':kind==='worldGeothermal'?(zh?'這是熱輸出；淨電力需另扣循環與輔助耗能。':'Thermal output; net electricity requires cycle and auxiliary accounting.'):'';}
