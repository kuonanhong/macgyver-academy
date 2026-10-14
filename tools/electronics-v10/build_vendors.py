#!/usr/bin/env python3
"""Curated supplier/product links; a learning association is not an endorsement or a supply contract."""
import json,hashlib
from pathlib import Path
from urllib.parse import urlparse
ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'public/academy/data'
def read(p):return json.loads(p.read_text())
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
# Descriptions paraphrase the linked primary product pages; no images reused.
rows=[
('tsmc','台積電','TSMC','晶圓代工、先進製程與 3DFabric 異質整合。','Foundry manufacturing, process platforms and 3DFabric heterogeneous integration.','https://www.tsmc.com/english','https://investor.tsmc.com/english','2330','TWSE','TWD'),
('ase','日月光投控／日月光半導體','ASE Technology Holding / ASE','封裝測試、2.5D/3D 整合及光電共封裝服務。','Assembly and test, 2.5D/3D integration and optical co-packaging services.','https://ase.aseglobal.com/silicon-photonics/','https://www.aseglobal.com/','3711','TWSE','TWD'),
('asml','艾司摩爾','ASML','EUV、DUV 微影與圖案化量測系統。','EUV and DUV lithography and patterning metrology systems.','https://www.asml.com/en/products','https://www.asml.com/en/investors','ASML','NASDAQ','USD'),
('amat','應用材料','Applied Materials','薄膜沉積、材料移除、改質與製程分析設備。','Equipment for film deposition, material removal, modification and process analysis.','https://www.appliedmaterials.com/us/en/semiconductor/products.html','https://investor.appliedmaterials.com/','AMAT','NASDAQ','USD'),
('lam','科林研發','Lam Research','半導體沉積、蝕刻、去膠清洗及封裝製程設備。','Semiconductor deposition, etch, strip, clean and packaging process equipment.','https://www.lamresearch.com/products/','https://investor.lamresearch.com/','LRCX','NASDAQ','USD'),
('kla','科磊','KLA','晶圓與封裝量測、缺陷檢測及製程控制。','Wafer and package metrology, defect inspection and process control.','https://www.kla.com/products','https://ir.kla.com/','KLAC','NASDAQ','USD'),
('amkor','艾克爾','Amkor Technology','晶圓級、倒裝及先進系統封裝與測試。','Wafer-level, flip-chip and advanced system packaging and test.','https://amkor.com/technology/','https://ir.amkor.com/','AMKR','NASDAQ','USD'),
('intel','英特爾','Intel','晶片、先進封裝與積體矽光子光學互連。','Chips, advanced packaging and integrated silicon-photonic optical interconnects.','https://www.intel.com/content/www/us/en/products/details/network-io/silicon-photonics.html','https://www.intc.com/','INTC','NASDAQ','USD'),
('ti','德州儀器','Texas Instruments','類比、電源管理、感測與嵌入式控制元件。','Analog, power-management, sensing and embedded-control components.','https://www.ti.com/product-category/power-management/overview.html','https://investor.ti.com/','TXN','NASDAQ','USD'),
('adi','亞德諾','Analog Devices','精密類比、資料轉換與訊號鏈元件。','Precision analog, data-conversion and signal-chain components.','https://www.analog.com/en/product-category.html','https://investor.analog.com/','ADI','NASDAQ','USD'),
('entegris','英特格','Entegris','高純材料、微污染控制、流體輸送及 CMP 相關材料。','High-purity materials, contamination control, fluid delivery and CMP materials.','https://www.entegris.com/en/home/our-science/by-industry/microelectronics/semiconductor.html','https://investor.entegris.com/','ENTG','NASDAQ','USD'),
('coherent','高意','Coherent','光通訊雷射、光收發器與相關光電元件。','Optical-communication lasers, transceivers and related photonic components.','https://www.coherent.com/networking/photonlink','https://investor.coherent.com/','COHR','NYSE','USD'),
('cadence','益華電腦','Cadence','多晶粒規劃、封裝共同設計與電熱分析工具。','Multi-die planning, package co-design and electrical/thermal analysis tools.','https://www.cadence.com/en_US/home/solutions/3dic-design-solutions.html','https://investor.cadence.com/','CDNS','NASDAQ','USD'),
('sumco','勝高','SUMCO','半導體用拋光、磊晶及其他矽晶圓。','Polished, epitaxial and other silicon wafers for semiconductor manufacturing.','https://www.sumcosi.com/english/products/','https://www.sumcosi.com/english/ir/','3436','TSE','JPY'),
('shinetsu','信越化學','Shin-Etsu Chemical','光阻及其他半導體電子材料。','Photoresists and other semiconductor electronic materials.','https://www.shinetsu.co.jp/en/products/electronics-materials/photoresist/','https://www.shinetsu.co.jp/en/ir/','4063','TSE','JPY'),
('evg','EV Group','EV Group','晶圓接合、暫時接合、微影與對位設備。','Wafer bonding, temporary bonding, lithography and alignment equipment.','https://www.evgroup.com/products/','https://www.evgroup.com/','','',''),
]
vendors=[]
for id,z,en,desc,descen,url,ir,ticker,exchange,currency in rows:
 vendors.append(dict(id=id,name=z,nameEn=en,business=desc,businessEn=descen,url=url,investorUrl=ir,sourceUrl=url,reviewed='2026-10-14',security=dict(symbol=ticker,exchange=exchange,currency=currency) if ticker else None))
by={v['id']:v for v in vendors};hints={}
for name in 'abc':
 p=ROOT/f'tools/electronics-v10/group_{name}.json'
 if p.exists():
  for c in read(p)['courses']:hints[c['id']]=c.get('vendorHints',[])
hints.update(read(ROOT/'tools/electronics-v10/other-vendor-hints.json'))
associations=[]
for c in read(DATA/'featured.json'):
 cat=c['category'];sub=c.get('subcategory','');ids=[];extra=[]
 if cat=='semiconductor':
  ids={'substrate':['sumco','entegris'],'lithography':['asml','shinetsu'],'fab':['entegris','kla'],'feol':['amat','lam'],'etch':['lam','amat'],'deposition':['amat','lam'],'interconnect':['amat','lam'],'metrology':['kla','amat'],'compound':['amat','kla'],'mems':['evg','kla'],'sensors':['tsmc','kla'],'memory':['lam','amat']}.get(sub,['tsmc','amat'])
 elif cat=='packaging':
  ids={'pkg-integration':['ase','tsmc'],'pkg-joining':['evg','amat'],'pkg-handling':['evg','entegris'],'pkg-encapsulation':['ase','amkor'],'pkg-vias':['lam','amat'],'pkg-substrates':['amkor','cadence'],'pkg-electrical':['cadence','tsmc'],'pkg-thermal':['amkor','cadence'],'pkg-reliability':['kla','amkor'],'pkg-passive':['intel','coherent'],'pkg-active':['intel','coherent'],'pkg-sources':['coherent','evg'],'pkg-circuits':['intel','coherent'],'pkg-sensing':['coherent','kla'],'pkg-verification':['kla','coherent'],'pkg-systems':['ase','intel'],'pkg-platforms':['tsmc','intel']}.get(sub,['ase','amkor'])
  if c['id'] in ['a196','a197']:ids=['tsmc','cadence']
  if c['id'] in ['a198','a199']:ids=['intel','cadence']
 elif c['id'] in hints:
  for h in hints.get(c['id'],[]):
   url=h.get('url') or h.get('website') or h.get('sourceUrl')
   if not isinstance(url,str) or not url.startswith('https://'):continue
   domain=urlparse(url).netloc.removeprefix('www.')
   match=next((v['id'] for v in vendors if domain==urlparse(v['url']).netloc.removeprefix('www.') or domain.endswith('.'+urlparse(v['url']).netloc.removeprefix('www.'))),None)
   if match:ids.append(match);extra.append({'vendorId':match,'role':h.get('role',''),'roleEn':h.get('roleEn',''),'productUrl':url})
   else:
    id='official-'+hashlib.sha256((h.get('nameEn') or h.get('name') or domain).encode()).hexdigest()[:12]
    if id not in by:
     v=dict(id=id,name=h.get('name') or domain,nameEn=h.get('nameEn') or h.get('name') or domain,business=h.get('role','官方產品與技術資料入口。'),businessEn=h.get('roleEn','Official product and technical reference.'),url=url,investorUrl='',sourceUrl=url,reviewed='2026-10-14',security=None)
     vendors.append(v);by[id]=v
    ids.append(id);extra.append({'vendorId':id,'role':h.get('role',''),'roleEn':h.get('roleEn',''),'productUrl':url})
  assert ids, f'Missing authored vendor hints for {c["id"]}'
 if ids:
  associations.append({'courseId':c['id'],'vendorIds':list(dict.fromkeys(ids)),'roles':extra,'connection':f'從 {c["title"]} 的材料、設備、設計或驗證問題，延伸查閱以下官方產品資料；這是教材關聯，不表示採用、合作或唯一供應商。','connectionEn':f'Explore official material, equipment, design or verification references related to {c["titleEn"]}. This learning association does not assert adoption, partnership or an exclusive supplier.'})
for item in read(ROOT/'tools/electronics-v10/listed-vendor-overrides.json'):
 assert item['vendorId'] in by and item['investorUrl'].startswith('https://')
 vendor=by[item['vendorId']];vendor['investorUrl']=item['investorUrl'];vendor['marketSourceUrl']=item['sourceUrl'];vendor['marketReviewed']=item['reviewed']
 if item.get('security'):
  security=item['security'];assert security['exchange'] in ('NYSE','NASDAQ') and security['currency']=='USD' and security['symbol'].isalnum()
  vendor['security']=security
assert {r['courseId'] for r in associations}=={c['id'] for c in read(DATA/'featured.json')}, 'Every guided course needs an industry association'
write(DATA/'vendors.json',{'version':10,'reviewed':'2026-10-14','vendors':vendors,'courses':associations})
# Only explicitly curated instruments are quotable; no arbitrary external symbols/URLs.
issuers={v['id']:{**v['security'],'name':v['nameEn'],'investorUrl':v['investorUrl']} for v in vendors if v['security']}
write(ROOT/'lib/market-issuers.json',issuers)
print(f'Vendors: {len(vendors)}; course associations: {len(associations)}; curated listed instruments: {len(issuers)}')
