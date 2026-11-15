#!/usr/bin/env python3
"""Confirm that the CDN serves this release and commit after Pages succeeds."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[1]


def check(value, *, commit, version, topics=None, guided=None):
    if not isinstance(value, dict) or value.get('schema') != 1:
        raise ValueError('線上尚無可驗證的版本標記。')
    if value.get('commit') != commit or value.get('version') != version:
        raise ValueError('線上版本尚未對應本次 commit / release。')
    if topics is not None and value.get('topics') != topics:
        raise ValueError('線上工程總數與本機不一致。')
    if guided is not None and value.get('guidedCourses') != guided:
        raise ValueError('線上逐步課程數與本機不一致。')
    if version.startswith('32.') and (value.get('missingCourses') or
            value.get('guidedCourses') != value.get('topics') or
            value.get('guidedByTrack', {}).get('resources', 0) < 200):
        raise ValueError('V32 課程覆蓋檢查失敗。')
    return value


def fetch(url):
    request = urllib.request.Request(url, headers={'Cache-Control': 'no-cache',
                                                   'User-Agent': 'MacGyver-Release-Verification/32'})
    with urllib.request.urlopen(request, timeout=25) as response:
        if urllib.parse.urlsplit(response.url).scheme != 'https':
            raise ValueError('版本檢查必須使用 HTTPS。')
        return response.read(32 * 1024 * 1024)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--url', default='https://kuonanhong.github.io/macgyver-academy/')
    parser.add_argument('--deployment-report', type=Path, required=True)
    parser.add_argument('--wait-seconds', type=int, default=240)
    parser.add_argument('--report', type=Path, default=ROOT / 'reports/live-verification-v32.json')
    args = parser.parse_args()
    origin = urllib.parse.urlsplit(args.url)
    if origin.scheme != 'https' or not origin.hostname or origin.username or origin.password or origin.query or origin.fragment:
        parser.error('--url must be an HTTPS site URL without credentials/query/fragment.')
    if not 0 <= args.wait_seconds <= 600:
        parser.error('--wait-seconds must be 0..600.')
    deployment = json.loads(args.deployment_report.read_text())
    commit = deployment.get('commit', '')
    if deployment.get('status') != 'success' or not re.fullmatch(r'[0-9a-f]{40}', commit):
        raise ValueError('尚未取得成功的 Pages 工作與 commit；不宣稱已上線。')
    source = json.loads((ROOT / 'SOURCE_VERSION.json').read_text())
    release = json.loads((ROOT / 'public/academy/data/release.json').read_text())
    until = time.monotonic() + args.wait_seconds
    url = args.url.rstrip('/') + '/'
    last = ''
    while True:
        try:
            value = json.loads(fetch(url + 'deployment.json?commit=' + commit))
            check(value, commit=commit, version=source['version'], topics=release['topics'], guided=release['guidedCourses'])
            raw = fetch(url + 'data/lazy/index.json?commit=' + commit)
            if hashlib.sha256(raw).hexdigest() != value['catalogSha256']:
                raise ValueError('線上課程索引與版本標記不一致，CDN 可能仍在更新。')
            result = {'status': 'PASS', 'url': url, 'commit': commit, 'deployment': value}
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
            print('已核實線上 %s：%d / %d 逐步課程；石油天然氣與採礦 %d 門。' %
                  (value['version'], value['guidedCourses'], value['topics'], value['guidedByTrack'].get('resources', 0)))
            return 0
        except (OSError, ValueError, KeyError) as error:
            last = str(error)
            if time.monotonic() >= until:
                raise ValueError('Pages 工作已完成，但線上核對未通過：' + last)
            print('等待 CDN 完成版本切換…', flush=True)
            time.sleep(min(5, max(0, until - time.monotonic())))


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (OSError, ValueError, KeyError) as error:
        print('線上核對：' + str(error), file=sys.stderr)
        sys.exit(1)
