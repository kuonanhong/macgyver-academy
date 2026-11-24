#!/usr/bin/env node
/** Real Three.js scene/math tests with only GPU and canvas raster calls stubbed.
 * Does not claim browser appearance, WebGL performance or final-film verification.
 */
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import assert from 'node:assert/strict';
import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const dir=path.join(root,'public/academy');
const sandbox={window:{},console,performance:{now:()=>0},document:{createElement:()=>({width:1,height:1,getContext:()=>({createLinearGradient:()=>({addColorStop(){}}),fillRect(){},fillText(){}})})}};
vm.createContext(sandbox);vm.runInContext(fs.readFileSync(path.join(dir,'vendor/three.js'),'utf8'),sandbox);
const real=sandbox.window.THREE;
class Renderer {constructor(){this.shadowMap={};this.info={render:{calls:0,triangles:0}};}setPixelRatio(){}setSize(){}render(scene,camera){scene.updateMatrixWorld(true);camera.updateMatrixWorld(true);}dispose(){}}
class PMREM {fromEquirectangular(){return {texture:{},dispose(){}};}dispose(){}}
sandbox.window.THREE={...real,WebGLRenderer:Renderer,PMREMGenerator:PMREM};
vm.runInContext(fs.readFileSync(path.join(dir,'packaging-process-scene-v34.js'),'utf8'),sandbox);
const engine=sandbox.window.MG_PACKAGING_PROCESS_SCENE.create({canvas:{clientWidth:1280,clientHeight:720}});
const titles=new Set(),centers=new Set();let frames=0;
for(const [w,h] of [[1280,720],[390,580]]){
  engine.resize(w,h,1);
  for(const t of [0,2,5,9,15,29.5,30,31,32,45,59.9,65,95,125,155,185,215,245,275,292,299,300]){
    const a=JSON.parse(JSON.stringify(engine.render(t)));engine.render(111);const b=JSON.parse(JSON.stringify(engine.render(t)));
    assert.deepEqual(a,b,`seek deterministic at ${w}/${t}`);
    assert.equal(a.chapterIndex,Math.min(9,Math.floor(t/30)));assert.equal(a.fieldVisualization,'illustrative_not_solved');
    assert.equal(a.architectureSelected,false);assert.ok(Object.values(a.camera).every(Number.isFinite));
    const p=a.projectedBounds;assert.ok(p.minX>-.99&&p.maxX<.99&&p.minY>-.8&&p.maxY<.9,`content out of frame at ${w}/${t}: ${JSON.stringify(p)}`);
    const center=.5-(p.minY+p.maxY)/4;assert.ok(Math.abs(center-.43)<.001,`caption-safe vertical center at ${w}/${t}`);
    for(const l of engine.getLabels()){assert.ok(l.en&&l.zh);assert.ok(Number.isFinite(l.x)&&Number.isFinite(l.y));}
    titles.add(a.view);if(t%30===5||t===15)centers.add([a.camera.x.toFixed(2),a.camera.z.toFixed(2)].join(','));frames++;
  }
}
assert.equal(titles.size,10);assert.ok(centers.size>=10);
assert.throws(()=>engine.setProcess('C02'),/not been implemented/);
const script=JSON.parse(fs.readFileSync(path.join(root,'docs/packaging-process-scripts-v34/C01.json'),'utf8'));
assert.equal(script.cues.length,10);assert.equal(script.durationSeconds,300);assert.equal(script.status.film,'not_produced');
assert.deepEqual(script.languages,['zh-TW','zh-CN','en','ja','ko']);
assert.deepEqual(JSON.parse(fs.readFileSync(path.join(dir,'assets/packaging-process-v34/C01/script.json'),'utf8')),script);
const scriptSandbox={window:{}};vm.runInNewContext(fs.readFileSync(path.join(dir,'packaging-process-c01-v34.js'),'utf8'),scriptSandbox);
assert.deepEqual(JSON.parse(JSON.stringify(scriptSandbox.window.MACGYVER_PACKAGING_C01)),script);
for(const [i,c] of script.cues.entries()){
  assert.equal(c.start,i*30);assert.equal(c.end,(i+1)*30);assert.equal(c.key,sandbox.window.MG_PACKAGING_PROCESS_SCENE.views[i]);
  assert.ok(c.text.en.split(/\s+/).length>=45);assert.ok(c.text['zh-TW'].length>=90);assert.ok(c.shot.camera&&c.shot.action);
  for(const lang of script.languages){assert.ok(c.text[lang]?.length>=90);assert.ok(c.title[lang]?.length>=5);}
  assert.match(c.text.ja,/[\u3040-\u30ff]/);assert.match(c.text.ko,/[\uac00-\ud7af]/);
}
const bw=script.example.bandwidth,th=script.example.thermal;
assert.equal(bw.oneDirectionLanes*bw.rawGbpsPerLane*bw.aggregateUsefulEfficiency/8,bw.usefulGBps);
assert.equal(th.exampleAmbientC+th.sustainedPackagePowerW*th.hypotheticalSystemEffectiveResistanceKPerW,th.screeningJunctionTemperatureC);
assert.equal(th.exampleAmbientC+th.sustainedPackagePowerW*script.example.changedCoolingScenario.hypotheticalSystemEffectiveResistanceKPerW,90);
engine.dispose();engine.dispose();
console.log(JSON.stringify({result:'PASS',frames,viewportSizes:[[1280,720],[390,580]],distinctViews:10,deterministicSeeks:true,captionSafeFraming:true,scriptCues:10,completeNarrationLanguages:5,exactPublicScriptCopies:true,filmStatus:'not_produced',limits:'CPU Three.js geometry/math only; GPU appearance, narration timing and actual film remain separate checks'},null,2));
