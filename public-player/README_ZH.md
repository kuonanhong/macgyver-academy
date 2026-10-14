# 獨立公開影片播放器

這個資料夾可以單獨部署為允許匿名存取的 HTTPS 靜態網站。`dist/` 只有五個檔案：入口頁、播放器 HTML、播放器 JS、CSS 與播放器專用設定。沒有工程學院帳號程式、課程資料庫、進度、Cookie 讀取、AI API、金鑰或模型；不要把主要學院的後端加入這個部署。

預設位置為 `https://macgyver-public-player.kuonanhong.chatgpt.site/video-player.html`。主要工程學院的存取權限獨立維持；公開的範圍只限這個無狀態播放器。YouTube 本身仍可能因作者限制、地區、年齡、網路或瀏覽器政策而無法播放，頁面提供原 YouTube 連結。

## 重建

從完整工程學院原始碼的根目錄執行：

```bash
node tools/build-public-player.mjs
```

這會由 `public/academy/data/media.json` 重新產生已核准影片 ID 清單，更新主要 `config.js` 的清單區塊，並從主要播放器程式產生此處的 `dist/`。只有清單中的 YouTube ID 能啟動播放器；未知 ID 與任意網址不會被載入。這是瀏覽器端使用範圍限制，不是 YouTube 代理或安全身分驗證。

要產生到另外一個已建立的播放器 Site 原始碼目錄：

```bash
node tools/build-public-player.mjs --out /你的路徑/macgyver-public-player
```

工具保留該目錄既有的 `.openai/hosting.json` project_id，設定 `static.directory` 為 `dist`，不更改網站的遠端 audience、不提交、不上傳、不發布。若目錄已有資料庫或物件儲存綁定，或 dist 中有不屬於播放器的檔案，工具會停止，以免把私人服務或未知內容公開。

## 部署自己的網域

只公開此 `dist/`，並讓 `/video-player.html` 可匿名透過 HTTPS 存取。不得要求 ChatGPT 或工程學院登入。主學院 `public/academy/config.js` 的 `videoPlayerUrl` 改成新網址，再重建播放器和離線套件。播放器專用的 `config.js` 只保留影片網址與白名單，不會複製主學院的其他設定。

本機 HTML 載入 HTTPS 播放頁後，才由真正的 HTTPS 文件嵌入 YouTube；未偽造 HTTP Referer。播放器與本機父頁面使用来源視窗、origin、影片 ID 及 channel 驗證公開就緒／錯誤訊息，沒有帳號或敏感資料交換。
