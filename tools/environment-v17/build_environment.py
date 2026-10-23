#!/usr/bin/env python3
"""Build forty bilingual learning tasks per environment course, preserving V16."""
import ast, copy, csv, hashlib, json, math, operator, sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
DATA=ROOT/'public/academy/data'
TAG='-v17-'
def read(p): return json.loads(p.read_text('utf-8'))
def write(p,x):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(x,ensure_ascii=False,separators=(',',':'))+'\n','utf-8')
def pair(x):
    assert isinstance(x,str) and '~' in x, str(x)[:120]
    a,b=x.split('~',1); assert a.strip() and b.strip()
    return a.strip(),b.strip()
def bilingual(obj,key,value):
    obj[key],obj[key+'En']=pair(value)
def first(x):
    z,e=pair(x)
    return z.split('。')[0]+'。',e.split('. ')[0].rstrip('.')+'.'
def calc(expression):
    ops={ast.Add:operator.add,ast.Sub:operator.sub,ast.Mult:operator.mul,ast.Div:operator.truediv,ast.FloorDiv:operator.floordiv,ast.Pow:operator.pow,ast.USub:operator.neg,ast.UAdd:operator.pos}
    funcs={'sqrt':math.sqrt,'log':math.log,'log10':math.log10,'exp':math.exp,'abs':abs,'min':min,'max':max,'round':round,'ceil':math.ceil,'floor':math.floor}
    def visit(n):
        if isinstance(n,ast.Constant) and isinstance(n.value,(int,float)): return n.value
        if isinstance(n,ast.BinOp) and type(n.op) in ops:return ops[type(n.op)](visit(n.left),visit(n.right))
        if isinstance(n,ast.UnaryOp) and type(n.op) in ops:return ops[type(n.op)](visit(n.operand))
        if isinstance(n,ast.Name) and n.id in {'pi','e'}:return getattr(math,n.id)
        if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id in funcs:return funcs[n.func.id](*[visit(a) for a in n.args])
        raise ValueError('Unsupported arithmetic: '+expression)
    return visit(ast.parse(expression,mode='eval').body)

STAGES=[('系統邊界與現場觀察','System boundaries and observation'),('程序機制與定量設計','Process mechanisms and quantitative design'),('設備操作與量測','Equipment operation and measurement'),('異常診斷與改善','Diagnosis and improvement'),('整合驗證與交接','Integrated verification and handover')]
SUB={
 'environment-water':('水處理與水資源循環','Water treatment and water reuse'),
 'environment-urban':('都市韌性與藍綠基盤','Urban resilience and blue-green infrastructure'),
 'environment-waste':('廢棄物與能源回收','Waste and energy recovery'),
 'environment-recycling':('資源分選與材料循環','Resource sorting and material circularity'),
 'environment-remediation':('土地與地下水整治','Land and groundwater remediation'),
 'environment-monitoring':('環境量測與生命週期','Environmental monitoring and life cycles')}
SCOPE=('公開原理與資料支持的原創教學。算例中的輸入為明示教學假設，非該設施實測或操作設定。此處任務在離線模型完成，不能作為現場設計、飲用水合格或設備操作許可。',
       'Original teaching based on public principles and sources. Numerical inputs are explicit teaching assumptions, not site measurements or operating setpoints. Tasks use offline models and do not certify field design, potable-water compliance or equipment operation.')

def step_for(c,u,index,facet,sourceids,previous):
    number=index*4+facet+1;sid=c['id']+TAG+f'{number:02d}'
    title,titleen=pair(u['title'])
    names=[('機制與觀察','Mechanism and observation'),('定量算例','Quantitative example'),('操作與驗證','Action and verification'),('異常診斷','Fault diagnosis')]
    key=['mechanism','model','verify','failure'][facet]
    text,texten=pair(u[key]);mis,misen=pair(u['misconception']);prac,pracen=pair(u['practice'])
    target=('辨識 '+title+' 的機制，說明可觀察的因果關係。','Identify the mechanism of '+titleen+' and its observable causal relationships.') if facet==0 else (
      ('重算 '+title+' 的教學算例，核對單位與適用條件。','Recalculate the teaching example for '+titleen+' and verify units and assumptions.') if facet==1 else (
      ('完成 '+title+' 的量測或模型練習，記錄與假設的差異。','Complete the measurement/model exercise for '+titleen+' and record deviations from assumptions.') if facet==2 else
      ('區分 '+title+' 的失效原因，提出能排除替代解釋的檢查。','Distinguish failure causes in '+titleen+' with a check that rules out an alternative explanation.')))
    correct,correcten=first(u['failure'] if facet==3 else u['mechanism'] if facet==0 else u['verify'])
    options=[mis,correct,'看到結果符合預期就可省略條件、單位與原始資料。']
    optionsen=[misen,correcten,'An expected result allows conditions, units and raw data to be omitted.']
    questions=[('哪一項能解釋本單元的工程機制？','Which statement explains this unit’s mechanism?'),('依照本單元基準算式，計算結果與單位為何？','What result and unit follow from the baseline expression?'),('哪一項能用來驗證本步的工程判斷？','Which action can verify this engineering decision?'),('哪一項正確描述本步應診斷的失效原因？','Which statement correctly describes the failure to diagnose?')]
    if facet==1:
        checks=c['modelChecks'];stride=len(checks)//10 if len(checks)%10==0 else 1
        check=checks[min(index*stride,len(checks)-1)];value=check['expected'];unit=check['unit']
        # Same-dimensional alternatives expose arithmetic/scale errors without changing the source example.
        candidates=[value*1000 if value else 1,value,value/1000 if value else -1]
        options=[format(v,'.7g')+' '+unit for v in candidates];optionsen=list(options)
        correct,correcten=pair(u['model'])
    rotate=number%3
    options=options[rotate:]+options[:rotate];optionsen=optionsen[rotate:]+optionsen[:rotate]
    k=[{'id':sid+'-k1','title':title,'titleEn':titleen,'text':text,'textEn':texten,'sourceIds':sourceids},
       {'id':sid+'-k2','title':'驗證與操作練習','titleEn':'Verification and practice','text':prac,'textEn':pracen,'sourceIds':sourceids}]
    return dict(id=sid,title=title+'：'+names[facet][0],titleEn=titleen+': '+names[facet][1],estimatedMinutes=15+(facet==1)*5,
        simulationOnly=True,sourceIds=sourceids,prerequisiteIds=[previous] if previous else [],
        objective=target[0],objectiveEn=target[1],instruction=text+(('\n操作任務：'+prac) if facet==2 else ''),instructionEn=texten+(('\nAction: '+pracen) if facet==2 else ''),
        observation=pair(u['model'])[0],observationEn=pair(u['model'])[1],failure=pair(u['failure'])[0],failureEn=pair(u['failure'])[1],
        check=pair(u['verify'])[0],checkEn=pair(u['verify'])[1],knowledge=k,
        quiz={'question':questions[facet][0],'questionEn':questions[facet][1], 'options':options,'optionsEn':optionsen,'answer':(1-rotate)%3,'explanation':correct+' '+pair(u['verify'])[0],'explanationEn':correcten+' '+pair(u['verify'])[1]},
        unit=index+1,unitFacet=['mechanism','calculation','verification','diagnosis'][facet],order=(number-1)%8+1,sequence=number)

def main():
    partial='--allow-partial' in sys.argv
    inputs=[read(p) for p in sorted((HERE/'inputs').glob('b*.json'))]
    assert partial or len(inputs)==100, f'Need100 authored inputs, got {len(inputs)}'
    targets={c['id']:c for c in read(HERE/'targets.json')}
    featured=read(DATA/'featured.json'); catalog=read(DATA/'catalog.json');by={c['id']:c for c in featured}; original=list(by)
    sources={s['id']:s for s in read(DATA/'sources.json')};media=read(DATA/'media.json');mm={m['courseId']:m for m in media['courses']}
    places=read(DATA/'course-places.json');pm={p['courseId']:p for p in places['courses']}
    related=read(DATA/'related-skills.json');rm={r['courseId']:r for r in related['courses']}
    checkrows=[]
    for c in inputs:
        cid=c['id'];assert cid in targets;assert len(c['units'])==10,cid
        for u in c['units']:
            for field in ['title','mechanism','model','verify','failure','misconception','practice']:pair(u[field])
        assert len(c['sources'])>=2,cid
        ids=[]
        for src in c['sources']:
            assert src['url'].startswith('https://'),src
            sid=src['id'];assert sid.startswith('v17s-'),sid
            old=sources.get(sid)
            assert not old or old['url']==src['url'],('source ID conflict',sid)
            sources[sid]={**src,'publisher':src.get('organization',src.get('publisher','')),'scope':'來源支持原理或工程背景；算例為明示教學假設。','scopeEn':'Source supports principles or project context; examples use explicit teaching assumptions.'};ids.append(sid)
        for record in c.get('modelChecks',[]):
            value=calc(record['expression']);assert math.isfinite(value) and math.isclose(value,record['expected'],rel_tol=record.get('relativeTolerance',1e-5),abs_tol=record.get('absoluteTolerance',1e-5)),(cid,record,value)
            checkrows.append({'course':cid,**record,'actual':value})
        assert c.get('modelChecks'),('No numerical checks',cid)
        base=copy.deepcopy(by.get(cid,targets[cid]));base['stages']=[st for st in base.get('stages',[]) if TAG not in st['id']]
        oldsteps=[s for st in base['stages'] for s in st['steps']];previous=oldsteps[-1]['id'] if oldsteps else None
        new=[]
        for i,u in enumerate(c['units']):
            for facet in range(4):
                s=step_for(c,u,i,facet,ids,previous);s['sequence']+=len(oldsteps);previous=s['id']
                checks=c['modelChecks'];stride=len(checks)//10 if len(checks)%10==0 else 1
                s['environmentExample']={k:checks[min(i*stride,len(checks)-1)][k] for k in ['expression','expected','unit','description'] if k in checks[min(i*stride,len(checks)-1)]}
                new.append(s)
        for i,(z,e) in enumerate(STAGES):base['stages'].append({'id':cid+TAG+'stage-'+str(i+1),'order':len(base['stages'])+1,'title':z,'titleEn':e,'description':'以可核對的機制、算例、操作與診斷逐步建立證據。','descriptionEn':'Build evidence through mechanisms, worked examples, actions and diagnosis.','steps':new[i*8:i*8+8]})
        base.update(category='environment',status='guided',kind='guided',contentStatus='authored-bilingual-teaching',simulationOnly=True,educationEdition=17,enrichmentVersion=17,curriculumVersion=17,depth=4,languageCoverage=['zh-TW','en'],sourceIds=list(dict.fromkeys(base.get('sourceIds',[])+ids)),scope=SCOPE[0],scopeEn=SCOPE[1])
        bilingual(base,'summary',c['summary']);base['stepCount']=len(oldsteps)+40;base['estimatedMinutes']=sum(s.get('estimatedMinutes',15) for st in base['stages'] for s in st['steps'])
        sub=c.get('discipline','environment-water');assert sub in SUB,(cid,sub)
        base.update(subcategory=sub,subcategoryTitle=SUB[sub][0],subcategoryTitleEn=SUB[sub][1],learningTrack='environment',learningSubdiscipline=sub,learningTags=[sub,'v17','environment'])
        nodes=c.get('architectureNodes') or [u['title'] for u in c['units'][::2]]
        base['architectureNodes']=[{'id':'n'+str(i),'label':pair(n)[0],'labelEn':pair(n)[1]} for i,n in enumerate(nodes)]
        base['architectureEdges']=[[i,i+1] for i in range(len(nodes)-1)]
        base['architectureFamily']=sub
        base['workedExample']={'title':'教學算例','titleEn':'Teaching example','text':pair(c['units'][0]['model'])[0],'textEn':pair(c['units'][0]['model'])[1]}
        base['flowDiagram']='assets/diagrams/'+cid+'-v17-zh.svg';base['flowDiagramEn']='assets/diagrams/'+cid+'-v17-en.svg'
        by[cid]=base
        p=c['place'];p={**p,'lng':p.get('lng',p.get('lon')),'coordinateScope':p.get('coordinateScope','公開設施或研究據點的近似代表位置；不是操作入口或實際教學實驗室。'),'coordinateScopeEn':p.get('coordinateScopeEn','Approximate public facility/research reference, not an operating entrance or the teaching laboratory.')}
        assert -90<=p['lat']<=90 and -180<=p['lng']<=180,cid
        hist=pair(c.get('history',c['summary']))
        pm[cid]={'courseId':cid,'place':p,'summary':hist[0],'summaryEn':hist[1],'history':[{'year':'工程背景','title':base['title'],'titleEn':base['titleEn'],'text':hist[0],'textEn':hist[1]}], 'connection':base['summary'],'connectionEn':base['summaryEn'],'references':[sources[s] for s in ids],'sourceIds':ids}
        m=mm.setdefault(cid,{'courseId':cid,'videos':[],'guides':[]});m['guides']=[g for g in m.get('guides',[]) if '-v17-' not in g['id']]+[{'id':cid+'-v17-practice','title':'工程操作與定量驗證手冊','titleEn':'Engineering actions and quantitative verification','concept':base['summary'],'conceptEn':base['summaryEn'],'procedure':[pair(u['practice'])[0] for u in c['units']],'procedureEn':[pair(u['practice'])[1] for u in c['units']],'evidence':[pair(u['verify'])[0] for u in c['units']],'evidenceEn':[pair(u['verify'])[1] for u in c['units']],'pitfalls':[pair(u['failure'])[0] for u in c['units']],'pitfallsEn':[pair(u['failure'])[1] for u in c['units']],'sourceIds':ids,'sources':[sources[s] for s in ids],'simulationOnly':True,'scope':SCOPE[0],'scopeEn':SCOPE[1]}]
        draw_diagrams(base)
    for c in inputs:
        cid=c['id'];base=by[cid]; group=[k for k in sorted(by) if by[k].get('subcategory')==base['subcategory'] and k!=cid]
        links=[]
        for other in group[:2]:
            d=by[other];links.append({'id':other,'title':d['title'],'titleEn':d['titleEn'],'why':'比較兩個系統的物質或能量收支，列出不可直接沿用的邊界條件。','whyEn':'Compare material or energy balances and identify boundary conditions that cannot be transferred.','transfer':'守恆、量測與失效驗證','transferEn':'Conservation, measurement and failure verification','difference':'設備尺度、進料組成與品質目標必須分別設定。','differenceEn':'Equipment scale, feed composition and quality objectives require separate definitions.','practice':['各選一個教學算例，記下輸入、輸出與單位。','對照兩課的系統邊界，說明哪些假設不能沿用。','改變一個輸入，提出量測與失效判據來核對結果。'],'practiceEn':['Choose one worked example from each course and record inputs, outputs and units.','Compare system boundaries and identify assumptions that cannot transfer.','Change one input and propose measurements and failure criteria to check the result.'],'place':pm[other]['place'],'referenceUrls':[sources[i]['url'] for i in d['sourceIds'] if i in sources][:3]})
        rm[cid]={'courseId':cid,'overview':'跨單元連結與比較練習','overviewEn':'Cross-process connections and comparisons','related':links,'references':[src for src in sources.values() if src['id'] in base['sourceIds'] or src['url'] in {u for link in links for u in link['referenceUrls']}]}
    order=original+[c['id'] for c in inputs if c['id'] not in original]
    featured=[by[cid] for cid in order]
    catalog=[{k:v for k,v in by.get(c['id'],c).items() if k not in {'stages','workedExample','v16Extension','v16Architecture'}} if c['id'] in {x['id'] for x in inputs} else c for c in catalog]
    write(DATA/'featured.json',featured);write(DATA/'catalog.json',catalog);write(DATA/'sources.json',list(sources.values()))
    write(DATA/'media.json',{**media,'version':17,'courses':list(mm.values())});write(DATA/'course-places.json',{**places,'version':17,'courses':list(pm.values())});write(DATA/'related-skills.json',{**related,'version':17,'courses':list(rm.values())})
    release=read(DATA/'release.json');release.update(version='17.0.0',date='2026-10-23',guidedCourses=len(featured),allSteps=sum(c['stepCount'] for c in featured),environmentCourses=len(inputs),environmentNewSteps=len(inputs)*40,sources=len(sources),courseHistories=len(pm),mapLocations=len(pm),knowledgePoints=sum(len(s.get('knowledge',[])) for c in featured for st in c['stages'] for s in st['steps']))
    write(DATA/'release.json',release)
    report={'status':'PASS' if len(inputs)==100 else 'PARTIAL','environmentCourses':len(inputs),'newSteps':len(inputs)*40,'guidedCourses':len(featured),'allSteps':release['allSteps'],'numericChecks':len(checkrows)}
    write(ROOT/'docs/VALIDATION_CURRICULUM_V17.json',report);write(HERE/'calculation-checks.json',checkrows)
    print(json.dumps(report))

def draw_diagrams(c):
    import html
    for lang in ['zh','en']:
        nodes=c['architectureNodes'];width=1000;height=180+len(nodes)*90
        a=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">','<rect width="100%" height="100%" fill="#112f36"/>',f'<text x="50" y="54" font-size="26" fill="#ffffff" font-family="sans-serif">{html.escape(c["titleEn" if lang=="en" else "title"])}</text>']
        for i,n in enumerate(nodes):
            y=100+i*90;label=n['labelEn' if lang=='en' else 'label'];a.append(f'<rect x="65" y="{y}" width="865" height="60" rx="12" fill="#e1eee3"/><text x="85" y="{y+38}" font-size="18" fill="#153c35" font-family="sans-serif">{i+1:02d} · {html.escape(label)}</text>')
            if i<len(nodes)-1:a.append(f'<path d="M500 {y+63}v23m-8-8l8 8 8-8" stroke="#e7b36c" fill="none" stroke-width="3"/>')
        a.append(f'<text x="65" y="{height-25}" fill="#e7b36c" font-size="18" font-family="sans-serif">'+('Original teaching process map · not site as-built drawings' if lang=='en' else '原創教學程序圖 · 非現場竣工圖')+'</text></svg>')
        path=DATA.parent/'assets/diagrams'/f'{c["id"]}-v17-{lang}.svg';path.write_text('\n'.join(a),'utf-8')

if __name__=='__main__':main()
