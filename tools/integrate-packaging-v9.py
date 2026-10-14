#!/usr/bin/env python3
"""Integrate 100 packaging / photonics curricula with exact provenance and stable IDs."""
import copy
import csv
import hashlib
import io
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT/'public/academy/data'
INPUT = ROOT/'tools/packaging-v9'
EXISTING = {'packaging', 'silicon-photonics', 'a106'}
def read(path): return json.loads(path.read_text(encoding='utf-8'))
def write(path, value):
    # The complete authored original remains in tools; ship compact large course data.
    body=json.dumps(value,ensure_ascii=False,separators=(',',':')) if path.name=='featured.json' else json.dumps(value,ensure_ascii=False,indent=2)
    path.write_text(body+'\n',encoding='utf-8')

def subcategory(ident):
    if ident=='packaging': return ('pkg-integration','封裝整合總覽','Package integration overview')
    if ident=='silicon-photonics': return ('pkg-systems','CPO 與系統整合','CPO and systems integration')
    n=int(ident[1:])
    for lo,hi,key,zh,en in [
        (103,108,'joining','凸塊與精密接合','Bumps and precision bonding'),
        (109,113,'handling','薄化、切割與晶粒搬運','Thinning, dicing and die handling'),
        (114,120,'encapsulation','封膠、扇出與異質整合','Encapsulation, fan-out and heterogeneous integration'),
        (121,124,'vias','穿孔與金屬互連','Through vias and metal interconnects'),
        (125,129,'substrates','中介層與封裝基板','Interposers and package substrates'),
        (130,138,'electrical','小晶片、訊號與電源','Chiplets, signals and power'),
        (139,145,'thermal','熱管理與功率封裝','Thermal management and power packaging'),
        (146,150,'reliability','可靠度與非破壞檢測','Reliability and nondestructive inspection'),
        (151,161,'passive','波導、耦合與被動元件','Waveguides, coupling and passive devices'),
        (162,167,'active','調變、偵測與相移','Modulation, detection and phase shifting'),
        (168,173,'sources','異質材料、雷射與光源','Heterogeneous materials, lasers and sources'),
        (174,178,'circuits','多工、開關與相干電路','Multiplexing, switches and coherent circuits'),
        (179,184,'sensing','光達、感測與量子光子','Lidar, sensing and quantum photonics'),
        (185,190,'verification','光子測試、漂移與設計驗證','Photonic test, drift and design verification'),
        (191,195,'systems','CPO 與系統整合','CPO and systems integration'),
        (196,200,'platforms','產業整合案例與平台','Industrial integration cases and platforms')]:
        if lo<=n<=hi: return 'pkg-'+key,zh,en
    raise ValueError(ident)

def main():
    catalog=read(DATA/'catalog.json');catalog_map={c['id']:c for c in catalog}
    target={c['id'] for c in catalog if c['category']=='packaging'}
    expected=target-EXISTING
    groups=[read(INPUT/f'group_{g}.json') for g in 'abc']
    enrichment=read(INPUT/'existing_enrichment.json')
    media_add=read(INPUT/'media.json')
    additions=[c for g in groups for c in g['courses']]
    assert len(target)==100 and len(additions)==len(expected)==97
    assert {c['id'] for c in additions}==expected
    assert {c['id'] for c in enrichment['courses']}==EXISTING
    sources={s['id']:s for s in read(DATA/'sources.json')}
    # Keep published source IDs stable. New records pointing to an already
    # indexed URL reuse that record, with every new citation remapped below.
    canonical_urls={}
    for s in sources.values():canonical_urls.setdefault(s['url'],s['id'])
    aliases={}
    for g in groups+[enrichment,media_add]:
        for s in g.get('sources',[]):
            assert s['url'].startswith('https://'),s['id']
            assert s['id'] not in sources or sources[s['id']]['url']==s['url'],s['id']
            if s['id'] not in sources and s['url'] in canonical_urls:
                aliases[s['id']]=canonical_urls[s['url']]
                continue
            s.setdefault('accessed','2026-10-14')
            s.setdefault('imageReuse','Link only; photographs are licensed separately.')
            sources[s['id']]=s
            canonical_urls.setdefault(s['url'],s['id'])
    def remap_citations(value):
        if isinstance(value,list):
            for item in value:remap_citations(item)
        elif isinstance(value,dict):
            if value.get('id') in aliases and value.get('url')==sources[aliases[value['id']]]['url']:
                value['id']=aliases[value['id']]
            for key,item in value.items():
                if key=='sourceIds':value[key]=list(dict.fromkeys(aliases.get(i,i) for i in item))
                elif key=='sourceId' and isinstance(item,str):value[key]=aliases.get(item,item)
                else:remap_citations(item)
    for g in groups+[enrichment,media_add]:remap_citations(g)
    featured=[c for c in read(DATA/'featured.json') if c['id'] not in target]+enrichment['courses']+additions
    assert len(featured)==240 and len({c['id'] for c in featured})==240
    by_id={c['id']:c for c in featured}
    preserved=read(INPUT/'preserved-step-ids.json')
    for ident,ids in preserved.items():
        actual=[s['id'] for stage in by_id[ident]['stages'] for s in stage['steps']]
        assert actual[:len(ids)]==ids,(ident,'existing steps were removed or reordered')
    for c in enrichment['courses']+additions:
        ident=c['id'];assert c['category']=='packaging' and c['title']==catalog_map[ident]['title']
        c.update(kind='course',status='guided',depth=4,languageCoverage=['zh-TW','en'])
        c['subcategory'],c['subcategoryTitle'],c['subcategoryTitleEn']=subcategory(ident)
        c['stepCount']=sum(len(stage['steps']) for stage in c['stages'])
        if ident in expected:
            c['curriculumVersion']=9
            assert c['stepCount']==24 and len(c['stages'])==4 and all(len(st['steps'])==6 for st in c['stages'])
        else:c['enrichmentVersion']=9
        assert len(c['sourceIds'])>=2 and set(c['sourceIds'])<=sources.keys(),ident
        steps=[s for stage in c['stages'] for s in stage['steps']];all_ids={s['id'] for s in steps}
        assert len(all_ids)==len(steps) and len({s['instruction'] for s in steps})==len(steps),ident
        seen=set();sequence=0
        for i,stage in enumerate(c['stages']):
            stage['order']=i+1
            for j,s in enumerate(stage['steps']):
                sequence+=1;s.update(order=j+1,sequence=sequence,simulationOnly=True)
                assert set(s.get('prerequisiteIds',[])) <= (all_ids if ident=='packaging' else seen),s['id']
                seen.add(s['id'])
                for key in ('title','objective','instruction','observation','failure','check'):
                    assert isinstance(s.get(key),str) and s[key].strip() and s.get(key+'En'),(s['id'],key)
                assert s['sourceIds'] and set(s['sourceIds'])<=sources.keys(),s['id']
                assert len(s['knowledge'])>=2
                for k in s['knowledge']:
                    assert all(k.get(field) for field in ('title','titleEn','text','textEn'))
                    assert set(k.get('sourceIds',[]))<=sources.keys(),(s['id'],k.get('id'))
                q=s['quiz'];assert len(q['options'])==len(q['optionsEn'])>=2 and 0<=q['answer']<len(q['options'])
                if ident in expected:assert len(q['options'])==3
        c['estimatedMinutes']=sum(s.get('estimatedMinutes',20) for s in steps)
    places=read(DATA/'course-places.json');place_map={p['courseId']:p for p in places['courses']}
    for g in groups+[enrichment]:
        for p in g.get('places',[]):
            assert p['courseId'] in target and len(p['history'])>=2 and len(p['references'])>=2
            point=p['place'];assert -90<=point['lat']<=90 and -180<=point['lng']<=180
            for key in ('name','nameEn','address','addressEn','coordinateScope','coordinateScopeEn'):
                assert point.get(key),(p['courseId'],key)
            for event in p['history']:
                assert all(event.get(k) for k in ('year','title','titleEn','text','textEn'))
            place_map[p['courseId']]=p
    assert set(place_map)==set(by_id)
    places.update(version=9,courses=list(place_map.values()))
    related=read(DATA/'related-skills.json');related_map={r['courseId']:r for r in related['courses']}
    for g in groups+[enrichment]:
        for r in g.get('related',[]):
            assert r['courseId'] in target and len(r['related'])==2
            related_map[r['courseId']]=r
    assert set(related_map)==set(by_id)
    source_by_url={s['url']:s for s in sources.values()}
    for r in related_map.values():
        r.setdefault('overview','比較相近工法的共同原理、適用差異與驗證方式。')
        r.setdefault('overviewEn','Compare shared principles, applicability and verification across related processes.')
        bibliography={x['url']:x for x in r.get('references',[])}
        for target_id in [r['courseId']]+[x['id'] for x in r['related']]:
            assert target_id in by_id,(r['courseId'],target_id)
            for ref in place_map[target_id]['references']:bibliography.setdefault(ref['url'],copy.deepcopy(ref))
        assert len({item['id'] for item in r['related']})==2
        for item in r['related']:
            target_id=item['id'];assert target_id!=r['courseId']
            item.update(title=by_id[target_id]['title'],titleEn=by_id[target_id]['titleEn'],place=copy.deepcopy(place_map[target_id]['place']))
            item.setdefault('why',item['transfer']);item.setdefault('whyEn',item['transferEn'])
            for key in ('transfer','transferEn','difference','differenceEn'):assert item.get(key),(r['courseId'],key)
            assert len(item['practice'])==len(item['practiceEn'])==3
            item['referenceUrls']=list(dict.fromkeys(item.get('referenceUrls',[])+[x['url'] for x in place_map[target_id]['references']]))
            for url in item['referenceUrls']:
                if url not in bibliography:
                    assert url in source_by_url,(r['courseId'],'missing bibliography',url)
                    bibliography[url]=copy.deepcopy(source_by_url[url])
        for ref in bibliography.values():
            ref.setdefault('titleEn',source_by_url.get(ref['url'],{}).get('titleEn',ref['title']))
            ref.setdefault('scope','公開來源用於比較原理與整合限制；不是廠商完整製程配方。')
            ref.setdefault('scopeEn','Public references support principles and integration boundaries, not full proprietary recipes.')
        r['references']=list(bibliography.values())
    related.update(version=9,courses=list(related_map.values()))
    photos=read(DATA/'photos.json');photo_map={p['id']:p for p in photos}
    for p in media_add['photos']:
        f=ROOT/'public/academy'/p['path'];assert f.is_file()
        assert all(p.get(k) for k in ('license','licenseUrl','sourceUrl','author'))
        if p.get('sha256'):assert hashlib.sha256(f.read_bytes()).hexdigest()==p['sha256'],p['id']
        assert set(p['courseIds'])<=catalog_map.keys(),p['id']
        photo_map[p['id']]=p
    for ident in target:
        candidates=[p for p in media_add['photos'] if ident in p.get('courseIds',[])]
        assert candidates,(ident,'representative image mapping missing')
        chosen=media_add.get('primaryPhotos',{}).get(ident,candidates[0]['id'])
        assert chosen in {p['id'] for p in candidates},(ident,'invalid primary photo')
        by_id[ident]['photoId']=chosen
    media=read(DATA/'media.json');media_map={m['courseId']:m for m in media['courses']}
    for m in media_add.get('media',media_add.get('courses',[])):
        assert m['courseId'] in target
        current=media_map.setdefault(m['courseId'],{'courseId':m['courseId'],'videos':[],'guides':[]})
        for field in ('videos','guides'):
            items={x['id']:x for x in current.get(field,[])};items.update({x['id']:x for x in m.get(field,[])})
            current[field]=list(items.values())
        # Video references belong to the courses that actually use them. Source
        # filtering is not inferred from a shared discipline or publisher.
        for v in m.get('videos',[]):
            url=v.get('sourcePage') or v.get('url')
            if not url or not url.startswith('https://'):continue
            source_id=next((s['id'] for s in sources.values() if s['url']==url),None)
            if not source_id:
                source_id='v9-media-'+hashlib.sha256(url.encode()).hexdigest()[:12]
                sources[source_id]={'id':source_id,'title':v['title'],'titleEn':v.get('titleEn',v['title']),'publisher':v.get('publisher','Original publisher'),'url':url,'scope':v.get('scope','課程引用的官方影片；不代表逐工序實拍。'),'scopeEn':v.get('scopeEn','Official course video, not footage of every lesson step.'),'accessed':'2026-10-14','imageReuse':'External player/link only.'}
            if source_id not in by_id[m['courseId']]['sourceIds']:by_id[m['courseId']]['sourceIds'].append(source_id)
    assert all(i in media_map and (media_map[i].get('videos') or media_map[i].get('guides')) for i in target)
    media.update(version=9,courses=list(media_map.values()))
    catalog=[{k:v for k,v in by_id[c['id']].items() if k!='stages'} if c['id'] in by_id else c for c in catalog]
    for name,value in [('featured',featured),('catalog',catalog),('sources',list(sources.values())),('course-places',places),('related-skills',related),('photos',list(photo_map.values())),('media',media)]:write(DATA/f'{name}.json',value)
    for filename,selection in [('catalog-index.csv',catalog),('packaging-photonics-100.csv',[c for c in catalog if c['id'] in target])]:
        output=io.StringIO(newline='');writer=csv.writer(output,lineterminator='\n')
        writer.writerow(['id','title_zh','title_en','category','subcategory_zh','subcategory_en','content_type','authored_steps','route'])
        for c in selection:writer.writerow([c['id'],c['title'],c['titleEn'],c['category'],c.get('subcategoryTitle',''),c.get('subcategoryTitleEn',''),'guided' if c['id'] in by_id else 'research',c.get('stepCount',0) if c['id'] in by_id else 0,'#project/'+c['id']])
        (DATA/filename).write_text(output.getvalue(),encoding='utf-8-sig')
    steps=[s for c in featured for stage in c['stages'] for s in stage['steps']]
    packaging_steps=[s for c in featured if c['id'] in target for stage in c['stages'] for s in stage['steps']]
    coverage=json.loads(subprocess.check_output(['node','tools/test-process-exercises.mjs'],cwd=ROOT,text=True))
    write(ROOT/'docs/EXERCISE_COVERAGE_V9.json',coverage)
    release=read(DATA/'release.json')
    release.update(version='9.0.0',date='2026-10-14',guidedCourses=240,researchTopics=1760,allSteps=len(steps),knowledgePoints=sum(len(s['knowledge']) for s in steps),sources=len(sources),actualPhotos=len(photo_map),newGuidedCourses=97,newGuidedSteps=sum(c['stepCount'] for c in additions),packagingTopics=100,packagingGuidedCourses=100,packagingSteps=len(packaging_steps),packagingKnowledgePoints=sum(len(s['knowledge']) for s in packaging_steps),packagingSubdisciplines=len({by_id[i]['subcategory'] for i in target}),packagingPhotoCourses=100,packagingMediaCourses=100,packagingLearningRoutes=8,materials=0,courseHistories=len(place_map),mapLocations=len(place_map),curatedRelatedCourses=len(related_map),curatedComparisons=sum(len(r['related']) for r in related_map.values()),curatedRelatedSkills=sum(len(r['related']) for r in related_map.values()),relatedMapLocations=sum(len(r['related']) for r in related_map.values()),mentorDemonstrations=len(steps),narratedGuideSteps=len(steps),videoResources=sum(len(m.get('videos',[])) for m in media['courses']),embeddedVideos=sum(bool(v.get('embedUrl') or v.get('nativeVideoUrl')) for m in media['courses'] for v in m.get('videos',[])),supplementalGuides=sum(len(m.get('guides',[])) for m in media['courses']),authoredInteractiveTasks=coverage['authored'],sharedInteractiveTasks=coverage['shared'],exerciseSceneFamilies=coverage['sceneFamilies'],projectVisualScope='99 semiconductor and 100 packaging/photonics topics have subject-specific original educational diagrams. Licensed photographs remain representative, not actual images of every step.')
    release['uniqueYouTubeVideos']=len({v['embedUrl'].split('/embed/')[1].split('?')[0] for m in media['courses'] for v in m.get('videos',[]) if 'youtube-nocookie.com/embed/' in v.get('embedUrl','')})
    release['relatedReferenceUrls']=len({ref['url'] for r in related_map.values() for ref in r.get('references',[])})
    release['photoAssignments']=sum(bool(s.get('photoId')) for s in steps)
    write(DATA/'release.json',release)
    # One complete attribution file, deterministically rebuilt from shipped media.
    license_text='PHOTOGRAPH ATTRIBUTION / V9\n\n'+ '\n\n'.join(p['id']+'\n'+p.get('attribution',p['author'])+'\nSource: '+p['sourceUrl']+'\nLicense: '+p['license']+' '+p['licenseUrl']+'\nChanges: '+p.get('changes','None') for p in photo_map.values())+'\n'
    (ROOT/'public/academy/assets/photos/LICENSES.txt').write_text(license_text,encoding='utf-8')
    print(json.dumps({k:release[k] for k in ('guidedCourses','packagingGuidedCourses','packagingSteps','allSteps','knowledgePoints','sources','actualPhotos','curatedComparisons','uniqueYouTubeVideos')},ensure_ascii=False))

if __name__=='__main__':main()
