# MacGyver Engineering Academy V17

新增環境與城市 100 門逐步課程、工程島任務導覽、逐階段操作輔助，以及可切換視角的教學場景。影像素材共 149 張實拍照片與 7 張固定位置 360 全景。

開始使用：[V17 操作與設計說明](docs/V17_Design_and_Quickstart_ZH.html)；[一鍵解壓與 SSH 上傳](docs/UPLOAD_V17_ZH.md)。

```bash
bash run-local.sh                              # 本機帳號與 AI 後端
bash Upload_MacGyver_v17_SSH.sh                 # SSH 增量上傳公開網站
bash Upload_MacGyver_v17_SSH.sh --with-assets   # 另將現有文件／權重送至私人倉庫
```

完整離線閱讀可開啟根目錄 `index.html`。公開靜態試讀輸出用 `bash deploy-static.sh`。管理員設定、帳戶資料與私人文件不放入公開 GitHub。下載完整包或全部四個 Alternative ZIP 後，執行同次發行的 `bash Install_and_Upload_MacGyver_v17.sh --with-assets`，即可校驗、解壓與增量上傳；第一次上傳需先完成 GitHub SSH 設定。

Traditional Chinese and English course content; additional languages use configured translation. Licensed representative photographs, fixed-position panoramas and teaching models are distinguished from calibrated live digital twins. AI providers or local models require configuration; model weights and credentials are not bundled.

See [existing owner setup](docs/OWNER_ACCESS_V16_ZH.md), [V17 SSH upload](docs/UPLOAD_V17_ZH.md), [source and scene scope](tools/references-v17/REFERENCE_ANALYSIS_V17_ZH.txt), and [V17 validation](docs/VALIDATION_V17.json). Explicit V16 tools remain available for older packages.
