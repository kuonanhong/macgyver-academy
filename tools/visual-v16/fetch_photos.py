#!/usr/bin/env python3
"""Fetch an explicitly reviewed Commons selection; record licenses and file hashes."""
from pathlib import Path
import concurrent.futures, hashlib, html, io, json, re, urllib.parse, urllib.request
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
PUBLIC = ROOT / 'public/academy'
HEADERS = {'User-Agent': 'MacGyverAcademy/16 educational asset attribution audit'}

def request(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=HEADERS), timeout=60) as response:
        return response.read()

def plain(value):
    return html.unescape(re.sub('<[^>]+>', '', value)).strip()

def fetch(item):
    proof = HERE / 'provenance' / (item['id'] + '.json')
    proof.parent.mkdir(parents=True, exist_ok=True)
    data = None
    refresh_image = False
    if proof.exists():
        data = json.loads(proof.read_text())
        cached_page = next(iter(data.get('query',{}).get('pages',{}).values()), {})
        normalized = lambda value: value.replace('_', ' ').casefold()
        if normalized(cached_page.get('title','')) != normalized('File:' + item['file']):
            # IDs are stable while an editor may replace the selected source.
            # Never reuse proof or image bytes belonging to the old filename.
            data = None
            refresh_image = True
    if data is None:
        query = urllib.parse.urlencode({'action':'query','format':'json','titles':'File:'+item['file'],
            'prop':'imageinfo','iiprop':'url|extmetadata|sha1|size','iiurlwidth':1280})
        data = json.loads(request('https://commons.wikimedia.org/w/api.php?' + query))
        proof.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    page = next(iter(data['query']['pages'].values()))
    info = page['imageinfo'][0]; meta = info['extmetadata']
    license_name = plain(meta.get('LicenseShortName',{}).get('value',''))
    license_url = plain(meta.get('LicenseUrl',{}).get('value',''))
    if not (license_name.startswith('CC BY') or license_name in ('CC0','Public domain')):
        raise ValueError('License needs manual review: ' + item['id'] + ': ' + license_name)
    if license_url.startswith('//'): license_url = 'https:' + license_url
    author = plain(meta.get('Artist',{}).get('value',''))
    if not author or not license_url: raise ValueError('Attribution incomplete: '+item['id'])
    target = PUBLIC/'assets/photos-v16'/(item['id']+'.jpg')
    target.parent.mkdir(parents=True, exist_ok=True)
    prior_path = HERE/'photos-added.json'
    if prior_path.exists():
        prior = next((p for p in json.loads(prior_path.read_text()) if p['id']==item['id']), None)
        refresh_image = refresh_image or bool(prior and prior.get('sourceUrl') != info['descriptionurl'])
    if refresh_image or not target.exists():
        raw = request(info.get('thumburl',info['url']))
        im = ImageOps.exif_transpose(Image.open(io.BytesIO(raw))).convert('RGB')
        im.thumbnail((1280,960),Image.Resampling.LANCZOS)
        im.save(target,'JPEG',quality=86,optimize=True,progressive=True)
    with Image.open(target) as im: dimensions=list(im.size)
    return {**{k:v for k,v in item.items() if k!='file'},'path':target.relative_to(PUBLIC).as_posix(),
        'author':author,'license':license_name,'licenseUrl':license_url,'sourceUrl':info['descriptionurl'],
        'originalFileUrl':info['url'],'originalSha1':info['sha1'],
        'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'width':dimensions[0],'height':dimensions[1],
        'changes':'Resized and JPEG recompressed; no scene edits. Display may crop. Photo derivative remains under its stated license.',
        'retrieved':'2026-10-23','photoType':'real-photograph','provenance':proof.relative_to(ROOT).as_posix()}

def main():
    selection=json.loads((HERE/'photo-selection.json').read_text())
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        results=list(executor.map(fetch,selection))
    (HERE/'photos-added.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'downloaded':len(results),'bytes':sum((PUBLIC/x['path']).stat().st_size for x in results)},indent=2))

if __name__=='__main__': main()
