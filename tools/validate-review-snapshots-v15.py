#!/usr/bin/env python3
"""Check complete, non-author V15 reviews against the exact current course inputs.

This is a freshness and arithmetic gate, not a substitute for the recorded human-like
semantic/source review. It never manufactures or refreshes a review automatically.
"""
from pathlib import Path
import ast
import hashlib
import json
import math
import sys

ROOT=Path(__file__).resolve().parents[1]
AUTHOR=ROOT/'tools/water-v15'
GROUPS={
 'support':['three-gorges']+[f'b{x}' for x in range(202,210)]+[f'b{x}' for x in range(215,221)]+[f'b{x}' for x in range(296,301)],
 'ai_sync':[f'b{x}' for x in range(261,281)],
 'ground':[f'b{x}' for x in range(256,261)]+['b293'],
 'locks_coast':[f'b{x}' for x in range(281,293)]+['b294','b295'],
 'landmarks':[f'b{x}' for x in range(221,241)],
 'investigation':[f'b{x}' for x in range(210,215)]+[f'b{x}' for x in range(241,256)],
}
MATH_FUNCTIONS={'sqrt','sin','cos','tan','asin','acos','atan','atan2','exp','log','log10','log2','radians','degrees','hypot','ceil','floor','sinh','cosh','tanh'}
BUILTINS={'abs':abs,'min':min,'max':max,'round':round,'sum':sum}
ALLOWED=(ast.Expression,ast.Constant,ast.BinOp,ast.UnaryOp,ast.Add,ast.Sub,ast.Mult,ast.Div,ast.Pow,ast.Mod,ast.USub,ast.UAdd,ast.Call,ast.Name,ast.Attribute,ast.Load,ast.List,ast.Tuple)
def sha(data):return hashlib.sha256(data).hexdigest()
def read(p):return json.loads(p.read_text('utf-8'))
def metadata_hash(d):return sha(json.dumps({k:v for k,v in d.items() if k!='units'},ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
def evaluate(expression):
 if not isinstance(expression,str) or not 1<=len(expression)<=4000:raise ValueError('Invalid review expression')
 tree=ast.parse(expression,mode='eval')
 for n in ast.walk(tree):
  if not isinstance(n,ALLOWED):raise ValueError('Unsupported arithmetic syntax: '+type(n).__name__)
  if isinstance(n,ast.Constant) and (isinstance(n.value,bool) or not isinstance(n.value,(int,float))):raise ValueError('Non-numeric constant')
  if isinstance(n,ast.Name) and n.id not in {'math',*BUILTINS}:raise ValueError('Unknown arithmetic name')
  if isinstance(n,ast.Attribute):
   if not isinstance(n.value,ast.Name) or n.value.id!='math' or n.attr not in MATH_FUNCTIONS|{'pi','e'}:raise ValueError('Unsupported math attribute')
  if isinstance(n,ast.Call):
   if n.keywords:raise ValueError('Keyword calls are not allowed')
   if isinstance(n.func,ast.Name):
    if n.func.id not in BUILTINS:raise ValueError('Unsupported function')
   elif isinstance(n.func,ast.Attribute):
    if n.func.attr not in MATH_FUNCTIONS:raise ValueError('Unsupported math function')
   else:raise ValueError('Unsupported call')
 value=eval(compile(tree,'<review-arithmetic>','eval'),{'__builtins__':{},'math':math,**BUILTINS})
 if isinstance(value,bool) or not isinstance(value,(int,float)) or not math.isfinite(value):raise ValueError('Non-finite scalar review result')
 return value

def main():
 models=set();courses=set();reports=[];numeric_values=0
 targets={t['id'] for t in read(AUTHOR/'targets.json')}
 assert set(sum(GROUPS.values(),[]))==targets and sum(map(len,GROUPS.values()))==100
 for reviewer,expected in GROUPS.items():
  path=AUTHOR/'reviews'/f'peer_{reviewer}.json';report=read(path)
  assert report.get('status')=='PASS',f'{path.name}: review unfinished'
  assert report.get('nonAuthorReviewer') is True,f'{path.name}: non-author declaration missing'
  expected_reviewer={'ai_sync':'/root/ai_sync','locks_coast':'/root/ai_sync/locks_coast'}.get(reviewer,f'/root/courses_{reviewer}')
  assert report.get('reviewer')==expected_reviewer,f'{path.name}: reviewer identity'
  rows=report['rows'];metadata=report['courses'];assert len(rows)==len(expected)*10 and len(metadata)==len(expected),path.name
  inputs={cid:read(AUTHOR/'inputs'/f'{cid}.json') for cid in expected}
  local_models=set();local_courses=set()
  for row in rows:
   cid=row['courseId'];i=row['unit'];assert cid in inputs and isinstance(i,int) and 1<=i<=10
   key=(cid,i);assert key not in models and key not in local_models,f'Duplicate review {key}'
   unit=inputs[cid]['units'][i-1]
   assert row['status']=='PASS' and len(row.get('boundaryNotes','').strip())>=20,f'Missing semantic review {key}'
   assert row['modelSha256']==sha(unit['model'].encode()),f'Stale model review {key}'
   assert row['quizSha256']==sha(unit['misconception'].encode()),f'Stale quiz review {key}'
   # A unit can record several independently checked intermediate/output values.
   # Preserve these richer reviews instead of silently discarding all but one.
   columns=[row[k] for k in ['expression','actual','expected','tolerance']]
   if isinstance(columns[0],list):
    assert all(isinstance(c,list) and len(c)==len(columns[0]) for c in columns)
    assert 1<=len(columns[0])<=30
    calculations=zip(*columns)
   else:
    assert not any(isinstance(c,list) for c in columns)
    calculations=[columns]
   for expression,actual,expected_value,tol in calculations:
    result=evaluate(expression)
    assert all(isinstance(x,(int,float)) and not isinstance(x,bool) and math.isfinite(x) for x in [actual,expected_value,tol])
    assert tol>=0 and math.isclose(result,actual,rel_tol=1e-11,abs_tol=1e-11),f'Review recomputation changed {key}'
    assert abs(result-expected_value)<=tol+1e-12*max(1,abs(result)),f'Displayed result fails review {key}'
    numeric_values+=1
   local_models.add(key)
  for row in metadata:
   cid=row['courseId'];assert cid in inputs and cid not in courses and cid not in local_courses
   assert row['status']=='PASS' and len(str(row.get('metadataNotes','')).strip())>=20,f'Missing metadata review {cid}'
   assert row['inputSha256']==sha((AUTHOR/'inputs'/f'{cid}.json').read_bytes()),f'Stale full course review {cid}'
   assert row['metadataSha256']==metadata_hash(inputs[cid]),f'Stale metadata review {cid}'
   assert set(row['sourceURLs'])=={s['url'] for s in inputs[cid]['sources']},f'Source review coverage {cid}'
   local_courses.add(cid)
  assert local_models=={(c,i) for c in inputs for i in range(1,11)}
  assert local_courses==set(inputs)
  models.update(local_models);courses.update(local_courses)
  reports.append({'reviewer':report['reviewer'],'courses':len(expected),'models':len(expected)*10,'sha256':sha(path.read_bytes())})
 assert courses==targets and len(models)==1000
 print(json.dumps({'status':'PASS','independentlyReviewedCourses':100,'independentlyRecomputedModels':1000,'recomputedNumericValues':numeric_values,'currentQuizReviews':1000,'currentMetadataReviews':100,'scope':'Exact input/model/quiz/metadata hashes plus re-executed peer arithmetic; semantic and source decisions remain recorded reviewer judgments.','reports':reports},ensure_ascii=False))

if __name__=='__main__':
 try:main()
 except (AssertionError,ValueError,KeyError,FileNotFoundError,TypeError) as e:
  print('FAIL review gate: '+str(e),file=sys.stderr);sys.exit(1)
