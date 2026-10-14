/* Payment UI never collects card details or grants its own entitlements. */
const escapeHTML = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const draftPlans = [{id:'all-30',title:'30 天學習通行證',titleEn:'30-day learning pass',amountTwd:299,durationDays:30},{id:'all-365',title:'365 天學習通行證',titleEn:'365-day learning pass',amountTwd:2490,durationDays:365}];
let config = {mode:'disabled',protected:false,checkoutAvailable:false,freeCourseIds:['semiconductor','packaging','a201','a242','a271','a281'],plans:draftPlans};
const evidenceCache = new Map();
let owner = null, pendingConfig = null;
export function billingState() { return config; }
export function resetLearningEvidence(nextOwner) { if(nextOwner!==owner){owner=nextOwner;evidenceCache.clear();} }
export async function loadBillingConfig({fetchImpl=globalThis.fetch,force=false}={}) {
  if(globalThis.location?.protocol==='file:')return config;
  if(pendingConfig&&!force)return pendingConfig;
  pendingConfig=(async()=>{
    try{
      const response=await fetchImpl('/api/billing/config',{credentials:'same-origin',cache:'no-store',signal:AbortSignal.timeout(12000)});
      if(!response.ok)return config;
      const data=await response.json();
      if(!['disabled','sandbox','live'].includes(data.mode)||typeof data.protected!=='boolean')throw new Error('Invalid billing configuration.');
      if(!Array.isArray(data.freeCourseIds)||data.freeCourseIds.some(id=>!(/^[a-zA-Z0-9_-]{1,100}$/).test(id)))throw new Error('Invalid free course IDs.');
      const plans=Array.isArray(data.plans)&&data.plans.length?data.plans:draftPlans;
      if(plans.some(p=>!p||typeof p.id!=='string'||!Number.isInteger(p.amountTwd)||p.amountTwd<1||!Number.isInteger(p.durationDays)||p.durationDays<1))throw new Error('Invalid billing plans.');
      config={...config,...data,plans,checkoutAvailable:data.protected&&data.mode!=='disabled'&&data.checkoutAvailable===true};
    }catch(error){if(config.protected)throw error;}
    return config;
  })();
  return pendingConfig;
}
async function request(url,body){
  const response=await fetch(url,{method:body===undefined?'GET':'POST',credentials:'same-origin',cache:'no-store',headers:body===undefined?{}:{'Content-Type':'application/json'},...(body===undefined?{}:{body:JSON.stringify(body)}),signal:AbortSignal.timeout(20000)});
  const data=await response.json().catch(()=>({error:'Invalid server response.'}));
  if(!response.ok)throw new Error(data.error||`Request failed (${response.status}).`);
  return data;
}
export async function loadVerifiedLearning(courseId){
  if(!config.protected)return null;
  const expectedOwner=owner,key=expectedOwner+':'+courseId;
  const value=await request('/api/learning/'+encodeURIComponent(courseId));
  if(owner!==expectedOwner)throw new Error('The learning account changed. Please retry.');
  evidenceCache.set(key,value);return value;
}
export async function submitVerifiedStep(courseId,stepId,answer){
  if(!config.protected)return null;
  const expectedOwner=owner,key=expectedOwner+':'+courseId,state=evidenceCache.get(key)||await loadVerifiedLearning(courseId);
  if(owner!==expectedOwner)throw new Error('The learning account changed. Please retry.');
  try{
    const result=await request('/api/learning/evidence',{courseId,revision:state.revision,stepId,answer,expectedUserId:expectedOwner});
    if(owner!==expectedOwner)throw new Error('The learning account changed. Please retry.');
    if(!result.passed)throw new Error('The server did not accept this learning check.');
    await loadVerifiedLearning(courseId);return result;
  }catch(error){evidenceCache.delete(key);throw error;}
}
export function courseAccessMarkup(course,zh=true){
  const free=config.freeCourseIds.includes(course.id), locked=course.locked===true;
  return `<div class="course-access ${locked?'locked':''}"><span>${zh?(free?'免費試學':'會員課程'):(free?'FREE COURSE':'MEMBER COURSE')}</span><p>${locked?(zh?'登入並啟用學習通行證後，即可依序完成本課工序。':'Sign in and activate a learning pass to work through this course.'):(config.protected?(zh?'學習驗收記錄由伺服器保存，可用於申領平台完成證書。':'Learning checks are recorded by the server for a platform completion certificate.'):(zh?'目前為完整教材展示／離線版，尚未啟用收費；可直接學習。':'This complete owner/demo edition has billing disabled; learning is available.'))}</p><a class="button light" href="#membership">${zh?'會員方案與證書':'Membership & certificates'} ↗</a></div>`;
}
export function membershipMarkup({zh=true,user=null}={}){
  const e=escapeHTML, pick=(z,en)=>zh?z:en;
  const notice=(!config.checkoutAvailable&&config.protected)?pick('課程權限已啟用保護；付款尚未完成設定，目前可使用免費試學或既有有效通行證。','Course access is protected, but checkout is not configured. Free courses and existing valid passes remain available.'):config.mode==='live'?pick('正式付款由綠界安全頁面處理。本站不收集完整卡號或安全碼。','Live payments are handled on ECPay’s secure page. This site does not collect full card numbers or security codes.'):config.mode==='sandbox'?pick('金流沙盒：只有測試付款與測試權限，不代表真實收款。','Payment sandbox: test payments and test access only; no real collection.'):pick('付款尚未啟用。目前可使用完整教材展示版；下列是建議試營運方案，不能在此付款。','Billing is not enabled. The complete demo is available; plans below are proposed launch pricing, with checkout disabled.');
  return `<div class="page-lead"><div><span class="page-number">MEMBERSHIP · LEARNING RECORDS</span><h1>${pick('為下一個工程，繼續學習。','Keep learning for your next engineering challenge.')}</h1><p>${pick('先試學，再選擇適合自己的學習期間。','Try a course, then choose a learning period that fits.')}</p></div></div><div class="notice ${config.mode==='live'?'':'warn'}">${notice}</div><div class="membership-plans"><article class="membership-plan"><span class="eyebrow">START EXPLORING</span><h2>${pick('免費試學','Free exploration')}</h2><strong class="plan-price">NT$0</strong><p>${pick('六門跨領域課程；正式營運時同樣可保存學習紀錄。','Six courses across disciplines, with saved learning records in the production service.')}</p><ul>${config.freeCourseIds.map(id=>`<li><a href="#project/${e(id)}" data-free-course-title="${e(id)}">${e(id)}</a></li>`).join('')}</ul></article>${config.plans.map(p=>`<article class="membership-plan"><span class="eyebrow">ENGINEERING PASS</span><h2>${e(pick(p.title,p.titleEn||p.title))}</h2><strong class="plan-price">NT$${Number(p.amountTwd).toLocaleString()}</strong><p>${e(p.durationDays)} ${pick('天 · 全部已展開逐步課程','days · all authored guided courses')}</p><ul><li>${pick('各帳號獨立保存進度','Progress saved separately per account')}</li><li>${pick('課程驗收完成後申領平台證書','Platform certificate after course checks')}</li><li>${pick('一次付款，不自動續扣','One payment; no automatic renewal')}</li></ul><button class="button" data-buy-plan="${e(p.id)}" ${!config.checkoutAvailable?'disabled':''}>${config.mode==='sandbox'?pick('前往沙盒測試','Test sandbox checkout'):pick('選擇此方案','Choose this plan')}</button></article>`).join('')}</div><section class="task-card"><h2>${pick('付款前確認','Before checkout')}</h2><p>${pick('目前身分：','Current identity: ')}<strong>${e(user?.name||pick('尚未登入','Not signed in'))}</strong></p><label class="terms-check"><input id="billingTerms" type="checkbox">${pick('我已閱讀此商戶的服務、隱私與退費條款，了解通行證期限及不自動續扣。','I have read this merchant’s service, privacy and refund terms, and understand the access period and no automatic renewal.')}</label><div class="billing-legal-links">${Object.entries(config.legalUrls||{terms:config.termsUrl||'commerce-terms.html',privacy:'commerce-terms.html#privacy',refund:'commerce-terms.html#refund'}).map(([key,url])=>[key,safeLegalURL(url)]).filter(([,url])=>url).map(([key,url])=>`<a href="${e(url)}" target="_blank" rel="noopener">${e(({terms:pick('服務條款','Terms'),privacy:pick('隱私說明','Privacy'),refund:pick('退款說明','Refunds')})[key]||key)} ↗</a>`).join(' · ')}</div><p class="subtext">${pick('正式營運者需先完成商戶審核、收款帳戶與正式條款設定；價格為待驗證的試營運假設。','The operator must complete merchant verification, settlement-account setup and final legal terms. Pricing is a launch hypothesis to validate.')}</p><p id="billingStatus" role="status" aria-live="polite"></p></section><section class="task-card mt"><h2>${pick('我的訂單、通行證與證書','My orders, passes and certificates')}</h2><button class="button light" id="refreshMembership">${pick('重新取得會員狀態','Refresh membership status')}</button><div id="membershipRecords" class="mt"></div><p class="subtext">${pick('證書記錄本平台測驗完成情形，不是學位、專業執照或實務操作能力認證。離線進度不能直接換成伺服器驗證證書。','Certificates record platform learning-check completion, not an academic degree, professional license or practical competence. Offline progress cannot directly become a server-verified certificate.')}</p></section>`;
}
export function certificateMarkup(course,zh=true){
  return `<div class="certificate-action"><button class="button light" data-certificate="${escapeHTML(course.id)}">${zh?'申領本課完成證書':'Request course completion certificate'}</button><span>${zh?'需完成全部伺服器驗收；離線／展示模式不發驗證證書。':'Requires all server-recorded checks; offline/demo mode does not issue verified certificates.'}</span><label class="terms-check"><input type="checkbox" data-publish-certificate-name>${zh?'我同意在公開證書驗證頁顯示我的帳號姓名（選填）':'I consent to show my account name on the public certificate verification page (optional).'}</label><div data-certificate-result role="status"></div></div>`;
}
function trustedCheckout(result){
  const allowed=config.mode==='live'?'https://payment.ecpay.com.tw/Cashier/AioCheckOut/V5':'https://payment-stage.ecpay.com.tw/Cashier/AioCheckOut/V5';
  if(!config.checkoutAvailable||result?.action!==allowed||!result.fields||typeof result.fields!=='object'||Array.isArray(result.fields))throw new Error('Unexpected checkout destination.');
  return allowed;
}
export function bindMembership(root,{zh=true,user=null,catalog=[],onLogin=()=>{}}={}){
  const pick=(a,b)=>zh?a:b, e=escapeHTML;
  const status=message=>{const node=root.querySelector('#billingStatus');if(node)node.textContent=message;};
  root.querySelectorAll('[data-free-course-title]').forEach(a=>{const c=catalog.find(c=>c.id===a.dataset.freeCourseTitle);if(c)a.textContent=zh?c.title:c.titleEn;});
  root.querySelectorAll('[data-buy-plan]').forEach(button=>button.onclick=async()=>{
    if(!user){onLogin();return;}
    if(!root.querySelector('#billingTerms')?.checked){status(pick('請先閱讀並勾選商戶條款。','Read and accept the merchant terms first.'));return;}
    button.disabled=true;status(pick('正在建立安全付款單…','Preparing secure checkout…'));
    try{
      const requestId=button.dataset.requestId||(button.dataset.requestId=crypto.randomUUID().replaceAll('-',''));
      const result=await request('/api/billing/checkout',{planId:button.dataset.buyPlan,termsAccepted:true,termsVersion:config.termsVersion||'v10-2026-10',requestId,expectedUserId:user.id});
      if(owner!==user.id)throw new Error('The learning account changed. Please retry.');
      const action=trustedCheckout(result),form=document.createElement('form');form.method='POST';form.action=action;
      for(const [key,value]of Object.entries(result.fields)){if(!/^[A-Z][A-Za-z0-9]{1,60}$/.test(key)||(typeof value!=='string'&&typeof value!=='number'))throw new Error('Invalid checkout field.');const input=document.createElement('input');input.type='hidden';input.name=key;input.value=String(value);form.append(input);}
      document.body.append(form);form.submit();
    }catch(error){status(error.message);button.disabled=false;}
  });
  const refresh=root.querySelector('#refreshMembership');
  if(refresh)refresh.onclick=async()=>{
    const target=root.querySelector('#membershipRecords');
    if(!config.protected){target.textContent=pick('此展示／離線版沒有啟用金流與伺服器證書。','Commerce and server certificates are disabled in this demo/offline edition.');return;}
    if(!user){onLogin();return;}
    refresh.disabled=true;
    try{
      const [data,certs]=await Promise.all([request('/api/billing/me'),request('/api/certificates')]);
      const certificates=Array.isArray(certs)?certs:certs.certificates||[];
      target.innerHTML=`<h3>${pick('通行證','Passes')}</h3><ul>${(data.entitlements||[]).map(x=>`<li>${e(x.planId||x.plan_id||pick('學習通行證','Learning pass'))} · ${e(formatBillingDate(x.expiresAt??x.expires_at,zh))} · ${e(entitlementLabel(x,zh))}</li>`).join('')||`<li>${pick('尚無有效通行證','No active pass')}</li>`}</ul><h3>${pick('付款記錄','Payment records')}</h3><ul>${(data.orders||[]).map(x=>`<li>${e(x.orderId||x.id||'')} · NT$${e(x.amountTwd||x.amount||'')} · ${e(x.status)}</li>`).join('')||`<li>${pick('尚無訂單','No orders')}</li>`}</ul><h3>${pick('完成證書','Completion certificates')}</h3><ul>${certificates.map(x=>`<li>${e(x.courseTitle||x.courseId||x.course_id)} · ${e(formatBillingDate(x.issuedAt??x.issued_at,zh))} · ${x.sandbox?'SANDBOX · ':''}${x.revoked?pick('已撤銷 · ','Revoked · '):''} · ${certificateLink(x,zh)}</li>`).join('')||`<li>${pick('尚無證書','No certificates')}</li>`}</ul>`;
    }catch(error){target.textContent=error.message;}finally{refresh.disabled=false;}
  };
  root.querySelectorAll('[data-certificate]').forEach(button=>button.onclick=async()=>{
    const output=button.parentElement.querySelector('[data-certificate-result]');
    if(!config.protected){output.textContent=pick('請在已設定的正式學習伺服器完成驗收；本版本不核發驗證證書。','Complete the checks on a configured learning server. This edition does not issue verified certificates.');return;}
    if(!user){onLogin();return;}
    button.disabled=true;
    try{const data=await request('/api/certificates',{courseId:button.dataset.certificate,publishName:button.parentElement.querySelector('[data-publish-certificate-name]')?.checked===true,expectedUserId:user.id});if(owner!==user.id)throw new Error('The learning account changed. Please retry.');output.innerHTML=certificateLink(data.certificate||data,zh);}catch(error){output.textContent=error.message;}finally{button.disabled=false;}
  });
}
function certificateLink(item,zh){
  const token=item.id||item.token||item.certificateId;
  if(!/^[a-f0-9]{40}$/.test(token||''))return escapeHTML(zh?'證書已記錄':'Certificate recorded');
  return `<a href="/api/certificates/${token}" target="_blank" rel="noopener">${zh?'開啟驗證記錄':'Open verification record'} ↗</a>`;
}

export function formatBillingDate(value,zh=true){
  const seconds=Number(value);
  if(!Number.isFinite(seconds)||seconds<=0)return '—';
  const date=new Date(seconds*1000);
  if(Number.isNaN(date.getTime()))return '—';
  return new Intl.DateTimeFormat(zh?'zh-TW':'en',{dateStyle:'medium',timeStyle:'short'}).format(date);
}
function entitlementLabel(item,zh){
  if(item.revokedAt)return zh?'已撤銷':'Revoked';
  const now=Date.now()/1000;
  if(item.expiresAt<=now)return zh?'已到期':'Expired';
  if(item.startsAt>now)return zh?'接續生效':'Scheduled renewal';
  return (item.mode==='sandbox'?'SANDBOX · ':'')+(zh?'有效':'Active');
}
export function safeLegalURL(value){
  if(typeof value!=='string'||!value||value.length>2048)return '';
  try{
    const base=new URL(globalThis.location?.href||'https://academy.example.invalid/');
    const url=new URL(value,base);
    if(url.username||url.password)return '';
    if(url.protocol==='https:'||(url.protocol==='http:'&&url.origin===base.origin))return url.href;
    if(base.protocol==='file:'&&url.protocol==='file:'&&!/^[a-zA-Z][a-zA-Z0-9+.-]*:|^\/\//.test(value)&&url.pathname.startsWith(new URL('.',base).pathname))return url.href;
  }catch{}
  return '';
}
