import fs from 'node:fs';
import assert from 'node:assert/strict';
import {spawnSync} from 'node:child_process';
import {EXPANSION_EXERCISE_IDS,resolveExpansionExercise,renderExpansionScene} from '../public/academy/expansion-exercises.js';
import {EXPANSION_STAGE_FAMILIES,EXPANSION_CONTEXT_FAMILIES,renderExpansionContext} from '../public/academy/expansion-contexts.js';
import {resolveExercise,evaluateExercise,renderExerciseSvg} from '../public/academy/process-exercises.js';

const expected='a004 a106 a405 a310 a203 b003 b102 b202 b301 b401 c001 c101 c213 c307 c407 d002 d107 d201 d310 d401'.split(' ');
assert.deepEqual([...EXPANSION_EXERCISE_IDS].sort(),[...expected].sort());
const locale=fs.readFileSync(new URL('../public/academy/locale.js',import.meta.url),'utf8');
const languages=locale.match(/const SUPPORTED = '([^']+)'/)?.[1].split(' ');
assert(languages?.includes('zh-TW')&&languages.includes('en'));
const specimens=[],geometry=new Set(),modes={},allSvg=[];
for(const id of expected){
 const course={id,sourceIds:['course-reference']},step={id:`${id}-v6-01`,sourceIds:['step-reference']};
 const spec=resolveExpansionExercise(course,step);
 assert(spec&&spec.expansion&&spec.provenance==='authored',id);
 assert.deepEqual(resolveExercise(course,step),spec,`${id}: resolver hook must choose authored task`);
 assert.deepEqual(spec.sourceIds,['step-reference']);
 assert.equal(resolveExpansionExercise(course,{id:`${id}-v6-02`}),null,'only the authored step is overridden');
 assert.equal(resolveExpansionExercise({id:'unknown'},step),null);
 for(const field of ['object','instruction','tool','evidence','coverage'])for(const language of ['zh','en'])assert(typeof spec[field]?.[language]==='string'&&spec[field][language].length>=6,`${id}/${field}/${language}`);
 assert(!evaluateExercise(spec,spec.initialState).passed,`${id}: initial state cannot pass`);
 const solved={values:Object.fromEntries(spec.controls.map(c=>[c.id,c.target])),choice:spec.expectedChoice,observed:true,performed:true};
 assert(evaluateExercise(spec,solved).passed,`${id}: expected evidence passes`);
 for(const control of spec.controls){
  const nearest=control.min+Math.round((control.target-control.min)/control.step)*control.step;
  assert(Math.abs(nearest-control.target)<=control.tolerance+1e-8,`${id}: slider target reachable`);
  assert(control.initial!==control.target,`${id}: learner must change the value`);
  assert(!evaluateExercise(spec,{...solved,values:{...solved.values,[control.id]:control.target+2*control.step}}).passed,`${id}: wrong measurement rejected`);
 }
 if(spec.expectedChoice)assert(!evaluateExercise(spec,{...solved,choice:'not-an-answer'}).passed,`${id}: wrong interpretation rejected`);
 if(spec.mode==='inspect')assert(!evaluateExercise(spec,{...solved,observed:false}).passed,`${id}: observation must be recorded`);
 if(spec.mode==='process')assert(!evaluateExercise(spec,{...solved,performed:false}).passed,`${id}: process evidence required`);
 modes[spec.mode]=(modes[spec.mode]||0)+1;
 const fragment=renderExpansionScene(spec,solved.values,solved.choice,4,'en');
 assert(fragment.includes(`data-expansion-scene="${id}"`));
 // Uniqueness must survive removal of all titles/labels and course-ID metadata.
 const shape=fragment.replace(/<text\b[^>]*>[\s\S]*?<\/text>/g,'').replace(/data-expansion-scene="[^"]*"/g,'');
 geometry.add(shape);
 for(const language of languages)for(const mentor of [false,true]){
  const svg=renderExerciseSvg({course,step,state:{exercise:mentor?solved:spec.initialState},mentor,labels:{language}});
  assert(svg.startsWith('<svg')&&svg.endsWith('</svg>'));
  assert(svg.includes(`data-scene="${spec.scene}"`));
  assert(!/NaN|undefined|Infinity|<script|onload=|(?:sixty|seventy)\(/.test(svg),`${id}/${language}: malformed output`);
  for(const match of svg.matchAll(/ d="([^"]*)"/g))assert(!/-\s+\d/.test(match[1]),`${id}: split negative path number`);
  if(['zh-TW','en'].includes(language))allSvg.push(svg);
 }
 specimens.push({courseId:id,stepId:step.id,mode:spec.mode,scene:spec.scene});
}
assert.equal(geometry.size,20,'twenty distinct diagram geometries, not cosmetic IDs or labels');
assert.deepEqual(modes,{inspect:11,measure:5,process:4});
let sharedCount=0;const sharedGeometry=new Set();
for(const group of ['technology','civil','mobility','science']){
 const {courses}=JSON.parse(fs.readFileSync(new URL(`../tools/expansion/${group}.json`,import.meta.url),'utf8'));
 for(const course of courses){
  const mapping=EXPANSION_STAGE_FAMILIES[course.id];assert.equal(mapping.length,3);assert.equal(new Set(mapping).size,3,`${course.id}: three distinct domain stages`);
  const courseScenes=new Set();
  for(const stage of course.stages)for(const raw of stage.steps){
   const step={...raw,stage},spec=resolveExercise(course,step);
   if(spec.provenance==='authored')continue;
   sharedCount++;courseScenes.add(spec.scene);
   assert.equal(spec.provenance,'semantic-template');assert.equal(spec.family,mapping[stage.order-1],`${step.id}: stage order selects domain context`);
   assert.notEqual(spec.family,'integration',`${step.id}: no generic integration fallback`);
   // Validate both incoming ID conventions and explicit order independent of ID.
   for(const stageMeta of [{id:stage.id},{id:`${course.id}-s${stage.order}`},{id:'unparsed',order:stage.order}])assert.equal(resolveExercise(course,{...raw,stage:stageMeta}).family,spec.family,`${step.id}: stage parser`);
   if(course.id==='b003')assert.notEqual(spec.scene,'bridge','suspension course never receives cable-stayed geometry');
   const solved={values:Object.fromEntries(spec.controls.map(c=>[c.id,c.target])),choice:spec.expectedChoice,observed:true,performed:true};assert(evaluateExercise(spec,solved).passed);
   for(const c of spec.controls)assert(Math.abs(c.min+Math.round((c.target-c.min)/c.step)*c.step-c.target)<=c.tolerance+1e-8,`${step.id}: reachable shared target`);
   for(const language of ['zh-TW','en'])for(const mentor of [false,true]){
    const svg=renderExerciseSvg({course,step,state:{exercise:solved},mentor,labels:{language}});assert(!/NaN|undefined|Infinity|<script|onload=/.test(svg));allSvg.push(svg);
   }
  }
  assert.equal(courseScenes.size,3,`${course.id}: stage-specific shared diagrams`);
 }
}
assert.equal(sharedCount,220);
for(const [id,f] of Object.entries(EXPANSION_CONTEXT_FAMILIES)){
 const svg=renderExpansionContext(f.scene,4,'en');assert(svg.includes(`data-domain-context="${id}"`));
 sharedGeometry.add(svg.replace(/<text\b[^>]*>[\s\S]*?<\/text>/g,'').replace(/data-(?:domain-context|expansion-scene)="[^"]*"/g,''));
 assert(f.observation[0].zh&&f.observation[0].en&&f.observation[1].zh&&f.observation[1].en);
}
assert.equal(sharedGeometry.size,Object.keys(EXPANSION_CONTEXT_FAMILIES).length,'domain contexts differ structurally');
assert.equal(resolveExercise({id:'future-course',category:'marine'},{id:'later',titleEn:'Review vessel boundary'}).family,'buoyancy','category fallback retains physical domain');
const parsed=spawnSync('python3',['-c','import json,sys,xml.etree.ElementTree as ET\nfor item in json.load(sys.stdin): ET.fromstring(item)\n'],{input:JSON.stringify(allSvg),encoding:'utf8'});
assert.equal(parsed.status,0,parsed.stderr);
console.log(`Expansion exercises PASS: 20 authored first-step tasks; ${languages.length} locale render paths (${languages.length*40} SVG renders, bilingual core/English fallback); 20 distinct geometries; ${allSvg.length} XML parses; positive/negative evidence and numeric reachability checks. Modes: ${JSON.stringify(modes)}.`);

console.log(`Shared expansion contexts PASS: ${sharedCount} steps, three appropriate stage families per course, ${sharedGeometry.size} added contexts, stage ID/order parsing, source-group alignment and geometry checks.`);

for(const [id,titleEn] of [['a405','Assemble optical acceptance and traceability'],['c001','Assemble a layered verification dossier']])assert.equal(resolveExercise({id},{id:`${id}-v6-12`,titleEn,stage:{order:3}}).mode,'inspect','documentation assembly is not physical part placement');
