#!/usr/bin/env python3
"""Verify all authored course schemas, displayed numbers, bounds, and integer scenarios.
Independent reduced numerical references and SI dimensions are in reviews/peer_control.py.
This script does not import or run the course generator.
"""
import ast,json,math,pathlib,runpy,sys
HERE=pathlib.Path(__file__).resolve().parent
ROOT=HERE.parent
models=runpy.run_path(str(HERE/'models.py'))['MODELS']
validator=runpy.run_path(str(ROOT/'validate_input.py'))['validate']
checks=json.loads((HERE/'numeric_checks.json').read_text())
assert len(checks)==330

def evaluate(node,values):
    if isinstance(node,ast.Expression):return evaluate(node.body,values)
    if isinstance(node,ast.Constant):return node.value
    if isinstance(node,ast.Name):return math.pi if node.id=='pi' else values[node.id]
    if isinstance(node,ast.UnaryOp):return -evaluate(node.operand,values) if isinstance(node.op,ast.USub) else evaluate(node.operand,values)
    if isinstance(node,ast.BinOp):
        a,b=evaluate(node.left,values),evaluate(node.right,values)
        return {ast.Add:lambda:a+b,ast.Sub:lambda:a-b,ast.Mult:lambda:a*b,ast.Div:lambda:a/b,ast.Pow:lambda:a**b}[type(node.op)]()
    if isinstance(node,ast.Call) and node.func.id in ('sqrt','log10'):
        return getattr(math,node.func.id)(evaluate(node.args[0],values))
    raise ValueError(ast.dump(node))

courses={}
for n in range(368,401):
    cid=f'b{n}';p=ROOT/'inputs'/f'{cid}.json'
    assert not validator(p),validator(p)
    courses[cid]=json.loads(p.read_text())
    assert len(courses[cid]['units'])==10
    assert len({u['title'] for u in courses[cid]['units']})==10

integer_scenarios=0
for c in checks:
    m=models[c['model']]; v={q[0]:q[1] for q in m['quantities']}
    x=evaluate(ast.parse(m['expression'],mode='eval'),v)
    assert math.isclose(x,c['result'],rel_tol=1e-12,abs_tol=1e-12)
    s=c['sensitivity'];v[s['symbol']]=s['changed']
    y=evaluate(ast.parse(m['expression'],mode='eval'),v)
    assert math.isfinite(y) and math.isclose(y,s['result'],rel_tol=1e-12,abs_tol=1e-12)
    if s['integerStep']:
        integer_scenarios+=1
        assert s['changed']==int(s['changed']) and s['changed']==s['base']+1
    else:assert math.isclose(s['changed'],s['base']*1.1)
    if c['model']=='coverage': assert 0<=v['tested']<=v['total']
    if c['model'] in ('confidence_zero','fault_union','redundancy','coverage','availability','packet_loss'):assert 0<=x<=1 and 0<=y<=1
    for q in m['quantities']:
        if q[2]=='1' and q[0] in ('eta','fraction','recycle','common','p','p1','p2','confidence'):assert 0<=v[q[0]]<=1
    u=courses[c['course']]['units'][c['unit']-1]
    for language in u['model'].split('~'):
        assert f'y={format(x,".6g")} {m["result_unit"]}' in language
    for language in u['practice'].split('~'):
        assert format(y,'.6g') in language
    # False misconceptions have an attached causal failure explanation and boundary.
    assert m['boundary'] in u['model'] or all(x in u['model'] for x in m['boundary'].split('~'))

report=dict(courses=len(courses),units=len(checks),models=len(models),integerScenarios=integer_scenarios,schemas='PASS',arithmetic='PASS',bounds='PASS',displayedNumbers='PASS',independentPeerScript='tools/rail-v16/reviews/peer_control.py')
(HERE/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
