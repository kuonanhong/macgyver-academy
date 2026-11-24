#!/usr/bin/env python3
"""Offline regression tests for Pages artifact and publication controls."""
from pathlib import Path
import contextlib
import importlib.util
import io
import json
import subprocess
import tarfile
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


check = module('pages_check_v28', ROOT / 'tools/check-pages-artifact-v28.py')
doctor = module('pages_doctor_v28', ROOT / 'tools/pages-doctor-v28.py')
exporter = module('pages_export_v28', ROOT / 'tools/export-preview-v21.py')


class ArtifactTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='pages 中文 paths ')
        self.root = Path(self.temporary.name) / 'output'
        self.root.mkdir()
        (self.root / 'index.html').write_text('<html>公開首階段</html>')
        (self.root / '.nojekyll').touch()
        (self.root / 'preview-manifest.json').write_text(json.dumps({
            'mode': 'first-stage-preview', 'memberBodies': 0, 'httpOnly': True}))

    def tearDown(self):
        self.temporary.cleanup()

    def test_valid_payload_and_tar_budget(self):
        report = check.inspect(self.root)
        buffer = io.BytesIO()
        with tarfile.open(fileobj=buffer, mode='w') as archive:
            archive.add(self.root, arcname='.')
        self.assertEqual(report['files'], 3)
        self.assertEqual(report['uncompressedBytes'], sum(p.stat().st_size for p in self.root.iterdir()))
        self.assertGreaterEqual(report['tarUpperBoundBytes'], buffer.tell())

    def test_budget_stops_before_upload(self):
        with self.assertRaisesRegex(ValueError, '容量'):
            check.inspect(self.root, max_bytes=20)

    def test_source_tree_blocked(self):
        (self.root / 'portable').mkdir()
        with self.assertRaises(ValueError):
            check.inspect(self.root)

    def test_private_key_blocked(self):
        (self.root / 'access.key').write_bytes(b'not a real key')
        with self.assertRaises(ValueError):
            check.inspect(self.root)

    def test_symlink_blocked(self):
        (self.root / 'shortcut').symlink_to(self.root / 'index.html')
        with self.assertRaises(ValueError):
            check.inspect(self.root)

    def test_member_manifest_blocked(self):
        (self.root / 'preview-manifest.json').write_text(json.dumps({'mode': 'full', 'memberBodies': 5}))
        with self.assertRaises(ValueError):
            check.inspect(self.root)

    def test_hidden_secret_blocked(self):
        (self.root / '.env').write_text('EXAMPLE=not-a-secret')
        with self.assertRaises(ValueError):
            check.inspect(self.root)


class DoctorTests(unittest.TestCase):
    repo = 'example/academy'
    sha = 'a' * 40

    def test_default_inspection_never_mutates(self):
        calls = []
        def fake(repo, endpoint, **kwargs):
            calls.append((endpoint, kwargs))
            return {'build_type': 'legacy'}
        with patch.object(doctor, 'api', fake), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(doctor.ensure_actions(self.repo)['build_type'], 'legacy')
        self.assertEqual(calls, [('pages', {})])

    def test_explicit_config_changes_only_build_type_and_verifies(self):
        calls = []
        def fake(repo, endpoint, **kwargs):
            calls.append((endpoint, kwargs))
            return {'build_type': 'workflow' if len(calls) == 3 else 'legacy'}
        with patch.object(doctor, 'api', fake), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(doctor.ensure_actions(self.repo, True)['build_type'], 'workflow')
        self.assertEqual(calls[1], ('pages', {'method': 'PUT', 'payload': {'build_type': 'workflow'}}))
        self.assertEqual(len(calls), 3)

    def test_failed_configuration_not_reported_as_success(self):
        with patch.object(doctor, 'api', return_value={'build_type': 'legacy'}), contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaises(doctor.PagesError):
                doctor.ensure_actions(self.repo, True)

    def publication(self, *, conclusion='success', no_wait=False, old_api=False, mismatch=False,
                    unsettled_reads=0, not_found_reads=0):
        calls, state, clock = [], {'reads': 0}, [0]
        def fake(repo, endpoint, **kwargs):
            calls.append((endpoint, kwargs))
            if endpoint == 'actions/workflows/pages.yml':
                return {'state': 'active', 'path': '.github/workflows/pages.yml'}
            if endpoint == 'commits/main':
                return {'sha': self.sha}
            if endpoint.endswith('/dispatches'):
                state['request_id'] = kwargs['payload']['inputs']['request_id']
                return {} if old_api else {'workflow_run_id': 42}
            run = {'id': 42, 'head_sha': ('b' * 40 if mismatch else self.sha),
                   'head_branch': 'main', 'path': '.github/workflows/pages.yml',
                   'event': 'workflow_dispatch', 'display_title': 'Pages · ' + state['request_id'],
                   'status': 'completed', 'conclusion': conclusion}
            if endpoint == 'actions/runs/42':
                state['reads'] += 1
                if state['reads'] <= not_found_reads:
                    raise doctor.PagesError('GitHub API 失敗：Not Found (HTTP 404)', http_status=404)
                if state['reads'] <= not_found_reads + unsettled_reads:
                    return {'id': 42, 'head_sha': self.sha, 'status': 'queued'}
            return {'workflow_runs': [run]} if '/runs?' in endpoint else run
        with patch.object(doctor, 'api', fake), patch.object(doctor.time, 'monotonic', side_effect=lambda: clock[0]), \
                patch.object(doctor.time, 'sleep', side_effect=lambda seconds: clock.__setitem__(0, clock[0] + seconds)), \
                contextlib.redirect_stdout(io.StringIO()):
            result = doctor.publish(self.repo, no_wait=no_wait)
        self.assertEqual(sum(endpoint.endswith('/dispatches') for endpoint, _ in calls), 1)
        if unsettled_reads or not_found_reads:
            self.assertEqual(state['reads'], unsettled_reads + not_found_reads + 1)
            self.assertFalse(any('/runs?' in endpoint for endpoint, _ in calls))
        return result

    def test_publish_waits_for_success_of_exact_run(self):
        result = self.publication()
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['runId'], 42)
        self.assertEqual(result['commit'], self.sha)

    def test_deploy_failure_is_failure(self):
        with self.assertRaisesRegex(doctor.PagesError, '未成功'):
            self.publication(conclusion='failure')

    def test_no_wait_never_claims_success(self):
        self.assertEqual(self.publication(no_wait=True)['status'], 'submitted')

    def test_old_api_204_correlates_unique_request(self):
        self.assertEqual(self.publication(old_api=True)['status'], 'success')

    def test_other_commit_cannot_satisfy_publish(self):
        with self.assertRaisesRegex(doctor.PagesError, '版本不符'):
            self.publication(mismatch=True)

    def test_initial_partial_metadata_recovers_without_redispatch(self):
        result = self.publication(unsettled_reads=2)
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['runId'], 42)

    def test_no_wait_still_requires_settled_identity(self):
        self.assertEqual(self.publication(unsettled_reads=1, no_wait=True)['status'], 'submitted')

    def test_initial_404_then_partial_identity_recovers_without_redispatch(self):
        result = self.publication(not_found_reads=2, unsettled_reads=1)
        self.assertEqual((result['status'], result['runId']), ('success', 42))

    def test_permanent_404_is_bounded_and_logs_known_run(self):
        clock, calls, output = [0], [], io.StringIO()
        def fake(repo, endpoint, **kwargs):
            calls.append((endpoint, kwargs))
            self.assertLessEqual(kwargs['timeout'], 90 - clock[0])
            raise doctor.PagesError('Not Found (HTTP 404)', http_status=404)
        with patch.object(doctor, 'api', fake), \
                patch.object(doctor.time, 'monotonic', side_effect=lambda: clock[0]), \
                patch.object(doctor.time, 'sleep', side_effect=lambda seconds: clock.__setitem__(0, clock[0] + seconds)), \
                contextlib.redirect_stdout(output):
            with self.assertRaisesRegex(doctor.PagesError, '90 秒'):
                doctor.wait_for_run_identity(self.repo, 42, self.sha, 'main', 'macgyver-fixture')
        self.assertEqual(clock[0], 90)
        self.assertEqual(len(calls), 30)
        self.assertEqual({endpoint for endpoint, _ in calls}, {'actions/runs/42'})
        self.assertTrue(all('method' not in kwargs for _, kwargs in calls))
        self.assertIn('https://github.com/example/academy/actions/runs/42', output.getvalue())

    def test_identity_permission_failures_do_not_retry(self):
        for status in (401, 403, 429, 500, None):
            with self.subTest(status=status), patch.object(doctor, 'api', side_effect=doctor.PagesError('failure', http_status=status)) as fake, \
                    patch.object(doctor.time, 'sleep') as sleeper, contextlib.redirect_stdout(io.StringIO()):
                with self.assertRaisesRegex(doctor.PagesError, 'failure'):
                    doctor.wait_for_run_identity(self.repo, 42, self.sha, 'main', 'macgyver-fixture')
                self.assertEqual(fake.call_count, 1)
                sleeper.assert_not_called()

    def test_api_preserves_http_status_for_read_retry_decision(self):
        result = subprocess.CompletedProcess([], 1, '', 'gh: Not Found (HTTP 404)\n')
        with patch.object(doctor.subprocess, 'run', return_value=result):
            with self.assertRaises(doctor.PagesError) as raised:
                doctor.api(self.repo, 'actions/runs/42')
        self.assertEqual(raised.exception.http_status, 404)

    def test_permanent_identity_mismatch_is_bounded_and_reads_only_same_id(self):
        expected = {'id': 42, 'head_sha': self.sha, 'head_branch': 'main',
                    'path': '.github/workflows/pages.yml', 'event': 'workflow_dispatch',
                    'display_title': 'Pages · macgyver-fixture', 'status': 'completed',
                    'conclusion': 'success'}
        for field, value in [('id', 43), ('head_sha', 'b' * 40), ('head_branch', 'other'),
                             ('path', '.github/workflows/other.yml'), ('event', 'push'),
                             ('display_title', 'Pages · unrelated-request')]:
            with self.subTest(field=field):
                clock, calls = [0], []
                def fake(repo, endpoint, **kwargs):
                    calls.append((endpoint, kwargs))
                    self.assertLessEqual(kwargs['timeout'], 90 - clock[0])
                    return {**expected, field: value}
                with patch.object(doctor, 'api', fake), \
                        patch.object(doctor.time, 'monotonic', side_effect=lambda: clock[0]), \
                        patch.object(doctor.time, 'sleep', side_effect=lambda seconds: clock.__setitem__(0, clock[0] + seconds)), \
                        contextlib.redirect_stdout(io.StringIO()):
                    with self.assertRaisesRegex(doctor.PagesError, '90 秒'):
                        doctor.wait_for_run_identity(self.repo, 42, self.sha, 'main', 'macgyver-fixture')
                self.assertEqual(clock[0], 90)
                self.assertEqual(len(calls), 30)
                self.assertEqual({endpoint for endpoint, _ in calls}, {'actions/runs/42'})
                self.assertTrue(all('method' not in kwargs for _, kwargs in calls))


class PublicMetadataTests(unittest.TestCase):
    def export(self, *, field=None, wrong_experiment=False):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source, destination = root / 'source', root / 'output'
            (source / 'data').mkdir(parents=True)
            destination.mkdir()
            languages = {'version': '28.0.0', 'targets': ['zh-TW', 'en', 'ja'],
                         'authored': ['zh-TW', 'en'], 'bundledHudTargets': ['zh-TW', 'en'],
                         'sourceSelection': 'browser preference', 'otherTargets': 'provider-dependent'}
            if field:
                languages[field] = [{'member': 'must not be exported'}]
            (source / 'data/languages-v28.json').write_text(json.dumps(languages))
            scene = {'id': 'xp-comm-v28', 'category': 'computing', 'specialty': 'communications',
                     'curriculumVersion': '28.0.0', 'chapters': [
                         {'id': 'test', 'labExperiment': 'eval' if wrong_experiment else 'comm-packet-delay'}]}
            (source / 'data/experiences-v21.json').write_text(json.dumps({
                'version': 21, 'domains': [], 'assets': [], 'experiences': [scene]}))
            names = exporter.public_game_data(source, destination)
            self.assertEqual(json.loads((destination / 'data/languages-v28.json').read_text()), languages)
            self.assertFalse((destination / 'data/languages-v28.js').exists())
            return names

    def test_known_language_metadata_and_communications_lab_are_public(self):
        self.assertEqual(self.export(), ['experiences-v21.json', 'languages-v28.json'])

    def test_member_lesson_cannot_hide_in_language_metadata(self):
        with self.assertRaises(ValueError):
            self.export(field='knowledge')

    def test_unknown_metadata_field_rejected(self):
        with self.assertRaises(ValueError):
            self.export(field='privateToken')

    def test_unknown_communications_experiment_rejected(self):
        with self.assertRaises(ValueError):
            self.export(wrong_experiment=True)


if __name__ == '__main__':
    unittest.main(verbosity=2)
