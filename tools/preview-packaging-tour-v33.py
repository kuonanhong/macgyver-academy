#!/usr/bin/env python3
"""Loopback-only preview and bounded MP4 production sink for the tour studio."""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlsplit
import argparse, hashlib, json, os, re

ROOT = Path(__file__).resolve().parents[1]
IDS = {'interposer','fanout','hybrid','bridge','chiplet','thermal'}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--port',type=int,default=8733)
    parser.add_argument('--out',type=Path,default=ROOT.parent/'MacGyver_Packaging_Tour_Experiment'/'recordings')
    args=parser.parse_args(); out=args.out.resolve();out.mkdir(parents=True,exist_ok=True)
    class Handler(SimpleHTTPRequestHandler):
        def __init__(self,*a,**kw):super().__init__(*a,directory=str(ROOT/'public/academy'),**kw)
        def send_head(self):
            self.range_remaining=None
            path=Path(self.translate_path(self.path))
            if path.suffix.lower()!='.mp4' or not path.is_file():return super().send_head()
            if not path.resolve().is_relative_to((ROOT/'public/academy').resolve()):
                self.send_error(403);return None
            size=path.stat().st_size;start=0;end=size-1;status=200
            header=self.headers.get('Range')
            if header:
                match=re.fullmatch(r'bytes=(\d*)-(\d*)',header)
                if not match or not (match[1] or match[2]):
                    self.send_error(416);return None
                if match[1]:
                    start=int(match[1]);end=min(end,int(match[2])) if match[2] else end
                else:start=max(0,size-int(match[2]))
                if start>=size or start>end:
                    self.send_response(416);self.send_header('Content-Range',f'bytes */{size}');self.send_header('Content-Length','0');self.end_headers();return None
                status=206
            source=path.open('rb');source.seek(start);self.range_remaining=end-start+1
            self.send_response(status);self.send_header('Content-Type','video/mp4');self.send_header('Accept-Ranges','bytes');self.send_header('Content-Length',str(self.range_remaining))
            if status==206:self.send_header('Content-Range',f'bytes {start}-{end}/{size}')
            self.end_headers();return source
        def copyfile(self,source,outputfile):
            if getattr(self,'range_remaining',None) is None:return super().copyfile(source,outputfile)
            remaining=self.range_remaining
            try:
                while remaining:
                    block=source.read(min(1024*1024,remaining))
                    if not block:break
                    outputfile.write(block);remaining-=len(block)
            except (BrokenPipeError,ConnectionResetError):pass
        def send_json(self,status,data):
            body=json.dumps(data).encode();self.send_response(status);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(body)));self.send_header('Cache-Control','no-store');self.end_headers();self.wfile.write(body)
        def valid_host(self):
            return self.headers.get('Host') in {f'127.0.0.1:{args.port}',f'localhost:{args.port}'}
        def do_GET(self):
            if not self.valid_host():return self.send_error(403)
            if self.path=='/__tour_studio/status':return self.send_json(200,{'enabled':True,'tourIds':sorted(IDS)})
            return super().do_GET()
        def do_POST(self):
            origin=self.headers.get('Origin','')
            if not self.valid_host() or origin not in {f'http://127.0.0.1:{args.port}',f'http://localhost:{args.port}'}:return self.send_error(403)
            match=re.fullmatch(r'/__tour_studio/video/([a-z]+)',self.path)
            if not match or match[1] not in IDS:return self.send_error(404)
            try:size=int(self.headers.get('Content-Length','0'))
            except ValueError:return self.send_error(400)
            if self.headers.get('Content-Type')!='video/mp4' or not 1000<size<=160*1024*1024:return self.send_error(400)
            temp=out/(match[1]+'.mp4.part');digest=hashlib.sha256();remaining=size
            try:
                self.connection.settimeout(90)
                with temp.open('wb') as f:
                    first=True
                    while remaining:
                        block=self.rfile.read(min(remaining,1024*1024))
                        if not block:raise ValueError('Truncated body')
                        if first and b'ftyp' not in block[:32]:raise ValueError('Not MP4')
                        first=False;f.write(block);digest.update(block);remaining-=len(block)
                os.replace(temp,out/(match[1]+'.mp4'))
                print(json.dumps({'saved':match[1]+'.mp4','bytes':size,'sha256':digest.hexdigest()}),flush=True)
                self.send_json(201,{'saved':match[1]+'.mp4','bytes':size})
            except Exception as error:
                temp.unlink(missing_ok=True);self.send_json(400,{'error':str(error)})
    server=ThreadingHTTPServer(('127.0.0.1',args.port),Handler)
    print(f'http://127.0.0.1:{args.port}/packaging-tour-v33.html',flush=True)
    try:server.serve_forever()
    except KeyboardInterrupt:pass
    finally:server.server_close()

if __name__=='__main__':main()
