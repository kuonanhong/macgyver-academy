// Exercise the real app language/save handlers without the full curriculum render sweep.
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import {resolveSupportedLanguage} from '../public/academy/locale.js';

const source=fs.readFileSync(process.argv[2]||new URL('../public/academy/app.js',import.meta.url),'utf8');
const messages=source.slice(source.indexOf('const messages='),source.indexOf('const dirtyNotes='));
assert(messages.includes('offlineSaved:'),'real application message catalogue is loaded');
const line=name=>{
  const found=source.split('\n').find(row=>row.startsWith(`function ${name}(`));
  assert(found,`real application handler ${name} exists`);return found;
};
const save=source.slice(source.indexOf('async function save('),source.indexOf('function suspendProtectedCurriculum('));
assert(save.includes('await saveQueue'),'real asynchronous save handler is loaded');
function fixture(){
  const storage=new Map(),status={textContent:''};let notes=null,storageFails=false,request=async()=>({ok:true,status:200,json:async()=>({updatedAt:100})});
  let context;
  context=vm.createContext({console,Date,JSON,Set,resolveSupportedLanguage,
    navigator:{languages:['en'],language:'en'},languageChoices:[['en','English'],['zh-TW','繁體中文'],['fr','Français']],
    localStorage:{getItem:key=>storage.get(key)||null,setItem:(key,value)=>{if(storageFails&&key!=='mg-language')throw Error('Storage full');storage.set(key,value)}},
    window:{MacGyverOffline:{storageAvailable:true}},$:selector=>selector==='#saveStatus'?status:selector==='#notes'?notes:null,
    fetch:(...args)=>request(...args),toast(){},download(){},onDeviceTranslator(){},loadDictionary:async()=>null,applyLanguage(){},
    render(){status.textContent=vm.runInContext('saveState||persistenceStatus()',context)}
  });
  vm.runInContext(`${messages}
    let saveState='',authMode='offline',user=null,deviceSaveOK=true,saveQueue=Promise.resolve(),accountGeneration=1,serverVersions={},activeId='demo',shownProjectId='';
    const projects={demo:{notes:'',completed:[],assembly:[],updatedAt:0}},dirtyNotes=new Set();
    const stateKey=()=> 'mg-progress-'+(user?.id||'guest'),record=id=>projects[id];
    ${line('persistenceStatus')}
    ${line('saveStatusMessageKey')}
    ${line('setPreferredLanguage')}
    ${line('captureNotes')}
    ${save}
  `,context);
  return {run:code=>vm.runInContext(code,context),status,storage,
    setNotes:value=>{notes=value},failStorage:()=>{storageFails=true},setRequest:handler=>{request=handler}};
}

const keys=['saved','localSaved','offlineSaved','sessionOnly','saving','syncError','notSaved','saveFailed'];
for(const key of keys){
  const f=fixture();f.run(`lang='zh-TW';saveState=t(${JSON.stringify(key)})`);
  f.run("setPreferredLanguage('en')");
  assert.equal(f.status.textContent,f.run(`messages[${JSON.stringify(key)}][1]`),`${key} becomes English without changing meaning`);
  f.run("setPreferredLanguage('zh-TW')");
  assert.equal(f.status.textContent,f.run(`messages[${JSON.stringify(key)}][0]`),`${key} returns to Chinese`);
}
{
  const f=fixture();f.run("lang='zh-TW'");await f.run("save('demo')");
  assert.equal(f.status.textContent,'已存至此瀏覽器／本機檔案');
  f.run("setPreferredLanguage('en')");assert.equal(f.status.textContent,'Saved in this browser / local profile','actual offline save screenshot regression');
}
{
  const f=fixture();f.run("lang='zh-TW';authMode='chatgpt';user={id:'learner'};saveState=t('syncError')");
  f.setNotes({id:'notes',dataset:{owner:'learner',projectId:'demo',savedValue:''},value:'Draft retained while changing language'});
  let finish;f.setRequest(()=>new Promise(resolve=>{finish=resolve}));
  f.run("setPreferredLanguage('en')");
  assert.equal(f.status.textContent,'Saving…','captureNotes starts a real save before choosing the translated status');
  assert.equal(f.run('projects.demo.notes'),'Draft retained while changing language');
  await Promise.resolve();await Promise.resolve();
  assert.equal(typeof finish,'function');
  finish({ok:true,status:200,json:async()=>({updatedAt:100})});await f.run('saveQueue');
  assert.equal(f.status.textContent,'Saved','pending response uses the current language');
}
for(const noDeviceBackup of [false,true]){
  const f=fixture();f.run("lang='zh-TW';authMode='chatgpt';user={id:'learner'}");
  if(noDeviceBackup)f.failStorage();
  let fail;f.setRequest(()=>new Promise((resolve,reject)=>{fail=reject}));
  const pending=f.run("save('demo')");f.run("setPreferredLanguage('en')");
  assert.equal(f.status.textContent,'Saving…');await Promise.resolve();await Promise.resolve();fail(Error('Offline'));await pending;
  const key=noDeviceBackup?'saveFailed':'syncError';
  assert.equal(f.status.textContent,f.run(`messages.${key}[1]`),'failed pending request preserves the appropriate backup distinction');
  f.run("setPreferredLanguage('zh-TW')");assert.equal(f.status.textContent,f.run(`messages.${key}[0]`),'failure remains a failure after another language switch');
}
{
  const f=fixture();f.failStorage();f.run("lang='zh-TW';authMode='chatgpt'");await f.run("save('demo')");
  f.run("setPreferredLanguage('en')");assert.equal(f.status.textContent,'Not saved; please export','guest storage failure is not reported as saved');
}
{
  const f=fixture();f.run("lang='zh-TW';saveState='Custom detail: do not discard';setPreferredLanguage('en')");
  assert.equal(f.status.textContent,'Custom detail: do not discard','unrecognized details are preserved');
  f.run("saveState='';setPreferredLanguage('zh-TW')");assert.equal(f.run('saveState'),'','unset status stays unset');
  f.run("saveState=t('saving');setPreferredLanguage('auto')");assert.equal(f.status.textContent,'Saving…','automatic language follows browser preference');
  f.run("lang='zh-TW';saveState=t('syncError');setPreferredLanguage('fr')");
  assert.equal(f.status.textContent,'Cloud sync failed; device backup saved','other locales receive the current core fallback before page translation');
}
console.log(JSON.stringify({status:'PASS',knownStatuses:8,bidirectionalMeaningPreserved:true,actualOfflineSave:true,dirtyNotesPendingSave:true,pendingCloudFailure:true,pendingNoBackupFailure:true,guestStorageFailure:true,unknownDetailsPreserved:true,autoAndThirdLanguage:true}));
