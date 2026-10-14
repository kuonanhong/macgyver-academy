#!/usr/bin/env python3
"""Read-only delimiter audit of independently authored V10 curriculum inputs.

This checks a concrete corruption risk: ASCII absolute-value bars inside the
pipe-delimited bilingual source format. It does not claim to verify physics.
"""
import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SPECS = (
    ("build_group_a.py", "add", 5, 3, "~"),
    ("group_b_specs.py", "C", 12, 6, None),
    ("core_c.py", "course", 13, 8, None),
)


def audit():
    errors = []
    counts = {}
    for filename, function, column, expected_width, bilingual in SPECS:
        path = ROOT / filename
        tree = ast.parse(path.read_text("utf-8"), filename=str(path))
        count = 0
        for node in ast.walk(tree):
            if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                    and node.func.id == function):
                continue
            try:
                values = [ast.literal_eval(arg) for arg in node.args]
            except (ValueError, TypeError):
                continue
            if len(values) <= column or not isinstance(values[column], str):
                continue
            course_id = f"a{values[0]}"
            count += 1
            rows = [line.split("|") for line in values[column].strip().splitlines()
                    if line.strip()]
            if len(rows) != 12:
                errors.append(f"{filename}:{node.lineno} {course_id}: {len(rows)} units, expected 12")
            for number, row in enumerate(rows, 1):
                if len(row) != expected_width:
                    errors.append(f"{filename}:{node.lineno} {course_id} unit {number}: "
                                  f"{len(row)} fields, expected {expected_width}")
                if bilingual:
                    for field in row:
                        if len(field.split(bilingual)) != 2:
                            errors.append(f"{filename}:{node.lineno} {course_id} unit {number}: "
                                          "invalid bilingual separator count")
            if function == "course" and len(values[4].split("|")) != 2:
                errors.append(f"{filename}:{node.lineno} {course_id}: formula needs exactly 2 languages")
        counts[filename] = count
    for filename, count in counts.items():
        print(f"{filename}: {count} authored courses")
    if errors:
        raise SystemExit("\n".join(errors))
    print("Bilingual delimiters: PASS (content correctness requires editorial review)")


if __name__ == "__main__":
    audit()
