"""Exercise private-document boundaries without invoking any network transfer."""
import os
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


class UploadWrapperTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name)
        self.root = self.base / 'project with spaces'
        self.root.mkdir()
        shutil.copy(Path(__file__).resolve().parents[1] / 'update-and-upload.sh', self.root)
        for name in ('publish-github.sh', 'index-documents.sh', 'build-offline.sh'):
            (self.root / name).write_text('#!/usr/bin/env bash\nprintf "%s\\n" "$@" >> "$TEST_CALLS"\n')
        self.calls = self.base / 'calls.txt'
        self.bin = self.base / 'bin'
        self.bin.mkdir()
        self.remote_calls = self.base / 'remote-calls.jsonl'
        (self.bin / 'rclone').write_text('#!/usr/bin/env python3\nimport sys,os,json\nwith open(os.environ["TEST_REMOTE_CALLS"],"a") as f:f.write(json.dumps(sys.argv[1:])+"\\n")\nsys.exit(int(os.environ.get("TEST_REMOTE_FAIL","0")))\n')
        (self.bin / 'rclone').chmod(0o755)
        self.env = dict(os.environ, TEST_CALLS=str(self.calls), TEST_REMOTE_CALLS=str(self.remote_calls), PATH=str(self.bin)+os.pathsep+os.environ['PATH'])

    def tearDown(self):
        self.temp.cleanup()

    def run_wrapper(self, source, index=True, extra=None):
        return subprocess.run(['bash', str(self.root / 'update-and-upload.sh'), '--repo',
                               'https://github.com/example/academy.git',
                               '--documents', str(source)] + (['--index-documents'] if index else []) + (extra or []), env=self.env, capture_output=True, text=True)

    def test_custom_in_repo_documents_rejected_before_any_upload(self):
        source = self.root / 'private-course'
        source.mkdir()
        (source / 'lesson.txt').write_text('Private course text')
        for index in (False, True):
            with self.subTest(index=index):
                result = self.run_wrapper(source, index=index)
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse(self.calls.exists())

    def test_external_documents_keep_path_as_one_argument(self):
        source = self.base / 'private course outside'
        source.mkdir()
        result = self.run_wrapper(source)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.calls.read_text().splitlines(), ['--if-needed', '--source', str(source), '--repo', 'https://github.com/example/academy.git', '--dry-run', '--repo', 'https://github.com/example/academy.git', '--push'])

    def test_failed_offline_build_stops_before_index_or_upload(self):
        source = self.base / 'private course outside'
        source.mkdir()
        (self.root / 'build-offline.sh').write_text('#!/usr/bin/env bash\nexit 17\n')
        result = self.run_wrapper(source)
        self.assertEqual(result.returncode, 17)
        self.assertFalse(self.calls.exists())

    def test_tracked_default_documents_rejected(self):
        source = self.root / 'local-documents'
        source.mkdir()
        (source / 'lesson.txt').write_text('Private course text')
        subprocess.run(['git','init','-q',str(self.root)], check=True)
        subprocess.run(['git','-C',str(self.root),'add','local-documents'], check=True)
        for index in (False, True):
            with self.subTest(index=index):
                result = self.run_wrapper(source, index=index)
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse(self.calls.exists())

    def test_model_backup_is_explicit_and_excludes_partial_files(self):
        source = self.base / 'outside'; source.mkdir()
        (self.root / 'models').mkdir()
        result = self.run_wrapper(source, index=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(self.remote_calls.exists())
        result = self.run_wrapper(source, index=False, extra=['--models-remote','cloud:weights with spaces'])
        self.assertEqual(result.returncode, 0, result.stderr)
        calls = [json.loads(line) for line in self.remote_calls.read_text().splitlines()]
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0][:3], ['copy', str(self.root/'models'), 'cloud:weights with spaces'])
        self.assertIn('*.part', calls[0]); self.assertIn('*.tmp', calls[0]); self.assertIn('*.partial', calls[0])
        self.assertIn('.incomplete/**', calls[0]); self.assertNotIn('sync', calls[0])
        self.assertNotIn('--models-remote', self.calls.read_text())

    def test_snapshot_failure_stops_all_backups(self):
        source = self.base / 'outside'; source.mkdir(); (self.root/'models').mkdir()
        (self.root / 'publish-github.sh').write_text('#!/usr/bin/env bash\nexit 23\n')
        result = self.run_wrapper(source, index=False, extra=['--models-remote','cloud:weights','--documents-remote','cloud:private'])
        self.assertEqual(result.returncode,23)
        self.assertFalse(self.remote_calls.exists())

    def test_backup_failure_stops_git_push(self):
        source = self.base / 'outside'; source.mkdir(); (self.root/'models').mkdir()
        self.env['TEST_REMOTE_FAIL']='24'
        result = self.run_wrapper(source, index=False, extra=['--models-remote','cloud:weights'])
        self.assertEqual(result.returncode,24)
        self.assertIn('--dry-run',self.calls.read_text());self.assertNotIn('--push',self.calls.read_text())

    def test_original_origin_unchanged_and_invalid_branch_rejected(self):
        source = self.base / 'outside'; source.mkdir()
        subprocess.run(['git','init','-q',str(self.root)],check=True)
        subprocess.run(['git','-C',str(self.root),'remote','add','origin','https://git.chatgpt-team.site/example/academy'],check=True)
        result=self.run_wrapper(source,index=False)
        self.assertEqual(result.returncode,0,result.stderr)
        origin=subprocess.check_output(['git','-C',str(self.root),'remote','get-url','origin'],text=True).strip()
        self.assertEqual(origin,'https://git.chatgpt-team.site/example/academy')
        self.calls.unlink()
        result=self.run_wrapper(source,index=False,extra=['--branch','-invalid'])
        self.assertNotEqual(result.returncode,0);self.assertFalse(self.calls.exists())


if __name__ == '__main__':
    unittest.main()
