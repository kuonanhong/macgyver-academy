import * as labResources from '../public/academy/lab-resources.js';
import {assertRenderedData} from './assert-rendered-data.mjs';
import * as computingPaths from '../public/academy/computing-paths.js';
import * as opticsPaths from '../public/academy/optics-paths.js';
import * as structuresPaths from '../public/academy/structures-paths.js';
import * as projectIcons from '../public/academy/project-icons.js';
import * as learningMap from '../public/academy/learning-map.js';
import * as quantumLab from '../public/academy/quantum-lab.js';
// Browser-independent integration smoke test. Does not test visual layout.
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import * as electronicsPaths from '../public/academy/electronics-paths.js';
import * as membership from '../public/academy/membership.js';
import * as vendors from '../public/academy/vendors.js';
import {showcaseMarkup,createPersonalization} from '../public/academy/personalization.js';
import * as packagingPaths from '../public/academy/packaging-paths.js';
import * as sourceLibrary from '../public/academy/source-library.js';
import * as projectIdentity from '../public/academy/project-identity.js';
import * as researchPlans from '../public/academy/research-plans.js';
import * as exercises from '../public/academy/process-exercises.js';
import * as media from '../public/academy/learning-media.js';
import * as mentorNarration from '../public/academy/mentor-guide.js';
import * as coursePlaces from '../public/academy/course-places.js';
import * as demonstration from '../public/academy/demo-controller.js';
import * as relatedSkills from '../public/academy/related-skills.js';
import * as workshopModel from '../public/academy/workshop-model.js';
import * as labs from '../public/academy/engineering-labs.js';
import * as locale from '../public/academy/locale.js';
import * as paywall from '../public/academy/paywall.js';
import * as pricing from '../public/academy/pricing.js';
import * as cloudSync from '../public/academy/cloud-sync.js';
import { fileURLToPath, pathToFileURL } from 'node:url';

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../public/academy');
const data=Object.fromEntries(['catalog','featured','sources','photos'].map(k=>[k,JSON.parse(fs.readFileSync(path.join(root,'data',`${k}.json`),'utf8'))]));
data.release=JSON.parse(fs.readFileSync(path.join(root,'data','release.json'),'utf8'));
data.coursePlaces=JSON.parse(fs.readFileSync(path.join(root,'data','course-places.json'),'utf8'));
data.relatedSkills=JSON.parse(fs.readFileSync(path.join(root,'data','related-skills.json'),'utf8'));
data.media=JSON.parse(fs.readFileSync(path.join(root,'data','media.json'),'utf8'));
data.vendors=JSON.parse(fs.readFileSync(path.join(root,'data','vendors.json'),'utf8'));
const guidedById=new Map(data.featured.map(c=>[c.id,c]));data.catalog=data.catalog.map(c=>guidedById.get(c.id)||c);
assert.equal(data.catalog.length,data.release.topics);
const originalCourseIds=['semiconductor','sub2nm','asml','idf','apache','submarine','danjiang','hsuehshan','cybersecurity','packaging','silicon-photonics','steam-locomotive','ferrari','tesla','starlink','three-gorges','metro'];
assert.equal(data.featured.length,data.release.guidedCourses,'release counts match complete guided data');
for(const id of originalCourseIds)assert(data.featured.some(c=>c.id===id),`original requested course ${id} must remain`);
assert.equal(data.featured.reduce((count,c)=>count+c.stages.flatMap(s=>s.steps).length,0),data.release.allSteps,'release step count matches curricula');
for(const c of data.featured.filter(c=>!originalCourseIds.includes(c.id)))assert(((c.educationEdition>=11&&c.stepCount===c.stages.flatMap(s=>s.steps).length)||(c.enrichmentVersion>=12&&c.stepCount===c.stages.flatMap(s=>s.steps).length)||[12,24].includes(c.stages.flatMap(s=>s.steps).length)||(c.id==='a106'&&c.enrichmentVersion===9&&c.stages.flatMap(s=>s.steps).length===36)||(['a203','a211'].includes(c.id)&&c.enrichmentVersion===10&&c.stages.flatMap(s=>s.steps).length===({a203:36,a211:48}[c.id]))),`${c.id}: added course step count`);
for(const k of ['catalog','featured','sources','photos'])assert.equal(new Set(data[k].map(x=>x.id)).size,data[k].length,`${k}: duplicate IDs`);
assert.equal(projectIdentity.projectIdentityDomains.length,20,'twenty dedicated discipline motifs');
assert(projectIdentity.projectIdentitySubjectIds.length>=49,'original authored course silhouettes remain available');
const subjectGeometry=projectIdentity.projectIdentitySubjectIds.map(id=>{const c=data.catalog.find(c=>c.id===id);assert(c,'subject belongs to catalog '+id);const icon=projectIdentity.projectIconSvg(c);assert(icon.includes('data-subject-art="'+id+'"'),'emblem uses course-specific subject '+id);assert(projectIdentity.projectIdentitySvg(c).includes('data-subject-art="'+id+'"'),'image uses course-specific subject '+id);return icon.match(/<g transform="translate\(20 18\) scale\(\.75\)"[^>]*>([\s\S]*?)<\/g>/)?.[1]||icon.match(/<g data-geometry="[^"]+">([\s\S]*?)<\/g>/)?.[1]||icon.match(/<g transform="translate\(12 12\)"[^>]*data-icon-geometry="[^"]+"[^>]*>([\s\S]*?)<\/g><text/)?.[1]||(icon.includes('data-original="true"')?icon.replace(/<text\b[^>]*>[\s\S]*?<\/text>/g,'').replace(/<svg[^>]*>|<\/svg>/g,''):null);});
assert(subjectGeometry.every(Boolean),'subject geometry can be inspected');assert(new Set(subjectGeometry).size>=40,'subject geometry retains broad engineering diversity; related semiconductor processes may share a physical family');
for(const c of data.featured)assert(projectIdentity.projectIdentitySvg(c).includes('<svg'),'guided course renders identity '+c.id);

assert.equal(new Set(projectIdentity.projectIdentityDomains.map(category=>projectIdentity.domainIdentitySvg(category))).size,20,'twenty distinct discipline illustrations');
assert.equal(new Set(projectIdentity.projectIdentityDomains.map(category=>projectIdentity.domainIconSvg(category).replace(/aria-label="[^"]+"/,''))).size,20,'discipline geometry is distinct');
for(const factory of [projectIdentity.projectIdentitySvg,projectIdentity.projectIconSvg]){
  const identities=data.catalog.map(c=>factory(c));
  assert.equal(new Set(identities).size,data.catalog.length,'every catalog project has a distinct identity');
  for(let i=0;i<data.catalog.length;i++)assert.equal(identities[i],factory(data.catalog[i]),'identity is stable across renders');
  assert(!factory({id:'<img src=x>',title:'<script>alert(1)</script>',category:'structures'}).includes('<script>'),'identity escapes user-facing labels');
}
const sourceIds=new Set(data.sources.map(s=>s.id));
for(const c of data.catalog){
  for(const id of c.sourceIds||[])assert(sourceIds.has(id),`${c.id}: unknown source ${id}`);
  assert(c.title&&c.titleEn&&c.summary&&c.summaryEn,`${c.id}: missing bilingual metadata`);
}
for(const c of data.featured){
  assert(data.catalog.find(x=>x.id===c.id)?.stages,`${c.id}: guided course absent from catalog`);
  const steps=c.stages.flatMap(s=>s.steps);
  assert.equal(new Set(steps.map(s=>s.id)).size,steps.length,`${c.id}: duplicate step ID`);
  for(const s of steps){assert(s.objective&&s.objectiveEn&&s.check&&s.checkEn,`${s.id}: missing bilingual lesson`);assert(s.quiz.options[s.quiz.answer]&&s.quiz.optionsEn[s.quiz.answer],`${s.id}: invalid quiz answer`);}
}
for(const p of data.photos){assert(fs.existsSync(path.resolve(root,p.path)),`missing photo ${p.path}`);for(const id of p.courseIds||[])assert(data.featured.some(c=>c.id===id),`photo ${p.id}: invalid course ${id}`);}

let elements=[],ids=new Map(),activeElement=null,lastScrollTarget='',clock=1000,timerId=0;
const timers=new Map();
class TestDate extends Date {static now(){return clock;}}
const schedule=(callback,delay=0)=>{const id=++timerId;timers.set(id,{callback,at:clock+delay});return id;};
function advanceClock(amount){const target=clock+amount;let iterations=0;while(true){const next=[...timers].filter(([,timer])=>timer.at<=target).sort((a,b)=>a[1].at-b[1].at)[0];if(!next)break;assert(++iterations<20000,'fake scheduler must settle');clock=next[1].at;timers.delete(next[0]);next[1].callback();}clock=target;}
const fixed=new Map();
function element(id=''){
  const attrs=new Map(); const e={id,dataset:{},style:{},value:'',disabled:false,textContent:'',setAttribute(k,v){attrs.set(k,String(v));},getAttribute(k){return attrs.get(k)||null},getBoundingClientRect(){return{width:400,height:240}},setPointerCapture(){},classList:{add(){},remove(){},toggle(){}},focus(){activeElement=this;},scrollIntoView(){lastScrollTarget=this.id;},showModal(){this.open=true},close(){this.open=false},checkValidity(){return this.value.includes('@')},addEventListener(){},removeEventListener(){},setSelectionRange(start,end){this.selectionStart=start;this.selectionEnd=end;}};
  e.querySelector=selector=>select(selector);e.querySelectorAll=selector=>selectAll(selector);e.replaceChildren=()=>{e.innerHTML='';};let html='';Object.defineProperty(e,'innerHTML',{get:()=>html,set:v=>{html=v;if(id==='main')mount(v);else if(e.id==='atlasContent')mount(v,'atlasContent');else if(e.id==='dialogBody')mount(v,'dialog');}});return e;
}
for(const id of ['main','toast','pageTitle','accountName','language','dialog','dialogTitle','dialogBody','preferencesButton','preferencesDialog'])fixed.set(id,element(id));
function mount(html,group='main'){
  // Main and dialog are independent siblings; atlas is a child of main.
  const replaced=el=>el.mountGroup===group||(group==='main'&&el.mountGroup==='atlasContent');
  for(const el of elements.filter(replaced))if(el.id&&ids.get(el.id)===el)ids.delete(el.id);
  elements=elements.filter(el=>!replaced(el));
  const atlasStart=html.indexOf('id="atlasContent"');
  for(const match of html.matchAll(/<([a-z][\w-]*)\b([^>]*)>/gi)){
    const el=element();el.tagName=match[1].toUpperCase();el.mountGroup=group==='atlasContent'||(atlasStart>=0&&match.index>atlasStart)?'atlasContent':group;
    for(const a of match[2].matchAll(/([\w:-]+)(?:=(?:"([^"]*)"|'([^']*)'|([^\s>]+)))?/g)){
      const name=a[1],value=a[2]??a[3]??a[4]??'';
      if(name==='id'){el.id=value;ids.set(value,el);}else if(name==='disabled')el.disabled=true;else if(name==='value')el.value=value;else if(name.startsWith('data-'))el.dataset[name.slice(5).replace(/-([a-z])/g,(_,c)=>c.toUpperCase())]=value;
    }
    elements.push(el);
  }
  for(const m of html.matchAll(/<textarea\b(?=[^>]*\sid="([^"]+)")[^>]*>([\s\S]*?)<\/textarea>/g))if(ids.has(m[1]))ids.get(m[1]).value=m[2];
}
const select=s=>s.startsWith('#')?(ids.get(s.slice(1))||fixed.get(s.slice(1))||null):null;
const selectAll=s=>{const m=s.match(/^\[data-([\w-]+)\]$/);if(!m)return[];const key=m[1].replace(/-([a-z])/g,(_,c)=>c.toUpperCase());return elements.filter(e=>key in e.dataset);};
const storage=new Map();
const context=vm.createContext({console,Date:TestDate,JSON,Set,URL,Blob,AbortController,NodeFilter:{SHOW_TEXT:4},setTimeout:schedule,clearTimeout:id=>timers.delete(id),setInterval:()=>1,clearInterval(){},...labResources,...computingPaths,...opticsPaths,...structuresPaths,...projectIcons,...learningMap,...quantumLab,...electronicsPaths,...paywall,...pricing,...cloudSync,...membership,...vendors,showcaseMarkup,bindMembership:()=>{},bindVendors:()=>{},bindShowcase:()=>{},createPersonalization:options=>createPersonalization({...options,document:context.document,environment:{localStorage:context.localStorage}}),...sourceLibrary,...packagingPaths,...projectIdentity,...researchPlans,...workshopModel,...locale,...labs,...exercises,...media,...demonstration,...relatedSkills,...mentorNarration,...coursePlaces,bindCoursePlaces:()=>Promise.resolve(),navigator:{languages:['en'],language:'en'},location:{hash:'#workshop'},window:{scrollTo(){}},document:{querySelector:select,querySelectorAll:selectAll,addEventListener(){},removeEventListener(){},getElementById:id=>select('#'+id),documentElement:{dataset:{}},get activeElement(){return activeElement;}},localStorage:{getItem:k=>storage.get(k)||null,setItem:(k,v)=>storage.set(k,v)},fetch:async()=>{throw Error('Unexpected network request');},DATA:data});
const appSource=fs.readFileSync(path.join(root,'app.js'),'utf8');
// Supply actual new dependencies and fail early for an unrecognized export.
// Existing DOM adapter overrides remain intentional fixture implementations.
for(const match of appSource.matchAll(/^import\s*\{([^}]+)\}\s*from\s*['"]([^'"]+)['"];?$/gm)){
  const actual=await import(new URL(match[2],pathToFileURL(path.join(root,'app.js'))));
  for(const item of match[1].split(',')){const [original,binding=original]=item.trim().split(/\s+as\s+/);if(!(binding in context))context[binding]=actual[original];assert.notEqual(context[binding],undefined,'VM fixture supplies '+binding);}
}
const script=appSource.replace(/^import .*?;\n/gm,'');
assert(!/您提供的課程教材|Your course materials|data-show-materials|photos','materials/.test(script),'app no longer renders or loads user materials');
const cutoff=script.indexOf("$('#preferencesButton').onclick");assert(cutoff>0,'startup boundary not found');
vm.runInContext(script.slice(0,cutoff),context,{filename:'app.js'});
vm.runInContext('({catalog,featured,sources,photos}=DATA)',context);
// This suite exercises the fully loaded canonical release. Cold boot,
// network/file loading and route races live in the dedicated lazy/offline tests.
data.courseResources=new Map();
const mediaById=new Map(data.media.courses.map(c=>[c.courseId,c])),relatedById=new Map(data.relatedSkills.courses.map(c=>[c.courseId,c])),placesById=new Map(data.coursePlaces.courses.map(c=>[c.courseId,c])),associations=new Map(data.vendors.courses.map(c=>[c.courseId,c])),vendorsById=new Map(data.vendors.vendors.map(v=>[v.id,v]));
for(const c of data.catalog){const association=associations.get(c.id);data.courseResources.set(c.id,{sources:[],media:{courses:[mediaById.get(c.id)].filter(Boolean)},related:{courses:[relatedById.get(c.id)].filter(Boolean)},places:{courses:[placesById.get(c.id)].filter(Boolean)},vendors:{courses:[association].filter(Boolean),vendors:(association?.vendorIds||[]).map(id=>vendorsById.get(id)).filter(Boolean)}});}
vm.runInContext('setLearningMedia(DATA.media);setVendors(DATA.vendors);setRelatedSkills(DATA.relatedSkills,catalog);setAtlasPlaces(DATA.coursePlaces);for(const [id,value]of DATA.courseResources)courseResourceCache.set(id,value);coreReady=true;accountReady=true;accountReadyPromise=Promise.resolve();sourcesReady=true;',context);
assert.equal(vm.runInContext('courseResourceCache.size',context),data.catalog.length);
assert.equal(vm.runInContext("routeDataGate('workshop',[],location.hash.slice(1))",context),false,'fully loaded workshop passes the real route gate');
vm.runInContext('setLearningMedia(DATA.media);setVendors(DATA.vendors);setRelatedSkills(DATA.relatedSkills,catalog);setCoursePlaces(DATA.coursePlaces)',context);
const run=s=>vm.runInContext(s,context);
async function finishDemo(){if(run('mentorDemo.status')==='complete'&&run('demonstrationReady()'))return;if(!['waiting','speaking','paused'].includes(run('mentorGuide.status')))await run('mentorGuide.begin({voice:false})');let segments=0;while(run('mentorGuide.status')!=='complete'){assert(++segments<180,'narrated procedure must finish');run('mentorGuide.next()');advanceClock(600)}assert.equal(run('mentorDemo.status'),'complete');assert.equal(run('demonstrationReady()'),true);}
function clean(html,label){assertRenderedData(html,label);}
let projectRenders=0,stepRenders=0,maxTutorContextChars=0;
const taskModes=new Set();
for(const language of ['zh-TW','en']){
  console.error(`[frontend] ${language}: ${data.catalog.length} projects / ${data.release.allSteps} steps`);
  run(`lang=${JSON.stringify(language)};projects={};`);
  for(const c of data.catalog){
    const html=run(`renderProject(${JSON.stringify(c.id)})`);clean(html,`${language}/${c.id}`);projectRenders++;
    assert(html.includes('data-project-icon="'+c.id+'"'),'project brief includes its dedicated emblem');
    assert(html.includes('data-media-kind="'),'project brief includes a labelled photo or original illustration');
    if(c.stages){const courseSteps=c.stages.flatMap(stage=>stage.steps),visibleIds=[...html.matchAll(/data-curriculum-step="([^"]+)"/g)].map(match=>match[1]);assert.deepEqual(visibleIds,courseSteps.map(step=>step.id),'overview exposes every step once, in order');}
  }
  // Render every step as an entitled learner; the paywall itself is checked below.
  paywall.configurePaywall({config:{paywall:{enabled:false}}});
  for(const c of data.featured){
    const steps=c.stages.flatMap(s=>s.steps);
    for(let i=0;i<steps.length;i++){
      const prior=steps.slice(0,i).map(s=>s.id);
      run(`activeId=${JSON.stringify(c.id)};activeStep=${i};projects[activeId]={completed:${JSON.stringify(prior)},assembly:${JSON.stringify(prior)},notes:'',updatedAt:1};`);
      clean(run('renderWorkshop()'),`${language}/${c.id}/${i}`);assert.equal(run('activeStep'),i);stepRenders++;
      const serializedContext=run('JSON.stringify(tutorContext(course(),allSteps(course())[activeStep]))');
      maxTutorContextChars=Math.max(maxTutorContextChars,serializedContext.length);
      assert(serializedContext.length<=18000,`${language}/${c.id}/${i}: tutor context exceeds API limit`);
      const lessonContext=JSON.parse(serializedContext);
      const expectedRelated=relatedSkills.relatedForCourse(c);
      assert.equal(lessonContext.relatedLearning.length,expectedRelated.curated?Math.min(3,expectedRelated.related.length):0,`${language}/${c.id}/${i}: tutor includes curated comparisons`);
      for(const item of lessonContext.relatedLearning)for(const field of ['title','transfer','difference'])assert(typeof item[field]==='string'&&item[field].length>0&&item[field].length<=500,`${language}/${c.id}/${i}: bounded bilingual comparison ${field}`);
      assert(lessonContext.exercise?.instruction&&lessonContext.exercise?.object,`${language}/${c.id}/${i}: tutor sees the interactive task`);
      taskModes.add(lessonContext.exercise.mode);
      const expectedSourceIds=(steps[i].sourceIds?.length?steps[i].sourceIds:c.sourceIds||[]).filter(id=>sourceIds.has(id)).slice(0,8);
      assert.deepEqual(lessonContext.sources.map(source=>source.id),expectedSourceIds,`${language}/${c.id}/${i}: context must use the step sources`);
      for(const source of lessonContext.sources)assert.deepEqual(Object.keys(source).sort(),['id','scope','title','url'],'tutor sends only compact source metadata');
      for(const field of ['instruction','observation','failure'])assert.equal(lessonContext[field],run(`txt(allSteps(course())[activeStep],${JSON.stringify(field)})`),`${language}/${c.id}/${i}: detailed lesson context ${field}`);
    }
  }
  for(const fn of ['renderHome','renderCatalog','renderProgress','renderMap'])clean(run(`${fn}()`),`${language}/${fn}`);
  for(const tab of ['official','photos']){run(`sourceTab=${JSON.stringify(tab)}`);clean(run('renderSources()'),`${language}/sources/${tab}`);}
  console.error(`[frontend] ${language}: complete (${projectRenders} projects / ${stepRenders} steps cumulative)`);
}

console.error('[frontend] checking catalogue, atlas and every guided-course entry');
// The former home/catalog routes share one explorer with live coverage and filters.
run("lang='en';location.hash='#home';render()");
assert.equal((fixed.get('main').innerHTML.match(/id="search"/g)||[]).length,1,'one merged search');assert.equal(run('renderHome()'),run('renderCatalog()'),'home/catalog share explorer');assert(!run('renderSources()').includes('Your course materials'),'removed materials section');
const checkpointRoadmap=data.catalog.find(c=>!c.stages);const roadmapHtml=run('renderProject('+JSON.stringify(checkpointRoadmap.id)+')');assert.equal((roadmapHtml.match(/data-research-evidence=/g)||[]).length,8,'roadmap renders eight research checkpoints');assert(roadmapHtml.includes('id="researchNotes"'),'research worksheet preserves the existing project notebook');
assert.equal(run('domainCounts().length'),20,'all twenty disciplines are represented');
assert.equal((fixed.get('main').innerHTML.match(/data-domain-identity=/g)||[]).length,20,'each domain has an illustration as well as an icon');
select('#search').value='semiconductor';select('#search').selectionStart=13;select('#search').oninput();assert(run('filteredCatalog().length')<data.catalog.length,'home search is bound');
select('#categoryFilter').onchange({target:{value:'structures'}});assert(run('filteredCatalog().every(c=>c.category==="structures")'),'home domain filter is bound');
run("location.hash='#home';lastCatalogRoute='';render()");assert.equal(run('filteredCatalog().length'),data.catalog.length,'legacy home route resets to complete explorer');

assert(fixed.get('main').innerHTML.includes(`All ${data.featured.length} guided courses`),'home count matches live data');
const csv=run('catalogCsv()');assert(csv.startsWith('\uFEFF'),'CSV preserves bilingual UTF-8 spreadsheet text');assert.equal(csv.split('\r\n').length,data.catalog.length+1,'CSV includes the header and every catalog entry');for(const c of data.featured)assert(csv.includes('"'+c.id+'"'),'CSV includes guided course '+c.id);
run("location.hash='#catalog/all';render()");assert.equal(run('filteredCatalog().length'),data.catalog.length);
select('#catalogPage').value=String(Math.ceil(data.catalog.length/24));select('#catalogPageForm').onsubmit({preventDefault(){}});assert.equal(run('pageIndex'),Math.ceil(data.catalog.length/24)-1,'page jump reaches the final catalog page');assert(fixed.get('main').innerHTML.includes('#project/'+data.catalog.at(-1).id),'last catalog topic is reachable');
run("location.hash='#catalog/ready';render()");assert.equal(run('filteredCatalog().length'),data.featured.length,'guided filter uses hydrated curricula');
const discoverableGuided=[];
for(let page=0;page<Math.ceil(data.featured.length/24);page++){run(`pageIndex=${page};render()`);discoverableGuided.push(...[...fixed.get('main').innerHTML.matchAll(/data-guided-course="([^"]+)"/g)].map(match=>match[1]));}
assert.equal(discoverableGuided.length,data.featured.length,'guided pagination includes every course once');assert.deepEqual(new Set(discoverableGuided),new Set(data.featured.map(c=>c.id)),'new guided courses are not omitted');
select('#categoryFilter').onchange({target:{value:'space'}});assert(run('filteredCatalog().every(c=>c.category==="space"&&c.stages)'),'combined domain and guided filters are respected');
run("location.hash='#catalog/all';render()");assert.equal(run('filteredCatalog().length'),data.catalog.length,'All link clears prior filters');
const targetCourse=data.featured.at(-1);select('#search').value=targetCourse.titleEn;select('#search').selectionStart=targetCourse.titleEn.length;select('#search').oninput();assert(run('filteredCatalog().length')<data.catalog.length,'search actually narrows the full catalog');assert(run('filteredCatalog().some(c=>c.id==='+JSON.stringify(targetCourse.id)+')'),'new course can be found by its English title');selectAll('[data-catalog-route]').find(link=>link.dataset.catalogRoute==='all').onclick();assert.equal(run('filteredCatalog().length'),data.catalog.length,'All link resets search even when its hash does not change');
run("location.hash='#catalog/domain/packaging';render()");
assert.equal(run('filteredCatalog().length'),100,'packaging collection reaches all 100 topics');
assert(run('filteredCatalog().every(c=>c.stages)'),'all 100 packaging topics are guided');
assert.equal(packagingPaths.PACKAGING_PATHS.length,8);
for(const path of packagingPaths.PACKAGING_PATHS)for(const id of path.courses)assert(guidedById.has(id),'learning route links to guided course '+id);
assert(fixed.get('main').innerHTML.includes('100 guided courses'),'collection shows actual coverage');
const packagingSub=data.featured.find(c=>c.category==='packaging').subcategory;
select('#catalogSubdiscipline').onchange({target:{value:packagingSub}});
assert(run('filteredCatalog().length')>0&&run('filteredCatalog().length')<100,'subcategory control narrows the collection');
assert(run('filteredCatalog().every(c=>courseSubcategory(c).id==='+JSON.stringify(packagingSub)+')'),'subcategory results match selected discipline');
select('#categoryFilter').onchange({target:{value:'semiconductor'}});assert.equal(run('subdiscipline'),'','switching domain clears incompatible subdiscipline');
run("location.hash='#catalog/all';render()");assert.equal(run('filteredCatalog().length'),data.catalog.length,'All route clears the collection filter');
run("atlasQuery='';location.hash='#map';render()");assert.equal(selectAll('[data-place]').length,data.coursePlaces.courses.length,'atlas lists every sourced course location');assert.equal(new Set(selectAll('[data-place]').map(b=>b.dataset.place)).size,data.coursePlaces.courses.length,'atlas has no duplicate course entries');
const lastPlace=data.coursePlaces.courses.at(-1);select('#atlasQuery').oninput({target:{value:lastPlace.place.nameEn}});assert(run('filteredAtlas().some(e=>e.courseId==='+JSON.stringify(lastPlace.courseId)+')'),'atlas search covers all course place names');assert.equal(run('atlasQuery'),lastPlace.place.nameEn,'atlas updates keep the search input state');
assert(run("iconSvg('suspension').includes('data-load-path=\"main-cable\"')&&iconSvg('suspension').includes('data-load-path=\"hanger\"')"),'suspension art has a main cable and vertical hangers');assert(run("iconSvg('water-treatment').includes('REVERSE OSMOSIS')&&!iconSvg('water-treatment').includes('data-load-path')"),'water treatment has process units, not bridge art');

// Local-only worksheet evidence remains discoverable without manufacturing completion or cloud claims.
const actualResearchProgressFor=context.researchProgressFor;const researchRequests=[];
context.researchProgressFor=profileId=>{researchRequests.push(profileId);return profileId==='research-profile'?[{courseId:checkpointRoadmap.id,done:3,total:8,updatedAt:'2026-10-13T12:00:00.000Z'},{courseId:'missing-catalog-id',done:1,total:8,updatedAt:'2026-10-13T12:00:00.000Z'}]:[];};
run("user={id:'research-profile',name:'Research apprentice'};projects={};lang='en'");const worksheetProgress=run('renderProgress()');
assert(worksheetProgress.includes('Research worksheets on this device'),'local worksheet section has explicit storage scope');assert(worksheetProgress.includes('data-research-course="'+checkpointRoadmap.id+'"'),'worksheet-only save links to its project');assert(worksheetProgress.includes('3 / 8'),'worksheet counts show research checkpoints');assert(worksheetProgress.includes('2026-10-13T12:00:00.000Z'),'worksheet has last-updated time');assert(!worksheetProgress.includes('missing-catalog-id'),'unknown catalog records are excluded');assert(!worksheetProgress.includes('class="empty mt"'),'existing worksheets suppress the empty-project card');assert.equal(run('Object.keys(projects).length'),0,'local worksheets never create cloud or guided-progress records');assert.equal(run('percent('+JSON.stringify(checkpointRoadmap.id)+')'),0,'research checkpoints never inflate course completion');
run("user={id:'other-research-profile',name:'Other apprentice'}");assert(!run('renderProgress()').includes('data-local-research'),'another profile cannot see the local worksheet');assert.equal(researchRequests.at(-1),'other-research-profile','lookup uses the active account ID');run("user=null");run('renderProgress()');assert.equal(researchRequests.at(-1),'guest','guest storage uses a separate stable profile');context.researchProgressFor=actualResearchProgressFor;

// Every original and added course opens independently; stale long-course filters cannot hide it.
for(const c of data.featured){
  run("navStage=19;navQuery='previous-course-only';location.hash="+JSON.stringify('#project/'+c.id)+";render()");
  await select('#beginCourse').onclick();assert.equal(run('activeId'),c.id,'begin selects '+c.id);assert.equal(run("localStorage.getItem('mg-active')"),c.id,'active course survives reload');assert.equal(run('navStage'),-1);assert.equal(run('navQuery'),'');run("location.hash='#workshop';render()");assert(selectAll('[data-step]').length>0,'new course navigator is populated: '+c.id);assert.equal(run('course().id'),c.id);
}

console.error(`[frontend] ${data.featured.length} course entries passed; checking controls and persistence`);
// Exercise actual handlers across three consecutive steps. No quiz or placement gate is bypassed.
run("lang='en';projects={};quizPass.clear();activeId=featured[0].id;activeStep=0;location.hash='#workshop';currentPage='workshop';render();");
assert.equal(select('#complete').dataset.ready,'false','initial completion gate remains closed');assert(!select('#complete').disabled,'next-action button remains usable');
assert.equal(await run('completeStep()'),false,'direct completion without evidence rejected');
assert.equal(run('confirmAssembly()'),false,'misaligned placement rejected');
const beforeDemonstration=run('JSON.stringify(poseContext().state.pose)');
run("handleWorkshopKey({type:'keydown',code:'ArrowRight',key:'ArrowRight',target:{tagName:'DIV'},preventDefault(){}})");
assert.equal(run('JSON.stringify(poseContext().state.pose)'),beforeDemonstration,'teacher demonstration never moves the learner');
assert(select('#poseFeedback').textContent.includes('demonstration'),'keys received during demo explain the prerequisite');
assert(fixed.get('main').innerHTML.indexOf('id="workbenchControls"')<fixed.get('main').innerHTML.indexOf('id="exerciseTask"'),'physical controls precede task and lesson text');
assert(fixed.get('main').innerHTML.indexOf('id="assist"')<fixed.get('main').innerHTML.indexOf('id="learnerModel"'),'large assistance precedes the apprentice model');assert(fixed.get('main').innerHTML.indexOf('data-workshop-context="relatedSkillsRegion"')<fixed.get('main').innerHTML.indexOf('id="assemblySection"'),'related-learning shortcut is visible before the workbenches');assert(fixed.get('main').innerHTML.indexOf('id="relatedSkillsRegion"')>fixed.get('main').innerHTML.indexOf('id="workbenchControls"'),'full related context follows practical controls');assert.equal((fixed.get('main').innerHTML.match(/id="complete"/g)||[]).length,1,'one primary next control');
assert.equal(run('mentorGuide.status'),'idle','new narration waits for an explicit gesture');
assert.equal(select('#complete').onclick(),false,'primary next starts the required explanation without advancing');
assert.equal(run('mentorGuide.phase'),'lesson','complete demonstration begins with the full lesson');assert.equal(lastScrollTarget,'stepHeading','next preserves the narration pointer target instead of scrolling back to the mentor bench');select('#complete').onclick();assert.equal(lastScrollTarget,'lessonSection','next narration scrolls to the actual lesson target');assert(select('#nextRequirements').textContent.includes(select('#mentorGuideText').textContent.slice(0,30)),'fixed dock repeats the current narration while its panel is elsewhere');
assert.equal(select('#dockGuideControls').hidden,false,'guide controls stay in the fixed dock');select('#dockPauseGuide').onclick();assert.equal(run('mentorGuide.status'),'paused','dock can pause narration');select('#dockPauseGuide').onclick();assert.equal(run('mentorGuide.status'),'waiting','dock resumes text narration');select('#dockSkipTour').onclick();assert.equal(select('#dockSkipTour').hidden,true,'skip hides once the tour is skipped');assert.equal(run('demonstrationReady()'),false,'skipping keyboard tour never passes the demonstration gate');
let beforeDemo=0;while(run('mentorGuide.phase')!=='demo'){assert(++beforeDemo<80);run('mentorGuide.next()');advanceClock(600);assert.notEqual(run('mentorGuide.phase'),'tour','skipped keyboard tour stays skipped');}
assert.equal(run('demonstrationReady()'),false,'even after all lesson narration, the real procedure still must be demonstrated');
await finishDemo();assert.equal(run('keyboardActive'),true,'newly selected step owns physical keyboard without another activate click');
const learnerBeforeReplay=run('JSON.stringify(poseContext().state.pose)');
select('#demoReplay').onclick();assert.equal(run('demonstrationReady()'),false,'replay gates new input until demonstration finishes');
run('mentorGuide.pause()');const pausedIndex=run('mentorGuide.index');
advanceClock(5000);assert.equal(run('mentorGuide.index'),pausedIndex,'paused narration is stable');
select('#demoNext').onclick();assert(run('mentorGuide.index')>pausedIndex,'manual next section advances paused text narration');
await finishDemo();
assert.equal(run('JSON.stringify(poseContext().state.pose)'),learnerBeforeReplay,'replaying the teacher never edits learner pose');
select('#notes').value='Draft before control rerenders';select('#notes').oninput();
select('#grab').onclick();
const origin=JSON.parse(run('JSON.stringify(poseContext().state.pose)'));
run("heldControls.add('x+');heldControls.add('z+');performMotion();stopMotion()");
const moved=JSON.parse(run('JSON.stringify(poseContext().state.pose)'));
assert(moved.x>origin.x&&moved.z>origin.z,'two axes move together');
assert(storage.get('mg-pose-v2-guest'),'pose stored by device/account');
select('#undo').onclick();
assert.equal(run('poseContext().state.pose.x'),origin.x,'undo restores previous pose');
select('#resetPose').onclick();assert.equal(run('poseContext().state.pose.grabbed'),false);
run("handleWorkshopKey({type:'keydown',key:' ',target:{tagName:'DIV'},preventDefault(){}})");
assert.equal(run('poseContext().state.pose.grabbed'),true,'Space grabs');
run("handleWorkshopKey({type:'keydown',key:'d',target:{tagName:'DIV'},preventDefault(){}});handleWorkshopKey({type:'keyup',key:'d',target:{tagName:'DIV'},preventDefault(){}})");
assert(run('poseContext().state.pose.x')>workshopModel.initialPose().x,'WASD handler moves piece');
// Precision is a modifier, not an existing motion: Shift-first must still take
// an undo snapshot before the first directional movement.
run('poseHistory.clear()');
const beforeShift=JSON.parse(run('JSON.stringify(poseContext().state.pose)'));
run("handleWorkshopKey({type:'keydown',key:'Shift',target:{tagName:'DIV'},preventDefault(){}});handleWorkshopKey({type:'keydown',key:'d',shiftKey:true,target:{tagName:'DIV'},preventDefault(){}});handleWorkshopKey({type:'keyup',key:'d',shiftKey:true,target:{tagName:'DIV'},preventDefault(){}});handleWorkshopKey({type:'keyup',key:'Shift',target:{tagName:'DIV'},preventDefault(){}})");
assert.equal(run('poseContext().state.pose.x'),beforeShift.x+1,'Shift movement uses the precision increment');
select('#undo').onclick();
assert.deepEqual(JSON.parse(run('JSON.stringify(poseContext().state.pose)')),beforeShift,'undo restores a Shift-first movement');
// Physical keyboard events, including IME/non-Latin key labels, operate only
// after a deliberate focus action. Inputs and dialogs retain normal behavior.
function keyEvent(type,code,extra={}){
  const event={type,code,key:code,target:{tagName:'DIV'},defaultPrevented:false,preventDefault(){this.defaultPrevented=true;},...extra};
  context.KEY_EVENT=event;run('handleWorkshopKey(KEY_EVENT)');return event;
}
run("deactivateWorkshopKeyboard();poseContext().state.pose={...initialPose(),grabbed:false,z:35}");
const inactiveX=run('poseContext().state.pose.x');
assert.equal(keyEvent('keydown','ArrowRight').defaultPrevented,true,'a non-editing workshop key automatically resumes control');
assert.equal(run('poseContext().state.pose.x'),inactiveX);
select('#activateKeyboard').onclick();
assert.equal(activeElement?.id,'learnerModel','activation button focuses the actual iframe workbench');
assert.equal(run('keyboardActive'),true);
keyEvent('keydown','ArrowRight');keyEvent('keyup','ArrowRight');
assert.equal(run('poseContext().state.pose.x'),inactiveX,'released object cannot move');
assert(select('#poseFeedback').textContent.includes('Grab'),'received arrow explains the grab requirement');
keyEvent('keydown','Space',{key:' '});assert.equal(run('poseContext().state.pose.grabbed'),true);
for(const [code,axis,delta] of [['ArrowRight','x',4],['ArrowLeft','x',-4],['ArrowUp','y',-4],['ArrowDown','y',4]]){
  const before=JSON.parse(run('JSON.stringify(poseContext().state.pose)'));
  assert(keyEvent('keydown',code).defaultPrevented,`${code} handled inside active workbench`);
  const after=JSON.parse(run('JSON.stringify(poseContext().state.pose)'));
  assert.equal(after[axis],before[axis]+delta,`${code} moves default XY axis`);
  assert.equal(after.z,before.z,`${code} does not change depth`);assert.equal(after.rotation,before.rotation,`${code} does not rotate`);
  keyEvent('keyup',code);
}
for(const [code,key,axis,delta] of [['KeyW','Process','y',-4],['KeyD','ㄎ','x',4],['KeyQ','Dead','rotation',-4],['KeyI','i','z',4],['PageDown','PageDown','z',-4],['KeyL','l','rotation',4]]){
  const before=run(`poseContext().state.pose.${axis}`);
  keyEvent('keydown',code,{key,isComposing:key==='Process'});keyEvent('keyup',code,{key:'Unidentified'});
  assert.equal(run(`poseContext().state.pose.${axis}`),before+delta,`${code} uses its physical position despite key label ${key}`);
}
assert.equal(keyEvent('keydown','Quote',{key:'Dead'}).defaultPrevented,false,'unmapped dead key remains untouched');
keyEvent('keydown','ArrowRight');const once=run('poseContext().state.pose.x');
keyEvent('keydown','ArrowRight',{repeat:true});assert.equal(run('poseContext().state.pose.x'),once,'OS autorepeat does not double the movement timer');
run('performMotion()');assert.equal(run('poseContext().state.pose.x'),once+4,'held key advances through the motion timer');
keyEvent('keydown','KeyD',{key:'d'});keyEvent('keyup','ArrowRight');
assert.equal(run("heldControls.has('x+')"),true,'releasing one alias retains the other physical key');
keyEvent('keyup','KeyD',{key:'d'});assert.equal(run("heldControls.has('x+')"),false);
keyEvent('keydown','ArrowLeft');keyEvent('keyup','ArrowLeft',{target:{tagName:'INPUT'}});
assert.equal(run('heldControls.size'),0,'keyup releases held motion even after focus entered an input');
for(const target of [{tagName:'INPUT'},{tagName:'TEXTAREA'},{tagName:'SELECT'},{tagName:'SPAN',isContentEditable:true},{tagName:'SPAN',closest:()=>({tagName:'DIV'})}]){
  const before=run('JSON.stringify(poseContext().state.pose)');
  assert.equal(keyEvent('keydown','ArrowUp',{target}).defaultPrevented,false,'editable controls keep their native keys');
  assert.equal(run('JSON.stringify(poseContext().state.pose)'),before);
}
fixed.get('dialog').open=true;const dialogPose=run('JSON.stringify(poseContext().state.pose)');
assert.equal(keyEvent('keydown','ArrowDown').defaultPrevented,false);assert.equal(run('JSON.stringify(poseContext().state.pose)'),dialogPose,'dialog excludes workshop keys');fixed.get('dialog').open=false;
keyEvent('keydown','ArrowUp');run('deactivateWorkshopKeyboard()');
assert.equal(run('heldControls.size'),0);assert.equal(run('motionTimer'),null);assert.equal(run('keyboardActive'),false,'blur pauses keyboard and all movement');
select('#activateKeyboard').onclick();keyEvent('keydown','Escape');assert.equal(run('keyboardActive'),false,'Escape exits keyboard control');
select('#activateKeyboard').onclick();assert(select('#keyboardStatus').textContent.includes('Keys received'),'visible diagnostic identifies received keys');
// Right Shift may have been pressed while an input owned focus. Its inferred
// modifier must not be recorded as a physical left Shift that never releases.
run('deactivateWorkshopKeyboard()');keyEvent('keydown','ShiftRight',{key:'Shift',target:{tagName:'INPUT'}});
select('#activateKeyboard').onclick();const beforeRightShift=run('poseContext().state.pose.x');
keyEvent('keydown','ArrowRight',{shiftKey:true});assert.equal(run('poseContext().state.pose.x'),beforeRightShift+1,'inferred right Shift enables precision');
keyEvent('keyup','ShiftRight',{key:'Shift',shiftKey:false});keyEvent('keyup','ArrowRight',{shiftKey:false});
assert.equal(run("heldControls.has('precision')"),false,'right Shift release clears an inferred modifier');
const afterRightShift=run('poseContext().state.pose.x');keyEvent('keydown','ArrowRight',{shiftKey:false});keyEvent('keyup','ArrowRight');
assert.equal(run('poseContext().state.pose.x'),afterRightShift+4,'movement returns to normal speed after inferred Shift release');
// Independent touch pointers can hold different axes and release separately.
const xyPad=selectAll('[data-motion]').find(button=>button.dataset.motion==='x+'),zPad=selectAll('[data-motion]').find(button=>button.dataset.motion==='z+');
xyPad.onpointerdown({pointerId:1,preventDefault(){}});zPad.onpointerdown({pointerId:2,preventDefault(){}});
assert(run("heldControls.has('x+')&&heldControls.has('z+')"),'two hands can move XY and Z simultaneously');
xyPad.onpointerup({pointerId:1,preventDefault(){}});assert.equal(run("heldControls.has('z+')"),true,'releasing one hand keeps the other held');
zPad.onpointercancel({pointerId:2});assert.equal(run('heldControls.size'),0);
// Pointer movement maps through the SVG coordinate system, including the
// horizontal letterbox and the inverse of the isometric XY projection.
const dragModel=select('#learnerModel');
dragModel.getBoundingClientRect=()=>({left:0,top:0,width:800,height:304});
run('poseContext().state.pose={...initialPose(),z:35}');
const beforeDrag=JSON.parse(run('JSON.stringify(poseContext().state.pose)'));
dragModel.onpointerdown({pointerId:7,clientX:500,clientY:150,target:{closest:()=>({id:'activePiece'})},preventDefault(){}});
dragModel.onpointermove({pointerId:7,clientX:520,clientY:158.6,preventDefault(){}});
assert(Math.abs(run('poseContext().state.pose.x')-(beforeDrag.x+11.6))<1e-8,'drag compensates for Y contribution to projected X');
assert(Math.abs(run('poseContext().state.pose.y')-(beforeDrag.y+20))<1e-8,'drag respects 400×304 viewBox and letterboxing');
dragModel.onpointerup();assert.equal(run('poseContext().state.pose.grabbed'),false,'pointer release drops the tool');
context.MATRIX_MODEL={querySelector:()=>({getScreenCTM:()=>({inverse:()=>({scale:2})}),createSVGPoint:()=>({x:0,y:0,matrixTransform(matrix){return{x:(this.x-100)/matrix.scale,y:(this.y-50)/matrix.scale};}})})};
assert.deepEqual(JSON.parse(run('JSON.stringify(workshopPointer({clientX:120,clientY:80},MATRIX_MODEL))')),{x:10,y:15},'native SVG inverse matrix takes precedence over bounding-box fallback');
const beforeReload=run('JSON.stringify(poseContext().state.pose)');
run("poseStore={};poseOwner='';");
assert.equal(run('JSON.stringify(poseContext().state.pose)'),beforeReload,'pose reload keeps course/step state');
run('render()');assert.equal(select('#notes').value,'Draft before control rerenders','notes survive rerender');
for(let i=0;i<3;i++){
  await finishDemo();
  assert.equal(run('activeStep'),i);
  assert.equal(select('#complete').dataset.ready,'false','each new step starts gated');
  assert.equal(run('goToStep(activeStep+1)'),false,'locked next step is not reachable');
  const correct=run('allSteps(course())[activeStep].quiz.answer');
  selectAll('[data-answer]')[correct].onclick();
  assert.equal(select('#complete').dataset.ready,'false','correct quiz alone does not unlock completion');
  select('#assist').onclick();
  const guidedDuration=run('assistanceDemo.duration');
  advanceClock(guidedDuration/2);select('#assistPause').onclick();
  const pausedGuidance=run('JSON.stringify(poseContext().state)');advanceClock(30000);
  assert.equal(run('JSON.stringify(poseContext().state)'),pausedGuidance,'paused assistance does not continue editing the learner');
  assert.equal(select('#complete').onclick(),false,'next action resumes guidance without completing the step');
  advanceClock(guidedDuration+100);
  assert.equal(run('progressFor(course().id).assembly.length'),i,'full guided operation still requires explicit evidence confirmation');
  assert.equal(run('poseContext().state.pose.grabbed'),false,'full guidance releases the learner tool');
  assert.equal(run('demonstrationState().practice.assisted'),true,'guided completion is explicitly recorded as assisted');
  assert.equal(run('practiceStatus().passed'),true,'full guidance completes the operation conditions');
  const spec=run('exerciseContext().spec');
  assert.equal(run('exerciseContext().result.passed'),true,`step ${i+1} task evidence passes its own evaluator`);
  if(i===0){const task=run('JSON.stringify(exerciseContext().exercise)');run("poseStore={};poseOwner=''");assert.equal(run('JSON.stringify(exerciseContext().exercise)'),task,'task controls persist through a device reload');run('render()');}
  assert.equal(select('#place').onclick(),true,'valid task evidence can be submitted');
  assert.equal(select('#complete').dataset.ready,'true','confirmed assembly plus check unlocks');
  const wrong=(correct+1)%selectAll('[data-answer]').length;
  selectAll('[data-answer]')[wrong].onclick();assert.equal(select('#complete').dataset.ready,'false','wrong answer recloses gate');
  selectAll('[data-answer]')[correct].onclick();select('#workflowAction').onclick();
  assert.equal(run('activeStep'),i+1,'completion advances exactly one step');
  assert.equal(run('progressFor(course().id).completed.length'),i+1);
}
assert.deepEqual(taskModes,new Set(['assembly','inspect','process','measure']),'curriculum renders four meaningful task modes');
assert.equal(run('demonstrationReady()'),false,'next step does not inherit the preceding step’s demo gate');
run('goToStep(0)');assert.equal(run('demonstrationReady()'),true,'a completed step remains available when revisited');
select('#demoReplay').onclick();assert.equal(run('gateState(course(),allSteps(course())[0]).ready'),true,'mentor replay never withdraws an earned completion');
run('goToStep(3)');assert.equal(run('demonstrationReady()'),false,'returning to an unseen step still requires its own demonstration');
await run('mentorGuide.startTour({voice:false})');let tourSegments=0;while(run('mentorGuide.status')!=='complete'){assert(++tourSegments<100);run('mentorGuide.next()');advanceClock(600)}assert.equal(run('demonstrationReady()'),false,'standalone controls review never unlocks an unseen step');

// Previously completed V2 steps remain complete even without V3 task state or
// a separate assembly entry; an update never withdraws earned progress.
run('projects[activeId].assembly=[];activeStep=0;render()');
assert.equal(run('gateState(course(),allSteps(course())[0]).ready'),true,'old completed progress remains unlocked');
assert.equal(run('progressFor(activeId).completed.length'),3,'V3 does not replace old completion records');
assert(select('#place').disabled,'old completed task remains submitted');
// Exercise a real measurement step through its input and decision controls.
const measurementIndex=run("allSteps(course()).findIndex(s=>resolveExercise(course(),s).mode==='measure')");
run(`activeStep=${measurementIndex};projects[activeId]={completed:allSteps(course()).slice(0,activeStep).map(s=>s.id),assembly:allSteps(course()).slice(0,activeStep).map(s=>s.id),notes:'Measurement notebook',updatedAt:1};render()`);
await finishDemo();const originalMeasurementAnswer=run('poseContext().state.answer');const beforeGuidedMeasurement=run('JSON.stringify({pose:poseContext().state.pose,exercise:exerciseContext().exercise,practice:demonstrationState().practice})');select('#assist').onclick();advanceClock(run('assistanceDemo.duration')+100);select('#undo').onclick();assert.equal(run('JSON.stringify({pose:poseContext().state.pose,exercise:exerciseContext().exercise,practice:demonstrationState().practice})'),beforeGuidedMeasurement,'undo restores pose, task values and practice before guidance');select('#assist').onclick();advanceClock(run('assistanceDemo.duration')+100);
assert.equal(run('poseContext().state.answer'),originalMeasurementAnswer,'full assistance never changes a quiz answer');assert.equal(run('gateState(course(),allSteps(course())[activeStep]).checked'),false,'guidance does not mark the knowledge check passed');const measurementSpec=run('exerciseContext().spec');assert.equal(measurementSpec.mode,'measure');
run('demonstrationState().practice.controls=[];updatePoseFeedback()');assert.equal(select('#place').onclick(),false,'unrecorded sample cannot be submitted');
if(measurementSpec.choices.length)selectAll('[data-exercise-choice]').find(button=>button.dataset.exerciseChoice===measurementSpec.expectedChoice).onclick();
for(const control of measurementSpec.controls){const input=select('#exercise-'+control.id);input.value=String(control.target);input.oninput();assert(select('#exercise-value-'+control.id).textContent.includes(String(control.target)),'measurement readout follows the entered value');}
run('demonstrationState().practice.controls=[];updatePoseFeedback()');
assert.equal(run('exerciseContext().result.passed'),true,'restored readings can already be numerically correct');
assert.equal(select('#place').onclick(),false,'restored correct readings still need an explicit record action');
assert(select('#exerciseReadout').textContent.includes('Record current'),'feedback identifies the missing recording action');
select('#confirmReadings').onclick();
assert.equal(select('#place').onclick(),true,'correct measured values and classification submit evidence');
assert.equal(select('#complete').dataset.ready,'false','measurement evidence still requires its separate knowledge check');
// Standalone physics affordances are schematic, bounded, and deterministic.
let pose={...workshopModel.initialPose(),grabbed:true,x:-74,y:0,z:0};
const blocked=workshopModel.advancePose(pose,{x:3},false,{fixture:true});assert(blocked.blocked,'fixture blocks low movement');
const lifted=workshopModel.advancePose({...pose,z:35},{x:3},false,{fixture:true});assert(!lifted.blocked,'lifting clears fixture');
assert(workshopModel.alignment(workshopModel.targetFor({id:'x'}),workshopModel.targetFor({id:'x'})).aligned);
const fast=workshopModel.advancePose({...pose,z:35},{x:1});const precise=workshopModel.advancePose({...pose,z:35},{x:1},true);assert(fast.pose.x-pose.x>precise.pose.x-pose.x,'precision reduces increment');
// New curricula must not inherit old numbered gates. Keep notes and a downloadable legacy snapshot.
run("projects[activeId]={completed:['old-step-001'],assembly:['old-step-001'],notes:'Legacy notebook',updatedAt:1};render();");
assert.equal(run('progressFor(activeId).completed.length'),0);
assert(storage.get('mg-legacy-progress-v2-guest').includes('old-step-001'));
assert.equal(run('progressFor(activeId).notes'),'Legacy notebook');
assert(select('#exportLegacy'),'migration notice provides export');
assert(!fixed.get('main').innerHTML.includes('data-step="519"'),'navigator does not render all 520 controls');
assert(selectAll('[data-step]').length<=40,'bounded process navigation');
assert.equal(locale.resolveSupportedLanguage('auto',{languages:['ar-SA']},run('languageChoices')),'ar');assert.equal(locale.languageDirection('ar'),'rtl');
run("setPreferredLanguage('fr')");assert.equal(storage.get('mg-language'),'fr');
context.location.hash='#catalog';run('render()');assert.equal(run('resolved()'),'fr','language remains selected across routes');
context.location.hash='#workshop';run('render()');assert.equal(run('resolved()'),'fr');
const roadmap=data.catalog.find(c=>!c.stages);context.location.hash=`#project/${roadmap.id}`;run('render()');select('#researchNotes').value='Persistent research draft';select('#researchNotes').oninput();assert(storage.get('mg-progress-guest').includes('Persistent research draft'));
// Stress the actual renderer with a 20-module / 520-process course, without huge navigation DOM.
const synthetic=JSON.parse(JSON.stringify(data.featured[0]));const template=synthetic.stages[0].steps[0];
synthetic.stages=Array.from({length:20},(_,m)=>({id:`stress-stage-${m}`,title:`模組 ${m}`,titleEn:`Module ${m}`,steps:Array.from({length:26},(_,n)=>({...template,id:`stress-${m}-${n}`}))}));
context.SYNTHETIC=synthetic;context.location.hash='#workshop';run("featured=[SYNTHETIC,...DATA.featured.slice(1)];activeId=SYNTHETIC.id;activeStep=519;projects={};projects[activeId]={completed:allSteps(course()).slice(0,519).map(s=>s.id),assembly:allSteps(course()).slice(0,519).map(s=>s.id),notes:'',updatedAt:1};render();");
assert.equal(run('activeStep'),519);assert(selectAll('[data-step]').length<=26,'large module navigation renders only active module');assert((fixed.get('main').innerHTML.match(/class="(?:filled )?(?:current)?" title=/g)||[]).length<=9,'windowed model tokens stay bounded');
// Account switches cannot transfer an old visible notebook or pose into the new account.
select('#notes').value='Guest-only notebook';select('#notes').oninput();run("user={id:'isolation-test',name:'Test'};projects={};render()");assert.equal(select('#notes').value,'');assert.equal(run('poseOwner'),'mg-pose-v2-isolation-test');
run("user=null;featured=DATA.featured;");

// A is in flight; B captures a newer local state before A receives a conflict.
// Both A's retry and queued B must keep the remote record and the latest typing.
run("user={id:'sync-test',name:'Sync Test'};projects={};serverVersions={};saveQueue=Promise.resolve();activeId=featured[0].id;activeStep=0;lang='en';render()");
const localStepA=run('allSteps(course())[0].id'),localStepB=run('allSteps(course())[1].id'),remoteStep=run('allSteps(course())[2].id');
let releaseFirst,releaseRetry,signalFirst,signalRetry;
const firstResponse=new Promise(resolve=>{releaseFirst=resolve;});
const retryResponse=new Promise(resolve=>{releaseRetry=resolve;});
const firstStarted=new Promise(resolve=>{signalFirst=resolve;});
const retryStarted=new Promise(resolve=>{signalRetry=resolve;});
const requests=[];
context.fetch=async(url,options)=>{
  assert.equal(url,'/api/progress');assert.equal(options.method,'PUT');
  requests.push(JSON.parse(options.body));
  if(requests.length===1){signalFirst();return firstResponse;}
  if(requests.length===2){signalRetry();return retryResponse;}
  assert.equal(requests.length,3,'only the two saves and one conflict retry are expected');
  return {ok:true,status:200,json:async()=>({updatedAt:12})};
};
select('#notes').value='Local A';select('#notes').oninput();
run(`record(activeId).completed.push(${JSON.stringify(localStepA)});record(activeId).assembly.push(${JSON.stringify(localStepA)})`);
const saveA=run('save(activeId)');await firstStarted;
select('#notes').value='Local B newest';select('#notes').setSelectionRange(5,5);select('#notes').oninput();
run(`record(activeId).completed.push(${JSON.stringify(localStepB)});record(activeId).assembly.push(${JSON.stringify(localStepB)})`);
const saveB=run('save(activeId)');
releaseFirst({ok:false,status:409,json:async()=>({current:{completed:[remoteStep],assembly:[remoteStep],notes:'Remote notebook',updatedAt:10}})});
await retryStarted;
assert.deepEqual(new Set(requests[1].completed),new Set([localStepA,localStepB,remoteStep]),'A retry includes newer local progress and remote completion');
assert.deepEqual(new Set(requests[1].assembly),new Set([localStepA,localStepB,remoteStep]),'A retry includes newer local assembly and remote assembly');
assert(requests[1].notes.startsWith('Local B newest'),'conflict retains B notes instead of replacing with snapshot A');
assert.equal(requests[1].notes.split('Remote notebook').length-1,1,'remote notes are merged once');
assert.equal(select('#notes').value,requests[1].notes,'visible editor retains the remote merge for future input');
assert.equal(select('#notes').selectionStart,5,'conflict preserves the typing caret');
assert.equal(requests[1].baseUpdatedAt,10,'conflict retry uses the remote version');
select('#notes').value=select('#notes').value.replace('Local B newest','Local B typed during retry');select('#notes').oninput();
releaseRetry({ok:true,status:200,json:async()=>({updatedAt:11})});
await Promise.all([saveA,saveB]);
assert.equal(requests[2].baseUpdatedAt,11,'queued B uses the acknowledged A retry version');
assert.deepEqual(new Set(requests[2].completed),new Set([localStepA,localStepB,remoteStep]),'queued B cannot overwrite remote completion');
assert.deepEqual(new Set(requests[2].assembly),new Set([localStepA,localStepB,remoteStep]),'queued B cannot overwrite remote assembly');
assert(requests[2].notes.startsWith('Local B typed during retry'),'queued B rebases onto typing that happened after its snapshot');
assert.equal(requests[2].notes.split('Remote notebook').length-1,1,'queued B retains remote notes exactly once');
assert.equal(requests[2].notes.split('--- MERGED DEVICE NOTES ---').length-1,1,'one conflict marker, with no repeated merge block');
assert.equal(run('record(activeId).notes'),requests[2].notes,'latest local notes match the preserved queued state');
assert.equal(select('#notes').value,requests[2].notes,'the typed editor is not clobbered by an older acknowledgment');
assert.equal(run('serverVersions[activeId]'),12);
assert.equal(run("mergeDeviceNotes(record(activeId).notes, 'Remote notebook')"),requests[2].notes,'repeated remote note merge is idempotent');
assert.equal(run('mergeDeviceNotes(record(activeId).notes, record(activeId).notes)'),requests[2].notes,'already merged notebooks do not duplicate markers');
// Optional media gets a bounded deadline and updates only its own region.
const notesBeforeMedia=select('#notes'),notesValueBeforeMedia=notesBeforeMedia.value,mainBeforeMedia=fixed.get('main').innerHTML;
let mediaDeadline,mediaSignal;
context.setTimeout=(callback,milliseconds)=>{assert.equal(milliseconds,5000);mediaDeadline=callback;return 42;};
context.fetch=async(url,options)=>{assert.equal(url,'data/media.json');mediaSignal=options.signal;return new Promise(()=>{});};
const stalledMedia=run('loadLearningMedia()');assert.equal(typeof mediaDeadline,'function','optional media arms a deadline without blocking other code');
mediaDeadline();await stalledMedia;assert(mediaSignal.aborted,'media timeout aborts its request');
context.setTimeout=()=>0;
context.fetch=async()=>({ok:true,json:async()=>({courses:[]})});await run('loadLearningMedia()');
assert.equal(select('#notes'),notesBeforeMedia,'media update does not rebuild the notebook element');
assert.equal(select('#notes').value,notesValueBeforeMedia,'media update preserves the active draft');
assert.equal(fixed.get('main').innerHTML,mainBeforeMedia,'media update never rerenders the workshop');
context.fetch=async()=>{throw Error('Unexpected network request');};run('user=null');
context.window.MacGyverOffline={storageAvailable:false};run("authMode='offline'");assert(run('persistenceStatus()').includes('This session only'),'offline quota failure cannot claim durable storage');context.window.MacGyverOffline.storageAvailable=true;assert(run('persistenceStatus()').includes('local profile'),'offline saved label identifies browser-local persistence');run("authMode='static'");
// Geolocation can resolve after navigation or a different selected project.
const geoRequests=[];context.navigator.geolocation={getCurrentPosition(success,error){geoRequests.push({success,error});}};
run("location.hash='#map';selectedPlace='';atlasQuery='';render()");select('#mapFrame').isConnected=true;
select('#locate').onclick();const staleMapHost=select('#mapFrame');
run("location.hash='#progress';render()");staleMapHost.isConnected=false;
assert.doesNotThrow(()=>geoRequests[0].success({coords:{latitude:1,longitude:2}}),'late position after navigation is ignored');
run("location.hash='#map';render()");select('#mapFrame').isConnected=true;select('#locate').onclick();
selectAll('[data-place]')[1].onclick();select('#mapFrame').isConnected=true;const newlySelectedMap=select('#mapFrame'),newMapMarkup=newlySelectedMap.innerHTML;
geoRequests[1].success({coords:{latitude:3,longitude:4}});assert.equal(newlySelectedMap.innerHTML,newMapMarkup,'old geolocation cannot overwrite a new selected place');
select('#locate').onclick();select('#locate').onclick();geoRequests[2].success({coords:{latitude:5,longitude:6}});assert.equal(newlySelectedMap.innerHTML,newMapMarkup,'only the most recent location request may update the map');geoRequests[3].success({coords:{latitude:7,longitude:8}});assert(newlySelectedMap.innerHTML.includes('q=7,8'),'current map request still displays the requested location');
console.error('[frontend] checking account forms, account races and protected completion');
// Name/email local profiles and optional cloud auth forms remain distinct.
let localCreated=null,cloudSignup=null,cloudLogin=null,cloudReset=null,cloudPassword=null,cloudUser=null;
context.window.MacGyverOffline={storageAvailable:true,listProfiles:()=>[{id:'profile-one',name:'Local learner'}],activeProfile:()=>({id:'profile-one'}),createProfile:(name,email)=>{localCreated={name,email}},createMember:async value=>{localCreated=value},switchProfile:()=>{}};
context.fetch=async url=>({ok:true,json:async()=>url==='/api/me'?{authMode:cloudUser?'supabase':'offline',user:cloudUser||{id:'profile-one',name:'Local learner'},aiAvailable:false}:{projects:{}}});
run("authMode='offline';user={id:'profile-one',name:'Local learner'};offlineAccountModal()");
// V12: local member accounts need username, password, email and mobile number.
for(const id of ['#offlineUsername','#offlinePassword','#offlineProfileEmail','#offlinePhone'])assert(select(id),'local member form has '+id);
select('#offlineUsername').value='nanhong';select('#offlinePassword').value='short';select('#offlineProfileEmail').value='learner@example.org';select('#offlinePhone').value='0912345678';select('#offlineProfileName').value='Nan-Hong';
await select('#offlineMemberForm').onsubmit({preventDefault(){}});assert.equal(localCreated,null,'weak password is rejected before creating a member');assert(select('#offlineProfileError').textContent.length>0);
select('#offlinePassword').value='valid long password';await select('#offlineMemberForm').onsubmit({preventDefault(){}});assert.deepEqual(JSON.parse(JSON.stringify(localCreated)),{username:'nanhong',password:'valid long password',email:'learner@example.org',phone:'+886912345678',name:'Nan-Hong'});
context.window.MacGyverCloud={configured:false};await run('cloudAccountModal()');assert(fixed.get('dialogBody').innerHTML.includes('not configured'));assert(!select('#memberPassword'),'unconfigured cloud never solicits a password');
context.window.MacGyverCloud={configured:true,getSession:async()=>cloudUser?{user:cloudUser}:null,checkAvailability:async()=>({usernameAvailable:true,phoneAvailable:true}),signUp:async value=>{cloudSignup=value;return{verificationRequired:true}},signInWithLogin:async value=>{cloudLogin=value;cloudUser={id:'cloud-one',name:'Cloud learner',email:'learner@example.org'};return{user:cloudUser}},resetPassword:async email=>{cloudReset=email},updatePassword:async password=>{cloudPassword=password},signOut:async()=>{cloudUser=null}};
await run('cloudAccountModal()');
for(const id of ['#memberUsername','#memberPassword','#memberEmail','#memberPhone','#memberLogin'])assert(select(id),'cloud member form has '+id);
select('#memberUsername').value='cloud_learner';select('#memberPassword').value='valid long password';select('#memberPassword2').value='valid long password';select('#memberEmail').value='learner@example.org';select('#memberPhone').value='+886912345678';select('#memberName').value='Cloud learner';select('#memberTerms').checked=true;
await select('#memberSignUp').onsubmit({preventDefault(){},submitter:{value:'signup'}});assert.equal(cloudSignup.username,'cloud_learner');assert.equal(cloudSignup.phone,'+886912345678');assert.equal(cloudSignup.email,'learner@example.org');assert(select('#cloudAccountStatus').textContent.includes('verification'),'registration requests email verification instead of claiming login');assert.equal(fixed.get('dialog').open,true,'verification dialog remains open');assert(!fixed.get('main').innerHTML.includes('id="protectedAccountStatus"'),'unverified registration restores the background page');assert.equal(run('currentPage'),run("location.hash.slice(1).split('/')[0]"));
select('#memberLogin').value='learner@example.org';await select('#memberSignIn').onsubmit({preventDefault(){},submitter:{value:'reset'}});assert.equal(cloudReset,'learner@example.org');
select('#memberLogin').value='cloud_learner';select('#memberLoginPassword').value='valid long password';await select('#memberSignIn').onsubmit({preventDefault(){},submitter:{value:'signin'}});assert.equal(cloudLogin.login,'cloud_learner');assert.equal(run('authMode'),'supabase');assert.equal(run('user.id'),'cloud-one');
await run('cloudAccountModal()');select('#cloudNewPassword').value='new valid long password';await select('#cloudPasswordForm').onsubmit({preventDefault(){}});assert.equal(cloudPassword,'new valid long password');await select('#cloudLogout').onclick();assert.equal(run('authMode'),'offline');assert.equal(run('user.id'),'profile-one','cloud sign-out returns to the local profile');
// Retrying a stored cloud session after a failed startup needs an explicit
// profile switch, and must drain local saves before reading cloud records.
cloudUser={id:'cloud-resume',name:'Returning learner',email:'returning@example.org'};let cloudResumed=false,resumeCalls=0,releaseLocalQueue;
const localBeforeResume={semiconductor:{completed:[],assembly:[],notes:'Local retained',updatedAt:20}};storage.set('mg-progress-profile-one',JSON.stringify(localBeforeResume));
context.window.MacGyverCloud.resumeSession=async({expectedUserId})=>{assert.equal(expectedUserId,'cloud-resume');resumeCalls++;cloudResumed=true;return{user:cloudUser}};
context.fetch=async url=>({ok:true,json:async()=>url==='/api/me'?{authMode:cloudResumed?'supabase':'offline',user:cloudResumed?cloudUser:{id:'profile-one',name:'Local learner'}}:{projects:cloudResumed?{semiconductor:{completed:[],assembly:[],notes:'Cloud retained',updatedAt:30}}:localBeforeResume}});
context.pendingLocalQueue=new Promise(resolve=>{releaseLocalQueue=resolve});run("authMode='offline';user={id:'profile-one',name:'Local learner'};projects={};saveQueue=pendingLocalQueue");
await run('cloudAccountModal()');assert(select('#cloudResume'),'verified but inactive session exposes Resume cloud learning');assert.equal(run('authMode'),'offline','opening the account dialog does not switch profiles');const resumeAction=select('#cloudResume').onclick();await Promise.resolve();assert.equal(resumeCalls,0,'resume waits for the local save queue');releaseLocalQueue();await resumeAction;
assert.equal(resumeCalls,1);assert.equal(run('user.id'),'cloud-resume');assert.equal(run('projects.semiconductor.notes'),'Cloud retained');assert.deepEqual(JSON.parse(storage.get('mg-progress-profile-one')),localBeforeResume,'UI resume preserves local progress');await run('cloudAccountModal()');assert(!select('#cloudResume'),'active cloud session does not offer redundant resume');
// The course-specific photo context is visible in both places; explicit step
// captions still take priority for a more precise process-stage description.
run("lang='en';activeId=featured[0].id;activeStep=0;projects={};");
run("var captionCourse=course(),captionStep=allSteps(captionCourse)[0],captionPhoto=photos.find(p=>p.id===captionStep.photoId)||photoFor(captionCourse),captionHero=photoFor(captionCourse),captionBefore=captionPhoto.courseContext,captionHeroBefore=captionHero.courseContext,captionStepBefore=captionStep.photoNoteEn;captionPhoto.courseContext={...captionPhoto.courseContext,[captionCourse.id]:{noteEn:'COURSE-SPECIFIC PHOTO CONTEXT'}};captionHero.courseContext={...captionHero.courseContext,[captionCourse.id]:{noteEn:'COURSE-SPECIFIC PHOTO CONTEXT'}};captionStep.photoNoteEn='';");
// A Chinese fallback may exist on the step, so test context only with both
// language variants temporarily absent.
run("var captionStepZhBefore=captionStep.photoNote;captionStep.photoNote=''");
assert(run('renderWorkshop()').includes('COURSE-SPECIFIC PHOTO CONTEXT'));assert(run('renderProject(activeId)').includes('COURSE-SPECIFIC PHOTO CONTEXT'));
run("captionStep.photoNoteEn='EXPLICIT STEP PHOTO CONTEXT'");assert(run('renderWorkshop()').includes('EXPLICIT STEP PHOTO CONTEXT'));
run('captionPhoto.courseContext=captionBefore;captionHero.courseContext=captionHeroBefore;captionStep.photoNoteEn=captionStepBefore;captionStep.photoNote=captionStepZhBefore');
// A pending save must never mutate the newly selected account or send its queued sibling.
run("user={id:'owner-A',name:'A'};authMode='supabase';projects={semiconductor:{completed:[],assembly:[],notes:'A private',updatedAt:1}};serverVersions={semiconductor:1};saveQueue=Promise.resolve();accountGeneration++");
let releaseOldSave,oldRequests=0;
context.fetch=async(url,options)=>{assert.equal(url,'/api/progress');assert.equal(JSON.parse(options.body).ownerId,'owner-A','save snapshots retain the owning account for service-transition checks');oldRequests++;return new Promise(resolve=>{releaseOldSave=resolve})};
const oldSave=run("save('semiconductor')");await Promise.resolve();await Promise.resolve();assert.equal(oldRequests,1);
const queuedOldSave=run("save('semiconductor')");
run("user={id:'owner-B',name:'B'};projects={semiconductor:{completed:[],assembly:[],notes:'B private',updatedAt:90}};serverVersions={semiconductor:90};saveState='B status';accountGeneration++");
releaseOldSave({ok:false,status:409,json:async()=>({current:{completed:['from-A'],assembly:['from-A'],notes:'A remote',updatedAt:2}})});
await Promise.all([oldSave,queuedOldSave]);assert.equal(oldRequests,1,'queued A save is dropped after account change');assert.equal(run('projects.semiconductor.notes'),'B private');assert.equal(run('serverVersions.semiconductor'),90);assert.equal(run('saveState'),'B status','late A result does not alter B status');
// A slower account initialization cannot overwrite a newer login.
let releaseMe,meCount=0;context.fetch=async url=>{if(url==='/api/me'&&meCount++===0)return new Promise(resolve=>{releaseMe=resolve});return {ok:true,json:async()=>url==='/api/me'?{user:{id:'new-owner',name:'New'},authMode:'supabase'}:{projects:{}}}};
const staleInit=run('initAccount()');await run('initAccount()');releaseMe({ok:true,json:async()=>({user:{id:'old-owner',name:'Old'},authMode:'supabase'})});await staleInit;assert.equal(run('user.id'),'new-owner','new login survives late older /api/me response');
// Protected completion must not double-advance or alter a newly selected course.
context.billingState=()=>({protected:true,freeCourseIds:[],plans:[]});
run("featured=DATA.featured;activeId='semiconductor';activeStep=0;user={id:'verified-A',name:'A'};accountGeneration++;projects={};var verifyStep=allSteps(course())[0];record(activeId).assembly.push(verifyStep.id);stepPose(activeId,verifyStep.id).answer=verifyStep.quiz.answer;quizPass.add(activeId+':'+verifyStep.id)");
let releaseEvidence,evidenceRequests=0;
context.submitVerifiedStep=()=>{evidenceRequests++;return new Promise(resolve=>{releaseEvidence=resolve})};
const checking=run('completeStep()');assert.equal(await run('completeStep()'),false);assert.equal(evidenceRequests,1,'one server evidence request despite double click');
run("activeId='packaging';activeStep=0");releaseEvidence({passed:true});assert.equal(await checking,false);assert.equal(run('activeStep'),0,'old course response does not advance new course');assert.equal(run('completionPending'),false,'inflight guard resets');
run("activeId='semiconductor';activeStep=0");const checkingOwner=run('completeStep()');run("user={id:'verified-B',name:'B'};accountGeneration++");releaseEvidence({passed:true});assert.equal(await checkingOwner,false);assert.equal(run('activeStep'),0,'old account response cannot mutate new account');
context.billingState=membership.billingState;
const css=fs.readFileSync(path.join(root,'style.css'),'utf8');assert(!/fonts\.googleapis\.com/.test(css),'local stylesheet has no automatic font CDN request');assert(/\.workbenches \.model\{height:clamp\(115px,33vw,175px\);min-height:0;max-height:none;aspect-ratio:auto\}/.test(css),'compact mobile model overrides the older more-specific sizing rule');
// V12 paywall: first stage free, later stages locked until a pass is active.
paywall.configurePaywall({config:{paywall:{enabled:true,freeStagesPerCourse:1,ownerPreviewOnFile:false}}});
{
  const semi=data.featured.find(c=>c.id==='semiconductor'),firstStage=semi.stages[0].steps.length,all=semi.stages.flatMap(s=>s.steps).map(s=>s.id);
  run(`activeId='semiconductor';activeStep=${firstStage+5};projects.semiconductor={completed:${JSON.stringify(all)},assembly:${JSON.stringify(all)},notes:'',updatedAt:1};`);
  const html=run('renderWorkshop()');
  assert.equal(run('activeStep'),firstStage,'navigation stops at the first paid step');
  assert(html.includes('paywallStep')&&!html.includes('id="quizSection"'),'paid step shows the membership card, not the lesson');
  run(`activeStep=${firstStage-1}`);assert(run('renderWorkshop()').includes('id="quizSection"'),'free first stage renders the full lesson');
}
console.log(JSON.stringify({passed:true,projectRenders,stepRenders,catalog:data.catalog.length,guidedCourses:data.featured.length,sources:data.sources.length,photos:data.photos.length,consecutiveStepsVerified:3,taskModes:[...taskModes],taskReloadVerified:true,oldCompletedProgressPreserved:true,controls:['grab','arrow XY','physical code','IME/non-Latin labels','dead-key code','focus activation','input/dialog exclusion','autorepeat','keyup after focus change','blur','two-hand touch','combined axes','precision','inferred Right Shift release','Shift-first undo','collision','undo','reset','pose reload'],migrationVerified:true,languagePreferenceVerified:true,synthetic520Verified:true,accountIsolationVerified:true,cloudAccountFormsVerified:true,optionalLocalEmailVerified:true,queuedConflictMergeVerified:true,queuedAccountSwitchIsolationVerified:true,accountInitRaceVerified:true,protectedDoubleClickAndSwitchVerified:true,realWorkspaceBootVerified:true,nonblockingMediaVerified:true,tutorContextVerified:true,maxTutorContextChars,narratedProcedureVerified:true,skipTourCannotCompleteStep:true,fullGuidanceRequiresEvidenceAndQuiz:true,guidancePauseAndFullUndoVerified:true,visibleNextActionVerified:true,allGuidedCoursesVisible:true,catalogCsvRows:data.catalog.length,domainCountsVerified:20,allAtlasEntriesVisible:true,atlasEntries:data.coursePlaces.courses.length,limitations:'Node VM checks HTML/data and handlers with mocked requests; no browser layout or real network/auth coverage.'},null,2));
