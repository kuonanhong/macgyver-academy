#!/usr/bin/env bash
# V16 owner setup: password input stays hidden and is never sent to GitHub.
# bash setup-owner-v16.sh
# bash setup-owner-v16.sh --bootstrap /path/to/owner-private/owner-bootstrap-v16.json
# Reset an existing owner's password: add --reset-existing.
set -euo pipefail
TASK_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
TASK_PYTHON=''
for TASK_CANDIDATE in "${MACGYVER_PYTHON:-}" "${CONDA_PREFIX:+${CONDA_PREFIX}/bin/python}" python3 python; do
  [[ -n "${TASK_CANDIDATE}" ]] || continue
  if command -v "${TASK_CANDIDATE}" >/dev/null 2>&1 && "${TASK_CANDIDATE}" -c 'import sys;sys.exit(sys.version_info < (3,10))' 2>/dev/null; then
    TASK_PYTHON="$(command -v "${TASK_CANDIDATE}")"
    break
  fi
done
if [[ -z "${TASK_PYTHON}" ]]; then
  printf '%s\n' '需要 Python 3.10+。可先啟用您的 Conda 環境，再執行此腳本。' >&2
  exit 1
fi
cd -- "${TASK_ROOT}"
exec "${TASK_PYTHON}" -m portable.owner_admin "$@"
