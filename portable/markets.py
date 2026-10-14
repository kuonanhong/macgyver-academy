"""Read-only quotes from fixed, licensed sources. Keys never enter responses."""
import datetime,json,math,os,threading,time,urllib.parse,urllib.request
from pathlib import Path
ISSUERS=json.loads((Path(__file__).resolve().parents[1]/'lib/market-issuers.json').read_text())
TWSE='https://openapi.twse.com.tw/v1/exchangeReport/STOCK_DAY_ALL'
_cache={};_lock=threading.Lock()
def number(v):
 try:
  if v is None or str(v).strip()=='':return None
  n=float(str(v).replace(',','').replace('−','-'));return n if math.isfinite(n) else None
 except (ValueError,TypeError):return None
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def get_json(url):
 class NoRedirect(urllib.request.HTTPRedirectHandler):
  def redirect_request(self,*args,**kwargs):return None
 with urllib.request.build_opener(NoRedirect()).open(urllib.request.Request(url,headers={'Accept':'application/json'}),timeout=10) as r:
  data=r.read(4000001)
  if len(data)>4000000:raise ValueError('Response too large')
  return json.loads(data)
def quote(ident):
 if ident not in ISSUERS:raise ValueError('Unknown listed company')
 issuer=ISSUERS[ident];symbol=issuer['symbol'];exchange=issuer['exchange'];base={'symbol':symbol,'exchange':exchange,'currency':issuer['currency'],'investorUrl':issuer['investorUrl']}
 key='twse' if exchange=='TWSE' else ident;ttl=900 if exchange=='TWSE' else 60
 if exchange!='TWSE' and not(os.environ.get('MARKET_DATA_API_KEY') and os.environ.get('MARKET_DATA_LICENSE_ACK')=='true'):return dict(base,status='unconfigured',reason='Configure a licensed data plan and server-only API key. No price is fabricated.')
 try:
  with _lock:
   cached=_cache.get(key);hit=bool(cached and time.monotonic()-cached[0]<ttl)
   if hit:data,stamp=cached[1:]
   else:
    url=TWSE if exchange=='TWSE' else 'https://api.twelvedata.com/quote?'+urllib.parse.urlencode({'symbol':symbol,'exchange':exchange,'apikey':os.environ['MARKET_DATA_API_KEY']})
    data=get_json(url);stamp=now();_cache[key]=(time.monotonic(),data,stamp)
  if exchange=='TWSE':
   row=next(r for r in data if r['Code']==symbol);raw=str(row['Date']).replace('/','').replace('-','');year=int(raw[:-4]);year=year+1911 if len(raw)==7 else year
   date=datetime.date(year,int(raw[-4:-2]),int(raw[-2:])).isoformat();price=number(row['ClosingPrice']);change=number(row['Change']);previous=price-change if price is not None and change is not None else None
   if price is None or price<=0:raise ValueError('Invalid price')
   return dict(base,status='ok',price=price,change=change,changePercent=change/previous*100 if previous and previous>0 else None,asOf=date,timeZone='Asia/Taipei',retrievedAt=stamp,frequency='end-of-day',source='TWSE OpenAPI',sourceUrl=TWSE,licenseUrl='https://data.gov.tw/license',isRealtime=False,cached=hit)
  price=number(data.get('close'));timestamp=number(data.get('timestamp'))
  if data.get('symbol')!=symbol or str(data.get('exchange','')).upper()!=exchange.upper() or data.get('currency')!=issuer['currency'] or price is None or price<=0 or timestamp is None or timestamp<946684800:raise ValueError('Invalid instrument')
  return dict(base,status='ok',price=price,change=number(data.get('change')),changePercent=number(data.get('percent_change')),asOf=datetime.datetime.fromtimestamp(timestamp,datetime.timezone.utc).isoformat(),timeZone=data.get('exchange_timezone','UTC'),retrievedAt=stamp,frequency='provider-feed',source='Twelve Data',sourceUrl='https://twelvedata.com/',isRealtime=False,cached=hit,delayNotice='Timing and coverage depend on licensed feed; cache at most 60 seconds.')
 except Exception:return dict(base,status='unavailable',retrievedAt=now(),reason='Market source could not be verified. Retry or open investor information.')
