# macOS Bash 變數邊界修正（V14 / V15）

Python 3.12.11 已正常；無須重裝 Conda。第65行舊字串 `（$PY）` 的變數與全形括號緊接，在使用者目前的 shell 環境引發 `PY?: 未綁定的變數`。已改為 `（${PY}）`，並修正 macgyver.sh 其他五處及 run-ai-local.sh 一處同類寫法，保持 set -u 防護。

把 ZIP 中 macgyver.sh、run-ai-local.sh 覆蓋 V14 根目錄同名檔；執行：

```bash
conda activate macgyver
bash macgyver.sh doctor
```

不需 sudo，也不需重新安裝 Python。單下載 macgyver.sh 即可修復 doctor；完整小修補包也包含本地AI啟動腳本。

驗證：8項離線Python／shell回歸測試與 Bash 語法檢查；本環境不是實體macOS，未冒稱完成macOS原機測試。

GNU Bash官方說明變數大括號可隔開其後字元：https://www.gnu.org/s/bash/manual/html_node/Shell-Parameter-Expansion.html
