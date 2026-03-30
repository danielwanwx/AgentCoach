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
  - Quiz/Learn: -10 to +15 (lower stakes)
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
        try:
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
