/* Original accessible engineering campus. No WebGL or network needed. */
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const COLORS=['#4bb4c4','#bba0ef','#7cc984','#f3b358','#dd8394','#8cb5ed','#c0d876','#e6aa78','#a797d4','#89cbc4'];
export function environmentPathsMarkup(catalog,zh=true){
 const groups=new Map();for(const c of catalog.filter(c=>c.category==='environment'&&c.stages)){const key=c.subcategory||'environment-water';if(!groups.has(key))groups.set(key,{title:zh?c.subcategoryTitle:c.subcategoryTitleEn,count:0});groups.get(key).count++;}
 return `<section class="environment-paths"><span class="eyebrow">V17 · ENVIRONMENT & CITIES</span><h2>${zh?'選一條環境工程學習路線':'Choose an environmental engineering path'}</h2><p>${zh?'每門課由機制、定量算例、操作驗證和故障診斷組成。先選子領域，再從一門課開始。':'Each course combines mechanisms, quantitative examples, operational verification and diagnosis. Pick a field and begin with one course.'}</p><div class="environment-path-grid">${[...groups].map(([id,g])=>`<button class="button light" data-environment-path="${esc(id)}"><strong>${esc(g.title||id)}</strong><small>${g.count} ${zh?'門逐步課程':'guided courses'} →</small></button>`).join('')}</div></section>`;
}
export function engineeringIslandMarkup(categories,{zh=true}={}){
 return `<section class="engineering-island" data-island-v17 data-time="day" aria-label="${zh?'工程群島互動地圖':'Interactive engineering campus'}"><header><div><span class="eyebrow">V17 · ENGINEERING CAMPUS</span><h1>${zh?'點一座實驗室，開始今天的工程':'Choose a laboratory. Begin today’s project.'}</h1><p>${zh?'先探索設備，再完成一個小任務。需要幫忙時，師傅可帶你完成當前步驟。':'Explore the equipment, then complete one small task. Your mentor can guide the current step.'}</p></div><div class="island-display"><button type="button" data-island-time="day" aria-pressed="true">☀ ${zh?'日景':'Day'}</button><button type="button" data-island-time="night" aria-pressed="false">☾ ${zh?'夜景':'Night'}</button><label><input type="checkbox" data-island-links> ${zh?'系統連結':'Connections'}</label></div></header><div class="island-layout"><div class="island-grid" role="group" aria-label="${zh?'20 個工程領域':'20 engineering domains'}">${categories.map((c,i)=>`<button type="button" class="island-tile" data-island-category="${esc(c.id)}" style="--tile:${COLORS[i%COLORS.length]};--delay:${i*30}ms" aria-pressed="false"><span class="island-tile-icon">${c.icon}</span><strong>${esc(c.name)}</strong><small>${c.guided} ${zh?'門逐步課':'guided courses'}</small></button>`).join('')}</div><aside class="island-detail"><span class="eyebrow">01 · CHOOSE</span><h3 data-island-title>${zh?'從環境與城市開始':'Start with environment and cities'}</h3><p data-island-summary>${zh?'選一個領域，查看可立即開始的任務。':'Choose a domain to see tasks you can start now.'}</p><div data-island-recommendations></div><div class="island-connection-note" hidden>${zh?'工程連結：水與能源支撐城市；材料與製程支撐設備；量測與資訊驗證效能。這是學習關係，不是設施管線圖。':'Learning connections: water and energy support cities; materials and processes support equipment; measurement and computing verify performance. This is not a site piping diagram.'}</div><a data-island-catalog class="button light" href="#catalog/domain/environment">${zh?'查看此領域全部課程':'All courses in this domain'} ↗</a></aside></div><ol class="island-onboarding"><li><b>01</b><span>${zh?'進入實景，點選設備':'Enter a scene and select equipment'}</span></li><li><b>02</b><span>${zh?'調整參數，看見變化':'Change a parameter and observe'}</span></li><li><b>03</b><span>${zh?'跟隨師傅，完成這一步':'Follow the mentor and complete one step'}</span></li></ol></section>`;
}
export function mountEngineeringIsland(root,categories,catalog,{zh=true}={}){
 if(!root)return;
 const choose=id=>{
   const c=categories.find(x=>x.id===id);if(!c)return;
   root.querySelectorAll('[data-island-category]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.islandCategory===id)));
   root.querySelector('[data-island-title]').textContent=c.name;
   root.querySelector('[data-island-summary]').textContent=zh?`${c.guided} 門逐步課程 · ${c.count} 個專題。可先進入免費實景與第一節。`:`${c.guided} guided courses · ${c.count} topics. Explore the scene and free first lesson.`;
   const preferred=id==='environment'?['b410','b457','b467']:[];
   const pool=catalog.filter(x=>x.category===id&&x.stages);
   const picks=[...preferred.map(p=>pool.find(c=>c.id===p)).filter(Boolean),...pool].filter((c,i,a)=>a.findIndex(x=>x.id===c.id)===i).slice(0,3);
   root.querySelector('[data-island-recommendations]').innerHTML=picks.map(c=>`<a class="island-mission" href="#scene/${esc(c.id)}"><span>${esc(zh?c.title:c.titleEn||c.title)}</span><small>${zh?'探索現場':'Explore scene'} →</small></a>`).join('')||`<a href="#catalog/domain/${esc(id)}">${zh?'探索研究題目':'Explore research topics'} →</a>`;
   root.querySelector('[data-island-catalog]').href='#catalog/domain/'+id;
 };
 root.querySelectorAll('[data-island-category]').forEach(b=>b.onclick=()=>choose(b.dataset.islandCategory));
 root.querySelectorAll('[data-island-time]').forEach(b=>b.onclick=()=>{root.dataset.time=b.dataset.islandTime;root.querySelectorAll('[data-island-time]').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));});
 root.querySelector('[data-island-links]').onchange=e=>{root.classList.toggle('show-links',e.target.checked);root.querySelector('.island-connection-note').hidden=!e.target.checked;};
 choose('environment');
}
