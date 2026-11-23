// iconMap brief panel: a tiny local server (no dependencies, 127.0.0.1 only, nothing leaves the computer).
//   node server.mjs --dir <folder> [--port 0]
// The page (index.html) asks the 4 questions step by step and writes the answers to <folder>/brief.json as they come.
// Claude writes <folder>/ideas.json (5 ideas) as soon as brief.json has "type"; the page shows them in step 4.
// An uploaded voice recording is saved to <folder>/upload/ and listed in brief.json (voice.file).
//   brief.json : { type, size, audience, audienceOther, voiceMode: 'free'|'eleven'|'file', voice:{file}, idea, ownIdea, done }
//   ideas.json : { ideas: [ { title, places, why }, ... 5 ] }
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const arg = (n, d) => { const i = process.argv.indexOf('--' + n); return i < 0 ? d : process.argv[i + 1]; };
const dir = path.resolve(arg('dir', path.join(process.env.TEMP || process.env.TMPDIR || '.', 'iconmap-brief')));
fs.mkdirSync(path.join(dir, 'upload'), { recursive: true });
const BRIEF = path.join(dir, 'brief.json'), IDEAS = path.join(dir, 'ideas.json');
const KEYS = new Set(['type', 'size', 'audience', 'audienceOther', 'voiceMode', 'idea', 'ownIdea', 'done']);
const read = (f, d) => { try { return JSON.parse(fs.readFileSync(f, 'utf8')); } catch { return d; } };
const write = (f, o) => fs.writeFileSync(f, JSON.stringify(o, null, 1), 'utf8');
const bodyOf = (req, max = 120e6) => new Promise((ok, no) => { const c = []; let n = 0; req.on('data', d => { n += d.length; if (n > max) { no(new Error('too large')); req.destroy(); } else c.push(d); }); req.on('end', () => ok(Buffer.concat(c))); });
const send = (res, code, data, type = 'application/json; charset=utf-8') => { res.writeHead(code, { 'Content-Type': type, 'Cache-Control': 'no-store' }); res.end(typeof data === 'string' || Buffer.isBuffer(data) ? data : JSON.stringify(data)); };

let last = Date.now();
const srv = http.createServer(async (req, res) => {
  last = Date.now();
  const url = new URL(req.url, 'http://x');
  try {
    if (req.method === 'GET' && (url.pathname === '/' || url.pathname === '/index.html')) return send(res, 200, fs.readFileSync(path.join(here, 'index.html')), 'text/html; charset=utf-8');
    if (req.method === 'GET' && (url.pathname === '/f/reg.ttf' || url.pathname === '/f/bold.ttf'))
      return send(res, 200, fs.readFileSync(path.join(here, '..', 'assets', 'fonts', url.pathname === '/f/reg.ttf' ? 'IBMPlexSansArabic-Regular.ttf' : 'IBMPlexSansArabic-Bold.ttf')), 'font/ttf');
    if (req.method === 'GET' && url.pathname === '/api/state') return send(res, 200, { brief: read(BRIEF, {}), ideas: read(IDEAS, null) });
    if (req.method === 'POST' && url.pathname === '/api/answer') {
      const { key, value } = JSON.parse((await bodyOf(req, 1e5)).toString('utf8'));
      if (!KEYS.has(key)) return send(res, 400, { error: 'unknown key' });
      const b = read(BRIEF, {}); b[key] = value; write(BRIEF, b); return send(res, 200, { ok: true });
    }
    if (req.method === 'POST' && url.pathname === '/api/upload') {
      const name = (url.searchParams.get('name') || 'voice.wav').replace(/[^\w.\-؀-ۿ]+/g, '_').slice(-80);
      const f = path.join(dir, 'upload', name); fs.writeFileSync(f, await bodyOf(req));
      const b = read(BRIEF, {}); b.voiceMode = 'file'; b.voice = { file: f }; write(BRIEF, b); return send(res, 200, { ok: true, file: name });
    }
    send(res, 404, { error: 'not found' });
  } catch (e) { send(res, 500, { error: String(e.message || e) }); }
});
srv.listen(+arg('port', 0), '127.0.0.1', () => {
  console.log('URL http://127.0.0.1:' + srv.address().port + '/');
  console.log('DIR ' + dir);
});
setInterval(() => { if (Date.now() - last > 60 * 60 * 1000) process.exit(0); }, 60000).unref();
