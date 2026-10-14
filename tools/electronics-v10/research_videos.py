import urllib.request,urllib.parse,json,re,concurrent.futures
from pathlib import Path
P=Path(__file__).resolve().parent/'media-research'
pages=[('lam-moly','https://newsroom.lamresearch.com/molybdenum-metallization?blog=true'),('lam-package','https://newsroom.lamresearch.com/inside-the-chip-advanced-packaging?blog=true'),('lam-logic','https://newsroom.lamresearch.com/gate-all-around-and-logic-scaling?blog=true'),('lam-package101','https://newsroom.lamresearch.com/semi-101-advanced-packaging-techniques?blog=true'),('kla-system','https://www.kla.com/media-room/kla-technologies')]
def f(item):
 slug,url=item
 try:
  data=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=45).read().decode();ids=list(set(re.findall(r'(?:youtube(?:-nocookie)?\.com/(?:embed/|watch\?v=)|youtu\.be/)([a-zA-Z0-9_-]{11})',data)));(P/(slug+'.html')).write_text(data);return {'slug':slug,'url':url,'youtubeIds':ids}
 except Exception as e:return {'slug':slug,'error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:rows=list(ex.map(f,pages))
print(json.dumps(rows,ensure_ascii=False,indent=2));(P/'video-pages.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
