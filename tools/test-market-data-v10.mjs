import assert from 'node:assert/strict';
import {numberOrNull,tradingDate,normalizeTWSE,normalizeTwelve,marketQuote} from '../lib/market-core.mjs';
import {quoteMarkup} from '../public/academy/vendors.js';
const issuer={symbol:'2330',exchange:'TWSE',currency:'TWD',investorUrl:'https://investor.tsmc.com/english'};
assert.equal(numberOrNull(''),null);assert.equal(numberOrNull('--'),null);assert.equal(numberOrNull('1,200.5'),1200.5);assert.equal(numberOrNull('Infinity'),null);
assert.equal(tradingDate('1151013'),'2026-10-13');assert.equal(tradingDate('2026-10-13'),'2026-10-13');assert.equal(tradingDate('20269999'),null);assert.equal(tradingDate('20260229'),null);assert.equal(tradingDate('20240229'),'2024-02-29');
const row={Code:'2330',Date:'1151013',ClosingPrice:'100',Change:'-5'},stamp='2026-10-14T01:00:00Z';
const q=normalizeTWSE(row,issuer,stamp);assert.equal(q.price,100);assert.equal(q.change,-5);assert(Math.abs(q.changePercent-(-5/105*100))<1e-10);assert.equal(q.isRealtime,false);assert.equal(q.frequency,'end-of-day');
assert.throws(()=>normalizeTWSE({...row,Code:'3711'},issuer,stamp));assert.throws(()=>normalizeTWSE({...row,ClosingPrice:'--'},issuer,stamp));
const us={symbol:'TXN',currency:'USD',exchange:'NASDAQ'};const feed={symbol:'TXN',currency:'USD',exchange:'NASDAQ',timestamp:1791936000,close:'100.25',change:'0.25',percent_change:'0.25'};
assert.equal(normalizeTwelve(feed,us,stamp).price,100.25);assert.throws(()=>normalizeTwelve({...feed,exchange:'NYSE'},us,stamp));assert.throws(()=>normalizeTwelve({...feed,currency:'JPY'},us,stamp));
let calls=0;const issuers={tsmc:issuer,ti:us};const mock=async()=>{calls++;return new Response(JSON.stringify([row]));};
assert.equal((await marketQuote('tsmc',{issuers,fetcher:mock})).status,'ok');assert.equal((await marketQuote('tsmc',{issuers,fetcher:mock})).cached,true);assert.equal(calls,1);
assert.equal((await marketQuote('ti',{issuers,config:{apiKey:'private-example-key',licenseAcknowledged:false},fetcher:()=>{throw Error('must not call')}})).status,'unconfigured');
await assert.rejects(marketQuote('https://localhost/private',{issuers,fetcher:mock}),/Unknown/);
let failures=0;const fail=async()=>{failures++;throw Error('private-example-key');};const failed=await marketQuote('ti',{issuers,config:{apiKey:'private-example-key',licenseAcknowledged:true},fetcher:fail});assert.equal(failed.status,'unavailable');assert(!JSON.stringify(failed).includes('private-example-key'));await marketQuote('ti',{issuers,config:{apiKey:'private-example-key',licenseAcknowledged:true},fetcher:fail});assert.equal(failures,1);
for(const zh of [true,false]){const html=quoteMarkup(q,zh);assert(html.includes('2026-10-13'));assert(!html.includes('NaN'));assert(!quoteMarkup({...q,source:'<script>x</script>'},zh).includes('<script>'));}
console.log('Market data PASS: instrument identity, exchange/currency, dates, signed daily change, no fabricated prices, license gate, fixed sources, bounded cache, negative backoff and escaping.');
