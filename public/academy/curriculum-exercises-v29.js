/** V29 lesson evidence workbench. No new lesson/answer payload is bundled here. */
const bi=(zh,en)=>({zh,en});
const esc=value=>String(value??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const short=(value,n)=>{const chars=Array.from(String(value??'').replace(/\s+/g,' '));return chars.length>n?chars.slice(0,n-1).join('')+'…':chars.join('')};

export function resolveCurriculumExerciseV29(course,step,make){
  const match=/^(soft)-v29-(\d{3})$/.exec(String(course.id||''));
  if(!match||Number(match[2])<1||Number(match[2])>210||Number(course.curriculumVersion)!==29)return null;
  const track='software';
  const stepMatch=String(step.id||'').match(/-v29-(\d{2})$/);
  const sequence=Number(stepMatch?.[1]);
  if(!stepMatch||step.id!==`${course.id}-v29-${stepMatch[1]}`||sequence<1||sequence>40)return null;
  const quiz=step.quiz;
  const complete=!step.locked&&quiz&&Array.isArray(quiz.options)&&Array.isArray(quiz.optionsEn)
    &&quiz.options.length>=2&&quiz.options.length===quiz.optionsEn.length
    &&quiz.options.every(s=>typeof s==='string'&&s.trim())&&quiz.optionsEn.every(s=>typeof s==='string'&&s.trim())
    &&Number.isInteger(quiz.answer)&&quiz.answer>=0&&quiz.answer<quiz.options.length
    &&['instruction','instructionEn','observation','observationEn','check','checkEn'].every(k=>typeof step[k]==='string'&&step[k].trim())
    &&['question','questionEn','explanation','explanationEn'].every(k=>typeof quiz[k]==='string'&&quiz[k].trim())
    &&Array.isArray(step.knowledge)&&step.knowledge.length>=2
    &&step.knowledge.slice(0,2).every(item=>item&&['title','titleEn','text','textEn'].every(k=>typeof item[k]==='string'&&item[k].trim()));
  const choices=complete?quiz.options.map((value,i)=>({id:'answer-'+i,label:bi(value,quiz.optionsEn[i])})):[];
  const offset=choices.length?sequence%choices.length:0;
  const object=bi(short(step.title||course.title,27),short(step.titleEn||course.titleEn,51));
  const instruction=complete?bi(
    `${step.instruction}\n觀察與紀錄：${step.observation}\n證據判讀：${quiz.question}\n選擇與本步資料相符的判讀，再記錄觀察。`,
    `${step.instructionEn}\nObserve and document: ${step.observationEn}\nEvidence decision: ${quiz.questionEn}\nChoose the interpretation supported by this step, then record your observation.`
  ):bi('請載入已授權的完整步驟，才能開始此證據任務。','Load the authorized complete step before starting this evidence task.');
  const evidence=complete?bi(`${step.check}\n${quiz.explanation}`,`${step.checkEn}\n${quiz.explanationEn}`):bi('尚未載入本步證據。','Step evidence has not been loaded.');
  return make(`${step.id}-authored-evidence-v29`,'inspect',`curriculum-v29:${track}`,object,instruction,
    bi('資訊系統、程式與驗收證據台','Systems, programs and acceptance evidence'),evidence,{
      choices:[...choices.slice(offset),...choices.slice(0,offset)],expectedChoice:complete?'answer-'+quiz.answer:'unavailable',
      provenance:complete?'step-authored-evidence':'unavailable',family:'software-evidence',
      decisionFeedback:bi('此判讀尚未符合本步證據；請重新核對模型假設、輸入條件與題目選項。','This interpretation does not yet match the step evidence. Recheck model assumptions, input conditions and answer options.'),
      curriculumEvidenceV29:{track,sequence,available:!!complete,courseTitle:bi(course.title,course.titleEn),
        question:complete?bi(quiz.question,quiz.questionEn):instruction,
        artifacts:complete?[...(step.knowledge||[]).slice(0,2).map(item=>({label:bi(item.title,item.titleEn),text:bi(item.text,item.textEn)})),
          {label:bi('本階段驗收紀錄','Investigation acceptance record'),text:bi(step.check,step.checkEn)}]:[]},
      coverage:bi('本步原創教材的證據判讀任務。證據台直接呈現本案例的模型、資料與驗收條件摘要；完整內容在下方任務欄。這些是明示教學資料，不代表原廠設備拓樸、正式環境資料或實機測試。','An evidence decision authored for this lesson. The board displays this case’s model, data and acceptance criteria; full records appear in the task panel. These are stated teaching records, not equipment topology, production-system records or equipment tests.')
    });
}

/** Inspect the actual lesson's evidence records, without inventing hardware imagery. */
export function renderCurriculumEvidenceV29(spec,choice,lang){
  const context=spec.curriculumEvidenceV29;if(!context)return '';
  const zh=lang==='zh',selected=spec.choices.find(c=>c.id===choice);
  const text=(x,y,value,size=9,color='#234b4e',anchor='start')=>`<text x="${x}" y="${y}" font-size="${size}" fill="${color}" text-anchor="${anchor}" font-family="system-ui,sans-serif">${esc(value)}</text>`;
  let out=`<g data-v29-evidence="${context.track}" aria-label="${esc(context.courseTitle[lang])}"><title>${esc(context.courseTitle[lang])}</title>`;
  out+=text(20,59,short(context.courseTitle[lang],zh?28:58),9);
  out+=text(20,75,zh?`本案例證據紀錄 · ${context.sequence} / 40`:`CASE EVIDENCE RECORDS · ${context.sequence} / 40`,8,'#607e80');
  context.artifacts.forEach((artifact,i)=>{
    const y=86+i*43,body=artifact.text[lang]||'',label=artifact.label[lang]||'';
    out+=`<g data-v29-artifact="${i}"><title>${esc(label+': '+body)}</title><rect x="19" y="${y}" width="362" height="38" rx="6" fill="${i===2&&selected?'#e9d9a9':'#e1eeea'}" stroke="#719795"/>`;
    out+=text(29,y+13,short(label,zh?32:64),7.5,'#326b70');
    out+=text(29,y+28,short(body,zh?36:72),zh?8.5:7.5)+'</g>';
  });
  if(!context.available)out+=text(29,123,zh?'尚未載入已授權的完整證據。':'Authorized evidence has not been loaded.',9);
  out+=`<title>${esc(context.question[lang])}</title>`;
  out+=text(20,224,zh?'完整題目與原始證據請見下方任務欄。':'Full question and evidence appear in the task panel.',8,'#607e80');
  out+=text(20,237,selected?(zh?'已選判讀；請記錄觀察並提交檢查。':'Interpretation selected; record observation and submit.'):(zh?'移動觀察工具，核對教材，再選擇證據判讀。':'Move the review tool, check the lesson, then choose evidence.'),zh?9:8);
  return out+'</g>';
}
