"""Adaptive coach loop for post-session training adjustments."""
from __future__ import annotations

from typing import Any

from agentcoach.analytics.recommender import Recommender
from agentcoach.planner.system_design_route import (
    SYSTEM_DESIGN_PROBLEM_PATH,
    build_topic_card,
)

DIMENSION_DRILLS = {
    "requirements": ("system_design.api_design", "learn"),
    "communication": ("system_design.api_design", "reinforce"),
    "specificity": ("system_design.numbers_to_know", "learn"),
    "high_level_design": ("system_design.data_modeling", "reinforce"),
    "deep_dive": ("system_design.caching", "reinforce"),
    "scalability": ("system_design.scaling_reads", "reinforce"),
    "tradeoffs": ("system_design.cap_theorem", "learn"),
}

AREA_TOPIC_HINTS = [
    (("read", "replica", "fanout"), "system_design.scaling_reads"),
    (("write", "partition", "hot key"), "system_design.scaling_writes"),
    (("cache", "redis", "ttl"), "system_design.caching"),
    (("queue", "kafka", "async"), "system_design.message_queues"),
    (("rate", "limit", "429"), "system_design.rate_limiting"),
    (("websocket", "realtime", "sse"), "system_design.realtime_updates"),
    (("workflow", "background", "worker", "saga"), "system_design.long_running_tasks"),
    (("lock", "race", "contention", "booking"), "system_design.dealing_with_contention"),
    (("blob", "file", "upload", "s3"), "system_design.large_blobs"),
    (("estimate", "qps", "storage", "capacity"), "system_design.numbers_to_know"),
]


def _weakest_dimension(dimensions: list[dict[str, Any]]) -> dict[str, Any]:
    scored = []
    for dim in dimensions or []:
        try:
            score = float(dim.get("score"))
        except (TypeError, ValueError):
            continue
        scored.append((score, dim))
    if not scored:
        return {}
    scored.sort(key=lambda item: item[0])
    return scored[0][1]


def _topic_from_free_text(text: str) -> str:
    lower = text.lower()
    for markers, topic_id in AREA_TOPIC_HINTS:
        if any(marker in lower for marker in markers):
            return topic_id
    return ""


def _next_problem_topic(current_topic_id: str, topics: list[dict[str, Any]], analytics, user_id: str, syllabus) -> str:
    problem_topics = [topic for topic in topics if topic.get("id") in SYSTEM_DESIGN_PROBLEM_PATH]
    if problem_topics:
        recommendation = Recommender(analytics).recommend(user_id, problem_topics, syllabus)
        rec_topic = recommendation.get("topic_id")
        if rec_topic and rec_topic != current_topic_id:
            return rec_topic
    for topic_id in SYSTEM_DESIGN_PROBLEM_PATH:
        if topic_id != current_topic_id and syllabus.get_topic(topic_id):
            return topic_id
    return current_topic_id


def build_next_action(
    assessment: dict,
    *,
    syllabus,
    analytics,
    topics: list[dict[str, Any]],
    user_id: str,
) -> dict:
    """Turn a completed session report into the next coach action."""
    current_topic_id = assessment.get("topic_id") or "system_design.networking"
    dimensions = assessment.get("dimensions") or []
    weakest = _weakest_dimension(dimensions)
    weakest_name = weakest.get("name") or "requirements"
    weakest_score = float(weakest.get("score") or 0)
    overall = float(assessment.get("overall_score") or 0)
    areas_text = " ".join(str(item) for item in assessment.get("areas_to_improve") or [])
    hinted_topic = _topic_from_free_text(areas_text)

    if overall >= 4.0 and weakest_score >= 3.5:
        topic_id = _next_problem_topic(current_topic_id, topics, analytics, user_id, syllabus)
        mode = "mock_system_design"
        label = "Stretch"
        reason = "You cleared this session well enough to move into another full system and increase ambiguity."
    elif weakest_score <= 2.5:
        topic_id, mode = DIMENSION_DRILLS.get(weakest_name, (current_topic_id, "reinforce"))
        topic_id = hinted_topic or topic_id
        if not syllabus.get_topic(topic_id):
            topic_id = current_topic_id
        label = "Patch"
        reason = f"The coach should patch {weakest_name.replace('_', ' ')} before another broad mock."
    else:
        topic_id = hinted_topic or current_topic_id
        if not syllabus.get_topic(topic_id):
            topic_id = current_topic_id
        mode = "reinforce"
        label = "Drill"
        reason = f"Stay close to this topic and run a focused drill on {weakest_name.replace('_', ' ')}."

    action = build_topic_card(
        syllabus=syllabus,
        analytics=analytics,
        topics=topics,
        user_id=user_id,
        topic_id=topic_id,
        mode=mode,
        reason=reason,
    )
    action.update({
        "label": label,
        "focus_dimension": weakest_name,
        "focus_score": weakest_score,
        "coach_brief": (
            f"Start by diagnosing {weakest_name.replace('_', ' ')}. "
            "Give one short explanation, ask one targeted prompt, then retest."
        ),
        "loop": [
            {"key": "diagnose", "status": "done"},
            {"key": "plan", "status": "done"},
            {"key": "teach", "status": "next" if mode == "learn" else "queued"},
            {"key": "test", "status": "next" if mode != "learn" else "queued"},
            {"key": "adjust", "status": "active"},
        ],
    })
    return action


__all__ = ["build_next_action"]
