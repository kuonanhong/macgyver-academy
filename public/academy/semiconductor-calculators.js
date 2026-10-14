/* Transparent, dimensioned educational models. All input defaults are invented
   specimens; none are qualified operating settings or acceptance specifications. */
export const SEMICONDUCTOR_LABS = {
  ald:{title:['ALD 循環與膜厚','ALD cycles and thickness'],formula:'t = N × g',unit:'nm',params:[['cycles',['循環數 N','Cycles N'],0,500,1,100,''],['growth',['假設每循環增厚 g','Assumed growth per cycle g'],.01,.3,.01,.1,'nm/cycle']],note:['穩態每循環增厚的線性算例；忽略成核延遲、反應未飽和及深孔傳輸。單一線性曲線不能證明自限反應。','Linear steady-growth example; nucleation delay, incomplete saturation and deep-feature transport are excluded. A linear curve alone does not prove self-limiting chemistry.'],question:['若前 20 個循環沒有成核，原模型如何修正？增加循環能否消除底部供應不足？','How would 20 inactive nucleation cycles alter this model? Can extra cycles eliminate deficient delivery at the bottom?'],source:'https://plasma.oxinst.com/technologies/atomic-layer-deposition'},
  selectivity:{title:['蝕刻選擇比','Etch selectivity'],formula:'S = r_target / r_mask',unit:'',params:[['target',['目標膜假設速率','Assumed target-film rate'],1,100,1,40,'nm/min'],['mask',['遮罩假設速率','Assumed mask rate'],.1,20,.1,2,'nm/min']],note:['僅為同一條件下兩個量測速率的比；忽略圖形負載、深度效應、側壁損傷及時間漂移。高選擇比不自動等於正確輪廓。','Ratio of two measured rates under matching conditions; loading, depth effects, sidewall damage and drift are excluded. High selectivity does not guarantee the intended profile.'],question:['目標膜速率不變，遮罩消耗加倍後選擇比如何變化？還需什麼截面證據？','At fixed target rate, what does doubling mask loss do to selectivity? Which cross-sectional evidence is still needed?'],source:'https://plasma.oxinst.com/technologies/atomic-layer-etching'},
  aspect:{title:['孔洞深寬比','Feature aspect ratio'],formula:'AR = h / w',unit:'',params:[['height',['深度 h','Depth h'],20,2000,10,600,'nm'],['width',['開口寬 w','Opening width w'],10,500,10,100,'nm']],note:['幾何比值不預測蝕刻速率或填孔成功；底部寬度、側壁傾斜與反應物傳輸需另外量測。','A geometric ratio predicts neither etch rate nor fill success. Bottom width, taper and reactant transport require separate measurements.'],question:['相同深度，開口減半會怎樣？為何同樣深寬比仍可能有不同傳輸限制？','What happens when the opening halves at fixed depth? Why can equal aspect ratios have different transport limits?'],source:''},
  diffusion:{title:['一維擴散長度','One-dimensional diffusion length'],formula:'σ = √(2Dt)',unit:'nm',params:[['diffusivity',['假設常數 D','Assumed constant D'],.1,100,.1,2,'nm²/s'],['time',['時間 t','Time t'],1,1000,1,100,'s']],note:['無限介質、常數擴散係數下高斯分布的標準差；不是有限晶圓的接面深度。忽略濃度相依性、邊界及熱歷程。','Gaussian standard deviation in an infinite medium with constant diffusivity; not junction depth in a finite wafer. Concentration dependence, boundaries and thermal histories are excluded.'],question:['時間增為四倍，標準差為何只增為兩倍？D 隨溫度變化時應積分什麼？','Why does quadrupling time only double the standard deviation? What must be integrated if diffusivity changes with temperature?'],source:'https://ocw.mit.edu/courses/6-774-physics-of-microfabrication-front-end-processing-fall-2004/'},
  capacitance:{title:['理想平行板電容','Ideal parallel-plate capacitance'],formula:'C = ε₀ εr A / t',unit:'fF',params:[['area',['面積 A','Area A'],.1,100,.1,10,'µm²'],['relative',['相對介電常數 εr','Relative permittivity εr'],1,30,.1,4,''],['thickness',['厚度 t','Thickness t'],1,100,1,10,'nm']],note:['理想線性介電質、均勻平行板；不含邊緣場、漏電、介面陷阱與量子電容，不代表 DRAM 或 MOS 的完整模型。','Uniform plates and a linear dielectric; fringing, leakage, interface traps and quantum capacitance are excluded. This is not a complete DRAM or MOS model.'],question:['膜厚減半可使電容加倍，但為何還需要漏電與可靠度測試？','Halving thickness doubles capacitance here. Why are leakage and reliability tests still needed?'],source:''},
  capability:{title:['偏心與製程能力 Cpk','Off-centering and process capability'],formula:'Cpk = min(20 − μ, μ − 10) / (3σ)',unit:'',params:[['mean',['平均 μ（示例界限 10–20）','Mean μ (example limits 10–20)'],10,20,.1,15,'a.u.'],['sigma',['標準差 σ','Standard deviation σ'],.1,5,.1,1,'a.u.']],note:['假設穩定、近似常態、獨立的母體，示例規格界限固定為 10 和 20。規格界限不是管制界限；小樣本估計需信賴區間。','Assumes a stable, approximately normal, independent population, with illustrative specification limits 10 and 20. Specification limits are not control limits; small-sample estimates need confidence intervals.'],question:['標準差不變，平均偏向上限時 Cpk 如何變化？控制圖不穩定時為何不能直接宣稱能力？','At fixed standard deviation, how does moving the mean toward the upper limit change Cpk? Why does an unstable chart invalidate a simple capability claim?'],source:'https://itl.nist.gov/div898/handbook/pmc/section1/pmc16.htm'},
  shot:{title:['光子數與相對散粒雜訊','Photon count and relative shot noise'],formula:'σN / N = 1 / √N',unit:'%',params:[['photons',['平均偵測光子數 N','Mean detected photons N'],1,10000,1,100,'photons']],note:['獨立 Poisson 偵測計數；不含讀出雜訊、暗計數、增益波動與光阻化學隨機性。偵測光子數不等於入射光子數。','Independent Poisson detected counts; readout noise, dark counts, gain variation and resist chemistry are excluded. Detected counts differ from incident counts.'],question:['要把相對雜訊減半，需要幾倍光子？為何不能直接推論光阻缺陷減半？','How many times more photons halve relative noise? Why does that not imply halving resist defects?'],source:'https://camera.hamamatsu.com/us/en/learn/camera_glossary/p.html'},
  tlm:{title:['TLM 接觸與片電阻','TLM contact and sheet resistance'],formula:'Rtotal = 2Rc + Rsh L/W',unit:'Ω',params:[['length',['接觸間距 L','Contact spacing L'],1,100,1,20,'µm'],['width',['寬度 W','Width W'],1,100,1,10,'µm'],['sheet',['片電阻 Rsh','Sheet resistance Rsh'],1,100,1,10,'Ω/□'],['contact',['每端接觸電阻 Rc','Per-contact resistance Rc'],0,100,1,5,'Ω']],note:['相同接觸、均勻薄膜的一維線性模型；忽略電流擁擠、有限接觸長度與非歐姆行為。截距的一半是此模型 Rc，不直接等於比接觸電阻率。','One-dimensional model with identical contacts and a uniform film; current crowding, finite contact length and non-ohmic effects are excluded. Half the intercept gives model Rc, not specific contact resistivity.'],question:['比較不同間距時，斜率與截距各反映什麼？若 I–V 非線性，這種擬合還適用嗎？','What do slope and intercept encode across spacings? Is the fit still valid for nonlinear current-voltage behavior?'],source:''}
};
export function semiconductorLabKind(course,step){
  if(course.category!=='semiconductor'||!/^a\d{3}$/.test(course.id))return '';
  const n=Number(course.id.slice(1)),text=(step.titleEn||'').toLowerCase();
  if([12,57,58,59].includes(n))return /conform|coverage/.test(text)?'coverage':'ald';
  if([14,15,16,17,19].includes(n))return 'diffusion';
  if([29,30,61,63,65].includes(n))return 'tlm';
  if([34,41,50,78,79,80].includes(n))return 'shot';
  if([53,54,72].includes(n))return 'aspect';
  if(n>=51&&n<=56)return 'selectivity';
  if([11,64,70,71,73,77].includes(n))return 'capacitance';
  if([94,95,96,97].includes(n))return 'capability';
  return '';
}
export function calculateSemiconductorLab(kind,v){
  if(kind==='ald')return v.cycles*v.growth;
  if(kind==='selectivity')return v.target/v.mask;
  if(kind==='aspect')return v.height/v.width;
  if(kind==='diffusion')return Math.sqrt(2*v.diffusivity*v.time);
  if(kind==='capacitance')return 8.8541878128*v.relative*v.area/v.thickness;
  if(kind==='capability')return Math.min(20-v.mean,v.mean-10)/(3*v.sigma);
  if(kind==='shot')return 100/Math.sqrt(v.photons);
  if(kind==='tlm')return 2*v.contact+v.sheet*v.length/v.width;
  return null;
}
