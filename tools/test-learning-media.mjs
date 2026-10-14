import assert from 'node:assert/strict';
import {assertRenderedData} from './assert-rendered-data.mjs';
import fs from 'node:fs';
import vm from 'node:vm';
import {setLearningMedia,learningMediaMarkup,bindLearningMedia,disposeLearningMedia,createVideoChannel,safeEmbedUrl,safeMediaLink,safeNativeVideoUrl,safeVideoPlayerUrl,HOSTED_VIDEO_PLAYER,videoPlaybackPlan,trustedVideoMessage,videoErrorMessage,safeBundledPhotoPath,photoContextCaption} from '../public/academy/learning-media.js';

for (const path of ['assets/photos/wafer-foundry.jpg','assets/photos/v6-landsat-tirs2.png','assets/v8-wafer.jpg']) assert.equal(safeBundledPhotoPath(path),path);
for (const path of ['assets/v8-x.svg','assets/v8-x.jpg?token=secret','assets/v8-x.jpg#track','assets/v8-../x.jpg','assets/photos/../private.jpg','assets/photos/%2e%2e/private.jpg','assets/photos/https://evil.test/x.jpg','//evil.test/x.jpg','https://evil.test/x.jpg','data:image/png;base64,x','assets\\photos\\x.jpg',null,{}]) assert.equal(safeBundledPhotoPath(path),'');
const contextualPhoto = {path:'assets/v8-wafer.jpg',courseIds:['photo-test'],title:'Wafer',titleEn:'Wafer',note:'一般說明',noteEn:'General caption',courseContext:{'photo-test':{note:'晶圓概觀；不是 CFET 截面。',noteEn:'Wafer overview; not a CFET cross-section.'}}};
assert.match(photoContextCaption(contextualPhoto,'photo-test',false),/not a CFET/);
assert.equal(photoContextCaption(contextualPhoto,'other',false),'General caption');
const photoMarkup=learningMediaMarkup({id:'photo-test'},{zh:false,photos:[contextualPhoto,{...contextualPhoto,path:'https://evil.test/track.jpg'},{...contextualPhoto,path:'assets/photos/../../private.jpg'}]});
assert.equal((photoMarkup.match(/<img /g)||[]).length,1,'the V8 bundled photo renders while unsafe manifest paths are rejected');
assert(photoMarkup.includes('not a CFET cross-section.'));
assert(!photoMarkup.includes('evil.test')&&!photoMarkup.includes('../../'));

assert.equal(safeEmbedUrl('https://www.youtube-nocookie.com/embed/abcdefghijk?autoplay=1'),'https://www.youtube-nocookie.com/embed/abcdefghijk?rel=0&playsinline=1');
for(const bad of ['javascript:alert(1)','https://evil.example/embed/abcdefghijk','https://www.youtube-nocookie.com.evil.example/embed/abcdefghijk','https://user:pass@www.youtube-nocookie.com/embed/abcdefghijk','https://www.youtube-nocookie.com:8443/embed/abcdefghijk','https://www.youtube-nocookie.com/embed/../../evil','http://www.youtube-nocookie.com/embed/abcdefghijk']) assert.equal(safeEmbedUrl(bad),'');
assert.equal(safeMediaLink('javascript:alert(1)'),'');
assert.equal(safeEmbedUrl('https://www.nps.gov/media/video/embed.htm?id=EE5457B1-DC6A-44C3-9EC0-3C416C15AB8D'),'https://www.nps.gov/media/video/embed.htm?id=EE5457B1-DC6A-44C3-9EC0-3C416C15AB8D');
assert.equal(safeEmbedUrl('https://www.nps.gov/media/video/embed.htm?id=javascript:alert(1)'), '');
setLearningMedia({courses:[{courseId:'test',videos:[{title:'<script>alert(1)</script>',publisher:'A & B',url:'https://example.org/video',embedUrl:'https://www.youtube-nocookie.com/embed/abcdefghijk'}],guides:[]}]});
const before=learningMediaMarkup({id:'test'});
assert(!before.includes('<iframe'),'No third-party iframe before explicit play');
assert(!before.includes('<script>'),'Metadata must be escaped');
assert(before.includes('&lt;script&gt;'));
let changed=0;const frame={innerHTML:''};const button={dataset:{videoEmbed:'https://www.youtube-nocookie.com/embed/abcdefghijk',videoTitle:'Example <title>'},closest:()=>frame};
bindLearningMedia({querySelectorAll:()=>[button]},()=>changed++);button.onclick();
assert(frame.innerHTML.includes('<iframe'));
assert(frame.innerHTML.includes('strict-origin-when-cross-origin'));
assert(frame.innerHTML.includes('allowfullscreen'));
assert(frame.innerHTML.includes('Example &lt;title&gt;'));
assert.equal(changed,1);
assert.equal(safeNativeVideoUrl('https://evil.example/video.mp4'),'');
button.dataset.videoEmbed='';button.dataset.videoFile='https://www.aidc.com.tw/avideo/AIDCenterprise_en.mp4';button.onclick();
assert(frame.innerHTML.includes('<video controls playsinline preload="none"'),'Native video must not preload large remote files');
assert(!frame.innerHTML.includes('autoplay'));

const yt='https://www.youtube-nocookie.com/embed/abcdefghijk';
const filePlan=videoPlaybackPlan(yt,{protocol:'file:',href:'file:///local/index.html'});
assert.equal(filePlan.kind,'https-wrapper');
assert.equal(new URL(filePlan.src).origin,new URL(HOSTED_VIDEO_PLAYER).origin);
assert.equal(new URL(filePlan.src).pathname,'/video-player.html');
assert.equal(new URL(filePlan.src).searchParams.get('video'),'abcdefghijk');
assert.equal(new URL(filePlan.src).searchParams.has('origin'),false,'do not fake local Referer with an origin parameter');
const hostedPlan=videoPlaybackPlan(yt,{protocol:'https:',href:'https://academy.example.test/academy/index.html'});
assert.equal(hostedPlan.kind,'direct');
assert.equal(new URL(hostedPlan.src).origin,'https://www.youtube-nocookie.com');
assert.equal(new URL(hostedPlan.src).searchParams.get('origin'),'https://academy.example.test');
assert.equal(videoPlaybackPlan('javascript:alert(1)'),null);
const customPlayer='https://learning.example.org/courses/video-player.html';
assert.equal(safeVideoPlayerUrl(customPlayer),customPlayer);
for(const bad of ['javascript:alert(1)','http://learning.example.org/video-player.html','https://user:secret@learning.example.org/video-player.html','https://learning.example.org/video-player.html?token=secret','https://learning.example.org/video-player.html#token','https://learning.example.org/anything.html']){
  assert.equal(safeVideoPlayerUrl(bad),'');
  assert.equal(new URL(videoPlaybackPlan(yt,{protocol:'file:'},{videoPlayerUrl:bad}).src).origin,new URL(HOSTED_VIDEO_PLAYER).origin,'invalid deployment URLs cannot become iframe destinations');
}
const customPlan=videoPlaybackPlan(yt,{protocol:'file:'},{videoPlayerUrl:customPlayer});
assert.equal(new URL(customPlan.src).origin,'https://learning.example.org');
assert.equal(new URL(customPlan.src).pathname,'/courses/video-player.html');
assert.match(videoErrorMessage(153,false),/website identification/);
assert.match(videoErrorMessage(101,false),/does not allow embedding/);
const channel='01234567-89ab-cdef-0123-456789abcdef', playerWindow={};
const session={channel,videoId:'abcdefghijk',source:playerWindow,origin:new URL(HOSTED_VIDEO_PLAYER).origin};
const accepted={origin:new URL(HOSTED_VIDEO_PLAYER).origin,source:playerWindow,data:{scope:'macgyver-video-v1',channel,videoId:'abcdefghijk',type:'error',code:153}};
assert.equal(trustedVideoMessage(accepted,session),true);
for(const bad of [{...accepted,origin:'https://evil.example'}, {...accepted,source:{}}, {...accepted,data:{...accepted.data,channel:'wrong'}}, {...accepted,data:{...accepted.data,videoId:'differentID'}}, {...accepted,data:{...accepted.data,code:'153'}}, {...accepted,data:{...accepted.data,type:'set-token'}}])assert.equal(trustedVideoMessage(bad,session),false,'reject untrusted player messages');
const customSession={...session,origin:'https://learning.example.org'};
assert.equal(trustedVideoMessage({...accepted,origin:customSession.origin},customSession),true);
assert.equal(trustedVideoMessage(accepted,customSession),false,'a custom deployment only accepts the origin captured for that session');

// Exercise local-parent handshake and visible error path with no network API.
const listeners=new Map(), sent=[], status={textContent:''};
let removedFrames=0,clearedTimers=0;
const iframe={contentWindow:{postMessage:(...args)=>sent.push(args)},remove(){removedFrames++}};
const localFrame={innerHTML:'',isConnected:true,classList:{add(){}},querySelector:()=>iframe};
const localButton={dataset:{videoEmbed:yt,videoTitle:'Local player',videoLanguage:'en'},closest:s=>s==='.video-card'?{querySelector:()=>status}:localFrame};
globalThis.window={location:{protocol:'file:',href:'file:///offline/index.html'},crypto:{randomUUID:()=>channel},setTimeout:()=>1,clearTimeout(){clearedTimers++},addEventListener:(type,handler)=>listeners.set(type,handler),removeEventListener(type,handler){if(listeners.get(type)===handler)listeners.delete(type)}};
const localRoot={querySelectorAll:()=>[localButton]};
const disposeLocal=bindLearningMedia(localRoot);localButton.onclick();
assert(localFrame.innerHTML.includes(HOSTED_VIDEO_PLAYER));
assert(!localFrame.innerHTML.includes('src="https://www.youtube-nocookie.com'),'local page must not directly embed YouTube');
iframe.onload();assert.equal(sent[0][1],new URL(HOSTED_VIDEO_PLAYER).origin);
const matching={...accepted,source:iframe.contentWindow};
listeners.get('message')({...matching,origin:'https://evil.example'});assert(!status.textContent.includes('153'));
listeners.get('message')(matching);assert(status.textContent.includes('153'));
// Cleanup is explicit, including after player-ready already cleared its timer;
// it cannot depend on another incoming message after navigation.
listeners.get('message')({...matching,data:{...matching.data,type:'player-ready'}});
assert.equal(listeners.size,1);disposeLearningMedia(localRoot);
assert.equal(listeners.size,0);assert.equal(removedFrames,1);assert(clearedTimers>=2);
disposeLocal();assert.equal(removedFrames,1,'the returned disposer is idempotent');
localButton.onclick();assert.equal(listeners.size,1);disposeLocal();assert.equal(listeners.size,0,'returned disposer removes later sessions from the same binding');
delete globalThis.window;

const actualRandom=Math.random;
try{Math.random=()=>0.5;const fallback=createVideoChannel({});assert(/^[A-Za-z0-9-]{20,80}$/.test(fallback),'short base36 randomness still produces a valid fixed-length channel');Math.random=()=>0;assert(/^[A-Za-z0-9-]{20,80}$/.test(createVideoChannel({})));}finally{Math.random=actualRandom;}
assert.equal(createVideoChannel({crypto:{getRandomValues:bytes=>bytes.fill(1)}}).length,32);

// A failed YouTube API load must not permanently cache rejection. Simulate an
// onerror, another explicit video click, successful API load, then disposal.
const apiScripts=[];let destroyedPlayers=0,createdPlayers=0;
const apiWindow={location:{protocol:'https:',href:'https://academy.example.test/academy/index.html'},setTimeout:()=>1,clearTimeout(){},document:{createElement:()=>({remove(){this.removed=true}}),head:{appendChild:script=>apiScripts.push(script)}}};
globalThis.window=apiWindow;
function directBinding(){const playerFrame={contentWindow:{},remove(){this.removed=true}},card={textContent:''};const frame={isConnected:true,innerHTML:'',querySelector:()=>playerFrame};const button={dataset:{videoEmbed:yt,videoLanguage:'en'},closest:s=>s==='.video-card'?{querySelector:()=>card}:frame};const root={querySelectorAll:()=>[button]};return{root,button,dispose:bindLearningMedia(root),frame:playerFrame};}
const failedBinding=directBinding();failedBinding.button.onclick();assert.equal(apiScripts.length,1);
apiScripts[0].onerror();await new Promise(resolve=>setImmediate(resolve));assert.equal(apiScripts[0].removed,true);
const retryBinding=directBinding();retryBinding.button.onclick();assert.equal(apiScripts.length,2,'a new click retries after API script failure');
apiScripts[0].onerror();
const simultaneousBinding=directBinding();simultaneousBinding.button.onclick();assert.equal(apiScripts.length,2,'an old failure cannot clear a newer in-flight API promise');
simultaneousBinding.dispose();
apiWindow.YT={Player:function(){createdPlayers++;this.destroy=()=>destroyedPlayers++}};
apiWindow.onYouTubeIframeAPIReady();await new Promise(resolve=>setImmediate(resolve));
assert.equal(createdPlayers,1,'disposed pending requests never create a player after the API arrives');
disposeLearningMedia(retryBinding.root);assert.equal(destroyedPlayers,1);assert.equal(retryBinding.frame.removed,true);
retryBinding.dispose();assert.equal(destroyedPlayers,1,'a player is destroyed only once');failedBinding.dispose();
delete globalThis.window;

// Execute the actual standalone wrapper: no third-party requests before a
// validated local-parent handshake or an explicit manual click.
const wrapperSource=fs.readFileSync(new URL('../public/academy/video-player.js',import.meta.url),'utf8');
function wrapper({protocol='https:',video='Z-E5IUozd7M',token=channel,top=false,config}={}){
  const nodes=new Map(['videoStatus','loadVideo','playerFrame','watchVideo','hostedVideo'].map(id=>[id,{textContent:'',hidden:true,replaceChildren(...children){this.children=children}}]));
  const messages=[],scripts=[],events=new Map(),players=[];
  const parent={postMessage:(data,target)=>messages.push({data,target})};
  const globals={URL,URLSearchParams,console,location:{protocol,origin:protocol==='https:'?new URL(HOSTED_VIDEO_PLAYER).origin:'null',search:'?video='+encodeURIComponent(video)+'&lang=en',hash:'#channel='+token},setTimeout:()=>1,clearTimeout(){},document:{documentElement:{},getElementById:id=>nodes.get(id),createElement:tag=>({tag}),head:{appendChild:node=>scripts.push(node)}},addEventListener:(name,fn)=>events.set(name,fn),YT:{Player:function(node,options){players.push({node,options})}}};
  globals.window=globals;globals.parent=top?globals:parent;globals.MG_CONFIG=config;
  vm.runInNewContext(fs.readFileSync(new URL('../public/academy/config.js',import.meta.url),'utf8'),globals,{filename:'config.js'});
  vm.runInNewContext(wrapperSource,globals,{filename:'video-player.js'});
  return {nodes,messages,scripts,events,players,globals,parent};
}
const wrapped=wrapper();
assert.equal(wrapped.scripts.length,0);
assert.equal(wrapped.messages[0].data.type,'ready');
const init={source:wrapped.parent,origin:'null',data:{scope:'macgyver-video-v1',type:'init',channel,videoId:'Z-E5IUozd7M'}};
for(const event of [{...init,source:{}},{...init,origin:'https://evil.example'},{...init,data:{...init.data,channel:'wrong'}},{...init,data:{...init.data,videoId:'wrong'}}])wrapped.events.get('message')(event);
assert.equal(wrapped.scripts.length,0,'untrusted commands cannot load third-party resources');
wrapped.events.get('message')(init);
assert.equal(wrapped.scripts.length,1);
const nested=wrapped.nodes.get('playerFrame').children[0];
assert.equal(nested.referrerPolicy,'strict-origin-when-cross-origin');
assert.equal(new URL(nested.src).searchParams.get('origin'),new URL(HOSTED_VIDEO_PLAYER).origin,'nested iframe uses its actual HTTPS document origin');
assert(!nested.src.includes(channel),'handshake channel is not forwarded to YouTube');
assert(!nested.src.includes('autoplay'));
wrapped.globals.onYouTubeIframeAPIReady();
wrapped.players[0].options.events.onReady();
wrapped.players[0].options.events.onError({data:153});
assert.equal(wrapped.messages.at(-1).data.code,153);
assert.match(wrapped.nodes.get('videoStatus').textContent,/website identification/);
for(const message of wrapped.messages){assert.deepEqual(Object.keys(message.data).sort(),message.data.type==='error'?['channel','code','scope','type','videoId']:['channel','scope','type','videoId']);}
const badWrapper=wrapper({video:'../../secret'});assert.equal(badWrapper.scripts.length,0);assert.equal(badWrapper.nodes.get('loadVideo').disabled,true);
const unknownWrapper=wrapper({video:'abcdefghijk'});assert.equal(unknownWrapper.scripts.length,0);assert.equal(unknownWrapper.nodes.get('loadVideo').disabled,true);assert.match(unknownWrapper.nodes.get('videoStatus').textContent,/approved public curriculum/);
const missingList=wrapper({config:{allowedYouTubeIds:[]}});assert.equal(missingList.scripts.length,0);assert.equal(missingList.nodes.get('loadVideo').disabled,true,'empty approved list fails closed');
const localWrapper=wrapper({protocol:'file:'});assert.equal(localWrapper.scripts.length,0);assert.equal(localWrapper.nodes.get('loadVideo').disabled,true);assert(localWrapper.nodes.get('hostedVideo').href.startsWith(HOSTED_VIDEO_PLAYER));
const customWrapper=wrapper({protocol:'file:',config:{videoPlayerUrl:customPlayer}});assert(customWrapper.nodes.get('hostedVideo').href.startsWith(customPlayer));assert.equal(customWrapper.globals.MG_CONFIG.googleMapsEmbedKey,'');
const unsafeWrapper=wrapper({protocol:'file:',config:{videoPlayerUrl:'https://user:secret@evil.example/video-player.html'}});assert(unsafeWrapper.nodes.get('hostedVideo').href.startsWith(HOSTED_VIDEO_PLAYER));
const standalone=wrapper({top:true});assert.equal(standalone.scripts.length,0);standalone.nodes.get('loadVideo').onclick();assert.equal(standalone.scripts.length,1);assert.equal(standalone.messages.length,0);
for(const entry of ['index.html','video-player.html']){const html=fs.readFileSync(new URL('../public/academy/'+entry,import.meta.url),'utf8');assert(html.indexOf('src="config.js"')<html.indexOf(entry==='index.html'?'src="bootstrap.js"':'src="video-player.js"'),'classic config loads before either entry point');}

const data=JSON.parse(fs.readFileSync(new URL('../public/academy/data/media.json',import.meta.url)));
const courses=JSON.parse(fs.readFileSync(new URL('../public/academy/data/featured.json',import.meta.url)));
const photos=JSON.parse(fs.readFileSync(new URL('../public/academy/data/photos.json',import.meta.url)));
assert(data.courses.length>=21 && data.courses.every(entry=>courses.some(c=>c.id===entry.courseId)));
assert.equal(new Set(data.courses.map(c=>c.courseId)).size,data.courses.length);
setLearningMedia(data);
let videos=0,embeds=0,guides=0;
for(const course of courses){
  const entry=data.courses.find(c=>c.courseId===course.id);
  const original=!/^[abcd]\d{3}$/.test(course.id)&&!course.id.startsWith('v11-');
  if(original)assert(entry,course.id);
  if(!entry){
    const html=learningMediaMarkup(course,{photos,compact:true});
    if(photos.some(p=>p.courseIds?.includes(course.id)))assert(html.includes('media-photo-gallery'),'New-course photos render even without a video entry');
    else assert.equal(html,'');
    continue;
  }
  assert(entry.videos.length+entry.guides.length>=1,`${course.id}: supporting media missing`);
  if(original){
    assert(entry.guides.length>=2,`${course.id}: deeper guides missing`);
    assert(photos.some(p=>p.courseIds?.includes(course.id)),`${course.id}: photo missing`);
  }
  for(const v of entry.videos){
    for(const key of ['title','titleEn','publisher','sourcePage'])assert(typeof v[key]==='string'&&v[key],`${course.id}: video ${key}`);
    assert(safeMediaLink(v.url));assert(safeMediaLink(v.sourcePage));
    if(v.embedUrl){assert(safeEmbedUrl(v.embedUrl),`${course.id}: unsupported embed ${v.embedUrl}`);embeds++;}
    if(v.nativeVideoUrl){assert(safeNativeVideoUrl(v.nativeVideoUrl),`${course.id}: unsupported native stream`);embeds++;}
    for(const key of ['watchFor','watchForEn'])assert(Array.isArray(v[key])&&v[key].length>=2,`${course.id}: observation prompts`);
    videos++;
  }
  for(const g of entry.guides){
    for(const key of ['title','titleEn','concept','conceptEn'])assert(typeof g[key]==='string'&&g[key],`${course.id}: guide ${key}`);
    for(const key of ['procedure','procedureEn','pitfalls','pitfallsEn'])assert(Array.isArray(g[key])&&g[key].length,`${course.id}: guide ${key}`);
    assert(g.sources?.length);for(const source of g.sources)assert(safeMediaLink(source.url));guides++;
  }
  for(const zh of [true,false]){
    const html=learningMediaMarkup(course,{zh,photos,step:course.stages[0].steps[0],compact:true});
    assertRenderedData(html,`${course.id}: media`);
    assert(!html.includes('<iframe'),'No external media fetched on render');
    assert(html.includes('media-library'));
  }
}
console.log(`Learning media PASS: ${courses.length} courses, ${videos} videos (${embeds} embedded), ${guides} guides; bilingual render, explicit-load, file/HTTPS routing, real-origin parameters, wrapper handshake/source/origin/nonce/ID validation, error153, manual fallback and URL checks. No live playback claim.`);
