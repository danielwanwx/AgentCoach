"""Scorer — uses LLM to extract per-topic scores from a session."""
import json
import re
from agentcoach.llm.base import LLMAdapter, Message


SCORE_PROMPT = """Evaluate this {mode} session on topic "{topic_id}".

{rubric_section}

Return a single JSON object. Do NOT wrap it in markdown code fences. Do NOT add any text before or after the JSON.

Example output:
{{"topic_id": "system_design.caching", "overall_score": 3.8, "dimensions": [{{"name": "requirements", "score": 4, "evidence": "Asked good clarifying questions about scale"}}, {{"name": "high_level_design", "score": 3, "evidence": "Proposed reasonable architecture but missed CDN layer"}}], "strengths": ["Strong grasp of cache invalidation patterns"], "areas_to_improve": ["Need to discuss trade-offs between consistency models"]}}

Now score this session:
{{
  "topic_id": "{topic_id}",
  "overall_score": <float 1.0-5.0>,
  "dimensions": [
    {{"name": "<dimension>", "score": <int 1-5>, "evidence": "<one sentence>"}}
  ],
  "strengths": ["<strength1>"],
  "areas_to_improve": ["<area1>"]
}}

Rules:
- Score each dimension 1-5 using the rubric above
- overall_score = weighted average of dimensions
- Be fair but rigorous. Cite specific moments from the conversation.
- Return ONLY the JSON object, no markdown, no explanation.
{kb_reference_section}"""

# Mastery gain multipliers per mode (adjusted for better user progression)
MASTERY_GAIN = {
    "learn": 0.15,           # 15% of score → mastery
    "reinforce": 0.20,       # 20%
    "mock": 0.25,            # 25% (hardest mode, should reward most)
    "mock_system_design": 0.25,
    "mock_algorithms": 0.25,
    "mock_ai_agent": 0.25,
    "mock_behavioral": 0.25,
    "behavioral": 0.25,
}
MAX_MASTERY_GAIN_PER_SESSION = 25  # cap at 25% per session

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

        # Accept either List[Message] (from Coach.history) or List[dict]
        # {role, content} (from e2e/harness transcripts). Normalize to Message
        # with OpenAI-compatible roles so any adapter can consume it: the
        # party being evaluated (candidate) → "user", everyone else → "assistant".
        normalized: list = []
        for item in history:
            if isinstance(item, Message):
                normalized.append(item)
                continue
            if not isinstance(item, dict):
                continue
            raw_role = (item.get("role") or "").lower()
            content = item.get("content") or ""
            if raw_role in {"system", "user", "assistant"}:
                role = raw_role
            elif raw_role in {"coach", "interviewer", "teacher"}:
                role = "assistant"
            else:
                # Treat any other role (junior/intermediate/senior/candidate/...)
                # as the learner being scored.
                role = "user"
            normalized.append(Message(role=role, content=content))
        history = normalized

        # Get rubric for this domain
        domain = topic_id.split(".")[0] if topic_id else "system_design"
        try:
            from agentcoach.scoring.rubrics import format_rubric_for_prompt
            rubric_text = format_rubric_for_prompt(domain)
        except Exception:
            rubric_text = ""

        # Optionally include KB ground truth for answer validation
        kb_ref = ""
        if self.kb_store and topic_id:
            try:
                results = self.kb_store.search(topic_id, limit=3, category=domain)
                if results:
                    excerpts = "\n".join(f"- {r['content'][:400]}" for r in results)
                    kb_ref = KB_REFERENCE_SECTION.format(kb_excerpts=excerpts)
            except Exception:
                pass

        prompt = SCORE_PROMPT.format(
            mode=mode, topic_id=topic_id or "general",
            rubric_section=rubric_text,
            kb_reference_section=kb_ref,
        )
        messages = list(history) + [Message(role="user", content=prompt)]

        try:
            response = self.llm.generate(messages)
            result = self._parse_structured_score(response, mode, topic_id)
            if not result:
                import sys
                print(f"  [Scorer] WARNING: empty parse result. Raw LLM response (first 300 chars):\n  {response[:300]}", file=sys.stderr)
            return result
        except Exception as e:
            # Fallback to legacy parsing
            try:
                return self._parse_scores(response, fallback_topic_id=topic_id)
            except Exception:
                import sys
                print(f"  [Scorer] ERROR: all parsing failed: {e}", file=sys.stderr)
                return []

    @staticmethod
    def _clean_llm_json(text: str) -> str:
        """Strip markdown fences, think tags, and surrounding text from LLM JSON output."""
        # Strip <think>...</think> blocks
        text = re.sub(r"<think>[\s\S]*?</think>\s*", "", text)
        # Strip markdown code fences: ```json ... ``` or ``` ... ```
        fence_match = re.search(r'```(?:json)?\s*(\{[\s\S]*?\})\s*```', text)
        if fence_match:
            return fence_match.group(1)
        return text

    def _parse_structured_score(self, text: str, mode: str, topic_id: str) -> list:
        """Parse structured JSON score and compute mastery delta."""
        try:
            text = self._clean_llm_json(text)

            # Check if response is legacy array format [{"score_delta": ...}]
            array_match = re.search(r'\[[\s\S]*\]', text)
            if array_match and '"score_delta"' in text and '"overall_score"' not in text:
                return self._parse_scores(text, fallback_topic_id=topic_id)

            match = re.search(r'\{[\s\S]*\}', text)
            if not match:
                return self._parse_scores(text, fallback_topic_id=topic_id)

            data = json.loads(match.group())

            # Extract overall score (1-5 scale)
            overall = float(data.get("overall_score", 3.0))

            # Compute mastery delta from overall score and mode
            # Fall back to "mock" rate for any mock_* variant not explicitly listed
            gain_rate = MASTERY_GAIN.get(mode) or MASTERY_GAIN.get(
                "mock" if mode.startswith("mock") else mode, 0.15
            )
            # Score 3.0 = neutral, 5.0 = max gain, 1.0 = negative
            raw_delta = (overall - 2.0) * gain_rate * 20  # maps 1-5 → -20 to +60 before cap
            score_delta = int(max(-20, min(MAX_MASTERY_GAIN_PER_SESSION / gain_rate, raw_delta)))

            # Build evidence from dimensions
            dims = data.get("dimensions", [])
            strengths = data.get("strengths", [])
            areas = data.get("areas_to_improve", [])
            evidence_parts = []
            if dims:
                evidence_parts.append("; ".join(f"{d['name']}={d.get('score','?')}" for d in dims[:4]))
            if strengths:
                evidence_parts.append(f"Strengths: {', '.join(strengths[:2])}")
            if areas:
                evidence_parts.append(f"Improve: {', '.join(areas[:2])}")
            evidence = ". ".join(evidence_parts)[:200]

            normalized_id = self._normalize_topic_id(
                data.get("topic_id", topic_id), fallback_topic_id=topic_id
            )

            return [{
                "topic_id": normalized_id,
                "score_delta": score_delta,
                "overall_score": overall,
                "evidence": evidence,
                "dimensions": dims,
            }]
        except (json.JSONDecodeError, ValueError, KeyError):
            return self._parse_scores(text, fallback_topic_id=topic_id)

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
