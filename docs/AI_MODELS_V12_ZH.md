# 生成式 AI 模型（V13 更新）：需要哪些權重、如何取得、如何放進私人倉庫、網站如何讀取

> 檔名保留 `AI_MODELS_V12_ZH.md`，因為網站與 77 種語言的介面字典都連到這個路徑；內容已更新到 V13。

學員在課程右側「問師傅」時，網站可以用三種方式產生回答（都會把目前課程、步驟與來源一起放進提示，並提醒以課程與原始來源為準）：

| 方式 | 在哪裡執行 | 需要的權重 | 適合 |
|---|---|---|---|
| **瀏覽器 CPU 模型**（預設） | 學員自己的瀏覽器（wllama 3.8.1／llama.cpp WebAssembly，隨套件附上） | GGUF 小模型，第一次使用時下載、核對 SHA-256 後快取 | GitHub Pages 靜態網站；手機、平板、筆電、桌機 |
| 本機原生模型 | 你的電腦（llama.cpp 或 Ollama） | 較大的 GGUF／Ollama 模型 | 自己的電腦離線、教室主機 |
| 伺服器 AI | `portable/server.py`、Gemini 或其他後端 | 依後端設定 | 自架網站、看圖問答 |

## 1. 這個專案需要哪些模型與權重？

清單、固定版本與 SHA-256 在 `tools/model-manifest.json`（只用 Qwen 官方 Hugging Face 倉庫，Apache-2.0，可合法再散布並需保留授權檔）：

| id | 模型 | 類型 | 下載量 | 建議記憶體 | 用途 |
|---|---|---|---|---|---|
| `qwen25-05b` | Qwen2.5-0.5B-Instruct · Q4_K_M | 瀏覽器 | 約 491 MB | 4 GB | **網站預設**；手機與舊筆電也能跑 |
| `qwen3-06b` | Qwen3-0.6B · Q8_0 | 瀏覽器 | 約 639 MB | 4 GB | 推理較好、稍慢；**與華佗學院使用的是同一個檔案**（SHA-256 `9465e63a…b031`） |
| `qwen3-17b` | Qwen3-1.7B · Q8_0 | 原生 | 約 1.83 GB | 8 GB | 本機 llama.cpp（`bash run-ai-llamacpp.sh`）；華佗學院的 CPU 預設 |
| `qwen3-4b` | Qwen3 4B（Ollama） | 原生 | 約 2.5 GB | 12 GB | 本機 Ollama，較完整的工程問答 |
| `qwen3-vl-2b` | Qwen3-VL 2B（Ollama） | 原生 | 約 1.9 GB | 8 GB | 可看圖的本機模型 |

**GitHub Pages 網站上的學徒問答只需要 `qwen25-05b` 與（可選）`qwen3-06b`。** 預設設定
`MODELS="qwen25-05b qwen3-06b"`，合計約 1.1 GB。

## 2. 取得權重（在你的電腦）

一個指令就會依序處理每個模型（已存在且 SHA-256 正確就略過，中斷後重跑會接續）：

```bash
bash macgyver.sh models
```

- `qwen3-06b`：先找你電腦上已有的**華佗學院模型**——`HuaTuo_v2_Qwen3_CPU_part1of4.zip`～`part4of4.zip`
  （套件上一層資料夾、`~/Downloads`，或 `~/.macgyver-academy.conf` 的 `HUATUO_DIR`），或華佗資料夾內已還原的
  `models/Qwen3-0.6B-Q8_0.gguf`。找到就逐片、整檔核對 SHA-256 後直接匯入，**不必再下載 639 MB**。
- 其他模型：從 Hugging Face 官方倉庫的**固定版本**下載，完成後核對 SHA-256。

只想下載不想上傳：`bash install-ai-models.sh --model qwen25-05b --download --directory models`。
權重放在套件的 `models/`；`.gitignore` 與匯出規則保證它們**不會**進入公開網站倉庫。

> 為什麼不直接附在 ZIP 或由我下載給你：權重約 0.5–2.5 GB，超過對話附件的大小上限；製作本套件的雲端環境也無法連到
> Hugging Face。腳本在你的電腦下載、驗證並上傳，結果與我代為下載相同，而且每個檔案都核對官方 SHA-256。

## 3. 上傳到私人倉庫 `kuonanhong/PRIVATE-MODELS`（只傳新增的部分）

先在 GitHub 確認該倉庫是 **Private**。之後 `bash macgyver.sh models`（或連同網站一起 `bash upload-all.sh`）會：

1. 以 `--filter=blob:none` 淺層取得私人倉庫的檔案清單——**不下載任何權重內容**。
2. 把每個本機模型切成 **40 MiB** 分片（與華佗學院上傳工具相同大小），分片以 SHA-256 命名：
   `projects/macgyver/parts/<前兩碼>/<sha256>.part`，並寫入 `projects/macgyver/weights-manifest.json`
   （每檔大小、每片 SHA-256、整檔 SHA-256）。
3. **比對與只傳差異**：
   - 同一路徑已有相同分片 → 不動；
   - 倉庫其他地方已有完全相同內容（例如華佗學院已上傳的同一個 Qwen3-0.6B 分片）→ 只新增一個指向同一 Git 物件的路徑，**不再傳送資料**；
   - 雲端沒有的分片 → 上傳；每約 400 MiB 推送一批，斷線後重跑同一命令從已完成的批次接續。
4. 新清單與「刪除不再引用的舊分片」放在同一個最後提交，讀取端永遠不會遇到缺片。
5. **只會增刪 `projects/macgyver/` 底下的檔案**；華佗學院的 `projects/huatuo/` 等其他資料夾完全不碰。
   V12 若曾把權重放在倉庫根目錄（`parts/`、`weights-manifest.json`），確認不再需要後可加
   `bash macgyver.sh models --prune-legacy-root` 一併移除。

先看差異、不上傳：

```bash
bash macgyver.sh models-compare
```

輸出會列出：本機模型、雲端已登記的模型、已存在的分片數、可直接引用的相同分片數、需要上傳的分片與 MiB、將刪除的分片。

在另一台電腦還原（逐片、整檔核對 SHA-256）：

```bash
bash macgyver.sh restore-models ~/macgyver-models
```

## 4. 網站（`kuonanhong/macgyver-academy`）如何讀取私人倉庫的權重？

**公開網站不能直接讀取私人倉庫。** 瀏覽器要讀私人倉庫就必須帶 GitHub token，而網頁裡的 token 任何人都看得到，
等於公開你的帳號權限。安全做法有兩種：

### A. 預設：從 Hugging Face 官方固定版本下載（不需設定）
`public/academy/config.js` 的 `modelMirrors` 為空時，學員瀏覽器直接下載官方檔案、核對 SHA-256 後存入瀏覽器快取，之後離線可用。
此時 PRIVATE-MODELS 是你的**備份與教室主機來源**。

### B. 由私人倉庫供應：Cloudflare Worker 代理（token 只存在伺服器端）
`tools/model-proxy/worker.js` 是一個很小的唯讀代理：
1. GitHub → Settings → Developer settings → **Fine-grained token**：只選 PRIVATE-MODELS，權限 **Contents: Read-only**。
2. ```bash
   cd tools/model-proxy && cp wrangler.toml.example wrangler.toml   # 已預設 MODEL_PREFIX = "projects/macgyver/"
   npm i -g wrangler && wrangler login
   wrangler secret put GITHUB_TOKEN      # 貼上剛才的 token（只存在 Cloudflare）
   wrangler deploy
   ```
3. 把得到的網址填進 `public/academy/config.js`：
   ```js
   modelMirrors: ['https://macgyver-models.<你的帳號>.workers.dev/'],
   ```
   然後 `bash macgyver.sh` 上傳網站。
4. 網站讀 `weights-manifest.json`，逐片下載、逐片核對 SHA-256、組回後再核對整檔 SHA-256；任何一步失敗就自動改用 Hugging Face。
   Worker 只回應 `ALLOWED_ORIGINS`（預設 `https://kuonanhong.github.io`），且只能讀 `projects/macgyver/` 底下的清單與分片。

本機或教室主機則直接用私人倉庫：`bash macgyver.sh restore-models models` 還原後，執行 `bash run-ai-llamacpp.sh` 以原生 CPU 回答學徒問題（預設使用 Qwen3-1.7B，需先把 `qwen3-17b` 加進 `MODELS`；只有 0.6B 時可用 `MACGYVER_GGUF=models/Qwen3-0.6B-Q8_0.gguf bash run-ai-llamacpp.sh`）。

> 注意：一旦網站能下載權重，任何訪客都能取得那些權重檔；「私人倉庫」保護的是你的倉庫與帳號，不是讓權重變成秘密。
> 不要上傳你沒有再散布權的權重。

## 5. 主控台語音會跟著觀看者的語言嗎？

會。個人化設定的「語音語言」預設為「自動」時，依瀏覽器語言偏好挑選語音；不使用 GPS 或 IP 定位。
可選的聲音取決於學員裝置已安裝的語音，所以「男聲／女聲／音高／風格」是在該裝置可用語音中挑最接近的。
