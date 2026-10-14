#!/usr/bin/env bash
# Listing is the default. --download is the user's explicit model download action.
set -euo pipefail
TASK_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
for candidate in python3 python; do
  if command -v "$candidate" >/dev/null 2>&1 && "$candidate" -c 'import sys;sys.exit(sys.version_info<(3,10))' 2>/dev/null; then
    exec "$candidate" "$TASK_ROOT/tools/download_ai_model.py" "$@"
  fi
done
if command -v py >/dev/null 2>&1; then exec py -3 "$TASK_ROOT/tools/download_ai_model.py" "$@"; fi
echo '需要 Python 3.10+。Conda：conda create -n macgyver python=3.12；conda activate macgyver。pip 無法升級 Python。' >&2
exit 1
