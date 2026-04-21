# AgentCoach "Her"-inspired Web UI

**Date**: 2026-04-20
**Ask**: Build a minimal, cinematic web frontend — white background, a single
black wave line that pulses with voice, Apple-Music-style lyric scroll below
it, end-of-session survey modal, then a precise scoring-report page.

## 1. Visual identity

| Element       | Value                                                                |
| ------------- | -------------------------------------------------------------------- |
| Background    | `#ffffff` (pure white, Her-like)                                     |
| Ink           | `#0a0a0a` (near-black for the wave and primary text)                 |
| Secondary ink | `#9e958a` warm grey (lyric fade, secondary labels)                   |
| Accent warm   | `#ddd3c4` cream — subtle dividers, card fill                         |
| Accent signal | `#e05a2b` — used *only* for "focus next" callouts in the report      |
| Type          | `ui-sans-serif, -apple-system, "SF Pro Text", "Inter", sans-serif`   |
| Type (lyric)  | `ui-serif, "New York", "Charter", Georgia, serif` at 44px → 56px     |
| Motion        | `cubic-bezier(0.22, 1, 0.36, 1)` 400–800ms — slow, cinematic         |

Everything else is whitespace. No icons except the close glyph (×) and
the play glyph on the report's replay CTA.

## 2. Pages

### 2.1 `/` Landing
Single column, vertically centered.
- Title: "AgentCoach" in the lyric serif at 48px.
- Sub: "System-design interview rehearsal." in 16px warm grey.
- Mode pill selector (Learn / Reinforce / Mock) — plain text with a thin
  underline on the active one, 40px gap between pills.
- Topic dropdown (Bitly, Ticketmaster, Rate limiter, Kafka, …).
- Name field (optional — saved as `user_id` for growth curve).
- `Begin` button — plain text, underlined, 24px.

### 2.2 `/session.html` Live
Full-bleed canvas in the centre. Top-left shows current mode + topic in
12px warm grey. Top-right shows a single `×` that ends the session.

Layout, top→bottom:
1. Mode line (12px).
2. Waveform canvas — height `max(160px, 22vh)`, full width, line only.
3. Lyric stack — bottom 35% of the viewport, centre-aligned.
   - Current line: 52px, black, opacity 1.
   - Previous line: 28px, warm grey, opacity 0.5, above current.
   - Line before that: 20px, warm grey, opacity 0.22, above previous.
   - New lines animate in from below with `translateY(12px) → 0` + fade.
4. Turn indicator (microdot): single 4×4px dot, black when the user's
   mic is hot, grey while coach is speaking, invisible otherwise.

### 2.3 Survey modal
Appears when the user taps `×` or says "end session" (and either party has
spoken at least 3 turns).
- Card 560px wide, white, 1px border `#0a0a0a`, padding 48px.
- Questions (4, 1–5 stars each): "Was the coach useful?", "Was the
  difficulty right?", "Did it feel like a real conversation?", "Would
  you practice this topic again?".
- Optional free-form 1-line field "one word that describes how this went".
- Submit button — plain underlined text "See my report".

### 2.4 `/report.html`
Loaded with `?session=<id>` once survey is submitted.
- Hero: topic + mode on top in 12px. Below, `Overall 3.8 / 5` in 72px
  black serif. Below that, a 6px-tall horizontal bar filling to 76% black.
- Dimension table — one row per rubric dimension, same layout as CLI
  `render_skill_report`: name (18px), 10-cell bar, score, evidence.
- Strengths — 3 items max, dot-bullets in black.
- Focus next — 3 items max, dot-bullets in signal orange `#e05a2b`.
- Growth curve card (if ≥ 2 prior assessments): per-dimension SVG
  sparkline with the latest point emphasised.
- Reply survey snapshot at the bottom (so we know what the user said).
- Replay CTA: "Practice this again" underline link that returns to
  `/session.html?mode=…&topic=…`.

## 3. Sound + waveform

Browser-native stack — no extra install:
- `navigator.mediaDevices.getUserMedia({ audio: true })` → `AnalyserNode`
  → reads mic amplitude while the user speaks.
- `SpeechRecognition` (Webkit) → interim + final transcripts.
- `SpeechSynthesisUtterance` for the coach voice. Because its audio is
  not exposed to an `AnalyserNode`, we drive the wave amplitude from
  the `onboundary` word events (rise on each word, exp-decay 140 ms).
- Both sources feed the same `amplitude` scalar ∈ [0, 1]. A single
  `requestAnimationFrame` loop draws a centred cosine wave whose
  envelope is the smoothed amplitude, using a Perlin-ish phase shift
  so it never looks purely sinusoidal (more alive, still minimal).

## 4. Backend

Stdlib `http.server` (no new dep):
- `POST /api/session/start   {mode, topic, user_id?}` → `{session_id, opening}`
- `POST /api/session/turn    {session_id, user_text}` → `{coach_text}`
- `POST /api/session/end     {session_id, survey?}`  → scoring payload:
  ```json
  {
    "overall_score": 3.8, "mode": "mock_system_design",
    "topic_id": "system_design.url_shortener",
    "dimensions": [{name, score, evidence}, …],
    "strengths": [...], "areas_to_improve": [...],
    "mastery_before": 42, "mastery_after": 51,
    "growth": {dim: [values, ...]}
  }
  ```
- `GET  /api/session/{id}/report` → same payload (idempotent reload).
- Static file serving for `/*` from `frontend/`.

Under the hood the backend reuses `Coach`, `Scorer`, `AnalyticsStore`,
and `render_skill_report` — no new ML code.

## 5. Graceful fallback

- If `OPENAI_API_KEY` / Ollama is missing, the backend returns a fixed
  demo script so the UI is still explorable.
- The frontend also ships a `mockMode` flag in `api.js`: when the backend
  isn't reachable it falls back to a scripted conversation so a reviewer
  can load `file://.../frontend/session.html?demo=1` and see the wave +
  lyrics dance with canned text.

## 6. Out of scope for this pass

- Multi-user auth / accounts — single local user, keyed by name.
- Real-time streaming coach output (TTFB) — v2.
- Mobile tuning — responsive but desktop-first.
