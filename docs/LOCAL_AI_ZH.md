> V8 新增瀏覽器 CPU 推論與 llama.cpp Intel CPU 啟動方式，請先閱讀 [LOCAL_AI_V8_ZH.md](LOCAL_AI_V8_ZH.md)。目前 Ollama 官方要求 macOS 14+；Intel x86 為 CPU 運作。

# 本機生成式 AI 師傅

本套件沒有預裝或假稱已下載模型權重。完整課程與組合工作台不依賴模型；未設定 AI 時，「課程知識模式」只是整理本工序知識，並非生成式推論。

1. 從 https://ollama.com/ 安裝符合您作業系統的 Ollama，啟動服務。
2. 於專案資料夾執行 `bash run-ai-local.sh --download`。只有明確加上 `--download` 才會透過 Ollama 下載 `qwen3:4b`，再啟動網站。註冊／登入本機帳號後可使用 AI。
3. 需要較小模型可執行 `MACGYVER_MODEL=qwen3:0.6b bash run-ai-local.sh --download`。小模型的工程推理和多語翻譯品質有限；請以課程及官方來源核對。
4. 欲使用自有服務，設定 AI_BASE_URL、AI_API_KEY、AI_MODEL，參見 BACKEND_ZH.md。金鑰只存在伺服器環境，不能寫入 HTML 或提交 Git。

Mac Intel i9／64 GB 記憶體可嘗試 CPU 模型，但本次未在您的硬體量測速度。推論超時由伺服器回報，不會假裝成功。

本機模型等待上限預設 180 秒，可用 `AI_TIMEOUT_SECONDS=300 bash run-ai-local.sh` 改為最多 300 秒。Windows 另附 PowerShell 啟動檔 run-ai-local.ps1。一般網站預設埠改為 8010，未指定埠時可自動避開已占用埠。

教材匯入：先用 `python3 -m pip install -r requirements-documents.txt` 安裝可選的 PDF 讀取套件，再執行 `bash index-documents.sh --source /完整路徑/教材`。文字、PPTX、DOCX 不需額外套件。索引保存在 portable/data/knowledge.json，自動重載；詳見 README。這不訓練模型，只將符合中英關鍵字的段落提供給本次問答，並附檔名頁碼。掃描 PDF 需先 OCR。

模型下載由 Ollama 管理；本套件 `models/` 供自行取得、且有合法再散布權利的權重使用。Git LFS 與 rclone 上傳不會自動把模型接到推論服務。Hosted 網站無法連入您 Mac 的 127.0.0.1，需使用您管理的 HTTPS 模型 API。請勿將未驗證身分的 Ollama 服務裸露到網際網路。

來源（2026-10-12 查閱）：
- https://docs.ollama.com/api/openai-compatibility ：OpenAI-compatible chat completions 介面。
- https://ollama.com/library/qwen3 ：模型與大小選擇。

授權以實際下載模型的官方 LICENSE 為準。本次只測試 AI 介面轉接與未設定時的錯誤處理，未完成真實模型推論測試。
