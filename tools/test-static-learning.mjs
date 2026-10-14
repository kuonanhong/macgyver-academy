import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import {webcrypto} from 'node:crypto';
const legacyRow={completed:['sc-001'],assembly:['sc-001'],notes:'V7 retained',updatedAt:1234};
const legacy=JSON.stringify({semiconductor:legacyRow,bad:{notes:42}});
const data=new Map([['mg-progress-guest',legacy]]),network=[];
const storage={get length(){return data.size},key:i=>[...data.keys()][i]??null,getItem:k=>data.get(k)??null,setItem:(k,v)=>data.set(k,String(v)),removeItem:k=>data.delete(k)};
const location=new URL('https://example.github.io/macgyver-academy/index.html');
const originalFetch=async (input,options)=>{network.push(String(input));return new Response(JSON.stringify({resource:true}),{headers:{'Content-Type':'application/json'}})};
const globals={URL,Response,Request,JSON,Date,Map,Set,Error,Number,crypto:webcrypto,location,localStorage:storage,fetch:originalFetch,MG_STATIC_MODE:true,MG_CONFIG:{},MacGyverNativeFetch:originalFetch};
globals.window=globals;let context=vm.createContext(globals);
const runtime=fs.readFileSync(new URL('../public/academy/offline-runtime.js',import.meta.url),'utf8');
vm.runInContext(runtime,context);
const api=context.MacGyverOffline;
const first=api.activeProfile();assert(first.id.startsWith('offline-'));
assert.equal((await (await context.fetch('/api/progress')).json()).projects.semiconductor.notes,'V7 retained');
assert.equal(data.get('mg-progress-guest'),legacy);
assert(!Object.hasOwn((await (await context.fetch('/api/progress')).json()).projects,'bad'));
const named=api.createProfile('Test learner','learner@example.test');assert.equal(named.email,'learner@example.test');
assert.throws(()=>api.createProfile('Bad','not-an-email'));
const me=await (await context.fetch('/api/me')).json();assert.equal(me.user.id,named.id);assert.equal(me.authMode,'offline');assert.equal(me.user.email,named.email);
const row={projectId:'a003',completed:['a003-v8-01'],assembly:['a003-v8-01'],notes:'First learner',baseUpdatedAt:null};
let response=await context.fetch('/api/progress',{method:'PUT',body:JSON.stringify(row)});assert.equal(response.status,200);const saved=await response.json();
assert.equal((await context.fetch('/api/progress',{method:'PUT',body:JSON.stringify(row)})).status,409);
assert.equal((await (await context.fetch('/api/progress')).json()).projects.a003.notes,'First learner');
api.switchProfile(first.id);assert.equal((await (await context.fetch('/api/progress')).json()).projects.semiconductor.notes,'V7 retained');api.switchProfile(named.id);
await context.fetch('data/catalog.json');assert.deepEqual(network,['data/catalog.json']);
assert.equal((await context.fetch('https://unrequested.example/api')).status,503);
assert.equal(network.length,1);
// Same-origin local profiles persist across a new page instance without a server.
const second={...globals,window:null,fetch:originalFetch,localStorage:storage};second.window=second;const reloaded=vm.createContext(second);vm.runInContext(runtime,reloaded);
assert.equal(reloaded.MacGyverOffline.activeProfile().id,named.id);
assert.equal((await (await reloaded.fetch('/api/progress')).json()).projects.a003.updatedAt,saved.updatedAt);
// The bridge must preserve HTTP conflict errors and never fall back to local
// profile writes after an authenticated cloud failure.
let session=null,cloudRecords={},calls=0,fail=false,notifyAuth=null;
context.createCloudSync=({onAuthChange})=>{notifyAuth=onAuthChange;return {configured:true,handleRedirect:async()=>({handled:false}),getSession:async()=>session,
 signIn:async value=>{const id=value.email==='b@example.test'?'cloud-B':'cloud-A';session={user:{id,name:id,email:value.email}};onAuthChange(session);return session},
 signUp:async()=>({verificationRequired:true}),signOut:async()=>{session=null;onAuthChange(null)},
 loadProgress:async()=>cloudRecords,
 saveProgress:async(id,payload,revision)=>{calls++;if(fail)throw Object.assign(new Error('Changed elsewhere'),{code:'conflict',current:{notes:'Cloud changed',updatedAt:3000}});assert.equal(revision,null);const value={...payload,updatedAt:2000,revision:2000};cloudRecords[id]=value;return value}
};};
const services=fs.readFileSync(new URL('../public/academy/services.js',import.meta.url),'utf8').replace(/^import[^\n]+\n/,'').replace('export async function','async function');
vm.runInContext(services,context);await vm.runInContext('initializeServices()',context);
assert.equal((await (await context.fetch('/api/me')).json()).authMode,'offline');
await context.MacGyverCloud.signIn({email:'a@example.test',password:'not-a-real-password'});
assert.equal((await (await context.fetch('/api/me')).json()).authMode,'supabase');
response=await context.fetch('/api/progress',{method:'PUT',body:JSON.stringify({...row,notes:'Cloud only'})});assert.equal(response.status,200);assert.equal((await response.json()).updatedAt,2000);
fail=true;response=await context.fetch('/api/progress',{method:'PUT',body:JSON.stringify({...row,baseUpdatedAt:2000,notes:'must not land locally'})});assert.equal(response.status,409);assert.equal((await response.json()).current.notes,'Cloud changed');assert.equal(calls,2);
// Request bodies can be asynchronous streams. Never read an A payload and
// write it as B if sign-in changes while the stream is being consumed.
fail=false;let releaseBody;const beforeRace=calls;
const streamedRequest={url:location.origin+'/api/progress',method:'PUT',text:()=>new Promise(resolve=>{releaseBody=resolve})};
const oldRequest=context.fetch(streamedRequest);await context.MacGyverCloud.signIn({email:'b@example.test',password:'not-a-real-password'});releaseBody(JSON.stringify({...row,notes:'Private A streaming body'}));const changed=await oldRequest;assert.equal(changed.status,401);assert.equal(calls,beforeRace,'A request cannot reach B save');assert(!Object.values(cloudRecords).some(v=>v.notes==='Private A streaming body'));
// Refreshing tokens for the same account must not interrupt a legitimate save.
let releaseSameOwner;const sameOwner=context.fetch({url:location.origin+'/api/progress',method:'PUT',text:()=>new Promise(resolve=>{releaseSameOwner=resolve})});notifyAuth(session);releaseSameOwner(JSON.stringify({...row,notes:'B after token refresh'}));assert.equal((await sameOwner).status,200);assert.equal(calls,beforeRace+1);
// Explicit same-user reauthentication still invalidates requests queued under
// the earlier authentication action, including logout/sign-in cycles.
let releaseRelogin;const relogin=context.fetch({url:location.origin+'/api/progress',method:'PUT',text:()=>new Promise(resolve=>{releaseRelogin=resolve})});await context.MacGyverCloud.signIn({email:'b@example.test',password:'not-a-real-password'});releaseRelogin(JSON.stringify({...row,notes:'Before reauthentication'}));assert.equal((await relogin).status,401);assert.equal(calls,beforeRace+1);
await context.MacGyverCloud.signOut();assert.equal((await (await context.fetch('/api/me')).json()).user.id,named.id);
assert.equal((await (await context.fetch('/api/progress')).json()).projects.a003.notes,'First learner');
// A token refresh can persist credentials before the identity check fails.
// Merely retrying that check must not switch a local learning profile to cloud.
const retryGlobals={...globals,fetch:originalFetch,localStorage:storage};retryGlobals.window=retryGlobals;
const retryContext=vm.createContext(retryGlobals);vm.runInContext(runtime,retryContext);
let retrySession={user:{id:'cloud-retry',name:'Returning learner',email:'retry@example.test'}},failIdentity=true,holdIdentity=null,resumeWrites=0;
const retainedLocal=data.get('mg-progress-'+named.id);
retryContext.createCloudSync=({onAuthChange})=>({configured:true,handleRedirect:async()=>({handled:false}),getSession:async()=>{onAuthChange(retrySession);if(holdIdentity)return holdIdentity;if(failIdentity)throw Error('Temporary identity network failure');return retrySession},signOut:async()=>{retrySession=null;onAuthChange(null)},loadProgress:async()=>({a003:{completed:['cloud-step'],assembly:['cloud-step'],notes:'Cloud retained',updatedAt:7000}}),saveProgress:async()=>{resumeWrites++;return{updatedAt:8000}}});
vm.runInContext(services,retryContext);await vm.runInContext('initializeServices()',retryContext);
assert(retryContext.MacGyverCloudStartupError.includes('network failure'));
assert.equal((await (await retryContext.fetch('/api/me')).json()).user.id,named.id,'failed startup stays local even if a token refresh fired');
failIdentity=false;assert.equal((await retryContext.MacGyverCloud.getSession()).user.id,'cloud-retry');
assert.equal((await (await retryContext.fetch('/api/me')).json()).authMode,'offline','session inspection alone does not resume cloud learning');
await retryContext.MacGyverCloud.resumeSession({expectedUserId:'cloud-retry'});
assert.equal((await (await retryContext.fetch('/api/me')).json()).user.id,'cloud-retry');
assert.equal((await (await retryContext.fetch('/api/progress')).json()).projects.a003.notes,'Cloud retained');
assert.equal(data.get('mg-progress-'+named.id),retainedLocal,'resuming cloud preserves the separate local profile');
assert.equal(resumeWrites,0,'resume never uploads local records');assert.equal(retryContext.MacGyverCloudStartupError,undefined);
assert.equal((await retryContext.fetch('/api/progress',{method:'PUT',body:JSON.stringify({...row,ownerId:named.id})})).status,401,'save captured during the UI transition cannot enter another owner');assert.equal(resumeWrites,0);
assert.equal((await retryContext.fetch('/api/progress',{method:'PUT',body:JSON.stringify({...row,ownerId:'cloud-retry'})})).status,200);assert.equal(resumeWrites,1);
await retryContext.MacGyverCloud.signOut();assert.equal((await (await retryContext.fetch('/api/progress')).json()).projects.a003.notes,'First learner');
retrySession={user:{id:'cloud-retry'}};let releaseResume;holdIdentity=new Promise(resolve=>{releaseResume=resolve});
const staleResume=retryContext.MacGyverCloud.resumeSession({expectedUserId:'cloud-retry'});const rejectedResume=assert.rejects(staleResume,/changed/);await retryContext.MacGyverCloud.signOut();releaseResume({user:{id:'cloud-retry'}});await rejectedResume;holdIdentity=null;
assert.equal((await (await retryContext.fetch('/api/me')).json()).authMode,'offline','late resume cannot undo explicit logout');
// An old cloud view cannot land a late save in the local profile after logout.
await context.MacGyverCloud.signOut();
assert.equal((await context.fetch('/api/progress',{method:'PUT',body:JSON.stringify({...row,ownerId:'cloud-A',notes:'wrong destination'})})).status,401);
assert.equal((await (await context.fetch('/api/progress')).json()).projects.a003.notes,'First learner');
console.log('PASS: static HTTPS profiles, persistence, isolation, CAS, optional cloud bridge, streamed-body account guards, startup retry with explicit resume, local retention, transition owner guards and no local fallback on cloud conflict.');
