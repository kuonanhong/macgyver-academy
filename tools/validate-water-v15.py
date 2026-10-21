#!/usr/bin/env python3
"""Release gate: 100 curricula, bilingual authored depth, V14 preservation and assets."""
import hashlib, importlib.util, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];DATA=ROOT/'public/academy/data';AUTHOR=ROOT/'tools/water-v15'
read=lambda p:json.loads(p.read_text('utf-8'))
spec=importlib.util.spec_from_file_location('author_validator',AUTHOR/'validate_input.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
errors=[]
def expect(condition,message):
 if not condition:errors.append(message)
def digest(value):return hashlib.sha256(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def main():
 targets=read(AUTHOR/'targets.json');ids={t['id'] for t in targets};expect(len(ids)==100,'100 distinct target IDs')
 inputs=list((AUTHOR/'inputs').glob('*.json'));expect({p.stem for p in inputs}==ids,'all and only 100 author input files')
 for p in inputs:errors.extend(f'{p.stem}: {v}' for v in module.validate(p))
 baseline=read(ROOT/'docs/V15_BASELINE.json'); featured=read(DATA/'featured.json');by={c['id']:c for c in featured};catalog=read(DATA/'catalog.json');src={s['id'] for s in read(DATA/'sources.json')}
 expect(len(featured)==904,'904 guided curricula');expect(len(catalog)==2066,'2066 catalog entries')
 expect(len(by)==len(featured),'unique guided IDs')
 total=sum(len(st['steps']) for c in featured for st in c['stages']);expect(total==28274,f'28274 total steps (actual {total})')
 oldcount=0
 for cid,snapshot in baseline['courses'].items():
  expect(cid in by,f'original course {cid} retained')
  original=[st for st in by.get(cid,{}).get('stages',[]) if '-v15-' not in st['id']]
  expect(digest(original)==snapshot['stagesSha256'],f'{cid}: all V14 stage objects unchanged')
  expect(sum(len(st['steps']) for st in original)==snapshot['stepCount'],f'{cid}: V14 step count unchanged')
  oldcount+=snapshot['stepCount']
 expect(oldcount==24274,'24274 original step IDs in baseline')
 newcount=0
 for cid in ids:
  c=by.get(cid,{})
  expect(c.get('category')=='water',f'{cid}: water category')
  expect(c.get('learningTrack')=='water',f'{cid}: water learning track')
  stages=[st for st in c.get('stages',[]) if '-v15-' in st['id']];steps=[s for st in stages for s in st['steps']];newcount+=len(steps)
  expect(len(stages)==5 and len(steps)==40,f'{cid}: five new stages / 40 new steps')
  expect({s.get('unit') for s in steps}==set(range(1,11)),f'{cid}: 10 units')
  expect({s.get('unitFacet') for s in steps}=={'mechanism','model','verification','failure'},f'{cid}: four unit facets')
  seen=set()
  for st in c.get('stages',[]):
   for s in st['steps']:
    expect(s['id'] not in seen,f'{cid}: unique step {s["id"]}')
    expect(set(s.get('prerequisiteIds',[]))<=seen,f'{s["id"]}: valid earlier prerequisites');seen.add(s['id'])
    expect(set(s.get('sourceIds',[]))<=src,f'{s["id"]}: resolvable sources')
    if '-v15-' in s['id']:
     for k in ['title','objective','instruction','observation','failure','check']:
      expect(bool(s.get(k)) and bool(s.get(k+'En')),f'{s["id"]}: bilingual {k}')
     expect(len(s.get('knowledge',[]))==2,f'{s["id"]}: two knowledge points')
  for suffix in ('zh','en','icon'):
   expect((ROOT/f'public/academy/assets/diagrams/water-v15/{cid}-{suffix}.svg').is_file(),f'{cid}: {suffix} SVG')
 expect(newcount==4000,'4000 new water steps')
 media={m['courseId']:m for m in read(DATA/'media.json')['courses']}
 for cid in ids:
  guides={g['id']:g for g in media.get(cid,{}).get('guides',[])}
  g=guides.get(cid+'-v15-dossier',{})
  expect(6<=len(g.get('facts',[]))<=10 and len(g.get('facts',[]))==len(g.get('factsEn',[])),f'{cid}: bilingual dossier')
 for filename in ['course-places.json','related-skills.json','vendors.json']:
  entries=read(DATA/filename)['courses'];expect(ids<={x['courseId'] for x in entries},f'{filename}: all water associations')
 release=read(DATA/'release.json');expect(release.get('version')=='15.0.0','V15 release version');expect(release.get('waterSteps')==4000,'release new-step count')
 if errors:
  print('\n'.join('FAIL '+e for e in errors));return 1
 print(json.dumps({'status':'PASS','targetCourses':100,'authoredUnits':1000,'newSteps':4000,'preservedSteps':oldcount,'guidedCourses':len(featured),'allSteps':total,'originalSVGs':300},ensure_ascii=False));return 0
if __name__=='__main__':sys.exit(main())
