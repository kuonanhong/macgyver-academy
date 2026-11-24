#!/usr/bin/env python3
"""Verify mismatched timelines, output coverage, and source preservation offline."""
import hashlib
import importlib.util
from pathlib import Path
import re
import sys
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location("bilingual", Path(__file__).with_name("export-bilingual-packaging-subtitles-v33.py"))
M = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = M
SPEC.loader.exec_module(M)


class BilingualTests(unittest.TestCase):
    def test_different_counts_and_crossing_boundaries_match_time_not_index(self):
        local = [M.Cue(0, 7000, "甲"), M.Cue(7000, 20000, "乙")]
        english = [M.Cue(0, 3000, "A"), M.Cue(3000, 11000, "B"), M.Cue(11000, 20000, "C")]
        result = M.align_tracks(local, english, 20000)
        self.assertEqual(result, [M.Cue(0, 3000, "甲\nA"), M.Cue(3000, 7000, "甲\nB"),
                                  M.Cue(7000, 11000, "乙\nB"), M.Cue(11000, 20000, "乙\nC")])

    def test_gap_and_overlap_are_rejected_instead_of_filled_or_dropped(self):
        for second_start in (999, 1001):
            with self.subTest(second_start=second_start), self.assertRaises(ValueError):
                M.align_tracks([M.Cue(0, 1000, "a"), M.Cue(second_start, 2000, "b")],
                               [M.Cue(0, 2000, "English")], 2000)

    def test_real_six_tours_five_languages_cover_full_duration_and_keep_all_text(self):
        source = M.ASSETS / "subtitles"
        before = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in source.glob("*.vtt")}
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            report = M.export(source, directory / "vtt", directory / "srt")
            self.assertEqual((report["vttFiles"], report["srtFiles"]), (30, 30))
            for record in report["tracks"]:
                tour, language = record["tour"], record["language"]
                originals = M.parse_vtt((source / f"{tour}.{language}.vtt").read_text())
                english = M.parse_vtt((source / f"{tour}.en.vtt").read_text())
                vtt = (directory / "vtt" / f"{tour}.{language}.vtt").read_text()
                # Parse output independently; the source parser intentionally flattens lines.
                blocks = vtt.strip().split("\n\n")[1:]
                previous = 0
                for block in blocks:
                    lines = block.splitlines()
                    start, end = [M.parse_time(s.strip()) for s in lines[1].split("-->")]
                    self.assertEqual(start, previous)
                    self.assertGreater(end, start)
                    previous = end
                    local = next(c for c in originals if c.start <= start and end <= c.end)
                    self.assertEqual(lines[2], local.text)
                    self.assertEqual(len(lines[2:]), 1 if language == "en" else 2)
                    if language != "en":
                        active = next(c for c in english if c.start <= start and end <= c.end)
                        self.assertEqual(lines[3], active.text)
                self.assertEqual(previous, 300000)
                if language == "en":
                    self.assertEqual(len(blocks), len(originals))
                srt = (directory / "srt" / f"{tour}.{language}.srt").read_text()
                normalized_srt = re.sub(r"(\d{2}:\d{2}:\d{2}),(\d{3})", r"\1.\2", srt)
                self.assertEqual(vtt, "WEBVTT\n\n" + normalized_srt)
            self.assertTrue(report["originalSubtitlesUnchanged"])
        after = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in source.glob("*.vtt")}
        self.assertEqual(before, after)

    def test_input_directory_cannot_be_used_as_output(self):
        with self.assertRaises(ValueError):
            M.export(M.ASSETS / "subtitles", M.ASSETS / "subtitles", M.DELIVERY / "unused")


if __name__ == "__main__":
    unittest.main(verbosity=2)
