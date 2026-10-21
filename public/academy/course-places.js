/* Public engineering geography. Loading a map is always an explicit action. */
let places = new Map();
let pending = null, initialized=false;
const escape = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const field = (value, key, zh) => value?.[zh ? key : `${key}En`] || value?.[key] || '';
const array = value => Array.isArray(value) ? value : [];
function https(value) { try { const u = new URL(value); return u.protocol === 'https:' && !u.username && !u.password ? u.href : ''; } catch { return ''; } }
export function setCoursePlaces(data) {
  initialized=true;
  places = new Map(array(data?.courses).filter(c => typeof c?.courseId === 'string' && c.place && Number.isFinite(c.place.lat) && Math.abs(c.place.lat)<=90 && Number.isFinite(c.place.lng) && Math.abs(c.place.lng)<=180).map(c => [c.courseId,c]));
}
export function placeForCourse(id) { return places.get(id) || null; }
export function googlePlaceUrls(place, language='en', apiKey='') {
  if(!Number.isFinite(place?.lat)||Math.abs(place.lat)>90||!Number.isFinite(place?.lng)||Math.abs(place.lng)>180)throw new TypeError('A valid representative map coordinate is required');
  // Pin the reviewed coordinate; free-text names can resolve to a different site.
  const query = `${place.lat},${place.lng}`;
  const link = new URL('https://www.google.com/maps/search/');
  link.searchParams.set('api','1'); link.searchParams.set('query',query);
  const embed = new URL(apiKey ? 'https://www.google.com/maps/embed/v1/place' : 'https://maps.google.com/maps');
  if(apiKey) embed.searchParams.set('key',apiKey);
  else {embed.searchParams.set('output','embed');embed.searchParams.set('z','12');}
  embed.searchParams.set('q',query);
  embed.searchParams.set(apiKey?'language':'hl',/^[a-z]{2,3}(?:-[a-z0-9]{2,8})*$/i.test(language)?language:'en');
  return {link:link.href,embed:embed.href};
}
/** Plain geographic details and an external map link; rendering makes no request. */
export function placeLocationMarkup(place,{zh=true,language='en',includeName=true,includeLink=true}={}) {
  if(!Number.isFinite(place?.lat)||Math.abs(place.lat)>90||!Number.isFinite(place?.lng)||Math.abs(place.lng)>180)return `<p class="subtext">${zh?'尚未核實專屬地點，暫不提供定位。':'A dedicated location has not been verified; no map pin is supplied.'}</p>`;
  const address=field(place,'address',zh)||place.mapQuery||[field(place,'city',zh),field(place,'country',zh)].filter(Boolean).join(', ');
  const coordinates=`${place.lat}, ${place.lng}`,url=googlePlaceUrls(place,language).link;
  return `<div class="place-location-details">${includeName?`<strong>${escape(field(place,'name',zh))}</strong>`:''}<p><span>${zh?'地址／地理位置':'Address / geographical location'}</span><br>${escape(address)}</p><p><span>${zh?'代表座標（約，緯度／經度）':'Approximate reference coordinate (latitude / longitude)'}</span><br><bdi>${escape(coordinates)}</bdi></p>${includeLink?`<a class="text-link" href="${escape(url)}" target="_blank" rel="noopener">${zh?'開啟此座標的 Google 地圖':'Open this coordinate in Google Maps'} ↗</a>`:''}<small>${escape(field(place,'coordinateScope',zh)||(zh?'代表定位點，可能是工程、園區、博物館、入口或城市；並非整體工程邊界或參訪許可。':'A representative project, campus, museum, entrance or city point; not the full project boundary or permission to visit.'))}</small></div>`;
}
function entryMarkup(entry, zh, compact, language) {
  const p = entry.place, urls = googlePlaceUrls(p,language), summary = field(entry,'summary',zh);
  const teaser = compact && summary.length>(zh?100:220) ? summary.slice(0,zh?100:220)+'…' : summary;
  const history = `${compact?`<p class="place-full-story">${escape(summary)}</p>`:''}<ol class="place-timeline">${array(entry.history).map(h=>`<li><span>${escape(h.year)}</span><div><h4>${escape(field(h,'title',zh))}</h4><p>${escape(field(h,'text',zh))}</p></div></li>`).join('')}</ol><p class="place-connection"><strong>${zh?'帶回工作台的問題':'Bring this question to your workbench'}</strong><br>${escape(field(entry,'connection',zh))}</p><details class="place-references"><summary>${zh?'歷史與地點的資料來源':'Sources for the history and location'}</summary><ul>${array(entry.references).filter(r=>https(r.url)).map(r=>`<li><a href="${escape(https(r.url))}" target="_blank" rel="noopener">${escape(field(r,'title',zh))} ↗</a><small>${escape(r.publisher)}</small></li>`).join('')}</ul></details>`;
  return `<div class="place-heading"><span class="task-label">PLACE · HISTORY · ENGINEERING</span><h3>${zh?'工程在哪裡？它的故事是什麼？':'Where does this engineering happen?'}</h3></div><div class="place-overview"><div><h4>◎ ${escape(field(p,'name',zh))}</h4><p class="subtext">${escape(field(p,'city',zh))} · ${escape(field(p,'country',zh))}</p><p class="place-summary">${escape(teaser)}</p></div><div class="place-map-actions">${placeLocationMarkup(p,{zh,language,includeName:false,includeLink:false})}<button type="button" class="button light" data-load-course-map>${zh?'在此載入 Google 地圖':'Load Google Maps here'}</button><a href="${escape(urls.link)}" target="_blank" rel="noopener">${zh?'在 Google 地圖開啟':'Open in Google Maps'} ↗</a><small>${zh?'點擊載入會連線 Google，不需取得您的位置。':'Loading connects to Google; your location is not requested.'}</small></div></div><div class="course-map-host" data-course-map-host></div>${compact?`<details class="place-story"><summary>${zh?'展開工程歷史、故事與學習連結':'Explore the history, story and learning connections'}</summary>${history}</details>`:history}`;
}
export function coursePlacesMarkup(course,{zh=true,compact=false}={}) {
  if(!course?.stages) return '';
  const id=String(course.id||'');
  return `<section class="course-place task-card${compact?' compact':''}" data-course-place="${escape(id)}" data-place-compact="${compact}"><h3>${zh?'工程地點與歷史故事':'Engineering places and stories'}</h3><p role="status">${zh?'正在載入本工程的地點與故事…':'Loading this project’s location and history…'}</p></section>`;
}
async function loadPlaces() {
  if(initialized) return;
  if(globalThis.window?.MG_DATA?.['course-places']) {setCoursePlaces(window.MG_DATA['course-places']);return;}
  if(!pending) pending=(async()=>{const controller=new AbortController();const timer=setTimeout(()=>controller.abort(),6000);try{const response=await fetch('data/course-places.json',{signal:controller.signal});if(!response.ok)throw new Error('Places unavailable');setCoursePlaces(await response.json());}finally{clearTimeout(timer);}})().finally(()=>{pending=null;});
  await pending;
}
export async function bindCoursePlaces({zh=true,language='en',onRendered=()=>{}}={}) {
  const roots=[...document.querySelectorAll('[data-course-place]')]; if(!roots.length)return;
  try {await loadPlaces();} catch {for(const root of roots)if(root.isConnected)root.innerHTML=`<h3>${zh?'工程地點與故事':'Engineering places and stories'}</h3><p>${zh?'地點資料尚未載入；請重新開啟完整套件。':'Location data could not load. Reopen the complete package.'}</p>`;return;}
  for(const root of roots) {
    if(!root.isConnected)continue;
    const entry=placeForCourse(root.dataset.coursePlace);
    if(!entry){root.innerHTML=`<p>${zh?'此項工程尚未編寫專屬地理與歷史教案。':'Dedicated geography and history have not been authored for this topic.'}</p>`;continue;}
    root.innerHTML=entryMarkup(entry,zh,root.dataset.placeCompact==='true',language);
    const button=root.querySelector('[data-load-course-map]'),host=root.querySelector('[data-course-map-host]');
    if(button&&host)button.addEventListener('click',()=>{
      if(host.querySelector('iframe'))return;
      const urls=googlePlaceUrls(entry.place,language,globalThis.window?.MG_CONFIG?.googleMapsEmbedKey||'');
      const iframe=document.createElement('iframe');iframe.src=urls.embed;iframe.title=`Google Maps · ${field(entry.place,'name',zh)}`;iframe.loading='lazy';iframe.referrerPolicy='strict-origin-when-cross-origin';iframe.allowFullscreen=true;
      host.appendChild(iframe);button.disabled=true;button.textContent=zh?'地圖已載入下方；未顯示時請使用外開連結':'Map requested below; use the external link if unavailable';
    });
  }
  onRendered();
}
