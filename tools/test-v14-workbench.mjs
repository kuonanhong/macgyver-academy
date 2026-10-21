import assert from 'node:assert/strict';
import fs from 'node:fs';
import {resolveExercise} from '../public/academy/process-exercises.js';
const courses=JSON.parse(fs.readFileSync(new URL('../public/academy/data/featured.json',import.meta.url),'utf8'));
let oldSteps=0,newSteps=0;
for(const id of ['hsuehshan','b102','b103']){
 const original=courses.find(c=>c.id===id);assert(original);
 const without={...original};delete without.v14Architecture;
 const extended={...original,v14Architecture:original.v14Architecture||{architectureFamily:'tunnel',architectureNodes:[['地層','Ground'],['開挖','Excavation'],['支護','Support']],architectureEdges:[[0,1],[1,2]]}};
 for(const step of original.stages.flatMap(s=>s.steps).filter(s=>!s.id.includes('-v14-'))){assert.deepEqual(resolveExercise(extended,step),resolveExercise(without,step),id+': existing exercise preserved');oldSteps++;}
 const added=original.stages.flatMap(s=>s.steps).filter(s=>s.id.includes('-v14-'));
 const targets=added.length?added:[{...original.stages[0].steps[0],id:id+'-v14-01',sequence:1}];
 for(const step of targets){const spec=resolveExercise(extended,step);assert.equal(spec.mode,'inspect');assert.equal(spec.worldCourse.architectureFamily,extended.v14Architecture.architectureFamily);assert.deepEqual(spec.worldCourse.architectureNodes,extended.v14Architecture.architectureNodes);newSteps++;}
}
console.log(JSON.stringify({passed:true,originalExerciseStepsPreserved:oldSteps,extensionStepsOrSyntheticFixturesChecked:newSteps}));
