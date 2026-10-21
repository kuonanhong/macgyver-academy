#!/usr/bin/env python3
"""Reproducible authored b126–b150 inputs; numbers are original teaching assumptions."""
import json, pathlib, importlib.util, math, re
HERE=pathlib.Path(__file__).resolve().parent
T={x['id']:x for x in json.loads((HERE/'targets.json').read_text())}
D={}; S={}
def source(k,zh,en,pub,url,scope,scope_en):
 S[k]={'key':k,'title':zh,'titleEn':en,'publisher':pub,'url':url,'sourceType':'primary','scope':scope,'scopeEn':scope_en}
source('fhwa','公路隧道設計施工技術手冊','Technical Manual for Design and Construction of Road Tunnels—Civil Elements','FHWA / US Government Publishing Office','https://www.govinfo.gov/app/details/GOVPUB-TD2-PURL-gpo93381','官方二〇〇九年手冊書目；工程調查、掘進與襯砌設計的背景參考，非現行個案施工規格。','Official 2009 manual record; background for investigation, excavation and lining design, not a current project specification.')
source('geo','岩土指南二：場地勘察','Geoguide 2: Guide to Site Investigation','Hong Kong CEDD','https://www.cedd.gov.hk/eng/publications/geo/geoguides/geo-g2/','場地調查的建議良好實務及二〇一七年更新資訊；用以區分調查資料與設計推論。','Recommended investigation practice and 2017 update information; distinguishes observations from design interpretations.')
source('geo3','岩土指南三：岩土描述','Geoguide 3: Guide to Rock and Soil Descriptions','Hong Kong CEDD','https://www.cedd.gov.hk/eng/publications/geo/geoguides/geo-g3/geo-g3-version/index.html','一九八八年第一版的官方出版紀錄，支援岩心與土岩描述術語的背景。','Official record of the 1988 first edition; background for consistent soil and rock logging terminology.')
source('crossrail-geology','橫貫鐵路地質縱剖面完工更新','Crossrail Geological Long Section: Post-Construction Update','Crossrail Learning Legacy','https://learninglegacy.crossrail.co.uk/documents/crossrail-geological-long-section-post-construction-update/','鑽孔密度、偏離路線與斷層簡化造成的地層邊界不確定性；非直接施工圖。','Uncertainty from borehole spacing, offset and fault simplification; the section is not a direct construction drawing.')
source('usgs-imaging','聲學與光學孔壁成像研究','Borehole-wall imaging with acoustic and optical televiewers','US Geological Survey','https://www.usgs.gov/publications/borehole-wall-imaging-acoustic-and-optical-televiewers-fractured-bedrock-aquifer','政府研究者的孔壁影像與裂隙判釋研究，支援影像幾何與多資料交叉判讀。','Government research on borehole images and fracture interpretation, supporting image geometry and multiple evidence streams.')
source('amberg-seismic','隧道震波超前探測','Tunnel Seismic Prediction','Amberg Technologies','https://ambergtechnologies.com/solutions-services/amberg-geophysics/tunnel-seismic-prediction','儀器供應者對超前震波探測的用途說明；不以行銷範圍當作本課精度保證。','Instrument supplier explanation of ahead-of-face seismics; advertised ranges are not course accuracy guarantees.')
source('isrm-stress','岩體應力估計之品質控制','ISRM Suggested Methods for rock stress estimation—Part 4','ISRM authors / Elsevier','https://www.sciencedirect.com/science/article/abs/pii/S1365160903001242','原研究之公開摘要與書目，說明原位應力資料品質控制；未聲稱讀取付費全文。','Public abstract and metadata of the original methods paper on stress-estimation quality control; no claim of reading paywalled text.')
source('isrm-methods','岩石試驗建議方法完整目錄','ISRM Suggested Methods: complete list','International Society for Rock Mechanics and Rock Engineering','https://w.isrm.net/page/show/1305','標準組織的方法清單，用以定位應力、剪力與岩石性質試驗之方法依據。','Methods list from the professional standards organization, locating stress, shear and rock-property test guidance.')
source('gotthard-context','新阿爾卑斯鐵路連線官方介紹','New Rail Link through the Alps','Swiss DETEC / UVEK','https://www.uvek.admin.ch/en/nrla','瑞士政府對聖哥達基線隧道規模與鐵路營運背景之公開資料。','Swiss government background on the Gotthard Base Tunnel scale and rail operation.')

def pair(z,e):return z+'~'+e
def halves(v):return v.split('~')
def register(cid,focus,source_keys,text,context=None):
 rows=[]
 for line in text.strip().splitlines():
  if not line.strip():continue
  p=[x.strip() for x in line.split('||')]
  assert len(p)==7,(cid,len(p),p[0])
  assert all(x.count('~')==1 for x in p),(cid,p[0])
  title,cause,model,verify,failure,misconception,practice=p
  zc,ec=halves(cause); zm,em=halves(model); zf,ef=halves(failure)
  rows.append({'anchor':title,'title':title,'mechanism':pair(zc+' '+zm+' '+zf,ec+' '+em+' '+ef),'model':pair('以下為教學假設，非現場操作設定。'+zm,'The following are teaching assumptions, not field operating settings. '+em),'verify':verify,'failure':failure,'misconception':misconception,'practice':practice})
 assert len(rows)==10,(cid,len(rows))
 D[cid]={'focus':focus,'sources':source_keys,'units':rows,'context':context}

def compact(cid,focus,keys,text):
 rows=[]
 for line in text.strip().splitlines():
  p=[x.strip() for x in line.split('||')]
  assert len(p)==5,(cid,p)
  title,cause,model,measure,risk=p
  zt,et=halves(title);zm,em=halves(measure);zr,er=halves(risk)
  verify=pair(zm+'驗證亦須釐清下列替代解釋：'+zr,em+' Verification must also resolve this competing explanation: '+er)
  practice=pair('交接時逐項記錄'+zt+'的資料來源與適用條件。'+zm, 'At handover, document the evidence and applicable conditions for '+et.lower()+'. '+em)
  wrong=pair('只要'+zt+'的名義數值符合預期，便不必再查邊界條件與獨立證據。','An expected nominal result for '+et.lower()+' makes boundary checks and independent evidence unnecessary.')
  rows.append('||'.join([title,cause,model,verify,risk,wrong,practice]))
 register(cid,focus,keys,'\n'.join(rows))

def make(cid,d):
 t=T[cid]; zf,ef=halves(d['focus']); u=d['units']; keys=list(dict.fromkeys(d['sources']+['fhwa','crossrail-geology']))[:5]
 facts=[]
 for i in range(10):
  z,e=halves(u[i]['model']); z=z.replace('以下為教學假設，非現場操作設定。',''); e=e.replace('The following are teaching assumptions, not field operating settings. ','')
  # A fact card explicitly identifies calculated assumptions rather than project measurements.
  if len(re.findall(r'[㐀-鿿]',z))+6 <=90 and len(re.findall(r'[A-Za-z]{2,}',e))+3<=45:
   facts.append(pair('教學量化備忘：'+z,'Teaching quantitative note: '+e))
  if len(facts)==6:break
 assert len(facts)==6,(cid,'need six bounded quantitative facts')
 z1,e1=halves(u[0]['model']); z2,e2=halves(u[1]['model'])
 example=pair('原創教學算例，所有輸入是為比較機制而假設，並非任何地標的實測資料。'+z1+z2+'將第一式的一個線性乘數加倍而固定其他邊界，該項貢獻隨之加倍；若為非線性式則必須重新代入，不能等比例外推。把輸入值、單位換算、計算結果及假設列成四欄，再用獨立計算器重算；最後比較量測誤差與模型簡化，判斷改變是否足以支持工程決策。',
 'Original teaching example: all inputs are assumptions for comparing mechanisms, not measurements from a landmark project. '+e1+' '+e2+' Doubling one linear multiplicative input in the first relation while holding the remaining boundaries fixed doubles that contribution; a nonlinear relation must instead be evaluated again. Tabulate inputs, unit conversions, results and assumptions in separate columns, and recalculate independently. Finally compare measurement uncertainty with model simplification before deciding whether the difference supports an engineering decision.')
 summary=pair('本課聚焦'+zf+'。沿著調查依據、物理作用、數量估算、現場驗證到工程交接逐項建立可追溯的推論鏈，特別辨別單一數值無法揭露的空間差異及時間效應。以獨立量測檢驗簡化模型，並把觀測結果、教學假設與需要主管工程師審查的決策清楚分列。',
 'This course focuses on '+ef[0].lower()+ef[1:]+'. It develops a traceable reasoning chain from evidence and physical processes through quantitative estimates, field verification and engineering handover. Spatial variation and time effects are separated from a single nominal result. Independent observations test the simplified models, while measured evidence, teaching assumptions and decisions requiring the responsible engineer remain explicitly distinguished.')
 history=pair('美國聯邦公路管理局於2009年發行公路隧道土建技術手冊，整理調查與土建工程的公開原理；瑞士官方介紹聖哥達基線隧道長57公里並於2016年投入營運，提供深埋長隧道的工程環境對照。Crossrail於2017年公開完工後地質縱剖面，提醒讀者鑽孔密度、偏離隧道位置與簡化斷層會限制推論。這些出版節點顯示'+zf+'需要把原始紀錄和模型分開保存；地標僅供工程環境比較，本課只重建公開原理。',
 'FHWA issued its civil-elements road-tunnel manual in 2009, collecting public investigation and civil-engineering principles. Swiss government information records the 57 km Gotthard Base Tunnel entering operation in 2016, providing context for long deep tunnels. Crossrail published a post-construction geological section in 2017, explaining limitations from borehole density, offset and simplified faults. These publication milestones show why '+ef[0].lower()+ef[1:]+' requires original observations to be preserved separately from interpretations. Landmarks provide contextual comparisons only; this course reconstructs public principles.')
 # Source scope is explicit; no unsourced assertion that all taught techniques were used at a landmark.
 marks=[pair('倫敦Crossrail：公開調查與建設背景','London Crossrail: public investigation and construction context'),pair('聖哥達基線隧道：深埋岩體對照','Gotthard Base Tunnel: deep-rock comparison')]
 keys=list(dict.fromkeys(keys+['gotthard-context']))[:5]
 if 'gotthard-context' not in keys:keys[-1]='gotthard-context'
 # Universal publication references used in history are kept as documentation sources in research manifest.
 vendor_keys=[d['sources'][0],'fhwa']
 vendors=[]
 for k in vendor_keys:
  s=S[k]
  vendors.append({'name':s['publisher'],'nameEn':s['publisher'],'business':'提供本課相關方法、研究或工程手冊的機構。','businessEn':'Organization providing methods, research or engineering guidance relevant to this course.','url':s['url'],'investorUrl':'','security':None,'role':s['scope'],'roleEn':s['scopeEn']})
 return {'id':cid,'title':t['title']+'~'+t['titleEn'],'discipline':t['discipline'],'family':t['family'],'focus':d['focus'],'summary':summary,'units':u,'example':example,'history':history,'facts':facts,'timeline':[{'year':'2016','event':pair('瑞士聖哥達基線隧道投入營運，提供長隧道背景對照','The Gotthard Base Tunnel enters operation, providing a long-tunnel comparison context')},{'year':'2009','event':pair('美國聯邦公路管理局出版公路隧道土建手冊','FHWA publishes its civil-elements manual for road tunnels')},{'year':'2017','event':pair('Crossrail公開地質縱剖面完工更新與適用限制','Crossrail publishes its updated geological section and interpretation limitations')}],'codes':[pair('美國聯邦公路管理局公路隧道設計施工技術手冊，2009','FHWA Technical Manual for Design and Construction of Road Tunnels, 2009'),pair('香港岩土指南二：場地勘察，2017更新','Hong Kong Geoguide 2: Guide to Site Investigation, 2017 update')],'landmarks':marks,'place':{'name':pair('倫敦Crossrail公開背景參照點','London Crossrail public context reference'),'country':pair('英國','United Kingdom'),'lat':51.5194,'lng':-0.1056,'query':'Farringdon Elizabeth line station London'},'sources':[S[k] for k in keys],'vendors':vendors,'related':[f'b{int(cid[1:])-1:03}',f'b{int(cid[1:])+1:03}'],'architectureNodes':[[*halves(u[i]['title'])] for i in (0,2,4,6,9)],'architectureEdges':[[0,1],[1,2],[2,3],[3,4],[3,1]]}

def main():
 for p in sorted((HERE/'authoring_investigation').glob('batch*.py')):
  sp=importlib.util.spec_from_file_location(p.stem,p); mod=importlib.util.module_from_spec(sp);sp.loader.exec_module(mod);mod.author(register,source,compact)
 sp=importlib.util.spec_from_file_location('investigation_misconceptions',HERE/'authoring_investigation'/'misconceptions.py')
 mod=importlib.util.module_from_spec(sp);sp.loader.exec_module(mod)
 for cid,items in mod.DATA.items():
  for unit,misconception in zip(D[cid]['units'],items):unit['misconception']=misconception
 for cid,d in sorted(D.items()):
  course=make(cid,d)
  course['timeline'].sort(key=lambda m:m['year'])
  (HERE/'inputs'/f'{cid}.json').write_text(json.dumps(course,ensure_ascii=False,indent=2)+'\n')
 (HERE/'research_investigation.json').write_text(json.dumps({'accessed':'2026-10-21','courses':{cid:d['sources'] for cid,d in D.items()},'sources':S,'limitations':['All numerical scenarios are original teaching assumptions; no machine operating limits or project measured values are inferred.','Source pages were searched or opened; ISRM publisher abstracts and FHWA metadata were available, not all paid or large full texts.','Approximate public map point indicates context, not an entrance or work permission.','Securities are null; no unverified ticker is shown.','Landmarks are comparison contexts; no claim is made that each taught technique occurred at both landmarks.']},ensure_ascii=False,indent=2)+'\n')
 print('Wrote',len(D),'courses',sum(len(d['units']) for d in D.values()),'units')
if __name__=='__main__':main()
