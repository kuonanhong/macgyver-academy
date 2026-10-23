# V16 一鍵 SSH 差異上傳

完整解壓縮 V16 後，在專案資料夾執行：

```bash
bash Upload_MacGyver_v16_SSH.sh
```

腳本不需要先執行 `git init`、修改 origin 或手動 `git add`。它使用專案外的專用狀態資料夾，不操作你的來源資料夾 Git 歷史。腳本需要與完整 V16 套件放在一起，不是脫離套件的獨立上傳器。

執行順序：

1. 檢查 Git、SSH、Python 3.10+、Git 作者姓名與 email。
2. 對照 `git@github.com:kuonanhong/macgyver-academy.git` 的 `main` 分支，只提交新增和修改的公開原始碼。保留所有遠端其他檔案，不 force push。
3. 若有現成 `models/` 權重，或 `local-documents/` 文件，確認 `PRIVATE-MODELS` 可見性後，將它們分片上傳到 `git@github.com:kuonanhong/PRIVATE-MODELS.git`。不存在的資料夾會略過；不下載或安裝模型。
4. 顯示結果。這是原始碼／私人檔案上傳；發布網站請依目前倉庫 GitHub Actions／Pages 設定操作。

## 常用指令

```bash
# 先比較，不提交／上傳（仍需要 SSH，可建立本地比較快取）
bash Upload_MacGyver_v16_SSH.sh --dry-run

# 只更新網站
bash Upload_MacGyver_v16_SSH.sh --skip-models --skip-documents

# 指定已有的模型及文件；含空白的路徑要加雙引號
bash Upload_MacGyver_v16_SSH.sh --models-dir "$HOME/models" --documents-dir "$HOME/Teaching Documents"

# 模型略過；文件仍可上傳
bash Upload_MacGyver_v16_SSH.sh --skip-models

# 分片批次改為約 40 MiB 一次推送，適合較不穩定的網路
bash Upload_MacGyver_v16_SSH.sh --batch-mib 40

# 還原私人資產，產生 DEST/models/ 與 DEST/documents/；逐片及整檔核對 SHA-256
bash Upload_MacGyver_v16_SSH.sh --restore-assets "$HOME/MacGyver_Restored"

# 查看所有選項
bash Upload_MacGyver_v16_SSH.sh --help
```

指定分支可用 `--branch main`；換用新的專用快取可用 `--state "$HOME/MacGyver_v16_SSH_State"`。狀態資料夾必須在專案之外，不可指向既有手動維護的 Git checkout；工具會拒絕未標記、已有其他檔案的資料夾。預設在 V16 專案旁建立 `MacGyver_v16_SSH_Upload_State/`，請勿在其中手動編輯檔案。另一個上傳程序執行中會拒絕同時操作；異常停止後可重跑，已結束程序的鎖會自動清理。

## SSH 與 Python

先確定本機 SSH key 已加入 GitHub，並且有這兩個倉庫的寫入權限：

```bash
ssh -T git@github.com
git ls-remote git@github.com:kuonanhong/macgyver-academy.git
```

GitHub 的 SSH 認證成功訊息仍可能伴隨非零結束碼。首次連線請正常核對 GitHub 主機指紋；本腳本不關閉主機金鑰檢查。若 key 有密語，先以 `ssh-add` 載入 agent，再執行上傳。`Permission denied (publickey)` 表示 SSH key／帳號授權未完成，反覆重跑無法解決。

設定 Git 作者資訊（使用你要顯示的姓名與 GitHub email）：

```bash
git config --global user.name "你的姓名"
git config --global user.email "你的 GitHub email"
```

腳本優先採用 `MACGYVER_PYTHON`，其次是已啟用的 Conda Python，最後搜尋 `python3`／`python`。例如你原本使用的環境：

```bash
conda activate svm_kernels
python --version
bash Upload_MacGyver_v16_SSH.sh
```

Python 需 3.10 以上。也可用 `MACGYVER_PYTHON="/完整路徑/python" bash Upload_MacGyver_v16_SSH.sh`。已完成建置的 V16 上傳不需 Node、不重新抓行情、不執行安裝器。

## 公開原始碼與私人資產的界線

網站公開原始碼保留原本根目錄加 `public/academy/` 結構，不把子資料夾攤平。舊版程式與已管理的舊分片也不刪除；這是本次「只新增與修改」要求的行為。公開原始碼中的完整教材仍可被下載，登入畫面不能保護已在公開 Git 歷史中的內容。真正受保護的教材須移到授權後端及私有儲存，並處理既有公開歷史；本腳本不改寫或清除歷史。

以下不會作為私人資產上傳，也不會混入公開網站提交：`owner-private/`、`portable/data/`、登入帳號資料庫、`.env`、SSH 私鑰、常見 credentials／secrets 目錄、使用者資料與模型快取。請把要公開的網站教材放在受版本管理的教材來源；把要私下備份的學習文件放在 `local-documents/`。不要把私人文件放進公開 `docs/` 或 `public/`。

PRIVATE-MODELS 必須是 Private。若本機已安裝且登入 `gh`，工具優先查驗它的 `private=true`；否則使用 GitHub 匿名 API 404 加上 SSH 可讀取的檢查。API 逾時、限流、倉庫公開、倉庫不存在或 SSH 無權限時會停止，不將未確認的私有文件送出。只上傳網站可使用 `--skip-models --skip-documents`。

支援的現成模型：`.gguf .safetensors .onnx .bin .pt .pth .ckpt .model .h5 .hdf5 .pb .npy .npz`。同資料夾內可一併上傳 tokenizer/config 等 `.json .txt .md .tiktoken .vocab .merges .yaml .yml`。必須至少存在一個權重檔才處理模型資料夾。官方清單裡已固定的檔名會核對官方大小及 SHA-256；自訂權重可用其他檔名，不要求先加入官方模型清單。

支援的文件：`.txt .md .csv .tsv .json .pdf .docx .pptx .xlsx .odt .ods .odp .html .htm .rtf .tex`。不打包 ZIP、整個家目錄或任意未知副檔名。明顯金鑰、密碼欄位及密碼雜湊會使操作停止；Office/OpenDocument 會檢查壓縮內文。這不是完整 DLP 或 OCR，無法辨識圖片、掃描 PDF、任意自訂密碼格式裡的全部敏感資料，請只選擇確定要上傳的教材／模型資料夾。

## 分片、斷線與還原

私人資產放在 `projects/macgyver/v16-assets/`：

- `assets-manifest.json`：原檔相對路徑、大小、SHA-256、分片清單。
- `parts/<前兩碼>/<SHA-256>.part`：每片最多 40 MiB，依內容定址，相同內容可重用。

預設約 120 MiB 一次提交／推送，最終才更新資產清單。若中斷，重跑同一指令：成功的批次仍留在遠端，新比較可跳過它們；失敗批次的 Git pack 可能重新傳輸，不是位元組級斷點續傳。推送最多重試四次，從不 force。有人同時更新同一分支時可能停止，請確認後重跑。

本地缺少某文件或模型，不會刪除遠端記錄；較早版本分片亦保留。刪除本地檔案不等於刪除私人備份。修改檔案會更新它在清單中的內容，但 Git 歷史仍保存先前版本。不同資料夾裡相同相對檔名會更新同一資產，請使用不同子資料夾區分。

上傳私人文件只是備份／同步；不會自動重新建立 AI 檢索索引，也不會把雲端權重自動載入瀏覽器。使用前須在執行 AI 的主機還原檔案、設定模型與重建文件索引。

## 驗證

本版測試使用本機 bare Git 倉庫，驗證網站新增／修改、未變更不產生提交、保留遠端檔案、預覽不變更遠端、私人檔案隔離、憑證攔截、含空白與中文字路徑、自訂模型、分片中斷續跑及整檔還原。未替使用者執行實際 GitHub push。

```bash
python3 tools/upload-v16/test_upload.py
bash -n Upload_MacGyver_v16_SSH.sh
```

## V16 入口與舊指令相容

`bash macgyver.sh`、`bash macgyver.sh upload`、`bash macgyver.sh deploy`、`bash macgyver.sh all` 與 `bash upload-all.sh` 都轉到本版上傳器。這些入口不重新建置、不更新行情、不下載權重；只上傳已存在的網站與私人資產。`bash macgyver.sh compare` 會自動加上 `--dry-run`；`bash macgyver.sh serve` 開啟本機受保護網站。舊選項 `--skip-data` 可保留，V16 本來就不更新行情。

完整舊 CLI 保存在根目錄 `macgyver-legacy-v15.sh`。`doctor`、`config`、`models`、`models-compare`、`restore-models`、`stocks`、`schedule`、`unschedule` 仍可經由 `macgyver.sh` 呼叫，但會明示使用 V15 設定與行為。舊 `models` 可能下載權重，`stocks` 可能上傳行情，`schedule` 會安裝排程；一般 V16 上傳不需要這些指令。舊設定檔不會改變新上傳器固定的 GitHub 目的地。本次並未替使用者安裝排程或執行這些進階操作。

2026-10-23 修訂：補上 V16 入口，避免舊 `deploy` 再跑只接受 V15 課程數量的驗證；修正 Ollama 啟動器在 Bash 3.2 搭配 `set -u` 時的空陣列展開；統一雲端 AI 的 Python／Conda 選取順序。詳見 `docs/SHELL_LAUNCH_V16_ZH.md`。
