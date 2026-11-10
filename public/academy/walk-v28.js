/* V28 field controls and reference-room planning. No captured depth is invented. */
import {safePhotoPath} from './walk-domains-v22.js';

const clamp=(v,a,b)=>Math.max(a,Math.min(b,v));
export function normalizeWalkSettings(value={}) {
  const number=(key,fallback,a,b)=>Number.isFinite(Number(value[key]))?clamp(Number(value[key]),a,b):fallback;
  return {fov:number('fov',72,45,120),speed:number('speed',1,0.35,1.6),quality:['auto','high','low'].includes(value.quality)?value.quality:'auto',labels:value.labels!==false};
}
export function compassHeading(yaw=0) {
  const degrees=((-(Number(yaw)||0)*180/Math.PI)%360+360)%360;
  return {degrees:Math.round(degrees)%360,cardinal:['N','NE','E','SE','S','SW','W','NW'][Math.round(degrees/45)%8]};
}
export function planReferenceGallery(scene,assets=[]) {
  const requested=new Set(scene?.assetIds||[]),seen=new Set();
  return assets.filter(a=>a&&a.projection!=='equirectangular'&&safePhotoPath(a.src||a.path)&&(requested.has(a.id)||a.categories?.includes(scene?.category)))
    .sort((a,b)=>Number(requested.has(b.id))-Number(requested.has(a.id)))
    .filter(a=>{const src=safePhotoPath(a.src||a.path);if(seen.has(src))return false;seen.add(src);return true;})
    .slice(0,4).map(a=>({id:a.id,src:safePhotoPath(a.src||a.path),title:a.title||a.titleEn||'',titleEn:a.titleEn||a.title||'',author:a.author||'',license:a.license||'',sourceUrl:a.sourceUrl||'',licenseUrl:a.licenseUrl||''}));
}
export function enrichWorldConfig(config,scene,assets=[],courseId='') {
  const result={...config,referencePhotos:planReferenceGallery(scene,assets)};
  if(scene?.specialty==='communications'||/^comm-v28-\d{3}$/.test(courseId)) {
    result.specialty='communications';result.color='#61dbe4';
    const kinds=['rf-bench','fiber-link','network-fabric','packet-wall','timing-bench','dish'];
    result.stations=config.stations.map((s,i)=>({...s,kind:kinds[i%kinds.length]}));
  }
  return result;
}

export function createFieldControls({getWorld,getScene,getConfig,getLanguage,openPhoto,openTask,toast,translate=()=>{},onSettings=()=>{}}) {
  const L=(a,b)=>getLanguage()==='zh-TW'?a:b;
  const escape=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  let settings=normalizeWalkSettings(),guided=false,stationIndex=0,arrived=false,lastState=null;
  try{settings=normalizeWalkSettings(JSON.parse(localStorage.getItem('mg-walk-settings-v28')||'{}'));}catch{}
  const dock=document.createElement('section');dock.id='field-dock-v28';dock.setAttribute('aria-label','Field controls');
  const compass=document.createElement('div');compass.id='field-compass-v28';compass.dataset.noTranslate='';compass.setAttribute('aria-hidden','true');
  const hud=document.querySelector('#hud');hud.append(dock,compass);
  let layoutFrame=0;
  function measureDock(){layoutFrame=0;const height=dock.getBoundingClientRect().height;if(height>0)hud.style.setProperty('--field-dock-height',Math.ceil(height)+'px');}
  function queueLayout(){if(!layoutFrame)layoutFrame=requestAnimationFrame(measureDock);}
  const layoutObserver=typeof ResizeObserver==='function'?new ResizeObserver(measureDock):null;
  layoutObserver?.observe(dock);window.addEventListener('resize',queueLayout);
  function apply(){getWorld()?.setDisplaySettings?.(settings);onSettings(settings);try{localStorage.setItem('mg-walk-settings-v28',JSON.stringify(settings));}catch{}}
  function stop(silent=true){guided=false;arrived=false;getWorld()?.stop?.();renderRoute();if(!silent)toast(L('已停止導覽，現在可以自由行走。','Tour stopped. You can walk freely.'));}
  function name(station){return getLanguage()==='zh-TW'?station?.title||station?.titleEn:station?.titleEn||station?.title;}
  function route(){return getConfig()?.stations||[];}
  function renderRoute(){document.body.classList.toggle('field-tour-v28',guided);const node=dock.querySelector('.field-route-v28');if(!node)return;
    const s=route()[stationIndex];node.hidden=!guided;
    node.innerHTML=guided?`<span>${escape(L('導覽站','Tour stop'))} ${stationIndex+1}/${route().length} · ${escape(name(s)||'')}</span><button data-tour-action>${escape(arrived?L('下一站','Next station'):L('停止導覽','Stop tour'))}</button>${arrived?`<button data-operate>${escape(L('操作本站','Operate station'))}</button>`:''}`:'';
    const action=node.querySelector('[data-tour-action]');if(action)action.onclick=()=>arrived?advance():stop(false);
    const operate=node.querySelector('[data-operate]');if(operate)operate.onclick=()=>openTask(s.id);
    if(guided)translate(node);queueLayout();
  }
  function travel(){const s=route()[stationIndex];if(!s){stop();return;}
    arrived=false;getWorld()?.setView('follow');
    if(!getWorld()?.goToStation(s.id)){stop();toast(L('這個工作站目前沒有可通行的路線。','No walkable route to this station is available.'));return;}
    renderRoute();
  }
  function advance(){if(stationIndex+1>=route().length){stop();toast(L('現場導覽結束。操作與課程進度仍由你逐項完成。','Facility tour complete. Station work and course progress remain yours to complete.'));return;}
    stationIndex++;travel();
  }
  function begin(){if(!route().length)return;guided=true;stationIndex=0;getWorld()?.stop?.();travel();}
  function render(){
    const expanded=dock.querySelector('details')?.open||false;
    dock.setAttribute('aria-label',L('現場鏡頭與移動設定','Field camera and movement settings'));
    dock.innerHTML=`<div class="field-actions-v28"><button data-field-photos>◉ ${escape(L('全螢幕實拍 / 360°','Full-screen photos / 360°'))}</button><button data-field-tour>⌁ ${escape(L('帶我走一遍','Walk me through'))}</button><details ${expanded?'open':''}><summary>${escape(L('鏡頭與步速','Camera & pace'))}</summary><div class="field-settings-v28"><label for="field-fov-v28">${escape(L('廣角鏡頭','Field of view'))}<span data-fov-value>${settings.fov}°</span><input id="field-fov-v28" data-setting="fov" aria-describedby="field-lens-note-v28" aria-label="${escape(L('視野角度','Field of view'))}" type="range" min="45" max="120" step="1" value="${settings.fov}"></label><p id="field-lens-note-v28" class="field-lens-note-v28" hidden>${escape(L('僅 3D 模式可調廣角；2D 模式請用滾輪或雙指縮放。','Field of view is 3D only. In 2D, use the wheel or pinch to zoom.'))}</p><label for="field-speed-v28">${escape(L('行走速度','Walking pace'))}<span data-speed-value>${settings.speed.toFixed(2)}×</span><input id="field-speed-v28" data-setting="speed" aria-label="${escape(L('行走速度倍率','Walking speed multiplier'))}" type="range" min="0.35" max="1.6" step="0.05" value="${settings.speed}"></label><label for="field-quality-v28">${escape(L('畫質與耗電','Quality & power'))}<select id="field-quality-v28" data-setting="quality" aria-label="${escape(L('畫質與耗電','Quality and power'))}"><option value="auto" ${settings.quality==='auto'?'selected':''}>${escape(L('自動調整','Adaptive'))}</option><option value="high" ${settings.quality==='high'?'selected':''}>${escape(L('高畫質','High'))}</option><option value="low" ${settings.quality==='low'?'selected':''}>${escape(L('省電流暢','Power saving'))}</option></select></label><label class="field-check-v28" for="field-labels-v28"><input id="field-labels-v28" data-setting="labels" aria-label="${escape(L('顯示工作站標籤','Show station labels'))}" type="checkbox" ${settings.labels?'checked':''}>${escape(L('顯示工作站標籤','Show station labels'))}</label><p>${escape(L('WASD 行走 · 拖曳環視 · E 操作；手機左右拇指可同時移動與轉向。','WASD walks · drag looks · E operates; use both thumb pads to walk and turn on touch screens.'))}</p></div></details></div><div class="field-route-v28" hidden></div>`;
    dock.querySelector('[data-field-photos]').onclick=()=>{stop();openPhoto();};
    dock.querySelector('[data-field-tour]').onclick=begin;
    dock.querySelectorAll('[data-setting]').forEach(input=>input.addEventListener('input',()=>{
      const key=input.dataset.setting;settings=normalizeWalkSettings({...settings,[key]:input.type==='checkbox'?input.checked:input.value});apply();
      dock.querySelector('[data-fov-value]').textContent=settings.fov+'°';dock.querySelector('[data-speed-value]').textContent=settings.speed.toFixed(2)+'×';
    }));
    const lens=dock.querySelector('[data-setting=fov]');if(lens&&getWorld()?.getState?.()?.renderer==='canvas2d'){lens.disabled=true;dock.querySelector('#field-lens-note-v28').hidden=false;lens.title=L('2D 模式使用滾輪或雙指縮放。','Use wheel or pinch zoom in 2D mode.');}
    renderRoute();apply();if(lastState)onMove(lastState);translate(dock);
  }
  function onMove(state){lastState=state;if(!state)return;
    const heading=compassHeading(state.yaw);compass.innerHTML=`<span class="compass-mark-v28">▲</span><b>${heading.cardinal}</b><span>${String(heading.degrees).padStart(3,'0')}°</span><i></i><span>${Number(state.speedMps||0).toFixed(1)} m/s</span><span class="field-renderer-v28">${state.renderer==='webgl'?'3D':'2D'}${state.fps?' · '+Math.round(state.fps)+' fps':''}</span>`;
    document.body.classList.toggle('field-moving-v28',!!state.moving);
    if(!guided||arrived)return;
    const s=route()[stationIndex];if(s&&state.nearId===s.id&&Math.hypot(state.x-s.approach.x,state.z-s.approach.z)<.7){
      getWorld()?.stop?.();arrived=true;renderRoute();toast(L('已到達：','Arrived: ')+name(s));
    }
  }
  function manual(){if(guided){guided=false;arrived=false;renderRoute();}}
  function sceneChanged(){guided=false;arrived=false;stationIndex=0;render();}
  return {render,onMove,manual,sceneChanged,stop,getSettings:()=>({...settings}),dispose(){layoutObserver?.disconnect();window.removeEventListener('resize',queueLayout);cancelAnimationFrame(layoutFrame);dock.remove();compass.remove();document.body.classList.remove('field-tour-v28');}};
}
