#!/usr/bin/env python3
"""Add a verified LINE QR card in seconds 290–300 without re-recording the films.

Dependencies: Python 3.9+, Pillow, opencv-python (or opencv-python-headless),
NumPy, FFmpeg/ffprobe with libx264. Existing source MP4s are backed up first.
Only the final GOPs are re-encoded; the initial video packets are stream-copied.
Default: create an interposer preview outside public/. --all renders all films;
--apply installs verified outputs and refreshes their media manifest.

Use this retrofit only for the previously published films without a QR card.
The v33.0.2 browser renderer already draws its own card; finalize those recordings
with finalize-packaging-videos-v33.py instead. Already verified QR films are a no-op.
"""
from __future__ import annotations
import argparse
from fractions import Fraction
import hashlib
import json
import math
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

try:
    import cv2
    import numpy as np
    from PIL import Image, ImageDraw, ImageFont
except ImportError as error:
    raise SystemExit('Install media dependencies in a virtual environment: python -m pip install Pillow opencv-python-headless numpy') from error

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'public/academy/assets/packaging-tour-v33'
IDS = ('interposer', 'fanout', 'hybrid', 'bridge', 'chiplet', 'thermal')
URL = 'https://line.me/R/ti/p/%40530pgchc'
FPS = 24
START = 290
CARD_X, CARD_Y = 976, 175
CARD_WIDTH, CARD_HEIGHT = 276, 380


def sha(file):
    h = hashlib.sha256()
    with Path(file).open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def run(argv):
    result = subprocess.run([str(x) for x in argv], check=True, capture_output=True, text=True)
    return result.stdout


def probe(file):
    return json.loads(run(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-show_chapters', '-of', 'json', file]))


def font(size, explicit=None):
    choices = [explicit] if explicit else []
    choices += ['/Library/Fonts/Arial Unicode.ttf', '/System/Library/Fonts/Supplemental/Arial Unicode.ttf',
                '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
                'C:/Windows/Fonts/msjh.ttc']
    for candidate in choices:
        if candidate and Path(candidate).is_file():
            return ImageFont.truetype(candidate, size)
    raise ValueError('A CJK font is required for 郭南宏. Supply --font PATH; no font is bundled.')


def make_card(explicit_font=None):
    params = cv2.QRCodeEncoder_Params()
    params.correction_level = cv2.QRCODE_ENCODER_CORRECT_LEVEL_H
    matrix = cv2.QRCodeEncoder_create(params).encode(URL)
    ys, xs = np.where(matrix < 128)
    core = matrix[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    # Four-module white quiet zone, plus integer nearest-neighbor module sizing.
    bordered = np.pad(core, 4, constant_values=255)
    qr = Image.fromarray(bordered).convert('RGB')
    scale = 246 // qr.width
    qr = qr.resize((qr.width * scale, qr.height * scale), getattr(Image, 'Resampling', Image).NEAREST)
    qr_file = ASSETS / 'line-530pgchc-qr.png'
    qr.save(qr_file)
    decoded = cv2.QRCodeDetector().detectAndDecode(cv2.imread(str(qr_file)))[0]
    if decoded != URL:
        raise ValueError('Generated QR does not decode to the exact official-account URL.')
    card = Image.new('RGB', (CARD_WIDTH, CARD_HEIGHT), 'white')
    draw = ImageDraw.Draw(card)
    draw.rectangle((0, 0, CARD_WIDTH - 1, CARD_HEIGHT - 1), outline='#bfd6ca', width=2)
    draw.rectangle((0, 0, CARD_WIDTH - 1, 5), fill='#06c755')
    for text, size, y, fill in [('郭南宏 官方帳號', 20, 16, '#122a20'),
                               ('LINE  ·  SCAN TO ADD', 13, 43, '#087b36'),
                               ('@530pgchc', 25, 320, '#15291f'),
                               ('好友加入 / Add friend', 12, 354, '#486154')]:
        face = font(size, explicit_font)
        bounds = draw.textbbox((0, 0), text, font=face)
        draw.text(((CARD_WIDTH - (bounds[2] - bounds[0])) / 2, y - bounds[1]), text, font=face, fill=fill)
    card.paste(qr, ((CARD_WIDTH - qr.width) // 2, 66))
    card_file = ASSETS / 'line-530pgchc-endcard.png'
    card.save(card_file)
    return card_file, {'url': URL, 'errorCorrection': 'H', 'quietZoneModules': 4,
                       'qrPixels': qr.width, 'qrSha256': sha(qr_file), 'cardSha256': sha(card_file),
                       'x': CARD_X, 'y': CARD_Y, 'width': CARD_WIDTH, 'height': CARD_HEIGHT,
                       'start': START, 'end': 300}


def backup_originals(backup):
    backup.mkdir(parents=True, exist_ok=True)
    saved = backup / 'manifest.json'
    if saved.exists():
        manifest = json.loads(saved.read_text('utf-8'))
    else:
        manifest = json.loads((ASSETS / 'videos/manifest.json').read_text('utf-8'))
        if manifest.get('lineQr') or manifest.get('endCard'):
            raise ValueError('These movies already carry a LINE QR. Choose their original backup directory.')
        if sorted(v['id'] for v in manifest['videos']) != sorted(IDS):
            raise ValueError('Expected all six published original films.')
    for item in manifest['videos']:
        dest = backup / (item['id'] + '.mp4')
        current = ASSETS / 'videos' / dest.name
        if saved.exists() and sha(current) != item['sha256']:
            raise ValueError('Current video differs from the original backup. Do not retrofit newly rendered QR movies: ' + item['id'])
        if not dest.exists():
            source = ASSETS / 'videos' / dest.name
            if sha(source) != item['sha256']:
                raise ValueError('Original film differs from its manifest: ' + item['id'])
            shutil.copy2(source, dest)
        if dest.stat().st_size != item['bytes'] or sha(dest) != item['sha256']:
            raise ValueError('Existing original backup differs: ' + str(dest))
    if not saved.exists():
        saved.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', 'utf-8')
    return manifest


def last_keyframe_before(file, second):
    frames = json.loads(run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-skip_frame', 'nokey',
                             '-show_frames', '-show_entries', 'frame=best_effort_timestamp_time', '-of', 'json', file]))['frames']
    keys = [float(f['best_effort_timestamp_time']) for f in frames]
    return max(k for k in keys if k <= second)


def frame_at(file, second, dest):
    run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-ss', format(second, '.9f'), '-i', file,
         '-map', '0:v:0', '-frames:v', '1', dest])


def frame_hashes(file, frames):
    text = run(['ffmpeg', '-v', 'error', '-i', file, '-map', '0:v:0', '-frames:v', frames,
                '-f', 'framemd5', '-'])
    return [line.rsplit(',', 1)[1].strip() for line in text.splitlines() if line and not line.startswith('#')]


def verify(source, dest, cut_frame, folder):
    old, current = probe(source), probe(dest)
    video = [s for s in current['streams'] if s['codec_type'] == 'video']
    subtitles = [s for s in current['streams'] if s['codec_type'] == 'subtitle']
    if len(video) != 1 or video[0]['codec_name'] != 'h264' or (video[0]['width'], video[0]['height']) != (1280, 720):
        raise ValueError('Unexpected output video format.')
    if int(video[0]['nb_frames']) != 7200 or not math.isclose(float(video[0]['duration']), 300, abs_tol=.001):
        raise ValueError('Splice changed the five-minute duration or frame count.')
    if Fraction(video[0]['r_frame_rate']) != 24 or len(subtitles) != 5:
        raise ValueError('Frame rate or subtitle track count changed.')
    if any(s['codec_type'] == 'audio' for s in current['streams']):
        raise ValueError('Unexpected audio track.')
    chapters = lambda m: [(c['start_time'], c['end_time'], c.get('tags', {}).get('title')) for c in m['chapters']]
    if chapters(old) != chapters(current) or len(current['chapters']) != 10:
        raise ValueError('Original chapter boundaries changed.')
    original_subs = [s for s in old['streams'] if s['codec_type'] == 'subtitle']
    for i in range(5):
        if original_subs[i].get('tags') != subtitles[i].get('tags'):
            raise ValueError('Subtitle metadata changed.')
        get_vtt = lambda p: run(['ffmpeg', '-v', 'error', '-i', p, '-map', f'0:s:{i}', '-f', 'webvtt', '-'])
        if get_vtt(source) != get_vtt(dest):
            raise ValueError('Subtitle text or timing changed.')
    decoded = json.loads(run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_frames',
                              '-show_entries', 'frame=best_effort_timestamp_time', '-of', 'json', dest]))['frames']
    if len(decoded) != 7200 or any(abs(float(f['best_effort_timestamp_time']) - i / FPS) > .00001 for i, f in enumerate(decoded)):
        raise ValueError('Decoded presentation timestamps are not a continuous 24 fps timeline.')
    original_hashes, actual_hashes = frame_hashes(source, cut_frame), frame_hashes(dest, cut_frame)
    if original_hashes != actual_hashes or len(actual_hashes) != cut_frame:
        raise ValueError('The decoded images in the untouched prefix differ.')
    decoder = cv2.QRCodeDetector()
    scans = []
    for second in (289 + 23 / 24, 290, 295, 299 + 23 / 24):
        still = folder / (dest.stem + '-' + str(round(second, 3)).replace('.', '_') + '.png')
        frame_at(dest, second, still)
        image = cv2.imread(str(still))
        decoded_url = decoder.detectAndDecode(image[CARD_Y:CARD_Y + CARD_HEIGHT, CARD_X:CARD_X + CARD_WIDTH])[0]
        expected = URL if second >= START else ''
        if decoded_url != expected:
            raise ValueError(f'QR presence/payload incorrect at {second}: {decoded_url}')
        scans.append({'second': second, 'decoded': decoded_url, 'still': str(still)})
    return {'status': 'PASS', 'frames': 7200, 'duration': 300, 'fps': '24/1',
            'subtitleTextTimingAndMetadata': 'UNCHANGED', 'chapters': 10,
            'prefixDecodedFramesUnchanged': cut_frame, 'decodedPresentationTimeline': 'PASS',
            'qrChecks': scans, 'bytes': dest.stat().st_size, 'sha256': sha(dest)}


def render(source, output, card, review):
    cut = last_keyframe_before(source, START)
    cut_frame = round(cut * FPS)
    cut = cut_frame / FPS
    if cut < 260 or cut > START:
        raise ValueError('No safe nearby keyframe for a bounded tail-only edit.')
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='line-qr-tail-', dir=review) as temporary:
        work = Path(temporary)
        head, tail, staged = work / 'head.mp4', work / 'tail.mp4', work / 'result.mp4'
        run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', source, '-map', '0:v:0',
             '-frames:v', cut_frame, '-c:v', 'copy', '-an', '-sn', '-dn', '-video_track_timescale', '12288', head])
        graph = f"[0:v]setpts=PTS-STARTPTS[v];[v][1:v]overlay=x={CARD_X}:y={CARD_Y}:enable='gte(t,{START-cut:.9f})':eof_action=repeat:shortest=1[out]"
        run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-ss', f'{cut:.9f}', '-i', source,
             '-loop', '1', '-i', card, '-filter_complex', graph, '-map', '[out]', '-frames:v', 7200 - cut_frame,
             '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-maxrate', '1000k', '-bufsize', '2000k',
             '-threads', '2', '-profile:v', 'high', '-level:v', '3.1', '-pix_fmt', 'yuv420p',
             '-r', '24', '-video_track_timescale', '12288', '-an', '-sn', '-dn', tail])
        # A concat demuxer re-inserts the tail's H.264 parameter sets at its IDR.
        # Filenames are fixed safe names and the list is relative to its directory.
        listing = work / 'segments.ffconcat'
        listing.write_text("ffconcat version 1.0\nfile 'head.mp4'\nfile 'tail.mp4'\n", 'utf-8')
        run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-f', 'concat', '-safe', '1', '-i', listing,
             '-i', source, '-map', '0:v:0', '-map', '1:s', '-map_metadata', '1', '-map_chapters', '1',
             '-c', 'copy', '-movflags', '+faststart', '-video_track_timescale', '12288', staged])
        stills = review / source.stem
        stills.mkdir(exist_ok=True)
        result = verify(source, staged, cut_frame, stills)
        result.update({'tailReencodedFrom': cut, 'tailFrames': 7200 - cut_frame, 'output': str(output)})
        os.replace(staged, output)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--all', action='store_true')
    parser.add_argument('--tour', choices=IDS, default='interposer')
    parser.add_argument('--apply', action='store_true', help='Install only after media validation; requires --all.')
    parser.add_argument('--font', type=Path, help='A CJK font for the official account name.')
    parser.add_argument('--backup', type=Path, default=ROOT.parent / 'MacGyver_Packaging_Tour_Pre_LINE_QR_Backup')
    parser.add_argument('--review', type=Path, default=ROOT.parent / 'MacGyver_Packaging_Tour_Experiment/line-qr-review')
    args = parser.parse_args()
    if args.apply and not args.all:
        parser.error('--apply requires --all, so the public manifest always describes all six movies.')
    for name in ('ffmpeg', 'ffprobe'):
        if not shutil.which(name):
            raise ValueError(name + ' is required.')
    existing = json.loads((ASSETS / 'videos/manifest.json').read_text('utf-8'))
    end_card = existing.get('endCard', {})
    if end_card.get('verified') is True and end_card.get('url') == URL:
        for entry in existing['videos']:
            file = ASSETS / 'videos' / (entry['id'] + '.mp4')
            if file.stat().st_size != entry['bytes'] or sha(file) != entry['sha256']:
                raise ValueError('A verified QR video no longer matches its manifest: ' + entry['id'])
        print(json.dumps({'status': 'ALREADY_VERIFIED', 'action': 'No second QR card added.', 'url': URL}))
        return
    backup, review = args.backup.resolve(), args.review.resolve()
    if backup.is_relative_to(ASSETS.resolve()) or review.is_relative_to(ASSETS.resolve()):
        raise ValueError('Original backups and staging must stay outside public assets.')
    review.mkdir(parents=True, exist_ok=True)
    manifest = backup_originals(backup)
    card, qr = make_card(args.font)
    verified = {}
    for name in ('LINE_QR_VALIDATION_PREVIEW.json', 'LINE_QR_VALIDATION_ALL.json'):
        prior = review / name
        if not prior.is_file():
            continue
        data = json.loads(prior.read_text('utf-8'))
        if data.get('status') == 'PASS' and data.get('backup') == str(backup) and data.get('qr') == qr:
            for result in data.get('videos', []):
                cached = Path(result.get('output', ''))
                if result.get('status') == 'PASS' and cached.is_file() and sha(cached) == result.get('sha256'):
                    verified[result['id']] = result
    results = []
    for identity in IDS if args.all else (args.tour,):
        print('Rendering and checking ' + identity, flush=True)
        target = review / (identity + '.line-qr.mp4')
        item = verified.get(identity)
        if item is None:
            item = render(backup / (identity + '.mp4'), target, card, review)
        else:
            print('Reusing the unchanged, fully verified preview for ' + identity, flush=True)
        item['id'] = identity
        results.append(item)
        print(json.dumps(item, ensure_ascii=False), flush=True)
    report = {'status': 'PASS', 'officialLineUrl': URL, 'qr': qr, 'backup': str(backup), 'applied': bool(args.apply), 'videos': results}
    if args.apply:
        for result in results:
            source = Path(result['output'])
            target = ASSETS / 'videos' / (result['id'] + '.mp4')
            temporary = target.with_suffix('.mp4.line-qr-tmp')
            shutil.copy2(source, temporary)
            os.replace(temporary, target)
        by_id = {r['id']: r for r in results}
        updated = json.loads(json.dumps(manifest))
        for entry in updated['videos']:
            entry.update({k: by_id[entry['id']][k] for k in ('bytes', 'sha256')})
        updated['version'] = '33.0.2'
        updated['date'] = '2026-11-24'
        updated['endCard'] = {**qr, 'startSeconds': 290, 'endSeconds': 300, 'verified': True,
                              'verification': 'Decoded the exact URL from each final MP4 at 290, 295 and 299.958 seconds; absent at 289.958 seconds.'}
        updated['encoding'] = 'Original H.264 prefix stream-copied; final GOPs re-encoded for a 290–300s LINE QR card.'
        (ASSETS / 'videos/manifest.json').write_text(json.dumps(updated, ensure_ascii=False, indent=2) + '\n', 'utf-8')
    (review / ('LINE_QR_VALIDATION_ALL.json' if args.all else 'LINE_QR_VALIDATION_PREVIEW.json')).write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', 'utf-8')


if __name__ == '__main__':
    main()
