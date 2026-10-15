// V12 project icons: data integrity, safe SVG rendering and the hero icon wall (no dependencies).
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {PROJECT_ICON_CATEGORY_LABELS,loadProjectIcons,getProjectIcon,projectGlyph,heroIconWallMarkup,mountHeroIconWall} from '../public/academy/project-icons.js';

const read = rel => fs.readFileSync(new URL(rel, import.meta.url), 'utf8');
const catalog = JSON.parse(read('../public/academy/data/catalog.json'));
const raw = read('../public/academy/data/project-icons.json');
const doc = JSON.parse(raw);
const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));

// ---- data file --------------------------------------------------------------------------------
assert.equal(doc.version, 12);
assert.deepEqual(doc.sources.tabler, {license: 'MIT', url: 'https://tabler.io/icons'});
assert.deepEqual(doc.sources.mdi, {license: 'Apache-2.0', url: 'https://pictogrammers.com/library/mdi/'});
assert(Buffer.byteLength(raw) < 1.2 * 1024 * 1024, `project-icons.json is ${Buffer.byteLength(raw)} bytes`);
assert(!/\n\s/.test(raw), 'project-icons.json is compact');
const ids = catalog.map(p => p.id);
const entries = Object.entries(doc.icons);
assert.equal(catalog.length, 2066, 'catalog size');
assert.equal(entries.length, 2066, 'one icon per project');
assert.deepEqual(new Set(Object.keys(doc.icons)), new Set(ids), 'every catalog id is covered, no extras');

const ELEMENT = /<(path|circle|line|rect|polyline|polygon|ellipse)((?:\s+[a-z0-9]+="[^"]*")+)\s*\/>/g;
const GEOMETRY = new Set(['d', 'cx', 'cy', 'r', 'x', 'y', 'width', 'height', 'rx', 'ry', 'points', 'x1', 'y1', 'x2', 'y2']);
const names = new Set(), markups = new Set();
for (const [id, e] of entries) {
  assert.equal(typeof e.n, 'string', id);
  assert(e.n.length > 0 && !e.n.startsWith('brand-'), `${id}: no brand glyphs`);
  assert(e.s === 't' || e.s === 'm', `${id}: source`);
  assert(typeof e.q === 'number' && e.q >= 0 && e.q <= 1 && Math.abs(Math.round(e.q * 100) - e.q * 100) < 1e-9 && String(e.q).replace(/^\d\.?/, '').length <= 2, `${id}: q`);
  assert(typeof e.d === 'string' && e.d.length > 0, `${id}: markup`);
  assert(!/<script/i.test(e.d) && !/\son[a-z]+\s*=/i.test(e.d) && !/href/i.test(e.d) && !/style/i.test(e.d), `${id}: unsafe markup`);
  assert(!/<svg|<!--|<g[\s>]/.test(e.d), `${id}: inner geometry only`);
  assert.equal(e.d.replace(ELEMENT, ''), '', `${id}: only geometry elements`);
  for (const m of e.d.matchAll(ELEMENT)) {
    for (const [, attr] of m[2].matchAll(/([a-z0-9]+)="/g)) assert(GEOMETRY.has(attr), `${id}: attribute ${attr}`);
  }
  if (e.s === 'm') assert(/^<path d="[^"]+"\/>$/.test(e.d), `${id}: MDI glyphs are single paths`);
  names.add(e.n);
  markups.add(e.d);
}
assert.equal(names.size, 2066, 'all glyph names distinct');
assert.equal(markups.size, 2066, 'all glyph geometries distinct');
const sourceCounts = entries.reduce((acc, [, e]) => (acc[e.s] = (acc[e.s] || 0) + 1, acc), {});
assert(sourceCounts.t > sourceCounts.m, 'Tabler is the primary source');

// ---- licenses, styles and bundler compatibility ----------------------------------------------
const licenses = read('../public/academy/assets/icons/LICENSES.md');
assert(/MIT License/.test(licenses) && /Apache License/.test(licenses) && /selected and assigned/.test(licenses));
const css = read('../public/academy/hero-icons.css');
for (const needle of ['.icon-wall', '.icon-tile', ':focus-visible', ':root[data-theme="dark"]', 'prefers-reduced-motion', 'var(--ink', 'var(--line', '.is-swapping'])
  assert(css.includes(needle), `hero-icons.css: ${needle}`);
const source = read('../public/academy/project-icons.js');
assert(!/export\s+default|export\s*\*|\bimport\s*\(/.test(source), 'offline bundler: named exports only, no dynamic import');
assert(!/^import\s/m.test(source) || /^import\s*\{[^}]+\}\s*from\s*['"]\.\.?\//m.test(source), 'relative named imports only');
for (const name of ['loadProjectIcons', 'projectGlyph', 'heroIconWallMarkup', 'mountHeroIconWall'])
  assert(new RegExp(`^export function ${name}\\(`, 'm').test(source), `export function ${name}`);

// ---- projectGlyph ------------------------------------------------------------------------------
function wellFormed(svg) {
  const stack = [];
  for (const m of svg.matchAll(/<(\/?)([a-z]+)\b[^>]*?(\/?)>/g)) {
    if (m[1]) assert.equal(stack.pop(), m[2], `balanced </${m[2]}>`);
    else if (!m[3]) stack.push(m[2]);
  }
  assert.equal(stack.length, 0, 'all tags closed');
  return true;
}
const tablerEntry = entries.find(([, e]) => e.s === 't')[1];
const mdiEntry = entries.find(([, e]) => e.s === 'm')?.[1];
const g1 = projectGlyph(tablerEntry);
assert(g1.startsWith('<svg ') && g1.endsWith('</svg>') && wellFormed(g1));
assert(g1.includes('viewBox="0 0 24 24"') && g1.includes('stroke-width="1.75"') && g1.includes('fill="none"'));
assert(g1.includes('stroke-linecap="round"') && g1.includes('stroke-linejoin="round"') && g1.includes('aria-hidden="true"'));
assert(g1.includes('width="24"') && !g1.includes('role="img"'));
if (mdiEntry) {
  const g2 = projectGlyph(mdiEntry, {size: 40});
  assert(wellFormed(g2) && g2.includes('fill="currentColor"') && !g2.includes('stroke=') && g2.includes('width="40"'));
}
const g3 = projectGlyph(tablerEntry, {label: 'A <b> & "c" \'d\''});
assert(g3.includes('role="img"') && g3.includes('aria-label="A &lt;b&gt; &amp; &quot;c&quot; &#39;d&#39;"') && !g3.includes('aria-hidden'));
const g4 = projectGlyph({n: 'evil', s: 't', d: '<path d="M0 0"/><script>alert(1)</script>'});
assert(wellFormed(g4) && !g4.includes('script'), 'tampered geometry falls back');
assert(!projectGlyph({s: 't', d: '<path d="M0 0" onload="x()"/>'}).includes('onload'));
for (const bad of [null, undefined, {}, 'x', 42]) assert(wellFormed(projectGlyph(bad)), 'missing entries render a fallback');
assert(wellFormed(projectGlyph(tablerEntry, {size: 'huge'})) && projectGlyph(tablerEntry, {size: 'huge'}).includes('width="24"'));
assert.equal(PROJECT_ICON_CATEGORY_LABELS.megascience[1], 'Megascience');
for (const [id, e] of entries) assert(projectGlyph(e).includes(`>${e.d}</svg>`), `${id}: stored geometry passes the renderer whitelist`);

// ---- heroIconWallMarkup ------------------------------------------------------------------------
const zhMarkup = heroIconWallMarkup(), enMarkup = heroIconWallMarkup({zh: false});
for (const m of [zhMarkup, enMarkup]) {
  assert(m.startsWith('<section class="icon-wall" data-icon-wall') && m.endsWith('</section>') && wellFormed(m));
  assert(m.includes('aria-live="polite"') && m.includes('data-icon-wall-grid') && m.includes('icon-wall-sr'));
}
assert(/[一-鿿]/.test(zhMarkup) && /cycles through/.test(enMarkup));

// ---- loadProjectIcons: fetch failure, fetch success, cache, offline preload ---------------------
let fetchCalls = 0;
globalThis.fetch = async () => { fetchCalls++; throw new Error('offline'); };
assert.deepEqual(await loadProjectIcons(), {}, 'failure resolves to {}');
globalThis.fetch = async url => { fetchCalls++; assert.equal(url, 'data/project-icons.json'); return {ok: true, json: async () => doc}; };
const loaded = await loadProjectIcons();
assert.equal(Object.keys(loaded).length, 2066);
assert.equal(await loadProjectIcons(), loaded, 'cached');
assert.equal(fetchCalls, 2);
assert.equal(getProjectIcon(ids[0]).n, doc.icons[ids[0]].n);
delete globalThis.fetch;
globalThis.MG_DATA = {'project-icons': doc};
const fresh = await import('../public/academy/project-icons.js?offline-preload');
assert.equal(Object.keys(await fresh.loadProjectIcons()).length, 2066, 'MG_DATA preload (file:// mode)');
delete globalThis.MG_DATA;

// ---- mountHeroIconWall against a tiny fake DOM ----------------------------------------------------
class FakeElement {
  constructor(tag, ownerDocument) {
    this.tagName = tag.toUpperCase(); this.ownerDocument = ownerDocument; this.children = []; this.parentNode = null;
    this.attributes = new Map(); this.listeners = new Map(); this._text = ''; this._html = ''; this.clientWidth = 0;
    const set = new Set();
    this.classList = {add: c => set.add(c), remove: c => set.delete(c), contains: c => set.has(c),
      toggle: (c, force) => ((force ?? !set.has(c)) ? set.add(c) : set.delete(c), set.has(c))};
    this._classes = set;
    this.style = {props: {}, setProperty(k, v) { this.props[k] = v; }};
  }
  set className(v) { this._classes.clear(); String(v).split(/\s+/).filter(Boolean).forEach(c => this._classes.add(c)); }
  get className() { return [...this._classes].join(' '); }
  setAttribute(k, v) { this.attributes.set(k, String(v)); }
  getAttribute(k) { return this.attributes.has(k) ? this.attributes.get(k) : null; }
  hasAttribute(k) { return this.attributes.has(k); }
  appendChild(el) { el.parentNode = this; this.children.push(el); return el; }
  set textContent(v) { this.children = []; this._html = ''; this._text = String(v); }
  get textContent() { return this._text + this.children.map(c => c.textContent).join(''); }
  set innerHTML(v) { this.children = []; this._text = ''; this._html = String(v); }
  get innerHTML() { return this._html; }
  matches(sel) { const m = /^\[([\w-]+)\]$/.exec(sel); return Boolean(m && this.attributes.has(m[1])); }
  querySelector(sel) { for (const c of this.children) { if (c.matches(sel)) return c; const f = c.querySelector(sel); if (f) return f; } return null; }
  contains(el) { for (let n = el; n; n = n.parentNode) if (n === this) return true; return false; }
  addEventListener(type, fn) { (this.listeners.get(type) || this.listeners.set(type, new Set()).get(type)).add(fn); }
  removeEventListener(type, fn) { this.listeners.get(type)?.delete(fn); }
  dispatch(type, event = {}) { for (const fn of [...(this.listeners.get(type) || [])]) fn(event); }
  listenerCount() { return [...this.listeners.values()].reduce((n, s) => n + s.size, 0); }
}
class FakeDocument extends FakeElement {
  constructor() { super('#document', null); this.hidden = false; }
  createElement(tag) { return new FakeElement(tag, this); }
}
const observers = [];
globalThis.ResizeObserver = class { constructor(cb) { this.cb = cb; this.disconnected = false; observers.push(this); } observe(el) { this.el = el; } disconnect() { this.disconnected = true; } };

function tilesOf(root) { return root.querySelector('[data-icon-wall-grid]').children; }
const shownIds = root => tilesOf(root).map(t => t.getAttribute('data-project-id'));

// desktop width: 36 tiles, links, labels, rotation, caption, distinct
{
  const document = new FakeDocument();
  const root = document.createElement('div');
  root.clientWidth = 1100;
  const wall = mountHeroIconWall(root, catalog, {icons: doc.icons, reducedMotion: false, interval: 25, seed: 7});
  const tiles = tilesOf(root);
  assert.equal(tiles.length, 36, 'desktop wall has 36 tiles');
  const section = root.querySelector('[data-icon-wall]');
  assert.equal(section.style.props['--icon-wall-cols'], '12');
  for (const t of tiles) {
    const id = t.getAttribute('data-project-id');
    assert.equal(t.tagName, 'A'); assert(t.classList.contains('icon-tile'));
    assert.equal(t.getAttribute('href'), `#project/${encodeURIComponent(id)}`);
    assert(t.getAttribute('title').length > 0);
    assert(t.innerHTML.startsWith('<svg') && t.innerHTML.includes('class="icon-tile-label"') && t.innerHTML.includes('aria-hidden="true"'));
  }
  assert.equal(new Set(shownIds(root)).size, 36);
  const before = shownIds(root).join();
  await sleep(220);
  const after = shownIds(root);
  assert.notEqual(after.join(), before, 'tiles rotate');
  assert.equal(new Set(after).size, after.length, 'no duplicates on the wall');
  const caption = root.querySelector('[data-icon-wall-caption]');
  assert.equal(caption.getAttribute('aria-live'), 'polite');
  assert.equal(caption.children.length, 2);
  assert(caption.children[0].textContent.length > 0 && Object.values(PROJECT_ICON_CATEGORY_LABELS).some(l => l[0] === caption.children[1].textContent));
  // pause on hover and focus
  section.dispatch('pointerenter');
  await sleep(60);
  const hovered = shownIds(root).join();
  await sleep(120);
  assert.equal(shownIds(root).join(), hovered, 'paused while hovered');
  section.dispatch('pointerleave');
  section.dispatch('focusin');
  await sleep(60);
  const focusedIds = shownIds(root).join();
  await sleep(120);
  assert.equal(shownIds(root).join(), focusedIds, 'paused while focused');
  section.dispatch('focusout', {relatedTarget: null});
  // hidden document pauses
  document.hidden = true; document.dispatch('visibilitychange');
  await sleep(60);
  const hiddenIds = shownIds(root).join();
  await sleep(120);
  assert.equal(shownIds(root).join(), hiddenIds, 'paused while document.hidden');
  document.hidden = false; document.dispatch('visibilitychange');
  await sleep(150);
  assert.notEqual(shownIds(root).join(), hiddenIds, 'resumes when visible');
  // resize to phone and tablet
  const ro = observers.at(-1);
  root.clientWidth = 360; ro.cb([]);
  assert.equal(tilesOf(root).length, 12, 'phone wall has 12 tiles');
  root.clientWidth = 700; ro.cb([]);
  assert.equal(tilesOf(root).length, 24, 'tablet wall has 24 tiles');
  assert.equal(new Set(shownIds(root)).size, 24);
  wall.dispose();
  assert(ro.disconnected, 'observer disconnected');
  assert.equal(section.listenerCount() + document.listenerCount(), 0, 'listeners removed');
  await sleep(80);
  const frozen = shownIds(root).join();
  await sleep(150);
  assert.equal(shownIds(root).join(), frozen, 'dispose stops the rotation');
  assert(tilesOf(root).every(t => !t.classList.contains('is-swapping')));
  wall.dispose();
}

// every project of the permutation appears over time (small catalog)
{
  const document = new FakeDocument();
  const root = document.createElement('div');
  root.clientWidth = 300;
  const small = catalog.slice(0, 50);
  const seen = new Set();
  const wall = mountHeroIconWall(root, small, {icons: doc.icons, reducedMotion: false, interval: 20, seed: 3});
  for (let i = 0; i < 60 && seen.size < 50; i++) { shownIds(root).forEach(id => seen.add(id)); await sleep(20); }
  wall.dispose();
  assert.equal(seen.size, 50, 'every project appears on the wall over time');
}

// existing markup is reused; reduced motion renders a static set
{
  const document = new FakeDocument();
  const section = document.createElement('section');
  section.setAttribute('data-icon-wall', '');
  const grid = section.appendChild(document.createElement('div')); grid.setAttribute('data-icon-wall-grid', '');
  const cap = section.appendChild(document.createElement('p')); cap.setAttribute('data-icon-wall-caption', '');
  section.clientWidth = 1000;
  const wall = mountHeroIconWall(section, catalog, {zh: false, icons: doc.icons, reducedMotion: true, interval: 20, seed: 1});
  assert.equal(grid.children.length, 36);
  assert(section.classList.contains('is-static'));
  const ids0 = shownIds(section).join();
  await sleep(120);
  assert.equal(shownIds(section).join(), ids0, 'reduced motion: static');
  assert(Object.values(PROJECT_ICON_CATEGORY_LABELS).some(l => l[1] === cap.children[1].textContent), 'English caption');
  wall.dispose();
}

// robustness: empty or missing inputs never throw
{
  const document = new FakeDocument();
  const root = document.createElement('div');
  for (const [cat, icons] of [[[], {}], [null, undefined], [catalog.slice(0, 5), {}], [[{id: 'x'}, null, {id: 'x'}], null]]) {
    const w = mountHeroIconWall(root, cat, {icons: icons || {}, reducedMotion: false, interval: 20});
    await sleep(30);
    w.dispose();
  }
  assert.equal(tilesOf(root).length, 1, 'deduplicated tiny catalog');
  assert.doesNotThrow(() => mountHeroIconWall(null, catalog).dispose());
  assert.doesNotThrow(() => mountHeroIconWall({}, catalog).dispose());
}
delete globalThis.ResizeObserver;

console.log(`project icons ok (${entries.length} projects, tabler ${sourceCounts.t}, mdi ${sourceCounts.m || 0}, ${(Buffer.byteLength(raw) / 1024).toFixed(1)} KB)`);
