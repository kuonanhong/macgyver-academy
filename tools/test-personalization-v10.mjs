import assert from 'node:assert/strict';
import fs from 'node:fs';
import {createRequire} from 'node:module';
import {createPersonalization,normalizePreferences,preferenceKey,choosePersonalVoice,showcaseMarkup,SHOWCASES} from '../public/academy/personalization.js';

const voices=[{name:'English A',lang:'en-US',voiceURI:'en-a',default:true},{name:'English B',lang:'en-GB',voiceURI:'en-b'},{name:'Chinese',lang:'zh-TW',voiceURI:'zh-a'}];
assert.equal(choosePersonalVoice(voices,'en','en-b'),voices[1]);
assert.equal(choosePersonalVoice(voices,'zh-TW','en-b'),voices[2],'a saved foreign voice cannot override text language');
assert.equal(choosePersonalVoice(voices,'ja','en-b'),null);
assert.deepEqual(normalizePreferences({theme:'evil',layout:'hidden',voiceLanguage:'<script>',rate:Infinity,pitch:-2}),{theme:'system',layout:'comfortable',accent:'forest',fontScale:1,sidebar:'full',voiceGender:'any',voiceStyle:'professional',voiceLanguage:'follow',voiceURI:'',rate:.9,pitch:.6});
assert.notEqual(preferenceKey('guest'),preferenceKey('member:alice'));

const records=new Map(),storage={getItem:key=>records.get(key),setItem:(key,value)=>records.set(key,value)};
const root={dataset:{}},themeColor={},document={documentElement:root,querySelector:()=>themeColor,getElementById:()=>null};
let profile='member:alice';const media={matches:true,addEventListener(){},removeEventListener(){}},environment={matchMedia:()=>media,addEventListener(){},removeEventListener(){}};
const controller=createPersonalization({document,environment,storage,getProfileId:()=>profile,getLanguage:()=> 'zh-TW',speechSynthesis:{getVoices:()=>voices,addEventListener(){},removeEventListener(){}}});
assert.equal(root.dataset.theme,'dark','system dark preference is effective');
controller.update({theme:'light',layout:'compact',voiceLanguage:'en-GB',voiceURI:'en-b',rate:.8,pitch:1.1});
assert.equal(root.dataset.theme,'light');assert.equal(root.dataset.layout,'compact');
assert.equal(controller.getNarrationLanguage('zh-TW'),'en-GB');
assert.deepEqual(controller.getSpeechOptions('en-GB'),{language:'en-GB',voiceURI:'en-b',rate:.8,pitch:1.1,genderApproximated:false});
profile='member:bob';controller.syncProfile();assert.equal(root.dataset.theme,'dark');assert.equal(root.dataset.layout,'comfortable');assert.equal(controller.preferences.voiceURI,'');
controller.update({theme:'dark',rate:1.2});profile='member:alice';controller.syncProfile();assert.equal(root.dataset.theme,'light');assert.equal(controller.preferences.rate,.8);assert.equal(controller.preferences.voiceURI,'en-b');controller.destroy();
const broken=createPersonalization({document,environment,storage:{getItem(){throw Error('blocked')},setItem(){throw Error('blocked')}},getProfileId:()=> 'private-browser'});assert.doesNotThrow(()=>broken.update({theme:'dark'}));assert.equal(root.dataset.theme,'dark');broken.destroy();

const html=showcaseMarkup({zh:true});assert.equal((html.match(/role="tabpanel"/g)||[]).length,2);assert(!/<iframe/.test(html),'third-party frames are absent before a click');for(const item of SHOWCASES)assert(html.includes(item.url));assert(html.includes('data-showcase-load'));assert(html.includes('rel="noopener noreferrer"'));
const require=createRequire(import.meta.url),deps=createRequire(require.resolve('@tailwindcss/postcss')),postcss=deps('postcss'),lightning=deps('lightningcss');
const css=fs.readFileSync(new URL('../public/academy/workspace-v10.css',import.meta.url),'utf8');postcss.parse(css);const parsed=lightning.transform({filename:'workspace-v10.css',code:Buffer.from(css),errorRecovery:false});assert.equal(parsed.warnings.length,0);
function luminance(hex){const c=hex.slice(1).match(/../g).map(x=>parseInt(x,16)/255).map(x=>x<=.04045?x/12.92:((x+.055)/1.055)**2.4);return c[0]*.2126+c[1]*.7152+c[2]*.0722}
for(const [fg,bg] of [['#233842','#f5f7f8'],['#61717b','#ffffff'],['#ffffff','#245f66'],['#e0eaed','#19282f'],['#a8bcc4','#111b20'],['#102c33','#87cbd0']]){const pair=[luminance(fg),luminance(bg)].sort((a,b)=>b-a);assert((pair[0]+.05)/(pair[1]+.05)>=4.5,`${fg} on ${bg} needs AA text contrast`)}
console.log('V10 personalization PASS: profile isolation/reload, bounded preferences, unavailable storage, same-language voice choice, no third-party iframe before opt-in, CSS parsing and light/dark text contrast.');
