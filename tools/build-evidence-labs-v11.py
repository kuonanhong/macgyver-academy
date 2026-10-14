#!/usr/bin/env python3
"""Validate and reproducibly package the original synthetic evidence models."""
from pathlib import Path
import hashlib,subprocess,sys,zipfile
root=Path(__file__).resolve().parents[1];folder=root/'public/academy/assets/labs/v11'
subprocess.run([sys.executable,str(folder/'run-evidence-labs.py'),'--check'],check=True,stdout=subprocess.DEVNULL)
names=['run-evidence-labs.py','synthetic-cases.json','README_ZH.txt','README_EN.txt']
(folder/'SHA256SUMS.txt').write_text(''.join(hashlib.sha256((folder/name).read_bytes()).hexdigest()+'  '+name+'\n' for name in names))
target=folder/'MacGyver_V11_Synthetic_Labs.zip';temp=target.with_suffix('.zip.tmp')
with zipfile.ZipFile(temp,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for name in names+['SHA256SUMS.txt']:
        info=zipfile.ZipInfo('MacGyver_V11_Synthetic_Labs/'+name,(2026,10,14,0,0,0));info.create_system=3;info.external_attr=0o100644<<16;info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,(folder/name).read_bytes())
with zipfile.ZipFile(temp) as z:assert z.testzip() is None
temp.replace(target)
print('Twelve checked synthetic mini labs packaged reproducibly.')
