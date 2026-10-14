import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import MagicMock, patch
from portable import server


class AdapterBoundaryTests(unittest.TestCase):
    def test_long_translation_json_is_not_truncated(self):
        answer = json.dumps({'translations': ['a' * 10000, 'b' * 10000, 'c' * 10000]})
        response = MagicMock()
        response.__enter__.return_value.read.return_value = json.dumps({'choices': [{'message': {'content': answer}}]}).encode()
        with patch.dict(os.environ, {'AI_BASE_URL': 'https://model.example/v1', 'AI_API_KEY': 'test-only', 'AI_MODEL': 'test-model'}), patch.object(server, 'build_opener') as factory:
            factory.return_value.open.return_value = response
            result = server.ai_completion('Translate', {}, json_output=True)
            self.assertEqual(json.loads(result)['translations'][2], 'c' * 10000)
            self.assertEqual(factory.return_value.open.call_args.kwargs['timeout'], 60)

    def test_sensitive_storage_cannot_be_inside_static_web_root(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            public = root / 'public'
            public.mkdir()
            with patch.dict(os.environ, {'KNOWLEDGE_INDEX': str(root / 'knowledge.json')}):
                with self.assertRaisesRegex(ValueError, 'outside the static web root'):
                    server.Application(public / 'accounts.sqlite3', public, 'http://127.0.0.1:8010')
            self.assertFalse((public / 'accounts.sqlite3').exists())
            with patch.dict(os.environ, {'KNOWLEDGE_INDEX': str(public / 'knowledge.json')}):
                with self.assertRaisesRegex(ValueError, 'outside the static web root'):
                    server.Application(root / 'accounts.sqlite3', public, 'http://127.0.0.1:8010')

