// Exercise the real controller with a minimal DOM and deterministic renderer.
// No browser or WebGL is simulated: these checks cover account/role/station
// transitions, note ownership and renderer callback ordering only.
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import test from 'node:test';
import {newWalkRecord,restoreWalkRecord} from '../public/academy/walk-state-v22.js';
import {buildWorldConfig} from '../public/academy/walk-domains-v22.js';
import {resolveLanguage,uiText,languageChoices} from '../public/academy/walk-i18n-v22.js';

const source=fs.readFileSync(new URL('../public/academy/walk-v22.js',import.meta.url),'utf8').replace(/^import .*;\s*$/gm,'');
const html=fs.readFileSync(new URL('../public/academy/experience.html',import.meta.url),'utf8');
const decode=s=>String(s).replace(/&(amp|lt|gt|quot|#39);/g,(_,v)=>({amp:'&',lt:'<',gt:'>',quot:'"','#39':"'"}[v]));

class Element {
  constructor(doc,tag='div',attrs={}){this.doc=doc;this.tagName=tag.toUpperCase();this.attrs={...attrs};this.id=attrs.id||'';this.dataset={};this.hidden='hidden' in attrs;this.open=false;this.style={};this.value=decode(attrs.value||'');this.children=[];this.listeners=new Map();this.classNames=new Set((attrs.class||'').split(/\s+/).filter(Boolean));this.classList={add:(...v)=>v.forEach(x=>this.classNames.add(x)),remove:(...v)=>v.forEach(x=>this.classNames.delete(x)),toggle:(v,on)=>{const set=on??!this.classNames.has(v);set?this.classNames.add(v):this.classNames.delete(v);return set;}};for(const [key,value]of Object.entries(attrs))if(key.startsWith('data-'))this.dataset[key.slice(5).replace(/-([a-z])/g,(_,c)=>c.toUpperCase())]=decode(value);}
  set innerHTML(value){for(const child of this.children)this.doc.drop(child);this.children=[];this._html=String(value);this.doc.parse(this._html,this);}
  get innerHTML(){return this._html||'';}
  get innerText(){return decode(this.innerHTML.replace(/<[^>]+>/g,' '));}
  addEventListener(name,fn){this.listeners.set(name,fn);}
  setAttribute(name,value){this.attrs[name]=String(value);}
  getAttribute(name){return this.attrs[name]??null;}
  focus(){this.doc.activeElement=this;}
  close(){this.open=false;this.listeners.get('close')?.({target:this});}
  showModal(){this.open=true;}
  remove(){this.doc.drop(this);}
  querySelector(selector){return this.doc.find(selector,this.children)[0]||null;}
  querySelectorAll(selector){return this.doc.find(selector,this.children);}
  getBoundingClientRect(){return {left:0,top:0,right:1200,bottom:800,width:1200,height:800};}
  setPointerCapture(){}
  closest(){return null;}
}
class Document {
  constructor(){this.nodes=[];this.documentElement={lang:'',dir:''};this.hidden=false;this.listeners=new Map();this.body=new Element(this,'body');this.parse(html,this.body);}
  parse(markup,parent){for(const match of markup.matchAll(/<([a-z][a-z0-9-]*)\b([^>]*)>/gi)){const attrs={};for(const attr of match[2].matchAll(/([\w-]+)(?:="([^"]*)"|'([^']*)'|=([^\s>]+))?/g))attrs[attr[1]]=decode(attr[2]??attr[3]??attr[4]??'');const el=new Element(this,match[1],attrs);if(el.tagName==='TEXTAREA'){const tail=markup.slice(match.index+match[0].length);el.value=decode(tail.slice(0,tail.indexOf('</textarea>')));}this.nodes.push(el);parent.children.push(el);}}
  drop(el){this.nodes=this.nodes.filter(x=>x!==el);for(const child of el.children)this.drop(child);}
  find(selector,nodes=this.nodes){if(selector.includes(','))return [...new Set(selector.split(',').flatMap(s=>this.find(s.trim(),nodes)))];if(selector.startsWith('#'))return nodes.filter(n=>n.id===selector.slice(1));if(/^\[data-/.test(selector)){const attr=selector.slice(1,-1);return nodes.filter(n=>Object.hasOwn(n.attrs,attr));}return nodes.filter(n=>n.tagName===selector.toUpperCase());}
  querySelector(selector){return this.find(selector)[0]||null;}
  querySelectorAll(selector){return this.find(selector);}
  addEventListener(name,fn){this.listeners.set(name,fn);}
}

function fixture(){
  const scenes=['route-a','route-b'].map(id=>({id,category:'semiconductor',title:id,titleEn:id,roles:[{id:'designer',title:'設計',titleEn:'Designer'},{id:'tester',title:'測試',titleEn:'Tester'}],assetIds:[],chapters:[
    {id:id+'-inspect',title:'檢查',titleEn:'Inspect',task:'檢查資料',taskEn:'Inspect evidence',observations:[{id:'reading',title:'讀值',titleEn:'Reading',text:'已取得量測值',textEn:'A measurement is available'}],choices:[{id:'verify',title:'驗證',titleEn:'Verify',outcome:'已驗證',outcomeEn:'Verified'}]},
    {id:id+'-validate',title:'驗收',titleEn:'Validate',task:'交叉檢查',taskEn:'Cross-check',observations:[],choices:[]},
  ]}));
  const storage=new Map(),document=new Document(),timers=new Map();let timerId=0,engine=null,rendererMounts=0;
  const createEngine=options=>{rendererMounts++;let config=options.config,position={x:0,z:14,yaw:0};const emit=()=>options.onMove({...position,moving:false});const api={setConfig(next){config=next;position={x:0,z:config.bounds.depth/2-4,yaw:0};emit();},setLanguage(){},setView(){},setPaused(){},setCompleted(){},setPosition(next){position={...next};emit();return true;},getState(){return {...position};},setMove(){},dispose(){},goToStation(){return true;},interact(){return true;}};engine=api;emit();return api;};
  const window={MG_CAMPAIGN_UTILS:{},MACGYVER_EXPERIENCES_V21:{experiences:scenes,assets:[],domains:[{id:'semiconductor',title:'半導體',titleEn:'Semiconductor'}]},addEventListener(){},speechSynthesis:{cancel(){}}};
  const scope={window,document,localStorage:{getItem:k=>storage.get(k)||null,setItem:(k,v)=>storage.set(k,String(v))},location:{protocol:'file:',search:'',pathname:'/experience.html',hash:''},history:{replaceState(){}},navigator:{languages:['en']},innerWidth:1200,URLSearchParams,URL,Date,JSON,Set,Map,console,speechSynthesis:window.speechSynthesis,setTimeout:fn=>{timers.set(++timerId,fn);return timerId;},clearTimeout:id=>timers.delete(id),buildWorldConfig,resolveLanguage,uiText,languageChoices,newWalkRecord,restoreWalkRecord,createWalkWorld:createEngine,createFallbackWorld:createEngine};
  const context=vm.createContext(scope);
  vm.runInContext(source+`\n globalThis.controller={loadScene,openTask,onNear,refreshIdentity,save,prime(ownerId){owner=ownerId;identityReady=true;},state(){return JSON.parse(JSON.stringify({owner,record,sceneId:scene?.id}));}};`,context,{filename:'walk-v22.js'});
  const c=context.controller;
  return {c,scenes,storage,document,get engine(){return engine;},get rendererMounts(){return rendererMounts;},element:s=>document.querySelector(s),stored(owner,id=scenes[0].id){return JSON.parse(storage.get(`mg-walk-v22:${owner}:${id}`)||'null');},put(owner,record){storage.set(`mg-walk-v22:${owner}:${record.sceneId}`,JSON.stringify(record));},enter(){c.prime('device:guest');c.loadScene(scenes[0].id);},open(index=0){const station=scenes[0].chapters[index];c.onNear(station);c.openTask(station.id);},drainTimers(){const pending=[...timers.values()];timers.clear();pending.forEach(fn=>fn());}};
}

test('switching identity resumes the target account without overwriting its record',async()=>{
  const f=fixture();f.enter();f.open();f.element('#field-note').value='Guest draft belongs only to guest';
  const target={...newWalkRecord(f.scenes[0],'tester'),notes:{'route-a-inspect':'Existing tester measurements'},position:{x:4,z:3,yaw:.7}};
  f.put('device:offline-bbbbbbb',target);const saved=JSON.stringify(target);
  f.storage.set('mg-offline-active-v1','offline-bbbbbbb');f.storage.set('mg-offline-profiles-v1',JSON.stringify([{id:'offline-bbbbbbb'}]));
  await f.c.refreshIdentity();
  assert.equal(f.c.state().owner,'device:offline-bbbbbbb');
  assert.equal(f.c.state().record.roleId,'tester');
  assert.equal(f.c.state().record.notes['route-a-inspect'],'Existing tester measurements');
  assert.equal(JSON.stringify(f.stored('device:offline-bbbbbbb')),saved,'target storage remains intact during identity loading');
  assert.equal(f.stored('device:guest').notes['route-a-inspect'],'Guest draft belongs only to guest');
  f.drainTimers();assert.equal(f.stored('device:offline-bbbbbbb').notes['route-a-inspect'],'Existing tester measurements');
});

test('role selection preserves each role and ignores the hidden old note field',()=>{
  const f=fixture();f.enter();f.open();f.element('#field-note').value='Designer tolerance assumptions';
  f.element('#role').onchange({target:{value:'tester'}});
  assert.equal(f.element('#task-panel').hidden,true);assert.equal(f.c.state().record.notes['route-a-inspect'],undefined);
  assert.equal(f.element('#field-note').value,'Designer tolerance assumptions','hidden DOM deliberately retains the old textarea');
  f.open();assert.equal(f.element('#field-note').value,'','tester starts with a clean note');
  f.element('#field-note').value='Tester verification results';f.element('#save-note').onclick();
  f.element('#role').onchange({target:{value:'designer'}});f.open();
  assert.equal(f.element('#field-note').value,'Designer tolerance assumptions');
  assert.equal(f.c.state().record.roleRuns.tester.notes['route-a-inspect'],'Tester verification results');
});

test('completing a station never copies its note into the next station',()=>{
  const f=fixture();f.enter();f.open();f.element('#field-note').value='Station one measured at 25 C';
  f.element('[data-observe]').onclick();f.element('[data-choice]').onclick();f.element('#complete-task').onclick();
  assert.equal(f.c.state().record.chapterId,'route-a-validate');
  assert.equal(f.c.state().record.notes['route-a-inspect'],'Station one measured at 25 C');
  assert.equal(f.c.state().record.notes['route-a-validate'],undefined);
  f.open(1);assert.equal(f.element('#field-note').value,'');assert.equal(f.c.state().record.notes['route-a-validate'],undefined);
  f.element('#field-note').value='Station two cross-check';f.element('#save-note').onclick();
  const stored=f.stored('device:guest');assert.equal(stored.notes['route-a-inspect'],'Station one measured at 25 C');assert.equal(stored.notes['route-a-validate'],'Station two cross-check');
});

test('saved location survives spawn callbacks on initial mount and scene changes',()=>{
  const f=fixture(),position={x:4.1,z:-3.2,yaw:.9};f.put('device:guest',{...newWalkRecord(f.scenes[0]),position});
  f.enter();assert.equal(f.rendererMounts,1);assert.deepEqual(f.engine.getState(),position);
  f.c.loadScene(f.scenes[1].id);f.c.loadScene(f.scenes[0].id);
  assert.equal(f.rendererMounts,1,'scene changes reuse the live renderer');
  assert.deepEqual(f.engine.getState(),position,'setConfig emits a spawn before the saved location is restored');
  assert.deepEqual(f.c.state().record.position,position);f.drainTimers();assert.deepEqual(f.stored('device:guest').position,position);
});

test('malformed persisted JSON does not block entry or damage another journey',()=>{
  const f=fixture();f.storage.set('mg-walk-v22:device:guest:route-a','{bad JSON');
  assert.doesNotThrow(()=>f.enter());assert.equal(f.c.state().record.chapterId,'route-a-inspect');assert.deepEqual(f.c.state().record.completed,[]);
  f.open();f.element('#field-note').value='Recovered progress';f.element('#save-note').onclick();
  f.storage.set('mg-walk-v22:device:guest:route-b','[malformed');assert.doesNotThrow(()=>f.c.loadScene('route-b'));
  assert.equal(f.c.state().record.sceneId,'route-b');assert.equal(f.stored('device:guest','route-a').notes['route-a-inspect'],'Recovered progress');
});
