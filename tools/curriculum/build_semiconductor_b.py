"""Original educational tasks, not a foundry recipe. No real tool setpoints."""
import json
from pathlib import Path
ROOT=Path(__file__).parent
MODULES={}
def module(number,title,title_en,context,context_en,sources,rows):
    MODULES[number]=(title,title_en,context,context_en,sources,rows)

module(11,'源汲極、摻雜與活化','Source/drain, doping and activation',
'佈植劑量、深度分佈、晶格損傷與電性活化是不同變量；外延與佈植屬可替代或組合的整合分支。',
'Implanted dose, depth distribution, lattice damage and electrical activation are different variables; epitaxy and implantation are alternative or combined integration branches.',
['scb-modify','scb-epi','scb-metrology'],r'''
延伸接面剖面建模~Model extension-junction profiles|比較淺接面濃度剖面與通道邊界~Compare shallow dopant profiles with the channel boundary|接面深度與橫向侵入均有標示~Both junction depth and lateral encroachment are identified|只看峰值會漏掉深部尾端~Peak concentration alone hides deep tails
離子種與極性配對~Match dopant species and polarity|將施體與受體分別配置至示意 NMOS 與 PMOS~Assign donors and acceptors to model NMOS and PMOS regions|摻雜極性與源汲極導電型一致~Dopant polarity matches the intended source/drain type|極性顛倒使接面結構錯置~Reversed polarity creates the wrong junction structure
阻擋光罩覆蓋檢查~Inspect implant-block coverage|疊合佈植遮罩與有源區圖形~Overlay the implant mask and active-area geometry|非目標元件均落在阻擋區內~All non-target devices lie inside blocked regions|遮罩缺口造成錯區摻雜~Mask gaps cause unwanted doping
束流質量分析判讀~Interpret beam mass analysis|在模擬質譜中辨別目標離子與污染峰~Distinguish target ions from contaminant peaks in a model spectrum|目標質荷比峰與鄰峰可分離~The target mass-to-charge peak is resolved from neighbors|峰重疊提示離子選擇不足~Overlapping peaks indicate inadequate species selection
法拉第杯劑量積分~Integrate Faraday-cup dose|將校正後束流對曝光時間積分~Integrate calibrated beam current over exposure time|積分電荷與掃描面積可追溯~Integrated charge and scanned area are traceable|漏算掃描空檔會偏估劑量~Ignoring scan gaps biases dose estimates
束流掃描均勻度~Evaluate beam-scan uniformity|重建晶圓不同位置的示意劑量圖~Reconstruct the model dose map across the wafer|中心與邊緣分佈皆在題定範圍~Center and edge distributions meet the exercise limits|條帶紋提示掃描同步異常~Stripes suggest scan-synchronization errors
傾角抑制通道效應~Assess tilt and channeling|比較不同晶向入射的深度分佈~Compare penetration profiles for different crystal orientations|深尾端變化與入射方向相關~Deep-tail changes correlate with incidence direction|忽略晶向會誤認深尾為擴散~Ignoring orientation can mislabel channeling as diffusion
遮蔽陰影與旋轉~Inspect implant shadowing|在閘極立體模型追蹤離子可達區~Trace ion access around model gate topography|兩側源汲極的遮蔽差異已辨認~Shadowing differences between both junctions are identified|單一方位可能造成非對稱摻雜~One azimuth can produce asymmetric doping
佈植充電監看~Monitor implant charging|比較充電監測結構與束流紀錄~Compare charging monitors with beam records|充電事件與介電層損傷訊號未共現~Charging events do not coincide with dielectric-damage signals|劑量正常仍可能有閘氧損傷~Correct dose does not exclude gate-oxide damage
光阻熱負載判讀~Assess resist thermal loading|比對佈植前後光阻輪廓影像~Compare resist profiles before and after model implantation|遮罩邊緣未塌陷或產生顯著退縮~Mask edges show no collapse or marked recession|熱退縮會改變實際阻擋範圍~Thermal recession changes the effective blocked region
預非晶化分支評估~Evaluate pre-amorphization|標示示意非晶層與預定接面的位置~Locate the amorphous layer relative to the intended junction|非晶化範圍與後續再結晶需求相容~Amorphized depth is compatible with recrystallization needs|過深損傷可能增加接面附近缺陷~Excess depth can add defects near the junction
延伸接面低能量模擬~Simulate low-energy extensions|比較投影射程與表面損失的相對影響~Compare projected range with near-surface dopant loss|淺層分佈仍保留可辨認的有效摻雜區~The shallow profile retains a discernible doped region|表面損失可使名義劑量高估有效量~Surface loss can make nominal dose overstate retained dose
袋狀摻雜分支定位~Locate pocket-implant branches|疊合袋狀摻雜與短通道電位模型~Overlay pocket doping and short-channel potential models|抑制穿通區未不當侵入導通通道~Punch-through control does not excessively encroach on the channel|過度重疊可能犧牲遷移率~Excess overlap may reduce mobility
源汲極重摻雜分佈~Inspect heavily doped junctions|分開比較表面濃度與接面梯度~Compare surface concentration and junction gradient separately|低電阻需求與接面漏電限制同時列入~Resistance and junction-leakage constraints are both considered|提高濃度不保證活化同步提升~Higher concentration does not guarantee higher activation
植入後光阻去除檢查~Inspect post-implant resist removal|判讀硬化表層與殘留碳的分析圖~Interpret hardened-skin and residual-carbon evidence|遮罩殘留消失且有源表面未受損~Mask residue is removed without active-surface damage|強行去除可能引入表面粗化~Overaggressive removal can roughen the surface
源汲極凹槽幾何~Measure source/drain recess geometry|在截面圖量取凹槽深度與側壁形狀~Measure recess depth and sidewalls in cross sections|凹槽接近目標形狀且間隔層完整~Recess shape meets the target while spacers remain intact|底部尖角可能集中應力或缺陷~Sharp bottom corners may concentrate stress or defects
外延前界面清潔判讀~Assess the pre-epitaxy interface|比較表面氧化與碳污染分析結果~Compare surface oxide and carbon-contamination results|外延界面具有可追溯的潔淨證據~The epitaxial interface has traceable cleanliness evidence|殘氧會破壞外延起始一致性~Residual oxygen disrupts consistent epitaxial nucleation
選擇性外延成核~Inspect selective epitaxial nucleation|區分矽區成長與介電層寄生成核~Distinguish growth on silicon from parasitic dielectric nucleation|生長侷限於指定晶體開口~Growth is confined to intended crystalline openings|介電層上顆粒提示選擇性失效~Particles on dielectric indicate lost selectivity
外延晶面與合併~Inspect epitaxial facets and merging|追蹤相鄰源汲極外延體的晶面輪廓~Trace facets of neighboring source/drain epitaxial regions|合併或隔離狀態符合版圖分支~Merged or isolated geometry matches the layout branch|非預期合併可能短接獨立節點~Unintended merging can short independent nodes
應變源材料映射~Map strain-source materials|關聯組成圖與通道應變量測~Relate composition maps to channel-strain measurements|應變方向與元件極性需求相容~Strain direction matches the device-polarity objective|組成均勻不代表應變未鬆弛~Uniform composition does not prove unrelaxed strain
原位摻雜外延檢查~Assess in-situ doped epitaxy|分開檢視外延厚度與摻雜濃度圖~Inspect epitaxial thickness and dopant maps separately|兩種分佈均有獨立量測支持~Both distributions have independent measurement support|厚度穩定仍可能有摻雜漂移~Stable thickness can coexist with dopant drift
活化退火熱預算~Evaluate activation thermal budget|比較示意退火後活化率與接面展寬~Compare activation fraction and junction broadening after model anneals|活化改善未超出接面幾何限制~Activation improves without excessive junction broadening|僅追求活化會忽略擴散代價~Optimizing activation alone ignores diffusion cost
快速退火溫度均勻度~Assess rapid-anneal temperature uniformity|對照測溫訊號與晶圓電阻圖~Compare pyrometry traces and wafer resistance maps|空間電性變化可與熱場交叉檢查~Spatial electrical variation can be cross-checked against the thermal field|放射率誤差可冒充真實溫差~Emissivity error can mimic temperature differences
毫秒退火分支比較~Compare millisecond-anneal branches|對照短熱脈衝與較長熱歷程模型~Compare short thermal pulses with longer thermal histories|活化與損傷修復均有驗證指標~Both activation and damage recovery have validation metrics|短脈衝不代表所有缺陷皆已修復~A short pulse does not prove complete defect recovery
SIMS 與片電阻交叉驗證~Cross-check SIMS and sheet resistance|比對化學摻雜剖面與電性導通量測~Compare chemical dopant profiles with electrical conduction|保留摻雜量與有效活化量分別判讀~Retained dopant and electrically active dopant are distinguished|把化學濃度當活化濃度會誤判~Equating chemical and active concentration causes misinterpretation
接面漏電與活化放行~Release junctions using leakage and activation|聯合判读接面漏電、片電阻與缺陷證據~Review leakage, sheet resistance and defect evidence together|導通改善與漏電風險同時符合題定標準~Conduction improvement and leakage risk meet the stated criteria|低片電阻仍可能掩蓋接面缺陷~Low sheet resistance can conceal junction defects
''')

module(12,'矽化物與接觸整合','Silicide and contact integration',
'接觸電阻包含界面與導體貢獻；矽化物、阻障層及塞孔材料依整合路線選擇，不能視為每個節點都使用的固定堆疊。',
'Contact resistance includes interface and conductor contributions; silicides, barriers and plug materials depend on the integration route rather than a universal stack.',
['scb-silicide','scb-cobalt','scb-metallization'],r'''
矽化物界面氧化檢查~Inspect oxide at silicide interfaces|辨認接觸區天然氧化層的分析訊號~Identify native-oxide signatures in contact regions|金屬接觸前界面狀態有獨立證據~Interface condition is documented before metal contact|殘氧可能造成不連續反應~Residual oxide can cause discontinuous reaction
矽消耗厚度預算~Budget silicon consumption|把矽化物形成所需矽量投影至薄源汲極~Project silicide silicon consumption into a thin junction|剩餘矽厚度不侵犯接面完整性~Remaining silicon preserves junction integrity|忽略消耗量可能使接觸穿入接面~Ignored consumption can drive contact into a junction
金屬前驅薄膜連續性~Inspect precursor-metal continuity|檢視反應前金屬覆蓋的截面與表面图~Inspect pre-reaction metal coverage in sections and maps|目標區金屬連續且厚度分佈可追溯~Metal is continuous with traceable thickness variation|孤島成膜會形成不均勻矽化物~Island growth produces nonuniform silicide
自對準反應區辨認~Identify self-aligned reaction regions|標示金屬在矽與介電層上的不同去向~Map metal behavior over silicon and dielectric regions|矽化物僅在指定矽接觸區形成~Silicide forms only at intended silicon contacts|未反應金屬殘留可能跨接間隔層~Unreacted metal residue may bridge spacers
首段矽化反應判讀~Interpret initial silicidation|比較反應前後物相與片電阻訊號~Compare phase and sheet-resistance evidence before and after reaction|電阻變化可由物相轉變支持~Phase evidence supports the resistance change|只看顏色不能證明目標物相~Color alone does not establish the target phase
未反應金屬選擇性去除~Assess unreacted-metal removal|比較介電層殘金屬與矽化物保留量~Compare dielectric metal residue and silicide retention|殘金屬清除且有效矽化物未明顯流失~Residual metal is removed while useful silicide remains|去除不選擇會侵蝕有效接觸~Nonselective removal erodes useful contacts
後段物相穩定化~Assess silicide phase stabilization|判讀後續熱處理的物相與電阻對照~Interpret phase and resistance after subsequent thermal treatment|目標相與低電阻區域空間對應~Target phase spatially matches low-resistance regions|相變不完全可能造成雙峰電阻分佈~Incomplete conversion can cause bimodal resistance
矽化物團聚檢查~Inspect silicide agglomeration|對照島狀影像與局部電阻異常~Relate island-like morphology to local resistance anomalies|導電膜連續性未被團聚破壞~Agglomeration has not broken film continuity|平均厚度合格仍可能局部斷路~Acceptable mean thickness can conceal local opens
側向矽化侵入~Inspect lateral silicide encroachment|在閘邊截面標示反應前沿~Mark the reaction front near gate edges|矽化前沿保留設計所需隔離距離~The reaction front preserves required isolation spacing|側向侵入可導致閘極短接~Lateral encroachment can cause gate shorts
矽化物表面粗糙度~Measure silicide roughness|比較表面高度圖與後續接觸覆蓋模型~Compare height maps with subsequent contact coverage|粗糙度未造成接觸層覆蓋中斷~Roughness does not disrupt contact-layer coverage|局部突起可能造成高場與覆蓋弱點~Protrusions can create high-field and coverage weak spots
接觸介電層厚度檢查~Inspect contact-dielectric thickness|量取接觸層介電膜及停止層厚度~Measure contact dielectric and stop-layer thicknesses|厚度差異已納入接觸孔深度模型~Thickness variation is included in the contact-depth model|膜厚漂移會改變蝕刻終點餘裕~Thickness drift changes etch endpoint margin
接觸孔套刻裕量~Evaluate contact overlay margin|疊合接觸孔與源汲極落點~Overlay contact openings and source/drain landing areas|最差方向仍保留題定落點重疊~The worst direction preserves the required landing overlap|平均套刻可掩蓋局部錯位~Average overlay can hide local misalignment
接觸孔臨界尺寸~Measure contact critical dimensions|對照頂部孔徑與底部孔徑~Compare contact top and bottom dimensions|底部有效接触面積可獨立估計~Effective bottom contact area is independently estimated|只量頂部會漏判底部縮口~Top-only measurement misses bottom narrowing
接觸孔停止層開口~Inspect contact stop-layer opening|區分尚未開口與已傷及落點的截面~Distinguish incomplete opening from landing damage|停止層清除且落點未過度受損~The stop layer clears without excessive landing damage|過度蝕刻會增加接觸界面損傷~Overetch can damage the contact interface
孔底殘留清潔判讀~Assess contact-bottom residue|比對孔底元素分析與電阻分佈~Compare bottom elemental analysis and resistance distribution|孔底殘留訊號降低且介面保持完整~Bottom residue decreases while the interface remains intact|薄殘膜可能造成高接觸電阻~A thin residue film can raise contact resistance
原位轉移防再氧化~Assess in-situ transfer protection|比較清潔至沉積間界面再氧化證據~Compare reoxidation evidence between cleaning and deposition|等待與轉移條件可解釋界面變化~Queue and transfer conditions explain interface evolution|乾淨表面可能在轉移時重新氧化~A clean surface can reoxidize during transfer
接觸襯層底部覆蓋~Inspect contact-liner bottom coverage|在高深寬比孔截面追蹤襯層連續性~Trace liner continuity in high-aspect-ratio contacts|底部與側壁均有連續覆蓋~Both bottom and sidewalls have continuous coverage|頂部成膜正常不保證孔底連續~Good top coverage does not guarantee bottom continuity
接觸阻障層完整性~Verify contact-barrier integrity|比較阻障層截面與元素擴散證據~Compare barrier sections with elemental diffusion evidence|導體元素未出現非預期越界分佈~Conductor species show no unintended boundary crossing|針孔可能讓局部擴散被平均量測漏掉~Pinholes can permit diffusion hidden by averages
鎢成核分支~Inspect tungsten nucleation|辨認示意孔底成核延遲與側壁成長~Identify model bottom nucleation delay and sidewall growth|成核均勻性支持連續塞孔成長~Nucleation uniformity supports continuous plug growth|成核延遲會留下接觸空隙~Delayed nucleation can leave contact voids
鈷填孔分支~Assess cobalt contact filling|比較填充截面與接觸電阻尾端~Compare fill sections and resistance tails|低電阻改善未伴隨界面或空洞異常~Resistance improves without interface or void anomalies|更換材料不會自動消除整合缺陷~Changing material does not automatically remove integration defects
接觸塞孔縫隙辨認~Identify contact-plug seams|在多位置截面區分接合縫與開放空洞~Distinguish seams from open voids across sections|塞孔有效導通路徑保持連續~The effective plug conduction path remains continuous|單一截面可能漏掉偏心空洞~One section can miss off-center voids
塞孔回蝕或研磨終點~Assess plug recess or polish endpoint|比較導體去除量與介電層暴露圖~Compare conductor removal and exposed dielectric maps|場區金屬清除且塞孔未過度凹陷~Field metal clears without excessive plug recess|終點太晚會增加塞孔高度損失~A late endpoint increases plug height loss
塞孔凹陷高度量測~Measure contact-plug recess|以高度剖面量取塞孔與介電層階差~Measure plug-to-dielectric height differences|階差與後續金屬落點需求相容~Height differences suit subsequent metal landing needs|過深凹陷可能增加下一層接觸阻抗~Deep recess can increase next-level contact impedance
Kelvin 接觸電阻抽取~Extract Kelvin contact resistance|用四端結構分離引線與接觸電阻~Separate lead and contact resistance with four terminals|接觸貢獻不被長引線電阻混淆~Lead resistance does not confound the contact contribution|二端量測可能把引線變化當接觸變化~Two-terminal tests can confuse lead and contact changes
接觸鏈失效定位~Locate contact-chain failures|由分段鏈電阻定位高阻接觸群~Use segmented chain resistance to locate high-resistance groups|異常可縮小至可再檢測的接觸區~The anomaly is localized to a reviewable contact region|整條鏈的總值不能指出單一故障位置~Total chain resistance cannot identify one failed contact
接觸整合分支放行~Release a contact integration branch|整合界面、塞孔形貌與電阻尾端證據~Combine interface, plug morphology and resistance-tail evidence|材料分支的形貌與電性結論一致~Morphological and electrical conclusions agree for the material branch|低平均值不能取代缺陷尾端審查~A low mean cannot replace tail-defect review
''')

module(13,'層間介電膜與化學機械平坦化','Interlayer dielectrics and CMP',
'介電膜必須同時提供隔離、機械支撐與可加工性；CMP 的去除速率與圖形密度、膜材及接觸狀態相互耦合。',
'Dielectrics provide isolation, mechanical support and process compatibility; CMP removal couples material, pattern density and pad contact.',
['scb-deposition','scb-cmp','scb-interconnect'],r'''
層間介電膜間隙映射~Map interlayer dielectric gaps|量取導體間空間與待填充的深寬比~Measure conductor spacing and gap aspect ratios|最狹窄區與最深區皆列入填充評估~Both narrowest and deepest regions enter the fill assessment|只檢查開闊區會漏掉窄縫風險~Checking open areas misses narrow-gap risks
介電膜沉積共形性~Assess dielectric conformality|比较階梯頂部、側壁與底部厚度~Compare thickness at tops, sidewalls and bottoms|覆蓋差異能由多位置截面重現~Coverage differences are reproducible across sections|平均膜厚不反映側壁薄弱點~Average thickness misses thin sidewalls
間隙填充夾口辨識~Identify gap-fill pinch-off|追蹤填充過程中開口縮合的幾何變化~Trace closure of the gap opening during filling|開口閉合前內部空間已充分填充~Interior filling precedes closure of the opening|先封口會埋入封閉空洞~Premature closure traps a buried void
可流動介電膜分支~Assess flowable dielectric branches|比較回流前後窄縫內膜形~Compare gap profiles before and after model flow|填充改善與後續收縮均可量測~Fill improvement and later shrinkage are both measurable|良好初始填充可能在固化後生裂~Good initial filling may crack after curing
等離子增強沉積膜質~Inspect PECVD film quality|關聯膜密度、鍵結訊號與漏電樣本~Relate film density, bonding signatures and leakage samples|膜質判讀不僅依賴沉積厚度~Film quality is assessed beyond deposited thickness|疏鬆膜可能增加吸水與漏電~A porous film may increase moisture uptake and leakage
介電膜折射率映射~Map dielectric refractive index|用橢圓偏光模型區分厚度與光學常數~Separate thickness and optical constants in ellipsometry|擬合殘差與參數相關性均受檢查~Fit residuals and parameter correlations are checked|錯誤光學模型會產生假膜厚差~A wrong optical model creates false thickness differences
介電膜應力曲率量測~Measure dielectric stress by curvature|比較沉積前後晶圓曲率~Compare wafer curvature before and after deposition|應力推估使用相同基板與幾何假設~Stress inference uses consistent substrate and geometry assumptions|忽略原始翹曲會誤估薄膜應力~Ignoring initial bow biases film-stress estimates
低介電常數膜孔隙~Assess low-k porosity|對照孔隙特徵、介電常數與機械性~Compare porosity, dielectric constant and mechanical properties|降低電容的收益與強度代價並列~Capacitance benefit and strength cost are considered together|最低介電常數未必適合後續研磨~The lowest dielectric constant may not survive CMP
低介電膜固化收縮~Measure low-k cure shrinkage|比較固化前後膜厚與鍵結變化~Compare thickness and bonding before and after curing|收縮量與材料轉變相互對應~Shrinkage corresponds to the material transformation|不均勻固化可造成局部應力~Nonuniform curing can create local stress
吸濕後膜性質漂移~Assess moisture-induced film drift|比較乾燥與吸濕樣本的光學及電性~Compare optical and electrical data for dry and humid samples|環境歷程與膜性質變化可追溯~Environmental history tracks property changes|將吸水漂移當成沉積漂移會誤修機台~Misreading moisture drift can prompt an incorrect tool adjustment
CMP 前階差掃描~Scan pre-CMP topography|建立高低區高度與圖形密度對照圖~Map height differences against pattern density|待去除高度與保留層位置清楚分離~Removal height is separated from layers that must remain|未知初始階差會誤導終點判斷~Unknown initial topography confuses endpoint decisions
研磨墊表面狀態~Inspect polishing-pad condition|比較墊面孔隙影像與去除速率趨勢~Compare pad-pore images and removal-rate trends|墊面狀態變化可解釋速率變化~Pad-condition changes explain rate variation|釉化墊面可能降低局部去除能力~Pad glazing can reduce local removal capability
研磨墊修整一致性~Assess pad conditioning consistency|重建修整路徑與墊面磨耗圖~Reconstruct conditioning tracks and pad-wear maps|修整覆蓋與墊面磨耗分佈相容~Conditioning coverage matches pad-wear distribution|不均修整可造成徑向研磨偏差~Uneven conditioning can produce radial polish bias
研磨液粒子聚集檢查~Inspect slurry particle aggregation|比較粒徑分佈尾端與刮傷事件~Compare large-particle tails with scratch events|大粒子異常與刮傷關聯已查核~Large-particle excursions are checked against scratching|平均粒徑可能掩蓋少量大聚集物~Mean particle size hides rare large agglomerates
研磨液化學狀態~Assess slurry chemical condition|關聯供液檢測與材料去除選擇性~Relate slurry measurements to material-removal selectivity|供液狀態與參考樣本具有可比性~Slurry condition is comparable with the reference sample|化學漂移可改變去除而非僅改變速率~Chemical drift can change selectivity as well as rate
載具分區壓力響應~Assess carrier-zone response|比較各區調整後的殘膜徑向分佈~Compare radial residual films after zone adjustments|調整方向與局部殘膜變化一致~Adjustment direction agrees with local residual-film changes|盲目加壓可能把中央問題轉移至邊緣~Blind pressure increases can move the problem to the edge
晶圓邊緣研磨效應~Inspect CMP edge effects|量測邊緣排除區內外的殘膜變化~Measure residual films across the edge-exclusion boundary|邊緣模型與可用晶粒範圍相符~The edge model matches the usable die region|省略邊緣資料會低估實際不均勻度~Omitting edge data understates nonuniformity
光學研磨終點訊號~Interpret optical CMP endpoint|比較多波段訊號與薄膜轉換位置~Compare multiband signals with film-transition locations|終點特徵可與獨立膜厚量測對應~Endpoint features match independent thickness measurements|單一波長干涉可能產生假終點~Single-wavelength interference can produce false endpoints
介電層停止選擇比~Assess dielectric stop selectivity|對照介電膜與停止層去除曲線~Compare removal curves for dielectric and stop layers|停止層保留量可抵抗題定過研磨變動~Retained stop thickness tolerates the stated overpolish variation|高主膜速率不代表良好停止能力~High main-film removal does not imply good stopping
圖形密度侵蝕效應~Assess pattern-density erosion|對照密集與稀疏區的平坦化結果~Compare planarization in dense and sparse regions|跨圖形密度的高度差均受控制~Height differences across pattern densities are controlled|均勻空白片不能代表圖形晶圓~A uniform blanket wafer does not represent patterned wafers
局部凹陷與殘膜區分~Distinguish recess from residual film|用高度及材料訊號分辨過研磨與欠研磨~Use height and material signals to separate overpolish from underpolish|凹陷與殘留對應不同的材料證據~Recess and residue have distinct material evidence|把兩者混為一談會反向調整製程~Confusing them can reverse the needed correction
CMP 刮傷方向分析~Analyze CMP scratch direction|把刮傷方向與墊面運動軌跡對照~Compare scratch orientation with pad motion tracks|方向與缺陷形貌支持一致的來源假說~Orientation and morphology support a consistent source hypothesis|孤立粒子與連續刮痕不應共用診斷~Isolated particles and continuous scratches need different diagnoses
研磨後刷洗殘粒~Inspect post-CMP brush-clean residues|比較清洗前後顆粒地圖與膜損傷~Compare particle maps and film damage before and after cleaning|顆粒減少未增加薄弱膜損傷~Particles decrease without added fragile-film damage|更強刷洗可能增加機械傷害~More aggressive brushing can increase mechanical damage
乾燥水痕辨識~Identify post-clean drying marks|分辨環狀水痕與研磨殘粒形貌~Distinguish ring-shaped drying marks from CMP particles|污染形貌與乾燥位置具有一致關聯~Residue morphology correlates with drying locations|水痕可能被誤判為原始沉積缺陷~Drying marks may be mistaken for deposition defects
平坦化後膜厚閉合~Close the post-CMP thickness balance|對照初始膜厚、去除量與最終殘膜~Compare initial film, removed amount and final residual film|三者在量測不確定度內相互一致~The three quantities agree within measurement uncertainty|不閉合提示量測模型或材料變化~Nonclosure suggests model error or material change
介電隔離與平坦度放行~Release dielectric isolation and planarity|整合高度圖、漏電與機械缺陷證據~Combine height maps, leakage and mechanical-defect evidence|平坦化改善未犧牲電氣隔離~Planarization improvement preserves electrical isolation|表面平坦不能保證介電膜無損傷~A flat surface does not prove an undamaged dielectric
''')

module(14,'鑲嵌式互連圖形與蝕刻','Damascene interconnect patterning and etch',
'鑲嵌互連先在介電層形成溝槽或導通孔，再填入導體；先孔後槽、先槽後孔及其他整合路線的順序不可任意混接。',
'Damascene forms trenches or vias in dielectric before conductor fill; via-first, trench-first and other integration routes cannot be combined arbitrarily.',
['scb-interconnect','scb-lam-interconnect','scb-deposition'],r'''
互連層與網路對照~Map interconnect levels to nets|把示意金屬層、導通孔與電路節點逐一對照~Map model metal levels and vias to circuit nodes|每個跨層連接具有明確的起點與終點~Each interlevel connection has a defined start and endpoint|層號正確仍可能連到錯誤網路~A correct layer number can still connect the wrong net
先孔後槽路線選擇~Select a via-first branch|排列先孔後槽的遮罩與保護層示意~Arrange masks and protection layers for a via-first model|導通孔在溝槽圖形化時仍獲保護~Vias remain protected during trench patterning|省略保護會使孔底受二次攻擊~Missing protection exposes via bottoms to additional attack
先槽後孔路線選擇~Select a trench-first branch|排列先槽後孔的對準與底部開口步驟~Arrange alignment and bottom opening in a trench-first model|導通孔落在已定義溝槽的允許區~Vias land within the permitted trench region|套刻裕量不足可能造成孔槽失配~Insufficient overlay margin can misregister trench and via
硬遮罩堆疊識別~Identify the hardmask stack|把圖形轉移層與最終介電膜分開標示~Separate pattern-transfer layers from final dielectric|每層的轉移與停止功能均可說明~Transfer and stopping roles are explained for each layer|混淆遮罩與介電膜會誤判去除順序~Confusing masks and dielectric leads to incorrect removal order
底部蝕刻停止層定位~Locate the bottom etch stop|在多層截面找出下層金屬上的保護層~Locate protection above the lower metal in a multilayer section|開孔終點與下層導體保持可辨間隔~The opening endpoint is distinguished from the lower conductor|看不清停止層容易接受金屬損傷~An unresolved stop layer can conceal metal damage
孔層抗反射模型~Assess via-layer antireflection|比較反射模型與導通孔尺寸變化~Compare reflection models with via-size variation|反射變化與尺寸偏差有相容解釋~Reflection changes plausibly explain dimension variation|只調曝光可能掩蓋膜堆疊反射差~Exposure-only adjustments can conceal stack-reflection differences
導通孔曝光焦距裕量~Evaluate via focus margin|比較焦距掃描樣本的孔形輪廓~Compare via profiles across a focus-sweep sample set|可接受孔徑區與焦距變動範圍相容~Acceptable via dimensions cover the focus-variation range|單一最佳焦點不代表可量產窗口~One best-focus image does not establish a production window
導通孔殘膜辨識~Identify via scum|檢視顯影後孔底殘膜與開口尺寸~Inspect post-develop bottom scum and opening dimensions|孔底實際開放且邊緣未過度流失~The bottom is open without excessive edge loss|表面開孔可能仍被薄殘膜封住~An apparent opening may retain a thin blocking film
導通孔硬遮罩轉移~Transfer the via hardmask|比较光阻孔形與硬遮罩孔形~Compare resist openings with transferred hardmask openings|圖形偏移與尺寸偏差已逐層量化~Shift and dimensional bias are quantified across layers|只量最上層不能追蹤轉移損失~Top-layer measurements cannot track transfer loss
導通孔側壁角度~Measure via sidewall angle|從截面分離垂直、錐形與弓形輪廓~Separate vertical, tapered and bowed via profiles|孔底可達性與預定填充方式相容~Bottom accessibility is compatible with intended filling|弓形側壁可增加局部薄襯層風險~Bowed sidewalls can increase local liner-thinning risk
深孔蝕刻滯後~Assess aspect-ratio-dependent etch lag|比較不同孔寬的實際蝕刻深度~Compare etched depth across different via widths|尺寸依賴的深度差有可量測上限~Width-dependent depth differences are explicitly bounded|大孔到達終點不代表小孔已開通~Large-via endpoint does not prove small vias are open
導通孔底部微溝~Inspect via-bottom microtrenching|在孔底角落尋找局部加深特徵~Look for localized deepening at via-bottom corners|孔底邊角未形成非預期凹槽~Bottom corners lack unintended grooves|局部微溝可能被中央深度值掩蓋~A central depth value can hide corner microtrenches
孔內犧牲填充~Assess sacrificial via fill|追蹤孔內保護填料的高度與空隙~Track protective via-fill height and voids|保護層覆蓋孔底且可在後續移除~Protection covers the bottom and remains removable|填料空洞使孔底仍暴露於槽蝕刻~Fill voids leave via bottoms exposed during trench etch
溝槽光罩與孔套刻~Align trench masks to vias|比較溝槽中心線與導通孔位置~Compare trench centerlines and via positions|孔槽重疊保留題定連接面積~Trench–via overlap preserves the stated connection area|中心套刻正常仍可能有場內旋轉誤差~Good center overlay can hide intrafield rotation
溝槽線寬與線距~Measure trench width and spacing|在密集與孤立線分別量取線槽尺寸~Measure dense and isolated trench patterns separately|兩類圖形皆符合各自的題定尺度~Both pattern types meet their respective exercise dimensions|孤立線合格不能代表密集線不橋接~Passing isolated lines does not exclude dense-pattern bridging
溝槽硬遮罩選擇性~Assess trench hardmask selectivity|比較溝槽刻深與遮罩剩餘厚度~Compare trench depth and remaining mask thickness|遮罩在溝槽成形前仍保有完整性~The mask remains intact until trench formation completes|過早消耗遮罩會放大線寬偏差~Premature mask loss increases linewidth bias
溝槽深度終點~Determine trench-depth endpoint|對照截面深度與示意终點訊號~Compare sectional depth and model endpoint signals|溝槽深度保留介電隔離與導體截面需求~Trench depth preserves insulation and conductor cross-section needs|只追求深槽可能增加寄生電容~Deeper trenches can increase parasitic capacitance
孔槽交會肩部輪廓~Inspect trench–via shoulder profiles|檢視孔槽交會處的尖角與肩部殘留~Inspect sharp corners and shoulder residue at trench–via intersections|交會幾何允許後續襯層連續覆蓋~Junction geometry permits continuous subsequent liners|肩部殘留可能縮小有效導通截面~Shoulder residue can reduce effective conduction area
蝕刻後聚合殘留~Inspect post-etch polymer residue|區分側壁保護膜與應移除殘留~Distinguish protective sidewall films from unwanted residue|殘留清除不使介電側壁明顯後退~Residue removal avoids substantial dielectric recession|殘膜與過度清洗都可損害填充~Residue and excessive cleaning can both impair filling
低介電膜電漿損傷~Assess plasma damage to low-k films|比較表層化學與介電特性變化~Compare surface chemistry and dielectric-property changes|損傷深度與電容變化有獨立佐證~Damage depth and capacitance change have independent evidence|外觀正常不表示孔隙結構未改變~Normal appearance does not imply unchanged porosity
停止層最終開通~Inspect final stop-layer breakthrough|比較停止層清除與下層金屬暴露程度~Compare stop-layer removal and lower-metal exposure|接觸落點開放且金屬損失受控~The landing is open with controlled metal loss|延長開通時間可能造成金屬凹蝕~Longer breakthrough can recess the lower metal
下層金屬表面氧化~Assess exposed lower-metal oxidation|對照等待時間與孔底金屬表面訊號~Compare queue time and bottom-metal surface signatures|暴露後的界面狀態可納入接觸模型~Post-exposure interface condition enters the contact model|忽略再氧化可能錯怪填孔材料~Ignoring reoxidation can misattribute failure to fill material
雙鑲嵌空腔三維重建~Reconstruct dual-damascene cavities|整合俯視與截面資料重建空腔連通~Combine plan-view and sectional data to reconstruct cavity connectivity|導通孔與溝槽在三維模型中連通~Vias and trenches connect in the reconstructed geometry|兩張分離截面可能造成假連通印象~Separate sections can misleadingly suggest connectivity
線端與孔端最小間距~Inspect line-end and via-end spacing|量測線端附近最易失去隔離的區域~Measure isolation-critical regions near line ends|最弱局部間距仍符合題定隔離需求~The weakest local spacing meets stated isolation needs|平均線距會漏掉線端狹縫~Mean spacing misses line-end pinch points
圖形轉移偏差回饋~Feed back pattern-transfer bias|分開整理曝光、遮罩與介電蝕刻偏差~Separate exposure, hardmask and dielectric-etch biases|修正歸因至造成偏差的具體工站~Correction targets the station producing the bias|把所有偏差推回曝光會過度補償~Assigning every bias to exposure overcompensates
填金屬前空腔放行~Release cavities before metallization|合併空腔形貌、殘留與落點界面證據~Combine cavity morphology, residue and landing-interface evidence|空腔可填充且接觸面可用~Cavities are fillable and landing interfaces are usable|幾何正確但界面污染仍會造成高阻~Correct geometry with contamination can still produce high resistance
''')

module(15,'金屬阻障、填充與多層連接','Metal barriers, filling and multilayer connections',
'細互連的有效導體截面受阻障與襯層占比影響；成核、填充、退火與研磨需以導通、隔離及可靠度共同驗證。',
'Barrier and liner fractions reduce the conducting cross-section of narrow wires; nucleation, filling, annealing and polishing require joint electrical and reliability checks.',
['scb-electroplating','scb-metallization','scb-cobalt','scb-cmp'],r'''
阻障厚度與導體截面~Budget barrier thickness and conductor area|從空腔尺寸扣除阻障及襯層佔用面積~Subtract barrier and liner area from cavity dimensions|電阻模型使用剩餘有效導體截面~Resistance modeling uses the remaining conductor cross-section|用外部線寬估算會低估電阻~Using outer linewidth underestimates resistance
擴散阻障材料分支~Compare diffusion-barrier branches|對照候選阻障與相鄰金屬介電膜相容性~Compare barrier compatibility with adjacent metal and dielectric|候選材料具有界面及擴散的證據鏈~Candidate materials have interface and diffusion evidence|低電阻不代表阻擋擴散能力足夠~Low resistance does not ensure adequate diffusion blocking
ALD 阻障飽和判讀~Assess ALD barrier saturation|比較沉積響應與表面位點飽和示意~Compare deposition response with surface-site saturation models|增加前驅曝露不再改變單循環增量~Added precursor exposure no longer changes growth per cycle|未飽和反應會破壞深孔厚度一致性~Unsaturated reactions impair deep-feature uniformity
阻障層側壁連續性~Inspect barrier sidewall continuity|追蹤溝槽角落與孔底的連續薄膜~Trace continuous films at trench corners and via bottoms|最薄位置仍具可辨識連續阻隔~The thinnest location retains a discernible continuous barrier|一個針孔即可形成局部擴散捷徑~One pinhole can form a local diffusion shortcut
金屬襯層附著評估~Evaluate metal-liner adhesion|比較界面剝離位置與材料堆疊~Compare delamination locations with the material stack|破壞位置與題定附著需求相容~Failure location is compatible with stated adhesion requirements|把內聚破壞誤判界面破壞會選錯改善項~Confusing cohesive and interface failure misdirects improvements
種子層孔底覆蓋~Inspect seed coverage at via bottoms|區分連續種子層與局部未覆蓋區~Distinguish continuous seed films from uncovered bottom areas|待電鍍表面具有連續導電路徑~Plating surfaces have continuous conductive paths|局部斷種會造成延遲成核與空洞~Seed discontinuities delay nucleation and cause voids
種子層懸簷遮蔽~Inspect seed-layer overhangs|量取孔口懸簷與剩餘開口大小~Measure opening overhang and remaining aperture|孔口仍允許後續填充傳質~The opening still permits mass transport during filling|過厚孔口種子層會提早封口~Excess seed at the opening can seal it prematurely
種子層片電阻圖~Map seed-layer sheet resistance|比對種子膜電阻與電鍍供電路徑~Compare seed resistance maps and plating current paths|高電阻區未破壞均勻供電假設~High-resistance regions do not invalidate uniform-current assumptions|厚度正常但污染仍可提高電阻~Normal thickness with contamination can still raise resistance
電鍍液添加劑平衡~Assess plating-additive balance|比較加速、抑制與整平作用的示意響應~Compare accelerator, suppressor and leveler responses|底部增長與孔口抑制能在模型中共存~The model supports bottom growth and opening suppression together|單看總沉積量會漏判添加劑失衡~Total deposition can hide additive imbalance
電鍍潤濕與困氣~Assess plating wetting and trapped gas|檢查孔內液體進入與氣泡遮蔽示意~Inspect liquid access and bubble masking within cavities|待鍍表面可被連續電解液接觸~Electrolyte continuously contacts the intended plating surface|困氣會造成局部無沉積區~Trapped gas causes local nondeposition
底部向上填充~Evaluate bottom-up fill|追蹤截面序列的孔底與孔口生長~Track bottom and opening growth through section sequences|空腔由底部填滿而非由口部封閉~The cavity fills from the bottom rather than sealing at the opening|側壁等速成長可能留下中心縫~Equal sidewall growth may leave a central seam
電流分佈邊緣效應~Assess plating edge-current effects|比較邊緣導電接點與鍍層厚度圖~Compare edge electrical contacts with plated-thickness maps|厚度徑向差異有對應的供電解釋~Radial thickness variation has a matching electrical explanation|邊緣厚膜可能源於電流擁擠~Thick edges can result from current crowding
鍍銅過覆蓋厚度~Measure copper overburden|區分空腔內填充與表面過覆蓋金屬~Separate cavity fill from surface overburden|過覆蓋量符合後續研磨可處理範圍~Overburden falls within the subsequent polish capability|減少表面銅不代表孔內已填滿~Less surface copper does not prove complete cavity fill
鍍後自退火追蹤~Track post-plating self-annealing|比較存放歷程中的電阻與晶粒變化~Compare resistance and grain changes during storage|量測時間點與材料演化一致記錄~Measurement timing is documented with material evolution|跨時間比較會把自退火誤當機台漂移~Time-mismatched comparisons can misread self-annealing as tool drift
金屬晶粒与散射~Assess metal grains and scattering|關聯晶粒尺度、線寬與電阻變化~Relate grain size, linewidth and resistance changes|電阻解釋同時考慮尺寸與微結構~Resistance interpretation includes size and microstructure|只用塊材電阻率會低估細線效應~Bulk resistivity alone understates narrow-line effects
填充空洞三維抽樣~Sample fill voids in three dimensions|比較多方位截面與電性異常區~Compare sections from multiple orientations with electrical anomalies|空洞位置與可能導通瓶頸相對應~Void locations match potential conduction bottlenecks|單張良好截面不足以排除空洞~One good section does not exclude voids
銅過覆蓋研磨終點~Determine copper-overburden polish endpoint|追蹤場區銅消失與阻障層暴露~Track field-copper clearance and barrier exposure|場區銅完全清除而導線仍完整~Field copper clears while lines remain intact|欠研磨可留下連接相鄰線的銅膜~Underpolish can leave copper bridging neighboring lines
阻障去除與低介電保護~Balance barrier removal and low-k protection|比較阻障殘留與介電侵蝕程度~Compare residual barrier and dielectric erosion|阻障清除未造成介電支撐明顯損失~Barrier clearance avoids significant dielectric support loss|更久研磨可能造成線間結構受損~Longer polishing can damage structures between lines
寬銅線凹陷量測~Measure dishing in wide copper lines|量取不同線寬中央與邊緣高度~Measure center and edge heights across line widths|線寬依賴凹陷被納入導體截面估計~Width-dependent dishing enters conductor-area estimates|表面平均高度可能掩蓋線中央凹陷~Mean surface height can hide center-line dishing
密集互連區侵蝕~Assess erosion in dense interconnects|比較密集陣列與參考區的整體高度~Compare dense arrays and reference-area heights|圖形密度造成的高度差已受控~Pattern-density-dependent height differences are controlled|線條各自平坦仍可能整區下降~Individually flat lines can coexist with array-wide erosion
金屬蓋層完整性~Verify metal capping integrity|檢查銅表面蓋層的連續性與界面~Inspect continuity and interfaces of copper caps|蓋層覆蓋對應已清潔的金屬表面~Cap coverage matches a verified clean metal surface|污染界面可能使蓋層附著失效~Contaminated interfaces can impair cap adhesion
導通孔電流擁擠~Assess via current crowding|將電流密度模型疊合實際孔槽幾何~Overlay current-density models on measured via–trench geometry|高電流區與幾何收縮位置一致~High-current regions match geometric constrictions|只用平均電流密度會漏判局部熱點~Average current density misses local hotspots
冗餘導通孔連接~Evaluate redundant-via connections|比較單孔與多孔連接的失效路徑~Compare failure paths for single- and multi-via connections|替代電流路徑在局部失效後仍存在~An alternate current path remains after a local failure|多孔共用弱界面可能形成共同失效~Multiple vias sharing a weak interface can fail together
多層累積套刻~Assess accumulated multilayer overlay|疊合多層落點與量測誤差方向~Overlay multilayer landings and error directions|累積偏差未壓縮最弱層連接裕量~Accumulated error preserves the weakest layer's landing margin|各層平均合格不保證全堆疊對準~Passing layer averages does not guarantee stack alignment
多層 RC 網路量測~Measure multilayer RC networks|用鏈路與電容結構分離電阻電容來源~Separate resistance and capacitance using chain and capacitor structures|延遲變化可對應至具體導線層~Delay changes can be assigned to specific wiring levels|總延遲不能單獨指出材料或幾何問題~Total delay alone cannot distinguish material and geometry problems
互連堆疊電性放行~Release the interconnect stack electrically|合併開短路、線阻與層間漏電圖~Combine opens, shorts, line resistance and interlevel leakage maps|導通與隔離兩種要求同時成立~Conduction and isolation requirements are both satisfied|只測導通會漏掉線間短接風險~Continuity-only testing misses interline-short risks
''')

module(16,'鈍化、背面加工與晶圓完工','Passivation, backside processing and wafer finish',
'鈍化保護與薄化支撐要一起設計；晶圓厚度、殘餘損傷、翹曲與後续封裝介面是不同放行項。',
'Passivation protection and thinning support are designed together; thickness, residual damage, bow and packaging interfaces require separate acceptance evidence.',
['scb-deposition','scb-grinding','scb-stressrelief','scb-metrology'],r'''
頂層金屬完整性~Inspect top-metal integrity|檢查最上層導體輪廓與暴露表面~Inspect top-level conductor profiles and exposed surfaces|最終保護前無未解釋裂縫或橋接~No unexplained cracks or bridges remain before protection|蓋上鈍化會使既有缺陷更難定位~Passivation makes preexisting defects harder to locate
鈍化膜水氣阻隔~Assess passivation moisture barriers|比较膜結構與示意水氣滲入路徑~Compare film structure and model moisture paths|連續阻隔路徑覆蓋需保護區~A continuous barrier covers protected regions|針孔會使平均膜厚失去代表性~Pinholes undermine average-thickness arguments
鈍化膜應力配平~Balance passivation stress|比較保護膜堆疊與晶圓曲率變化~Compare passivation stacks and wafer-curvature changes|保護能力與整體翹曲同時符合需求~Protection and global bow meet their respective requirements|提高阻隔能力可能增加膜應力~Improved barrier properties can increase film stress
焊墊開口光罩對位~Align pad-opening masks|把鈍化開口疊合金屬焊墊與保護邊界~Overlay openings on pads and protective boundaries|開口保留焊墊邊缘所需覆蓋~Openings retain required pad-edge coverage|開口偏移可能暴露非接合區金屬~Misalignment can expose nonbonding metal regions
焊墊開口蝕刻~Inspect pad-opening etch|對照開口底部清除與金屬表面損傷~Compare bottom clearance and pad-metal damage|介電殘留清除且焊墊表面完整~Dielectric residue clears while the pad surface remains intact|過度蝕刻可能降低後續接合品質~Overetch can reduce subsequent bonding quality
焊墊表面殘留~Inspect pad-surface residues|分辨介電殘渣、腐蝕物與有機污染~Distinguish dielectric residue, corrosion and organic contamination|污染種類由相容的分析證據支持~Contamination type is supported by suitable analytical evidence|不同殘留混同會選錯清潔策略~Confusing residue types leads to an unsuitable cleaning strategy
保護聚合物覆蓋~Assess protective polymer coverage|比較聚合膜在階梯與平坦區的厚度~Compare polymer coverage over steps and flat regions|機械緩衝覆蓋不阻擋必要焊墊~Mechanical buffer coverage leaves required pads accessible|厚膜跨階梯可能保留氣泡或空隙~Thick films over steps can trap bubbles or voids
聚合物固化收縮~Assess polymer cure shrinkage|量取固化後開口尺寸與膜厚變化~Measure opening dimensions and thickness after curing|收縮後形貌仍符合介面需求~Post-cure geometry still satisfies interface requirements|固化前尺寸合格不保證固化後合格~Pre-cure compliance does not prove post-cure compliance
劃片道結構辨認~Identify structures in dicing streets|標示測試結構、金屬與允許切割區~Map test structures, metal and allowable cut regions|切割區與晶粒保護邊界清楚分離~Cut regions are separated from die-protection boundaries|誤切金屬可能增加毛邊與剝離~Cutting unintended metal can increase burrs and delamination
密封環連續性~Inspect seal-ring continuity|沿晶粒邊界追蹤密封環結構~Trace seal-ring structures around die boundaries|密封環沒有非設計開口或中斷~The ring lacks unintended gaps or interruptions|單一邊緣截面不能證明周邊連續~One edge section cannot prove perimeter continuity
薄化前正面保護~Assess frontside protection before thinning|比較保護膠帶與表面凸起的貼合~Compare protective-tape conformity around surface features|敏感結構受支撐且無顯著懸空區~Sensitive features are supported without substantial unsupported regions|局部懸空可放大研磨受力~Unsupported areas amplify grinding loads
保護膠帶氣泡檢查~Inspect protection-tape bubbles|建立貼附氣泡與正面結構位置圖~Map lamination bubbles against frontside structures|氣泡位置不破壞題定支撐條件~Bubble locations preserve the stated support conditions|氣泡可在薄化時引起局部厚度偏差~Bubbles can cause local thickness variation during thinning
臨時載板接合分支~Assess temporary carrier bonding|判讀接合界面空洞與支撐平整度~Interpret bond voids and support flatness|接合區提供連續支撐且可後續分離~Bonded regions provide continuous support and remain releasable|高接合強度不代表易於安全分離~High bond strength does not ensure safe release
晶圓邊緣預修整~Evaluate wafer edge trimming|比較薄化前後邊緣形狀模型~Compare edge-shape models before and after thinning|薄化後不形成易碎尖銳邊緣~Thinning does not create a fragile sharp edge|忽略邊緣形狀會增加崩邊風險~Ignoring edge geometry increases chipping risk
粗研磨去除模型~Model coarse backgrinding removal|追蹤主要厚度去除與表面損傷層~Track bulk thickness removal and surface-damage layers|粗磨去除量為後續細磨保留餘裕~Coarse removal leaves allowance for fine grinding|追求快速去除可能留下過深損傷~Fast removal can leave excessively deep damage
細研磨表面精化~Assess fine-grinding refinement|比較粗細研磨後的粗糙度與損傷深度~Compare roughness and damage depth after coarse and fine grinding|表面改善有粗糙度與損傷的雙重證據~Both roughness and damage measurements support improvement|表面光滑不保證次表面無裂紋~A smooth surface does not exclude subsurface cracks
非接觸厚度量測~Measure thickness without contact|比較矽厚度量測與膠帶載板厚度~Separate silicon thickness from tape and carrier thickness|量測指標對應真正的矽殘厚~The measured variable represents remaining silicon thickness|總堆疊厚度會混入膠層變動~Total stack thickness includes adhesive variation
總厚度變異映射~Map total-thickness variation|量測薄化晶圓不同位置的殘厚~Measure remaining thickness at multiple wafer locations|局部極值與全片分佈均有呈現~Local extremes and wafer-wide distribution are both reported|僅平均厚度會漏掉薄弱區~Mean thickness alone misses thin weak regions
薄化後翹曲量測~Measure bow after thinning|區分自由狀態與受夾持狀態的形狀~Distinguish free-state shape from clamped shape|翹曲量測的邊界條件明確記錄~Boundary conditions of bow measurement are documented|受夾持平整不能代表自由晶圓平整~Clamped flatness does not establish free-wafer flatness
研磨損傷應力消除~Assess grinding-damage stress relief|比較去損傷前後裂紋深度與強度樣本~Compare crack depth and strength before and after damage removal|損傷減少與機械強度改善一致~Reduced damage agrees with improved mechanical strength|只看外觀不能量化強度恢復~Appearance alone cannot quantify strength recovery
背面清潔粒子圖~Map backside cleaning particles|區分研磨碎屑與外來粒子分佈~Separate grinding debris from foreign-particle patterns|背面殘粒降低且正面未新增污染~Backside particles decrease without new frontside contamination|共用清洗路徑可能轉移污染~Shared cleaning paths can transfer contamination
薄晶圓搬運支撐~Assess thin-wafer handling support|在示意搬運軌跡分析接觸與彎曲~Analyze contact and bending along a model handling path|搬運支點不產生非預期局部彎曲~Support points avoid unintended local bending|厚晶圓合格軌跡未必適合薄晶圓~A thick-wafer handling path may not suit thin wafers
載板分離後殘膠~Inspect residue after carrier release|比較分離後表面殘留與膜剝離影像~Compare release residue and film-delamination images|分離完成且功能膜未隨膠層脫落~Release is complete without removing functional films|乾淨外觀可能掩蓋薄層殘膠~A clean appearance can conceal thin adhesive residue
背面金屬相容分支~Assess optional backside metallization|對照背面金屬用途與基板電位配置~Match optional backside metal to substrate-potential requirements|只有需要背面電接觸的路線使用此分支~The branch is used only where backside electrical contact is required|所有晶片一律鍍背金屬會引入錯誤假設~Universal backside metallization is an invalid assumption
完工晶圓外觀與厚度放行~Release finished-wafer appearance and thickness|聯合審查崩邊、刮傷、殘厚及翹曲圖~Review chipping, scratches, thickness and bow together|晶粒可用區與後續設備夾持需求皆滿足~Usable die regions and downstream handling needs are satisfied|單看良好區域照片會漏掉局部破損~A good-area photograph can miss local damage
完工晶圓與封裝介面交接~Handoff finished wafers to packaging|核對焊墊表面、晶圓厚度及晶粒座標版本~Cross-check pad surfaces, wafer thickness and die-map versions|封裝端接收的物理與資料介面一致~Physical and data interfaces agree for packaging receipt|座標版本錯配會把好壞晶粒標反~A map-version mismatch can misidentify good and bad die
''')

module(17,'線上檢查、量測與統計製程管制','Inline inspection, metrology and SPC',
'缺陷檢查回答哪裡有異常，量測回答物理量是多少；統計管制需先確認量測系統及穩定基線，管制界限不等同設計規格。',
'Inspection locates anomalies while metrology estimates physical quantities; statistical control requires a qualified measurement system and stable baseline, and control limits are not specifications.',
['scb-kla','scb-metrology','scb-spc','scb-virtual','scb-cdsem','scb-afm'],r'''
量測座標重定位~Relocate metrology coordinates|把晶圓缺口、晶粒與量測點座標對齊~Align wafer-notch, die and measurement-site coordinates|重複量測指向相同實體結構~Repeated measurements address the same physical structure|座標旋轉錯誤會製造假空間漂移~A coordinate rotation creates false spatial drift
參考標準片偏差~Assess reference-wafer bias|將儀器讀值與可追溯參考值比對~Compare instrument readings with traceable reference values|偏差與參考值不確定度一同記錄~Bias is recorded together with reference uncertainty|把參考值當絕對真值會低估不確定度~Treating a reference as exact understates uncertainty
量測重複性試驗~Evaluate measurement repeatability|對同一結構重測並分離短期散布~Remeasure one structure to isolate short-term scatter|重複散布小於待辨識的製程變化~Repeatability scatter is below the process change of interest|儀器雜訊可冒充晶圓變異~Instrument noise can mimic wafer variation
量測再現性分解~Separate measurement reproducibility|比較不同操作者與機台的交叉量測~Compare crossed measurements across operators and tools|機台及操作者貢獻可獨立估计~Tool and operator contributions can be estimated separately|混用機台會把校正差當製程差~Mixed tools can turn calibration differences into apparent process differences
量測線性與範圍~Assess metrology linearity and range|用不同尺寸參考結構檢查量測偏差~Check bias using reference structures spanning the range|偏差不隨尺度產生未校正趨勢~Bias has no uncorrected scale-dependent trend|單點校正不能保證全範圍準確~Single-point calibration does not establish full-range accuracy
CD-SEM 邊緣判定~Assess CD-SEM edge detection|比較閾值與影像邊緣模型的尺寸結果~Compare dimensions from threshold and edge-model methods|尺寸定義與演算法設定具有一致性~Dimension definitions and algorithm settings are consistent|演算法更換可造成非物理的線寬跳變~Algorithm changes can cause nonphysical CD jumps
電子束量測擾動~Assess electron-beam measurement effects|比較連續掃描前後的敏感圖形~Compare sensitive patterns before and after repeated scans|重測未導致可辨識尺寸或充電改變~Repeated scanning causes no discernible size or charging change|量測本身可能改變待測光阻~Measurement itself can alter the resist
線邊粗糙度頻譜~Analyze line-edge roughness spectra|將邊緣位置轉為空間頻率分佈~Convert edge positions into spatial-frequency distributions|粗糙度頻帶與取樣解析度一起報告~Roughness bands are reported with sampling resolution|低解析影像會濾掉高頻粗糙度~Low-resolution images suppress high-frequency roughness
光學散射模型校驗~Validate scatterometry models|對照散射模型反演與截面參考資料~Compare scatterometric inversion with sectional references|多參數解沒有未辨識的高度相關性~The solution lacks unrecognized strong parameter correlations|不同幾何可能產生相似光學光譜~Different geometries can produce similar optical spectra
橢圓偏光多層膜擬合~Fit multilayer ellipsometry|比較單層假設與實際多層膜模型~Compare a single-layer assumption with the multilayer model|模型殘差改善且參數維持物理合理~Residuals improve while parameters remain physically plausible|過多自由參數可能只是在擬合雜訊~Too many free parameters can fit noise
AFM 探針形狀影響~Assess AFM tip-shape effects|比較尖端卷積模型與量得的窄溝輪廓~Compare tip-convolution models with measured narrow trenches|可達溝底與側壁區域均明確界定~Accessible bottoms and sidewall regions are identified|探針太鈍會把窄結構量得過寬~A blunt tip can broaden narrow features
膜應力量測基準扣除~Subtract baseline in stress metrology|以同片沉積前後曲率建立差分~Use same-wafer curvature before and after deposition|差分扣除保留一致支撐及溫度條件~Baseline subtraction preserves support and temperature conditions|改變夾持條件會混入機械假訊號~Changed clamping introduces mechanical artifacts
套刻標記與產品偏差~Assess overlay-target representativeness|比較專用套刻標記與產品圖形的偏差~Compare dedicated overlay targets with product patterns|標記結果可由產品區量測支持~Target results are supported by product-area measurements|標記對準不保證實際元件對準~Aligned targets do not prove aligned device patterns
明場缺陷對比~Inspect bright-field defect contrast|比較明場影像中的圖形差異與參考晶粒~Compare bright-field pattern differences with reference dies|真正形貌異常與背景變動可區分~Physical anomalies are separated from background variation|照明差異可能增加假缺陷~Illumination differences can increase nuisance detections
暗場散射缺陷檢出~Detect dark-field scattering defects|把散射亮點與表面粒子位置比對~Match scattering spots to surface-particle locations|檢出靈敏度與背景散射一同評估~Detection sensitivity is assessed with background scatter|表面粗糙度可能被分類成顆粒~Surface roughness can be classified as particles
電子束電壓對比~Interpret e-beam voltage contrast|比較浮接與接地結構的對比圖~Compare contrast from floating and grounded structures|對比異常具有合理的電連通解釋~Contrast anomalies have a plausible connectivity explanation|充電狀態不同也可能改變亮度~Different charging states can change brightness
缺陷複判抽樣~Sample defects for review|從不同分類與尺寸群選擇複判樣本~Select review samples across defect classes and sizes|複判涵蓋少見但高風險缺陷群~Review includes rare but high-risk defect groups|只選最顯眼缺陷會造成抽樣偏誤~Selecting only conspicuous defects biases sampling
假缺陷與漏檢取捨~Balance nuisance detections and misses|比較檢出門檻改變時的驗證標籤~Compare validated labels as detection thresholds change|漏檢與誤報以同一資料集量化~Misses and false alarms are quantified on the same dataset|降低報點數不等同降低真缺陷~Fewer reported sites do not imply fewer true defects
晶圓空間變異分解~Decompose spatial wafer variation|分離徑向、方位與局部殘差特徵~Separate radial, azimuthal and local residual features|空間模型不抹除具有製程意義的群聚~The spatial model preserves process-relevant clusters|過度平滑會掩蓋局部異常~Excess smoothing hides local excursions
合理子群建立~Form rational SPC subgroups|按相近製程條件分組示意量測序列~Group measurements under similar process conditions|組內及組間變異對應明確來源~Within- and between-group variation have defined meanings|任意混批會扭曲管制界限~Arbitrary lot mixing distorts control limits
Shewhart 圖基線審查~Review Shewhart-chart baselines|從穩定歷史段計算中心與散布~Estimate center and spread from stable historical segments|特殊原因事件未被直接當成正常變異~Special-cause events are not treated as normal variation|把異常納入基線會放寬警報門檻~Including excursions widens alarm limits
EWMA 小漂移檢出~Detect small drifts with EWMA|比較移動加權指標與原始時間序列~Compare exponentially weighted indicators with raw time series|持續小偏移可與單點雜訊區分~Persistent small shifts are distinguished from isolated noise|忽略時間相關性可能產生過多警報~Ignoring autocorrelation can create excessive alarms
管制界限與規格分離~Separate control limits from specifications|將製程分布與設計容許範圍疊合~Overlay process distributions and design allowances|穩定性與符合規格分開下結論~Stability and specification compliance receive separate conclusions|穩定製程仍可能持續製造不合格品~A stable process can consistently produce nonconforming output
製程能力適用性~Assess capability-index applicability|檢查分佈形狀與穩定性再估能力~Check distribution shape and stability before estimating capability|能力指標的分佈假設明確可查~Distribution assumptions behind capability indices are explicit|不穩定資料的能力值容易誤導~Capability estimates from unstable data are misleading
虛擬量測不確定度~Assess virtual-metrology uncertainty|比較預測值、實測值與模型信賴區間~Compare predictions, measurements and model uncertainty intervals|不確定度增加時會觸發實體量測~Higher uncertainty triggers physical measurements|模型外推可能給出自信但錯誤的數值~Extrapolation can yield confident but wrong values
量測異常封鎖與復歸~Contain and clear metrology excursions|用參考片區分量測漂移與真製程漂移~Use reference wafers to separate metrology and process drift|復歸由獨立參考與產品證據共同支持~Recovery is supported by reference and product evidence|只重設警報會保留未解決根因~Resetting alarms alone preserves the unresolved cause
''')

module(18,'電性製程監控與晶圓針測','Electrical process control and wafer probing',
'電性量測必須控制接觸、漏電、溫度與儀器限制；PCM 結構用於辨識製程參數，晶粒功能測試則回答產品是否完成指定功能。',
'Electrical tests control contact quality, leakage, temperature and instrument limits; PCM structures identify process parameters while functional tests evaluate product behavior.',
['scb-probecards','scb-probesystems','scb-metrology','scb-lowlevel','scb-parameters'],r'''
探針台晶圓座標配準~Register probe-station wafer coordinates|對齊缺口、參考晶粒與探針測試座標~Align notch, reference die and probe-test coordinates|所有測試落點皆對應正確晶粒~Every test landing maps to the intended die|座標鏡射可把電性結果寫入錯晶粒~Mirrored coordinates assign results to the wrong die
探針焊墊接觸區~Inspect probe-to-pad landing|比較針痕位置與焊墊開口邊界~Compare probe marks with pad-opening boundaries|針痕留在允許區且未穿出保護邊界~Probe marks stay within the permitted pad region|邊緣落針可能造成不穩定接觸或剝膜~Edge landing can cause unstable contact or delamination
探針平面度~Assess probe coplanarity|檢視多針接觸先後與針痕深淺~Inspect contact timing and mark depth across probes|所有必要端點具相容接觸條件~All required terminals have compatible contact conditions|部分針未接觸會製造假開路~Uncontacted probes produce false opens
探針接触電阻驗證~Verify probe contact resistance|使用參考導通結構重複落針~Repeat touchdowns on reference continuity structures|接觸電阻穩定且不主導待測值~Contact resistance is stable and does not dominate the measurement|接觸漂移可能被誤判為晶片失效~Contact drift may be mistaken for device failure
探針清潔前後比較~Compare probes before and after cleaning|比較清潔前後接觸散布與針尖影像~Compare contact scatter and tip images before and after cleaning|改善可由污染減少與電阻穩定支持~Reduced contamination and stable resistance support improvement|頻繁清潔也可能加速針尖磨耗~Frequent cleaning can accelerate tip wear
溫控載台穩定性~Assess thermal-chuck stability|比較載台設定、實測與晶粒電性時間序列~Compare chuck settings, measured temperature and electrical time traces|電性擷取時溫度已達題定穩態~Temperature reaches the stated steady condition before acquisition|未穩態測試會混入溫漂~Testing before equilibrium introduces thermal drift
低電流守護與遮蔽~Assess guarding and shielding|比較守護接法前後的空載漏電~Compare open-circuit leakage with and without guarding|背景漏電小於要辨識的元件訊號~Background leakage is below the device signal of interest|量測線路漏電可能高於元件漏電~Fixture leakage can exceed device leakage
SMU 量程與限流~Select SMU range and compliance|核對示意掃描的量程與保護限制~Check measurement range and compliance in model sweeps|量測未因限流而被誤當元件特性~Compliance-limited data are not mistaken for device behavior|被截斷曲線不代表物理飽和~A clipped curve does not establish physical saturation
四端片電阻量測~Measure four-terminal sheet resistance|由不同接點組合檢查薄膜電阻~Check film resistance with different terminal combinations|引線貢獻與幾何修正分別處理~Lead contribution and geometry correction are treated separately|忽略幾何因子會把尺寸差當材料差~Ignoring geometry confuses size and material effects
閾值電壓抽取~Extract threshold voltage|在相同定義下比較轉移曲線~Compare transfer curves using the same extraction definition|各樣本使用一致且明示的閾值規則~Every sample uses the same stated threshold definition|不同抽取法可能產生不同但合理的值~Different extraction methods can yield different valid values
次臨界擺幅量測~Measure subthreshold swing|在對數電流區挑選可信線性區間~Select a credible linear region in log-current data|擬合區避開儀器底噪與強反轉~The fit avoids the noise floor and strong inversion|把底噪納入擬合會扭曲斜率~Including the noise floor distorts slope
汲極誘發能障降低~Measure drain-induced barrier lowering|比較兩種汲極偏壓下的閾值抽取~Compare threshold extraction at two drain biases|閾值變化由相同方法與溫度取得~Threshold shifts use the same method and temperature|偏壓與溫度同時改變會混淆原因~Changing bias and temperature together confounds the cause
跨導與遷移率代理量~Assess transconductance and mobility proxies|從轉移曲線求導並檢查串聯電阻~Differentiate transfer curves and inspect series resistance|跨導解釋保留幾何及串聯電阻限制~Transconductance interpretation retains geometry and resistance caveats|高跨導不能直接等同本徵遷移率~High transconductance is not directly intrinsic mobility
導通電流比較~Compare on-state current|在相同偏壓及有效寬度下比較元件~Compare devices at matched bias and effective width|比較已正規化且未受限流主導~The comparison is normalized and not compliance-limited|未正規化寬度會誤導效能排序~Unnormalized widths distort performance ranking
關斷電流量測~Measure off-state current|分離通道關斷與儀器背景漏電~Separate channel off-current from background leakage|關斷電流高於可辨識下限並有背景扣查~Off-current is measurable with background verification|背景扣除過度可能產生非物理負值~Excess background subtraction can create nonphysical negatives
閘極漏電檢查~Inspect gate leakage|對照閘電流與汲源電流的偏壓依賴~Compare bias dependence of gate and drain/source currents|漏電路徑可由端點電流關係識別~Terminal-current relationships identify the leakage path|只量總電流可能混入接面漏電~Total current can include junction leakage
接面二極體漏電~Measure junction-diode leakage|比較不同面積及周長二極體~Compare diodes with different areas and perimeters|體積與邊緣漏電貢獻可區分~Bulk-area and edge leakage contributions are distinguishable|只按面積正規化會漏掉邊緣缺陷~Area-only normalization hides perimeter defects
MOS 電容 C–V~Measure MOS capacitor C–V|比較頻率掃描的累積與耗盡區~Compare accumulation and depletion over frequency sweeps|串聯電阻及漏電影響先被檢查~Series resistance and leakage effects are checked first|非理想量測可能模仿界面陷阱~Measurement artifacts can mimic interface traps
接觸 TLM 結構~Evaluate transmission-line contact structures|比較不同間距結構的總電阻~Compare total resistance across spacing variants|線性模型適用性與截距不確定度被記錄~Model validity and intercept uncertainty are documented|不良擬合截距不能當可靠接觸電阻~A poor-fit intercept is not reliable contact resistance
導通孔链電性~Test via-chain continuity|以分段鏈結果定位跨層連接異常~Use segmented chains to localize interlevel connection anomalies|高阻段可與幾何或缺陷區相互對照~High-resistance segments map to geometry or defect regions|整體通過不能排除接近失效的尾端~Overall passing can hide near-failure tails
梳狀與蛇形互連測試~Test comb and serpentine structures|分別用梳狀測短路與蛇形測斷路~Use combs for shorts and serpentines for opens|測試結構與欲辨識故障類型相匹配~Test structures match the intended failure mode|把兩種結構混用會降低診斷能力~Confusing the structures reduces diagnostic power
環形振盪器延遲~Measure ring-oscillator delay|將振盪頻率對照級數與負载~Relate oscillation frequency to stage count and load|延遲換算使用正確拓撲與負載假設~Delay extraction uses correct topology and load assumptions|频率變動也可能源於電源或溫度~Frequency variation can also arise from supply or temperature
記憶體位元失效圖~Map memory bit failures|把位元錯誤位置還原至列行座標~Map failing bits back to row and column coordinates|列、行與孤立位元失效可分辨~Row, column and isolated-bit failures are distinguished|地址映射錯誤會製造假失效群聚~Wrong address mapping creates false failure clusters
數位掃描測試分群~Classify digital scan-test failures|比較掃描鏈與功能測試失效類型~Compare scan-chain and functional failure classes|結構性與功能性故障證據分開記錄~Structural and functional failure evidence is recorded separately|單一測試通過不代表全功能覆蓋~One passing test does not establish full functional coverage
針測重測與測試接觸區分~Separate retest recovery from contact issues|比較原測、重落針與重新測試結果~Compare original, retouch and retest outcomes|恢復案例可歸因至接觸或元件證據~Recovered cases have contact- or device-based explanations|直接以最好一次結果放行會隱藏不穩定~Passing the best result hides instability
晶圓測試分級與座標輸出~Export wafer-test bins and coordinates|核對分級規則、測試版本與晶粒地圖~Check bin rules, test revision and die-map output|每個良品判定均有可追溯測試紀錄~Every good-die decision has a traceable test record|檔案格式正確不代表座標與分級正確~A valid file format does not prove correct coordinates or bins
''')

module(19,'良率、可靠度與缺陷失效分析','Yield, reliability and failure analysis',
'良率描述指定測試下的合格比例，可靠度描述隨時間與應力演變的失效；缺陷相關性需要物理證據才能轉為根因結論。',
'Yield describes conformance under specified tests; reliability concerns failure evolution with time and stress. Defect correlations require physical evidence before becoming root-cause conclusions.',
['scb-kla','scb-spc','scb-reliability','scb-reliability-models'],r'''
良率分母與重測去重~Define yield denominators and deduplicate retests|把原始測試紀錄整理成唯一晶粒結果~Reduce test records to unique die outcomes|投入、有效測試與合格數的定義一致~Input, valid-test and pass counts use consistent definitions|重測重複計數會虛增樣本數~Counting retests repeatedly inflates sample size
失效分級 Pareto~Build a failure-bin Pareto|依互斥與重疊失效分類整理數量~Count mutually exclusive and overlapping failure classes|圖表分母與多重失效規則明示~Denominators and multiple-failure rules are explicit|把重疊類別相加可能超過總晶粒數~Summing overlapping classes can exceed the die count
晶圓環狀失效圖~Interpret ring-shaped wafer failures|比較失效環帶與製程徑向量測~Compare failing rings with radial process measurements|失效位置與候選製程機制具空間一致性~Failure locations spatially agree with the candidate mechanism|環狀圖樣不是特定機台的唯一指紋~A ring is not a unique fingerprint of one tool
刮傷型線性失效圖~Interpret scratch-like failure patterns|疊合線性失效與表面刮傷座標~Overlay linear failures and surface-scratch coordinates|實體刮傷與失效晶粒位置相關~Physical scratches correlate with failed-die locations|只靠視覺相似不足以證實因果~Visual similarity alone does not establish causality
缺陷與電性座標關聯~Correlate defects with electrical failures|把缺陷座標轉至相同晶粒與結構座標~Transform defect coordinates into the electrical-test frame|重疊率超過適當的隨機對照~Overlap exceeds an appropriate random baseline|未校正密度會高估偶然重疊~Uncorrected defect density exaggerates coincidental overlap
關鍵面積與缺陷尺寸~Relate critical area to defect size|用版圖間距估算不同尺寸缺陷的影響~Estimate defect impact from layout spacing and defect size|良率推估包含幾何敏感度~Yield estimates include geometric sensitivity|相同缺陷數不代表相同晶粒失效率~Equal defect counts do not imply equal die failure rates
隨機與群聚良率模型~Compare random and clustered yield models|對照均勻與群聚缺陷下的晶粒良率~Compare die yield under uniform and clustered defects|模型選擇符合空間分佈證據~Model choice matches spatial-distribution evidence|強群聚資料不適合直接套均勻模型~Strongly clustered data do not fit a uniform model directly
製程機台履歷交叉表~Cross-tabulate process-tool genealogy|比較共同經過機台的失效群與對照群~Compare failed and control groups sharing process tools|候選機台關聯已排查批次與時間混淆~Candidate-tool association is checked for lot and time confounding|同批共現不等同機台造成失效~Co-occurrence in a lot does not prove tool causation
分割實驗根因驗證~Validate causes with split experiments|設計僅改變候選因子的示意分組~Form model groups varying only the candidate factor|結果差異可追溯至受控的分割因子~Outcome differences trace to the controlled split factor|多因子同變使改善無法歸因~Simultaneous changes prevent attribution
失效樣本保全~Preserve failure-analysis samples|記錄分析前電性、位置與既有加工歷程~Record electrical state, location and prior processing before analysis|後續破壞分析可回溯至原始失效~Destructive analysis remains traceable to the original failure|先破壞樣本可能抹除關鍵證據~Premature destruction can erase crucial evidence
非破壞定位順序~Sequence nondestructive localization|比較電性、光學與熱影像定位結果~Compare electrical, optical and thermal localization|開封或切片前已縮小疑似區域~Suspect regions are narrowed before opening or sectioning|直接廣域切片可能錯過失效位置~Broad sectioning can miss the failure site
發光顯微定位~Localize with emission microscopy|把異常發光與電性偏壓狀態對照~Relate anomalous emission to electrical bias state|發光位置對應可重現的失效条件~Emission corresponds to a reproducible failure condition|正常元件也可能發光而造成假判~Healthy devices can also emit and mislead interpretation
熱點影像判讀~Interpret thermal hotspots|比較熱影像背景與疑似漏電路徑~Compare thermal backgrounds and suspected leakage paths|熱點與功耗異常及空間定位一致~Hotspots agree with power anomalies and localization|高導熱擴散會使熱點偏離故障源~Thermal spreading can displace the apparent hotspot
FIB 截面定位~Target FIB cross sections|以座標轉換把疑似故障切入截面~Use coordinate transforms to section the suspected defect|截面確實穿過目標故障而非鄰近正常區~The section intersects the target rather than an adjacent healthy region|切片偏移會造成找不到缺陷的假陰性~Section misplacement creates a false negative
TEM 界面證據~Assess TEM interface evidence|檢查界面晶格、空洞與樣品製備假象~Inspect lattice, voids and specimen-preparation artifacts|結構異常可與製樣損傷區分~Structural anomalies are separated from preparation damage|離子製樣可能引入非原始非晶層~Ion preparation can introduce an artificial amorphous layer
元素分析污染辨識~Identify contamination by elemental analysis|比較失效與正常位置的元素光譜~Compare elemental spectra at failed and healthy locations|額外元素與空間位置及背景一致核對~Extra species are checked against location and background|分析支架或保護層也可能貢獻訊號~Mounts or protective layers can contribute signals
閘介電時間相依崩潰~Assess time-dependent dielectric breakdown|比較示意應力時間與失效分佈~Compare model stress duration and breakdown distributions|失效定義與未失效截尾樣本一起保留~Failure definitions and censored survivors are retained|刪掉未失效样本會高估失效率~Deleting survivors overestimates failure probability
偏壓溫度不穩定性~Assess bias-temperature instability|追蹤閾值漂移與量測間隔中的恢復~Track threshold shifts and recovery during measurement delays|恢復時間被納入應力後量測紀錄~Recovery time is included in post-stress records|不同延遲量測會產生不可比漂移~Different delays produce incomparable shifts
熱載子劣化~Assess hot-carrier degradation|比較應力前後跨導與電流變化~Compare transconductance and current before and after stress|劣化指標與選定偏壓機制相容~Degradation metrics match the selected bias mechanism|單看閾值可能漏掉其他參數劣化~Threshold alone can miss other degradation
互連電遷移~Assess interconnect electromigration|關聯電阻演化、電流方向與空洞位置~Relate resistance evolution, current direction and void location|失效位置支持材料遷移的物理解釋~Failure location supports a material-transport explanation|自熱造成的可逆電阻上升不等同失效~Reversible self-heating resistance is not failure
應力誘發空洞~Assess stress-induced voiding|比較熱歷程與無外加電流的空洞演化~Compare thermal history and void growth without applied current|可區分熱機應力與電流驅動機制~Thermomechanical and current-driven mechanisms are distinguishable|所有金屬空洞都歸電遷移會誤診~Attributing every metal void to electromigration misdiagnoses it
介電層間漏電劣化~Assess intermetal dielectric degradation|比較相鄰導線間漏電與時間變化~Compare leakage between adjacent lines over time|漏電路徑對應介電隔離結構~Leakage paths correspond to dielectric isolation structures|探針污染也可能產生假線間漏電~Probe contamination can mimic interline leakage
濕氣腐蝕機制~Assess moisture-corrosion mechanisms|對照保護層缺口、污染物與腐蝕位置~Relate barrier gaps, contaminants and corrosion locations|腐蝕假說同時具有水氣路徑與材料證據~The hypothesis includes moisture pathways and material evidence|只見變色不能證明特定腐蝕機制~Discoloration alone does not prove a corrosion mechanism
加速模型外推限制~Assess accelerated-model extrapolation|比較不同應力區間的主導失效機制~Compare dominant mechanisms across stress ranges|外推只涵蓋已支持的同一機制區間~Extrapolation stays within supported mechanism consistency|高應力可能切換機制使外推失效~High stress can switch mechanisms and invalidate extrapolation
修正後獨立驗證~Independently verify corrective action|用未參與調整的對照樣本檢查改善~Use samples excluded from tuning to verify improvement|改善可跨獨立批次與指標重現~Improvement reproduces across independent lots and metrics|重用調整資料會過度樂觀估計效果~Reusing tuning data overstates improvement
良率與可靠度聯合結案~Close yield and reliability investigations|對照即時合格率與受應力後的失效證據~Compare initial conformance and post-stress failures|即時良率與長期機制風險分別結論~Initial yield and longer-term mechanism risks have separate conclusions|提高出貨良率不代表壽命已改善~Higher shipment yield does not establish better lifetime
''')

module(20,'先進電晶體、背面供電與製造交接','Advanced transistors, backside power and handoff',
'本模組是互斥或可組合架構的比較分支：FinFET、GAA 與背面供電並非每條製程都同時存在；學習順序不等於實際晶圓行程。',
'This module compares alternative or combinable architectures: FinFETs, GAA and backside power do not occur together in every flow. Learning order is not a wafer traveler.',
['scb-nanosheet','scb-backside','scb-backside-dtco','scb-epi','scb-metrology'],r'''
FinFET 鰭寬與高度~Measure FinFET fin width and height|從立體截面比較有效通道尺寸~Compare effective channel dimensions in 3D sections|鰭寬與暴露高度分別量化~Fin width and exposed height are quantified separately|單一俯視尺寸不能代表通道總寬~One top-view dimension cannot represent total channel width
FinFET 隔離層凹回~Assess FinFET isolation recess|標示隔離層頂部與鰭側壁暴露範圍~Mark isolation height and exposed fin sidewalls|有效鰭高與隔離功能同時滿足需求~Effective fin height and isolation requirements are both met|凹回過深可能增加不希望的寄生通道~Excess recess can expose unwanted parasitic channels
FinFET 閘極包覆~Inspect FinFET gate wrapping|比較鰭頂及兩側閘介電層連續性~Compare gate-dielectric continuity on the fin top and sides|三面通道的閘控覆蓋可被驗證~Gate coverage over the three channel faces is verifiable|鰭頂完整不能保證側壁界面品質~An intact fin top does not prove good sidewall interfaces
FinFET 多鰭匹配~Assess matching across multiple fins|比較同一元件內各鰭的尺寸及連接~Compare dimensions and connections of fins within one device|每根鰭皆對有效電流提供可解釋貢獻~Each fin makes an explainable contribution to effective current|單根缺陷可被總電流平均掩蓋~One defective fin can be hidden by total current
GAA 交替外延堆疊~Inspect alternating GAA epitaxial layers|辨認通道層與犧牲層的週期結構~Identify channel and sacrificial layers in the periodic stack|層序與材料區分符合釋放路線~Layer order and material identity match the release route|層序錯誤會破壞選擇性釋放假設~Wrong layer order invalidates selective-release assumptions
奈米片厚度匹配~Assess nanosheet thickness matching|逐層量取奈米片厚度及片間間距~Measure each nanosheet thickness and intersheet spacing|不同高度奈米片的差異均被量化~Differences among sheets at different heights are quantified|平均厚度會掩蓋最薄奈米片~Average thickness conceals the thinnest sheet
GAA 堆疊圖形邊壁~Inspect patterned GAA stack sidewalls|比較交替材料側壁的蝕刻偏差~Compare sidewall etch bias across alternating materials|材料交界未形成非預期凸凹輪廓~Interfaces lack unintended protrusions or recesses|不同材料速率差可形成鋸齒側壁~Different material rates can produce serrated sidewalls
內間隔層犧牲層凹蝕~Assess inner-spacer recess|標示犧牲層端部的選擇性橫向凹蝕~Map selective lateral recess at sacrificial-layer ends|凹蝕長度兼顧閘極隔離與通道保存~Recess length balances gate isolation and channel preservation|凹蝕侵入通道層會削弱奈米片~Recess into the channel layer weakens nanosheets
內間隔介電填充~Inspect inner-spacer dielectric filling|比較凹槽內填充與外部殘膜~Compare cavity fill and external dielectric residue|內部隔離連續且外部接觸區可清除~Internal isolation is continuous and external contacts remain clearable|內間隔空隙可能造成閘源汲耦合異常~Inner-spacer gaps can disturb gate–source/drain coupling
內間隔回蝕邊界~Assess inner-spacer etchback boundaries|辨認應保留內層與應移除外膜~Identify retained inner dielectric and removable outer film|隔離留在凹槽而源汲極成長面開放~Isolation remains in recesses while growth surfaces are exposed|過度回蝕會削弱內間隔隔離~Excess etchback weakens inner-spacer isolation
GAA 源汲極片端連接~Inspect GAA sheet-end junction connections|追蹤各奈米片與源汲極外延的接合~Trace each nanosheet connection to source/drain epitaxy|每片通道均具有連續源汲極連接~Each channel sheet has continuous source/drain connections|下層接合缺陷可能被上層截面漏掉~Upper sections can miss defective lower-sheet junctions
犧牲層選擇性釋放~Assess selective sacrificial-layer release|比較犧牲材料殘留與通道材料損失~Compare sacrificial residue and channel-material loss|通道可自由包覆且自身厚度保留~Channels become accessible while retaining their thickness|完全去犧牲層不代表通道未被侵蝕~Complete release does not prove undamaged channels
奈米片機械下垂~Inspect nanosheet sagging|量取釋放後奈米片形狀與相鄰間距~Measure released-sheet shape and neighboring gaps|奈米片未接觸彼此或支撐結構~Sheets do not touch neighboring sheets or supports|毛細或殘餘應力可能引起黏附~Capillary or residual stress can cause sticking
環繞閘介電共形覆蓋~Assess wraparound gate-dielectric coverage|追蹤奈米片上、下與側面的薄膜~Trace films above, below and beside each nanosheet|全部閘控表面均有連續介電隔離~All gate-controlled surfaces have continuous dielectric isolation|只看頂面無法驗證下表面品質~Top-surface inspection cannot verify underside quality
片間金屬閘填充~Inspect intersheet metal-gate filling|比較片間剩餘空間與金屬填充截面~Compare remaining intersheet space and gate-fill sections|金屬連續且未封住尚未填充的深處~Metal stays continuous without trapping unfilled deep regions|狹窄片間空間增加封口空洞風險~Narrow intersheet spaces increase pinch-off void risk
GAA 閾值分支與功函數~Assess GAA work-function branches|對照功函數層分支與元件閾值分佈~Compare work-function branches and threshold distributions|閾值差異與實際閘堆疊分支相符~Threshold differences match the actual gate-stack branch|用通道尺寸差補償可能掩蓋材料問題~Geometry compensation can conceal a material problem
背面供電拓撲選擇~Select backside-power connectivity topology|比較埋入電源軌與直接背接觸示意~Compare buried-rail and direct-backside-contact schemes|每條電源路徑都有明確接觸對象~Each power path has an explicit landing target|把兩種拓撲混接會產生無效連接~Mixing the topologies produces invalid connections
背面加工載板支撐~Assess carriers for backside processing|在背面路線中標示正面接合及承載結構~Map frontside bonding and support in the backside flow|薄化與後續加工期間有連續承載路徑~Support is maintained through thinning and subsequent processing|暫時載板條件不合可損害前端結構~Unsuitable carrier conditions can damage frontside devices
背面殘矽終點~Determine residual-silicon endpoints|對照背面薄化深度與目標接觸位置~Compare thinning depth with intended contact locations|保留厚度足以暴露目標且避免元件損傷~Remaining thickness enables target access without device damage|單看平均厚度會漏掉局部過薄~Mean thickness misses local overthinning
背正面套刻驗證~Verify backside-to-frontside overlay|將背面標記轉換到前端元件座標~Transform backside marks into frontside device coordinates|最差偏差仍讓導通孔落在允許區~Worst-case error keeps vias inside permitted landings|背面鏡像關係處理錯誤會全面錯位~Incorrect backside mirroring causes systematic misalignment
奈米導通孔隔離與落點~Inspect nano-via isolation and landing|同時檢查孔壁介電與底部導電連接~Inspect via-wall dielectric and bottom electrical connection|側壁隔離與底部導通同時成立~Sidewalls isolate while the bottom conducts|全面金屬接觸可能造成基板短路~Unisolated metal contact can short the substrate
背面配線電壓降~Assess backside-wiring voltage drop|比較前端與背面供電模型的節點電壓~Compare node voltages in frontside and backside power models|改善來自明示電阻與電流路徑改變~Improvement follows explicit resistance and path changes|只縮短路徑不能忽略接觸電阻~A shorter path does not remove contact resistance
背面製程對前端影響~Assess backside-process impact on devices|比較背面加工前後同一批元件電性~Compare matched devices before and after backside processing|差分檢查涵蓋閾值、漏電及導通~Paired checks include threshold, leakage and conduction|平均不變仍可能有局部尾端劣化~An unchanged mean can hide local tail degradation
製程路線與結構證據交接~Handoff route and structural evidence|把選用分支、剖面及材料標記綁定同一版本~Bind selected branches, sections and material labels to one revision|交接圖與實際分支沒有互斥結構混搭~Handoff diagrams do not mix mutually exclusive structures|漂亮總圖可能包含未製作的分支~A polished overview may include unbuilt branches
晶圓放行電性封存~Freeze wafer-release electrical evidence|核對 PCM、晶粒分級與可追溯測試版本~Reconcile PCM, die bins and traceable test revisions|最終放行使用同一晶圓與有效版本結果~Release uses the same wafer and valid result revisions|新舊測試混用會破壞放行可重現性~Mixing revisions makes release decisions irreproducible
良品晶圓製造交接~Handoff qualified wafers|整合缺陷位置、封裝介面與未結案限制~Combine defect locations, packaging interfaces and open restrictions|接收端可重建良品判定及剩餘限制~The receiver can reconstruct good-die decisions and remaining limits|只有合格標籤而無證據不足以交接~A pass label without evidence is insufficient for handoff
''')

# Source pages were retrieved through web search on 2026-10-12. They support
# principles and terminology, not every authored exercise or an exact factory SOP.
SOURCE_ROWS=[
('scb-modify','Materials Modification','https://www.appliedmaterials.com/us/en/semiconductor/products/modify.html','Applied Materials','佈植、晶格損傷與熱處理原理'),
('scb-epi','Epitaxy','https://www.appliedmaterials.com/us/en/semiconductor/products/processes/epitaxy.html','Applied Materials','選擇性外延、摻雜與應變工程'),
('scb-silicide','Endura ALPS PVD (ALPS Co & Ni)','https://www.appliedmaterials.com/us/en/product-library/endura-alps-pvd-alps-co-ni.html','Applied Materials','矽化物與接觸金屬沉積原理'),
('scb-cobalt','Cobalt Product Suite','https://www.appliedmaterials.com/us/en/product-library/cobalt-product-suite.html','Applied Materials','接觸及互連材料整合分支'),
('scb-metallization','Metallization','https://www.lamresearch.com/products/our-solutions/metallization/','Lam Research','金屬沉積、成核與材料選擇'),
('scb-deposition','Deposition','https://www.lamresearch.com/products/our-processes/deposition/','Lam Research','導體及介電層沉積的基本功能'),
('scb-cmp','Shape','https://www.appliedmaterials.com/us/en/semiconductor/products/shape.html','Applied Materials','CMP 與選擇性材料去除原理'),
('scb-interconnect','Tech Brief: An Introduction to Interconnects','https://newsroom.lamresearch.com/Tech-Brief-An-Introduction-to-Interconnects','Lam Research','鑲嵌式互連基本流程與功能'),
('scb-lam-interconnect','Interconnect Solutions','https://www.lamresearch.com/products/our-solutions/interconnect-solutions/','Lam Research','互連介電、蝕刻與填充整合背景'),
('scb-electroplating','Tech Brief: Elements of Electroplating','https://newsroom.lamresearch.com/Tech-Brief-Elements-of-Electroplating','Lam Research','阻障、種子層與電化學填充原理'),
('scb-kla','Chip Manufacturing 101','https://www.kla.com/wp-content/uploads/ChipManufacturing101.pdf','KLA','檢查、量測與資料分析的分工'),
('scb-metrology','Metrology Program','https://www.nist.gov/chips/research-development-programs/metrology-program','NIST','半導體量測的準確性、精密度及適用性'),
('scb-spc','What are Process Control Techniques?','https://www.itl.nist.gov/div898/handbook/pmc/section1/pmc12.htm','NIST/SEMATECH','SPC、Shewhart、EWMA 與基線管制概念'),
('scb-virtual','A Comparative Study of Semiconductor Virtual Metrology Methods and Novel Algorithmic Framework for Dynamic Sampling','https://www.nist.gov/publications/comparative-study-semiconductor-virtual-metrology-methods-and-novel-algorithmic','NIST','虛擬量測漂移、不確定度及動態取樣'),
('scb-probecards','Probe Cards','https://www.formfactor.com/products/probe-cards/','FormFactor','線上與完工參數測試及探針接觸'),
('scb-probesystems','Advanced Probe Systems','https://www.formfactor.com/products/probe-systems/high-performance-probe-systems/','FormFactor','晶圓電性量測、參數測試與失效分析平台'),
('scb-grinding','Ultra-Thin Grinding','https://www.disco.co.jp/eg/solution/library/grinder/thin.html','DISCO','晶圓薄化、支撐與邊緣完整性'),
('scb-stressrelief','Dry Polishing (Stress Relief)','https://www.disco.co.jp/eg/solution/library/polisher/strelief.html','DISCO','研磨損傷層與應力消除原理'),
('scb-reliability','Reliability','https://www.ti.com/quality-reliability/reliability.html','Texas Instruments','半導體可靠度設計與驗證背景'),
('scb-reliability-models','Reliability calculators','https://www.ti.com/quality-reliability/reliability/calculators.html','Texas Instruments','電遷移、介電崩潰及壽命分佈模型背景'),
('scb-nanosheet','Entering the nanosheet transistor era','https://www.imec-int.com/en/articles/entering-nanosheet-transistor-era-0','imec','GAA 奈米片與內間隔層整合原理'),
('scb-backside','Backside power delivery','https://www.imec-int.com/en/articles/how-power-chips-backside','imec','背面供電、薄化及奈米導通孔架構'),
('scb-backside-dtco','Backside power delivery options: a DTCO study','https://www.imec-int.com/en/articles/backside-power-delivery-options-dtco-study','imec','埋入電源軌與直接背接觸的架構分支'),
('scb-cdsem','Critical Dimension Metrology in the Scanning Electron Microscope','https://www.nist.gov/publications/critical-dimension-metrology-scanning-electron-microscope','NIST','CD-SEM 尺寸量測與影像解讀'),
('scb-afm','Atomic-force microscopy','https://www.nist.gov/programs-projects/atomic-force-microscopy','NIST','探針形狀、側壁及奈米尺寸量測'),
('scb-lowlevel','Keithley Low Level Measurements Handbook, 7th Edition','https://www.tek.com/en/documents/product-article/keithley-low-level-measurements-handbook---7th-edition','Tektronix / Keithley','低電流、守護、漏電及四端電阻量測'),
('scb-parameters','Parameter Analyzers','https://www.keysight.com/zz/en/products/semiconductors/parameter-analyzers.html','Keysight Technologies','元件 IV、CV、閾值、關斷電流與參數量測範圍'),
]

# Normalize stray simplified glyphs in authoring rows without altering English.
TRAD=str.maketrans({
'体':'體','较':'較','导':'導','频':'頻','电':'電','图':'圖','触':'觸','层':'層','线':'線','数':'數',
'样':'樣','归':'歸','读':'讀','开':'開','宽':'寬','计':'計','与':'與','损':'損','杂':'雜','测':'測',
'边':'邊','显':'顯','径':'徑','环':'環','变':'變','连':'連','标':'標','对':'對','录':'錄','极':'極',
'间':'間','类':'類','识':'識','转':'轉','异':'異','时':'時','净':'淨','终':'終','条':'條','缘':'緣',
'负':'負','载':'載','链':'鏈','独':'獨','组':'組','预':'預','据':'據','稳':'穩','续':'續'
})
def tc(text):return text.translate(TRAD).replace('后续','後續').replace('判读','判讀').replace('比对','比對')

stages=[]
all_steps=[]
for num,(title,title_en,concept,concept_en,source_ids,raw) in sorted(MODULES.items()):
    rows=[]
    for line in raw.strip().splitlines():
        cols=line.split('|')
        assert len(cols)==4,(num,line)
        pairs=[col.split('~') for col in cols]
        assert all(len(p)==2 for p in pairs),(num,line)
        rows.append([(tc(zh),en) for zh,en in pairs])
    assert len(rows)==26,(num,len(rows))
    stage={'id':f'sc-m{num:02d}','title':tc(title),'titleEn':title_en,
      'description':tc(concept)+' 本模組以示意模型、截面判讀及量測資料完成教學任務；此順序為學習編排，不是可直接執行的晶圓製造行程。',
      'descriptionEn':concept_en+' Exercises use models, cross sections and measurement datasets. The ordering is pedagogical, not an executable wafer traveler.',
      'sourceIds':source_ids,'simulationOnly':True,'steps':[]}
    for index,(names,actions,evidence,diagnosis) in enumerate(rows):
        n=(num-1)*26+index+1
        sid=f'sc-{n:03d}'
        name,name_en=names;action,action_en=actions;ev,ev_en=evidence;diag,diag_en=diagnosis
        # Competing answers are real evidence from different operations in the
        # same module: the learner must choose the measurement for this task.
        distractors=[rows[(index+7)%26][2],rows[(index+13)%26][2]]
        choices=[evidence,*distractors]
        rotation=n%3
        choices=choices[-rotation:]+choices[:-rotation] if rotation else choices
        answer=next(i for i,c in enumerate(choices) if c==evidence)
        step={'id':sid,'title':name,'titleEn':name_en,
          'objective':f'完成「{name}」的證據判讀，辨識『{action}』所涉及的物理量與整合限制。',
          'objectiveEn':f'Evaluate {name_en.lower()} by identifying the physical quantities and integration limits involved in this task: {action_en.lower()}.',
          'instruction':f'以工程概念模型，或另行提供且已審查的示意截面／量測資料，{action}。標出比較基準與量測位置並保留判讀依據；未掛接資料或未給允收數值時，標記定量驗證未完成，不自行編造機台參數。',
          'instructionEn':f'Using an engineering concept model, or a separately supplied and reviewed section or measurement dataset, {action_en[0].lower()+action_en[1:]}. Mark the comparison baseline and measurement locations. If data or numerical acceptance limits are unavailable, mark quantitative validation incomplete rather than inventing tool settings.',
          'observation':f'觀察與驗證重點：{ev}。這是要檢查的證據條件，並非宣稱已取得真實工廠量測結果。',
          'observationEn':f'Observation and validation target: {ev_en[0].lower()+ev_en[1:]}. This is an evidence criterion, not a claim of measured factory results.',
          'failure':f'診斷提醒：{diag}。先用本工序的物理證據確認，再考慮修改上游假設。',
          'failureEn':f'Diagnostic consideration: {diag_en[0].lower()+diag_en[1:]}. Confirm this with physical evidence before revising upstream assumptions.',
          'check':f'提交一項能支持「{ev}」的標註圖或量測表；再指出「{diag}」會如何改變判讀。資料缺漏時保持未放行狀態。',
          'checkEn':f'Submit an annotated figure or measurement table supporting this criterion: {ev_en}. Then explain the implication of this diagnostic caveat: {diag_en}. Keep the task unreleased if evidence is missing.',
          'knowledge':[
            {'id':sid+'-k1','title':f'{name}的物理定位','titleEn':f'Physical role of {name_en.lower()}',
             'text':tc(concept)+f' 本題具體操作為「{action}」，應先分辨施加的條件、實際量到的變量與推論出的性質。',
             'textEn':concept_en+f' Here the concrete task is: {action_en}. Distinguish imposed conditions, measured variables and inferred properties.'},
            {'id':sid+'-k2','title':f'{name}的證據與失效','titleEn':f'Evidence and failure modes for {name_en.lower()}',
             'text':f'有效證據需支持「{ev}」。但{diag}；因此單一漂亮影像或平均值不能自動取代對本工序目標的檢驗。',
             'textEn':f'Evidence should establish the following: {ev_en}. However, {diag_en[0].lower()+diag_en[1:]}; an attractive image or a mean value cannot automatically substitute for a task-specific check.'}
          ],
          'quiz':{'question':f'哪一項證據最直接支持「{name}」這一道教學工序的判定？','questionEn':f'Which evidence most directly supports acceptance for {name_en.lower()}?',
             'options':[c[0] for c in choices],'optionsEn':[c[1] for c in choices],'answer':answer,
             'explanation':f'本題操作是「{action}」，因此直接證據是「{ev}」。其他選項屬本模組其他工序，不能單独取代此項檢查；另需留意：{diag}。',
             'explanationEn':f'The task is to {action_en[0].lower()+action_en[1:]}; the direct criterion is: {ev_en}. The alternatives concern other operations and cannot alone replace this check. Also note: {diag_en}.'},
          'sourceIds':source_ids,'simulationOnly':True,'estimatedMinutes':8+2*(n%4),'sequence':n,'order':index+1,
          'prerequisiteIds':[f'sc-{n-1:03d}'],
          'routeNote':'教育順序；實際晶圓依選定製程分支、核准規格及合格設備行程執行。',
          'routeNoteEn':'Educational ordering; actual wafers follow selected integration branches, approved specifications and qualified equipment travelers.'}
        # Convert every Chinese-only field after constructing reusable phrases.
        for key in ('objective','instruction','observation','failure','check','routeNote'):step[key]=tc(step[key])
        step['quiz']['explanation']=tc(step['quiz']['explanation'])
        stage['steps'].append(step);all_steps.append(step)
    stages.append(stage)

sources=[{'id':i,'title':title,'url':url,'publisher':publisher,
  'scope':scope+'。第一手來源支援原理、術語及技術背景；本課程的操作拆解、驗收題與診斷提示為原創教學設計，不代表該來源提供完整 SOP、製程參數或逐項驗證。'} for i,title,url,publisher,scope in SOURCE_ROWS]
assert len(stages)==10 and len(all_steps)==260
assert [s['id'] for s in all_steps]==[f'sc-{i:03d}' for i in range(261,521)]
assert len({s['title'] for s in all_steps})==260
assert len({s['titleEn'] for s in all_steps})==260
assert len({s['instruction'] for s in all_steps})==260
assert len({s['observation'] for s in all_steps})==260
assert len({s['failure'] for s in all_steps})==260
assert all(len(set(s['quiz']['options']))==3 and len(set(s['quiz']['optionsEn']))==3 for s in all_steps)
known={s['id'] for s in sources}
assert all(set(s['sourceIds'])<=known for s in all_steps)
assert len(sources)>=10
ROOT.joinpath('semiconductor_b.json').write_text(json.dumps(stages,ensure_ascii=False,indent=2)+'\n')
ROOT.joinpath('sources_semiconductor_b.json').write_text(json.dumps(sources,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'stages':len(stages),'steps':len(all_steps),'range':[all_steps[0]['id'],all_steps[-1]['id']],'sources':len(sources),'uniqueActions':260,'uniqueEvidence':260,'uniqueDiagnostics':260}))
