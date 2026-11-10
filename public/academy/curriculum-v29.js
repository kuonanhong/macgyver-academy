/* Course register only; full lessons use the existing integrity-checked loader. */
(function(){'use strict';
 const $=id=>document.getElementById(id),meta=window.MG_SOFTWARE_V29;
 if(!meta||!Array.isArray(meta.courses)||meta.courses.length!==210){$('result-count').textContent='課程目錄未完整載入，請重新整理。Course index failed to load; reload this page.';return;}
 const COURSES=meta.courses,GROUPS=meta.groups;
 const COPY={
 map:['課程地圖','Learning map'],lab:['進入軟體系統實驗室 ↗','Enter the software systems lab ↗'],
 heading:['從一行程式，\n走進軟體系統的內部。','Start with a line of code.\nExplore the systems beneath it.'],
 intro:['走進 UNIX、編譯器、資料庫、瀏覽器與可信交付。用可重算的模型、可辨識的故障與具體證據，完成每一次工程判斷。','Explore UNIX, compilers, databases, browsers and trustworthy delivery. Build engineering judgment through reproducible models, distinguishable faults and concrete evidence.'],
 browse:['探索 210 門課程 ↓','Explore 210 courses ↓'],walk:['走進全螢幕實驗室 ↗','Walk into the full-screen lab ↗'],plate:['原創軟體資料流示意','Original software dataflow'],
 courses:['新增逐步課程','new guided courses'],steps:['新增學習步驟','new learning steps'],groups:['專題學習分組','topic groups'],perCourse:['每門詳細步驟','steps in each course'],
 method:['每一步，都留下可查核的答案。','Make every step verifiable.'],
 preserved:['保留原有 2,499 門逐步課程與 92,674 步。新課含繁體中文與英文全文、來源、算例、五項探究與驗收紀錄。','All 2,499 earlier guided courses and 92,674 steps are retained. New courses include full Traditional Chinese and English text, references, worked examples, five investigations and acceptance evidence.'],
 register:['選擇你的下一條學習路線。','Choose your next learning route.'],allAcademy:['所有學院課程 ↗','All academy courses ↗'],all:['全部 210 門','All 210 courses'],
 systems:['系統與程式原理 70','Systems & programming · 70'],data:['資料與分散式系統 70','Data & distributed systems · 70'],delivery:['Web、工程與交付 70','Web, engineering & delivery · 70'],
 search:['搜尋課程','Search courses'],groupFilter:['專題分組','Topic group'],reset:['重設','Reset'],ordered:['依學習分組與課序排列','Ordered by group and course sequence'],empty:['沒有符合的課程。試試較短關鍵字或重設篩選。','No matching courses. Try shorter keywords or reset the filters.'],
 closing:['把計算帶到工作台。','Take the calculation to the bench.'],closingText:['行走到六個軟體工程工作站，調整參數、比較預測與結果，記錄你的工程判讀。','Walk to six software engineering workstations, adjust parameters, compare predictions with results and document your engineering decisions.'],
 scope:['課內數值是明示的教學假設。官方來源支持具名系統與原理，並不代表實機量測、產品規格或已完成正式設計。','Numerical inputs are stated teaching assumptions. Official references support the named systems and principles; exercises are not live measurements, product specifications or certified designs.'],
 access:['公開網站保留第一階段預覽；完整套件包含所有課文。其他語言全文需要可用的瀏覽器或已設定的翻譯服務。','The public website retains first-stage previews; the complete package contains all lessons. Full text in other languages requires an available browser or configured translation service.']
 };
 const PHASES=[
 [['證據與介面','Evidence & interfaces'],['定義系統邊界、資料來源與可驗證目標。','Define system boundaries, evidence and verifiable goals.']],
 [['模型與計算','Model & calculate'],['從輸入、單位與假設，推導可重算的結果。','Derive reproducible results from inputs, units and assumptions.']],
 [['變更與驗證','Change & verify'],['只改一項條件，比較預測與獨立計算。','Change one condition and compare predictions with an independent check.']],
 [['故障與判讀','Diagnose & distinguish'],['用不同觀察，分辨看似相同的故障。','Use discriminating observations to separate similar failure symptoms.']],
 [['驗收與交接','Accept & hand over'],['交付原始資料、判據、限制與重驗紀錄。','Deliver raw data, criteria, limits and retest records.']]
 ];
 const node=(tag,cls,text)=>{const e=document.createElement(tag);if(cls)e.className=cls;if(text!==undefined)e.textContent=text;return e;};
 let lang='zh-TW',track='all',group='',query='',ui;
 function get(key){try{return localStorage.getItem(key)}catch{return null}}
 function set(key,value){try{localStorage.setItem(key,value)}catch{}}
 const tx=pair=>pair[lang==='zh-TW'?0:1];
 function state(){const p=new URLSearchParams(location.hash.slice(1));track=['systems','data','delivery'].includes(p.get('track'))?p.get('track'):'all';group=/^(?:[1-9]|1[0-9]|2[01])$/.test(p.get('group')||'')?p.get('group'):'';query=(p.get('q')||'').slice(0,200);if(group&&track!=='all'&&family(Number(group))!==track)group='';}
 function family(g){return g<=7?'systems':g<=14?'data':'delivery'}
 function persist(){const p=new URLSearchParams();if(track!=='all')p.set('track',track);if(group)p.set('group',group);if(query)p.set('q',query);p.set('lang',ui.preference);try{history.replaceState(null,'',location.pathname+location.search+'#'+p)}catch{}}
 function groupOptions(){const select=$('group');select.replaceChildren();const first=node('option','',lang==='zh-TW'?'所有專題分組':'All topic groups');first.value='';select.append(first);GROUPS.forEach((p,i)=>{if(track!=='all'&&family(i+1)!==track)return;const option=node('option','',String(i+1).padStart(2,'0')+' · '+tx(p));option.value=String(i+1);select.append(option)});select.value=group;}
 function render(){if(!ui)return;ui.invalidate();const words=query.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);const selected=COURSES.filter(c=>(track==='all'||family(c.group)===track)&&(!group||c.group===Number(group))&&words.every(w=>[c.id,...c.title,...GROUPS[c.group-1]].join(' ').toLocaleLowerCase().includes(w)));const root=$('course-groups');root.replaceChildren();
  for(let g=1;g<=21;g++){const rows=selected.filter(c=>c.group===g);if(!rows.length)continue;const section=node('section','course-group'),heading=node('div','group-heading'),label=node('div');label.append(node('p','',String(g).padStart(2,'0')+' / '+tx(COPY[family(g)])),node('h3','',tx(GROUPS[g-1])));heading.append(label,node('span','group-count',rows.length+(lang==='zh-TW'?' 門課':' courses')));section.append(heading);const grid=node('div','course-grid');
   for(const c of rows){const link=node('a','course-card');link.href='index.html#project/'+c.id;link.dataset.courseId=c.id;const m=node('div','course-meta');m.append(node('b','',String(c.position).padStart(3,'0')),node('span','',c.id.toUpperCase()));const other=node('p','course-secondary',c.title[lang==='zh-TW'?1:0]);other.setAttribute('data-no-translate','');other.lang=lang==='zh-TW'?'en':'zh-TW';const foot=node('div','course-foot');foot.append(node('span','',lang==='zh-TW'?'40 步 · 10 單元 · 五項探究':'40 steps · 10 units · 5 investigations'),node('span','course-arrow','↗'));link.append(m,node('h4','',tx(c.title)),other,foot);grid.append(link)}section.append(grid);root.append(section);}
  $('empty').hidden=selected.length>0;$('result-count').textContent=lang==='zh-TW'?`顯示 ${selected.length} / 210 門課程`:`Showing ${selected.length} of 210 courses`;document.querySelectorAll('[data-track]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.track===track)));void ui.apply(document.body);
 }
 function translate(){if(!ui)return;lang=ui.language;document.documentElement.lang=lang;document.title=lang==='zh-TW'?'資訊系統與軟體基礎 · 210 門逐步課程 · 馬蓋先':'Systems & Software · 210 Courses · MacGyver';document.querySelectorAll('[data-copy]').forEach(e=>{if(COPY[e.dataset.copy])e.textContent=tx(COPY[e.dataset.copy])});$('query').placeholder=lang==='zh-TW'?'UNIX、SQLite、Git、LLVM、Kubernetes…':'UNIX, SQLite, Git, LLVM, Kubernetes…';$('query').value=query;$('language').value=ui.preference;const list=$('method-steps');list.replaceChildren();PHASES.forEach((p,i)=>{const li=node('li');li.append(node('span','',String(i+1).padStart(2,'0')),node('strong','',tx(p[0])),node('p','',tx(p[1])));list.append(li)});const c=COURSES.find(c=>c.id===get('mg-v29-last-course'));$('resume').hidden=!c;if(c){$('resume').href='index.html#project/'+c.id;$('resume').textContent=(lang==='zh-TW'?'繼續上次課程：':'Last opened: ')+tx(c.title)+' ↗'}groupOptions();render();}
 state();ui=window.MG_CURRICULUM_LOCALE_V29.create({select:$('language'),status:$('translation-status'),cloudButton:$('translation-cloud'),deviceButton:$('translation-device'),urlPreference:new URLSearchParams(location.hash.slice(1)).get('lang')||new URLSearchParams(location.search).get('lang'),onChange:s=>{lang=s.language;translate();persist()}});translate();
 $('filters').addEventListener('submit',e=>e.preventDefault());$('query').addEventListener('input',e=>{query=e.target.value;render();persist()});$('group').addEventListener('change',e=>{group=e.target.value;render();persist()});$('reset').addEventListener('click',()=>{track='all';group='';query='';$('query').value='';groupOptions();render();persist()});document.querySelectorAll('[data-track]').forEach(b=>b.addEventListener('click',()=>{track=b.dataset.track;group='';groupOptions();render();persist()}));$('course-groups').addEventListener('click',e=>{const link=e.target.closest('[data-course-id]');if(link)set('mg-v29-last-course',link.dataset.courseId)});window.addEventListener('hashchange',()=>{if(location.hash.includes('=')){state();ui.readUrl(new URLSearchParams(location.hash.slice(1)).get('lang'));translate()}});
})();
