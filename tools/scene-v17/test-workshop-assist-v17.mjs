// Exercise the actual application functions with the actual timeline, geometry and
// exercise evaluator. Deferred network responses test account/route transitions.
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import {buildDemonstration,createDemoController} from '../../public/academy/demo-controller.js';
import {resolveExercise,evaluateExercise} from '../../public/academy/process-exercises.js';
import {initialPose,alignment} from '../../public/academy/workshop-model.js';
const source=fs.readFileSync(new URL('../../public/academy/app.js',import.meta.url),'utf8');
const courses=JSON.parse(fs.readFileSync(new URL('../../public/academy/data/featured.json',import.meta.url),'utf8'));
function exact(name){const marker=new RegExp('(?:^|\\n)((?:async )?function '+name+'\\()'),m=marker.exec(source);assert(m,`${name} exists`);const from=m.index+(source[m.index]==='\n'?1:0),tail=source.slice(from),next=/\n(?:async )?function /.exec(tail);return next?tail.slice(0,next.index):tail;}
const functions=['exerciseContext','demonstrationState','demonstrationReady','practiceStatus','notePractice','confirmAssembly','gateState','stopV17Assist','startV17Assist','completeStep'].map(exact).join('\n');
function deferred(){let resolve,reject;const promise=new Promise((yes,no)=>{resolve=yes;reject=no});return {promise,resolve,reject};}
async function flush(){for(let n=0;n<8;n++)await Promise.resolve();}
function harness({protectedMode=false,submit=async()=>({}),locked=false}={}){
 let clock=0,nextTimer=0;const timers=new Map(),nodes=new Map(),poses=new Map(),data=new Map(),notices=[],submissions=[];
 const base=structuredClone(courses.find(c=>c.stages?.length&&c.stages[0].steps.length>1));assert(base,'fixture course');
 const alternate={...structuredClone(base),id:'other-course'};const catalog=[base,alternate];
 const node=id=>{if(!nodes.has(id))nodes.set(id,{disabled:false,hidden:true,textContent:'',value:'',focus(){}});return nodes.get(id);};
 const context={v17Assist:null,completionPending:false,accountGeneration:0,routeLoadSerial:0,activeId:base.id,activeStep:0,currentPage:'workshop',user:protectedMode?{id:'A'}:null,navStage:-1,navQuery:'',quizPass:new Set(),demoKey:'',mentorDemo:{status:'idle',dispose(){throw Error('Reusable mentor controller must not be disposed by one-step guidance');}},mentorGuide:{stop(){}},
  Date:{now:()=>clock},Math,JSON,Set,window:{matchMedia:()=>({matches:false})},
  setTimeout:fn=>{const id=++nextTimer;timers.set(id,fn);return id;},clearTimeout:id=>timers.delete(id),
  course:()=>catalog.find(c=>c.id===context.activeId),allSteps:c=>c.stages.flatMap((stage,stageIndex)=>stage.steps.map(s=>({...s,stage,stageIndex}))),
  stepPose:(cid,sid)=>{const key=(context.user?.id||'guest')+':'+cid+':'+sid;if(!poses.has(key))poses.set(key,{pose:initialPose(),answer:null});return poses.get(key);},
  record:cid=>{const key=(context.user?.id||'guest')+':'+cid;if(!data.has(key))data.set(key,{completed:[],assembly:[],notes:''});return data.get(key);},
  progressFor:cid=>context.record(cid),poseStorageKey:()=>context.user?.id||'guest',
  $:node,stepLocked:()=>locked,isZh:()=>false,t:x=>x,txt:(o,key='title')=>o?.[key+'En']||o?.[key]||'',exerciseText:v=>v?.en||v,
  billingState:()=>({protected:protectedMode}),accountModal:()=>{context.modalCount++;},modalCount:0,
  submitVerifiedStep:async(...args)=>{submissions.push({owner:context.user?.id,args});return submit(...args);},
  buildDemonstration,createDemoController,resolveExercise,evaluateExercise,initialPose,alignment,
  stopMotion(){},stopAssistance(){},pushPoseHistory(){},captureNotes(){},persistPose(){},updatePoseFeedback(){},syncExerciseControls(){},updateDemonstrationUI(){},refreshWorkflow(){},focusSection(){},save(){},
  toast:value=>notices.push(value),render(){context.routeLoadSerial++;context.stopV17Assist();},
 };
 vm.createContext(context);vm.runInContext(functions,context,{filename:'app.js:actual-workshop-assist'});
 return {context,nodes,poses,data,notices,submissions,course:base,node,
  start:()=>context.startV17Assist(),stop:()=>context.stopV17Assist(),
  async tick(ms){clock+=ms;const jobs=[...timers.values()];timers.clear();for(const job of jobs)job();await flush();},
  state:()=>context.stepPose(context.activeId,context.allSteps(context.course())[context.activeStep].id),
  record:()=>context.record(context.activeId),
  ready(){const sid=context.allSteps(context.course())[context.activeStep].id;context.record(context.activeId).assembly.push(sid);context.quizPass.add(context.activeId+':'+sid);context.stepPose(context.activeId,sid).answer=context.allSteps(context.course())[context.activeStep].quiz.answer;return sid;},
 };
}
let checks=0;
{
 const app=harness();app.start();await app.tick(20000);const s=app.context.allSteps(app.course)[0];
 assert.deepEqual([...app.record().completed],[s.id]);assert.deepEqual([...app.record().assisted],[s.id]);assert.equal(app.context.activeStep,0,'one click must not advance or start the next step');assert.equal(app.state().answer,s.quiz.answer);assert.equal(app.state().practice.released,true);assert(app.record().notes.includes('Guided completion:'));assert.equal(app.context.v17Assist,null);assert.equal(app.node('#v17Assist').disabled,false);assert.equal(app.node('#v17AssistCancel').hidden,true);
 app.start();await app.tick(20000);assert.equal(app.record().completed.length,1);assert.equal(app.record().notes.split('Guided completion:').length,2,'repeat click cannot duplicate a completion note');checks++;
}
{
 const app=harness();app.start();await app.tick(1000);app.stop();const pose=JSON.stringify(app.state());await app.tick(20000);assert.equal(app.record().completed.length,0);assert.equal(JSON.stringify(app.state()),pose,'cancelled callbacks cannot keep changing the pose');assert.equal(app.node('#v17Assist').disabled,false);assert(app.context.mentorDemo,'normal mentor controls remain reusable');checks++;
}
for(const change of ['course','account','page']){
 const app=harness();app.start();await app.tick(800);const old=[...app.poses.values()][0],before=JSON.stringify(old);
 if(change==='course')app.context.activeId='other-course';if(change==='account'){app.context.accountGeneration++;app.context.user={id:'B'};}if(change==='page')app.context.currentPage='home';
 await app.tick(20000);assert.equal(JSON.stringify(old),before,`${change} transition prevents stale animation state writes`);assert.equal([...app.data.values()].flatMap(p=>p.completed).length,0);checks++;
}
{
 const app=harness({locked:true});app.start();assert.equal(app.context.v17Assist,null);assert.equal(await app.context.completeStep(),false);assert.equal(app.submissions.length,0);checks++;
}
{
 const app=harness();assert.equal(await app.context.completeStep(),false);assert.equal(app.record().completed.length,0,'knowledge and assembly gates remain required');checks++;
}
{
 const reply=deferred(),app=harness({protectedMode:true,submit:()=>reply.promise});app.start();await app.tick(20000);assert.equal(app.submissions.length,1);assert.equal(app.record().completed.length,0,'server verification precedes completion');assert.equal(app.node('#v17AssistCancel').hidden,true,'committed request is not falsely advertised as cancellable');assert(app.node('#v17AssistStatus').textContent.includes('cannot be recalled'));
 reply.reject(Error('verification offline'));await flush();assert.equal(app.record().completed.length,0);assert.equal(app.record().notes,'','failed requests must not claim completion');assert.equal(app.node('#v17Assist').disabled,false);assert(app.node('#v17AssistStatus').textContent.includes('retry'));checks++;
}
for(const change of ['course','account','route-away-and-back']){
 const reply=deferred(),app=harness({protectedMode:true,submit:()=>reply.promise});app.start();await app.tick(20000);
 if(change==='course')app.context.activeId='other-course';if(change==='account'){app.context.accountGeneration++;app.context.user={id:'B'};}if(change==='route-away-and-back'){app.context.routeLoadSerial+=2;app.stop();}
 reply.resolve({});await flush();assert.equal([...app.data.values()].flatMap(p=>p.completed).length,0,`${change}: late server response cannot write into current progress`);checks++;
}
{
 const reply=deferred(),app=harness({protectedMode:true,submit:()=>reply.promise});const sid=app.ready();const first=app.context.completeStep({stay:true});assert.equal(await app.context.completeStep({stay:true}),false);assert.equal(app.submissions.length,1,'duplicate clicks share one pending request');reply.resolve({});await first;assert.deepEqual([...app.record().completed],[sid]);await app.context.completeStep({stay:true});assert.equal(app.submissions.length,1,'already completed step does not resubmit verification');checks++;
}
{
 const app=harness();const sid=app.ready();app.state().practice={assisted:true};assert.equal(await app.context.completeStep({stay:true}),true);assert.deepEqual([...app.record().assisted],[sid]);assert(app.record().notes.includes('Operation guidance used'),'manual completion retains past guidance provenance');checks++;
}
{
 const old=deferred(),newer=deferred();let calls=0;const app=harness({protectedMode:true,submit:()=>++calls===1?old.promise:newer.promise});app.ready();const oldSave=app.context.completeStep({stay:true});app.context.accountGeneration++;app.context.user={id:'B'};app.ready();const newSave=app.context.completeStep({stay:true});assert.equal(app.submissions.length,2,'slow old-account save cannot block new account');old.resolve({});await oldSave;assert(app.context.completionPending,'old request cannot clear new request pending state');newer.resolve({});await newSave;assert.equal(app.record().completed.length,1);checks++;
}
console.log(JSON.stringify({passed:true,scenarios:checks,actualTimeline:true,actualExerciseEvaluator:true,coverage:'single-step, cancellation, retry, duplicate click, access gates, stale course/account/route, assisted provenance'}));
