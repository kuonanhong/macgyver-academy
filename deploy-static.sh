#!/usr/bin/env bash
# Assemble only public static assets. Does not upload code, credentials, or accounts.
set -euo pipefail
TASK_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT_DIR="$TASK_ROOT/github-pages"
while [[ $# -gt 0 ]]; do
  case "$1" in
    --out)
      [[ $# -ge 2 && -n "$2" ]] || { echo '缺少 --out 資料夾。' >&2; exit 2; }
      OUTPUT_DIR="$2"; shift 2;;
    -h|--help)
      echo '使用：bash deploy-static.sh [--out 輸出資料夾]'
      echo '預設輸出 github-pages/；產生 GitHub Pages 免費第一節試讀網站；完整會員課文由後端按權限提供。'
      echo '重複匯出只允許覆寫本腳本標記的生成目錄，不覆寫其他既有資料夾。'
      exit 0;;
    *) echo "未知選項：$1" >&2; exit 2;;
  esac
done
command -v python3 >/dev/null || { echo '需要 Python 3.10 或更新版本。' >&2; exit 1; }
if [[ ! -f "$TASK_ROOT/public/academy/preview-manifest.json" ]]; then
  bash "$TASK_ROOT/build-offline.sh" --if-needed
fi
exec python3 "$TASK_ROOT/tools/export-preview-v18.py" --out "$OUTPUT_DIR"
