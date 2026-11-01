#!/usr/bin/env python3
"""Real local Git fixtures; never contacts GitHub or changes global user config."""
from __future__ import annotations
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest import mock
from urllib.error import HTTPError, URLError
import zipfile

SOURCE = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('v21_upload_under_test', Path(__file__).with_name('upload.py'))
u = importlib.util.module_from_spec(spec)
spec.loader.exec_module(u)


def cmd(*args, cwd=None, env=None):
    return subprocess.run(list(args), cwd=cwd, env=env, check=True, capture_output=True, text=True).stdout.strip()


class UploadTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='macgyver-v21-upload-test-')
        self.base = Path(self.tmp.name)
        self.source = self.base / 'V21 source with spaces'
        self.source.mkdir()
        for name in ('macgyver.sh', 'upload-all.sh', 'Upload_MacGyver_v21_SSH.sh', 'tools/upload-v21/upload.py', 'tools/upload-v21/site_sync.py', 'tools/upload-v21/public_transport.py', 'tools/export-preview-v21.py', 'deploy-static.sh', 'tools/sync-v12/sync_github.py', 'tools/sync-v13/models_sync.py', 'tools/export_github.py', 'tools/model-manifest.json'):
            target = self.source / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(SOURCE / name, target)
        for name, data in {'index.html': 'V21 entry', 'public/academy/index.html': 'V21 home', 'public/academy/app.bundle.js': 'console.log(16)', 'publish-github.sh': '#!/bin/bash\n', '.github/workflows/pages.yml': 'name: fixture\n', '.gitignore': '*.gguf\n', 'owner-private/bootstrap.json': '{"owner":"PRIVATE-ONLY"}', 'portable/data/accounts.json': '{"account":"PRIVATE-ONLY"}'}.items():
            p = self.source / name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(data)
        self.make_preview_fixture()
        config = self.base / 'gitconfig'
        config.write_text('[user]\nname = Upload Fixture\nemail = fixture@example.invalid\n[init]\ndefaultBranch = main\n')
        self.site = self.base / 'site.git'
        self.private = self.base / 'private.git'
        self.state = self.base / 'upload-state'
        self.env = dict(os.environ, GIT_CONFIG_GLOBAL=str(config), GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_COUNT='0',
                        MACGYVER_UPLOAD_V21_TEST='1', MACGYVER_UPLOAD_V21_TEST_SITE=self.site.as_uri(),
                        MACGYVER_UPLOAD_V21_TEST_PRIVATE=self.private.as_uri(), MACGYVER_MODELS_TEST_REMOTE='1',
                        MACGYVER_MODELS_TEST_CHUNK_BYTES='16')
        for path in (self.site, self.private):
            cmd('git', 'init', '--bare', str(path), env=self.env)
            seed = self.base / (path.stem + '-seed')
            cmd('git', 'clone', str(path), str(seed), env=self.env)
            (seed / 'remote-only.txt').write_text('keep me')
            cmd('git', 'add', 'remote-only.txt', cwd=seed, env=self.env)
            cmd('git', 'commit', '-m', 'seed', cwd=seed, env=self.env)
            cmd('git', 'push', 'origin', 'main', cwd=seed, env=self.env)


    def make_preview_fixture(self):
        import hashlib
        root = self.source / 'public/academy'
        loader = importlib.util.spec_from_file_location('fixture_preview', self.source / 'tools/export-preview-v21.py')
        exporter = importlib.util.module_from_spec(loader)
        loader.loader.exec_module(exporter)
        metadata = {'id':'test','title':'Test','titleEn':'Test','category':'aerospace','_lazy':True,
                    'stages':[{'id':'s1','title':'Free','titleEn':'Free','order':1,'steps':[{'id':'free1'}]},
                              {'id':'s2','title':'Member','titleEn':'Member','order':2,'steps':[{'id':'paid1'}]}]}
        course = {**metadata, 'previewOnly':True,'freeStagesPerCourse':1,
                  'stages':[{'id':'s1','title':'Free','titleEn':'Free','order':1,
                             'steps':[{'id':'free1','instruction':'PUBLIC-LESSON'}]},
                            {'id':'s2','title':'Member','titleEn':'Member','order':2,
                             'steps':[{'id':'paid1','locked':True,'knowledge':[],
                                       'quiz':{'question':'','questionEn':'','options':[],'optionsEn':[],'answer':0}}]}]}
        def descriptor(group, identifier, value):
            raw=(json.dumps(value,ensure_ascii=False)+'\n').encode()
            sha=hashlib.sha256(raw).hexdigest()
            file=f'data/lazy/{group}/{identifier}-{sha[:16]}.json'
            record={'file':file,'script':file[:-5]+'.js','sha256':sha,'byteLength':len(raw)}
            path=root/file; path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(raw)
            (root/record['script']).write_bytes(exporter.bound_script(record,raw))
            return record
        index={'lazyVersion':1,'catalog':[metadata],'guidedIds':['test'],'photos':[],
               'release':{'version':'21.0.0'},'courses':{'test':descriptor('courses','test',course)},
               'resources':{'test':descriptor('resources','test',{'media':{'courses':[]}})},'auxiliary':{}}
        (root/'data/lazy/index.json').write_text(json.dumps(index))
        (root/'data/lazy/index.compact.json').write_text(json.dumps(exporter.compact_index(index)))
        (root/'data/lazy/owner-courses').mkdir()
        (root/'data/lazy/owner-courses/private.json').write_text('MEMBER-LESSON-SECRET')
        (root/'data/featured.json').write_text('MEMBER-LESSON-SECRET')
        (self.source/'tools/environment-v17/inputs').mkdir(parents=True)
        (self.source/'tools/environment-v17/inputs/private.json').write_text('MEMBER-LESSON-SECRET')
        for name in ('aviation-v18', 'marine-v19'):
            folder = self.source / 'tools' / name / 'inputs'
            folder.mkdir(parents=True)
            (folder / 'private.json').write_text('MEMBER-LESSON-SECRET')
        (root/'campaign.html').write_text('<main>Original V21 game</main>')
        (root/'campaign-core.js').write_text('/* Original V21 game code */')
        (root/'campaign.css').write_text('main { color: #123; }')
        (root/'data/campaigns-v20.json').write_text(json.dumps({'version':20,'campaigns':[
            {'id':'fixture-game','category':'semiconductor','title':'Original teaching game',
             'courseIds':['test'],'missions':[{'id':'inspect','brief':'Original inspection task'}]}]}))
        (root/'data/campaigns-v20.js').write_text('throw new Error("Do not copy source wrappers");')
        (root/'data/campaign-index-v20.json').write_text(json.dumps({'version':20,'courses':{'test':['fixture-game']}}))
        (root/'data/campaign-media-v20.json').write_text(json.dumps({'version':20,'photos':[]}))
        (root/'data/campaigns-semiconductor-v20.json').write_text('AUTHOR-INTERMEDIATE-ONLY')
        (root/'data/course-missions-v20.json').write_text('MEMBER-LESSON-SECRET')
        (root/'experience.html').write_text('<main>Full window engineering journey</main>')
        (root/'experience-v21.js').write_text('/* public viewer */')
        (root/'experience-v21.css').write_text('main {position:fixed;inset:0}')
        (root/'data/experiences-v21.json').write_text(json.dumps({
            'version':21,'domains':[{'id':'automotive','title':'汽車'}], 'assets':[],
            'experiences':[{'id':'car-journey','category':'automotive','courseId':'test',
                'title':'A vehicle journey','roles':[], 'assetIds':[], 'equipment':[],
                'chapters':[{'id':'assembly','title':'Assembly',
                    'description':'Public original story', 'task':'Observe',
                    'roleTasks':{'inspector':{'task':'Check assembly evidence','taskEn':'Check assembly evidence'}},
                    'observations':[], 'choices':[{'id':'test','title':'Test before release',
                        'roleOutcomes':{'inspector':{'outcome':'Check complete','outcomeEn':'Check complete'}}}]}]}]}))
        (root/'data/experiences-v21.js').write_text('throw new Error("Source wrapper must be rebuilt");')

    def test_v21_and_v22_source_markers_set_public_readme_and_keep_preview_policy(self):
        for major in ('21', '22'):
            (self.source / 'SOURCE_VERSION.json').write_text(json.dumps({'version': major + '.0.0'}))
            self.run_upload('--skip-models', '--skip-documents')
            marker = json.loads(self.show(self.site, 'SOURCE_VERSION.json'))
            self.assertEqual(marker['version'], major + '.0.0')
            self.assertIn('Academy V' + major, self.show(self.site, 'README.md'))
            names = cmd('git', '--git-dir', str(self.site), 'ls-tree', '-r', '--name-only', 'main', env=self.env).splitlines()
            for name in ('macgyver.sh', 'Upload_MacGyver_v21_SSH.sh', 'tools/upload-v21/site_sync.py', 'tools/upload-v21/upload.py', 'tools/upload-v21/public_transport.py', 'tools/sync-v13/models_sync.py'):
                self.assertIn(name, names)
            self.assertNotIn('public/academy/data/featured.json', names)
            self.assertNotIn('MEMBER-LESSON-SECRET', self.show(self.site, 'public/academy/data/lazy/index.json'))

    def test_unrecognized_source_version_blocks_public_push(self):
        original = self.head(self.site)
        (self.source / 'SOURCE_VERSION.json').write_text('{"version":"23.0.0"}')
        result = self.run_upload('--skip-models', '--skip-documents', check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('must identify V21 or V22', result.stderr)
        self.assertEqual(original, self.head(self.site))

    def test_v21_fullscreen_journeys_export_with_rebuilt_wrapper(self):
        self.run_upload('--skip-models', '--skip-documents')
        names=cmd('git','--git-dir',str(self.site),'ls-tree','-r','--name-only','main',env=self.env).splitlines()
        for name in ('experience.html','experience-v21.js','experience-v21.css',
                     'data/experiences-v21.json','data/experiences-v21.js'):
            self.assertIn('public/academy/'+name,names)
        wrapper=self.show(self.site,'public/academy/data/experiences-v21.js')
        self.assertIn('window.MACGYVER_EXPERIENCES_V21=',wrapper)
        self.assertIn('window.MG_EXPERIENCES_V21=window.MACGYVER_EXPERIENCES_V21',wrapper)
        self.assertNotIn('throw new Error',wrapper)

    def test_public_export_omits_atomic_write_and_editor_backups(self):
        root=self.source/'public/academy'
        leftovers=('.private.js', 'vendor/wllama/.compat.js.atomic',
                   'assets/photos/photo.jpg.bak', 'assets/.drafts/member.json',
                   'i18n/translations.json.tmp')
        for relative in leftovers:
            path=root/relative;path.parent.mkdir(parents=True,exist_ok=True)
            path.write_text('PRIVATE-TEMPORARY-CONTENT')
        (root/'vendor/wllama/compat.js').write_text('/* intended public resource */')
        self.run_upload('--skip-models','--skip-documents')
        names=cmd('git','--git-dir',str(self.site),'ls-tree','-r','--name-only','main',env=self.env).splitlines()
        self.assertIn('public/academy/vendor/wllama/compat.js',names)
        for relative in leftovers:
            self.assertNotIn('public/academy/'+relative,names)

    def test_journey_member_payload_and_unrecognized_fields_block_push(self):
        path=self.source/'public/academy/data/experiences-v21.json'
        original=json.loads(path.read_text())
        old=self.head(self.site)
        for field in ('knowledge','stages','unreviewedLessonBody'):
            data=json.loads(json.dumps(original))
            data['experiences'][0][field]='MEMBER-LESSON-SECRET'
            path.write_text(json.dumps(data))
            result=self.run_upload('--skip-models','--skip-documents',check=False)
            self.assertNotEqual(0,result.returncode)
            self.assertEqual(old,self.head(self.site))
        path.write_text(json.dumps(original))

    def test_journey_nonfinite_number_blocks_push(self):
        old=self.head(self.site)
        path=self.source/'public/academy/data/experiences-v21.json'
        path.write_text('{"version":21,"domains":[],"assets":[],"experiences":[],"x":NaN}')
        result=self.run_upload('--skip-models','--skip-documents',check=False)
        self.assertNotEqual(0,result.returncode)
        self.assertIn('Non-finite',result.stderr)
        self.assertEqual(old,self.head(self.site))

    def test_missing_journey_catalogue_stops_before_public_push(self):
        old=self.head(self.site)
        (self.source/'public/academy/data/experiences-v21.json').unlink()
        result=self.run_upload('--skip-models','--skip-documents',check=False)
        self.assertNotEqual(0,result.returncode)
        self.assertIn('without its checked scene catalogue',result.stderr)
        self.assertEqual(old,self.head(self.site))

    def test_direct_transport_cannot_upload_unverified_full_source(self):
        old = self.head(self.site)
        result = subprocess.run(
            ['python3', str(self.source/'tools/upload-v21/public_transport.py'),
             '--repo', self.site.as_uri(), '--push', '--state', str(self.state)],
            env=self.env, cwd=self.base, capture_output=True, text=True)
        self.assertNotEqual(0, result.returncode)
        self.assertIn('cannot upload directly', result.stderr)
        self.assertEqual(old, self.head(self.site))

    def test_public_snapshot_excludes_full_member_bodies_and_author_inputs(self):
        self.run_upload('--skip-models', '--skip-documents')
        names=cmd('git','--git-dir',str(self.site),'ls-tree','-r','--name-only','main',env=self.env).splitlines()
        self.assertFalse(any('/owner-' in name or name.endswith('/featured.json') or 'environment-v17/inputs' in name for name in names))
        for name in names:
            data=self.show(self.site,name)
            self.assertNotIn('MEMBER-LESSON-SECRET',data,name)
        self.assertIn('public/academy/preview-manifest.json',names)

    def test_v21_games_are_public_without_author_intermediates(self):
        self.run_upload('--skip-models', '--skip-documents')
        names=cmd('git','--git-dir',str(self.site),'ls-tree','-r','--name-only','main',env=self.env).splitlines()
        for name in ('campaign.html','campaign-core.js','campaign.css','data/campaigns-v20.json',
                     'data/campaigns-v20.js','data/campaign-index-v20.json','data/campaign-index-v20.js',
                     'data/campaign-media-v20.json','data/campaign-media-v20.js'):
            self.assertIn('public/academy/'+name,names)
        self.assertNotIn('public/academy/data/campaigns-semiconductor-v20.json',names)
        self.assertNotIn('public/academy/data/course-missions-v20.json',names)
        wrapper=self.show(self.site,'public/academy/data/campaigns-v20.js')
        self.assertIn('window.MG_CAMPAIGNS_V20=',wrapper)
        self.assertNotIn('throw new Error',wrapper)

    def test_campaign_member_payload_rejected_before_public_push(self):
        old=self.head(self.site)
        path=self.source/'public/academy/data/campaigns-v20.json'
        path.write_text(json.dumps({'version':20,'campaigns':[{'id':'bad','stages':[{'knowledge':'MEMBER-LESSON-SECRET'}]}]}))
        result=self.run_upload('--skip-models','--skip-documents',check=False)
        self.assertNotEqual(0,result.returncode)
        self.assertIn('Full lesson fields',result.stderr)
        self.assertEqual(old,self.head(self.site))

    def test_campaign_nonfinite_number_rejected_before_public_push(self):
        old=self.head(self.site)
        path=self.source/'public/academy/data/campaigns-v20.json'
        path.write_text('{"version":20,"campaigns":[{"value":NaN}]}')
        result=self.run_upload('--skip-models','--skip-documents',check=False)
        self.assertNotEqual(0,result.returncode)
        self.assertIn('Non-finite',result.stderr)
        self.assertEqual(old,self.head(self.site))

    def test_known_legacy_member_payload_removed_unrelated_file_retained(self):
        seed=self.base/'site-seed'
        for name in ['public/academy/data/lazy/owner-courses/old.json',
                     'public/academy/data/course-parts/old.json',
                     'public/academy/data/.featured.json.known-v17-temp',
                     'tools/environment-v17/inputs/old.json',
                     'tools/aviation-v18/inputs/old.json',
                     'tools/marine-v19/inputs/old.json',
                     'user-custom/project-notes.txt']:
            file=seed/name;file.parent.mkdir(parents=True,exist_ok=True);file.write_text('legacy content')
        cmd('git','add','.',cwd=seed,env=self.env)
        cmd('git','commit','-m','legacy fixture',cwd=seed,env=self.env)
        cmd('git','push','origin','main',cwd=seed,env=self.env)
        old=self.head(self.site)
        self.run_upload('--skip-models','--skip-documents')
        names=cmd('git','--git-dir',str(self.site),'ls-tree','-r','--name-only','main',env=self.env)
        self.assertNotIn('owner-courses',names)
        self.assertNotIn('course-parts',names)
        self.assertNotIn('.featured.json.',names)
        self.assertNotIn('environment-v17/inputs',names)
        self.assertNotIn('aviation-v18/inputs', names)
        self.assertNotIn('marine-v19/inputs', names)
        self.assertIn('user-custom/project-notes.txt',names)
        # Migration does not rewrite or purge old commit history.
        self.assertEqual('legacy content',cmd('git','--git-dir',str(self.site),'show',old+':public/academy/data/course-parts/old.json',env=self.env))

    def tearDown(self):
        self.tmp.cleanup()

    def run_upload(self, *args, check=True):
        return subprocess.run(['bash', str(self.source / 'Upload_MacGyver_v21_SSH.sh'), '--with-assets', '--state', str(self.state), *args],
                              env=self.env, cwd=self.base, text=True, capture_output=True, check=check)

    def head(self, repo):
        return cmd('git', '--git-dir', str(repo), 'rev-parse', 'refs/heads/main', env=self.env)

    def show(self, repo, path):
        return cmd('git', '--git-dir', str(repo), 'show', 'main:' + path, env=self.env)

    def assets(self):
        model = self.source / 'models/custom model.gguf'
        doc = self.source / 'local-documents/lesson.md'
        model.parent.mkdir(exist_ok=True)
        doc.parent.mkdir(exist_ok=True)
        model.write_bytes(b'MODEL-EXAMPLE-1234' * 8)
        doc.write_text('Private teaching notes, multilingual: 水利工程。')
        (doc.parent / '.env').write_text('NEVER_UPLOAD=credential')
        (doc.parent / 'accounts.sqlite').write_bytes(b'PRIVATE ACCOUNT DB')
        (model.parent / 'credentials.json').write_text('{"doNot":"upload"}')
        return model, doc

    def test_dry_run_has_no_remote_mutation(self):
        self.assets()
        old = (self.head(self.site), self.head(self.private))
        r = self.run_upload('--dry-run')
        self.assertIn('遠端未變更', r.stdout)
        self.assertEqual(old, (self.head(self.site), self.head(self.private)))

    def test_reuses_existing_private_chunk_namespace(self):
        self.assertEqual('projects/macgyver/v18-assets', u.PREFIX)
        self.assertEqual('projects/macgyver/v18-assets/assets-manifest.json', u.MANIFEST)

    def test_default_updates_only_public_website(self):
        self.assets()
        original = self.head(self.private)
        subprocess.run(['bash', str(self.source / 'Upload_MacGyver_v21_SSH.sh'), '--state', str(self.state)],
                       env=self.env, cwd=self.base, text=True, capture_output=True, check=True)
        self.assertEqual(original, self.head(self.private))
        self.assertEqual('V21 entry', self.show(self.site, 'index.html'))

    def test_missing_preview_uploader_never_falls_back_to_legacy(self):
        (self.source / 'Upload_MacGyver_v21_SSH.sh').unlink()
        (self.source / 'Upload_MacGyver_v16_SSH.sh').write_text('#!/usr/bin/env bash\ntouch LEGACY-UNSAFE-UPLOAD\n')
        result = subprocess.run(['bash', str(self.source / 'macgyver.sh'), 'compare'], env=self.env, cwd=self.source, capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('不回退', result.stderr)
        self.assertFalse((self.source / 'LEGACY-UNSAFE-UPLOAD').exists())

    def test_generic_aliases_use_v21_and_accept_with_assets(self):
        self.assets()
        original = (self.head(self.site), self.head(self.private))
        for script, arguments in [('macgyver.sh', ['compare']), ('upload-all.sh', ['--dry-run'])]:
            result = subprocess.run(['bash', str(self.source / script), *arguments,
                                     '--with-assets', '--state', str(self.state)],
                                    env=self.env, cwd=self.base, text=True, capture_output=True, check=True)
            self.assertIn('遠端未變更', result.stdout)
            self.assertEqual(original, (self.head(self.site), self.head(self.private)))

    def test_upload_noop_modify_preserve_and_restore(self):
        model, doc = self.assets()
        self.run_upload()
        self.assertEqual('V21 entry', self.show(self.site, 'index.html'))
        for repo in (self.site, self.private):
            self.assertEqual('keep me', self.show(repo, 'remote-only.txt'))
        public_names = cmd('git', '--git-dir', str(self.site), 'ls-tree', '-r', '--name-only', 'main', env=self.env)
        for blocked in ('owner-private/', 'portable/data/', 'models/custom', 'local-documents/'):
            self.assertNotIn(blocked, public_names)
        manifest = json.loads(self.show(self.private, u.MANIFEST))
        self.assertEqual(['documents/lesson.md', 'models/custom model.gguf'], [x['path'] for x in manifest['files']])
        old = (self.head(self.site), self.head(self.private))
        self.run_upload()
        self.assertEqual(old, (self.head(self.site), self.head(self.private)))
        model.write_bytes(b'UPDATED-WEIGHT-ABCDE' * 8)
        original_doc = doc.read_bytes()
        doc.unlink()
        (self.source / 'index.html').write_text('V21 changed')
        self.run_upload()
        self.assertEqual('V21 changed', self.show(self.site, 'index.html'))
        manifest = json.loads(self.show(self.private, u.MANIFEST))
        self.assertEqual(['documents/lesson.md', 'models/custom model.gguf'], [x['path'] for x in manifest['files']])
        destination = self.base / 'restore destination'
        self.run_upload('--restore-assets', str(destination))
        self.assertEqual(model.read_bytes(), (destination / 'models/custom model.gguf').read_bytes())
        self.assertEqual(original_doc, (destination / 'documents/lesson.md').read_bytes())

    def test_skip_private_and_no_download(self):
        self.assets()
        old = self.head(self.private)
        self.run_upload('--skip-models', '--skip-documents')
        self.assertEqual(old, self.head(self.private))
        shutil.rmtree(self.source / 'models')
        shutil.rmtree(self.source / 'local-documents')
        r = self.run_upload()
        self.assertIn('不下載模型', r.stdout)
        self.assertFalse((self.source / 'models').exists())

    def test_reject_unsafe_credentials_before_any_push(self):
        self.assets()
        private = self.source / 'local-documents/lesson.md'
        private.write_text('service credential ' + 'sk-' + 'x' * 48)
        old = (self.head(self.site), self.head(self.private))
        r = self.run_upload(check=False)
        self.assertNotEqual(0, r.returncode)
        self.assertIn('疑似金鑰', r.stderr)
        self.assertNotIn('sk-' + 'x' * 48, r.stderr)
        self.assertEqual(old, (self.head(self.site), self.head(self.private)))

    def test_reject_office_embedded_credentials(self):
        directory = self.base / 'documents'
        directory.mkdir()
        with zipfile.ZipFile(directory / 'notes.docx', 'w', compression=zipfile.ZIP_DEFLATED) as f:
            f.writestr('word/document.xml', '<doc>' + 'github_' + 'pat_' + 'a' * 40 + '</doc>')
        with self.assertRaisesRegex(ValueError, '疑似金鑰'):
            u.collect(directory, 'documents')

    def test_owner_private_selected_subfolder_rejected(self):
        directory = self.source / 'owner-private' / 'models'
        directory.mkdir()
        (directory / 'model.gguf').write_bytes(b'weight')
        with self.assertRaisesRegex(ValueError, '子資料夾'):
            u.collect(directory, 'models')

    def test_unowned_state_is_never_reset(self):
        self.state.mkdir()
        p = self.state / 'precious.txt'
        p.write_text('keep')
        r = self.run_upload('--skip-models', '--skip-documents', check=False)
        self.assertNotEqual(0, r.returncode)
        self.assertEqual('keep', p.read_text())

    def test_private_visibility_fails_closed(self):
        with mock.patch.object(u.shutil, 'which', return_value=None):
            with mock.patch.object(u, 'urlopen', return_value=contextlib.nullcontext(io.BytesIO(b'{"private":false}'))):
                with self.assertRaises(ValueError):
                    u.check_private_repo(u.PRIVATE_REPO)
            with mock.patch.object(u, 'urlopen', side_effect=URLError('offline')):
                with self.assertRaises(ValueError):
                    u.check_private_repo(u.PRIVATE_REPO)
            with mock.patch.object(u, 'urlopen', side_effect=HTTPError('test', 404, 'missing', {}, None)), mock.patch.object(u.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, '', '')):
                self.assertIn('authenticated SSH', u.check_private_repo(u.PRIVATE_REPO))

    def test_unknown_model_and_document_paths_with_spaces(self):
        custom = self.base / 'external weights'
        custom.mkdir()
        (custom / 'custom.h5').write_bytes(b'my custom trained weights')
        docs = self.base / 'external docs'
        docs.mkdir()
        (docs / '實驗課程.txt').write_text('資料')
        self.run_upload('--models-dir', str(custom), '--documents-dir', str(docs))
        manifest = json.loads(self.show(self.private, u.MANIFEST))
        self.assertEqual(['documents/實驗課程.txt', 'models/custom.h5'], [x['path'] for x in manifest['files']])

    def test_selected_private_folder_inside_public_tree_is_not_published(self):
        private = self.source / 'docs' / 'my private teaching files'
        private.mkdir(parents=True)
        (private / 'notes.txt').write_text('Private class discussion')
        self.run_upload('--skip-models', '--documents-dir', str(private))
        public_names = cmd('git', '--git-dir', str(self.site), 'ls-tree', '-r', '--name-only', 'main', env=self.env)
        self.assertNotIn('my private teaching files', public_names)
        manifest = json.loads(self.show(self.private, u.MANIFEST))
        self.assertEqual(['documents/notes.txt'], [x['path'] for x in manifest['files']])

    def test_model_formats_and_uppercase_credentials_excluded_from_public(self):
        public = self.source / 'public' / 'academy'
        (public / 'training.h5').write_bytes(b'local weights')
        (public / 'training.model').write_bytes(b'local weights')
        (public / 'CREDENTIALS').mkdir()
        (public / 'CREDENTIALS' / 'notes.txt').write_text('Private account notes')
        self.run_upload('--skip-models', '--skip-documents')
        names = cmd('git', '--git-dir', str(self.site), 'ls-tree', '-r', '--name-only', 'main', env=self.env)
        self.assertNotIn('training.h5', names)
        self.assertNotIn('training.model', names)
        self.assertNotIn('CREDENTIALS', names)

    def test_interrupted_chunk_batches_resume(self):
        model, doc = self.assets()
        with mock.patch.dict(os.environ, self.env):
            engine = u.load_engine()
            plans = u.plan_assets(engine, [('models', model.parent, [model])])
            state = self.base / 'resume-state'
            original = engine.commit_and_push
            calls = 0
            def interrupted(*args, **kwargs):
                nonlocal calls
                calls += 1
                if calls == 2:
                    raise RuntimeError('simulated interruption')
                return original(*args, **kwargs)
            with mock.patch.object(engine, 'commit_and_push', side_effect=interrupted):
                with self.assertRaisesRegex(RuntimeError, 'simulated interruption'):
                    u.upload_assets(engine, plans, self.private.as_uri(), 'main', state, batch_mib=0)
            names = cmd('git', '--git-dir', str(self.private), 'ls-tree', '-r', '--name-only', 'main', env=self.env)
            self.assertIn(u.PREFIX + '/parts/', names)
            self.assertNotIn(u.MANIFEST, names)
            u.upload_assets(engine, plans, self.private.as_uri(), 'main', state, batch_mib=0)
            dest = self.base / 'resumed-restore'
            u.restore_assets(engine, self.private.as_uri(), 'main', state, dest)
            self.assertEqual(model.read_bytes(), (dest / 'models/custom model.gguf').read_bytes())

    def test_manifest_traversal_rejected(self):
        with self.assertRaises(ValueError):
            u.validate_remote_manifest({'schema': 1, 'files': [{'path': 'documents/../../owner-private/x'}]})

    def test_public_unicode_filename_does_not_recommit(self):
        p = self.source / 'public/academy/水利 教材.html'
        p.write_text('公開教材')
        self.run_upload('--skip-models', '--skip-documents')
        first = self.head(self.site)
        self.run_upload('--skip-models', '--skip-documents')
        self.assertEqual(first, self.head(self.site))
        self.assertEqual('公開教材', self.show(self.site, 'public/academy/水利 教材.html'))

    def test_password_assignments_rejected(self):
        data = ('{"pass' + 'word":"sample1234"}').encode()
        with self.assertRaises(ValueError):
            u.scan_stream(io.BytesIO(data), 'example.json')

    def test_retry_never_force_pushes(self):
        with mock.patch.dict(os.environ, self.env):
            engine = u.load_engine()
            with mock.patch.object(engine, 'git', side_effect=['tree', 'commit']), mock.patch.object(engine.subprocess, 'run', return_value=subprocess.CompletedProcess([], 1)) as run, mock.patch.object(engine.time, 'sleep'):
                with self.assertRaises(SystemExit):
                    engine.commit_and_push(self.base, None, self.base / 'index', 'test', 'main')
                self.assertEqual(4, run.call_count)
                self.assertTrue(all('--force' not in c.args[0] and '-f' not in c.args[0] for c in run.call_args_list))


if __name__ == '__main__':
    unittest.main(verbosity=2)
