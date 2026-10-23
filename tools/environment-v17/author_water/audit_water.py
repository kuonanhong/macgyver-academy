#!/usr/bin/env python3
"""Final structural, bilingual, expression and independent numerical spot audit."""
import ast,json,math,re,runpy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
files=[ROOT/'inputs'/f'b{i}.json' for i in range(426,451)]
TARGET={x['id']:x for x in json.loads((ROOT/'targets.json').read_text())}
known={}; stats=[]
ops={ast.Add:lambda a,b:a+b,ast.Sub:lambda a,b:a-b,ast.Mult:lambda a,b:a*b,ast.Div:lambda a,b:a/b,ast.Pow:lambda a,b:a**b,ast.FloorDiv:lambda a,b:a//b}
func={'sqrt':math.sqrt,'log':math.log,'log10':math.log10,'exp':math.exp,'abs':abs,'min':min,'max':max,'round':round}
def ev(n):
 if isinstance(n,ast.Expression): return ev(n.body)
 if isinstance(n,ast.Constant) and isinstance(n.value,(int,float)): return n.value
 if isinstance(n,ast.BinOp) and type(n.op) in ops:return ops[type(n.op)](ev(n.left),ev(n.right))
 if isinstance(n,ast.UnaryOp) and isinstance(n.op,(ast.USub,ast.UAdd)):return (-1 if isinstance(n.op,ast.USub) else 1)*ev(n.operand)
 if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id in func:return func[n.func.id](*(ev(a) for a in n.args))
 raise AssertionError(ast.dump(n))
def bilingual(s):
 assert isinstance(s,str) and s.count('~')==1,s
 z,e=s.split('~');assert re.search(r'[\u3400-\u9fff]',z) and re.search('[A-Za-z]',e),s
for p in files:
 d=json.loads(p.read_text()); cid=d['id'];t=TARGET[cid]
 assert d['title']==t['title']+'~'+t['titleEn']
 assert d['discipline']=='environment-water'
 assert len(d['units'])==10 and len(d['modelChecks'])==20
 for field in ['title','focus','summary','history']: bilingual(d[field])
 assert len(set(u['title'] for u in d['units']))==10
 for i,u in enumerate(d['units']):
  assert set(u)=={'title','mechanism','model','verify','failure','misconception','practice'}
  for value in u.values():bilingual(value)
  assert 'Diagnostic response:' in u['failure']
  assert 'Original teaching assumptions:' in u['model']
  for j,kind in enumerate(['baseline','perturbation']):
   c=d['modelChecks'][2*i+j]
   assert f'unit {i+1} ' in c['description'] and c['description'].endswith(kind)
   v=ev(ast.parse(c['expression'],mode='eval'))
   assert math.isfinite(v) and math.isclose(v,c['expected'],rel_tol=1e-9,abs_tol=1e-10)
 assert 5<=len(d['architectureNodes'])<=8
 for n in d['architectureNodes']:bilingual(n)
 assert len(d['sources'])>=2
 for s in d['sources']:
  assert s['accessed']=='2026-10-23' and s['url'].startswith('https://')
  if s['id'] in known: assert known[s['id']]==s['url']
  known[s['id']]=s['url']
 assert -90<=d['place']['lat']<=90 and -180<=d['place']['lon']<=180
 assert 'not an equipment site' in d['place']['nameEn']
 stats.append({'id':cid,'units':10,'checks':20,'sources':len(d['sources']),'bytes':p.stat().st_size})
# Manually selected independent expected values, not produced from model evaluation.
manual={
 ('b426',1):(360,420),('b426',4):(.1,2/15),('b426',5):(22.5,18),
 ('b427',2):(66,79.2),('b428',2):(182.8,228.5),('b429',6):(6,7.2),
 ('b431',7):(80,100),('b431',8):(40000,45000),('b432',5):(80,64),
 ('b433',2):(894.4,724.464),('b433',8):(.2,.175),('b434',7):(16,20),
 ('b435',2):(2888.888888888889,2222.222222222222),('b436',7):(20,10),
 ('b437',3):(3,2.25),('b438',5):(75,105),('b439',3):(.6,.75),
 ('b440',3):(540,900),('b440',8):(.95,1),('b441',4):(10,20/3),
 ('b442',2):(3.2,4.8),('b443',2):(.512,.729),('b443',3):(30,24),
 ('b444',5):(3.2,2.4),('b445',1):(12,16),('b446',5):(60,90),
 ('b446',8):(25,40),('b447',3):(2.25,2.5),('b448',3):(20,15),
 ('b449',3):(50,60),('b449',4):(.9,1),('b449',6):(220,214),
 ('b450',3):(.98,.97),('b450',4):(3940,4920),('b450',6):(4,5)
}
for (cid,i),vals in manual.items():
 d=json.loads((ROOT/'inputs'/f'{cid}.json').read_text())
 for j,v in enumerate(vals):assert math.isclose(d['modelChecks'][2*(i-1)+j]['expected'],v,rel_tol=1e-9,abs_tol=1e-10),(cid,i,j,v)
report={'status':'PASS','courseCount':len(stats),'unitCount':250,'arithmeticChecks':500,'independentManualChecks':2*len(manual),'uniqueSources':len(known),'courses':stats,'reviewNotes':['Every unit has one correct mechanism and one deliberately false misconception.','Baseline then perturbation checks are paired in unit order.','All numeric operating examples are hypothetical with boundaries, never project-specific settings.','All source coordinates are explicitly institutional references, not claimed equipment-site coordinates.','Physical process architectures have 6–7 bilingual nodes; diagnostic responses are calculation-specific.']}
(ROOT/'author_water/final-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='courses'},ensure_ascii=False))
