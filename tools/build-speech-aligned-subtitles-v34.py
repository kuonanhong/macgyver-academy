#!/usr/bin/env python3
"""Bind bilingual captions to measured native-language speech with semantic maps.

The English translation follows the meaning of each native-language sentence,
not the independent timing of the English voice. Display cues extend through
pauses, while original speechStart/speechEnd remain available in the report.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('bilingual_v33', Path(__file__).with_name('export-bilingual-packaging-subtitles-v33.py'))
BASE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = BASE
SPEC.loader.exec_module(BASE)

# Reviewed chapter-local semantic exceptions, using one-based English sentence
# references. Equal-count chapters retain their existing parallel sentence order.
# A string is a closer translation when one English sentence spans two native
# sentences. No narration text or original English subtitle is rewritten.
EXCEPTIONS = {
    ('interposer', 1, 'zh-TW'): [[1], [2, 3]],
    ('interposer', 2, 'ko'): [[1], [2], 'This tour represents silicon-interposer 2.5D packaging.',
                             'CoWoS variants can use different interconnect structures; they are not all the same silicon plate.'],
    ('interposer', 3, 'zh-TW'): [[1], [2], [3, 4]],
    ('interposer', 6, 'zh-TW'): [[1], [2], [3, 4]],
    ('interposer', 7, 'zh-TW'): [[1], [2], [3, 4]],
    ('interposer', 8, 'ko'): [[1], 'A clean X-ray image does not prove every signal works.',
                             'An electrical pass does not prove lifetime reliability.', [3]],
    ('fanout', 1, 'zh-TW'): [[1, 2], [3], [4]],
    ('fanout', 1, 'ja'): [[1, 2], [3], [4]],
    ('fanout', 1, 'ko'): [[1, 2], [3], [4]],
    ('fanout', 3, 'ko'): [[1], 'RDL is constrained routing, not arbitrary drawing.',
                         'Width, spacing, return paths and insulation all matter.', [3]],
    ('fanout', 4, 'zh-TW'): [[1], [2], [3, 4]],
    ('fanout', 4, 'ja'): [[1], [2], [3, 4]],
    ('fanout', 4, 'ko'): [[1], [2], [3, 4]],
    ('fanout', 5, 'zh-TW'): [[1, 2], [3], [4]],
    ('fanout', 6, 'zh-TW'): [[1], [2], [3, 4]],
    ('fanout', 6, 'ja'): [[1], [2], [3, 4]],
    ('fanout', 7, 'zh-TW'): [[1], [2], [3, 4]],
    ('fanout', 8, 'zh-TW'): [[1, 2], [3], [4]],
    ('fanout', 8, 'ja'): [[1, 2], [3], [4]],
    ('fanout', 8, 'ko'): [[1, 2], [3], [4]],
    ('fanout', 9, 'zh-TW'): [[1], [2, 3]],
    ('hybrid', 1, 'zh-TW'): [[1], [2, 3], [4]],
    ('hybrid', 1, 'ja'): ['Begin overhead, then tilt.',
                         'Functions can be stacked rather than placed side by side, shortening selected die-to-die routes.',
                         [2, 3], [4]],
    ('hybrid', 1, 'ko'): ['Begin overhead, then tilt.',
                         'Functions can be stacked rather than placed side by side, shortening selected die-to-die routes.',
                         [2, 3], [4]],
    ('hybrid', 2, 'zh-TW'): [[1, 4], [2], [3]],
    ('hybrid', 2, 'ja'): [[1, 2], [3], [4]],
    ('hybrid', 2, 'ko'): [[1, 2], [3], [4]],
    ('hybrid', 3, 'zh-TW'): [[1, 2], [3, 4]],
    ('hybrid', 6, 'zh-TW'): [[1], [2, 3], [4]],
    ('hybrid', 6, 'ja'): [[1], [2], [3, 4]],
    ('hybrid', 7, 'zh-TW'): [[1], [2], [3, 4]],
    ('hybrid', 10, 'zh-TW'): [[1], [2, 3]],
    ('bridge', 4, 'zh-TW'): [[1, 2], [3], [4]],
    ('bridge', 4, 'ja'): [[1], [2, 3],
                         'This sequence explains assembly relationships, not a particular machine recipe.',
                         'Actual work follows qualified process documentation.'],
    ('bridge', 6, 'zh-TW'): [[1, 2], [3], [4]],
    ('bridge', 7, 'zh-TW'): [[1], [2], [3, 4]],
    ('bridge', 10, 'ja'): [[1],
                         'Reserve precision for critical crossings instead of making every part of the package equally complex.',
                         'That restraint is the visual beauty of this approach.'],
    ('chiplet', 5, 'zh-TW'): [[1], [2], [3, 4]],
    ('chiplet', 5, 'ja'): [[1], [2], [3, 4]],
    ('chiplet', 5, 'ko'): [[1], [2], [3, 4]],
    ('chiplet', 6, 'zh-TW'): ['Follow data between functional districts. Every boundary crossing requires interface work.',
                             'Excessive partitioning can add communication and synchronization overhead.', [3]],
    ('chiplet', 6, 'ja'): ['Follow data between functional districts. Every boundary crossing requires interface work.',
                          'Excessive partitioning can add communication and synchronization overhead.', [3]],
    ('chiplet', 6, 'ko'): ['Follow data between functional districts. Every boundary crossing requires interface work.',
                          'Excessive partitioning can add communication and synchronization overhead.', [3]],
    ('chiplet', 7, 'zh-TW'): [[1, 2], [3], [4]],
    ('thermal', 3, 'zh-TW'): [[1], [2], [3, 4]],
    ('thermal', 3, 'ko'): [[1], [2], [3, 4]],
    ('thermal', 8, 'zh-TW'): [[1], [2], [3, 4]],
}


def text_hash(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def create_semantic_mapping():
    mapping = {'schemaVersion': 1, 'basis': 'Existing parallel translations, reviewed chapter-local sentence splits/merges',
               'timingPolicy': 'Each language follows its own measured speech; English second line is a semantic translation, not English audio timing.',
               'tracks': []}
    for tour in BASE.TOURS:
        tracks = {language: BASE.parse_vtt((BASE.ASSETS / 'subtitles' / f'{tour}.{language}.vtt').read_text('utf-8'))
                  for language in BASE.LANGUAGES}
        for language in BASE.LANGUAGES:
            rows = []
            for chapter in range(1, 11):
                local = [c.text for c in tracks[language] if (chapter - 1) * 30000 <= c.start < chapter * 30000]
                english = [c.text for c in tracks['en'] if (chapter - 1) * 30000 <= c.start < chapter * 30000]
                key_language = 'zh-TW' if language == 'zh-CN' else language
                choices = EXCEPTIONS.get((tour, chapter, key_language))
                if choices is None:
                    if len(local) != len(english):
                        raise ValueError(f'Unreviewed sentence count mismatch: {tour}/{language}/{chapter}')
                    choices = [[i + 1] for i in range(len(local))]
                if len(choices) != len(local):
                    raise ValueError('Semantic mapping no longer matches the source segmentation')
                for index, (source, selection) in enumerate(zip(local, choices), 1):
                    translated = selection if isinstance(selection, str) else ' '.join(english[i - 1] for i in selection)
                    rows.append({'chapter': chapter, 'sentence': index, 'sourceText': source,
                                 'sourceTextSha256': text_hash(source), 'englishText': translated,
                                 'englishSentenceIndices': selection if isinstance(selection, list) else None,
                                 'alignment': 'reviewed-clause-translation' if isinstance(selection, str) else 'parallel-meaning'})
            mapping['tracks'].append({'tourId': tour, 'language': language, 'sentences': rows})
    return mapping


def display_cues(speech_cues, semantic_rows):
    if len(speech_cues) != len(semantic_rows):
        raise ValueError('Measured narration has a different sentence count; update the semantic map explicitly')
    result = []
    # Match text inside each fixed chapter, never independent English cue indices.
    for chapter in range(1, 11):
        mapped = [s for s in semantic_rows if s['chapter'] == chapter]
        measured = [c for c in speech_cues if (chapter - 1) * 30 <= c['start'] < chapter * 30]
        if len(mapped) != len(measured):
            raise ValueError('Measured chapter sentence count mismatch')
        for index, (cue, semantic) in enumerate(zip(measured, mapped)):
            if cue['text'].strip() != semantic['sourceText']:
                raise ValueError('Narration sentence differs from its reviewed semantic mapping')
            start = (chapter - 1) * 30000 if index == 0 else round(cue['start'] * 1000)
            end = round(measured[index + 1]['start'] * 1000) if index + 1 < len(measured) else chapter * 30000
            if not (0 <= cue['start'] < cue['end'] <= chapter * 30 + .001) or cue['end'] * 1000 > end + 1:
                raise ValueError('Overlapping or out-of-chapter measured speech')
            result.append({'displayStart': start / 1000, 'displayEnd': end / 1000,
                           'speechStart': cue['start'], 'speechEnd': cue['end'],
                           'text': semantic['sourceText'], 'englishText': semantic['englishText'],
                           'chapter': chapter, 'sentence': index + 1})
    return result


def build(manifest_path, output, allow_partial=False, semantic_mapping=None, file_suffix='V34'):
    manifest = json.loads(manifest_path.read_text('utf-8'))
    if manifest.get('status') != 'PASS' and not (allow_partial and manifest.get('status') == 'PARTIAL'):
        raise ValueError('Final measured narration manifest required')
    semantic = semantic_mapping or create_semantic_mapping()
    maps = {(t['tourId'], t['language']): t['sentences'] for t in semantic['tracks']}
    tracks = {(t['tourId'], t['language']): t for t in manifest['tracks']}
    if not tracks or not set(tracks).issubset(maps) or (not allow_partial and set(tracks) != set(maps)):
        raise ValueError('Expected all six tours in five languages')
    pending, records = [], []
    for key, rows in maps.items():
        if key not in tracks:
            continue
        tour, language = key
        measured = tracks[key]['cues']
        display = display_cues(measured, rows)
        cues = [BASE.Cue(round(c['displayStart'] * 1000), round(c['displayEnd'] * 1000),
                         c['text'] if language == 'en' else c['text'] + '\n' + c['englishText']) for c in display]
        BASE.validate_coverage(cues, 300000)
        record = {'tourId': tour, 'language': language, 'durationSeconds': 300, 'cues': display, 'files': {}}
        for suffix in ('vtt', 'srt'):
            file = output / f'{tour}.{language}.{suffix}'
            raw = BASE.render(cues, suffix).encode('utf-8')
            pending.append((file, raw))
            record['files'][suffix] = {'file': str(file.resolve()), 'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)}
        records.append(record)
    output.mkdir(parents=True, exist_ok=True)
    for file, raw in pending:
        file.write_bytes(raw)
    (output / f'SEMANTIC_MAPPING_{file_suffix}.json').write_text(json.dumps(semantic, ensure_ascii=False, indent=2) + '\n', 'utf-8')
    result = {'schemaVersion': 1, 'status': 'PASS' if len(records) == len(maps) else 'PARTIAL', 'durationSeconds': 300, 'tracks': records,
              'sourceNarrationManifestSha256': hashlib.sha256(manifest_path.read_bytes()).hexdigest(),
              'displayPolicy': 'First sentence begins at chapter start; each displayEnd is next speechStart or chapter end. Original speechStart/speechEnd are retained.',
              'alignmentPolicy': semantic['timingPolicy']}
    (output / f'BILINGUAL_SUBTITLE_MANIFEST_{file_suffix}.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', 'utf-8')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--audio-manifest', type=Path, default=ROOT.parent / 'delivery/narration-v34/AUDIO_MANIFEST_V34.json')
    parser.add_argument('--output', type=Path, default=ROOT.parent / 'delivery/narrated-v33/subtitles-bilingual')
    parser.add_argument('--mapping-only', action='store_true')
    parser.add_argument('--allow-partial', action='store_true', help='Export only completed measured tracks; report remains PARTIAL until all 30 are present.')
    parser.add_argument('--public-js', type=Path, default=ROOT / 'public/academy/packaging-captions-v33.js')
    args = parser.parse_args()
    if args.mapping_only:
        result = create_semantic_mapping()
        args.output.mkdir(parents=True, exist_ok=True)
        (args.output / 'SEMANTIC_MAPPING_V34.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', 'utf-8')
    else:
        result = build(args.audio_manifest, args.output, args.allow_partial)
        browser = {'version': '33.0.3', 'status': result['status'], 'duration': 300,
                   'trackCount': len(result['tracks']), 'expectedTrackCount': 30,
                   'alignment': 'measured native speech with semantically corresponding English', 'tours': {}}
        for track in result['tracks']:
            browser['tours'].setdefault(track['tourId'], {})[track['language']] = [
                {'start': cue['displayStart'], 'end': cue['displayEnd'], 'text': cue['text'],
                 'english': '' if track['language'] == 'en' else cue['englishText'],
                 'speechStart': cue['speechStart'], 'speechEnd': cue['speechEnd'],
                 'chapter': cue['chapter'], 'sentence': cue['sentence']} for cue in track['cues']]
        args.public_js.parent.mkdir(parents=True, exist_ok=True)
        staged = args.public_js.with_suffix(args.public_js.suffix + '.tmp')
        staged.write_text('// Generated from measured narration and reviewed sentence meanings.\n'
                          + 'window.MACGYVER_PACKAGING_CAPTIONS=' + json.dumps(browser, ensure_ascii=False, separators=(',', ':')) + ';\n', 'utf-8')
        staged.replace(args.public_js)
    print(json.dumps({'status': result.get('status', 'MAPPING_READY'), 'tracks': len(result['tracks']), 'output': str(args.output.resolve())}))


if __name__ == '__main__':
    main()
