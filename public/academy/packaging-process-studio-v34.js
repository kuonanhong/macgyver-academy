/* C01 production rehearsal and video-only master encoder. Actual narration is
 * generated and timed separately; this page never claims to contain final audio.
 */
(() => {
  'use strict';
  const D=window.MACGYVER_PACKAGING_C01,$=id=>document.getElementById(id);
  const film=$('film'),ctx=film.getContext('2d'),sceneCanvas=$('scene');
  const params=new URLSearchParams(location.search);
  const state={time:Math.max(0,Math.min(300,Number(params.get('t'))||0)),lang:params.get('lang')==='en'?'en':'zh-TW',playing:false,rendering:false,cancel:false,frame:0};
  let engine,last=0,localSink=false;
  const text=(zh,en)=>state.lang==='en'?en:zh;
  const clock=t=>String(Math.floor(t/60)).padStart(2,'0')+':'+String(Math.floor(t%60)).padStart(2,'0');
  const chapter=t=>D.cues[Math.min(9,Math.floor(Math.max(0,t)/30))];
  const previewCues={};
  for(const lang of D.languages){previewCues[lang]=D.cues.flatMap(c=>{
    const parts=[...new Intl.Segmenter(lang,{granularity:'sentence'}).segment(c.text[lang])].map(s=>s.segment.trim()).filter(Boolean),total=parts.reduce((n,s)=>n+s.length,0);let offset=0;
    return parts.map(s=>{const start=c.start+30*offset/total;offset+=s.length;return {start,end:c.start+30*offset/total,text:s};});
  });}
  function wrap(content,maxWidth){const chars=[...content],rows=[];let line='';for(const char of chars){if(line&&ctx.measureText(line+char).width>maxWidth){rows.push(line);line=char.trimStart();}else line+=char;}if(line)rows.push(line);return rows;}
  function paintQr(t){if(t<290)return;const qr=$('line-qr');if(!qr.complete||!qr.naturalWidth)return;const x=1052,y=287,w=200,h=260;ctx.fillStyle='#fff';ctx.fillRect(x,y,w,h);ctx.drawImage(qr,x+18,y+12,164,164);ctx.fillStyle='#163529';ctx.font='600 14px system-ui';ctx.fillText(text('郭南宏官方帳號','Kuo Nan-Hong · Official'),x+12,y+187);ctx.font='600 19px monospace';ctx.fillText('@530pgchc',x+12,y+212);ctx.font='12px system-ui';ctx.fillText(text('掃描加入 LINE','Scan to join LINE'),x+12,y+240);}
  function render(t=state.time,{master=false}={}){
    if(!engine)return;state.time=Math.max(0,Math.min(300,t));engine.render(state.time);ctx.drawImage(sceneCanvas,0,0,1280,720);const c=chapter(state.time);
    const grad=ctx.createLinearGradient(0,0,0,145);grad.addColorStop(0,'#07101cf2');grad.addColorStop(1,'#07101c00');ctx.fillStyle=grad;ctx.fillRect(0,0,1280,145);ctx.textAlign='left';ctx.textBaseline='top';ctx.font='600 13px system-ui';ctx.fillStyle='#efbe80';ctx.fillText('MACGYVER / C01 / REQUIREMENTS ENGINEERING',32,23);ctx.font='500 25px system-ui';ctx.fillStyle='#e7f0f7';ctx.fillText(D.title[state.lang],32,48);ctx.font='12px system-ui';ctx.fillStyle='#afc1d2';ctx.fillText(text('教學重建・案例數值為假設・非工廠實拍','Teaching reconstruction · hypothetical values · not factory footage'),32,83);ctx.textAlign='right';ctx.fillStyle='#efbe80';ctx.fillText(clock(state.time)+' / 05:00',1248,25);ctx.textAlign='left';
    const occupied=[];ctx.font='13px system-ui';for(const label of engine.getLabels()){
      if(!label.visible||label.x<100||label.x>1180||label.y<150||label.y>500||state.time>=290&&label.x>1000)continue;
      const s=state.lang==='en'?label.en:label.zh,w=ctx.measureText(s).width+20,x=label.x-w/2,y=label.y-23;
      if(x<20||x+w>1260||occupied.some(a=>x<a.x+a.w&&x+w>a.x&&Math.abs(y-a.y)<28))continue;occupied.push({x,y,w});ctx.fillStyle='#071321e0';ctx.fillRect(x,y,w,25);ctx.fillStyle='#ccebe3';ctx.fillText(s,x+10,y+5);
    }
    // Short quantitative cards are separate from the final subtitle region.
    ctx.fillStyle='#0a1726e5';ctx.fillRect(32,510,930,54);ctx.font='500 15px system-ui';ctx.fillStyle='#f1c58f';
    c.shot.overlay[state.lang].slice(0,2).forEach((s,i)=>ctx.fillText(s,46,520+i*21));
    ctx.fillStyle='#07101cf5';ctx.fillRect(0,584,1280,136);ctx.fillStyle='#efbe80';ctx.fillRect(32,601,3,90);ctx.font='500 17px system-ui';ctx.fillText(`${String(Math.min(10,Math.floor(state.time/30)+1)).padStart(2,'0')}  ${c.title[state.lang]}`,48,599);
    if(!master){const cue=previewCues[state.lang].find(s=>state.time>=s.start&&state.time<s.end)||previewCues[state.lang].at(-1);ctx.font='20px system-ui';ctx.fillStyle='#e3edf6';wrap(cue.text,1180).slice(0,3).forEach((s,i)=>ctx.fillText(s,48,631+i*25));}
    ctx.fillStyle='#283a4a';ctx.fillRect(0,717,1280,3);ctx.fillStyle='#a9e2d3';ctx.fillRect(0,717,1280*state.time/300,3);paintQr(state.time);
    $('clock').textContent=clock(state.time)+' / 05:00';$('timeline').value=String(state.time);
    [...$('chapters').children].forEach((button,i)=>button.setAttribute('aria-current',String(i===Math.min(9,Math.floor(state.time/30)))));
    return film;
  }
  function refresh(){
    document.documentElement.lang=state.lang;$('language').value=state.lang;$('title').textContent='C01 · '+D.title[state.lang];
    $('intro').textContent=text('五分鐘設計活動。原創教學重建；數值為假設案例，並非廠商產品規格或實測。此頁為無聲母片製作預覽；預覽字幕依文字估時，並非已實測語音字幕。','A five-minute design activity using original teaching geometry and hypothetical numbers. This is a silent master rehearsal; preview captions are estimated from text, not measured narration timings.');
    $('play').textContent=state.playing?text('暫停','Pause'):text('播放預覽','Play preview');$('fullscreen').textContent=text('全螢幕','Full screen');$('render').textContent=text('製作 C01 無聲母片','Render C01 silent master');$('cancel').textContent=text('取消','Cancel');
    $('production-note').textContent=text('匯出 1280×720、24fps、300 秒的無聲母片，保留字幕區並包含最後 10 秒 LINE QR。旁白、精準句子字幕與最終影片由後續製作步驟合成，這個匯出本身不是完整有聲影片。','Export a 1280×720, 24fps, 300-second silent master with subtitle space and a LINE QR in the last ten seconds. Recorded narration, measured sentence captions and the final film are assembled separately. This export alone is not the completed narrated film.');
    $('chapters').replaceChildren();$('transcript').replaceChildren();
    D.cues.forEach((cue,i)=>{const button=document.createElement('button');button.textContent=`${String(i+1).padStart(2,'0')}  ${cue.title[state.lang]}`;button.onclick=()=>seek(cue.start);$('chapters').append(button);const article=document.createElement('article'),title=document.createElement('h3');title.textContent=clock(cue.start)+' '+cue.title[state.lang];article.append(title);for(const lang of [state.lang,state.lang==='en'?'zh-TW':'en']){const p=document.createElement('p');p.lang=lang;p.textContent=cue.text[lang];article.append(p);}$('transcript').append(article);});
    $('sources').replaceChildren();D.sources.forEach(source=>{const p=document.createElement('p'),a=document.createElement('a');a.href=source.url;a.target='_blank';a.rel='noopener noreferrer';a.textContent=source.publisher+' · '+source.title;p.append(a);$('sources').append(p);});render();
  }
  function seek(t){if(state.rendering)return;state.playing=false;state.time=Math.max(0,Math.min(300,Number(t)||0));refresh();}
  async function report(value){if(!localSink)return;const r=await fetch('/__process_studio/progress',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(value)});if(!r.ok)throw Error('Local progress receiver rejected request: '+r.status);}
  function download(blob,name){const a=document.createElement('a'),url=URL.createObjectURL(blob);a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),60000);}
  async function exportMaster(){
    if(state.rendering)return;state.playing=false;state.rendering=true;state.cancel=false;state.frame=0;
    const savedLanguage=state.lang,savedTime=state.time;state.lang='en';refresh();$('render').disabled=true;$('play').disabled=true;$('language').disabled=true;$('cancel').hidden=false;
    let output;try{
      if(!engine||!('VideoEncoder' in window))throw Error('WebGL and WebCodecs are required; use current Chrome or Edge.');
      await $('line-qr').decode();if(!$('line-qr').naturalWidth)throw Error('LINE QR image is unavailable.');await document.fonts.ready;
      try{const response=await fetch('/__process_studio/status');localSink=response.ok&&(await response.json()).enabled===true;}catch{localSink=false;}
      const {Output,Mp4OutputFormat,BufferTarget,CanvasSource,Quality}=await import('./vendor/mediabunny/mediabunny-1.66.2.min.mjs');
      const target=new BufferTarget();output=new Output({format:new Mp4OutputFormat({fastStart:'in-memory'}),target});
      const source=new CanvasSource(film,{codec:'avc',quality:new Quality({bitrate:1200000}),keyFrameInterval:2,latencyMode:'quality'});output.addVideoTrack(source,{frameRate:24});output.setMetadataTags({title:'C01 - Define system and package requirements - silent production master',artist:'MacGyver Engineering Academy',comment:'Original ten-scene teaching reconstruction. Hypothetical worked examples; not vendor CAD, factory footage or measured simulation. Narration and subtitles are separate production assets.'});
      await output.start();await report({state:'rendering',frame:0,totalFrames:7200,processId:'C01'});
      for(let f=0;f<7200;f++){
        if(state.cancel)throw Error('CANCELLED');render(f/24,{master:true});await source.add(f/24,1/24);state.frame=f+1;
        if(f%24===0){$('progress').value=f+1;$('status').textContent=`Rendering C01 · ${f+1} / 7,200 frames · ${Math.floor(f/72)}%`;if(f%120===0)await report({state:'rendering',frame:f+1,totalFrames:7200,processId:'C01'});await new Promise(resolve=>setTimeout(resolve,0));}
      }
      await output.finalize();output=null;const blob=new Blob([target.buffer],{type:'video/mp4'});$('status').textContent='Saving C01.master.mp4…';
      if(localSink){const response=await fetch('/__process_studio/video/C01',{method:'POST',headers:{'Content-Type':'video/mp4'},body:blob});if(!response.ok)throw Error('Local video save failed: '+response.status);}else download(blob,'C01.master.mp4');
      $('progress').value=7200;$('status').textContent=`Silent master complete · 7,200 frames · ${blob.size} bytes. Narration / final film verification pending.`;await report({state:'master_saved',frame:7200,totalFrames:7200,processId:'C01',bytes:blob.size});
    }catch(error){if(output)try{await output.cancel();}catch{}$('status').textContent=error.message;try{await report({state:state.cancel?'cancelled':'failed',frame:state.frame,totalFrames:7200,processId:'C01',message:String(error.message).slice(0,200)});}catch{}}
    finally{state.rendering=false;state.lang=savedLanguage;state.time=savedTime;$('render').disabled=false;$('play').disabled=false;$('language').disabled=false;$('cancel').hidden=true;refresh();}
  }
  $('play').onclick=()=>{if(state.rendering||!engine)return;if(state.time>=300)state.time=0;state.playing=!state.playing;last=performance.now();refresh();};$('restart').onclick=()=>seek(0);$('timeline').oninput=e=>seek(e.target.value);$('language').onchange=e=>{state.lang=e.target.value;refresh();};$('fullscreen').onclick=async()=>{try{if(document.fullscreenElement)await document.exitFullscreen();else await $('stage').requestFullscreen();}catch{}};$('render').onclick=exportMaster;$('cancel').onclick=()=>state.cancel=true;
  try{engine=window.MG_PACKAGING_PROCESS_SCENE.create({canvas:sceneCanvas});engine.resize(1280,720,1);}catch(error){$('error').hidden=false;$('error').textContent=error.message;$('play').disabled=true;$('render').disabled=true;}
  function tick(now){if(state.playing&&!state.rendering){state.time=Math.min(300,state.time+Math.min((now-last)/1000,.2));render();if(state.time>=300){state.playing=false;refresh();}}last=now;requestAnimationFrame(tick);}
  refresh();requestAnimationFrame(tick);
  window.MG_PACKAGING_PROCESS_PLAYER={renderFrame:render,seek,exportSilentMaster:exportMaster,state:()=>({...state,localSink,scene:engine?.getState()}),script:D};
})();
