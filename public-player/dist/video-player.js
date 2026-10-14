/* Public stateless HTTPS presentation wrapper, not a proxy or account service.
 * A file:// parent has the opaque origin "null". Replies to that parent must use
 * targetOrigin="*", but contain only a public video ID, nonce and player status.
 * Source window + opaque origin + nonce + video ID are checked before loading.
 * No credentials, cookies, account identity, progress, local path or API keys are read.
 */
(function () {
  'use strict';
  const params = new URLSearchParams(location.search);
  const videoId = params.get('video') || '';
  const zh = params.get('lang') !== 'en';
  const channel = new URLSearchParams(location.hash.slice(1)).get('channel') || '';
  const idValid = /^[A-Za-z0-9_-]{11}$/.test(videoId);
  const approved = Array.isArray(window.MG_CONFIG?.allowedYouTubeIds) && window.MG_CONFIG.allowedYouTubeIds.includes(videoId);
  const channelValid = /^[A-Za-z0-9-]{20,80}$/.test(channel);
  const embedded = window.parent !== window;
  const status = document.getElementById('videoStatus');
  const button = document.getElementById('loadVideo');
  const frame = document.getElementById('playerFrame');
  const watch = document.getElementById('watchVideo');
  const hosted = document.getElementById('hostedVideo');
  let started = false, handshake = false, readyTimer;
  const say = (a, b) => { status.textContent = zh ? a : b; };
  function post(type, code) {
    if (!embedded || !channelValid) return;
    const message = { scope: 'macgyver-video-v1', type, channel, videoId };
    if (Number.isInteger(code)) message.code = code;
    window.parent.postMessage(message, '*');
  }
  function error(code) {
    clearTimeout(readyTimer);
    const reason = ({
      2: ['影片識別碼或參數不正確。', 'Invalid video ID or player parameters.'],
      5: ['瀏覽器無法播放此格式。', 'The browser could not play this format.'],
      100: ['影片不存在、已移除或設為私人。', 'The video is unavailable, removed or private.'],
      101: ['作者禁止內嵌播放。', 'The publisher does not permit embedding.'],
      150: ['作者禁止內嵌播放。', 'The publisher does not permit embedding.'],
      153: ['YouTube 未收到可接受的網站來源識別。', 'YouTube did not receive acceptable website identification.']
    })[code] || ['播放器未能載入。', 'The player could not load.'];
    say(`播放錯誤 ${code}：${reason[0]}請使用下方 YouTube 連結。`, `Playback error ${code}: ${reason[1]} Use the YouTube link below.`);
    post('error', code);
  }
  if (!idValid) {
    button.disabled = true;
    say('無效的影片識別碼；未連線至影片提供者。', 'Invalid video ID. No connection to the video provider was made.');
    return;
  }
  if (!approved) {
    button.disabled = true;
    say('此影片不在工程學院公開教材清單中；未載入外部播放器。', 'This video is not in the academy’s approved public curriculum. No external player was loaded.');
    return;
  }
  document.documentElement.lang = zh ? 'zh-Hant' : 'en';
  watch.href = `https://www.youtube.com/watch?v=${videoId}`; watch.hidden = false;
  watch.textContent = zh ? '在 YouTube 觀看 ↗' : 'Watch on YouTube ↗';
  button.textContent = zh ? '載入 YouTube 教學影片' : 'Load YouTube educational video';
  if (location.protocol !== 'https:') {
    button.disabled = true;
    let destination = 'https://macgyver-public-player.kuonanhong.chatgpt.site/video-player.html';
    try {
      const custom = new URL(window.MG_CONFIG?.videoPlayerUrl);
      if (custom.protocol === 'https:' && !custom.username && !custom.password && !custom.search && !custom.hash && custom.pathname.endsWith('/video-player.html')) destination = custom.href;
    } catch { /* Invalid configuration falls back to the shipped HTTPS page. */ }
    const online = new URL(destination); online.searchParams.set('video', videoId); online.searchParams.set('lang', zh ? 'zh-TW' : 'en');
    hosted.href = online.href;
    hosted.hidden = false;
    say('請開啟 HTTPS 播放頁；本機 HTML 無法自行提供 HTTP Referer。', 'Open the HTTPS player page. A local HTML file cannot provide an HTTP Referer by itself.');
    return;
  }
  function start() {
    if (started) return;
    started = true;
    say('正在載入 YouTube；請按影片中的播放鍵。', 'Loading YouTube. Select the video’s play button.');
    const iframe = document.createElement('iframe');
    iframe.title = zh ? 'YouTube 教學影片' : 'YouTube educational video';
    iframe.referrerPolicy = 'strict-origin-when-cross-origin';
    iframe.allow = 'encrypted-media; fullscreen; picture-in-picture';
    iframe.allowFullscreen = true;
    const source = new URL(`https://www.youtube-nocookie.com/embed/${videoId}`);
    source.searchParams.set('rel', '0'); source.searchParams.set('playsinline', '1'); source.searchParams.set('enablejsapi', '1');
    source.searchParams.set('origin', location.origin);
    iframe.src = source.href;
    frame.replaceChildren(iframe);
    readyTimer = setTimeout(() => {
      say('YouTube 尚未就緒；若網路、瀏覽器或影片限制阻擋內嵌，請在 YouTube 原頁觀看。', 'YouTube is not ready. If network, browser or video restrictions block embedding, watch on YouTube.');
      post('error', 0);
    }, 15000);
    window.onYouTubeIframeAPIReady = function () {
      if (!window.YT?.Player) { error(0); return; }
      new window.YT.Player(iframe, { events: {
        onReady() { clearTimeout(readyTimer); say('播放器已就緒；請按影片的播放鍵。', 'Player ready. Select the video’s play button.'); post('player-ready'); },
        onError(event) { error(Number.isInteger(event.data) ? event.data : 0); }
      } });
    };
    const script = document.createElement('script'); script.src = 'https://www.youtube.com/iframe_api'; script.async = true;
    script.referrerPolicy = 'strict-origin-when-cross-origin'; script.onerror = () => error(0);
    document.head.appendChild(script);
  }
  button.onclick = start;
  window.addEventListener('message', event => {
    const data = event.data;
    if (!embedded || !channelValid || event.source !== window.parent || event.origin !== 'null' || !data || typeof data !== 'object' || Array.isArray(data) || data.scope !== 'macgyver-video-v1' || data.type !== 'init' || data.channel !== channel || data.videoId !== videoId) return;
    // Only a matching explicit click in the local parent authorizes this load.
    handshake = true; start();
  });
  if (embedded && channelValid) {
    post('ready');
    setTimeout(() => { if (!handshake && !started) say('等待本機頁面授權；也可按「載入」或下方 YouTube 連結。', 'Waiting for the local page. You can also select Load or use the YouTube link.'); }, 8000);
  }
})();
