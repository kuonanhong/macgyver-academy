/* Classic scripts also run under file://, where ES module imports are blocked. */
(function () {
  'use strict';
  function load(source) {
    return new Promise((resolve, reject) => {
      const script = document.createElement('script');
      script.src = source; script.async = false;
      script.onload = resolve;
      script.onerror = () => reject(new Error('Unable to load ' + source));
      document.head.appendChild(script);
    });
  }
  (async function () {
    window.MacGyverNativeFetch = window.fetch.bind(window);
    await load('config.js');
    await load('runtime-mode.js');
    const staticMode = location.protocol === 'file:' || window.MG_STATIC_MODE === true || window.MG_CONFIG?.siteMode === 'static' || /(^|\.)github\.io$/i.test(location.hostname || '');
    if (staticMode) {
      window.MG_STATIC_MODE = true;
      if (location.protocol === 'file:') {
        await load('offline-data.js');
        for(const part of window.MG_DATA_FILES || []) {
          if(!/^offline-data-\d+\.js$/.test(part)) throw new Error('Invalid course part');
          await load(part);
        }
      }
      await load('offline-runtime.js');
    }
    await load('app.bundle.js');
  })().catch(error => {
    const main = document.getElementById('main');
    if (!main) return;
    main.replaceChildren();
    const title = document.createElement('h2'); title.textContent = '離線套件載入失敗 / Offline package could not load';
    const detail = document.createElement('p'); detail.textContent = '請先完整解壓縮 ZIP，再以目前的 Chrome、Edge、Firefox 或 Safari 開啟根目錄 index.html。保留 public/academy/ 的所有檔案。Extract the whole ZIP before opening index.html.';
    const technical = document.createElement('code'); technical.textContent = error.message;
    main.append(title, detail, technical);
  });
})();
