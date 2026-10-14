import assert from 'node:assert/strict';
import {WORLD_LABS,calculateWorldLab,worldLabKind} from '../public/academy/world-project-labs.js';
for(const [kind,lab] of Object.entries(WORLD_LABS)){
 const values=Object.fromEntries(lab.params.map(p=>[p[0],p[5]]));assert(Number.isFinite(calculateWorldLab(kind,values)),kind);
 for(const p of lab.params)assert(Math.abs((p[5]-p[2])/p[4]-Math.round((p[5]-p[2])/p[4]))<1e-8,kind+': initial value aligns with slider step');
 for(const p of lab.params)for(const boundary of [p[2],p[3]])assert(Number.isFinite(calculateWorldLab(kind,{...values,[p[0]]:boundary})),kind);
 assert.throws(()=>calculateWorldLab(kind,{...values,[lab.params[0][0]]:NaN}));
 assert.throws(()=>calculateWorldLab(kind,{...values,[lab.params[0][0]]:lab.params[0][3]+1}));
}
assert.equal(calculateWorldLab('worldCarnot',{hot:600,cold:300}),50);
assert.equal(calculateWorldLab('worldOre',{ore:1000,grade:2,recovery:.8}),1.6);
assert.equal(calculateWorldLab('worldGeothermal',{flow:50,cp:4.2,drop:80}),16.8);
assert(Math.abs(calculateWorldLab('worldHydro',{head:50,flow:100,eta:.9})-44.145)<1e-10);
assert.equal(calculateWorldLab('worldHeat',{heat:100,efficiency:.2,aux:150}),-130,'Do not hide negative net output');
assert.equal(worldLabKind({educationEdition:11,architectureFamily:'wind'}),'worldWind');
console.log('PASS 8 world-project balances: unit conversions, physical bounds, negative net output and input rejection.');
