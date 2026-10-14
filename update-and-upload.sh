#!/usr/bin/env bash
# Refresh offline assets, update the private index, back up explicit folders, then push.
set -euo pipefail
TASK_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
DOCUMENTS_DIR="$TASK_ROOT/local-documents"
DOCUMENTS_REMOTE=''
MODELS_REMOTE=''
DO_INDEX=0
REBUILD_CURRICULUM=0
PUSH_ARGS=()
REPO_URL=''
TARGET_BRANCH='main'
usage() {
  cat <<'USAGE'
使用：bash update-and-upload.sh --repo https://github.com/OWNER/REPO.git [選項]
  --index-documents               先重建本機 AI 教材索引
  --rebuild-curriculum            將 tools/ 中的課程原稿重新整合並驗證（Python + Node）
  --documents DIRECTORY          教材資料夾（預設 local-documents/）
  --documents-remote remote:path  以 rclone copy 備份教材；不刪除目的地
  --models-remote remote:path     明確同意以 rclone copy 備份 models/；未填就不上傳權重
  --branch NAME                  Git 目的分支
  --message TEXT                 Git 提交說明
  --out DIRECTORY                專案外的獨立 GitHub 匯出資料夾

先設定 GitHub 認證及 rclone remote。提供 documents-remote 代表將指定資料夾
上傳至該目的地，請先確認教材有再散布權限及目的地的存取權。
程式不把私有教材、帳號資料庫或 AI 索引加入公開 Git；教材備份與程式更新分開。
模型不自動進入 Git／Git LFS；只有指定 --models-remote 才備份，並排除未完成下載。
GitHub 上傳使用隔離的公開原始碼副本，不改動原 Sites 倉庫的 origin。
模型備份不會自動訓練模型；AI 啟動請用 run-ai-llamacpp.sh 或 run-ai-local.sh。
程式或公開教材變更時，先自動重建雙擊即用的離線套件；需要 Node.js 18+。
套件未變更時直接使用已附的版本，不需 Node.js 或 npm 套件。
USAGE
}
while [[ $# -gt 0 ]]; do
  case "$1" in
    --index-documents) DO_INDEX=1; shift;;
    --rebuild-curriculum) REBUILD_CURRICULUM=1; shift;;
    --documents|--documents-remote|--models-remote|--repo|--branch|--message|--out)
      [[ $# -ge 2 && -n "$2" ]] || { echo "缺少 $1 參數" >&2; exit 2; }
      case "$1" in
        --documents) DOCUMENTS_DIR="$2";;
        --documents-remote) DOCUMENTS_REMOTE="$2";;
        --models-remote) MODELS_REMOTE="$2";;
        --repo) REPO_URL="$2"; PUSH_ARGS+=("$1" "$2");;
        --branch) TARGET_BRANCH="$2"; PUSH_ARGS+=("$1" "$2");;
        *) PUSH_ARGS+=("$1" "$2");;
      esac
      shift 2;;
    -h|--help) usage; exit 0;;
    *) echo "未知選項：$1" >&2; usage; exit 2;;
  esac
done
HAS_REPO=0
for value in "${PUSH_ARGS[@]}"; do [[ "$value" != '--repo' ]] || HAS_REPO=1; done
[[ "$HAS_REPO" == 1 ]] || { echo '需要 --repo；請先明確指定程式目的倉庫。' >&2; exit 2; }
[[ "$REPO_URL" =~ ^https://github\.com/[A-Za-z0-9][A-Za-z0-9_.-]*/[A-Za-z0-9][A-Za-z0-9_.-]*(\.git)?$ || "$REPO_URL" =~ ^git@github\.com:[A-Za-z0-9][A-Za-z0-9_.-]*/[A-Za-z0-9][A-Za-z0-9_.-]*(\.git)?$ ]] || { echo '需要不含帳密的 GitHub HTTPS 或 SSH 倉庫網址。' >&2; exit 2; }
command -v git >/dev/null || { echo '請先安裝 Git。' >&2; exit 1; }
git check-ref-format --branch "$TARGET_BRANCH" >/dev/null || { echo 'Git 分支名稱無效；未執行傳輸。' >&2; exit 2; }
if [[ "$DO_INDEX" == 1 || -n "$DOCUMENTS_REMOTE" ]]; then
  [[ -d "$DOCUMENTS_DIR" ]] || { echo '找不到指定的教材資料夾。' >&2; exit 1; }
fi
TASK_PYTHON=()
for candidate in python3 python; do
  if command -v "$candidate" >/dev/null 2>&1 && "$candidate" -c 'import sys;sys.exit(sys.version_info<(3,10))' 2>/dev/null; then TASK_PYTHON=("$candidate"); break; fi
done
if [[ ${#TASK_PYTHON[@]} -eq 0 ]] && command -v py >/dev/null 2>&1 && py -3 -c 'import sys;sys.exit(sys.version_info<(3,10))' 2>/dev/null; then TASK_PYTHON=(py -3); fi
[[ ${#TASK_PYTHON[@]} -gt 0 ]] || { echo '需要 Python 3.10+ 進行匯出與路徑檢查。' >&2; exit 1; }
# Keep private materials outside every public-source snapshot.
"${TASK_PYTHON[@]}" - "$TASK_ROOT" "$DOCUMENTS_DIR" <<'PY'
from pathlib import Path
import subprocess, sys
root, source = (Path(v).resolve() for v in sys.argv[1:])
try:
    relative = source.relative_to(root)
except ValueError:
    relative = None
if relative is not None:
    if not relative.parts or relative.parts[0] != 'local-documents':
        sys.exit('教材不能放在會提交 Git 的專案子目錄。請移至專案外，或使用 local-documents/。未執行傳輸。')
probe = subprocess.run(['git','-C',str(root),'rev-parse','--show-toplevel'], capture_output=True, text=True)
if probe.returncode == 0:
    tracked = subprocess.run(['git','-C',str(root),'ls-files','-z','--','local-documents'], capture_output=True, check=True)
    if tracked.stdout:
        sys.exit('local-documents/ 已有 Git 追蹤檔案；請先移除追蹤並檢查歷史，避免私人教材隨程式上傳。未執行傳輸。')
PY
for remote in "$DOCUMENTS_REMOTE" "$MODELS_REMOTE"; do
  if [[ -n "$remote" ]]; then
    [[ "$remote" == *:* && "$remote" != -* ]] || { echo '備份 remote 須為 remote:path。' >&2; exit 2; }
    command -v rclone >/dev/null || { echo '請安裝 rclone 並執行 rclone config。' >&2; exit 1; }
  fi
done
if [[ -n "$MODELS_REMOTE" ]]; then
  [[ -d "$TASK_ROOT/models" && ! -L "$TASK_ROOT/models" ]] || { echo '需要實際的 models/ 資料夾；不能是符號連結。' >&2; exit 1; }
fi
# Build before any upload so new JS, public JSON, media metadata and related
# study links cannot leave a stale direct-file package in the remote checkout.
if [[ "$REBUILD_CURRICULUM" == 1 ]]; then
  bash "$TASK_ROOT/rebuild-curriculum.sh"
fi
bash "$TASK_ROOT/build-offline.sh" --if-needed
if [[ "$DO_INDEX" == 1 ]]; then
  bash "$TASK_ROOT/index-documents.sh" --source "$DOCUMENTS_DIR"
fi
# Validate the public snapshot and credentials scan before any external backup.
# This is read-only; the final --push below performs the actual Git operation.
bash "$TASK_ROOT/publish-github.sh" "${PUSH_ARGS[@]}" --dry-run
BACKUP_EXCLUDES=(--exclude '.env*' --exclude '.git/**' --exclude '*.pem' --exclude '*.key' --exclude '*.sqlite*' --exclude '.DS_Store' --exclude '*.part' --exclude '*.partial' --exclude '*.tmp' --exclude '*.download' --exclude '*.crdownload' --exclude '.incomplete/**')
if [[ -n "$DOCUMENTS_REMOTE" ]]; then
  rclone copy "$DOCUMENTS_DIR" "$DOCUMENTS_REMOTE" --progress --retries 8 --low-level-retries 20 --transfers 2 --checkers 4 "${BACKUP_EXCLUDES[@]}"
fi
if [[ -n "$MODELS_REMOTE" ]]; then
  rclone copy "$TASK_ROOT/models" "$MODELS_REMOTE" --progress --retries 8 --low-level-retries 20 --transfers 2 --checkers 4 "${BACKUP_EXCLUDES[@]}"
fi
exec bash "$TASK_ROOT/publish-github.sh" "${PUSH_ARGS[@]}" --push
