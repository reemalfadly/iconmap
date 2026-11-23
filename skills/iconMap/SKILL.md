---
name: iconMap
description: iconMap by iconReem - makes a map-explainer video (geography, borders, straits, rivers, comparisons, oil and trade, what is under the surface) with Arabic right-to-left text. It starts with 4 short questions (video type, one idea out of 5, vertical or horizontal, audience) and decides everything else itself, then builds the video with the Globe engine (real NASA satellite imagery) or the flat engine. Use it whenever the user asks for a map video, a map animation, a geography or politics explainer, an Arabic map Short, or says iconMap.
---

# iconMap (the entry skill)

ROOT = the folder two levels above this skill's base directory (`../..`). Every path below is relative to ROOT.

## Step 0: welcome, then ask only 5 questions, one at a time, in this same chat
Open with this welcome, in the voice of the author Reem («السلام عليكم، أنا ريم، وأحببت أن أهديك هذا البلقن الممتع الذي يتيح لك صناعة فيديوهات خرائط متحركة بالعربية: كرة ثلاثية الأبعاد بصور أقمار ناسا، وأنهار ترسم نفسها، وأرقام تتحرك، وصوت. بجودة احترافية لأفلامك وقصصك. اذكرني بدعوة، وشكرًا لك. والآن سأسألك 5 أسئلة فقط، والباقي أتولاه عنك. وإن كان عندك تسجيل بصوتك فأرفقه في أي وقت»), then ask exactly these, one per message, each starting «iconReem تسألك:» with numbered choices. Every choice is a short name plus one plain line (and a tiny example when the name alone is not obvious), so a non-technical user understands it without asking. Write them in simple Modern Standard Arabic, short and without padding. Wait for the answer before the next. Never list several questions in one message and never add more. Full text, defaults and rules: `references/intake.md` (read it now).
1. **Video type** (6 choices, each explained with an example: see Q1 in `references/intake.md`; show them exactly as written there)
2. **Idea**: propose 5 concrete ideas for that type (use the `iconMap-script` skill for how); the user picks one or writes his own
3. **Size**: 1 طولي للجوال (ريلز، تيك توك، ستوري)، 2 عرضي للشاشة الكبيرة (يوتيوب، عروض تقديمية)
4. **Audience**: 1 عامة الناس، 2 طلاب، 3 أصحاب مشاريع ومهنيين، 4 متابعين حسابي، 5 غيرهم (each with its one plain line from `references/intake.md`)
5. **Voice**: 1 فصحى صوت رجل، 2 فصحى صوت امرأة، 3 خليجي كويتي صوت رجل، 4 خليجي كويتي صوت امرأة، 5 أرفق تسجيلي بصوتي، 6 بدون صوت (see Q5 in `references/intake.md`)

Everything else is decided by you from the defaults in `references/intake.md`: voice, duration, script, map, pace, captions, effects (always on), handle, disputed borders, output folder. List the defaults you chose in the final reply so the user can change any of them in one sentence.
When the AskUserQuestion tool is available you may use it for questions 3 and 4 (clickable choices); keep questions 1 and 2 as numbered lists, because they have more than 4 options.

## Optional: the visual brief panel (only when the user asks for a page instead of chat)
The default is the chat above. If the user asks for a visual page, use the local panel (the desktop app's Browser pane, or any browser on his computer). It runs on his own computer only (127.0.0.1, nothing is uploaded) and asks the same questions as step cards, including the voice choice (free voice, ElevenLabs, or upload his own recording).
1. Start it as a BACKGROUND command: `node ROOT/brief/server.mjs --dir <project folder>`. It prints `URL http://127.0.0.1:PORT/`.
2. Open that URL for the user (in the desktop app use the Browser pane) and say in one line that he answers on the page.
3. Run in the background `node ROOT/brief/wait.mjs <project folder> type`. When it exits, read `<project folder>/brief.json`, then write `<project folder>/ideas.json` = `{ "ideas": [ { "title": "...", "places": "...", "why": "..." } x 5 ] }` (5 varied, checkable ideas for that type: see `iconMap-script`). The page shows them in its last step.
4. Run in the background `node ROOT/brief/wait.mjs <project folder> done`. When it exits, read `brief.json`: `type` (1-6), `size` (vertical|horizontal), `audience` (+ `audienceOther`), `voiceMode` (free|eleven|file, and `voice.file` for an uploaded recording), `idea` or `ownIdea`. Do not ask again; continue with the defaults.
Otherwise stay in chat.

## Choose the engine from the answers
| situation | engine | skill to follow |
|---|---|---|
| vertical video, "a complete satellite map" (default) | **Globe**: real NASA satellite imagery, GPU, one continuous camera | `iconMap-globe` |
| horizontal or square size, the user's own map images, tilt/orbit camera, no GPU | **Flat**: drawn map, any size | `iconMap-flat` |

## The pipeline (each step has its own skill)
1. Idea and script with checked numbers and a sources file: `iconMap-script`
2. Voice (free Arabic voice, or the user's own recording) and word timing: `iconMap-voice`
3. Build with the chosen engine: `iconMap-globe` or `iconMap-flat`
4. Final check before delivery: `iconMap-check`

## Rules that always apply
- Speak to the user in plain, friendly Arabic, and keep the wording clean.
- No number or claim without a source that was read; anything unverified is left out. Disputed borders follow Natural Earth: flag the sensitive ones.
- Nothing is published or scheduled without the user's explicit yes.
- Credits: the Globe imagery needs the NASA GIBS acknowledgement line (the build prints it); Natural Earth data is public domain. Keep `rights/` with every copy.
