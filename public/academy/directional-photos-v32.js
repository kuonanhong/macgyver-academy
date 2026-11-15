/* Shared by the real photo UI and its persistence tests. No network access. */
(function(root){'use strict';
 const DIRECTIONS=Object.freeze(['front','back','left','right','up','down']);
 function identity(domain,site,direction){
  for(const value of [domain,site])if(typeof value!=='string'||!value.trim()||value.length>160)throw TypeError('Invalid scene identity');
  if(direction!==undefined&&!DIRECTIONS.includes(direction))throw TypeError('Invalid photo direction');
  return {scope:JSON.stringify([domain,site]),id:JSON.stringify([domain,site,direction]),legacyScope:domain+':'+site,legacyId:domain+':'+site+':'+direction};
 }
 function createPhotoStore(factory,options={}){
  const name=options.name||'macgyver-directional-photos';let opening=null,connection=null;
  function open(){
   if(connection)return Promise.resolve(connection);
   if(!opening)opening=new Promise((resolve,reject)=>{
    if(!factory)return reject(Error('IndexedDB unavailable'));
    let request;try{request=factory.open(name,1);}catch(error){reject(error);return;}
    let rejected=false;
    request.onupgradeneeded=()=>{if(!request.result.objectStoreNames.contains('photos'))request.result.createObjectStore('photos',{keyPath:'id'});};
    request.onsuccess=()=>{if(rejected){request.result.close();return;}connection=request.result;connection.onversionchange=()=>{connection?.close();connection=null;opening=null;};resolve(connection);};
    request.onerror=()=>reject(request.error||Error('Unable to open photo storage'));
    request.onblocked=()=>{rejected=true;reject(Error('Storage is busy in another tab'));};
   }).catch(error=>{opening=null;throw error;});
   return opening;
  }
  async function transaction(mode,operate){
   const handle=await open();return new Promise((resolve,reject)=>{
    let tx,result;
    try{tx=handle.transaction('photos',mode);const request=operate(tx.objectStore('photos'));if(request)request.onsuccess=()=>{result=request.result;};}
    catch(error){try{tx?.abort();}catch{}reject(error);return;}
    // Request success is not a durable write until the transaction commits.
    tx.oncomplete=()=>resolve(result);tx.onabort=tx.onerror=()=>reject(tx.error||Error('Photo storage transaction failed'));
   });
  }
  async function get(domain,site,direction){const key=identity(domain,site,direction);return await transaction('readonly',s=>s.get(key.id))||await transaction('readonly',s=>s.get(key.legacyId));}
  async function put(value){
   const {domain,site,direction}=value,key=identity(domain,site,direction);
   if(!value.blob||typeof value.blob.size!=='number'||value.blob.size<=0||value.blob.size>12*1024*1024||!['image/jpeg','image/png','image/webp'].includes(value.blob.type))throw TypeError('Invalid stored photo');
   const record={id:key.id,scope:key.scope,domain,site,direction,blob:value.blob,by:String(value.by||'').trim().slice(0,240),rights:String(value.rights||'').trim().slice(0,240),updatedAt:new Date().toISOString()};
   await transaction('readwrite',s=>{s.delete(key.legacyId);return s.put(record);});return record;
  }
  async function list(domain,site){const key=identity(domain,site),rows=await transaction('readonly',s=>s.getAll());const found=new Map();for(const row of rows){if(row.scope===key.legacyScope&&DIRECTIONS.includes(row.direction))found.set(row.direction,row);}for(const row of rows){if(row.scope===key.scope&&DIRECTIONS.includes(row.direction))found.set(row.direction,row);}return DIRECTIONS.filter(d=>found.has(d)).map(d=>found.get(d));}
  async function remove(domain,site,direction){const key=identity(domain,site,direction);await transaction('readwrite',s=>{s.delete(key.legacyId);return s.delete(key.id);});}
  async function close(){if(opening)await opening.catch(()=>{});connection?.close();connection=null;opening=null;}
  return Object.freeze({get,put,list,remove,close,scope:(domain,site)=>identity(domain,site).scope});
 }
 const api={createPhotoStore,DIRECTIONS};if(typeof module==='object'&&module.exports)module.exports=api;root.MG_DIRECTIONAL_PHOTOS_V32=api;
})(typeof window==='undefined'?globalThis:window);
