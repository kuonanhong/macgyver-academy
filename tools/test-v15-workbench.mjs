import assert from 'node:assert/strict';
import fs from 'node:fs';
import {resolveExercise} from '../public/academy/process-exercises.js';
const courses=JSON.parse(fs.readFileSync(new URL('../public/academy/data/featured.json',import.meta.url),'utf8'));
const targets=JSON.parse(fs.readFileSync(new URL('./water-v15/targets.json',import.meta.url),'utf8'));
let oldSteps=0,newSteps=0;
for(const id of ['three-gorges','b202','b226']){
 const original=courses.find(c=>c.id===id);assert(original);
 const without={...original};delete without.v15Architecture;
 assert(original.v15Architecture,id+': V15 architecture is required');
 for(const step of original.stages.flatMap(s=>s.steps).filter(s=>!s.id.includes('-v15-'))){assert.deepEqual(resolveExercise(original,step),resolveExercise(without,step),id+': existing exercise preserved');oldSteps++;}
}
for(const {id} of targets){
 const course=courses.find(c=>c.id===id);assert(course,id+': guided course exists');
 const architecture=course.v15Architecture||course;
 assert(architecture.architectureFamily?.startsWith('water-'),id+': water diagram family');
 assert.equal(architecture.architectureNodes.length,5,id+': five authored concept nodes');
 const added=course.stages.flatMap(s=>s.steps).filter(s=>s.id.includes('-v15-'));
 assert.equal(added.length,40,id+': 40 real steps, no synthetic fallback');
 for(const step of added){
  const spec=resolveExercise(course,step);
  assert.equal(spec.mode,'inspect',step.id+': inspect workbench');
  assert.equal(spec.worldCourse.architectureFamily,architecture.architectureFamily);
  assert.deepEqual(spec.worldCourse.architectureNodes,architecture.architectureNodes);
  newSteps++;
 }
}
assert.equal(newSteps,4000);
console.log(JSON.stringify({passed:true,courses:targets.length,originalExerciseStepsPreserved:oldSteps,realExtensionStepsChecked:newSteps}));
