---
name: iconMap-globe
description: iconMap Globe engine - builds a vertical (1080x1920, 60 fps) map-explainer video on REAL NASA satellite imagery with a 3D globe that dives from space to the place with no hard cut, rivers that draw on and flow, ghost shapes for size comparisons, ships, count-up numbers, atlas names and Arabic captions timed word by word. Use it for the default "complete satellite map" video after the iconMap interview, or when the user asks for a real-satellite globe map. GPU with WebGL needed.
---

# iconMap Globe engine

ROOT = the folder two levels above this skill's base directory (`../..`). `S` = `ROOT/globe/scripts`. Python 3.10+ with the packages in `requirements.txt`; node has Playwright installed at ROOT (`npm install` once, see `setup.ps1`).
Read `references/globe.md` (workflow, limits) and `globe/references/style.md` (story shape, look, sound) and `globe/references/story-api.md` (every story call: cam, region, river, ghost, shade, swarm, atlasName, title, icon, measure, path, ships, ruler, pin, ping, label, number, captions) before writing a story.

## Steps
1. `python S/new.py <folder> --lang ar` (or `--from rivers-ar | hormuz-ar | nile-en`).
2. Script in `<folder>/script.txt` (see `iconMap-script`): spell numbers as words so the voice reads them right; show the digits on screen with `number(...)`.
3. Voice and timing: `python S/voice.py <folder>` (see `iconMap-voice`). `config.json`: `"engine": "edge"` with a voice, or `"engine": "file"` with the user's recording at `vo/raw.wav`; `"whisperModel": "small"` keeps memory low.
4. Write `<folder>/web/story.js`, keyed to the spoken words with `T('كلمة')` (`T('كلمة#2')` = second time it is said, `T('كلمة.end')` = its end). Every place the voice names lights up on that word. Keep the subject between 25% and 65% of the height; captions sit near 79%. Put the handle with `label({x:540,y:1862}, '‎@name', {size:24})` when the user wants one (the LRM mark keeps the @ on the left).
5. Imagery: `python S/build.py <folder> prep` (NASA Blue Marble via GIBS: the globe once into `ROOT/globe/cache`, then the detail patches the camera needs).
6. Check: `python S/build.py <folder> stills 0.6,2.6,5.8,...`, then open `check/sheet.jpg` and look at it.
7. Sound: `cues.json`. `LIB:` file names map to the built-in kit in `ROOT/assets/sfx` by name (whoosh, swish, pop, impact, riser). One accent per event, subtle.
8. `python S/build.py <folder> all` (frames at 120 fps blended to 60, sound mix, -14 LUFS master, encode). It prints the credit line for the description.
9. Run `iconMap-check`, then deliver.

## 3D toolbox (read `globe/references/story-api.md`, section "iconMap 3D additions")
Camera `tilt` and `roll` (the picture laid back in perspective), numbers that run, drop, flip, zoom or walk with a 3D body, `odometer` (rolling digits), `bars3d` (3D columns on the map), `arc3d` (routes that rise in an arc), `zoomBlur` (punch-in transition) and a 3D title (`depth`). Use them on the beats that matter: one 3D effect per idea, not everything at once.
## Limits
Imagery is about 500 m a pixel (soft closer than about 3 degrees of width); borders and rivers only (no provinces); vertical only; patches do not cross the date line. For horizontal or square use `iconMap-flat`.
