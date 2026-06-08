"""Diagnostic-first mission orchestrator."""
from __future__ import annotations

import uuid
from pathlib import Path
from typing import Any

from agentcoach.diagnostics import (
    evaluate_diagnostic_answers,
    generate_diagnostic_probe,
    sniff_topic,
)
from agentcoach.harness.evidence import build_evidence_event
from agentcoach.harness.planner import build_harness_plan
from agentcoach.missions.adapters.local_kb import LocalKBAdapter
from agentcoach.missions.adapters.stubs import default_stub_adapters
from agentcoach.missions.store import MissionStore
from agentcoach.roles import get_role_profile, map_transition_gaps, normalize_role_family


class MissionOrchestrator:
    def __init__(
        self,
        *,
        store: MissionStore,
        project_root: Path,
        syllabus=None,
        adapters: list | None = None,
    ):
        self.store = store
        self.project_root = project_root
        self.syllabus = syllabus
        self.adapters = adapters or [LocalKBAdapter(project_root, syllabus=syllabus)] + default_stub_adapters()

    def create_mission(self, request: dict[str, Any]) -> dict[str, Any]:
        user_id = (request.get("user_id") or "web-guest").strip() or "web-guest"
        mission_id = uuid.uuid4().hex[:12]
        target_role = normalize_role_family(request.get("target_role") or "")
        input_text = (request.get("input_text") or request.get("topic") or "").strip()
        if not input_text:
            input_text = "AI Engineer interview readiness"
        normalized_request = dict(request)
        normalized_request.update({
            "user_id": user_id,
            "input_text": input_text,
            "target_role": target_role,
        })
        self.store.create(mission_id=mission_id, user_id=user_id, request=normalized_request)
        topic_sniff = sniff_topic(
            input_text,
            target_role=target_role,
            background=normalized_request.get("background", ""),
        )
        probe = generate_diagnostic_probe(topic_sniff, target_role=target_role)
        return self.store.update(
            mission_id,
            status="diagnosing",
            topic_sniff=topic_sniff,
            diagnostic_probe=probe,
        )

    def submit_diagnostic(self, mission_id: str, answers: list[dict[str, Any]]) -> dict[str, Any]:
        mission = self.store.get(mission_id)
        if not mission:
            return {"error": "unknown mission"}
        request = mission.get("request") or {}
        topic_sniff = mission.get("topic_sniff") or {}
        probe = mission.get("diagnostic_probe") or {}
        target_role = normalize_role_family(request.get("target_role") or topic_sniff.get("role_hint") or "")
        diagnosis = evaluate_diagnostic_answers(
            probe,
            answers,
            topic_sniff=topic_sniff,
            target_role=target_role,
            background=request.get("background", ""),
        )
        role_profile = get_role_profile(target_role, company=request.get("target_company") or "")
        transition_gaps = map_transition_gaps(
            learner_diagnosis=diagnosis,
            role_profile=role_profile,
            background=request.get("background", ""),
        )
        source_manifest = self._build_source_manifest(request, topic_sniff)
        harness_plan = build_harness_plan(
            mission_id=mission_id,
            topic_sniff=topic_sniff,
            learner_diagnosis=diagnosis,
            role_profile=role_profile,
            transition_gaps=transition_gaps,
            source_manifest=source_manifest,
        )
        event = build_evidence_event(
            mission_id=mission_id,
            user_id=mission.get("user_id", "web-guest"),
            topic_id=topic_sniff.get("topic_id", ""),
            role_family=target_role,
            stage="diagnose",
            input_text=" | ".join(str(a.get("answer", "")) for a in answers),
            score=float(diagnosis.get("score", 0)),
            gap_signals=diagnosis.get("gap_signals", []),
            strength_signals=diagnosis.get("strength_signals", []),
            source_refs=source_manifest.get("source_refs", []),
        )
        self.store.add_evidence(event)
        updated = self.store.update(
            mission_id,
            status="training",
            learner_diagnosis=diagnosis,
            source_manifest=source_manifest,
            role_profile=role_profile,
            harness_plan=harness_plan,
            next_action=harness_plan.get("next_action", {}),
        )
        updated["transition_gaps"] = transition_gaps
        updated["evidence"] = self.store.list_evidence(mission_id)
        return updated

    def get_mission(self, mission_id: str) -> dict[str, Any]:
        mission = self.store.get(mission_id)
        if not mission:
            return {"error": "unknown mission"}
        mission["evidence"] = self.store.list_evidence(mission_id)
        return mission

    def record_session_result(self, mission_id: str, assessment: dict[str, Any]) -> dict[str, Any]:
        mission = self.store.get(mission_id)
        if not mission:
            return {"error": "unknown mission"}
        request = mission.get("request") or {}
        topic_sniff = mission.get("topic_sniff") or {}
        diagnosis = mission.get("learner_diagnosis") or {}
        role_profile = mission.get("role_profile") or get_role_profile(
            request.get("target_role") or topic_sniff.get("role_hint") or "",
            company=request.get("target_company") or "",
        )
        target_role = normalize_role_family(role_profile.get("role_family") or request.get("target_role") or "")
        overall = float(assessment.get("overall_score") or 0)
        weak_dimension = _weakest_dimension(assessment.get("dimensions") or [])
        event = build_evidence_event(
            mission_id=mission_id,
            user_id=mission.get("user_id", "web-guest"),
            topic_id=topic_sniff.get("topic_id") or assessment.get("topic_id", ""),
            role_family=target_role,
            stage=_stage_from_mode(assessment.get("mode", "")),
            input_text=assessment.get("summary") or assessment.get("evidence") or "",
            score=overall / 5.0 if overall > 1 else overall,
            gap_signals=[weak_dimension] if weak_dimension else diagnosis.get("gap_signals", []),
            strength_signals=assessment.get("strengths", []),
            source_refs=(mission.get("source_manifest") or {}).get("source_refs", []),
        )
        event["session_id"] = assessment.get("session_id")
        event["assessment"] = {
            "overall_score": assessment.get("overall_score"),
            "dimensions": assessment.get("dimensions", []),
            "areas_to_improve": assessment.get("areas_to_improve", []),
        }
        self.store.add_evidence(event)

        next_action = _next_action_after_session(
            topic_sniff=topic_sniff,
            diagnosis=diagnosis,
            role_profile=role_profile,
            assessment=assessment,
            weak_dimension=weak_dimension,
            source_manifest=mission.get("source_manifest") or {},
        )
        harness_plan = dict(mission.get("harness_plan") or {})
        harness_plan["last_assessment"] = event["assessment"]
        harness_plan["next_action"] = next_action
        updated = self.store.update(
            mission_id,
            status="training",
            harness_plan=harness_plan,
            next_action=next_action,
        )
        updated["evidence"] = self.store.list_evidence(mission_id)
        return updated

    def _build_source_manifest(self, request: dict[str, Any], topic_sniff: dict[str, Any]) -> dict[str, Any]:
        bundles = []
        source_refs = []
        for adapter in self.adapters:
            if not adapter.can_handle(request, topic_sniff):
                continue
            bundle = adapter.collect(request, topic_sniff)
            bundles.append(bundle)
            for source in bundle.get("sources") or []:
                source_refs.append({
                    "label": source.get("title") or bundle.get("label"),
                    "type": source.get("type", "source"),
                    "url": source.get("url"),
                    "source": source.get("source"),
                    "adapter_id": bundle.get("adapter_id"),
                })
        return {
            "manifest_id": uuid.uuid4().hex[:12],
            "topic_id": topic_sniff.get("topic_id"),
            "topic_name": topic_sniff.get("topic_name"),
            "bundles": bundles,
            "source_refs": source_refs,
            "adapter_status": {
                bundle.get("adapter_id"): bundle.get("status")
                for bundle in bundles
            },
        }


def _stage_from_mode(mode: str) -> str:
    if mode == "learn":
        return "learn"
    if mode == "reinforce":
        return "drill"
    if mode.startswith("mock"):
        return "mock"
    return "retest"


def _weakest_dimension(dimensions: list[dict[str, Any]]) -> str:
    scored = []
    for dim in dimensions or []:
        try:
            scored.append((float(dim.get("score")), dim.get("name", "")))
        except (TypeError, ValueError):
            continue
    if not scored:
        return ""
    scored.sort(key=lambda item: item[0])
    return scored[0][1] or ""


def _next_action_after_session(
    *,
    topic_sniff: dict[str, Any],
    diagnosis: dict[str, Any],
    role_profile: dict[str, Any],
    assessment: dict[str, Any],
    weak_dimension: str,
    source_manifest: dict[str, Any],
) -> dict[str, Any]:
    current_mode = assessment.get("mode", "")
    topic_name = topic_sniff.get("topic_name") or assessment.get("topic_name") or "Topic"
    role_label = role_profile.get("label", "AI Engineer")
    focus = weak_dimension or (diagnosis.get("gap_signals") or ["transfer"])[0]
    if current_mode == "learn":
        mode = "reinforce"
        stage_text = "closed-book recall and targeted drill"
    elif current_mode == "reinforce" and topic_sniff.get("domain") == "system_design":
        mode = "mock_system_design"
        stage_text = "pressure transfer in a system design prompt"
    elif current_mode.startswith("mock"):
        mode = "reinforce"
        stage_text = "repair the weakest interview dimension"
    else:
        mode = "reinforce"
        stage_text = "role-transfer drill"
    coach_brief = (
        f"Continue the same mission on {topic_name} for {role_label}. "
        f"The last session's weakest signal was {focus or 'transfer'}. "
        f"Run {stage_text}; keep the answer tied to AI-native or customer-facing constraints."
    )
    return {
        "topic_id": topic_sniff.get("topic_id") or assessment.get("topic_id"),
        "topic_name": topic_name,
        "domain": topic_sniff.get("domain") or assessment.get("domain") or "system_design",
        "mode": mode,
        "focus_dimension": focus or "transfer",
        "coach_brief": coach_brief,
        "reason": f"Continue {topic_name} for {role_label}: {stage_text}.",
        "source_manifest_id": source_manifest.get("manifest_id"),
    }
