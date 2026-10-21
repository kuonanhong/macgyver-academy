#!/usr/bin/env node
/** Real Chromium smoke/viewport QA; no dependencies are added to this repository.
 * MACGYVER_PLAYWRIGHT_MODULE=/absolute/path/playwright/index.mjs node tools/test-browser-v15.mjs
 * Optional MACGYVER_BROWSER_SCREEN_DIR and MACGYVER_BROWSER_REPORT select output paths.
 * MACGYVER_BROWSER_SCENARIOS selects a comma-separated subset for focused diagnostics.
 * Run after the final offline build. No course data or application source is modified.
 */
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import http from 'node:http';
import crypto from 'node:crypto';
import {fileURLToPath,pathToFileURL} from 'node:url';

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const publicRoot=path.join(root,'public/academy');
const screenDir=path.resolve(process.env.MACGYVER_BROWSER_SCREEN_DIR||path.join(root,'artifacts/browser-v15/screens'));
const reportFile=path.resolve(process.env.MACGYVER_BROWSER_REPORT||path.join(root,'docs/VALIDATION_BROWSER_V15.json'));
if(process.argv.includes('--help')){
  console.log('Set MACGYVER_PLAYWRIGHT_MODULE to a separately installed playwright/index.mjs. Optional: MACGYVER_BROWSER_SCREEN_DIR, MACGYVER_BROWSER_REPORT. Run after final build-offline. The test starts a loopback static server, blocks external browser requests, and checks three emulated viewports plus file://.');
  process.exit(0);
}
if(process.argv.length>2)throw Error('Only --help is supported. Configure paths with environment variables.');
const sha=file=>crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');
const report={schemaVersion:1,status:'RUNNING',startedAt:new Date().toISOString(),test:'Actual headless Chromium browser; simulated viewports, not physical devices',
  limitations:['No physical phone/tablet, Safari or Firefox was tested.','Arabic checks cover bundled interface strings and RTL layout; course text may remain canonical English, not pretranslated Arabic.','AI entry and local lesson mode controls are checked; no model weights are downloaded and no generative service is invoked.','Local HTTP and file:// only; this is not a live deployment or network-performance benchmark.'],
  staticRuntime:'Loopback server serves runtime-mode.js with MG_STATIC_MODE=true, matching static export; source file remains untouched.',
  browser:null,sourceHashes:{},scenarios:[],screenshots:[],fatalErrors:[]};
report.testHarnessSha256=sha(fileURLToPath(import.meta.url));
for(const name of ['app.bundle.js','offline-data.js','bootstrap.js','curriculum-loader.js','lazy-index-codec.js','workspace-v12.css','style.css','data/lazy/index.compact.json'])report.sourceHashes[name]=sha(path.join(publicRoot,name));
report.rootFileLauncherSha256=sha(path.join(root,'index.html'));
const index=JSON.parse(fs.readFileSync(path.join(publicRoot,'data/lazy/index.json'),'utf8'));
const b296=JSON.parse(fs.readFileSync(path.join(publicRoot,index.courses.b296.file),'utf8'));
const expectedSteps=b296.stages.flatMap(s=>s.steps);
assert.equal(expectedSteps.length,40,'b296 must have the final 40-step curriculum before browser QA');
report.generatedSnapshot={catalog:index.catalog.length,guidedCourses:index.guidedIds.length,reviewedCourse:'b296',reviewedCourseSteps:expectedSteps.length};
const mime={'.html':'text/html; charset=utf-8','.js':'text/javascript; charset=utf-8','.json':'application/json; charset=utf-8','.css':'text/css; charset=utf-8','.svg':'image/svg+xml','.png':'image/png','.jpg':'image/jpeg','.jpeg':'image/jpeg','.webp':'image/webp','.woff2':'font/woff2','.wasm':'application/wasm'};
const server=http.createServer(async(req,res)=>{
  try{
    const pathname=decodeURIComponent(new URL(req.url,'http://127.0.0.1').pathname);
    if(pathname==='/runtime-mode.js'){res.writeHead(200,{'content-type':mime['.js'],'cache-control':'no-store'});res.end('window.MG_STATIC_MODE = true;\n');return;}
    const file=path.resolve(publicRoot,'.'+(pathname==='/'?'/index.html':pathname));
    if(!file.startsWith(publicRoot+path.sep)){res.writeHead(403);res.end();return;}
    const stat=await fs.promises.stat(file);
    if(!stat.isFile()){res.writeHead(404);res.end();return;}
    // A complete local Buffer gives deterministic transport events in the QA
    // browser. Chromium 134 reported cancellation after fully consumed JSON
    // with this fixture's fs ReadStream piping; no app error is suppressed.
    const body=req.method==='HEAD'?null:await fs.promises.readFile(file);
    res.writeHead(200,{'content-type':mime[path.extname(file)]||'application/octet-stream','content-length':body?.length??stat.size,'cache-control':'no-store'});
    res.end(body);
  }catch(error){res.writeHead(error.code==='ENOENT'?404:500);res.end();}
});
let browser;
const payloadRequests=rows=>rows.filter(u=>/\/data\/lazy\/(courses|resources)\//.test(u));
const courseRequests=rows=>rows.filter(u=>/\/data\/lazy\/courses\//.test(u));
const resourceRequests=rows=>rows.filter(u=>/\/data\/lazy\/resources\//.test(u));
const tick=page=>page.evaluate(()=>new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve))));
async function within(promise,milliseconds,message){
  let timer;
  try{return await Promise.race([promise,new Promise((_,reject)=>{timer=setTimeout(()=>reject(Error(message)),milliseconds);})]);}
  finally{clearTimeout(timer);}
}
async function capture(page,scenario,name){
  await page.evaluate(()=>document.fonts.ready);await tick(page);
  const file=path.join(screenDir,`${scenario.id}-${name}.png`);
  await page.screenshot({path:file,animations:'disabled',fullPage:false});
  const row={scenario:scenario.id,name,path:file,sha256:sha(file)};
  report.screenshots.push(row);scenario.screenshots.push(row.path);
}
async function layout(page,scenario,name){
  await tick(page);
  const result=await page.evaluate(()=>{
    const viewport=document.documentElement.clientWidth;
    const width=Math.max(document.documentElement.scrollWidth,document.body.scrollWidth);
    const offenders=width>viewport+1?[...document.body.querySelectorAll('*')].filter(el=>{const r=el.getBoundingClientRect(),s=getComputedStyle(el);return r.width&&r.height&&s.visibility!=='hidden'&&s.position!=='fixed'&&(r.right>viewport+1||r.left< -1);}).slice(0,12).map(el=>({tag:el.tagName,id:el.id,class:typeof el.className==='string'?el.className:'svg',rect:{left:el.getBoundingClientRect().left,right:el.getBoundingClientRect().right,width:el.getBoundingClientRect().width}})):[];
    return {viewport,width,overflow:Math.max(0,width-viewport),direction:document.documentElement.dir,language:document.documentElement.lang,offenders};
  });
  scenario.layouts.push({page:name,...result});
  assert(result.overflow<=1,`${scenario.id} ${name}: horizontal overflow ${result.overflow}px; ${JSON.stringify(result.offenders)}`);
}
async function clickable(page,selector){
  const item=page.locator(selector).first();
  await item.waitFor({state:'visible'});await item.scrollIntoViewIfNeeded();
  // Playwright checks hit target, visibility and enabled state without force.
  await item.click({trial:true});
  return item;
}
async function language(page,code){
  await page.locator('#language').selectOption(code);
  await page.waitForFunction(code=>document.documentElement.lang===code,code);
  if(code==='ar')await page.waitForFunction(()=>!!window.MG_I18N?.ar&&/[\u0600-\u06ff]/.test(document.querySelector('#pageTitle')?.textContent||''));
  await tick(page);
}
async function scenario({id,viewport,isMobile=false,hasTouch=false,file=false},origin){
  const result={id,viewport,isMobile,hasTouch,mode:file?'file://':'HTTP static',status:'RUNNING',checks:[],layouts:[],screenshots:[],requests:[],pageErrors:[],consoleErrors:[],failedResources:[],expectedResourceFailures:[],networkFailures:[],blockedExternal:[]};
  report.scenarios.push(result);
  const context=await browser.newContext({viewport,isMobile,hasTouch,locale:'zh-TW',reducedMotion:'reduce',serviceWorkers:'block'});
  // Record transport completion without copying response bodies or changing
  // application data. This distinguishes incomplete loads from Chromium's
  // occasional Network.loadingFailed event after a Fetch stream reached EOF.
  await context.addInitScript(()=>{
    const streams=new WeakMap(),readers=new WeakMap(),records=[];
    window.__MG_BROWSER_QA_STREAMS__=records;
    const fetch=window.fetch,getReader=ReadableStream.prototype.getReader,read=ReadableStreamDefaultReader.prototype.read;
    window.fetch=function(input,options){return fetch.call(this,input,options).then(response=>{
      const url=new URL(typeof input==='string'||input instanceof URL?String(input):input.url,location.href).href;
      const record={url,status:response.status,declaredBytes:Number(response.headers.get('content-length'))||null,readBytes:0,eof:false,signalAborted:options?.signal?.aborted||false};
      records.push(record);options?.signal?.addEventListener('abort',()=>{record.signalAborted=true;},{once:true});
      if(response.body)streams.set(response.body,record);return response;
    });};
    ReadableStream.prototype.getReader=function(...args){const reader=getReader.apply(this,args),record=streams.get(this);if(record)readers.set(reader,record);return reader;};
    ReadableStreamDefaultReader.prototype.read=function(...args){return read.apply(this,args).then(value=>{const record=readers.get(this);if(record){record.readBytes+=value.value?.byteLength||0;if(value.done)record.eof=true;}return value;});};
  });
  const page=await context.newPage();page.setDefaultTimeout(15000);
  const cdp=await context.newCDPSession(page),networkURLs=new Map();
  await cdp.send('Network.enable');
  cdp.on('Network.requestWillBeSent',event=>networkURLs.set(event.requestId,event.request.url));
  cdp.on('Network.loadingFailed',event=>result.networkFailures.push({url:networkURLs.get(event.requestId),...event}));
  let releaseIndex,startedIndex;
  const indexGate=new Promise(resolve=>{releaseIndex=resolve;});
  const indexStarted=new Promise(resolve=>{startedIndex=resolve;});
  page.on('request',request=>result.requests.push(request.url()));
  page.on('pageerror',error=>result.pageErrors.push(error.message));
  page.on('console',msg=>{if(msg.type()==='error')result.consoleErrors.push(msg.text());});
  page.on('requestfailed',request=>result.failedResources.push({url:request.url(),error:request.failure()?.errorText||'failed'}));
  page.on('response',response=>{if(response.status()>=400)result.failedResources.push({url:response.url(),status:response.status()});});
  await context.route('**/*',async route=>{
    const url=new URL(route.request().url());
    if(!['file:','data:','blob:','about:'].includes(url.protocol)&&url.origin!==origin){result.blockedExternal.push(url.href);await route.abort('blockedbyclient');return;}
    if(!file&&url.pathname==='/data/lazy/index.compact.json'){startedIndex();await indexGate;}
    await route.continue();
  });
  try{
    await page.goto(file?pathToFileURL(path.join(root,'index.html')).href:origin+'/index.html',{waitUntil:'domcontentloaded'});
    if(file){await page.waitForURL(pathToFileURL(path.join(publicRoot,'index.html')).href);result.checks.push({name:'Root file launcher redirects to academy without a server',status:'PASS'});}
    if(!file){
      await within(indexStarted,15000,'Compact index request did not start');
      const entry=await clickable(page,'#main a[href="#catalog/ready"]');
      assert(await page.locator('#main h1').isVisible(),'Home shell has real visible heading while index is held');
      await entry.click();assert.equal(new URL(page.url()).hash,'#catalog/ready');
      assert.equal(payloadRequests(result.requests).length,0);
      await layout(page,result,'delayed-index-home');await capture(page,result,'delayed-index-home');
      result.checks.push({name:'Homepage entry clickable with index response held',status:'PASS'});
      releaseIndex();
    }
    await page.locator('.explorer-hero').waitFor({state:'visible'});
    await clickable(page,'[data-catalog-route="ready"]');
    await layout(page,result,'home-zh');await capture(page,result,'home-zh');
    assert.equal(payloadRequests(result.requests).length,0,'Homepage must not load any course or resources payload');
    result.checks.push({name:'Home loads zero course/resource bodies',status:'PASS',payloadRequests:0});
    await page.locator('#search').fill('b296');
    await page.locator('#explorerCatalog a[href="#project/b296"]').first().click();
    await page.locator('#beginCourse[data-id="b296"]').waitFor({state:'visible'});
    assert.equal(await page.locator('[data-curriculum-step]').count(),40);
    assert.deepEqual(await page.locator('[data-curriculum-step]').evaluateAll(nodes=>nodes.map(n=>n.dataset.curriculumStep)),expectedSteps.map(s=>s.id));
    assert.equal(courseRequests(result.requests).length,1);assert.equal(resourceRequests(result.requests).length,1);
    assert(payloadRequests(result.requests).every(url=>/\/b296-[a-f0-9]+\.(?:json|js)$/.test(new URL(url).pathname)),'Only b296 course/resources are loaded');
    result.checks.push({name:'b296 target-only lazy loading and 40-step catalogue',status:'PASS',courseRequests:courseRequests(result.requests),resourceRequests:resourceRequests(result.requests)});
    await layout(page,result,'b296-brief-zh');await capture(page,result,'b296-brief-zh');
    await page.locator('#beginCourse').click();
    await page.locator('#learnerModel').waitFor({state:'visible'});
    assert.equal(await page.locator('#courseSelect').inputValue(),'b296');
    assert.match(await page.locator('#stepHeading').innerText(),/1\s*\/\s*40/);
    await clickable(page,'#workflowAction');
    await (await clickable(page,'#activateKeyboard')).click();
    assert.equal(await page.locator('#activateKeyboard').getAttribute('aria-pressed'),'true');
    if(await page.locator('#toggleNavigator').isVisible()){
      await page.locator('#toggleNavigator').click();
      assert.equal(await page.locator('#toggleNavigator').getAttribute('aria-expanded'),'true');
      await clickable(page,'#navStage');
      await page.locator('#toggleNavigator').click();
    }
    const correct=page.locator(`[data-answer="${expectedSteps[0].quiz.answer}"]`);
    await correct.click();assert.equal(await correct.getAttribute('aria-pressed'),'true');
    assert((await page.locator('#quizResult').innerText()).trim().length>10);
    result.checks.push({name:'Workshop controls and quiz click/feedback',status:'PASS'});
    for(const code of ['zh-TW','en','ar']){
      await language(page,code);
      assert.equal(await page.locator('html').getAttribute('dir'),code==='ar'?'rtl':'ltr');
      if(code!=='ar')assert.equal((await page.locator('#stepHeading h2').innerText()).trim(),code==='zh-TW'?expectedSteps[0].title:expectedSteps[0].titleEn);
      await page.locator('#stepHeading').scrollIntoViewIfNeeded();
      await clickable(page,'#workflowAction');
      await layout(page,result,'workshop-'+code);await capture(page,result,'workshop-'+code);
    }
    result.checks.push({name:'Traditional Chinese / English lesson headings and Arabic RTL interface',status:'PASS',arabicScope:'UI dictionary and layout; no claim of pretranslated Arabic lesson content'});
    await language(page,'en');
    await (await clickable(page,'#mentorButton')).click();
    await page.locator('#mentorPanel').waitFor({state:'visible'});
    assert.equal(await page.locator('[data-ai-model]').inputValue(),'lesson');
    await page.locator('#mentorQuestion').fill('How do the assumptions affect this engineering example?');
    await clickable(page,'[data-ai-submit]');
    await layout(page,result,'AI-entry');await capture(page,result,'AI-entry');
    await page.locator('[data-ai-close]').click();
    result.checks.push({name:'AI mentor entry, mode selector and question control',status:'PASS',inference:'Not invoked; no model downloads'});
    assert.equal(courseRequests(result.requests).length,1,'Language and workshop navigation must reuse target course');
    assert.equal(resourceRequests(result.requests).length,1,'Language and workshop navigation must reuse target resources');
    result.fetchStreams=await page.evaluate(()=>window.__MG_BROWSER_QA_STREAMS__||[]);
    assert.equal(result.pageErrors.length,0,JSON.stringify(result.pageErrors));
    // A plain static export intentionally has no billing API. Preserve its
    // exact 404 (and cancellation of that unread 404 body) in the report.
    const isBilling=url=>!file&&url===origin+'/api/billing/config';
    const billing404=result.failedResources.some(row=>isBilling(row.url)&&row.status===404);
    result.expectedResourceFailures=result.failedResources.filter(row=>isBilling(row.url)&&(row.status===404||(billing404&&row.error==='net::ERR_ABORTED'))).map(row=>({...row,reason:'Expected absence of optional billing API on a static export'}));
    const completedPayloads=new Map([index.courses.b296,index.resources.b296].map(d=>[origin+'/'+d.file,d]));
    result.postReadCancellations=result.failedResources.flatMap(row=>{
      const d=completedPayloads.get(row.url),read=result.fetchStreams.find(r=>r.url===row.url);
      if(file||row.error!=='net::ERR_ABORTED'||!d||read?.status!==200||!read.eof||read.signalAborted||read.declaredBytes!==d.byteLength||read.readBytes!==d.byteLength)return [];
      return [{...row,classification:'Chromium cancellation event after a fully consumed and application-verified target payload',readEvidence:read,expectedSha256:d.sha256,applicationChecksumEvidence:'The unchanged curriculum loader verifies exact bytes and SHA-256 before returning; b296 course, 40 step IDs, workshop and resources rendered successfully in this scenario.'}];
    });
    const classified=[...result.expectedResourceFailures,...result.postReadCancellations];
    const unexpected=result.failedResources.filter(row=>!classified.some(known=>known.url===row.url&&known.status===row.status&&known.error===row.error));
    result.unexpectedResourceFailures=unexpected;
    assert.equal(unexpected.length,0,JSON.stringify(unexpected));
    assert.equal(result.blockedExternal.length,0,'Unexpected external request attempted: '+result.blockedExternal.join(', '));
    result.status=result.postReadCancellations.length?'PASS_WITH_TRANSPORT_DIAGNOSTIC':'PASS';
  }catch(error){
    result.status='FAIL';result.error=error.stack||String(error);
    try{await capture(page,result,'FAIL');}catch{}
  }finally{releaseIndex();if(!result.fetchStreams)try{result.fetchStreams=await page.evaluate(()=>window.__MG_BROWSER_QA_STREAMS__||[]);}catch{}await context.close();}
  console.log(JSON.stringify({scenario:id,status:result.status,checks:result.checks.length,error:result.error?.split('\n')[0]}));
}
try{
  const entry=process.env.MACGYVER_PLAYWRIGHT_MODULE;
  const playwright=await import(entry?(entry.startsWith('file:')?entry:pathToFileURL(path.resolve(entry)).href):'playwright');
  fs.mkdirSync(screenDir,{recursive:true});
  await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
  const origin='http://127.0.0.1:'+server.address().port;
  browser=await playwright.chromium.launch({headless:true,args:['--no-sandbox','--disable-background-networking','--disable-component-update','--disable-default-apps','--disable-sync','--no-first-run']});
  report.browser={engine:'Chromium',version:browser.version(),headless:true,playwrightModule:entry||'playwright',deviceMethod:'Playwright viewport/touch/mobile emulation; not physical hardware'};
  const configurations=[
    {id:'desktop',viewport:{width:1440,height:960}},
    {id:'mobile',viewport:{width:390,height:844},isMobile:true,hasTouch:true},
    {id:'tablet',viewport:{width:768,height:1024},isMobile:true,hasTouch:true},
    {id:'file-desktop',viewport:{width:1440,height:960},file:true}
  ];
  const selected=process.env.MACGYVER_BROWSER_SCENARIOS?.split(',').filter(Boolean)||configurations.map(v=>v.id);
  assert(selected.length&&selected.every(id=>configurations.some(v=>v.id===id)),'Unknown browser scenario');
  report.requestedScenarios=selected;
  for(const config of configurations.filter(v=>selected.includes(v.id)))await scenario(config,origin);
}catch(error){report.fatalErrors.push(error.stack||String(error));}
finally{
  if(browser)await browser.close();
  await new Promise(resolve=>server.close(resolve));
  report.finishedAt=new Date().toISOString();
  const passed=report.scenarios.length===(report.requestedScenarios?.length||4)&&report.scenarios.every(s=>['PASS','PASS_WITH_TRANSPORT_DIAGNOSTIC'].includes(s.status))&&!report.fatalErrors.length;
  report.status=passed?(report.scenarios.some(s=>s.status==='PASS_WITH_TRANSPORT_DIAGNOSTIC')?'PASS_WITH_TRANSPORT_DIAGNOSTIC':'PASS'):'FAIL';
  report.diagnosticPathsScope='Absolute scratch screenshot and diagnostics paths describe this run; only bundledScreenshots are guaranteed to be included in the deliverable.';
  report.bundledScreenshots=[];
  for(const [id,name,description] of [['desktop','home-zh','1440×960 desktop home'],['mobile','workshop-zh-TW','390×844 mobile workshop'],['tablet','workshop-en','768×1024 tablet English workshop']]){
    const scenario=report.scenarios.find(s=>s.id===id),shot=report.screenshots.find(s=>s.scenario===id&&s.name===name);
    if(!scenario?.status.startsWith('PASS')||!shot)continue;
    const relative=`docs/qa-v15/${id}-${name}.png`,destination=path.join(root,relative);
    fs.mkdirSync(path.dirname(destination),{recursive:true});fs.copyFileSync(shot.path,destination);
    report.bundledScreenshots.push({path:relative,description,sha256:sha(destination),horizontalOverflowPx:0});
  }
  if(report.status==='PASS_WITH_TRANSPORT_DIAGNOSTIC')report.limitations.push('Raw Chromium cancellation events after fully consumed, application-verified payloads are retained. This result does not claim zero network warnings.');
  fs.mkdirSync(path.dirname(reportFile),{recursive:true});fs.writeFileSync(reportFile,JSON.stringify(report,null,2)+'\n');
  console.log(JSON.stringify({status:report.status,scenarios:report.scenarios.length,report:reportFile,screenshots:report.screenshots.length,fatalErrors:report.fatalErrors}));
  process.exitCode=passed?0:1;
}
