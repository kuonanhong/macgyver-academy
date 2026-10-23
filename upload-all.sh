#!/usr/bin/env bash
# V17 compatibility alias: incremental website upload; --with-assets includes existing private assets.
# No rebuild, market refresh, automatic model download, deletion or force push.
# Preview: bash upload-all.sh --dry-run
set -euo pipefail
TASK_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
exec bash "$TASK_ROOT/macgyver.sh" all "$@"
