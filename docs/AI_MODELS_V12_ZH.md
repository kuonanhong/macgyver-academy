# V12 生成式 AI 模型：需要哪些權重、如何下載、如何放進私人倉庫、網站如何讀取

學員在課程右側「問師傅」時，網站可以用三種方式產生回答：

| 方式 | 在哪裡執行 | 需要的權重 | 適合 |
|---|---|---|---|
| **瀏覽器 CPU 模型**（預設） | 學員自己的瀏覽器（wllama / llama.cpp WebAssembly） | GGUF 小模型，第一次使用時下載並快取 | GitHub Pages 靜態網站、手機／平板／筆電 |
| 本機原生模型 | 你的電腦（llama.cpp 或 Ollama） | 較大的 GGUF／Ollama 模型 | 自己的電腦離線使用、教室主機 |
| 伺服器 AI | `portable/server.py` 或其他後端 | 依後端設定 | 自架網站 |

## 1. 需要哪個模型？

清單與固定版本、SHA-256 都在 `tools/model-manifest.json`（只使用官方來源、Apache-2.0 授權）：

| id | 模型 | 類型 | 下載量 | 建議記憶體 | 用途 |
|---|---|---|---|---|---|
| `qwen25-05b` | Qwen2.5-0.5B-Instruct · Q4_K_M | 瀏覽器 | 約 491 MB | 4 GB | **預設**；手機與舊筆電也能跑，多語、推理有限 |
| `qwen3-06b` | Qwen3-0.6B · Q8_0 | 瀏覽器 | 約 639 MB | 4 GB | 推理稍好，較慢 |
| `qwen3-17b` | Qwen3-1.7B · Q8_0 | 原生 | 約 1.8 GB | 8 GB | 本機 llama.cpp |
| `qwen3-4b` | Qwen3 4B（Ollama） | 原生 | 約 2.5 GB | 12 GB | 本機 Ollama，較完整的工程問答 |
| `qwen3-vl-2b` | Qwen3-VL 2B（Ollama） | 原生 | 約 1.9 GB | 8 GB | 可看圖的本機模型 |

GitHub Pages 網站上的學徒問答只需要 **`qwen25-05b`**（可加 `qwen3-06b`）。
小模型會出錯：網站會把課程內容、步驟與來源一起送進提示，並提醒學員以課程與原始來源為準。

## 2. 下載（在你的電腦）

```bash
bash install-ai-models.sh                         # 只列出可用模型
bash install-ai-models.sh --model qwen25-05b --download --directory models
```
腳本從 Hugging Face 官方倉庫的**固定版本**下載，完成後核對 SHA-256；中斷後重跑會接續。
權重放在套件的 `models/`，`.gitignore` 與匯出規則保證它們**不會**被上傳到公開網站倉庫。

## 3. 上傳到私人倉庫 `kuonanhong/PRIVATE-MODELS`

先在 GitHub 建立該倉庫並確認是 **Private**（已建立可跳過）。之後一個指令：

```bash
bash macgyver.sh models
```

它會：
1. 依 `~/.macgyver-academy.conf` 的 `MODELS="qwen25-05b"` 下載並驗證權重（要多個就寫 `MODELS="qwen25-05b qwen3-06b"`）。
2. 呼叫 `upload-github-ssh.sh --weights-repo git@github.com:kuonanhong/PRIVATE-MODELS.git`：
   - 把每個權重切成 32 MiB 分片（GitHub 單檔上限 100 MB，所以不需要 Git LFS）
   - 寫入 `parts/xx/<sha256>.part` 與 `weights-manifest.json`（schema 1：每檔大小、每片 SHA-256、整檔 SHA-256）
   - 分批 push、失敗自動重試；中斷後重跑同一命令只補上缺的分片
3. **比對與只傳差異**：分片檔名就是內容的 SHA-256（`parts/ab/ab12….part`），同樣內容永遠是同一個檔名；
   Git 只會上傳雲端還沒有的分片，已存在的分片不重傳。換新版模型時只多出新分片，`weights-manifest.json` 會改指向新的分片清單。
   想先看雲端有哪些模型（只下載清單，不下載權重）：
   ```bash
   git clone --depth 1 --filter=blob:none --no-checkout git@github.com:kuonanhong/PRIVATE-MODELS.git /tmp/pm
   git -C /tmp/pm show HEAD:weights-manifest.json | python3 -m json.tool | head -40
   ```
4. 從倉庫還原到另一台電腦：
   ```bash
   bash upload-github-ssh.sh --weights-repo git@github.com:kuonanhong/PRIVATE-MODELS.git --restore-to ~/macgyver-models
   ```
   會重組並逐片、整檔核對 SHA-256。

## 4. 網站如何讀取模型？

**重點：公開網站無法直接讀取私人倉庫。** 瀏覽器要讀私人倉庫就必須帶 GitHub token，
而放進網頁的 token 任何人都看得到，等於把整個帳號權限公開。所以有兩種安全做法：

### A. 預設：直接從 Hugging Face 官方下載（不需要私人倉庫）
`config.js` 的 `modelMirrors` 為空時，學員的瀏覽器從 Hugging Face 固定版本下載，核對 SHA-256 後存進瀏覽器快取，之後離線可用。
這是最簡單、最穩定的方式。PRIVATE-MODELS 此時是你的**備份**。

### B. 由私人倉庫供應：Cloudflare Worker 代理（token 只存在伺服器）
`tools/model-proxy/worker.js` 是一個很小的代理：
1. GitHub → Settings → Developer settings → **Fine-grained token**：只選 PRIVATE-MODELS，權限 **Contents: Read-only**。
2. ```bash
   cd tools/model-proxy && cp wrangler.toml.example wrangler.toml
   npm i -g wrangler && wrangler login
   wrangler secret put GITHUB_TOKEN      # 貼上剛才的 token（只存在 Cloudflare）
   wrangler deploy
   ```
3. 把得到的網址填進 `public/academy/config.js`：
   ```js
   modelMirrors: ['https://macgyver-models.<你的帳號>.workers.dev/'],
   ```
   然後 `bash macgyver.sh` 上傳。
4. 網站讀 `weights-manifest.json`，逐片下載、逐片核對 SHA-256、組回後再核對整檔 SHA-256；任何一步失敗就自動改用 Hugging Face。
   Worker 只回應 `ALLOWED_ORIGINS`（預設 `https://kuonanhong.github.io`）的請求，且只能讀 `weights-manifest.json` 與 `parts/` 底下的檔案。

> 注意：一旦網站能下載權重，任何訪客都能取得那些權重檔；「私人倉庫」保護的是你的倉庫與帳號，不是讓權重變成秘密。
> Qwen 系列為 Apache-2.0，可合法再散布（請保留授權檔）。不要上傳你沒有再散布權的權重。

## 5. 主控台語音會跟著觀看者的語言嗎？

會。個人化設定的「語音語言」預設為「自動」時，網站依瀏覽器的語言偏好（`navigator.languages`，通常就是作業系統語言）
挑選語音；不使用 GPS 或 IP 定位。可選的聲音取決於學員裝置已安裝的語音（Windows、macOS、iOS、Android、Chrome 各不同），
所以「男聲／女聲／音高／專業風格」是**在該裝置可用的語音中**挑最接近的；若裝置沒有男聲，會以音高近似並在設定中標示「近似」。
