#!/usr/bin/env python3
"""Test precise static-export exclusions and optionally verify an actual fresh export.

No upload. Fixture exports use a no-op offline builder; the integration run invokes
real deploy-static.sh, snapshots its source, and checks every lazy JSON/script.
"""
import argparse
import hashlib
import json
import pathlib
import subprocess
import tempfile
import unittest
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[1]
MARKER = '.macgyver-static-export'
LIMIT = 1_000_000_000
REQUIRED = ['index.html','bootstrap.js','app.bundle.js','offline-data.js',
            'offline-runtime.js','offline-build.json','app.js','style.css',
            'data/lazy/index.json','data/catalog.json','data/featured.json',
            'data/sources.json','data/photos.json']


def digest(data):
    return hashlib.sha256(data).hexdigest()


def inventory(folder):
    rows = {}
    for path in sorted(folder.rglob('*')):
        if path.is_file():
            raw = path.read_bytes()
            rows[path.relative_to(folder).as_posix()] = {
                'bytes': len(raw), 'sha256': digest(raw)
            }
    return rows


def inventory_digest(rows):
    return digest(json.dumps(rows, sort_keys=True, ensure_ascii=False,
                             separators=(',', ':')).encode())


def run_export(project, output):
    return subprocess.run(['bash', str(project/'deploy-static.sh'), '--out', str(output)],
                          cwd=project, text=True, capture_output=True)


class StaticExportFixtures(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='v15-static-fixture-')
        self.addCleanup(self.temp.cleanup)
        self.base = pathlib.Path(self.temp.name)
        self.project = self.base/'project'
        self.source = self.project/'public/academy'
        self.source.mkdir(parents=True)
        (self.project/'deploy-static.sh').write_bytes((ROOT/'deploy-static.sh').read_bytes())
        (self.project/'build-offline.sh').write_text('#!/usr/bin/env bash\nexit 0\n')
        for name in REQUIRED:
            self.put(name, ('fixture '+name+'\n').encode())
        for name in ['data/course-parts/index.json', 'data/course-parts/part-0001.json',
                     'data/lazy/courses/example.json', 'data/lazy/courses/example.js',
                     'assets/data/featured.json', 'assets/data/course-parts/keep.json',
                     'featured.json', 'course-parts/keep.json',
                     '.env.local', 'nested/.env', 'nested/key.pem']:
            self.put(name, ('fixture '+name+'\n').encode())
        self.output = self.base/'output'

    def put(self, name, data):
        path = self.source/name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return path

    def test_only_exact_rebuild_paths_omitted_source_unchanged(self):
        before = inventory(self.source)
        result = run_export(self.project, self.output)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse((self.output/'data/course-parts').exists())
        self.assertFalse((self.output/'data/featured.json').exists())
        for name in ['assets/data/featured.json','assets/data/course-parts/keep.json',
                     'featured.json','course-parts/keep.json',
                     'data/lazy/courses/example.json','data/lazy/courses/example.js',
                     'offline-data.js','offline-runtime.js','app.bundle.js']:
            self.assertEqual((self.output/name).read_bytes(), (self.source/name).read_bytes(), name)
        for name in ['.env.local','nested/.env','nested/key.pem']:
            self.assertFalse((self.output/name).exists(), 'Existing private-file filtering retained')
        self.assertEqual(inventory(self.source), before, 'Export must not remove or rewrite source files')
        self.assertTrue((self.output/MARKER).is_file())

    def test_existing_unmarked_output_preserved(self):
        self.output.mkdir()
        (self.output/'user.txt').write_bytes(b'preserve user data')
        before = inventory(self.output)
        result = run_export(self.project, self.output)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('非本腳本產生', result.stderr)
        self.assertEqual(inventory(self.output), before)

    def test_marked_output_reexport_removes_stale_generated_files(self):
        self.assertEqual(run_export(self.project, self.output).returncode, 0)
        (self.output/'stale-generated.txt').write_text('old generated file')
        self.put('app.js', b'updated runtime\n')
        result = run_export(self.project, self.output)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse((self.output/'stale-generated.txt').exists())
        self.assertEqual((self.output/'app.js').read_bytes(), b'updated runtime\n')
        self.assertTrue((self.source/'data/featured.json').exists())

    def test_source_and_ancestor_descendant_targets_refused(self):
        before = inventory(self.source)
        for output in [self.project, self.source, self.source.parent, self.source/'nested-output']:
            with self.subTest(output=output):
                result = run_export(self.project, output)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('來源的上下層', result.stderr)
        self.assertEqual(inventory(self.source), before)


def verify_actual(output, report_path):
    output = output.resolve()
    if output.exists():
        raise ValueError('Actual integration export requires a fresh output directory')
    source = ROOT/'public/academy'
    before = inventory(source)
    assert 'data/featured.json' in before
    assert any(k.startswith('data/course-parts/') for k in before)
    result = run_export(ROOT, output)
    assert result.returncode == 0, result.stdout+'\n'+result.stderr
    after = inventory(source)
    assert before == after, 'Static export changed canonical source assets'
    exported = inventory(output)
    assert not (output/'data/featured.json').exists()
    assert not (output/'data/course-parts').exists()
    total = sum(row['bytes'] for row in exported.values())
    assert total < LIMIT, f'Export {total} bytes exceeds the strict decimal 1GB budget'
    # Every retained runtime/asset file must be byte-identical, except the intended
    # static-mode switch and generated export markers. This includes every lazy JS.
    for name, row in exported.items():
        if name not in (MARKER, '.nojekyll', 'runtime-mode.js'):
            assert before[name] == row, f'Export differs from source: {name}'
    for name in ['bootstrap.js','app.bundle.js','offline-data.js','offline-runtime.js',
                 'data/lazy/index.json','data/lazy/index.compact.json']:
        assert exported[name] == before[name], name
    index = json.loads((output/'data/lazy/index.json').read_text())
    checked = []
    counts = {}
    for group in ['courses','resources','auxiliary']:
        counts[group] = len(index[group])
        for key, desc in index[group].items():
            item = {'group':group, 'id':key}
            for field in ['file','script']:
                relative = pathlib.PurePosixPath(desc[field])
                assert not relative.is_absolute() and '..' not in relative.parts
                assert relative.parts[:2] == ('data','lazy')
                name = relative.as_posix()
                assert name in exported, f'Missing lazy {field}: {name}'
                item[field] = {'path':name, **exported[name]}
                assert exported[name] == before[name], f'Changed lazy asset: {name}'
            payload = item['file']
            assert payload['bytes'] == desc['byteLength'], f'Lazy byte length mismatch: {key}'
            assert payload['sha256'] == desc['sha256'], f'Lazy checksum mismatch: {key}'
            # File-mode script also retains the matching descriptor and digest;
            # script bytes/hash are separately compared with the verified source.
            script_text = (output/desc['script']).read_text()
            assert json.dumps(desc['file']) in script_text
            assert f'sha256:"{desc["sha256"]}"' in script_text
            checked.append(item)
    removed = {name:row for name,row in before.items()
               if name == 'data/featured.json' or name.startswith('data/course-parts/')}
    report = {
        'status':'PASS', 'reviewedAt':datetime.now(timezone.utc).isoformat(),
        'command':['bash',str(ROOT/'deploy-static.sh'),'--out',str(output)],
        'validationCommand':['python3',str(ROOT/'tools/test-static-export-v15.py'),
                             '--actual-out',str(output),'--report',str(report_path)],
        'networkUpload':False, 'output':str(output), 'source':str(source),
        'deployScriptSha256':digest((ROOT/'deploy-static.sh').read_bytes()),
        'testScriptSha256':digest(pathlib.Path(__file__).read_bytes()),
        'sourceFiles':len(before), 'sourceBytes':sum(x['bytes'] for x in before.values()),
        'sourceBeforeManifestSha256':inventory_digest(before),
        'sourceAfterManifestSha256':inventory_digest(after), 'sourceUnchanged':True,
        'exportFiles':len(exported), 'exportBytes':total, 'maximumBytesExclusive':LIMIT,
        'headroomBytes':LIMIT-total, 'exportManifestSha256':inventory_digest(exported),
        'omittedExactPaths':['data/course-parts','data/featured.json'],
        'omittedSourceFilesRetained':removed,
        'omittedBytes':sum(x['bytes'] for x in removed.values()),
        'lazyDescriptorCounts':counts, 'verifiedLazyDescriptors':len(checked),
        'verifiedLazyAssets':len(checked)*2, 'lazyAssets':checked,
        'fixtureChecks':['Exact relative-path omissions preserve same names elsewhere',
                         'Canonical source bytes retained',
                         'Existing unmarked output refused without modification',
                         'Marked generated output can be regenerated',
                         'Source/ancestor/descendant output guards retained',
                         'Existing private-file ignore patterns retained'],
        'stdout':result.stdout.strip(),
        'scope':'Static export only; source and complete archives retain rebuild inputs. '
                'Every declared lazy JSON is checked against index bytes/SHA256; every '
                'offline lazy script is checked against source bytes/SHA256 and its descriptor. '
                'All retained assets except intended static-mode/marker files match source.'
    }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ['status','exportBytes','headroomBytes',
        'verifiedLazyDescriptors','verifiedLazyAssets','sourceUnchanged','exportManifestSha256']}))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--actual-out',type=pathlib.Path)
    parser.add_argument('--report',type=pathlib.Path,
                        default=ROOT/'docs/VALIDATION_STATIC_EXPORT_V15.json')
    args = parser.parse_args()
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(StaticExportFixtures)
    results = unittest.TextTestRunner(verbosity=2).run(suite)
    if not results.wasSuccessful():
        raise SystemExit(1)
    if args.actual_out:
        verify_actual(args.actual_out,args.report.resolve())


if __name__ == '__main__':
    main()
