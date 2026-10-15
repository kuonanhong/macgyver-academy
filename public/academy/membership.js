/* Payment UI never collects card details or grants its own entitlements.
 * V12: regional prices (pricing.js), first-section-free policy (paywall.js),
 * PayPal / card and ECPay checkout via the owner's Supabase Edge Functions
 * (checkout.js), plus the original self-hosted Python ECPay flow. */
import { loadPricing, plans as pricingPlans, priceTable, selectedCurrency, setCurrency, availableCurrencies, chargeCurrency, formatMoney, convertTwd, pricingState, fxAgeDays, detectCountry } from './pricing.js';
import { accessState, refreshAccess, freeStageCount, courseAccessSummary } from './paywall.js';
import { checkoutAvailability, mountPayPalButtons, startEcpay, submitSignedForm, TERMS_VERSION } from './checkout.js';
const escapeHTML = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const draftPlans = [{id:'all-30',title:'30 天學習通行證',titleEn:'30-day learning pass',amountTwd:299,durationDays:30},{id:'all-365',title:'365 天學習通行證',titleEn:'365-day learning pass',amountTwd:2490,durationDays:365}];
let config = {mode:'disabled',protected:false,checkoutAvailable:false,freeCourseIds:[],plans:draftPlans};
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
  const table=priceTable(selectedCurrency().currency,zh?'zh-TW':undefined);
  return courseAccessSummary(course,{zh,priceText:table[0]?.display||''});
}
function localeTag(zh){return zh?'zh-TW':(globalThis.document?.documentElement?.lang||undefined);}
export function membershipMarkup({zh=true,user=null}={}){
  const e=escapeHTML, pick=(z,en)=>zh?z:en;
  const access=accessState(), avail=checkoutAvailability({billing:config});
  const chosen=selectedCurrency(), cur=chosen.currency, locale=localeTag(zh), table=priceTable(cur,locale), {fx}=pricingState();
  const where=detectCountry();
  const credit=/exchangerate-api|open\.er-api/i.test(fx.source||'')?` · <a href="https://www.exchangerate-api.com" target="_blank" rel="noopener">Rates By Exchange Rate API</a>`:'';
  const tidy=`<span>${pick('價格以新台幣定價，乘以最新匯率換算，並無條件進位到當地慣用價位。','Prices are set in TWD, converted at the latest exchange rate and rounded up to a tidy local price.')}</span> `;
  const fxNote=fx.status==='approximate-seed'||!fx.updatedAt?pick('匯率為近似種子值，尚未取得最新匯率；結帳金額以伺服器報價為準。','Exchange rates are an approximate seed until the latest rates are fetched; the server quote at checkout is authoritative.'):`${tidy}<span>${pick('匯率更新日期：','Exchange rates updated:')}</span> <span data-no-translate>${new Date(fx.updatedAt).toLocaleDateString(locale)} · ${e(String(fx.source||'').replace(/\s*[—-]\s*Rates By Exchange Rate API/i,''))}${credit}</span> <span>${pick('結帳金額以伺服器報價為準。','The server quote at checkout is authoritative.')}</span>`;
  const anyCheckout=avail.paypal||avail.ecpay||avail.server;
  const notice=access.mode==='owner-preview'?pick('擁有者離線預覽：此版本顯示全部課程內容。公開網站上，每門課只有第一節免費，其餘需學習通行證。','Owner offline preview: all content is visible here. On the public site only the first section of each course is free.'):
    !anyCheckout?pick('線上付款尚未由站長啟用。每門課第一節可免費試學；啟用付款後即可購買通行證解鎖全部階段。','Online payment has not been enabled by the site owner yet. The first section of every course is free; once payment is enabled, a pass unlocks all stages.'):
    (avail.sandbox&&avail.paypal)||config.mode==='sandbox'?pick('付款沙盒模式：只會建立測試付款與測試權限。','Payment sandbox: test payments and test access only.'):
    pick('刷卡與 PayPal 由金流商的安全頁面處理並完成驗證（含 3-D Secure）；本站不接觸完整卡號或安全碼。','Card and PayPal payments are processed and verified (including 3-D Secure) on the provider’s secure pages; this site never sees full card numbers or security codes.');
  const options=availableCurrencies().map(c=>`<option value="${e(c)}" ${c===cur?'selected':''}>${e(c)}</option>`).join('');
  const status=access.active?pick('你的學習通行證有效','Your learning pass is active')+(access.expiresAt?` · ${pick('到期','expires')} ${new Date(access.expiresAt).toLocaleDateString(locale)}`:''):pick('目前沒有有效通行證','No active pass');
  const paidLabel=pick('付款方式','Payment method');
  return `<div class="page-lead"><div><span class="page-number">MEMBERSHIP · LEARNING PASSES</span><h1>${pick('為下一個工程，繼續學習。','Keep learning for your next engineering challenge.')}</h1><p>${pick('每門逐步課程的第一節免費試學；喜歡再選擇學習期間，解鎖全部課程與階段。','The first section of every guided course is free. Choose a learning period to unlock every course and stage.')}</p></div></div>
<div class="notice ${anyCheckout&&!avail.sandbox?'':'warn'}">${notice}</div>
<section class="currency-bar task-card"><div><strong>${pick('顯示幣別','Display currency')}</strong><p class="subtext">${pick('依你的語系與時區推測地區','Region inferred from your time zone / language')}<span data-no-translate>：${e(where.country)} · ${e(chosen.basis==='manual'?pick('手動選擇','manual choice'):where.zone||where.basis)}</span></p></div><label class="sr-only" for="currencySelect">${pick('幣別','Currency')}</label><select id="currencySelect" data-no-translate>${options}</select><button class="text-link" id="currencyAuto">${pick('依所在地自動','Use my region')}</button><p class="subtext fx-note">${fxNote}</p></section>
<div class="membership-plans">
<article class="membership-plan"><span class="eyebrow">START EXPLORING</span><h2>${pick('免費試學','Free trial')}</h2><strong class="plan-price">${e(formatMoney(0,cur,locale))}</strong><p>${pick(`每門逐步課程的第${freeStageCount()===1?'一':' '+freeStageCount()+' '}節（第一階段）免費，包含師傅示範、互動工作台與驗收。`,`The first ${freeStageCount()===1?'section':freeStageCount()+' sections'} (stage) of every guided course is free, including mentor demonstrations, the interactive workbench and checks.`)}</p><ul><li>${pick('所有課程皆可試學第一節','Try the first section of every course')}</li><li>${pick('第二節起需學習通行證','From the second section on, a learning pass is needed')}</li><li>${pick('可先註冊帳號保存進度','Register to keep your progress')}</li></ul></article>
${table.map(p=>{const charge=chargeCurrency('paypal',cur),chargeAmount=convertTwd(p.amountTwd,charge);return `<article class="membership-plan" data-plan-card="${e(p.id)}"><span class="eyebrow">ENGINEERING PASS</span><h2>${e(pick(p.title,p.titleEn||p.title))}</h2><strong class="plan-price" data-no-translate>${e(p.display)}</strong><p class="subtext"><span data-no-translate>${cur==='TWD'?'':`≈ ${e(p.twdDisplay)} · `}</span>${pick(`${e(p.durationDays)} 天`,`${e(p.durationDays)} days`)}</p><p>${pick('全部已展開的逐步課程與階段','All authored guided courses and stages')}</p><ul><li>${pick('各帳號獨立保存進度、跨裝置同步','Progress per account, synced across devices')}</li><li>${pick('課程驗收完成後申領平台證書','Platform certificate after course checks')}</li><li>${pick('一次付款，不自動續扣','One payment; no automatic renewal')}</li>${charge!==cur&&avail.paypal?`<li>${pick('PayPal 以','PayPal charges in')} ${e(charge)} ${pick('結帳','')} (${e(formatMoney(chargeAmount,charge,locale))})</li>`:''}</ul><button class="button" data-buy-plan="${e(p.id)}" ${anyCheckout?'':'disabled'}>${anyCheckout?pick('選擇此方案','Choose this plan'):pick('付款尚未開放','Checkout not yet available')}</button></article>`}).join('')}
</div>
<section class="task-card checkout-panel" id="checkoutPanel" hidden><h2>${pick('結帳','Checkout')} · <span id="checkoutPlanName"></span></h2><p>${pick('目前身分：','Signed in as: ')}<strong data-no-translate>${e(user?.name||pick('尚未登入','Not signed in'))}</strong></p><label class="terms-check"><input id="billingTerms" type="checkbox">${pick('我已閱讀此商戶的服務、隱私與退費條款，了解通行證期限及不自動續扣。','I have read this merchant’s service, privacy and refund terms, and understand the access period and no automatic renewal.')}</label><div class="billing-legal-links">${Object.entries(config.legalUrls||{terms:config.termsUrl||'commerce-terms.html',privacy:'commerce-terms.html#privacy',refund:'commerce-terms.html#refund'}).map(([key,url])=>[key,safeLegalURL(url)]).filter(([,url])=>url).map(([key,url])=>`<a href="${e(url)}" target="_blank" rel="noopener">${e(({terms:pick('服務條款','Terms'),privacy:pick('隱私說明','Privacy'),refund:pick('退款說明','Refunds')})[key]||key)} ↗</a>`).join(' · ')}</div><fieldset class="pay-methods"><legend>${paidLabel}</legend>${avail.paypal?`<div class="pay-method"><h3>PayPal ${pick('或信用卡／金融卡','or credit / debit card')}</h3><p class="subtext">${pick('由 PayPal 安全頁面處理卡號與驗證；可不註冊 PayPal 直接刷卡（依地區提供）。','PayPal’s secure pages handle card data and verification; guest card payment is available in supported regions.')}</p><div id="paypalButtons" class="paypal-buttons"></div></div>`:''}${avail.ecpay?`<div class="pay-method"><h3>${pick('綠界 ECPay 信用卡（新台幣）','ECPay credit card (TWD)')}</h3><p class="subtext">${pick('前往綠界安全付款頁，完成 3-D 驗證後自動開通。','Pay on ECPay’s secure page; access opens after 3-D Secure verification.')}</p><button class="button light" id="ecpayButton">${pick('前往綠界付款','Pay with ECPay')}</button></div>`:''}${avail.server?`<div class="pay-method"><h3>${pick('本站付款（綠界）','Site checkout (ECPay)')}</h3><button class="button light" id="serverCheckout">${pick('建立安全付款單','Create secure checkout')}</button></div>`:''}</fieldset><p id="billingStatus" role="status" aria-live="polite"></p></section>
<section class="task-card mt"><h2>${pick('我的通行證、訂單與證書','My passes, orders and certificates')}</h2><p><strong>${e(status)}</strong></p><button class="button light" id="refreshMembership">${pick('重新取得會員狀態','Refresh membership status')}</button><div id="membershipRecords" class="mt"></div></section>
<details class="task-card mt"><summary>${pick('付款與撥款說明（站長）','Payments and payouts (site owner)')}</summary><p>${pick('信用卡與 PayPal 款項先由金流商驗證並入帳到商家帳戶，再依商家後台設定撥款到站長的本人金融帳戶（例如郵局帳戶）。網站程式不保存、也不顯示任何收款帳號。設定方式見套件 docs/PAYMENTS_V12_ZH.md。','Card and PayPal payments are verified and settled to the merchant account by the provider, then paid out to the owner’s own bank account (for example a post-office account) as configured in the provider dashboard. The website never stores or displays payout account numbers. See docs/PAYMENTS_V12_ZH.md.')}</p></details>`;
}
export function certificateMarkup(course,zh=true){
  return `<div class="certificate-action"><button class="button light" data-certificate="${escapeHTML(course.id)}">${zh?'申領本課完成證書':'Request course completion certificate'}</button><span>${zh?'需完成全部伺服器驗收；離線／展示模式不發驗證證書。':'Requires all server-recorded checks; offline/demo mode does not issue verified certificates.'}</span><label class="terms-check"><input type="checkbox" data-publish-certificate-name>${zh?'我同意在公開證書驗證頁顯示我的帳號姓名（選填）':'I consent to show my account name on the public certificate verification page (optional).'}</label><div data-certificate-result role="status"></div></div>`;
}
function trustedCheckout(result){
  const allowed=config.mode==='live'?'https://payment.ecpay.com.tw/Cashier/AioCheckOut/V5':'https://payment-stage.ecpay.com.tw/Cashier/AioCheckOut/V5';
  if(!config.checkoutAvailable||result?.action!==allowed||!result.fields||typeof result.fields!=='object'||Array.isArray(result.fields))throw new Error('Unexpected checkout destination.');
  return allowed;
}
export function bindMembership(root,{zh=true,user=null,catalog=[],onLogin=()=>{},onAccessChanged=()=>{}}={}){
  const pick=(a,b)=>zh?a:b, e=escapeHTML;
  const status=message=>{const node=root.querySelector('#billingStatus');if(node)node.textContent=message;};
  const panel=root.querySelector('#checkoutPanel');
  let disposePayPal=null, planId='';
  const rerender=()=>{try{globalThis.dispatchEvent(new Event('hashchange'));}catch{}};
  const currency=root.querySelector('#currencySelect');
  if(currency)currency.onchange=()=>{setCurrency(currency.value);rerender();};
  const auto=root.querySelector('#currencyAuto');
  if(auto)auto.onclick=()=>{setCurrency('');rerender();};
  const termsOk=()=>{if(root.querySelector('#billingTerms')?.checked)return true;status(pick('請先閱讀並勾選商戶條款。','Read and accept the merchant terms first.'));return false;};
  const paid=async result=>{status(pick('付款完成並已驗證，通行證已開通。','Payment verified; your pass is active.')+(result?.expiresAt?` ${pick('到期：','Expires: ')}${new Date(result.expiresAt).toLocaleDateString(zh?'zh-TW':undefined)}`:''));await refreshAccess({user});onAccessChanged();};
  const mountPayPal=async()=>{
    const box=root.querySelector('#paypalButtons');if(!box)return;
    disposePayPal?.();disposePayPal=null;
    if(!root.querySelector('#billingTerms')?.checked){box.innerHTML=`<p class="subtext">${pick('勾選條款後顯示付款按鈕。','Accept the terms to show the payment buttons.')}</p>`;return;}
    const cur=chargeCurrency('paypal',selectedCurrency().currency);
    try{disposePayPal=await mountPayPalButtons(box,{planId,currency:cur,zh,onPaid:paid,onStatus:status});}catch(error){status(error.message);}
  };
  root.querySelectorAll('[data-buy-plan]').forEach(button=>button.onclick=()=>{
    if(!user){status('');onLogin();return;}
    planId=button.dataset.buyPlan;
    const plan=pricingPlans().find(p=>p.id===planId);
    if(panel){panel.hidden=false;const name=panel.querySelector('#checkoutPlanName');if(name)name.textContent=plan?(zh?plan.title:plan.titleEn):planId;panel.scrollIntoView?.({behavior:'smooth',block:'start'});}
    mountPayPal();
  });
  const terms=root.querySelector('#billingTerms');
  if(terms)terms.onchange=()=>mountPayPal();
  const ecpay=root.querySelector('#ecpayButton');
  if(ecpay)ecpay.onclick=async()=>{if(!user){onLogin();return;}if(!termsOk())return;ecpay.disabled=true;status(pick('正在建立綠界付款單…','Preparing the ECPay checkout…'));try{await startEcpay({planId,zh});}catch(error){status(error.message);ecpay.disabled=false;}};
  const server=root.querySelector('#serverCheckout');
  if(server)server.onclick=async()=>{
    if(!user){onLogin();return;}if(!termsOk())return;
    server.disabled=true;status(pick('正在建立安全付款單…','Preparing secure checkout…'));
    try{
      const requestId=server.dataset.requestId||(server.dataset.requestId=crypto.randomUUID().replaceAll('-',''));
      const result=await request('/api/billing/checkout',{planId,termsAccepted:true,termsVersion:config.termsVersion||'v10-2026-10',requestId,expectedUserId:user.id});
      if(owner!==user.id)throw new Error('The learning account changed. Please retry.');
      trustedCheckout(result);submitSignedForm(result,zh);
    }catch(error){status(error.message);server.disabled=false;}
  };
  const refresh=root.querySelector('#refreshMembership');
  if(refresh)refresh.onclick=async()=>{
    const target=root.querySelector('#membershipRecords');
    if(!user){onLogin();return;}
    refresh.disabled=true;
    try{
      const access=await refreshAccess({user});onAccessChanged();
      if(!config.protected){
        const cloud=globalThis.MacGyverCloud;let orders=[];
        if(cloud?.configured&&cloud.myOrders){try{const rows=await cloud.myOrders();orders=Array.isArray(rows)?rows:[];}catch{}}
        target.innerHTML=`<h3>${pick('通行證','Passes')}</h3><p>${access.active?pick('有效','Active')+(access.expiresAt?' · '+e(new Date(access.expiresAt).toLocaleString(zh?'zh-TW':undefined)):''):pick('尚無有效通行證','No active pass')}</p><h3>${pick('付款記錄','Payment records')}</h3><ul>${orders.map(x=>`<li data-no-translate>${e(x.id||'')} · ${e(x.plan_id||'')} · ${e(x.currency||'')} ${e(x.amount??'')} · ${e(x.provider||'')} · ${e(x.status||'')} · ${e(x.created_at?new Date(x.created_at).toLocaleString(zh?'zh-TW':undefined):'')}</li>`).join('')||`<li>${pick('尚無訂單','No orders')}</li>`}</ul>`;
        return;
      }
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
/** After ECPay redirects back (?payment=ecpay&order=MG…), poll the server until verified. */
export async function resumeEcpayReturn({zh=true,user=null,onDone=()=>{},onStatus=()=>{}}={}){
  if(typeof URLSearchParams!=='function')return null;
  const params=new URLSearchParams(globalThis.location?.search||'');
  const orderId=params.get('order');
  if(params.get('payment')!=='ecpay'||!/^MG[0-9A-F]{18}$/.test(orderId||''))return null;
  const cloud=globalThis.MacGyverCloud;if(!cloud?.callFunction||!user)return null;
  const pick=(a,b)=>zh?a:b;
  for(let i=0;i<24;i++){
    try{
      const result=await cloud.callFunction('checkout-capture',{orderId});
      if(result?.status==='paid'){onStatus(pick('綠界付款已驗證，通行證已開通。','ECPay payment verified; your pass is active.'));await refreshAccess({user});onDone(result);history.replaceState?.(null,'',location.pathname+location.hash);return result;}
    }catch(error){if(!/pending/i.test(String(error.message))){onStatus(String(error.message));return null;}}
    onStatus(pick('正在等待綠界付款通知與伺服器查核…','Waiting for ECPay’s notification and server verification…'));
    await new Promise(r=>setTimeout(r,5000));
  }
  onStatus(pick('尚未收到付款確認；稍後可在「我的通行證」重新整理。','Payment not confirmed yet; refresh “My passes” later.'));
  return null;
}
export { loadPricing };
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
