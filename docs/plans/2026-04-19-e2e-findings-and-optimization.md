# AgentCoach — End-to-End Audit & Optimization Spec

**Date:** 2026-04-19
**Scope:** System Design domain, HelloInterview content, gemma4:31b coach
**Method:** `scripts/roleplay_e2e.py` — 12 sessions = 4 scenarios × 3 candidate levels
**Results report:** `e2e_report_20260419_235826.json`

---

## 1. Headline results

Overall 3.95 / 5 from an LLM judge (gpt-4o-mini) using an 8-axis rubric.

| Axis                    | Score | Verdict |
|-------------------------|-------|---------|
| topic_discipline        | 5.00  | Perfect — the `TOPIC_CONSTRAINT` block works |
| mode_fidelity           | 4.67  | Strong — learn teaches then quizzes, mock runs a real SD interview |
| difficulty_calibration  | 4.17  | Good — junior gets analogies, senior gets trade-offs |
| conversational_tone     | 4.17  | Good — short TTS-friendly replies |
| error_handling          | 3.75  | Middling — too agreeable with vague answers |
| followup_depth          | 3.75  | Middling — mostly 1 probe, rarely 2–3 |
| kb_grounding            | 3.33  | **Weak** — coach rarely cites specific numbers / patterns |
| closing_quality         | 2.75  | **Weakest** — sessions end mid-thought, no summary, no score |

Per mode: `reinforce 4.21 > learn 4.17 > mock_system_design 3.71`.
Per level: `intermediate 4.03 > junior 3.91 ≈ senior 3.91`.

---

## 2. 360° Defect Inventory

### DEF-01 — Sessions end without summary/score  (severity: HIGH, 9 / 12 sessions)

Every mode template says "provide feedback with a score (1–10)" at the end,
but the coach has no notion of "end". In a turn-bounded test (or a user who
closes the CLI) the session just stops mid-drilldown. The `Coach` class
already has `get_feedback_summary()` that the CLI calls on exit, but:

- the CLI's `_run_session` decides when to exit (user command), not the coach;
- the coach never self-signals readiness to wrap up;
- in a mock interview the score+feedback is the *point* — without it the
  session has no take-home value.

Judge verbatim: "absence of closing reduces the overall effect", "ended
abruptly without an actionable summary or score", appearing across all modes.

### DEF-02 — KB grounding is 2.67 in mock mode, 4.0 in learn/reinforce  (severity: HIGH)

For learn / reinforce we pipe `kb_teaching_context` into the system prompt.
For `mock_*` we explicitly do not — `kb_teaching` is `""`. The coach therefore
runs the Bitly / Rate-Limiter / Ticketmaster interviews on priors alone, and
misses the HelloInterview canonical numbers / patterns (e.g. 1B URLs, 100M
DAU, Base62, 1000:1 read/write ratio for Bitly; Redis sorted-set with
`INCR+EXPIRE` for rate limiter; virtual waiting-room + seat-hold TTL for
Ticketmaster).

Judge verbatim: "missed opportunities to introduce concrete examples or best
practices", "more specific examples or grounding for the discussion".

Root cause: `cli/main.py` only pre-fetches KB for `mode == "learn"`, and
`Coach.respond` uses `kb_store` for per-turn context but the projection into
the system prompt is `kb_teaching_context`, which mock mode never gets.

### DEF-03 — Follow-ups are one-deep  (severity: MEDIUM)

Mock system-design follow-up depth is 3.5. The coach asks a probe, accepts
the first reasonable answer, and moves on. A senior-level mock should drill
2–3 levels deep ("you said X — *why not Y?* — what breaks at 10× scale?").

Root cause: templates mention "1–2 follow-ups" but don't specify the
drill-down pattern; coach LLM defaults to breadth over depth.

### DEF-04 — Vague answers under-pushed  (severity: MEDIUM)

Error-handling axis lowest in learn mode (3.33): when junior answers "it kind
of like puts it in a storage box", coach validates ("Exactly.") instead of
pinning down the term ("What do we actually call that — durability,
persistence, replication? Which one matches what Kafka guarantees?").

Root cause: no explicit "challenge imprecise language" rule in templates.

### DEF-05 — Mock mode loses context-specific numbers  (severity: MEDIUM)

Even when KB content exists, the coach paraphrases in generic terms. E.g.
Bitly mock stayed at "high availability, ~100ms latency" generic, never
quoted "1B URLs / 100M DAU" from the HelloInterview breakdown.

Intertwined with DEF-02, but also calls for a "quote a concrete number from
reference material at least once" rule in the mock template.

### DEF-06 — Topic calibration gap for senior (error_handling 3.5)  (severity: LOW)

With senior candidates the coach over-praises and under-challenges. Deeper
probes and contrarian pushback are expected from a real Staff-level
interviewer.

### DEF-07 — Coach occasionally truncated mid-sentence  (severity: LOW, fixed in test harness)

With 31b + OpenAI-compat, thinking tokens ate the `max_tokens` budget; this
was rediscovered in the harness and fixed by switching to the Ollama native
`/api/chat` endpoint with `think: false`. **This is a finding about the
production `LLM_PROVIDER=ollama` path too** — users running the real CLI on
Gemma 4 will get occasional empty coach replies today.

### DEF-08 — `quiz_active` detection never fires in learn mode ≥ short sessions  (severity: LOW)

`Coach._update_quiz_state` relies on `detect_quiz_start` heuristics. In our
5-turn learn sessions the quiz never started, so difficulty calibration code
paths stayed dormant. Short sessions run out of turns before the coach
transitions "teach → quiz".

### DEF-09 — HelloInterview scrape is a table-of-contents for 6 of 9 SD files  (severity: MEDIUM, data)

Files that are <8 KB are essentially TOC + comment spam — the article body
was not captured by the scraper. Affects `core-concepts_caching.md`,
`deep-dives_redis.md`, `core-concepts_cap-theorem.md`,
`core-concepts_consistent-hashing.md`, `core-concepts_sharding.md`.
Only problem-breakdowns and the Kafka deep dive have usable body text.

---

## 3. Optimization Spec

Each change below is ordered by expected score lift. `S:` is severity (of the
defect it targets), `L:` is expected axis lift, `R:` is risk.

### OPT-1  Auto-wrap with summary+score at end of session  (S:H, L:closing +1.5, R:low)

**Change in `Coach` + runner API**: add `Coach.wrap_up() → str` that always
produces:

- two-sentence recap of what was covered
- top-3 strengths (evidence-linked)
- top-3 improvement areas (evidence-linked)
- 1–10 score with one-line rationale

Implementation:
1. New instruction block `MOCK_CLOSING_INSTRUCTION` appended to the message
   list (not to the system prompt) when `wrap_up` is called, overriding
   normal Q&A behaviour for one turn.
2. `scripts/roleplay_e2e.py` calls `coach.wrap_up()` on the final turn and
   records the result in the transcript so the judge sees it.
3. `cli/session.py` optionally calls `wrap_up()` when the user types `done`
   or `end` (falls back to `get_feedback_summary`).

### OPT-2  Inject KB reference context into mock mode  (S:H, L:kb_grounding +1.0, grounding +0.5 follow-up, R:low)

**Change in `cli/main.py` + `prompt/templates.py`**:

1. When `mode == "mock_system_design"` (and other mock modes) also pre-fetch
   top-K KB hits for the chosen problem, same as learn mode does.
2. Format them into a new section `MOCK_REFERENCE_SECTION`:

   ```
   ## Reference Material (interviewer cheat-sheet)
   You are the interviewer. Use these reference numbers, patterns, and
   gotchas to probe the candidate and to push back on weak answers. Do NOT
   read this content to the candidate verbatim — use it to ASK.
   ```

3. `build_system_prompt` gains a `mock_reference_content` kwarg mirroring
   `kb_teaching_content`.

### OPT-3  Drill-down rule in mock templates  (S:M, L:followup +0.7, R:low)

Add to `MOCK_SYSTEM_DESIGN_PROMPT` (and variants):

- "When the candidate answers, do TWO probes before moving on: (a) *why this
  over the obvious alternative?* (b) *what breaks at 10× the stated scale?*"
- "Accept a move-on only after the candidate has named at least one
  concrete trade-off."

### OPT-4  Imprecise-language challenge rule  (S:M, L:error_handling +0.5, R:low)

Add a universal rule to `LEARN_PROMPT`, `REINFORCE_PROMPT`, and the mock
templates:

> "If the candidate uses vague or colloquial words ('kind of', 'something
> like', 'stuff that does X'), ask them to restate using the correct
> technical term before you agree."

### OPT-5  Always quote one concrete number/pattern per mock turn  (S:M, L:kb_grounding +0.5, R:low)

Add to mock templates:

> "Each of your prompts should surface at least one concrete number, name,
> or pattern (e.g. '100 M DAU', 'Redis sorted set', 'Base62', 'consistent
> hashing with virtual nodes') — drawn from the reference material if
> provided, or from your own knowledge otherwise."

### OPT-6  Fix Gemma 4 thinking-vs-content collision in the production adapter  (S:L→prod-H, L:robustness, R:low)

Currently the production `ollama` path uses `OpenAICompatAdapter`, which
*does not* honour `think: false` and silently loses content to reasoning
tokens when `max_tokens` is tight. Fix:

1. Create `agentcoach/llm/providers/ollama_provider.py` that wraps
   `/api/chat` with `think: false` by default (configurable via
   `OLLAMA_THINK=1` for debugging).
2. Update `agentcoach/llm/router.create_provider` to select the new provider
   when `provider_name in {"ollama", "ollama-small"}`.
3. Keep `OpenAICompatAdapter` as fallback for non-Gemma OpenAI-compat
   servers.

### OPT-7  Quiz-start heuristic + explicit phase marker  (S:L, L:mode_fidelity robustness, R:medium)

Add a lightweight phase tracker:

- After 3 exchanges or a "ready for quiz"-ish user cue, the coach tags its
  reply with a hidden `<phase>quiz</phase>` token.
- The coach code strips the token before display but uses it to flip
  `QuizState._quiz_active`.

Keeps current `detect_quiz_start` as fallback.

### OPT-8  Re-scrape the thin HelloInterview core-concepts  (S:M, data, R:low)

Run `scripts/scrape_hellointerview.py` against the 5 files that came back as
TOCs. Alternatively, fall back to the DDIA-style prose inside the
`blog/`/`deep-dives_*` directories. Not required for today's scoring, but
unblocks `learn` sessions for caching / CAP / consistent hashing.

---

## 4. Tight implementation plan (today)

Order by impact / effort:

1. **OPT-1** and **OPT-2** — ship together. They move the two weakest axes.
2. **OPT-3, OPT-4, OPT-5** — single template edit.
3. **OPT-6** — real production-path fix, small file.
4. Re-run `scripts/roleplay_e2e.py` with the same seed (4 scenarios × 3
   levels, 5 turns) and confirm:
   - `closing_quality` ≥ 4.0
   - mock `kb_grounding` ≥ 3.5
   - `followup_depth` ≥ 4.0
   - no regressions on `topic_discipline` / `mode_fidelity`.

OPT-7 and OPT-8 deferred; track as follow-ups.

---

## 5. Test harness findings (independent of coach quality)

- `scripts/roleplay_e2e.py` is now the canonical E2E rig. It wraps the real
  `Coach` class, uses the real `KnowledgeStore`, feeds in real
  HelloInterview markdown, and judges every session with an LLM auditor.
- Latency on gemma4:31b with `think: false` is ~12 tok/s → ~15 s per coach
  turn — acceptable for interactive use.
- Voice path confirmed working with `say` — Samantha / Daniel / Karen / Alex
  correctly differentiate speakers.

