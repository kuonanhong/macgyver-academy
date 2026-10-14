# V7 驗證紀錄

本檔記錄本次發佈前的檢查範圍；數量以 public/academy/data/release.json 為準。

## 自動化檢查

- 2,000 個唯一工程／工藝題目、49 門已編寫課程、1,951 個研究工作表。
- V7 新增 12 門，各 4 階段、24 步，共 288 步；合計 1,850 步。
- 舊版 37 門的階段與步驟 ID 保留，避免使既有學習紀錄失去對應。
- 49 門各兩項相近工程，共 98 組比較；與對應課程據點一致，Google Maps 連結使用緯經度。
- 「您提供的課程教材」頁籤及 materials.json 已移除；離線資料不再包含此索引。
- 原創領域圖示／插畫 20 組，2,000 題各有穩定識別；49 門課另有明確主題輪廓。
- 49 門雙語專案頁、全部雙語工序、搜尋與分頁、課程啟動、操作狀態、鍵盤焦點、師傅示範、工程輔助、驗收和下一步皆納入程式檢查。
- 完整經典 JavaScript 離線封裝測試：file 模式不依賴原生 fetch，資料預載、個人檔案、重新載入和 JSON 備份均可操作。
- GitHub 匯出檢查：排除憑證／私有資料／模型；隔離輸出；首次推送、更新與分歧停止以本機 bare Git 倉庫驗證。沒有實際推送到使用者 GitHub。
- 可選 Python 後端與匯出工具共 22 項單元測試通過。

## 圖像及人工檢查

SVG 結構與雙語文字經解析；49 個主題圖示及系統示意接觸表使用本機 SVG 渲染工具查看。修正 High-NA 反射路徑、風場集電連線和 PET 響應線端點。插畫、原理示意與實景照片有不同標籤。

執行環境未提供支援的瀏覽器控制，因此沒有聲稱已在真實 Safari／Chrome／手機／平板逐台試用，也沒有在瀏覽器中實際播放所有語音、Google Maps 或影片。程式測試不等同真實工業驗證。

## 可重現的主要命令

```bash
bash rebuild-curriculum.sh
node tools/test-frontend.mjs
node tools/test-offline.mjs
node tools/test-v7-contexts.mjs
node tools/test-course-places.mjs
node tools/test-related-skills.mjs
node tools/test-learning-media.mjs
node tools/test-demo-controller.mjs
python3 -m unittest discover -s tests -v
bash deploy-static.sh
```

所有外部內容仍受原發布者／服務與瀏覽器政策影響。本版未新增官方設備 CAD、製造配方、核准施工文件或每步專屬實拍。
