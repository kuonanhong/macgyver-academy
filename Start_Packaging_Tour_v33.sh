#!/usr/bin/env bash
set -euo pipefail
TOUR_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
if command -v python3 >/dev/null 2>&1; then
  exec python3 "$TOUR_ROOT/tools/preview-packaging-tour-v33.py" "$@"
elif command -v py >/dev/null 2>&1; then
  exec py -3 "$TOUR_ROOT/tools/preview-packaging-tour-v33.py" "$@"
else
  echo '需要 Python 3。也可直接開 public/academy/packaging-tour-v33.html 觀看三維導覽。' >&2
  exit 1
fi
