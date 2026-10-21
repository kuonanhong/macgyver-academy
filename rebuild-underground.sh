#!/usr/bin/env bash
# Rebuild the V14 underground extension without changing V13 stage objects.
set -euo pipefail
TASK_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
TASK_PY="${MACGYVER_PYTHON:-python3}"
"$TASK_PY" -c 'import sys; sys.exit(0 if sys.version_info >= (3,10) else "Python 3.10+ required")'
command -v node >/dev/null || { echo 'Node.js 22.13+ required for rebuilding.' >&2; exit 1; }
node -e 'const [major,minor]=process.versions.node.split(".").map(Number);if(major<22||(major===22&&minor<13))process.exit(1)'
cd "$TASK_ROOT"
"$TASK_PY" -I tools/underground-v14/validate_input.py
"$TASK_PY" -I tools/underground-v14/build_underground.py
"$TASK_PY" -I tools/integrate-underground-v14.py
node tools/build-underground-visuals-v14.mjs
"$TASK_PY" public/academy/assets/labs/v14/run-underground-labs.py --check
"$TASK_PY" tools/build-underground-lab-package-v14.py
node tools/test-underground-calculators-v14.mjs
node tools/build-offline.mjs
"$TASK_PY" -I tools/validate-underground-v14.py
"$TASK_PY" -I tools/validate-data.py
printf '%s\n' 'V14 地下工程已重建。啟動：bash run-local.sh；上傳比對：bash upload-all.sh --dry-run --skip-models'
