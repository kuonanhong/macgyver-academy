"""Local bare Git mocks; no GitHub/network, real commits and remote reads."""
import importlib.util,json,os,subprocess,sys,tempfile,unittest,contextlib,io,shutil
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('sync_v14',ROOT/'tools/sync-v12/sync_github.py'); sync=importlib.util.module_from_spec(spec);spec.loader.exec_module(sync)
class SyncTests(unittest.TestCase):
 def test_empty_remote_retry_preservation_and_managed_deletion(self):
  with tempfile.TemporaryDirectory() as tmp:
   base=Path(tmp);source=base/'source';source.mkdir();remote=base/'remote.git';state=base/'state'
   real_run=subprocess.run
   env={'MACGYVER_SYNC_TEST_REMOTE':'1','GIT_AUTHOR_NAME':'Test','GIT_AUTHOR_EMAIL':'test@example.org','GIT_COMMITTER_NAME':'Test','GIT_COMMITTER_EMAIL':'test@example.org','GIT_CONFIG_COUNT':'2','GIT_CONFIG_KEY_0':'user.name','GIT_CONFIG_VALUE_0':'Test','GIT_CONFIG_KEY_1':'user.email','GIT_CONFIG_VALUE_1':'test@example.org'}
   with patch.dict(os.environ,env):
    real_run(['git','init','--bare','-q',str(remote)],check=True)
    files={'index.html':b'v1','old.txt':b'old'};argv=['sync','--repo',remote.as_uri(),'--state',str(state),'--push']; attempts=[]
    def failing(args,*a,**kw):
     if 'push' in args:
      attempts.append(args);return subprocess.CompletedProcess(args,1)
     return real_run(args,*a,**kw)
    with patch.object(sync,'ROOT',source),patch.object(sync.export_github,'snapshot',lambda root:(dict(files),{})),patch.object(sys,'argv',argv),patch.object(sync.time,'sleep',lambda _:None),contextlib.redirect_stdout(io.StringIO()):
     with patch.object(sync.subprocess,'run',failing): self.assertEqual(sync.main(),1)
     self.assertEqual(len(attempts),4);self.assertFalse(any('--force' in x or '-f' in x for x in attempts))
     self.assertEqual(sync.main(),0,'retry must publish even after first push never created a remote branch')
     seed=base/'seed';real_run(['git','clone','-q','--branch','main',remote.as_uri(),str(seed)],check=True)
     (seed/'owner-added.txt').write_text('retain unknown remote content');real_run(['git','-C',str(seed),'add','.'],check=True);real_run(['git','-C',str(seed),'commit','-qm','owner'],check=True);real_run(['git','-C',str(seed),'push','-q','origin','main'],check=True)
     files.pop('old.txt');files['index.html']=b'v2';self.assertEqual(sync.main(),0)
     names=real_run(['git','--git-dir',str(remote),'ls-tree','-r','--name-only','main'],capture_output=True,text=True,check=True).stdout.splitlines()
     self.assertIn('owner-added.txt',names);self.assertNotIn('old.txt',names)
     head=real_run(['git','--git-dir',str(remote),'rev-parse','main'],capture_output=True,text=True,check=True).stdout
     self.assertEqual(sync.main(),0)
     self.assertEqual(head,real_run(['git','--git-dir',str(remote),'rev-parse','main'],capture_output=True,text=True,check=True).stdout)
 def test_protected_rebuild_removes_all_owner_payloads(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);public=root/'public/academy';data=public/'data';data.mkdir(parents=True);(root/'tools').mkdir()
   for name in ('build-offline.mjs','restore-featured.mjs'):shutil.copyfile(ROOT/'tools'/name,root/'tools'/name)
   (public/'app.js').write_text('console.log("fixture");')
   shutil.copyfile(ROOT/'public/academy/lazy-index-codec.js',public/'lazy-index-codec.js')
   (data/'sources.json').write_text('[]');(data/'photos.json').write_text('[]');(data/'release.json').write_text('{}')
   course={'id':'b101','title':'fixture','stages':[{'id':'free','steps':[{'id':'first','instruction':'free body'}]},{'id':'paid','steps':[{'id':'second','instruction':'OWNER_PRIVATE_SENTINEL'}]}]}
   (data/'featured.json').write_text(json.dumps([course]));(data/'catalog.json').write_text(json.dumps([course]))
   files={'public/academy/data/lazy/courses/old.json':b'OWNER_PRIVATE_SENTINEL','public/academy/offline-data.js':b'OWNER_PRIVATE_SENTINEL'}
   with patch.object(sync,'ROOT',root):
    result=sync.stub_paid_stages(files,free_stages=1)
    self.assertTrue(any('data/lazy/courses/' in k for k in result));self.assertFalse(any(b'OWNER_PRIVATE_SENTINEL' in v for v in result.values()))
    with patch.object(sync.shutil,'which',lambda _:None):self.assertRaises(ValueError,sync.stub_paid_stages,files)
if __name__=='__main__':unittest.main()
