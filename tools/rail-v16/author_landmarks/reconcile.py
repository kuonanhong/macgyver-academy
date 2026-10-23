"""Reconcile project-specific exercises with the precise calculation boundary."""
def apply(P):
    fixes={
('b316','freeze'):'將輸入熱量與單位體積融冰潛熱需求分開，辨認等效融化深度不等同沉陷量。~Separate incoming heat from volumetric latent melting demand and distinguish equivalent thaw depth from settlement.',
('b302','rubber'):'用相同輪載與速度比較輪胎滾動阻力功率，另列導向輪的功能。~Compare tyre rolling-resistance power at equal wheel load and speed, separately identifying guide-wheel functions.',
('b303','doors'):'將停準、門位和測量誤差分開，檢查月台門對位的不確定度。~Separate stopping, door-position and survey errors when checking platform-door alignment uncertainty.',
('b305','baggage'):'依門口交換負荷建立攜行李旅客的等效係數，與一般旅客分開計數。~Define baggage-passenger equivalents for doorway exchange load and count them separately from ordinary passengers.',
('b305','queue'):'以相同平均班距但不同波動估算機場旅客的隨機到站等候。~Estimate random-arrival waiting for airport passengers with equal mean headway but different variability.',
('b307','pressure'):'以隧道內外溫度和絕對壓力估算空氣密度，另列壓力波模型。~Estimate air density from tunnel and outside temperature and absolute pressure, separately identifying the pressure-wave model.',
('b312','queue'):'對抵達終端後隨機候車的旅客比較規則與不規則班距。~Compare regular and irregular headways for passengers who arrive randomly to wait at the terminal.',
('b312','baggage'):'比較行李客群的等效車門交換需求，保留每人負荷係數。~Compare equivalent doorway demand from baggage travellers while retaining the per-person load factor.',
('b315','isolation'):'在隧道設備基座檢查振動隔離的頻率比，區分共振與高頻隔振。~Check frequency ratio for a tunnel-equipment isolator and distinguish resonance from high-frequency isolation.',
('b316','pressure'):'以高原絕對氣壓與溫度計算空氣密度，另列含氧與生理議題。~Calculate air density from altitude pressure and temperature, separately identifying oxygen and physiological questions.',
('b318','sand'):'把地表沉積通量與設備接收面積連結，估算清理週期的積砂質量。~Relate deposition flux to equipment receiving area and estimate sand mass over a cleaning interval.',
('b318','queue'):'在均可登車的假設下比較不同班距波動造成的隨機等候。~Compare random waiting caused by headway variability under the assumption that every arrival can board.',
('b318','baggage'):'以行李比例建立等效通道負荷，再與旅客實際人數分列。~Build equivalent passage load from baggage proportions and report it separately from actual headcount.',
('b320','queue'):'比較接駁班距波動造成的隨機等候，批次到達另做事件模擬。~Compare random waiting from feeder-headway variability and separately simulate batch arrivals.',
('b321','doors'):'分開停準、車門位置與測量誤差，核對平台對位的合成標準差。~Separate stopping, door-position and survey errors when checking combined alignment standard deviation.',
('b322','congestion'):'把兩個轉乘入口流量與共同出口容量比較，追蹤隊列守恆。~Compare two interchange inflows with shared exit capacity and track queue conservation.',
('b323','baggage'):'以行李旅客的等效交換需求比較市區站和航廈站負荷。~Compare city and terminal station loads through equivalent exchange demand from baggage passengers.',
('b323','queue'):'比較規則與不規則機場列車班距對隨機到站旅客的等候。~Compare random-arrival waiting under regular and irregular airport-train headways.',
('b324','doors'):'把列車停準與站門位置誤差分開，檢查共同偏差會否低估對位。~Separate stopping and platform-door position errors and check whether shared bias understates alignment error.',
('b324','isolation'):'對地下設備隔振基座比較激振頻率與固有頻率的比例。~Compare excitation and natural frequency for an underground-equipment isolation mount.',
('b325','sand'):'把設備表面積砂通量與接收面積相乘，估算一個維修週期的沉積。~Multiply surface deposition flux by receiving area to estimate accumulation over a maintenance interval.',
('b325','doors'):'在熱變形情境下分開列車停準、門位和測量對位誤差。~Separate stopping, door-position and survey alignment errors in a thermal-movement scenario.',
('b326','grout'):'以局部展開的薄層空隙估算灌漿量，區分理論體積與實注量。~Estimate grout for a locally unwrapped thin void, distinguishing theoretical from injected volume.',
('b327','doors'):'分開停準、門位和測量誤差，對比統計對位與最大機械淨空。~Separate stopping, door-position and survey errors, contrasting statistical alignment with maximum mechanical clearance.',
('b328','baggage'):'比較機場與通勤客群的等效通行負荷，保留行李比例。~Compare equivalent passage loads of airport and commuter groups while retaining baggage proportions.',
('b329','grout'):'用局部薄層幾何估算漿量，另外記錄超灌與回流來源。~Estimate grout volume from local thin-layer geometry and separately record excess injection and returns.',
('b330','congestion'):'把兩個出站方向匯入共同通道的流量與出口容量相減。~Subtract two merging exit flows from the capacity of their shared downstream passage.',
('b331','doors'):'讓新站門位與既有車輛停準配對量測，區分隨機及共同偏差。~Pair new station door-position measurements with existing vehicle stops and distinguish random from shared error.',
('b332','sand'):'用設備表面沉積通量與接收面積建立維修週期中的積砂質量。~Use surface deposition flux and receiving area to estimate sand mass over a maintenance interval.',
('b333','queue'):'把不規則班距帶入隨機等候估算，活動批次到達另建事件模型。~Estimate random waiting from irregular headways and separately model event-release batches.',
('b333','doors'):'在活動尖峰停站情境量測停準和門位誤差，保留對位分布。~Measure stopping and door-position errors during event-peak stops and retain the alignment distribution.',
('b333','isolation'):'對冷房設備基座檢查隔振傳遞率，區分阻尼與剛度變化。~Check transmissibility of cooling-equipment mounts and distinguish damping from stiffness changes.',
('b334','grout'):'以假想隧道局部薄層空隙驗算注漿體積，保留超灌和漏失項。~Check grout volume for a hypothetical local thin tunnel void, retaining excess and loss terms.'}
    for (cid,key),value in fixes.items(): P[cid]['contexts'][P[cid]['keys'].index(key)]=value
    # All tunnelwave calculations concern travel time, not wave amplitude.
    for cid,p in P.items():
        if 'tunnelwave' in p['keys']:
            p['contexts'][p['keys'].index('tunnelwave')]='在連續隧道與洞口測點之間比較聲波傳播時間和列車通過時間，另列波幅問題。~Compare acoustic travel time with train-passage time between tunnel and portal sensors, treating wave amplitude as a separate problem.'
