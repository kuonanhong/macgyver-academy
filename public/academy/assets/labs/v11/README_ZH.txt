馬蓋先 V11：12 個原創合成資料微型實驗

本套件只使用 Python 3.10+ 標準函式庫；不需 pip、不連線、不下載模型，也不存取 GPU/QPU、設備或外部網路。
請解壓後在資料夾中執行：
  python3 run-evidence-labs.py --check
Windows 若使用 py launcher：
  py -3 run-evidence-labs.py --check
選一題：
  python3 run-evidence-labs.py --case attention

12 題：pipeline 管線 CPI、roofline 記憶體/運算上界、quorum 分區法定多數、alerts 告警精確率、dns TTL 更新、queue M/M/1 尾端延遲、privacy DP尺度/基本組合、attention 單頭注意力、neuron 單一神經元梯度學習、hydro 水力功率、gold 品位與回收、facility PUE能耗。

所有數字均為原創、虛構、合成情境，不是現場量測、效能跑分、正式安全閾值或工業操作參數。結果包含模型假設、單位及輸入SHA-256，可保留作工程筆記。
1. 先執行 --check 核對已提供的獨立已知答案。
2. 複製 synthetic-cases.json 成自己的檔，改一個輸入並寫下預測。
3. 用 --inputs 你的檔.json --case 題名，比較結果；更改輸入後原 checks 不會自动更新，--check 的失敗不代表你的假設一定無效。
4. 每次記錄變動、單位、模型限制與結果。重算能證明模型內的一致性，不能替代設備驗證。
5. 神經元案例是1維線性決策；在XOR會遇到能力限制。注意力案例只有一個query/head，未包含位置編碼或完整Transformer。

這是12個選出的可執行微型模型；100門課的其餘工作單、架構圖、算例與驗收題在網站內。這些結果不會自動取得正式會員證書。
