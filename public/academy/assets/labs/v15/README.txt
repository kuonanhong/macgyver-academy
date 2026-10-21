MacGyver V15 水利與海岸工程 / Water and coastal engineering

使用 Python 3.10+，不需第三方套件。所有數值是合成教學資料。
Python 3.10+, standard library only. Every input is synthetic teaching data.

python3 run-water-labs.py --check
python3 run-water-labs.py --output my-results.json

修改 experiments() 中輸入再執行。各函數標示單位、假設、適用邊界。
Change inputs in experiments() and rerun. Each function names units and limits.
1. 水庫時段收支 / Reservoir interval mass balance: check conservation and infeasible releases.
2. 矩形明渠 / Rectangular channel: roughness sensitivity and wetted perimeter.
3. 水躍 / Hydraulic jump: check momentum conservation and positive energy loss.
4. 深水規則波 / Regular deep-water waves: group velocity and squared wave-height scaling.
5. 快速水錘 / Rapid water hammer: compare closure duration with wave round-trip time.
6. 福祿縮尺 / Froude scaling: distinguish length, velocity, time and discharge ratios.

練習：先預測改變方向，再計算；最後記錄模型未包含的因素與驗證資料。
Exercise: predict the trend before calculating, then record omitted mechanisms and needed evidence.
未提供操作規則、允收值或真實工程預測。No operating rules, acceptance values or real-project forecasts.

延伸閱讀 / References:
https://www.usbr.gov/tsc/techreferences/mands/wmm/indexframe.html
https://www.hec.usace.army.mil/software/hec-ras/documentation/HEC-RAS_Hydraulic_Reference_Manual_v6.6.pdf
https://www.publications.usace.army.mil/USACE-Publications/Engineer-Manuals/u43544q/636F617374616C20656E67696E656572696E67/
