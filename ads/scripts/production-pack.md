# Production pack — "Nobody Told Me When"

Everything you need to shoot and voice the film. Assets are in `ads/film-assets/`.

---

## Part 1 — The five shots

**Phone settings, once:**

- **4K at 30fps** if your phone allows (1080p is fine if not)
- **Portrait**, 9:16
- **Lock exposure and focus** by long-pressing on the paper (this is the single biggest quality difference)
- **Turn off HDR** if you can — it wrecks the warm-lamp look
- Wipe the lens. Genuinely.

**Set-up, once:**

- A wooden or plain table, cleared
- **One lamp**, low and to the left, at about 45°. Turn off the ceiling light — that flat overhead light is what makes phone footage look cheap
- Shoot in the evening with a curtain half-closed; mixed warm lamp + cool window is the whole look
- Camera on a stack of books or a tripod. **No handheld** except shot 3.

---

### Shot 1 — The pamphlet (0:00–0:08)

**Frame:** Top-down. Paper fills about 70% of the frame, edges visible.
**Action:** Hands enter, flatten a crumpled pamphlet. It does not sit flat. Hold still for 6 seconds.
**Length:** 10 seconds — you need a clean 6.
**Tip:** Crumple the paper the day before so the creases are real.

### Shot 2 — Three papers (0:08–0:20)

**Frame:** Top-down. Three sheets overlapping slightly: pamphlet, phone screen (WhatsApp forward), notebook page.
**Action:** None. Stillness. The camera does not move.
**Length:** 12 seconds.
**Note:** For the phone, screenshot a fake forward on your own phone and display it at low brightness so it photographs evenly.

### Shot 3 — Her exhale (0:20–0:28)

**Frame:** Medium shot, chest up, sitting at the table. Lamp from the left, face half-lit.
**Action:** She looks down at the papers, breathes out — small, tired, almost a laugh — then picks up a pen.
**Length:** 12 seconds.
**This is the only handheld-adjacent shot.** Put the phone on something, but let her move naturally inside frame.
**Casting:** A friend or family member, 30–40. No makeup, no jewellery that catches light, ordinary clothes. **Do not let her act** — ask her to actually read the papers and react.

### Shot 4 — Turning the papers (0:28–0:38)

**Frame:** Top-down, hands only.
**Action:** Hand turns each sheet over in sequence, revealing the printed date on the back. Three sheets, three turns, evenly spaced.
**Length:** 14 seconds — one turn every ~4 seconds.
**Critical:** The dates must be **printed on the back of the actual paper**. Print `ads/film-assets/dates-*.png` onto paper at small size (about 2 cm tall) and stick them on. Small print is the point.

### Shot 5 — The laptop (0:38–0:50)

**Frame:** Over the shoulder, then cut to the screen itself.
**Action:** She opens the laptop. Hand scrolls once. Nothing else.
**Length:** 12 seconds.
**Important:** Do **not** film a real screen — phone cameras produce moiré and colour banding. Instead:
1. Film her hands and the laptop lid open, screen off
2. Cut to `insert-laptop-screen.mp4` (I built it) full-frame for 6 seconds
3. Cut back to her closing the lid

That cut is standard practice and it looks professional.

---

## Part 2 — Voiceover

Record in **ElevenLabs**. Free tier is ~10 minutes a month — enough for both languages.

**Voice choice:** search for an **Indian English female** voice. Low, unhurried, close to the mic. Do not pick anything bright or "commercial".

**Settings that matter:**

| Setting | Value | Why |
|---|---|---|
| Stability | **0.65–0.75** | Too low makes it theatrical; too high makes it flat |
| Similarity | 0.75 | Default is fine |
| Style | **0** (off) | Style exaggeration is what makes AI voices sound fake |
| Speed | **0.9** | Slightly slow. The script needs air |

**Direction:** read it like you're telling one friend something you just found out. Not to a room. Not to a camera.

---

### English (54 words, ~28 seconds)

| Time | Line |
|---|---|
| 0:00 | Everyone had a number for me. |
| 0:08 | My bank said one thing. My cousin said another. |
| 0:20 | They were all telling the truth. |
| 0:28 | They just never told me when. |
| 0:38 | A rate without a date isn't a fact. It's a guess. |
| 0:50 | PaisaClear. Every figure dated. Every figure sourced. Before you put money in. |

### Hindi (~30 seconds)

| Time | Line | Transliteration |
|---|---|---|
| 0:00 | सबके पास मेरे लिए एक आंकड़ा था। | Sabke paas mere liye ek aankda tha. |
| 0:08 | बैंक कुछ कहता था, चचेरा भाई कुछ और। | Bank kuch kehta tha, chachera bhai kuch aur. |
| 0:20 | वो सब सच कह रहे थे। | Wo sab sach kah rahe the. |
| 0:28 | फ़र्क़ सिर्फ़ ये था — कब का सच? | Farq sirf ye tha — kab ka sach? |
| 0:38 | बिना तारीख़ की दर, तथ्य नहीं, अंदाज़ा है। | Bina taareekh ki dar, tathya nahin, andaaza hai. |
| 0:50 | PaisaClear. हर आंकड़ा तारीख़ के साथ। हर आंकड़ा स्रोत के साथ। पैसा लगाने से पहले। | PaisaClear. Har aankda taareekh ke saath. Har aankda srot ke saath. Paisa lagane se pehle. |

**Hindi note:** keep "PaisaClear" in English. Do not transliterate it. Say "तारीख़" with the soft kh — if the voice butchers it, use "तारीख" without the nukta.

---

## Part 3 — Assembly timeline

| Time | What | Source |
|---|---|---|
| 0:00–0:08 | Hands flatten pamphlet | your shot 1 |
| 0:08–0:20 | Three papers, still | your shot 2 |
| 0:20–0:28 | Her exhale | your shot 3 |
| 0:28–0:38 | Turning papers + date supers | your shot 4 + `dates-as-on-*.png` |
| 0:38–0:50 | Laptop opens → screen insert | your shot 5 + `insert-laptop-screen.mp4` |
| 0:50–0:60 | End card | `endcard.mp4` |

**Date supers:** place `dates-as-on-01-04-2021.png`, `dates-as-on-2022.png`, `dates-as-on-2023.png` over shot 4, one per turn, each fading in over 0.4s and holding until the next turn. They are transparent PNGs at 1080×1920 — drop them on their own track.

---

## Part 4 — What to send me

When you have them, put everything in one folder and tell me the path:

- `shot1.mp4` … `shot5.mp4` (or any names — just list them)
- `vo-english.mp3`, `vo-hindi.mp3`

I'll cut the film to the script, sync each line to its beat, place the supers and end card, add crossfades, and hand you two finished files: one English, one Hindi.
