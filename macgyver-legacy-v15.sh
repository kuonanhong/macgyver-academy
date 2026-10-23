#!/usr/bin/env bash
# 馬蓋先 MacGyver Engineering Academy V15 — one-click maintenance.
#
#   bash macgyver.sh              same as "deploy"
#   bash macgyver.sh all          deploy the website AND upload new model weights (one click for both repos)
#   bash macgyver.sh deploy       update stocks+FX → rebuild → validate → upload ONLY changed files, delete stale ones
#   bash macgyver.sh compare      show what is new / modified / deleted vs GitHub (no upload)
#   bash macgyver.sh models       get the AI weights (download, or import from the HuaTuo ZIPs) and upload only new chunks to PRIVATE-MODELS
#   bash macgyver.sh models-compare   show which weight chunks are already in PRIVATE-MODELS (no upload)
#   bash macgyver.sh restore-models DIR   rebuild and verify the weights from PRIVATE-MODELS into DIR
#   bash macgyver.sh stocks       weekly stock & FX refresh, upload just those two data files
#   bash macgyver.sh schedule     run "stocks" every Monday 09:07 on this computer (launchd / cron)
#   bash macgyver.sh unschedule   remove that schedule
#   bash macgyver.sh doctor       check git, python, node, SSH access and settings
#   bash macgyver.sh config       show / edit the saved settings
#
# Settings are saved in ~/.macgyver-academy.conf (never uploaded):
#   SITE_REPO=git@github.com:kuonanhong/macgyver-academy.git
#   MODELS_REPO=git@github.com:kuonanhong/PRIVATE-MODELS.git
#   BRANCH=main
#   MODELS="qwen25-05b qwen3-06b"  # ids from tools/model-manifest.json (browser models are enough for the website)
#   HUATUO_DIR=""                  # optional folder holding HuaTuo_v2_Qwen3_CPU_part1..4of4.zip or the HuaTuo package
#   PROTECT_CONTENT=0              # 1 = publish static site only, paid stages stubbed (needs Supabase)
set -euo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
CONF="${MACGYVER_CONF:-$HOME/.macgyver-academy.conf}"
SITE_REPO='git@github.com:kuonanhong/macgyver-academy.git'
MODELS_REPO='git@github.com:kuonanhong/PRIVATE-MODELS.git'
BRANCH='main'
MODELS='qwen25-05b qwen3-06b'
HUATUO_DIR=''
MODEL_DIR="$ROOT/models"
MODEL_BATCH_MIB=120
SKIP_DATA=0
PROTECT_CONTENT=0
STATE="$(dirname "$ROOT")/MacGyver_GitHub_Sync_State"
# shellcheck disable=SC1090
[[ -f "$CONF" ]] && source "$CONF"

say(){ printf '\033[1;32m▶ %s\033[0m\n' "$*"; }
warn(){ printf '\033[1;33m! %s\033[0m\n' "$*" >&2; }
die(){ printf '\033[1;31m✖ %s\033[0m\n' "$*" >&2; exit 1; }
PY=''
# Honour the chosen environment before PATH (including Conda paths with spaces).
for c in "${MACGYVER_PYTHON:-}" "${CONDA_PREFIX:+$CONDA_PREFIX/bin/python}" python3 python; do
  [[ -n "$c" ]] || continue
  if command -v "$c" >/dev/null 2>&1 && "$c" -c 'import sys;sys.exit(sys.version_info<(3,10))' 2>/dev/null; then
    PY="$(command -v "$c")"
    break
  fi
done

save_conf(){
  umask 077
  { for key in SITE_REPO MODELS_REPO BRANCH MODELS HUATUO_DIR MODEL_DIR MODEL_BATCH_MIB PROTECT_CONTENT STATE; do
      printf '%s=%q\n' "$key" "${!key}"
    done; } > "$CONF"
  say "設定已存到 $CONF"
}

doctor(){
  local ok=1
  command -v git >/dev/null || { warn '缺少 git（macOS：xcode-select --install）'; ok=0; }
  if [[ -n "$PY" ]]; then
    say "$("$PY" --version 2>&1)（${PY}）"
  else
    warn '缺少 Python 3.10+（macOS：brew install python 或 conda create -n macgyver python=3.12；之後 conda activate macgyver）'
    ok=0
  fi
  if command -v node >/dev/null; then say "Node $(node --version)（重建網站用）"; else warn '未安裝 Node.js 22.13+：改程式後無法重建 app.bundle.js（只更新資料仍可）'; fi
  for k in user.name user.email; do [[ -n "$(git config --global --get $k || true)" ]] || { warn "請先執行 git config --global $k \"…\""; ok=0; }; done
  if [[ "$SITE_REPO" == git@* ]]; then
    local out; out="$(ssh -o BatchMode=yes -o ConnectTimeout=10 -T git@github.com 2>&1 || true)"
    if grep -q 'successfully authenticated' <<<"$out"; then say "GitHub SSH 認證成功：${out%%!*}"; else warn "GitHub SSH 尚未設定：$out"; warn '請依 docs/UPLOAD_SYNC_V12_ZH.md 第 1 節建立 SSH key 並加到 GitHub。'; ok=0; fi
  fi
  git ls-remote --heads "$SITE_REPO" "$BRANCH" >/dev/null 2>&1 && say "可讀取網站倉庫 $SITE_REPO" || { warn "無法讀取 $SITE_REPO"; ok=0; }
  git ls-remote --heads "$MODELS_REPO" "$BRANCH" >/dev/null 2>&1 && say "可讀取模型私人倉庫 $MODELS_REPO" || warn "無法讀取 ${MODELS_REPO}（若尚未建立：GitHub → New repository → Private）"
  if [[ -n "$PY" ]]; then
    "$PY" - "$ROOT" "$MODEL_DIR" <<'PY' || { warn '模型清單檢查失敗。'; ok=0; }
import json,hashlib,sys,pathlib
root=pathlib.Path(sys.argv[1]);model_dir=pathlib.Path(sys.argv[2]);m=json.load(open(root/'tools/model-manifest.json'))['models']
for x in m:
    f=model_dir/x.get('file','-')
    print(('  ✓ ' if f.is_file() and f.stat().st_size==x.get('bytes') else '  · ')+x['id'],'—',x['label'],'（本機檔案存在）' if f.is_file() else '')
PY
  fi
  ((ok)) && say '環境檢查通過。' || warn '請先處理上述項目。'
  return $((1-ok))
}

update_data(){
  say '更新每週股價與匯率（需要網路；失敗時保留上週資料）'
  "$PY" "$ROOT/tools/markets-v12/update_markets.py" || warn '部分行情或匯率更新失敗，詳見 public/academy/data/markets.json 的 failures。'
}

rebuild(){
  if [[ -d "$ROOT/public/academy/i18n" ]] && ls "$ROOT/public/academy/i18n/"*.json >/dev/null 2>&1; then
    "$PY" "$ROOT/tools/i18n-v12/build_i18n.py"
  fi
  if command -v node >/dev/null; then
    say '重建離線套件與網站程式'
    node "$ROOT/tools/build-offline.mjs" --if-needed
  else
    "$PY" "$ROOT/tools/check-offline.py" || die '程式已修改但沒有 Node.js 可重建；請安裝 Node.js 22.13+。'
  fi
  say '驗證課程資料'
  "$PY" "$ROOT/tools/validate-data.py" >/dev/null || die '課程資料驗證失敗，未上傳。'
}

sync(){
  local extra=()
  ((PROTECT_CONTENT)) && extra+=(--site-only --protect-content)
  # ${extra[@]+...} keeps macOS's bash 3.2 happy with an empty array under "set -u".
  "$PY" "$ROOT/tools/sync-v12/sync_github.py" --repo "$SITE_REPO" --branch "$BRANCH" --state "$STATE" ${extra[@]+"${extra[@]}"} "$@"
}

schedule(){
  local script="$ROOT/macgyver.sh"
  if [[ "$(uname)" == Darwin ]]; then
    local plist="$HOME/Library/LaunchAgents/tw.macgyver.weekly-stocks.plist"
    mkdir -p "$HOME/Library/LaunchAgents" "$HOME/Library/Logs"
    cat > "$plist" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
  <key>Label</key><string>tw.macgyver.weekly-stocks</string>
  <key>ProgramArguments</key><array><string>/bin/bash</string><string>$script</string><string>stocks</string></array>
  <key>StartCalendarInterval</key><dict><key>Weekday</key><integer>1</integer><key>Hour</key><integer>9</integer><key>Minute</key><integer>7</integer></dict>
  <key>StandardOutPath</key><string>$HOME/Library/Logs/macgyver-weekly-stocks.log</string>
  <key>StandardErrorPath</key><string>$HOME/Library/Logs/macgyver-weekly-stocks.log</string>
  <key>EnvironmentVariables</key><dict><key>PATH</key><string>/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin</string></dict>
</dict></plist>
EOF
    launchctl bootout "gui/$(id -u)/tw.macgyver.weekly-stocks" 2>/dev/null || true
    launchctl bootstrap "gui/$(id -u)" "$plist"
    say "已排程：每週一 09:07 執行 stocks（記錄：~/Library/Logs/macgyver-weekly-stocks.log）。Mac 需開機且未睡眠。"
  else
    local line="7 9 * * 1 /bin/bash '$script' stocks >> \$HOME/.macgyver-weekly-stocks.log 2>&1 # macgyver-weekly"
    ( crontab -l 2>/dev/null | grep -v 'macgyver-weekly' ; echo "$line" ) | crontab -
    say '已加入 crontab：每週一 09:07 執行 stocks。'
  fi
  say '建議同時啟用 GitHub Actions「Weekly market & FX snapshot」：電腦關機時也會在雲端每週更新。'
}

unschedule(){
  if [[ "$(uname)" == Darwin ]]; then
    launchctl bootout "gui/$(id -u)/tw.macgyver.weekly-stocks" 2>/dev/null || true
    rm -f "$HOME/Library/LaunchAgents/tw.macgyver.weekly-stocks.plist"
  else
    crontab -l 2>/dev/null | grep -v 'macgyver-weekly' | crontab - || true
  fi
  say '已移除本機每週排程。'
}

models_prepare(){
  local dir="$MODEL_DIR" id kind file
  mkdir -p "$dir"
  for id in $MODELS; do
    kind="$("$PY" -c "import json,sys;m={x['id']:x for x in json.load(open(sys.argv[1]))['models']};x=m.get(sys.argv[2]);print((x or {}).get('kind','?'),(x or {}).get('file',''))" "$ROOT/tools/model-manifest.json" "$id")"
    file="${kind#* }"; kind="${kind%% *}"
    if [[ "$kind" == '?' ]]; then warn "未知模型 ${id}，略過"; continue; fi
    if [[ -z "$file" ]]; then warn "$id 是 Ollama 模型（由 ollama pull 管理），不需上傳私人倉庫"; continue; fi
    if [[ "$id" == qwen3-06b && ! -f "$dir/$file" ]]; then
      say "嘗試從華佗學院已有的 Qwen3-0.6B（四份 ZIP 或已還原的 GGUF）匯入，免重新下載"
      local search=(--search "$(dirname "$ROOT")" --search "$HOME/Downloads")
      [[ -n "$HUATUO_DIR" ]] && search+=(--search "$HUATUO_DIR")
      "$PY" "$ROOT/tools/sync-v13/models_sync.py" import-huatuo "${search[@]}" --to "$dir" || true
    fi
    say "確認模型 ${id}（官方固定版本與 SHA-256；已存在且正確就不重抓，中斷可重跑接續）"
    bash "$ROOT/install-ai-models.sh" --model "$id" --download --directory "$dir"
  done
}
models(){
  models_prepare
  say "比對並上傳權重到私人倉庫 ${MODELS_REPO}（40 MiB 分片，只傳雲端還沒有的部分；不會改動華佗學院的檔案）"
  warn '請確認該倉庫在 GitHub 上是 Private。'
  "$PY" "$ROOT/tools/sync-v13/models_sync.py" push --repo "$MODELS_REPO" --branch "$BRANCH" --models-dir "$MODEL_DIR" --state "$STATE" --private-confirmed --batch-mib "$MODEL_BATCH_MIB" "$@"
}

cmd="${1:-deploy}"; shift || true
case "$cmd" in
  doctor) doctor ;;
  config)
    echo "設定檔：$CONF"; echo "SITE_REPO=$SITE_REPO"; echo "MODELS_REPO=$MODELS_REPO"; echo "BRANCH=$BRANCH"; echo "MODELS=$MODELS"; echo "HUATUO_DIR=$HUATUO_DIR"; echo "PROTECT_CONTENT=$PROTECT_CONTENT"; echo "STATE=$STATE"
    if [[ -t 0 ]]; then
      read -r -p '網站倉庫 SSH 網址 [Enter 保留]：' v; [[ -n "$v" ]] && SITE_REPO="$v"
      read -r -p '模型私人倉庫 SSH 網址 [Enter 保留]：' v; [[ -n "$v" ]] && MODELS_REPO="$v"
      read -r -p '分支 [Enter 保留]：' v; [[ -n "$v" ]] && BRANCH="$v"
      save_conf
    fi ;;
  compare) [[ -n "$PY" ]] || die '需要 Python 3.10+'; sync "$@" ;;
  models-compare) [[ -n "$PY" ]] || die '需要 Python 3.10+'; "$PY" "$ROOT/tools/sync-v13/models_sync.py" compare --repo "$MODELS_REPO" --branch "$BRANCH" --models-dir "$MODEL_DIR" --state "$STATE" ;;
  restore-models) [[ -n "$PY" ]] || die '需要 Python 3.10+'; "$PY" "$ROOT/tools/sync-v13/models_sync.py" restore --repo "$MODELS_REPO" --branch "$BRANCH" --state "$STATE" --to "${1:-$ROOT/models}" ;;
  deploy)
    [[ -n "$PY" ]] || die '需要 Python 3.10+'
    [[ -f "$CONF" ]] || save_conf
    ((SKIP_DATA)) || update_data; rebuild
    say '比較本機套件與 GitHub，只上傳新增與修改的檔案，清理已管理的舊分片；保留遠端另加檔案'
    sync --push --message "${MESSAGE:-MacGyver Academy V15 update $(date +%F)}" "$@"
    say '上傳完成；請在 GitHub Actions 確認建置與 Pages 狀態：https://kuonanhong.github.io/macgyver-academy/' ;;
  all)
    [[ -n "$PY" ]] || die '需要 Python 3.10+'
    dry_run=0; skip_models=0; sync_extra=()
    while (($#)); do
      case "$1" in
        --dry-run) dry_run=1 ;;
        --skip-models) skip_models=1 ;;
        --skip-data) SKIP_DATA=1 ;;
        --models-dir) [[ $# -ge 2 ]] || die '--models-dir 需要目錄'; MODEL_DIR="$2"; shift ;;
        --batch-mib) [[ $# -ge 2 ]] || die '--batch-mib 需要 40..1024'; MODEL_BATCH_MIB="$2"; shift ;;
        --no-delete|--prune) sync_extra+=("$1") ;;
        --help|-h) printf '%s\n' 'bash upload-all.sh [--dry-run] [--skip-models] [--skip-data] [--models-dir DIR] [--batch-mib 40..1024] [--no-delete|--prune]'; exit 0 ;;
        *) die "未知上傳選項：$1" ;;
      esac
      shift
    done
    if ((dry_run)); then
      sync ${sync_extra[@]+"${sync_extra[@]}"}
      if ((!skip_models)); then "$PY" "$ROOT/tools/sync-v13/models_sync.py" compare --repo "$MODELS_REPO" --branch "$BRANCH" --models-dir "$MODEL_DIR" --state "$STATE"; fi
    else
      [[ -f "$CONF" ]] || save_conf
      ((SKIP_DATA)) || update_data; rebuild
      say '① 網站：差異上傳；未知遠端檔案預設保留'
      sync --push --message "${MESSAGE:-MacGyver Academy V15 update $(date +%F)}" ${sync_extra[@]+"${sync_extra[@]}"}
      if ((!skip_models)); then say '② 模型：分片與提交檢查點'; models; fi
      say '上傳完成。請到 GitHub Actions 確認網站建置與 Pages 狀態。'
    fi ;;
  stocks)
    [[ -n "$PY" ]] || die '需要 Python 3.10+'
    update_data
    sync --push --only public/academy/data/markets.json --only public/academy/data/fx.json --message "Weekly market & FX snapshot $(date +%F)" ;;
  models) [[ -n "$PY" ]] || die '需要 Python 3.10+'; models "$@" ;;
  schedule) schedule ;;
  unschedule) unschedule ;;
  -h|--help|help) sed -n '2,25p' "$0" ;;
  *) die "未知指令：${cmd}（bash macgyver.sh help）" ;;
esac
