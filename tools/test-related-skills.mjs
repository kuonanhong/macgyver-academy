import assert from 'node:assert/strict';
import fs from 'node:fs';
import {setRelatedSkills, relatedForCourse, relatedSkillsMarkup, safeReference} from '../public/academy/related-skills.js';

const read = name => JSON.parse(fs.readFileSync(new URL(`../public/academy/data/${name}`, import.meta.url), 'utf8'));
const catalog = read('catalog.json');
const featured = read('featured.json');
const byId = new Map(catalog.map(course => [course.id, course]));
const featuredIds = new Set(featured.map(course => course.id));
const places = new Map(read('course-places.json').courses.map(entry=>[entry.courseId,entry.place]));
const moduleOnly = process.argv.includes('--module-only');
const hasText = (value, label) => assert(typeof value === 'string' && value.trim(), label);
const bilingual = (object, key, label) => {
  hasText(object[key], `${label}: ${key}`);
  hasText(object[`${key}En`], `${label}: ${key}En`);
};
const noAutomaticRequests = html => assert(!/<(?:script|iframe|img|video|audio|source|link|object|embed)\b/i.test(html), 'Related skills must not load external resources while rendering');
const cleanMarkup = (html, label) => {
  assert(html.includes('related-skills'), `${label}: missing section`);
  assert(!/\bundefined\b|\[object Object\]/.test(html), `${label}: unresolved content`);
  noAutomaticRequests(html);
  for (const match of html.matchAll(/<a\b([^>]+)>/g)) {
    const attributes = match[1];
    const href = attributes.match(/\bhref="([^"]*)"/)?.[1];
    assert(href, `${label}: missing anchor URL`);
    if (href.startsWith('#project/')) {
      assert(byId.has(decodeURIComponent(href.slice('#project/'.length))), `${label}: invalid catalogue destination ${href}`);
    } else {
      assert(safeReference(href), `${label}: unsafe external destination ${href}`);
      assert(/\btarget="_blank"/.test(attributes) && /\brel="[^"]*noopener\b/.test(attributes), `${label}: external link must isolate its opener`);
    }
  }
};

assert.equal(catalog.length, read('release.json').topics);
assert.equal(byId.size, catalog.length, 'Catalogue IDs are unique');
assert.equal(featuredIds.size, featured.length);
assert(featured.every(course => byId.has(course.id)));
assert.equal(safeReference('https://example.org/a?x=1&y=2'), 'https://example.org/a?x=1&y=2');
for (const url of ['javascript:alert(1)', 'data:text/html,<script>alert(1)</script>', 'file:///tmp/index.html', 'http://example.org', '//example.org/path', '/relative/path', 'https://user:pass@example.org', 'https://user@example.org', 'not a URL', '', null, undefined]) {
  assert.equal(safeReference(url), '', `Reject unsafe URL ${url}`);
}

// Adversarial metadata must stay text, and invalid references must never become links.
const payload = '<script>alert("x")</script><img src=x onerror="alert(1)"> & \' "';
const syntheticCourse = {id: 'security-fixture', category: 'fixture'};
const syntheticItem = {id: 'target-"<>&', referenceUrls: ['https://example.org/?x=1&y=2', 'javascript:alert(1)']};
for (const field of ['title', 'why', 'transfer', 'difference']) {
  syntheticItem[field] = payload;
  syntheticItem[`${field}En`] = `English ${payload}`;
}
syntheticItem.practice = [payload, payload, payload];
syntheticItem.practiceEn = [`English ${payload}`, 'Second instruction', 'Third instruction'];
const syntheticEntry = {
  courseId: syntheticCourse.id, overview: payload, overviewEn: `English ${payload}`,
  related: [syntheticItem], references: [
    {url: 'https://example.org/?x=1&y=2', title: payload, titleEn: `English ${payload}`, publisher: payload, scope: payload, scopeEn: `English ${payload}`},
    {url: 'javascript:alert(1)', title: payload, titleEn: payload, publisher: payload, scope: payload, scopeEn: payload}
  ]
};
setRelatedSkills({courses: [syntheticEntry]}, [{id: syntheticItem.id, title: payload, titleEn: payload}]);
for (const zh of [true, false]) {
  const html = relatedSkillsMarkup(syntheticCourse, {zh, compact: true});
  noAutomaticRequests(html);
  assert(html.includes('&lt;script&gt;') && html.includes('&quot;'), 'Metadata is HTML-escaped');
  assert(!html.includes('href="javascript:') && !html.includes('href="data:'), 'Invalid references have no links');
  assert(html.includes(`href="#project/${encodeURIComponent(syntheticItem.id)}"`), 'Catalogue IDs are encoded');
  assert(html.includes('x=1&amp;y=2'), 'URL attributes are escaped');
  assert(html.includes('skill-library'), 'Compact mode is expandable');
  if (!zh) assert(html.includes('English &lt;script&gt;'), 'English field selected');
}

// Every uncurated topic must get honest, deterministic same-category navigation.
setRelatedSkills({courses: []}, catalog);
let fallbackCount = 0;
for (const course of catalog.filter(course => !featuredIds.has(course.id))) {
  const entry = relatedForCourse(course);
  assert.equal(entry.curated, false);
  assert.equal(entry.courseId, course.id);
  assert(entry.related.length > 0 && entry.related.length <= 6, `${course.id}: fallback count`);
  assert.equal(new Set(entry.related.map(item => item.id)).size, entry.related.length, `${course.id}: duplicate fallback`);
  assert(entry.related.every(item => byId.has(item.id) && item.id !== course.id && item.category === course.category), `${course.id}: fallback must remain in its category and exclude itself`);
  assert.deepEqual(relatedForCourse(course).related.map(item => item.id), entry.related.map(item => item.id), `${course.id}: fallback order is deterministic`);
  for (const zh of [true, false]) {
    const html = relatedSkillsMarkup(course, {zh, compact: fallbackCount % 2 === 0});
    cleanMarkup(html, course.id);
    assert(html.includes(zh ? '自動推薦' : 'Automatically suggested'), `${course.id}: disclose automatic suggestions`);
    assert(!html.includes('skill-comparison'), `${course.id}: do not present fallback as a researched lesson`);
    for (const item of entry.related) bilingual(item, 'title', item.id);
  }
  fallbackCount++;
}
assert.equal(fallbackCount, catalog.length-featured.length);

if (moduleOnly) {
  console.log(`Related skills module PASS: URL/escaping checks and ${fallbackCount} bilingual automatic fallback renders. Curated-data validation intentionally omitted (--module-only).`);
  process.exit(0);
}

const data = read('related-skills.json');
assert.equal(data.courses.length, featured.length);
assert.equal(new Set(data.courses.map(course => course.courseId)).size, featured.length, 'No duplicate curated course IDs');
const curatedIds=new Set(data.courses.map(course=>course.courseId));
assert.deepEqual([...curatedIds].sort(),[...featuredIds].sort(),'Every guided course has curated comparisons');
assert([...curatedIds].every(id=>featuredIds.has(id)), 'Curated comparisons belong to guided courses');
setRelatedSkills(data, catalog);
let comparisons = 0;
let references = 0;
for (const course of featured.filter(c=>curatedIds.has(c.id))) {
  const entry = relatedForCourse(course);
  assert.equal(entry.curated, true, course.id);
  bilingual(entry, 'overview', course.id);
  assert(Array.isArray(entry.related) && entry.related.length === 2, `${course.id}: two curated comparisons required`);
  assert(Array.isArray(entry.references) && entry.references.length >= 3, `${course.id}: three references required`);
  const urls = new Set();
  for (const ref of entry.references) {
    for (const key of ['title', 'scope']) bilingual(ref, key, `${course.id} reference`);
    hasText(ref.publisher, `${course.id}: publisher`);
    assert(safeReference(ref.url), `${course.id}: unsafe reference ${ref.url}`);
    assert(!urls.has(ref.url), `${course.id}: duplicate reference ${ref.url}`);
    urls.add(ref.url);
    references++;
  }
  const linkedIds = new Set();
  for (const item of entry.related) {
    for (const key of ['title', 'why', 'transfer', 'difference']) bilingual(item, key, `${course.id} comparison`);
    for (const key of ['practice', 'practiceEn']) {
      assert(Array.isArray(item[key]) && item[key].length === 3, `${course.id}: three practice instructions in ${key}`);
      item[key].forEach((value, index) => hasText(value, `${course.id}: ${key}[${index}]`));
    }
    assert(Array.isArray(item.referenceUrls) && item.referenceUrls.length > 0, `${course.id}: comparison needs sources`);
    assert(item.referenceUrls.every(url => urls.has(url) && safeReference(url)), `${course.id}: reference outside its course bibliography`);
    if (item.id != null) {
      assert(byId.has(item.id), `${course.id}: unknown linked catalogue ID ${item.id}`);
      assert(item.id !== course.id, `${course.id}: comparison must not link to itself`);
      assert(!linkedIds.has(item.id), `${course.id}: duplicate comparison destination ${item.id}`);
      linkedIds.add(item.id);
    }
    assert(featuredIds.has(item.id),`${course.id}: related destination must be a guided course`);
    const p=places.get(item.id);assert(p,`${item.id}: destination place missing`);
    assert.deepEqual(item.place,p,`${item.id}: inherit its reviewed representative place`);
    assert(Number.isFinite(item.place.lat)&&Number.isFinite(item.place.lng));
    hasText(item.place.address,`${item.id}: address or geographical description`);
    hasText(item.place.coordinateScope,`${item.id}: approximate-point scope`);
    comparisons++;
  }
  for (const zh of [true, false]) for (const compact of [true, false]) {
    const html = relatedSkillsMarkup(course, {zh, compact});
    cleanMarkup(html, course.id);
    assert.equal((html.match(/class="skill-comparison"/g) || []).length, entry.related.length);
    assert(!html.includes(zh ? '依相同領域自動推薦' : 'Automatically suggested research topics'), `${course.id}: curated content mislabeled`);
    assert(html.includes(zh ? '三步比較練習' : 'Three-step comparison exercise'));
    assert.equal((html.match(/class="skill-project"/g)||[]).length,2,'Visible project-comparison cards');
    assert.equal((html.match(/class="place-location-details"/g)||[]).length,2,'Visible address/coordinate blocks');
    for(const item of entry.related){
      const map=new URL('https://www.google.com/maps/search/');map.searchParams.set('api','1');map.searchParams.set('query',`${item.place.lat},${item.place.lng}`);
      assert(html.includes(map.href.replaceAll('&','&amp;')),`${item.id}: exact coordinate map link`);
      assert(html.includes(`${item.place.lat}, ${item.place.lng}`),`${item.id}: visible coordinates`);
    }
  }
}
for(const course of featured.filter(c=>!curatedIds.has(c.id))){
 const entry=relatedForCourse(course);assert.equal(entry.curated,false);
 assert(entry.related.length>0);for(const zh of [true,false])cleanMarkup(relatedSkillsMarkup(course,{zh}),course.id);
}
assert.equal(comparisons,featured.length*2);
console.log(`Related skills PASS: ${featured.length} curated courses, ${comparisons} comparisons, ${references} reference entries, ${fallbackCount} automatic fallback topics; bilingual renders, source links, escaping, IDs and no automatic resource loading.`);
