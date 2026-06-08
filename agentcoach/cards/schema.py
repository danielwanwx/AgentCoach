"""Shared card and frame schema.

Cards are coaching instruments, not a Learn-only UI object. The schema keeps a
stable payload that Learn, Train, and Mock can all render while preserving the
legacy ``card.body`` shape the current frontend already understands.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class CoachCard:
    card_id: str
    topic_id: str
    topic_name: str
    mode: str
    stage: str
    title: str
    objective: str
    visible_body: str
    coach_brief: str = ""
    check: dict[str, Any] | None = None
    rubric_signals: list[dict[str, Any]] = field(default_factory=list)
    source_refs: list[dict[str, Any]] = field(default_factory=list)
    personalization: dict[str, Any] = field(default_factory=dict)
    actions: list[dict[str, Any]] = field(default_factory=list)
    detail: dict[str, Any] = field(default_factory=dict)
    eyebrow: str = "Coach card"

    def to_dict(self) -> dict[str, Any]:
        detail = dict(self.detail)
        if self.coach_brief and "coach_brief" not in detail:
            detail["coach_brief"] = self.coach_brief
        if self.rubric_signals and "rubric_signals" not in detail:
            detail["rubric_signals"] = list(self.rubric_signals)
        if self.source_refs and "sources" not in detail:
            detail["sources"] = list(self.source_refs)
        if self.personalization and "personalization" not in detail:
            detail["personalization"] = dict(self.personalization)
        return {
            "card_id": self.card_id,
            "topic_id": self.topic_id,
            "topic_name": self.topic_name,
            "mode": self.mode,
            "stage": self.stage,
            "eyebrow": self.eyebrow,
            "title": self.title,
            "objective": self.objective,
            "visible_body": self.visible_body,
            # Legacy alias used by frontend/assets/session.js today.
            "body": self.visible_body,
            "coach_brief": self.coach_brief,
            "check": dict(self.check) if self.check else None,
            "rubric_signals": list(self.rubric_signals),
            "source_refs": list(self.source_refs),
            "personalization": dict(self.personalization),
            "actions": [dict(action) for action in self.actions],
            "detail": detail,
        }


@dataclass(frozen=True)
class SessionFrame:
    session_id: str
    mode: str
    topic_id: str
    topic_name: str
    kind: str
    card: CoachCard
    coach_text: str
    spoken_script: str = ""
    progress: dict[str, Any] = field(default_factory=dict)
    input: dict[str, Any] = field(default_factory=dict)
    source: dict[str, Any] = field(default_factory=dict)
    unit: dict[str, Any] = field(default_factory=dict)
    check: dict[str, Any] | None = None
    evaluation: dict[str, Any] | None = None
    actions: list[dict[str, Any]] = field(default_factory=list)
    version: int = 2

    def to_dict(self) -> dict[str, Any]:
        card_dict = self.card.to_dict()
        actions = self.actions or card_dict.get("actions") or []
        check = self.check if self.check is not None else card_dict.get("check")
        return {
            "version": self.version,
            "session_id": self.session_id,
            "mode": self.mode,
            "topic_id": self.topic_id,
            "topic_name": self.topic_name,
            "kind": self.kind,
            "card": card_dict,
            "coach_text": self.coach_text,
            "spoken_script": self.spoken_script or self.coach_text,
            "progress": dict(self.progress),
            "input": dict(self.input) if self.input else {
                "enabled": True,
                "placeholder": "Type your answer",
            },
            "source": dict(self.source),
            "unit": dict(self.unit),
            "check": dict(check) if check else None,
            "evaluation": dict(self.evaluation) if self.evaluation else None,
            "actions": [dict(action) for action in actions],
        }
