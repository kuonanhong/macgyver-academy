#!/usr/bin/env python3
"""Wait for the current run's complete Pages artifact metadata (read-only).

GitHub may briefly omit a just-uploaded artifact from its run-artifact listing.
Require two consecutive matching ID/size/SHA256 observations before deployment.
Only GET https://api.github.com/repos/OWNER/REPO/actions/runs/RUN/artifacts is
used. No redirects, downloads, dispatches or retries of deployment are performed.
GITHUB_TOKEN is read only from the environment and is never printed. Python 3
standard library only; Actions read permission is sufficient for this endpoint:
https://docs.github.com/en/rest/actions/artifacts#list-workflow-run-artifacts
"""
from __future__ import annotations
import json
import os
import re
import signal
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.request import HTTPRedirectHandler, Request, build_opener

TIMEOUT_SECONDS = 90
POLL_SECONDS = 5
MAX_RESPONSE_BYTES = 2_000_000


class WaitError(RuntimeError):
    """Safe, deliberately non-sensitive failure message."""


class MetadataPending(WaitError):
    """A transient API response that must reset the stable-observation count."""


class WaitTimeout(WaitError):
    pass


class NoRedirects(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise WaitError('Artifact API redirected; refusing to forward credentials.')


def environment():
    repository = os.environ.get('GITHUB_REPOSITORY', '')
    run_id = os.environ.get('GITHUB_RUN_ID', '')
    token = os.environ.get('GITHUB_TOKEN', '')
    if (not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', repository)
            or any(part in ('.', '..') for part in repository.split('/'))
            or not re.fullmatch(r'[1-9][0-9]*', run_id)):
        raise WaitError('Valid GITHUB_REPOSITORY and GITHUB_RUN_ID are required.')
    if not token or '\r' in token or '\n' in token:
        raise WaitError('GITHUB_TOKEN must be provided through the step environment.')
    return repository, run_id, token


def fetch_artifacts(repository, run_id, token, remaining, opener=None):
    # This job produces only two artifacts. A non-complete first page is retried,
    # never treated as proof of uniqueness; no untrusted Link URL is followed.
    url = f'https://api.github.com/repos/{repository}/actions/runs/{run_id}/artifacts?per_page=100&page=1'
    request = Request(url, method='GET', headers={
        'Authorization': 'Bearer ' + token,
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28',
        'User-Agent': 'macgyver-pages-artifact-wait-v34',
        'Cache-Control': 'no-cache',
    })
    client = opener or build_opener(NoRedirects())
    try:
        with client.open(request, timeout=max(.01, min(10, remaining))) as response:
            if response.status != 200:
                raise WaitError('Artifact API returned an unexpected response status.')
            body = response.read(MAX_RESPONSE_BYTES + 1)
        if len(body) > MAX_RESPONSE_BYTES:
            raise WaitError('Artifact metadata response exceeded the bounded size.')
        return json.loads(body)
    except HTTPError as error:
        code = error.code
        error.close()
        if code in (401, 403):
            raise WaitError(f'Artifact API authorization failed (HTTP {code}); check Actions read permission.') from None
        if code in (404, 408, 429, 500, 502, 503, 504):
            raise MetadataPending(f'Artifact metadata is temporarily unavailable (HTTP {code}).') from None
        raise WaitError(f'Artifact API request failed (HTTP {code}).') from None
    except (URLError, TimeoutError, OSError):
        raise MetadataPending('Artifact metadata request temporarily failed.') from None
    except (json.JSONDecodeError, UnicodeDecodeError):
        raise MetadataPending('Artifact metadata is not yet readable JSON.') from None


def candidate(data, run_id):
    if not isinstance(data, dict) or not isinstance(data.get('artifacts'), list):
        raise MetadataPending('Artifact listing metadata is incomplete.')
    artifacts = data['artifacts']
    if (type(data.get('total_count')) is not int or data['total_count'] < 0
            or data['total_count'] != len(artifacts) or len(artifacts) > 100
            or any(not isinstance(a, dict) for a in artifacts)):
        raise MetadataPending('A complete artifact listing is not yet visible.')
    matches = [a for a in artifacts if a.get('name') == 'github-pages']
    if len(matches) > 1:
        raise WaitError('Multiple github-pages artifacts exist in this run; refusing an ambiguous deployment.')
    if not matches:
        raise MetadataPending('The github-pages artifact is not yet visible.')
    artifact = matches[0]
    if artifact.get('expired') is True:
        raise WaitError('The github-pages artifact is expired.')
    digest = artifact.get('digest')
    if (type(artifact.get('id')) is not int or artifact['id'] <= 0
            or type(artifact.get('size_in_bytes')) is not int or artifact['size_in_bytes'] <= 0
            or artifact.get('expired') is not False
            or not isinstance(digest, str) or not re.fullmatch(r'sha256:[0-9a-fA-F]{64}', digest)):
        raise MetadataPending('Pages artifact ID, size, expiration or SHA256 metadata is incomplete.')
    workflow_run = artifact.get('workflow_run')
    if workflow_run is not None and (not isinstance(workflow_run, dict) or str(workflow_run.get('id')) != str(run_id)):
        raise WaitError('Artifact metadata identifies a different workflow run.')
    return artifact['id'], artifact['size_in_bytes'], digest.lower()


def wait_for_artifact(fetch, run_id, timeout=TIMEOUT_SECONDS, interval=POLL_SECONDS,
                      clock=time.monotonic, sleep=time.sleep, emit=print):
    deadline = clock() + timeout
    previous = None
    observations = 0
    attempts = 0
    while clock() < deadline:
        attempts += 1
        try:
            current = candidate(fetch(deadline - clock()), run_id)
        except MetadataPending as error:
            current = None
            emit(f'Pages artifact check {attempts}: {error}')
        if clock() >= deadline:
            break
        observations = observations + 1 if current is not None and current == previous else (1 if current else 0)
        previous = current
        if observations >= 2:
            result = {'status': 'PASS', 'artifact': 'github-pages', 'id': current[0],
                      'bytes': current[1], 'sha256': current[2], 'stableObservations': observations,
                      'attempts': attempts, 'deploymentPerformed': False}
            emit(json.dumps(result))
            return result
        if current:
            emit(f'Pages artifact check {attempts}: complete metadata observed; waiting for a second matching observation.')
        remaining = deadline - clock()
        if remaining > 0:
            sleep(min(interval, remaining))
    raise WaitTimeout('Pages artifact did not become uniquely visible with stable complete metadata within 90 seconds; deployment must not proceed.')


def main():
    def timeout_handler(signum, frame):
        raise WaitTimeout('Pages artifact visibility check exceeded its 90-second limit; deployment must not proceed.')
    previous_handler = signal.signal(signal.SIGALRM, timeout_handler)
    signal.setitimer(signal.ITIMER_REAL, TIMEOUT_SECONDS)
    try:
        repository, run_id, token = environment()
        client = build_opener(NoRedirects())
        wait_for_artifact(lambda remaining: fetch_artifacts(repository, run_id, token, remaining, client), run_id)
        return 0
    except WaitError as error:
        print('Pages artifact check failed: ' + str(error), file=sys.stderr)
        return 1
    except Exception:
        # Never print request objects, API response bodies, headers or tokens.
        print('Pages artifact check failed unexpectedly; deployment must not proceed.', file=sys.stderr)
        return 1
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, previous_handler)


if __name__ == '__main__':
    sys.exit(main())
