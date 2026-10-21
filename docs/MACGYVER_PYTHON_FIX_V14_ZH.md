# V14 macgyver.sh 第 68 行修正

原因：原程式只接受 Python 3.10+。若目前環境沒有相容版本，PY 保持空字串；doctor() 雖已顯示缺少 Python，仍在原第 68 行執行空指令，造成「指令找不到」。這不是 GitHub SSH 權限問題。

## 套用

將修補包內 macgyver.sh 複製到已解壓的 MacGyver_Engineering_Academy_v14 根目錄，取代同名檔案。其餘教材和模型不需重新下載。完整 V14 ZIP 也已納入相同修正。

在該資料夾的終端機執行：

```bash
conda create -n macgyver python=3.12 -y
conda activate macgyver
python --version
bash macgyver.sh doctor
```

若 macgyver 環境已存在，可先直接 conda activate macgyver；確認 python --version 為 3.10 或以上即可。無須升級或改動原 base 環境。

新版會依序檢查 MACGYVER_PYTHON、目前 Conda 環境的 bin/python、PATH 中的 python3 與 python。檢查通過會顯示實際版本與路徑；找不到時會清楚提示，跳過需要 Python 的模型清單，並回傳環境檢查失敗，不再執行空指令。模型清單亦依已設定的 MODEL_DIR 檢查。

如需指定已安裝的 Python：

```bash
MACGYVER_PYTHON="$CONDA_PREFIX/bin/python" bash macgyver.sh doctor
```

檢查通過後，再按原需求執行 upload-all.sh。回歸測試使用隔離的假 Git／SSH／Node 與暫存目錄，沒有實際上傳或部署。
