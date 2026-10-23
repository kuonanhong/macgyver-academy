# V17 一鍵解壓、更新與上傳

把這次提供的 `Install_and_Upload_MacGyver_v17.sh` 與完整包 `MacGyver_Engineering_Academy_v17.zip` 放在同一資料夾，執行：

```bash
bash Install_and_Upload_MacGyver_v17.sh
```

完整包下載不順時，改放 `MacGyver_v17_Alternative_1_of_4.zip` 到 `MacGyver_v17_Alternative_4_of_4.zip` 四個檔案，執行同一命令即可。四包都是標準 ZIP，包含不同檔案，合併解壓至同一個 `MacGyver_Engineering_Academy_v17` 資料夾；不能只下載其中一包。請保留下載檔名。四包齊全時優先使用四包。

發行資料夾裡的獨立 `.sh` 已由打包工具嵌入**同次發行**的 ZIP 大小與 SHA-256，不需再另外下載清單才能執行。程式先核對全部 ZIP，再解壓到暫存資料夾，逐檔核對 `RELEASE_FILES_V17.json`，成功後才放到正式資料夾。缺包、損壞、重複路徑或不安全解壓路徑都會停止，尚未上傳網站。

原始碼內的同名 `.sh` 是可重新打包的模板：尚未解壓的情況，需要同目錄的 `RELEASE_ARCHIVES_V17.json`，或以 `--manifest` 指定。它沒有舊版本的固定校驗值。SHA-256 用來檢查檔案一致性；不是發行者的數位簽章。

## 第一次執行的依賴

macOS、Linux、Windows Git Bash 或 WSL 需要 Python 3.10 以上；上傳還需要 Git 和 SSH。腳本不代替您安裝套件或建立帳戶。已有 Conda 環境可先啟用；也可用 `MACGYVER_PYTHON` 指定 Python 的完整路徑。

請先把 SSH 公開金鑰加到具有此倉庫寫入權限的 GitHub 帳戶，並設定 Git 提交姓名與電子郵件。不要把 SSH 私鑰放在本專案。GitHub 官方步驟：

- [建立 SSH key 並加入 ssh-agent](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)
- [把公開金鑰加入 GitHub](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account)
- [測試 SSH 連線與核對主機指紋](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/testing-your-ssh-connection)

完成設定後可測試：

```bash
ssh -T git@github.com
```

首次連線請依官方文件核對主機指紋。GitHub 顯示驗證成功、但不提供 shell 的訊息時，結束碼 1 是正常行為。若私鑰設有密語，先依官方文件將它載入 ssh-agent；上傳工具使用非互動 SSH，不會在背景收集密碼或自行接受主機指紋。

手機和平板可操作網站；這個 Bash 上傳流程需要具備上述工具的終端環境。

## 常用命令

| 目的 | 命令 |
| --- | --- |
| 校驗、解壓並上傳網站 | `bash Install_and_Upload_MacGyver_v17.sh` |
| 只校驗、解壓，不連 GitHub | `bash Install_and_Upload_MacGyver_v17.sh --extract-only` |
| 解壓後連線比較，不寫入遠端 | `bash Install_and_Upload_MacGyver_v17.sh --dry-run` |
| 同時上傳現有私人文件與權重 | `bash Install_and_Upload_MacGyver_v17.sh --with-assets` |
| 查看選項 | `bash Install_and_Upload_MacGyver_v17.sh --help` |

若已解壓，可在專案內直接執行：

```bash
bash Upload_MacGyver_v17_SSH.sh
```

此直接上傳命令預設處理公開網站；加上 `--with-assets` 才一併處理已存在的 `models/` 與 `local-documents/`。也可搭配 `--skip-models` 或 `--skip-documents` 略過其中一種私人資產。`bash macgyver.sh upload` 與 `bash upload-all.sh` 都指向同一個 V17 工具，接受相同選項。已完整解壓的資料夾會保留您的修改和新增檔案；不會重新覆蓋成壓縮包內容。若您刻意刪掉發行檔案，請直接用 `Upload_MacGyver_v17_SSH.sh`；解壓工具會把缺少的發行檔案視為未完整解壓。

```bash
bash Upload_MacGyver_v17_SSH.sh --with-assets
```

自訂私人資料夾範例，路徑含空白時保留引號：

```bash
bash Install_and_Upload_MacGyver_v17.sh --with-assets \
  --models-dir "/path/to/my models" \
  --documents-dir "/path/to/my documents"
```

## 增量更新與私人資產

公開程式及附件固定送至 `git@github.com:kuonanhong/macgyver-academy.git`。工具比較本地與遠端 Git blob，只提交新增或修改的檔案；相同檔案略過，遠端其他檔案保留。遇到同檔衝突會停止，不用 force push。比較快取位於專案旁的 `MacGyver_v17_SSH_Upload_State`，可用 `--state` 指定另一個專案外的新空資料夾。

現有模型和私人文件固定分流至 `git@github.com:kuonanhong/PRIVATE-MODELS.git`，位置為 `projects/macgyver/v17-assets/`。這個倉庫必須已存在、具備 SSH 權限，且能確認為私人倉庫。若已登入 `gh`，優先讀取明確的 private 欄位；否則使用 GitHub 匿名 API 不可讀取且 SSH 可存取的檢查。網路、權限或可見性不能確認時停止私人資產上傳。

私人檔案使用約 40 MiB 分片；已上傳的內容可重用，中斷後可重跑。遠端原有資產與 V16 的命名空間會保留。自訂私人文件夾即使位於 `docs/` 裡，也會從公開快照排除；金鑰、帳戶資料、常見權重格式與憑證資料夾不會混入公開網站。

**發行 ZIP 沒有附帶巨量模型權重。** 工具只處理您本地已存在的文件及模型，不會因為按上傳就自動下載模型。是否能回覆生成式 AI 問題，仍取決於您設定的本機推論服務或雲端供應商。上傳至私人倉庫也不等於模型已在雲端執行。

網站 Git push 完成後，若倉庫已有 GitHub Actions／Pages 設定，會依該設定執行；工具不會代您建立新的部署設定。請到倉庫 Actions 查看結果。

## 維護者重新打包

合併完成並產生 `docs/VALIDATION_V17.json`（`status: "PASS"`）後，才執行：

```bash
python3 tools/package-v17.py /absolute/path/to/release-v17 --parts
```

輸出包含完整 ZIP、四個 Alternative ZIP、嵌入當次校驗值的獨立 `.sh`、`RELEASE_ARCHIVES_V17.json`、`SHA256SUMS_V17.txt` 與 `PACKAGE_VALIDATION_V17.json`。程式保留 V16 舊工具，不呼叫任何真實 GitHub push；打包時不納入本地權重、登入資料或私人文件。既有可下載課程實驗 ZIP 會保留。

每次改動原始碼後都要重新打包與重新發送整組對應的檔案。不要把新版 ZIP 與上次生成的獨立 `.sh` 混用。
