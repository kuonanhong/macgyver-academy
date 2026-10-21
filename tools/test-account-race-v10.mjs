// Execute the real initAccount function with deferred HTTP/service responses.
// Focused account-transition regression test; no full curriculum render loop.
import assert from 'node:assert/strict';
import {resetProtectedContent,refreshAccess} from '../public/academy/paywall.js';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import {fileURLToPath} from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const source = fs.readFileSync(path.join(root, 'public/academy/app.js'), 'utf8');
const start = source.indexOf('function suspendProtectedCurriculum()');
const end = source.indexOf('\nfunction poseStorageKey()', start);
assert(start >= 0 && end > start, 'initAccount extraction boundaries are present');
const exactFunction = source.slice(start, end);
const deferred = () => {
  let resolve, reject;
  const promise = new Promise((yes, no) => {resolve = yes; reject = no;});
  return {promise, resolve, reject};
};
const until = async predicate => {
  for (let i = 0; i < 100; i++) {
    if (predicate()) return;
    await Promise.resolve();
  }
  assert.fail('The expected deferred request did not start');
};
const course = owner => ({id:'semiconductor', title:owner, locked:false, stages:[{id:'stage',steps:[{id:'lesson',objective:owner+' private lesson'}]}]});

function harness({curriculum, evidence} = {}) {
  let session = 'A', curriculumCalls = 0, evidenceCalls = 0, mapDisposals = 0;
  const storage = new Map(), main = {innerHTML:'A previously rendered private lesson'}, status = {textContent:''};
  const context = {
    Map, Set, JSON, resetProtectedContent,refreshAccess,stepCache:new WeakMap(),window:{},translationAvailable:false,accountGeneration:0, user:null, authMode:'local',
    aiAvailable:false, aiRoutes:[], serverVersions:{}, projects:{}, saveState:'',
    activeId:'semiconductor', featured:[], catalog:[course('initial')], sourceIndex:null,
    currentPage:'workshop', isZh:() => false,
    learningMapController:null,
    $:selector => selector === '#main' ? main : selector === '#protectedAccountStatus' ? status : null,
    captureNotes:() => {}, stopDemonstration:() => {}, deactivateWorkshopKeyboard:() => {},
    tutorPanel:{close() {}}, localeController:{invalidate() {}}, disposeLearningMedia:() => {},
    localStorage:{getItem:key => storage.get(key) ?? null, setItem:(key,value) => storage.set(key,value)},
    stateKey:() => 'mg-progress-' + context.user?.id,
    save:() => {}, t:value => value, persistenceStatus:() => 'saved',
    resetLearningEvidence:owner => {context.evidenceOwner = owner;},
    billingState:() => ({protected:true}),
    record:id => context.projects[id] ??= {completed:[],assembly:[],notes:'',updatedAt:0},
    fetch:async url => {
      const owner = session;
      return {ok:true, json:async () => url === '/api/me'
        ? {user:owner ? {id:owner} : null,authMode:'local'}
        : {projects:{semiconductor:{completed:[owner+'-progress'],assembly:[],notes:owner+' notes',updatedAt:1}}}};
    },
    loadCurriculumData:async (name, options) => {
      assert.equal(name, 'featured');
      assert.equal(options.protected, true);
      const call = ++curriculumCalls, owner = session;
      return curriculum ? curriculum(call, owner) : [course(owner)];
    },
    loadVerifiedLearning:async id => {
      assert.equal(id, 'semiconductor');
      const call = ++evidenceCalls, owner = session;
      return evidence ? evidence(call, owner) : {completed:[owner+'-proof']};
    }
  };
  vm.createContext(context);
  vm.runInContext(exactFunction, context, {filename:'app.js:initAccount'});
  const attachLearningMap = () => {
    // A map mounted by render() holds its then-current metadata/curriculum.
    // Disposal must make a queued component callback unable to repaint it.
    let disposed=false;
    const capturedTitle=context.featured[0]?.title || 'initial';
    const controller={
      get disposed(){return disposed;},
      dispose(){if(disposed)return;disposed=true;mapDisposals++;},
      repaint(){if(!disposed)main.innerHTML='STALE MAP '+capturedTitle;}
    };
    context.learningMapController=controller;
    context.currentPage='learning-map';
    return controller;
  };
  return {
    context, storage, main, status,
    attachLearningMap,
    login:owner => {session = owner; return vm.runInContext('initAccount()', context);},
    snapshot:() => JSON.stringify({user:context.user,projects:context.projects,featured:context.featured,catalog:context.catalog,evidenceOwner:context.evidenceOwner}),
    get curriculumCalls() {return curriculumCalls;},
    get evidenceCalls() {return evidenceCalls;},
    get mapDisposals() {return mapDisposals;}
  };
}

// Public home/catalog remains visible during slow background account verification.
for(const page of ['home','catalog']){
  const delayed=deferred(),app=harness({curriculum:()=>delayed.promise});
  app.context.currentPage=page;app.main.innerHTML='PUBLIC CATALOGUE READY';
  const pending=app.login('A');await until(()=>app.curriculumCalls===1);
  assert.equal(app.main.innerHTML,'PUBLIC CATALOGUE READY','background account checks must not hide '+page);
  assert.equal(app.context.currentPage,page);
  delayed.resolve([course('A')]);await pending;
  assert.equal(app.main.innerHTML,'PUBLIC CATALOGUE READY');
}

// A failed verification request from A cannot clear B's verified completion.
{
  const old = deferred();
  const app = harness({evidence:(call, owner) => call === 1 ? old.promise : {completed:[owner+'-proof']}});
  const first = app.login('A');
  await until(() => app.evidenceCalls === 1);
  await app.login('B');
  assert.deepEqual(app.context.projects.semiconductor.completed, ['B-proof']);
  const before = app.snapshot();
  old.reject(new Error('A verification failed after the account changed'));
  await first;
  assert.equal(app.snapshot(), before, 'late A verification failure cannot mutate B');
}

// A successful old protected-curriculum response cannot replace B's catalogue.
{
  const old = deferred();
  const app = harness({curriculum:(call, owner) => call === 1 ? old.promise : [course(owner)]});
  const first = app.login('A');
  await until(() => app.curriculumCalls === 1);
  await app.login('B');
  const before = app.snapshot();
  old.resolve([course('stale-A')]);
  await first;
  assert.equal(app.snapshot(), before, 'late A curriculum cannot overwrite B');
}

// An old protected loader rejection must not fall back to paid cached curricula
// or clear the newly selected account's progress. Obsolete errors are ignored.
{
  const old = deferred();
  const app = harness({curriculum:(call, owner) => call === 1 ? old.promise : [course(owner)]});
  const first = app.login('A');
  await until(() => app.curriculumCalls === 1);
  await app.login('B');
  const before = app.snapshot();
  old.reject(new Error('Old protected curriculum request failed'));
  await first;
  assert.equal(app.snapshot(), before, 'late A curriculum failure cannot mutate B');
  assert.equal(app.context.evidenceOwner, 'B');
}

// A current account transition fails closed before /api/me can settle. If the
// protected loader fails, neither the in-memory catalogue nor the DOM retains
// A's lesson. A later successful retry can restore the current owner's lessons.
{
  const failed = deferred();
  const app = harness({curriculum:(call, owner) => call === 2 ? failed.promise : [course(owner)]});
  await app.login('A');
  const oldMap=app.attachLearningMap();
  app.main.innerHTML = 'PRIVATE A RENDERED LESSON';
  const second = app.login('B');
  assert.equal(oldMap.disposed,true,'the old map is disposed before the first account request settles');
  assert.equal(app.context.learningMapController,null,'the old map reference is cleared');
  assert.equal(app.mapDisposals,1);
  const hidden=app.main.innerHTML;oldMap.repaint();
  assert.equal(app.main.innerHTML,hidden,'a disposed map callback cannot restore old account content');
  assert(!app.main.innerHTML.includes('PRIVATE A'), 'the old lesson DOM is cleared synchronously');
  assert.equal(app.context.featured[0].stages.length, 0);
  assert.equal(app.context.catalog[0].stages.length, 0);
  assert.equal(app.context.featured[0].locked, true);
  const rejected = assert.rejects(second, /B curriculum unavailable/);
  await until(() => app.curriculumCalls === 2);
  failed.reject(new Error('B curriculum unavailable'));
  await rejected;
  assert.equal(app.context.user.id, 'B');
  assert.equal(app.context.featured[0].stages.length, 0, 'A lessons remain absent after failure');
  assert(app.status.textContent.includes('Lessons remain hidden'));
  await app.login('B');
  assert.equal(app.context.featured[0].locked, false, 'successful retry restores access');
  assert.equal(app.context.featured[0].stages[0].steps[0].objective, 'B private lesson');
}

// Logout followed by a failed curriculum request also clears the prior user's
// lesson. Guest catalogue metadata remains navigable, with no prior stages.
{
  const app = harness({curriculum:(call, owner) => {
    if (call === 2) throw new Error('Guest curriculum unavailable');
    return [course(owner)];
  }});
  await app.login('A');
  const oldMap=app.attachLearningMap();
  app.main.innerHTML = 'PRIVATE A RENDERED LESSON';
  await assert.rejects(app.login(null), /Guest curriculum unavailable/);
  assert.equal(oldMap.disposed,true,'logout disposes the prior account map');
  assert.equal(app.context.learningMapController,null);
  const hidden=app.main.innerHTML;oldMap.repaint();assert.equal(app.main.innerHTML,hidden);
  assert.equal(app.context.user, null);
  assert(!app.main.innerHTML.includes('PRIVATE A'));
  assert.equal(app.context.featured[0].stages.length, 0);
  assert.equal(app.context.catalog[0].stages.length, 0);
  assert.equal(app.context.evidenceOwner, 'guest');
}

// A current account's failed server verification still removes unverified
// completion, while retaining its own notes and assembly evidence.
{
  const app = harness({evidence:() => {throw new Error('Current verification unavailable');}});
  await app.login('A');
  assert.equal(app.context.user.id, 'A');
  assert.equal(app.context.projects.semiconductor.completed.length, 0);
  assert.equal(app.context.projects.semiconductor.notes, 'A notes');
}

console.log('PASS 8 account-transition checks: public homepage/catalogue stays visible during delayed account verification, stale verification/curriculum responses, fail-closed account change/logout, synchronous learning-map disposal and inert old callbacks, retry recovery, and current-owner verification failure; exact initAccount/helper in Node VM, no real network.');
