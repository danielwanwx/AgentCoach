"""Stub adapters for future external research/tool integrations."""
from __future__ import annotations

from typing import Any

from agentcoach.missions.adapters.base import ResearchAdapter, source_bundle


class StubResearchAdapter(ResearchAdapter):
    def __init__(self, adapter_id: str, label: str, capability: str):
        self.adapter_id = adapter_id
        self.label = label
        self.capability = capability

    def can_handle(self, request: dict[str, Any], topic_sniff: dict[str, Any]) -> bool:
        return True

    def collect(self, request: dict[str, Any], topic_sniff: dict[str, Any]) -> dict[str, Any]:
        return source_bundle(
            adapter_id=self.adapter_id,
            label=self.label,
            status="stub",
            sources=[],
            notes=[f"Capability reserved: {self.capability}. No external fetch is performed in v1."],
        )


def default_stub_adapters() -> list[ResearchAdapter]:
    return [
        StubResearchAdapter("notebooklm", "NotebookLM Artifact Adapter", "generate source-grounded study artifacts"),
        StubResearchAdapter("youtube_transcript", "YouTube Transcript Adapter", "fetch and analyze relevant transcripts"),
        StubResearchAdapter("interview_intel", "Interview Intelligence Adapter", "collect company/interview forum signals"),
        StubResearchAdapter("hot_topics", "Hot Topic Adapter", "score recent role and topic demand"),
        StubResearchAdapter("public_jobs", "Public Jobs Adapter", "extract live role requirements from public job pages"),
    ]
