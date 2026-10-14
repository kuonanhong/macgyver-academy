#!/usr/bin/env python3
"""Restore the three pre-enrichment inputs before replaying curriculum generations.

V9 enrichments are reapplied last. Stable lesson IDs remain unchanged; this acts
only on authored source data, never on a learner database or local progress.
"""
import json
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root))
from portable.curriculum_parts import ensure_featured
ensure_featured(root/'public/academy')
baseline = json.loads((root/'tools/packaging-v9/existing_baseline.json').read_text('utf-8'))
path = root/'public/academy/data/featured.json'
courses = json.loads(path.read_text('utf-8'))
by_id = {c['id']:c for c in baseline['courses']}
assert set(by_id) == {'packaging', 'silicon-photonics', 'a106'}
courses = [by_id.get(c['id'], c) for c in courses]
path.write_text(json.dumps(courses, ensure_ascii=False, indent=2)+'\n', 'utf-8')

# V11 promotes 97 computing roadmaps and adds/promotes 80 world projects.
# Replay legacy generations against their original 2,000-topic input, then
# append V11 again; never use an enriched course as its own authoring baseline.
v11 = root/'tools/computing-v11'
if (v11/'v10-provenance.json').is_file():
    provenance=json.loads((v11/'v10-provenance.json').read_text('utf-8'))
    computing=json.loads((v11/'group_a_snapshot.json').read_text('utf-8'))
    original_computing={c['id']:c for c in computing['existing']}
    courses=[original_computing.get(c['id'],c) for c in courses if c['id'] in provenance['courses'] and (c['category']!='computing' or c['id'] in original_computing)]
    path.write_text(json.dumps(courses,ensure_ascii=False,indent=2)+'\n','utf-8')
    data=root/'public/academy/data'
    (data/'catalog.json').write_text((v11/'catalog-v10-snapshot.json').read_text('utf-8'),'utf-8')
    for name in ['sources','photos','release','media','vendors']:
        snapshot=v11/(name+'-v10-snapshot.json')
        (data/(name+'.json')).write_text(snapshot.read_text('utf-8'),'utf-8')
print('Restored baseline authoring inputs; enrichment is reapplied by V9 integration.')

# Restore the two V9 electronics courses before replaying V6/V7 authoring.
electronics = json.loads((root/'tools/electronics-v10/group_a_snapshot.json').read_text('utf-8'))
original = {c['id']: c for c in electronics['existing']}
assert set(original) == {'a203','a211'}
courses = [original.get(c['id'], c) for c in courses if c['category']!='electronics' or c['id'] in original]
path.write_text(json.dumps(courses, ensure_ascii=False, indent=2)+'\n', 'utf-8')
