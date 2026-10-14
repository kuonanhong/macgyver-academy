/** Curated, attributable educational media. No third-party request until play. */
let mediaCourses = [];
// A separate public, stateless player serves anonymous video viewing only.
// A file:// parent cannot manufacture an HTTP Referer by adding origin=.
export const HOSTED_VIDEO_PLAYER = 'https://macgyver-public-player.kuonanhong.chatgpt.site/video-player.html';
const VIDEO_ID = /^[A-Za-z0-9_-]{11}$/;
let youtubeApiPromise;
const mediaSessions = new Set();
const escape = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const text = (object, key, zh) => object?.[zh ? key : `${key}En`] || object?.[key] || '';
const array = value => Array.isArray(value) ? value : [];
// Bundled raster images only: no parent traversal, URL schemes, query strings,
// encoded separators or executable SVG imported through the photo manifest.
export function safeBundledPhotoPath(value) {
  return typeof value === 'string' && /^(?:assets\/photos\/[A-Za-z0-9_-]+|assets\/v8-[A-Za-z0-9_-]+)\.(?:jpg|jpeg|png|webp)$/i.test(value) ? value : '';
}
export function photoContextCaption(photo, courseId, zh = true) {
  return text(photo?.courseContext?.[courseId], 'note', zh) || text(photo, 'scope', zh) || text(photo, 'note', zh) || text(photo, 'caption', zh) || '';
}
export function safeMediaLink(value) {
  try { const url = new URL(value); return url.protocol === 'https:' && !url.username && !url.password ? url.href : ''; } catch { return ''; }
}
export function safeNativeVideoUrl(value) {
  const safe=safeMediaLink(value); if(!safe) return '';
  const url=new URL(safe);
  const approved=(url.hostname==='www.aidc.com.tw' && url.pathname==='/avideo/AIDCenterprise_en.mp4') ||
    (url.hostname==='ferrari.scene7.com' && /^\/is\/content\/ferrari\/[a-f0-9-]+$/.test(url.pathname)) ||
    (url.hostname==='www.ctg.com.cn' && ['/cypc/fileDirweb/cypc/video/sxgc.mp4','/sxjt/sxgc4/kpsp/2024081105575717439/2021062916005544951.mp4'].includes(url.pathname));
  return approved && !url.port && !url.search && !url.hash ? safe : '';
}
export function safeEmbedUrl(value) {
  try {
    const url = new URL(value);
    if (url.protocol !== 'https:' || url.username || url.password || url.port) return '';
    if (url.hostname === 'www.youtube-nocookie.com' && /^\/embed\/[A-Za-z0-9_-]{11}$/.test(url.pathname)) {
      // Deliberately do not forward arbitrary data parameters or enable autoplay.
      return `${url.origin}${url.pathname}?rel=0&playsinline=1`;
    }
    if (url.hostname === 'player.vimeo.com' && /^\/video\/\d+$/.test(url.pathname)) return `${url.origin}${url.pathname}`;
    if (url.hostname === 'www.nps.gov' && url.pathname === '/media/video/embed.htm' && /^[A-Fa-f0-9-]{36}$/.test(url.searchParams.get('id')||'')) return `${url.origin}${url.pathname}?id=${url.searchParams.get('id')}`;
  } catch {}
  return '';
}
export function youtubeVideoId(value) {
  const safe = safeEmbedUrl(value);
  if (!safe) return '';
  const url = new URL(safe);
  return url.hostname === 'www.youtube-nocookie.com' ? url.pathname.split('/').at(-1) : '';
}
export function safeVideoPlayerUrl(value) {
  try {
    if (typeof value !== 'string') return '';
    const url = new URL(value);
    return url.protocol === 'https:' && !url.username && !url.password && !url.search && !url.hash && url.pathname.endsWith('/video-player.html') ? url.href : '';
  } catch { return ''; }
}
export function videoPlaybackPlan(value, currentLocation = globalThis.location, config = globalThis.window?.MG_CONFIG || globalThis.MG_CONFIG) {
  const src = safeEmbedUrl(value), videoId = youtubeVideoId(src);
  if (!src) return null;
  if (!videoId) return { kind: 'direct', src };
  const wrapper = new URL(safeVideoPlayerUrl(config?.videoPlayerUrl) || HOSTED_VIDEO_PLAYER); wrapper.searchParams.set('video', videoId);
  const watchUrl = `https://www.youtube.com/watch?v=${videoId}`;
  if (currentLocation?.protocol === 'file:') return { kind: 'https-wrapper', src: wrapper.href, wrapperUrl: wrapper.href, watchUrl, videoId };
  const direct = new URL(src); direct.searchParams.set('enablejsapi', '1');
  // origin is the actual current HTTP(S) page, never a made-up substitute for Referer.
  try { const origin = new URL(currentLocation?.href || currentLocation?.origin); if (['https:', 'http:'].includes(origin.protocol)) direct.searchParams.set('origin', origin.origin); } catch {}
  return { kind: 'direct', src: direct.href, wrapperUrl: wrapper.href, watchUrl, videoId };
}
export function trustedVideoMessage(event, session) {
  const data = event?.data;
  return !!(session.source && typeof session.origin === 'string' && session.origin.startsWith('https://') && event?.source === session.source && event.origin === session.origin && data && typeof data === 'object' && !Array.isArray(data) && data.scope === 'macgyver-video-v1' && data.channel === session.channel && data.videoId === session.videoId && VIDEO_ID.test(data.videoId) && ['ready', 'player-ready', 'error'].includes(data.type) && (data.type !== 'error' || Number.isInteger(data.code)));
}
export function videoErrorMessage(code, zh = true) {
  const descriptions = {
    2: ['影片識別碼或播放器參數不正確。', 'The video ID or player parameters are invalid.'],
    5: ['瀏覽器無法播放此影片格式。', 'The browser could not play this video format.'],
    100: ['影片不存在、已移除或設為私人。', 'The video is unavailable, removed or private.'],
    101: ['影片作者禁止嵌入；請在 YouTube 原頁觀看。', 'The publisher does not allow embedding. Watch on YouTube.'],
    150: ['影片作者禁止嵌入；請在 YouTube 原頁觀看。', 'The publisher does not allow embedding. Watch on YouTube.'],
    153: ['YouTube 未收到可接受的網站來源識別。請開啟線上播放器或 YouTube 原頁。', 'YouTube did not receive acceptable website identification. Open the online player or watch on YouTube.']
  };
  const detail = descriptions[code]?.[zh ? 0 : 1] || (zh ? '播放器未能載入。請使用下方直接開啟連結。' : 'The player could not load. Use the direct links below.');
  return `${zh ? '播放錯誤' : 'Playback error'} ${Number.isInteger(code) ? code : ''}: ${detail}`;
}
function loadYouTubeApi(view) {
  if (view.YT?.Player) return Promise.resolve(view.YT);
  if (youtubeApiPromise) return youtubeApiPromise;
  const pending = new Promise((resolve, reject) => {
    const previous = view.onYouTubeIframeAPIReady;
    let settled = false, timer;
    const script = view.document.createElement('script'); script.src = 'https://www.youtube.com/iframe_api'; script.async = true; script.referrerPolicy = 'strict-origin-when-cross-origin';
    const finish = error => {
      if (settled) return; settled = true; view.clearTimeout(timer);
      if (view.onYouTubeIframeAPIReady === ready) view.onYouTubeIframeAPIReady = previous;
      if (error) { script.remove?.(); reject(error); } else resolve(view.YT);
    };
    const ready = () => { try { if (typeof previous === 'function') previous(); } finally { finish(view.YT?.Player ? null : new Error('YouTube API unavailable')); } };
    view.onYouTubeIframeAPIReady = ready;
    timer = view.setTimeout(() => finish(new Error('YouTube API timeout')), 15000);
    script.onerror = () => finish(new Error('YouTube API unavailable'));
    view.document.head.appendChild(script);
  });
  youtubeApiPromise = pending;
  // A transient script/network failure must allow the next explicit play to
  // retry. An older rejection must not clear a newer in-flight request.
  pending.catch(() => { if (youtubeApiPromise === pending) youtubeApiPromise = undefined; });
  return pending;
}
export function createVideoChannel(view = globalThis.window) {
  try {
    const uuid = view?.crypto?.randomUUID?.();
    if (typeof uuid === 'string' && /^[A-Za-z0-9-]{20,80}$/.test(uuid)) return uuid;
    if (view?.crypto?.getRandomValues) return [...view.crypto.getRandomValues(new Uint8Array(16))].map(n => n.toString(16).padStart(2, '0')).join('');
  } catch { /* Non-security fallback for this public playback-status channel. */ }
  return `${Date.now().toString(36).padStart(12, '0')}-${Math.random().toString(36).slice(2).padEnd(24, '0')}`;
}
export function disposeLearningMedia(root = globalThis.document) {
  for (const session of [...mediaSessions]) if (root === session.root || root === session.frame || root?.contains?.(session.frame)) session.dispose();
}
export function setLearningMedia(data) {
  mediaCourses = array(Array.isArray(data) ? data : data?.courses).filter(c => typeof c?.courseId === 'string');
}
export function mediaForCourse(id) { return mediaCourses.find(c => c.courseId === id) || null; }
function guideMarkup(guide, zh) {
  const rows = [['concept','原理與邊界','Principle and limits'],['procedure','練習流程','Learning procedure'],['evidence','要留下的證據','Evidence to record'],['pitfalls','常見誤判','Common mistakes']];
  const diagramPath=(!zh&&guide.diagram?.pathEn)||guide.diagram?.path;
  const diagram=guide.diagram?.original===true&&/^assets\/diagrams\/v10-[a-z0-9-]+\.svg$/.test(diagramPath||'')?`<figure class="media-original-diagram"><img loading="lazy" src="${escape(diagramPath)}" alt="${escape(text(guide.diagram,'alt',zh)||text(guide.diagram,'title',zh))}" style="width:100%;height:auto"><figcaption>${escape(text(guide.diagram,'title',zh))} · ${zh?'本站原創概念圖；非依比例繪製，非廠商施工圖。':'Original educational concept diagram; not to scale or a vendor construction drawing.'}</figcaption></figure>`:'';
  return `<details class="media-guide"><summary>${escape(text(guide,'title',zh))}</summary>${diagram}${rows.map(([key,z,en]) => {
    const value = text(guide,key,zh); if (!value || (Array.isArray(value) && !value.length)) return '';
    return `<h4>${zh?z:en}</h4>${Array.isArray(value)?`<ol>${value.map(item=>`<li>${escape(item)}</li>`).join('')}</ol>`:`<p>${escape(value)}</p>`}`;
  }).join('')}<div class="media-references">${array(guide.sources || (guide.sourceURL?[guide.sourceURL]:[])).map(source => {
    const url = safeMediaLink(typeof source === 'string' ? source : source.url); return url?`<a href="${escape(url)}" target="_blank" rel="noopener">${escape(typeof source==='string' ? new URL(url).hostname : text(source,'title',zh) || new URL(url).hostname)} ↗</a>`:'';
  }).join(' · ')}</div></details>`;
}
function videoMarkup(video, zh, index) {
  const url = safeMediaLink(video.url || video.sourcePage), embed = safeEmbedUrl(video.embedUrl), native=safeNativeVideoUrl(video.nativeVideoUrl);
  const plan = videoPlaybackPlan(embed), local = plan?.kind === 'https-wrapper';
  const playerLinks = plan?.videoId ? `<div class="video-fallbacks"><a class="video-direct-link" href="${escape(plan.wrapperUrl)}&amp;lang=${zh?'zh-TW':'en'}" target="_blank" rel="noopener" referrerpolicy="strict-origin-when-cross-origin">${zh?'開啟線上播放器':'Open online player'} ↗</a><a class="video-direct-link" href="${escape(plan.watchUrl)}" target="_blank" rel="noopener" referrerpolicy="strict-origin-when-cross-origin">${zh?'在 YouTube 觀看':'Watch on YouTube'} ↗</a></div><p class="video-status" data-video-status role="status">${local?(zh?'本機檔案透過免學院登入的公開 HTTPS 播放頁載入影片；需要網路。若瀏覽器或 YouTube 限制內嵌，可直接開啟上方連結。':'Local files use a public HTTPS player without academy sign-in. Internet is required. Use the direct links if your browser or YouTube restricts embedding.'):(zh?'點擊後才連線至 YouTube；若內嵌受限，請使用直接開啟連結。':'YouTube connects only after you select Load. Use a direct link if embedding is restricted.')}</p>` : '<p class="video-status" data-video-status role="status"></p>';
  const title = text(video,'title',zh);
  return `<article class="video-card"><div class="video-frame" data-video-frame>${(embed||native)?`<button type="button" class="video-load" data-video-embed="${escape(embed)}" data-video-file="${escape(native)}" data-video-language="${zh?'zh-TW':'en'}" data-video-title="${escape(title)}"><span aria-hidden="true">▶</span><b>${zh?'載入教學影片':'Load educational video'}</b><small>${local?(zh?'點擊後連線至已部署的 HTTPS 播放頁與 YouTube':'Connects to the deployed HTTPS player and YouTube when selected'):(zh?'點擊後連線至影片提供者':'Connects to the video provider when selected')}</small></button>`:`<div class="video-official"><span aria-hidden="true">↗</span><p>${zh?'官方頁面內播放':'Watch on the official page'}</p>${url?`<a class="button light" href="${escape(url)}" target="_blank" rel="noopener">${zh?'開啟影片':'Open video'} ↗</a>`:''}</div>`}</div><div class="video-copy">${playerLinks}<span class="task-label">VIDEO ${String(index+1).padStart(2,'0')} · ${escape(video.publisher)}</span><h4>${escape(title)}</h4>${video.scope?`<p>${escape(text(video,'scope',zh))}</p>`:''}<p class="subtext">${zh?'影片原文':'Original language'}: ${escape(video.language || 'See provider')} · ${zh?'字幕依原作者提供':'Captions depend on the publisher'}</p>${array(text(video,'watchFor',zh)).length?`<p><strong>${zh?'觀看時找出':'While watching, identify'}</strong></p><ol>${array(text(video,'watchFor',zh)).map(point=>`<li>${escape(point)}</li>`).join('')}</ol>`:''}${video.captionNote?`<p class="subtext">${escape(text(video,'captionNote',zh))}</p>`:''}${video.before?`<p><b>${zh?'看前':'Before'}:</b> ${escape(text(video,'before',zh))}</p>`:''}${video.after?`<p><b>${zh?'看後':'After'}:</b> ${escape(text(video,'after',zh))}</p>`:''}<div class="media-references">${url?`<a href="${escape(url)}" target="_blank" rel="noopener">${zh?'影片原頁／播放失敗時開啟':'Original / open if the player fails'} ↗</a>`:''}${safeMediaLink(video.sourcePage)&&video.sourcePage!==url?`<a href="${escape(safeMediaLink(video.sourcePage))}" target="_blank" rel="noopener">${zh?'官方來源':'Official source'} ↗</a>`:''}</div></div></article>`;
}
export function learningMediaMarkup(course, {zh=true, photos=[], step=null, compact=false}={}) {
  const matchedPhotos = array(photos).filter(p => array(p.courseIds).includes(course.id) && safeBundledPhotoPath(p.path));
  const entry = mediaForCourse(course.id) || {videos:[],guides:[]};
  const videos = array(entry.videos), guides = array(entry.guides);
  if(!matchedPhotos.length&&!videos.length&&!guides.length)return '';
  const stepTitle = step ? text(step,'title',zh) : '';
  const heading = zh?'圖像、影片與深入研習':'Photographs, videos and deeper study';
  return `<section class="learning-media task-card"><span class="task-label">OBSERVE · EXPLAIN · VERIFY</span><h3>${heading}</h3><p class="subtext">${zh?'本區是專案層級的補充教材；影片與照片不代表每一道工序的實拍。':'These are project-level supporting materials, not recordings of every individual process.'}</p>${step?`<p class="media-step-prompt">${zh?'本步觀察任務':'Your observation task'}: <strong>${escape(stepTitle)}</strong> — ${escape(text(step,'observation',zh) || text(step,'objective',zh))}</p>`:''}${compact?'<details class="media-library"><summary>'+ (zh?'展開本專案的照片、影片與研習':'Open this project’s photos, videos and study guides') +'</summary>':''}${matchedPhotos.length?`<div class="media-photo-gallery">${matchedPhotos.map(p=>`<figure><a href="${escape(p.path)}" target="_blank" rel="noopener"><img loading="lazy" src="${escape(p.path)}" alt="${escape(text(p,'title',zh))}"></a><figcaption><strong>${escape(text(p,'title',zh))}</strong><p>${escape(photoContextCaption(p,course.id,zh))}</p><small>${escape(p.author)} · ${escape(p.license)} · <a href="${escape(safeMediaLink(p.sourceUrl))}" target="_blank" rel="noopener">${zh?'來源':'Source'} ↗</a> · <a href="${escape(safeMediaLink(p.licenseUrl))}" target="_blank" rel="noopener">${zh?'授權':'License'} ↗</a></small></figcaption></figure>`).join('')}</div>`:''}${guides.length?`<h4 class="mt">${zh?'深入理解與證據練習':'Deeper understanding and evidence exercises'}</h4><div class="media-guides">${guides.map(g=>guideMarkup(g,zh)).join('')}</div>`:''}${videos.length?`<h4 class="mt">${zh?'教學影片':'Educational videos'}</h4><div class="video-grid">${videos.map((v,i)=>videoMarkup(v,zh,i)).join('')}</div>`:''}${compact?'</details>':''}</section>`;
}
export function bindLearningMedia(root=globalThis.document, onChange=()=>{}) {
  const owned = new Set();
  const own = (frame, cleanup) => {
    let disposed = false;
    const session = { root, frame, dispose() { if (disposed) return; disposed = true; try { cleanup(); } finally { owned.delete(session); mediaSessions.delete(session); } } };
    owned.add(session); mediaSessions.add(session); return session.dispose;
  };
  for (const button of root?.querySelectorAll?.('[data-video-embed]') || []) {
    button.onclick=()=>{
      const src = safeEmbedUrl(button.dataset.videoEmbed), file=safeNativeVideoUrl(button.dataset.videoFile); if (!src && !file) return;
      const frame=button.closest?.('[data-video-frame]'); if(!frame) return;
      disposeLearningMedia(frame);
      const view = root?.ownerDocument?.defaultView || globalThis.window;
      const plan = videoPlaybackPlan(src, view?.location || globalThis.location), zh = button.dataset.videoLanguage !== 'en';
      const status = button.closest?.('.video-card')?.querySelector?.('[data-video-status]');
      const report = value => { if (status) status.textContent = value; };
      let channel = '', playerSrc = plan?.src || src;
      if (plan?.kind === 'https-wrapper') {
        channel = createVideoChannel(view);
        const wrapper = new URL(playerSrc); wrapper.searchParams.set('lang', zh ? 'zh-TW' : 'en'); wrapper.hash = new URLSearchParams({ channel }).toString(); playerSrc = wrapper.href;
        frame.classList?.add('has-video-wrapper');
        report(zh?'正在連線至公開 HTTPS 播放頁，不需登入工程學院。':'Connecting to the public HTTPS player. No academy sign-in is required.');
      }
      frame.innerHTML=file?`<video controls playsinline preload="none" aria-label="${escape(button.dataset.videoTitle)}"><source src="${escape(file)}" type="video/mp4"></video>`:`<iframe src="${escape(playerSrc)}" title="${escape(button.dataset.videoTitle)}" referrerpolicy="strict-origin-when-cross-origin" allow="encrypted-media; fullscreen; picture-in-picture" allowfullscreen></iframe>`;
      const iframe = frame.querySelector?.('iframe');
      if (plan?.kind === 'https-wrapper' && iframe && view) {
        // Capture this load's actual validated origin; later config changes
        // cannot widen the origin accepted by an already running player.
        const target = new URL(playerSrc).origin;
        let received = false, timer;
        const session = { source: iframe.contentWindow, origin: target, channel, videoId: plan.videoId };
        const init = () => iframe.contentWindow?.postMessage({ scope: 'macgyver-video-v1', type: 'init', channel, videoId: plan.videoId }, target);
        const listener = event => {
          if (frame.isConnected === false) { dispose(); return; }
          if (!trustedVideoMessage(event, session)) return;
          if (event.data.type === 'ready') { received = true; init(); }
          if (event.data.type === 'player-ready') { view.clearTimeout(timer); report(zh?'播放器已就緒；請按影片的播放鍵。':'Player ready. Select the video’s play button.'); }
          if (event.data.type === 'error') { view.clearTimeout(timer); report(videoErrorMessage(event.data.code, zh)); }
        };
        const dispose = own(frame, () => { view.removeEventListener('message', listener); view.clearTimeout(timer); iframe.onload = null; iframe.remove?.(); });
        view.addEventListener('message', listener); iframe.onload = init;
        timer = view.setTimeout(() => { if (frame.isConnected === false) { dispose(); return; } report(received?(zh?'YouTube 尚未就緒；網路或瀏覽器可能限制內嵌。請開啟線上播放器或 YouTube 原頁。':'YouTube is not ready. Network or browser restrictions may block embedding. Open the online player or YouTube.'):(zh?'無法確認公開播放頁已載入；網路或瀏覽器可能阻擋。請開啟線上播放器或 YouTube 原頁。':'The public player has not responded. Network or browser restrictions may block it. Open the online player or YouTube.')); }, 15000);
      } else if (plan?.videoId && iframe && view) {
        let disposed = false, player;
        own(frame, () => { disposed = true; try { player?.destroy?.(); } finally { iframe.remove?.(); } });
        report(zh?'正在載入 YouTube；請按影片的播放鍵。':'Loading YouTube. Select the video’s play button.');
        loadYouTubeApi(view).then(YT => {
          if (disposed || frame.isConnected === false) return;
          player = new YT.Player(iframe, { events: { onReady: () => report(zh?'播放器已就緒；請按影片的播放鍵。':'Player ready. Select the video’s play button.'), onError: event => report(videoErrorMessage(event.data, zh)) } });
        }).catch(() => { if (!disposed) report(zh?'無法取得播放器狀態；若影片無法播放，請使用直接開啟連結。':'Player status is unavailable. Use the direct links if playback fails.'); });
      }
      onChange();
    };
  }
  return () => { for (const session of [...owned]) session.dispose(); };
}
