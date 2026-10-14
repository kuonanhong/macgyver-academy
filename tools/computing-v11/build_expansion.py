"""V11 authored world-computing / civil-energy engineering curriculum.

Run: python3 tools/computing-v11/build_expansion.py
Frozen catalog subset, independently authored technical units and primary URLs
are in expansion_inputs.json. No deployment, public-data or Git mutation.
"""
from __future__ import annotations
import copy, json, math, pathlib

P = pathlib.Path(__file__).resolve().parent

def pair(value):
    z, e = value.split('~', 1)
    return z.strip(), e.strip()

def build():
    data = json.loads((P / 'expansion_inputs.json').read_text())
    sources = {s['key']: {k:v for k,v in s.items() if k != 'key'} for s in data['sources']}
    rows = data['projects']
    catalog = {c['id']:c for c in data['catalogSnapshot']}
    assert len(rows) == 80 and len({r['id'] for r in rows}) == 80
    courses=[]; places=[]; related=[]
    by_id={r['id']:r for r in rows}
    for serial, r in enumerate(rows):
        cid=r['id']; z,en=pair(r['title']); f,fe=pair(r['focus'])
        old=catalog.get(cid)
        assert not old or old.get('status') != 'guided', (cid,'already guided')
        c=copy.deepcopy(old or {'id':cid})
        source_ids=[sources[k]['id'] for k in r['sources']]
        definitions=[data['units'][key] for key in r['units']]
        assert len(definitions)==6
        example, example_en=pair(r['example'])
        stages=[]; previous=None
        for si in range(3):
            stage_z,stage_en=pair(data['stageTitles'][si]); steps=[]
            for j in range(4):
                n=si*4+j; u=definitions[n//2]
                uz,ue=pair(u['title']); mechanism,me=pair(u['mechanism']); check,ce=pair(u['verify'])
                anchor,anchor_en=pair(r['anchors'][n//2]); analysis=n%2==0
                sid=f'{cid}-v11-{n+1:02d}'
                title=uz+('：架構分析' if analysis else '：證據驗證')
                title_en=ue+(': architecture analysis' if analysis else ': evidence validation')
                task=(f'在「{z}」的師傅示意與公開來源中，先辨識{anchor}。{mechanism} '
                      f'建立{uz}的輸入、狀態、輸出及邊界圖；本課重點是{f}。用本課假想算例建立基準，再只改一個相關假設，預測哪個輸出先變。{check} 記錄單位、未公開參數及模型失效條件。'
                      if analysis else f'沿用前一步「{uz}」模型，檢查{anchor}的兩個假想案例。{check} 先訂可接受誤差，再比較預測與獨立計算；區分{mechanism}與另一個可能造成相同輸出的機制。保存輸入、殘差、不確定度及採信／保留理由。缺少公開資料就標示尚未驗證，不補造產品數字。')
                task_en=(f'Identify {anchor_en.lower()} in the mentor diagram and primary sources for {en}. {me} '
                         f'Draw the inputs, states, outputs and boundaries of {ue.lower()}, focusing on {fe.lower()}. Establish a baseline with the hypothetical worked example, change one relevant assumption and predict the first affected output. {ce} Record units, undisclosed parameters and model breakdown conditions.'
                         if analysis else f'Use the previous {ue.lower()} model to inspect two hypothetical cases involving {anchor_en.lower()}. {ce} Set acceptable error before comparing predictions with an independent calculation. Distinguish "{me}" from an alternative cause with similar output. Save inputs, residuals, uncertainty and accept/hold reasoning. Mark absent public evidence as unverified rather than inventing product values.')
                wrong_z,wrong_en=pair(u['misconception'])
                answer_z,answer_en=(mechanism,me) if analysis else (check,ce)
                options=[wrong_z,'兩個案例的平均相同，就足以排除空間、時間及模型誤差。']
                options_en=[wrong_en,'Equal case averages rule out spatial, temporal and model errors.']
                answer=n%3;options.insert(answer,answer_z);options_en.insert(answer,answer_en)
                knowledge=[{'id':sid+'-k1','title':uz,'titleEn':ue,'text':mechanism+' 本課架構對應：'+anchor,'textEn':me+' Course architecture correspondence: '+anchor_en,'sourceIds':source_ids},
                           {'id':sid+'-k2','title':'獨立驗證與失效邊界','titleEn':'Independent validation and breakdown boundary','text':check+' 應逐項保留基準與不確定度；'+wrong_z+' 是本單元要排除的誤解。','textEn':ce+' Retain each reference and uncertainty; reject the misconception: '+wrong_en,'sourceIds':source_ids}]
                if n in (0,1,10,11):
                    knowledge.append({'id':sid+'-k3','title':'原創假想量化練習','titleEn':'Original hypothetical quantitative exercise','text':example,'textEn':example_en,'sourceIds':source_ids,'authorship':'original-hypothetical-exercise'})
                steps.append({'id':sid,'order':n+1,'sequence':n+1,'title':title,'titleEn':title_en,'estimatedMinutes':35,'simulationOnly':True,'sourceIds':source_ids,'prerequisiteIds':[previous] if previous else [],'objective':f'針對{anchor}提出可反駁的{uz}模型與驗證紀錄。','objectiveEn':f'Produce a falsifiable {ue.lower()} model and evidence record for {anchor_en.lower()}.','instruction':task,'instructionEn':task_en,'observation':check,'observationEn':ce,'failure':'常見誤判：'+wrong_z,'failureEn':'Common misconception: '+wrong_en,'check':f'提交{anchor}的系統邊界圖、兩案例計算、單位／不確定度表及一項能區分競爭機制的證據。','checkEn':f'Submit a boundary diagram, two-case calculation, units/uncertainty table and discriminating evidence for {anchor_en.lower()}.','knowledge':knowledge,'quiz':{'question':f'就{anchor}的「{uz}」，哪個推論或驗證成立？','questionEn':f'Which inference or check is justified for {ue.lower()} in {anchor_en.lower()}?','options':options,'optionsEn':options_en,'answer':answer,'explanation':mechanism+' '+check,'explanationEn':me+' '+ce}})
                previous=sid
            stages.append({'id':f'{cid}-v11-stage{si+1}','order':si+1,'title':stage_z,'titleEn':stage_en,'description':f'在{z}案例中比較{pair(r["anchors"][si*2])[0]}與{pair(r["anchors"][si*2+1])[0]}，各完成分析及驗證。','descriptionEn':f'Analyze and validate {pair(r["anchors"][si*2])[1].lower()} and {pair(r["anchors"][si*2+1])[1].lower()} within the {en} case.','steps':steps})
        scope,scope_en=pair(data['scopes'][r['family']])
        if r.get('scopeExtra'):
            more,more_en=pair(r['scopeExtra']);scope+=' '+more;scope_en+=' '+more_en
        c.update({'id':cid,'title':z,'titleEn':en,'category':r['category'],'subcategory':r['discipline'],'subcategoryTitle':pair(data['disciplineNames'][r['discipline']])[0],'subcategoryTitleEn':pair(data['disciplineNames'][r['discipline']])[1],'learningTrack':r['track'],'learningSubdiscipline':r['discipline'],'learningTags':[r['track'],r['discipline'],r['slug']], 'kind':'course','status':'guided','contentStatus':'reviewable-educational-curriculum','depth':4,'curriculumVersion':11,'stepCount':12,'estimatedMinutes':420,'simulationOnly':True,'languageCoverage':['zh-TW','en'],'sourceIds':list(dict.fromkeys(c.get('sourceIds',[])+source_ids)),'stages':stages,'summary':f'以{f}解析{z}：六個原理與架構單元、十二項可保存的分析及驗證作業，附假想量化例、來源及衍生工程比較。','summaryEn':f'Explore {en} through {fe.lower()}: six principle/architecture units and twelve saved analysis/validation tasks, with an assumed numerical example, primary sources and related engineering comparisons.','scope':scope,'scopeEn':scope_en,'workedExample':{'title':'原創假想算例與邊界','titleEn':'Original hypothetical example and boundaries','text':example,'textEn':example_en,'assumptions':'數值是本課自行設定的假設，不代表實機量測、產品額定或操作參數；改變模型邊界後必須重算。','assumptionsEn':'Inputs are independently selected assumptions, not measured hardware, ratings or operating parameters; recalculate after boundary changes.','sourceScope':'原創數值練習；來源支援公開架構及領域原理，不宣稱來源提供這組假想數據。','sourceScopeEn':'Original numerical exercise; sources support public architecture and principles, not these assumed measurements.'},'diagram':{'type':r['diagram'],'labels':[pair(a)[0] for a in r['anchors']],'labelsEn':[pair(a)[1] for a in r['anchors']],'original':True,'notToScale':True},'vendorHints':[{'name':sources[k]['publisher'],'nameEn':sources[k]['publisher'],'url':sources[k]['url'],'role':'官方工程或研究資料；不表示背書、授課或本平臺能訪問其設備。','roleEn':'Official engineering/research reference; no endorsement, teaching partnership or hardware access is implied.','sourceIds':[sources[k]['id']]} for k in r['sources'][:2]]})
        courses.append(c)
        c['architectureNodes']=copy.deepcopy(r['architectureNodes'])
        c['architectureEdges']=copy.deepcopy(r['architectureEdges'])
        c['architectureFamily']=r['architectureFamily']
        c['learningTags']=list(dict.fromkeys(c['learningTags']+r.get('extraLearningTags',[])))
        loc=r['place'];name,name_en=pair(loc['name']);history,history_en=pair(r['history'])
        refs=[{k:sources[s][k] for k in ['title','titleEn','publisher','url']} for s in r['sources']]
        pl={'name':name,'nameEn':name_en,'city':name,'cityEn':name_en,'country':pair(loc['country'])[0],'countryEn':pair(loc['country'])[1],'lat':loc['lat'],'lng':loc['lng'],'address':loc['query'],'addressEn':loc['query'],'mapQuery':loc['query'],'coordinateScope':'人工選定的公開城市、研究機構或工程區域之近似代表座標；非設備定位、施工入口或參訪許可。模型及晶片課程的機構座標不代表實際製造地。','coordinateScopeEn':'Manually selected approximate public city/institution/project-region reference, not equipment coordinates, an access point or a visit permit. An institution marker for a model/chip does not imply its fabrication site.'}
        places.append({'courseId':cid,'place':pl,'summary':f'{z}以{f}連結科學、系統設計與驗收。','summaryEn':f'{en} connects science, system design and validation through {fe.lower()}.','connection':f'從{pair(r["anchors"][0])[0]}追蹤到{pair(r["anchors"][-1])[0]}；地圖提供公開案例的地理脈絡。','connectionEn':f'Trace {pair(r["anchors"][0])[1].lower()} to {pair(r["anchors"][-1])[1].lower()}; the map supplies public-case geographical context.','history':[{'year':'公開工程脈絡 / Public engineering context','title':z,'titleEn':en,'text':history,'textEn':history_en,'sourceIds':source_ids},{'year':'學習延伸 / Learning transfer','title':'從工程故事到可檢查模型','titleEn':'From engineering story to reviewable models','text':f'本課將{f}改寫為原創離線分析題；不複製來源的製造圖、影片逐字稿或現場程序。','textEn':f'The course turns {fe.lower()} into original offline analysis exercises without copying manufacturing drawings, video transcripts or field procedures.','sourceIds':source_ids}],'references':refs,'sourceIds':source_ids})
        rs=[]
        for tid in r['related']:
            t=by_id[tid];tz,te=pair(t['title']);tf,tfe=pair(t['focus']);shared,shared_en=pair(data['transfers'][r['family']])
            diff=f'本課針對{f}；{tz}改以{tf}為架構重點，不能直接沿用幾何、邊界或產品數值。';diff_en=f'This course focuses on {fe.lower()}; {te} centers on {tfe.lower()}, so geometry, boundaries and product values cannot transfer unchanged.'
            rs.append({'id':tid,'title':tz,'titleEn':te,'why':shared,'whyEn':shared_en,'transfer':shared,'transferEn':shared_en,'difference':diff,'differenceEn':diff_en,'practice':[f'對照{pair(r["anchors"][0])[0]}與{pair(t["anchors"][0])[0]}，重畫兩項工程的輸入及系統邊界。',f'把本課假想算例移到{tz}，列出可沿用的方程與必須重設的參數。',f'以{pair(r["anchors"][-1])[0]}為起點，設計一項能區分「{f}」與「{tf}」的觀測，註明不確定度。'],'practiceEn':[f'Compare {pair(r["anchors"][0])[1].lower()} with {pair(t["anchors"][0])[1].lower()} and redraw inputs and boundaries.',f'Transfer the assumed example to {te}, separating reusable equations from respecified parameters.',f'Start from {pair(r["anchors"][-1])[1].lower()} and propose an observation distinguishing {fe.lower()} from {tfe.lower()}, including uncertainty.'],'referenceUrls':[sources[k]['url'] for k in r['sources']]})
        assert len(rs)==2 and len({x['id'] for x in rs})==2 and cid not in {x['id'] for x in rs}
        related.append({'courseId':cid,'overview':'以可遷移原理比較架構差異；關聯不表示同一廠商、世代或驗收規格。','overviewEn':'Compare architecture differences through transferable principles; a link does not imply the same vendor, generation or acceptance requirements.','related':rs,'references':refs})
    output={'version':11,'authorship':'Original bilingual educational models and assumed exercises; primary sources linked, not reproduced.','courses':courses,'sources':list(sources.values()),'places':places,'related':related,'enrichmentRequests':data.get('enrichmentRequests',[]),'coverage':data['coverage']}
    (P/'expansion.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
    summary={'courses':len(courses),'steps':sum(c['stepCount'] for c in courses),'knowledgeRecords':sum(len(s['knowledge']) for c in courses for st in c['stages'] for s in st['steps']),'sources':len(sources),'places':len(places),'relatedComparisons':len(related)*2,'existingRoadmapsGuided':sum(r['id'] in catalog for r in rows),'newIds':sum(r['id'] not in catalog for r in rows),'enrichmentRequests':len(output['enrichmentRequests'])}
    print(json.dumps(summary,ensure_ascii=False))
    return output

if __name__=='__main__':
    build()
