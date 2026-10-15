# 一鍵上傳、比對雲端與每週股價更新（V13 更新）

> 檔名保留 `UPLOAD_SYNC_V12_ZH.md`，因為網站與介面字典連到這個路徑；內容已更新到 V13。

本文件說明如何用 **一個指令** 把本機套件的新增／修改上傳到 GitHub（`kuonanhong/macgyver-academy`），
如何先「比對」本機新套件與雲端倉庫的差異，以及如何每週自動更新股價與匯率。
模型權重上傳到私人倉庫 `kuonanhong/PRIVATE-MODELS` 的細節見 `docs/AI_MODELS_V12_ZH.md`。

**最簡單：一鍵同時更新兩個倉庫**

```bash
bash upload-all.sh        # = bash macgyver.sh all：網站只傳差異＋刪除多餘檔案，再把新權重分片傳到私人倉庫
```

> 所有腳本只在**你自己的電腦**執行。本套件不含任何 GitHub 密碼或 token，也不會替你按下 push。

---

## 0. 指令總覽（`macgyver.sh`）

| 指令 | 做什麼 |
|---|---|
| `bash upload-all.sh` | **一鍵全部**＝`bash macgyver.sh all`：網站（只傳新增／修改、刪除雲端多餘檔案）＋模型（只傳私人倉庫還沒有的分片） |
| `bash macgyver.sh` | 等於 `deploy`：更新股價匯率 → 重建 → 驗證 → **只上傳新增／修改的檔案，並刪除雲端多餘檔案** |
| `bash macgyver.sh compare` | 只比對網站倉庫，不上傳；列出新增 / 修改 / 刪除 / 相同 |
| `bash macgyver.sh models` | 取得 AI 權重（已存在就驗證；Qwen3-0.6B 可由華佗 ZIP 匯入；其餘官方下載），只上傳私人倉庫沒有的 40 MiB 分片 |
| `bash macgyver.sh models-compare` | 只比對私人倉庫的權重分片，不上傳 |
| `bash macgyver.sh restore-models 資料夾` | 從私人倉庫還原並驗證權重 |
| `bash macgyver.sh stocks` | 每週股價與匯率：只更新並上傳 `markets.json`、`fx.json` 兩個檔 |
| `bash macgyver.sh schedule` | 在這台電腦排程：每週一 09:07 自動執行 `stocks` |
| `bash macgyver.sh unschedule` | 取消本機排程 |
| `bash macgyver.sh doctor` | 檢查 git、Python、Node、SSH 認證、兩個倉庫的讀取與本機已有的模型 |
| `bash macgyver.sh config` | 顯示／修改設定（存在 `~/.macgyver-academy.conf`，不會上傳） |

V13 移除了多餘的 `upload-github-ssh.sh` 與其說明文件（功能由 `macgyver.sh` 與 `tools/sync-v13/models_sync.py` 取代）；
下次 `deploy` 時，雲端上的這些舊檔會被列為「刪除」並移除。`publish-github.sh`（隔離匯出）仍保留，由匯出工具在內部使用。


---

## 1. 第一次設定（Mac；Linux 相同，Windows 請用 Git Bash 或 WSL）

1. 安裝工具：`xcode-select --install`（含 git）。Python 3.10+：`brew install python` 或 conda。
   修改程式後重建需要 Node.js 18+：`brew install node`。只更新資料（股價）不需要 Node。
2. 設定提交者：
   ```bash
   git config --global user.name  "Nan-Hong Kuo"
   git config --global user.email "你的 GitHub 信箱"
   ```
3. 建立 SSH 金鑰並加到 GitHub（只需一次）：
   ```bash
   ssh-keygen -t ed25519 -C "你的 GitHub 信箱"      # 一路 Enter，可設密語
   pbcopy < ~/.ssh/id_ed25519.pub                    # 複製公鑰
   ```
   到 GitHub → **Settings → SSH and GPG keys → New SSH key** 貼上。
4. 測試：`ssh -T git@github.com`。第一次會問主機指紋，請與 GitHub 官方公布值核對
   （Ed25519 為 `SHA256:+DiY3wvvV6TuJJhbpZisF/zLDA0zPMSvHdkr4UvCOqU`，官方頁面：
   https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/githubs-ssh-key-fingerprints ）。
   看到 `Hi kuonanhong! You've successfully authenticated` 即完成。
5. 在解壓後的套件資料夾執行：
   ```bash
   bash macgyver.sh doctor
   ```
   全部通過後就能上傳。預設設定已指向你的兩個倉庫；要改用其他倉庫或分支，執行 `bash macgyver.sh config`。

---

## 2. 比對：本機新套件 vs. 雲端倉庫

```bash
bash macgyver.sh compare
```

輸出範例（2026-10-15 以本 V13 套件唯讀比對 `kuonanhong/macgyver-academy@main`（雲端為 V12，提交 9d32de2）的實際結果）：

```
比較結果 / comparison  (git@github.com:kuonanhong/macgyver-academy.git @ main)
  新增 added    : 289
  修改 modified : 135
  刪除 deleted  : 14
  相同 unchanged: 2,057（不會重新上傳）
  需上傳資料量  : 309.3 MiB（git 另行壓縮）
    + docs/UPGRADE_V13_ZH.md
    + public/academy/structures-paths.js
    + public/academy/data/bridges-buildings-100.csv
    ~ public/academy/app.bundle.js
    - public/academy/data/course-parts/part-0001-45a134bea8a54413.json   （舊分片，已被新分片取代）
    - upload-github-ssh.sh
    - docs/GITHUB_SSH_UPLOAD_ZH.md
```
14 個刪除就是「多餘的舊腳本與舊分片」：12 個被新版取代的課程分片，以及 V13 移除的 `upload-github-ssh.sh` 與其說明文件。
修改最多的是 78 個介面語言檔（新增橋樑與建築收藏等 38 個字串）。

### 比對原理（為什麼可靠）

1. 先依 `tools/export_github.py` 的規則建立「可公開快照」：自動排除模型權重、金鑰、帳號資料庫、
   `owner-private/`（含郵局帳號）與 `featured.json`（由 course-parts 重建）。
2. 把雲端分支淺層下載到套件**外面**的狀態資料夾 `../MacGyver_GitHub_Sync_State/site`（不碰你的套件）。
3. 對每個檔案計算 Git 自己的檔案指紋（blob id）：`sha1("blob <位元組數>\0" + 檔案內容)`，
   與 `git ls-tree` 列出的雲端指紋逐一比較：
   - **新增**：本機有、雲端沒有
   - **修改**：兩邊都有但指紋不同
   - **刪除**：雲端有、新套件已沒有（多餘的舊腳本、舊的 course-parts 分片）
   - **相同**：指紋一致，完全不會重新上傳
4. 完整清單存在 `../MacGyver_GitHub_Sync_State/last-comparison.json`，可用任何文字編輯器打開。

想自己用 git 驗證某一個檔案：
```bash
git hash-object public/academy/app.js                       # 本機指紋
git -C ../MacGyver_GitHub_Sync_State/site ls-tree HEAD public/academy/app.js   # 雲端指紋
```
兩個值相同就代表雲端已是同一版本。

只想比對某些路徑：`bash macgyver.sh compare --only public/academy/data`。

---

## 3. 一鍵上傳（只傳差異）

```bash
bash macgyver.sh            # 或 bash macgyver.sh deploy
```

依序執行：
1. 更新股價與匯率（失敗時保留上週資料，不會中斷）
2. 若有翻譯原稿，編譯 `i18n/<語言>.js`
3. 有 Node 時重建 `app.bundle.js` 與離線資料（內容沒變就跳過）
4. `tools/validate-data.py` 驗證全部選題、逐步課程與步驟數（V13：含橋樑與建築 100 門）；失敗就**不上傳**
5. 比對雲端 → 只把新增／修改寫入、刪除多餘檔案 → 一次 commit → push（失敗自動重試 3 次）

GitHub Pages 通常 1–3 分鐘後更新：https://kuonanhong.github.io/macgyver-academy/

選項：
- 自訂提交訊息：`MESSAGE="新增光學課程" bash macgyver.sh`
- 不刪除雲端任何檔案：`bash macgyver.sh deploy --no-delete`
- 保留雲端的 `CNAME`、`.nojekyll`、`LICENSE`（永遠不刪）

### 保護付費內容（進階）

GitHub Pages 是公開的靜態網站：放在倉庫裡的課程 JSON，懂技術的人都能直接下載。
若要真正保護付費章節，請：
1. 依 `docs/PAYMENTS_V12_ZH.md` 設定 Supabase，並執行 `python3 tools/paywall-v12/upload_protected_content.py` 把付費章節上傳到 Supabase（只有已付款會員能讀取）。
2. `bash macgyver.sh config` 後在 `~/.macgyver-academy.conf` 設 `PROTECT_CONTENT=1`。
之後 `deploy` 只發布網站本體，公開檔中每門課只保留第一節，其餘章節只留標題。

> ⚠️ 這個模式會讓公開倉庫**只剩網站本體**（`public/academy/`、首頁轉址、README、每週股價腳本與 Action）。
> 第一次執行時 `compare` 會列出約 480 個「刪除」：`app/`、`portable/`、`tools/`、`docs/` 等原始碼會從公開倉庫移除，
> 它們仍完整保存在你的電腦與 V13 ZIP。請先 `bash macgyver.sh compare` 看清楚再上傳；Git 歷史中的舊版本仍可被查到，
> 若要徹底移除歷史內容，需另行重建倉庫歷史。

---

## 4. 每週股價與匯率更新

三種方式，可以同時使用：

### A. 雲端自動（建議，電腦關機也會跑）
倉庫內的 `.github/workflows/weekly-markets.yml` 每週一 01:07 UTC（台灣 09:07）執行：
1. GitHub 倉庫 → **Settings → Actions → General → Workflow permissions** 選 **Read and write permissions**。
2. **Actions** 分頁 → 「Weekly market & FX snapshot」→ **Run workflow** 先手動跑一次。
它只會提交 `public/academy/data/markets.json` 與 `fx.json` 兩個檔，Pages 隨後自動更新。

### B. 本機排程
```bash
bash macgyver.sh schedule     # Mac 用 launchd，Linux 用 crontab；每週一 09:07
bash macgyver.sh unschedule   # 取消
```
記錄檔：`~/Library/Logs/macgyver-weekly-stocks.log`。Mac 必須開機且未睡眠。

### C. 手動
```bash
bash macgyver.sh stocks
```

### 資料來源與限制
- 股價：Yahoo Finance chart 端點（非官方、延遲），失敗時改用 Stooq 日線或台灣證交所／櫃買中心開放資料。
- 匯率：open.er-api.com（ExchangeRate-API 開放版），備援 jsDelivr 上的 fawazahmed0/exchange-api。
- 網站顯示「每週延遲快照」；課程頁的「載入即時走勢圖」在學員點擊後才連到 TradingView 顯示即時或延遲報價。
- 腳本會把交易所登記的公司名稱與課程資料比對，不一致的代號列在 `markets.json` 的 `reviewTickers`，網頁也會標示「代號待核對」。請修正 `public/academy/data/vendors.json` 後再上傳。
- 行情只供產業觀察，不構成投資建議。

---

## 5. 常見問題

| 狀況 | 處理 |
|---|---|
| `Permission denied (publickey)` | SSH 金鑰未加到 GitHub，回到第 1 節第 3 步 |
| `push 第 N 次失敗` | 可能有人（或每週 Action）剛更新雲端；直接再執行同一命令，會重新比對後只傳差異 |
| `課程資料驗證失敗，未上傳` | 執行 `python3 tools/validate-data.py` 看錯誤行 |
| `程式已修改但沒有 Node.js 可重建` | `brew install node` 後重跑 |
| 想看會刪掉哪些檔 | 先跑 `bash macgyver.sh compare`，`-` 開頭的就是 |
| 狀態資料夾佔空間 | 可刪除 `../MacGyver_GitHub_Sync_State`，下次會重新下載 |
