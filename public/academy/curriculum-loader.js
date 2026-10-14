/* Hosted curricula use bounded, content-addressed parts. file:// uses the
 * already-loaded classic MG_DATA scripts; canonical JSON remains authoring data. */
const CURRICULUM_NAMES = new Set(['catalog', 'featured', 'sources', 'photos', 'media', 'course-places', 'related-skills', 'release']);
const PART_LIMIT = 7 * 1024 * 1024;
const TOTAL_LIMIT = 256 * 1024 * 1024;
const MANIFEST_LIMIT = 1024 * 1024;
const TIMEOUT_MS = 120000;
const courseIdPattern = /^[a-z0-9]+(?:[-_][a-z0-9]+)*$/;

function validateManifest(manifest) {
  if (!manifest || manifest.schemaVersion !== 1 || manifest.dataSet !== 'featured' ||
      !Number.isSafeInteger(manifest.courseCount) || manifest.courseCount < 1 || manifest.courseCount > 20000 ||
      !Array.isArray(manifest.parts) || !manifest.parts.length || manifest.parts.length > 1024) {
    throw new Error('Invalid curriculum manifest.');
  }
  const ids = new Set(), files = new Set();
  let count = 0, bytes = 0;
  for (const [index, part] of manifest.parts.entries()) {
    if (!part || typeof part.file !== 'string' || !/^part-\d{4}-[a-f0-9]{16}\.json$/.test(part.file) ||
        !part.file.startsWith(`part-${String(index + 1).padStart(4, '0')}-`) || files.has(part.file) ||
        !Number.isSafeInteger(part.byteLength) || part.byteLength < 2 || part.byteLength > PART_LIMIT ||
        !Number.isSafeInteger(part.courseCount) || part.courseCount < 1 ||
        typeof part.sha256 !== 'string' || !/^[a-f0-9]{64}$/.test(part.sha256) ||
        !part.file.endsWith(`-${part.sha256.slice(0, 16)}.json`) ||
        !Array.isArray(part.courseIds) || part.courseIds.length !== part.courseCount) {
      throw new Error('Invalid or unsafe curriculum part descriptor.');
    }
    files.add(part.file);
    for (const id of part.courseIds) {
      if (typeof id !== 'string' || id.length > 120 || !courseIdPattern.test(id) || ids.has(id)) {
        throw new Error('Invalid or duplicate curriculum course ID.');
      }
      ids.add(id);
    }
    count += part.courseCount;
    bytes += part.byteLength;
  }
  if (count !== manifest.courseCount || bytes > TOTAL_LIMIT) throw new Error('Curriculum manifest totals exceed their bounds.');
  return manifest;
}

async function boundedJSON(url, limit, fetchImpl, parentSignal, cache = 'no-cache') {
  const controller = new AbortController();
  const abort = () => controller.abort();
  if (parentSignal?.aborted) controller.abort();
  else parentSignal?.addEventListener('abort', abort, { once: true });
  const timer = setTimeout(abort, TIMEOUT_MS);
  try {
    const response = await fetchImpl(url, { signal: controller.signal, credentials: 'same-origin', redirect: 'error', cache });
    if (!response?.ok) throw new Error(`Curriculum request failed: ${url} (${response?.status || 'network'}).`);
    const declared = response.headers?.get?.('content-length');
    if (declared && Number(declared) > limit) throw new Error(`Curriculum response exceeds its size limit: ${url}.`);
    let raw;
    if (response.body?.getReader) {
      const reader = response.body.getReader(), chunks = [];
      let length = 0;
      try {
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;
          length += value.byteLength;
          if (length > limit) {
            await reader.cancel();
            throw new Error(`Curriculum response exceeds its size limit: ${url}.`);
          }
          chunks.push(value);
        }
      } finally { reader.releaseLock(); }
      raw = new Uint8Array(length);
      let offset = 0;
      for (const chunk of chunks) { raw.set(chunk, offset); offset += chunk.byteLength; }
    } else {
      raw = new TextEncoder().encode(await response.text());
      if (raw.byteLength > limit) throw new Error(`Curriculum response exceeds its size limit: ${url}.`);
    }
    let value;
    try { value = JSON.parse(new TextDecoder('utf-8', { fatal: true }).decode(raw)); }
    catch { throw new Error(`Invalid curriculum JSON: ${url}.`); }
    return { value, raw };
  } finally {
    clearTimeout(timer);
    parentSignal?.removeEventListener('abort', abort);
  }
}

async function loadFeatured(fetchImpl, signal) {
  const base = 'data/course-parts/';
  const { value } = await boundedJSON(`${base}index.json`, MANIFEST_LIMIT, fetchImpl, signal);
  const manifest = validateManifest(value);
  const results = new Array(manifest.parts.length);
  const controller = new AbortController();
  const abort = () => controller.abort();
  if (signal?.aborted) controller.abort();
  else signal?.addEventListener('abort', abort, { once: true });
  let next = 0;
  async function worker() {
    while (next < manifest.parts.length) {
      const index = next++, part = manifest.parts[index];
      const { value: courses, raw } = await boundedJSON(`${base}${part.file}`, part.byteLength, fetchImpl, controller.signal, 'default');
      if (raw.byteLength !== part.byteLength || !Array.isArray(courses) || courses.length !== part.courseCount ||
          courses.some((course, i) => !course || course.id !== part.courseIds[i] ||
            typeof course.title !== 'string' || !Array.isArray(course.stages))) {
        throw new Error(`Curriculum part contents do not match the manifest: ${part.file}.`);
      }
      // Web Crypto is present on HTTPS/localhost. Other HTTP contexts retain
      // byte/count/ID validation; content-addressed filenames prevent mixed builds.
      if (globalThis.crypto?.subtle) {
        const digest = await globalThis.crypto.subtle.digest('SHA-256', raw);
        const actual = Array.from(new Uint8Array(digest), n => n.toString(16).padStart(2, '0')).join('');
        if (actual !== part.sha256) throw new Error(`Curriculum part checksum mismatch: ${part.file}.`);
      }
      results[index] = courses;
    }
  }
  try {
    await Promise.all(Array.from({ length: Math.min(2, manifest.parts.length) }, () => worker().catch(error => { controller.abort(); throw error; })));
    return results.flat();
  } finally { signal?.removeEventListener('abort', abort); }
}

export async function loadCurriculumData(name, options = {}) {
  if (!CURRICULUM_NAMES.has(name)) throw new Error('Unknown curriculum data set.');
  // Production commerce never falls back to bundled paid lessons. Static and
  // offline editions remain complete owner/demo copies, with billing disabled.
  if (name === 'featured' && options.protected === true) {
    const result = await boundedJSON('/api/curriculum', TOTAL_LIMIT, options.fetchImpl || globalThis.fetch, options.signal, 'no-store');
    if (!Array.isArray(result.value) || result.value.some(c => !c?.id || !Array.isArray(c.stages) || (c.locked === true && c.stages.length))) throw new Error('Invalid protected curriculum response.');
    return result.value;
  }
  const data = options.data === undefined ? globalThis.window?.MG_DATA : options.data;
  if (data && Object.prototype.hasOwnProperty.call(data, name)) return data[name];
  if (globalThis.location?.protocol === 'file:') throw new Error('Offline curriculum parts are missing. Re-extract the complete application package.');
  const fetchImpl = options.fetchImpl || globalThis.fetch;
  if (typeof fetchImpl !== 'function') throw new Error('Curriculum fetching is unavailable.');
  if (name === 'featured') return loadFeatured(fetchImpl, options.signal);
  return (await boundedJSON(`data/${name}.json`, 16 * 1024 * 1024, fetchImpl, options.signal)).value;
}
