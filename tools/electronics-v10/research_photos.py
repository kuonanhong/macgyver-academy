import urllib.request,urllib.parse,json,concurrent.futures,time
from pathlib import Path
BASE=Path(__file__).resolve().parent/'media-research'
queries=['silicon ingot','semiconductor dicing tape','wire bonding','optical fiber coupler','atomic force microscope','wafer cleaning','physical vapor deposition','sputtering target','scanning electron microscopy semiconductor','ceramic chip package','thermal cycling chamber','printed circuit board manufacturing','power transformer generator','photonic crystal silicon','laser diode wafer','electroplating copper']
def fetch(q):
 p=BASE/('search-'+q.replace(' ','-')+'.json')
 if p.exists():return q,json.loads(p.read_text())
 u='https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode({'action':'query','format':'json','generator':'search','gsrsearch':q,'gsrnamespace':6,'gsrlimit':12,'prop':'imageinfo','iiprop':'url|extmetadata','iiurlwidth':960})
 try:
  r=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=45);d=json.load(r);p.write_text(json.dumps(d,ensure_ascii=False,indent=2));return q,d
 except Exception as e:return q,{'error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:
 for q,d in ex.map(fetch,queries):
  print('\nQUERY',q,flush=True)
  for p in d.get('query',{}).get('pages',{}).values():
   i=p.get('imageinfo',[{}])[0];em=i.get('extmetadata',{});print(p['title'],em.get('LicenseShortName',{}).get('value'),flush=True)
  if 'error'in d:print(d,flush=True)
