# V8 生成式 AI 師傅：瀏覽器 CPU、原生 CPU 與雲端

問答視窗有三種性質不同的方式：課程知識是既有教材摘要；瀏覽器 CPU 以真實 GGUF 模型產生文字；已設定的服務使用站長的後端模型。沒有下載或未設定時，不會假裝是生成式回答。生成內容需核對附上的官方來源，尤其是數值、容差、製程配方與安全條件。

## 選擇與大小

沒有對所有硬體及問題都最好的模型。本版優先選有官方 GGUF、明確授權及已核對 runtime API 的文字模型；尚未對您的 Mac Intel i9 實測速度或比較答案品質。

| 選项 | 權重下載量 | 用途 | 記憶體規劃估計 |
|---|---:|---|---:|
| Qwen2.5 0.5B Instruct Q4_K_M | 491,400,032 bytes | 瀏覽器先試用；推理能力有限 | 4 GB 以上裝置，關閉其他大型分頁 |
| Qwen3 0.6B Q8_0 | 639,446,688 bytes | 瀏覽器多語文字，停用長思考 | 4 GB 以上裝置 |
| Qwen3 1.7B Q8_0 | 1,834,426,016 bytes | 原生 llama.cpp CPU，避免瀏覽器記憶體上限 | 8 GB 以上，實際依 context 決定 |
| Qwen3 4B Q4_K_M（Ollama） | 約 2.5 GB，依下載 manifest | 較大記憶體桌機／筆電的另一候選 | 12 GB 以上，速度須實測 |

前三项固定官方 repository revision 與 SHA-256；權重皆標示 Apache-2.0。Ollama 選項由 Ollama 管理下載、恢復与 manifest 雜湊。您的 64 GB 記憶體適合先評估原生 1.7B 或 4B，並不等於推論速度保證。已查到官方 Qwen3.5 小模型，但本版未驗證其量化權重與此 runtime 的整合，因此沒有為追求版本號而自動換用。

## 網頁內直接使用 CPU

1. 以最新瀏覽器開啟 HTTPS 網站（包括 GitHub Pages），在師傅視窗選瀏覽器模型。
2. 先看大小、來源、授權與用途，再勾選同意並按下載／載入。沒有同意不會下載權重。
3. 下載有進度與取消功能，完整 SHA-256 通過才載入；已驗證模型保存在該瀏覽器的專用快取。瀏覽器配額不足時可能只能本次使用；清除網站資料也會刪除模型。
4. 載入後才可生成回答。模型在自己的 CPU worker 內執行，本機問句與課程內容不傳給 Hugging Face 或 AI 雲端；下載請求仍會連到模型供應商。網頁 runtime 隨套件附上，不從不固定版本 CDN 載入。
5. 「卸載」釋放模型記憶體；「清除模型快取」刪除該瀏覽器下載的模型。初始化時取消可能要等當前載入動作收尾才釋放記憶體。輸入問題上限 1,200 字元；精簡課程引用保留最多三筆來源。

CPU 設定為 `n_gpu_layers=0`。GitHub Pages 通常沒有跨來源隔離標頭，因此使用單執行緒；有正確隔離標頭時最多使用四執行緒。Safari／Firefox 使用隨附相容 WASM，速度可能較低。手機、平板可使用完整課程與觸控操作，但可能因 RAM、瀏覽器或配額無法載入本機 AI；不能承諾每一台裝置都能運行模型。

**`file://` 雙擊模式會在下載前拒絕瀏覽器模型載入**，避免下載完才遇到 worker 限制。課程仍可直接雙擊使用。需要生成式 AI 時，改開 HTTPS 網站，或依下段啟動本機 HTTP 網站；純 HTML 無法繞過瀏覽器的本機 worker/CORS 規則。

## Mac Intel／Linux／Windows：原生 llama.cpp CPU

Python 須 3.10+；pip 不能升級 Python 本身。Conda 可用：

```bash
conda create -n macgyver python=3.12
conda activate macgyver
```

先列出模型（完全不下載），再明確下載：

```bash
bash install-ai-models.sh --list
bash install-ai-models.sh --model qwen3-17b --download
```

下載保存於 `models/`。中斷後重跑同一指令可接續，完成後驗證固定 SHA-256；不匹配不會安裝或覆寫現有模型。也可選 `qwen25-05b` 或 `qwen3-06b`，並在啟動時用 `MACGYVER_GGUF` 指定檔案。

安裝 `llama.cpp` 官方提供、適合系統的版本，確認 `llama-server --version` 可執行；官方入口：https://github.com/ggml-org/llama.cpp 。macOS 可使用支援您系統版本的 Homebrew `brew install llama.cpp`。CPU 原始碼編譯範例（需 Git、CMake、C++ 編譯器）：

```bash
git clone https://github.com/ggml-org/llama.cpp.git
cd llama.cpp
cmake -B build -DGGML_METAL=OFF -DGGML_CUDA=OFF -DGGML_VULKAN=OFF
cmake --build build --config Release -j 8 --target llama-server
# 將 build/bin 加入 PATH；Windows 的 Release 路徑依產生器不同。
```

取得來源後可自行固定經驗證的 tag/commit；本套件不自動執行下載來的 shell 安裝器。Windows 使用 Git Bash 搭配可執行的 `llama-server.exe`、Python，或在 WSL 安裝 Linux 版本。舊 macOS 是否能編譯，仍取決於可用的 SDK、編譯器與選用 llama.cpp 版本；沒有冒稱支援所有已停止維護的系統。

回到本套件資料夾執行：

```bash
bash run-ai-llamacpp.sh
```

腳本只綁定 `127.0.0.1` 的 AI 埠 8383，建立臨時 API key，再啟動原有 Python 網站。使用終端機顯示的**本機網站**，註冊／登入本機帳號後使用「已設定服務」。結束時只停止本腳本啟動的模型程序，不會刪除資料。埠占用則停止提示，沒有終止其他程式：

```bash
MACGYVER_AI_PORT=8384 MACGYVER_CPU_THREADS=8 bash run-ai-llamacpp.sh
```

本機帳號與 Supabase／ChatGPT Sites 帳號是不同服務；可用進度匯出／匯入轉移。HTTPS GitHub Pages 不能保證直接連入每位學員的 localhost，會受混合內容、私人網路存取與 CORS 限制，因此本版不把未認證的 Ollama 暴露到網際網路。

## Ollama 選項

目前官方要求 **macOS 14 Sonoma 或更新**；Apple M 系列支援 CPU/GPU，Intel x86 是 CPU。若您的 Intel Mac 仍是較舊 macOS，請先核對版本，可改用上面的 llama.cpp CPU 方式，或在 Linux/WSL 運行。

```bash
# 先從官方安裝相容的 Ollama 並開啟它；--download 才會下載模型。
MACGYVER_MODEL=qwen3:4b bash run-ai-local.sh --download
# 後續使用已下載模型：
bash run-ai-local.sh
```

V8.1 改用原生 Ollama 同源路線，由 `OLLAMA_TEXT_MODEL`／`OLLAMA_VISION_MODEL` 決定允許的模型；前端只可選已設定路線。圖片與 Gemini 路線請看 [AI_ROUTES_V81_ZH.md](AI_ROUTES_V81_ZH.md)。雲端 AI 亦需在自己的後端設 `AI_BASE_URL`、`AI_API_KEY`、`AI_MODEL`；瀏覽器不收取或保存供應商私密金鑰。

## 更新、權重備份與驗證範圍

`publish-github.sh` 上傳完整程式但排除模型與學員私有資料。更新工作台後，可用下列一個指令重建離線資料並推送：

```bash
bash update-and-upload.sh --repo https://github.com/kuonanhong/macgyver-academy.git
```

它先檢查路徑與離線建置、預覽公開匯出，再呼叫 `publish-github.sh --push`。程式進入專案外的隔離副本，不改原 Sites 倉庫的 origin，也不隱含改用 Git LFS。您仍須事先建立自己的 GitHub 倉庫並設定 Git 認證。

只有明確指定備份目的地，才會另外使用已設定的 rclone 上傳權重或私人教材；例如：

```bash
bash update-and-upload.sh \
  --repo https://github.com/kuonanhong/macgyver-academy.git \
  --models-remote mycloud:MacGyver/models \
  --documents /完整路徑/私人教材 \
  --documents-remote mycloud:MacGyver/private-documents \
  --index-documents
```

先用 `rclone config` 設定 `mycloud`，並確認目的地存取權。未指定 `--models-remote` 就不上傳權重；不完整的 `*.part`、`*.partial`、`*.tmp`、`*.download`、`*.crdownload` 與 `.incomplete/` 會排除。`rclone copy` 不刪除遠端檔案；任何建置、公開匯出預檢或備份失敗都停止後續推送。`--out` 可指定新的專案外 GitHub 匯出資料夾；`--branch` 可選目的分支。

模型不放進 GitHub Pages 網站，不會因 git push 就訓練或啟動模型。下載更新應使用新 manifest/revision，不默默覆寫舊權重。只上傳您有權再散布的檔案。

隨附 `tools/model-manifest.json`、`public/academy/vendor/wllama/LOCK.json`、runtime 原授權、`tools/vendor-ai-runtime.py`。恢復 runtime 時以固定 npm tarball SHA-512 驗證，並再次比對每個 JS/WASM 檔 SHA-256；不是更新到未固定的 latest。

本版通過：增量 SHA-256 多種資料長度、未同意不連線、取消下載、損毀權重拒絕、CPU 參數、對真實 wllama 3.8.1 API 的轉接契約與模擬回覆、模型 runtime 檔案完整性，以及 Auth／身份切換／衝突測試。**未在本次環境下載數 GB 權重進行真實模型推論，未逐台實測瀏覽器或您的 Intel Mac**；介面整合可用不等於實測效能保證。

官方来源（2026-10-13 查閱）：
- https://github.com/ngxson/wllama
- https://github.ngxson.com/wllama/docs/classes/Wllama.html
- https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct-GGUF
- https://huggingface.co/Qwen/Qwen3-0.6B-GGUF
- https://huggingface.co/Qwen/Qwen3-1.7B-GGUF
- https://huggingface.co/Qwen/Qwen3.5-0.8B
- https://ollama.com/library/qwen3:4b
- https://docs.ollama.com/macos
- https://github.com/ggml-org/llama.cpp/blob/master/docs/build.md
