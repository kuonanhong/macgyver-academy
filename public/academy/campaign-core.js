/* MacGyver Academy V20 — original educational campaign state machine.
 * No fab24hr engine, story, characters, or assets are copied here.
 * Simulation records are separate from course completion and certification.
 */
(function(root){
'use strict';
const own=(o,k)=>Object.prototype.hasOwnProperty.call(o,k);
const clone=v=>JSON.parse(JSON.stringify(v));
const finite=v=>typeof v==='number'&&Number.isFinite(v);
const clamp=(x,a,b)=>Math.max(a,Math.min(b,x));
function expression(node,values,depth=0){
 if(depth>24)throw Error('Expression nesting limit');
 if(finite(node))return node;
 if(typeof node==='string'){if(!own(values,node)||!finite(values[node]))throw Error('Unknown or invalid input: '+node);return values[node];}
 if(!node||typeof node!=='object'||!Array.isArray(node.args)||node.args.length<1||node.args.length>12)throw Error('Invalid expression');
 const a=node.args.map(n=>expression(n,values,depth+1));let value;
 switch(node.op){
 case 'add':value=a.reduce((x,y)=>x+y,0);break;
 case 'sub':if(a.length!==2)throw Error('sub needs 2 arguments');value=a[0]-a[1];break;
 case 'mul':value=a.reduce((x,y)=>x*y,1);break;
 case 'div':if(a.length!==2||a[1]===0)throw Error('Invalid division');value=a[0]/a[1];break;
 case 'pow':if(a.length!==2)throw Error('pow needs 2 arguments');value=a[0]**a[1];break;
 case 'sqrt':if(a.length!==1||a[0]<0)throw Error('Invalid square root');value=Math.sqrt(a[0]);break;
 case 'exp':if(a.length!==1)throw Error('exp needs 1 argument');value=Math.exp(a[0]);break;
 case 'abs':if(a.length!==1)throw Error('abs needs 1 argument');value=Math.abs(a[0]);break;
 case 'min':value=Math.min(...a);break;
 case 'max':value=Math.max(...a);break;
 default:throw Error('Unsupported operation');
 }
 if(!finite(value))throw Error('Non-finite model output');return value;
}
function inputValues(model,recommended=false){return Object.fromEntries(model.inputs.map(i=>[i.id,recommended?i.recommended:i.value]));}
function evaluate(model,values){
 for(const input of model.inputs){const v=values[input.id];if(!finite(v)||v<input.min||v>input.max)throw Error('Input outside range: '+input.id);}
 const value=expression(model.expression,values),scale=Math.max(1,Math.abs(value),Math.abs(model.target.min),Math.abs(model.target.max)),eps=1e-10*scale;
 return {value,pass:value>=model.target.min-eps&&value<=model.target.max+eps};
}
function validateCampaign(c){
 const errors=[];const id=/^[a-zA-Z0-9][a-zA-Z0-9_-]{0,99}$/;
 if(!c||!id.test(c.id||''))errors.push('Invalid campaign id');
 if(!Array.isArray(c?.missions)||!c.missions.length)errors.push('No missions');
 if(!Array.isArray(c?.stations)||!c.stations.length)errors.push('No stations');
 const stations=new Set((c?.stations||[]).map(s=>s.id)),seen=new Set();
 for(const m of c?.missions||[]){
  if(!id.test(m.id||'')||seen.has(m.id))errors.push('Invalid/duplicate mission id '+m.id);seen.add(m.id);
  if(!stations.has(m.stationId))errors.push('Unknown station '+m.stationId);
  if(!m.title||!m.titleEn||!m.brief||!m.briefEn)errors.push('Missing bilingual mission text '+m.id);
  if(!Array.isArray(m.evidence)||!m.evidence.length||new Set(m.evidence.map(e=>e.id)).size!==m.evidence.length)errors.push('Invalid evidence '+m.id);
  if(!Array.isArray(m.decisions)||m.decisions.length<2||m.decisions.filter(d=>d.recommended).length!==1||new Set(m.decisions.map(d=>d.id)).size!==m.decisions.length)errors.push('Invalid decisions '+m.id);
  try{
   if(!m.model||!Array.isArray(m.model.inputs)||!m.model.inputs.length||new Set(m.model.inputs.map(i=>i.id)).size!==m.model.inputs.length)throw Error('Invalid inputs');
   for(const i of m.model.inputs)if(!id.test(i.id)||![i.min,i.max,i.step,i.value,i.recommended].every(finite)||i.min>i.max||i.step<=0)throw Error('Invalid input metadata');
   if(!finite(m.model.target.min)||!finite(m.model.target.max)||m.model.target.min>m.model.target.max)throw Error('Invalid target');
   evaluate(m.model,inputValues(m.model));if(!evaluate(m.model,inputValues(m.model,true)).pass)throw Error('Recommended inputs miss target');
  }catch(e){errors.push(m.id+': '+e.message);}
 }
 return errors;
}
function missionState(m){return {stationSeen:false,observed:[],inputs:inputValues(m.model),trial:null,decision:null,assisted:false};}
function initial(c){return {version:20,campaignId:c.id,index:0,paused:false,complete:false,metrics:{quality:100,safety:100,resources:100,time:0},mission:missionState(c.missions[0]),history:[],actions:[],revision:0};}
function current(c,s){return c.missions[s.index]||null;}
function readiness(c,s){const m=current(c,s);return !!m&&!s.paused&&!s.complete&&s.mission.stationSeen&&m.evidence.every(e=>s.mission.observed.includes(e.id))&&!!s.mission.trial?.pass&&!s.mission.decision;}
function record(s,action){const a={type:action.type};for(const k of ['id','value','assisted'])if(action[k]!==undefined)a[k]=action[k];s.actions.push(a);if(s.actions.length>5000)throw Error('Session action limit');s.revision++;}
function apply(c,state,action){
 if(!action||typeof action.type!=='string')throw Error('Invalid action');
 const s=clone(state),m=current(c,s);if(!m||s.campaignId!==c.id)throw Error('Campaign mismatch');
 if(action.type==='pause'){s.paused=true;record(s,action);return s;}
 if(action.type==='resume'){s.paused=false;record(s,action);return s;}
 if(s.paused||s.complete)throw Error(s.paused?'Session paused':'Session complete');
 const work=s.mission;
 if(work.decision&&action.type!=='next')throw Error('Review the result and continue');
 switch(action.type){
 case 'station':if(action.id!==m.stationId)throw Error('Inspect the active station');work.stationSeen=true;break;
 case 'observe':if(!work.stationSeen)throw Error('Inspect station first');if(!m.evidence.some(e=>e.id===action.id))throw Error('Unknown evidence');if(!work.observed.includes(action.id))work.observed.push(action.id);break;
 case 'input':{const i=m.model.inputs.find(i=>i.id===action.id);if(!i||!finite(action.value)||action.value<i.min||action.value>i.max)throw Error('Input outside range');work.inputs[i.id]=action.value;work.trial=null;break;}
 case 'trial':if(!work.stationSeen||!m.evidence.every(e=>work.observed.includes(e.id)))throw Error('Observe all evidence before the trial');work.trial=evaluate(m.model,work.inputs);s.metrics.time+=2;if(!work.trial.pass)s.metrics.resources=clamp(s.metrics.resources-1,0,100);break;
 case 'decide':{
  if(!readiness(c,s))throw Error('Complete observation and a passing trial first');
  const d=m.decisions.find(d=>d.id===action.id);if(!d)throw Error('Unknown decision');work.decision=d.id;
  for(const k of ['quality','safety','resources'])s.metrics[k]=clamp(s.metrics[k]+(finite(d.effects?.[k])?d.effects[k]:0),0,100);
  s.metrics.time=Math.max(0,s.metrics.time+(finite(d.effects?.time)?d.effects.time:0));
  if(action.assisted)work.assisted=true;
  s.history.push({missionId:m.id,decisionId:d.id,recommended:!!d.recommended,assisted:work.assisted,inputs:clone(work.inputs),result:work.trial.value,metrics:clone(s.metrics)});
  break;}
 case 'next':if(!work.decision)throw Error('Choose a decision first');if(s.index===c.missions.length-1)s.complete=true;else{s.index++;s.mission=missionState(c.missions[s.index]);}break;
 default:throw Error('Unknown action');
 }
 if(action.assisted)work.assisted=true;record(s,action);return s;
}
function nextAssistance(c,s){
 if(s.paused||s.complete)return null;const m=current(c,s),w=s.mission;
 if(w.decision)return {type:'next',assisted:true};
 if(!w.stationSeen)return {type:'station',id:m.stationId,assisted:true};
 const e=m.evidence.find(e=>!w.observed.includes(e.id));if(e)return {type:'observe',id:e.id,assisted:true};
 const i=m.model.inputs.find(i=>w.inputs[i.id]!==i.recommended);if(i)return {type:'input',id:i.id,value:i.recommended,assisted:true};
 if(!w.trial?.pass)return {type:'trial',assisted:true};
 return {type:'decide',id:m.decisions.find(d=>d.recommended).id,assisted:true};
}
function restore(c,value){
 if(!value||value.version!==20||value.campaignId!==c.id||!Array.isArray(value.actions)||value.actions.length>5000)throw Error('Invalid saved campaign');
 let s=initial(c);for(const a of value.actions)s=apply(c,s,a);return s;
}
function ending(c,s){
 if(!s.complete)return null;const wrong=s.history.filter(x=>!x.recommended).length;
 const mode=s.history.some(x=>x.assisted)?'assisted':'manual';
 const grade=s.metrics.safety<70||s.metrics.quality<65?'review':wrong?'recover':'qualified';
 return {grade,mode,wrong,decisions:s.history.length,assisted:s.history.filter(x=>x.assisted).length};
}
root.MG_CAMPAIGN_CORE=Object.freeze({expression,inputValues,evaluate,validateCampaign,initial,current,readiness,apply,nextAssistance,restore,ending});
})(typeof window!=='undefined'?window:globalThis);
