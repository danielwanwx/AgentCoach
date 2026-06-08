"""Shared mission constants and status helpers."""
from __future__ import annotations


MISSION_STATUSES = {
    "created",
    "diagnosing",
    "planning",
    "training",
    "reviewing",
    "complete",
    "failed",
}


def normalize_status(value: str) -> str:
    value = (value or "").strip().lower()
    return value if value in MISSION_STATUSES else "created"
