#!/usr/bin/env python3
"""Original bilingual lessons for b146–b150. Rebuilds only this assigned batch."""
import json, pathlib, importlib.util
HERE=pathlib.Path(__file__).resolve().parent
TARGETS={x['id']:x for x in json.loads((HERE/'targets.json').read_text())}
COURSES={}
def pair(z,e):return z+'~'+e
def split(s):return s.split('~')
def course(cid,focus,summary,history,text):
 units=[]
 for line in text.strip().splitlines():
  if not line.strip():continue
  p=[x.strip() for x in line.split('||')];assert len(p)==7,(cid,p)
  title,cause,model,verify,failure,misconception,practice=p
  assert all(s.count('~')==1 for s in p),(cid,title)
  zc,ec=split(cause);zm,em=split(model);zf,ef=split(failure)
  units.append(dict(title=title,anchor=title,mechanism=pair(zc+' '+zm+' '+zf,ec+' '+em+' '+ef),model=pair('教學假設，非現場設定或設計允收值。'+zm,'Teaching assumptions, not operating settings or design acceptance limits. '+em),verify=verify,failure=failure,misconception=misconception,practice=practice))
 assert len(units)==10,(cid,len(units));COURSES[cid]=dict(focus=focus,summary=summary,history=history,units=units)
S={}
def source(key,zh,en,publisher,url,scope,scope_en):S[key]=dict(key=key,title=zh,titleEn=en,publisher=publisher,url=url,sourceType='primary',scope=scope,scopeEn=scope_en)
source('ita-mainbeam','國際隧協敞開與雙護盾掘進原理','ITA main-beam and double-shield TBM principles','ITA-AITES','https://tunnel.ita-aites.org/en/how-to-go-underground/construction-methods/mechanized-tunnelling/main-beam-tbms','協會對反力路徑與掘進循環的公開說明，不是特定設備操作手冊。','Association overview of reaction paths and excavation cycles, not an operating manual for an individual machine.')
source('hk-double','海瑞克雙護盾掘進機產品技術介紹','Herrenknecht Double Shield TBM technical overview','Herrenknecht AG','https://www.herrenknecht.com/en/products/productdetail/double-shield-tbm/','已由搜尋確認官方頁與伸縮盾構造摘要；直接全文擷取受限，不引用未見的性能數字。','Official page and telescopic-shield description confirmed by search; direct full-page retrieval was restricted. No unseen performance figures are cited.')
source('hk-gripper','海瑞克撐靴式掘進機技術介紹','Herrenknecht Gripper TBM technical overview','Herrenknecht AG','https://www.herrenknecht.com/en/products/productdetail/gripper-tbm/','已由搜尋確認官方硬岩機型頁；只用作設備類型參考，直接全文擷取受限。','Official hard-rock machine page confirmed by search; used only as a machine-type reference because direct full-page retrieval was restricted.')
source('fhwa-manual','公路隧道設計施工土建技術手冊','Technical Manual for Design and Construction of Road Tunnels: Civil Elements','FHWA / US Government Publishing Office','https://www.govinfo.gov/app/details/GOVPUB-TD2-PURL-gpo93381','二〇〇九年官方手冊書目；用作隧道土建設計參考來源，未聲稱此舊手冊是現行個案規範。','Official 2009 manual record; a civil tunnel design reference, not a claim that an older manual is the current specification for a project.')
source('crossrail-scl','Crossrail噴凝土襯砌的設計觀點','Design of Sprayed Concrete Linings in Soft Ground: A Crossrail Perspective','Crossrail Learning Legacy','https://learninglegacy.crossrail.co.uk/documents/design-sprayed-concrete-linings-soft-ground%E2%94%80-crossrail-perspective/','原作者技術論文，支援施工序列、地層互制與早齡襯砌之背景，算例另列為合成假設。','Original authors technical paper supporting construction sequence, ground interaction and early-age lining context. Course calculations are separately identified as synthetic assumptions.')
source('crossrail-stepney','Stepney Green洞室襯砌設計與表現','Stepney Green Cavern: Design Concepts and Performance of SCL Lining','Crossrail Learning Legacy','https://learninglegacy.crossrail.co.uk/documents/stepney-green-cavern-design-concepts-and-performance-of-scl-lining/','原作者公開側壁導坑與襯砌觀測案例；不把案例斷面與步距移植為本課施工處方。','Original authors public side-drift and lining-monitoring case; its dimensions and advances are not transferred into a construction prescription.')
source('swiss-nrla','瑞士新阿爾卑斯鐵路連線官方背景','Swiss New Rail Link through the Alps: official background','Swiss DETEC / UVEK','https://www.uvek.admin.ch/en/nrla','政府對聖哥達基線隧道二〇一六年營運的背景資料；不聲稱每一教學方法都曾在此採用。','Government context for Gotthard Base Tunnel entering operation in 2016; no claim that every taught technique was used there.')
def make(cid,d):
 t=TARGETS[cid];u=d['units'];mechanized=cid in ('b146','b147')
 keys=(['ita-mainbeam','hk-double' if cid=='b146' else 'hk-gripper','fhwa-manual','crossrail-stepney','swiss-nrla'] if mechanized else ['crossrail-scl','crossrail-stepney','fhwa-manual'])
 facts=[]
 for v in u[:6]:
  z,e=split(v['model']);facts.append(pair(z,e))
 z1,e1=split(u[0]['model']);z2,e2=split(u[1]['model']);zf,ef=split(d['focus'])
 example=pair('以下原創算例針對'+zf+'，每個輸入都是教學假設而非地標實測資料。'+z1+z2+'兩式只回答各自所列的量與邊界，不應把單一平均結果當成整體穩定證明。請另以最不利的幾何、時間或接觸條件代入，分別標示量測誤差和模型偏差；交接記錄須保留原單位、資料日期以及未能確認的條件。',
 'This original worked example examines '+ef.lower()+'. Every input is a teaching assumption, not a measured value from a landmark. '+e1+' '+e2+' Each relation answers only its stated quantity under its stated boundary conditions. A favorable mean value is not proof of overall stability. Recalculate with an adverse geometry, timing or contact condition, distinguishing measurement uncertainty from model error. The handover record must retain original units, observation dates and conditions that remain unverified; the responsible designer decides whether additional evidence is needed.')
 marks=[pair('聖哥達基線隧道：深埋岩體背景對照','Gotthard Base Tunnel: deep-rock context'),pair('倫敦Stepney Green洞室：序列對照','London Stepney Green caverns: sequence comparison')] if mechanized else [pair('倫敦Stepney Green洞室：側導坑案例','London Stepney Green caverns: side-drift case'),pair('倫敦Heathrow Express試驗隧道','London Heathrow Express trial tunnel')]
 timeline=([{'year':'2009','event':pair('美國聯邦公路管理局出版隧道土建手冊','FHWA publishes its manual covering tunnel civil elements')},{'year':'2014','event':pair('Crossrail公開Stepney Green大型洞室設計研究論文','Crossrail publishes the Stepney Green cavern design paper')},{'year':'2016','event':pair('聖哥達基線隧道投入營運，作為深埋背景對照','Gotthard Base Tunnel enters operation as a deep-rock contextual comparison')}] if mechanized else [{'year':'1992','event':pair('Heathrow Express試驗隧道展示倫敦軟土噴凝土襯砌','The Heathrow Express trial tunnel demonstrates soft-ground sprayed lining in London')},{'year':'2009','event':pair('美國聯邦公路管理局發布隧道土建技術手冊','FHWA issues its tunnel manual covering civil engineering elements')},{'year':'2014','event':pair('Crossrail公開噴凝土設計與Stepney Green案例論文','Crossrail publishes sprayed-lining design and Stepney Green case papers')}])
 vendors=[]
 for key in keys[:1]+['fhwa-manual']:
  s=S[key];vendors.append(dict(name=s['publisher'],nameEn=s['publisher'],business='提供本課設備原理或隧道工程公開方法資料。',businessEn='Provides public machine principles or tunnel engineering methodology.',url=s['url'],investorUrl='',security=None,role=s['scope'],roleEn=s['scopeEn']))
 return dict(id=cid,title=pair(t['title'],t['titleEn']),discipline=t['discipline'],family=t['family'],focus=d['focus'],summary=d['summary'],history=d['history'],units=u,example=example,facts=facts,timeline=timeline,codes=[pair('美國聯邦公路管理局公路隧道土建技術手冊，2009','FHWA road tunnel civil-elements technical manual, 2009'),pair('國際隧協掘進方法說明：背景指引而非操作規範','ITA construction-method guidance: background rather than an operating specification') if mechanized else pair('Crossrail噴凝土襯砌設計論文，2014：案例指引','Crossrail sprayed-concrete lining design paper, 2014: case guidance')],landmarks=marks,place=dict(name=pair('倫敦Stepney Green洞室背景參照','London Stepney Green cavern context reference'),country=pair('英國','United Kingdom'),lat=51.5195,lng=-0.0440,query='Stepney Green Crossrail caverns London'),sources=[S[k] for k in keys],vendors=vendors,related=[f'b{int(cid[1:])-1:03}',f'b{int(cid[1:])+1:03}'],architectureNodes=[split(u[i]['title']) for i in (0,2,4,6,9)],architectureEdges=[[0,1],[1,2],[2,3],[3,4],[3,1]])
def main():
 for name in ('author_146_147_rows','author_148_150_rows'):
  spec=importlib.util.spec_from_file_location(name,HERE/(name+'.py'));mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);mod.author(course)
 for cid,d in COURSES.items():(HERE/'inputs'/f'{cid}.json').write_text(json.dumps(make(cid,d),ensure_ascii=False,indent=2)+'\n')
 (HERE/'research_146_150.json').write_text(json.dumps(dict(accessed='2026-10-21',courses=list(COURSES),sources=S,limitations=['All calculations are original synthetic teaching assumptions, not actual project measurements or machine settings.','Herrenknecht official URLs were search-confirmed; direct fetch was restricted.','FHWA bibliography was verified; its full 32 MB manual was not fetched.','Landmarks supply contrasting contexts, not claims that each method was used at each site.','All securities are null. No securities claim is made.']),ensure_ascii=False,indent=2)+'\n')
 print('Wrote',len(COURSES),'courses',sum(len(v['units']) for v in COURSES.values()),'units')
if __name__=='__main__':main()
