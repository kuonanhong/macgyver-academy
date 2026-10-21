V14 隧道與地下工程：六個可執行合成資料微型實驗

需求：Python 3.10+；不需pip、不連網、沒有第三方套件。
執行：python3 run-underground-labs.py --check
結果：python3 run-underground-labs.py --output results.json
Windows可將python3改成python或py -3。

1. 高斯沉陷：Simpson積分核對體積守恆。
2. TBM時間預算：每天有效掘進時數，避免利用率重複計算。
3. 平行Darcy流路：流量、質量與分流比例。
4. 風機與系統曲線：二分法求工作交點與功率。
5. 收斂監測：有界指數曲線擬合與外插限制。
6. 一維固結：級數解、90%時間與排水距離平方效應。

所有輸入為合成資料，結果記錄單位、假設及輸入SHA-256。可修改synthetic-cases.json後用--cases指定檔案；輸出僅供學習，非施工、設計或穩定性判定。實測與現場決策需要專業分析。
