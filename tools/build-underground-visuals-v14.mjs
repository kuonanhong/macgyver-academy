import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {renderWorldVisual,renderWorldIcon,hasWorldVisual} from '../public/academy/world-project-visuals.js';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..'),dir=path.join(root,'public/academy/assets/diagrams/underground-v14'),check=process.argv.includes('--check');
const data=JSON.parse(fs.readFileSync(path.join(root,'tools/underground-v14/underground.json'),'utf8'));if(data.courses.length!==100)throw Error('Expected 100 authored projects');
if(!check)fs.mkdirSync(dir,{recursive:true});
let count=0;
for(const c of data.courses){
 if(!/^[a-z0-9-]+$/.test(c.id)||!hasWorldVisual(c))throw Error('Invalid diagram inputs '+c.id);
 for(const [suffix,content] of [['zh',renderWorldVisual(c,{zh:true})],['en',renderWorldVisual(c,{zh:false})],['icon',renderWorldIcon(c,{en:true})]]){
  const file=path.join(dir,c.id+'-'+suffix+'.svg');if(check){if(fs.readFileSync(file,'utf8')!==content+'\n')throw Error('Stale diagram '+file);}else fs.writeFileSync(file,content+'\n');count++;
 }
}
console.log(`${check?'Verified':'Built'} ${count} original underground SVGs (100 bilingual architectures and icons).`);
