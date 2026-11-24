#!/usr/bin/env python3
"""Remote assets may be omitted only when every local copy matches a verified release."""
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
spec=importlib.util.spec_from_file_location('exporter',Path(__file__).with_name('export-preview-v21.py'))
exporter=importlib.util.module_from_spec(spec);spec.loader.exec_module(exporter)

class HostingTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
        self.base=self.root/'assets/packaging-tour-v33/videos';self.base.mkdir(parents=True)
        self.policy={'status':'verified','tag':'packaging-tours-v33.0.3','videos':{}}
        for name in ('interposer','fanout','hybrid','bridge','chiplet','thermal'):
            raw=('verified film '+name).encode();(self.base/(name+'.mp4')).write_bytes(raw)
            self.policy['videos'][name]={'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'url':'https://github.com/kuonanhong/macgyver-academy/releases/download/packaging-tours-v33.0.3/'+name+'.mp4'}
    def write(self):
        (self.base/'hosting.json').write_text(json.dumps(self.policy))
    def test_no_policy_keeps_local_films(self):
        self.assertEqual(exporter.remote_packaging_videos(self.root),set())
    def test_all_verified_copies_can_be_omitted(self):
        self.write();self.assertEqual(len(exporter.remote_packaging_videos(self.root)),6)
    def test_changed_film_is_never_silently_removed(self):
        self.write();(self.base/'hybrid.mp4').write_bytes(b'new film')
        with self.assertRaises(ValueError):exporter.remote_packaging_videos(self.root)
    def test_missing_upload_cannot_enable_omission(self):
        self.policy['status']='pending';self.write()
        with self.assertRaises(ValueError):exporter.remote_packaging_videos(self.root)
    def test_other_account_is_not_accepted(self):
        self.policy['videos']['interposer']['url']='https://github.com/other/repo/releases/download/tag/interposer.mp4';self.write()
        with self.assertRaises(ValueError):exporter.remote_packaging_videos(self.root)

if __name__=='__main__':unittest.main()
