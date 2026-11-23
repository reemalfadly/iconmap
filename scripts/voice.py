#!/usr/bin/env python3
"""iconMap free Arabic voice (edge-tts): script text -> mp3 + word timestamps.

Usage:
  python voice.py list                                   # Arabic voices available
  python voice.py "النص" out.mp3 [options]               # text on the command line
  python voice.py @script.txt out.mp3 [options]          # text from a UTF-8 file
Options:
  --dialect kuwait|msa     kuwait = Kuwaiti-accent voices (default), msa = Modern Standard Arabic voices (Saudi)
  --gender male|female     default male
  --voice ar-KW-FahedNeural   pick an exact voice (overrides --dialect/--gender)
  --rate +0%               speed, e.g. -10% slower, +10% faster
  --pitch +0Hz
  --words words.json       word timestamps for the scene (default: <out>.words.json)
  --no-normalize           keep the raw level (default: loudness set to -18 LUFS)
  --engine elevenlabs --voice-id <id> [--model eleven_multilingual_v2] [--stability .5] [--similarity .75] [--style 0] [--speed 1.0]
                           natural voice from the user's own ElevenLabs account (key: set_key.ps1; voices: eleven.py voices --language ar)

Notes
- Free, no key. The text is sent to Microsoft's online read-aloud service, so do not send private text.
- The Kuwaiti voices have a Kuwaiti accent, but they read Modern Standard Arabic best. Dialect words
  may need light diacritics (tashkeel) to be read right. Always listen before you publish.
- Timestamps: taken from the service when it sends word boundaries, otherwise from faster-whisper.
Needs: pip install edge-tts   (and faster-whisper for the fallback timing)
"""
import asyncio, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

VOICES = {
    ("kuwait", "male"): "ar-KW-FahedNeural", ("kuwait", "female"): "ar-KW-NouraNeural",
    ("msa", "male"): "ar-SA-HamedNeural", ("msa", "female"): "ar-SA-ZariyahNeural",
}


def opt(name, default=None):
    a = sys.argv
    return a[a.index(name) + 1] if name in a and a.index(name) + 1 < len(a) else default


async def list_voices():
    import edge_tts
    for v in await edge_tts.list_voices():
        if v["Locale"].startswith("ar-"):
            print(v["ShortName"], v["Gender"], v["Locale"])


async def synth(text, out, voice, rate, pitch):
    import edge_tts
    comm = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch, boundary="WordBoundary")
    words, audio = [], bytearray()
    async for ch in comm.stream():
        if ch["type"] == "audio":
            audio += ch["data"]
        elif ch["type"] == "WordBoundary":
            s = ch["offset"] / 1e7
            words.append({"word": ch["text"], "start": round(s, 2), "end": round(s + ch["duration"] / 1e7, 2)})
    with open(out, "wb") as f:
        f.write(audio)
    return words


def normalize(path, lufs="-18"):
    """Bring the voice to -18 LUFS (reel voice standard) with a -1.5 dB true-peak ceiling. Timing is unchanged."""
    import shutil, subprocess
    if shutil.which("ffmpeg") is None:
        return False
    tmp = path + ".norm.mp3"
    r = subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", path, "-af", f"loudnorm=I={lufs}:TP=-1.5:LRA=11", "-ar", "44100", "-b:a", "192k", tmp])
    if r.returncode == 0 and os.path.exists(tmp):
        os.replace(tmp, path)
        return True
    return False


def whisper_words(path):
    from faster_whisper import WhisperModel
    model = WhisperModel("small", compute_type="int8")
    segs, _ = model.transcribe(path, word_timestamps=True, vad_filter=True, language="ar")
    words, sents = [], []
    for s in segs:
        sents.append({"text": s.text.strip(), "start": round(s.start, 2), "end": round(s.end, 2)})
        for w in s.words or []:
            words.append({"word": w.word.strip(), "start": round(w.start, 2), "end": round(w.end, 2)})
    return words, sents


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    if sys.argv[1] == "list":
        return asyncio.run(list_voices())
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    text, out = sys.argv[1], sys.argv[2]
    if text.startswith("@"):
        with open(text[1:], encoding="utf-8") as f:
            text = f.read()
    text = " ".join(text.split())
    if opt("--engine", "edge") == "elevenlabs":      # natural voice from the user's ElevenLabs account (exact timing, no Whisper)
        import eleven
        vid = opt("--voice-id") or sys.exit("--voice-id is required (list voices: python eleven.py voices --language ar)")
        print("sending the text to ElevenLabs (uses credits of your account) ...")
        audio, words = eleven.tts(text, vid, opt("--model", "eleven_multilingual_v2"), float(opt("--stability", .5)), float(opt("--similarity", .75)), float(opt("--style", 0)), float(opt("--speed", 1.0)))
        with open(out, "wb") as f:
            f.write(audio)
        if "--no-normalize" not in sys.argv:
            print("loudness set to -18 LUFS" if normalize(out) else "loudness not changed (ffmpeg missing or failed)")
        wpath = opt("--words") or os.path.splitext(out)[0] + ".words.json"
        with open(wpath, "w", encoding="utf-8") as f:
            json.dump({"voice": vid, "timing": "elevenlabs", "words": [{"word": w, "start": s, "end": e} for w, s, e in words], "sentences": []}, f, ensure_ascii=False, indent=1)
        print(f"wrote {out} and {wpath}: {len(words)} words (exact timing from ElevenLabs)")
        return
    voice = opt("--voice") or VOICES.get((opt("--dialect", "kuwait"), opt("--gender", "male")))
    if not voice:
        sys.exit("unknown --dialect/--gender (use kuwait|msa and male|female)")
    rate, pitch = opt("--rate", "+0%"), opt("--pitch", "+0Hz")
    wpath = opt("--words") or os.path.splitext(out)[0] + ".words.json"
    print(f"voice {voice}: sending text to Microsoft's online read-aloud service ...")
    words = asyncio.run(synth(text, out, voice, rate, pitch))
    if "--no-normalize" not in sys.argv:
        print("loudness set to -18 LUFS" if normalize(out) else "loudness not changed (ffmpeg missing or failed)")
    sents, source = [], "service"
    if not words:
        words, sents = whisper_words(out)
        source = "whisper"
    with open(wpath, "w", encoding="utf-8") as f:
        json.dump({"voice": voice, "timing": source, "words": words, "sentences": sents}, f, ensure_ascii=False, indent=1)
    print(f"wrote {out} and {wpath}: {len(words)} words (timing from {source})")


if __name__ == "__main__":
    main()
