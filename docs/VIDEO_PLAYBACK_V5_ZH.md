# 本機檔案與 YouTube 播放

Google 官方將 YouTube 播放器錯誤 `153` 定義為請求缺少 HTTP `Referer` 或相等的 API 用戶端識別，並建議採用 `strict-origin-when-cross-origin` Referrer-Policy。直接雙擊 `file://` HTML 並不會因為加上 `origin=` 參數就產生真實的 HTTP 網站来源。

本版採用兩條路徑：

- **HTTP／HTTPS 網站**：點擊「載入教學影片」後，直接嵌入 YouTube，使用 `strict-origin-when-cross-origin`，API 的 `origin` 設為實際開啟頁面的 HTTP(S) origin。
- **直接開啟本機 HTML**：點擊後載入已部署的 HTTPS 播放頁 `https://macgyver-public-player.kuonanhong.chatgpt.site/video-player.html?video=影片ID`。由這個真正的 HTTPS 文件嵌入 YouTube，讓瀏覽器送出其實際 HTTP Referer。這是呈現播放器的網頁，沒有代理、下載或重新散布影片。

不會預先載入外部播放器或遠端縮圖。載入按鈕先說明會連線到哪一方；YouTube 的播放鍵仍由觀看者自行按下，沒有自動播放。

## 播放仍可能受限

V6 將播放器移到獨立、公開、無狀態的 HTTPS 網站。這個播放器不要求工程學院或 ChatGPT 帳號，也不含學院帳號、進度、AI API 或私人資料；主要學院的存取權限維持獨立。YouTube 本身仍可能因作者禁止嵌入、年齡／地區限制、瀏覽器擴充套件或網路阻擋而無法播放。

每張 YouTube 卡片從一開始就有「開啟線上播放器」及「在 YouTube 觀看」兩個可見連結。線上播放器可直接匿名開啟；若 YouTube 仍限制內嵌，直接觀看原 YouTube 頁面。播放器回報 `100`、`101`／`150`、`153` 等錯誤時，顯示對應原因；15 秒未收到就緒訊息時提示使用直接連結，不把「載入 iframe」宣稱為成功播放。

本套件的 Python 可攜後端保留 `X-Frame-Options: SAMEORIGIN`。若把它放到 HTTPS 反向代理後再當作本機 HTML 的播放器，跨來源內嵌仍會被阻擋；可直接開啟播放器，或將這些不含帳號資料的播放器靜態檔部署到您管理且允許內嵌的 HTTPS 靜態網站。不要為了播放器解除整個帳號後端的框架保護。

## 訊息與隱私

本機頁面與 HTTPS 播放頁的握手只傳送影片 ID、隨機 channel 及就緒／錯誤狀態。接收端核對來源視窗、origin、channel 及影片 ID；不接受任意網址或任意命令。channel 在 URL fragment 中，不作為 YouTube 參數或 Referer 查詢內容傳出。未讀取、傳送或複製帳號 Cookie、密碼、學習進度、API 金鑰或本機路徑。

`file://` 的 message origin 是不透明的 `null`，無法用一般 HTTPS origin 指定回覆目標。因此僅限父視窗的公開播放器狀態回覆使用 `targetOrigin="*"`，並由來源視窗及每次載入的 channel 再校驗；從本機送往 HTTPS 頁面的訊息則使用精確的 HTTPS origin。這個機制不作為身分驗證，也不提升網站存取權限。

## 驗證範圍

`node tools/test-learning-media.mjs` 驗證直接／本機分流、URL 白名單、明確點擊才連線、實際 origin 參數、來源／origin／channel／ID 偽造訊息拒絕、錯誤 153 顯示及直接開啟退路。測試不連線播放影片；實際播放仍須在目標瀏覽器與可連線的網路下驗證。公開部署與播放器運作是分開的檢查，不把程式測試當作已匿名連線播放的證據。

## 使用自己的 HTTPS 部署

只需修改 `public/academy/config.js` 的 `videoPlayerUrl`，不必修改兩支播放程式：

```js
videoPlayerUrl: 'https://你的網域/video-player.html',
googleMapsEmbedKey: ''
```

執行 `node tools/build-public-player.mjs`，只將 `public-player/dist/` 發布到可匿名存取的 HTTPS 靜態網站，再重建與上傳離線套件。不要公開主要工程學院的後端或帳號資料。產生器僅複製播放器 HTML／JS／CSS、最小入口頁與經過篩選的設定，並從 `data/media.json` 產生核准的 YouTube ID 清單。詳細操作見 `public-player/README_ZH.md`。網址必須是 HTTPS、結尾為 `/video-player.html`，不可包含帳密、query 或 fragment；錯誤設定會回到套件預設 HTTPS 播放頁。每次播放器載入會固定採用當時的目標 origin，後續修改設定不能改變已啟用握手的信任來源。

`config.js` 是公開的瀏覽器設定檔。`googleMapsEmbedKey` 若填入，必須是有 HTTP 網站來源及 Maps Embed API 使用限制的瀏覽器金鑰，所有觀看者都看得到；這不是伺服器祕密金鑰。不要在這裡填入 AI API 金鑰、密碼或存取 token。請只指向自己管理、明確允許匿名載入的播放器部署；不要把主學院的存取限制整體解除。

## 官方依據

查核日期：2026-10-13。

- [YouTube IFrame Player API：onError 與已存在 iframe 的 API 綁定](https://developers.google.com/youtube/iframe_api_reference)
- [YouTube API Services Required Minimum Functionality：API Client Identity and Credentials](https://developers.google.com/youtube/terms/required-minimum-functionality)
- [YouTube Embedded Players and Player Parameters：origin](https://developers.google.com/youtube/player_parameters)
