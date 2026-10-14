import assert from 'node:assert/strict';
import {calculateLab,LABS} from '../public/academy/engineering-labs.js';
const near=(actual,expected)=>assert.ok(Math.abs(actual-expected)<1e-9,`${actual} != ${expected}`);
near(calculateLab('lithography',{k:.3,wavelength:13.5,na:.33}),12.272727272727272);
near(calculateLab('coverage',{top:20,side:12}),60);
near(calculateLab('resistance',{rho:1.7,length:100,width:200,thickness:200}),42.5);
near(calculateLab('thermal',{power:20,thickness:100,k:2,area:100}),10);
near(calculateLab('yield',{density:0,area:100}),100);
near(calculateLab('overlay',{stage:3,mark:4,distortion:0}),5);
near(calculateLab('ald',{cycles:100,growth:.1}),10);
near(calculateLab('selectivity',{target:40,mask:2}),20);
near(calculateLab('aspect',{height:600,width:100}),6);
near(calculateLab('diffusion',{diffusivity:2,time:100}),20);
near(calculateLab('capacitance',{area:10,relative:4,thickness:10}),35.4167512512);
near(calculateLab('capability',{mean:15,sigma:1}),5/3);
near(calculateLab('shot',{photons:100}),10);
near(calculateLab('tlm',{length:20,width:10,sheet:10,contact:5}),30);
for(const [kind,lab] of Object.entries(LABS)){
 for(const pos of [2,3,5])assert.ok(Number.isFinite(calculateLab(kind,Object.fromEntries(lab.params.map(p=>[p[0],p[pos]])))));
}
console.log('PASS: fourteen engineering formulas, unit conversion and slider boundary values');
