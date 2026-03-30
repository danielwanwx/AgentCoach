# Phase B: Three Modes Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Implement Learn, Reinforce, and Mock mode handlers with mode-specific prompts and post-session scoring that updates analytics.

**Architecture:** Each mode has a dedicated prompt template and session handler. After each session, the Scorer uses LLM to extract per-topic scores from the conversation and updates AnalyticsStore.

**Tech Stack:** Existing Coach engine, AnalyticsStore, SyllabusLoader, LLM adapters

---

### Task 1: Mode-Specific Prompt Templates

**Files:**
- Modify: `agentcoach/prompt/templates.py`
- Create: `tests/test_mode_prompts.py`

**Step 1: Write tests**

```python
# tests/test_mode_prompts.py
from agentcoach.prompt.templates import get_coach_system_prompt

def test_learn_prompt():
    prompt = get_coach_system_prompt("learn")
    assert "quiz" in prompt.lower() or "question" in prompt.lower()
    assert "resource" in prompt.lower() or "study" in prompt.lower()

def test_reinforce_prompt():
    prompt = get_coach_system_prompt("reinforce")
    assert "follow" in prompt.lower() or "deeper" in prompt.lower()

def test_mock_system_design_prompt():
    prompt = get_coach_system_prompt("mock_system_design")
    assert "interview" in prompt.lower()
    assert "design" in prompt.lower()

def test_mock_algorithms_prompt():
    prompt = get_coach_system_prompt("mock_algorithms")
    assert "algorithm" in prompt.lower() or "coding" in prompt.lower()

def test_mock_ai_agent_prompt():
    prompt = get_coach_system_prompt("mock_ai_agent")
    assert "agent" in prompt.lower() or "llm" in prompt.lower()
```

**Step 2: Add prompts to templates.py**

READ `agentcoach/prompt/templates.py` first. Add new prompt constants and register them in TEMPLATES dict.

LEARN_PROMPT: You are a study coach. First present the learning resources to the user. When they say "ready", ask 3-5 knowledge-check questions one at a time. Judge each answer immediately — say if correct/incorrect and give a brief explanation. After all questions, give an overall assessment.

REINFORCE_PROMPT: You are a practice coach reinforcing a specific topic. Start with a concept-check question, then progressively harder application questions. Ask follow-up questions to probe deeper. Keep it focused on one topic. After 5-7 exchanges, summarize performance.

MOCK_SYSTEM_DESIGN_PROMPT: Full system design interviewer. Give a design problem, guide through requirements → high-level design → component deep-dive → scalability → trade-offs. Be realistic.

MOCK_ALGORITHMS_PROMPT: Coding interviewer. Present an algorithm problem, ask for approach, discuss time/space complexity, ask for edge cases.

MOCK_AI_AGENT_PROMPT: AI/Agent engineering interviewer. Ask about LLM internals, RAG pipelines, agent architecture, evaluation, tool use.

Keep existing BEHAVIORAL_PROMPT as mock_behavioral.

**Step 3: Run tests, commit**

---

### Task 2: Scorer — Extract Topic Scores from Sessions

**Files:**
- Create: `agentcoach/analytics/scorer.py`
- Create: `tests/test_scorer.py`

**Step 1: Write tests**

```python
# tests/test_scorer.py
from unittest.mock import MagicMock
from agentcoach.analytics.scorer import Scorer
from agentcoach.llm.base import Message

def test_scorer_parses_llm_response():
    mock_llm = MagicMock()
    mock_llm.generate.return_value = '''[
        {"topic_id": "system_design.caching", "score_delta": 15, "evidence": "Good understanding of cache invalidation"},
        {"topic_id": "system_design.cap_theorem", "score_delta": -5, "evidence": "Confused availability with consistency"}
    ]'''

    scorer = Scorer(mock_llm)
    history = [
        Message(role="system", content="You are an interviewer"),
        Message(role="user", content="ready"),
        Message(role="assistant", content="What is caching?"),
        Message(role="user", content="Caching stores frequently accessed data in memory"),
        Message(role="assistant", content="Good. What about CAP theorem?"),
        Message(role="user", content="It means you can have all three properties"),
    ]
    results = scorer.score_session(history, mode="learn", topic_id="system_design.caching")
    assert len(results) == 2
    assert results[0]["topic_id"] == "system_design.caching"
    assert results[0]["score_delta"] == 15

def test_scorer_handles_invalid_json():
    mock_llm = MagicMock()
    mock_llm.generate.return_value = "Sorry, I cannot parse this."

    scorer = Scorer(mock_llm)
    history = [Message(role="system", content="test")]
    results = scorer.score_session(history, mode="quiz", topic_id="test")
    assert results == []
```

**Step 2: Write implementation**

```python
# agentcoach/analytics/scorer.py
"""Scorer — uses LLM to extract per-topic scores from a session."""
import json
import re
from agentcoach.llm.base import LLMAdapter, Message


SCORE_PROMPT = """Analyze this interview/quiz session and score the candidate's performance on each topic discussed.

Session mode: {mode}
Primary topic: {topic_id}

Return a JSON array with scores. Each entry:
- topic_id: the specific topic (e.g., "system_design.caching")
- score_delta: integer from -20 to +25 representing performance change
  - Quiz: -10 to +15 (lower stakes)
  - Reinforce: -15 to +20 (medium stakes)
  - Mock: -20 to +25 (high stakes)
- evidence: one sentence explaining the score

Rules:
- Only score topics that were actually discussed
- Be fair but rigorous
- If candidate showed strong understanding: positive score
- If candidate was wrong or confused: negative score
- If partially correct: small positive score

Return ONLY the JSON array, no other text. Example:
[{{"topic_id": "system_design.caching", "score_delta": 15, "evidence": "Correctly explained cache invalidation strategies"}}]"""


class Scorer:
    def __init__(self, llm: LLMAdapter):
        self.llm = llm

    def score_session(self, history: list, mode: str, topic_id: str = "") -> list:
        if len(history) < 3:
            return []

        prompt = SCORE_PROMPT.format(mode=mode, topic_id=topic_id or "general")
        messages = list(history) + [Message(role="user", content=prompt)]

        try:
            response = self.llm.generate(messages)
            return self._parse_scores(response)
        except Exception:
            return []

    def _parse_scores(self, text: str) -> list:
        # Try to extract JSON array from response
        try:
            # Find JSON array in text
            match = re.search(r'\[.*\]', text, re.DOTALL)
            if match:
                data = json.loads(match.group())
                results = []
                for item in data:
                    if "topic_id" in item and "score_delta" in item:
                        results.append({
                            "topic_id": item["topic_id"],
                            "score_delta": int(item["score_delta"]),
                            "evidence": item.get("evidence", ""),
                        })
                return results
        except (json.JSONDecodeError, ValueError):
            pass
        return []
```

**Step 3: Run tests, commit**

---

### Task 3: Wire Scorer into Session End

**Files:**
- Modify: `agentcoach/cli.py`

**Step 1: Update _run_session to accept scorer and call it on session end**

After the existing `_end_session` feedback logic, add scoring:

```python
def _run_session(coach, mem, tts, analytics, user_id, topic, mode, llm):
    # ... existing session loop ...
    # On quit/done:
    _end_session(coach, mem)
    # Score the session
    if len(coach.history) > 4:
        from agentcoach.analytics.scorer import Scorer
        scorer = Scorer(llm)
        topic_id = topic["id"] if topic else ""
        scores = scorer.score_session(coach.history, mode=mode, topic_id=topic_id)
        if scores:
            print("\n--- Session Scores ---")
            for s in scores:
                analytics.record_score(user_id, s["topic_id"], s["score_delta"], mode, s["evidence"])
                icon = "📈" if s["score_delta"] > 0 else "📉"
                print(f"  {icon} {s['topic_id']}: {'+' if s['score_delta'] > 0 else ''}{s['score_delta']} — {s['evidence']}")
            print()
```

**Step 2: Pass llm to _run_session from main()**

**Step 3: Run all tests, commit**

---

### Task 4: Run All Tests + Tag

**Step 1:** `python3 -m pytest tests/ -v`
**Step 2:** `git tag v0.5.0-phase-b`
