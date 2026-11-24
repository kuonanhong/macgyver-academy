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
  removeAttribute(k){delete this.attributes[k];delete this[k];}
  addEventListener(){}
  remove(){}
  click(){return this.onclick?.();}
  pause(){this.paused=true;}
  play(){this.paused=false;return Promise.resolve();}
  showModal(){this.open=true;}
  close(){this.open=false;}
  getBoundingClientRect(){return this.rect||{width:1280,height:720,top:0,left:0,bottom:720,right:1280};}
}
function loadPlayer({lang='en',webgl=true,speech=true,youtube={},narration={},captions={}}={}){
  const nodes=new Map();const get=id=>{if(!nodes.has(id))nodes.set(id,new Element());return nodes.get(id);};
  get('caption').rect={width:1180,height:100,top:600,left:30,bottom:700,right:1210};get('line-qr-image').complete=true;get('line-qr-image').naturalWidth=410;get('line-qr-image').decode=()=>Promise.resolve();
  const engine={setTour(){},render(){},resize(){},getLabels(){return [];},getState(){return {webgl:true};}};
  const document={getElementById:get,createElement:tag=>new Element(tag),createTextNode:text=>({textContent:text}),querySelectorAll:()=>[],documentElement:new Element('html'),body:new Element('body'),fonts:{ready:Promise.resolve()},addEventListener(){}};
  const window={MACGYVER_PACKAGING_TOURS:data,MACGYVER_PACKAGING_YOUTUBE:youtube,MACGYVER_PACKAGING_NARRATION:narration,MACGYVER_PACKAGING_CAPTIONS:captions,MG_PACKAGING_SCENE:{create(){if(!webgl)throw Error('WebGL intentionally unavailable');return engine;}},addEventListener(){}};
  const sandbox={window,document,URL,URLSearchParams,Intl,Map,Set,Blob,performance:{now:()=>0},location:{search:'?lang='+lang,href:'https://example.test/packaging-tour-v33.html?lang='+lang,hostname:'example.test'},history:{replaceState(){}},navigator:{language:'en-US',languages:['en-US']},localStorage:{getItem(){return null;},setItem(){}},devicePixelRatio:1,ResizeObserver:class{observe(){}},requestAnimationFrame(){},setTimeout(){return 1;},clearTimeout(){},console:{error(){}}};
  if(speech){sandbox.speechSynthesis=window.speechSynthesis={cancel(){},getVoices(){return [];}};}
  const instrumented=playerCode.replace(' window.MG_PACKAGING_TOUR=', ' window.__PACKAGING_TEST={paintFilm,paintLineCard,ensureLineQr};\n window.MG_PACKAGING_TOUR=');
  vm.runInNewContext(instrumented,sandbox,{filename:'packaging-tour-v33.js'});
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
assert.ok(fallback.get('fallback-video').src.endsWith('/interposer.mp4?v=33.0.3'));
await fallback.get('downloads').onclick();
const modeButton=fallback.get('dialog-content').children.flatMap(n=>n.children||[]).find(n=>n.textContent==='Return to 3D tour');
assert.ok(modeButton?.disabled,'Do not offer an unavailable 3D renderer on the video fallback path');
modeButton.onclick();assert.equal(fallback.api.state().video,true,'An unavailable renderer must never hide the working video');
// Real player functions, minimal DOM: no public links until IDs are verified.
const blank=loadPlayer();assert.equal(blank.get('youtube-playlist').hidden,true);assert.equal(blank.get('youtube-video').hidden,true);
assert.equal(blank.get('full-lesson-link').hidden,true);assert.equal(blank.get('full-lesson-pending').hidden,false);
const longReady=loadPlayer({youtube:{longVideos:[{tour:'interposer',videoId:'abc123DEF_0',status:'verified'}]}});
assert.equal(longReady.get('full-lesson-link').hidden,false);assert.equal(longReady.get('full-lesson-pending').hidden,true);
const longDraft=loadPlayer({youtube:{longVideos:[{tour:'interposer',videoId:'abc123DEF_0',status:'draft'}]}});
assert.equal(longDraft.get('full-lesson-link').hidden,true);
const linked=loadPlayer({youtube:{playlistId:'PL0123456789abcdefghijklmnopqrstuv',videos:[{tour:'interposer',videoId:'abc123DEF_0'}]}});
assert.equal(linked.get('youtube-playlist').hidden,false);assert.equal(linked.get('youtube-video').hidden,false);
assert.equal(new URL(linked.get('youtube-video').href).searchParams.get('v'),'abc123DEF_0');
linked.get('tours').children.find(n=>n.dataset.tour==='fanout').onclick();assert.equal(linked.get('youtube-video').hidden,true);assert.equal(linked.get('youtube-playlist').hidden,false);
const unsafe=loadPlayer({youtube:{playlistId:'javascript:alert(1)',videos:[{tour:'interposer',videoId:'" onclick="alert(1)'}]}});assert.equal(unsafe.get('youtube-video').hidden,true);assert.equal(unsafe.get('youtube-playlist').hidden,true);
// The final ten seconds show a join link above subtitles. Earlier frames and
// already-burned video playback must not show a duplicate card.
for(const [time,visible] of [[0,false],[289.999,false],[290,true],[299.96,true],[300,true]]){blank.get('timeline').oninput({target:{value:String(time)}});assert.equal(blank.get('line-endcard').hidden,!visible);}
assert.equal(blank.get('line-endcard').href,'https://line.me/R/ti/p/%40530pgchc');assert.equal(blank.get('line-endcard').style.bottom,'132px');
for(const lang of languages){blank.get('language').onchange({target:{value:lang}});assert.ok(blank.get('line-account-name').textContent.length>3);assert.ok(blank.get('line-join').textContent.length>3);assert.ok(blank.get('youtube-playlist').textContent.includes('YouTube'));}
fallback.get('timeline').oninput({target:{value:'295'}});assert.equal(fallback.get('line-endcard').hidden,true);
const calls=[];const context={save(){},restore(){},fillRect(...args){calls.push({kind:'rect',args});},drawImage(...args){calls.push({kind:'image',args});},fillText(...args){calls.push({kind:'text',args});},measureText(s){return {width:[...s].length*8};},createLinearGradient(){return {addColorStop(){}};}};
for(const lang of languages){for(const t of [289.96,290,299.96]){calls.length=0;blank.window.__PACKAGING_TEST.paintFilm(context,{width:1280,height:720},t,lang,true);const qr=calls.filter(c=>c.kind==='image'&&c.args[0]===blank.get('line-qr-image'));assert.equal(qr.length,t>=290?1:0);if(t>=290){assert.ok(qr[0].args[2]+qr[0].args[4]<720-109,'QR above the subtitle band');assert.ok(calls.some(c=>c.kind==='text'&&c.args[0]==='@530pgchc'));}}}
await blank.window.__PACKAGING_TEST.ensureLineQr();blank.get('line-qr-image').naturalWidth=0;await assert.rejects(blank.window.__PACKAGING_TEST.ensureLineQr(),e=>e.code==='QR_UNAVAILABLE');
// Recorded audio follows seeks, language changes and pause, without relying on
// OS speech voices. Semantic English comes from the selected-language cue.
const spoken=loadPlayer({lang:'zh-TW',speech:false,narration:{tours:{interposer:{'zh-TW':{file:'assets/packaging-tour-v33/audio/interposer.zh-TW.m4a'},en:{file:'assets/packaging-tour-v33/audio/interposer.en.m4a'}}}},captions:{tours:{interposer:{'zh-TW':[{start:0,end:300,text:'封裝測試',english:'Packaging test'}],en:[{start:0,end:300,text:'Packaging test',english:''}]}}}});
assert.equal(spoken.api.state().bilingual,true);
assert.equal(spoken.api.state().voice,true);
assert.equal(spoken.get('secondary-subtitle').textContent,'Packaging test');
await spoken.get('play').onclick();assert.equal(spoken.get('narration').paused,false);
spoken.get('timeline').oninput({target:{value:'120'}});assert.equal(spoken.get('narration').currentTime,120);
await spoken.get('language').onchange({target:{value:'en'}});
assert.ok(spoken.get('narration').src.includes('interposer.en.m4a'));assert.equal(spoken.get('narration').currentTime,120);assert.equal(spoken.get('secondary-subtitle').hidden,true);
await spoken.get('voice').onclick();assert.equal(spoken.get('narration').paused,true);
await spoken.get('voice').onclick();assert.equal(spoken.get('narration').paused,false);
await spoken.get('play').onclick();assert.equal(spoken.get('narration').paused,true);
// A delayed play promise from an old language must not stop the new language.
let resolveOld;spoken.get('narration').play=function(){this.paused=false;return new Promise(resolve=>{resolveOld=resolve;});};
const oldPlay=spoken.get('play').onclick();
spoken.get('narration').play=function(){this.paused=false;return Promise.resolve();};
await spoken.get('language').onchange({target:{value:'zh-TW'}});resolveOld();await oldPlay;
assert.equal(spoken.get('narration').paused,false,'Stale play completion must not pause new-language audio');
spoken.get('narration').onended();assert.equal(spoken.api.state().time,300);assert.equal(spoken.api.state().playing,false);
console.log(JSON.stringify({recordedAudioControls:'PASS',staleAudioPlayGuard:'PASS',status:'PASS',tours:ids.length,languages:languages.length,chapters:chapterCount,chapterTranslations:translationCount,cues:cueCount,vttTracks:vttCount,secondsPerTrack:300,endSeekReplay:'PASS',languageSwitch:'PASS',noWebGLNoSpeechInitialization:'PASS',unavailable3DGuard:'PASS',verifiedYouTubeLinks:'PASS',lineQrBoundaryAndNoVideoDuplicate:'PASS',localizedExportQr:'PASS',missingQrExportGuard:'PASS',limits:['No GPU rendering, codec execution, actual media playback, or responsive layout verified by this test.']},null,2));
