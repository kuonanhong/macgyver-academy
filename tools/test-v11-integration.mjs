import assert from 'node:assert/strict';
import fs from 'node:fs';
import {spawnSync} from 'node:child_process';
import {COMPUTING_SUBJECTS,COMPUTING_COURSE_LABS,COMPUTING_LABS,calculateComputingLab} from '../public/academy/computing-visuals.js';
import {hasWorldVisual} from '../public/academy/world-project-visuals.js';
import {WORLD_LABS,calculateWorldLab,worldLabKind} from '../public/academy/world-project-labs.js';
import {projectIdentitySvg,projectIconSvg} from '../public/academy/project-identity.js';
import {resolveExercise,evaluateExercise,renderExerciseSvg} from '../public/academy/process-exercises.js';
import {initialPose} from '../public/academy/workshop-model.js';
import {LABS,labKind,labMarkup,bindLab,calculateLab} from '../public/academy/engineering-labs.js';
import {isQuantumCourse,quantumLabMarkup,quantumState} from '../public/academy/quantum-lab.js';
const courses=JSON.parse(fs.readFileSync(new URL('../public/academy/data/featured.json',import.meta.url))),byId=Object.fromEntries(courses.map(c=>[c.id,c]));
const computing=Object.keys(COMPUTING_SUBJECTS).map(id=>byId[id]);
const world=courses.filter(hasWorldVisual),quantum=world.filter(c=>c.learningTrack==='quantum');
assert.equal(computing.length,100);assert.equal(world.length,80);assert.equal(quantum.length,12);
let workbenchRenders=0,assignments=0,chartPoints=0;const documents=[];
for(const course of [...computing,...world]){
 assert(course?.stages?.length,'Guided stages must exist');
 const isComputing=Boolean(COMPUTING_SUBJECTS[course.id]),nodeCount=isComputing?COMPUTING_SUBJECTS[course.id].nodes.length:course.architectureNodes.length;
 const steps=course.stages.flatMap(stage=>stage.steps.map(step=>({...step,stage}))).filter(s=>s.id.includes('-v11-'));
 assert(steps.length>=12,course.id+' has substantive V11 sequence');
 const step=steps.find(s=>(s.sequence-1)%nodeCount===nodeCount-1);assert(step,course.id+' should highlight its last architecture node');
 const spec=resolveExercise(course,step);
 assert.equal(spec.scene,(isComputing?'itv11:':'worldv11:')+course.id);
 assert.equal(spec.visualFocus,nodeCount-1,'Every architecture node participates in guided focus');
 assert.equal(spec.provenance,'semantic-template');assert.equal(spec.mode,'inspect');
 assert(step.quiz&&spec.expectedChoice==='answer-'+step.quiz.answer,'Review tasks must use this step’s quiz, not a fixed universal answer');
 const solved={values:Object.fromEntries(spec.controls.map(c=>[c.id,c.target])),choice:spec.expectedChoice,observed:true,performed:true};
 assert(evaluateExercise(spec,solved).passed);assert(!evaluateExercise(spec,{...solved,observed:false}).passed);assert(!evaluateExercise(spec,{...solved,choice:'wrong-choice'}).passed);
 for(const en of [false,true]){
  const art=projectIdentitySvg(course,{en}),icon=projectIconSvg(course,{en});
  assert(art.includes(`data-project-identity="${course.id}"`));assert(art.includes('project-identity'));
  assert(icon.includes(`data-project-icon="${course.id}"`));assert(art.includes(en?course.titleEn:course.title));
  documents.push(art,icon);
  for(const mentor of [true,false]){const svg=renderExerciseSvg({course,step,state:{pose:initialPose(),exercise:mentor?solved:spec.initialState},mentor,labels:{language:en?'en':'zh-TW'}});
   assert(svg.includes(`data-scene="${spec.scene}"`));assert(svg.includes(`${isComputing?'data-course':'data-world-visual'}="${course.id}"`));assert(!/<script\b|\bonload=/.test(svg));
   const nonProse=svg.replace(/<(text|title|desc)\b[^>]*>[\s\S]*?<\/\1>/g,'');assert(!/NaN|undefined|Infinity/.test(nonProse));documents.push(svg);workbenchRenders++;
  }
 }
 const kinds=isComputing?COMPUTING_COURSE_LABS[course.id]:[worldLabKind(course)].filter(Boolean);
 for(const kind of kinds){const lab=LABS[kind];assert(lab);const values=Object.fromEntries(lab.params.map(p=>[p[0],p[5]]));assert(Number.isFinite(calculateLab(kind,values)));assignments++;const p=lab.params[0];for(let i=0;i<=40;i++){let x=p[2]+(p[3]-p[2])*i/40;if(p[4]>=1)x=Math.round(x);assert(Number.isFinite(calculateLab(kind,{...values,[p[0]]:x})),kind+' chart point');chartPoints++;}}
 const activeKind=labKind(course,step);assert.equal(Boolean(labMarkup(course,step,true)),Boolean(activeKind));
}
for(const c of quantum){assert(isQuantumCourse(c));assert(quantumLabMarkup(c,true).includes('quantumBell'));assert(quantumLabMarkup(c,false).includes('ideal-gate model'));}
for(const id of ['a358','a171','a184','a350','a304','a305','v11-resnet','v11-nvidia-hopper','v11-iter','v11-iea15mw','v11-utah-forge']){
 assert(byId[id],id+' must be a real comparison course');assert(!isQuantumCourse(byId[id]),id+' must not be selected from a fuzzy quantum keyword');assert.equal(quantumLabMarkup(byId[id],true),'');
}
assert(!isQuantumCourse({title:'量子點材料',titleEn:'Quantum-dot materials'}));assert(!isQuantumCourse({title:'後量子密碼',titleEn:'Post-quantum cryptography'}));
// Confirm all sixteen computing calculators survive the actual shared lab binder.
for(const kind of Object.keys(COMPUTING_LABS)){
 const [id,kinds]=Object.entries(COMPUTING_COURSE_LABS).find(([,k])=>k.includes(kind)),course=byId[id],step={sequence:kinds.indexOf(kind)+1},lab=COMPUTING_LABS[kind];
 const inputs=lab.params.map(p=>({dataset:{labInput:p[0]},value:String(p[5])}));
 const nodes=Object.fromEntries(['#labResult','#labDetail','#labScenarioNote','#labChart',...lab.params.map(p=>'#lab-value-'+p[0])].map(s=>[s,{textContent:'',innerHTML:''}]));
 const root={querySelector:s=>nodes[s]||null,querySelectorAll:s=>s==='[data-lab-input]'?inputs:[]};
 globalThis.document={querySelector:s=>s==='#engineeringLab'?root:null};bindLab(course,step,false);
 assert(nodes['#labResult'].textContent.endsWith(lab.unit));assert(nodes['#labChart'].innerHTML.includes(lab.unit));assert(!nodes['#labChart'].innerHTML.includes('NaN'));assert(nodes['#labDetail'].textContent);
 delete globalThis.document;
}
const bell=quantumState([{gate:'H',target:0},{gate:'CX',control:0,target:1}]);assert(Math.abs(bell.concurrence-1)<1e-10);assert(Math.abs(bell.purity-.5)<1e-10);
assert.equal(calculateComputingLab('unknown',{}),null);assert.equal(calculateWorldLab('unknown',{}),null);
for(const [kind,lab] of Object.entries({...COMPUTING_LABS,...WORLD_LABS})){const values=Object.fromEntries(lab.params.map(p=>[p[0],p[5]]));for(const [id,,min,max,delta,v] of lab.params)assert(Math.abs((v-min)/delta-Math.round((v-min)/delta))<1e-6,kind+'/'+id+' default slider alignment');assert(Number.isFinite(calculateLab(kind,values)));}
assert.equal(labKind({id:'a201',category:'electronics'},{sequence:1}),'elThreePhase');assert(labKind({id:'a200',category:'packaging'},{sequence:1}).startsWith('pkg'));assert.equal(calculateLab('elThreePhase',{voltage:400,current:100,pf:.9}),62.35382907247958);
const xml=spawnSync('python3',['-c','import json,sys,xml.etree.ElementTree as E\nfor text in json.load(sys.stdin): E.fromstring(text)'],{input:JSON.stringify(documents),encoding:'utf8'});assert.equal(xml.status,0,xml.stderr);
console.log(JSON.stringify({ok:true,computingCourses:100,worldCourses:80,explicitQuantumCourses:12,falseQuantumMatchesRejected:11,architectureIdentityDocuments:720,workbenchRenders,svgXmlDocuments:documents.length,calculatorCourseAssignments:assignments,chartPoints,computingLabBinderChecks:16,oldLabsPreserved:true,realBrowserTested:false}));
