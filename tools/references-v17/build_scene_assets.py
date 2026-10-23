#!/usr/bin/env python3
"""Build the V17 scene manifest from the checked source bundle and local downloads.

Asset processing only resizes the two licensed industrial panoramas; it creates
no synthetic photographic scene content. Source arguments are explicit so this
script can also be used when refreshing the licensed files in a local checkout.
"""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import zipfile
from PIL import Image


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--taichi-zip', type=Path, required=True)
    parser.add_argument('--warehouse-jpeg', type=Path, required=True)
    parser.add_argument('--powerplant-jpeg', type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    academy = root / 'public/academy'
    destination = academy / 'assets/scenes-v17'
    destination.mkdir(parents=True, exist_ok=True)
    previous = json.loads((academy / 'data/scene-photos-v16.json').read_text())
    selected = json.loads((Path(__file__).parent / 'selected-taichi-photos.json').read_text())
    assets = []
    for item in previous['photos']:
        photo = dict(item)
        photo['src'] = photo['path']
        photo['projection'] = 'flat'
        photo['panoramaVerified'] = False
        photo['verification'] = 'Inherited V16 source/author/license record; local file and SHA-256 checked in V17.'
        photo['sceneMatch'] = 'reference-photo; course-specific match retained in scene-photos-v16.json'
        path = academy / photo['path']
        assert path.is_file(), path
        assert digest(path) == photo['sha256'], path
        assets.append(photo)
    imported = []
    water = {'park-002', 'park-005', 'park-020', 'park-024', 'park-034', 'park-039', 'park-041', 'park-053', 'park-060', 'park-063', 'park-067', 'park-070', 'park-075', 'park-128', 'park-144', 'park-167'}
    with zipfile.ZipFile(args.taichi_zip) as archive:
        for source in selected:
            p = source['photo']
            filename = Path(p['path']).name
            member = 'SmartAction_Taichi_Game_v4/assets/places/' + filename
            output = destination / filename
            output.write_bytes(archive.read(member))
            assert digest(output) == p['sha256'], filename
            width, height = Image.open(output).size
            is_panorama = source.get('sceneType') == 'panorama360'
            assert not is_panorama or width == height * 2
            asset_id = 'v17-' + (filename.removesuffix('.jpg') if is_panorama else source['id'])
            path = 'assets/scenes-v17/' + filename
            categories = ['environment'] + (['water'] if source['id'] in water else [])
            if source['id'] == 'park-060': categories += ['marine', 'structures']
            if source['id'] in {'park-034', 'park-063'}: categories += ['energy', 'structures']
            if source['id'] == 'park-076': categories += ['rail']
            photo = {
                'id': asset_id, 'title': source['names']['zh-Hant'],
                'titleEn': source['names']['en'], 'path': path, 'src': path,
                'projection': 'equirectangular' if is_panorama else 'flat',
                'photoType': 'real-panorama' if is_panorama else 'real-photograph',
                'panoramaVerified': is_panorama, 'width': width, 'height': height,
                'sourceUrl': p['source'], 'author': p['author'],
                'license': p['license'], 'licenseUrl': p['licenseUrl'],
                'categories': categories, 'changes': p['modifications'] + ' Bundled thumbnail copied byte-for-byte from the user-provided Taichi v4.1 archive.',
                'sha256': digest(output), 'bytes': output.stat().st_size,
                'capturedDate': p.get('captureDate'), 'verifiedDate': '2026-10-23',
                'verification': 'Author and reuse license checked on the original Wikimedia Commons file page; panorama classification checked against original source description/metadata.',
                'sceneMatch': 'Representative environmental reference; not claimed to be the exact site of another course.',
                'sceneMatchZh': '環境觀察參考照片；不宣稱是其他課程工程的現場。',
                'location': {'name': source['names']['en'], 'latitude': source.get('lat'), 'longitude': source.get('lng')},
            }
            if is_panorama:
                photo.update({'horizontalFov': 360, 'verticalFov': 180,
                              'limitations': 'A real panorama from one fixed capture position. Looking around and optical-style zoom do not reveal hidden object surfaces or measured geometry.',
                              'limitationsZh': '實拍固定位置全景；可轉頭觀察與縮放，不能移動到照片未拍攝的物件背面，也不代表實測幾何。'})
            assets.append(photo)
            imported.append(photo)
    for key, source_path, title, title_en, author, source_slug, categories in [
        ('warehouse', args.warehouse_jpeg, '空倉庫：工業空間觀察', 'Empty Warehouse 01: industrial space reference', 'Sergej Majboroda', 'empty_warehouse_01', ['manufacturing', 'materials', 'structures', 'automotive']),
        ('powerplant', args.powerplant_jpeg, '廢棄電廠：工業遺產觀察', 'Peppermint Powerplant: abandoned industrial reference', 'Andreas Mischok', 'peppermint_powerplant', ['energy', 'process', 'manufacturing', 'environment']),
    ]:
        high_path = destination / ('pano-' + key + '-8k.jpg')
        shutil.copyfile(source_path, high_path)
        image = Image.open(source_path)
        assert image.size == (8192, 4096), image.size
        path = destination / ('pano-' + key + '.jpg')
        image.resize((4096, 2048), Image.Resampling.LANCZOS).save(path, quality=88, optimize=True)
        rel = 'assets/scenes-v17/' + path.name
        asset = {
            'id': 'v17-pano-' + key, 'title': title, 'titleEn': title_en,
            'path': rel, 'src': rel, 'highResolutionPath': 'assets/scenes-v17/' + high_path.name,
            'projection': 'equirectangular', 'photoType': 'real-panorama',
            'panoramaVerified': True, 'horizontalFov': 360, 'verticalFov': 180,
            'width': 4096, 'height': 2048, 'originalWidth': 8192, 'originalHeight': 4096,
            'sourceUrl': 'https://polyhaven.com/a/' + source_slug,
            'downloadUrl': 'https://dl.polyhaven.org/file/ph-assets/HDRIs/extra/Tonemapped%20JPG/' + source_slug + '.jpg',
            'author': author, 'license': 'CC0 1.0',
            'licenseUrl': 'https://creativecommons.org/publicdomain/zero/1.0/',
            'providerLicenseUrl': 'https://polyhaven.com/license',
            'categories': categories, 'changes': 'Official tonemapped HDRI JPEG. 8K source retained byte-for-byte. Default 4K image resized and JPEG recompressed. No generated scene details.',
            'sha256': digest(path), 'bytes': path.stat().st_size,
            'sourceSha256': digest(high_path), 'sourceBytes': high_path.stat().st_size,
            'verifiedDate': '2026-10-23',
            'verification': 'Source author, HDRI identity and CC0 confirmed on Poly Haven asset page. Official Tonemapped JPG downloaded through its visible download control.',
            'sceneMatch': 'Representative industrial reference; not an active teaching laboratory or exact site twin.',
            'sceneMatchZh': '工業空間參考；不是運作中的教學實驗室，也不是指定工程的精確數位孿生。',
            'limitations': 'One fixed capture position. Surface depth, equipment state, dimensions and hidden surfaces are not measured by this photograph.',
            'limitationsZh': '固定拍攝點全景；影像不提供實測深度、設備現況、尺寸或被遮擋的表面。',
        }
        assets.append(asset)
        imported.append(asset)
    defaults = {key: value['photoId'] for key, value in previous['categories'].items()}
    photo_sets = {key: [value] for key, value in defaults.items()}
    panoramas = {key: [] for key in defaults}
    for asset in imported:
        for key in asset['categories']:
            if key in photo_sets:
                if asset['projection'] == 'equirectangular':
                    panoramas[key].append(asset['id'])
                else:
                    photo_sets[key].append(asset['id'])
    panorama_ids = [a['id'] for a in imported if a['projection'] == 'equirectangular']
    manifest = {
        'version': 17, 'verifiedDate': '2026-10-23', 'assets': assets,
        'categoryDefaults': defaults, 'categoryPhotoSets': photo_sets,
        'panoramaSets': panoramas, 'allPanoramaIds': panorama_ids,
        'scope': {
            'inheritedPhotographs': 129, 'newPhotographs': 20, 'newPanoramas': 7,
            'newPanoramaCaptureTypes': {'urbanParks': 5, 'industrialInteriors': 2},
            'allAssetsAvailableOffline': True,
            'notEverySpecialtyHasAnExactSitePanorama': True,
            'noMeasuredGeometryClaim': True,
            'labelZh': '149張實拍照片與7張固定拍攝點360環景；各專科模型是教學示意。',
            'labelEn': '149 real photographs and 7 fixed-position 360 panoramas; specialty geometry is a teaching model.',
        },
    }
    assert len(assets) == 156 and len(imported) == 27 and len(panorama_ids) == 7
    assert len(defaults) == 20
    assert len({a['id'] for a in assets}) == len(assets)
    (academy / 'data/scene-assets-v17.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    attribution = ['MacGyver Engineering Academy V17 — photographic asset attribution',
                   'Each image retains the license below. The repository code license does not replace image licenses.',
                   'CC BY-SA images and any adapted versions remain under their stated compatible share-alike license.',
                   'No author or institution endorsement is implied. Photographs do not establish current operating conditions.', '']
    for photo in assets:
        attribution.extend([photo['id'] + ' — ' + photo['titleEn'],
                            'File: ' + photo['path'], 'Author: ' + photo['author'],
                            'License: ' + photo['license'] + ' — ' + photo['licenseUrl'],
                            'Source: ' + photo['sourceUrl'], 'Changes: ' + photo['changes'], ''])
    (destination / 'ATTRIBUTION.txt').write_text('\n'.join(attribution))
    audit = {'assetCount': len(assets), 'newAssetCount': len(imported),
             'allFilesPresent': True, 'originalBundleHashesVerified': True,
             'newAssets': [{key: a.get(key) for key in ['id', 'path', 'projection', 'width', 'height', 'sha256', 'license', 'sourceUrl']} for a in imported],
             'limitations': manifest['scope']}
    (Path(__file__).parent / 'ASSET_AUDIT_V17.json').write_text(json.dumps(audit, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'assets': len(assets), 'newAssets': len(imported), 'newPanoramas': len(panorama_ids), 'categories': len(defaults)}))


if __name__ == '__main__':
    main()
