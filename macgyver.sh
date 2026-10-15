#!/usr/bin/env bash
# 馬蓋先 MacGyver Engineering Academy V12 — one-click maintenance.
#
#   bash macgyver.sh              same as "deploy"
#   bash macgyver.sh deploy       update stocks+FX → rebuild → validate → upload ONLY changed files
#   bash macgyver.sh compare      show what is new / modified / deleted vs GitHub (no upload)
#   bash macgyver.sh stocks       weekly stock & FX refresh, upload just those two data files
#   bash macgyver.sh models       download the browser AI model(s) and upload weights to PRIVATE-MODELS
#   bash macgyver.sh schedule     run "stocks" every Monday 09:07 on this computer (launchd / cron)
#   bash macgyver.sh unschedule   remove that schedule
#   bash macgyver.sh doctor       check git, python, node, SSH access and settings
#   bash macgyver.sh config       show / edit the saved settings
#
# Settings are saved in ~/.macgyver-academy.conf (never uploaded):
#   SITE_REPO=git@github.com:kuonanhong/macgyver-academy.git
#   MODELS_REPO=git@github.com:kuonanhong/PRIVATE-MODELS.git
#   BRANCH=main
#   MODELS="qwen25-05b"           # space-separated ids from tools/model-manifest.json
#   PROTECT_CONTENT=0             # 1 = publish static site only, paid stages stubbed (needs Supabase)
set -euo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
CONF="${MACGYVER_CONF:-$HOME/.macgyver-academy.conf}"
SITE_REPO='git@github.com:kuonanhong/macgyver-academy.git'
MODELS_REPO='git@github.com:kuonanhong/PRIVATE-MODELS.git'
BRANCH='main'
MODELS='qwen25-05b'
PROTECT_CONTENT=0
STATE="$(dirname "$ROOT")/MacGyver_GitHub_Sync_State"
# shellcheck disable=SC1090
[[ -f "$CONF" ]] && source "$CONF"

say(){ printf '\033[1;32m▶ %s\033[0m\n' "$*"; }
warn(){ printf '\033[1;33m! %s\033[0m\n' "$*" >&2; }
die(){ printf '\033[1;31m✖ %s\033[0m\n' "$*" >&2; exit 1; }
PY=''
for c in python3 python; do
  if command -v "$c" >/dev/null 2>&1 && "$c" -c 'import sys;sys.exit(sys.version_info<(3,10))' 2>/dev/null; then PY="$c"; break; fi
done

save_conf(){
  umask 077
  cat > "$CONF" <<EOF
SITE_REPO='$SITE_REPO'
MODELS_REPO='$MODELS_REPO'
BRANCH='$BRANCH'
MODELS='$MODELS'
PROTECT_CONTENT=$PROTECT_CONTENT
STATE='$STATE'
EOF
  say "設定已存到 $CONF"
}

doctor(){
  local ok=1
  command -v git >/dev/null || { warn '缺少 git（macOS：xcode-select --install）'; ok=0; }
  [[ -n "$PY" ]] || { warn '缺少 Python 3.10+（macOS：brew install python 或 conda create -n macgyver python=3.12）'; ok=0; }
  if command -v node >/dev/null; then say "Node $(node --version)（重建網站用）"; else warn '未安裝 Node.js 18+：改程式後無法重建 app.bundle.js（只更新資料仍可）'; fi
  for k in user.name user.email; do [[ -n "$(git config --global --get $k || true)" ]] || { warn "請先執行 git config --global $k \"…\""; ok=0; }; done
  if [[ "$SITE_REPO" == git@* ]]; then
    local out; out="$(ssh -o BatchMode=yes -o ConnectTimeout=10 -T git@github.com 2>&1 || true)"
    if grep -q 'successfully authenticated' <<<"$out"; then say "GitHub SSH 認證成功：${out%%!*}"; else warn "GitHub SSH 尚未設定：$out"; warn '請依 docs/UPLOAD_SYNC_V12_ZH.md 第 1 節建立 SSH key 並加到 GitHub。'; ok=0; fi
  fi
  git ls-remote --heads "$SITE_REPO" "$BRANCH" >/dev/null 2>&1 && say "可讀取網站倉庫 $SITE_REPO" || { warn "無法讀取 $SITE_REPO"; ok=0; }
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
    "$PY" "$ROOT/tools/check-offline.py" || die '程式已修改但沒有 Node.js 可重建；請安裝 Node.js 18+。'
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

models(){
  local dir="$ROOT/models"
  for id in $MODELS; do
    say "下載並驗證模型 $id（官方來源、固定版本與 SHA-256；可中斷後重跑接續）"
    bash "$ROOT/install-ai-models.sh" --model "$id" --download --directory "$dir"
  done
  say "分片上傳權重到私人倉庫 $MODELS_REPO（每片 32 MiB，可續傳）"
  warn '請確認該倉庫在 GitHub 上是 Private。'
  bash "$ROOT/upload-github-ssh.sh" --weights-repo "$MODELS_REPO" --models-dir "$dir" --weights-private-confirmed --branch "$BRANCH"
}

cmd="${1:-deploy}"; shift || true
case "$cmd" in
  doctor) doctor ;;
  config)
    echo "設定檔：$CONF"; echo "SITE_REPO=$SITE_REPO"; echo "MODELS_REPO=$MODELS_REPO"; echo "BRANCH=$BRANCH"; echo "MODELS=$MODELS"; echo "PROTECT_CONTENT=$PROTECT_CONTENT"; echo "STATE=$STATE"
    if [[ -t 0 ]]; then
      read -r -p '網站倉庫 SSH 網址 [Enter 保留]：' v; [[ -n "$v" ]] && SITE_REPO="$v"
      read -r -p '模型私人倉庫 SSH 網址 [Enter 保留]：' v; [[ -n "$v" ]] && MODELS_REPO="$v"
      read -r -p '分支 [Enter 保留]：' v; [[ -n "$v" ]] && BRANCH="$v"
      save_conf
    fi ;;
  compare) [[ -n "$PY" ]] || die '需要 Python 3.10+'; sync "$@" ;;
  deploy)
    [[ -n "$PY" ]] || die '需要 Python 3.10+'
    [[ -f "$CONF" ]] || save_conf
    update_data; rebuild
    say '比較本機套件與 GitHub，只上傳新增與修改的檔案，並刪除雲端多餘檔案'
    sync --push --message "${MESSAGE:-MacGyver Academy V12 update $(date +%F)}" "$@"
    say '完成。GitHub Pages 通常 1–3 分鐘後更新：https://kuonanhong.github.io/macgyver-academy/' ;;
  stocks)
    [[ -n "$PY" ]] || die '需要 Python 3.10+'
    update_data
    sync --push --only public/academy/data/markets.json --only public/academy/data/fx.json --message "Weekly market & FX snapshot $(date +%F)" ;;
  models) models ;;
  schedule) schedule ;;
  unschedule) unschedule ;;
  -h|--help|help) sed -n '2,20p' "$0" ;;
  *) die "未知指令：$cmd（bash macgyver.sh help）" ;;
esac
