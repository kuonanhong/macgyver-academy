# 馬蓋先工程學院 V14

V14 新增「隧道與地下工程」100 門深入逐步課程，每門 10 個技術單元、40 個新增步驟，合計新增 4,000 步；雪山、英法與哥達三門原課的既有步驟保留。每單元包含機制、定量算例、驗證與失效診斷，附中英教材、工程檔案、官方來源、地圖與原創示意圖。

首頁先呈現入口，課文、來源及相關資料依路由延後載入。13 個透明互動模型與 6 個 Python 合成資料實驗可離線使用。79 種語言選項依瀏覽器偏好自動選擇；完整原創教材為繁中／英文，其餘全文須由已配置翻譯服務、已載入本機模型或瀏覽器翻譯器完成，介面會顯示完成範圍。

- 啟動：`bash run-local.sh`（Windows 也可用 `run-local.bat`）。
- 重建地下教材：`bash rebuild-underground.sh`，需 Python 3.10+ 與 Node.js 22.13+。
- 檢查差異：`bash upload-all.sh --dry-run --skip-models`。
- 網站與自有權重同步：見 [docs/UPLOAD_AI_V14_ZH.md](docs/UPLOAD_AI_V14_ZH.md)。預設保留遠端未受同步工具管理的檔案；不使用 force push。
- AI：OpenAI 相容、Claude、Gemini、Ollama 或明確載入的瀏覽器本機模型；金鑰與大型權重不包含在交付包。
- 可重建的教材原稿：`tools/underground-v14/inputs/`；完整統計：`public/academy/data/release.json`；檢核：`tools/validate-underground-v14.py`。

本包保留既有應用程式、HTML、離線資產、套件鎖檔與啟動／上傳工具。下方為先前版本功能紀錄；遇有語言、同步或模型行為差異，以 V14 文件為準。實際付費 API、外部 GitHub 推送與手機實機效能需在你的部署環境配置與確認。

---

# 馬蓋先 · MacGyver Engineering Academy

以總工程師的視角，把複雜工程拆為「專案 → 階段 → 工序 → 知識點」。學徒在左側操作，師傅在右側示範；看示範、閱讀原理、操作教具、完成驗收，依學員與專案保存進度。

**V13（2026-10-15）：** 新增「橋樑與建築」100 門逐步課程：96 門新課各 **5 階段 × 8 步 = 40 步**，淡江大橋、明石海峽大橋、舊金山金門大橋、台北 101 四門延伸 40 步且舊步驟 ID 不變。每門附工程檔案（關鍵數據、年代時間軸、規範與標準、代表工程比較）、原創結構架構圖、地圖與歷史、相關公司與股價。全站 2,066 選題中 **710 門逐步課程、20,274 步、45,440 個知識點**、2,028 個公開來源、693 家公司（394 家上市）。收費：每門課只開放**第一節免費**（沒有整門免費的課程），通行證 30 天 NT$299／365 天 NT$2,490，**依觀看者語系推定幣別、乘以最新匯率（12 小時快取）並進位到當地慣用價位**（參考華佗學院做法），伺服器重新計價後才收款。模型：`bash macgyver.sh models` 與華佗學院共用私人倉庫 PRIVATE-MODELS，只傳新分片。一鍵：`bash upload-all.sh`。介面 77 種語言字典已含 V13 新字串。詳見 `docs/UPGRADE_V13_ZH.md`。

**一鍵上傳：** `bash upload-all.sh`（網站＋模型，差異同步；V14預設保留未知遠端檔案）；分開執行：`bash macgyver.sh`（網站）、`bash macgyver.sh models`（模型）；先比對：`bash macgyver.sh compare`、`bash macgyver.sh models-compare`。見 `docs/UPLOAD_SYNC_V12_ZH.md`、`docs/AI_MODELS_V12_ZH.md`、`docs/PAYMENTS_V12_ZH.md`（檔名保留，內容已更新到 V13）。

先開 `public/academy/help.html` 看入口與設定。橋樑與建築課程索引為 `public/academy/data/bridges-buildings-100.csv`；修改課程原稿 `tools/structures-v13/inputs/` 後執行 `bash rebuild-structures.sh`。實際統計見 `public/academy/data/release.json`。原始 V13 的私人收款設定筆記不納入 V14 可攜原始碼交付包。

<details><summary>V12 摘要</summary>

**V12（2026-10-15）：** 新增「光學與精密儀器」101 門逐步課程（99 門新課各 32 步，`asml`、`a405` 延伸且舊步驟 ID 不變），全站 2,066 選題中 614 門逐步課程、16,274 步。每門課只開放**第一節免費**，其餘以學習通行證（30 天 NT$299／365 天 NT$2,490，依觀看地區換算當地幣別）解鎖；會員註冊需帳號、密碼、信箱、手機四項。每門課附相關公司、官方業務連結與每週股價快照（522 家，351 家上市）。介面更簡潔，可存個人主題、版面與語音；首頁輪播 2,066 個不重複專案圖示；介面另有 77 種語言字典（依瀏覽器語言自動切換）。詳見 `docs/UPGRADE_V12_ZH.md`。

光學課程索引為 `public/academy/data/optics-precision-101.csv`。
</details>

<details><summary>V11 摘要</summary>

V11 聚焦資訊與資安及世界工程：資訊與資安 100 門各增加 32 步；另外加入 80 門具名的量子、神經網路／加速器、伺服器、能源與資源工程；新增課程地圖、180 組雙語原創架構圖、16 個資訊算例、8 個能源／資源算例、雙量子位理想模擬器及 12 個 Python 小實驗。參見 `docs/UPGRADE_V11_ZH.md`。
</details>

## 快速開始：直接開啟 HTML

1. **完整解壓 ZIP**，保留所有資料夾，不要只抽出一個 HTML。
2. 雙擊最外層 `index.html`。課程、照片、師傅示範、雙手控制與本機進度不需啟動伺服器。
3. 使用當代 Chrome、Edge、Firefox 或 Safari。影片、外部來源、Google Maps 需要網路。
4. 本機會員帳號（帳號、密碼、信箱、手機）只存在此瀏覽器，密碼以加鹽雜湊保存，可防止同一台裝置上的他人切換你的紀錄；它**不是跨裝置帳號**。請定期匯出 JSON，避免清除瀏覽器資料、改用另一瀏覽器或移動資料夾後遺失紀錄。
5. 手機／平板優先使用 HTTPS 網站。檔案預覽器未必能執行 JavaScript；觸控學習不需要在手機安裝 Python。

離線包已預先建好，不需安裝 npm 套件。修改原始碼或課程後，執行 `bash build-offline.sh` 重建；修改課程原稿後可執行 `bash rebuild-curriculum.sh` 整合與驗證。

`file://` 雙擊模式可學習，但不能可靠建立模型 worker，因此會在下載權重前提示改用 HTTPS 網站或可選本機 HTTP 服務。

## V11 課程與來源

- 20 個工程領域、2,066 筆中英選題；515 門逐步課程、1,551 項領域研究工作表。這是編輯選題，不是官方世界排名。
- 資訊／資安 100 門涵蓋系統、網路、儲存、可靠性、防禦資安、密碼學、軟體驗證、AI、加速器與大規模運算。每門新增四階段／32 步，原有三門的 54 步保持內容與 ID。
- 80 門具名工程涵蓋 12 門量子、15 門神經網路與加速器、9 門伺服器、35 門能源、9 門資源；各 12 步。課程地圖含 17 條主線、35 個分支、先修路徑、狀態與搜尋。
- 新增 100 組資訊與 80 組世界工程架構圖，各有繁中／英文 SVG 及圖示，合計 540 個新增 SVG 檔。計算、圖解與實際量產設計的範圍分別標示。
- 電機與電子 100 門已展開，含 11 個子領域：發電設備、輸電與保護、電網、再生能源、儲能供電、馬達、功率轉換、類比／射頻、PCB、工業介面及跨海直流輸電巨作。98 門新課各 4 階段／24 步；既有 `a203` 變壓器 12→36 步、`a211` HVDC 換流站 24→48 步，舊步驟保持原 ID 與順序。
- 原有半導體 99 門、先進封裝與矽光子 100 門繼續保留，並補強其材料、影像與觀看任務。199 個主題各有繁中／英文原創 SVG 學習圖，共 398 檔；這是 199 個主題的雙語版本，不是 398 種不同工廠剖面。
- 半導體製程總覽與先進封裝深入課仍各有 20 模組／520 步。520 是教學拆解與分支數，不是某廠固定的量產製程數；其餘半導體課程也不是各有 500 道實際工序。
- 每個新增步驟包含目標、操作任務、觀察、失效判讀、驗收、中英知識點、測驗及公開來源。原有課程與步驟 ID 保留。
- 半導體、先進封裝與矽光子專題具有原創主題圖示與架構示意；真實照片明示作者、授權及適用範圍。部分照片與教具跨步驟共用，不將代表照片描述成每步專屬實拍。
- 官方資料與延伸閱讀、照片與授權可依工程領域、專業子領域、引用的逐步課程篩選；引用關係從實際課程／階段／步驟／知識點資料建立，不因同領域就自動算作引用。
- 逐步課程附相近工法的比較、差異與延伸學習，並提供近似代表據點與 Google Maps 座標。研究機構、公司園區可能被多門課共用，不代表每項技術只有該處生產。
- 保留 V10 的 118 張授權真實影像與 48 個不同 YouTube 影片來源，本輪沒有增加實拍或影片。新增架構圖、原理、算例及官方閱讀；影片下的中英重點與觀察問題仍保留，影片共享時說明適用脈絡。
- 影片以原發布者的官方頁或播放器提供，點擊後才連線；不把影片放進 ZIP，也不能繞過 YouTube、發布者、地區、年齡或網路限制。其他語言的頁面重點依已設定翻譯服務呈現，影片字幕仍由原發布者控制；SVG 圖中文字只有繁中／英文。

實際數量以 `public/academy/data/release.json` 為準；步驟數不等於各自具有完整、獨立物理模擬。架構圖、示範和控制是工程概念教具，並非精密 CAD、物理求解器、原廠 SOP 或認證施工程序。詳細範圍見 `docs/PROJECT_SCOPE_ZH.md`。

## 師傅示範、操作與語言

左右手方向鍵、鍵盤與觸控長按、旋轉、升降、抓取／釋放、精調、吸附輔助、撤銷與重置均在工作台提供。按鍵區緊接在工作台下方，工程輔助及下一步狀態保持可見。師傅逐段講解、紅箭頭與語音示範可略過；觀看示範不直接算通過，學徒仍需完成操作證據及驗收。

繁體中文／英文是隨套件提供的核心內容。介面有共 79 個語言選項，另外 77 種依設定的 AI 服務進行機器翻譯；**不是 79 種已完整人工翻譯的教材**。瀏覽器偏好用於選語言，GPS 不用來推斷語言。語音依裝置已安裝聲音，有文字講解備援；其他語言的翻譯與聲音均不保證每台裝置具備。

## 個人工作室、產業資訊與展示

頂部「我的工作室」可選淺色／深色／跟隨系統、舒適／緊湊佈局、講解語言、裝置提供的具名聲音、語速與音高，並試聽或停止。所有課程與選項保留。偏好按目前帳號／本機檔案保存於此瀏覽器，可另匯出／匯入；不宣稱自動跨裝置同步。聲音清單沒有跨平台一致的男女／專業度欄位，因此不杜撰聲音性別。完整說明：`docs/WORKSPACE_V10_ZH.md`。

課程的「從課程走進產業」提供廠商業務、與工法的關聯、官方產品與投資人連結。股價採點擊時查詢：台股使用 TWSE 每日盤後開放資料，**不是逐筆即時行情**；其他市場需後端設定具對外展示授權的 Twelve Data 方案與私有 API key。未連接或資料失效時不填假價格。完整設定：`docs/VENDORS_MARKETS_V10_ZH.md`。

探索頁保留 [Holo-Artisan 肖像博物館](https://kuonanhong.github.io/HoloArtisan_PortraitMuseum/)，加入 [Holo-Artisan 技術展示](https://kuonanhong.github.io/HoloArtisanDemo/)。兩者均按「在此載入展示」才建立 iframe，另可獨立開啟；沒有複製原站內容。需相機等功能或內嵌受限時，使用原站獨立視窗。

## 會員、付款與完成證書

「會員與證書」：每門逐步課程只開放第一節免費（沒有整門免費的課程），通行證 NT$299／30 天、NT$2,490／365 天，依觀看者語系換算當地幣別，均為一次付款、不自動續扣。**本次 Sites owner/demo 與 ZIP 未啟用真實付款。** 不能在 GitHub Pages 的公開 JSON 前只放 JavaScript 鎖，便宣稱課程受保護。

可另外部署 `bash run-commerce.sh --port 8010` 的 Python 後端，搭配同一 HTTPS 網域，讓所有請求經過權限檢查。正式金流需業主自行申請綠界商家、設定收款銀行及私有 MerchantID / HashKey / HashIV；卡號只在綠界收銀台輸入。Webhook 簽章與伺服器查單均通過後才發期限權限，沙盒與正式資料隔離。預設禁用，沒有偷偷收費或自動建立商家。

此後端的完成證書來自伺服器依序記錄的課程測驗；有公開驗證、撤銷狀態、列印／存 PDF，姓名公開需同意。它不是學位、專業執照、監考認證或實體技能驗證。離線進度不能直接換成驗證證書。部署、撥款、退款對帳、價格實驗及限制見 `docs/COMMERCE_V10_ZH.md`；正式條款範本需業主填妥後才能營運。

## GitHub Pages 帳號：本機或可選雲端

GitHub Pages 可以提供登入介面，但驗證信、密碼與雲端資料庫需要外部服務。本版已附 Supabase Auth REST、RLS 資料表與衝突處理；站長設定後，學員可用姓名、信箱、密碼註冊，驗證信箱後登入，下次在另一裝置繼續學習。

1. 建立您自己的 Supabase 專案，執行 `supabase/001_learning_progress.sql`。
2. 設定 Email 驗證、正式 SMTP、Site URL 與精確登入回呼路徑。
3. 在 `public/academy/config.js` 填 `supabaseUrl` 與 **publishable／anon key**，不可放 secret 或 service-role key。
4. 重建離線包並更新 Pages。以兩個不同帳號驗證資料隔離、跨裝置同步與衝突處理。

本套件沒有替您開設 Supabase，也沒有內建私人憑證；尚未完成您服務上的跨裝置實測。未設定時，本機姓名／信箱學習檔案仍可使用。完整說明見 `docs/GITHUB_ACCOUNTS_V8_ZH.md`。

雲端同步保存完成工序、概念組合與筆記；操作中的位置／角度與獨立研究工作表主要保存在目前瀏覽器，使用對應 JSON 匯出搬移。不同服務的帳號不會自動互通。

## 生成式 AI：瀏覽器與原生 CPU 候選

| 模型 | 執行方式 | 權重下載量 |
|---|---|---:|
| Qwen2.5 0.5B Instruct Q4_K_M | 瀏覽器 CPU | 約 491 MB |
| Qwen3 0.6B Q8_0 | 瀏覽器 CPU | 約 639 MB |
| Qwen3 1.7B Q8_0 | 原生 llama.cpp CPU | 約 1.83 GB |
| Qwen3 4B Q4_K_M | 原生 Ollama | 約 2.5 GB |

這是依容量與相容性提供的候選，不宣稱任何模型對所有問題都最好。小模型可能答錯，請核對課程來源。師傅視窗清楚區分教材摘要、瀏覽器生成及已設定服務。

瀏覽器模型必須先同意下載；可看進度、取消、卸載或刪除快取，SHA-256 通過才載入。runtime 隨包附上，版本固定為 wllama 3.8.1；**模型權重沒有包在 ZIP**。手機或平板可能因記憶體、瀏覽器或配額無法載入模型，仍能使用課程。

您的 Intel Mac 可另評估原生 CPU：

```bash
# 只列出，不下載
bash install-ai-models.sh --list

# 明確下載、接續中斷並驗證官方檔案
bash install-ai-models.sh --model qwen3-17b --download

# 先安裝官方 llama.cpp，使 llama-server 可執行
bash run-ai-llamacpp.sh
```

目前 Ollama 官方要求 macOS 14+；Intel x86 使用 CPU。相容系統也可安裝、開啟 Ollama 後執行 `bash run-ai-local.sh --download`；以後不加 `--download` 即可使用既有模型。`--both --download` 可明確下載文字與 Qwen3-VL 2B 視覺模型。Windows 可選 Git Bash／WSL 的 llama.cpp 方式，或原有 PowerShell 啟動檔。

本機 HTTP 網站需 Python 3.10+。`pip` 不能升級 Python；Conda 可用 `conda create -n macgyver python=3.12`，再 `conda activate macgyver`。一般不需 AI 的可選 Python 網站可執行 `bash run-local.sh` 或 `run-local.bat`，預設 8010，占用時另選埠，不會停止舊程式。

實際設定、記憶體估計、CORS 限制、下載來源與原生 CPU 安裝見 `docs/LOCAL_AI_V8_ZH.md`。尚未逐台實測模型推論與速度；雲端 AI 的 `AI_BASE_URL`、`AI_API_KEY`、`AI_MODEL` 應放在後端環境，金鑰不得放進 HTML。

## V8.1 圖片提問與 Gemini

「AI 師傅」可選取、預覽及移除一張 PNG／JPEG／WebP（最多 4 MiB）；按送出才交給所選服務，圖片不寫入對話儲存。小型瀏覽器 CPU 模型只接受文字，圖片需用已設定的 Ollama 視覺或 Gemini 路線。

- 本機文字＋視覺：先啟動 Ollama，再 `bash run-ai-local.sh --both --download`；之後只需 `bash run-ai-local.sh --both`。Qwen3-VL 2B 官方標示約 1.9 GB，CPU 速度依裝置而異。
- Gemini：在後端環境或私人 `.env` 設定 `GEMINI_API_KEY`，再執行 `bash run-ai-gemini.sh`。預設 `gemini-3.5-flash-lite`；可用 `GEMINI_MODEL` 指定官方仍提供的其他型號。每次送出需明確同意提供問題、課程脈絡、近期對話及圖片。
- Sites 代管後端同樣附 Gemini 介接；尚未提供金鑰的服務會保持不可用。GitHub Pages 不會執行 Python，不能把秘密金鑰放到 `config.js`。
- 模型、配額與價格由供應者決定；本次未使用私人金鑰或下載大型權重做正式推論。V14 路線與設定見 `docs/UPLOAD_AI_V14_ZH.md`；早期四路線紀錄見 `docs/AI_ROUTES_V81_ZH.md`。

## 加入自己的教材供 AI 查詢

本機伺服器管理者可把教材放進 `local-documents/` 或專案之外：

```bash
python3 -m pip install -r requirements-documents.txt
bash index-documents.sh --source /完整路徑/教材資料夾
```

PDF 需可選 pypdf，掃描 PDF 需先 OCR；文字、Markdown、CSV、JSON、PPTX、DOCX 使用標準函式庫。中英文關鍵字索引不會訓練模型，也不能理解未擷取的圖片。相關段落、檔名與頁碼提供給已設定的伺服器模型；遠端 AI 會收到那些段落。

索引保存在 `portable/data/knowledge.json`，是該伺服器共用的管理者教材，不是每位學員的私人上傳區。V10 受保護付費模式中，私有文件檢索只提供有效付費會員；免費會員仍可詢問其提供的免費課程脈絡。帳號資料庫在 `portable/data/macgyver.sqlite3`，應另行備份，皆不提交公開 Git。

## 整包 GitHub 推送與更新（V14）

**一鍵：** 在解壓後的資料夾執行 `bash upload-all.sh`。它會先比對本機套件與網站倉庫 `kuonanhong/macgyver-academy`，只上傳新增與修改的檔案，移除工具先前管理且本機已刪除的檔案；遠端其他檔案預設保留；再準備 AI 權重（Qwen3-0.6B 可直接從華佗學院四份 ZIP 匯入），比對私人倉庫 `kuonanhong/PRIVATE-MODELS`，只上傳雲端還沒有的 40 MiB 分片（只動 `projects/macgyver/`，不碰華佗學院的檔案）。

```bash
bash macgyver.sh doctor            # 第一次：檢查 git、Python、SSH、兩個倉庫與本機模型
bash macgyver.sh compare           # 網站：新增 / 修改 / 刪除 / 相同（不上傳）
bash macgyver.sh models-compare    # 模型：已存在 / 可引用 / 需上傳 / 將刪除（不上傳）
bash upload-all.sh                 # 一鍵：網站＋模型
bash macgyver.sh stocks            # 每週股價與匯率（或 bash macgyver.sh schedule 自動排程）
```

GitHub Pages 由私人倉庫發布時，符合 GitHub 方案條件的預設網頁仍可公開觀看；隨頁面發布的教材亦可供訪客取得。模型分片保留在獨立私人倉庫，Pages 不會自動載入它們（要由私人倉庫供應，見 `docs/AI_MODELS_V12_ZH.md` 的 Cloudflare Worker 代理）。SSH 驗證可用 `ssh -T git@github.com` 測試；第一次連線須先核對 GitHub 官方主機指紋。

比對原理、SSH 設定、保護付費內容與每週排程見 `docs/UPLOAD_SYNC_V12_ZH.md`。舊的 `update-and-upload.sh`、`push-updates.sh`（V12）與 `upload-github-ssh.sh`（V13）已移除；`publish-github.sh` 保留為內部匯出工具。

GitHub **Settings → Pages → GitHub Actions**，再手動執行 **Publish static MacGyver Academy** workflow，才會發布網站。`bash deploy-static.sh` 也可產生獨立 `github-pages/` 靜態資料夾。靜態課程可搭配瀏覽器 CPU AI；跨裝置帳號由設定的 Supabase 提供，伺服器 AI 須另設後端。

## 升級與檔案位置

先匯出學習及研究 JSON，並備份舊 `portable/data/`。用同一資料庫路徑或移動資料目錄啟動新 Python 版；不將不同版本的工序強行視為同一製程。直接檔案模式的瀏覽器儲存受路徑影響，匯出／匯入是跨資料夾、瀏覽器、服務搬移的方式。

| 路徑 | 用途 |
|---|---|
| `index.html` | 完整解壓後雙擊使用 |
| `public/academy/` | HTML、CSS、JS、課程資料、照片與 runtime |
| `public/academy/tutor-panel.js` / `ai-client.js` | 問答視窗、CPU 模型下載與推論介接 |
| `public/academy/cloud-sync.js` / `services.js` | 可選雲端帳號、同步與靜態模式銜接 |
| `public/academy/source-library.js` | 分類、子領域與課程反向引用索引 |
| `public/academy/vendor/wllama/` | 固定版 runtime、雜湊與授權；不含模型 |
| `supabase/001_learning_progress.sql` | 學習資料表、RLS 與版本比對函式 |
| `tools/semiconductor-v8/` | 半導體課程原稿與生成程式 |
| `tools/packaging-v9/` | 先進封裝／矽光子 100 門課程原稿、原始引用與媒體 |
| `tools/electronics-v10/` | 電機／電子原稿與 199 個既有主題媒體補充 |
| `tools/computing-v11/` | 資訊／資安與世界工程原稿、來源、審查與 V10 保留證據 |
| `public/academy/learning-map.js` / `learning-map.css` | 課程地圖、分支、先修路徑與搜尋 |
| `public/academy/quantum-lab.js` | 理想雙量子位閘、機率、相位與糾纏模型 |
| `public/academy/assets/labs/v11/` | 12 個標準函式庫 Python 小實驗、假想資料與可下載 ZIP |
| `public/academy/personalization.js` / `membership.js` / `vendors.js` | 個人工作室、會員與產業資訊介面 |
| `public/academy/pricing.js` / `paywall.js` / `checkout.js` | V12 地區定價、第一節免費門禁、PayPal／綠界結帳 |
| `supabase/002_accounts_commerce.sql` / `supabase/functions/` | V12 會員四欄位、訂單、通行證與金流驗證 |
| `tools/optics-v12/` / `tools/integrate-optics-v12.py` | 光學與精密儀器 101 門原稿、建置與整合 |
| `tools/markets-v12/` / `.github/workflows/weekly-markets.yml` | 公司名單合併、每週股價匯率更新 |
| `tools/sync-v12/sync_github.py` | 以 Git blob 指紋比對雲端並只上傳差異 |
| `tools/model-proxy/` | 可選：私人模型倉庫的 Cloudflare Worker 代理 |
| `portable/commerce.py` / `commerce_admin.py` | 可另部署的受保護金流、權限與證書 |
| `run-commerce.sh` / `examples/commerce-*` | 付費後端啟動與設定範本，預設不收款 |
| `tools/model-manifest.json` | 官方模型版本、檔名、大小、雜湊及授權 |
| `portable/server.py` | Python／SQLite／伺服器 AI 可選後端 |
| `app/api/`、`db/`、`drizzle/` | 原 Sites 代管後端 |
| `build-offline.sh` / `rebuild-underground.sh` | 重建延後載入與離線程式；重建地下工程 100 門（V14） |
| `rebuild-structures.sh` | 重建 V13 橋樑與建築（修改舊版內容後須明確更新版本保留基線） |
| `rebuild-curriculum.sh` | 舊版各代課程重播（V12 原包起已無法完整跑完，僅供參考） |
| `install-ai-models.sh` / `run-ai-llamacpp.sh` | 原生 CPU 權重下載與啟動 |
| `run-ai-local.sh` / `.ps1` | Ollama 下載與本機網站啟動 |
| `upload-all.sh` / `macgyver.sh` | V14 差異與分批同步，預設保留未知遠端檔案；比對、每週股價、排程 |
| `tools/sync-v13/models_sync.py` | 私人模型倉庫比對、只傳新分片、還原、從華佗 ZIP 匯入 |
| `tools/structures-v13/` / `tools/integrate-structures-v13.py` | 橋樑與建築 100 門原稿、驗證、產生與整合 |
| `publish-github.sh` | 隔離 GitHub 匯出（由上傳工具內部使用） |
| `public-player/` | 獨立靜態影片播放器 |
| `docs/` | 部署、AI、帳號、內容界線及驗證說明 |

開發代管版需要 Node.js 22.13+ 與 pnpm；依 `package.json`、`pnpm-lock.yaml` 安裝，不把 `node_modules` 放進 ZIP。閱讀預先封裝的網頁不需要它們。原始碼、HTML、課程附件、必要 runtime 及建置腳本皆隨完整套件提供；可選工具、模型權重和外部影片依文件另行取得。

MacGyver 是「馬蓋先」的英文。本獨立教學專案與影視 IP、廠商或工程業主無隸屬或背書關係，第三方素材保留個別授權。


## 大型課程資料的原始碼儲存

Git 保留 `public/academy/data/course-parts/` 的雜湊分段及完整作者原稿；超過單一 Git 物件上限的 `featured.json` 是衍生檔，不再直接追蹤。Node 建置會自動重建它，Python 啟動及離線完整性檢查亦可無 Node 重建。下載 ZIP 已包含完整重建結果，雙擊 HTML 不需額外操作。每段先檢查 SHA-256、大小、課程 ID 與順序後才整合；缺段或損壞時停止，不以空教材替代。
