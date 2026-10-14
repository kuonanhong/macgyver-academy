/** Rebuild the generated whole-course JSON from checked-in bounded parts. */
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {fileURLToPath} from 'node:url';
const hash=bytes=>crypto.createHash('sha256').update(bytes).digest('hex');
export function restoreFeatured(root,{normalize=false}={}){
 const data=path.join(root,'public/academy/data'),target=path.join(data,'featured.json');
 if(fs.existsSync(target)){
  if(normalize){const old=fs.readFileSync(target),value=JSON.parse(old);if(!Array.isArray(value))throw Error('Invalid canonical curriculum');const bytes=Buffer.from(JSON.stringify(value)+'\n');if(!bytes.equals(old)){fs.writeFileSync(target+'.tmp',bytes);fs.renameSync(target+'.tmp',target)}}
  return target;
 }
 const dir=path.join(data,'course-parts'),index=JSON.parse(fs.readFileSync(path.join(dir,'index.json'),'utf8'));
 if(index.schemaVersion!==1||index.dataSet!=='featured'||!Array.isArray(index.parts)||!index.parts.length||index.parts.length>1024||!Number.isSafeInteger(index.courseCount)||index.courseCount<1||index.courseCount>20000)throw Error('Invalid curriculum manifest');
 const chunks=[],seen=new Set();let size=0;
 for(const [i,p]of index.parts.entries()){
  if(typeof p.file!=='string'||!/^part-\d{4}-[a-f0-9]{16}\.json$/.test(p.file)||!p.file.startsWith(`part-${String(i+1).padStart(4,'0')}-`)||!/^[a-f0-9]{64}$/.test(p.sha256)||!p.file.endsWith(`-${p.sha256.slice(0,16)}.json`)||!Number.isSafeInteger(p.byteLength)||p.byteLength<2||p.byteLength>7*1024*1024)throw Error('Unsafe curriculum part');
  const file=path.join(dir,p.file);const stat=fs.lstatSync(file);if(!stat.isFile()||stat.isSymbolicLink()||stat.size!==p.byteLength)throw Error('Unexpected curriculum file or size');
  const bytes=fs.readFileSync(file);size+=bytes.length;if(size>256*1024*1024||bytes.length!==p.byteLength||hash(bytes)!==p.sha256)throw Error('Curriculum checksum or size mismatch');
  const courses=JSON.parse(bytes);if(!Array.isArray(courses)||courses.length!==p.courseCount||!Array.isArray(p.courseIds)||p.courseIds.length!==courses.length)throw Error('Curriculum part count mismatch');
  for(const [j,c]of courses.entries()){if(!c?.id||c.id!==p.courseIds[j]||seen.has(c.id)||!Array.isArray(c.stages))throw Error('Curriculum ID or course mismatch');seen.add(c.id)}
  const raw=bytes.toString('utf8').trim();if(!raw.startsWith('[')||!raw.endsWith(']'))throw Error('Invalid curriculum array');if(courses.length)chunks.push(raw.slice(1,-1));
 }
 if(seen.size!==index.courseCount)throw Error('Curriculum total mismatch');
 const raw='['+chunks.join(',')+']\n';if(JSON.parse(raw).length!==index.courseCount)throw Error('Invalid restored curriculum');
 fs.writeFileSync(target+'.tmp',raw);fs.renameSync(target+'.tmp',target);return target;
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)){const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');restoreFeatured(root);console.log('Complete curriculum available from verified bounded source parts.');}
