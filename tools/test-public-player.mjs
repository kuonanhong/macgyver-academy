// Checks the exact standalone publishable boundary; does not access a live Site.
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';
import { HOSTED_VIDEO_PLAYER, safeVideoPlayerUrl } from '../public/academy/learning-media.js';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const output = process.argv[2] ? path.resolve(process.argv[2]) : path.join(root, 'public-player');
const source = path.join(root, 'public/academy');
const dist = path.join(output, 'dist');
assert.deepEqual(fs.readdirSync(dist).sort(), ['config.js', 'index.html', 'video-player.css', 'video-player.html', 'video-player.js']);
const manifest = JSON.parse(fs.readFileSync(path.join(output, '.openai/hosting.json'), 'utf8'));
assert.deepEqual(manifest.static, { directory: 'dist' }); assert.equal(manifest.d1, null); assert.equal(manifest.r2, null);
const publicContext = { window: {} };
vm.runInNewContext(fs.readFileSync(path.join(dist, 'config.js'), 'utf8'), publicContext);
const config = JSON.parse(JSON.stringify(publicContext.window.MG_CONFIG));
assert.deepEqual(Object.keys(config).sort(), ['allowedYouTubeIds', 'videoPlayerUrl'], 'public config must not copy maps keys or other academy settings');
assert.equal(safeVideoPlayerUrl(config.videoPlayerUrl), config.videoPlayerUrl);
assert.equal(HOSTED_VIDEO_PLAYER, 'https://macgyver-public-player.kuonanhong.chatgpt.site/video-player.html');
const media = JSON.parse(fs.readFileSync(path.join(source, 'data/media.json'), 'utf8'));
const expected = [...new Set(media.courses.flatMap(c => c.videos.map(v => {
  try { const url = new URL(v.embedUrl); return url.hostname === 'www.youtube-nocookie.com' ? url.pathname.match(/^\/embed\/([A-Za-z0-9_-]{11})$/)?.[1] : null; } catch { return null; }
})).filter(Boolean))].sort();
assert.deepEqual(config.allowedYouTubeIds, expected, 'every allowed ID comes from current approved curriculum media');
assert(expected.length > 0);
const academyContext = { window: {} }; vm.runInNewContext(fs.readFileSync(path.join(source, 'config.js'), 'utf8'), academyContext);
assert.deepEqual(JSON.parse(JSON.stringify(academyContext.window.MG_CONFIG.allowedYouTubeIds)), expected);
for (const filename of ['video-player.html', 'video-player.js', 'video-player.css']) assert.equal(fs.readFileSync(path.join(dist, filename), 'utf8'), fs.readFileSync(path.join(source, filename), 'utf8'), `${filename}: generated copy must be current`);
const script = fs.readFileSync(path.join(dist, 'video-player.js'), 'utf8');
assert(!/\bfetch\s*\(|document\.cookie|localStorage|\/api\/|sign(?:in|out)-with-chatgpt|Authorization:/.test(script), 'public player does not read accounts/storage or call an application API');
const html = fs.readFileSync(path.join(dist, 'video-player.html'), 'utf8');
assert(html.includes('strict-origin-when-cross-origin'));
assert(!/<iframe\b|https:\/\/www\.youtube/.test(html), 'initial HTML makes no third-party request');
const index = fs.readFileSync(path.join(dist, 'index.html'), 'utf8');
for (const match of index.matchAll(/video=([A-Za-z0-9_-]{11})/g)) assert(expected.includes(match[1]), 'entry example must be allowlisted');
console.log(`Public player PASS: exactly 5 static files, ${expected.length} approved video IDs, source copies current, no account/API/storage bindings, sanitized config. Remote anonymous access is checked separately by deployment.`);
