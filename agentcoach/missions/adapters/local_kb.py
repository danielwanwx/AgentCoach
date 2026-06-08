"""Local KB research adapter for missions."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from agentcoach.kb.hellointerview import load_hellointerview_chunks
from agentcoach.missions.adapters.base import ResearchAdapter, source_bundle


class LocalKBAdapter(ResearchAdapter):
    adapter_id = "local_kb"
    label = "Local Knowledge Base"

    def __init__(self, project_root: Path, syllabus=None):
        self.project_root = project_root
        self.syllabus = syllabus

    def can_handle(self, request: dict[str, Any], topic_sniff: dict[str, Any]) -> bool:
        return True

    def collect(self, request: dict[str, Any], topic_sniff: dict[str, Any]) -> dict[str, Any]:
        topic_id = topic_sniff.get("topic_id", "")
        topic_name = topic_sniff.get("topic_name", "")
        domain = topic_sniff.get("domain", "system_design")
        kb_root = self.project_root / "kb" / "hellointerview"
        chunks = load_hellointerview_chunks(kb_root, topic_id, topic_name, domain, max_files=4, max_chunks=8)
        sources = []
        for idx, chunk in enumerate(chunks, start=1):
            sources.append({
                "source_id": f"local_kb:{idx}",
                "title": chunk.get("section") or topic_name,
                "type": "kb_chunk",
                "source": chunk.get("source", "local"),
                "category": chunk.get("category", domain),
                "preview": (chunk.get("content") or "")[:360],
                "url": None,
            })
        for resource in _resources_for_topic(self.syllabus, topic_id):
            sources.append({
                "source_id": f"syllabus:{len(sources) + 1}",
                "title": resource.get("title", "Resource"),
                "type": resource.get("type", "resource"),
                "source": "syllabus",
                "category": domain,
                "preview": "",
                "url": resource.get("url"),
            })
        status = "ready" if sources else "empty"
        notes = [] if sources else ["No local source matched; downstream planner should use role taxonomy fallback."]
        return source_bundle(
            adapter_id=self.adapter_id,
            label=self.label,
            status=status,
            sources=sources,
            notes=notes,
        )


def _resources_for_topic(syllabus, topic_id: str) -> list[dict[str, Any]]:
    if syllabus is None:
        return []
    try:
        return list(syllabus.get_resources(topic_id) or [])
    except Exception:
        return []
