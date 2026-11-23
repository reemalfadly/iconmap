// iconMap first-run welcome: prints a short instruction for Claude ONCE per installed version (then stays silent).
// The marker lives in ~/.iconmap/ ; delete it to see the welcome again.
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
let version = '1';
try { version = JSON.parse(fs.readFileSync(path.join(root, '.claude-plugin', 'plugin.json'), 'utf8')).version || '1'; } catch { /* keep */ }
const dir = path.join(os.homedir(), '.iconmap'), marker = path.join(dir, 'welcomed-' + version);
try { if (fs.existsSync(marker)) process.exit(0); fs.mkdirSync(dir, { recursive: true }); fs.writeFileSync(marker, new Date().toISOString()); } catch { process.exit(0); }
const msg = [
  'iconMap was just installed or updated for this user (first run of version ' + version + ').',
  'In your FIRST reply of this session, after answering anything the user asked, start iconMap: invoke the iconmap:iconMap skill from its Step 0.',
  'That means this exact welcome in Arabic, in the voice of the plugin author Reem («السلام عليكم، أنا ريم، وأحببت أن أهديك هذا البلقن الممتع الذي يتيح لك صناعة فيديوهات خرائط متحركة بالعربية: كرة ثلاثية الأبعاد بصور أقمار ناسا، وأنهار ترسم نفسها، وأرقام تتحرك، وصوت. بجودة احترافية لأفلامك وقصصك. اذكرني بدعوة، وشكرًا لك. والآن سأسألك 5 أسئلة فقط، والباقي أتولاه عنك.») and then question 1 (the video type) right away, in the same reply, in simple Modern Standard Arabic, each option as a short explanation plus a short example (see references/intake.md Q1).',
  'If the user clearly said they want something unrelated to maps, give only the one-line welcome and mention /iconmap. Do not repeat the welcome later in the session.'
].join('\n');
console.log(msg);
