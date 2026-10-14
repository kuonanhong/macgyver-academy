#!/usr/bin/env bash
# Export a reviewed, isolated source snapshot; never repoint the Sites checkout.
set -euo pipefail
TASK_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
TASK_PYTHON=()
for candidate in python3 python; do
  if command -v "$candidate" >/dev/null 2>&1 && "$candidate" -c 'import sys; raise SystemExit(sys.version_info < (3, 10))' 2>/dev/null; then
    TASK_PYTHON=("$candidate"); break
  fi
done
if [[ ${#TASK_PYTHON[@]} -eq 0 ]] && command -v py >/dev/null 2>&1 && py -3 -c 'import sys; raise SystemExit(sys.version_info < (3, 10))' 2>/dev/null; then
  TASK_PYTHON=(py -3)
fi
[[ ${#TASK_PYTHON[@]} -gt 0 ]] || { echo '上傳工具需要 Python 3.10+；雙擊 index.html 閱讀課程不需要 Python。' >&2; exit 1; }
exec "${TASK_PYTHON[@]}" "$TASK_ROOT/tools/export_github.py" --source "$TASK_ROOT" "$@"
