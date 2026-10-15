import json,pathlib,collections
root=pathlib.Path(__file__).resolve().parents[1]
base=root/'public/academy'
def load(n):return json.loads((base/'data'/f'{n}.json').read_text())
cs=load('catalog');fs=load('featured');ss=load('sources');ps=load('photos')
release=load('release')
assert len(cs)==release['topics'] and len(fs)==release['guidedCourses']
assert len(fs)==({'13':710,'12':614,'11':515}.get(release['version'].split('.')[0],338))
if release['version'].split('.')[0] in ('12','13'):assert len([c for c in fs if c['category']=='instruments'])==101 and all(c.get('status')=='guided' for c in cs if c['category']=='instruments')
if release['version'].startswith('13.'):
 st=[c for c in fs if c['category']=='structures'];assert len(st)==100 and all(c.get('status')=='guided' for c in cs if c['category']=='structures'),'V13: 100 guided bridges & buildings courses'
 for c in st:
  v13=[x for x in c['stages'] if '-v13-' in x['id']];assert len(v13)==5 and all(len(x['steps'])==8 for x in v13),c['id']
  assert c.get('learningTrack')=='structures' and c.get('learningSubdiscipline','').startswith('st-'),c['id']
 assert release.get('structuresCourses')==100 and release.get('structuresSteps')==4000
assert len([c for c in fs if c['category']=='semiconductor'])==99
assert len([c for c in fs if c['category']=='packaging'])==100
for key in ('id','title','titleEn'):
 vals=[c[key].casefold() for c in cs];assert len(vals)==len(set(vals)),f'duplicate {key}'
sourceIds={s['id'] for s in ss};stepcount=knowledge=0
for c in cs:
 assert all(i in sourceIds for i in c.get('sourceIds',[])),c['id']
for c in fs:
 catalog_entry=next(i for i in cs if i['id']==c['id'])
 assert catalog_entry['stepCount']==sum(len(s['steps']) for s in c['stages'])
 assert 'stages' not in catalog_entry,'Catalog must stay slim; frontend hydrates from featured.'
 seen=set()
 for stage in c['stages']:
  for step in stage['steps']:
   assert step['id'] not in seen;seen.add(step['id']);stepcount+=1
   assert step['objective'] and step['objectiveEn']
   assert all(i in sourceIds for i in step.get('sourceIds',[])),step['id']
   q=step['quiz'];assert len(q['options'])==len(q['optionsEn']);assert 0<=q['answer']<len(q['options'])
   for k in step['knowledge']:
    assert k['text'] and k['textEn'];knowledge+=1
 if c['id'] in ('semiconductor','packaging'):
  assert len(c['stages'])==20
  steps=[s for stage in c['stages'] for s in stage['steps']]
  assert len(steps)==520 and all(len(stage['steps'])==26 for stage in c['stages'])
  assert len({s['title'] for s in steps})==520
  assert len({s['instruction'] for s in steps})==520
  photoIds={p['id'] for p in ps}
  for s in steps:
   for field in ('title','objective','instruction','observation','failure','check','photoNote'):
    assert isinstance(s.get(field),str) and s[field].strip(),(s['id'],field)
    assert isinstance(s.get(field+'En'),str) and s[field+'En'].strip(),(s['id'],field+'En')
   assert s['photoId'] in photoIds
   assert s['photoEvidence']=='representative-equipment-or-structure'
   assert all(i in seen for i in s['prerequisiteIds']),s['id']
  graph={s['id']:s['prerequisiteIds'] for s in steps};done=set();visiting=set()
  def visit(i):
   if i in done:return
   assert i not in visiting,f'Cycle at {i}'
   visiting.add(i)
   for p in graph[i]:visit(p)
   visiting.remove(i);done.add(i)
  for i in graph:visit(i)
for p in ps:
 assert (base/p['path']).is_file(),p['path']
 assert p['author'] and p['license'] and p['licenseUrl'] and p['sourceUrl']
assert not (base/'data/materials.json').exists(), 'Removed user-material index must not be shipped'
assert stepcount==release['allSteps'] and knowledge==release['knowledgePoints']
assert stepcount==({'13':13042+3232+4000,'12':13042+3232,'11':13042}.get(release['version'].split('.')[0],8882))
assert len([c for c in fs if c['category']=='electronics'])==100
print(json.dumps({'topics':len(cs),'guided':len(fs),'steps':stepcount,'knowledge':knowledge,'sources':len(ss),'photos':len(ps),'materials':0,'status':'PASS'}))
