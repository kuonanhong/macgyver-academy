#!/usr/bin/env python3
"""Original V16 track/power teaching cases. No proprietary operating settings.

Compact authored unit records are expanded into complete bilingual teaching
tasks. Numeric examples are executable and every parameter carries a unit.
The cited sources provide scope/background, not the invented numerical inputs.
"""
from pathlib import Path
import json, math, re, hashlib

HERE=Path(__file__).resolve().parent
TARGETS={t['id']:t for t in json.loads((HERE/'targets.json').read_text())}
COURSES={}
CHECKS=[]

def pair(s):
    a,b=s.split('~');return a.strip(),b.strip()
def C(n,kind,focus,context,instruments,boundary,units):
    COURSES[n]=dict(kind=kind,focus=focus,context=context,instruments=instruments,boundary=boundary,units=units)

SOURCES={
 'fra':('美國鐵路管理局軌道檢查架構','FRA Track and Structures Compliance Manual 2026','Federal Railroad Administration','https://railroads.dot.gov/elibrary/track-and-structures-compliance-manual-2026','美國軌道檢查與維護的比較框架；不把美國條文當成其他地區的允收值。','Comparative US track inspection framework; no US limit is presented as a universal acceptance value.'),
 'tsi':('歐洲鐵路基礎設施互通規範入口','Infrastructure TSI','European Union Agency for Railways','https://www.era.europa.eu/domains/technical-specifications-interoperability/infrastructure-tsi_en','基礎設施互通要求的官方入口；教材算例不是規範限值。','Official infrastructure interoperability entry point; teaching calculations are not regulatory limits.'),
 'cwr':('連續焊接鋼軌規則歷史資料','Continuous Welded Rail final rule','Federal Railroad Administration','https://railroads.dot.gov/elibrary/track-safety-standards-continuous-welded-rail-cwr','連續焊軌維護與檢查制度背景，非現場放散指令。','Background to welded-rail maintenance and inspection governance, not field destressing instructions.'),
 'trans':('軌道過渡段研究報告','Design of Track Transitions, Research Results Digest 79','Transportation Research Board / FRA','https://railroads.dot.gov/sites/fra.dot.gov/files/fra_net/14977/Research%20Results%20Digest%2079%20Design%20of%20Track%20Transitions.pdf','過渡段比較研究入口；本課數值是另行設定的縮減模型。','Entry point for transition research; numerical values in this course belong to separately assumed reduced models.'),
 'tamp':('搗固填充量監測技術','The tamping unit that understands the ballast','Plasser & Theurer','https://www.plassertheurer.com/en/pt-research/artikel/the-tamping-unit-that-understands-the-ballast','設備原理背景；不複製廠商液壓設定或作業程序。','Equipment-principle background without reproducing manufacturer hydraulic settings or work procedures.'),
 'clean':('道碴清篩技術','Cleaning ballast quickly and efficiently','Plasser & Theurer','https://www.plassertheurer.com/en/machine/technologie/bettungsreinigung/ueber-bettungsreinigung/schotter-schnell-und-effizient-reinigen','清篩設備流程背景；原創算例不宣稱廠商性能。','Ballast-cleaning process background; original examples do not claim manufacturer performance.'),
 'weld':('工廠鋼軌加工','Stationary rail processing','Vossloh','https://www.vossloh.com/en/products/stationary-rail-processing','焊軌與幾何加工的產品範圍；不表示本課與廠商合作。','Rail welding and geometry-processing product scope; no partnership is implied.'),
 'fast':('鋼軌扣件系統','Rail fastening systems','Vossloh','https://www.vossloh.com/en-us/fastening-systems','扣件產品範圍及後續查證入口，不提供專利設計圖。','Fastening product scope and follow-up reference, without proprietary drawings.'),
 'ultra':('鋼軌超音波檢測國際標準範圍','ISO 5735-1:2024 ultrasonic rail testing','International Organization for Standardization','https://www.iso.org/standard/82194.html','標準適用範圍與名稱；未複製付費條文或判退門檻。','Standard identity and scope, without reproducing paid clauses or rejection thresholds.'),
 'rtri':('非接觸鋼軌開口超音波研究','Non-contact detection of rail openings using aerial ultrasonic waves','Railway Technical Research Institute','https://www.rtri.or.jp/eng/rd/seika/2020/05-26.html','研究例說明耦合與雜訊需驗證；不把試驗展示當成通用合格證明。','Research example illustrating coupling and noise verification; a demonstration is not universal certification.'),
 'ole':('鐵路電氣化工程介紹','Electrification','Network Rail','https://www.networkrail.co.uk/our-work/living-by-the-railway/electrification/','架空電車線工程與相鄰構造物的背景。','Context for overhead-line works and surrounding structures.'),
 'elsafe':('鐵路電氣安全架構','Electrical Safety','Network Rail','https://safety.networkrail.co.uk/safety/electrical-safety/','電氣工作授權與風險管理入口；教學模型僅使用隔離低壓。','Electrical-work authorisation and risk management; teaching models use isolated low voltage only.'),
 'storage':('華盛頓都會區軌旁儲能展示報告','WMATA Wayside Energy Storage Demonstration Project','Federal Transit Administration','https://rosap.ntl.bts.gov/view/dot/39022','儲能展示研究背景；本課效率與容量均為假設而非展示績效。','Storage demonstration background; course efficiencies and capacities are assumed rather than demonstration results.'),
 'storage1979':('軌旁儲能早期系統研究','Wayside Energy Storage Study Volume 2','Federal Railroad Administration','https://rosap.ntl.bts.gov/view/dot/10599','早期系統研究的年代背景，不沿用其成本預測。','Historical systems-study context; its cost forecasts are not reused.'),
 'brake':('歐洲列車控制制動曲線介紹','Braking curves','European Union Agency for Railways','https://www.era.europa.eu/domains/european-rail-traffic-management-system/braking-curves','制動曲線官方入口；常減速度算例不宣稱重現完整ETCS演算法。','Official braking-curve entry point; constant-deceleration examples do not reproduce the full ETCS algorithm.'),
 'ccs':('控制命令與號誌互通規範入口','Control Command and Signalling TSI','European Union Agency for Railways','https://www.era.europa.eu/domains/technical-specifications-interoperability/control-command-and-signalling-tsi_en','號誌子系統互通範圍，不是可部署的安全認證軟體。','Signalling interoperability scope, not deployable safety-certified software.'),
 'betuwe':('荷蘭貨運鐵路路線','Routes voor goederentreinen','Government of the Netherlands','https://www.rijksoverheid.nl/themas/verkeer-en-vervoer/goederenvervoer/routes-voor-goederentreinen','貝圖威貨運線與路線背景；教學時刻表及列車性能另設。','Betuweroute and route context; teaching timetables and train performance are independently assumed.'),
 'cold':('寒區基礎研究資料','Foundations of structures in cold regions','US Army Engineer Research and Development Center','https://erdc-library.erdc.dren.mil/items/81b728f7-5e24-4ef8-e053-411ac80adeb3/full','凍土基礎熱邊界背景；不將建築基礎方法直接當鐵路設計。','Thermal boundary context for frozen foundations; building-foundation methods are not directly prescribed for railways.'),
}

def source(key):
 z,e,p,u,s,se=SOURCES[key]
 return dict(key='track-'+key,title=z,titleEn=e,publisher=p,url=u,sourceType='primary',scope=s,scopeEn=se)

def unit(row,course,n,i):
 # Seven authored fields: title, named values with units, expression, result unit,
 # mechanism, discriminating observation, and failure mechanism.
 a=row.split('|');assert len(a) in (7,9),(n,i,len(a))
 title,raw,expr,outunit,concept,observable,fault=[x.strip() for x in a[:7]]
 tz,te=pair(title);cz,ce=pair(concept);oz,oe=pair(observable);fz,fe=pair(fault)
 values={};details=[];parameter_units={}
 for item in raw.split(';'):
  m=re.fullmatch(r'\s*([A-Za-z][A-Za-z0-9_]*)\[([^\]]+)\]\s*=\s*([0-9.eE+\-]+)\s*',item)
  assert m,(n,i,item);k,u,v=m.groups();values[k]=float(v);parameter_units[k]=u;details.append(f'{k}={v} {u}')
 safe=dict(sqrt=math.sqrt,pi=math.pi,sin=math.sin,cos=math.cos,atan=math.atan,log=math.log,exp=math.exp,abs=abs,min=min,max=max)
 calc=lambda p:float(eval(expr,{'__builtins__':{}},{**safe,**p}))
 val=calc(values);assert math.isfinite(val)
 first=next(iter(values)); discrete=parameter_units[first] in ('count','events','bits','states')
 bounded_efficiency=(n==366 and i==7)
 absolute_temperature=parameter_units[first]=='degC'
 changed_input=values[first]+1 if (discrete or absolute_temperature) else (values[first]+0.01 if bounded_efficiency else values[first]*1.1)
 alter={**values,first:changed_input};new=calc(alter)
 perturbz='增加一個整數單位' if discrete else ('增加攝氏一度' if absolute_temperature else ('增加零點零一' if bounded_efficiency else '增加百分之十'))
 perturbe='an increase of one whole unit' if discrete else ('an increase of one degree Celsius' if absolute_temperature else ('an absolute increase of 0.01' if bounded_efficiency else 'a ten-percent increase'))
 formatted=f'{val:.6g}';changed=f'{new:.6g}'
 bz,be=pair(a[7].strip() if len(a)==9 else BOUNDS[tz]); iz,ie=pair(a[8].strip() if len(a)==9 else MEASURES[tz])
 modelz=f'原創假想算例，輸入不是現場操作值：{", ".join(details)}；y={expr}={formatted} {outunit}。只把 {first} {perturbz}，y={changed} {outunit}。模型邊界：{bz}；上式只代表本單元明列項，不把它視為完整驗證。'
 modele=f'Original assumed example, not field operating values: {", ".join(details)}; y={expr}={formatted} {outunit}. Increasing only {first} with {perturbe} gives y={changed} {outunit}. Boundary: {be}; this equation represents only the explicitly listed term and is not a complete verification.'
 verifyz=f'本單元以{oz}區分模型與觀察，先用{iz}建立基準，再保留相同量測位置與工況重複比較。將輸入表與輸出表分開保存，記下校正、解析度及時間戳記；至少改變一個輸入並保持其餘條件，檢查結果方向是否符合「{tz}」的方程。殘差超出事先設定的教學容差時，先查單位與量測鏈，再查省略的物理項。'
 verifye=f'Use {oe} to distinguish the model from observation in this unit. Establish a baseline using {ie}, then repeat at the same locations and conditions. Keep input and output records separate, recording calibration, resolution and timestamps. Change one input while holding others fixed and check the trend predicted by {te}. When residuals exceed a predefined teaching tolerance, examine units and the measurement chain before attributing the difference to omitted physics.'
 failurez=f'{fz}。這個失效與「{tz}」的量測偏差可能產生相似表象，因此必須同時檢查{oz}，不能只靠一個合成指標判定原因。若資料無法區分兩種假說，結論應保留未確定狀態，並提出下一項可推翻假說的獨立測試。'
 failuree=f'{fe}. This failure and a measurement bias in {te} can produce similar symptoms. Cross-check {oe} rather than diagnosing from one aggregate score. If the available observations cannot distinguish the hypotheses, retain an unresolved conclusion and specify an independent test that could falsify one explanation. Repeating the same biased sensor is not independent confirmation.'
 practicez=f'重算「{tz}」的基準與所列單一輸入變動案例，畫出輸入至輸出的關係，並寫出{bz}如何限制結論。接著設計一組符合模型及一組由{fz}造成偏離的合成觀察，以{oz}說明哪個證據能分辨兩者，保留單位及有效位數。'
 practicee=f'Recalculate the baseline and specified single-input perturbation for {te}, plot the input-output relationship, and explain the limiting assumption: {be}. Construct one synthetic observation consistent with the model and another affected by this failure: {fe}. Explain which evidence in {oe} distinguishes them, keeping units and justified significant figures throughout.'
 misconceptionz=f'本單元絕不可能出現這種失效：{fz}'
 misconceptone=f'This unit cannot exhibit the following failure: {fe}.'
 CHECKS.append(dict(courseId=f'b{n}',unit=i,title=te,parameters=values,parameterUnits={x.split('[')[0].strip():x.split('[')[1].split(']')[0] for x in raw.split(';')},expression=expr,result=val,resultUnit=outunit,sensitivityParameter=first,sensitivityValue=changed_input,sensitivityMode="plus-one-integer" if discrete else ("plus-one-degC" if absolute_temperature else ("plus-0.01" if bounded_efficiency else "plus-ten-percent")),sensitivityResult=new,modelBoundary=be,measurementChain=ie))
 change_pct=(new/val-1)*100 if val else None
 directionz='增加' if new>val else ('減少' if new<val else '不變')
 directione='increases' if new>val else ('decreases' if new<val else 'is unchanged')
 mechanismz=f'{cz}。本模型把 {first} 當成主動改變的輸入，其餘輸入固定；當它{perturbz}，輸出{directionz}為 {changed} {outunit}。這個比較描述明列方程的局部敏感度，不能把相關變數也一起改變後仍稱為相同測試。{bz}。使用{oz}作量測證據，才能檢查方程是否對應此處的實際物理量；{fz}，因此應把該原因與量測偏差分開。'
 mechanisme=f'{ce}. In this model, {first} is deliberately changed while every other input is held fixed. {perturbe.capitalize()} means the output {directione} to {changed} {outunit}. This comparison describes the sensitivity of the stated equation; changing correlated variables at the same time would be a different experiment. {be}. Use {oe} as measurement evidence that the equation represents the intended physical quantity. {fe}; separate that causal mechanism from bias in the measurement chain.'
 return dict(anchor=title,title=title,mechanism=mechanismz+'~'+mechanisme,model=modelz+'~'+modele,verify=verifyz+'~'+verifye,failure=failurez+'~'+failuree,misconception=misconceptionz+'~'+misconceptone,practice=practicez+'~'+practicee)

def build():
 CHECKS.clear()
 for n,c in sorted(COURSES.items()):
  cid=f'b{n}';t=TARGETS[cid];z,e=t['title'],t['titleEn'];fz,fe=pair(c['focus']);xz,xe=pair(c['context']);bz,be=pair(c['boundary'])
  units=[unit(row,c,n,i+1) for i,row in enumerate(c['units'].strip().splitlines()) if row.strip()]
  assert len(units)==10,(cid,len(units))
  keys=source_keys(n)
  summary=f'{z}以「{fz}」為主線，將十個物理或系統問題拆成機制、計算、驗證與診斷。{xz}。每個單元附帶可重算的假想數據與敏感度，學員需提交帶單位的工作表、可區分失效的證據及模型邊界。~This course develops {fe.lower()} through ten physical or systems questions, each studied through mechanism, calculation, verification and diagnosis. {xe}. Every unit contains reproducible assumed inputs and a sensitivity calculation. Learners submit a worksheet with units, discriminating evidence for failures, and explicit model boundaries.'
  history=f'本課把{z}放在可追溯的技術演進脈絡中，不把機構研究、規範出版與個別路線通車混為一談。{xz}。下列年代欄是工程事件、相關研究或規範出版節點；除明確標明實際工程事件者外，並非本專題設備的製造或投入營運日期。工程改進的判準是能否以量測區分假說，不能只依新舊設備外觀判斷。~The course places {e} in a traceable engineering context and distinguishes institutional research, standards publication and the opening of individual lines. {xe}. The timeline identifies engineering events, relevant research and standards-publication milestones. Unless explicitly labelled as a project event, a date is not the manufacture or commissioning date of the equipment. Improvement is assessed by whether measurements distinguish hypotheses, rather than by the apparent age of machinery.'
  example='以下為跨單元的原創假想工作表。先用第一單元定義邊界與單位，再以第二單元檢查另一個控制量，最後用第三單元提出前兩式未涵蓋的另一個檢查問題。'+pair(units[0]['model'])[0]+' '+pair(units[1]['model'])[0]+'把兩個算例的單一輸入敏感度放在同一張決策表，說明哪個變化最值得先量測；不可把不同物理量的裸數字直接比較，也不可把任一結果當成實際設備的設計、施工或營運許可。~This original worksheet connects the first three units using assumed inputs. Establish boundaries and units with the first unit, examine another controlling quantity with the second, and use the third to pose a separate check outside the first two equations. '+pair(units[0]['model'])[1]+' '+pair(units[1]['model'])[1]+'Put both single-input sensitivities in one decision table and explain which change most deserves measurement. Do not compare bare numbers with different physical dimensions, and do not treat any result as design approval, a construction procedure or operating permission.'
  facts=[f'教學單元{i+1}的基準量級：{pair(units[i]["model"])[0].split("。只把")[0]}~Teaching unit {i+1} baseline scale: {pair(units[i]["model"])[1].split(". Increasing only")[0]}.' for i in range(6)]
  timeline=course_timeline(n)
  nodes=architecture(n)
  place=dict(name='鐵道綜合技術研究所國立研究基地~RTRI Kunitachi research campus',country='日本~Japan',lat=35.7074,lng=139.4446,query='Railway Technical Research Institute Kunitachi Japan')
  if n==335:place=dict(name='鹿特丹港公共地理參考點~Port of Rotterdam public geographic reference',country='荷蘭~Netherlands',lat=51.947,lng=4.139,query='Port of Rotterdam Netherlands')
  vendors=[dict(name='福斯羅~Vossloh'.split('~')[0],nameEn='Vossloh',business='鋼軌扣件、道岔與軌道生命週期服務；僅為延伸閱讀對象。',businessEn='Fastenings, switches and rail lifecycle services; a further-reading entity only.',url='https://www.vossloh.com/en/company',role='軌道構件與維護技術延伸閱讀，並非本課指定承包商。',roleEn='Further reading on track components and maintenance, not a nominated course contractor.',security=None),dict(name='普拉塞與陶依爾',nameEn='Plasser & Theurer',business='軌道施工與維護機械，教材不採用其未公開操作設定。',businessEn='Track construction and maintenance machines; undisclosed machine settings are not used.',url='https://www.plassertheurer.com/en/machine/technologies/overview',role='量測與維護設備技術比較，並非合作或採購推薦。',roleEn='Technical comparison of measurement and maintenance equipment, without partnership or purchasing recommendation.',security=None)]
  if n>=360:vendors[1]=dict(name='英國鐵路網公司',nameEn='Network Rail',business='鐵路基礎設施管理與電氣化工程公開資訊。',businessEn='Public information on railway infrastructure management and electrification.',url='https://www.networkrail.co.uk/our-work/living-by-the-railway/electrification/',role='牽引供電與維護背景閱讀，不宣稱其參與本課假想工程。',roleEn='Traction-power and maintenance background, without claiming involvement in the assumed course project.',security=None)
  d=dict(id=cid,title=z+'~'+e,discipline=t['discipline'],family='power' if n in (360,361,362,363,364,366) else ('control' if n==367 else ('rail' if n==335 else 'track')),focus=c['focus'],summary=summary,history=history,example=example,units=units,facts=facts,timeline=timeline,codes=['歐洲基礎設施互通技術規範：依適用地區與版本另行核對。~European Infrastructure TSI: check jurisdiction and applicable edition separately.','美國聯邦法規第四十九篇第二百十三部分：僅作軌道比較閱讀。~US 49 CFR Part 213: comparative reading on track requirements only.'],landmarks=['台灣高速鐵路工程~Taiwan High Speed Rail','東海道新幹線工程~Tokaido Shinkansen'],place=place,sources=[source(k) for k in keys],vendors=vendors,related=[f'b{335+(n-335+1)%33}',f'b{335+(n-335+9)%33}'],architectureNodes=nodes,architectureEdges=architecture_edges(n))
  d['codes']=course_codes(n)
  d['landmarks']=course_landmarks(n)
  if n in (360,361,362,363,364,366): d['vendors']=power_vendors()
  if n==367: d['vendors']=control_vendors()
  (HERE/'inputs'/f'{cid}.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
 (HERE/'reviews/track_numeric_models.json').write_text(json.dumps({'author':'v16_rail_track','count':len(CHECKS),'models':CHECKS},ensure_ascii=False,indent=2)+'\n')
 print('Authored',len(COURSES),'courses;',len(CHECKS),'executable teaching models')

C(335,'structure','港區貨運列車的阻力制動與容量協同~Coordinating freight resistance braking and port capacity',
 '專用貨運線把港區裝卸、列車編組與幹線運行連成同一條物流鏈，列車較長與較重會同時改變加速、制動及站場占用，單看最高速度不足以推估吞吐量~A dedicated freight line links port handling, train assembly and mainline movement; longer heavier trains change acceleration, braking and yard occupation together, so maximum speed alone does not determine throughput',
 '合成運行圖、牽引力曲線與模擬重量紀錄~synthetic timetables, tractive-force curves and simulated mass records',
 '均勻坡度與固定列車質量的縮減模型，不含實際列車操縱策略~a reduced model with uniform gradient and fixed mass, excluding real driving strategies',
 '''列車單向運能~Directional train throughput | n[trains/h]=5; q[t/train]=1800 | n*q | t/h | 運能是班次與有效載重的乘積，空車回送及車站衝突仍會消耗路徑~Throughput multiplies departures by useful payload, while empty returns and conflicting moves still consume paths | 滿載率與實際發車間距~load factor and actual departure intervals | 把額定載重當實際載重會高估貨物流量~Using rated payload as actual payload overstates cargo flow
坡道牽引分力~Gradient traction force | m[kg]=2000000; g[m/s2]=9.81; s[1]=0.01 | m*g*s/1000 | kN | 小坡度下重力沿軌分量與列車質量成正比，坡度正負號決定牽引或制動需求~At small gradients the longitudinal gravitational force scales with train mass, and its sign distinguishes traction from braking demand | 坡度定位與車列總重~gradient location and total consist mass | 忽略尾車仍在另一坡段會誤算整列車受力~Ignoring wagons still on another gradient miscalculates total force
速度與牽引功率~Speed and tractive power | F[N]=300000; v[m/s]=20 | F*v/1e6 | MW | 同一牽引力在較高速度需要更高機械功率，功率限制與黏著限制是不同邊界~The same tractive force needs more mechanical power at higher speed; power and adhesion limits are different boundaries | 輪周功率與速度的同步紀錄~synchronous wheel-power and speed records | 把低速最大牽引力延用到高速會超出功率邊界~Extending maximum low-speed force to high speed exceeds the power boundary
貨列制動距離~Freight braking distance | v[m/s]=25; a[m/s2]=0.5; tau[s]=4 | v*tau+v**2/(2*a) | m | 制動建立前列車仍前進，反應距離與常減速度制動距離必須相加~The train continues moving while braking builds up, so delay distance must be added to constant-deceleration stopping distance | 制動建立延遲與速度衰減曲線~brake build-up delay and speed-decay trace | 只計算穩態制動段會低估長車列停車距離~Counting only steady braking underestimates a long consist stopping distance
貨物外廓餘量~Cargo clearance margin | limit[mm]=4200; load[mm]=4000; sway[mm]=70 | limit-load-sway | mm | 靜態貨物高度之外仍須扣除動態擺動與測量不確定度，名義外廓不等於可用空間~Dynamic movement and measurement uncertainty consume space beyond static cargo height; a nominal envelope is not usable clearance | 貨物掃描與代表性搖擺包絡~cargo scans and representative sway envelopes | 裝載偏心會使動態外廓侵入鄰近構造~Eccentric loading can move the dynamic envelope into nearby structures
閉塞占用時間~Block occupation time | L[m]=1500; train[m]=650; v[m/s]=25; margin[s]=20 | (L+train)/v+margin | s | 路徑釋放取決於列車尾端離開受保護區，而非車頭通過訊號點~A path is released when the rear clears the protected region, not merely when the front passes a signal | 頭尾通過時刻與解鎖狀態~front and rear passing times with release status | 忽略列車長度會讓理論班距低於實際占用~Ignoring train length produces a theoretical headway below real occupancy
滾動阻力能量~Rolling-resistance energy | F[N]=40000; L[m]=10000 | F*L/3.6e6 | kWh | 阻力作功按距離積分，長距離低阻力仍可形成可觀耗能~Resistance work is integrated over distance, so modest resistance over a long route can consume substantial energy | 牽引能量與里程分段帳~traction-energy accounts divided by route distance | 用單次瞬時功率代表整段能量會混淆時間與距離~Using one instantaneous power value confuses energy with time and distance
港區停留庫存~Port dwell inventory | lam[trains/h]=4; T[h]=2.5 | lam*T | trains | 穩態到達率乘平均停留時間給出平均在場列車數，但不提供尖峰排隊的上界~Arrival rate times average dwell gives mean inventory in steady conditions, but does not bound peak queues | 到達時刻、離開時刻與在場列車數~arrival times, departure times and yard inventory | 到達成群時平均庫存可能掩蓋短時壅塞~Bunched arrivals can hide short congestion behind a moderate average inventory
列車噪音能量比較~Train noise-energy comparison | n[events]=12; ref[events]=6 | 10*log(n/ref)/log(10) | dB | 同聲能事件數倍增只改變能量總量，不代表單一列車更吵~Multiplying equal-energy events increases total energy without making an individual train louder | 相同距離的事件聲暴露與事件數~event sound exposure and count at equal distance | 將分貝直接相加會嚴重誤判累積噪音~Adding decibels directly misrepresents accumulated sound energy
隧道換氣量級~Tunnel ventilation scale | A[m2]=65; u[m/s]=1.2 | A*u | m3/s | 平均流速乘有效斷面給出體積流量，列車活塞作用與局部回流需另列~Mean velocity times effective area gives volume flow, while piston action and local recirculation need separate treatment | 多點風速與有效斷面~multi-point air velocity and effective area | 只用中心風速代表全斷面會高估或低估通風~Using only centreline velocity misrepresents total ventilation''')

C(336,'geometry','平縱曲線連續性與高速動態舒適性~Alignment continuity and high-speed dynamic comfort',
 '路線設計先建立平面與高程共同里程，再檢查曲率、坡度和變化率；地形可行的中心線仍可能因高速動態需求而需要更長緩和段~Alignment design uses a shared chainage for plan and elevation before checking curvature, gradient and their rates; a terrain-feasible centreline may still require longer transitions for high-speed dynamics',
 '合成座標點、里程表與曲率曲線~synthetic coordinates, chainage tables and curvature traces',
 '小角度幾何及固定速度假設，不含完整車輛動力學~small-angle geometry at fixed speed, excluding full vehicle dynamics',
 '''圓曲線向心加速~Circular-curve acceleration | v[m/s]=80; R[m]=6400 | v**2/R | m/s2 | 向心加速度隨速度平方增加並隨半徑增加而降低~Centripetal acceleration increases with speed squared and decreases with radius | 同里程速度及曲率~speed and curvature at matching chainage | 忽略速度變動會把幾何問題誤判為懸吊問題~Ignoring speed variation can misidentify a geometry problem as suspension failure
曲線外矢估算~Curve versine estimate | L[m]=20; R[m]=5000 | L**2/(8*R)*1000 | mm | 小弦長近似下外矢與弦長平方成正比，弦長改變時不能直接比較讀值~For a short chord the versine scales with chord length squared; different chord lengths cannot be compared directly | 已知弦長的中點偏距~midpoint offset for a known chord length | 把不同弦長外矢當同一幾何量會誤判曲率~Comparing versines from different chords misidentifies curvature
緩和曲線曲率率~Transition curvature rate | R[m]=6000; L[m]=240 | 1/(R*L) | 1/m2 | 克羅梭曲線讓曲率沿里程線性增長，並不代表橫向加速度在變速時仍線性~A clothoid increases curvature linearly with distance, but lateral acceleration need not remain linear when speed changes | 曲率對里程的斜率~curvature slope against chainage | 緩和段縮短會提高曲率變化率~Shortening the transition increases curvature rate
橫向加加速度~Lateral jerk estimate | v[m/s]=80; R[m]=6000; L[m]=240 | v**3/(R*L) | m/s3 | 固定速度時幾何橫向加加速度含速度三次方，不能以速度比例直接外推~At fixed speed the geometric lateral jerk contains speed cubed, so linear speed scaling is incorrect | 固定速率曲率變化與橫向加速度~curvature change and lateral acceleration at steady speed | 只檢查圓曲線半徑會漏掉進出曲線的不平順~Checking circular radius alone misses transition discomfort
縱坡高程增量~Vertical grade rise | s[1]=0.018; L[m]=1200 | s*L | m | 小坡度以高差除水平距離定義，應與沿軌距離使用方式一致~Small gradients use rise over horizontal distance and require consistent distance conventions | 起終點高程與水平里程~endpoint elevations and horizontal chainage | 混用百分率與小數坡度會產生百倍誤差~Mixing percentage and decimal gradients creates a hundredfold error
豎曲線加速度~Vertical-curve acceleration | v[m/s]=75; R[m]=20000 | v**2/R | m/s2 | 豎曲線改變車體垂向慣性作用，凸凹方向決定輪重增減的趨勢~Vertical curvature changes vertical inertia; crest or sag direction determines the wheel-load trend | 車速、豎曲率與垂向反應~speed, vertical curvature and vertical response | 曲線正負號錯誤會顛倒輪重增加或減少~A curvature sign error reverses the inferred wheel-load trend
坡度接續長度~Grade-transition length | R[m]=25000; ds[1]=0.024 | R*ds | m | 小坡度圓形豎曲線長度約為半徑乘坡度差，坡度差須包含正負號~For small grades a circular vertical transition length is approximately radius times signed grade change | 兩端坡度與中間高程~endpoint gradients and intermediate levels | 只比較坡度絕對值會遺漏跨越零坡的變化~Comparing only gradient magnitudes misses a change across zero
平面偏角累積~Plan deflection accumulation | L[m]=350; R[m]=7000 | L/R*180/pi | degree | 圓弧方向改變是弧長除半徑，角度轉換不改變幾何關係~Circular-arc direction change is arc length divided by radius; unit conversion preserves the geometry | 兩端切線方向差~difference between endpoint tangent directions | 將角度與弧度混用會破壞座標積分~Mixing degrees and radians corrupts coordinate integration
里程誤差投影~Chainage-error projection | ds[m]=0.12; slope[1]=0.02 | ds*slope*1000 | mm | 里程位置誤差會經縱坡投影為高程誤差，並非所有高程差都來自水準測量~Chainage error projects through gradient into elevation error, so not every level discrepancy originates in levelling | 同基準的里程和高程殘差~chainage and elevation residuals on one datum | 把定位偏移當沉陷會引發錯誤修正~Mistaking position shift for settlement leads to incorrect correction
設計容差合成~Alignment uncertainty combination | ux[mm]=1.2; uy[mm]=1.6 | sqrt(ux**2+uy**2) | mm | 獨立正交誤差可按平方和合成，共同系統偏差則不能如此抵消~Independent orthogonal errors combine by root-sum-square, but shared systematic biases do not cancel this way | 重複測站與獨立閉合差~repeat stations and independent closure errors | 把相關誤差當獨立誤差會低估不確定度~Treating correlated errors as independent understates uncertainty''')

C(337,'geometry','曲線超高不足與混合速度的取捨~Cant deficiency and mixed-speed trade-offs',
 '超高把軌道平面旋轉以分擔曲線橫向作用，固定超高只能對特定速度平衡；快慢列車共享軌道時，需同時辨認超高不足與超高過剩~Cant rotates the track plane to balance part of the lateral action on a curve; fixed cant balances only a particular speed, so shared tracks require both deficiency and excess to be examined',
 '合成軌距量測、超高尺與車速紀錄~synthetic gauge measurements, cant levels and speed records',
 '小傾角與剛性車體幾何，不包含懸吊滾動或輪重分配~small roll angle and rigid-body geometry, excluding suspension roll and wheel-load distribution',
 '''平衡超高計算~Equilibrium cant calculation | G[m]=1.5; v[m/s]=70; R[m]=6000; g[m/s2]=9.81 | G*v**2/(g*R)*1000 | mm | 平衡超高由向心需求和重力分量匹配求得，所用軌距應明確定義~Equilibrium cant matches centripetal demand with a gravity component, using an explicitly defined effective gauge | 有效軌距與曲線半徑~effective gauge and curve radius | 代入名義軌距卻沿用另一公式係數會產生系統差異~Mixing nominal gauge with a coefficient based on another gauge causes systematic error
超高不足辨認~Cant-deficiency calculation | eq[mm]=165; actual[mm]=125 | eq-actual | mm | 平衡需求高於實際超高時留下向外未平衡作用~A balance requirement greater than installed cant leaves an outward unbalanced action | 速度分組後的平衡需求~equilibrium demand grouped by speed | 只看安裝超高會漏掉高速通過的未平衡作用~Installed cant alone misses the unbalanced action of fast passages
超高過剩辨認~Cant-excess calculation | actual[mm]=125; eq[mm]=45 | actual-eq | mm | 慢車平衡需求較小，軌道傾斜可能使重力分量主導向內作用~A slow train has a smaller balance requirement, allowing the inward gravity component to dominate | 低速或停車時的傾斜量~cant during slow movement or a stop | 把較大超高視為所有列車都有利會忽略慢車負擔~Assuming larger cant benefits every train ignores slow-train loading
未平衡橫向加速~Unbalanced lateral acceleration | g[m/s2]=9.81; D[m]=0.04; G[m]=1.5 | g*D/G | m/s2 | 超高不足乘重力再除有效軌距可估未平衡橫向加速度~Cant deficiency times gravity divided by effective gauge estimates unbalanced lateral acceleration | 超高不足與橫向感測值~cant deficiency and lateral sensor readings | 感測器安裝傾角未校正會混入重力~Uncorrected sensor roll mixes gravity into the measurement
超高順坡梯度~Cant-ramp gradient | dh[mm]=120; L[m]=180 | dh/L | mm/m | 超高沿路線的變化形成扭轉，總超高相同時縮短順坡會加大梯度~Cant variation creates track twist; shortening a ramp increases its gradient even with unchanged total cant | 等距超高剖面~equally spaced cant profile | 接點突變會使實際扭轉集中於短區段~A discontinuity concentrates actual twist into a short section
超高變化時間率~Temporal cant rate | dh[mm]=120; L[m]=180; v[m/s]=60 | dh*v/L | mm/s | 行車速度將空間超高梯度轉換成乘客經歷的時間變化率~Train speed converts spatial cant gradient into the temporal rate experienced by occupants | 車速與順坡里程同步資料~synchronized speed and ramp chainage | 靜態合格的順坡在更高速度可能造成更快滾動~A statically acceptable ramp can produce faster roll at higher speed
不足變化時間率~Deficiency change rate | dD[mm]=50; L[m]=200; v[m/s]=70 | dD*v/L | mm/s | 超高不足沿緩和段的變化反映曲率與超高兩個剖面是否協調~Deficiency change along a transition reflects coordination of curvature and cant profiles | 曲率剖面與超高剖面的共同里程~curvature and cant profiles on shared chainage | 兩個剖面錯位時會在接點產生額外不平順~Misaligned profiles create an additional disturbance at the join
平衡速度反算~Equilibrium-speed inversion | g[m/s2]=9.81; R[m]=5000; h[m]=0.12; G[m]=1.5 | sqrt(g*R*h/G)*3.6 | km/h | 反算速度含超高平方根，超高增加不會同比例提高平衡速度~Inverted speed contains the square root of cant, so cant increase does not raise equilibrium speed proportionally | 半徑與實測超高~radius and measured cant | 線性外推速度會高估可平衡速度的增幅~Linear extrapolation overstates the increase in balance speed
混合列車均方速度~Mixed-traffic squared speed | p[1]=0.6; vf[m/s]=70; vs[m/s]=40 | p*vf**2+(1-p)*vs**2 | m2/s2 | 若以平方速度需求加權，應先平方再平均，不能先取平均速度再平方~Weighting squared-speed demand requires squaring before averaging, not squaring the mean speed | 各速度群比例與平方速度~group proportions and squared speeds | 只使用平均速度會低估平方速度的平均值~Using mean speed alone understates mean squared speed
超高量測不確定度~Cant measurement uncertainty | ul[mm]=0.5; ur[mm]=0.5 | sqrt(ul**2+ur**2) | mm | 左右軌高程差的不確定度要保留兩側誤差與相關性~Uncertainty in rail-level difference must retain both rail errors and their correlation | 左右軌交換測量的閉合差~closure from swapped left-right measurements | 儀器零點漂移可能被誤認為整段超高偏移~Instrument zero drift can resemble a cant shift along the whole segment''')

C(338,'material','底座承載溫縮排水與灌築品質~Foundation support thermal shrinkage drainage and placing quality',
 '無碴軌道底座把離散扣件作用分配到下層基礎，施工高程與長期沉陷共同決定後續可調整量；混凝土品質、排水和接縫需在同一系統內檢查~A slab-track foundation distributes discrete fastening actions to the substructure, while construction level and later settlement consume adjustment capacity; concrete quality, drainage and joints belong to one system',
 '模型載重板、溫度計與數位水準紀錄~model loading plates, temperature sensors and digital level records',
 '均勻材料與簡化支承，不代表現場灌築配比或施工指令~uniform material and simplified support, not a field mix design or placing instruction',
 '''底座平均承壓~Foundation mean pressure | P[kN]=240; A[m2]=1.2 | P/A | kPa | 合力除有效面積只給平均壓力，接觸空隙會改變實際分布~Resultant force divided by effective area gives average pressure only; voids change its actual distribution | 載重與接觸面積~load and contact area | 局部脫空會使剩餘接觸區承壓上升~Local voids increase pressure over the remaining contact area
底座幾何方量~Foundation concrete volume | L[m]=25; b[m]=3; h[m]=0.25 | L*b*h | m3 | 幾何體積是材料帳的起點，局部凹槽與預埋空間需單獨扣除~Geometric volume starts the material account, with recesses and embedded voids deducted separately | 斷面量測與供料總量~section measurements and delivered volume | 只按供料量驗收會掩蓋外溢或空洞~Acceptance by delivery volume alone can hide leakage or voids
均勻溫降收縮~Uniform cooling contraction | alpha[1/K]=0.00001; L[m]=25; dT[K]=20 | alpha*L*dT*1000 | mm | 自由溫縮由熱膨脹係數、長度及溫差相乘，約束會把部分位移轉為應力~Free thermal contraction multiplies expansion coefficient, length and temperature change; restraint converts part of it into stress | 接縫位移與平均溫度~joint movement and average temperature | 以空氣溫度代替底座溫度會錯判收縮~Air temperature used as slab temperature misrepresents contraction
約束熱應力量級~Restrained thermal stress | E[GPa]=30; alpha[1/K]=0.00001; dT[K]=15; r[1]=0.4 | E*1000*alpha*dT*r | MPa | 部分約束係數只是簡化參數，真實約束會隨開裂與徐變改變~A restraint factor is a reduced parameter; actual restraint changes with cracking and creep | 溫度剖面與受限應變~temperature profile and restrained strain | 假設完全約束或完全自由都可能偏離現場~Assuming either complete restraint or total freedom can misrepresent the site
乾縮位移估算~Drying shrinkage displacement | eps[1]=0.00025; L[m]=20 | eps*L*1000 | mm | 乾縮應變與溫縮不同，含水變化和齡期使其具有時間依賴~Drying shrinkage differs from thermal strain and depends on moisture change and age | 同溫條件下長度與含水紀錄~length and moisture records at equal temperature | 將乾縮當成量測零點漂移會漏掉接縫變化~Treating shrinkage as zero drift misses real joint movement
養護顯熱預算~Curing sensible-heat budget | m[kg]=12000; c[J/kgK]=900; dT[K]=5 | m*c*dT/1e6 | MJ | 顯熱變化不能取代水化熱與環境散熱帳，平均溫度也不能代表梯度~Sensible heat does not replace hydration and environmental heat accounts, nor does mean temperature describe gradients | 核心與表面溫度~core and surface temperatures | 表面過快冷卻會產生內外差異~Rapid surface cooling produces an internal-external mismatch
排水橫坡高差~Drainage crossfall drop | s[1]=0.02; b[m]=3 | s*b*1000 | mm | 排水坡度把橫向距離轉成高差，局部反坡仍可能積水~Crossfall converts transverse distance into level difference, while a local reverse slope can still trap water | 網格高程與低點位置~gridded elevations and low-point locations | 平均坡度正確卻存在局部窪地會積水~A correct average slope with local depressions still ponds water
基礎壓縮變形~Foundation compression | P[kN]=180; k[kN/mm]=60 | P/k | mm | 集中支承剛度以力除位移定義，不能與每面積地基係數混用~Lumped support stiffness is force per displacement and must not be confused with an area-normalized subgrade coefficient | 載重卸載循環~loading and unloading cycles | 首次壓密會讓重載前後的剛度不同~Initial compaction changes stiffness between first and repeated loading
高程修整餘量~Level adjustment reserve | range[mm]=30; construct[mm]=8; settle[mm]=12 | range-construct-settle | mm | 施工誤差與預估沉陷共同消耗後續調整範圍，餘量不能重複計算~Construction error and estimated settlement consume the same later adjustment range, so reserve cannot be counted twice | 竣工高程與沉陷趨勢~as-built levels and settlement trend | 施工階段耗盡調整量會限制後續維修~Using all adjustment during construction limits later maintenance
試件平均強度~Specimen mean strength | f1[MPa]=38; f2[MPa]=42; f3[MPa]=40 | (f1+f2+f3)/3 | MPa | 三個試件平均只描述樣本，不能推定所有底座位置均達相同性能~A three-specimen mean describes that sample and does not prove identical properties everywhere in the foundation | 取樣位置與試件破壞型態~sampling locations and specimen failure modes | 不具代表性的取樣會使漂亮平均值失去意義~Unrepresentative sampling makes an attractive average uninformative''')

C(339,'geometry','多點測量調整閉合與誤差傳播~Multi-point survey adjustment closure and uncertainty propagation',
 '軌道板精調把控制網、板體剛體位姿與扣件調整串接；若控制點與板上測點的座標基準不一致，精密讀值仍會導致錯誤的實際位置~Slab alignment connects a control network, rigid-body pose and fastening adjustment; precision readings still give the wrong physical position when control and slab coordinates use different datums',
 '合成全站儀座標、水準資料與調整螺桿位移~synthetic total-station coordinates, level data and adjustment-screw displacement',
 '小角度剛體位姿與獨立誤差，未含板體彈性扭曲~small-angle rigid-body pose and independent errors, excluding elastic slab distortion',
 '''平移偏差合成~Translation-error magnitude | dx[mm]=3; dy[mm]=4 | sqrt(dx**2+dy**2) | mm | 平面偏差是向量，兩方向符號決定修正方向而長度描述誤差量級~Plan error is a vector: component signs define correction direction while magnitude describes scale | 東北向殘差與控制點~east-north residuals and control points | 只看誤差長度而丟失方向會使調整走錯方向~Discarding direction while retaining magnitude can reverse an adjustment
板端偏轉估算~Slab yaw from endpoint offsets | dy[mm]=2; L[m]=5 | dy/(L*1000)*1000 | mrad | 兩端橫向差除板長近似偏轉角，角度不是兩端位移的平均~Endpoint lateral difference divided by length approximates yaw; it is not the mean endpoint translation | 前後測點橫向差~lateral difference between front and rear targets | 平移與轉角未分離會讓一端修正另一端惡化~Confusing translation with rotation improves one end while worsening the other
板體俯仰估算~Slab pitch estimate | dz[mm]=1.5; L[m]=5 | dz/(L*1000)*1000 | mrad | 縱向高差形成俯仰，應先扣除設計縱坡再判斷誤差~Longitudinal level difference produces pitch; subtract the design gradient before identifying error | 設計高程與實測高程差~differences between design and measured levels | 把設計坡度當板體誤差會破壞路線縱面~Treating design gradient as slab error damages the vertical alignment
調整螺距位移~Adjustment screw displacement | pitch[mm/turn]=2; turn[turn]=0.35 | pitch*turn | mm | 螺距與轉角決定位移，但間隙與受力回彈使實際變化需回測~Pitch and turns determine nominal travel, but backlash and elastic recovery require remeasurement | 單向逼近與回程差~one-direction approach and reverse-travel difference | 反覆換向會把螺紋間隙誤當板體不穩~Repeated direction reversal can mistake thread backlash for slab instability
測站角度投影~Station angle projection | R[m]=40; theta[rad]=0.00002 | R*theta*1000 | mm | 角度誤差沿視距放大成橫向誤差，長視距不一定更精確~Angular error grows into transverse error with sight distance, so a longer sight is not necessarily more precise | 視距與重複角度觀測~sight distance and repeated angular observations | 忽略視距放大會低估遠端點誤差~Ignoring distance amplification understates far-target error
棱鏡常數偏差~Prism-constant bias | measured[m]=30; bias[mm]=2 | measured*1000-bias | mm | 棱鏡常數是系統修正，不能藉增加相同觀測次數消除~A prism constant is a systematic correction and cannot be removed by repeating the same observation | 不同棱鏡互換與基線~prism interchange and a reference baseline | 錯誤常數會平移整批量測~An incorrect constant shifts the entire measurement batch
水準閉合分配~Levelling closure allocation | closure[mm]=2.4; length[m]=200; total[m]=800 | closure*length/total | mm | 按長度分配閉合差只是一種模型，需先排除粗差再調整~Allocating closure by length is one adjustment model; blunders must be excluded first | 往返高差及分段長度~forward-back level differences and segment lengths | 直接分配粗差會把錯誤散布到全部控制點~Distributing a blunder spreads error across all control points
三點高程平均~Three-point elevation mean | z1[mm]=1; z2[mm]=2; z3[mm]=3 | (z1+z2+z3)/3 | mm | 等權平均適用相近精度的獨立觀測，不適用共同基準偏差~Equal-weight averaging suits independent observations of similar precision, not shared datum bias | 點位精度與殘差~point precision and residuals | 平均值可能掩蓋板體扭曲~A mean can hide slab distortion
相鄰板接縫差~Adjacent slab joint step | end1[mm]=1.2; end2[mm]=-0.8 | end1-end2 | mm | 兩板各自偏差很小仍可能在接縫形成不利相對高差~Two small individual slab errors can still create an unfavorable relative step at a joint | 接縫兩側同時高程~simultaneous levels on both sides of the joint | 分別使用不同基準驗收會漏掉接縫跳差~Separate acceptance against different datums misses the joint step
重測平均不確定度~Repeated-survey mean uncertainty | sigma[mm]=1.2; n[count]=9 | sigma/sqrt(n) | mm | 獨立隨機誤差的平均不確定度隨樣本數平方根下降，系統偏差不隨之下降~Mean uncertainty of independent random error decreases with square-root sample count, while systematic bias remains | 不同測站而非同站重讀~independent stations rather than repeated display readings | 把同一基準的相關觀測當獨立會誇大精度~Treating correlated readings as independent exaggerates precision''')


for _record in sorted(HERE.glob("track_records_*.py")):
    exec(compile(_record.read_text(),str(_record),"exec"),globals())
exec(compile((HERE/"track_unit_context.py").read_text(),str(HERE/"track_unit_context.py"),"exec"),globals())
exec(compile((HERE/"track_metadata.py").read_text(),str(HERE/"track_metadata.py"),"exec"),globals())
for _context in sorted(HERE.glob("track_context_*.py")):
    exec(compile(_context.read_text(),str(_context),"exec"),globals())
if __name__ == "__main__":build()
