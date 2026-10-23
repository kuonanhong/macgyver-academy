"""Cross-check the actual V16 builder and public exporter with private sentinels."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('preview_v16',ROOT/'tools/export-preview-v16.py')
preview=importlib.util.module_from_spec(spec);spec.loader.exec_module(preview)

class PreviewExportTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(prefix='macgyver-preview-security-')
        self.root=Path(self.tmp.name);self.public=self.root/'source/public/academy';self.data=self.public/'data';self.data.mkdir(parents=True)
        (self.root/'source/tools').mkdir()
        for name in ('build-offline.mjs','restore-featured.mjs'):shutil.copyfile(ROOT/'tools'/name,self.root/'source/tools'/name)
        for name in ('paywall.js','lazy-index-codec.js'):shutil.copyfile(ROOT/'public/academy'/name,self.public/name)
        (self.public/'index.html').write_text('<title>Public fixture</title>')
        (self.public/'app.js').write_text('console.log("fixture");')
        (self.public/'immersive-v16.js').write_text('export function mountImmersiveScene(){return null;}')
        course={'id':'test-rail','title':'Rail','titleEn':'Rail','category':'rail','stages':[{'id':'trial','steps':[{'id':'s1','instruction':'FREE_BODY'}]},{'id':'paid','steps':[{'id':'s2','instruction':'MEMBER_BODY_SENTINEL','instructionEn':'MEMBER_ENGLISH_SENTINEL','quiz':{'question':'MEMBER_QUIZ_SENTINEL','options':['A','B'],'answer':0}}]}]}
        values={'featured':[course],'catalog':[{'id':'test-rail','title':'Rail','category':'rail'}],'photos':[],'sources':[],'release':{'version':'16.0.0'},'pricing':{'freeStagesPerCourse':1},'media':{'courses':[{'courseId':'test-rail','guides':[{'text':'MEMBER_GUIDE_SENTINEL'}]}]}}
        for name,value in values.items():(self.data/f'{name}.json').write_text(json.dumps(value))
        subprocess.run(['node',str(self.root/'source/tools/build-offline.mjs')],check=True,capture_output=True,text=True)
        self.output=self.root/'preview'
        self.index=json.loads((self.data/'lazy/index.json').read_text())

    def tearDown(self):self.tmp.cleanup()

    def exported_bytes(self):return b'\n'.join(p.read_bytes() for p in self.output.rglob('*') if p.is_file())

    def write_indexes(self):
        (self.data/'lazy/index.json').write_text(json.dumps(self.index))
        (self.data/'lazy/index.compact.json').write_text(json.dumps(preview.compact_index(self.index)))

    def rewrite_course(self,change):
        old=self.index['courses']['test-rail'];value=json.loads((self.public/old['file']).read_text());change(value)
        raw=(json.dumps(value,separators=(',',':'))+'\n').encode();digest=hashlib.sha256(raw).hexdigest()
        name=f'data/lazy/courses/test-rail-{digest[:16]}.json'
        descriptor={'file':name,'script':name[:-5]+'.js','sha256':digest,'byteLength':len(raw)}
        (self.public/name).write_bytes(raw);(self.public/descriptor['script']).write_bytes(preview.bound_script(descriptor,raw))
        self.index['courses']['test-rail']=descriptor;self.write_indexes()

    def test_real_builder_exports_only_public_json_scripts_and_bootstrap(self):
        result=preview.export(self.public,self.output)
        content=self.exported_bytes()
        self.assertEqual(result['memberBodies'],0);self.assertIn(b'FREE_BODY',content)
        for sentinel in (b'MEMBER_BODY_SENTINEL',b'MEMBER_ENGLISH_SENTINEL',b'MEMBER_QUIZ_SENTINEL',b'MEMBER_GUIDE_SENTINEL'):
            self.assertNotIn(sentinel,content)
        self.assertFalse(any('owner-' in p.as_posix() for p in self.output.rglob('*')))
        self.assertFalse((self.output/'data/featured.json').exists())

    def test_stale_classic_script_is_rejected_even_with_valid_public_json(self):
        descriptor=self.index['courses']['test-rail']
        with (self.public/descriptor['script']).open('a') as f:f.write('window.oldPrivate="MEMBER_BODY_SENTINEL";')
        with self.assertRaisesRegex(ValueError,'Classic script'):preview.export(self.public,self.output)
        self.assertFalse(self.output.exists())

    def test_stale_full_bootstrap_is_replaced_from_checked_index(self):
        (self.public/'offline-data.js').write_text('window.MG_DATA={featured:["MEMBER_BODY_SENTINEL"]};')
        preview.export(self.public,self.output)
        self.assertNotIn(b'MEMBER_BODY_SENTINEL',self.exported_bytes())

    def test_mismatched_compact_index_is_rejected(self):
        value=json.loads((self.data/'lazy/index.compact.json').read_text());value['catalog'][0]['title']='stale'
        (self.data/'lazy/index.compact.json').write_text(json.dumps(value))
        with self.assertRaisesRegex(ValueError,'indexes disagree'):preview.export(self.public,self.output)

    def test_english_paid_body_is_rejected(self):
        self.rewrite_course(lambda c:c['stages'][1]['steps'][0].update(instructionEn='MEMBER_ENGLISH_SENTINEL'))
        with self.assertRaisesRegex(ValueError,'Member body'):preview.export(self.public,self.output)

    def test_public_bilingual_diagram_and_architecture_survive_export(self):
        self.rewrite_course(lambda c:c.update(flowDiagramEn='assets/diagrams/v16-b301-en.svg',v16Architecture={'architectureFamily':'rail-system','architectureNodes':[['車輛','Vehicle'],['軌道','Track']],'architectureEdges':[[0,1]]}))
        preview.export(self.public,self.output)
        value=json.loads((self.output/self.index['courses']['test-rail']['file']).read_text())
        self.assertEqual(value['v16Architecture']['architectureNodes'][1],['軌道','Track'])
        self.assertEqual(value['flowDiagramEn'],'assets/diagrams/v16-b301-en.svg')

    def test_architecture_cannot_hide_lesson_bodies_or_paths(self):
        self.rewrite_course(lambda c:c.update(v16Architecture={'architectureFamily':'rail-system','architectureNodes':[['車輛','Vehicle']],'architectureEdges':[],'stages':[{'instruction':'MEMBER_BODY_SENTINEL'}]}))
        with self.assertRaisesRegex(ValueError,'architecture fields'):preview.export(self.public,self.output)
        self.rewrite_course(lambda c:(c.pop('v16Architecture'),c.update(flowDiagramEn='../../owner-private/secret.svg')))
        with self.assertRaisesRegex(ValueError,'diagram asset'):preview.export(self.public,self.output)

    def test_increased_free_stage_count_is_rejected(self):
        self.rewrite_course(lambda c:c.update(freeStagesPerCourse=2))
        with self.assertRaisesRegex(ValueError,'exactly one'):preview.export(self.public,self.output)

    def test_catalogue_body_is_rejected(self):
        self.index['catalog'][0]['stages'][1]['steps'][0]['instruction']='MEMBER_BODY_SENTINEL';self.write_indexes()
        with self.assertRaisesRegex(ValueError,'Catalogue step'):preview.export(self.public,self.output)

    def test_quiz_english_answer_body_is_rejected(self):
        self.rewrite_course(lambda c:c['stages'][1]['steps'][0]['quiz'].update(questionEn='MEMBER_QUIZ_SENTINEL'))
        with self.assertRaisesRegex(ValueError,'Member body'):preview.export(self.public,self.output)

    def test_auxiliary_media_cannot_reintroduce_full_guides(self):
        raw=b'{"courses":[{"courseId":"test-rail","guides":[{"text":"MEMBER_GUIDE_SENTINEL"}]}]}\n'
        digest=hashlib.sha256(raw).hexdigest();name=f'data/lazy/data/media-{digest[:16]}.json'
        descriptor={'file':name,'script':name[:-5]+'.js','sha256':digest,'byteLength':len(raw)}
        (self.public/name).write_bytes(raw);(self.public/descriptor['script']).write_bytes(preview.bound_script(descriptor,raw))
        self.index['auxiliary']['media']=descriptor;self.write_indexes()
        with self.assertRaisesRegex(ValueError,'supplemental guide'):preview.export(self.public,self.output)

    def test_descriptor_path_escape_is_rejected(self):
        self.index['courses']['test-rail']['file']='../../owner-private/bootstrap.json';self.write_indexes()
        with self.assertRaisesRegex(ValueError,'Unsafe public descriptor'):preview.export(self.public,self.output)

    def test_symlink_output_is_rejected_without_touching_target(self):
        target=self.root/'keep';target.mkdir();(target/preview.MARKER).write_text('fixture');(target/'precious.txt').write_text('keep')
        self.output.symlink_to(target,target_is_directory=True)
        with self.assertRaisesRegex(ValueError,'symlink'):preview.export(self.public,self.output)
        self.assertEqual((target/'precious.txt').read_text(),'keep')

if __name__=='__main__':unittest.main(verbosity=2)
