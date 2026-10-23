#!/usr/bin/env bash
set -euo pipefail
TASK_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_EXE="${MACGYVER_PYTHON:-}"
if [[ -z "$PYTHON_EXE" && -n "${CONDA_PREFIX:-}" && -x "$CONDA_PREFIX/bin/python" ]]; then
  PYTHON_EXE="$CONDA_PREFIX/bin/python"
fi
if [[ -z "$PYTHON_EXE" ]]; then
  for candidate in python3 python; do
    if command -v "$candidate" >/dev/null 2>&1 && "$candidate" -c 'import sys; sys.exit(sys.version_info < (3,10))' 2>/dev/null; then
      PYTHON_EXE="$candidate"
      break
    fi
  done
fi
if [[ -z "$PYTHON_EXE" ]]; then
  echo '需要 Python 3.10+；pip 無法升級 Python 本身。若使用 Conda：' >&2
  echo '  conda create -n macgyver python=3.12 -y' >&2
  echo '  conda activate macgyver' >&2
  echo '再執行 bash run-local.sh。Windows 可執行 run-local.bat。' >&2
  exit 1
fi
"$PYTHON_EXE" -c 'import sys; sys.exit(0 if sys.version_info >= (3,10) else "需要 Python 3.10+")'
exec "$PYTHON_EXE" "$TASK_ROOT/portable/launch_v16.py" "$@"
