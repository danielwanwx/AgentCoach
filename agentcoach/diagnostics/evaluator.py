"""Evaluate diagnostic answers into learner diagnosis."""
from __future__ import annotations

from typing import Any


def evaluate_diagnostic_answers(
    probe: dict[str, Any],
    answers: list[dict[str, Any]],
    *,
    topic_sniff: dict[str, Any],
    target_role: str = "",
    background: str = "",
) -> dict[str, Any]:
    by_id = {str(a.get("question_id")): str(a.get("answer", "")).strip() for a in answers or []}
    question_results = []
    correct_count = 0
    gap_signals: list[str] = []
    strength_signals: list[str] = []
    for question in probe.get("questions") or []:
        answer = by_id.get(str(question.get("question_id")), "")
        correct = _is_correct(question, answer)
        if correct:
            correct_count += 1
            strength_signals.append(question.get("gap_signal") or "concept")
        else:
            gap = question.get("gap_signal") or "concept"
            if gap not in gap_signals:
                gap_signals.append(gap)
        question_results.append({
            "question_id": question.get("question_id"),
            "answer": answer,
            "correct": correct,
            "gap_signal": question.get("gap_signal", ""),
        })

    total = max(1, len(probe.get("questions") or []))
    score = correct_count / total
    concept_level = _concept_level(score)
    current_base = _normalize_background(background)
    target = target_role or probe.get("target_role") or topic_sniff.get("role_hint") or "ai_engineer"
    return {
        "topic_id": probe.get("topic_id"),
        "topic_name": probe.get("topic_name"),
        "concept_level": concept_level,
        "score": round(score, 2),
        "current_base": current_base,
        "target_role": target,
        "swe_base_strengths": _swe_strengths(current_base),
        "ai_native_gaps": _ai_gaps(gap_signals, target),
        "fde_gaps": _fde_gaps(gap_signals, target),
        "interview_gaps": _interview_gaps(gap_signals),
        "gap_signals": gap_signals,
        "strength_signals": sorted(set(strength_signals)),
        "question_results": question_results,
        "next_training_focus": _next_training_focus(gap_signals, concept_level, target),
    }


def _is_correct(question: dict[str, Any], answer: str) -> bool:
    qtype = question.get("type")
    answer_norm = answer.lower().strip()
    if qtype in {"true_false", "multiple_choice"}:
        correct = str(question.get("correct_option_id", "")).lower()
        if answer_norm == correct:
            return True
        for opt in question.get("options") or []:
            if opt.get("id", "").lower() == correct:
                label = str(opt.get("label", "")).lower()
                return bool(label and label in answer_norm)
        return False
    keywords = [str(k).lower() for k in question.get("expected_keywords") or []]
    if not keywords:
        return len(answer_norm.split()) >= 5
    return any(k in answer_norm for k in keywords)


def _concept_level(score: float) -> str:
    if score >= 0.85:
        return "interview_ready"
    if score >= 0.6:
        return "usable"
    if score >= 0.35:
        return "fuzzy"
    return "unknown"


def _normalize_background(background: str = "") -> str:
    value = (background or "").strip().lower()
    for key in ("backend", "fullstack", "infra", "data", "ml", "product"):
        if key in value:
            return key
    return "backend"


def _swe_strengths(background: str) -> list[str]:
    base = {
        "backend": ["API design", "service boundaries", "production reliability"],
        "fullstack": ["user-facing product flow", "API integration", "shipping behavior"],
        "infra": ["reliability", "observability", "deployment constraints"],
        "data": ["data pipelines", "quality metrics", "retrieval foundations"],
        "ml": ["model quality", "evaluation", "experimentation"],
        "product": ["customer problem framing", "business impact", "demo narrative"],
    }
    return base.get(background, base["backend"])


def _ai_gaps(gaps: list[str], target: str) -> list[str]:
    out = []
    for gap in gaps:
        if gap in {"transfer", "evaluation", "retrieval", "agentic", "productionization"}:
            out.append(gap)
    if target in {"ai_engineer", "agentic_engineer", "applied_ai"} and not out:
        out.append("ai_native_transfer")
    return out


def _fde_gaps(gaps: list[str], target: str) -> list[str]:
    if target != "fde":
        return []
    out = [gap for gap in gaps if gap in {"communication", "fde_customer_framing", "transfer"}]
    return out or ["customer_deployment_framing"]


def _interview_gaps(gaps: list[str]) -> list[str]:
    out = [gap for gap in gaps if gap in {"tradeoff", "failure_mode", "communication"}]
    return out or (["pressure_retest"] if gaps else [])


def _next_training_focus(gaps: list[str], concept_level: str, target: str) -> list[str]:
    focus = []
    if concept_level in {"unknown", "fuzzy"}:
        focus.append("repair mental model")
    if "transfer" in gaps or target in {"ai_engineer", "agentic_engineer", "applied_ai"}:
        focus.append("transfer SWE concept into AI-native scenario")
    if "failure_mode" in gaps or "tradeoff" in gaps:
        focus.append("practice trade-off and failure-mode answer")
    if target == "fde":
        focus.append("frame answer as customer deployment impact")
    return focus[:3] or ["run a pressure retest"]
