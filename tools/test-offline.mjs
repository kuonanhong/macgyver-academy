// Executes the delivered classic bootstrap + bundle with all native fetch denied.
// This verifies packaging/runtime behavior, not browser layout or file:// policy.
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { webcrypto } from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const publicRoot = path.join(root, 'public/academy');
const checked = spawnSync(process.execPath, [path.join(root, 'tools/build-offline.mjs'), '--check'], { encoding: 'utf8' });
assert.equal(checked.status, 0, checked.stdout + checked.stderr);
const manifest = JSON.parse(fs.readFileSync(path.join(publicRoot, 'offline-build.json'), 'utf8'));
const expectedData = fs.readdirSync(path.join(publicRoot, 'data')).filter(n => n.endsWith('.json')).map(n => n.slice(0, -5)).sort();
assert.deepEqual(manifest.dataSets, expectedData, 'every public JSON is embedded');
assert(!fs.readFileSync(path.join(publicRoot, 'index.html'), 'utf8').includes('type="module"'), 'file entry must use classic scripts');
assert(!fs.readFileSync(path.join(root, 'index.html'), 'utf8').includes('<iframe'), 'root launcher must not trap keyboard focus in an iframe');

function browser({ protocol = 'file:', denied = false, storage = new Map() } = {}) {
  let nativeRequests = 0, context;
  const scripts = [], listeners = new Map(), eventHandlers = new Map(), fixed = new Map(), mounted = new Map();
  function addListener(type, fn) {
    if (!eventHandlers.has(type)) eventHandlers.set(type, new Set());
    eventHandlers.get(type).add(fn);
    listeners.set(type, event => { for (const handler of [...eventHandlers.get(type)]) handler(event); });
  }
  function removeListener(type, fn) { eventHandlers.get(type)?.delete(fn); }
  function el(id = '') {
    const attrs = new Map();
    const node = { id, dataset: {}, value: '', disabled: false, textContent: '', style: {}, tagName: 'DIV',
      setAttribute(k, v) { attrs.set(k, String(v)); }, getAttribute(k) { return attrs.get(k) ?? null; }, hasAttribute(k) { return attrs.has(k); },
      classList: { add() {}, remove() {}, toggle() {} }, focus() {}, scrollIntoView() {}, showModal() {}, close() {}, addEventListener() {}, removeEventListener() {},
      querySelector() { return null; }, querySelectorAll() { return []; }, getBoundingClientRect() { return { width: 400, height: 304 }; },
      append() {}, replaceChildren() { this.innerHTML = ''; }, setSelectionRange() {}, setPointerCapture() {} };
    let html = '';
    Object.defineProperty(node, 'innerHTML', { get: () => html, set(value) {
      html = value;
      if (id === 'main' || id === 'dialogBody') {
        if (id === 'main') mounted.clear();
        for (const match of value.matchAll(/<([a-z][\w-]*)\b([^>]*)>/gi)) {
          const item = el(); item.tagName = match[1].toUpperCase();
          for (const a of match[2].matchAll(/([\w:-]+)(?:=(?:"([^"]*)"|'([^']*)'|([^\s>]+)))?/g)) {
            const name = a[1], val = a[2] ?? a[3] ?? a[4] ?? '';
            if (name === 'id') { item.id = val; mounted.set(val, item); }
            else if (name === 'disabled') item.disabled = true;
            else if (name === 'value') item.value = val;
            else if (name.startsWith('data-')) item.dataset[name.slice(5).replace(/-([a-z])/g, (_, c) => c.toUpperCase())] = val;
          }
        }
      }
    } });
    return node;
  }
  for (const id of ['main', 'toast', 'pageTitle', 'accountName', 'language', 'dialog', 'dialogTitle', 'dialogBody', 'sidebar', 'menu', 'guideButton', 'mentorButton', 'account', 'closeDialog', 'translateButton', 'preferencesButton']) fixed.set(id, el(id));
  const skip = el('skip');
  const document = {
    body: null, documentElement: {dataset:{}}, activeElement: null, hidden: false,
    querySelector(s) { return s === '.skip' ? skip : s.startsWith('#') ? mounted.get(s.slice(1)) || fixed.get(s.slice(1)) || null : null; },
    querySelectorAll(s) { const match = s.match(/^\[data-([\w-]+)\]$/); if (!match) return []; const key = match[1].replace(/-([a-z])/g, (_, c) => c.toUpperCase()); return [...mounted.values()].filter(n => key in n.dataset); },
    getElementById(id) { return mounted.get(id) || fixed.get(id) || null; },
    addEventListener() {}, removeEventListener() {}, createElement: () => el(),
    head: { appendChild(script) {
      scripts.push(script.src);
      queueMicrotask(() => { try { vm.runInContext(fs.readFileSync(path.join(publicRoot, script.src), 'utf8'), context, { filename: script.src }); script.onload?.(); } catch (error) { script.onerror?.(error); throw error; } });
    } }
  };
  const storageAPI = { get length() { return storage.size; }, key: i => [...storage.keys()][i] ?? null, getItem: k => storage.get(String(k)) ?? null, setItem: (k, v) => storage.set(String(k), String(v)), removeItem: k => storage.delete(String(k)), clear: () => storage.clear() };
  const globals = { console, Date, JSON, URL, Response, Request, Blob, AbortController, crypto: webcrypto, NodeFilter: { SHOW_TEXT: 4 },
    setTimeout: () => 1, clearTimeout() {}, setInterval: () => 1, clearInterval() {}, queueMicrotask,
    navigator: { languages: ['en'], language: 'en' }, location: { protocol, href: protocol === 'file:' ? 'file:///unpacked%20folder/public/academy/index.html' : 'https://example.test/academy/index.html', hash: '#home' },
    document, scrollTo() {}, matchMedia: () => ({ matches: false }), addEventListener: addListener, removeEventListener: removeListener,
    fetch: async () => { nativeRequests++; throw new Error('Native network is forbidden in the offline test'); } };
  Object.defineProperty(globals, 'localStorage', { configurable: true, get() { if (denied) throw new Error('SecurityError: file storage denied'); return storageAPI; } });
  globals.window = globals; globals.globalThis = globals;
  context = vm.createContext(globals);
  const run = source => vm.runInContext(source, context);
  return { context, run, scripts, storage, fixed, mounted, listeners, get nativeRequests() { return nativeRequests; } };
}
const flush = async () => { for (let i = 0; i < 20; i++) await new Promise(resolve => setImmediate(resolve)); };
async function boot(options) {
  const instance = browser(options);
  instance.run(fs.readFileSync(path.join(publicRoot, 'bootstrap.js'), 'utf8'));
  await flush();
  assert.deepEqual(instance.scripts, ['config.js', 'runtime-mode.js', 'offline-data.js', ...manifest.offlineParts, 'offline-runtime.js', 'app.bundle.js']);
  const html = instance.fixed.get('main').innerHTML;
  assert(/class="[^"]*\bexplorer-hero\b[^"]*"/.test(html) && html.includes('data-catalog-route="ready"') && !html.includes('Unable to load curriculum'), 'the complete classic bundle renders the merged explorer: ' + html.slice(0, 900));
  assert.equal(instance.nativeRequests, 0);
  return instance;
}
const app = await boot();
const api = app.context.MacGyverOffline;
assert.equal(api.storageAvailable, true);
const first = api.activeProfile();
const me = await (await app.context.fetch('/api/me')).json();
assert.equal(me.authMode, 'offline'); assert.equal(me.aiAvailable, false); assert.equal(me.user.id, first.id);
assert.equal(app.context.MG_DATA.catalog.length, app.context.MG_DATA.release.topics); assert.equal(app.context.MG_DATA.featured.length, app.context.MG_DATA.release.guidedCourses);
assert(!Object.hasOwn(app.context.MG_DATA, 'materials'), 'removed private-material index is absent from the offline bundle');
for (const key of expectedData) assert.deepEqual(JSON.parse(JSON.stringify(app.context.MG_DATA[key])), JSON.parse(fs.readFileSync(path.join(publicRoot, 'data', `${key}.json`), 'utf8')));
const put = async body => app.context.fetch('/api/progress', { method: 'PUT', body: JSON.stringify(body) });
const payload = { projectId: 'semiconductor', completed: ['sc-001'], assembly: ['sc-001'], notes: 'Offline evidence <script>literal</script>', baseUpdatedAt: null };
let response = await put(payload); assert.equal(response.status, 200); const saved = await response.json();
response = await put({ ...payload, notes: 'stale overwrite' }); assert.equal(response.status, 409); assert.equal((await response.json()).current.notes, payload.notes);
response = await put({ ...payload, notes: 'Reviewed evidence', baseUpdatedAt: saved.updatedAt }); assert.equal(response.status, 200); assert((await response.json()).updatedAt > saved.updatedAt);
const second = api.createProfile('第二位學徒'); assert.notEqual(second.id, first.id);
assert.deepEqual((await (await app.context.fetch('/api/progress')).json()).projects, {});
await put({ ...payload, notes: 'Second profile only' });
api.switchProfile(first.id);
assert.equal((await (await app.context.fetch('/api/progress')).json()).projects.semiconductor.notes, 'Reviewed evidence');
// Progress JSON exports/imports use these same scoped rows; restoring a backup
// into a third profile must not overwrite either original local learner.
const exported = (await (await app.context.fetch('/api/progress')).json()).projects;
api.createProfile('Imported backup');
for (const [projectId, row] of Object.entries(exported)) assert.equal((await put({ projectId, ...row, baseUpdatedAt: null })).status, 200);
api.switchProfile(second.id); assert.equal((await (await app.context.fetch('/api/progress')).json()).projects.semiconductor.notes, 'Second profile only');
api.switchProfile(first.id);
for (const projectId of ['__proto__', 'constructor', 'prototype', '../escape']) assert.equal((await put({ ...payload, projectId })).status, 400);
assert.equal((await app.context.fetch('https://example.com/api')).status, 503);
assert.equal((await app.context.fetch('/api/tutor', { method: 'POST' })).status, 503);
assert.equal((await app.context.fetch('data/not-in-package.json')).status, 404);
assert.equal(app.nativeRequests, 0);
// Reload the actual boot path and then visit the workbench; no HTTP server or
// ES module loader participates in either render.
const reloaded = await boot({ storage: app.storage });
assert.equal(reloaded.context.MacGyverOffline.activeProfile().id, first.id);
reloaded.fixed.get('account').onclick();
assert(reloaded.fixed.get('dialogBody').innerHTML.includes('offlineProfileForm'), 'offline account opens local profiles');
assert(!reloaded.fixed.get('dialogBody').innerHTML.includes('/signout-with-chatgpt'), 'offline profile never offers a cloud logout');
reloaded.context.location.hash = '#workshop'; reloaded.listeners.get('hashchange')(); await flush();
assert(reloaded.fixed.get('main').innerHTML.includes('learnerModel'), 'direct-file workbench renders');
assert(reloaded.fixed.get('main').innerHTML.includes('mentorModel'), 'teacher workbench renders');
const notes = reloaded.mounted.get('notes');
notes.value = 'Actual workbench note saved with no server'; notes.oninput();
let extraRouteEvents = 0; const extraRouteListener = () => { extraRouteEvents++; };
reloaded.context.addEventListener('hashchange', extraRouteListener);
reloaded.context.location.hash = '#progress'; reloaded.listeners.get('hashchange')(); await flush();
assert.equal((await (await reloaded.context.fetch('/api/progress')).json()).projects.semiconductor.notes, notes.value, 'real app note handler saves through the offline bridge');
assert.equal(extraRouteEvents, 1, 'route dispatch calls both app and additional subscribers');
reloaded.context.removeEventListener('hashchange', extraRouteListener);
assert.equal(reloaded.nativeRequests, 0);
const denied = await boot({ denied: true });
assert.equal(denied.context.MacGyverOffline.storageAvailable, false, 'storage denial is honest session-only mode');
const deniedSaved = await denied.context.fetch('/api/progress', { method: 'PUT', body: JSON.stringify(payload) }); assert.equal(deniedSaved.status, 200); assert.equal((await deniedSaved.json()).storageAvailable, false);
const hosted = browser({ protocol: 'https:' }); const native = hosted.context.fetch;
hosted.run(fs.readFileSync(path.join(publicRoot, 'offline-runtime.js'), 'utf8'));
assert.equal(hosted.context.fetch, native, 'hosted authentication and APIs remain untouched');
assert.equal(hosted.context.MacGyverOffline, undefined);
console.log(`PASS offline: ${expectedData.length} complete embedded data sets, classic full-app home/workbench boot, zero native fetches, 3 isolated profiles, reload, backup restore, CAS, invalid inputs, denied-storage fallback, hosted no-op.`);
