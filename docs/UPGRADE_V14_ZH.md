# V14 隧道與地下工程更新

本版以原始五份 V13 上傳 ZIP 為基礎，2,479 個檔案的 SHA-256 核對一致；GitHub main 的 release.json 也確認為 13.0.0。未直接改寫遠端倉庫，交付的是可本地啟動、可重建、可自行上傳的完整程式包。

## 教材與保留範圍

新增 100 門「隧道與地下工程」深入教材：每門 10 個技術單元，每個單元依序展開「機制與系統路徑、定量估算、試驗與驗證、失效診斷」四步，共 4,000 個新增步驟。雪山、英法、哥達三門原課的 54 個步驟保留；地下工程共 4,054 步。全站仍為 2,066 個主題，其中逐步課程增加為 807 門、24,274 步。

每門附繁中與英文原稿、工程檔案、公開資料與合成假設的區分、來源範圍、地理參照、比較案例與原創功能示意圖。九個子領域涵蓋世界巨作、地質與監測、TBM、分部開挖、支護襯砌、地下水、明挖逆打沉管、無開挖與豎井岩洞、地盤改良及維護。100 門索引為 `public/academy/data/tunnels-underground-100.csv`。

原有 710 門課的全部階段物件以 SHA-256 保存基線，重建驗證逐一比較，保留 20,274 個原步驟與識別碼。舊課程的進度不因新增單元而重新編號；原有三門地下課程的新增實驗只作用於 V14 新步驟。

## 首頁與跨平台使用

先完整解壓縮，執行 `bash run-local.sh`，依終端機顯示網址開啟。Windows 可用 `run-local.bat`，Bash 同步工具使用 Git Bash 或 WSL。一般本機網站只需 Python 3.10+；重新建置教材及應用程式使用 Node.js 22.13+。既有 Node 套件清單與鎖檔完整保留，相關安裝工具位於 `scripts/`。

根目錄 `index.html` 也提供檔案模式入口。首頁 HTML 立即呈現介紹與導覽，之後載入精簡目錄；完整課文、媒體、來源與地圖資料按需載入。檔案模式使用對應的傳統 JavaScript 分檔，避免依賴 `fetch(file://)`。詳見 `LAZY_LOADING_V14_ZH.md`。

手機與平板使用響應式同一網站，建議開啟已部署的 HTTPS 網址。手機的 localhost 指手機本身。GitHub Pages 只能提供靜態前端；需要雲端 AI、帳號及付費權限時，必須部署對應後端。相容設計與自動化 DOM 測試不等於已在每一品牌手機或作業系統實機量測。

## 互動與離線實驗

13 個透明教學模型涵蓋有效應力、水壓、均布面壓合力、掘進時間、高斯沉陷、Darcy 滲流、薄圓環膜力、支護分配、浮力、一維固結、通風功率、量測不確定度與環狀空隙。每個模型都列出單位、假設、適用範圍及思考題；超出範圍會清除舊結果與曲線。

另附 6 個 Python 標準函式庫實驗，無須 pip、不連網：沉陷體積積分、TBM 日曆預算、平行 Darcy 流路、風機工作點、收斂曲線擬合、一維固結級數解。檔案與獨立小包位於 `public/academy/assets/labs/v14/`。

```bash
python3 public/academy/assets/labs/v14/run-underground-labs.py --check
python3 public/academy/assets/labs/v14/run-underground-labs.py --output results.json
```

## 多語與 AI

79 種目標語言依瀏覽器偏好選擇，使用者也可手動切換。繁中／英文教材為完整原稿；其他全文依已配置翻譯服務、已載入本機模型或瀏覽器翻譯能力完成。失敗時保留原文並顯示未完成範圍，不能把可選語言數視為 79 份人工校訂教材。

助教提供 OpenAI 相容、Claude、Gemini、Ollama 及瀏覽器本機模型路線。API 金鑰與大型模型權重不包含在套件；網站登入權限也不等於 API 帳號配置。設定、啟動及差異上傳的完整命令見 `UPLOAD_AI_V14_ZH.md`。

## 更新程式與自有模型

```bash
bash macgyver.sh doctor
bash upload-all.sh --dry-run --skip-models
bash upload-all.sh --skip-models --skip-data
bash upload-all.sh --models-dir ./models --batch-mib 120
```

先做差異比對，再選擇網站或網站加模型同步。模型分成 40 MiB 分片、預設每批 120 MiB；具備雜湊比對、失敗重試與提交檢查點。預設保留遠端未由同步工具管理的檔案，不使用 force push。請閱讀文件中 `MODELS`、私人權重倉庫及資料更新選項的實際含義。

## 修改教材與重建

編輯 `tools/underground-v14/inputs/<課程ID>.json`，執行：

```bash
bash rebuild-underground.sh
```

此流程檢查雙語深度、生成教材、整合目錄、輸出 300 份 SVG、建立實驗包與離線分檔，最後檢查全站資料與 V13 保留雜湊。若也改動舊版橋樑等教材，須明確更新對應基線與版本紀錄，不能把預期修改誤當成自動通過的保留檢查。

大型權重、API 金鑰、帳號資料、運行快取及原 V13 私人收款筆記不納入可攜原始碼包。公開上傳工具另行排除私密設定。課程的計算與示意圖是教學材料，工程數值假設及適用邊界均在各課內明示。

## 驗證紀錄與再次封裝

完整發布紀錄見 `docs/VALIDATION_V14.json`；課文與原版保留檢查、獨立算例審核快照、兩次隔離還原、實際 HTTP 啟動及前端全量掃描，均有對應報告與可重跑工具。工程模型的算術與邊界審核不等於現場設計認證。

```bash
python3 tools/validate-underground-v14.py
python3 tools/validate-review-snapshots-v14.py
python3 tools/test-rebuild-v14.py
python3 tools/package-v14.py --output ../release-v14 --parts-mib 40
```

修改教材後，請重新審核並更新相應算例及 metadata 紀錄；封裝會拒絕與目前作者檔案不符的舊審核快照。發布包提供第三方瀏覽器執行資產與套件清單、鎖檔；`node_modules` 由安裝腳本依鎖檔建立，並未重複打包。

完整 ZIP 與分包二擇一使用。分包是各自可解壓的 ZIP，所有分包要解到同一個父資料夾，重建共同的 `MacGyver_Engineering_Academy_v14/`；不可把分包位元組串接。外部下載說明附各檔案大小、SHA-256 及 macOS／Linux／Windows 驗證命令。
