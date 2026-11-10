#!/usr/bin/env python3
"""Read Pages status; explicitly configure Actions and publish one verified run."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time
from urllib.parse import quote
import uuid

WORKFLOW = 'pages.yml'
API_VERSION = '2026-03-10'


class PagesError(RuntimeError):
    pass


def api(repo, endpoint, *, method='GET', payload=None):
    command = ['gh', 'api', '--hostname', 'github.com', '--method', method,
               '-H', 'Accept: application/vnd.github+json',
               '-H', 'X-GitHub-Api-Version: ' + API_VERSION,
               'repos/' + repo + '/' + endpoint]
    if payload is not None:
        command += ['--input', '-']
    result = subprocess.run(command, input=json.dumps(payload) if payload is not None else None,
                            capture_output=True, text=True, encoding='utf-8', timeout=60)
    if result.returncode:
        # gh errors may include local context. Show only the short final message;
        # authentication tokens are never read, logged, or placed in arguments.
        detail = result.stderr.strip().splitlines()
        raise PagesError('GitHub API 失敗：' + (detail[-1][:400] if detail else endpoint))
    if not result.stdout.strip():
        return {}
    return json.loads(result.stdout)


def workflow_path(run):
    return str(run.get('path', '')).split('@', 1)[0]


def validate_run(run, sha, branch, request_id):
    if (run.get('head_sha') != sha or run.get('head_branch') != branch
            or workflow_path(run) != '.github/workflows/pages.yml'
            or run.get('event') != 'workflow_dispatch'
            or request_id not in str(run.get('display_title', ''))):
        raise PagesError('工作識別／版本不符；未將其他部署當成此次成功。')


def ensure_actions(repo, configure=False):
    settings = api(repo, 'pages')
    current = settings.get('build_type')
    print('Pages 發布來源：' + str(current or '未回傳'), flush=True)
    if current != 'workflow' and configure:
        if current != 'legacy':
            raise PagesError('未知 Pages 發布設定；請先檢查 https://github.com/' + repo + '/settings/pages')
        # Change exactly one setting; preserve CNAME, HTTPS, and every other
        # repository/site field. No branch, workflow or deployment is deleted.
        api(repo, 'pages', method='PUT', payload={'build_type': 'workflow'})
        settings = api(repo, 'pages')
        if settings.get('build_type') != 'workflow':
            raise PagesError('Pages 尚未切換成 GitHub Actions，已停止發布。')
        print('已將 Pages Source 切換為 GitHub Actions。', flush=True)
    return settings


def find_requested_run(repo, sha, branch, request_id, deadline):
    while time.monotonic() < deadline:
        result = api(repo, 'actions/workflows/' + WORKFLOW + '/runs?event=workflow_dispatch&branch='
                     + quote(branch, safe='') + '&per_page=100')
        matches = [run for run in result.get('workflow_runs', [])
                   if request_id in str(run.get('display_title', ''))]
        if len(matches) > 1:
            raise PagesError('找到重複工作識別，請查看 Actions；未自動重複發布。')
        if matches:
            validate_run(matches[0], sha, branch, request_id)
            return matches[0]
        time.sleep(3)
    raise PagesError('已送出發布，但尚未取得工作編號；請查看 Actions，不要連續重複提交。')


def publish(repo, branch='main', wait_seconds=1800, no_wait=False):
    workflow = api(repo, 'actions/workflows/' + WORKFLOW)
    if workflow.get('state') != 'active' or workflow.get('path') != '.github/workflows/pages.yml':
        raise PagesError('pages.yml 工作未啟用或路徑不符。')
    commit = api(repo, 'commits/' + quote(branch, safe=''))
    sha = commit.get('sha', '')
    if not re.fullmatch(r'[0-9a-f]{40}', sha):
        raise PagesError('未取得發布分支的完整 commit SHA。')
    request_id = 'macgyver-' + uuid.uuid4().hex[:16]
    print('發布 commit：' + sha + '；工作識別：' + request_id, flush=True)
    dispatched = api(repo, 'actions/workflows/' + WORKFLOW + '/dispatches', method='POST',
                     payload={'ref': branch, 'inputs': {'request_id': request_id}})
    run_id = dispatched.get('workflow_run_id')
    if run_id:
        run = api(repo, 'actions/runs/' + str(int(run_id)))
        validate_run(run, sha, branch, request_id)
    else:
        # Older API deployments return 204: correlate by unique request ID, not
        # the latest run or merely a shared commit SHA.
        run = find_requested_run(repo, sha, branch, request_id, time.monotonic() + 90)
        run_id = run['id']
    url = 'https://github.com/' + repo + '/actions/runs/' + str(run_id)
    print('此次發布工作：' + url, flush=True)
    if no_wait:
        print('發布已送出，尚未確認成功。', flush=True)
        return {'status': 'submitted', 'runId': run_id, 'url': url, 'commit': sha}
    deadline, last = time.monotonic() + wait_seconds, None
    while True:
        validate_run(run, sha, branch, request_id)
        state = (run.get('status'), run.get('conclusion'))
        if state != last:
            print('Pages 工作狀態：%s / %s' % state, flush=True)
            last = state
        if run.get('status') == 'completed':
            if run.get('conclusion') != 'success':
                raise PagesError('此次 Pages 發布未成功（%s）。請查看 %s；不會宣稱已更新網站。'
                                 % (run.get('conclusion'), url))
            print('已確認此次 GitHub Pages 工作完成且成功：' + url, flush=True)
            return {'status': 'success', 'runId': run_id, 'url': url, 'commit': sha}
        if time.monotonic() >= deadline:
            raise PagesError('本機等待時間已到，遠端工作可能仍在執行；請查看 ' + url)
        time.sleep(5)
        run = api(repo, 'actions/runs/' + str(run_id))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', default='kuonanhong/macgyver-academy')
    parser.add_argument('--ref', default='main')
    parser.add_argument('--configure-actions', action='store_true',
                        help='明確將現有 Pages Source 從 branch 改為 GitHub Actions；需維護者權限')
    parser.add_argument('--publish', action='store_true', help='送出一次 pages.yml 並等待該工作結果')
    parser.add_argument('--no-wait', action='store_true', help='只送出；不宣稱部署成功')
    parser.add_argument('--wait-seconds', type=int, default=1800)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', args.repo):
        parser.error('--repo 必須是 owner/repository。')
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._/-]{0,200}', args.ref):
        parser.error('--ref 格式無效。')
    if args.no_wait and not args.publish:
        parser.error('--no-wait 需要 --publish。')
    if not 30 <= args.wait_seconds <= 3600:
        parser.error('--wait-seconds 必須介於 30 與 3600。')
    if not shutil.which('gh'):
        parser.error('需要 GitHub CLI gh；請先安裝並執行 gh auth login。')
    try:
        settings = ensure_actions(args.repo, args.configure_actions)
        if args.publish:
            if settings.get('build_type') != 'workflow':
                raise PagesError('請加 --configure-actions 或到 Settings → Pages → Source 選 GitHub Actions 後再發布。')
            result = publish(args.repo, args.ref, args.wait_seconds, args.no_wait)
        else:
            latest = api(args.repo, 'actions/workflows/' + WORKFLOW + '/runs?per_page=5')
            result = {'buildType': settings.get('build_type'), 'siteURL': settings.get('html_url'),
                      'runs': [{k: run.get(k) for k in ('id', 'html_url', 'head_sha', 'status', 'conclusion')}
                               for run in latest.get('workflow_runs', [])]}
            print(json.dumps(result, ensure_ascii=False, indent=2))
        if args.report:
            args.report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        return 0
    except (OSError, ValueError, PagesError, subprocess.SubprocessError) as error:
        print('Pages：' + str(error), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
