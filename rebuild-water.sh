#!/usr/bin/env bash
# Rebuild the V15 extension while preserving all V14 course stages.
set -euo pipefail
TASK_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
TASK_PY="${MACGYVER_PYTHON:-${CONDA_PREFIX:+${CONDA_PREFIX}/bin/python}}"
TASK_PY="${TASK_PY:-python3}"
"${TASK_PY}" -c 'import sys; sys.exit(0 if sys.version_info >= (3,10) else "Python 3.10+ required")'
command -v node >/dev/null || { echo 'Node.js 22.13+ required for rebuilding.' >&2; exit 1; }
node -e 'const [major,minor]=process.versions.node.split(".").map(Number);if(major<22||(major===22&&minor<13))process.exit(1)'
cd "${TASK_ROOT}"
"${TASK_PY}" -I tools/water-v15/validate_input.py
"${TASK_PY}" -I tools/water-v15/build_water.py
"${TASK_PY}" -I tools/integrate-water-v15.py
node tools/build-water-visuals-v15.mjs
"${TASK_PY}" tools/build-water-lab-package-v15.py
node tools/test-water-calculators-v15.mjs
node tools/build-offline.mjs
"${TASK_PY}" -I tools/validate-water-v15.py
"${TASK_PY}" -I tools/validate-data.py
printf '%s\n' 'V15 水利與海岸課程已重建。啟動：bash run-local.sh；比對：bash upload-all.sh --dry-run --skip-models'
