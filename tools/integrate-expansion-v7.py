#!/usr/bin/env python3
"""Integrate reviewed V7 lessons without changing existing course/step IDs."""
import csv
import io
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'public/academy/data'
GROUPS = ('civil', 'technology', 'science')
EXPECTED_IDS = {'b015','b021','b103','b226','a025','a042','a211','a319','c005','c325','d036','d202'}
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def write(p,v): p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def main():
    catalog=read(DATA/'catalog.json'); original={c['id']:c for c in catalog}
    groups=[read(ROOT/'tools/expansion-v7'/f'{g}.json') for g in GROUPS]
    additions=[c for g in groups for c in g['courses']]
    assert {c['id'] for c in additions}==EXPECTED_IDS and len(additions)==12
    sources={s['id']:s for s in read(DATA/'sources.json')}
    for g in groups:
        for s in g['sources']:
            assert s['url'].startswith('https://'),s['id']
            if s['id'] in sources: assert sources[s['id']]['url']==s['url']
            s.setdefault('accessed','2026-10-13')
            s.setdefault('imageReuse','Link only; source images are not redistributed.')
            sources[s['id']]=s
    for course in additions:
        ident=course['id']; assert course['category']==original[ident]['category'],ident
        course.update(status='guided',kind='course',depth=4,contentStatus='reviewable-educational-curriculum',languageCoverage=['zh-TW','en'],curriculumVersion=7)
        stages=course['stages']; steps=[s for g in stages for s in g['steps']]
        assert len(stages)==4 and all(len(g['steps'])==6 for g in stages) and len(steps)==24,ident
        seen=set()
        assert len({s['instruction'] for s in steps})==24
        for k in ('title','summary','scope'):
            assert course.get(k) and course.get(k+'En'),(ident,k)
        for i,stage in enumerate(stages):
            stage['order']=i+1
            assert stage.get('title') and stage.get('titleEn'),(ident,'stage title')
            for j,s in enumerate(stage['steps']):
                assert s['id'] not in seen
                assert set(s.get('prerequisiteIds',[]))<=seen,(s['id'],'prerequisites')
                seen.add(s['id']); s['sequence']=i*6+j+1; s['order']=j+1
                for k in ('title','objective','instruction','observation','failure','check'):
                    assert s.get(k) and s.get(k+'En'),(s['id'],k)
                assert s['simulationOnly'] is True
                assert len(s['knowledge'])>=2
                for k in s['knowledge']:
                    assert all(k.get(field) for field in ('title','titleEn','text','textEn'))
                assert s['sourceIds'] and set(s['sourceIds'])<=sources.keys()
                q=s['quiz']; assert len(q['options'])==len(q['optionsEn'])==3 and 0<=q['answer']<3
        assert set(course['sourceIds'])<=sources.keys()
        course['stepCount']=24
        course['estimatedMinutes']=sum(s.get('estimatedMinutes',20) for s in steps)
    featured=[c for c in read(DATA/'featured.json') if c['id'] not in EXPECTED_IDS and c.get('curriculumVersion',0)<8]+additions
    assert len(featured)==49
    by_id={c['id']:c for c in featured}
    catalog=[{k:v for k,v in by_id[c['id']].items() if k!='stages'} if c['id'] in by_id else c for c in catalog]
    for k in ('id','title','titleEn'): assert len({c[k].casefold() for c in catalog})==2000,k
    places=read(DATA/'course-places.json')
    places['courses']=[p for p in places['courses'] if p['courseId'] not in EXPECTED_IDS]+[p for g in groups for p in g['places']]
    assert len(places['courses'])==49 and {p['courseId'] for p in places['courses']}==by_id.keys()
    places['version']=7
    for p in places['courses']:
        assert -90<=p['place']['lat']<=90 and -180<=p['place']['lng']<=180
        assert len(p['history'])>=2 and len(p['references'])>=2,p['courseId']
    for name,value in [('featured',featured),('catalog',catalog),('sources',list(sources.values())),('course-places',places)]:write(DATA/f'{name}.json',value)
    (DATA/'materials.json').unlink(missing_ok=True)
    photos=read(DATA/'photos.json')
    for p in photos:
        if p['id']=='webb' and 'c325' not in p['courseIds']: p['courseIds'].append('c325')
    write(DATA/'photos.json',photos)
    coverage=json.loads(subprocess.check_output(['node','tools/test-process-exercises.mjs'],cwd=ROOT,text=True))
    write(ROOT/'docs/EXERCISE_COVERAGE_V7.json',coverage)
    steps=[s for c in featured for g in c['stages'] for s in g['steps']]
    release=read(DATA/'release.json')
    release.update(version='7.0.0',date='2026-10-13',guidedCourses=49,researchTopics=1951,
        allSteps=len(steps),knowledgePoints=sum(len(s['knowledge']) for s in steps),sources=len(sources),
        courseHistories=49,mapLocations=49,materials=0,newGuidedCourses=12,newGuidedSteps=288,
        mentorDemonstrations=len(steps),narratedGuideSteps=len(steps),
        authoredInteractiveTasks=coverage['authored'],sharedInteractiveTasks=coverage['shared'],exerciseSceneFamilies=coverage['sceneFamilies'],
        projectVisualScope='All 2000 topics have stable ID-coded icons and category-based original catalog illustrations; the 49 guided courses have subject-specific silhouettes. Licensed photos remain clearly attributed. Illustrations are not site photography or CAD.',
        sourceVisibility='User-provided course-material index removed from the released site and offline data.')
    write(DATA/'release.json',release)
    output=io.StringIO(newline=''); writer=csv.writer(output)
    writer.writerow(['id','title_zh','title_en','category','content_type','authored_steps','research_checkpoints','route'])
    for c in catalog:
        ready=c['id'] in by_id
        row=[c['id'],c['title'],c['titleEn'],c['category'],'guided' if ready else 'research',c.get('stepCount',0) if ready else 0,0 if ready else 8,'#project/'+c['id']]
        writer.writerow(["'"+v if isinstance(v,str) and v.startswith(('=','+','-','@')) else v for v in row])
    (DATA/'catalog-index.csv').write_text(output.getvalue(),encoding='utf-8-sig')
    print(json.dumps({k:release[k] for k in ('guidedCourses','researchTopics','allSteps','knowledgePoints','sources')},ensure_ascii=False))
if __name__=='__main__':main()
