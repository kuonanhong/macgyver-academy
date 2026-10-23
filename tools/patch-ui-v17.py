from pathlib import Path
r=Path(__file__).resolve().parents[1];p=r/'public/academy/app.js';s=p.read_text()
s=s.replace("import { railPathsMarkup }", "import { engineeringIslandMarkup, mountEngineeringIsland } from './engineering-island-v17.js';\nimport { railPathsMarkup }",1)
s=s.replace('let immersiveDispose=null,scenePhotoData=null,sceneMountSerial=0;','let immersiveDispose=null,scenePhotoData=null,sceneMountSerial=0;\nlet v17Assist=null;')
s=s.replace("function renderHome(){const picks=['b301','b310','b202','b101','a001','b400']", "function islandCategories(){return domainCounts().map(d=>({...d,name:catName(d.id),guided:catalog.filter(c=>c.category===d.id&&c.stages).length,icon:domainIconSvg(d.id)}));}\nfunction renderHome(){const picks=['b410','b457','b467','b401','b301','a001']",1)
s=s.replace('return `${explorerIntro().replace', 'return `${engineeringIslandMarkup(islandCategories(),{zh:isZh()})}${explorerIntro().replace',1)
s=s.replace('V16 · RAIL & TRANSPORT','V17 · ENVIRONMENT & CITIES').replace('從高速列車到智慧交通','從水循環到韌性城市').replace('From high-speed trains to transport systems','From water reuse to resilient cities').replace('100 門鐵道與交通專題，逐步理解軌道、車輛、供電、號誌、車站與營運。','100 門環境與城市課程，逐步探索水處理、海綿城市、資源回收、污染整治與環境監測。').replace('100 railway and transport projects covering track, rolling stock, traction, signalling, stations and operation.','100 environmental and urban courses covering water treatment, sponge cities, recycling, remediation and monitoring.')
s=s.replace('href="#catalog/domain/rail" class="button">${isZh()?\'探索鐵道與交通\':\'Explore rail and transport\'}','href="#catalog/domain/environment" class="button">${isZh()?\'探索環境與城市\':\'Explore environment and cities\'}',1)
s=s.replace('bind();try{const wallRoot=',"bind();if(currentPage==='home')mountEngineeringIsland($('#main [data-island-v17]'),islandCategories(),catalog,{zh:isZh()});try{const wallRoot=",1)
s=s.replace('function stopDemonstration(){','function stopDemonstration(){stopV17Assist();',1)
s=s.replace('async function completeStep(){','async function completeStep({stay=false,assisted=false}={}){',1)
s=s.replace('if(!p.completed.includes(s.id))p.completed.push(s.id);save(c.id);','if(!p.completed.includes(s.id))p.completed.push(s.id);if(assisted){p.assisted=Array.isArray(p.assisted)?p.assisted:[];if(!p.assisted.includes(s.id))p.assisted.push(s.id);}save(c.id);',1)
s=s.replace('if(index<allSteps(c).length-1){activeStep=index+1;','if(!stay&&index<allSteps(c).length-1){activeStep=index+1;',1)
needle='<div class="workflow-bar" id="workflowBar">'
strip='''<section class="v17-assisted-strip ${p.assisted?.includes(s.id)?'v17-assisted-complete':''}" aria-label="${isZh()?'單步工程輔助':'One-step engineering guidance'}"><button id="v17Assist" class="button">✦ ${isZh()?'師傅帶我完成這一步':'Guide me through this step'}</button><button id="v17AssistCancel" class="button light v17-assisted-cancel" hidden>${isZh()?'停止輔助':'Stop guidance'}</button><p id="v17AssistStatus" role="status">${p.assisted?.includes(s.id)?(isZh()?'✓ 本步已輔助完成。可自行重做，或按下一步繼續。':'✓ Completed with guidance. Repeat independently or continue to the next step.'):(isZh()?'按一次：示範操作 → 套用參數 → 說明答案 → 完成本步。每次只處理目前這一步。':'One click: demonstrate → apply parameters → explain the answer → complete this step only.')}</p><p>${isZh()?'輔助完成會留下紀錄；學習進度不代表已具備獨立操作資格。':'Guided completion is recorded; progress does not certify independent operating competence.'}</p></section>'''
assert needle in s;s=s.replace(needle,strip+needle,1)
s=s.replace("$('#assist').onclick=alignAssist;","$('#assist').onclick=alignAssist;$('#v17Assist').onclick=startV17Assist;$('#v17AssistCancel').onclick=()=>{stopV17Assist();if($('#v17AssistStatus'))$('#v17AssistStatus').textContent=isZh()?'已停止，可隨時重新開始。':'Stopped. You can restart at any time.';};",1)
functions='''
function stopV17Assist(){if(v17Assist){v17Assist.dispose();v17Assist=null;}if($('#v17Assist'))$('#v17Assist').disabled=false;if($('#v17AssistCancel'))$('#v17AssistCancel').hidden=true;}
function startV17Assist(){
 const c=course(),s=allSteps(c)[activeStep];if(!s||stepLocked(c,s))return;
 if(gateState(c,s).done){toast(isZh()?'本步已完成；按下一步繼續。':'This step is complete. Continue to the next step.');return;}
 stopMotion();stopDemonstration();captureNotes(false);pushPoseHistory();
 const owner=accountGeneration,cid=c.id,sid=s.id,{state,spec}=exerciseContext(),{practice,demo}=demonstrationState(c,s);
 const valid=()=>accountGeneration===owner&&currentPage==='workshop'&&activeId===cid&&allSteps(course())[activeStep]?.id===sid;
 practice.assisted=true;state.pose=initialPose();practice.distance=0;practice.grabbed=false;practice.released=false;practice.controls=[];practice.choice=false;practice.observed=false;practice.performed=false;
 const frames=buildDemonstration(spec,state.pose).map(f=>({...f,at:f.at*.5}));let last=-1;
 $('#v17Assist').disabled=true;$('#v17AssistCancel').hidden=false;
 $('#v17AssistStatus').textContent=isZh()?'師傅正示範本步操作；可隨時停止。':'Your mentor is demonstrating this step. Stop at any time.';
 v17Assist=createDemoController({frames,reducedMotion:!!window.matchMedia?.('(prefers-reduced-motion: reduce)').matches,now:()=>Date.now(),schedule:fn=>setTimeout(fn,40),cancel:clearTimeout,
  onFrame:frame=>{if(!valid()){stopV17Assist();return;}const before={...state.pose};state.pose={...frame.state.pose};state.exercise={...JSON.parse(JSON.stringify(frame.state.exercise)),specId:spec.id};recordPracticeMotion(before,state.pose,true);
   for(let i=last+1;i<=frame.index;i++){const f=frames[i];if(f.action==='grab')notePractice('grab');if(f.action==='adjust')for(const ctl of spec.controls)notePractice('control',ctl.id);if(f.action==='choose')notePractice('choice');if(f.action==='observe')notePractice('observed');if(f.action==='perform')notePractice('performed');if(f.action==='release')notePractice('release');}last=frame.index;
   syncExerciseControls();updatePoseFeedback();updateDemonstrationUI(frame);
  },onComplete:async()=>{if(!valid())return;v17Assist=null;demo.seen=true;demo.completedAt=Date.now();practice.released=!state.pose.grabbed;persistPose();updatePoseFeedback();
   if(!confirmAssembly()){stopV17Assist();$('#v17AssistStatus').textContent=isZh()?'已示範；請依工作台提示補完尚未通過的條件。':'Demonstration complete. Follow the workbench cue for any remaining condition.';return;}
   state.answer=s.quiz.answer;quizPass.add(cid+':'+sid);persistPose();
   $('#quizResult').textContent=(isZh()?'師傅解說：':'Mentor explanation: ')+txt(s.quiz,'explanation');
   const p=record(cid);const explanation=(isZh()?'輔助完成：':'Guided completion: ')+txt(s)+' — '+txt(s.quiz,'explanation');p.notes=(p.notes+'\\n'+explanation).slice(-20000);if($('#notes'))$('#notes').value=p.notes;
   await completeStep({stay:true,assisted:true});
  }});v17Assist.play();
}
'''
pos=s.index('function alignAssist()');s=s[:pos]+functions+s[pos:]
p.write_text(s)
f=r/'public/academy/index.html';h=f.read_text().replace('href="v16-ui.css">','href="v16-ui.css"><link rel="stylesheet" href="v17-ui.css">').replace('EDITION / 16','EDITION / 17').replace('ACADEMY · V16','ACADEMY · V17');f.write_text(h)
print('V17 island and guided completion integrated')
