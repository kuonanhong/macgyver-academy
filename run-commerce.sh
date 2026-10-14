#!/usr/bin/env bash
# Starts the protected backend only. It does not activate or configure payments.
set -euo pipefail
TASK_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_EXE="${PYTHON_EXE:-python3}"
if ! command -v "$PYTHON_EXE" >/dev/null 2>&1; then
  printf '%s\n' 'Python 3.10+ is required. Install Python from python.org or your operating-system package manager.' >&2
  exit 1
fi
"$PYTHON_EXE" -c 'import sys; sys.exit(0 if sys.version_info >= (3,10) else "Python 3.10+ is required; pip does not upgrade Python.")'
export COMMERCE_MODE=protected
printf '%s\n' 'Starting protected courses. Checkout stays disabled until merchant secrets and HTTPS are configured.'
exec "$PYTHON_EXE" "$TASK_ROOT/portable/server.py" "$@"
