# V3 更新與操作

## 保留您已有的進度

更新前在舊版「我的工程進度」匯出 JSON，並備份原本的 `portable/data/`。
請將新版解壓到**另一個資料夾**，用下列方式連接原本資料庫：

```bash
bash run-local.sh --database /完整路徑/舊版/portable/data/macgyver.sqlite3
```

請把例子的路徑換成您的實際路徑。帳號與已完成工序使用相同 ID，V2 → V3 不需重新驗收已完成工序。瀏覽器的姿態／練習暫存仍按帳號與裝置儲存；新任務類型的狀態不能解讀成實際工程製造紀錄。

新版預設仍從 8010 找可用埠，不終止 8000 的舊程式。瀏覽器暫存按 origin（協定、主機、埠）區分；換埠時請登入同一後端帳號或匯入進度 JSON。直接雙擊 HTML（file://）無法使用帳號與讀取 JSON 課程，請由啟動腳本提供 HTTP。

## 鍵盤與觸控

先在工作台按「啟用鍵盤」或點學徒模型，讓鍵盤焦點進入工作台。箭頭 / WASD 操作平面；右手升降與旋轉的鍵位顯示在控制面板。方向鍵用於移動時，網頁會停止用這些鍵捲動。輸入筆記、問題、選單或操作對話框時，工作台不攔截按鍵。

| 操作 | 鍵盤 |
|---|---|
| 平面 X / Y | ← ↑ ↓ → 或 WASD |
| 上升／下降 | I / K 或 PageUp / PageDown |
| 左轉／右轉 | J / L 或 Q / E |
| 抓取／放開 | 空白鍵 |
| 精細移動 | 按住 Shift，或點精調 |
| 撤銷 | Ctrl+Z / ⌘Z，或點撤銷 |
| 暫停鍵盤操控 | Esc |

如果頁面顯示未抓取，先按空白鍵或畫面的抓取按鈕。查看「已接收按鍵」狀態；按鍵已收到但模型未動時，檢查是否已完成鎖定、未抓取、被夾具擋住或已到邊界。點影片後焦點會移到播放器，繼續組合時請再次點「啟用鍵盤」。觸控裝置可用畫面雙手控制，支援長按；頁面失焦／切換工序會停止移動。

## 教學素材

專案說明頁及工作台新增照片、教學影片、深入研習與觀察題。影片由原發布者提供：支援嵌入的影片按載入後在 HTML 內播放，其他使用官方影片頁面。每則均保留原始入口，遇到地區限制、下架或發布者禁止嵌入，可開啟原頁。

影片字幕由發布者提供；網站 AI 翻譯不會自動翻譯影片音軌或產生字幕。照片保留作者、授權與適用範圍，並可點開完整圖片。相同教材可用於多個相關步驟，不能把共用照片誤認為逐工序的實拍。

## 一次更新教材、模型與程式

```bash
bash update-and-upload.sh \
  --repo https://github.com/kuonanhong/YOUR_REPOSITORY.git \
  --index-documents \
  --documents /完整路徑/教材資料夾 \
  --documents-remote myremote:macgyver-documents \
  --models-remote myremote:macgyver-models \
  --message 'Update curriculum and learning assets'
```

`YOUR_REPOSITORY`、教材路徑、rclone 目的地須換成您的設定。需先登入 GitHub 與設定 rclone。Windows 執行 `.sh` 更新腳本時需 Git Bash 或 WSL，並確保其中可執行 `python3`；一般網站啟動仍可直接使用 `run-local.bat`。沒有外部教材備份需求時，可省略 `--documents-remote`；沒有模型備份時可省略 `--models-remote`。欲上傳的模型放在 `models/`，權重由您另行取得。本腳本使用 copy，不刪除遠端舊檔；傳輸失敗會停止，可再次執行。

本機 AI 仍使用 `bash run-ai-local.sh`；Windows 用 `run-ai-local.ps1`。AI 索引是檢索教材文字，不是訓練或微調權重。私有教材預設不提交 Git。手機和平板使用瀏覽器連到同一 HTTPS 服務，無需在手機安裝 Python；電腦可使用 macOS、Windows 或 Linux。

## 驗證範圍

原始碼包含鍵盤事件、工序場景、教學媒體及後端的自動檢查。這不能代替在您的實際筆電、中文輸入法、手機瀏覽器和模型服務進行的現場驗收。工序圖是原創教育示意，並非設備廠的 CAD、製造數位分身或物理求解器。
