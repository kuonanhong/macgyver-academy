#!/usr/bin/env python3
"""Check integrated release identities, V15 preservation and V16 completeness."""
import hashlib
import importlib.util
import json
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'public/academy/data'
def read(path):
    return json.loads(path.read_text(encoding='utf-8'))
def stage_hash(stage):
    return hashlib.sha256(json.dumps(stage, ensure_ascii=False, sort_keys=True).encode()).hexdigest()

def main():
    baseline = read(ROOT/'docs/V16_BASELINE.json')['courses']
    courses = read(DATA/'featured.json')
    catalog = read(DATA/'catalog.json')
    release = read(DATA/'release.json')
    by = {c['id']: c for c in courses}
    assert len(by) == len(courses) == 1003
    assert len(catalog) == len({c['id'] for c in catalog}) == 2066
    assert len(baseline) == 904
    preserved = 0
    for cid, old in baseline.items():
        assert cid in by, ('lost V15 course', cid)
        old_stages = by[cid]['stages'][:len(old['stageHashes'])]
        assert list(map(stage_hash, old_stages)) == old['stageHashes'], ('changed V15 stage', cid)
        assert sum(len(s['steps']) for s in old_stages) == old['steps']
        if cid != 'b301':
            assert len(by[cid]['stages']) == len(old['stageHashes']), ('unexpected extension', cid)
        preserved += old['steps']
    assert preserved == 28274
    targets = read(ROOT/'tools/rail-v16/targets.json')
    spec = importlib.util.spec_from_file_location('rail_validator', ROOT/'tools/rail-v16/validate_input.py')
    validator = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(validator)
    all_step_ids = set()
    all_steps = [s for c in courses for stage in c['stages'] for s in stage['steps']]
    assert len(all_steps) == 32274
    for step in all_steps:
        assert step['id'] not in all_step_ids, ('duplicate step ID', step['id'])
        all_step_ids.add(step['id'])
    source_ids = {s['id'] for s in read(DATA/'sources.json')}
    new_steps = 0
    for target in targets:
        cid = target['id']
        errors = validator.validate(ROOT/f'tools/rail-v16/inputs/{cid}.json')
        assert not errors, '\n'.join(errors)
        c = by[cid]
        assert c['subcategory'] == target['discipline']
        stages = [s for s in c['stages'] if '-v16-' in s['id']]
        steps = [s for stage in stages for s in stage['steps']]
        assert len(stages) == 5 and len(steps) == 40, cid
        new_steps += len(steps)
        assert c.get('sourceIds') and set(c['sourceIds']) <= source_ids, cid
        for step in steps:
            assert set(step.get('sourceIds', [])) <= source_ids, step['id']
        for lang in ('zh', 'en'):
            svg = ROOT/f'public/academy/assets/diagrams/v16-{cid}-{lang}.svg'
            ET.parse(svg)
            assert c['flowDiagramEn' if lang == 'en' else 'flowDiagram'] == str(svg.relative_to(ROOT/'public/academy'))
    assert new_steps == 4000
    for key, expected in {'version':'16.0.0','guidedCourses':1003,'allSteps':32274,'railCourses':100,'railSteps':4000,'newGuidedCourses':99,'newGuidedSteps':4000,'actualPhotos':129}.items():
        assert release[key] == expected, (key, release[key], expected)
    public = read(DATA/'lazy/index.json')
    owner = read(DATA/'lazy/owner-index.json')
    assert len([c for c in public['catalog'] if c.get('_lazy')]) == 1003
    for cid in [t['id'] for t in targets]:
        preview = read(ROOT/'public/academy'/public['courses'][cid]['file'])
        full = read(ROOT/'public/academy'/owner['courses'][cid]['file'])
        assert full == by[cid]
        assert preview['previewOnly'] and preview['freeStagesPerCourse'] == 1
        assert preview['stages'][0] == full['stages'][0]
        assert all(step['locked'] for stage in preview['stages'][1:] for step in stage['steps'])
    result = {'status':'PASS', 'version':'16.0.0', 'topics':2066, 'guidedCourses':1003,
              'allSteps':32274, 'preservedV15Courses':904, 'preservedV15Steps':preserved,
              'railCourses':100, 'authoredRailUnits':1000, 'newRailSteps':4000,
              'newGuidedCourses':99, 'extendedExistingCourse':'b301', 'railDiagramFiles':200,
              'baselineStageHashesMatch':True, 'uniqueStepIds':True,
              'publicFirstStageOnly':True, 'ownerPayloadsExact':True,
              'scope':'Structural and preservation validation; formula/source peer reviews are separate reports.'}
    (ROOT/'docs/VALIDATION_CURRICULUM_V16.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result, ensure_ascii=False))

if __name__ == '__main__':
    main()
