#!/usr/bin/env bash
# A model is downloaded only when --download is explicitly supplied.
set -euo pipefail
TASK_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
DOWNLOAD=false
MODE=text
SERVER_ARGS=()
while (($#)); do
  case "$1" in
    --download) DOWNLOAD=true ;;
    --vision) MODE=vision ;;
    --both) MODE=both ;;
    --help|-h)
      echo 'Usage: bash run-ai-local.sh [--vision|--both] [--download] [server arguments]'
      echo 'Default: use installed qwen3:4b. --vision: qwen3-vl:2b. --both: both routes.'
      echo 'Only --download authorizes an Ollama model download (about 2.5 GB text / 1.9 GB vision).'
      exit 0 ;;
    *) SERVER_ARGS+=("$1") ;;
  esac
  shift
done
if ! command -v ollama >/dev/null 2>&1; then
  echo '請先從 https://ollama.com/ 安裝相容的 Ollama，啟動後重新執行本檔。' >&2
  exit 1
fi
if ! ollama list >/dev/null 2>&1; then
  echo '請先開啟 Ollama 應用程式，或在另一個終端機執行 ollama serve。' >&2
  exit 1
fi
export OLLAMA_BASE_URL='http://127.0.0.1:11434'
MODELS=()
if [[ "$MODE" == text || "$MODE" == both ]]; then
  export OLLAMA_TEXT_MODEL="${MACGYVER_MODEL:-qwen3:4b}"
  MODELS+=("$OLLAMA_TEXT_MODEL")
fi
if [[ "$MODE" == vision || "$MODE" == both ]]; then
  export OLLAMA_VISION_MODEL="${MACGYVER_VISION_MODEL:-qwen3-vl:2b}"
  MODELS+=("$OLLAMA_VISION_MODEL")
fi
for MODEL_NAME in "${MODELS[@]}"; do
  [[ "$MODEL_NAME" =~ ^[a-zA-Z0-9][a-zA-Z0-9_.:/-]*$ ]] || { echo 'Invalid model name.' >&2; exit 2; }
  if $DOWNLOAD; then
    ollama pull "$MODEL_NAME"
  elif ! ollama show "$MODEL_NAME" >/dev/null 2>&1; then
    echo "尚未安裝 ${MODEL_NAME}。若同意下載權重，請加上 --download 後重跑本檔；目前未下載。" >&2
    exit 1
  fi
done
echo '本機 AI 路線已設定；請使用接下來顯示的本機網站，註冊／登入本機帳號。'
echo 'CPU 推論可能需要數分鐘；網站的路線清單顯示設定，不代表已實測模型品質。'
exec bash "$TASK_ROOT/run-local.sh" "${SERVER_ARGS[@]}"
