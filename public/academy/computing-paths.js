const e=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
export const COMPUTING_FOCUS_IDS=['cybersecurity',...Array.from({length:99},(_,i)=>'a'+(302+i))];
export const COMPUTING_PATHS=[
 ['hardware',['處理器、GPU、TPU與信任鏈','Processors, GPUs, TPUs and trust chains'],['a302','a303','a304','a305','a306','a308','a310']],
 ['software',['作業系統到可信交付','Operating systems to trusted delivery'],['a311','a312','a313','a314','a315','a327','a328']],
 ['distributed',['儲存、共識與平台','Storage, consensus and platforms'],['a316','a317','a318','a319','a321','a325','a330']],
 ['network',['從網路到全球通訊','Networks to global communications'],['a331','a332','a334','a335','a339','a345','a346','a350']],
 ['identity',['零信任與密碼遷移','Zero trust and cryptographic migration'],['a351','a352','a353','a354','a355','a357','a358']],
 ['defense',['監測、事件應變與鑑識','Monitoring, incident response and forensics'],['cybersecurity','a360','a361','a362','a364','a368','a369','a370']],
 ['privacy',['隱私保護計算','Privacy-preserving computation'],['a371','a372','a373','a374','a375']],
 ['ai',['神經網路、RAG與推論','Neural networks, RAG and inference'],['a376','a377','a378','a379','a380','a381','a382','a384']],
 ['hpc',['科學運算與世界級超算','Scientific computing and landmark supercomputers'],['a388','a389','a390','a391','a392','a393','a395','a396']],
 ['internet',['網際網路的工程歷史','Engineering history of the Internet'],['a397','a398','a399','a400']]
];
export function computingPathsMarkup(catalog,zh=true){
 const by=new Map(catalog.map(c=>[c.id,c])),courses=COMPUTING_FOCUS_IDS.map(id=>by.get(id)).filter(c=>c?.stages?.length),total=courses.reduce((n,c)=>n+c.stepCount,0);if(courses.length!==100)return '';
 const pick=(z,en)=>zh?z:en;
 return `<section class="packaging-collection computing-collection" aria-labelledby="computingCollectionTitle"><div class="packaging-collection-head"><div><span class="eyebrow">COLLECTION 11 · COMPUTING × SECURITY</span><h2 id="computingCollectionTitle">${pick('資訊與資安：從架構理解到證據驗證。','Computing and security: architecture to verified evidence.')}</h2><p>${pick('100門逐步課程 · 13個專業子領域 · '+total.toLocaleString()+'個學習步驟','100 guided courses · 13 subdisciplines · '+total.toLocaleString()+' learning steps')}</p></div><a class="button" href="#learning-map">${pick('開啟課程地圖','Open learning map')} ↗</a></div><p>${pick('100張原創功能架構圖、16種本地算例；以合成資料與授權隔離環境學習。量子、AI加速器及能源巨作可從課程地圖繼續探索。','100 original architectures and 16 local calculators. Learn with synthetic data and authorized isolated environments. Continue into quantum, AI acceleration and energy landmarks from the learning map.')}</p><p><a href="data/information-security-100.csv" download>${pick('下載完整中英課程索引','Download bilingual course index')} ↓</a></p><details class="packaging-routes"><summary>${pick('展開10條資訊學習路線','Explore 10 computing learning paths')}</summary><div class="packaging-route-grid">${COMPUTING_PATHS.map(([id,title,ids])=>`<article><span class="task-label">${id.toUpperCase()}</span><h3>${e(title[zh?0:1])}</h3><ol>${ids.map(id=>by.get(id)).filter(Boolean).map(c=>`<li><a href="#project/${e(c.id)}">${e(zh?c.title:c.titleEn)}</a></li>`).join('')}</ol></article>`).join('')}</div></details></section>`;
}
