#!/usr/bin/env python3
"""Create a deterministic V15 source ZIP, optional independent part ZIPs and SHA-256 list.
Run only after the release gates pass. Does not upload, deploy or include runtime secrets.
"""
from pathlib import Path
import argparse, hashlib, json, shutil, subprocess, sys, zipfile
ROOT=Path(__file__).resolve().parents[1]
NAME='MacGyver_Engineering_Academy_v15'
STAMP=(2026,10,21,0,0,0)
BLOCKED={'.git','node_modules','.next','.wrangler','__pycache__','.pytest_cache','.mypy_cache','.venv','venv','dist'}
ROOT_PRIVATE={'owner-private','local-documents','models','model-cache','uploads','incoming','deliverables'}
PRIVATE_DIRS={'owner-private','local-documents','credentials','secrets','userdata','user-data','uploads','models','model-cache'}
PRIVATE_SUFFIXES={'.gguf','.safetensors','.ckpt','.pt','.pth','.onnx','.bin','.pem','.key','.p12','.pfx'}
PUBLIC_DOT_CONFIG={'.github','.openai','.gitignore','.gitattributes','.gitkeep','.npmrc','.env.example','.dockerignore','.editorconfig','.nvmrc','.eslintignore','.prettierrc','.prettierrc.json','.well-known'}

def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
 return h.hexdigest()

def permitted(p):
 rel=p.relative_to(ROOT)
 if set(rel.parts)&BLOCKED or set(rel.parts[:-1])&PRIVATE_DIRS or rel.parts[0] in ROOT_PRIVATE:return False
 if any(part.startswith('.') and part not in PUBLIC_DOT_CONFIG for part in rel.parts):return False
 if '.openai' in rel.parts and rel.as_posix()!='.openai/hosting.json':return False
 if rel.as_posix()=='SHA256SUMS.txt':return False
 if rel.parts[:2]==('portable','data') and rel.as_posix() not in ('portable/data/README.md','portable/data/.gitkeep'):return False
 if p.name in ('.DS_Store','RELEASE_FILES_V15.json','SHA256SUMS','id_rsa','id_ed25519'):return False
 if p.name.startswith('.env') and p.name!='.env.example':return False
 if p.suffix.lower() in PRIVATE_SUFFIXES|{'.pyc','.pyo','.sqlite','.sqlite3','.db','.tmp','.log'} or '.sqlite' in p.name:return False
 return True

def write_zip(target,files,expected):
 with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True) as z:
  for p in files:
   name=NAME+'/'+p.relative_to(ROOT).as_posix()
   info=zipfile.ZipInfo(name,STAMP);info.compress_type=zipfile.ZIP_DEFLATED
   mode=0o755 if p.suffix in ('.sh','.command') else 0o644;info.external_attr=(0o100000|mode)<<16
   checked=hashlib.sha256()
   with p.open('rb') as src,z.open(info,'w',force_zip64=p.stat().st_size>=2**31) as dst:
    for block in iter(lambda:src.read(1024*1024),b''):
     checked.update(block);dst.write(block)
   if checked.hexdigest()!=expected[p.relative_to(ROOT).as_posix()]:raise ValueError('Source changed during packaging: '+str(p.relative_to(ROOT)))
 with zipfile.ZipFile(target) as z:
  bad=z.testzip()
  if bad:raise RuntimeError('ZIP CRC failure: '+bad)
 return {'file':target.name,'bytes':target.stat().st_size,'sha256':digest(target),'members':len(files)}

def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True);parser.add_argument('--parts-mib',type=int,default=40);args=parser.parse_args()
 output=args.output.resolve()
 if output==ROOT or ROOT in output.parents:raise ValueError('Output must be outside source tree')
 if not 16<=args.parts_mib<=48:raise ValueError('Part budget: 16–48 MiB')
 existing=list(output.glob(NAME+'*.zip'))+[p for p in (output/(NAME+'.zip.sha256'),output/(NAME+'_parts.sha256'),output/'V15_ARCHIVES.json') if p.exists()]
 if existing:raise ValueError('Release archives already exist; use a new output directory to avoid mixing old parts.')
 subprocess.run([sys.executable,str(ROOT/'tools/validate-water-v15.py')],cwd=ROOT,check=True)
 subprocess.run([sys.executable,str(ROOT/'tools/validate-review-snapshots-v15.py')],cwd=ROOT,check=True)
 subprocess.run(['node',str(ROOT/'tools/build-offline.mjs'),'--check'],cwd=ROOT,check=True)
 report=json.loads((ROOT/'docs/VALIDATION_V15.json').read_text('utf-8'))
 if report.get('status')!='PASS':raise ValueError('Final validation report is not PASS')
 files=sorted(p for p in ROOT.rglob('*') if p.is_file() and permitted(p))
 if any(p.is_symlink() for p in files):raise ValueError('Symlinks are not packaged')
 manifest={'version':'15.0.0','date':'2026-10-21','root':NAME,'scope':'Source, HTML, original assets, lockfiles, authored curricula, generated offline/lazy data and scripts. No API keys, large model weights, account databases or owner-private notes.','files':[{'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,'sha256':digest(p)} for p in files]}
 (ROOT/'RELEASE_FILES_V15.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n','utf-8')
 files.append(ROOT/'RELEASE_FILES_V15.json');files.sort()
 (ROOT/'SHA256SUMS').write_text(''.join(f'{digest(p)}  {p.relative_to(ROOT).as_posix()}\n' for p in files),'utf-8')
 files.append(ROOT/'SHA256SUMS');files.sort();output.mkdir(parents=True,exist_ok=True)
 expected={row['path']:row['sha256'] for row in manifest['files']}
 expected['RELEASE_FILES_V15.json']=digest(ROOT/'RELEASE_FILES_V15.json');expected['SHA256SUMS']=digest(ROOT/'SHA256SUMS')
 full=output/(NAME+'.zip');archives=[write_zip(full,files,expected)]
 with zipfile.ZipFile(full) as z:sizes={item.filename:item.compress_size+2*len(item.filename.encode())+200 for item in z.infolist()}
 budget=args.parts_mib*1024*1024;groups=[];group=[];size=0
 for p in files:
  cost=sizes[NAME+'/'+p.relative_to(ROOT).as_posix()]
  if cost>budget:raise ValueError('One compressed member exceeds part budget: '+str(p.relative_to(ROOT)))
  if group and size+cost>budget:groups.append(group);group=[];size=0
  group.append(p);size+=cost
 if group:groups.append(group)
 if len(groups)>1:
  for i,group in enumerate(groups,1):
   item=write_zip(output/f'{NAME}_part{i}of{len(groups)}.zip',group,expected)
   if item['bytes']>=50*1024*1024:raise ValueError('Part exceeds direct-save budget')
   archives.append(item)
 (output/(NAME+'.zip.sha256')).write_text(f'{archives[0]["sha256"]}  {archives[0]["file"]}\n','utf-8')
 if len(archives)>1:
  (output/(NAME+'_parts.sha256')).write_text(''.join(f'{a["sha256"]}  {a["file"]}\n' for a in archives[1:]),'utf-8')
 (output/'V15_ARCHIVES.json').write_text(json.dumps({'archives':archives,'partInstructions':'The part ZIPs are independent archives with disjoint files. Extract all parts into the same parent folder; they recreate the same source tree. Do not concatenate the ZIPs.'},ensure_ascii=False,indent=2)+'\n','utf-8')
 print(json.dumps({'status':'PASS','archives':archives,'sourceFiles':len(files)},ensure_ascii=False))
if __name__=='__main__':main()
