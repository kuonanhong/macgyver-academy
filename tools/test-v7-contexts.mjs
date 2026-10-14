import assert from 'node:assert/strict';
import fs from 'node:fs';
import {spawnSync} from 'node:child_process';
import {V7_STAGE_FAMILIES,V7_CONTEXT_FAMILIES,renderV7Context} from '../public/academy/v7-contexts.js';
import {resolveExercise,evaluateExercise,renderExerciseSvg} from '../public/academy/process-exercises.js';

const ids='b015 b021 b103 b226 a025 a042 a211 a319 c005 c325 d036 d202'.split(' ');
assert.deepEqual(Object.keys(V7_STAGE_FAMILIES).sort(),ids.sort());
assert.equal(Object.keys(V7_CONTEXT_FAMILIES).length,11);
const svg=[],geometry=new Set();
for(const [family,definition] of Object.entries(V7_CONTEXT_FAMILIES)){
 assert(definition.observation.every(item=>item.zh&&item.en));
 for(const lang of ['zh','en']){
  const fragment=renderV7Context(definition.scene,4,lang);
  assert(fragment.length>100);
  assert(!/NaN|undefined|Infinity|<script|onload=/.test(fragment));
  svg.push(`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 304">${fragment}</svg>`);
  if(lang==='en')geometry.add(fragment.replace(/<text\b[^>]*>[\s\S]*?<\/text>/g,''));
 }
}
assert.equal(geometry.size,11,'distinct geometries after removing labels');
const webb=renderV7Context('v7-webb',4,'en');
assert.equal((webb.match(/fill="#d3b66d"/g)||[]).length,18,'Webb contains exactly 18 gold mirror segments');
const consensus=renderV7Context('v7-consensus',4,'en');
assert.equal((consensus.match(/<circle /g)||[]).length,5);
assert.equal((consensus.match(/<circle[^>]+fill="#68987b"/g)||[]).length,3,'five-node consensus highlights a majority of three');
assert(consensus.includes('Not arbitrary three acknowledgements'));
let stages=0;
for(const id of ids){
 const mapping=V7_STAGE_FAMILIES[id];assert.equal(mapping.length,4);
 for(let order=1;order<=4;order++){
  const step={id:`${id}-v7-${String(order*6).padStart(2,'0')}`,title:'彙整驗收證據',titleEn:'Assemble acceptance evidence',stage:{id:`${id}-stage${order}`,order},sourceIds:['review-source']};
  const course={id},spec=resolveExercise(course,step);
  assert.equal(spec.family,mapping[order-1],`${id} stage ${order}`);
  assert.notEqual(spec.family,'integration');
  assert.equal(spec.mode,'inspect','assembling documents is evidence review, not physical assembly');
  assert(!evaluateExercise(spec,spec.initialState).passed);
  const solved={values:{},choice:spec.expectedChoice,observed:true,performed:false};
  assert(evaluateExercise(spec,solved).passed);
  assert(!evaluateExercise(spec,{...solved,observed:false}).passed);
  assert(!evaluateExercise(spec,{...solved,choice:'appearance'}).passed);
  for(const stage of [{id:`${id}-stage${order}`},{id:`${id}-s${order}`},{id:'unparsed',order}])assert.equal(resolveExercise(course,{...step,stage}).family,spec.family);
  for(const language of ['zh-TW','en'])for(const mentor of [false,true])svg.push(renderExerciseSvg({course,step,state:{exercise:solved},mentor,labels:{language}}));
  stages++;
 }
}
let authored=0;
for(const group of ['civil','technology','science']){
 const path=new URL(`../tools/expansion-v7/${group}.json`,import.meta.url);
 if(!fs.existsSync(path))continue;
 for(const course of JSON.parse(fs.readFileSync(path,'utf8')).courses)for(const [index,stage] of course.stages.entries())for(const raw of stage.steps){
  const step={...raw,stage:{...stage,order:index+1}},spec=resolveExercise(course,step);
  assert.equal(spec.family,V7_STAGE_FAMILIES[course.id][index],raw.id);
  assert.equal(spec.mode,'inspect',raw.id);
  for(const language of ['zh-TW','en'])svg.push(renderExerciseSvg({course,step,state:{exercise:spec.initialState},labels:{language}}));
  authored++;
 }
}
const parsed=spawnSync('python3',['-c','import json,sys,xml.etree.ElementTree as ET\nfor s in json.load(sys.stdin): ET.fromstring(s)\n'],{input:JSON.stringify(svg),encoding:'utf8'});
assert.equal(parsed.status,0,parsed.stderr);
console.log(`V7 contexts PASS: 11 distinct geometries, Webb 18 mirror segments, consensus 3 of 5, ${stages} mapped stages, ${authored} currently available authored lessons, ${svg.length} bilingual SVG XML parses; evidence gates reject initial/wrong/unobserved states.`);
