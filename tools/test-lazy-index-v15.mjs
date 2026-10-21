import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import {gzipSync} from 'node:zlib';
import {expandLazyIndex} from '../public/academy/lazy-index-codec.js';
const root=new URL('../public/academy/',import.meta.url);
const read=name=>fs.readFileSync(new URL(name,root));
const raw=read('data/lazy/index.json'),wire=read('data/lazy/index.compact.json');
const expanded=JSON.parse(raw),compact=JSON.parse(wire);
assert.deepEqual(expandLazyIndex(compact),expanded,'all fields, order, step IDs and descriptors survive wire compaction');
assert(wire.length<raw.length*.85,'wire representation saves at least 15% before HTTP compression');
const context=vm.createContext({window:{}});
vm.runInContext(read('offline-data.js').toString(),context);
assert.deepEqual(JSON.parse(JSON.stringify(context.window.MG_LAZY_INDEX)),expanded,'file mode expands exactly the same index');
assert(!read('index.html').toString().includes('offline-data.js'),'homepage shell is parsed before course catalogue script');
const mutated=change=>{const v=structuredClone(compact);change(v);return v;};
const id=Object.keys(compact.courses)[0];
for(const [label,change] of [
 ['path traversal',v=>{v.courses['../bad']=v.courses[id];}],
 ['prototype name',v=>{v.courses.constructor=v.courses[id];}],
 ['invalid digest',v=>{v.courses[id][0]='not-a-digest';}],
 ['oversized chunk',v=>{v.courses[id][1]=33*1024*1024;}],
 ['fractional bytes',v=>{v.courses[id][1]=3.5;}],
 ['step object in compact payload',v=>{v.catalog.find(c=>c.stages).stages[0].steps[0]={id:'bad'};}],
 ['malformed catalogue',v=>{v.catalog=[null];}],
 ['malformed descriptor table',v=>{v.resources=[];}]
])assert.throws(()=>expandLazyIndex(mutated(change)),/Invalid compact/,label);
assert.equal(expandLazyIndex(expanded),expanded,'expanded indexes remain accepted');
console.log(JSON.stringify({status:'PASS',catalog:expanded.catalog.length,lossless:true,malformedCases:8,expandedBytes:raw.length,compactBytes:wire.length,reductionPercent:Number((100*(1-wire.length/raw.length)).toFixed(2)),gzipCompactBytes:gzipSync(wire).length,gzipNote:'Measurement only; actual server compression depends on host configuration.'}));
