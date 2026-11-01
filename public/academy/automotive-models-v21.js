/* Original bounded teaching calculators. Synthetic inputs, not vehicle ratings. */
(function(root){
'use strict';
const input=(key,label,labelEn,unit,value,min,max,step)=>({key,label,labelEn,unit,value,min,max,step});
const models=[
 {id:'stopping',title:'反應與理想制動距離',titleEn:'Reaction and ideal braking distance',unit:'m',formula:'s = v·t + v²/(2a)',inputs:[input('speed','初速','Initial speed','m/s',20,0,100,.5),input('reaction','反應延遲','Reaction delay','s',1,0,10,.1),input('deceleration','恆定減速度','Constant deceleration','m/s²',6,.1,20,.1)]},
 {id:'dragPower',title:'氣動阻力功率',titleEn:'Aerodynamic drag power',unit:'kW',formula:'P = ρ·Cd·A·v³/2000',inputs:[input('density','空氣密度','Air density','kg/m³',1.2,.1,2,.01),input('cd','阻力係數','Drag coefficient','1',.28,.05,2,.01),input('area','參考面積','Reference area','m²',2.2,.1,30,.1),input('speed','車速','Speed','m/s',30,0,150,.5)]},
 {id:'range',title:'可用能量與續航',titleEn:'Usable energy and range',unit:'km',formula:'range = 100·E·(1−reserve)/consumption',inputs:[input('energy','名義能量','Nominal energy','kWh',60,.1,2000,.5),input('reserve','保留能量比例','Reserved energy fraction','1',.1,0,1,.01),input('consumption','平均能耗','Average consumption','kWh/100 km',18,.1,1000,.1)]},
 {id:'driveTorque',title:'減速後軸端轉矩',titleEn:'Output torque after reduction',unit:'N m',formula:'Tout = Tin·ratio·η',inputs:[input('torque','輸入轉矩','Input torque','N m',200,0,100000,1),input('ratio','減速比','Reduction ratio','1',9,.1,100,.1),input('efficiency','機械效率','Mechanical efficiency','1',.96,0,1,.01)]},
 {id:'batteryHeat',title:'電阻熱功率',titleEn:'Resistive heating power',unit:'W',formula:'P = I²·R',inputs:[input('current','電流','Current','A',100,-3000,3000,1),input('resistance','等效電阻','Equivalent resistance','Ω',.005,0,10,.001)]},
 {id:'coolantHeat',title:'冷卻液顯熱流',titleEn:'Coolant sensible heat flow',unit:'W',formula:'Q̇ = ṁ·cp·ΔT',inputs:[input('flow','質量流率','Mass flow','kg/s',.2,0,20,.01),input('heatCapacity','比熱','Specific heat','J/(kg K)',3800,100,5000,10),input('deltaT','出口減入口溫差','Outlet minus inlet temperature','K',5,-100,100,.5)]},
 {id:'takt',title:'需求節拍',titleEn:'Demand takt time',unit:'s/unit',formula:'takt = available_seconds/demand',inputs:[input('available','可用生產時間','Available production time','s',25200,0,604800,60),input('demand','需求件數','Demanded units','unit',420,1,1000000,1)]},
 {id:'brakingEnergy',title:'假想回生能量',titleEn:'Hypothetical recovered braking energy',unit:'kWh',formula:'Erec = η·m·v²/(2·3600000)',inputs:[input('mass','車輛質量','Vehicle mass','kg',1600,1,1000000,10),input('speed','初速','Initial speed','m/s',20,0,150,.5),input('efficiency','回收效率','Recovery efficiency','1',.65,0,1,.01)]}
];
const equations={stopping:p=>p.speed*p.reaction+p.speed*p.speed/(2*p.deceleration),dragPower:p=>p.density*p.cd*p.area*p.speed**3/2000,range:p=>100*p.energy*(1-p.reserve)/p.consumption,driveTorque:p=>p.torque*p.ratio*p.efficiency,batteryHeat:p=>p.current*p.current*p.resistance,coolantHeat:p=>p.flow*p.heatCapacity*p.deltaT,takt:p=>p.available/p.demand,brakingEnergy:p=>p.efficiency*p.mass*p.speed*p.speed/(2*3600000)};
function calculate(id,params){
 const model=models.find(m=>m.id===id);if(!model)throw new RangeError('Unknown automotive model');
 if(!params||typeof params!=='object')throw new RangeError('Inputs are required');
 const checked={};for(const field of model.inputs){const v=params[field.key];if(typeof v!=='number'||!Number.isFinite(v)||v<field.min||v>field.max)throw new RangeError('Invalid '+field.key+': expected '+field.min+' … '+field.max);if(field.key==='demand'&&!Number.isInteger(v))throw new RangeError('Demand must be an integer');checked[field.key]=v;}
 const value=equations[id](checked);if(!Number.isFinite(value))throw new RangeError('Non-finite model output');return {value,unit:model.unit,formula:model.formula};
}
root.MG_AUTOMOTIVE_MODELS_V21=Object.freeze({version:21,models,calculate,scope:'Hypothetical educational models; no road, manufacturing or maintenance authorization.'});
})(typeof window!=='undefined'?window:globalThis);
