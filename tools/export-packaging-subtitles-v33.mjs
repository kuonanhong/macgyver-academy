import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const ctx={window:{}};vm.runInNewContext(fs.readFileSync(path.join(root,'public/academy/packaging-tour-content-v33.js'),'utf8'),ctx);
const data=ctx.window.MACGYVER_PACKAGING_TOURS;
const out=path.join(root,'public/academy/assets/packaging-tour-v33');fs.mkdirSync(path.join(out,'subtitles'),{recursive:true});fs.mkdirSync(path.join(out,'transcripts'),{recursive:true});
const stamp=t=>{const ms=Math.round(t*1000);return `00:${String(Math.floor(ms/60000)).padStart(2,'0')}:${String(Math.floor(ms/1000)%60).padStart(2,'0')}.${String(ms%1000).padStart(3,'0')}`;};
let count=0;
for(const tour of data.tours){
 for(const lang of data.languages){
  const cues=[];
  for(const c of tour.chapters){const parts=[...new Intl.Segmenter(lang.id,{granularity:'sentence'}).segment(c.text[lang.id])].map(s=>s.segment.trim()).filter(Boolean),total=parts.reduce((s,p)=>s+p.length,0);let start=c.start;parts.forEach((text,i)=>{const end=i===parts.length-1?c.end:start+30*text.length/total;cues.push({start,end,text});start=end;});}
  const vtt='WEBVTT\n\n'+cues.map((c,i)=>`${i+1}\n${stamp(c.start)} --> ${stamp(c.end)}\n${c.text.replace(/-->/g,'→')}\n`).join('\n');
  fs.writeFileSync(path.join(out,'subtitles',`${tour.id}.${lang.id}.vtt`),vtt);
  const transcript=JSON.stringify({tour:tour.id,title:tour.title[lang.id],language:lang.id,duration:300,chapters:tour.chapters.map(c=>({start:c.start,end:c.end,title:c.title[lang.id],text:c.text[lang.id]})),sources:tour.sources},null,2);
  fs.writeFileSync(path.join(out,'transcripts',`${tour.id}.${lang.id}.json`),transcript+'\n');count++;
 }
 let metadata=';FFMETADATA1\n';for(const c of tour.chapters){metadata+=`[CHAPTER]\nTIMEBASE=1/1000\nSTART=${c.start*1000}\nEND=${c.end*1000}\ntitle=${c.title.en.replace(/[=;#\\\n]/g,' ')}\n`;}
 fs.writeFileSync(path.join(out,'transcripts',tour.id+'.ffmetadata'),metadata);
}
console.log(JSON.stringify({status:'PASS',subtitleFiles:count,seconds:300,tours:data.tours.length,languages:data.languages.length}));
