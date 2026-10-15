// V12 home collection: 101 optics & precision-instrument courses grouped by
// the learning-map subdivisions written by tools/integrate-optics-v12.py.
const e=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
export const OPTICS_ROUTES=[
 ['optics-lithography','LITHOGRAPHY'],['optics-design-fabrication','DESIGN · FAB'],['optics-coatings-elements','COATINGS'],
 ['optics-modulation-holography','HOLOGRAPHY'],['optics-microscopy','MICROSCOPY'],['optics-spectroscopy-radiometry','SPECTROSCOPY'],
 ['optics-precision-metrology','METROLOGY'],['optics-analytical-instruments','ANALYTICAL'],['optics-lab-infrastructure','CRYO · VACUUM'],
 ['optics-accelerators-detectors','DETECTORS'],['optics-astronomical','ASTRONOMY'],['optics-facilities-accelerators','LIGHT SOURCES'],
 ['optics-facilities-observatories','OBSERVATORIES']
];
export function opticsPathsMarkup(catalog,zh=true){
 const courses=catalog.filter(c=>c.learningTrack==='optics'&&(c.stages?.length||c.stepCount));
 if(courses.length<100)return '';
 const total=courses.reduce((n,c)=>n+(c.stepCount||0),0),pick=(z,en)=>zh?z:en;
 const groups=OPTICS_ROUTES.map(([id,label])=>{const list=courses.filter(c=>c.learningSubdiscipline===id);return {id,label,list,title:list[0]?pick(list[0].subcategoryTitle,list[0].subcategoryTitleEn):id}}).filter(g=>g.list.length);
 return `<section class="packaging-collection optics-collection" aria-labelledby="opticsCollectionTitle"><div class="packaging-collection-head"><div><span class="eyebrow">COLLECTION 12 · OPTICS × PRECISION INSTRUMENTS</span><h2 id="opticsCollectionTitle">${pick('光學與精密儀器：從原理、算例到驗證。','Optics and precision instruments: principles, calculations, verification.')}</h2><p>${pick(`${courses.length}門逐步課程 · ${groups.length}個專業子領域 · ${total.toLocaleString()}個學習步驟`,`${courses.length} guided courses · ${groups.length} subdisciplines · ${total.toLocaleString()} learning steps`)}</p></div><a class="button" href="#learning-map">${pick('開啟課程地圖','Open learning map')} ↗</a></div><p>${pick('每門課以機制、定量算例、量測驗證與失效診斷四個角度拆解：從 EUV 微影、干涉量測與電子顯微，到同步輻射光源、重力波與大型望遠鏡。每門第一節免費試學。','Each course works through mechanism, quantitative example, verification and failure diagnosis: from EUV lithography, interferometry and electron microscopy to synchrotron light sources, gravitational-wave detectors and large telescopes. The first section of every course is free.')}</p><p><a href="data/optics-precision-101.csv" download>${pick('下載完整中英課程索引','Download bilingual course index')} ↓</a></p><details class="packaging-routes"><summary>${pick(`展開${groups.length}個光學與儀器子領域`,`Explore ${groups.length} optics and instrument subdisciplines`)}</summary><div class="packaging-route-grid">${groups.map(g=>`<article><span class="task-label">${e(g.label)}</span><h3>${e(g.title)}</h3><ol>${g.list.map(c=>`<li><a href="#project/${e(c.id)}">${e(zh?c.title:c.titleEn)}</a></li>`).join('')}</ol></article>`).join('')}</div></details></section>`;
}
