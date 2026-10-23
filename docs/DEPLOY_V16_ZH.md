# V16 網頁與跨裝置部署

## 公開免費試讀：GitHub Pages

在完整套件根目錄執行 `bash deploy-static.sh`，將生成的 `github-pages/` 作為網站根目錄。既有 `.github/workflows/pages.yml` 會執行同一個匯出程序；上傳原始碼後，在 GitHub Actions 手動執行 Publish static MacGyver Academy。

這個輸出包含每門課第一節與後續章節標題，不含完整會員課文、帳號資料庫或 owner 私人設定。靜態版可閱讀、探索場景並在裝置保存進度；不會憑前端輸入的帳密產生管理員權限。

GitHub Pages 提供靜態檔案託管。完整帳號、跨裝置保存與伺服器 AI 需要另外部署本套件的 Python 後端。官方說明：https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages

## 完整帳號與 AI：Python 後端加 HTTPS

適用於已有網域與伺服器的操作者。以下網址、服務帳號及路徑都是範例，須替換為實際值；本次沒有建立雲端主機、註冊網域或發布網站。

1. 在伺服器放置完整 V16，例如 `/opt/macgyver/`，使用 Python 3.10+。
2. 將私人 owner 包與私人 `.env` 放在相應位置，帳號資料庫預設位於 `portable/data/`。執行程式的非 root 服務帳號需能寫入此資料夾。
3. 私人 `.env` 填入正確公開來源：

```dotenv
SITE_ORIGIN=https://academy.example.org
COMMERCE_MODE=protected
BILLING_MODE=disabled
```

視需求加入 AI provider 金鑰與模型。`BILLING_MODE=disabled` 不妨礙 owner 閱讀所有課程；本版沒有替你開通金流。正式付費設定另見既有 commerce 文件。

4. 先啟動後端並檢查終端輸出：

```bash
bash run-local.sh --host 127.0.0.1 --port 8010
```

5. 使用 HTTPS 反向代理。`examples/deploy-v16/Caddyfile` 是 Caddy 範例；將網域指向主機並讓代理可使用 80/443，再依 Caddy 官方安裝與服務管理方式啟動。代理轉送到本機 8010，瀏覽者使用公開 HTTPS 網址。官方設定依據：https://caddyserver.com/docs/quick-starts/reverse-proxy
6. Linux 若以 systemd 管理，可依實際服務帳號、Python 路徑與安裝目錄調整 `examples/deploy-v16/macgyver.service`；它不包含私人金鑰。這是設定範本，未在本次環境實際安裝服務或申請 TLS 憑證。

手機、平板、Windows、macOS 與 Linux 以瀏覽器開啟相同 HTTPS 網址；不要把另一台電腦的 `127.0.0.1` 當成可分享網址。Ollama／llama.cpp 推論服務維持伺服器本機存取，不需直接公開給訪客。

部署後以訪客確認第一節、以 owner 確認完整課文，並檢查手機螢幕、登入登出、AI 路線與進度保存。定期備份 `portable/data/`，與公開原始碼分開保管。服務大量同時使用者時，應依實測負載規劃程序、資料庫與推論資源；本次未進行公網壓力測試。

## 內容保護範圍

本版阻擋直接讀取完整課文分片及原始補充講義，只有經授權 API 提供。匯出器驗證資料雜湊、JSON／腳本一致性與付費欄位。但完整原始碼若仍放在公開 GitHub，原始教材可直接下載；要保護教材本身，需另管理私人來源與既有 Git 歷史。上傳器不自動刪除或改寫遠端歷史。
