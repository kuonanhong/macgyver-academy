#!/usr/bin/env python3
"""Create the public source ZIP and optional independent fallback ZIPs.

The private owner bootstrap is deliberately never packaged by this tool.
Usage: python3 tools/package-v16.py /absolute/output/folder [--parts]
"""
import argparse
import hashlib
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BLOCKED_DIRS = {'.git','.venv','venv','node_modules','__pycache__','.pytest_cache',
                'owner-private','credentials','secrets','uploads','user-data','userdata',
                'github-pages','.macgyver-state','.sites-runtime','.agents','.codex',
                '.ssh','.aws','.azure','.gnupg','gcloud','owner-kit'}
BLOCKED_FILES = {'id_rsa','id_ed25519','id_ecdsa','id_dsa','.netrc','.git-credentials',
                 '.gitconfig','credentials.json','tokens.json','token.json',
                 'cookies.txt','cookies.json','accounts.json','users.json'}

def permitted(path):
    rel = path.relative_to(ROOT)
    parts = tuple(p.casefold() for p in rel.parts)
    name = path.name.casefold()
    suffix = path.suffix.casefold()
    if any(p in BLOCKED_DIRS for p in parts): return False
    if parts[:2] == ('portable','data'): return False
    if parts[0] in ('models','local-documents') and name != 'readme.md': return False
    if name.startswith('.env') and path.name != '.env.example': return False
    if suffix in {'.pyc','.sqlite','.sqlite3','.db','.pem','.key','.p12','.pfx','.gguf','.safetensors'}: return False
    if name in BLOCKED_FILES or name.startswith(('owner-bootstrap','owner_bootstrap')): return False
    # A downloaded private kit may sit beside the extracted source. Never
    # embed that archive in the public distribution, regardless of letter case.
    if suffix in {'.zip','.tar','.gz','.tgz','.bz2','.xz','.7z'} and any(
            marker in name.replace('_','-') for marker in ('owner-private','private-owner','private-models')): return False
    if name.endswith(('-wal','-shm','.part','.tmp')): return False
    return path.is_file() and not path.is_symlink()

def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(8*1024*1024),b''): h.update(block)
    return h.hexdigest()

def archive(path, files):
    if path.is_symlink(): raise ValueError('Archive output must not be a symbolic link.')
    with zipfile.ZipFile(path,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True) as z:
        for f in files: z.write(f, f.relative_to(ROOT.parent))
    with zipfile.ZipFile(path) as z:
        bad=z.testzip()
        if bad: raise RuntimeError('ZIP CRC failure: '+bad)
    return {'filename':path.name,'bytes':path.stat().st_size,'sha256':digest(path),'files':len(files)}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('output',type=Path)
    p.add_argument('--parts',action='store_true',help='Also make four independently extractable fallback ZIPs.')
    args=p.parse_args();out=args.output.resolve()
    if out == ROOT or ROOT in out.parents:
        raise ValueError('Output must be outside the source tree.')
    report=json.loads((ROOT/'docs/VALIDATION_CURRICULUM_V16.json').read_text())
    if report.get('status') != 'PASS' or report.get('guidedCourses') != 1003:
        raise ValueError('A passing final V16 curriculum validation is required before packaging.')
    out.mkdir(parents=True,exist_ok=True)
    files=sorted(f for f in ROOT.rglob('*') if permitted(f))
    entries=[{'path':str(f.relative_to(ROOT)),'bytes':f.stat().st_size,'sha256':digest(f)} for f in files if f.name not in {'RELEASE_FILES_V16.json','SHA256SUMS'}]
    manifest=ROOT/'RELEASE_FILES_V16.json'
    if manifest.is_symlink(): raise ValueError('Release manifest must not be a symbolic link.')
    manifest.write_text(json.dumps({'version':'16.0.0','files':entries,'privateOwnerDataIncluded':False},ensure_ascii=False,indent=2)+'\n')
    files=sorted(set(files)|{manifest})
    sums=ROOT/'SHA256SUMS'
    if sums.is_symlink(): raise ValueError('Checksum output must not be a symbolic link.')
    sums.write_text(''.join(f"{digest(f)}  {f.relative_to(ROOT)}\n" for f in files if f != sums))
    files=sorted(set(files)|{sums})
    results=[archive(out/'MacGyver_Engineering_Academy_v16.zip',files)]
    if args.parts:
        # Balance uncompressed sizes; each ZIP is standard and extracts to the same root.
        bins=[[] for _ in range(4)];sizes=[0]*4
        for f in sorted(files,key=lambda x:x.stat().st_size,reverse=True):
            i=min(range(4),key=lambda j:sizes[j]);bins[i].append(f);sizes[i]+=f.stat().st_size
        assert sum(map(len,bins))==len(files)
        for i,part in enumerate(bins,1):
            results.append(archive(out/f'MacGyver_v16_Alternative_{i}_of_4.zip',sorted(part)))
    (out/'MacGyver_Engineering_Academy_v16.zip.sha256').write_text(''.join(f"{r['sha256']}  {r['filename']}\n" for r in results))
    (out/'PACKAGE_VALIDATION_V16.json').write_text(json.dumps({'status':'PASS','zipCRC':'PASS','archives':results,'publicSourceFiles':len(files),'uncompressedBytes':sum(f.stat().st_size for f in files),'privateOwnerDataIncluded':False},indent=2)+'\n')
    print(json.dumps(results))

if __name__=='__main__':main()
