#!/usr/bin/env python3
"""Publish traceable real-photo scene assignments without claiming exact scenes."""
from pathlib import Path
import collections, hashlib, json, re
from PIL import Image

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
PUBLIC=ROOT/'public/academy'
DEFAULTS={'semiconductor':'cleanroom','packaging':'v9-photonic-assembly','electronics':'v10-pick-place-machine',
 'computing':'v3-network-switches','instruments':'v9-optical-table','structures':'danjiang','underground':'hsuehshan',
 'water':'hoover-dam','rail':'v16-thsr','environment':'v16-wastewater','aerospace':'v6-a350','marine':'v6-alvin',
 'automotive':'tesla','space':'webb','manufacturing':'v16-robot','energy':'v6-hoover-generator',
 'materials':'v16-material-test','biomedical':'v16-ct','process':'v16-industrial','megascience':'v6-atlas'}

# Exact refers to the named asset/subject, never to a current operational state,
# this course's numerical assumptions or a certified digital twin.
EXACT={'danjiang':'danjiang','hsuehshan':'hsuehshan','three-gorges':'v3-threegorges',
 'b202':'hoover-dam','b204':'v6-itaipu','b301':'v16-thsr','b307':'v16-shinkansen','c407':'v16-robot',
 'd001':'v3-threegorges','d002':'v6-itaipu','d003':'v6-hoover-generator'}

def main():
    photos=json.loads((PUBLIC/'data/photos.json').read_text())
    added=json.loads((HERE/'photos-added.json').read_text())
    by_id={p['id']:p for p in photos}
    for p in added:by_id[p['id']]=p
    photos=list(by_id.values())
    for p in photos:
        f=PUBLIC/p['path'];assert f.is_file(),p['id']
        for key in ('author','license','licenseUrl','sourceUrl','changes'):assert p.get(key), (p['id'],key)
        with Image.open(f) as im:
            p['width'],p['height']=im.size
        p.setdefault('photoType','real-photograph')
        p['sha256']=hashlib.sha256(f.read_bytes()).hexdigest()
    catalog=json.loads((PUBLIC/'data/catalog.json').read_text())
    courses={}
    for c in catalog:
        ident,cat=c['id'],c['category']
        candidates=[p['id'] for p in photos if ident in p.get('courseIds',[])]
        name=c.get('titleEn','').lower()
        keyword_photo=None
        if cat=='energy' and 'wind' in name:keyword_photo='v16-offshore-wind'
        elif cat=='materials' and re.search(r'\b(mine|mining|placer)\b',name):keyword_photo='v16-mine'
        elif cat=='biomedical' and ident=='d201':keyword_photo='v16-emi-ct'
        elif cat=='rail':
            if re.search(r'signal|interlock|train control|operations.control',name):keyword_photo='v16-rail-control'
            elif re.search(r'shinkansen|high.speed|lgv|thsr',name):keyword_photo='v16-shinkansen'
            elif re.search(r'metro|mrt|transit|tram|line',name):keyword_photo='v3-metro'
            elif re.search(r'wheel|bogie|brak|coupl|axle',name):keyword_photo='v3-steam-drivers'
        exact=EXACT.get(ident)
        chosen=exact or keyword_photo or (candidates[0] if candidates else DEFAULTS[cat])
        ids=list(dict.fromkeys([chosen]+candidates+[DEFAULTS[cat]]))[:4]
        for pid in ids:assert pid in by_id,pid
        match='exact' if exact else 'representative'
        note=('實拍對象與本專題具名工程／設備相符；拍攝日期、地點及作者見來源。不是目前即時影像，亦不代表本課模型經現場校準。' if exact else
          '同領域的真實工程／實驗室代表照片。照片標題指出實際拍攝對象；不宣稱是本專題工程或本步驟的現場紀錄。')
        note_en=('The photographed named asset matches this topic. Date, place and author are documented in the source. This is not a live view or proof that the teaching model is site-calibrated.' if exact else
          'Real engineering/laboratory reference photograph from a related field. Its title identifies the actual subject; it is not claimed as a photograph of this project or this process step.')
        courses[ident]={'photoId':chosen,'photoIds':ids,'match':match,'note':note,'noteEn':note_en}
    categories={cat:{'photoId':pid,'match':'representative'} for cat,pid in DEFAULTS.items()}
    manifest={'version':16,'photos':photos,'categories':categories,'courses':courses,
      'scope':{'zh':'真實授權照片搭配獨立原創教學模型；不同專題可重用已標示的代表照片。照片不是每步專屬實拍，也不是經校準的數位孿生。',
       'en':'Licensed real photographs accompany separate original teaching models. Labeled reference photographs may be reused across topics. Images are not step-specific photography or calibrated digital twins.'}}
    (PUBLIC/'data/photos.json').write_text(json.dumps(photos,ensure_ascii=False,indent=2)+'\n')
    (PUBLIC/'data/scene-photos-v16.json').write_text(json.dumps(manifest,ensure_ascii=False,separators=(',',':'))+'\n')
    report={'version':16,'status':'PASS','photos':len(photos),'addedPhotos':len(added),'categoriesCovered':len(categories),'topicsCovered':len(courses),
      'guidedTopicsCovered':sum(c.get('status')=='guided' for c in catalog),'assignments':dict(collections.Counter(c['match'] for c in courses.values())),
      'localFilesVerified':len(photos),'licenseFieldsPresent':len(photos),'newPhotoBytes':sum((PUBLIC/p['path']).stat().st_size for p in added),
      'newSourcesChecked':'Wikimedia Commons imageinfo.extmetadata plus source description; raw provenance JSON retained.',
      'existingSources':'118 V15 licensed photographs retained with original attribution and new local SHA-256 checks.'}
    (HERE/'PHOTO_AUDIT_V16.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    lines=['# V16 photographic assets and attribution','',
      'The individual photographs remain under their stated licenses. Resize/JPEG derivatives have the same photo license. UI models and hotspots are separate original overlays, not edits of the photographs. No endorsement is implied.','',
      '| ID | Actual subject | Author | License | Original source |','| --- | --- | --- | --- | --- |']
    for p in photos:
        clean=lambda s:str(s).replace('|','\\|').replace('\n',' ')
        lines.append('| '+ ' | '.join([clean(p['id']),clean(p['titleEn']),clean(p['author']),f"[{clean(p['license'])}]({p['licenseUrl']})",f"[Source]({p['sourceUrl']})"])+' |')
    (PUBLIC/'assets/photos-v16/ATTRIBUTION.md').write_text('\n'.join(lines)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
