#!/usr/bin/env python3
"""Voiceover -> word timestamps for iconMap.
Usage: python3 timestamps.py vo.mp3 words.json [--model small] [--lang ar]
Output: [{"word": "...", "start": 0.12, "end": 0.40}, ...] plus a sentence list.
Needs: pip install faster-whisper
"""
import json, sys

def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    src, out = sys.argv[1], sys.argv[2]
    model_name = sys.argv[sys.argv.index("--model") + 1] if "--model" in sys.argv else "small"
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        sys.exit("faster-whisper not installed: pip install faster-whisper")
    model = WhisperModel(model_name, compute_type="int8")
    lang = sys.argv[sys.argv.index("--lang") + 1] if "--lang" in sys.argv else None  # e.g. ar; default: auto-detect
    segments, _ = model.transcribe(src, word_timestamps=True, vad_filter=True, language=lang)
    words, sentences = [], []
    for seg in segments:
        sentences.append({"text": seg.text.strip(), "start": round(seg.start, 2), "end": round(seg.end, 2)})
        for w in seg.words or []:
            words.append({"word": w.word.strip(), "start": round(w.start, 2), "end": round(w.end, 2)})
    with open(out, "w", encoding="utf-8") as f:
        json.dump({"words": words, "sentences": sentences}, f, indent=1, ensure_ascii=False)
    print(f"wrote {out}: {len(words)} words, {len(sentences)} sentences")

if __name__ == "__main__":
    main()
