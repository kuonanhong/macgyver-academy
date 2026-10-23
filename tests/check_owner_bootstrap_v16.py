#!/usr/bin/env python3
"""Opt-in integration check for a real owner kit and the full local V16 site.

Read the login password only from OWNER_TEST_PASSWORD. Never pass it on the
command line, persist it, or include credentials/verifiers in the report.
This script starts its own loopback server and disposable database. It does
not alter the real owner kit, curriculum, or an existing preview server.
"""
import argparse
import contextlib
import http.client
import io
import json
import os
from pathlib import Path
import secrets
import sys
import tempfile
import threading
import time
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from portable import launch_v16, server as APP
from portable.owner_admin import validate_verifier, write_bootstrap


def require(condition, message):
    if not condition:
        raise AssertionError(message)


class IsolatedLauncher:
    """Exercise actual launch_v16.main -> server.main, binding an ephemeral port."""
    def __init__(self, task_root, public, database):
        self.root, self.public, self.database = task_root, public, database
        self.ready = threading.Event()
        self.instance = None
        self.error = None

    def __enter__(self):
        owner = self
        original = APP.ThreadingHTTPServer

        class RecordingServer(original):
            def serve_forever(self, *args, **kwargs):
                owner.instance = self
                owner.ready.set()
                return super().serve_forever(*args, **kwargs)

        self.context = contextlib.ExitStack()
        self.context.enter_context(patch.object(launch_v16, 'ROOT', self.root))
        # Ignore all deployed .env files: this local verification uses no providers.
        self.context.enter_context(patch.object(launch_v16, 'read_dotenv'))
        self.context.enter_context(patch.object(APP, 'read_dotenv'))
        self.context.enter_context(patch.object(APP, 'ThreadingHTTPServer', RecordingServer))
        self.context.enter_context(patch.object(sys, 'argv', [
            'launch_v16.py', '--host', '127.0.0.1', '--port', '0',
            '--database', str(self.database), '--public', str(self.public)]))
        # Intentionally start with the legacy demo setting to verify enforcement.
        self.context.enter_context(patch.dict(os.environ, {
            'COMMERCE_MODE': 'demo', 'BILLING_MODE': 'disabled'}))
        self.context.enter_context(patch.dict(os.environ))
        os.environ.pop('SITE_ORIGIN', None)
        self.context.enter_context(contextlib.redirect_stdout(io.StringIO()))
        self.context.enter_context(contextlib.redirect_stderr(io.StringIO()))

        def run():
            try:
                launch_v16.main()
            except BaseException as error:
                self.error = type(error).__name__
                self.ready.set()

        self.thread = threading.Thread(target=run, daemon=True)
        self.thread.start()
        if not self.ready.wait(30) or self.instance is None or self.error:
            self.context.close()
            raise AssertionError('The isolated V16 launcher did not start successfully.')
        self.origin = f'http://127.0.0.1:{self.instance.server_port}'
        return self

    def __exit__(self, *exception):
        self.instance.shutdown()
        self.thread.join(10)
        self.context.close()
        require(not self.thread.is_alive() and self.error is None,
                'The isolated server did not shut down cleanly.')

    def request(self, method, path, payload=None, cookie=''):
        client = http.client.HTTPConnection('127.0.0.1', self.instance.server_port, timeout=30)
        headers = {'Origin': self.origin, 'Content-Type': 'application/json'}
        if cookie:
            headers['Cookie'] = cookie
        try:
            client.request(method, path, json.dumps(payload) if payload is not None else None, headers)
            response = client.getresponse()
            status, headers, body = response.status, dict(response.getheaders()), response.read()
            try:
                value = json.loads(body)
            except ValueError:
                value = None
            return status, headers, value
        finally:
            client.close()


def assert_preview(value, course):
    require(value.get('partial') is True, 'Guest course must be marked partial.')
    require(value['stages'][0]['steps'] == course['stages'][0]['steps'],
            'The guest must receive the complete first stage.')
    for stage in value['stages'][1:]:
        for step in stage['steps']:
            require(step.get('locked') is True and not any(step.get(k) for k in (
                'instruction', 'instructionEn', 'objective', 'objectiveEn',
                'observation', 'observationEn', 'failure', 'failureEn', 'check', 'checkEn', 'knowledge')),
                'A guest received course content beyond the first stage.')


def verify(bootstrap, report, bootstrap_only=False):
    checks = report['checks']
    password = os.environ.pop('OWNER_TEST_PASSWORD', None)
    require(bootstrap_only or bool(password), 'OWNER_TEST_PASSWORD is required for the full login check.')
    require(bootstrap.stat().st_size <= 8192, 'Owner bootstrap exceeds its size limit.')
    value = json.loads(bootstrap.read_text('utf-8'))
    username, expected_salt, expected_digest = validate_verifier(value)
    public = ROOT / 'public/academy'
    owner_index = json.loads((public / 'data/lazy/owner-index.json').read_text('utf-8'))
    descriptor = owner_index['courses']['b301']
    course = json.loads((public / descriptor['file']).read_text('utf-8'))
    require(len(course['stages']) > 1, 'The full b301 source must contain multiple stages.')
    report['course'] = {'id': 'b301', 'stages': len(course['stages']),
                        'fullSteps': sum(len(stage['steps']) for stage in course['stages']),
                        'previewSteps': len(course['stages'][0]['steps'])}
    with tempfile.TemporaryDirectory(prefix='v16-owner-kit-check-') as directory:
        temporary = Path(directory)
        database = temporary / 'private/accounts.sqlite3'
        write_bootstrap(temporary / 'owner-private/owner-bootstrap-v16.json', value)
        with IsolatedLauncher(temporary, public, database) as running:
            app = running.instance.app
            require(app.commerce.protected, 'The launcher failed to enforce protected mode.')
            checks['launcherForcesProtectedMode'] = True
            with app.db() as db:
                row = db.execute('SELECT id,salt,password_hash,role FROM users WHERE username=?', (username,)).fetchone()
                require(row is not None and row['role'] == 'owner', 'Bootstrap did not create an owner.')
                require(row['salt'] == expected_salt and row['password_hash'] == expected_digest,
                        'The imported verifier differs from the supplied private bootstrap.')
                require(db.execute('SELECT count(*) FROM owner_admin_audit').fetchone()[0] == 1,
                        'Expected one initial provisioning audit entry.')
                user_id = row['id']
            checks['actualPrivateBootstrapImported'] = True
            status, _, guest = running.request('GET', '/api/courses/b301')
            require(status == 200, 'Guest course request failed.')
            assert_preview(guest, course)
            checks['guestFirstStageOnly'] = True
            require(running.request('GET', '/' + descriptor['file'])[0] == 403,
                    'Raw owner lesson is publicly accessible.')
            checks['rawOwnerCourseDenied'] = True
            if not bootstrap_only:
                status, headers, response = running.request('POST', '/api/login', {
                    'login': username, 'password': password})
                del password
                require(status == 200 and response.get('user', {}).get('role') == 'owner'
                        and response['user'].get('owner') is True,
                        'Actual owner login did not return owner authority.')
                require('HttpOnly' in headers.get('Set-Cookie', ''), 'Owner session cookie is not HttpOnly.')
                cookie = headers['Set-Cookie'].split(';', 1)[0]
                checks['actualOwnerPasswordLogin'] = True
                for path in ('/api/courses/b301', '/api/curriculum?courseId=b301'):
                    status, headers, full = running.request('GET', path, cookie=cookie)
                    require(status == 200 and full.get('stages') == course['stages'],
                            'Owner did not receive all full b301 stages.')
                    require('no-store' in headers.get('Cache-Control', ''),
                            'Owner lesson response is not marked no-store.')
                checks['ownerFullB301BothEndpoints'] = True
                account = running.request('GET', '/api/billing/me', cookie=cookie)[2]
                require(account.get('owner') is True and account.get('active') is True
                        and account.get('accessType') == 'owner' and not account['orders']
                        and not account['entitlements'], 'Owner access unexpectedly requires payment.')
                checks['ownerAccessWithoutPayment'] = True
                require(running.request('POST', '/api/logout', {}, cookie)[0] == 200, 'Owner logout failed.')
                require(running.request('GET', '/api/billing/me', cookie=cookie)[0] == 401,
                        'Logged-out owner cookie retained account authority.')
                status, headers, guest = running.request('GET', '/api/courses/b301', cookie=cookie)
                require(status == 200, 'Logged-out guest request failed.')
                assert_preview(guest, course)
                checks['logoutRevokesAuthorityAndRestoresPreview'] = True
            else:
                checks['actualOwnerPasswordLogin'] = 'NOT_RUN: bootstrap-only mode'

            # Model an owner who has changed their password since the kit was
            # created. Use random verifier bytes, never a persisted password.
            changed_salt, changed_digest = secrets.token_bytes(32), secrets.token_bytes(32)
            with app.db() as db:
                db.execute('UPDATE users SET salt=?,password_hash=? WHERE id=?',
                           (changed_salt, changed_digest, user_id))
                db.execute('INSERT INTO sessions VALUES(?,?,?)',
                           ('existing-session-preservation-fixture', user_id, int(time.time()) + 3600))
        with IsolatedLauncher(temporary, public, database) as restarted:
            with restarted.instance.app.db() as db:
                row = db.execute('SELECT id,salt,password_hash,role FROM users WHERE username=?', (username,)).fetchone()
                require(tuple(row) == (user_id, changed_salt, changed_digest, 'owner'),
                        'Restart reset an existing owner account or its changed password.')
                require(db.execute('SELECT count(*) FROM owner_admin_audit').fetchone()[0] == 1,
                        'Restart reprovisioned an existing owner.')
                require(db.execute('SELECT count(*) FROM sessions WHERE token_hash=?',
                                   ('existing-session-preservation-fixture',)).fetchone()[0] == 1,
                        'Restart revoked an existing owner session.')
            checks['restartPreservesExistingOwnerPasswordAndSession'] = True
    report['status'] = 'BOOTSTRAP_ONLY_PASS' if bootstrap_only else 'PASS'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bootstrap', required=True, type=Path)
    parser.add_argument('--bootstrap-only', action='store_true', help='Skip password login; report explicitly remains partial')
    parser.add_argument('--report', type=Path, default=ROOT / 'docs/VALIDATION_OWNER_BOOTSTRAP_V16.json')
    args = parser.parse_args()
    report = {'status': 'FAIL', 'scope': 'Actual private owner bootstrap and full V16 source via isolated loopback HTTP server',
              'entryPoint': 'portable.launch_v16.main -> portable.server.main',
              'database': 'temporary; removed after verification', 'bind': '127.0.0.1, ephemeral port',
              'checks': {}, 'externalCalls': False,
              'secretsInReport': False, 'curriculumModified': False}
    try:
        verify(args.bootstrap, report, args.bootstrap_only)
    except BaseException as error:
        # Fixed test messages are safe; never emit HTTP payloads, database rows,
        # private bootstrap content, tracebacks or credential-bearing locals.
        report['failureType'] = type(error).__name__
        if isinstance(error, AssertionError):
            report['failure'] = str(error)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Owner bootstrap integration: ' + report['status'])
    return 0 if report['status'] in ('PASS', 'BOOTSTRAP_ONLY_PASS') else 1


if __name__ == '__main__':
    raise SystemExit(main())
