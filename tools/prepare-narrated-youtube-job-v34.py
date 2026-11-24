#!/usr/bin/env python3
"""Prepare a new local narrated-film publication job; never access OAuth/network.

V33 metadata and its bound upload state are untouched. Run after media mux and
speech-caption validation. YouTube alternate audio still needs Studio; a
multi-audio MP4 is not a promise that YouTube imports every audio track.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
DELIVERY = ROOT.parent / 'delivery/narrated-v33'
CONTENT = ROOT / 'public/academy/packaging-tour-content-v33.js'
ACADEMY = 'https://kuonanhong.github.io/macgyver-academy/'
AERO = 'https://kuonanhong.github.io/AERO_Explorer/'
LINE = 'https://line.me/R/ti/p/%40530pgchc'
LANGUAGES = ('zh-TW', 'en', 'ja', 'ko', 'zh-CN')
LABELS = {'zh-TW': '繁體中文 + English', 'en': 'English', 'ja': '日本語 + English',
          'ko': '한국어 + English', 'zh-CN': '简体中文 + English'}
COPY = {
 'zh-TW': {'suffix':'5分鐘俯瞰導覽', 'chapters':'章節', 'references':'官方技術參考',
           'notice':'本片為三維工程教學重建，不是廠房實拍、原廠 CAD 或量測模擬；圖中比例、顏色與動態用於解說，不代表製程尺寸、實測溫度、速度、良率或壽命。',
           'audio':'交付 MP4 含繁中、英文、日文、韓文與簡中五語合成旁白；預設繁中。字幕以本語實際語音時間配對英文，英文軌為單語。YouTube 可選語音與字幕以播放器已發布的選單為準。',
           'independent':'本片為獨立教學創作，不代表所列企業或標準組織背書。'},
 'en': {'suffix':'5-minute aerial tour', 'chapters':'Chapters', 'references':'Official technical references',
        'notice':'An educational 3D reconstruction, not factory footage, vendor CAD or a measurement-based simulation. Visual scale, color and motion explain concepts; they do not establish manufacturing dimensions, measured temperatures, speeds, yields or lifetime.',
        'audio':'The delivery MP4 contains synthetic narration in Traditional Chinese, English, Japanese, Korean and Simplified Chinese; Traditional Chinese is the default. Native-language captions follow measured speech with a corresponding English line; the English track is English-only. Available YouTube audio and caption languages depend on the tracks published in its player.',
        'independent':'This independent educational work is not endorsed by the listed companies or standards organizations.'},
 'ja': {'suffix':'5分間の俯瞰ツアー', 'chapters':'チャプター', 'references':'公式技術資料',
        'notice':'工学教育用の3D再現映像です。工場の実写、メーカーのCAD、測定に基づくシミュレーションではありません。縮尺・色・動きは説明用で、製造寸法、実測温度、速度、歩留まり、寿命を示すものではありません。',
        'audio':'配布MP4は繁体字中国語・英語・日本語・韓国語・簡体字中国語の合成音声を収録し、標準音声は繁体字中国語です。各言語の実際の発話時刻に対応する英訳を字幕の次行に表示します。英語字幕は英語のみです。YouTubeで選択できる音声・字幕は公開済みのトラックをご確認ください。',
        'independent':'独立した教育作品であり、記載された企業や標準化団体の承認・推奨を意味しません。'},
 'ko': {'suffix':'5분 항공 시점 투어', 'chapters':'챕터', 'references':'공식 기술 자료',
        'notice':'공학 교육용 3D 재구성 영상입니다. 공장 실사, 제조사 CAD 또는 측정 기반 시뮬레이션이 아닙니다. 크기·색·움직임은 개념 설명용이며 실제 제조 치수, 온도, 속도, 수율 또는 수명을 나타내지 않습니다.',
        'audio':'배포 MP4에는 번체 중국어·영어·일본어·한국어·간체 중국어 합성 음성이 있으며 기본 음성은 번체 중국어입니다. 각 언어의 실제 발화 시간에 맞춘 자막 아래에 해당 의미의 영어를 표시합니다. 영어 자막은 영어만 표시합니다. YouTube에서 선택할 수 있는 음성과 자막은 게시된 트랙 메뉴를 확인하세요.',
        'independent':'독립 교육 작품이며 기재된 기업이나 표준화 단체의 보증 또는 추천을 의미하지 않습니다.'},
 'zh-CN': {'suffix':'5分钟俯瞰导览', 'chapters':'章节', 'references':'官方技术参考',
           'notice':'本片为三维工程教学重建，不是工厂实拍、原厂 CAD 或测量模拟；图中比例、颜色与动态用于解说，不代表工艺尺寸、实测温度、速度、良率或寿命。',
           'audio':'交付 MP4 含繁体中文、英文、日文、韩文与简体中文五语合成旁白；默认繁体中文。字幕以本语实际语音时间配对英文，英文轨为单语。YouTube 可选语音与字幕以播放器已发布的菜单为准。',
           'independent':'本片为独立教学创作，不代表所列企业或标准组织背书。'}
}
OUTCOMES = {
 'interposer': ('分清運算晶粒、HBM、中介層與基板；沿資料、供電與熱路徑找出設計取捨，並區分 CoWoS 的不同變體。',
                'Distinguish compute dies, HBM, interposer and substrate; follow data, power and heat, evaluate integration tradeoffs, and distinguish CoWoS variants.'),
 'fanout': ('追蹤接點如何經 RDL 扇出；辨認介電層、導孔、訊號回路及對位偏移，理解製程順序、翹曲與良率之間的關係。',
             'Trace connections through RDL, dielectrics and vias; examine return paths and placement error, and connect process ordering, warpage and yield.'),
 'hybrid': ('辨認銅接點與介電表面的共同鍵合；連結表面準備、對位、可測試性和熱路徑，理解堆疊架構的限制。',
             'Identify copper and dielectric bonding; connect surface preparation, alignment, testability and heat flow to the constraints of a stacked architecture.'),
 'bridge': ('定位局部矽橋與晶粒邊緣介面；區分實體橋接和通訊協定，評估組裝公差、材料應力與測試證據。',
             'Locate silicon bridges and die-edge interfaces; separate physical integration from communication protocols, and evaluate assembly tolerances, material stress and test evidence.'),
 'chiplet': ('從系統功能分工走到封裝與互連；區分實體訊號、協定與互通性，將 UCIe、供電散熱和整合驗證放在同一條技術路線上。',
              'Move from functional partitioning to packaging and interconnect; distinguish signaling, protocols and interoperability, and integrate UCIe, power, cooling and validation.'),
 'thermal': ('由發熱源追到散熱器，分清熱、機械、電性與壽命測試；用邊界條件、量測和不確定性判讀改善效果。',
              'Follow heat from source to cooler; distinguish thermal, mechanical, electrical and lifetime tests, and assess improvements using boundary conditions, measurements and uncertainty.')
}


def sha(file):
    h = hashlib.sha256()
    with Path(file).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def validate_text(title, description):
    if not isinstance(title, str) or not 1 <= len(title) <= 100:
        raise ValueError('YouTube title must contain 1–100 Unicode characters')
    if not isinstance(description, str) or len(description.encode('utf-8')) > 5000:
        raise ValueError('YouTube description exceeds 5000 UTF-8 bytes')
    if any(character in title + description for character in '<>'):
        raise ValueError('YouTube metadata must not contain angle brackets')
    return {'titleCharacters': len(title), 'titleUtf8Bytes': len(title.encode('utf-8')),
            'descriptionCharacters': len(description), 'descriptionUtf8Bytes': len(description.encode('utf-8')), 'status': 'PASS'}


def timecode(seconds):
    return f'{int(seconds) // 60:02}:{int(seconds) % 60:02}'


def link_block(tour, language):
    return (f'Interactive tour / 互動導覽\n{ACADEMY}packaging-tour-v33.html?tour={tour}&lang={language}\n'
            f'MacGyver Engineering Academy\n{ACADEMY}\nAERO Explorer\n{AERO}\n'
            f'郭南宏 官方 LINE / Official LINE\n{LINE}')


def localized(tour, language, index):
    copy = COPY[language]
    title = f'{index:02}｜{tour["title"][language]}｜{copy["suffix"]}'
    chapters = '\n'.join(f'{timecode(c["start"])} {c["title"][language]}' for c in tour['chapters'])
    references = '\n'.join(f'{s["title"]}\n{s["url"]}' for s in tour['sources'])
    description = '\n\n'.join([tour['summary'][language], copy['notice'], copy['audio'],
                                link_block(tour['id'], language), copy['chapters'] + '\n' + chapters,
                                copy['references'] + '\n' + references, copy['independent']])
    return {'title': title, 'description': description}


def bilingual(tour, index):
    title = f'{index:02}｜{tour["title"]["zh-TW"]}｜{tour["title"]["en"]}｜5分鐘 / 5 min'
    chapters = '\n'.join(f'{timecode(c["start"])} {c["title"]["zh-TW"]} / {c["title"]["en"]}' for c in tour['chapters'])
    references = '\n'.join(f'{s["title"]}\n{s["url"]}' for s in tour['sources'])
    outcomes = '\n'.join(OUTCOMES[tour['id']])
    description = '\n\n'.join([
        tour['summary']['zh-TW'] + '\n' + tour['summary']['en'], '學習重點 / Learning objectives\n' + outcomes,
        COPY['zh-TW']['notice'] + '\n' + COPY['en']['notice'],
        COPY['zh-TW']['audio'] + '\n' + COPY['en']['audio'],
        link_block(tour['id'], 'zh-TW'), '章節 / Chapters\n' + chapters,
        '官方技術參考 / Official technical references\n' + references,
        COPY['zh-TW']['independent'] + '\n' + COPY['en']['independent'], '#先進封裝 #半導體 #AdvancedPackaging'])
    return {'title': title, 'description': description}


def read_content():
    script = 'const fs=require("fs"),vm=require("vm"),c={window:{}};vm.runInNewContext(fs.readFileSync(process.argv[1],"utf8"),c);process.stdout.write(JSON.stringify(c.window.MACGYVER_PACKAGING_TOURS));'
    return json.loads(subprocess.run(['node', '-e', script, str(CONTENT)], check=True, capture_output=True, text=True).stdout)


def prepare(media_dir, audio_manifest_path, output, tour_id=None):
    manifest_path = media_dir / (f'manifest.{tour_id}.partial.json' if tour_id else 'manifest.json')
    manifest = json.loads(manifest_path.read_text('utf-8'))
    speech = json.loads(audio_manifest_path.read_text('utf-8'))
    accepted_status = ('PASS', 'PARTIAL') if tour_id else ('PASS',)
    if manifest.get('status') not in accepted_status or manifest.get('silent') is not False or speech.get('status') not in accepted_status:
        raise ValueError('Validated narrated media and speech manifest required')
    assets = {v['id']: v for v in manifest['videos']}
    audio = {(a['tourId'], a['language']): a for a in speech['tracks']}
    content = read_content()
    original_metadata = ROOT / 'docs/PACKAGING_YOUTUBE_METADATA_V33.json'
    old_sha = sha(original_metadata)
    original = json.loads(original_metadata.read_text('utf-8'))
    result = {'schemaVersion': 2, 'jobVersion': '34.0.0', 'preparedAt': '2026-11-24',
              'status': 'prepared-not-uploaded', 'jobCompleteness': 'single-video-review' if tour_id else 'complete-six-video-job',
              'sourceSha256': sha(CONTENT),
              'mediaManifest': str(manifest_path.resolve()), 'mediaManifestSha256': sha(manifest_path),
              'defaultAudioLanguage': 'zh-TW', 'mediaVersion': manifest['version'],
              'playlist': {'title': original['playlist']['title'], 'requireExisting': False,
                           'creationPolicy': 'reuse-exact-title-or-create-if-absent',
                           'description': '六部各5分鐘的先進封裝俯瞰導覽，含合成旁白與字幕。\nSix five-minute educational fly-throughs of advanced semiconductor packaging with synthetic narration and captions.\n\n'
                                          + f'Academy: {ACADEMY}\nAERO Explorer: {AERO}\nOfficial LINE: {LINE}'},
              'publicationNotes': {'existingPlaylist': 'Resolve the exact title on the verified channel: reuse one match, create only after an exhaustive zero-match result, reject ambiguity, and reconcile uncertain creation before retrying. No remote operation was performed by this preparation.',
                                   'networkOrOAuthUsed': False, 'originalV33MetadataModified': False,
                                   'alternateAudio': 'MP4 contains five audio tracks. Upload four alternate-language audio-only M4A files through YouTube Studio when the account has the feature; do not assume container tracks become selectable YouTube dubs.',
                                   'subtitleUpload': 'Upload speech-aligned external bilingual VTT or SRT per language. English is English-only. Embedded mov_text tracks support the downloadable MP4.',
                                   'metadataLanguageLimits': 'title <=100 Unicode characters; description <=5000 UTF-8 bytes. Same conservative validation is applied to each localization.',
                                   'primaryAudioLanguage': 'Set original video language to Traditional Chinese in Studio. This job does not use auto-dubbing.'},
              'videos': [], 'validation': []}
    for index, tour in enumerate(content['tours'], 1):
        key = tour['id']
        if tour_id and key != tour_id:
            continue
        file = media_dir / f'{key}.mp4'
        asset = assets[key]
        if file.stat().st_size != asset['bytes'] or sha(file) != asset['sha256']:
            raise ValueError('Final media differs from its verified manifest')
        text = bilingual(tour, index)
        localizations = {language: localized(tour, language, index) for language in LANGUAGES}
        validation = {'id': key, 'default': validate_text(**text),
                      'localizations': {language: validate_text(**value) for language, value in localizations.items()}}
        captions, audio_tracks = [], []
        for language in LANGUAGES:
            vtt = media_dir / 'subtitles-bilingual' / f'{key}.{language}.vtt'
            srt = vtt.with_suffix('.srt')
            captions.append({'language': language, 'label': LABELS[language], 'file': str(vtt.resolve()),
                             'format': 'webvtt', 'sha256': sha(vtt), 'srtFile': str(srt.resolve()), 'srtSha256': sha(srt)})
            track = audio[(key, language)]
            audio_file = Path(track['file'])
            if not audio_file.is_absolute():
                audio_file = audio_manifest_path.parent / audio_file
            if sha(audio_file) != track['sha256']:
                raise ValueError('Narration differs from its final manifest')
            audio_tracks.append({'language': language, 'file': str(audio_file.resolve()), 'sha256': track['sha256'],
                                 'bytes': track['bytes'], 'default': language == 'zh-TW', 'studioUploadRequired': language != 'zh-TW'})
        result['videos'].append({'id': key, 'playlistPosition': index - 1, **text, 'localizations': localizations,
                                 'defaultLanguage': 'zh-TW', 'defaultAudioLanguage': 'zh-TW', 'durationSeconds': 300,
                                 'videoFile': str(file.resolve()), 'videoBytes': asset['bytes'], 'videoSha256': asset['sha256'],
                                 'audio': 'five-language-synthetic-narration', 'audioTracks': audio_tracks,
                                 'subtitleTracks': captions, 'chapters': [{'timecode': timecode(c['start']), 'startSeconds': c['start'],
                                                                         'endSeconds': c['end'], 'title': c['title']} for c in tour['chapters']],
                                 'sources': tour['sources'], 'links': {'academy': ACADEMY, 'aero': AERO, 'line': LINE}})
        result['validation'].append(validation)
    encoded = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if 'resilience' in encoded.lower():
        raise ValueError('Unexpected unrelated project link')
    if sha(original_metadata) != old_sha:
        raise ValueError('Original metadata changed during preparation')
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(encoded, 'utf-8')
    return result


def export_source_job(input_job, destination):
    """Export a portable job only after root installs the verified source assets."""
    result = copy.deepcopy(json.loads(input_job.read_text('utf-8')))
    if result.get('jobCompleteness') != 'complete-six-video-job':
        raise ValueError('A complete verified six-film job is required')
    base = destination.resolve().parent
    def relative(file):
        return Path(os.path.relpath(file.resolve(), base)).as_posix()
    media = ROOT / 'public/academy/assets/packaging-tour-v33'
    manifest = media / 'videos/manifest.json'
    if sha(manifest) != result['mediaManifestSha256']:
        raise ValueError('Install the verified narrated manifest into source before exporting the portable job')
    result['mediaManifest'] = relative(manifest)
    result['pathResolutionMode'] = 'metadata-relative'
    result['pathResolution'] = 'All file paths resolve relative to this metadata JSON file, not the current working directory.'
    result['sourceFile'] = relative(CONTENT)
    result['playlist']['requireExisting'] = False
    result['playlist']['creationPolicy'] = 'reuse-exact-title-or-create-if-absent'
    for video in result['videos']:
        key = video['id']
        file = media / 'videos' / f'{key}.mp4'
        if file.stat().st_size != video['videoBytes'] or sha(file) != video['videoSha256']:
            raise ValueError('Install the verified narrated source movie before exporting: ' + key)
        video['videoFile'] = relative(file)
        for track in video['audioTracks']:
            file = media / 'audio' / f'{key}.{track["language"]}.m4a'
            if sha(file) != track['sha256']:
                raise ValueError('Installed narration differs from its reviewed hash')
            track['file'] = relative(file)
        for track in video['subtitleTracks']:
            file = media / 'subtitles-bilingual' / f'{key}.{track["language"]}.vtt'
            srt = file.with_suffix('.srt')
            if sha(file) != track['sha256'] or sha(srt) != track['srtSha256']:
                raise ValueError('Install both the final semantic VTT and SRT into source before exporting')
            track['file'], track['srtFile'] = relative(file), relative(srt)
    result['publicationNotes']['portableAssetsVerified'] = True
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', 'utf-8')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--media', type=Path, default=DELIVERY)
    parser.add_argument('--audio-manifest', type=Path, default=ROOT.parent / 'delivery/narration-v34/AUDIO_MANIFEST_V34.json')
    parser.add_argument('--output', type=Path)
    parser.add_argument('--tour', choices=tuple(OUTCOMES), help='Prepare one completed film for Studio review while the other films are rendering.')
    parser.add_argument('--check-text-only', action='store_true')
    parser.add_argument('--export-source-job', type=Path, help='After source installation, export metadata-relative paths into this JSON file.')
    parser.add_argument('--input-job', type=Path, default=DELIVERY / 'youtube-job-v34/metadata.json')
    args = parser.parse_args()
    if args.export_source_job:
        result = export_source_job(args.input_job, args.export_source_job)
        print(json.dumps({'status': 'PASS', 'videos': len(result['videos']), 'portableJob': str(args.export_source_job.resolve())}, ensure_ascii=False))
    elif args.check_text_only:
        rows = []
        for index, tour in enumerate(read_content()['tours'], 1):
            rows.append({'id': tour['id'], 'default': validate_text(**bilingual(tour, index)),
                         'localizations': {l: validate_text(**localized(tour, l, index)) for l in LANGUAGES}})
        print(json.dumps({'status': 'PASS', 'validation': rows}, ensure_ascii=False))
    else:
        output = args.output or (args.media / 'youtube-job-v34' / (f'{args.tour}.metadata.json' if args.tour else 'metadata.json'))
        result = prepare(args.media, args.audio_manifest, output, args.tour)
        print(json.dumps({'status': 'PASS', 'videos': len(result['videos']), 'localizations': 5 * len(result['videos']), 'output': str(output.resolve())}, ensure_ascii=False))


if __name__ == '__main__':
    main()
