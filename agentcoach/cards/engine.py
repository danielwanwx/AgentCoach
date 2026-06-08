"""Mode-aware card frame helpers.

This module is intentionally lightweight for the first vertical slice. It does
not replace the existing Learn harness yet; it gives all modes a common frame
shape and creates just-in-time cards from observer signals.
"""
from __future__ import annotations

from copy import deepcopy
from typing import Any

from agentcoach.cards.schema import CoachCard, SessionFrame
from agentcoach.coaching.learning_harness import NETWORKING_AGENTIC_BLUEPRINT


LOCAL_CARD_ACTIONS = [
    {"id": "play", "label": "Listen", "kind": "local"},
]


TARGETED_NETWORKING_TITLES = {
    "networking.protocol_choice": "Let's choose the protocol from the use case",
    "networking.realtime_protocols": "Let's slow down before saying WebSocket",
    "networking.webrtc": "Let's name signaling and NAT traversal",
    "networking.failures": "Let's make the recovery plan safe",
    "networking.load_balancing": "Let's explain who picks the server",
    "networking.lb_client_side": "Let's check DNS TTLs and stale endpoints",
    "networking.lb_dedicated": "Let's choose the balancer by what it can see",
    "networking.latency": "Let's budget the latency path",
}


def frame_from_learning_frame(frame: dict[str, Any], *, session_id: str = "") -> dict[str, Any]:
    """Normalize a legacy Learn-harness frame into the shared frame shape."""
    normalized = deepcopy(frame)
    normalized["version"] = 2
    if session_id:
        normalized["session_id"] = session_id
    card = normalized.setdefault("card", {})
    topic_id = normalized.get("topic_id", "")
    topic_name = normalized.get("topic_name", "")
    unit = normalized.get("unit") or {}
    card.setdefault("card_id", unit.get("id") or f"{topic_id}.{normalized.get('kind', 'card')}")
    card.setdefault("topic_id", topic_id)
    card.setdefault("topic_name", topic_name)
    card.setdefault("mode", normalized.get("mode", "learn"))
    card.setdefault("stage", normalized.get("kind", "teach"))
    card.setdefault("objective", unit.get("objective", ""))
    if "visible_body" not in card:
        card["visible_body"] = card.get("body", "")
    card.setdefault("coach_brief", normalized.get("spoken_script", ""))
    card.setdefault("source_refs", (card.get("detail") or {}).get("sources", []))
    card.setdefault("rubric_signals", [])
    card.setdefault("personalization", {})
    card.setdefault("actions", normalized.get("actions", []))
    return normalized


def start_frame(
    *,
    session_id: str,
    mode: str,
    topic_id: str,
    topic_name: str,
    domain: str,
    mastery: int = 0,
    focus_dimension: str = "",
    coach_brief: str = "",
    resources: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    if mode == "reinforce":
        return _train_start_frame(
            session_id=session_id,
            topic_id=topic_id,
            topic_name=topic_name,
            domain=domain,
            mastery=mastery,
            focus_dimension=focus_dimension,
            coach_brief=coach_brief,
            resources=resources or [],
        )
    if mode == "mock_system_design":
        return _mock_start_frame(
            session_id=session_id,
            topic_id=topic_id,
            topic_name=topic_name,
            domain=domain,
            mastery=mastery,
            focus_dimension=focus_dimension,
            coach_brief=coach_brief,
            resources=resources or [],
        )
    return _learn_route_frame(
        session_id=session_id,
        topic_id=topic_id,
        topic_name=topic_name,
        domain=domain,
        mastery=mastery,
        focus_dimension=focus_dimension,
        coach_brief=coach_brief,
        resources=resources or [],
    )


def followup_frame_from_signal(
    signal: dict[str, Any],
    *,
    session_id: str,
    mode: str,
    topic_id: str,
    topic_name: str,
    domain: str,
    resources: list[dict[str, Any]] | None = None,
) -> dict[str, Any] | None:
    action = signal.get("recommended_action") or "continue"
    if action == "continue":
        return None
    detail_key_points = _signal_key_points(signal)
    targeted = _targeted_networking_followup(signal)
    if action == "insert_repair_card":
        title = targeted.get("title") or "Let's clean this up before moving on"
        body = targeted.get("body") or (
            "Your answer is still too broad. Stabilize it with one precise mechanism, "
            "one concrete number or boundary, and one failure mode."
        )
        detail_key_points = targeted.get("key_points") or detail_key_points
        stage = "repair"
        kind = "repair"
    elif action == "recommend_learn_card":
        title = "This is a Learn-mode gap"
        body = (
            "You asked for explanation during a pressure mode. That is useful signal: "
            "pause the broad rep, review the smaller prerequisite, then retest."
        )
        stage = "teach"
        kind = "coach_recommendation"
    elif action == "insert_test_card":
        title = "Retest the weak signal"
        body = (
            "Answer this in one tight pass: responsibility, request-path position, "
            "mechanism, and trade-off."
        )
        stage = "drill"
        kind = "test"
    else:
        title = "Coach adjustment"
        body = signal.get("detected_gap") or "The coach is adjusting the next step."
        stage = "feedback"
        kind = "coach_adjustment"

    card = CoachCard(
        card_id=f"{topic_id}.{stage}.{signal.get('event_type', 'turn')}",
        topic_id=topic_id,
        topic_name=topic_name,
        mode=mode,
        stage=stage,
        eyebrow="Coach adjustment",
        title=title,
        objective="Adjust the session based on the latest answer.",
        visible_body=body,
        coach_brief=signal.get("coach_brief", ""),
        source_refs=_source_refs(resources or []),
        personalization={
            "detected_gap": signal.get("detected_gap", ""),
            "specificity_score": signal.get("specificity_score", 0),
            "confidence_signal": signal.get("confidence_signal", ""),
        },
        actions=LOCAL_CARD_ACTIONS,
        detail={
            "body": body,
            "key_points": detail_key_points,
            "recommended_card_id": signal.get("recommended_card_id", ""),
        },
    )
    return SessionFrame(
        session_id=session_id,
        mode=mode,
        topic_id=topic_id,
        topic_name=topic_name,
        kind=kind,
        card=card,
        coach_text=(
            "I am adding a smaller card because the last answer exposed a training signal."
        ),
        spoken_script=body,
        source=_source_block(resources or []),
        unit=_unit(topic_id, topic_name, stage=stage),
        actions=LOCAL_CARD_ACTIONS,
    ).to_dict()


def _targeted_networking_followup(signal: dict[str, Any]) -> dict[str, Any]:
    card_id = signal.get("recommended_card_id") or ""
    blueprint = NETWORKING_AGENTIC_BLUEPRINT.get(card_id)
    if not blueprint:
        return {}
    points = blueprint.get("card_points", [])[:3]
    dimensions = blueprint.get("quiz_dimensions", [])[:3]
    body = " ".join(points)
    if dimensions:
        body = (
            f"{body} For the next pass, I would listen for the same idea in a concrete scenario: "
            f"{', '.join(dimensions)}."
        )
    key_points = list(points)
    if signal.get("coach_brief"):
        key_points.append(signal["coach_brief"])
    return {
        "title": TARGETED_NETWORKING_TITLES.get(card_id, "Let's tighten the networking answer"),
        "body": body,
        "key_points": key_points,
    }


def _train_start_frame(**kwargs) -> dict[str, Any]:
    topic_id = kwargs["topic_id"]
    topic_name = kwargs["topic_name"]
    focus = kwargs.get("focus_dimension") or "recap"
    body = (
        f"Start with a 30-second recap of {topic_name}: what it is responsible "
        "for, where it sits in the system, and one failure mode it must handle."
    )
    check = {
        "type": "free_text",
        "prompt": "Give the recap in your own words.",
        "options": [],
    }
    card = CoachCard(
        card_id=f"{topic_id}.train.diagnostic",
        topic_id=topic_id,
        topic_name=topic_name,
        mode="reinforce",
        stage="diagnose",
        eyebrow="Train card",
        title=f"Diagnostic recap: {topic_name}",
        objective="Verify the concept before increasing difficulty.",
        visible_body=body,
        coach_brief=kwargs.get("coach_brief") or (
            "Listen for responsibility, placement, mechanism, and failure mode."
        ),
        check=check,
        rubric_signals=[
            {"name": "specificity", "target": "names a concrete mechanism"},
            {"name": "tradeoffs", "target": "names what gets harder"},
        ],
        source_refs=_source_refs(kwargs.get("resources") or []),
        personalization={
            "mastery": kwargs.get("mastery", 0),
            "focus_dimension": focus,
        },
        actions=LOCAL_CARD_ACTIONS,
        detail={
            "body": body,
            "key_points": [
                "Responsibility: what job does it do?",
                "Placement: where does it sit in the request or data path?",
                "Failure mode: what breaks or gets expensive?",
            ],
        },
    )
    return SessionFrame(
        session_id=kwargs["session_id"],
        mode="reinforce",
        topic_id=topic_id,
        topic_name=topic_name,
        kind="diagnose",
        card=card,
        coach_text="Train starts with one diagnostic recap card.",
        spoken_script=body,
        source=_source_block(kwargs.get("resources") or []),
        unit=_unit(topic_id, topic_name, stage="diagnose"),
        check=check,
        actions=LOCAL_CARD_ACTIONS,
    ).to_dict()


def _mock_start_frame(**kwargs) -> dict[str, Any]:
    topic_id = kwargs["topic_id"]
    topic_name = kwargs["topic_name"]
    body = (
        f"Run {topic_name} like an interview. First lock requirements: users, "
        "core operations, scale, latency, reliability, and explicit non-goals."
    )
    card = CoachCard(
        card_id=f"{topic_id}.mock.requirements",
        topic_id=topic_id,
        topic_name=topic_name,
        mode="mock_system_design",
        stage="interview",
        eyebrow="Mock stage",
        title="Requirements pressure point",
        objective="Collect high-signal evidence before design begins.",
        visible_body=body,
        coach_brief=kwargs.get("coach_brief") or (
            "Probe requirements first; do not teach unless the user pauses the mock."
        ),
        rubric_signals=[
            {"name": "requirements", "target": "clarifies functional and non-functional scope"},
            {"name": "specificity", "target": "uses concrete scale and success metrics"},
            {"name": "communication", "target": "keeps assumptions visible"},
        ],
        source_refs=_source_refs(kwargs.get("resources") or []),
        personalization={
            "mastery": kwargs.get("mastery", 0),
            "focus_dimension": kwargs.get("focus_dimension", ""),
        },
        actions=LOCAL_CARD_ACTIONS,
        detail={
            "body": body,
            "key_points": [
                "Clarify who uses the system and what operation matters most.",
                "Ask for scale before drawing architecture.",
                "Name non-goals so the answer does not sprawl.",
            ],
        },
    )
    return SessionFrame(
        session_id=kwargs["session_id"],
        mode="mock_system_design",
        topic_id=topic_id,
        topic_name=topic_name,
        kind="interview",
        card=card,
        coach_text="Mock starts with the active interview stage card.",
        spoken_script=body,
        source=_source_block(kwargs.get("resources") or []),
        unit=_unit(topic_id, topic_name, stage="requirements"),
        actions=LOCAL_CARD_ACTIONS,
    ).to_dict()


def _learn_route_frame(**kwargs) -> dict[str, Any]:
    topic_id = kwargs["topic_id"]
    topic_name = kwargs["topic_name"]
    body = (
        f"Learn {topic_name} by building one mental model, checking it, repairing "
        "the first weak point, and then retesting."
    )
    card = CoachCard(
        card_id=f"{topic_id}.learn.route",
        topic_id=topic_id,
        topic_name=topic_name,
        mode="learn",
        stage="teach",
        eyebrow="Learn card",
        title=f"Learn path: {topic_name}",
        objective="Build a source-grounded mental model before pressure.",
        visible_body=body,
        source_refs=_source_refs(kwargs.get("resources") or []),
        actions=LOCAL_CARD_ACTIONS,
        detail={"body": body},
    )
    return SessionFrame(
        session_id=kwargs["session_id"],
        mode="learn",
        topic_id=topic_id,
        topic_name=topic_name,
        kind="teach",
        card=card,
        coach_text="Learn starts with one source-grounded card.",
        spoken_script=body,
        source=_source_block(kwargs.get("resources") or []),
        unit=_unit(topic_id, topic_name, stage="teach"),
        actions=LOCAL_CARD_ACTIONS,
    ).to_dict()


def _source_refs(resources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    refs = []
    for resource in resources[:3]:
        if not resource:
            continue
        refs.append({
            "label": resource.get("title") or resource.get("label") or "Source",
            "url": resource.get("url"),
            "type": resource.get("type", "resource"),
        })
    return refs


def _source_block(resources: list[dict[str, Any]]) -> dict[str, Any]:
    refs = _source_refs(resources)
    return {
        "id": "topic_resources",
        "label": "Sources",
        "resources": refs,
        "note": "Trusted source material feeds the card; the coach controls the practice loop.",
    }


def _unit(topic_id: str, topic_name: str, *, stage: str) -> dict[str, Any]:
    return {
        "id": f"{topic_id}.{stage}",
        "index": 1,
        "total": 1,
        "title": topic_name,
        "objective": stage.replace("_", " "),
        "estimated_read_seconds": 30,
    }


def _signal_key_points(signal: dict[str, Any]) -> list[str]:
    points = []
    if signal.get("detected_gap"):
        points.append(f"Detected gap: {signal['detected_gap']}")
    score = signal.get("specificity_score")
    if score is not None:
        points.append(f"Specificity score: {score}")
    if signal.get("recommended_action"):
        points.append(f"Recommended action: {signal['recommended_action']}")
    return points
