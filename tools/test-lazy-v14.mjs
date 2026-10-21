import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import crypto from 'node:crypto';
import {fileURLToPath} from 'node:url';
import {createCurriculumLoader,curriculumDigest} from '../public/academy/curriculum-loader.js';
import {buildSourceIndex} from '../public/academy/source-library.js';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../public/academy');
const read=file=>JSON.parse(fs.readFileSync(path.join(root,file),'utf8'));
const index=read('data/lazy/index.json'),featured=read('data/featured.json'),catalog=read('data/catalog.json'),sourceData=read('data/sources.json');
const full=new Map([...catalog,...featured].map(c=>[c.id,c]));
assert.equal(index.catalog.length,catalog.length);assert.equal(index.catalog.filter(c=>c._lazy).length,featured.length);
for(const c of index.catalog){assert(!c.workedExample&&!c.scope&&!c.v13Extension&&!c.v14Extension,'initial metadata omits full teaching bodies');if(c.stages){assert(c._lazy);assert.deepEqual(c.stages.flatMap(s=>s.steps.map(x=>x.id)),full.get(c.id).stages.flatMap(s=>s.steps.map(x=>x.id)));for(const st of c.stages)for(const step of st.steps)assert.deepEqual(Object.keys(step),['id']);}}
for(const [id,d]of Object.entries(index.courses))assert.deepEqual(read(d.file),full.get(id),'single course preserves all authoring data '+id);
for(const [id,d]of Object.entries(index.resources)){const r=read(d.file);assert(r.media&&r.related&&r.places&&r.vendors);for(const source of r.sources)assert(sourceData.some(s=>s.id===source.id),'resource references real source '+id);}
const usage=read(index.auxiliary['source-usage'].file),a=buildSourceIndex({courses:featured,sources:sourceData,photos:index.photos}),b=buildSourceIndex({courses:usage,sources:sourceData,photos:index.photos});
const summary=rows=>rows.map(r=>[r.item.id,[...r.uses].map(([id,u])=>[id,[...u.scopes],[...u.steps]])]);
assert.deepEqual(summary(a.official),summary(b.official),'lazy citation index preserves exact stage/step/knowledge citations');assert.deepEqual(summary(a.photos),summary(b.photos));
for(const content of ['', 'abc','測試 SHA-256 '.repeat(300)]){const bytes=new TextEncoder().encode(content);assert.equal(await curriculumDigest(bytes,null),crypto.createHash('sha256').update(bytes).digest('hex'),'non-secure HTTP SHA-256 fallback');}
let requests=[],failOnce=false,corrupt=false;
const fetcher=async(url)=>{requests.push(url);assert(!url.startsWith('/'),'static asset URLs retain GitHub Pages subdirectory');if(failOnce&&url.includes('/courses/')){failOnce=false;return new Response('',{status:503});}let bytes=fs.readFileSync(path.join(root,url));if(corrupt&&url.includes('/courses/')){corrupt=false;bytes=Buffer.from(bytes);bytes[bytes.indexOf(Buffer.from('semiconductor'))]^=1;}return new Response(bytes);};
let loader=createCurriculumLoader({fetchImpl:fetcher,location:{protocol:'https:'},view:{},cryptoImpl:null});
assert.equal((await loader.data('featured')).length,featured.length);assert.deepEqual(requests,['data/lazy/index.compact.json'],'opening home never requests course bodies');
const id=featured[0].id;const [c1,c2]=await Promise.all([loader.course(id),loader.course(id)]);assert.deepEqual(c1,full.get(id));assert.deepEqual(c2,c1);assert.notEqual(c1,c2,'returned courses do not share mutable protected hydration');assert.equal(requests.filter(u=>u.includes('/courses/')).length,1,'concurrent loads deduplicate');
c1.stages=[];assert((await loader.course(id)).stages.length,'cached immutable payload survives local mutations');
failOnce=true;loader=createCurriculumLoader({fetchImpl:fetcher,location:{protocol:'https:'},view:{}});await assert.rejects(loader.course(id),/request failed/);assert.equal((await loader.course(id)).id,id,'failed loads can retry');
corrupt=true;loader=createCurriculumLoader({fetchImpl:fetcher,location:{protocol:'http:'},view:{},cryptoImpl:null});await assert.rejects(loader.course(id),/checksum/);assert.equal((await loader.course(id)).id,id,'checksum failures can retry');
const unsafe=structuredClone(index);unsafe.courses[id].file='../escape.json';await assert.rejects(createCurriculumLoader({view:{MG_LAZY_INDEX:unsafe}}).index(),/unsafe/);
await assert.rejects(loader.course('constructor'),/Invalid course ID/);await assert.rejects(loader.auxiliary('prototype'),/Invalid course or data ID/);
// Limit both declared and chunked response sizes before parsing or hashing.
let readCount=0,cancelCount=0;
const descriptor=index.courses[id];
const oversized=createCurriculumLoader({view:{MG_LAZY_INDEX:index},fetchImpl:async()=>({ok:true,headers:{get:()=>String(descriptor.byteLength+1)},body:{getReader(){readCount++;}}})});
await assert.rejects(oversized.course(id),/too large/);assert.equal(readCount,0,'reject oversized Content-Length before reading');
const streaming=createCurriculumLoader({view:{MG_LAZY_INDEX:index},fetchImpl:async()=>({ok:true,headers:{get:()=>null},body:{getReader(){return {async read(){return {done:false,value:new Uint8Array(descriptor.byteLength+1)};},async cancel(){cancelCount++;},releaseLock(){}};}}})});
await assert.rejects(streaming.course(id),/too large/);assert.equal(cancelCount,1,'oversized chunked bodies are cancelled');
const privateRequests=[];const privateLoader=createCurriculumLoader({fetchImpl:async url=>{privateRequests.push(url);return new Response(JSON.stringify(url.includes('index=1')?[index.catalog.find(c=>c.id===id)]:full.get(id)));},view:{MG_LAZY_INDEX:index}});
await privateLoader.data('featured',{protected:true});await privateLoader.course(id,{protected:true});await privateLoader.course(id,{protected:true});assert.deepEqual(privateRequests,['/api/curriculum?index=1','/api/curriculum?courseId='+id,'/api/curriculum?courseId='+id],'private data bypasses immutable static caches');
const scripts=[],view={MG_LAZY_INDEX:index},sandbox=vm.createContext({window:view});const document={createElement:()=>({remove(){}}),head:{appendChild(script){scripts.push(script.src);queueMicrotask(()=>{vm.runInContext(fs.readFileSync(path.join(root,script.src),'utf8'),sandbox);script.onload();});}}};
const offline=createCurriculumLoader({view,document,location:{protocol:'file:'},fetchImpl:()=>{throw Error('file mode must not fetch');}});
assert.equal((await offline.data('featured')).length,featured.length);assert.deepEqual(scripts,[]);assert.deepEqual(JSON.parse(JSON.stringify(await offline.course(id))),full.get(id));await offline.resources(id);assert.equal(scripts.length,2,'offline course plus its resources only');await offline.course(id);assert.equal(scripts.length,2);
console.log(JSON.stringify({passed:true,catalog:index.catalog.length,guided:featured.length,allCoursePayloadsPreserved:true,exactSourceUsage:true,dedupe:true,retry:true,checksum:true,sha256HttpFallback:true,protectedUncached:true,fileScripts:true,initialBytes:fs.statSync(path.join(root,'offline-data.js')).size}));
