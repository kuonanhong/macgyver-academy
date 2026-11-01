import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {DOMAIN_PROFILES_V22, buildWorldConfig, safePhotoPath} from '../public/academy/walk-domains-v22.js';
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const academy = path.join(root,'public/academy');
const data = JSON.parse(fs.readFileSync(path.join(academy,'data/experiences-v21.json'),'utf8'));
const before = JSON.stringify(data);
assert.equal(Object.keys(DOMAIN_PROFILES_V22).length,20);
assert.deepEqual(new Set(Object.keys(DOMAIN_PROFILES_V22)),new Set(data.domains.map(d=>d.id)));
const signatures = new Set();
const kinds = new Set(['lithography','robot','vehicle','turbine','bench','crane','tank','rack','bridge','furnace','ship','aircraft','instrument','train','dish']);
let worlds=0,stationCount=0,photographs=0;
for(const scene of data.experiences){
  const world = buildWorldConfig(scene,data.assets,'zh-TW');
  assert.equal(world.id,scene.id);
  assert.equal(world.domainId,scene.category);
  assert.equal(world.stations.length,scene.chapters.length);
  assert.equal(world.stations.length,6);
  assert.equal(world.language,'zh-TW');
  assert(world.bounds.width>=24 && world.bounds.depth>=32);
  for(const [i,s] of world.stations.entries()){
    assert.equal(s.id,scene.chapters[i].id);
    assert.equal(s.title,scene.chapters[i].title);
    assert.equal(s.titleEn,scene.chapters[i].titleEn);
    assert(kinds.has(s.kind),s.kind);
    assert(Math.abs(s.x)+1.8<world.bounds.width/2-1,'Machinery fits within side walls');
    assert(Math.abs(s.z)+1.5<world.bounds.depth/2-1,'Machinery fits within end walls');
    assert(Math.abs(s.approach.x-s.x)>1.8+.35,'Approach is outside collision footprint');
    assert(Math.abs(s.approach.x)<world.bounds.width/2-1);
    assert.equal(s.approach.z,s.z);
    for(const other of world.stations.slice(i+1)){
      assert(Math.abs(s.x-other.x)>3.6+.7 || Math.abs(s.z-other.z)>3+.7,'Separate machinery and navigable walkways');
    }
    if(s.photoSrc){
      photographs++;
      assert(fs.existsSync(path.join(academy,s.photoSrc)),s.photoSrc);
      assert(data.assets.some(a=>a.id===s.photoAssetId && (a.src||a.path)===s.photoSrc));
      assert(s.photoCredit.author && s.photoCredit.license && s.photoCredit.sourceUrl,'Photo provenance retained');
      assert(!data.assets.find(a=>a.id===s.photoAssetId).panoramaVerified,'Fixed panoramas are not stretched into photo panels');
    }
    stationCount++;
  }
  signatures.add(JSON.stringify([world.layout,world.bounds,world.stations.map(s=>[s.kind,s.x,s.z])]));
  // The renderer receives independent objects; editing one world does not alter
  // the authored profile or another journey's machine layout.
  const expected = DOMAIN_PROFILES_V22[scene.category].stations[0].x;
  world.stations[0].x=999;
  world.bounds.width=999;
  assert.equal(DOMAIN_PROFILES_V22[scene.category].stations[0].x,expected);
  assert.notEqual(buildWorldConfig(scene,data.assets).bounds.width,999);
  worlds++;
}
assert.equal(JSON.stringify(data),before,'No edits to curriculum or source metadata');
assert.equal(signatures.size,20,'Twenty distinct equipment/layout combinations');
for(const invalid of ['../assets/a.jpg','assets/../a.jpg','assets//a.jpg','assets/./a.jpg','https://example.com/a.jpg','blob:x','assets/a.svg','assets/a.jpg?key=secret','assets/a.jpg#x','assets/a%2Ejpg','assets/a\\b.jpg','assets/a.jpg\n']){
  assert.equal(safePhotoPath(invalid),'',invalid);
}
assert.equal(safePhotoPath('assets/photos/v21-test_1.jpg'),'assets/photos/v21-test_1.jpg');
assert.throws(()=>buildWorldConfig(null),TypeError);
assert.throws(()=>buildWorldConfig({category:'unlisted',chapters:[{}]}),RangeError);
assert.throws(()=>buildWorldConfig({category:'semiconductor',chapters:[]}),RangeError);
assert.throws(()=>buildWorldConfig({category:'semiconductor',chapters:Array(7).fill({})}),RangeError);
assert.equal(buildWorldConfig(data.experiences[0],[]).stations[0].photoSrc,'','Missing imagery remains explicitly empty');
console.log(JSON.stringify({ok:true,worlds,stations:stationCount,photoReferences:photographs,distinctDomainLayouts:signatures.size}));
