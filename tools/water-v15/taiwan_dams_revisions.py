# Unit-specific physics extensions; independent of failure, verification and practice text.
EXTRA={
'b215':[
'融雪產流還受積雪含水量與土壤暫存控制，同一氣溫未必產生同一入流；庫內水量平衡只核算已到達的水。~Snow water equivalent and temporary soil storage also control melt runoff. Identical air temperatures need not produce identical inflows; this reservoir balance accounts only for water that has already arrived.',
'薄膜模型的壓力乘半徑是每單位高度的環向內力，再除厚度才成為平均應力；這兩個量的單位與用途應分開。~Pressure times radius is circumferential force per unit height; division by thickness converts it to mean stress. Distinguishing force resultant from stress makes the approximation and its units explicit.',
'同一模數配上不同受力面積或岩盤有效深度，會形成不同支承剛度，因而需要先說明彈簧代表的幾何尺度。~The same modulus combined with different loaded areas or effective rock depths produces different support stiffnesses. The equivalent spring therefore needs a declared geometric scale before its displacement has physical meaning.',
'熱應變本身沒有力的單位，只有與彈性模數及拘束條件結合才形成應力；自由收縮與完全拘束提供兩個理想端點。~Thermal strain has no force unit. Stress emerges only when stiffness and restraint are supplied, making free contraction and full restraint distinct ideal endpoints for interpreting a temperature change.',
'能量線沿流向下降，而壓力線還受高程和速度影響；把兩者分開可避免看到局部低壓便誤判全部水頭耗失。~The energy line falls along the conduit, while the pressure line also depends on elevation and velocity. Separating them prevents local low pressure from being mistaken for total head dissipation.',
'控制體邊界必須說明是否包含發電機、變壓器與輔機用電，否則兩個看似相同效率可能其實分母分子範圍不同。~The conversion boundary must identify whether generator, transformer and auxiliary consumption are included. Otherwise two apparently comparable efficiencies can refer to different energy inputs and different reported electrical outputs.',
'波速由水與管壁的合成可壓縮性決定，並非水流平均速度；壓力訊息能快速往返，而水體本身位移相對較小。~Wave speed reflects the combined compressibility of water and wall, not mean flow velocity. A pressure signal can travel rapidly back and forth while the water itself moves a comparatively short distance.',
'總揚程包含出口與集水坑的位能差及流動損失，泵的工作點由供能曲線與管路需求曲線交會決定而非單看銘牌。~Total head contains elevation difference and flow losses. The operating point follows the intersection of pump supply and system demand curves, rather than being fixed by the nameplate flow alone.',
'係數描述既有資料中的統計關聯，不保證每一項都是獨立因果；水位與季節高度相關時，係數可變得難以辨識。~Coefficients describe associations in the calibration record rather than independent causal mechanisms. Strong correlation between reservoir level and season can make individual parameter estimates difficult to identify even when overall fit is good.',
'緩衝所需容積是累積差額曲線的最大與最小之差，若脈衝並非矩形，必須先積分完整歷線才能辨認容量需求。~For a repeating cycle, required active storage is the range of the cumulative imbalance curve. Nonrectangular pulses require integration of the complete hydrograph before the relevant volume can be identified.'
],
'b216':[
'名目時間只包含一個平均流率，若入流沿某深度快速通過，水庫可同時存在很年輕的水團與多年未交換的深層水。~A nominal time contains only one averaged flow. Rapid passage along one depth can coexist with young water parcels and deep water that exchanges much more slowly, creating a broad age distribution.',
'積分可用水平分力逐點相加，也可先投影再積分，兩種路徑在靜水條件下應一致，這提供幾何模型的獨立檢核。~The horizontal force may be integrated from local components or calculated after projection. Under hydrostatic conditions these routes must agree, providing an independent geometric check without assuming a structural load path.',
'總剛度相加來自同位移條件，與串聯彈簧的同力條件不同；分力比恰為剛度比，只在這個線性並聯模型成立。~Adding stiffnesses follows from common displacement, unlike the common force of series springs. The force ratio equals the stiffness ratio only within this linear parallel model, not as a universal dam property.',
'孔壓作用的方向垂直層面，水壓與總正向力使用相同符號約定才能相減；孔壓上升不是直接增加摩擦的壓緊力。~Pore pressure acts normal to the bedding plane, so it must use a compatible sign convention with total normal force. Increasing water pressure is not additional clamping force available to mobilize friction.',
'若接縫兩側都朝縫面伸長，相對閉合量可能大於單塊伸長；若一起平移則縫寬不變，顯示絕對與相對位移不同。~When both blocks expand toward a joint, relative closure can exceed one block expansion. Common translation leaves gap unchanged, demonstrating why absolute movement and relative aperture are different observables.',
'約化重力只保留密度差造成的浮力尺度，不能用完整重力取代；其平方根與水深共同形成可與流速比較的特徵速度。~Reduced gravity retains the buoyancy associated with density difference and cannot be replaced by full gravitational acceleration. Combined with depth under a square root, it produces a characteristic velocity comparable with withdrawal speed.',
'局部面積就是庫容對水位的導數，因此固定面積近似只適合變動不大的一段高程；跨越地形突變時應分段處理。~Local surface area is the derivative of storage with respect to elevation. Constant area is therefore a local approximation, and a level change spanning abrupt topographic variation should be integrated in segments.',
'躍前與躍後流量相同但速度與水深改變，動量函數相等不代表比能相等，兩斷面的比能差才是耗散的量。~Discharge is conserved across the jump while depth and velocity change. Equal momentum functions do not imply equal specific energies; their specific-energy difference quantifies the mechanical energy dissipated in the transition.',
'質量率積分得到的是運輸量，轉成沉積體積還要知道留下比例與乾容重，因而輸砂與庫容測量應分開設計。~Integrating mass flux gives transported solids. Conversion to deposited volume additionally requires retention and dry bulk density, so sediment transport measurements and reservoir-capacity surveys address related but distinct quantities.',
'質量守恆以溶質通量為基礎，濃度本身不能直接相加；每股流量權重的總和必須等於一，混合濃度應介於兩來源之間。~Mass conservation applies to solute flux rather than concentration alone. Flow weights must sum to unity, and a conservative two-source blend should lie between the source concentrations when both flows are positive.'
]}
FALSE={
'b215':[
'蓄量增加必然讓水位以固定比例上升~Every storage increase raises level in a fixed proportion',
'只靠圓環平均壓應力就足以完成整座拱壩設計~Mean ring compression alone is sufficient for complete arch-dam design',
'岩石彈性模數可直接當成支承彈簧剛度~Rock elastic modulus can directly substitute for support spring stiffness',
'每日氣溫變化就是整座壩體的平均溫變~Daily air-temperature change equals the mean temperature change of the entire dam',
'沿程水頭損失只與流速一次方成比例~Friction head loss is proportional only to the first power of velocity',
'機組功率乘秒仍可直接標成兆瓦小時~Power multiplied by seconds can directly be labelled megawatt-hours',
'一次水錘增量就是整條管線所有位置的最大壓力~One water-hammer increment is the maximum pressure at every pipeline location',
'抽水電功率應將水力功率乘上效率~Pumping electrical input equals hydraulic power multiplied by efficiency',
'監測回歸殘差很小即可證明結構完全安全~A small monitoring regression residual proves complete structural safety',
'每個放流脈衝都能重新使用緩衝池的全部容量~Every release pulse can reuse the entire buffer capacity from scratch'
],
'b216':[
'名目停留時間就是每滴水完全相同的水齡~Nominal residence time is the identical age of every water parcel',
'曲面水平水推力可直接用底壓乘全部曲面面積~Horizontal hydrostatic force equals bottom pressure times the entire curved area',
'一條力路變軟不會改變另一條力路的分力~Softening one load path leaves force in the other path unchanged',
'不必扣除孔隙水壓即可用總正向力算摩擦~Friction can use total normal force without deducting pore pressure',
'單塊自由伸長必然等於接縫實際開口增量~Free expansion of one block necessarily equals actual joint opening',
'密度福祿數有適用所有取水口的固定允許值~Densimetric Froude number has one fixed permitted value for all intakes',
'只知道水位增量就能判斷剩餘蓄洪空間~Knowing only level increment establishes remaining flood-storage capacity',
'水躍同時保持動量函數與機械比能不變~A hydraulic jump conserves both momentum function and mechanical specific energy',
'濁度數值可以直接當作每立方公尺固體公斤數~A turbidity value directly equals kilograms of solids per cubic metre',
'兩股流量不同時仍可把濃度直接取算術平均~Two concentrations can be averaged arithmetically even when source flows differ'
]}
for cid,items in EXTRA.items():
 for i,addition in enumerate(items):
  u,a=C[cid]['units'][i];z,e=split(u['mechanism']);az,ae=split(addition);u['mechanism']=pair(z+' '+az,e+' '+ae);u['misconception']=FALSE[cid][i]
