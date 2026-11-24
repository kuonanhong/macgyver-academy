#!/usr/bin/env python3
"""Loopback C01 preview, bounded MP4 sink and render progress. No final-film claim."""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from threading import Lock
import argparse, hashlib, json, os, time

ROOT = Path(__file__).resolve().parents[1]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8746)
    parser.add_argument('--out', type=Path, default=ROOT.parent / 'MacGyver_Packaging_Tour_Experiment' / 'process-v34' / 'raw')
    args = parser.parse_args()
    out = args.out.resolve(); out.mkdir(parents=True, exist_ok=True)
    lock = Lock()
    state = {'state': 'ready', 'frame': 0, 'totalFrames': 7200, 'processId': 'C01', 'filmStatus': 'not_produced'}
    saved = None
    def persist():
        temp = out / 'C01.render-status.json.part'
        temp.write_text(json.dumps({**state, 'savedMaster': saved, 'updatedEpochSeconds': time.time()}, indent=2) + '\n')
        os.replace(temp, out / 'C01.render-status.json')
    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *a, **kw): super().__init__(*a, directory=str(ROOT / 'public/academy'), **kw)
        def valid_host(self): return self.headers.get('Host') in {f'127.0.0.1:{args.port}', f'localhost:{args.port}'}
        def send_json(self, status, data):
            body = json.dumps(data).encode(); self.send_response(status); self.send_header('Content-Type', 'application/json'); self.send_header('Content-Length', str(len(body))); self.send_header('Cache-Control', 'no-store'); self.end_headers(); self.wfile.write(body)
        def do_GET(self):
            if not self.valid_host(): return self.send_error(403)
            if self.path == '/__process_studio/status':
                with lock: return self.send_json(200, {'enabled': True, **state, 'savedMaster': saved})
            return super().do_GET()
        def do_POST(self):
            nonlocal saved
            if not self.valid_host() or self.headers.get('Origin', '') not in {f'http://127.0.0.1:{args.port}', f'http://localhost:{args.port}'}: return self.send_error(403)
            try: size = int(self.headers.get('Content-Length', '0'))
            except ValueError: return self.send_error(400)
            if self.path == '/__process_studio/progress':
                if self.headers.get('Content-Type') != 'application/json' or not 0 < size < 4096: return self.send_error(400)
                try:
                    update = json.loads(self.rfile.read(size))
                    if update.get('processId') != 'C01' or update.get('state') not in {'rendering','master_saved','failed','cancelled'}: raise ValueError('Invalid process state')
                    if update.get('totalFrames') != 7200 or not isinstance(update.get('frame'), int) or not 0 <= update['frame'] <= 7200: raise ValueError('Invalid frame count')
                    with lock:
                        state.update({k: update[k] for k in ('state','frame','totalFrames','processId')})
                        state['message'] = str(update.get('message', ''))[:200]; persist()
                    return self.send_json(200, {'accepted': True})
                except (ValueError, TypeError, KeyError): return self.send_error(400)
            if self.path != '/__process_studio/video/C01': return self.send_error(404)
            if self.headers.get('Content-Type') != 'video/mp4' or not 1000 < size <= 160 * 1024 * 1024: return self.send_error(400)
            temp = out / 'C01.master.mp4.part'; digest = hashlib.sha256(); remaining = size
            try:
                self.connection.settimeout(90)
                with temp.open('wb') as target:
                    first = True
                    while remaining:
                        block = self.rfile.read(min(remaining, 1024 * 1024))
                        if not block: raise ValueError('Truncated body')
                        if first and b'ftyp' not in block[:32]: raise ValueError('Not MP4')
                        first = False; target.write(block); digest.update(block); remaining -= len(block)
                os.replace(temp, out / 'C01.master.mp4')
                with lock:
                    saved = {'file': 'C01.master.mp4', 'bytes': size, 'sha256': digest.hexdigest(), 'kind': 'silent_production_master', 'finalFilmVerified': False}
                    state.update(state='master_saved', frame=7200); persist()
                print(json.dumps(saved), flush=True); self.send_json(201, saved)
            except Exception as error:
                temp.unlink(missing_ok=True); self.send_json(400, {'error': str(error)})
    server = ThreadingHTTPServer(('127.0.0.1', args.port), Handler)
    print(f'http://127.0.0.1:{args.port}/packaging-process-studio-v34.html?lang=en', flush=True)
    print(f'Progress: {out / "C01.render-status.json"}', flush=True)
    try: server.serve_forever()
    except KeyboardInterrupt: pass
    finally: server.server_close()

if __name__ == '__main__': main()
