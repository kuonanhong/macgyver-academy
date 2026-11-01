/* Behavioral checks use a minimal canvas host; navigation is the production physics implementation. */
import assert from 'node:assert/strict';
import {createFallbackWorld} from '../public/academy/walk-fallback-v22.js';
const events=new Map();
const handlers=prefix=>({addEventListener:(name,fn)=>events.set(prefix+name,fn),removeEventListener:name=>events.delete(prefix+name)});
let frame,removed=false,draws=0,dialog=false,printed=[];
const context=new Proxy({
  createLinearGradient:()=>({addColorStop(){}}),measureText:text=>({width:text.length*6}),
  fillText(text){printed.push(text);},
},{get:(object,key)=>key in object?object[key]:(()=>{draws++;}),set:(object,key,value)=>(object[key]=value,true)});
const canvas={style:{},setAttribute(){},getContext:()=>context,getBoundingClientRect:()=>({left:0,top:0,width:1000,height:800}),focus(){},closest:()=>null,remove(){removed=true;},...handlers('canvas:')};
globalThis.document={createElement:()=>canvas,querySelector:()=>dialog?{}:null,activeElement:canvas,hidden:false,...handlers('doc:')};
globalThis.window={devicePixelRatio:1,...handlers('win:')};
globalThis.requestAnimationFrame=fn=>(frame=fn,1);
globalThis.cancelAnimationFrame=()=>{};
let near=null;const interactions=[];
const config={id:'test',color:'#87c9cf',layout:'lab',bounds:{width:30,depth:36},stations:[{id:'a',title:'甲',titleEn:'Alpha',kind:'bench',x:6,z:0,approach:{x:3.1,z:0}}]};
const world=createFallbackWorld({container:{appendChild(){},getBoundingClientRect:()=>({width:1000,height:800})},config,onInteract:s=>interactions.push(s.id),onNear:s=>{near=s;}});
let checks=0,time=0;
function step(){time+=50;frame(time);}
function test(name,fn){fn();checks++;console.log('PASS',name);}
function stationary(){world.setMove(0,0);world.setPosition({x:0,z:14});}
step();
test('Avatar spawns at the continuous room entrance',()=>assert.equal(world.getState().z,14));
test('Distant equipment cannot be operated',()=>assert.equal(world.interact(),false));
test('Saved position inside a machine is rejected',()=>assert.equal(world.setPosition({x:6,z:0}),false));
test('Non-finite saved coordinates are rejected',()=>assert.equal(world.setPosition({x:NaN,z:0}),false));
test('Saved position outside room walls is rejected',()=>assert.equal(world.setPosition({x:100,z:0}),false));
test('Valid restored position updates proximity',()=>{assert.equal(world.setPosition({x:3,z:0}),true);assert.equal(near.id,'a');});
test('Equipment operates only after arriving nearby',()=>{assert.equal(world.interact(),true);assert.deepEqual(interactions,['a']);});
test('Reset returns the avatar to the entrance',()=>{world.resetPosition();assert.equal(world.getState().z,14);});
test('Camera-relative forward motion translates both world coordinates',()=>{const before=world.getState();world.setMove(0,-1);step();assert.notEqual(world.getState().x,before.x);assert.notEqual(world.getState().z,before.z);});
test('Fallback renders a world during movement',()=>assert.ok(draws>0));
test('Pause releases held movement and stops position changes',()=>{world.setPaused(true);const before=world.getState();step();assert.equal(world.getState().x,before.x);assert.equal(world.getState().z,before.z);world.setPaused(false);});
test('A target station generates a real navigation path',()=>{stationary();assert.equal(world.goToStation('a'),true);assert.ok(world.getState().pathRemaining>0);});
test('Unknown station identifiers do not generate a path',()=>assert.equal(world.goToStation('missing'),false));
test('Equipment paths reach the operating point without teleportation',()=>{for(let i=0;i<180&&world.getState().pathRemaining;i++)step();assert.equal(world.getState().nearId,'a');assert.ok(Math.hypot(world.getState().x-3.1,world.getState().z)<.25);});
test('Open dialogs stop motion',()=>{stationary();dialog=true;world.setMove(0,-1);const before=world.getState();step();assert.equal(world.getState().x,before.x);dialog=false;world.setMove(0,0);});
test('Text input focus stops motion',()=>{stationary();document.activeElement={tagName:'INPUT',closest:()=>null};world.setMove(0,-1);const before=world.getState();step();assert.equal(world.getState().x,before.x);document.activeElement=canvas;world.setMove(0,0);});
test('Overview preserves a live room view',()=>{world.setView('overview');assert.equal(world.getState().view,'overview');});
test('Completed stations display a checkmark',()=>{world.setPosition({x:3,z:0});world.setCompleted(['a']);printed=[];step();assert.ok(printed.includes('✓'));});
test('Setting another scene clears prior completion markers',()=>{world.setConfig(config);world.setPosition({x:3,z:0});printed=[];step();assert.ok(!printed.includes('✓'));});
test('Disposal removes the canvas and every event handler',()=>{world.dispose();assert.equal(removed,true);assert.equal(events.size,0);});
console.log(`${checks} canvas fallback behavior checks passed.`);
