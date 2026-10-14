# GitHub SSH 逐批上傳與斷線續傳

此文件適用於 Mac、Linux 或 Windows 的 Git Bash／WSL。網站程式與權重分兩個 GitHub repository：網站程式可以用 GitHub Pages 公開示範；權重倉庫另外設為 **Private**。腳本只接受 `git@github.com:OWNER/REPO.git` 形式，不會把 token、SSH 私鑰或權重寫進網站匯出。

## 首次設定

1. 在 GitHub 建立空白網站倉庫與空白私人權重倉庫。若暫時沒有要傳模型，先建立網站倉庫即可。不要在新倉庫勾選 README、License 或 `.gitignore`，可避免首次推送時與隔離匯出的歷史衝突。
2. 在本機安裝 Git、Python 3.10+。確認已有 SSH 金鑰；若尚未建立，可按 GitHub 官方教學產生 ED25519 公鑰，將**公鑰**新增至 GitHub 的 **Settings → SSH and GPG keys**。不要上傳私鑰。
3. 先手動執行 `ssh -T git@github.com`。首次看到主機指紋時，先與 [GitHub 官方公布的 SSH 指紋](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/githubs-ssh-key-fingerprints) 比對。出現 `Hi USERNAME!` 即完成認證；GitHub 不提供 shell，所以此測試通常以狀態碼 1 結束。
4. 在本機設定提交者姓名與信箱：`git config --global user.name "你的 GitHub 名稱"` 及 `git config --global user.email "你的提交信箱"`。

## 上傳程式與選用的模型

在完整解壓的 `MacGyver_Engineering_Academy_v11` 資料夾執行以下指令，將 `OWNER/ACADEMY` 換成**您親自建立的倉庫**：

```bash
bash upload-github-ssh.sh --repo git@github.com:OWNER/ACADEMY.git --dry-run
bash upload-github-ssh.sh --repo git@github.com:OWNER/ACADEMY.git
```

程式使用現有的 `publish-github.sh`、`tools/export_github.py` 建立隔離快照，過濾會員資料、文件索引、API 金鑰、模型與權重，再 SSH 推送。若中途斷線，**重跑同一指令**；未完成提交留在本機，已在 GitHub 的提交會再比對，不強推。這是 Git 提交層級續傳，不能從中斷的封包位元組偏移繼續。網站程式約數百 MiB 的原始檔符合目前的單次 2 GiB push 限制；單一普通 Git 物件仍不得超過 100 MiB。

權重請先確認另一個倉庫為 Private，並核對各模型的散布授權與來源：

```bash
bash upload-github-ssh.sh \
  --weights-repo git@github.com:OWNER/PRIVATE-MODELS.git \
  --models-dir /你的模型資料夾 \
  --weights-private-confirmed --dry-run

bash upload-github-ssh.sh \
  --weights-repo git@github.com:OWNER/PRIVATE-MODELS.git \
  --models-dir /你的模型資料夾 \
  --weights-private-confirmed
```

預設每檔分成 32 MiB 片，每四片推一批；可指定 `--chunk-mib 16`（1–48 MiB）。每片按內容 SHA-256 命名，`weights-manifest.json` 保存相對路徑、完整檔案大小、分片雜湊與最終 SHA-256。程序先推完可驗證的分片，最後才發布 manifest。斷線後重跑：已成功推送的分片不用重新提交；當批 Git 傳輸可能重試整批。預設最多重試 5 次、總權重不超過 4 GiB；超過請分成不同私人倉庫，或選擇為大檔設計的物件儲存與 `rclone`。Git 歷史保存舊版本，模型更新多次會增加倉庫大小。

已在隔離的本機 Git 倉庫，以假想權重測過首批推送中斷、重試、再次執行不重複提交、權重變更及 SHA-256 還原。這項測試沒有使用您的 GitHub SSH 金鑰、未向真實 GitHub 推送，也不代表您網路或帳戶配額已驗收。

本機續傳資料夾預設位於專案旁的 `MacGyver_GitHub_Upload_State/`，包含獨立 Git 工作目錄和分片。**不要在傳完之前刪除它**，也不要指定在網站專案裡。尚未完成的來源下載（例如 `.part`、`.tmp`）不會被選入，符號連結會被拒絕。網站與權重倉庫不得相同。

在另一台電腦上可從私人倉庫經 SSH 還原，腳本會核對每片及完整檔案 SHA-256；使用全新 `--state` 路徑可避免混用兩台電腦的續傳目錄：

```bash
bash upload-github-ssh.sh \
  --weights-repo git@github.com:OWNER/PRIVATE-MODELS.git \
  --restore-to /想要還原模型的資料夾
```

## 開啟網頁 Demo

上傳程式**不等於**啟用 Pages。前往網站程式倉庫 **Settings → Pages → Build and deployment → GitHub Actions**，再於 **Actions** 手動執行套件內的 `Publish static MacGyver Academy` workflow。成功後專案頁通常位於 `https://OWNER.github.io/ACADEMY/`，以 Pages 設定顯示的網址為準。

GitHub Free 可從公開倉庫使用 Pages；私人倉庫使用 Pages 須符合 GitHub Pro／Team／Enterprise 的方案條件。**即使程式倉庫是 Private，發布出來的 Pages 網站預設仍可由任何人觀看，頁面中的 HTML、JS、圖片與教材也可取得。** GitHub Enterprise Cloud 的組織專案站可設定私人 Pages，屬不同的存取控制。私人權重倉庫的分片不會自動提供給 Pages 訪客；GitHub Pages 不支援 Git LFS 權重作為網站素材。若要讓一般訪客使用生成模型，須另行設計合適的授權下載或後端推論，並處理散布授權及容量。

官方依據：[Pages 發布來源及可見性](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)、[Enterprise Cloud 私人 Pages](https://docs.github.com/en/enterprise-cloud@latest/pages/getting-started-with-github-pages/changing-the-visibility-of-your-github-pages-site)、[GitHub 大檔案與倉庫限制](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github)、[SSH 測試](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/testing-your-ssh-connection)。
