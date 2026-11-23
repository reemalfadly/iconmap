# iconMap: opening interview (only 5 questions)

**The interview speaks as iconReem.** Open with the author's welcome from `skills/iconMap/SKILL.md` Step 0 (it ends with «والآن سأسألك 5 أسئلة فقط، والباقي أتولاه عنك»). Start each question with «iconReem تسألك:» (no emoji).

Rules:
- **Only these 5 questions, in this order.** Long interviews are boring. Everything else is decided by the skill from the defaults below and reported at the end, so the user can ask for a change in one sentence. Sound effects are always on.
- **ONE question at a time.** Send a single question, wait for the answer, then send the next. Never list several questions in one message.
- Options are a short numbered list the user answers with one number (use AskUserQuestion with one question per call when it exists and there are 4 or fewer options).
- Skip any question the user already answered (for example when the first message already gives the idea or the size).
- Write the welcome, the questions and the options in simple Modern Standard Arabic (فصحى مبسطة), short, with no padding. The voice of the video is a separate choice (see the voice row in the defaults).

## The 5 questions

**Q1. نوع الفيديو** (what iconMap can make). Show it exactly like this (a short explanation and an example beside each name, no extra words), then «اكتب رقمًا واحدًا»:
1. **شرح موقع**: أين يقع المكان على الخريطة ولماذا هو مهم. مثال: لماذا موقع دولة الكويت مهم؟
2. **مقارنة**: دولتان أو مدينتان جنبًا إلى جنب بالأرقام. مثال: السعودية ومصر في المساحة وعدد السكان
3. **مناطق وتصنيفات**: خريطة مقسمة بألوان، لكل مجموعة لون. مثال: المناطق الزمنية، دول مجلس التعاون
4. **مسار ورحلة**: خط يسير على الخريطة بين نقطتين. مثال: طريق تجاري قديم، خط طيران
5. **خبر بالأرقام**: حدث أو قرار تُعرض أرقامه على الخريطة. مثال: أعداد، نسب، مقاعد
6. **ما تحت السطح**: مقطع من الداخل، تحت الأرض أو البحر. مثال: كيف تتحرك الصفائح الأرضية

**Q2. اختيار الفكرة**: the skill proposes **5 concrete ideas** for the chosen type (each one line: a title phrased as a question or a surprising fact, plus the places that will appear). The user picks 1-5, or writes his own idea.
- Make the ideas varied (different regions, one local or Gulf idea, one surprising), visual on a map, and checkable from official sources. Do not propose an idea whose key claim cannot be verified.

**Q3. المقاس**
1. **طولي** للجوال. مثال: ريلز، تيك توك، ستوري (1080×1920)
2. **عرضي** للشاشة الكبيرة. مثال: يوتيوب، عروض تقديمية (1920×1080)

**Q4. لمن الفيديو؟** (the audience; it decides how simple the words are)
1. **عامة الناس**: كلمات بسيطة بلا مصطلحات صعبة
2. **طلاب**: معلومات مرتبة بخطوات واضحة
3. **أصحاب مشاريع ومهنيون**: أرقام مختصرة تفيد القرار
4. **متابعو حسابي**: بأسلوب حسابك
5. **غيرهم**: اكتب لمن

**Q5. الصوت** (asked last, before researching the script; never skipped)
1. **فصحى، صوت رجل**
2. **فصحى، صوت امرأة**
3. **خليجي كويتي، صوت رجل**
4. **خليجي كويتي، صوت امرأة**
5. **أرفق تسجيلي بصوتي**: يرسل الملف ويُبنى الفيديو عليه
6. **بدون صوت**: كابشن ومؤثرات فقط
Map: فصحى = `--dialect msa`, كويتي = `--dialect kuwait`, with `--gender male|female`; 5 = the user's own file; 6 = no voice-over, build on caption timing. If the user asks for a natural human voice (بشري), use ElevenLabs (see `iconMap-voice`); it needs his own key saved with `scripts/set_key.ps1`, so tell him that and never ask him to type the key in the chat. Without a key, use the free voice and say it is machine-made.
## Defaults the skill decides (do not ask)
| item | default |
|---|---|
| voice | chosen in Q5 above (not a default). Decision order after the choice: the user's attached recording or audio file; else ElevenLabs when the user saved a key and chose a voice (natural, see `iconMap-voice`); else a free voice (Kuwaiti-accent, male) from `scripts/voice.py`. Mention in the final reply that the text goes to Microsoft's free service. A user who asks for his own voice or another one gets it |
| duration | from the idea; if not stated: Short ≈ 30 s (about 52 words at +10% voice speed), long-form as needed |
| script | the skill writes it from the idea (see "Script" below) |
| map | vertical video: the Globe engine with real NASA satellite imagery (eferences/globe.md); horizontal or square size, or the user's own map images: the flat engine (`"basemap":{"style":"satellite"}`, drawn by code) |
| pace | by type: a new visual every 2.5-4 s; fast for Shorts, calmer for long-form |
| captions | full speech phrases at the bottom, keyword in yellow |
| music / effects | sound effects are ALWAYS on; music only if the user attaches it |
| handle | none, unless the user wrote one in the idea (then `"handle": "@name"`) |
| disputed borders | the skill checks every border it draws, and flags the sensitive ones in the final report |
| output | a new folder named after the video, next to the project |

## How the answers drive the build
| answer | what to do |
|---|---|
| Q1 | pick shot types from `references/style-guide.md` §4: 1 Establish + Build-up + pin; 2 Versus; 3 Zones + timeTag; 4 path + ruler + meridians; 5 blueprint (box, line, people, seats, number); 6 section + plume + arrow |
| Q2 | the chosen idea: topic and the places that must appear, every one highlighted on its beat |
| Q3 | set `width`/`height` at 30 fps (vertical 1080×1920, horizontal 1920×1080). Place text by lon/lat or as fractions of W/H, then check a contact sheet at THAT size |
| Q4 | wording level, examples, how much geography to explain first |

Voice and timing: free voice: `python scripts/voice.py @script.txt vo.mp3 --dialect kuwait|msa --gender male|female --rate +10%` (also writes `vo.words.json`, level -18 LUFS). Spell numbers as words in the voice text (digits can be read wrong), and show the digits on screen. Always re-transcribe the generated voice with Whisper (`python scripts/timestamps.py`, medium model if memory allows) and compare every number and name with the script before building. User audio: `python scripts/timestamps.py vo.mp3 words.json --lang ar`. Fit the script length to the target duration with a test run, then trim.
## Script (when the user gave only an idea)
1. List the claims the script needs, and verify each from a primary or official source (government, statistics office, official atlas or agency). Separate confirmed facts from estimates and opinions. Keep the wording neutral.
2. Anything that cannot be verified is left out, never used in the hook.
3. Hook in the first 2 seconds, one idea per shot, a closing line that answers the opening question.
4. Keep the sources in a separate file after the script, not in the narration.
5. Check the wording (plain Arabic, the user's own dialect, no hype).

## Final reply
Say what was made and where the files are; list the defaults that were chosen (duration, pace, captions, effects, handle) so the user can change them in one sentence; say what was checked by eye and what was not (for example the voice quality, which only a listener can judge); attach the script and the sources. Nothing is published or scheduled without the user's explicit yes.
