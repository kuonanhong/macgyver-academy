#!/usr/bin/env python3
"""Integrate exactly 100 electronics courses, preserving every V9 learning ID."""
import copy,csv,hashlib,io,json,re,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];DATA=ROOT/'public/academy/data';INPUT=ROOT/'tools/electronics-v10'
def read(p):return json.loads(p.read_text('utf-8'))
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,**({'separators':(',',':')} if p.name=='featured.json' else {'indent':2}))+'\n','utf-8')
def subcategory(id):
 n=int(id[1:])
 for lo,hi,key,z,en in [(201,210,'apparatus','發電與高壓設備','Generation and high-voltage apparatus'),(211,220,'transmission','輸電、補償與保護','Transmission, compensation and protection'),(221,230,'grid','電網運轉與數位化','Grid operation and digitalization'),(231,240,'renewables','再生能源電力系統','Renewable electrical systems'),(241,250,'storage','儲能與供電整合','Storage and power integration'),(251,260,'motion','馬達與運動控制','Motors and motion control'),(261,270,'conversion','功率轉換與電子','Power conversion and electronics'),(271,280,'signal','類比、射頻與訊號鏈','Analog, RF and signal chains'),(281,290,'assembly','電路板、組裝與驗證','Boards, assembly and validation'),(291,297,'interfaces','顯示、致動與工業介面','Displays, actuation and industrial interfaces'),(298,300,'landmarks','跨海直流輸電巨作','Landmark HVDC interconnectors')]:
  if lo<=n<=hi:return 'elec-'+key,z,en
 raise ValueError(id)
def main():
 catalog=read(DATA/'catalog.json');cat={c['id']:c for c in catalog};target={c['id'] for c in catalog if c['category']=='electronics'};assert len(target)==100
 vendorSources=read(INPUT/'other-vendor-sources.json')['sources']
 for v in vendorSources:v.setdefault('scope',v.get('basis','Official industry reference.'));v.setdefault('scopeEn',v.get('basis','Official industry reference.'));v.setdefault('titleEn',v['title'])
 groups=[read(INPUT/f'group_{g}.json') for g in 'abc'];overlay=read(INPUT/'media.json');allnew=[c for g in groups for c in g['courses']]
 assert len(allnew)==100 and {c['id'] for c in allnew}==target
 sources={s['id']:s for s in read(DATA/'sources.json')};canonical={s['url']:s['id'] for s in sources.values()};aliases={}
 for g in groups+[overlay,{'sources':vendorSources}]:
  for s in g.get('sources',[]):
   assert s['url'].startswith('https://') and s.get('title'),s
   if s['id'] in sources:assert sources[s['id']]['url']==s['url'],s['id']
   elif s['url'] in canonical:aliases[s['id']]=canonical[s['url']];continue
   s.setdefault('accessed','2026-10-14');s.setdefault('imageReuse','Linked reference only; no image reuse implied.');sources[s['id']]=s;canonical[s['url']]=s['id']
 def remap(value):
  if isinstance(value,list):
   for v in value:remap(v)
  elif isinstance(value,dict):
   for k,v in value.items():
    if k=='sourceIds':value[k]=list(dict.fromkeys(aliases.get(i,i) for i in v))
    elif k=='sourceId' and isinstance(v,str):value[k]=aliases.get(v,v)
    else:remap(v)
 for g in groups+[overlay]:remap(g)
 featured=[c for c in read(DATA/'featured.json') if c['id'] not in target]+allnew;by={c['id']:c for c in featured}
 assert len(featured)==len(by)==338
 for v in vendorSources:
  sid=canonical[v['url']]
  if sid not in by[v['courseId']]['sourceIds']:by[v['courseId']]['sourceIds'].append(sid)
 baseline=read(INPUT/'group_a_snapshot.json')['existing']
 for old in baseline:
  ids=[s['id'] for st in old['stages'] for s in st['steps']];new=[s['id'] for st in by[old['id']]['stages'] for s in st['steps']]
  assert new[:len(ids)]==ids,(old['id'],'V9 step IDs removed/reordered')
  assert by[old['id']].get('curriculumVersion')==old.get('curriculumVersion'),(old['id'],'migration version changed')
 for c in allnew:
  id=c['id'];assert c['title']==cat[id]['title'] and c['titleEn']==cat[id]['titleEn'],id
  c.update(kind='course',status='guided',depth=4,languageCoverage=['zh-TW','en']);c['subcategory'],c['subcategoryTitle'],c['subcategoryTitleEn']=subcategory(id)
  if id in {'a203','a211'}:c['enrichmentVersion']=10
  else:c['curriculumVersion']=10;assert len(c['stages'])==4 and all(len(st['steps'])==6 for st in c['stages']),id
  steps=[s for st in c['stages'] for s in st['steps']];c['stepCount']=len(steps);c['estimatedMinutes']=sum(s.get('estimatedMinutes',20) for s in steps)
  assert len(steps)==({'a203':36,'a211':48}.get(id,24))
  assert len({s['id'] for s in steps})==len(steps) and len({s['instruction'] for s in steps})==len(steps),id
  assert len(c['sourceIds'])>=2 and set(c['sourceIds'])<=sources.keys(),id
  seen=set();seq=0
  for i,stage in enumerate(c['stages']):
   stage['order']=i+1
   for j,s in enumerate(stage['steps']):
    seq+=1;s.update(order=j+1,sequence=seq,simulationOnly=True)
    assert set(s.get('prerequisiteIds',[]))<=seen,s['id'];seen.add(s['id'])
    for key in ('title','objective','instruction','observation','failure','check'):
     assert s.get(key) and s.get(key+'En'),(s['id'],key)
    assert s.get('sourceIds') and set(s['sourceIds'])<=sources.keys(),s['id']
    assert len(s['knowledge'])>=2
    for k in s['knowledge']:
     assert all(k.get(key) for key in ('title','titleEn','text','textEn'));assert set(k.get('sourceIds',[]))<=sources.keys()
    q=s['quiz'];assert len(q['options'])==len(q['optionsEn'])==3 and q['answer'] in (0,1,2)
 places=read(DATA/'course-places.json');pm={p['courseId']:p for p in places['courses']}
 related=read(DATA/'related-skills.json');rm={r['courseId']:r for r in related['courses']}
 for g in groups:
  for p in g['places']:
   assert p['courseId'] in target and len(p['history'])>=2 and len(p['references'])>=2
   point=p['place'];assert -90<=point['lat']<=90 and -180<=point['lng']<=180
   for key in ('name','nameEn','address','addressEn','coordinateScope','coordinateScopeEn'):assert point.get(key),(p['courseId'],key)
   pm[p['courseId']]=p
  for r in g['related']:rm[r['courseId']]=r
 assert set(pm)==set(rm)==set(by)
 def enrich_reference(ref):
  full=sources.get(canonical.get(ref['url'],''),{})
  for key in ('title','titleEn','publisher','scope','scopeEn'):
   if not ref.get(key) and full.get(key):ref[key]=full[key]
  ref.setdefault('titleEn',ref.get('title','Official reference'))
  ref.setdefault('scope','官方技術、機構或工程歷史參考；請依頁面所述範圍閱讀。')
  ref.setdefault('scopeEn','Official technical, institutional or engineering-history reference; consult the stated scope of the linked page.')
  assert all(ref.get(key) for key in ('title','titleEn','publisher','scope','scopeEn')),ref['url']
  return ref
 for p in pm.values():p['references']=[enrich_reference(ref) for ref in p['references']]
 for r in rm.values():
  assert len(r['related'])==len({x['id'] for x in r['related']})==2,r['courseId']
  refs={x['url']:x for x in r.get('references',[])}
  for id in [r['courseId']]+[x['id'] for x in r['related']]:
   assert id in by,(r['courseId'],id)
   for ref in pm[id]['references']:refs.setdefault(ref['url'],copy.deepcopy(ref))
  for x in r['related']:
   id=x['id'];assert id!=r['courseId'];x.update(title=by[id]['title'],titleEn=by[id]['titleEn'],place=copy.deepcopy(pm[id]['place']))
   x.setdefault('why',x['transfer']);x.setdefault('whyEn',x['transferEn'])
   assert all(x.get(k) for k in ('transfer','transferEn','difference','differenceEn'))
   assert len(x['practice'])==len(x['practiceEn'])==3
   x['referenceUrls']=list(dict.fromkeys(x.get('referenceUrls',[])+[ref['url'] for ref in pm[id]['references']]))
   for url in x['referenceUrls']:
    if url not in refs:
     assert url in canonical,(r['courseId'],url);refs[url]=copy.deepcopy(sources[canonical[url]])
  r.setdefault('overview','比較工程原理、適用邊界與證據。');r.setdefault('overviewEn','Compare engineering principles, boundaries and evidence.');r['references']=[enrich_reference(ref) for ref in refs.values()]
 places.update(version=10,courses=list(pm.values()));related.update(version=10,courses=list(rm.values()))
 photos={p['id']:p for p in read(DATA/'photos.json')};media=read(DATA/'media.json');mm={m['courseId']:m for m in media['courses']}
 for p in overlay['photos']:
  path=ROOT/'public/academy'/p['path'];assert path.is_file() and all(p.get(k) for k in ('author','license','licenseUrl','sourceUrl'))
  assert not re.search(r'\bNC\b|NonCommercial',p['license'],re.I),p['id']
  if p.get('sha256'):assert hashlib.sha256(path.read_bytes()).hexdigest()==p['sha256']
  assert set(p.get('courseIds',[]))<=by.keys(),p['id'];photos[p['id']]=p
 for entry in overlay.get('courses',overlay.get('media',[])):
  id=entry['courseId'];assert id in by
  current=mm.setdefault(id,{'courseId':id,'videos':[],'guides':[]})
  for field in ('videos','guides'):
   key=(lambda v:v.get('youtubeId') or v.get('embedUrl') or v['id']) if field=='videos' else (lambda v:v['id'])
   items={key(v):v for v in current.get(field,[])};items.update({key(v):v for v in entry.get(field,[])});current[field]=list(items.values())
  for guide in entry.get('guides',[]):
   for sid in guide.get('sourceIds',[]):
    assert sid in sources,(id,sid)
    if sid not in by[id]['sourceIds']:by[id]['sourceIds'].append(sid)
  for v in entry.get('videos',[]):
   url=v.get('sourcePage') or v.get('url')
   if not url or not url.startswith('https://'):continue
   sid=canonical.get(url)
   if not sid:
    sid='v10-video-'+hashlib.sha256(url.encode()).hexdigest()[:12];sources[sid]={'id':sid,'title':v['title'],'titleEn':v.get('titleEn',v['title']),'publisher':v.get('publisher','Official publisher'),'url':url,'scope':v.get('scope','官方背景影片；非逐步製程錄影。'),'scopeEn':v.get('scopeEn','Official background video; not a recording of every process.'),'accessed':'2026-10-14','imageReuse':'External embed/link only.'};canonical[url]=sid
   if sid not in by[id]['sourceIds']:by[id]['sourceIds'].append(sid)
 media.update(version=10,courses=list(mm.values()))
 catalog=[{k:v for k,v in by[c['id']].items() if k!='stages'} if c['id'] in by else c for c in catalog]
 for name,value in [('featured',featured),('catalog',catalog),('sources',list(sources.values())),('photos',list(photos.values())),('course-places',places),('related-skills',related),('media',media)]:write(DATA/f'{name}.json',value)
 for filename,rows in [('catalog-index.csv',catalog),('electrical-electronics-100.csv',[c for c in catalog if c['id'] in target])]:
  stream=io.StringIO(newline='');writer=csv.writer(stream,lineterminator='\n');writer.writerow(['id','title_zh','title_en','category','subcategory_zh','subcategory_en','content_type','authored_steps','route'])
  for c in rows:writer.writerow([c['id'],c['title'],c['titleEn'],c['category'],c.get('subcategoryTitle',''),c.get('subcategoryTitleEn',''),'guided' if c['id'] in by else 'research',c.get('stepCount',0) if c['id'] in by else 0,'#project/'+c['id']])
  (DATA/filename).write_text(stream.getvalue(),'utf-8-sig')
 steps=[s for c in featured for st in c['stages'] for s in st['steps']];electrical=[s for c in allnew for st in c['stages'] for s in st['steps']]
 assert len(steps)==8882 and len(electrical)==2436
 coverage=json.loads(subprocess.check_output(['node','tools/test-process-exercises.mjs'],cwd=ROOT,text=True))
 write(ROOT/'docs/EXERCISE_COVERAGE_V10.json',coverage)
 release=read(DATA/'release.json');release.update(authoredInteractiveTasks=coverage['authored'],sharedInteractiveTasks=coverage['shared'],exerciseSceneFamilies=coverage['sceneFamilies'],projectVisualScope='99 semiconductor, 100 packaging/photonics and 100 electrical/electronics topics have subject-specific original educational diagrams. Licensed photos are representative, not step-by-step production recordings.',version='10.0.0',date='2026-10-14',guidedCourses=338,researchTopics=1662,allSteps=len(steps),knowledgePoints=sum(len(s['knowledge']) for s in steps),sources=len(sources),actualPhotos=len(photos),newGuidedCourses=98,newGuidedSteps=2400,electronicsTopics=100,electronicsGuidedCourses=100,electronicsSteps=len(electrical),electronicsSubdisciplines=11,materials=0,courseHistories=338,mapLocations=338,curatedRelatedCourses=338,curatedComparisons=676,curatedRelatedSkills=676,relatedMapLocations=676,mentorDemonstrations=len(steps),narratedGuideSteps=len(steps),videoResources=sum(len(m.get('videos',[])) for m in media['courses']),embeddedVideos=sum(bool(v.get('embedUrl') or v.get('nativeVideoUrl')) for m in media['courses'] for v in m.get('videos',[])),supplementalGuides=sum(len(m.get('guides',[])) for m in media['courses']),photoAssignments=sum(bool(s.get('photoId')) for s in steps),relatedReferenceUrls=len({r['url'] for entry in rm.values() for r in entry.get('references',[])}),billingScope='Hosted owner/demo and offline editions contain complete source; protected Python HTTPS commerce requires operator configuration. No live payment activated.',languageScope='Traditional Chinese and English core; 77 optional machine-translated languages require a configured service. Voice availability depends on the device.')
 release['uniqueYouTubeVideos']=len({v['embedUrl'].split('/embed/')[1].split('?')[0] for m in media['courses'] for v in m.get('videos',[]) if 'youtube-nocookie.com/embed/' in v.get('embedUrl','')})
 write(DATA/'release.json',release)
 (ROOT/'public/academy/assets/photos/LICENSES.txt').write_text('PHOTOGRAPH ATTRIBUTION / V10\n\n'+'\n\n'.join(p['id']+'\n'+p.get('attribution',p['author'])+'\nSource: '+p['sourceUrl']+'\nLicense: '+p['license']+' '+p['licenseUrl']+'\nChanges: '+p.get('changes','None') for p in photos.values())+'\n','utf-8')
 subprocess.run(['python3','tools/electronics-v10/build_vendors.py'],cwd=ROOT,check=True)
 vendors=read(DATA/'vendors.json');release.update(industryEntities=len(vendors['vendors']),industryCourseAssociations=len(vendors['courses']),listedInstruments=sum(bool(v.get('security')) for v in vendors['vendors']),newLicensedPhotos=len(overlay['photos']),newOriginalMediaSvgFiles=398,electronicsOriginalDiagrams=100,electronicsInteractiveModels=25,electronicsModelCourses=93)
 write(DATA/'release.json',release)
 print(json.dumps({k:release[k] for k in ('guidedCourses','electronicsGuidedCourses','electronicsSteps','allSteps','knowledgePoints','sources','actualPhotos','uniqueYouTubeVideos')}))
if __name__=='__main__':main()
