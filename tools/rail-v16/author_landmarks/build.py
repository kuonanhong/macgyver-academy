#!/usr/bin/env python3
"""Build b301–b334 from authored, bilingual project and model records."""
import json, math, pathlib, sys, hashlib, copy
from models import M
from depth import D
from projects import P
from reconcile import apply
apply(P)
HERE=pathlib.Path(__file__).resolve().parent
ROOT=HERE.parent
TARGET={x['id']:x for x in json.loads((ROOT/'targets.json').read_text())}
OUT=ROOT/'inputs'; OUT.mkdir(exist_ok=True)
REV=ROOT/'reviews'; REV.mkdir(exist_ok=True)
P['b311']['url']='https://noeud-ferroviaire-lyonnais.debatpublic.fr/images/archives-rencontres/lyon-27062019/NFL-20190627-presentation-MO.pdf'
P['b311']['publisher']='SNCF Réseau / Commission nationale du débat public'
PRIMARY=dict(brake='v',cant='v',jerk='ramp',capacity='headway',dwell='exchange',turnback='reverse',regen='mass',drag='v',tunnelwave='length',pantograph='tension',thermal='deltaT',seismic='distance',settlement='drop',bridge='L',suspension='mass',wheelheat='energy',adhesion='mu',grade='mass',voltage='current',powerloss='current',isolation='ratio',localize='s1',communication='latency',interlock='inputs',brakecurve='initial',axle='wheel_force',fatigue='n1',snow='snow',crosswind='wind',noise='L1',drain='rain',freeze='heat',cooling='heat',filter='pressure',platform='people',escalator='speed',doors='stop_sigma',ventilation='flow',piston='train_area',queue='mean',availability='mtbf',rubber='coefficient',baggage='luggage',mixed='gap',neutral='force',sampling='speed',bearing='rpm',fleet='cycle',backup='energy',redundancy='q1',pressure='pressure',sand='flux',survey='dx',grout='gap',transfer='distance',congestion='flow1',clearance='gap',construction='setup')
INTEGER={'people','doors','exchange','inputs','n1','N1','n2','N2','plain','luggage'}
ENV={'__builtins__':{},'log':math.log,'log10':math.log10,'ceil':math.ceil}
def split(x): return x.split('~')
def join(*xs):
    v=[split(x) for x in xs]
    return ' '.join(x[0] for x in v)+'~'+' '.join(x[1] for x in v)
def num(x): return f'{x:.7g}'
def compute(expr,values): return float(eval(expr,ENV,values))
def sample(cid,key):
    m=M[key]; values={k:v[0] for k,v in m['variables'].items()}
    n=int(cid[1:])-301; factor=1+0.01*(n%7)
    main=PRIMARY[key]
    if key=='interlock': values['inputs']=6+n%3
    elif key=='noise': values['L1']=70+n%5
    else: values[main]*=factor
    # These are invented engineering test rigs, not published route parameters.
    if int(cid[1:]) in {302,303,304,305,*range(321,335)}:
        if key=='brake': values['v']=22+0.5*(n%5)
        if key=='cant': values.update(v=21+0.3*(n%5),R=600,cant=0.08)
        if key=='brakecurve': values.update(initial=24+0.4*(n%5),target=10)
        if key=='grade': values['v']=20
        if key=='mixed': values.update(fast=28,slow=18)
        if key=='drag': values['v']=25
    for k in values:
        if k in INTEGER: values[k]=int(round(values[k]))
    changed=copy.deepcopy(values)
    if key=='interlock': changed[main]+=1; delta='增加 1 個布林輸入~add one Boolean input'
    elif key=='noise': changed[main]+=3; delta='聲級增加 3 dB，不代表數值百分比的功率增加~increase the level by 3 dB, not a percentage increase in acoustic power'
    elif main in INTEGER: changed[main]=int(math.ceil(values[main]*1.1)); delta=f'將整數計數增加到 {changed[main]}~increase the integer count to {changed[main]}'
    else: changed[main]*=1.1; delta='單獨增加百分之十~increase this input alone by ten percent'
    return values,changed,delta

def source(cid,key,title,titleEn,publisher,url,scope,scopeEn):
    return dict(key=f'{cid}-{key}',title=title,titleEn=titleEn,publisher=publisher,url=url,sourceType='primary',scope=scope,scopeEn=scopeEn)

def vendors():
    return [dict(name='西門子交通',nameEn='Siemens Mobility',business='鐵道車輛與基礎設施技術',businessEn='Rail vehicles and infrastructure technology',url='https://www.mobility.siemens.com/global/en/portfolio/rail.html',role='供比較研究的產業技術入口；不宣稱為本專案供應商或承包商。',roleEn='Industry reference for comparative study; no project-specific supply or contract role is asserted.',investorUrl='',security=None),dict(name='阿爾斯通',nameEn='Alstom',business='鐵道車輛與號誌技術',businessEn='Rail vehicles and signalling technology',url='https://www.alstom.com/solutions',role='供比較研究的產業技術入口；不宣稱為本專案供應商或承包商。',roleEn='Industry reference for comparative study; no project-specific supply or contract role is asserted.',investorUrl='',security=None)]

records=[]; provenance=[]
for cid,p in P.items():
    t=TARGET[cid]; title=t['title']+'~'+t['titleEn']; units=[]; calculations=[]
    for index,(key,context) in enumerate(zip(p['keys'],p['contexts']),1):
        m=M[key]; depth=D[key]; values,changed,delta=sample(cid,key); main=PRIMARY[key]
        value=compute(m['expression'],values); revised=compute(m['expression'],changed)
        assert math.isfinite(value) and math.isfinite(revised)
        inputs='; '.join(f'{k}={num(v)} {m["variables"][k][1]}' for k,v in values.items())
        output,unit=m['output']; zbound,ebound=split(m['boundary']); dz,de=split(delta)
        calc=f'{output}={m["expression"]}={num(value)} {unit}'
        model=(f'原創假想算例，全部輸入均非本工程操作參數：{inputs}；計算：{calc}。敏感度：{main} {dz}至 {num(changed[main])} {m["variables"][main][1]}，其餘固定，結果為 {num(revised)} {unit}。模型邊界：{zbound}'
               f'~Original hypothetical exercise; none of these inputs are operating parameters of this project: {inputs}; calculation: {calc}. Sensitivity: {main}, {de}, to {num(changed[main])} {m["variables"][main][1]}, with all other inputs fixed, gives {num(revised)} {unit}. Model boundary: {ebound}')
        practice_extra=(f'再以本單元 {main} 的對照值重算 {output}，提交含單位、輸入來源和模型不適用條件的結果表。'
                        f'~Also recalculate {output} for the alternative {main} value in this unit, submitting units, input provenance and conditions under which the model is inapplicable.')
        u=dict(anchor=m['title'],title=m['title'],mechanism=join(m['mechanism'],depth['mechanism'],context),model=model,verify=join(m['verify'],depth['verify']),failure=join(m['failure'],depth['failure']),misconception=m['myth'],practice=join(m['practice'],practice_extra))
        if cid=='b326' and key=='fleet':
            u['anchor']=u['title']='單圈週期與車隊需求~Loop cycle and fleet requirement'
            u['mechanism']=join('環狀路線的循環時間是一圈行駛時間加沿途停站時間，不需要假設每圈都在端點換向。以循環時間除以班距並向上取整，可得到維持規則發車的最低運轉車數；如果某站停站延誤，車距不均會沿環線傳播，不能靠沒有終端站就宣稱沒有瓶頸。~For a circular route, cycle time is one loop of running and station dwell; reversal at a terminal is not required on every circuit. Dividing cycle time by headway and rounding up gives the minimum circulating fleet for regular departures. Delay at one station can propagate uneven spacing around the loop, so absence of a terminus does not imply absence of bottlenecks.',depth['mechanism'],context)
            u['verify']=join('以同一列車通過固定參考站兩次的時間差量測單圈週期，逐站記錄停站時間，再重播連續數圈班表，確認每次發車有可用車組。若延誤持續累積，應分辨新增車輛、調節停站或進出車場安排的不同效果。~Measure loop time between two successive passages of the same train at a fixed reference station. Record dwell at each stop, then replay several circuits to confirm a train is available at every departure. If delay accumulates, distinguish the effects of extra trains, dwell regulation and depot entry or exit.','核對單圈行駛、沿途停站與班距使用相同時間單位，以逐列事件表確認每圈都有可用列車。~Verify common time units for loop running, station dwell and headway, using a train-by-train event table to confirm availability on every circuit.')
            u['misconception']='環狀線沒有終端折返就不必核對單圈時間與車組數~A circular line without terminal reversal need not check loop time against fleet size.'
            u['practice']=join('增加一個轉乘站的停站時間並重算單圈週期與向上取整車數，再以逐列時刻表檢查車距不均是否沿環線擴大。另列維修備車，不能把最低運轉車數當成全車隊採購量。~Increase dwell at one interchange and recalculate loop time and the upward-rounded train requirement. Replay individual trains to check whether uneven spacing grows around the circle. List maintenance spares separately, rather than treating the minimum circulating count as total fleet procurement.',practice_extra)
        units.append(u)
        row=dict(course=cid,unit=index,key=key,expression=m['expression'],inputs=values,inputUnits={k:v[1] for k,v in m['variables'].items()},output=output,outputUnit=unit,expected=value,perturbedInput=main,perturbedInputs=changed,perturbedExpected=revised,perturbation=delta,boundary=m['boundary'])
        records.append(row); calculations.append(row)
    first=calculations[0]; second=calculations[1]; third=calculations[2]
    ez,ee=split(p['scenario'])
    examples='；'.join(f'單元 {x["unit"]} 得 {x["output"]}={num(x["expected"])} {x["outputUnit"]}' for x in calculations[:3])
    examplesEn='; '.join(f'unit {x["unit"]} gives {x["output"]}={num(x["expected"])} {x["outputUnit"]}' for x in calculations[:3])
    example=(f'整合原創算例：{examples}。上述三個結果使用各單元明示的不同邊界，不能任意相加或視為實際工程實測值。以第一單元 {first["perturbedInput"]} 的擾動測試，結果改為 {num(first["perturbedExpected"])} {first["outputUnit"]}；學徒需先比較單位、敏感度和假設，再決定是否要細化模型。{ez} 最終交付應保留原始輸入、測點時間戳、誤差範圍與無法由簡化式證明的結論。'
             f'~Integrated original exercise: {examplesEn}. These three results use different explicit boundaries and must not be added or presented as measurements of the real railway. Perturbing {first["perturbedInput"]} in the first unit changes its result to {num(first["perturbedExpected"])} {first["outputUnit"]}. Compare units, sensitivity and assumptions before deciding which model needs refinement. {ee} The final submission should retain original inputs, measurement timestamps, uncertainty ranges and conclusions that the simplified expressions cannot establish.')
    historyevents='；'.join(f'{year} 年：{split(event)[0]}' for year,event in p['events'])
    historyeventsEn='; '.join(f'{year}: {split(event)[1]}' for year,event in p['events'])
    history=(f'公開工程與出版時間線：{historyevents}。這些事件由下列機構來源提供背景，不表示來源公開了本課程所有設計數據。{ez} 本課程另以可靠度、可用度、可維修度與安全方法整理需求、證據和變更邊界；歷史年份屬可查證事項，數學模型的輸入則是明示的教學假設。'
             f'~Public engineering and publication chronology: {historyeventsEn}. The institutional sources below establish this background; they do not imply publication of every design input in this course. {ee} The course separately uses reliability, availability, maintainability and safety reasoning to organise requirements, evidence and change boundaries. Historical dates are verifiable facts, whereas numerical model inputs are explicitly declared teaching assumptions.')
    timeline=[dict(year=year,event=event) for year,event in p['events']]
    if len(timeline)<3:
        timeline.append(dict(year='2025',event='IEC 發布新版鐵道 RAMS 第二部分安全系統方法~IEC published the revised railway RAMS Part 2 systems approach to safety'))
    facts=[f'已查證背景：{p["events"][0][0]} 年，{split(p["events"][0][1])[0]}。~Verified background: {p["events"][0][0]}, {split(p["events"][0][1])[1]}.']
    for r in calculations[:5]:
        main=r['perturbedInput']; values=r['inputs']; val=values[main]; un=r['inputUnits'][main]
        facts.append(f'教學假設，單元 {r["unit"]}：{main}={num(val)} {un}，計算 {r["output"]}={num(r["expected"])} {r["outputUnit"]}；非實測性能。~Teaching assumption, unit {r["unit"]}: {main}={num(val)} {un}, calculated {r["output"]}={num(r["expected"])} {r["outputUnit"]}; not measured performance.')
    sources=[source(cid,'history','專案官方歷史與路網背景','Official project history and network context',p['publisher'],p['url'],'支援已標示的公開歷史事件；不提供本課程假想數值，也不證實所有模型適用於現地。','Supports stated public historical events; does not supply invented numerical inputs or validate all models for the actual site.'),source(cid,'iec-rams-1','鐵道 RAMS 第一部分通用程序','Railway RAMS Part 1 generic process','International Electrotechnical Commission','https://webstore.iec.ch/en/publication/68933','IEC 62278-1:2025 書目與通用程序範圍；作為需求及證據整理參考，不宣稱本案採用特定條款。','Bibliographic edition and generic process scope of IEC 62278-1:2025; a requirements and evidence reference, not a claim about project-specific clauses.'),source(cid,'iec-rams-2','鐵道 RAMS 第二部分安全系統方法','Railway RAMS Part 2 systems approach to safety','International Electrotechnical Commission','https://webstore.iec.ch/en/publication/79793','IEC 62278-2:2025 書目與安全系統方法範圍；不重製付費標準條文。','Bibliographic edition and systems approach scope of IEC 62278-2:2025; no reproduction of paid standard text.')]
    if p['second']:
        sources.append(source(cid,'background','機構專案與工程背景補充','Institutional project and engineering background supplement','Primary institution at '+p['second'].split('/')[2],p['second'],'補充時間線與路網介面背景；詳細設計參數仍以原始工程文件為準。','Additional chronology and network-interface context; detailed design parameters remain subject to original project documentation.'))
    n=int(cid[1:]); related=[f'b{301+((n-301+1)%34)}',f'b{301+((n-301+7)%34)}']
    # Named landmarks remain real railway projects; relation is pedagogical, not a shared contract.
    landmark2=TARGET[related[0]]['title']+'~'+TARGET[related[0]]['titleEn']
    family='track' if cid=='b316' else ('station' if n>=321 or 302<=n<=305 else 'rail')
    data=dict(id=cid,title=title,discipline=t['discipline'],family=family,focus=p['focus'],summary=p['scenario'],example=example,history=history,units=units,facts=facts,timeline=timeline,codes=['IEC 62278-1:2025，鐵道 RAMS 通用程序；方法參考，不等同本案合約要求~IEC 62278-1:2025, railway RAMS generic process; methodological reference, not a project contract requirement','IEC 62278-2:2025，鐵道安全系統方法；應另查現地適用規範~IEC 62278-2:2025, systems approach to railway safety; local applicable rules require separate checking'],landmarks=[title,landmark2],place=dict(name=p['place'],country=p['country'],lat=p['coords'][0],lng=p['coords'][1],query=split(p['place'])[1]),sources=sources,vendors=vendors(),related=related,architectureNodes=[['路線與土建','Alignment and civil works'],['車輛與接觸','Vehicle and contact'],['牽引供電','Traction supply'],['行車控制','Movement control'],['車站與旅客','Stations and passengers'],['監測與維護','Monitoring and maintenance']],architectureEdges=[[0,1],[1,2],[2,3],[3,1],[3,4],[4,5],[5,0],[5,3]])
    path=OUT/(cid+'.json'); path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    provenance.append(dict(course=cid,reviewedDate='2026-10-23',projectSource=p['url'],supplement=p['second'],events=[dict(year=y,event=e) for y,e in p['events']],methodSources=[s['url'] for s in sources if s['key'].startswith(cid+'-iec')],placeScope='Approximate public station area, not a surveyed location, project centroid or equipment position.',authoredNumericScope='All numeric exercises are original hypothetical cases; project sources support context only.',fileSha256=hashlib.sha256(path.read_bytes()).hexdigest()))
    if (n-300)%5==0: print(f'Checkpoint: {n-300} course inputs written through {cid}')
(REV/'landmarks_numeric.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
(REV/'landmarks_sources.json').write_text(json.dumps(provenance,ensure_ascii=False,indent=2)+'\n')
print(f'Wrote {len(P)} courses, {len(records)} numeric examples and perturbations.')
