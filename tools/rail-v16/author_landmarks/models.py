"""Original railway teaching models. SI inputs; all values are invented exercises."""
M = {}
def add(key, title, mechanism, variables, expression, output, boundary, verify, failure, myth, practice):
    M[key] = dict(title=title, mechanism=mechanism, variables=variables, expression=expression,
                  output=output, boundary=boundary, verify=verify, failure=failure, myth=myth, practice=practice)

add('brake', '延遲與制動距離~Delay and braking distance',
'列車在控制命令傳遞與煞車建立期間仍向前行駛，減速段才把動能耗散；因此停車距離包含延遲距離與減速距離。速度平方項說明高速時少量速度誤差會被放大，固定減速度只能作第一輪界限估算。~A train continues moving while the command propagates and brake force builds. Only the deceleration phase removes kinetic energy, so stopping distance includes both a delay term and a braking term. The squared speed dependence amplifies speed uncertainty; constant deceleration is only an initial bounding approximation.',
{'v':(70,'m/s'),'delay':(2.5,'s'),'a':(0.7,'m/s^2')}, 'v*delay+v*v/(2*a)', ('distance','m'),
'水平直線、定減速、無風；沒有建立黏著分布與煞車熱衰退。~Level straight track and constant deceleration; adhesion variation and thermal fade are excluded.',
'對齊速度、煞車缸壓力與里程的時間戳，分開辨識命令延遲及穩態減速度，再以積分速度的距離交叉檢查。~Align speed, brake-cylinder pressure and distance timestamps. Identify command delay separately from steady deceleration and cross-check distance by integrating measured speed.',
'輪滑保護介入與濕軌會降低實際減速度；感測時間不同步也能製造假延遲，須以第二個時鐘和輪速紀錄區分。~Wheel-slide protection and wet rails can reduce deceleration; unsynchronised sensors can imitate a delay, requiring an independent clock and wheel-speed records.',
'速度增加一成時制動距離必定也只增加一成~A ten percent speed increase must increase braking distance by only ten percent.',
'分別增加延遲與初速，畫出兩條停車曲線；寫出哪個區段對各參數敏感，以及需要哪些現場資料才可建立保護曲線。~Increase delay and initial speed separately, plot both stopping curves, identify the sensitive phase, and list the field evidence needed before defining a protection curve.')

add('cant','曲線超高與未平衡加速度~Cant and unbalanced acceleration',
'曲線需求的向心加速度由重力沿軌道平面的分量與輪軌側向作用共同提供。超高平衡速度只對特定半徑和速度成立，慢車可能出現超高過剩；不能把增加超高當成所有車種都受益的措施。~On a curve, the component of gravity in the track plane and wheel-rail lateral forces together provide centripetal acceleration. Equilibrium cant applies to one radius and speed. A slower service can experience cant excess, so increasing cant does not improve every train condition.',
{'v':(60,'m/s'),'R':(4000,'m'),'gauge':(1.5,'m'),'cant':(0.12,'m')},'v*v/R-9.81*cant/gauge',('residual','m/s^2'),
'小角度近似與剛性車體；未計懸吊側滾、動態輪重減載和規範允收值。~Small-angle approximation and rigid body; suspension roll, dynamic wheel unloading and acceptance limits are excluded.',
'在相同半徑區段量測軌面高差與橫向加速度，扣除感測器安裝角度，並把車體讀值與軌道平面讀值分開記錄。~Measure rail level difference and lateral acceleration on the same curve, remove sensor mounting angle, and distinguish carbody readings from track-plane readings.',
'只依高速通過最佳化超高，可能讓慢車或停車承受反向側向力；感測器橫滾又會把重力投影混入振動訊號。~Cant optimised only for fast trains can impose reverse lateral loading on slow or stopped trains; sensor roll also mixes gravity into vibration measurements.',
'任何速度下增加超高都一定減少車內橫向加速度~Increasing cant always reduces lateral acceleration at every operating speed.',
'選兩種速度共同計算殘餘加速度，找出符號反轉位置，說明為何混合服務需要速度分布而非單一最高速度。~Calculate residual acceleration for two speeds, locate its sign reversal, and explain why mixed services require a speed distribution rather than one maximum speed.')

add('jerk','加速度斜坡與舒適性~Acceleration ramps and comfort',
'相同加速度峰值可以用不同建立時間達到，旅客感受到的突然性由加加速度描述。限制斜坡能減少站立乘客失衡，但也延長加速時間；行車時間、牽引功率及停準控制必須一起重新計算。~The same acceleration peak can be reached with different ramp durations. Jerk measures how abruptly acceleration changes. Limiting the ramp reduces sudden disturbance to standing passengers but extends acceleration time, so running time, traction power and stopping control must be reconsidered together.',
{'a':(0.9,'m/s^2'),'ramp':(3,'s')},'a/ramp',('jerk','m/s^3'),
'線性加速度斜坡；不把此值視為任何營運者的舒適性門檻。~Linear acceleration ramp; the result is not an operator comfort threshold.',
'將加速度經已知頻寬濾波後再微分，保留原始資料，利用速度積分檢查濾波相位延遲沒有改變控制事件的先後。~Filter acceleration with a documented bandwidth before differentiating, retain raw data, and integrate it to check that phase delay has not reordered control events.',
'直接微分含雜訊的加速度會放大高頻誤差，過度平滑又會掩蓋真實尖峰；兩者都可能造成錯誤的舒適性判定。~Differentiating noisy acceleration amplifies high-frequency error, while excessive smoothing hides real peaks; either can produce a false comfort assessment.',
'只要最大加速度相同乘客感受到的突然性就相同~Equal peak acceleration guarantees equal abruptness felt by passengers.',
'比較快慢兩種斜坡在同一終速度下的時間與位移，提交含濾波頻寬及感測器安裝方向的分析紀錄。~Compare fast and slow ramps at the same final speed, calculate elapsed time and distance, and document filter bandwidth and sensor orientation with the analysis.')

add('capacity','班距與有效運能~Headway and usable capacity',
'每小時運能由列車可用容量與通過頻率共同決定，平均班距縮短不代表每個車站都能吸收人流。車門交換、轉乘尖峰與不均勻到站會讓理論運能無法實現，容量計算應同時報告負載分布。~Hourly capacity combines usable train capacity with passage frequency. A shorter average headway does not ensure every station can absorb the passenger flow. Door exchange, transfer surges and irregular arrivals can prevent the theoretical rate from being realised, so occupancy distribution must accompany the capacity estimate.',
{'people':(900,'persons/train'),'headway':(180,'s/train')},'3600*people/headway',('capacity','persons/hour'),
'固定班距且每列都能使用指定容量；不包含站台壅塞及服務波動。~Fixed headway with the stated usable capacity on every train; platform congestion and service variability are excluded.',
'以連續列車的實際到站時間與逐車廂乘載量重算，將未登車人數保留在隊列，不以列車額定容量代替實際服務量。~Recalculate from consecutive arrival times and individual car loads. Carry passengers unable to board into the queue instead of treating rated capacity as delivered service.',
'某一列延誤會使後車追近而前方隊列累積；只看小時平均會漏掉最擁擠列車與長等待尾端。~A delayed train lets following trains bunch while the upstream queue grows; an hourly mean hides both the fullest train and the long-wait tail.',
'只要平均班距減半所有乘客的等待時間就一定減半~Halving average headway necessarily halves the waiting time of every passenger.',
'用一組規則班距與一組相同平均值的不規則班距，追蹤每班留下的人數，解釋理論容量與可用容量的差距。~Compare regular and irregular headways with the same mean, track passengers left behind after each departure, and explain the gap between theoretical and usable capacity.')

add('dwell','車門交換與停站時間~Door exchange and dwell time',
'停站時間由車門開關、旅客交換與確認安全三部分組成。把旅客平均分到所有車門只是基準，樓梯位置會使某幾扇門超載；最慢的門組可能控制全列發車，因此不能只用平均流率。~Dwell time comprises door movement, passenger exchange and confirmation before departure. Equal distribution across doors is only a baseline: stair placement can overload selected doors. The slowest door group may govern departure of the entire train, so average flow alone is insufficient.',
{'exchange':(240,'persons'),'doors':(24,'doors'),'rate':(0.8,'persons/(door*s)'),'fixed':(12,'s')},'exchange/(doors*rate)+fixed',('dwell','s'),
'均勻分配旅客與固定單門流率；不含對向人流衝突。~Uniform passenger distribution and fixed per-door flow; opposing-flow conflicts are excluded.',
'逐門標註下車、上車與關門事件，檢查樓梯附近門組是否偏慢，再以各門最大完成時間對照整列停站時間。~Annotate alighting, boarding and closure at each door, check slow groups near stairs, and compare the latest completion time with whole-train dwell.',
'行李卡門或乘客集中會讓均勻模型低估尾端；延長關門提示可能改善秩序，也可能提高固定停站時間。~Luggage obstruction and clustered passengers make the uniform model underestimate the tail; a longer closing warning may improve order while increasing the fixed dwell component.',
'每扇門的平均流率相同就能忽略乘客分布差異~Equal average door flow rates make passenger distribution irrelevant to dwell time.',
'將一半上車需求集中在四分之一車門，重算最慢門組；提出導引與月台配置改進並區分其對固定時間和交換時間的作用。~Concentrate half the demand at one quarter of the doors, recalculate the slowest group, and distinguish guidance changes affecting fixed time from those affecting exchange time.')

add('turnback','折返作業與路徑占用~Turnback and route occupation',
'終端折返的限制可能來自進站清空、換端、道岔鎖閉或離站衝突。將事件畫成時間線才能分辨能平行的任務與必須串接的任務；簡單加總是一條明示串聯路徑，不是所有終端的通用最小班距。~A terminus may be constrained by approach clearance, cab change, point locking or conflicting departure routes. An event timeline separates parallel tasks from mandatory serial tasks. A simple sum represents one declared serial path, rather than a universal minimum headway for every terminal layout.',
{'arrival':(35,'s'),'reverse':(75,'s'),'release':(25,'s')},'arrival+reverse+release',('cycle','s'),
'單一折返路徑且三項活動不可重疊；不含備用月台與延誤恢復。~One turnback route with three nonoverlapping activities; spare platforms and delay recovery are excluded.',
'把軌道占用、道岔位置與駕駛換端紀錄放在同一時間軸，逐項檢查是否存在未被模型表示的互斥條件。~Place track occupation, point position and cab-change logs on one timeline, then identify exclusion conditions omitted by the simplified sequence.',
'只縮短換端時間而未解除路徑衝突，未必能縮短班距；錯把進路解鎖時間當成列車清空時間也會低估占用。~Reducing cab-change time cannot remove an unresolved route conflict; confusing route release with physical clearance also understates occupation time.',
'換端作業加快多少秒最小班距就一定縮短相同秒數~Every second saved in cab change always removes one second from minimum headway.',
'畫出單月台與雙月台折返的甘特圖，標註不可同時使用的路徑，並以一班晚到列車檢查延誤是否傳到下一班。~Draw single-platform and dual-platform turnback timelines, mark mutually exclusive routes, and introduce one late train to test propagation into the next departure.')

add('regen','再生煞車能量與受電條件~Regenerative energy and receptivity',
'煞車可回收的能量上限來自列車動能，但電網是否能接受能量、逆變器效率與輔助負載會改變實際回送量。把機械可回收量和變電站收到的電量分開，才不會把理想效率當成節電實績。~Train kinetic energy sets an upper bound on regenerative recovery, but network receptivity, converter efficiency and auxiliary demand determine actual delivery. Separating mechanically recoverable energy from electricity received at a substation prevents ideal efficiency from being reported as measured savings.',
{'mass':(240000,'kg'),'v':(25,'m/s'),'eta':(0.65,'1')},'0.5*mass*v*v*eta/3.6e6',('recovered','kWh'),
'一次水平減速、固定總效率；不含阻力及架線電壓限制導致的截斷。~One level deceleration with fixed overall efficiency; resistance and voltage-limited curtailment are excluded.',
'同步積分直流鏈、受電端與制動電阻的功率，對照初末速度；將輔助用電和回送電量用一致符號處理。~Integrate DC-link, line-side and braking-resistor power synchronously and compare initial and final speeds, treating auxiliary consumption and exported energy with consistent signs.',
'鄰車不在受電時再生電壓可能升高而轉入電阻制動；只量逆變器端會高估真正回到供電網的能量。~Without a receptive neighbouring train, voltage can rise and trigger resistor braking; measurement only at the inverter can overstate energy returned to the supply network.',
'只要列車裝有再生煞車全部動能都能回到電網~Installing regenerative braking returns all train kinetic energy to the supply network.',
'比較有受電列車與無受電列車兩種功率時間圖，做能量收支表，提出儲能需求並說明額定能量不等於可接受功率。~Compare power traces with and without a receptive train, build an energy balance, and size an illustrative storage requirement while distinguishing energy capacity from acceptable power.')

add('drag','空氣阻力與牽引功率~Aerodynamic drag and traction power',
'高速列車的空氣阻力與速度平方成正比，而克服此阻力所需功率再乘一次速度，形成三次方敏感度。有效阻力面積包含外形與附屬物影響；會車、隧道及側風會使定常自由場模型失效。~Aerodynamic drag scales with speed squared, and the power needed to overcome it adds another speed factor. Effective drag area includes shape and attachments. Passing trains, tunnels and crosswinds can invalidate the steady open-air approximation even when the nominal speed remains unchanged.',
{'rho':(1.2,'kg/m^3'),'CdA':(10,'m^2'),'v':(70,'m/s')},'0.5*rho*CdA*v**3/1000',('power','kW'),
'定常靜風且阻力面積固定；僅空氣阻力功率，不含輪軌阻力與效率。~Steady still air and constant drag area; aerodynamic power only, excluding rolling resistance and conversion losses.',
'在相同編組與天候下做不同速度的惰行分析，記錄風速方向與車頭迎角，避免把坡度造成的加速度誤判成空阻。~Compare coast-down observations across speeds with the same consist, log wind speed and direction, and separate gradient acceleration from aerodynamic resistance.',
'車底設備改變或側風會改變有效阻力面積；若只以單一速度校準，仍可能在另一速度得到錯誤牽引需求。~Underbody changes and crosswinds alter effective drag area; fitting one speed can still produce a wrong traction requirement at another speed.',
'速度增加一成時克服空氣阻力的功率只增加一成~A ten percent speed increase raises aerodynamic power by only ten percent.',
'對速度增加一成與阻力面積減少一成各算一次，對比功率節省，並把輪軌阻力另列以避免誇大整列節能比例。~Calculate a ten percent speed increase and a ten percent drag-area reduction separately, compare power changes, and keep rolling resistance separate from whole-train energy savings.')

add('tunnelwave','隧道壓力波傳遞~Tunnel pressure-wave travel',
'列車鼻部入隧道產生壓縮擾動，壓力波以接近音速傳播而不是跟著列車速度前進。入口緩衝設計影響波形上升率，波到達出口的時間與車身到達時間屬不同問題，須分開建立量測觸發。~A train nose entering a tunnel creates a compression disturbance whose propagation speed is close to acoustic speed rather than train speed. Entrance treatments affect the rise of the waveform. Wave arrival and train arrival are different events and require separate measurement triggers.',
{'length':(2500,'m'),'sound':(340,'m/s')},'length/sound',('travel','s'),
'一維線性聲學且音速均勻；不預測波幅、微壓波峰值或反射耗散。~One-dimensional linear acoustics with uniform sound speed; amplitude, micro-pressure-wave peaks and reflection losses are not predicted.',
'在入口與出口配置同步壓力計，用互相關估計傳遞時間，並用溫度估算音速；列車里程觸發另存一條通道。~Use synchronised pressure sensors at both portals, estimate travel time by cross-correlation and sound speed from temperature, and retain train-position triggering separately.',
'時間戳誤差會被誤認為波速變化；長隧道的反射波與多車事件也可能讓互相關找到錯誤的峰。~Timestamp error can imitate a wave-speed change, while reflected waves and multiple train events can make cross-correlation select the wrong peak.',
'隧道壓力波必定與列車以相同速度到達出口~A tunnel pressure wave necessarily reaches the portal at the same speed as the train.',
'比較壓力波與列車兩種到達時間，加入一次端部反射畫出事件圖，說明單一延遲量無法判斷出口微壓波是否超標。~Compare wave and train arrival times, add one end reflection to the event diagram, and explain why travel time alone cannot establish compliance of portal micro-pressure waves.')

add('pantograph','接觸線張力波速~Contact-wire tension wave speed',
'受電弓擾動會沿接觸線傳播，張力提高使橫波速度上升而線密度增加使波速下降。波速與列車速度的比值提供動態風險線索，但多跨懸掛、吊弦和接觸非線性不能由單根弦模型取代。~Pantograph disturbances propagate along the contact wire. Greater tension raises transverse wave speed, whereas greater mass per length lowers it. The ratio to train speed offers a dynamic clue, but multispan suspension, droppers and contact nonlinearity cannot be replaced by a single-string model.',
{'tension':(20000,'N'),'density':(1.1,'kg/m')},'(tension/density)**0.5',('wave_speed','m/s'),
'無彎曲剛度的均勻張弦；不是受流合格判定或允許車速。~Uniform tensioned string without bending stiffness; not a current-collection acceptance rule or permitted train speed.',
'核對補償裝置行程、線溫與張力紀錄，再量測受電弓接觸力統計及離線事件，辨別平均值正常但峰值異常。~Check compensation travel, wire temperature and tension, then examine contact-force statistics and loss-of-contact events to distinguish acceptable means from abnormal peaks.',
'補償裝置卡滯會讓溫度變化改變張力，吊弦鬆弛又會改變局部動態剛度；只讀取靜態高度難以辨識。~A sticking tensioning device lets temperature change tension, while slack droppers change local dynamic stiffness; static wire height alone cannot identify either mechanism.',
'只要靜態接觸線高度正確就能保證高速受流品質~Correct static contact-wire height alone guarantees good current collection at high speed.',
'將張力降低一成和線密度增加一成分別計算波速，列出尚需哪些接觸力量測才能討論動態受流品質。~Reduce tension and increase wire mass density separately by ten percent, calculate wave speed, and identify the contact-force measurements still needed to assess dynamic collection.')

add('thermal','長軌溫升與受限熱應力~Long-rail temperature and restrained stress',
'自由鋼軌升溫會伸長，完全拘束的理想鋼軌則把熱應變轉成壓應力。鎖定軌溫決定應力零點而空氣溫度不等於鋼軌溫度；實際扣件滑移與軌道側向阻力還會改變穩定問題。~A free rail expands on heating, while an ideally restrained rail converts thermal strain into compression. Stress-free rail temperature defines the reference and differs from air temperature. Fastener slip and lateral track resistance additionally govern stability, beyond the one-dimensional thermal-stress estimate.',
{'E':(210000,'MPa'),'alpha':(0.0000115,'1/K'),'deltaT':(30,'K')},'E*alpha*deltaT',('compression','MPa'),
'完全軸向拘束與線彈性；不計挫曲、初彎、殘留應力及塑性。~Full axial restraint and linear elasticity; buckling, initial curvature, residual stress and plasticity are excluded.',
'量鋼軌本體溫度與縱向應變，記錄鎖定狀態和扣件維修歷程，用不同位置感測器區分局部溫差與整段受限變形。~Measure rail temperature and longitudinal strain, record the fastening and maintenance history, and use spatially separated sensors to distinguish local heating from restrained segment behaviour.',
'把氣溫直接當成鋼軌溫度會錯估熱荷載；扣件鬆動可能降低局部軸力卻增加位移，不能據此宣稱整體穩定性改善。~Substituting air temperature misstates thermal loading; loose fasteners may reduce local force while increasing displacement, which does not prove improved overall stability.',
'完全拘束的鋼軌升溫仍會無應力地自由伸長~A fully restrained rail still expands freely without stress when heated.',
'畫出自由、部分拘束與完全拘束三種邊界，重算熱變形或應力，標明哪些輸入必須由鋼軌溫度及扣件試驗取得。~Draw free, partial and full restraint boundaries, recalculate expansion or stress, and identify inputs requiring rail-temperature measurements and fastener tests.')

add('seismic','地震偵測提前量~Seismic detection lead time',
'地震警報的可用提前量來自較快波到達感測點與較慢強震波到達設施之間的差，再扣掉傳輸和判定延遲。距離太近時提前量可能為負，警報並不能讓列車瞬間停止。~Usable seismic lead time is the difference between faster-wave detection and slower damaging-wave arrival, less communication and decision delay. A nearby source may leave negative lead time. An alarm therefore cannot make a moving train stop instantaneously, even when the detection itself works correctly.',
{'distance':(100000,'m'),'vp':(6000,'m/s'),'vs':(3500,'m/s'),'latency':(2,'s')},'distance/vs-distance/vp-latency',('lead','s'),
'共線源站幾何與固定波速；不預測震度或實際地震動。~Collinear source-station geometry and constant wave speeds; neither intensity nor actual ground motion is predicted.',
'用歷史或合成波形重播整條訊號鏈，記錄偵測、判定、通訊及列車接收時間，量出漏警、誤警和延遲分布。~Replay historical or synthetic waveforms through the complete chain, log detection, decision, communication and train receipt times, and measure missed alarms, false alarms and latency distribution.',
'只驗證感測器觸發而不驗證下游通訊，可能高估提前量；設備共用電源也可能讓兩條名義獨立通道同時失效。~Testing the sensor without downstream communication overestimates lead time; a shared power supply can also defeat nominally independent channels simultaneously.',
'地震預警成功觸發就代表列車必能在強震前完全停下~A successfully triggered earthquake warning guarantees a complete stop before strong shaking.',
'將震源距離縮短並把通訊延遲加倍，計算剩餘提前量；與制動時間比較，提出只在模型範圍內成立的結論。~Shorten source distance and double communication delay, calculate remaining lead time, and compare it with braking time without extending the conclusion beyond the model.')

add('settlement','沉陷差與軌道坡折~Differential settlement and track kink',
'均勻沉陷主要改變高程，短距離差異沉陷則改變軌道坡度和車輪動態荷載。兩端高差除以基長只給平均坡度，無法描述局部尖峰；需要多點剖面才能辨認曲率與變形長度。~Uniform settlement mainly changes elevation, whereas differential settlement over a short distance alters track slope and dynamic wheel loading. End-to-end difference divided by baseline gives only an average gradient, not a local peak. A spatial profile is needed to identify curvature and deformation length.',
{'drop':(0.012,'m'),'baseline':(20,'m')},'1000*drop/baseline',('gradient','mm/m'),
'小變形平均坡度；不計車軌耦合動力或容許軌道幾何。~Small-deformation average gradient; vehicle-track dynamics and permissible geometry limits are excluded.',
'採用同一穩定水準基點反覆量測，保留溫度和施工時間，利用多點高程剖面區分整段平移、坡折與量測基點漂移。~Repeat surveys against one stable datum, retain temperature and construction timing, and use multipoint profiles to separate translation, kinks and datum drift.',
'基點本身下沉會讓全段看似正常；只量端點又會漏掉中間沉陷槽，兩種情況均可低估輪軌衝擊。~A settling datum can hide movement of the whole section, and endpoint-only measurement misses an intermediate trough; both may understate wheel-rail impact.',
'兩端高程相同就能證明兩點之間沒有差異沉陷~Equal endpoint elevations prove there is no differential settlement between them.',
'構造端點相同但中間下陷的剖面，與直線坡度模型比較；提出足以辨識沉陷槽寬度的測點間距與複測頻率。~Construct a profile with equal endpoints and an intermediate trough, compare it with a straight-gradient model, and propose spacing and repeat intervals able to resolve the trough.')

add('bridge','橋梁撓度與跨長敏感度~Bridge deflection and span sensitivity',
'簡支梁在均布荷載下的撓度對跨長有四次方敏感度，截面慣性矩與材料剛度共同抵抗彎曲。鐵道橋還需要動態與軌道相互作用檢查，靜態梁算例只用來辨認參數量級。~For a simply supported beam under uniform load, deflection scales with the fourth power of span. Section inertia and material stiffness jointly resist bending. A railway bridge also requires dynamic and track-interaction checks; this static beam exercise only reveals parameter magnitudes.',
{'w':(50000,'N/m'),'L':(25,'m'),'E':(35000000000,'Pa'),'I':(8,'m^4')},'5*w*L**4/(384*E*I)*1000',('deflection','mm'),
'簡支Euler梁、小撓度、靜態均布荷載；不代表列車移動荷載。~Simply supported Euler beam, small deflection and static uniform load; not a moving train-load analysis.',
'在已知載重位置量測跨中和支點位移，扣除支承沉陷後對照彎矩圖，並用卸載後讀值檢查是否存在殘留變形。~Measure midspan and support movement under known loading, subtract support settlement, compare with the moment diagram, and inspect residual displacement after unloading.',
'支承鬆動或局部開裂可能改變有效剛度，若把所有位移都當成梁彎曲，校準出的彈性模數就會失真。~Loose supports and local cracking alter effective stiffness; interpreting all displacement as beam bending produces a misleading calibrated elastic modulus.',
'橋梁跨長增加一成其彈性撓度最多只增加一成~Increasing bridge span by ten percent increases elastic deflection by at most ten percent.',
'保持截面不變增加跨長，再比較提高慣性矩的補償幅度，說明靜態位移符合預期為何仍不能取代動態驗證。~Increase span while keeping the section fixed, calculate the compensating inertia change, and explain why agreement in static deflection cannot replace dynamic verification.')

add('suspension','懸吊固有頻率與激振~Suspension frequency and excitation',
'彈簧與質量的組合決定垂向固有頻率，增加質量降低頻率而提高剛度使頻率升高。軌道不平順被車速轉換成時間激振；因此相同軌道波長在不同速度下可能接近或遠離共振。~Spring stiffness and supported mass determine vertical natural frequency. Added mass lowers frequency, while increased stiffness raises it. Train speed converts spatial track irregularity into temporal excitation, so the same wavelength may approach or leave resonance as speed changes.',
{'k':(900000,'N/m'),'mass':(12000,'kg')},'(k/mass)**0.5/(2*3.141592653589793)',('frequency','Hz'),
'單自由度無阻尼模型；不含俯仰、側滾與輪軌接觸。~Undamped single-degree-of-freedom model; pitch, roll and wheel-rail contact are excluded.',
'量測已知質量下的自由衰減與頻率響應，對照不同載客狀態；同步記錄軌道波長和速度，避免混淆激振頻率與固有頻率。~Measure free decay and frequency response at known mass, repeat for different passenger loading, and log track wavelength and speed to distinguish excitation from natural frequency.',
'只調剛度追求低頻隔振可能增加行程需求；阻尼器失效可能保持固有頻率近似不變，卻大幅增加共振振幅。~Softening springs for low-frequency isolation increases travel demand; a failed damper may barely change natural frequency while greatly increasing resonant amplitude.',
'量到固有頻率不變就能證明阻尼器沒有劣化~An unchanged natural frequency proves that the damper has not deteriorated.',
'比較空車與滿載頻率，計算一個指定波長對應的激振速度，並列出阻尼與行程限制對判斷的影響。~Compare empty and loaded frequencies, calculate the speed corresponding to one irregularity wavelength, and explain the influence of damping and suspension travel limits.')

add('wheelheat','煞車熱量與溫升~Brake heat and temperature rise',
'未回收的動能會在摩擦煞車與阻力路徑中轉成熱，平均溫升由分配到構件的能量除以熱容量決定。短時平均模型無法描述表面熱點、對流冷卻或熱裂紋，需要把能量分配與熱擴散分開。~Unrecovered kinetic energy becomes heat through friction brakes and resistance paths. Average temperature rise is allocated energy divided by thermal capacity. A short-duration lumped model cannot describe surface hot spots, cooling or thermal cracks; energy allocation and thermal diffusion are separate questions.',
{'energy':(12000000,'J'),'mass':(220,'kg'),'cp':(460,'J/(kg*K)')},'energy/(mass*cp)',('rise','K'),
'均勻溫度且無散熱、常數比熱；不推定摩擦材極限。~Uniform temperature without heat loss and with constant heat capacity; no friction-material limit is inferred.',
'以熱電偶與紅外量測交叉檢查溫升，記錄煞車能量、環境溫度與冷卻時間，並校正紅外放射率。~Cross-check temperature rise with thermocouples and infrared measurements, record braking energy, ambient temperature and cooling time, and calibrate infrared emissivity.',
'局部接觸不均會產生熱點，即使平均溫升不高仍可能形成熱裂紋；錯誤放射率也會掩蓋真實表面溫度。~Uneven contact can create hot spots and thermal cracks despite a modest mean rise; incorrect emissivity can also conceal the actual surface temperature.',
'煞車盤平均溫度低就能保證局部沒有熱點~A low mean brake-disc temperature guarantees the absence of local hot spots.',
'將同一能量分給兩種有效熱容量，計算平均溫升後設計能辨認熱點的量測網格，說明集中參數模型缺少哪些資訊。~Allocate equal energy to two effective thermal capacities, calculate average rise, and design a measurement grid for hot spots while identifying information missing from the lumped model.')

add('adhesion','黏著限制與可用牽引力~Adhesion limit and usable traction',
'牽引力需要透過接觸斑傳到軌道，簡化上限與黏著係數及動輪法向力相乘。電機能提供更大扭矩不代表輪軌能傳遞；雨水、落葉與速度都會改變接觸狀態，使固定係數模型失去精度。~Traction reaches the track through contact patches. A simple upper bound multiplies adhesion coefficient by normal force on driven wheels. More motor torque does not guarantee more transmitted force; rain, leaves and speed alter contact conditions and limit the accuracy of a fixed coefficient.',
{'mu':(0.18,'1'),'weight':(900000,'N')},'mu*weight/1000',('traction','kN'),
'準靜態庫倫上限與均勻輪重；未建模蠕滑曲線及動態減載。~Quasi-static Coulomb bound with uniform wheel load; creep curves and dynamic unloading are not modelled.',
'比較輪速、列車獨立速度與牽引電流，找出滑轉開始點；濕乾條件必須分組，不能用全日平均係數掩蓋低黏著尾端。~Compare wheel speed, independently measured train speed and traction current to locate slip onset, separating wet and dry conditions rather than hiding low-adhesion tails in a daily mean.',
'只提高扭矩可能觸發滑轉並降低可控牽引；輪徑設定誤差也會製造假的滑差，需以獨立地速判別。~Increasing torque can trigger slip and reduce controllable traction; an incorrect wheel diameter also creates apparent slip, requiring independent ground-speed evidence.',
'電機額定扭矩夠大就不需要考慮輪軌黏著~A sufficiently large rated motor torque eliminates the need to consider wheel-rail adhesion.',
'把黏著係數減半並比較動輪荷重調整，計算牽引上限，解釋為何撒砂或控制策略的效果需用試驗而不能只看馬達功率。~Halve adhesion and compare a change in driven-wheel load, calculate traction bounds, and explain why sanding or control performance requires tests rather than motor-power data alone.')

add('grade','坡度阻力與爬坡功率~Gradient resistance and climbing power',
'列車爬坡需提高重力位能，坡度小時沿線重力分量約等於重量乘坡度。功率還與速度相乘，因此相同牽引力下高速爬坡更耗功率；下坡則需處理持續制動能量而非僅一次停車。~Climbing raises gravitational potential energy. For small gradients, the along-track gravity force is approximately weight times gradient. Multiplication by speed gives power, making faster climbing more demanding at equal force; descending requires continuous energy management rather than merely one stopping event.',
{'mass':(300000,'kg'),'gradient':(0.02,'1'),'v':(40,'m/s')},'mass*9.81*gradient*v/1000',('climbing','kW'),
'小坡度且定速；不含空阻、輪阻、加速與傳動損失。~Small gradient and constant speed; aerodynamic drag, rolling resistance, acceleration and drive losses are excluded.',
'以路線縱斷面和列車速度重建位能變化，對照受電功率積分；坡度資料與里程基準必須一致。~Reconstruct potential-energy change from the vertical alignment and train speed, compare it with integrated line power, and keep gradient and distance datums consistent.',
'忽略長下坡持續熱負荷會把短時煞車能力誤當連續能力；坡度正負號錯誤則會把耗能段當成回收段。~Ignoring sustained downhill heat confuses short-term braking capability with continuous rating; a gradient-sign error can mislabel an energy-consuming section as regenerative.',
'長下坡只需通過一次緊急停車試驗就能驗證持續制動~One emergency stop test verifies continuous braking capability on a long descent.',
'用相同高差設計長緩坡與短陡坡，對比理想位能和峰值功率，指出兩者為何不能用同一項設備額定值評估。~Design a long gentle and short steep climb with equal height gain, compare ideal energy and peak power, and explain why one equipment rating cannot evaluate both.')

add('voltage','牽引饋線壓降~Traction feeder voltage drop',
'牽引電流經導體與回流路徑產生壓降，電壓下降又可能讓定功率列車要求更大電流，形成非線性負荷互動。單一電阻模型先隔離線路損耗，再逐步引入雙端供電和多列車位置。~Current through the feeder and return path creates voltage drop. A constant-power train may draw more current as voltage falls, creating nonlinear load interaction. A single resistance model first isolates line loss before adding two-ended supply and multiple train positions.',
{'current':(1500,'A'),'resistance':(0.06,'ohm')},'current*resistance',('drop','V'),
'固定電流與集中等效電阻；不含回生、功率因數與暫態。~Fixed current and lumped equivalent resistance; regeneration, power factor and transients are excluded.',
'同步量測變電所與列車端電壓及電流，記錄列車位置，將接頭接觸電阻與導體溫度造成的變化分別辨識。~Synchronise substation and train voltage and current measurements, log train position, and distinguish joint contact resistance from conductor-temperature changes.',
'高阻接頭可能在總壓降看似可接受時局部過熱；把導體長度和回流路徑計算一半會系統性低估損耗。~A high-resistance joint may overheat while total drop looks modest; omitting part of the return path systematically understates resistance and losses.',
'量到變電所輸出電壓正常就代表所有列車端電壓正常~Normal substation output voltage proves that every train receives normal voltage.',
'加入第二列同時加速的列車，畫出共享與非共享饋線段，分段重算壓降並說明何時需改用完整潮流分析。~Add a second accelerating train, distinguish shared and separate feeder sections, recalculate each drop, and explain when a complete load-flow analysis becomes necessary.')

add('powerloss','電流平方損耗與散熱~Current-squared losses and cooling',
'導體與接點的焦耳熱與電流平方成正比，短時高電流可能主導熱循環而平均電流看不出來。散熱取決於環境與接觸表面，電氣損耗量不能直接當成最終溫升。~Joule heating in conductors and joints scales with current squared, so short current peaks can dominate thermal cycling even when mean current looks moderate. Heat rejection depends on environment and contact surfaces; electrical loss alone is not a final temperature prediction.',
{'current':(1200,'A'),'resistance':(0.025,'ohm')},'current*current*resistance/1000',('loss','kW'),
'恆定電阻且直流或等效均方根電流；不含散熱暫態。~Constant resistance with direct or equivalent RMS current; transient cooling is excluded.',
'以均方根電流而非算術平均電流求熱負荷，同步記錄接頭溫度及環境；停電隔離後才由合格人員檢查接點。~Use RMS rather than arithmetic-mean current for thermal loading, log joint and ambient temperatures, and restrict physical inspection to qualified staff after isolation.',
'鬆動接點會增加電阻並使熱量集中；熱像單次讀值偏低也可能只是量測時負載不高，不能否定間歇性過熱。~Loose joints increase resistance and concentrate heating; a cool one-time thermal image may simply coincide with low load and cannot rule out intermittent overheating.',
'用平均電流代入平方損耗公式總能得到正確熱負荷~Squaring average current always gives the correct resistive heat load.',
'比較固定電流與同平均值脈衝電流的均方根，計算兩種損耗，寫出溫度監測與電流紀錄需要同步的原因。~Compare constant and pulsed currents with equal means, calculate their RMS losses, and explain why current and temperature records must be time-aligned.')

add('isolation','振動隔離與頻率比~Vibration isolation and frequency ratio',
'浮動道床可用彈簧質量阻尼器理解，其隔振效果取決於激振頻率與固有頻率的比值。接近共振時柔軟支承反而會放大響應，超過隔振區後才可能衰減；靜態撓度與動態效果需要同時檢查。~A floating track slab can be understood as a spring-mass-damper system whose isolation depends on excitation-to-natural-frequency ratio. Soft support can amplify response near resonance before attenuating higher frequencies. Static deflection and dynamic performance therefore need to be checked together.',
{'ratio':(3,'1'),'zeta':(0.12,'1')},'((1+(2*zeta*ratio)**2)/((1-ratio**2)**2+(2*zeta*ratio)**2))**0.5',('transmissibility','1'),
'線性單自由度力傳遞率；不含土層波傳、側向耦合及建築響應。~Linear single-degree-of-freedom force transmissibility; soil propagation, lateral coupling and building response are excluded.',
'同步量測軌道、道床與鄰近結構振動，使用頻譜比值而非只比較總加速度，並記錄列車速度與載重。~Measure rail, slab and neighbouring-structure vibration synchronously, compare spectra rather than only overall acceleration, and retain train speed and load.',
'隔振墊硬化會提高固有頻率，局部短路接觸則繞過彈性路徑；兩者都可能讓預期隔振頻段失效。~Pad hardening raises natural frequency, while a rigid local contact bypasses the elastic path; either can remove the intended isolation band.',
'支承越柔軟所有頻率的振動就一定越小~Softer supports necessarily reduce vibration at every frequency.',
'計算接近共振與高頻兩種頻率比，畫出傳遞率趨勢，提出能辨別材料硬化與剛性短路的量測位置。~Calculate near-resonant and high-frequency ratios, plot the transmission trend, and propose sensor locations distinguishing material hardening from a rigid bypass.')

add('localize','里程融合與不確定度~Position fusion and uncertainty',
'獨立位置感測器可用變異數倒數加權，但只有誤差不相關且偏差已校正時，融合後不確定度才按公式下降。輪徑誤差和共同地圖偏差可能讓多個通道一起偏移，不能靠增加感測器數量消除。~Independent position measurements can be weighted by inverse variance, but uncertainty decreases as predicted only when errors are uncorrelated and biases have been corrected. Wheel-diameter error and shared map bias can shift multiple channels together, so merely adding sensors does not remove systematic error.',
{'s1':(4,'m'),'s2':(2,'m')},'(1/(1/s1**2+1/s2**2))**0.5',('sigma','m'),
'零均值獨立高斯誤差；不含共同偏差與完整性風險。~Independent zero-mean Gaussian errors; common bias and integrity risk are excluded.',
'以獨立已知控制點比較融合前後殘差，逐段檢查偏差及相關性，並故意遮蔽一個感測器觀察降級行為。~Compare pre-fusion and post-fusion residuals at independently surveyed points, check bias and correlation by segment, and mask one sensor to inspect degraded operation.',
'共用錯誤地圖會讓兩個感測器看似一致卻都錯；錯把相關訊號當獨立會使報告的置信區間過窄。~A shared wrong map can make two sensors agree while both are wrong; treating correlated signals as independent produces an overconfident interval.',
'兩個定位來源彼此一致就能保證定位沒有共同偏差~Agreement between two position sources guarantees absence of common bias.',
'建立獨立誤差與共同偏差兩組資料，對比融合結果，指出哪一種誤差需要外部控制點才能發現。~Construct independent-error and common-bias datasets, compare their fused results, and identify the error requiring an external control point for detection.')

add('communication','通訊延遲與位置陳舊量~Communication delay and stale position',
'移動列車在訊息傳遞期間繼續前進，最簡單的陳舊位置上界是速度乘延遲。封包延遲、遺失與時鐘偏差應分開，平均延遲不能代表最壞情況，也不能直接替代列車保護的安全論證。~A moving train advances while a message is in transit. Speed times delay gives the simplest stale-position bound. Packet delay, loss and clock bias must be separated; mean latency neither represents a worst case nor replaces a safety argument for train protection.',
{'v':(25,'m/s'),'latency':(0.3,'s')},'v*latency',('stale_distance','m'),
'固定速度且單次訊息延遲；未含加速度、連續遺失及協定重試。~Constant speed and one delayed message; acceleration, consecutive losses and protocol retries are excluded.',
'以送出和接收兩端的同步時間戳量延遲分布，注入延遲及封包遺失，確認過期訊息被辨識而非繼續當成即時位置。~Measure latency distribution using synchronised transmit and receive timestamps, inject delay and packet loss, and confirm stale messages are identified rather than treated as current position.',
'時鐘漂移可能讓過期訊息被誤判為新資料；只測低負載網路會漏掉交接區、干擾和突發流量造成的延遲尾端。~Clock drift can make stale data appear fresh; low-load tests miss latency tails caused by handover, interference and burst traffic.',
'平均網路延遲很低就足以證明所有控制訊息都及時到達~A low average network delay proves that every control message arrives on time.',
'把速度與延遲各提高一成，比較位置陳舊量；設計含連續遺失的重播案例，列出接收端需要保留的時間與序號資訊。~Increase speed and delay separately, compare stale distance, and design a replay with consecutive losses listing the timestamps and sequence information required at the receiver.')

add('interlock','互斥進路與真值驗證~Conflicting routes and truth-table verification',
'聯鎖的核心是明確禁止衝突進路同時成立，安全條件需要由占用、道岔鎖閉和列車完整通過共同決定。狀態數隨布林輸入快速增加，真值表可檢查邏輯完整性，但不能代替時序與硬體故障分析。~Interlocking explicitly excludes simultaneous conflicting routes. Occupancy, locked points and complete train passage jointly determine permissive conditions. Boolean input combinations grow rapidly; a truth table checks logical coverage but does not replace timing analysis or hardware fault assessment.',
{'inputs':(6,'Boolean inputs')},'2**inputs',('combinations','states'),
'有限個獨立二值輸入的完整枚舉；不代表實際聯鎖軟體測試已完成。~Complete enumeration of independent binary inputs; not a claim that real interlocking software has been tested.',
'把每個允許輸出對應到必要條件，逐項加入反例測試；再檢查占用訊號失效或道岔未鎖閉時是否回到禁止狀態。~Map every permissive output to its necessary conditions, add counterexample tests, and check that occupancy failure or unlocked points leads to a restrictive state.',
'只測正常進路順序會漏掉同時請求和殘留狀態；感測器卡在允許值也可能使紙上正確的邏輯收到錯誤輸入。~Testing only the normal route sequence misses simultaneous requests and residual states; a sensor stuck permissive can feed wrong inputs to otherwise correct logic.',
'聯鎖只要正常路徑通過測試就不需要檢查衝突請求~Passing normal route tests removes the need to test conflicting requests.',
'為兩條衝突進路建立真值表，標記禁止組合，再加入先占用後解鎖的事件序列，說明組合邏輯和時序邏輯的差異。~Build a truth table for two conflicting routes, mark forbidden combinations, then add occupancy and release event sequences to distinguish combinational from temporal logic.')

add('brakecurve','速度限制轉換與預告距離~Speed-limit transition and warning distance',
'進入較低速區前需把速度差轉成足夠的減速距離，能量式包含初速與目標速度的平方差。此處用明示減速度得到教學距離，真正保護曲線還需加入定位誤差、坡度、制動建立及車輛差異。~Before entering a lower-speed section, the train needs distance to remove the difference in kinetic energy. The expression contains the difference of squared initial and target speeds. A teaching deceleration gives one distance; a real protection curve additionally needs position uncertainty, gradient, brake build-up and vehicle variation.',
{'initial':(70,'m/s'),'target':(40,'m/s'),'a':(0.65,'m/s^2')},'(initial**2-target**2)/(2*a)',('transition','m'),
'初速大於目標速度且定減速度；沒有通訊延遲與安全裕度。~Initial speed above target and constant deceleration; communication delay and safety margins are excluded.',
'重播速度剖面並檢查每個限制點的里程基準，將定位誤差和煞車建立時間分別加入，不以單次成功停準代替整個包絡驗證。~Replay speed profiles with a common distance datum, add positioning error and brake build-up separately, and do not substitute one successful stop for verification of the full envelope.',
'限制點座標偏移或單位錯誤會使制動開始過晚；過度依賴平均減速度則可能漏掉低黏著條件下的長制動距離。~A shifted restriction coordinate or unit error causes late braking, while reliance on mean deceleration can miss long stopping distances under low adhesion.',
'降低目標速度時可忽略初速與目標速度的平方差~Reducing target speed allows the squared-speed difference to be ignored.',
'對同一初速設定兩個目標速度，重算轉換距離，畫出能量差並說明為何不能按速度差線性縮放距離。~Use two target speeds at one initial speed, recalculate transition distance, plot the energy differences, and explain why distance cannot scale linearly with the speed difference.')

add('axle','軸重與接觸面平均壓力~Axle load and mean contact pressure',
'輪軌接觸面積很小，使局部壓力量級遠高於車體平均承載壓力。荷載除以假設接觸面積只給平均值，真實赫茲接觸的壓力分布與輪軌曲率有關，不能拿平均壓力直接判斷疲勞壽命。~The small wheel-rail contact area creates local pressures far above average body-support pressures. Dividing load by an assumed area gives only the mean. The actual Hertzian distribution depends on wheel and rail curvature, so mean pressure cannot directly establish fatigue life.',
{'wheel_force':(85000,'N'),'area':(0.00015,'m^2')},'wheel_force/area/1e6',('mean_pressure','MPa'),
'已給定均勻接觸面積；不求赫茲橢圓、塑性和滾動接觸疲勞。~Prescribed uniform contact area; Hertz ellipse, plasticity and rolling-contact fatigue are not solved.',
'比對輪重與輪軌斷面量測，檢查磨耗是否改變接觸位置，再以接觸模型預測壓力分布而非只用平均值。~Compare wheel loads with measured wheel and rail profiles, check wear-induced contact shifts, and use a contact model for the distribution rather than the mean alone.',
'磨耗或輪緣接觸會改變接觸斑與應力集中；單純以軸重相同推論損傷相同，會忽略曲率及側向力差異。~Wear and flange contact change patches and stress concentration; equal axle load does not imply equal damage when curvature and lateral forces differ.',
'兩列車軸重相同就必定具有相同輪軌接觸疲勞壽命~Equal axle loads necessarily give equal wheel-rail rolling-contact fatigue life.',
'在相同輪重下把接觸面積減少一成，計算平均壓力，再列出需要輪軌斷面及材料資料才能推估的項目。~Reduce contact area by ten percent at fixed wheel load, calculate mean pressure, and list predictions requiring measured profiles and material data.')

add('fatigue','重複荷載與線性損傷帳~Repeated loading and linear damage account',
'疲勞取決於應力範圍與循環次數，線性累積把各級循環數除以對應壽命後相加。此帳務能比較荷載譜，卻忽略順序效應、腐蝕與裂紋成長，損傷和為一不是對任何構件的通用失效保證。~Fatigue depends on stress range and cycle count. Linear accumulation sums the fraction of life consumed at each level. This accounting compares load spectra but omits sequence effects, corrosion and crack growth; a sum of one is not a universal failure guarantee for every component.',
{'n1':(200000,'cycles'),'N1':(1000000,'cycles'),'n2':(50000,'cycles'),'N2':(250000,'cycles')},'n1/N1+n2/N2',('damage_index','1'),
'兩級循環的Miner帳務且壽命輸入已假設；不外推真實剩餘壽命。~Two-level Miner accounting with assumed life values; no real residual-life prediction is made.',
'以雨流計數整理應變歷程，核對儀器零漂與列車通過事件，保留應力轉換和材料曲線的來源與適用範圍。~Count strain histories using rainflow analysis, check sensor drift against train passages, and retain the source and applicability of stress conversion and material curves.',
'漏記少量大應力循環可能比漏記大量小循環更嚴重；焊趾局部應力也不能直接由遠處名義應變代表。~Missing a few large cycles can matter more than missing many small ones; nominal strain away from a weld cannot directly represent local weld-toe stress.',
'疲勞損傷只取決於通過列車總數而不受應力幅影響~Fatigue damage depends only on train count and is independent of stress range.',
'保持總循環數不變，將部分低應力循環移到高應力級，重算損傷帳並說明需要何種檢測來支持剩餘壽命判讀。~Keep total cycles fixed while moving some cycles to the higher-stress level, recalculate damage, and identify inspections needed to support any remaining-life interpretation.')

add('snow','融雪熱量與補給率~Snow-melting heat and supply rate',
'把積雪融化需要先加熱到熔點再供應潛熱，若雪已在熔點則主要負荷是融化潛熱。積雪落在轉轍器附近會妨礙動作，融化後排水若再凍結也可能重新形成阻塞。~Melting snow requires heating it to the melting point and supplying latent heat; snow already at that temperature mainly requires latent heat. Snow near point mechanisms can obstruct movement, while meltwater that refreezes may create another obstruction even after initial melting succeeds.',
{'snow':(0.04,'kg/s'),'latent':(334000,'J/kg')},'snow*latent/1000',('melt_power','kW'),
'雪初溫為熔點且無環境散熱；僅理論潛熱功率。~Snow initially at melting point with no environmental losses; latent-heat power only.',
'量測進雪質量、融水流率及加熱電功率，記錄周圍溫度與風速，檢查能量帳和排水是否一致。~Measure snow mass input, meltwater flow and electrical heating power, log ambient temperature and wind, and check consistency of both the energy balance and drainage.',
'加熱器正常卻排水結冰時仍可能阻塞道岔；只量加熱器溫度不能確認冰雪已從關鍵間隙移除。~A working heater can coexist with frozen drainage and obstructed points; heater temperature alone does not prove snow has cleared the critical gap.',
'只要加熱器表面很熱就表示道岔冰雪問題已解決~A hot heater surface proves that snow and ice obstruction at the points is resolved.',
'加入初始低於冰點的顯熱與散熱兩項需求，重新列出能量收支，並為排水再凍結設計獨立的觀察點。~Add sensible heating below freezing and environmental losses to the balance, then design an independent observation point for drainage refreezing.')

add('crosswind','側風力與翻覆力矩~Crosswind force and overturning moment',
'側風作用可由動壓乘有效側向面積估算，再乘作用高度形成翻覆力矩。車輛質量、重心、風向及橋面遮蔽同時影響輪重分配，單一靜態力矩只能提供比較而非營運風速門檻。~Crosswind force can be estimated from dynamic pressure and effective lateral area, then multiplied by application height for an overturning moment. Mass, centre of gravity, wind direction and shielding affect wheel loading together; one static moment only supports comparison, not an operational wind threshold.',
{'rho':(1.2,'kg/m^3'),'wind':(25,'m/s'),'side_area':(90,'m^2'),'coefficient':(1.0,'1'),'height':(2,'m')},'0.5*rho*wind**2*side_area*coefficient*height/1000',('moment','kN*m'),
'定常橫風與已假設氣動係數；不含陣風、列車運動與動態輪重減載。~Steady crosswind and assumed aerodynamic coefficient; gusts, train motion and dynamic unloading are excluded.',
'同步記錄沿線風速、風向、列車速度及車體側滾，檢查風速站是否受地形遮蔽，再用多點資料評估代表性。~Synchronise wind speed, direction, train speed and carbody roll, inspect terrain shielding at the anemometer, and assess representativeness with multiple locations.',
'受遮蔽的風速計可能低估橋上曝露，空載與滿載車又具有不同抗翻覆力矩；不能只用最近測站單一讀值。~A sheltered anemometer can understate exposure on a viaduct, and empty versus loaded vehicles have different restoring moments; the nearest sensor alone is insufficient.',
'側風翻覆力矩只和風速成正比而不涉及車體高度~Crosswind overturning moment is linear in wind speed and independent of vehicle height.',
'把風速與作用高度各增加一成，對比力矩敏感度，提出能區分地形加速與儀器誤差的多點量測配置。~Increase wind speed and load height separately by ten percent, compare moment sensitivity, and propose measurements distinguishing terrain acceleration from instrument error.')

add('noise','聲能相加與分貝~Sound-energy addition and decibels',
'分貝是對數量，兩個聲源不能直接把分貝數字相加。非相干聲源需先還原相對聲能再合成，頻帶、量測位置及時間加權若不同，表面上相同的數值也不能直接比較。~Decibels are logarithmic, so sound levels cannot be added as ordinary numbers. Incoherent sources must first be converted to relative acoustic energy. Different bands, measurement positions or time weightings prevent direct comparison even when displayed values happen to match.',
{'L1':(70,'dB'),'L2':(67,'dB')},'10*log10(10**(L1/10)+10**(L2/10))',('combined','dB'),
'相同基準與加權的非相干聲源；不含相位干涉與背景扣除。~Incoherent sources with the same reference and weighting; phase interference and background subtraction are excluded.',
'同時保留背景、列車通過和設備單獨運轉紀錄，確認麥克風校正、距離與頻帶設定一致，避免把不同時間窗混合。~Retain background, train-passage and equipment-only recordings, confirm microphone calibration, distance and frequency settings, and avoid mixing incompatible time windows.',
'未扣除背景可能高估列車貢獻，錯用算術平均則低估高噪事件；屏障缺口還可能讓局部接收點明顯偏高。~Unremoved background can overstate train contribution, while arithmetic averaging understates loud events; barrier gaps can also produce local receiver hot spots.',
'兩個七十分貝聲源同時工作一定產生一百四十分貝~Two seventy-decibel sources operating together necessarily produce one hundred forty decibels.',
'比較相同聲級與相差十分貝的兩聲源合成，列出背景扣除的適用條件，並解釋聲壓幅與聲能的對數係數差異。~Combine equal-level sources and sources ten decibels apart, list the conditions for background subtraction, and explain the different logarithmic factors for pressure amplitude and energy.')

add('drain','集水與排水容量~Catchment inflow and drainage capacity',
'短時逕流可先以降雨強度、集水面積和逕流係數估計，但設施排水還受入口阻塞、管線坡度與下游水位影響。鐵路集水範圍若只算軌道面，會漏掉坡面與站區流入。~A first runoff estimate combines rainfall intensity, catchment area and runoff coefficient. Actual drainage also depends on inlet blockage, pipe slope and downstream water level. Counting only track surface can omit inflow from adjacent slopes and station areas.',
{'coefficient':(0.85,'1'),'rain':(0.00002,'m/s'),'area':(18000,'m^2')},'coefficient*rain*area',('flow','m^3/s'),
'均勻降雨的合理化法概念；不含集流時間、水文頻率分析或蓄滯。~Uniform-rainfall rational-method concept; concentration time, frequency analysis and storage are excluded.',
'現地核對集水分界和入口標高，以雨量、液位與泵浦運轉紀錄檢查水量收支，分開分析正常排放和下游頂托。~Check catchment boundaries and inlet elevations, use rainfall, water-level and pump logs for a balance, and distinguish normal outflow from downstream backwater.',
'垃圾堵塞入口會讓理論管徑容量無法發揮；下游水位上升又可能使出口排量下降，僅加大泵浦不能解決所有原因。~Blocked inlets can prevent nominal pipe capacity from being used, while rising tailwater reduces outflow; a larger pump does not resolve every cause.',
'排水管截面夠大就不需要檢查入口堵塞及下游水位~A sufficiently large drain eliminates the need to check blocked inlets and tailwater.',
'將部分入口視為堵塞，建立地表暫存與排出的水量表；比較增加入口和增加泵量對不同瓶頸的效果。~Block selected inlets in the scenario, tabulate surface storage and discharge, and compare additional inlets with additional pumping for different bottlenecks.')

add('freeze','凍土潛熱與融化厚度~Permafrost latent heat and thaw depth',
'凍土融化需要供應冰的潛熱，單位面積熱量除以體積潛熱可估算理想融化厚度。實際土層含水率、對流與季節反覆凍融會改變結果，融化厚度也不直接等於路基沉陷。~Thawing ground requires the latent heat of its ice. Heat input per area divided by volumetric latent heat gives an ideal thaw depth. Water content, convection and repeated seasonal freezing modify the result, and thaw depth is not identical to embankment settlement.',
{'heat':(12000000,'J/m^2'),'ice_density':(917,'kg/m^3'),'latent':(334000,'J/kg'),'ice_fraction':(0.35,'1')},'heat/(ice_density*latent*ice_fraction)',('thaw_depth','m'),
'全部熱量用於相變且冰分率均勻；不計顯熱、地下水及土骨架壓縮。~All input heat goes to phase change with uniform ice fraction; sensible heat, groundwater and skeleton compression are excluded.',
'將溫度剖面、含冰量和路基高程聯合判讀，固定測點深度基準，避免把感測器隨沉陷移動誤當成融化面下移。~Interpret temperature profiles, ice content and elevation together, maintain a fixed depth datum, and avoid mistaking sensor movement with settlement for a descending thaw front.',
'局部富冰層融化可能造成不均勻沉陷，平均地溫穩定也不能排除某一薄層已跨過相變區。~Thawing an ice-rich lens can cause differential settlement, and a stable average ground temperature does not rule out phase change in a thin layer.',
'計算出的凍土融化厚度必定等於路基沉陷量~Calculated permafrost thaw depth necessarily equals embankment settlement.',
'對兩種含冰率計算理想融化厚度，保持熱量不變，再說明為何需要土骨架壓縮性和排水條件才能推估沉陷。~Calculate ideal thaw depth for two ice fractions at equal heat input, then explain why skeleton compressibility and drainage are required to estimate settlement.')

add('cooling','通風散熱與設備溫升~Ventilation cooling and equipment heat',
'流動空氣帶走的顯熱與質量流率和溫升相乘，風量不足會提高排氣溫度。設備房還存在短路循環和局部熱點，平均送排風溫差不能保證所有電子模組都在同樣環境中。~Air removes sensible heat through mass flow and temperature rise. Insufficient flow raises exhaust temperature. Equipment rooms also contain recirculation and hot spots, so an average supply-to-exhaust difference does not guarantee identical conditions around every electronic module.',
{'heat':(18000,'W'),'density':(1.2,'kg/m^3'),'cp':(1005,'J/(kg*K)'),'flow':(1.2,'m^3/s')},'heat/(density*cp*flow)',('air_rise','K'),
'穩態顯熱且混合均勻；不含潛熱、輻射與空調循環效率。~Steady sensible heat and uniform mixing; latent heat, radiation and refrigeration-cycle efficiency are excluded.',
'同時量送風量、進出口溫度和設備用電，沿機櫃高度布置測點，確認冷風沒有直接繞過設備流回出口。~Measure supply flow, inlet and outlet temperatures and electrical load together, instrument cabinet height, and check that cold air does not bypass the equipment.',
'濾網堵塞或風道短路會降低有效冷卻，即使總風機轉速正常；散熱器積塵也可能提高晶片溫度而房間平均值不變。~A blocked filter or airflow bypass reduces effective cooling despite normal fan speed; dusty heat sinks can raise chip temperature without changing the room average.',
'風機轉速正常就能保證機櫃內每個設備都有足夠散熱~Normal fan speed guarantees adequate cooling for every device in the cabinet.',
'比較降低風量與增加設備負載兩種情況，建立溫升敏感度表，再選出能辨別旁通流和真正熱負荷增加的測點。~Compare reduced flow with increased equipment load, tabulate temperature sensitivity, and choose sensors distinguishing bypass flow from a genuine load increase.')

add('filter','濾網壓差與通風功率~Filter pressure drop and fan power',
'風機必須克服風道與濾網壓差才能輸送空氣，輸入功率近似為壓差乘體積流率再除效率。積塵提高阻力但工作點會沿風機曲線改變，因此固定風量假設只是一種受控比較。~A fan must overcome duct and filter pressure losses to move air. Input power is approximately pressure rise times volume flow divided by efficiency. Dust raises resistance but shifts the operating point on the fan curve, so fixed flow is only a controlled comparison.',
{'pressure':(350,'Pa'),'flow':(2.5,'m^3/s'),'eta':(0.6,'1')},'pressure*flow/eta',('fan_power','W'),
'固定風量與總效率；不包含風機曲線移動和馬達熱限制。~Fixed flow and overall efficiency; fan-curve shifts and motor thermal limits are excluded.',
'同時量濾網前後壓差、實際風量和電功率，用乾淨濾網建立基準，並記錄沙塵、濕度與維修時間。~Measure differential pressure, actual flow and input power together, establish a clean-filter baseline, and record dust exposure, humidity and maintenance timing.',
'旁路漏氣可能讓壓差降低但過濾品質變差；只以壓差低判定良好，會忽略濾網破損和密封失效。~Bypass leakage may lower pressure drop while worsening filtration; a low drop alone can therefore hide a damaged filter or failed seal.',
'濾網壓差越低就一定表示過濾狀況越好~Lower filter pressure drop always means better filtration condition.',
'對堵塞與旁路兩個情境列出壓差、風量和粒子濃度的預期方向，設計三項量測共同判斷而非只靠單一數字。~Predict pressure drop, airflow and particle concentration for clogging and bypass scenarios, then design a three-measurement diagnosis instead of relying on one number.')

add('platform','月台暫存與隊列守恆~Platform storage and queue conservation',
'月台人數是進入、登車與離開人數的累積差，短時尖峰會使隊列成長，即使全天總運能足夠。可用面積應扣除樓梯口、設備與安全帶；密度只能描述平均狀態，不能單獨代表行人動態風險。~Platform population accumulates from arrivals minus boarding and exits. A short surge can grow a queue despite sufficient daily capacity. Usable area excludes stairs, equipment and safety strips. Density describes an average state but does not alone represent dynamic pedestrian risk.',
{'people':(420,'persons'),'usable_area':(350,'m^2')},'people/usable_area',('density','persons/m^2'),
'均勻平均密度；未含局部擠壓、行李和對向人流。~Uniform average density; local compression, luggage and opposing streams are excluded.',
'用匿名計數器核對入口、出口與登車量，分區觀察月台密度，保留列車延誤時間以辨認隊列成長來源。~Reconcile anonymous counts at entrances, exits and train doors, observe density by zone, and retain train-delay times to identify why queues grow.',
'平均密度低仍可能在樓梯出口形成局部瓶頸；計數器漏記同行群體也會使守恆帳不閉合。~A low mean density can coexist with a bottleneck at a stair exit; missed group entries can also prevent the passenger balance from closing.',
'只要月台平均密度低就不會在任何局部出現壅塞~Low average platform density prevents congestion at every local point.',
'模擬一列取消後兩個班距內的人數變化，扣除不能站立的面積，提出分流措施並比較它們改變的是流量還是暫存容量。~Simulate population for two headways after one cancellation, subtract unusable area, and compare whether proposed controls change flow rate or storage capacity.')

add('escalator','垂直動線有效輸送率~Vertical circulation throughput',
'電扶梯的理論輸送率可由速度、梯級間距及每級人數估算，實際值還受入口遲疑、行李和站立習慣限制。多台設備不一定能線性相加，因為共用入口或出口可能先形成瓶頸。~Escalator theoretical throughput follows speed, step pitch and occupants per step. Hesitation, luggage and standing habits limit actual use. Several escalators do not necessarily add linearly when a shared entrance or exit becomes the earlier bottleneck.',
{'speed':(0.5,'m/s'),'pitch':(0.4,'m/step'),'occupants':(1.2,'persons/step')},'3600*speed/pitch*occupants',('throughput','persons/hour'),
'穩定速度和平均梯級占用；不含出入口匯流與無障礙替代路徑。~Steady speed and mean step occupancy; entrance merging and accessible alternative routes are excluded.',
'逐時段計數入口和出口，記錄空梯級比例與行李比例，並在共用平台量隊列長度，避免把額定值當現場值。~Count entrance and exit flow by interval, record empty-step and luggage fractions, and measure the shared-landing queue rather than substituting rated throughput.',
'出口暫停會造成回堵並影響整段動線；一台設備停機時，另一台的入口可能無法吸收全部轉移人流。~A pause at the exit causes spillback through the circulation path; when one escalator is unavailable, the other entrance may not accept all diverted passengers.',
'兩台電扶梯的實際總輸送率必定等於單台額定值兩倍~Two escalators necessarily deliver twice the rated throughput of one escalator.',
'比較一台停機與出口縮窄兩種情境，畫出瓶頸位置，提出電梯與樓梯的替代動線並記錄不同旅客所需時間。~Compare one failed escalator with a narrowed exit, map the bottleneck, and propose lift and stair alternatives while recording journey times for different passenger needs.')

add('doors','停準誤差與月台門對位~Stopping error and platform-door alignment',
'列車停準與月台門對位由列車位置、門中心距和控制容差共同決定。多個獨立誤差可用平方和開根號描述標準差，但系統偏差須另加；幾何對位也不能代替障礙物偵測和關門互鎖。~Train-to-platform door alignment combines stopping position, door spacing and control tolerances. Independent random errors can be combined by root-sum-square, but systematic offsets must be added separately. Geometric alignment does not replace obstruction detection or the door-closure interlock.',
{'stop_sigma':(0.08,'m'),'survey_sigma':(0.02,'m'),'door_sigma':(0.015,'m')},'(stop_sigma**2+survey_sigma**2+door_sigma**2)**0.5',('combined_sigma','m'),
'獨立零均值誤差；不是最大誤差界限，也未給允收公差。~Independent zero-mean errors; not a maximum bound and no acceptance tolerance is specified.',
'以固定月台基準量車門中心偏差，區分重複性與平均偏移，並在載重、方向和制動條件改變時重複測試。~Measure door-centre offset against fixed platform datums, separate repeatability from mean bias, and repeat with changes in load, direction and braking conditions.',
'定位偏差和站台測量偏差可能同向累積，僅看標準差會漏掉系統偏移；門對準也不代表夾物偵測有效。~Position and survey biases may accumulate in the same direction and escape a standard-deviation check; aligned doors also do not prove obstruction detection works.',
'停準誤差標準差小就代表不可能出現固定方向偏移~A small stopping-error standard deviation rules out a persistent directional offset.',
'把隨機誤差和固定偏移分開做誤差預算，畫出不同載重的停準分布，列出對位與互鎖需分別驗證的證據。~Build separate random-error and fixed-bias budgets, plot stopping distributions at different loads, and list distinct evidence for alignment and interlocking.')

add('ventilation','隧道換氣與稀釋時間~Tunnel air exchange and dilution time',
'完全混合空間的濃度在定風量清除下呈指數衰減，體積除以風量給出特徵時間。真實隧道存在分層、死角及列車活塞風，因此這個模型只適合示範稀釋量級，不能直接用作火災避難判定。~A perfectly mixed volume under constant clean-air flow exhibits exponential concentration decay, with volume divided by flow as the time constant. Real tunnels contain layering, stagnant regions and train-induced piston flow. This model illustrates dilution scale and cannot establish fire evacuation tenability.',
{'volume':(3000,'m^3'),'flow':(25,'m^3/s'),'remaining':(0.1,'1')},'-volume/flow*log(remaining)',('dilution_time','s'),
'完全混合且污染源已停止；不含煙層、熱浮力與火災成長。~Perfect mixing after source removal; smoke layers, buoyancy and fire growth are excluded.',
'用非危險示蹤試驗在不同高度與距離採樣，量測實際風量並檢查濃度衰減是否符合單一指數。~Use a harmless tracer test with samples at several heights and distances, measure actual airflow, and check whether one exponential describes the decay.',
'死角可能在平均濃度下降後仍維持高濃度；風機反轉或風門錯位也會改變流路，不能只用風機啟動回饋判斷通風。~Stagnant pockets may remain concentrated after the average falls; reversed fans or misplaced dampers alter flow paths, so a running-status signal alone cannot verify ventilation.',
'風機已經啟動就能證明隧道每一處濃度同樣下降~A running fan proves concentration falls equally at every point in the tunnel.',
'對兩種風量計算達到同一殘餘比例的時間，加入一個不完全混合死角，說明量測配置如何發現模型失配。~Calculate time to one residual fraction at two airflows, add a poorly mixed pocket, and explain how sensor placement can reveal model mismatch.')

add('piston','列車活塞流量與堵塞比~Train piston flow and blockage ratio',
'列車進入受限斷面時排擠空氣，列車截面乘速度提供幾何排量的量級。實際空氣可經車旁間隙、通風井和相鄰隧道分流，因此幾何排量不是某一通風井的實測流量。~A train displaces air in a confined section, and frontal area times speed gives the geometric displacement scale. Air divides through the annular gap, shafts and adjoining tunnels. Geometric displacement therefore does not equal measured flow through a particular ventilation shaft.',
{'train_area':(9,'m^2'),'speed':(20,'m/s')},'train_area*speed',('displacement_flow','m^3/s'),
'不可壓縮幾何排量；未求壓差、流路分配與空氣壓縮。~Incompressible geometric displacement; pressure difference, path splitting and compressibility are not solved.',
'以列車位置同步觸發各風井和月台風速量測，檢查流量方向與時間差，避免把瞬時尖峰當成持續換氣能力。~Trigger shaft and platform air-velocity measurements from train position, inspect direction and delay, and avoid treating a brief peak as continuous ventilation capacity.',
'風井受阻時氣流可能轉移到月台，造成局部強風；單一風速計又可能量到回流區而低估主流。~A blocked shaft can redirect flow toward the platform and create local gusts; one anemometer inside a recirculation region may underestimate the main flow.',
'列車截面乘速度就是所有風井各自收到的相同流量~Train frontal area times speed is the identical flow received by every ventilation shaft.',
'將總排量分配到兩條假想阻力路徑，畫出質量守恆圖，再說明需要哪些壓差資料才能求分流比例。~Divide the displacement among two hypothetical resistance paths, draw the mass balance, and identify the pressure measurements required to determine the split.')

add('queue','到站變異與平均等候~Arrival variability and mean waiting',
'當旅客隨機到站且不受容量限制時，平均等待與班距平方的期望值有關，長班距被更多旅客遇到。兩組平均班距相同的服務仍可能有不同等待時間，因此準點與均勻性具有獨立價值。~With random passenger arrivals and no capacity constraint, mean waiting depends on the expected squared headway. More passengers encounter longer gaps. Services with identical mean headway can therefore have different waiting times, giving regularity a value separate from the average frequency.',
{'mean':(180,'s'),'sd':(60,'s')},'(mean**2+sd**2)/(2*mean)',('wait','s'),
'獨立隨機旅客到達、穩態班距且皆可登車；不含時刻表配合到站。~Random independent passenger arrivals, stationary headways and no denied boarding; timetable-aware arrivals are excluded.',
'從連續到站紀錄計算班距平均與變異數，再用匿名旅客到站時刻重播等待，檢查是否存在容量不足或非隨機到站。~Calculate headway mean and variance from consecutive arrivals, replay waiting with anonymous passenger arrival times, and check for capacity limits or nonrandom arrivals.',
'只報平均班距會低估不規則服務的等待；旅客配合時刻表到站時又不能直接套用隨機到站公式。~Reporting only mean headway understates waiting under irregular service, while timetable-aware arrivals invalidate the random-arrival formula.',
'兩組平均班距相同就一定有相同平均等候時間~Two services with equal mean headway necessarily have equal mean passenger waiting time.',
'保持平均班距不變，把標準差減半後重算等待，並用一組確定性到站時間說明公式假設何時失效。~Hold mean headway fixed and halve its standard deviation, recalculate waiting, then use deterministic arrivals to show when the formula assumptions fail.')

add('availability','可用度與修復時間~Availability and repair time',
'在簡化更新過程中，可用度是平均故障間隔占故障間隔加修復時間的比例。這個指標不能替代安全性，因為快速恢復服務可能仍保留危險失效；備品、交通與診斷都會影響實際修復時間。~In a simplified renewal process, availability is mean time between failures divided by that time plus mean repair time. It does not replace safety: rapidly restoring service may leave a hazardous failure unresolved. Spares, travel and diagnosis all affect actual restoration time.',
{'mtbf':(1200,'h'),'mttr':(4,'h')},'mtbf/(mtbf+mttr)',('availability','1'),
'兩狀態穩態平均模型；不含計畫維修、共同原因與降級服務品質。~Two-state steady-state mean model; planned maintenance, common causes and degraded service quality are excluded.',
'將故障開始、到場、診斷、修復及恢復服務分段記錄，明確定義可用狀態，避免把降級運轉與完整服務混算。~Record failure onset, arrival, diagnosis, repair and service restoration separately, define the available state, and avoid mixing degraded operation with full service.',
'只縮短更換時間但備品仍缺貨，可用度未必改善；將延後報修時間排除也會讓數字看似漂亮卻失去代表性。~Shorter replacement time may not improve availability when spare parts remain unavailable; excluding reporting delays can also create an unrepresentative figure.',
'設備可用度高就表示所有安全風險一定很低~High equipment availability necessarily means every safety risk is low.',
'比較提高故障間隔與縮短修復時間兩種措施，用同一故障定義重算，並列出可用度之外需要追蹤的危險失效指標。~Compare increasing failure interval with reducing repair time under one failure definition, and list hazardous-failure measures that must be tracked separately from availability.')

add('rubber','膠輪滾阻與熱耗散~Rubber-tyre rolling loss',
'膠輪變形造成遲滯能量損失，可用等效滾動阻力係數乘法向力估計阻力。胎壓、溫度和路面狀態都會改變係數；承載輪與導向輪的功能不同，不能用鋼輪系統的固定係數直接替代。~Rubber deformation creates hysteretic energy loss, represented approximately by a rolling coefficient times normal force. Tyre pressure, temperature and running surface change the coefficient. Load-bearing and guidance wheels serve different functions, so a coefficient from a steel-wheel system cannot simply be substituted.',
{'coefficient':(0.012,'1'),'normal':(600000,'N'),'speed':(15,'m/s')},'coefficient*normal*speed/1000',('rolling_power','kW'),
'固定等效係數與定速；不含轉彎側滑、胎溫演化或驅動損失。~Fixed effective coefficient and constant speed; curve scrub, tyre-temperature evolution and drive losses are excluded.',
'比較相同負載下的牽引能量與胎溫，記錄胎壓、路面濕度及輪胎批次，並將導向輪磨耗獨立檢查。~Compare traction energy and tyre temperature at equal load, record pressure, surface moisture and tyre batch, and inspect guidance-wheel wear separately.',
'胎壓偏低可能增加變形和熱累積，導向偏差又會造成額外磨耗；只看馬達電流無法區分兩種原因。~Low tyre pressure can increase deformation and heat accumulation, while guidance misalignment adds wear; motor current alone cannot distinguish the causes.',
'膠輪與鋼輪的滾動阻力係數可以不經試驗直接互換~Rubber-tyre and steel-wheel rolling coefficients can be interchanged without testing.',
'改變胎壓造成的假想滾阻係數，重算同速耗能，設計同時記錄輪溫與側向磨耗的對照試驗。~Change the hypothetical rolling coefficient associated with tyre pressure, recalculate energy at equal speed, and design a comparison recording tyre temperature and lateral wear.')

add('baggage','行李旅客與等效交換需求~Luggage and effective passenger exchange',
'機場旅客攜帶行李時占用更大空間且上下車較慢，可先以等效旅客係數整理交換需求。係數應由觀察校準而非固定刻板印象；門寬、坡差與同行群體又會改變通過時間。~Passengers with luggage often occupy more space and take longer to board, so an equivalent-passenger factor can organise exchange demand. It must be calibrated from observation rather than stereotypes. Door width, level differences and travelling groups also alter passage time.',
{'plain':(100,'persons'),'luggage':(60,'persons'),'factor':(1.6,'equivalent/person')},'plain+luggage*factor',('equivalent_demand','equivalent persons'),
'線性加權的教學需求指標；不是正式容量標準或特定旅客評分。~Linear teaching demand index; not a formal capacity standard or a rating of individual passengers.',
'匿名觀察不同門口的通過時間與行李尺寸群組，保留空間配置差異，避免把環境障礙全歸因於旅客行為。~Observe door passage times and luggage-size groups anonymously, retain layout differences, and avoid attributing environmental barriers entirely to passenger behaviour.',
'行李集中在少數車門會使全列停站時間由局部控制；同樣人數但不同分布可能造成完全不同的交換效率。~Luggage clustering at a few doors can control whole-train dwell; the same passenger total with a different distribution can have very different exchange efficiency.',
'機場列車只要乘客總數相同就一定具有相同停站需求~Airport trains with equal passenger totals necessarily have equal dwell demand.',
'比較集中行李區與分散行李區的等效需求，提出無障礙與一般旅客都可使用的導引方式，並列出需要實測校準的係數。~Compare concentrated and distributed luggage areas, propose guidance usable by passengers with different access needs, and list coefficients requiring measurement-based calibration.')

add('mixed','快慢車追及與待避~Fast-slow train catch-up',
'快車在同一路段追上慢車的時間取決於初始間距除相對速度。這個簡單關係能辨認待避需求，但實際時刻表還需加入停站、進路鎖閉與加減速；追及點不是允許兩車接近的安全距離。~Catch-up time on a shared section is initial separation divided by relative speed. This relation identifies the need for overtaking opportunities, but real timetables also include stops, route locking and acceleration. The meeting point is not a permitted safe separation between trains.',
{'gap':(12000,'m'),'fast':(60,'m/s'),'slow':(40,'m/s')},'gap/(fast-slow)',('catch_time','s'),
'同向恆速且快車較快；不含號誌保護和停站。~Same-direction constant speeds with a faster following train; signalling protection and stops are excluded.',
'用列車運行圖標出快慢車路徑與停站，把相交位置對照可待避地點，並核對道岔與站台實際占用時間。~Plot fast and slow trajectories including stops, compare intersections with overtaking locations, and verify actual point and platform occupation times.',
'只看區間平均速度可能把追及位置判錯；慢車停站時間波動會改變待避窗口並將延誤傳給快車。~Using section-average speed can misplace the catch-up location; variable stopping time shifts overtaking windows and passes delay to the fast train.',
'快慢車平均速度不同也不會影響同線時刻表容量~Different fast and slow train speeds do not affect shared-line timetable capacity.',
'增加慢車停站與快車出發延後各一個情境，畫出時空圖，討論待避線能解決的衝突與仍存在的交叉進路限制。~Add a slow-train stop and a delayed fast departure as separate cases, draw time-distance diagrams, and distinguish conflicts solved by a loop from remaining crossing-route restrictions.')

add('neutral','無電區惰行與速度損失~Coasting through an unpowered section',
'列車通過無電區時需依靠動能克服阻力，簡化恆阻力模型把阻力做功從初始動能扣除。區段長度、初速與坡度決定剩餘速度，供電切換邏輯和防誤合閘仍需獨立驗證。~A train coasting through an unpowered section uses kinetic energy to overcome resistance. A constant-resistance model subtracts work from initial kinetic energy. Length, entry speed and gradient determine remaining speed, while switching logic and prevention of inappropriate re-energisation require separate verification.',
{'v':(50,'m/s'),'force':(15000,'N'),'length':(500,'m'),'mass':(250000,'kg')},'(v*v-2*force*length/mass)**0.5',('exit_speed','m/s'),
'水平路線且恆阻力，根號內必須非負；不含低速停車及切換暫態。~Level track and constant resistance with a nonnegative radicand; stopping within the section and switching transients are excluded.',
'同步記錄受電電壓、主斷路器狀態和列車速度，確認無電區邊界與里程一致，再核對惰行能量差。~Synchronise line voltage, main-breaker status and speed, align electrical boundaries with distance coordinates, and check the coasting energy difference.',
'邊界定位誤差可能使主斷路器切換時機錯誤；把坡度阻力遺漏會低估上坡無電區的速度下降。~Boundary-position error can mistime breaker switching; omitting gradient resistance understates speed loss in an uphill unpowered section.',
'無電區長度改變不會影響列車離開時的速度~Changing the length of an unpowered section cannot change exit speed.',
'在相同初速下增加區段長度，檢查能量是否足夠通過，再列出電氣切換與機械惰行模型各自需要的驗證資料。~Increase section length at fixed entry speed, test whether energy remains sufficient, and list separate evidence for electrical switching and mechanical coasting models.')

add('sampling','空間波長與量測取樣~Spatial wavelength and sampling',
'移動量測車把軌道空間波長轉成時間頻率，速度除波長得到激振頻率。要避免混疊，取樣率需高於訊號頻寬兩倍並搭配抗混疊濾波；提高取樣率本身不能修正輪滑造成的里程誤差。~A moving inspection vehicle converts track wavelength into temporal frequency through speed divided by wavelength. Avoiding aliasing requires a sampling rate above twice the signal bandwidth and an antialias filter. A higher sample rate alone cannot correct distance errors caused by wheel slip.',
{'speed':(50,'m/s'),'wavelength':(2,'m')},'2*speed/wavelength',('nyquist_lower_bound','samples/s'),
'單一最短波長的理想Nyquist下界；實務需留濾波與取樣裕度。~Ideal Nyquist lower bound for one shortest wavelength; practical filters and sampling need additional margin.',
'用已知波長的校驗訊號檢查量測鏈，對照獨立里程基準，並在不同車速下比較空間頻譜是否一致。~Check the chain with a known-wavelength reference, compare an independent distance datum, and inspect whether spatial spectra agree at different vehicle speeds.',
'不足取樣會把短波缺陷偽裝成長波，里程跳動又會改變重採樣位置；兩者需分別診斷。~Undersampling disguises short-wave defects as long waves, while distance jumps alter resampling positions; the two mechanisms require separate diagnosis.',
'量測車速度提高時仍可永遠沿用原本取樣率~The original sampling rate remains sufficient at every increased inspection speed.',
'把速度提高一成並把最短波長減半，計算取樣率需求，繪出混疊示意後提出抗混疊濾波的頻寬要求。~Increase speed by ten percent and halve the shortest wavelength, calculate sampling needs, illustrate aliasing, and specify the required antialias-filter bandwidth.')

add('bearing','軸承故障頻率與轉速~Bearing signatures and rotational speed',
'滾動軸承幾何決定故障衝擊相對轉速的頻率倍率，教學以已假設倍率乘轉速辨認階次。車速變動時固定頻率譜會展寬，階次追蹤可保留與轉速同步的訊號，但仍需排除輪軌激振。~Bearing geometry determines fault-impact orders relative to rotational speed. Multiplying an assumed order by rotation frequency illustrates diagnosis. Variable speed smears fixed-frequency spectra; order tracking retains speed-synchronous signatures but must still distinguish wheel-rail excitation from bearing faults.',
{'rpm':(600,'rev/min'),'order':(4.5,'cycles/rev')},'rpm/60*order',('signature','Hz'),
'已知故障階次且轉速穩定；不代表某型軸承真實幾何。~Assumed fault order and steady rotation; not the geometry of a particular bearing type.',
'同步量測振動與轉速脈波，對比負載改變後的階次峰，並用溫度與潤滑紀錄作獨立佐證。~Synchronise vibration and tachometer pulses, compare order peaks under changing load, and use temperature and lubrication records as independent corroboration.',
'輪扁或軌道接縫也能產生週期衝擊，單一頻譜峰不能唯一定位軸承損傷；速度估計錯誤則會使階次偏移。~Wheel flats and track joints also create periodic impacts, so one spectral peak cannot uniquely identify bearing damage; wrong speed estimates shift calculated orders.',
'頻譜中出現一個週期峰就一定證明軸承已損壞~One periodic spectral peak necessarily proves that a bearing is damaged.',
'用兩種轉速檢查同一峰是否維持固定階次，再加入輪軌接縫頻率，比較哪些特徵能區分故障來源。~Use two speeds to test whether a peak maintains constant order, add a rail-joint excitation frequency, and compare features that distinguish the sources.')

add('fleet','周轉時間與車隊需求~Round-trip time and fleet size',
'維持固定班距所需列車數取決於完整周轉時間除班距並向上取整，周轉包含兩端折返與停站。備用車和維修車需另列；只用單程行車時間會把車隊需求低估接近一半。~Fleet requirement for fixed headway is round-trip cycle time divided by headway, rounded upward. The cycle includes terminal turnbacks and stops. Spares and maintenance vehicles are additional; using only one-way running time can underestimate the requirement by nearly half.',
{'cycle':(5400,'s'),'headway':(180,'s')},'ceil(cycle/headway)',('fleet','trains'),
'固定周轉與班距、無延誤；不含備用率和維修排程。~Fixed cycle and headway without delays; reserve ratio and maintenance scheduling are excluded.',
'逐列串接實際到發時間檢查周轉，將折返與等待分開，並對尖峰班距需求與可出車數建立同一時點的清單。~Join actual arrival and departure logs by train, separate turnback from waiting, and compare peak headway requirements with trains available at the same time.',
'列車數足夠仍可能因機廠出入路徑受限而無法準時上線；忽略維修週期則會讓紙上車隊數不可持續。~Sufficient fleet count may still fail when depot access restricts insertion; ignoring maintenance cycles makes the paper fleet unsustainable.',
'車隊需求可以只用單程時間除以班距決定~Fleet requirement can be determined using one-way time divided by headway alone.',
'增加一端折返時間後重算車隊，檢查向上取整造成的跳變，再提出維修備用與臨時故障應如何另列。~Increase one terminal turnback time, recalculate fleet and examine rounding jumps, then explain separate allowances for maintenance reserve and unexpected failures.')

add('backup','備援電池與可維持時間~Backup battery endurance',
'備援電池可供負載使用的能量由額定容量、允許放電深度和轉換效率相乘，除負載功率得到理想時間。低溫、老化及啟動電流會縮短可用時間；額定安時也不能直接當成瓦時。~Usable backup energy combines rated energy, permitted discharge fraction and conversion efficiency. Dividing by load gives ideal endurance. Cold temperature, ageing and start-up current can shorten it; an ampere-hour rating must not be mistaken directly for watt-hours.',
{'energy':(20,'kWh'),'usable':(0.8,'1'),'eta':(0.9,'1'),'load':(4,'kW')},'energy*usable*eta/load',('endurance','h'),
'固定負載與額定能量；不含電池倍率效應、溫度與容量衰退。~Constant load and nominal energy; rate effects, temperature and capacity degradation are excluded.',
'定期以已知負載做受控放電，量端電壓、電流及溫度，核對控制器切離點與真正可用能量。~Perform controlled discharges into a known load, measure voltage, current and temperature, and compare controller cutoff with actually delivered energy.',
'老化電池可能有正常開路電壓卻無法承受負載；共用充電器故障也可能同時耗盡兩組名義備援。~An aged battery may show normal open-circuit voltage yet fail under load; a shared charger fault can also deplete two nominally redundant banks.',
'備援電池開路電壓正常就能保證額定支援時間~Normal open-circuit battery voltage guarantees the rated backup duration.',
'將負載增加一成並把可用容量降為老化假設值，重新計算時間，提出量測端電壓以外必須保留的證據。~Increase load and reduce usable capacity for an ageing case, recalculate endurance, and identify evidence required beyond terminal-voltage readings.')

add('redundancy','並聯備援與共同原因~Parallel redundancy and common cause',
'兩個獨立元件只要有一個成功即可服務時，系統失效機率等於兩者失效機率相乘。但共用電源、軟體或環境會破壞獨立假設，備援數量增加不能自動證明整體風險按平方下降。~When either of two independent components can serve the demand, system failure probability is the product of their failure probabilities. Shared power, software or environment breaks independence. More redundant components therefore do not automatically prove a squared reduction in overall risk.',
{'q1':(0.02,'1'),'q2':(0.03,'1')},'q1*q2',('joint_failure','1'),
'同一時間窗內獨立失效且切換完美；不含共同原因與切換失敗。~Independent failures in one time window with perfect switching; common causes and switch failure are excluded.',
'畫出供電、網路、冷卻和軟體版本的依賴圖，逐一驗證切換功能；以故障注入確認另一通道可承接完整需求。~Map dependencies in power, networking, cooling and software versions, verify switching, and use fault injection to confirm the surviving channel can carry the full demand.',
'兩台設備接在同一配電盤可能被一次故障同時切斷；過載備援也可能在接手後立即失效。~Two devices on one distribution board can be lost together, and an undersized backup can fail immediately after taking over.',
'只要設備數量變成兩台失效機率就必定平方降低~Doubling equipment count necessarily squares down the failure probability.',
'在獨立模型加入一個共同原因機率，對比結果，列出可用物理隔離與不同依賴路徑降低的風險。~Add one common-cause probability to the independent model, compare the result, and identify risks reduced by physical separation and distinct dependencies.')

add('pressure','高海拔壓力與氣體密度~Altitude pressure and air density',
'理想氣體密度由絕對壓力除氣體常數與絕對溫度決定，高海拔低壓會減少同體積空氣所攜帶的質量。這同時影響散熱和氣動力，但車廂供氧與醫療需求不能由密度公式單獨決定。~Ideal-gas density is absolute pressure divided by gas constant and absolute temperature. Lower pressure at altitude reduces the mass carried in a fixed air volume, affecting cooling and aerodynamic loads. Cabin oxygen provision and medical needs cannot be determined by density alone.',
{'pressure':(60000,'Pa'),'Rair':(287,'J/(kg*K)'),'temperature':(280,'K')},'pressure/(Rair*temperature)',('density','kg/m^3'),
'乾空氣理想氣體、均勻壓溫；不計濕度與生理反應。~Dry ideal air at uniform pressure and temperature; humidity and physiological response are excluded.',
'使用絕對壓力計與校正溫度計，核對感測器是否誤報表壓，並用已知風量估算質量流率檢查冷卻設計假設。~Use absolute-pressure and calibrated temperature sensors, check that gauge pressure is not mistaken for absolute pressure, and compare mass flow inferred from measured volume flow.',
'把攝氏溫度直接代入氣體公式會產生巨大誤差；低密度時沿用海平面風量又可能不足以移除同一熱負載。~Using Celsius directly in the gas equation creates a large error; at low density, sea-level volume flow may not remove the same heat load.',
'空氣體積流率相同就表示任何海拔的散熱質量流率相同~Equal volumetric airflow guarantees equal cooling mass flow at every altitude.',
'比較兩種絕對壓力下的密度與同風量質量流率，標註溫標換算，再說明哪些車廂環境議題需要其他專業模型。~Compare density and mass flow at two absolute pressures, show temperature-scale conversion, and identify cabin-environment questions requiring additional specialised models.')

add('sand','砂塵沉積與清理週期~Dust deposition and cleaning interval',
'沉積質量可由有效集塵面積、入射質量通量與時間估算，防砂構造改變局部風場也會改變沉積位置。清理週期應依累積量與功能影響決定，而不是把全年平均濃度當成每次沙塵事件。~Deposited mass can be estimated from effective collection area, incident mass flux and time. Wind barriers alter local airflow and deposition location. Cleaning intervals should follow accumulation and functional impact rather than treating annual mean concentration as a description of every dust event.',
{'flux':(0.00008,'kg/(m^2*s)'),'area':(12,'m^2'),'duration':(3600,'s')},'flux*area*duration',('deposit','kg'),
'固定沉積通量與面積；不含再懸浮、顆粒分徑和風向變化。~Fixed deposition flux and area; resuspension, particle-size distribution and changing wind direction are excluded.',
'在不同高度和背風位置配置集塵盤，對照風速風向與設備故障紀錄，量出事件累積量而非只取單點濃度。~Place deposition trays at different heights and sheltered locations, correlate with wind and equipment records, and measure event accumulation rather than one concentration reading.',
'防風牆可能把沉積集中到設備附近，清理不到的角落會比平均面積更快受堵；濕砂還可能附著於絕緣表面。~A wind barrier may concentrate deposits near equipment, inaccessible corners can clog faster than the mean, and wet dust can adhere to insulating surfaces.',
'防風牆一旦設置就必定讓所有位置的砂塵沉積同時下降~Installing a wind barrier necessarily reduces dust deposition at every location.',
'比較同總入砂量的均勻與集中沉積，設計清理頻率表，說明為何要保留風向與設備位置而不能只報總重量。~Compare uniform and concentrated deposition at equal total input, design a cleaning-interval table, and explain why wind direction and equipment location matter beyond total mass.')

add('survey','控制網與獨立量測殘差~Survey control and independent residuals',
'兩套獨立量測可用座標差的平方和開根號描述平面殘差，但這只是對照量而不是絕對準確度。共同基點錯誤會同時影響兩套結果，控制網需要閉合檢查及外部基準才能發現系統偏差。~The root-sum-square of coordinate differences describes planar residual between independent measurements, not absolute accuracy. A shared control-point error affects both results. Network closure and an external datum are needed to reveal systematic bias that agreement alone can conceal.',
{'dx':(0.003,'m'),'dy':(0.004,'m')},'(dx*dx+dy*dy)**0.5*1000',('residual','mm'),
'平面兩分量殘差；不含座標轉換協方差和垂直誤差。~Planar two-component residual; transformation covariance and vertical error are excluded.',
'用獨立控制點做閉合觀測，記錄儀器溫度、氣壓改正與視線長度，將重複性和系統偏差分開報告。~Close observations on independent controls, record instrument temperature, pressure correction and sight length, and report repeatability separately from systematic bias.',
'同一錯誤基點會讓兩台儀器一致偏移；長視線折光與站體熱變形也可能被誤認為施工偏差。~One wrong datum can shift both instruments consistently; long-sight refraction and thermal movement can also be mistaken for construction error.',
'兩台儀器量得同樣座標就證明座標絕對正確~Matching coordinates from two instruments prove absolute coordinate accuracy.',
'加入一個共同平移偏差，檢查兩儀器殘差與外部基準差異，提出能辨識系統誤差的控制網配置。~Add a shared translation bias, compare inter-instrument residual with error to an external datum, and propose a control network that can reveal systematic error.')

add('grout','注漿量與空隙體積~Grout volume and void account',
'填充空隙所需漿量先由幾何空隙體積估算，再考慮損失與材料體積變化。注入量大不代表填充完整，因為漿液可能沿裂縫流失；壓力、流量與返漿紀錄必須互相對照。~Required grout begins with geometric void volume and allowances for loss and volume change. A large injected volume does not prove complete filling because grout can escape through cracks. Pressure, flow and returns must be interpreted together to distinguish filling from loss.',
{'length':(20,'m'),'width':(2.5,'m'),'gap':(0.04,'m'),'allowance':(1.15,'1')},'length*width*gap*allowance',('grout_volume','m^3'),
'均勻幾何間隙與假設損失係數；不指定注漿壓力或現地工法。~Uniform geometric gap and assumed loss allowance; no injection pressure or field procedure is specified.',
'核對批次體積、流量計及返漿量，將注入壓力與時間曲線同步，完成後以獨立檢測確認空隙分布。~Reconcile batch volume, flow meter and returns, synchronise injection pressure over time, and verify void distribution afterward using an independent inspection method.',
'漏失會讓注入體積增加而空隙仍未填滿，局部封堵又會使壓力快速上升；僅憑達到預算漿量不能驗收。~Loss can increase injected volume while leaving a void unfilled, and local blockage can raise pressure rapidly; reaching the budgeted volume is not acceptance evidence.',
'注入漿量超過幾何空隙體積就能證明沒有殘留空洞~Injecting more than the geometric void volume proves that no void remains.',
'比較正常填充與沿裂縫漏失兩組流量壓力紀錄，做體積收支並提出能辨識兩者的獨立檢測。~Compare flow-pressure records for normal filling and crack leakage, build a volume balance, and propose an independent inspection that distinguishes the two.')

add('transfer','轉乘步行與銜接餘裕~Transfer walking and connection margin',
'轉乘能否銜接取決於實際可用時間扣除下車、步行、垂直動線與候車需求。最短路徑不一定最快，因為樓梯、閘門與人流交會造成等待；無障礙路徑需要獨立列出而非套用同一速度。~A connection depends on available time after alighting, walking, vertical circulation and boarding needs. The shortest route is not always fastest because stairs, gates and crossing streams cause waiting. Accessible routes need their own timing rather than an assumed common walking speed.',
{'available':(300,'s'),'distance':(180,'m'),'speed':(1.0,'m/s'),'vertical':(45,'s')},'available-distance/speed-vertical',('margin','s'),
'固定步速與額外時間；不包含動態排隊或旅客個別差異分布。~Fixed walking speed and additional time; dynamic queues and individual variability distributions are excluded.',
'以匿名實測旅程時間分位數比較路徑，記錄電梯等待及閘門排隊，檢查轉乘圖的距離是否包含所有垂直動線。~Compare route-time quantiles from anonymous observations, record lift and gate waits, and check that route distances include every vertical circulation segment.',
'只用最快步行者校準會低估多數人的轉乘時間；電梯停機又可能使唯一無障礙路徑失去連續性。~Calibrating to the fastest walkers understates many passengers’ transfer time; a failed lift can also break the only continuous accessible route.',
'轉乘路線距離最短就一定適合所有旅客最快銜接~The shortest transfer route necessarily gives every passenger the fastest connection.',
'比較一般與無障礙兩條路徑的餘裕，加入一台電梯停機情境，說明時刻表調整與空間導引分別能改善哪一段。~Compare connection margins for ordinary and accessible routes, add one unavailable lift, and distinguish improvements from timetable changes versus spatial guidance.')

add('congestion','匯入流量與瓶頸餘裕~Merging flow and bottleneck margin',
'兩支線人流或列車流匯入同一通道時，總需求需與下游服務率比較。差值為正只代表平均有餘裕，突發到達仍會形成隊列；服務率降低時積壓以需求和服務的差累積。~When two passenger or train streams merge, their combined demand must be compared with downstream service. Positive average margin does not prevent queues after bursts. If service falls below demand, backlog accumulates at the difference between their rates.',
{'capacity':(100,'persons/min'),'flow1':(45,'persons/min'),'flow2':(35,'persons/min')},'capacity-flow1-flow2',('margin','persons/min'),
'定常平均流量；不包含隨機到達、優先權和實體隊列長度。~Steady mean flows; random arrivals, priority rules and physical queue length are excluded.',
'同時記錄兩個入口和下游出口，將資料用相同時間窗聚合，檢查需求尖峰是否被過大的平均窗隱藏。~Record both inlets and the downstream outlet synchronously, aggregate with equal windows, and check whether long averaging periods hide demand peaks.',
'一支線延誤後集中釋放會造成瞬時過載，即使全天平均需求較小；下游出口短暫阻塞則可能向上游回堵。~A delayed branch can release a concentrated surge despite modest daily demand; a brief downstream blockage can spill a queue back upstream.',
'平均總需求低於容量就保證任何時間都不會排隊~Mean demand below capacity guarantees that no queue forms at any time.',
'保持平均需求相同但把一支線改成脈衝到達，逐分鐘更新隊列，提出分流或節流措施並檢查其上游影響。~Keep mean demand fixed while making one branch arrive in pulses, update the queue minute by minute, and assess upstream consequences of rerouting or metering.')

add('clearance','限界疊加與幾何餘裕~Clearance stack and geometric margin',
'車輛與固定設備之間的餘裕需扣除車體擺動、施工偏差與量測不確定度，最壞界限相加和統計平方和不同。曲線、軌道超高與懸吊動作會改變掃掠包絡，靜止車體尺寸不能代表動態限界。~Clearance margin subtracts body motion, construction offset and measurement uncertainty from the available gap. Worst-case stacking differs from statistical root-sum-square. Curves, cant and suspension motion change the swept envelope, so static body dimensions do not represent dynamic clearance.',
{'gap':(160,'mm'),'sway':(45,'mm'),'build':(15,'mm'),'survey':(5,'mm')},'gap-sway-build-survey',('margin','mm'),
'保守同向疊加的假設值；不含完整車體掃掠或規範限界。~Assumed conservative same-direction stack; no complete swept-body or regulatory envelope is calculated.',
'用軌道基準對照點雲與設備位置，分別記錄空車、滿載及曲線條件，核對量測遮蔽處是否有未掃描障礙。~Compare point clouds and equipment against track datums, record empty, loaded and curved-track conditions, and check for obstacles hidden from the survey.',
'把互不相同的座標系直接相減會產生假餘裕；只掃描一側也可能漏掉曲線內側的車體內偏。~Subtracting coordinates from mismatched frames creates false margin, while a one-sided scan can miss inward body throw on a curve.',
'靜止車體與設備不接觸就能保證所有運動狀態都不接觸~No contact for a stationary vehicle guarantees clearance in every moving condition.',
'對直線與曲線各做一張限界預算，分開最大界限與隨機誤差，指出哪些項目需以實車量測或掃掠分析確認。~Prepare straight and curved clearance budgets, separate maximum bounds from random errors, and identify items requiring vehicle measurements or swept-envelope analysis.')

add('construction','施工窗口與可完成工作量~Possession window and achievable work',
'夜間施工窗口需先扣除封鎖確認、隔離、運入及恢復測試時間，剩餘時間才可進行實際工作。提高施工速度不一定提高總產出，若撤場與驗收成為關鍵路徑，必須先調整作業協調。~A night possession must allow for protection, isolation, access and restoration testing before productive work begins. Higher work rate does not always increase output if clearance and acceptance dominate the critical path. Coordination of dependencies may matter more than nominal production speed.',
{'window':(240,'min'),'setup':(45,'min'),'restore':(55,'min'),'rate':(4,'m/min')},'(window-setup-restore)*rate',('work_length','m'),
'固定速度與確定性窗口；不含返工、設備故障和分段驗收。~Fixed production rate and deterministic window; rework, equipment failure and phased acceptance are excluded.',
'按事件紀錄封鎖、確認隔離、進場、工作結束與試驗完成時間，用實際有效工作時間計算產率。~Log possession, isolation confirmation, access, work completion and final testing, then calculate productivity from actual effective work time.',
'壓縮恢復測試時間可能掩蓋未完成檢查；低估撤場時間會造成延誤，不能把安全確認當成可任意削減的冗餘。~Compressing restoration tests can hide incomplete checks, while underestimated clearance causes delay; safety confirmation cannot be treated as arbitrary slack.',
'施工窗口全長都可以直接乘以施工速度當成可完成量~The entire possession duration can be multiplied by work rate to obtain achievable production.',
'增加前置作業時間並加入一次返工，重畫關鍵路徑，區分可平行任務與必須完成後才可開放的檢查。~Increase setup time and add one rework event, redraw the critical path, and distinguish parallel tasks from checks that must finish before reopening.')
