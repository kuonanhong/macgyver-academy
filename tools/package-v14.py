#!/usr/bin/env python3
"""Create a deterministic V14 source ZIP, optional independent part ZIPs and SHA-256 list.
Run only after the release gates pass. Does not upload, deploy or include runtime secrets.
"""
from pathlib import Path
import argparse, hashlib, json, shutil, subprocess, sys, zipfile
ROOT=Path(__file__).resolve().parents[1]
NAME='MacGyver_Engineering_Academy_v14'
STAMP=(2026,10,21,0,0,0)
BLOCKED={'.git','node_modules','.next','.wrangler','__pycache__','.pytest_cache','.mypy_cache','.venv','venv','dist'}
ROOT_PRIVATE={'owner-private','models','model-cache','uploads','incoming','deliverables'}
PUBLIC_DOT_CONFIG={'.github','.openai','.gitignore','.gitattributes','.gitkeep','.npmrc','.env.example','.dockerignore','.editorconfig','.nvmrc','.eslintignore','.prettierrc','.prettierrc.json','.well-known'}

def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
 return h.hexdigest()

def permitted(p):
 rel=p.relative_to(ROOT)
 if set(rel.parts)&BLOCKED or rel.parts[0] in ROOT_PRIVATE:return False
 if any(part.startswith('.') and part not in PUBLIC_DOT_CONFIG for part in rel.parts):return False
 if rel.parts[:2]==('portable','data') and p.name not in ('README.md','.gitkeep'):return False
 if p.name in ('.DS_Store','RELEASE_FILES_V14.json','SHA256SUMS'):return False
 if p.name.startswith('.env') and p.name!='.env.example':return False
 if p.suffix.lower() in ('.pyc','.pyo','.sqlite','.sqlite3','.db','.pem','.key','.p12','.tmp','.log'):return False
 return True

def write_zip(target,files):
 with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True) as z:
  for p in files:
   name=NAME+'/'+p.relative_to(ROOT).as_posix()
   info=zipfile.ZipInfo(name,STAMP);info.compress_type=zipfile.ZIP_DEFLATED
   mode=0o755 if p.suffix=='.sh' else 0o644;info.external_attr=(0o100000|mode)<<16
   with p.open('rb') as src,z.open(info,'w',force_zip64=p.stat().st_size>=2**31) as dst:shutil.copyfileobj(src,dst,1024*1024)
 with zipfile.ZipFile(target) as z:
  bad=z.testzip()
  if bad:raise RuntimeError('ZIP CRC failure: '+bad)
 return {'file':target.name,'bytes':target.stat().st_size,'sha256':digest(target),'members':len(files)}

def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True);parser.add_argument('--parts-mib',type=int,default=40);args=parser.parse_args()
 output=args.output.resolve()
 if output==ROOT or ROOT in output.parents:raise ValueError('Output must be outside source tree')
 if not 16<=args.parts_mib<=48:raise ValueError('Part budget: 16–48 MiB')
 subprocess.run([sys.executable,str(ROOT/'tools/validate-underground-v14.py')],cwd=ROOT,check=True)
 subprocess.run([sys.executable,str(ROOT/'tools/validate-review-snapshots-v14.py')],cwd=ROOT,check=True)
 subprocess.run(['node',str(ROOT/'tools/build-offline.mjs'),'--check'],cwd=ROOT,check=True)
 report=json.loads((ROOT/'docs/VALIDATION_V14.json').read_text('utf-8'))
 if report.get('status')!='PASS':raise ValueError('Final validation report is not PASS')
 files=sorted(p for p in ROOT.rglob('*') if p.is_file() and permitted(p))
 if any(p.is_symlink() for p in files):raise ValueError('Symlinks are not packaged')
 manifest={'version':'14.0.0','date':'2026-10-21','root':NAME,'scope':'Source, HTML, original assets, lockfiles, authored curricula, generated offline/lazy data and scripts. No API keys, large model weights, account databases or owner-private notes.','files':[{'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,'sha256':digest(p)} for p in files]}
 (ROOT/'RELEASE_FILES_V14.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n','utf-8')
 files.append(ROOT/'RELEASE_FILES_V14.json');files.sort()
 (ROOT/'SHA256SUMS').write_text(''.join(f'{digest(p)}  {p.relative_to(ROOT).as_posix()}\n' for p in files),'utf-8')
 files.append(ROOT/'SHA256SUMS');files.sort();output.mkdir(parents=True,exist_ok=True)
 full=output/(NAME+'.zip');archives=[write_zip(full,files)]
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
   item=write_zip(output/f'{NAME}_part{i}of{len(groups)}.zip',group)
   if item['bytes']>=50*1024*1024:raise ValueError('Part exceeds direct-save budget')
   archives.append(item)
 (output/(NAME+'.zip.sha256')).write_text(f'{archives[0]["sha256"]}  {archives[0]["file"]}\n','utf-8')
 if len(archives)>1:
  (output/(NAME+'_parts.sha256')).write_text(''.join(f'{a["sha256"]}  {a["file"]}\n' for a in archives[1:]),'utf-8')
 (output/'V14_ARCHIVES.json').write_text(json.dumps({'archives':archives,'partInstructions':'The part ZIPs are independent archives with disjoint files. Extract all parts into the same parent folder; they recreate the same source tree. Do not concatenate the ZIPs.'},ensure_ascii=False,indent=2)+'\n','utf-8')
 print(json.dumps({'status':'PASS','archives':archives,'sourceFiles':len(files)},ensure_ascii=False))
if __name__=='__main__':main()
