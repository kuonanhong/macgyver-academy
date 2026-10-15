#!/usr/bin/env python3
"""Upload paid course stages (stage index >= FREE_STAGES) to Supabase table
public.course_content, readable only by members with an active pass (RLS in
supabase/002_accounts_commerce.sql). Run on the OWNER's computer only:

  export SUPABASE_URL=https://<project>.supabase.co
  export SUPABASE_SERVICE_ROLE_KEY=...        # never commit or put in the website
  python3 tools/paywall-v12/upload_protected_content.py [--dry-run] [--free-stages 1]

Afterwards publish the website with paid stages removed:
  PROTECT_CONTENT=1 bash macgyver.sh deploy    (static site only, stages stubbed)
"""
import argparse, hashlib, json, os, sys, urllib.request
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--free-stages', type=int, default=1)
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--batch-bytes', type=int, default=4_000_000)
    a = ap.parse_args()
    featured = json.loads((ROOT / 'public/academy/data/featured.json').read_text('utf-8'))
    rows = []
    for c in featured:
        for i, stage in enumerate(c.get('stages', [])):
            if i < a.free_stages:
                continue
            raw = json.dumps(stage, ensure_ascii=False, separators=(',', ':'))
            rows.append({'course_id': c['id'], 'stage_index': i, 'revision': hashlib.sha256(raw.encode()).hexdigest(), 'payload': stage})
    total = sum(len(json.dumps(r, ensure_ascii=False)) for r in rows)
    print(f'{len(rows)} paid stages from {len(featured)} courses, {total/1024/1024:.1f} MiB')
    if a.dry_run:
        return 0
    url, key = os.environ.get('SUPABASE_URL', '').rstrip('/'), os.environ.get('SUPABASE_SERVICE_ROLE_KEY', '')
    if not url.startswith('https://') or not key:
        sys.exit('Set SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY (owner computer only).')
    batch, size, sent = [], 0, 0
    def flush():
        nonlocal batch, size, sent
        if not batch:
            return
        req = urllib.request.Request(url + '/rest/v1/course_content?on_conflict=course_id,stage_index', method='POST',
                                     data=json.dumps(batch, ensure_ascii=False).encode(),
                                     headers={'apikey': key, 'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json',
                                              'Prefer': 'resolution=merge-duplicates,return=minimal'})
        with urllib.request.urlopen(req, timeout=120) as r:
            if r.status not in (200, 201, 204):
                sys.exit(f'Upload failed: HTTP {r.status}')
        sent += len(batch); print(f'  uploaded {sent}/{len(rows)}', flush=True)
        batch, size = [], 0
    for r in rows:
        n = len(json.dumps(r, ensure_ascii=False).encode())
        if batch and size + n > a.batch_bytes:
            flush()
        batch.append(r); size += n
    flush()
    print('Done. Members with an active pass can now load paid stages from Supabase.')
    return 0

if __name__ == '__main__':
    sys.exit(main())
