/** Deterministic mentor timeline. It never edits the learner's state. */
const copy=value=>JSON.parse(JSON.stringify(value));
const bi=(zh,en)=>({zh,en});
export function buildDemonstration(spec,startingPose={x:-86,y:50,z:30,rotation:-24,grabbed:false,precision:false}){
  const state={pose:{...startingPose,grabbed:false},exercise:copy(spec.initialState)};
  const frames=[];let time=0;
  const add=(duration,action,label,change=()=>{})=>{time+=duration;change();frames.push({at:time,action,label,state:copy(state)})};
  add(0,'identify',bi('辨識本步工具與目標','Identify the tool and target'));
  add(650,'grab',bi('抓取示意工具','Grab the teaching tool'),()=>state.pose.grabbed=true);
  add(700,'lift',bi('抬高工具，準備接近工作界面','Lift the tool toward the working interface'),()=>state.pose.z=38);
  add(1100,'move',bi('移到本步的觀察／工作位置','Move to this step’s observation / work position'),()=>Object.assign(state.pose,{x:spec.target.x,y:spec.target.y,rotation:spec.target.rotation}));
  add(750,'position',bi('降低至界面並確認位置','Lower to the interface and check the position'),()=>state.pose.z=spec.target.z);
  for(const control of spec.controls){
    const start=Number(state.exercise.values[control.id]),count=control.id==='phase'?Math.min(6,Math.max(1,Math.abs(control.target-start))):2;
    for(let n=1;n<=count;n++){
      const value=n===count?control.target:Math.round((start+(control.target-start)*n/count)/control.step)*control.step;
      add(520,'adjust',bi(`${control.label.zh}：${Number(value.toFixed(4))} ${control.unit||''}`,`${control.label.en}: ${Number(value.toFixed(4))} ${control.unit||''}`),()=>state.exercise.values[control.id]=value);
    }
  }
  if(spec.expectedChoice){const choice=spec.choices.find(c=>c.id===spec.expectedChoice);add(850,'choose',bi(`判讀：${choice?.label.zh||spec.expectedChoice}`,`Choose: ${choice?.label.en||spec.expectedChoice}`),()=>state.exercise.choice=spec.expectedChoice)}
  if(spec.mode==='inspect')add(700,'observe',bi('記錄觀察與判讀證據','Record the observation and decision'),()=>state.exercise.observed=true);
  if(spec.mode==='process')add(950,'perform',bi('執行示意製程，核對結果','Run the teaching process and check its result'),()=>state.exercise.performed=true);
  add(650,'release',bi('放開工具，再檢查操作證據','Release the tool and check the evidence'),()=>state.pose.grabbed=false);
  add(650,'ready',bi('輪到你：依同一順序完成這道工序','Your turn: perform this operation in the same order'));
  return frames;
}
export function sampleDemonstration(frames,elapsed,reducedMotion=false){
  const end=frames.at(-1).at,t=Math.max(0,Math.min(end,elapsed));let index=0;
  while(index+1<frames.length&&frames[index+1].at<=t)index++;
  const from=frames[index],to=frames[Math.min(index+1,frames.length-1)],state=copy(from.state);
  const amount=to.at===from.at?1:(t-from.at)/(to.at-from.at);
  if(!reducedMotion&&index<frames.length-1){
    const ease=amount*amount*(3-2*amount);
    for(const key of ['x','y','z','rotation'])state.pose[key]=from.state.pose[key]+(to.state.pose[key]-from.state.pose[key])*ease;
    for(const key of Object.keys(to.state.exercise.values))state.exercise.values[key]=(from.state.exercise.values[key]??0)+((to.state.exercise.values[key]??0)-(from.state.exercise.values[key]??0))*ease;
  }
  return {state,index,total:frames.length,progress:end?t/end:1,action:from.action,label:from.label,complete:t>=end};
}
export function createDemoController({frames,onFrame=()=>{},onState=()=>{},onComplete=()=>{},reducedMotion=false,now=()=>Date.now(),schedule=callback=>setTimeout(callback,40),cancel=clearTimeout}={}){
  if(!frames?.length)throw new Error('Demonstration frames required');
  let status='idle',elapsed=0,last=0,timer=null,disposed=false,notified=false;
  const emit=()=>{const frame=sampleDemonstration(frames,elapsed,reducedMotion);onFrame(frame);return frame};
  const clear=()=>{if(timer!==null){cancel(timer);timer=null}};
  const finish=()=>{clear();status='complete';onState(status);if(!notified){notified=true;onComplete()}return emit()};
  const tick=()=>{timer=null;if(disposed||status!=='playing')return;const at=now();elapsed+=Math.max(0,at-last);last=at;const frame=emit();if(frame.complete){finish();return}timer=schedule(tick)};
  const api={
    get status(){return status},get frame(){return sampleDemonstration(frames,elapsed,reducedMotion)},get duration(){return frames.at(-1).at},
    play(){if(disposed)return;if(status==='complete'){elapsed=0;notified=false}if(status==='playing')return;status='playing';last=now();onState(status);emit();timer=schedule(tick)},
    pause(){if(disposed||status!=='playing')return;elapsed+=Math.max(0,now()-last);clear();status='paused';onState(status);emit()},
    replay(){if(disposed)return;clear();elapsed=0;notified=false;status='idle';api.play()},
    next(){if(disposed)return;clear();const next=frames.find(frame=>frame.at>elapsed);elapsed=next?.at??frames.at(-1).at;if(elapsed>=frames.at(-1).at){finish();return}status='paused';onState(status);emit()},
    showComplete(){clear();elapsed=frames.at(-1).at;status='complete';notified=true;onState(status);emit()},
    dispose(){clear();disposed=true;status='disposed'},
  };return api;
}
