#!/usr/bin/env node
/** Keep the native Sites/Vinext build intact; prepare bounded public assets around it. */
import { spawnSync } from 'node:child_process';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const commands = [
  ['tools/build-offline.mjs', '--if-needed'],
  ['scripts/run-framework.mjs', 'build', ...process.argv.slice(2)],
  ['tools/prepare-hosted-curriculum.mjs'],
];
for (const [script, ...args] of commands) {
  const result = spawnSync(process.execPath, [path.join(root, script), ...args], { cwd: root, stdio: 'inherit' });
  if (result.error) throw result.error;
  if (result.status !== 0) {
    if (result.signal) console.error(`Build stage ${script} terminated by ${result.signal}.`);
    process.exit(result.status || 1);
  }
}
