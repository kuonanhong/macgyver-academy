import hashlib,importlib.util,io,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
spec=importlib.util.spec_from_file_location('download_ai_model',Path(__file__).parents[1]/'tools/download_ai_model.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
class Response(io.BytesIO):
 def __init__(self,body,status=200,headers=None):super().__init__(body);self.status=status;self.url='https://huggingface.co/test';self.headers=headers or {}
class ModelDownloads(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name);self.payload=b'GGUF-test-weight-data';self.model={'file':'sample.gguf','bytes':len(self.payload),'sha256':hashlib.sha256(self.payload).hexdigest(),'repo':'owner/model','revision':'pinned'}
 def tearDown(self):self.temp.cleanup()
 def test_resume_checks_range_and_full_hash(self):
  (self.root/'sample.gguf.part').write_bytes(self.payload[:5])
  with patch.object(module,'urlopen',return_value=Response(self.payload[5:],206,{'Content-Range':f'bytes 5-{len(self.payload)-1}/{len(self.payload)}'})) as fetch:
   result=module.download(self.model,self.root)
  self.assertEqual(result.read_bytes(),self.payload);self.assertEqual(fetch.call_args.args[0].headers['Range'],'bytes=5-')
 def test_server_ignores_range_restarts_safely(self):
  (self.root/'sample.gguf.part').write_bytes(b'old')
  with patch.object(module,'urlopen',return_value=Response(self.payload)):
   self.assertEqual(module.download(self.model,self.root).read_bytes(),self.payload)
 def test_tamper_never_installs_or_overwrites(self):
  bad=bytearray(self.payload);bad[0]=0
  with patch.object(module,'urlopen',return_value=Response(bytes(bad))):
   with self.assertRaisesRegex(ValueError,'Checksum'):module.download(self.model,self.root)
  self.assertFalse((self.root/'sample.gguf').exists())
  (self.root/'sample.gguf').write_bytes(b'personal original')
  with self.assertRaisesRegex(ValueError,'not overwritten'):module.download(self.model,self.root)
  self.assertEqual((self.root/'sample.gguf').read_bytes(),b'personal original')
 def test_existing_valid_weights_need_no_network(self):
  (self.root/'sample.gguf').write_bytes(self.payload)
  with patch.object(module,'urlopen',side_effect=AssertionError('Unexpected download')):
   self.assertEqual(module.download(self.model,self.root).read_bytes(),self.payload)
if __name__=='__main__':unittest.main()
