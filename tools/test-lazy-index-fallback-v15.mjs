// Focused request-contract tests; no build, generated data, or network required.
import assert from 'node:assert/strict';
import {createCurriculumLoader} from '../public/academy/curriculum-loader.js';
import {expandLazyIndex} from '../public/academy/lazy-index-codec.js';

const compactURL='data/lazy/index.compact.json',legacyURL='data/lazy/index.json';
const digest='a'.repeat(64);
const compact={compactVersion:1,lazyVersion:1,guidedIds:['fixture'],catalog:[{id:'fixture',title:'Fixture',stages:[{id:'stage',steps:['step-1']}]}],photos:[],release:{},courses:{fixture:[digest,2]},resources:{fixture:[digest,2]},auxiliary:{}};
const expanded=expandLazyIndex(compact);
const response=value=>new Response(JSON.stringify(value));
let cases=0;
function fixture(handle,options={}){
  const calls=[];
  const loader=createCurriculumLoader({view:{},location:{protocol:'https:'},...options,fetchImpl:async(url,init)=>{calls.push(url);assert.equal(init.cache,'no-cache');assert.equal(init.redirect,'error');return handle(url,init);}});
  return {loader,calls};
}
for(const payload of [compact,expanded]){
  const {loader,calls}=fixture(()=>response(payload));
  const [first,second]=await Promise.all([loader.index(),loader.index()]);
  assert.deepEqual(first,expanded);assert.equal(first,second);
  assert.deepEqual(calls,[compactURL]);cases++;
}
for(const status of [404,410]){
  const {loader,calls}=fixture(url=>url===compactURL?new Response('',{status}):response(expanded));
  assert.deepEqual(await loader.index(),expanded);
  assert.deepEqual(calls,[compactURL,legacyURL]);cases++;
}
for(const status of [401,403,429,500,503]){
  const {loader,calls}=fixture(url=>url===compactURL?new Response('',{status}):response(expanded));
  await assert.rejects(loader.index(),/request failed/);
  assert.deepEqual(calls,[compactURL]);cases++;
}
for(const fail of [
  ()=>{throw new TypeError('network failed');},
  ()=>{throw Object.assign(new Error('not an HTTP response'),{status:404});},
  ()=>new Response('{broken JSON'),
  ()=>response({...compact,courses:{fixture:['bad digest',2]}}),
  ()=>response({...compact,guidedIds:['unknown']}),
  ()=>response({...compact,catalog:[null]}),
  ()=>new Response('{}',{headers:{'content-length':String(13*1024*1024)}})
]){
  const {loader,calls}=fixture(url=>url===compactURL?fail():response(expanded));
  await assert.rejects(loader.index());
  assert.deepEqual(calls,[compactURL]);cases++;
}
{
  const bad=structuredClone(expanded);bad.courses.fixture.file='../unsafe.json';
  const {loader,calls}=fixture(url=>url===compactURL?new Response('',{status:404}):response(bad));
  await assert.rejects(loader.index(),/unsafe/);
  assert.deepEqual(calls,[compactURL,legacyURL]);cases++;
}
{
  let missing=true;
  const {loader,calls}=fixture(url=>url===compactURL||missing?new Response('',{status:404}):response(expanded));
  await assert.rejects(loader.index(),/request failed/);missing=false;
  assert.deepEqual(await loader.index(),expanded);
  assert.deepEqual(calls,[compactURL,legacyURL,compactURL,legacyURL]);cases++;
}
{
  const {loader,calls}=fixture(()=>{throw Error('file mode must not fetch');},{location:{protocol:'file:'}});
  await assert.rejects(loader.index(),/Extract the complete ZIP/);
  assert.deepEqual(calls,[]);cases++;
}
{
  const {loader,calls}=fixture(()=>{throw Error('preloaded mode must not fetch');},{view:{MG_LAZY_INDEX:expanded},location:{protocol:'file:'}});
  assert.equal(await loader.index(),expanded);assert.deepEqual(calls,[]);cases++;
}
console.log(JSON.stringify({status:'PASS',cases,legacyFallback:'HTTP 404/410 only',malformedPayloads:'fail closed',fileMode:'unchanged',writes:0,networkRequests:0}));
