#!/usr/bin/env python3
"""Require all 1000 independent numerical reviews and 100 metadata reviews to match current author inputs."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
AUTHOR = ROOT / 'tools/underground-v14'
read = lambda p: json.loads(p.read_text('utf-8'))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    models = set()
    def add(course, unit):
        key = (course, unit)
        assert key not in models, ('Duplicate reviewed model', key)
        assert 1 <= unit <= 10
        models.add(key)

    a = read(AUTHOR / 'audit_landmarks_support_peer.json')
    assert not a['errors'] and len(a['checks']) == 250
    for cid, digest in a['inputSha256'].items():
        assert sha(AUTHOR / 'inputs' / f'{cid}.json') == digest, ('Stale landmark review', cid)
    for row in a['checks']:
        assert row['numericResult'] == 'pass'
        add(row['courseId'], row['unit'])

    a = read(AUTHOR / 'audit_investigation_ai.json')
    assert a['reviewStatus'] == 'PASS' and a['arithmeticFail'] == 0 and a['openBoundaryFindings'] == 0
    assert len(a['checks']) == 250 and not a['pendingCourses']
    for row in a['checks']:
        cid = row['courseId']
        assert sha(AUTHOR / 'inputs' / f'{cid}.json') == row['inputSha256'], ('Stale investigation review', cid)
        add(cid, row['unit'])

    a = read(AUTHOR / 'review_support_by_ground.json')
    assert a['findingSummary']['open'] == 0 and a['findingSummary']['arithmeticErrors'] == 0 and len(a['checks']) == 250
    for name, digest in a['inputSha256'].items():
        assert sha(AUTHOR / 'inputs' / name) == digest, ('Stale support review', name)
    for row in a['checks']:
        assert row['result'] == 'pass'
        add(row['course'], row['unit'])

    a = read(ROOT / 'docs/CROSS_REVIEW_GROUND_V14.json')
    assert a['arithmeticPassed'] and not a['pendingCourses'] and len(a['calculations']) == 250
    for row in a['calculations']:
        cid = row['course']
        course = read(AUTHOR / 'inputs' / f'{cid}.json')
        assert row['model'] == course['units'][row['unit'] - 1]['model'], ('Stale ground model review', cid, row['unit'])
        add(cid, row['unit'])

    targets = {row['id'] for row in read(AUTHOR / 'targets.json')}
    assert models == {(cid, unit) for cid in targets for unit in range(1, 11)}
    a = read(AUTHOR / 'audit_metadata.json')
    assert a['manualReviewed'] == 100 and a['openFindingCount'] == 0 and not a['automatedErrors']
    assert {row['id'] for row in a['rows']} == targets
    for row in a['rows']:
        assert sha(AUTHOR / 'inputs' / f"{row['id']}.json") == row['sha256'], ('Stale metadata review', row['id'])
    print(json.dumps({'status': 'PASS', 'independentlyReviewedModels': len(models), 'metadataCourses': 100, 'scope': 'Checks reviewed input snapshots and reported dispositions; the four independent arithmetic reports contain the actual calculations. No field-design certification.'}))


if __name__ == '__main__':
    main()
