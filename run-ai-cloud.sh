#!/usr/bin/env bash
# Keys stay in the server environment or private .env, never in browser config.
set -euo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
for TASK_ARGUMENT in "$@"; do
  case "$TASK_ARGUMENT" in
    -h|--help)
      printf '%s\n' 'Usage: bash run-ai-cloud.sh [server arguments]' 'Set provider keys/models in the private .env or environment.' 'Python priority: MACGYVER_PYTHON, active Conda, python3, python.'
      exit 0 ;;
  esac
done
PY=''
for c in "${MACGYVER_PYTHON:-}" "${CONDA_PREFIX:+${CONDA_PREFIX}/bin/python}" python3 python; do
  [[ -n "$c" ]] || continue
  if command -v "$c" >/dev/null 2>&1 && "$c" -c 'import sys;sys.exit(sys.version_info<(3,10))' 2>/dev/null; then PY="$c";break;fi
done
[[ -n "$PY" ]] || { printf '%s\n' 'Python 3.10+ is required.' >&2;exit 1; }
export MACGYVER_PYTHON="$PY"
"$PY" - "$ROOT" <<'PY'
import sys
from pathlib import Path
sys.path.insert(0,sys.argv[1])
from portable.server import read_dotenv, ai_routes
read_dotenv(Path(sys.argv[1])/'.env')
if not ai_routes():raise SystemExit('Set a server-side provider key and model in .env; see docs/UPLOAD_AI_V14_ZH.md.')
print('Configured AI route(s): '+', '.join(r['id'] for r in ai_routes()))
PY
exec bash "$ROOT/run-local.sh" "$@"
