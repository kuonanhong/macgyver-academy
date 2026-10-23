#!/usr/bin/env python3
"""Validate authored inputs using the integration builder's arithmetic engine."""
from pathlib import Path
import importlib.util,json,math
p=Path(__file__).resolve().parent.parent
s=importlib.util.spec_from_file_location('env_builder',p/'build_environment.py')
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
targets={x['id']:x for x in json.loads((p/'targets.json').read_text())}
report={'courses':0,'units':0,'numericChecks':0,'bilingualFields':0,'bytes':0}
urls=set()
for i in range(476,501):
    path=p/'inputs'/f'b{i}.json';c=json.loads(path.read_text());assert c['id']==f'b{i}'
    assert c['title']==targets[c['id']]['title']+'~'+targets[c['id']]['titleEn']
    for key in ('title','focus','summary','history'):m.pair(c[key]);report['bilingualFields']+=1
    assert len(c['units'])==10 and len({u['title'] for u in c['units']})==10
    for u in c['units']:
        for k in ('title','mechanism','model','verify','failure','misconception','practice'):
            m.pair(u[k]);report['bilingualFields']+=1
        assert 'Original teaching assumptions' in u['model']
    for node in c['architectureNodes']:m.pair(node)
    assert 5<=len(c['architectureNodes'])<=8 and len(c['sources'])>=2
    for source in c['sources']:
        assert source['url'].startswith('https://') and source['id'].startswith('v17s-')
        urls.add(source['url'])
    assert len(c['modelChecks'])==20
    for r in c['modelChecks']:
        value=m.calc(r['expression'])
        assert math.isfinite(value) and math.isclose(value,r['expected'],rel_tol=r.get('relativeTolerance',1e-5),abs_tol=1e-5),(c['id'],r,value)
        report['numericChecks']+=1
    report['courses']+=1;report['units']+=len(c['units']);report['bytes']+=path.stat().st_size
report['primarySourceCount']=len(urls)
report['result']='PASS: root calculator, target titles, paired fields, 10 unique topics/course, 20 checks/course, source links'
(p/'author_waste'/'integration_validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False))
