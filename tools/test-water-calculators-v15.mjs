import assert from 'node:assert/strict';
import {WATER_LABS,calculateWaterLab as calc,waterLabKind} from '../public/academy/water-calculators.js';
import {calculateLab,labKind,labMarkup} from '../public/academy/engineering-labs.js';
const close=(a,b,rel=1e-9)=>assert.ok(Math.abs(a-b)<=rel*Math.max(1,Math.abs(b)),`${a} != ${b}`);
const defaults=k=>Object.fromEntries(WATER_LABS[k].params.map(p=>[p[0],p[5]]));
assert.equal(Object.keys(WATER_LABS).length,12);
for(const k of Object.keys(WATER_LABS)){
 const v=defaults(k);assert.ok(Number.isFinite(calc(k,v)),k);close(calculateLab(k,v),calc(k,v));
 for(const [key,,min,max] of WATER_LABS[k].params){for(const bad of [NaN,Infinity,min-1,max+1])assert.throws(()=>calc(k,{...v,[key]:bad}),RangeError);}
}
close(calc('waterHydro',defaults('waterHydro')),490.5);
close(calc('waterPower',defaults('waterPower')),28.2528);
close(calc('waterFroude',defaults('waterFroude')),.32);
close(calc('waterStorage',defaults('waterStorage')),107200);
close(calc('waterDarcy',defaults('waterDarcy')),1.8);
close(calc('waterHammer',defaults('waterHammer')),1);
// Independent physical identities: conjugate momentum and critical Froude.
const j=defaults('waterJump'),y2=calc('waterJump',j),q=j.depth*j.velocity;
close(j.depth**2/2+q*q/(9.81*j.depth),y2*y2/2+q*q/(9.81*y2));
const c=defaults('waterCritical'),yc=calc('waterCritical',c);close((c.flow/(c.b*yc))**2/(9.81*yc),1);
const w=defaults('waterWeir'),qw=calc('waterWeir',w);close(2*w.head/3+(qw/(w.b*2*w.head/3))**2/(2*9.81),w.head);
const wave=defaults('waterWave'),pw=calc('waterWave',wave);close(calc('waterWave',{...wave,height:4}),4*pw);
assert.throws(()=>calc('waterWave',{...wave,depth:10}),RangeError);
assert.throws(()=>calc('waterWave',{...wave,height:8,period:2}),RangeError);
assert.throws(()=>calc('waterJump',{...j,velocity:.5}),RangeError);
assert.throws(()=>calc('waterHydro',{b:4,top:5,bottom:2}),RangeError);
assert.throws(()=>calc('waterStorage',{storage:0,inflow:0,outflow:10,hours:1}),RangeError);
assert.throws(()=>calc('waterHammer',{...defaults('waterHammer'),closure:3}),RangeError);
const course={id:'b260',category:'water',educationEdition:15};const step={id:'b260-v15-001',titleEn:'Water hammer'};
assert.equal(labKind(course,step),'waterHammer');assert.equal(waterLabKind(course,{titleEn:'Legal history'}),'');
assert.equal(waterLabKind({id:'b202',category:'water',v15Extension:{}},{id:'old-step',titleEn:'Water hammer'}),'');
assert.match(labMarkup(course,step,true),/焦科夫斯基/);assert.match(labMarkup(course,step,false),/Joukowsky/);
console.log('PASS: 12 water models; independent conservation identities, unit results, domain rejection, routing and bilingual markup.');
