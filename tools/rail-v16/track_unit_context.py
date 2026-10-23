"""Authored per-unit model bounds and measurement chains, never course-wide defaults."""
BOUNDS={}; MEASURES={}
def U(text):
 for line in text.strip().splitlines():
  title,boundary,measure=line.split('|');BOUNDS[title.strip()]=boundary.strip();MEASURES[title.strip()]=measure.strip()
U('''
列車單向運能 | 固定每列有效載重與發車率，不含尖峰到達或空車需求~Fixed useful payload and departure rate, excluding peak arrivals and empty returns | 站場發車時間戳與貨物秤重帳~yard departure timestamps and cargo weighing records
坡道牽引分力 | 全列車處於同一小坡度，只計重力沿軌分量~The whole consist occupies one small gradient; only longitudinal gravity is included | 合成坡度圖與逐車質量清單~synthetic gradient profile and wagon mass list
速度與牽引功率 | 輪周力與速度同時取得，只計機械功率~Wheel force and speed are simultaneous; only mechanical power is counted | 模擬輪周力與同步速度訊號~simulated wheel force and synchronous speed signal
貨列制動距離 | 延遲時等速，其後固定減速度，不含坡度與黏著變化~Constant speed during delay followed by constant deceleration, without gradient or adhesion variation | 合成制動命令、速度及減速度時間序列~synthetic brake-command, speed and deceleration traces
貨物外廓餘量 | 同一垂向基準的標量包絡，不含側向外廓和不確定度餘量~Scalar vertical envelopes on one datum, excluding lateral envelopes and uncertainty reserve | 貨物輪廓掃描與動態外廓樣本~cargo-profile scans and dynamic-envelope samples
閉塞占用時間 | 固定速度、已知列車長度及固定解鎖裕量~Fixed speed, known train length and fixed release allowance | 合成車頭車尾通過時間戳~synthetic front and rear passage timestamps
滾動阻力能量 | 固定阻力沿指定距離作功，不含加速或坡度能量~Constant resistance over a stated distance, excluding acceleration and gradient energy | 模型牽引力計與里程積分紀錄~model force gauge and distance integration record
港區停留庫存 | 穩態平均到達率且無持續積累，不預測尖峰隊長~Steady mean arrival rate without growing inventory; peak queues are not predicted | 進出站場事件紀錄與在場盤點~yard entry-exit event records and inventory counts
列車噪音能量比較 | 各事件聲暴露相同且能量相加，不含不同列車差異~Equal sound exposure per event with additive energy, excluding differences among trains | 固定位置聲暴露計與事件計數~fixed-position sound-exposure meter and event counter
隧道換氣量級 | 有效斷面上的均勻平均風速，不含暫態活塞效應~Uniform mean velocity across effective area, excluding transient piston effects | 多點風速計與斷面量測~multi-point anemometers and section measurements
圓曲線向心加速 | 等速圓周運動且半徑固定，不含超高補償~Uniform circular motion at fixed radius, without cant compensation | 合成速度計與路線曲率資料~synthetic speed sensor and alignment curvature data
曲線外矢估算 | 弦長遠小於半徑的小弦近似~Short-chord approximation with chord length much smaller than radius | 固定弦長直尺與中點偏距計~fixed-chord straightedge and midpoint displacement gauge
緩和曲線曲率率 | 曲率沿緩和長度線性變化~Curvature varies linearly along transition length | 共同里程的曲率樣本與基線~curvature samples and baseline on common chainage
橫向加加速度 | 克羅梭曲線與固定速度，不含超高或車體滾動~Clothoid at constant speed, excluding cant and body roll | 合成橫向加速度序列與時間基準~synthetic lateral-acceleration trace and timebase
縱坡高程增量 | 固定小坡度且長度為水平距離~Constant small gradient with horizontal distance | 水準尺與水平距離資料~levelling staff and horizontal-distance data
豎曲線加速度 | 等速圓形豎曲線，只計幾何加速度幅值~Constant-speed circular vertical curve; geometric acceleration magnitude only | 合成垂向加速度計與豎曲率~synthetic vertical accelerometer and vertical curvature
坡度接續長度 | 小坡度圓形豎曲線近似~Small-gradient circular vertical-curve approximation | 兩端縱坡與里程表~endpoint grades and chainage table
平面偏角累積 | 固定半徑圓弧的弧長定義~Arc-length definition for a constant-radius circular arc | 全站儀切線方向與里程~total-station tangent directions and chainage
里程誤差投影 | 局部坡度固定的第一階誤差投影~First-order error projection at fixed local gradient | 同步里程標記與水準觀測~synchronized chainage markers and level observations
設計容差合成 | 兩個零均值獨立正交誤差，不含共同偏差~Two zero-mean independent orthogonal errors, excluding shared bias | 獨立控制網閉合觀測~independent survey-network closure observations
平衡超高計算 | 小傾角剛體平衡且使用指定有效軌距~Small-angle rigid-body balance using the stated effective gauge | 超高尺、半徑與同步速度紀錄~cant level, radius and synchronized speed record
超高不足辨認 | 平衡超高與實際超高採同一有效軌距~Equilibrium and actual cant use the same effective gauge | 同里程速度群與超高剖面~speed groups and cant profiles at matching chainage
超高過剩辨認 | 低速平衡超高已獨立算得，不含車體懸吊~Low-speed equilibrium cant is independently calculated; suspension is excluded | 低速通過紀錄與超高尺~low-speed passage records and cant level
未平衡橫向加速 | 小傾角近似且超高不足以公尺輸入~Small-angle approximation with cant deficiency in metres | 軌面座標橫向加速度計~lateral accelerometer in track-plane coordinates
超高順坡梯度 | 線性超高順坡，不含局部階躍~Linear cant ramp without local steps | 等距雙軌水準量測~equally spaced level measurements of both rails
超高變化時間率 | 固定速度通過線性超高順坡~Constant speed through a linear cant ramp | 速度計與同步雙軌高程~speed sensor and synchronized rail levels
不足變化時間率 | 不足量沿里程線性改變且車速固定~Deficiency changes linearly with distance at fixed speed | 共里程曲率超高與速度資料~curvature, cant and speed on common chainage
平衡速度反算 | 小傾角靜力平衡，不是允許營運速度~Small-angle static balance, not an allowed operating speed | 半徑量測與實測超高~radius measurement and measured cant
混合列車均方速度 | 兩群速度固定且權重相加為一~Two fixed speed groups with weights summing to one | 車次計數與分群速度紀錄~train counts and grouped speed records
超高量測不確定度 | 左右軌誤差獨立，未納入共同零點偏差~Independent rail errors, excluding common zero bias | 左右交換的水準尺讀值~levelling readings with left-right reversal
底座平均承壓 | 已知有效承壓面積且只求平均值~Known effective bearing area; mean pressure only | 模型荷重元與接觸印跡~model load cell and contact imprint
底座幾何方量 | 等斷面長方體，未扣預埋件及凹槽~Prismatic rectangular volume before deducting embedded objects and recesses | 長寬厚度量測與方量帳~length, width and thickness measurements with a volume ledger
均勻溫降收縮 | 均勻降溫且無機械約束~Uniform cooling without mechanical restraint | 底座內埋溫度計與端部位移~embedded slab thermometers and endpoint movement
約束熱應力量級 | 常數彈模與假定約束係數，不含徐變開裂~Constant modulus and assumed restraint factor, excluding creep and cracking | 溫度補償應變計與多點溫度~temperature-compensated strain gauges and multiple temperatures
乾縮位移估算 | 已給定均勻乾縮應變且無約束~Given uniform drying strain without restraint | 同溫長度比較儀與含水紀錄~constant-temperature length comparator and moisture records
養護顯熱預算 | 常數比熱與均勻溫變，不含水化熱~Constant heat capacity and uniform temperature change, excluding hydration heat | 核心表面溫度與材料質量~core-surface temperatures and material mass
排水橫坡高差 | 平面橫坡，不含局部窪地~Planar crossfall excluding local depressions | 網格水準點與排水低點圖~gridded level points and drainage low-point map
基礎壓縮變形 | 集中線性支承，不含塑性壓密~Lumped linear support excluding plastic compaction | 模型荷重元與位移計~model load cell and displacement gauge
高程修整餘量 | 三個量使用同一方向與基準~Three quantities share one direction and datum | 竣工水準表與沉陷監測~as-built level table and settlement monitoring
試件平均強度 | 三個等權試件平均，不是特徵強度~Equal-weight mean of three specimens, not characteristic strength | 試驗機荷重與試件尺寸~test-machine load and specimen dimensions
平移偏差合成 | 二維歐氏距離，不包含座標基準誤差~Two-dimensional Euclidean distance excluding datum error | 同基準全站儀座標~total-station coordinates on one datum
板端偏轉估算 | 小角度剛體偏轉，不含板體彎曲~Small-angle rigid yaw excluding slab bending | 板前後棱鏡橫向座標~lateral coordinates of front and rear slab prisms
板體俯仰估算 | 已扣設計縱坡的小角度俯仰~Small-angle pitch after subtracting design gradient | 板兩端水準與設計高程~endpoint levelling and design elevations
調整螺距位移 | 理想螺距且無間隙或受力回彈~Ideal thread pitch without backlash or elastic recovery | 螺桿角度標記與位移計~screw-angle marks and displacement gauge
測站角度投影 | 小角度橫向投影，不含距離誤差~Small-angle transverse projection excluding range error | 全站儀角度與視距~total-station angle and sight distance
棱鏡常數偏差 | 單一固定量距偏差，符號按校正定義~One fixed range bias with sign defined by calibration | 基線量測與棱鏡互換~baseline measurement and prism interchange
水準閉合分配 | 已排除粗差後按路線長度分配~Length-weighted allocation after excluding blunders | 往返水準閉合與分段距離~forward-back levelling closure and segment distances
三點高程平均 | 等權獨立觀測，不含共同系統偏差~Equal-weight independent observations without shared bias | 三個獨立板面高程點~three independent slab elevation points
相鄰板接縫差 | 共同基準上的兩個接縫端點~Two joint endpoints on one common datum | 同次水準測量的接縫兩側讀值~readings on both sides of the joint in one levelling run
重測平均不確定度 | 獨立同分布隨機誤差，無自相關~Independent identically distributed random errors without autocorrelation | 不同測站重測結果~repeat observations from independent stations
''')
