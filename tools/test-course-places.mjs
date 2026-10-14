import assert from 'node:assert/strict';
import fs from 'node:fs';
import {setCoursePlaces,placeForCourse,googlePlaceUrls,coursePlacesMarkup,bindCoursePlaces,placeLocationMarkup} from '../public/academy/course-places.js';
const data=JSON.parse(fs.readFileSync(new URL('../public/academy/data/course-places.json',import.meta.url)));
const courses=JSON.parse(fs.readFileSync(new URL('../public/academy/data/featured.json',import.meta.url)));
setCoursePlaces(data);
assert.equal(data.courses.length,courses.length);
for(const course of courses){
  const entry=placeForCourse(course.id);assert.ok(entry,course.id);
  for(const zh of [true,false]){
    const html=coursePlacesMarkup(course,{zh});assert.ok(html.includes(`data-course-place="${course.id}"`));assert.ok(!html.includes('<iframe'), 'No external map before click');
  }
  const links=googlePlaceUrls(entry.place,'zh-TW');
  assert.equal(new URL(links.link).hostname,'www.google.com');
  assert.equal(new URL(links.embed).searchParams.get('q'),`${entry.place.lat},${entry.place.lng}`);
  assert.equal(new URL(links.link).searchParams.get('query'),`${entry.place.lat},${entry.place.lng}`);
  assert(entry.place.address&&entry.place.coordinateScope);
  for(const zh of [true,false]){
    const detail=placeLocationMarkup(entry.place,{zh});
    assert(detail.includes(`${entry.place.lat}, ${entry.place.lng}`));
    assert(detail.includes(zh?'地址／地理位置':'Address / geographical location'));
    assert(!/<(?:iframe|script|img)\b/.test(detail),'Details do not load a map');
  }
  assert.ok(entry.history.length>=2);assert.ok(entry.references.length>=2);
}
assert.equal(coursePlacesMarkup({id:'roadmap'}),'');
const odd=googlePlaceUrls({lat:0,lng:0,mapQuery:'<script>&東京 / Taiwan'},'" onload=alert(1)');
assert.equal(new URL(odd.embed).searchParams.get('hl'),'en');
assert.equal(new URL(odd.embed).searchParams.get('q'),'0,0');
assert.equal(new URL(odd.link).searchParams.get('query'),'0,0');
assert.throws(()=>googlePlaceUrls({lat:91,lng:20}),TypeError);
assert.throws(()=>googlePlaceUrls({lat:10,lng:NaN}),TypeError);
const attack=placeLocationMarkup({lat:0,lng:0,name:'<script>alert(1)</script>',address:'<img src=x onerror=alert(1)>',coordinateScope:'<script>x</script>'});
assert(!/<(?:script|img)\b/.test(attack));assert(attack.includes('&lt;script&gt;'));
assert(!placeLocationMarkup(null).includes('maps.google'),'Unknown places get no invented map pin');
const api=googlePlaceUrls({lat:10,lng:20,mapQuery:'Hsinchu'},'en','browser-restricted-test');
assert.equal(new URL(api.embed).pathname,'/maps/embed/v1/place');
assert.equal(new URL(api.embed).searchParams.get('key'),'browser-restricted-test');
let load=null, externalRequests=0,rendered=0;
const children=[];
const host={appendChild:frame=>{children.push(frame);externalRequests++;},querySelector:()=>children[0]||null};
const button={addEventListener:(type,fn)=>{assert.equal(type,'click');load=fn;}};
const root={isConnected:true,dataset:{coursePlace:courses[0].id,placeCompact:'true'},innerHTML:'',querySelector:s=>s==='[data-load-course-map]'?button:host};
globalThis.document={querySelectorAll:()=>[root],createElement:tag=>{assert.equal(tag,'iframe');return {};}};
globalThis.window={};
await bindCoursePlaces({zh:true,language:'zh-TW',onRendered:()=>rendered++});
assert.equal(externalRequests,0);assert.equal(rendered,1);assert.ok(root.innerHTML.includes('Google'));
load();load();assert.equal(externalRequests,1);assert.equal(children[0].referrerPolicy,'strict-origin-when-cross-origin');assert.ok(button.disabled);
root.isConnected=false;root.innerHTML='stale';await bindCoursePlaces();assert.equal(root.innerHTML,'stale');
assert(root.innerHTML==='stale');
console.log(`Course places passed: ${courses.length} bilingual histories, safe URLs, explicit map consent, no duplicate iframe, stale-render protection.`);
