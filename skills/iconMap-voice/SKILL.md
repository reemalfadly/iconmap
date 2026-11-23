---
name: iconMap-voice
description: iconMap voice - turns a script into a voice-over and word timings for map videos. Free Arabic voices (Modern Standard or Kuwaiti accent, male or female) or the user's own recording or audio file, normalised to -18 LUFS, with word timestamps. Use it after the script is ready, or when the user asks for a free Arabic voice, a voice sample, or timing for his own recording.
---

# iconMap voice

ROOT = the folder two levels above this skill's base directory (`../..`).

## Free voices (Edge TTS, no key)
`python ROOT/scripts/voice.py @script.txt vo.mp3 --dialect kuwait|msa --gender male|female [--rate +10%]` also writes `vo.words.json` and normalises to -18 LUFS.
- Voices: `ar-KW-FahedNeural` (Kuwaiti male), `ar-KW-NouraNeural` (Kuwaiti female), `ar-SA-HamedNeural` (Modern Standard male), `ar-SA-ZariyahNeural` (Modern Standard female).
- The text is sent to Microsoft's free online service: say so once, and do not send private text.
- The Kuwaiti voices read Modern Standard best; dialect words may need light diacritics. Spell numbers as words in the voice text (digits can be read wrong: one run read 102 as 108), show the digits on screen.
- Always re-transcribe the generated voice with Whisper (for example `python ROOT/scripts/timestamps.py voice.mp3 words.json --lang ar`, `--model medium` if memory allows) and compare every number and name with the script. The transcript proves the words, not the beauty of the voice: tell the user to listen.
- Speed: about 1.5 words/s plain, about 2 with `--rate +10%`. Length check: words / 2 = seconds.

## Natural voice: ElevenLabs (the user's own account)
The free voices are neural and sound synthetic. For a natural, human voice use ElevenLabs:
1. Key (once): the user runs `powershell -ExecutionPolicy Bypass -File ROOT/scripts/set_key.ps1` in a terminal (the key is typed hidden and stored in `~/.iconmap/elevenlabs.key`). Never ask for the key in the chat, never print it, never put it in a project folder.
2. Pick a voice: `python ROOT/scripts/eleven.py voices --language ar --gender male` lists voices with their `voice_id` (ask the user to choose by listening to the preview link, or to paste a `voice_id`). Gulf and Kuwaiti-sounding voices are in the ElevenLabs voice library: search `--search kuwaiti` or `--accent gulf`.
3. Speak: `python ROOT/scripts/voice.py @script.txt vo.mp3 --engine elevenlabs --voice-id <id>` (also `--model eleven_multilingual_v2`, `--stability 0.4`, `--similarity 0.75`, `--style 0`, `--speed 1.0`). It writes `vo.words.json` with exact word timing from ElevenLabs (no Whisper). Globe projects: `"engine": "elevenlabs", "voiceId": "<id>"` in `config.json`.
4. The text is sent to ElevenLabs and uses credits of the user's account: say so once. Test on a short sentence first, and tell the user to listen (a transcript proves the words, not the naturalness).
Status: this path was tested against a local fake of the API (request, key header, parsing, word timing), not yet against a real ElevenLabs account.

## Choosing the voice (decision order)
1. The user attached a recording or audio file: use it.
2. The user has an ElevenLabs key saved and picked a voice: ElevenLabs.
3. Otherwise the free Edge voice (Kuwaiti male by default), and say that a recording or ElevenLabs sounds more human.
## The user's own voice or an audio file
- Globe engine: put it at `<project>/vo/raw.wav` (48 kHz mono) and use `"engine": "file"` in `config.json`; `ROOT/globe/scripts/voice.py <project>` trims, squeezes long pauses and writes `web/timing.json`.
- Flat engine: `python ROOT/scripts/timestamps.py vo.mp3 words.json --lang ar`.

## Memory note
Whisper `small` on CPU is enough for timing. If loading a bigger model fails with a memory error, close other heavy programs or use `"whisperModel": "small"`.
