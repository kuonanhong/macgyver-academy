import fs from 'node:fs';
import assert from 'node:assert/strict';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
import {COMPUTING_SUBJECTS,COMPUTING_COURSE_LABS,renderComputingVisual,renderComputingIcon} from '../public/academy/computing-visuals.js';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const directory=path.join(root,'public/academy/assets/diagrams/computing-v11'),iconDirectory=path.join(root,'public/academy/assets/icons/computing-v11');
const check=process.argv.includes('--check');
if(!check){fs.mkdirSync(directory,{recursive:true});fs.mkdirSync(iconDirectory,{recursive:true});}
const files=[];
const save=(target,body)=>{const text=body+'\n';if(check)assert.equal(fs.readFileSync(target,'utf8'),text,'Stale computing artwork: '+target);else fs.writeFileSync(target,text);files.push({path:path.relative(path.join(root,'public/academy'),target).split(path.sep).join('/'),sha256:createHash('sha256').update(text).digest('hex'),bytes:Buffer.byteLength(text)});};
for(const id of Object.keys(COMPUTING_SUBJECTS).sort()){save(path.join(directory,id+'-zh.svg'),renderComputingVisual(id,{zh:true}));save(path.join(directory,id+'-en.svg'),renderComputingVisual(id,{zh:false}));save(path.join(iconDirectory,id+'.svg'),renderComputingIcon(id));}
const manifest={version:11,license:'CC-BY-4.0',author:'MacGyver Engineering Academy',original:true,scope:'Conceptual architecture, not proprietary layouts or measured digital twins.',topics:Object.entries(COMPUTING_SUBJECTS).map(([id,s])=>({id,title:s.title,titleEn:s.titleEn,family:s.family,layout:s.layout,labKinds:COMPUTING_COURSE_LABS[id],icon:`assets/icons/computing-v11/${id}.svg`,diagrams:{zh:`assets/diagrams/computing-v11/${id}-zh.svg`,en:`assets/diagrams/computing-v11/${id}-en.svg`}})),files};
const manifestText=JSON.stringify(manifest,null,2)+'\n';
if(check)assert.equal(fs.readFileSync(path.join(directory,'manifest.json'),'utf8'),manifestText,'Stale computing artwork manifest');else fs.writeFileSync(path.join(directory,'manifest.json'),manifestText);
console.log(JSON.stringify({ok:true,checked:check,topics:manifest.topics.length,diagrams:200,icons:100,bytes:files.reduce((n,f)=>n+f.bytes,0),mappedLabs:new Set(manifest.topics.flatMap(s=>s.labKinds)).size}));
