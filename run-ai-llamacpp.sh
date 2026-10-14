#!/usr/bin/env bash
# Native CPU alternative for Intel Mac / Linux / Windows Git Bash or WSL.
set -euo pipefail
TASK_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
MODEL_FILE="${MACGYVER_GGUF:-$TASK_ROOT/models/Qwen3-1.7B-Q8_0.gguf}"
MODEL_PORT="${MACGYVER_AI_PORT:-8383}"
THREADS="${MACGYVER_CPU_THREADS:-8}"
[[ -f "$MODEL_FILE" ]] || { echo '先執行 bash install-ai-models.sh --model qwen3-17b --download' >&2; exit 1; }
command -v llama-server >/dev/null 2>&1 || { echo '需要 llama.cpp 的 llama-server；安裝或 CPU 編譯步驟見 docs/LOCAL_AI_V8_ZH.md。' >&2; exit 1; }
[[ "$MODEL_PORT" =~ ^[0-9]+$ && "$THREADS" =~ ^[0-9]+$ ]] || { echo '埠與執行緒數必須是整數。' >&2; exit 2; }
TASK_PYTHON=''
for candidate in python3 python; do
 if command -v "$candidate" >/dev/null 2>&1 && "$candidate" -c 'import sys;sys.exit(sys.version_info<(3,10))' 2>/dev/null; then TASK_PYTHON="$candidate"; break; fi
done
[[ -n "$TASK_PYTHON" ]] || { echo '需要 Python 3.10+。' >&2; exit 1; }
"$TASK_PYTHON" - "$MODEL_PORT" <<'PY'
import socket,sys
port=int(sys.argv[1])
if not 1024<=port<=65535:sys.exit('Choose a port from 1024 to 65535.')
with socket.socket() as s:
 try:s.bind(('127.0.0.1',port))
 except OSError:sys.exit('AI port is occupied. Set MACGYVER_AI_PORT to another port; no existing process was stopped.')
PY
export AI_BASE_URL="http://127.0.0.1:$MODEL_PORT/v1"
export AI_API_KEY="$("$TASK_PYTHON" -c 'import secrets;print(secrets.token_urlsafe(32))')"
export AI_MODEL='macgyver-cpu'
llama-server --model "$MODEL_FILE" --alias "$AI_MODEL" --host 127.0.0.1 --port "$MODEL_PORT" --api-key "$AI_API_KEY" --n-gpu-layers 0 --threads "$THREADS" --ctx-size 16384 --jinja >/dev/null 2>&1 &
AI_CHILD=$!
cleanup(){ kill "$AI_CHILD" 2>/dev/null || true; }
trap cleanup EXIT INT TERM
"$TASK_PYTHON" - "$MODEL_PORT" "$AI_CHILD" <<'PY'
import urllib.request,time,sys,os
for _ in range(240):
 try:
  request=urllib.request.Request('http://127.0.0.1:'+sys.argv[1]+'/health',headers={'Authorization':'Bearer '+os.environ['AI_API_KEY']})
  with urllib.request.urlopen(request,timeout=2) as r:
   if r.status==200:break
 except Exception:pass
 try:os.kill(int(sys.argv[2]),0)
 except OSError:sys.exit('llama-server exited. Verify its version, model and OS compatibility.')
 time.sleep(.5)
else:sys.exit('Model did not become ready within 120 seconds.')
PY
echo '原生 CPU 模型已就緒；請使用接著顯示的本機網站網址，登入本機帳號後提問。'
bash "$TASK_ROOT/run-local.sh" "$@"
