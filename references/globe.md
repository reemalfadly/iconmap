# iconMap Globe: real satellite imagery (the `globe/` folder)

iconMap has two map engines. Pick by the look the video needs:

| | flat engine (`engine/`, `scripts/render.mjs`) | **Globe engine (`globe/`)** |
|---|---|---|
| picture | drawn map (satellite-style), any projection, the user's own map images | **real NASA satellite imagery** on a 3D globe that dives from space to a region with no hard cut |
| strengths | tilt, orbit, rivers layer, any size (vertical, horizontal, square), user images | real terrain and sea colour, one continuous camera, rivers drawn on and flowing, ghost shapes (size comparison), ships, shade, swarm, atlas names, count-up numbers |
| needs | CPU only | GPU with WebGL (tested on an RTX 4060: about 35-200 ms a frame) |
| output | any size, 30 fps | vertical 1080x1920, 60 fps (rendered at 120 and blended for motion blur), -14 LUFS master |

**Default for "a complete satellite map"**: the Globe engine. Use the flat engine when the user brings his own map images, wants a horizontal or square video, or needs a tilted/orbit camera.

## Workflow (Globe)
`S` = `<skill>/globe/scripts`. Run python 3.10+ with the packages in `requirements.txt` (numpy, scipy, soundfile, Pillow, faster-whisper, edge-tts) and node (Playwright is installed in the skill folder).
1. **Project**: `python S/new.py <folder> --lang ar` (or `--from rivers-ar | hormuz-ar | nile-en`). It copies the engine into `<folder>/web`.
2. **Script**: `script.txt`. Short sentences, one map idea each; shape in `globe/references/style.md` (hook, question, steps, one number at a time, one-line payoff). Spell numbers as words in the script so the voice reads them right, and show the digits on screen with `number(...)`. Every number comes from a primary source, listed in a sources file.
3. **Voice and timing**: `python S/voice.py <folder>`. `config.json`: `"engine": "edge"` (free Edge voices: `ar-KW-FahedNeural` Kuwaiti male, `ar-KW-NouraNeural` Kuwaiti female, `ar-SA-HamedNeural` / `ar-SA-ZariyahNeural` Modern Standard), or `"engine": "file"` with the user's recording at `vo/raw.wav`. Word timing comes from Whisper (`"whisperModel": "small"`, CPU). The text of a free voice goes to Microsoft's free service.
4. **Story**: `web/story.js` (API in `globe/references/story-api.md`). Key everything to the spoken words: `T('كلمة')`.
5. **Imagery**: `python S/build.py <folder> prep`. Downloads NASA Blue Marble (layer `BlueMarble_ShadedRelief_Bathymetry`, about 500 m a pixel) once as `globe/cache/globe-8k.jpg`, then the detail patches the camera needs into `<folder>/web/img/`.
6. **Check**: `python S/build.py <folder> stills 0.6,2.6,5.8 ...` then look at `check/sheet.jpg`. Every place the voice names is lit on its word, labels are clear of the caption band, numbers readable, nothing cropped.
7. **Sound**: `cues.json`. Cue files named `LIB:...` use the built-in kit in `assets/sfx/` (matched by name: whoosh, swish, pop, impact, riser...) unless `ICONMAP_SFX_LIB` points to the user's own library. Subtle, one accent per event.
8. **Build**: `python S/build.py <folder> all` (prep + frames + mix + master + encode). Prints loudness and the credit line.
9. **Credit**: put the printed credit line in the video description: NASA GIBS acknowledgement for the imagery; Natural Earth borders and rivers are public domain.

## Limits
- Imagery is about 500 m a pixel: perfect from the whole globe down to a country or a gulf, soft closer than about 3 degrees of width. Street level needs a sharper source.
- Country borders and rivers only (no provinces or states yet); patches do not cross the date line.
- Vertical 1080x1920 only. For other sizes use the flat engine.
- Disputed borders follow Natural Earth: check each one before publishing.
