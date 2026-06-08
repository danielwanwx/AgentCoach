"""SQLite mission store for diagnostic-first coach harnesses."""
from __future__ import annotations

import json
import os
import sqlite3
from datetime import datetime
from typing import Any


JSON_COLUMNS = {
    "request_json": "request",
    "topic_sniff_json": "topic_sniff",
    "diagnostic_probe_json": "diagnostic_probe",
    "learner_diagnosis_json": "learner_diagnosis",
    "source_manifest_json": "source_manifest",
    "role_profile_json": "role_profile",
    "harness_plan_json": "harness_plan",
    "next_action_json": "next_action",
}


class MissionStore:
    def __init__(self, db_path: str = ""):
        if not db_path:
            db_path = os.path.expanduser("~/.agentcoach/missions.db")
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db_path = db_path
        self._init_db()

    def _init_db(self) -> None:
        conn = sqlite3.connect(self.db_path)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS missions (
                mission_id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                status TEXT NOT NULL,
                request_json TEXT NOT NULL,
                topic_sniff_json TEXT,
                diagnostic_probe_json TEXT,
                learner_diagnosis_json TEXT,
                source_manifest_json TEXT,
                role_profile_json TEXT,
                harness_plan_json TEXT,
                next_action_json TEXT,
                error TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS evidence_events (
                event_id TEXT PRIMARY KEY,
                mission_id TEXT NOT NULL,
                user_id TEXT NOT NULL,
                event_json TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()

    def create(self, *, mission_id: str, user_id: str, request: dict[str, Any]) -> dict[str, Any]:
        now = datetime.utcnow().isoformat()
        conn = sqlite3.connect(self.db_path)
        conn.execute(
            "INSERT INTO missions "
            "(mission_id, user_id, status, request_json, created_at, updated_at) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (mission_id, user_id, "created", _dump(request), now, now),
        )
        conn.commit()
        conn.close()
        return self.get(mission_id) or {}

    def update(self, mission_id: str, **fields: Any) -> dict[str, Any]:
        if not fields:
            return self.get(mission_id) or {}
        assignments = []
        params: list[Any] = []
        for key, value in fields.items():
            if key in JSON_COLUMNS.values():
                column = next(c for c, public in JSON_COLUMNS.items() if public == key)
                assignments.append(f"{column} = ?")
                params.append(_dump(value))
            elif key in {"status", "error"}:
                assignments.append(f"{key} = ?")
                params.append(str(value or ""))
            else:
                continue
        assignments.append("updated_at = ?")
        params.append(datetime.utcnow().isoformat())
        params.append(mission_id)
        conn = sqlite3.connect(self.db_path)
        conn.execute(f"UPDATE missions SET {', '.join(assignments)} WHERE mission_id = ?", params)
        conn.commit()
        conn.close()
        return self.get(mission_id) or {}

    def get(self, mission_id: str) -> dict[str, Any] | None:
        conn = sqlite3.connect(self.db_path)
        row = conn.execute(
            "SELECT mission_id, user_id, status, request_json, topic_sniff_json, "
            "diagnostic_probe_json, learner_diagnosis_json, source_manifest_json, "
            "role_profile_json, harness_plan_json, next_action_json, error, "
            "created_at, updated_at FROM missions WHERE mission_id = ?",
            (mission_id,),
        ).fetchone()
        conn.close()
        if not row:
            return None
        record = {
            "mission_id": row[0],
            "user_id": row[1],
            "status": row[2],
            "error": row[11],
            "created_at": row[12],
            "updated_at": row[13],
        }
        for idx, column in enumerate(JSON_COLUMNS, start=3):
            record[JSON_COLUMNS[column]] = _load(row[idx])
        return record

    def add_evidence(self, event: dict[str, Any]) -> None:
        conn = sqlite3.connect(self.db_path)
        conn.execute(
            "INSERT OR REPLACE INTO evidence_events "
            "(event_id, mission_id, user_id, event_json, created_at) VALUES (?, ?, ?, ?, ?)",
            (
                event["event_id"],
                event["mission_id"],
                event["user_id"],
                _dump(event),
                event["created_at"],
            ),
        )
        conn.commit()
        conn.close()

    def list_evidence(self, mission_id: str) -> list[dict[str, Any]]:
        conn = sqlite3.connect(self.db_path)
        rows = conn.execute(
            "SELECT event_json FROM evidence_events WHERE mission_id = ? ORDER BY created_at, event_id",
            (mission_id,),
        ).fetchall()
        conn.close()
        return [_load(row[0]) for row in rows]


def _dump(value: Any) -> str:
    return json.dumps(value or {}, ensure_ascii=False, sort_keys=True)


def _load(value: str | None) -> Any:
    if not value:
        return {}
    try:
        return json.loads(value)
    except (TypeError, ValueError):
        return {}
