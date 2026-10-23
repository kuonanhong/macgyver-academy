#!/usr/bin/env python3
"""Independent arithmetic and dimensional review of authored track models.

No generator evaluator is imported. Expressions are walked as an AST with a
small mathematical vocabulary, and dimensions propagate independently.
"""
from pathlib import Path
from fractions import Fraction
import ast
import collections
import hashlib
import json
import math
import re

HERE=Path(__file__).resolve().parent
BASE=HERE.parent
ZERO=(0,0,0,0,0,0)  # mass, length, time, temperature, electrical current, amount
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def scale(a,b):return tuple(x*b for x in a)
D={
 '1':ZERO,'count':ZERO,'cycles':ZERO,'events':ZERO,'trains':ZERO,'train':ZERO,'states':ZERO,'sleepers':ZERO,'pixel':ZERO,'alarms':ZERO,
 'turn':ZERO,'rad':ZERO,'mrad':ZERO,'degree':ZERO,'percent':ZERO,'dB':ZERO,
 'kg':(1,0,0,0,0),'g':(1,0,0,0,0),'t':(1,0,0,0,0),'MGT':(1,0,0,0,0),
 'm':(0,1,0,0,0),'mm':(0,1,0,0,0),'cm':(0,1,0,0,0),'um':(0,1,0,0,0),'km':(0,1,0,0,0),'litre':(0,3,0,0,0),
 's':(0,0,1,0,0),'ms':(0,0,1,0,0),'h':(0,0,1,0,0),'min':(0,0,1,0,0),'day':(0,0,1,0,0),
 'K':(0,0,0,1,0),'degC':(0,0,0,1,0),'C':(0,0,1,0,1),'A':(0,0,0,0,1),'mA':(0,0,0,0,1),
 'N':(1,1,-2,0,0),'kN':(1,1,-2,0,0),'MN':(1,1,-2,0,0),
 'Pa':(1,-1,-2,0,0),'kPa':(1,-1,-2,0,0),'MPa':(1,-1,-2,0,0),'GPa':(1,-1,-2,0,0),'HV':(1,-1,-2,0,0),
 'J':(1,2,-2,0,0),'kJ':(1,2,-2,0,0),'MJ':(1,2,-2,0,0),'Wh':(1,2,-2,0,0),'kWh':(1,2,-2,0,0),
 'W':(1,2,-3,0,0),'kW':(1,2,-3,0,0),'MW':(1,2,-3,0,0),'MVA':(1,2,-3,0,0),
 'V':(1,2,-3,0,-1),'kV':(1,2,-3,0,-1),
 'ohm':(1,2,-3,0,-2),'kohm':(1,2,-3,0,-2),'Mohm':(1,2,-3,0,-2),'mohm':(1,2,-3,0,-2),'S':(-1,-2,3,0,2),
 'Hz':(0,0,-1,0,0),'F':(-1,-2,4,0,2),'H':(1,2,-2,0,-2),
}
D={key:value+(0,) if len(value)==5 else value for key,value in D.items()}
D['mol']=(0,0,0,0,0,1)
TOKEN=re.compile('('+'|'.join(re.escape(x) for x in sorted(D,key=len,reverse=True))+r')(\d+(?:\.\d+)?)?')

def dimension(unit):
    if unit in D:return D[unit]
    result=ZERO
    for i,part in enumerate(unit.split('/')):
        pos=0
        while pos<len(part):
            if part[pos] in '* ':pos+=1;continue
            match=TOKEN.match(part,pos)
            if not match:raise ValueError('Unknown unit token: '+unit+' at '+part[pos:])
            name,power=match.groups();power=Fraction(power or '1')*(-1 if i else 1)
            result=add(result,scale(D[name],power));pos=match.end()
    return result

def evaluate(expression,parameters,units):
    def walk(n):
        if isinstance(n,ast.Constant) and isinstance(n.value,(int,float)):return float(n.value),ZERO
        if isinstance(n,ast.Name):
            if n.id=='pi':return math.pi,ZERO
            return parameters[n.id],dimension(units[n.id])
        if isinstance(n,ast.UnaryOp):
            value,dim=walk(n.operand)
            if isinstance(n.op,ast.USub):return -value,dim
            if isinstance(n.op,ast.UAdd):return value,dim
        if isinstance(n,ast.BinOp):
            left,ld=walk(n.left);right,rd=walk(n.right)
            if isinstance(n.op,(ast.Add,ast.Sub)):
                assert ld==rd,('Incompatible additive dimensions',ld,rd)
                return (left+right if isinstance(n.op,ast.Add) else left-right),ld
            if isinstance(n.op,ast.Mult):return left*right,add(ld,rd)
            if isinstance(n.op,ast.Div):return left/right,add(ld,scale(rd,-1))
            if isinstance(n.op,ast.Pow):
                assert rd==ZERO,'Dimensional exponent'
                return left**right,scale(ld,Fraction(right).limit_denominator(10000))
        if isinstance(n,ast.Call) and isinstance(n.func,ast.Name):
            vals=[walk(x) for x in n.args];name=n.func.id
            if name=='sqrt':return math.sqrt(vals[0][0]),scale(vals[0][1],Fraction(1,2))
            if name=='abs':return abs(vals[0][0]),vals[0][1]
            if name in ('min','max'):
                assert all(d==vals[0][1] for v,d in vals),'Incompatible extrema dimensions'
                return (min if name=='min' else max)(v for v,d in vals),vals[0][1]
            if name in ('sin','cos','atan','log','exp'):
                assert vals[0][1]==ZERO,('Function requires dimensionless input',name)
                return getattr(math,name)(vals[0][0]),ZERO
        raise ValueError('Unsupported expression node: '+ast.dump(n))
    return walk(ast.parse(expression,mode='eval').body)

def main():
    source=BASE/'reviews/track_numeric_models.json'
    data=json.loads(source.read_text());models=data['models'];issues=[];details=[]
    for row in models:
        loc=f"{row['courseId']}:{row['unit']}"
        try:
            value,dim=evaluate(row['expression'],row['parameters'],row['parameterUnits'])
            assert math.isfinite(value),'Nonfinite baseline'
            assert math.isclose(value,row['result'],rel_tol=1e-11,abs_tol=1e-12),('Baseline mismatch',value,row['result'])
            assert dim==dimension(row['resultUnit']),('Result dimension mismatch',dim,dimension(row['resultUnit']))
            name=row['sensitivityParameter'];changed=dict(row['parameters'])
            changed[name]=row.get('sensitivityValue',row.get('sensitivityInput',changed[name]*1.1))
            new,_=evaluate(row['expression'],changed,row['parameterUnits'])
            assert math.isclose(new,row['sensitivityResult'],rel_tol=1e-11,abs_tol=1e-12),('Sensitivity mismatch',new,row['sensitivityResult'])
            path=BASE/'inputs'/f"{row['courseId']}.json"
            if path.exists():
                lesson=json.loads(path.read_text())['units'][row['unit']-1]
                assert row['modelBoundary'] in lesson['model'], 'Generated lesson has stale model boundary'
            details.append({'id':loc,'baseline':value,'perturbedInput':changed[name],'perturbedResult':new,'dimensionPass':True})
        except Exception as error:
            issues.append({'id':loc,'title':row['title'],'problem':str(error)})
    report={'reviewer':'v16_visual_assets','method':'Independent AST arithmetic and dimensional propagation; no generator evaluator imported.',
        'inputSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'models':len(models),'passed':len(details),'issues':issues,'details':details,
        'scope':'Arithmetic, dimensional consistency and generated-boundary freshness; not site validation or proof that chosen reduced models cover all physical effects.'}
    (HERE/'peer_track_numeric.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='details'},ensure_ascii=False,indent=2))
    return bool(issues)

if __name__=='__main__':raise SystemExit(main())
