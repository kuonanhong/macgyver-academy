/* Optional Supabase Auth + RLS persistence for static hosts. No admin credentials. */
const CLOUD_PROJECT_ID=/^[a-zA-Z0-9_-]{1,100}$/;
const CLOUD_STEP_ID=/^[a-zA-Z0-9_.:-]{1,100}$/;
function cloudError(message,code='cloud',current=null){const e=new Error(message);e.code=code;e.current=current;return e;}
function cloudConfiguration(config){
  const raw=String(config?.supabaseUrl||'').trim(),key=String(config?.supabasePublishableKey||'').trim();
  if(!raw&&!key)return null;
  try{const u=new URL(raw);if(u.protocol!=='https:'||u.username||u.password||u.search||u.hash||u.pathname!=='/'||!key)throw Error();
    // Secret/service-role keys must never enter a published browser bundle.
    if(key.startsWith('sb_secret_'))throw Error();
    if(key.startsWith('eyJ')){const part=key.split('.')[1];const payload=JSON.parse(atob(part.replace(/-/g,'+').replace(/_/g,'/')));if(payload.role!=='anon')throw Error();}
    else if(!key.startsWith('sb_publishable_'))throw Error();
    return {url:u.origin,key};
  }catch{throw cloudError('Use a valid HTTPS Supabase URL and publishable (or legacy anon) key. Never use a service-role key.','configuration');}
}
export function sanitizeCloudProgress(value){
  if(!value||typeof value!=='object'||Array.isArray(value))throw cloudError('Invalid progress.','validation');
  const ids=v=>{if(!Array.isArray(v)||v.length>5000||v.some(x=>typeof x!=='string'||!CLOUD_STEP_ID.test(x)))throw cloudError('Invalid step identifiers.','validation');return [...new Set(v)];};
  if(typeof value.notes!=='string'||value.notes.length>20000)throw cloudError('Notes must be at most 20,000 characters.','validation');
  return {completed:ids(value.completed),assembly:ids(value.assembly),notes:value.notes};
}
export function createCloudSync({config=globalThis.MG_CONFIG||{},storage=globalThis.localStorage,fetcher=globalThis.fetch?.bind(globalThis),onAuthChange=()=>{},location=globalThis.location,history=globalThis.history}={}){
  let conf=null,configurationError=null;try{conf=cloudConfiguration(config);}catch(e){configurationError=e;}
  const key=conf?'mg-cloud-session:'+conf.url:'mg-cloud-unconfigured';let session=null,refreshing=null,generation=0;
  try{const raw=JSON.parse(storage?.getItem(key)||'null');if(raw?.refresh_token&&raw?.access_token&&raw?.user?.id&&Number.isFinite(raw.expires_at))session=raw;}catch{}
  const publicSession=()=>session?{user:{id:session.user.id,name:session.user.user_metadata?.name||session.user.email?.split('@')[0]||'Learner',email:session.user.email||''},expiresAt:session.expires_at*1000}:null;
  function persist(value){session=value;try{value?storage?.setItem(key,JSON.stringify(value)):storage?.removeItem(key);}catch{}onAuthChange(publicSession());}
  const requireConfigured=()=>{if(!conf)throw configurationError||cloudError('Cloud accounts are not configured by the site owner.','unconfigured');};
  async function request(path,{method='GET',body,token,signal}={}){
    requireConfigured();const controller=new AbortController(),timeout=setTimeout(()=>controller.abort(),20000);const abort=()=>controller.abort();signal?.addEventListener('abort',abort,{once:true});
    try{const res=await fetcher(conf.url+path,{method,headers:{apikey:conf.key,...(body?{'Content-Type':'application/json'}:{}),...(token?{Authorization:'Bearer '+token}:{})},body:body?JSON.stringify(body):undefined,signal:controller.signal,credentials:'omit',redirect:'error'});
      const raw=await res.text();if(raw.length>2000000)throw cloudError('Cloud response too large.');let data;try{data=raw?JSON.parse(raw):null;}catch{throw cloudError('Invalid cloud response.');}
      if(!res.ok){const code=data?.code==='MG409'?'conflict':res.status===401?'auth':'cloud';throw cloudError(data?.msg||data?.error_description||data?.message||'Cloud request failed.',code);}
      return data;
    }finally{clearTimeout(timeout);signal?.removeEventListener('abort',abort);}
  }
  function normalizeSession(data){if(!data?.access_token||!data?.refresh_token||!data?.user?.id)throw cloudError('No verified session was returned.','auth');return {...data,expires_at:Number(data.expires_at)||Math.floor(Date.now()/1000)+Number(data.expires_in||3600)};}
  async function token(){
    requireConfigured();if(!session)throw cloudError('Sign in to sync learning progress.','auth');
    if(session.expires_at*1000>Date.now()+60000)return session.access_token;
    if(!refreshing){const turn=generation,refreshToken=session.refresh_token;const action=async()=>{try{
      // Re-read after an optional cross-tab lock, because refresh tokens rotate.
      try{const shared=JSON.parse(storage?.getItem(key)||'null');if(shared?.user?.id===session?.user?.id&&shared.expires_at>session.expires_at)session=shared;}catch{}
      if(session?.expires_at*1000>Date.now()+60000)return session.access_token;
      const data=normalizeSession(await request('/auth/v1/token?grant_type=refresh_token',{method:'POST',body:{refresh_token:session?.refresh_token||refreshToken}}));
      if(turn!==generation||data.user.id!==session?.user?.id)throw cloudError('Session changed.','auth');persist(data);return data.access_token;
    }catch(e){if(turn===generation&&e.code==='auth')persist(null);throw e;}};
      const locks=globalThis.navigator?.locks;refreshing=(locks?locks.request(key,action):action()).finally(()=>{refreshing=null;});
    }return refreshing;
  }
  function redirectURL(){if(!location||!/^https?:$/.test(location.protocol))throw cloudError('Email verification needs the HTTPS website, not a file:// page.','configuration');return location.origin+location.pathname;}
  const passwordCheck=p=>{if(typeof p!=='string'||p.length<12||p.length>128)throw cloudError('Use a password of 12–128 characters.','validation');};
  const credentials=v=>{if(typeof v.email!=='string'||v.email.length>254||!/^\S+@\S+\.\S+$/.test(v.email))throw cloudError('Enter a valid email.','validation');passwordCheck(v.password);return {email:v.email.trim(),password:v.password};};
  function rowValue(row){const p=sanitizeCloudProgress(row.payload);return {...p,revision:Number(row.revision),updatedAt:Number(row.revision)};}
  async function getRow(projectId,access){const rows=await request('/rest/v1/academy_progress?select=project_id,payload,revision&project_id=eq.'+encodeURIComponent(projectId),{token:access});return rows?.[0]?rowValue(rows[0]):null;}
  return {
    configured:!!conf,configurationError:configurationError?.message||'',
    async signUp(value){const cred=credentials(value);const name=String(value.name||'').trim();if(!name||name.length>100)throw cloudError('Name must be 1–100 characters.','validation');
      const turn=++generation;const data=await request('/auth/v1/signup?redirect_to='+encodeURIComponent(redirectURL()),{method:'POST',body:{...cred,data:{name}}});
      if(turn!==generation)throw cloudError('Session changed.','auth');if(data?.access_token){persist(normalizeSession(data));}return {user:publicSession()?.user||null,verificationRequired:!data?.access_token};},
    async signIn(value){const cred=credentials(value),turn=++generation;const data=normalizeSession(await request('/auth/v1/token?grant_type=password',{method:'POST',body:cred}));if(turn!==generation)throw cloudError('Session changed.','auth');persist(data);return publicSession();},
    async resetPassword(email){if(typeof email!=='string'||!/^\S+@\S+\.\S+$/.test(email))throw cloudError('Enter a valid email.','validation');await request('/auth/v1/recover?redirect_to='+encodeURIComponent(redirectURL()),{method:'POST',body:{email:email.trim()}});return {sent:true};},
    async updatePassword(password){passwordCheck(password);const turn=generation,owner=session?.user?.id;const access=await token();if(turn!==generation||session?.user?.id!==owner)throw cloudError('Session changed.','auth');await request('/auth/v1/user',{method:'PUT',token:access,body:{password}});if(turn!==generation||session?.user?.id!==owner)throw cloudError('Session changed.','auth');return {updated:true};},
    async signOut(){const old=session?.access_token;generation++;persist(null);if(old)try{await request('/auth/v1/logout?scope=local',{method:'POST',token:old});}catch{/* Local sign-out always succeeds, even offline. */}},
    async getSession(){if(!conf||!session)return null;const turn=generation,owner=session.user.id;try{const access=await token();if(turn!==generation||session?.user?.id!==owner)return null;const user=await request('/auth/v1/user',{token:access});if(turn!==generation)return null;if(!user?.id||user.id!==session?.user?.id)throw cloudError('Session identity changed.','auth');session.user=user;return publicSession();}catch(e){if(e.code==='auth'&&turn===generation)persist(null);throw e;}},
    async handleRedirect(){if(!conf||!location?.hash?.includes('access_token='))return {handled:false,recovery:false};const params=new URLSearchParams(location.hash.slice(1));const access=params.get('access_token'),refresh=params.get('refresh_token'),recovery=params.get('type')==='recovery';history?.replaceState(null,'',location.pathname+location.search);if(!access||!refresh)throw cloudError('Incomplete verification link.','auth');
      const turn=++generation;const user=await request('/auth/v1/user',{token:access});if(turn!==generation)throw cloudError('Session changed.','auth');persist(normalizeSession({access_token:access,refresh_token:refresh,expires_in:Number(params.get('expires_in'))||3600,user}));return {handled:true,recovery};},
    async loadProgress(){const turn=generation,owner=session?.user?.id;const access=await token();if(turn!==generation||session?.user?.id!==owner)throw cloudError('Session changed while loading.','auth');let result=Object.create(null);for(let offset=0;offset<20000;offset+=500){const rows=await request('/rest/v1/academy_progress?select=project_id,payload,revision&order=project_id&limit=500&offset='+offset,{token:access});if(turn!==generation||session?.user?.id!==owner)throw cloudError('Session changed while loading.','auth');for(const row of rows||[])if(CLOUD_PROJECT_ID.test(row.project_id))result[row.project_id]=rowValue(row);if((rows||[]).length<500)return result;}throw cloudError('Too many progress records.');},
    async saveProgress(projectId,value,expectedRevision=null){if(!CLOUD_PROJECT_ID.test(projectId))throw cloudError('Invalid project ID.','validation');const payload=sanitizeCloudProgress(value);if(expectedRevision!==null&&(!Number.isSafeInteger(expectedRevision)||expectedRevision<1))throw cloudError('Invalid revision.','validation');const turn=generation,owner=session?.user?.id;const access=await token();if(turn!==generation||session?.user?.id!==owner)throw cloudError('Session changed while saving.','auth');
      try{const data=await request('/rest/v1/rpc/academy_save_progress',{method:'POST',token:access,body:{p_project_id:projectId,p_payload:payload,p_expected_revision:expectedRevision}});if(turn!==generation||session?.user?.id!==owner)throw cloudError('Session changed while saving.','auth');return rowValue(Array.isArray(data)?data[0]:data);}
      catch(e){if(e.code==='conflict'&&turn===generation&&session?.user?.id===owner){const current=await getRow(projectId,access);if(turn!==generation||session?.user?.id!==owner)throw cloudError('Session changed while reading a conflict.','auth');e.current=current;}throw e;}}
  };
}
