import urllib.request,json,concurrent.futures,re,hashlib,io
from pathlib import Path
from PIL import Image
P=Path(__file__).resolve().parent/'media-research';A=P/'downloaded';A.mkdir(exist_ok=True)
rows=[]
for f in ['selected.json','selected-more.json']:
 if (P/f).exists():rows+=json.loads((P/f).read_text())
SKIP=['.webm','Cetko pvd','Buharlastirilmis','DCplasma','QCPM8893 03','NatSem','Silicon single crystal']
rows=[r for r in rows if not any(s in r['title'] for s in SKIP)]
def down(r):
 i=r.get('imageinfo',[{}])[0];name=r['title'][5:];ext=Path(name).suffix.lower();fn=hashlib.sha256(name.encode()).hexdigest()[:12]+ext;target=A/fn
 try:
  if not target.exists():
   u=i.get('thumburl',i['url']).split('?')[0];res=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=45);b=res.read(6*1024*1024+1);assert len(b)<=6*1024*1024;Image.open(io.BytesIO(b)).verify();target.write_bytes(b)
  size=Image.open(target).size;return {'title':name,'file':fn,'size':size,'sha256':hashlib.sha256(target.read_bytes()).hexdigest()}
 except Exception as e:return {'title':name,'error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
 out=[]
 for row in ex.map(down,rows):out.append(row);print(row,flush=True)
(P/'downloads.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
valid=[x for x in out if 'file'in x];w=1000;h=((len(valid)+3)//4)*210;img=Image.new('RGB',(w,h),'white');from PIL import ImageDraw
d=ImageDraw.Draw(img)
for n,v in enumerate(valid):
 im=Image.open(A/v['file']);im.thumbnail((240,170));x=(n%4)*250;y=(n//4)*210;img.paste(im,(x,y));d.text((x,y+172),str(n)+' '+v['title'][:30],fill='black');d.text((x,y+187),v['title'][30:60],fill='black')
img.save(P/'contact-sheet.jpg')
