# V10 個人工作室與 Holo Artisan 展示

頂部滑桿圖示開啟「我的工作室」。淺色、深色、跟隨系統，以及舒適／緊湊佈局，皆保留原有課程、來源、地圖、工作台和 AI 選項。桌面、平板、手機使用相同響應式頁面；小螢幕透過左上角選單進入完整導覽。

設定依目前會員 ID 或本機學習檔案分開保存在此瀏覽器，不宣稱自動跨裝置同步。匯出／匯入設定可搬移到另一部裝置；輸出只有外觀與語音偏好，不含個資、登入資料、付費狀態或學習紀錄。無法使用瀏覽器儲存空間時，當次設定仍有效並提示備份。

## 講解語言與聲音

V9 已將手動選擇的語言或瀏覽器語言偏好傳給師傅講解控制器；不是使用 GPS、IP 或國家猜測。非核心語言必須由已設定的翻譯服務準備講解內容，且裝置提供相符語音，才能發聲；缺少其中一項就保留文字、由學員按下一段。

V10 允許選擇「跟隨頁面／瀏覽器」或獨立講解語言、具名聲音、語速 0.6–1.4 與音高 0.6–1.4。控制器先取得該語言的文字再選語音；不會用外語聲音硬讀未翻譯的原文。試聽、清楚慢講／自然／快速複習預設、停止按鈕皆由使用者操作，不會自動播放。新的設定在下一段講解生效。

瀏覽器 `SpeechSynthesisVoice` 提供 `name`、`lang`、`voiceURI`、`localService` 等欄位，沒有一致的「男性／女性／專業性」欄位。網站因此呈現裝置提供的真實聲音名稱供試聽，不自行推測性別或保證聲線。音高改變也不等於變更性別。專業度取決於講解內容，不是瀏覽器聲線標籤。網路語音可能把文字交給系統提供的語音服務；選單會標示裝置語音／網路語音。

參考：

- Web Speech API 規範：https://webaudio.github.io/web-speech-api/#speechsynthesisvoice
- MDN `getVoices()`：https://developer.mozilla.org/en-US/docs/Web/API/SpeechSynthesis/getVoices
- MDN 語言設定：https://developer.mozilla.org/en-US/docs/Web/API/SpeechSynthesisUtterance/lang

## Holo Artisan

「探索工程」包含兩個獨立創作的展示分頁：

- 肖像博物館：https://kuonanhong.github.io/HoloArtisan_PortraitMuseum/
- 技術展示：https://kuonanhong.github.io/HoloArtisanDemo/

兩個原頁在 2026-10-14 取得 HTTP 200；HTML 標題分別為 `Holo-Artisan · The Living Portrait Museum` 和 `H.A.I – Holo-Artisan Intelligence`。這僅確認頁面可取得，不能保證每個瀏覽器的內嵌、媒體及裝置功能都能運作。

預設不建立 iframe，也不向外部網站發出展示請求。點「在此載入展示」後才建立受限的 iframe；切換展示分頁、關閉預覽或離開探索頁會移除預覽。另保留「獨立視窗開啟」，供嵌入被阻擋、畫面空白或需要相機等裝置功能時使用。原站內容及語言保持原樣，不抄錄、重新發布或暗示已轉授權。

## 維護介面

`personalization.js` 匯出 `createPersonalization(options)`、`showcaseMarkup({zh})`、`bindShowcase(root,{onRendered})`。

個人工作室的主要 methods：`syncProfile()`、`open()`、`getNarrationLanguage(pageLanguage)`、`getSpeechOptions(spokenLanguage)`、`update(preferences)`、`destroy()`。初始化時提供 `getProfileId`、`getProfileName`、`getLanguage`；開啟設定前可用 `onOpen` 停止講解，`onRendered` 可讓既有翻譯服務處理設定介面。這些函式本身不修改登入狀態或課程進度。

`mentor-guide.js` 接收 `getSpeechOptions(language)` callback，在各段講解重新讀取指定聲音、語速和音高。`language` 必須傳入 `getNarrationLanguage(resolvedLanguage)`，確保文字翻譯與實際講解語言一致。

檢查：`node tools/test-personalization-v10.mjs`、`node tools/test-mentor-guide.mjs`。這些是邏輯、語音控制器替身、CSS 與色彩對比檢查；並不代表實機聲音或第三方頁面已完成跨瀏覽器驗證。
