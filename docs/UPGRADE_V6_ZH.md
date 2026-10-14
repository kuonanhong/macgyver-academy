# V6 更新與開啟方式

## 先備份，再解壓

1. 舊版「我的專案」先匯出學習進度 JSON；有使用 Python 後端時，另備份 `portable/data/`。
2. 完整解壓 V6 ZIP，雙擊最外層 `index.html`，不需要啟動 Python、不占用 8000 或 8010。
3. 如瀏覽器把新資料夾視為新儲存區，選擇原學員後匯入進度 JSON。原有 17 門課程的工序 ID 沒有更換。
4. 手機／平板建議使用已部署的 HTTPS 網站；系統檔案預覽器可能不允許執行本機 HTML。

## 影片登入問題

V5 截圖中的登入畫面來自需要 ChatGPT 登入的播放器網站。V6 改用獨立的公開、無帳號播放器：

https://macgyver-public-player.kuonanhong.chatgpt.site/video-player.html

直接開啟本機 `index.html` 後，按課程影片的播放按鈕，頁內會載入這個 HTTPS 播放頁。它只接收已核准的公開影片 ID，沒有學員資料庫、AI 金鑰或學習進度。學院本身的存取權保持原設定。

匿名 HTTP 檢查確認播放器回傳 200 與播放器 HTML，沒有轉往登入頁；這不等於已在您的 Safari／Chrome 完整播放每部影片。YouTube 的年齡、地區、網路、Cookie 或發布者禁用內嵌等限制仍由原服務決定。頁面會保留 YouTube 原影片連結，不規避原服務限制、不另行下載影片。

若自行架站，可把 `public-player/dist/` 放到可匿名存取的 HTTPS 靜態主機，再改 `public/academy/config.js` 的 `videoPlayerUrl`，執行 `bash build-offline.sh`。獨立播放器不需 Python、Node、登入或 API 金鑰。來源和重建工具一併附上。

## 所有工程在哪裡

- 首頁第一個大按鈕：全部 2,000 項工程。
- 首頁第二個大按鈕：全部 37 門逐步課程。
- 首頁依原指定順序列出原 17 項，再列新增 20 門，涵蓋 20 個領域。
- 目錄可搜尋中英名稱、按領域／教材狀態篩選、切換清單／圖片、直接跳頁，並下載完整 CSV。
- 世界地圖依資料顯示全部 37 個課程的代表據點、歷史及課程連結，不再固定只顯示 10 個。

37 門共 1,562 道已編寫學習工序、3,124 個知識點；半導體與先進封裝仍各 520 步。新增 20 門各 12 步，每步有中英目的、操作、觀察、異常判讀、驗收、知識點與來源。

工作台共 52 個專屬任務、1,510 個採用主題模型的步驟，合計 154 種場景。新增課程首步有獨立圖解；其餘依課程、階段及觀察重點選用模型，會明示共用教具，不把它們宣稱為 1,562 個獨立工業數位分身。原有 17 門的課程工序資料與 ID 保持一致。

其餘 1,963 題各有八道依工程領域設計的研究關卡：範圍、來源、系統拆解、取捨、工序依賴、量測、失效／相近技能、總工程師審查。這些是工作表，不冒充已編完的工業製程教材。填入證據後才能勾選完成。

研究關卡記錄按學員及專案儲存在本瀏覽器，使用該工作表的 JSON 匯出／匯入搬移；匯入會合併文字。它與原有可同步的課程筆記分開。2,000 題是代表性選題，未宣称符合某個官方世界前 500／1,000 排名；部分歷史案例早於近百年。

## 修改課程與更新文件／模型

新增 20 門原稿位於 `tools/expansion/{technology,civil,mobility,science}.json`；修改後執行：

```bash
bash rebuild-curriculum.sh
```

此指令整合課程、來源、地點、目錄 CSV、互動覆蓋報告與離線包；會驗證 ID、双語內容、題數、前置關係、來源及所有操作模型。一般只改 JS／CSS 時，執行 `bash build-offline.sh` 即可。

上傳自己的程式、教材與模型範例（目的地需先設定）：

```bash
bash update-and-upload.sh \
  --repo https://github.com/YOUR_NAME/YOUR_REPOSITORY.git \
  --rebuild-curriculum \
  --index-documents \
  --documents /absolute/path/to/teaching-documents \
  --documents-remote myremote:macgyver-documents \
  --models-remote myremote:macgyver-models \
  --message "Update MacGyver lessons and source material"
```

請將示例目的地換為自己的 GitHub 倉庫與 rclone remote。不要把私人教材放進會被 Git 提交的任意子資料夾；使用 `local-documents/` 或專案外目錄。脚本使用 `rclone copy`，不刪除目的地檔案、不強制覆寫 Git 歷史。無上傳需求時不用執行。

模型權重未附於 ZIP；本機 AI 可用 `bash run-ai-local.sh`，Windows 可用 `run-ai-local.ps1`。需要 Python 3.10+ 的是可選帳號／AI 後端；`pip` 不會升級 Python 解譯器。

繁體中文與英文隨套件提供。其他語言選項需配置翻譯服務及裝置語音；沒有相符語音時仍可閱讀逐段文字。本版不宣稱 2,000 題均有完整專屬照片、逐工序影片、量產配方或各國語言人工翻譯。
