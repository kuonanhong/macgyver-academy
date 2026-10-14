import fs from 'node:fs';
import assert from 'node:assert/strict';
import {resolveExercise,evaluateExercise,renderExerciseSvg} from '../public/academy/process-exercises.js';
import {initialPose,targetFor} from '../public/academy/workshop-model.js';
const courses=JSON.parse(fs.readFileSync(new URL('../public/academy/data/featured.json',import.meta.url),'utf8'));
// Compiler lessons legitimately discuss undefined behavior. Numeric failures
// belong to SVG geometry, not accessible titles or visible teaching prose.
function invalidNumericDrawing(svg){
 const geometry=svg.replace(/<(text|title|desc)\b[^>]*>[\s\S]*?<\/\1>/g,'');
 return /[A-Za-z]+Fix\(|NaN|undefined|Infinity|\b(?:nineteen|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred)\(/.test(geometry);
}
assert(!invalidNumericDrawing('<svg><title>Undefined-behavior boundaries</title><desc>Review undefined behavior, not an Infinity guarantee.</desc><text>Submit undefined-behavior evidence.</text><rect x="12" y="20" width="40" height="60"/></svg>'),'Legitimate teaching prose must not count as invalid coordinates');
assert(invalidNumericDrawing('<svg><text>Valid prose</text><rect x="NaN" y="20" width="40" height="60"/></svg>'),'NaN coordinates must still fail');
assert(invalidNumericDrawing('<svg><path d="M0 0Lundefined 12"/></svg>'),'Unresolved path coordinates must still fail');
assert(invalidNumericDrawing('<svg><g transform="translate(Infinity 2)"/></svg>'),'Infinite transforms must still fail');
let total=0,authored=0,shared=0;const scenes=new Set(),modes={},coverage=[];
for(const course of courses){
 let count=0,explicit=0;const localScenes=new Set();
 for(const stage of course.stages)for(const raw of stage.steps){
  const step={...raw,stage},spec=resolveExercise(course,step);total++;count++;
  assert(['assembly','measure','inspect','process'].includes(spec.mode),`${step.id} mode`);
  assert(spec.id&&spec.scene&&spec.object.zh&&spec.object.en&&spec.tool.zh&&spec.tool.en,`${step.id} metadata`);
  assert(['authored','semantic-template'].includes(spec.provenance));
  if(spec.provenance==='authored'){authored++;explicit++}else shared++;
  scenes.add(spec.scene);localScenes.add(spec.scene);modes[spec.mode]=(modes[spec.mode]||0)+1;
  for(const control of spec.controls){
   assert(control.step>0&&control.min<=control.max,`${step.id} control bounds`);
   assert(control.target>=control.min&&control.target<=control.max,`${step.id} target bounds`);
   const nearest=control.min+Math.round((control.target-control.min)/control.step)*control.step;
   assert(Math.abs(nearest-control.target)<=control.tolerance+1e-8,`${step.id}/${control.id}: target unreachable using slider step`);
  }
  const solved={values:Object.fromEntries(spec.controls.map(c=>[c.id,c.target])),choice:spec.expectedChoice,observed:true,performed:true};
  assert(evaluateExercise(spec,solved).passed,`${step.id} target satisfies task`);
  if(spec.mode==='inspect')assert(!evaluateExercise(spec,{...solved,observed:false}).passed,`${step.id} requires recorded observation`);
  if(spec.mode==='process')assert(!evaluateExercise(spec,{...solved,performed:false}).passed,`${step.id} requires execution evidence`);
  assert.deepEqual(targetFor(step,course),spec.target,`${step.id} renderer/pose target`);
  for(const language of ['zh-TW','en'])for(const mentor of [true,false]){
   const svg=renderExerciseSvg({course,step,state:{pose:initialPose(),exercise:mentor?solved:spec.initialState},mentor,labels:{language}});
   assert(svg.startsWith('<svg')&&svg.endsWith('</svg>'),`${step.id} SVG`);
   assert(!invalidNumericDrawing(svg),`${step.id} invalid numeric drawing`);
   for(const m of svg.matchAll(/ d="([^"]*)"/g))assert(!/-\s+\d/.test(m[1]),`${step.id} invalid split signed path coordinate: ${m[1]}`);
   assert(svg.includes(`data-scene="${spec.scene}"`));
   assert(!svg.includes('<script')&&!svg.includes('onload='));
  }
 }
 coverage.push({course:course.id,steps:count,authored:explicit,shared:count-explicit,sceneFamilies:[...localScenes]});
}
const first=courses.find(c=>c.id==='semiconductor').stages[0];
const specs=first.steps.slice(0,3).map(step=>resolveExercise(courses[0],{...step,stage:first}));
assert.deepEqual(specs.map(s=>s.scene),['cmos','mask-map','route']);
assert.deepEqual(specs.map(s=>s.mode),['assembly','inspect','process']);
const body=step=>renderExerciseSvg({course:courses[0],step:{...step,stage:first},state:{pose:initialPose()},mentor:true});
assert(new Set(first.steps.slice(0,3).map(body)).size===3);
assert(!body(first.steps[2]).includes('Substrate → oxide'), 'route branch is not a wafer assembly');
assert.equal(authored,52,'26 semiconductor + 6 packaging + 20 expansion authored tasks');
console.log(JSON.stringify({total,authored,shared,sceneFamilies:scenes.size,modes,coverage},null,2));
