"""Restore generated featured.json from bounded Git-friendly course parts.

Only the Python standard library is needed. Validated array interiors retain
their exact UTF-8 bytes, including JavaScript's numeric serialization.
"""
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile

PART_LIMIT = 7 * 1024 * 1024
TOTAL_LIMIT = 256 * 1024 * 1024
MANIFEST_LIMIT = 1024 * 1024
COURSE_ID = re.compile(r"[a-z0-9]+(?:[-_][a-z0-9]+)*")


def _integer(value, minimum, maximum):
    return type(value) is int and minimum <= value <= maximum


def _read(path, limit):
    with path.open("rb") as stream:
        raw = stream.read(limit + 1)
    if len(raw) > limit:
        raise ValueError("Curriculum file exceeds its size limit: " + path.name)
    return raw


def _json(raw):
    def invalid_constant(value):
        raise ValueError("Non-JSON numeric constant: " + value)
    return json.loads(raw.decode("utf-8"), parse_constant=invalid_constant)


def ensure_featured(publicroot):
    """Return featured.json, atomically reconstructing it only when absent."""
    public = Path(publicroot).resolve()
    target = public / "data" / "featured.json"
    if target.is_file():
        return target
    if target.exists():
        raise ValueError("featured.json must be a regular file")
    directory = (public / "data" / "course-parts").resolve()
    manifest = _json(_read(directory / "index.json", MANIFEST_LIMIT))
    if (not isinstance(manifest, dict) or not _integer(manifest.get("schemaVersion"), 1, 1)
            or manifest.get("dataSet") != "featured"
            or not _integer(manifest.get("courseCount"), 1, 20000)
            or not isinstance(manifest.get("parts"), list)
            or not 1 <= len(manifest["parts"]) <= 1024):
        raise ValueError("Invalid curriculum manifest")
    seen, interiors, total, count = set(), [], 0, 0
    for index, part in enumerate(manifest["parts"], 1):
        if not isinstance(part, dict):
            raise ValueError("Invalid curriculum part descriptor")
        name, digest = part.get("file"), part.get("sha256")
        size, number, ids = part.get("byteLength"), part.get("courseCount"), part.get("courseIds")
        if (not isinstance(name, str) or not isinstance(digest, str)
                or not re.fullmatch(r"[a-f0-9]{64}", digest)
                or name != f"part-{index:04d}-{digest[:16]}.json"
                or not _integer(size, 2, PART_LIMIT)
                or not _integer(number, 1, 20000)
                or not isinstance(ids, list) or len(ids) != number):
            raise ValueError("Invalid curriculum part descriptor")
        for course_id in ids:
            if (not isinstance(course_id, str) or len(course_id) > 120
                    or not COURSE_ID.fullmatch(course_id) or course_id in seen):
                raise ValueError("Invalid or duplicate curriculum course ID")
            seen.add(course_id)
        total += size
        count += number
        if total >= TOTAL_LIMIT or count > manifest["courseCount"]:
            raise ValueError("Curriculum totals exceed their bounds")
        file = (directory / name).resolve()
        if file.parent != directory:
            raise ValueError("Curriculum part escapes its directory")
        raw = _read(file, PART_LIMIT)
        if len(raw) != size or hashlib.sha256(raw).hexdigest() != digest:
            raise ValueError("Curriculum part byte length or checksum mismatch: " + name)
        courses = _json(raw)
        if (not isinstance(courses, list) or len(courses) != number
                or any(not isinstance(c, dict) or c.get("id") != ids[i]
                       or not isinstance(c.get("stages"), list)
                       for i, c in enumerate(courses))):
            raise ValueError("Curriculum part contents do not match the manifest")
        array = raw.strip(b" \t\r\n")
        if not array.startswith(b"[") or not array.endswith(b"]"):
            raise ValueError("Curriculum part is not a JSON array")
        interiors.append(array[1:-1])
    if count != manifest["courseCount"]:
        raise ValueError("Curriculum course count mismatch")
    payload = b"[" + b",".join(interiors) + b"]\n"
    if len(payload) >= TOTAL_LIMIT:
        raise ValueError("Restored curriculum exceeds its size limit")
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="wb", dir=target.parent,
                                         prefix=".featured-", suffix=".tmp", delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, target)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    return target
