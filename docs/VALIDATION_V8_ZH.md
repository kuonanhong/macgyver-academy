# V8 驗證紀錄

數量以 `public/academy/data/release.json` 為準。本紀錄區分程式檢查、素材檢查與尚未執行的實機驗證。

## 課程與進度

- 2,000 個目錄題目；143 門逐步課程、4,106 步、8,212 個雙語知識紀錄；其餘 1,857 題為研究工作表。
- 半導體分類 99 門均有課程，新增 94 門各 4 階段、24 步。24 步是教學工作包，不是廠商的完整量產流程。
- 與 V7 比較，原本 49 門的階段內容及 1,850 個步驟 ID 完全保留。
- 143 門皆有雙語歷史與代表據點、各兩項相近工法，共 286 組比較。重用機構據點不等於有 143 座獨立工廠。
- 資料檢查涵蓋唯一 ID、來源存在、前置關係、雙語欄位、測驗選項及可達成的互動驗收條件。
- 4,000 個雙語專案頁及 8,212 個雙語工序畫面通過 Node VM 檢查；驗證連續三步、重新載入、下一步、示範、輔助、鍵盤、雙手觸控處理、帳號切換與儲存競態。

## 照片與圖解

- 73 張隨附授權照片／量測影像，其中 24 張為 V8 新增；99 門半導體課程皆有明示用途的代表性照片。不是每道工序的現場實拍。
- 99 個半導體主題使用 36 種原創結構家族、47 種圖形變化；另有 36 種適合小尺寸呈現的原創圖示。
- SVG XML、課程對應、照片雜湊與授權欄位已檢查。使用 Inkscape 檢視照片與圖形聯絡表，以及工作台範例；不等同瀏覽器版面測試。
- 新增 6 個不同的官方 YouTube 影片 ID；全部課程合計 30 個不同 YouTube ID，重複引用另計。播放器測試涵蓋白名單、手動載入、錯誤訊息、來源與訊息驗證。
- 外部影片是否可播放，仍由平台、發布者與觀看環境決定；沒有繞過登入或年齡等限制。

## 帳號與 AI

- 本機姓名／信箱檔案、重新載入、舊版進度保留、匯入匯出與帳號隔離經測試。這種本機檔案不提供密碼驗證，也不是跨裝置帳號。
- 可選 Supabase Auth 與 SQL RLS/CAS 實作已附上。模擬請求檢查登入、驗證信、重設密碼、衝突、舊請求與帳號切換、啟動失敗後明確恢復雲端進度。
- 實際 Supabase 專案與金鑰尚未配置，沒有宣稱真實驗證信或跨裝置同步已實測。
- 瀏覽器 CPU 模型的下載同意、進度、取消、雜湊拒收、快取與引擎 API 契約經測試；wllama 套件及執行檔雜湊已固定。
- 多輪問答測試涵蓋最近三輪、長度限制、繁中提示大小、目前問題不重複、課程／帳號隔離，以及錯誤回覆不當作有效歷史。
- 沒有下載大型正式權重實際推論；沒有模型速度、答案正確率或手機記憶體的實測保證。小模型是可選學習輔助。

## 交付與測試邊界

- 完整 `index.html` 離線啟動經 VM 執行：所有 JSON 隨包、零原生網路請求、裝置檔案、備份與儲存受限時的暫存模式。
- GitHub Pages 靜態模式會在匯出時明確啟用；姓名／信箱檔案可用，Supabase 雲端帳號為選配。瀏覽器 CPU AI 需 HTTP(S)，不能從 `file://` 啟動模型 worker。
- Python 後端、資料索引、模型下載、GitHub 匯出與上傳腳本共 30 項單元測試通過。測試使用暫存檔與模擬回應，沒有向使用者 GitHub 或模型儲存空間實際上傳。
- 語音、語系切換及 CSS 已有控制器／語法檢查；完整人工編寫語言為繁中、英文，其他 77 個語言選項需設定機器翻譯與適合的語音。
- 執行環境未提供支援的瀏覽器控制，未逐台驗證 Chrome、Safari、手機及平板，也未宣稱所有外部影片、Google Maps、語音與模型已實機操作。

## 重現主要檢查

```bash
bash rebuild-curriculum.sh
python3 tools/validate-data.py
node tools/test-frontend.mjs
node tools/test-offline.mjs
node tools/test-static-learning.mjs
node tools/test-ai-accounts.mjs
node tools/test-tutor-panel.mjs
node tools/test-tutor-history.mjs
node tools/test-source-library.mjs
node tools/test-course-places.mjs
node tools/test-related-skills.mjs
node tools/test-learning-media.mjs
node tools/test-public-player.mjs
node tools/test-semiconductor-visuals.mjs
node tools/test-semiconductor-icons.mjs
node tools/test-engineering-labs.mjs
python3 -m unittest discover -s tests -v
bash deploy-static.sh
```
