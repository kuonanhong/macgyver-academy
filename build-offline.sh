#!/usr/bin/env bash
set -euo pipefail
TASK_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
if [[ "${1:-}" == '--if-needed' ]] && command -v python3 >/dev/null && python3 "$TASK_ROOT/tools/check-offline.py"; then
  exit 0
fi
command -v node >/dev/null || { echo '教材或程式已有更新：請安裝 Node.js 18+，再執行 bash build-offline.sh。開啟已附的離線網站不需要 Node.js。' >&2; exit 1; }
exec node "$TASK_ROOT/tools/build-offline.mjs" "$@"
