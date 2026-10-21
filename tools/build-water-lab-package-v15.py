#!/usr/bin/env python3
"""Build reproducible standard-library water labs and synthetic results."""
from pathlib import Path
import subprocess, sys, zipfile
ROOT=Path(__file__).resolve().parents[1]
p=ROOT/'public/academy/assets/labs/v15'
subprocess.run([sys.executable,str(p/'run-water-labs.py'),'--check'],check=True)
subprocess.run([sys.executable,str(p/'run-water-labs.py'),'--output',str(p/'example-results.json')],check=True)
with zipfile.ZipFile(p/'water-labs-v15.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in sorted(p.iterdir()):
  if f.suffix not in ('.py','.txt','.json'):continue
  info=zipfile.ZipInfo(f.name,(2026,10,21,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16;z.writestr(info,f.read_bytes())
print('Built deterministic V15 six-lab ZIP.')
