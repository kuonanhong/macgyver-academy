# V8.1：四條 AI 路線、圖片提問與明確同意

四條路線共用 AI 師傅問答視窗，但安裝條件不同。沒有對所有硬體、語言與工程問題都最好的模型；本版提供可切換的候選，沒有冒稱已在您的 Intel Mac 做模型排名或速度測試。

| 路線 | 模型候選 | 需要什麼 | 圖片 | 問題送到哪裡 |
|---|---|---|---|---|
| 瀏覽器 CPU | Qwen2.5 0.5B、Qwen3 0.6B | HTTPS／本機 HTTP、同意下載約 491／639 MB | 否 | 在目前瀏覽器推論 |
| 本機 Ollama 文字 | Qwen3 4B Q4_K_M | Ollama、Python 3.10+、約 2.5 GB 權重 | 否 | 同電腦的 Ollama |
| 本機 Ollama 圖文 | Qwen3-VL 2B Q4_K_M | Ollama、Python 3.10+、約 1.9 GB 權重 | 是 | 同電腦的 Ollama |
| Gemini 雲端圖文 | Gemini 3.5 Flash-Lite | 自己的伺服器設定 Gemini API key／配額 | 是 | Google Gemini |

原生 llama.cpp Qwen3 1.7B 及原有 OpenAI 相容文字服務仍保留。站內原有機器翻譯也可使用已設定的 Gemini／Ollama JSON 回覆；由學員明確啟用翻譯，翻譯文字會交給目前伺服器預設路線，並不等同人工完整翻譯。Ollama 翻譯批次使用 16,384 context，需要額外記憶體。

本版未下載大型模型做真實推論，也未替您申請 API key；已設定清單代表伺服器設定，模型是否已啟動、帳號配額與回答品質仍需實際測試。網站不會把課程摘要假稱為生成式回答。

## 本機文字與圖片：明確下載後再開啟

先從 https://ollama.com/ 安裝與您的 OS 相容的 Ollama，開啟應用程式或另開終端機執行 `ollama serve`。目前官方 macOS 要求 14 Sonoma 以上；較舊 Intel Mac 可考慮 [原生 llama.cpp CPU 路徑](LOCAL_AI_V8_ZH.md)，本套件不保證舊 OS 能安裝最新 runtime。

```bash
# 只下載文字模型並啟動：
bash run-ai-local.sh --download
# 只下載圖片模型並啟動：
bash run-ai-local.sh --vision --download
# 明確同意下載兩者並啟動：
bash run-ai-local.sh --both --download
# 後續啟動已安裝模型，不下載：
bash run-ai-local.sh --both
```

Windows PowerShell 可用 `./run-ai-local.ps1 -Both -Download`，後續去掉 `-Download`；Git Bash／WSL 使用 `.sh`。未加下載參數且模型不存在時，腳本會停下提示，絕不自動拉取權重。Ollama 自行管理權重位置、續傳與 manifest 雜湊；`models/` 的 rclone 備份只涵蓋該資料夾的 GGUF，並不自動包含 Ollama 的獨立快取。

請使用終端機印出的**本機網站網址**，註冊／登入該 Python 服務的帳號，在 AI 視窗選已設定的路線。原生問答請求強制 `num_gpu: 0`、`num_ctx: 8192`，以 CPU 執行；圖片處理會額外使用記憶體與時間，8 GB 是規劃起點，不是所有圖片都可流暢推論的保證。伺服器最多等待 180 秒，可用 `AI_TIMEOUT_SECONDS=300` 調到 300 秒。

GitHub Pages 不能執行 Python 後端。公開 HTTPS 網頁也不會擅自連到訪客的 Ollama／localhost；若需要原生模型，就開啟自己的同源本機網站。不要將沒有認證的 Ollama 埠公開到網際網路。

## Gemini：金鑰放在自己的後端

官方模型清單：https://ai.google.dev/gemini-api/docs/models 。預設 `gemini-3.5-flash-lite`，實際可用性與計費依自己的 Google 帳號、地區及目前服務規則。可設定 `GEMINI_MODEL` 為自己的帳號支援的圖文模型；程式不保證任意名稱都可用。

將 `.env.example` 複製為 `.env`，在本機編輯器填入 `GEMINI_API_KEY`，不要傳到 GitHub。或者在 Bash 暫時輸入而不將金鑰寫進命令歷史：

```bash
read -r -s -p 'Gemini API key: ' GEMINI_API_KEY
printf '\n'
export GEMINI_API_KEY
bash run-ai-gemini.sh
# 停止網站後清除該終端機的環境值：
unset GEMINI_API_KEY
```

PowerShell 可在私有 `.env` 填好 key 後執行 `run-local.bat`；不必將 key 寫在命令參數。Python 只讀取 KEY=value，不執行 `.env` 內容。金鑰留在 Python 程序，使用 `x-goog-api-key` header 傳給固定 Google API 網域，不在 `/api/config`、HTML、匯出包或回覆中出現。

每一次雲端提問，都必須同意傳送**問句、課程引用、可能檢索到的本機教材片段及本次圖片**。未同意，伺服器在讀取教材／呼叫供應商前拒絕。私有教材若不能交給雲端，請選本機路線；不要只看模型名稱判斷資料去向。雲端供應商的資料保存政策依其服務條款，本站不保證其零保存。原有非 loopback OpenAI 相容路線亦需逐次同意。

## 圖片提問與錯誤提示

選圖片路線後，附上一張 PNG／JPEG／WebP，檔案最多 4 MiB；建議先縮至長邊 2,048 px。伺服器還會檢查 base64、格式標記與尺寸：單邊最多 8,192 px、總計最多 3,200 萬像素。這是輸入界線檢查，不是專業影像真偽／安全鑑定。圖片不寫入本網站檔案、資料庫或歷史紀錄；本次請求結束後不留持久副本。

範例：「這張晶圓照片中哪些是可見特徵？哪些製程、尺度或缺陷種類無法只靠照片判斷？請連結本課的知識点。」模型必須區分可見特徵、推測與不可判定，不能從照片冒稱取得精確尺寸或原廠製程條件。

不支援圖片的路線會拒絕圖片；未安裝、服務未啟動、配額耗盡或供應商拒絕，都顯示錯誤，不會改用假生成答案。不把供應商錯誤原文、密鑰或問句寫入日誌。可以移除圖片、改選已設定路線或先使用課程知識摘要。

## API 契約與驗證

`GET /api/config` 回傳 `aiAvailable`、`aiRoutes` 與 `imageLimitBytes`。每個路線項目只有 `id,label,model,supportsImages,cloud,destination`；清單不暴露 key。`GET /api/me`、註冊與登入回覆也帶路線清單。

`POST /api/tutor` 仍需同源登入 cookie，接收 `question,context,language`，另加 `route`、可選 `image:{mimeType,data}`（純 base64）、雲端 `cloudConsent:true`；一次最多一張圖。回覆有 `answer,generated,model,route,references`。圖片路線同樣受每帳號每小時 60 次限制。輸入尺寸與同意檢查在供應商請求之前完成。

自動測試使用假供應商回覆，驗證同意、路線選擇、金鑰不外露、圖片界線、錯誤處理與下載參數；沒有把真實課程、使用者圖片或秘密送給供應商來測試。套件下載也不包含模型權重。

官方來源（2026-10-13 查閱）：
- https://docs.ollama.com/api/chat
- https://docs.ollama.com/capabilities/vision
- https://ollama.com/library/qwen3-vl:2b
- https://ollama.com/library/qwen3:4b
- https://docs.ollama.com/macos
- https://ai.google.dev/gemini-api/docs/models
- https://ai.google.dev/api/generate-content
- https://ai.google.dev/gemini-api/docs/api-key
