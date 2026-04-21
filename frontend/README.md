# AgentCoach Web UI

A cinematic, Her-inspired web front-end for AgentCoach. White room, a single
black wave that pulses with voice, Apple-Music-style lyric scroll, survey on
session end, then a detailed HTML scoring report.

## Run

From the repo root:

```bash
# Demo mode — no LLM needed, scripted coach, stub-but-real scoring curve.
python -m agentcoach.web.server --port 8765 --demo

# Real mode — uses your existing LLM_PROVIDER / OPENAI_API_KEY env.
python -m agentcoach.web.server --port 8765
```

Then open <http://127.0.0.1:8765/>.

## Flow

1. Landing picks mode (Learn / Reinforce / Mock) + topic.
2. Session page opens: mic-driven wave, coach speaks via `SpeechSynthesis`,
   your words are transcribed with `SpeechRecognition`. Hold the space-bar
   (or tap the bottom-right button) to talk.
3. Tap × top-right to end. A survey modal appears.
4. Submit → report page with overall score, per-dimension bars + evidence,
   strengths, focus-next, and per-dimension growth sparklines across all
   your prior sessions (keyed by the name you typed on the landing page).

## Files

| File                          | Purpose                                   |
| ----------------------------- | ----------------------------------------- |
| `index.html`                  | Landing (mode + topic picker)             |
| `session.html` + `session.js` | Live wave + lyrics + survey modal         |
| `report.html` + `report.js`   | Detailed scoring report                   |
| `assets/app.css`              | All styling                               |
| `assets/wave.js`              | Black-wave audio-reactive canvas          |
| `assets/api.js`               | Backend client with offline demo fallback |

## Browsers

Chrome / Edge / Safari on macOS are best — Safari ships the highest-quality
voices. Firefox has no Web Speech Recognition, so the wave + coach TTS will
still work but you'll need to type instead of talk (future work).
