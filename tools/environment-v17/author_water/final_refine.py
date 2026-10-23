from pathlib import Path
p=Path(__file__).with_name('build_water.py')
s=p.read_text()
s=s.replace("(436,9):'gasbreak'}", "(436,9):'gasbreak',(436,6):'gasstorage',(440,7):'levelcalib',(445,0):'docload',(446,7):'filterwaste'}")
models='''
m('gasstorage','假想產氣=30、用氣=20 m³/h；時段=2 h~Hypothetical production=30, demand=20 m³/h; interval=2 h','ΔV=(Qprod-Quse)t','(30-20)*2','m³ reference gas','同一參考溫壓下的累積氣量差；不能直接當儲氣設備實際幾何容量或容許壓力。~Accumulated gas-volume difference at one reference condition; not vessel geometric capacity or permitted pressure.','量產用氣歷線、溫壓與其他氣體去向，逐時累積收支。~Measure production/demand traces, temperature/pressure and other destinations, then integrate hourly balances.','Quse:20→25 m³/h','(30-25)*2')
m('levelcalib','參考水位=0、2 m；讀值=0.05、1.95 m~Reference levels=0, 2 m; readings=0.05, 1.95 m','slope=(y2-y1)/(x2-x1)','(1.95-.05)/2','ratio','二點線性水位校正，不代表全量程或波動水面皆準確；須保留獨立驗證點。~Two-point linear level calibration does not establish full-range or fluctuating-surface accuracy; retain an independent check point.','核對高程基準、第三水位點與事件時間戳。~Check the elevation datum, a third level point and event timestamps.','y2:1.95→2.05 m','(2.05-.05)/2')
m('docload','Q=2000 m³/d；DOC=6 mg C/L~Q=2000 m³/d; DOC=6 mg C/L','LC=Q×DOC/1000','2000*6/1000','kg C/d','溶解有機碳負荷，不是濁度換算，也不單獨決定混凝藥量。~Dissolved-organic-carbon loading, not a turbidity conversion or a stand-alone coagulation-dose predictor.','以過濾樣本量 DOC，並同步量原水濁度、鹼度及 pH。~Measure DOC in filtered samples with concurrent source turbidity, alkalinity and pH.','DOC:6→8 mg C/L','2000*8/1000')
m('filterwaste','初濾排放流量=100 m³/h；假想持續=0.25 h~Filter-to-waste flow=100 m³/h; hypothetical duration=0.25 h','Vftw=Q×t','100*.25','m³','只計排放水量；持續時間不是水質達標門檻，實際回供需依監測及核准程序。~Waste-water volume only; duration is not a quality pass criterion, and return to supply requires monitoring/approved procedure.','對齊排放流量、連續濁度與閥位紀錄，辨識復原期。~Align waste flow, continuous turbidity and valve-state records to identify recovery.','t:0.25→0.40 h','100*.40')
'''
s=s.replace('# Process architecture is the physical/analytical flow, not the lesson index.',models+'\n# Process architecture is the physical/analytical flow, not the lesson index.')
s=s.replace("RESPONSE={", """RESPONSE={
'gasstorage':'逐時閉合產用氣，確認其他氣體去向與儲存參考狀態。~Close hourly production/demand and confirm other gas destinations and storage reference conditions.',
'levelcalib':'核對高程基準並以獨立水位驗證，重新播放感測偏差情境。~Check elevation datum against an independent level and replay the sensor-bias scenario.',
'docload':'重測 DOC 與原水特性，經瓶杯試驗判讀需求而非直接線性投藥。~Remeasure DOC/source properties and assess demand with jar tests rather than direct linear dosing.',
'filterwaste':'以連續水質確認復原，將初濾排放從淨產水扣除。~Confirm recovery with continuous quality and subtract filter-to-waste from net production.',""")
p.write_text(s)
