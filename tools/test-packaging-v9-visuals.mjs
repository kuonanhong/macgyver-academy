import assert from 'node:assert/strict';
import fs from 'node:fs';
import {spawnSync} from 'node:child_process';
import {PACKAGING_SUBJECTS,packagingGeometry,renderPackagingVisual} from '../public/academy/packaging-visuals.js';
import {renderPackagingIcon,packagingIconFamilies} from '../public/academy/packaging-icons.js';
import {PACKAGING_LABS,PACKAGING_COURSE_LABS,calculatePackagingLab,packagingLabKind,packagingLabDetail} from '../public/academy/packaging-calculators.js';
import {labMarkup,calculateLab,bindLab} from '../public/academy/engineering-labs.js';
import {projectIdentitySvg,projectIconSvg} from '../public/academy/project-identity.js';
import {resolveExercise,evaluateExercise,renderExerciseSvg} from '../public/academy/process-exercises.js';
const catalog=JSON.parse(fs.readFileSync(new URL('../public/academy/data/catalog.json',import.meta.url)));
const ids=catalog.filter(c=>c.category==='packaging').map(c=>c.id).sort();
assert.equal(ids.length,100);assert.deepEqual(Object.keys(PACKAGING_SUBJECTS).sort(),ids);assert.deepEqual(Object.keys(PACKAGING_COURSE_LABS).sort(),ids);
assert.equal(renderPackagingVisual('unknown'),'');assert.equal(renderPackagingIcon('unknown'),'');
const svgs=[],shapes=new Set();let rendered=0;
for(const id of ids){const c={...catalog.find(c=>c.id===id),curriculumVersion:9};
 for(const en of [false,true]){
  const svg=projectIdentitySvg(c,{en}),icon=projectIconSvg(c,{en});svgs.push(svg,icon);assert(svg.includes('data-original="true"'));assert(svg.includes('data-project-identity="'+id+'"'));assert(icon.includes('data-project-icon="'+id+'"'));assert(svg.includes(en?c.titleEn:c.title));
  assert(!/<(?:script|image|foreignObject)\b|\bon\w+=|NaN|undefined/.test(svg+icon));
 }
 const geometry=packagingGeometry(PACKAGING_SUBJECTS[id].family,{labels:false});assert(geometry);shapes.add(geometry);
 for(const kind of PACKAGING_COURSE_LABS[id])assert(PACKAGING_LABS[kind]);
 const step={id:id+'-v9-test',sequence:3,title:'界面證據與誤差',titleEn:'Interface evidence and uncertainty',instruction:'比較此工序的量測與模型。',instructionEn:'Compare this step’s measurement and model.',check:'核對材料、單位及邊界。',checkEn:'Check material, units and boundaries.',quiz:{question:'哪項是本工序的直接證據？',questionEn:'Which is direct evidence for this step?',options:['量測值','外觀','其他材料'],optionsEn:['Measurement','Appearance','Another material'],answer:0,explanation:'須核對量測定義。',explanationEn:'Check the measurement definition.'}};
 const kind=packagingLabKind(c,step);assert.equal(kind!==undefined,true);
 if(PACKAGING_COURSE_LABS[id].length){assert(kind);assert(labMarkup(c,step,true).includes('engineeringLab'));}
 else {assert.equal(kind,'');assert.equal(labMarkup(c,step,false),'');}
 if(!['packaging','silicon-photonics','a106'].includes(id)){
  const spec=resolveExercise(c,step);assert.equal(spec.scene,'packv9:'+id);assert.equal(spec.provenance,'semantic-template');assert.equal(spec.expectedChoice,'answer-0');assert(spec.instruction.en.includes(step.quiz.questionEn));
  assert(!evaluateExercise(spec,spec.initialState).passed);assert(!evaluateExercise(spec,{choice:'answer-1',observed:true}).passed);assert(!evaluateExercise(spec,{choice:'answer-0',observed:false}).passed);assert(evaluateExercise(spec,{choice:'answer-0',observed:true}).passed);
  const scene=renderExerciseSvg({course:c,step,state:{choice:'answer-0',observed:true},labels:{language:'en'}});assert(scene.includes('data-course="'+id+'"'));svgs.push(scene);rendered++;
 }
}
assert(shapes.size>=90,'Distinct geometry must remain distinct with all human labels removed');assert(packagingIconFamilies.length>=50);
const py=spawnSync('python',['-c','import json,sys,xml.etree.ElementTree as E\nfor s in json.load(sys.stdin): E.fromstring(s)'],{input:JSON.stringify(svgs),encoding:'utf8'});assert.equal(py.status,0,py.stderr);
const near=(v,w,tol=1e-9)=>assert(Math.abs(v-w)<tol,`${v} vs ${w}`);
near(calculateLab('pkgTsv',{rho:1.7,length:50,diameter:10}),10.822536130248883);
near(calculateLab('pkgUncertainty',{rho:3,length:1,diameter:2}),Math.sqrt(26));
near(calculateLab('pkgCte',{alpha1:17,alpha2:2.6,length:10,deltaT:100}),14.4);
near(calculateLab('pkgCte',{alpha1:2.6,alpha2:17,length:10,deltaT:100}),-14.4);
near(calculateLab('pkgTim',{thickness:50,conductivity:5,area:100,contact:.1}),.2);
near(calculateLab('pkgFill',{gap:20,surface:30,angle:60,time:30,viscosity:.5}),Math.sqrt(6));
near(calculateLab('pkgPdn',{allow:20,current:40}),.5);
near(calculateLab('pkgOverlap',{offset:1,radius:2}),77.8800783071405);
near(calculateLab('pkgFsr',{wavelength:1550,group:4,radius:10}),9.559243769456964);
near(calculateLab('pkgDrift',{wavelength:1550,group:4,thermo:1.8,neff:2.4,alpha:2.6,temperature:10}),.72168);
near(calculateLab('pkgPhase',{index:1,length:1,wavelength:1550}),.40536679401158615);
near(calculateLab('pkgAwg',{wavelength:1550,group:4,increment:30}),20.020833333333332);
near(calculateLab('pkgBudget',{transmit:3,coupling:4,path:3,reserve:2,sensitivity:-10}),4);
near(calculateLab('pkgN1',{paths:4,capacity:100,demand:250}),50);
near(calculateLab('pkgStressPhase',{length:1,wavelength:1550,deltaIndex:-50,effective:2.4,strain:100}),770.1969086220137);
near(calculateLab('pkgRc',{resistance:50,capacitance:100}),31.830988618379067);
near(calculateLab('pkgCoolant',{power:100,flow:10,specific:4200}),2.380952380952381);
// Independent one-dimensional numerical Gaussian overlap: the orthogonal y factor cancels.
let overlap=0,normA=0,normB=0;const dx=.002,w=2,d=1;
for(let x=-16;x<=16;x+=dx){const a=Math.exp(-x*x/(w*w)),b=Math.exp(-(x-d)*(x-d)/(w*w));overlap+=a*b*dx;normA+=a*a*dx;normB+=b*b*dx;}
near(calculateLab('pkgOverlap',{offset:d,radius:w})/100,overlap*overlap/(normA*normB),1e-10);
assert.equal(calculatePackagingLab('unknown',{}),null);
for(const [kind,lab]of Object.entries(PACKAGING_LABS)){
 assert(lab.note[0].length>40&&lab.note[1].length>80);const defaults=Object.fromEntries(lab.params.map(p=>[p[0],p[5]]));
 for(const param of lab.params)for(const index of [2,3])assert(Number.isFinite(calculateLab(kind,{...defaults,[param[0]]:param[index]})),kind+' bound '+param[0]);
 assert.equal(typeof packagingLabDetail(kind,defaults,true),'string');
}
// Verify a signed chart remains within its plotting window and outputs remain signed.
const lab=PACKAGING_LABS.pkgCte,inputs=lab.params.map(p=>({dataset:{labInput:p[0]},value:String(p[5])}));inputs.find(x=>x.dataset.labInput==='alpha1').value='2';inputs.find(x=>x.dataset.labInput==='alpha2').value='17';
const nodes=new Map(['#labResult','#labDetail','#labScenarioNote','#labChart'].map(id=>[id,{}]));
const root={querySelectorAll:()=>inputs,querySelector:id=>nodes.get(id)||null};globalThis.document={querySelector:()=>root};bindLab({id:'a115',category:'packaging'},{sequence:1},false);delete globalThis.document;
assert(nodes.get('#labResult').textContent.startsWith('-'));assert(!nodes.get('#labChart').innerHTML.includes('NaN'));assert(nodes.get('#labChart').innerHTML.includes('-30.0'));
if(process.argv.includes('--contact-sheet')){
 const samples=['a103','a106','a114','a123','a139','a151','a154','a160','a174','a178','a188','a196'];
 const svg=`<svg xmlns="http://www.w3.org/2000/svg" width="1800" height="1480" viewBox="0 0 1800 1480"><rect width="1800" height="1480" fill="white"/>${samples.map((id,i)=>`<g transform="translate(${i%3*600} ${Math.floor(i/3)*370})">${renderPackagingVisual(id,{zh:false}).replace('<svg ','<svg width="600" height="370" ')}</g>`).join('')}</svg>`;fs.writeFileSync('/tmp/packaging-v9-contact.svg',svg);
 const glyphSvg=`<svg xmlns="http://www.w3.org/2000/svg" width="960" height="1400" viewBox="0 0 960 1400"><rect width="960" height="1400" fill="white"/>${ids.map((id,i)=>`<g transform="translate(${i%10*96} ${Math.floor(i/10)*140})">${renderPackagingIcon(id,{en:true}).replace('<svg ','<svg width="88" height="104" ')}</g>`).join('')}</svg>`;fs.writeFileSync('/tmp/packaging-v9-icons.svg',glyphSvg);
}
console.log(JSON.stringify({ok:true,packagingTopics:ids.length,distinctLabelFreeGeometry:shapes.size,iconFamilies:packagingIconFamilies.length,svgXmlDocuments:svgs.length,newWorkbenchScenes:rendered,dimensionedModels:Object.keys(PACKAGING_LABS).length,calculatorMappedTopics:Object.values(PACKAGING_COURSE_LABS).filter(x=>x.length).length,realBrowserTested:false}));
