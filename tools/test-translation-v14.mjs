import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import {createAIClient} from '../public/academy/ai-client.js';
import {claudeCompletion,geminiCompletion,hostedRoutes} from '../lib/tutor-providers.ts';
const bytes=new TextEncoder().encode('GGUF test fixture');
const model={id:'tiny',kind:'browser',bytes:bytes.length,minMemoryGB:1,sha256:crypto.createHash('sha256').update(bytes).digest('hex'),repo:'test/test',revision:'pinned',file:'tiny.gguf'};
const environment={location:{protocol:'https:',origin:'https://example.org',href:'https://example.org/academy/'},document:{baseURI:'https://example.org/academy/'},Worker:class{},WebAssembly:{},navigator:{deviceMemory:8,hardwareConcurrency:8}};
let replies=[],calls=[];class Runtime{setCompat(){}async loadModel(){}async exit(){}async createChatCompletion(options){calls.push(options);let text=replies.shift();return (async function*(){yield {choices:[{delta:{content:text}}]};})();}}
const ai=createAIClient({environment,models:[model],fetcher:async()=>new Response(bytes),importer:async()=>({Wllama:Runtime})});
await assert.rejects(()=>ai.translate({texts:['source'],language:'fr'}));assert.equal(calls.length,0);
await ai.load('tiny',{consent:true});replies=['{"translation":"un"}','```json\n{"translation":"deux"}\n```'];
assert.deepEqual((await ai.translate({texts:['one','','two'],language:'fr'})).translations,['un','','deux']);assert.equal(calls.length,2);assert.match(calls[0].messages[1].content,/one/);assert.equal(calls[0].temperature,0);
for(const malformed of ['{"translation":""}','{"translations":["wrong shape"]}','not JSON']){replies=[malformed];await assert.rejects(()=>ai.translate({texts:['source'],language:'fr'}));assert.equal(ai.state().phase,'ready');}
const before=calls.length;await assert.rejects(()=>ai.translate({texts:['source'],language:'zz'}));assert.equal(calls.length,before);await ai.unload();
let sent;globalThis.fetch=async(url,options)=>{sent={url,options};return Response.json({content:[{type:'thinking',text:'hidden'},{type:'text',text:'answer'}]});};
assert.equal(hostedRoutes({ANTHROPIC_API_KEY:'secret'}).length,0);
assert(!JSON.stringify(hostedRoutes({ANTHROPIC_API_KEY:'secret',ANTHROPIC_MODEL:'test-model'})).includes('secret'));
const image={mimeType:'image/png',data:'AAAA'};const result=await claudeCompletion({ANTHROPIC_API_KEY:'secret',ANTHROPIC_MODEL:'test-model'},'policy','question',image,true);
assert.equal(result.answer,'answer');assert.equal(sent.url,'https://api.anthropic.com/v1/messages');assert.equal(sent.options.redirect,'error');assert.equal(sent.options.headers['x-api-key'],'secret');
const payload=JSON.parse(sent.options.body);assert.equal(payload.system,'policy');assert.equal(payload.messages[0].content[1].source.media_type,'image/png');assert.equal(payload.max_tokens,8192);assert(!sent.options.body.includes('secret'));
await assert.rejects(()=>claudeCompletion({ANTHROPIC_API_KEY:'secret',ANTHROPIC_MODEL:'../bad'},'s','q'));
console.log('PASS V14: explicit loaded CPU model, ordered translations, empty preservation, malformed output rejection, readiness recovery, native Claude system/image/key separation (mock runtimes/providers).');

// Gemini 3.5 Flash-Lite and later omit deprecated sampling parameters.
globalThis.fetch=async(url,options)=>{sent={url,options};return Response.json({candidates:[{content:{parts:[{text:'hidden',thought:true},{text:'{"translations":["bonjour"]}'}]}}]});};
const gemini=await geminiCompletion({GEMINI_API_KEY:'secret'},'translate','hello',undefined,true);
const geminiPayload=JSON.parse(sent.options.body);assert.equal(gemini.answer,'{"translations":["bonjour"]}');
assert.equal(geminiPayload.generationConfig.responseMimeType,'application/json');
for(const key of ['temperature','topP','topK'])assert(!(key in geminiPayload.generationConfig));
console.log('PASS Gemini request omits deprecated sampling parameters and preserves structured output.');
