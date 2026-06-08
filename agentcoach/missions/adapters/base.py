"""Research adapter contracts for missions."""
from __future__ import annotations

from typing import Any


class ResearchAdapter:
    adapter_id = "base"
    label = "Base Adapter"

    def can_handle(self, request: dict[str, Any], topic_sniff: dict[str, Any]) -> bool:
        return False

    def collect(self, request: dict[str, Any], topic_sniff: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError


def source_bundle(
    *,
    adapter_id: str,
    label: str,
    status: str,
    sources: list[dict[str, Any]] | None = None,
    notes: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "adapter_id": adapter_id,
        "label": label,
        "status": status,
        "sources": list(sources or []),
        "notes": list(notes or []),
    }
