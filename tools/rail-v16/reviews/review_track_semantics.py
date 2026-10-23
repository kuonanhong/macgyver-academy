#!/usr/bin/env python3
"""Reproduce targeted peer-review regressions without importing author_track."""
from pathlib import Path
import collections
import hashlib
import importlib.util
import json
import math
import statistics

HERE = Path(__file__).resolve().parent
BASE = HERE.parent


def main():
    numeric_path = HERE / 'track_numeric_models.json'
    rows = json.loads(numeric_path.read_text())['models']
    by = {(r['courseId'], r['unit']): r for r in rows}
    courses = {f'b{n}': json.loads((BASE / f'inputs/b{n}.json').read_text()) for n in range(335, 368)}
    spec = importlib.util.spec_from_file_location('track_schema_review', BASE / 'validate_input.py')
    validator = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(validator)
    schema_issues = [x for cid in courses for x in validator.validate(BASE / f'inputs/{cid}.json')]
    checks = []

    def check(label, result, evidence):
        checks.append(dict(check=label, passed=bool(result), evidence=evidence))

    def row(n, i):
        return by[(f'b{n}', i)]

    def lesson(n, i):
        return courses[f'b{n}']['units'][i - 1]

    check('33 course schemas', not schema_issues, schema_issues or '33/33 pass')
    counts = collections.Counter(r['courseId'] for r in rows)
    check('330 models, ten per course', len(rows) == 330 and set(counts) == set(courses) and set(counts.values()) == {10}, dict(counts))
    check('Unit-specific model boundaries', all(len({r['modelBoundary'] for r in rows if r['courseId'] == cid}) == 10 for cid in courses), 'Each course has ten distinct explicit boundaries.')
    check('Measurement chains available', all(r.get('measurementChain') for r in rows), '330 nonempty measurement chains.')
    check('Distinct course architectures', len({json.dumps(d['architectureNodes']) for d in courses.values()}) == 33, '33 distinct named subsystem sets.')
    check('Original assumed inputs clearly identified', all('Original assumed example, not field operating values' in u['model'] for d in courses.values() for u in d['units']), 'All 330 units state that their numeric inputs are classroom assumptions.')
    check('Old generic force-path padding removed', all('Applied forces require a complete path' not in u['mechanism'] and '外力必須經過構件與支承形成閉合傳力路徑' not in u['mechanism'] for d in courses.values() for u in d['units']), 'No known stale universal force-path paragraph.')
    check('Observation independence not asserted automatically', all('as independent evidence' not in u['mechanism'] for d in courses.values() for u in d['units']), 'Template now calls observables measurement evidence; independence remains a separate validation question.')
    check('Mean-strength title matches averaging expression', 'mean strength' in row(338, 10)['title'] and row(338, 10)['expression'] == '(f1+f2+f3)/3', row(338, 10)['title'])
    check('Sieve parameter is valid Python identifier', 'pass' not in row(344, 5)['parameters'], row(344, 5)['expression'])
    check('Prestress bending axis', 'transverse axis' in row(350, 4)['modelBoundary'], row(350, 4)['modelBoundary'])
    check('Finite difference identified as interval stiffness', 'interval' in row(356, 9)['title'] and 'finite difference' in row(356, 9)['modelBoundary'].lower(), row(356, 9)['modelBoundary'])
    check('Annual energy-balance title', 'net heat balance' in row(355, 7)['title'].lower(), row(355, 7)['title'])
    check('Alarm frequency title and units', 'rate' in row(359, 10)['title'] and row(359, 10)['resultUnit'] == 'alarms/h', row(359, 10)['title'])
    check('Recall sensitivity allows changed dataset count', 'total may change' in row(359, 4)['modelBoundary'], row(359, 4)['modelBoundary'])

    discrete = [r for r in rows if r['parameterUnits'][r['sensitivityParameter']] in ('count', 'events', 'bits', 'states')]
    check('Discrete sensitivities preserve integers', all(r['sensitivityValue'].is_integer() and r['sensitivityValue'] == r['parameters'][r['sensitivityParameter']] + 1 for r in discrete), {'models': len(discrete), 'mode': 'plus one whole unit'})
    check('Binary state combinations', all(row(n, i)['result'] == 16 and row(n, i)['sensitivityValue'] == 5 and row(n, i)['sensitivityResult'] == 32 for n, i in [(352, 7), (367, 8)]), '4 binary inputs -> 16 combinations; 5 -> 32.')
    check('Celsius and Coulomb units separated', row(353, 7)['parameterUnits']['off'] == 'degC' and row(353, 10)['parameterUnits']['target'] == 'degC' and row(364, 5)['parameterUnits']['Q'] == 'C', 'degC denotes absolute temperature; C denotes charge.')
    check('Absolute-temperature sensitivities are increments', row(353, 7)['sensitivityValue'] == 6 and row(353, 7)['sensitivityResult'] == 4 and row(353, 10)['sensitivityValue'] == 4 and math.isclose(row(353, 10)['sensitivityResult'], 2.8), 'Both absolute temperatures increase by one degree, independent of temperature origin.')
    std = row(361, 3)
    samples = [std['parameters'][k] for k in ('F1', 'F2', 'F3')]
    changed = [std['sensitivityValue'], *samples[1:]]
    check('Population standard deviation recomputes the mean', math.isclose(std['result'], statistics.pstdev(samples)) and math.isclose(std['sensitivityResult'], statistics.pstdev(changed)), {'baseline': statistics.pstdev(samples), 'changed': statistics.pstdev(changed)})
    eff = row(366, 7)
    check('Efficiency sensitivity remains physically bounded', 0 <= eff['sensitivityValue'] <= 1 and math.isclose(eff['sensitivityValue'], .96) and math.isclose(eff['sensitivityResult'], 90.24), '.95 -> .96 charging efficiency; round-trip result 89.3% -> 90.24%.')
    check('Daily cycle-rate dimension', row(366, 9)['parameterUnits']['throughput'] == 'kWh/day' and row(366, 9)['resultUnit'] == 'cycles/day', 'Daily bidirectional energy / twice energy capacity gives cycles per day.')
    check('Energy acceptance labelled as energy', 'energy acceptance' in row(366, 10)['title'].lower(), row(366, 10)['title'])

    source_audit = json.loads((HERE / 'peer_track_sources.json').read_text())
    audited = {s['key'] for s in source_audit['sources']}
    used = {s['key'].removeprefix('track-') for d in courses.values() for s in d['sources']}
    check('Every used source has an identity/scope audit', used <= audited, {'used': len(used), 'missing': sorted(used - audited)})
    check('CWR historical source routed to CWR course', 'track-cwr' in {s['key'] for s in courses['b340']['sources']}, '2009 CWR rule is included in the course references.')
    check('Friction course has dedicated research sources', {'track-wet2012', 'track-wet2014', 'track-tor2017'} <= {s['key'] for s in courses['b365']['sources']}, 'Wet-adhesion and friction-layer measurement research replaces unrelated generic-only references.')
    check('Energy-storage direct report link', any(s['key'] == 'track-storage2010' and '/read/22911/chapter/1' in s['url'] for s in courses['b366']['sources']), 'Direct National Academies reader.')
    check('Three source-backed timeline entries per course', all(len(d['timeline']) == 3 for d in courses.values()), '99 entries; unique publication/project dates manually checked in the source audit.')
    issues = [c for c in checks if not c['passed']]
    result = dict(reviewer='v16_visual_assets', status='PASS' if not issues else 'NEEDS_FIXES', modelInputSha256=hashlib.sha256(numeric_path.read_bytes()).hexdigest(), checks=checks, issues=issues)
    (HERE / 'peer_track_semantics.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'status': result['status'], 'checks': len(checks), 'issues': issues, 'modelInputSha256': result['modelInputSha256']}, ensure_ascii=False, indent=2))
    return bool(issues)


if __name__ == '__main__':
    raise SystemExit(main())
