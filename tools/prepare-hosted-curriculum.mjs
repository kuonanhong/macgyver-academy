#!/usr/bin/env node
/** Validate the hosted copy before removing only its oversized source duplicate. */
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';

const repoRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const hash = value => crypto.createHash('sha256').update(value).digest('hex');

export function prepareHostedCurriculum(root = repoRoot) {
  const sourceData = path.join(root, 'public/academy/data');
  const builtRoot = path.join(root, 'dist/client');
  const builtData = path.join(builtRoot, 'academy/data');
  const sourceIndex = fs.readFileSync(path.join(sourceData, 'course-parts/index.json'));
  const builtIndex = fs.readFileSync(path.join(builtData, 'course-parts/index.json'));
  if (!sourceIndex.equals(builtIndex)) throw new Error('Hosted curriculum manifest differs from the generated source.');
  const manifest = JSON.parse(sourceIndex);
  const canonical = JSON.parse(fs.readFileSync(path.join(sourceData, 'featured.json'), 'utf8'));
  if (manifest.schemaVersion !== 1 || manifest.dataSet !== 'featured' || !Array.isArray(manifest.parts) ||
      !manifest.parts.length || !Array.isArray(canonical) || canonical.length !== manifest.courseCount) {
    throw new Error('Hosted curriculum manifest or canonical data is invalid.');
  }
  let cursor = 0;
  const ids = new Set();
  for (const [index, part] of manifest.parts.entries()) {
    if (!part || !/^part-\d{4}-[a-f0-9]{16}\.json$/.test(part.file) ||
        !part.file.startsWith(`part-${String(index + 1).padStart(4, '0')}-`) ||
        !/^[a-f0-9]{64}$/.test(part.sha256) || !part.file.endsWith(`-${part.sha256.slice(0, 16)}.json`)) {
      throw new Error('Unsafe hosted curriculum part name or checksum.');
    }
    const raw = fs.readFileSync(path.join(builtData, 'course-parts', part.file));
    if (raw.length !== part.byteLength || raw.length > 7 * 1024 * 1024 || hash(raw) !== part.sha256) {
      throw new Error(`Invalid hosted curriculum part: ${part.file}.`);
    }
    const courses = JSON.parse(raw);
    if (!Array.isArray(courses) || courses.length !== part.courseCount ||
        !Array.isArray(part.courseIds) || part.courseIds.length !== courses.length) throw new Error('Hosted curriculum count mismatch.');
    for (const [i, course] of courses.entries()) {
      if (!course?.id || course.id !== part.courseIds[i] || ids.has(course.id) ||
          JSON.stringify(course) !== JSON.stringify(canonical[cursor])) {
        throw new Error('Hosted courses differ from canonical content or order.');
      }
      ids.add(course.id); cursor++;
    }
  }
  if (cursor !== canonical.length) throw new Error('Hosted curriculum is incomplete.');
  // Never mutate public/academy/data/featured.json: it remains the authoring,
  // Python-backend, offline and downloadable-source canonical file.
  fs.rmSync(path.join(builtData, 'featured.json'), { force: true });
  let files = 0, largest = 0;
  function inspect(dir) {
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      const name = path.join(dir, entry.name);
      if (entry.isDirectory()) inspect(name);
      else if (entry.isFile()) {
        const size = fs.statSync(name).size; files++; largest = Math.max(largest, size);
        if (size > 25 * 1024 * 1024) throw new Error(`Hosted asset exceeds 25 MiB: ${path.relative(builtRoot, name)}.`);
      } else if (entry.isSymbolicLink()) throw new Error(`Unexpected hosted asset symlink: ${path.relative(builtRoot, name)}.`);
    }
  }
  inspect(builtRoot);
  return { courses: cursor, parts: manifest.parts.length, assets: files, largestAssetBytes: largest };
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  if (process.argv.length > 2) throw new Error('prepare-hosted-curriculum.mjs takes no arguments.');
  console.log('Hosted curriculum prepared:', JSON.stringify(prepareHostedCurriculum()));
}
