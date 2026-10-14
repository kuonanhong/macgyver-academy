#!/usr/bin/env bash
# Safe, repeatable GitHub upload. No credential is embedded or accepted in a URL.
set -euo pipefail
TASK_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_URL=''
TARGET_BRANCH=''
COMMIT_MESSAGE='Update MacGyver engineering academy'
MODEL_REMOTE=''
UPLOAD_REMOTE='macgyver-upload'
usage() {
  cat <<'USAGE'
使用：bash push-updates.sh --repo https://github.com/OWNER/REPO.git [選項]
  --branch NAME          目標分支；預設目前分支或 main
  --message TEXT         本次提交訊息
  --models-remote PATH   選填 rclone remote:path；將 models/ 複製至遠端，不刪除遠端檔案
  --path DIRECTORY      專案資料夾，預設本腳本所在位置

先用 gh auth login + gh auth setup-git，或 Git Credential Manager / SSH 金鑰登入。
腳本不建立 GitHub 倉庫、不覆寫 origin、不強推、不把 token 寫入檔案。
模型可用 Git LFS（須已安裝且遠端額度足夠），或 --models-remote + rclone。
USAGE
}
while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo|--branch|--message|--models-remote|--path)
      [[ $# -ge 2 && -n "$2" ]] || { echo "缺少 $1 參數" >&2; exit 2; }
      case "$1" in
        --repo) REPO_URL="$2";; --branch) TARGET_BRANCH="$2";;
        --message) COMMIT_MESSAGE="$2";; --models-remote) MODEL_REMOTE="$2";;
        --path) TASK_ROOT="$2";;
      esac
      shift 2;;
    -h|--help) usage; exit 0;;
    *) echo "未知選項：$1" >&2; usage; exit 2;;
  esac
done
[[ "$REPO_URL" =~ ^https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+(\.git)?$ || "$REPO_URL" =~ ^git@github\.com:[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+(\.git)?$ ]] || { echo '請指定不含帳密的 GitHub HTTPS 或 SSH 倉庫網址：--repo URL' >&2; exit 2; }
command -v git >/dev/null || { echo '需要 Git。' >&2; exit 1; }
command -v python3 >/dev/null || { echo '需要 Python 3（用於檔案與敏感資訊檢查）。' >&2; exit 1; }
TASK_ROOT="$(cd -- "$TASK_ROOT" && pwd -P)"
cd -- "$TASK_ROOT"
bash "$TASK_ROOT/build-offline.sh" --if-needed
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  git init -b "${TARGET_BRANCH:-main}"
fi
[[ "$(git rev-parse --show-toplevel)" == "$(pwd -P)" ]] || { echo '請在 Git 倉庫根目錄執行。' >&2; exit 1; }
TARGET_BRANCH="${TARGET_BRANCH:-$(git symbolic-ref --short -q HEAD || echo main)}"
git check-ref-format --branch "$TARGET_BRANCH" >/dev/null
if git remote get-url "$UPLOAD_REMOTE" >/dev/null 2>&1; then
  [[ "$(git remote get-url "$UPLOAD_REMOTE")" == "$REPO_URL" ]] || { echo 'macgyver-upload 遠端已指向另一倉庫；請先檢查後以 git remote set-url 自行修正。' >&2; exit 1; }
else
  git remote add "$UPLOAD_REMOTE" "$REPO_URL"
fi
git config user.name >/dev/null || { echo '先設定 git config user.name "你的姓名"。' >&2; exit 1; }
git config user.email >/dev/null || { echo '先設定 git config user.email "你的提交 email"。' >&2; exit 1; }

# Check before staging: filenames are printed, never matched secret contents.
python3 - "$MODEL_REMOTE" <<'PY'
import pathlib, re, subprocess, sys
files = subprocess.check_output(['git','ls-files','-co','--exclude-standard','-z']).split(b'\0')
blocked=[]; model_files=[]
for raw in set(files):
    if not raw: continue
    path=pathlib.Path(raw.decode('utf-8','surrogateescape'))
    if not path.is_file(): continue
    if ((path.name.startswith('.env') and path.name!='.env.example') or path.suffix in ('.pem','.key','.sqlite','.sqlite3') or '.sqlite3-' in path.name or path.name in ('id_rsa','id_ed25519') or 'portable/data' in str(path)):
        blocked.append(str(path)); continue
    is_remote_model = sys.argv[1] and path.parts and path.parts[0]=='models'
    if not is_remote_model and (path.suffix.lower() in ('.gguf','.safetensors','.ckpt','.pt','.pth','.onnx','.bin') or path.stat().st_size>=50*1024*1024):
        model_files.append(str(path))
    if path.stat().st_size<2*1024*1024:
        data=path.read_bytes()
        if re.search(rb'(?:github_pat_[A-Za-z0-9_]{30,}|gh[pousr]_[A-Za-z0-9]{30,}|sk-(?:proj-)?[A-Za-z0-9_-]{40,}|-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----)',data):
            blocked.append(str(path))
if blocked:
    sys.exit('停止：可能包含憑證或私人帳號資料（未顯示內容）：\n'+'\n'.join(sorted(set(blocked))))
if model_files:
    if subprocess.run(['git','lfs','version'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode:
        sys.exit('發現模型或 >=50 MiB 檔案。先安裝 git-lfs，或使用 --models-remote 將 models/ 上傳物件儲存。')
    subprocess.run(['git','lfs','install','--local'],check=True)
    for filename in model_files:
        subprocess.run(['git','lfs','track','--filename',filename],check=True)
PY

if [[ -n "$MODEL_REMOTE" ]]; then
  command -v rclone >/dev/null || { echo '需要 rclone；先執行 rclone config 設定遠端。' >&2; exit 1; }
  [[ "$MODEL_REMOTE" == *:* && "$MODEL_REMOTE" != -* ]] || { echo 'models remote 格式須為 remote:path。' >&2; exit 2; }
  [[ -d models ]] || { echo '找不到 models/ 資料夾。' >&2; exit 1; }
  if ! git diff --cached --quiet -- models; then
    echo 'models/ 已有 staged 變更。請先用 git restore --staged -- models 取消 staging，再重跑，以免模型同時進入 Git 提交。' >&2
    exit 1
  fi
  # copy is deliberately non-destructive; partial failure can be retried.
  rclone copy models/ "$MODEL_REMOTE" --progress --retries 8 --low-level-retries 20 --transfers 2 --checkers 4 --exclude '.env*' --exclude '.git/**' --exclude '*.pem' --exclude '*.key' --exclude '*.sqlite*' --exclude '.DS_Store'
  git add -A -- . ':!models'
else
  git add -A
fi
if ! git diff --cached --quiet; then
  git commit -m "$COMMIT_MESSAGE"
fi
git rev-parse --verify HEAD >/dev/null || { echo '沒有可上傳的提交。' >&2; exit 1; }

# Fetch does not modify the working tree. Divergent history is never overwritten.
if git ls-remote --exit-code --heads "$UPLOAD_REMOTE" "$TARGET_BRANCH" >/dev/null 2>&1; then
  git fetch --no-tags "$UPLOAD_REMOTE" "$TARGET_BRANCH"
  if ! git merge-base --is-ancestor FETCH_HEAD HEAD; then
    echo '遠端有尚未合併的提交；本地提交已保留。請檢查後合併 FETCH_HEAD，再重跑腳本。沒有進行強推。' >&2
    exit 1
  fi
fi
for attempt in 1 2 3 4 5; do
  if git -c http.version=HTTP/1.1 -c http.lowSpeedLimit=1000 -c http.lowSpeedTime=120 push "$UPLOAD_REMOTE" "HEAD:refs/heads/$TARGET_BRANCH"; then
    echo "完成：$REPO_URL（$TARGET_BRANCH）"
    exit 0
  fi
  [[ "$attempt" -lt 5 ]] || break
  echo "傳輸未完成，$((attempt * 3)) 秒後重試（$attempt / 5）。" >&2
  sleep "$((attempt * 3))"
done
echo '上傳失敗；本地提交完整保留。請檢查網路、認證與遠端分支，再重跑腳本。' >&2
exit 1
