"""Original teaching models. Parameters are assumptions, not railway settings."""
import math

MODELS = {}

def M(key, quantities, expression, result_unit, mechanism, boundary, verification, failure, misconception, sensitivity):
    MODELS[key] = dict(quantities=quantities, expression=expression, result_unit=result_unit,
                      mechanism=mechanism, boundary=boundary, verification=verification,
                      failure=failure, misconception=misconception, sensitivity=sensitivity)

# Each quantity is (symbol, assumed value, unit, bilingual physical meaning).
M('braking', [('v',20,'m/s','初速~initial speed'),('a',0.8,'m/s2','定減速度大小~constant deceleration magnitude'),('tau',1.5,'s','反應時間~response time')],
  'v*tau+v*v/(2*a)','m',
  '停止距離由反應期間的等速前進與制動期間的動能消散相加。速度增加會同時增加兩項，而減速度只影響第二項；把控制命令發出時間當成制動力建立時間會漏掉一段距離。~Stopping distance combines constant-speed travel during response with kinetic-energy removal during braking. Speed changes both contributions, whereas deceleration changes only the second. A command timestamp is not the instant at which the full braking force becomes available.',
  '平直路線、定減速度、無輪滑；未含坡度、黏著變動或制動建立曲線。~Level track, constant deceleration and no slip; gradients, adhesion variation and brake build-up curves are excluded.',
  '以同一時基記錄速度、制動命令與加速度，分別積分反應段及減速段，再與實際位移比較。~Record speed, brake command and acceleration on one clock, integrate response and deceleration separately, and compare their sum with measured displacement.',
  '減速度偏低與反應延遲都會使停車超出目標，但速度曲線的起始轉折可以區分兩種原因。~Weak deceleration and delayed response both cause an overrun, but the onset of the speed-curve change distinguishes these causes.',
  '速度提高一成時停止距離也必定只增加一成~Increasing speed by ten percent always increases stopping distance by exactly ten percent.', 'v')
M('jerk', [('a0',0,'m/s2','起始加速度~initial acceleration'),('a1',0.9,'m/s2','終點加速度~final acceleration'),('dt',3,'s','過渡時間~transition time')],
  '(a1-a0)/dt','m/s3',
  '加加速度描述加速度改變的快慢，與最高加速度是不同的舒適性指標。相同速度增量可由平滑過渡或突變控制產生，站立乘客受到的瞬態擾動卻不同；控制器飽和也會截斷原先規畫的平滑曲線。~Jerk measures how rapidly acceleration changes and is distinct from peak acceleration. Smooth and abrupt commands can produce the same speed increment while imposing different transient disturbances on standing passengers. Actuator saturation can truncate an otherwise smooth planned transition.',
  '僅計線性加速度斜坡的平均加加速度，不代表振動舒適度完整指標。~Average jerk of a linear acceleration ramp only; this is not a complete vibration-comfort metric.',
  '先去除速度微分造成的高頻雜訊，再比較加速度計與里程推估的斜坡時間。~Control differentiation noise before comparing ramp duration from an accelerometer with the duration inferred from odometry.',
  '過度濾波可能讓顯示曲線看似平順，卻掩蓋真實衝擊；致動飽和則留下平頂加速度。~Excessive filtering can hide a real shock behind a smooth display, whereas actuator saturation leaves a flat-topped acceleration trace.',
  '最高加速度相同就代表乘坐感受一定相同~Equal peak acceleration guarantees an identical ride sensation.', 'dt')
M('traction', [('m',180000,'kg','列車質量~train mass'),('a',0.6,'m/s2','加速度~acceleration'),('R',12000,'N','等效阻力~equivalent resistance'),('v',15,'m/s','速度~speed')],
  '(m*a+R)*v/1000','kW',
  '牽引力先克服阻力，剩餘部分才增加列車動量。輪周機械功率等於牽引力乘速度，因此低速大力不必然等於高功率；電源側功率另受效率、輔助負載及回生可受納性影響。~Traction force first overcomes resistance; the remainder changes train momentum. Mechanical power at the wheel equals force times speed, so a large low-speed force need not imply high power. Electrical input also depends on efficiency, auxiliaries and regenerative receptivity.',
  '集中質量與定阻力模型，未含輪軸轉動慣量、坡度或黏著上限。~Lumped mass and fixed resistance; rotating inertia, gradient and adhesion limits are omitted.',
  '將速度與牽引力同步取樣，對照加速度反推的慣性力，並另列輔助設備耗電。~Synchronize speed and traction-force samples, compare inertial force inferred from acceleration, and account separately for auxiliary consumption.',
  '把電網輸入功率直接當成輪周功率會高估加速能力，低速輪滑亦可使電流很高而車速不升。~Treating grid input as wheel power overstates acceleration capability; low-speed slip can produce high current without increasing train speed.',
  '牽引電流變大就能保證車速增加得更快~Higher traction current guarantees a greater train acceleration.', 'm')
M('energy', [('m',180000,'kg','等效質量~equivalent mass'),('v',22,'m/s','速度~speed'),('eta',0.7,'1','回收效率~recovery efficiency')],
  '0.5*m*v*v*eta/3.6e6','kWh',
  '回生能量的上限先受列車動能限制，再受轉換損失與受電端容量限制。速度平方決定動能量級，回生率不能單獨說明整趟能耗；若鄰車或儲能無法接收，原可回收的能量仍可能轉為電阻熱。~Recoverable energy is bounded first by kinetic energy and then by conversion losses and receiver capacity. The square of speed sets the energy scale, while recovery efficiency alone cannot describe journey consumption. Energy may still become resistor heat when nearby trains or storage cannot accept it.',
  '忽略旋轉動能、坡度位能及輔機，效率固定且假設有足夠受納容量。~Rotating energy, elevation and auxiliaries are omitted; efficiency is constant and receiving capacity is assumed adequate.',
  '比較電機側與直流母線能量積分，分開記錄制動電阻消耗與儲能充電。~Compare integrated machine-side and DC-bus energy, keeping braking-resistor dissipation distinct from energy stored.',
  '電壓過高限制回生時，制動力仍可能由混合制動維持，不能由低回收量直接判定制動失效。~High bus voltage can restrict regeneration while blended braking preserves stopping effort; low recovered energy alone does not prove brake failure.',
  '有回生制動的列車就不會產生任何制動熱~A train with regenerative braking produces no braking heat.', 'v')
M('position_latency', [('v',18,'m/s','列車速度~train speed'),('t',0.25,'s','資料年齡~data age'),('e',0.6,'m','定位誤差界~position error bound')],
  'v*t+e','m',
  '位置資料的數值誤差與資料變舊造成的位移應分開處理。即使感測器本身準確，封包等待與處理延遲仍會擴大當前位置的不確定範圍；接收時間不能取代量測時間，否則不同子系統可能各自認為資料是新的。~Position measurement error and displacement accumulated while data ages are separate contributions. Even an accurate sensor can yield an uncertain current location after queuing and processing delays. Reception time cannot substitute for measurement time because subsystems could then each mistakenly regard stale information as new.',
  '定速與有界誤差的保守加總，非隨機誤差的均方根合成。~Constant speed and a conservative sum of bounded errors, not root-sum-square combination of random errors.',
  '保留量測、傳送及接收三個時間戳，以延遲注入重播檢查界限是否包住真值。~Preserve measurement, transmit and receive timestamps; replay injected delays and verify that the resulting bound encloses the reference position.',
  '時鐘偏移會偽裝成網路延遲，重設時間戳又可能隱藏陳舊資料，需用獨立時間基準辨認。~Clock offset can imitate network delay, while timestamp replacement can conceal stale data; an independent time reference distinguishes them.',
  '封包剛收到就代表其中位置一定是現在的位置~A newly received packet always contains the present position.', 't')
M('headway', [('L',180,'m','列車占用長度~occupied train length'),('S',420,'m','假想防護距離~hypothetical protected distance'),('v',15,'m/s','等速速度~constant speed'),('td',20,'s','附加處理時間~additional processing time')],
  '(L+S)/v+td','s',
  '班距是時間資源問題，不能僅用兩車車頭距離判斷。列車長度、防護距離與釋放時間會共同占用線路；車站停靠、路口衝突或折返可能比區間運轉更先成為瓶頸，所以縮小單一間隔不等於全線增能。~Headway is a time-resource problem, not merely a distance between train fronts. Train length, protected separation and release time occupy the route together. Dwell, conflicting junctions or terminal reversals can dominate capacity before open-line running does, so reducing one interval need not raise line throughput.',
  '等速單一資源的概念下界，不是任何號誌系統的實際最小班距。~Conceptual lower bound for one resource at constant speed, not an operating minimum for any signalling system.',
  '以時空圖標出車尾清空與資源釋放時刻，再檢查月台、道岔及折返各自的占用。~Mark rear clearance and resource release on a time-distance diagram, then examine platform, point and reversal occupation separately.',
  '將車頭離站當成月台路徑已清空會低估占用時間，瓶頸轉移則會造成局部改善卻全線延誤。~Treating front departure as complete route clearance understates occupation; a shifted bottleneck can improve one section while delays persist elsewhere.',
  '只要區間最小間距縮短全線運能必定同比提高~Reducing open-line separation always increases whole-line capacity in the same proportion.', 'S')
M('dwell', [('N',180,'persons','登車人數~boarding passengers'),('doors',12,'doors','有效門數~effective doors'),('rate',0.8,'persons/(s*door)','每門流率~flow per door'),('fixed',12,'s','固定程序時間~fixed procedure time')],
  'N/(doors*rate)+fixed','s',
  '停站時間包含人流服務與固定開關門程序。各門均分旅客時可用總服務率估算，但熱門樓梯旁的門通常更壅塞；瓶頸門完成時間控制發車，平均流率因此不能保證最忙車門也能按時結束。~Dwell includes passenger service and fixed door sequences. Dividing by total service rate assumes an even passenger distribution, yet doors near popular stairs are often more crowded. The busiest door governs completion, so average flow cannot guarantee timely clearance at that door.',
  '均勻單向登車，沒有下車逆流、行李阻塞或門重開。~Uniform one-way boarding without alighting counterflow, luggage blockage or door reopening.',
  '逐門記錄開始與結束時間，將固定程序從人流時間中扣除，再比較最忙門與平均門。~Record start and finish at each door, subtract fixed procedure time, and compare the busiest door with the mean.',
  '平均人數正常但單門集中仍會延誤；門故障與旅客逆流都可能造成相似的總停站時間。~A normal average load can hide a concentrated door queue; mechanical faults and passenger counterflow can produce similar total dwell.',
  '總旅客數相同就代表每次停站時間一定相同~Equal total passenger counts always produce equal dwell times.', 'N')
M('timetable_slack', [('scheduled',140,'s','排定間隔~scheduled interval'),('occupied',110,'s','資源占用~resource occupation'),('delay',18,'s','入侵延誤~incoming delay')],
  'scheduled-occupied-delay','s',
  '時刻表餘裕是已排間隔扣除占用與擾動後的剩餘時間。餘裕可以吸收小延誤，卻不是可隨意重複使用的免費容量；同一段緩衝若被兩個衝突約束同時借用，紙面上可行的時刻仍會在實際重播中互相追趕。~Timetable margin is scheduled separation less occupation and perturbation. It can absorb small delays but is not free capacity that may be reused indefinitely. If two conflicting constraints both claim the same buffer, a timetable that appears feasible on paper can still produce converging delays in replay.',
  '單一衝突資源與確定延誤，未求解整個網路的隨機時刻最佳化。~One conflicting resource and a deterministic delay; no stochastic network-wide timetable optimization is implied.',
  '將每一段餘裕標記唯一用途，逐列重播延誤，檢查負餘裕是否傳到下一個路口。~Assign each buffer a unique purpose, replay train delays in sequence, and check whether negative margin propagates to the next junction.',
  '重複計入同一緩衝會掩蓋衝突；把終點補時誤算為上游路口可用時間也會高估穩健度。~Double-counted buffers hide conflicts; recovery time at a terminus cannot automatically be used at an earlier junction.',
  '同一段時刻餘裕可以同時完整吸收所有列車延誤~The same timetable buffer can fully absorb every train delay simultaneously.', 'delay')
M('utilization', [('arrival',8,'jobs/h','平均到達率~mean arrival rate'),('service',12,'jobs/h','單通道服務率~single-channel service rate')],
  'arrival/service','1',
  '利用率比較需求與服務能力，是穩定性檢查而非等待時間的完整答案。平均需求小於平均容量仍可能出現短暫尖峰與排隊；若排程把所有時段填滿，任何變異都只能向後傳播，缺乏讓系統恢復的空間。~Utilization compares demand with service capacity; it is a stability check rather than a complete waiting-time answer. Mean demand below mean capacity still permits bursts and queues. When every interval is fully occupied, variability propagates downstream because no recovery space remains.',
  '固定平均率且單一服務通道；實際批次、優先權與休息中斷須另建模。~Fixed mean rates and one service channel; batches, priorities and interruptions require separate modelling.',
  '以不同時間窗統計到達與完成數，檢查平均值是否掩蓋短時過載，並保留未完成工作。~Count arrivals and completions over several windows, test for hidden bursts, and retain unfinished work in the accounting.',
  '只統計完成案件會漏掉被延後或放棄者，使負荷被低估；設備停機又會降低可用服務率。~Counting only completed jobs omits deferred or abandoned demand and understates loading; downtime also reduces available service rate.',
  '平均利用率低於百分之百就保證完全不會排隊~Mean utilization below one hundred percent guarantees that no queue ever forms.', 'arrival')
M('latency_sum', [('sense',0.03,'s','量測時間~sensing time'),('network',0.08,'s','網路時間~network time'),('compute',0.02,'s','運算時間~computation time'),('actuate',0.12,'s','致動時間~actuation time')],
  'sense+network+compute+actuate','s',
  '端到端延遲由量測、通訊、運算與致動串接而成。改善最快的一段通常影響有限，且平均延遲不能代表最壞尾端；定義一致的起訖事件，才能避免子系統都量到好看的數值卻漏掉交接等待。~End-to-end delay spans sensing, communication, computation and actuation. Improving the fastest stage often yields little benefit, and mean latency does not represent its worst tail. Consistent start and end events prevent subsystems from reporting attractive numbers while overlooking handoff queues.',
  '各階段串行且時間確定，沒有平行重疊或隨機尾端。~Deterministic serial stages without overlap or random latency tails.',
  '沿同一事件編號串接時間戳，檢查每一段邊界是否重疊或漏算，並注入負載重測。~Follow one event identifier through timestamps, check stage boundaries for overlap or gaps, and repeat under injected load.',
  '時間基準不同可造成負延遲假象；漏記排隊會使快速單元測試無法預測整合表現。~Different clock references can create apparently negative delays; omitted queues prevent fast unit tests from predicting integrated performance.',
  '每個子系統平均很快就代表整體最壞延遲一定很短~Fast average subsystems guarantee a short worst-case end-to-end delay.', 'network')
M('packet_loss', [('p',0.02,'1','獨立遺失率~independent loss probability'),('n',3,'packets','連續封包數~consecutive packet count')],
  'p**n','1',
  '獨立封包遺失可以相乘得到連續遺失機率，但實際無線遮蔽常造成成串遺失。增加重送次數會占用時間與頻寬，不能把可靠度與時效分開最佳化；舊封包即使最後送達，也可能已不適合當前控制。~Independent packet losses multiply to give a consecutive-loss probability, but radio obstruction often causes correlated bursts. Retransmissions consume time and bandwidth, so reliability and freshness cannot be optimized independently. A packet eventually delivered may already be too old for the current control decision.',
  '明確假設各次遺失獨立同分布，不適用遮蔽引起的相關失聯。~Losses are explicitly independent and identically distributed; correlated outages are outside the model.',
  '同時統計單包遺失率與最長連續遺失段，將結果和獨立模型比較以辨識相關性。~Measure single-packet loss and the longest loss burst together, then compare them with the independent model to identify correlation.',
  '把成串失聯當成獨立事件會嚴重低估尾端風險，時間戳重排也可能讓重送掩蓋陳舊資料。~Treating burst outages as independent events understates tail risk; reordered timestamps may also hide stale retransmissions.',
  '只知道平均丟包率就能完全判定通訊可靠性~The mean packet-loss rate completely determines communication reliability.', 'p')
M('throughput', [('trains',30,'trains','列車數~train count'),('bytes',240,'bytes','每次訊息大小~message size'),('rate',5,'Hz','更新頻率~update frequency'),('overhead',1.6,'1','協定擴張倍率~protocol overhead factor')],
  'trains*bytes*8*rate*overhead/1000','kbit/s',
  '網路負載必須把列車數、更新頻率、封包長度及協定額外開銷一併計入。總位元率只是起點，同步突發、重送與頻道共享仍會改變排隊延遲；容量充足也不代表封包的截止時間一定可以滿足。~Network demand includes train count, update frequency, packet length and protocol overhead. Aggregate bit rate is only a starting point because synchronized bursts, retransmissions and channel sharing affect queues. Adequate average capacity does not guarantee that every packet meets its deadline.',
  '均勻持續流量，不包含加密協商、重送尖峰或介質競爭。~Uniform sustained traffic; handshakes, retransmission bursts and medium contention are omitted.',
  '在封包擷取中核對實際線上長度，將同步與錯開更新兩種情境分別量測延遲。~Check actual wire length in packet captures and compare delay for synchronized versus staggered updates.',
  '只用應用資料長度估算會漏掉協定開銷，所有車同時更新又可能造成短時佇列爆滿。~Application payload length alone misses protocol overhead; simultaneous train updates can fill queues despite moderate mean traffic.',
  '平均頻寬足夠就保證每一個封包都準時抵達~Sufficient average bandwidth guarantees on-time arrival of every packet.', 'trains')
M('availability', [('mtbf',2000,'h','平均故障間隔~mean time between failures'),('mttr',4,'h','平均修復時間~mean repair time')],
  'mtbf/(mtbf+mttr)','1',
  '可用度描述長時間內能提供服務的比例，故障頻率與修復速度都會影響它。相同可用度可能來自頻繁短停或罕見長停，對旅客與維修資源的影響不同；更不能把高可用度直接解讀為故障發生時一定安全。~Availability describes the fraction of long-run time during which service is possible; both failure frequency and repair duration matter. The same value can arise from frequent brief outages or rare long ones with different passenger and maintenance consequences. High availability does not itself establish safe behaviour during failure.',
  '可修復二狀態穩態模型，未含共同原因故障、預防保養與供應鏈等待。~Repairable two-state steady model; common-cause failures, planned maintenance and supply-chain waiting are excluded.',
  '分別核對故障起點、服務恢復及完全修復時間，避免把部分恢復誤列為全功能。~Audit failure onset, service restoration and full repair separately rather than counting degraded service as full functionality.',
  '刪除長停機紀錄會扭曲平均修復時間；重複報修同一缺陷則會錯估故障頻率。~Removing long outages distorts mean repair time, while duplicate reports of one defect distort failure frequency.',
  '系統可用度很高就能直接證明所有故障都是安全的~High system availability directly proves that every failure is safe.', 'mttr')
M('coverage', [('tested',72,'cases','已執行案例~executed cases'),('total',90,'cases','已定義案例~defined cases')],
  'tested/total','1',
  '測試覆蓋率只對已定義的分母有意義。需求、狀態、轉移與危害各有不同分母，執行很多正常案例仍可能漏掉罕見但重要的交接；同一案例重跑多次不會自動增加獨立需求的覆蓋。~Coverage is meaningful only relative to its defined denominator. Requirements, states, transitions and hazards have different denominators. Many normal cases can still omit a rare but important handoff, and repeating one case does not automatically cover additional independent requirements.',
  '計數式已知案例覆蓋，不是失效機率或安全完整性量化。~Count-based coverage of known cases, not a probability of failure or a safety-integrity measure.',
  '建立需求到案例的一對多追溯表，將未測、失敗與不適用分開，抽查原始證據。~Build requirement-to-case traceability, separate untested, failed and inapplicable cases, and sample raw evidence.',
  '縮小分母可讓覆蓋率看似提高，重複案例也可能掩蓋邊界狀態根本未被執行。~Shrinking the denominator makes coverage look better; duplicate cases can hide boundary states that were never exercised.',
  '測試覆蓋率達到百分之百就等於零故障風險~One hundred percent test coverage means zero failure risk.', 'tested')
M('state_space', [('bits',8,'bits','布林變數數量~number of Boolean state variables')],
  '2**bits','states',
  '布林狀態組合隨變數個數指數成長，這說明逐一人工檢查很快失去效率。可達性約束能排除不可能組合，但刪除條件必須有證據；安全性質通常針對所有可達狀態，而非幾個畫面上看起來合理的狀態。~Boolean combinations grow exponentially with variable count, explaining why manual enumeration soon becomes ineffective. Reachability constraints can eliminate impossible combinations, but each exclusion needs justification. Safety properties normally concern every reachable state rather than a few states that look plausible on a display.',
  '未限制的布林笛卡兒積；實際可達狀態通常較少，但需另證明。~Unconstrained Boolean Cartesian product; actual reachability can be smaller but must be established separately.',
  '用小型模型列舉轉移，再與需求允許的轉移表比較，對被排除狀態留下理由。~Enumerate transitions in a small model, compare against the required transition table, and document reasons for excluded states.',
  '把感測器故障狀態預先刪掉會讓證明失去關鍵邊界，狀態抽象過粗也可能隱藏時序競爭。~Excluding sensor-fault states can remove the crucial boundary from a proof; overly coarse abstraction may hide timing races.',
  '狀態變數多一個只會多出一種狀態組合~Adding one Boolean state variable creates only one additional combination.', 'bits')
M('fault_union', [('p1',0.001,'1','事件一機率~event one probability'),('p2',0.002,'1','事件二機率~event two probability')],
  'p1+p2-p1*p2','1',
  '只要任一支路失效就產生頂事件時，需計算聯集而不是把兩機率相乘。獨立假設允許扣掉交集的乘積，若共享電源、環境或軟體則交集另有結構；事件樹和失效樹必須保持同一任務時間。~When either branch can trigger the top event, the relevant probability is a union rather than a product. Independence permits the intersection to be written as a product; shared power, environment or software changes that intersection. Event and fault trees must use the same mission duration.',
  '兩事件獨立且機率屬同一任務期間，並非每小時危險失效率。~Two independent events over one mission interval, not a dangerous-failure rate per hour.',
  '先畫頂事件邏輯再代機率，明列共享資源並檢查事件時間窗是否一致。~Draw top-event logic before inserting probabilities, list shared resources, and check consistent time windows.',
  '把聯集誤寫成交集會低估危險；混合年度機率與每小時機率則使結果失去量綱意義。~Confusing a union with an intersection understates risk; mixing annual and hourly probabilities destroys the intended meaning.',
  '任一支路故障即失效時總機率等於兩機率相乘~If either branch failure is sufficient, total failure probability equals their product.', 'p1')
M('redundancy', [('p',0.002,'1','獨立支路失效機率~independent branch failure probability'),('common',0.0001,'1','共同原因事件機率~common-cause event probability')],
  'common+(1-common)*p*p','1',
  '兩支路都失效才失去功能的架構可降低獨立故障貢獻，卻不能消除共同原因。共同電源、相同軟體缺陷或同處淹水會同時影響兩支路；因此增加硬體數量不能取代分離、異質性與失效偵測的證據。~A function lost only when both branches fail can reduce independent contributions but cannot eliminate common causes. Shared power, identical software defects or flooding at one location can affect both branches. More hardware does not replace evidence for separation, diversity and fault detection.',
  '共同原因先發生的簡化條件模型，其餘支路相互獨立；非安全等級認證。~Simple conditional model with common cause considered first and remaining branches independent; no safety-level certification is implied.',
  '把獨立與共同原因兩類試驗分開，在隔離試驗台檢查共享介面失效的影響。~Separate independent and common-cause tests, using an isolated bench to examine failures of shared interfaces.',
  '共享電源中斷會讓看似雙備援同時失去功能，若故障偵測也共用同一支路更可能誤報正常。~Loss of a shared supply can defeat apparently duplicated equipment, especially if fault detection depends on that same branch.',
  '裝設兩套相同設備就能完全消除共同原因故障~Installing two identical systems completely removes common-cause failures.', 'common')
M('ohm', [('V',12,'V','激勵電壓~excitation voltage'),('R',8,'ohm','等效電阻~equivalent resistance')],
  'V/R','A',
  '電壓與電流的關係取決於完整回路阻抗，不能只看單一導體。簡化電阻模型能用來辨認分流、接觸與漏電的量級，但交流軌道電路還涉及頻率、相位與耦合；量到電壓存在並不等於接收端已可靠判定。~Voltage-current behaviour depends on the entire circuit rather than one conductor. A resistance model helps reason about shunts, contacts and leakage, while AC track circuits also depend on frequency, phase and coupling. Voltage presence alone does not establish a valid receiver decision.',
  '純電阻穩態概念模型，未含交流電抗或任何現場占用判定門檻。~Steady resistive teaching model; AC reactance and real occupancy thresholds are not included.',
  '在完全隔離的低壓教具量測源端與負載端電壓電流，逐一改變接觸或漏電支路。~On an isolated low-voltage teaching rig, measure source and load voltage/current while changing contact or leakage branches one at a time.',
  '接觸阻抗上升與供電下降都會降低電流，可用兩端電壓分布辨認，不能直接在營運軌道上試驗。~Contact resistance and supply drop both reduce current; terminal voltage distribution distinguishes them. Such experiments do not belong on an operating track.',
  '只量到供電端有電壓就可確認接收端一定正常~Voltage at the supply terminal proves the receiver is operating correctly.', 'R')
M('parallel', [('R1',10,'ohm','支路一電阻~branch one resistance'),('R2',40,'ohm','支路二電阻~branch two resistance')],
  'R1*R2/(R1+R2)','ohm',
  '並聯支路分配電流並降低總等效電阻。新增漏電路徑可能改變接收訊號而不改變供電電壓，乾濕環境的差異因此不能被單純視為量測雜訊；是否代表安全占用仍須由完整的故障安全設計決定。~Parallel paths divide current and reduce equivalent resistance. A leakage path can alter the received signal without changing supply voltage, so differences between dry and wet conditions are not merely measurement noise. Whether a condition produces a safe occupied indication depends on the complete fail-safe design.',
  '兩個線性電阻的靜態教具，未模擬頻率選擇接收器。~Static teaching circuit with two linear resistors; frequency-selective receivers are not represented.',
  '保持激勵相同而分別量支路電流，確認總電流守恆，再比對不同絕緣情境。~Keep excitation fixed, measure branch currents separately, verify current conservation, and compare insulation scenarios.',
  '將漏電誤判為輪對分流會混淆故障來源；量測儀輸入電阻太低也可能自己形成額外分流。~Confusing leakage with a wheelset shunt misidentifies the fault; an instrument with low input resistance can itself create a parallel path.',
  '並聯多一條漏電路徑不會改變整個電路的電流~Adding a parallel leakage path cannot change the total circuit current.', 'R2')
M('rc', [('R',10000,'ohm','電阻~resistance'),('C',0.0001,'F','電容量~capacitance')],
  'R*C','s',
  '電阻電容時間常數表示一階響應速度，濾除短脈衝也會延後真正的狀態改變。增強濾波與提高反應速度常互相衝突；訊號判定應結合雜訊頻譜與允許延遲，不可只追求顯示平穩。~An RC time constant characterizes first-order response. Suppressing brief pulses also delays genuine state changes, creating a tradeoff between filtering and response. Signal interpretation must consider noise spectra and allowable delay rather than aiming only for a smooth display.',
  '線性一階小訊號模型，時間常數不是確定的安全動作延時。~Linear first-order small-signal model; the time constant is not a prescribed safety-action delay.',
  '用已知階躍輸入量測上升與下降曲線，從曲線擬合時間常數並檢查非對稱。~Apply a known step, measure rise and decay, fit the time constant, and inspect response asymmetry.',
  '濾波過重會延遲異常呈現，電容量漂移則可能讓同一設定在不同溫度下具有不同反應。~Over-filtering delays anomaly indication; capacitance drift can change response with temperature despite unchanged settings.',
  '濾波越強就能同時得到越快的狀態反應~Stronger filtering always gives a faster state response as well.', 'C')
M('snr', [('signal',2,'V_rms','訊號有效值~signal RMS'),('noise',0.1,'V_rms','雜訊有效值~noise RMS')],
  '20*log10(signal/noise)','dB',
  '以相同阻抗下的電壓比換算訊雜比時使用二十倍對數。訊號與雜訊必須採一致頻寬與有效值定義；只把量測頻寬縮小可能讓數字改善，卻同時刪掉辨識狀態所需的訊息。~Voltage-ratio signal-to-noise uses twenty times the logarithm when impedances match. Signal and noise must share bandwidth and RMS definitions. Narrowing measurement bandwidth can improve the number while removing information needed to distinguish states.',
  '相同阻抗與相同頻寬的均方根電壓，不適用任意峰值比。~RMS voltages with equal impedance and bandwidth; arbitrary peak ratios are not interchangeable.',
  '將有訊號與無訊號樣本採同一濾波器處理，保留頻譜與時間波形交叉比對。~Process signal-present and signal-absent samples through the same filter, retaining both spectra and time traces.',
  '電磁干擾若落在訊號頻帶內，總有效值可能變大但辨識反而變差；飽和也會破壞比例。~In-band interference may increase total RMS while worsening identification; saturation also destroys the assumed proportionality.',
  '總量測電壓越大就能保證訊號品質越好~A larger measured total voltage guarantees better signal quality.', 'noise')
M('count_balance', [('enter',48,'axles','進入軸數~entering axles'),('leave',44,'axles','離開軸數~leaving axles')],
  'enter-leave','axles',
  '計軸占用利用邊界流入與流出守恆，計數差不是列車位置量測。差值為零仍需邊界感測器、方向判斷與狀態可信度成立；未知或故障狀態不能僅因兩個數字相等就自動宣告清空。~Axle counting applies conservation at section boundaries; the count difference is not a position measurement. A zero difference is useful only when boundary sensing, direction and state validity are trustworthy. Unknown or failed states cannot be declared clear merely because two numbers match.',
  '離線整數守恆模型，不含任何現場重置或解鎖程序。~Offline integer-conservation model without any real reset or release procedure.',
  '以標記輪對的玩具車雙向重播，對照人工真值、事件順序與感測器有效旗標。~Replay a marked model vehicle in both directions and compare manual truth, event ordering and sensor-validity flags.',
  '漏計與多計可能互相抵消形成假零值，方向錯誤則會讓計數增減的符號顛倒。~Missed and extra counts can cancel into a false zero, while direction errors reverse the signs of increments.',
  '進出計數剛好相同就能無條件證明區段無車~Equal entry and exit counts unconditionally prove that a section is empty.', 'enter')
M('pulse_speed', [('spacing',0.3,'m','感測點間距~sensor separation'),('dt',0.015,'s','通過時間差~passage time difference')],
  'spacing/dt','m/s',
  '兩個相鄰感測點的事件先後順序可提供方向，間距除以時間差可估局部速度。時間解析度與輪緣幾何都影響結果；接近停車或往返擺動時，事件配對比公式本身更容易出錯。~Event ordering across two nearby sensors provides direction, while separation divided by transit time estimates local speed. Timing resolution and wheel geometry affect the estimate. Near standstill or during oscillatory movement, pairing the correct events is often harder than evaluating the equation.',
  '同一輪對等速通過且事件配對正確，忽略感測區域寬度。~One wheelset moving at constant speed with correct event pairing; sensing-zone width is neglected.',
  '使用獨立位置尺與時間基準核對事件配對，包含低速、停止與反向的離線測試。~Check event pairing against an independent ruler and clock, including low-speed, stopped and reversed offline tests.',
  '將不同輪對的脈衝配成一對會產生不合理速度，反向回滾也會破壞單純遞增事件假設。~Pairing pulses from different wheelsets produces implausible speed; rollback violates assumptions of monotonically ordered events.',
  '感測點越近就能在所有速度下得到越精準的速度~Closer sensors always give more accurate speed at every operating speed.', 'dt')
M('work', [('F',4500,'N','作用力~applied force'),('s',0.12,'m','作用行程~travel'),('eta',0.65,'1','機械效率~mechanical efficiency')],
  'F*s/eta','J',
  '致動器輸入能量必須支應負載作功與摩擦損失。相同行程不代表相同負載，潤滑、對位與溫度會改變力的分布；只看總電流峰值可能忽略行程中某一位置的卡滯，需把力與位移配對。~Actuator input energy must cover load work and frictional loss. Equal travel does not imply equal loading because lubrication, alignment and temperature change force distribution. A single current peak can miss binding at a particular position, so force should be paired with displacement.',
  '定力準靜態行程與定效率，不含撞擊、慣性及實際轉轍鎖閉要求。~Constant-force quasistatic travel and fixed efficiency; impacts, inertia and real point-locking requirements are excluded.',
  '在隔離試驗台同步記錄力、位移與電流，積分力位移曲線並比較往返差異。~On an isolated bench, synchronize force, displacement and current, integrate the force-travel curve and compare both directions.',
  '摩擦增加與機構偏心都能提高能耗，但其位置依賴不同；行程結束也不等於鎖閉已被證明。~Friction and misalignment both increase energy but differ with position; reaching the end of travel does not prove locking.',
  '致動器走完行程就能保證機構已完成安全鎖閉~Completing actuator travel guarantees safe mechanical locking.', 'F')
M('torque', [('F',1800,'N','切向作用力~tangential force'),('r',0.08,'m','力臂~lever arm')],
  'F*r','N*m',
  '力矩取決於力與轉軸的垂直力臂，不只取決於馬達功率。連桿角度改變會改變機械利益，接近死點時力與位移關係尤其敏感；外殼上的扭矩讀值也不一定等於尖軌端的實際推力。~Torque depends on force and perpendicular lever arm, not merely motor power. Linkage angle changes mechanical advantage, particularly near a dead centre where force-displacement relations become sensitive. Torque measured at the housing need not equal effective force at the switch blade.',
  '垂直定力臂的靜力模型，忽略齒輪摩擦與連桿角度變化。~Static perpendicular constant lever arm; gear friction and changing linkage angle are omitted.',
  '以量測幾何核對力臂方向，分別量輸入扭矩與輸出推力，建立行程對應曲線。~Check lever-arm direction from measured geometry, measure input torque and output force separately, and map both against travel.',
  '把半徑當成所有位置的有效力臂會造成系統性誤差，鬆動連接則可能有高轉矩卻沒有有效位移。~Using radius as the effective lever arm at every position causes systematic error; loose connections can absorb torque without useful travel.',
  '力臂變短時相同作用力一定產生更大的力矩~A shorter lever arm always produces greater torque from the same force.', 'r')
M('fusion', [('x1',100,'m','觀測一位置~first observed position'),('x2',104,'m','觀測二位置~second observed position'),('s1',2,'m','觀測一標準差~first standard deviation'),('s2',4,'m','觀測二標準差~second standard deviation')],
  '(x1/s1**2+x2/s2**2)/(1/s1**2+1/s2**2)','m',
  '獨立無偏觀測可依變異數倒數加權，較小不確定度取得較大權重。融合不會自動修正共同偏差或地圖錯誤；如果兩個感測器實際共享同一來源，當成獨立資料就會過度自信，並把錯誤估計包裝成精準結果。~Independent unbiased observations can be weighted by inverse variance, giving more weight to lower uncertainty. Fusion does not automatically remove common bias or map errors. Treating two sensors that share a source as independent creates false confidence and can make an incorrect estimate appear precise.',
  '兩個獨立高斯無偏位置觀測，不含跨時間濾波與完整性保證。~Two independent Gaussian unbiased position observations, without temporal filtering or integrity assurance.',
  '以保留的獨立真值資料檢查殘差平均與分布，另測共同偏移時是否仍能被辨識。~Use held-out independent truth to examine residual mean and spread, then test whether a shared offset remains detectable.',
  '共同地圖誤差可讓兩感測器互相同意卻都錯，將相關性忽略會縮小不合理的信賴區間。~A common map error can make both sensors agree while both are wrong; ignored correlation yields unrealistically narrow confidence intervals.',
  '兩個感測器讀值一致就能保證融合位置正確~Agreement between two sensors guarantees a correct fused position.', 's2')
M('odometry', [('distance',1500,'m','行走距離~travelled distance'),('scale',0.004,'1','比例誤差~scale error'),('bias',0.2,'m','固定偏差~fixed offset')],
  'distance*scale+bias','m',
  '輪徑與脈衝換算比例的誤差會隨行走距離累積，固定零點偏差則不隨距離放大。輪滑與空轉使輪周距離不等於地面位移；定期地標校正能約束累積誤差，但地標本身的位置與辨識可信度仍須驗證。~Wheel diameter and pulse-scale error accumulate with distance, whereas a fixed zero offset does not grow. Slip makes wheel travel differ from ground displacement. Landmark updates can constrain drift, but the landmark position and identification credibility still require verification.',
  '固定比例誤差與固定偏移，未包含時變輪滑或輪徑磨耗歷程。~Constant scale error plus fixed offset; variable slip and wheel-wear history are not modelled.',
  '在多個已知距離區段繪製殘差對距離，利用斜率與截距分別估計比例及零點。~Plot residual against several known travel distances and use slope and intercept to separate scale and zero-offset effects.',
  '一次短距離校正可能掩蓋比例誤差，輪滑事件則在殘差曲線留下突跳而非固定斜率。~A short calibration run can hide scale error; slip events cause residual jumps rather than a constant slope.',
  '短距離校正準確就能保證長距離里程也完全準確~Accurate short-distance calibration guarantees perfectly accurate long-distance odometry.', 'distance')
M('sampling', [('v',25,'m/s','移動速度~motion speed'),('f',20,'Hz','取樣頻率~sampling frequency')],
  'v/f','m/sample',
  '固定時間取樣在移動系統中對應空間間隔，速度越高相同頻率越容易漏過狹窄特徵。時間戳抖動會讓空間取樣不均勻；提高取樣率仍需足夠感測頻寬與抗混疊處理，不能只增加資料列數。~Time sampling in a moving system corresponds to spatial spacing; at higher speed, the same rate can miss narrow features. Timestamp jitter makes spatial samples nonuniform. A higher rate still requires adequate sensor bandwidth and anti-alias filtering, rather than merely more rows of data.',
  '等速與等時間取樣的間距，不代表可以解析同樣大小的最小缺陷。~Spacing for constant speed and uniform sampling; it is not automatically the smallest resolvable defect size.',
  '對已知長度特徵以不同速度重播，檢查事件是否保留並比較位置內插誤差。~Replay a known-length feature at different speeds, check event retention, and compare position-interpolation error.',
  '高頻振動混疊成低頻漂移可能被誤判為幾何偏差，遺失時間戳也會破壞空間重建。~High-frequency vibration can alias into apparent low-frequency geometry drift; missing timestamps also corrupt spatial reconstruction.',
  '取樣頻率固定時不同速度的空間解析度也一定相同~Fixed sampling frequency gives identical spatial resolution at every speed.', 'v')
M('clock', [('drift',20,'ppm','時鐘頻率偏差~clock frequency offset'),('duration',3600,'s','未校時期間~unsynchronized interval')],
  'drift*1e-6*duration','s',
  '時鐘頻率偏差會隨時間累積成時間差，校時瞬間的偏移與之不同。多系統事件排序若依不同時鐘，可能把因果順序顛倒；校時跳變又會使量測區間長度失真，所以需記錄時鐘品質與校正事件。~Clock frequency error accumulates into time offset and differs from initial synchronization offset. Ordering multisystem events on different clocks can reverse apparent causality. Synchronization jumps can distort interval lengths, so clock quality and correction events must be recorded.',
  '固定頻率偏差的線性累積，忽略溫度漂移與校時伺服動態。~Linear accumulation at fixed frequency offset; temperature drift and synchronization-servo dynamics are omitted.',
  '用獨立時間基準比較多個時刻的偏移，從斜率分辨頻率誤差與一次性跳變。~Compare offsets at several times against an independent reference, using slope to distinguish frequency error from a one-time jump.',
  '只對齊開始時刻卻忽略頻率漂移，會讓長測試中的事件逐漸錯位，並誤判通訊延遲。~Aligning only the initial instant leaves frequency drift uncorrected, progressively misaligning events and suggesting false network delay.',
  '測試開始時時鐘一致就能保證整天時間戳都一致~Clocks aligned at test start remain aligned for the entire day.', 'duration')
M('queue', [('arrival',3.2,'persons/s','到達流率~arrival flow'),('service',2.6,'persons/s','離開流率~departure flow'),('duration',120,'s','觀察時間~observation duration')],
  '(arrival-service)*duration','persons',
  '排隊人數依流入減流出的守恆關係累積。平均服務能力若只略高於平均需求，瞬間車潮仍會形成等待；人群不能被無限壓縮，所以排隊長度會回堵上游樓梯或月台，改變原先假設的到達方式。~A queue accumulates according to inflow minus outflow. Even service capacity slightly above mean demand can be overwhelmed by a train-arrival pulse. People cannot be compressed indefinitely, so a growing queue can block upstream stairs or platforms and alter the assumed arrival process.',
  '固定流率、初始無排隊且流入大於流出；不含放棄、繞行及密度回饋。~Constant flows, initially empty queue and inflow above outflow; abandonment, rerouting and density feedback are excluded.',
  '同時數進入、離開與區內存量，以影像匿名計數或人工抽樣核對人數守恆。~Count entries, exits and occupancy together, using anonymous image counts or manual samples to verify conservation.',
  '只量出口通過量會看不到後方累積，感測器漏計還可能讓看似平衡的流率掩蓋真實回堵。~Exit throughput alone misses upstream accumulation; missed detections can hide real spillback behind apparently balanced flows.',
  '出口每秒通過人數穩定就能證明站內沒有排隊~Stable exit throughput proves that no queue is forming inside the station.', 'duration')
M('little', [('arrival',2,'persons/s','平均到達率~mean arrival rate'),('waiting',45,'s','平均停留時間~mean residence time')],
  'arrival*waiting','persons',
  '穩態平均存量等於平均到達率乘平均停留時間，這是流量與庫存的連結，不需要先指定排隊分布。它不能描述單一尖峰時刻，也不會告訴人群在空間上如何分布；量測窗若仍在快速累積，就不宜直接套用穩態關係。~Mean occupancy equals mean arrival rate times mean residence time in steady flow. This connects throughput and inventory without requiring a specific queue distribution. It does not describe one peak instant or spatial distribution, and a rapidly accumulating observation window does not satisfy the steady-state interpretation.',
  '穩態同一人群與同一系統邊界的長時間平均。~Long-run averages of the same population within one steady system boundary.',
  '使用一致進出邊界估計流率與停留時間，並與獨立區內人數平均值比對。~Estimate flow and residence time using consistent boundaries and compare with an independent mean occupancy count.',
  '把包含站外等待的停留時間乘上站內流率會混用邊界，造成存量高估或低估。~Combining residence time that includes an outside queue with an inside flow rate mixes boundaries and biases occupancy.',
  '平均人數關係能直接預測任何瞬間的最大擁擠程度~A mean occupancy relation directly predicts the maximum crowding at every instant.', 'waiting')
M('flow_width', [('width',2.4,'m','有效淨寬~effective clear width'),('specific',1.1,'persons/(m*s)','假想單位寬流率~hypothetical specific flow')],
  'width*specific','persons/s',
  '通道容量與有效淨寬有關，但扶手、門扇、行李及靠邊避讓會減少可用寬度。單位寬流率是情境參數，受方向、坡度與群體能力影響；多條通道的容量只有在下游沒有共同瓶頸時才能直接相加。~Passage capacity depends on effective clear width, reduced by rails, door leaves, luggage and edge avoidance. Specific flow is scenario dependent and varies with direction, slope and user capability. Parallel passage capacities may be added only when they do not share a downstream bottleneck.',
  '均勻單向流的教學係數，不是法定疏散容量或規範值。~Teaching coefficient for uniform one-way flow, not a statutory evacuation capacity or code value.',
  '量測最窄位置的有效淨寬，將各方向流量分開統計，檢查下游是否出現排隊。~Measure clear width at the narrowest section, count each travel direction separately, and inspect downstream queues.',
  '以建築軸線寬度代替淨寬會高估容量，出口匯流也可能讓上游兩條通道互相阻塞。~Using structural width instead of clear width overstates capacity; merging exits can make two upstream passages obstruct each other.',
  '兩條走道接到同一狹窄出口時容量仍可直接相加~Two corridors feeding one narrow exit always have directly additive capacity.', 'width')
M('density', [('people',180,'persons','區內人數~occupants'),('area',90,'m2','可站立面積~usable standing area')],
  'people/area','persons/m2',
  '平均密度是人數除以可用面積，設備、柱體與危險邊緣應從面積中扣除。相同平均密度可以包含完全不同的局部群聚；門口、扶梯出口與轉角的局部高密度，常比整個大廳平均值更能解釋行走速度下降。~Mean density divides people by usable area after excluding equipment, columns and unsafe edges. The same average can conceal very different local clustering. High density at doors, escalator landings or corners often explains reduced walking speed better than the average across a large concourse.',
  '靜態平均密度，不是擠壓力或個別人的安全風險模型。~Static mean density, not a crowd-pressure or individual-risk model.',
  '用網格分區計數比較平均與局部尖峰，記錄可用面積隨設備或圍籬變動的情況。~Count occupants in spatial cells, compare mean and local peaks, and record changes in usable area from equipment or barriers.',
  '將封閉區域算入面積會低估密度，遮蔽導致漏計又可能恰好發生在最擁擠的地方。~Including closed areas understates density; occlusion-related undercounting can be worst precisely where crowding is greatest.',
  '整個大廳平均密度低就能保證每個出口都不擁擠~A low concourse-average density guarantees that every exit is uncrowded.', 'area')
M('travel', [('distance',120,'m','行走距離~walking distance'),('speed',0.8,'m/s','假想步速~assumed walking speed'),('wait',35,'s','等待時間~waiting time')],
  'distance/speed+wait','s',
  '總旅行時間應同時計入移動與等待，不能只比較平面上的最短距離。坡道、門扇與轉乘決策都可能造成停頓；對行動受限旅客而言，較遠但連續可達的路徑往往比短而不連續的路徑更可用。~Travel time includes movement and waiting rather than plan distance alone. Ramps, doors and transfer decisions can introduce pauses. For a mobility-limited traveller, a longer continuously accessible route can be more usable than a shorter route containing an inaccessible interruption.',
  '定步速與固定等待的概念估算，未含煙氣、擁擠及協助需求分布。~Constant speed and fixed waiting; smoke, crowd interaction and distribution of assistance needs are omitted.',
  '分段記錄行走與等待，不以最快受試者代表所有旅客，並對照不同能力群體。~Record movement and waiting separately, avoid representing everyone by the fastest participant, and compare groups with different abilities.',
  '只量無人環境步行時間會低估轉乘負擔，電梯等待與路徑中斷可能主導總時間。~Uncrowded walking tests understate transfer burden when elevator waits or route interruptions dominate total time.',
  '平面圖上最短的路徑一定是每位旅客最快的路徑~The shortest route on a plan is always the fastest route for every passenger.', 'speed')
M('slope', [('rise',0.45,'m','高差~vertical rise'),('run',7.5,'m','水平長度~horizontal run')],
  'rise/run*100','percent',
  '坡度以高差除以水平長度定義，不能把斜面長度直接當分母。平均坡度之外還要檢查平台、橫坡與轉折，因為輪椅使用者在坡道終端需要轉向與停止的空間；符合一個幾何比值並不代表整條無障礙路徑連續可用。~Slope uses rise divided by horizontal run, not sloping surface length. Landings, cross-slope and transitions also matter because wheelchair users need space to turn and stop. Meeting one geometric ratio does not establish continuous usability of an accessible route.',
  '幾何教學值，不宣告符合任何司法區的坡道上限。~Geometric teaching value, without asserting compliance with a jurisdictional ramp limit.',
  '以同一高程基準量端點，再沿行走路徑抽測局部坡度、橫坡與平台平整度。~Survey endpoints on one elevation datum, then sample local slope, cross-slope and landing level along the route.',
  '兩端平均坡度合格仍可能隱藏短距離陡坡，排水沉陷又可能造成輪椅偏向。~An acceptable endpoint average can hide a short steep segment, while drainage settlement can introduce a destabilizing cross-slope.',
  '只要坡道平均坡度適當就不用檢查平台與橫坡~An acceptable mean ramp slope removes the need to check landings and cross-slope.', 'run')
M('gap_budget', [('track',8,'mm','軌道偏移界~track offset bound'),('body',10,'mm','車體位移界~body displacement bound'),('survey',3,'mm','測量誤差界~survey error bound')],
  'track+body+survey','mm',
  '月台與車體介面的間隙預算需分開列入軌道幾何、懸吊移動與測量誤差。保守界限可直接相加，而隨機誤差合成必須有分布與相關性證據；只在空車靜止狀態量一個間隙，無法代表載重與動態情境。~A platform-vehicle gap budget separates track geometry, suspension movement and survey error. Conservative bounds can be summed, while stochastic combination requires evidence for distributions and correlation. One stationary empty-vehicle measurement cannot represent loaded and dynamic conditions.',
  '三項同向有界誤差的保守和，不是法定間隙允收值。~Conservative sum of three same-direction bounded errors, not a statutory gap allowance.',
  '建立共同座標，對空載、載重及不同車型分別量測，並保留各誤差來源的符號。~Establish one coordinate system, measure empty and loaded vehicles of each type, and retain signs of individual error sources.',
  '把最大值當成標準差再作均方根合成會失去保守性，基準點沉陷也會造成整排讀值偏移。~Treating maxima as standard deviations and applying root-sum-square loses conservatism; datum settlement can bias the whole measurement row.',
  '三個最大誤差都可直接用均方根方式縮小總界限~Three maximum error bounds may always be reduced through root-sum-square combination.', 'body')
M('rss', [('s1',3,'mm','獨立誤差一標準差~first independent standard deviation'),('s2',4,'mm','獨立誤差二標準差~second independent standard deviation')],
  'sqrt(s1*s1+s2*s2)','mm',
  '獨立零均值誤差的變異數可以相加，因此標準差以平方和開根號合成。這個做法不適合直接合併最大容差或共同偏差；一旦共享基準造成相關性，協方差項就必須回到計算中，不能繼續假裝量測彼此獨立。~Variances of independent zero-mean errors add, giving a root-sum-square standard deviation. This is not a way to combine maximum tolerances or common bias. When a shared datum creates correlation, covariance terms belong in the calculation rather than assuming continued independence.',
  '獨立隨機標準差，不代表確定的最大偏移界。~Independent random standard deviations, not a deterministic maximum displacement bound.',
  '以重複量測估計標準差與相關係數，將固定偏差另列，再核對合成殘差。~Estimate standard deviations and correlation from repeated observations, separate fixed bias, and compare combined residuals.',
  '共同基準誤差會使所有讀值同向偏移，重複次數增加也無法把這種偏差平均掉。~A common datum error shifts readings together, and additional repetition cannot average away that shared bias.',
  '任何兩個誤差都可以不問相關性直接平方和開根號~Any two errors can be combined by root-sum-square without considering correlation.', 's1')
M('ventilation', [('Q',32,'m3/s','體積流量~volume flow'),('A',16,'m2','有效通風面積~effective airflow area')],
  'Q/A','m/s',
  '平均風速是流量除以有效斷面，局部阻塞與流場分離可讓同一平均值對應很不均勻的速度。風向與煙氣來源位置同樣重要；正常通風的舒適性目標和火災時的煙流控制目標不能共用一個數字就視為完成驗證。~Mean air speed is flow divided by effective area, but obstruction and separation can produce highly nonuniform fields at the same mean. Direction and smoke-source location also matter. Normal comfort ventilation and emergency smoke control cannot be validated by one shared number alone.',
  '不可壓縮均勻截面平均，未求解火災浮力、毒性或能見度。~Incompressible cross-section mean; fire buoyancy, toxicity and visibility are not solved.',
  '在斷面多點量測速度與方向，積分得到流量，再檢查門開閉或列車位置變化。~Measure velocity and direction at several section points, integrate flow, and repeat for changed door or train positions.',
  '單點風速可剛好量到高速射流而高估全斷面流量，反向區域也可能被平均抵消。~One sensor may sample a fast jet and overstate total flow; reverse-flow regions can disappear in an unsigned average.',
  '一個測點風速符合目標就能證明整個煙流場符合需求~One velocity reading at target proves that the entire smoke-flow field meets requirements.', 'A')
M('fan_power', [('Q',40,'m3/s','流量~flow'),('dp',600,'Pa','總壓升~total pressure rise'),('eta',0.7,'1','總效率~overall efficiency')],
  'Q*dp/eta/1000','kW',
  '風機輸入功率由流量乘壓升再除效率估算。壓力不足與流路阻力增加都會改變工作點，不能把銘牌額定流量視為任何風道中都能達成；備援風機還可能共享同一阻塞路徑而無法提供預想的獨立能力。~Fan input power is flow times pressure rise divided by efficiency. Inadequate pressure and increased duct resistance shift the operating point; nameplate flow is not guaranteed in every duct. Redundant fans may also share a blocked path and fail to provide the expected independent capability.',
  '單一穩態工作點，未含風機曲線、失速或高溫效率變動。~One steady operating point without fan-curve shape, stall or high-temperature efficiency change.',
  '同時量測流量、前後壓差與電功率，對照風門位置並檢查各項能量是否一致。~Measure flow, pressure rise and electrical power together, correlate with damper position, and check energy consistency.',
  '風門位置回授正常但機械連桿脫落會形成錯誤狀態，僅看馬達運轉訊號無法證明有足夠送風。~A detached damper linkage can coexist with apparently normal position feedback; a motor-running signal does not prove adequate airflow.',
  '風機馬達正在轉動就表示所需通風量一定已達成~A running fan motor proves that the required airflow has been achieved.', 'dp')
M('pressure', [('rho',1.2,'kg/m3','空氣密度~air density'),('v',15,'m/s','代表風速~representative air speed')],
  '0.5*rho*v*v','Pa',
  '動壓與風速平方成正比，這有助判斷列車活塞作用與門扇負載的量級。實際瞬變壓力仍受隧道阻塞率、旁通開口與波傳反射影響；動壓不是任何測點必定出現的靜壓差，兩者不能直接等同。~Dynamic pressure scales with speed squared, helping estimate the magnitude of train-induced airflow and door loading. Actual transients also depend on blockage, bypass openings and wave reflections. Dynamic pressure is not automatically the static pressure difference measured at a particular location.',
  '低馬赫數局部量級估算，不是全隧道壓力波解。~Local low-Mach-number scale estimate, not a tunnel-wide pressure-wave solution.',
  '同步量測列車速度、局部風速與兩側靜壓，觀察峰值時刻及符號是否相符。~Synchronize train speed, local air speed and static pressure on both sides, comparing peak timing and sign.',
  '把測壓管朝向流動形成的總壓誤當靜壓會高估門扇負載，時間平均又可能掩蓋短暫峰值。~A probe facing the flow can measure total rather than static pressure and overstate door loading; time averaging can hide transient peaks.',
  '風速加倍時動壓也只會跟著加倍~Doubling air speed merely doubles dynamic pressure.', 'v')
M('orifice', [('Cd',0.65,'1','流量係數~discharge coefficient'),('A',4,'m2','開口面積~opening area'),('dp',80,'Pa','兩側壓差~pressure difference'),('rho',1.2,'kg/m3','空氣密度~air density')],
  'Cd*A*sqrt(2*dp/rho)','m3/s',
  '開口通風量由壓差驅動，受面積與縮流損失共同控制。流量和壓差平方根成正比，不是線性比例；旁通開口增加可能減輕壓力卻同時改變煙氣路徑，因此開口位置和通風模式必須一起討論。~Pressure difference drives opening flow, with area and contraction losses jointly controlling it. Flow scales with the square root of pressure rather than linearly. Adding a bypass can relieve pressure while changing smoke paths, so location and ventilation mode must be considered together.',
  '固定流量係數的不可壓縮孔口近似，未含雙向分層流。~Incompressible orifice approximation with fixed coefficient; bidirectional stratified flow is excluded.',
  '量測開口兩側壓差與斷面流量，將不同開度下的結果畫成流量對壓差平方根。~Measure pressure difference and section flow, then plot flow against square-root pressure for several openings.',
  '格柵堵塞會改變有效面積與損失係數，僅看風門命令開度可能誤判實際旁通能力。~Blocked grilles alter effective area and loss coefficient; commanded damper opening can misrepresent actual bypass capacity.',
  '開口壓差增加四倍時流量一定增加四倍~Quadrupling pressure difference necessarily quadruples opening flow.', 'dp')
M('evacuation', [('people',600,'persons','待疏散人數~evacuating population'),('width',2.5,'m','有效出口寬~effective exit width'),('flow',0.9,'persons/(m*s)','假想比流率~assumed specific flow'),('travel',110,'s','代表行走時間~representative travel time'),('response',45,'s','反應時間~response time')],
  'response+travel+people/(width*flow)','s',
  '疏散估算需把察覺反應、移動與出口服務分開。此處串接估算保守地把行走和排隊相加，實際兩者可重疊；火災分析還要比較可用安全時間、煙氣與群體差異，不能只由一個清空時間判定生命安全。~Evacuation estimates separate recognition/response, movement and exit service. This serial estimate conservatively adds travel and queuing, which can overlap in reality. Fire assessment must also consider available safe time, smoke and population differences; one clearance time cannot establish life safety.',
  '原創串行教學模型，非規範認可疏散驗證，也未估可用安全疏散時間。~Original serial teaching model, not code-approved egress verification; available safe egress time is not estimated.',
  '以不造成擁擠的受控演練校對各時間段，逐項保留行動受限者與協助程序的差異。~Use controlled non-crowding exercises to check timing components and retain differences for assisted and mobility-limited users.',
  '把預先知道演練的反應時間套到真實事件會低估延誤，忽略封閉出口又會高估容量。~Using reaction times from announced drills understates real-event delay; ignoring an unavailable exit overstates capacity.',
  '算出疏散清空時間就足以單獨證明火災時絕對安全~A calculated evacuation clearance time alone proves absolute fire safety.', 'people')
M('illuminance', [('flux',2400,'lm','光通量~luminous flux'),('util',0.45,'1','利用係數~utilization factor'),('area',24,'m2','受照面積~illuminated area')],
  'flux*util/area','lx',
  '平均照度由到達工作面的光通量除以面積估算，但光學分布決定暗點是否存在。煙氣、污損與電池老化可能同時降低可見性；指示方向、對比與旅客視力也會影響辨識，不能只用燈具是否亮著作為完成檢核。~Mean illuminance divides useful luminous flux by area, but optical distribution determines dark spots. Smoke, dirt and battery ageing can reduce visibility together. Directional cues, contrast and eyesight affect recognition, so a lamp being on is not a complete verification.',
  '均勻平均照度估算，未模擬煙氣散射或法定最低照度。~Uniform mean-illuminance estimate without smoke scattering or statutory minimum values.',
  '以網格量測平面照度並尋找最低點，對照電池放電前後與不同觀看方向。~Measure illuminance on a grid, identify minima, and compare before/after battery discharge and different viewing directions.',
  '亮度集中在燈具下方可能留下暗區，指示牌反光也可降低遠距離的有效對比。~Light concentrated beneath fixtures leaves dark regions; sign glare can also reduce effective contrast at a distance.',
  '照明平均值足夠就保證所有角落都能清楚辨識出口~Adequate mean lighting guarantees clear exit recognition at every corner.', 'flux')
M('battery', [('capacity',80,'Ah','額定容量~rated capacity'),('voltage',24,'V','標稱電壓~nominal voltage'),('fraction',0.7,'1','可用比例~usable fraction'),('load',350,'W','固定負載~constant load')],
  'capacity*voltage*fraction/load','h',
  '電池續航以可用能量除以負載估算，容量不能只看安培小時而忽略電壓。溫度、老化、放電速率與截止電壓都影響可用比例；緊急供電還需檢查負載啟動尖峰，平均能量充足不代表瞬間電壓不會崩落。~Battery duration divides usable energy by load, so ampere-hours alone are insufficient without voltage. Temperature, ageing, discharge rate and cutoff affect usable fraction. Emergency supply must also handle starting surges; sufficient average energy does not guarantee stable instantaneous voltage.',
  '定電壓定負載近似，未含電池非線性放電與溫度效應。~Constant-voltage constant-load approximation; nonlinear discharge and temperature effects are excluded.',
  '量測完整負載曲線與最低端電壓，分別核對連續能量及啟動瞬間壓降。~Measure the load profile and minimum terminal voltage, checking continuous energy and startup sag separately.',
  '老化電池可能保有部分容量但內阻升高，啟動負載時掉壓使設備提早中止。~An aged battery may retain some capacity while internal resistance rises, causing early shutdown during a starting load.',
  '只要安培小時數相同任何兩種電池續航就一定相同~Equal ampere-hour ratings guarantee equal runtime for any two batteries.', 'load')
M('heat', [('P',900,'W','持續發熱~continuous heat'),('Rth',0.035,'K/W','等效熱阻~equivalent thermal resistance'),('ambient',30,'degC','環境溫度~ambient temperature')],
  'ambient+P*Rth','degC',
  '穩態溫升由發熱乘等效熱阻決定，散熱路徑和熱源功率同樣重要。風道阻塞、接觸面鬆動與環境升溫都可能造成相同的最高溫度；若只換大風機而不追蹤熱路，可能改善外殼卻讓內部熱點繼續惡化。~Steady temperature rise equals heat generation times thermal resistance, making heat paths as important as source power. Blocked airflow, loose interfaces and warmer ambient conditions can produce similar maxima. A larger fan may cool the enclosure while an internal hotspot continues to worsen.',
  '單節點線性穩態熱阻模型，未解析空間熱點與瞬態熱容。~Single-node linear steady thermal-resistance model without spatial hotspots or transient heat capacity.',
  '同時記錄功率、環境與多點溫度，改變一項邊界條件以辨認熱源與熱阻變化。~Record power, ambient and several temperatures together, changing one boundary to distinguish source and resistance changes.',
  '環境感測器放在熱排氣中會把自身熱源誤當室溫升高，遮蔽熱點又會低估最大元件溫度。~An ambient sensor in hot exhaust mistakes self-heating for room temperature rise, while hidden hotspots understate component maxima.',
  '外殼溫度正常就能證明所有內部元件都沒有過熱~A normal enclosure temperature proves that every internal component is free from overheating.', 'Rth')
M('lifting', [('m',18000,'kg','總吊升質量~lifted mass'),('g',9.81,'m/s2','重力加速度~gravity'),('points',4,'points','承載點數~support count'),('factor',1.15,'1','教學動態倍率~teaching dynamic factor')],
  'm*g*factor/points/1000','kN/point',
  '平均吊點反力來自總重量分配，但實際分力受重心位置、支承剛度與同步誤差控制。動態倍率只是概念帳項，不能取代設備認證；把總能力除以吊點數也無法證明最不利吊點仍有足夠承載餘裕。~Mean lifting reaction follows total load distribution, while actual reactions depend on centre of gravity, support stiffness and synchronization error. A dynamic factor is a conceptual accounting term, not equipment certification. Dividing total rating by support count does not establish margin at the most heavily loaded point.',
  '對稱均分載重與假想動態倍率，非吊裝方案或設備額定能力。~Symmetric equal load sharing with an assumed dynamic factor, not a lifting plan or equipment rating.',
  '在縮尺或空載試驗台核對各點高度與負載，逐步施加偏心以觀察反力重新分配。~On a scale or unloaded test rig, compare support heights and loads, then introduce eccentricity to observe reaction redistribution.',
  '一個吊點不同步會把載重移往其他支承，總載重不變也可能局部超載並扭曲車體。~A lagging support transfers load to others; unchanged total weight can still produce local overload and body distortion.',
  '總起重能力足夠就能保證每個吊點都不會超載~Adequate total lifting capacity guarantees that no individual support is overloaded.', 'm')
M('eccentric', [('W',200,'kN','總載重~total load'),('L',4,'m','支承間距~support spacing'),('e',0.4,'m','重心偏心~centre-of-gravity eccentricity')],
  'W*(0.5+e/L)','kN',
  '兩支承反力由力與力矩平衡同時決定。重心偏向一側時，該側反力增加而另一側減少，總和仍不變；平均反力看似充足不能掩蓋單側限制，支承接觸若脫離還會改變原先的邊界條件。~Two support reactions follow both force and moment equilibrium. Moving the centre of gravity toward one support raises that reaction while reducing the other without changing the total. Adequate mean reaction cannot hide a local limit, and loss of contact changes the assumed boundary conditions.',
  '剛體兩簡支靜力模型且兩支承保持接觸，忽略動態擺動。~Rigid body on two simple supports that remain in contact, neglecting dynamic swing.',
  '核對兩反力之和與各自力矩，再以已知小偏心移動驗證量測方向與零點。~Check the reaction sum and moments, then apply a known small eccentricity to verify sensor direction and zero.',
  '把幾何中心當成重心會錯估分力，支承沉陷或接觸鬆脫又可能使靜力模型失效。~Confusing geometric centre with centre of gravity misallocates load; settlement or loose contact can invalidate the static model.',
  '總重量不變時左右支承的載重也一定不變~Unchanged total weight guarantees unchanged load at each support.', 'e')
M('hydraulic', [('p',12,'MPa','油壓~hydraulic pressure'),('A',0.008,'m2','活塞面積~piston area'),('eta',0.9,'1','力傳遞效率~force-transfer efficiency')],
  'p*1e6*A*eta/1000','kN',
  '液壓推力由壓力乘有效活塞面積決定，回程側面積與背壓可能不同。壓力達標並不保證位移同步，漏油、氣泡和摩擦會改變動作；安全承載還需獨立機械保持機制與設備規定，不能只依賴壓力表。~Hydraulic force follows pressure times effective piston area, with different return-side area and back pressure possible. Target pressure does not guarantee synchronized movement because leakage, air and friction affect motion. Safe support also requires specified holding mechanisms rather than dependence on a pressure gauge alone.',
  '單一活塞準靜態推力，未含背壓、管路瞬變與額定安全係數。~Quasistatic force of one piston; back pressure, line transients and rated safety factors are excluded.',
  '以獨立力感測器核對壓力推算，並記錄停留時的位移漂移與油溫變化。~Compare pressure-derived force with an independent load cell and record displacement drift and oil temperature during holding.',
  '內洩漏可造成保持位置下降但壓力讀值短時正常，空氣混入則可能使動作變軟並延遲。~Internal leakage can cause sag despite temporarily normal pressure, while entrained air makes motion compliant and delayed.',
  '油壓讀值正常就能單獨保證負載永遠保持原位~A normal hydraulic pressure reading alone guarantees that the load remains fixed indefinitely.', 'p')
M('sync_error', [('v1',0.012,'m/s','升降端一速度~first lift speed'),('v2',0.0115,'m/s','升降端二速度~second lift speed'),('t',20,'s','動作時間~motion time')],
  '(v1-v2)*t*1000','mm',
  '小速度差會累積成高度差，長行程時尤其明顯。位置閉迴路可以限制累積，但感測器基準、通訊延遲和負載差異仍會影響同步；比較瞬間馬達轉速相同，並不足以證明各吊點的實際高度相同。~A small speed difference accumulates into height mismatch, particularly over long travel. Position feedback can limit drift, but sensor references, communication delay and unequal loading still affect synchronization. Equal instantaneous motor speeds do not establish equal actual support heights.',
  '定速度差的運動學模型，未含閉迴路補償與結構柔度。~Kinematic model with constant speed difference; feedback correction and structural compliance are excluded.',
  '用獨立高程量測核對兩端位置，分別比較空載與偏載情境的誤差累積斜率。~Check both positions with independent elevation measurement and compare drift slopes for unloaded and eccentric-load scenarios.',
  '共同位置零點錯誤可能讓控制器以為同步，車體卻已傾斜；某端摩擦突增則會出現斜率轉折。~A shared zero-reference error can make the controller report synchronization while the body tilts; increased friction at one end changes the drift slope.',
  '兩個馬達當下轉速相同就代表兩端高度永遠相同~Equal instantaneous motor speeds mean that both heights are always identical.', 't')
M('cut_speed', [('D',0.84,'m','輪徑~wheel diameter'),('rpm',60,'rev/min','轉速~rotational speed')],
  'pi*D*rpm','m/min',
  '切削線速度由輪徑與轉速共同決定，相同轉速在不同直徑會造成不同刀具接觸條件。輪對鏇削還要考慮夾持剛度、材料硬點和輪廓基準；把工具轉速設定正確，並不能保證完成後輪廓與同軸度符合需求。~Cutting surface speed depends on diameter and rotational speed, so the same rotation rate produces different tool conditions on different wheels. Reprofiling also depends on clamping stiffness, hard spots and profile reference. Correct speed setting does not by itself establish final profile or concentricity.',
  '幾何線速度換算，未指定刀具材料或實際切削參數。~Geometric surface-speed conversion without specifying tool material or production cutting settings.',
  '以實際輪徑核對轉速回授，將加工前後的輪廓掃描、圓度與刀具磨耗分開記錄。~Check rotation feedback against measured diameter and record pre/post profile, roundness and tool wear separately.',
  '以標稱輪徑代替磨耗後直徑會錯估速度，輪面滑動則使驅動滾輪轉速不再代表輪對轉速。~Nominal instead of worn diameter biases speed; roller slip makes drive-roller rotation differ from wheelset rotation.',
  '輪徑改變時固定轉速仍會維持相同切削線速度~Fixed rotational speed maintains the same cutting speed when wheel diameter changes.', 'D')
M('diameter_loss', [('D0',840,'mm','原始輪徑~initial diameter'),('depth',1.5,'mm','單側徑向去除~radial removal per side')],
  'D0-2*depth','mm',
  '徑向切深在直徑上會出現兩倍的減少，輪徑耗用應與可維修壽命一起追蹤。修掉一處缺陷所需的最小去除量可能決定整個輪對的加工深度；只追求表面光滑而忽略剩餘輪緣與直徑，可能提早耗盡零件壽命。~Radial removal reduces diameter by twice the cut depth, so diameter consumption belongs in life tracking. The removal needed for one defect may govern the entire wheelset. Optimizing surface appearance while ignoring remaining flange and diameter can consume useful life prematurely.',
  '同心均勻去除的幾何帳，不包含輪廓規範或最小使用輪徑。~Geometric accounting for concentric uniform removal; profile rules and minimum service diameter are not specified.',
  '用獨立量具比對加工前後直徑，將每次去除量累積到輪對履歷並核對輪廓基準。~Compare before/after diameters with an independent gauge and accumulate removal in wheelset history while checking profile datums.',
  '把徑向去除誤當直徑去除會少算一倍耗用量，量具零點偏差又可能讓兩側輪徑差被隱藏。~Confusing radial and diametral removal understates consumption by a factor of two; gauge zero error can hide a side-to-side difference.',
  '切去一毫米徑向材料時輪徑也只會減少一毫米~Removing one millimetre radially reduces diameter by only one millimetre.', 'depth')
M('material_rate', [('width',6,'mm','加工寬度~cutting width'),('depth',0.4,'mm','切入厚度~cut thickness'),('feed',100,'mm/s','相對進給速度~relative feed speed')],
  'width*depth*feed','mm3/s',
  '體積去除率由截面乘相對進給估算，能用來連結節拍、切屑與能量需求。增加去除率會同時提高熱與力的負擔，實際效果受刀具、材料與剛度限制；縮短加工時間若造成重工，總維修週期反而可能增加。~Volumetric removal rate is cross-sectional area times relative feed, linking cycle time, chips and energy demand. Higher removal increases thermal and mechanical loading, limited by tooling, material and stiffness. A shorter cut can lengthen the total maintenance cycle when it creates rework.',
  '矩形切屑截面的概念估算，非輪廓加工刀路與實際參數建議。~Conceptual rectangular chip section, not an actual reprofiling tool path or production setting.',
  '比較去除前後體積與切屑收集量，將停頓、量測與重工時間納入完整節拍。~Compare removed volume with collected chips and include pauses, measurements and rework in total cycle time.',
  '只記刀具接觸時間會低估設備占用，刀具磨耗造成去除率下降也可能被程序時間掩蓋。~Recording only tool-contact time understates equipment occupation; tool wear can reduce removal rate without appearing in nominal program duration.',
  '切削速度提高就能保證整個維修週期必定縮短~Increasing cutting speed guarantees a shorter overall maintenance cycle.', 'feed')
M('water_use', [('flow',0.003,'m3/s','噴洗總流量~total spray flow'),('duration',180,'s','噴洗時間~spray duration'),('recycle',0.75,'1','回收再用比例~reused fraction')],
  'flow*duration*(1-recycle)*1000','L',
  '補充清水量取決於總噴洗量與可再用比例，回收水的品質限制和總量限制必須同時滿足。污泥、油脂與清潔劑會改變處理需求；回收率提高不一定等於清洗品質提高，也不能將所有排放都假設成可再用水。~Freshwater makeup depends on spray volume and reusable fraction, subject to both quality and quantity constraints. Sludge, oils and detergents alter treatment needs. Higher recovery is not necessarily better cleaning, and not every discharge can be assumed reusable.',
  '固定流量與固定回收率，忽略蒸發、帶出水與濃度累積的細部分配。~Fixed flow and reuse fraction; evaporation, carry-out and detailed concentration buildup are omitted.',
  '以進水、回流水與排放水三支表做水量平衡，另驗濁度與清潔劑殘留。~Balance makeup, return and discharge meters, then test turbidity and detergent residue independently.',
  '回收管漏水會使計算比例看似良好但耗水上升，污染累積則可能使高回收率降低清洗效果。~A leaking return line can increase consumption despite apparent recovery; contaminant accumulation can worsen cleaning at high reuse.',
  '回收比例越高就能保證清洗效果一定越好~A higher recycling fraction always guarantees better cleaning performance.', 'recycle')
M('dose', [('volume',800,'L','處理水量~treated water volume'),('concentration',0.002,'kg/L','目標教學濃度~assumed teaching concentration')],
  'volume*concentration','kg',
  '配藥量必須以有效處理水量和濃度定義為基礎，質量濃度與體積百分比不能互換。回收水已有殘留物時，追加量不等於全量新配；混合不均與接觸時間不足也會讓平均濃度正常卻有局部清洗差異。~Dosing depends on treated volume and concentration definition; mass concentration and volume percent are not interchangeable. Recycled water already containing residue needs an incremental rather than full fresh dose. Poor mixing or insufficient contact time can cause local differences despite a correct mean concentration.',
  '純質量平衡教學，不指定實際清潔化學品或使用濃度。~Mass-balance teaching only; no real cleaning chemical or operating concentration is prescribed.',
  '核對濃度單位與有效成分比例，在不同槽位取樣檢查混合均勻度。~Check concentration units and active fraction, then sample several tank locations to examine mixing uniformity.',
  '把商品原液質量當成有效成分質量會配錯比例，感測器污染又可能造成濃度回授偏差。~Treating product mass as active-component mass misdoses the solution; a fouled sensor can bias concentration feedback.',
  '相同數字的質量百分比與體積百分比一定完全相同~The same numerical mass percentage and volume percentage are always equivalent.', 'volume')
M('potential', [('m',70000,'kg','車輛質量~vehicle mass'),('g',9.81,'m/s2','重力加速度~gravity'),('h',1.2,'m','下降高度~vertical drop')],
  'm*g*h/1000','kJ',
  '位能下降可轉成動能與耗散，質量同時影響可用能量和需要消散的能量。駝峰調速的速度結果還受滾動阻力、風與車輛狀態影響；只用高度差決定目標速度會漏掉路徑上的持續損失與偶發阻力。~Lost gravitational energy becomes kinetic energy and dissipation. Mass affects both available and required dissipated energy. Hump-yard speed also depends on rolling resistance, wind and vehicle condition. Height drop alone cannot determine final speed without accounting for losses along the path.',
  '重力位能帳，未計真實場站阻力、風與調速設備控制。~Gravitational energy accounting without real yard resistance, wind or retarder control.',
  '以縮尺斜面比較同高度與不同阻力表面的末速，記錄能量差而非只看是否滑動。~Use a scale incline to compare final speeds at equal drop but different resistance, recording the energy difference rather than merely motion.',
  '低阻車輛可能比預測更快，輪軸阻力增加則可能停在途中，兩者都不能靠平均車重辨認。~A low-resistance wagon can exceed the predicted speed, while increased bearing resistance can stop it early; average mass cannot distinguish either condition.',
  '下降高度一樣就能保證所有貨車得到相同末速度~Equal height drop guarantees equal final speed for all freight wagons.', 'h')
M('retarder', [('m',70000,'kg','車輛質量~vehicle mass'),('v0',5,'m/s','初速~initial speed'),('v1',2,'m/s','末速~final speed'),('length',18,'m','耗能距離~dissipation distance')],
  '0.5*m*(v0*v0-v1*v1)/length/1000','kN',
  '所需平均耗能力可由動能差除以作用距離估算，初速平方使高速偏差特別敏感。平均力不是峰值力，也不會描述濕滑、延遲和接觸分布；調速結果必須同時檢查能量帳、末速與沿程減速度。~Required mean dissipating force follows kinetic-energy change divided by distance, making high initial-speed errors particularly influential. Mean force is not peak force and does not describe wet contact, delay or force distribution. Verification needs energy, exit speed and deceleration along the path together.',
  '平直路徑與定等效耗能，不包含實際編組場操作參數。~Level path and constant equivalent dissipation, without real hump-yard operating settings.',
  '在離線模型比較能量積分與末速度，將接觸延遲及作用長度誤差各自改變。~In an offline model, compare integrated energy with exit speed and vary contact delay and effective length independently.',
  '作用延遲縮短有效距離時，即使平均接觸力沒變也可能留下過高末速；速度感測偏差會誤導診斷。~Delayed action shortens effective distance and raises exit speed despite unchanged contact force; biased speed sensing can obscure the cause.',
  '耗能設備平均力相同就能保證所有進入速度的末速相同~Equal mean retarding force gives the same exit speed for every entry speed.', 'v0')
M('cycle', [('lift',35,'s','吊升時間~hoisting time'),('travel',50,'s','橫移時間~travel time'),('lower',30,'s','下降時間~lowering time'),('align',25,'s','對位時間~alignment time')],
  '3600/(lift+travel+lower+align)','moves/h',
  '吊運節拍需包含吊升、移動、下降與對位等完整工作，而不是只看最快的馬達行程。部分動作可以重疊，但前提是設備允許且不增加碰撞或擺動；空返、等待車輛與查驗也可能使實際吞吐低於理想循環率。~Handling cycle time includes hoisting, travel, lowering and alignment rather than the fastest motor movement alone. Some motions can overlap only when permitted and without increasing collision or sway. Empty returns, vehicle waiting and inspections can reduce throughput below the ideal cycle rate.',
  '單設備串行理想循環，未含等待、空返或安全聯鎖延遲。~Ideal serial cycle for one machine, excluding waiting, empty returns and interlock delays.',
  '逐動作記錄起訖與等待原因，把理想循環率和整班實際完成量分開報告。~Timestamp every motion and waiting cause, reporting ideal cycle rate separately from completed moves over a shift.',
  '忽略空返會高估吞吐，作業區交通互相阻塞則使設備利用率高但有效完成量低。~Ignoring empty returns overstates throughput; yard traffic conflicts can yield high equipment utilization with low useful completion.',
  '吊車馬達速度提高一倍場站吞吐就必定提高一倍~Doubling crane motor speed necessarily doubles terminal throughput.', 'align')
M('sway', [('length',8,'m','吊索有效長度~effective suspension length'),('g',9.81,'m/s2','重力加速度~gravity')],
  '2*pi*sqrt(length/g)','s',
  '小角度吊重擺動近似單擺，週期主要受吊索長度影響而非質量。移動命令若與擺動相位不合，停止後仍會持續擺盪；反擺控制需知道有效長度和感測延遲，不能只把速度降到零就視為吊具已穩定。~Small-angle suspended-load sway approximates a pendulum, with period governed mainly by suspension length rather than mass. Poorly phased travel commands leave residual sway after stopping. Anti-sway control needs effective length and sensing delay; zero travel speed does not mean a stable load.',
  '質點、無阻尼、小角度單擺，不含雙擺與柔性吊具。~Undamped small-angle point-mass pendulum without double-pendulum or flexible-spreader effects.',
  '在縮尺吊具量測停止後的擺動週期，改變長度而保持其他條件比較平方根關係。~Measure residual-sway period on a scale rig, varying length while holding other conditions fixed to test square-root scaling.',
  '吊索長度估錯會讓抑擺脈衝相位偏移，雙擺模態則可能讓單一週期辨識不足。~Incorrect suspension length misphases anti-sway pulses; double-pendulum modes can defeat a single-period estimate.',
  '吊重質量加倍就一定使小角度單擺週期加倍~Doubling suspended mass necessarily doubles the small-angle pendulum period.', 'length')
M('thermal_stress', [('E',210000,'MPa','彈性模數~Young modulus'),('alpha',0.000012,'1/K','線膨脹係數~thermal expansion coefficient'),('dT',25,'K','相對無應力溫差~change from stress-free temperature')],
  'E*alpha*dT','MPa',
  '完全軸向拘束的熱應力大小由彈性模數、膨脹係數與溫差相乘得到，加熱時是壓應力。實際鋼軌可能滑移並透過扣件與道床重新分配作用；量得總應變必須分離熱應變與機械應變，才能推論應力。~The magnitude of thermal stress under complete axial restraint is modulus times expansion coefficient times temperature change; heating produces compression. Real rail can slip and redistribute force through fasteners and ballast. Total measured strain must be separated into thermal and mechanical components before inferring stress.',
  '線彈性、單軸完全拘束且均勻溫升；未分析軌道挫屈或接頭。~Linear-elastic fully restrained uniaxial uniform heating; track buckling and joints are not analysed.',
  '同步量測軌溫與應變，使用獨立參考方法或已知拘束試件檢查溫度補償與零點。~Record rail temperature and strain together and use an independent reference or known-restraint specimen to check thermal compensation and zero.',
  '把總應變直接乘彈性模數可能把自由熱膨脹誤當機械應力，感測器脫膠則會低估變化。~Multiplying total strain by modulus can misinterpret free thermal expansion as mechanical stress; sensor debonding can suppress the response.',
  '任何溫度造成的總應變都可以直接乘彈性模數求應力~Any total thermally induced strain can be multiplied directly by modulus to obtain stress.', 'dT')
M('thermal_length', [('L',30,'m','構件長度~member length'),('alpha',0.000012,'1/K','膨脹係數~expansion coefficient'),('dT',20,'K','溫度變化~temperature change')],
  'L*alpha*dT*1000','mm',
  '自由熱伸長與原長、膨脹係數及溫差成正比，但受拘束後伸長會被轉成內力。接縫、支承與鄰接構件共同決定這種轉換；因此同一個溫差可能在自由端表現為位移，在固定端表現為應力，不能用一種量測代替另一種。~Free thermal expansion scales with length, coefficient and temperature change, while restraint converts some expansion into force. Joints, supports and adjoining members govern that conversion. The same temperature change can produce movement at a free end and stress at a restrained end, so one measurement cannot replace the other.',
  '均勻溫度與自由伸長；不包含熱梯度引起的彎曲。~Uniform temperature and free expansion; thermal-gradient bending is omitted.',
  '以多點溫度檢查均勻假設，再對照端點位移與支承狀態，分辨自由與拘束行為。~Check temperature uniformity at several points and compare end movement with support condition to distinguish free and restrained behaviour.',
  '支承卡住可能讓位移很小但內力增加，日照溫差又可能造成彎曲而非單純伸長。~A seized support can suppress movement while increasing force; solar gradients may cause bending rather than simple extension.',
  '量不到熱伸長就表示構件完全沒有熱應力~No measured thermal expansion means that a member has no thermal stress.', 'L')
M('strain_gauge', [('strain',400,'microstrain','機械應變~mechanical strain'),('GF',2.1,'1','應變規係數~gauge factor'),('V',5,'V','橋路激勵~bridge excitation')],
  'V*GF*strain*1e-6/4*1000','mV',
  '四分之一橋路的小訊號輸出與激勵、應變規係數及應變成正比。導線電阻、溫度與黏貼品質都會改變零點或靈敏度；量測微小訊號時，需要分開檢查橋路、放大器和構件本身，避免把儀器漂移當成鋼軌應變。~Small-signal quarter-bridge output is proportional to excitation, gauge factor and strain. Lead resistance, temperature and bonding affect zero and sensitivity. Small-signal measurement requires separate checks of bridge, amplifier and structure so instrument drift is not mistaken for rail strain.',
  '理想四分之一橋小應變近似，輸入已是分離後的機械應變。~Ideal small-strain quarter bridge with already separated mechanical strain.',
  '用電阻分流校驗核對整條量測鏈，再以無載溫度循環檢查表觀應變。~Use a shunt calibration to check the complete measurement chain, then an unloaded thermal cycle to examine apparent strain.',
  '激勵電壓漂移會按比例改變輸出，黏貼層鬆脫則可能讓訊號幅度下降而噪音增加。~Excitation drift scales output, while a failing bond can reduce response amplitude and increase noise.',
  '橋路輸出變化一定全都來自被測鋼軌的機械應變~Every bridge-output change necessarily comes from mechanical rail strain.', 'V')
M('beam_deflection', [('P',80000,'N','跨中集中力~central point load'),('L',20,'m','簡支跨度~simply supported span'),('E',35000000000,'Pa','彈性模數~Young modulus'),('I',0.5,'m4','截面慣性矩~second moment of area')],
  'P*L**3/(48*E*I)*1000','mm',
  '簡支梁跨中集中荷載的撓度隨跨度三次方增加，與彎曲剛度成反比。跨座導梁的車輛輪載並非真正集中於單點，支承與扭轉也會參與；概念梁模型適合量級檢查，但不能直接作為完整導梁的行車驗收。~Midspan deflection of a simply supported beam under a central point load scales with span cubed and inversely with flexural rigidity. Monorail wheel loads are distributed and involve supports and torsion. The beam model is useful for scale checks, not complete guideway acceptance.',
  '小撓度等截面歐拉梁，簡支與單一跨中力，忽略剪切及扭轉。~Small-deflection uniform Euler beam with simple supports and one central load; shear and torsion are omitted.',
  '量跨中與支承位移並扣除支承沉陷，以不同載重檢查線性比例及卸載回復。~Measure midspan and support movement, subtract support settlement, and test load proportionality and unloading recovery.',
  '未扣支承沉陷會把基礎移動當成梁撓度，裂縫或接頭滑移則使載重關係不再線性。~Unremoved support settlement appears as beam deflection; cracking or joint slip can make the load relation nonlinear.',
  '跨度加倍時其他條件相同的梁撓度也只增加一倍~Doubling span with other conditions fixed merely doubles beam deflection.', 'L')
M('torsion', [('T',120000,'N*m','扭矩~torque'),('L',15,'m','構件長度~member length'),('G',14000000000,'Pa','剪切模數~shear modulus'),('J',0.3,'m4','等效扭轉常數~equivalent torsion constant')],
  'T*L/(G*J)*1000','mrad',
  '偏心輪載會扭轉導梁，扭角由扭矩、長度與扭轉剛度控制。兩側輪道相對高差會影響導向輪接觸，即使跨中垂直撓度很小仍可能存在明顯扭轉；開口截面與翹曲拘束的行為不能用單純圓軸公式概括。~Eccentric wheel loading twists a guideway, with angle governed by torque, length and torsional rigidity. Relative rail-surface height affects guide-wheel contact even when vertical deflection is small. Open sections and restrained warping cannot be represented fully by a simple shaft analogy.',
  '均勻聖維南扭轉與已知等效扭轉常數，未含翹曲拘束。~Uniform Saint-Venant torsion with a known equivalent torsion constant; restrained warping is excluded.',
  '在兩側同斷面量高程差，將剛體轉動與支承沉陷分離，再比較偏心載重方向反轉。~Measure opposite-side elevations at common sections, separate rigid rotation and settlement, and reverse eccentric loading for comparison.',
  '只量梁中心線會漏掉扭轉，左右感測器不同基準則可能製造假的扭角。~Centreline-only measurements miss torsion; mismatched sensor datums can create an artificial twist angle.',
  '導梁中心線沒有明顯下沉就表示不可能發生扭轉~Little guideway-centreline settlement proves that torsion cannot occur.', 'T')
M('centripetal', [('v',12,'m/s','速度~speed'),('R',150,'m','曲線半徑~curve radius')],
  'v*v/R','m/s2',
  '曲線向心加速度與速度平方成正比、與半徑成反比，導向輪與懸吊需共同提供相應作用。傾斜或超高可改變乘客感受的側向分量，但不會消除車輛轉彎所需的向心加速度；轉折處的變化率亦影響舒適。~Centripetal acceleration scales with speed squared and inverse radius, supplied through guidance and suspension forces. Tilt or banking changes the lateral component felt by passengers but does not remove the acceleration needed to turn. Its rate of change through transitions also affects comfort.',
  '平面定速圓曲線，不含超高、傾斜與過渡曲線。~Constant-speed planar circular curve, excluding cant, tilt and transition geometry.',
  '同步比較速度、曲率及車體側向加速度，先轉換感測器座標再討論乘坐感受。~Compare synchronized speed, curvature and body lateral acceleration after transforming sensor coordinates.',
  '感測器未扣重力投影會把傾斜誤當側向動態，曲率定位錯位則使模型峰值位置偏移。~Unremoved gravity projection can mimic lateral dynamics; misregistered curvature shifts the predicted peak location.',
  '速度加倍但半徑不變時側向加速度也只增加一倍~Doubling speed at unchanged radius merely doubles lateral acceleration.', 'v')
M('magnetic_pressure', [('B',0.6,'T','代表磁通密度~representative flux density'),('A',0.02,'m2','作用面積~active area'),('mu0',1.2566370614359173e-6,'H/m','真空導磁率~vacuum permeability')],
  'B*B*A/(2*mu0)/1000','kN',
  '簡化氣隙磁壓與磁通密度平方成正比，幾何間隙與磁路會影響可達磁通。電磁吸引與電動懸浮的機制不同，不能把這個靜態吸力式套到所有磁浮；線圈控制、飽和與動態穩定性仍需要獨立模型。~Simplified air-gap magnetic pressure scales with flux density squared, while gap geometry and magnetic circuit govern attainable flux. Electromagnetic attraction differs from electrodynamic suspension, so this static expression does not apply to every maglev. Control, saturation and dynamic stability need separate models.',
  '均勻理想氣隙的靜態磁壓，不是超導電動懸浮系統的完整力模型。~Static magnetic pressure in an ideal uniform air gap, not a complete superconducting electrodynamic-suspension force model.',
  '在低能量封閉教具同時量間隙、磁通與力，檢查平方關係並標出飽和區域。~In an enclosed low-energy teaching rig, measure gap, flux and force together, testing square scaling and identifying saturation.',
  '把磁場讀值所在位置與有效氣隙混淆會錯估力，結構變形又可能改變間隙形成回饋。~Confusing probe location with effective air gap biases force; structural deformation can alter the gap and create feedback.',
  '所有磁浮列車都能直接使用同一個靜態吸力公式~Every maglev train can use the same static attraction formula directly.', 'B')
M('survey_angle', [('distance',40,'m','視線距離~sight distance'),('angle',0.000025,'rad','小角誤差~small angular error')],
  'distance*angle*1000','mm',
  '小角度方向誤差會隨視線距離放大成橫向位置誤差，長視線不一定帶來更準的幾何控制。基準網、折光、儀器對中與目標安裝都會影響結果；同一站多次讀值一致，仍可能共同受到基準偏移影響。~A small angular error becomes transverse position error proportional to sight distance, so a longer sight is not automatically more accurate. Control networks, refraction, centring and target mounting all matter. Repeated agreement from one station can still share a common datum error.',
  '小角近似與單一方向誤差，未含完整測量網平差。~Small-angle approximation for one direction error, not a complete survey-network adjustment.',
  '用不同站位與往返觀測交叉核對，將角度誤差、對中誤差與基準移動分列。~Cross-check from different stations and reciprocal observations, separating angular error, centring and datum movement.',
  '儀器重複性良好可能掩蓋穩定的對中偏差，熱折光則使日夜結果有系統差異。~Good repeatability can conceal stable centring bias; thermal refraction can create systematic day-night differences.',
  '同一站位重複量測完全一致就能保證絕對位置正確~Identical repeated observations from one station guarantee correct absolute position.', 'distance')
M('spatial_frequency', [('speed',40,'m/s','運行速度~running speed'),('wavelength',20,'m','幾何波長~geometric wavelength')],
  'speed/wavelength','Hz',
  '固定空間波長在移動車輛上轉換成時間激振頻率，因此同一幾何不平順在不同速度下可能接近不同振動模態。只看最大偏差會漏掉波長資訊；導梁精度控制需要把幾何頻譜、車速與車輛動態連結，而非只追求單點誤差最小。~A spatial wavelength becomes a temporal excitation frequency on a moving vehicle, so the same geometry can excite different modes at different speeds. Maximum deviation alone loses wavelength information. Guideway precision therefore links geometry spectra, speed and vehicle dynamics rather than only minimizing point errors.',
  '定速通過單一正弦空間成分，未計車輛傳遞函數。~Constant-speed passage over one sinusoidal spatial component; the vehicle transfer function is not included.',
  '將幾何資料按里程頻譜分析，再用速度轉換頻率，與車上加速度頻譜比較。~Analyse geometry by spatial frequency, transform using speed, and compare with onboard acceleration spectra.',
  '里程軸不均勻會扭曲頻譜，忽略車輛模態又可能把所有波長視為同樣重要。~Uneven distance sampling distorts spectra; ignoring vehicle modes incorrectly treats every wavelength as equally important.',
  '幾何最大誤差一樣時所有波長的乘坐影響一定一樣~Equal maximum geometry error gives identical ride effects at every wavelength.', 'speed')
M('resonance', [('k',1800000,'N/m','等效剛度~equivalent stiffness'),('m',12000,'kg','等效質量~equivalent mass')],
  'sqrt(k/m)/(2*pi)','Hz',
  '單自由度固有頻率由剛度與質量比的平方根決定。提高剛度可能移開一個激振頻率，也可能移近另一個頻率；阻尼控制峰值而不只改變頻率，因此僅比較靜態變形不能預測動態放大。~A single-degree natural frequency follows the square root of stiffness-to-mass ratio. Stiffening can move away from one excitation yet toward another. Damping controls the resonant peak as well as frequency effects, so static deflection alone cannot predict dynamic amplification.',
  '線性無阻尼單自由度頻率，未含多模態與輪軌或磁路耦合。~Linear undamped single-degree frequency without multimode, wheel-rail or magnetic coupling.',
  '用低能量掃頻或自由衰減試驗量頻率與阻尼，對照載重改變後的模態移動。~Measure frequency and damping with low-energy sweep or free decay, then compare modal shifts after changing load.',
  '只增加剛度而忽略激振頻帶可能使振動更大，感測器裝在節點則可能漏掉主要模態。~Stiffening without considering excitation bands can increase vibration; a sensor at a node may miss the dominant mode.',
  '結構越硬就能保證任何速度下振動都一定更小~A stiffer structure always guarantees smaller vibration at every speed.', 'k')
M('wear', [('depth',0.6,'mm','觀察磨耗深度~observed wear depth'),('cycles',30000,'cycles','觀察循環數~observed cycles'),('future',10000,'cycles','外推循環數~extrapolated cycles')],
  'depth/cycles*future','mm',
  '線性磨耗率可以作短區間履歷比較，但磨耗機制可能隨潤滑、負載與表面狀態改變。早期磨合與後期疲勞不一定沿同一斜率；把短期平均率外推到全壽命，容易忽略加速劣化及偶發損傷。~A linear wear rate supports short-interval history comparisons, but lubrication, load and surface state can change the mechanism. Running-in and later fatigue need not share one slope. Extrapolating a short average across a whole life can miss accelerating deterioration and incidental damage.',
  '固定工況短區間線性外推，不是剩餘壽命保證。~Short-range linear extrapolation at fixed conditions, not a remaining-life guarantee.',
  '在相同位置重複量輪廓與累積負載，檢查分段斜率是否改變，再決定是否可外推。~Repeat profile and cumulative-load measurements at identical positions, examine changes in segment slopes, and only then judge extrapolation.',
  '量測基準改變可產生假磨耗，潤滑中斷則可能使後續斜率突然增大。~Changed measurement datum can create apparent wear; interrupted lubrication can sharply increase later wear rate.',
  '前一個月的平均磨耗率能保證整個使用壽命都不變~The previous month average wear rate is guaranteed to remain unchanged throughout life.', 'future')
M('test_time', [('cases',120,'cases','測試案例數~test cases'),('minutes',8,'min/case','平均案例時間~mean case duration'),('setup',180,'min','設定與恢復時間~setup and recovery time')],
  '(cases*minutes+setup)/60','h',
  '測試工時包含案例執行與環境設定、資料復原及證據整理。平行化只有在資源和狀態真正獨立時有效；把多個會修改同一狀態的測試同時執行，可能造成結果不可重現，表面節省時間卻增加診斷成本。~Test effort includes case execution, setup, state restoration and evidence handling. Parallelism helps only when resources and state are genuinely independent. Concurrent tests modifying one shared state can become irreproducible, apparently saving execution time while increasing diagnostic cost.',
  '確定平均案例時間的串行估算，未含故障重測與資源衝突。~Serial estimate with deterministic mean case time; failure reruns and resource conflicts are excluded.',
  '逐案記錄前置狀態、執行時間與復原時間，分開列出正常完成和失敗重測。~Record preconditions, execution and restoration for every case, separating normal completion from failure reruns.',
  '省略復原步驟會讓前案狀態污染後案，僅報告成功案例時間則低估總測試成本。~Omitted restoration contaminates later tests with earlier state; reporting only successful durations understates total effort.',
  '所有整合測試都可以同時執行而完全不影響結果~All integration tests can run simultaneously without affecting results.', 'cases')
M('confidence_zero', [('tests',300,'independent trials','獨立試驗次數~independent trial count'),('confidence',0.95,'1','單側信賴水準~one-sided confidence level')],
  '1-(1-confidence)**(1/tests)','failure probability',
  '零次觀察到失效不代表真實失效機率為零。獨立伯努利試驗可由全數成功的機率反推單側上界，試驗數增加才會縮小界限；相關測試或只選容易案例會使這個統計推論不再成立，也不能由此宣告達到安全完整性等級。~Zero observed failures does not imply zero true failure probability. Independent Bernoulli trials allow a one-sided upper bound from the probability of all successes, which decreases with sample count. Correlated or selectively easy cases invalidate this inference and cannot establish a safety-integrity level.',
  '獨立同分布二元試驗且觀察零失效，非每小時失效率。~Independent identical binary trials with zero observed failures, not an hourly failure rate.',
  '核對案例獨立性與抽樣範圍，保留所有失敗紀錄，再說明統計界限對哪一類情境有效。~Audit independence and sampling scope, retain all failures, and state the scenario population to which the bound applies.',
  '反覆重跑相同狀態可能沒有增加獨立證據，刪去失敗案例則直接破壞零失效假設。~Repeated identical states may add no independent evidence, while deleting failures invalidates the zero-failure assumption.',
  '完成很多次沒有故障的測試就能證明故障機率為零~Many failure-free tests prove that the failure probability is zero.', 'tests')
M('alarm_rate', [('events',18,'alarms','警報數~alarm count'),('minutes',6,'min','觀察期間~observation interval')],
  'events/minutes','alarms/min',
  '警報到達率描述操作員接收訊息的負荷，但嚴重度、重複性與處置時間也決定可管理性。大量同根因警報可能淹沒最早的關鍵訊息；抑制重複訊號應保留可追溯性，不能以刪掉重要警報來美化數字。~Alarm arrival rate describes operator information load, while severity, repetition and action time determine manageability. Many alarms from one cause can obscure the first critical message. Duplicate suppression must preserve traceability rather than deleting important alarms to improve a metric.',
  '平均警報到達率，非人因可接受上限或人員能力評分。~Mean alarm arrival rate, not an acceptable human-factors limit or a rating of operator capability.',
  '以匿名情境重播記錄首個相關警報、確認與處置時刻，分開統計重複及獨立事件。~Replay anonymized scenarios, timestamp first relevant alarm, acknowledgement and action, and separate duplicates from independent events.',
  '警報洪流可能使操作員確認了所有訊息卻未處理根因，缺乏優先順序又會延遲關鍵判斷。~An alarm flood can lead to acknowledging messages without addressing causes; missing prioritization delays critical interpretation.',
  '操作員把所有警報點選確認就代表根本問題都已解決~Acknowledging every alarm means that all underlying problems have been solved.', 'events')
M('reaction_distance', [('v',16,'m/s','接近速度~approach speed'),('reaction',2.5,'s','假想反應時間~assumed reaction time')],
  'v*reaction','m',
  '反應期間移動距離由速度乘反應時間決定，這段距離在任何制動能力發揮前已經消耗。察覺、理解與動作不是同一時刻，介面可讀性和預期程度會改變反應；把受訓受試者的最佳表現當作所有人的固定值會低估需求。~Distance during reaction is speed times reaction time and is consumed before braking can take effect. Detection, interpretation and action are separate moments influenced by readability and expectation. The best performance of a trained participant is not a fixed value applicable to everyone.',
  '等速反應距離的原創假設，不是道路或鐵道的正式設計視距。~Constant-speed reaction-distance teaching assumption, not an official road or railway sight-distance requirement.',
  '以安全桌面重播分別量察覺與動作時間，呈現分布與不確定度，而非只報最快一次。~Use safe desktop replay to separate detection and action times, reporting distributions and uncertainty rather than only the fastest attempt.',
  '事先告知事件時刻會使反應異常快速，視線遮蔽則可能讓訊號亮起到被察覺之間增加延誤。~Announcing event timing produces unusually fast responses; occlusion adds delay between signal activation and detection.',
  '制動性能很好就可以完全忽略人員反應期間的距離~Good braking performance allows reaction distance to be ignored completely.', 'reaction')

# Wording-specific variants prevent measurement-chain leakage between domains.
import copy
MODELS['actuator_sync']=copy.deepcopy(MODELS['sync_error'])
MODELS['actuator_sync']['quantities']=[('v1',0.012,'m/s','致動端一速度~first actuator speed'),('v2',0.0115,'m/s','致動端二速度~second actuator speed'),('t',20,'s','動作時間~motion time')]
MODELS['actuator_sync']['mechanism']='耦合致動器的小速度差會隨動作時間累積成行程差，使連桿扭轉或局部阻力增加。位置回授能限制累積，卻仍需共同座標和獨立零點檢查；兩個馬達瞬間轉速相同只代表該時刻差值不再增加，並不能消除先前留下的位置偏移。~A small speed difference between coupled actuators accumulates into travel mismatch, twisting linkages or increasing local resistance. Position feedback can limit accumulation but requires a common coordinate and independent zero checks. Equal instantaneous motor speeds only stop further growth at that instant; they do not remove the position offset already accumulated.'
MODELS['actuator_sync']['verification']='以獨立位移計同時量測兩個連接點，對照編碼器零點與連桿幾何，再比較低負載及偏載時的誤差斜率。~Measure both connection points simultaneously with independent displacement sensors, compare encoder zeros and linkage geometry, then compare drift slopes at low and uneven load.'
MODELS['actuator_sync']['failure']='某端摩擦增加會造成位移差斜率改變，共同零點錯誤則可能讓兩端回授一致卻偏離機構中線。~Extra friction at one end changes the mismatch slope, whereas a shared zero error can make feedback agree while the linkage is displaced from its reference.'
MODELS['actuator_sync']['misconception']='兩致動器瞬間速度相同就能證明已累積的位置差為零~Equal instantaneous actuator speeds prove that the accumulated position difference is zero.'
MODELS['vehicle_clearance']=copy.deepcopy(MODELS['travel'])
MODELS['vehicle_clearance']['quantities']=[('distance',30,'m','車尾需行進的清空距離~rear-end clearance travel'),('speed',2,'m/s','假想定車速~assumed constant vehicle speed'),('wait',4,'s','起步等待~startup waiting')]
MODELS['vehicle_clearance']['mechanism']='道路車輛清空時間從開始等待到車尾完全離開衝突區計算，距離必須包含車長而不能只看車頭的位置。定速度估算只展示等待與移動兩部分，長車起步、轉彎和下游阻塞可能改變速度；鄰近號誌的放行並不保證車尾已有足夠可用空間。~Road-vehicle clearance runs from initial waiting until the rear leaves the conflict area, so the distance must include vehicle length rather than front position alone. Constant speed separates waiting and movement conceptually. Long-vehicle acceleration, turning and downstream blockage alter speed; a nearby green indication does not establish adequate space for the vehicle rear.'
MODELS['vehicle_clearance']['boundary']='定車速與固定起步等待的桌面教學模型，未含加速、坡度、轉彎或現場警示設定。~Desktop constant-speed model with fixed startup waiting, excluding acceleration, gradient, turning and field-warning settings.'
MODELS['vehicle_clearance']['verification']='在桌面交通模型標記車頭與車尾事件，分別計算等待與移動；以不同車長重播並核對清空定義完全一致。~Mark front and rear events in a desktop traffic model, measure waiting and motion separately, and replay different vehicle lengths with one consistent clearance definition.'
MODELS['vehicle_clearance']['failure']='用車頭通過代替車尾清空會低估占用時間，下游排隊還可能讓正常起步的車輛停在衝突區內。~Using front passage instead of rear clearance understates occupation; downstream queues can stop a vehicle inside the conflict area after an otherwise normal start.'
MODELS['vehicle_clearance']['misconception']='車頭通過平交道出口就表示整輛長車已完全清空~The front passing the crossing exit means that the entire long vehicle is clear.'
M('groove_tolerance', [('groove',0.4,'mm','槽形製造誤差界~groove manufacturing error bound'),('flange',0.3,'mm','輪緣幾何誤差界~flange geometry error bound'),('survey',0.2,'mm','測量誤差界~survey error bound')],
  'groove+flange+survey','mm',
  '槽形鋼軌與輪緣之間的幾何介面包含製造、磨耗與量測的不確定度。把各個最大誤差同向相加可得到保守的誤差預算，但不能因此推得槽寬、輪緣空間或真正間隙；實際幾何還需要名義尺寸、變形與曲線姿態，而行人和自行車風險屬另一組介面需求。~The groove–flange interface contains uncertainty from manufacturing, wear and measurement. Adding same-direction maximum error bounds gives a conservative uncertainty budget, not the groove width, flange clearance or actual gap. Real geometry also needs nominal dimensions, deformation and curve attitude. Pedestrian and bicycle risks form a separate set of street-interface requirements.',
  '僅合成三個有界誤差，不是實際槽寬、輪緣間隙或允收限值。~Three bounded errors only, not actual groove width, flange clearance or an acceptance limit.',
  '以獨立量具核對槽形與輪緣輪廓，在相同座標保留名義尺寸及誤差符號，另檢查測量零點。~Check groove and flange profiles with independent gauges, retain nominal dimensions and error signs in one coordinate system, and verify instrument zeros separately.',
  '將誤差總和當成實際間隙會省略名義幾何；共用失準量具還可能讓兩個錯誤輪廓看似互相吻合。~Treating an error sum as the actual gap omits nominal geometry; a shared miscalibrated gauge can also make two incorrect profiles appear mutually compatible.',
  '三項誤差界的總和就是現場鋼軌槽內的實際間隙~The sum of three error bounds is the actual clearance inside the rail groove.', 'groove')
M('runoff', [('C',0.7,'1','假想逕流係數~assumed runoff coefficient'),('i',30,'mm/h','教學降雨強度~teaching rainfall intensity'),('A',120,'m2','集水面積~catchment area')],
  'C*i*A/3600','L/s',
  '降雨逕流需求可由雨強、集水面積與逕流係數估算，毫米乘平方米等於公升。這個需求量尚未描述排水口能力，槽內泥砂、路面坡度和尾水都會影響真正排放；短小雨場的計算也不能代表暴雨頻率與都市集水區的完整水文過程。~Rainfall runoff demand follows intensity, catchment area and a runoff coefficient, with millimetres times square metres giving litres. This demand does not describe inlet capacity. Sediment, pavement slope and tailwater affect actual discharge, while a short simple event cannot represent storm frequency or the full hydrology of an urban catchment.',
  '均勻穩定降雨的簡化需求模型，未求排水容量、集流延遲或淹水水深。~Simple demand under uniform steady rainfall; drain capacity, concentration delay and flood depth are not solved.',
  '以集水邊界核對面積與降雨單位，在低風險縮尺水槽量測流入及流出，分開記錄槽內暫存水量。~Check catchment boundaries and rainfall units, measure inflow and outflow on a low-risk scale water rig, and record temporary storage separately.',
  '漏算鄰近路面集水會低估需求，排水口淤塞則會在雨強不變時使暫存水量上升而不改變此公式的需求。~Omitted adjoining pavement understates demand; a blocked inlet raises storage at unchanged rainfall without changing the demand calculated by this formula.',
  '算出的降雨逕流量就等於排水口保證可以排走的流量~Calculated rainfall runoff equals the flow that the drain is guaranteed to remove.', 'i')
M('feeder_loss', [('I',200,'A','假想直流電流~assumed direct current'),('R',0.03,'ohm','等效回路電阻~equivalent circuit resistance')],
  'I*I*R/1000','kW',
  '直流饋電與接觸路徑的電阻損耗與電流平方成正比，所以尖峰電流對發熱特別敏感。等效電阻可包含導線與接點，卻不能把各部位的散熱條件視為相同；平均總損耗正常仍可能有局部接點過熱，分段供電的安全狀態也不是由此功率公式決定。~Resistive loss in a DC feeder and contact path scales with current squared, making peak current particularly influential. Equivalent resistance may include conductors and contacts, but their cooling conditions differ. A normal total loss can coexist with a hot contact, and the safe state of segmented supply is not determined by this power equation.',
  '理想穩態直流電阻損耗，未提供地面供電分段邏輯或現場帶電作業方法。~Ideal steady DC resistance loss, without ground-supply segmentation logic or live electrical work procedures.',
  '在隔離低壓台同時量測電流與電壓降，核對功率帳後以溫度分布尋找局部接觸電阻異常。~Measure current and voltage drop together on an isolated low-voltage rig, check power balance, and use temperature distribution to locate abnormal contact resistance.',
  '鬆動接點會把損耗集中在小區域，平均回路電阻的低解析度量測可能漏掉隨振動發生的間歇接觸。~A loose contact concentrates loss in a small region; low-resolution mean resistance measurement can miss intermittent contact changes under vibration.',
  '直流電流增加兩倍時導線電阻損耗也只會增加兩倍~Doubling DC current merely doubles resistive conductor loss.', 'I')
MODELS['switch_torque']=copy.deepcopy(MODELS['torque'])
MODELS['switch_torque']['mechanism']='懸掛式轉轍梁的驅動力矩由致動力與垂直有效力臂相乘，連桿角度會讓有效力臂隨行程改變。馬達輸出足夠不代表遠端梁位已到達，彈性變形、齒隙與摩擦均會改變傳力；機械保持及位置確認必須有獨立證據，不能由一次成功轉動推論。~Drive torque for a suspended switch beam is actuator force times perpendicular effective lever arm, which changes with linkage angle. Adequate motor output does not establish that the remote beam has arrived. Compliance, backlash and friction affect force transfer; mechanical retention and position confirmation need independent evidence rather than inference from one successful movement.'
MODELS['switch_torque']['boundary']='準靜態剛性連桿力矩，不包含實際懸掛式轉轍構造、動態衝擊或額定設計。~Quasistatic rigid-link torque, excluding actual suspended-switch construction, impact dynamics and rated design.'
MODELS['switch_torque']['verification']='用縮尺連桿同時量測力與垂直力臂，在不同角度比較力矩，再以獨立位移計核對遠端梁的位置。~Measure force and perpendicular lever arm on a scale linkage at several angles, then independently check remote beam position with a displacement sensor.'
MODELS['switch_torque']['failure']='連桿接近不利幾何時所需力會提高，齒隙又可能使馬達角度改變卻沒有相應梁位移。~Unfavourable linkage geometry raises required force, while backlash can allow motor-angle change without corresponding beam displacement.'
MODELS['switch_torque']['misconception']='馬達角度已達目標就能保證懸掛式轉轍梁定位完成~The target motor angle guarantees completed positioning of a suspended switch beam.'
MODELS['pedestrian_sampling']=copy.deepcopy(MODELS['sampling'])
MODELS['pedestrian_sampling']['quantities']=[('v',1.2,'m/s','假想行走速度~assumed walking speed'),('f',10,'Hz','軌跡取樣頻率~trajectory sampling rate')]
MODELS['pedestrian_sampling']['mechanism']='行人軌跡在固定時間間隔取樣時，相鄰位置的距離隨步速增加而變大。較密的資料點能保留短暫停頓，但追蹤器遮蔽、身分配對及位置誤差仍可能主導結果；取樣頻率提高不會自動改善定位精度，也不能以均勻步速替代門口交互避讓的動態。~Fixed-time trajectory sampling produces wider spatial gaps at higher walking speed. Denser samples can preserve brief pauses, but occlusion, identity matching and position errors may still dominate. Increasing sample rate does not automatically improve localization accuracy, and uniform walking speed cannot represent the interactions and avoidance movements near a doorway.'
MODELS['pedestrian_sampling']['boundary']='定步速與規則取樣的教學幾何，不含人群互動、遮蔽及定位誤差。~Teaching geometry at constant walking speed with regular samples, excluding crowd interaction, occlusion and position error.'
MODELS['pedestrian_sampling']['verification']='使用標記地面的低密度步行教具，同步保留影像時間與獨立位置刻度，抽查轉彎、停頓及遮蔽前後的軌跡。~Use a marked-floor low-density walking exercise, retain image times and independent position scales, and inspect trajectories around turns, pauses and occlusion.'
MODELS['pedestrian_sampling']['failure']='追蹤器身分交換會製造不合理跳躍，影格遺失則可能被內插掩蓋；應回到原始影像區分演算法與真實移動。~Identity swaps create implausible jumps, while interpolation can conceal dropped frames; return to raw imagery to distinguish algorithmic artefacts from real movement.'
MODELS['pedestrian_sampling']['misconception']='只要軌跡取樣頻率提高就必定得到更準確的行人位置~Increasing trajectory sample rate always produces more accurate pedestrian positions.'
M('temporal_sampling',[('f',20,'Hz','壓力取樣頻率~pressure sampling frequency')],
 '1000/f','ms',
 '壓力時間序列的相鄰樣點間隔由取樣頻率倒數決定，短於此間隔的事件可能完全落在兩點之間。提高頻率仍需要適當感測頻寬與抗混疊濾波，資料記錄器和感測器中較慢的一環會限制真實解析度；只增加輸出的資料筆數不會補回已被濾掉的峰值。~The interval between pressure samples is the reciprocal of sampling frequency, so an event shorter than that interval can fall entirely between observations. A higher rate still needs appropriate sensor bandwidth and anti-alias filtering. The slower part of the sensor-recorder chain limits actual resolution; producing more output rows cannot restore an already filtered peak.',
 '等間隔時間取樣，未代表感測器頻寬或峰值重建精度。~Equally spaced temporal samples, not sensor bandwidth or peak-reconstruction accuracy.',
 '以校正器產生已知持續時間的低壓脈衝，對照獨立高頻記錄，保留濾波設定並比較峰值與脈衝面積。~Generate a calibrated low-pressure pulse of known duration, compare with an independent faster recorder, retain filter settings and compare peak and pulse area.',
 '資料內插會讓曲線平順卻沒有新增觀測，未經抗混疊的高頻擾動也可能折回低頻形成虛假活塞風特徵。~Interpolation smooths a curve without adding observations, while unfiltered high-frequency disturbance can alias into an apparent low-frequency piston-flow feature.',
 '把相鄰壓力資料內插成更多點就能恢復任何短暫峰值~Interpolating extra points between pressure observations can recover every brief pressure peak.', 'f')
MODELS['pressure_rss']=copy.deepcopy(MODELS['rss'])
MODELS['pressure_rss']['quantities']=[('s1',3,'Pa','獨立壓力通道一標準差~first independent pressure standard deviation'),('s2',4,'Pa','獨立壓力通道二標準差~second independent pressure standard deviation')]
MODELS['pressure_rss']['result_unit']='Pa'
MODELS['pressure_rss']['boundary']='獨立隨機壓力標準差，不是最大門負荷或確定壓差界限。~Independent random pressure standard deviations, not maximum door load or a deterministic pressure-difference bound.'
MODELS['strain_rss']=copy.deepcopy(MODELS['rss'])
MODELS['strain_rss']['quantities']=[('s1',3,'microstrain','獨立應變通道一標準差~first independent strain standard deviation'),('s2',4,'microstrain','獨立應變通道二標準差~second independent strain standard deviation')]
MODELS['strain_rss']['result_unit']='microstrain'
MODELS['strain_rss']['boundary']='獨立隨機應變標準差，不包含共同溫度偏差或無應力溫度的不確定度。~Independent random strain standard deviations, excluding common temperature bias and uncertainty in stress-free temperature.'
M('elevator_cycle',[('board',18,'s','開門登乘及關門~door and boarding time'),('travel',24,'s','載客行進~loaded travel'),('alight',16,'s','開門離開及關門~door and alighting time'),('return_',24,'s','回程時間~return travel')],
 '3600/(board+travel+alight+return_)','trips/h',
 '單台電梯往返週期由登乘、行進、離開及回程組成，門動作必須被計入服務階段。理想每小時循環數不等於每小時可服務人數，還需考慮載客量、樓層呼叫、上下行需求與可用性；乘客集中到達時，平均循環有餘裕也可能形成長候梯隊伍。~An elevator round trip includes boarding, travel, alighting and return, with door actions included in the service phases. Ideal cycles per hour are not passengers per hour: occupancy, floor calls, directional demand and availability also matter. Concentrated passenger arrivals can create long waits even when the mean cycle appears to offer spare capacity.',
 '兩樓層串行往返且無中途停靠的理想循環，未含載客量及等待分布。~Ideal serial round trip between two levels without intermediate stops, excluding occupancy and waiting distributions.',
 '以同一門開關事件界定各階段，分別記錄登乘與離開，抽查回程空載及途中呼叫是否改變循環邊界。~Define stages with consistent door events, record boarding and alighting separately, and inspect whether empty return or intermediate calls change the cycle boundary.',
 '漏算回程會高估循環率，把門動作在兩個階段重複計入則會低估能力；實際載客需求還可能由上游排隊控制。~Omitting return overstates cycle rate, while counting door motion twice understates capacity; actual passenger demand may also be governed by upstream queues.',
 '電梯每小時往返次數可以直接當作每小時服務人數~Elevator round trips per hour can directly be treated as passengers served per hour.', 'board')
M('depot_cycle',[('receive',120,'s','接車確認~receiving confirmation'),('inspect',900,'s','假想檢查工作~hypothetical inspection'),('move',180,'s','工位間移動~movement between bays'),('handoff',240,'s','驗證交回~verified handoff')],
 '3600/(receive+inspect+move+handoff)','jobs/h',
 '檢修物流的完整週期從接車確認開始，到驗證交回才結束，不能只計工具接觸車輛的時間。各階段若串行使用同一資源，其持續時間需要相加；平行工位可改變整體吞吐，但共用移車通道、量測儀器或簽核人員仍可能成為瓶頸，需在資源圖上明確表示。~The maintenance logistics cycle begins at receiving confirmation and ends at verified handoff rather than counting only tool contact. Durations add when stages serially use one resource. Parallel bays can alter throughput, but shared movement paths, instruments or release personnel may remain bottlenecks that must appear explicitly in the resource graph.',
 '單工位無重疊的串行假想作業，未包含備品等待與返工分布。~Hypothetical non-overlapping serial work in one bay, excluding spares waiting and rework distributions.',
 '以工單與獨立事件觀察核對四階段起訖，記錄等待原因和返工次數，避免電子完成時間早於實際移交。~Cross-check four stage boundaries using work orders and independent event observation, recording wait causes and reruns so electronic completion cannot precede physical handoff.',
 '只統計檢查時間會高估工位吞吐，交回前文件缺失可能讓車輛占位卻被系統標示為已完成。~Inspection-only accounting overstates bay throughput; missing release evidence can keep a vehicle occupying a bay after software has labelled the task complete.',
 '檢查工具停止作業就代表整個機廠工位週期已完成~The maintenance-bay cycle is complete as soon as inspection tools stop working.', 'inspect')
MODELS['wheel_sampling']=copy.deepcopy(MODELS['sampling'])
MODELS['wheel_sampling']['quantities']=[('v',2.64,'m/s','假想輪面圓周速度~assumed wheel-surface speed'),('f',2000,'Hz','輪廓取樣頻率~profile sampling frequency')]
MODELS['wheel_sampling']['boundary']='定輪面圓周速度與等間隔取樣，不包含輪面滑動、徑向振動或感測頻寬。~Constant circumferential surface speed and regular samples, excluding surface slip, radial vibration and sensor bandwidth.'
MODELS['container_lifting']=copy.deepcopy(MODELS['lifting'])
MODELS['container_lifting']['failure']=MODELS['lifting']['failure'].replace('扭曲車體','扭曲貨櫃或吊具').replace('body distortion','container or spreader distortion')
MODELS['switch_work']=copy.deepcopy(MODELS['work'])
MODELS['switch_work']['boundary']='定力準靜態構件行程與定效率，不含動態衝擊或懸掛式轉轍的實際保持要求。~Constant-force quasistatic member travel and fixed efficiency, excluding dynamic impact and actual suspended-switch retention requirements.'
M('vehicle_queue',[('arrival',0.4,'vehicles/s','道路到達率~road-vehicle arrival rate'),('service',0.3,'vehicles/s','下游離開率~downstream departure rate'),('duration',90,'s','觀察期間~observation duration')],
 '(arrival-service)*duration','vehicles',
 '道路車列的新增存量來自到達與離開流率差乘時間，計數邊界必須在同一車道群。這是預期流量的連續近似，實際車輛是離散事件；回堵是否到達平交道還取決於車長、車間距和可儲存道路長度，僅有平均服務率無法證明衝突區不被占用。~New road-queue occupancy is the difference between arrival and departure rates times duration, measured over one lane group. This is a continuous approximation to expected flow while actual vehicles are discrete events. Whether spillback reaches a crossing also depends on vehicle lengths, gaps and storage distance; average service rate alone cannot prove that the conflict area remains clear.',
 '固定平均流率且佇列持續存在的增量模型，未計初始車數、儲車長度或離散到達。~Increment under fixed mean flows with a persistent queue, excluding initial occupancy, storage length and discrete arrivals.',
 '用桌面道路模型核對同一邊界的進出車數與內部存量，再以不同車長重播，將車數與實際排隊長度分開量測。~Reconcile arrivals, departures and internal occupancy in a desktop road model, replay different vehicle lengths, and measure vehicle count separately from physical queue length.',
 '只看路口出口放行量會漏掉上游車列增長，長車比例提高又可能在車數不變時使排隊尾端更接近平交道。~Exit discharge alone misses upstream queue growth, while a greater proportion of long vehicles can move the queue tail toward the crossing at unchanged vehicle count.',
 '下游每分鐘放行車數穩定就能證明上游不會回堵~Stable downstream vehicle discharge per minute proves that upstream spillback cannot occur.', 'duration')
