#!/usr/bin/env python3
"""Original bilingual educational work packages, not manufacturing recipes.
Each course's 24 investigations and conclusions are individually authored below.
Shared formatting does not imply a qualified equipment operating procedure.
"""
import json, copy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
CAT={x['id']:x for x in json.loads((ROOT/'public/academy/data/catalog.json').read_text())}
DATA={}
def add(cid,stage_names,stage_principles,stage_errors,rows,refs,neighbors,place='imec'):
    rows=[x.split('|') for x in rows.strip().splitlines() if x.strip()]
    assert len(rows)==24,(cid,len(rows))
    assert all(len(x)==4 for x in rows),(cid,'fields')
    DATA[cid]=dict(stages=stage_names,principles=stage_principles,errors=stage_errors,rows=rows,refs=refs,neighbors=neighbors,place=place)

add('a034',
['吸收與反應路徑|Absorption and reaction','塗膜與表面|Coating and surfaces','曝光與統計|Exposure and statistics','轉移與驗證|Transfer and validation'],
['金屬氧化物光阻的吸收、配體反應與不溶化必須分開驗證。|Absorption, ligand reactions and insolubilization require separate evidence in metal-oxide resists.','薄膜厚度與組成會同時影響吸收、顆粒及顯影結果。|Film thickness and composition affect absorption, particles and development together.','平均線寬不能取代斷線與橋接等罕見事件的統計。|Mean linewidth cannot replace rare-event statistics for breaks and bridges.','光阻圖案、硬罩圖案與金屬電性是不同驗證層次。|Resist patterns, hard-mask patterns and metal electrical behavior are distinct validation levels.'],
['吸收更多就必定具有較低缺陷。|Greater absorption necessarily guarantees fewer defects.','相同厚度就表示化學組成相同。|Equal thickness proves equal chemical composition.','只看平均線寬即可排除罕見缺陷。|Mean linewidth alone rules out rare defects.','光阻影像正常即可保證互連導通。|A good resist image guarantees conductive interconnects.'],
'''
畫出光子到溶解度的因果鏈|Trace photons to changed solubility|吸收與化學轉換不是同一事件。|Absorption and chemical conversion are different events.
比較有機與金屬氧化物光阻的元素角色|Compare elemental roles in organic and metal-oxide resists|材料分類不能單獨預測感度。|Material class alone does not predict sensitivity.
分開金屬核心與配體的功能|Separate metal-core and ligand functions|配體會改變成膜及曝光後反應。|Ligands affect film formation and post-exposure reactions.
以假設吸收係數計算厚度衰減|Calculate attenuation using an assumed absorption coefficient|Beer–Lambert 模型須標明均勻薄膜假設。|Beer–Lambert modeling assumes a uniform film.
將曝光反應與烘烤反應分欄|Separate exposure and bake reactions|後曝光歷程可能改變最終溶解度。|Post-exposure history can alter final solubility.
建立配方批次與量測追溯表|Build a formulation-batch measurement ledger|批次差異不能全歸因於曝光機。|Batch variation cannot all be attributed to the scanner.
繪製中心到邊緣的膜厚取樣網格|Map center-to-edge film-thickness sampling|單點膜厚無法證明晶圓均勻性。|One thickness point cannot establish wafer uniformity.
比較兩種底層上的接觸角證據|Compare wetting evidence on two underlayers|表面能會影響潤濕與缺陷。|Surface energy influences wetting and defects.
用空白片分辨顆粒與圖案缺陷|Distinguish particles from pattern defects using blanks|曝光前缺陷可在後續被放大。|Pre-exposure defects can be amplified downstream.
對照曝光前後的光譜變化|Compare spectra before and after exposure|光譜改變需要對應可辨識的化學訊號。|Spectral changes need an identifiable chemical assignment.
規畫金屬污染與交叉污染監控|Plan metal and cross-contamination monitoring|成像材料的金屬含量也構成整合問題。|Metal content creates an integration issue as well as an imaging opportunity.
建立膜厚與顯影殘留的對照圖|Relate film thickness to development residue|殘留可能來自不完全溶解或底層相容性。|Residue can reflect incomplete dissolution or underlayer compatibility.
設計劑量與焦距的二維矩陣|Design a dose–focus matrix|最佳單點不等於具有寬製程窗口。|An optimum point is not a broad process window.
分別標記正負光阻的保留區|Mark retained regions for positive and negative tones|顯影後保留區取決於反應與顯影機制。|Retention depends on reaction and development mechanism.
量測邊緣粗糙度並標示取樣長度|Measure edge roughness with a stated sampling length|粗糙度數值受量測頻寬與取樣影響。|Roughness values depend on bandwidth and sampling.
統計斷線與橋接的個別發生率|Count breaks and bridges separately|兩種缺陷可能對劑量有不同趨勢。|The two defect types can have different dose trends.
為零缺陷樣本計算統計上限|Estimate an upper bound for zero observed defects|零觀察不等於真實發生率為零。|Zero observations do not imply a zero true rate.
比較相同線寬下的不同曝光條件|Compare exposure conditions at matched linewidth|同線寬比較可減少幾何混淆。|Matched linewidth reduces geometric confounding.
追蹤光阻到硬罩的尺寸偏差|Trace dimensional bias from resist to hard mask|蝕刻可能放大或縮小原始粗糙度。|Etching can amplify or reduce initial roughness.
檢查薄光阻的遮罩消耗預算|Check the consumption budget of a thin resist mask|薄膜提升圖案穩定性仍須滿足轉移耐受性。|Thin films still require sufficient transfer resistance.
將蛇形線導通對應至斷線位置|Relate serpentine continuity to break locations|電性測試與影像提供互補證據。|Electrical tests and images provide complementary evidence.
將梳狀漏電對應至橋接位置|Relate comb leakage to bridge locations|橋接缺陷的危害取決於網路連接。|The impact of a bridge depends on network connectivity.
比較研究展示與可量產證據|Distinguish research demonstrations from production evidence|局部良率不能代表整個產品的良率。|Local yield is not whole-product yield.
提出包含化學、圖形與電性的材料審查|Review chemistry, pattern and electrical evidence together|材料選擇應由多層證據支持。|Material selection needs multiple levels of evidence.
''',['mor','pattern','stochastic','euvyield'],['a033','a050'])

add('a035',
['資料與尺度|Data and scale','束流與定位|Beam and placement','劑量與拼接|Dose and stitching','光罩驗收|Mask acceptance'],
['光罩寫入誤差經投影縮小後仍參與晶圓邊緣位置誤差。|Mask-writing errors remain part of wafer edge-placement error after projection reduction.','束斑尺寸、位置與電流穩定度是不同性能量。|Spot size, position and current stability are distinct metrics.','局部散射與跨場拼接需分別建模。|Local scattering and field stitching require separate models.','光罩幾何合格仍須驗證實際成像。|A geometrically acceptable mask still needs imaging verification.'],
['把晶圓尺寸直接當作光罩尺寸。|Use wafer dimensions directly as mask dimensions.','較小束斑必定代表較高吞吐量。|A smaller beam spot necessarily means higher throughput.','平均劑量相同即可忽略拼接。|Equal mean dose makes stitching irrelevant.','只測一個位置即可批准全片光罩。|One measured site is sufficient to accept a whole mask.'],
'''
將晶圓目標依縮小倍率轉成光罩座標|Convert wafer targets into mask coordinates using reduction|光罩與晶圓座標必須註明尺度。|Mask and wafer coordinates require explicit scales.
檢查版圖多邊形的自交與空隙|Check layout polygons for self-intersections and gaps|資料拓樸錯誤可能形成可印缺陷。|Topology errors can become printable defects.
將曲線分割成允許的寫入圖元|Fracture curves into allowed writing primitives|資料分割會影響邊緣誤差與寫入時間。|Fracturing affects edge error and writing time.
比較可變形束與多束寫入資料流|Compare variable-shaped and multibeam data flows|平行化改變資料與校正需求。|Parallelism changes data and calibration demands.
建立關鍵圖形的寫入優先檢查清單|Prioritize critical patterns for writing checks|接點與線端可能比大面積區更敏感。|Contacts and line ends may be more sensitive than broad regions.
追蹤設計版號到光罩工作單|Trace design revision into the mask job|幾何正確但版號錯誤仍是不合格。|Correct geometry with the wrong revision is still unacceptable.
分別估算束流與駐留時間的劑量|Estimate dose from beam current and dwell time|劑量是電荷除以曝光面積。|Dose is charge divided by exposed area.
以法拉第杯量測概念檢查電流漂移|Use a Faraday-cup model to assess current drift|電流漂移會造成曝光量的時間偏差。|Current drift produces time-dependent dose error.
繪製載台誤差與偏轉誤差的分工|Separate stage and deflection errors|大行程定位與小視場偏轉具有不同誤差來源。|Long-range positioning and field deflection have different error sources.
以標記網格擬合旋轉與縮放|Fit rotation and scale from a mark grid|至少需要足夠獨立標記約束模型。|The model needs sufficient independent marks.
比較熱漂移前後的座標殘差|Compare coordinate residuals before and after thermal drift|慢漂移不會由單次校正永久消除。|One calibration does not permanently remove slow drift.
檢查絕緣基板充電造成的偏移|Assess displacement caused by insulating-substrate charging|充電會改變電子軌跡與局部曝光。|Charging alters trajectories and local exposure.
畫出前向與背向散射的作用範圍|Sketch forward- and backscatter ranges|鄰近效應包含不同空間尺度。|Proximity effects span different spatial scales.
為密集與孤立圖形比較劑量修正|Compare dose correction for dense and isolated features|相同直接劑量不代表相同總沉積能量。|Equal direct dose does not imply equal deposited energy.
量測跨寫入場的接縫|Measure seams across writing fields|場內尺寸與跨場拼接需分開報告。|Within-field size and across-field stitching need separate reporting.
比較單次與多次分攤曝光|Compare single-pass and divided-pass writing|多次曝光能平均部分誤差但增加時間。|Multiple passes can average some errors while adding time.
估算圖元數與移動時間的吞吐量|Estimate throughput from shot count and movement overhead|吞吐量不能只用束流大小推算。|Beam current alone cannot predict throughput.
保留寫入中斷後的接續驗證紀錄|Plan verification after a writing interruption|中斷前後可能有漂移與重複曝光。|Interruptions can introduce drift and repeated exposure.
對照顯影前後的線寬偏差|Compare linewidth bias introduced by development|電子束寫入不是最終光罩幾何的唯一來源。|Beam writing is not the sole source of final mask geometry.
檢查光罩蝕刻造成的邊緣位移|Assess edge displacement from mask etching|蝕刻偏差須與曝光偏差分離。|Etch bias must be separated from exposure bias.
建立全片定位誤差向量圖|Create a full-mask placement-error vector map|全片系統誤差可能與局部隨機誤差並存。|Global systematic errors can coexist with local random errors.
將光罩缺陷送入可印性判讀|Evaluate mask defects for printability|可見缺陷不一定同樣影響晶圓圖形。|Visible defects do not all affect wafer patterns equally.
建立修補後再次量測的關卡|Define remeasurement gates after repair|修補本身可能改變鄰近區域。|Repair can modify neighboring regions.
交付資料、曝光與量測的完整鏈結|Deliver a linked data-writing-metrology record|追溯性讓異常能回到對應來源。|Traceability links anomalies to their sources.
''',['jeol','maskmetro','maskrepair','comp'],'a036 a047'.split(),'nist')

add('a036',
['缺陷與成像|Defects and imaging','定位與分類|Localization and classification','修補策略|Repair strategy','再驗證|Requalification'],
['缺陷分類須同時包括幾何、相位與可印性。|Defect classification must include geometry, phase and printability.','檢查的靈敏度與誤報率有取捨。|Inspection sensitivity trades against false-positive rate.','添加與移除材料的修補有不同副作用。|Additive and subtractive repair have different side effects.','修補成功以成像及定位證據判定，不只看修補區照片。|Repair success requires imaging and placement evidence, not merely a repair image.'],
['所有小顆粒都一定可忽略。|All small particles are negligible.','檢查未報警就等於沒有任何缺陷。|No inspection alarm proves there are no defects.','修補深度越大越可靠。|Deeper repair is always more reliable.','外觀平整即代表相位正確。|A smooth appearance proves correct phase.'],
'''
把透明、遮光與相位缺陷分欄|Separate clear, opaque and phase defects|三者對光場的作用不同。|The three classes affect the optical field differently.
比較光罩缺陷與晶圓重複缺陷|Compare mask defects with repeating wafer defects|光罩缺陷可能在多個晶粒重複。|Mask defects can repeat across dies.
標記多層膜下方與吸收層缺陷|Distinguish buried multilayer from absorber defects|缺陷深度改變修補可行性。|Defect depth changes repair feasibility.
畫出缺陷位置相對於線端的關係|Locate defects relative to line ends|相同缺陷在不同圖形位置可有不同危害。|Identical defects can have different impacts at different pattern locations.
比較光強缺陷與相位缺陷的空中像|Compare intensity- and phase-defect aerial images|相位擾動可在外觀不明顯時影響成像。|Phase perturbations can affect imaging without obvious surface contrast.
定義缺陷分級需要的證據|Define evidence for defect disposition|缺陷尺寸不是唯一分級指標。|Size is not the only disposition metric.
建立檢查座標到修補座標的轉換|Transform inspection coordinates into repair coordinates|工具間座標需共同標記校準。|Coordinate transfer needs shared calibration marks.
比較 die-to-die 與 die-to-database 檢查|Compare die-to-die and die-to-database inspection|比較基準不同會改變可見異常。|Different references reveal different anomalies.
計算缺陷偵測的漏檢與誤報率|Calculate miss and false-alarm rates|提高靈敏度可能增加複查負擔。|Higher sensitivity can increase review burden.
對重複掃描評估缺陷位置再現性|Assess defect-position repeatability by rescanning|定位再現性限制局部修補。|Localization repeatability limits local repair.
分辨顆粒污染與圖形本體缺損|Distinguish contamination from pattern damage|清潔與修補不是可互換的處置。|Cleaning and repair are not interchangeable treatments.
為不確定缺陷建立複查分流|Route uncertain defects for further review|不確定性應保留而非強迫二分。|Uncertainty should be retained rather than forced into a binary result.
對遮光多餘區規畫局部移除|Plan local removal for excess opaque material|移除不得侵入應保留的圖形。|Removal must avoid intended features.
對缺少吸收層的區域規畫局部添加|Plan local addition where absorber is missing|添加層需滿足光學及幾何要求。|Added material must meet optical and geometric requirements.
畫出電子束與前驅物的作用區|Sketch the beam–precursor interaction region|反應區域由束流與表面分子共同決定。|Beam exposure and surface molecules jointly define the reaction region.
檢查修補殘留與暈圈效應|Inspect repair residue and halo effects|修補區外也可能受影響。|Effects may extend beyond the intended repair area.
比較修補與圖形位移避讓方案|Compare repair with pattern-shift avoidance|埋藏缺陷不一定適合直接修補。|Buried defects are not always suitable for direct repair.
建立停止修補的判定條件|Define repair stop criteria|反覆處置可能累積損傷。|Repeated intervention can accumulate damage.
量測修補後邊緣位置|Measure post-repair edge placement|尺寸恢復與位置恢復是不同要求。|Restoring size and restoring position are distinct requirements.
以工作波長檢查空中像|Evaluate aerial images at the operating wavelength|可印性驗證應對應實際成像條件。|Printability verification should match imaging conditions.
比較焦距掃描中的修補表現|Compare repair performance through focus|單一焦點合格不能保證製程窗口。|Passing one focus point does not establish a process window.
檢查修補區與邻近圖形的相互作用|Check repair interaction with neighboring patterns|局部修補也可能改變鄰近光學耦合。|Local repair can change neighboring optical coupling.
追蹤光罩清潔後的再驗證|Plan requalification after mask cleaning|清潔可能改變殘留與表面狀態。|Cleaning can change residue and surface condition.
完成可追溯的缺陷關閉報告|Complete a traceable defect-closure report|關閉缺陷需要前後證據與接受條件。|Closure needs before/after evidence and acceptance criteria.
''',['maskrepair','maskqual','maskmetro','pattern'],'a035 a037'.split())

add('a037',
['振幅與相位|Amplitude and phase','光罩結構|Mask structures','成像窗口|Imaging window','量測與整合|Metrology and integration'],
['強度來自複數光場相加後取模平方，不能直接相加强度。|Intensity is the squared magnitude of summed complex fields, not a direct sum of intensities.','交替式與衰減式相位移光罩具有不同振幅與相位配置。|Alternating and attenuated phase-shift masks use different amplitude and phase layouts.','相位移改善取決於圖形、照明與焦距。|Phase-shift benefits depend on pattern, illumination and focus.','光學相位、透射率與幾何位置須分別量測。|Optical phase, transmission and geometric placement require separate measurements.'],
['只需把兩束光強相加。|Simply add the two intensities.','所有相位移光罩都完全不透光。|Every phase-shift mask is completely opaque.','最佳焦點改善代表所有焦距都改善。|Better best-focus imaging proves improvement at every focus.','幾何厚度相同就必定相位相同。|Equal geometric thickness necessarily means equal phase.'],
'''
以複數平面表示兩束等振幅光|Represent equal-amplitude fields in the complex plane|相位差決定相長或相消干涉。|Phase difference controls constructive or destructive interference.
計算零與半週期相位差的合成強度|Calculate intensity at zero and half-cycle phase difference|理想反相等振幅場可相消。|Ideal equal-amplitude opposing fields can cancel.
比較振幅減半與強度減半|Distinguish halved amplitude from halved intensity|強度與振幅平方成正比。|Intensity scales with amplitude squared.
繪製二元光罩邊緣的模糊像|Sketch blurred edges from a binary mask|繞射限制圖形轉移的陡峭度。|Diffraction limits the sharpness of transferred edges.
加入相位反轉區觀察暗線|Add a phase-reversal region and inspect the dark line|暗線可由干涉形成而非遮光形成。|Interference can create a dark line without an opaque strip.
列出簡化干涉模型的限制|List limits of a simplified interference model|實際成像還包含孔徑、偏振與照明。|Real imaging also includes aperture, polarization and illumination.
畫出交替式光罩的相位分配|Assign phases in an alternating mask|相位標記必須與圖形拓樸相容。|Phase labels must be compatible with pattern topology.
找出封閉迴圈中的相位衝突|Find phase conflicts in closed loops|並非每個任意圖形都能直接交替著色。|Not every arbitrary layout permits simple alternating phase assignment.
比較衰減式吸收層的透射與相位|Compare transmission and phase of an attenuating film|衰減式光罩仍有有限透光。|Attenuated masks retain finite transmission.
以折射率與厚度估算相位差|Estimate phase difference from index and thickness|相位延遲同時依賴波長與材料。|Phase delay depends on wavelength and material.
標出製造厚度偏差造成的相位誤差|Map thickness error into phase error|厚度均勻性會成為光學均勻性問題。|Thickness uniformity becomes an optical-uniformity issue.
比较石英蝕刻與薄膜型結構|Compare etched-quartz and thin-film structures|不同結構需要不同蝕刻及清潔驗證。|Different structures require different etch and cleaning checks.
對密集與孤立線比較成像對比|Compare imaging contrast for dense and isolated lines|一種相位配置不會同等改善所有圖形。|One phase scheme does not improve every pattern equally.
繪製線寬對焦距的曲線|Plot linewidth versus focus|離焦靈敏度是製程窗口的一部分。|Defocus sensitivity is part of the process window.
建立劑量與焦距共同容許區|Construct a joint dose–focus acceptance region|窗口要同時滿足多個圖形的尺寸要求。|A window must satisfy size limits for multiple patterns.
檢查旁瓣是否跨過光阻閾值|Check whether sidelobes cross the resist threshold|光學旁瓣可能產生非預期圖形。|Optical sidelobes can print unintended features.
比較不同照明對相位邊界的影響|Compare illumination effects on phase boundaries|照明條件會改變相位干涉的利用方式。|Illumination changes how phase interference is used.
評估線端與拐角的修正需求|Assess correction needs at line ends and corners|一維線條結果不能直接推廣至二維圖形。|One-dimensional line results do not automatically extend to two dimensions.
分別驗證透射率與相位角|Verify transmission and phase angle separately|兩者皆會改變成像但不互相替代。|Both affect imaging but do not substitute for each other.
量測圖形定位與相位邊界偏差|Measure placement and phase-boundary offsets|相位邊界位置本身是關鍵幾何量。|The phase-boundary position is itself a critical geometry.
建立修補後的空中像比較|Compare aerial images before and after repair|修補可能恢復外形卻未恢復相位。|Repair can restore shape without restoring phase.
追蹤清潔造成的光學變化|Track optical changes caused by cleaning|光學性能需要跨清潔循環追蹤。|Optical performance needs tracking across cleaning cycles.
比較光罩端與晶圓端驗收|Compare mask-side and wafer-side acceptance|光罩量測必須能連結晶圓成像需求。|Mask metrology must link to wafer imaging requirements.
提交相位配置與成像窗口設計審查|Review phase assignment and imaging window together|設計可印性與光罩可製造性需共同成立。|Printability and mask manufacturability must both hold.
''',['psm','psmibm','maskqual','comp'],'a036 a038'.split())

add('a038',
['成像誤差|Imaging error','模型校準|Model calibration','局部修正|Local correction','窗口驗證|Window validation'],
['OPC 修正光罩以補償成像及製程偏差，不是任意更改電路目標。|OPC modifies masks to compensate imaging and process bias, not to arbitrarily alter circuit targets.','校準集與驗證集須分離，且模型應記錄適用圖形範圍。|Calibration and validation sets must be separate and model pattern coverage documented.','局部邊緣移動會改變鄰近區域的光場。|Moving one edge alters the neighboring optical field.','OPC 必須在製程窗口內驗證，並符合光罩製造限制。|OPC needs process-window verification and mask-manufacturing constraints.'],
['直接把最終晶圓圖形複製到光罩即可。|Directly copy target wafer geometry onto the mask.','訓練誤差低就足以證明預測準確。|Low training error alone proves predictive accuracy.','每一條邊緣都可以完全獨立修正。|Every edge can be corrected independently.','只有最佳焦點需要驗證。|Only best focus requires verification.'],
'''
疊合設計輪廓與模擬晶圓輪廓|Overlay target and simulated wafer contours|邊緣位置誤差需以共同座標計算。|Edge-placement error requires common coordinates.
分開線端縮短與拐角圓化|Separate line-end shortening from corner rounding|兩者需要不同的局部修正。|The two effects need different local corrections.
比較密集線與孤立線偏差|Compare dense- and isolated-line bias|鄰近環境改變成像。|Neighboring geometry changes imaging.
定義邊緣評估點與正負方向|Define edge-evaluation points and sign conventions|一致符號讓修正方向可判讀。|Consistent signs make correction direction interpretable.
檢查光阻閾值對輪廓的影響|Inspect contour sensitivity to resist threshold|光學像不是最終顯影輪廓。|The optical image is not the final developed contour.
建立微影與蝕刻偏差分帳|Separate lithographic and etch bias|混合偏差會使補償失去可追溯性。|Mixed biases obscure the origin of compensation.
選擇涵蓋線寬與間距的校準圖形|Choose calibration patterns spanning widths and spaces|模型需要涵蓋代表性圖形環境。|Models need representative pattern environments.
保留未參與擬合的驗證圖形|Hold out patterns from fitting|獨立資料可揭露過度擬合。|Independent data can reveal overfitting.
比較量測噪聲與模型殘差|Compare measurement noise with model residuals|殘差不全是模型失準。|Residuals are not entirely model error.
檢查參數相關性與可辨識性|Check parameter correlation and identifiability|不同參數可能產生相似預測。|Different parameters can produce similar predictions.
建立量測條件與模型版號鏈結|Link measurement conditions to model revision|混用不同製程資料會污染校準。|Mixing process conditions contaminates calibration.
標示模型無法外推的圖形|Mark patterns outside validated coverage|未涵蓋圖形應增加驗證而非直接外推。|Uncovered patterns need added validation rather than blind extrapolation.
以線端延伸減少縮短|Use line-end extension to reduce shortening|延伸量須檢查鄰近空間。|Extension must respect neighboring spaces.
比較加入與不加入角落修正的輪廓|Compare contours with and without corner correction|修正效益須以晶圓輪廓評估。|Correction benefit is evaluated on wafer contours.
測試次解析輔助圖形的可印性|Test whether subresolution assist features print|輔助圖形應改善主圖形而不形成額外圖形。|Assists should improve main features without printing extra features.
逐次更新邊緣並觀察誤差收斂|Update edges iteratively and track error convergence|過大更新可能振盪。|Oversized updates can cause oscillation.
比較局部成本與全區成本|Compare local and regional objective values|局部改善可能惡化鄰近圖形。|Local improvement can worsen neighbors.
檢查最小光罩特徵限制|Check minimum mask-feature constraints|計算解仍需能被光罩設備寫入。|Computed solutions must remain writable.
掃描焦距與劑量下的輪廓|Sweep contours across focus and dose|製程窗口驗證需超出最佳點。|Window validation must extend beyond the nominal point.
以最壞邊緣誤差補充平均誤差|Supplement mean error with worst-edge error|平均值可掩蓋局部致命缺陷。|Averages can hide localized fatal defects.
檢查橋接與斷線熱點|Inspect bridge and break hotspots|功能失效與連通性有關。|Functional failure depends on connectivity.
比較修正前後的光罩資料量|Compare mask-data volume before and after correction|精細修正可能提高寫入成本。|Fine correction can increase writing cost.
將光罩量測回饋到 OPC 模型|Feed mask metrology back into the OPC model|實際光罩偏差會影響晶圓預測。|Actual mask bias affects wafer prediction.
提交可製造且有窗口的修正版圖|Submit a manufacturable correction with validated window|良好修正需兼顧成像與製造。|A sound correction balances imaging and manufacturing.
''',['comp','pattern','maskmetro'],'a039 a049'.split(),'asml')

add('a039',
['反問題定義|Inverse problem','最佳化設計|Optimization design','可製造性|Manufacturability','穩健驗證|Robust validation'],
['反向微影從目標晶圓輪廓求光罩，通常存在多種候選解。|Inverse lithography solves for masks from target wafer contours and can admit multiple solutions.','目標函數與正則化共同決定求得的圖形。|The objective and regularization jointly determine the resulting pattern.','曲線光罩可改善自由度，也增加資料與量測要求。|Curvilinear masks add freedom and increase data and metrology demands.','單一條件的最佳解未必對焦距、劑量及光罩误差穩健。|A single-condition optimum may be fragile to focus, dose and mask errors.'],
['反問題永遠只有唯一光罩解。|The inverse problem always has one unique mask solution.','成本下降就表示所有限制都滿足。|A lower cost proves all constraints are satisfied.','曲線越複雜就一定越容易製造。|More complex curves are necessarily easier to manufacture.','名目条件合格即可省略擾動測試。|Passing nominal conditions removes the need for perturbation tests.'],
'''
定義目標輪廓與可修改的光罩區|Define target contours and editable mask regions|反問題需先界定設計自由度。|An inverse problem requires defined design freedoms.
建立從光罩到光阻的前向模型|Construct a mask-to-resist forward model|反演品質受前向模型準確度限制。|Inversion quality is limited by forward-model accuracy.
比較像素與曲線兩種參數化|Compare pixel and contour parameterization|參數化影響解空間與計算需求。|Parameterization affects the solution space and computation.
選擇邊緣誤差或影像誤差目標|Choose edge-error or image-error objectives|不同成本函數可能偏好不同解。|Different objectives can favor different solutions.
畫出非唯一解的簡化示例|Sketch a simplified nonunique solution example|相似晶圓像可來自不同光罩。|Similar wafer images can arise from different masks.
保留電路連通性的不可改條件|Preserve noneditable circuit-connectivity constraints|可印性改善不能破壞電路意圖。|Improved printability must preserve circuit intent.
用有限差分估算邊緣移動梯度|Estimate an edge-movement gradient by finite differences|步長太小會放大量測或數值噪聲。|Too small a step amplifies measurement or numerical noise.
比較兩個初始解的收斂路徑|Compare convergence from two initial masks|局部最佳化可能依賴初始條件。|Local optimization can depend on initialization.
加入平滑正則項並觀察圖形|Add smoothing regularization and inspect the mask|平滑程度與成像自由度有取捨。|Smoothing trades against imaging freedom.
檢查更新步長對振盪的影響|Check update-step effects on oscillation|成本下降速度不等於最終解品質。|Fast cost reduction does not guarantee final solution quality.
分開訓練圖形與盲測圖形|Separate training and blind-test patterns|盲測有助於發現模型與最佳化偏誤。|Blind testing helps reveal model and optimization bias.
記錄每次迭代的限制違反|Record constraint violations at each iteration|可行性應與成本值一起追蹤。|Feasibility should be tracked alongside cost.
設定最小曲率半徑與間距|Set minimum curvature radius and spacing|光罩可寫入性限制細小曲率。|Mask writability constrains fine curvature.
將曲線轉成寫入資料並比較輪廓|Convert curves to writing data and compare contours|資料離散化會引入新的邊緣誤差。|Data discretization introduces additional edge error.
估算多束寫入的資料吞吐需求|Estimate data throughput for multibeam writing|光罩計算與寫入能力必須相容。|Mask computation must be compatible with writer capabilities.
比較曲線區與直線區的量測取樣|Compare metrology sampling on curves and straight edges|曲線量測需要足夠的方向與密度。|Curve metrology needs adequate orientations and density.
加入光罩製造偏差再模擬|Resimulate with mask-fabrication bias|理想光罩解需要考慮實體製作誤差。|Ideal mask solutions must account for fabrication error.
評估小缺陷修補的可行區|Evaluate feasible repair regions for small defects|極細複雜圖形可能增加修補難度。|Fine complex patterns can complicate repair.
把多個焦距點加入成本函數|Include several focus points in the objective|多條件最佳化可避免名目點過度最佳化。|Multi-condition optimization reduces nominal-point overfitting.
比較劑量偏差下的邊緣誤差分布|Compare edge-error distributions under dose shifts|尾端誤差比平均值更能顯示局部風險。|Tail errors reveal local risk better than the mean.
用獨立模型交叉檢查熱點|Cross-check hotspots with an independent model|相同模型自我驗證可能漏掉共同偏誤。|Self-validation with one model can miss shared bias.
建立計算成本與可印性比較表|Compare computational cost with printability|更昂貴的求解需要可量測的收益。|More expensive optimization needs measurable benefit.
標記尚未取得晶圓證據的主張|Mark claims lacking wafer evidence|模擬改善不是晶圓實測改善。|Simulated improvement is not measured wafer improvement.
交付光罩、模型與窗口的版本封包|Deliver versioned mask, model and process window|可重現性需要完整的輸入與限制。|Reproducibility needs complete inputs and constraints.
''',['comp','maskmetro','jeol','pattern'],'a038 a035'.split(),'asml')

add('a040',
['光學與液體|Optics and liquid','表面與液體介面|Surface and liquid interfaces','掃描與誤差|Scanning and error','微影整合|Lithographic integration'],
['浸潤提高晶圓側成像介質折射率，數值孔徑需依所定義空間計算。|Immersion raises the wafer-side imaging-medium refractive index; NA must be defined in the appropriate optical space.','液體、頂層與光阻的相容性是成像條件的一部分。|Compatibility among liquid, topcoat and resist is part of the imaging process.','動態液體管理會連結掃描速度、溫度與缺陷。|Dynamic liquid management couples scan speed, temperature and defects.','解析度、套刻與缺陷率必須同時驗證。|Resolution, overlay and defect rate require joint validation.'],
['浸潤只要把晶圓浸水即可。|Immersion simply requires submerging a wafer.','頂層完全不影響光阻反應。|The topcoat cannot affect resist behavior.','速度提高不會改變液體狀態。|Higher speed cannot affect liquid behavior.','解析線寬最小就代表製程最好。|The smallest resolved line proves the best process.'],
'''
用 NA=n sinθ 比較乾式與浸潤式|Compare dry and immersion imaging using NA=n sinθ|折射率與入射角共同決定數值孔徑。|Index and ray angle jointly determine numerical aperture.
計算固定波長下的相對解析度|Calculate relative resolution at fixed wavelength|Rayleigh 比較須固定其餘模型係數。|Rayleigh comparisons require other model factors to remain fixed.
比較解析度與焦深的縮放|Compare resolution and depth-of-focus scaling|提高 NA 通常使焦深更敏感。|Higher NA generally tightens depth-of-focus sensitivity.
畫出鏡頭、液體與晶圓的光路|Sketch the lens–liquid–wafer optical path|液體介面不能從光路中省略。|Liquid interfaces cannot be omitted from the optical path.
檢查氣泡造成的局部折射變化|Assess local refraction caused by a bubble|氣泡會破壞均勻介質假設。|Bubbles violate the uniform-medium assumption.
列出折射率隨溫度變化的誤差鏈|Trace temperature-dependent index into imaging error|熱穩定性會變成光學穩定性。|Thermal stability becomes optical stability.
比較有頂層與無頂層的介面|Compare coated and uncoated resist interfaces|保護層會改變接觸、溶出及光學條件。|A protective layer changes contact, leaching and optical conditions.
以接觸角示意液體潤濕|Illustrate wetting with contact-angle measurements|靜態接觸角不能完全代表動態掃描。|Static contact angles do not fully describe dynamic scanning.
建立光阻成分溶出的檢查表|Plan checks for resist-component leaching|溶出可能影響液體與光學表面。|Leaching can affect liquid and optical surfaces.
分辨水痕與曝光圖形缺陷|Distinguish watermarks from pattern defects|缺陷外觀需結合曝光前後位置。|Defect appearance needs before/after spatial evidence.
檢查晶圓邊緣液體管理|Assess liquid management at wafer edges|邊緣幾何改變液體邊界條件。|Edge geometry changes liquid boundary conditions.
規畫顆粒與液體潔淨度取樣|Plan particle and liquid-cleanliness sampling|過濾性能不代表表面完全無顆粒。|Filtration performance does not prove a particle-free surface.
追蹤掃描方向與缺陷條紋|Relate scan direction to defect streaks|方向性缺陷可提供液體或運動線索。|Directional defects can reveal fluid or motion effects.
比較加速段與等速段的液體介面|Compare liquid interfaces during acceleration and steady motion|暫態條件可能不同於穩態。|Transient conditions can differ from steady state.
將焦點地圖與晶圓翹曲疊合|Overlay focus maps with wafer bow|基板形貌會消耗焦點預算。|Substrate topography consumes focus budget.
拆解工具間套刻誤差|Decompose tool-to-tool overlay error|多機混用需要交叉匹配。|Using several tools requires cross-matching.
比較曝光前量測與曝光中控制|Compare pre-exposure measurement with in-exposure control|前饋與回饋處理不同時間尺度。|Feedforward and feedback address different timescales.
建立液體溫度與焦點漂移的關聯|Relate liquid temperature to focus drift|相關性仍需排除其他漂移來源。|Correlation still requires excluding other drift sources.
建立劑量焦距矩陣並檢查線端|Build a dose–focus matrix including line ends|一維線寬不能代表所有版圖。|One-dimensional linewidth does not represent every layout.
比較浸潤單次與多重圖案化|Compare immersion single exposure with multipatterning|多重圖案化加入套刻與製程介面。|Multipatterning adds overlay and process interfaces.
追蹤光阻到硬罩的轉移偏差|Track resist-to-hard-mask transfer bias|曝光品質需延伸到圖案轉移驗證。|Exposure quality must extend into pattern-transfer verification.
比較晶圓中心與邊緣缺陷密度|Compare center and edge defect densities|空間取樣不能只挑最佳區域。|Spatial sampling must not select only favorable regions.
分析吞吐量與良率的共同限制|Analyze throughput and yield together|更快曝光若增加缺陷未必提升有效產出。|Faster exposure may not increase useful output if defects rise.
交付光學、液體與量測整合圖|Deliver an integrated optics–fluid–metrology diagram|浸潤微影是多子系統協同工程。|Immersion lithography is a coordinated multisystem process.
''',['duv','lenses','comp','maskmetro'],'a048 a043'.split(),'asml')

add('a041',
['系統與圖形|System and patterns','材料與光罩|Materials and masks','窗口與缺陷|Window and defects','電性與整合|Electrical integration'],
['EUV 以反射式光學與真空路徑成像，材料與光罩都參與成像誤差。|EUV uses reflective optics and vacuum paths; materials and masks both contribute imaging errors.','光阻厚度、吸收、粗糙度與轉移耐受性需共同選擇。|Resist thickness, absorption, roughness and transfer resistance require joint selection.','隨機缺陷、尺寸與套刻是不同合格條件。|Stochastic defects, dimensions and overlay are distinct acceptance conditions.','單次曝光減少工序的效益仍需以整合良率驗證。|Benefits from fewer exposures still require integrated-yield validation.'],
['EUV 可直接套用透射玻璃鏡頭。|EUV can directly use transmitting glass lenses.','最薄光阻一定最適合所有圖形。|The thinnest resist is best for every pattern.','套刻合格就不會發生隨機斷線。|Good overlay prevents stochastic breaks.','減少曝光次數即可保證產品良率增加。|Fewer exposures guarantee improved product yield.'],
'''
畫出光源至晶圓的反射路徑|Sketch the reflective source-to-wafer path|EUV 光路各反射介面都影響能量。|Each reflecting interface affects EUV throughput.
分配光源穩定度與晶圓劑量責任|Separate source stability from wafer-dose control|光源輸出不是晶圓上吸收劑量。|Source output is not absorbed wafer dose.
標出真空、污染與維護的介面|Mark vacuum, contamination and maintenance interfaces|污染會改變反射率及製程穩定性。|Contamination can alter reflectivity and process stability.
比較線空間與接觸孔的成像目標|Compare line-space and contact-hole targets|不同圖形有不同的失敗模式。|Different patterns have different failure modes.
建立目標邊緣位置誤差預算|Build a target edge-placement-error budget|尺寸、位置及轉移誤差需共同分配。|Size, placement and transfer errors need joint allocation.
選擇可比的 DUV 或 EUV 對照流程|Choose a comparable DUV or EUV reference flow|公平比較需一致設計目標。|A fair comparison needs matching design targets.
檢查多層光罩與吸收層的功能|Distinguish multilayer and absorber functions|反射式光罩與透射式光罩機制不同。|Reflective and transmissive masks operate differently.
比較光罩三維效應的方向性|Compare orientation dependence of mask 3D effects|斜入射可造成方向相關成像。|Oblique incidence can produce orientation-dependent imaging.
評估光罩保護膜的光學代價|Assess optical costs of a pellicle|防顆粒保護也會影響能量與熱。|Particle protection also affects energy and heat.
比較不同底層對光阻的影響|Compare underlayer effects on resist behavior|底層可影響反應與圖案轉移。|Underlayers affect reactions and pattern transfer.
建立薄光阻與硬罩的厚度分工|Allocate thickness between resist and hard mask|薄光阻需要可行的後續轉移。|Thin resist requires a viable downstream transfer.
追蹤塗佈到曝光的等待歷程|Track delay history between coating and exposure|時間歷程可能改變材料狀態。|Time history can change material state.
建立焦距劑量矩陣的取樣順序|Design sampling order for a focus–dose matrix|隨機化順序有助於分離漂移。|Randomized order helps separate drift.
分開密集區與孤立區的尺寸偏差|Separate dense and isolated dimensional bias|同一劑量不保證所有圖形相同表現。|One dose does not guarantee equal behavior for all patterns.
計算缺失接觸孔的發生率|Calculate missing-contact incidence|接觸孔缺失與線條粗糙度不可互換。|Missing contacts are not interchangeable with line roughness.
比較斷線與橋接的劑量趨勢|Compare dose trends for breaks and bridges|提高劑量可能改善一種缺陷卻惡化另一種。|Increasing dose can improve one defect class while worsening another.
將光罩重複缺陷與隨機缺陷分群|Separate repeating mask defects from stochastic defects|空間重複性可提示系統來源。|Spatial repetition can indicate a systematic source.
為檢查面積不足的零缺陷結果加註|Qualify zero-defect results with inadequate inspected area|稀有事件結論需要足夠樣本量。|Rare-event conclusions need sufficient sample size.
對照顯影後與蝕刻後圖形|Compare post-development and post-etch patterns|圖案轉移可能改變缺陷可見性。|Transfer can change defect visibility.
以電阻鏈驗證通孔連接|Verify via connectivity using resistance chains|形貌完整不代表接觸電阻合格。|Intact morphology does not prove acceptable contact resistance.
以梳狀結構驗證線間隔離|Verify line isolation with comb structures|漏電能揭露影像未辨識的連接。|Leakage can reveal connections missed by imaging.
比較单次與多次曝光的誤差累積|Compare error accumulation for single and multiple exposure|工序數與失敗機會相關但非唯一因素。|Step count affects failure opportunities but is not the only factor.
記錄研究良率與產品良率的範圍|State the scope of research and product yield|測試載具結果不可無條件外推。|Test-vehicle results cannot be extrapolated unconditionally.
提出具缺陷、尺寸與電性證據的整合評審|Review integration with defect, dimensional and electrical evidence|整合成熟度需要多種獨立證據。|Integration maturity requires several independent evidence types.
''',['euv','pattern','stochastic','euvyield'],'a034 a042'.split(),'asml')

add('a043',
['分解與配色|Decomposition and coloring','曝光與轉移|Exposure and transfer','誤差分配|Error allocation','整合比較|Integration comparison'],
['雙重圖案化把難以單次解析的圖形拆成可處理的子集合。|Double patterning partitions patterns into subsets that can be processed separately.','兩次微影與側壁自對準是不同流程，不能混用誤差模型。|Two-exposure lithography and spacer self-alignment are different flows with different error models.','相對位置、線寬與側壁厚度具有不同的誤差傳遞方式。|Relative placement, linewidth and spacer thickness propagate errors differently.','圖案化方案應同時比較版圖限制、步數與電性結果。|Patterning schemes need comparison of layout constraints, step count and electrical results.'],
['只需把曝光時間加倍。|Simply double the exposure time.','所有雙重圖案化都沒有套刻需求。|All double patterning eliminates overlay requirements.','兩次曝光平均位置正確就不會有局部錯誤。|Correct mean placement prevents local errors.','步驟最少的方案永遠最佳。|The fewest-step scheme is always best.'],
'''
將密集線分成兩種顏色|Split dense lines into two colors|每個子集合的間距可大於最終間距。|Each subset can have larger pitch than the final pattern.
在鄰接圖找出奇數迴圈|Find odd cycles in a conflict graph|某些圖形不能只用兩色無衝突分解。|Some patterns cannot be conflict-free with two colors.
標記必須切割的版圖區域|Mark layout regions requiring stitches|切割點可能增加局部失敗風險。|Stitch points can add local failure risk.
比較 LELE 與側壁雙重圖案化|Compare LELE with spacer double patterning|兩者的線形成方式不同。|They form lines by different mechanisms.
寫出最終線寬與間距目標|State final linewidth and spacing targets|圖案密度不等於線寬。|Pattern density is not linewidth.
畫出兩組光罩與共同座標|Draw both masks in shared coordinates|分解後仍須保留電路連通性。|Decomposition must preserve circuit connectivity.
追蹤第一組光阻到硬罩|Trace first-pattern resist into the hard mask|第一組圖形必須能承受第二組製程。|The first pattern must survive the second process.
標出第一組保護與平坦化需求|Mark first-pattern protection and planarization needs|既有地形會影響第二次微影。|Existing topography affects the second lithography.
安排第二組對位標記位置|Plan second-pattern alignment marks|標記須在後續薄膜後仍可辨識。|Marks must remain detectable after later films.
比較先蝕刻與凍結光阻策略|Compare intermediate etch with resist-freeze strategies|材料相容性會限制流程選擇。|Material compatibility constrains flow selection.
檢查兩組圖形合併後的缺口|Inspect gaps after merging both patterns|各組合格不保證合併後連通。|Each subset passing does not guarantee merged connectivity.
追蹤清潔對第一組線條的侵蝕|Track cleaning damage to first-pattern lines|重複清潔可能累積尺寸損失。|Repeated cleaning can accumulate dimensional loss.
畫出套刻偏移造成的交替間距|Sketch alternating spaces caused by overlay shift|相對位移會產生間距交替。|Relative displacement produces alternating spacing.
把兩組線寬偏差分別加入模型|Add linewidth bias for each subset separately|共同偏差與差分偏差後果不同。|Common and differential biases have different consequences.
比較系統偏移與隨機偏移|Compare systematic and random displacement|可補償誤差與不可預測誤差需分帳。|Correctable and unpredictable errors need separate budgets.
計算最小間距的最壞條件|Calculate worst-case minimum spacing|平均間距可能掩蓋最小間距不足。|Mean spacing can hide insufficient minimum spacing.
評估切割點的重疊容忍度|Assess overlap tolerance at a stitch|切割接縫需要額外連通裕量。|A stitched seam needs extra connectivity margin.
為兩組曝光建立分群統計|Build separate statistics for both exposures|分群可揭露工具或製程差異。|Grouping can reveal tool or process differences.
以蛇形線檢查接縫斷線|Check stitched breaks using serpentine lines|電阻異常需回溯到圖案群組。|Resistance anomalies need tracing to pattern groups.
以梳狀結構檢查間距短路|Check spacing shorts using comb structures|橋接風險集中於最小間距。|Bridge risk concentrates at minimum spacing.
比較雙重與單次 EUV 的介面數|Compare interfaces in double patterning and single EUV|减少介面可能減少誤差來源但引入不同材料風險。|Fewer interfaces can reduce error sources while introducing different material risks.
建立工序、檢查與返工成本表|Tabulate process, inspection and rework costs|曝光次數不是成本的唯一來源。|Exposure count is not the only cost driver.
標記不可沿用到任意版圖的規則|Mark rules that do not transfer to arbitrary layouts|規則有效範圍取決於圖形與流程。|Rule validity depends on layout and flow.
交付兩組圖案的整合驗收|Deliver integrated acceptance for both pattern subsets|驗收需涵蓋單組與合併後性能。|Acceptance must cover subsets and their combined behavior.
''',['multipattern','saqp','comp','maskmetro'],'a044 a048'.split())

add('a044',
['骨架與倍增|Mandrels and multiplication','第一輪側壁|First spacer cycle','第二輪與切割|Second cycle and cuts','誤差與電性|Errors and electrical tests'],
['SAQP 利用兩輪側壁圖形倍增，線位置由多道沉積與蝕刻共同決定。|SAQP uses two spacer multiplication cycles; deposition and etch jointly determine line placement.','側壁厚度控制與方向性蝕刻共同決定保留輪廓。|Spacer thickness and directional etch jointly determine retained contours.','自對準線條仍需要切割或阻擋图形定義電路。|Self-aligned lines still need cuts or blocks to define circuits.','四倍密度不表示所有線寬、間距與端點誤差自動一致。|Fourfold density does not automatically equalize widths, spaces or end errors.'],
['SAQP 就是連續曝光四次。|SAQP means exposing four times.','沉積越厚就一定得到越細的線。|Thicker deposition necessarily produces finer lines.','自對準代表完全不需要切割對位。|Self-alignment eliminates all cut alignment.','所有線條誤差必然完全相同。|Every line necessarily has the same error.'],
'''
畫出最初骨架與最終四倍線群|Draw initial mandrels and final fourfold line sets|骨架週期與最終節距不同。|Mandrel period differs from final pitch.
用不同顏色追蹤各代材料|Color-code each material generation|材料身分決定選擇性移除次序。|Material identity determines selective-removal order.
比較 SADP 與 SAQP 的輪數|Compare cycle counts in SADP and SAQP|增加一輪也增加介面與誤差來源。|Another cycle adds interfaces and error sources.
列出骨架線寬與側壁厚度的幾何關係|Relate mandrel width to spacer thickness geometrically|節距倍增不是任意厚度都能達成。|Pitch multiplication requires compatible dimensions.
標記需要保留及刪除的最終線|Mark retained and deleted final lines|規則線群仍需轉成電路拓樸。|Regular line arrays still need circuit topology.
建立每層選擇性蝕刻矩陣|Build a layer-selectivity matrix|可分辨材料是多輪轉移的基礎。|Material discrimination enables repeated transfer.
檢查第一輪沉積的側壁覆蓋|Inspect first-cycle sidewall coverage|頂部膜厚不能代表侧壁膜厚。|Top thickness does not establish sidewall thickness.
畫出方向性回蝕後的側壁|Draw spacers after directional etchback|底部殘留會改變相鄰線連通性。|Bottom residue can alter neighboring-line connectivity.
比較骨架移除前後的支撐|Compare support before and after mandrel removal|細長側壁可能因機械作用失穩。|Slender spacers can become mechanically unstable.
量測第一輪的交替間距|Measure alternating spacing after the first cycle|骨架寬度誤差可形成節距游移。|Mandrel-width error can produce pitch walking.
追蹤側壁圓角向硬罩轉移|Trace spacer corner shape into the hard mask|輪廓形狀會影響後續線位置。|Contour shape affects subsequent line placement.
記錄第一輪中心與邊緣均勻性|Record center-to-edge uniformity in the first cycle|晶圓內不均勻會傳入下一輪。|Within-wafer nonuniformity propagates to the next cycle.
把第一輪圖形改作第二輪骨架|Use first-cycle patterns as second-cycle mandrels|上一輪輸出即下一輪輸入。|One cycle's output becomes the next cycle's input.
檢查第二輪厚度對最終線寬的影響|Assess second-cycle thickness effects on final width|後段厚度控制可能直接決定線寬。|Later thickness control can directly set linewidth.
疊合兩輪造成的節距游移|Superpose pitch walking from both cycles|誤差可依線群具有週期結構。|Errors can form periodic patterns across line groups.
規畫切割光罩的容許窗口|Plan the cut-mask acceptance window|切割套刻會影響線端及殘留連接。|Cut overlay affects line ends and residual connections.
比較 EUV 切割與多次 DUV 切割|Compare EUV cuts with multiple DUV cuts|切割方案改變步數與套刻要求。|Cut strategies change step count and overlay requirements.
檢查切割後是否留下短支線|Inspect short stubs after cutting|殘留支線可能改變寄生與短路風險。|Residual stubs can affect parasitics and shorting risk.
逐群統計四組線寬與間距|Measure widths and spaces by all four line groups|混合平均可能掩蓋系統性交替誤差。|Pooled averages can hide systematic alternating errors.
把側壁粗糙度與硬罩粗糙度對照|Compare spacer and hard-mask roughness|轉移可能改變粗糙度頻譜。|Transfer can alter the roughness spectrum.
用金屬電阻比較不同線群|Compare line-group resistance after metallization|相似影像可能有不同有效導電面積。|Similar images can hide different conducting areas.
檢查切割區的漏電與開路|Check leakage and opens at cut regions|線體與線端需要不同電性載具。|Line bodies and ends need different electrical vehicles.
比較 SAQP 與單次成像的完整預算|Compare complete SAQP and single-image budgets|自對準收益須扣除新增製程變異。|Self-alignment gains must account for added process variation.
交付可追溯的四代圖形流程|Deliver a traceable four-generation pattern flow|每道轉移都需有輸入與輸出證據。|Each transfer needs input and output evidence.
''',['saqp','multipattern','pattern','euvyield'],'a043 a057'.split())

add('a045',
['自組裝原理|Self-assembly principles','引導模板|Guiding templates','缺陷與轉移|Defects and transfer','整合選擇|Integration choices'],
['區塊共聚物的自組裝有固有尺度，但仍需模板設定位置與方向。|Block-copolymer self-assembly has a natural scale but still needs guides for placement and orientation.','表面化學、侷限幾何與薄膜厚度共同控制排列。|Surface chemistry, confinement and film thickness jointly control ordering.','漂亮的局部排列不能替代大面積缺陷統計。|Attractive local ordering does not replace large-area defect statistics.','移除一個區塊及圖案轉移可能改變原始自組裝結構。|Removing one block and transferring patterns can change the original self-assembled structure.'],
['自組裝完全不需要任何定位模板。|Self-assembly needs no placement template.','只要材料相同，所有厚度都形成相同排列。|The same material orders identically at every thickness.','單張顯微照片足以證明零缺陷。|One micrograph proves zero defects.','聚合物圖案可直接等同最終金屬線。|Polymer patterns are equivalent to final metal lines.'],
'''
分開區塊相分離與宏觀混合|Distinguish microphase separation from macroscopic mixing|共價連接限制兩區塊完全分離。|Covalent linkage prevents complete block separation.
以組成比例比較柱狀與層狀相|Compare cylinder and lamellar phases by composition|相態取決於材料與組成條件。|Morphology depends on material and composition.
標示自然週期與模板週期|Mark natural and guiding periods|模板需與材料尺度相容。|Guides must be compatible with the material length scale.
比較高χ材料與較低χ材料的目標|Compare high-χ and lower-χ material goals|提高分離強度仍需處理界面與動力學。|Stronger segregation still requires interface and kinetic control.
画出缺陷能量與退火動力學的分工|Separate defect energetics from annealing kinetics|最低能態不保證在有限時間內到達。|The lowest-energy state may not be reached in finite time.
區分密度倍增與任意電路成形|Distinguish density multiplication from arbitrary circuitry|規則自組裝不直接產生所有電路圖形。|Regular self-assembly does not directly generate every circuit pattern.
比較化學引導與地形引導|Compare chemical and topographic guidance|兩者以不同邊界條件定位。|They guide through different boundary conditions.
標記中性層與選擇性潤濕層|Mark neutral and preferential wetting layers|表面偏好可能改變區塊方向。|Surface preference can change block orientation.
量測模板線寬對排列的影響|Assess guide-width effects on ordering|模板尺寸誤差會傳入自組裝結果。|Guide-size error propagates into ordering.
比較薄膜厚度與自然週期的比例|Compare film thickness with natural period|厚度不相容可能引起缺陷或方向改變。|Incompatible thickness can cause defects or reorientation.
建立退火條件的對照矩陣|Build an annealing-condition comparison matrix|熱史與溶劑史可能產生不同排列。|Thermal and solvent histories can produce different ordering.
追蹤模板邊界附近的排列|Track ordering near guide boundaries|邊界效應可能不同於內部區域。|Boundary behavior can differ from the interior.
將位錯、橋接與缺失線分開|Separate dislocations, bridges and missing lines|不同缺陷代表不同失敗機制。|Different defect classes indicate different failure mechanisms.
估算檢查面積與罕見缺陷信賴區間|Relate inspected area to rare-defect confidence|樣本面積限制可聲稱的缺陷率。|Sample area limits supportable defect-rate claims.
比較模板缺陷與自組裝缺陷位置|Compare guide-defect and assembly-defect locations|空間關聯有助於追蹤來源。|Spatial association helps trace origins.
設計移除單一區塊後的檢查|Plan inspection after removing one block|選擇性移除也可能傷害保留區塊。|Selective removal can damage retained blocks.
比較浸潤強化前後的輪廓|Compare contours before and after infiltration strengthening|強化改善耐受性但可能改變尺寸。|Strengthening can improve resistance while changing dimensions.
追蹤聚合物到硬罩的缺陷|Trace defects from polymer into the hard mask|轉移會改變缺陷大小與可見度。|Transfer can change defect size and visibility.
比較線條與接觸孔縮小的用途|Compare line patterning with contact-hole shrinking|不同用途需要不同模板與驗收。|Different uses require different guides and acceptance criteria.
把自組裝位置誤差加入套刻預算|Include assembly-placement error in overlay budgets|自然週期精準不代表絕對位置正確。|Accurate natural pitch does not prove absolute placement.
用電性結構檢查殘留橋接|Check residual bridges with electrical structures|形貌與電性結果可能不完全一致。|Morphological and electrical results may differ.
比較 DSA 與 EUV 補充關係|Compare DSA as a complement to EUV|自組裝可協助圖案化而非必然取代微影。|Self-assembly can assist rather than necessarily replace lithography.
記錄實验展示的尺寸與材料範圍|Document demonstration dimensions and material scope|研究展示只支持所測條件。|A demonstration supports only tested conditions.
提交模板、材料與缺陷證據鏈|Deliver a guide–material–defect evidence chain|可整合性需要位置、缺陷與轉移共同證據。|Integrability needs combined placement, defect and transfer evidence.
''',['dsa','dsahigh','sis','pattern'],'a044 a046'.split())

add('a046',
['模板與樹脂|Template and resin','填充與對位|Filling and alignment','固化與脫模|Curing and release','缺陷與轉移|Defects and transfer'],
['奈米壓印以模板與樹脂的接觸轉移圖形，與投影微影機制不同。|Nanoimprint transfers patterns through template–resin contact, unlike projection lithography.','填充速度與殘留層均勻性需同時控制。|Filling speed and residual-layer uniformity require joint control.','固化與脫模會引入收縮、應力及黏附問題。|Curing and release can introduce shrinkage, stress and adhesion issues.','模板重複使用使顆粒與缺陷複製成為重要風險。|Template reuse makes particles and replicated defects important risks.'],
['奈米壓印只靠提高投影鏡頭 NA。|Nanoimprint works by increasing projection-lens NA.','樹脂越多就一定填充越完整且均勻。|More resin always improves filling and uniformity.','固化後可以忽略脫模力。|Release force becomes irrelevant after curing.','模板上的小缺陷只會影響一次。|A small template defect affects only one imprint.'],
'''
比較模板接觸與光學投影的資訊傳遞|Compare information transfer by contact and projection|接觸轉移仍需光學或其他對位量測。|Contact transfer still needs optical or other alignment metrology.
畫出模板凹凸與最終光阻極性|Relate template relief to final resist polarity|凸凹關係須在圖案轉移前釐清。|Relief polarity must be clarified before transfer.
標記模板主模與複製模的關係|Distinguish master templates from replicas|複製會增加缺陷追溯層次。|Replication adds layers to defect traceability.
比較線條、孔洞與大面積區的填充|Compare filling of lines, holes and broad regions|局部圖形密度改變樹脂需求。|Local pattern density changes resin demand.
列出樹脂黏度與潤濕的角色|Identify the roles of viscosity and wetting|填充不只取決於施加力量。|Filling depends on more than applied force.
建立模板耐用度與清潔的評估項|Define template-durability and cleaning measures|清潔效率不能脫離表面壽命評估。|Cleaning efficacy must be assessed with surface lifetime.
依局部圖案體積規畫滴液分布|Plan droplets using local pattern volume|均勻滴液未必得到均勻殘留層。|Uniform droplets need not yield uniform residual layers.
追蹤兩滴樹脂合流的氣泡風險|Track bubble risk where droplets merge|被困氣體會造成未填滿區。|Trapped gas can create unfilled regions.
比較接觸時間與填充完成度|Compare contact time with fill completeness|更短時間可能增加缺陷但非線性關係。|Shorter time can increase defects in a nonlinear way.
畫出模板與晶圓的對位標記|Draw template and wafer alignment marks|多層製造仍需對準既有圖形。|Multilayer manufacturing still needs alignment to existing patterns.
把晶圓變形加入套刻模型|Include wafer deformation in overlay models|剛體位移不足以描述所有形變。|Rigid displacement cannot describe every deformation.
比較局部圖案密度與殘留層厚度|Compare local density with residual-layer thickness|殘留層差異會傳入後續蝕刻。|Residual-layer differences propagate into etching.
區分光固化與熱壓印的能量途徑|Distinguish photocuring from thermal imprinting|不同機制有不同材料与熱預算。|Different mechanisms have different materials and thermal budgets.
檢查固化前後的體積收縮|Assess volume shrinkage during curing|收縮可能改變尺寸與應力。|Shrinkage can alter dimensions and stress.
畫出脫模方向與高深寬比結構|Relate release direction to high-aspect-ratio features|脫模受力可能損傷細小結構。|Release forces can damage fine structures.
比較抗黏附表面使用前後|Compare anti-adhesion surfaces before and after use|表面狀態會隨使用歷程改變。|Surface condition changes with use history.
檢查模板污染對下一次壓印的影響|Assess template contamination in the next imprint|污染可在連續晶粒中複製。|Contamination can replicate across successive dies.
為脫模異常設計停止與複查條件|Define stop-and-review criteria for release anomalies|持續壓印可能擴大模板損傷。|Continuing to imprint can amplify template damage.
將未填充、顆粒與脫模缺陷分類|Classify nonfill, particle and release defects|缺陷分類有助於選擇改善方向。|Defect classification guides corrective action.
量測殘留層開口後的尺寸|Measure dimensions after residual-layer opening|開口蝕刻也可能侵蝕圖形側壁。|Opening etch can also erode pattern sidewalls.
比較模板輪廓與最終硬罩輪廓|Compare template and final hard-mask contours|接觸複製仍有多道尺寸偏差。|Contact replication still accumulates dimensional biases.
建立模板使用次數與缺陷趨勢|Trend defects against template use count|壽命評估需要序列資料。|Lifetime assessment needs sequential data.
比較吞吐、缺陷與套刻的共同窗口|Compare the joint throughput–defect–overlay window|單一性能優勢不能代表整體成熟度。|One performance advantage does not establish overall maturity.
交付有代表性圖形的壓印驗證報告|Deliver imprint validation across representative patterns|驗證需涵蓋密度與形狀多樣性。|Validation must cover density and shape diversity.
''',['nil','pattern','maskmetro'],'a045 a047'.split())

add('a047',
['資料與束斑|Data and spot','曝光與散射|Exposure and scattering','對位與拼接|Alignment and stitching','顯影與驗證|Development and validation'],
['電子束直寫直接在基板定義圖形，通常需在解析度與時間間取捨。|Electron-beam direct writing patterns substrates directly, usually trading resolution against time.','電子散射使局部沉積能量不同於名目劑量。|Electron scattering makes deposited energy differ from nominal dose.','場內定位、跨場拼接與層間套刻是不同誤差。|Within-field placement, field stitching and interlayer overlay are distinct errors.','顯影與圖案轉移可能改變原始曝光尺寸。|Development and transfer can alter exposure-defined dimensions.'],
['束斑直徑就是最終可製作線寬。|Beam diameter equals the final manufacturable linewidth.','每個位置收到的能量只來自該點束流。|Each location receives energy only from its own beam exposure.','拼接合格就表示層間套刻合格。|Good stitching proves good interlayer overlay.','曝光後尺寸不會再改變。|Dimensions cannot change after exposure.'],
'''
把設計版圖轉成可寫入圖元|Convert layout into writable primitives|資料轉換須保留尺度與拓樸。|Conversion must preserve scale and topology.
比較正型與負型電子束光阻|Compare positive- and negative-tone e-beam resists|光阻極性改變保留區域。|Resist tone changes the retained region.
依最小圖形選擇取樣格點|Choose a sampling grid for the smallest features|格點量化會引入邊緣位置誤差。|Grid quantization introduces edge-placement error.
估算曝光面積與總電荷|Estimate exposed area and total charge|總電荷由面劑量與面積決定。|Total charge is area dose multiplied by area.
分開曝光時間與載台等待時間|Separate beam time from stage overhead|寫入吞吐量包含非曝光時間。|Writing throughput includes non-exposure time.
設定小片樣品的座標原點|Define the coordinate origin for a small sample|樣品座標與機台座標需要轉換。|Sample and instrument coordinates need transformation.
畫出前向散射與背向散射|Sketch forward and backscattering|基板會影響長程鄰近曝光。|The substrate affects long-range proximity exposure.
比較薄厚光阻中的束斑展寬|Compare beam broadening in thin and thick resists|厚度會改變散射與後續轉移能力。|Thickness changes scattering and transfer capability.
建立密集與孤立圖形的劑量矩陣|Build dose matrices for dense and isolated features|圖形環境會改變最佳劑量。|Pattern environment can change optimum dose.
檢查大面積曝光對小間隙的影響|Assess broad exposure next to a narrow gap|鄰近沉積能量可能使間隙封閉。|Proximity energy can close a narrow gap.
比較導電與絕緣樣品的充電|Compare charging on conducting and insulating samples|充電可使束流偏轉。|Charging can deflect the beam.
評估導電保護層的相容性|Assess compatibility of a conductive coating|抑制充電措施也須可移除且不破壞光阻。|Charge suppression must be removable without harming resist.
以多個標記擬合平移旋轉|Fit translation and rotation using several marks|標記配置決定可辨識的誤差類型。|Mark geometry determines identifiable errors.
檢查標記辨識的訊號與損傷|Assess alignment-mark signal and damage|辨識曝光可能影響附近光阻。|Mark-detection exposure can affect nearby resist.
把大圖形跨場放置並檢查接縫|Place a large pattern across fields and inspect seams|連續設計可能被寫入場切割。|A continuous design can be divided by writing fields.
比較掃描順序造成的時間漂移|Compare temporal drift under different write orders|序列順序會改變漂移的空間分布。|Write order changes the spatial expression of drift.
量測第一層到第二層的套刻|Measure overlay from the first to the second layer|層間對位須獨立驗證。|Interlayer registration needs independent validation.
分開全域與局部座標殘差|Separate global and local coordinate residuals|全域修正不能消除所有局部變形。|Global correction cannot remove every local distortion.
對照顯影時間與保留尺寸|Relate development history to retained dimensions|顯影不是單纯的圖像顯現。|Development is not merely revealing an unchanged image.
檢查細長圖形倒塌與殘留|Inspect collapse and residue in slender patterns|機械穩定性也限制可用解析度。|Mechanical stability also limits useful resolution.
比較抬離用與蝕刻用截面|Compare lift-off and etch-mask profiles|相同光阻輪廓未必適合兩種用途。|One resist profile may not suit both applications.
評估顯微量測本身的曝光效應|Assess exposure effects caused by electron microscopy|量測可能改變敏感材料。|Measurement can modify sensitive materials.
以獨立量測驗證最小尺寸|Verify minimum dimensions with independent measurement|儀器解析度聲明不是樣品尺寸證據。|An instrument-resolution claim is not sample-dimension evidence.
交付資料、劑量與套刻的實驗紀錄|Deliver data, dose and overlay records|重現直寫需要完整設計與歷程。|Reproducing direct writing needs complete design and history.
''',['jeol','nisttools','maskmetro'],'a035 a046'.split(),'nist')

add('a048',
['向量與標記|Vectors and marks','誤差模型|Error models','量測品質|Measurement quality','補償與驗證|Correction and validation'],
['套刻是兩層圖形相對位置，不等於單層線寬。|Overlay is relative placement between layers, not single-layer linewidth.','平移、旋轉、縮放與高階形變需用適當模型區分。|Translation, rotation, scale and higher-order deformation need suitable models.','標記偏差、工具偏差與真實套刻會混合在觀測值中。|Mark bias, tool bias and true overlay combine in observations.','補償必須用保留位置或下一批次驗證，不能只看擬合殘差。|Correction needs held-out sites or a subsequent lot, not only fit residuals.'],
['線寬合格就能證明套刻合格。|Passing linewidth proves acceptable overlay.','只加一個平移量即可修正所有形變。|One translation corrects every distortion.','量測工具不會產生系統偏差。|Metrology tools cannot introduce systematic bias.','校準資料殘差為零就表示沒有風險。|Zero calibration residual means no risk.'],
'''
畫出上下兩層的相對位置向量|Draw relative-placement vectors between two layers|套刻需要共同座標與方向定義。|Overlay needs common coordinates and sign conventions.
把接觸孔偏移映射成落點風險|Map contact-hole offset into landing risk|容忍度取決於上下層幾何。|Tolerance depends on both layers' geometry.
比較影像式與繞射式標記|Compare image-based and diffraction-based marks|不同標記對製程非對稱的反應不同。|Marks respond differently to process asymmetry.
標記量測圖形與產品圖形的距離|Mark distances between metrology and product features|標記區不一定代表產品區。|Metrology marks may not represent device regions.
分開晶圓級與場內套刻|Separate wafer-level and within-field overlay|兩種尺度需要不同取樣。|The two scales need different sampling.
建立套刻與邊緣位置誤差的關係|Relate overlay to edge-placement error|邊緣誤差还包括尺寸與形狀。|Edge error also includes dimensions and shape.
由向量圖辨識平移分量|Identify translation from a vector map|一致方向偏移可能來自全域位移。|A consistent shift can indicate global translation.
由切向殘差辨識旋轉|Identify rotation from tangential residuals|旋轉誤差隨距離增加位移。|Rotational displacement grows with distance.
由放射殘差辨識縮放|Identify scale from radial residuals|倍率誤差不是固定平移。|Magnification error is not constant translation.
比較 X 與 Y 不同縮放|Compare anisotropic X and Y scaling|非等向變形需要分方向係數。|Anisotropic distortion needs separate directional coefficients.
檢查高階模型是否過度擬合|Check higher-order models for overfitting|增加係數也會增加資料需求。|More coefficients require more data.
保留未參與擬合的量測位置|Reserve measurement sites from fitting|保留點可測試模型外推。|Held-out sites test model generalization.
以重複量測估計再現性|Estimate repeatability from repeated measurement|重複性不代表對真值的準確度。|Repeatability is not accuracy relative to truth.
比較晶圓旋轉前後的工具偏差|Compare tool bias before and after wafer rotation|旋轉量測可協助分離工具與樣品效應。|Rotated measurements help separate tool and sample effects.
檢查標記被薄膜覆蓋後的訊號|Inspect mark signals after film coverage|對比變化可能造成量測偏差。|Contrast changes can cause metrology bias.
分析非對稱蝕刻造成的標記位移|Analyze apparent mark shift from asymmetric etching|量測中心不一定等於設計中心。|The measured center need not equal the design center.
比較不同工具的交叉匹配|Compare cross-matching between metrology tools|工具間偏差會污染製程比較。|Inter-tool bias can contaminate process comparisons.
用不確定度區間評估邊界結果|Assess borderline results using uncertainty intervals|接近限值的結果不能忽略量測不確定度。|Near-limit results require measurement uncertainty.
把可修正係數轉成曝光補償|Translate correctable coefficients into exposure compensation|補償自由度受曝光機控制能力限制。|Correction freedom is limited by scanner controls.
區分批次前饋與批次後回饋|Distinguish lot feedforward from post-lot feedback|兩者使用不同時間點資訊。|They use information available at different times.
比較補償前後的保留點殘差|Compare held-out residuals before and after correction|真正改善應出現在獨立資料。|Real improvement should appear in independent data.
檢查局部最大误差而非只看均值|Check local maximum error rather than only the mean|均值接近零仍可能有大幅散布。|A near-zero mean can coexist with wide dispersion.
將套刻結果連結到電性載具|Link overlay results to electrical test structures|幾何誤差需對應功能容忍度。|Geometric error must relate to functional tolerance.
交付模型係數與不確定度報告|Deliver model coefficients and uncertainty|可追溯補償需要資料、模型及限制。|Traceable correction needs data, model and limitations.
''',['maskmetro','duv','comp','metrology'],'a043 a049'.split(),'asml')

add('a049',
['焦點劑量定義|Focus and dose','窗口量測|Window measurement','感測與補償|Sensing and correction','變異與接受|Variation and acceptance'],
['焦距與劑量影響不同但會共同改變顯影輪廓。|Focus and dose have distinct effects that jointly change developed contours.','製程窗口是多個圖形與限制的交集。|A process window is the intersection of multiple patterns and constraints.','焦點控制需要表面高度、工具狀態與實際成像的鏈結。|Focus control needs links among surface height, tool state and imaging.','平均值合格不能保證整片晶圓或長時間穩定。|Acceptable averages do not prove whole-wafer or long-term stability.'],
['焦距與劑量是完全相同的控制量。|Focus and dose are the same control variable.','只用一種圖形即可代表所有版圖。|One pattern represents every layout.','高度感測器讀值就等於光阻最佳焦點。|A height-sensor reading equals the resist best focus.','平均線寬不變就表示控制正常。|An unchanged mean linewidth proves healthy control.'],
'''
定義名目焦點與離焦符號|Define nominal focus and defocus signs|焦點需有一致的參考面。|Focus needs a consistent reference plane.
分開入射劑量與吸收劑量|Separate incident and absorbed dose|材料吸收會改變有效能量。|Material absorption changes effective energy.
畫出劑量變化的光阻閾值輪廓|Sketch resist-threshold contours under dose change|劑量改變可能使線寬增或減，取決於極性。|Dose can increase or decrease width depending on tone.
比較密集線與接觸孔的焦點反應|Compare focus response of dense lines and contacts|不同圖形有不同敏感度。|Patterns have different sensitivities.
把晶圓表面高度轉成焦點預算|Translate surface height into focus budget|局部地形會消耗可用焦深。|Local topography consumes available depth of focus.
列出材料、曝光與顯影的混淆變因|List material, exposure and development confounders|線寬漂移不一定只由劑量造成。|Linewidth drift need not be caused only by dose.
規畫二維焦距劑量矩陣|Plan a two-dimensional focus–dose matrix|兩變量聯合掃描能揭露交互作用。|Joint sweeps reveal interactions.
用 Bossung 曲線比較線寬隨焦距|Compare linewidth through focus with Bossung curves|曲線形狀提供焦點與敏感度資訊。|Curve shape informs focus and sensitivity.
為線寬與缺陷分別畫合格區|Draw separate acceptance regions for width and defects|尺寸合格不代表缺陷合格。|Passing dimensions does not imply passing defects.
求多種圖形窗口的交集|Intersect process windows for several patterns|共同窗口可能比單圖形窗口更窄。|The common window can be narrower than an individual one.
比較插值與外推的可信範圍|Compare confidence in interpolation and extrapolation|未量測邊界外不應直接宣告合格。|Untested regions beyond the measured boundary should not be declared acceptable.
檢查矩陣掃描期間的漂移|Check drift during the matrix sweep|時間漂移可假裝成焦距或劑量效應。|Temporal drift can mimic focus or dose effects.
畫出表面高度到鏡頭焦點的前饋鏈|Sketch height-to-focus feedforward|量測延遲與空間對應會影響補償。|Latency and spatial registration affect compensation.
比較晶圓翹曲與局部台階|Compare wafer bow with local steps|不同空間尺度需要不同補償能力。|Different spatial scales require different correction capability.
檢查光源漂移到劑量控制的回路|Trace source drift through the dose-control loop|回路頻寬限制可抑制的漂移。|Loop bandwidth limits suppressible drift.
用監控片分離工具與材料批次差異|Use monitor wafers to separate tool and material variation|對照材料可減少歸因混淆。|Reference materials reduce attribution ambiguity.
比較曝光前量測與曝光後量測|Compare pre- and post-exposure metrology|前饋與結果驗證互相補充。|Feedforward and outcome verification complement each other.
建立異常感測訊號的複查程序|Plan review for anomalous sensor signals|感測故障不能直接當成製程變化。|Sensor faults must not be mistaken for process changes.
把焦距劑量散布疊在窗口上|Overlay focus–dose variation on the window|名目點位於窗口內仍可能有尾端超限。|A nominal point inside the window can still have out-of-limit tails.
比較最大裕量與最佳尺寸兩種設定|Compare maximum-margin and best-dimension settings|最佳單點不一定最穩健。|The best nominal point need not be the most robust.
檢查晶圓邊緣與中心的不同窗口|Compare edge and center windows|空間差異可能限制全片合格。|Spatial differences can limit whole-wafer acceptance.
追蹤跨批次的焦點與劑量趨勢|Trend focus and dose across lots|慢漂移需要長時間監控。|Slow drift needs long-term monitoring.
將窗口結果傳入套刻與蝕刻審查|Pass window results into overlay and etch reviews|微影窗口只是整合窗口的一部分。|Lithographic margin is only part of integration margin.
交付包含條件與取樣範圍的控制計畫|Deliver controls with conditions and sampling scope|控制計畫需要清楚的適用範圍。|Control plans need explicit applicability limits.
''',['duv','comp','pattern','metrology'],'a048 a050'.split(),'asml')

add('a050',
['事件與機率|Events and probability','取樣與量測|Sampling and metrology','來源分離|Source separation','設計與接受|Design and acceptance'],
['隨機缺陷研究需定義事件、觀測機會與獨立性假設。|Stochastic-defect analysis requires events, opportunities and independence assumptions.','缺陷檢查的靈敏度與檢查面積會限制統計結論。|Inspection sensitivity and inspected area limit statistical conclusions.','光子、材料與圖形變異會共同影響缺陷，不能單一歸因。|Photon, material and pattern variation jointly affect defects and preclude simple attribution.','研究結果必須連結實際圖形與電性失效。|Research findings must link to actual patterns and electrical failures.'],
['零觀察缺陷就表示缺陷率為零。|Zero observed defects means zero defect probability.','增加放大倍率就不需要增加取樣面積。|More magnification removes the need for larger sampled area.','所有缺陷都只由光子數決定。|Photon count alone determines every defect.','影像缺陷率可以直接等同整顆晶片良率。|Image defect rate directly equals whole-chip yield.'],
'''
區分線邊粗糙度與離散失敗事件|Distinguish line-edge roughness from discrete failures|連續變異與罕見事件需要不同指標。|Continuous variation and rare failures need different metrics.
定義斷線、橋接與缺孔的判準|Define breaks, bridges and missing-hole criteria|分類一致性是跨批次比較前提。|Consistent classification enables cross-lot comparisons.
以簡化泊松模型估算光子波動|Estimate photon fluctuations with a simple Poisson model|相對波動隨平均事件數增加而下降。|Relative fluctuation decreases as mean event count rises.
列出泊松獨立性假設的限制|List limits of Poisson independence|材料聚集與空間相關會破壞簡化假設。|Material clustering and spatial correlation violate simple assumptions.
分開單特徵失敗率與單位面積缺陷率|Separate per-feature probability from areal defect density|不同分母不能直接互換。|Different denominators are not interchangeable.
畫出缺陷到電路失效的連結|Map defects into circuit failures|不是每個缺陷都造成相同功能後果。|Not every defect causes the same functional consequence.
計算零缺陷樣本的近似上限|Calculate an approximate upper bound after zero defects|在獨立事件假設下，95%上限約為3除以樣本數。|For independent opportunities, the approximate 95% upper bound is 3 divided by sample count.
比較兩組不等樣本數的缺陷率|Compare rates from unequal sample sizes|原始缺陷數不能直接代表風險高低。|Raw counts alone cannot rank risk.
設計覆蓋不同晶圓區域的取樣|Sample across different wafer regions|只抽中心會漏掉空間非均勻。|Center-only sampling misses spatial nonuniformity.
估計檢查工具的漏檢比例|Estimate the inspection false-negative rate|觀察缺陷率可能低於真實缺陷率。|Observed rate can be lower than the true rate.
比較人工複查與自動分類一致性|Compare manual review with automated classification|分類器偏差會影響統計。|Classifier bias affects statistics.
把量測噪聲從粗糙度中區分|Distinguish metrology noise from roughness|量測噪聲可提高表觀粗糙度。|Measurement noise can inflate apparent roughness.
以相同線寬比較不同劑量條件|Compare doses at matched linewidth|幾何改變會混淆純劑量效應。|Geometry changes confound dose-only effects.
分別繪製橋接與斷線的趨勢|Plot bridge and break trends separately|兩者可能對製程調整反向回應。|They can respond oppositely to process changes.
比較光阻、底層與蝕刻三個因素|Compare resist, underlayer and etch factors|多因素對照有助於分離整合來源。|Multifactor controls help isolate integration sources.
檢查缺陷是否以光罩位置重複|Check whether defects repeat at mask coordinates|重複缺陷可能屬於系統來源。|Repeating defects can indicate systematic origins.
量測缺陷的空間自相關|Measure spatial autocorrelation of defects|群聚會減少有效獨立樣本數。|Clustering reduces effective independent sample size.
比較顯影後與蝕刻後的缺陷演化|Compare defect evolution through etching|蝕刻可放大、移除或新增缺陷。|Etching can amplify, remove or create defects.
用蛇形線連結斷線與開路|Link line breaks to opens using serpentine structures|電性載具驗證形貌的功能意義。|Electrical vehicles test the functional meaning of morphology.
用叉狀結構連結橋接與漏電|Link bridges to leakage using fork structures|漏電位置需與影像座標對應。|Leakage needs registration to image coordinates.
以簡化獨立模型估算多特徵良率|Estimate many-feature yield with an independent model|Y=(1-p)^N 依賴獨立且同分布假設。|Y=(1-p)^N assumes independent identically distributed events.
比較模型良率與實測載具良率|Compare modeled yield with measured vehicle yield|差異可能顯示相關性或未分類失敗。|Differences can indicate correlation or unclassified failures.
設計兼顧劑量與吞吐的接受條件|Define acceptance balancing dose and throughput|提高劑量的收益需同時評估成本。|Dose benefits must be evaluated alongside cost.
交付帶信賴區間與限制的缺陷報告|Deliver a defect report with confidence intervals and limits|明確分母與不確定度才使結果可比較。|Explicit denominators and uncertainty enable comparison.
''',['stochastic','euvyield','pattern','metrology'],'a034 a049'.split())

add('a051',
['電漿與表面|Plasma and surface','輪廓與選擇性|Profile and selectivity','端點與均勻性|Endpoint and uniformity','損傷與轉移|Damage and transfer'],
['RIE 的化學反應與離子轟擊共同決定蝕刻結果。|Chemical reactions and ion bombardment jointly determine RIE outcomes.','速率、方向性與選擇性是不同指標，不能以單一速率排名。|Rate, directionality and selectivity are distinct and cannot be ranked by rate alone.','電漿端點是間接訊號，需對應實際剩餘膜厚。|Plasma endpoint is an indirect signal requiring correlation with remaining thickness.','完成圖案仍需檢查表面、電性與污染。|Completed patterns still need surface, electrical and contamination checks.'],
['RIE 完全只有物理撞擊。|RIE is purely physical bombardment.','蝕刻最快就一定具有最好選擇性。|The fastest etch necessarily has the best selectivity.','亮度下降一定代表所有區域已蝕刻完成。|Falling brightness proves every region has finished etching.','側壁筆直就可排除電性損傷。|Straight sidewalls rule out electrical damage.'],
'''
畫出電子、離子與中性自由基|Draw electrons, ions and neutral radicals|粒子族群具有不同能量與方向性。|Particle populations have different energies and directionality.
分開體電漿與基板鞘層|Separate bulk plasma from substrate sheath|鞘層電場會加速離子。|Sheath fields accelerate ions.
比較化學蝕刻與物理濺射|Compare chemical etching with physical sputtering|可揮發產物有利於材料移除。|Volatile products facilitate material removal.
繪製離子入射方向分布|Sketch ion-incidence angular distributions|角度分布影響側壁與底部。|Angular distributions affect sidewalls and bottoms.
標記掩膜、目標膜與停止層|Mark mask, target film and stop layer|各材料均可能被製程消耗。|Every material can be consumed by the process.
建立不涉及實際機台配方的參數地圖|Build a parameter map without operating recipes|功率、壓力與溫度彼此耦合。|Power, pressure and temperature are coupled.
由蝕刻前後厚度計算平均速率|Calculate mean rate from thickness change|平均速率需註明實際作用時間。|Mean rate needs the effective process time.
以兩材料速率計算選擇比|Calculate selectivity from two material rates|選擇比依材料對與條件定義。|Selectivity is defined for a material pair and conditions.
比較垂直與橫向蝕刻量|Compare vertical and lateral removal|方向性不能只由深度判斷。|Depth alone does not establish anisotropy.
檢查光阻消耗與硬罩剩餘|Check resist consumption and hard-mask remainder|掩膜預算會限制可達深度。|Mask budget limits achievable depth.
比較密集與孤立圖形速率|Compare dense and isolated pattern rates|局部負載會改變反應物供應。|Local loading changes reactant supply.
辨識側壁聚合物與底部殘留|Distinguish sidewall polymer from bottom residue|有益鈍化與有害殘留需要分辨。|Useful passivation must be distinguished from harmful residue.
畫出 OES 訊號與層間界面|Relate OES signals to layer interfaces|發光強度不是直接膜厚。|Emission intensity is not direct thickness.
比較時間停止與端點停止|Compare timed and endpoint-controlled stopping|端點控制仍需延遲與過蝕刻預算。|Endpoint control still needs latency and overetch budgets.
以深度地圖檢查晶圓均勻性|Check wafer uniformity using depth maps|單點端點不能保證全片同時完成。|One endpoint does not guarantee simultaneous wafer completion.
檢查小開口比例對端點訊號的影響|Assess small open-area effects on endpoint signals|開口少可能使反應產物訊號太弱。|Low open area can weaken byproduct signals.
比較腔體清潔前後的速率漂移|Compare rate drift before and after chamber cleaning|腔壁狀態會影響電漿化學。|Wall condition affects plasma chemistry.
建立晶圓背面熱接觸的誤差鏈|Trace backside thermal-contact errors|基板溫度改變反應與鈍化。|Substrate temperature changes reaction and passivation.
檢查微溝槽與底部角落|Inspect microtrenching and bottom corners|局部離子軌跡會形成輪廓異常。|Local ion trajectories can produce profile anomalies.
比較充電前後的元件電性|Compare device electrical behavior after charging exposure|電漿可造成介電層或介面損傷。|Plasma can damage dielectrics or interfaces.
評估去膠與清潔造成的二次改變|Assess secondary changes from stripping and cleaning|後清潔可能改變已形成圖形。|Post-cleaning can modify completed patterns.
將截面尺寸與電阻載具對照|Relate cross-sectional dimensions to resistance vehicles|幾何與電性應共同驗證。|Geometry and electrical behavior need joint verification.
比較不同樣品材料對腔體的污染風險|Compare chamber-contamination risks of sample materials|共用設備需要材料相容性規則。|Shared equipment needs material-compatibility rules.
交付速率、輪廓、選擇性與損傷報告|Report rate, profile, selectivity and damage|RIE 合格判準必須是多維度。|RIE acceptance criteria must be multidimensional.
''',['rie','lametch','endpoint','nisttools'],'a052 a056'.split(),'nist')

add('a052',
['自限制反應|Self-limiting reactions','循環與視窗|Cycles and windows','三維與選擇性|3D and selectivity','電性與效率|Electrical quality and efficiency'],
['ALE 必須以飽和與對照證據確認自限制性，不能只因製程循環就稱為原子層蝕刻。|ALE requires saturation and control evidence of self-limitation; cycling alone is insufficient.','每循環移除量與循環數的關係可能有成核或暫態階段。|Removal per cycle can include nucleation or transient behavior.','方向性、材料選擇性與損傷是不同控制目標。|Directionality, material selectivity and damage are separate control objectives.','小移除量不自動代表無損傷或高效率。|Small removal per cycle does not automatically mean no damage or high efficiency.'],
['任何分段電漿都可直接稱為 ALE。|Any segmented plasma process is automatically ALE.','每個循環必定精確移除一個完整晶格層。|Each cycle necessarily removes exactly one complete lattice plane.','自限制就表示所有材料完全不受影響。|Self-limitation means all other materials are completely unaffected.','蝕刻量很小就完全不需要電性驗證。|Tiny removal eliminates the need for electrical validation.'],
'''
畫出表面改質與移除兩個半循環|Draw surface-modification and removal half-cycles|反應分離是循環控制的核心。|Separated reactions enable cycle control.
比較連續 RIE 與循環 ALE|Compare continuous RIE with cyclic ALE|時間分離改變控制方式而非消除所有反應。|Temporal separation changes control without eliminating all reactions.
設計只有改質步驟的對照|Design a modification-only control|單一步驟對照可檢查非預期移除。|Single-step controls test unintended removal.
設計只有移除步驟的對照|Design a removal-only control|未改質表面的移除量影響協同性。|Removal of unmodified surfaces affects synergy.
計算完整循環與對照的協同程度|Compare full-cycle removal with controls|完整循環需優於獨立步驟的非選擇性效果。|Full cycles must be distinguished from independent nonspecific removal.
列出熱式與電漿式 ALE 的差異|Distinguish thermal and plasma ALE|能量來源會改變方向性與材料適用性。|Energy source changes directionality and material applicability.
繪製改質暴露時間的飽和曲線|Plot modification saturation against exposure time|平台區才支持自限制解釋。|A plateau supports self-limiting interpretation.
繪製移除能量的允許視窗|Plot a permissible removal-energy window|過低可能不移除，過高可能直接濺射。|Too little energy may not remove; too much may sputter directly.
檢查吹除不足造成的混合反應|Assess mixed reactions from insufficient purging|半循環重疊會破壞理想分離。|Overlapping half-cycles undermine ideal separation.
比較前幾循環與穩態循環|Compare initial cycles with steady cycles|表面初始狀態可造成暫態。|Initial surface state can cause transients.
以厚度對循環數求每循環移除量|Fit removal per cycle from thickness versus cycles|線性區間應明確標示。|The fitted linear range must be stated.
計算剩餘薄膜的量測不確定度|Calculate uncertainty in remaining thickness|移除量接近噪聲時需增加可辨識性。|Removal near the noise floor needs improved identifiability.
比較水平與垂直表面的移除|Compare removal on horizontal and vertical surfaces|方向性取決於活化機制。|Directionality depends on the activation mechanism.
檢查高深寬比區的反應物到達|Assess reactant access in high-aspect-ratio features|自限制不代表所有位置即時飽和。|Self-limitation does not imply immediate saturation everywhere.
測試不同材料的飽和與移除|Compare saturation and removal across materials|材料選擇性需實際對照證據。|Material selectivity needs comparative evidence.
將粗糙度頻譜前後疊合|Overlay roughness spectra before and after etching|平均平滑可能掩蓋特定尺度粗糙化。|Mean smoothing can hide roughening at particular scales.
檢查表面改質層是否殘留|Check for residual modified surface layers|幾何完成不等於化學狀態恢復。|Geometric completion does not imply restored chemistry.
分析循環中的再沉積可能性|Assess redeposition during cycles|移除產物仍須有效排出。|Removed products must still be evacuated effectively.
比較閘極凹槽深度與電性|Compare gate-recess depth with electrical behavior|薄層深度差可改變元件特性。|Small depth changes can alter device behavior.
以漏電或介面量測檢查損傷|Check damage through leakage or interface measurements|低能量處理仍需電性證據。|Low-energy processing still needs electrical evidence.
比較 ALE 與 RIE 的總處理時間|Compare total ALE and RIE processing time|循環精度可能犧牲吞吐量。|Cyclic precision can trade against throughput.
建立端點與循環數共同控制|Combine endpoint and cycle-count control|循環計數不能補償所有初始厚度差。|Cycle counting cannot compensate every initial-thickness difference.
記錄材料適用範圍與未驗證條件|Record material scope and untested conditions|一種材料的視窗不能直接移植。|A window for one material cannot be transferred directly.
交付飽和、選擇性及電性證據包|Deliver saturation, selectivity and electrical evidence|自限制主張需要可重現實驗支持。|Self-limitation claims need reproducible experimental support.
''',['ale','atomic','lamale','endpoint'],'a051 a055'.split(),'nist')

add('a053',
['深矽幾何|Deep-silicon geometry','循環與低溫|Cycling and cryogenics','深度與輪廓|Depth and profile','整合與可靠度|Integration and reliability'],
['DRIE 的深度與方向性須同時考慮掩膜、反應物運輸及側壁保護。|DRIE depth and directionality depend on mask, transport and sidewall protection together.','Bosch 循環與低溫製程採用不同鈍化控制，不應混成一組配方。|Bosch and cryogenic processes use different passivation control and must not be combined into one recipe.','深寬比增加會改變離子與中性物種到達底部的機會。|Increasing aspect ratio changes ion and neutral access to the bottom.','深孔完成後的清潔、絕緣與金屬化會決定最終功能。|Cleaning, insulation and metallization after etching determine final functionality.'],
['只延長時間就能維持相同輪廓無限加深。|Longer time preserves the same profile at unlimited depth.','Bosch 與低溫蝕刻的鈍化完全相同。|Bosch and cryogenic passivation are identical.','孔口寬度相同就代表底部速率相同。|Equal opening width proves equal bottom etch rate.','孔洞已打通就等於 TSV 已完成。|An open hole means a completed TSV.'],
'''
用孔深除以孔寬定義深寬比|Define aspect ratio from depth and width|深寬比需註明採用的橫向尺度。|Aspect ratio needs a stated lateral dimension.
比較 MEMS 溝槽與 TSV 孔用途|Compare MEMS trenches with TSV holes|機械釋放與電性連接有不同要求。|Mechanical release and electrical connection have different requirements.
估算硬罩消耗所允許的深度|Estimate mask-limited achievable depth|高選擇比仍需保留厚度裕量。|High selectivity still needs thickness margin.
畫出頂部、側壁與底部的輸運路徑|Draw transport paths to top, walls and bottom|深部表面接收的通量不同。|Deep surfaces receive different fluxes.
標記晶圓背面散熱與支撐|Mark backside cooling and support|深蝕刻熱負載會影響鈍化。|Thermal load affects passivation during deep etching.
規畫開放面積與局部密度取樣|Plan sampling of open area and local density|圖形密度會影響速率與均勻性。|Pattern density affects rate and uniformity.
畫出 Bosch 蝕刻與鈍化交替|Sketch alternating Bosch etch and passivation|交替作用產生方向性也可能形成扇貝紋。|Alternation enables anisotropy and can produce scallops.
比較長短循環的輪廓代價|Compare profile costs of long and short cycles|循環時間會影響粗糙度與效率。|Cycle timing affects roughness and efficiency.
解釋低溫侧壁保護的角色|Explain cryogenic sidewall protection|低溫改變表面反應与鈍化平衡。|Low temperature changes surface reaction and passivation balance.
比較兩種製程的溫度敏感性|Compare temperature sensitivity of both processes|熱接觸差異可造成輪廓差異。|Thermal-contact differences can alter profiles.
檢查鈍化過多與不足的截面|Inspect profiles with excessive and insufficient passivation|過量可阻塞，過少可造成側蝕。|Excess can block etching; deficiency can cause lateral erosion.
追蹤循環參數隨深度的控制概念|Track the concept of depth-dependent cycle control|深度增加時輸運條件會改變。|Transport conditions change as depth increases.
比較不同孔徑的蝕刻延遲|Compare etch lag at different opening sizes|深寬比相依速率可能造成深度差。|Aspect-ratio-dependent rate can create depth differences.
量測頂寬、底寬與側壁角|Measure top width, bottom width and wall angle|只量測孔口不能描述截面。|Opening width alone cannot describe the section.
計算扇貝紋的振幅與週期|Measure scallop amplitude and period|扇貝紋會影響後續覆蓋與應力。|Scallops affect subsequent coverage and stress.
辨識底部缺口與介電停止層充電|Identify notching near a dielectric stop|底部電場改變可能導致側向異常。|Changed bottom fields can cause lateral anomalies.
檢查晶圓中心與邊緣的深度圖|Inspect center-to-edge depth maps|全片均勻性與局部深寬比效應不同。|Wafer uniformity differs from local aspect-ratio effects.
比較時間控制與光學端點證據|Compare timed control with optical endpoint evidence|端點訊號需能辨識實際停止層。|Endpoint signals must identify the actual stop layer.
評估側壁殘留去除的需求|Assess removal of sidewall residue|殘留會影響絕緣與黏著。|Residue affects insulation and adhesion.
畫出深孔絕緣層的覆蓋困難|Sketch insulation-coverage challenges in deep holes|蝕刻輪廓決定後續可沉積性。|Etch profile determines later depositability.
比較深孔金屬填充與機械釋放驗收|Compare metal-fill and mechanical-release acceptance|用途不同會改變允許粗糙度與殘留。|Application changes acceptable roughness and residue.
檢查薄結構翹曲與破裂|Inspect warpage and fracture of thin structures|幾何深度之外還需機械穩定性。|Mechanical stability matters beyond geometric depth.
建立對照截面與功能量測|Pair cross sections with functional measurements|形貌合格不自動證明功能合格。|Acceptable morphology does not automatically prove function.
交付深度、側壁與後續相容性報告|Report depth, walls and downstream compatibility|DRIE 應作為整合流程的一部分驗收。|DRIE should be accepted as part of an integrated flow.
''',['drie','caltechdrie','rie','endpoint'],'a051 a065'.split(),'nist')

add('a054',
['介電堆疊|Dielectric stacks','輸運與充電|Transport and charging','輪廓控制|Profile control','端點與功能|Endpoint and function'],
['高深寬比介電蝕刻要同時管理硬罩消耗、帶電粒子与反應物輸運。|High-aspect-ratio dielectric etching jointly manages mask consumption, charged particles and reactant transport.','絕緣側壁可能累積電荷並改變離子路徑。|Insulating walls can accumulate charge and alter ion trajectories.','孔形狀由不同深度的局部反應平衡決定。|Hole shape follows local reaction balances at different depths.','完整貫穿不等於孔底損傷、殘留與後續覆蓋合格。|Complete penetration does not prove acceptable bottom damage, residue or later coverage.'],
['開口相同就代表所有深度的通量相同。|Equal openings imply equal flux at every depth.','介電層沒有自由電子，所以不會充電。|Dielectrics cannot charge because they lack free electrons.','孔口圓形可保證整孔筆直。|A circular opening guarantees a straight hole.','只檢查是否打通即可驗收。|Checking breakthrough alone is sufficient.'],
'''
畫出交替介電層與目標通道|Draw alternating dielectric layers and the target channel|不同材料層可能有不同移除速率。|Different layers can have different removal rates.
定義深度、最小孔徑與偏斜量|Define depth, minimum diameter and deviation|輪廓需要多個幾何指標。|Profiles require multiple geometric metrics.
估算硬罩厚度與孔口縮窄|Estimate mask thickness and opening narrowing|厚硬罩也會增加入口輸運限制。|Thick masks can also restrict entrance transport.
比较單層與多層堆疊模型|Compare single-layer and multilayer models|單一平均材料不能捕捉層間反應差異。|An average material misses layer-specific reactions.
標記開口密度與全片負載|Mark open-area density and wafer loading|圖形布局會影響反應物供應。|Layout influences reactant supply.
建立孔底允許損傷的功能需求|Define allowable bottom damage from function|停止位置需連結後續接觸或儲存功能。|Stop position must relate to later contact or storage function.
畫出離子與自由基的不同入孔路徑|Draw distinct ion and radical entry paths|方向性物種與中性物種傳輸不同。|Directional and neutral species travel differently.
比較高深寬比下的反應物耗盡|Assess reactant depletion at high aspect ratio|孔底反應可能受輸運而非源端濃度限制。|Bottom reactions can be transport-limited rather than source-limited.
分析電子與離子到達不對稱|Analyze unequal electron and ion access|到達差異可形成局部電位。|Unequal access can create local potentials.
畫出充電偏折造成的孔道彎曲|Sketch charging-induced channel deflection|局部電場可能使孔道偏离垂直。|Local fields can deflect channels from vertical.
比較連續與脈衝控制的研究目標|Compare goals of continuous and pulsed control|脈衝設計可影響充電與反應歷程。|Pulsing can alter charging and reaction history.
檢查孔內副產物排出的限制|Assess byproduct-removal limitations|產物滯留可能抑制反應或再沉積。|Retained products can inhibit reaction or redeposit.
量測孔口、最大膨脹處與孔底|Measure opening, maximum bow and bottom|單一截面寬度不足以描述弓形。|One width cannot characterize bowing.
比較側壁保護不足與過量|Compare insufficient and excess wall protection|保護不足會側蝕，過量會使孔收窄。|Insufficient protection erodes walls; excess narrows holes.
檢查局部材料層造成的條紋|Inspect striations associated with local layers|層間速率差可能留在側壁形貌中。|Layer-rate differences can remain in wall morphology.
追蹤孔道扭曲與設計落點|Trace channel twist against the intended landing|孔底偏移會破壞層間連接。|Bottom displacement can disrupt interlayer connection.
比較不同孔徑的深度延遲|Compare depth lag across diameters|尺寸差異會造成完成時間分散。|Size differences spread completion times.
評估遮罩侵蝕造成的孔口擴大|Assess opening growth caused by mask erosion|早期遮罩變化會傳入深部輪廓。|Early mask changes propagate into deep profiles.
選擇能辨識堆疊底部的端點證據|Choose endpoint evidence for the stack bottom|發光訊號需對應特定材料轉換。|Emission signals must map to a specific material transition.
為最慢孔與最快孔分配過蝕刻裕量|Budget overetch for the slowest and fastest holes|補足慢孔會增加快孔損傷風險。|Finishing slow holes increases damage risk in fast holes.
檢查孔底殘留與局部表面化學|Inspect bottom residue and surface chemistry|幾何打通可能仍有絕緣殘留。|Geometric breakthrough can still leave insulating residue.
比較後續共形膜的覆蓋品質|Compare subsequent conformal-film coverage|蝕刻輪廓會限制沉積和填孔。|Etch profiles constrain deposition and fill.
將孔道形貌與電性分布連結|Relate channel morphology to electrical distributions|局部幾何差異可造成元件散布。|Local geometric differences can cause device variation.
交付含深度剖面的整合風險圖|Deliver an integration-risk map with depth profiles|高深寬比驗證必須涵蓋整個深度。|High-aspect-ratio validation must cover the full depth.
''',['lametch','lamemory','endpoint','rie'],'a053 a056'.split(),'nist')

add('a055',
['材料與選擇性|Materials and selectivity','反應與幾何|Reaction and geometry','釋放與表面|Release and surfaces','元件整合|Device integration'],
['選擇性蝕刻是材料對的相對速率，不是目標外材料絕對零損失。|Selective etching is a relative rate for a material pair, not necessarily zero loss elsewhere.','SiGe 組成、應變、表面與幾何都可能改變反應。|SiGe composition, strain, surfaces and geometry can change reaction behavior.','側向釋放需要檢查深部移除與保留矽的完整性。|Lateral release needs checks of deep removal and retained-silicon integrity.','通道釋放或停止層移除都需與後續介面品質聯動。|Channel release and stop-layer removal both require downstream interface validation.'],
['高選擇比表示矽完全沒有任何損失。|High selectivity means absolutely no silicon loss.','所有鍺比例的 SiGe 都有相同反應速率。|Every SiGe composition has the same reaction rate.','孔口乾淨就表示內部完全釋放。|A clean opening proves complete internal release.','釋放完成即可省略閘極介面驗證。|Completed release removes the need for gate-interface checks.'],
'''
畫出交替矽與矽鍺奈米片|Draw alternating Si and SiGe nanosheets|犧牲層與保留通道的角色不同。|Sacrificial layers and retained channels serve different roles.
比較通道釋放與背面停止層移除|Compare channel release with backside stop removal|兩用途有不同幾何與終點要求。|The two uses have different geometries and endpoints.
用兩材料損失定義選擇比|Define selectivity from loss of both materials|極小分母需要量測偵測限。|A very small denominator requires a detection limit.
標明 SiGe 組成與應變狀態|State SiGe composition and strain|材料標籤不足以描述反應條件。|A material label is insufficient to describe reaction conditions.
建立保留矽厚度損失預算|Budget allowable retained-silicon loss|通道厚度損失可能改變電性。|Channel-thickness loss can alter electrical behavior.
列出不同晶面與摻雜的可能影響|List possible orientation and doping effects|材料微觀狀態可影響表面反應。|Microscopic material state can affect surface reactions.
分開表面反應與反應物輸運|Separate surface reaction from reactant transport|狹窄間隙可能由輸運限制。|Narrow gaps can be transport-limited.
比較各向同性移除與方向性蝕刻|Compare isotropic removal with directional etching|通道側向釋放通常需要側向進入。|Lateral channel release requires lateral access.
畫出反應物到達中間層的路徑|Trace reactant access to middle layers|最外層完成不代表中間層完成。|Outer-layer completion does not prove middle-layer completion.
檢查原生氧化層對反應起始的影響|Assess native-oxide effects on reaction initiation|起始延遲可造成層間差異。|Initiation delays can create layer-to-layer differences.
以空白矽與 SiGe 試片建立對照|Use blanket Si and SiGe controls|平面對照有助於分離材料因素。|Blanket controls help isolate material effects.
比較平面速率與奈米間隙有效速率|Compare blanket rates with nanogap effective rates|平面速率不能無條件代入三維結構。|Blanket rates cannot be inserted unconditionally into 3D structures.
由截面辨識未移除的 SiGe 殘留|Identify residual SiGe in sections|局部殘留會阻礙後續閘極包覆。|Local residue can obstruct later gate wrapping.
檢查通道頂底的厚度差|Inspect thickness differences across channels|選擇性損失可能隨位置不同。|Selective loss can vary by location.
比較釋放前後的粗糙度|Compare roughness before and after release|小平均損失仍可能增加粗糙度。|Small average loss can still increase roughness.
評估釋放後奈米片的機械穩定|Assess released-sheet mechanical stability|薄片可能因應力或表面力變形。|Thin sheets can deform under stress or surface forces.
檢查清潔後的元素與氧化狀態|Inspect elements and oxidation states after cleaning|清潔度需以化學量測支持。|Cleanliness needs chemical measurement evidence.
標出內間隔層需保留的區域|Mark inner-spacer regions to preserve|選擇性需涵蓋完整周邊材料集合。|Selectivity must cover the full surrounding material set.
比較閘極共形沉積前的表面條件|Compare surfaces before conformal gate deposition|釋放表面直接影響介面品質。|Released surfaces directly affect interface quality.
用漏電與臨界電壓檢查後果|Assess consequences through leakage and threshold voltage|幾何差異可能表現在電性散布。|Geometric differences can appear as electrical variation.
追蹤三維堆疊中各層的性能|Track performance across layers in a 3D stack|平均元件值可能掩蓋單層異常。|Average device values can hide one-layer anomalies.
比較選擇性提升與總時間代價|Compare improved selectivity with total-time cost|更溫和移除可能延長製程。|Gentler removal can lengthen processing.
記錄不能跨組成外推的條件|Document conditions not transferable across compositions|特定材料對的結果不是通用配方。|A result for one material pair is not a universal recipe.
交付釋放、表面與元件的證據鏈|Deliver release, surface and device evidence|成功整合需要形貌與功能共同支持。|Successful integration needs morphological and functional support.
''',['selective','shape','backside','ale'],'a052 a025'.split())

add('a056',
['訊號來源|Signal origins','訊號處理|Signal processing','停止邏輯|Stop logic','驗證與漂移|Validation and drift'],
['端點偵測是從間接光學或電性訊號推斷製程狀態。|Endpoint detection infers process state from indirect optical or electrical signals.','訊號濾波會影響噪聲與延遲，不能只追求平滑。|Filtering affects noise and latency, so smoothness is not the sole objective.','停止邏輯需兼顧誤觸發、漏檢及控制延遲。|Stop logic must balance false triggers, misses and control latency.','端點模型需要以實際剩餘膜厚與腔體歷程持續驗證。|Endpoint models need validation against remaining thickness and chamber history.'],
['所有亮度變化都等於材料已蝕刻完。|Every brightness change means etching is complete.','把濾波時間拉長永遠更好。|Longer filtering is always better.','偵測到端點後所有反應立即停止。|All reactions stop instantly when endpoint is detected.','一次校準後不需要再量膜厚。|One calibration removes the need for further thickness measurement.'],
'''
把 OES 發光峰對應至可能物種|Associate OES peaks with candidate species|峰值指認需排除重疊與背景。|Peak assignments need overlap and background checks.
比較反應物消耗與產物生成訊號|Compare reactant depletion with product-generation signals|不同訊號可能在端點反向變化。|Signals can change in opposite directions at endpoint.
畫出薄膜反射干涉的訊號|Sketch thin-film reflection-interference signals|條紋與光學厚度有關。|Fringes depend on optical thickness.
區分界面端點與指定深度端點|Distinguish interface endpoints from target-depth endpoints|兩者需要不同判讀模型。|They require different interpretation models.
標示量測視野與實際開口區|Mark the viewing area and actual open regions|感測訊號可能平均多個位置。|Sensor signals can average multiple locations.
比較大開口與小開口訊號強度|Compare large- and small-open-area signals|小開口可能降低可偵測性。|Low open area can reduce detectability.
建立曝光前背景與暗訊號|Establish background and dark signals|背景扣除需要穩定的參考。|Background subtraction needs a stable reference.
比較單一波長與峰值比值|Compare one wavelength with peak ratios|比值可減少部分共同強度漂移。|Ratios can reduce some common intensity drift.
以合成資料測試移動平均延遲|Test moving-average delay using synthetic data|平滑會把轉折向後移。|Smoothing delays apparent transitions.
比較斜率與絕對強度判準|Compare slope and absolute-intensity criteria|兩種判準對背景漂移敏感度不同。|The criteria differ in sensitivity to baseline drift.
辨識脈衝或點火暫態的假端點|Identify false endpoints from pulses or ignition|初期暫態應與材料轉換分離。|Startup transients need separation from material transitions.
記錄訊號飽和與資料缺失|Record saturation and missing data|無效訊號不能直接視為合格。|Invalid signals must not be treated as acceptance.
設計持續時間確認以避免誤觸發|Require persistence to reduce false triggers|確認時間也增加停止延遲。|Persistence confirmation adds stop delay.
將感測、判讀與機台停止延遲分帳|Separate sensing, decision and tool-stop delays|總延遲決定額外移除量。|Total latency determines extra removal.
以速率估算延遲造成的過蝕刻|Estimate overetch caused by latency|速率不確定度會傳入深度誤差。|Rate uncertainty propagates into depth error.
設計端點未出現時的逾時分流|Define timeout handling when no endpoint appears|逾時是異常而非正常完工證據。|Timeout is an anomaly, not proof of completion.
比較最快與最慢區域的停止需求|Compare stop needs of the fastest and slowest regions|全片完成度可能需要有限過蝕刻。|Whole-wafer completion may need bounded overetch.
區分腔體清潔端點與晶圓端點|Distinguish chamber-cleaning and wafer endpoints|相同物種訊號可代表不同反應狀態。|The same species signal can indicate different process states.
以截面膜厚驗證端點判讀|Validate endpoint decisions using cross-sectional thickness|直接量測提供外部參考。|Direct measurements provide an external reference.
用盲測批次檢驗判讀門檻|Test thresholds on held-out lots|門檻需在未調整資料上驗證。|Thresholds need validation on untuned data.
追蹤視窗污染造成的光學漂移|Track optical drift from window contamination|透光變化會改變量測基線。|Transmission changes alter the measurement baseline.
比較清潔前後的模型可用性|Compare model validity before and after cleaning|腔體重置可能改變訊號特徵。|Chamber reset can change signal features.
建立誤停與漏停的成本矩陣|Build a cost matrix for early and missed stops|兩種失敗的後果可能不對稱。|The consequences of the two failures can be asymmetric.
交付具回溯資料的端點控制計畫|Deliver an endpoint plan with traceable data|每次停止應能對應訊號與膜厚證據。|Each stop should link to signal and thickness evidence.
''',['endpoint','endpointblog','ale','lametch'],'a051 a054'.split(),'nist')

add('a057',
['電漿與成膜|Plasma and growth','膜性與應力|Film properties and stress','三維覆蓋|3D coverage','整合與可靠度|Integration and reliability'],
['PECVD 利用電漿活化反應，較低基板溫度不代表所有損傷都較低。|PECVD activates reactions with plasma; lower substrate temperature does not guarantee lower total damage.','膜厚、化學組成、氫含量與應力是不同材料指標。|Thickness, composition, hydrogen content and stress are distinct film metrics.','頂部沉積均勻性不代表三維側壁共形性。|Uniform top-surface deposition does not establish 3D conformality.','介電與機械驗證需依用途制定，不能只測折射率。|Electrical and mechanical validation must match application, not rely only on index.'],
['較低溫度就能保證完全無電漿損傷。|Lower temperature guarantees no plasma damage.','厚度相同就表示介電品質相同。|Equal thickness proves equal dielectric quality.','平面均勻就表示所有側壁等厚。|Planar uniformity proves equal sidewall thickness.','折射率合格即可取代漏電測試。|Passing refractive index replaces leakage testing.'],
'''
畫出電漿活化到表面反應路徑|Trace plasma activation into surface growth|氣相與表面反應共同參與沉積。|Gas-phase and surface reactions both contribute to deposition.
比較熱 CVD 與 PECVD 能量来源|Compare energy sources in thermal CVD and PECVD|電漿可降低部分熱活化需求。|Plasma can reduce some thermal-activation requirements.
列出基板可接受的熱預算|List the substrate thermal budget|低溫整合仍需評估累積熱史。|Low-temperature integration still needs cumulative thermal history.
分開沉積與離子轟擊的作用|Separate deposition from ion-bombardment effects|轟擊可能改變密度與損傷。|Bombardment can alter density and damage.
建立基板前處理的對照組|Create controls for substrate pretreatment|初始表面影響成核與黏著。|Initial surfaces affect nucleation and adhesion.
選擇絕緣、保護或側壁用途|Choose insulation, passivation or spacer use|不同用途需要不同膜性目標。|Different uses require different film-property targets.
量測膜厚與折射率並檢查模型|Measure thickness and index while checking the model|橢圓偏光擬合參數可能相關。|Ellipsometric fit parameters can be correlated.
用光譜辨識氫相關鍵結|Identify hydrogen-related bonds spectroscopically|氫可影響後續熱穩定與電性。|Hydrogen can affect later thermal stability and electrical behavior.
以晶圓曲率估算薄膜應力|Estimate film stress from wafer curvature|Stoney 近似需滿足薄膜與基板條件。|The Stoney approximation requires suitable film and substrate conditions.
比較拉伸與壓縮應力的失效|Compare tensile- and compressive-stress failures|兩種應力可能導致裂紋或剝離等不同結果。|The stress signs can produce different cracking or delamination outcomes.
將濕蝕刻速率作為輔助膜性指標|Use wet-etch rate as a supplementary film metric|速率不是膜密度或電性的唯一證据。|Rate is not sole evidence of density or electrical quality.
比較沉積後與熱處理後的膜性|Compare as-deposited and annealed properties|後續熱史可能改變氫與應力。|Later thermal history can change hydrogen and stress.
畫出溝槽頂部、側壁與底部厚度|Map thickness at trench top, walls and bottom|共形性需以位置比值表達。|Conformality needs location-dependent ratios.
比較高黏著機率與反應物耗盡|Compare high sticking probability with reactant depletion|入口消耗會限制深部覆蓋。|Entrance consumption can limit deep coverage.
辨識夾縫封口與內部空洞|Identify pinch-off and internal voids|表面閉合不能證明內部填滿。|Surface closure does not prove internal fill.
量測晶圓邊緣與中心膜厚|Measure edge and center thickness|晶圓內均勻性需要空間統計。|Within-wafer uniformity needs spatial statistics.
檢查顆粒與腔壁沉積關聯|Relate particles to chamber-wall deposition|腔壁膜可能形成顆粒來源。|Wall films can become particle sources.
比較腔體清潔前後的成膜漂移|Compare deposition drift around chamber cleaning|腔壁狀態可能改變製程再現性。|Wall condition can alter process repeatability.
以電容結構估算介電常數|Estimate permittivity using capacitor structures|面積、厚度與邊緣效應需分辨。|Area, thickness and fringe effects need separation.
量測漏電隨電場的關係|Measure leakage versus electric field|相同電壓在不同厚度有不同電場。|Equal voltage gives different fields at different thicknesses.
比較介面陷阱與體材料缺陷|Distinguish interface traps from bulk defects|介面與體材料需要不同量測解釋。|Interface and bulk behavior need different interpretations.
檢查膜層與金屬接觸的黏著|Assess adhesion to metal-contact regions|介面污染可降低附著與可靠度。|Interface contamination can weaken adhesion and reliability.
追蹤濕度或熱循環後的變化|Track changes after humidity or thermal cycling|初始合格不代表長期穩定。|Initial acceptance does not prove long-term stability.
交付膜性、覆蓋與可靠度矩陣|Deliver a property–coverage–reliability matrix|PECVD 材料需按整合用途驗收。|PECVD films need application-specific acceptance.
''',['lamdep','oxpecvd','nisttools','lamemory'],'a058 a064'.split(),'nist')

add('a058',
['熱反應與低壓|Thermal reaction and low pressure','批次與均勻性|Batch and uniformity','材料與膜性|Materials and film properties','整合與品質|Integration and quality'],
['LPCVD 的速率受表面反應與氣體輸運共同限制。|LPCVD rate is jointly constrained by surface reactions and gas transport.','批次位置、溫度分布與前驅物耗盡會造成不均勻。|Batch position, temperature distribution and precursor depletion cause nonuniformity.','不同 LPCVD 材料有不同結構、應力與熱預算要求。|Different LPCVD materials have different structure, stress and thermal-budget requirements.','高溫成膜必須與已有元件、摻雜及金屬相容。|High-temperature growth must remain compatible with existing devices, dopants and metals.'],
['降低壓力必定增加所有材料的沉積速率。|Lower pressure necessarily increases every deposition rate.','同一批次所有位置自然完全相同。|Every batch position is inherently identical.','所有 LPCVD 膜都具有相同低應力。|Every LPCVD film has the same low stress.','膜質好就可以忽略元件熱預算。|Good film quality removes device thermal-budget concerns.'],
'''
畫出進氣、熱區與排氣的流程|Draw inlet, heated zone and exhaust|氣體歷程會影響基板反應。|Gas history affects substrate reaction.
比較反應限制與輸運限制區|Compare reaction-limited and transport-limited regimes|不同區域有不同溫度與流量敏感性。|Regimes differ in temperature and flow sensitivity.
用概念 Arrhenius 圖辨識熱活化|Use a conceptual Arrhenius plot to identify activation|斜率解釋需限於相同反應機制。|Slope interpretation requires the same reaction mechanism.
分開總壓與前驅物分壓|Separate total pressure from precursor partial pressure|相同總壓可能有不同反應物供應。|Equal total pressure can have different reactant supply.
列出晶圓間距與表面積負載|List wafer spacing and exposed surface load|批次裝載會改變耗盡程度。|Batch loading changes depletion.
建立已加工元件的熱預算清單|Build a thermal-budget list for processed devices|可沉積溫度受前段歷程限制。|Allowable temperature is constrained by earlier processing.
規畫沿爐管方向的見證片|Plan witness wafers along the furnace|軸向取樣可揭露反應物與溫度梯度。|Axial sampling reveals reactant and temperature gradients.
比較單片中心與邊緣膜厚|Compare within-wafer center and edge thickness|批間與片內不均勻需分開。|Batch and within-wafer nonuniformity need separation.
檢查入氣端到出氣端的耗盡|Inspect depletion from inlet to outlet|上游沉積會改變下游供應。|Upstream deposition changes downstream supply.
以空載與滿載假設比較成膜|Compare hypothetical lightly and fully loaded growth|装載差異需要一致的對照條件。|Loading differences require controlled comparisons.
追蹤爐管清潔前後的膜厚變化|Track thickness around tube cleaning|管壁狀態可改變再現性。|Tube-wall state can alter repeatability.
比較升溫與穩溫階段的貢獻|Compare ramp and soak contributions|有效熱史不只有名目沉積時間。|Effective thermal history extends beyond nominal deposition time.
比較非晶矽與多晶矽的結構證據|Compare evidence for amorphous and polycrystalline silicon|相同元素不代表相同微結構。|The same element does not imply the same microstructure.
分開化學計量氮化矽與低應力氮化矽|Distinguish stoichiometric and low-stress silicon nitride|低應力命名不保證所有膜性一致。|A low-stress label does not guarantee identical properties.
比較 LTO 與其他氧化層的整合用途|Compare LTO with other oxide uses|成膜方式會影響密度、雜質與熱史。|Growth method affects density, impurities and thermal history.
量測膜厚、折射率與化學鍵結|Measure thickness, index and chemical bonds|多種量測可減少單一模型歧義。|Multiple measurements reduce single-model ambiguity.
由曲率變化估算應力符號|Infer stress sign from curvature change|應力估算依賴基板與薄膜假設。|Stress estimation depends on substrate and film assumptions.
檢查厚膜裂紋與邊緣剝離|Inspect thick-film cracks and edge delamination|累積應力能量可能超過介面耐受。|Accumulated strain energy can exceed interface resistance.
評估側壁覆蓋與狹窄溝槽封口|Assess sidewall coverage and trench pinch-off|共形沉積仍可能封口留下空洞。|Conformal growth can still pinch off and leave voids.
比較沉積前後的摻雜分布需求|Assess dopant-profile constraints before and after growth|高溫可能改變摻雜擴散。|High temperature can alter dopant diffusion.
檢查既有金屬的材料相容性|Check compatibility of existing metals|共用爐管通常有嚴格材料限制。|Shared furnaces commonly have strict material restrictions.
以電性載具驗證介電或導電用途|Verify insulating or conducting function electrically|外觀均勻不代表功能符合。|Uniform appearance does not establish function.
建立批次位置與最終良率對照|Relate batch position to final yield|位置相關性可提供製程來源線索。|Position dependence can identify process-origin clues.
交付熱史、均勻性與材料驗收|Deliver thermal history, uniformity and material acceptance|LPCVD 需將批次管理納入整合。|LPCVD integration must include batch management.
''',['lpcvd','nistpoly','nistnitride','nistlto'],'a057 a059'.split(),'nist')

add('a059',
['前驅物與磊晶|Precursors and epitaxy','反應器與均勻性|Reactor and uniformity','結構與光電性|Structure and optoelectronics','界面與整合|Interfaces and integration'],
['MOCVD 的氣相輸運、前驅物分解與表面結晶須共同分析。|MOCVD requires joint analysis of gas transport, precursor decomposition and surface crystallization.','反應器流場與溫度場共同影響成分與厚度。|Reactor flow and temperature jointly affect composition and thickness.','厚度、合金組成、應變與缺陷都會影響光電性能。|Thickness, alloy composition, strain and defects all affect optoelectronic behavior.','本課程以公開原理和模擬資料分析，不提供有毒或自燃前驅物操作配方。|This course analyzes public principles and simulated data, not operating recipes for toxic or pyrophoric precursors.'],
['氣相混合均勻就能保證晶體完全無缺陷。|Uniform gas mixing guarantees defect-free crystals.','每片晶圓只需相同轉速即可均勻。|Equal rotation speed alone ensures uniform wafers.','發光強度相同就代表晶體品質完全相同。|Equal emission intensity proves identical crystal quality.','研究配方可直接搬到任意反應器。|A research recipe transfers directly to any reactor.'],
'''
畫出金屬有機源到晶體薄膜的路徑|Trace metal-organic sources into crystalline films|氣相分解與表面反應不是同一階段。|Gas decomposition and surface reaction are different stages.
區分同質與異質磊晶|Distinguish homoepitaxy from heteroepitaxy|基板與薄膜晶格关系影響缺陷。|Film–substrate lattice relations affect defects.
比較 III–V 材料不同元素來源的角色|Compare precursor roles in III–V materials|元素供應比不直接等於固體組成比。|Supply ratio does not directly equal solid composition.
繪製反應限制與輸運限制示意|Sketch reaction- and transport-limited regimes|速率控制機制可隨條件改變。|Rate-control mechanisms can change with conditions.
標記氣體隔離、監測與排放介面|Mark gas isolation, monitoring and exhaust interfaces|反應器分析需包含設施介面。|Reactor analysis must include facility interfaces.
建立不含操作配方的材料需求表|Build a material-requirement table without recipes|公開材料目標與現場操作授權不同。|Public material targets differ from operational authorization.
比較行星式與近距離淋浴式反應器|Compare planetary and close-coupled showerhead reactors|氣體導入與基板運動方式不同。|Gas delivery and substrate motion differ.
畫出邊界層與表面物種耗盡|Sketch boundary layers and surface-species depletion|表面供應不等於入口濃度。|Surface supply differs from inlet concentration.
檢查晶圓溫度與載盤溫度差|Assess wafer–susceptor temperature differences|控制器溫度不必然等於表面溫度。|Controller temperature need not equal surface temperature.
比較中心與邊緣的成分地圖|Compare center-to-edge composition maps|厚度均勻不保證成分均勻。|Thickness uniformity does not guarantee composition uniformity.
分析晶圓翹曲對熱接觸的影響|Analyze bow effects on thermal contact|翹曲可改變溫度與成長分布。|Bow can alter temperature and growth distribution.
以見證片追蹤反應器歷程|Use witness samples to track reactor history|腔壁沉積可能帶來記憶效應。|Wall deposits can create memory effects.
用 XRD 概念分開晶格常數與應變|Use XRD concepts to distinguish lattice parameter and strain|峰位改變可能有多種來源。|Peak shifts can have multiple origins.
比較光激發光峰位與線寬|Compare photoluminescence peak position and width|光譜需要結合厚度、成分與缺陷解釋。|Spectra need interpretation with thickness, composition and defects.
畫出量子井與障壁的能帶示意|Sketch quantum-well and barrier band profiles|能階也依賴井寬與材料參數。|Levels depend on well width and material parameters.
檢查界面漸變對量子井的影響|Assess graded interfaces in quantum wells|氣體切換不一定形成瞬間銳利界面。|Gas switching need not create instantly sharp interfaces.
比較缺陷密度與發光效率證據|Compare defect-density and emission-efficiency evidence|單一光譜指標不能唯一決定缺陷密度。|One spectral metric cannot uniquely determine defect density.
以霍爾量測概念分開濃度與遷移率|Separate carrier density and mobility through Hall concepts|導電率同時依賴兩者。|Conductivity depends on both.
追蹤摻雜切換與記憶效應|Track dopant switching and memory effects|先前成長歷程可能污染後續層。|Previous growth history can affect later layers.
比較緩衝層與主動層的功能|Compare buffer and active-layer functions|緩衝層可能處理應變與缺陷傳遞。|Buffers can manage strain and defect propagation.
檢查成長後冷卻造成的熱應力|Assess thermal stress during cooldown|熱膨脹不匹配可能造成裂紋。|Thermal-expansion mismatch can cause cracking.
建立跨片厚度與光電性能對照|Relate wafer thickness maps to optoelectronic maps|多圖疊合有助於辨識共同來源。|Map overlays help identify shared origins.
區分研究磊晶片與產品製程資格|Distinguish research epitaxy from product qualification|研究性能不等於產品可靠度。|Research performance is not product reliability.
交付反應器、結構與性能的證據链|Deliver reactor, structure and performance evidence|可重現成長需要完整條件與量測範圍。|Reproducible growth needs complete conditions and measurement scope.
''',['mocvd','planetary','showerhead','aixhistory'],'a058 a060'.split(),'nist')

add('a060',
['動量與輸運|Momentum and transport','靶材與電漿|Targets and plasma','薄膜與介面|Films and interfaces','圖案與驗收|Patterns and acceptance'],
['濺鍍以粒子動量移除靶原子並沉積，與蒸發及化學沉積不同。|Sputtering ejects target atoms by momentum transfer and differs from evaporation and chemical deposition.','放電方式與靶材導電性相互限制。|Discharge mode and target conductivity constrain each other.','薄膜密度、應力與粗糙度取決於到達粒子與表面遷移。|Film density, stress and roughness depend on arriving particles and surface mobility.','平面膜質合格不保證深孔覆蓋或抬離品質。|Acceptable planar films do not guarantee deep-hole coverage or lift-off quality.'],
['濺鍍就是把靶材煮沸。|Sputtering simply boils the target.','所有絕緣靶都能直接使用相同 DC 放電。|Every insulating target can use the same DC discharge.','較厚薄膜一定較低應力。|Thicker films necessarily have lower stress.','平面膜厚可代表所有側壁。|Planar thickness represents every sidewall.'],
'''
畫出離子撞擊靶材與原子逸出|Sketch ion impact and target-atom ejection|濺鍍產率依入射與材料條件改變。|Sputter yield depends on incidence and material conditions.
比較濺鍍、蒸發與 CVD 的物質來源|Compare material sources in sputtering, evaporation and CVD|不同來源造成不同覆蓋與污染議題。|Sources create different coverage and contamination issues.
繪製靶到晶圓的角度分布|Sketch target-to-wafer angular distributions|到達方向會影響陰影區覆蓋。|Arrival direction affects shadowed coverage.
以平均自由程概念比較碰撞|Compare collisions using mean-free-path concepts|壓力會改變粒子輸運與能量。|Pressure changes particle transport and energy.
分開基壓與製程壓力|Separate base pressure from working pressure|殘餘氣體與工作氣體有不同角色。|Residual and working gases have different roles.
建立靶材、基板與污染相容性表|Build target–substrate contamination compatibility|共用設備需要追蹤材料交叉污染。|Shared equipment needs cross-contamination tracking.
比較 DC 與 RF 濺鍍適用性|Compare DC and RF sputtering applicability|導電性影響穩定放電方式。|Conductivity affects stable discharge modes.
畫出磁控場對電子路徑的影響|Sketch magnetron effects on electron paths|磁控可增加近靶區電離效率。|Magnetron confinement can improve ionization near the target.
檢查靶面侵蝕區與使用歷程|Inspect target erosion tracks and use history|靶面狀態可能改變均勻性。|Target condition can change uniformity.
比較預濺鍍與正式沉積的目的|Compare pre-sputter and deposition purposes|靶面清理不等於基板清理。|Target cleaning is not substrate cleaning.
以反應式濺鍍概念畫靶中毒迴圈|Sketch target-poisoning hysteresis in reactive sputtering|反應氣體可改變靶面與放電。|Reactive gas can change target surfaces and discharge.
分開離子束沉積與偏壓靶沉積|Distinguish ion-beam and biased-target deposition|能量控制方式會影響介面混合。|Energy-control methods affect interface mixing.
量測厚度地圖並計算均勻性|Map thickness and calculate uniformity|均勻性公式與取樣範圍需明示。|Uniformity definition and sampling range must be stated.
比較沉積速率與時間的線性|Test linearity of thickness with time|起始與靶面變化可能造成非線性。|Startup and target changes can cause nonlinearity.
用曲率檢查應力符號|Check stress sign through curvature|應力需與膜厚和基板條件一起解釋。|Stress needs interpretation with thickness and substrate conditions.
比較 AFM 粗糙度與密度指標|Compare AFM roughness with density measures|表面平滑不能單獨證明高密度。|Smoothness alone does not prove high density.
檢查介面氧化與黏著問題|Inspect interface oxidation and adhesion|真空中轉移可減少部分再氧化。|Vacuum transfer can reduce some reoxidation.
量測薄膜片電阻與連續性|Measure sheet resistance and continuity|超薄膜可能未形成連續導電路徑。|Ultrathin films may lack continuous conducting paths.
比較階梯頂部與側壁覆蓋|Compare coverage on step tops and sidewalls|方向性輸運可造成陰影。|Directional transport can create shadows.
評估深孔入口懸垂與底部覆蓋|Assess overhang and bottom coverage in deep holes|入口增厚可能阻礙後續填孔。|Entrance thickening can obstruct later fill.
檢查抬離圖形的側壁金屬連接|Inspect sidewall metal bridges in lift-off patterns|過度側壁覆蓋可能妨礙抬離。|Excess sidewall coating can hinder lift-off.
比較多層連續沉積與中途曝氣|Compare continuous multilayers with air breaks|曝氣可能增加介面污染。|Air breaks can increase interface contamination.
追蹤熱處理後電阻與應力|Track resistance and stress after annealing|後續熱史可能改變晶粒與介面。|Later heating can change grains and interfaces.
交付厚度、介面、電性與覆蓋證據|Deliver thickness, interface, electrical and coverage evidence|薄膜用途決定驗收指標組合。|Film application determines the acceptance metrics.
''',['sputter','nistpaper','lamdep','plating'],'a065 a059'.split(),'nist')

add('a061',
['接點與材料|Contacts and materials','成核與填充|Nucleation and fill','平坦化與介面|Planarization and interfaces','電性與可靠度|Electrical quality and reliability'],
['鎢插塞需同時提供低阻連接與相容介面，不只是填滿洞。|Tungsten plugs need low-resistance connections and compatible interfaces, not merely filled holes.','成核延遲與共形生長會影響接縫及空洞。|Nucleation delay and conformal growth affect seams and voids.','阻障、襯層與前清潔會改變接觸電阻與有效導電面積。|Barriers, liners and preclean change contact resistance and conducting area.','總電阻包含體材料、幾何與上下介面。|Total resistance includes bulk material, geometry and both interfaces.'],
['鎢體電阻率即可決定所有接點電阻。|Bulk tungsten resistivity determines every contact resistance.','洞口封閉就能證明內部填滿。|A closed opening proves full internal fill.','襯層越厚一定越低電阻。|A thicker liner necessarily lowers resistance.','單一接點導通即可證明整批可靠。|One conducting contact proves whole-lot reliability.'],
'''
畫出元件到第一層金屬的接點|Draw a contact from device to first metal|垂直接點包含多個材料介面。|A vertical contact includes multiple material interfaces.
比較鎢插塞與銅通孔的角色|Compare tungsten plugs with copper vias|材料選擇受到整合位置與熱史影響。|Material choice depends on integration level and thermal history.
估算孔徑縮小對電阻的影響|Estimate resistance changes as diameter shrinks|導電截面縮小會增加幾何電阻。|A smaller conducting section increases geometric resistance.
分開體電阻與接觸電阻|Separate bulk and interface resistance|介面可在小尺寸下占重要比例。|Interfaces can dominate at small dimensions.
標記前清潔與原生氧化層|Mark preclean and native oxide|殘留氧化層可能增加接觸電阻。|Residual oxide can increase contact resistance.
建立孔底與側壁的材料清單|List materials at the bottom and sidewalls|相容性需涵蓋整個接點堆疊。|Compatibility must cover the full contact stack.
畫出成核層與主體鎢的生長|Draw nucleation and bulk tungsten growth|成核與主體沉積可有不同機制。|Nucleation and bulk growth can have different mechanisms.
比較 ALD 成核與 CVD 主體填充|Compare ALD nucleation with CVD bulk fill|薄層精度與高產率可由不同步驟分工。|Thin-layer precision and productivity can be split across steps.
檢查不同表面的成核延遲|Assess nucleation delay on different surfaces|非均勻起始可造成局部空隙。|Nonuniform initiation can create local gaps.
比較共形生長的中央接縫|Inspect central seams from conformal growth|側壁相向生長可能留下接縫。|Opposing sidewall growth can leave a seam.
追蹤孔口懸垂到封口|Trace entrance overhang into pinch-off|過早封口可能包住空洞。|Early closure can trap voids.
對照截面與沉積厚度的填充狀態|Compare fill state with deposition thickness|外部厚度不能唯一代表孔內填充。|External thickness does not uniquely establish internal fill.
檢查阻障與襯層的連續性|Inspect barrier and liner continuity|局部破口可能造成化學或擴散問題。|Local gaps can cause chemical or diffusion problems.
比較襯層厚度對有效孔徑的影響|Assess liner thickness against effective diameter|襯層占用導電截面。|Liners consume conducting area.
畫出 CMP 移除頂部多餘鎢|Sketch CMP removal of excess top tungsten|平坦化需停止在適當介電層。|Planarization needs an appropriate dielectric stop.
量測凹陷與殘留金屬|Measure recess and residual metal|過度與不足移除造成不同失效。|Over- and under-removal cause different failures.
檢查 CMP 後清潔的顆粒與腐蝕|Inspect post-CMP particles and corrosion|清潔可能改善顆粒也改變表面。|Cleaning can reduce particles while changing surfaces.
比較熱處理前後的界面狀態|Compare interfaces before and after heating|熱史可能改變反應層與應力。|Thermal history can alter reaction layers and stress.
以 Kelvin 結構分離接觸電阻|Separate contact resistance using Kelvin structures|量測設計可減少導線電阻混入。|Measurement design can reduce lead-resistance contamination.
以接點鏈放大稀有開路事件|Use contact chains to reveal rare opens|長鏈增加觀察機會也需對應樣本數。|Long chains increase opportunities and require defined sample counts.
比較電阻尾端與平均值|Compare resistance tails with the mean|少數高阻接點可能主導產品失效。|A few high-resistance contacts can dominate failures.
將空洞位置與電阻異常對應|Relate void locations to resistance anomalies|形貌因果需用同位置證據。|Morphological causality needs co-located evidence.
檢查熱循環後的接點穩定度|Assess contact stability after thermal cycling|初始導通不等於長期穩定。|Initial continuity is not long-term stability.
交付填充、平坦化與接觸電阻審查|Review fill, planarization and contact resistance|插塞驗證需跨越幾何與介面。|Plug validation must cover geometry and interfaces.
''',['lamdep','lamale','interconnect','lamemory'],'a062 a065'.split())

add('a062',
['線孔整合|Line–via integration','蝕刻與襯層|Etch and liners','填銅與平坦化|Copper fill and planarization','RC 與可靠度|RC and reliability'],
['雙鑲嵌先在介電層形成線槽與通孔，再以金屬填入。|Dual damascene forms trenches and vias in dielectric before metal filling.','線槽、通孔、停止層與阻障之間的介面決定可填充性。|Interfaces among trenches, vias, stops and barriers determine fillability.','填滿與平坦化需避免空洞、凹陷及殘留短路。|Fill and planarization must avoid voids, dishing and residual shorts.','互連效能同時受電阻、電容與可靠度限制。|Interconnect performance is constrained by resistance, capacitance and reliability together.'],
['雙鑲嵌就是直接蝕刻厚銅形成所有線孔。|Dual damascene directly etches thick copper into all lines and vias.','阻障層越厚越不需要考慮電阻。|Thicker barriers remove resistance concerns.','表面平坦可排除內部空洞。|A planar surface rules out internal voids.','只有直流電阻決定互連效能。|DC resistance alone determines interconnect performance.'],
'''
畫出兩金屬層之間的通孔與線槽|Draw a via and trench between metal levels|垂直與水平連接具有不同幾何。|Vertical and horizontal connections have different geometry.
比較 via-first 與 trench-first 流程|Compare via-first and trench-first flows|順序改變保護、清潔與對位需求。|Sequence changes protection, cleaning and alignment needs.
標記蝕刻停止層與低介電層|Mark etch-stop and low-k layers|不同介電層具有不同功能。|Different dielectric layers serve different functions.
規畫通孔落在下層線上的裕量|Budget via landing on the lower line|套刻偏差會降低接觸面積或形成短路。|Overlay error can reduce contact area or cause shorts.
比較線寬與線距對 RC 的影響|Compare width and spacing effects on RC|加寬降阻可能增加耦合電容。|Widening can lower resistance while increasing coupling capacitance.
建立跨兩層的連通性圖|Build connectivity across two metal levels|幾何疊合需符合網路意圖。|Geometric overlap must match network intent.
追蹤通孔蝕刻到停止層|Trace via etching to the stop layer|停止層保護下層但也需適時開啟。|A stop protects the lower layer but must later be opened.
檢查線槽深度與通孔肩部|Inspect trench depth and via shoulders|肩部形狀會影響襯層與填充。|Shoulder geometry affects lining and fill.
評估光阻去除對低 k 的損傷|Assess low-k damage during resist removal|去膠可能改變表面組成與介電性。|Stripping can change surface composition and permittivity.
檢查下層銅表面氧化與殘留|Inspect lower-copper oxidation and residue|接點介面污染可能增加通孔電阻。|Interface contamination can increase via resistance.
畫出阻障層與種子層的位置|Draw barrier and seed-layer locations|阻擴散與供電鍍起始是不同功能。|Diffusion blocking and plating initiation are different functions.
比较側壁與孔底覆蓋比例|Compare wall and bottom coverage ratios|最薄位置可能決定失效。|The thinnest region can determine failure.
用截面追蹤自底向上的銅填充|Trace bottom-up copper fill in sections|超共形填充可避免過早封口。|Superconformal fill can avoid premature closure.
辨識接縫、空洞與未連續種子|Distinguish seams, voids and seed discontinuity|相似高阻結果可能有不同起因。|Similar high resistance can have different causes.
比較電鍍厚度與頂部過鍍|Compare plated thickness with overburden|填孔與表面過鍍需共同控制。|Feature fill and overburden need joint control.
畫出 CMP 先去銅再處理阻障|Sketch copper and barrier CMP stages|不同材料移除需避免相對高度失控。|Removing different materials requires height control.
量測線寬相關凹陷與圖形密度侵蝕|Measure width-dependent dishing and density-dependent erosion|局部版圖影響平坦化結果。|Local layout affects planarization.
檢查金屬殘留與後清潔腐蝕|Inspect metal residue and post-clean corrosion|清潔與平坦化共同影響短路與可靠度。|Cleaning and planarization jointly affect shorts and reliability.
以線電阻分離幾何與材料貢獻|Separate geometric and material contributions to line resistance|有效截面包括襯層占用。|Effective cross section accounts for liner occupancy.
以 Kelvin 通孔量測分離接觸損失|Use Kelvin via structures to separate contact loss|四端量測降低引線影響。|Four-terminal measurement reduces lead effects.
以梳狀結構量測線間漏電|Measure interline leakage using comb structures|介電損傷可能在電性上才明顯。|Dielectric damage may become clear only electrically.
評估電遷移的電流密度與溫度|Assess current density and temperature in electromigration|壽命比較需一致應力條件。|Lifetime comparisons need matching stress conditions.
比較銅雙鑲嵌與釕半鑲嵌|Compare copper dual damascene with ruthenium semi-damascene|不同金屬可能搭配不同圖案形成方式。|Different metals can use different patterning schemes.
交付兩層互連的 RC 與失效審查|Deliver a two-level RC and failure review|局部製程合格仍需跨層功能驗證。|Local process acceptance still needs cross-layer functional validation.
''',['copperhistory','plating','semidam','wiring'],'a066 a063'.split())

add('a063',
['尺度與材料|Scaling and materials','整合路線|Integration routes','電阻與介面|Resistance and interfaces','可靠度比較|Reliability comparison'],
['奈米線電阻不能只依塊材電阻率排名，表面散射與有效截面很重要。|Nanoscale line resistance cannot be ranked by bulk resistivity alone; surface scattering and effective area matter.','替代金屬研究需比較沉積、蝕刻、襯層與介電整合。|Alternative-metal research must compare deposition, etch, liners and dielectric integration.','線、通孔與接觸的限制可能不同。|Lines, vias and contacts can have different limitations.','研究測試結構的優勢不代表所有金屬層或所有产品皆適用。|Test-structure benefits do not imply suitability for every level or product.'],
['塊材電阻率最低的金屬永遠最佳。|The lowest bulk-resistivity metal is always best.','更換金屬不需要改任何製程。|Changing metal requires no process changes.','線電阻較低就保證通孔電阻較低。|Lower line resistance guarantees lower via resistance.','一次研究展示即可宣布全面量產替代。|One demonstration proves universal production replacement.'],
'''
比較塊材與奈米線的電阻率概念|Compare bulk and nanoscale-wire resistivity|尺寸效應會改變材料排序。|Size effects can change material rankings.
畫出阻障占比隨線寬縮小的變化|Plot barrier fraction as linewidth shrinks|非導電或高阻襯層會占用截面。|Nonconducting or resistive liners consume cross section.
分開表面散射與晶界散射|Separate surface and grain-boundary scattering|兩者對微結構的依賴不同。|They depend differently on microstructure.
比較 Cu、Co 與 Ru 的整合問題|Compare integration issues for Cu, Co and Ru|材料優勢與可製造性必須共同評估。|Material advantages and manufacturability need joint assessment.
選定線、通孔或接點的研究範圍|Choose a line, via or contact study scope|不同位置不能直接套用同一比較。|Different locations cannot share an unqualified comparison.
建立相同有效截面的公平基準|Build a fair benchmark at matched conducting area|名目線寬相同未必導電面積相同。|Equal nominal width need not mean equal conducting area.
比較鑲嵌填充與減法金屬蝕刻|Compare damascene fill with subtractive metal etch|材料可蝕刻性影響路線選擇。|Metal etchability influences integration choice.
畫出半鑲嵌的通孔與上層線|Draw vias and upper lines in semi-damascene|通孔填充與上層金屬可在相關步驟形成。|Via fill and upper metal can be formed in related steps.
評估自對準通孔的落點保護|Assess landing protection from self-aligned vias|自對準仍有材料選擇性與形貌要求。|Self-alignment still needs material selectivity and profile control.
比較有襯層與無襯層的材料風險|Compare lined and linerless material risks|省去襯層需證明擴散與黏著相容。|Removing liners requires diffusion and adhesion evidence.
檢查金屬成核與連續膜形成|Assess nucleation and continuous-film formation|薄膜早期可能是不連續島狀。|Early films can consist of disconnected islands.
評估直接蝕刻後的側壁殘留|Assess residues after direct metal etching|殘留可改變電性與介電整合。|Residues can affect electrical and dielectric integration.
量測電阻對導電面積的關係|Measure resistance versus conducting area|面積量測誤差會影響材料比較。|Area-measurement errors affect material comparison.
把線長掃描分解成斜率與截距|Use length scaling to separate slope and intercept|截距可包含接觸與引線貢獻。|The intercept can contain contact and lead contributions.
比較不同晶粒結構的電阻|Compare resistance across grain structures|微結構是電阻模型的一部分。|Microstructure is part of the resistance model.
量測通孔分布而非只看平均|Measure via distributions rather than only means|高阻尾端可能決定電路風險。|High-resistance tails can determine circuit risk.
比較高深寬比線對電容的影響|Assess capacitance of tall narrow lines|加高可降阻但可能增加側壁耦合。|Greater height can lower resistance but increase sidewall coupling.
將空氣間隙加入 RC 比較|Include air gaps in RC comparisons|低電容方案也有機械與封口要求。|Low-capacitance schemes also need mechanical and sealing control.
設計線間介電崩潰對照|Design interline dielectric-breakdown comparisons|可靠度取決於金屬與介電介面。|Reliability depends on metal–dielectric interfaces.
比較相同溫度與電流密度下的壽命|Compare lifetime at matched temperature and current density|不同應力條件不能直接排名。|Different stress conditions cannot be ranked directly.
檢查熱處理後的擴散與黏著|Assess diffusion and adhesion after heating|初始電阻低不保證熱穩定。|Low initial resistance does not prove thermal stability.
區分模擬改善與實驗展示|Distinguish simulated gains from demonstrations|不同證據層次支持不同主張。|Different evidence levels support different claims.
比較研究節點名稱與實際測試尺寸|Compare node labels with measured test dimensions|節點名稱不是完整幾何規格。|A node label is not a complete geometry specification.
提交材料、流程、RC 與可靠度取捨|Review material, flow, RC and reliability tradeoffs|替代金屬選擇是整合問題。|Alternative-metal selection is an integration problem.
''',['altmetals','metals2018','semidam','beoltoolbox'],'a062 a064'.split())

add('a064',
['電容與孔隙|Capacitance and porosity','成膜與固化|Growth and curing','圖案化損傷|Patterning damage','機械與可靠度|Mechanics and reliability'],
['降低介電常數可減少耦合電容，但孔隙可能降低機械與化學耐受性。|Lower permittivity reduces coupling but porosity can weaken mechanical and chemical resistance.','材料名目 k 值與整合後有效 k 值不同。|Nominal material k differs from integrated effective k.','蝕刻、去膠、清潔與吸水會改變低 k 表面與孔隙。|Etch, strip, clean and moisture can change low-k surfaces and pores.','低 k 成功需同時滿足 RC、漏電、附著與封裝機械要求。|Successful low-k integration needs RC, leakage, adhesion and packaging mechanics together.'],
['只要孔隙越多就一定更適合整合。|More porosity always improves integration.','材料標稱 k 值就等於整個互連有效 k。|Nominal k equals the effective k of the entire interconnect.','去膠只影響光阻，不影響低 k。|Stripping affects resist but never low-k.','電容下降即可忽略機械裂紋。|Lower capacitance makes mechanical cracks irrelevant.'],
'''
用平行板模型分開 k、面積與厚度|Separate k, area and thickness in a plate model|電容改變不一定來自材料 k 改變。|A capacitance change need not originate from k.
畫出線間與上下層耦合電容|Draw lateral and vertical coupling capacitances|實際互連有多種電場路徑。|Real interconnects have multiple field paths.
比較緻密低 k 與多孔低 k|Compare dense and porous low-k|孔隙降低平均極化也改變強度。|Porosity reduces average polarization and alters strength.
建立 RC 延遲的簡化比較|Build a simplified RC-delay comparison|低 k 的收益需與導線電阻共同評估。|Low-k benefits need evaluation with line resistance.
分開材料 k 與有效堆疊 k|Separate material k from effective-stack k|襯層與停止層也貢獻電容。|Liners and stops also contribute capacitance.
列出封裝載荷與附著需求|List packaging loads and adhesion needs|晶片後段機械負載會傳入低 k。|Back-end mechanical loads reach low-k layers.
比較沉積前驅物與造孔概念|Compare film-precursor and porogen concepts|造孔需要控制孔隙形成與移除。|Porosity generation needs controlled formation and removal.
畫出固化前後的網路結構|Sketch network structure before and after curing|固化可改變鍵結、應力與孔隙。|Curing can alter bonding, stress and porosity.
用光譜追蹤碳相關鍵結|Track carbon-related bonds spectroscopically|鍵結變化可提示材料損傷。|Bond changes can indicate material damage.
比較孔徑分布與總孔隙率|Compare pore-size distribution with total porosity|相同孔隙率可能有不同連通性。|Equal porosity can have different connectivity.
量測膜厚與應力的固化變化|Measure thickness and stress changes during curing|收縮會改變幾何及機械狀態。|Shrinkage changes geometry and mechanics.
建立吸濕前後的電容對照|Compare capacitance before and after moisture exposure|水分可提高有效介電反應。|Moisture can increase effective dielectric response.
檢查蝕刻後側壁的化學改變|Inspect sidewall chemistry after etching|損傷層可能比本體有更高 k。|A damaged layer can have higher k than the bulk.
比較不同去膠路線的材料保留|Compare material preservation in stripping routes|去除效率與低 k 保護需兼顧。|Removal efficiency and low-k preservation need balancing.
評估濕清潔液進入開放孔隙|Assess cleaning-liquid entry into open pores|開放孔隙會改變污染與乾燥歷程。|Open pores change contamination and drying history.
畫出側壁封孔對有效尺寸的影響|Sketch pore-sealing effects on effective dimensions|封孔可能改善保護但占用空間。|Pore sealing can protect surfaces while consuming space.
比較圖形化前後的有效 k|Compare effective k before and after patterning|整合過程可能抵銷材料原始優勢。|Integration can offset the material's original benefit.
檢查銅阻障在多孔側壁的連續性|Inspect barrier continuity on porous sidewalls|表面孔隙可能妨礙完整覆蓋。|Surface pores can obstruct continuous coverage.
以梳狀結構評估漏電與崩潰|Assess leakage and breakdown with comb structures|低電容不保證高介電可靠度。|Low capacitance does not guarantee dielectric reliability.
比較不同應力下的裂紋路徑|Compare crack paths under different stresses|最弱介面可能決定整體機械失效。|The weakest interface can control mechanical failure.
檢查 CMP 與接合載荷的後果|Assess consequences of CMP and bonding loads|加工載荷需納入低 k 整合。|Processing loads belong in low-k integration analysis.
比較空氣間隙與多孔介電層|Compare air gaps with porous dielectrics|兩種低電容策略有不同支撐需求。|The two low-capacitance strategies need different support.
將電容、漏電與機械強度放入取捨表|Tabulate capacitance, leakage and strength tradeoffs|单一 k 數字不足以決定材料選擇。|One k value is insufficient for material selection.
交付整合後低 k 的性能證據|Deliver evidence for integrated low-k performance|材料驗收需跨越成膜與後續圖案化。|Acceptance must span growth and subsequent patterning.
''',['beoltoolbox','wiring','semidam','lowkbarrier'],'a057 a063'.split())

add('a065',
['功能與截面|Functions and sections','沉積與連續性|Deposition and continuity','介面與填充|Interfaces and filling','擴散與可靠度|Diffusion and reliability'],
['阻障層阻擋擴散，種子層提供電鍍起始與導電路徑，功能不可混同。|Barriers block diffusion; seeds enable plating and electrical continuity; the roles differ.','最薄側壁或孔底可能決定整體阻障完整性。|The thinnest wall or bottom region can determine barrier integrity.','種子連續性、氧化與潤濕會影響後續銅成核。|Seed continuity, oxidation and wetting affect subsequent copper nucleation.','減薄襯層增加導電面積，但需保持擴散與附著可靠度。|Thinner liners increase conducting area but must retain diffusion and adhesion reliability.'],
['有種子層就不需要任何擴散阻障。|A seed layer eliminates all need for a diffusion barrier.','平均厚度合格就能保證沒有針孔。|Acceptable average thickness proves no pinholes.','種子表面氧化不會影響電鍍。|Seed oxidation cannot affect plating.','襯層無限薄一定最佳。|An arbitrarily thin liner is always best.'],
'''
畫出介電層、阻障、種子與銅主體|Draw dielectric, barrier, seed and bulk copper|不同層負責不同物理功能。|Different layers serve different physical functions.
比較擴散阻擋與電性導通需求|Compare diffusion blocking with electrical continuity|良好阻擴散不一定是良好電鍍表面。|A good diffusion barrier need not be a good plating surface.
估算襯層占用的導電截面|Estimate conducting area consumed by liners|尺度縮小時占比會提高。|The fractional occupancy grows as dimensions shrink.
標記側壁、孔底與轉角的要求|Mark wall, bottom and corner requirements|各位置的覆蓋難度不同。|Coverage difficulty differs by location.
建立基板表面污染的影響鏈|Trace effects of surface contamination|污染可破壞成核與附著。|Contamination can disrupt nucleation and adhesion.
比較多層阻障與整合襯層概念|Compare multilayer barriers with integrated liners|新材料需重新驗證每項功能。|New materials require revalidation of every function.
比較 PVD、CVD 與 ALD 覆蓋機制|Compare PVD, CVD and ALD coverage|不同沉積機制有不同深部可達性。|Deposition mechanisms differ in deep-feature access.
量測頂部與側壁厚度比|Measure top-to-sidewall thickness ratios|平面厚度不能替代共形性。|Planar thickness does not substitute for conformality.
檢查孔底最薄點的連續性|Inspect continuity at the thinnest bottom region|局部破口可能支配擴散失效。|Local gaps can dominate diffusion failure.
比較成核島連結成膜的階段|Compare nucleation islands merging into a film|名目沉積量不一定代表連續薄膜。|Nominal deposited amount need not imply a continuous film.
評估 PVD 孔口懸垂與遮蔽|Assess PVD entrance overhang and shadowing|入口沉積可阻擋深部通量。|Entrance deposition can block deep flux.
追蹤層間曝氣造成的表面氧化|Track oxidation caused by interlayer air breaks|曝氣歷程會改變接觸與潤濕。|Air-break history changes contact and wetting.
以片電阻地圖檢查種子連續性|Map sheet resistance to assess seed continuity|低平均電阻仍可能伴隨局部斷點。|Low mean resistance can coexist with local discontinuities.
比較氧化前後的電鍍起始|Compare plating initiation before and after oxidation|表面化學影響成核過電位。|Surface chemistry affects nucleation overpotential.
畫出邊緣接點到孔底的供電路徑|Trace current from edge contacts to feature bottoms|種子層提供電流分布的路徑。|The seed provides current-distribution paths.
檢查浸潤不足與孔底氣泡|Inspect poor wetting and trapped bottom bubbles|未潤濕區域可能無法正常電鍍。|Unwetted regions may not plate normally.
比較前清潔強度與種子損失|Compare preclean intensity with seed loss|清潔過程可能同時消耗薄種子。|Cleaning can also consume a thin seed.
把填孔空洞回溯至覆蓋缺陷|Trace fill voids back to coverage defects|電鍍失敗可能源自更早沉積。|Plating failures can originate in earlier deposition.
以熱處理後元素剖面檢查擴散|Check diffusion using post-anneal elemental profiles|阻障驗證需要時間與溫度條件。|Barrier validation needs stated time and temperature.
以漏電結構檢查銅污染影響|Assess copper-contamination effects using leakage structures|微量擴散可能先表現在電性。|Small diffusion can first appear electrically.
比較附著與熱循環的介面耐受|Compare adhesion and thermal-cycle interface resistance|阻擴散合格不代表附著合格。|Passing diffusion control does not prove adequate adhesion.
評估薄襯層的電阻收益與風險|Evaluate resistance benefit and risk of thin liners|面積收益需與最薄點可靠度相衡。|Area gains must be balanced against weakest-point reliability.
比較單一截面與統計取樣結論|Compare one cross section with statistical sampling|局部影像不能代表全片缺陷率。|A local image cannot establish wafer defect rate.
交付覆蓋、導通、擴散與附著評審|Review coverage, continuity, diffusion and adhesion|阻障種子整合需要四類證據。|Barrier–seed integration needs four classes of evidence.
''',['plating','sputter','wiring','copperhistory'],'a060 a066'.split())

add('a066',
['電化學與供電|Electrochemistry and current','傳質與添加劑|Transport and additives','超共形填充|Superconformal filling','缺陷與後段|Defects and downstream processing'],
['電鍍總電荷與沉積量相關，但需考慮電流效率與實際有效面積。|Plating charge relates to deposited mass but requires current efficiency and effective area.','添加劑、流場與電位共同影響不同位置的沉積速率。|Additives, flow and potential jointly affect local deposition rates.','自底向上填充需要抑制過早封口，不能只提高整體沉積速度。|Bottom-up fill requires avoiding early closure, not merely increasing overall deposition rate.','填銅驗收需連結空洞、應力、晶粒、平坦化與電性。|Copper-fill acceptance links voids, stress, grains, planarization and electrical behavior.'],
['通過多少電荷就保證全部都變成銅。|All passed charge is guaranteed to become copper.','添加劑越多一定填孔越好。|More additive always improves fill.','孔口沉積最快就是最佳填孔。|Fastest opening deposition is the best fill.','表面光亮就證明孔內沒有空洞。|A shiny surface proves void-free features.'],
'''
畫出陽極、陰極與電解液的電流路徑|Draw anode, cathode and electrolyte current paths|電子與離子在不同路徑傳輸。|Electrons and ions travel through different paths.
用法拉第定律估算理想沉積質量|Estimate ideal deposited mass with Faraday's law|實際質量還依賴電流效率。|Actual mass also depends on current efficiency.
分開總電流與局部電流密度|Separate total current from local current density|局部沉積速率由局部條件決定。|Local conditions determine local deposition rate.
檢查種子層的供電連續性|Check seed-layer electrical continuity|電化學填充需要可到達的導電表面。|Electrochemical fill needs accessible conducting surfaces.
標記阻障與介電層不應鍍銅的區域|Mark regions that should not plate copper|材料選擇與遮蔽影響沉積位置。|Material choice and masking affect deposition location.
建立假設鍍液與量測資料的邊界|Define the scope of hypothetical electrolyte data|教學電化學模型不是商用鍍液配方。|Educational electrochemical models are not commercial bath recipes.
畫出孔口到孔底的濃度梯度|Sketch concentration gradients into a feature|深部供應可能受傳質限制。|Deep supply can be mass-transfer-limited.
比較擴散、對流與電遷移|Compare diffusion, convection and migration|三種輸運機制依條件有不同權重。|The three mechanisms have condition-dependent importance.
區分抑制劑、促進劑與整平劑功能|Distinguish suppressor, accelerator and leveler roles|添加劑會改變表面反應而非只改導電率。|Additives change surface reactions, not merely conductivity.
比較旋轉或流動對邊界層的影響|Compare flow effects on boundary layers|外部流動改善不一定完全解除孔內限制。|External flow improvements need not remove internal transport limits.
檢查添加劑消耗與鍍液歷程|Assess additive depletion and bath history|鍍液狀態會隨使用時間改變。|Bath condition changes with use history.
比較定電流與定電位的觀測量|Compare observables under current and potential control|控制一個量時另一個量提供狀態資訊。|When one is controlled, the other provides state information.
繪製共形填充與自底向上填充|Sketch conformal and bottom-up filling|底部較快成長可減少封口空洞。|Faster bottom growth can reduce pinch-off voids.
追蹤填充前緣與孔口剩餘空間|Track fill fronts and remaining opening|孔口必須保持足夠傳輸通道。|The opening must retain sufficient transport access.
比較窄孔與寬槽的填充演化|Compare filling of narrow vias and wide trenches|不同幾何需要不同局部速率分布。|Different geometries require different local rate distributions.
檢查底部氣泡與未潤濕區|Inspect bottom bubbles and unwetted regions|氣泡可隔斷電解液與表面。|Bubbles can isolate the surface from electrolyte.
將種子斷裂與接縫空洞分開|Separate seed discontinuity from seam voids|相似空洞可能有不同上游來源。|Similar voids can have different upstream origins.
比較過鍍厚度與填孔完成度|Compare overburden thickness with fill completeness|大量過鍍不能補救所有內部空洞。|Heavy overplating cannot repair every internal void.
估算電荷與截面體積是否一致|Check consistency between charge and filled volume|不一致可能來自效率或面積估算錯誤。|Disagreement can reflect efficiency or area-estimation errors.
檢查沉積後應力與晶粒演化|Assess post-deposition stress and grain evolution|銅組織可能隨時間或熱處理改變。|Copper microstructure can evolve with time or heating.
比較 CMP 前後的缺陷可見度|Compare defect visibility before and after CMP|平坦化可能暴露原先埋藏空洞。|Planarization can expose previously buried voids.
以通孔鏈量測高阻與開路|Measure high resistance and opens using via chains|電性量測可放大稀有填充失敗。|Electrical measurements can reveal rare fill failures.
建立鍍液監控與缺陷趨勢對照|Relate bath monitoring to defect trends|相關趨勢需對照材料與設備變動。|Correlations need controls for material and equipment changes.
交付電荷、截面與電性一致性報告|Deliver charge, cross-section and electrical consistency|填孔成功需要多種相互支持的證據。|Successful fill needs mutually supporting evidence types.
''',['plating','lamdep','copperhistory','interconnect'],'a062 a065'.split())

# Primary sources were checked through public search/open on 2026-10-14 (Taipei).
# Links are references, not redistribution licenses for their illustrations.
S={}
def src(key,zh,en,publisher,url,scope,scopeEn):
 S[key]=dict(id='v8b-'+key,title=zh,titleEn=en,publisher=publisher,url=url,scope=scope,scopeEn=scopeEn,accessedAt='2026-10-14')
src('mor','金屬氧化物光阻後曝光處理研究','Metal-oxide resist post-exposure processing research','imec','https://www.imec-int.com/en/press/imec-unlocks-lever-euv-dose-reduction-oxygen-injection-during-metal-oxide-resist-post','公開 MOR 研究案例；不外推為所有材料通用配方。','A public MOR study, not a universal material recipe.')
src('pattern','圖案化挑戰與創新','Challenges and innovations in patterning','imec','https://www.imec-int.com/en/articles/challenges-and-innovations-patterning','光罩、光阻、隨機缺陷與圖案轉移的整合挑戰。','Integration challenges in masks, resists, stochastic defects and pattern transfer.')
src('stochastic','EUV 單次曝光與隨機缺陷整合','Pushing single-exposure EUV patterning limits','imec','https://www.imec-int.com/en/press/imec-pushes-single-exposure-patterning-capability-033na-euvl-its-extreme-limits','光學、電子束與電性缺陷證據的比較。','Comparison of optical, electron-beam and electrical defect evidence.')
src('euvyield','High-NA 單次圖案化金屬線的電性良率','Electrical yield of High-NA single-patterned metal lines','imec','https://www.imec-int.com/en/press/imec-demonstrates-electrical-yield-20nm-pitch-metal-lines-obtained-high-na-euv-single','特定測試結構的線條、斷線、橋接及電性驗證。','Lines, breaks, bridges and electrical validation in specific test structures.')
src('jeol','電子束微影系統的定位與吞吐量','Development of the JBX-8100FS electron-beam lithography system','JEOL','https://www.jeol.com/solutions/applications/details/1698.php','束流、載台、拼接、套刻與寫入時間的公開技術說明。','Public explanation of beam, stage, stitching, overlay and write time.')
src('maskmetro','光罩定位與量測','Photomask metrology solutions','ZEISS','https://www.zeiss.com/semiconductor-manufacturing-technology/products/photomask-solutions/mask-metrology.html','光罩定位、平整度及光罩到晶圓的量測關係。','Mask placement, flatness and mask-to-wafer metrology relationships.')
src('maskrepair','光罩局部添加與移除修補','Mask repair solutions','ZEISS','https://www.zeiss.com/semiconductor-manufacturing-technology/products/photomask-solutions/mask-repair.html','電子束誘發局部加工與缺陷修補的功能。','Functions of electron-beam-induced local processing and defect repair.')
src('maskqual','光罩空中像與可印性驗證','Mask qualification solutions','ZEISS','https://www.zeiss.com/semiconductor-manufacturing-technology/products/photomask-solutions/mask-qualification.html','DUV 與 EUV 光罩成像及可印性驗證。','Imaging and printability qualification for DUV and EUV masks.')
src('psm','相位移光罩原理與類型','Photomask types and phase-shift masks','Tekscend Photomask','https://www.photomask.com/product/photomask/','製造者說明交替與衰減相位移光罩；原文日文。','Manufacturer explanation of alternating and attenuated phase-shift masks; Japanese original.')
src('psmibm','193 nm 相位移吸收層研究','Molybdenum-silicide phase-shifting absorber study','IBM Research','https://research.ibm.com/publications/evaluation-of-molybdenum-silicide-for-use-as-a-193-nm-phase-shifting-absorber-in-photomask-manufacturing','原研究摘要：吸收層材料與相位移光罩的評估。','Original research abstract on absorber materials and phase-shift mask evaluation.')
src('comp','計算微影','Computational lithography','ASML','https://www.asml.com/en/products/computational-lithography','成像預測、修正與製程控制的角色；非軟體原始碼。','Roles of image prediction, correction and process control; not software source code.')
src('duv','DUV 與浸潤式微影系統','DUV and immersion lithography systems','ASML','https://www.asml.com/en/products/duv-lithography-systems','浸潤、焦點、套刻與跨工具匹配的系統功能。','System roles of immersion, focus, overlay and cross-tool matching.')
src('lenses','微影透鏡與反射鏡','Lenses and mirrors in lithography','ASML','https://www.asml.com/en/technology/lithography-principles/lenses-and-mirrors','DUV 透鏡、浸潤介質與 EUV 反射光學的區別。','Distinction between DUV lenses, immersion media and EUV reflective optics.')
src('euv','EUV 微影系統','EUV lithography systems','ASML','https://www.asml.com/en/products/euv-lithography-systems','EUV 系統公開功能與整合概覽。','Public EUV system functions and integration overview.')
src('multipattern','N5 等效金屬層的混合圖案化','Patterning solutions for N5-equivalent metal layers','imec','https://www.imec-int.com/en/articles/imec-presents-patterning-solutions-for-n5-equivalent-metal-layers','多重圖案化、阻擋與 EUV 整合的研究案例。','Research examples combining multipatterning, blocks and EUV.')
src('saqp','SAQP 與 EUV 阻擋圖案化','SAQP with EUV block patterning','imec','https://www.imec-int.com/en/imec-magazine/imec-magazine-march-2017/first-euv-lithography-high-volume-manufacturing-solution-for-n5-beol','2017 年 SAQP 與 EUV 的整合案例；不是所有節點的固定流程。','A 2017 SAQP/EUV integration example, not a fixed flow for every node.')
src('dsa','由下而上的輔助圖案化','Building patterns from the bottom','imec','https://www.imec-int.com/en/articles/building-patterns-from-the-bottom-a-complementary-approach-to-lithography','導向自組裝與選擇性沉積作為微影補充。','Directed self-assembly and selective deposition as complements to lithography.')
src('dsahigh','高χ區塊共聚物圖案化研究','High-chi directed self-assembly patterning study','imec','https://staging.imec-int.com/en/press/imec-demonstrates-18nm-pitch-linespace-patterning-high-chi-directed-self-assembly-process','特定高χ材料的線空間展示；不代表所有版圖可直接自組裝。','A line-space demonstration for a specific high-chi material, not arbitrary-layout assembly.')
src('sis','序列浸潤強化 EUV 圖案','Sequential infiltration synthesis for EUV patterns','imec','https://www.imec-int.com/en/articles/sequential-infiltration-synthesis-sis-significantly-improves-euv-patterning','聚合物圖案無機浸潤強化與轉移。','Inorganic infiltration strengthening and transfer of polymer patterns.')
src('nil','奈米壓印微影原理','Nanoimprint lithography','Canon','https://global.canon/en/technology/canon-tech/tech/nil/','模板、樹脂分布、對位、脫模與顆粒控制；不引用供應商效能比較為通用事實。','Templates, resin distribution, alignment, release and particles; vendor comparisons are not universalized.')
src('metrology','晶圓量測與缺陷檢查','Wafer metrology and inspection systems','ASML','https://www.asml.com/en/products/metrology-and-inspection-systems','套刻、線寬與缺陷的互補量測角色。','Complementary roles of overlay, dimensional and defect metrology.')
src('rie','反應式離子蝕刻','Reactive ion etching','Oxford Instruments','https://plasma.oxinst.com/technologies/rie','RIE 功能、材料與圖形範圍；不是操作配方。','RIE functions, materials and pattern scope; not an operating recipe.')
src('lametch','半導體導體與介電層蝕刻','Conductor and dielectric etching','Lam Research','https://www.lamresearch.com/products/our-processes/etch/','導體、介電層及原子層蝕刻的整合概念。','Integration concepts for conductor, dielectric and atomic-layer etch.')
src('endpoint','光學發射與反射端點偵測','Optical emission and reflection endpoint detection','Oxford Instruments','https://plasma.oxinst.com/service-support/upgrades/endpoint-detectors','OES 與干涉端點的訊號、用途及開口面積限制。','Signals, uses and open-area limitations of OES and interference endpoints.')
src('endpointblog','何時停止蝕刻：端點方法','Automatic endpoint detection','Oxford Instruments','https://plasma.oxinst.com/media-centre/blog/automatic-endpoint-detection','2020 年原廠技術解說：物種發光與界面判讀。','A 2020 manufacturer technical explanation of species emission and interfaces.')
src('ale','原子層蝕刻與深度量測','Atomic-layer etching and depth monitoring','Oxford Instruments','https://plasma.oxinst.com/technologies/atomic-layer-etching','循環蝕刻及深度控制的公開設備功能。','Public equipment functions for cyclic etch and depth control.')
src('atomic','原子尺度處理','Atomic-scale processing','Oxford Instruments','https://plasma.oxinst.com/technologies/atomic-scale-processing','循環處理、低損傷與表面品質的設計目標。','Design goals for cyclic processing, low damage and surface quality.')
src('lamale','導體與介電層 ALE 發展','Atomic-layer etch for conductors and dielectrics','Lam Research','https://newsroom.lamresearch.com/New-Atomic-Layer-Etching-Capability-Enables-Continued-Device-Scaling?blog=true','循環沉積與移除的 ALE 公開概念。','Public ALE concepts of cyclic deposition and removal.')
src('drie','Bosch 與低溫深矽蝕刻','Bosch and cryogenic deep silicon etching','Oxford Instruments','https://plasma.oxinst.com/products/dsie/','深矽蝕刻的两類技術、鈍化與 MEMS 用途。','Two deep-silicon technologies, passivation and MEMS uses.')
src('caltechdrie','深矽蝕刻的研究設施說明','DRIE: Bosch and cryogenic ICP-RIE for silicon','Caltech KNI','https://lab.kni.caltech.edu/DRIE%3A_Bosch_%26_Cryo_ICP-RIE_for_Silicon','研究設施的技術範圍；不複製機台設定。','Research-facility technical scope; equipment settings are not reproduced.')
src('lamemory','先進記憶體的蝕刻與沉積','Advanced-memory etch and deposition solutions','Lam Research','https://www.lamresearch.com/products/our-solutions/advanced-memory-solutions/','高深寬比結構、介電沉積及鎢金屬化的整合。','Integration of high-aspect-ratio structures, dielectric deposition and tungsten metallization.')
src('selective','選擇性材料移除','Selective material removal','Applied Materials','https://www.appliedmaterials.com/il/en/semiconductor/products/shape/selective-etch.html','共同設計材料與化學以保留周邊結構。','Co-design of materials and chemistry to preserve surrounding structures.')
src('shape','導體與選擇性蝕刻原理','Conductor and selective-etch concepts','Applied Materials','https://www.appliedmaterials.com/us/en/semiconductor/products/shape.html','方向性、自由基選擇性與三維結構成形。','Directionality, radical selectivity and three-dimensional shaping.')
src('backside','背面供電中的薄化與 SiGe 停止層','Backside power: thinning and SiGe stop layers','imec','https://www.imec-int.com/en/articles/how-power-chips-backside','以公開流程說明 SiGe 停止層用途；不複製配方數值。','A public flow illustrating SiGe stop-layer use; recipe values are not reproduced.')
src('lamdep','化學與電化學沉積','Chemical and electrochemical deposition','Lam Research','https://www.lamresearch.com/products/our-processes/deposition/','PECVD、CVD、ALD 與電鍍的功能分工。','Functional roles of PECVD, CVD, ALD and electroplating.')
src('oxpecvd','MEMS 與封裝中的電漿製程','Plasma processes for MEMS, NEMS and packaging','Oxford Instruments','https://plasma.oxinst.com/assets/uploads/documents/3182_PT_Process_News_Mar2015_Low_res_Spreads.pdf','低溫 PECVD 與其他電漿成膜及蝕刻的公開比較。','Public comparisons of low-temperature PECVD and other plasma growth and etch methods.')
src('lpcvd','低壓化學氣相沉積爐','Low-pressure chemical-vapor deposition furnaces','University of Utah Nanofab','https://www.nanofab.utah.edu/wiki/ctr-lpcvd-furnaces/','低壓高溫表面反應與研究設備用途。','Low-pressure high-temperature surface reactions and research-tool uses.')
src('nistpoly','LPCVD 非晶與多晶矽設備','LPCVD amorphous and polycrystalline silicon','NIST','https://www.nist.gov/laboratories/tools-instruments/nanofab-tool-sandvik-lpcvd-amorphous-and-polycrystalline-silicon','非晶與多晶矽沉積用途。','Amorphous and polycrystalline silicon deposition uses.')
src('nistnitride','LPCVD 氮化矽設備','LPCVD silicon nitride','NIST','https://www.nist.gov/laboratories/tools-instruments/nanofab-tool-sandvik-lpcvd-silicon-nitride','化學計量與低應力氮化矽的區別。','Distinction between stoichiometric and low-stress silicon nitride.')
src('nistlto','LPCVD 低溫氧化層設備','LPCVD low-temperature oxide','NIST','https://www.nist.gov/laboratories/tools-instruments/nanofab-tool-sandvik-lpcvd-lto','研究設施的氧化層沉積範圍。','Oxide-deposition scope in a research facility.')
src('mocvd','MOCVD 基礎說明','How MOCVD works','AIXTRON','https://www.aixtron.com/innovation/technologien/pdfs/How_MOCVD_works.pdf','金屬有機化學氣相沉積原理與薄膜用途。','MOCVD principles and thin-film applications.')
src('planetary','MOCVD 行星式反應器原理','Planetary reactor principle','AIXTRON','https://www.aixtron.com/en/innovation/technologies/planetary-principle','行星式基板運動與氣體輸送概念。','Planetary substrate motion and gas-delivery concepts.')
src('showerhead','MOCVD 近距離淋浴式原理','Close-coupled showerhead principle','AIXTRON','https://www.aixtron.com/en/innovation/technologies/showerhead-principle','淋浴式氣體分布與成膜面積控制。','Showerhead gas distribution and coating-area control.')
src('aixhistory','AIXTRON 歷史','AIXTRON history','AIXTRON','https://www.aixtron.com/en/company/about-aixtron/history','1983 成立、1985 MOCVD 系統及後續反應器發展。','1983 founding, 1985 MOCVD system and later reactor development.')
src('sputter','離子束與偏壓靶濺鍍','Ion-beam and biased-target sputter deposition','NIST','https://www.nist.gov/laboratories/tools-instruments/nanofab-tool-4wave-ibdbtd-cluster-sputter-deposition-system','薄膜能量、密度與介面控制的設備功能。','Equipment functions for film energy, density and interface control.')
src('nistpaper','共用奈米製程設施的原始研究','So, You Want to Have a Nanofab?','NIST researchers / PMC','https://pmc.ncbi.nlm.nih.gov/articles/PMC9017145/','原始設施研究的製程、量測與材料管理經驗。','Original facility study on processing, metrology and material management.')
src('nisttools','NIST NanoFab 設備總覽','NIST NanoFab equipment','NIST','https://www.nist.gov/cnst/equipment','微影、沉積、蝕刻與量測設備的互補關係。','Complementary lithography, deposition, etch and metrology tools.')
src('interconnect','互連製程整合','Interconnect process integration','Lam Research','https://www.lamresearch.com/products/our-solutions/interconnect-solutions/','鎢、銅、介電層與互連製程功能。','Tungsten, copper, dielectric and interconnect process functions.')
src('copperhistory','銅互連革命的技術回顧','Celebrating the copper revolution','Lam Research','https://newsroom.lamresearch.com/Celebrating-the-Copper-Revolutions-20th-Anniversary','阻障、電鍍與 CMP 的共同整合；歷史案例不等於當前節點配方。','Joint integration of barriers, plating and CMP; historical cases are not current-node recipes.')
src('plating','電鍍的基本要素','Tech Brief: Elements of Electroplating','Lam Research','https://newsroom.lamresearch.com/Tech-Brief-Elements-of-Electroplating','阻障、種子與銅電鍍的功能及填充要求。','Functions and fill requirements of barriers, seeds and copper plating.')
src('semidam','半鑲嵌與自對準通孔研究','Semi-damascene and fully self-aligned vias','imec','https://www.imec-int.com/en/articles/imec-demonstrates-semi-damascene-interconnects-fully-self-aligned-vias-18nm-metal-pitch','Ru 減法圖案化與通孔整合的研究展示。','A research demonstration of subtractive Ru patterning and via integration.')
src('wiring','銅與低 k 互連創新','Copper wiring and low-k integration innovations','Applied Materials','https://investor.appliedmaterials.com/news-releases/news-release-details/applied-materials-unveils-chip-wiring-innovations-more-energy','導線、阻障與低 k 的整合挑戰；廠商量化主張不做普遍化。','Wire, barrier and low-k integration challenges; vendor quantitative claims are not generalized.')
src('altmetals','先進互連的替代金屬研究','Alternative metals for advanced interconnects','imec','https://www.imec-int.com/en/press/imec-presents-alternative-metals-advanced-interconnect-and-contact-schemes-path-2nm','Ru、半鑲嵌與空氣間隙的公開研究。','Public research on Ru, semi-damascene and air gaps.')
src('metals2018','Ru 互連延伸研究','Ruthenium interconnect-scaling study','imec','https://www.imec-int.com/en/articles/imec-reports-breakthrough-in-extending-interconnects-beyond-the-3nm-technology-node','奈米互連替代材料的研究主張與適用範圍。','Research claims and scope for alternative nanoscale interconnect materials.')
src('beoltoolbox','BEOL 製程與材料工具箱','Scaling the BEOL: processes, boosters and conductors','imec','https://www.imec-int.com/en/imec-magazine/imec-magazine-september-2019/scaling-the-beol-a-toolbox-filled-with-new-processes-boosters-and-conductors','尺寸效應、替代導體與低電容介電方案。','Size effects, alternative conductors and low-capacitance dielectrics.')
src('lowkbarrier','銅晶片低 k 阻障的歷史案例','Historical low-k barrier integration for copper chips','Applied Materials','https://ir.appliedmaterials.com/news-releases/news-release-details/applied-materials-launches-revolutionary-low-k-barrier-film/','歷史材料整合案例；不把歷史效能數字當成通用材料規格。','Historical material-integration example; historical performance is not a universal specification.')
src('imecplace','imec 魯汶總部與地圖','imec Leuven headquarters and map','imec','https://www.imec-int.com/en/connect-with-us/imec-belgium','1984 年沿革、訪客地址與官方地圖代表點。','1984 history, visitor address and official-map reference point.')
src('nisthistory','CNST 成立與奈米量測任務','CNST establishment and nanometrology mission','NIST','https://www.nist.gov/publications/nist-center-nanoscale-science-and-technology-supporting-us-innovation-nanotechnology','原始文章指出 CNST 於 2007 年 5 月成立。','The original article states CNST was established in May 2007.')
src('nistreopen','NIST NanoFab 重新開放','NIST NanoFab reopens to research users','NIST','https://www.nist.gov/news-events/news/2023/04/nists-nanofab-reopens-its-doors-universities-industry-and-research','2023 年設施重新開放與量測、製程功能。','2023 facility reopening and fabrication/metrology functions.')
src('nistplace','NIST Gaithersburg 交通與地址','Getting to NIST Gaithersburg','NIST','https://www.nist.gov/about-nist/visit/getting-nist-gaithersburg','100 Bureau Drive 園區地址；地圖並非實驗室入口。','100 Bureau Drive campus address; map is not a laboratory entrance.')
src('asmlhistory','ASML 微影發展歷史','ASML lithography history','ASML','https://www.asml.com/en/company/about-asml/history','1984 年成立及 2003 年首台浸潤式系統。','1984 founding and first immersion machine in 2003.')
src('aixplace','AIXTRON 總部交通圖','AIXTRON headquarters directions','AIXTRON','https://www.aixtron.com/Wegbeschreibungen/Wegbeschreibung-AIX-Herzogenrath_E_FINAL.pdf','官方總部地址 Dornkaulstraße 2。','Official headquarters address at Dornkaulstraße 2.')
src('aixmap','AIXTRON 建築輪廓座標','AIXTRON building-outline coordinates','OpenStreetMap contributors','https://api.openstreetmap.org/api/0.6/way/192119752/full','建物頂點平均代表點；非入口、實驗室或精確重心，ODbL 地圖資料。','Mean building-vertex reference point; not an entrance, lab or exact centroid; ODbL map data.')
REL={}
def rel(cid,target,t,te,d,de):REL[(cid,target)]=(t,te,d,de)
rel('a034','a033','兩種光阻都把吸收能量轉成顯影選擇性。','Both resists convert absorbed energy into development selectivity.','金屬氧化物與化學放大型光阻的材料、反應與污染管理不同。','Metal-oxide and chemically amplified resists differ in materials, reactions and contamination management.')
rel('a034','a050','材料選擇必須用斷線、橋接與缺孔統計檢驗。','Material choices need break, bridge and missing-hole statistics.','材料研究改變化學；缺陷分析需要獨立取樣與信賴區間。','Material research changes chemistry; defect analysis needs independent sampling and confidence intervals.')
rel('a035','a036','寫入與修補都需要精確電子束定位。','Writing and repair both require precise electron-beam positioning.','写入建立全片圖形；修補處理局部缺陷並重新驗證可印性。','Writing creates a full pattern; repair addresses local defects and rechecks printability.')
rel('a035','a047','束流、散射、拼接與資料分割可共同學習。','Beam control, scattering, stitching and data fracturing transfer between the topics.','光罩製作需考慮投影縮小與重複使用；直寫直接作用於基板。','Mask fabrication includes projection reduction and reuse; direct writing acts on the substrate.')
rel('a036','a035','光罩定位地圖可回饋缺陷修補座標。','Mask-placement maps can inform repair coordinates.','全片寫入誤差與局部修補誤差需分開追蹤。','Full-mask writing errors and local repair errors need separate tracking.')
rel('a036','a037','幾何與光學相位都會影響可印性。','Geometry and optical phase both affect printability.','相位移光罩的修補不能只恢復外觀尺寸。','Repairing a phase-shift mask cannot rely only on restoring visible dimensions.')
rel('a037','a036','空中像驗證可檢查相位或吸收層修補。','Aerial-image verification can assess phase or absorber repair.','相位設計追求成像；修補還要維持原先設計光學效果。','Phase design targets imaging; repair must preserve the intended optical behavior.')
rel('a037','a038','光場干涉與鄰近耦合是兩者共同基礎。','Field interference and proximity coupling underpin both topics.','相位移改變複數透射；OPC 可透過圖形邊緣修正補償。','Phase shifting changes complex transmission; OPC can compensate by moving pattern edges.')
rel('a038','a039','都用前向成像模型把光罩連到晶圓輪廓。','Both use forward imaging models to connect masks and wafer contours.','傳統 OPC 常調整邊緣；ILT 可搜尋更廣的圖形參數空間。','Conventional OPC often adjusts edges; ILT can search broader mask parameter spaces.')
rel('a038','a049','修正需跨焦距與劑量窗口驗證。','Corrections need verification across focus and dose.','OPC 改變光罩；焦距劑量控制改變曝光條件。','OPC changes the mask; focus–dose control changes exposure conditions.')
rel('a039','a038','校準與獨立驗證都能減少模型偏誤。','Calibration and independent validation reduce model bias in both.','ILT 的自由度與正則化需明確，不能只追求成本下降。','ILT freedoms and regularization must be explicit rather than pursuing cost reduction alone.')
rel('a039','a035','計算光罩必須能轉成可寫入的資料。','Computed masks must become writable data.','理想曲線最佳解仍受束流、圖元與寫入時間限制。','Ideal optimized curves remain constrained by beam, primitives and write time.')
rel('a040','a048','掃描與量測共同決定層間相對位置。','Scanning and metrology jointly determine relative layer placement.','浸潤需管理液體介面；套刻課程集中於位置模型與量測偏差。','Immersion manages fluid interfaces; overlay focuses on placement models and metrology bias.')
rel('a040','a043','浸潤曝光可用於分解後的子圖形。','Immersion exposure can print decomposed pattern subsets.','光學解析度與多次曝光的相對套刻是不同限制。','Optical resolution and relative overlay between exposures are different limits.')
rel('a041','a034','EUV 整合需要光阻吸收與轉移耐受性。','EUV integration needs resist absorption and transfer resistance.','曝光整合還包括光罩、套刻與電性；材料課程深入光阻化學。','Exposure integration also covers masks, overlay and electrical tests; material study examines resist chemistry.')
rel('a041','a042','兩者都連結反射光學、薄光阻與量測。','Both connect reflective optics, thin resist and metrology.','提高 NA 會收緊焦點與場形狀要求，不能直接照搬原窗口。','Higher NA tightens focus and field-shape requirements, so old windows cannot simply be reused.')
rel('a043','a044','都以分解與轉移突破單次圖案密度限制。','Both use decomposition and transfer to exceed single-pattern density limits.','雙次微影與兩輪側壁倍增具有不同套刻與厚度誤差鏈。','Two lithography steps and two spacer cycles have different overlay and thickness error chains.')
rel('a043','a048','相對位置誤差會改變兩組線間距。','Relative placement errors change spacing between line subsets.','圖案化選擇流程；套刻量測估計可補償與殘餘誤差。','Patterning selects the flow; overlay metrology estimates correctable and residual error.')
rel('a044','a043','圖案配色、阻擋與電性載具可共同使用。','Coloring, blocks and electrical vehicles can be studied together.','SAQP 的線位置更多由側壁厚度決定，不等於四次獨立曝光。','SAQP placement depends strongly on spacer thickness and is not four independent exposures.')
rel('a044','a057','側壁沉積的厚度与共形性直接影響線寬。','Spacer thickness and conformality directly affect linewidth.','PECVD 是沉積方法；SAQP 還需多輪選擇性移除與切割。','PECVD is a deposition method; SAQP additionally needs repeated selective removal and cuts.')
rel('a045','a044','都能由較稀疏模板得到較密集規則線群。','Both can produce denser regular lines from sparse guides.','DSA 依賴聚合物相分離；SAQP 依賴側壁沉積與蝕刻。','DSA relies on polymer microphase separation; SAQP relies on spacer deposition and etch.')
rel('a045','a046','模板精度與局部缺陷都會傳入最終圖形。','Template accuracy and local defects propagate into final patterns.','DSA 透過自組裝回應模板；壓印透過接觸直接轉移形貌。','DSA responds to guides by assembly; imprint transfers relief by contact.')
rel('a046','a045','模板、材料与缺陷統計共同決定可用圖案。','Templates, materials and defect statistics determine useful patterns in both.','壓印需處理填充與脫模；自組裝需處理相分離與排列缺陷。','Imprint manages filling and release; self-assembly manages phase separation and ordering defects.')
rel('a046','a047','電子束可作為精細模板製作的研究工具。','Electron beams can serve as research tools for fine-template fabrication.','直寫逐點曝光；壓印反覆複製模板並承受接觸磨耗。','Direct writing exposes sequentially; imprint replicates templates and faces contact wear.')
rel('a047','a035','資料格點、散射修正與拼接概念相通。','Data grids, scattering correction and stitching concepts transfer.','直寫基板與光罩基板的後續用途和尺寸尺度不同。','Direct-write substrates and masks differ in downstream use and dimensional scale.')
rel('a047','a046','都需檢查設計圖形到實體輪廓的偏差。','Both need checks of design-to-physical contour bias.','電子束有散射與充電；壓印有流動、氣泡與脫模。','Electron beams involve scattering and charging; imprint involves flow, bubbles and release.')
rel('a048','a043','套刻向量可預測雙圖形交替間距。','Overlay vectors can predict alternating spacing in split patterns.','量測模型不替代圖案分解或接縫設計。','Metrology models do not replace decomposition or stitch design.')
rel('a048','a049','共同使用取樣、前饋與獨立驗證。','Both use sampling, feedforward and independent validation.','套刻處理橫向相對位置；焦點處理軸向成像條件。','Overlay addresses lateral relative placement; focus addresses axial imaging conditions.')
rel('a049','a048','兩者都需要區分真實變異與感測偏差。','Both distinguish real variation from sensor bias.','焦距劑量窗口與套刻容許區不是相同性能量。','Focus–dose windows and overlay tolerance are not the same metric.')
rel('a049','a050','窗口驗收必須包含缺陷而非只有線寬。','Window acceptance must include defects, not just linewidth.','控制設定尋找可用窗口；統計分析估計罕見失敗機率。','Control selects a usable window; statistics estimates rare-failure probability.')
rel('a050','a034','光阻化學與吸收會影響隨機失敗。','Resist chemistry and absorption affect stochastic failures.','缺陷分析需排除材料外的圖形、量測與蝕刻因素。','Defect analysis must account for pattern, metrology and etch factors beyond materials.')
rel('a050','a049','劑量焦距矩陣可提供缺陷趨勢資料。','Dose–focus matrices supply defect-trend data.','平均尺寸窗口不等於稀有缺陷合格窗口。','An average-dimensional window is not a rare-defect acceptance window.')
rel('a051','a052','表面反應、離子能量與選擇性是共同概念。','Surface reactions, ion energy and selectivity are shared concepts.','連續 RIE 與循環自限制 ALE 需不同速率與飽和驗證。','Continuous RIE and cyclic self-limiting ALE need different rate and saturation tests.')
rel('a051','a056','蝕刻完成度需連結訊號與剩餘膜厚。','Etch completion links signals to remaining thickness.','RIE 決定材料移除；端點偵測處理間接訊號與停止延遲。','RIE removes material; endpoint detection handles indirect signals and stop latency.')
rel('a052','a051','兩者都需檢查輪廓、選擇性與損傷。','Both need profile, selectivity and damage checks.','ALE 循環需證明兩半反應飽和；RIE 不以循環自限制為前提。','ALE must demonstrate half-cycle saturation; RIE does not presume cyclic self-limitation.')
rel('a052','a055','精確移除需要保留周邊材料與介面。','Precise removal must preserve surrounding materials and interfaces.','自限制深度控制與材料對選擇比是不同主張。','Self-limited depth control and pairwise material selectivity are different claims.')
rel('a053','a051','兩者結合化學移除、離子方向性與掩膜。','Both combine chemical removal, ion directionality and masks.','深矽製程更受高深寬比輸運、鈍化與熱接觸限制。','Deep-silicon processing is more constrained by transport, passivation and thermal contact.')
rel('a053','a065','深孔輪廓決定後續阻障與種子覆蓋。','Deep-hole profiles determine subsequent barrier and seed coverage.','蝕刻移除材料；襯層沉積必須在已形成的陰影區保持連續。','Etch removes material; liners must remain continuous in the resulting shadowed regions.')
rel('a054','a053','兩者都需追蹤深寬比相依速率與側壁形貌。','Both track aspect-ratio-dependent rates and sidewall profiles.','介電堆疊充電及層間速率差異不同於深矽蝕刻。','Charging and layer-rate differences in dielectric stacks differ from deep-silicon etching.')
rel('a054','a056','停止層與小開口比例限制端點可辨識性。','Stop layers and small open areas limit endpoint identifiability.','深孔局部完成時間可能不同於全腔平均訊號。','Local deep-hole completion may differ from chamber-average signals.')
rel('a055','a052','都需量測保留材料損失與表面損傷。','Both measure loss and damage in retained materials.','SiGe 選擇性強調材料區分；ALE 強調循環飽和。','SiGe selectivity emphasizes material discrimination; ALE emphasizes cyclic saturation.')
rel('a055','a025','SiGe 可作為薄化停止層並在後段選擇性移除。','SiGe can serve as a thinning stop and later be selectively removed.','通道釋放是側向奈米間隙問題；背面薄化是大面積厚度控制。','Channel release concerns lateral nanogaps; backside thinning concerns large-area thickness control.')
rel('a056','a051','端點訊號需與 RIE 速率及層間轉換校準。','Endpoint signals need calibration against RIE rate and layer transitions.','訊號偵測可靠不代表輪廓與電性自然合格。','Reliable signal detection does not automatically establish profile or electrical acceptance.')
rel('a056','a054','深孔最後完成區域會影響過蝕刻需求。','The last completed deep-hole region affects overetch needs.','全局光訊號可能無法直接辨識最慢孔的剩餘材料。','Global optical signals may not directly reveal material remaining in the slowest hole.')
rel('a057','a058','都需要控制表面反應、膜厚與應力。','Both control surface reaction, thickness and stress.','PECVD 以電漿活化；LPCVD 常依較高溫熱反應與批次管理。','PECVD uses plasma activation; LPCVD commonly uses higher-temperature thermal reactions and batch management.')
rel('a057','a064','低 k 整合需要膜化學、氫與應力證據。','Low-k integration needs film-chemistry, hydrogen and stress evidence.','PECVD 是沉積技術；低 k 還需蝕刻損傷、吸濕與機械驗證。','PECVD is a growth technique; low-k additionally needs etch-damage, moisture and mechanical tests.')
rel('a058','a057','薄膜驗證共同包含厚度、折射率與電性。','Film validation includes thickness, index and electrical behavior in both.','相同材料名稱不代表兩種沉積方法產生相同膜性。','Identical material names do not imply identical properties from the two methods.')
rel('a058','a059','兩者都有氣體輸運與表面反應的競爭。','Both involve competition between gas transport and surface reaction.','MOCVD 常關注化合物磊晶與組成；LPCVD 課程集中矽系薄膜與批次。','MOCVD often targets compound epitaxy and composition; LPCVD here focuses on silicon-family films and batches.')
rel('a059','a058','熱場、流場與反應物耗盡都影響均勻性。','Thermal fields, flow and depletion affect uniformity in both.','磊晶還需晶格、應變與異質界面證據。','Epitaxy additionally needs lattice, strain and heterointerface evidence.')
rel('a059','a060','都需連結到達物種、表面與薄膜性質。','Both link arriving species, surfaces and film properties.','MOCVD 依化學分解；濺鍍依靶原子動量移除。','MOCVD uses chemical decomposition; sputtering uses momentum-driven target removal.')
rel('a060','a065','PVD 濺鍍可用於金屬阻障與種子層。','PVD sputtering can form metal barriers and seed layers.','平面膜質需再延伸到孔底連續性與擴散功能。','Planar film quality must extend to bottom continuity and diffusion function.')
rel('a060','a059','均勻性、應力與界面量測可共同練習。','Uniformity, stress and interface metrology can be practiced together.','物理濺鍍與化學磊晶有不同成核與結晶控制。','Physical sputtering and chemical epitaxy control nucleation and crystallization differently.')
rel('a061','a062','都需填孔、平坦化與接觸電阻驗證。','Both need hole fill, planarization and contact-resistance validation.','鎢常以 CVD/ALD 金屬化；銅雙鑲嵌通常加入種子與電鍍。','Tungsten commonly uses CVD/ALD metallization; copper dual damascene typically adds seed and plating.')
rel('a061','a065','襯層連續性與有效孔徑影響接點電阻。','Liner continuity and effective diameter affect contact resistance.','鎢接點材料系統不應直接套用銅阻障種子流程。','Tungsten-contact material stacks must not simply inherit copper barrier–seed flows.')
rel('a062','a066','雙鑲嵌的線槽與通孔需要無空洞銅填充。','Dual-damascene trenches and vias need void-free copper fill.','電鍍只負責金屬填入；完整整合還包括介電蝕刻與 CMP。','Plating fills metal; complete integration also includes dielectric etch and CMP.')
rel('a062','a063','都以 RC、接點與可靠度衡量互連。','Both evaluate interconnects through RC, contacts and reliability.','銅雙鑲嵌與釕減法半鑲嵌的製程順序不同。','Copper dual damascene and subtractive Ru semi-damascene use different sequences.')
rel('a063','a062','有效截面與襯層比例都影響小尺寸電阻。','Effective area and liner fraction affect nanoscale resistance in both.','替代材料不只是換一個塊材電阻率。','Alternative materials are not merely a substitution of bulk resistivity.')
rel('a063','a064','導體電阻與介電電容共同決定 RC。','Conductor resistance and dielectric capacitance jointly determine RC.','加高金屬降阻可能提高側壁電容，需要低 k 或空氣間隙評估。','Taller metal may lower resistance while increasing lateral capacitance, requiring low-k or air-gap assessment.')
rel('a064','a057','薄膜成分、固化與應力可由成膜階段控制。','Composition, curing and stress can be influenced during growth.','低 k 最終表現還受圖案化與濕氣歷程改變。','Final low-k behavior is also changed by patterning and moisture history.')
rel('a064','a063','替代金屬與低 k 必須共同驗證漏電及機械介面。','Alternative metals and low-k need joint leakage and mechanical-interface validation.','單獨降低 k 或電阻都不保證最終 RC 與可靠度更好。','Reducing k or resistance alone does not guarantee better final RC and reliability.')
rel('a065','a060','濺鍍角度與陰影效應決定襯層厚度分布。','Sputter angles and shadowing determine liner thickness distribution.','種子功能需額外驗證電鍍起始，不能只測平面厚度。','Seed function additionally needs plating-initiation tests, not just planar thickness.')
rel('a065','a066','種子連續性提供局部電鍍電流路徑。','Seed continuity provides local plating-current paths.','電鍍空洞可能来自種子中斷，也可能來自傳質與添加劑。','Plating voids can arise from seed gaps or from transport and additives.')
rel('a066','a062','電鍍填充結果決定雙鑲嵌內部空洞與過鍍。','Plating determines internal voids and overburden in dual damascene.','填孔完成還需要 CMP、通孔接觸與介電隔離驗收。','Completed fill still needs CMP, via-contact and dielectric-isolation acceptance.')
rel('a066','a065','潤濕、表面氧化與供電連續性連結兩門課。','Wetting, surface oxidation and current continuity connect the topics.','阻障需要阻擴散；種子需要導通；電鍍需要適當局部反應速率。','Barriers block diffusion; seeds conduct; plating requires suitable local reaction rates.')
src('nil2018','奈米壓印研發的工業化故事','Nanoimprint opens a new door','Canon','https://global.canon/en/business/group/industry/2018.html','模板轉移、缺陷與產業研發背景。','Template transfer, defects and industrial research context.')
DATA['a046']['refs'].append('nil2018')
DATA['a059']['place']='aix'

# Reuse already verified V7 campus points and their original provenance.
existing_places=json.loads((ROOT/'public/academy/data/course-places.json').read_text())['courses']
oldplace={x['courseId']:x for x in existing_places}
P={
 'imec':copy.deepcopy(oldplace['a025']['place']),
 'nist':copy.deepcopy(oldplace['a310']['place']),
 'asml':copy.deepcopy(oldplace['a042']['place']),
 'aix':dict(name='AIXTRON Herzogenrath 總部（建物代表點）',nameEn='AIXTRON Herzogenrath headquarters: building reference',city='黑爾措根拉特',cityEn='Herzogenrath',country='德國',countryEn='Germany',lat=50.823395,lng=6.079164,address='Dornkaulstraße 2, 52134 Herzogenrath, Germany',addressEn='Dornkaulstraße 2, 52134 Herzogenrath, Germany',mapQuery='Dornkaulstraße 2, 52134 Herzogenrath, Germany',coordinateScope='官方地址經核對；座標是 OpenStreetMap 建物 192119752 不重複頂點的算術平均代表點，不是入口、實驗室或精確幾何重心。',coordinateScopeEn='Official address checked; coordinates are the mean of unique vertices of OpenStreetMap building 192119752, not an entrance, laboratory or exact geometric centroid.')
}
P['nist']['name']='NIST Gaithersburg／CNST NanoFab 園區代表點'
P['nist']['nameEn']='NIST Gaithersburg / CNST NanoFab campus reference'
P['nist']['coordinateScope']='沿用已核對的 NIST 園區近似代表點，官方地址為 100 Bureau Drive；不是特定機台、無塵室或訪客入口座標。'
P['nist']['coordinateScopeEn']='Previously checked approximate NIST campus reference; official address is 100 Bureau Drive, not a specific instrument, cleanroom or visitor entrance.'
for place in P.values():
 place['mapQuery']=f"{place['lat']},{place['lng']}"
H={
'imec':[('1984','imec 在魯汶成立','imec begins in Leuven','官方總部沿革將魯汶列為 1984 年發展的起點。','The official headquarters history identifies Leuven as the 1984 starting point.','imecplace'),('2017','公開混合圖案化整合案例','A public hybrid-patterning integration case','imec 說明 SAQP 與 EUV 阻擋圖案化如何共同服務金屬層整合。這是產業研發沿革，不表示本課程全部技術於當年或此地發明。','imec described combining SAQP and EUV block patterning for metal-layer integration. This is research history, not a claim that every course technology was invented there or then.','saqp')],
'nist':[('2007','CNST 成立','CNST is established','NIST 原始文章記錄 CNST 在 2007 年 5 月成立，連結奈米製造與量測。','The NIST original article records CNST establishment in May 2007, linking nanofabrication and measurement.','nisthistory'),('2023','NanoFab 重新向研究使用者開放','NanoFab reopens to research users','NIST 公告設施重新開放，介紹微影、蝕刻、沉積與表徵的共同工作。','NIST announced reopening and described complementary lithography, etch, deposition and characterization work.','nistreopen')],
'asml':[('1984','ASML 成立','ASML is founded','ASML 官方沿革記錄 Philips 與 ASMI 共同建立微影公司。','ASML history records the lithography venture founded by Philips and ASMI.','asmlhistory'),('2003','首台浸潤式系統登場','First immersion system debuts','官方沿革列出 TWINSCAN AT:1150i，說明成像改進也需要掃描與量測整合。','The official history lists the TWINSCAN AT:1150i, illustrating that imaging advances need scanning and metrology integration.','asmlhistory')],
'aix':[('1983','AIXTRON 成立','AIXTRON is founded','官方沿革記錄亞琛大學半導體技術研究所人員創立公司。','The official chronology records founding by members of RWTH Aachen semiconductor technology.','aixhistory'),('1985','第一套 MOCVD 系統啟用','First MOCVD system is commissioned','官方沿革列出首套系統啟用；後續行星式與淋浴式反應器為不同技術路線。','The official chronology lists commissioning of the first system; planetary and showerhead reactors later represent distinct approaches.','aixhistory')]
}
PLACE_REFS={'imec':['imecplace','saqp'],'nist':['nistplace','nisthistory','nistreopen','nisttools'],'asml':['asmlhistory'],'aix':['aixplace','aixmap','aixhistory']}

def pair(x):return x.split('|')
def reference(k):return {f:S[k][f] for f in ['title','titleEn','publisher','url','scope','scopeEn']}

# Reusable evidence formats change with the investigation's purpose, while
# the action, technical conclusion and applicable misconception are authored.
EVIDENCE=[
 ('附上帶材料、方向與尺度標記的示意圖，圈出一處不能由圖單獨推論的量。','Attach a diagram labeled with materials, directions and scales; circle one quantity not inferable from the drawing alone.'),
 ('建立兩種條件的對照表，分別寫出固定量、改變量與可量測的輸出。','Build a two-condition comparison table listing fixed quantities, changed quantities and measurable outputs.'),
 ('用自訂並標明的假設資料做一個計算或分類例，保留單位、分母與中間結果。','Use explicitly hypothetical data for one calculation or classification; retain units, denominators and intermediate results.'),
 ('建立因果與量測對照表，區分直接觀測、模型推論與尚需額外證據的結論。','Build a cause–measurement table separating direct observations, model inferences and conclusions needing more evidence.'),
 ('列出一個可能混淆原因，提出能區分兩個解釋的對照或額外量測。','List one plausible confounder and propose a control or measurement distinguishing two explanations.'),
 ('完成一頁審查紀錄，列出接受条件、證據缺口與不應外推的範圍。','Complete a one-page review listing acceptance criteria, evidence gaps and limits on extrapolation.')
]
COURSES=[];PLACES=[];RELATED=[]
for cid,d in DATA.items():
 c=copy.deepcopy(CAT[cid]);c.update(status='guided',contentStatus='reviewable-educational-curriculum',depth=4,stepCount=24,estimatedMinutes=720,languageCoverage=['zh-TW','en'],simulationOnly=True,curriculumVersion=8)
 refs=d['refs'];c['sourceIds']=[S[k]['id'] for k in refs]
 stnames=[pair(s) for s in d['stages']]
 c['summary']='以四階段、24 個工程判讀工作包，逐步研究'+ '、'.join(x[0] for x in stnames)+'；每步交付圖表、對照、計算或驗證紀錄。'
 c['summaryEn']='Work through 24 engineering investigations in four stages: '+', '.join(x[1].lower() for x in stnames)+'. Each step produces a diagram, comparison, calculation or verification record.'
 c['scope']='依公開原理編寫的教學課程；24 步是研究與工程判讀任務，不是完整晶圓廠配方或設備操作指令。自訂數據須標示假設，數值不代表任何廠商製程。課程內容完整提供繁體中文與英文。'
 c['scopeEn']='Educational investigations based on public principles. These 24 steps are research and engineering-review tasks, not complete fab recipes or equipment operating instructions. Hypothetical data must be labeled and do not represent any vendor process. Full content is supplied in Traditional Chinese and English.'
 c['diagram']={'type':'wafer','labels':[x[0] for x in stnames],'labelsEn':[x[1] for x in stnames],'original':True,'notToScale':True}
 c['stages']=[]
 for g,(sz,se) in enumerate(stnames):
  pz,pe=pair(d['principles'][g]);ez,ee=pair(d['errors'][g]);stage={'id':f'{cid}-v8-stage{g+1:02}', 'order':g+1,'title':sz,'titleEn':se,'description':pz,'descriptionEn':pe,'steps':[]}
  for j in range(6):
   i=g*6+j;n=i+1;tz,te,fz,fe=d['rows'][i];rz,re=EVIDENCE[j]; otherz,othere=pair(d['errors'][(g+1)%4]);answer=i%3
   opts=[ez,otherz];optse=[ee,othere];opts.insert(answer,fz);optse.insert(answer,fe)
   step={'id':f'{cid}-v8-{n:02}','order':n,'sequence':n,'estimatedMinutes':30,'simulationOnly':True,'sourceIds':list(c['sourceIds']),'prerequisiteIds':[] if n==1 else [f'{cid}-v8-{n-1:02}'],
     'title':tz,'titleEn':te,'objective':'透過本步證據判讀：'+fz,'objectiveEn':'Use this investigation to assess the following principle: '+fe,
     'instruction':tz+'。先讀本步來源，標出其實際材料、圖形或工具適用範圍，再以教學草圖或明確假設資料完成任務。'+rz+'最後以「'+fz+'」檢查推論是否超出證據。',
     'instructionEn':te+'. Read the step sources and identify their actual material, pattern or tool scope. Complete the task using an educational sketch or explicitly hypothetical data. '+re+' Finally check your inference against this principle: '+fe,
     'observation':fz+' 本步須保留至少一項直接觀測與一項推論的區別。','observationEn':fe+' Preserve the distinction between at least one direct observation and one inference.',
     'failure':'若報告假設「'+ez+'」，回到本階段原理重畫因果鏈，並補上反例或未量測項。','failureEn':'If the report assumes "'+ee+'", revisit the stage principle, redraw the causal chain and add a counterexample or unmeasured quantity.',
     'check':'交付「'+tz+'」的圖表或計算、採用來源、假設與單位；說明本步結論「'+fz+'」可由哪些證據支持，並保留一項限制。','checkEn':'Submit the diagram, table or calculation for "'+te+'", with sources, assumptions and units. Identify evidence supporting "'+fe+'" and retain one limitation.',
     'knowledge':[{'id':f'{cid}-v8-{n:02}-k1','title':'本步技術判讀','titleEn':'Step-specific technical interpretation','text':fz,'textEn':fe},{'id':f'{cid}-v8-{n:02}-k2','title':sz+'的原理與限制','titleEn':se+': principle and limits','text':pz,'textEn':pe}],
     'quiz':{'question':'完成「'+tz+'」後，哪項判讀可靠？','questionEn':'After "'+te+'", which interpretation is defensible?','options':opts,'optionsEn':optse,'answer':answer,'explanation':fz+' '+pz,'explanationEn':fe+' '+pe}}
   stage['steps'].append(step)
  c['stages'].append(stage)
 COURSES.append(c)
 pk=d['place']; pref=list(dict.fromkeys(PLACE_REFS[pk]+refs[:2])); history=[]
 for y,t,te,tx,txe,k in H[pk]:history.append(dict(year=y,title=t,titleEn=te,text=tx,textEn=txe,sourceIds=[S[k]['id']]))
 p={'courseId':cid,'place':copy.deepcopy(P[pk]),'summary':c['title']+'涉及跨國材料、設備與量測合作。本課程地圖選用'+P[pk]['name']+'作為公開研究或設備技術的代表位置。課程練習以公開原理連結圖形、材料與驗證，不宣稱此處為唯一發明地、所有技術的生產工廠或實際機台位置。','summaryEn':c['titleEn']+' involves international collaboration in materials, equipment and metrology. The map uses '+P[pk]['nameEn']+' as a public research or equipment-technology reference. Exercises connect patterns, materials and validation through public principles; this is not claimed to be the sole invention site, a factory producing every technology, or an instrument location.','history':history,'connection':'比較相關課程時，逐項追蹤材料、圖案形成方式、誤差與驗收證據的差異；相似原理不表示配方可直接移植。','connectionEn':'Compare related courses by materials, pattern formation, errors and acceptance evidence. Similar principles do not make recipes directly transferable.','references':[reference(k) for k in pref],'sourceIds':[S[k]['id'] for k in pref]}
 if pk=='asml':p['references']+=copy.deepcopy(oldplace['a042']['references'][:2])
 if cid=='a046':
  p['summary']+=' 此處僅代表共通圖案化研究脈絡；Canon 奈米壓印設備的研發地點另見 Canon 官方來源，並不宣稱位於此園區。'
  p['summaryEn']+=' This point represents shared patterning research context only; Canon nanoimprint equipment development is described in the Canon sources and is not claimed to occur on this campus.'
 PLACES.append(p)
 related=[]
 for target in d['neighbors']:
  t,te,df,dfe=REL[(cid,target)]
  if target in DATA: other=DATA[target]['rows'][0][:2]
  else:other=('畫出「'+CAT[target]['title']+'」與本課程的材料或訊號交接','Draw the material or signal handoff between '+CAT[target]['titleEn']+' and this course')
  practices=[d['rows'][0][0],other[0],'就「'+t+'」列出一項可沿用原理與一項必須重新驗證的條件']
  practicesEn=[d['rows'][0][1],other[1],'For "'+te+'", identify one transferable principle and one condition needing revalidation']
  related.append({'id':target,'transfer':t,'transferEn':te,'difference':df,'differenceEn':dfe,'practice':practices,'practiceEn':practicesEn,'referenceUrls':[S[k]['url'] for k in refs]})
 RELATED.append({'courseId':cid,'related':related,'references':[reference(k) for k in refs]})

OUT={'version':8,'group':'b','courses':COURSES,'sources':list(S.values()),'places':PLACES,'related':RELATED,'media':[]}
# One individually designed worked example per course. Numbers are fictional
# teaching inputs, not recommended operating conditions or manufacturer data.
WORKED={
'a034':(4,'假設均勻膜的吸收係數 α=0.020 nm⁻¹、厚度 t=20 nm、入射光子數 100。計算 T=exp(-αt)=0.6703，約 67.0 個等效光子穿透、33.0 個被吸收；厚度改為 40 nm 時吸收比例為 55.1%。比較吸收增加與實際化學轉換兩件事，不能由此計算單獨宣告感度或缺陷率。','Assume a uniform-film absorption coefficient α=0.020 nm⁻¹, thickness t=20 nm and 100 incident equivalent photons. T=exp(-αt)=0.6703 gives 67.0 transmitted and 33.0 absorbed. At 40 nm, absorption becomes 55.1%. Separate increased absorption from chemical conversion; this calculation alone establishes neither sensitivity nor defect rate.','結果須有 33.0% 與 55.1%，並註明反應產率尚未量測。','Report 33.0% and 55.1%, explicitly noting that reaction yield is unmeasured.'),
'a035':(7,'假設某圖元曝光面積為 100 μm²、所需總電荷為 0.20 nC、束流為 1.0 nA。先換算 100 μm²=10⁻⁶ cm²，再得面劑量 200 μC/cm²，理想駐留總時間 Q/I=0.20 s。另有 0.10 s 載台與資料開銷時，總時間是 0.30 s；不可把理想束流時間當作整體吞吐量。','Assume a 100 μm² exposed area, total charge 0.20 nC and beam current 1.0 nA. Convert the area to 10⁻⁶ cm²: dose is 200 μC/cm² and ideal beam time Q/I is 0.20 s. With 0.10 s of stage and data overhead, total time is 0.30 s; beam time alone is not throughput.','確認面積換算、200 μC/cm² 與 0.30 s，分開曝光和開銷。','Check the area conversion, 200 μC/cm² and 0.30 s, separating exposure and overhead.'),
'a036':(9,'假設盲測標準片有 100 處已知缺陷及 100 處已知正常區。檢查器找出 90 處真缺陷，但將 5 處正常區誤報。列出 TP=90、FN=10、FP=5、TN=95；漏檢率為 10%，誤報率為 5%。若只報告 95 次警報，無法得知靈敏度；並須說明此結果只適用於標準片所涵蓋的缺陷尺寸與類型。','A hypothetical blind standard contains 100 known defects and 100 clean sites. Inspection detects 90 true defects and falsely flags 5 clean sites: TP=90, FN=10, FP=5, TN=95. The miss rate is 10% and false-positive rate 5%. Reporting 95 alarms alone cannot establish sensitivity. The result applies only to the defect sizes and classes represented by the standard.','交付四格表、10% 與 5%，不可用警報總數代替辨識性能。','Submit the confusion matrix, 10% and 5%; do not substitute alarm count for detection performance.'),
'a037':(2,'假設兩束相干光的振幅皆為 1。相位差 0 時，I=|1+1|²=4；相位差 π 時，I=|1-1|²=0。若第二束振幅僅 0.8，反相後 I=|1-0.8|²=0.04，便不是完全黑暗。畫出複數向量，說明相位正確仍需要振幅匹配；此為兩束光模型，不是完整投影系統。','Assume coherent fields with amplitudes 1 and 1. At phase difference 0, I=|1+1|²=4; at π, I=|1-1|²=0. If the second amplitude is 0.8, opposing fields give I=|1-0.8|²=0.04 rather than complete darkness. Draw complex vectors and explain why phase alone is insufficient without amplitude matching. This is a two-field model, not a complete projection system.','須得到 4、0、0.04，不能直接相加兩束強度。','Obtain 4, 0 and 0.04 without directly adding intensities.'),
'a038':(16,'設目標晶圓邊緣 x=100 nm，初始模擬位置 x=94 nm。採用局部線性教學模型：4 倍縮小光罩的邊緣移動 +8 nm，晶圓邊緣只移動 +2 nm。一次修正後位置為 96 nm，帶符號誤差由 -6 nm 變為 -4 nm。不要把光罩 +8 nm 直接加到晶圓；實際 OPC 須重新模擬鄰近耦合，不能永遠沿用此固定斜率。','Let the wafer target edge be x=100 nm and the initial prediction x=94 nm. In a local linear teaching model with 4× mask reduction, moving a mask edge +8 nm shifts the wafer edge only +2 nm. The new prediction is 96 nm and signed error changes from -6 to -4 nm. Do not add mask displacement directly to the wafer. Real OPC needs neighborhood resimulation instead of assuming this slope always holds.','交付修正前後 -6 nm 與 -4 nm，以及光罩／晶圓尺度標記。','Report -6 nm and -4 nm with explicit mask/wafer scale labels.'),
'a039':(9,'比較兩個假想候選光罩，使用無因次成本 J=E²+λP。A 的 E=2、P=16；B 的 E=3、P=1。λ=0 時 J_A=4、J_B=9，選 A；λ=1 時 J_A=20、J_B=10，選 B。求交叉點 λ=1/3。說明 P 是本例定義的複雜度罰項，並非真實光罩寫入成本；權重改變會改變最佳解。','Compare hypothetical masks with dimensionless cost J=E²+λP. A has E=2, P=16; B has E=3, P=1. At λ=0, costs are 4 and 9, favoring A; at λ=1, costs are 20 and 10, favoring B. The crossover is λ=1/3. P is an illustrative complexity penalty, not actual mask-writing cost. Changing weights changes the preferred solution.','須算出 4/9、20/10 及 λ=1/3，並交代罰項定義。','Calculate 4/9, 20/10 and λ=1/3, stating the penalty definition.'),
'a040':(3,'假設波長、k₁、k₂ 都固定，只把 NA 從 1.00 改為 1.35。由 CD∝1/NA，CD 比值為 0.741；由 DOF∝1/NA²，焦深比值為 0.549。若原假想 CD=100 nm、DOF=200 nm，新值約為 74.1 nm、109.7 nm。這是相對縮放示例，不能視為特定掃描機的保證尺寸。','Hold wavelength, k₁ and k₂ fixed while changing NA from 1.00 to 1.35. CD∝1/NA gives a ratio of 0.741; DOF∝1/NA² gives 0.549. Hypothetical initial CD=100 nm and DOF=200 nm become approximately 74.1 nm and 109.7 nm. These are scaling examples, not scanner performance guarantees.','同時報告解析度改善與焦深縮小，不可只選前者。','Report both improved resolution and reduced depth of focus.'),
'a041':(1,'在假設的四面反射鏡教學光路中，每面能量反射率皆為 0.70，且忽略其他損失。總傳輸比例為 0.70⁴=0.2401；100 單位入射能量只剩 24.01 單位。若其中一面因污染變成 0.60，剩餘為 0.70³×0.60=20.58，較原來降低 14.3%。本例鏡數與反射率不是任何 EUV 機台規格。','In a hypothetical four-mirror path, each mirror has energy reflectivity 0.70 and other losses are ignored. Total transmission is 0.70⁴=0.2401, leaving 24.01 of 100 incident energy units. If one mirror falls to 0.60, the result is 0.70³×0.60=20.58, a 14.3% relative decrease. Mirror count and reflectivities are not specifications of any EUV scanner.','用乘積得到 24.01 與 20.58，不可把反射率直接相加。','Use products to obtain 24.01 and 20.58; do not add reflectivities.'),
'a043':(13,'設兩組交錯線條在完美對位時的左右間隙皆為 40 nm。第二組向右偏移 5 nm，而線寬不變，則左右間隙變成 45 nm 與 35 nm，平均仍為 40 nm。若最小間隙要求為 36 nm，這組圖形不合格，即使平均間隙完全正確。畫出帶方向的套刻向量與兩個間隙。','Two interleaved line sets have 40 nm gaps on both sides at ideal alignment. Shift the second set 5 nm right without changing widths: gaps become 45 and 35 nm while their mean remains 40 nm. A 36 nm minimum-gap requirement is violated despite the correct mean. Draw the signed overlay vector and both gaps.','交付 45/35 nm 與不合格理由，明確指出平均值盲點。','Report 45/35 nm and the failure reason, identifying the mean-value blind spot.'),
'a044':(1,'設理想骨架節距為 160 nm；每輪側壁倍增恰好使規則線群節距減半。第一輪為 80 nm，第二輪為 40 nm。這並不表示最終線寬是 40 nm：若目標線寬為 15 nm，名目間隙應為 25 nm。另標記切割光罩的位置需求，避免把四倍線密度誤解為完整電路已完成。','Assume an ideal 160 nm mandrel pitch and each spacer multiplication exactly halves regular-line pitch. The first cycle gives 80 nm and the second 40 nm. Final linewidth is not therefore 40 nm: a 15 nm line leaves a nominal 25 nm gap. Also mark cut-mask placement requirements so fourfold line density is not mistaken for a completed circuit.','須區分 160→80→40 nm 節距、15 nm 線寬及 25 nm 間隙。','Distinguish 160→80→40 nm pitch, 15 nm width and 25 nm gap.'),
'a045':(14,'假設對 10⁶ 個獨立且同分布的自組裝位置檢查，未發現缺陷。以零事件近似 95% 上限 3/N，得到 p<約 3×10⁻⁶；不是 p=0。若空間群聚讓有效独立樣本數只剩 10⁵，上限變為約 3×10⁻⁵。畫出分散與群聚取樣，說明需先驗證獨立性。','Inspect 10⁶ hypothetical independent, identically distributed assembly sites and observe no defects. The approximate zero-event 95% upper bound 3/N is about 3×10⁻⁶, not zero. If spatial clustering reduces effective independent samples to 10⁵, the bound becomes about 3×10⁻⁵. Sketch dispersed and clustered sampling and explain the independence requirement.','交付兩個上限與獨立性限制，不宣稱零缺陷製程。','Report both bounds and the independence limitation without claiming a defect-free process.'),
'a046':(7,'假設模板凹槽總體積 100 μm³，壓印區面積 1000 μm²，目標殘留層厚度 0.020 μm。理想所需樹脂體積為 100+1000×0.020=120 μm³。若滴入 140 μm³且完全填充、沒有流出或收縮，殘留層為 (140-100)/1000=0.040 μm，即 40 nm。實際還需評估氣泡、收縮與局部密度，不能只用總體積保證均勻。','Assume 100 μm³ of template-cavity volume, 1000 μm² imprint area and a target 0.020 μm residual layer. Ideal resin volume is 100+1000×0.020=120 μm³. Dispensing 140 μm³ with complete filling and no outflow or shrinkage yields (140-100)/1000=0.040 μm, or 40 nm, residual thickness. Bubbles, shrinkage and local density still matter; total volume does not guarantee uniformity.','算出 120 μm³與 40 nm，並列出體積守恆假設。','Calculate 120 μm³ and 40 nm and state the volume-conservation assumptions.'),
'a047':(5,'假設完整曝光面積為 1 mm²=0.01 cm²、面劑量 100 μC/cm²、束流 1 nA。總電荷為 1 μC，理想束流時間為 1000 s。再加 120 s 載台與資料開銷，總時間為 1120 s，約 18.7 min。這只是單一曝光面積的電荷帳本；不代表特定光阻配方或機台吞吐量。','Assume a fully exposed area of 1 mm²=0.01 cm², dose 100 μC/cm² and current 1 nA. Total charge is 1 μC and ideal beam time 1000 s. Adding 120 s of stage/data overhead gives 1120 s, about 18.7 min. This is a charge ledger for one area, not a resist recipe or tool-throughput claim.','交付面積換算、1 μC 與 1120 s，勿漏掉非曝光開銷。','Show the area conversion, 1 μC and 1120 s without omitting non-exposure overhead.'),
'a048':(9,'在簡化一維例中，x=-1 mm 的套刻位移為 +1 nm，x=+1 mm 為 +3 nm。擬合 Δx=t+s x，得到平移 t=2 nm、縮放 s=1 nm/mm=1 ppm。若 x=0 的保留點實測為 +4 nm，模型預測只有 +2 nm，殘差 +2 nm 提醒你兩個校準點不足以證明完整形變模型。','In a one-dimensional example, overlay displacement is +1 nm at x=-1 mm and +3 nm at x=+1 mm. Fitting Δx=t+s x gives translation t=2 nm and scale s=1 nm/mm=1 ppm. If a held-out point at x=0 measures +4 nm, the model predicts only +2 nm and residual is +2 nm. Two calibration points do not establish a complete distortion model.','需有 2 nm、1 ppm 及保留點 +2 nm 殘差。','Report 2 nm, 1 ppm and the held-out +2 nm residual.'),
'a049':(10,'假設線條 A 的合格焦距範圍為 [-40,40] nm、正規化劑量 [0.90,1.10]；接觸孔 B 為 [-20,30] nm、劑量 [0.95,1.05]，並先忽略交互作用。共同窗口為 [-20,30]×[0.95,1.05]，幾何中心是焦距 +5 nm、劑量 1.00。點 (+35 nm,1.00) 對 A 合格卻對共同窗口不合格。','Assume line A passes at focus [-40,40] nm and normalized dose [0.90,1.10]; contact B passes at [-20,30] nm and [0.95,1.05], initially ignoring interactions. Their common window is [-20,30]×[0.95,1.05], with geometric center (+5 nm,1.00). The point (+35 nm,1.00) passes A but fails the common window.','交付交集與 +5 nm/1.00 中心，並說明矩形與忽略交互作用假設。','Report the intersection and +5 nm/1.00 center, stating rectangular-window and no-interaction assumptions.'),
'a050':(7,'假設 N=100000 個獨立、同分布機會皆無缺陷。精確單側 95% 二項上限為 p=1-0.05^(1/N)=2.9957×10⁻⁵，近似 3/N=3.0×10⁻⁵。若報告 p=0，便超出資料支持範圍。另說明漏檢與空間相關會破壞此計算的假設；此範例沒有實際晶圓良率數據。','For N=100000 independent identically distributed opportunities with zero defects, the exact one-sided 95% binomial upper bound is p=1-0.05^(1/N)=2.9957×10⁻⁵; 3/N approximates it as 3.0×10⁻⁵. Reporting p=0 exceeds the evidence. Missed detections and spatial correlation violate assumptions; the example contains no measured wafer-yield data.','精確值與近似值需一致至約 0.15%，並列出至少一個假設。','Exact and approximate values should agree within about 0.15%; state at least one assumption.'),
'a051':(8,'假設 20 s 內目標膜減少 100 nm、掩膜減少 10 nm。速率分別為 5.0 與 0.50 nm/s，選擇比為 10。若保持同速率再延長 4 s，目標膜多移除 20 nm、掩膜多損失 2 nm。說明此線性外推只適用於本假想穩態區間，不能忽略停止層與負載改變。','Assume target loss of 100 nm and mask loss of 10 nm in 20 s. Rates are 5.0 and 0.50 nm/s, giving selectivity 10. Four extra seconds at the same rates remove 20 nm more target and 2 nm more mask. This linear extrapolation applies only to the hypothetical steady interval and cannot ignore stop layers or loading changes.','交付 5.0、0.50、10、20 nm 與 2 nm，分清速率和選擇比。','Report 5.0, 0.50, 10, 20 nm and 2 nm, distinguishing rates from selectivity.'),
'a052':(5,'設完整循環移除量 0.20 nm；僅改質對照 0.02 nm；僅移除對照 0.03 nm。本例定義協同分率 S=[E_full-(E_mod+E_remove)]/E_full，得到 S=0.75。即使 S 高，仍必須另畫暴露時間飽和曲線，因為協同性不單獨證明自限制；0.20 nm 也不代表恰好一個晶格層。','Let full-cycle removal be 0.20 nm, modification-only removal 0.02 nm and removal-only control 0.03 nm. Define synergy S=[E_full-(E_mod+E_remove)]/E_full; S=0.75. High synergy still requires exposure-time saturation curves because synergy alone does not establish self-limitation. Nor does 0.20 nm necessarily equal one lattice plane.','以明示定義得到 75%，並保留飽和性尚需驗證的結論。','Obtain 75% using the stated definition and retain the need for saturation verification.'),
'a053':(3,'假設溝槽目標深度 100 μm、孔寬 5 μm，深寬比為 20。若矽對硬罩選擇比為 50，理想硬罩消耗為 2 μm；初始 2.5 μm 僅剩 0.5 μm。若另需 20% 等效過蝕刻，硬罩總消耗為 2.4 μm，只剩 0.1 μm。數值是假想預算，未包含均勻性與側向侵蝕。','Assume a 100 μm target depth and 5 μm width: aspect ratio is 20. At silicon-to-mask selectivity 50, ideal mask loss is 2 μm, leaving 0.5 μm from an initial 2.5 μm. Adding 20% equivalent overetch raises loss to 2.4 μm and leaves only 0.1 μm. These are hypothetical budgets excluding nonuniformity and lateral erosion.','須報告 AR=20、剩餘 0.5/0.1 μm，並指出小裕量風險。','Report AR=20 and 0.5/0.1 μm remainder, identifying the small-margin risk.'),
'a054':(13,'假設介電孔深 1000 nm，孔口 100 nm，中段最大孔徑 120 nm，孔底最小孔徑 60 nm。以孔口計 AR=10，但以最小孔徑計有效幾何比為 16.7；中段相對孔口膨脹 20%。在同一截面標出三個量測位置，不能只用孔口照片宣告全孔垂直與等寬。','Assume a 1000 nm deep dielectric hole with 100 nm opening, 120 nm maximum mid-depth diameter and 60 nm minimum bottom diameter. Opening-based AR is 10, while the minimum-diameter ratio is 16.7; mid-depth bow is 20% relative to the opening. Mark all three sites in one section rather than declaring a straight, uniform hole from an opening image.','交付 10、16.7、20% 與三位置截面標記。','Report 10, 16.7 and 20% with three labeled cross-sectional sites.'),
'a055':(3,'假設同一處理後 SiGe 損失 100 nm，Si 損失 2.0 nm，選擇比為 50。若另一測試的 Si 損失低於 0.20 nm 偵測限，只能在量測前提下說明選擇比大於 500，不能報告無限大或矽零損失。另指出平面試片結果仍需在奈米間隙幾何重新驗證。','Assume 100 nm SiGe loss and 2.0 nm Si loss in the same treatment: selectivity is 50. If another test has Si loss below a 0.20 nm detection limit, the measurement supports a lower bound above 500, not infinite selectivity or zero silicon loss. Blanket-sample results still need revalidation in nanogap geometry.','分別報告 50 與 >500，清楚標出偵測限。','Report 50 and >500 separately and state the detection limit.'),
'a056':(15,'假設穩態速率 2.0 nm/s，感測延遲 0.20 s、濾波判讀 0.50 s、停止反應延遲 0.30 s。總延遲 1.00 s，額外移除量約 2.0 nm。若實際速率介於 1.8–2.2 nm/s，延遲所致移除量也介於 1.8–2.2 nm。忽略化學反應停止後的殘餘效應，並把此限制寫入報告。','Assume steady removal 2.0 nm/s, sensing delay 0.20 s, filtering/decision delay 0.50 s and process-stop delay 0.30 s. Total latency is 1.00 s, causing about 2.0 nm extra removal. A rate range of 1.8–2.2 nm/s gives 1.8–2.2 nm extra removal. State that residual post-stop chemistry is excluded.','必須把三種延遲相加，得到 1.00 s 與 1.8–2.2 nm 範圍。','Sum all three delays to obtain 1.00 s and the 1.8–2.2 nm range.'),
'a057':(19,'使用假想平行板電容 A=1.00 mm²、膜厚 t=1.00 μm、C=35.416 pF，忽略邊緣與寄生電容。由 εr=Ct/(ε0A)，ε0=8.854×10⁻¹² F/m，得到 εr=4.00。若未扣除 5 pF 寄生，表觀值約 4.565；這說明量測寄生不能直接歸因於膜成分。','Use a hypothetical parallel-plate capacitor with A=1.00 mm², t=1.00 μm and C=35.416 pF, initially neglecting fringing and parasitics. εr=Ct/(ε0A), with ε0=8.854×10⁻¹² F/m, gives 4.00. An unremoved 5 pF parasitic gives an apparent 4.565, showing why parasitics cannot be attributed directly to film composition.','交付 SI 單位換算、4.00 與約 4.565，並明示寄生假設。','Show SI conversions, 4.00 and about 4.565, stating parasitic assumptions.'),
'a058':(7,'假設三個爐管位置的見證片膜厚為 50、55、60 nm。平均值為 55 nm；本例定義半範圍不均勻度 U=(max-min)/(2mean)=9.09%。若另一批三片皆 55 nm，平均仍相同但 U=0。只用批次平均無法判斷軸向均勻性；三片也不足以證明所有晶圓位置。','Three hypothetical furnace witness wafers measure 50, 55 and 60 nm. Mean is 55 nm; define half-range nonuniformity U=(max-min)/(2mean)=9.09%. Another batch with three 55 nm values has the same mean but U=0. Batch means cannot establish axial uniformity, and three wafers cannot establish every position.','交付 55 nm、9.09% 與取樣限制，明確定義均勻度公式。','Report 55 nm, 9.09% and sampling limits with the uniformity formula stated.'),
'a059':(14,'假設兩片磊晶樣品的 PL 峰位為 450 與 460 nm，以 E≈1240/λ(nm) eV 換算為 2.756 與 2.696 eV，能量下降約 0.060 eV。這個紅移可能牽涉組成、應變、溫度或量子井厚度，不能只由峰位反推唯一材料組成；提出 XRD 或厚度對照以區分。','Hypothetical epitaxial samples have PL peaks at 450 and 460 nm. E≈1240/λ(nm) eV gives 2.756 and 2.696 eV, a decrease of about 0.060 eV. Composition, strain, temperature or well thickness can cause such a redshift; peak position alone cannot uniquely determine composition. Propose XRD or thickness controls to distinguish causes.','算出約 60 meV 紅移，並保留至少兩種可能原因。','Calculate an approximately 60 meV redshift and retain at least two possible causes.'),
'a060':(18,'假設均勻且連續的濺鍍膜厚 50 nm，片電阻 20 Ω/□。由 ρ=Rs t 得 ρ=1.0×10⁻⁶ Ω·m=100 μΩ·cm。若厚度估計偏高 10%，推算電阻率也偏高 10%。此關係假設連續膜與適當幾何修正；不連續島狀膜不能直接用同一塊材模型解釋。','Assume a uniform continuous sputtered film 50 nm thick with sheet resistance 20 Ω/□. ρ=Rs t gives 1.0×10⁻⁶ Ω·m=100 μΩ·cm. A 10% high thickness estimate makes inferred resistivity 10% high. The relation assumes a continuous film and proper geometry correction; disconnected islands cannot be interpreted with the same bulk-film model.','交付 100 μΩ·cm、誤差傳遞與連續膜假設。','Report 100 μΩ·cm, error propagation and the continuous-film assumption.'),
'a061':(4,'假設圓柱插塞長 100 nm、直徑 20 nm、有效電阻率 2.0×10⁻⁷ Ω·m。R=ρL/[π(d/2)²]≈63.7 Ω；上下介面各 10 Ω 時總計約 83.7 Ω。直徑減半時主體電阻變為約 254.6 Ω，總計 274.6 Ω，而不是 83.7 的四倍；介面在此簡化例中假設固定。','Assume a cylindrical plug with length 100 nm, diameter 20 nm and effective resistivity 2.0×10⁻⁷ Ω·m. R=ρL/[π(d/2)²]≈63.7 Ω. With 10 Ω at each interface, total is about 83.7 Ω. Halving diameter raises bulk resistance to about 254.6 Ω and total to 274.6 Ω, not four times 83.7; interfaces are held constant in this simplified model.','分開主體 63.7 Ω 與總值 83.7 Ω，並說明介面固定假設。','Separate 63.7 Ω bulk from 83.7 Ω total and state the fixed-interface assumption.'),
'a062':(19,'假設線槽寬 40 nm、高 60 nm，兩側與底部各由 3 nm 非銅襯層占用，不計頂部帽層。銅截面為 (40-6)(60-3)=1938 nm²，而外部截面為 2400 nm²。若銅電阻率與長度固定，襯層占用使電阻相對理想全銅增加 2400/1938-1≈23.8%。這尚未計入尺寸散射與接觸電阻。','Assume a 40 nm wide, 60 nm tall trench with 3 nm non-copper liners on both sides and bottom, excluding a top cap. Copper area is (40-6)(60-3)=1938 nm² versus 2400 nm² external area. With fixed copper resistivity and length, liner occupancy raises resistance by 2400/1938-1≈23.8% over ideal all-copper. Size scattering and contact resistance are excluded.','交付 1938 nm² 與 23.8%，標出襯層位於兩側和底部。','Report 1938 nm² and 23.8%, marking liners on both sides and bottom.'),
'a063':(6,'以同一外框 20×30 nm² 比較假想材料。Cu 有兩側與底部 3 nm 襯層，導電面積 14×27=378 nm²，有效ρ=4 μΩ·cm；無襯層候選金屬面積600 nm²、有效ρ=6 μΩ·cm。相同線長下比較 ρ/A，比例為 (6/600)/(4/378)=0.945；較高ρ的候選反而低阻約5.5%。這不證明無襯層可靠，須另驗證擴散與附著。','Compare hypothetical materials in the same 20×30 nm² footprint. Cu has 3 nm side/bottom liners, conducting area 14×27=378 nm² and effective ρ=4 μΩ·cm. A linerless candidate has area 600 nm² and effective ρ=6 μΩ·cm. At equal length, resistance ratio is (6/600)/(4/378)=0.945: the higher-ρ candidate is about 5.5% lower in resistance. This does not prove linerless reliability; diffusion and adhesion need separate tests.','算出 0.945 並指出材料數字為假設、外框相同但有效截面不同。','Calculate 0.945 and state that values are hypothetical and footprints match while conducting areas differ.'),
'a064':(4,'假設幾何不變，介電常數從 4.0 降為 2.8，電容比 C₂/C₁=0.70。若電阻保持不變，RC 降低30%；但若新整合使電阻增加50%，RC 比值變為 1.5×0.70=1.05，反而增加5%。本例以集中參數 RC 說明取捨，不等於完整訊號時序模擬。','At fixed geometry, lowering permittivity from 4.0 to 2.8 gives capacitance ratio 0.70. With unchanged resistance, RC falls 30%; if the new integration raises resistance by 50%, RC ratio becomes 1.5×0.70=1.05, a 5% increase. This lumped-RC example illustrates tradeoffs rather than full timing simulation.','須同時給出 0.70 與 1.05，避免把低 k 等同更低延遲。','Report both 0.70 and 1.05 rather than equating lower k with lower delay.'),
'a065':(3,'假設矩形溝槽外框 20×40 nm²，襯層只占兩側與底部。厚度 2 nm 時導電截面為 16×38=608 nm²；厚度 3 nm 時為14×37=518 nm²。固定ρ與長度後，電阻比為608/518≈1.174，增加17.4%。但較薄層若有針孔，不能只憑低電阻選用；補上擴散可靠度關卡。','Assume a 20×40 nm² trench with liners on both sides and bottom. At 2 nm thickness, conducting area is 16×38=608 nm²; at 3 nm it is 14×37=518 nm². With fixed ρ and length, resistance ratio is 608/518≈1.174, a 17.4% increase. A thinner layer with pinholes cannot be selected on resistance alone; add diffusion-reliability gates.','交付 608、518 nm²與17.4%，且不得省略阻障完整性。','Report 608 and 518 nm² and 17.4%, retaining barrier-integrity requirements.'),
'a066':(2,'用純粹教學電荷帳本：Cu²⁺還原為 Cu，假設 Q=0.10 C，M=63.546 g/mol，F=96485 C/mol，z=2。理想質量 m=MQ/(zF)=32.93 μg；若電流效率90%，則為29.64 μg。這不包含任何鍍液組成或操作條件；需再用截面體積與銅密度檢查電荷、體積及損失是否一致。','For an educational charge ledger, reduce Cu²⁺ to Cu with Q=0.10 C, M=63.546 g/mol, F=96485 C/mol and z=2. Ideal mass m=MQ/(zF)=32.93 μg; at 90% current efficiency it is 29.64 μg. No bath composition or operating conditions are supplied. Check consistency against cross-sectional volume and copper density to account for charge, volume and losses.','交付 32.93 與29.64 μg，不能把電流效率假設成自動100%。','Report 32.93 and 29.64 μg without automatically assuming 100% efficiency.')
}
assert set(WORKED)==set(DATA)
for course in OUT['courses']:
 n,zz,ee,cz,ce=WORKED[course['id']]
 step=course['stages'][(n-1)//6]['steps'][(n-1)%6]
 step['instruction']+='\n\n具體演算（全部數據為教學假設）：'+zz
 step['instructionEn']+='\n\nWorked example (all values are teaching assumptions): '+ee
 step['observation']+='\n'+cz
 step['observationEn']+='\n'+ce
 step['check']+='\n本例驗收：'+cz
 step['checkEn']+='\nExample acceptance: '+ce
 step['knowledge'][1]['title']='具體案例、推導與適用限制'
 step['knowledge'][1]['titleEn']='Worked case, derivation and applicability'
 step['knowledge'][1]['text']=zz
 step['knowledge'][1]['textEn']=ee
 step['workedExample']={'hypothetical':True,'text':zz,'textEn':ee,'check':cz,'checkEn':ce}

# Fix incidental Simplified Chinese characters in the authored Traditional Chinese strings.
REPLACE={'独':'獨','来':'來','访':'訪','复':'複','总':'總','并':'並','最坏':'最壞','发':'發','镜':'鏡','厂':'廠','术':'術','时':'時','稳':'穩','过':'過','气':'氣','温':'溫','邻':'鄰','比较':'比較','画':'畫','构':'構','图':'圖','误':'誤','单':'單','实':'實','验':'驗','与':'與','应':'應','产':'產','还':'還','纯':'純','线':'線','两':'兩','处':'處','条':'條','离':'離','为':'為','历':'歷','页':'頁','转':'轉','预':'預','电':'電','体':'體','带':'帶','压':'壓','场':'場','层':'層','样':'樣','据':'據','数':'數','学':'學','观':'觀','测':'測','组':'組','杂':'雜','轴':'軸','显':'顯','态':'態','导':'導','种':'種','见':'見','过':'過','关':'關','侧':'側','间':'間','内':'內','网':'網','环':'環','变':'變','后':'後','开':'開','记':'記','无':'無','写':'寫','准':'準','传':'傳','减':'減','识':'識','链':'鏈','范':'範','够':'夠','装':'裝','别':'別','证':'證','统':'統','损':'損','动':'動','径':'徑','扩':'擴','仪':'儀','反应':'反應','条件':'條件'}
def clean(v):
 if isinstance(v,str):
  for a,b in REPLACE.items():v=v.replace(a,b)
  return v
 if isinstance(v,list):return [clean(x) for x in v]
 if isinstance(v,dict):return {k:clean(x) for k,x in v.items()}
 return v
OUT=clean(OUT)
# Schema/integrity checks: every authored course, step, source and comparison.
expected={f'a{i:03}' for i in range(34,67)}-{'a042'}
assert {c['id'] for c in OUT['courses']}==expected
sourceids={x['id'] for x in OUT['sources']}
stepids=[]; instructions=[]
for c in OUT['courses']:
 assert c['title']==CAT[c['id']]['title'] and c['titleEn']==CAT[c['id']]['titleEn']
 assert len(c['stages'])==4 and len(set(c['sourceIds']))>=2
 assert set(c['sourceIds'])<=sourceids
 answers=[]
 for st in c['stages']:
  assert len(st['steps'])==6
  for s in st['steps']:
   stepids.append(s['id']);instructions.append(s['instruction']);answers.append(s['quiz']['answer'])
   for f in ['title','objective','instruction','observation','failure','check']:
    assert s[f] and s[f+'En'],(c['id'],s['id'],f)
   assert len(s['knowledge'])==2
   assert all(k['text'] and k['textEn'] for k in s['knowledge'])
   assert len(set(s['quiz']['options']))==3
   assert set(s['sourceIds'])<=sourceids
 assert [answers.count(i) for i in range(3)]==[8,8,8]
assert len(stepids)==len(set(stepids))==768
assert len(instructions)==len(set(instructions))==768
assert len(OUT['places'])==32 and len(OUT['related'])==32
for r in OUT['related']:
 assert len(r['related'])==2
 for item in r['related']:
  assert item['id'] in CAT and len(item['practice'])==len(item['practiceEn'])==3
for p in OUT['places']:
 assert len(p['history'])==2
 assert all(x in p['place'] for x in ['name','nameEn','city','cityEn','country','countryEn','address','addressEn','lat','lng','coordinateScope','coordinateScopeEn'])
 assert -90<=p['place']['lat']<=90 and -180<=p['place']['lng']<=180
 assert set(p['sourceIds'])<=sourceids
out=ROOT/'tools/semiconductor-v8/group_b.json';out.write_text(json.dumps(OUT,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'courses':len(COURSES),'steps':len(stepids),'knowledge':len(stepids)*2,'sources':len(S),'places':len(PLACES),'related':sum(len(r['related']) for r in RELATED),'file':str(out)},ensure_ascii=False))
