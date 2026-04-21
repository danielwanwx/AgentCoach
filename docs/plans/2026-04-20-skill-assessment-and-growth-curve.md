# Skill Assessment & Growth Curve System

**Date**: 2026-04-20
**Author**: coach-eval loop
**Source**: 12-session realistic sweep (`e2e_report_20260420_115540.json`), overall 4.07/5
**Requested by**: user — "产生 candidate 技能评估报告 + 看生成逻辑是否精准 + 自我评估曲线 + 记住用户 skill"

---

## 1. Current state (what already works)

| Layer                              | File                                             | Does it exist? | Notes                                                                                     |
| ---------------------------------- | ------------------------------------------------ | -------------- | ----------------------------------------------------------------------------------------- |
| Per-domain dimension rubrics       | `agentcoach/scoring/rubrics.py`                  | ✅              | 4 rubrics × 4–5 dims × 1–5 level descriptors                                              |
| LLM scorer (produces dims + delta) | `agentcoach/analytics/scorer.py`                 | ✅              | Emits `{overall_score, dimensions[], strengths, areas_to_improve}` but **drops dims**     |
| Mastery store (events → decay)     | `agentcoach/analytics/store.py`                  | ✅              | Records only `score_delta` per topic. Dimensions **not persisted**.                       |
| Progress dashboard                 | `agentcoach/cli/session.py::_show_progress_dashboard` | ✅            | Aggregates mastery by domain/topic but no dimensions, no trend, no growth curve           |
| Session wrap-up (coach-written)    | `agentcoach/coaching/coach.py::wrap_up`          | ✅              | Prose RECAP/STRENGTHS/IMPROVE/SCORE — candidate-visible but not machine-readable          |
| Judge (coach-quality only)         | `scripts/roleplay_e2e.py::judge_session`         | ✅              | Scores **the coach**, not the candidate                                                   |

### Gap analysis

1. **Dimension data is thrown away.** `Scorer` already returns dimensions, but `_score_and_save` only writes `topic_id, score_delta, mode, evidence` to `score_events`. Dimensions, strengths, areas_to_improve, and overall_score are never persisted ⇒ we cannot render a growth curve for "trade-offs" or "deep-dive".
2. **No candidate-facing report.** After a session the user sees a prose wrap-up and a mastery bar — there is **no structured skill report** with per-dimension bars, weaknesses, or study recommendations.
3. **No trajectory view.** We cannot answer "has the user's `deep_dive` score improved over the last 5 sessions?" because dimensions are not stored and there is no trajectory renderer.
4. **No accuracy verification.** We never cross-check whether the scorer's `overall_score` agrees with independent signals (coach wrap-up SCORE, judge verdict, human intuition). The scorer prompt has never been calibrated against a held-out set.
5. **E2E harness never exercises the scorer.** `scripts/roleplay_e2e.py` runs only the coach+judge path. The candidate-scoring path (which is what a real user experiences) is never tested end-to-end.

---

## 2. Target: Skill Assessment & Growth Curve

### 2.1 User-facing deliverables

1. **Structured Skill Report** printed at the end of every session:
   ```
   === Skill Report: Message Queues with Kafka (learn) ===
   Overall: 3.4/5   Mastery: 42% → 51% (+9)
   
   Requirements       ███████░░░  4/5   "Clarified QPS + retention scope"
   High-level design  ██████░░░░  3/5   "Listed components but vague on partition routing"
   Deep dive          █████░░░░░  2/5   "Could not explain ISR or replication factor"
   Scalability        ███████░░░  4/5   "Cited 100k QPS baseline"
   Trade-offs         █████░░░░░  2/5   "Hedged on durability vs latency"
   
   Strengths
     • Solid grasp of topic/partition vocabulary
   Focus next
     • Replica lag and acknowledgement modes
     • Latency-vs-durability trade-off framing
   ```

2. **Skill Growth Curve** via `progress` command (or new `skills` command):
   ```
   === Skills — System Design ===
   requirements       4.2 ▂▄▅▆▇      (↑ from 2.8 over 5 sessions)
   high_level_design  3.1 ▄▅▃▄▄      (flat)
   deep_dive          2.6 ▂▃▂▃▄      (↑ from 1.8)
   scalability        3.8 ▃▄▅▅▆      (↑ from 2.5)
   tradeoffs          2.3 ▂▂▃▂▃      (slow climb)
   ```

3. **Per-archetype skill report in E2E harness** — after the 12-session sweep we aggregate each persona's dimensions so we can see, e.g., that `senior_overconfident` scores 4.5 on high-level design but 2.1 on trade-offs.

### 2.2 Internal machinery

**New table** `skill_assessments`:
```sql
CREATE TABLE skill_assessments (
  id              INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id         TEXT    NOT NULL,
  topic_id        TEXT    NOT NULL,
  domain          TEXT    NOT NULL,
  mode            TEXT    NOT NULL,
  session_id      TEXT,
  overall_score   REAL    NOT NULL,
  dimensions_json TEXT    NOT NULL,  -- [{name, score, evidence}]
  strengths_json  TEXT,
  areas_json      TEXT,
  created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_assess_user_topic ON skill_assessments(user_id, topic_id);
CREATE INDEX idx_assess_user_domain ON skill_assessments(user_id, domain);
```

**New module** `agentcoach/analytics/skill_profile.py`:
- `SkillProfile(user_id, domain)` → per-dimension current + trend + history
- `render_skill_report(assessment)` → text block for end-of-session output
- `render_growth_curve(profile)` → ASCII sparkline trajectories
- Uses `get_rubric(domain)` so dimension names + weights come from a single source of truth

**Hook points**:
- `agentcoach/cli/session.py::_score_and_save` — after `Scorer.score_session`, also call `store.record_assessment(...)` with the full dict, then `print(render_skill_report(...))`.
- `agentcoach/cli/session.py::_show_progress_dashboard` — call `render_growth_curve` next to the existing mastery bars.
- `scripts/roleplay_e2e.py::run_session` — run the Scorer on each candidate transcript, aggregate by persona, dump into the report JSON.

### 2.3 Accuracy verification

**Method**: replay today's 12 transcripts through `Scorer.score_session`, then compare the scorer's `overall_score` against:
1. The wrap-up `SCORE` (1–10 scale, normalize to 1–5).
2. The judge's mean of coaching-axis scores (proxy — not a perfect ground truth but a sanity check).

**Pass criteria**:
- Mean absolute error (scorer vs wrap-up) ≤ 0.6 on a 1–5 scale.
- No single session with |delta| > 1.5 between scorer and both references.
- Per-dimension scores fall in [1,5] integer range in ≥95% of calls (guards against JSON-shape regressions).

If any criterion fails, iterate on `SCORE_PROMPT` (e.g., add anchor examples) and re-run.

---

## 3. Remaining coach-side gaps from last sweep (carry-over work, not this PR's primary goal)

| Defect                                                                 | Symptom in 115540 run      | Proposed fix                             |
| ---------------------------------------------------------------------- | -------------------------- | ---------------------------------------- |
| `followup_depth` mean 3.17 — coach asks once and moves on              | transcript turns 6–10      | Force two-probe rule in mock templates   |
| `kb_grounding` mean 3.17 — concrete numbers rarely cited in mock mode  | Bitly/Ticketmaster mocks   | Inject `MOCK_REFERENCE_SECTION` numbers  |
| Wrap-up SCORE occasionally on 1–10 despite rubric being 1–5            | 3/12 sessions              | Tighten wrap-up prompt, add post-parse normalization |

These three are tracked separately and are **not blocking** the skill-report work, because the report consumes whatever the scorer emits regardless of coach behaviour.

---

## 4. Implementation order

1. **P1 — persistence**: extend `AnalyticsStore` with `skill_assessments` + `record_assessment`, `get_skill_history`, `get_skill_profile`. Backwards-compatible.
2. **P1 — renderer**: `agentcoach/analytics/skill_profile.py` — `SkillProfile`, `render_skill_report`, `render_growth_curve`.
3. **P1 — CLI hook**: `_score_and_save` writes full assessment + prints report; `_show_progress_dashboard` gains a "Skills" section.
4. **P2 — E2E hook**: harness runs scorer on every candidate transcript; aggregate per-persona + per-scenario; dump into report JSON.
5. **P2 — accuracy test**: `scripts/verify_skill_assessor.py` loads today's report, replays all 12 transcripts through the scorer, prints MAE table against wrap-up SCORE, decides pass/fail per §2.3.
6. **P3 — tests**: unit tests for store round-trip, renderer snapshot, and an integration test that runs scorer against a fixture transcript.

---

## 5. Out of scope (intentionally)

- Web/UI dashboard — CLI only for this pass.
- Cross-user anonymized benchmarking — requires privacy work.
- Automatic curriculum recommendations off the dimension gaps — `recommender.py` already exists; we'll feed it dimension data in a follow-up.
