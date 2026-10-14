#!/usr/bin/env bash
# Reads server-side environment/.env only; never accepts a key as a CLI argument.
set -euo pipefail
TASK_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
TASK_PYTHON=''
for candidate in python3 python; do
  if command -v "$candidate" >/dev/null 2>&1 && "$candidate" -c 'import sys;sys.exit(sys.version_info<(3,10))' 2>/dev/null; then TASK_PYTHON="$candidate"; break; fi
done
[[ -n "$TASK_PYTHON" ]] || { echo '需要 Python 3.10+；pip 不能升級 Python。' >&2; exit 1; }
"$TASK_PYTHON" - "$TASK_ROOT" <<'PY'
import os,sys
from pathlib import Path
sys.path.insert(0,sys.argv[1])
from portable.server import read_dotenv
read_dotenv(Path(sys.argv[1])/'.env')
if not os.environ.get('GEMINI_API_KEY'):
    sys.exit('請在私有 .env 設 GEMINI_API_KEY；參考 .env.example。不要放進 HTML、Git 或指令參數。')
print('Gemini 雲端路線已設定；每次傳送前，學員仍需同意將問句、課程引用、检索教材與圖片交給 Google。')
PY
exec bash "$TASK_ROOT/run-local.sh" "$@"
