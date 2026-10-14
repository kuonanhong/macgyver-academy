#!/usr/bin/env python3
"""Rebuild 32 courses from immutable title snapshot and independently authored units.
Run: python tools/electronics-v10/build_group_c.py
Only writes group_c.json and review_group_c.json in this directory.
"""
import json, hashlib
from pathlib import Path
from core_c import COURSES
from metadata_c import SOURCES, PLACES, VENDORS, RELATIONS
ROOT=Path(__file__).resolve().parent
TITLES={x['id']:x for x in json.loads((ROOT/'catalog_titles_c.json').read_text())}

def bilingual(d,key,zh,en):
    d[key]=zh;d[key+'En']=en
    return d

def source_ids(c):return [SOURCES[k]['id'] for k in c['sourceKeys']]
def refs(c):return [{k:SOURCES[s][k] for k in ('title','titleEn','publisher','url')} for s in c['sourceKeys']]

def make_course(c,index):
    base=TITLES[c['id']];cid=c['id'];ids=source_ids(c)
    course={**base,'category':'electronics','status':'guided','contentStatus':'reviewable-educational-curriculum','curriculumVersion':10,'depth':4,'stepCount':24,'estimatedMinutes':840,'simulationOnly':True,'languageCoverage':['zh-TW','en'],'sourceIds':ids}
    bilingual(course,'summary',f"以 4 階段、24 項作業探究{c['lens']}；每個技術單元分為模型與判別，包含計算、失效機制、可保存的工程證據與知識測驗。",f"Four stages and 24 work packages investigate {c['lensEn']}. Each technical unit pairs modeling with diagnosis, calculations, failure mechanisms, saveable evidence and a knowledge check.")
    bilingual(course,'scope','公開原理與案例資料判讀課。教學示意、算例和操作是工程模型，不是供應商配方、現場施工或帶電操作程序；實際設計須由合格專業人員依適用標準與實測條件審查。','Public-principle and case-data interpretation course. Diagrams, examples and operations are engineering models, not vendor recipes, construction instructions or energized procedures. Actual design needs qualified review against applicable standards and measured conditions.')
    course['subcategory']='power-integrity' if int(cid[1:])<271 else 'analog-rf' if int(cid[1:])<=280 else 'pcb-assembly-reliability' if int(cid[1:])<=290 else 'display-sensing' if int(cid[1:])<=297 else 'hvdc-case-studies'
    course['workedExample']={'title':'可重算的工程算例','titleEn':'Reproducible engineering example','text':c['example'][0],'textEn':c['example'][1],'assumptions':c['bounds'][0],'assumptionsEn':c['bounds'][1],'sourceScope':'2019 年公告的端口額定核算；不表示今日可用容量。' if cid=='a298' else '自行設定的假想算例；來源支援原理，不提供此組假想輸入。','sourceScopeEn':'Terminal-rating calculation from the 2019 announcement; not current availability.' if cid=='a298' else 'Independently chosen hypothetical inputs; references support principles, not these assumed inputs.'}
    course['diagram']={'type':'electronics','labels':[x[0] for x in c['stages']],'labelsEn':[x[1] for x in c['stages']],'original':True,'notToScale':True}
    v=VENDORS[c['vendorKey']]
    vh={'name':v[0],'nameEn':v[1],'url':v[2],'role':v[3],'roleEn':v[4],'sourceIds':ids,'productUrl':next((SOURCES[k]['url'] for k in c['sourceKeys'] if v[1].lower() in SOURCES[k]['publisher'].lower()),v[2])}
    if v[5]:vh.update(ticker=v[5],exchange=v[6])
    course['vendorHints']=[vh]
    course['stages']=[];previous=None
    for si,(stagezh,stageen) in enumerate(c['stages']):
        stage={'id':f'{cid}-stage{si+1:02d}','order':si+1,'title':stagezh,'titleEn':stageen,'description':f'以三個技術單元逐一建立「{stagezh}」的模型和可反駁的驗證證據。','descriptionEn':f'Three technical units build models and falsifiable verification evidence for {stageen.lower()}.','steps':[]}
        for ui in range(si*3,si*3+3):
            title,en,principle,principle_en,diagnosis,diagnosis_en,wrong,wrong_en=c['units'][ui]
            for phase in range(2):
                seq=ui*2+phase+1;sid=f'{cid}-v10-{seq:02d}'
                step={'id':sid,'order':seq,'sequence':seq,'estimatedMinutes':35,'simulationOnly':True,'sourceIds':ids,'prerequisiteIds':[previous] if previous else []}
                bilingual(step,'title',title+('：模型與設計' if phase==0 else '：量測與判別'),en+(': model and design' if phase==0 else ': measurement and diagnosis'))
                bilingual(step,'objective',f"以「{title}」{'建立可檢驗的模型，明確標出座標、變數、單位和有效邊界。' if phase==0 else '區分可能失效機制，提出可追溯的判讀與交付證據。'}",f"{'Build a testable model for' if phase==0 else 'Discriminate failure mechanisms in'} {en.lower()}, {'stating coordinates, variables, units and validity bounds.' if phase==0 else 'with traceable interpretation and evidence.'}")
                if phase==0:
                    bilingual(step,'instruction',f'先觀看師傅的概念示範，再排列本單元的元件、能量或資料路徑。{principle} 畫出基準與改變一個參數後的兩個狀態；用「{diagnosis}」提出可被推翻的預測。另列未量測條件，勿把動畫位置當真實尺寸。',f'Watch the mentor concept demonstration, then arrange this unit’s components, energy or data paths. {principle_en} Draw baseline and one-parameter-changed states. Form a falsifiable prediction using: {diagnosis_en} List unmeasured conditions; animation positions are not physical dimensions.')
                    bilingual(step,'check',f'提交「{title}」兩狀態圖、變數單位表和預期差異；以本步判別方法說明何種結果會推翻模型。',f'Submit two states, a variable/unit table and predicted differences for {en.lower()}; specify which diagnostic result would falsify the model.')
                else:
                    bilingual(step,'instruction',f'保留前一步模型，檢查它能否解釋觀察。{diagnosis} 記錄原始量、基準、重複性與單位；比較正確機制「{principle}」和待排除假說「{wrong}」。最後作出接受、重測或修正模型的決定，並列出資料不能支持的結論。',f'Retain the preceding model and check whether it explains observations. {diagnosis_en} Record raw values, reference, repeatability and units. Compare the supported mechanism “{principle_en}” with the hypothesis to reject “{wrong_en}”. Decide to accept, repeat or revise and state what the data cannot establish.')
                    bilingual(step,'check',f'交付判別表與證據：{diagnosis} 附上不確定度或未知量、反例及接受／重測理由。',f'Deliver a discrimination table and evidence: {diagnosis_en} Include uncertainty or unknowns, a counterexample and acceptance/retest rationale.')
                bilingual(step,'observation',diagnosis,diagnosis_en)
                bilingual(step,'failure',f'待排除的錯誤主張：{wrong} 若模型與資料不符，先查參考面、單位與假設，再用本步的獨立量測區分原因。',f'Incorrect claim to reject: {wrong_en} If model and data disagree, check reference planes, units and assumptions before using this step’s independent diagnostic.')
                step['knowledge']=[{'id':sid+'-k1','title':'物理機制與系統邊界','titleEn':'Mechanism and system boundary','text':principle,'textEn':principle_en,'sourceIds':ids},{'id':sid+'-k2','title':'判別方法與證據','titleEn':'Diagnostic and evidence','text':diagnosis,'textEn':diagnosis_en,'sourceIds':ids},{'id':sid+'-k3','title':'課程量化模型與適用界限','titleEn':'Course quantitative model and validity limits','text':c['formula'][0]+' '+c['bounds'][0],'textEn':c['formula'][1]+' '+c['bounds'][1],'sourceIds':ids}]
                # Rotate answers; distractors are distinct misconceptions authored for this topic.
                nextwrong=c['units'][(ui+1)%12][6:8]
                answer=(index+ui+phase)%3
                correct=[principle,principle_en] if phase==0 else [diagnosis,diagnosis_en]
                choices=[[wrong,wrong_en],nextwrong];choices.insert(answer,correct)
                step['quiz']={'question':f'審查「{title}」時，哪項主張或判別方法有根據？','questionEn':f'Which claim or diagnostic is justified for {en.lower()}?','options':[x[0] for x in choices],'optionsEn':[x[1] for x in choices],'answer':answer,'explanation':principle+' '+diagnosis,'explanationEn':principle_en+' '+diagnosis_en}
                stage['steps'].append(step);previous=sid
        course['stages'].append(stage)
    return course

def make_place(c):
    z,en,city,cityen,country,countryen,lat,lng,address,key=PLACES[c['placeKey']]
    ids=source_ids(c); place={'name':z,'nameEn':en,'city':city,'cityEn':cityen,'country':country,'countryEn':countryen,'lat':lat,'lng':lng,'mapQuery':address,'address':address,'addressEn':address,'coordinateScope':'座標為城市／代表地區的近似定位，不是上述機構地址的精確地理編碼或設備位置。地圖搜尋使用公開地址；此地只代表供應鏈或案例脈絡。','coordinateScopeEn':'Coordinates are approximate city/regional references, not an exact geocode of the institutional address or an equipment location. Map search uses the public address; this location represents supply-chain or case context only.'}
    n=int(c['id'][1:]);hist=[]
    if n>=298:
        events={298:[('2019','VSC 新連線投運','New VSC link commissioned','營運者和供應商在 2019 年公告新北本 300 MW 設備投運；它與既有 600 MW LCC 連線分開辨識。','The operator and supplier announced the new 300 MW link in 2019, distinct from the existing 600 MW LCC link.','hokkaido'),('工程脈絡 / Engineering context','隧道與交流系統介面','Tunnel and AC-system interfaces','營運者公開資料連結北海道、本州與青函隧道路線；本課把地理路由、換流原理和可用性分開分析，不推測站內細節。','Public operator information connects Hokkaido, Honshu and the Seikan Tunnel route. The course separates route, conversion principles and availability without inferring station internals.','hokkaido-operator')],299:[('1986','IFA 的工程年代','IFA commissioning era','National Grid 區分 1961 年早期互聯與 1986 年 IFA；本課以後者及營運者公布的约 70 km、2,000 MW 系統為案例。','National Grid distinguishes the earlier 1961 connection from IFA in 1986. This course studies the latter and the operator’s approximately 70 km, 2,000 MW system.','ifa-history'),('工程脈絡 / Engineering context','跨國共同營運','Joint cross-border operation','IFA 由 National Grid 與 RTE 的營運生態系連接英法電網；地圖標示英國端代表地區，法國端和海纜路由請查官方圖。','IFA links the British and French grids through National Grid and RTE. The map shows the British-end reference region; consult official maps for the French end and cable route.','ifa')],300:[('1965 / 2013','跨島連線與極線更新','Inter-island connection and pole renewal','紐西蘭電力管理局記錄 1965 年起始與 2013 年 Pole 3 替代的歷史；不同年代的容量數字不可混成現況。','New Zealand’s Electricity Authority documents the 1965 beginning and 2013 Pole 3 replacement; ratings from different eras must not be merged into a current status.','nz-history'),('2026 公告 / announcement','海纜更新仍是計畫時程','Cable renewal remains a planned timeline','Transpower 的 2026 合約公告說明預計 2031 年鋪纜及 2032 年上半年投運；這是公告時的計畫，不是已完成工程。它與較早更新頁面的時程須保留版本差異。','Transpower’s 2026 contract notice plans cable installation in 2031 and commissioning in the first half of 2032. This is the plan at publication, not completed work; retain differences from earlier programme pages.','nz-contract')]}
        for year,t,te,txt,txte,s in events[n]:hist.append(dict(year=year,title=t,titleEn=te,text=txt,textEn=txte,sourceIds=[SOURCES[s]['id']]))
    else:
        hist=[{'year':'技術脈絡 / Technical context','title':'從元件機制到系統設計','titleEn':'From component mechanisms to system design','text':f"{SOURCES[c['sourceKeys'][0]]['publisher']} 的原廠技術資料提供本課的可追溯起點。{c['units'][0][2]} 本課以自行編写的教學模型連到「{c['lens']}」，不主張地圖所標機構發明了全部技術。",'textEn':f"Manufacturer documentation from {SOURCES[c['sourceKeys'][0]]['publisher']} provides a traceable starting point. {c['units'][0][3]} Independently authored models connect this to {c['lensEn']}; the mapped organization is not claimed to have invented all these techniques.",'sourceIds':[ids[0]]},{'year':'工程脈絡 / Engineering context','title':'從標稱數據走向驗證證據','titleEn':'From nominal metrics to verification evidence','text':f"本課進一步處理這個系統問題：{c['units'][6][2]} 以「{c['units'][6][4]}」練習判讀；這段是公開原理的學習脈絡，不是機構的發明年表。",'textEn':f"The course then examines a system issue: {c['units'][6][3]} Practice interpretation using: {c['units'][6][5]} This is public-principle learning context, not an institutional invention timeline.",'sourceIds':ids[:2]}]
    return {'courseId':c['id'],'place':place,'summary':TITLES[c['id']]['title']+'以'+c['lens']+'連結元件、系統和驗證。此定位提供公開供應鏈或工程案例的地理背景。','summaryEn':TITLES[c['id']]['titleEn']+' links components, systems and validation through '+c['lensEn']+'. The location gives public supply-chain or case geography.','connection':'比較相關課程時，保留本課的基本模型，重新核對材料、規模、環境與驗收邊界。','connectionEn':'Transfer the basic models to related courses while rechecking materials, scale, environment and acceptance boundaries.','history':hist,'references':refs(c)+[{k:SOURCES[key][k] for k in ('title','titleEn','publisher','url')}],'sourceIds':list(dict.fromkeys(ids+[SOURCES[key]['id']]))}

def make_related(c):
    rows=[]
    for j,rid in enumerate(c['relatedIds']):
        same,se,diff,de=RELATIONS[int(c['id'][1:])][j];target=TITLES[rid]
        rows.append({'id':rid,'title':target['title'],'titleEn':target['titleEn'],'why':same,'whyEn':se,'transfer':same,'transferEn':se,'difference':diff,'differenceEn':de,'practice':[f"把「{c['units'][j][0]}」的概念圖與「{target['title']}」的輸入輸出對照。",c['units'][j+3][4],f'用一項可重算的量或反例檢查差異：{diff}'],'practiceEn':[f"Compare the {c['units'][j][1].lower()} concept map with inputs/outputs of {target['titleEn']}.",c['units'][j+3][5],f'Test the difference with a reproducible quantity or counterexample: {de}'],'referenceUrls':[SOURCES[k]['url'] for k in c['sourceKeys'][:3]]})
    return {'courseId':c['id'],'overview':'由'+c['lens']+'延伸到兩種可繼續實作的工法；比較共享物理關係與不能直接複製的條件。','overviewEn':'Extend '+c['lensEn']+' into two guided courses, comparing shared physical relations and nontransferable conditions.','related':rows,'references':refs(c)}

def main():
    courses=[make_course(c,i) for i,c in enumerate(COURSES)]
    used=set(k for c in COURSES for k in c['sourceKeys'])|{PLACES[c['placeKey']][-1] for c in COURSES}
    output={'version':10,'scope':'Independently authored bilingual educational engineering models; public principles, not production recipes. Source imagery is link-only.','courses':courses,'sources':[SOURCES[k] for k in sorted(used)],'places':[make_place(c) for c in COURSES],'related':[make_related(c) for c in COURSES]}
    assert len(courses)==32 and [c['id'] for c in courses]==[f'a{n}' for n in range(269,301)]
    seen=set();answer_counts=[0,0,0]
    for c in courses:
        assert len(c['stages'])==4 and all(len(s['steps'])==6 for s in c['stages'])
        assert c['title']==TITLES[c['id']]['title']
        for st in c['stages']:
            for s in st['steps']:
                assert s['id'] not in seen;seen.add(s['id'])
                for k in ('title','objective','instruction','observation','failure','check'):assert s[k] and s[k+'En']
                assert len(s['knowledge'])==3
                q=s['quiz'];assert len(set(q['options']))==3 and len(set(q['optionsEn']))==3 and q['answer'] in range(3)
                answer_counts[q['answer']]+=1
                assert all(x in {SOURCES[k]['id'] for k in used} for x in s['sourceIds'])
    assert len(seen)==768
    assert all(len(p['history'])>=2 for p in output['places'])
    assert all(len(r['related'])==2 and all(len(x['practice'])==3 and len(x['practiceEn'])==3 for x in r['related']) for r in output['related'])
    data=json.dumps(output,ensure_ascii=False,indent=2)+'\n'
    (ROOT/'group_c.json').write_text(data,encoding='utf-8')
    report={'courses':32,'technicalUnits':384,'steps':768,'knowledge':2304,'sources':len(output['sources']),'places':32,'relatedComparisons':64,'answerCounts':answer_counts,'sha256':hashlib.sha256(data.encode()).hexdigest(),'independentAudit':'Reviewed numerical examples and all technical units by v10_media; fixes: Friis rounding, ratiometric cancellation, absolute-value delimiter; added PI positioning and IFA fire-recovery primary sources.','knownLimits':['Public conceptual teaching, not full physical simulation or field SOP.','Coordinates are city/region reference points, not exact site geocodes.','Source links do not confer media redistribution permission.','Stock symbols are reference hints; quotes need a configured licensed provider and timestamps.']}
    (ROOT/'review_group_c.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False))
if __name__=='__main__':main()
