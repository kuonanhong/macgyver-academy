#!/usr/bin/env python3
"""Compile authored V7 comparison lessons after the 49-course merge.

No geocoding and no invented location: every comparison inherits its destination
course's reviewed representative point. Broad research topics remain unlocated.
"""
import argparse
import copy
import json
from pathlib import Path
from urllib.parse import urlparse

ROOT=Path(__file__).resolve().parents[1]
def read(path): return json.loads(path.read_text(encoding='utf-8'))
def write(path,value): path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def safe_url(url):
    parsed=urlparse(url or '')
    return parsed.scheme=='https' and bool(parsed.hostname) and not parsed.username and not parsed.password

def compile_relations(data_dir):
    authored=read(ROOT/'tools/expansion-v7/relations.json')
    featured=read(data_dir/'featured.json')
    courses={c['id']:c for c in featured}
    source_by_id={s['id']:s for s in read(data_dir/'sources.json')}
    places_data=read(data_dir/'course-places.json')
    places={p['courseId']:p for p in places_data['courses']}
    assert set(courses)==set(authored['map'])==set(places), 'Run the V7 course/place merge first'
    pairs={tuple(sorted(p['ids'])):p for p in authored['pairs']}
    assert len(courses)==49 and len(pairs)==62
    # Two entries refer to the same documented campus; use the existing base point.
    if places['a310']['place']['mapQuery'].startswith('NIST'):
        for axis in ('lat','lng'):
            places['a310']['place'][axis]=places['cybersecurity']['place'][axis]
    for entry in places.values():
        p=entry['place']
        assert -90<=p['lat']<=90 and -180<=p['lng']<=180
        assert p.get('mapQuery') and p.get('name') and p.get('nameEn')
        # A campus/city/bridge descriptor is not presented as an exact postal address.
        p.setdefault('address',p['mapQuery'])
        p.setdefault('addressEn',p.get('addressEn') or p['mapQuery'])
        p.setdefault('coordinateScope','公開代表定位點，座標為近似值；依地點可能是工程、園區、博物館、入口或城市，並非整體工程邊界。')
        p.setdefault('coordinateScopeEn','Approximate public reference point: a project, campus, museum, entrance or city depending on the entry, not the boundary of the entire project.')
    def refs_for(ident):
        c=courses[ident]
        candidates=[source_by_id[s] for s in c.get('sourceIds',[])[:4] if s in source_by_id]
        candidates+=authored.get('extraReferences',{}).get(ident,[])
        candidates+=places[ident]['references']
        result=[]; seen=set()
        for ref in candidates:
            url=ref.get('url','')
            if not safe_url(url) or url in seen: continue
            seen.add(url)
            result.append(dict(url=url,title=ref.get('title') or url,titleEn=ref.get('titleEn') or ref.get('title') or url,
                publisher=ref.get('publisher') or urlparse(url).hostname,
                scope=ref.get('scope') or f'支持「{c["title"]}」的工程背景或代表地點；跨專案比較為原創教學整理。',
                scopeEn=ref.get('scopeEn') or f'Public engineering or location reference for {c["titleEn"]}; the cross-project comparison is original educational synthesis.'))
        assert len(result)>=2,(ident,'references')
        return result
    compiled=[]
    for ident,targets in authored['map'].items():
        c=courses[ident]; bibliography={}; comparisons=[]
        assert len(targets)==len(set(targets))==2
        for target in targets:
            assert target!=ident and target in courses
            p=pairs[tuple(sorted((ident,target)))]; dest=courses[target]
            for key in ('transfer','transferEn','difference','differenceEn'):
                assert isinstance(p[key],str) and p[key].strip(),(ident,target,key)
            assert len(p['practice'])==len(p['practiceEn'])==3
            references=refs_for(ident)+refs_for(target)
            item=dict(id=target,title=dest['title'],titleEn=dest['titleEn'],
                why=f'把「{c["title"]}」與「{dest["title"]}」對照，先辨認能沿用的原理，再檢查不能直接移植的設計條件。',
                whyEn=f'Compare {c["titleEn"]} with {dest["titleEn"]}: identify transferable principles, then check design conditions that cannot be transferred directly.',
                place=copy.deepcopy(places[target]['place']),
                referenceUrls=list(dict.fromkeys(r['url'] for r in references)))
            for key in ('transfer','transferEn','difference','differenceEn','practice','practiceEn'): item[key]=p[key]
            comparisons.append(item)
            for ref in references: bibliography[ref['url']]=ref
        compiled.append(dict(courseId=ident,
            overview=f'從「{c["title"]}」延伸到兩項可直接開啟的逐步課程；下列比較分別說明相似原理、差異與驗證練習，並附代表地點、地址或地理描述與近似座標。',
            overviewEn=f'Extend {c["titleEn"]} into two directly accessible guided courses. Each comparison identifies shared principles, differences and verification exercises, with a representative location, address or geographical descriptor and approximate coordinates.',
            related=comparisons,references=list(bibliography.values())))
    result=dict(version=7,courses=compiled,scope=authored['editorialScope'],scopeEn=authored['editorialScopeEn'])
    places_data['version']=7
    write(data_dir/'course-places.json',places_data)
    write(data_dir/'related-skills.json',result)
    release_path=data_dir/'release.json'
    if release_path.exists():
        release=read(release_path)
        release.update(curatedRelatedCourses=49,curatedComparisons=98,curatedRelatedSkills=98,relatedMapLocations=98,
            relatedReferenceUrls=len({ref['url'] for c in compiled for ref in c['references']}),
            comparisonScope='49 guided courses each have two authored comparisons with other guided courses, using 49 reviewed representative places; 98 links do not mean 98 distinct locations.')
        write(release_path,release)
    return {'guidedCourses':len(compiled),'comparisons':sum(len(c['related']) for c in compiled),'uniquePlaces':len(places),'authoredPairLessons':len(pairs)}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data-dir',type=Path,default=ROOT/'public/academy/data')
    args=parser.parse_args()
    print(json.dumps(compile_relations(args.data_dir),ensure_ascii=False))
