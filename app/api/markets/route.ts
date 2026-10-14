import { env } from 'cloudflare:workers';
import { json } from '@/lib/backend';
import issuers from '@/lib/market-issuers.json';
import { marketQuote } from '@/lib/market-core.mjs';
export const dynamic = 'force-dynamic';
export async function GET(request:Request){
 const id=new URL(request.url).searchParams.get('vendor')||'';
 if(!Object.prototype.hasOwnProperty.call(issuers,id))return json({error:'Unknown listed company.'},400);
 const vars=env as unknown as Record<string,string|undefined>;
 const quote=await marketQuote(id,{issuers,config:{apiKey:vars.MARKET_DATA_API_KEY,licenseAcknowledged:vars.MARKET_DATA_LICENSE_ACK==='true'}});
 return json(quote);
}
