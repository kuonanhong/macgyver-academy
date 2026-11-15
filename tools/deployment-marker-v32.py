#!/usr/bin/env python3
"""Record the exact public artifact, never credentials or owner lesson bodies."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess


def marker(root, commit=''):
    raw = (root / 'data/lazy/index.json').read_bytes()
    index = json.loads(raw)
    release = index['release']
    catalog = index['catalog']
    guided = set(index['guidedIds'])
    counts = subprocess.run(['node', str(Path(__file__).with_name('count-learning-tracks-v32.mjs')),
                             str(root / 'data/lazy/index.json')], capture_output=True, text=True, check=True)
    return {
        'schema': 1,
        'version': release['version'],
        'commit': commit if re.fullmatch(r'[0-9a-f]{40}', commit) else None,
        'builtAt': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'topics': len(catalog),
        'guidedCourses': len(guided),
        'missingCourses': [c['id'] for c in catalog if c['id'] not in guided],
        'guidedByCategory': {category: sum(c['category'] == category and c['id'] in guided for c in catalog)
                            for category in sorted({c['category'] for c in catalog})},
        'guidedByTrack': json.loads(counts.stdout),
        'catalogSha256': hashlib.sha256(raw).hexdigest(),
        'mode': 'first-stage-preview',
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    args = parser.parse_args()
    value = marker(args.directory, os.environ.get('GITHUB_SHA', ''))
    (args.directory / 'deployment.json').write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
    print('Public artifact: %s · %d / %d guided courses' %
          (value['version'], value['guidedCourses'], value['topics']))
