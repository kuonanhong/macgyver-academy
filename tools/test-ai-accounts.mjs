import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import fs from 'node:fs';
import {createModelHasher,createAIClient,AI_MODELS,compactTutorContext} from '../public/academy/ai-client.js';
import {createCloudSync,sanitizeCloudProgress} from '../public/academy/cloud-sync.js';
const memory=()=>{const m=new Map();return {getItem:k=>m.get(k)||null,setItem:(k,v)=>m.set(k,v),removeItem:k=>m.delete(k)};};
for(const n of [0,1,55,56,63,64,65,1024,1000000]){const bytes=crypto.randomBytes(n),h=createModelHasher();for(let i=0;i<n;i+=137)h.update(bytes.subarray(i,i+137));assert.equal(h.hex(),crypto.createHash('sha256').update(bytes).digest('hex'));}
assert.equal(AI_MODELS.filter(m=>m.kind==='browser').length,2);
let calls=0;const unconfigured=createCloudSync({config:{},storage:memory(),fetcher:()=>{calls++;}});assert.equal(unconfigured.configured,false);assert.equal(await unconfigured.getSession(),null);await assert.rejects(()=>unconfigured.loadProgress(),e=>e.code==='unconfigured');assert.equal(calls,0);
assert.equal(createCloudSync({config:{supabaseUrl:'https://fake.supabase.co',supabasePublishableKey:'sb_secret_PRIVATE'}}).configured,false);
assert.throws(()=>sanitizeCloudProgress({completed:[],assembly:[],notes:'x'.repeat(20001)}));
const config={supabaseUrl:'https://fake.supabase.co',supabasePublishableKey:'sb_publishable_demo'};
const good={completed:['a:1'],assembly:['a:1'],notes:'engineering note'};
const storage=memory();let responseQueue=[],seen=[];
const cloud=createCloudSync({config,storage,location:{origin:'https://owner.github.io',pathname:'/academy/',protocol:'https:',hash:''},fetcher:async(url,options)=>{seen.push({url,options});const [status,body]=responseQueue.shift();return new Response(JSON.stringify(body),{status});}});
const login={access_token:'access-token',refresh_token:'refresh-token',expires_in:3600,user:{id:'owner1',email:'owner@example.org',user_metadata:{name:'Owner'}}};
responseQueue.push([200,login]);assert.equal((await cloud.signIn({email:'owner@example.org',password:'a password of length'})).user.id,'owner1');
assert.equal(seen[0].options.credentials,'omit');assert.equal(JSON.parse(seen[0].options.body).password,'a password of length');
responseQueue.push([200,[{payload:good,revision:1750000000000}]]);const saved=await cloud.saveProgress('a001',good,null);assert.equal(saved.updatedAt,1750000000000);assert.equal(JSON.parse(seen.at(-1).options.body).p_expected_revision,null);
responseQueue.push([400,{code:'MG409',message:'Conflict'}],[200,[{payload:{...good,notes:'remote'},revision:1750000000001}]]);await assert.rejects(()=>cloud.saveProgress('a001',good,1750000000000),e=>e.code==='conflict'&&e.current.notes==='remote');
responseQueue.push([200,[{project_id:'a001',payload:good,revision:1750000000001}]]);assert.equal((await cloud.loadProgress()).a001.revision,1750000000001);
responseQueue.push([200,{id:'owner2'}]);await assert.rejects(()=>cloud.getSession(),e=>e.code==='auth');assert.equal(await cloud.getSession(),null);
const wrongKey=btoa(JSON.stringify({role:'service_role'}));assert.equal(createCloudSync({config:{...config,supabasePublishableKey:'eyJ.'+wrongKey+'.sig'}}).configured,false);
const sql=fs.readFileSync(new URL('../supabase/001_learning_progress.sql',import.meta.url),'utf8');assert.match(sql,/enable row level security/i);assert.match(sql,/security invoker/i);assert.match(sql,/revision=p_expected_revision/);assert.match(sql,/revoke all.*public,anon/);assert.equal((sql.match(/auth\.uid\(\)/g)||[]).length,6);
const tinyBytes=new TextEncoder().encode('TEST GGUF fixture'),tiny={id:'test',kind:'browser',bytes:tinyBytes.length,minMemoryGB:1,sha256:crypto.createHash('sha256').update(tinyBytes).digest('hex'),repo:'test/test',revision:'pin',file:'test.gguf'};
const env={location:{protocol:'https:',origin:'https://owner.github.io',href:'https://owner.github.io/academy/'},document:{baseURI:'https://owner.github.io/academy/'},Worker:class{},WebAssembly:{},navigator:{deviceMemory:8,hardwareConcurrency:8}};
let inference=0,exits=0,settings;class FakeWllama{setCompat(){} async loadModel(blobs,options){assert.equal(await blobs[0].text(),'TEST GGUF fixture');settings=options;}async exit(){exits++;}async createChatCompletion(options){inference++;assert.match(options.messages[1].content,/QUESTION: Explain/);return (async function*(){yield {choices:[{delta:{content:'Actual engine reply'}}]};})();}}
const ai=createAIClient({environment:env,models:[tiny],fetcher:async()=>{calls++;return new Response(tinyBytes);},importer:async()=>({Wllama:FakeWllama})});
const before=calls;await assert.rejects(()=>ai.load('test'),e=>e.code==='consent');assert.equal(calls,before);await ai.load('test',{consent:true});assert.equal(settings.n_gpu_layers,0);assert.equal(settings.n_threads,1);assert.equal(ai.state().phase,'ready');assert.equal((await ai.ask({question:'Explain this process',context:{objective:'Learn'}})).answer,'Actual engine reply');assert.equal(inference,1);await ai.unload();assert.equal(ai.state().phase,'idle');assert.equal(exits,1);
let aborted=false;const cancelling=createAIClient({environment:env,models:[tiny],fetcher:async(url,{signal})=>new Promise((resolve,reject)=>signal.addEventListener('abort',()=>{aborted=true;reject(new DOMException('Cancelled','AbortError'));})),importer:async()=>({Wllama:FakeWllama})});const pending=cancelling.load('test',{consent:true});await new Promise(r=>setTimeout(r,0));cancelling.cancel();await assert.rejects(()=>pending,e=>e.name==='AbortError');assert.equal(aborted,true);assert.equal(cancelling.state().phase,'idle');
const bad=createAIClient({environment:env,models:[tiny],fetcher:async()=>new Response('wrong fixture'),importer:async()=>{throw Error('Should never import invalid weights');}});await assert.rejects(()=>bad.load('test',{consent:true}),e=>e.code==='integrity');
assert.equal(createAIClient({environment:{...env,location:{protocol:'file:'}}}).capabilities().supported,false);
const compact=JSON.parse(compactTutorContext({sources:[{id:'official',title:'Official title',url:'https://example.org/source'}],instruction:'Very long instructions'.repeat(1000),knowledge:[{title:'Test',text:'x'.repeat(4000)}]}));assert.equal(compact.sources[0].url,'https://example.org/source');assert.ok(JSON.stringify(compact).length<=3200);
// A pending login must not undo a newer explicit sign-out.
let releaseLogin;const racing=createCloudSync({config,storage:memory(),fetcher:()=>new Promise(resolve=>{releaseLogin=resolve;})});
const oldLogin=racing.signIn({email:'owner@example.org',password:'a password of length'});await racing.signOut();releaseLogin(new Response(JSON.stringify(login),{status:200}));await assert.rejects(()=>oldLogin,e=>e.code==='auth');assert.equal(await racing.getSession(),null);
// A queued read from identity A cannot return A's data after identity B starts signing in.
let reads=0;const identities=createCloudSync({config,storage:memory(),fetcher:async url=>{if(url.includes('/token'))return new Response(JSON.stringify(reads++?{...login,user:{id:'owner2',email:'two@example.org'}}:login));throw Error('A stale identity must not request rows');}});
await identities.signIn({email:'owner@example.org',password:'a password of length'});const oldRead=identities.loadProgress();const newLogin=identities.signIn({email:'two@example.org',password:'another password'});await assert.rejects(()=>oldRead,e=>e.code==='auth');await newLogin;
assert.deepEqual(JSON.parse(fs.readFileSync(new URL('../tools/model-manifest.json',import.meta.url))).models,AI_MODELS);
const lock=JSON.parse(fs.readFileSync(new URL('../public/academy/vendor/wllama/LOCK.json',import.meta.url)));for(const[file,hash]of Object.entries(lock.files)){assert.equal(crypto.createHash('sha256').update(fs.readFileSync(new URL('../public/academy/vendor/wllama/'+file,import.meta.url))).digest('hex'),hash);}
console.log('PASS: incremental SHA-256, consent, cancellation, real engine adapter contract, CPU settings, tamper rejection, native/file fallback, unconfigured no-network, auth isolation, CAS conflict and pinned runtime checks.');
