#!/usr/bin/env python3
"""Reproduce all 30 measured narration tracks with bounded local concurrency.

Uses installed macOS compact voices, Node Intl.Segmenter and FFmpeg. No paid
service, model download, or source movie modification. Successful unchanged
tracks resume from validated hashes. Default 3 workers; never more than 4.
Example: python3 tools/build-all-packaging-narration-v34.py --publish-assets
"""
from __future__ import annotations
import argparse
from concurrent.futures import ThreadPoolExecutor,as_completed
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import threading
import time

ROOT=Path(__file__).resolve().parents[1]
TOURS=('interposer','fanout','hybrid','bridge','chiplet','thermal')
LANGUAGES=('zh-TW','en','zh-CN','ja','ko')


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--jobs',type=int,choices=(1,2,3,4),default=3)
    p.add_argument('--out',type=Path,default=ROOT.parent/'delivery/narration-v34')
    p.add_argument('--publish-assets',action='store_true')
    a=p.parse_args();out=a.out.resolve();out.mkdir(parents=True,exist_ok=True)
    active={};lock=threading.Lock();stop=threading.Event();results=[]
    def job(item):
        tour,lang=item
        if stop.is_set():return None
        logfile=out/f'{tour}-{lang}-sentence-build.log';start=time.monotonic()
        with logfile.open('w') as log:
            with lock:
                if stop.is_set():return None
                child=subprocess.Popen([sys.executable,str(ROOT/'tools/build-native-narration-v34.py'),'--tour',tour,'--languages',lang,
                                        '--full','--bitrate','40k','--discard-wav','--out',str(out/tour)],stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
                active[child.pid]=child
            code=child.wait()
            with lock:active.pop(child.pid,None)
        return {'tour':tour,'language':lang,'exitCode':code,'seconds':round(time.monotonic()-start,2),'log':logfile.name}
    pool=ThreadPoolExecutor(max_workers=a.jobs)
    futures=[pool.submit(job,(tour,lang)) for tour in TOURS for lang in LANGUAGES]
    try:
        for future in as_completed(futures):
            row=future.result()
            if row is None:continue
            results.append(row);print(json.dumps(row),flush=True)
            status=out/'BATCH_SENTENCE_STATUS.json';tmp=status.with_suffix('.tmp')
            tmp.write_text(json.dumps({'results':results,'completeTracks':len(results),'requestedTracks':30,'workers':a.jobs},indent=2)+'\n')
            tmp.replace(status)
    except KeyboardInterrupt:
        stop.set()
        for future in futures:future.cancel()
        with lock:
            for child in active.values():
                try:os.killpg(child.pid,signal.SIGTERM)
                except ProcessLookupError:pass
        raise
    finally:pool.shutdown(wait=True,cancel_futures=True)
    if any(r['exitCode'] for r in results):
        raise SystemExit('Some tracks failed; see per-track logs. Verified tracks can be reused on the next run.')
    command=[sys.executable,str(ROOT/'tools/collect-packaging-narration-v34.py'),'--delivery',str(out)]
    if a.publish_assets:command.append('--publish-assets')
    subprocess.run(command,check=True)


if __name__=='__main__':main()
