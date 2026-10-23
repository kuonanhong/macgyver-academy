const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const url=v=>typeof v==='string'&&/^https:\/\//.test(v)?v:'';
let registry={vendors:[],courses:[]},loading=null;
export function setVendors(data){registry={vendors:Array.isArray(data?.vendors)?data.vendors:[],courses:Array.isArray(data?.courses)?data.courses:[]};}
export async function loadVendors(){
 if(loading)return loading;
 loading=(async()=>{try{const data=globalThis.window?.MG_DATA?.vendors||await fetch('data/vendors.json',{signal:AbortSignal.timeout(12000)}).then(r=>{if(!r.ok)throw Error('Vendor data unavailable');return r.json();});if(Array.isArray(data?.vendors)&&Array.isArray(data?.courses))registry=data;}catch{}return registry;})();return loading;
}
let markets={quotes:{}},marketsLoading=null;
export async function loadMarkets(){
 if(marketsLoading)return marketsLoading;
 marketsLoading=(async()=>{try{const data=globalThis.window?.MG_DATA?.markets||await fetch('data/markets.json',{cache:'no-cache',signal:AbortSignal.timeout(12000)}).then(r=>{if(!r.ok)throw Error('Market snapshot unavailable');return r.json();});if(data&&typeof data.quotes==='object')markets=data;}catch{}return markets;})();return marketsLoading;
}
const TV={NASDAQ:'NASDAQ',NYSE:'NYSE',NYSEAMERICAN:'AMEX',TWSE:'TWSE',TPEx:'TPEX',TSE:'TSE',LSE:'LSE',XETRA:'XETR',ETR:'XETR',EPA:'EURONEXT',EURONEXT:'EURONEXT',AMS:'EURONEXT',EBR:'EURONEXT',SIX:'SIX',KRX:'KRX',KOSDAQ:'KRX',HKEX:'HKEX',SSE:'SSE',SZSE:'SZSE',STO:'OMXSTO',CPH:'OMXCOP',HEL:'OMXHEX',OSL:'OSL',MIL:'MIL',BIT:'MIL',BME:'BME',TSX:'TSX',ASX:'ASX',NSE:'NSE'};
export function tradingViewSymbol(security){if(!security?.symbol||!security?.exchange)return '';const sym=['STO','CPH','HEL'].includes(security.exchange)?String(security.symbol).replace(/-/g,'_'):String(security.symbol);return (TV[security.exchange]||security.exchange)+':'+sym;}
const signed=(v,locale)=>typeof v==='number'&&Number.isFinite(v)?`<span class="${v>0?'up':v<0?'down':''}">${v>0?'+':''}${new Intl.NumberFormat(locale,{maximumFractionDigits:2}).format(v)}%</span>`:'<span>—</span>';
export function sparklineSvg(values=[],{width=160,height=40,label=''}={}){
 const v=values.filter(x=>typeof x==='number'&&Number.isFinite(x));if(v.length<2)return '';
 const min=Math.min(...v),max=Math.max(...v),span=max-min||1,step=width/(v.length-1);
 const pts=v.map((x,i)=>`${(i*step).toFixed(1)},${(height-2-(x-min)/span*(height-4)).toFixed(1)}`).join(' ');
 const up=v[v.length-1]>=v[0];
 return `<svg class="sparkline ${up?'up':'down'}" viewBox="0 0 ${width} ${height}" width="${width}" height="${height}" role="img" aria-label="${esc(label)}"><polyline fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round" stroke-linecap="round" points="${pts}"/></svg>`;
}
export function snapshotMarkup(vendor,{zh=true}={}){
 const pick=(a,b)=>zh?a:b,q=markets.quotes?.[vendor.id],locale=zh?'zh-TW':undefined;
 if(!q||!(q.price>0))return `<p class="subtext">${pick('尚無每週行情快照；請執行每週更新或開啟即時走勢。','No weekly snapshot yet; run the weekly update or open the live chart.')}</p>`;
 const money=new Intl.NumberFormat(locale,{maximumFractionDigits:q.price<10?3:2}).format(q.price);
 return `<div class="market-snapshot" data-no-translate><div class="market-head"><strong class="quote-price">${esc(q.currency||vendor.security?.currency||'')} ${esc(money)}</strong>${sparklineSvg(q.spark,{label:pick('近一年週收盤走勢','One-year weekly closing trend')})}</div><dl class="market-changes"><div><dt>1D</dt><dd>${signed(q.changePct1d,locale)}</dd></div><div><dt>1W</dt><dd>${signed(q.changePct1w,locale)}</dd></div><div><dt>1M</dt><dd>${signed(q.changePct1m,locale)}</dd></div><div><dt>YTD</dt><dd>${signed(q.changePctYtd,locale)}</dd></div><div><dt>1Y</dt><dd>${signed(q.changePct1y,locale)}</dd></div></dl>${q.high52?`<p class="subtext">${pick('52 週區間','52-week range')} ${esc(new Intl.NumberFormat(locale).format(q.low52))} – ${esc(new Intl.NumberFormat(locale).format(q.high52))}</p>`:''}<p class="subtext">${pick('收盤日','Close date')} ${esc(q.asOf||'')} · ${esc(q.source||'')}${q.stale?pick(' · 本週更新失敗，顯示上週資料',' · update failed this week; previous data shown'):''}</p>${q.nameMismatch?`<p class="notice warn">${pick('交易所登記名稱與本公司不一致，代號待站長核對：','The exchange lists a different company name; the ticker awaits review:')} <span data-no-translate>${esc(q.listedName||'')}</span></p>`:''}</div>`;
}
export function vendorsMarkup(course,{zh=true}={}){
 const pick=(a,b)=>zh?a:b,association=registry.courses.find(c=>c.courseId===course.id);
 if(!association)return `<div data-vendors-slot="${esc(course.id)}"></div>`;
 const vendors=association.vendorIds.map(id=>registry.vendors.find(v=>v.id===id)).filter(Boolean).sort((a,b)=>(b.security?1:0)-(a.security?1:0));
 const updated=markets.updatedAt?new Date(markets.updatedAt).toLocaleDateString(zh?'zh-TW':undefined):'';
 return `<section class="vendor-section task-card" data-vendors-slot="${esc(course.id)}"><span class="task-label">INDUSTRY · COMPANIES · STOCK PERFORMANCE</span><h3>${pick('從課程走進產業：相關廠商與股價表現','From course to industry: related companies and stock performance')}</h3><p>${esc(pick(association.connection,association.connectionEn))}</p><div class="vendor-cards">${vendors.map(v=>{const role=association.roles?.find(r=>r.vendorId===v.id),tv=tradingViewSymbol(v.security);return `<article class="vendor-card"><div class="vendor-title"><h4>${esc(pick(v.name,v.nameEn))}</h4>${v.security?`<span class="vendor-security" data-no-translate>${esc(v.security.exchange)}: ${esc(v.security.symbol)}</span>${v.security.parent?`<span class="vendor-parent subtext">${pick('由母公司上市：','Listed via parent:')} <span data-no-translate>${esc(pick(v.security.parent,v.security.parentEn||v.security.parent))}</span></span>`:''}`:`<span class="vendor-security muted">${pick(v.entityType==='technical-source-publisher'?'技術資料來源':'未提供股票資料',v.entityType==='technical-source-publisher'?'Technical source publisher':'Stock data not provided')}</span>`}</div><p>${esc(pick(role?.business||v.business,role?.businessEn||v.businessEn))}</p>${role?.role?`<p class="subtext"><strong>${pick('與本課的關係','Relation to this course')}</strong> · ${esc(pick(role.role,role.roleEn))}</p>`:''}<div class="vendor-links"><a href="${esc(url(role?.productUrl)||url(v.url))}" target="_blank" rel="noopener">${pick('官方業務介紹','Official business overview')} ↗</a>${url(v.investorUrl)?`<a href="${esc(url(v.investorUrl))}" target="_blank" rel="noopener">${pick('投資人關係','Investor relations')} ↗</a>`:''}${tv?`<a href="https://www.tradingview.com/symbols/${esc(tv.replace(':','-'))}/" target="_blank" rel="noopener">TradingView ↗</a>`:''}</div>${v.security?`${snapshotMarkup(v,{zh})}<div class="vendor-actions"><button class="button light" data-live-chart="${esc(tv)}">${pick('載入即時走勢圖','Load live chart')}</button>${globalThis.MG_STATIC_MODE===true?'':`<button class="text-link" data-quote-vendor="${esc(v.id)}">${pick('伺服器報價','Server quote')}</button>`}</div><div class="live-chart" data-live-chart-slot="${esc(tv)}"></div><div class="quote-output" data-quote-output="${esc(v.id)}" role="status"></div>`:''}</article>`;}).join('')}</div><p class="subtext">${pick(`股價為每週更新的延遲快照${updated?`（最近更新 ${esc(updated)}）`:''}；「載入即時走勢圖」會在你點擊後連線 TradingView 顯示交易所的即時或延遲報價。行情僅供產業觀察，不構成投資建議，也不代表廠商與本課程有合作關係。`,`Prices are a weekly delayed snapshot${updated?` (last updated ${esc(updated)})`:''}; “Load live chart” connects to TradingView after you click and shows real-time or delayed exchange quotes. Market data supports industry context only — not investment advice, and no partnership with the course is implied.`)}</p></section>`;
}
export function quoteMarkup(data,zh=true){
 const pick=(a,b)=>zh?a:b;
 if(data?.status!=='ok')return `<p>${data?.status==='unconfigured'?pick('行情服務尚未設定；請使用上方官方投資人資訊。','Market data is not configured; use the official investor link above.'):pick('目前無法核對行情；請稍後重試或開啟官方資訊。','The quote could not be verified. Retry later or open official information.')}</p>`;
 if(!Number.isFinite(data.price)||data.price<=0)return `<p>${pick('行情數值無效。','Invalid quote value.')}</p>`;
 const numeric=v=>typeof v==='number'&&Number.isFinite(v),fmt=v=>new Intl.NumberFormat(zh?'zh-TW':'en',{maximumFractionDigits:4}).format(v);
 const asof=String(data.asOf||''),stamp=new Date(data.retrievedAt),retrieved=Number.isFinite(stamp.getTime())?stamp.toLocaleString(zh?'zh-TW':'en'):data.retrievedAt;
 return `<div data-no-translate><strong class="quote-price">${esc(data.currency)} ${esc(fmt(data.price))}</strong><span class="quote-change">${numeric(data.change)?(data.change>=0?'+':'')+esc(fmt(data.change)):'—'} ${numeric(data.changePercent)?'('+esc(fmt(data.changePercent))+'%)':''}</span></div><dl class="quote-meta"><dt>${pick('交易／報價時間','Trading / quote time')}</dt><dd data-no-translate>${esc(asof)} · ${esc(data.timeZone||'')}</dd><dt>${pick('取得時間','Retrieved')}</dt><dd data-no-translate>${esc(retrieved)}</dd><dt>${pick('資料頻率','Frequency')}</dt><dd>${data.frequency==='end-of-day'?pick('每日盤後','End of day'):pick('依供應商授權行情；最多快取 60 秒','Licensed provider feed; cached for up to 60 seconds')}</dd></dl><a href="${esc(url(data.sourceUrl))}" target="_blank" rel="noopener">${esc(data.source||'')} ↗</a>${url(data.licenseUrl)?` · <a href="${esc(url(data.licenseUrl))}" target="_blank" rel="noopener">${pick('資料授權','Data license')} ↗</a>`:''}`;
}
/* Official TradingView embed code, isolated in a sandboxed srcdoc frame (opaque
 * origin: the widget cannot read this site's storage or cookies). Loaded only
 * after the learner clicks. */
export function liveChartMarkup(symbol,{zh=true,dark=false}={}){
 if(!/^[A-Z]{2,10}:[A-Z0-9_.-]{1,15}$/.test(symbol||''))return '';
 const config=JSON.stringify({symbol,width:'100%',height:220,locale:zh?'zh_TW':'en',dateRange:'12M',colorTheme:dark?'dark':'light',isTransparent:true,autosize:true,largeChartUrl:'',noTimeScale:false}).replace(/</g,'\\u003c');
 return `<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>html,body{margin:0;background:transparent}</style></head><body><div class="tradingview-widget-container"><div class="tradingview-widget-container__widget"></div><script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-mini-symbol-overview.js" async>${config}</script></div></body></html>`;
}
export function bindVendors(root,{zh=true,onRendered=()=>{}}={}){
 root.querySelectorAll('[data-live-chart]').forEach(button=>button.onclick=()=>{
  const symbol=button.dataset.liveChart,slot=button.closest('.vendor-card')?.querySelector('[data-live-chart-slot]');if(!slot)return;
  const src=liveChartMarkup(symbol,{zh,dark:document.documentElement.dataset.theme==='dark'});if(!src){slot.textContent=zh?'此代號無法顯示即時走勢。':'No live chart for this symbol.';return;}
  const frame=document.createElement('iframe');frame.srcdoc=src;frame.title=(zh?'即時走勢：':'Live chart: ')+symbol;frame.loading='lazy';frame.referrerPolicy='no-referrer-when-downgrade';frame.setAttribute('sandbox','allow-scripts allow-popups allow-popups-to-escape-sandbox');frame.style.cssText='width:100%;height:230px;border:0';
  const credit=document.createElement('p');credit.className='subtext';credit.innerHTML='<a href="https://www.tradingview.com/" target="_blank" rel="noopener">'+(zh?'行情圖表由 TradingView 提供 ↗':'Chart by TradingView ↗')+'</a>';
  slot.replaceChildren(frame,credit);button.disabled=true;onRendered();
 });
 root.querySelectorAll('[data-quote-vendor]').forEach(button=>button.onclick=async()=>{
  const output=button.parentElement.querySelector('[data-quote-output]');button.disabled=true;output.textContent=zh?'正在查詢…':'Fetching…';
  try{if(globalThis.location?.protocol==='file:')throw Error('offline');const r=await fetch('/api/markets?vendor='+encodeURIComponent(button.dataset.quoteVendor),{credentials:'same-origin',cache:'no-store',signal:AbortSignal.timeout(15000)});if(!r.ok)throw Error('source');const data=await r.json();if(!output.isConnected)return;output.innerHTML=quoteMarkup(data,zh);onRendered();}
  catch{output.textContent=zh?'此環境尚未提供行情 API 或資料服務暫時不可用；請開啟官方投資人連結。':'This environment has no quote API or the source is unavailable. Open the official investor link.';}finally{button.disabled=false;}
 });
}
