import test from 'node:test';
import assert from 'node:assert/strict';
import {newWalkRecord,restoreWalkRecord} from '../public/academy/walk-state-v22.js';

const scene={id:'engineering-route',roles:[{id:'designer'},{id:'builder'},{id:'tester'}],chapters:[
  {id:'requirements',observations:[{id:'measure'},{id:'spec'}],choices:[{id:'verify'},{id:'guess'}]},
  {id:'manufacture',observations:[{id:'material'}],choices:[{id:'inspect'}]},
  {id:'test',observations:[],choices:[]}
]};
const raw=(overrides={})=>({...newWalkRecord(scene),...overrides});
const completed=(roleId='designer')=>raw({roleId,chapterId:'manufacture',seen:{requirements:['measure','spec']},decisions:{requirements:{choiceId:'verify',assisted:false}},completed:['requirements'],notes:{requirements:'Record the tolerance.'}});

test('new records have a valid first station and separate mutable progress',()=>{
  const a=newWalkRecord(scene),b=newWalkRecord(scene,'tester');
  assert.equal(a.version,22);assert.equal(a.sceneId,scene.id);assert.equal(a.roleId,'designer');assert.equal(a.chapterId,'requirements');
  assert.equal(b.roleId,'tester');a.completed.push('requirements');a.notes.requirements='A';
  assert.deepEqual(b.completed,[]);assert.deepEqual(b.notes,{});
});

test('wrong version or route and primitive imports reset to a fresh record',()=>{
  for(const value of [null,undefined,[],42,'text',raw({version:21}),raw({sceneId:'other'})])assert.deepEqual(restoreWalkRecord(scene,value),newWalkRecord(scene));
});

test('chapter, role, evidence and completion identifiers are confined to this scene',()=>{
  const value=restoreWalkRecord(scene,raw({roleId:'administrator',chapterId:'forged',seen:{requirements:['measure','measure','spec','forged']},decisions:{requirements:{choiceId:'verify'}},completed:['requirements','requirements','forged',{id:'test'}]}));
  assert.equal(value.roleId,'designer');assert.equal(value.chapterId,'requirements');
  assert.deepEqual(value.seen.requirements,['measure','spec']);assert.deepEqual(value.completed,['requirements']);
});

test('a forged completion without all local observation records is removed',()=>{
  const value=restoreWalkRecord(scene,raw({seen:{requirements:['measure']},decisions:{requirements:{choiceId:'verify'}},completed:['requirements']}));
  assert.deepEqual(value.completed,[]);
});

test('a forged completion without a valid decision is removed',()=>{
  for(const decisions of [{},{requirements:{choiceId:'unlisted'}}]){
    const value=restoreWalkRecord(scene,raw({seen:{requirements:['measure','spec']},decisions,completed:['requirements']}));
    assert.deepEqual(value.completed,[]);assert.deepEqual(value.decisions,{});
  }
});

test('valid completed stations survive export and JSON import',()=>{
  const original=completed();original.completed.push('test');
  const value=restoreWalkRecord(scene,JSON.parse(JSON.stringify(original)));
  assert.deepEqual(value.completed,['requirements','test']);assert.equal(value.notes.requirements,'Record the tolerance.');
  assert.equal(value.chapterId,'manufacture');
});

test('decisions copy only known choice and strict assistance state',()=>{
  const value=restoreWalkRecord(scene,raw({decisions:{requirements:{choiceId:'guess',assisted:'true',score:100,roleId:'administrator'},manufacture:{choiceId:'inspect',assisted:true}}}));
  assert.deepEqual(value.decisions.requirements,{choiceId:'guess',assisted:false});
  assert.deepEqual(value.decisions.manufacture,{choiceId:'inspect',assisted:true});
});

test('note imports keep strings only, cap length and reject unknown chapters',()=>{
  const value=restoreWalkRecord(scene,raw({notes:{requirements:'x'.repeat(10000),manufacture:{html:'<script>'},forged:'extra'}}));
  assert.equal(value.notes.requirements.length,4000);assert.equal(value.notes.manufacture,undefined);assert.equal(value.notes.forged,undefined);
});

test('positions accept finite bounded numbers and copy only x z yaw',()=>{
  const value=restoreWalkRecord(scene,raw({position:{x:3,z:-8,yaw:1.2,admin:true}}));
  assert.deepEqual(value.position,{x:3,z:-8,yaw:1.2});
  for(const position of [{x:Infinity,z:0,yaw:0},{x:0,z:NaN,yaw:0},{x:10000,z:0,yaw:0},{x:0,z:0,yaw:10000},{x:'1',z:0,yaw:0},{x:0,z:0}])assert.equal(restoreWalkRecord(scene,raw({position})).position,null);
});

test('action imports are bounded, tied to known chapters and strip extra payload',()=>{
  const actions=Array.from({length:620},(_,i)=>({type:'observe',chapterId:'requirements',assisted:i%2===0,at:String(i),privatePayload:'discard'}));
  actions.push({type:'forged',chapterId:'other',at:'now'},{type:'x'.repeat(80),chapterId:'requirements',at:'now'},{type:'observe',chapterId:'requirements',at:42});
  const value=restoreWalkRecord(scene,raw({actions}));
  assert.equal(value.actions.length,600);assert.equal(value.actions[0].at,'20');
  assert.deepEqual(Object.keys(value.actions[0]).sort(),['assisted','at','chapterId','type']);
});

test('role runs are separately restored and cannot recursively inject unknown roles',()=>{
  const designer=completed('designer');const tester=raw({roleId:'tester',chapterId:'test',notes:{test:'Only tester note'},completed:['test'],roleRuns:{designer:{completed:['requirements']}}});
  const value=restoreWalkRecord(scene,raw({roleId:'builder',roleRuns:{designer,tester,administrator:completed()}}));
  assert.deepEqual(Object.keys(value.roleRuns).sort(),['designer','tester']);
  assert.equal(value.roleRuns.designer.roleId,'designer');assert.deepEqual(value.roleRuns.designer.completed,['requirements']);
  assert.equal(value.roleRuns.tester.roleId,'tester');assert.equal(value.roleRuns.tester.notes.test,'Only tester note');
  assert.deepEqual(value.roleRuns.tester.roleRuns,{});assert.deepEqual(value.completed,[]);assert.deepEqual(value.notes,{});
});

test('tampered role-run completions undergo the same evidence checks',()=>{
  const value=restoreWalkRecord(scene,raw({roleRuns:{designer:raw({completed:['requirements','manufacture','test']})}}));
  assert.deepEqual(value.roleRuns.designer.completed,['test']);
});

test('input objects and nested role progress remain unchanged during restore',()=>{
  const original=completed();original.roleRuns.tester=completed('tester');original.actions=[{type:'observe',chapterId:'requirements',at:'now',extra:9}];
  const snapshot=JSON.stringify(original);const value=restoreWalkRecord(scene,original);
  value.completed.push('test');value.roleRuns.tester.notes.requirements='different';
  assert.equal(JSON.stringify(original),snapshot);
});

test('oversized dates and action metadata do not expand stored records',()=>{
  const value=restoreWalkRecord(scene,raw({updatedAt:'A'.repeat(1000),actions:[{type:'observe',chapterId:'requirements',at:'B'.repeat(1000)}]}));
  assert.equal(value.updatedAt.length,40);assert.equal(value.actions[0].at.length,40);
});
