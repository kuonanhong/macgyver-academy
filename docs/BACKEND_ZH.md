# 帳號、保存、AI 與穩定上傳

此專案提供兩種實際可執行的後端。它們使用相同的學習進度與 AI 介面，但帳號系統與資料庫互相獨立，沒有自動跨站合併。進度 JSON 匯出／匯入可作為移轉方式。

## 1. 已代管的網站

- 使用平台的 ChatGPT 登入與 `getChatGPTUser()`；使用者 ID 是資料擁有者。Email 只供顯示。
- D1 `project_progress` 以 `(user_id, project_id)` 為複合主鍵，保存完成步驟、組合元件、筆記與時間。每個讀寫查詢均由伺服器取得登入 ID，不接受瀏覽器指定使用者 ID。
- `.openai/hosting.json` 必須宣告 `"d1": "DB"`。本專案已由 `npm run db:generate` 產生 `drizzle/0000_icy_wolfpack.sql`；发布時平台執行 migration。不要在 route handler 建表。
- 寫入要求同來源 Origin 與 JSON；請勿跨站直接呼叫受保護 API。
- 登入使用頂層 `<a href="/signin-with-chatgpt?return_to=/" target="_top">`；不要自行實作此平台保留路由。

## 2. Python 可攜版：macOS / Linux / Windows

需要 Python 3.10 以上，沒有額外 Python 套件需求。`portable/public/` 是完整靜態 HTML 與素材；若尚未匯出，伺服器自動改讀原始專案的 `public/academy/`。`--public DIRECTORY` 或 `--root DIRECTORY` 可指定其他靜態目錄。`portable/server.py` 同時提供靜態頁面、帳號、SQLite 儲存與 AI adapter。

macOS / Linux / WSL / Git Bash：

```bash
bash run-local.sh
```

Windows PowerShell：

```powershell
py -3 portable/server.py
```

Windows 也可直接雙擊 `run-local.bat`。`.env` 由 Python 以單純 KEY=value 格式讀取；不執行 shell、不插值 `$()` 或反引號。已設定的系統環境變數優先。

預設開啟 `http://127.0.0.1:8010`；未指定埠且被占用時會往後選可用埠，以終端顯示為準。以本機帳號註冊後，關閉伺服器再重開，進度仍會保留在 `portable/data/macgyver.sqlite3`。密碼至少 12 字元；密碼使用每人隨機 salt 與 PBKDF2-SHA256（600,000 輪），資料庫不保存明文密碼。Session 使用隨機 token，資料庫僅保存 token 的 SHA-256，Cookie 為 HttpOnly、SameSite=Lax、有效 7 天；HTTPS 模式加上 Secure。登出即撤銷目前 session。

本機 Email 為帳號識別字，**此版本沒有 Email 驗證或忘記密碼寄信功能**。這是單一伺服器的本機／自架方案，沒有多副本分散式 session／資料庫同步。預設僅監聽 loopback；不同裝置需連到同一台部署好的伺服器，才能共用帳號進度。

若使用反向代理對外部署，先配置有效 HTTPS 與 `SITE_ORIGIN=https://你的網域`，把代理 upstream 的 `Host` 保留為公開網域。Python server 仍建議只監聽 loopback。不要把 SQLite、`.env` 或 `portable/data/` 放在 `portable/public/`，也不要上傳至 GitHub。SQLite 備份請在停止伺服器後複製資料庫，或使用 SQLite 線上備份 API（WAL 模式下直接只複製主檔可能不完整）。

## 3. API

| 方法 / 路徑 | 請求 | 回應 |
| --- | --- | --- |
| GET `/api/me` | 無 | `{user:{id,name,email}\|null, aiAvailable, authMode}` |
| GET `/api/progress` | 已登入 | `{projects:{[projectId]:{completed,notes,assembly,updatedAt}}}` |
| PUT `/api/progress` | `{projectId,completed:string[],notes:string,assembly:string[],baseUpdatedAt:number\|null}` | 儲存後的單一專案進度；版本衝突 409 |
| POST `/api/tutor` | `{question,context:string,language}` | `{answer,model,generated:true}` |
| POST `/api/translate` | `{texts:string[],language}` | `{translations:string[],generated:true}` |
| POST `/api/register` | `{name,email,password}` | 本機版專用；建立帳號及 Cookie |
| POST `/api/login` | `{email,password}` | 本機版專用；驗證帳號及 Cookie |
| POST `/api/logout` | `{}` | 本機版專用；撤銷 Cookie |

寫入由伺服器自動產生單調遞增的 `updatedAt`（毫秒）。每個專案最多 5,000 個完成 ID、5,000 個組合 ID、20,000 字元筆記，ID 最多 100 字元。重複 ID 自動去除。更新時提供上次讀到的 `baseUpdatedAt`；新紀錄使用 null。若其他裝置已更新，伺服器回傳 `409 {error,current}`，`current` 包含最新的 completed、assembly、notes、updatedAt，舊寫入不會覆蓋新資料。代管版以帶版本條件的原子 UPDATE／INSERT 衝突檢查，可攜版以 SQLite 交易保護。前端可合併完成 ID 與組合 ID 的聯集，保留兩份不同筆記並標記衝突，再以 current.updatedAt 重試一次；若仍有衝突，應提示使用者並保留本機草稿／匯出。

一般狀態碼：未登入 401、來源不符 403、輸入不合法 400、進度版本衝突 409、過大 413、配額 429、AI 未設定 503、模型供應商錯誤 502。前端不得將 503 包裝成已生成的回答。

## 4. 真正的生成式 AI

預設**沒有 API key 或模型權重**。課程可照常閱讀；AI 只有在管理者完成設定後才會啟用。此程式不假裝規則查找是模型推論。

把 `.env.example` 複製成 `.env`（可攜版），配置：

```text
AI_BASE_URL=https://your-compatible-provider.example/v1
AI_API_KEY=在本機填入實際金鑰
AI_MODEL=供應商實際支援的模型名稱
```

代管網站用伺服器環境變數／secret 設定相同三個名稱，勿放進前端或 `.openai/hosting.json`。`AI_BASE_URL` 是不含 `/chat/completions` 的 API base URL；adapter 會附加該路徑。代管版僅接受 HTTPS；可攜版另外允許 loopback HTTP 以連接已安裝的本機 OpenAI-compatible 模型伺服器。範例 `http://127.0.0.1:11434/v1`、`AI_API_KEY=local` 只是本機服務設定格式；你必須自行啟動、選擇並安裝合法可用的模型，程式不會自動下載權重。

AI 題目上限 3,000 字元、脈絡 18,000 字元；模型可看到該次輸入的問題與脈絡，請勿輸入未授權的秘密資料。翻譯每批最多 40 段、合計 18,000 字元。兩者合計每帳號每小時 60 次，35 秒 timeout。不提供管理者金鑰到瀏覽器、不接受前端任意 AI URL、不跟隨上游重新導向。自動翻譯可能有術語誤差，需保留原文查核。

提示詞要求標示依據、假設與未知，並限制軍事、危險製造與未授權資安操作為安全的原理與模擬說明。此為教育產品的生成限制，**不能取代內容審校、工程認證或實際施工審查**。

## 5. GitHub 更新與模型上傳

先在 GitHub 建立你要使用的倉庫；此腳本不會假定或覆蓋 `taichi` 倉庫，也不包含任何 token。請先使用 Git Credential Manager、SSH key，或：

```bash
gh auth login
gh auth setup-git
git config user.name "你的姓名"
git config user.email "你的提交 email"
bash push-updates.sh --repo https://github.com/你的帳號/你的倉庫.git --branch main
```

會新增 `macgyver-upload` 遠端並保留原 `origin`，檢查常見秘密與私人資料、提交本機新增／修改檔案、讀取遠端狀態，再以 HTTP/1.1 傳送。網路失敗最多重試 5 次；提交會保留，可重跑。遠端存在未合併提交時會停止，讓你先檢查與合併，**不使用 `--force`**。腳本無法保證所有秘密都被辨識，也不清除 Git 歷史中的既有秘密；上傳前應檢查差異與模型授權。

大型模型選項：

1. 安裝 Git LFS；腳本遇到模型副檔名或 >=50 MiB 檔案時，以 LFS tracking 處理。GitHub 的儲存與流量額度由你的帳戶方案決定。
2. 在 `models/` 放已取得使用權的權重，設定 rclone 遠端，再執行：

```bash
rclone config
bash push-updates.sh --repo https://github.com/你的帳號/你的倉庫.git --models-remote modelstore:macgyver-models
```

此選項使用 `rclone copy`（不刪除遠端），多次重試及略過已成功檔案，並不保證所有儲存後端都支援單檔位元組級續傳。`models/` 不加入這次 Git staging；若已經手動 staged，腳本會停止，請先檢查並取消 staging。複製會排除常見憑證與資料庫檔案。上傳權重不等於啟動推論服務，仍須用對應的模型 runtime 提供 API。

### GitHub Pages 靜態網站

```bash
bash deploy-static.sh
```

此命令把 `public/academy/` 複製到 `github-pages/`，核對必要資料集，加入 `.nojekyll`，不複製後端帳號或密鑰。可用 `--out 新資料夾` 指定輸出；不會覆寫未經本腳本標記的既有資料夾。重跑時替換的是已標記的生成結果，來源檔保留。

套件含 `.github/workflows/pages.yml`，僅接受手動 `workflow_dispatch`。上傳到你自己的 GitHub 倉庫後，在 Settings → Pages 選 GitHub Actions，再至 Actions → Publish static MacGyver Academy → Run workflow。工作流程組裝靜態檔、上傳 artifact 並發布至該倉庫的 Pages。沒有修改／強推既有 Pages 分支。

**Pages 是純靜態模式**：可瀏覽教材、操作練習、保存本裝置進度與匯出；不提供 Python／D1、跨裝置登入同步或伺服器 AI。需要完整功能時，使用已代管網站或可攜伺服器。GitHub Actions 沒有在本次環境實際執行；倉庫權限與 Pages 設定仍須由倉庫擁有者完成。

## 6. 已做的驗證

`python3 -m unittest discover -s tests -p 'test_*.py' -v` 的 4 組測試驗證：兩個帳號同一專案彼此隔離、重新登入取回進度、登出撤銷、偽造代管身份標頭無效、跨站寫入拒絕、路徑穿越拒絕、短密碼拒絕、未設 AI 的真實 503 回應、AI adapter／配額，以及同專案版本衝突返回 409 且不覆寫、依最新版本合併重試成功。AI 測試以 mock adapter 驗證路由，不代表已連上商用模型。正式供應商費用、實際模型品質與雲端運行仍需設定後再測。
