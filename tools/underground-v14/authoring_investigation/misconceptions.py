"""Authored unit-specific quiz distractors; deliberately false engineering beliefs."""
DATA={}
def add(cid,text):
 DATA[cid]=text.strip().splitlines()
 assert len(DATA[cid])==10,cid
add('b127',r'''
反射振幅只由岩石名稱決定，與密度及波速無關。~Reflection amplitude depends only on rock names, regardless of density and velocity.
反射走時乘波速就是距離，不必考慮去程回程。~Multiplying reflection travel time by velocity gives distance without accounting for the return path.
把顯示像素縮小就能提高地下薄層的實際分辨率。~Smaller display pixels increase the actual resolution of thin underground layers.
取樣後再提高插值點數即可完全修復時間混疊。~Adding interpolation points after acquisition completely repairs temporal aliasing.
任何雜訊都會按疊加筆數的平方根規則消失。~Every kind of noise decreases according to the square-root stacking rule.
側壁量到的所有反射都必定來自掌子面正前方。~All reflections measured at a sidewall must originate directly ahead of the face.
波速推得的動態模數可以直接代表長期靜態變形。~A velocity-derived dynamic modulus directly represents long-term static deformation.
只要遠處振幅較小就能證明前方存在含水破碎帶。~A smaller distant amplitude proves a water-bearing fractured zone lies ahead.
走時拾取非常準確時，就可以忽略波速模型誤差。~Very precise arrival picking makes velocity-model uncertainty irrelevant to location.
只統計成功預警案例就能完整評估探測可靠度。~Counting successful warning examples alone fully evaluates prediction reliability.
''')
add('b128',r'''
岩心缺失的深度可以任意放在該回次最底部。~Missing core may always be assigned arbitrarily to the bottom of a run.
岩心回收率很高就代表岩石品質指標必定很高。~High total core recovery necessarily means a high rock quality designation.
不同方向鑽孔的表觀節理間距可以不修正直接比較。~Apparent joint spacing from differently oriented holes can be compared without correction.
洗乾淨的節理岩壁足以代表原位含填料剪切行為。~Cleaned joint walls adequately represent the original infilled joint's shear behavior.
完整岩心抗壓強度就是含節理岩體的設計強度。~Intact-core compressive strength is the design strength of the jointed rock mass.
岩體分類總分相同，就表示它們具有相同破壞機制。~Equal rock-mass classification totals imply identical governing failure mechanisms.
乘法岩體指標中的地下水因子永遠不會隨施工改變。~The water factor in a multiplicative rock index never changes during construction.
岩心與隧道的尺寸比可直接當成強度折減係數。~The core-to-tunnel size ratio directly supplies the required strength-reduction factor.
兩位記錄者有分歧時，把總分平均就能消除偏差。~Averaging two disagreeing loggers' total scores removes the underlying bias.
折減整體模數後再加同一節理弱化不會重複計算。~Reducing bulk stiffness and adding the same joint weakening cannot double-count damage.
''')
add('b129',r'''
孔壁影像看不清楚的區段可以直接記為沒有裂隙。~Unreadable borehole-wall intervals can be logged directly as having no fractures.
展開圖的峰谷總高度就是正弦半振幅。~The total peak-to-trough image height is the sinusoidal half-amplitude.
掃描時間間隔固定就保證垂直像素的深度間距固定。~A fixed scan-time interval guarantees constant vertical pixel spacing in depth.
影像正北標記必定等於地理北，鋼套管不會影響。~Image north always equals geographic north and is unaffected by steel casing.
孔壁橢圓化一定由原位應力造成，不可能是鑽進效應。~Borehole ovality always comes from in-situ stress rather than drilling effects.
影像暗帶寬度可直接當成裂隙的水力開度。~The width of a dark image band directly equals hydraulic fracture aperture.
每一種節理方向被單一鑽孔取樣的機率都相同。~A single borehole samples every joint orientation with equal probability.
看起來最寬的裂隙必定是導水能力最大的裂隙。~The widest-looking fracture necessarily has the greatest hydraulic conductivity.
使用調整過模型參數的同批影像也算獨立驗證。~Images already used to tune the model also count as independent validation.
只保存彩色三維模型就足以重新校正全部裂隙方位。~Saving only the colored three-dimensional model permits recalibration of all fracture orientations.
''')
add('b130',r'''
隧道海拔乘岩石重度就是上覆岩體垂直應力。~Tunnel altitude multiplied by rock unit weight gives vertical overburden stress.
只要主應力量值正確，坐標軸和剪應力符號就不重要。~Correct principal magnitudes make coordinate axes and shear signs unimportant.
所有岩石都必須用等於一的係數扣除孔隙水壓。~Every rock must use a coefficient of exactly one when subtracting pore pressure.
套鑽量到的所有應變都只能來自原始應力釋放。~All strain measured during overcoring must arise solely from original stress relief.
泵浦停止後的第一個壓力尖峰就是裂縫閉合壓力。~The first pressure spike after pump shutdown is the fracture closure pressure.
任何單側孔壁剝落都能直接判定最大主應力方向。~Any one-sided borehole spalling directly establishes the maximum principal-stress direction.
層理岩的不同方向模數可以任意交換而不影響反演。~Directional moduli in bedded rock can be interchanged without affecting inversion.
洞壁附近的應力量測必定就是未擾動遠場應力。~A measurement near the tunnel wall necessarily represents undisturbed far-field stress.
反演殘差很小就證明不存在共同感測器偏差。~Small inversion residuals prove that common sensor bias is absent.
不同深度的應力只要取平均就可代表整個場址。~Averaging stress measurements at different depths adequately represents the entire site.
''')
add('b131',r'''
兩點擬合的線性摩擦包絡可以外推到任何法向應力。~A linear friction envelope fitted to two points applies at any normal stress.
外加法向荷重除面積就是含水節理的有效法向應力。~Applied normal load divided by area equals effective stress on a wet joint.
定法向力與定法向剛度試驗必定得到同樣的曲線。~Constant-normal-load and constant-normal-stiffness tests necessarily produce the same curve.
只用單側位移計就能完全排除試件轉動造成的假剪脹。~One displacement gauge on one side completely excludes rocking-induced false dilation.
試驗曲線的最後一點必定已代表真正殘餘強度。~The final point of any test curve necessarily represents true residual strength.
剪切位移增加時，應力仍應永遠除以最初重疊面積。~Shear stress should always use initial overlap area as displacement increases.
只要試驗速度很慢，就不必再檢查孔壓和排水。~A sufficiently slow test never needs pore-pressure or drainage checks.
一條高解析表面剖面足以代表所有方向和尺度的粗糙度。~One high-resolution profile represents roughness in every direction and at every scale.
力計精度就是整個節理抗剪應力試驗的不確定度。~Load-cell accuracy equals the complete uncertainty of a joint shear-stress test.
剪切曲線下面積全部是目標節理轉成熱的摩擦能。~All area under the shear curve is frictional heat generated at the intended joint.
''')
add('b132',r'''
量到沉陷槽中央最大值就能唯一決定槽的寬度。~The maximum centerline settlement uniquely determines the trough width.
地表體積損失百分比就是直接量得的超挖土量百分比。~Surface volume-loss percentage is a directly measured overexcavation percentage.
水準網閉合差很小，就證明所有基準點絕對穩定。~A small leveling closure proves absolute stability of every benchmark.
建物總沉陷最大時，一定也承受最大的彎曲損傷。~The building with the largest total settlement necessarily suffers the most bending damage.
任何時間窗算出的平均沉陷速率都有相同工程意義。~Average settlement rates from any time window have the same engineering meaning.
儀器顯示到十分之一毫米就具有同等實際準確度。~An instrument displaying tenths of a millimetre has the same actual accuracy.
水位下降時總應力永遠不變，可以無條件使用水頭換算。~Total stress never changes during drawdown, so head conversion applies unconditionally.
每個監測點的變形只能由距離最近的掌子面造成。~Movement at a monitoring point can only be caused by the nearest face.
大部分監測點正常就能取消少數敏感建物的超限警報。~Normal readings at most points justify canceling an exceedance at a sensitive building.
掌子面通過後就可以立刻認定延時沉陷已經結束。~Face passage immediately establishes that all delayed settlement has ended.
''')
add('b133',r'''
兩點間弦長不變就證明兩個測點都沒有移動。~An unchanged chord proves that neither of its endpoints has moved.
較晚安裝的測點記錄較小收斂，就表示該斷面更穩定。~Smaller convergence at a later-installed section proves that section is more stable.
全測站角度精度固定，所以位置誤差與觀測距離無關。~Fixed total-station angular precision makes positional error independent of sight distance.
鋼尺讀值變化只能是圍岩變形，不會受溫度和張力影響。~A steel-tape reading changes only with ground movement, never temperature or tension.
所有測點共同位移時，一定可以全部扣除當作基準漂移。~Common movement of all targets can always be subtracted as reference drift.
收斂對時間增加必定代表潛變，與掌子面推進無關。~Increasing convergence with time necessarily indicates creep unrelated to face advance.
支護剛度乘位移可在有空隙未接觸時直接算出反力。~Support stiffness times movement directly gives reaction even before a gap closes.
把斷面最佳擬合成圓就能保留全部橢圓化資訊。~Fitting the section to a best-fit circle preserves all ovalization information.
自動監測有持續更新的畫面就代表資料必定是最新值。~A continuously updating automated display necessarily contains fresh measurements.
兩個模型同樣吻合收斂曲線，就表示其力學機制相同。~Two models fitting convergence equally well necessarily use the same physical mechanism.
''')
add('b134',r'''
增加輸出點雲數量可以創造原始照片沒有的細節。~Increasing output point count creates detail absent from the original photographs.
所有照片在同一位置拍得越多，深度精度就一定越高。~Taking more photographs from one position necessarily improves depth accuracy.
重投影誤差很低就保證鏡頭畸變和物面曲率已正確分離。~Low reprojection error guarantees correct separation of lens distortion and surface curvature.
一根比例尺就足以完全控制整個模型的三維形狀。~One scale bar fully constrains the entire model's three-dimensional shape.
濕壁上的反光亮點在所有視角都可以當固定紋理。~Wet-wall highlights can be treated as fixed texture in every viewing direction.
自動補成封閉網格就代表所有背面都已實際觀測。~Automatic mesh closure means every hidden back surface has actually been observed.
控制點也可以同時當作獨立精度檢核點。~Control points can simultaneously serve as independent accuracy checkpoints.
跨越兩個節理面擬合的平均平面就是現場的真實節理。~The average plane fitted across two joints is a real joint surface in the ground.
把兩期全部點雲最佳配準就不會消除任何真實位移。~Best-fitting all points across two epochs cannot remove genuine movement.
彩色模型看起來逼真，就足以代替原始照片與坐標紀錄。~A realistic colored model adequately replaces original photographs and coordinate records.
''')
add('b135',r'''
不排水強度和排水摩擦角可不分條件地混在同一模型。~Undrained strength and drained friction can be mixed unconditionally in one model.
一個底部壓力計正常就代表整個掌子面支護都足夠。~A normal invert pressure reading proves adequate support over the entire face.
支護壓力越高越安全，不必考慮淺覆土上舉。~Higher support pressure is always safer without considering shallow-cover uplift.
某工程的臨界穩定指標可以不看幾何直接搬到另一工程。~A critical stability index transfers between projects without considering geometry.
只要土倉壓力正常，就可假設泥膜永遠完整不透水。~Normal chamber pressure permits assuming an eternally intact impermeable filter cake.
濕出土重量增加就必定代表原位土被過量開挖。~Greater wet discharge mass necessarily means excessive excavation of in-situ soil.
停止推進後土倉壓力和改良土性質會永遠保持不變。~Chamber pressure and conditioned-soil properties remain unchanged forever after advance stops.
高透水砂只占小面積，就一定只造成同等比例風險。~A small permeable sand area necessarily contributes only that proportional share of risk.
敏感度分析算出的百分比就是實際失敗機率。~A percentage from sensitivity analysis is the actual probability of failure.
多數訊號正常時可以直接刪除少數異常當作離群值。~When most signals are normal, the remaining anomalies may simply be deleted as outliers.
''')
add('b136',r'''
改良土越稀越容易流動，就一定越有利於穩定支護。~More fluid conditioned soil is necessarily better for stable face support.
乾基含水率與水占濕土重量比例永遠可以互換。~Dry-basis moisture content and water fraction of wet mass are always interchangeable.
常壓泡沫體積就是進入加壓土倉後的有效氣體體積。~Atmospheric foam volume equals its effective gas volume inside the pressurized chamber.
細料百分比相同的土一定具有相同塑性和改良需求。~Soils with equal fines content necessarily have equal plasticity and conditioning needs.
單一剪切速率的黏度足以代表停放和重啟流變行為。~Viscosity at one shear rate fully represents rest and restart rheology.
刀盤功率降低就能證明改良成功，不必看進尺和地質。~Lower cutterhead power proves successful conditioning without checking advance or geology.
添加總量達標就證明各區材料分布一定均勻。~Meeting the total addition quantity proves uniform distribution throughout the chamber.
試驗流量測不到就證明改良土真正完全不透水。~Undetectable test flow proves that conditioned soil has exactly zero permeability.
材料短時試驗合格就保證任何溫度和停放時間都相容。~Passing a short trial guarantees compatibility at every temperature and storage duration.
只保留最成功配比試驗就足以說明改良方案適用範圍。~Retaining only the most successful trial fully describes the conditioning scheme's applicability.
''')
add('b137',r'''
送回流量瞬時差就是地層流入量，不必考慮槽位儲存。~The instantaneous supply-return difference equals ground inflow regardless of tank storage.
單一管段平均速度正常就保證所有彎頭都不會沉積。~Normal mean velocity in one pipe guarantees no deposition in any bend.
馬達額定功率就是實際可用的液壓輸送功率。~Rated motor power equals the hydraulic power actually available for transport.
泥水的固體體積百分比就是固體質量百分比。~The solids volume percentage in slurry equals its solids mass percentage.
旋流器總回收率就是每個粒徑完全相同的分離率。~Overall cyclone recovery equals the separation efficiency at every particle size.
槽體幾何容積永遠等於沒有沉積影響的有效緩衝容積。~Geometric tank volume always equals effective buffering volume regardless of deposits.
不論流速改變多慢，都會產生同一個瞬時水擊壓峰。~A velocity change produces the same instantaneous water-hammer peak however slowly it occurs.
管壁平均厚度正常就證明每個局部位置都足夠厚。~Normal mean pipe thickness proves adequate thickness at every local position.
兩台泵即使共用電源，也能當作完全獨立的備援。~Two pumps remain completely independent backups even with a shared power supply.
每班平均報表足以取代所有原始流量與壓力時間序列。~Shift-average reports adequately replace all original flow and pressure time series.
''')
add('b138',r'''
多道密封即使共用失效供應，也能直接按獨立機率相乘。~Multiple seals sharing a failed supply still justify multiplying independent failure probabilities.
盾尾平均間隙正常就保證整圈刷毛接觸都正常。~Normal mean tail clearance guarantees adequate brush contact around the entire circumference.
供應端壓力很高就證明材料已經到達每道刷列。~High supply-end pressure proves material has reached every brush row.
密封材料消耗越大就代表實際阻水性能必定越好。~Higher seal-medium consumption necessarily means better actual water resistance.
常溫黏度較高的材料在所有工況都一定較適合密封。~Higher ambient viscosity necessarily makes a material the better seal under every condition.
環片外表面缺陷很小就不可能損傷多道盾尾刷列。~A small segment exterior defect cannot damage multiple tail-brush rows.
灌漿和密封各自儀表正常就不必檢查彼此介面。~Normal separate grout and seal readings eliminate the need to examine their interface.
排水泵總量可以全部直接歸因於盾尾密封漏水。~All sump-pump discharge can be attributed directly to tail-seal leakage.
停機前不漏水就保證任何停留時間後仍有相同性能。~No leakage before stopping guarantees identical performance after any standstill duration.
監測資料覆蓋比例高，就可以忽略相鄰缺測區的風險。~High overall monitoring coverage permits ignoring risk in adjacent unmeasured zones.
''')
add('b139',r'''
所有刀位轉數相同時，接觸行程和磨耗需求也完全相同。~Equal revolutions give identical contact travel and wear demand at every cutter position.
每轉進尺越大就必定代表切削效率和刀具壽命越好。~Greater penetration per revolution necessarily improves cutting efficiency and cutter life.
總推力除刀具數就能得到每顆刀實際承受的峰值荷重。~Total thrust divided by cutter count gives each cutter's actual peak load.
旋轉比能增加只能由岩石變硬造成，與排碴無關。~Higher rotational specific energy can only come from harder rock, never muck removal.
前一岩層的平均磨耗率可以無條件預測下一岩層壽命。~The previous stratum's mean wear rate predicts life in the next stratum unconditionally.
刀環剩餘直徑足夠就證明軸承和轉動狀態也正常。~Adequate remaining ring diameter proves that bearings and rotation are also healthy.
班平均扭矩正常就表示沒有局部刀具衝擊疲勞。~Normal shift-average torque means no localized cutter impact fatigue is occurring.
相同刀間距貫入比在所有岩性都會有同樣最佳切削效果。~The same spacing-penetration ratio gives identical optimum cutting in every rock type.
只更換刀環就可以把未更換軸承的累積使用時間歸零。~Replacing only the ring resets accumulated service time of the unchanged bearing.
刀具平均磨耗很低就能排除任何單刀卡死風險。~Low average cutter wear excludes any possibility of one seized cutter.
''')
add('b140',r'''
永久成環荷載合格就代表運輸和吊運階段必定合格。~Adequate permanent-ring capacity necessarily proves adequate transport and handling performance.
少量試塊平均強度就是整批環片的特徵設計強度。~The mean of a few specimens is the characteristic design strength of the whole batch.
纖維添加重量相同就一定產生相同方向的殘餘拉力。~Equal fibre dosage necessarily produces equal residual tensile resistance in every direction.
同向尺寸偏差可以和獨立隨機誤差一樣平方根加總。~Same-direction dimensional biases can be combined like independent random errors by root-sum-square.
早齡抗壓強度高就代表不會發生溫差收縮裂縫。~High early compressive strength guarantees absence of thermal shrinkage cracking.
同一環片的吊運支點移動不會改變暫態彎矩。~Moving handling support points cannot change transient bending in the same segment.
千斤頂總推力除總接觸面積足以排除所有局部劈裂。~Total jack force divided by total contact area excludes all local splitting.
熱擴散尺度就是實際爆裂深度和必需耐火厚度。~Thermal diffusion scale equals actual spalling depth and required fire-protection thickness.
完好混凝土擴散係數可以完整代表貫穿裂縫的傳輸。~An intact-concrete diffusion coefficient fully represents transport through a through-crack.
掃碼成功就代表環片資料內容已完成工程品質審查。~A successful barcode scan means the segment records have passed engineering quality review.
''')
add('b141',r'''
只量止水墊原始高度就能知道安裝後的實際壓縮率。~Original gasket height alone determines its actual installed compression ratio.
短時間不漏水就保證所有老化和變形情境都合格。~Brief absence of leakage proves adequacy under every aging and deformation scenario.
縫寬和錯台分別合格就代表任何組合都一定水密。~Separate gap and offset compliance guarantees watertightness for every combination.
止水墊反力越大越好，不必檢查混凝土溝槽劈裂。~Greater gasket reaction is always better without checking concrete groove splitting.
橡膠外觀沒有裂紋就證明接觸力沒有長期鬆弛。~An uncracked rubber appearance proves that contact force has not relaxed over time.
直線墊條試驗合格就可以省略全部角部交會試驗。~Passing straight-strip tests makes all corner-intersection testing unnecessary.
止水墊黏貼固定良好就可以不考慮最終接縫壓縮。~Secure gasket bonding eliminates the need to consider final joint compression.
夾雜硬顆粒時增加閉合力必定能恢復完整止水。~Increasing closure force always restores complete sealing when hard debris is trapped.
共同模具偏差可當作彼此獨立的小誤差互相抵消。~Shared mould biases can be treated as independent small errors that cancel each other.
產品通過證書可以取代現地接縫幾何和批次追溯。~A product pass certificate replaces field joint geometry and batch traceability.
''')
add('b142',r'''
接縫軸力不大時就不必考慮偏心彎矩與局部接觸。~Modest joint axial force eliminates the need to consider eccentric bending and local contact.
偏心超出核心就表示混凝土已必然立即破壞。~Eccentricity outside the kern necessarily means immediate concrete failure has already occurred.
螺栓扭矩相同就保證實際預力相同，不受摩擦影響。~Equal bolt torque guarantees equal preload regardless of friction conditions.
接縫初始轉動剛度可以直接套用到任何大轉角。~Initial joint rotational stiffness applies directly at any large rotation.
接縫中心平均縫寬就是止水線實際承受的最大張開。~Mean gap at the joint center equals maximum actual opening at the sealing line.
只要環片錯縫排列就可以把多環當成完全黏結整體。~Staggering segments permits modeling multiple rings as a perfectly bonded monolithic structure.
疲勞循環次數足夠多就能不看幅值直接決定剩餘壽命。~A large cycle count determines remaining fatigue life without considering amplitudes.
外露螺栓完好就代表其周邊混凝土錨定也一定完好。~An intact exposed bolt guarantees intact anchorage in its surrounding concrete.
足尺接縫試驗不需要扣除設備柔度與支座就位效應。~Full-scale joint tests never require correction for frame compliance or seating effects.
結構和水密報告各自通過就無須統一張開幾何定義。~Separate structural and sealing approvals eliminate the need for a common opening definition.
''')
add('b143',r'''
注入量達理論環隙體積就證明頂部不可能留下空洞。~Delivering the theoretical annular volume proves that no crown void can remain.
泵浦計量總量就是全部有效進入目標環隙的材料量。~The total metered pump quantity all effectively enters the intended annulus.
泵端壓力可以不修正高程與管損直接當環片外壓。~Pump-end pressure directly equals lining pressure without elevation or line-loss correction.
流動度合格就可以不再檢查漿體泌水或材料分離。~Passing a flow test removes any need to inspect bleeding or segregation.
平均管線停留短就保證所有死區材料都尚未老化。~A short mean line residence guarantees that material in every dead zone remains fresh.
計算環片浮力時應使用混凝土材料體積作排開漿體體積。~Concrete material volume should be used as displaced grout volume when calculating ring buoyancy.
最終硬化模數可直接代表剛注入時漿體的支承剛度。~Final hardened modulus directly represents support stiffness immediately after injection.
自由試樣收縮百分比必定等於現場環隙的空洞率。~Free specimen shrinkage percentage necessarily equals field annular void ratio.
非破壞檢測圖上的每一個反射異常都必定是空洞。~Every reflection anomaly on a nondestructive survey necessarily represents a void.
整班平均填充比正常就可以省略個別環異常處置。~A normal shift-average fill ratio permits waiving individual ring anomaly resolution.
''')
add('b144',r'''
最終止水屏障完整就代表過渡階段絕不會出現空檔。~Complete final sealing barriers guarantee no gap during intermediate transitions.
井深就是所有含水層作用於井口的實際壓力水頭。~Shaft depth equals the actual pressure head from every aquifer at the opening.
少數高強度處理體試件可以排除所有貫通薄弱通道。~A few strong treated-ground specimens exclude every connected weak pathway.
處理體總厚度永遠就是地下水能走過的最短路徑。~The full treated-block thickness always equals the shortest possible groundwater path.
平均止水環壓縮正常就能排除偏心造成的局部失去接觸。~Normal mean sealing-ring compression excludes local loss of contact from eccentricity.
機器中心點對準就不需要再檢查俯仰偏航和穿越長度。~A correctly positioned machine center removes the need to check pitch, yaw and crossing length.
總反力除支點數就是每個實際支點的真實受力。~Total reaction divided by support count equals the actual force at every support.
井內沒有看見漏水就證明地層不可能向其他空間流失。~No visible shaft leakage proves that ground cannot be flowing into other spaces.
資料傳輸延遲就是地層可以安全等待處置的時間。~Data transmission latency is the time the ground can safely wait for intervention.
始發到達成功就代表拆除臨時密封後永久止水也已合格。~Successful launch or reception proves permanent sealing after temporary barriers are removed.
''')
add('b145',r'''
坐標原點重合就保證整條長隧道的尺度與旋轉都正確。~Coincident coordinate origins guarantee correct scale and rotation along the entire long tunnel.
每一測段的角度誤差必定獨立而且可以互相抵消。~Angular errors in every survey segment are necessarily independent and cancel each other.
陀螺方向是自動真值，不需再校準或考慮溫度漂移。~Gyro orientation is automatic truth needing no calibration or thermal-drift consideration.
從目標點算刀盤中心只需平移，不必考慮機身旋轉。~Transforming a target to cutterhead center requires translation only, without machine rotation.
平面里程和斜距可以不加說明直接用在同一環號表。~Horizontal chainage and slope distance can be interchanged within one ring table without explanation.
只要能回到設計中心線，就不必檢查組環曲率與止水限制。~Returning to the design centerline removes the need to check ring curvature and seal limits.
刀盤在設計線上就代表盾尾與已安裝環片必定同心。~A cutterhead on the design alignment guarantees concentric shield tail and installed rings.
把受折射影響的讀值平滑後就能恢復真實機器姿態。~Smoothing refracted observations restores the true machine attitude automatically.
兩個共用錯誤基準的感測器融合後可以消除共同偏差。~Fusing two sensors sharing an incorrect datum eliminates their common bias.
事後強制閉合差歸零，就不需要再保存原始貫通誤差。~Forcing closure to zero afterward removes any need to retain the original breakthrough discrepancy.
''')
