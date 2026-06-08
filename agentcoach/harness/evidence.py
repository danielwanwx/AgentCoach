"""Evidence event helpers for harness missions."""
from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any


def build_evidence_event(
    *,
    mission_id: str,
    user_id: str,
    topic_id: str,
    role_family: str,
    stage: str,
    input_text: str,
    score: float,
    gap_signals: list[str] | None = None,
    strength_signals: list[str] | None = None,
    source_refs: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    return {
        "event_id": uuid.uuid4().hex[:12],
        "mission_id": mission_id,
        "user_id": user_id,
        "topic_id": topic_id,
        "role_family": role_family,
        "stage": stage,
        "input_text": input_text,
        "score": float(score),
        "gap_signals": list(gap_signals or []),
        "strength_signals": list(strength_signals or []),
        "source_refs": list(source_refs or []),
        "created_at": datetime.utcnow().isoformat(),
    }
