#!/usr/bin/env python3
"""Export only first-stage curricula and public assets; full authoring stays local."""
from __future__ import annotations
import argparse, hashlib, json, re, shutil, tempfile
from pathlib import Path

MARKER = '.macgyver-static-export'
BLOCKED = {'.git','node_modules','models','local-documents','owner-private','credentials','secrets','uploads','__pycache__','userdata','user-data','accounts','auth'}
SUFFIXES = {'.pem','.key','.p12','.pfx','.sqlite','.sqlite3','.db','.gguf','.safetensors','.ckpt','.pt','.pth','.onnx','.bin','.pyc','.h5','.hdf5','.pb','.npy','.npz','.pkl','.pickle','.keras','.model'}
ID = re.compile(r'^[a-z0-9]+(?:[-_][a-z0-9]+)*$')
META = {'id','title','titleEn','category','subcategory','subcategoryTitle','subcategoryTitleEn','summary','summaryEn','status','kind','stepCount','estimatedMinutes','photoId','educationEdition','enrichmentVersion','curriculumVersion','contentStatus','depth','languageCoverage','learningTrack','learningSubdiscipline','learningTags','tags','architectureFamily','_lazy','_lazyTopic','stages'}

def serial(value):
    return json.dumps(value,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c').replace('\u2028','\\u2028').replace('\u2029','\\u2029')

def safe_index(index):
    if index.get('lazyVersion')!=1 or not isinstance(index.get('catalog'),list):raise ValueError('Invalid public catalogue.')
    ids=[];guided=[]
    for course in index['catalog']:
        if not isinstance(course,dict) or set(course)-META or not ID.fullmatch(course.get('id','')):raise ValueError('Catalogue contains non-public fields.')
        ids.append(course['id'])
        if 'stages' in course:
            guided.append(course['id'])
            for stage in course['stages']:
                if set(stage)-{'id','title','titleEn','order','steps'}:raise ValueError('Catalogue stage contains lesson bodies.')
                if any(set(step)!={'id'} for step in stage['steps']):raise ValueError('Catalogue step contains lesson bodies.')
    if len(set(ids))!=len(ids) or set(index.get('guidedIds',[]))!=set(guided) or len(index.get('guidedIds',[]))!=len(guided):raise ValueError('Invalid guided catalogue IDs.')
    for group in ('courses','resources'):
        if not isinstance(index.get(group),dict) or set(index[group])!=set(ids):raise ValueError('Incomplete public descriptors.')
    if not isinstance(index.get('auxiliary'),dict):raise ValueError('Invalid public auxiliary descriptors.')
    if set(index['auxiliary'])&{'catalog','featured','photos','release'}:raise ValueError('Full curriculum cannot be an auxiliary payload.')

def compact_index(index):
    result={**index,'compactVersion':1}
    result['catalog']=[{**c,'stages':[{**s,'steps':[step['id'] for step in s['steps']]} for s in c['stages']]} if 'stages' in c else c for c in index['catalog']]
    for group in ('courses','resources','auxiliary'):
        result[group]={identifier:[d['sha256'],d['byteLength']] for identifier,d in index[group].items()}
    return result

def safe_course(value,cid):
    if not isinstance(value,dict) or value.get('id')!=cid:raise ValueError('Mismatched preview course: '+cid)
    if not isinstance(value.get('stages'),list):return
    if set(value)-(META|{'scope','scopeEn','sourceIds','diagram','flowDiagram','flowDiagramEn','architectureNodes','architectureEdges','v16Architecture','previewOnly','freeStagesPerCourse'}):raise ValueError('Unexpected full-course fields reached preview export: '+cid)
    if 'flowDiagramEn' in value and (not isinstance(value['flowDiagramEn'],str) or not re.fullmatch(r'assets/diagrams/[A-Za-z0-9_-]+\.svg',value['flowDiagramEn'])):
        raise ValueError('Unsafe English diagram asset: '+cid)
    if 'v16Architecture' in value:
        arch=value['v16Architecture']
        if not isinstance(arch,dict) or set(arch)!={'architectureFamily','architectureNodes','architectureEdges'}:
            raise ValueError('Invalid public architecture fields: '+cid)
        nodes,edges=arch['architectureNodes'],arch['architectureEdges']
        if not isinstance(arch['architectureFamily'],str) or not re.fullmatch(r'[a-z0-9-]{1,80}',arch['architectureFamily']):
            raise ValueError('Invalid public architecture family: '+cid)
        if not isinstance(nodes,list) or not 1<=len(nodes)<=64 or any(not isinstance(n,list) or len(n)!=2 or any(not isinstance(t,str) or not 1<=len(t)<=200 for t in n) for n in nodes):
            raise ValueError('Invalid public architecture nodes: '+cid)
        if not isinstance(edges,list) or len(edges)>128 or any(not isinstance(e,list) or len(e)!=2 or any(type(i) is not int or not 0<=i<len(nodes) for i in e) for e in edges):
            raise ValueError('Invalid public architecture edges: '+cid)
    if value.get('previewOnly') is not True or type(value.get('freeStagesPerCourse')) is not int or value['freeStagesPerCourse']!=1:raise ValueError('Only exactly one free stage may be exported: '+cid)
    for stage in value['stages'][1:]:
        if set(stage)-{'id','order','title','titleEn','steps'}:raise ValueError('Member stage body reached preview export: '+cid)
        for step in stage['steps']:
            allowed={'id','order','sequence','title','titleEn','locked','prerequisiteIds','sourceIds','knowledge','quiz'}
            quiz=step.get('quiz',{})
            if step.get('locked') is not True or set(step)-allowed or step.get('knowledge') or any(quiz.get(k) for k in ('question','questionEn')) or any(any(quiz.get(k,[])) for k in ('options','optionsEn')) or set(quiz)-{'question','questionEn','options','optionsEn','answer'}:
                raise ValueError('Member body reached preview export: '+cid)

def safe_media(value,cid):
    if not isinstance(value,dict):raise ValueError('Invalid public resources: '+cid)
    media=value.get('media',value)
    if media.get('guides') or any(c.get('guides') for c in media.get('courses',[]) if isinstance(c,dict)):
        raise ValueError('Full supplemental guide reached preview export: '+cid)

def bound_script(descriptor,raw):
    payload=raw.decode('utf-8').strip().replace('<','\\u003c').replace('\u2028','\\u2028').replace('\u2029','\\u2029')
    return ('/* Generated on-demand data. */\nwindow.MG_LAZY_DATA=window.MG_LAZY_DATA||Object.create(null);\nwindow.MG_LAZY_DATA['+json.dumps(descriptor['file'])+']={sha256:'+json.dumps(descriptor['sha256'])+',value:'+payload+'};\n').encode('utf-8')

def export(source: Path, output: Path) -> dict:
    if output.is_symlink():raise ValueError('Output must not be a symlink.')
    source, output = source.resolve(), output.resolve()
    if source == output or source in output.parents or output in source.parents:
        raise ValueError('Output must be separate from the public source.')
    if output.exists() and (output.is_symlink() or not (output/MARKER).is_file()):
        raise ValueError('Output exists and is not a marked generated export. Choose another directory.')
    index = json.loads((source/'data/lazy/index.json').read_text('utf-8'))
    if index.get('release',{}).get('version','').split('.')[0] != '19':
        raise ValueError('Rebuild V19 before exporting the public preview.')
    safe_index(index)
    compact=compact_index(index)
    if json.loads((source/'data/lazy/index.compact.json').read_text('utf-8'))!=compact:
        raise ValueError('Public expanded/compact indexes disagree; rebuild V19.')
    output.parent.mkdir(parents=True,exist_ok=True)
    temp = Path(tempfile.mkdtemp(prefix='macgyver-preview-',dir=output.parent))
    def copy(rel):
        src = source/rel
        if src.is_symlink() or not src.is_file() or not src.resolve().is_relative_to(source):
            raise ValueError('Unsafe or absent public asset: '+str(rel))
        if {part.casefold() for part in rel.parts}&BLOCKED or src.suffix.lower() in SUFFIXES or src.name.casefold().startswith('.env') or src.name.casefold() in {'credentials.json','accounts.json','users.json','tokens.json','token.json','cookies.json','cookies.txt','owner.json'}:
            raise ValueError('Private file in public export: '+str(rel))
        dst=temp/rel; dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst)
    try:
        # Only reviewed browser code and art. The data directory uses a descriptor allowlist.
        for src in source.iterdir():
            if src.is_file() and src.suffix in {'.html','.js','.css','.webmanifest','.txt'} and not src.name.startswith('offline-data'):
                copy(src.relative_to(source))
        for folder in ('assets','vendor','i18n'):
            for src in (source/folder).rglob('*'):
                if src.is_file():copy(src.relative_to(source))
        (temp/'data/lazy').mkdir(parents=True,exist_ok=True)
        (temp/'data/lazy/index.json').write_text(serial(index)+'\n','utf-8')
        (temp/'data/lazy/index.compact.json').write_text(serial(compact)+'\n','utf-8')
        # Derive file:// bootstrap from the same reviewed public index. Never
        # copy an old full/offline payload left over from another version.
        bootstrap='/* Generated public preview catalogue only. */\nwindow.MG_LAZY_INDEX='+serial(index)+';\nwindow.MG_DATA={catalog:window.MG_LAZY_INDEX.catalog,featured:window.MG_LAZY_INDEX.guidedIds.map(id=>window.MG_LAZY_INDEX.catalog.find(c=>c.id===id)),photos:window.MG_LAZY_INDEX.photos,sources:[],release:window.MG_LAZY_INDEX.release};\nwindow.MG_DATA_FILES=[];\n'
        (temp/'offline-data.js').write_text(bootstrap,'utf-8')
        count=0
        for group in ('courses','resources','auxiliary'):
            for cid, d in index[group].items():
                prefix='data' if group=='auxiliary' else group
                if not ID.fullmatch(cid) or not re.fullmatch(r'[0-9a-f]{64}',d.get('sha256','')) or type(d.get('byteLength')) is not int or not 2<=d['byteLength']<=32*1024*1024 or d.get('file')!=f"data/lazy/{prefix}/{cid}-{d['sha256'][:16]}.json" or d.get('script')!=d['file'][:-5]+'.js':
                    raise ValueError('Unsafe public descriptor: '+cid)
                rel=Path(d['file'])
                if (source/rel).is_symlink() or not (source/rel).resolve().is_relative_to(source):raise ValueError('Unsafe public payload: '+cid)
                raw=(source/rel).read_bytes()
                if len(raw)!=d['byteLength'] or hashlib.sha256(raw).hexdigest()!=d['sha256']:
                    raise ValueError('Rebuild: mismatched '+str(rel))
                value=json.loads(raw)
                if group=='courses':safe_course(value,cid)
                if group=='resources' or group=='auxiliary' and cid=='media':safe_media(value,cid)
                script=source/d['script']
                if script.is_symlink() or not script.resolve().is_relative_to(source) or script.read_bytes()!=bound_script(d,raw):
                    raise ValueError('Classic script does not match its checked JSON; rebuild: '+cid)
                copy(rel);copy(Path(d['script']));count+=1
                if group=='auxiliary':
                    (temp/'data'/f'{cid}.json').write_bytes(raw)
        for name in ('catalog','photos','release'):
            (temp/'data'/f'{name}.json').write_text(json.dumps(index[name],ensure_ascii=False)+'\n','utf-8')
        for name in ('markets.json','fx.json'):
            if (source/'data'/name).is_file():copy(Path('data')/name)
        (temp/'.nojekyll').write_text('','utf-8')
        (temp/'runtime-mode.js').write_text("window.MG_STATIC_MODE=true;window.MG_PUBLIC_PREVIEW_ONLY=true;window.MG_CONFIG=window.MG_CONFIG||{};window.MG_CONFIG.paywall=Object.assign({},window.MG_CONFIG.paywall,{ownerPreviewOnFile:false});\n",'utf-8')
        (temp/MARKER).write_text('V19 generated public first-stage preview\n','utf-8')
        files=[p for p in temp.rglob('*') if p.is_file()]
        result={'version':19,'mode':'first-stage-preview','files':len(files),'bytes':sum(p.stat().st_size for p in files),'descriptors':count,'memberBodies':0}
        (temp/'preview-manifest.json').write_text(json.dumps(result,indent=2)+'\n','utf-8')
        if output.exists():shutil.rmtree(output)
        temp.replace(output)
        return result
    finally:
        if temp.exists():shutil.rmtree(temp)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    root=Path(__file__).resolve().parents[1]
    try:print(json.dumps(export(root/'public/academy',args.out),ensure_ascii=False))
    except (OSError,ValueError,KeyError) as error:parser.exit(1,'Export stopped: '+str(error)+'\n')

if __name__=='__main__':main()
