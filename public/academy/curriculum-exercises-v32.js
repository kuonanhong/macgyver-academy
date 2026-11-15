/** V32 lesson-linked evidence and arithmetic workbenches. No lesson payload is bundled. */
import {calculateCurriculumModelV31} from './curriculum-exercises-v31.js';
const bi=(zh,en)=>({zh,en});
const esc=value=>String(value??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const short=(s,n)=>{const a=Array.from(String(s??'').replace(/\s+/g,' '));return a.length>n?a.slice(0,n-1).join('')+'…':a.join('')};
const number=value=>Math.abs(value)>=1e8||(value!==0&&Math.abs(value)<1e-4)?value.toExponential(6):value.toLocaleString('en-US',{maximumSignificantDigits:9});

function sequenceFor(course,step){
 if(!/^d\d{3}$/.test(String(course?.id||''))||step?.locked||course?.locked||course?.access==='locked'||step?.access==='locked')return 0;
 const match=String(step?.id||'').match(/^(d\d{3})-v32-(\d{2})$/);
 if(!match||match[1]!==course.id)return 0;
 const sequence=Number(match[2]);return sequence>=1&&sequence<=40?sequence:0;
}

export function calculateCurriculumModelV32(model,values){
 const result=calculateCurriculumModelV31(model,values);
 const pairs={yield:['good','feed'],porosity:['bulk','solid'],reduction:['final','initial'],shrink:['fired','green'],
  recovery:['product','feed'],rejection:['permeate','feed'],moisture:['final','wet'],coverage:['verified','required']};
 const pair=pairs[model.key];if(pair&&values[pair[0]]>values[pair[1]])throw new RangeError('Inputs violate the stated material/count boundary');
 if(model.key==='dilution'&&values.amount>values.total)throw new RangeError('Stock volume exceeds total volume');
 return result;
}

export function modelForCurriculumV32(course,step){
 const sequence=sequenceFor(course,step);if(!sequence||sequence%4!==2)return null;
 const unit=Math.floor((sequence-1)/4)+1;
 const model=step.v32Model||(Array.isArray(course.v32Models)?course.v32Models.find(m=>m.unit===unit):null);
 if(!model||model.unit!==unit||model.provenance!=='original-v32-synthetic-teaching-model')return null;
 try{calculateCurriculumModelV32(model,model.variables);return model;}catch{return null;}
}

export function curriculumLabMarkupV32(course,step,zh=true){
 const m=modelForCurriculumV32(course,step);if(!m)return '';
 const fields=Object.entries(m.variables).map(([name,value])=>{
  const b=m.bounds?.[name]||{};
  const range=[b.min!==undefined?`${b.exclusiveMin?'>':'≥'} ${b.min}`:'',b.max!==undefined?`${b.exclusiveMax?'<':'≤'} ${b.max}`:''].filter(Boolean).join(' · ');
  return `<label class="field">${esc(name)} <small>${esc(m.variableUnits?.[name]||'')}</small><input data-v32-number="${esc(name)}" type="number" inputmode="decimal" step="any" value="${value}" style="min-height:44px;width:100%"><small>${esc(range)}</small></label>`;
 }).join('');
 return `<section class="lesson-card engineering-lab" id="engineeringLabV32" data-v32-model="${esc(step.id)}"><div class="eyebrow">${zh?'工程算例｜合成教學資料':'ENGINEERING MODEL · SYNTHETIC DATA'}</div><h3>${esc(zh?m.title:m.titleEn)}</h3><p><code>${esc(m.formula)}</code></p><p>${esc(zh?m.meaning:m.meaningEn)}</p><div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,180px),1fr));gap:12px">${fields}</div><div style="display:flex;gap:10px;flex-wrap:wrap;margin:14px 0"><button type="button" data-v32-compute>${zh?'計算與比較':'Compute and compare'}</button><button type="button" data-v32-reset>${zh?'還原教學值':'Restore teaching inputs'}</button></div><output data-v32-result aria-live="polite" style="display:block;font-size:22px;font-weight:700">${zh?'按計算取得結果。':'Press Compute for a result.'}</output><p data-v32-sensitivity></p><p class="notice">${esc(zh?m.limit:m.limitEn)}</p><small>${zh?'預設值全部為合成教學假設。修改後需重算；算例不會自動完成步驟，也不是實機設定。':'All defaults are synthetic teaching assumptions. Recompute after edits; calculations do not complete the step and are not equipment settings.'}</small></section>`;
}

export function bindCurriculumLabV32(course,step,zh=true,doc=globalThis.document,storage){
 if(storage===undefined)try{storage=globalThis.localStorage;}catch{storage=null;}
 const m=modelForCurriculumV32(course,step),root=doc?.querySelector?.('#engineeringLabV32');if(!m||!root)return false;
 const inputs=Array.from(root.querySelectorAll('[data-v32-number]')),result=root.querySelector('[data-v32-result]'),sensitivity=root.querySelector('[data-v32-sensitivity]');
 const key='mg-v32-model:'+course.id+':'+step.id;
 const clear=()=>{root.dataset.computed='false';result.textContent=zh?'輸入已變更，請重新計算。':'Inputs changed; compute again.';sensitivity.textContent='';};
 try{const saved=JSON.parse(storage?.getItem?.(key)||'null');if(saved?.inputs){calculateCurriculumModelV32(m,saved.inputs);for(const input of inputs)input.value=String(saved.inputs[input.dataset.v32Number]);clear();}}catch{}
 for(const input of inputs)input.oninput=clear;
 root.querySelector('[data-v32-compute]').onclick=()=>{
  try{
   const values=Object.fromEntries(inputs.map(input=>{if(!String(input.value).trim())throw new RangeError('Empty input');return [input.dataset.v32Number,Number(input.value)];}));
   const value=calculateCurriculumModelV32(m,values);result.textContent=`${zh?'結果':'Result'}: ${number(value)} ${m.unitLabel}`;root.dataset.computed='true';
   try{const changed=calculateCurriculumModelV32(m,{...values,[m.vary]:values[m.vary]*1.1});sensitivity.textContent=`${m.vary} +10% → ${number(changed)} ${m.unitLabel}`;}catch{sensitivity.textContent=zh?'增加10%後超出模型邊界。':'The +10% scenario exceeds model boundaries.';}
   try{storage?.setItem?.(key,JSON.stringify({inputs:values,result:value,savedAt:Date.now()}));}catch{}
  }catch(error){result.textContent=zh?'輸入無效或超出模型邊界。':'Invalid inputs or model boundary exceeded.';sensitivity.textContent=error.message;root.dataset.computed='false';}
 };
 root.querySelector('[data-v32-reset]').onclick=()=>{for(const input of inputs)input.value=String(m.variables[input.dataset.v32Number]);try{storage?.removeItem?.(key);}catch{}clear();};
 return true;
}

export function resolveCurriculumExerciseV32(course,step,make){
 const sequence=sequenceFor(course,step);if(!sequence)return null;
 const q=step.quiz;
 const complete=q&&Array.isArray(q.options)&&Array.isArray(q.optionsEn)&&q.options.length===3&&q.optionsEn.length===3
  &&Number.isInteger(q.answer)&&q.answer>=0&&q.answer<3&&['instruction','instructionEn','observation','observationEn','check','checkEn'].every(k=>typeof step[k]==='string'&&step[k].trim());
 if(!complete)return null;
 const choices=q.options.map((s,i)=>({id:'answer-'+i,label:bi(s,q.optionsEn[i])}));
 const unit=Math.floor((sequence-1)/4)+1;
 const nodes=Array.isArray(course.v32Architecture?.nodes)?course.v32Architecture.nodes.map(n=>bi(n[0],n[1])):[];
 return make(step.id+'-evidence-v32','inspect','curriculum-v32:'+course.category,bi(step.title,step.titleEn),
  bi(`${step.instruction}\n觀察紀錄：${step.observation}\n工程判讀：${q.question}`,`${step.instructionEn}\nObservation: ${step.observationEn}\nDecision: ${q.questionEn}`),
  bi('工程證據工作台','Engineering evidence workbench'),bi(step.check+'\n'+q.explanation,step.checkEn+'\n'+q.explanationEn),{
   choices,expectedChoice:'answer-'+q.answer,provenance:'step-authored-evidence',family:'v32-evidence',
   decisionFeedback:bi('請重核本課的介面、單位、合成算例及適用邊界。','Recheck the case interfaces, units, synthetic calculation and applicability boundary.'),
   curriculumEvidenceV32:{available:true,sequence,unit,courseTitle:bi(course.title,course.titleEn),focus:bi(course.v32Focus||course.title,course.v32FocusEn||course.titleEn),
    nodes,artifacts:(step.knowledge||[]).slice(0,2).map(k=>({label:bi(k.title,k.titleEn),text:bi(k.text,k.textEn)})),check:bi(step.check,step.checkEn)},
   coverage:bi('本課的具體焦點與失效情境，搭配明示共通方法；數值是教學假設，畫面是原創架構示意。','The case focus and failure scenario use explicitly shared methods. Numbers are teaching assumptions and the architecture is an original schematic.')
  });
}

export function renderCurriculumEvidenceV32(spec,choice,lang='zh'){
 const c=spec.curriculumEvidenceV32;if(!c)return '';
 if(c.available===false)return `<g data-v32-evidence="unavailable"><text x="18" y="112" font-size="12" font-family="system-ui,sans-serif">${esc(lang==='zh'?'請先載入已授權的完整步驟。':'Load the authorized complete step first.')}</text></g>`;
 const zh=lang==='zh',selected=spec.choices.find(x=>x.id===choice);
 const text=(x,y,value,size=8)=>`<text x="${x}" y="${y}" font-size="${size}" fill="#173e45" font-family="system-ui,sans-serif">${esc(value)}</text>`;
 let out=`<g data-v32-evidence="${c.unit}"><title>${esc(c.courseTitle[lang])}</title>`;
 out+=text(18,56,short(c.courseTitle[lang],zh?28:56),10)+text(18,73,zh?`單元 ${c.unit}/10 · 第 ${c.sequence}/40 步`:`UNIT ${c.unit}/10 · STEP ${c.sequence}/40`,8);
 const nodes=c.nodes.slice(0,5),width=nodes.length?350/nodes.length:0;
 nodes.forEach((n,i)=>{const x=18+i*width;out+=`<rect x="${x}" y="84" width="${width-5}" height="29" rx="5" fill="#e2efeb" stroke="#6a9b8d"/><title>${esc(n[lang])}</title>`+text(x+5,102,short(n[lang],zh?7:12),7);});
 const fields=[{label:bi('本課焦點','Case focus'),text:c.focus},...c.artifacts];
 fields.forEach((a,i)=>{const y=122+i*31;out+=`<rect x="18" y="${y}" width="355" height="28" rx="5" fill="#f2f6f4" stroke="#becfc7"/><title>${esc(a.label[lang]+': '+a.text[lang])}</title>`+text(25,y+10,short(a.label[lang],32),6.8)+text(25,y+22,short(a.text[lang],zh?37:73),7.6);});
 out+=text(18,226,zh?'完整算式、證據與判讀請見下方任務欄。':'Full formulas, evidence and decisions appear below.',8);
 out+=text(18,240,selected?(zh?'已選判讀；記錄觀察後提交檢查。':'Decision selected; record evidence and submit.'):(zh?'核對本課證據後選擇判讀。':'Inspect the case evidence, then choose a decision.'),8);
 return out+'</g>';
}
