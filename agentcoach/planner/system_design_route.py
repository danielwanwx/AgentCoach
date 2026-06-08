"""System design coach route planner.

This module owns the product logic for turning a lightweight intake form into
the first adaptive training route. The web server should only wire HTTP state
into this planner; it should not decide pedagogy.
"""
from __future__ import annotations

from typing import Any

from agentcoach.analytics.recommender import Recommender

SUPPORTED_MODES = ["learn", "reinforce", "mock_system_design"]

SYSTEM_DESIGN_INTERVIEW_OS_PATH = [
    "system_design.networking",
    "system_design.api_design",
    "system_design.data_modeling",
    "system_design.numbers_to_know",
]

SYSTEM_DESIGN_BUILDING_BLOCK_PATH = [
    "system_design.load_balancing",
    "system_design.db_indexing",
    "system_design.caching",
    "system_design.sharding",
    "system_design.consistent_hashing",
    "system_design.cap_theorem",
    "system_design.message_queues",
]

SYSTEM_DESIGN_PATTERN_PATH = [
    "system_design.scaling_reads",
    "system_design.scaling_writes",
    "system_design.rate_limiting",
    "system_design.realtime_updates",
    "system_design.long_running_tasks",
    "system_design.dealing_with_contention",
    "system_design.large_blobs",
    "system_design.multi_step_processes",
    "system_design.event_sourcing",
    "system_design.circuit_breaker",
    "system_design.leader_election",
]

SYSTEM_DESIGN_PROBLEM_PATH = [
    "system_design.url_shortener",
    "system_design.distributed_rate_limiter",
    "system_design.distributed_cache",
    "system_design.metrics_monitoring",
    "system_design.whatsapp",
    "system_design.youtube",
    "system_design.dropbox",
    "system_design.ticketmaster",
    "system_design.payment_system",
    "system_design.google_docs",
    "system_design.uber",
]

TOPIC_ALIAS_TERMS = {
    "system_design.url_shortener": ["bitly", "tinyurl", "shortener", "short url", "url"],
    "system_design.distributed_rate_limiter": ["rate limiter", "rate limiting", "429", "token bucket"],
    "system_design.ticketmaster": ["ticketmaster", "ticket", "booking"],
    "system_design.whatsapp": ["whatsapp", "messaging", "chat"],
    "system_design.youtube": ["youtube", "video"],
    "system_design.load_balancing": ["load balancing", "load balancer", "balancer"],
    "system_design.caching": ["cache", "caching", "redis"],
    "system_design.sharding": ["shard", "sharding", "partition"],
    "system_design.message_queues": ["queue", "kafka", "stream"],
    "system_design.consistent_hashing": ["consistent hash", "hash ring"],
    "system_design.cap_theorem": ["cap", "consistency", "availability"],
    "system_design.db_indexing": ["index", "database index"],
    "system_design.numbers_to_know": ["capacity", "estimation", "numbers", "qps", "storage"],
    "system_design.scaling_reads": ["read scaling", "reads", "read replica", "replication lag"],
    "system_design.scaling_writes": ["write scaling", "writes", "write burst", "partition key"],
    "system_design.realtime_updates": ["realtime", "websocket", "sse", "polling"],
    "system_design.long_running_tasks": ["long running", "background job", "worker", "workflow"],
    "system_design.dealing_with_contention": ["contention", "double booking", "race condition", "lock"],
    "system_design.large_blobs": ["large blob", "object storage", "s3", "file upload"],
    "system_design.multi_step_processes": ["multi step", "saga", "temporal", "durable execution"],
}


def normalize_mode(mode: str) -> str:
    if mode == "mock":
        return "mock_system_design"
    if mode in SUPPORTED_MODES:
        return mode
    return "learn"


def resolve_topic(topic_id: str, topics: list[dict[str, Any]]) -> tuple[str, str, str]:
    for topic in topics:
        if topic["id"] == topic_id:
            return topic["id"], topic["name"], topic["domain"]
    if "." in topic_id:
        domain, tail = topic_id.split(".", 1)
        return topic_id, tail.replace("_", " ").title(), domain
    return topic_id, topic_id.title(), "system_design"


def build_topic_card(
    *,
    syllabus,
    analytics,
    topics: list[dict[str, Any]],
    user_id: str,
    topic_id: str,
    mode: str = "",
    reason: str = "",
) -> dict:
    topic = syllabus.get_topic(topic_id) or {}
    resolved_id, topic_name, domain = resolve_topic(topic_id, topics)
    mastery = analytics.get_mastery(user_id, resolved_id)
    if not mode:
        if mastery < Recommender.LEARN_THRESHOLD:
            mode = "learn"
        elif mastery < Recommender.REINFORCE_THRESHOLD:
            mode = "reinforce"
        else:
            mode = "mock_system_design"
    resources = []
    for resource in (topic.get("resources") or [])[:2]:
        resources.append({
            "type": resource.get("type", "resource"),
            "title": resource.get("title", ""),
            "url": resource.get("url"),
        })
    return {
        "topic_id": resolved_id,
        "topic_name": topic.get("name") or topic_name,
        "domain": topic.get("domain") or domain,
        "mode": normalize_mode(mode),
        "mastery": mastery,
        "reason": reason,
        "resources": resources,
    }


def _detect_focus_topic(text: str) -> str:
    lower = text.lower()
    for topic_id, aliases in TOPIC_ALIAS_TERMS.items():
        if any(alias in lower for alias in aliases):
            return topic_id
    return ""


def _style_from_intake(body: dict, text: str) -> str:
    style = (body.get("start_style") or "guided").strip().lower()
    if style in {"zero", "sprint", "diagnose", "blocks", "patterns"}:
        return style
    if any(marker in text for marker in ["problem breakdown", "problem ladder"]):
        return "sprint"
    if "building blocks" in text:
        return "blocks"
    if any(marker in text for marker in ["patterns", "scaling reads", "scaling writes", "realtime updates", "contention"]):
        return "patterns"
    if any(marker in text for marker in ["interview", "onsite", "phone screen", "meta", "google", "faang", "soon"]):
        return "sprint"
    if any(marker in text for marker in ["beginner", "new", "from zero", "no idea", "don't know", "not sure", "小白", "基础", "不知道"]):
        return "zero"
    return "guided"


def build_system_design_plan(
    body: dict,
    *,
    syllabus,
    analytics,
    topics: list[dict[str, Any]],
) -> dict:
    user_id = (body.get("user_id") or "web-guest").strip() or "web-guest"
    target = (body.get("target") or "").strip()
    baseline = (body.get("baseline") or "").strip()
    friction = (body.get("friction") or "").strip()
    availability = (body.get("availability") or "").strip()
    text = " ".join([target, baseline, friction, availability]).lower()
    style = _style_from_intake(body, text)
    mentioned_topic = _detect_focus_topic(text)

    system_topics = [topic for topic in topics if topic.get("domain") == "system_design"]
    recommendation = Recommender(analytics).recommend(user_id, system_topics, syllabus)
    rec_topic = mentioned_topic or recommendation["topic_id"]

    if style == "zero":
        first_topic = "system_design.networking"
        level = "Foundation"
        headline = "Start with the ground layer, then earn the first design problem."
        summary = "Your path should remove choice overload: interview moves, core building blocks, then one simple system."
        interview_os = SYSTEM_DESIGN_INTERVIEW_OS_PATH
        building_blocks = SYSTEM_DESIGN_BUILDING_BLOCK_PATH[:6]
        patterns = SYSTEM_DESIGN_PATTERN_PATH[:5]
        problems = SYSTEM_DESIGN_PROBLEM_PATH[:5]
        first_reason = "This is the first brick for APIs, load balancers, caches, and almost every follow-up question."
    elif style == "sprint":
        first_topic = rec_topic if rec_topic in SYSTEM_DESIGN_PROBLEM_PATH else "system_design.url_shortener"
        level = "Interview Sprint"
        headline = "Use one concrete problem as the spine, patch fundamentals as they appear."
        summary = "Because the interview clock matters, the coach starts with a problem and folds missing basics into drills."
        interview_os = ["system_design.numbers_to_know", "system_design.api_design", "system_design.data_modeling"]
        building_blocks = ["system_design.caching", "system_design.db_indexing", "system_design.sharding", "system_design.message_queues"]
        patterns = ["system_design.scaling_reads", "system_design.scaling_writes", "system_design.long_running_tasks", "system_design.dealing_with_contention"]
        problems = [first_topic] + [topic for topic in SYSTEM_DESIGN_PROBLEM_PATH if topic != first_topic][:3]
        first_reason = "A worked problem quickly reveals whether the gaps are requirements, data flow, scale, or trade-offs."
    elif style == "blocks":
        first_topic = rec_topic if rec_topic in SYSTEM_DESIGN_BUILDING_BLOCK_PATH else "system_design.load_balancing"
        level = "Building Blocks"
        headline = "Start with the primitive that unlocks the most future answers."
        summary = "The coach maps HelloInterview-style core concepts into practical choices: balancers, indexes, caches, shards, consistency, and queues."
        interview_os = ["system_design.api_design", "system_design.data_modeling", "system_design.numbers_to_know"]
        building_blocks = SYSTEM_DESIGN_BUILDING_BLOCK_PATH
        patterns = ["system_design.scaling_reads", "system_design.scaling_writes", "system_design.realtime_updates", "system_design.long_running_tasks", "system_design.large_blobs"]
        problems = ["system_design.distributed_cache", "system_design.distributed_rate_limiter", "system_design.metrics_monitoring", "system_design.whatsapp"]
        first_reason = "This track turns vague primitives into concrete decisions you can reuse in every design."
    elif style == "patterns":
        first_topic = rec_topic if rec_topic in SYSTEM_DESIGN_PATTERN_PATH else "system_design.scaling_reads"
        level = "Pattern Muscles"
        headline = "Turn prompts into recognizable system moves."
        summary = "The coach starts from HelloInterview-style patterns: scaling reads, scaling writes, realtime updates, long-running tasks, contention, and large objects."
        interview_os = ["system_design.api_design", "system_design.data_modeling", "system_design.numbers_to_know"]
        building_blocks = ["system_design.db_indexing", "system_design.caching", "system_design.sharding", "system_design.message_queues"]
        patterns = SYSTEM_DESIGN_PATTERN_PATH[:8]
        problems = ["system_design.url_shortener", "system_design.distributed_rate_limiter", "system_design.ticketmaster", "system_design.whatsapp"]
        first_reason = "Pattern recognition is the bridge between knowing components and choosing a design under interview pressure."
    else:
        first_topic = mentioned_topic or recommendation["topic_id"]
        level = "Guided Ramp"
        headline = "Let the coach pick the next smallest useful step."
        summary = "The plan balances fundamentals, pattern drills, and problem walkthroughs so you are not browsing a catalog."
        interview_os = SYSTEM_DESIGN_INTERVIEW_OS_PATH
        building_blocks = SYSTEM_DESIGN_BUILDING_BLOCK_PATH[:6]
        patterns = SYSTEM_DESIGN_PATTERN_PATH[:7]
        problems = SYSTEM_DESIGN_PROBLEM_PATH[:4]
        first_reason = recommendation.get("reason", "Best next topic based on current mastery and prerequisites.")

    if not syllabus.get_topic(first_topic):
        first_topic = "system_design.networking"

    card_args = {
        "syllabus": syllabus,
        "analytics": analytics,
        "topics": topics,
        "user_id": user_id,
    }
    first_mode = "mock_system_design" if style == "sprint" and first_topic in SYSTEM_DESIGN_PROBLEM_PATH else "learn"
    next_session = build_topic_card(**card_args, topic_id=first_topic, mode=first_mode, reason=first_reason)

    phases = [
        {
            "title": "Interview OS",
            "cadence": "First 2-4 sessions",
            "goal": "Learn the repeatable interview loop: clarify, estimate, shape APIs/data, then draw the first design.",
            "items": [
                build_topic_card(**card_args, topic_id=topic_id, mode="learn", reason="Build the operating system for every later answer.")
                for topic_id in interview_os
                if syllabus.get_topic(topic_id)
            ],
        },
        {
            "title": "Building Blocks",
            "cadence": "Next 5-8 sessions",
            "goal": "Master the primitives Grokking-style courses keep returning to: balancers, indexes, caches, shards, consistency, and queues.",
            "items": [
                build_topic_card(**card_args, topic_id=topic_id, mode="learn", reason="Learn the primitive and the trade-off it buys.")
                for topic_id in building_blocks
                if syllabus.get_topic(topic_id)
            ],
        },
        {
            "title": "Pattern Muscles",
            "cadence": "Then 6-10 drills",
            "goal": "Compress real interview problems into reusable moves: scale reads, scale writes, async jobs, realtime, contention, and large objects.",
            "items": [
                build_topic_card(**card_args, topic_id=topic_id, mode="reinforce", reason="Recognize the pattern and explain when not to use it.")
                for topic_id in patterns
                if syllabus.get_topic(topic_id)
            ],
        },
        {
            "title": "Problem Ladder",
            "cadence": "After the base is stable",
            "goal": "Walk through canonical systems in increasing ambiguity, using HelloInterview-style breakdowns and Alex Xu-style case templates.",
            "items": [
                build_topic_card(
                    **card_args,
                    topic_id=topic_id,
                    mode="learn" if index == 0 and style != "sprint" else "mock_system_design",
                    reason="Apply the concepts in a full system and capture weak signals.",
                )
                for index, topic_id in enumerate(problems)
                if syllabus.get_topic(topic_id)
            ],
        },
        {
            "title": "Mock Loop",
            "cadence": "Ongoing",
            "goal": "Use reports to choose the next drill: requirements, high-level design, deep dive, scale, reliability, or trade-offs.",
            "items": [
                build_topic_card(**card_args, topic_id=topic_id, mode="mock_system_design", reason="Full interview simulation with scoring.")
                for topic_id in problems[:3]
                if syllabus.get_topic(topic_id)
            ],
        },
    ]

    foundation_score = 18 if style == "zero" else 42 if style == "guided" else 55
    interview_score = 22 if style == "zero" else 38 if style == "guided" else 62
    adaptive_score = max(20, min(88, next_session["mastery"] + 30))
    return {
        "user_id": user_id,
        "style": style,
        "assessment": {
            "level": level,
            "headline": headline,
            "summary": summary,
            "signals": [
                {"label": "foundation", "score": foundation_score},
                {"label": "interview readiness", "score": interview_score},
                {"label": "known mastery", "score": adaptive_score},
            ],
        },
        "next_session": next_session,
        "phases": phases,
        "notes": [
            "The knowledge map stays available, but it is now secondary.",
            "After each session, the report updates mastery and the coach can adjust the next drill.",
            "The first session uses local HelloInterview notes when matching KB files exist.",
        ],
    }


__all__ = [
    "SUPPORTED_MODES",
    "build_topic_card",
    "build_system_design_plan",
    "normalize_mode",
    "resolve_topic",
]
