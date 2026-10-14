import json
from pathlib import Path
ROOT=Path(__file__).parent
BASE=ROOT.parents[1]/'public/academy/data'
def read(p):return json.loads(p.read_text())
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
photos={p['id']:p for p in read(BASE/'photos.json')}
photo_notes={
 'wafers':('可觀察晶圓外觀與整片／晶粒尺度的差異；照片不顯示奈米結構或本步量測結果。','Observe wafer appearance and wafer-versus-die scale; the photograph does not show nanoscale structures or this step’s measured results.'),
 'wafer-tweezers':('可觀察晶圓夾持工具的接觸端；這不是自動晶圓搬運設備，也未展示本步清洗或熱處理。','Observe the contact end of wafer tweezers; this is not an automated wafer handler and does not show this step’s cleaning or thermal treatment.'),
 'wafer-foundry':('可觀察無塵室設備與搬運環境；此廠房照片不是任何指定節點或本步製程的實拍證據。','Observe cleanroom equipment and handling context; this facility photograph does not document a specific node or this process step.'),
 'cleanroom':('可觀察微影工作環境；照片不能呈現光阻化學、線寬、套刻或設備內部狀態。','Observe a lithography working environment; the photograph cannot establish resist chemistry, critical dimension, overlay or internal tool state.'),
 'lithography-lab':('可觀察微影實驗室的黃光照明與工作區；它不是 EUV 掃描機內部或本步光阻反應的照片。','Observe yellow lighting and the lithography work area; this is not an EUV scanner interior or an image of this step’s resist reaction.'),
 'sputter-chamber':('可觀察濺鍍設備的真空腔體與外部硬體；不能由照片推知 ALD/CVD 反應、膜厚、配方或本步結果。','Observe sputtering vacuum equipment and external hardware; the photograph does not establish ALD/CVD reactions, film thickness, recipes or step outcomes.'),
 'probe-station':('可觀察探針台的定位與量測硬體；照片不包含待測電路的 I-V 曲線、測試條件或良率。','Observe probe-station positioning and measurement hardware; no DUT I–V curves, test conditions or yield data are shown.'),
 'sem-microscope':('可觀察掃描式電子顯微鏡設備；這是設備照片，不是本步缺陷、截面或尺寸的 SEM 影像。','Observe scanning-electron-microscope hardware; this is an equipment photograph, not a micrograph of this step’s defects, section or dimensions.'),
 'wirebond':('可觀察開蓋晶粒、接合線與周邊接點；它示範打線結構，不代表倒裝、混合鍵合或特定先進節點。','Observe a decapped die, bond wires and surrounding contacts; it illustrates wire bonding, not flip-chip, hybrid bonding or a particular advanced node.'),
 'bga-section':('可觀察封裝截面、基板與外部焊球；它不是 TSV／HBM／混合鍵合的專屬截面，也不能判定內部空洞。','Observe a package cross section, substrate and external balls; it is not a TSV/HBM/hybrid-bond cross section and cannot establish internal voiding.'),
 'bga-inside':('可觀察 BGA 封裝內的晶粒及周邊互連；不將這張傳統封裝內部照片當作扇出、RDL、HBM 或 CPO 實拍。','Observe a die and surrounding interconnects in a BGA package; this conventional package interior is not a fan-out, RDL, HBM or CPO process photograph.'),
 'bga-balls':('可觀察電路板上封裝元件的位置及外觀；這是頂視圖，焊球位於底部不可見，無法由此判定接合品質。','Observe the package on a circuit board; this is a top view, so underside balls are not visible and joint quality cannot be inferred.')}
sc_photos=['wafer-foundry','wafer-tweezers','sem-microscope','wafer-foundry','sem-microscope','sputter-chamber','lithography-lab','cleanroom','sem-microscope','sem-microscope','wafer-foundry','probe-station','sputter-chamber','sputter-chamber','sputter-chamber','wafers','sem-microscope','probe-station','probe-station','wafers']
pk_photos=['bga-section','wafers','wafer-tweezers','wafers','bga-inside','wirebond','bga-section','bga-inside','bga-section','sputter-chamber','sem-microscope','wafers','bga-section','bga-inside','probe-station','bga-section','bga-section','bga-balls','sem-microscope','probe-station']
featured=read(BASE/'featured.json')
legacy=ROOT/'legacy_courses_v1.json'
if not legacy.exists():write(legacy,[c for c in featured if c['id'] in ['semiconductor','packaging']])
sources=read(BASE/'sources.json');source_map={s['id']:s for s in sources}
for name in ['sources_semiconductor_a','sources_semiconductor_b','sources_packaging_a','sources_packaging_b']:
 data=read(ROOT/(name+'.json'))
 if isinstance(data,dict):data=data.get('sources',data.get('items'))
 for src in data:
  src.setdefault('accessed','2026-10-12');src.setdefault('sourceType','primary technical reference');src.setdefault('imageReuse','Link only; image redistribution requires separate permission.')
  if src['id'] in source_map:assert source_map[src['id']]['url']==src['url'],src['id']
  source_map[src['id']]=src
for courseid,names,mapping in [('semiconductor',['semiconductor_a','semiconductor_b'],sc_photos),('packaging',['packaging_a','packaging_b'],pk_photos)]:
 stages=[]
 for n in names:
  data=read(ROOT/(n+'.json'));stages.extend(data['stages'] if isinstance(data,dict) else data)
 stages.sort(key=lambda s:int(s['id'].rsplit('m',1)[1]))
 assert len(stages)==20
 steps=[s for stage in stages for s in stage['steps']];assert len(steps)==520
 c=next(c for c in featured if c['id']==courseid);c['stages']=stages;c['curriculumVersion']=2;c['stepCount']=520;c['flowDiagram']='assets/diagrams/'+courseid+'-flow.svg'
 c['sourceIds']=list(dict.fromkeys(i for s in steps for i in s['sourceIds']))
 c['summary']='以 20 個模組、520 個學習步驟，拆解晶圓製作、元件、微影、薄膜、蝕刻、互連、量測與製程整合。' if courseid=='semiconductor' else '以 20 個模組、520 個學習步驟，深入減薄切割、打線、倒裝、扇出、RDL、TSV、混合鍵合、HBM、散熱與可靠度。'
 c['summaryEn']='Twenty modules and 520 learning steps explore wafers, devices, lithography, films, etch, interconnects, metrology and integration.' if courseid=='semiconductor' else 'Twenty modules and 520 learning steps cover thinning, singulation, wire bonding, flip-chip, fan-out, RDL, TSV, hybrid bonding, HBM, thermal design and reliability.'
 c['scope']='依公開原理編寫的教學拆解；模組編號是學習順序，製程分支與實際前後關係另有說明。520 步不代表任何廠商的完整量產配方或固定製程數。所有步驟使用明確標示的代表照片；重複使用照片不等於每步專屬實拍。操作為原創概念模擬與工程推理，實驗資料需自行提供或查閱來源。'
 c['scopeEn']='Educational subdivisions based on public principles. Module numbers describe learning order; process branches and actual dependencies are identified separately. The 520 steps are not a proprietary manufacturing recipe or universal process count. Every step has a labeled representative photograph; reused images are not step-specific process photography. Activities use original concept simulations and engineering reasoning; measured data must be supplied or obtained from sources.'
 for stageidx,stage in enumerate(stages):
  stage['order']=stageidx+1
  for idx,s in enumerate(stage['steps']):
   s['order']=idx+1;s['sequence']=stageidx*26+idx+1
   s['photoId']=mapping[stageidx];note=photo_notes[s['photoId']]
   s['photoNote']='本步代表性真實照片（同模組可能共用）。'+note[0]
   s['photoNoteEn']='Representative real photograph for this step (may be shared within the module). '+note[1]
   s['photoEvidence']='representative-equipment-or-structure'
   # Scientific manufacturing prerequisites may point forward in curriculum order.
   s.setdefault('prerequisiteIds',[])
   assert s['photoId'] in photos
 for s in steps:
  assert all(i in source_map for i in s['sourceIds']),(s['id'],s['sourceIds'])
  assert all(i in {x['id'] for x in steps} for i in s['prerequisiteIds']),(s['id'],s['prerequisiteIds'])
catalog=read(BASE/'catalog.json');byid={c['id']:c for c in featured}
for i,c in enumerate(catalog):
 if c['id'] in byid:
  c=byid[c['id']].copy();c['stepCount']=sum(len(s['steps']) for s in c.pop('stages'));catalog[i]=c
write(BASE/'featured.json',featured);write(BASE/'catalog.json',catalog);write(BASE/'sources.json',list(source_map.values()))
stats={'topics':len(catalog),'guidedCourses':len(featured),'deepCourses':2,'deepSteps':1040,'allSteps':sum(len(s['steps']) for c in featured for s in c['stages']),'knowledgePoints':sum(len(x['knowledge']) for c in featured for s in c['stages'] for x in s['steps']),'sources':len(source_map),'actualPhotos':len(photos),'photoAssignments':1040,'materials':0}
write(BASE/'release.json',{'version':'2.0.0','date':'2026-10-12',**stats,'photography':'Representative photographs are reused; no claim of step-specific photos.','curriculum':'Educational subdivisions and route branches, not a qualified manufacturing traveler.'})
print(json.dumps(stats,ensure_ascii=False))
