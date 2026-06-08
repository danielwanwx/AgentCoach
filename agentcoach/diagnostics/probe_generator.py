"""Deterministic topic sniffing and diagnostic probe generation."""
from __future__ import annotations

import re
from typing import Any


TOPIC_PATTERNS = [
    {
        "topic_id": "system_design.rate_limiting",
        "topic_name": "Rate Limiting",
        "domain": "system_design",
        "aliases": ["rate limiter", "rate limiting", "token bucket", "quota", "429", "llm gateway"],
        "cluster": "rate_limiting",
        "role_hint": "ai_engineer",
    },
    {
        "topic_id": "ai_engineering.rag",
        "topic_name": "RAG and Retrieval",
        "domain": "ai_engineering",
        "aliases": ["rag", "retrieval", "vector db", "vector database", "embedding", "rerank", "chunking"],
        "cluster": "rag",
        "role_hint": "ai_engineer",
    },
    {
        "topic_id": "ai_engineering.agent_tool_use",
        "topic_name": "Agent Tool Use",
        "domain": "ai_engineering",
        "aliases": ["agent", "tool calling", "tool use", "planner", "executor", "mcp"],
        "cluster": "agentic",
        "role_hint": "agentic_engineer",
    },
    {
        "topic_id": "ai_engineering.evaluation",
        "topic_name": "AI Evaluation",
        "domain": "ai_engineering",
        "aliases": ["eval", "evaluation", "golden dataset", "regression", "observability"],
        "cluster": "evaluation",
        "role_hint": "ai_engineer",
    },
    {
        "topic_id": "system_design.caching",
        "topic_name": "Caching",
        "domain": "system_design",
        "aliases": ["cache", "caching", "redis", "context cache"],
        "cluster": "caching",
        "role_hint": "ai_engineer",
    },
    {
        "topic_id": "system_design.url_shortener",
        "topic_name": "URL Shortener",
        "domain": "system_design",
        "aliases": ["url shortener", "bitly", "tinyurl", "short url"],
        "cluster": "system_design",
        "role_hint": "swe_ai_platform",
    },
]


def sniff_topic(
    input_text: str,
    *,
    target_role: str = "",
    background: str = "",
) -> dict[str, Any]:
    text = (input_text or "").strip()
    lower = text.lower()
    best = None
    best_hits = 0
    for pattern in TOPIC_PATTERNS:
        hits = sum(1 for alias in pattern["aliases"] if alias in lower)
        if hits > best_hits:
            best = pattern
            best_hits = hits
    if best is None:
        title = _title_from_text(text)
        return {
            "topic_id": _freeform_topic_id(title),
            "topic_name": title,
            "domain": "ai_engineering" if _looks_ai_native(lower) else "system_design",
            "cluster": "freeform",
            "confidence": 0.35,
            "input_kind": _input_kind(text),
            "role_hint": target_role or ("ai_engineer" if _looks_ai_native(lower) else "swe_ai_platform"),
            "background": background,
            "matched_aliases": [],
        }
    return {
        "topic_id": best["topic_id"],
        "topic_name": best["topic_name"],
        "domain": best["domain"],
        "cluster": best["cluster"],
        "confidence": min(0.95, 0.55 + best_hits * 0.18),
        "input_kind": _input_kind(text),
        "role_hint": target_role or best["role_hint"],
        "background": background,
        "matched_aliases": [alias for alias in best["aliases"] if alias in lower],
    }


def generate_diagnostic_probe(
    topic_sniff: dict[str, Any],
    *,
    target_role: str = "",
) -> dict[str, Any]:
    cluster = topic_sniff.get("cluster") or "freeform"
    role = target_role or topic_sniff.get("role_hint") or "ai_engineer"
    questions = _questions_for_cluster(cluster, topic_sniff, role)
    return {
        "probe_id": f"{topic_sniff.get('topic_id', 'topic')}.diagnostic.v1",
        "topic_id": topic_sniff.get("topic_id", "freeform.topic"),
        "topic_name": topic_sniff.get("topic_name", "Topic"),
        "target_role": role,
        "questions": questions[:5],
    }


def _questions_for_cluster(cluster: str, topic: dict[str, Any], role: str) -> list[dict[str, Any]]:
    topic_name = topic.get("topic_name", "this topic")
    if cluster == "rate_limiting":
        return [
            _tf("q1", "A token bucket always guarantees fair per-user distribution.", False, "definition"),
            _mc(
                "q2",
                "For an enterprise LLM gateway, which limit most directly protects cost?",
                [
                    ("requests_per_ip", "Requests per IP"),
                    ("tokens_per_tenant", "Tokens per tenant"),
                    ("database_rows", "Database rows per request"),
                    ("browser_tabs", "Browser tabs per user"),
                ],
                "tokens_per_tenant",
                "transfer",
            ),
            _short(
                "q3",
                "Name one failure mode if a client retries aggressively after hitting a rate limit.",
                ["retry storm", "cost", "overload", "backoff", "quota", "duplicate"],
                "failure_mode",
            ),
        ]
    if cluster == "rag":
        return [
            _tf("q1", "RAG removes the need for evaluation because answers are source-grounded.", False, "evaluation"),
            _mc(
                "q2",
                "Which issue is most likely caused by poor chunking or retrieval quality?",
                [
                    ("grounding_gap", "The answer cites irrelevant context."),
                    ("syntax_error", "The application fails to parse Python."),
                    ("tls_timeout", "The browser cannot complete TLS."),
                    ("dns_cache", "The DNS record is stale."),
                ],
                "grounding_gap",
                "retrieval",
            ),
            _short(
                "q3",
                "What would you measure to know whether retrieval improved an LLM product?",
                ["recall", "precision", "grounding", "answer quality", "eval", "latency"],
                "evaluation",
            ),
        ]
    if cluster == "agentic":
        return [
            _tf("q1", "Adding more tools to an agent always improves its reliability.", False, "agentic"),
            _mc(
                "q2",
                "Which design choice makes a tool-using agent easier to debug?",
                [
                    ("trace_steps", "Trace each plan step, tool call, and observation."),
                    ("hide_tools", "Hide tool calls from logs."),
                    ("increase_temperature", "Increase model temperature by default."),
                    ("remove_eval", "Remove evals so the agent explores freely."),
                ],
                "trace_steps",
                "failure_mode",
            ),
            _short(
                "q3",
                "Name one guardrail for an agent that can call external tools.",
                ["allowlist", "permission", "human", "budget", "schema", "sandbox", "approval"],
                "productionization",
            ),
        ]
    if cluster == "evaluation":
        return [
            _tf("q1", "A single impressive demo is enough evidence that an AI feature is production-ready.", False, "evaluation"),
            _mc(
                "q2",
                "What belongs in a basic eval harness?",
                [
                    ("golden_set", "A golden set, rubric, scorer, and regression checks."),
                    ("only_prompt", "Only the latest prompt text."),
                    ("dashboard_color", "A dashboard color palette."),
                    ("random_users", "Only random user comments."),
                ],
                "golden_set",
                "evaluation",
            ),
            _short(
                "q3",
                "Name one failure category an LLM eval should track.",
                ["hallucination", "grounding", "tool", "latency", "cost", "safety", "format"],
                "failure_mode",
            ),
        ]
    return [
        _tf("q1", f"Knowing the definition of {topic_name} is enough to use it well in an interview.", False, "transfer"),
        _mc(
            "q2",
            f"What should you explain before choosing {topic_name} in a system design answer?",
            [
                ("requirement_tradeoff", "The requirement and trade-off it addresses."),
                ("brand_name", "The vendor with the best brand name."),
                ("all_features", "Every possible feature it could support."),
                ("syntax", "The syntax of one library."),
            ],
            "requirement_tradeoff",
            "tradeoff",
        ),
        _short(
            "q3",
            f"Give one failure mode or operational cost of {topic_name}.",
            ["failure", "latency", "cost", "consistency", "complexity", "reliability", "monitor"],
            "failure_mode",
        ),
    ]


def _tf(question_id: str, prompt: str, correct: bool, gap_signal: str) -> dict[str, Any]:
    return {
        "question_id": question_id,
        "type": "true_false",
        "prompt": prompt,
        "options": [{"id": "true", "label": "True"}, {"id": "false", "label": "False"}],
        "correct_option_id": "true" if correct else "false",
        "expected_keywords": [],
        "gap_signal": gap_signal,
    }


def _mc(
    question_id: str,
    prompt: str,
    options: list[tuple[str, str]],
    correct: str,
    gap_signal: str,
) -> dict[str, Any]:
    return {
        "question_id": question_id,
        "type": "multiple_choice",
        "prompt": prompt,
        "options": [{"id": oid, "label": label} for oid, label in options],
        "correct_option_id": correct,
        "expected_keywords": [],
        "gap_signal": gap_signal,
    }


def _short(
    question_id: str,
    prompt: str,
    expected_keywords: list[str],
    gap_signal: str,
) -> dict[str, Any]:
    return {
        "question_id": question_id,
        "type": "short_answer",
        "prompt": prompt,
        "options": [],
        "correct_option_id": "",
        "expected_keywords": expected_keywords,
        "gap_signal": gap_signal,
    }


def _looks_ai_native(lower: str) -> bool:
    return any(term in lower for term in (
        "llm", "rag", "agent", "ai", "embedding", "vector", "eval", "prompt",
        "retrieval", "mcp", "tool calling",
    ))


def _input_kind(text: str) -> str:
    if len(text) > 300:
        return "pasted_content"
    if re.search(r"https?://", text):
        return "url"
    if any(term in text.lower() for term in ("job description", "requirements", "responsibilities")):
        return "job_description"
    return "topic"


def _title_from_text(text: str) -> str:
    words = re.findall(r"[A-Za-z0-9][A-Za-z0-9+/#.-]*", text)
    if not words:
        return "AI Engineering Topic"
    return " ".join(words[:6]).strip().title()


def _freeform_topic_id(title: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", title.lower()).strip("_") or "topic"
    return f"ai_engineering.{slug}"
