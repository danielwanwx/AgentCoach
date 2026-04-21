"""Skill profile + report renderer.

Reads structured assessments produced by ``agentcoach.analytics.scorer.Scorer``
(persisted via ``AnalyticsStore.record_assessment``) and renders:

1. A per-session **Skill Report** — dimension bars, strengths, focus areas.
2. A per-domain **Growth Curve** — ASCII sparkline trajectories across sessions.

The renderer intentionally consumes plain dicts so it works equally well for
(a) the CLI wrap-up path, (b) the e2e harness's per-persona aggregate, and
(c) offline accuracy verification scripts.
"""
from __future__ import annotations

from typing import Iterable, Optional

from agentcoach.scoring.rubrics import get_rubric

_SPARK_CHARS = "▁▂▃▄▅▆▇█"


def _bar(score: float, width: int = 10) -> str:
    """Return a unicode progress bar for a score in [0, 5]."""
    score = max(0.0, min(5.0, float(score)))
    filled = int(round((score / 5.0) * width))
    return "█" * filled + "░" * (width - filled)


def _sparkline(values: Iterable[float], lo: float = 1.0, hi: float = 5.0) -> str:
    """Render values as a unicode sparkline. Empty → empty string."""
    vals = [float(v) for v in values]
    if not vals:
        return ""
    span = hi - lo
    if span <= 0:
        return _SPARK_CHARS[0] * len(vals)
    out = []
    for v in vals:
        frac = max(0.0, min(1.0, (v - lo) / span))
        idx = int(round(frac * (len(_SPARK_CHARS) - 1)))
        out.append(_SPARK_CHARS[idx])
    return "".join(out)


def _trend_label(values: list[float]) -> str:
    """Summarize movement: ↑ / ↓ / flat based on first-half vs second-half mean."""
    if len(values) < 2:
        return "n/a"
    mid = len(values) // 2
    first = sum(values[:mid]) / max(mid, 1)
    second = sum(values[mid:]) / max(len(values) - mid, 1)
    diff = second - first
    if diff >= 0.4:
        return f"↑ +{diff:.1f}"
    if diff <= -0.4:
        return f"↓ {diff:.1f}"
    return "→ flat"


def _resolve_domain(topic_id: str, explicit: Optional[str] = None) -> str:
    if explicit:
        return explicit
    return topic_id.split(".", 1)[0] if "." in topic_id else (topic_id or "system_design")


# -------- Per-session report -------- #

def render_skill_report(
    assessment: dict,
    *,
    mastery_before: Optional[int] = None,
    mastery_after: Optional[int] = None,
    width: int = 10,
) -> str:
    """Render a human-readable skill report for one session.

    `assessment` is the dict returned by ``Scorer.score_session``-style code
    (keys: ``topic_id``, ``overall_score``, ``dimensions``, ``strengths``,
    ``areas_to_improve``) or a row from ``AnalyticsStore.get_assessments``.
    """
    topic = assessment.get("topic_id") or assessment.get("topic") or "general"
    mode = assessment.get("mode", "")
    domain = _resolve_domain(topic, assessment.get("domain"))
    overall = float(assessment.get("overall_score") or 0.0)
    dims = assessment.get("dimensions") or []
    strengths = assessment.get("strengths") or []
    areas = assessment.get("areas_to_improve") or []

    rubric = get_rubric(domain)
    rubric_dims = rubric.get("dimensions", {})

    header_bits = [f"=== Skill Report: {topic}"]
    if mode:
        header_bits.append(f"({mode})")
    header_bits.append("===")
    header = " ".join(header_bits)

    lines = [header]
    overall_line = f"Overall: {overall:.1f}/5  {_bar(overall, width)}"
    if mastery_before is not None and mastery_after is not None:
        delta = mastery_after - mastery_before
        sign = "+" if delta >= 0 else ""
        overall_line += f"   Mastery: {mastery_before}% → {mastery_after}% ({sign}{delta})"
    lines.append(overall_line)
    lines.append("")

    # Dimension rows — honour rubric order when possible, otherwise keep raw order
    raw_by_name = {d.get("name"): d for d in dims if d.get("name")}
    ordered_names = [n for n in rubric_dims.keys() if n in raw_by_name]
    # Append any emitted dims that were NOT in the rubric (forward-compat)
    for d in dims:
        name = d.get("name")
        if name and name not in ordered_names:
            ordered_names.append(name)

    if ordered_names:
        name_w = max(len(n) for n in ordered_names)
        for name in ordered_names:
            d = raw_by_name.get(name, {"score": "?", "evidence": ""})
            try:
                score = float(d.get("score"))
            except (TypeError, ValueError):
                score = 0.0
            evidence = (d.get("evidence") or "").strip()
            evidence_short = evidence if len(evidence) <= 80 else evidence[:77] + "..."
            lines.append(
                f"  {name.ljust(name_w)}  {_bar(score, width)}  {score:.0f}/5"
                + (f"   {evidence_short}" if evidence_short else "")
            )
        lines.append("")

    if strengths:
        lines.append("Strengths")
        for s in strengths[:4]:
            lines.append(f"  • {s}")
        lines.append("")

    if areas:
        lines.append("Focus next")
        for a in areas[:4]:
            lines.append(f"  • {a}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


# -------- Growth curve -------- #

def build_skill_profile(store, user_id: str, domain: str, limit: int = 20) -> dict:
    """Collect per-dimension history for a user in a domain.

    Returns {
      'domain': ...,
      'sessions_counted': int,
      'dimensions': {
         name: {
           'current': float,     # latest recorded score
           'mean': float,        # average over window
           'trend': str,         # '↑ +x.x' / '↓ -x.x' / '→ flat'
           'spark': str,         # unicode sparkline (oldest→newest)
           'history': [score,...],
         },
         ...
      }
    }
    """
    traj = store.get_skill_trajectory(user_id, domain=domain, limit=limit)
    dims_out: dict = {}
    for name, entries in traj.items():
        values = [e["score"] for e in entries]
        if not values:
            continue
        dims_out[name] = {
            "current": values[-1],
            "mean": sum(values) / len(values),
            "trend": _trend_label(values),
            "spark": _sparkline(values),
            "history": values,
        }
    return {
        "domain": domain,
        "sessions_counted": max((len(v) for v in traj.values()), default=0),
        "dimensions": dims_out,
    }


def render_growth_curve(profile: dict, *, order: Optional[list] = None) -> str:
    """Render a profile (from ``build_skill_profile``) as ASCII text."""
    domain = profile.get("domain", "unknown")
    dims = profile.get("dimensions") or {}
    if not dims:
        return f"=== Skills — {domain} ===\n  (no assessments yet — complete a session first)\n"

    rubric_order = list(get_rubric(domain).get("dimensions", {}).keys())
    ordered = order or [n for n in rubric_order if n in dims] + \
        [n for n in dims if n not in rubric_order]

    name_w = max(len(n) for n in ordered)
    sessions = profile.get("sessions_counted", 0)
    lines = [f"=== Skills — {domain} (last {sessions} sessions) ==="]
    for name in ordered:
        d = dims[name]
        lines.append(
            f"  {name.ljust(name_w)}  {d['current']:.1f}  {d['spark']:<12}  ({d['trend']}, mean {d['mean']:.1f})"
        )
    lines.append("")
    return "\n".join(lines)


# -------- Aggregation helpers (e2e / per-persona) -------- #

def aggregate_assessments(assessments: list) -> dict:
    """Aggregate a list of assessment dicts into a single summary.

    Used e.g. to produce a per-persona or per-scenario roll-up in the e2e
    report. Returns a structure shaped like a single assessment so we can
    reuse ``render_skill_report`` on it.
    """
    if not assessments:
        return {}
    overall = sum(float(a.get("overall_score") or 0) for a in assessments) / len(assessments)

    dim_totals: dict = {}
    for a in assessments:
        for d in a.get("dimensions", []) or []:
            name = d.get("name")
            if not name:
                continue
            try:
                score = float(d.get("score"))
            except (TypeError, ValueError):
                continue
            dim_totals.setdefault(name, []).append(score)
    dims = [
        {
            "name": name,
            "score": round(sum(vals) / len(vals), 1),
            "evidence": f"avg over {len(vals)} sessions",
        }
        for name, vals in dim_totals.items()
    ]

    strengths: list = []
    areas: list = []
    for a in assessments:
        for s in (a.get("strengths") or [])[:2]:
            if s and s not in strengths:
                strengths.append(s)
        for x in (a.get("areas_to_improve") or [])[:2]:
            if x and x not in areas:
                areas.append(x)

    return {
        "topic_id": assessments[0].get("topic_id", "aggregate"),
        "mode": assessments[0].get("mode", "mixed"),
        "overall_score": round(overall, 2),
        "dimensions": dims,
        "strengths": strengths[:6],
        "areas_to_improve": areas[:6],
        "sessions_counted": len(assessments),
    }
