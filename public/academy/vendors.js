const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const url=v=>typeof v==='string'&&/^https:\/\//.test(v)?v:'';
let registry={vendors:[],courses:[]},loading=null;
export async function loadVendors(){
 if(loading)return loading;
 loading=(async()=>{try{const data=globalThis.window?.MG_DATA?.vendors||await fetch('data/vendors.json',{signal:AbortSignal.timeout(12000)}).then(r=>{if(!r.ok)throw Error('Vendor data unavailable');return r.json();});if(Array.isArray(data?.vendors)&&Array.isArray(data?.courses))registry=data;}catch{}return registry;})();return loading;
}
export function vendorsMarkup(course,{zh=true}={}){
 const pick=(a,b)=>zh?a:b,association=registry.courses.find(c=>c.courseId===course.id);
 if(!association)return `<div data-vendors-slot="${esc(course.id)}"></div>`;
 const vendors=association.vendorIds.map(id=>registry.vendors.find(v=>v.id===id)).filter(Boolean);
 return `<section class="vendor-section task-card" data-vendors-slot="${esc(course.id)}"><span class="task-label">INDUSTRY · PRODUCTS · MARKET DATA</span><h3>${pick('從課程走進產業','Connect the course to industry')}</h3><p>${esc(pick(association.connection,association.connectionEn))}</p><div class="vendor-cards">${vendors.map(v=>{const role=association.roles?.find(r=>r.vendorId===v.id);return `<article class="vendor-card"><h4>${esc(pick(v.name,v.nameEn))}</h4><p>${esc(pick(v.business,v.businessEn))}</p>${role?.role?`<p class="subtext">${esc(pick(role.role,role.roleEn))}</p>`:''}<div class="vendor-links"><a href="${esc(url(role?.productUrl)||url(v.url))}" target="_blank" rel="noopener">${pick('官方業務／產品','Official business / products')} ↗</a>${url(v.investorUrl)?`<a href="${esc(url(v.investorUrl))}" target="_blank" rel="noopener">${pick('投資人資訊','Investor information')} ↗</a>`:''}</div>${v.security?`<div class="vendor-security" data-no-translate>${esc(v.security.exchange)}: ${esc(v.security.symbol)} · ${esc(v.security.currency)}</div><button class="button light" data-quote-vendor="${esc(v.id)}">${pick('取得最新可用股價','Get latest available quote')}</button><div class="quote-output" data-quote-output="${esc(v.id)}" role="status">${pick('點擊時查詢；沒有預先填入股價。','Fetched on request; no prefilled price.')}</div>`:`<p class="subtext">${pick('尚未設定可核對的上市證券；請查官方公司資訊。','No verified listed instrument is configured; consult the official company information.')}</p>`}<small>${pick('業務資料核對：','Business references checked: ')}${esc(v.reviewed)}</small></article>`;}).join('')}</div><p class="subtext">${pick('台股採證交所每日盤後開放資料，不是逐筆即時行情。其他市場需管理者設定有對外顯示權限的資料服務；未連接時保留官方連結。股價僅作產業觀察，不作課程品質排名。','Taiwan quotes use TWSE daily closing open data, not a real-time tick feed. Other markets require an operator-configured data service licensed for external display; official links remain available otherwise. Quotes support industry observation, not a ranking of course quality.')}</p></section>`;
}
export function quoteMarkup(data,zh=true){
 const pick=(a,b)=>zh?a:b;
 if(data?.status!=='ok')return `<p>${data?.status==='unconfigured'?pick('行情服務尚未設定；請使用上方官方投資人資訊。','Market data is not configured; use the official investor link above.'):pick('目前無法核對行情；請稍後重試或開啟官方資訊。','The quote could not be verified. Retry later or open official information.')}</p>`;
 if(!Number.isFinite(data.price)||data.price<=0)return `<p>${pick('行情數值無效。','Invalid quote value.')}</p>`;
 const numeric=v=>typeof v==='number'&&Number.isFinite(v),fmt=v=>new Intl.NumberFormat(zh?'zh-TW':'en',{maximumFractionDigits:4}).format(v);
 const asof=String(data.asOf||''),stamp=new Date(data.retrievedAt),retrieved=Number.isFinite(stamp.getTime())?stamp.toLocaleString(zh?'zh-TW':'en'):data.retrievedAt;
 return `<div data-no-translate><strong class="quote-price">${esc(data.currency)} ${esc(fmt(data.price))}</strong><span class="quote-change">${numeric(data.change)?(data.change>=0?'+':'')+esc(fmt(data.change)):'—'} ${numeric(data.changePercent)?'('+esc(fmt(data.changePercent))+'%)':''}</span></div><dl class="quote-meta"><dt>${pick('交易／報價時間','Trading / quote time')}</dt><dd data-no-translate>${esc(asof)} · ${esc(data.timeZone||'')}</dd><dt>${pick('取得時間','Retrieved')}</dt><dd data-no-translate>${esc(retrieved)}</dd><dt>${pick('資料頻率','Frequency')}</dt><dd>${data.frequency==='end-of-day'?pick('每日盤後','End of day'):pick('依供應商授權行情；最多快取 60 秒','Licensed provider feed; cached for up to 60 seconds')}</dd></dl><a href="${esc(url(data.sourceUrl))}" target="_blank" rel="noopener">${esc(data.source||'')} ↗</a>${url(data.licenseUrl)?` · <a href="${esc(url(data.licenseUrl))}" target="_blank" rel="noopener">${pick('資料授權','Data license')} ↗</a>`:''}`;
}
export function bindVendors(root,{zh=true,onRendered=()=>{}}={}){
 root.querySelectorAll('[data-quote-vendor]').forEach(button=>button.onclick=async()=>{
  const output=button.parentElement.querySelector('[data-quote-output]');button.disabled=true;output.textContent=zh?'正在查詢…':'Fetching…';
  try{if(globalThis.location?.protocol==='file:')throw Error('offline');const r=await fetch('/api/markets?vendor='+encodeURIComponent(button.dataset.quoteVendor),{credentials:'same-origin',cache:'no-store',signal:AbortSignal.timeout(15000)});if(!r.ok)throw Error('source');const data=await r.json();if(!output.isConnected)return;output.innerHTML=quoteMarkup(data,zh);onRendered();}
  catch{output.textContent=zh?'此環境尚未提供行情 API 或資料服務暫時不可用；請開啟官方投資人連結。':'This environment has no quote API or the source is unavailable. Open the official investor link.';}finally{button.disabled=false;}
 });
}
