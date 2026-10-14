#!/usr/bin/env python3
"""Explicit, resumable official GGUF downloader with pinned SHA-256. Python 3.10+."""
import argparse, hashlib, json, os, sys
from pathlib import Path
from urllib.request import Request, urlopen
ROOT=Path(__file__).resolve().parents[1]
MODELS=json.loads((ROOT/'tools/model-manifest.json').read_text())['models']
def digest(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
 return h.hexdigest()
def download(model,destination):
 destination.mkdir(parents=True,exist_ok=True)
 target=destination/model['file'];part=destination/(model['file']+'.part')
 if target.is_symlink() or part.is_symlink():raise ValueError('Refusing symbolic-link model output')
 if target.exists():
  if target.stat().st_size==model['bytes'] and digest(target)==model['sha256']:print('Verified existing model:',target);return target
  raise ValueError('Existing model does not match. Rename it before downloading; it was not overwritten.')
 offset=part.stat().st_size if part.exists() else 0
 if offset>model['bytes']:raise ValueError('Partial file too large. Remove only that .part file and retry.')
 if offset<model['bytes']:
  url=f"https://huggingface.co/{model['repo']}/resolve/{model['revision']}/{model['file']}"
  req=Request(url,headers={'User-Agent':'MacGyver-model-downloader/8','Range':f'bytes={offset}-'} if offset else {'User-Agent':'MacGyver-model-downloader/8'})
  with urlopen(req,timeout=90) as r:
   if not r.url.startswith('https://'):raise ValueError('Refusing insecure download redirect')
   if offset and r.status!=206:offset=0
   if r.status==206 and not r.headers.get('Content-Range','').startswith(f'bytes {offset}-'):raise ValueError('Unexpected resume range')
   with part.open('ab' if offset else 'wb') as f:
    while True:
     chunk=r.read(1024*1024)
     if not chunk:break
     offset+=len(chunk)
     if offset>model['bytes']:raise ValueError('Download exceeds pinned size')
     f.write(chunk);print(f'\r{offset:,} / {model["bytes"]:,} bytes ({100*offset/model["bytes"]:.1f}%)',end='',flush=True)
  print()
 if part.stat().st_size!=model['bytes'] or digest(part)!=model['sha256']:raise ValueError('Checksum mismatch. Model was NOT installed. Remove the .part file and retry.')
 os.replace(part,target);print('SHA-256 verified:',target);return target

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--model',choices=[m['id'] for m in MODELS]);p.add_argument('--download',action='store_true');p.add_argument('--list',action='store_true');p.add_argument('--directory',type=Path,default=ROOT/'models');a=p.parse_args()
 if not a.download:
  for m in MODELS:print(f"{m['id']:15} {m['bytes']/1e6:8.1f} MB  {m['license']}  {m['sourceUrl']}")
  print('No download. To consent: bash install-ai-models.sh --model qwen3-17b --download');return
 if not a.model:p.error('--download needs --model')
 model=next(m for m in MODELS if m['id']==a.model)
 if not model.get('sha256'):p.error('This model uses Ollama: bash run-ai-local.sh ' + ('--vision ' if model.get('supportsImages') else '') + '--download (explicit download; Ollama verifies its manifest).')
 download(model,a.directory.expanduser().resolve())
if __name__=='__main__':
 try:main()
 except KeyboardInterrupt:sys.exit('\nCancelled; resume by running the same command.')
 except Exception as e:sys.exit(str(e))
