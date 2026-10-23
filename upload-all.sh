#!/usr/bin/env bash
# V16 compatibility alias: incremental upload of the website and existing assets.
# No rebuild, market refresh, automatic model download, deletion or force push.
# Preview: bash upload-all.sh --dry-run
set -euo pipefail
TASK_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
exec bash "$TASK_ROOT/macgyver.sh" all "$@"
