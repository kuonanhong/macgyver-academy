"""AI routing boundaries: mocked providers, no model downloads or secrets."""
import base64
import http.client
import io
import json
import os
from pathlib import Path
import struct
import subprocess
import tempfile
import threading
import unittest
from unittest.mock import MagicMock, patch
from urllib.error import HTTPError
from portable import server

PNG = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+jRZkAAAAASUVORK5CYII=')
IMAGE = {'mimeType': 'image/png', 'data': base64.b64encode(PNG).decode()}
ENV = {'AI_BASE_URL': '', 'AI_API_KEY': '', 'AI_MODEL': '', 'OLLAMA_BASE_URL': 'http://127.0.0.1:11434', 'OLLAMA_TEXT_MODEL': 'qwen3:4b', 'OLLAMA_VISION_MODEL': 'qwen3-vl:2b', 'GEMINI_API_KEY': 'fake-test-key', 'GEMINI_MODEL': 'gemini-3.5-flash-lite'}


def provider_reply(value):
    response = MagicMock()
    response.__enter__.return_value.read.return_value = json.dumps(value).encode()
    return response


class RouteAdapterTests(unittest.TestCase):
    def test_capabilities_only_configured_models_no_key(self):
        with patch.dict(os.environ, ENV, clear=True):
            routes = server.ai_routes()
            self.assertEqual([r['id'] for r in routes], ['ollama-text', 'ollama-vision', 'gemini'])
            self.assertNotIn('fake-test-key', json.dumps(routes))
            self.assertFalse(routes[0]['supportsImages'])
            self.assertTrue(routes[1]['supportsImages'])
            self.assertTrue(routes[2]['cloud'])
        with patch.dict(os.environ, {**ENV, 'OLLAMA_BASE_URL': 'https://remote.example', 'GEMINI_API_KEY': ''}, clear=True):
            self.assertEqual(server.ai_routes(), [])

    def test_images_type_dimensions_and_encoding(self):
        self.assertEqual(server.validate_image(IMAGE), IMAGE)
        for invalid in ({'mimeType': 'image/svg+xml', 'data': IMAGE['data']}, {'mimeType': 'image/jpeg', 'data': IMAGE['data']}, {'mimeType': 'image/png', 'data': 'data:image/png;base64,' + IMAGE['data']}, {'mimeType': 'image/png', 'data': '%%%'}):
            with self.assertRaises(server.ApiError):
                server.validate_image(invalid)
        oversized = {'mimeType': 'image/png', 'data': 'a' * (((server.MAX_IMAGE_BYTES + 2) // 3) * 4 + 1)}
        with self.assertRaises(server.ApiError) as caught:
            server.validate_image(oversized)
        self.assertEqual(caught.exception.status, 413)
        for width, height in ((9000, 1), (1, 0), (8192, 8192)):
            malformed = PNG[:16] + struct.pack('>II', width, height) + PNG[24:]
            with self.assertRaises(server.ApiError):
                server.validate_image({'mimeType': 'image/png', 'data': base64.b64encode(malformed).decode()})

    def test_ollama_vision_is_cpu_native_image_api(self):
        with patch.dict(os.environ, ENV, clear=True), patch.object(server, 'build_opener') as factory:
            factory.return_value.open.return_value = provider_reply({'message': {'content': 'Visible layers; scale unknown.'}})
            route = server.select_ai_route('ollama-vision')
            answer = server.routed_completion(route, 'System', {'question': 'Explain'}, IMAGE)
            request = factory.return_value.open.call_args.args[0]
            payload = json.loads(request.data)
            self.assertEqual(request.full_url, 'http://127.0.0.1:11434/api/chat')
            self.assertEqual(payload['messages'][1]['images'], [IMAGE['data']])
            self.assertEqual(payload['options']['num_gpu'], 0)
            self.assertEqual(payload['options']['num_ctx'], 8192)
            self.assertFalse(payload['stream'])
            self.assertFalse(payload['think'])
            self.assertIn('scale unknown', answer)
            self.assertEqual(factory.return_value.open.call_args.kwargs['timeout'], 180)

    def test_gemini_key_in_header_only_and_thoughts_excluded(self):
        with patch.dict(os.environ, ENV, clear=True), patch.object(server, 'build_opener') as factory:
            factory.return_value.open.return_value = provider_reply({'candidates': [{'content': {'parts': [{'text': 'not shown', 'thought': True}, {'text': 'Layer diagram explanation'}]}}]})
            answer = server.routed_completion(server.select_ai_route('gemini'), 'System', {'question': 'Explain'}, IMAGE)
            request = factory.return_value.open.call_args.args[0]
            payload = json.loads(request.data)
            self.assertEqual(request.get_header('X-goog-api-key'), 'fake-test-key')
            self.assertNotIn('fake-test-key', request.full_url)
            self.assertNotIn('fake-test-key', request.data.decode())
            self.assertEqual(payload['contents'][0]['parts'][1]['inlineData'], IMAGE)
            self.assertEqual(answer, 'Layer diagram explanation')

    def test_gemini_translation_requests_json_without_truncation(self):
        translated = json.dumps({'translations': ['a' * 10000, 'b' * 10000, 'c' * 10000]})
        with patch.dict(os.environ, ENV, clear=True), patch.object(server, 'build_opener') as factory:
            factory.return_value.open.return_value = provider_reply({'candidates': [{'content': {'parts': [{'text': translated}]}}]})
            answer = server.routed_completion(server.select_ai_route('gemini'), 'Translate', {'texts': ['a', 'b', 'c']}, json_output=True)
            payload = json.loads(factory.return_value.open.call_args.args[0].data)
            self.assertEqual(payload['generationConfig']['responseMimeType'], 'application/json')
            self.assertEqual(payload['generationConfig']['maxOutputTokens'], 8192)
            self.assertEqual(json.loads(answer)['translations'][2], 'c' * 10000)

    def test_provider_errors_do_not_echo_private_response(self):
        request = server.Request('https://provider.example')
        with patch.object(server, 'build_opener') as factory:
            factory.return_value.open.side_effect = HTTPError(request.full_url, 429, 'secret-key-and-private-data', {}, io.BytesIO(b'private prompt'))
            with self.assertRaises(server.ApiError) as caught:
                server.provider_json(request, local=False)
            self.assertEqual(caught.exception.status, 429)
            self.assertNotIn('private', caught.exception.message)
            self.assertNotIn('secret', caught.exception.message)
            factory.return_value.open.return_value = provider_reply({'candidates': []})
            factory.return_value.open.side_effect = None
            with patch.dict(os.environ, ENV, clear=True), self.assertRaises(server.ApiError):
                server.routed_completion(server.select_ai_route('gemini'), 'System', {})


class TutorRouteHTTPTests(unittest.TestCase):
    def setUp(self):
        self.env = patch.dict(os.environ, ENV, clear=True)
        self.env.start()
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        public = root / 'public'
        public.mkdir()
        (public / 'index.html').write_text('<title>Test</title>')
        self.server = server.ThreadingHTTPServer(('127.0.0.1', 0), server.Handler)
        self.origin = 'http://127.0.0.1:' + str(self.server.server_port)
        self.server.app = server.Application(root / 'data' / 'accounts.sqlite3', public, self.origin)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        status, headers, data = self.call('POST', '/api/register', {'email': 'routes@example.test', 'name': 'Learner', 'password': 'test-passphrase-long', 'username': 'routes_learner', 'phone': '+886912345678'})
        self.assertEqual(status, 200, data)
        self.cookie = headers['Set-Cookie'].split(';')[0]

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()
        self.tmp.cleanup()
        self.env.stop()

    def call(self, method, path, data=None, cookie=None):
        connection = http.client.HTTPConnection('127.0.0.1', self.server.server_port, timeout=5)
        headers = {'Origin': self.origin, 'Content-Type': 'application/json'}
        if cookie:
            headers['Cookie'] = cookie
        connection.request(method, path, body=json.dumps(data) if data is not None else None, headers=headers)
        response = connection.getresponse()
        result = response.status, dict(response.getheaders()), json.loads(response.read())
        connection.close()
        return result

    def test_cloud_requires_per_request_consent_before_retrieval_or_provider(self):
        payload = {'route': 'gemini', 'question': 'Explain the layers', 'image': IMAGE}
        with patch.object(server, 'routed_completion', return_value='Answer') as adapter, patch.object(self.server.app.knowledge, 'search', return_value=[]) as retrieval:
            self.assertEqual(self.call('POST', '/api/tutor', payload)[0], 401)
            for consent in (None, False, 'true', 1):
                self.assertEqual(self.call('POST', '/api/tutor', {**payload, 'cloudConsent': consent}, self.cookie)[0], 400)
            adapter.assert_not_called()
            retrieval.assert_not_called()
            status, _, result = self.call('POST', '/api/tutor', {**payload, 'cloudConsent': True}, self.cookie)
            self.assertEqual(status, 200, result)
            self.assertEqual(result['route'], 'gemini')
            self.assertEqual(adapter.call_args.args[3], IMAGE)
            # Prior consent is not remembered by the server.
            self.assertEqual(self.call('POST', '/api/tutor', payload, self.cookie)[0], 400)
            self.assertEqual(adapter.call_count, 1)
        names = [p.name for p in Path(self.tmp.name).rglob('*') if p.is_file()]
        self.assertFalse(any(n.endswith(('.png', '.jpg', '.webp')) for n in names))

    def test_unknown_and_text_only_routes_reject_before_call(self):
        with patch.object(server, 'routed_completion', return_value='Answer') as adapter:
            for route in ('arbitrary-model', 'ollama-text'):
                self.assertEqual(self.call('POST', '/api/tutor', {'route': route, 'question': 'Explain', 'image': IMAGE}, self.cookie)[0], 400)
            adapter.assert_not_called()
            status, _, result = self.call('POST', '/api/tutor', {'route': 'ollama-vision', 'question': 'Explain', 'image': IMAGE}, self.cookie)
            self.assertEqual(status, 200, result)
            self.assertEqual(result['route'], 'ollama-vision')

    def test_translation_with_only_gemini_configured(self):
        with patch.dict(os.environ, {'OLLAMA_TEXT_MODEL': '', 'OLLAMA_VISION_MODEL': ''}), patch.object(server, 'routed_completion', return_value='{"translations":["熱應力"]}') as adapter:
            status, _, result = self.call('POST', '/api/translate', {'texts': ['Thermal stress'], 'language': 'zh-TW'}, self.cookie)
            self.assertEqual(status, 200, result)
            self.assertEqual(result['translations'], ['熱應力'])
            self.assertEqual(adapter.call_args.args[0]['id'], 'gemini')
            self.assertTrue(adapter.call_args.kwargs['json_output'])

    def test_config_and_me_never_return_key(self):
        for path in ('/api/config', '/api/me'):
            status, _, result = self.call('GET', path, cookie=self.cookie)
            self.assertEqual(status, 200)
            self.assertEqual(len(result['aiRoutes']), 3)
            self.assertTrue(result['aiAvailable'])
            self.assertNotIn('fake-test-key', json.dumps(result))


class LauncherConsentTests(unittest.TestCase):
    def test_ollama_missing_model_does_not_pull_without_flag(self):
        repo = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            calls = root / 'calls.txt'
            stub = root / 'ollama'
            stub.write_text('#!/usr/bin/env bash\nprintf "%s\\n" "$*" >> "$TEST_CALLS"\n[[ "$1" == list ]] && exit 0\n[[ "$1" == show ]] && exit 1\n[[ "$1" == pull ]] && exit 7\nexit 2\n')
            stub.chmod(0o700)
            env = {**os.environ, 'PATH': directory + os.pathsep + os.environ['PATH'], 'TEST_CALLS': str(calls)}
            first = subprocess.run(['bash', str(repo / 'run-ai-local.sh'), '--vision'], env=env, capture_output=True, text=True)
            self.assertNotEqual(first.returncode, 0)
            self.assertNotIn('pull', calls.read_text())
            self.assertIn('--download', first.stderr)
            calls.write_text('')
            second = subprocess.run(['bash', str(repo / 'run-ai-local.sh'), '--vision', '--download'], env=env, capture_output=True, text=True)
            self.assertEqual(second.returncode, 7)
            self.assertIn('pull qwen3-vl:2b', calls.read_text())


if __name__ == '__main__':
    unittest.main()
