import assert from 'node:assert/strict';
import fs from 'node:fs';
import {resolveExercise,evaluateExercise} from '../../public/academy/process-exercises.js';
import {buildDemonstration,sampleDemonstration} from '../../public/academy/demo-controller.js';
import {renderWorldVisual} from '../../public/academy/world-project-visuals.js';
import {setRelatedSkills,relatedSkillsMarkup} from '../../public/academy/related-skills.js';
import {setCoursePlaces,placeForCourse,googlePlaceUrls} from '../../public/academy/course-places.js';
import {setLearningMedia,learningMediaMarkup} from '../../public/academy/learning-media.js';
import {courseNodes} from '../../public/academy/scene-v17-core.js';
const read=name=>JSON.parse(fs.readFileSync(new URL('../../public/academy/data/'+name+'.json',import.meta.url),'utf8'));
const courses=read('featured'),targets=courses.filter(c=>c.category==='environment'&&c.stages.some(s=>s.id.includes('-v17-'))),partial=process.argv.includes('--allow-partial');
assert.equal(partial?targets.length>0:targets.length===100,true,'All 100 built courses required; --allow-partial is only for authoring review');
setRelatedSkills(read('related-skills'),courses);setCoursePlaces(read('course-places'));setLearningMedia(read('media'));
let count=0,arrows=0,rendererChecks=0;
for(const c of targets){
 const steps=c.stages.flatMap(stage=>stage.steps.map(s=>({...s,stage}))).filter(s=>s.id.includes('-v17-'));assert.equal(steps.length,40,c.id+' forty new steps');
 assert.equal(new Set(steps.map(s=>s.id)).size,40,c.id+' unique new step IDs');
 assert.equal(c.stepCount,c.stages.flatMap(s=>s.steps).length,c.id+' accurate step count');
 for(const s of steps){
  const spec=resolveExercise(c,s);assert.equal(spec.id,s.id+'-evidence',s.id+' uses dedicated step evidence rather than shared fallback');assert.equal(spec.mode,'inspect');assert(spec.worldCourse,s.id+' architecture attached');
  const correct=spec.choices.find(x=>x.id===spec.expectedChoice);assert.equal(correct.label.zh,s.quiz.options[s.quiz.answer]);assert.equal(correct.label.en,s.quiz.optionsEn[s.quiz.answer]);
  const frames=buildDemonstration(spec),end=sampleDemonstration(frames,frames.at(-1).at);assert(evaluateExercise(spec,end.state.exercise).passed,s.id+' timeline reaches a valid exercise');assert.equal(end.state.pose.grabbed,false,s.id+' releases the tool');assert.equal(end.state.exercise.observed,true,s.id+' records an observation');
  assert(s.environmentExample&&Number.isFinite(s.environmentExample.expected),s.id+' numerical example available');count++;
 }
 const visual=renderWorldVisual(c);assert(!/NaN|undefined|\[object Object\]/.test(visual),c.id+' well-formed architecture');const lines=(visual.match(/marker-end=/g)||[]).length;assert(lines>0,c.id+' architecture links must be visible');arrows+=lines;
 const scene=courseNodes(c);assert(scene.nodes.length>=3);assert(scene.edges.length>0);
 const p=placeForCourse(c.id);assert(p,c.id+' readable place');assert(googlePlaceUrls(p.place).link.startsWith('https://www.google.com/maps/search/'));
 for(const zh of [true,false]){const related=relatedSkillsMarkup(c,{zh});assert(related.includes('skill-project'),c.id+' comparison renders');assert(!/<ol><\/ol>/.test(related),c.id+' comparison practice list is not empty');const media=learningMediaMarkup(c,{zh});assert(media.includes('media-guide'),c.id+' supplemental guide renders');rendererChecks+=2;}
}
console.log(JSON.stringify({passed:true,partial,courses:targets.length,newStepDemonstrations:count,visibleArchitectureArrows:arrows,rendererChecks}));
