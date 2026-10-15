# V13 驗證紀錄（2026-10-15）

## 1. 自動檢查

| 檢查 | 結果 |
|---|---|
| `python3 tools/structures-v13/validate_input.py` | 100／100 門原稿 OK（欄位、長度、數字、雙語、來源類型、上市代號格式） |
| `python3 tools/validate-data.py` | PASS：2,066 選題、710 門逐步課程、20,274 步、45,440 知識點、2,028 來源 |
| `node tools/test-frontend.mjs` | passed：4,132 次專案頁、40,548 次步驟頁渲染；710 門全部可見；AI 師傅上下文、會員、進度遷移等 |
| `node tools/test-payments-v12.mjs` | payments ok（含 V13 價位規則：網頁 `tidyPrice()` 與伺服器 `amountFor()` 逐幣別一致） |
| `python3 -m unittest discover -s tests` | 63 項，只有 2 項啟動器測試失敗（V12 原包即失敗：埠號佔用測試依賴本機環境） |
| 其他 `tools/test-*.mjs` | 33／38 通過；未通過的 5 項在 V12 原包相同失敗（缺 typescript、tailwind 等開發套件或缺 `public-player/.openai/hosting.json`），與 V13 無關 |
| 瀏覽器實測（Chromium） | 桌機 1366 px、手機 390 px、平板 820 px：無橫向捲動；繁中／日文／德文介面翻譯正確；日文顯示 ¥1,480／¥12,300、德文 8,49 €／69,49 €、台灣 NT$299／NT$2,490 |
| `tests/test_models_sync.py` | 私人倉庫：只傳新分片、引用同倉庫相同內容、不動其他專案資料夾、刪除不再引用的分片、還原後逐位元相同 |

## 2. 課程內容的查證方式與限制

- 100 門課由 13 位撰寫助手分組完成，每門都經驗證程式檢查；所有算例與定量模型都由助手以程式重算並標示為教學假設。
- 撰寫中途，整輪共用的**網路搜尋額度（200 次）用完**。之後的來源改為直接開啟官方網頁（WebFetch）逐頁核對；
  各組回報「每個列出的來源網址都已開啟確認」，少數廠商首頁因網站阻擋自動讀取而未逐頁確認（例如 sydneyoperahouse.com、topcon.com、dot.ny.gov、lotteenc.com、ceci.com.tw），這些都是公司或機關的官方首頁。
- 無法確認的數字一律寫成「約」或移入教學假設算例；來源互相矛盾時採業主／CTBUH 數值並註明。
- 另有兩位**獨立審查者**（未參與撰寫）逐門複核 37 門具名巨作與阻尼器、外伸臂課程的關鍵數據：
  - 橋梁 20 門：修正 6 處（例：米約高架橋懸臂施工用的是預先安裝的永久斜索、昂船洲大橋 COWI 為 Arup 團隊分包顧問、聯邦大橋最重構件約 7,500 公噸、昆斯費里通車時才是最長三塔斜張橋），另把 2 個來源不一的數值改為範圍或「約」。
  - 建築 17 門：修正 22 處（例：電梯「部數」與「車廂數」、上海中心大廈基坑面積、東京晴空塔 TMD 位置、樂天世界塔為「韓國最高」而非「首座超高層」、威利斯大樓用鋼量比較、ICC 岩盤深度、雪梨歌劇院預力鋼索長度、慕尼黑屋頂封閉期間）。
- 仍有少數細節各來源不一（例：部分完工年份相差一年、帝國大廈單位用鋼量 42 或 66 lb/ft²），課程中已以「約」或並列方式處理。

## 3. 上市代號

- 54 家新增公司附上市代號，大多來自作者簡報的已核對清單；以下為助手依專業知識填寫、未逐一在交易所網站核對：
  AkzoNobel（AMS:AKZA）、Norsk Hydro（OSL:NHY）、Intertek（LSE:ITRK）、Mitsubishi Heavy Industries（TSE:7011）、Rockwell Automation（NYSE:ROK）、
  POSCO Holdings（KRX:005490）、Sun Hung Kai Properties（HKEX:0016）、Lincoln Electric（NASDAQ:LECO）、Enerpac（NYSE:EPAC）、
  Las Vegas Sands（NYSE:LVS）、Severfield（LSE:SFR）、ESAB（NYSE:ESAB）、Sherwin-Williams（NYSE:SHW）、PPG（NYSE:PPG）。
- 每週股價更新（`bash macgyver.sh stocks` 或 GitHub Action）會自動比對交易所登記名稱，不一致者在網頁標示「代號待核對」。
- 無法確認者一律 `null`（例：Topcon、FARO 已下市或被收購的可能性、DL E&C、Kumagai Gumi、Hazama Ando、Tobu Railway）。

## 4. 已知限制

- 77 種介面語言為 AI 翻譯並通過格式驗證，尚未經母語者審稿；助手特別建議複核 am、ha、yo、ig、zu、so、cy、km、my、lo、fil、mn 的土木術語。
- 課程正文只有繁中與英文；其他語言由支援的 Chrome 以裝置內建翻譯。
- `rebuild-curriculum.sh`（舊版各代課程重播）在 V12 原包已無法完整跑完（V8 半導體步驟數檢查失敗）；V13 課程請用 `bash rebuild-structures.sh`。
