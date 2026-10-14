#!/usr/bin/env python3
"""Integrate original V11 curricula and references; preserve V10 learning IDs.
Run after the V10 builder for a complete repeatable rebuild, or repeat in place.
"""
import copy,csv,hashlib,io,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'public/academy/data';INPUT=ROOT/'tools/computing-v11'
def read(p):return json.loads(p.read_text('utf-8'))
def write(p,value):
    p.parent.mkdir(parents=True,exist_ok=True)
    text=json.dumps(value,ensure_ascii=False,**({'separators':(',',':')} if p.name=='featured.json' else {'indent':2}))+'\n'
    tmp=p.with_suffix(p.suffix+'.tmp');tmp.write_text(text,'utf-8');tmp.replace(p)
def digest(c):return hashlib.sha256(json.dumps(c,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def subcategory(id):
    n=301 if id=='cybersecurity' else int(id[1:])
    rows=[(301,310,'architecture','處理器與信任鏈','Processors and trust chains'),(311,315,'systems','作業系統與編譯器','Operating systems and compilers'),(316,320,'distributed','儲存、交易與共識','Storage, transactions and consensus'),(321,330,'platforms','雲端平台與可靠交付','Cloud platforms and reliable delivery'),(331,337,'network','網路與時間同步','Networking and time synchronization'),(338,342,'wireless','無線與行動網路','Wireless and mobile networks'),(343,350,'optical','光纖、衛星與量子通訊','Optical, satellite and quantum communication'),(351,358,'trust','零信任、身分與密碼','Zero trust, identity and cryptography'),(359,370,'defense','防禦、監測與事件應變','Defense, monitoring and incident response'),(371,375,'privacy','隱私保護與安全計算','Privacy-preserving and secure computation'),(376,387,'ai','神經網路、資料與視覺系統','Neural networks, data and visual systems'),(388,396,'hpc','高效能運算與世界級超算','HPC and landmark supercomputers'),(397,400,'internet','網際網路的基礎工程','Foundations of Internet engineering')]
    for lo,hi,key,z,en in rows:
        if lo<=n<=hi:return 'it-'+key,z,en
    raise ValueError(id)
def main():
    baseline=read(INPUT/'v10-provenance.json')
    groups=[read(INPUT/f'group_{g}.json') for g in 'abc']
    expansion=read(INPUT/'expansion.json')
    target={x['id'] for g in 'abc' for x in read(INPUT/f'group_{g}_snapshot.json')['catalog']}
    new=[c for g in groups for c in g['courses']]
    assert len(new)==len(target)==100 and {c['id'] for c in new}==target
    extras=expansion['courses'];assert len(extras)==80 and len({c['id'] for c in extras})==80
    assert not target.intersection(c['id'] for c in extras),'Expansion must not overwrite the focused 100'
    catalog=read(DATA/'catalog.json');cat={c['id']:c for c in catalog}
    old=read(DATA/'featured.json');oldby={c['id']:c for c in old}
    for c in extras:
        assert c['id'] not in baseline['courses'],'Existing guided courses must be enriched separately without replacement'
        assert re.fullmatch(r'[a-z0-9][a-z0-9-]{0,79}',c['id']),c['id']
        assert 3<=len(c.get('architectureNodes',[]))<=5 and c.get('architectureFamily'),c['id']
        if c['id'] in cat:
            assert c['title']==cat[c['id']]['title'] and c['titleEn']==cat[c['id']]['titleEn'],c['id']
    sources={s['id']:s for s in read(DATA/'sources.json')};canonical={s['url']:s['id'] for s in sources.values()};aliases={}
    for g in groups+[expansion]:
        for s in g['sources']:
            assert s.get('title') and s.get('titleEn') and s.get('publisher') and s['url'].startswith('https://'),s['id']
            if s['id'] in sources:assert s['url']==sources[s['id']]['url']
            elif s['url'] in canonical:aliases[s['id']]=canonical[s['url']];continue
            s.setdefault('accessed','2026-10-14');s.setdefault('imageReuse','Link only. No source image or article reproduction.');s.setdefault('scope','公開原理或工程背景；本課工作單與數值情境為原創教學。');s.setdefault('scopeEn','Public principles or project context; worksheets and numerical scenarios are original teaching material.')
            sources[s['id']]=s;canonical[s['url']]=s['id']
    def remap(v):
        if isinstance(v,list):
            for x in v:remap(x)
        elif isinstance(v,dict):
            for k,x in v.items():
                if k=='sourceIds':v[k]=list(dict.fromkeys(aliases.get(i,i) for i in x))
                elif k=='sourceId':v[k]=aliases.get(x,x)
                else:remap(x)
    for g in groups+[expansion]:remap(g)
    added={c['id']:c for c in new+extras}
    featured=[c for c in old if c['id'] not in added]+new+extras
    by={c['id']:c for c in featured};assert len(by)==len(featured)
    for id,proof in baseline['courses'].items():
        assert id in by,'V10 course lost: '+id
        if id not in target:assert digest(by[id])==proof['sha256'],'V10 content changed: '+id
        else:
            ids=[s['id'] for st in by[id]['stages'] for s in st['steps']]
            assert ids[:len(proof['stepIds'])]==proof['stepIds'],'Old step IDs/order changed: '+id
            assert by[id].get('curriculumVersion')==proof['curriculumVersion'],'Progress migration changed: '+id
    photos={p['id']:p for p in read(DATA/'photos.json')}
    for c in new+extras:
        id=c['id'];c.update(kind='course',status='guided',depth=4,educationEdition=11,languageCoverage=['zh-TW','en'])
        if id in target:
            c['subcategory'],c['subcategoryTitle'],c['subcategoryTitleEn']=subcategory(id)
            c.setdefault('learningTrack','computing');c.setdefault('learningSubdiscipline',c['subcategory'])
            assert id in cat and c['title']==cat[id]['title'] and c['titleEn']==cat[id]['titleEn'],id
        else:
            c.setdefault('subcategory','v11-'+c.get('learningTrack',c['category']));c.setdefault('subcategoryTitle',c['title']);c.setdefault('subcategoryTitleEn',c['titleEn'])
        c['enrichmentVersion']=11
        if id not in baseline['courses']:c['curriculumVersion']=11
        c.setdefault('contentStatus','reviewable-educational-curriculum')
        c.setdefault('scope','依一手公開資料編寫的原創教學與本地模擬；課程順序是學習路線，不是設備建造、設置或運轉程序。')
        c.setdefault('scopeEn','Original learning exercises and local models based on primary public sources. The sequence is a learning path, not equipment construction, configuration or operating instructions.')
        steps=[s for st in c['stages'] for s in st['steps']]
        expected=len(baseline['courses'].get(id,{}).get('stepIds',[]))+(32 if id in target else 12)
        assert len(steps)==expected,(id,len(steps),expected)
        assert len({s['id'] for s in steps})==len(steps),id
        c['stepCount']=len(steps);c['estimatedMinutes']=sum(s.get('estimatedMinutes',20) for s in steps)
        assert len(c['sourceIds'])>=2 and set(c['sourceIds'])<=sources.keys(),id
        seen=set();number=0
        for i,stage in enumerate(c['stages']):
            stage['order']=i+1
            for j,s in enumerate(stage['steps']):
                number+=1;s.update(order=j+1,sequence=number,simulationOnly=True)
                assert set(s.get('prerequisiteIds',[]))<=seen,s['id'];seen.add(s['id'])
                legacy=s['id'] in baseline['courses'].get(id,{}).get('stepIds',[])
                required=['title','objective','check'] if legacy else ['title','objective','instruction','observation','failure','check']
                for k in required:
                    assert isinstance(s.get(k),str) and s[k].strip() and isinstance(s.get(k+'En'),str) and s[k+'En'].strip(),(id,s['id'],k)
                assert s.get('sourceIds') and set(s['sourceIds'])<=sources.keys(),s['id']
                assert len(s['knowledge'])>=2
                for k in s['knowledge']:
                    assert all(k.get(v) for v in ('id','title','titleEn','text','textEn')),(s['id'],k)
                    assert set(k.get('sourceIds',[]))<=sources.keys()
                q=s['quiz'];assert len(q['options'])==len(q['optionsEn'])==3 and q['answer'] in (0,1,2),s['id']
                assert len(set(q['options']))==3 and len(set(q['optionsEn']))==3,s['id']
                if s.get('photoId'):assert s['photoId'] in photos,s['id']
    # Keep V10 identities and catalogs; append only genuinely new project IDs.
    catalog=[{k:v for k,v in by[c['id']].items() if k!='stages'} if c['id'] in by else c for c in catalog]
    for c in extras:
        if c['id'] not in cat:catalog.append({k:v for k,v in c.items() if k!='stages'})
    assert set(baseline['catalogIds'])<={c['id'] for c in catalog}
    for key in ('id','title','titleEn'):assert len({str(c[key]).casefold() for c in catalog})==len(catalog),'Duplicate '+key
    pm={p['courseId']:p for p in read(DATA/'course-places.json')['courses']};rm={r['courseId']:r for r in read(DATA/'related-skills.json')['courses']}
    for g in groups+[expansion]:
        for p in g['places']:pm[p['courseId']]=p
        for r in g['related']:rm[r['courseId']]=r
    assert set(pm)==set(rm)==set(by),'Every guided course needs place/history/comparisons'
    def reference(ref):
        full=sources.get(canonical.get(ref['url'],''),{})
        for key in ('title','titleEn','publisher','scope','scopeEn'):
            if not ref.get(key) and full.get(key):ref[key]=full[key]
        ref.setdefault('titleEn',ref.get('title','Primary reference'));ref.setdefault('scope','官方工程背景與原理；請依來源適用範圍查閱。');ref.setdefault('scopeEn','Official engineering context and principles; consult the scope of the original source.')
        assert all(ref.get(k) for k in ('title','titleEn','publisher','scope','scopeEn')) and ref['url'].startswith('https://'),ref
        return ref
    for p in pm.values():
        point=p['place'];assert -90<=point['lat']<=90 and -180<=point['lng']<=180
        for key in ('name','nameEn','address','addressEn','coordinateScope','coordinateScopeEn'):assert point.get(key),(p['courseId'],key)
        assert len(p['history'])>=2 and len(p['references'])>=2,p['courseId']
        p['references']=[reference(r) for r in p['references']]
    for r in rm.values():
        assert len(r['related'])==len({v['id'] for v in r['related']})==2,r['courseId']
        refs={ref['url']:reference(ref) for ref in r.get('references',[])}
        for id in [r['courseId']]+[v['id'] for v in r['related']]:
            assert id in by,id
            for ref in pm[id]['references']:refs.setdefault(ref['url'],copy.deepcopy(ref))
        for v in r['related']:
            id=v['id'];assert id!=r['courseId'];v.update(title=by[id]['title'],titleEn=by[id]['titleEn'],place=copy.deepcopy(pm[id]['place']))
            v.setdefault('why',v.get('transfer'));v.setdefault('whyEn',v.get('transferEn'))
            assert all(v.get(k) for k in ('transfer','transferEn','difference','differenceEn'))
            assert len(v['practice'])==len(v['practiceEn'])==3
            v['referenceUrls']=list(dict.fromkeys(v.get('referenceUrls',[])+[ref['url'] for ref in pm[id]['references']]))
            for url in v['referenceUrls']:
                if url not in refs:assert url in canonical,url;refs[url]=reference(copy.deepcopy(sources[canonical[url]]))
        r.setdefault('overview','比較可轉移的原理、適用邊界與驗證證據。');r.setdefault('overviewEn','Compare transferable principles, limits and verification evidence.');r['references']=list(refs.values())
    media=read(DATA/'media.json');mm={m['courseId']:m for m in media['courses']}
    for c in new+extras:
        steps=[s for st in c['stages'] for s in st['steps']];entry=mm.setdefault(c['id'],{'courseId':c['id'],'videos':[],'guides':[]});key=c['id']+'-v11-architecture-guide'
        guide={'id':key,'title':'架構、算例與證據：'+c['title'],'titleEn':'Architecture, examples and evidence: '+c['titleEn'],'concept':c['summary'],'conceptEn':c['summaryEn'],'procedure':[s['instruction'] for s in steps[-(32 if c['id'] in target else 12):][::(6 if c['id'] in target else 2)]],'procedureEn':[s['instructionEn'] for s in steps[-(32 if c['id'] in target else 12):][::(6 if c['id'] in target else 2)]],'evidence':[s['check'] for s in steps[-3:]],'evidenceEn':[s['checkEn'] for s in steps[-3:]],'pitfalls':[steps[-1]['failure']],'pitfallsEn':[steps[-1]['failureEn']],'sourceIds':c['sourceIds'],'sources':[copy.deepcopy(sources[sid]) for sid in c['sourceIds']],'simulationOnly':True,'scope':c['scope'],'scopeEn':c['scopeEn']}
        entry['guides']=[g for g in entry.get('guides',[]) if g['id']!=key]+[guide]
    media.update(version=11,courses=list(mm.values()))
    for name,value in [('featured',featured),('catalog',catalog),('sources',list(sources.values())),('course-places',{'version':11,'courses':list(pm.values())}),('related-skills',{'version':11,'courses':list(rm.values())}),('media',media)]:write(DATA/f'{name}.json',value)
    # Industry links are explicitly presented as technical-source publishers,
    # not guessed suppliers. Existing curated securities remain unchanged.
    vendors=read(DATA/'vendors.json');vm={v['id']:v for v in vendors['vendors']};am={a['courseId']:a for a in vendors['courses']}
    for c in new+extras:
        refs=[sources[s] for s in c['sourceIds']];ids=[];roles=[]
        for ref in refs:
            pub=ref['publisher'];id='v11-publisher-'+hashlib.sha256(pub.casefold().encode()).hexdigest()[:12]
            if id not in vm:vm[id]={'id':id,'name':pub,'nameEn':pub,'business':ref.get('scope','本課引用的公開技術資料發布者。'),'businessEn':ref.get('scopeEn','Publisher of a public technical reference cited by this course.'),'url':ref['url'],'sourceUrl':ref['url'],'investorUrl':'','reviewed':'2026-10-14','security':None,'entityType':'technical-source-publisher'}
            ids.append(id);roles.append({'vendorId':id,'role':'公開技術資料與工程案例來源','roleEn':'Public technical and engineering-case reference','productUrl':ref['url']})
        am[c['id']]={'courseId':c['id'],'vendorIds':list(dict.fromkeys(ids)),'roles':roles,'connection':'以下為本課引用的技術發布者、研究機構或工程業主；來源關聯不代表供應、合作或背書。','connectionEn':'These are cited technical publishers, research institutions or project owners. A reference association does not assert supply, partnership or endorsement.'}
    vendors.update(version=11,vendors=list(vm.values()),courses=list(am.values()));write(DATA/'vendors.json',vendors)
    for filename,rows in [('catalog-index.csv',catalog),('information-security-100.csv',[by[x['id']] for g in 'abc' for x in read(INPUT/f'group_{g}_snapshot.json')['catalog']]),('world-expansion-v11.csv',extras)]:
        buf=io.StringIO(newline='');w=csv.writer(buf,lineterminator='\n');w.writerow(['id','title_zh','title_en','category','subcategory_zh','subcategory_en','content_type','authored_steps','route'])
        for c in rows:w.writerow([c['id'],c['title'],c['titleEn'],c['category'],c.get('subcategoryTitle',''),c.get('subcategoryTitleEn',''),'guided' if c['id'] in by else 'research',c.get('stepCount',0) if c['id'] in by else 0,'#project/'+c['id']])
        (DATA/filename).write_text(buf.getvalue(),'utf-8-sig')
    allsteps=[s for c in featured for st in c['stages'] for s in st['steps']];itsteps=[s for c in new for st in c['stages'] for s in st['steps']]
    release=read(DATA/'release.json');release.update(version='11.0.0',date='2026-10-14',topics=len(catalog),guidedCourses=len(featured),researchTopics=len(catalog)-len(featured),allSteps=len(allsteps),knowledgePoints=sum(len(s['knowledge']) for s in allsteps),sources=len(sources),newGuidedCourses=len(featured)-338,newGuidedSteps=4160,computingFocusCourses=100,computingFocusSteps=len(itsteps),computingSubdisciplines=13,worldExpansionCourses=80,worldExpansionSteps=960,courseHistories=len(pm),mapLocations=len(pm),curatedRelatedCourses=len(rm),curatedComparisons=sum(len(r['related']) for r in rm.values()),curatedRelatedSkills=sum(len(r['related']) for r in rm.values()),relatedMapLocations=sum(len(r['related']) for r in rm.values()),mentorDemonstrations=len(allsteps),narratedGuideSteps=len(allsteps),supplementalGuides=sum(len(m.get('guides',[])) for m in media['courses']),industryEntities=len(vm),industryCourseAssociations=len(am),listedInstruments=sum(bool(v.get('security')) for v in vm.values()),relatedReferenceUrls=len({r['url'] for entry in rm.values() for r in entry['references']}),computingScope='100 focused computing/security curricula plus named quantum, acceleration, energy and resource systems. Original architectural exercises and synthetic local evidence, not deployment or industrial operating manuals.')
    release.update(authoredInteractiveTasks=52,sharedInteractiveTasks=len(allsteps)-52,exerciseSceneFamilies=636,computingOriginalDiagrams=100,worldOriginalDiagrams=80,newOriginalArchitectureSvgFiles=360,newOriginalIconSvgFiles=180,computingInteractiveModels=16,worldInteractiveModels=8,idealQuantumModel=True,executableMiniLabs=12,learningMapTracks=17,learningMapBranches=35,learningMapRoutes=12,computingLearningRoutes=10)
    release['newLicensedPhotos']=0
    release['newOriginalMediaSvgFiles']=540
    release['projectVisualScope']='Original subject architectures: 99 semiconductor, 100 packaging/photonics, 100 electrical/electronics, 100 computing/security and 80 named world projects. Diagrams are educational, not CAD. Licensed photographs are representative; V11 adds diagrams and preserves V10 photographs/videos.'
    write(DATA/'release.json',release)
    print(json.dumps({k:release[k] for k in ('topics','guidedCourses','allSteps','computingFocusCourses','computingFocusSteps','worldExpansionCourses','knowledgePoints','sources')},ensure_ascii=False))
if __name__=='__main__':main()
