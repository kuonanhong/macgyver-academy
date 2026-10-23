C('b481',P('以粒徑、解離度和品位回收率設計底渣金屬分選的教學流程','Build a bottom-ash metal-separation workflow around size, liberation and grade-recovery evidence'),'environment-waste',['wi','wiindex','tclp'],[
U(P('底渣批次與金屬基準','Bottom-ash batches and metal basis'),P('先確認底渣來源與乾濕基，區分爐底渣、飛灰和其他混入物流。','Identify the bottom-ash source and moisture basis, distinguishing it from fly ash and other mixed streams.'),'fraction'),
U(P('粒徑分級與篩分','Size classes and screening'),P('不同粒徑的解離程度和適用分選機不同，先分級再比較效率。','Particle sizes differ in liberation and suitable separators; classify before comparing performance.'),'screen'),
U(P('鐵磁性金屬回收','Ferromagnetic metal recovery'),P('磁選以鐵磁性響應分離，夾附礦物和纏繞金屬會改變產品重量。','Magnetic separation uses ferromagnetic response; adhering minerals and tangled metal change product mass.'),'recovery'),
U(P('非鐵金屬渦電流分選','Nonferrous eddy-current separation'),P('導電性、尺寸與形狀影響拋射路徑，不能把所有非鐵金屬看作同一粒子。','Conductivity, size and shape affect trajectories; nonferrous particles are not interchangeable.'),'purity'),
U(P('含水與細泥附著','Moisture and adhering fines'),P('表面水與細泥增加黏附，影響篩分和金屬品位；乾濕處理流程需用同基準比較。','Surface water and fines promote adhesion, affecting screening and grade; compare wet and dry routes on consistent bases.'),'dry_solids'),
U(P('細粒金屬損失','Fine-metal losses'),P('粗粒回收率高仍可能漏掉細粒金屬，應為每個粒級建立獨立收支。','High coarse recovery may hide fine-metal losses; construct separate balances by size class.'),'recovery'),
U(P('礦物產物浸出評估','Leaching of mineral products'),P('金屬回收後的礦物料仍需確認環境適用性；外觀乾淨不是浸出證據。','The mineral fraction still needs environmental suitability assessment; clean appearance is not leaching evidence.'),'leach'),
U(P('粉塵捕集與外逸','Dust collection and escape'),P('乾式分選的粉塵負荷應沿各轉運點追蹤，末端濃度要連同氣量解讀。','Track dry-separation dust at transfer points and interpret outlet concentrations with gas flow.'),'gas_mass'),
U(P('分選用電與資源效益','Separation electricity and resource benefit'),P('更精細分選增加回收也增加能耗，按每噸進料與產品品質比較情境。','Finer separation increases recovery and energy demand; compare scenarios per tonne of feed and by product quality.'),'lca_energy'),
U(P('品位回收率交接','Grade-recovery handoff'),P('交付進料、產品、尾料的乾重與化驗，指出最影響金屬閉合的不確定項。','Deliver dry masses and assays for feed, product and tailings and identify the dominant metal-balance uncertainty.'),'uncertainty')])

C('b482',P('分辨飛灰污染總量、固定化效能與長期浸出證據','Distinguish fly-ash inventory, immobilization performance and long-term leaching evidence'),'environment-waste',['wi','tclp','sw846','remedy'],[
U(P('飛灰與防制殘渣界定','Fly ash and control-residue identification'),P('不同捕集點產生不同鹽分、金屬和碳含量，混樣前必須保留來源。','Different collection points yield different salts, metals and carbon; preserve provenance before compositing.'),'fraction'),
U(P('粒徑與均質分樣','Particle size and representative splitting'),P('細粒與團聚物可能分層，取樣和縮分須避免只取得表面鬆散粉體。','Fines and agglomerates can segregate; sampling and splitting must avoid selecting only loose surface powder.'),'screen'),
U(P('乾基添加量','Dry-basis amendment quantity'),P('固定化與固化不是同一機制，添加物需按乾基記帳並經獨立試驗選擇。','Stabilization and solidification differ; record additives on a dry basis and select them through independent testing.'),'dose'),
U(P('混合含水與成形','Blend moisture and forming'),P('水參與反應與成形，過多水也可能增加孔隙或產生滲出，需保留水收支。','Water supports reactions and forming, while excess may increase pores or drainage; retain the water balance.'),'forming_water'),
U(P('固定介質容量概念','Immobilizing-media capacity'),P('以抽象吸附容量模型說明有限反應能力；實際飛灰需考慮 pH 和競爭離子。','Use an abstract sorption-capacity model to explain finite capacity; real ash also requires pH and competing-ion analysis.'),'capacity'),
U(P('浸出方法與液固比','Leaching method and liquid-solid ratio'),P('方法選擇決定試驗邊界，單次萃取不能替代所有環境暴露。','The test method defines its boundary; one extraction does not represent every environmental exposure.'),'leach'),
U(P('洗液與污染轉移','Wash water and contaminant transfer'),P('若流程含預洗，鹽與污染物會進入水相，必須把洗液處理納入整體方案。','If pretreatment includes washing, salts and contaminants enter water; include wash-water treatment in the system.'),'massflow'),
U(P('批次品質與採樣格','Batch quality and sampling coverage'),P('用批次與空間標記規劃樣點，避免單一合格樣品替整批背書。','Plan samples by batch and location rather than allowing one passing specimen to represent the entire lot.'),'sampling'),
U(P('穩定化能耗比較','Stabilization energy comparison'),P('比較混拌、養護與後續處置的邊界，不能只報添加物用量忽略額外負荷。','Compare mixing, curing and disposal boundaries rather than reporting additive mass while omitting added burdens.'),'lca_energy'),
U(P('不確定度與長期證據','Uncertainty and long-term evidence'),P('將批次差異、分析誤差與試驗條件分開，長期表現需另有老化與不同暴露證據。','Separate batch variability, analytical uncertainty and test conditions; long-term performance needs ageing and exposure evidence.'),'uncertainty')])

C('b483',P('由濾餅、配流與差壓理解袋濾除塵與破袋診斷','Understand bag filtration and failure diagnosis through cake, flow distribution and differential pressure'),'environment-monitoring',['fabric','control','wi'],[
U(P('入口粉塵負荷','Inlet dust loading'),P('入口濃度與實際處理氣量共同決定濾袋每天承受的粉塵，不只看濃度百分比。','Inlet concentration and gas flow jointly determine dust presented to the bags; concentration alone is insufficient.'),'gas_mass'),
U(P('濾布面積與過濾風速','Cloth area and filtration velocity'),P('計算在線面積時扣除停用濾室，並對照分室氣流而非假定均勻。','Subtract isolated compartments from online area and compare compartment flows rather than assuming uniformity.'),'filter_velocity'),
U(P('濾餅累積與阻力','Cake accumulation and resistance'),P('濾餅能捕捉細粒，也增加阻力；清灰需求需從差壓與出口一起判讀。','The dust cake captures fine particles while adding resistance; interpret cleaning need using both pressure drop and outlet data.'),'pressure'),
U(P('清灰週期與能耗','Cleaning cycles and energy'),P('過度清灰會耗能並擾動濾餅，不足清灰會堵塞；在模擬中比較兩種極端。','Over-cleaning consumes energy and disrupts cake; under-cleaning causes blockage. Compare both extremes in simulation.'),'blower'),
U(P('出口濃度與去除率','Outlet concentration and removal'),P('出口濃度是直接量測，去除率需配對入口；兩者不可互相取代。','Outlet concentration is directly measured, while removal needs matched inlet data; neither replaces the other.'),'efficiency'),
U(P('溫壓乾濕基與氧校正','Reference conditions and oxygen correction'),P('保留原始報表與校正欄位，避免在溫度或含濕變化時錯判效能。','Retain raw and normalized fields to avoid false performance changes when temperature or moisture changes.'),'oxygen_correction'),
U(P('破袋事件的時間延遲','Timing of a bag-failure signal'),P('粉塵監測與清灰訊號需扣除取樣傳輸延遲，才能建立合理的事件先後。','Align dust monitoring and cleaning signals for sampling delay before inferring event order.'),'lag'),
U(P('監測失效與缺測','Monitor failure and data gaps'),P('高粉塵或凝結時儀器容易失效，缺值不應變成低排放證據。','Instruments can fail during high dust or condensation; missing values are not evidence of low emissions.'),'coverage'),
U(P('分室診斷可信度','Confidence in compartment diagnosis'),P('比較差壓、粉塵訊號與查漏證據，明確標示哪一項尚不足以定位破袋。','Compare pressure, dust signals and leak-test evidence and identify which observations cannot yet localize a failed bag.'),'uncertainty'),
U(P('維修隔離與備援容量','Maintenance isolation and backup capacity'),P('模擬隔離一室後的風速和處理能力，記錄維修期間的實際可用狀態。','Simulate velocity and capacity after isolating one compartment and record actual availability during maintenance.'),'availability')])

C('b484',P('比較 SCR 與 SNCR 的反應、混合、逸出與監測邊界','Compare SCR and SNCR through reaction, mixing, reagent slip and monitoring boundaries'),'environment-monitoring',['control','wi','cems'],[
U(P('氮氧化物入口基準','NOx inlet basis'),P('先確認 NOx 報告基準與乾標準氣量，將濃度轉成可比較的質量負荷。','Confirm the NOx reporting basis and dry standard flow before converting to comparable mass loading.'),'gas_mass'),
U(P('反應計量與藥劑需求','Reaction stoichiometry and reagent demand'),P('用抽象摩爾模型辨認理論需求與實際轉換的差別，不把比例當成現場注入設定。','Use abstract molar accounting to separate theoretical demand from actual conversion; ratios are not injection settings.'),'stoich'),
U(P('混合與空間速度','Mixing and space velocity'),P('SCR 催化床需均勻配流；局部高速度可能使平均空間速度掩蓋穿透。','An SCR catalyst bed needs uniform flow; local high velocity can cause breakthrough hidden by a mean space velocity.'),'catalyst'),
U(P('反應溫度與熱需求','Reaction temperature and heat demand'),P('SCR 與 SNCR 的反應窗口不同，教學只用顯熱評估熱需求，不提供操作窗口。','SCR and SNCR have different reaction windows; the lesson estimates heat demand without prescribing operating windows.'),'sensible'),
U(P('催化床壓降與積灰','Catalyst pressure drop and deposits'),P('催化活性下降與流道堵塞是不同失效，需將差壓與污染物轉換一起比較。','Activity loss and flow-channel blockage are different failures; compare pressure drop with conversion.'),'pressure'),
U(P('NOx 去除與氨逸出','NOx reduction and ammonia slip'),P('提高去除率時仍須追蹤未反應藥劑，單看 NOx 下降會漏掉副作用。','Track unreacted reagent when increasing removal; NOx decline alone misses side effects.'),'efficiency'),
U(P('氧校正與稀釋','Oxygen correction and dilution'),P('比較不同負荷時先統一氧基準，並保留未校正值供排查漏氣。','Normalize oxygen consistently across loads and retain raw values for leakage diagnosis.'),'oxygen_correction'),
U(P('分析延遲與控制判讀','Analyzer lag and control interpretation'),P('進料、藥劑和出口訊號不同步會造成假因果，先重播延遲再討論回饋。','Asynchronous feed, reagent and outlet signals create false causality; replay delays before interpreting feedback.'),'lag'),
U(P('量測性能與校正','Measurement performance and calibration'),P('藥劑濃度與 NOx 儀器各有零點與跨度誤差，需用獨立標準查核。','Reagent and NOx instruments have separate offset and span errors requiring independent standards.'),'calibration'),
U(P('催化劑壽命與交接','Catalyst life and handoff'),P('交接應包含轉換、逸出、壓降和停機記錄，不能只用日曆年齡推定剩餘能力。','Handoff includes conversion, slip, pressure drop and outages; calendar age alone does not determine remaining capacity.'),'availability')])

C('b485',P('用酸性氣體質量、化學當量與液氣接觸評估洗滌流程','Assess acid-gas scrubbing through mass load, chemical equivalents and gas-liquid contact'),'environment-monitoring',['control','wi','cems'],[
U(P('酸性氣體負荷與成分','Acid-gas loading and species'),P('不同酸性氣體有不同反應當量與溶解性，先分種記錄入口負荷。','Acid gases differ in reaction equivalents and solubility; inventory inlet loading by species.'),'gas_mass'),
U(P('中和反應當量','Neutralization equivalents'),P('先用已平衡的反應式建立理論當量，再將副反應與未利用藥劑列為額外證據。','Start from a balanced reaction and treat side reactions and unused reagent as separate evidence.'),'stoich'),
U(P('循環液與氣體接觸','Recirculating-liquid contact'),P('噴淋與填料潤濕決定有效接觸，總循環量正常不代表每個區域都均勻。','Spray and packing wetting determine effective contact; normal total circulation does not guarantee uniform zones.'),'liquidgas'),
U(P('洗滌塔壓降與阻塞','Scrubber pressure drop and obstruction'),P('填料結垢、液泛與除霧器堵塞可能呈現不同差壓分布，需分段測量。','Scaling, flooding and demister blockage can produce different pressure profiles, requiring sectional measurements.'),'pressure'),
U(P('循環泵與輸送能量','Recirculation-pump energy'),P('循環液輸送需要克服高度與管路損失，泵耗應和處理效能一起比較。','Recirculation overcomes elevation and line losses; compare pumping demand with treatment performance.'),'pump'),
U(P('排放濃度與去除率','Emission concentration and removal'),P('以同一物種同一基準比較進出口，低入口負荷時不以百分比獨斷效果。','Compare the same species and reference basis at inlet and outlet; removal percentage alone is weak evidence at low inlet load.'),'efficiency'),
U(P('排污水鹽分負荷','Blowdown salt load'),P('被捕集的酸形成液相鹽分，需追蹤排污水處理，不能把捕集等同污染消失。','Captured acids form dissolved salts; track blowdown treatment rather than treating capture as disappearance.'),'massflow'),
U(P('水分蒸發與補水','Evaporation and makeup water'),P('高溫煙氣與洗液交換熱與水分，補水需求需與排污和帶出分開。','Hot gas exchanges heat and moisture with scrubbing liquid; distinguish makeup for evaporation, blowdown and carryover.'),'evaporation'),
U(P('量測校正與反應證據','Calibration and reaction evidence'),P('pH、導電度和污染分析各自回應不同物理量；單一感測器正常不代表全部正常。','pH, conductivity and pollutant analysis measure different quantities; one normal sensor does not validate the whole process.'),'calibration'),
U(P('異常負荷與暫存能力','Upset loading and holding capacity'),P('在模擬中增加入口或排污波動，檢查液槽儲量和後段負荷是否超出假設。','Increase inlet or blowdown variability in simulation and examine liquid storage and downstream load assumptions.'),'storage')])
