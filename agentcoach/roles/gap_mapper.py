"""Map diagnostic evidence into role-transition gaps."""
from __future__ import annotations

from typing import Any


BACKGROUND_TRANSFER = {
    "backend": ["core_swe", "system_design", "productionization"],
    "fullstack": ["core_swe", "product_sense", "behavioral_communication"],
    "infra": ["core_swe", "system_design", "observability", "productionization"],
    "data": ["core_swe", "rag_retrieval", "evaluation"],
    "ml": ["evaluation", "productionization", "ai_application_engineering"],
    "product": ["product_sense", "fde_customer_deployment", "behavioral_communication"],
}

GAP_TO_CLUSTER = {
    "definition": "core_swe",
    "mechanism": "llm_application_engineering",
    "tradeoff": "system_design",
    "failure_mode": "productionization",
    "transfer": "ai_application_engineering",
    "communication": "behavioral_communication",
    "fde_customer_framing": "fde_customer_deployment",
    "evaluation": "evaluation",
    "agentic": "agentic_systems",
    "retrieval": "rag_retrieval",
}


def _normalize_background(value: str = "") -> str:
    v = (value or "").strip().lower()
    for key in BACKGROUND_TRANSFER:
        if key in v:
            return key
    return "backend"


def map_transition_gaps(
    *,
    learner_diagnosis: dict[str, Any],
    role_profile: dict[str, Any],
    background: str = "",
) -> dict[str, Any]:
    background_key = _normalize_background(background or learner_diagnosis.get("current_base", ""))
    transfer_strengths = BACKGROUND_TRANSFER.get(background_key, BACKGROUND_TRANSFER["backend"])
    required = list(role_profile.get("must_have_clusters") or [])
    gap_signals = list(learner_diagnosis.get("gap_signals") or [])
    signaled_clusters = [
        GAP_TO_CLUSTER[g] for g in gap_signals
        if g in GAP_TO_CLUSTER and GAP_TO_CLUSTER[g] in required
    ]
    missing = []
    for cluster in required:
        if cluster in transfer_strengths and cluster not in signaled_clusters:
            continue
        if cluster not in missing:
            missing.append(cluster)

    if not missing:
        missing = [cluster for cluster in required if cluster not in transfer_strengths][:2]

    return {
        "background": background_key,
        "transfer_strengths": transfer_strengths,
        "missing_clusters": missing[:5],
        "role_family": role_profile.get("role_family", "ai_engineer"),
        "target_company": role_profile.get("company"),
        "recommended_focus": _recommended_focus(missing, role_profile),
    }


def _recommended_focus(missing: list[str], role_profile: dict[str, Any]) -> list[str]:
    labels = {
        "llm_application_engineering": "Connect the SWE concept to LLM app behavior.",
        "ai_application_engineering": "Connect the SWE concept to AI application behavior.",
        "rag_retrieval": "Practice retrieval, grounding, and quality trade-offs.",
        "agentic_systems": "Practice tool-use workflow and failure handling.",
        "evaluation": "Add eval criteria, golden examples, and regression checks.",
        "productionization": "Name latency, cost, reliability, and deployment guardrails.",
        "fde_customer_deployment": "Frame the technical choice as customer workflow impact.",
        "behavioral_communication": "Tighten the answer into a concise interview narrative.",
        "system_design": "State the architecture trade-off before choosing a component.",
    }
    out = [labels.get(cluster, f"Practice {cluster.replace('_', ' ')}.") for cluster in missing[:3]]
    if not out:
        signals = role_profile.get("interview_likely_signals") or []
        out = [f"Prepare for {signals[0]}." if signals else "Retest the concept under interview pressure."]
    return out
