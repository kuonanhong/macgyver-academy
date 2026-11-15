/* One persistent, grouped navigation tree; existing app event handlers stay on links. */
(()=>{'use strict';
 const nav=document.getElementById('nav'),side=document.getElementById('sidebar');if(!nav||!side)return;
 const isZh=()=>/^zh/i.test(document.documentElement.lang||navigator.language);
 const words={
 zh:['學習路線','工程現場','課程專輯','更多工具','逐步課程','收合選單'],en:['LEARNING','FIELD LAB','Course collections','More tools','Guided courses','Close menu'],
 ja:['学習','エンジニアリング現場','講座コレクション','その他のツール','ステップ別講座','メニューを閉じる'],ko:['학습','공학 현장','강좌 모음','추가 도구','단계별 강좌','메뉴 닫기'],
 es:['APRENDIZAJE','LABORATORIO','Colecciones de cursos','Más herramientas','Cursos guiados','Cerrar menú'],fr:['APPRENTISSAGE','LABORATOIRE','Collections de cours','Autres outils','Cours guidés','Fermer le menu'],
 de:['LERNEN','LABOR','Kurssammlungen','Weitere Werkzeuge','Schrittweise Kurse','Menü schließen'],pt:['APRENDIZAGEM','LABORATÓRIO','Coleções de cursos','Mais ferramentas','Cursos guiados','Fechar menu'],
 ru:['ОБУЧЕНИЕ','ЛАБОРАТОРИЯ','Подборки курсов','Другие инструменты','Пошаговые курсы','Закрыть меню'],ar:['التعلم','المختبر الهندسي','مجموعات الدورات','أدوات إضافية','دورات خطوة بخطوة','إغلاق القائمة'],
 hi:['अध्ययन','इंजीनियरिंग प्रयोगशाला','पाठ्यक्रम संग्रह','अन्य उपकरण','चरणबद्ध पाठ्यक्रम','मेनू बंद करें'],id:['BELAJAR','LABORATORIUM','Koleksi kursus','Alat lainnya','Kursus bertahap','Tutup menu'],
 vi:['HỌC TẬP','PHÒNG THÍ NGHIỆM','Bộ khóa học','Công cụ khác','Khóa học từng bước','Đóng trình đơn']};
 const t=i=>(words[(document.documentElement.lang||'en').split('-')[0]]||words.en)[i];
 function compact(a){const b=a.querySelector('b');if(!b||b.dataset.t)return;if(b.querySelector('br')){const parts=b.innerHTML.split(/<br\s*\/?\s*>/i).map(x=>{const n=document.createElement('span');n.innerHTML=x;return n.textContent.trim();});b.dataset.navZh=parts[0];b.dataset.navEn=parts.slice(1).join(' ');}if(b.dataset.navZh)b.textContent=isZh()?b.dataset.navZh:b.dataset.navEn||b.dataset.navZh;}
 nav.classList.add('nav-v32');
 const main=document.createElement('div'),field=document.createElement('div'),collections=document.createElement('details'),more=document.createElement('details');
 main.className=field.className='nav-v32-group';collections.className=more.className='nav-v32-fold';collections.id='nav-v32-collections';more.id='nav-v32-tools';
 const label1=document.createElement('p'),label2=document.createElement('p'),sum1=document.createElement('summary'),sum2=document.createElement('summary');
 label1.className=label2.className='nav-v32-label';main.append(label1);field.append(label2);collections.append(sum1);more.append(sum2);
 const ready=document.createElement('a');ready.href='#catalog/ready';ready.className='nav-v32-ready';ready.innerHTML='<span aria-hidden="true">▤</span><b></b>';main.append(ready);
 let busy=false;
 function organize(){if(busy)return;busy=true;
  const links=[...nav.querySelectorAll('a')].filter(a=>a!==ready);const seen=new Set();
  for(const a of links){const href=a.getAttribute('href')||'';if(seen.has(href)){a.remove();continue;}seen.add(href);
   let target=/^curriculum-/.test(href)?collections:/^(realworld-|experience\.html)/.test(href)?field:['#home','#learning-map','#workshop','#progress'].includes(href)?main:more;
   if(a.parentElement!==target)target.append(a);
   compact(a);if(/^curriculum-/.test(href))a.classList.remove('campaign-nav-v20');
  }
  for(const group of [main,field,collections,more])if(group.parentElement!==nav)nav.append(group);
  label1.textContent=t(0);label2.textContent=t(1);sum1.textContent=t(2);sum2.textContent=t(3);ready.querySelector('b').textContent=t(4);
  const active=[...nav.querySelectorAll('a')].find(a=>a.getAttribute('href')===location.hash);if(active?.closest('details'))active.closest('details').open=true;
  ready.classList.toggle('active',location.hash.startsWith('#catalog'));busy=false;
 }
 const close=document.createElement('button');close.type='button';close.className='nav-v32-close';close.textContent='×';close.setAttribute('aria-label',t(5));side.prepend(close);close.onclick=()=>{side.classList.remove('open');document.getElementById('menu')?.focus();};
 const shade=document.createElement('button');shade.type='button';shade.className='nav-v32-shade';shade.tabIndex=-1;shade.setAttribute('aria-label',t(5));side.after(shade);shade.onclick=close.onclick;
 nav.addEventListener('click',e=>{if(e.target.closest('a')&&matchMedia('(max-width:700px)').matches)side.classList.remove('open');});
 addEventListener('keydown',e=>{if(e.key==='Escape'&&side.classList.contains('open'))close.click();});
 addEventListener('hashchange',organize);
 // Later bundles may add course shortcuts. Move only new root links, preserving listeners.
 new MutationObserver(list=>{if(list.some(m=>[...m.addedNodes].some(n=>n.nodeType===1&&n.tagName==='A'&&n.parentElement===nav)))organize();}).observe(nav,{childList:true});
 new MutationObserver(()=>{organize();close.setAttribute('aria-label',t(5));shade.setAttribute('aria-label',t(5));}).observe(document.documentElement,{attributes:true,attributeFilter:['lang']});
 organize();
})();
