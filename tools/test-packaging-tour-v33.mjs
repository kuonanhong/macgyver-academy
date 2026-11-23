#!/usr/bin/env node
/** Content and timeline checks; no browser, GPU or network is simulated as verified. */
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import {fileURLToPath} from 'node:url';

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const dir=path.join(root,'public/academy');
const contentCode=fs.readFileSync(path.join(dir,'packaging-tour-content-v33.js'),'utf8');
const playerCode=fs.readFileSync(path.join(dir,'packaging-tour-v33.js'),'utf8');
const dataSandbox={window:{}};
vm.runInNewContext(contentCode,dataSandbox,{filename:'packaging-tour-content-v33.js'});
const data=dataSandbox.window.MACGYVER_PACKAGING_TOURS;
const ids=['interposer','fanout','hybrid','bridge','chiplet','thermal'];
const languages=['zh-TW','zh-CN','en','ja','ko'];
assert.deepEqual([...data.tours.map(t=>t.id)].sort(),[...ids].sort(),'All six distinct films must exist');
assert.deepEqual([...data.languages.map(l=>l.id)].sort(),[...languages].sort(),'All five complete subtitle languages must exist');
assert.equal(data.duration,300);

const officialHosts=new Set(['3dfabric.tsmc.com','www.tsmc.com','www.intel.com','ase.aseglobal.com','www.uciexpress.org']);
const topics={
  interposer:[/interposer/i,/HBM/,/through.silicon|TSV/i],
  fanout:[/redistribution|RDL/i,/mold/i,/warpage|warp/i],
  hybrid:[/copper/i,/dielectric/i,/align|planar|clean/i],
  bridge:[/bridge/i,/local/i,/substrate/i],
  chiplet:[/UCIe/i,/protocol/i,/test|validat/i],
  thermal:[/thermal|heat/i,/interface/i,/reliab|cycling/i]
};
const texts=new Map(languages.map(lang=>[lang,new Set()]));
let chapterCount=0,translationCount=0;
for(const tour of data.tours){
  assert.equal(tour.duration,300,`${tour.id}: five minutes`);
  assert.equal(tour.chapters.length,10,`${tour.id}: ten substantive chapters`);
  assert.ok(tour.sources.length>=2,`${tour.id}: technical sources`);
  for(const source of tour.sources){
    const u=new URL(source.url);
    assert.equal(u.protocol,'https:');
    assert.ok(officialHosts.has(u.hostname),`Non-primary source: ${source.url}`);
    assert.equal(u.username+u.password,'');
    assert.ok(source.title.trim().length>8);
  }
  for(const lang of languages){
    assert.ok(tour.title[lang]?.trim().length>2,`${tour.id}/${lang}: title`);
    assert.ok(tour.summary[lang]?.trim().length>20,`${tour.id}/${lang}: summary`);
  }
  for(let i=0;i<tour.chapters.length;i++){
    const c=tour.chapters[i];chapterCount++;
    assert.equal(c.start,i*30,`${tour.id}/${i}: no missing or overlapping chapter time`);
    assert.equal(c.end,(i+1)*30);
    assert.ok(c.view&&typeof c.view==='string');
    for(const lang of languages){
      const s=c.text[lang]?.trim();
      assert.ok(s&&s.length>45,`${tour.id}/${i}/${lang}: complete explanation, not a placeholder`);
      assert.ok(!/\b(?:TODO|TBD|lorem ipsum)\b|待補|翻譯中/i.test(s));
      assert.ok(c.title[lang]?.trim().length>2,`${tour.id}/${i}/${lang}: chapter title`);
      assert.ok(!texts.get(lang).has(s),`${tour.id}/${i}/${lang}: duplicate chapter prose`);
      texts.get(lang).add(s);translationCount++;
      if(lang.startsWith('zh'))assert.match(s,/[\u4e00-\u9fff]/);
      if(lang==='ja')assert.match(s,/[\u3040-\u30ff]/);
      if(lang==='ko')assert.match(s,/[\uac00-\ud7af]/);
    }
  }
  const en=tour.chapters.map(c=>c.text.en).join(' ');
  for(const concept of topics[tour.id])assert.match(en,concept,`${tour.id}: technique-specific explanation`);
}

// A minimal DOM permits loading the actual player and calling its exported cue
// functions. It does not pretend to test WebGL, real media playback, or layout.
class Element {
  constructor(tag='div') {this.tagName=tag.toUpperCase();this.children=[];this.dataset={};this.style={};this.attributes={};this.textContent='';this.hidden=false;this.open=false;this.clientWidth=1280;this.clientHeight=720;this.offsetWidth=120;this.offsetHeight=24;this.classList={add(){},remove(){},toggle(){},contains(){return false;}};}
  append(...nodes){this.children.push(...nodes);}
  replaceChildren(...nodes){this.children=[...nodes];}
  setAttribute(k,v){this.attributes[k]=v;}
  getAttribute(k){return this.attributes[k];}
  addEventListener(){}
  remove(){}
  click(){return this.onclick?.();}
  pause(){}
  play(){return Promise.resolve();}
  showModal(){this.open=true;}
  close(){this.open=false;}
  getBoundingClientRect(){return {width:1280,height:720,top:0,left:0};}
}
function loadPlayer({lang='en',webgl=true,speech=true}={}){
  const nodes=new Map();const get=id=>{if(!nodes.has(id))nodes.set(id,new Element());return nodes.get(id);};
  const engine={setTour(){},render(){},resize(){},getLabels(){return [];},getState(){return {webgl:true};}};
  const document={getElementById:get,createElement:tag=>new Element(tag),createTextNode:text=>({textContent:text}),querySelectorAll:()=>[],documentElement:new Element('html'),body:new Element('body'),fonts:{ready:Promise.resolve()},addEventListener(){}};
  const window={MACGYVER_PACKAGING_TOURS:data,MG_PACKAGING_SCENE:{create(){if(!webgl)throw Error('WebGL intentionally unavailable');return engine;}},addEventListener(){}};
  const sandbox={window,document,URL,URLSearchParams,Intl,Map,Set,Blob,performance:{now:()=>0},location:{search:'?lang='+lang,href:'https://example.test/packaging-tour-v33.html?lang='+lang,hostname:'example.test'},history:{replaceState(){}},navigator:{language:'en-US',languages:['en-US']},localStorage:{getItem(){return null;},setItem(){}},devicePixelRatio:1,ResizeObserver:class{observe(){}},requestAnimationFrame(){},setTimeout(){return 1;},clearTimeout(){},console:{error(){}}};
  if(speech){sandbox.speechSynthesis=window.speechSynthesis={cancel(){},getVoices(){return [];}};}
  vm.runInNewContext(playerCode,sandbox,{filename:'packaging-tour-v33.js'});
  assert.ok(window.MG_PACKAGING_TOUR,'Player boot must finish');
  return {api:window.MG_PACKAGING_TOUR,nodes,get,window,document};
}
const player=loadPlayer();let cueCount=0,vttCount=0;
const parseTimestamp=s=>{const [h,m,sec]=s.split(':').map(Number);return h*3600+m*60+sec;};
for(const tour of data.tours)for(const lang of languages){
  const cues=player.api.cuesFor(tour,lang);let previous=0;
  assert.ok(cues.length>=tour.chapters.length);
  for(const cue of cues){
    assert.ok(Math.abs(cue.start-previous)<1e-7,`${tour.id}/${lang}: cue gap or overlap at ${previous}`);
    assert.ok(cue.end>cue.start&&cue.end<=300);
    assert.ok(cue.text.trim());previous=cue.end;cueCount++;
  }
  assert.equal(previous,300);
  const normalize=s=>s.replace(/\s/g,'');
  assert.equal(normalize(cues.map(c=>c.text).join('')),normalize(tour.chapters.map(c=>c.text[lang]).join('')),`${tour.id}/${lang}: subtitles must retain every narration character`);
  const vtt=player.api.vttFor(tour,lang);assert.ok(vtt.startsWith('WEBVTT\n\n'));
  const times=[...vtt.matchAll(/^(\d\d:\d\d:\d\d\.\d{3}) --> (\d\d:\d\d:\d\d\.\d{3})$/gm)];
  assert.equal(times.length,cues.length);previous=0;
  for(const [,start,end] of times){assert.equal(parseTimestamp(start),previous);assert.ok(parseTimestamp(end)>previous);previous=parseTimestamp(end);}
  assert.equal(previous,300,`${tour.id}/${lang}: downloadable VTT must end at exactly 05:00`);vttCount++;
}
// Exact end seeks must show the final chapter and final subtitle, and replay
// must reset the timeline. This boundary commonly fails with floor(300/30).
player.get('timeline').oninput({target:{value:'300'}});
assert.equal(player.api.state().time,300);
assert.equal(player.get('chapter-number').textContent,'10 / 10');
assert.equal(player.get('play').textContent,'Replay');
assert.equal(player.get('subtitle').textContent,player.api.cuesFor(data.tours[0],'en').at(-1).text);
await player.get('play').onclick();assert.equal(player.api.state().time,0);
for(const lang of languages){player.get('language').onchange({target:{value:lang}});assert.equal(player.document.documentElement.lang,lang);assert.equal(player.get('subtitle').textContent,player.api.cuesFor(data.tours[0],lang)[0].text);}
// Browsers without either WebGL or speech must still initialize the MP4 path.
const fallback=loadPlayer({webgl:false,speech:false});
assert.equal(fallback.api.state().video,true);
assert.equal(fallback.get('fallback-video').hidden,false);
fallback.get('timeline').oninput({target:{value:'300'}});
assert.equal(fallback.api.state().time,300);
assert.ok(fallback.get('fallback-video').src.endsWith('/interposer.mp4'));
await fallback.get('downloads').onclick();
const modeButton=fallback.get('dialog-content').children.flatMap(n=>n.children||[]).find(n=>n.textContent==='Return to 3D tour');
assert.ok(modeButton?.disabled,'Do not offer an unavailable 3D renderer on the video fallback path');
modeButton.onclick();assert.equal(fallback.api.state().video,true,'An unavailable renderer must never hide the working video');
console.log(JSON.stringify({status:'PASS',tours:ids.length,languages:languages.length,chapters:chapterCount,chapterTranslations:translationCount,cues:cueCount,vttTracks:vttCount,secondsPerTrack:300,endSeekReplay:'PASS',languageSwitch:'PASS',noWebGLNoSpeechInitialization:'PASS',unavailable3DGuard:'PASS',limits:['No GPU rendering, codec execution, actual media playback, or responsive layout verified by this test.']},null,2));
