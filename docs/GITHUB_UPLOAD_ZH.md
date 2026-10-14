# 將完整程式上傳 GitHub，再發布 github.io

「程式碼倉庫」和「公開網站」是兩件事。`git push` 會把版本提交送到 GitHub 倉庫；GitHub Pages 則把 HTML、CSS、JavaScript 變成別人可瀏覽的網站。本套件把這兩個動作分開，避免備份程式時順便公開網站。

## 一、先準備一個空白倉庫

1. 登入 GitHub，建立自己的空白 repository，例如 `kuonanhong/macgyver-academy`。這只是範例名稱；本套件沒有替你建立這個倉庫。
2. 新倉庫先不要加入 README、`.gitignore` 或 license，避免初次提交歷史不同。若要保留程式私密，選 Private；GitHub Free 的 Pages 通常使用 Public 倉庫，私有倉庫是否可用 Pages 依方案而定。
3. 安裝 Git。macOS 可用終端機執行 `git --version`，依系統提示安裝命令列工具。Windows 可使用 Git Bash 或 WSL；Linux 使用發行版套件管理器。
4. 上傳腳本需要 Python 3.10+；若修改了網頁原始碼並需重建離線套件，另需 Node.js 18+。完整 ZIP 已附離線檔，單純雙擊 `index.html` 不需要上述工具。Python 是獨立程式，不能用 `pip install python` 升級直譯器。

建議用 GitHub CLI 的瀏覽器登入：

```bash
gh auth login
gh auth setup-git
git config --global user.name "你的姓名"
git config --global user.email "你的 GitHub 提交 email"
```

`gh` 是另外安裝的 GitHub CLI。如果沒有 `gh`，可用 Git Credential Manager 或 SSH 金鑰。HTTPS 的 Git 操作不能用 GitHub 網站密碼；若採 personal access token，交給認證提示／憑證管理器，不要寫進網址、HTML、腳本或傳給聊天視窗。推送含 `.github/workflows/` 的倉庫需要相應的 workflow 寫入權限；認證不足時依 GitHub 提示調整。

## 二、完整解壓縮，在套件根目錄執行

把終端機切到同時包含 `index.html` 和 `publish-github.sh` 的資料夾。macOS 可先輸入 `cd `，再把解壓縮後的資料夾拖入終端機，按 Enter。Windows 使用 Git Bash，並確定 Git 和 Python 在 PATH 裡。

先預覽：

```bash
bash publish-github.sh --repo https://github.com/kuonanhong/macgyver-academy.git --dry-run
```

確認網址為自己的倉庫、清單全是要上傳的公開原始碼後，再執行：

```bash
bash publish-github.sh --repo https://github.com/kuonanhong/macgyver-academy.git --push
```

腳本會在原專案旁建立 `<原資料夾名稱>-github`，複製這個版本的公開程式和教材，再在該獨立資料夾建立 Git、提交並推送 `main`。原專案的 Git 歷史、Sites 的 `origin` 和原始檔案不會被換成 GitHub 倉庫；需要時只會重新產生離線 bundle。不要把 ZIP 本身當作網站推送；腳本上傳的是解壓後可瀏覽、可比較版本的程式。

如果要先取得可檢查的複本：

```bash
bash publish-github.sh --repo https://github.com/kuonanhong/macgyver-academy.git --out ../macgyver-github --export
bash publish-github.sh --repo https://github.com/kuonanhong/macgyver-academy.git --out ../macgyver-github --push
```

`--dry-run` 完全不修改檔案、不建立 Git、不連線。`--export` 只產生複本；`--push` 才提交與上傳。預設亦為 dry run。自訂分支可加 `--branch main`；提交說明可加 `--message "補充工程課程"`。更換 `--out` 代表建立新的提交歷史，因此日後更新請保留並重用同一個輸出目錄。

### 上傳範圍

| 包含 | 排除 |
|---|---|
| HTML、CSS、JS、課程資料、授權照片、原始碼、教學文件、測試、Bash、可選 Python 後端、套件鎖檔、Pages workflow | 既有 `.git` 歷史、Sites 專案 ID、密碼／token、私人教材 `local-documents/`、學員帳號資料庫、AI 私人索引、模型權重、`node_modules`、執行快取 |

腳本會列出**實際將上傳的每個檔案**，掃描常見憑證格式，並拒絕達 100 MiB 的普通 Git 檔案。這不是能辨識所有秘密的自動工具；仍需檢查新增的公開 `docs/`、課程 JSON、照片是否可公開。個人 Google Maps 瀏覽器金鑰即使可公開，也應先在 Google Cloud 設定 referrer/API 限制。

大型模型不要塞入這個 GitHub 快照。可用原本的 `update-and-upload.sh --models-remote remote:path` 和已設定的 rclone 另行備份，或自行管理 Git LFS；模型授權與儲存額度需自行確認。此新腳本會排除模型權重，不會替你下載或訓練模型。

## 三、啟用 github.io 網站

1. 在 GitHub 倉庫的 **Settings → Pages → Build and deployment → Source**，選 **GitHub Actions**。
2. 打開 **Actions → Publish static MacGyver Academy → Run workflow**，選 `main` 並執行。
3. 成功後到 Settings → Pages 取得實際網站連結。若倉庫是 `kuonanhong/macgyver-academy`，一般專案網址是 `https://kuonanhong.github.io/macgyver-academy/`，不會取代原本的 `/taichi/`。

workflow 執行 `deploy-static.sh`，只把 `public/academy/` 組成 `github-pages/` 後上傳。`index.html` 放在發布成品的根目錄，並有 `.nojekyll`；圖片、樣式和資料使用相對路徑，可在 `/macgyver-academy/` 子路徑工作。**整個原始碼倉庫不會當成 Pages artifact 發布**。但若倉庫選 Public，任何人仍可直接查看該公開倉庫的原始碼。

工作流程使用 `workflow_dispatch`：每次 `git push` 不會自動發布，確認內容後再按 **Run workflow**。GitHub 顯示完成前網址可能尚未更新。若 organisation 或 repository 限制 Actions／Pages，需在 GitHub 設定允許；腳本不會更改帳號方案或權限。

## 四、日後更新

在**原始解壓縮專案**修改課程或程式後，重跑相同的 `--dry-run` 和 `--push` 指令。若修改 `tools/` 的課程原稿，先執行：

```bash
bash rebuild-curriculum.sh
bash publish-github.sh --repo https://github.com/kuonanhong/macgyver-academy.git --dry-run
bash publish-github.sh --repo https://github.com/kuonanhong/macgyver-academy.git --push
```

`--push` 會在需要時重建離線 bundle。請不要直接修改 `-github` 生成資料夾；工具發現手動修改或陌生檔案會停止，避免覆寫。先把修改搬回原始專案、備份輸出資料夾，再決定如何整理。

### 遠端已有檔案，或出現 non-fast-forward

腳本不會 force push。若 GitHub 上已有不同的初始 README，最簡單是改用新的空白倉庫並指定新的 `--out`。若遠端是別人的更新，先由 Git 使用者在輸出倉庫中檢查、fetch、合併並解決衝突，不要隨便刪除遠端歷史。手動改動後請先保留備份；若輸出快照清單與檔案不一致，後續自動同步將停止，由一般 Git 工作流程接續管理即可。

### Repository not found／authentication failed

確認 `--repo` 拼字、倉庫已建立、登入的 GitHub 帳號具有寫入權限。可用 `gh auth status` 檢查登入狀態。不必把 token 放入遠端 URL。網路失敗時本地提交仍保留，修正認證／網路後重跑即可。

## 五、兩種網站服務的差別

| 項目 | `*.chatgpt.site` 的學院 | GitHub Pages `*.github.io` |
|---|---|---|
| 託管來源 | ChatGPT Sites 建立與部署的網站；是獨立網址，不是聊天記錄 | GitHub repository 的靜態檔案 |
| 是否公開 | 由 Sites 的 audience 設定決定，網址本身不能證明公開；目前學院仍依既有存取設定 | 一般 Pages 發布後公開；企業方案可能有額外存取控制 |
| Git push | 由 Sites 工具管理自己的來源倉庫 | 推送到自己指定的 GitHub 倉庫 |
| HTML／CSS／JS、課程、工作台、影片連結 | 支援 | 支援 |
| 學習進度 | 依完整站的登入及後端設定 | 姓名／信箱本機檔案可保存進度；設定 Supabase Auth 與隨附 SQL 後可跨裝置登入同步，見 GITHUB_ACCOUNTS_V8_ZH.md |
| 生成式 AI | 可選瀏覽器 CPU，或設定後端服務／Gemini 金鑰 | 可選瀏覽器 CPU；Pages 本身不執行 Python、Ollama 或秘密金鑰後端，不會因 git push 自動取得雲端 AI |

從 ChatGPT 建站並不表示網站每次回答都在呼叫 ChatGPT，也不表示每位訪客都能直接使用你的模型額度。Google Maps／YouTube 仍由第三方提供；影片所有者關閉嵌入、年齡／地區限制或 YouTube 登入要求，不會因搬到 GitHub 而消失。

## 官方參考（2026-10-13 查核）

- [GitHub Pages 的功能與網址](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages)
- [使用自訂 GitHub Actions 工作流程發布 Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)
- [GitHub 命令列認證：HTTPS、CLI、SSH](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/about-authentication-to-github)
- [大型檔案與 GitHub 的限制](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github)
