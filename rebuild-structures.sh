#!/usr/bin/env bash
# V13: rebuild only the 100 bridges & buildings courses after editing tools/structures-v13/inputs/*.json.
#   validate authored inputs → build 40-step courses → merge into public/academy/data → rebuild offline bundle → validate all data
# Safe to rerun: earlier V13 content is replaced, all other courses and the existing step IDs of
# danjiang / b003 / b015 / b021 stay unchanged.
set -euo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
PY="${MACGYVER_PYTHON:-python3}"
"$PY" -I "$ROOT/tools/structures-v13/validate_input.py" > /dev/null || { "$PY" -I "$ROOT/tools/structures-v13/validate_input.py" | grep -v ': OK'; exit 1; }
"$PY" -I "$ROOT/tools/structures-v13/build_structures.py"
"$PY" -I "$ROOT/tools/integrate-structures-v13.py"
if [[ -d "$ROOT/public/academy/i18n" ]]; then "$PY" -I "$ROOT/tools/i18n-v12/build_i18n.py"; fi
command -v node >/dev/null || { echo '需要 Node.js 18+ 才能重建離線套件（開啟網站本身不需要）。' >&2; exit 1; }
node "$ROOT/tools/build-offline.mjs"
"$PY" -I "$ROOT/tools/validate-data.py"
echo '橋樑與建築課程已重建並通過驗證。上傳：bash macgyver.sh（或 bash upload-all.sh）'
