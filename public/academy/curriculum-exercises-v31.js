/** V31 oil, gas and mining lesson evidence workbench. No lesson or answer payload is bundled here. */
const bi=(zh,en)=>({zh,en});
const esc=value=>String(value??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const short=(value,n)=>{const chars=Array.from(String(value??'').replace(/\s+/g,' '));return chars.length>n?chars.slice(0,n-1).join('')+'…':chars.join('')};
const FACETS={mechanism:bi('機制與能量路徑','Mechanism and energy path'),model:bi('定量估算與敏感度','Quantitative estimate and sensitivity'),verification:bi('試驗與驗證','Testing and verification'),failure:bi('失效診斷','Failure diagnosis')};
const FACET_ORDER=['mechanism','model','verification','failure'];

/** Resolve only genuine V31 energy steps: <courseId>-v31-01 … -40 in a resources course. */
export function resolveCurriculumExerciseV31(course,step,make){
  const courseId=String(course?.id||''),stepId=String(step?.id||'');
  if(course?.category!=='materials'||!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(courseId))return null;
  const stepMatch=stepId.match(/-v31-(\d{2})$/);
  const sequence=Number(stepMatch?.[1]);
  if(!stepMatch||stepId!==`${courseId}-v31-${stepMatch[1]}`||sequence<1||sequence>40)return null;
  const facet=FACET_ORDER.includes(step.unitFacet)?step.unitFacet:FACET_ORDER[(sequence-1)%4];
  const unit=Math.floor((sequence-1)/4)+1;
  const quiz=step.quiz;
  const complete=!step.locked&&quiz&&Array.isArray(quiz.options)&&Array.isArray(quiz.optionsEn)
    &&quiz.options.length>=2&&quiz.options.length===quiz.optionsEn.length
    &&quiz.options.every(s=>typeof s==='string'&&s.trim())&&quiz.optionsEn.every(s=>typeof s==='string'&&s.trim())
    &&Number.isInteger(quiz.answer)&&quiz.answer>=0&&quiz.answer<quiz.options.length
    &&['instruction','instructionEn','observation','observationEn','check','checkEn'].every(k=>typeof step[k]==='string'&&step[k].trim())
    &&['question','questionEn','explanation','explanationEn'].every(k=>typeof quiz[k]==='string'&&quiz[k].trim());
  const choices=complete?quiz.options.map((value,i)=>({id:'answer-'+i,label:bi(value,quiz.optionsEn[i])})):[];
  const offset=choices.length?sequence%choices.length:0;
  const object=bi(short(step.title||course.title,27),short(step.titleEn||course.titleEn,51));
  const instruction=complete?bi(
    `${step.instruction}\n觀察與紀錄：${step.observation}\n工程判讀：${quiz.question}\n選擇與本步資料相符的判讀，再記錄你的觀察。`,
    `${step.instructionEn}\nObserve and document: ${step.observationEn}\nEngineering decision: ${quiz.questionEn}\nChoose the interpretation supported by this step, then record your observation.`
  ):bi('請載入已授權的完整步驟，才能開始此工程任務。','Load the authorized complete step before starting this engineering task.');
  const evidence=complete?bi(`${step.check}\n${quiz.explanation}`,`${step.checkEn}\n${quiz.explanationEn}`):bi('尚未載入本步證據。','Step evidence has not been loaded.');
  const architecture=course.v31Architecture;
  const nodes=Array.isArray(architecture?.nodes)?architecture.nodes.filter(n=>Array.isArray(n)&&n.length===2).slice(0,6).map(n=>bi(String(n[0]),String(n[1]))):[];
  const knowledge=Array.isArray(step.knowledge)?step.knowledge.filter(item=>item&&['title','titleEn','text','textEn'].every(k=>typeof item[k]==='string'&&item[k].trim())).slice(0,2):[];
  return make(`${step.id}-authored-evidence-v31`,'inspect','curriculum-v31:resources',object,instruction,
    bi('資源工程證據台','Resource engineering evidence bench'),evidence,{
      choices:[...choices.slice(offset),...choices.slice(0,offset)],expectedChoice:complete?'answer-'+quiz.answer:'unavailable',
      provenance:complete?'step-authored-evidence':'unavailable',family:'resources-evidence',
      decisionFeedback:bi('此判讀尚未符合本步證據；請重新核對機制、單位、數量級與題目選項。','This interpretation does not yet match the step evidence. Recheck the mechanism, units, magnitude and answer options.'),
      curriculumEvidenceV31:{sequence,unit,facet,available:!!complete,courseTitle:bi(course.title,course.titleEn),facetTitle:FACETS[facet],
        nodes,focus:nodes.length?(unit-1)%nodes.length:0,
        question:complete?bi(quiz.question,quiz.questionEn):instruction,
        artifacts:complete?[...knowledge.map(item=>({label:bi(item.title,item.titleEn),text:bi(item.text,item.textEn)})),
          {label:bi('本步驗收紀錄','Acceptance record for this step'),text:bi(step.check,step.checkEn)}].slice(0,3):[]},
      coverage:bi('本步原創教材的工程判讀任務。證據台呈現本課的系統架構、本步的知識重點與驗收條件；完整內容在下方任務欄。數值是公開標稱值或明示的教學假設，不是場址設計值、運轉限值或實機試驗。','An engineering decision authored for this lesson. The bench shows this course’s system architecture, the step’s key knowledge and its acceptance criterion; full records appear in the task panel. Numbers are public nominal values or stated teaching assumptions, not site design values, operating limits or equipment tests.')
    });
}

/** Draw the course architecture and this step's records; never invents plant imagery. */
export function renderCurriculumEvidenceV31(spec,choice,lang){
  const context=spec.curriculumEvidenceV31;if(!context)return '';
  const zh=lang==='zh',selected=spec.choices.find(c=>c.id===choice);
  const text=(x,y,value,size=9,color='#4a3a12',anchor='start')=>`<text x="${x}" y="${y}" font-size="${size}" fill="${color}" text-anchor="${anchor}" font-family="system-ui,sans-serif">${esc(value)}</text>`;
  let out=`<g data-v31-evidence="resources" aria-label="${esc(context.courseTitle[lang])}"><title>${esc(context.courseTitle[lang])}</title>`;
  out+=text(20,57,short(context.courseTitle[lang],zh?28:58),9);
  out+=text(20,71,zh?`單元 ${context.unit} / 10 · ${context.facetTitle.zh} · 第 ${context.sequence} / 40 步`:`UNIT ${context.unit} / 10 · ${context.facetTitle.en} · STEP ${context.sequence} / 40`,7.5,'#7a6a44');
  const count=context.nodes.length;
  if(count){
    const gap=6,width=(362-gap*(count-1))/count;
    context.nodes.forEach((node,i)=>{
      const x=19+i*(width+gap),active=i===context.focus;
      out+=`<g data-v31-node="${i}"><title>${esc(node[lang])}</title><rect x="${x.toFixed(1)}" y="78" width="${width.toFixed(1)}" height="24" rx="5" fill="${active?'#f3d58a':'#f4eedb'}" stroke="${active?'#8a5a14':'#b9a877'}"/>`;
      out+=text((x+width/2).toFixed(1),93,short(node[lang],zh?Math.max(3,Math.floor(width/8.2)):Math.max(5,Math.floor(width/4.4))),zh?7.2:6.2,'#4a3a12','middle')+'</g>';
      if(i<count-1)out+=`<path d="M${(x+width+1).toFixed(1)} 90h${gap-2}" stroke="#8a5a14" stroke-width="1.2"/>`;
    });
  }
  const top=count?108:84,rowHeight=count?35:42;
  context.artifacts.forEach((artifact,i)=>{
    const y=top+i*(rowHeight+3),body=artifact.text[lang]||'',label=artifact.label[lang]||'';
    out+=`<g data-v31-artifact="${i}"><title>${esc(label+': '+body)}</title><rect x="19" y="${y}" width="362" height="${rowHeight}" rx="6" fill="${i===context.artifacts.length-1&&selected?'#e9d9a9':'#f1ecdc'}" stroke="#a8956a"/>`;
    out+=text(29,y+12,short(label,zh?32:64),7.5,'#8a5a14');
    out+=text(29,y+26,short(body,zh?36:72),zh?8.5:7.5)+'</g>';
  });
  if(!context.available)out+=text(29,123,zh?'尚未載入已授權的完整證據。':'Authorized evidence has not been loaded.',9);
  out+=`<title>${esc(context.question[lang])}</title>`;
  out+=text(20,228,zh?'完整題目、算式與原始證據請見下方任務欄。':'The full question, formula and evidence appear in the task panel.',8,'#7a6a44');
  out+=text(20,240,selected?(zh?'已選判讀；請記錄觀察並提交檢查。':'Interpretation selected; record observation and submit.'):(zh?'移動觀察工具，核對教材，再選擇工程判讀。':'Move the review tool, check the lesson, then choose a decision.'),zh?9:8);
  return out+'</g>';
}

/** Parse only bounded arithmetic. User input can never become executable JavaScript. */
const MODEL_FUNCTIONS={sqrt:Math.sqrt,sin:Math.sin,cos:Math.cos,tan:Math.tan,log:Math.log,log10:Math.log10,log2:Math.log2,exp:Math.exp,radians:x=>x*Math.PI/180,ceil:Math.ceil,floor:Math.floor,min:Math.min,max:Math.max,abs:Math.abs};
function arithmeticV31(expression,variables){
 const src=String(expression);if(!src||src.length>400)throw new RangeError('Invalid expression size');
 const tokens=src.match(/\s+|\d+\.?\d*(?:[eE][+-]?\d+)?|\.\d+|\*\*|[-+*/(),]|[A-Za-z_][A-Za-z0-9_]*/g)||[];
 if(tokens.join('')!==src)throw new TypeError('Invalid arithmetic token');
 const list=tokens.filter(t=>!/^\s+$/.test(t));let i=0,depth=0;
 const peek=()=>list[i],next=()=>list[i++];
 function primary(){
  if(++depth>40)throw new RangeError('Expression nested too deeply');
  const t=next();let value;
  if(t===undefined)throw new TypeError('Unexpected end of formula');
  if(t==='('){value=sum();if(next()!==')')throw new TypeError('Missing parenthesis');}
  else if(/^[\d.]/.test(t))value=Number(t);
  else if(t==='-')value=-power();else if(t==='+')value=power();
  else if(peek()==='('){const f=Object.hasOwn(MODEL_FUNCTIONS,t)?MODEL_FUNCTIONS[t]:null;if(!f)throw new TypeError('Unapproved function');next();const args=[sum()];while(peek()===','){next();args.push(sum());}if(next()!==')')throw new TypeError('Missing parenthesis');value=f(...args);}
  else if(t==='pi')value=Math.PI;
  else if(Object.hasOwn(variables,t))value=variables[t];else throw new TypeError('Unknown variable');
  depth--;return value;
 }
 function power(){const base=primary();if(peek()==='**'){next();return Math.pow(base,power());}return base;}
 function product(){let v=power();while(peek()==='*'||peek()==='/'){const op=next(),r=power();v=op==='*'?v*r:v/r;}return v;}
 function sum(){let v=product();while(peek()==='+'||peek()==='-'){const op=next(),r=product();v=op==='+'?v+r:v-r;}return v;}
 const result=sum();if(i!==list.length||!Number.isFinite(result))throw new RangeError('Formula outside its finite domain');return result;
}
export function calculateCurriculumModelV31(model,values){
 if(!model||typeof model!=='object'||!model.variables||typeof model.variables!=='object'||Array.isArray(model.variables))throw new TypeError('Missing model variables');
 const names=Object.keys(model.variables);if(!names.length||names.length>16||names.some(n=>!(/^[A-Za-z][A-Za-z0-9_]{0,31}$/.test(n))))throw new TypeError('Invalid variable names');
 if(!values||typeof values!=='object'||Object.keys(values).length!==names.length||names.some(n=>!Object.hasOwn(values,n)))throw new TypeError('Inputs do not match model');
 for(const n of names){
  const v=values[n],b=model.bounds?.[n]||{};
  if(typeof b!=='object'||Array.isArray(b)||Object.keys(b).some(k=>!['min','max','exclusiveMin','exclusiveMax'].includes(k))||(b.min!==undefined&&b.max!==undefined&&b.min>b.max))throw new TypeError(`Invalid bounds: ${n}`);
  if(typeof v!=='number'||!Number.isFinite(v)||Math.abs(v)>1e15)throw new RangeError(`Invalid input: ${n}`);
  if(b.min!==undefined&&(!Number.isFinite(b.min)||v<b.min||(b.exclusiveMin&&v===b.min)))throw new RangeError(`Below model bound: ${n}`);
  if(b.max!==undefined&&(!Number.isFinite(b.max)||v>b.max||(b.exclusiveMax&&v===b.max)))throw new RangeError(`Above model bound: ${n}`);
 }
 return arithmeticV31(model.expression,values);
}
export function modelForCurriculumV31(course,step){
 if(course?.category!=='materials'||step?.locked||!String(step?.id||'').startsWith(String(course?.id||'')+'-v31-'))return null;
 const suffix=String(step.id).match(/-v31-(\d{2})$/)?.[1],sequence=Number(suffix);if(!Number.isInteger(sequence)||sequence<1||sequence>40||step.id!==`${course.id}-v31-${suffix}`)return null;
 const unit=Math.floor((sequence-1)/4)+1;
 const model=step.v31Model||(Array.isArray(course.v31Models)?course.v31Models.find(m=>m.unit===unit):null);
 if(!model)return null;
 try{calculateCurriculumModelV31(model,model.variables);return model;}catch{return null;}
}
const formatModelV31=value=>Math.abs(value)>=1e8||(value!==0&&Math.abs(value)<1e-4)?value.toExponential(5):value.toLocaleString('en-US',{maximumSignificantDigits:7});
export function curriculumLabMarkupV31(course,step,zh=true){
 const m=modelForCurriculumV31(course,step);if(!m)return '';
 const fields=Object.entries(m.variables).map(([name,value])=>{
  const bounds=m.bounds?.[name]||{},unit=m.variableUnits?.[name]||'';
  const range=[bounds.min!==undefined?`${bounds.exclusiveMin?'>':'≥'} ${bounds.min}`:'',bounds.max!==undefined?`${bounds.exclusiveMax?'<':'≤'} ${bounds.max}`:''].filter(Boolean).join(' · ');
  return `<label class="field">${esc(name)} <small>${esc(unit)}</small><input data-v31-number="${esc(name)}" type="number" inputmode="decimal" step="any" value="${value}" ${bounds.min!==undefined?`min="${bounds.min}"`:''} ${bounds.max!==undefined?`max="${bounds.max}"`:''} style="min-height:44px;width:100%"><small>${esc(range)}</small></label>`;
 }).join('');
 return `<section id="engineeringLabV31" class="lesson-card engineering-lab" data-v31-model="${esc(step.id)}"><div class="eyebrow">${zh?'可重算的工程算例':'RECOMPUTABLE ENGINEERING MODEL'}</div><h3>${zh?'修改輸入、計算與比較':'Change inputs, compute and compare'}</h3><p><code>${esc(m.formula)}</code></p><p>${esc(zh?m.meaning:m.meaningEn)}</p><div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,180px),1fr));gap:12px">${fields}</div><div style="display:flex;gap:10px;flex-wrap:wrap;margin:14px 0"><button type="button" data-v31-compute>${zh?'計算並保存':'Compute and save'}</button><button type="button" data-v31-reset>${zh?'還原教學輸入':'Restore teaching inputs'}</button></div><output data-v31-result aria-live="polite" style="display:block;font-size:22px;font-weight:700">${zh?'按計算取得結果。':'Press Compute for the result.'}</output><p data-v31-sensitivity></p><small>${zh?'所有預設值皆為教學假設。修改輸入後需重新計算；此練習不會自動完成課程步驟。':'All defaults are teaching assumptions. Recompute after edits; this exploration does not automatically complete a lesson step.'}</small></section>`;
}
export function bindCurriculumLabV31(course,step,zh=true,doc=globalThis.document,storage){
 if(storage===undefined)try{storage=globalThis.localStorage;}catch{storage=null;}
 const m=modelForCurriculumV31(course,step),root=doc?.querySelector?.('#engineeringLabV31');if(!m||!root)return false;
 const inputs=Array.from(root.querySelectorAll('[data-v31-number]')),result=root.querySelector('[data-v31-result]'),sensitivity=root.querySelector('[data-v31-sensitivity]');
 const key='mg-v31-model:'+course.id+':'+step.id;
 const clear=()=>{result.textContent=zh?'輸入已更改，請重新計算。':'Inputs changed; compute again.';sensitivity.textContent='';root.dataset.computed='false';};
 try{const saved=JSON.parse(storage?.getItem?.(key)||'null');if(saved?.inputs){calculateCurriculumModelV31(m,saved.inputs);for(const input of inputs)input.value=String(saved.inputs[input.dataset.v31Number]);clear();}}catch{}
 for(const input of inputs)input.oninput=clear;
 root.querySelector('[data-v31-compute]').onclick=()=>{
  try{
   const values=Object.fromEntries(inputs.map(input=>{if(String(input.value).trim()==='')throw new RangeError('Empty input');return [input.dataset.v31Number,Number(input.value)];}));
   const value=calculateCurriculumModelV31(m,values);result.textContent=`${zh?'結果':'Result'}: ${formatModelV31(value)} ${m.unitLabel||''}`;root.dataset.computed='true';
   try{const varied={...values,[m.vary]:values[m.vary]*1.1};const changed=calculateCurriculumModelV31(m,varied);sensitivity.textContent=`${m.vary} +10% → ${formatModelV31(changed)} ${m.unitLabel||''}`;}catch{sensitivity.textContent=zh?'增加10%後超出模型適用範圍。':'A10% increase exceeds the model domain.';}
   try{storage?.setItem?.(key,JSON.stringify({inputs:values,result:value,savedAt:Date.now()}));}catch{}
  }catch(error){result.textContent=zh?'輸入無效或超出模型範圍。':'Invalid input or values outside the model domain.';sensitivity.textContent=error.message;root.dataset.computed='false';}
 };
 root.querySelector('[data-v31-reset]').onclick=()=>{for(const input of inputs)input.value=String(m.variables[input.dataset.v31Number]);try{storage?.removeItem?.(key);}catch{}clear();};
 return true;
}
