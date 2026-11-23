// iconMap: wait until the brief panel has a given answer.   node wait.mjs <dir> <key> [timeoutSeconds=1800]
// Exits 0 when <dir>/brief.json has a truthy <key> (for example "type", then "done"), 2 on timeout.
// Run it as a background command: when it exits, read brief.json (the answers) and continue.
import fs from 'node:fs';
import path from 'node:path';
const [dir, key, to] = process.argv.slice(2);
if (!dir || !key) { console.error('usage: node wait.mjs <dir> <key> [timeoutSeconds]'); process.exit(1); }
const f = path.join(path.resolve(dir), 'brief.json'), end = Date.now() + (+to || 1800) * 1000;
const has = () => { try { const b = JSON.parse(fs.readFileSync(f, 'utf8')); return !!b[key]; } catch { return false; } };
const tick = () => { if (has()) { console.log('ready: ' + key); process.exit(0); } if (Date.now() > end) { console.log('timeout waiting for ' + key); process.exit(2); } setTimeout(tick, 1000); };
tick();
