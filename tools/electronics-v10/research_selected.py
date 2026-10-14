import urllib.request,urllib.parse,json,re,html,time
from pathlib import Path
P=Path(__file__).resolve().parent/'media-research'
files=['Monocrystalline silicon ingot.jpg','Rounded Silicon Carbide Ingot (cropped).jpg','Gold wire for wire bonding.JPG','TF78 60 - Wire bonding.jpg','A semiconductor wafer on a dicing (blue) tape. Few chips (dies) from the wafer have already been picked up (removed) for further manufacturing.png','Atomic Force Microscope 1.jpg','AFM-Raman-TERS.jpg','Physical Vapor Deposition (PVD).jpg','FHR Target.jpg','DCplasmaSputtering.jpg','Gold Target in XPS Spectrometer.jpg','Titanium target with oxide film.jpg','MC6847 Ceramic Package.png','BeamLeadedChipcompliantBonded to goldpattern0001.jpg','Chipbond bipolartr.jpg','Chip bond wire.jpg','Optical-fiber-coupler-FC-APC 1.jpg','Fiberoptic Transmitter Module.jpg','Optical fiber in protective coating that transports a Laser beam - Laser Physics Lab - NTNU-NT.jpg','Partially etched silicon dioxide via Nomarski DIC.jpg','GaP-wafer.jpg','Buharlastirilmis tungsten2.jpg','CompliantBondingAGold wire0001.jpg','Connecting a laser & optical fibres to an optical communications system testbed.jpg','FiberCoupler.JPG','QCPM8893 02.jpg','QCPM8893 03.jpg','NatSem NS32332U 15 1.jpg','Cetko pvd 2624.jpg','Silicon single crystal.jpg','Ultrasonic wedge bonding.webm']
allpages={}
for p in P.glob('search-*.json'):
 d=json.loads(p.read_text())
 for v in d.get('query',{}).get('pages',{}).values():allpages[v['title']]=v
missing=['File:'+f for f in files if 'File:'+f not in allpages]
for j in range(0,len(missing),8):
 u='https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode({'action':'query','format':'json','titles':'|'.join(missing[j:j+8]),'prop':'imageinfo','iiprop':'url|extmetadata','iiurlwidth':960})
 try:
  r=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=50);d=json.load(r);(P/f'exact-{j}.json').write_text(json.dumps(d,ensure_ascii=False,indent=2))
  for v in d.get('query',{}).get('pages',{}).values():allpages[v['title']]=v
 except Exception as e:print('ERROR',str(e),flush=True)
selected=[allpages['File:'+f] for f in files if 'File:'+f in allpages]
(P/'selected.json').write_text(json.dumps(selected,ensure_ascii=False,indent=2))
for v in selected:
 i=v.get('imageinfo',[{}])[0];e=i.get('extmetadata',{});clean=lambda x:html.unescape(re.sub('<[^>]+>','',x));print(v['title'],e.get('LicenseShortName',{}).get('value'),'AUTHOR',clean(e.get('Artist',{}).get('value','')),'DESC',clean(e.get('ImageDescription',{}).get('value',''))[:500],flush=True)
