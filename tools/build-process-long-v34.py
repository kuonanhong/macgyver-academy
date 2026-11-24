#!/usr/bin/env python3
"""Build an independent 15-minute process lesson locally; never publish/upload.

Inputs are reviewed scripts, measured narration, semantic mappings and a verified
master. Outputs stay under delivery/process-long-v34/<film-id>. Existing short
films, public assets, OAuth and network services are never accessed or changed.
"""
from __future__ import annotations
import argparse
from fractions import Fraction
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
DELIVERY = ROOT.parent / 'delivery/process-long-v34'
LANGUAGES = ('zh-TW', 'en', 'ja', 'ko', 'zh-CN')


def module(name, filename):
    spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(filename))
    result = importlib.util.module_from_spec(spec)
    sys.modules[name] = result
    spec.loader.exec_module(result)
    return result


BASE = module('long_subtitle_base', 'export-bilingual-packaging-subtitles-v33.py')
MUX = module('long_mux_helpers', 'mux-narrated-packaging-v34.py')
JOB = module('long_metadata_helpers', 'prepare-narrated-youtube-job-v34.py')
SHORT = module('long_chapter_helpers', 'build-c01-narrated-job-v34.py')


def read(path):
    return json.loads(Path(path).read_text('utf-8'))


def atomic(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    data = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, indent=2) + '\n'
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(data, 'utf-8')
    temporary.replace(path)


def text_sha(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def resolve(base, value):
    path = Path(value)
    return path.resolve() if path.is_absolute() else (Path(base) / path).resolve()


def checked_file(base, record):
    file = resolve(base, record['file'])
    if not file.is_file() or file.stat().st_size != record['bytes'] or MUX.sha(file) != record['sha256']:
        raise ValueError('Input file differs from its verified manifest: ' + file.name)
    return file


def contract(script, require_languages=True):
    film = script['id']
    if not re.fullmatch(r'[A-Z][0-9]{2,3}-long', film):
        raise ValueError('A separate process-long id is required')
    if script['durationSeconds'] != 900 or len(script['cues']) != 30:
        raise ValueError('A 900-second lesson with thirty authored chapters is required')
    languages = LANGUAGES if require_languages else script['languages']
    for index, chapter in enumerate(script['cues']):
        if (chapter['start'], chapter['end']) != (index * 30, (index + 1) * 30):
            raise ValueError('Chapter boundaries must cover 0–900 without gaps')
        for language in languages:
            if not chapter['text'].get(language, '').strip() or not chapter['title'].get(language, '').strip():
                raise ValueError('A chapter lacks complete language content')
    return film


def display_track(cues, sentences, chapters, language):
    """Bind authored meaning to native speech, not another track's time or index."""
    mapping = {(r['chapter'] - 1, r['sentence'] - 1): r for r in sentences}
    if len(mapping) != len(sentences) or len(cues) != len(sentences):
        raise ValueError('Semantic mapping count or sentence identifiers differ')
    actual_keys = [(c['chapterIndex'], c['sentenceIndex']) for c in cues]
    if actual_keys != sorted(set(actual_keys)) or set(actual_keys) != set(mapping):
        raise ValueError('Measured cues must have ordered, unique mapped identifiers')
    result = []
    for chapter_index, chapter in enumerate(chapters):
        selected = [c for c in cues if c['chapterIndex'] == chapter_index]
        if not selected or [c['sentenceIndex'] for c in selected] != list(range(len(selected))):
            raise ValueError('Every chapter needs complete measured sentence indices')
        previous_end = chapter['start']
        for index, cue in enumerate(selected):
            row = mapping[(chapter_index, index)]
            start, end = float(cue['start']), float(cue['end'])
            if (not math.isfinite(start) or not math.isfinite(end) or
                    not previous_end <= start < end <= chapter['end']):
                raise ValueError('Speech intervals overlap or leave their authored chapter')
            if (row['sourceText'] != cue['text'] or row['sourceTextSha256'] != text_sha(cue['text'])
                    or not row.get('englishText', '').strip()):
                raise ValueError('A semantic mapping no longer matches the spoken sentence')
            if row.get('speechStart') != cue['start'] or row.get('speechEnd') != cue['end']:
                raise ValueError('A mapping lacks the exact final measured speech binding')
            if language == 'en' and row['englishText'] != cue['text']:
                raise ValueError('English captions must preserve the spoken English sentence')
            display_start = chapter['start'] if index == 0 else start
            display_end = selected[index + 1]['start'] if index + 1 < len(selected) else chapter['end']
            result.append({'start': round(display_start, 3), 'end': round(display_end, 3),
                           'text': cue['text'], 'english': '' if language == 'en' else row['englishText'],
                           'speechStart': start, 'speechEnd': end,
                           'chapter': chapter_index + 1, 'sentence': index + 1})
            previous_end = end
        # Ensure actual sentence text, not merely count, reconstructs the chapter.
        squash = lambda value: re.sub(r'\s+', '', value)
        if squash(''.join(c['text'] for c in selected)) != squash(chapter['text'][language]):
            raise ValueError('Measured narration does not reconstruct the authored chapter')
    subtitle_cues = [BASE.Cue(round(c['start'] * 1000), round(c['end'] * 1000),
                              c['text'] + ('\n' + c['english'] if c['english'] else '')) for c in result]
    BASE.validate_coverage(subtitle_cues, round(chapters[-1]['end'] * 1000))
    return result, subtitle_cues


SUMMARY = {
 'zh-TW': '以假想加速器練習需求追溯、有效頻寬、熱與供電預算、測試證據及架構取捨。所有數值為教學假設；不代表產品規格、實測結果或合規認證。',
 'en': 'Work through requirements traceability, useful bandwidth, thermal and power budgets, test evidence, and architecture choices for a hypothetical accelerator. All numbers are teaching assumptions, not product specifications, measurements or compliance claims.',
 'ja': '仮想アクセラレーターを題材に、要件の追跡、実効帯域、熱・電力予算、試験証拠、構成の選択を学びます。数値は教育用の仮定であり、製品仕様、実測値、適合認証ではありません。',
 'ko': '가상의 가속기로 요구사항 추적, 유효 대역폭, 열·전력 예산, 시험 증거와 구조 선택을 연습합니다. 모든 수치는 교육용 가정이며 제품 사양, 실측 결과 또는 적합성 인증이 아닙니다.',
 'zh-CN': '以假想加速器练习需求追溯、有效带宽、热与供电预算、测试证据及架构取舍。所有数值为教学假设；不代表产品规格、实测结果或合规认证。'
}
NOTICE = {
 'zh-TW': '原創3D教學重建與五語合成旁白，非工廠實拍或經驗證模擬。字幕跟隨本語實際語音，下行為對應英文；英語軌僅英文。YouTube可選音軌以實際發布選單為準。',
 'en': 'Original educational 3D reconstruction with five synthetic narration tracks, not factory footage or a validated simulation. Native captions follow measured speech with corresponding English; English is single-language. YouTube audio choices depend on published tracks.',
 'ja': '独自の教育用3D再現と5言語の合成音声です。工場の実写や検証済みシミュレーションではありません。実測した発話時刻に各言語字幕と対応する英訳を表示します。英語は単言語です。YouTube音声の選択肢は公開済みトラックによります。',
 'ko': '독창적인 교육용 3D 재구성과 5개 언어 합성 음성입니다. 공장 실사나 검증된 시뮬레이션이 아닙니다. 실측 발화 시간에 본국어 자막과 해당 영어를 표시하며 영어는 단일 언어입니다. YouTube 음성 선택은 게시된 트랙에 따릅니다.',
 'zh-CN': '原创3D教学重建与五语合成旁白，非工厂实拍或经验证模拟。字幕跟随本语实际语音，下行为对应英文；英语轨仅英文。YouTube可选音轨以实际发布菜单为准。'
}
def metadata_text(script, languages=LANGUAGES):
    film = contract(script, require_languages=set(languages) == set(LANGUAGES))
    process = film.removesuffix('-long')
    summary = script.get('metadataSummary', SUMMARY if film == 'C01-long' else None)
    bilingual_title = script.get('youtubeBilingualTitle')
    if bilingual_title is None and film == 'C01-long':
        bilingual_title = f'{process}｜封裝需求與工程決策｜Packaging requirements & decisions｜15分鐘 / 15 min'
    if not summary or not bilingual_title:
        raise ValueError('Other long lessons require their own reviewed metadataSummary and youtubeBilingualTitle')
    references = '\n'.join(f'{source["title"]}\n{source["url"]}' for source in script['sources'])
    links = f'MacGyver Engineering Academy\n{JOB.ACADEMY}\nAERO Explorer\n{JOB.AERO}\n郭南宏 官方 LINE / Official LINE\n{JOB.LINE}'
    versions = {}
    for language in ('default', *languages):
        bilingual = language == 'default'
        lang = 'zh-TW' if bilingual else language
        titles = []
        for chapter in script['cues']:
            short = chapter.get('shortTitle', chapter['title'])
            label = short[lang] + (' / ' + short['en'] if bilingual else '')
            titles.append(f'{JOB.timecode(chapter["start"])} {label}')
        title = (bilingual_title
                 if bilingual else script.get('youtubeTitle', script['title'])[lang])
        description = '\n\n'.join([
            summary[lang] + ('\n' + summary['en'] if bilingual else ''),
            NOTICE[lang] + ('\n' + NOTICE['en'] if bilingual else ''), links,
            '章節 / Chapters\n' + '\n'.join(titles),
            '官方技術參考 / Official technical references\n' + references,
            'Independent educational work; no supplier endorsement.'])
        JOB.validate_text(title, description)
        versions[language] = {'title': title, 'description': description}
    return versions


def qr_verify(file, duration, rectangle=None):
    try:
        import cv2
        import numpy as np
    except ImportError:
        return {'status': 'INHERITED_BY_PACKET_IDENTITY', 'reason': 'Verified master QR retained byte-for-byte; OpenCV unavailable for an additional decode.'}
    checks = []
    for second in (duration - 10, duration - 5, duration - 1 / 24):
        raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{second:.9f}', '-i', str(file), '-map', '0:v:0',
                              '-frames:v', '1', '-f', 'image2pipe', '-vcodec', 'png', '-'], check=True, capture_output=True).stdout
        frame = cv2.imdecode(np.frombuffer(raw, dtype=np.uint8), cv2.IMREAD_COLOR)
        if frame is None:
            raise ValueError('QR frame could not be decoded')
        if rectangle:
            x, y, width, height = [int(rectangle[k]) for k in ('x', 'y', 'width', 'height')]
            if min(x, y) < 0 or min(width, height) <= 0 or x + width > frame.shape[1] or y + height > frame.shape[0]:
                raise ValueError('QR crop lies outside the decoded frame')
            frame = frame[y:y + height, x:x + width]
        value = cv2.QRCodeDetector().detectAndDecode(frame)[0]
        if value != JOB.LINE:
            raise ValueError('Long-film final QR payload mismatch')
        checks.append({'second': second, 'decoded': value})
    return {'status': 'PASS', 'checks': checks}


def verify(master, destination, audio_files, caption_files, chapters, end_card):
    final = MUX.probe(destination)
    video = [s for s in final['streams'] if s['codec_type'] == 'video']
    audio = [s for s in final['streams'] if s['codec_type'] == 'audio']
    captions = [s for s in final['streams'] if s['codec_type'] == 'subtitle']
    if len(video) != 1 or len(audio) != 5 or len(captions) != 5:
        raise ValueError('One video, five audio and five subtitle streams required')
    v = video[0]
    if (v['codec_name'] != 'h264' or int(v['nb_frames']) != 21600 or Fraction(v['r_frame_rate']) != 24
            or (v['width'], v['height']) != (1280, 720) or abs(float(v['duration']) - 900) > .001
            or abs(float(final['format']['duration']) - 900) > .025):
        raise ValueError('Long-film video contract differs from 900s/21600frames/720p24')
    original_packets, final_packets = MUX.packets(master, 'v:0'), MUX.packets(destination, 'v:0')
    if len(final_packets) != 21600 or original_packets != final_packets:
        raise ValueError('Master video packet data or timing changed')
    actual_chapters = [(float(c['start_time']), float(c['end_time']), c.get('tags', {}).get('title')) for c in final['chapters']]
    if actual_chapters != chapters:
        raise ValueError('Thirty chapter titles or time boundaries changed')
    for index, (language, iso, _) in enumerate(MUX.LANGUAGES):
        a, s = audio[index], captions[index]
        if a['codec_name'] != 'aac' or abs(float(a['duration']) - 900) > .025 or s['codec_name'] != 'mov_text':
            raise ValueError('Narration/subtitle format differs from the delivery contract')
        for stream in (a, s):
            if stream.get('tags', {}).get('language') != iso or stream['disposition']['default'] != int(index == 0):
                raise ValueError('Language/default stream flag mismatch')
        if MUX.packets(audio_files[index], 'a:0') != MUX.packets(destination, f'a:{index}'):
            raise ValueError('Narration packet data or timing changed')
        if MUX.subtitles(caption_files[index], '0:s:0') != MUX.subtitles(destination, f'0:s:{index}'):
            raise ValueError('Caption text, line breaks or timing changed')
    return {'status': 'PASS', 'videoPacketsByteIdentical': True, 'videoPacketTimingUnchanged': True,
            'aacPacketsByteIdentical': True, 'subtitleTextTimingAndLineBreaks': 'PASS',
            'chapterCount': 30, 'chapterBoundariesAndTitles': 'MATCHES_AUTHORED_SCRIPT',
            'qrDecoded': qr_verify(destination, 900, end_card.get('rectangle'))}


def build(script_path, audio_manifest_path, source_manifest_path, mapping_path):
    script = read(script_path)
    film = contract(script)
    output = DELIVERY / film
    source, speech, mapping = map(read, (source_manifest_path, audio_manifest_path, mapping_path))
    script_hash = MUX.sha(script_path)
    if speech.get('status') != 'PASS' or mapping.get('status') != 'PASS':
        raise ValueError('Five measured narration tracks and final semantic review must pass first')
    if speech.get('sourceScriptSha256') != script_hash or mapping.get('scriptSha256') != script_hash:
        raise ValueError('Narration/mapping belongs to a different script revision')
    if speech.get('durationSeconds') != 900 or speech.get('chapterCount') != 30:
        raise ValueError('Audio manifest must explicitly bind 900 seconds and 30 chapters')
    end_card = source.get('endCard', {})
    if (end_card.get('verified') is not True or end_card.get('url') != JOB.LINE
            or end_card.get('startSeconds') != 890 or end_card.get('endSeconds') != 900):
        raise ValueError('Verified 890–900-second LINE end card required')
    if source.get('sourceScriptSha256') != script_hash:
        raise ValueError('Master manifest must bind the reviewed long script')
    master = checked_file(source_manifest_path.parent, source)
    tracks = {t['language']: t for t in speech['tracks']}
    maps = {t['language']: t for t in mapping['tracks']}
    if len(speech['tracks']) != 5 or len(mapping['tracks']) != 5 or set(tracks) != set(LANGUAGES) or set(maps) != set(LANGUAGES):
        raise ValueError('Exactly five complete and unique language tracks required')
    prepared = []
    for language in LANGUAGES:
        track, meaning = tracks[language], maps[language]
        if track['tourId'] != film or meaning['tourId'] != film:
            raise ValueError('Narration/mapping film id mismatch')
        audio = checked_file(audio_manifest_path.parent, track)
        streams = [s for s in MUX.probe(audio)['streams'] if s['codec_type'] == 'audio']
        if len(streams) != 1 or streams[0]['codec_name'] != 'aac' or abs(float(streams[0]['duration']) - 900) > .025:
            raise ValueError('Each input narration must be a single 900-second AAC track')
        displays, subtitle_cues = display_track(track['cues'], meaning['sentences'], script['cues'], language)
        prepared.append((language, audio, displays, subtitle_cues))
    versions = metadata_text(script)  # Reject oversized metadata before changing any output.
    chapters = [(float(c['start']), float(c['end']), c['title']['en']) for c in script['cues']]
    declared = [(float(c['startSeconds']), float(c['endSeconds']), c['title']) for c in source['chaptersToMux']]
    if declared != chapters:
        raise ValueError('Source chapter manifest differs from reviewed script')
    output.mkdir(parents=True, exist_ok=True)
    destination = output / (film + '.mp4')
    if destination.resolve() == master:
        raise ValueError('Never replace the source master')
    subtitle_dir = output / 'subtitles-bilingual'
    bindings = {'scriptSha256': script_hash, 'sourceVideoSha256': source['sha256'],
                'audioManifestSha256': MUX.sha(audio_manifest_path), 'semanticMappingSha256': MUX.sha(mapping_path)}
    final_path = output / ('manifest.' + film + '.json')
    if destination.exists():
        if not final_path.exists() or any(read(final_path).get(k) != v for k, v in bindings.items()):
            raise ValueError('Existing completed film has different inputs; use a new reviewed version')
        existing = read(final_path)
        if existing['sha256'] != MUX.sha(destination):
            raise ValueError('Existing completed film changed after verification')
    caption_records, audio_files, caption_files = [], [], []
    browser = {'version': '34.0.0-long', 'status': 'PASS', 'duration': 900, 'trackCount': 5,
               'processes': {film: {}}}
    for language, audio, displays, subtitle_cues in prepared:
        record = {'language': language, 'cueCount': len(displays), 'cues': displays, 'files': {}}
        for suffix in ('vtt', 'srt'):
            file = subtitle_dir / f'{film}.{language}.{suffix}'
            atomic(file, BASE.render(subtitle_cues, suffix))
            record['files'][suffix] = {'file': str(file.relative_to(output)), 'sha256': MUX.sha(file), 'bytes': file.stat().st_size}
        caption_records.append(record)
        audio_files.append(audio)
        caption_files.append(subtitle_dir / f'{film}.{language}.vtt')
        browser['processes'][film][language] = displays
    if destination.exists():
        verification = verify(master, destination, audio_files, caption_files, chapters, end_card)
    else:
        with tempfile.TemporaryDirectory(prefix='long-mux-', dir=output) as temporary:
            folder = Path(temporary)
            chapter_file, staged = folder / 'chapters.ffmetadata', folder / destination.name
            chapter_file.write_text(SHORT.ffmetadata(chapters), 'utf-8')
            command = ['ffmpeg', '-v', 'error', '-y', '-i', master]
            for file in audio_files + caption_files:
                command += ['-i', file]
            command += ['-f', 'ffmetadata', '-i', chapter_file, '-map', '0:v:0']
            for index in range(1, 6):
                command += ['-map', f'{index}:a:0']
            for index in range(6, 11):
                command += ['-map', f'{index}:s:0']
            command += ['-map_chapters', '11', '-c:v', 'copy', '-c:a', 'copy', '-c:s', 'mov_text', '-movflags', '+faststart']
            for index, (language, iso, label) in enumerate(MUX.LANGUAGES):
                for kind, title in [('a', label), ('s', label if language == 'en' else label + ' + English')]:
                    command += [f'-metadata:s:{kind}:{index}', 'language=' + iso,
                                f'-metadata:s:{kind}:{index}', 'title=' + title,
                                f'-metadata:s:{kind}:{index}', 'handler_name=' + title,
                                f'-disposition:{kind}:{index}', 'default' if index == 0 else '0']
            MUX.run(command + [staged])
            verification = verify(master, staged, audio_files, caption_files, chapters, end_card)
            staged.replace(destination)
    caption_report = {'status': 'PASS', 'filmId': film, 'durationSeconds': 900, 'chapterCount': 30,
                      'timingPolicy': 'Native measured speech; display extends through gaps to the next sentence or chapter boundary. Original speech start/end retained. English is semantically mapped, never joined by English audio timing.',
                      **bindings, 'tracks': caption_records}
    atomic(output / 'BILINGUAL_SUBTITLE_MANIFEST_LONG_V34.json', caption_report)
    atomic(output / 'captions.json', browser)
    final = {'status': 'PASS', 'version': '34.0.0-long', 'id': film, 'file': destination.name,
             'bytes': destination.stat().st_size, 'sha256': MUX.sha(destination), 'durationSeconds': 900,
             'frames': 21600, 'width': 1280, 'height': 720, 'fps': '24/1', 'audioLanguages': list(LANGUAGES),
             'subtitleLanguages': list(LANGUAGES), 'defaultAudioLanguage': 'zh-TW', 'chapters': source['chaptersToMux'],
             'endCard': end_card, **bindings, 'verification': verification,
             'distribution': 'Local delivery and YouTube only; not public source or GitHub Release.',
             'publicationStatus': 'not-uploaded-by-this-local-build'}
    atomic(final_path, final)
    relative = lambda file: Path(os.path.relpath(file, output)).as_posix()
    video = {'id': film, **versions['default'], 'videoFile': destination.name,
             'videoSha256': final['sha256'], 'videoBytes': final['bytes'], 'defaultLanguage': 'zh-TW',
             'durationSeconds': 900,
             'defaultAudioLanguage': 'zh-TW', 'categoryId': '27', 'madeForKids': False, 'containsSyntheticMedia': True,
             'privacyStatus': 'public', 'notifySubscribers': False, 'localizations': {lang: versions[lang] for lang in LANGUAGES},
             'audioTracks': [{'language': lang, 'file': relative(file), 'sha256': MUX.sha(file), 'bytes': file.stat().st_size}
                             for lang, file in zip(LANGUAGES, audio_files)],
             'subtitleTracks': [{'language': r['language'], 'name': JOB.LABELS[r['language']],
                                'file': r['files']['vtt']['file'], 'sha256': r['files']['vtt']['sha256'],
                                'srtFile': r['files']['srt']['file'], 'srtSha256': r['files']['srt']['sha256']} for r in caption_records]}
    metadata = {'schemaVersion': 2, 'pathResolutionMode': 'metadata-relative', 'status': 'prepared-not-uploaded',
                'jobCompleteness': 'single-long-process-film', 'expectedChannelId': 'UCXcPnnnM7btkcHwSFkVckzQ',
                'mediaManifest': final_path.name, 'mediaManifestSha256': MUX.sha(final_path),
                'sourceScript': relative(script_path.resolve()), 'sourceScriptSha256': script_hash,
                'videos': [video], 'sources': script['sources'],
                'validation': {key: JOB.validate_text(**value) for key, value in versions.items()},
                'publicationNotes': {'uploader': 'Use Upload_Process_V34.sh with this metadata after offline preflight and channel quota reset. The six-overview job and state remain separate.',
                                     'alternateAudio': 'A multi-audio MP4 does not guarantee YouTube imports alternate tracks. Publish alternate narration in Studio when the channel supports it.',
                                     'playlistId': None, 'videoId': None, 'networkUsed': False}}
    atomic(output / 'youtube-metadata.long-v34.json', metadata)
    return final


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--script', type=Path, default=DELIVERY / 'C01-long.json')
    parser.add_argument('--audio-manifest', type=Path)
    parser.add_argument('--source-manifest', type=Path)
    parser.add_argument('--mapping', type=Path)
    parser.add_argument('--check-text-only', action='store_true')
    args = parser.parse_args()
    script = read(args.script)
    film = contract(script, require_languages=not args.check_text_only)
    if args.check_text_only:
        versions = metadata_text(script, script['languages'])
        print(json.dumps({'status': 'PASS', 'languages': script['languages'],
                          'validation': {key: JOB.validate_text(**value) for key, value in versions.items()}}, ensure_ascii=False))
        return
    result = build(args.script, args.audio_manifest or DELIVERY / f'AUDIO_MANIFEST_{film}.json',
                   args.source_manifest or DELIVERY / film / f'SOURCE_VIDEO_MANIFEST_{film}.json',
                   args.mapping or DELIVERY / film / f'SEMANTIC_MAPPING_{film}.json')
    print(json.dumps({'status': result['status'], 'file': str(DELIVERY / film / result['file']),
                      'bytes': result['bytes'], 'sha256': result['sha256']}, ensure_ascii=False))


if __name__ == '__main__':
    main()
