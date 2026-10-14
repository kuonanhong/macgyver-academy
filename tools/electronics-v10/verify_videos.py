import urllib.request,urllib.parse,json,concurrent.futures
from pathlib import Path
P=Path(__file__).resolve().parent/'media-research'
ids=['4G8wXQGEBrA','pk7yLLw3zAU','YhbUOq5oaes','VSX-tFSwCtE','CAKWkOuoWrs','_T-mh72VRIY','ykfong1WNU8']
def f(v):
 p=P/('video-'+v+'.json')
 try:
  url='https://www.youtube.com/oembed?'+urllib.parse.urlencode({'url':'https://www.youtube.com/watch?v='+v,'format':'json'})
  d=json.load(urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=45));p.write_text(json.dumps(d,ensure_ascii=False,indent=2));return v,d.get('title'),d.get('author_name'),d.get('html','')[:140]
 except Exception as e:return v,str(e)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
 for x in ex.map(f,ids):print(x,flush=True)
