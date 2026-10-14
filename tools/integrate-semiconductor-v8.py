#!/usr/bin/env python3
"""Merge source-reviewed semiconductor learning packages without renumbering old lessons."""
import copy
import csv
import hashlib
import io
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT/'public/academy/data'
INPUT = ROOT/'tools/semiconductor-v8'
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def write(p, value): p.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n',encoding='utf-8')
def subcategory(ident):
    if ident=='semiconductor': return ('integration','整合流程','Process integration')
    if ident=='sub2nm': return ('devices','先進電晶體','Advanced transistors')
    n=int(ident[1:])
    for lo,hi,key,zh,en in [(3,6,'substrate','晶圓與基板','Wafers and substrates'),(7,10,'fab','廠務與搬運','Fab infrastructure'),(11,20,'feol','前段材料與接面','FEOL materials and junctions'),(21,30,'devices','先進電晶體','Advanced transistors'),(31,50,'lithography','光阻、光罩與微影','Resists, masks and lithography'),(51,56,'etch','蝕刻與電漿','Etch and plasma'),(57,60,'deposition','薄膜沉積','Thin-film deposition'),(61,70,'interconnect','互連、平坦化與可靠度','Interconnect, planarization and reliability'),(71,77,'memory','記憶體','Memory'),(78,80,'sensors','影像與光子感測','Image and photon sensors'),(81,87,'compound','化合物與新材料元件','Compound and emerging devices'),(88,90,'mems','微機電與顯示','MEMS and displays'),(91,97,'metrology','量測、良率與控制','Metrology, yield and control'),(98,99,'fab','廠務與搬運','Fab infrastructure')]:
        if lo<=n<=hi:return key,zh,en
    raise ValueError(ident)
def main():
    catalog=read(DATA/'catalog.json');catalog_map={c['id']:c for c in catalog}
    groups=[read(INPUT/f'group_{g}.json') for g in 'abc']
    if (INPUT/'group_c_related.json').exists():
        groups[2]['related']=read(INPUT/'group_c_related.json')['related']
    additions=[c for g in groups for c in g['courses']]
    existing_semi={'semiconductor','sub2nm','a004','a025','a042'}
    expected={c['id'] for c in catalog if c['category']=='semiconductor'}-existing_semi
    assert len(expected)==94 and len(additions)==94 and {c['id'] for c in additions}==expected
    sources={s['id']:s for s in read(DATA/'sources.json')}
    for g in groups:
        for s in g['sources']:
            assert s['url'].startswith('https://'),s['id']
            assert s['id'] not in sources or sources[s['id']]['url']==s['url'],s['id']
            s.setdefault('accessed','2026-10-14');s.setdefault('imageReuse','Link only; photographs are licensed separately.')
            sources[s['id']]=s
    for c in additions:
        assert c['category']=='semiconductor' and c['title']==catalog_map[c['id']]['title'],c['id']
        c.update(kind='course',status='guided',curriculumVersion=8,depth=4,stepCount=24,languageCoverage=['zh-TW','en'])
        assert len(c['stages'])==4 and all(len(g['steps'])==6 for g in c['stages']),c['id']
        steps=[s for stage in c['stages'] for s in stage['steps']];seen=set()
        assert len({s['instruction'] for s in steps})==24,c['id']
        assert len(c['sourceIds'])>=2 and set(c['sourceIds'])<=sources.keys(),c['id']
        for i,stage in enumerate(c['stages']):
            stage['order']=i+1
            for j,s in enumerate(stage['steps']):
                assert s['id'] not in seen and set(s.get('prerequisiteIds',[]))<=seen,s['id']
                seen.add(s['id']);s.update(order=j+1,sequence=i*6+j+1,simulationOnly=True)
                for key in ('title','objective','instruction','observation','failure','check'):
                    assert isinstance(s.get(key),str) and s[key].strip() and s.get(key+'En'),(s['id'],key)
                assert s['sourceIds'] and set(s['sourceIds'])<=sources.keys(),s['id']
                assert len(s['knowledge'])>=2 and all(k.get('text') and k.get('textEn') and k.get('title') and k.get('titleEn') for k in s['knowledge'])
                q=s['quiz'];assert len(q['options'])==len(q['optionsEn'])==3 and q['answer'] in (0,1,2)
    featured=[c for c in read(DATA/'featured.json') if c['id'] not in expected]+additions
    assert len(featured)==143
    by_id={c['id']:c for c in featured}
    for c in featured:
        if c['category']=='semiconductor': c['subcategory'],c['subcategoryTitle'],c['subcategoryTitleEn']=subcategory(c['id'])
    catalog=[{k:v for k,v in by_id[c['id']].items() if k!='stages'} if c['id'] in by_id else c for c in catalog]
    assert sum(c['category']=='semiconductor' for c in featured)==99
    places=read(DATA/'course-places.json');place_map={p['courseId']:p for p in places['courses']}
    for g in groups:
        for p in g['places']:
            assert p['courseId'] in expected and len(p['history'])>=2 and len(p['references'])>=2
            point=p['place'];assert -90<=point['lat']<=90 and -180<=point['lng']<=180
            for key in ('name','nameEn','address','addressEn','coordinateScope','coordinateScopeEn'):assert point.get(key),(p['courseId'],key)
            place_map[p['courseId']]=p
    assert set(place_map)==set(by_id)
    places.update(version=8,courses=list(place_map.values()))
    related=read(DATA/'related-skills.json');related_map={r['courseId']:r for r in related['courses']}
    for g in groups:
        for r in g['related']:
            assert r['courseId'] in expected and len(r['related'])>=2
            r.setdefault('overview','比較相近工法的共同原理、適用差異與驗證方式。')
            r.setdefault('overviewEn','Compare shared principles, applicability and verification across related processes.')
            for item in r['related']:
                target=item['id'];assert target in by_id and target!=r['courseId']
                item.update(title=by_id[target]['title'],titleEn=by_id[target]['titleEn'],place=copy.deepcopy(place_map[target]['place']))
                item.setdefault('why',item['transfer']);item.setdefault('whyEn',item['transferEn'])
                for key in ('transfer','transferEn','difference','differenceEn'):assert item.get(key)
                assert len(item['practice'])==len(item['practiceEn'])>=3
                item['referenceUrls']=list(dict.fromkeys(item.get('referenceUrls',[])+[x['url'] for x in place_map[target]['references']]))
            bibliography={x['url']:x for x in r.get('references',[])}
            for target in [r['courseId']]+[x['id'] for x in r['related']]:
                for ref in place_map[target]['references']:
                    bibliography.setdefault(ref['url'],copy.deepcopy(ref))
            source_by_url={ref['url']:ref for ref in sources.values()}
            for item in r['related']:
                for url in item['referenceUrls']:
                    if url not in bibliography:
                        assert url in source_by_url,(r['courseId'],'missing bibliography',url)
                        bibliography[url]=copy.deepcopy(source_by_url[url])
            for ref in bibliography.values():
                ref.setdefault('scope','公開機構資料；用於比較共同原理、應用情境與差異，不代表製造配方。')
                ref.setdefault('scopeEn','Public institutional information for comparing principles, applications and differences, not fabrication recipes.')
            r['references']=list(bibliography.values())
            related_map[r['courseId']]=r
    assert set(related_map)==set(by_id)
    related.update(version=8,courses=list(related_map.values()))
    photos=read(DATA/'photos.json');photo_map={p['id']:p for p in photos}
    media=read(DATA/'media.json');media_map={m['courseId']:m for m in media['courses']}
    supplement=read(INPUT/'media.json') if (INPUT/'media.json').exists() else {'photos':[],'courses':[]}
    for p in supplement['photos']:
        f=ROOT/'public/academy'/p['path'];assert f.is_file() and p['license'] and p['licenseUrl'] and p['sourceUrl'] and p['author']
        if p.get('sha256'):assert hashlib.sha256(f.read_bytes()).hexdigest()==p['sha256']
        photo_map[p['id']]=p
    for m in supplement.get('courses',[]):
        assert m['courseId'] in by_id
        current=media_map.setdefault(m['courseId'],{'courseId':m['courseId'],'videos':[],'guides':[]})
        for field in ('videos','guides'):
            items={x['id']:x for x in current.get(field,[])};items.update({x['id']:x for x in m.get(field,[])})
            current[field]=list(items.values())
    media['courses']=list(media_map.values());media['version']=8
    for name,value in [('featured',featured),('catalog',catalog),('sources',list(sources.values())),('course-places',places),('related-skills',related),('photos',list(photo_map.values())),('media',media)]:write(DATA/f'{name}.json',value)
    output=io.StringIO(newline='');writer=csv.writer(output,lineterminator='\n')
    writer.writerow(['id','title_zh','title_en','category','content_type','authored_steps','research_checkpoints','route'])
    for c in catalog:
        ready=c['id'] in by_id;writer.writerow([c['id'],c['title'],c['titleEn'],c['category'],'guided' if ready else 'research',c.get('stepCount',0) if ready else 0,0 if ready else 8,'#project/'+c['id']])
    (DATA/'catalog-index.csv').write_text(output.getvalue(),encoding='utf-8-sig')
    steps=[s for c in featured for stage in c['stages'] for s in stage['steps']]
    assert len(steps)==4106
    coverage=json.loads(subprocess.check_output(['node','tools/test-process-exercises.mjs'],cwd=ROOT,text=True))
    write(ROOT/'docs/EXERCISE_COVERAGE_V8.json',coverage)
    release=read(DATA/'release.json')
    release.update(aiRoutesScope='Browser CPU text; optional native CPU text/vision and server-side Gemini text/image with explicit per-request cloud consent. No weights or private keys bundled.',version='8.1.0',date='2026-10-14',guidedCourses=143,researchTopics=1857,allSteps=len(steps),knowledgePoints=sum(len(s['knowledge']) for s in steps),sources=len(sources),actualPhotos=len(photo_map),newGuidedCourses=94,newGuidedSteps=2256,semiconductorTopics=99,semiconductorGuidedCourses=99,materials=0,courseHistories=len(place_map),mapLocations=len(place_map),curatedRelatedCourses=len(related_map),curatedComparisons=sum(len(r['related']) for r in related_map.values()),curatedRelatedSkills=sum(len(r['related']) for r in related_map.values()),relatedMapLocations=sum(len(r['related']) for r in related_map.values()),mentorDemonstrations=len(steps),narratedGuideSteps=len(steps),videoResources=sum(len(m.get('videos',[])) for m in media['courses']),embeddedVideos=sum(bool(v.get('youtubeId')) for m in media['courses'] for v in m.get('videos',[])),supplementalGuides=sum(len(m.get('guides',[])) for m in media['courses']),authoredInteractiveTasks=coverage['authored'],sharedInteractiveTasks=coverage['shared'],exerciseSceneFamilies=coverage['sceneFamilies'],comparisonScope='Each guided course has authored comparisons and representative map points. Repeated institutions are not distinct fabrication sites.',projectVisualScope='99 semiconductor topics have subject-labeled original architecture diagrams. Photographs remain licensed representative images, not a separate photo for every step.',aiScope='Optional consent-based local CPU generation; models download separately. Cloud accounts require Supabase configuration; local profiles work without it.')
    release['embeddedVideos']=sum(bool(v.get('embedUrl') or v.get('nativeVideoUrl')) for m in media['courses'] for v in m.get('videos',[]))
    release['semiconductorSubdisciplines']=len({c['subcategory'] for c in featured if c['category']=='semiconductor'})
    release['semiconductorPhotoCourses']=sum(any(c['id'] in p.get('courseIds',[]) for p in photo_map.values()) for c in featured if c['category']=='semiconductor')
    release['uniqueYouTubeVideos']=len({v['embedUrl'].split('/embed/')[1].split('?')[0] for m in media['courses'] for v in m.get('videos',[]) if 'youtube-nocookie.com/embed/' in v.get('embedUrl','')})
    release['relatedReferenceUrls']=len({ref['url'] for r in related_map.values() for ref in r.get('references',[])})
    write(DATA/'release.json',release)
    print(json.dumps({k:release[k] for k in ('guidedCourses','semiconductorGuidedCourses','allSteps','knowledgePoints','sources','actualPhotos','curatedComparisons')},ensure_ascii=False))
if __name__=='__main__':main()
