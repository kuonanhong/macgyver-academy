#!/usr/bin/env python3
"""Offline regression tests; no GitHub requests, credentials or deployments."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import unittest
from unittest.mock import patch
from urllib.error import HTTPError

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('wait_pages', ROOT/'tools/wait-pages-artifact-v34.py')
wait = importlib.util.module_from_spec(spec); spec.loader.exec_module(wait)


def listing(**changes):
    artifact = {'id': 7, 'name': 'github-pages', 'size_in_bytes': 1234,
                'expired': False, 'digest': 'sha256:' + 'a'*64, 'workflow_run': {'id': 42}}
    artifact.update(changes)
    return {'total_count': 1, 'artifacts': [artifact]}


class FakeClock:
    def __init__(self): self.now = 0
    def clock(self): return self.now
    def sleep(self, seconds): self.now += seconds


class VisibilityTests(unittest.TestCase):
    def run_checks(self, snapshots, timeout=90):
        clock = FakeClock(); calls = []; messages = []; queue = iter(snapshots)
        def fetch(remaining):
            calls.append(remaining)
            value = next(queue)
            if isinstance(value, Exception): raise value
            return value
        result = wait.wait_for_artifact(fetch, 42, timeout=timeout, clock=clock.clock, sleep=clock.sleep, emit=messages.append)
        return result, calls, messages, clock.now

    def test_upload_visibility_delay_then_two_complete_observations(self):
        result, calls, messages, seconds = self.run_checks([
            {'total_count': 1, 'artifacts': [{'id': 8, 'name': 'pages-payload-report'}]},
            listing(digest=None), listing(size_in_bytes=0), listing(), listing()])
        self.assertEqual((result['status'], result['attempts'], seconds), ('PASS', 5, 20))
        self.assertEqual(result['stableObservations'], 2)
        self.assertFalse(result['deploymentPerformed'])

    def test_changed_id_size_or_digest_requires_new_stable_pair(self):
        for changed in (listing(id=9), listing(size_in_bytes=2345), listing(digest='sha256:'+'b'*64)):
            with self.subTest(changed=changed):
                result, _, _, seconds = self.run_checks([listing(), changed, changed])
                self.assertEqual((result['attempts'], seconds), (3, 10))

    def test_transient_error_resets_stability(self):
        result, _, _, _ = self.run_checks([listing(), wait.MetadataPending('HTTP 404'), listing(), listing()])
        self.assertEqual(result['attempts'], 4)

    def test_duplicates_fail_closed(self):
        data = listing(); data['artifacts'].append(listing(id=9)['artifacts'][0]); data['total_count'] = 2
        with self.assertRaisesRegex(wait.WaitError, 'Multiple'):
            self.run_checks([data])

    def test_expired_or_wrong_run_fails(self):
        for data in (listing(expired=True), listing(workflow_run={'id': 43})):
            with self.subTest(data=data), self.assertRaises(wait.WaitError): self.run_checks([data])

    def test_missing_metadata_and_incomplete_pagination_never_pass(self):
        for data in ({}, listing(expired=None), listing(id=True), listing(digest='sha256:bad'), {'total_count': 101, 'artifacts': []}):
            with self.subTest(data=data), self.assertRaises(wait.WaitTimeout): self.run_checks([data]*18)

    def test_timeout_is_bounded_without_extra_attempt(self):
        clock = FakeClock(); calls = []; messages = []
        def fetch(remaining): calls.append(remaining); return {'total_count': 0, 'artifacts': []}
        with self.assertRaises(wait.WaitTimeout):
            wait.wait_for_artifact(fetch, 42, clock=clock.clock, sleep=clock.sleep, emit=messages.append)
        self.assertEqual((clock.now, len(calls)), (90, 18))
        self.assertFalse(any('"status": "PASS"' in m for m in messages))

    def test_auth_failure_is_not_retried(self):
        with self.assertRaisesRegex(wait.WaitError, 'authorization'):
            self.run_checks([wait.WaitError('authorization failed')])


class HttpTests(unittest.TestCase):
    def test_only_current_run_get_and_token_header(self):
        captured = []
        class Response:
            status = 200
            def __enter__(self): return self
            def __exit__(self, *args): pass
            def read(self, limit): self.limit = limit; return json.dumps(listing()).encode()
        class Opener:
            def open(self, request, timeout): captured.append((request, timeout)); return Response()
        self.assertEqual(wait.fetch_artifacts('owner/repo', '42', 'fake-secret', 4, Opener()), listing())
        request, timeout = captured[0]
        self.assertEqual(request.get_method(), 'GET')
        self.assertEqual(request.full_url, 'https://api.github.com/repos/owner/repo/actions/runs/42/artifacts?per_page=100&page=1')
        self.assertEqual(request.get_header('Authorization'), 'Bearer fake-secret')
        self.assertEqual(timeout, 4)

    def test_http_auth_status_fails_without_echoing_secret(self):
        for code in (401, 403):
            class Opener:
                def open(self, request, timeout): raise HTTPError(request.full_url, code, 'fake-secret', {}, None)
            with self.subTest(code=code), self.assertRaises(wait.WaitError) as error:
                wait.fetch_artifacts('owner/repo', '42', 'fake-secret', 5, Opener())
            self.assertNotIsInstance(error.exception, wait.MetadataPending)
            self.assertNotIn('fake-secret', str(error.exception))

    def test_http_404_is_transient(self):
        class Opener:
            def open(self, request, timeout): raise HTTPError(request.full_url, 404, 'ignored body', {}, None)
        with self.assertRaises(wait.MetadataPending): wait.fetch_artifacts('owner/repo', '42', 'fake', 5, Opener())

    def test_redirect_never_creates_a_followup_request(self):
        with self.assertRaisesRegex(wait.WaitError, 'redirected'):
            wait.NoRedirects().redirect_request(None, None, 302, '', {}, 'https://other.example/')

    def test_main_auth_failure_exits_nonzero_without_token_output(self):
        output = io.StringIO()
        with patch.dict(wait.os.environ, {'GITHUB_REPOSITORY':'owner/repo','GITHUB_RUN_ID':'42','GITHUB_TOKEN':'fake-secret'}, clear=True), patch.object(wait, 'fetch_artifacts', side_effect=wait.WaitError('Artifact API authorization failed (HTTP 403).')), contextlib.redirect_stderr(output), contextlib.redirect_stdout(output):
            self.assertEqual(wait.main(), 1)
        self.assertNotIn('fake-secret', output.getvalue())
        self.assertNotIn('PASS', output.getvalue())


if __name__ == '__main__': unittest.main()
