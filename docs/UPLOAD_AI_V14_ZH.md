# V14：跨平台啟動、AI 與差異上傳

更新日：2026-10-21。本套件提供原始碼、HTML、瀏覽器推論執行器與模型下載／匯入工具；不附大型模型權重、API 金鑰或私人帳號資料。以下操作在你的電腦執行，交付時尚未替你推送 GitHub 或部署網站。

## 電腦與手機

Mac Intel／Apple Silicon、Linux 可在終端機執行 Bash；Windows 可用 Git Bash 或 WSL，或在 PowerShell 中執行 `bash ./run-local.sh`（須先安裝可用的 Bash）。先安裝 Git、Python 3.10+；修改網站或執行完整 Node 測試請用 Node.js 22.13+。模型能否運作取決於可用記憶體、CPU 與所裝推論器；瀏覽器 CPU 模式不要求 NVIDIA GPU，仍需支援 WebAssembly／Worker 的安全瀏覽器環境。

```bash
bash run-local.sh
```

依終端機顯示網址開啟網站。桌機、筆電、平板與手機共用響應式介面。手機連伺服器須使用可連線的 HTTPS 網址；手機的 `localhost` 指手機本身。將 Python 服務放在受管理 HTTPS 反向代理之後，維持網站與 `/api/` 同源；不要把模型服務或金鑰直接公開給手機。GitHub Pages 提供靜態網站，不能單獨執行 Python API；須配置獨立完整後端部署，或使用使用者明確載入的瀏覽器本機文字模型。

## 生成式學徒助教

ChatGPT、Claude、Gemini 網站帳號和 API 服務是不同介面；允許開網站不會自動取得 API 金鑰。把金鑰放在伺服器環境或本機 `.env`，不放進 public、HTML 或前端設定。複製 `.env.example` 後選一條路線設定：

- OpenAI 相容服務：`AI_BASE_URL`、`AI_API_KEY`、`AI_MODEL`；網址使用該服務官方 API 設定。設定來自伺服器，瀏覽者不能指定任意上游 URL。
- Claude 原生：`ANTHROPIC_API_KEY`、`ANTHROPIC_MODEL`；model 填帳號實際可用的模型 ID。後端呼叫官方 Messages API，支援文字與經驗證的圖片，金鑰只在請求標頭。
- Gemini 原生：`GEMINI_API_KEY`，可另設 `GEMINI_MODEL`。預設沿用套件設定；模型權限與供應商可用性以帳號實況為準。

```bash
bash run-ai-cloud.sh
```

本機 CPU 路線使用已安裝的 Ollama 模型（需先啟動 Ollama）：

```bash
bash run-ai-local.sh
bash run-ai-local.sh --vision
```

只有加上 `--download` 才會下載該啟動器的模型。`MACGYVER_MODEL`／`MACGYVER_VISION_MODEL` 可選已安裝模型；不保證每個模型都支援圖像。後端送 Ollama 的選項指定 CPU `num_gpu:0`。瀏覽器內模型在學徒明確同意後才下載、驗證 SHA-256 並載入，圖片使用合適的本機伺服器或明確同意的雲端路線。回答會區分引用資料與生成內容；推論品質、專業答案正確性仍需驗證。

## 79 種語言

介面依瀏覽器語言偏好順序選語系，處理繁簡中文地區別名與 RTL 文字方向；使用者可自行切換。中文／英文原始教材、部分詞典與已快取機器翻譯可離線使用。其餘全文需要已載入的本機文字模型、瀏覽器翻譯能力或配置的 `/api/translate` 服務，不能把「可選 79 種目標語言」解讀成「79 種全文已由人工審校」。

全文翻譯分批進行，每批檢查筆數、順序與非空字串；失敗保留原文並顯示部分完成／服務未配置。公開課文與 UI 可送往設定的翻譯器，使用者表單輸入、私人筆記及程式碼不作自動全文翻譯。已載入模型可同時供助教與翻譯共用，忙碌或失敗時不自動另下載模型。專業術語、公式與單位需要人工複核。

## 一個 Bash 檔更新網站與權重

先設定 Git 身分與 GitHub 認證，確認網站倉庫 `kuonanhong/macgyver-academy` 可寫，權重倉庫 `kuonanhong/PRIVATE-MODELS` 為 Private。私人設定預設寫在使用者目錄的 `.macgyver-academy.conf`，不會上傳；可用 `MACGYVER_CONF` 指定另一個設定檔。

```bash
bash macgyver.sh doctor
bash upload-all.sh --dry-run --skip-models
bash upload-all.sh --skip-models --skip-data
```

第一行檢查環境，第二行只比較，第三行更新網站且保留現有行情。需同時更新權重時：

```bash
bash upload-all.sh --models-dir ./models --batch-mib 120
```

`all` 預設會準備 manifest 指定的模型；若只想同步你已放入目錄的權重，在私人設定檔設 `MODELS=''`，再執行上述命令。`HUATUO_DIR` 可指向既有 HuaTuo 模型／分片，僅作讀取匯入，不修改原資料。權重儲存工具只管理 `projects/macgyver`；其他專案既有相同 Git blob 可重用，其路徑與內容不會刪除或改寫。

網站以 Git blob 比對，只提交新增與修改；自動移除以前由此同步工具管理且本地已移除的檔案及過期產生分片。遠端另加而未由本工具管理的檔案預設保留；`--prune` 才明確清理它們，`--no-delete` 可禁止移除。工具不使用 force push，遠端同檔衝突會停止供檢查。公開快照排除私人文件、金鑰、帳號資料、模型權重。

權重以 40 MiB 分片，預設每批最多約 120 MiB 的新內容建立提交並推送，`--batch-mib` 可選 40–1024。每批推送最多嘗試 4 次（首次加 3 次退避重試）；已到遠端的內容可續用。Git 的壓縮傳輸失敗可能重傳尚未完成那一批，這是提交檢查點續傳，並非保證每個 TCP 位元組都續接。

```bash
bash macgyver.sh models-compare
bash macgyver.sh restore-models ./restored-models
```

還原檢查路徑、檔案大小與整體 SHA-256。不要把未成功的半成品當可用權重。若上傳中斷，修復網路後重跑原命令；保留專案外的同步狀態目錄可加快重試。成功推送後到 GitHub Actions 檢查網站建置／Pages 結果，推送成功不代表部署成功。

保護付費課文模式必須先完成對應權限後端配置；公開匯出會先剝除內容，再用 Node 重建所有 lazy／離線分片，缺少 Node 時拒絕匯出。保護模式不能搭配 `--no-delete`，避免留下舊的完整課文。隱藏按鈕不是存取控制，權限由伺服器逐課判斷。

## 已驗證的範圍

詳見 `AI_SYNC_VALIDATION_V14.json`。測試使用本機 Git remote、極小假權重、受控 DOM 與假 API；不連線真實付費 API、不上傳 GitHub、不下載大型權重，也沒有宣稱在每一手機／Mac Intel 上完成實機推論效能量測。

## API 文件核對（2026-10-21）

Gemini 預設模型 `gemini-3.5-flash-lite` 已依 Google 官方模型目錄核對。按照官方遷移說明，請求不再送出已淘汰的 `temperature`、`top_p` 或 `top_k`；保留結構化 JSON 輸出與輸出長度限制。Claude 使用官方 Messages API、`x-api-key` 與 `anthropic-version: 2023-06-01`。這是接口格式核對，沒有替你呼叫付費帳號。

- https://ai.google.dev/gemini-api/docs/models/gemini-3.5-flash-lite
- https://ai.google.dev/gemini-api/docs/generate-content/whats-new-gemini-3.6
- https://docs.anthropic.com/claude/reference/getting-started-with-the-api
- https://docs.anthropic.com/claude/reference/versioning
