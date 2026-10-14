/* Fixed issuer allowlist is supplied by the caller. No user-controlled URLs. */
const TWSE='https://openapi.twse.com.tw/v1/exchangeReport/STOCK_DAY_ALL';
const cache=new Map(),pending=new Map();
export function numberOrNull(value){if(value===null||value===undefined||String(value).trim()==='')return null;const n=Number(String(value).replaceAll(',','').replaceAll('−','-'));return Number.isFinite(n)?n:null;}
export function tradingDate(value){
 const s=String(value||'').replaceAll('/','').replaceAll('-','');
 if(!/^\d{7,8}$/.test(s))return null;
 const year=Number(s.slice(0,-4))+(s.length===7?1911:0),month=Number(s.slice(-4,-2)),day=Number(s.slice(-2));
 const d=new Date(Date.UTC(year,month-1,day));
 if(year<1900||year>2200||d.getUTCFullYear()!==year||d.getUTCMonth()+1!==month||d.getUTCDate()!==day)return null;
 return d.toISOString().slice(0,10);
}
export function normalizeTWSE(row,issuer,retrievedAt){
 const price=numberOrNull(row?.ClosingPrice),change=numberOrNull(row?.Change),date=tradingDate(row?.Date);
 if(String(row?.Code)!==issuer.symbol||price===null||price<=0||!date)throw new Error('Invalid TWSE instrument or quote.');
 const previous=change===null?null:price-change;
 return {status:'ok',price,change,changePercent:previous&&previous>0?change/previous*100:null,currency:'TWD',symbol:issuer.symbol,exchange:'TWSE',asOf:date,timeZone:'Asia/Taipei',retrievedAt,frequency:'end-of-day',source:'TWSE OpenAPI',sourceUrl:TWSE,licenseUrl:'https://data.gov.tw/license',isRealtime:false};
}
export function normalizeTwelve(row,issuer,retrievedAt){
 const price=numberOrNull(row?.close),timestamp=Number(row?.timestamp),currency=row?.currency;
 if(row?.status==='error'||row?.symbol!==issuer.symbol||String(row?.exchange||'').toUpperCase()!==issuer.exchange.toUpperCase()||price===null||price<=0||currency!==issuer.currency||!Number.isFinite(timestamp)||timestamp<946684800)throw new Error('Invalid quote or instrument identity.');
 return {status:'ok',price,change:numberOrNull(row.change),changePercent:numberOrNull(row.percent_change),currency,symbol:issuer.symbol,exchange:issuer.exchange,asOf:new Date(timestamp*1000).toISOString(),timeZone:row.exchange_timezone||'UTC',retrievedAt,frequency:'provider-feed',source:'Twelve Data',sourceUrl:'https://twelvedata.com/',isRealtime:false,delayNotice:'Feed timing and coverage depend on the licensed provider subscription; server cache is at most 60 seconds.'};
}
async function getJSON(url,fetcher){
 const r=await fetcher(url,{signal:AbortSignal.timeout(10000),redirect:'error',headers:{Accept:'application/json'}});
 if(!r.ok)throw new Error('Market source unavailable.');
 if(Number(r.headers.get('content-length')||0)>4000000)throw new Error('Market response too large.');
 const reader=r.body?.getReader();let raw='';
 if(reader){const decoder=new TextDecoder();let length=0;try{while(true){const {done,value}=await reader.read();if(done)break;length+=value.byteLength;if(length>4000000){await reader.cancel();throw new Error('Market response too large.');}raw+=decoder.decode(value,{stream:true});}raw+=decoder.decode();}finally{reader.releaseLock();}}
 else {raw=await r.text();if(raw.length>4000000)throw new Error('Market response too large.');}
 return JSON.parse(raw);
}
async function cached(key,ttl,action,clock){
 const item=cache.get(key);if(item&&clock()-item.at<ttl)return {...item.value,cached:true};
 if(pending.has(key))return pending.get(key);
 const work=action().then(value=>{cache.set(key,{at:clock(),value});return value;}).finally(()=>pending.delete(key));pending.set(key,work);return work;
}
/** @param {string} id
 * @param {{issuers:Record<string,{symbol:string,exchange:string,currency:string,investorUrl:string}>,config?:{apiKey?:string,licenseAcknowledged?:boolean},fetcher?:typeof fetch,clock?:()=>number}} options */
export async function marketQuote(id,{issuers,config={},fetcher=fetch,clock=Date.now}){
 const issuer=issuers[id];if(!issuer)throw Object.assign(new Error('Unknown listed company.'),{status:400});
 const now=()=>new Date(clock()).toISOString();
 const failed=cache.get('failed:'+id);if(failed&&clock()-failed.at<30000)return {...failed.value,cached:true};
 try{
  if(issuer.exchange==='TWSE'){
   const data=await cached('twse',900000,async()=>({rows:await getJSON(TWSE,fetcher),retrievedAt:now()}),clock);
   if(!Array.isArray(data.rows))throw new Error('Invalid TWSE response.');
   const row=data.rows.find(x=>x.Code===issuer.symbol);
   return {...normalizeTWSE(row,issuer,data.retrievedAt),cached:!!data.cached};
  }
  if(!config.apiKey||config.licenseAcknowledged!==true)return {status:'unconfigured',symbol:issuer.symbol,exchange:issuer.exchange,currency:issuer.currency,source:'Twelve Data',investorUrl:issuer.investorUrl,reason:'A licensed market-data plan and server-only API key must be configured. No price is fabricated.'};
  return await cached('twelve:'+id,60000,async()=>{
   const url=new URL('https://api.twelvedata.com/quote');url.searchParams.set('symbol',issuer.symbol);url.searchParams.set('exchange',issuer.exchange);url.searchParams.set('apikey',config.apiKey);
   return normalizeTwelve(await getJSON(url.href,fetcher),issuer,now());
  },clock);
 }catch{const value={status:'unavailable',symbol:issuer.symbol,exchange:issuer.exchange,currency:issuer.currency,retrievedAt:now(),investorUrl:issuer.investorUrl,reason:'The market source could not be verified. Retry or open official investor information.'};cache.set('failed:'+id,{at:clock(),value});return value;}
}
