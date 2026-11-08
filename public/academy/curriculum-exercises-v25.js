/** V25 lesson evidence workbench. No new lesson/answer payload is bundled here. */
const bi=(zh,en)=>({zh,en});
const esc=value=>String(value??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const short=(value,n)=>{const chars=Array.from(String(value??'').replace(/\s+/g,' '));return chars.length>n?chars.slice(0,n-1).join('')+'…':chars.join('')};

export function resolveCurriculumExerciseV25(course,step,make){
  const match=/^(qpu|ai)-v25-(\d{3})$/.exec(String(course.id||''));
  if(!match||Number(match[2])<1||Number(match[2])>100||Number(course.curriculumVersion)!==25)return null;
  const track=match[1]==='qpu'?'quantum':'ai';
  const stepMatch=String(step.id||'').match(/-v25-(\d{2})$/);
  const sequence=Number(stepMatch?.[1]);
  if(!stepMatch||step.id!==`${course.id}-v25-${stepMatch[1]}`||sequence<1||sequence>40)return null;
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
    `${step.instruction}\n觀察與紀錄：${step.observation}\n證據判讀：${quiz.question}\n選擇與本步資料相符的判讀，再記錄觀察。`,
    `${step.instructionEn}\nObserve and document: ${step.observationEn}\nEvidence decision: ${quiz.questionEn}\nChoose the interpretation supported by this step, then record your observation.`
  ):bi('請載入已授權的完整步驟，才能開始此證據任務。','Load the authorized complete step before starting this evidence task.');
  const evidence=complete?bi(`${step.check}\n${quiz.explanation}`,`${step.checkEn}\n${quiz.explanationEn}`):bi('尚未載入本步證據。','Step evidence has not been loaded.');
  return make(`${step.id}-authored-evidence-v25`,'inspect',`curriculum-v25:${track}`,object,instruction,
    track==='quantum'?bi('量子模型、觀測與驗收證據台','Quantum model, observation and acceptance workbench'):bi('張量、效能與驗收證據台','Tensor, performance and acceptance workbench'),evidence,{
      choices:[...choices.slice(offset),...choices.slice(0,offset)],expectedChoice:complete?'answer-'+quiz.answer:'unavailable',
      provenance:complete?'step-authored-evidence':'unavailable',family:track==='quantum'?'quantum-evidence':'tensor-evidence',
      decisionFeedback:bi('此判讀尚未符合本步證據；請重新核對模型假設、輸入條件與題目選項。','This interpretation does not yet match the step evidence. Recheck model assumptions, input conditions and answer options.'),
      curriculumEvidenceV25:{track,sequence,available:!!complete,courseTitle:bi(course.title,course.titleEn),
        question:complete?bi(quiz.question,quiz.questionEn):instruction},
      coverage:bi('本步原創教材的證據判讀任務。圖中為量測／計算紀錄的概念工作流；不代表原廠設備拓樸、量子態演化或 AI 運算模擬。完整算例與實驗紀錄請依本步教材完成。','An evidence decision authored for this lesson. The diagram is a conceptual workflow for measurement/calculation records, not an equipment topology, quantum-state simulation or AI execution model. Complete calculations and laboratory records using this step’s lesson.')
    });
}

/** A workflow board, explicitly not a fictitious QPU/tensor hardware diagram. */
export function renderCurriculumEvidenceV25(spec,choice,lang){
  const context=spec.curriculumEvidenceV25;if(!context)return '';
  const zh=lang==='zh',quantum=context.track==='quantum',selected=spec.choices.find(c=>c.id===choice);
  const labels=quantum?(zh?['模型與假設','量子觀測','經典紀錄','證據驗收']:['Model / assumptions','Quantum observation','Classical record','Evidence review']):(zh?['張量與輸入','運算／記憶體','量測紀錄','證據驗收']:['Tensors / inputs','Compute / memory','Measurement record','Evidence review']);
  const text=(x,y,value,size=9,color='#234b4e',anchor='start')=>`<text x="${x}" y="${y}" font-size="${size}" fill="${color}" text-anchor="${anchor}" font-family="system-ui,sans-serif">${esc(value)}</text>`;
  let out=`<g data-v25-evidence="${context.track}" aria-label="${esc(context.courseTitle[lang])}"><title>${esc(context.courseTitle[lang])}</title>`;
  out+=text(20,59,short(context.courseTitle[lang],zh?28:58),9);
  out+=text(20,75,zh?`本步證據工作流 · ${context.sequence} / 40`:`STEP EVIDENCE WORKFLOW · ${context.sequence} / 40`,8,'#607e80');
  labels.forEach((label,i)=>{
    const x=19+i*95;
    if(i<3)out+=`<path d="M${x+79} 117h12m-4-3 4 3-4 3" fill="none" stroke="#6b9695" stroke-width="1.5"/>`;
    out+=`<rect x="${x}" y="90" width="79" height="55" rx="7" fill="${i===3&&selected?'#e9d9a9':'#e1eeea'}" stroke="#719795"/>`;
    out+=text(x+39.5,110,String(i+1),10,'#326b70','middle')+text(x+39.5,132,label,zh?9:6.7,'#234b4e','middle');
  });
  const question=context.question[lang],questionChars=Array.from(String(question));
  out+=`<rect x="19" y="157" width="362" height="62" rx="7" fill="#f8fbf5" stroke="#b0c7bd"/><title>${esc(question)}</title>`;
  out+=text(29,173,zh?'依本步資料判讀（完整題目在下方任務欄）':'USE THIS STEP’S EVIDENCE · FULL QUESTION IN TASK PANEL',7.5,'#607e80');
  const lineLength=zh?31:64;
  out+=text(29,191,questionChars.slice(0,lineLength).join(''),zh?9:8);
  out+=text(29,207,short(questionChars.slice(lineLength).join(''),lineLength),zh?9:8);
  out+=text(20,237,selected?(zh?'已選判讀；請記錄觀察並提交檢查。':'Interpretation selected; record observation and submit.'):(zh?'移動觀察工具，核對教材，再選擇證據判讀。':'Move the review tool, check the lesson, then choose evidence.'),zh?9:8);
  return out+'</g>';
}
