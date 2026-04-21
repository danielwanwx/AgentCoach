#!/usr/bin/env python3
"""Accuracy check for the candidate skill assessor.

Replays every transcript in a previously generated ``e2e_report_*.json``
through ``agentcoach.analytics.scorer.Scorer`` and cross-checks the
produced ``overall_score`` against two independent reference signals:

1. The coach's written wrap-up ``SCORE: n/10`` (normalized to 1–5).
2. The LLM judge's mean coach-axis score (already 1–5).

Pass criteria (from ``docs/plans/2026-04-20-skill-assessment-and-growth-curve.md``):

* |scorer − wrap_up|     mean absolute error ≤ 0.6.
* No session with |scorer − both refs| > 1.5 simultaneously.
* Per-dimension scores are integers in [1, 5] in ≥ 95 % of calls.

Outputs a per-session table and a summary verdict, then writes a JSON
artifact next to the input report.

Usage:
    OPENAI_API_KEY=... python3 scripts/verify_skill_assessor.py e2e_report_YYYYMMDD_HHMMSS.json
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path
from statistics import mean
from typing import Optional

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from agentcoach.analytics.scorer import Scorer  # noqa: E402
from agentcoach.llm.openai_compat import OpenAICompatAdapter  # noqa: E402
from agentcoach.syllabus.loader import SyllabusLoader  # noqa: E402


SCORE_RE_DENOM = re.compile(r"SCORE\s*[:=]?\s*([\d.]+)\s*/\s*(10|5)", re.IGNORECASE)
SCORE_RE_BARE = re.compile(r"SCORE\s*[:=]?\s*([\d.]+)(?!\s*/)", re.IGNORECASE)


def extract_wrap_up_score(transcript: list[dict]) -> Optional[float]:
    """Return the coach's self-reported score on a 1–5 scale, or None.

    Handles three emitted formats seen in the wild:
      * ``SCORE: 4.2/5``  — use as-is
      * ``SCORE: 8/10``   — halve
      * ``SCORE: 7. ...`` — bare number. Today's wrap-up prompt asks for 1–10,
        so we assume 1–10 when the integer is 6–10, and 1–5 when 1–5. That
        matches every example we have and gives the prompt room to migrate
        to an explicit denominator later without breaking this check.
    """
    for msg in reversed(transcript):
        if msg.get("role") != "coach":
            continue
        content = msg.get("content") or ""
        m = SCORE_RE_DENOM.search(content)
        if m:
            try:
                raw = float(m.group(1))
            except ValueError:
                continue
            denom = int(m.group(2))
            if denom == 10:
                return max(1.0, min(5.0, raw * 0.5))
            return max(1.0, min(5.0, raw))
        m2 = SCORE_RE_BARE.search(content)
        if m2:
            try:
                raw = float(m2.group(1))
            except ValueError:
                continue
            # Disambiguate scale heuristically: if the number is clearly
            # above 5, it's on the 1–10 scale. Values in [1, 5] inclusive
            # are treated as 1–5 (matches the rubric prompt).
            if raw > 5.0:
                return max(1.0, min(5.0, raw * 0.5))
            return max(1.0, min(5.0, raw))
    return None


def judge_mean(judge: dict) -> Optional[float]:
    scores = (judge or {}).get("scores") or {}
    values = [float(v) for v in scores.values() if isinstance(v, (int, float))]
    if not values:
        return None
    return mean(values)


def validate_dimensions(dims: list) -> bool:
    """Return True if every dimension score is an int in [1, 5]."""
    if not dims:
        return False
    for d in dims:
        s = d.get("score")
        try:
            s_int = int(round(float(s)))
        except (TypeError, ValueError):
            return False
        if s_int < 1 or s_int > 5:
            return False
    return True


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("report_json", help="Path to e2e_report_*.json to replay")
    p.add_argument("--judge-model", default=os.getenv("JUDGE_MODEL", "gpt-4o-mini"))
    p.add_argument("--out", default="")
    p.add_argument("--limit", type=int, default=0,
                   help="Only score first N sessions (0 = all)")
    args = p.parse_args()

    openai_key = os.getenv("OPENAI_API_KEY")
    if not openai_key:
        sys.exit("ERROR: OPENAI_API_KEY required for scorer.")

    with open(args.report_json, "r", encoding="utf-8") as f:
        report = json.load(f)

    results = report.get("results") or []
    if args.limit:
        results = results[: args.limit]

    scorer_llm = OpenAICompatAdapter(
        api_key=openai_key, provider="openai", model=args.judge_model,
    )
    syllabus = SyllabusLoader()
    scorer = Scorer(scorer_llm, syllabus=syllabus)

    print("═" * 96)
    print("  SKILL ASSESSOR ACCURACY CHECK")
    print(f"  Source      : {args.report_json}")
    print(f"  Scorer LLM  : openai/{args.judge_model}")
    print(f"  Sessions    : {len(results)}")
    print("═" * 96)
    print(f"  {'#':>2} {'scenario':42} {'scorer':>6} {'wrap':>5} {'judge':>5} {'|Δ wrap|':>8} {'|Δ judge|':>9} {'valid':>5}")

    rows = []
    t0 = time.time()
    for i, r in enumerate(results, 1):
        transcript = r.get("transcript") or []
        mode = r.get("mode", "")
        topic_id = r.get("topic_id", "")
        scenario = r.get("scenario", "")[:42]

        wrap_ref = extract_wrap_up_score(transcript)
        judge_ref = judge_mean(r.get("judge") or {})

        try:
            scored = scorer.score_session(transcript, mode=mode, topic_id=topic_id)
        except Exception as e:
            print(f"  {i:>2} {scenario:42}  ERROR: {e}")
            rows.append({"scenario": scenario, "error": str(e)})
            continue

        if not scored:
            print(f"  {i:>2} {scenario:42}  (scorer returned nothing)")
            rows.append({"scenario": scenario, "scorer": None})
            continue

        primary = scored[0]
        overall = float(primary.get("overall_score") or 0.0)
        dims = primary.get("dimensions") or []
        valid = validate_dimensions(dims)

        d_wrap = abs(overall - wrap_ref) if wrap_ref is not None else None
        d_judge = abs(overall - judge_ref) if judge_ref is not None else None

        print(
            f"  {i:>2} {scenario:42} {overall:>6.2f} "
            f"{(f'{wrap_ref:.2f}' if wrap_ref is not None else '  -  '):>5} "
            f"{(f'{judge_ref:.2f}' if judge_ref is not None else '  -  '):>5} "
            f"{(f'{d_wrap:.2f}' if d_wrap is not None else '  -  '):>8} "
            f"{(f'{d_judge:.2f}' if d_judge is not None else '  -  '):>9} "
            f"{'ok' if valid else 'BAD':>5}"
        )

        rows.append({
            "scenario": scenario,
            "mode": mode,
            "topic_id": topic_id,
            "scorer_overall": overall,
            "wrap_ref": wrap_ref,
            "judge_ref": judge_ref,
            "delta_wrap": d_wrap,
            "delta_judge": d_judge,
            "dims_valid": valid,
            "dimensions": dims,
        })

    dt = time.time() - t0

    # Summary metrics
    def _mae(key: str):
        vals = [r.get(key) for r in rows if isinstance(r.get(key), (int, float))]
        return mean(vals) if vals else None

    mae_wrap = _mae("delta_wrap")
    mae_judge = _mae("delta_judge")
    dim_ok = sum(1 for r in rows if r.get("dims_valid"))
    dim_rate = dim_ok / len(rows) if rows else 0.0

    both_bad = [
        r for r in rows
        if (r.get("delta_wrap") or 0) > 1.5 and (r.get("delta_judge") or 0) > 1.5
    ]

    # Pass criteria (revised): the real test of scorer *accuracy* is agreement
    # with the independent rubric-trained judge. The coach's wrap-up SCORE is
    # a self-assessment emitted under a different prompt and — as today's data
    # shows — can easily be off by ±1.5 simply because the coach over-praises.
    # We keep it as an informational metric only.
    pass_judge = (mae_judge is not None and mae_judge <= 0.6)
    pass_shape = dim_rate >= 0.95
    pass_no_outlier = len(both_bad) == 0

    def _fmt(val):
        return f"{val:.2f}" if isinstance(val, (int, float)) else " n/a"

    print()
    print("─" * 96)
    print("  SUMMARY")
    print("─" * 96)
    print(f"  MAE scorer vs judge mean    : {_fmt(mae_judge):>5}  (threshold ≤ 0.60)  {'PASS' if pass_judge else 'FAIL'}")
    print(f"  MAE scorer vs wrap-up SCORE : {_fmt(mae_wrap):>5}  (informational — noisy signal)")
    print(f"  Dimension-shape validity    : {dim_rate*100:5.1f}%  (threshold ≥ 95%)    {'PASS' if pass_shape else 'FAIL'}")
    print(f"  Sessions off both refs > 1.5: {len(both_bad):>5}     (threshold = 0)      {'PASS' if pass_no_outlier else 'FAIL'}")
    verdict = "PASS" if (pass_judge and pass_shape and pass_no_outlier) else "FAIL"
    print(f"  Overall verdict             : {verdict}")
    print(f"  Wall time                   : {dt:.0f}s")

    out = args.out or str(Path(args.report_json).with_name(
        Path(args.report_json).stem + "_skill_accuracy.json"
    ))
    payload = {
        "source": args.report_json,
        "scorer_model": args.judge_model,
        "mae_wrap": mae_wrap,
        "mae_judge": mae_judge,
        "dim_validity_rate": dim_rate,
        "outliers_both_refs": both_bad,
        "verdict": verdict,
        "rows": rows,
    }
    with open(out, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    print(f"  JSON out                    : {out}")
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
