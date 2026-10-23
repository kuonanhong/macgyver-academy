#!/usr/bin/env python3
"""Launch the local protected academy; optionally import its separate owner kit."""
import argparse, json, os, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from portable.server import Application, main as serve, read_dotenv
from portable.owner_admin import validate_verifier, provision

def main():
    read_dotenv(ROOT/'.env')
    # This entry point promises protected owner/member access. A copied V15
    # .env with COMMERCE_MODE=demo must not silently publish every lesson.
    # An intentional full demo can still use portable/server.py directly.
    os.environ['COMMERCE_MODE']='protected'
    parser=argparse.ArgumentParser(add_help=False)
    parser.add_argument('--database',type=Path,default=ROOT/'portable/data/macgyver.sqlite3')
    parser.add_argument('--public','--root',dest='public',type=Path,default=ROOT/'public/academy')
    args,_=parser.parse_known_args()
    bootstrap=ROOT/'owner-private/owner-bootstrap-v16.json'
    if not any(a in ('-h','--help') for a in sys.argv[1:]) and bootstrap.is_file():
        if bootstrap.stat().st_size>8192:raise SystemExit('Owner bootstrap is too large.')
        value=json.loads(bootstrap.read_text('utf-8'));username,_,_=validate_verifier(value)
        app=Application(args.database.resolve(),args.public.resolve(),os.environ.get('SITE_ORIGIN','http://127.0.0.1:8010'))
        with app.db() as db:
            row=db.execute('SELECT role FROM users WHERE lower(username)=?',(username,)).fetchone()
        if row is None:
            provision(app,value)
            print('管理員帳號已從私有設定建立 / Owner account imported.',flush=True)
        elif row['role']!='owner':
            raise SystemExit('Account exists without owner role. Run setup-owner-v16.sh with --bootstrap and --reset-existing to explicitly grant ownership.')
    serve()

if __name__=='__main__':main()
