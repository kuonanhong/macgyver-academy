/* V25 immersive evidence viewer. Real panoramas are fixed-camera captures;
 * movement remains in the independent teaching world, never a photo warp. */
import {safePhotoPath} from './walk-domains-v22.js';
import {uiText} from './walk-i18n-v22.js';
export const isVerifiedPanorama = a => !!a && a.projection === 'equirectangular' && a.panoramaVerified === true && !!safePhotoPath(a.src || a.path);
export function sceneMedia(scene, assets) {
  const ids = new Set(scene?.assetIds || []);
  return assets.filter(a => safePhotoPath(a.src || a.path) && (ids.has(a.id) || a.categories?.includes(scene?.category)))
    .sort((a,b) => Number(isVerifiedPanorama(b))-Number(isVerifiedPanorama(a)) || Number(ids.has(b.id))-Number(ids.has(a.id)));
}
export function directionPose(direction, yaw=0) {
  return ({front:[0,0],right:[Math.PI/2,0],back:[Math.PI,0],left:[-Math.PI/2,0],up:[yaw,Math.PI/2-.001],down:[yaw,-Math.PI/2+.001]})[direction] || [yaw,0];
}
const escape = s => String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const safeLink = s => {try{return new URL(s).protocol==='https:'?s:'#';}catch{return '#';}};
const clamp = (v,a,b) => Math.max(a,Math.min(b,v));
export function createImmersiveMedia({THREE:T,utils={},getLanguage=()=> 'en',translate=()=>{},onClose=()=>{}}={}) {
  const dialog=document.createElement('dialog');dialog.className='walk-media';dialog.setAttribute('aria-labelledby','media-title');document.body.append(dialog);
  let assets=[],scene=null,current=null,index=0,epoch=0,renderer=null,image=null,yaw=0,pitch=0,fov=75,zoom=1,offset={x:0,y:0},frame=0,priorFocus=null;
  const pointers=new Map();let pinch=0;
  const zh=()=>getLanguage().startsWith('zh'),L=(a,b)=>zh()?a:b,t=key=>uiText(getLanguage(),key),field=(o,k)=>o?.[zh()?k:k+'En']||o?.[k+'En']||o?.[k]||'';
  const q=s=>dialog.querySelector(s);
  function disposeRenderer(){renderer?.dispose();renderer=null;cancelAnimationFrame(frame);frame=0;}
  function draw(){frame=0;if(!dialog.open||!image?.complete||!image.naturalWidth)return;
    if(renderer){renderer.draw(yaw,pitch,fov);return;}
    const r=q('.media-stage').getBoundingClientRect(),scale=Math.min(r.width/image.naturalWidth,r.height/image.naturalHeight)*zoom;
    const w=image.naturalWidth*scale,h=image.naturalHeight*scale;
    offset.x=clamp(offset.x,-Math.max(0,(w-r.width)/2),Math.max(0,(w-r.width)/2));offset.y=clamp(offset.y,-Math.max(0,(h-r.height)/2),Math.max(0,(h-r.height)/2));
    image.style.width=w+'px';image.style.height=h+'px';image.style.transform=`translate(-50%,-50%) translate(${offset.x}px,${offset.y}px)`;
  }
  function paint(){if(!frame)frame=requestAnimationFrame(draw);}
  function gpu(canvas,img){if(!T?.WebGLRenderer)return null;let r,geometry,material,texture;
    try{r=new T.WebGLRenderer({canvas,antialias:false,powerPreference:'low-power'});r.outputColorSpace=T.SRGBColorSpace;r.setPixelRatio(Math.min(devicePixelRatio||1,1.5));
      const s=new T.Scene(),c=new T.PerspectiveCamera(75,1,.1,20);texture=new T.Texture(img);texture.needsUpdate=true;texture.colorSpace=T.SRGBColorSpace;
      geometry=new T.SphereGeometry(10,48,32);material=new T.MeshBasicMaterial({map:texture,side:T.BackSide});const sphere=new T.Mesh(geometry,material);sphere.rotation.y=-Math.PI/2;s.add(sphere);
      return {draw(y,p,f){const box=q('.media-stage').getBoundingClientRect();r.setSize(Math.max(1,box.width),Math.max(1,box.height),false);c.aspect=box.width/Math.max(1,box.height);c.fov=f;c.updateProjectionMatrix();c.lookAt(Math.sin(y)*Math.cos(p),Math.sin(p),-Math.cos(y)*Math.cos(p));r.render(s,c);},dispose(){geometry.dispose();material.dispose();texture.dispose();r.dispose();r.forceContextLoss();}};
    }catch{geometry?.dispose();material?.dispose();texture?.dispose();r?.dispose();return null;}
  }
  function reset(){yaw=pitch=0;fov=75;zoom=1;offset={x:0,y:0};paint();}
  function changeZoom(factor){if(renderer)fov=clamp(fov/factor,35,110);else zoom=clamp(zoom*factor,1,5);paint();}
  function refreshText(){q('#media-title').textContent=field(current,'title');q('.media-scope').textContent=renderer?L('實拍 360° · 固定拍攝位置，可環視上下左右；不提供未拍攝的步行視差。','Photographed 360° · Look in every direction from the fixed capture point; walking parallax is not recorded.'):L('實拍平面照片 · 平移與縮放只顯示原有影像範圍。','Flat photograph · Pan and zoom within the recorded image.');
    q('.media-credit').innerHTML=`${escape(current.author||'')} · ${escape(current.license||'')} <a href="${escape(safeLink(current.sourceUrl))}" target="_blank" rel="noopener noreferrer">${escape(t('source'))} ↗</a> <a href="${escape(safeLink(current.licenseUrl))}" target="_blank" rel="noopener noreferrer">${escape(current.license||'License')} ↗</a>`;
    q('.media-direction').hidden=!renderer;q('.media-count').textContent=`${index+1} / ${assets.length}`;translate(dialog);
  }
  function select(next){index=(next+assets.length)%assets.length;current=assets[index];const captured=++epoch;disposeRenderer();pointers.clear();pinch=0;reset();q('.media-stage').replaceChildren();
    const message=document.createElement('p');message.className='media-loading';message.textContent=t('loading');q('.media-stage').append(message);
    image=new Image();image.className='media-image';image.alt=field(current,'title');image.hidden=true;q('.media-stage').append(image);
    image.onload=()=>{if(captured!==epoch||!dialog.open)return;message.remove();image.hidden=false;
      if(isVerifiedPanorama(current)&&Math.abs(image.naturalWidth/image.naturalHeight-2)<.03){let canvas=document.createElement('canvas');canvas.className='media-panorama';q('.media-stage').append(canvas);renderer=gpu(canvas,image);
        if(!renderer&&utils.createCpuPanorama){canvas.remove();canvas=document.createElement('canvas');canvas.className='media-panorama';q('.media-stage').append(canvas);const cpu=utils.createCpuPanorama(canvas,{maxWidth:480,maxHeight:270});if(cpu?.setImage(image))renderer={draw(y,p,f){const r=q('.media-stage').getBoundingClientRect();const w=Math.max(1,Math.round(r.width)),h=Math.max(1,Math.round(r.height));if(canvas.width!==w)canvas.width=w;if(canvas.height!==h)canvas.height=h;cpu.draw(y,p,75/f);},dispose(){cpu.dispose();}};else cpu?.dispose();}
        if(renderer)image.hidden=true;else canvas.remove();
      }refreshText();paint();};
    image.onerror=()=>{if(captured!==epoch)return;message.textContent=L('影像無法載入；可選擇其他影像或返回實驗室。','This image could not load. Choose another or return to the lab.');};
    image.src=safePhotoPath(current.src||current.path);refreshText();
    for(const button of dialog.querySelectorAll('[data-media-index]'))button.setAttribute('aria-pressed',String(Number(button.dataset.mediaIndex)===index));
  }
  function open(nextScene,allAssets,preferredId){scene=nextScene;assets=sceneMedia(scene,allAssets);if(!assets.length)return false;priorFocus=document.activeElement;
    dialog.innerHTML=`<div class="media-stage" tabindex="0" role="img" aria-label="${escape(t('photos'))}"></div><header class="media-top"><div><p class="eyebrow">${escape(t('photos'))} · V25</p><h2 id="media-title"></h2><p class="media-scope"></p></div><button data-close>${escape(t('close'))} ×</button></header><nav class="media-direction" aria-label="${escape(t('look'))}">${[['front','前','Front'],['left','左','Left'],['right','右','Right'],['back','後','Back'],['up','上','Up'],['down','下','Down']].map(([d,a,b])=>`<button data-direction="${d}">${L(a,b)}</button>`).join('')}</nav><aside class="media-filmstrip" aria-label="${escape(t('photos'))}">${assets.map((a,i)=>`<button data-media-index="${i}" aria-label="${escape(field(a,'title'))}" title="${escape(field(a,'title'))}"><img src="${escape(safePhotoPath(a.src||a.path))}" loading="lazy" alt=""><span>${isVerifiedPanorama(a)?'360°':'▣'}</span></button>`).join('')}</aside><footer class="media-bottom"><p class="media-credit"></p><div class="media-tools"><button data-prev aria-label="${escape(t('previous'))}">←</button><span class="media-count"></span><button data-next aria-label="${escape(t('next'))}">→</button><button data-zoom-out aria-label="${escape(t('zoom'))} −">−</button><button data-zoom-in aria-label="${escape(t('zoom'))} +">＋</button><button data-reset>${escape(t('recenter'))}</button><a class="button" href="experience-photo-v21.html?domain=${encodeURIComponent(scene.category)}&lang=${encodeURIComponent(getLanguage())}#scene=${encodeURIComponent(scene.id)}">${L('匯入我的全景／六向照片','Import my panorama / six photographs')} ↗</a></div></footer>`;
    q('[data-close]').onclick=()=>dialog.close();q('[data-prev]').onclick=()=>select(index-1);q('[data-next]').onclick=()=>select(index+1);q('[data-zoom-in]').onclick=()=>changeZoom(1.2);q('[data-zoom-out]').onclick=()=>changeZoom(1/1.2);q('[data-reset]').onclick=reset;
    for(const b of dialog.querySelectorAll('[data-media-index]'))b.onclick=()=>select(Number(b.dataset.mediaIndex));
    for(const b of dialog.querySelectorAll('[data-direction]'))b.onclick=()=>{[yaw,pitch]=directionPose(b.dataset.direction,yaw);paint();};
    const stage=q('.media-stage');stage.onpointerdown=e=>{if(e.button>0)return;stage.focus({preventScroll:true});stage.setPointerCapture(e.pointerId);pointers.set(e.pointerId,{x:e.clientX,y:e.clientY});if(pointers.size===2){const p=[...pointers.values()];pinch=Math.hypot(p[0].x-p[1].x,p[0].y-p[1].y);}};
    stage.onpointermove=e=>{const before=pointers.get(e.pointerId);if(!before)return;const dx=e.clientX-before.x,dy=e.clientY-before.y;pointers.set(e.pointerId,{x:e.clientX,y:e.clientY});if(pointers.size===2){const p=[...pointers.values()],d=Math.hypot(p[0].x-p[1].x,p[0].y-p[1].y);if(pinch>0)changeZoom(d/pinch);pinch=d;}else if(renderer){yaw-=dx*.004*fov/75;pitch=clamp(pitch+dy*.004*fov/75,-Math.PI/2+.001,Math.PI/2-.001);}else{offset.x+=dx;offset.y+=dy;}paint();};
    for(const type of ['pointerup','pointercancel','lostpointercapture'])stage.addEventListener(type,e=>{pointers.delete(e.pointerId);pinch=0;});
    stage.addEventListener('wheel',e=>{e.preventDefault();changeZoom(Math.exp(-clamp(e.deltaY,-120,120)*.002));},{passive:false});
    if(!dialog.open)dialog.showModal();document.body.classList.add('media-open');select(Math.max(0,assets.findIndex(a=>a.id===preferredId)));return true;
  }
  dialog.addEventListener('keydown',e=>{if(e.target.closest('input,textarea,select'))return;const keys={ArrowLeft:[-.12,0],ArrowRight:[.12,0],ArrowUp:[0,.12],ArrowDown:[0,-.12]};if(keys[e.key]){e.preventDefault();if(renderer){yaw+=keys[e.key][0];pitch=clamp(pitch+keys[e.key][1],-Math.PI/2+.001,Math.PI/2-.001);}else{offset.x-=keys[e.key][0]*300;offset.y+=keys[e.key][1]*300;}paint();}else if(e.key==='+'||e.key==='=')changeZoom(1.15);else if(e.key==='-')changeZoom(1/1.15);});
  dialog.addEventListener('close',()=>{epoch++;disposeRenderer();pointers.clear();document.body.classList.remove('media-open');onClose();priorFocus?.focus({preventScroll:true});});
  window.addEventListener('resize',paint);
  return {open,close:()=>dialog.close(),isOpen:()=>dialog.open,dispose(){epoch++;disposeRenderer();window.removeEventListener('resize',paint);dialog.remove();}};
}
