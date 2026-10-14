# V8：半導體 99 門、AI 問答與可選雲端帳號

完整解壓後，雙擊根目錄 `index.html`。保留整個資料夾，不能只拿一個 HTML。課程與控制可離線，影片、Google Maps 與外部來源需網路；生成式模型依下述方式另行下載。

## 半導體課程擴充

V7 原有 49 門逐步課程全部保留。本次新增 94 門半導體專題，每門 4 階段／24 步，共 2,256 步；加上原有 5 門，目錄中全部 **99 項半導體題目**均有逐步課程。

全站仍為 2,000 項工程與工藝選題，其中 **143 門逐步課程、4,106 道教學步驟、8,212 個知識點**；另外 1,857 項是研究工作表。半導體總覽及先進封裝各 520 步，保留原來內容與工序 ID。

新課逐步涵蓋需求與物理原理、流程與介面、量測與失效、整合與驗證。各步含任務、觀察、失效判讀、驗收、兩個中英知識點、測驗及公開資料。這是完整的教學路徑，不是每門都有 500 道原廠量產工序，更不是可直接執行的機台配方或認證 SOP。

每門逐步課附相近專題與工法比較，包括共同原理、不能照搬的差異、延伸練習與來源。地圖提供有說明的代表據點與近似座標；通用半導體技術可能選研究基地或企業園區，多門共用同一地點，不把它說成唯一製造地。

## 分類來源、真實照片與架構圖

「官方資料與延伸閱讀」「照片與授權」新增工程領域、半導體子領域、引用的逐步課程及關鍵字篩選。來源卡顯示實際哪些課程引用，以及適用的課程／步驟層級；同領域不自動等於引用。保留來源 URL、照片作者與授權。

99 項半導體專題增加原創主題架構示意，並補充有授權的真實照片及官方影音入口。照片明示適用範圍，可能跨課程或步驟共用；架構示意與實景照片明確區別。每項素材精確數量與對應關係以 `data/release.json`、`data/photos.json`、`data/media.json` 為準，並非每一步都有一張專屬工廠實拍。

影片由原發布者提供，點擊才載入，不重新散布至 ZIP。YouTube、片方、地區、年齡、Cookie 或網路限制仍可能阻止頁內播放，不能由本網站取消。

## 提問與生成式回答

師傅視窗可輸入問題、觀看回答、選擇回答方式及模型。既有教材摘要與真正生成式回答分別標示。瀏覽器 CPU 有兩個模型選擇，必須先同意下載；可查看進度、取消、卸載與清除快取，固定 SHA-256 通過才載入。

| 選項 | 模型權重 | 執行處 |
|---|---:|---|
| Qwen2.5 0.5B Instruct Q4_K_M | 約 491 MB | 瀏覽器 CPU |
| Qwen3 0.6B Q8_0 | 約 639 MB | 瀏覽器 CPU |
| Qwen3 1.7B Q8_0 | 約 1.83 GB | 原生 llama.cpp CPU |
| Qwen3 4B Q4_K_M | 約 2.5 GB | 原生 Ollama |

四項是不同容量與用途的候選，不聲稱有一個適合所有裝置的「最佳模型」。權重不隨 ZIP 附上。套件只附固定版本 wllama runtime 與相容 WASM；所有模型回答仍須核對來源。

`file://` 雙擊課程模式會在下載模型前提醒改用 HTTPS 或本機 HTTP，避免下載後才碰到 worker 限制。手機／平板可正常閱讀與觸控，能否推論則取決於瀏覽器、記憶體及儲存配額。

原生 CPU 起步：

```bash
bash install-ai-models.sh --list
bash install-ai-models.sh --model qwen3-17b --download
# 先依文件安裝官方 llama.cpp，確定 llama-server 可執行
bash run-ai-llamacpp.sh
```

目前 Ollama 官方要求 macOS 14+，Intel x86 為 CPU；舊 macOS 請先查系統／編譯器相容性。詳見 `docs/LOCAL_AI_V8_ZH.md`。尚未在您的 Intel Mac 或逐款行動裝置量測模型速度。

## GitHub Pages 姓名／信箱帳號

未設定雲端服務時，本機學習檔案可填姓名與信箱，保存這台裝置的進度；**不是信箱驗證帳號，也不會跨裝置同步**。

若要跨裝置，站長在自己的 Supabase 建立 Auth 與資料庫、執行 `supabase/001_learning_progress.sql`，再於 `config.js` 填專案 URL 和公開 publishable／anon key。學員註冊、驗證信箱後登入，可同步完成步驟、概念組合與筆記。雲端資料依使用者 ID 隔離，版本衝突保留資料並提示，不以另一裝置的舊內容靜默覆蓋。

本版沒有替您開設 Supabase 或預填憑證，實際服務尚需站長設定與跨裝置驗收。操作姿態及研究工作表仍以裝置保存／匯出為主。完整步驟在 `docs/GITHUB_ACCOUNTS_V8_ZH.md`。

## 整包程式與權重上傳

程式、HTML、課程資料、照片、runtime、SQL 與腳本隨完整 ZIP 提供；模型、外部影片及可選開發工具另取得。GitHub 倉庫建好並完成認證後：

```bash
bash publish-github.sh --repo https://github.com/kuonanhong/macgyver-academy.git --dry-run
bash publish-github.sh --repo https://github.com/kuonanhong/macgyver-academy.git --push
```

更新程式可用：

```bash
bash update-and-upload.sh --repo https://github.com/kuonanhong/macgyver-academy.git
```

腳本先重建與檢查，再推送專案外的隔離副本，不改 Sites 倉庫的 origin。未指定權重備份目的地就不上傳模型；只有明確加上 `--models-remote mycloud:MacGyver/models` 才以 rclone 複製，排除 `.part` 等未完成檔。權重不放進 GitHub Pages，不因上傳就訓練模型。

GitHub Pages 仍須在 Settings → Pages 選 GitHub Actions，並手動執行發布 workflow；本次程式交付不代表替您推送或公開 GitHub 網站。原 Sites 的網址與存取權也不因有了這些腳本而自動變更。

## 語言、平台與升級紀錄

核心課文為繁體中文與英文；另 77 個語言選項需要配置 AI 進行機器翻譯，未逐語言人工校對，不能宣稱全部語言完整。語音依裝置已安裝聲音，GPS 不用來推斷語言。桌機／筆電／手機／平板採響應式版面與鍵盤／觸控控制，尚未逐台實機驗證。

更新前先匯出進度與研究 JSON，備份 `portable/data/`。V7 既有工序不因加入新課而重新編號；不同目錄、瀏覽器與後端帳號仍需自行匯入或使用同一後端。若使用雲端帳號，必須確認已同步，不能把「此裝置已保存」當成雲端保存成功。
