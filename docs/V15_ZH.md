# MacGyver Engineering Academy V15：水利與海岸工程

本版以已交付的 V14 為基礎，新增或擴充 100 門水利與海岸逐步課程。三峽、胡佛壩與巴拿馬擴建船閘保留原有步驟，再各加 40 步；其餘 97 項由研究路線圖升級為逐步課程。原 V14 的 807 門課、24,274 步保留；完整 V15 為 904 門逐步課程、28,274 步。完整目錄仍有 2,066 項題目。

每門本次新增 10 個技術單元，每個單元依序包含機制、帶單位算例、驗證及失效診斷，共新增 4,000 步、8,000 個知識點。繁體中文與英文均含正文、練習、問題解釋、假設和來源。工程名稱、公開歷史與來源分開處理；算例數值明示為教學假設，不冒充專案設計值或現場量測。

## 下載與解壓縮

交付檔可選完整的 `MacGyver_Engineering_Academy_v15.zip`，或下載**全部** `MacGyver_Engineering_Academy_v15_part…of….zip`。兩種方式還原相同的專案，擇一即可；分包數量以檔名和 `V15_ARCHIVES.json` 為準。

分包是各自可開啟、內含不同檔案的**獨立 ZIP**。將每一包解壓到同一個新建的目的資料夾，讓它們共同形成 `MacGyver_Engineering_Academy_v15/`。不要替每包另建不同目錄，也不要用 `cat` 或 `copy /b` 串接 ZIP 二進位檔。圖形解壓工具也應每次選擇同一目的資料夾。

macOS／Linux：將所有分包放在同一下載目錄，從該目錄執行：

```bash
mkdir -p macgyver-v15
for part in MacGyver_Engineering_Academy_v15_part*of*.zip; do
  unzip "$part" -d macgyver-v15
done
cd macgyver-v15/MacGyver_Engineering_Academy_v15
```

Windows PowerShell 的對應方式：

```powershell
New-Item -ItemType Directory -Force .\macgyver-v15
Get-ChildItem .\MacGyver_Engineering_Academy_v15_part*of*.zip |
  ForEach-Object { Expand-Archive -LiteralPath $_.FullName -DestinationPath .\macgyver-v15 }
Set-Location .\macgyver-v15\MacGyver_Engineering_Academy_v15
```

完整 ZIP 則直接解壓一次。下載檔的 SHA-256 清單分別為 `MacGyver_Engineering_Academy_v15.zip.sha256` 與 `MacGyver_Engineering_Academy_v15_parts.sha256`；解壓後的根目錄另有 `SHA256SUMS` 和 `RELEASE_FILES_V15.json`。請保留整個目錄，不能只複製 HTML。

macOS 可執行 `shasum -a 256 -c MacGyver_Engineering_Academy_v15.zip.sha256`，Linux 可執行 `sha256sum -c MacGyver_Engineering_Academy_v15.zip.sha256`。分包改用 `_parts.sha256` 清單。Windows 可用 `Get-FileHash 檔名.zip -Algorithm SHA256` 與清單比對。

## 開始使用

完整解壓縮後，開啟根目錄 `index.html` 可閱讀靜態版本。需要本機帳號、API 或助教服務時，在同一資料夾開啟終端機：

```bash
bash run-local.sh
```

若已有 Python 3.10+ 環境可沿用；使用已建立的 Conda 環境時，先執行 `conda activate macgyver`（或自己的環境名稱）。尚無相容 Python 且已安裝 Conda 時，可執行 `conda create -n macgyver python=3.12 -y` 後啟用環境。依終端機顯示的網址開啟，預設從 `http://127.0.0.1:8010` 尋找可用連接埠，不會停止已占用連接埠的程式。

`bash macgyver.sh doctor` 用於檢查 Git／SSH、倉庫及同步環境，不是閱讀教材或啟動本機網站的前提。

Mac Intel、Apple Silicon 與 Linux 使用 Bash；Windows 可用 `run-local.bat`，上傳腳本可用 Git Bash／WSL。修改程式並重建需要 Node.js 22.13+。手機和平板使用部署網址；手機自己的 localhost 並不是電腦的伺服器。介面為響應式，教材閱讀不需要下載大型 AI 模型。

本版修復 `macgyver.sh` 兩項已回報問題：缺少相容 Python 時不再執行空指令；變數後接中文字或全形括號時，使用 `${變數}` 明確界定名稱，避免第 65 行的未綁定變數錯誤。Python 選擇順序為明確指定的 `MACGYVER_PYTHON`、目前 Conda 環境、PATH 的 python3／python。

## 首頁與逐頁載入

首頁 HTML 先顯示標題、導覽和課程入口。應用程式之後取得目錄中繼資料；課程正文、影片／補充教材、工程位置、公司及引用來源，按開啟的課程分別取得。來源總表、世界地圖等大型輔助資料只在需要時載入。

每個資料分片有 SHA-256 和長度檢查。重複請求共用載入工作；網路錯誤可重試。file:// 版本使用對應的傳統 JavaScript 分片，HTTP 版本使用 JSON。這是同一份教材的兩種載入方式，不會在首頁一次匯入全部正文。不要移除 public/academy 下的分片或只複製 index.html。

本次索引在資訊完全相同的情況下，由 4,520,940 bytes 縮為 3,773,201 bytes，減少 16.54%；實際網路壓縮與下載時間仍由部署主機及連線決定。首頁 HTML 為 5,031 bytes，會先顯示入口，再取得索引與所選課程。

要產生可部署的靜態目錄，可執行：

```bash
bash deploy-static.sh --out ../macgyver-v15-static
```

此輸出省略只供教材重建的 `data/featured.json`、`data/course-parts/`，保留網站所有按需 JSON、離線 JavaScript、圖片和教材附件；完整原始碼包仍保留重建輸入。實際驗證輸出為 695,827,360 bytes，符合 [GitHub Pages 的 1 GB 網站大小上限](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits)。此命令只產生目錄；GitHub Actions 發布流程見 README。若需自行改課文，請回到完整原始碼包重建，不在精簡部署目錄編修。

## 100 門課的範圍

| 課程 ID | 數量 | 範圍 |
|---|---:|---|
| three-gorges、b202–b220 | 20 | 世界水壩與水庫 |
| b221–b240 | 20 | 防潮、航運與大壩施工 |
| b241–b260 | 20 | 壩工監測、溢洪與壓力水路 |
| b261–b280 | 20 | 輸配水、河川與都市防洪 |
| b281–b300 | 20 | 海岸、港灣與水資源韌性 |

完整雙語索引：`public/academy/data/water-coastal-100.csv`。從網站「水利與海岸工程」集合或課程地圖進入。每課另有工程檔案、關鍵數值、年代、指南索引、具名比較工程與原創功能架構圖；公開機構／公司連結是學習關聯，不代表承包、合作或背書。

12 種互動模型呈現公式、單位和適用範圍。水錘慢關、非超臨界水躍、不符合深水小振幅假設的波浪、負庫容等輸入會明確拒絕。模型只在相關課程單元顯示，不把任意計算器當成該工程的設計模型。

6 個可執行練習不需第三方 Python 套件：水庫質量平衡、明渠流量、水躍動量、深水規則波能、快速水錘、福祿縮尺。可在集合頁下載，或執行：

```bash
python public/academy/assets/labs/v15/run-water-labs.py --check
python public/academy/assets/labs/v15/run-water-labs.py --output my-results.json
```

## AI 助教與多語系

提供 OpenAI 相容 API、Claude Messages、Gemini、Ollama 本機 CPU，以及使用者明確載入的瀏覽器 CPU 文字模型路線。設定方式沿用 `docs/UPLOAD_AI_V14_ZH.md` 和 `.env.example`。帳號網站權限不等於 API 金鑰；本套件不內附金鑰、付費帳號或大型權重。需要的金鑰留在伺服器環境或私人 `.env`，不放進 HTML／public。

```bash
bash run-ai-cloud.sh
# 或使用已啟動的 Ollama 與已安裝的模型：
bash run-ai-local.sh
```

若尚未安裝 Ollama 所需模型，可明確執行 `bash run-ai-local.sh --download` 下載；一般啟動不會自動下載權重。

要讓本機助教參考新增教材，將文件放在專案外或 `local-documents/`，再執行：

```bash
bash index-documents.sh --source /完整路徑/教材資料夾
```

文字、Markdown、CSV、JSON、DOCX、PPTX 可直接索引；PDF 另需 `python -m pip install -r requirements-documents.txt`，掃描 PDF 須先 OCR。索引會由本機後端自動重載，相關段落與檔名頁碼提供給所選模型；選雲端模型時，這些段落會傳到該服務。這是檢索輔助問答，不是訓練模型。私人文件及索引不會由網站公開上傳流程傳出；公開教學文件則放在準備發布的網站目錄，隨網站更新同步。

提供 79 種可選目標語言（包含繁中、英文），依瀏覽器的語言偏好順序自動選擇，也可自行切換，支援 RTL 顯示。**完整原創教材為繁體中文與英文。** 其餘 77 種語言全文需要配置翻譯服務、載入適用的本機模型，或使用支援的瀏覽器翻譯器；畫面會顯示已完成／部分完成／無服務，不把尚未翻譯的原文標為完成。這不是 79 種已離線翻譯且人工審校的全套教材。

## 上傳本地更新與模型權重

在 V15 根目錄先比較，再按需要執行：

```bash
bash macgyver.sh doctor
bash upload-all.sh --dry-run --skip-models
bash upload-all.sh --skip-models --skip-data
```

第三行會上傳網站更新並保留現有行情資料；省略 `--skip-data` 時，腳本會更新每週股價與匯率。若修改了水利課程作者原稿，須先執行 `bash rebuild-water.sh`；上傳腳本的離線建置不代替作者原稿整合。要同時準備並上傳 AI 權重：

```bash
bash upload-all.sh --models-dir ./models --batch-mib 120
```

網站預設為 `kuonanhong/macgyver-academy`，模型為 `kuonanhong/PRIVATE-MODELS`；請先建立並設定私人模型倉庫。腳本使用已配置的 Git／SSH 認證，私人設定存於使用者目錄。網站同步新增／修改的檔案，移除先前管理後已刪除的檔案及過期產生分片，預設保留其他遠端另加檔案；沒有 force push。`--no-delete` 可停用網站差異同步的刪除，不能與保護課文模式併用。

權重按 40 MiB 分片，預設約 120 MiB 一批提交；已成功提交的分片可在重跑時續用。這是模型倉庫的儲存格式，與前述獨立下載 ZIP 分包不同。模型還原使用下列工具，會核對完整大小與 SHA-256：

```bash
bash macgyver.sh models-compare
bash macgyver.sh restore-models ./restored-models
```

若只要上傳已放入模型目錄的檔案，可在私人設定檔設 `MODELS=''`，避免額外準備 manifest 預設模型。完整權重與其授權由您選擇的官方來源取得；不要將私人文件或 API 金鑰放進公開網站。GitHub Pages 本身只執行靜態前端，雲端助教需另配置後端，瀏覽器本機推論則依裝置記憶體與能力運作。

## 重新產生與驗證

```bash
bash rebuild-water.sh
node tools/test-lazy-v14.mjs
node tools/test-lazy-index-v15.mjs
node tools/test-v15-workbench.mjs
python3 tools/validate-review-snapshots-v15.py
python3 tools/test-rebuild-v15.py
node tools/test-lazy-index-fallback-v15.mjs
node tools/test-water-calculators-v15.mjs
python -m unittest tests.test_macgyver_shell -v
```

`tools/water-v15/inputs/` 是 100 門雙語作者輸入；`build_water.py` 產生四面向步驟，`integrate-water-v15.py` 合併資料，`build-offline.mjs` 重建離線／按需分片。V15 的教材重建入口是 `rebuild-water.sh`；先前版本的重建工具留作來源追溯，不用它們覆寫 V15 成品。

`docs/V15_BASELINE.json` 保存 V14 每門原有階段的摘要雜湊；V15 驗證器逐門核對未變更。驗證結果與實際限制見 `docs/VALIDATION_V15.json`。使用受控 API／Git 測試不等於已替您部署到 GitHub，也不等於每款手機均已實機測試。

工程內容是原創學習任務與假想算例。實際設計、施工、操作或安全判斷仍須使用當地規範、實測邊界和合格專業審查。
