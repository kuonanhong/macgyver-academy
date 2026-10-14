/** Whole-interface, opt-in machine translation with a bounded offline cache.
 * App renders its canonical English (or core Traditional Chinese) first, calls
 * invalidate() before rendering, and calls apply() after rendering / opening a
 * dialog or details element. Mark private/user-generated content and language
 * names with data-no-translate. No form values are read or sent to the service.
 */
const SUPPORTED = 'zh-TW en zh-CN ja ko es fr de pt it nl ru uk pl cs sk sl hr sr bg ro hu el tr ar he fa ur hi bn ta te mr gu kn ml pa ne si th vi id ms fil km lo my mn kk uz az ka hy sw am ha yo ig zu af so sv no da fi is et lv lt ga cy mt sq mk bs eu gl ca eo'.split(' ');
const CACHE_KEY = 'mg-translation-cache-v2';
const MAX_ENTRIES = 3000;
const MAX_CACHE_CHARS = 1000000;
const MAX_TEXT_CHARS = 2900;
const MAX_BATCH_CHARS = 4000;
const MAX_BATCH_SIZE = 12;
const TIMEOUT_MS = 45000;
const ATTRIBUTES = ['placeholder', 'title', 'aria-label'];
const NEVER_TRANSLATE = '[data-no-translate],[translate="no"],[data-private],script,style,noscript,template,code,pre,textarea,[contenteditable]:not([contenteditable="false"]),#language,#translationLanguage,#notes,#researchNotes,#question,#answer,#accountName';

function tag(value) {
  const parts = String(value || '').trim().replaceAll('_', '-').split('-');
  const aliases = { iw: 'he', in: 'id', tl: 'fil', nb: 'no', nn: 'no' };
  parts[0] = aliases[parts[0].toLowerCase()] || parts[0].toLowerCase();
  return parts.join('-');
}

/** Resolve BCP-47 preferences against supported codes. Choice entries can be
 * strings, [code, label] pairs, or {value/code/id, ...} objects. Browser locales
 * are considered in order; an unsupported manual choice falls back to them.
 */
export function resolveSupportedLanguage(preference = 'auto', browser, choices = SUPPORTED) {
  const available = Array.from(choices || SUPPORTED, item => typeof item === 'string' ? item : Array.isArray(item) ? item[0] : item?.value || item?.code || item?.id).filter(Boolean);
  const codes = available.length ? available : SUPPORTED;
  const exact = candidate => codes.find(code => tag(code).toLowerCase() === candidate.toLowerCase());
  const match = value => {
    const candidate = tag(value);
    if (!candidate || candidate === 'auto') return null;
    const direct = exact(candidate);
    if (direct) return direct;
    const bits = candidate.toLowerCase().split('-');
    const base = bits[0];
    if (base === 'zh') {
      const traditional = bits.includes('hant') || (!bits.includes('hans') && bits.some(v => ['tw', 'hk', 'mo'].includes(v))) || bits.length === 1;
      return (traditional ? exact('zh-TW') || exact('zh-Hant') : exact('zh-CN') || exact('zh-Hans')) || exact('zh') || null;
    }
    return exact(base) || codes.find(code => tag(code).toLowerCase().split('-')[0] === base) || null;
  };
  const environment = browser === undefined ? (typeof navigator !== 'undefined' ? navigator : {}) : browser || {};
  const manual = Array.isArray(preference) ? preference : preference && preference !== 'auto' ? [preference] : [];
  const browserPreferences = Array.isArray(environment) ? environment : typeof environment === 'string' ? [environment] : [...(environment.languages || []), environment.language].filter(Boolean);
  for (const candidate of [...manual, ...browserPreferences]) {
    const found = match(candidate);
    if (found) return found;
  }
  return exact('en') || codes[0];
}

export function languageDirection(language) {
  const bits = tag(language).toLowerCase().split('-');
  if (bits.includes('latn')) return 'ltr';
  return bits.includes('arab') || ['ar', 'he', 'fa', 'ur', 'ps', 'sd', 'ug', 'yi', 'dv'].includes(bits[0]) ? 'rtl' : 'ltr';
}

function splitText(raw) {
  const chunks = [];
  let remaining = raw;
  while (remaining.length > MAX_TEXT_CHARS) {
    let boundary = Math.max(remaining.lastIndexOf('\n', MAX_TEXT_CHARS), remaining.lastIndexOf(' ', MAX_TEXT_CHARS));
    if (boundary < MAX_TEXT_CHARS / 2) boundary = MAX_TEXT_CHARS;
    // Never cut a UTF-16 surrogate pair in half.
    if (/[\uD800-\uDBFF]/.test(remaining[boundary - 1])) boundary--;
    chunks.push(remaining.slice(0, boundary));
    remaining = remaining.slice(boundary);
  }
  if (remaining) chunks.push(remaining);
  return chunks.map(chunk => {
    const leading = chunk.match(/^\s*/)[0];
    const trailing = chunk.match(/\s*$/)[0];
    const text = chunk.trim();
    return { text, leading, trailing: text ? trailing : '', translate: translatable(text) };
  });
}

function translatable(text) {
  return !!text && /\p{L}/u.test(text) && !/^https?:\/\/\S+$/i.test(text) && !/\b[^\s@]+@[^\s@]+\.[^\s@]+\b/.test(text);
}

function hiddenOrExcluded(element, attributes = false) {
  if (!element) return true;
  // Textareas contain private notes. Their prompts can still be translated.
  let selector = NEVER_TRANSLATE;
  if (attributes) selector = selector.replace(',textarea', '').replace(',#notes', '').replace(',#researchNotes', '').replace(',#question', '');
  if (element.closest(selector) || element.closest('[hidden],dialog:not([open])')) return true;
  for (let details = element.closest('details:not([open])'); details; details = details.parentElement?.closest('details:not([open])')) {
    const summary = [...details.children].find(child => child.localName === 'summary');
    if (!summary || !summary.contains(element)) return true;
  }
  return false;
}

export function createLocaleController({ getLanguage = () => 'en', getAIAvailable = () => false, onStatus = () => {} } = {}) {
  const textSources = new WeakMap();
  const attributeSources = new WeakMap();
  const cache = new Map();
  let generation = 0;
  let activeRequest = null;
  let cacheChars = 0;
  let requests = 0;
  let storageAvailable = true;
  let latestStatus = { state: 'core', language: 'en', total: 0, translated: 0, pending: 0, cached: 0, failed: 0 };
  const keyFor = (language, source) => language + '\u0000' + source;
  const weight = (key, value) => key.length + value.length;

  function trimCache() {
    while (cache.size > MAX_ENTRIES || cacheChars > MAX_CACHE_CHARS) {
      const first = cache.entries().next().value;
      if (!first) break;
      cache.delete(first[0]);
      cacheChars -= weight(first[0], first[1]);
    }
  }
  function put(key, value) {
    if (cache.has(key)) { cacheChars -= weight(key, cache.get(key)); cache.delete(key); }
    cache.set(key, value);
    cacheChars += weight(key, value);
    trimCache();
  }
  function get(key) {
    const value = cache.get(key);
    if (value !== undefined) { cache.delete(key); cache.set(key, value); }
    return value;
  }
  function persist() {
    try {
      localStorage.setItem(CACHE_KEY, JSON.stringify({ version: 2, entries: [...cache] }));
      storageAvailable = true;
    } catch { storageAvailable = false; }
  }
  try {
    const saved = JSON.parse(localStorage.getItem(CACHE_KEY) || 'null');
    if (saved?.version === 2 && Array.isArray(saved.entries)) {
      for (const entry of saved.entries.slice(-MAX_ENTRIES)) {
        if (Array.isArray(entry) && entry.length === 2 && typeof entry[0] === 'string' && entry[0].includes('\u0000') && entry[0].length <= MAX_TEXT_CHARS + 60 && typeof entry[1] === 'string' && entry[1].trim() && entry[1].length <= 12000) put(entry[0], entry[1]);
      }
    }
  } catch { storageAvailable = false; }

  function invalidate() {
    generation++;
    activeRequest?.abort();
    activeRequest = null;
  }

  function collect(root) {
    const descriptors = [];
    const remember = (node, attribute = null) => {
      const current = attribute ? node.getAttribute(attribute) : node.nodeValue;
      if (!current || !current.trim()) return;
      let memory;
      if (attribute) {
        let attributes = attributeSources.get(node);
        if (!attributes) attributeSources.set(node, attributes = new Map());
        memory = attributes.get(attribute);
        if (!memory || (current !== memory.rendered && current !== memory.source)) attributes.set(attribute, memory = { source: current, rendered: current });
      } else {
        memory = textSources.get(node);
        if (!memory || (current !== memory.rendered && current !== memory.source)) textSources.set(node, memory = { source: current, rendered: current });
      }
      descriptors.push({ node, attribute, memory, current, parts: splitText(memory.source) });
    };
    const documentForRoot = root.ownerDocument || root;
    const walker = documentForRoot.createTreeWalker(root, 4 /* SHOW_TEXT */);
    let node;
    while ((node = walker.nextNode())) if (!hiddenOrExcluded(node.parentElement)) remember(node);
    const elements = root.querySelectorAll ? [...root.querySelectorAll('[placeholder],[title],[aria-label]')] : [];
    if (root.nodeType === 1 && ATTRIBUTES.some(attribute => root.hasAttribute(attribute))) elements.unshift(root);
    for (const element of elements) {
      if (hiddenOrExcluded(element, true)) continue;
      for (const attribute of ATTRIBUTES) if (element.hasAttribute(attribute)) remember(element, attribute);
    }
    return descriptors;
  }

  async function apply(root = document.body) {
    invalidate();
    const token = generation;
    const language = resolveSupportedLanguage(getLanguage(), {});
    const core = language === 'en' || language === 'zh-TW';
    const descriptors = root ? collect(root) : [];
    const texts = [...new Set(descriptors.flatMap(descriptor => descriptor.parts.filter(part => part.translate).map(part => part.text)))];
    const translations = new Map();
    if (!core) for (const source of texts) {
      const value = get(keyFor(language, source));
      if (value !== undefined) translations.set(source, value);
    }
    const cached = translations.size;
    let failed = 0;
    const cancelled = () => token !== generation;
    const report = (state, error) => {
      const status = { state, language, total: texts.length, translated: core ? texts.length : translations.size, pending: core ? 0 : texts.length - translations.size, cached, failed, ...(error ? { error } : {}) };
      if (!cancelled()) {
        latestStatus = status;
        try { onStatus({ ...status }); } catch { /* A status widget must not interrupt translation. */ }
      }
      return status;
    };
    const write = () => {
      if (cancelled()) return;
      for (const descriptor of descriptors) {
        const { node, attribute, memory } = descriptor;
        if (!node.isConnected) continue;
        const current = attribute ? node.getAttribute(attribute) : node.nodeValue;
        // A component may have changed a connected text node while awaiting AI.
        if (current !== descriptor.current) continue;
        const value = core ? memory.source : descriptor.parts.map(part => part.leading + (translations.get(part.text) ?? part.text) + part.trailing).join('');
        if (current !== value) {
          if (attribute) node.setAttribute(attribute, value);
          else node.nodeValue = value;
        }
        descriptor.current = value;
        memory.rendered = value;
      }
    };
    write();
    if (core) return report('core');
    const missing = texts.filter(source => !translations.has(source));
    if (!missing.length) return report(cached ? 'cached' : 'translated');
    if (!getAIAvailable()) return report('unavailable', 'Translation requires a signed-in account and a configured AI service. Cached translations remain available.');

    report('translating');
    let cursor = 0;
    while (cursor < missing.length && !cancelled()) {
      const batch = [];
      let size = 0;
      while (cursor < missing.length && batch.length < MAX_BATCH_SIZE && size + missing[cursor].length <= MAX_BATCH_CHARS) {
        batch.push(missing[cursor]);
        size += missing[cursor++].length;
      }
      const controller = new AbortController();
      activeRequest = controller;
      let timedOut = false;
      const timeout = setTimeout(() => { timedOut = true; controller.abort(); }, TIMEOUT_MS);
      try {
        requests++;
        const response = await fetch('/api/translate', {
          method: 'POST', credentials: 'same-origin',
          headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
          body: JSON.stringify({ language, texts: batch }), signal: controller.signal,
        });
        if (!response.ok) throw new Error(response.status === 401 || response.status === 403 ? 'Sign in to translate new content.' : response.status === 429 ? 'Translation limit reached. Cached translations remain available; try again later.' : `Translation service unavailable (${response.status}).`);
        const result = await response.json();
        if (cancelled()) return { ...latestStatus, state: 'cancelled' };
        if (!Array.isArray(result.translations) || result.translations.length !== batch.length || result.translations.some(value => typeof value !== 'string' || !value.trim() || value.length > 12000)) throw new Error('The translation service returned an incomplete response. Original text remains visible.');
        result.translations.forEach((value, index) => {
          const translated = value.trim();
          translations.set(batch[index], translated);
          put(keyFor(language, batch[index]), translated);
        });
        persist();
        write();
        report(cursor < missing.length ? 'translating' : 'translated');
      } catch (error) {
        if (cancelled()) return { ...latestStatus, state: 'cancelled' };
        failed = texts.length - translations.size;
        write();
        return report(translations.size ? 'partial' : 'error', timedOut ? 'Translation timed out. Original text and cached translations remain available.' : error instanceof Error ? error.message : 'Translation unavailable. Original text remains visible.');
      } finally {
        clearTimeout(timeout);
        if (activeRequest === controller) activeRequest = null;
      }
    }
    return cancelled() ? { ...latestStatus, state: 'cancelled' } : report('translated');
  }

  return {
    apply,
    invalidate,
    stats: () => ({ entries: cache.size, characters: cacheChars, maxEntries: MAX_ENTRIES, storageAvailable, requests, status: { ...latestStatus } }),
    clearCache: () => { invalidate(); cache.clear(); cacheChars = 0; try { localStorage.removeItem(CACHE_KEY); } catch { storageAvailable = false; } },
  };
}
