#!/usr/bin/env node
/** Assemble the anonymous, stateless player only; never publish the academy API. */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { safeVideoPlayerUrl, HOSTED_VIDEO_PLAYER } from '../public/academy/learning-media.js';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const source = path.join(root, 'public/academy');
const args = process.argv.slice(2);
if (args.length && (args.length !== 2 || args[0] !== '--out')) throw new Error('Usage: node tools/build-public-player.mjs [--out PROJECT_DIRECTORY]');
const output = path.resolve(args[1] || path.join(root, 'public-player'));
if (output === root || output === source || source.startsWith(output + path.sep) || output.startsWith(source + path.sep)) throw new Error('Choose a separate public-player project folder.');
const curriculum = JSON.parse(fs.readFileSync(path.join(source, 'data/media.json'), 'utf8'));
const ids = [...new Set((curriculum.courses || []).flatMap(c => (c.videos || []).map(v => {
  try { const u = new URL(v.embedUrl); return u.protocol === 'https:' && u.hostname === 'www.youtube-nocookie.com' && !u.username && !u.password && !u.port ? u.pathname.match(/^\/embed\/([A-Za-z0-9_-]{11})$/)?.[1] : null; } catch { return null; }
})).filter(Boolean))].sort();
if (!ids.length) throw new Error('No approved curriculum YouTube IDs were found.');
const configPath = path.join(source, 'config.js');
const oldConfig = fs.readFileSync(configPath, 'utf8');
const block = /  \/\/ BEGIN GENERATED YOUTUBE IDS[^\n]*\n[\s\S]*?  \/\/ END GENERATED YOUTUBE IDS/;
if (!block.test(oldConfig)) throw new Error('config.js is missing its generated YouTube ID markers.');
const newConfig = oldConfig.replace(block, `  // BEGIN GENERATED YOUTUBE IDS — node tools/build-public-player.mjs\n  allowedYouTubeIds: ${JSON.stringify(ids)},\n  // END GENERATED YOUTUBE IDS`);
if (newConfig !== oldConfig) fs.writeFileSync(configPath, newConfig);
const configured = newConfig.match(/\bvideoPlayerUrl\s*:\s*(['"])([^'"\n]+)\1/)?.[2];
const playerUrl = safeVideoPlayerUrl(configured) || HOSTED_VIDEO_PLAYER;

fs.mkdirSync(output, { recursive: true });
const manifestPath = path.join(output, '.openai/hosting.json');
const existing = fs.existsSync(manifestPath) ? JSON.parse(fs.readFileSync(manifestPath, 'utf8')) : {};
if (existing.d1 || existing.r2) throw new Error('Refusing to overwrite a project with database or private object-storage bindings.');
const files = new Map();
for (const name of ['video-player.html', 'video-player.js', 'video-player.css']) files.set(name, fs.readFileSync(path.join(source, name), 'utf8'));
// Do not copy the academy config wholesale: maps keys, future account settings
// and other unrelated configuration must never enter this public deployment.
files.set('config.js', `/* Generated anonymous player settings. No API keys or account settings. */\nwindow.MG_CONFIG=Object.freeze(${JSON.stringify({ videoPlayerUrl: playerUrl, allowedYouTubeIds: ids }, null, 2)});\n`);
files.set('index.html', '<!doctype html>\n<html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="referrer" content="strict-origin-when-cross-origin"><title>MacGyver · 公開教學影片播放器</title><link rel="stylesheet" href="video-player.css"></head><body><main class="player-info"><h1>MacGyver 公開教學影片播放器</h1><p>不需要工程學院或 ChatGPT 帳號。這個網站僅呈現已選入教材的 YouTube 影片，不提供帳號、學習紀錄或 AI API。</p><p>No academy or ChatGPT sign-in is required. This stateless site only presents approved public YouTube videos; it contains no accounts, progress records or AI API.</p><p><a href="video-player.html?video=Z-E5IUozd7M">開啟半導體製程影片 / Open the semiconductor video ↗</a></p><p>影片連線仍受 YouTube、作者、網路及瀏覽器的限制。 / YouTube, publisher, network and browser restrictions still apply.</p></main></body></html>\n');
const dist = path.join(output, 'dist');
if (fs.existsSync(dist)) for (const name of fs.readdirSync(dist)) {
  if (!files.has(name) || !fs.lstatSync(path.join(dist, name)).isFile()) throw new Error(`Unexpected file in public dist: ${name}. Inspect it before rebuilding.`);
}
fs.mkdirSync(dist, { recursive: true });
for (const [name, content] of files) { const temp = path.join(dist, name + '.tmp'); fs.writeFileSync(temp, content); fs.renameSync(temp, path.join(dist, name)); }
fs.mkdirSync(path.dirname(manifestPath), { recursive: true });
fs.writeFileSync(manifestPath, JSON.stringify({ ...existing, static: { directory: 'dist' }, d1: null, r2: null }, null, 2) + '\n');
const readme = path.join(root, 'public-player/README_ZH.md');
if (fs.existsSync(readme) && output !== path.dirname(readme)) fs.copyFileSync(readme, path.join(output, 'README_ZH.md'));
console.log(`Public player assembled: 5 static files, ${ids.length} approved YouTube IDs, no account/API bindings. Output: ${output}`);
