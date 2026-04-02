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
- IMPORTANT: Use ONLY the primary topic_id "{topic_id}" for scoring. Do NOT invent sub-topic IDs. Combine all scores into a single entry for the primary topic.

Return ONLY the JSON array, no other text. Example:
[{{"topic_id": "{topic_id}", "score_delta": 15, "evidence": "Correctly explained cache invalidation strategies"}}]
{kb_reference_section}"""

KB_REFERENCE_SECTION = """
## Reference Material (ground truth)
Use this to verify the candidate's answers for factual accuracy.
Score DOWN if the candidate contradicts this material. Score UP if consistent.

{kb_excerpts}"""


class Scorer:
    def __init__(self, llm: LLMAdapter, kb_store=None, syllabus=None):
        self.llm = llm
        self.kb_store = kb_store
        self.syllabus = syllabus

    def score_session(self, history: list, mode: str, topic_id: str = "") -> list:
        if len(history) < 3:
            return []

        # Optionally include KB ground truth for answer validation
        kb_ref = ""
        if self.kb_store and topic_id:
            try:
                results = self.kb_store.search(topic_id, limit=3)
                if results:
                    excerpts = "\n".join(
                        f"- {r['content'][:400]}" for r in results
                    )
                    kb_ref = KB_REFERENCE_SECTION.format(kb_excerpts=excerpts)
            except Exception:
                pass

        prompt = SCORE_PROMPT.format(
            mode=mode, topic_id=topic_id or "general",
            kb_reference_section=kb_ref,
        )
        messages = list(history) + [Message(role="user", content=prompt)]

        try:
            response = self.llm.generate(messages)
            return self._parse_scores(response, fallback_topic_id=topic_id)
        except Exception:
            return []

    def _parse_scores(self, text: str, fallback_topic_id: str = "") -> list:
        try:
            match = re.search(r'\[.*\]', text, re.DOTALL)
            if match:
                data = json.loads(match.group())
                results = []
                for item in data:
                    if "topic_id" in item and "score_delta" in item:
                        results.append({
                            "topic_id": self._normalize_topic_id(item["topic_id"], fallback_topic_id),
                            "score_delta": int(item["score_delta"]),
                            "evidence": item.get("evidence", ""),
                        })
                return results
        except (json.JSONDecodeError, ValueError):
            pass
        return []

    def _normalize_topic_id(self, topic_id: str, fallback_topic_id: str = "") -> str:
        """Normalize topic_id to match syllabus leaf topics.

        Strategy: exact match → strip last segment → strip to domain → fallback to primary topic.
        """
        if not self.syllabus:
            return topic_id
        if self.syllabus.get_topic(topic_id):
            return topic_id
        # Try parent: strip last segment (a.b.c → a.b)
        parts = topic_id.rsplit(".", 1)
        if len(parts) > 1 and self.syllabus.get_topic(parts[0]):
            return parts[0]
        # Try grandparent (a.b.c.d → a.b)
        parts2 = topic_id.split(".")
        if len(parts2) > 2:
            grandparent = ".".join(parts2[:2])
            if self.syllabus.get_topic(grandparent):
                return grandparent
        # Fall back to the primary topic from the session
        if fallback_topic_id and self.syllabus.get_topic(fallback_topic_id):
            return fallback_topic_id
        return topic_id
