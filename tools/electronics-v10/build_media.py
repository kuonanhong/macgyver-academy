#!/usr/bin/env python3
"""Build V10 licensed-media overlays and original bilingual evidence maps.
No network needed: reviewed manifests and local photo files are canonical inputs.
The original written video guides summarize linked primary descriptions, not a
claimed viewing/transcription. Videos are never downloaded or rehosted.
"""
import json,re,html,hashlib,shutil,textwrap
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; HERE=Path(__file__).resolve().parent
P=HERE/'media-research'; ASSETS=ROOT/'public/academy/assets/photos'; DIAG=ROOT/'public/academy/assets/diagrams';DIAG.mkdir(exist_ok=True)
read=lambda p:json.loads(p.read_text());write=lambda p,d:p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
clean=lambda s:html.unescape(re.sub('<[^>]+>','',str(s))).strip()
metadata={r['title'][5:]:r['imageinfo'][0] for fn in ['selected.json','selected-more.json'] for r in read(P/fn) if r.get('imageinfo')}
downloads={r['title']:r for r in read(P/'downloads.json') if r.get('file')}
courses=read(HERE/'media-course-baseline.json'); sourcebase={r['id']:r for r in read(HERE/'media-source-baseline.json')};byid={c['id']:c for c in courses}
photos=[]
for line in (HERE/'photo-specs.txt').read_text().splitlines():
 filename,slug,zh,en,ids,note,noteEn=line.split('|');i=metadata[filename];em=i['extmetadata'];author=clean(em.get('Artist',{}).get('value',''));assert author
 lic=em['LicenseShortName']['value'];assert lic.startswith(('CC BY','CC0')) or lic=='Public domain';assert 'NC'not in lic
 licenseUrl=em.get('LicenseUrl',{}).get('value','')
 if not licenseUrl:licenseUrl='https://creativecommons.org/publicdomain/zero/1.0/' if lic=='CC0' else 'https://commons.wikimedia.org/wiki/Template:PD-self'
 if slug=='fiber-alignment':author='Per Henning / NTNU, Faculty of Natural Sciences and Technology'
 ext=Path(filename).suffix.lower();path='assets/photos/v10-'+slug+ext;target=ROOT/'public/academy'/path
 src=P/'downloaded'/downloads[filename]['file']
 if src.exists():shutil.copyfile(src,target)
 assert target.is_file() and hashlib.sha256(target.read_bytes()).hexdigest()==downloads[filename]['sha256']
 courseids=ids.split(',');context={cid:{'note':note,'noteEn':noteEn} for cid in courseids}
 photos.append({'id':'v10-'+slug,'title':zh,'titleEn':en,'author':author,'license':lic,'licenseUrl':licenseUrl,'sourceUrl':i['descriptionurl'],'downloadUrl':i.get('thumburl',i['url']).split('?')[0],'originalSourceCredit':clean(em.get('Credit',{}).get('value','')),'path':path,'sha256':downloads[filename]['sha256'],'courseIds':courseids,'categories':list(dict.fromkeys(byid[c]['category'] if c in byid else 'electronics' for c in courseids)),'courseContext':context,'note':note,'noteEn':noteEn,'attribution':author+' — '+en+' — '+lic,'changes':'Commons thumbnail copied without scene editing. Display may scale or crop; open the local original for its full frame.','changesZh':'直接複製 Commons 縮圖，未修改場景；版面可能縮放或裁切，可開啟本地圖片看完整構圖。','representative':True,'verifiedAt':'2026-10-14','mediaType':'radiograph' if slug=='pcb-xray' else 'micrograph' if slug in ['oxide-etch-defect','cmos-bonds','solder-paste-macro','rf-pa-module','beam-lead'] else 'photograph','verification':{'method':'Commons imageinfo/file metadata checked for author, commercial-compatible license and context; local image visually reviewed in contact sheet; exact bytes identified by SHA-256.','downloaded':True,'visuallyReviewed':True}})
# Canonical video records: exact title/channel come from saved oEmbed responses.
videos={};sources=[]
for v in read(HERE/'video-specs.json'):
 o=read(P/('video-'+v['youtubeId']+'.json'));vid=v['youtubeId'];v=dict(v);v.update(id='v10-video-'+v.pop('slug'),titleEn=o['title'],originalTitle=o['title'],author=o['author_name'],authorUrl=o['author_url'],url='https://www.youtube.com/watch?v='+vid,embedUrl='https://www.youtube-nocookie.com/embed/'+vid,language='en',fallbackUrl='https://www.youtube.com/watch?v='+vid,captionNote='字幕與翻譯由原平台提供；下列中英重點由本學院依官方介紹另行撰寫，不是逐字稿或時間軸。',captionNoteEn='Captions and translations depend on the source platform. The bilingual points are original academy guides based on official descriptions, not a transcript or timestamped account.',before='先讀本課的原理與材料邊界，再把影片作為跨工序背景。',beforeEn='Read this course’s principles and material boundaries before using the video as process context.',after='寫下影片能支持的一項結論、仍缺的一種量測，以及該結論不適用的材料或結構。',afterEn='Record one supported conclusion, one missing measurement and a material or structure to which the conclusion does not apply.',rights='Official external player/link only. Copyright remains with the publisher. No download, clipping, transcript or rehosting license is claimed.',verification={'checkedAt':'2026-10-14','method':'Exact title/channel and iframe HTML verified by YouTube oEmbed; official video description or linked publisher article checked. No claimed full-video viewing.','oembedVerified':True,'playbackTested':False,'summaryBasis':'Original editorial study points derived from linked official descriptions and primary technical pages; not a transcript.','availabilityNote':'Player access, login requests, regional restrictions and captions remain under the provider’s control.'})
 for s in v['sources']:
  sid='v10-media-'+hashlib.sha256(s['url'].encode()).hexdigest()[:12];s['id']=sid
  if not any(x['id']==sid for x in sources):sources.append(s|{'scope':'官方影片介紹或原理來源；中英導讀由學院另行撰寫，沒有重製影片、逐字稿或廠商圖。','scopeEn':'Official video descriptions or technical principles; bilingual guides are independently authored without reproducing video, transcripts or vendor figures.'})
 videos[vid]=v
# A few existing official videos supply fabrication/lithography background.
existing=read(ROOT/'public/academy/data/media.json')['courses']
for entry in existing:
 for v in entry.get('videos',[]):
  if v.get('youtubeId')in ['Z-E5IUozd7M','h_zgURwr6nA','ST_1krgYni4'] and v['youtubeId']not in videos:videos[v['youtubeId']]=v
# Store V9 reusable video records, so a later rebuild does not depend on integrated metadata.
basefile=HERE/'media-existing-videos.json'
if not basefile.exists():write(basefile,{k:v for k,v in videos.items() if not v['id'].startswith('v10-')})
videos.update(read(basefile))
def video_for(c):
 cid=c['id'];n=int(cid[1:]) if re.fullmatch(r'a\d{3}',cid) else 0
 if c['category']=='semiconductor':
  if n in range(61,71):return 'YhbUOq5oaes'
  if n in range(11,31) or n in range(51,61) or n in range(71,78) or cid=='sub2nm':return '4G8wXQGEBrA'
  if n in range(35,51):return 'h_zgURwr6nA'
  return 'Z-E5IUozd7M'
 if n in [124,127]:return '_T-mh72VRIY'
 if n in [185,190,191,192,193,194,200]:return 'ykfong1WNU8'
 if n in range(151,196) or cid=='silicon-photonics':return 'pk7yLLw3zAU'
 if n in range(146,151):return 'CAKWkOuoWrs'
 return 'VSX-tFSwCtE'
def short(s,limit=220):
 s=str(s or '').strip();return s if len(s)<=limit else s[:limit].rsplit(' ',1)[0]+'…'
def unit(s,en=False):return re.split(r'\s*[｜|]\s*',s.get('titleEn'if en else'title',''))[0]
def family(c):
 n=int(c['id'][1:])if re.fullmatch(r'a\d{3}',c['id']) else 0
 if c['id']=='silicon-photonics' or n in range(151,201):return 4
 if n in range(146,151) or n in [69,70,95,96,97]:return 6
 if n in range(103,146) or c['id']=='packaging':return 5
 if n in range(21,31) or c['id']=='sub2nm':return 7
 if n in range(31,51):return 3
 if n in range(11,21) or n in range(51,79):return 1
 if n in range(91,95) or n in range(3,8):return 2
 return 8
# Original learning diagrams. Their geometry illustrates inquiry relationships,
# not equipment specifications, device layout or an unverified manufacturing SOP.
def diagram(c,en=False):
 esc=lambda s:html.escape(str(s),quote=True);title=c['titleEn'if en else'title'];st=c['selectedSteps'];labels=[unit(st[i],en)for i in [0,1,2,4]];f=family(c)
 bg='#f6f8fb';ink='#14243b';blue='#2065aa';teal='#168478';gold='#bf8c29'
 svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="800" viewBox="0 0 1200 800" role="img" aria-labelledby="title desc"><title id="title">{esc(title)} — {"evidence map" if en else "證據關係圖"}</title><desc id="desc">{esc("Original conceptual learning map. Not a manufacturer drawing or to scale." if en else "原創概念學習圖。非廠商圖面，非比例工程圖。")}</desc><rect width="1200" height="800" fill="{bg}"/><defs><marker id="arrow" markerWidth="9" markerHeight="9" refX="7" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8Z" fill="{teal}"/></marker></defs>']
 def txt(x,y,s,size=20,color=ink,width=32):
  lines=textwrap.wrap(s,width=width,break_long_words=True)or['']
  for i,line in enumerate(lines[:4]):svg.append(f'<text x="{x}" y="{y+i*(size+7)}" font-family="system-ui,sans-serif" font-size="{size}" fill="{color}">{esc(line)}</text>')
 txt(46,45,('ENGINEERING EVIDENCE / '+c['id'].upper()),16,teal,80);txt(46,85,title,25,ink,64 if en else 36)
 # Four course-specific technical nodes; the map asks students to establish evidence, not follow an implied production order.
 positions=[(40,200),(810,200),(40,510),(810,510)];heads=(['MODEL','OBSERVE','DISCRIMINATE','ACCEPT / HOLD']if en else['建立模型','規劃觀察','區分機制','接受／暫緩'])
 for i,((x,y),lab)in enumerate(zip(positions,labels)):
  svg.append(f'<rect x="{x}" y="{y}" width="350" height="155" rx="16" fill="white" stroke="#ced9e6" stroke-width="2"/>');txt(x+22,y+30,f'{i+1:02}  '+heads[i],16,teal,32);txt(x+22,y+67,lab,20,ink,27 if en else 14)
 for x1,y1,x2,y2 in [(390,277,488,323),(810,277,712,323),(390,587,488,447),(810,587,712,447)]:svg.append(f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{teal}" stroke-width="3" fill="none" marker-end="url(#arrow)"/>')
 # Different inquiry families have independently drawn central symbols.
 if f==1:
  for j,(co,w)in enumerate([(blue,230),(gold,190),(teal,250),(blue,210)]):svg.append(f'<rect x="{600-w/2}" y="{304+j*35}" width="{w}" height="24" rx="4" fill="{co}" opacity=".85"/>')
 elif f==2:
  svg.append(f'<circle cx="600" cy="382" r="105" fill="#dce9f4" stroke="{blue}" stroke-width="4"/>')
  for x,y in [(600,310),(540,348),(660,348),(540,415),(660,415),(600,460),(600,382)]:svg.append(f'<circle cx="{x}" cy="{y}" r="8" fill="{teal}"/>')
  svg.append(f'<path d="M510 475 L540 448" stroke="{gold}" stroke-width="7"/>')
 elif f==3:
  svg.append(f'<path d="M510 400 L560 400 L560 345 L630 345 L630 410 L695 410" fill="none" stroke="{blue}" stroke-width="11"/><path d="M510 420 L580 420 L580 366 L650 366 L650 434 L695 434" fill="none" stroke="{gold}" stroke-width="4" stroke-dasharray="7 5"/>')
 elif f==4:
  svg.append(f'<path d="M475 383 H545 C570 300 630 300 655 383 H725 M545 383 C570 465 630 465 655 383" fill="none" stroke="{blue}" stroke-width="8"/><circle cx="600" cy="383" r="44" fill="none" stroke="{teal}" stroke-width="6"/>')
 elif f==5:
  for j in range(3):svg.append(f'<rect x="{510+j*14}" y="{300+j*45}" width="180" height="32" rx="4" fill="{[blue,teal,gold][j]}"/>')
  svg.append(f'<rect x="480" y="442" width="250" height="20" fill="{ink}"/>')
  for x in range(499,722,28):svg.append(f'<circle cx="{x}" cy="478" r="7" fill="{gold}"/>')
 elif f==6:
  svg.append(f'<path d="M490 468 H723 M493 465 V289" stroke="{ink}" fill="none" stroke-width="3"/><path d="M500 440 L527 440 L527 328 L567 328 L567 440 L607 440 L607 328 L650 328 L650 440 L706 440" stroke="{teal}" fill="none" stroke-width="6"/>')
 elif f==7:
  svg.append(f'<rect x="490" y="430" width="230" height="40" fill="{blue}"/><path d="M515 420 V330 H688 V420" stroke="{gold}" fill="none" stroke-width="20"/>')
  for y in [357,382,407]:svg.append(f'<rect x="540" y="{y}" width="120" height="12" rx="6" fill="{teal}"/>')
 else:
  svg.append(f'<rect x="490" y="304" width="220" height="163" rx="16" fill="white" stroke="{blue}" stroke-width="4"/>')
  for x in [520,582,644]:svg.append(f'<rect x="{x}" y="330" width="42" height="50" rx="5" fill="{teal}"/>')
  svg.append(f'<path d="M513 422 H691" stroke="{gold}" stroke-width="10"/>')
 txt(440,165,('RELATIONS TO VERIFY'if en else'待驗證的關係'),18,teal,40)
 txt(430,600,('Concept symbol only'if en else'中央圖示僅表達概念'),16,ink,35)
 txt(46,710,('Observe → compare → record uncertainty → justify a decision'if en else'觀察 → 比較 → 記錄不確定度 → 提出可審查判斷'),18,ink,105)
 txt(46,751,('Original academy learning map · not a process recipe or manufacturer drawing · not to scale'if en else'學院原創學習架構圖 · 非量產流程／廠商圖面 · 非比例圖'),15,'#5c687a',120)
 svg.append('</svg>');return ''.join(svg)
entries=[]
for c in courses:
 cid=c['id'];steps=c['selectedSteps'];ss=[steps[i]for i in [0,2,4]];sids=list(dict.fromkeys(c['sourceIds']+[sid for st in ss for sid in st['sourceIds']]));refs=[sourcebase[sid]for sid in sids if sid in sourcebase][:6]
 # The knowledge content is previously authored academy material, not copied external prose.
 k=ss[0].get('knowledge')or[];principle=k[0].get('text','')if k else ss[0]['objective'];principleEn=k[0].get('textEn','')if k else ss[0]['objectiveEn']
 guide={'id':'v10-observation-'+cid,'title':c['title']+'：影像判讀與證據工作簿','titleEn':c['titleEn']+': visual evidence workbook','concept':'先用「'+unit(ss[0])+'」建立判讀邊界。'+short(principle,280)+' 照片說明外觀，概念圖說明學習關係；真正材料組成、性能與製程窗口需由本課的獨立量測與官方資料確認。','conceptEn':'Begin with '+unit(ss[0],True)+' to define the interpretation boundary. '+short(principleEn,430)+' Photographs show appearance and the map shows learning relationships; composition, performance and process windows require independent measurements and course references.','procedure':[f'觀察站 {i+1}｜{unit(s)}：{short(s["observation"],190)}'for i,s in enumerate(ss)],'procedureEn':[f'Observation station {i+1} | {unit(s,True)}: {short(s["observationEn"],300)}'for i,s in enumerate(ss)],'evidence':['逐圖記錄來源、材料身分、可見結構、不可見界面與可用尺度；未知處填「未證實」。','為「'+unit(ss[1])+'」建立對照：同一基準下比較兩個樣本，列出單位、採樣位置、誤差來源及競爭解釋。','以「'+unit(ss[2])+'」整理接受／暫緩證據；保留原始觀察及推論兩欄，不以模擬畫面當成實測。'],'evidenceEn':['For each image record source, material identity, visible structures, hidden interfaces and available scale; mark unknowns as unverified.','Build a controlled comparison for '+unit(ss[1],True)+': use a common reference, two samples, units, sampling locations, uncertainty sources and competing explanations.','Use '+unit(ss[2],True)+' to organize accept/hold evidence. Separate raw observations from inference; a simulation image is not a measurement.'],'pitfalls':[short(ss[0]['failure'],210),short(ss[1]['failure'],210),'官方展示影片的畫面與本課專有製程不必相同；不要把通用示例當成產品認證。'],'pitfallsEn':[short(ss[0]['failureEn'],350),short(ss[1]['failureEn'],350),'An official demonstration need not show this course’s exact process; a general example is not product qualification.'],'sources':refs,'sourceIds':sids,'basis':'Original observation prompts built from the academy’s sourced V8/V9 units; no manufacturer text or figures reproduced.','diagram':{'path':'assets/diagrams/v10-'+cid+'.svg','pathEn':'assets/diagrams/v10-'+cid+'-en.svg','title':c['title']+'：概念與證據關係','titleEn':c['titleEn']+': concepts and evidence','alt':'本課四個技術單元與建模、觀察、診斷、放行證據之間的關係。','altEn':'Relationships among four technical units and model, observation, diagnosis and acceptance evidence.','original':True,'notToScale':True,'kind':'learning-evidence-map','family':family(c)}}
 for en in [False,True]:(DIAG/('v10-'+cid+('-en'if en else'')+'.svg')).write_text(diagram(c,en))
 v=dict(videos[video_for(c)]);v['id']='v10-'+cid+'-'+v['youtubeId'];v['scope']='本課「'+c['title']+'」的延伸背景。'+v.get('scope','')+' 影片並非本課每一道步驟的實拍。';v['scopeEn']='Related background for '+c['titleEn']+'. '+v.get('scopeEn','')+' It is not footage of every step in this course.'
 # Original focus questions link the shared background video to this unique topic.
 v['before']='先問：「'+unit(ss[0])+'」需要哪種材料或介面證據？畫出本課與影片案例的共同處及不同處。';v['beforeEn']='Ask what material or interface evidence '+unit(ss[0],True)+' requires. Draw the common ground and differences between this course and the video case.'
 v['after']='把「'+unit(ss[1])+'」列為查證任務：'+short(ss[1]['observation'],170);v['afterEn']='Follow-up evidence task for '+unit(ss[1],True)+': '+short(ss[1]['observationEn'],260)
 entries.append({'courseId':cid,'title':c['title'],'titleEn':c['titleEn'],'videos':[v],'guides':[guide]})
out={'version':10,'photos':photos,'courses':entries,'sources':sources,'scope':'31 additional licensed photographs/micrographs/radiograph; 199 bilingual original evidence workbooks and 398 language-specific learning maps. Seven newly verified official YouTube videos plus clearly scoped existing background videos. No claim of unique footage per step, full-video viewing, manufacturer endorsement, or production-ready recipes.','verification':{'checkedAt':'2026-10-14','photoCount':len(photos),'courses':len(entries),'originalDiagramTopics':len(entries),'svgLanguageFiles':len(entries)*2,'newDistinctVideos':7,'totalSelectedVideoIds':len({v['youtubeId']for e in entries for v in e['videos']}),'playbackTested':False}}
write(HERE/'media.json',out)
licenseText='V10 LICENSED MEDIA\n\nPhotos are separately licensed assets. CC BY-SA conditions apply to adaptations of those photos, not automatically to unrelated software or other independent collection items. Preserve attribution, source, license and change notices when redistributing. No endorsement is implied.\n\n'+'\n\n'.join(p['id']+'\n'+p['attribution']+'\nSource: '+p['sourceUrl']+'\nLicense: '+p['licenseUrl']+'\nChanges: '+p['changes']+'\nSHA256: '+p['sha256']for p in photos)+'\n\nOriginal SVG evidence maps: MacGyver Engineering Academy, 2026. These are independently authored learning maps, not vendor drawings.\n'
(ASSETS/'V10-LICENSES.txt').write_text(licenseText)
print(json.dumps(out['verification'],ensure_ascii=False))
