# AI production pack — "Nobody Told Me When"

Five prompts. Paste, generate, assemble. Read the traps section first — two of them will ruin
the ad if you don't plan around them.

---

## The two traps

**1. AI cannot render text.** Ask a video model for "a pamphlet showing 8.50%" and you get
something that looks like a number and isn't. Every figure, date and URL in this film must be
**overlaid in post**, using the files in `ads/film-assets/`.

**2. AI cannot render hands.** Fingers multiply, thumbs bend backwards. So: never ask for hands
doing something delicate. Frame them at the edge of shot, in shadow, or half out of frame — or
cut away and let the *paper* carry the shot.

Everything below is written around those two limits.

---

## The look — one paragraph to anchor every prompt

> Warm late-evening light from a single low lamp on the left, deep shadows on the right, a wooden
> table, off-white paper, muted palette of cream and deep green, shot on 35mm film, shallow depth
> of field, gentle grain, no text anywhere, no logos.

Paste that into every prompt. It's what makes five separate clips look like one film.

---

## Tool setup

| Need | Tool | Notes |
|---|---|---|
| Video from an image | **Kling 2.x** or **Runway Gen-4** | Cheapest path that holds consistency |
| Video from text | **Veo 3** (via Flow) | Best light and physics, fewer credits |
| Stills first | **Flux** or **Ideogram** | Generate the frame, then animate it |
| Voice | **ElevenLabs** | Indian English female, style 0 |

**Recommended route:** generate a still for each shot (Flux/Ideogram), then animate that still in
Kling/Runway for 5 seconds. Image-to-video is far more controllable than text-to-video, and it
keeps the lighting identical across shots.

---

## The character

Meera appears in shots 3 and 5 only. Copy this description **verbatim** into both prompts — any
change of wording and you get a different person:

> an Indian woman in her mid-thirties, medium-brown skin, dark hair tied back loosely, no makeup,
> wearing a plain cotton kurta in muted olive, sitting at a wooden table, tired but composed,
> natural skin texture, no jewellery

---

## Shot 1 — The pamphlet (0:00–0:08)

**Image prompt:**
> Overhead close-up of a crumpled cream-coloured paper pamphlet lying on a warm wooden table, single
> lamp light from the left raking across the creases, deep shadow on the right, off-white paper,
> shallow depth of field, 35mm film grain, no text, no logos, no hands.

**Motion prompt:** `very slow push in, paper texture catching the light, dust motes drifting`

**Negative:** `text, letters, numbers, hands, fingers, logo, watermark`

**Length:** 5s (slow it to 8s in the edit)
**Trap note:** no hands at all. The film starts on the paper, not on someone touching it.

---

## Shot 2 — Three papers (0:08–0:20)

**Image prompt:**
> Overhead shot of three sheets of paper overlapping on a wooden table — a creased pamphlet, a
> printout of a phone screenshot, a page torn from a lined notebook with handwriting in blue ink,
> warm lamp light from the left, cream and grey palette, 35mm film grain, no readable text, no
> hands.

**Motion prompt:** `almost still, faint paper movement, light shifting slightly, camera locked`

**Length:** 5s, loop or slow to 12s
**Trap note:** the handwriting will be gibberish — that's fine, it's out of focus and the overlay
carries the meaning.

---

## Shot 3 — Her exhale (0:20–0:28)

**Image prompt:** *character paragraph* + 
> medium shot, chest up, sitting at a wooden table with papers in front of her, single warm lamp
> from the left, half her face in shadow, dark room behind, 35mm film grain, shallow depth of field.

**Motion prompt:** `she looks down at the papers, exhales slowly, small tired almost-laugh, then
reaches for a pen, natural micro-movements, no camera movement`

**Negative:** `talking, smiling broadly, crying, exaggerated expression, camera shake`

**Length:** 5s, generate **4 attempts** — this is the hardest shot and the one that decides the film.
**Trap note:** reject any take where the face morphs or the eyes drift. A slightly too-still take
beats a melting one.

---

## Shot 4 — Turning the papers (0:28–0:38)

**This is the shot the whole ad turns on, and AI will fight you.** Don't fight back — split it:

**4a — generate:** 
> overhead close-up of a paper being flipped over on a wooden table, motion blur, warm lamp light,
> cream paper, hands only at the very edge of frame and out of focus, 35mm grain, no text.

**4b — overlay (the important part):** the three PNGs in `ads/film-assets/dates-*.png`, one per
flip, each fading in over 0.4s and holding. Positioned bottom-left.

Time the overlays to your flip, not the other way round. The date appearing **after** the paper
lands is what makes it feel like a discovery.

---

## Shot 5 — The laptop (0:38–0:50)

**5a — generate:**
> over-the-shoulder shot of the same Indian woman opening a laptop on the wooden table, screen
> dark, warm lamp light from the left, dark room, 35mm grain, shallow depth of field, no text.

**Motion prompt:** `her hands open the lid, screen stays dark, she leans back slightly`

**5b — cut to** `ads/film-assets/insert-laptop-screen.mp4` — full frame, 6 seconds. That's the properly
rendered rates page with 8.20%, the date and the source link.

**5c — generate:**
> close-up of a laptop lid closing, warm lamp light, cream and deep green palette, 35mm grain.

**Never ask AI for a screen with content.** It will produce convincing nonsense. The insert exists
precisely so you don't have to.

---

## Shot 6 — End card

Not generated. Use `ads/film-assets/endcard.mp4` — 4 seconds, already labelled and on-brand.

---

## Order of work

1. **Voiceover first.** ElevenLabs, Indian English female, stability 0.7, style 0, speed 0.9, both
   languages. Export `vo-english.mp3`, `vo-hindi.mp3`.
2. **Stills.** Generate all five frames. Iterate on the stills until they look right — it's far
   cheaper to fix a still than a clip.
3. **Animate.** Image-to-video, 5 seconds each. Three attempts per shot; keep the best.
4. **Assemble.** CapCut or Premiere: clips in script order, date supers on shot 4, screen insert at
   0:38, end card at 0:50, voiceover on top.
5. **Or send it to me.** Drop the clips and audio in a folder and I'll cut, sync, and mux both
   language versions here with ffmpeg.

---

## Budget expectation

At roughly ₹40–80 per 5-second clip on Kling or Runway, five shots with three attempts each is
**₹600–1,200 per film**, plus a free ElevenLabs tier for the voice.

Start with **shot 3 only**. If you can get a believable exhale, the film works and the rest is easy.
If shot 3 keeps looking wrong after five attempts, stop and shoot it on a phone — a real face at
1080p beats a generated one, and it's the only shot where that's true.
