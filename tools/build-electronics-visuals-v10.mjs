import fs from 'node:fs';
import assert from 'node:assert/strict';
const root=new URL('../',import.meta.url),input=new URL('tools/electronics-v10/visual-subjects.json',root),output=new URL('public/academy/electronics-visuals.js',root);
const subjects=JSON.parse(fs.readFileSync(input,'utf8'));
assert.equal(Object.keys(subjects).length,100);
for(let i=201;i<=300;i++){const item=subjects['a'+i];assert(item?.title&&item.titleEn&&item.nodes?.length===3);for(const node of item.nodes)assert(node.kind&&node.zh&&node.en)}
const current=fs.readFileSync(output,'utf8'),start=current.indexOf('export const ELECTRONICS_SUBJECTS=Object.freeze('),end=current.indexOf('\nconst C=');assert(start>=0&&end>start);
const next=current.slice(0,start)+'export const ELECTRONICS_SUBJECTS=Object.freeze('+JSON.stringify(subjects)+');'+current.slice(end);
if(process.argv.includes('--check'))assert.equal(current,next,'Electronics visual metadata must be rebuilt');else fs.writeFileSync(output,next);
console.log('100 electronics visual subject definitions '+(process.argv.includes('--check')?'verified':'rebuilt'));
