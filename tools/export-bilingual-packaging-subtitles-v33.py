#!/usr/bin/env python3
"""Combine existing timed subtitles using time boundaries, never cue indices.

Non-English tracks contain one source-language line followed by one English
line. English remains a single-language track. A player can wrap these logical
lines to fit its viewport. Source VTT files are read only.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "public/academy/assets/packaging-tour-v33"
DELIVERY = ROOT.parent / "MacGyver_Packaging_Tour_Experiment"
TOURS = ("interposer", "fanout", "hybrid", "bridge", "chiplet", "thermal")
LANGUAGES = ("zh-TW", "en", "ja", "ko", "zh-CN")
STAMP = r"(?:\d{2,}:)?\d{2}:\d{2}\.\d{3}"
TIMING = re.compile(rf"^({STAMP})\s+-->\s+({STAMP})(?:\s+.*)?$")


@dataclass(frozen=True)
class Cue:
    start: int
    end: int
    text: str


def parse_time(value: str) -> int:
    fields = value.split(":")
    if len(fields) == 2:
        fields.insert(0, "0")
    hours, minutes = map(int, fields[:2])
    seconds, milliseconds = map(int, fields[2].split("."))
    if minutes > 59 or seconds > 59:
        raise ValueError(f"Invalid subtitle timestamp: {value}")
    return ((hours * 60 + minutes) * 60 + seconds) * 1000 + milliseconds


def parse_vtt(source: str) -> list[Cue]:
    normalized = source.lstrip("\ufeff").replace("\r\n", "\n").replace("\r", "\n")
    blocks = re.split(r"\n[ \t]*\n", normalized.strip())
    if not blocks or not blocks[0].splitlines()[0].startswith("WEBVTT"):
        raise ValueError("Expected a WEBVTT header")
    cues = []
    for block in blocks[1:]:
        lines = block.splitlines()
        if not lines:
            continue
        if lines[0] == "NOTE" or lines[0].startswith("NOTE "):
            continue
        if lines[0] in ("STYLE", "REGION"):
            raise ValueError("Styled/positioned source subtitles require explicit conversion")
        timing_index = 0 if "-->" in lines[0] else 1
        if timing_index >= len(lines):
            raise ValueError("Subtitle cue is missing its timing line")
        match = TIMING.fullmatch(lines[timing_index])
        if not match:
            raise ValueError("Invalid subtitle timing line")
        # One logical line per language; player-controlled wrapping is retained.
        text = " ".join(line.strip() for line in lines[timing_index + 1:] if line.strip())
        if not text or "-->" in text:
            raise ValueError("Subtitle cue must contain non-empty text")
        cues.append(Cue(parse_time(match[1]), parse_time(match[2]), text))
    return cues


def validate_coverage(cues: list[Cue], duration_ms: int) -> None:
    if not cues:
        raise ValueError("Subtitle track is empty")
    expected = 0
    for cue in cues:
        if cue.start != expected:
            raise ValueError(f"Subtitle gap, overlap or unsorted cue at {expected} ms")
        if cue.end <= cue.start or cue.end > duration_ms:
            raise ValueError("Subtitle cue has an invalid duration")
        expected = cue.end
    if expected != duration_ms:
        raise ValueError(f"Subtitle coverage ends at {expected} ms, expected {duration_ms} ms")


def align_tracks(local: list[Cue], english: list[Cue], duration_ms: int) -> list[Cue]:
    """Split at the union of both timelines and use the active cue on each."""
    validate_coverage(local, duration_ms)
    validate_coverage(english, duration_ms)
    boundaries = sorted({time for cue in local + english for time in (cue.start, cue.end)})
    local_index = english_index = 0
    aligned = []
    for start, end in zip(boundaries, boundaries[1:]):
        while local[local_index].end <= start:
            local_index += 1
        while english[english_index].end <= start:
            english_index += 1
        first, second = local[local_index], english[english_index]
        if not (first.start <= start < end <= first.end
                and second.start <= start < end <= second.end):
            raise ValueError("Source subtitle interval does not cover the aligned cue")
        aligned.append(Cue(start, end, first.text + "\n" + second.text))
    validate_coverage(aligned, duration_ms)
    return aligned


def timestamp(milliseconds: int, separator: str = ".") -> str:
    seconds, ms = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}{separator}{ms:03}"


def render(cues: list[Cue], file_format: str) -> str:
    separator = "," if file_format == "srt" else "."
    header = "WEBVTT\n\n" if file_format == "vtt" else ""
    return header + "\n\n".join(
        f"{index}\n{timestamp(cue.start, separator)} --> {timestamp(cue.end, separator)}\n{cue.text}"
        for index, cue in enumerate(cues, 1)
    ) + "\n"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def export(input_dir: Path, vtt_output: Path, srt_output: Path,
           duration_ms: int = 300000) -> dict:
    input_dir, vtt_output, srt_output = [p.resolve() for p in (input_dir, vtt_output, srt_output)]
    if input_dir in (vtt_output, srt_output):
        raise ValueError("Output directories must differ from the read-only source directory")
    sources = {}
    tracks = {}
    # Validate every input before writing any generated subtitle.
    for tour in TOURS:
        for language in LANGUAGES:
            name = f"{tour}.{language}.vtt"
            raw = (input_dir / name).read_bytes()
            cues = parse_vtt(raw.decode("utf-8-sig"))
            validate_coverage(cues, duration_ms)
            sources[name] = digest(raw)
            tracks[(tour, language)] = cues
    pending = []
    records = []
    for tour in TOURS:
        for language in LANGUAGES:
            local = tracks[(tour, language)]
            english = tracks[(tour, "en")]
            cues = local if language == "en" else align_tracks(local, english, duration_ms)
            validate_coverage(cues, duration_ms)
            record = {"tour": tour, "language": language, "secondLanguage": None if language == "en" else "en",
                      "cueCount": len(cues), "startMs": cues[0].start, "endMs": cues[-1].end,
                      "minimumCueMs": min(c.end - c.start for c in cues), "files": {}}
            for file_format, output in (("vtt", vtt_output), ("srt", srt_output)):
                target = output / f"{tour}.{language}.{file_format}"
                data = render(cues, file_format).encode("utf-8")
                pending.append((target, data))
                record["files"][file_format] = {"path": str(target), "sha256": digest(data), "bytes": len(data)}
            records.append(record)
    for target, data in pending:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    if any(digest((input_dir / name).read_bytes()) != sha for name, sha in sources.items()):
        raise ValueError("A source subtitle changed while generating the outputs")
    return {"schemaVersion": 1, "durationMs": duration_ms, "alignment": "union-of-source-cue-time-boundaries",
            "languageOrder": "source-language-first, English-second; English track is English-only",
            "note": "Two logical text lines may wrap on small screens. Source timing is preserved; neighboring sentence changes can create short union intervals.",
            "originalSubtitlesUnchanged": True, "sourceSha256": sources, "tracks": records,
            "status": "PASS", "vttFiles": len(records), "srtFiles": len(records)}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=ASSETS / "subtitles")
    parser.add_argument("--vtt-output", type=Path, default=ASSETS / "subtitles-bilingual")
    parser.add_argument("--srt-output", type=Path, default=DELIVERY / "subtitles-bilingual")
    parser.add_argument("--report", type=Path, default=DELIVERY / "bilingual-subtitles-report-v33.json")
    args = parser.parse_args()
    result = export(args.input, args.vtt_output, args.srt_output)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "vttFiles": result["vttFiles"],
                      "srtFiles": result["srtFiles"], "durationSeconds": result["durationMs"] / 1000,
                      "report": str(args.report.resolve())}, ensure_ascii=False))


if __name__ == "__main__":
    main()
