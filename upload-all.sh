#!/usr/bin/env bash
# 一鍵上傳 / One-click upload — MacGyver Engineering Academy V15
#
# 在解壓後的資料夾執行：  bash upload-all.sh
#   ① 比對本機套件與 GitHub 網站倉庫（kuonanhong/macgyver-academy），只上傳新增與修改的檔案，
#      清理已管理的舊分片；未知的遠端另加檔案預設保留。
#   ② 準備 AI 模型（已存在就驗證；Qwen3-0.6B 可直接從華佗學院四份 ZIP 匯入；其餘從官方來源下載），
#      再比對私人倉庫（kuonanhong/PRIVATE-MODELS），只上傳雲端還沒有的權重分片。
# 預覽網站差異、不下載模型：bash upload-all.sh --dry-run --skip-models
# 支援 --skip-data --models-dir DIR --batch-mib 40..1024 --skip-models
# 只想先看差異、不上傳：  bash macgyver.sh compare   與   bash macgyver.sh models-compare
# 第一次使用請先：         bash macgyver.sh doctor
set -euo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
exec bash "$ROOT/macgyver.sh" all "$@"
