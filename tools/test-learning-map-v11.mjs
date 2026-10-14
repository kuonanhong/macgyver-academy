import assert from 'node:assert/strict';
import fs from 'node:fs';
import {LEARNING_TRACKS,LEARNING_SUBDISCIPLINES,LEARNING_ROUTES,classifyLearningCourse,buildLearningMapIndex,filterLearningMapCourses,resolveLearningRoute,learningCoursePath,renderLearningMap,mountLearningMap} from '../public/academy/learning-map.js';

const catalog=JSON.parse(fs.readFileSync(new URL('../public/academy/data/catalog.json',import.meta.url)));
const featured=JSON.parse(fs.readFileSync(new URL('../public/academy/data/featured.json',import.meta.url)));
const index=buildLearningMapIndex(catalog,featured);
const originalComputingIds=['cybersecurity',...Array.from({length:99},(_,i)=>`a${302+i}`)];
assert.equal(index.length,new Set(catalog.map(course=>course.id)).size);
assert.deepEqual(new Set(index.filter(course=>course.category==='computing').map(course=>course.id)),new Set(catalog.filter(course=>course.category==='computing').map(course=>course.id)),'All computing topics are retained');
assert.equal(originalComputingIds.length,100);
for(const id of originalComputingIds)assert(index.some(course=>course.id===id&&course.category==='computing'),`Original computing topic is retained: ${id}`);
assert.equal(LEARNING_TRACKS.length,new Set(LEARNING_TRACKS.map(track=>track.id)).size);
assert.equal(LEARNING_SUBDISCIPLINES.length,new Set(LEARNING_SUBDISCIPLINES.map(item=>item.id)).size);
assert.equal(LEARNING_SUBDISCIPLINES.length,35);
assert.equal(classifyLearningCourse({category:'computing',title:'Linux 核心移植',titleEn:'Linux kernel porting',summaryEn:'Planned architecture, defensive security and testing.'}).track,'foundation','Generic summaries do not collapse every topic into cybersecurity');
assert.equal(classifyLearningCourse({category:'computing',title:'GPU 平行運算核心',titleEn:'GPU parallel-compute cores'}).subdiscipline,'ai-gpu');
assert.equal(classifyLearningCourse({category:'computing',title:'FPGA 資料流加速器',titleEn:'FPGA dataflow accelerators'}).subdiscipline,'ai-fpga');
assert.equal(classifyLearningCourse({category:'computing',title:'Cerebras CS-3 晶圓尺度叢集',titleEn:'Cerebras CS-3 wafer-scale cluster',learningTrack:'ai',learningSubdiscipline:'ai-wafer'}).subdiscipline,'ai-wafer');
assert.equal(classifyLearningCourse({category:'semiconductor',title:'矽晶圓線鋸切片',titleEn:'Silicon wafer wire sawing'}).track,'semiconductor','Ordinary wafer processing is not an AI accelerator');
assert(classifyLearningCourse({category:'quantum',title:'Majorana parity',learningTrack:'quantum',learningSubdiscipline:'quantum-topological'}).subdivisionNote[1].includes('does not establish topology'));
assert.equal(classifyLearningCourse({category:'computing',title:'量子通訊網路測試平台',titleEn:'Quantum-communication network testbeds'}).track,'networks','Quantum communication is not presented as a quantum computer');
assert.equal(classifyLearningCourse({category:'energy',title:'小型模組化反應爐',titleEn:'Small modular reactor'}).subdiscipline,'energy-smr');
assert.equal(classifyLearningCourse({category:'energy',title:'核融合仿星器',titleEn:'Fusion stellarator'}).subdiscipline,'energy-fusion');
assert.equal(classifyLearningCourse({category:'quantum',title:'超導量子位元',titleEn:'Superconducting qubits'}).subdiscipline,'quantum-superconducting');
assert.equal(classifyLearningCourse({category:'megascience',title:'超導加速器低溫分配系統',titleEn:'Superconducting accelerator cryogenic distribution'}).track,'science','An accelerator is not inferred to be a quantum computer');
assert.equal(classifyLearningCourse({category:'computing',title:'核心設計',titleEn:'Kernel design',subcategory:'operating-systems',subcategoryTitle:'作業系統',subcategoryTitleEn:'Operating systems'}).subdiscipline,'foundation-operating-systems','Authored subcategories remain available as filters');

const expansion=[
  ...['superconducting','ion','neutral','photon','spin','annealing','qec','topological'].map((school,i)=>({id:`quantum-fixture-${i}`,category:'computing',title:`量子門派 ${school}`,titleEn:`Quantum school ${school}`,learningTrack:'quantum',learningSubdiscipline:`quantum-${school}`,status:'roadmap'})),
  {id:'fixture-neural',category:'computing',title:'神經網路',titleEn:'Neural networks',learningTrack:'ai',learningSubdiscipline:'ai-neural',status:'roadmap'},
  {id:'fixture-tpu',category:'computing',title:'TPU',titleEn:'TPU',learningTrack:'ai',learningSubdiscipline:'ai-tpu',status:'roadmap'},
  {id:'fixture-nuclear',category:'energy',title:'核電廠',titleEn:'Nuclear plant',learningTrack:'energy',learningSubdiscipline:'energy-nuclear',status:'roadmap'},
  {id:'fixture-smr',category:'energy',title:'SMR',titleEn:'SMR',learningTrack:'energy',learningSubdiscipline:'energy-smr',status:'roadmap'},
  {id:'fixture-fusion',category:'energy',title:'核融合',titleEn:'Fusion',learningTrack:'energy',learningSubdiscipline:'energy-fusion',status:'roadmap'},
  ...['oil','gold','mining'].map(school=>({id:`fixture-${school}`,category:'resources',title:`資源 ${school}`,titleEn:`Resource ${school}`,learningTrack:'resources',learningSubdiscipline:`resources-${school}`,status:'roadmap'}))
];
const enlarged=buildLearningMapIndex([...catalog,...expansion],featured);
assert.equal(enlarged.length,index.length+expansion.length);
for(const item of expansion) assert.equal(enlarged.find(course=>course.id===item.id).subdiscipline,item.learningSubdiscipline);
for(const school of ['superconducting','ion','neutral','photon','spin','annealing','qec','topological']) assert(filterLearningMapCourses(enlarged,{track:'quantum',subdiscipline:`quantum-${school}`}).length>=1);
assert(filterLearningMapCourses(enlarged,{query:'GPu'}).some(course=>course.id==='a304'));
assert(filterLearningMapCourses(enlarged,{query:'量子'}).length>=8);
assert(filterLearningMapCourses(enlarged,{track:'energy',query:'geothermal'}).length>=5);
assert.equal(filterLearningMapCourses(enlarged,{query:'unfindable-fixture-998'}).length,0);

const lockedFixture={id:'a304',title:'GPU 平行運算核心',titleEn:'GPU parallel-compute cores',category:'computing',status:'guided',locked:true,stepCount:24};
const secureIndex=buildLearningMapIndex([lockedFixture],[{...lockedFixture,locked:false,stages:[{steps:[]}]}]);
assert(secureIndex[0].locked,'Stale featured data cannot clear a catalog lock');
assert.equal(filterLearningMapCourses(secureIndex,{maturity:'locked'}).length,1);
assert.equal(filterLearningMapCourses(secureIndex,{maturity:'research'}).length,0);
assert.equal(buildLearningMapIndex([...catalog,catalog[0]],featured).length,index.length,'Duplicate metadata does not create duplicate cards');
assert.equal(resolveLearningRoute({courses:['missing-course','a304','a304',{track:'quantum',subdiscipline:'quantum-ion'}]},enlarged).length,2,'Missing and duplicate course links are removed');
assert.equal(learningCoursePath('missing',index),null);
assert(learningCoursePath('a304',index).prior.some(course=>course.id==='a303'));
assert(learningCoursePath('a304',index).next.some(course=>course.id==='a305'));
assert.equal(learningCoursePath('quantum-fixture-1',enlarged).prior.length,0,'Alternative quantum schools are comparisons, not a fabricated serial prerequisite');

const authoredExpansionPath=new URL('./computing-v11/expansion.json',import.meta.url);
if(fs.existsSync(authoredExpansionPath)) {
  const authored=JSON.parse(fs.readFileSync(authoredExpansionPath)).courses;
  const bySubdivision=new Map(LEARNING_SUBDISCIPLINES.map(item=>[item.id,item]));
  assert.equal(authored.length,80);
  for(const course of authored) {
    const definition=bySubdivision.get(course.learningSubdiscipline);
    assert(definition,`Known authored expansion subdiscipline: ${course.id}`);
    assert.equal(definition.track,course.learningTrack,`Matching expansion track: ${course.id}`);
    const resolved=classifyLearningCourse(course);
    assert.equal(resolved.track,course.learningTrack,course.id);
    assert.equal(resolved.subdiscipline,course.learningSubdiscipline,course.id);
  }
  assert.equal(authored.find(course=>course.id==='v11-majorana-parity')?.learningSubdiscipline,'quantum-topological');
  assert.equal(authored.find(course=>course.id==='v11-cerebras-cs3')?.learningSubdiscipline,'ai-wafer');
}

for(const language of ['zh-TW','en']) {
  const seen=new Set();
  const count=Math.ceil(enlarged.length/18);
  for(let page=0;page<count;page++) {
    const html=renderLearningMap([...catalog,...expansion],featured,language,{page});
    for(const match of html.matchAll(/data-learning-course="([^"]+)"/g)) {assert(!seen.has(match[1]),'Paginated card IDs do not repeat');seen.add(match[1]);}
    for(const match of html.matchAll(/href="#project\/([^"]+)"/g)) assert(enlarged.some(course=>course.id===decodeURIComponent(match[1])),`No missing project links: ${match[1]}`);
    assert(!/<iframe|<script|on(?:click|load|error)=/i.test(html),'The map does not load external media or inline handlers');
    assert(html.includes('role="search"')&&html.includes('role="status"'));
  }
  assert.equal(seen.size,enlarged.length,'Every item is available through pagination');
  const selected=renderLearningMap(catalog,featured,language,{selectedId:'a304',track:'ai'});
  assert(selected.includes('id="learningMapPathTitle"'));
  assert(selected.includes(language==='en'?'not enforced prerequisites':'不是強制先修'));
  const empty=renderLearningMap(catalog,featured,language,{query:'unfindable-fixture-998'});
  assert(!empty.includes('data-learning-course='));
  assert(empty.includes(language==='en'?'No matching topics':'沒有符合的項目'));
}
const attack=renderLearningMap([{id:'fixture-<x>"',title:'<script>alert(1)</script>',titleEn:'<img src=x onerror=alert(1)>',category:'computing',summary:'<svg onload=alert(1)>',status:'roadmap'}],[],'en',{query:'" autofocus onfocus="alert(1)'});
assert(!/<script|<img|<svg onload|value=""\sautofocus/i.test(attack));
assert(attack.includes('&quot; autofocus onfocus=&quot;'));
const hostileRoute=renderLearningMap(catalog,featured,'en',{routes:[{title:['<script>','<script>'],goal:['<img>','<img>'],courses:['a302','a303','missing']} ]});
assert(!/<script|<img>/i.test(hostileRoute));
assert(hostileRoute.includes('&lt;script&gt;'));

const listeners=new Map();let opened=null,rendered=0;
const formValues={query:'GPU',subdiscipline:'',maturity:''};
const form={querySelector:selector=>({value:formValues[selector.match(/name="([^"]+)"/)[1]]||''})};
const root={innerHTML:'',addEventListener:(type,handler)=>listeners.set(type,handler),removeEventListener:(type,handler)=>{assert.equal(listeners.get(type),handler);listeners.delete(type);},contains:()=>true,querySelector:selector=>selector==='[data-map-filter-form]'?form:null};
const controller=mountLearningMap(root,{catalog,featured,language:'en',onRendered:()=>rendered++,onOpenCourse:id=>{opened=id;}});
assert(root.innerHTML.includes('Course & skill map'));
assert.equal(listeners.size,3);
const click=(dataset,extras={})=>{let prevented=false;const target={dataset,...extras};listeners.get('click')({target:{closest:()=>target},preventDefault:()=>{prevented=true;}});return prevented;};
click({mapTrack:'cyber'});assert.equal(controller.getState().track,'cyber');
click({mapTrack:''});
listeners.get('submit')({target:{matches:()=>true},preventDefault(){}});assert.equal(controller.getState().query,'GPU');assert(root.innerHTML.includes('data-learning-course="a304"'));
click({mapSelectCourse:'a304'});assert.equal(controller.getState().selectedId,'a304');
click({mapClosePath:''});assert.equal(controller.getState().selectedId,'');
assert(click({learningOpen:'a304'}));assert.equal(opened,'a304');
click({mapReset:''});assert.equal(controller.getState().query,'');
click({mapPage:'1'});assert.equal(controller.getState().page,1);
const previous=controller.getState().page;click({mapPage:'99'},{disabled:true});assert.equal(controller.getState().page,previous);
listeners.get('change')({target:{matches:selector=>selector==='[data-map-page-input]',value:'2'}});assert.equal(controller.getState().page,1);
controller.update({language:'zh-TW',state:{selectedId:'a304'}});assert(root.innerHTML.includes('課程與技能地圖'));
controller.update({catalog:[catalog[0]],featured:[]});assert.equal(controller.getState().selectedId,'','Removed courses are cleared after account/data changes');
controller.dispose();assert.equal(listeners.size,0);controller.dispose();const final=root.innerHTML;controller.update({catalog});assert.equal(root.innerHTML,final);
assert(rendered>=8);

// Simulate the exact lifetime boundary used by protected account changes:
// dispose the real map before replacing the main content, then invoke queued
// handlers from the old map. They must neither repaint nor trigger rendering.
{
  const handlers=new Map();let renders=0;
  const host={innerHTML:'',addEventListener:(type,handler)=>handlers.set(type,handler),removeEventListener:(type,handler)=>{assert.equal(handlers.get(type),handler);handlers.delete(type);},contains:()=>true,querySelector:()=>null};
  const paid={id:'protected-paid-fixture',title:'A 的課程',titleEn:'A course',category:'computing',status:'guided',locked:false,summaryEn:'Original public course summary',stages:[{steps:[{id:'paid-step',knowledge:[{text:'A-only lesson'}]}]}]};
  const first=mountLearningMap(host,{catalog:[paid],featured:[paid],language:'en',onRendered:()=>renders++});
  const queued={...Object.fromEntries(handlers)};assert.equal(renders,1);
  first.dispose();assert.equal(handlers.size,0);
  host.innerHTML='<div role="status">Checking account and course access</div>';
  const hidden=host.innerHTML;
  queued.click({target:{closest:()=>({dataset:{mapTrack:'ai'}})},preventDefault(){}});
  queued.submit({target:{matches:()=>true},preventDefault(){}});
  queued.change({target:{matches:()=>true,value:'2'}});
  first.update({catalog:[paid],featured:[paid]});
  assert.equal(host.innerHTML,hidden,'Queued old controller events cannot repaint old entitlements after protected removal');
  assert.equal(renders,1,'Disposed callbacks do not invoke localization/render callbacks');
  const denied={...paid,stages:[],locked:true};
  const second=mountLearningMap(host,{catalog:[denied],featured:[denied],language:'en'});
  assert(host.innerHTML.includes('learning-map-status locked'),'The new account receives locked metadata');
  assert(!host.innerHTML.includes('A-only lesson'),'Private lesson material is not emitted by the map');
  second.dispose();assert.equal(handlers.size,0);
}

console.log(JSON.stringify({ok:true,catalog:index.length,originalComputingRetained:originalComputingIds.length,computing:index.filter(course=>course.category==='computing').length,expandedFixture:enlarged.length,tracks:LEARNING_TRACKS.length,subdisciplines:LEARNING_SUBDISCIPLINES.length,routes:LEARNING_ROUTES.length,tests:'Complete bilingual pagination, all 100 computing IDs, declared quantum/energy/resource schools, research and lock labels, valid links, XSS escaping, account-data refresh, protected removal with inert queued callbacks, and mount/dispose controls.'},null,2));
