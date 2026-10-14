import assert from 'node:assert/strict';
import {readFileSync,existsSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {dirname,resolve} from 'node:path';
import {SEMICONDUCTOR_SUBJECTS,renderSemiconductorVisual,semiconductorVisualFamily} from '../public/academy/semiconductor-visuals.js';
import {learningMediaMarkup,photoContextCaption} from '../public/academy/learning-media.js';
const root=resolve(dirname(fileURLToPath(import.meta.url)),'..');
const catalog=JSON.parse(readFileSync(resolve(root,'public/academy/data/catalog.json')));
const ids=catalog.filter(c=>c.category==='semiconductor').map(c=>c.id).sort();
assert.deepEqual(Object.keys(SEMICONDUCTOR_SUBJECTS).sort(),ids);
assert.equal(ids.length,99);assert.equal(renderSemiconductorVisual('unknown'), '');
const svgs=[];const shapes=new Set();
for(const id of ids){for(const zh of [true,false])for(const mode of ['full','compact']){
  const svg=renderSemiconductorVisual(id,{zh,mode});svgs.push(svg);
  assert(svg.includes('data-original="true"'));assert(svg.includes(`<title>${zh?SEMICONDUCTOR_SUBJECTS[id].title:SEMICONDUCTOR_SUBJECTS[id].titleEn}</title>`));
  assert(!/<(?:script|iframe|image|foreignObject)\b|\bon\w+=|https?:|NaN|undefined/.test(svg.replace('http://www.w3.org/2000/svg','')));
  assert(svg.includes(`data-family="${semiconductorVisualFamily(id)}"`));
  if(!zh&&mode==='compact')shapes.add(svg.match(/<g data-geometry="[^"]+">(.*)<\/g>/s)[1]);
}}
assert(new Set(Object.values(SEMICONDUCTOR_SUBJECTS).map(x=>x.family)).size>=36);
assert(shapes.size>=40,'Architecturally different subjects should produce distinct shapes/labels');
assert(renderSemiconductorVisual('a042',{zh:false}).includes('Reflective imaging'));
assert(renderSemiconductorVisual('a022',{zh:false}).includes('upright fin'));
assert(renderSemiconductorVisual('a089',{zh:false}).includes('Pressure diaphragm'));
assert.notEqual(renderSemiconductorVisual('a074'),renderSemiconductorVisual('a075'));
const py=spawnSync('python',['-c','import json,sys,xml.etree.ElementTree as E\nfor s in json.load(sys.stdin): E.fromstring(s)\nprint("SVG XML parsed")'],{input:JSON.stringify(svgs),encoding:'utf8'});assert.equal(py.status,0,py.stderr);
const media=JSON.parse(readFileSync(resolve(root,'tools/semiconductor-v8/media.json')));assert.equal(media.photos.length,24);
const urls=new Set(),hashes=new Set(),videos=new Set();let bytes=0;
for(const p of media.photos){
 for(const field of ['id','title','titleEn','author','license','licenseUrl','sourceUrl','note','noteEn','path','sha256','verifiedAt'])assert(p[field],p.id+' '+field);
 assert(!urls.has(p.sourceUrl),'Repeated source photo');urls.add(p.sourceUrl);
 assert(!hashes.has(p.sha256),'Repeated image bytes');hashes.add(p.sha256);
 const file=resolve(root,'public/academy',p.path);assert(existsSync(file));const data=readFileSync(file);bytes+=data.length;
 assert.equal(createHash('sha256').update(data).digest('hex'),p.sha256);assert.equal(data.readUInt16BE(0),0xffd8);
 assert(p.courseIds.length);for(const c of p.courseIds)assert(ids.includes(c),c);
 assert(/^CC BY|^CC0|^Public domain/.test(p.license));
 for(const [id,context] of Object.entries(p.courseContext||{})){assert(p.courseIds.includes(id));assert(context.note&&context.noteEn);assert.equal(photoContextCaption(p,id,false),context.noteEn);}
}
assert(bytes<10*1024*1024);
const combinedPhotos=[...JSON.parse(readFileSync(resolve(root,'public/academy/data/photos.json'))),...media.photos];
const photoCovered=ids.filter(id=>combinedPhotos.some(p=>p.courseIds?.includes(id)));
assert.equal(photoCovered.length,99,'Every semiconductor course has an explicitly mapped contextual image');
for(const id of ids)assert(learningMediaMarkup({id},{photos:combinedPhotos}).includes('media-photo-gallery'),id+' mapped photos render in the gallery');
for(const c of media.courses){assert(ids.includes(c.courseId));for(const v of c.videos){videos.add(v.youtubeId);assert(/^[\w-]{11}$/.test(v.youtubeId));assert.equal(v.verification.playbackTested,false);assert.equal(v.verification.oembedVerified,true);assert(v.before&&v.beforeEn&&v.after&&v.afterEn&&v.scope&&v.scopeEn);assert(v.watchFor.length===v.watchForEn.length);assert.equal(v.embedUrl,'https://www.youtube-nocookie.com/embed/'+v.youtubeId);}for(const g of c.guides){assert(g.simulationOnly);for(const a of ['procedure','evidence','pitfalls'])assert.equal(g[a].length,g[a+'En'].length);}}
assert.equal(videos.size,6);
console.log(JSON.stringify({ok:true,courses:ids.length,geometryFamilies:36,distinctEnglishGeometries:shapes.size,svgXmlDocuments:svgs.length,verifiedBundledPhotos:24,photoBytes:bytes,coursesWithContextualPhoto:photoCovered.length,uniqueVideoMetadata:videos.size,videoCourseMappings:media.courses.length,actualVideoPlaybackTested:false}));
