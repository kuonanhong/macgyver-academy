import { expandLazyIndex } from './lazy-index-codec.js';
/* V14: catalogue first; one immutable course and its resources on demand.
 * Protected lesson responses are never taken from a static cache. */
const ID=/^[a-z0-9]+(?:[-_][a-z0-9]+)*$/;
const validID=id=>typeof id==='string'&&ID.test(id)&&!['constructor','prototype'].includes(id);
const own=(value,key)=>Object.prototype.hasOwnProperty.call(value,key);
const LIMIT=32*1024*1024;
const CORE=new Set(['catalog','featured','photos','release']);
class CurriculumRequestError extends Error {
  constructor(status,url){super(`Curriculum request failed (${status||'network'}): ${url}`);this.status=status;}
}
function clone(value){return typeof structuredClone==='function'?structuredClone(value):JSON.parse(JSON.stringify(value));}
function validateIndex(value){
  if(value?.lazyVersion!==1||!Array.isArray(value.catalog)||!value.catalog.length||value.catalog.length>20000||!Array.isArray(value.photos)||!Array.isArray(value.guidedIds)||!value.courses||!value.resources||!value.auxiliary)throw Error('Invalid lazy curriculum index.');
  const ids=new Set();
  for(const c of value.catalog){if(!c||!validID(c.id)||ids.has(c.id)||typeof c.title!=='string')throw Error('Invalid catalogue course.');ids.add(c.id);if(c.stages&&!Array.isArray(c.stages))throw Error('Invalid stage index.');}
  for(const [group,entries] of [['courses',value.courses],['resources',value.resources],['data',value.auxiliary]])for(const [id,d]of Object.entries(entries)){
    if(!validID(id)||!d||!Number.isSafeInteger(d.byteLength)||d.byteLength<2||d.byteLength>LIMIT||!/^[a-f0-9]{64}$/.test(d.sha256)||d.file!==`data/lazy/${group}/${id}-${d.sha256.slice(0,16)}.json`||d.script!==d.file.replace(/\.json$/,'.js'))throw Error('Invalid or unsafe lazy data descriptor.');
  }
  const guided=new Set(value.catalog.filter(c=>Array.isArray(c.stages)).map(c=>c.id));if(value.guidedIds.length!==guided.size||new Set(value.guidedIds).size!==guided.size||value.guidedIds.some(id=>!guided.has(id)))throw Error('Invalid guided course order.');
  for(const id of ids)if(!own(value.courses,id)||!own(value.resources,id))throw Error('Incomplete lazy catalogue.');
  return value;
}
// A small SHA-256 fallback preserves integrity checks on ordinary HTTP too,
// where Web Crypto is not available. This is hashing public data, not secrets.
export async function curriculumDigest(raw,cryptoImpl=globalThis.crypto){
  if(cryptoImpl?.subtle){const digest=await cryptoImpl.subtle.digest('SHA-256',raw);return [...new Uint8Array(digest)].map(n=>n.toString(16).padStart(2,'0')).join('');}
  const K=[0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2];
  const H=[0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19],length=raw.byteLength,bytes=new Uint8Array(Math.ceil((length+9)/64)*64);bytes.set(raw);bytes[length]=128;
  const view=new DataView(bytes.buffer);view.setUint32(bytes.length-8,Math.floor(length/0x20000000));view.setUint32(bytes.length-4,(length*8)>>>0);
  const rotate=(x,n)=>(x>>>n)|(x<<(32-n)),W=new Uint32Array(64);
  for(let offset=0;offset<bytes.length;offset+=64){
    for(let i=0;i<16;i++)W[i]=view.getUint32(offset+i*4);
    for(let i=16;i<64;i++){const x=W[i-15],y=W[i-2];W[i]=(W[i-16]+(rotate(x,7)^rotate(x,18)^(x>>>3))+W[i-7]+(rotate(y,17)^rotate(y,19)^(y>>>10)))>>>0;}
    let [a,b,c,d,e,f,g,h]=H;
    for(let i=0;i<64;i++){const t1=(h+(rotate(e,6)^rotate(e,11)^rotate(e,25))+((e&f)^(~e&g))+K[i]+W[i])>>>0,t2=((rotate(a,2)^rotate(a,13)^rotate(a,22))+((a&b)^(a&c)^(b&c)))>>>0;h=g;g=f;f=e;e=(d+t1)>>>0;d=c;c=b;b=a;a=(t1+t2)>>>0;}
    [a,b,c,d,e,f,g,h].forEach((n,i)=>H[i]=(H[i]+n)>>>0);
  }
  return H.map(n=>n.toString(16).padStart(8,'0')).join('');
}
function waitFor(start,signal){
  if(signal?.aborted)return Promise.reject(new DOMException('Aborted','AbortError'));
  const promise=start();if(!signal)return promise;
  return new Promise((resolve,reject)=>{const abort=()=>reject(new DOMException('Aborted','AbortError'));signal.addEventListener('abort',abort,{once:true});promise.then(resolve,reject).finally(()=>signal.removeEventListener('abort',abort));});
}
export function createCurriculumLoader({fetchImpl=(...args)=>globalThis.fetch(...args),view=globalThis.window,document=globalThis.document,location=globalThis.location,cryptoImpl=globalThis.crypto,timeoutMs=30000}={}){
  let indexPromise=null,ownerIndexPromise=null;const pending=new Map(),cache=new Map();
  async function json(url,limit=LIMIT,cacheMode='default'){
    const controller=new AbortController(),timer=setTimeout(()=>controller.abort(),timeoutMs);
    try{
      const response=await fetchImpl(url,{signal:controller.signal,credentials:'same-origin',redirect:'error',cache:cacheMode});
      if(!response?.ok)throw new CurriculumRequestError(response?.status,url);
      const declared=response.headers?.get?.('content-length');if(declared&&Number(declared)>limit)throw Error('Curriculum response is too large.');
      let raw;
      if(response.body?.getReader){const reader=response.body.getReader(),chunks=[];let size=0;try{while(true){const {done,value}=await reader.read();if(done)break;size+=value.byteLength;if(size>limit){await reader.cancel();throw Error('Curriculum response is too large.');}chunks.push(value);}}finally{reader.releaseLock();}raw=new Uint8Array(size);let offset=0;for(const chunk of chunks){raw.set(chunk,offset);offset+=chunk.byteLength;}}
      else{raw=new TextEncoder().encode(await response.text());if(raw.byteLength>limit)throw Error('Curriculum response is too large.');}
      return {raw,value:JSON.parse(new TextDecoder('utf-8',{fatal:true}).decode(raw))};
    }finally{clearTimeout(timer);}
  }
  function index(){
    if(!indexPromise)indexPromise=(async()=>{
      if(view?.MG_LAZY_INDEX)return validateIndex(view.MG_LAZY_INDEX);
      if(location?.protocol==='file:')throw Error('Initial catalogue is missing. Extract the complete ZIP.');
      let response;
      try{response=await json('data/lazy/index.compact.json',12*1024*1024,'no-cache');}
      catch(error){
        // Older releases have only the expanded index. Never bypass a bad
        // payload, an authorization failure, or a network error with fallback.
        if(!(error instanceof CurriculumRequestError)||![404,410].includes(error.status))throw error;
        response=await json('data/lazy/index.json',12*1024*1024,'no-cache');
      }
      return validateIndex(expandLazyIndex(response.value));
    })().catch(error=>{indexPromise=null;throw error;});
    return indexPromise;
  }
  function script(descriptor){return new Promise((resolve,reject)=>{
    const existing=view?.MG_LAZY_DATA?.[descriptor.file];if(existing?.sha256===descriptor.sha256){resolve(existing.value);return;}
    if(!document?.createElement||!view){reject(Error('Offline script loading is unavailable.'));return;}
    const node=document.createElement('script');let timer,settled=false;
    const finish=(error)=>{if(settled)return;settled=true;clearTimeout(timer);node.remove?.();const result=view.MG_LAZY_DATA?.[descriptor.file];if(error)reject(error);else if(result?.sha256!==descriptor.sha256)reject(Error('Offline data does not match its index.'));else resolve(result.value);};
    node.src=descriptor.script;node.async=true;node.onload=()=>finish();node.onerror=()=>finish(Error('Offline data failed to load. Extract all files and retry.'));timer=setTimeout(()=>finish(Error('Offline data request timed out.')),timeoutMs);document.head.appendChild(node);
  });}
  async function readDescriptor(d){
    if(cache.has(d.file))return cache.get(d.file);
    if(!pending.has(d.file))pending.set(d.file,(async()=>{
      let value;
      if(location?.protocol==='file:')value=await script(d);
      else{const result=await json(d.file,d.byteLength);if(result.raw.byteLength!==d.byteLength||await curriculumDigest(result.raw,cryptoImpl)!==d.sha256)throw Error('Curriculum checksum mismatch. Retry to fetch a consistent release.');value=result.value;}
      cache.set(d.file,value);return value;
    })().finally(()=>pending.delete(d.file)));
    return pending.get(d.file);
  }
  async function chunk(group,id){
    if(!validID(id))throw Error('Invalid course or data ID.');
    const manifest=await index(),d=own(manifest[group]||{},id)?manifest[group][id]:null;if(!d)throw Error('Course or data is not in this release.');
    return readDescriptor(d);
  }
  // Complete owner content is never selected by a visitor-facing HTTP flag.
  // Direct files are the explicitly distributed owner package, not authentication.
  async function ownerChunk(group,id){
    if(location?.protocol!=='file:'||!validID(id))throw Error('Owner files require the complete local package.');
    if(!ownerIndexPromise)ownerIndexPromise=new Promise((resolve,reject)=>{
      if(view?.MG_OWNER_INDEX){resolve(view.MG_OWNER_INDEX);return;}
      const node=document.createElement('script');let settled=false;
      const finish=error=>{if(settled)return;settled=true;clearTimeout(timer);node.remove?.();error?reject(error):resolve(view.MG_OWNER_INDEX);};
      const timer=setTimeout(()=>finish(Error('Owner index timed out.')),timeoutMs);
      node.src='data/lazy/owner-index.js';node.onload=()=>finish();node.onerror=()=>finish(Error('Extract the complete owner ZIP to read member content offline.'));document.head.appendChild(node);
    }).catch(error=>{ownerIndexPromise=null;throw error;});
    const manifest=await ownerIndexPromise,d=own(manifest?.[group]||{},id)?manifest[group][id]:null;
    if(manifest?.version!==16||!d||!/^[a-f0-9]{64}$/.test(d.sha256)||!Number.isSafeInteger(d.byteLength)||d.byteLength<2||d.byteLength>LIMIT||d.file!==`data/lazy/owner-${group}/${id}-${d.sha256.slice(0,16)}.json`||d.script!==d.file.replace(/\.json$/,'.js'))throw Error('Invalid owner content descriptor.');
    return readDescriptor(d);
  }
  async function course(id,{protected:protectedMode=false,owner=false}={}){
    if(!validID(id))throw Error('Invalid course ID.');
    // No shared promise/cache here: two identities cannot share private content.
    const value=protectedMode?(await json('/api/curriculum?courseId='+encodeURIComponent(id),LIMIT,'no-store')).value:owner&&location?.protocol==='file:'?await ownerChunk('courses',id):await chunk('courses',id);
    if(!value||value.id!==id||typeof value.title!=='string')throw Error('Course contents do not match the request.');
    return clone(value);
  }
  async function resources(id,{protected:protectedMode=false,owner=false}={}){
    if(!validID(id))throw Error('Invalid course ID.');
    const value=protectedMode?(await json('/api/curriculum?resources='+encodeURIComponent(id),LIMIT,'no-store')).value:owner&&location?.protocol==='file:'?await ownerChunk('resources',id):await chunk('resources',id);
    return clone(value);
  }
  async function data(name,options={}){
    if(name==='featured'&&options.protected){const value=(await json('/api/curriculum?index=1',12*1024*1024,'no-store')).value;if(!Array.isArray(value)||value.some(c=>!validID(c?.id)||!Array.isArray(c.stages)||(c.locked&&c.stages.length)))throw Error('Invalid protected curriculum index.');return value;}
    if(CORE.has(name)){const value=await index();return name==='featured'?value.guidedIds.map(id=>value.catalog.find(c=>c.id===id)):value[name];}
    return chunk('auxiliary',name);
  }
  return {index,data:(name,options={})=>waitFor(()=>data(name,options),options.signal),course:(id,options={})=>waitFor(()=>course(id,options),options.signal),resources:(id,options={})=>waitFor(()=>resources(id,options),options.signal),auxiliary:name=>chunk('auxiliary',name)};
}
let defaultLoader;
function loader(){if(!defaultLoader){defaultLoader=createCurriculumLoader();if(globalThis.window)globalThis.window.MG_LOAD_AUXILIARY=name=>defaultLoader.auxiliary(name);}return defaultLoader;}
export function loadCurriculumIndex(){return loader().index();}
export function loadCurriculumData(name,options={}){if(options.data&&Object.prototype.hasOwnProperty.call(options.data,name)&&!options.protected)return Promise.resolve(options.data[name]);return (options.fetchImpl?createCurriculumLoader({fetchImpl:options.fetchImpl,view:options.data===null?{}:globalThis.window}):loader()).data(name,options);}
export function loadCourseOnDemand(id,options={}){return loader().course(id,options);}
export function loadCourseResources(id,options={}){return loader().resources(id,options);}
export function loadAuxiliaryData(name){return loader().auxiliary(name);}
