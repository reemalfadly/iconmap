"""iconMap: ElevenLabs text-to-speech with exact word timing (no Whisper needed).

The key is read from the environment variable ELEVENLABS_API_KEY, or from the file  ~/.iconmap/elevenlabs.key
(create it with  powershell -File set_key.ps1 , which asks for the key without showing it). The key is never printed,
never written to a project folder, never sent anywhere but api.elevenlabs.io.

  python eleven.py voices [--language ar] [--search kuwaiti] [--gender male] [--accent gulf]
  python eleven.py say "نص" out.mp3 --voice-id <id> [--model eleven_multilingual_v2] [--stability .5] [--similarity .75]
                       [--style 0] [--speed 1.0] [--words out.words.json]
Used by voice.py (--engine elevenlabs) and by globe/scripts/voice.py ("engine": "elevenlabs").
The text is sent to ElevenLabs and uses credits of the user's account.
"""
import base64, json, os, sys, urllib.error, urllib.parse, urllib.request
from pathlib import Path

BASE = os.environ.get('ELEVENLABS_BASE_URL', 'https://api.elevenlabs.io').rstrip('/')
KEYFILE = Path.home() / '.iconmap' / 'elevenlabs.key'


def api_key():
    k = os.environ.get('ELEVENLABS_API_KEY', '').strip()
    if not k and KEYFILE.exists():
        k = KEYFILE.read_text(encoding='utf-8').strip()
    if not k:
        sys.exit('No ElevenLabs key. Run  powershell -File set_key.ps1  (or set ELEVENLABS_API_KEY). The key is never printed.')
    return k


def _req(url, body=None):
    data = json.dumps(body).encode('utf-8') if body is not None else None
    r = urllib.request.Request(url, data=data, method='POST' if body is not None else 'GET',
                               headers={'xi-api-key': api_key(), 'Content-Type': 'application/json', 'Accept': 'application/json', 'User-Agent': 'iconmap'})
    try:
        with urllib.request.urlopen(r, timeout=180) as f:
            return json.loads(f.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        msg = e.read().decode('utf-8', 'replace')[:400].replace(api_key(), '***')
        sys.exit(f'ElevenLabs error {e.code}: {msg}')


def words_from_alignment(al):
    """character alignment -> [[word, start, end], ...] (words split on spaces, script spelling kept)"""
    ch, st, en = al['characters'], al['character_start_times_seconds'], al['character_end_times_seconds']
    out, cur, s0, e0 = [], '', None, None
    for c, a, b in zip(ch, st, en):
        if c.isspace():
            if cur: out.append([cur, round(s0, 3), round(e0, 3)]); cur, s0 = '', None
            continue
        if s0 is None: s0 = a
        cur += c; e0 = b
    if cur: out.append([cur, round(s0, 3), round(e0, 3)])
    return out


def tts(text, voice_id, model='eleven_multilingual_v2', stability=.5, similarity=.75, style=0.0, speed=1.0, fmt='mp3_44100_128'):
    """returns (mp3 bytes, words [[w,start,end]...])"""
    body = {'text': text, 'model_id': model,
            'voice_settings': {'stability': stability, 'similarity_boost': similarity, 'style': style, 'use_speaker_boost': True, 'speed': speed}}
    res = _req(f'{BASE}/v1/text-to-speech/{urllib.parse.quote(voice_id)}/with-timestamps?output_format={fmt}', body)
    al = res.get('alignment') or res.get('normalized_alignment')
    if not al: sys.exit('ElevenLabs returned no alignment for this text')
    return base64.b64decode(res['audio_base64']), words_from_alignment(al)


def voices(language=None, search=None, gender=None, accent=None, page_size=50):
    q = {'page_size': page_size, 'include_total_count': 'false'}
    if language: q['language'] = language
    if search: q['search'] = search
    if gender: q['gender'] = gender
    if accent: q['accent'] = accent
    return _req(f'{BASE}/v2/voices?' + urllib.parse.urlencode(q)).get('voices', [])


def _opt(name, default=None):
    a = sys.argv
    return a[a.index(name) + 1] if name in a and a.index(name) + 1 < len(a) else default


if __name__ == '__main__':
    try: sys.stdout.reconfigure(encoding='utf-8')
    except Exception: pass
    if len(sys.argv) < 2: sys.exit(__doc__)
    if sys.argv[1] == 'voices':
        for v in voices(_opt('--language'), _opt('--search'), _opt('--gender'), _opt('--accent')):
            lb = v.get('labels') or {}
            print(f"{v.get('name')}  |  {v.get('voice_id')}  |  {lb.get('gender', '')} {lb.get('accent', '')} {lb.get('language', '')}  |  {v.get('category', '')}  |  {v.get('preview_url', '')}")
    elif sys.argv[1] == 'say' and len(sys.argv) >= 4:
        text = sys.argv[2]
        if text.startswith('@'): text = Path(text[1:]).read_text(encoding='utf-8')
        text = ' '.join(text.split())
        vid = _opt('--voice-id') or sys.exit('--voice-id is required (list voices with: eleven.py voices --language ar)')
        audio, words = tts(text, vid, _opt('--model', 'eleven_multilingual_v2'), float(_opt('--stability', .5)), float(_opt('--similarity', .75)), float(_opt('--style', 0)), float(_opt('--speed', 1.0)))
        Path(sys.argv[3]).write_bytes(audio)
        wp = _opt('--words') or str(Path(sys.argv[3]).with_suffix('')) + '.words.json'
        Path(wp).write_text(json.dumps({'voice': vid, 'timing': 'elevenlabs', 'words': [{'word': w, 'start': s, 'end': e} for w, s, e in words]}, ensure_ascii=False, indent=1), encoding='utf-8')
        print(f'wrote {sys.argv[3]} and {wp}: {len(words)} words (exact timing from ElevenLabs)')
    else:
        sys.exit(__doc__)
