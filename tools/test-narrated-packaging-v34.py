#!/usr/bin/env python3
"""Offline regression tests for speech/display timing and localized metadata."""
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest


def load(name, file):
    spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(file))
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


S = load('speech_captions', 'build-speech-aligned-subtitles-v34.py')
J = load('narrated_job', 'prepare-narrated-youtube-job-v34.py')


class NarratedTests(unittest.TestCase):
    def setUp(self):
        self.mapping = S.create_semantic_mapping()

    def test_semantic_alignment_handles_merges_and_reordered_meaning(self):
        track = next(t for t in self.mapping['tracks'] if t['tourId'] == 'interposer' and t['language'] == 'zh-TW')
        second = track['sentences'][1]
        self.assertEqual(second['englishSentenceIndices'], [2, 3])
        self.assertIn('city', second['englishText'])
        self.assertIn('who computes', second['englishText'])
        hybrid = next(t for t in self.mapping['tracks'] if t['tourId'] == 'hybrid' and t['language'] == 'zh-TW')
        first = next(s for s in hybrid['sentences'] if s['chapter'] == 2)
        self.assertEqual(first['englishSentenceIndices'], [1, 4])
        self.assertIn('Architecture determines', first['englishText'])
        # Equal sentence counts do not imply equal semantic splits.
        for language in ('ja', 'ko'):
            hybrid = next(t for t in self.mapping['tracks'] if t['tourId'] == 'hybrid' and t['language'] == language)
            self.assertEqual(hybrid['sentences'][0]['englishText'], 'Begin overhead, then tilt.')
            self.assertIn('shortening selected die-to-die', hybrid['sentences'][1]['englishText'])
            self.assertIn('not a stack of circuit boards', hybrid['sentences'][2]['englishText'])
            self.assertIn('carefully controlled interfaces', hybrid['sentences'][2]['englishText'])
        bridge = next(t for t in self.mapping['tracks'] if t['tourId'] == 'bridge' and t['language'] == 'ja')
        assembly = [s for s in bridge['sentences'] if s['chapter'] == 4]
        self.assertIn('tolerances', assembly[1]['englishText'])
        self.assertNotIn('tolerances', assembly[2]['englishText'])
        for language in ('ja', 'ko', 'zh-TW', 'zh-CN'):
            chiplet = next(t for t in self.mapping['tracks'] if t['tourId'] == 'chiplet' and t['language'] == language)
            traffic = [s for s in chiplet['sentences'] if s['chapter'] == 6]
            self.assertIn('interface work', traffic[0]['englishText'])
            self.assertNotIn('interface work', traffic[1]['englishText'])

    def test_every_output_covers_300_seconds_but_keeps_actual_speech_gaps(self):
        tracks = []
        for mapped in self.mapping['tracks']:
            # Explicit test fixture: generated speech windows, not real narration.
            cues = []
            for chapter in range(1, 11):
                sentences = [s for s in mapped['sentences'] if s['chapter'] == chapter]
                for index, sentence in enumerate(sentences):
                    start = (chapter - 1) * 30 + index * 30 / len(sentences) + .35
                    end = (chapter - 1) * 30 + (index + 1) * 30 / len(sentences) - .5
                    cues.append({'start': start, 'end': end, 'text': sentence['sourceText']})
            tracks.append({'tourId': mapped['tourId'], 'language': mapped['language'], 'cues': cues})
        with tempfile.TemporaryDirectory() as temporary:
            folder = Path(temporary)
            manifest = folder / 'fixture.json'
            manifest.write_text(json.dumps({'status': 'PASS', 'tracks': tracks}, ensure_ascii=False))
            result = S.build(manifest, folder / 'captions')
            self.assertEqual(len(result['tracks']), 30)
            for track in result['tracks']:
                self.assertEqual(track['cues'][0]['displayStart'], 0)
                self.assertEqual(track['cues'][0]['speechStart'], .35)
                self.assertEqual(track['cues'][-1]['displayEnd'], 300)
                previous = 0
                for cue in track['cues']:
                    self.assertEqual(cue['displayStart'], previous)
                    self.assertLess(cue['speechEnd'], cue['displayEnd'])
                    previous = cue['displayEnd']
                vtt = Path(track['files']['vtt']['file']).read_text()
                for block in vtt.strip().split('\n\n')[1:]:
                    self.assertEqual(len(block.splitlines()), 3 if track['language'] == 'en' else 4)

    def test_changed_sentence_requires_explicit_remapping(self):
        rows = self.mapping['tracks'][0]['sentences']
        cues = [{'start': (r['chapter'] - 1) * 30 + .35, 'end': r['chapter'] * 30 - .5, 'text': 'changed'} for r in rows]
        with self.assertRaises(ValueError):
            S.display_cues(cues, rows)

    def test_title_uses_characters_description_uses_utf8_bytes(self):
        J.validate_text('封' * 100, '封' * 1666 + 'ab')
        with self.assertRaises(ValueError):
            J.validate_text('封' * 101, 'ok')
        with self.assertRaises(ValueError):
            J.validate_text('ok', '封' * 1667)

    def test_all_localizations_include_ten_chapters_and_required_links(self):
        data = J.read_content()
        for index, tour in enumerate(data['tours'], 1):
            versions = [J.bilingual(tour, index)] + [J.localized(tour, language, index) for language in J.LANGUAGES]
            for version in versions:
                J.validate_text(**version)
                for chapter in tour['chapters']:
                    self.assertIn(J.timecode(chapter['start']) + ' ', version['description'])
                for url in (J.ACADEMY, J.AERO, J.LINE):
                    self.assertIn(url, version['description'])
                self.assertNotIn('resilience', version['description'].lower())


if __name__ == '__main__':
    unittest.main(verbosity=2)
