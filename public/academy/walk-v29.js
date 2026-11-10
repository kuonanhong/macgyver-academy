/* V29 field controls. Uses the existing collision-aware avatar/camera engine. */
import {createFieldControls as previousControls,enrichWorldConfig as previousConfig} from './walk-v28.js';
import {sceneMedia,isVerifiedPanorama} from './walk-media-v25.js';
export {normalizeWalkSettings,compassHeading,planReferenceGallery} from './walk-v28.js';
const clamp=(v,a,b)=>Math.max(a,Math.min(b,v));
const escape=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
export function enrichWorldConfig(config,scene,assets=[],courseId=''){
 const c=previousConfig(config,scene,assets,courseId);
 if(scene?.specialty==='software'||/^soft-v29-\d{3}$/.test(courseId)){
  const kinds=['certificate-terminal','memory-bench','storage-array','soc-console','availability-panel','log-archive'];
  return {...c,specialty:'software',color:'#a3cfff',stations:c.stations.map((s,i)=>({...s,kind:kinds[i%kinds.length]}))};
 }return c;
}
export function radialDeadzone(x,z,deadzone=.18){
 if(!Number.isFinite(x)||!Number.isFinite(z))return {x:0,z:0};
 const d=Number.isFinite(deadzone)?clamp(deadzone,.08,.45):.18,m=Math.hypot(x,z);
 if(m<=d)return {x:0,z:0};const strength=(Math.min(1,m)-d)/(1-d);
 return {x:x/m*strength,z:z/m*strength};
}
export function sampleStandardPad(pad,deadzone=.18){
 const neutral={move:{x:0,z:0},look:{x:0,z:0},buttons:[]};
 if(!pad?.connected)return {...neutral,state:'missing'};
 if(pad.mapping!=='standard'||!pad.axes||pad.axes.length<4)return {...neutral,state:'unmapped'};
 return {state:'ready',move:radialDeadzone(pad.axes[0],pad.axes[1],deadzone),look:radialDeadzone(pad.axes[2],pad.axes[3],deadzone),buttons:Array.from(pad.buttons||[],b=>b?.pressed===true)};
}
export function sceneMediaCounts(scene,assets=[]){
 const selected=sceneMedia(scene,assets),panoramas=selected.filter(isVerifiedPanorama).length;
 return {total:selected.length,panoramas,photos:selected.length-panoramas};
}
/** Separable input driver permits deterministic tests without a physical pad. */
export function createGamepadDriver({getWorld,isBlocked=()=>false,onAction=()=>{},onStatus=()=>{}}){
 let enabled=false,deadzone=.18,sensitivity=1,armed=false,ownsMove=false,previous=[],last=null,status='off';
 function report(s){if(s!==status){status=s;onStatus(s);}}
 function release(){if(ownsMove)getWorld()?.setMove?.(0,0);ownsMove=false;previous=[];last=null;armed=false;}
 function step(now,pads=[]){
  if(!enabled){release();report('off');return;}
  if(isBlocked()){release();report('paused');return;}
  const connected=Array.from(pads||[]).filter(p=>p?.connected),pad=connected.find(p=>p.mapping==='standard')||connected[0],sample=sampleStandardPad(pad,deadzone);
  if(sample.state!=='ready'){release();report(sample.state);return;}
  const neutral=!sample.move.x&&!sample.move.z&&!sample.look.x&&!sample.look.z&&!sample.buttons.some(Boolean);
  if(!armed){if(neutral){armed=true;report('ready');last=now;}else report('center');previous=sample.buttons;return;}
  const dt=last===null?0:clamp((now-last)/1000,0,.05);last=now;report('ready');
  if(sample.move.x||sample.move.z){getWorld()?.setMove?.(sample.move.x,sample.move.z);ownsMove=true;}else if(ownsMove){getWorld()?.setMove?.(0,0);ownsMove=false;}
  if(sample.look.x||sample.look.z)getWorld()?.look?.(-sample.look.x*dt*1.8*sensitivity,-sample.look.z*dt*1.4*sensitivity);
  const commands={0:'interact',1:'stop',2:'photo',3:'camera',9:'stations'};
  for(const [index,command]of Object.entries(commands))if(sample.buttons[index]&&!previous[index])onAction(command);
  previous=sample.buttons;
 }
 return {step,setEnabled(v){enabled=!!v;release();report(enabled?'center':'off');},relinquish:release,setSettings(v={}){deadzone=Number.isFinite(Number(v.deadzone))?clamp(Number(v.deadzone),.08,.45):.18;sensitivity=Number.isFinite(Number(v.sensitivity))?clamp(Number(v.sensitivity),.5,2):1;release();},getStatus:()=>status,isEnabled:()=>enabled,dispose(){enabled=false;release();}};
}

export function createFieldControls(options){
 const base=previousControls(options),{getWorld,getScene,getConfig,getLanguage,openPhoto,openTask,toast,translate=()=>{}}=options;
 const L=(a,b)=>getLanguage()==='zh-TW'?a:b;
 const name=s=>getLanguage()==='zh-TW'?s?.title||s?.titleEn:s?.titleEn||s?.title;
 const q=s=>document.querySelector(s),listeners=[];
 const listen=(node,type,fn,opt)=>{node?.addEventListener(type,fn,opt);listeners.push(()=>node?.removeEventListener(type,fn,opt));};
 const dialog=document.createElement('dialog');dialog.id='field-stations-v29';dialog.setAttribute('aria-labelledby','field-stations-title-v29');document.body.append(dialog);
 const exit=document.createElement('button');exit.id='field-exit-v29';exit.hidden=true;exit.dataset.noTranslate='';document.body.append(exit);
 const stop=document.createElement('button');stop.id='field-stop-v29';stop.hidden=true;stop.dataset.noTranslate='';document.body.append(stop);
 let disposed=false,frame=0,lastState=null,fullscreenBusy=false,focus=false,priorFocus=null,routeId='',padSettings={deadzone:.18,sensitivity:1};
 try{const saved=JSON.parse(localStorage.getItem('mg-pad-v29')||'{}');if(Number.isFinite(saved.deadzone))padSettings.deadzone=clamp(saved.deadzone,.08,.45);if(Number.isFinite(saved.sensitivity))padSettings.sensitivity=clamp(saved.sensitivity,.5,2);}catch{}
 const visible=node=>!!node&&!node.hidden&&node.getClientRects().length>0;
 const blocked=()=>document.hidden||!document.hasFocus()||!!document.querySelector('dialog[open]')||visible(q('#task-panel'))||visible(q('.mentor-panel'))||!!document.activeElement?.closest('input,textarea,select,[contenteditable]:not([contenteditable=false])');
 function stopNow(){driver.relinquish();base.stop();getWorld()?.stop?.();routeId='';stop.hidden=true;}
 const statusText={off:()=>L('未啟用','Disabled'),missing:()=>L('按一下已連接控制器的按鈕以辨識','Press a connected controller button to detect it'),unmapped:()=>L('此控制器沒有標準按鍵映射，請用觸控或鍵盤','No standard mapping; use touch or keyboard'),center:()=>L('放開按鍵、讓兩個搖桿回正後開始','Release buttons and center both sticks to begin'),paused:()=>L('開啟面板或切換視窗時暫停','Paused while panels or other windows are active'),ready:()=>L('可用：左桿行走／右桿環視','Ready: left stick walks / right stick looks')};
 function updatePadStatus(){const node=q('[data-pad-status-v29]');if(node)node.textContent=(statusText[driver.getStatus()]||statusText.missing)();}
 const driver=createGamepadDriver({getWorld,isBlocked:blocked,onStatus:updatePadStatus,onAction:action=>{
  if(action==='stop')stopNow();else if(action==='interact')getWorld()?.interact?.();else if(action==='photo'){stopNow();openPhoto();}else if(action==='stations')openStations();else if(action==='camera'){
   const state=getWorld()?.getState?.(),views=state?.renderer==='canvas2d'?['follow','close','overview']:['follow','close','first','overview'];getWorld()?.setView?.(views[(views.indexOf(state?.view)+1)%views.length]);
  }
 }});driver.setSettings(padSettings);
 function refreshFullscreen(){focus=focus||!!document.fullscreenElement;document.body.classList.toggle('field-focus-v29',focus);exit.hidden=!focus;exit.textContent=L('退出沉浸畫面','Exit immersive view')+' · Esc';const b=q('#fullscreen-button');if(b)b.setAttribute('aria-pressed',String(focus));getWorld()?.resize?.();}
 async function fullscreen(){
  if(fullscreenBusy)return;fullscreenBusy=true;stopNow();
  try{if(focus||document.fullscreenElement){focus=false;if(document.fullscreenElement)await document.exitFullscreen();}else{
   focus=true;const request=document.documentElement.requestFullscreen;
   if(request){try{await request.call(document.documentElement);}catch{toast(L('使用瀏覽器滿版模式；工具列由裝置管理。','Using a full browser view; browser chrome is controlled by your device.'));}}
   else toast(L('使用瀏覽器滿版模式；可從退出鍵回復。','Using a full browser view. Use Exit to restore the controls.'));
  }}finally{fullscreenBusy=false;refreshFullscreen();}
 }
 exit.onclick=fullscreen;stop.onclick=()=>{stopNow();q('#walk-world')?.focus({preventScroll:true});};
 listen(document,'fullscreenchange',()=>{if(!document.fullscreenElement&&!fullscreenBusy)focus=false;refreshFullscreen();});
 // Capture both entry points so a denied request cannot trigger the older handler twice.
 listen(document,'click',e=>{if(e.target.closest?.('#fullscreen-button')){e.preventDefault();e.stopImmediatePropagation();fullscreen();}},true);
 listen(window,'keydown',e=>{
  if(e.key==='Escape'&&focus&&!document.querySelector('dialog[open]')&&!visible(q('#task-panel'))){e.preventDefault();e.stopImmediatePropagation();fullscreen();return;}
  if(e.ctrlKey||e.metaKey||e.altKey||e.target?.closest?.('input,textarea,select,dialog,[contenteditable]:not([contenteditable=false]),.mentor-panel'))return;
  if(e.key.toLowerCase()==='f'){e.preventDefault();e.stopImmediatePropagation();if(!e.repeat)fullscreen();}
  else if(e.key.toLowerCase()==='m'){e.preventDefault();e.stopImmediatePropagation();if(!e.repeat)openStations();}
  else driver.relinquish();
 },true);
 listen(document,'pointerdown',()=>driver.relinquish(),true);
 listen(window,'blur',()=>driver.relinquish());listen(document,'visibilitychange',()=>{if(document.hidden)driver.relinquish();});listen(window,'gamepaddisconnected',()=>driver.relinquish());
 function viewport(){const v=window.visualViewport,keyboard=!!v&&v.scale===1&&v.height<innerHeight*.78;document.body.classList.toggle('field-keyboard-v29',keyboard);document.documentElement.style.setProperty('--field-visible-height-v29',`${Math.round(v?.height||innerHeight)}px`);getWorld()?.resize?.();}
 listen(window.visualViewport,'resize',viewport);listen(window,'resize',viewport);viewport();
 function resume(){if(!blocked())getWorld()?.setPaused(false);q('#walk-world')?.focus({preventScroll:true});}
 listen(dialog,'close',()=>{document.body.classList.remove('field-menu-v29');resume();priorFocus?.focus?.({preventScroll:true});});
 function go(id){const station=getConfig()?.stations?.find(s=>s.id===id);if(!station)return;dialog.close();getWorld()?.setPaused(false);base.manual();getWorld()?.stop?.();getWorld()?.setView('follow');if(getWorld()?.goToStation(id)){routeId=id;toast(L('沿可行走路線前往：','Following a walkable route to: ')+name(station));}else toast(L('目前無可行走路線；請回入口重試。','No walkable route is available. Return to the entrance and retry.'));}
 function openStations(){
  stopNow();priorFocus=document.activeElement;getWorld()?.setPaused(true);const scene=getScene(),stations=getConfig()?.stations||[],state=getWorld()?.getState?.()||{},assets=window.MACGYVER_EXPERIENCES_V21?.assets||[],media=sceneMediaCounts(scene,assets);
  dialog.innerHTML=`<header class="dialog-head"><div><p class="eyebrow">${escape(L('場內工作站','FIELD STATIONS'))}</p><h2 id="field-stations-title-v29">${escape(name(scene))}</h2></div><button data-close-v29 aria-label="${escape(L('關閉工作站清單','Close station list'))}">×</button></header><div class="dialog-body"><p class="field-menu-intro-v29">${escape(L('選擇工作站，人物會沿通道走到設備旁。到達後按 E 或「操作本站」。','Choose a station to walk along the aisles. On arrival, press E or Operate station.'))}</p><ol class="field-station-list-v29">${stations.map((s,i)=>`<li><span class="field-station-number-v29">${String(i+1).padStart(2,'0')}</span><div><h3>${escape(name(s))}</h3><p>${escape(getLanguage()==='zh-TW'?s.equipmentTitle||'':s.equipmentTitleEn||'')} · ${Math.hypot((state.x||0)-s.approach.x,(state.z||0)-s.approach.z).toFixed(1)} m</p></div><button data-go-v29="${escape(s.id)}">${escape(state.nearId===s.id?L('操作本站','Operate'):L('走向本站','Walk here'))} →</button></li>`).join('')}</ol><div class="field-media-summary-v29"><strong>${escape(L('實拍影像與全景','Photographs and panoramas'))}</strong><p>${media.photos} ${escape(L('張照片','photographs'))} · ${media.panoramas} ${escape(L('個已核對全景','verified panoramas'))}</p><p>${escape(L('這些是此領域的實拍參考；可行走場地是教學模型。360°影像可看前後左右上下，但拍攝位置固定，沒有步行視差。','These are photographed domain references. The walkable facility is a teaching model. A 360° capture shows all directions from one fixed position, without walking parallax.'))}</p><button data-photo-v29>◉ ${escape(L('全螢幕照片／360°','Full-screen photos / 360°'))}</button><a href="experience-photo-v21.html?domain=${encodeURIComponent(scene?.category||'')}&lang=${encodeURIComponent(getLanguage())}#scene=${encodeURIComponent(scene?.id||'')}">${escape(L('匯入自己的全景／六向照片','Import your panorama / six photographs'))} ↗</a></div></div>`;
  dialog.querySelector('[data-close-v29]').onclick=()=>dialog.close();dialog.querySelector('[data-photo-v29]').onclick=()=>{dialog.close();openPhoto();};
  for(const b of dialog.querySelectorAll('[data-go-v29]'))b.onclick=()=>{const id=b.dataset.goV29;if(getWorld()?.getState?.().nearId===id){dialog.close();openTask(id);}else go(id);};
  document.body.classList.add('field-menu-v29');if(!dialog.open)dialog.showModal();translate(dialog);
 }
 function decorate(){
  const actions=q('.field-actions-v28'),settings=q('.field-settings-v28');if(!actions||!settings)return;
  const button=document.createElement('button');button.dataset.stationsV29='';button.textContent='▦ '+L('工作站','Stations');button.title=L('M：場內工作站','M: field stations');button.onclick=openStations;actions.insertBefore(button,actions.querySelector('details'));
  const fieldset=document.createElement('fieldset');fieldset.className='field-pad-settings-v29';fieldset.innerHTML=`<legend>${escape(L('遊戲控制器','Game controller'))}</legend><label class="field-check-v28"><input type="checkbox" data-pad-enable-v29 ${driver.isEnabled()?'checked':''}>${escape(L('啟用標準控制器','Enable standard gamepad'))}</label><p data-pad-status-v29 role="status" data-no-translate></p><label>${escape(L('搖桿死區','Stick deadzone'))}<span>${Math.round(padSettings.deadzone*100)}%</span><input type="range" data-pad-deadzone-v29 min="0.08" max="0.45" step="0.01" value="${padSettings.deadzone}"></label><label>${escape(L('環視靈敏度','Look sensitivity'))}<span>${padSettings.sensitivity.toFixed(1)}×</span><input type="range" data-pad-sensitivity-v29 min="0.5" max="2" step="0.1" value="${padSettings.sensitivity}"></label><p>${escape(L('A／南鍵：操作；B／東鍵：停止；X／西鍵：照片；Y／北鍵：視角；Start：工作站。首次啟用及重新接手須先讓搖桿回正。','A / South: interact; B / East: stop; X / West: photos; Y / North: camera; Start: stations. Center both sticks when enabling or resuming control.'))}</p>`;settings.append(fieldset);
  fieldset.querySelector('[data-pad-enable-v29]').onchange=e=>driver.setEnabled(e.target.checked);
  for(const [key,selector]of [['deadzone','[data-pad-deadzone-v29]'],['sensitivity','[data-pad-sensitivity-v29]']])fieldset.querySelector(selector).oninput=e=>{padSettings[key]=Number(e.target.value);e.target.previousElementSibling.textContent=key==='deadzone'?Math.round(padSettings[key]*100)+'%':padSettings[key].toFixed(1)+'×';driver.setSettings(padSettings);try{localStorage.setItem('mg-pad-v29',JSON.stringify(padSettings));}catch{}};
  stop.textContent='■ '+L('停止移動','Stop');stop.setAttribute('aria-label',L('停止行走與導覽','Stop walking and guidance'));updatePadStatus();refreshFullscreen();translate(fieldset);translate(button);
 }
 function tick(now){if(disposed)return;let pads=[];if(driver.isEnabled()){try{pads=navigator.getGamepads?.()||[];}catch{}}driver.step(now,pads);frame=requestAnimationFrame(tick);}
 frame=requestAnimationFrame(tick);
 return {
  render(){base.render();decorate();},sceneChanged(){routeId='';driver.relinquish();base.sceneChanged();decorate();},
  onMove(state){lastState=state;base.onMove(state);stop.hidden=!state?.moving||blocked();if(routeId&&state?.nearId===routeId&&state.pathRemaining===0){const s=getConfig()?.stations?.find(s=>s.id===routeId);routeId='';toast(L('已到達：','Arrived: ')+name(s)+L('。按 E 操作本站。','. Press E to operate.'));}},
  manual(){routeId='';base.manual();},stop:stopNow,getSettings:()=>base.getSettings(),openStations,
  dispose(){disposed=true;cancelAnimationFrame(frame);driver.dispose();listeners.forEach(f=>f());base.dispose();dialog.remove();exit.remove();stop.remove();document.body.classList.remove('field-focus-v29','field-keyboard-v29','field-menu-v29');}
 };
}
