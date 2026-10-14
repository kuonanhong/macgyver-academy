#!/usr/bin/env bash
# Rebuild all curriculum generations and their static/offline delivery assets.
set -euo pipefail
TASK_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_EXE="${MACGYVER_PYTHON:-python3}"
"$PYTHON_EXE" "$TASK_ROOT/tools/prepare-curriculum-rebuild.py"
for name in semiconductor_a semiconductor_b packaging_a packaging_b; do
  "$PYTHON_EXE" "$TASK_ROOT/tools/curriculum/build_${name}.py"
done
"$PYTHON_EXE" "$TASK_ROOT/tools/curriculum/integrate.py"
"$PYTHON_EXE" "$TASK_ROOT/tools/refresh-media.py"
"$PYTHON_EXE" "$TASK_ROOT/tools/refresh-related.py"
"$PYTHON_EXE" "$TASK_ROOT/tools/refresh-places.py"
"$PYTHON_EXE" "$TASK_ROOT/tools/integrate-expansion.py"
"$PYTHON_EXE" "$TASK_ROOT/tools/integrate-expansion-v7.py"
"$PYTHON_EXE" "$TASK_ROOT/tools/expand-relations-v7.py"
"$PYTHON_EXE" "$TASK_ROOT/tools/integrate-semiconductor-v8.py"
"$PYTHON_EXE" "$TASK_ROOT/tools/integrate-packaging-v9.py"
for group in a b c; do
  "$PYTHON_EXE" "$TASK_ROOT/tools/electronics-v10/build_group_${group}.py"
done
"$PYTHON_EXE" "$TASK_ROOT/tools/electronics-v10/build_media.py"
node "$TASK_ROOT/tools/build-electronics-visuals-v10.mjs" --check
"$PYTHON_EXE" "$TASK_ROOT/tools/integrate-electronics-v10.py"
for group in a b c; do
  "$PYTHON_EXE" "$TASK_ROOT/tools/computing-v11/build_group_${group}.py"
done
"$PYTHON_EXE" "$TASK_ROOT/tools/computing-v11/build_expansion.py"
node "$TASK_ROOT/tools/build-computing-visuals-v11.mjs" --check
node "$TASK_ROOT/tools/build-world-visuals-v11.mjs"
"$PYTHON_EXE" "$TASK_ROOT/tools/build-evidence-labs-v11.py"
"$PYTHON_EXE" "$TASK_ROOT/tools/integrate-computing-v11.py"
"$PYTHON_EXE" "$TASK_ROOT/tools/validate-data.py"
node "$TASK_ROOT/tools/build-public-player.mjs"
bash "$TASK_ROOT/build-offline.sh"
