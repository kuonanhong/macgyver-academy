/* A classic-script scene bundle keeps both HTTP and file:// entry points usable. */
let pending=null;
export function loadImmersiveV16(){
  if(globalThis.MG_IMMERSIVE)return Promise.resolve(globalThis.MG_IMMERSIVE);
  if(pending)return pending;
  pending=new Promise((resolve,reject)=>{
    if(!document.querySelector('link[data-v16-scene-css]')){
      const css=document.createElement('link');css.rel='stylesheet';css.href='immersive-v16.css';css.dataset.v16SceneCss='';document.head.append(css);
    }
    const script=document.createElement('script');script.src='immersive-v16.bundle.js';script.async=true;
    const timer=setTimeout(()=>{script.remove();reject(Error('Scene loading timed out.'));},30000);
    script.onload=()=>{clearTimeout(timer);script.remove();globalThis.MG_IMMERSIVE?resolve(globalThis.MG_IMMERSIVE):reject(Error('Scene module is incomplete.'));};
    script.onerror=()=>{clearTimeout(timer);script.remove();reject(Error('Extract the complete package to load the scene.'));};document.head.append(script);
  }).catch(error=>{pending=null;throw error;});
  return pending;
}
