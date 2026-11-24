#!/usr/bin/env python3
"""Build the independent C01 narrated film, five caption tracks and review job.

Reads verified source media and measured narration. Never uploads, reads OAuth,
changes the six-overview job, or replaces the silent production master.
"""
from __future__ import annotations
import argparse
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
DELIVERY = ROOT.parent / 'delivery/process-v34'
SCRIPT = ROOT / 'docs/packaging-process-scripts-v34/C01.json'
PUBLIC = ROOT / 'public/academy'


def load_module(name, filename):
    spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(filename))
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


SUB = load_module('c01_subtitles', 'build-speech-aligned-subtitles-v34.py')
MUX = load_module('c01_mux', 'mux-narrated-packaging-v34.py')
JOB = load_module('c01_metadata', 'prepare-narrated-youtube-job-v34.py')
SUMMARY = {
 'zh-TW': '以假設的加速器建立可追溯需求表，從工作負載走到頻寬、散熱、外形與測試條件。所有數值都是教學假設，不是產品規格或量測結果。',
 'en': 'Build traceable requirements for a hypothetical accelerator, connecting workload to bandwidth, cooling, envelope and test conditions. Every numerical value is an educational assumption, not a product specification or measured result.',
 'ja': '仮想アクセラレーターを例に、ワークロードから帯域、冷却、寸法、試験条件へと追跡可能な要件を作ります。数値はすべて教育用の仮定であり、製品仕様や測定結果ではありません。',
 'ko': '가상의 가속기를 예로 작업 부하를 대역폭, 냉각, 크기와 시험 조건에 연결하여 추적 가능한 요구사항을 만듭니다. 모든 수치는 교육용 가정이며 제품 사양이나 측정 결과가 아닙니다.',
 'zh-CN': '以假设的加速器建立可追溯需求表，从工作负载走到带宽、散热、外形与测试条件。所有数值都是教学假设，不是产品规格或测量结果。'
}


def metadata_text(script):
    tour = {'id': 'C01', 'title': script['title'], 'summary': SUMMARY,
            'chapters': script['cues'], 'sources': script['sources']}
    JOB.OUTCOMES['C01'] = (
        '交付含需求 ID、單位、條件、責任人、驗證方法與版本的需求基線；分清原始線速與有效資料率、整體熱預算與局部熱點，並用失效情境檢查未決事項。',
        'Deliver a requirements baseline with IDs, units, conditions, owners, verification methods and revisions. Distinguish raw line rate from useful throughput and system heat budgets from local hot spots; challenge unresolved assumptions with a failure case.')
    versions = {'default': JOB.bilingual(tour, 1)}
    versions.update({language: JOB.localized(tour, language, 1) for language in JOB.LANGUAGES})
    for version in versions.values():
        version['title'] = version['title'].replace('01｜', 'C01｜', 1)
        version['description'] = version['description'].replace(
            JOB.ACADEMY + 'packaging-tour-v33.html?tour=C01&lang=',
            JOB.ACADEMY + 'packaging-process-film-v34.html?lang=')
        version['description'] += '\n\n120 工序技術路線 / Process roadmap\n' + JOB.ACADEMY + 'packaging-process-v34.html#process-C01'
        JOB.validate_text(**version)
    return versions


def ffmetadata(chapters):
    def escape(value):
        for char in ('\\', '=', ';', '#'):
            value = value.replace(char, '\\' + char)
        return value.replace('\n', ' ')
    result = ';FFMETADATA1\n'
    for chapter in chapters:
        result += ('[CHAPTER]\nTIMEBASE=1/1000\n'
                   f'START={round(chapter[0] * 1000)}\nEND={round(chapter[1] * 1000)}\n'
                   f'title={escape(chapter[2])}\n')
    return result


def build(output, audio_manifest_path, source_manifest_path, mapping_path, master_override=None):
    script = json.loads(SCRIPT.read_text('utf-8'))
    source_manifest = json.loads(source_manifest_path.read_text('utf-8'))
    audio_manifest = json.loads(audio_manifest_path.read_text('utf-8'))
    mapping = json.loads(mapping_path.read_text('utf-8'))
    if audio_manifest.get('status') != 'PASS' or mapping.get('status') != 'PASS':
        raise ValueError('All five measured C01 narration tracks and exact-text semantic mappings must pass first')
    if mapping.get('scriptSha256') != MUX.sha(SCRIPT) or audio_manifest.get('sourceScriptSha256') != MUX.sha(SCRIPT):
        raise ValueError('C01 script differs from the measured/mapped source')
    if source_manifest.get('endCard', {}).get('verified') is not True or source_manifest.get('endCard', {}).get('url') != MUX.LINE_URL:
        raise ValueError('Verified C01 LINE QR source required')
    source = master_override or Path(source_manifest['file'])
    if not source.is_file() or source.stat().st_size != source_manifest['bytes'] or MUX.sha(source) != source_manifest['sha256']:
        raise ValueError('C01 source master differs from its verified manifest')
    tracks = {t['language']: t for t in audio_manifest['tracks'] if t['tourId'] == 'C01'}
    if set(tracks) != set(JOB.LANGUAGES) or len(audio_manifest['tracks']) != 5:
        raise ValueError('Exactly five C01 language tracks required')
    audio_files = []
    for language, _, _ in MUX.LANGUAGES:
        record = tracks[language]
        file = audio_manifest_path.parent / record['file']
        if file.stat().st_size != record['bytes'] or MUX.sha(file) != record['sha256']:
            raise ValueError('C01 narration changed after validation')
        stream = [s for s in MUX.probe(file)['streams'] if s['codec_type'] == 'audio']
        if len(stream) != 1 or stream[0]['codec_name'] != 'aac' or abs(float(stream[0]['duration']) - 300) > .025:
            raise ValueError('C01 narration is not a single 300-second AAC stream')
        audio_files.append(file.resolve())
    subtitle_dir = output / 'subtitles-bilingual'
    caption_report = SUB.build(audio_manifest_path, subtitle_dir, semantic_mapping=mapping, file_suffix='C01')
    captions = [subtitle_dir / f'C01.{language}.vtt' for language, _, _ in MUX.LANGUAGES]
    chapters = [(float(c['start']), float(c['end']), c['title']['en']) for c in script['cues']]
    manifest_chapters = [(float(c['startSeconds']), float(c['endSeconds']), c['title']) for c in source_manifest['chaptersToMux']]
    if len(chapters) != 10 or chapters != manifest_chapters or any(c[:2] != (i * 30, (i + 1) * 30) for i, c in enumerate(chapters)):
        raise ValueError('C01 chapter contract mismatch')
    destination = output / 'C01.mp4'
    if destination.resolve() == source.resolve():
        raise ValueError('Never replace the source master')
    if destination.exists():
        verification = MUX.verify(source, destination, audio_files, captions, expected_chapters=chapters,
                                  qr_rectangle=source_manifest['endCard'].get('rectangle'))
    else:
        with tempfile.TemporaryDirectory(prefix='C01-mux-', dir=output) as temporary:
            folder = Path(temporary)
            chapter_file = folder / 'chapters.ffmetadata'
            chapter_file.write_text(ffmetadata(chapters), 'utf-8')
            staged = folder / 'C01.mp4'
            command = ['ffmpeg', '-v', 'error', '-y', '-i', source]
            for file in audio_files + captions:
                command += ['-i', file]
            command += ['-f', 'ffmetadata', '-i', chapter_file, '-map', '0:v:0']
            for i in range(1, 6):
                command += ['-map', f'{i}:a:0']
            for i in range(6, 11):
                command += ['-map', f'{i}:s:0']
            command += ['-map_chapters', '11', '-c:v', 'copy', '-c:a', 'copy', '-c:s', 'mov_text', '-movflags', '+faststart']
            for i, (language, iso, label) in enumerate(MUX.LANGUAGES):
                for kind, title in [('a', label), ('s', label if language == 'en' else label + ' + English')]:
                    command += [f'-metadata:s:{kind}:{i}', f'language={iso}',
                                f'-metadata:s:{kind}:{i}', f'title={title}',
                                f'-metadata:s:{kind}:{i}', f'handler_name={title}',
                                f'-disposition:{kind}:{i}', 'default' if i == 0 else '0']
            command += [staged]
            MUX.run(command)
            verification = MUX.verify(source, staged, audio_files, captions, expected_chapters=chapters,
                                      qr_rectangle=source_manifest['endCard'].get('rectangle'))
            staged.replace(destination)
    browser = {'version': '34.0.0', 'status': 'PASS', 'processId': 'C01', 'trackCount': 5,
               'duration': 300, 'processes': {'C01': {}}}
    public_tracks = []
    for record in caption_report['tracks']:
        language = record['language']
        browser['processes']['C01'][language] = [
            {'start': c['displayStart'], 'end': c['displayEnd'], 'text': c['text'],
             'english': '' if language == 'en' else c['englishText'],
             'speechStart': c['speechStart'], 'speechEnd': c['speechEnd']} for c in record['cues']]
        audio_relative = f'assets/packaging-process-v34/C01/audio/C01.{language}.m4a'
        caption_relative = f'assets/packaging-process-v34/C01/subtitles/C01.{language}.vtt'
        audio_target, caption_target = output / 'public-assets' / audio_relative, output / 'public-assets' / caption_relative
        audio_target.parent.mkdir(parents=True, exist_ok=True)
        caption_target.parent.mkdir(parents=True, exist_ok=True)
        source_audio = audio_manifest_path.parent / tracks[language]['file']
        shutil.copyfile(source_audio, audio_target)
        shutil.copyfile(subtitle_dir / f'C01.{language}.vtt', caption_target)
        if MUX.sha(audio_target) != tracks[language]['sha256'] or MUX.sha(caption_target) != record['files']['vtt']['sha256']:
            raise ValueError('Published sidecar copy differs from the verified input')
        public_tracks.append({'language': language, 'audio': audio_relative, 'audioSha256': MUX.sha(audio_target),
                              'audioBytes': audio_target.stat().st_size, 'stagedAudio': str(audio_target.resolve()),
                              'caption': caption_relative, 'captionSha256': MUX.sha(caption_target),
                              'stagedCaption': str(caption_target.resolve())})
    caption_js = output / 'public-assets/packaging-process-captions-v34.js'
    caption_js.write_text(
        'window.MACGYVER_PACKAGING_PROCESS_CAPTIONS=' + json.dumps(browser, ensure_ascii=False, separators=(',', ':')) + ';\n', 'utf-8')
    final = {'schemaVersion': 1, 'version': '34.0.0', 'status': 'PASS', 'processId': 'C01',
             'file': str(destination.resolve()), 'remoteUrl': None, 'bytes': destination.stat().st_size, 'sha256': MUX.sha(destination),
             'durationSeconds': 300, 'frames': 7200, 'width': 1280, 'height': 720, 'fps': '24/1',
             'audioLanguages': list(JOB.LANGUAGES), 'subtitleLanguages': list(JOB.LANGUAGES), 'defaultAudioLanguage': 'zh-TW',
             'chapters': source_manifest['chaptersToMux'], 'endCard': source_manifest['endCard'],
             'verification': verification, 'publicTracks': public_tracks, 'stagedCaptionScript': str(caption_js.resolve()),
             'publicAssetsInstalled': False,
             'sourceVideoSha256': source_manifest['sha256'], 'sourceScriptSha256': MUX.sha(SCRIPT),
             'audioManifestSha256': MUX.sha(audio_manifest_path), 'semanticMappingSha256': MUX.sha(mapping_path),
             'publicationStatus': 'not-uploaded-by-this-local-build', 'masterModified': False}
    manifest_output = output / 'manifest.C01.json'
    manifest_output.write_text(json.dumps(final, ensure_ascii=False, indent=2) + '\n', 'utf-8')
    versions = metadata_text(script)
    video = {'id': 'C01', **versions['default'], 'defaultLanguage': 'zh-TW', 'defaultAudioLanguage': 'zh-TW',
             'localizations': {language: versions[language] for language in JOB.LANGUAGES},
             'videoFile': str(destination.resolve()), 'videoBytes': final['bytes'], 'videoSha256': final['sha256'],
             'durationSeconds': 300, 'chapters': final['chapters'], 'sources': script['sources'],
             'audioTracks': [{'language': l, 'file': str((audio_manifest_path.parent / tracks[l]['file']).resolve()),
                              'sha256': tracks[l]['sha256'], 'default': l == 'zh-TW'} for l in JOB.LANGUAGES],
             'subtitleTracks': [{'language': r['language'], 'label': JOB.LABELS[r['language']],
                                 'file': r['files']['vtt']['file'], 'sha256': r['files']['vtt']['sha256'],
                                 'srtFile': r['files']['srt']['file'], 'srtSha256': r['files']['srt']['sha256']} for r in caption_report['tracks']]}
    old = json.loads((ROOT / 'docs/PACKAGING_YOUTUBE_METADATA_V33.json').read_text('utf-8'))
    job = {'schemaVersion': 2, 'jobVersion': '34.0.0-C01', 'status': 'prepared-not-uploaded',
           'jobCompleteness': 'single-process-film', 'expectedChannel': 'UCXcPnnnM7btkcHwSFkVckzQ',
           'playlist': {'title': old['playlist']['title'], 'requireExisting': False,
                        'creationPolicy': 'reuse-exact-title-or-create-if-absent'},
           'mediaManifest': str(manifest_output.resolve()), 'mediaManifestSha256': MUX.sha(manifest_output),
           'publicationNotes': {'noVideoIdInvented': True, 'noNetworkOrOAuthUsed': True,
                                'uploadMethod': 'Review/upload C01 separately in Studio; the six-overview publisher intentionally rejects this independent process job.',
                                'audio': 'Five embedded AAC tracks plus independent M4A files. YouTube alternate languages require explicit supported Studio publication.',
                                'seriesStatus': 'C01 is one produced design-activity film. The remaining 119 process films have independent production status.'},
           'videos': [video], 'validation': {key: JOB.validate_text(**value) for key, value in versions.items()}}
    job_dir = output / 'youtube-job-C01-v34'
    job_dir.mkdir(exist_ok=True)
    (job_dir / 'metadata.json').write_text(json.dumps(job, ensure_ascii=False, indent=2) + '\n', 'utf-8')
    return final


def export_source_job(input_job, destination):
    result = json.loads(input_job.read_text('utf-8'))
    if result.get('jobCompleteness') != 'single-process-film' or [v['id'] for v in result['videos']] != ['C01']:
        raise ValueError('The reviewed independent C01 job is required')
    video = result['videos'][0]
    installed = PUBLIC / 'assets/packaging-process-v34/C01'
    manifest_path, movie = installed / 'manifest.json', installed / 'C01.mp4'
    manifest = json.loads(manifest_path.read_text('utf-8'))
    if (manifest.get('status') != 'PASS' or manifest.get('sha256') != video['videoSha256']
            or MUX.sha(movie) != video['videoSha256'] or movie.stat().st_size != video['videoBytes']):
        raise ValueError('Installed C01 movie/manifest differs from the reviewed job')
    relative = lambda file: Path(os.path.relpath(file.resolve(), destination.resolve().parent)).as_posix()
    result['mediaManifest'], result['mediaManifestSha256'] = relative(manifest_path), MUX.sha(manifest_path)
    result['pathResolutionMode'] = 'metadata-relative'
    result['sourceFile'] = relative(SCRIPT)
    video['videoFile'] = relative(movie)
    for track in video['audioTracks']:
        file = installed / 'audio' / f'C01.{track["language"]}.m4a'
        if MUX.sha(file) != track['sha256']:
            raise ValueError('Installed C01 narration mismatch')
        track['file'] = relative(file)
    for track in video['subtitleTracks']:
        file = installed / 'subtitles' / f'C01.{track["language"]}.vtt'
        srt = file.with_suffix('.srt')
        if MUX.sha(file) != track['sha256'] or MUX.sha(srt) != track['srtSha256']:
            raise ValueError('Installed C01 caption mismatch')
        track['file'], track['srtFile'] = relative(file), relative(srt)
    result['publicationNotes']['portableAssetsVerified'] = True
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', 'utf-8')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=DELIVERY / 'narrated')
    parser.add_argument('--audio-manifest', type=Path, default=DELIVERY / 'AUDIO_MANIFEST_C01.json')
    parser.add_argument('--source-manifest', type=Path, default=DELIVERY / 'C01/SOURCE_VIDEO_MANIFEST_C01.json')
    parser.add_argument('--mapping', type=Path, default=DELIVERY / 'C01/SEMANTIC_MAPPING_C01.json')
    parser.add_argument('--master', type=Path)
    parser.add_argument('--check-text-only', action='store_true')
    parser.add_argument('--export-source-job', type=Path)
    parser.add_argument('--input-job', type=Path, default=DELIVERY / 'narrated/youtube-job-C01-v34/metadata.json')
    args = parser.parse_args()
    if args.export_source_job:
        export_source_job(args.input_job, args.export_source_job)
        print(json.dumps({'status': 'PASS', 'portableJob': str(args.export_source_job.resolve())}, ensure_ascii=False))
        return
    if args.check_text_only:
        versions = metadata_text(json.loads(SCRIPT.read_text('utf-8')))
        print(json.dumps({'status': 'PASS', 'validation': {k: JOB.validate_text(**v) for k, v in versions.items()}}, ensure_ascii=False))
        return
    subprocess.run(['node', str(ROOT / 'tools/build-c01-semantic-mapping-v34.mjs'), '--require-all'], check=True)
    result = build(args.output, args.audio_manifest, args.source_manifest, args.mapping, args.master)
    print(json.dumps({'status': result['status'], 'file': result['file'], 'bytes': result['bytes'], 'sha256': result['sha256']}, ensure_ascii=False))


if __name__ == '__main__':
    main()
