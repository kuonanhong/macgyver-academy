"""Project-specific course framing. Dates refer to public project/operator records."""
P={}
def p(n,focus,scenario,events,url,publisher,place,country,coords,keys,contexts,second=None):
    P[f'b{n}']=dict(focus=focus,scenario=scenario,events=events,url=url,publisher=publisher,place=place,country=country,coords=coords,keys=keys.split(),contexts=contexts.split('\n'),second=second)

p(301,'高速鐵路車軌橋與地震系統介面~High speed vehicle track bridge and seismic interfaces',
'以臺灣南北高速運輸走廊為背景，設計一段包含高架橋、曲線與隧道的教學路線。比較正常行車、地震警報和異常受電三種工況，要求學徒追蹤每項設計假設如何傳到停車位置與班表恢復。~Use Taiwan’s north-south high-speed corridor as the setting for an invented alignment with a viaduct, curve and tunnel. Compare routine running, an earthquake warning and disrupted current collection. Trace each design assumption through to stopping position and timetable recovery rather than treating vehicle, structure and control calculations as isolated answers.',
[('2007','臺灣高鐵開始提供營運服務~Taiwan High Speed Rail began passenger service'),('2025','IEC 發布新版鐵道 RAMS 第一部分通用程序~IEC published the revised railway RAMS Part 1 generic process')],
'https://tdiscovery.thsrc.com.tw/exhibition_en.html','Taiwan High Speed Rail', '高鐵臺中站周邊~THSR Taichung station area','臺灣~Taiwan',(24.112,120.616),
'brake cant thermal seismic bridge pantograph regen tunnelwave settlement availability',
'''把警報後的列車停車位置與橋梁邊界放在同一里程圖上。~Plot the post-alarm stopping position and bridge limits on the same chainage diagram.
比較快車通過與低速受限運轉時相同曲線的殘餘側向加速度。~Compare residual lateral acceleration on one curve during fast passage and restricted low-speed operation.
以高架曝曬段和隧道出口作為不同鋼軌溫度量測位置。~Use an exposed viaduct and a tunnel exit as contrasting rail-temperature measurement locations.
把預警提前量與列車制動時間連結，辨認近場地震的限制。~Link warning lead time to braking time and identify the limitation of a nearby earthquake.
在高架跨中區分列車載重撓度與支承位置的共同移動。~Separate load-induced midspan deflection from movement shared with the viaduct supports.
在橋隧交界檢查接觸線張力與接觸品質的變化。~Examine contact-wire tension and collection quality across the transition between bridge and tunnel.
比較同方向追蹤列車與單獨列車對回送電能的接受條件。~Compare network receptivity with a following train and with an isolated train movement.
把隧道入口壓力波與列車速度聯繫，避免以風壓取代波動分析。~Relate tunnel-entry pressure disturbance to speed without substituting steady wind pressure for wave analysis.
在橋台與路堤銜接處設計足以辨認短波變形的測點。~Place survey points at a bridge-abutment transition densely enough to resolve short deformation wavelengths.
把供電與列車可用性分開，分析停駛時間是否由同一故障主導。~Separate power-system and fleet availability to determine whether one failure dominates downtime.''')

p(302,'膠輪中運量自動運轉與高架站介面~Automated medium capacity operation and elevated station interfaces',
'以文湖線的都市中運量路網為背景，建立密站距、曲線與高架車站的縮尺營運實驗。課程從輪胎接觸和乘客舒適性延伸到進路互鎖及失去通訊後的安全狀態，對照班距縮短與折返瓶頸。~Use the Wenhu urban corridor to construct a scaled operational experiment with closely spaced stations, curves and elevated platforms. Begin with tyre contact and passenger comfort, then investigate route interlocking and the safe state after communication loss. Contrast shorter line headways with a terminal that cannot release routes quickly enough.',
[('1996','木柵線開始營運形成後續文湖線基礎~The Muzha line opened as a predecessor of the Wenhu line'),('2009','內湖線通車並與既有路段連接營運~The Neihu line opened and connected with the existing route')],
'https://english.dorts.gov.taipei/News_Content.aspx?n=F5C47899DE0D7088&s=761F1E2163C50391','Taipei Department of Rapid Transit Systems','臺北大直站周邊~Taipei Dazhi station area','臺灣~Taiwan',(25.079,121.547),
'rubber jerk dwell brakecurve interlock communication turnback voltage noise backup',
'''用試驗輪載與接觸面積比較輪胎壓力，另列導向輪的功能。~Compare tyre contact pressure from experimental wheel load and area, and distinguish the guide-wheel function.
把站立旅客的加速度斜坡與短站距加速時間一併記錄。~Record acceleration ramps for standing passengers together with acceleration time on short station spacing.
檢查小編組車門集中需求是否使某一門組決定停站尾端。~Check whether concentrated demand in a short train makes one door group govern the dwell tail.
將自動運轉的目標停車點與速度監督包絡分開表示。~Distinguish the automatic-operation target stop from the speed-supervision envelope.
對相向折返與側線進入建立互斥進路的真值表。~Construct mutually exclusive route truth tables for reversing movements and siding entry.
在無線封包延遲增加時檢查授權有效期，保留停止狀態。~Check authority expiry as wireless packet delay grows, retaining a defined stopping state.
比較一列列車換端與另一列車進入終端時的道岔占用。~Compare switch occupation during one train reversal with a following train entering the terminus.
把最遠受電列車與同區段加速列車放入簡化供電模型。~Place the most distant receiving train and another accelerating train in a simplified supply model.
在高架曲線旁區分輪胎滾動、設備與背景聲能。~Separate tyre rolling, equipment and background acoustic energy beside an elevated curve.
驗證失去正常電源後通訊與疏散照明的負載分配。~Verify load allocation to communications and evacuation lighting after normal power is lost.''')

p(303,'高密度都市幹線月台人流與行車協同~Dense urban trunk platform flow and train coordination',
'以淡水信義線的市區與郊區運輸情境為背景，設計一個連接轉乘站與終端站的排隊實驗。分別處理旅客到站、上車、關門及折返事件，並把地下車站的排水、通風和導航失效納入復原討論。~Use the Tamsui–Xinyi corridor as a setting for a queueing experiment linking an interchange and a terminus. Treat arrivals, boarding, closure and reversal as separate events. Include underground station drainage, ventilation and localisation failures in the recovery discussion so that line capacity is tested against station and infrastructure constraints.',
[('1997','淡水線開始營運成為臺北捷運早期路線~The Tamsui line opened as an early Taipei Metro route'),('2013','信義線於十一月通車延伸南北運輸走廊~The Xinyi line opened in November and extended the north-south corridor')],
'https://english.dorts.gov.taipei/News_Content.aspx?n=F5C47899DE0D7088&s=761F1E2163C50391','Taipei Department of Rapid Transit Systems','臺北中山站周邊~Taipei Zhongshan station area','臺灣~Taiwan',(25.053,121.52),
'capacity dwell doors platform turnback regen ventilation drain localize transfer',
'''讓尖峰轉乘需求與線上可用運能使用相同的時間窗比較。~Compare peak interchange demand and usable line capacity over the same time window.
把樓梯附近的車門視為獨立服務群，檢查不均勻上車。~Treat doors beside the stairs as a distinct service group and test uneven boarding.
在月台門與車門確認不同步時追蹤發車許可的邏輯。~Trace departure permission when platform-door and train-door confirmations are not simultaneous.
以轉乘列車批次到達測試等候區占用與通道淨寬。~Test waiting-area occupation and clear circulation width under batch arrivals from connecting trains.
觀察終端進站、換端和離站哪個互斥事件控制下一班。~Identify which conflicting arrival, reversal or departure event controls the following service.
比較市區短站距煞車頻率與受電列車的時間重疊。~Compare frequent braking on urban station spacing with temporal overlap of receptive trains.
在地下站內分開一般換氣估算與火災排煙的設計問題。~Separate an underground station air-change estimate from the distinct design problem of smoke control.
把入口集水範圍與抽水機啟停水位連成體積平衡。~Connect the entrance catchment and pump switching levels through a volume balance.
對連續地下區間加入里程誤差，說明校正標誌的重要性。~Introduce odometry error in a continuous underground section and examine correction references.
將垂直移動與平面步行分開，檢查轉乘時間的分布。~Separate vertical circulation from level walking and inspect the distribution of transfer times.''',second='https://ebook.dorts.gov.taipei/JRTST/ebook/no48/files/basic-html/page170.html')

p(304,'炎熱都市捷運供電熱負載與站體運轉~Hot climate metro power thermal loads and station operation',
'以高雄紅線的南北都市走廊為背景，建立炎熱午後的站車負載案例。學徒需把冷房耗電、尖峰上車與加速電流放在同一時間軸，並在強降雨與單一電源失效下檢查服務降級和人員引導。~Use Kaohsiung’s north-south Red Line as the setting for a hot-afternoon station and train load case. Place cooling demand, peak boarding and acceleration current on one timeline. Under heavy rainfall and a single supply failure, examine degraded service and passenger guidance without assuming that comfortable room temperature alone demonstrates system resilience.',
[('2008','高雄捷運紅線於三月開始營運服務~Kaohsiung MRT Red Line began service in March'),('2023','營運者回顧紅橘兩線通車十五周年~The operator reviewed fifteen years of Red and Orange line service')],
'https://www.krtc.com.tw/Information/news_more?id=1b8bdb412efe4f489271bd368efdd22d','Kaohsiung Rapid Transit Corporation','高雄美麗島站周邊~Kaohsiung Formosa Boulevard station','臺灣~Taiwan',(22.631,120.302),
'cooling capacity dwell powerloss voltage regen drain ventilation backup platform',
'''把月台與車廂顯熱負載分開，避免用總冷量代替區域舒適度。~Separate platform and carriage sensible loads instead of substituting total cooling for local comfort.
在同一尖峰小時比較編組容量與實際逐車廂載客量。~Compare nominal train capacity with actual per-car loading within one peak hour.
把空調門檻造成的停留與上車交換時間分開觀測。~Separate hesitation near conditioned entrances from the time required for passenger exchange.
分析長供電路徑的電流平方損失與午後輔助負載。~Examine current-squared loss on long supply paths together with afternoon auxiliary demand.
檢查兩列列車同時加速時最遠端的受電電壓。~Check receiving voltage at the far end when two trains accelerate together.
以一列煞車和一列加速的時間差研究再生能量接受率。~Study receptivity through the time offset between a braking and an accelerating train.
把短延時暴雨與站口集水量連結，標註泵浦失效情境。~Link a short intense storm to entrance runoff and mark the failed-pump scenario.
區分換氣帶走熱量與污染物稀釋所需的不同測點。~Distinguish measurement points for heat removal from those for contaminant dilution.
分開列車牽引與車站緊急負載，核對備援能源邊界。~Separate traction from station emergency loads when checking backup-energy boundaries.
將臨時停駛造成的累積人數分配到不同月台區域。~Distribute passengers accumulated during a temporary suspension across platform zones.''')

p(305,'機場快慢車混跑與行李轉乘介面~Airport express commuter mixing and baggage interfaces',
'以桃園機場捷運的機場、都市及沿線通勤需求為背景，建立快慢車共享走廊的時間表。旅客攜帶行李會同時影響車門交換、垂直移動與安檢服務；課程要求以事件表追蹤延誤傳播，而非只比較行車速度。~Use the Taoyuan airport corridor to build an express and commuter timetable on shared infrastructure. Baggage affects door exchange, vertical circulation and processing queues together. Track disruption propagation through event tables, including passengers arriving from flights, rather than comparing train speeds alone or assuming every passenger moves at the same rate.',
[('2017','桃園機場捷運於三月正式通車營運~Taoyuan Airport MRT opened for commercial service in March'),('2025','IEC 發布新版鐵道 RAMS 第一部分通用程序~IEC published the revised railway RAMS Part 1 generic process')],
'https://www.tymetro.com.tw/tymetro-new/en/_pages/about/video-show-247-1.html','Taoyuan Metro','桃園機場第一航廈站~Taoyuan Airport Terminal One station','臺灣~Taiwan',(25.081,121.238),
'mixed baggage dwell transfer fleet brakecurve voltage regen queue availability',
'''比較快車追上慢車的時刻與可用待避路徑。~Compare the time when an express catches a commuter train with available passing routes.
在行李服務台建立旅客到達率與單件處理時間的關係。~Relate passenger arrival rate to individual handling time at the baggage service desk.
用行李占用車門附近空間的情境檢查最慢門組。~Test the slowest door group when baggage occupies space beside the train doors.
把航廈步行、電扶梯與候車拆成可獨立量測的轉乘區段。~Split terminal walking, escalator travel and waiting into separately measurable transfer stages.
讓終端折返與單程時間共同決定最少上線車組數。~Use both terminal turnaround and one-way running time to estimate the minimum circulating fleet.
區分機場站停準目標與防護用速度監督曲線。~Separate the airport stopping target from the protective speed-supervision curve.
在共享供電區段中測試快慢車同時加速的壓降。~Test voltage drop when express and commuter trains accelerate in the same supply section.
用不同停站頻率比較理想可回收能量與網路可接受能量。~Compare ideal recoverable energy and network receptivity under different stopping patterns.
模擬航班批次到達的隊列，檢查平均到達率模型的限制。~Simulate queues after batch flight arrivals and examine the limits of a mean arrival-rate model.
把旅客服務可用性與單一設備可用性分開定義。~Define passenger-service availability separately from the availability of one item of equipment.''')

p(306,'高速成熟走廊密集班表與車輛動力~Dense mature high speed timetables and vehicle dynamics',
'以東海道新幹線的成熟高速走廊為背景，建立服務密度高且有快慢停站差異的教學班表。將空氣阻力、受電弓、制動及車輛懸吊與運能相連，檢查提高速度後是否反而減少維護或恢復裕度。~Use the mature Tokaido corridor to construct a dense high-speed timetable with different stopping patterns. Connect aerodynamic resistance, current collection, braking and suspension to delivered capacity. Investigate whether raising speed consumes maintenance or recovery margins, and require an explicit distinction between historical project facts and the invented vehicle parameters used in the exercises.',
[('1964','東海道新幹線於十月開始營運服務~The Tokaido Shinkansen began passenger service in October'),('2024','營運者年度報告回顧東海道新幹線六十年~The operator annual report reviewed sixty years of the Tokaido Shinkansen')],
'https://global.jr-central.co.jp/en/company/ir/annualreport/_pdf/annualreport2024-13.pdf','Central Japan Railway Company','東京新幹線車站周邊~Tokyo Shinkansen station area','日本~Japan',(35.681,139.767),
'drag pantograph brake suspension mixed capacity thermal fatigue bearing availability',
'''比較速度提升帶來的空氣阻力功率與節省的行車時間。~Compare aerodynamic power growth with the running time saved by a higher speed.
把接觸線波速裕度與高速受電的動態量測連結。~Connect contact-wire wave-speed margin to dynamic current-collection measurements.
檢查高速進站前的速度誤差如何放大停車位置誤差。~Examine how speed error before a high-speed approach magnifies stopping-position error.
將同一軌道波長轉成不同速度下的懸吊激振頻率。~Convert one track-irregularity wavelength into suspension excitation frequencies at different speeds.
在不停站與多停站列車之間追蹤追趕與待避時間。~Track catch-up and passing time between nonstop and multi-stop services.
對高密度班表保留逐列負載，避免只看小時平均。~Retain individual train loads in a dense timetable rather than only an hourly average.
比較曝曬軌段和維修後鎖定軌段的熱應力零點。~Compare the thermal-stress reference for exposed track and track after maintenance locking.
將不同載重循環分組，檢查少量高應力事件的影響。~Group different loading cycles and inspect the influence of a small number of high-stress events.
以軸承頻譜與轉速比對建立狀態監測的頻率基準。~Use bearing spectra and rotation speed together to establish condition-monitoring frequency references.
將列車故障修復與檢修窗口分開，檢查服務可用性。~Separate fault repair from maintenance windows when examining delivered service availability.''')

p(307,'山岳高速線隧道壓力與橋隧連續性~Mountain high speed tunnel pressure and bridge continuity',
'以山陽新幹線的跨區域高速運輸為背景，建立連續隧道、橋梁與車站的假想剖面。學徒把列車進洞壓力、受電品質與排水維修放在同一系統邊界，分析短隧道間露天段是否改變乘坐舒適與維修需求。~Use the Sanyo high-speed corridor as the setting for an invented profile containing successive tunnels, bridges and stations. Place entry pressure, current collection and drainage maintenance inside one system boundary. Investigate how a short open section between tunnels can alter pressure exposure, track behaviour and access requirements without treating a simplified pressure estimate as a tunnel certification calculation.',
[('1972','山陽新幹線新大阪至岡山區間開通~The Shin-Osaka to Okayama section of the Sanyo Shinkansen opened'),('1975','山陽新幹線延伸至博多完成當時全線~The Sanyo Shinkansen extension to Hakata completed the route')],
'https://www.kyotorailwaymuseum.jp/museum-report/sanyo_shinkansen_50th/','Kyoto Railway Museum / JR West','岡山新幹線站周邊~Okayama Shinkansen station area','日本~Japan',(34.667,133.918),
 'tunnelwave pressure piston brake cant bridge settlement drain pantograph wheelheat',
'''比較兩種進洞速度的壓力波尺度，另標洞口幾何影響。~Compare pressure-wave scales for two entry speeds and separately identify portal-geometry effects.
把外部快速壓力變化與車廂壓力舒適模型的邊界分開。~Distinguish external rapid pressure changes from the boundary of a cabin-comfort pressure model.
在隧道橫斷面中分開列車阻塞面積與剩餘通風面積。~Separate train blockage area from the remaining ventilation area in a tunnel cross-section.
把隧道內制動後的位置與避難通道的里程分開標示。~Mark the post-braking position and emergency-passage chainage separately inside a tunnel.
比較洞口附近曲線的平衡速度與低速維修列車工況。~Compare curve equilibrium speed near a portal with a slow maintenance-train condition.
檢查短橋跨的靜態撓度並指出移動列車動力仍待分析。~Check static deflection of a short bridge and identify the remaining moving-train dynamic analysis.
在路堤、橋台與隧道銜接處設計多點高程剖面。~Design multipoint elevation profiles across embankment, abutment and tunnel transitions.
將洞口雨水與隧道滲水分為兩個入流來源。~Separate portal runoff and tunnel seepage into two inflow sources.
比較露天和隧道內支承條件改變時的架線動態。~Compare contact-line dynamics when support conditions change between open track and tunnel.
在連續減速情境下區分單次熱量與尚未散去的殘熱。~Distinguish one braking event’s heat from residual heat during repeated deceleration.''')

p(308,'寒冷地區高速列車降雪側風與偵測~Cold region high speed snow crosswind and detection',
'以東北新幹線向日本北部延伸的歷史為背景，設計積雪、低溫與側風並存的教學工況。分析防雪、黏著、道床熱量與輪軌監測之間的取捨，要求每項氣候假設均對應可量測的環境量。~Use the northward development of the Tohoku Shinkansen to frame a teaching scenario combining snow, low temperature and crosswind. Examine tradeoffs among snow management, adhesion, thermal demand and wheel-rail monitoring. Every weather assumption must correspond to a measurable environmental quantity, and a successful single-condition test must be distinguished from validation across a winter operating envelope.',
[('1982','東北新幹線初期區間開始營運服務~The initial Tohoku Shinkansen sections entered passenger service'),('2011','東日本旅客鐵道導入 E5 系隼號服務~JR East introduced E5 Hayabusa passenger services')],
'https://www.jreast.co.jp/en/multi/routemaps/tohokushinkansen.html','East Japan Railway Company','仙台新幹線站周邊~Sendai Shinkansen station area','日本~Japan',(38.261,140.882),
 'snow adhesion crosswind tunnelwave seismic thermal sampling bearing brake filter',
'''把待融積雪質量與融雪能源分開量測，保留新雪補入量。~Measure snow mass and melting energy separately while recording newly deposited snow.
用濕軌與雪後工況比較可用牽引力，保留輪重分布。~Compare traction bounds on wet and post-snow track while retaining wheel-load distribution.
把側風平均值與陣風峰值分開，檢查兩種量測時間尺度。~Separate mean crosswind and gust peaks and examine their different measurement timescales.
比較寒冷環境空氣性質改變對進洞壓力尺度的影響。~Compare the influence of cold-air properties on the tunnel-entry pressure scale.
在警報訊號鏈加入低溫設備延遲，與波到達時間比較。~Add cold-equipment delay to the alarm chain and compare it with wave-arrival time.
檢查寒冬鋼軌降溫時應力方向與夏季熱壓縮的差別。~Examine the stress sign during winter cooling and contrast it with summer compression.
用列車通過雪害監測點的訊號決定所需取樣頻率。~Use passage signals at a snow-monitoring point to determine the required sampling frequency.
把低溫黏度與軸承頻率特徵分開，避免直接由振幅推論損傷。~Separate low-temperature lubrication effects from bearing frequency features instead of inferring damage from amplitude alone.
對降雪後低黏著情境重新估算制動距離的保守界限。~Re-estimate a conservative braking-distance bound for reduced adhesion after snowfall.
比較進氣濾材積雪前後壓差，檢查量測是否受風量改變干擾。~Compare intake-filter pressure drop before and after snow accumulation and control for airflow changes.''',second='https://www.jreast.co.jp/e/press/20101101/')

p(309,'山地高速路線坡度牽引與在地防災~Mountain high speed grades traction and hazard response',
'以九州新幹線分期連接的歷史為背景，建立坡道、橋梁與城市車站交替的教學路線。學徒要比較爬坡功率和下坡制動的能量流向，並在地震、短時暴雨與設備停機時安排可驗證的降級營運。~Use the staged connection of the Kyushu Shinkansen to construct a teaching route alternating gradients, bridges and urban stops. Compare energy flow during climbing and downhill braking. Define verifiable degraded operation under an earthquake warning, short intense rainfall and equipment downtime, rather than treating rated traction power as evidence that every disrupted movement remains feasible.',
[('2004','九州新幹線南側先行區間開始營運~The initial southern section of the Kyushu Shinkansen opened'),('2011','博多至新八代區間開通連接既有南段~The Hakata to Shin-Yatsushiro section opened and connected to the southern section')],
'https://www.jrkyushu.co.jp/company/info/business/project01.html','Kyushu Railway Company','熊本新幹線站周邊~Kumamoto Shinkansen station area','日本~Japan',(32.79,130.688),
'grade adhesion regen wheelheat cant seismic bridge drain voltage availability',
'''在同一坡道比較滿載與輕載的重力功率需求。~Compare gravitational power demand for loaded and lightly loaded trains on one gradient.
檢查坡道起步時動輪荷重和接觸狀態能否傳遞要求牽引力。~Check whether driven-wheel load and contact condition can transmit the requested force during a gradient start.
把下坡能量回送與電網可接受時段對齊，另列剩餘摩擦熱。~Align downhill regenerative export with receptive intervals and separately record remaining friction heat.
檢查連續下坡制動造成的累積熱負荷與冷卻間隔。~Examine cumulative heat loading and cooling intervals during repeated downhill braking.
在山地曲線比較通過速度與超高過剩的低速情境。~Compare running speed with low-speed cant excess on a mountain curve.
把震源距離和通訊延遲作為獨立變數，辨識預警限制。~Treat source distance and communication delay as separate variables when identifying warning limits.
量測橋跨與支點位移，避免把支承移動當成梁剛度改變。~Measure span and support motion to avoid mistaking support displacement for a stiffness change.
以坡面集水和站口集水不同面積建立入流量比較。~Compare inflow from a hillside catchment and a station entrance using their different areas.
在爬坡高電流時估算供電壓降並核對回路定義。~Estimate voltage drop during high-current climbing and verify the defined electrical loop.
對設備停機建立修復時間分布，分析單一平均值的限制。~Build a repair-duration distribution and examine the limits of representing downtime with one mean.''')

p(310,'首代法國高速線線形與電氣介面~Early French high speed alignment and electrical interfaces',
'以法國東南高速鐵路開創高速服務的歷史為背景，比較高速專用線和既有線銜接時的設計目標。課程將線形、牽引、分相、訊號與維護放在共同時間尺度，檢查一項速度提升是否需要多個子系統共同改變。~Use the introduction of French high-speed service on LGV Sud-Est to compare dedicated high-speed alignment with connections to conventional infrastructure. Place geometry, traction, neutral sections, signalling and maintenance on a common time axis. Investigate whether a speed increase demands coordinated changes in several subsystems rather than a single adjustment to motor output.',
[('1981','法國東南高速鐵路開始支援 TGV 營運~LGV Sud-Est began supporting TGV passenger operations'),('2023','SNCF 網路公司安全報告列示既有高速線背景~The SNCF infrastructure safety report documented the established high-speed network')],
'https://www.groupe-sncf.com/fr/groupe/patrimoine-archives/histoire-tgv','SNCF Group','里昂帕爾迪厄站周邊~Lyon Part Dieu station area','法國~France',(45.761,4.859),
 'cant grade drag pantograph neutral brakecurve thermal fatigue mixed powerloss',
'''用同一曲線比較高速專用服務與低速轉線時的橫向需求。~Compare lateral demand on one curve for dedicated high-speed running and slower connecting movements.
將坡度阻力與加速功率分開，檢查長坡頂部的速度裕度。~Separate gradient resistance from acceleration power and inspect speed margin near a long climb’s summit.
評估空氣阻力的速度三次方功率變化，保留阻力係數假設。~Evaluate cubic aerodynamic power growth while retaining the assumed drag coefficient.
把受電弓與接觸線看成互動系統，避免只提高張力求解。~Treat pantograph and contact wire as an interacting system rather than solving by tension increase alone.
在分相區設計無牽引滑行的初末速度與時間驗算。~Check entry speed, exit speed and coasting time through an unpowered neutral section.
對高速線轉入低速區的目標速度建立監督距離。~Construct supervision distance for a transition from high-speed running to a lower target speed.
比較線形改建前後鎖定軌溫與拘束條件的紀錄要求。~Compare documentation of stress-free temperature and restraint before and after alignment work.
將多年通過列車造成的循環分成應力幅級距。~Group repeated train passages into stress-range bins for cumulative-damage discussion.
在既有線接續處檢查不同停站模式的追趕關係。~Examine catch-up relationships where different stopping patterns join conventional infrastructure.
把高峰電流與線路損失連結，檢查單一饋電路徑的限制。~Link peak current to line losses and inspect the limits of a single feeding path.''',second='https://www.sncf-reseau.com/medias-publics/2024-07/rapport_securite_sncf_reseau_2023.pdf')

p(311,'跨區高速線分期銜接與控制互通~Phased high speed connections and control interoperability',
'以法國東歐高速鐵路兩階段建設為背景，建立新舊路段銜接、模式轉換和供電邊界的教學案例。學徒必須以訊號有效期、定位誤差及速度曲線共同驗證列車如何通過介面，並區分通訊可用與安全授權有效。~Use the two construction phases of LGV Est europeenne to frame a teaching case involving old-new route connections, mode transitions and supply boundaries. Verify passage through interfaces using authority validity, position error and speed curves together. Distinguish available communication from a valid movement authority, and require explicit evidence for each transition condition in the operational sequence.',
[('2007','法國東歐高速鐵路第一期開始營運~The first phase of LGV Est europeenne entered service'),('2016','法國東歐高速鐵路第二期開始營運~The second phase of LGV Est europeenne entered service')],
'https://www.lisea.fr/wp-content/uploads/2020/04/Bilan-LOTI-intermediaire-dec-janv-19.pdf','LISEA','史特拉斯堡車站周邊~Strasbourg railway station area','法國~France',(48.585,7.735),
'communication localize brakecurve interlock neutral pantograph crosswind drag sampling redundancy',
'''在模式轉換前後分別檢查封包年齡與授權到期時刻。~Check packet age and authority expiry separately before and after a mode transition.
將定位的不確定區間帶入路段邊界，檢查前端位置定義。~Carry position uncertainty into the section boundary and verify the train-front reference.
連結目標速度限制和定位誤差，檢查保護距離是否仍成立。~Connect target-speed restrictions and position error when checking protective distance.
為新舊線交會設計進路互斥邏輯與故障狀態。~Design route exclusion logic and fault states for the junction between new and old lines.
在供電邊界比較不同入口速度下的滑行通過時間。~Compare coasting passage time across a supply boundary for different entry speeds.
檢查高速段架線波速與支承變化對受電的限制。~Inspect contact-wire wave speed and support changes as limits on high-speed collection.
將開闊地段側風方向分解為列車橫向作用。~Resolve open-country wind direction into the component acting across the train.
比較高速與降速工況的氣動功率，說明降速的能源效果。~Compare aerodynamic power in fast and restricted operation to explain the energy effect of reduced speed.
以模式切換事件時間寬度檢查記錄器的取樣需求。~Use mode-transition event duration to check recorder sampling requirements.
辨認通訊與電源共因，避免把兩個設備當作完全獨立。~Identify shared communication and power causes instead of assuming two devices are independent.''')

p(312,'跨海高速接線都市隧道與國際轉乘~International high speed links urban tunnels and interchange',
'以英國一號高速鐵路分期通達倫敦的背景，建立國際列車與城市終端銜接的教學系統。案例把隧道壓力、旅客服務排隊、曲線噪音和道岔占用一起考慮，要求區分列車通過能力與邊境或航廈式服務的處理能力。~Use the phased arrival of High Speed 1 into London to construct a teaching system linking international trains to an urban terminal. Consider tunnel pressure, passenger-processing queues, curve noise and switch occupation together. Distinguish railway throughput from the capacity of border-style passenger processing, and trace how a delayed batch of passengers changes boarding and departure readiness.',
[('2003','英國一號高速鐵路第一階段路段開通~The first phase of High Speed 1 opened'),('2007','英國一號高速鐵路第二階段通達倫敦終端~The second phase of High Speed 1 opened to its London terminal')],
'https://stpancras-highspeed.com/news/opportunities-at-hs1/','St Pancras Highspeed','倫敦聖潘克拉斯站周邊~London St Pancras station area','英國~United Kingdom',(51.532,-0.126),
 'tunnelwave piston noise queue baggage platform turnback interlock brake availability',
'''比較都市隧道入口與開闊入口的幾何邊界，保留壓力模型範圍。~Compare urban and open portal boundary geometry while retaining the limits of the pressure model.
把列車排開體積與有效通風截面連結，檢查短時空氣流量。~Connect displaced train volume to effective ventilation area and inspect transient airflow.
將曲線、牽引設備與背景噪音以聲能相加而非分貝相加。~Combine curve, traction-equipment and background noise by acoustic energy rather than by adding decibels.
用發車前集中報到的需求檢查單一服務櫃台的利用率。~Check single-counter utilisation under concentrated predeparture processing demand.
比較大件行李比例增加後的單件處理時間與通道阻塞。~Compare handling time and aisle obstruction as the share of large baggage rises.
在終端候車區畫出排隊、移動與保留淨空的不同區域。~Separate queueing, movement and reserved clear zones in the terminal waiting area.
把終端進路清空與旅客下車完成分開，找出串聯瓶頸。~Separate route clearance from completion of alighting to identify serial bottlenecks.
檢查進出終端同時請求進路時的互鎖拒絕條件。~Check interlocking refusal conditions when arrivals and departures request routes simultaneously.
將高速降速段與終端低速停止分成不同制動工況。~Separate high-speed deceleration from the final low-speed terminal stop.
把基礎設施可用與旅客處理服務可用分別列出。~Report infrastructure availability separately from availability of passenger-processing services.''',second='https://www.bechtel.com/projects/high-speed-1/')

p(313,'炎熱地區高速線軌溫供電與更新~Hot region high speed rail temperature power and renewal',
'以馬德里至塞維亞高速鐵路的營運及更新背景，建立夏季高溫與設備改造並行的案例。學徒要分開鋼軌溫度、車廂熱負載和牽引電流，檢查更換控制或供電設備時舊系統與新系統能否用可驗證介面銜接。~Use the operation and renewal of the Madrid–Seville line to construct a case combining summer heat with equipment replacement. Separate rail temperature, carriage thermal load and traction current. Check whether renewed control or supply equipment can interface with the remaining system through verifiable conditions, rather than assuming a component upgrade automatically improves the complete railway.',
[('1992','馬德里至塞維亞高速鐵路開始商業營運~The Madrid–Seville high-speed railway began commercial service'),('2025','IEC 發布新版鐵道 RAMS 第一部分通用程序~IEC published the revised railway RAMS Part 1 generic process')],
'https://www.adifaltavelocidad.es/w/lav-madrid-sevilla-historia','ADIF Alta Velocidad','塞維亞聖胡斯塔站周邊~Seville Santa Justa station area','西班牙~Spain',(37.392,-5.976),
 'thermal cooling powerloss pantograph neutral brakecurve interlock fatigue construction availability',
'''把日照下鋼軌溫度與陰影氣溫分開量測，建立熱應力基準。~Measure sunlit rail temperature separately from shaded air temperature to establish a thermal-stress reference.
比較滿載車廂和低載車廂的顯熱需求，保留新風條件。~Compare sensible cooling demand in full and lightly loaded cars while retaining ventilation conditions.
以同時加速列車造成的尖峰電流檢查饋線損失。~Check feeder losses against peak current from trains accelerating simultaneously.
在高溫接觸線張力改變時檢查波速和受電量測。~Check wave speed and current-collection measurements as contact-wire tension changes with heat.
計算分相區滑行的速度下降，避免假定列車瞬間失速。~Calculate speed reduction through a neutral section without assuming an instantaneous loss of motion.
讓改造前後控制系統使用相同的目標速度測試資料。~Use identical target-speed test data for control systems before and after renewal.
在新舊控制邊界注入不一致狀態，檢查進路是否保持禁止。~Inject inconsistent states at an old-new control boundary and check that the route remains prohibited.
對更新後構件區分已累積循環和新設備的起算點。~Distinguish accumulated cycles in retained components from the starting point of new equipment.
把夜間施工窗口拆成保護、作業、檢查與還路時間。~Split an overnight possession into protection, work, inspection and handback time.
把計畫性停機與非預期故障分列，避免混用可用性口徑。~Separate planned outages from unexpected faults rather than mixing availability definitions.''',second='https://www.adifaltavelocidad.es/modernizacion-lav-madrid-sevilla')

p(314,'長大高架高速走廊沉陷與營運韌性~Long viaduct high speed corridor settlement and resilience',
'以北京至上海高速鐵路為背景，建立長距離橋梁、路基與多城市車站組成的教學網路。重點是把局部沉陷和橋梁撓度與高速車輛反應聯繫，同時檢查多站停靠造成的班表差異、風險監測與修復後的服務恢復。~Use Beijing–Shanghai high-speed rail to construct a teaching network of bridges, earthworks and stations in several cities. Relate local settlement and bridge deflection to vehicle response at speed. At the same time, inspect differing stopping patterns, environmental monitoring and service restoration after repair, distinguishing an average network metric from a critical local defect.',
[('2011','北京至上海高速鐵路於六月投入營運~The Beijing–Shanghai high-speed railway entered service in June'),('2019','世界銀行發布中國高速鐵路發展研究報告~The World Bank published its study of Chinese high-speed rail development')],
'https://cqtz.crec.cn/zgztywz/core_business/infrastructure_construction/railways/index.html','China Railway Group','南京南站周邊~Nanjing South station area','中國~China',(31.969,118.797),
 'bridge settlement suspension cant crosswind mixed capacity fatigue survey redundancy',
'''以跨中和支點同步位移辨識高架橋靜態剛度而非單點位移。~Identify viaduct static stiffness through simultaneous midspan and support displacement rather than one reading.
對橋路過渡區畫出多點沉陷槽，檢查短基長坡折。~Plot a multipoint settlement trough at a bridge-earthwork transition and inspect short-baseline kinks.
把軌道變形波長轉成列車所見激振頻率。~Convert track-deformation wavelength into the excitation frequency experienced by a moving train.
比較不同速度等級服務通過同一曲線時的超高需求。~Compare cant demand when services of different speed classes pass through one curve.
在高架開闊段使用陣風而非日平均風速檢查側向力尺度。~Use gusts rather than daily mean wind to inspect the lateral-force scale on an exposed viaduct.
用多城市停站模式建立快慢列車的追趕時間圖。~Construct a catch-up timeline for fast and slow services with different city stopping patterns.
把跨區長途客流與短途區間客流分開計算滿載位置。~Separate interregional and shorter-distance demand when locating the most heavily loaded section.
分組計算不同車型與載重循環的損傷貢獻。~Group damage contributions from different train types and load cycles.
對連續水準測量做閉合檢核，辨認基準點漂移。~Perform closure checks on repeated levelling and identify datum movement.
檢查環境監測與通訊設備是否共享會同時失效的電源。~Check whether environmental monitoring and communication equipment share a common failing power source.''',second='https://documents1.worldbank.org/curated/en/933411559841476316/pdf/China-High-Speed-Rail-Development.pdf')

p(315,'濕熱山地高速線排水與高速氣動~Humid mountain high speed drainage and aerodynamics',
'以武漢至廣州高速鐵路為背景，設計跨越濕熱平原和山地區段的教學走廊。課程將暴雨排水、隧道壓力和長坡牽引連結，要求在設備受潮、黏著下降與列車降速時重算能量、制動與班表影響。~Use Wuhan–Guangzhou high-speed rail to construct a teaching corridor crossing humid plains and mountain sections. Connect storm drainage, tunnel pressure and sustained climbing. Recalculate energy, braking and timetable consequences when equipment becomes damp, adhesion falls and speed is restricted, retaining explicit boundaries between a hydraulic runoff estimate and a complete flood-protection design.',
[('2009','武漢至廣州高速鐵路於十二月開通營運~The Wuhan–Guangzhou high-speed railway opened in December'),('2019','世界銀行發布中國高速鐵路發展研究報告~The World Bank published its study of Chinese high-speed rail development')],
'https://cqtz.crec.cn/zgztywz/core_business/infrastructure_construction/railways/index.html','China Railway Group','廣州南站周邊~Guangzhou South station area','中國~China',(22.989,113.269),
 'drain tunnelwave grade adhesion isolation brake wheelheat filter powerloss availability',
'''把山坡逕流與線路集水面積分開估算，檢查雨強時間尺度。~Estimate hillside runoff and railway catchment separately and check rainfall-intensity duration.
比較隧道進出時的壓力尺度，保留列車速度的不確定度。~Compare entry and exit pressure scales while retaining uncertainty in train speed.
對長坡計算持續重力功率，另列加速與空氣阻力需求。~Calculate sustained gravitational power on a long climb and separately list acceleration and drag demand.
把降雨前後輪軌接觸分組，避免用乾軌係數代表濕軌。~Group contact conditions before and after rainfall instead of representing wet rails with a dry coefficient.
在潮濕設備箱情境下量測絕緣漏電，區分接地和正常回流。~Measure insulation leakage in a damp enclosure scenario and distinguish earthing from normal return current.
對低黏著降速情境重算停車距離與命令延遲。~Recalculate stopping distance and command delay for a low-adhesion restricted-speed condition.
在長下坡減速後估算煞車平均溫升並辨認熱點風險。~Estimate mean brake temperature rise after descending deceleration and identify hot-spot risk.
檢查濕濾材造成的壓差是否隨風量變動而改變判讀。~Check whether changing airflow confounds interpretation of pressure drop across wet filter media.
在長距離供電段比較不同電流造成的線路熱損失。~Compare line heating losses under different current levels in a long supply section.
把防水維修時間與正常設備修復分別納入停機紀錄。~Record waterproofing maintenance separately from normal equipment repair in downtime records.''',second='https://documents1.worldbank.org/curated/en/933411559841476316/pdf/China-High-Speed-Rail-Development.pdf')

p(316,'高原凍土鐵路熱平衡與長期變形~High altitude permafrost rail thermal balance and deformation',
'以青藏鐵路凍土地段為背景，建立路基熱量、地下冰與列車荷載共同作用的教學剖面。學徒必須分開季節凍融和長期溫度趨勢，將溫度、沉陷與排水量同步量測，並辨認縮尺熱模型不能直接預測真實凍土穩定年限。~Use the permafrost sections of the Qinghai–Tibet Railway to construct a teaching profile combining ground heat, ice and train loading. Separate seasonal freeze-thaw from long-term temperature trends. Measure temperature, settlement and drainage together, and identify why a scaled thermal model cannot directly predict the actual service life or stability of frozen ground.',
[('2006','青藏鐵路格爾木至拉薩段開始營運服務~The Golmud–Lhasa section of the Qinghai–Tibet Railway entered service'),('2023','中國政府公開報導青藏鐵路營運與西藏鐵路網背景~A government publication reviewed Qinghai–Tibet operations and the Tibetan railway network')],
'https://english.www.gov.cn/news/topnews/202301/18/content_WS63c76458c6d0a757729e5c5b.html','State Council of China','拉薩火車站周邊~Lhasa railway station area','中國~China',(29.623,91.065),
 'freeze settlement drain thermal survey pressure grade adhesion sampling availability',
'''將土層潛熱需求與可供冷量分開，辨認簡化凍結前緣的限制。~Separate soil latent-heat demand from available cooling and identify simplified freezing-front limits.
比較相鄰路基段的差異沉陷，避免只看整段平均下沉。~Compare differential settlement in neighbouring embankment sections instead of only average subsidence.
檢查融雪水與排水溝通暢度如何改變路基附近的入流水量。~Check how snowmelt and drain obstruction change water inflow beside the embankment.
將鋼軌熱應力與路基凍土熱狀態分為不同物理問題。~Treat rail thermal stress and the thermal condition of permafrost as distinct physical problems.
用穩定外部基點檢查長期高程趨勢，避免基點同時移動。~Check long-term elevation trends against a stable external datum rather than a moving local reference.
以高原氣壓情境檢查封閉容積溫度變化，保留理想氣體假設。~Use an altitude-pressure scenario to examine temperature change in a sealed volume under an ideal-gas assumption.
比較高原坡道的重力功率與額外阻力，不把海拔當成坡度。~Compare gradient power with other resistance at altitude without treating elevation itself as gradient.
在凍結或融水條件下比較黏著上限，保留試驗範圍。~Compare adhesion bounds under freezing or meltwater conditions while retaining the experimental range.
選擇足以分辨日夜熱循環與列車振動的不同取樣頻率。~Choose different sampling rates for daily thermal cycles and train-induced vibration.
把遠距維修交通時間與實際修復工時分開記錄。~Record travel time for remote maintenance separately from the hands-on repair duration.''')

p(317,'城際高速系統車輛升級與運轉介面~Intercity high speed vehicle renewal and operating interfaces',
'以京釜高速鐵路及韓國高速列車演進為背景，建立不同車輛世代共用走廊的教學時刻表。課程比較牽引、制動、懸吊與受電特性改變後的介面需求，要求以共同量測基準評估車輛更新，而非只比較額定最高速度。~Use the Gyeongbu corridor and Korean high-speed train development to construct a teaching timetable shared by different vehicle generations. Compare interface demands after changes in traction, braking, suspension and current collection. Evaluate renewal using common measurement references, rather than only rated top speed, and track whether differences in dwell or maintenance alter delivered passenger service.',
[('2004','韓國高速鐵路 KTX 開始提供營運服務~KTX high-speed rail began passenger service in South Korea'),('2010','韓國鐵道公社導入 KTX 山川號列車服務~Korail introduced KTX Sancheon passenger services')],
'https://info.korail.com/info/contents.do?key=855','Korail','大田高速鐵路站周邊~Daejeon high speed station area','韓國~South Korea',(36.332,127.435),
 'grade brake suspension pantograph wheelheat mixed dwell fleet bearing redundancy',
'''以相同坡度和總質量比較不同牽引方案的需求功率。~Compare required power for alternative traction arrangements at equal gradient and total mass.
把不同車輛的制動建立時間與穩態減速度分開辨識。~Identify brake build-up time separately from steady deceleration for different vehicles.
比較不同懸吊剛度對滿載固有頻率及行程需求的影響。~Compare effects of suspension stiffness on loaded natural frequency and travel demand.
在共用架線條件下檢查不同受電配置的動態量測。~Inspect dynamic measurements for different collection arrangements under shared overhead conditions.
用相同煞車能量比較不同有效熱容量，標註能量分配。~Compare different effective thermal capacities under equal braking energy and state the allocation.
分析不同停站模式列車在共用線上的追趕位置。~Analyse where services with different stopping patterns catch one another on a shared route.
對不同車門數配置檢查乘客集中造成的停站尾端。~Inspect dwell tails from passenger concentration under different door-count arrangements.
把檢修備用和營運循環車數分開，避免把全部庫存算成上線能力。~Separate maintenance spares from circulating train requirements instead of treating total stock as available service.
以軸承幾何和轉速建立故障頻率參考，避免僅比振幅。~Use bearing geometry and rotation speed to establish fault-frequency references rather than comparing amplitude alone.
對新舊列車共用的供電與通訊檢查共因失效。~Check common-cause failure in power and communication shared by old and new trains.''')

p(318,'沙漠高速線砂塵熱量與旅客尖峰~Desert high speed sand heat and pilgrimage demand',
'以麥加至麥地那高速鐵路為背景，建立高溫、砂塵及集中旅客到達並存的教學案例。學徒把進氣過濾、散熱、供電和月台人流連結，在集中特殊需求下檢查系統瓶頸；所有人數與氣候數值均為自訂算例而非營運資料。~Use the Haramain high-speed corridor to frame a teaching case combining heat, airborne sand and concentrated passenger arrivals. Connect intake filtration, cooling, power supply and platform flow under exceptional demand. All passenger and weather numbers are invented exercises, and students must distinguish a bottleneck revealed by a model from a verified constraint on the actual railway.',
[('2018','哈拉曼高速鐵路開始商業旅客服務~Haramain high-speed railway began commercial passenger service'),('2021','沙烏地鐵路公司重組形成整合營運背景~Saudi railway restructuring established an integrated operating context')],
'https://www.sar.com.sa/about-sar/ourstory/','Saudi Arabia Railways','麥地那高速鐵路站周邊~Madinah high speed station area','沙烏地阿拉伯~Saudi Arabia',(24.48,39.671),
 'sand filter cooling thermal crosswind powerloss platform queue baggage fleet',
'''把砂粒濃度與通過風量連結，估算清理週期所需捕集質量。~Relate sand concentration to airflow and estimate collected mass for a cleaning interval.
比較乾淨與積塵濾材的壓差，將風量保持在可比較範圍。~Compare clean and dust-loaded filter pressure drop while holding airflow in a comparable range.
分開乘客、設備和外氣顯熱，檢查尖峰冷房負載。~Separate passenger, equipment and outdoor-air sensible heat when checking peak cooling demand.
比較曝曬鋼軌和遮蔭軌段的溫度，不以氣象站讀值直接替代。~Compare exposed and shaded rail temperature without directly substituting a weather-station reading.
對砂塵風中的側向風速單獨量測，不以能見度推估風力。~Measure crosswind separately during dusty conditions instead of inferring wind force from visibility.
在冷房和牽引同時高負載時估算供電回路的熱損失。~Estimate supply-loop heating loss when cooling and traction loads peak together.
將集中到達旅客分布到候車與流動區域，保留通道淨空。~Distribute concentrated arrivals across waiting and movement zones while preserving clear paths.
用批次旅客測試服務台隊列，指出平穩到達假設失效的位置。~Test a service-desk queue with batch arrivals and locate where stationary-arrival assumptions fail.
把大件行李處理與旅客通行時間分開觀測。~Observe large-baggage handling separately from passenger passage time.
依尖峰班距與完整循環時間估算上線車數和備用需求。~Estimate circulating trains and spare needs from peak headway and complete round-trip time.''',second='https://grupo.renfe.com/es/en/corporations/international-projects/haramain-project')

p(319,'新興高速走廊既有線銜接與能源~Emerging high speed corridor interfaces and energy',
'以摩洛哥丹吉爾至蓋尼特拉高速線為背景，建立高速專用段與既有網路連接的教學走廊。學徒比較不同區段速度、供電和停站模式，追蹤旅客轉乘及列車循環，並用原創算例檢查能源改善是否只是把負荷轉移到另一時段。~Use Morocco’s Tangier–Kenitra high-speed line to construct a teaching corridor joining a dedicated fast section to an existing network. Compare section speeds, supply boundaries and stopping patterns. Track passenger connections and train circulation, and test whether an apparent energy improvement merely shifts demand to another time instead of reducing total delivered energy.',
[('2018','摩洛哥阿爾波拉克高速服務正式揭幕~Morocco inaugurated Al Boraq high-speed service'),('2019','摩洛哥國家鐵路發布阿爾波拉克一周年營運回顧~ONCF published a first-anniversary review of Al Boraq operations')],
'https://www.oncf.ma/fr/Actualites/Al-boraq-notre-fierte-nationale','ONCF','丹吉爾城市車站周邊~Tangier Ville station area','摩洛哥~Morocco',(35.771,-5.787),
 'mixed brakecurve neutral voltage regen drag thermal transfer fleet availability',
'''在高速段出口檢查快車追上既有線列車的時間裕度。~Check catch-up margin where a fast train exits onto infrastructure shared with slower services.
將高速段至低速區的目標速度分段建立保護曲線。~Build staged protection curves for the transition from fast running to a lower-speed section.
比較供電分界前不同入口速度的無動力滑行距離。~Compare unpowered coasting distance at a supply boundary for different entry speeds.
在接續區段定義完整供電回路，避免只計一條導線壓降。~Define the complete supply loop at the connection rather than only one conductor’s voltage drop.
對不同停站模式比較可回收能量與同時受電條件。~Compare recoverable energy and simultaneous receptivity for different stopping patterns.
計算高速專用段的氣動功率，與行車時間節省並列。~Calculate aerodynamic power on the dedicated fast section alongside the travel-time saving.
將鋼軌溫度和維修後拘束狀態作為熱應力的獨立輸入。~Treat rail temperature and post-maintenance restraint as independent thermal-stress inputs.
把轉乘步行與候車分開，檢查班表銜接對總旅程的效果。~Separate transfer walking from waiting and examine timetable coordination over the complete journey.
讓慢速接續段時間進入完整車組循環，避免低估用車數。~Include time on the slower connecting section in the complete fleet cycle.
比較高速專用段和共同設備的停機事件對全程服務的影響。~Compare how outages on the dedicated fast section and shared equipment affect end-to-end service.''',second='https://www.oncf.ma/fr/Actualites/Al-boraq-souffle-sa-premiere-bougie-et-enregistre-un-franc-succes')

p(320,'熱帶新建高速線橋隧與接駁系統~Tropical new high speed bridges tunnels and feeder service',
'以雅加達至萬隆高速鐵路為背景，建立熱帶丘陵中的橋隧連續路線及接駁旅程。學徒從降雨、坡度和曲線開始，延伸到車站轉乘與需求批次到達，要求把列車行車時間和門到門旅程時間分別驗證。~Use the Jakarta–Bandung high-speed railway to construct a tropical hillside route with successive bridges, tunnels and feeder journeys. Begin with rainfall, gradients and curves, then extend the analysis to station interchange and batch arrivals. Verify train running time separately from door-to-door journey time so that fast line-haul service is not mistaken for a complete passenger-experience result.',
[('2023','雅萬高速鐵路於十月舉行啟用並開始付費服務~Jakarta–Bandung high-speed rail was inaugurated and began paid service in October'),('2024','營運者發布服務累計旅客與旅遊連結回顧~The operator published a review of accumulated ridership and tourism connections')],
'https://kcic.co.id/kcic-siaran-pers/ulang-tahun-ke-8-pt-kcic-resmikan-penjualan-tiket-kereta-cepat-whoosh-dari-berbagai-aplikasi-dan-hadirkan-promo-tiket/','PT Kereta Cepat Indonesia China','萬隆帕達拉朗站周邊~Bandung Padalarang station area','印尼~Indonesia',(-6.843,107.498),
 'bridge settlement drain grade cant seismic tunnelwave transfer queue fleet',
'''在高架橋量測跨中及支點位移，區分彎曲與基礎移動。~Measure viaduct midspan and support displacement to distinguish bending from foundation movement.
追蹤橋台與填土路基之間的差異沉陷長度尺度。~Track the length scale of differential settlement between an abutment and filled earthworks.
比較短時強降雨與長時降雨對集水估算的不同假設。~Compare assumptions for short intense rainfall and longer rainfall in catchment estimates.
把山區坡度帶來的持續功率與加速功率分別列出。~List sustained gradient power separately from acceleration power on a hillside section.
比較曲線設計速度與降速通過情境的未平衡加速度。~Compare unbalanced acceleration at design speed and during a restricted-speed passage.
用不同震源距離檢查預警可用提前量，不宣稱可預測地震。~Check available lead time at different source distances without claiming earthquake prediction.
將隧道阻塞比與進洞速度分開，檢查壓力模型敏感度。~Separate blockage ratio and entry speed when examining pressure-model sensitivity.
把接駁列車步行、等待和搭乘分成可核對的旅程段。~Split feeder walking, waiting and riding into independently verifiable journey stages.
以接駁車批次到達模擬服務台隊列，辨認非平穩需求。~Simulate service queues under batch feeder arrivals and identify nonstationary demand.
把接駁與高速列車班距分開排程，檢查整體銜接需求。~Schedule feeder and high-speed headways separately and inspect connection requirements.''',second='https://kcic.co.id/kcic-siaran-pers/whoosh-telah-layani-4-juta-penumpang-dampak-positif-di-bidang-pariwisata/')

p(321,'都市穿越線多介面控制與地下車站~Urban cross-city control interfaces and underground stations',
'以倫敦伊莉莎白線連接既有鐵路與新建中央隧道的情境為背景，建立多運轉區段的教學案例。課程把定位、通訊、車門及轉乘人流串成事件鏈，要求先證明每個邊界的允許狀態，再討論端到端班距與乘客便利。~Use the Elizabeth line’s connection of existing railways through a new central tunnel as the setting for a multi-section teaching case. Link localisation, communication, doors and interchange flows in an event chain. Establish permissible states at each boundary before discussing end-to-end headway or passenger convenience, and explicitly distinguish test readiness from the commencement of revenue service.',
[('2021','伊莉莎白線開始試運轉並進入試營運階段~The Elizabeth line began trial running and progressed into trial operations'),('2022','伊莉莎白線中央區段於五月開放旅客服務~The Elizabeth line central section opened to passengers in May')],
'https://tfl-newsroom.prgloo.com/news/tfl-press-release-elizabeth-line-to-open-on-24-may-2022','Transport for London','倫敦法靈頓車站周邊~London Farringdon station area','英國~United Kingdom',(51.52,-0.105),
 'localize communication brakecurve doors dwell platform ventilation transfer interlock availability',
'''在中央隧道與地面接續處追蹤位置誤差包絡。~Track the position-error envelope at the connection between central tunnel and surface sections.
對每次運轉模式轉換記錄封包年齡與授權狀態。~Record packet age and authority state for every operating-mode transition.
用相同距離基準檢查目標速度和保護曲線的關係。~Use a common distance reference to compare target speed with the protective curve.
將月台門和車門確認分開，列出安全發車必需條件。~Separate platform-door and train-door confirmation and list necessary departure conditions.
檢查長月台上旅客分布不均如何影響最慢門組。~Inspect how uneven distribution along a long platform affects the slowest door group.
以轉乘批次到達比較平均密度與局部通道壅塞。~Compare mean density with local passage congestion under interchange batch arrivals.
分開隧道活塞風和車站一般換氣的量測邊界。~Separate measurement boundaries for tunnel piston airflow and normal station ventilation.
把電扶梯與深層步行連通道分開計算轉乘時間。~Calculate transfer time separately for escalators and deep-level walking connections.
在接續區段以進路狀態表確認衝突移動不能同時授權。~Use a route-state table to confirm conflicting movements cannot receive simultaneous authority.
區分中央區段設備可用性與整條跨城服務的可用性。~Distinguish central-section equipment availability from availability of the complete cross-city service.''',second='https://tfl.gov.uk/cdn/static/cms/documents/elizabeth-line-post-opening-evaluation-interim-findings.pdf')

p(322,'都會區域幹線分支合流與尖峰人流~Metropolitan regional branches merging and peak passenger flow',
'以巴黎 RER A 的都會區域運輸背景，建立分支線列車進入共同核心段的教學模型。學徒比較列車合流、月台交換與下游延誤恢復，並以逐列隊列檢查高頻服務中平均班距容易掩蓋的局部擁擠。~Use Paris RER A as a metropolitan regional-rail setting for a teaching model in which branch trains enter a common core. Compare merging, platform exchange and downstream recovery. Track queues train by train to expose local crowding hidden by average headway, and separate a higher scheduled frequency from the ability of the busiest doors to complete passenger exchange.',
[('1969','巴黎區域快鐵東側早期路段開始營運~An early eastern section of the Paris regional express network opened'),('1977','巴黎奧貝爾與民族廣場間中央連結開通~The central connection between Auber and Nation opened in Paris')],
'https://www.ratp.fr/decouvrir/patrimoine/des-lignes-d-histoires','RATP','巴黎里昂車站周邊~Paris Gare de Lyon station','法國~France',(48.845,2.374),
 'mixed capacity dwell platform congestion interlock turnback regen transfer fleet',
'''讓兩條分支的列車到達時間競爭同一核心段進路。~Make arrival times from two branches compete for the same core-section route.
以核心段逐列負載驗算運能，保留無法登車的隊列。~Check core capacity train by train and retain the queue unable to board.
把轉乘樓梯附近門組與其他門組分開記錄交換時間。~Record exchange time separately for doors beside interchange stairs and other doors.
將月台等候面積扣除通行與設備占用，辨認有效區域。~Subtract circulation and equipment occupation from waiting area to identify usable platform space.
用人流密度與速度之間的關係解釋壅塞傳播。~Use the relationship between pedestrian density and speed to explain congestion propagation.
為分支合流建立互斥進路，注入一班晚到列車。~Build mutually exclusive routes at a branch merge and inject one late train.
檢查短線折返列車是否占用核心區段的必要進路。~Check whether a short-turn service occupies routes needed by the core service.
比較核心段密集煞車與相鄰列車加速的時間重疊。~Compare frequent core-section braking with the acceleration timing of neighbouring trains.
分開同月台換車與垂直轉乘，避免使用單一平均時間。~Separate cross-platform changes from vertical transfers instead of one mean time.
將不同分支往返時間分別納入循環車組估算。~Include different branch round-trip durations separately in circulating fleet estimates.''',second='https://www.iledefrance-mobilites.fr/decouvrir/histoire')

p(323,'機場快線長橋與航廈處理介面~Airport express long bridges and terminal processing',
'以香港機場快綫的城市與機場連接為背景，建立長橋通過、行李服務與航廈步行相連的旅程。學徒要區分列車時間、報到排隊與到登機口的移動，並在側風或服務中斷情境下分析乘客如何累積與轉移。~Use Hong Kong Airport Express to frame a journey linking long-bridge passage, baggage processing and terminal walking. Distinguish train time from check-in queues and movement toward a departure gate. Under crosswind restrictions or interrupted service, analyse passenger accumulation and redistribution without assuming that the scheduled train journey represents the complete airport access time.',
[('1998','香港機場快綫配合新機場啟用投入服務~Hong Kong Airport Express entered service with the new airport'),('2005','機場快綫延伸至亞洲國際博覽館站~Airport Express was extended to AsiaWorld-Expo station')],
'https://www.hyd.gov.hk/en/road_and_railway/railway_network/ael/index.html','Hong Kong Highways Department','香港九龍站周邊~Hong Kong Kowloon station area','香港~Hong Kong',(22.304,114.161),
 'crosswind bridge baggage queue transfer dwell fleet voltage brake availability',
'''在跨海暴露段將陣風與平均風分開，檢查側向作用尺度。~Separate gust and mean wind on an exposed crossing when checking lateral-force scale.
以橋跨與支點位移分別檢查車軌幾何變化的來源。~Use span and support movements separately to identify sources of changing track geometry.
將市區報到行李的服務時間與裝載空間需求分開量測。~Measure city check-in baggage handling time separately from loading-space demand.
模擬航班集中報到，檢查櫃台利用率接近一的後果。~Simulate clustered flight check-in and examine the consequences of counter utilisation approaching unity.
把車站出口至航廈目的地的垂直及水平移動分段。~Separate vertical and horizontal travel from station exit to the terminal destination.
用大件行李群組上車測試車門交換尾端。~Test door-exchange tails with groups boarding alongside large baggage.
把航廈端與市區端折返時間都納入完整循環。~Include both airport-terminal and city-terminal turnarounds in the complete cycle.
對長距離受電路徑建立回路電阻和受電電壓估算。~Estimate loop resistance and receiving voltage for a long supply path.
在受風降速後重新比較停止距離與原班表的裕度。~Recompare stopping distance and timetable margin after wind-related speed restriction.
把報到系統可用性與列車系統可用性分別呈現。~Present check-in system availability separately from train-system availability.''',second='https://www.mtr.com.hk/en/customer/services/airport_express_index.html')

p(324,'地下自動化捷運牽引通訊與疏散~Underground automated metro traction communication and egress',
'以新加坡東北地鐵線為背景，建立全地下自動運轉的教學案例。課程把供電、定位、車門與通風連成系統事件鏈，並以通訊失效和列車停在站間的情境檢查旅客資訊、備援能源及復原次序。~Use Singapore’s North East Line as the setting for an underground automated-operation teaching case. Connect power, localisation, doors and ventilation through system events. Use lost communication and an interstation stop to test passenger information, backup energy and recovery sequence, while distinguishing a reliable data link from the proof that a movement is safely authorised.',
[('2003','新加坡東北地鐵線開始營運服務~Singapore’s North East Line entered passenger service'),('2024','東北線榜鵝海岸站於十二月開放營運~Punggol Coast station on the North East Line opened in December')],
'https://www.lta.gov.sg/content/ltagov/en/getting_around/public_transport/rail_network/north_east_line.html','Singapore Land Transport Authority','新加坡盛港站周邊~Singapore Sengkang station area','新加坡~Singapore',(1.391,103.895),
 'communication localize interlock doors ventilation piston voltage isolation backup redundancy',
'''以封包遺失和延遲分別測試自動運轉的授權有效期。~Test automatic-operation authority validity separately under lost packets and delayed packets.
把輪徑誤差對地下定位的累積與參考點校正分開。~Separate accumulated underground odometry error from correction at reference points.
對站間列車和後續列車建立進路不可同時允許的條件。~Define conditions that prohibit conflicting authority for an interstation train and a following train.
在車門位置回報與鎖閉回報不一致時檢查發車禁止。~Check departure inhibition when door-position and lock confirmations disagree.
把一般換氣與停車時旅客負荷分開建立空氣量估算。~Estimate normal ventilation separately from passenger load during a stopped-train scenario.
用列車排開的體積檢查隧道壓力與風速的簡化關係。~Use displaced train volume to inspect a simplified relationship between tunnel flow and pressure.
在最遠受電位置估算壓降，列明供電和回流路徑。~Estimate voltage drop at the farthest receiving position and state supply and return paths.
檢查潮濕設備區的絕緣漏電，避免與正常回流混淆。~Check insulation leakage in damp equipment areas without confusing it with normal return current.
把資訊顯示、通訊和照明分開列出備援能源負載。~List backup-energy loads separately for information displays, communication and lighting.
檢查兩個控制通道是否仍共享機房、時鐘或電源。~Check whether two control channels still share a room, clock or supply.''',second='https://www.mot.gov.sg/news-resources/newsroom/opening-speech-by-minister-for-transport-and-second-minister-for-finance--mr-chee-hong-tat-at-the-opening-of-punggol-coast-mrt-station/')

p(325,'沙漠都市自動捷運熱管理與高架介面~Desert urban automated metro thermal and elevated interfaces',
'以杜拜地鐵紅線為背景，建立高架路段、空調車站與自動列車組成的教學系統。學徒需在砂塵、強日照與尖峰旅客並存時辨認冷卻及濾材維護瓶頸，並檢查旅客轉乘路徑和緊急供電對服務恢復的影響。~Use Dubai Metro Red Line to construct a teaching system with elevated sections, conditioned stations and automated trains. Under dust, intense sunlight and peak arrivals, identify cooling and filter-maintenance bottlenecks. Examine how transfer paths and emergency power affect service restoration, keeping outdoor weather observations separate from measured equipment and rail temperatures.',
[('2009','杜拜地鐵紅線於九月開始旅客服務~Dubai Metro Red Line began passenger service in September'),('2021','杜拜地鐵與電車營運維護交由新營運團隊~A new operating team took over Dubai Metro and Tram operations and maintenance')],
'https://rta.ae/wps/portal/rta/ae/home/news-and-media/all-news/NewsDetails/2.4-billion-riders-carried-by-dubai-metro-over-15-years','Dubai Roads and Transport Authority','杜拜聯合車站周邊~Dubai Union station area','阿拉伯聯合大公國~United Arab Emirates',(25.266,55.314),
 'cooling sand filter thermal doors platform escalator communication voltage backup',
'''比較月台、連通道和車廂的顯熱邊界，不以一個溫度代表全部區域。~Compare sensible-heat boundaries for platforms, links and cars rather than using one temperature for every zone.
把砂塵濃度與設備進氣量相乘，估算一個維修週期的積塵。~Multiply dust concentration by equipment intake flow to estimate loading over a maintenance interval.
在固定風量下比較積塵前後壓差，檢查濾材狀態。~Compare pressure drop before and after loading at fixed airflow to assess filter condition.
以日照鋼軌本體溫度計算受限熱應力，不直接套用氣溫。~Calculate restrained thermal stress from sunlit rail temperature rather than directly from air temperature.
將月台門開啟造成的空氣交換和安全鎖閉邏輯分開分析。~Analyse air exchange during platform-door opening separately from safe locking logic.
把旅客批次到達配置到車門附近不同候車區域。~Distribute batch passenger arrivals among different waiting zones near train doors.
比較步行與電扶梯速度對跨越道路連通道的轉乘時間。~Compare walking and escalator speed effects on transfer time across road-spanning links.
在通訊延遲情境中保留安全狀態，不以成功連線等同允許發車。~Retain a safe state under delayed communication rather than treating connection success as departure permission.
檢查高溫輔助負載與列車加速同時發生時的受電壓降。~Check receiving voltage when heat-related auxiliary load coincides with train acceleration.
分別估算疏散照明和乘客資訊的備援時間，保留負載優先序。~Estimate backup duration for egress lighting and passenger information separately and retain load priorities.''',second='https://rta.ae/wps/portal/rta/ae/home/news-and-media/all-news/NewsDetails/rta-announces-taking-over-of-dubai-metro-and-tram-operation-and-maintenance-by-keolis-mhi-llc?lang=ar')

p(326,'環狀自動捷運循環班表與深層車站~Automated orbital metro cycles and deep stations',
'以哥本哈根環狀地鐵為背景，建立沒有一般端點折返的循環營運實驗。課程研究列車間距、局部停站延誤與車站人流如何沿環線傳遞，並連接地下施工變形、垂直交通和設備備援的驗證資料。~Use Copenhagen Cityringen to construct a circular-operation experiment without a normal terminal reversal at each end. Study how train spacing, local dwell delays and station passenger flow propagate around the loop. Connect the operating model to evidence from underground construction movement, vertical circulation and equipment backup, avoiding the assumption that removing a terminus removes every capacity constraint.',
[('2011','哥本哈根環狀地鐵進入建設施工階段~Construction work for Copenhagen Cityringen began'),('2019','哥本哈根環狀地鐵於九月開放旅客服務~Copenhagen Cityringen opened to passengers in September')],
'https://metroselskabet.dk/da/kontakt-og-presse/presse/pressemeddelelser/cityringen-aabner-den-29-september/','Metroselskabet','哥本哈根城市廳站周邊~Copenhagen City Hall station area','丹麥~Denmark',(55.676,12.569),
 'fleet capacity dwell communication localize escalator ventilation settlement grout redundancy',
'''用單圈時間取代雙端折返循環，計算環線所需列車數。~Use loop time instead of a two-terminal cycle to calculate trains required on the ring.
把環線某站延誤後的實際班距逐班記錄，檢查運能。~Record successive headways after delay at one loop station and inspect delivered capacity.
比較環線各站不均勻交換需求對最大停站時間的控制。~Compare how uneven station exchange demand controls the longest dwell around the loop.
檢查循環運轉中授權資料到期如何影響後續列車。~Inspect how authority-data expiry affects following trains during circular operation.
在重複繞圈情境中檢查定位偏差是否獲參考點校正。~Check whether localisation bias is corrected at reference points during repeated circuits.
把深層車站垂直移動與出口步行時間分開量測。~Measure deep-station vertical travel separately from walking to the exit.
比較深層站有效通風容積與換氣率的單位定義。~Compare effective deep-station ventilation volume with the units used for air-change rate.
對施工鄰近建築建立多點沉陷剖面與穩定外部基準。~Build multipoint settlement profiles and a stable external datum for buildings near construction.
以假想環隙建立灌漿體積平衡，區分理論體積與實注量。~Construct a hypothetical annulus grout balance and distinguish theoretical from injected volume.
檢查環線控制備援是否仍受同一供電或機房事件影響。~Check whether ring-control redundancy remains exposed to one supply or equipment-room event.''',second='https://regeringen.dk/aktuelt/nyheder/2018/milepael-skinner-forbinder-cityringen/')

p(327,'新建自動捷運橋隧轉換與系統驗收~New automated metro bridge tunnel transitions and assurance',
'以雪梨地鐵西北線為背景，建立高架、地下與轉乘站交替的自動運轉教學路線。學徒從結構變形追蹤到定位和車門介面，並以不同試驗證據檢查全線服務是否具備可追溯的驗收條件與復原能力。~Use Sydney Metro Northwest as the setting for an automated-operation teaching route alternating elevated, underground and interchange sections. Trace structural movement through localisation and door interfaces. Use different test evidence to check whether the complete service has traceable acceptance conditions and recovery capability, instead of treating successful operation of one train as proof of full-system readiness.',
[('2019','雪梨地鐵西北線於五月開始旅客服務~Sydney Metro Northwest began passenger service in May'),('2024','雪梨地鐵網路向市中心延伸投入服務~The Sydney Metro network extension toward the city centre entered service')],
'https://www.sydneymetro.info/about','Sydney Metro','雪梨塔拉旺站周邊~Sydney Tallawong station area','澳洲~Australia',(-33.691,150.906),
 'bridge settlement localize communication doors brakecurve capacity transfer backup availability',
'''在高架跨中與橋端同步量測，辨認橋隧交界的變形來源。~Measure viaduct midspan and ends together to identify movement sources near a bridge-tunnel transition.
把過渡段差異沉陷的基長與車輪感受的不平順波長比較。~Compare differential-settlement baseline with the irregularity wavelength experienced by wheels.
對地上轉入地下的定位感測變化建立誤差包絡。~Build an error envelope for changes in localisation sensing between surface and underground sections.
注入通訊延遲後追蹤自動列車的授權和安全狀態。~Inject communication delay and track an automated train’s authority and safe state.
將停準、月台門對位及鎖閉確認分成不同驗收條件。~Separate stopping accuracy, platform-door alignment and lock confirmation into distinct acceptance conditions.
用目標站停車點和速度限制建立有明確邊界的監督曲線。~Construct a bounded supervision curve from the target stop and speed restriction.
比較預定班距與實際乘載分布，辨認車站瓶頸。~Compare scheduled headway with actual load distribution to identify station constraints.
把轉乘步行、垂直移動與等待拆成可量測旅程。~Split interchange walking, vertical movement and waiting into measurable journey stages.
在單一電源失效時檢查乘客資訊與疏散照明續航。~Check passenger-information and egress-lighting endurance after a single supply failure.
以驗收試運轉故障紀錄討論修復時間與服務可用性。~Use trial-operation fault records to discuss repair duration and service availability.''',second='https://international.austrade.gov.au/en/news-and-analysis/news/international-consortium-multibillion-dollar-sydney-metro-project')

p(328,'機場都市分支捷運合流與車站容量~Airport urban branched metro merging and station capacity',
'以溫哥華加拿大線連結市中心、列治文與機場的背景，建立兩分支匯入共用核心段的教學班表。學徒分析機場行李旅客與通勤族不同上車時間，並將橋梁、終端折返與車隊配置納入同一套容量檢核。~Use the Canada Line’s links among central Vancouver, Richmond and the airport to construct a teaching timetable with two branches entering a common core. Analyse different boarding times for airport passengers with baggage and commuters. Include bridges, terminal reversal and fleet allocation in one capacity review so that branch demand and core service are checked together.',
[('2005','加拿大線工程於十一月開始建設施工~Canada Line construction began in November'),('2009','加拿大線於八月開始旅客服務~Canada Line began passenger service in August')],
'https://buzzer.translink.ca/2014/08/canada-line-turns-five-years-old-today/','TransLink','溫哥華濱海車站周邊~Vancouver Waterfront station area','加拿大~Canada',(49.286,-123.112),
 'mixed interlock dwell baggage capacity turnback fleet bridge regen transfer',
'''讓機場與都市分支列車在共用區段競爭進入時刻。~Make airport and urban-branch trains compete for entry times to the common section.
為分支道岔列出鎖閉、占用與進路互斥條件。~List switch locking, occupation and route-exclusion conditions at the branch junction.
比較行李客群與通勤客群在相同車門配置下的交換時間。~Compare exchange time for baggage travellers and commuters with identical door arrangements.
將行李放置與車門通行分開，檢查空間對服務時間的影響。~Separate baggage placement from doorway passage and examine how space affects service time.
對共同核心段計算有效運能，同時保留分支負載差異。~Calculate usable capacity in the shared core while retaining different branch loads.
比較兩個分支端點折返時間，辨認較慢循環的影響。~Compare turnaround at the two branch terminals and identify the effect of the slower cycle.
依各分支完整循環估算車數，不能直接平均往返時間。~Estimate fleet requirements from each branch’s complete cycle rather than simply averaging round trips.
用橋跨靜態模型檢查尺度，再列出動態驗證需求。~Use a static bridge model to check magnitude, then list the required dynamic verification.
比較兩分支列車加速與核心段煞車的時間重疊。~Compare acceleration on the branches with braking times in the common core.
把機場航廈與市中心轉乘路徑分開建立步行模型。~Build separate walking models for the airport terminal and downtown interchange.''',second='https://archive.news.gov.bc.ca/releases/news_releases_2005-2009/2009tran0002-000047.htm')

p(329,'深層都市地鐵建設沉陷與垂直交通~Deep urban subway construction settlement and vertical circulation',
'以紐約第二大道地鐵一期為背景，建立密集街廓下方新站與既有線銜接的教學剖面。課程把測量、灌漿、施工時間窗口及乘客垂直交通結合，要求分開施工變形控制和營運期人流驗證，並保留不確定度。~Use Second Avenue Subway Phase 1 to construct a teaching section with new stations beneath dense city blocks and a connection to an existing line. Combine surveying, grouting, possession windows and vertical passenger movement. Keep construction-movement control distinct from operational passenger-flow validation, and retain uncertainty rather than treating one instrument reading as a complete statement about building or station performance.',
[('2007','第二大道地鐵一期進入隧道建設階段~Second Avenue Subway Phase 1 entered its tunnel construction phase'),('2017','第二大道地鐵一期於元旦開放旅客服務~Second Avenue Subway Phase 1 opened to passengers on New Year’s Day')],
'https://www.skanska.com/us/en/media/press-releases/2017/skanska-usa-celebrates-grand-opening-of-second-avenue-subway','Skanska','紐約第二大道七十二街站~New York Second Avenue 72nd Street station','美國~United States',(40.769,-73.958),
 'survey settlement grout construction escalator ventilation platform drain interlock noise',
'''對街區水準測量做閉合檢核並以穩定外部基準控制漂移。~Check closure in block-level levelling and control drift against a stable external datum.
將建築兩端高差與中間沉陷槽分開，檢查測點密度。~Separate end-to-end building difference from an intermediate trough and inspect point spacing.
用環隙幾何估算漿量，另外記錄超灌與回流來源。~Estimate grout volume from annular geometry and separately record excess injection and returns.
把接續工程窗口分成隔離、施工、測試與還路的串聯任務。~Split a connection-work possession into isolation, work, testing and handback tasks.
比較深層站電扶梯和樓梯的服務量及移動時間。~Compare escalator and stair throughput and travel time at a deep station.
建立車站一般換氣量，清楚區別火災煙流分析。~Estimate normal station ventilation while clearly separating fire-smoke analysis.
把月台候車、行走和設備占用劃成不同有效面積。~Divide platform waiting, movement and equipment occupation into distinct usable areas.
以入口短時降雨估算排水量，檢查泵浦停止時的積水。~Estimate entrance runoff during a short storm and examine accumulation with the pump stopped.
為新線接入既有線列出不可同時授權的進路。~List routes that cannot be authorised simultaneously where the new line joins the existing railway.
將施工和營運聲源分開，以聲能方式計算合成量級。~Separate construction and operating sources and combine their acoustic energy levels.''',second='https://www.arup.com/globalassets/downloads/arup-journal/the-arup-journal-2017-issue-1.pdf')

p(330,'市中心輕軌連通線路網重整與轉乘~Downtown light rail connector network reconfiguration and transfers',
'以洛杉磯區域連接線把既有路線貫通的背景，建立服務路徑重新組合的教學案例。學徒比較少一次轉乘與核心區段增班的不同效果，檢查合流進路、月台交換、地下站排水和施工交接如何共同決定實際效益。~Use the Los Angeles Regional Connector to construct a teaching case about through-running and reconfigured service paths. Compare the benefit of removing one transfer with that of increasing frequency in the central section. Examine how merge routes, platform exchange, underground drainage and construction handback jointly determine the realised passenger benefit, rather than assuming a shorter route diagram guarantees shorter journeys.',
[('2014','區域連接線取得聯邦資金協議推進建設~The Regional Connector secured a federal funding agreement advancing construction'),('2023','洛杉磯區域連接線於六月開放旅客服務~The Los Angeles Regional Connector opened to passengers in June')],
'https://thesource.metro.net/one-year-in-a-look-back-on-some-of-our-favorite-regional-connector-moments/','Los Angeles County Metropolitan Transportation Authority','洛杉磯小東京藝術區站~Los Angeles Little Tokyo Arts District station','美國~United States',(34.05,-118.238),
 'transfer mixed interlock capacity dwell localize drain settlement construction congestion',
'''比較原先轉乘步行和等待與貫通列車旅程中的剩餘時間。~Compare former transfer walking and waiting with remaining time in a through-running journey.
讓不同端點列車在共同地下段競爭進入時刻。~Make trains from different outer termini compete for entry into the common underground section.
在連接既有線的位置建立進路互斥和釋放條件。~Establish route exclusions and release conditions at connections to existing lines.
以核心段逐班服務量檢查增班後真正可用的運能。~Check actual usable capacity from successive central-section services after frequency increases.
分析乘客路徑改變是否讓原本較輕的車門變成瓶頸。~Analyse whether changed passenger paths make previously lightly used doors become bottlenecks.
在新舊線定位參考切換時保留誤差和狀態紀錄。~Retain error and state records when localisation references change between new and existing sections.
用地下站入口集水建立泵浦停機時的體積平衡。~Build a volume balance for underground station-entrance runoff during pump downtime.
比較施工前後同一測點剖面，避免基準更換造成假位移。~Compare identical survey profiles before and after construction to avoid apparent displacement from changed datums.
把交接窗口中的測試與還路時間列為必要工序。~Treat testing and handback time as necessary tasks within a commissioning possession.
將路徑簡化後集中出站的人流帶入密度與速度關係。~Apply the density-speed relationship to concentrated exit flows after route simplification.''')

p(331,'分期地下捷運通車與系統界面管理~Staged underground metro openings and interface management',
'以新加坡湯申東海岸線分期通車的背景，建立營運路段與延伸工程並存的教學系統。課程要求每次延伸都重新核對定位、通訊、進路、供電和旅客路徑，並保留已營運設備和新設備之間可追溯的測試證據。~Use the staged opening of Singapore’s Thomson–East Coast Line to build a teaching system where operating sections coexist with extension works. Recheck localisation, communications, routes, power and passenger paths at every extension. Retain traceable evidence across the boundary between existing and new equipment, rather than assuming acceptance of the earlier stage automatically covers the enlarged system.',
[('2020','湯申東海岸線第一階段開始旅客服務~Thomson–East Coast Line Stage 1 began passenger service'),('2021','湯申東海岸線第二階段於八月開放營運~Thomson–East Coast Line Stage 2 opened in August'),('2022','湯申東海岸線第三階段於十一月開放營運~Thomson–East Coast Line Stage 3 opened in November')],
'https://www.lta.gov.sg/content/ltagov/en/newsroom/2021/6/news-release/TEL2_to_welcome_commuters.html','Singapore Land Transport Authority','新加坡兀蘭地鐵站周邊~Singapore Woodlands MRT station area','新加坡~Singapore',(1.437,103.786),
 'construction interlock localize communication voltage doors transfer ventilation drain redundancy',
'''把延伸線接續窗口分為隔離、施工、測試及還路。~Split the extension connection window into isolation, construction, testing and handback.
對營運端與施工端建立明確互斥進路和隔離狀態。~Establish explicit route exclusion and isolation states between operating and construction sections.
比較延伸前後定位參考表，檢查資料版本一致性。~Compare localisation reference tables before and after extension and check version consistency.
在延伸設備通訊延遲時驗證既有區段仍維持安全狀態。~Verify the existing section retains a safe state when extension-equipment communication is delayed.
將新增列車負載帶入供電回路，重新估算最遠端電壓。~Add new train loads to the supply loop and re-estimate the far-end receiving voltage.
讓新站門控與既有車輛配對測試，分開位置與鎖閉證據。~Test new station doors with existing vehicles and separate position from lock evidence.
比較新轉乘路徑開放前後的步行與等候分布。~Compare walking and waiting distributions before and after a new interchange path opens.
隨新增地下站重新界定一般通風的體積和換氣需求。~Redefine normal ventilation volume and air-change demand as underground stations are added.
檢查新舊排水區域連接是否改變泵浦停機的積水邊界。~Check whether linked drainage zones change accumulation boundaries during pump downtime.
辨認新增備援設備是否仍依賴同一機房或電源。~Identify whether added backup equipment still depends on one equipment room or supply.''',second='https://www.lta.gov.sg/content/ltagov/en/newsroom/2022/10/news-releases/thomson---east-coast-line-stage-3-to-open-for-passenger-service-.html')

p(332,'大型新建地鐵網分階段啟用與熱管理~Large new metro network staged launch and thermal management',
'以利雅德地鐵分階段投入服務為背景，建立多路線與轉乘節點同時驗收的教學案例。學徒要把高溫冷房、砂塵維護、列車循環和轉乘容量放在共同需求情境，並以各路線分別啟用的狀態表檢查服務邊界。~Use the staged launch of Riyadh Metro to construct a teaching case involving several lines and interchange nodes under acceptance. Place cooling in extreme heat, dust maintenance, fleet circulation and transfer capacity within one demand scenario. Use a state table for separately opened lines to check the service boundary instead of assuming all parts of a new network become available at the same moment.',
[('2024','利雅德地鐵第一批路線於十二月開始旅客服務~The first Riyadh Metro lines began passenger service in December'),('2025','利雅德地鐵橘線於一月加入營運服務~Riyadh Metro Orange Line joined passenger operations in January')],
'https://www.rcrc.gov.sa/en/rcrc-announces-sequential-operation-schedule-of-riyadh-metro-lines/','Royal Commission for Riyadh City','利雅德金融區車站周邊~Riyadh financial district station area','沙烏地阿拉伯~Saudi Arabia',(24.763,46.64),
 'cooling sand filter transfer platform fleet interlock communication backup availability',
'''對大型轉乘站的不同空間分別設定顯熱負載及外氣條件。~Set sensible loads and outdoor-air conditions separately for different spaces in a large interchange.
用砂塵濃度與進氣量建立維修週期中的捕集質量。~Use sand concentration and intake flow to estimate captured mass over a maintenance interval.
把濾材積塵造成的壓差與風機調速造成的壓差區分。~Distinguish filter-loading pressure drop from pressure changes caused by fan-speed control.
在多路線尚未全開時重算可用轉乘路徑和等待時間。~Recalculate available transfer paths and waiting times while some lines remain unopened.
以分階段開放的出口數檢查有效候車與通行面積。~Check effective waiting and circulation area under a staged number of open exits.
按每條線完整循環估算車數，再辨認共用備援的限制。~Estimate fleet size from each line’s complete cycle and identify limits of shared spares.
在試運轉和載客區段之間建立不可同時成立的進路。~Build mutually exclusive routes between testing and passenger-service sections.
檢查多路線資料交換的封包時效，不把收到訊息當成許可。~Check packet freshness in inter-line data exchange rather than treating receipt as permission.
把高溫下緊急照明和通訊耗電分別納入備援估算。~Include emergency lighting and communication consumption separately in hot-condition backup estimates.
用逐線停機紀錄計算可用性，避免網路平均掩蓋單線中斷。~Calculate availability from line-specific outages instead of hiding one line’s failure in a network average.''',second='https://alriyadh.gov.sa/en/new/projects/metro-alriyadh')

p(333,'海灣自動地鐵熱濕環境與活動尖峰~Gulf automated metro heat humidity and event peaks',
'以多哈地鐵為背景，建立高溫潮濕環境與活動散場旅客同時出現的教學案例。學徒從空調、濾材與供電負載追蹤到月台隊列、車門和自動行車，區分日常平均需求與短時大量到達所需的控制措施。~Use Doha Metro to construct a teaching case combining a hot humid environment with a large post-event passenger release. Trace cooling, filters and power demand into platform queues, doors and automated movement. Distinguish normal mean demand from short-duration batch arrivals, and require measurable control actions instead of treating advertised frequency as evidence that every crowd can be absorbed immediately.',
[('2019','多哈地鐵紅線南段於五月開始初期旅客服務~The southern Red Line section of Doha Metro began initial passenger service in May'),('2025','IEC 發布新版鐵道 RAMS 第一部分通用程序~IEC published the revised railway RAMS Part 1 generic process')],
'https://www.mot.gov.qa/en/news/doha-metro-red-line-south-initial-operation-open-public-wednesday','Qatar Ministry of Transport','多哈姆謝里布站周邊~Doha Msheireb station area','卡達~Qatar',(25.283,51.532),
 'cooling filter capacity queue platform doors communication isolation regen backup',
'''把顯熱模型與尚未計入的潛熱除濕需求明確分開。~Separate the sensible-heat model explicitly from latent dehumidification demand not yet included.
在高濕進氣情境下檢查濾材壓差與風量的共同變化。~Examine joint changes in filter pressure drop and airflow under humid intake conditions.
用短時散場需求比較逐列服務量，不只報告每小時容量。~Compare successive train service with a short event-release surge, not only hourly capacity.
把批次到達加入排隊紀錄，檢查平穩單服務台模型的限制。~Add batch arrivals to queue records and test the limits of a stationary single-server model.
將散場人流分配到月台不同區域，保留疏散通道。~Distribute the post-event crowd across platform zones while preserving egress routes.
在高上車需求時檢查門口阻塞與安全鎖閉確認。~Check doorway obstruction and safe lock confirmation under heavy boarding demand.
對通訊遲到的車門與列車狀態保留禁止發車條件。~Retain departure-inhibition conditions when door or train-state messages arrive late.
區分設備受潮漏電與正常回流，核對量測接點。~Distinguish moisture-related equipment leakage from normal return current and verify measurement points.
比較散場加密列車的受電重疊與可回收煞車能量。~Compare receptivity overlap and recoverable braking energy in intensified post-event service.
按乘客資訊與照明分列緊急電量，不以額定電池直接推定續航。~List emergency energy for information and lighting separately rather than inferring endurance from rated battery capacity.''')

p(334,'新建都市鐵路隧道接網與全線整合~New urban rail tunnel network integration and service transition',
'以墨爾本地鐵隧道從建設到接入營運網路的背景，建立新站、隧道及既有郊區鐵路協同運轉的教學案例。學徒把施工沉陷、試驗紀錄、進路切換及轉乘時間相連，分開首次載客與完整班表整合兩個系統狀態。~Use the Melbourne Metro Tunnel’s transition from construction to network operation to construct a teaching case joining new stations and tunnels to suburban railways. Link construction movement, test records, route switching and transfer time. Treat the first passenger opening and full timetable integration as distinct system states with different acceptance and operating evidence.',
[('2015','墨爾本地鐵隧道展開早期現地調查工作~Early site investigations for Melbourne Metro Tunnel began'),('2025','墨爾本地鐵隧道於十一月開放旅客服務~Melbourne Metro Tunnel opened to passengers in November'),('2026','二月班表轉換將地鐵隧道整合進完整營運~The February timetable change integrated Metro Tunnel into full operations')],
'https://bigbuild.vic.gov.au/projects/metro-tunnel/about/overview','Victoria Big Build','墨爾本州立圖書館站周邊~Melbourne State Library station area','澳洲~Australia',(-37.809,144.963),
 'construction survey settlement grout interlock localize brakecurve transfer ventilation availability',
'''把接網施工窗口與全線班表轉換視為不同的交接事件。~Treat the connection possession and the complete timetable transition as separate handover events.
以固定外部基準重複測量，區分儀器誤差和真實位移。~Repeat surveys against a fixed external datum to separate instrument error from real movement.
對街區及既有鐵路分別畫出沉陷剖面和坡折尺度。~Plot settlement profiles and kink length scales separately for city blocks and existing tracks.
以假想隧道環隙驗算注漿體積，保留超灌和漏失項。~Check injected volume against a hypothetical tunnel annulus and retain excess and loss terms.
對新隧道與既有線進路切換建立互鎖狀態和拒絕條件。~Construct interlocking states and refusal conditions for route switching between new tunnel and existing lines.
在資料更新前後檢查列車位置參考和版本一致性。~Check train-position references and version consistency before and after data updates.
將接續區段的目標速度和定位誤差帶入保護距離。~Include target speed and localisation uncertainty in protective distance at the connecting section.
比較新站開放前後的旅客步行與垂直轉乘路徑。~Compare walking and vertical-transfer paths before and after the new stations open.
分開一般換氣與隧道活塞風的量測邊界，避免重複計量。~Separate normal-ventilation and piston-airflow measurement boundaries to avoid double counting.
將初期載客與完整班表的故障暴露時間分別統計。~Calculate failure exposure separately for initial passenger service and the complete timetable.''',second='https://bigbuild.vic.gov.au/use-metro-tunnel/faq')
