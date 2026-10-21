#!/usr/bin/env node
// Focused final-data follow-up. Preserves the earlier full layout report.
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import http from 'node:http';
import crypto from 'node:crypto';
import {fileURLToPath,pathToFileURL} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..'),pub=path.join(root,'public/academy');
const hash=file=>crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');
const layoutFile=path.join(root,'docs/VALIDATION_BROWSER_V15.json'),layout=JSON.parse(fs.readFileSync(layoutFile));
const outputReport=path.resolve(root,process.env.MACGYVER_FINAL_DATA_REPORT||'docs/VALIDATION_BROWSER_V15_FINAL_DATA.json');
const screenshotPath=process.env.MACGYVER_FINAL_DATA_SCREENSHOT||'docs/qa-v15/b225-final-sensitivity-en.png';
const index=JSON.parse(fs.readFileSync(path.join(pub,'data/lazy/index.json')));
const courses=Object.fromEntries(['b225','b296'].map(id=>[id,JSON.parse(fs.readFileSync(path.join(pub,index.courses[id].file)))]));
const names=['app.bundle.js','offline-data.js','bootstrap.js','curriculum-loader.js','lazy-index-codec.js','workspace-v12.css','style.css','data/lazy/index.compact.json'];
const result={status:'RUNNING',startedAt:new Date().toISOString(),scope:'Final index/home and b225/b296 data only; does not repeat three-viewport layout QA',browser:null,viewport:{width:1440,height:960},simulatedViewport:true,retainedLayoutReport:'docs/VALIDATION_BROWSER_V15.json',retainedLayoutReportSha256:hash(layoutFile),finalSourceHashes:Object.fromEntries(names.map(n=>[n,hash(path.join(pub,n))])),checks:[],responses:[],requests:[],pageErrors:[],rawFailedResources:[],networkFailures:[],blockedExternal:[],screenshots:[]};
const codeNames=names.filter(n=>!['offline-data.js','data/lazy/index.compact.json'].includes(n));
result.sourceChangesSinceLayout=codeNames.filter(n=>result.finalSourceHashes[n]!==layout.sourceHashes[n]);
if(result.sourceChangesSinceLayout.length){
  // The one reviewed saved-status localization correction changes the bundle.
  // Accept it only with a completed actual-browser regression for these bytes.
  assert.deepEqual(result.sourceChangesSinceLayout,['app.bundle.js']);
  assert(process.env.MACGYVER_FINAL_DATA_UI_REGRESSION,'Changed application bundle requires the targeted UI regression report');
  const file=path.resolve(root,process.env.MACGYVER_FINAL_DATA_UI_REGRESSION),regression=JSON.parse(fs.readFileSync(file));
  assert(['PASS','PASS_WITH_TRANSPORT_DIAGNOSTIC'].includes(regression.status));
  for(const name of codeNames)assert.equal(result.finalSourceHashes[name],regression.finalSourceHashes[name],'UI regression does not cover final bytes: '+name);
  result.targetedUIRegression={path:path.relative(root,file),sha256:hash(file),status:regression.status,scope:regression.scope};
}
result.layoutCodeAndStylesUnchanged=result.sourceChangesSinceLayout.length===0;
const assets=[{file:'data/lazy/index.compact.json',sha256:hash(path.join(pub,'data/lazy/index.compact.json')),byteLength:fs.statSync(path.join(pub,'data/lazy/index.compact.json')).size},...['b225','b296'].flatMap(id=>[index.courses[id],index.resources[id]])];
const mime={'.html':'text/html','.js':'text/javascript','.css':'text/css','.json':'application/json','.svg':'image/svg+xml','.png':'image/png','.jpg':'image/jpeg','.woff2':'font/woff2'};
const server=http.createServer(async(req,res)=>{
  try{
    const pathname=decodeURIComponent(new URL(req.url,'http://127.0.0.1').pathname);
    if(pathname==='/runtime-mode.js'){res.writeHead(200,{'content-type':'text/javascript'});res.end('window.MG_STATIC_MODE=true;');return;}
    const file=path.resolve(pub,'.'+(pathname==='/'?'/index.html':pathname));if(!file.startsWith(pub+path.sep)){res.writeHead(403);res.end();return;}
    const body=await fs.promises.readFile(file);res.writeHead(200,{'content-type':mime[path.extname(file)]||'application/octet-stream','content-length':body.length,'cache-control':'no-store'});res.end(body);
  }catch(error){res.writeHead(error.code==='ENOENT'?404:500);res.end();}
});
let browser,context;
try{
  const module=process.env.MACGYVER_PLAYWRIGHT_MODULE;
  const {chromium}=await import(module?pathToFileURL(path.resolve(module)).href:'playwright');
  await new Promise(r=>server.listen(0,'127.0.0.1',r));const origin='http://127.0.0.1:'+server.address().port;
  browser=await chromium.launch({headless:true,args:['--no-sandbox','--disable-background-networking','--disable-component-update','--disable-sync','--no-first-run']});
  result.browser={engine:'Chromium',version:browser.version(),headless:true};
  context=await browser.newContext({viewport:result.viewport,locale:'zh-TW',serviceWorkers:'block',reducedMotion:'reduce'});
  await context.addInitScript(()=>{
    const streams=new WeakMap(),readers=new WeakMap(),records=[];window.__MG_QA_STREAMS__=records;
    const fetch=window.fetch,getReader=ReadableStream.prototype.getReader,read=ReadableStreamDefaultReader.prototype.read;
    window.fetch=function(input,options){return fetch.call(this,input,options).then(response=>{const record={url:new URL(typeof input==='string'||input instanceof URL?String(input):input.url,location.href).href,status:response.status,declaredBytes:Number(response.headers.get('content-length'))||null,readBytes:0,eof:false,signalAborted:options?.signal?.aborted||false};records.push(record);options?.signal?.addEventListener('abort',()=>{record.signalAborted=true;},{once:true});if(response.body)streams.set(response.body,record);return response;});};
    ReadableStream.prototype.getReader=function(...args){const reader=getReader.apply(this,args);if(streams.has(this))readers.set(reader,streams.get(this));return reader;};
    ReadableStreamDefaultReader.prototype.read=function(...args){return read.apply(this,args).then(value=>{const record=readers.get(this);if(record){record.readBytes+=value.value?.byteLength||0;if(value.done)record.eof=true;}return value;});};
  });
  await context.route('**/*',route=>{const u=new URL(route.request().url());if(u.origin===origin||['data:','blob:','about:'].includes(u.protocol))return route.continue();result.blockedExternal.push(u.href);return route.abort('blockedbyclient');});
  const page=await context.newPage();page.setDefaultTimeout(15000);
  page.on('request',r=>result.requests.push(r.url()));page.on('pageerror',e=>result.pageErrors.push(e.message));
  page.on('requestfailed',r=>result.rawFailedResources.push({url:r.url(),error:r.failure()?.errorText}));
  page.on('response',r=>{if(r.status()>=400)result.rawFailedResources.push({url:r.url(),status:r.status()});});
  const cdp=await context.newCDPSession(page),urls=new Map();await cdp.send('Network.enable');cdp.on('Network.requestWillBeSent',e=>urls.set(e.requestId,e.request.url));cdp.on('Network.loadingFailed',e=>result.networkFailures.push({url:urls.get(e.requestId),...e}));
  await page.goto(origin+'/index.html',{waitUntil:'domcontentloaded'});await page.locator('.explorer-hero').waitFor({state:'visible'});
  assert.equal(result.requests.filter(u=>/\/data\/lazy\/(courses|resources)\//.test(u)).length,0);
  assert.match(await page.locator('.explorer-hero').innerText(),/904/);result.checks.push({name:'Final home visible with 904 guided courses and zero lesson-body preloads',status:'PASS'});
  result.responses=await page.evaluate(async assets=>{const out=[];for(const asset of assets){const response=await window.MacGyverNativeFetch(asset.file+'?qa=final-checksum',{cache:'no-store'});if(!response.ok)throw Error('HTTP '+response.status);const bytes=new Uint8Array(await response.arrayBuffer());const digest=await crypto.subtle.digest('SHA-256',bytes);const sha256=[...new Uint8Array(digest)].map(n=>n.toString(16).padStart(2,'0')).join('');const value=JSON.parse(new TextDecoder().decode(bytes));out.push({file:asset.file,status:response.status,byteLength:bytes.length,sha256,courseId:value.id||null,stepCount:value.stages?.flatMap(s=>s.steps).length||null,catalogCount:value.catalog?.length||null});}return out;},assets);
  for(const expected of assets){const got=result.responses.find(r=>r.file===expected.file);assert.equal(got.byteLength,expected.byteLength);assert.equal(got.sha256,expected.sha256);}
  assert.equal(result.responses[0].catalogCount,index.catalog.length);
  result.checks.push({name:'Actual Chromium downloaded bytes and SHA-256 match final index, both courses and both resources',status:'PASS',assets:assets.length});
  for(const id of ['b225','b296']){
    if(id==='b296'){await page.evaluate(()=>{location.hash='home';});await page.locator('#search').waitFor({state:'visible'});}
    await page.locator('#search').fill(id);await page.locator(`#explorerCatalog a[href="#project/${id}"]`).first().click();await page.locator(`#beginCourse[data-id="${id}"]`).waitFor({state:'visible'});
    assert.equal(await page.locator('[data-curriculum-step]').count(),40);assert.deepEqual(await page.locator('[data-curriculum-step]').evaluateAll(rows=>rows.map(r=>r.dataset.curriculumStep)),courses[id].stages.flatMap(s=>s.steps.map(x=>x.id)));
    assert((await page.locator('.project-brief-title h1').innerText()).trim()===courses[id].title);
    if(id==='b225'){
      const example=page.locator('.worked-example');await example.scrollIntoViewIfNeeded();assert(await example.isVisible());
      let text=await example.innerText();for(const value of ['降雨敏感度','60改為90','37.53','增加50%'])assert(text.includes(value),'Missing visible Chinese sensitivity: '+value);
      await page.locator('#language').selectOption('en');await page.waitForFunction(()=>document.documentElement.lang==='en');await example.scrollIntoViewIfNeeded();text=await example.innerText();for(const value of ['changing only rainfall intensity','60 to 90 mm/h','37.53','50%'])assert(text.includes(value),'Missing visible English sensitivity: '+value);
      const name=screenshotPath,file=path.join(root,name);await page.screenshot({path:file,animations:'disabled'});result.screenshots.push({path:name,sha256:hash(file)});
      await page.locator('#language').selectOption('zh-TW');await page.waitForFunction(()=>document.documentElement.lang==='zh-TW');
      result.checks.push({name:'b225 new single-parameter sensitivity is visibly rendered in Chinese and English',status:'PASS',inputs:'A=2 km² and C=0.75 fixed; intensity 60→90 mm/h',displayedResult:'25.02→37.53 m³/s; +50%'});
    }
    result.checks.push({name:id+' final course title and all 40 step IDs are visible/rendered',status:'PASS'});
  }
  result.fetchStreams=await page.evaluate(()=>window.__MG_QA_STREAMS__);
  const billing404=result.rawFailedResources.some(r=>r.url===origin+'/api/billing/config'&&r.status===404);
  result.expectedBillingFailures=result.rawFailedResources.filter(r=>r.url===origin+'/api/billing/config'&&(r.status===404||(billing404&&r.error==='net::ERR_ABORTED')));
  result.postReadCancellations=result.rawFailedResources.flatMap(row=>{
    const asset=assets.find(a=>row.url===origin+'/'+a.file),read=result.fetchStreams.find(r=>r.url===row.url),verified=asset&&result.responses.find(r=>r.file===asset.file&&r.sha256===asset.sha256&&r.byteLength===asset.byteLength);
    if(row.error!=='net::ERR_ABORTED'||!asset||!verified||read?.status!==200||!read.eof||read.signalAborted||read.declaredBytes!==asset.byteLength||read.readBytes!==asset.byteLength)return [];
    return [{...row,readEvidence:read,checksumEvidence:verified,scope:'Exact final asset, fully read to EOF; independent browser checksum matches disk. Requested pages and sensitivity text rendered.'}];
  });
  const classified=[...result.expectedBillingFailures,...result.postReadCancellations];result.unexpectedFailures=result.rawFailedResources.filter(row=>!classified.some(x=>x.url===row.url&&x.error===row.error&&x.status===row.status));
  assert.equal(result.unexpectedFailures.length,0,JSON.stringify(result.unexpectedFailures));assert.equal(result.pageErrors.length,0);assert.equal(result.blockedExternal.length,0);
  result.status=result.postReadCancellations.length?'PASS_WITH_TRANSPORT_DIAGNOSTIC':'PASS';
}catch(error){result.status='FAIL';result.error=error.stack||String(error);}
finally{
  if(context)await context.close();if(browser)await browser.close();await new Promise(r=>server.close(r));
  assert.equal(hash(layoutFile),result.retainedLayoutReportSha256,'The retained layout report must not be overwritten');
  result.finishedAt=new Date().toISOString();result.limitations=['This targeted supplement does not repeat device/layout coverage. Refer to the unchanged earlier report.','Static billing API absence and any fully consumed post-read cancellation events remain recorded; zero network warnings is not claimed.'];
  fs.writeFileSync(outputReport,JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify({status:result.status,checks:result.checks.length,assets:result.responses.length,error:result.error?.split('\n')[0]}));process.exitCode=result.status.startsWith('PASS')?0:1;
}
