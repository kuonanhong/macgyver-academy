
// V13 explorer collection: 100 bridges & buildings courses grouped by the
// learning-map subdivisions written by tools/integrate-structures-v13.py.
const e=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
export const STRUCTURES_ROUTES=[
 ['st-suspension','SUSPENSION'],['st-cable-stayed','CABLE-STAYED'],['st-arch-viaduct-sea','ARCH · SEA CROSSING'],
 ['st-bridge-construction','ERECTION'],['st-bridge-components-seismic','BEARINGS · SEISMIC'],['st-bridge-durability-monitoring','MONITORING'],
 ['st-supertall','SUPERTALL'],['st-tall-systems','TALL SYSTEMS'],['st-landmark-roofs','LONG-SPAN ROOFS'],
 ['st-concrete-steel','CONCRETE · STEEL'],['st-seismic-precast-fire','SEISMIC · FIRE'],['st-facade-digital','FACADE · DIGITAL']
];
export function structuresPathsMarkup(catalog,zh=true){
 const courses=catalog.filter(c=>c.learningTrack==='structures'&&(c.stages?.length||c.stepCount));
 if(courses.length<100)return '';
 const total=courses.reduce((n,c)=>n+(c.stepCount||0),0),pick=(z,en)=>zh?z:en;
 const groups=STRUCTURES_ROUTES.map(([id,label])=>{const list=courses.filter(c=>c.learningSubdiscipline===id);return {id,label,list,title:list[0]?pick(list[0].subcategoryTitle,list[0].subcategoryTitleEn):id}}).filter(g=>g.list.length);
 return `<section class="packaging-collection structures-collection" aria-labelledby="structuresCollectionTitle"><div class="packaging-collection-head"><div><span class="eyebrow">COLLECTION 13 · BRIDGES × BUILDINGS</span><h2 id="structuresCollectionTitle">${pick('橋樑與建築：從傳力路徑、施工到驗證。','Bridges and buildings: load paths, construction and verification.')}</h2><p>${pick(`${courses.length}門逐步課程 · ${groups.length}個專業子領域 · ${total.toLocaleString()}個學習步驟`,`${courses.length} guided courses · ${groups.length} subdisciplines · ${total.toLocaleString()} learning steps`)}</p></div><a class="button" href="#learning-map">${pick('開啟課程地圖','Open learning map')} ↗</a></div><p>${pick('每門課 5 個階段、40 步：荷載與結構系統、材料與接合、施工與階段控制、試驗與監測、耐久與交接；每一單元再拆成傳力機制、定量算例、試驗驗證與失效診斷。從明石海峽大橋、米約高架橋到台北 101、哈里發塔與雪梨歌劇院，並附關鍵數據、年代、規範與案例比較。每門第一節免費試學。','Each course has 5 stages and 40 steps: loads and structural system, materials and connections, construction and stage control, testing and monitoring, durability and handover; every unit is split into load path, calculation, verification and failure diagnosis. From the Akashi Kaikyō Bridge and Millau Viaduct to Taipei 101, Burj Khalifa and the Sydney Opera House, with key figures, timelines, codes and landmark comparisons. The first section of every course is free.')}</p><p><a href="data/bridges-buildings-100.csv" download>${pick('下載完整中英課程索引','Download bilingual course index')} ↓</a></p><details class="packaging-routes"><summary>${pick(`展開${groups.length}個橋樑與建築子領域`,`Explore ${groups.length} bridge and building subdisciplines`)}</summary><div class="packaging-route-grid">${groups.map(g=>`<article><span class="task-label">${e(g.label)}</span><h3>${e(g.title)}</h3><ol>${g.list.map(c=>`<li><a href="#project/${e(c.id)}">${e(zh?c.title:c.titleEn)}</a></li>`).join('')}</ol></article>`).join('')}</div></details></section>`;
}
