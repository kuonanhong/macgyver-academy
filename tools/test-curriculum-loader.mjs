#!/usr/bin/env node
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';
import { loadCurriculumData } from '../public/academy/curriculum-loader.js';
import { prepareHostedCurriculum } from './prepare-hosted-curriculum.mjs';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const dataDir = path.join(root, 'public/academy/data');
const index = JSON.parse(fs.readFileSync(path.join(dataDir, 'course-parts/index.json'), 'utf8'));
const canonical = JSON.parse(fs.readFileSync(path.join(dataDir, 'featured.json'), 'utf8'));
const content = new Map([['data/course-parts/index.json', JSON.stringify(index)]]);
for (const part of index.parts) content.set(`data/course-parts/${part.file}`, fs.readFileSync(path.join(dataDir, 'course-parts', part.file)));
content.set('data/catalog.json', fs.readFileSync(path.join(dataDir, 'catalog.json')));
let checks = 0;
const response = body => new Response(body, { status: 200, headers: { 'content-type': 'application/json' } });
const clone = value => JSON.parse(JSON.stringify(value));

let calls = [];
const offline = { featured: canonical };
assert.equal(await loadCurriculumData('featured', { data: offline, fetchImpl: () => { throw Error('offline must not fetch'); } }), canonical); checks++;
let running = 0, maximum = 0;
const fetchGood = async (url, options) => {
  calls.push({ url, options });
  running++; maximum = Math.max(maximum, running);
  await new Promise(resolve => setImmediate(resolve));
  running--;
  return content.has(url) ? response(content.get(url)) : new Response('', { status: 404 });
};
const hosted = await loadCurriculumData('featured', { data: null, fetchImpl: fetchGood });
assert.deepEqual(hosted, canonical, 'HTTP parts preserve every field and canonical order');
assert.deepEqual(hosted.map(c => c.id), index.parts.flatMap(p => p.courseIds));
assert.equal(calls[0].options.cache, 'no-cache');
assert(calls.every(c => !c.url.endsWith('/featured.json')), 'no oversize legacy fallback');
assert(maximum <= 2 && maximum >= Math.min(2, index.parts.length)); checks++;
assert.deepEqual(await loadCurriculumData('catalog', { data: null, fetchImpl: fetchGood }), JSON.parse(content.get('data/catalog.json'))); checks++;
await assert.rejects(loadCurriculumData('../secrets', { data: {}, fetchImpl: fetchGood }), /Unknown curriculum/); checks++;

async function rejectManifest(mutator, pattern) {
  const invalid = clone(index); mutator(invalid);
  const requests = [];
  await assert.rejects(loadCurriculumData('featured', { data: null, fetchImpl: async url => {
    requests.push(url);
    if (url !== 'data/course-parts/index.json') throw Error('Unsafe manifest fetched a part');
    return response(JSON.stringify(invalid));
  }}), pattern);
  assert.deepEqual(requests, ['data/course-parts/index.json']); checks++;
}
for (const unsafe of ['../featured.json', 'https://example.invalid/part.json', '//evil.test/part.json', 'part-0001-%2e%2e.json', 'part-0001-aaaaaaaaaaaaaaaa.json?x=1']) {
  await rejectManifest(m => { m.parts[0].file = unsafe; }, /unsafe|Invalid/);
}
await rejectManifest(m => { m.courseCount++; }, /totals/);
await rejectManifest(m => { m.parts[0].courseIds[1] = m.parts[0].courseIds[0]; }, /duplicate/);
await rejectManifest(m => { m.parts[0].byteLength = 7 * 1024 * 1024 + 1; }, /descriptor/);
await rejectManifest(m => {
  const sample = m.parts[0];
  m.parts = Array.from({ length: 40 }, (_, i) => ({ ...sample, file: `part-${String(i + 1).padStart(4, '0')}-${sample.sha256.slice(0, 16)}.json`, byteLength: 7 * 1024 * 1024, courseCount: 1, courseIds: [`sample-${i}`] }));
  m.courseCount = 40;
}, /totals/);

await assert.rejects(loadCurriculumData('featured', { data: null, fetchImpl: async () => new Response('', { status: 404 }) }), /request failed/); checks++;
await assert.rejects(loadCurriculumData('featured', { data: null, fetchImpl: async url => url.endsWith('index.json') ? response(content.get(url)) : new Response('', { status: 404 }) }), /request failed/); checks++;
await assert.rejects(loadCurriculumData('featured', { data: null, fetchImpl: async () => response('<html>hosting error</html>') }), /Invalid curriculum JSON/); checks++;

const firstURL = `data/course-parts/${index.parts[0].file}`;
const wrongOrder = JSON.parse(content.get(firstURL)); [wrongOrder[0], wrongOrder[1]] = [wrongOrder[1], wrongOrder[0]];
await assert.rejects(loadCurriculumData('featured', { data: null, fetchImpl: async url => response(url === firstURL ? JSON.stringify(wrongOrder) + '\n' : content.get(url)) }), /contents do not match/); checks++;
const wrongTitle = JSON.parse(content.get(firstURL));
wrongTitle[0].titleEn = wrongTitle[0].titleEn.replace(/[A-Za-z]/, letter => letter === 'Z' ? 'Y' : 'Z');
const tampered = JSON.stringify(wrongTitle) + '\n';
assert.equal(Buffer.byteLength(tampered), index.parts[0].byteLength, 'tamper retains size, IDs and count');
await assert.rejects(loadCurriculumData('featured', { data: null, fetchImpl: async url => response(url === firstURL ? tampered : content.get(url)) }), /checksum mismatch/); checks++;
await assert.rejects(loadCurriculumData('featured', { data: null, fetchImpl: async url => response(url === firstURL ? Buffer.concat([content.get(url), Buffer.from(' ')]) : content.get(url)) }), /size limit/); checks++;

// A streaming response must enforce limits across chunks, not just Content-Length.
await assert.rejects(loadCurriculumData('featured', { data: null, fetchImpl: async url => {
  if (url !== firstURL) return response(content.get(url));
  return response(new ReadableStream({ start(controller) { controller.enqueue(content.get(url)); controller.enqueue(new Uint8Array([32])); controller.close(); } }));
}}), /size limit/); checks++;
const aborter = new AbortController(); aborter.abort();
await assert.rejects(loadCurriculumData('featured', { data: null, signal: aborter.signal, fetchImpl: async (url, options) => {
  assert(options.signal.aborted); throw new DOMException('Aborted', 'AbortError');
}}), /Aborted/); checks++;

const fixture = fs.mkdtempSync(path.join(os.tmpdir(), 'macgyver-hosted-test-'));
try {
  const source = path.join(fixture, 'public/academy/data');
  const built = path.join(fixture, 'dist/client/academy/data');
  fs.mkdirSync(source, { recursive: true }); fs.mkdirSync(built, { recursive: true });
  fs.copyFileSync(path.join(dataDir, 'featured.json'), path.join(source, 'featured.json'));
  fs.copyFileSync(path.join(dataDir, 'featured.json'), path.join(built, 'featured.json'));
  fs.cpSync(path.join(dataDir, 'course-parts'), path.join(source, 'course-parts'), { recursive: true });
  fs.cpSync(path.join(dataDir, 'course-parts'), path.join(built, 'course-parts'), { recursive: true });
  const before = crypto.createHash('sha256').update(fs.readFileSync(path.join(source, 'featured.json'))).digest('hex');
  const prepared = prepareHostedCurriculum(fixture);
  assert.equal(prepared.courses, canonical.length);
  assert(!fs.existsSync(path.join(built, 'featured.json')));
  assert.equal(crypto.createHash('sha256').update(fs.readFileSync(path.join(source, 'featured.json'))).digest('hex'), before); checks++;
  assert.equal(prepareHostedCurriculum(fixture).courses, canonical.length, 'postbuild is idempotent'); checks++;
  fs.copyFileSync(path.join(dataDir, 'featured.json'), path.join(built, 'featured.json'));
  const missing = path.join(built, 'course-parts', index.parts[0].file);
  fs.unlinkSync(missing);
  assert.throws(() => prepareHostedCurriculum(fixture), /ENOENT/);
  assert(fs.existsSync(path.join(built, 'featured.json')), 'validation failure must retain the built source copy'); checks++;
  fs.copyFileSync(path.join(dataDir, 'course-parts', index.parts[0].file), missing);
  const big = path.join(fixture, 'dist/client/too-large.bin'); const fd = fs.openSync(big, 'w'); fs.ftruncateSync(fd, 25 * 1024 * 1024 + 1); fs.closeSync(fd);
  assert.throws(() => prepareHostedCurriculum(fixture), /exceeds 25 MiB/); checks++;
} finally { fs.rmSync(fixture, { recursive: true, force: true }); }

// Protected delivery must ignore any complete owner/offline copy and fail closed.
const privateCopy={featured:[{id:'paid',title:'Paid',stages:[{steps:[{id:'secret'}]}]}]};
let protectedCalls=[];
const publicMetadata=[{id:'paid',title:'Paid',locked:true,stages:[]}];
const protectedResult=await loadCurriculumData('featured',{protected:true,data:privateCopy,fetchImpl:async(url,options)=>{protectedCalls.push(url);assert.equal(options.cache,'no-store');return response(JSON.stringify(publicMetadata))}});
assert.deepEqual(protectedResult,publicMetadata);assert.deepEqual(protectedCalls,['/api/curriculum']);checks++;
await assert.rejects(loadCurriculumData('featured',{protected:true,data:privateCopy,fetchImpl:async()=>new Response('',{status:401})}),/request failed/);checks++;
await assert.rejects(loadCurriculumData('featured',{protected:true,data:privateCopy,fetchImpl:async()=>response(JSON.stringify([{id:'paid',locked:true,stages:[{steps:[]}]}]))}),/Invalid protected/);checks++;

// Exercise build orchestration without running a second full framework build.
const orchestration = fs.mkdtempSync(path.join(os.tmpdir(), 'macgyver-build-wrapper-'));
try {
  fs.mkdirSync(path.join(orchestration, 'tools')); fs.mkdirSync(path.join(orchestration, 'scripts'));
  fs.copyFileSync(path.join(root, 'tools/build-hosted.mjs'), path.join(orchestration, 'tools/build-hosted.mjs'));
  const recorder = `import fs from 'node:fs';fs.appendFileSync('events.jsonl',JSON.stringify({script:process.argv[1].split('/').pop(),args:process.argv.slice(2)})+'\\n');`;
  for (const script of ['tools/build-offline.mjs', 'scripts/run-framework.mjs', 'tools/prepare-hosted-curriculum.mjs']) fs.writeFileSync(path.join(orchestration, script), recorder);
  let result = spawnSync(process.execPath, [path.join(orchestration, 'tools/build-hosted.mjs'), '--mode', 'staging'], { encoding: 'utf8' });
  assert.equal(result.status, 0, result.stderr);
  let events = fs.readFileSync(path.join(orchestration, 'events.jsonl'), 'utf8').trim().split('\n').map(JSON.parse);
  assert.deepEqual(events.map(e => e.args), [['--if-needed'], ['build', '--mode', 'staging'], []]); checks++;
  fs.writeFileSync(path.join(orchestration, 'events.jsonl'), '');
  fs.writeFileSync(path.join(orchestration, 'scripts/run-framework.mjs'), recorder + 'process.exit(17);');
  result = spawnSync(process.execPath, [path.join(orchestration, 'tools/build-hosted.mjs')], { encoding: 'utf8' });
  assert.equal(result.status, 17);
  events = fs.readFileSync(path.join(orchestration, 'events.jsonl'), 'utf8').trim().split('\n').map(JSON.parse);
  assert.equal(events.length, 2, 'failed framework build prevents postbuild'); checks++;
} finally { fs.rmSync(orchestration, { recursive: true, force: true }); }

console.log(`PASS ${checks} curriculum-loader/build checks; ${hosted.length} courses in ${index.parts.length} bounded parts preserve canonical content and order.`);
