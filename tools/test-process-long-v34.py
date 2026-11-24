#!/usr/bin/env python3
"""Offline long-film contract tests; no media rewrite, network or OAuth."""
import copy
import importlib.util
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('long_builder_test', Path(__file__).with_name('build-process-long-v34.py'))
LONG = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = LONG
spec.loader.exec_module(LONG)


def sample():
    script = {'id': 'C01-long', 'durationSeconds': 900, 'languages': list(LONG.LANGUAGES),
              'title': {lang: 'C01 requirements' for lang in LONG.LANGUAGES}, 'sources': [], 'cues': []}
    cues, rows = [], []
    for chapter in range(30):
        script['cues'].append({'start': chapter * 30, 'end': (chapter + 1) * 30,
                              'title': {lang: f'Chapter {chapter + 1}' for lang in LONG.LANGUAGES},
                              'text': {lang: 'First. Second.' for lang in LONG.LANGUAGES}})
        for sentence, (text, offset, end) in enumerate([('First.', .35, 4.125), ('Second.', 9.7, 20.125)]):
            cue = {'chapterIndex': chapter, 'sentenceIndex': sentence,
                   'start': chapter * 30 + offset, 'end': chapter * 30 + end, 'text': text}
            cues.append(cue)
            rows.append({'chapter': chapter + 1, 'sentence': sentence + 1, 'sourceText': text,
                         'sourceTextSha256': LONG.text_sha(text), 'englishText': text,
                         'speechStart': cue['start'], 'speechEnd': cue['end']})
    return script, cues, rows


class LongContractTests(unittest.TestCase):
    def test_900_second_coverage_retains_real_gaps_and_chapter_boundaries(self):
        script, cues, rows = sample()
        display, rendered = LONG.display_track(cues, rows, script['cues'], 'zh-TW')
        self.assertEqual((display[0]['start'], display[-1]['end']), (0, 900))
        self.assertEqual(display[0]['speechStart'], .35)
        self.assertEqual(display[0]['speechEnd'], 4.125)
        self.assertEqual(display[0]['end'], 9.7)
        self.assertEqual(display[1]['end'], 30)
        self.assertEqual(display[2]['start'], 30)
        self.assertIn('00:15:00.000', LONG.BASE.render(rendered, 'vtt'))
        self.assertEqual(rendered[0].text, 'First.\nFirst.')

    def test_semantic_text_mismatch_refuses_even_when_count_is_identical(self):
        script, cues, rows = sample()
        rows[0]['sourceText'], rows[1]['sourceText'] = rows[1]['sourceText'], rows[0]['sourceText']
        with self.assertRaisesRegex(ValueError, 'spoken sentence'):
            LONG.display_track(cues, rows, script['cues'], 'ja')

    def test_wrong_recording_time_duplicate_or_omitted_sentence_rejected(self):
        script, cues, rows = sample()
        for mutation in ('timing', 'duplicate', 'missing'):
            changed = copy.deepcopy(rows)
            if mutation == 'timing':
                changed[0]['speechEnd'] += .001
            elif mutation == 'duplicate':
                changed[1]['sentence'] = 1
            else:
                changed.pop()
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                LONG.display_track(cues, changed, script['cues'], 'ko')

    def test_english_is_single_line_and_unrelated_source_text_rejected(self):
        script, cues, rows = sample()
        display, rendered = LONG.display_track(cues, rows, script['cues'], 'en')
        self.assertEqual(display[0]['english'], '')
        self.assertEqual(rendered[0].text, 'First.')
        script['cues'][0]['text']['en'] = 'A completely different chapter.'
        with self.assertRaisesRegex(ValueError, 'authored chapter'):
            LONG.display_track(cues, rows, script['cues'], 'en')

    def test_short_film_and_partial_translations_cannot_enter_long_pipeline(self):
        script, _, _ = sample()
        LONG.contract(script)
        for field, value in [('id', 'C01'), ('durationSeconds', 300)]:
            changed = copy.deepcopy(script)
            changed[field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                LONG.contract(changed)
        del script['cues'][29]['text']['ko']
        with self.assertRaisesRegex(ValueError, 'language content'):
            LONG.contract(script)

    def test_thirty_metadata_timecodes_and_utf8_limit(self):
        script, _, _ = sample()
        versions = LONG.metadata_text(script)
        self.assertEqual(set(versions), {'default', *LONG.LANGUAGES})
        for value in versions.values():
            self.assertIn('14:30 Chapter 30', value['description'])
            self.assertEqual(sum(line[:5].replace(':', '').isdigit() for line in value['description'].splitlines()), 30)
            self.assertIn(LONG.JOB.AERO, value['description'])
            self.assertIn(LONG.JOB.LINE, value['description'])
            self.assertNotIn('Resilience', value['description'])
            LONG.JOB.validate_text(**value)
        LONG.JOB.validate_text('界' * 100, '界' * 1666 + 'ab')
        with self.assertRaises(ValueError):
            LONG.JOB.validate_text('title', '界' * 1667)

    def test_mux_verification_rejects_300_second_outputs_or_changed_packets(self):
        chapters = [(i * 30., (i + 1) * 30., f'Chapter {i + 1}') for i in range(30)]
        streams = [{'codec_type': 'video', 'codec_name': 'h264', 'nb_frames': '21600', 'r_frame_rate': '24/1',
                    'width': 1280, 'height': 720, 'duration': '900.000'}]
        for kind, codec in [('audio', 'aac'), ('subtitle', 'mov_text')]:
            streams += [{'codec_type': kind, 'codec_name': codec, 'duration': '900.000',
                         'tags': {'language': iso}, 'disposition': {'default': int(i == 0)}}
                        for i, (_, iso, _) in enumerate(LONG.MUX.LANGUAGES)]
        probe = {'streams': streams, 'format': {'duration': '900.000'},
                 'chapters': [{'start_time': a, 'end_time': b, 'tags': {'title': title}} for a, b, title in chapters]}
        packets = lambda file, selector: ['packet'] * 21600 if selector == 'v:0' else ['audio']
        with patch.object(LONG.MUX, 'probe', return_value=probe), patch.object(LONG.MUX, 'packets', side_effect=packets), \
                patch.object(LONG.MUX, 'subtitles', return_value=['exact caption']), \
                patch.object(LONG, 'qr_verify', return_value={'status': 'PASS'}):
            self.assertEqual(LONG.verify('master', 'final', [1]*5, [2]*5, chapters, {})['status'], 'PASS')
            probe['streams'][0]['duration'] = '300.000'
            with self.assertRaisesRegex(ValueError, '900s'):
                LONG.verify('master', 'final', [1]*5, [2]*5, chapters, {})
            probe['streams'][0]['duration'] = '900.000'
            with patch.object(LONG.MUX, 'packets', side_effect=lambda file, selector: [file] * 21600):
                with self.assertRaisesRegex(ValueError, 'packet'):
                    LONG.verify('master', 'final', [1]*5, [2]*5, chapters, {})

    def test_new_process_cannot_inherit_c01_specific_metadata(self):
        script, _, _ = sample()
        script['id'] = 'C02-long'
        with self.assertRaisesRegex(ValueError, 'own reviewed'):
            LONG.metadata_text(script)


if __name__ == '__main__':
    unittest.main()
