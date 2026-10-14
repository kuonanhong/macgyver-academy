#!/usr/bin/env bash
set -euo pipefail
TASK_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_EXE="${MACGYVER_PYTHON:-python3}"
if [[ -n "${CONDA_PREFIX:-}" && -x "$CONDA_PREFIX/bin/python" && -z "${MACGYVER_PYTHON:-}" ]]; then PYTHON_EXE="$CONDA_PREFIX/bin/python"; fi
exec "$PYTHON_EXE" "$TASK_ROOT/tools/index-documents.py" "$@"
