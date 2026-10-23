# V16 Bash 與 AI 啟動說明

在解壓縮後的 V16 專案根目錄執行：

```bash
bash macgyver.sh --help
bash macgyver.sh compare
bash Upload_MacGyver_v16_SSH.sh
```

第一行只顯示說明；第二行比較差異，不推送；第三行用 SSH 上傳網站及現成的模型／學習文件。`bash macgyver.sh` 與第三行相同。只上傳網站可加 `--skip-models --skip-documents`。私人資產的設定、檢查與還原見 `tools/upload-v16/README_ZH.md`。

請使用 `bash`，不要使用 `sh macgyver.sh`，也不要把 Markdown 的反引號或指令提示符號一起貼到終端機。macOS／Linux 可用 Bash；Windows 使用 Git Bash 或 WSL 執行上傳腳本，本機網站亦提供 `run-local.bat`。網站可在手機／平板瀏覽器使用；上傳腳本須在具備 Git、SSH 與 Python 的電腦或終端機環境執行。

## Python 與 Conda

上傳器及 AI 啟動器優先採用 `MACGYVER_PYTHON`，其次採用已啟用 Conda 的 `bin/python`，最後尋找 PATH 中可用的 `python3`／`python`，需要 Python 3.10 以上。`run-local.sh` 對已指定的 Python 會先驗證版本；版本過舊時停止並顯示需求，不會執行空指令。

```bash
conda activate svm_kernels
python --version
bash macgyver.sh --dry-run
```

若環境尚未達到 Python 3.10，可選擇另一個已安裝的新版環境，或自行建立新版環境。`pip install --upgrade pip` 不會升級 Python 本身。包含空白的完整路徑必須加雙引號：

```bash
MACGYVER_PYTHON="/完整路徑/Python/bin/python" bash run-local.sh
```

## AI 啟動

```bash
bash run-ai-local.sh --help
bash run-ai-cloud.sh --help
bash run-ai-gemini.sh --help
bash run-ai-llamacpp.sh --help
```

以上說明指令不要求模型已安裝、不讀取供應商金鑰、不下載、不連接供應商。實際啟動方式如下：

| 指令 | 需求與行為 |
| --- | --- |
| `bash run-ai-local.sh` | 已安裝且啟動的 Ollama，以及現成文字模型。只有明確加上 `--download` 才會下載。 |
| `bash run-ai-local.sh --vision` | 使用現成的影像模型；`--both` 同時提供文字與影像路線。 |
| `bash run-ai-cloud.sh` | 私有 `.env` 或環境變數中已設定的供應商金鑰與模型。 |
| `bash run-ai-gemini.sh` | 私有 `.env` 或環境變數中的 `GEMINI_API_KEY`。 |
| `bash run-ai-llamacpp.sh` | 已安裝 `llama-server` 與現成 GGUF 權重；`MACGYVER_GGUF` 可指定模型檔。 |

雲端預檢與本機伺服器沿用同一個已選定的 Python。金鑰不放進 HTML、Git 或命令列參數。啟動 AI 路線不代表已完成模型品質或實際供應商帳號測試。一般 V16 本機網站仍由 `launch_v16.py` 強制使用受保護模式，帳號與課程授權由後端檢查。

## 修訂紀錄與驗證範圍

2026-10-23：

- 新 `macgyver.sh` 預設轉到 V16 差異上傳器，避免觸發舊 V15 建置／課程數驗證。舊進階 CLI 保留為 `macgyver-legacy-v15.sh`；呼叫舊進階指令時會提示其行為。
- `run-ai-local.sh` 的空參數陣列改用 Bash 3.2 可用的條件展開，避免 `set -u` 的未綁定變數錯誤；中文顯示文字附近的變數均以大括號分界。
- 雲端、Gemini、llama.cpp 啟動器支援 Python／Conda 路徑含空白，並在檢查金鑰／模型之前處理 `--help`。
- 本機測試涵蓋無 Python、模擬舊 Python、Conda／指定 Python 優先序、空參數、中文與空白路徑、轉送參數及預覽不變更本機 bare Git 遠端。

驗證環境是 Linux Bash 5.2；已修正已知 Bash 3.2 不相容用法，但未在實體 macOS Bash 3.2 或 Windows 上執行。沒有實際連接供應商、下載模型、向 GitHub 推送或安裝排程。GitHub Pages 工作流程先呼叫 `deploy-static.sh`，由 V16 匯出器驗證課程 SHA-256、JSON／JavaScript 對應與第一節試讀限制，再產生公開目錄；上傳程式碼與發布 Pages 是分開操作。
