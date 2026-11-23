---
name: iconMap-check
description: iconMap final check - the last gate before a map video is delivered. Looks at frames from the finished video, verifies every number and name against the script and sources, re-transcribes the voice, checks loudness and size, and lists the credit line and what was not checked. Use it after any iconMap build and before telling the user the video is ready.
---

# iconMap check

ROOT = the folder two levels above this skill's base directory (`../..`).

Report only what was measured or seen. Never say a thing works before it was tried.

1. **Frames**: extract 8-10 frames from the FINAL file (`ffmpeg -ss <t> -i video.mp4 -frames:v 1`), tile them and look: every place the voice names is lit on its word, labels clear of the caption band, nothing cropped, the title does not cover the subject, the handle is at the bottom, small and readable.
2. **Numbers**: every number on screen and in the voice equals the script and the sources file. If a voice reads a number differently from the script, fix the script (spell it as words) and regenerate.
3. **Voice**: re-transcribe the generated voice with Whisper (`python ROOT/scripts/timestamps.py voice.mp3 words.json --lang ar`) and compare words; check peak and loudness (voice about -18 LUFS before the mix; the Globe master is -14 LUFS, true peak under -1.5 dBTP). Say clearly that voice quality and accent can only be judged by listening.
4. **File**: `ffprobe` size, duration, codec, audio present; for scheduling on a platform that limits upload size, compress and re-check.
5. **Wording**: plain Arabic in the user's own dialect; Western digits 0-9 on screen.
6. **Credits**: the NASA GIBS line for Globe imagery goes in the description; Natural Earth is public domain; disputed borders flagged.
7. **Final message**: what was made and where; the defaults chosen (so they can be changed in one sentence); what was checked by eye; what was not (for example the voice quality); the script and sources attached. Nothing is published without an explicit yes.
