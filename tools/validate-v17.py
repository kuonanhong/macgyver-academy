#!/usr/bin/env python3
"""Release data checks; no network, uploads or private-state access."""
from pathlib import Path
import argparse,hashlib,json,subprocess,sys,importlib.util
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'public/academy/data'
def read(p):return json.loads(p.read_text())
def steps(c):return [s for st in c.get('stages',[]) for s in st['steps']]
def main():
 p=argparse.ArgumentParser();p.add_argument('--baseline',type=Path,required=True);p.add_argument('--browser-report',type=Path,required=True);args=p.parse_args()
 courses=read(DATA/'featured.json');index={c['id']:c for c in courses};catalog=read(DATA/'catalog.json');sources={s['id']:s for s in read(DATA/'sources.json')}
 assert len(index)==len(courses)==1102;assert len(catalog)==2066
 env=[c for c in courses if c['category']=='environment'];assert len(env)==100
 assert sum(len(steps(c)) for c in courses)==36274
 ids=set();new=[]
 for c in courses:
  assert c['stepCount']==len(steps(c)),c['id']
  for s in steps(c):
   assert s['id'] not in ids,s['id'];ids.add(s['id'])
   if '-v17-' not in s['id']:continue
   new.append(s)
   assert all(s.get(k) for k in ['title','titleEn','objective','objectiveEn','instruction','instructionEn','observation','observationEn','failure','failureEn','check','checkEn'])
   q=s['quiz'];assert len(q['options'])==len(q['optionsEn'])==3 and len(set(q['options']))==3 and 0<=q['answer']<3
   assert s['sourceIds'] and all(i in sources for i in s['sourceIds'])
   assert s['environmentExample']['expression'] and s['environmentExample']['unit']
 assert len(new)==4000
 spec=importlib.util.spec_from_file_location('environment_builder',ROOT/'tools/environment-v17/build_environment.py');builder=importlib.util.module_from_spec(spec);spec.loader.exec_module(builder)
 for inputfile in (ROOT/'tools/environment-v17/inputs').glob('b*.json'):
  authored=read(inputfile);built=[s for s in steps(index[authored['id']]) if '-v17-' in s['id']]
  for i,unit in enumerate(authored['units']):
   for facet in range(4):
    actual=built[i*4+facet];expected=builder.step_for(authored,unit,i,facet,actual['sourceIds'],actual['prerequisiteIds'][0] if actual['prerequisiteIds'] else None)
    assert all(actual[k]==v for k,v in expected.items() if k!='sequence'),('Stale authored input',actual['id'])
 original=read(args.baseline/'public/academy/data/featured.json');preserved=0
 for c in original:
  assert c['id'] in index
  for old in steps(c):
   current=next(s for s in steps(index[c['id']]) if s['id']==old['id']);assert current==old,old['id'];preserved+=1
 assert preserved==32274
 related={c['courseId']:c for c in read(DATA/'related-skills.json')['courses']};places={c['courseId']:c for c in read(DATA/'course-places.json')['courses']}
 for c in env:
  assert len([s for s in steps(c) if '-v17-' in s['id']])==40
  assert len({s['unit'] for s in steps(c) if '-v17-' in s['id']})==10
  r=related[c['id']];assert r['references'] and len(r['related'])==2
  for item in r['related']:assert len(item['practice'])==len(item['practiceEn'])==3
  loc=places[c['id']]['place'];assert -90<=loc['lat']<=90 and -180<=loc['lng']<=180 and (loc['lat'],loc['lng'])!=(0,0)
  for field in ['flowDiagram','flowDiagramEn']:assert (DATA.parent/c[field]).is_file()
 manifest=read(DATA/'scene-assets-v17.json');assets=manifest.get('assets',[]);assert len(assets)==156
 for asset in assets:
  filename=asset.get('localPath') or asset.get('path');assert filename,asset['id'];assert (DATA.parent/filename).is_file(),filename
 assert len(manifest['categoryDefaults'])==20
 curriculum=read(ROOT/'docs/VALIDATION_CURRICULUM_V17.json');assert curriculum['status']=='PASS'
 upload=read(ROOT/'docs/VALIDATION_UPLOAD_V17.json');assert upload['status']=='PASS'
 browser=read(args.browser_report);assert browser['status']=='PASS'
 # Run the actual scene math/state, assistance, account isolation and unit calculators.
 commands=[['node','tools/environment-v17/test-workbench-v17.mjs'],['node','tools/scene-v17/test-scene-v17.mjs'],['node','tools/scene-v17/test-workshop-assist-v17.mjs'],['node','tools/test-account-race-v10.mjs'],['node','--test','tools/environment-v17/test-unit-lab.mjs'],['python3','tools/check-offline.py']]
 logs=[]
 for command in commands:
  result=subprocess.run(command,cwd=ROOT,text=True,capture_output=True)
  logs.append({'command':' '.join(command),'exitCode':result.returncode,'output':result.stdout[-5000:],'error':result.stderr[-2000:]})
  if result.returncode:print(result.stdout,result.stderr);raise RuntimeError('Failed: '+' '.join(command))
 report={'status':'PASS','version':'17.0.0','catalogTopics':len(catalog),'guidedCourses':len(courses),'steps':len(ids),'environmentCourses':len(env),'newSteps':len(new),'oldStepsPreservedExactly':preserved,'numericChecks':curriculum['numericChecks'],'imageAssets':len(assets),'tests':logs,'browser':browser,'uploadValidation':'docs/VALIDATION_UPLOAD_V17.json','limitations':['Chinese and English authored; other language course translations require configured translation.','Seven fixed-view panoramas; no per-course surveyed digital twin.','No real cloud AI inference, GitHub push or production deployment performed.']}
 (ROOT/'docs/VALIDATION_V17.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items() if k not in ['tests','browser','limitations']},ensure_ascii=False))
if __name__=='__main__':main()
