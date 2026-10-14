import assert from 'node:assert/strict';
import fs from 'node:fs';
import { buildMentorSegments, createMentorGuide, mentorGuideMarkup, selectMentorVoice, splitMentorText, translateMentorSegments } from '../public/academy/mentor-guide.js';
import { buildDemonstration } from '../public/academy/demo-controller.js';
import { resolveExercise, evaluateExercise } from '../public/academy/process-exercises.js';

class Hub {
  constructor(){this.listeners=new Map()}
  addEventListener(name,fn){if(!this.listeners.has(name))this.listeners.set(name,new Set());this.listeners.get(name).add(fn)}
  removeEventListener(name,fn){this.listeners.get(name)?.delete(fn)}
  emit(name,extra={}){for(const fn of [...(this.listeners.get(name)||[])])fn({type:name,...extra})}
  count(){return [...this.listeners.values()].reduce((sum,set)=>sum+set.size,0)}
}
class Element extends Hub {
  constructor(){super();this.style={};this.attrs={};this.classes=new Set();this.classList={add:name=>this.classes.add(name),remove:name=>this.classes.delete(name)};this.isConnected=true;this.tagName='DIV';this.scrollCount=0;this.children=[]}
  setAttribute(name,value){this.attrs[name]=value}
  scrollIntoView(options){this.scrollCount++;this.scrollOptions=options}
  getBoundingClientRect(){return {left:100,top:150,right:300,bottom:220,width:200,height:70}}
  closest(){return this.tagName==='DETAILS'?this:null}
  appendChild(node){this.children.push(node)}
  remove(){this.isConnected=false;this.removed=true}
}
class Clock {
  constructor(){this.at=0;this.jobs=new Map();this.id=0}
  schedule=(fn,delay=0)=>{const id=++this.id;this.jobs.set(id,{fn,at:this.at+delay});return id};
  cancel=id=>this.jobs.delete(id);
  run(ms){const end=this.at+ms;let safety=20000;while(safety--){const next=[...this.jobs.entries()].filter(([,job])=>job.at<=end).sort((a,b)=>a[1].at-b[1].at)[0];if(!next)break;this.at=next[1].at;this.jobs.delete(next[0]);next[1].fn()}assert(safety>0,'timer loop is bounded');this.at=end}
}
class Speech extends Hub {
  constructor(voices=[]){super();this.voices=voices;this.spoken=[];this.current=null;this.cancels=0}
  getVoices(){return this.voices}
  speak(item){assert.equal(this.current,null,'speech must not overlap');this.current=item;this.spoken.push(item);item.onstart?.()}
  finish(){const item=this.current;this.current=null;item?.onend?.()}
  fail(){const item=this.current;this.current=null;item?.onerror?.({error:'not-allowed'})}
  cancel(){this.cancels++;const item=this.current;this.current=null;item?.onerror?.({error:'canceled'})}
}
class Utterance {constructor(text){this.text=text}}
const enVoice={name:'English',lang:'en-US',default:true},zhVoice={name:'國語',lang:'zh-TW'},jaVoice={name:'日本語',lang:'ja-JP'};
const flush=async()=>{for(let n=0;n<8;n++)await Promise.resolve()};
const courses=JSON.parse(fs.readFileSync(new URL('../public/academy/data/featured.json',import.meta.url),'utf8'));
const course=courses.find(item=>item.id==='semiconductor')||courses[0],step={...course.stages[0].steps[0],stage:course.stages[0]};
const spec=resolveExercise(course,step),frames=buildDemonstration(spec);
const segments=buildMentorSegments({course,step,spec,frames,zh:false});
const assertions=[];
function fixture(extra={}){
  const environment=new Hub(),document=new Hub(),clock=new Clock(),elements=new Map(),speech=new Speech(extra.voices||[enVoice]);
  environment.innerWidth=800;environment.innerHeight=600;environment.matchMedia=()=>({matches:true});
  document.defaultView=environment;document.body=new Element();document.createElement=()=>new Element();document.querySelector=selector=>elements.get(selector)||null;
  for(const selector of ['#mentorGuideStatus','#mentorGuideText','#mentorGuideNext','#mentorGuideTour','#mentorGuideSkipTour','#mentorGuideStop',...segments.lesson.map(s=>s.target),...segments.tour.map(s=>s.target),...segments.demo.map(s=>s.target)]){const node=new Element();if(selector.includes('details'))node.tagName='DETAILS';elements.set(selector,node)}
  const observed=[],completed=[],states=[];
  const guide=createMentorGuide({root:document,environment,speechSynthesis:extra.noSpeech?{}:speech,Utterance,course,step,spec,frames,language:'en',schedule:clock.schedule,cancel:clock.cancel,now:()=>clock.at,reducedMotion:true,onFrame:f=>observed.push(f),onComplete:event=>completed.push(event),onStatus:event=>states.push(event),...extra});
  return {guide,environment,document,elements,clock,speech,observed,completed,states};
}
function drainText(item){let attempts=300;while(!['complete','stopped','disposed'].includes(item.guide.status)&&attempts--)item.guide.next();assert(attempts>0,'manual reading completes');}

assert(mentorGuideMarkup({zh:true}).includes('略過按鍵導覽'));
assert.equal(selectMentorVoice([enVoice,zhVoice],'zh-TW'),zhVoice);
assert.equal(selectMentorVoice([enVoice],'ja'),null,'never read with an unrelated voice');
assert.equal(selectMentorVoice([{lang:'en-GB'},enVoice],'en-US'),enVoice);
{
 const secondVoice={name:'Preferred English',lang:'en-GB',voiceURI:'preferred-en'};
 let preferences={voiceURI:'preferred-en',rate:.75,pitch:1.2};
 const item=fixture({voices:[enVoice,secondVoice],getSpeechOptions:()=>preferences});
 await item.guide.begin({includeTour:false});await flush();assert.equal(item.speech.current.voice,secondVoice);assert.equal(item.speech.current.rate,.75);assert.equal(item.speech.current.pitch,1.2);
 preferences={voiceURI:'',rate:1.2,pitch:.85};item.guide.next();await flush();assert.equal(item.speech.current.voice,enVoice,'voice settings refresh between sections');assert.equal(item.speech.current.rate,1.2);assert.equal(item.speech.current.pitch,.85);item.guide.dispose();
 assertions.push('per-member named voice, rate and pitch applied to live narration and refreshed each section');
}
const unicode='光學🔬製程與比較。'.repeat(80),pieces=splitMentorText(unicode);
assert.equal(pieces.join(''),unicode);assert(pieces.every(text=>Array.from(text).length<=220));assert(!pieces.some(text=>/^[\uDC00-\uDFFF]|[\uD800-\uDBFF]$/.test(text)));
assertions.push('bounded Unicode narration and correct voice matching');

for(const name of ['objective','instruction','observation','failure','check'])assert(segments.lesson.some(segment=>segment.text.includes(step[name+'En'])),`whole ${name} is taught`);
for(const knowledge of step.knowledge)assert(segments.lesson.some(segment=>segment.text.includes(knowledge.textEn)),'every knowledge point is taught');
assert(!segments.lesson.some(segment=>segment.text.includes(step.quiz.explanationEn)),'quiz answer is not narrated');
for(const control of spec.controls)assert(segments.tour.some(segment=>segment.target===`[data-exercise-control="${control.id}"]`));
for(const key of ['↑ / W','← / A','↓ / S','→ / D','PageUp','PageDown','J / Q','L / E'])assert(segments.tour.some(segment=>segment.text.includes(key)));
assertions.push('full procedure, knowledge, acceptance and every control; no quiz answer');

{
 const item=fixture({noSpeech:true});assert.equal(item.guide.status,'idle');assert.equal(item.speech.spoken.length,0,'construction never autoplays');
 await item.guide.begin();assert.equal(item.guide.status,'waiting');assert.equal(item.guide.phase,'lesson');
 item.guide.skipTour();assert.equal(item.completed.length,0,'skipping tour cannot satisfy procedure gate');
 drainText(item);assert.equal(item.completed.length,1);assert.equal(item.completed[0].kind,'procedure');
 assert.equal(item.observed.at(-1).index,frames.length-1);assert(evaluateExercise(spec,item.observed.at(-1).state.exercise).passed,'text fallback reaches exact final teaching state');
 assert(!item.states.some(state=>state.phase==='tour'));item.guide.dispose();
 assertions.push('explicit start, no-audio manual reading, independent tour skip, final demo state');
}
{
 const item=fixture({noSpeech:true});await item.guide.begin();while(item.guide.phase==='lesson')item.guide.next();assert.equal(item.guide.phase,'tour');item.guide.skipTour();assert.equal(item.guide.phase,'demo');assert.equal(item.completed.length,0);drainText(item);assert.equal(item.completed[0].kind,'procedure');item.guide.dispose();
 const standalone=fixture({noSpeech:true});await standalone.guide.startTour();standalone.guide.skipTour();assert.equal(standalone.completed[0].kind,'tour');standalone.guide.dispose();
 assertions.push('skip during tour preserves demonstration; standalone tour has distinct completion');
}
{
 const item=fixture();await item.guide.begin({includeTour:false});await flush();const initial=item.guide.index;
 item.clock.run(1000);assert.equal(item.guide.index,initial,'narration waits for speech end instead of fixed animation time');
 item.speech.finish();await flush();assert(item.guide.index>=initial,'speech controls advancement');
 const oldHandler=item.speech.current?.onend;item.environment.emit('blur');assert.equal(item.guide.status,'paused');assert.equal(item.speech.current,null);
 oldHandler?.();assert.equal(item.guide.status,'paused','stale speech callback cannot restart navigation');item.guide.resume();await flush();assert.equal(item.guide.status,'speaking');
 item.environment.emit('hashchange');assert.equal(item.guide.status,'stopped');assert.equal(item.speech.current,null);item.guide.dispose();assert.equal(item.environment.count(),0);assert.equal(item.document.count(),0);
 assertions.push('speech pacing, pause/resume, blur/navigation cancellation and listener cleanup');
}
{
 const item=fixture({voices:[]});await item.guide.begin();assert.equal(item.guide.status,'preparing');
 item.speech.voices=[enVoice];item.speech.emit('voiceschanged');await flush();assert.equal(item.guide.status,'speaking');assert.equal(item.speech.current.voice,enVoice);assert.equal(item.speech.listeners.get('voiceschanged').size,0);item.guide.dispose();
 const missing=fixture({voices:[]});await missing.guide.begin();missing.clock.run(1800);await flush();assert.equal(missing.guide.status,'waiting');assert.equal(missing.states.at(-1).reason,'unavailable');assert.equal(missing.completed.length,0);missing.guide.dispose();
 assertions.push('asynchronous voiceschanged and bounded missing-voice fallback');
}
{
 const item=fixture({utteranceTimeoutMs:25});await item.guide.begin();await flush();item.clock.run(25);assert.equal(item.guide.status,'waiting');assert.equal(item.speech.current,null);assert.equal(item.states.at(-1).reason,'timeout');assert.equal(item.completed.length,0);item.guide.dispose();
 const error=fixture();await error.guide.begin();await flush();error.speech.fail();assert.equal(error.guide.status,'waiting');assert.equal(error.states.at(-1).reason,'error');error.guide.dispose();
 assertions.push('speech timeout/error fall back to manually advanced text');
}
{
 const item=fixture({language:'ja',voices:[jaVoice]});await item.guide.begin();assert.equal(item.guide.status,'waiting');assert.equal(item.speech.spoken.length,0);assert.equal(item.elements.get('#mentorGuideText').lang,'en');assert.equal(item.states.at(-1).reason,'translation');item.guide.dispose();
 const translated=fixture({language:'ja',voices:[jaVoice],translate:async({segments,language})=>({language,segments:segments.map(segment=>({id:segment.id,text:'日本語の説明。'}))})});await translated.guide.begin();await flush();assert.equal(translated.speech.current.lang,'ja-JP');assert.equal(translated.speech.current.text,'日本語の説明。');assert.equal(translated.elements.get('#mentorGuideText').lang,'ja');translated.guide.setLanguage('en');assert.equal(translated.speech.current,null);assert.equal(translated.guide.status,'idle');translated.guide.dispose();
 const malformed=fixture({language:'ja',voices:[jaVoice],translate:async()=>({language:'fr',segments:[]})});await malformed.guide.begin();assert.equal(malformed.guide.status,'waiting');assert.equal(malformed.speech.spoken.length,0);malformed.guide.dispose();
 assertions.push('no false foreign-language speech; matching translated speech and language cancellation');
}
{
 const item=fixture({noSpeech:true});await item.guide.readLesson();while(item.guide.status==='waiting'&&!item.elements.get('#lessonSection .knowledge details:nth-of-type(1)').open)item.guide.next();
 const target=item.elements.get('#lessonSection .knowledge details:nth-of-type(1)');assert.equal(target.open,true);assert(target.scrollCount>0);assert(target.classes.has('mentor-guide-target'));assert(item.document.body.children.some(node=>node.className==='mentor-guide-arrow'));
 item.guide.dispose();assert(!target.classes.has('mentor-guide-target'));assert(item.document.body.children.every(node=>node.removed));assert.equal(item.completed.length,0);
 assertions.push('knowledge disclosure, scrolling, red-arrow targeting and DOM cleanup');
}
{
 const item=fixture({noSpeech:true});const dock=new Element();dock.getBoundingClientRect=()=>({left:0,top:440,right:800,bottom:600,width:800,height:160});item.elements.set('.workshop-action-dock',dock);
 const scrolls=[];item.environment.scrollBy=options=>scrolls.push(options);
 await item.guide.startTour();const target=item.elements.get('#activateKeyboard');assert.equal(target.scrollOptions.block,'center');assert(scrolls.length>0,'target is adjusted for the fixed bottom dock');
 const pointer=item.document.body.children.at(-1);assert(Number.parseFloat(pointer.style.top)<440,'red arrow stays above the dock');
 item.guide.pause();const before=target.scrollCount;item.guide.resume();assert(target.scrollCount>before,'resume centers the current guide target again');
 item.guide.dispose();
 const tall=fixture({noSpeech:true});const lesson=tall.elements.get('#lessonSection');lesson.getBoundingClientRect=()=>({left:100,top:150,right:700,bottom:1650,width:600,height:1500});await tall.guide.readLesson();tall.guide.next();assert.equal(lesson.scrollOptions.block,'start','a large section retains its beginning instead of centering its middle');tall.guide.dispose();
 assertions.push('dock-aware centered controls, tall lesson headings and visible resumed arrow');
}
{
 const first=fixture(),second=fixture({speechSynthesis:first.speech});await first.guide.begin();await flush();assert(first.speech.current);await second.guide.begin();await flush();assert.equal(first.guide.status,'stopped');assert(first.speech.cancels>=1);assert(first.speech.current);first.guide.dispose();second.guide.dispose();
 assertions.push('only one guide owns native speech at a time');
}
{
 const requests=[];const text='製程🙂'.repeat(2300);
 const result=await translateMentorSegments({language:'ja',segments:[{id:'large',text},{id:'small',text:'Acceptance criteria'}],fetchImpl:async(url,config)=>{const body=JSON.parse(config.body);requests.push(body);assert.equal(url,'/api/translate');assert(body.texts.length<=12);assert(body.texts.join('').length<=4000);return {ok:true,json:async()=>({translations:body.texts.map((_,i)=>`訳 ${i}`)})}}});
 assert(requests.length>1);assert.equal(result.language,'ja');assert.equal(result.segments.length,2);assert(result.segments.every(segment=>segment.text));
 await assert.rejects(translateMentorSegments({language:'ja',segments:[{id:'x',text:'One'}],fetchImpl:async()=>({ok:true,json:async()=>({translations:[]})})}),/Incomplete/);
 assertions.push('bounded translation requests and incomplete-translation rejection');
}
console.log(JSON.stringify({passed:true,checks:assertions.length,coverage:assertions},null,2));
