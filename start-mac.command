#!/usr/bin/env bash
# Double-click in Finder, or run bash run-local.sh from an activated Conda shell.
set -euo pipefail
TASK_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
exec bash "$TASK_ROOT/run-local.sh" "$@"
