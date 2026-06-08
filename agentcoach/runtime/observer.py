"""First-pass real-time observer for coaching interactions.

The observer is deliberately deterministic in this slice. A local model can sit
behind the same contract later, but heuristics already let the coach react to
vague answers, requests for explanation inside pressure modes, and strong
specific answers without waiting for the final report.
"""
from __future__ import annotations

import re
from typing import Any

from agentcoach.coaching.learning_harness import NETWORKING_AGENTIC_BLUEPRINT


VAGUE_TERMS = (
    "stuff", "things", "kind of", "sort of", "maybe", "probably",
    "something like", "i guess", "not sure", "don't know", "dont know",
    "no idea", "不确定", "不知道", "不太懂", "不会",
)

EXPLANATION_TERMS = (
    "explain", "teach me", "what is", "how does", "why", "walk me through",
    "i don't understand", "i dont understand", "can you explain",
    "解释", "讲讲", "为什么", "怎么", "是什么",
)

MECHANISM_TERMS = (
    "cache", "index", "partition", "shard", "queue", "worker", "replica",
    "load balancer", "consistent hashing", "token bucket", "websocket",
    "sse", "grpc", "rest", "graphql", "webrtc", "cdn", "database", "timeout", "retry",
    "backoff", "idempotency", "lock", "lease", "rate limit",
)

TRADEOFF_TERMS = (
    "trade", "latency", "throughput", "consistency", "availability",
    "durability", "cost", "complexity", "failure", "p99", "p95",
    "reliability", "hot key", "bottleneck",
)


def observe_interaction(
    *,
    session_id: str,
    topic_id: str,
    mode: str,
    event_type: str,
    raw_text: str = "",
    card_action: str = "",
) -> dict[str, Any]:
    text = (raw_text or "").strip()
    lowered = text.lower()
    words = re.findall(r"[a-zA-Z0-9_+-]+|[\u4e00-\u9fff]", lowered)
    vague = _has_any(lowered, VAGUE_TERMS)
    asks_explanation = _looks_like_explanation_request(lowered)
    mechanisms = _count_terms(lowered, MECHANISM_TERMS)
    tradeoffs = _count_terms(lowered, TRADEOFF_TERMS)
    numbers = len(re.findall(r"\b\d+(\.\d+)?\s*(ms|s|qps|rps|k|m|b|gb|tb|%)?\b", lowered))
    specificity = min(1.0, (mechanisms * 0.22) + (tradeoffs * 0.18) + (numbers * 0.2) + (min(len(words), 35) / 100))

    detected_gap = ""
    recommended_action = "continue"
    confidence_signal = "unknown"
    recommended_card_id = ""
    coach_brief = ""

    if not text and event_type == "utterance":
        detected_gap = "empty_answer"
        recommended_action = "insert_repair_card"
        confidence_signal = "blocked"
    elif asks_explanation and mode in {"reinforce", "mock_system_design"}:
        detected_gap = "needs_teaching_in_pressure_mode"
        recommended_action = "recommend_learn_card"
        confidence_signal = "blocked"
    elif vague and specificity < 0.45:
        detected_gap = "vague_language"
        recommended_action = "insert_repair_card"
        confidence_signal = "shallow"
    elif specificity < 0.32 and len(words) >= 7:
        detected_gap = "low_specificity"
        recommended_action = "insert_repair_card"
        confidence_signal = "shallow"
    elif specificity >= 0.65:
        detected_gap = "ready_for_more_pressure"
        recommended_action = "insert_test_card" if mode == "reinforce" else "continue"
        confidence_signal = "specific"

    networking_gap = _networking_dynamic_gap(lowered) if topic_id == "system_design.networking" else {}
    if networking_gap and not detected_gap:
        detected_gap = networking_gap["detected_gap"]
        recommended_action = networking_gap["recommended_action"]
        recommended_card_id = networking_gap["recommended_card_id"]
        coach_brief = networking_gap["coach_brief"]
        confidence_signal = "targeted_gap"

    if card_action == "skip":
        detected_gap = detected_gap or "skipped_card"
        recommended_action = "insert_test_card"

    return {
        "session_id": session_id,
        "topic_id": topic_id,
        "mode": mode,
        "event_type": event_type,
        "raw_text": text,
        "specificity_score": round(specificity, 2),
        "confidence_signal": confidence_signal,
        "detected_gap": detected_gap,
        "recommended_action": recommended_action,
        "recommended_card_id": recommended_card_id,
        "card_action": card_action,
        "coach_brief": coach_brief or _coach_brief(detected_gap, recommended_action),
    }


def _has_any(text: str, terms: tuple[str, ...]) -> bool:
    return any(term in text for term in terms)


def _count_terms(text: str, terms: tuple[str, ...]) -> int:
    return sum(1 for term in terms if term in text)


def _looks_like_explanation_request(text: str) -> bool:
    if not text:
        return False
    return _has_any(text, EXPLANATION_TERMS) or text.endswith("?")


def _networking_dynamic_gap(text: str) -> dict[str, str]:
    checks = [
        (
            "webrtc",
            ("signaling", "stun", "turn", "nat", "fallback"),
            "networking.webrtc_signaling_missing",
            "networking.webrtc",
            0,
        ),
        (
            "websocket",
            ("long-lived", "stateful", "load balanc", "fanout", "failover", "connection"),
            "networking.websocket_infra_missing",
            "networking.realtime_protocols",
            1,
        ),
        (
            "graphql",
            ("resolver", "fan", "authorization", "auth", "cache", "complex"),
            "networking.graphql_resolver_complexity_missing",
            "networking.protocol_choice",
            2,
        ),
        (
            "retry",
            ("backoff", "jitter", "idempot", "budget", "circuit"),
            "networking.retry_guardrails_missing",
            "networking.failures",
            0,
        ),
        (
            "dns",
            ("ttl", "stale", "cache", "health", "resolver"),
            "networking.dns_ttl_missing",
            "networking.lb_client_side",
            0,
        ),
        (
            "region",
            ("data", "consistency", "failover", "locality", "replication"),
            "networking.regionalization_tradeoff_missing",
            "networking.latency",
            1,
        ),
    ]
    for trigger, required_terms, gap, card_id, rule_index in checks:
        if trigger in text and not any(term in text for term in required_terms):
            rules = NETWORKING_AGENTIC_BLUEPRINT.get(card_id, {}).get("dynamic_insert_rules", [])
            return {
                "detected_gap": gap,
                "recommended_action": "insert_repair_card",
                "recommended_card_id": card_id,
                "coach_brief": rules[min(rule_index, len(rules) - 1)] if rules else "",
            }
    return {}


def _coach_brief(gap: str, action: str) -> str:
    if action == "recommend_learn_card":
        return "Pause pressure mode and route to a smaller teaching card before retesting."
    if gap == "vague_language":
        return "Ask for precise terms before validating the answer."
    if gap == "low_specificity":
        return "Ask for one mechanism, one number or boundary, and one failure mode."
    if action == "insert_test_card":
        return "The answer was specific enough; retest under slightly more pressure."
    return ""
