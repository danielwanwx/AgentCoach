"""Local role taxonomy for AI-native engineering transition coaching."""
from __future__ import annotations

from copy import deepcopy
from typing import Any


ROLE_FAMILIES = {
    "ai_engineer": {
        "label": "AI Engineer",
        "must_have_clusters": [
            "core_swe",
            "llm_application_engineering",
            "rag_retrieval",
            "evaluation",
            "productionization",
            "system_design",
        ],
        "differentiators": [
            "Turns ambiguous product needs into reliable LLM-backed systems.",
            "Balances model quality, latency, cost, and safety in production.",
            "Can explain AI architecture with normal SWE trade-off discipline.",
        ],
        "interview_likely_signals": [
            "RAG and retrieval quality",
            "LLM eval harness design",
            "API/data modeling for AI products",
            "Production failure modes",
            "Cost and latency control",
        ],
    },
    "agentic_engineer": {
        "label": "Agentic Engineer",
        "must_have_clusters": [
            "core_swe",
            "llm_application_engineering",
            "agentic_systems",
            "evaluation",
            "observability",
            "productionization",
        ],
        "differentiators": [
            "Designs tool-using systems that can be observed, constrained, and retested.",
            "Understands planner/executor, memory, tool failure, and human-in-the-loop boundaries.",
            "Treats agents as production workflows, not demos.",
        ],
        "interview_likely_signals": [
            "Tool calling and failure handling",
            "Agent loop design",
            "Memory and context strategy",
            "Guardrails and rollback",
            "Agent evaluation",
        ],
    },
    "fde": {
        "label": "Forward Deployed Engineer",
        "must_have_clusters": [
            "core_swe",
            "system_design",
            "ai_application_engineering",
            "fde_customer_deployment",
            "productionization",
            "behavioral_communication",
        ],
        "differentiators": [
            "Finds the real customer workflow and ships into it.",
            "Connects technical choices to business outcome and deployment constraints.",
            "Can demo, scope, integrate, and feed learnings back into product.",
        ],
        "interview_likely_signals": [
            "Customer discovery",
            "Ambiguous problem scoping",
            "Enterprise integration",
            "Deployment constraints",
            "Business impact narrative",
        ],
    },
    "applied_ai": {
        "label": "Applied AI Engineer",
        "must_have_clusters": [
            "core_swe",
            "llm_application_engineering",
            "rag_retrieval",
            "agentic_systems",
            "evaluation",
            "product_sense",
        ],
        "differentiators": [
            "Ships AI product behavior rather than isolated model experiments.",
            "Owns data, UX, evals, and product feedback loops.",
            "Can move quickly without losing production judgment.",
        ],
        "interview_likely_signals": [
            "Product-grounded AI feature design",
            "Structured outputs and model APIs",
            "Retrieval and context quality",
            "User feedback loops",
            "Quality regression handling",
        ],
    },
    "swe_ai_platform": {
        "label": "SWE AI Platform",
        "must_have_clusters": [
            "core_swe",
            "system_design",
            "productionization",
            "observability",
            "evaluation",
            "security_compliance",
        ],
        "differentiators": [
            "Builds the platform layer other AI engineers rely on.",
            "Makes model access, evals, routing, observability, and safety operable.",
            "Bridges infra discipline and AI-specific constraints.",
        ],
        "interview_likely_signals": [
            "Gateway and routing design",
            "Reliability and observability",
            "Multi-tenant controls",
            "Security and policy boundaries",
            "Internal developer experience",
        ],
    },
}


ROLE_ALIASES = {
    "ai": "ai_engineer",
    "ai engineer": "ai_engineer",
    "ai_engineer": "ai_engineer",
    "agent": "agentic_engineer",
    "agent engineer": "agentic_engineer",
    "agentic": "agentic_engineer",
    "agentic_engineer": "agentic_engineer",
    "fde": "fde",
    "forward deployed": "fde",
    "forward_deployed": "fde",
    "forward deployed engineer": "fde",
    "applied ai": "applied_ai",
    "applied_ai": "applied_ai",
    "swe ai platform": "swe_ai_platform",
    "platform": "swe_ai_platform",
}


def normalize_role_family(value: str = "") -> str:
    normalized = (value or "").strip().lower().replace("-", " ").replace("_", " ")
    if not normalized:
        return "ai_engineer"
    return ROLE_ALIASES.get(normalized, ROLE_ALIASES.get(normalized.replace(" ", "_"), "ai_engineer"))


def get_role_profile(role_family: str = "", *, company: str = "") -> dict[str, Any]:
    role_key = normalize_role_family(role_family)
    profile = deepcopy(ROLE_FAMILIES[role_key])
    profile["role_family"] = role_key
    profile["company"] = (company or "").strip() or None
    if profile["company"]:
        profile["source_refs"] = [{
            "label": f"{profile['company']} role context",
            "type": "target_company",
            "url": None,
        }]
    else:
        profile["source_refs"] = []
    return profile
