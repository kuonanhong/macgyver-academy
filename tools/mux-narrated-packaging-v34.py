#!/usr/bin/env python3
"""Create verified narrated delivery MP4s without replacing the original movies.

Needs FFmpeg/ffprobe; OpenCV + NumPy enable independent final-frame QR decoding.
Original H.264 and all five existing AAC tracks are copied, never re-encoded.
All input hashes and final speech-aligned bilingual captions are required.
"""
from __future__ import annotations
import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parent
ASSETS = ROOT / 'public/academy/assets/packaging-tour-v33'
IDS = ('interposer', 'fanout', 'hybrid', 'bridge', 'chiplet', 'thermal')
LANGUAGES = (('zh-TW', 'zho', '繁體中文'), ('en', 'eng', 'English'),
             ('ja', 'jpn', '日本語'), ('ko', 'kor', '한국어'), ('zh-CN', 'zho', '简体中文'))
LINE_URL = 'https://line.me/R/ti/p/%40530pgchc'


def run(command):
    return subprocess.run([str(x) for x in command], check=True, capture_output=True, text=True).stdout


def sha(file):
    h = hashlib.sha256()
    with Path(file).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def probe(file):
    return json.loads(run(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-show_chapters', '-of', 'json', file]))


def packets(file, selector):
    return json.loads(run(['ffprobe', '-v', 'error', '-select_streams', selector, '-show_packets',
                          '-show_data_hash', 'sha256', '-show_entries',
                          'packet=pts_time,dts_time,duration_time,size,data_hash', '-of', 'json', file]))['packets']


def qr_checks(file, rectangle=None):
    try:
        import cv2
        import numpy as np
    except ImportError:
        return {'status': 'NOT_RUN', 'reason': 'OpenCV/NumPy not installed; unchanged video packet proof preserves the verified original QR.'}
    checks = []
    for second in (290, 295, 299 + 23 / 24):
        raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{second:.9f}', '-i', str(file),
                              '-map', '0:v:0', '-frames:v', '1', '-f', 'image2pipe', '-vcodec', 'png', '-'],
                             check=True, capture_output=True).stdout
        frame = cv2.imdecode(np.frombuffer(raw, dtype=np.uint8), cv2.IMREAD_COLOR)
        if rectangle:
            x, y, width, height = (int(rectangle[k]) for k in ('x', 'y', 'width', 'height'))
            if min(x, y) < 0 or min(width, height) <= 0 or x + width > frame.shape[1] or y + height > frame.shape[0]:
                raise ValueError('QR region lies outside the decoded final frame')
            frame = frame[y:y + height, x:x + width]
        value = cv2.QRCodeDetector().detectAndDecode(frame)[0]
        if value != LINE_URL:
            raise ValueError('Final QR payload mismatch')
        checks.append({'second': second, 'decoded': value})
    return {'status': 'PASS', 'checks': checks}


def subtitles(file, selector):
    text = run(['ffmpeg', '-v', 'error', '-i', file, '-map', selector, '-f', 'webvtt', '-'])
    result = []
    for block in text.strip().split('\n\n'):
        lines = block.splitlines()
        times = next((i for i, line in enumerate(lines) if ' --> ' in line), None)
        if times is not None:
            result.append((lines[times], '\n'.join(lines[times + 1:])))
    return result


def verify(source, destination, audio_files, subtitle_files, expected_chapters=None, qr_rectangle=None):
    original, final = probe(source), probe(destination)
    video = [s for s in final['streams'] if s['codec_type'] == 'video']
    audio = [s for s in final['streams'] if s['codec_type'] == 'audio']
    captions = [s for s in final['streams'] if s['codec_type'] == 'subtitle']
    if len(video) != 1 or video[0]['codec_name'] != 'h264' or int(video[0]['nb_frames']) != 7200:
        raise ValueError('Unexpected video codec or frame count')
    if (video[0]['width'], video[0]['height']) != (1280, 720) or Fraction(video[0]['r_frame_rate']) != 24:
        raise ValueError('Unexpected video dimensions or frame rate')
    if abs(float(video[0]['duration']) - 300) > .001 or abs(float(final['format']['duration']) - 300) > .025:
        raise ValueError('Final duration differs from 300 seconds')
    old_packets, new_packets = packets(source, 'v:0'), packets(destination, 'v:0')
    if len(new_packets) != 7200 or old_packets != new_packets:
        raise ValueError('Video packet bytes, timestamps or durations changed')
    chapter_values = lambda m: [(float(c['start_time']), float(c['end_time']), c.get('tags', {}).get('title')) for c in m['chapters']]
    required_chapters = chapter_values(original) if expected_chapters is None else expected_chapters
    if len(final['chapters']) != 10 or required_chapters != chapter_values(final):
        raise ValueError('The original ten chapters changed')
    if len(audio) != 5 or len(captions) != 5:
        raise ValueError('Five audio and five subtitle tracks required')
    for index, (language, iso, label) in enumerate(LANGUAGES):
        track = audio[index]
        if track['codec_name'] != 'aac' or abs(float(track['duration']) - 300) > .025:
            raise ValueError('Unexpected audio codec/duration')
        if track.get('tags', {}).get('language') != iso or track['disposition']['default'] != int(index == 0):
            raise ValueError('Audio language/default disposition mismatch')
        if packets(audio_files[index], 'a:0') != packets(destination, f'a:{index}'):
            raise ValueError('AAC packet bytes or timing changed during mux')
        if captions[index]['codec_name'] != 'mov_text' or captions[index].get('tags', {}).get('language') != iso:
            raise ValueError('Subtitle codec/language mismatch')
        if subtitles(subtitle_files[index], '0:s:0') != subtitles(destination, f'0:s:{index}'):
            raise ValueError('Subtitle text, line breaks or timestamps changed during mux')
    qr = qr_checks(destination, qr_rectangle)
    return {'status': 'PASS', 'videoPacketsByteIdentical': True, 'videoPacketTimingUnchanged': True,
            'aacPacketsByteIdentical': True, 'subtitleTextTimingAndLineBreaks': 'PASS',
            'chapterBoundariesAndTitles': 'UNCHANGED' if expected_chapters is None else 'MATCHES_AUTHORED_SCRIPT', 'qrDecoded': qr,
            'defaultAudioLanguage': 'zh-TW', 'defaultSubtitleLanguage': 'zh-TW'}


def assemble_verified(output, original_manifest_path, audio_manifest_path, inputs):
    """Combine already verified per-film jobs after rechecking every input hash.

No movie is rewritten or decoded again. Each frozen per-film review job binds
its validation manifest, output MP4, all audio files and all caption files.
"""
    entries = []
    original_hash = sha(original_manifest_path)
    template = None
    for tour in IDS:
        partial_path = output / f'manifest.{tour}.partial.json'
        review_path = output / 'youtube-job-v34' / f'{tour}.metadata.json'
        partial = json.loads(partial_path.read_text('utf-8'))
        review = json.loads(review_path.read_text('utf-8'))
        if partial.get('originalManifestSha256') != original_hash or review.get('mediaManifestSha256') != sha(partial_path):
            raise ValueError('Per-film review manifest changed: ' + tour)
        if len(partial.get('videos', [])) != 1 or len(review.get('videos', [])) != 1:
            raise ValueError('Expected one verified film per partial job')
        entry, record = partial['videos'][0], review['videos'][0]
        destination = output / f'{tour}.mp4'
        if entry['id'] != tour or record['id'] != tour or entry.get('verification', {}).get('status') != 'PASS':
            raise ValueError('Per-film verification is incomplete')
        if (destination.stat().st_size != entry['bytes'] or entry['bytes'] != record['videoBytes']
                or sha(destination) != entry['sha256'] or entry['sha256'] != record['videoSha256']):
            raise ValueError('Previously verified film changed')
        audio_records = {t['language']: t for t in record['audioTracks']}
        caption_records = {t['language']: t for t in record['subtitleTracks']}
        _, audio, captions = inputs[tour]
        for i, (language, _, _) in enumerate(LANGUAGES):
            if sha(audio[i]) != audio_records[language]['sha256'] or sha(captions[i]) != caption_records[language]['sha256']:
                raise ValueError('Previously verified narration/captions changed: ' + tour)
        entries.append(entry)
        template = template or partial
    final = {**template, 'status': 'PASS', 'audioManifestSha256': sha(audio_manifest_path), 'videos': entries,
             'assemblyVerification': 'All six per-film packet/QR/caption verifications remain bound to unchanged MP4, audio and subtitle SHA256 values; no completed movie was rewritten.'}
    target = output / 'manifest.json'
    target.write_text(json.dumps(final, ensure_ascii=False, indent=2) + '\n', 'utf-8')
    return target


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--audio-manifest', type=Path, default=WORKSPACE / 'delivery/narration-v34/AUDIO_MANIFEST_V34.json')
    parser.add_argument('--subtitles', type=Path, default=WORKSPACE / 'delivery/narrated-v33/subtitles-bilingual')
    parser.add_argument('--output', type=Path, default=WORKSPACE / 'delivery/narrated-v33')
    parser.add_argument('--tour', choices=IDS, help='Review one completed five-language movie while other narration is still being generated; writes a PARTIAL manifest.')
    parser.add_argument('--assemble-verified', action='store_true', help='Assemble six completed per-film review jobs by rechecking their bound hashes, without rewriting or decoding completed movies.')
    args = parser.parse_args()
    if args.tour and args.assemble_verified:
        parser.error('--tour cannot be combined with --assemble-verified')
    selected = (args.tour,) if args.tour else IDS
    original_manifest_path = ASSETS / 'videos/manifest.json'
    original = json.loads(original_manifest_path.read_text('utf-8'))
    speech = json.loads(args.audio_manifest.read_text('utf-8'))
    caption_manifest = json.loads((args.subtitles / 'BILINGUAL_SUBTITLE_MANIFEST_V34.json').read_text('utf-8'))
    caption_records = {(t['tourId'], t['language']): t for t in caption_manifest['tracks']}
    if original.get('status') != 'PASS' or original.get('endCard', {}).get('verified') is not True:
        raise ValueError('Verified original QR video manifest required')
    if speech.get('status') != 'PASS' and not (args.tour and speech.get('status') == 'PARTIAL'):
        raise ValueError('Completed, validated speech manifest required')
    tracks = {(t['tourId'], t['language']): t for t in speech['tracks']}
    required = {(tour, language) for tour in selected for language, _, _ in LANGUAGES}
    if len(tracks) != len(speech['tracks']) or not required.issubset(tracks) or (not args.tour and set(tracks) != required):
        raise ValueError('Exactly five final audio tracks required per selected movie')
    videos = {v['id']: v for v in original['videos']}
    inputs = {}
    for tour in selected:
        source = ASSETS / 'videos' / (tour + '.mp4')
        if source.stat().st_size != videos[tour]['bytes'] or sha(source) != videos[tour]['sha256']:
            raise ValueError('Original video manifest mismatch')
        audio, captions = [], []
        for language, _, _ in LANGUAGES:
            record = tracks[(tour, language)]
            file = Path(record['file'])
            if not file.is_absolute():
                file = args.audio_manifest.parent / file
            if file.stat().st_size != record['bytes'] or sha(file) != record['sha256']:
                raise ValueError('Narration manifest mismatch')
            streams = [s for s in probe(file)['streams'] if s['codec_type'] == 'audio']
            if len(streams) != 1 or streams[0]['codec_name'] != 'aac' or abs(float(streams[0]['duration']) - 300) > .025:
                raise ValueError('Input narration must be a single 300-second AAC track')
            subtitle = args.subtitles / f'{tour}.{language}.vtt'
            caption_record = caption_records.get((tour, language))
            if not subtitle.is_file() or not caption_record or sha(subtitle) != caption_record['files']['vtt']['sha256']:
                raise ValueError('Missing or changed speech-aligned bilingual VTT')
            recorded_speech = [(c['speechStart'], c['speechEnd'], c['text']) for c in caption_record['cues']]
            measured_speech = [(c['start'], c['end'], c['text']) for c in record['cues']]
            if recorded_speech != measured_speech:
                raise ValueError('Subtitle timing/text belongs to a different narration recording')
            audio.append(file.resolve())
            captions.append(subtitle.resolve())
        inputs[tour] = (source, audio, captions)
    output = args.output.resolve()
    if output == (ASSETS / 'videos').resolve():
        raise ValueError('Never overwrite the original movies')
    output.mkdir(parents=True, exist_ok=True)
    if args.assemble_verified:
        target = assemble_verified(output, original_manifest_path, args.audio_manifest, inputs)
        print(json.dumps({'status': 'PASS', 'videos': 6, 'manifest': str(target)}, ensure_ascii=False))
        return
    entries = []
    for tour in selected:
        source, audio, captions = inputs[tour]
        destination = output / f'{tour}.mp4'
        if destination.exists():
            # A completed file may already be under review/upload. Verify it
            # against every current input without replacing or rewriting it.
            # Changed inputs fail closed; use a new output directory/version.
            verification = verify(source, destination, audio, captions)
        else:
            with tempfile.TemporaryDirectory(prefix=f'{tour}-mux-', dir=output) as temporary:
                staged = Path(temporary) / destination.name
                command = ['ffmpeg', '-v', 'error', '-y', '-i', source]
                for file in audio + captions:
                    command += ['-i', file]
                command += ['-map', '0:v:0']
                for i in range(1, 6):
                    command += ['-map', f'{i}:a:0']
                for i in range(6, 11):
                    command += ['-map', f'{i}:s:0']
                command += ['-c:v', 'copy', '-c:a', 'copy', '-c:s', 'mov_text', '-map_chapters', '0',
                            '-movflags', '+faststart']
                for i, (language, iso, label) in enumerate(LANGUAGES):
                    subtitle_label = label if language == 'en' else label + ' + English'
                    for kind, title in [('a', label), ('s', subtitle_label)]:
                        command += [f'-metadata:s:{kind}:{i}', f'language={iso}',
                                    f'-metadata:s:{kind}:{i}', f'title={title}',
                                    f'-metadata:s:{kind}:{i}', f'handler_name={title}',
                                    f'-disposition:{kind}:{i}', 'default' if i == 0 else '0']
                command += [staged]
                run(command)
                verification = verify(source, staged, audio, captions)
                staged.replace(destination)
        entry = {**videos[tour], 'file': destination.name, 'bytes': destination.stat().st_size, 'sha256': sha(destination),
                 'audioLanguages': [l[0] for l in LANGUAGES], 'defaultAudioLanguage': 'zh-TW',
                 'subtitleMode': 'native language with semantically aligned English; English-only en track',
                 'verification': verification}
        entries.append(entry)
        print(json.dumps({'id': tour, 'status': 'PASS', 'bytes': entry['bytes']}, ensure_ascii=False), flush=True)
    final = {**original, 'version': '34.0.0', 'silent': False, 'status': 'PARTIAL' if args.tour else 'PASS',
             'encoding': 'Original 720p H.264 and five AAC speech tracks stream-copied; five speech-aligned mov_text tracks.',
             'audioProvider': 'Installed macOS synthetic voices; not human narration',
             'originalVideosModified': False, 'originalManifestSha256': sha(original_manifest_path),
             'audioManifestSha256': sha(args.audio_manifest), 'videos': entries}
    manifest_output = output / (f'manifest.{args.tour}.partial.json' if args.tour else 'manifest.json')
    manifest_output.write_text(json.dumps(final, ensure_ascii=False, indent=2) + '\n', 'utf-8')
    print(json.dumps({'status': final['status'], 'videos': len(entries), 'manifest': str(manifest_output)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
