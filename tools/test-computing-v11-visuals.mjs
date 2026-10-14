import assert from 'node:assert/strict';
import fs from 'node:fs';
import {spawnSync} from 'node:child_process';
import {createHash} from 'node:crypto';
import {COMPUTING_SUBJECTS,computingGlyph,computingGeometry,computingVisualFamily,renderComputingVisual,renderComputingIcon,searchComputingSubjects,COMPUTING_LABS,COMPUTING_COURSE_LABS,computingLabKind,calculateComputingLab,computingLabDetail} from '../public/academy/computing-visuals.js';
const source=fs.readFileSync(new URL('../public/academy/computing-visuals.js',import.meta.url),'utf8');assert(!/\b(fetch|WebSocket|XMLHttpRequest)\s*\(/.test(source),'Computing models must not emit external traffic');
const expected=['cybersecurity',...Array.from({length:99},(_,i)=>'a'+(302+i))].sort();
assert.deepEqual(Object.keys(COMPUTING_SUBJECTS).sort(),expected);
assert.deepEqual(Object.keys(COMPUTING_COURSE_LABS).sort(),expected);
const catalog=JSON.parse(fs.readFileSync(new URL('../public/academy/data/catalog.json',import.meta.url))),geometries=new Set(),icons=new Set(),svgs=[];
for(const id of expected){const s=COMPUTING_SUBJECTS[id],c=catalog.find(c=>c.id===id);assert(c,'catalog course '+id);assert.equal(c.category,'computing');assert.equal(s.title,c.title);assert.equal(s.titleEn,c.titleEn);assert.equal(s.nodes.length,4);assert.equal(computingVisualFamily(id),s.family);for(const n of s.nodes){assert(n.zh&&n.en);assert(computingGlyph(n.kind),'missing component '+n.kind);}geometries.add(computingGeometry(id,{labels:false}));icons.add(renderComputingIcon(id).replace(/<text[^>]*>[\s\S]*?<\/text>/g,'').replace(/(?:aria-label|data-[\w-]+)="[^"]*"/g,''));for(const zh of [true,false]){const v=renderComputingVisual(id,{zh}),focused=renderComputingVisual(id,{zh,focus:1});assert(v!==focused);assert(v.includes('data-original="true"'));assert(v.includes(`data-course="${id}"`));assert(!/<(?:script|foreignObject|image)\b|\bon\w+=|NaN|undefined/.test(v));svgs.push(v);}svgs.push(renderComputingIcon(id,{en:true}));for(const k of COMPUTING_COURSE_LABS[id])assert(COMPUTING_LABS[k]);const k=computingLabKind(c,{sequence:1,titleEn:'Check evidence'});assert.equal(Boolean(k),Boolean(COMPUTING_COURSE_LABS[id].length));}
assert.equal(geometries.size,100,'Subject geometries remain distinct without labels');assert.equal(icons.size,100,'Icons remain distinct without metadata or text');
assert.equal(renderComputingVisual('missing'),'');assert.equal(renderComputingIcon('missing'),'');assert.equal(computingGlyph('missing'),'');assert.equal(computingVisualFamily('missing'),null);assert.equal(calculateComputingLab('missing'),null);
const py=spawnSync('python3',['-c','import json,sys,xml.etree.ElementTree as E\nfor s in json.load(sys.stdin): E.fromstring(s)'],{encoding:'utf8',input:JSON.stringify(svgs)});assert.equal(py.status,0,py.stderr);
assert.equal(searchComputingSubjects().length,100);assert.equal(searchComputingSubjects('GPU',{zh:false}).find(x=>x.id==='a304').title,'GPU parallel-compute cores');assert(searchComputingSubjects('後量子').some(x=>x.id==='a358'));assert.equal(searchComputingSubjects('<script>').length,0);assert.equal(searchComputingSubjects('',{limit:3}).length,3);assert.equal(searchComputingSubjects('',{limit:-3}).length,0);
const near=(a,b,t=1e-8)=>assert(Math.abs(a-b)<=t,`${a} not near ${b}`);
near(calculateComputingLab('cpPipeline',{base:1,branches:20,miss:5,penalty:15}),1.15);
near(calculateComputingLab('cpCache',{hit:1,miss:5,penalty:50}),3.5);
near(calculateComputingLab('cpRoofline',{peak:100,bandwidth:1000,intensity:20}),20);
near(calculateComputingLab('cpMatmul',{m:1024,n:1024,k:1024}),2.147483648);
assert.equal(calculateComputingLab('cpQuorum',{nodes:5}),3);assert.equal(calculateComputingLab('cpQuorum',{nodes:6}),4);
near(calculateComputingLab('cpErasure',{data:8,parity:3}),1.375);
near(calculateComputingLab('cpDowntime',{availability:99.9}),43.2);
near(calculateComputingLab('cpTail',{service:2,utilization:70}),30.701134573253942);
near(calculateComputingLab('cpPqcBytes',{framing:256,rate:10}),2.0224);
near(calculateComputingLab('cpDns',{arrival:1,ttl:60}),60/61);
near(calculateComputingLab('cpPrecision',{prevalence:.1,tpr:95,fpr:1}),8.683729433272395);
near(calculateComputingLab('cpLaplace',{sensitivity:1,epsilon:.5}),2);
near(calculateComputingLab('cpKv',{batch:4,layers:32,tokens:4096,heads:8,width:128,bytes:2}),2);
near(calculateComputingLab('cpAmdahl',{serial:5,workers:64}),15.42168674698795);
near(calculateComputingLab('cpWire',{payload:1500,rate:10000}),1.2);
near(calculateComputingLab('cpRedundancy',{single:99,copies:2}),99.99);
for(const [kind,lab] of Object.entries(COMPUTING_LABS)){assert(lab.note.every(s=>s.length>=65));assert(lab.question.every(s=>s.length>=15));const values=Object.fromEntries(lab.params.map(p=>[p[0],p[5]]));assert(Number.isFinite(calculateComputingLab(kind,values)),kind);for(const zh of [true,false]){assert(computingLabDetail(kind,values,zh));}for(const [id,,min,max,step,initial] of lab.params){assert(Math.abs((initial-min)/step-Math.round((initial-min)/step))<1e-6,'Default must align with browser range step: '+kind+' '+id);for(const val of [min,max])assert(Number.isFinite(calculateComputingLab(kind,{...values,[id]:val})),kind+' boundary '+id);for(const val of [min-1,max+1,NaN,Infinity,-Infinity,'1',undefined])assert(Number.isNaN(calculateComputingLab(kind,{...values,[id]:val})),kind+' reject '+id);}}
near(calculateComputingLab('cpRoofline',{peak:100,bandwidth:1000,intensity:200}),100);
near(calculateComputingLab('cpKv',{batch:8,layers:32,tokens:4096,heads:8,width:128,bytes:2}),4);
near(calculateComputingLab('cpRedundancy',{single:80,copies:1}),80);
assert(calculateComputingLab('cpPrecision',{prevalence:1,tpr:95,fpr:1})>calculateComputingLab('cpPrecision',{prevalence:.1,tpr:95,fpr:1}));
const manifest=JSON.parse(fs.readFileSync(new URL('../public/academy/assets/diagrams/computing-v11/manifest.json',import.meta.url)));assert.equal(manifest.files.length,300);assert.equal(manifest.topics.length,100);for(const f of manifest.files){assert(!f.path.includes('..'));const bytes=fs.readFileSync(new URL('../public/academy/'+f.path,import.meta.url));const fileName=f.path.split('/').at(-1),id=fileName.replace(/-(?:zh|en)\.svg$|\.svg$/,'');const expectedBody=(f.path.includes('/icons/')?renderComputingIcon(id):renderComputingVisual(id,{zh:fileName.endsWith('-zh.svg')}))+'\n';assert.equal(bytes.toString('utf8'),expectedBody,'Source-rendered geometry must match stored artifact: '+f.path);assert.equal(bytes.length,f.bytes);assert.equal(createHash('sha256').update(bytes).digest('hex'),f.sha256);}
if(process.argv.includes('--contact-sheet')){const ids=['a302','a304','a319','a330','a335','a358','a373','a379','a389','a392','a395','a400'];const content=ids.map((id,i)=>`<g transform="translate(${i%3*600} ${Math.floor(i/3)*370})">${renderComputingVisual(id,{zh:false}).replace('<svg ','<svg width="600" height="370" ')}</g>`).join('');fs.writeFileSync('/tmp/computing-v11-contact.svg',`<svg xmlns="http://www.w3.org/2000/svg" width="1800" height="1480" viewBox="0 0 1800 1480"><rect width="1800" height="1480" fill="white"/>${content}</svg>`);}
console.log(JSON.stringify({ok:true,topics:100,labelFreeGeometries:geometries.size,uniqueIcons:icons.size,componentKinds:new Set(Object.values(COMPUTING_SUBJECTS).flatMap(s=>s.nodes.map(n=>n.kind))).size,svgDocuments:svgs.length,calculators:Object.keys(COMPUTING_LABS).length,mappedTopics:Object.values(COMPUTING_COURSE_LABS).filter(a=>a.length).length,networkRequests:0,realBrowserTested:false}));
