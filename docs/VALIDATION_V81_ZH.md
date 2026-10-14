# V8.1 交付與驗證紀錄

本次在 V8 的 99 門半導體逐步課程上補入附件所列的圖片問答與四條執行路線。課程、步驟 ID、照片與來源資料保留；側欄顯示 08.1，完整操作入口為 `public/academy/help.html`。

## 本次驗證

- 資料檢查通過：2,000 選題、143 門逐步課程（半導體 99）、4,106 步、8,212 知識點、660 來源、73 照片。其餘 1,857 項仍為研究工作表。
- Python 41 項測試通過，含帳號隔離、進度衝突、模型下載雜湊、GitHub 隔離匯出、文件與權重備份，以及新 Ollama／Gemini 路線與圖片輸入。
- 圖片問答測試涵蓋選檔只預覽、每次雲端同意、純文字模型拒絕圖片、傳送目的地、取消、圖片不寫入歷史、不隨下一題重送、切換帳號與課程時清除。
- 代管後端檢查涵蓋無金鑰時不提供路線、圖片 MIME／尺寸／base64／4 MiB 上限、同意前不呼叫供應者、固定 Gemini 網域及金鑰只在 header。修正接近 4 MiB 的 base64 驗證造成正規表示式堆疊溢位，新增上限回歸案例。
- 實際素材檔頭解析檢查涵蓋 72 張 JPEG、1 張 PNG 與 WebP 範例；前端另與實際影像尺寸對照。不是對每張圖做模型辨識。
- 完整前端 VM 檢查涵蓋 4,000 個中英專案頁及 8,212 個工序畫面、連續三步、示範與輔助、鍵盤／觸控控制、帳號儲存及課程來源。
- 離線啟動、本機學習檔案、可選 Supabase 請求、來源反向引用與模型 adapter 測試通過。套件包含經重建的 classic bundle、8 組完整內嵌資料與 CPU runtime。
- TypeScript 檢查、Bash 語法及 Python 編譯通過；發布前執行 Sites 正式建置。

## 本次沒有完成的外部驗收

尚未取得／設定使用者的 Supabase 專案、Gemini API key、GitHub 倉庫認證或模型備份目的地。本次沒有開設付費服務、發送驗證信、實際 git push 到使用者 GitHub、下載大型模型權重或做真實推論。供應者測試使用模擬回覆，並非速度、準確率或跨裝置實測。

環境未提供支援的瀏覽器控制，本次沒有 Chrome／Safari／手機版面及語音實測。課程可以直接雙擊 index.html；瀏覽器模型 worker 仍需 HTTPS 或本機 HTTP。影片、Google Maps 及雲端模型的實際可用性取決於外部服務。

繁中與英文是人工編寫核心；另外 77 個語言選項仍需要設定機器翻譯。教學圖與操作是工程概念教具，並非原廠完整製造配方、完整物理模擬或每道工序的實拍紀錄。

## 重現新增檢查

```bash
python3 -m unittest discover -s tests -v
node tools/test-hosted-ai.mjs
node tools/test-tutor-panel.mjs
node tools/test-tutor-vision.mjs
node tools/test-ai-accounts.mjs
bash build-offline.sh
node tools/test-offline.mjs
node tools/test-static-learning.mjs
python3 tools/validate-data.py
```

`test-hosted-ai.mjs` 需先依鎖檔安裝開發相依套件（使用 TypeScript transpile API）。開啟已封裝的離線課程不需要安裝開發套件。
