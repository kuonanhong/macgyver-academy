/* V12 project glyphs: data loading, safe inline-SVG rendering and the home-page icon wall.
   Glyph geometry: Tabler Icons (MIT) and Material Design Icons (Apache-2.0), selected and assigned
   to projects by the academy (tools/icons-v12/assign_icons.py). Notices: assets/icons/LICENSES.md.
   Named exports only, no imports: compatible with tools/build-offline.mjs. */

const DATA_URL = 'data/project-icons.json';
const FADE_MS = 380;
const GEOMETRY_RE = /^(?:<(?:path|circle|line|rect|polyline|polygon|ellipse)(?:\s+(?:d|cx|cy|r|x|y|width|height|rx|ry|points|x1|y1|x2|y2)="[-0-9.,eE\sMmLlHhVvCcSsQqTtAaZz]*")+\s*\/>)+$/;
const FALLBACK_GLYPH = '<path d="M12 3l7.8 4.5v9l-7.8 4.5l-7.8 -4.5v-9z"/><circle cx="12" cy="12" r="2.5"/>';

export const PROJECT_ICON_CATEGORY_LABELS = Object.freeze({
  semiconductor: ['半導體製程', 'Semiconductors'],
  packaging: ['先進封裝與矽光子', 'Packaging & photonics'],
  electronics: ['電機與電子', 'Electrical & electronics'],
  computing: ['資訊與資安', 'Computing & security'],
  instruments: ['光學與精密儀器', 'Optics & instruments'],
  structures: ['橋梁與建築', 'Bridges & structures'],
  underground: ['隧道與地下工程', 'Tunnels & geotechnics'],
  water: ['水利與海岸工程', 'Water & coastal'],
  rail: ['鐵路與交通', 'Rail & transit'],
  environment: ['環境與城市', 'Environment & cities'],
  aerospace: ['航空工程', 'Aeronautics'],
  marine: ['船舶與海洋', 'Marine & offshore'],
  automotive: ['汽車與交通工具', 'Automotive'],
  space: ['太空與衛星', 'Space & satellites'],
  manufacturing: ['機械與製造', 'Manufacturing'],
  energy: ['能源與儲能', 'Energy & storage'],
  materials: ['材料與冶金', 'Materials'],
  biomedical: ['醫療工程', 'Biomedical'],
  process: ['工業與食品製程', 'Industrial processes'],
  megascience: ['大型科學設施', 'Megascience']
});

let iconCache = null;
let iconPromise = null;

function esc(value) {
  return String(value ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}

function iconsOf(doc) {
  if (!doc || typeof doc !== 'object') return {};
  const map = doc.icons && typeof doc.icons === 'object' ? doc.icons : doc;
  return map && typeof map === 'object' && !Array.isArray(map) ? map : {};
}

/** Resolve to the {projectId: {n, s, d, q}} map. Uses the offline preload when present, else fetches once. */
export function loadProjectIcons() {
  if (iconCache) return Promise.resolve(iconCache);
  if (iconPromise) return iconPromise;
  const preloaded = globalThis.MG_DATA?.['project-icons'];
  if (preloaded) {
    iconCache = iconsOf(preloaded);
    return Promise.resolve(iconCache);
  }
  if (typeof globalThis.fetch !== 'function') return Promise.resolve({});
  iconPromise = globalThis.fetch(DATA_URL)
    .then(response => {
      if (!response || !response.ok) throw new Error('project icons unavailable');
      return response.json();
    })
    .then(doc => (iconCache = iconsOf(doc)))
    .catch(() => {
      iconPromise = null;   // allow a later retry; callers still get an empty map now
      return {};
    });
  return iconPromise;
}

/** Synchronous access after loadProjectIcons() resolved (or offline preload); null when unknown. */
export function getProjectIcon(projectId) {
  const map = iconCache || iconsOf(globalThis.MG_DATA?.['project-icons']);
  const entry = map[projectId];
  return entry && typeof entry === 'object' ? entry : null;
}

/** Inline SVG string for one icon entry ({n, s, d}). Unknown or unsafe geometry renders a neutral fallback. */
export function projectGlyph(entry, { size = 24, label = '' } = {}) {
  const px = Number.isFinite(Number(size)) && Number(size) > 0 ? Number(size) : 24;
  const geometry = entry && typeof entry.d === 'string' && GEOMETRY_RE.test(entry.d) ? entry.d : FALLBACK_GLYPH;
  const filled = Boolean(entry && entry.s === 'm' && geometry !== FALLBACK_GLYPH);
  const paint = filled
    ? 'fill="currentColor"'
    : 'fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"';
  const a11y = label ? `role="img" aria-label="${esc(label)}"` : 'aria-hidden="true"';
  const source = filled ? 'm' : 't';
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="${px}" height="${px}" ${paint} ` +
    `class="project-glyph" data-glyph-source="${source}" focusable="false" ${a11y}>${geometry}</svg>`;
}

/** Static markup for the (empty) wall; mountHeroIconWall() fills it. */
export function heroIconWallMarkup({ zh = true } = {}) {
  const name = zh ? '工程專案圖示牆' : 'Engineering project icon wall';
  const desc = zh
    ? '這面圖示牆會輪流展示每一個工程專案的代表圖示，每個圖示都是前往該專案的連結。滑鼠停留、鍵盤聚焦或系統偏好減少動態時會停止輪播。'
    : 'This wall cycles through a representative icon for every engineering project; each icon links to its project. Rotation pauses on hover, on keyboard focus and when reduced motion is preferred.';
  return `<section class="icon-wall" data-icon-wall aria-label="${esc(name)}" aria-describedby="icon-wall-desc">` +
    '<div class="icon-wall-grid" data-icon-wall-grid></div>' +
    '<p class="icon-wall-caption" data-icon-wall-caption aria-live="polite" aria-atomic="true"></p>' +
    `<p class="icon-wall-sr sr-only" id="icon-wall-desc" data-icon-wall-desc>${esc(desc)}</p>` +
    '</section>';
}

function mulberry32(seed) {
  let a = seed >>> 0;
  return function next() {
    a = (a + 0x6D2B79F5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function tileCountFor(width) {
  if (width >= 880) return { count: 36, cols: 12 };
  if (width >= 520) return { count: 24, cols: 8 };
  return { count: 12, cols: 6 };
}

function child(doc, parent, selector, tag, className, attrs) {
  const found = parent.querySelector ? parent.querySelector(selector) : null;
  if (found) return found;
  const el = doc.createElement(tag);
  el.className = className;
  for (const [k, v] of Object.entries(attrs)) el.setAttribute(k, v);
  parent.appendChild(el);
  return el;
}

/**
 * Fill the wall with project tiles and rotate them.  Returns {dispose()}.
 * options: zh (labels), icons (map; default: cached/loaded), reducedMotion (default: media query),
 *          interval (ms, default 2200), seed (shuffle seed, default: day number).
 */
export function mountHeroIconWall(root, catalog, { zh = true, icons, reducedMotion, interval = 2200, seed } = {}) {
  const noop = { dispose() {} };
  const doc = root && (root.ownerDocument || globalThis.document);
  if (!root || !doc || typeof doc.createElement !== 'function') return noop;

  const wall = root.matches && root.matches('[data-icon-wall]') ? root
    : (root.querySelector && root.querySelector('[data-icon-wall]')) || child(doc, root, '[data-icon-wall]', 'section', 'icon-wall', { 'data-icon-wall': '' });
  const grid = child(doc, wall, '[data-icon-wall-grid]', 'div', 'icon-wall-grid', { 'data-icon-wall-grid': '' });
  const caption = child(doc, wall, '[data-icon-wall-caption]', 'p', 'icon-wall-caption',
    { 'data-icon-wall-caption': '', 'aria-live': 'polite', 'aria-atomic': 'true' });

  const seen = new Set();
  const items = (Array.isArray(catalog) ? catalog : []).filter(p => {
    if (!p || p.id == null || seen.has(String(p.id))) return false;
    seen.add(String(p.id));
    return true;
  });
  const daySeed = Math.floor(Date.now() / 86400000);
  const rng = mulberry32(Number.isFinite(Number(seed)) ? Number(seed) : daySeed);
  const order = items.map((_, i) => i);
  for (let i = order.length - 1; i > 0; i--) {
    const j = Math.floor(rng() * (i + 1));
    [order[i], order[j]] = [order[j], order[i]];
  }

  const intervalMs = Math.max(20, Number(interval) || 2200);
  const fadeMs = Math.min(FADE_MS, Math.floor(intervalMs / 2));
  let iconMap = icons && typeof icons === 'object' ? icons : (iconCache || {});
  let disposed = false;
  let tiles = [];
  let shown = [];          // item index per tile
  let cursor = 0;          // next position in `order`
  let cols = 0;
  let timer = null;
  const timeouts = new Set();
  const cleanups = [];
  let hovering = false;
  let focused = false;
  let offscreen = false;

  const mql = typeof globalThis.matchMedia === 'function' ? globalThis.matchMedia('(prefers-reduced-motion: reduce)') : null;
  let reduced = reducedMotion == null ? Boolean(mql && mql.matches) : Boolean(reducedMotion);

  const titleOf = p => (zh ? p.title || p.titleEn : p.titleEn || p.title) || String(p.id);
  const categoryOf = p => {
    const labels = PROJECT_ICON_CATEGORY_LABELS[p.category];
    return labels ? labels[zh ? 0 : 1] : String(p.category || '');
  };

  function fill(tile, itemIndex) {
    const p = items[itemIndex];
    const entry = iconMap[p.id];
    const title = titleOf(p);
    tile.setAttribute('href', `#project/${encodeURIComponent(String(p.id))}`);
    tile.setAttribute('title', title);
    tile.setAttribute('data-project-id', String(p.id));
    tile.setAttribute('data-glyph-source', entry && entry.s === 'm' ? 'm' : 't');
    tile.innerHTML = projectGlyph(entry) + `<span class="icon-tile-label">${esc(title)}</span>`;
  }

  function announce(itemIndex) {
    const p = items[itemIndex];
    caption.textContent = '';
    const t = doc.createElement('span');
    t.className = 'icon-wall-caption-title';
    t.textContent = titleOf(p);
    const c = doc.createElement('span');
    c.className = 'icon-wall-caption-category';
    c.textContent = categoryOf(p);
    caption.appendChild(t);
    caption.appendChild(c);
  }

  function nextItem() {
    const onWall = new Set(shown);
    for (let guard = 0; guard < order.length; guard++) {
      const idx = order[cursor % order.length];
      cursor = (cursor + 1) % order.length;
      if (!onWall.has(idx)) return idx;
    }
    return -1;
  }

  function measure() {
    const width = wall.clientWidth || (wall.getBoundingClientRect && wall.getBoundingClientRect().width) ||
      root.clientWidth || globalThis.innerWidth || 1024;
    return tileCountFor(width);
  }

  function build() {
    const layout = measure();
    const count = Math.min(layout.count, items.length);
    if (count === tiles.length && layout.cols === cols) return;
    cols = layout.cols;
    if (wall.style && wall.style.setProperty) wall.style.setProperty('--icon-wall-cols', String(Math.min(cols, Math.max(count, 1))));
    grid.textContent = '';
    tiles = [];
    shown = shown.slice(0, count);
    for (let k = 0; k < count; k++) {
      const tile = doc.createElement('a');
      tile.className = 'icon-tile';
      if (tile.style && tile.style.setProperty) tile.style.setProperty('--icon-tile-index', String(k));
      if (shown[k] == null || shown[k] < 0) shown[k] = nextItem();
      const idx = shown[k];
      fill(tile, idx);
      grid.appendChild(tile);
      tiles.push(tile);
    }
    if (shown.length && !caption.textContent) announce(shown[0]);
  }

  function paused() {
    return disposed || reduced || hovering || focused || offscreen || Boolean(doc.hidden);
  }

  function tick() {
    if (paused() || tiles.length === 0 || items.length <= tiles.length) return;
    const swaps = Math.min(tiles.length, 3 + Math.floor(rng() * 2));
    const picked = new Set();
    while (picked.size < swaps) picked.add(Math.floor(rng() * tiles.length));
    let last = -1;
    for (const k of picked) {
      const idx = nextItem();
      if (idx < 0) break;
      shown[k] = idx;
      last = idx;
      const tile = tiles[k];
      tile.classList.add('is-swapping');
      const id = setTimeout(() => {
        timeouts.delete(id);
        if (disposed || tiles[k] !== tile) return;
        fill(tile, shown[k]);
        tile.classList.remove('is-swapping');
      }, fadeMs);
      timeouts.add(id);
    }
    if (last >= 0) announce(last);
  }

  function start() {
    if (timer == null && !reduced && !disposed && !doc.hidden && items.length > tiles.length) {
      timer = setInterval(tick, intervalMs);
    }
  }
  function stop() {
    if (timer != null) clearInterval(timer);
    timer = null;
  }

  function listen(target, type, handler, opts) {
    if (!target || typeof target.addEventListener !== 'function') return;
    target.addEventListener(type, handler, opts);
    cleanups.push(() => target.removeEventListener(type, handler, opts));
  }

  build();
  wall.classList && wall.classList.toggle('is-static', reduced);
  if (wall.setAttribute) wall.setAttribute('data-icon-wall-ready', '');

  listen(wall, 'pointerenter', () => { hovering = true; });
  listen(wall, 'pointerleave', () => { hovering = false; });
  listen(wall, 'focusin', () => { focused = true; });
  listen(wall, 'focusout', event => {
    focused = Boolean(event && event.relatedTarget && wall.contains && wall.contains(event.relatedTarget));
  });
  listen(doc, 'visibilitychange', () => { if (doc.hidden) stop(); else start(); });
  if (mql && reducedMotion == null) {
    const onChange = event => {
      reduced = Boolean(event && event.matches);
      wall.classList && wall.classList.toggle('is-static', reduced);
      if (reduced) stop(); else start();
    };
    if (typeof mql.addEventListener === 'function') {
      mql.addEventListener('change', onChange);
      cleanups.push(() => mql.removeEventListener('change', onChange));
    } else if (typeof mql.addListener === 'function') {
      mql.addListener(onChange);
      cleanups.push(() => mql.removeListener(onChange));
    }
  }
  if (typeof globalThis.ResizeObserver === 'function') {
    const ro = new globalThis.ResizeObserver(() => { if (!disposed) { build(); start(); } });
    ro.observe(wall);
    cleanups.push(() => ro.disconnect());
  }
  if (typeof globalThis.IntersectionObserver === 'function') {
    const io = new globalThis.IntersectionObserver(entries => {
      const last = entries[entries.length - 1];
      offscreen = Boolean(last) && !last.isIntersecting;
    });
    io.observe(wall);
    cleanups.push(() => io.disconnect());
  }
  if (!icons && !iconCache) {
    loadProjectIcons().then(map => {
      if (disposed || !map || !Object.keys(map).length) return;
      iconMap = map;
      tiles.forEach((tile, k) => { if (shown[k] >= 0) fill(tile, shown[k]); });
    });
  }
  start();

  return {
    dispose() {
      if (disposed) return;
      disposed = true;
      stop();
      for (const id of timeouts) clearTimeout(id);
      timeouts.clear();
      while (cleanups.length) {
        try { cleanups.pop()(); } catch (_) { /* observer already gone */ }
      }
      tiles.forEach(tile => tile.classList && tile.classList.remove('is-swapping'));
    }
  };
}
