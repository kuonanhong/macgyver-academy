import assert from 'node:assert/strict';
import {quantumState,quantumLabMarkup} from '../public/academy/quantum-lab.js';
const close=(a,b)=>assert(Math.abs(a-b)<1e-10,`${a} != ${b}`);
close(quantumState().probabilities[0],1);
const bell=quantumState([{gate:'H',target:0},{gate:'CX',control:0,target:1}]);
bell.probabilities.forEach((p,i)=>close(p,i===0||i===3?.5:0));close(bell.concurrence,1);close(bell.purity,.5);
const phase=quantumState([{gate:'H',target:0},{gate:'CX',control:0,target:1},{gate:'Z',target:0}]);
close(phase.state[3][0],-Math.SQRT1_2);phase.probabilities.forEach((p,i)=>close(p,bell.probabilities[i]));
for(const target of [0,1])for(const gate of ['H','X','Z']){const r=quantumState([{gate,target},{gate,target}]);close(r.probabilities[0],1);close(r.norm,1);close(r.concurrence,0);close(r.purity,1);}
close(quantumState([{gate:'RY',target:1,angle:Math.PI}]).probabilities[1],1);
const reverse=quantumState([{gate:'X',target:1},{gate:'CX',control:1,target:0}]);close(reverse.probabilities[3],1);
close(quantumState([{gate:'H',target:0},{gate:'S',target:0}]).state[2][1],Math.SQRT1_2);
assert.throws(()=>quantumState([{gate:'RY',angle:NaN}]));assert.throws(()=>quantumState([{gate:'CX',control:0,target:0}]));assert.throws(()=>quantumState(Array(65).fill({gate:'X'})));
assert(quantumLabMarkup({learningTrack:'quantum'},true).includes('quantumBell'));assert.equal(quantumLabMarkup({title:'Wind'}),'');
console.log('PASS ideal quantum lab: gate unitarity, basis order, phase, Bell entanglement, inverse gates, bounds and bilingual UI.');
