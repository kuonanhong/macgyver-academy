#!/usr/bin/env python3
"""Reproducible original bilingual support/underground course authoring."""
import json, pathlib, re, runpy
P=pathlib.Path(__file__).resolve().parent
C={}
def add(cid, focus, boundary, sensitivity, rows):
    units=[line.split('§') for line in rows.strip().splitlines() if line.strip()]
    assert len(units)==10,(cid,len(units))
    assert all(len(u)==6 for u in units),cid
    C[cid]=dict(focus=focus,boundary=boundary,sensitivity=sensitivity,units=units)
def pair(s):
    assert s.count('~')==1,s
    return s.split('~')
def bi(z,e):return z+'~'+e

S={}
def src(key,title,titleEn,publisher,url,scope,scopeEn):
    S[key]=dict(key=key,title=title,titleEn=titleEn,publisher=publisher,url=url,scope=scope,scopeEn=scopeEn,sourceType='primary')
src('fhwa-road','FHWA 道路隧道土木手冊官方典藏','FHWA road-tunnel civil manual official archive','Federal Highway Administration','https://rosap.ntl.bts.gov/view/dot/50019','官方典藏確認 2009 年、作者及涵蓋工法；本課原創計算不是手冊的專案實測資料。','Official archive verifies 2009, authorship and method scope; original course calculations are not measured project data from the manual.')
src('cedd-g4','CEDD 岩洞工程指南第二版','CEDD Guide to Cavern Engineering second edition','Civil Engineering and Development Department','https://www.cedd.gov.hk/filemanager/eng/content_112/eg4_20180102.pdf','2018 年第二版公開岩洞工程指引，涵蓋地質、岩栓、噴凝土、拱架、地下水與豎井；本課只重建原理。','The 2018 second edition covers geology, bolts, shotcrete, ribs, groundwater and shafts; the course reconstructs principles only.')
src('fhwa-tomie','FHWA 隧道檢查及 TOMIE 官方入口','FHWA tunnel inspection and TOMIE portal','Federal Highway Administration','https://www.fhwa.dot.gov/bridge/inspection/tunnel/ntis.cfm','官方頁列明 2015 年 TOMIE 與資產檢查文件；是閱讀脈絡，不是本課施工允收值。','Official portal lists the 2015 TOMIE and inspection documents; reading context, not construction acceptance values for these examples.')
src('efnarc','EFNARC 噴凝土規格及試驗出版品','EFNARC sprayed-concrete publications','EFNARC','https://efnarc.org/publications','官方索引確認 1996 規格、2011 面板彎曲及 2026 試板指引；不複製標準全文。','Official index confirms the 1996 specification, 2011 panel bending and 2026 panel guidance; no standard text is reproduced.')
src('sika-tunnel','Sika 隧道材料與系統','Sika tunnel materials and systems','Sika','https://www.sika.com/en/solutions-for-projects/tunneling.html','官方分類包含噴凝土、防水、注入及岩栓材料；只比較功能，不保證任何產品適用本課假想案例。','Official classification includes shotcrete, waterproofing, injection and bolting materials; functional comparison only, without product suitability claims for hypothetical examples.')
src('sika-membrane','Sika 隧道防水系統','Sika tunnel waterproofing systems','Sika','https://www.sika.com/en/construction/waterproofing-systems/tunnel.html','官方區分排水型、承壓型及分區膜系統，並列哥達與里德貝格案例；產品適用性須另查專案要求。','Official distinction between drained, pressurized and compartment membrane systems, with Gotthard and Riedberg references; product suitability requires separate project assessment.')
src('d-bolt-study','高應力岩體吸能岩栓原始研究','Original research on energy-absorbing bolts in high-stress rock','International Journal of Rock Mechanics and Mining Sciences','https://doi.org/10.1016/j.ijrmms.2010.01.005','2010 年原始研究區分靜態、動態與現地驗證；官方索引已讀，直接 DOI 全文取回受阻。本課不用產品數值代替設計。','The 2010 original research distinguishes static, dynamic and field evidence. Publisher-indexed content was retrieved; direct DOI full-text access was blocked. Product figures are not used as design values.')
src('femern','費馬恩隧道業主施工介紹','Fehmarnbelt tunnel owner construction overview','Femern A/S','https://femern.com/the-construction/how-were-building-the-fehmarnbelt-tunnel/','業主介紹工廠、溝槽、管節及丹麥 2020、德國 2021 開工；課程數值均非其專案設計。','Owner context on factory, trench, elements and Denmark 2020/Germany 2021 construction starts; course values are not project designs.')
src('gina','Trelleborg Gina 沉管接頭密封','Trelleborg Gina immersed-tunnel seals','Trelleborg Marine and Infrastructure','https://www.trelleborg.com/en/marine-and-infrastructure/products-solutions-and-services/infrastructure/seals/gina','製造商官方元件資料，支持密封功能比較；不借用產品壓縮曲線或額定值。','Official manufacturer component information for functional comparison; no product compression curves or ratings are adopted.')
src('omega','Trelleborg Omega 次級密封','Trelleborg Omega secondary seals','Trelleborg Marine and Infrastructure','https://www.trelleborg.com/en/marine-and-infrastructure/products-solutions-and-services/infrastructure/seals/omega','官方說明次級密封、壓差與多方向位移關係，並列深中通道比較案例。','Official explanation of secondary sealing, differential pressure and multidirectional movement, with a Shenzhen-Zhongshan comparison case.')
src('paddington','Crossrail 帕丁頓車站設計','Crossrail design of Paddington Station','Crossrail Learning Legacy','https://learninglegacy.crossrail.co.uk/documents/design-of-paddington-station/','專案團隊說明永久樓板支撐連續壁及逆打選擇理由；公開索引已核實，本課另設假想數值。','Project-team explanation of permanent slabs bracing diaphragm walls and reasons for top-down construction; indexed page verified and course values independently assumed.')
src('big-dig','MassDOT 大開挖隧道與橋梁','MassDOT Big Dig tunnels and bridges','Massachusetts Department of Transportation','https://www.mass.gov/info-details/the-big-dig-tunnels-and-bridges','官方索引確認頂進、沉管與明挖等不同工法；直接頁面取回受限，不聲稱全文查閱。','Official indexed page confirms jacking, immersed and cut-and-cover methods. Direct retrieval was restricted; no full-text review is claimed.')


src('pja','PJA 頂管與微型隧道出版品','PJA pipe-jacking and microtunnelling publications','Pipe Jacking Association','https://www.pipejacking.org/publications','協會官方索引涵蓋地調、管節、荷載、公差與良好實務；課程算例非指南專案數據。','Association index covers investigation, pipes, loads, tolerances and good practice; course examples are not project data from the guides.')
src('pja-interjack','PJA 中繼站分段推進原理','PJA intermediate-jacking principles','Pipe Jacking Association','https://www.pipejacking.org/assets/pj/static/flipbook/inc/html/22.html','官方第 22 頁說明中繼站前後管列分段移動與減少後座荷載；僅作機制研究，不作操作指令。','Official page 22 explains staged movement of leading and trailing strings and reduced shaft loading; used for mechanisms rather than operating instructions.')
src('fhwa-trenchless','FHWA 非開挖工法與導向','FHWA trenchless methods and guidance','Federal Highway Administration','https://www.fhwa.dot.gov/utilities/utilitycuts/man04.cfm?device=c','官方章節說明 HDD、頂管與微型隧道及導向干擾；歷史設備範圍不當作現行能力上限。','Official chapter covers HDD, pipe jacking, microtunneling and guidance interference; historical equipment ranges are not treated as current capability limits.')
src('werrington','Network Rail 威靈頓箱涵頂進紀錄','Network Rail Werrington box-jacking account','Network Rail','https://www.networkrail.co.uk/stories/how-did-we-build-a-tunnel-within-a-tunnel-and-why/','2021 年業主紀錄確認曲線箱涵、導向隧道及鐵路施工界面；本課尺寸與荷載均另設假想。','The 2021 owner account confirms curved-box jacking, guide tunnels and rail interfaces; course dimensions and loads are separately assumed.')
src('heathwall-plan','Tideway Heathwall 2013 規劃文件','Tideway Heathwall 2013 planning statement','Thames Water / Tideway','https://tideway.london/media/1258/planning-statement_heathwall-pumping-station.pdf','第 K.4.24 節提出先沉井後托換的方案；這是 2013 規劃內容，不聲稱為最終竣工方法。','Section K.4.24 proposes caisson sinking followed by underpinning; this is a 2013 proposal, not a claim about the final as-built method.')
src('cremorne','Tideway Cremorne 豎井完工方法紀錄','Tideway Cremorne shaft-method account','Tideway','https://tideway.london/news/site-news/2020/june/cremorne-wharf-drop-shaft-excavation-complete/','2020 年業主說明咬合樁加噴凝土襯砌；本課明確列為非沉井工法對照，不能因同屬 Tideway 就當沉井實例。','The 2020 owner account describes secant piles and sprayed lining; explicitly a non-caisson comparison, not evidence that every Tideway shaft was sunk as a caisson.')

def make_unit(r,c):
    title,mechanism,calc,verify,failure,mis=r
    zt,et=pair(title);zm,em=pair(mechanism);zv,ev=pair(verify);zf,ef=pair(failure);zb,eb=pair(c['boundary'])
    return dict(anchor=bi(zt[:24],et),title=title,
      mechanism=bi(zm+' 判別這個機制時，應觀察'+zv+'；若出現'+zf+'，便須重新檢查原先假設的接觸、力或水的傳遞邊界，而不能只調整計算結果。',em+' Use the following check to discriminate the mechanism: '+ev+'. If '+ef[0].lower()+ef[1:]+', revisit the assumed contact, force or water-transfer boundary rather than merely adjusting the calculated result.'),
      model=bi('原創教學假設：'+calc+'。'+zb+' 此結果僅用來核對量綱及模型敏感度，不是專案設計值、實測紀錄或現場允收門檻。','Original teaching assumptions: '+calc+'. '+eb+' This checks dimensions and model sensitivity; it is neither measured project data nor a design or acceptance value.'),
      verify=bi(zv+'。量測須保存位置、時間及基準，讓同條件的重複結果可比較；並特別檢查「'+zf+'」是否能由這組資料區分。儀器校核與誤差估計應先於判讀，由負責技師核定該項試驗的允收和停留點。',ev+'. Retain position, time and datums for comparable repeats, specifically distinguishing this scenario: '+ef+'. Instrument checks and uncertainty estimates precede interpretation; the responsible engineer sets acceptance and hold points for this test.'),
      failure=bi(zf+'。相似表徵也可能由量測偏差造成，因此應回到'+zv+'，以獨立證據判別原因；只修補可見症狀將留下原本的傳力或滲流問題。',ef+'. Similar symptoms can arise from measurement bias: return to '+ev[0].lower()+ev[1:]+' to discriminate the cause. Treating visible symptoms alone leaves the original transfer or seepage problem unresolved.'),
      misconception=mis,
      practice=bi('將'+zv+'列為該構件的交接證據，連結到施工位置、材料批次及判讀版本。若發現'+zf+'，先保留原始紀錄並由負責技師確認處置，不能以本課算例替代核定作業計畫。','Apply the following check at handover: '+ev+'. Link results to location, material batch and interpretation version. If '+ef[0].lower()+ef[1:]+', retain original records and obtain the responsible engineer\'s disposition; this example does not replace an approved work plan.'))

def build(cid,c,T):
    t=T[cid];rows=c['units'];titles=[pair(r[0]) for r in rows];fz,fe=pair(c['focus']);bz,be=pair(c['boundary']);sz,se=pair(c['sensitivity'])
    keys=['fhwa-road','cedd-g4','fhwa-tomie']
    if cid in ('b151','b152'):keys=['fhwa-road','cedd-g4','efnarc','sika-tunnel']
    elif int(cid[1:]) in (156,157,158,163,164,165):keys.append('sika-tunnel')
    if cid=='b157':keys.append('sika-membrane')
    if cid in ('b160','b161'):keys.append('d-bolt-study')
    if cid in ('b166','b167'):keys+=['paddington','big-dig']
    if cid in ('b168','b169','b170'):keys=['fhwa-road','cedd-g4','femern','gina','omega']
    if cid=='b171':keys=['fhwa-road','cedd-g4','pja','fhwa-trenchless','werrington']
    if cid in ('b172','b173'):keys=['fhwa-road','cedd-g4','pja','pja-interjack','fhwa-trenchless']
    if cid=='b174':keys=['fhwa-road','cedd-g4','fhwa-trenchless']
    if cid=='b175':keys=['fhwa-road','cedd-g4','heathwall-plan','cremorne']
    sources=[S[k] for k in keys]
    summary=bi('本課以'+fz+'為主線，從'+titles[0][0]+'與'+titles[1][0]+'建立系統邊界，再把'+titles[4][0]+'、'+titles[6][0]+'連到'+titles[9][0]+'。'+bz+' 十單元以可核算的模型和可追溯證據逐步判讀不同失效。','This course focuses on '+fe[0].lower()+fe[1:]+'. It begins with '+titles[0][1]+' and '+titles[1][1]+', links '+titles[4][1]+' and '+titles[6][1]+', and ends with '+titles[9][1]+'. '+be+' Ten units use reproducible models and traceable evidence to distinguish failure mechanisms.')
    example=bi('整合算例所有輸入均為教學假設。首先檢查'+titles[0][0]+'：'+rows[0][2]+'；再獨立檢查'+titles[1][0]+'：'+rows[1][2]+'。'+sz+' 兩個結果不能自動組成完整設計，因為'+bz+' 將'+pair(rows[7][3])[0]+'作為模型以外的驗證證據，並保留原始紀錄與尚待確認的邊界。','All inputs in this integrated example are teaching assumptions. First check '+titles[0][1]+': '+rows[0][2]+'. Independently check '+titles[1][1]+': '+rows[1][2]+'. '+se+' The two results are not a complete design because '+be[0].lower()+be[1:]+' Use '+pair(rows[7][3])[1].lower()+' as evidence independent of the calculation, retaining raw records and unverified boundaries.')
    history=bi('本課討論的'+fz+'，反映地下工程由單一構件強度走向地層、施工時序與維護共同驗證的發展。'+bz+' 1992 年 CEDD 岩洞指南初版、2009 年 FHWA 隧道土木手冊及 2018 年岩洞指南第二版提供公開閱讀脈絡。哥達與英法海底隧道僅作地質及地下水邊界的比較，本課不主張取得其專有圖說或現場數據，只重建公開原理。','The focus on '+fe.lower()+' reflects the development from isolated member strength toward combined ground, sequence and maintenance verification. '+be+' The 1992 first CEDD cavern guide, 2009 FHWA civil tunnel manual and 2018 second cavern-guide edition provide public context. Gotthard and the Channel Tunnel are comparisons of geological and groundwater boundaries only. This course claims no proprietary drawings or field data and reconstructs public principles.')
    facts=[bi('假想檢核 '+str(i+1)+'：'+titles[i][0]+'；'+rows[i][2],'Assumed check '+str(i+1)+': '+titles[i][1]+'; '+rows[i][2]) for i in range(6)]
    facts += ['CEDD 岩洞指南第二版出版於 2018 年，並非本課的實測報告~CEDD issued its second cavern guide in 2018; it is not a measurement report for these examples','FHWA 官方典藏將隧道土木手冊出版日期記為 2009 年~The FHWA official archive dates the civil tunnel manual to 2009']
    vendors=[dict(name=s['publisher']+'（公開資料機構）',nameEn=s['publisher'],business='提供地下工程公開技術指引與系統分類。',businessEn='Provides public underground-engineering guidance and system classification.',url=s['url'],investorUrl='',security=None,role='以其資料研究'+titles[2][0]+'與驗證證據，不表示承攬本課假想案例。',roleEn='Study '+titles[2][1]+' and verification evidence through its publications; no role in hypothetical projects is implied.') for s in (sources[1],sources[-1])]
    d=dict(id=cid,title=t['title']+'~'+t['titleEn'],discipline=t['discipline'],family=t['family'],focus=c['focus'],summary=summary,units=[make_unit(r,c) for r in rows],example=example,history=history,facts=facts,timeline=[dict(year='1992',event='CEDD 出版岩洞工程指南第一版，建立公開技術框架~CEDD publishes its first cavern-engineering guide as a public technical framework'),dict(year='2009',event='FHWA 隧道土木手冊彙整多類開挖及襯砌工法~The FHWA civil tunnel manual consolidates excavation and lining methods'),dict(year='2018',event='CEDD 第二版岩洞指南更新地層與支護評估脈絡~The second CEDD cavern guide updates ground and support assessment')],codes=['FHWA 道路隧道設計與施工土木技術手冊~FHWA Technical Manual for Design and Construction of Road Tunnels - Civil Elements','CEDD 岩土指南第四冊：岩洞工程第二版~CEDD Geoguide 4: Guide to Cavern Engineering second edition'],landmarks=['哥達基線隧道（地質邊界比較）~Gotthard Base Tunnel (geological-boundary comparison)','英法海底隧道（地下水邊界比較）~Channel Tunnel (groundwater-boundary comparison)'],place=dict(name='香港 CEDD 公開工程資料參照點~Hong Kong CEDD public engineering reference',country='香港~Hong Kong',lat=22.3204,lng=114.1794,query='Civil Engineering and Development Building 101 Princess Margaret Road Hong Kong'),sources=sources,vendors=vendors,related=[f'b{151+(int(cid[1:])-150)%25}',f'b{151+(int(cid[1:])-149)%25}'],architectureNodes=[titles[i] for i in (0,2,4,6,9)],architectureEdges=[[0,1],[1,2],[2,3],[3,4],[0,3]])
    if cid in ('b166','b167'):
        d['landmarks']=['波士頓大開挖（多工法界面比較）~Boston Big Dig (multiple-method interface comparison)','Crossrail 帕丁頓車站（逆打比較）~Crossrail Paddington Station (top-down comparison)']
        d['history']=history.replace('哥達與英法海底隧道僅作地質及地下水邊界的比較','大開挖公開資料列有明挖、沉管與頂進；帕丁頓專案團隊則說明永久樓板支撐連續壁的逆打選擇理由').replace('Gotthard and the Channel Tunnel are comparisons of geological and groundwater boundaries only.','Big Dig public information lists cut-and-cover, immersed and jacked works; the Paddington project team explains choosing top-down construction with permanent slabs bracing diaphragm walls.')
    if cid in ('b168','b169','b170'):
        d['landmarks']=['費馬恩隧道（預製與海事介面比較）~Fehmarnbelt tunnel (fabrication and marine interface comparison)','深中通道（接頭密封功能比較）~Shenzhen-Zhongshan Link (joint-sealing function comparison)']
        d['history']=history.replace('哥達與英法海底隧道僅作地質及地下水邊界的比較','費馬恩業主公開工廠、溝槽與管節施工脈絡，深中通道則列於密封製造商案例；兩者僅作工法與界面比較').replace('Gotthard and the Channel Tunnel are comparisons of geological and groundwater boundaries only.','Femern describes factory, trench and element interfaces, while the seal manufacturer lists the Shenzhen-Zhongshan Link. They are method and interface comparisons only.')
        d['timeline']=[dict(year='2009',event='FHWA 隧道土木手冊納入沉管工法的公開閱讀框架~The FHWA civil tunnel manual includes an immersed-tunnel reading framework'),dict(year='2020',event='費馬恩業主記錄丹麥側工程於此年開始施工~Femern records the construction start on the Danish side'),dict(year='2021',event='費馬恩業主記錄德國側工程於此年開始施工~Femern records the construction start on the German side')]
        d['place']=dict(name='費馬恩丹麥側公開參照點~Fehmarnbelt Danish public reference',country='丹麥~Denmark',lat=54.651,lng=11.353,query='Fehmarnbelt tunnel Rodbyhavn public information centre')
    if cid in ('b171','b172','b173','b174'):
        d['landmarks']=['威靈頓鐵路下穿（箱涵與管線界面比較）~Werrington railway underpass (box and pipeline interface comparison)','一般城市管線走廊（教學場景，非指定工程）~Generic urban utility corridor (teaching scenario, not a named project)'] if cid=='b171' else ['一般城市管線走廊（教學場景，非指定工程）~Generic urban utility corridor (teaching scenario, not a named project)','假想接收井（邊界比較，非指定工程）~Hypothetical receiving shaft (boundary comparison, not a named project)']
        d['history']=history.replace('哥達與英法海底隧道僅作地質及地下水邊界的比較','FHWA 公開章節區分 HDD、頂管與微型隧道，PJA 資料提供管列荷載與公差的閱讀脈絡；城市管線走廊為假想場景').replace('Gotthard and the Channel Tunnel are comparisons of geological and groundwater boundaries only.','FHWA distinguishes HDD, pipe jacking and microtunneling; PJA provides reading context for pipe loads and tolerances. The urban utility corridor is a hypothetical setting.')
        if cid=='b174':d['history']=d['history'].replace('，PJA 資料提供管列荷載與公差的閱讀脈絡','，並說明導向感測與磁場干擾').replace('; PJA provides reading context for pipe loads and tolerances',' and describes guidance sensing and magnetic interference')
        if cid=='b171':
            d['place']=dict(name='威靈頓鐵路下穿公開參照點~Werrington railway underpass public reference',country='英國~United Kingdom',lat=52.620,lng=-0.286,query='Werrington dive under Peterborough Network Rail')
            d['timeline'][-1]=dict(year='2021',event='Network Rail 公開威靈頓曲線箱涵頂進與導向隧道紀錄~Network Rail publishes its Werrington curved-box jacking and guide-tunnel account')
    if cid=='b175':
        d['landmarks']=['Heathwall（2013 沉井規劃，非竣工證明）~Heathwall (2013 caisson proposal, not as-built evidence)','Cremorne（樁加噴凝土，非沉井對照）~Cremorne (piles and sprayed lining, non-caisson comparison)']
        d['history']=history.replace('哥達與英法海底隧道僅作地質及地下水邊界的比較','Heathwall 2013 規劃提出沉井後轉托換，並非竣工證明；Cremorne 2020 紀錄採樁加噴凝土，特列為非沉井對照').replace('Gotthard and the Channel Tunnel are comparisons of geological and groundwater boundaries only.','The Heathwall 2013 proposal combines caisson sinking and underpinning and is not as-built evidence. The Cremorne 2020 account describes piles plus sprayed lining and is expressly a non-caisson comparison.')
        d['place']=dict(name='Heathwall 公開規劃參照點~Heathwall public planning reference',country='英國~United Kingdom',lat=51.484,lng=-0.139,query='Heathwall Pumping Station London Tideway')
        d['timeline']=[dict(year='2009',event='FHWA 公開隧道土木手冊提供地下工程閱讀框架~The FHWA civil tunnel manual provides an underground-engineering reading framework'),dict(year='2013',event='Heathwall 規劃文件提出沉井及托換方案，非竣工紀錄~The Heathwall planning statement proposes caisson and underpinning methods, not an as-built record'),dict(year='2020',event='Cremorne 業主紀錄樁與噴凝土工法，作為非沉井對照~The Cremorne owner records piles and sprayed lining as a non-caisson comparison')]
    return d

def main():
    for path in sorted(P.glob('support_rows_*.py')):
        runpy.run_path(str(path),init_globals={'add':add})
    T={x['id']:x for x in json.loads((P/'targets.json').read_text())}
    for cid,c in sorted(C.items()):
        (P/'inputs'/f'{cid}.json').write_text(json.dumps(build(cid,c,T),ensure_ascii=False,indent=2)+'\n')
    (P/'research_support.json').write_text(json.dumps(dict(reviewed='2026-10-21',courses=sorted(C),sources=list(S.values()),limits=['All numeric examples are original assumptions, not measured project data.','Public sources support the principles and publication context; no proprietary construction documents are claimed.','No listed security was reverified: security remains null.']),ensure_ascii=False,indent=2)+'\n')
    print('Wrote',len(C),'courses',sum(len(x['units']) for x in C.values()),'units')
if __name__=='__main__':main()
