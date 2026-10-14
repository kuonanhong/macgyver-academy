// Deterministic integration checks for the locale controller's external contract.
// DOM fixtures model text/attribute mutation; this does not test browser layout.
import assert from 'node:assert/strict';
import {
  createLocaleController,
  resolveSupportedLanguage,
  languageDirection,
} from '../public/academy/locale.js';

const storage = new Map();
globalThis.localStorage = {
  getItem: key => storage.get(key) || null,
  setItem: (key, value) => storage.set(key, value),
  removeItem: key => storage.delete(key),
};

function textNode(value, excludedSelector = '') {
  return {
    nodeValue: value,
    isConnected: true,
    parentElement: {
      closest: selector => excludedSelector && selector.includes(excludedSelector) ? {} : null,
    },
  };
}
function attributeElement(attributes) {
  return {
    attributes,
    isConnected: true,
    closest: () => null,
    getAttribute(name) { return this.attributes[name] ?? null; },
    setAttribute(name, value) { this.attributes[name] = value; },
    hasAttribute(name) { return name in this.attributes; },
  };
}
function root(nodes, elements = []) {
  return {
    nodeType: 11,
    ownerDocument: {
      createTreeWalker() {
        let index = 0;
        return { nextNode: () => nodes[index++] || null };
      },
    },
    querySelectorAll: () => elements,
  };
}

// Regional negotiation must preserve the Chinese writing system and find the
// supported base of other regional locales, using browser preference order.
for (const [locale, expected] of [
  ['zh-Hant', 'zh-TW'], ['zh-HK', 'zh-TW'], ['zh-Hans', 'zh-CN'],
  ['zh-SG', 'zh-CN'], ['zh-Hant-CN', 'zh-TW'], ['fr-CA', 'fr'],
  ['pt-BR', 'pt'], ['ar-EG', 'ar'], ['iw-IL', 'he'],
  ['tl-PH', 'fil'], ['nb-NO', 'no'],
]) assert.equal(resolveSupportedLanguage('auto', { languages: [locale] }), expected);
assert.equal(resolveSupportedLanguage('zz', { languages: ['zz', 'ja-JP', 'en'] }), 'ja');
assert.equal(resolveSupportedLanguage('de', { languages: ['fr-FR'] }), 'de');
assert.equal(languageDirection('ar-EG'), 'rtl');
assert.equal(languageDirection('az-Arab'), 'rtl');
assert.equal(languageDirection('ar-Latn'), 'ltr');
assert.equal(languageDirection('zh-TW'), 'ltr');

const requests = [];
globalThis.fetch = async (url, options) => {
  assert.equal(url, '/api/translate');
  assert.equal(options.method, 'POST');
  assert.equal(options.credentials, 'same-origin');
  const payload = JSON.parse(options.body);
  requests.push(payload);
  return {
    ok: true,
    json: async () => ({ translations: payload.texts.map(source => `${payload.language}:${source}`) }),
  };
};

let language = 'fr';
let online = true;
const controller = createLocaleController({
  getLanguage: () => language,
  getAIAvailable: () => online,
});
const hello = textNode(' Hello ');
const duplicate = textNode('Hello');
const secret = textNode('private engineering notes', 'textarea');
const code = textNode('npm run build', 'code');
const optedOut = textNode('Never upload this text', '[data-no-translate]');
const input = attributeElement({
  placeholder: 'Search projects', title: 'Search projects', 'aria-label': 'Search projects',
});
input.value = 'A private typed value';
const tree = root([hello, duplicate, secret, code, optedOut], [input]);
await controller.apply(tree);
assert.equal(hello.nodeValue, ' fr:Hello ');
assert.equal(duplicate.nodeValue, 'fr:Hello');
assert.equal(secret.nodeValue, 'private engineering notes');
assert.equal(code.nodeValue, 'npm run build');
assert.equal(optedOut.nodeValue, 'Never upload this text');
assert.equal(input.value, 'A private typed value');
assert.equal(input.attributes.placeholder, 'fr:Search projects');
assert.equal(input.attributes.title, 'fr:Search projects');
assert.equal(input.attributes['aria-label'], 'fr:Search projects');
assert.deepEqual(requests[0].texts, ['Hello', 'Search projects']);

// Repeat passes and target changes must always use canonical source strings.
await controller.apply(tree);
assert.equal(requests.length, 1, 'a second pass must use the cache');
language = 'de';
await controller.apply(tree);
assert.deepEqual(requests[1].texts, ['Hello', 'Search projects']);
assert.equal(hello.nodeValue, ' de:Hello ');
language = 'en';
await controller.apply(tree);
assert.equal(hello.nodeValue, ' Hello ');
assert.equal(input.attributes.placeholder, 'Search projects');

// A fresh controller must reuse persisted translations even without AI access.
language = 'fr';
online = false;
const offline = createLocaleController({ getLanguage: () => language, getAIAvailable: () => false });
const offlineHello = textNode('Hello');
await offline.apply(root([offlineHello]));
assert.equal(offlineHello.nodeValue, 'fr:Hello');
assert.equal(offline.stats().status.state, 'cached');
const uncached = textNode('Not cached');
await offline.apply(root([uncached]));
assert.equal(uncached.nodeValue, 'Not cached');
assert.equal(offline.stats().status.state, 'unavailable');

// Larger renders must respect both limits, including a single long text node.
online = true;
const start = requests.length;
await controller.apply(root(Array.from({ length: 27 }, (_, index) => textNode(`Text ${index}`))));
assert.equal(requests.length - start, 3);
const long = textNode('Science is useful. '.repeat(350));
await controller.apply(root([long]));
for (const request of requests.slice(start)) {
  assert(request.texts.length <= 12);
  assert(request.texts.join('').length <= 4000);
  assert(request.texts.every(source => source.length <= 2900));
}
assert(!long.nodeValue.includes('undefined'));

// Route changes must prevent an old request from writing to a stale render.
let resolveFetch;
globalThis.fetch = () => new Promise(resolve => { resolveFetch = resolve; });
const stale = textNode('Stale text');
const pending = controller.apply(root([stale]));
controller.invalidate();
stale.isConnected = false;
resolveFetch({ ok: true, json: async () => ({ translations: ['WRONG'] }) });
await pending;
assert.equal(stale.nodeValue, 'Stale text');

// A failed later batch retains earlier translations and exposes readable source.
let round = 0;
globalThis.fetch = async (url, options) => {
  const payload = JSON.parse(options.body);
  return ++round === 1
    ? { ok: true, json: async () => ({ translations: payload.texts.map(source => `X:${source}`) }) }
    : { ok: false, status: 503 };
};
const partial = Array.from({ length: 20 }, (_, index) => textNode(`Partial ${index}`));
const result = await controller.apply(root(partial));
assert.equal(result.state, 'partial');
assert.equal(result.translated, 12);
assert.equal(result.failed, 8);
assert.equal(partial[15].nodeValue, 'Partial 15');

// Loading an oversized persisted cache must not exceed the documented bounds.
localStorage.setItem('mg-translation-cache-v2', JSON.stringify({
  version: 2,
  entries: Array.from({ length: 3200 }, (_, index) => [`fr\u0000Cached ${index}`, `Traduit ${index}`]),
}));
const bounded = createLocaleController();
assert.equal(bounded.stats().entries, 3000);
assert(bounded.stats().characters <= 1000000);

console.log(JSON.stringify({
  passed: true,
  checks: [
    'regional negotiation and RTL', 'deduplication', 'translated attributes',
    'private values and opt-out', 'canonical source tracking', 'core restoration',
    'persistent offline cache', 'bounded batches and long text',
    'stale request cancellation', 'partial failure fallback', 'cache bounds',
  ],
  limitations: 'Controlled DOM fixtures exercise controller behavior; browser layout and live AI are not covered.',
}, null, 2));
