"""Build role-aware harness plans from diagnosis and source material."""
from __future__ import annotations

from typing import Any


def build_harness_plan(
    *,
    mission_id: str,
    topic_sniff: dict[str, Any],
    learner_diagnosis: dict[str, Any],
    role_profile: dict[str, Any],
    transition_gaps: dict[str, Any],
    source_manifest: dict[str, Any],
) -> dict[str, Any]:
    concept_level = learner_diagnosis.get("concept_level", "fuzzy")
    target_role = learner_diagnosis.get("target_role") or role_profile.get("role_family") or "ai_engineer"
    stages = _stages_for_level(concept_level, target_role, transition_gaps)
    next_action = _next_action(
        topic_sniff=topic_sniff,
        learner_diagnosis=learner_diagnosis,
        role_profile=role_profile,
        transition_gaps=transition_gaps,
        source_manifest=source_manifest,
    )
    return {
        "mission_id": mission_id,
        "topic_id": topic_sniff.get("topic_id"),
        "topic_name": topic_sniff.get("topic_name"),
        "target_role": target_role,
        "objective": _objective(topic_sniff, role_profile, transition_gaps),
        "stages": stages,
        "next_action": next_action,
    }


def _stages_for_level(concept_level: str, target_role: str, transition_gaps: dict[str, Any]) -> list[dict[str, Any]]:
    missing = transition_gaps.get("missing_clusters") or []
    stages = []
    if concept_level in {"unknown", "fuzzy"}:
        stages.append(_stage(
            "learn",
            "Repair the mental model before pressure.",
            "User explains the concept in their own words with one mechanism.",
            "short_teach_then_recall",
        ))
    stages.append(_stage(
        "recall",
        "Closed-book recall proves this is not passive reading.",
        "User gives a 45-second explanation without hints.",
        "active_recall",
    ))
    stages.append(_stage(
        "drill",
        "Target the weakest gap from diagnosis.",
        f"User handles a focused drill on {', '.join(missing[:2]) or 'trade-offs'}.",
        "gap_drill",
    ))
    stages.append(_stage(
        "transfer",
        f"Move the concept into a {target_role.replace('_', ' ')} scenario.",
        "User connects SWE concept to AI-native or customer-facing constraints.",
        "role_transfer",
    ))
    stages.append(_stage(
        "retest",
        "Retest the same weak signal after feedback.",
        "User improves the previous weak answer without a lecture.",
        "pressure_retest",
    ))
    return stages


def _stage(stage: str, reason: str, success_signal: str, prompt_strategy: str) -> dict[str, Any]:
    return {
        "stage": stage,
        "reason": reason,
        "success_signal": success_signal,
        "prompt_strategy": prompt_strategy,
        "source_strategy": {"use_source_manifest": True},
    }


def _next_action(
    *,
    topic_sniff: dict[str, Any],
    learner_diagnosis: dict[str, Any],
    role_profile: dict[str, Any],
    transition_gaps: dict[str, Any],
    source_manifest: dict[str, Any],
) -> dict[str, Any]:
    concept_level = learner_diagnosis.get("concept_level", "fuzzy")
    mode = "learn" if concept_level in {"unknown", "fuzzy"} else "reinforce"
    if concept_level == "interview_ready" and topic_sniff.get("domain") == "system_design":
        mode = "mock_system_design"
    focus = _focus_dimension(learner_diagnosis, transition_gaps)
    coach_brief = _coach_brief(topic_sniff, learner_diagnosis, role_profile, transition_gaps)
    return {
        "topic_id": topic_sniff.get("topic_id"),
        "topic_name": topic_sniff.get("topic_name"),
        "domain": topic_sniff.get("domain", "system_design"),
        "mode": mode,
        "focus_dimension": focus,
        "coach_brief": coach_brief,
        "reason": _objective(topic_sniff, role_profile, transition_gaps),
        "source_manifest_id": source_manifest.get("manifest_id"),
    }


def _focus_dimension(learner_diagnosis: dict[str, Any], transition_gaps: dict[str, Any]) -> str:
    gaps = learner_diagnosis.get("gap_signals") or []
    if gaps:
        return str(gaps[0])
    missing = transition_gaps.get("missing_clusters") or []
    if missing:
        return str(missing[0])
    return "transfer"


def _objective(topic_sniff: dict[str, Any], role_profile: dict[str, Any], transition_gaps: dict[str, Any]) -> str:
    topic = topic_sniff.get("topic_name", "this topic")
    role = role_profile.get("label", "AI Engineer")
    focus = transition_gaps.get("recommended_focus") or []
    focus_text = focus[0] if focus else "convert the concept into interview-ready behavior"
    return f"Train {topic} for {role}: {focus_text}"


def _coach_brief(
    topic_sniff: dict[str, Any],
    learner_diagnosis: dict[str, Any],
    role_profile: dict[str, Any],
    transition_gaps: dict[str, Any],
) -> str:
    topic = topic_sniff.get("topic_name", "this topic")
    role = role_profile.get("label", "AI Engineer")
    level = learner_diagnosis.get("concept_level", "fuzzy")
    gaps = ", ".join(learner_diagnosis.get("gap_signals") or transition_gaps.get("missing_clusters") or ["transfer"])
    return (
        f"The learner is {level} on {topic} for a {role} target. "
        f"Focus on {gaps}. Start with one short diagnostic repair, ask one active-recall prompt, "
        "then transfer the answer into an AI-native or customer-facing scenario."
    )
