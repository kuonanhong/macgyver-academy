# V9：先進封裝與矽光子 100 門課程

本版把目錄中「先進封裝與矽光子」的 100 項主題全部展開為逐步課程。新增 97 門，每門 4 階段、24 個工程學習步驟；既有先進封裝總覽保留 520 步，矽光子與 CPO 課程擴為 48 步，晶圓對晶圓混合接合擴為 36 步。這個領域合計 2,932 步；連同其他領域，全站共有 240 門逐步課程、6,482 步，另有 1,760 項研究工作表。

這些是公開原理的工程教學拆解。24 或 520 是學習步驟數，不是原廠量產 traveler 的工序數。未公开材料配方、機台參數與產品驗收規格沒有被臆造補齊。

## 先找到課程

1. 完整解壓新版；雙擊最外層 `index.html`。側欄應顯示 **ENGINEERING EDITION / 09**。
2. 「探索工程」新增「先進封裝與矽光子」專區，點「探索全部 100 門」。也可直接開 `public/academy/index.html#catalog/domain/packaging`。
3. 以「專業子領域」縮小範圍。晶粒接合、TSV、基板、熱管理、光學耦合、相移、CPO 等不是混在同一長清單。
4. 展開 8 條建議學習路線，依問題選擇先修順序。這是學習導覽，不是將彼此互斥的製造方法串成同一量產流程。
5. 課程簡報先閱讀目的、範圍、原創架構圖、地點故事及相近工法，再進入工作台。

## 本次教學內容

| 面向 | 學習方式 |
|---|---|
| 原理與假設 | 識別材料、介面、能量／訊號流、模型假設與適用範圍 |
| 定量推理 | 在明示的假設數值下計算，核對單位、敏感度及不確定度 |
| 量測規劃 | 定義量測量、參考平面、校正、對照樣本與取樣方式 |
| 失效判讀 | 分開直接觀察與原因假說，提出能區分競爭假說的證據 |
| 操作與驗收 | 師傅示範、學徒控制概念教具、提交證據、自己完成測驗 |
| 延伸工法 | 每門有兩項相近課程，說明能轉用的原理、差异與三步比較練習 |
| 地點與來源 | 顯示代表研究／產業據點、地址、經緯度、Google Maps 及原始來源 |

波導／耦合損耗不能直接等同封裝良率；熱阻模型不能取代完整熱機耦合；單一照片不能證明根因。課程與互動算例會明示這些界線，要求把模型結果與量測證據連起來。

## 照片、架構圖與影片

- 真實照片與顯微影像隨包附上作者、原始頁、授權及代表用途。圖片會跨課程共用，不宣稱每一步均有專屬量產實拍。
- 主題架構圖由本站原創繪製，採不同幾何與拓樸呈現接合面、穿孔、中介層、光波導、雷射、調變、偵測與系統介面。它們不是照抄廠商工程圖，也不是可施工 CAD。
- 教學影片採原发布者官方影片／頁面，按下才連線，並保留外部開啟入口。無法保證 YouTube 在每個地區、瀏覽器及網路都免登入；本版沒有繞過平台限制。
- 影片及引導工作單提供觀察重點與比較問題；外部影片未下載打包。
- 「知識與來源」的子領域篩選同時支援半導體、封裝與矽光子。反向引用列出哪些逐步課程實際引用來源，照片也可追查對應課程。

## 師傅、雙手控制與保存

先看完整示範，紅箭頭會指出按鍵；熟悉後可略過按鍵導覽。實體方向鍵／WASD 操作 XY，I/K 或 PageUp/PageDown 升降，J/L 或 Q/E 旋轉，Space 抓取／放開，Shift 精調。先點工作台啟用鍵盤；文字輸入框中的方向鍵仍用於編輯。

觸控按鍵位於工作台下方；工程輔助在學徒桌上方。輔助可完成概念操作，但不代答驗收題。固定在畫面底部的大按鈕會說明還缺什麼、提交證據或前往下一步。

原有 143 門課程的所有步驟 ID 和順序保留；兩門延伸課程只在末尾追加，已完成工序不會重編。升級前仍請匯出學習及研究 JSON，並備份自己的 Python 資料庫。`file://` 儲存與瀏覽器／路徑相關，移到新資料夾時可用匯入恢復。

## 作業系統與語言

課程為響應式 HTML/CSS/JavaScript；筆電／桌機可使用鍵盤，手機／平板以觸控操作。預先建置版本不需 Python、Node.js 或本機網頁伺服器即可在一般桌機瀏覽器開啟。手機檔案預覽器不一定執行 JavaScript，建議使用 HTTPS 網站。這不代表已在所有品牌與版本的裝置實測。

繁體中文與英文是隨包完整編寫的核心。介面保留 79 種語言選項；其餘 77 種需設定翻譯服務，屬機器翻譯，並非已逐語種完整人工審定。預設語言來自瀏覽器偏好；不以 GPS 猜語言。朗讀依可用的裝置語音，沒有聲音時仍可閱讀講解。

## 生成式 AI 與帳號

本次保留 V8.1 的 AI 問答與圖片提問：瀏覽器 CPU 文字、原生 Ollama CPU 文字／視覺、可選 Gemini 雲端服務，以及 llama.cpp。下載權重仍須使用者主動同意。模型不包進 ZIP、不自動上傳，也沒有替您啟用付費 API。使用方式見 `AI_ROUTES_V81_ZH.md`、`LOCAL_AI_V8_ZH.md`。

直接開檔及 GitHub Pages 可保存本機姓名／信箱學習檔案。真正跨裝置的驗證信箱帳號需設定隨附 Supabase Auth／RLS；GitHub Pages 本身不執行 Python 或秘密金鑰後端。設定步驟見 `GITHUB_ACCOUNTS_V8_ZH.md`。

## 重建、上傳與權重備份

課程作者可修改 `tools/packaging-v9/group_a.json`、`group_b.json`、`group_c.json`、`existing_enrichment.json` 及 `media.json`，再執行：

```bash
bash rebuild-curriculum.sh
```

它依序重建既有世代，最後合併 V9、檢查引用及舊 ID、更新影片白名單與離線程式。`existing_baseline.json` 是重播舊世代所需的原始教材，不是使用者進度。不要手動刪除它。只修改 HTML／JS／CSS 或已整合資料時可用 `bash build-offline.sh`。

先建立自己的 GitHub 倉庫並完成 Git 認證：

```bash
bash publish-github.sh --repo https://github.com/kuonanhong/macgyver-academy.git --dry-run
bash update-and-upload.sh --repo https://github.com/kuonanhong/macgyver-academy.git --rebuild-curriculum
```

若同時要更新私人教材索引並備份教材／模型，先設定自己的 rclone remote，再明確指定目的地：

```bash
bash update-and-upload.sh \
  --repo https://github.com/kuonanhong/macgyver-academy.git \
  --rebuild-curriculum \
  --index-documents \
  --documents /完整路徑/教材 \
  --documents-remote mycloud:MacGyver/documents \
  --models-remote mycloud:MacGyver/models
```

`mycloud` 是範例名稱，必須替換成您已設定的目的地。程式先驗證公開匯出，再 `rclone copy` 到明示位置，最後推送隔離的 GitHub 程式副本。私有教材、帳號資料庫、API 金鑰與權重不進公開 Git；`.part` 等未完成下載檔也不備份。索引只供檢索，不等於訓練模型。

Windows 可在 Git Bash／WSL 執行 `.sh`；Ollama 與本機伺服器另有既存 `.ps1`／`.bat`。本機後端及匯出需要 Python 3.10+，`pip install python` 不能升級直譯器。僅閱讀已打包課程不需要 Python。

GitHub Pages 首次發布需於 Settings → Pages 選 GitHub Actions，再手動執行包內的發布工作流程；git push 本身不保證 Pages 已啟用。代管學院保留原存取設定，發布來源包不會自動變更網站 audience。

## 程式與資料入口

- `public/academy/data/packaging-photonics-100.csv`：完整 100 門中英索引。
- `public/academy/data/release.json`：本版實際統計。
- `public/academy/packaging-paths.js`：8 條課程路線。
- `public/academy/packaging-visuals.js`、`packaging-icons.js`：原創架構圖與圖示。
- `public/academy/packaging-calculators.js`：公式、單位、參數與模型適用範圍。
- `tools/packaging-v9/`：雙語課程原稿、來源、媒體與保存 ID 清單。
- `docs/VALIDATION_V9_ZH.md`：本次驗證結果與尚未實測的服務。

English: V9 completes all 100 packaging and silicon-photonics topics with guided curricula. It preserves existing lesson IDs, adds 97 new 24-step courses, and extends two existing courses without reordering prior steps. Core content is authored in Traditional Chinese and English. Photographs are licensed representative media; diagrams and exercises are original educational models. Production recipes, unique footage of every step, universal device compatibility and fully human-reviewed localization into 79 languages are not claimed.
