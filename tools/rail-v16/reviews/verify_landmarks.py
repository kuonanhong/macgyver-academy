#!/usr/bin/env python3
"""Independent numerical and provenance review for original b301–b334 teaching cases.
Run: python3 tools/rail-v16/reviews/verify_landmarks.py
No network or installation required. Standard-library only.
"""
import ast, hashlib, json, math, pathlib
from types import SimpleNamespace as N
ROOT=pathlib.Path(__file__).resolve().parent.parent
R=json.loads((ROOT/'reviews/landmarks_numeric.json').read_text())
S=json.loads((ROOT/'reviews/landmarks_sources.json').read_text())
# Separately written reference calculations use outputs in the displayed units.
REF={
'brake':lambda x:x.v*(x.delay+x.v/(2*x.a)),
'cant':lambda x:(x.v/x.R)*x.v-9.81*(x.cant/x.gauge),
'jerk':lambda x:x.a/x.ramp,
'capacity':lambda x:x.people*(3600/x.headway),
'dwell':lambda x:x.fixed+(x.exchange/x.doors)/x.rate,
 'turnback':lambda x:sum([x.arrival,x.reverse,x.release]),
'regen':lambda x:(x.mass*x.v**2/2)/3600000*x.eta,
'drag':lambda x:(x.rho*x.v**2/2)*(x.CdA*x.v)/1000,
'tunnelwave':lambda x:x.length/x.sound,
'pantograph':lambda x:math.sqrt(x.tension/x.density),
'thermal':lambda x:x.E*(x.alpha*x.deltaT),
'seismic':lambda x:x.distance*(1/x.vs-1/x.vp)-x.latency,
'settlement':lambda x:(x.drop*1000)/x.baseline,
'bridge':lambda x:(5/384)*(x.w/x.E)*(x.L**4/x.I)*1000,
'suspension':lambda x:math.sqrt(x.k/x.mass)/math.tau,
'wheelheat':lambda x:(x.energy/x.mass)/x.cp,
'adhesion':lambda x:x.mu*(x.weight/1000),
'grade':lambda x:9.81*x.gradient*x.mass*x.v/1000,
'voltage':lambda x:x.resistance*x.current,
'powerloss':lambda x:x.current*(x.current*x.resistance)/1000,
'isolation':lambda x:math.hypot(1,2*x.zeta*x.ratio)/math.hypot(1-x.ratio**2,2*x.zeta*x.ratio),
'localize':lambda x:(x.s1*x.s2)/math.hypot(x.s1,x.s2),
'communication':lambda x:x.latency*x.v,
'interlock':lambda x:math.prod([2]*x.inputs),
'brakecurve':lambda x:(x.initial-x.target)*(x.initial+x.target)/(2*x.a),
'axle':lambda x:x.wheel_force/(1000000*x.area),
'fatigue':lambda x:sum([x.n1/x.N1,x.n2/x.N2]),
'snow':lambda x:x.latent*(x.snow/1000),
'crosswind':lambda x:x.coefficient*x.side_area*x.height*(x.rho*x.wind**2/2)/1000,
'noise':lambda x:max(x.L1,x.L2)+10*math.log10(1+10**(-abs(x.L1-x.L2)/10)),
'drain':lambda x:x.area*(x.coefficient*x.rain),
'freeze':lambda x:(x.heat/x.latent)/(x.ice_density*x.ice_fraction),
'cooling':lambda x:x.heat/((x.density*x.flow)*x.cp),
'filter':lambda x:(x.pressure/x.eta)*x.flow,
'platform':lambda x:x.people/x.usable_area,
'escalator':lambda x:(x.speed/x.pitch)*(3600*x.occupants),
'doors':lambda x:math.hypot(x.stop_sigma,x.survey_sigma,x.door_sigma),
'ventilation':lambda x:math.log(1/x.remaining)/(x.flow/x.volume),
'piston':lambda x:x.speed*x.train_area,
'queue':lambda x:x.mean/2+x.sd*x.sd/(2*x.mean),
'availability':lambda x:1/(1+x.mttr/x.mtbf),
'rubber':lambda x:(x.coefficient*x.normal)*(x.speed/1000),
'baggage':lambda x:sum([x.plain,x.luggage*x.factor]),
'mixed':lambda x:x.gap/(x.fast-x.slow),
'neutral':lambda x:math.sqrt((0.5*x.mass*x.v*x.v-x.force*x.length)*2/x.mass),
'sampling':lambda x:(x.speed/x.wavelength)*2,
'bearing':lambda x:(x.rpm*x.order)/60,
'fleet':lambda x:math.floor(x.cycle/x.headway)+(x.cycle%x.headway>0),
'backup':lambda x:(x.energy/x.load)*(x.usable*x.eta),
'redundancy':lambda x:x.q2*x.q1,
'pressure':lambda x:(x.pressure/x.temperature)/x.Rair,
'sand':lambda x:(x.flux*x.duration)*x.area,
'survey':lambda x:math.hypot(x.dx,x.dy)*1000,
'grout':lambda x:(x.length*x.width)*(x.gap*x.allowance),
'transfer':lambda x:x.available-(x.distance/x.speed+x.vertical),
'congestion':lambda x:x.capacity-sum([x.flow1,x.flow2]),
'clearance':lambda x:x.gap-sum([x.sway,x.build,x.survey]),
'construction':lambda x:x.rate*(x.window-(x.setup+x.restore)),
}
ALLOWED=(ast.Expression,ast.BinOp,ast.UnaryOp,ast.Name,ast.Load,ast.Constant,ast.Add,ast.Sub,ast.Mult,ast.Div,ast.Pow,ast.USub,ast.UAdd,ast.Call)
ENV={'__builtins__':{},'log':math.log,'log10':math.log10,'ceil':math.ceil}
seen=set()
for row in R:
    identity=(row['course'],row['unit']); assert identity not in seen; seen.add(identity)
    for values,expected in [(row['inputs'],row['expected']),(row['perturbedInputs'],row['perturbedExpected'])]:
        for node in ast.walk(ast.parse(row['expression'],mode='eval')):
            assert isinstance(node,ALLOWED),(identity,type(node).__name__)
            if isinstance(node,ast.Call): assert isinstance(node.func,ast.Name) and node.func.id in {'log','log10','ceil'}
        value=eval(row['expression'],ENV,values)
        reference=REF[row['key']](N(**values))
        assert math.isfinite(value) and math.isclose(value,expected,rel_tol=1e-12,abs_tol=1e-10),(identity,'stored calculation')
        assert math.isclose(value,reference,rel_tol=1e-12,abs_tol=1e-10),(identity,'independent reference')
        if row['key']=='interlock': assert isinstance(values['inputs'],int) and int(value)==value
        if row['key']=='fleet': assert int(value)==value and value*values['headway']>=values['cycle'] and (value-1)*values['headway']<values['cycle']
        if row['key']=='brakecurve': assert values['initial']>values['target']>=0
        if row['key']=='mixed': assert values['fast']>values['slow']
        if row['key']=='ventilation': assert 0<values['remaining']<1
        if row['key']=='construction': assert values['window']>values['setup']+values['restore']
        for name in ['eta','usable','q1','q2','ice_fraction','coefficient']:
            if name in values and row['inputUnits'][name]=='1': assert 0<values[name]<=1
    doc=json.loads((ROOT/'inputs'/f"{row['course']}.json").read_text())
    unit=doc['units'][row['unit']-1]
    assert f'{row["output"]}={row["expression"]}={row["expected"]:.7g} {row["outputUnit"]}' in unit['model'],(identity,'display result')
    assert 'Original hypothetical exercise' in unit['model']
    if row['key']=='noise': assert row['perturbedInputs']['L1']==row['inputs']['L1']+3
assert len(R)==340 and len(seen)==340
assert {x['course'] for x in R}=={f'b{x}' for x in range(301,335)}
for s in S:
    path=ROOT/'inputs'/(s['course']+'.json')
    assert hashlib.sha256(path.read_bytes()).hexdigest()==s['fileSha256'],(s['course'],'source review hash stale')
    d=json.loads(path.read_text()); assert len(d['sources']) in (3,4)
    assert all('~' in x['model'] and '非本工程操作參數' in x['model'] for x in d['units'])
# Independent limiting identities make sign, scaling and unit errors visible.
assert math.isclose(REF['noise'](N(L1=70,L2=70)),73.01029995664,abs_tol=1e-10)
assert REF['thermal'](N(E=210000,alpha=1.15e-5,deltaT=0))==0
assert REF['queue'](N(mean=180,sd=0))==90
assert REF['queue'](N(mean=180,sd=60))==100
assert REF['grout'](N(length=20,width=2.5,gap=0.04,allowance=1.15))==2.3
assert math.isclose(REF['bridge'](N(w=50000,L=27.5,E=35e9,I=8))/REF['bridge'](N(w=50000,L=25,E=35e9,I=8)),1.4641,rel_tol=1e-12)
assert math.isclose(REF['localize'](N(s1=4,s2=2)),math.sqrt(3.2),rel_tol=1e-12)
loop=json.loads((ROOT/'inputs/b326.json').read_text())['units'][0]
assert loop['title'].endswith('Loop cycle and fleet requirement')
assert 'turnaround times' not in loop['verify']
report=dict(courses=34,units=340,baselineAndSensitivityChecks=680,independentReferences=len({r['key'] for r in R}),hashesVerified=34,limitingIdentities=7,status='PASS',limitations='Arithmetic, domains, displays and provenance checks do not certify a real railway. Source checks establish context; all numerical values remain hypothetical.')
(ROOT/'reviews/landmarks_numeric_review.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False))
