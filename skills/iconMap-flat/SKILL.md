---
name: iconMap-flat
description: iconMap flat engine - builds a map-explainer video from a scene JSON on a drawn satellite-style map or the user's own map images, in any size (vertical, horizontal, square, 4:5), with Arabic right-to-left text, rivers, tilt and orbit camera, smooth waypoint camera moves, highlights, pins, paths, numbers, blueprint and cross-section cutaways. CPU only. Use it for horizontal or square map videos, for the user's own map images, or when no GPU is available; the default vertical satellite video uses iconMap-globe.
---
# iconMap flat engine

iconMap renders map explainer videos from a **scene JSON** file, with full Arabic (right-to-left) support. A deterministic SVG engine draws each frame in headless Chromium (Playwright), and ffmpeg encodes the result to MP4. It ships with real borders (countries, US states, and the states/provinces of the USA, Canada, Australia, Brazil, China, India, Indonesia, Russia and South Africa). It works on the built-in globe or on the user's own map images, which are georeferenced so every highlight lands on the right place in the picture.

Folder map:
- `engine/engine.js`: renderer, stages, camera, highlight styles, every element and background type
- `engine/geo.js`: bundled borders (Natural Earth countries 1:50m, admin-1 provinces 1:50m, US states 1:10m) + topojson-client
- `scripts/render.mjs`: scene JSON → MP4, contact sheet (`--contact`) or one frame (`--still t`)
- `scripts/georef.mjs`: draws the real borders over a user image to check its control points
- `references/intake.md`: the opening interview (questions, numbered choices, how answers drive the build)
- `scripts/voice.py`: free Arabic voice (Kuwaiti-accent or Modern Standard, male or female) → mp3 at -18 LUFS + word timestamps
- `scripts/timestamps.py`: voiceover → word timestamps (Whisper, `--lang ar`)
- `scripts/make_sfx.py` + `assets/sfx/`: the synthesised sound-effect kit
- `references/style-guide.md`: visual grammar and the **highlight rules**. Read it before planning shots.
- `references/elements.md`: every field of every element. Read it before writing JSON.
- `engine/names-ar.js`: Arabic names for every country and for the states/provinces of the USA, Canada, Australia, South Africa, Brazil, China and India. Edit it to add or fix a name.
- `examples/demo-ar.json` (Arabic / RTL, Kuwait), `examples/demo.json` (built-in globe, English) (no sample map images are shipped)
- `scripts/autoalign.py`: snaps a web-map screenshot to the real coastlines (land/water matching)
- `rights/`: ownership notice and data licences. Keep this folder with every copy.

ROOT = the folder two levels above this skill's base directory (`../..`). Every path in this skill (`engine/`, `scripts/`, `references/`, `examples/`) is relative to ROOT. The interview, the defaults and the sources/check steps belong to the `iconMap` entry skill.

## Requirements
Node 18+, Playwright with Chromium, ffmpeg. Optional: Python 3 + `faster-whisper` for automatic voiceover timing.
- One step: `bash setup.sh` (macOS/Linux) or `powershell -ExecutionPolicy Bypass -File setup.ps1` (Windows).
- Manual: `npm install && npx playwright install chromium`, install ffmpeg, optionally `pip install -r requirements.txt`.
- In Claude's workspace these are usually preinstalled. If Node can't find Playwright: `export NODE_PATH=$(npm root -g)`.

## Arabic / RTL (iconMap)
- Scenes are Arabic by default (`"lang": "ar"`; use `"lang": "en"` for English labels). Font: IBM Plex Sans Arabic (Poppins stays for Latin).
- Any text that contains Arabic is set right-to-left and joined correctly. Mixed text (`17,818 كم²`, `UTC+3`) works. Letter-spacing is switched off for Arabic, because it breaks the joining.
- Write place names in Arabic or English: `"names": ["الكويت", "السعودية"]` or `["Kuwait", "Saudi Arabia"]`. `"label": true` prints the Arabic name.
- `tag` sits at the right edge for Arabic text. In `box` rows and org charts, put the first item on the right (x large) so the eye reads right to left. Use `reveal: "wipeLeft"` for a right-to-left wipe.
- Always use Western digits 0-9, never Arabic-Indic digits.
- An account handle is drawn small and thin at the very bottom of the frame when the scene sets `"handle": "@name"` (none by default). Captions live at y ≈ 1500-1600, clear of it.
- Disputed borders (Western Sahara, Palestine, Kashmir, Crimea and others) follow Natural Earth's convention. Check each one before publishing.
- Facts: no number or claim without a source. Show the script and get approval before building.

## Camera moves (smooth, with tilt and orbit)
The camera is smooth by default (smootherstep easing). In a shot's `cam`:
- `{ "lon": 47.7, "lat": 29.3, "span": 9 }`: still view.
- `{ "from": {...}, "to": {...}, "dur": 4, "ease": "smooth|sine|soft|inOut|out|linear" }`: eased move. `"from": "prev"` starts exactly where the previous shot ended, so the camera keeps flowing through the cut. `"arc": 0.8` pulls the camera back in the middle of the move and pushes in again (zoom out then in).
- `{ "keys": [ {"t":0,"lon":..,"lat":..,"span":..}, {"t":2.2,...,"tilt":25,"rot":-6}, ... ] }`: waypoints (seconds after the shot starts) flown through with a smooth spline, no stop at each waypoint. This is the way to make an orbit or a long fly-over.
- `"rot"`: roll in degrees (a few degrees, ±4 to ±10, gives the orbiting feel). `"tilt"`: 0-60 degrees, looks at the map at an angle with perspective (use 20-40). Labels, pins and numbers follow the tilted map.
- Rhythm: change the angle every shot (alternate the rot sign), zoom in for the detail and out for the context, and keep every move slower than the words (about 4-6 s per move).
- Rendering: `--workers 4` (default) renders four frames at a time; use `--workers 6` on a strong PC.
## Rivers
- The world stage draws real rivers (Natural Earth 10m, `engine/rivers.js`) as a thin blue layer under the highlights. Small rivers appear as the camera gets closer. Turn them off with `"basemap": {"rivers": false}`, recolour with `"riverColor": "#5cc8ff"`.
- `{ "type": "river", "names": ["دجلة", "Euphrates"], "color": "#37b8ff", "width": 7, "drawDur": 2, "label": true }` draws one named river on in colour with a glow, and labels it in Arabic. Names work in Arabic or English (major rivers have Arabic names in `rivers.js`, field `a`). Use it when the voice names the river (the highlight rule).
## Helpers for size comparison, measuring and word-synced captions
- `{ "type": "ghost", "name": "France", "only": [-5.5, 41.2, 9.8, 51.2], "to": [29.4, 26.0], "fill": "blue", "label": true }`: lifts a country's real shape and lays it on another place to compare sizes (east-west is rescaled by latitude so it keeps its true size). `only` keeps just the polygons inside a box (the mainland). Names work in Arabic or English.
- `{ "type": "measure", "from": [31.24, 30.1], "to": [32.9, 24.09], "unit": "كم" }`: a double-headed arrow that grows from its middle while the number counts up to the real distance (or `"value": 1500`), laid along the line. `text`: `"# كم"` puts the number where the `#` is.
- Scene-level `"captions": { "words": "words.json", "max": 4, "y": 1540, "size": 46 }`: captions timed word by word from the file that `voice.py` or `timestamps.py` writes; the word being spoken is yellow. Phrases are cut at punctuation, at a pause longer than 0.5 s, or after `max` words.
## The highlight rule (most important)
**Whenever the narration names or explains a part of the map, that part lights up in colour on the same beat.** A country, state, province, zone, island chain, route or area is never just labelled or pinned: it gets a filled highlight with white borders, in a colour chosen for its role (see `references/style-guide.md` §5):
- The subject area (a whole country, "the United States") → `style:"tint"` (soft translucent blue, white borders).
- The places the story is about (California and Texas) → `style:"solid"` (opaque orange, or zone colours when comparing).
- Several categories at once (time zones, regions, blocs) → `zones` with one pastel colour each and pill labels (`UTC-7`).
- One hero feature (Hawaii, a volcano chain, a hotspot) → `style:"glow"` (fiery orange glow), optionally with `spotlight` to darken everything else.
- Anything without a border in the data (a mountain range, a sea route, an island chain, a crater) → `area` (free polygon, smooth) or a thick `path` in `sand`/`fire`.
Keep the earlier highlight on screen while the next one builds (tint underneath, solids on top), so the viewer always sees how the parts relate.

## Workflow
1. **Intake.** Take the answers of the `iconMap` interview (video type, idea, size, audience) and the defaults it chose. Then get the script and/or voiceover, the places named, and any map images or photos. Size comes from Q2: vertical 1080×1920 (default), 16:9 `"width":1920,"height":1080`, square 1080×1080, 4:5 `"width":1080,"height":1350`, all at 30 fps. Place text by lon/lat or as fractions of the canvas, then check the contact sheet at that size.
2. **Maps.** No images → the built-in globe (`"basemap":{"style":"satellite"}`). With images → georeference each one (next section) and check it with `georef.mjs` before anything else.
3. **Timing.** With the user's audio: `python3 scripts/timestamps.py vo.mp3 words.json --lang ar`. With a free generated voice: `python3 scripts/voice.py @script.txt vo.mp3 --dialect kuwait|msa --gender male|female` (also writes `vo.words.json`). Without audio, assume about 2.3 words per second for Arabic and split at sentence breaks.
4. **Beat sheet.** Split the narration into beats of 1–2.5 s. List every place or map part the narration mentions, and give each one a highlight on its beat (the highlight rule). Other beats get one visual event each: a camera move, a path drawing, a pin, a number, an icon burst, a caption keyword. Group beats into shots of 2.5–5 s.
5. **Write the scene JSON.** Shot `start`/`end` come from the timestamps; each element's `t0` is seconds after its shot starts. Land highlights and pops on the stressed word.
6. **QC.** `node scripts/render.mjs scene.json sheet.png --contact --scale 0.5`, then look at it: every named place highlighted, highlights sitting on the right land, labels legible and clear of the caption band (y ≈ 1500–1600), nothing cropped. Check single moments with `--still <seconds>`.
7. **Final.** `node scripts/render.mjs scene.json out.mp4 --audio vo.mp3 [--music bed.mp3]`. Sound effects are added automatically (see below; `--no-sfx` turns them off). Use `--scale 2` for 4K. Deliver the MP4 and the scene JSON.

## Using the user's own map images (georeferencing)
**Best: web-map screenshots** of imagery the user has the right to use (they are Web Mercator, so they align exactly):
1. Declare the map with `"projection": "mercator"` and 4–8 rough control points (landmarks read off a 50 px grid).
2. Run `python3 scripts/autoalign.py scene.json <mapId>`. It matches land and water in the picture against the real coastlines and lake shores, and writes exact points back into the scene (mismatch typically falls to 1–2%).
3. Check with `georef.mjs` (below). Coastlines and lake shores should sit on the picture's shores.
Ask the user for **clean images with no drawn borders or labels**: drawn lines never match real borders exactly, and the plugin draws its own.

**Other images** (AI-made maps, tilted globes, artistic renders) use the thin-plate warp: no `projection`, 10–25 control points.
Declare each image under `maps` with **control points**: landmarks you can see in the picture, as `[pixelX, pixelY, lon, lat]`.
```json
"maps": {
  "us": { "src": "us.png", "points": [
    [295, 685, -109.05, 37.0], [822, 935, -81.1, 25.15], [493, 930, -97.15, 25.95],
    [130, 745, -117.12, 32.53], [975, 575, -70.0, 41.67], [98, 425, -124.7, 48.38] ] }
},
"shots": [ { "start": 0, "end": 4, "map": "us", "cam": { "fit": true }, "elements": [
  { "type": "region", "set": "provinces", "names": ["California"], "style": "solid" } ] } ]
```
- A thin-plate spline warps the real borders onto the picture, so it works for satellite renders, tilted globe views and AI-made maps alike. Use 10–25 points spread over the whole area that will be highlighted, including its edges: coast tips and capes, border corners (Four Corners), lake ends, river mouths, bay corners.
- To find pixel positions, draw a labelled 50 px grid over the image (PIL) and view crops of it.
- **Always check:** `node scripts/georef.mjs scene.json us check.png`. Red dots (your pixels) and cyan rings (warped lon/lat) should overlap, and the drawn borders should sit on the picture's coastlines. Add points wherever the lines drift, then check again.
- Borders are only drawn within 12° of the control points (`margin`), so add points before highlighting places further out.
- Insets (an Alaska or Hawaii box on a US map) are not geographic. Leave them out with `"exclude":["Alaska","Hawaii"]`, or declare the same image a second time under another map id with the inset's own points.
- The camera never shows past the image edges. Use `cam: {fit:true}`, `{fit:true, zoom:1.5, x, y}` (pixels) or `{lon, lat, span}`.
- Images that are exact plate carrée or Mercator can instead go in `basemap.images` with `bounds` (see elements.md).

## Sound effects
The renderer mixes a built-in kit (`assets/sfx/`: `whoosh swish pop click ding impact riser flip`, made by `scripts/make_sfx.py`) under the voiceover. Cues come from the scene automatically:
- flash cut → whoosh; switch to a cutaway or another map → whoosh/swish; big camera zoom → swish
- region/area reveal → pop (wipes → swish); zones → a pop per zone; pins, boxes, time tags, numbers → pop; counters and seat charts → riser
- check icons → ding; titles → impact; paths, arrows, rulers → swish; marker circles and pinging dots → click
Control: per element `"sfx": "flip"` (replace), `"sfx": false` (silence), `"sfxVol"`; extra cues with scene `"sfx": [{"t": 12.3, "sound": "impact", "vol": 0.8}]` (absolute seconds; `sound` can also be a file path); overall level `"sfxVolume"` (default 0.55); `"autoSfx": false` for manual cues only. Keep effects under the voice, and pick one effect per beat.

## Style rules (summary)
- The map is the stage. Push the camera between beats with zooms, and hard-cut or `flash` on big reveals.
- Every place mentioned is highlighted (the highlight rule), built up layer by layer.
- Captions are small white phrases near the bottom (y ≈ 1500–1560), with `*keyword*` in yellow. Big numbers pop in yellow.
- Comparisons win: two solid regions in contrasting colours, two pins, A vs B numbers on screen together.
- Cut to `blueprint` for structures (org charts, counts, seats) and to `section` for "what's under the surface".
- Change something every 1–2 s. End on a twist.

## Extending
- New icon: `ICON.name = c => svg` (100 px box centred on 0,0).
- New element: `E.name = (ctx, e, L) => svg` (return `{map, screen}` to draw inside the camera transform).
- New zone preset: add to `PRESETS` (list of `{label, fill, names, labelAt}`).
- New highlight style: add to `RSTYLE`. New colour name: add to `COLORS`.
- New cutaway background: `BG.name = (ctx, b) => svg`.

## Ownership
Proprietary. Read `rights/OWNERSHIP_AND_RIGHTS.txt` before redistributing, and keep the `rights/` folder in every copy. Border data is Natural Earth (public domain) via world-atlas/us-atlas (ISC); see the licence files in `rights/`.
