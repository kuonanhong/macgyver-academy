import assert from 'node:assert/strict';
import {normalizeInput,isWalkable,moveWithCollisions,cameraRelativeMove,findPath,nearestStation} from '../public/academy/walk-physics-v22.js';
const bounds={width:20,depth:20}, obstacle={minX:-1,maxX:1,minZ:-3,maxZ:3};
let checks=0;function test(name,fn){fn();checks++;console.log('PASS',name);}
test('Diagonal movement has the same speed as straight movement',()=>assert.equal(Math.hypot(...Object.values(normalizeInput(1,1))),1));
test('Camera-relative input rotates with heading',()=>{const p=cameraRelativeMove({x:0,z:-1},Math.PI/2);assert.ok(Math.abs(p.x+1)<1e-8);assert.ok(Math.abs(p.z)<1e-8);});
test('Player radius stays inside the room boundary',()=>{assert.equal(isWalkable(9.8,0,bounds),false);assert.ok(isWalkable(9,0,bounds));});
test('Collider radius blocks the expanded machine edge',()=>{assert.equal(isWalkable(1.2,0,bounds,[obstacle]),false);assert.ok(isWalkable(1.5,0,bounds,[obstacle]));});
test('Large motion cannot tunnel through machinery',()=>{const p=moveWithCollisions({x:-5,z:0},{x:12,z:0},bounds,[obstacle]);assert.ok(p.x< -1.37);});
test('Diagonal motion slides along a machine',()=>{const p=moveWithCollisions({x:-2,z:-2},{x:3,z:2},bounds,[obstacle]);assert.ok(p.x< -1.37);assert.ok(p.z>-.2);});
test('Navigation routes around an obstructing machine',()=>{const route=findPath({x:-5,z:0},{x:5,z:0},bounds,[obstacle]);assert.ok(route.length>10);let p={x:-5,z:0};for(const target of route){assert.ok(isWalkable(target.x,target.z,bounds,[obstacle]));const moved=moveWithCollisions(p,{x:target.x-p.x,z:target.z-p.z},bounds,[obstacle]);assert.ok(Math.hypot(moved.x-target.x,moved.z-target.z)<.02);p=moved;}assert.ok(Math.hypot(p.x-5,p.z)<.02);});
test('An unreachable destination does not generate a teleport',()=>{const wall={minX:-1,maxX:1,minZ:-10,maxZ:10};assert.deepEqual(findPath({x:-5,z:0},{x:5,z:0},bounds,[wall]),[]);});
test('Blocked target resolves to a nearby free approach',()=>{const route=findPath({x:-5,z:0},{x:0,z:0},bounds,[obstacle]);assert.ok(route.length);const p=route.at(-1);assert.ok(isWalkable(p.x,p.z,bounds,[obstacle]));});
test('Interaction chooses only a nearby station approach',()=>{const stations=[{id:'a',x:0,z:0,approach:{x:2,z:0}},{id:'b',x:8,z:8}];assert.equal(nearestStation({x:2,z:1},stations).id,'a');assert.equal(nearestStation({x:-8,z:-8},stations),null);});
console.log(`${checks} meaningful walk physics checks passed.`);
const {DOMAIN_PROFILES_V22}=await import('../public/academy/walk-domains-v22.js');
let layoutRoutes=0;
for(const [domain,c] of Object.entries(DOMAIN_PROFILES_V22)){
  const blocks=c.stations.map(s=>({minX:s.x-1.7,maxX:s.x+1.7,minZ:s.z-1.8,maxZ:s.z+1.8}));
  let position={x:0,z:c.bounds.depth/2-4};
  for(const station of c.stations){
    const target={x:station.x-Math.sign(station.x||1)*2.9,z:station.z};
    const route=findPath(position,target,c.bounds,blocks);
    assert.ok(route.length,`${domain} ${station.equipmentTitleEn} must be reachable`);
    for(const step of route){
      const actual=moveWithCollisions(position,{x:step.x-position.x,z:step.z-position.z},c.bounds,blocks);
      assert.ok(Math.hypot(actual.x-step.x,actual.z-step.z)<.03,`${domain} path step must not cross blocked corners`);
      position=actual;
    }
    assert.ok(Math.hypot(position.x-target.x,position.z-target.z)<.03);
    layoutRoutes++;
  }
}
console.log(`PASS ${layoutRoutes} sequential station routes across all 20 domain layouts.`);
