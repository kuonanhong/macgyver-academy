/** V30 energy lesson evidence workbench. No lesson or answer payload is bundled here. */
const bi=(zh,en)=>({zh,en});
const esc=value=>String(value??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const short=(value,n)=>{const chars=Array.from(String(value??'').replace(/\s+/g,' '));return chars.length>n?chars.slice(0,n-1).join('')+'…':chars.join('')};
const FACETS={mechanism:bi('機制與能量路徑','Mechanism and energy path'),model:bi('定量估算與敏感度','Quantitative estimate and sensitivity'),verification:bi('試驗與驗證','Testing and verification'),failure:bi('失效診斷','Failure diagnosis')};
const FACET_ORDER=['mechanism','model','verification','failure'];

/** Resolve only genuine V30 energy steps: <courseId>-v30-01 … -40 in an energy course. */
export function resolveCurriculumExerciseV30(course,step,make){
  const courseId=String(course?.id||''),stepId=String(step?.id||'');
  if(course?.category!=='energy'||!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(courseId))return null;
  const stepMatch=stepId.match(/-v30-(\d{2})$/);
  const sequence=Number(stepMatch?.[1]);
  if(!stepMatch||stepId!==`${courseId}-v30-${stepMatch[1]}`||sequence<1||sequence>40)return null;
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
  const architecture=course.v30Architecture;
  const nodes=Array.isArray(architecture?.nodes)?architecture.nodes.filter(n=>Array.isArray(n)&&n.length===2).slice(0,6).map(n=>bi(String(n[0]),String(n[1]))):[];
  const knowledge=Array.isArray(step.knowledge)?step.knowledge.filter(item=>item&&['title','titleEn','text','textEn'].every(k=>typeof item[k]==='string'&&item[k].trim())).slice(0,2):[];
  return make(`${step.id}-authored-evidence-v30`,'inspect','curriculum-v30:energy',object,instruction,
    bi('能源工程證據台','Energy engineering evidence bench'),evidence,{
      choices:[...choices.slice(offset),...choices.slice(0,offset)],expectedChoice:complete?'answer-'+quiz.answer:'unavailable',
      provenance:complete?'step-authored-evidence':'unavailable',family:'energy-evidence',
      decisionFeedback:bi('此判讀尚未符合本步證據；請重新核對機制、單位、數量級與題目選項。','This interpretation does not yet match the step evidence. Recheck the mechanism, units, magnitude and answer options.'),
      curriculumEvidenceV30:{sequence,unit,facet,available:!!complete,courseTitle:bi(course.title,course.titleEn),facetTitle:FACETS[facet],
        nodes,focus:nodes.length?(unit-1)%nodes.length:0,
        question:complete?bi(quiz.question,quiz.questionEn):instruction,
        artifacts:complete?[...knowledge.map(item=>({label:bi(item.title,item.titleEn),text:bi(item.text,item.textEn)})),
          {label:bi('本步驗收紀錄','Acceptance record for this step'),text:bi(step.check,step.checkEn)}].slice(0,3):[]},
      coverage:bi('本步原創教材的工程判讀任務。證據台呈現本課的系統架構、本步的知識重點與驗收條件；完整內容在下方任務欄。數值是公開標稱值或明示的教學假設，不是電廠設計值、運轉限值或實機試驗。','An engineering decision authored for this lesson. The bench shows this course’s system architecture, the step’s key knowledge and its acceptance criterion; full records appear in the task panel. Numbers are public nominal values or stated teaching assumptions, not plant design values, operating limits or equipment tests.')
    });
}

/** Draw the course architecture and this step's records; never invents plant imagery. */
export function renderCurriculumEvidenceV30(spec,choice,lang){
  const context=spec.curriculumEvidenceV30;if(!context)return '';
  const zh=lang==='zh',selected=spec.choices.find(c=>c.id===choice);
  const text=(x,y,value,size=9,color='#4a3a12',anchor='start')=>`<text x="${x}" y="${y}" font-size="${size}" fill="${color}" text-anchor="${anchor}" font-family="system-ui,sans-serif">${esc(value)}</text>`;
  let out=`<g data-v30-evidence="energy" aria-label="${esc(context.courseTitle[lang])}"><title>${esc(context.courseTitle[lang])}</title>`;
  out+=text(20,57,short(context.courseTitle[lang],zh?28:58),9);
  out+=text(20,71,zh?`單元 ${context.unit} / 10 · ${context.facetTitle.zh} · 第 ${context.sequence} / 40 步`:`UNIT ${context.unit} / 10 · ${context.facetTitle.en} · STEP ${context.sequence} / 40`,7.5,'#7a6a44');
  const count=context.nodes.length;
  if(count){
    const gap=6,width=(362-gap*(count-1))/count;
    context.nodes.forEach((node,i)=>{
      const x=19+i*(width+gap),active=i===context.focus;
      out+=`<g data-v30-node="${i}"><title>${esc(node[lang])}</title><rect x="${x.toFixed(1)}" y="78" width="${width.toFixed(1)}" height="24" rx="5" fill="${active?'#f3d58a':'#f4eedb'}" stroke="${active?'#8a5a14':'#b9a877'}"/>`;
      out+=text((x+width/2).toFixed(1),93,short(node[lang],zh?Math.max(3,Math.floor(width/8.2)):Math.max(5,Math.floor(width/4.4))),zh?7.2:6.2,'#4a3a12','middle')+'</g>';
      if(i<count-1)out+=`<path d="M${(x+width+1).toFixed(1)} 90h${gap-2}" stroke="#8a5a14" stroke-width="1.2"/>`;
    });
  }
  const top=count?108:84,rowHeight=count?35:42;
  context.artifacts.forEach((artifact,i)=>{
    const y=top+i*(rowHeight+3),body=artifact.text[lang]||'',label=artifact.label[lang]||'';
    out+=`<g data-v30-artifact="${i}"><title>${esc(label+': '+body)}</title><rect x="19" y="${y}" width="362" height="${rowHeight}" rx="6" fill="${i===context.artifacts.length-1&&selected?'#e9d9a9':'#f1ecdc'}" stroke="#a8956a"/>`;
    out+=text(29,y+12,short(label,zh?32:64),7.5,'#8a5a14');
    out+=text(29,y+26,short(body,zh?36:72),zh?8.5:7.5)+'</g>';
  });
  if(!context.available)out+=text(29,123,zh?'尚未載入已授權的完整證據。':'Authorized evidence has not been loaded.',9);
  out+=`<title>${esc(context.question[lang])}</title>`;
  out+=text(20,228,zh?'完整題目、算式與原始證據請見下方任務欄。':'The full question, formula and evidence appear in the task panel.',8,'#7a6a44');
  out+=text(20,240,selected?(zh?'已選判讀；請記錄觀察並提交檢查。':'Interpretation selected; record observation and submit.'):(zh?'移動觀察工具，核對教材，再選擇工程判讀。':'Move the review tool, check the lesson, then choose a decision.'),zh?9:8);
  return out+'</g>';
}
