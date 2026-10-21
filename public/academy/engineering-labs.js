import {WATER_LABS,waterLabKind,calculateWaterLab,waterLabDetail} from './water-calculators.js';
import {UNDERGROUND_LABS,undergroundLabKind,calculateUndergroundLab,undergroundLabDetail} from './underground-calculators.js';
import { COMPUTING_LABS, COMPUTING_COURSE_LABS, computingLabKind, calculateComputingLab, computingLabDetail } from './computing-visuals.js';
import { WORLD_LABS, worldLabKind, calculateWorldLab, worldLabDetail } from './world-project-labs.js';
import {PACKAGING_LABS,packagingLabKind,calculatePackagingLab,packagingLabDetail} from './packaging-calculators.js';
/** Transparent teaching calculations. No foundry recipes or device-physics solver. */
import {SEMICONDUCTOR_LABS,semiconductorLabKind,calculateSemiconductorLab} from './semiconductor-calculators.js';
import {ELECTRONICS_LABS,ELECTRONICS_COURSE_LABS,electronicsLabKind,calculateElectronicsLab,electronicsLabDetail} from './electronics-calculators.js';
const e = value => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const choose = (pair, zh) => pair[zh ? 0 : 1];
export function labKind(course, step) {
  const water=waterLabKind(course,step);if(water)return water;
  const underground=undergroundLabKind(course,step);if(underground)return underground;
  if(COMPUTING_COURSE_LABS[course.id])return computingLabKind(course,step);
  const world=worldLabKind(course);if(world)return world;
  if(ELECTRONICS_COURSE_LABS[course.id])return electronicsLabKind(course,step);
  if(course.category==='packaging')return packagingLabKind(course,step);
  const semiconductorKind=semiconductorLabKind(course,step);if(semiconductorKind)return semiconductorKind;
  if (course.category!=='semiconductor' && !['semiconductor','packaging','sub2nm','asml','silicon-photonics','a025','a042'].includes(course.id)) return '';
  const text = `${step.titleEn || ''} ${step.stage?.titleEn || ''}`.toLowerCase();
  if (course.id === 'a042') return /overlay|align|register/.test(text) ? 'overlay' : 'lithography';
  if (course.id === 'a025') return /thermal|heat/.test(text) ? 'thermal' : /bond|align|overlay/.test(text) ? 'overlay' : 'resistance';
  if (/overlay|align|registration|hybrid/.test(text)) return 'overlay';
  if (/litho|exposure|photoresist|optical|pattern/.test(text) || course.id === 'asml') return 'lithography';
  if (/yield|defect|reliab|incoming|inspection|test|spc|wafer map/.test(text)) return 'yield';
  if (/thermal|underfill|attach|lid|heat|mold|stack/.test(text)) return 'thermal';
  if (/interconnect|metal|via|contact|rdl|tsv|silicide|substrate|bump|wire/.test(text)) return 'resistance';
  if (/deposit|film|dielectric|oxid|ald|cvd|barrier|gate/.test(text)) return 'coverage';
  return course.id === 'packaging' ? 'thermal' : 'yield';
}
export const LABS = {
  lithography: {
    title: ['微影解析度探索','Explore lithography resolution'], formula:'CD = k₁ × λ / NA', unit:'nm',
    note:['Rayleigh 尺寸趨勢模型。k₁ 是整體製程因子，不是設備旋鈕；不含光阻隨機性、圖形偏差、焦深或多重圖形化。計算 CD 不等於商品節點名稱。','Rayleigh scaling model. k₁ is a process factor, not a machine knob. Resist stochasticity, pattern bias, depth of focus and multipatterning are excluded. CD is not a marketed node name.'],
    question:['固定波長與 k₁，把 NA 增加一倍，CD 如何改變？為何不能把 EUV 波長直接當作最小線寬？','Hold wavelength and k₁ fixed. What happens to CD when NA doubles? Why is EUV wavelength not the minimum linewidth?'],
    params:[['wavelength',['波長 λ','Wavelength λ'],13.5,365,.5,193,'nm'],['na',['數值孔徑 NA','Numerical aperture NA'],.1,1.35,.01,1.35,''],['k',['製程因子 k₁','Process factor k₁'],.25,.8,.01,.35,'']],
    source:'https://www.asml.com/en/technology/lithography-principles/rayleigh-criterion',
  },
  coverage: {
    title:['薄膜階梯覆蓋率','Thin-film step coverage'],formula:'S = t_side / t_top × 100%',unit:'%',
    note:['這是量測幾何比值，不預測沉積速率；側壁與頂面厚度必須使用同一量測定義。ALD、CVD、PVD 在真實結構中的覆蓋率需實測，不由名稱決定。','This is a measured geometric ratio, not a deposition-rate model. Sidewall and top thickness must use consistent definitions. Real ALD/CVD/PVD coverage requires measurement.'],
    question:['頂面厚度相同但側壁只有一半厚，哪裡先可能形成不連續？覆蓋率是否能單獨證明薄膜電性合格？','With identical top thickness but half the sidewall thickness, where might continuity fail first? Can coverage alone establish electrical quality?'],
    params:[['top',['頂面厚度','Top thickness'],1,100,1,20,'nm'],['side',['側壁厚度','Sidewall thickness'],0,100,1,12,'nm']],
    source:'https://www.lamresearch.com/products/our-processes/deposition/',
  },
  resistance: {
    title:['互連電阻與幾何','Interconnect resistance and geometry'],formula:'R = ρL / (wt)',unit:'Ω',
    note:['均勻矩形導線的直流模型；電阻率由你輸入，預設僅為體材料量級示例。忽略奈米尺度散射、接觸電阻、溫升與高頻效應，不代表製程實際阻值。','Uniform rectangular conductor at DC. Resistivity is an input; its default is only a bulk-scale example. Nanoscale scattering, contacts, self-heating and high-frequency effects are excluded.'],
    question:['將線寬減半而其他條件不變，電阻如何改變？若量測阻值比模型大，還有哪些機制未包含？','Halve width while holding other inputs fixed. How does resistance change? Which omitted mechanisms could explain a larger measured value?'],
    params:[['rho',['電阻率 ρ','Resistivity ρ'],1,20,.1,1.7,'µΩ·cm'],['length',['長度 L','Length L'],1,1000,1,100,'µm'],['width',['線寬 w','Width w'],20,2000,10,200,'nm'],['thickness',['厚度 t','Thickness t'],20,2000,10,200,'nm']],
    source:'https://www.nist.gov/publications/improved-estimation-resistivity-pure-copper-electrical-determination-thin-copper-film',
  },
  thermal: {
    title:['封裝材料層的導熱','Conduction through a package layer'],formula:'R_th = t / (kA)   ·   ΔT = P R_th',unit:'K',
    note:['一維、穩態、均勻材料層，假設全部功率通過同一面積；忽略接觸熱阻、熱擴散、對流、輻射與暫態。只算此層溫差，不是晶片總接面溫度。','One-dimensional steady conduction through a homogeneous layer with all power crossing the same area. Contact resistance, spreading, convection, radiation and transients are excluded. This is the layer drop, not total junction temperature.'],
    question:['保持功率不變，將接合層厚度加倍，溫差如何變化？實際封裝有哪些並聯散熱路徑？','At fixed power, how does doubling bond-line thickness affect temperature drop? What parallel heat paths exist in a real package?'],
    params:[['power',['通過此層的功率 P','Power through layer P'],1,100,1,20,'W'],['thickness',['材料層厚度 t','Layer thickness t'],10,500,10,100,'µm'],['k',['熱傳導係數 k','Thermal conductivity k'],.2,20,.2,2,'W/(m·K)'],['area',['傳熱面積 A','Heat-flow area A'],1,400,1,100,'mm²']],
    source:'https://www.ti.com/design-development/design-simulation-tools/pcb-thermal-calculator.html',
  },
  yield: {
    title:['隨機缺陷與面積','Random defects and die area'],formula:'Y = exp(−D₀ A)',unit:'%',
    note:['自行定義的 Poisson 理想假設：致命缺陷獨立、均勻分布，每個缺陷必定致命。不含群聚、冗餘、參數性失效或實際關鍵面積，不可用作晶圓廠良率預測。','Ideal Poisson assumptions: independent uniformly distributed fatal defects, each causing failure. Clustering, redundancy, parametric failure and actual critical area are excluded; this is not a foundry yield prediction.'],
    question:['相同缺陷密度下，面積變大為何降低理想良率？若缺陷集中於局部，獨立均勻假設還成立嗎？','Why does larger area reduce ideal yield at fixed defect density? Does the independent-uniform assumption hold when defects cluster?'],
    params:[['density',['假設致命缺陷密度 D₀','Assumed fatal defect density D₀'],0,2,.01,.2,'cm⁻²'],['area',['晶粒面積 A','Die area A'],1,800,1,100,'mm²']],
    source:'',
  },
  overlay: {
    title:['對準誤差預算','Alignment error budget'],formula:'σ_total = √(σ₁² + σ₂² + σ₃²)',unit:'nm',
    note:['只計算三個獨立、零均值誤差的一維標準差；偏置不能靠平方和消除，相关誤差需加入共變異數。不是設備規格或合格公差。','One-dimensional standard deviation for three independent zero-mean errors. Bias is not removed by root-sum-square; correlated terms require covariance. These are not tool specifications or acceptance tolerances.'],
    question:['若兩個誤差源相關，直接取平方和為何失準？若其中一項已主導總誤差，改善其他項的效益如何？','Why does root-sum-square fail for correlated errors? What is the benefit of improving small terms when one source dominates?'],
    params:[['stage',['平台誤差 σ₁','Stage error σ₁'],0,20,.1,2,'nm'],['mark',['標記量測 σ₂','Mark measurement σ₂'],0,20,.1,3,'nm'],['distortion',['殘餘畸變 σ₃','Residual distortion σ₃'],0,20,.1,4,'nm']],
    source:'',
  },
};
export function calculateLab(kind, v) {
  if(WATER_LABS[kind])return calculateWaterLab(kind,v);
  const underground=calculateUndergroundLab(kind,v);if(underground!==null)return underground;
  const computing=calculateComputingLab(kind,v);if(computing!==null)return computing;
  const world=calculateWorldLab(kind,v);if(world!==null)return world;
  const electronicsValue=calculateElectronicsLab(kind,v);if(electronicsValue!==null)return electronicsValue;
  const packagingValue=calculatePackagingLab(kind,v);if(packagingValue!==null)return packagingValue;
  const semiconductorValue=calculateSemiconductorLab(kind,v);if(semiconductorValue!==null)return semiconductorValue;
  if (kind === 'lithography') return v.k * v.wavelength / v.na;
  if (kind === 'coverage') return 100 * v.side / v.top;
  if (kind === 'resistance') return v.rho * 1e-8 * v.length * 1e-6 / (v.width * 1e-9 * v.thickness * 1e-9);
  if (kind === 'thermal') return v.power * v.thickness * 1e-6 / (v.k * v.area * 1e-6);
  if (kind === 'yield') return 100 * Math.exp(-v.density * v.area / 100);
  if (kind === 'overlay') return Math.hypot(v.stage, v.mark, v.distortion);
  return 0;
}
Object.assign(LABS,SEMICONDUCTOR_LABS,PACKAGING_LABS,ELECTRONICS_LABS,COMPUTING_LABS,WORLD_LABS,UNDERGROUND_LABS,WATER_LABS);
export function labMarkup(course, step, zh) {
  const kind=labKind(course,step),lab=LABS[kind];if(!lab)return '';
  return `<section class="lesson-card engineering-lab" id="engineeringLab" data-kind="${kind}"><div class="eyebrow">EXPLORE / ${zh?'互動工程算例':'INTERACTIVE ENGINEERING'}</div><h3>${choose(lab.title,zh)}</h3><p><code>${e(lab.formula)}</code></p>${kind==='lithography'?`<label class="field">${zh?'光學情境預設':'Optical scenario'}<select id="labPreset"><option value="duv">ArF immersion · 193 nm · NA 1.35</option><option value="euv">EUV · 13.5 nm · NA 0.33</option><option value="highna">High-NA EUV · 13.5 nm · NA 0.55</option></select></label>`:''}<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,230px),1fr));gap:16px">${lab.params.map(([id,label,min,max,delta,value,unit])=>`<label class="field" for="lab-${id}">${e(choose(label,zh))} <output id="lab-value-${id}">${value}</output> ${e(unit)}<input id="lab-${id}" data-lab-input="${id}" type="range" min="${min}" max="${max}" step="${delta}" value="${value}" style="width:100%;min-height:42px;accent-color:#245443"></label>`).join('')}</div><div style="display:flex;align-items:center;gap:18px;flex-wrap:wrap;margin:20px 0"><output id="labResult" aria-live="polite" style="font-size:32px;font-weight:700;color:#245443"></output><span id="labDetail"></span></div><div id="labChart" aria-hidden="true"></div><p id="labScenarioNote" class="muted"></p><p class="notice">${e(choose(lab.note,zh))}</p><p><strong>${zh?'試著推理：':'Reason it through: '}</strong>${e(choose(lab.question,zh))}</p>${lab.source?`<a href="${e(lab.source)}" target="_blank" rel="noopener noreferrer">${zh?'公式／假設延伸閱讀':'Formula / assumptions reference'} ↗</a>`:''}</section>`;
}
export function bindLab(course, step, zh) {
  if(typeof document==='undefined')return;
  const root=document.querySelector('#engineeringLab');if(!root || !root.querySelectorAll)return;
  const kind=labKind(course,step),lab=LABS[kind];if(!lab)return;
  const inputs=[...root.querySelectorAll('[data-lab-input]')];if(!inputs.length)return;
  const update=()=>{
    const values=Object.fromEntries(inputs.map(input=>[input.dataset.labInput,Number(input.value)]));
    inputs.forEach(input=>{const output=root.querySelector('#lab-value-'+input.dataset.labInput);if(output)output.textContent=input.value;});
    const resultNode=root.querySelector('#labResult');let result;
    try {result=calculateLab(kind,values);if(!Number.isFinite(result))throw new RangeError('Non-finite result');}
    catch(error){
      if(resultNode)resultNode.textContent=zh?'輸入超出模型範圍':'Inputs outside model domain';
      const detail=root.querySelector('#labDetail');if(detail)detail.textContent=error.message;
      const chart=root.querySelector('#labChart');if(chart)chart.innerHTML='';
      const note=root.querySelector('#labScenarioNote');if(note)note.textContent='';
      return;
    }
    if(resultNode)resultNode.textContent=`${result.toFixed(result<1?3:2)} ${lab.unit}`;
    const detail=root.querySelector('#labDetail');if(detail)detail.textContent=waterLabDetail(kind,values,zh)||undergroundLabDetail(kind,values,zh)||computingLabDetail(kind,values,zh)||worldLabDetail(kind,values,zh)||electronicsLabDetail(kind,values,zh)||packagingLabDetail(kind,values,zh)||(kind==='thermal'?`R_th = ${(result/values.power).toFixed(3)} K/W`:kind==='yield'?`D₀ A = ${(values.density*values.area/100).toFixed(3)}`:'');
    const note=root.querySelector('#labScenarioNote');if(note)note.textContent=kind==='lithography'&&(values.wavelength<20&&values.na>.55)?(zh?'此組合超出本教學列出的 EUV 情境；數學結果不代表已有此設備。':'This combination exceeds the EUV scenarios supplied here; the mathematical result does not imply such a tool exists.') : kind==='lithography'&&(values.wavelength<20)?(zh?'EUV 情境使用反射光學；NA 不是可任意改動的機台設定。':'EUV scenarios use reflective optics; NA is not an arbitrary machine setting.') : '';
    const varying=lab.params[0],pts=[];for(let i=0;i<=40;i++){const sample=varying[2]+(varying[3]-varying[2])*i/40,x=(kind==='pkgN1'||kind==='elAdc'||kind==='elQuant'||kind==='elSettle'||kind==='elPll')||varying[4]>=1?Math.round(sample):sample;try{const y=calculateLab(kind,{...values,[varying[0]]:x});pts.push(Number.isFinite(y)?[x,y]:null);}catch{pts.push(null);}}
    const valid=pts.filter(Boolean),low=Math.min(0,...valid.map(p=>p[1])),high=Math.max(0,...valid.map(p=>p[1]),low+.001),span=high-low;let connected=false;const path=pts.map((p,i)=>{if(!p){connected=false;return '';}const command=connected?'L':'M';connected=true;return `${command}${30+i*9} ${(115-95*(p[1]-low)/span).toFixed(2)}`;}).join(' '),chart=root.querySelector('#labChart');
    if(chart)chart.innerHTML=`<svg viewBox="0 0 420 150" style="width:100%;max-width:580px"><path d="M30 10V115H390M30 ${115-95*(0-low)/span}H390" stroke="#8da18b" fill="none"/><path d="${path}" stroke="#dd8a44" stroke-width="3" fill="none"/><text x="30" y="141" font-size="11" fill="#52694e">${e(choose(varying[1],zh))} → (${e(varying[6])})</text><text x="330" y="18" font-size="11" fill="#52694e">${high.toFixed(1)} ${e(lab.unit)}</text><text x="330" y="127" font-size="11" fill="#52694e">${low.toFixed(1)} ${e(lab.unit)}</text></svg>`;
  };
  inputs.forEach(input=>input.oninput=update);
  const preset=root.querySelector('#labPreset');if(preset)preset.onchange=()=>{const p={duv:[193,1.35],euv:[13.5,.33],highna:[13.5,.55]}[preset.value];root.querySelector('#lab-wavelength').value=p[0];root.querySelector('#lab-na').value=p[1];update();};
  update();
}
