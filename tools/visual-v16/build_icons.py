#!/usr/bin/env python3
"""Build semantic, colorful, lazy-loadable course/category pictograms.

Geometry is selected from engineering concepts in each course, never its ID,
hash, serial number or color. Geometry-only duplicates are reported separately
from byte uniqueness. Nameplates identify related projects without pretending
that abstract pictograms are as-built drawings.
"""
from pathlib import Path
import collections, hashlib, html, json, re, sys, xml.etree.ElementTree as ET
from glyphs import GLYPHS, TERMS, CATEGORY_MAIN, TYPE_MAP

ROOT=Path(__file__).resolve().parents[2]
PUBLIC=ROOT/'public/academy'
HERE=Path(__file__).resolve().parent
PALETTES={
 'semiconductor':('#075985','#06b6d4','#f59e0b','#e0f2fe'),
 'packaging':('#6d28d9','#a78bfa','#06b6d4','#ede9fe'),
 'electronics':('#b45309','#f59e0b','#0d9488','#fef3c7'),
 'computing':('#1d4ed8','#60a5fa','#fb7185','#dbeafe'),
 'instruments':('#7e22ce','#c084fc','#14b8a6','#f3e8ff'),
 'structures':('#b91c1c','#f87171','#f59e0b','#fee2e2'),
 'underground':('#92400e','#d97706','#22c55e','#ffedd5'),
 'water':('#0369a1','#38bdf8','#14b8a6','#e0f2fe'),
 'rail':('#047857','#34d399','#f59e0b','#d1fae5'),
 'environment':('#15803d','#4ade80','#0ea5e9','#dcfce7'),
 'aerospace':('#1e40af','#93c5fd','#f97316','#eff6ff'),
 'marine':('#155e75','#22d3ee','#f59e0b','#cffafe'),
 'automotive':('#be123c','#fb7185','#2563eb','#ffe4e6'),
 'space':('#4338ca','#818cf8','#fbbf24','#e0e7ff'),
 'manufacturing':('#c2410c','#fb923c','#0891b2','#ffedd5'),
 'energy':('#a16207','#facc15','#16a34a','#fef9c3'),
 'materials':('#57534e','#a8a29e','#f97316','#f5f5f4'),
 'biomedical':('#be185d','#f472b6','#06b6d4','#fce7f3'),
 'process':('#0f766e','#2dd4bf','#f97316','#ccfbf1'),
 'megascience':('#6b21a8','#d8b4fe','#f43f5e','#faf5ff')}
NAMES={
 'semiconductor':('半導體製程','Semiconductors'),'packaging':('先進封裝與矽光子','Packaging & photonics'),
 'electronics':('電機與電子','Electrical & electronics'),'computing':('資訊與資安','Computing & security'),
 'instruments':('光學與精密儀器','Optics & instruments'),'structures':('橋梁與建築','Bridges & structures'),
 'underground':('隧道與地下工程','Tunnels & geotechnics'),'water':('水利與海岸工程','Water & coastal'),
 'rail':('鐵道與交通','Rail & transit'),'environment':('環境與城市','Environment & cities'),
 'aerospace':('航空工程','Aeronautics'),'marine':('船舶與海洋','Marine & offshore'),
 'automotive':('汽車與交通工具','Automotive'),'space':('太空與衛星','Space & satellites'),
 'manufacturing':('機械與製造','Manufacturing'),'energy':('能源與儲能','Energy & storage'),
 'materials':('材料與冶金','Materials'),'biomedical':('醫療工程','Biomedical'),
 'process':('工業與食品製程','Industrial processes'),'megascience':('大型科學設施','Megascience')}

def concepts(text):
    found=[]
    for name,expression in TERMS:
        if re.search(r'(?<![a-z])(?:'+expression+r')',text,re.I):found.append(name)
    return found

def dedup(items):return list(dict.fromkeys(items))

def main_glyph(course,old):
    item=old.get(course['id'],{})
    # Existing high-quality manually matched library symbols remain under their
    # original MIT/Apache license. Generic framework/backlog mappings do not.
    if item.get('q',0)>=.8 and item.get('d'):
        return 'licensed:'+item['s']+':'+item['n'],item['d'],item['s']
    kind=course.get('diagram',{}).get('type','')
    key=TYPE_MAP.get(kind,kind)
    if key not in GLYPHS:key=CATEGORY_MAIN[course['category']]
    return key,GLYPHS[key],'original'

def semantic_features(course,primary):
    diagram=course.get('diagram',{})
    labels=diagram.get('labelsEn',[])
    title=concepts(course.get('titleEn',''))
    label_concepts=[concepts(v) for v in labels]
    # Main architecture order comes from authored course labels, not a PRNG.
    ordered=[x[0] for x in label_concepts if x]
    ordered += title
    ordered += [n for group in label_concepts for n in group[1:]]
    ordered += concepts(course.get('summaryEn',''))
    return [x for x in dedup(ordered) if x!=primary]

def style_glyph(markup,source,color,accent):
    if source=='m':
        return f'<g fill="{color}" stroke="none">{markup}</g>'
    # Colored semantic lines over a colored foundation; no altered geometry.
    nodes=list(ET.fromstring('<g>'+markup+'</g>'))
    parts=[]
    for i,node in enumerate(nodes):
        node.set('stroke',color if i%3!=2 else accent)
        parts.append(ET.tostring(node,encoding='unicode'))
    return '<g fill="none" stroke-width="1.55" stroke-linecap="round" stroke-linejoin="round">'+''.join(parts)+'</g>'

def nameplate(title):
    words=re.findall(r'[A-Za-z0-9]+',title)
    omitted={'and','of','the','for','in','on','with','engineering','system','systems','design','fabrication','research','processing'}
    words=[w for w in words if w.lower() not in omitted]
    if not words:return title[:12]
    if len(words[0])<=9:return words[0].upper()
    return ''.join(w[0] for w in words[:8]).upper()

def svg(course,primary,markup,source,features,category=False):
    p,a,b,bg=PALETTES[course['category']]
    title=course.get('titleEn',course['title'])
    parts=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 96 96" role="img"><title>{html.escape(title)}</title>',
      '<desc>Engineering topic pictogram. Abstract subject and curriculum components; not an as-built drawing.</desc>',
      f'<rect x="1" y="1" width="94" height="94" rx="22" fill="{bg}"/>',
      f'<circle cx="48" cy="37" r="28" fill="{a}" fill-opacity=".16"/>',
      '<g transform="translate(23 10) scale(2.08)">'+style_glyph(markup,source,p,b)+'</g>']
    # Every extra shape is a declared engineering concept in the manifest.
    positions=[(7,61),(25,61),(43,61),(61,61),(75,6),(3,6),(75,32),(3,32)]
    for i,key in enumerate(features[:8]):
        x,y=positions[i]
        parts.append(f'<g transform="translate({x} {y}) scale(.64)">'+style_glyph(GLYPHS[key],'original',p,b if i%2==0 else a)+'</g>')
    if not category:
        parts.append(f'<rect x="10" y="80" width="76" height="12" rx="6" fill="{p}"/><text x="48" y="88.8" text-anchor="middle" font-family="Arial,sans-serif" font-weight="700" font-size="7.4" fill="white">{html.escape(nameplate(title))}</text>')
    else:
        parts.append(f'<path d="M30 85h36" stroke="{p}" stroke-width="4" stroke-linecap="round"/>')
    return ''.join(parts)+'</svg>\n'

def geometry_digest(content):
    root=ET.fromstring(content)
    keep=[]
    def visit(node,transforms=()):
        tag=node.tag.rsplit('}',1)[-1]
        if tag in ('title','desc','text'):return
        ts=transforms+((node.attrib['transform'],) if 'transform' in node.attrib else ())
        if tag in ('path','rect','circle','ellipse','line','polygon','polyline'):
            attrs={k:v for k,v in node.attrib.items() if k in ('d','x','y','x1','y1','x2','y2','width','height','rx','ry','cx','cy','r','points')}
            keep.append((tag,ts,attrs))
        for child in node:visit(child,ts)
    visit(root)
    return hashlib.sha256(json.dumps(keep,sort_keys=True).encode()).hexdigest()

def build():
    catalog=json.loads((PUBLIC/'data/catalog.json').read_text())
    old=json.loads((PUBLIC/'data/project-icons.json').read_text())['icons']
    overrides=json.loads((HERE/'icon-overrides.json').read_text()) if (HERE/'icon-overrides.json').exists() else {}
    specs={}
    for course in catalog:
        key,markup,source=main_glyph(course,old)
        over=overrides.get(course['id'],{})
        if over.get('main'):
            key=over['main'];markup=GLYPHS[key];source='original'
        features=over.get('features',semantic_features(course,key))
        specs[course['id']]={'course':course,'key':key,'markup':markup,'source':source,'features':features,'count':min(4,len(features)),'rationale':over.get('rationale','Subject and component concepts selected from course title, authored architecture labels and summary.')}
    # Expand genuine semantic feature prefixes where shorter pictograms collide.
    for _ in range(8):
        groups=collections.defaultdict(list)
        for ident,v in specs.items():groups[(v['markup'],tuple(v['features'][:v['count']]))].append(ident)
        changed=False
        for ids in groups.values():
            if len(ids)>1:
                for ident in ids:
                    v=specs[ident]
                    if v['count']<min(8,len(v['features'])):v['count']+=1;changed=True
        if not changed:break
    icons={}; categories={}; geometry=collections.defaultdict(list)
    directory=PUBLIC/'assets/icons-v16/projects';directory.mkdir(parents=True,exist_ok=True)
    for ident,v in specs.items():
        features=v['features'][:v['count']]
        content=svg(v['course'],v['key'],v['markup'],v['source'],features)
        target=directory/(ident+'.svg');target.write_text(content)
        digest=geometry_digest(content);geometry[digest].append(ident)
        icons[ident]={'path':target.relative_to(PUBLIC).as_posix(),'subject':v['key'],'components':features,
            'source':v['source'],'rationale':v['rationale'],'sha256':hashlib.sha256(content.encode()).hexdigest(),'geometrySha256':digest}
    directory=PUBLIC/'assets/icons-v16/categories';directory.mkdir(parents=True,exist_ok=True)
    features={'semiconductor':['mask','etch'],'packaging':['bond','waveguide'],'electronics':['voltage','wave'],
      'computing':['code','shield'],'instruments':['lens','probe'],'structures':['force','concrete'],'underground':['tbm','support'],
      'water':['flow','waves'],'rail':['track','signal'],'environment':['droplet','earth'],'aerospace':['gear','sensor'],
      'marine':['waves','pump'],'automotive':['motor','battery'],'space':['antenna','earth'],'manufacturing':['gear','probe'],
      'energy':['voltage','battery'],'materials':['test','heat'],'biomedical':['wave','sensor'],'process':['pipe','flow'],'megascience':['detector','magnet']}
    for cat,key in CATEGORY_MAIN.items():
        content=svg({'id':cat,'category':cat,'title':NAMES[cat][0],'titleEn':NAMES[cat][1]},key,GLYPHS[key],'original',features[cat],True)
        target=directory/(cat+'.svg');target.write_text(content)
        categories[cat]={'path':target.relative_to(PUBLIC).as_posix(),'title':NAMES[cat][0],'titleEn':NAMES[cat][1],'subject':key,'components':features[cat],'geometrySha256':geometry_digest(content)}
    required={x['id'] for x in catalog if x.get('status')=='guided' or x['category']=='rail'}
    collisions=[ids for ids in geometry.values() if len(ids)>1 and len(required.intersection(ids))>1]
    report={'version':16,'allTopics':len(icons),'requiredTopics':len(required),'categories':len(categories),
      'geometryUniqueAllTopics':len(geometry),'requiredGeometryCollisions':collisions,
      'allGeometryCollisions':[ids for ids in geometry.values() if len(ids)>1],
      'geometryAuditExcludes':'title, desc, text, IDs and all color/style attributes',
      'scope':'Original semantic composites; some subject glyphs are retained from Tabler MIT / Material Design Icons Apache-2.0. Pictograms are not as-built drawings.',
      'status':'PASS' if not collisions else 'NEEDS_SEMANTIC_OVERRIDES'}
    manifest={'version':16,'license':{'original':'CC0-1.0','tabler':'MIT','mdi':'Apache-2.0'},'categories':categories,'icons':icons}
    (PUBLIC/'data/icon-manifest-v16.json').write_text(json.dumps(manifest,ensure_ascii=False,separators=(',',':'))+'\n')
    (HERE/'ICON_AUDIT_V16.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='allGeometryCollisions'},ensure_ascii=False,indent=2))
    return report

if __name__=='__main__':build()
