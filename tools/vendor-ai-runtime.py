#!/usr/bin/env python3
"""Restore exactly the pinned wllama runtime; verify package and extracted file hashes."""
import base64,hashlib,io,json,tarfile,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]/'public/academy/vendor/wllama'
lock=json.loads((ROOT/'LOCK.json').read_text())
paths={'main':{'package/esm/index.min.js':'index.js','package/esm/wasm/wllama.wasm':'wllama.wasm','package/LICENCE':'LICENSE.txt'},'compat':{'package/wasm/wllama.js':'compat.js','package/wasm/wllama.wasm':'compat.wasm'}}
for name,package in lock['packages'].items():
 url=package['url']
 if not url.startswith('https://registry.npmjs.org/@wllama/'):raise ValueError('Unexpected package source')
 with urllib.request.urlopen(url,timeout=60) as response:data=response.read(50*1024*1024)
 actual='sha512-'+base64.b64encode(hashlib.sha512(data).digest()).decode()
 if actual!=package['integrity']:raise ValueError('Package checksum mismatch')
 with tarfile.open(fileobj=io.BytesIO(data),mode='r:gz') as archive:
  for source,target in paths[name].items():
   content=archive.extractfile(source).read()
   if hashlib.sha256(content).hexdigest()!=lock['files'][target]:raise ValueError('File checksum mismatch: '+target)
   temporary=ROOT/(target+'.tmp');temporary.write_bytes(content);temporary.replace(ROOT/target)
print('Pinned wllama 3.8.1 + compatibility runtime verified.')
