"""Lossless, bounded curriculum restoration without Node or third-party packages."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from portable.curriculum_parts import ensure_featured, PART_LIMIT


class CurriculumPartsTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.public = Path(self.tmp.name)
        self.parts = self.public / "data/course-parts"
        self.parts.mkdir(parents=True)
        self.target = self.public / "data/featured.json"
        # Python json.dumps would alter these numeric spellings. Restore bytes.
        self.raw = [b'[{"id":"a001","stages":[],"small":1e-7,"large":1e+21}]\n',
                    '[{"id":"a002","stages":[],"title":"電機"}]\n'.encode()]
        self.manifest = {"schemaVersion":1, "dataSet":"featured", "courseCount":2, "parts":[]}
        for index, raw in enumerate(self.raw, 1):
            digest = hashlib.sha256(raw).hexdigest()
            name = f"part-{index:04d}-{digest[:16]}.json"
            (self.parts / name).write_bytes(raw)
            self.manifest["parts"].append({"file":name, "sha256":digest, "byteLength":len(raw),
                                          "courseCount":1, "courseIds":[f"a{index:03d}"]})
        self.write_manifest()

    def tearDown(self):
        self.tmp.cleanup()

    def write_manifest(self):
        (self.parts / "index.json").write_text(json.dumps(self.manifest), encoding="utf-8")

    def assert_clean_failure(self, error=ValueError):
        with self.assertRaises(error):
            ensure_featured(self.public)
        self.assertFalse(self.target.exists())
        self.assertEqual(list(self.target.parent.glob(".featured-*.tmp")), [])

    def test_no_node_lossless_restore_and_existing_file_preserved(self):
        root = Path(__file__).resolve().parents[1]
        env = {**os.environ, "PATH":"", "PYTHONPATH":str(root)}
        subprocess.run([sys.executable, "-c", "from portable.curriculum_parts import ensure_featured; import sys; ensure_featured(sys.argv[1])", str(self.public)], env=env, cwd=self.public, check=True)
        expected = b"[" + b",".join(raw.strip()[1:-1] for raw in self.raw) + b"]\n"
        self.assertEqual(self.target.read_bytes(), expected)
        self.target.write_bytes(b"existing authored content\n")
        ensure_featured(self.public)
        self.assertEqual(self.target.read_bytes(), b"existing authored content\n")

    def test_corrupted_part_rejected_without_partial_output(self):
        name = self.manifest["parts"][1]["file"]
        (self.parts / name).write_bytes(self.raw[1].replace(b"a002", b"b002"))
        self.assert_clean_failure()

    def test_invalid_manifest_constraints_rejected(self):
        original = json.loads(json.dumps(self.manifest))
        cases = [
            lambda m: m["parts"][0].update(file="../escape.json"),
            lambda m: m["parts"][0].update(byteLength=PART_LIMIT+1),
            lambda m: m["parts"][0].update(byteLength=True),
            lambda m: m["parts"][1].update(courseIds=["a001"]),
            lambda m: m["parts"][0].update(courseIds=["wrong-id"]),
            lambda m: m.update(courseCount=3),
            lambda m: m["parts"].reverse(),
        ]
        for change in cases:
            self.manifest = json.loads(json.dumps(original))
            change(self.manifest)
            self.write_manifest()
            self.assert_clean_failure()

    def test_missing_part_rejected_without_partial_output(self):
        (self.parts / self.manifest["parts"][1]["file"]).unlink()
        self.assert_clean_failure(OSError)

    def test_failed_atomic_replace_cleans_temporary_file(self):
        with patch("portable.curriculum_parts.os.replace", side_effect=OSError("simulated replacement failure")):
            self.assert_clean_failure(OSError)


if __name__ == "__main__":
    unittest.main()
