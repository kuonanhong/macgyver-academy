/* V30 field controls for the walking world: six fixed wide-angle looks
 * (front, back, left, right, up, down) and a door to the real-world scene of the
 * same domain. Uses the existing collision-aware avatar and camera engine. */
import {createFieldControls as previousControls,enrichWorldConfig as previousConfig} from './walk-v29.js';
export const enrichWorldConfig=previousConfig;
export const SIX_LOOKS_V30=Object.freeze([
 ['front','↑',0,0,'前','Front'],['left','←',Math.PI/2,0,'左','Left'],['right','→',-Math.PI/2,0,'右','Right'],
 ['back','↓',Math.PI,0,'後','Back'],['up','⤒',0,1.3,'上','Up'],['down','⤓',0,-1.3,'下','Down']]);
export function realWorldHref(scene,config){
 const domain=String(scene?.category||config?.domainId||'energy').replace(/[^a-z0-9-]/gi,'').slice(0,40)||'energy';
 const course=String(scene?.courseId||'').replace(/[^a-z0-9-]/gi,'').slice(0,80);
 return 'realworld-v30.html?domain='+encodeURIComponent(domain)+(course?'&site='+encodeURIComponent(course):'');
}
export function createFieldControls(options){
 const base=previousControls(options),{getWorld,getScene,getConfig}=options;
 const bar=document.createElement('nav');bar.id='six-v30';bar.dataset.noTranslate='';bar.setAttribute('aria-label','六向廣角環視 / Six-way wide-angle look');
 const widen=()=>{const lens=document.querySelector('#field-fov-v28');if(!lens||lens.disabled||Number(lens.value)>=104)return;lens.value='104';for(const type of ['input','change'])lens.dispatchEvent(new Event(type,{bubbles:true}));};
 for(const [id,glyph,yaw,pitch,zh,en] of SIX_LOOKS_V30){
  const button=document.createElement('button');button.type='button';button.dataset.sixV30=id;button.textContent=glyph;button.title=button.ariaLabel=`${zh} / ${en}`;
  button.addEventListener('click',()=>{const world=getWorld();if(!world?.look||!world.setView)return;world.setView('first');world.recenter?.();world.look(yaw,pitch);widen();});
  bar.append(button);
 }
 const link=document.createElement('a');link.id='realworld-link-v30';link.textContent='實景 ↗';link.title=link.ariaLabel='全螢幕實景工程場景 / Full-screen real-world scene';link.href='realworld-v30.html';
 const refresh=()=>{link.href=realWorldHref(getScene?.(),getConfig?.());};
 link.addEventListener('pointerdown',refresh);link.addEventListener('focus',refresh);link.addEventListener('click',refresh);
 bar.append(link);document.body.append(bar);
 return base;
}
