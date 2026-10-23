#!/usr/bin/env bash
# V16: website changes + existing local documents/models, over SSH.
# Run from anywhere: bash /path/to/MacGyver_Engineering_Academy_v16/Upload_MacGyver_v16_SSH.sh
set -euo pipefail
TASK_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
TASK_PYTHON=''
for TASK_CANDIDATE in "${MACGYVER_PYTHON:-}" "${CONDA_PREFIX:+${CONDA_PREFIX}/bin/python}" python3 python; do
  [[ -n "$TASK_CANDIDATE" ]] || continue
  if command -v "$TASK_CANDIDATE" >/dev/null 2>&1 && "$TASK_CANDIDATE" -c 'import sys;sys.exit(sys.version_info<(3,10))' 2>/dev/null; then
    TASK_PYTHON="$TASK_CANDIDATE"
    break
  fi
done
if [[ -z "$TASK_PYTHON" ]]; then
  printf '%s\n' '需要 Python 3.10+。Conda 使用者可先 conda activate svm_kernels；也可用 MACGYVER_PYTHON 指定 Python 路徑。' >&2
  exit 1
fi
exec "$TASK_PYTHON" "$TASK_ROOT/tools/upload-v16/upload.py" "$@"
