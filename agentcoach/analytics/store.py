"""Analytics store — tracks per-topic mastery scores with time decay."""
import json as _json
import sqlite3
import os
from datetime import datetime
from typing import Optional


class AnalyticsStore:
    def __init__(self, db_path: str = ""):
        if not db_path:
            db_path = os.path.expanduser("~/.agentcoach/analytics.db")
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS score_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                topic_id TEXT NOT NULL,
                score_delta INTEGER NOT NULL,
                mode TEXT NOT NULL,
                evidence TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS skill_assessments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                topic_id TEXT NOT NULL,
                domain TEXT NOT NULL,
                mode TEXT NOT NULL,
                session_id TEXT,
                overall_score REAL NOT NULL,
                dimensions_json TEXT NOT NULL,
                strengths_json TEXT,
                areas_json TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_assess_user_topic "
            "ON skill_assessments(user_id, topic_id)"
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_assess_user_domain "
            "ON skill_assessments(user_id, domain)"
        )
        conn.commit()
        conn.close()

    def record_score(self, user_id: str, topic_id: str, score_delta: int,
                     mode: str, evidence: str = ""):
        conn = sqlite3.connect(self.db_path)
        conn.execute(
            "INSERT INTO score_events (user_id, topic_id, score_delta, mode, evidence) VALUES (?, ?, ?, ?, ?)",
            (user_id, topic_id, score_delta, mode, evidence),
        )
        conn.commit()
        conn.close()

    # Half-life for mastery decay (days) and mode score weights
    HALF_LIFE_DAYS = 30.0
    MODE_WEIGHTS = {"mock": 1.5, "reinforce": 1.0, "learn": 0.7, "quiz": 1.0}

    @staticmethod
    def _compute_decayed_mastery(rows) -> int:
        """Compute mastery from score events with exponential time decay and mode weighting.

        Each row is (score_delta, mode, created_at_str).
        """
        if not rows:
            return 0
        now = datetime.utcnow()
        total = 0.0
        for score_delta, mode, created_at_str in rows:
            try:
                created_at = datetime.fromisoformat(created_at_str)
            except (ValueError, TypeError):
                created_at = now  # fallback: treat unparseable as "just now"
            days_ago = max((now - created_at).total_seconds() / 86400.0, 0.0)
            decay = 0.5 ** (days_ago / AnalyticsStore.HALF_LIFE_DAYS)
            weight = AnalyticsStore.MODE_WEIGHTS.get(mode, 1.0)
            total += score_delta * weight * decay
        return max(0, min(100, int(total)))

    def get_mastery(self, user_id: str, topic_id: str) -> int:
        conn = sqlite3.connect(self.db_path)
        rows = conn.execute(
            "SELECT score_delta, mode, created_at FROM score_events "
            "WHERE user_id = ? AND topic_id = ?",
            (user_id, topic_id),
        ).fetchall()
        conn.close()
        return self._compute_decayed_mastery(rows)

    def get_progress(self, user_id: str, domain: str) -> list:
        conn = sqlite3.connect(self.db_path)
        rows = conn.execute(
            "SELECT topic_id, score_delta, mode, created_at FROM score_events "
            "WHERE user_id = ? AND topic_id LIKE ?",
            (user_id, f"{domain}.%"),
        ).fetchall()
        conn.close()
        # Group by topic_id and compute decayed mastery per topic
        from collections import defaultdict
        grouped = defaultdict(list)
        for topic_id_val, score_delta, mode, created_at in rows:
            grouped[topic_id_val].append((score_delta, mode, created_at))
        return [
            {"topic_id": tid, "mastery": self._compute_decayed_mastery(events)}
            for tid, events in grouped.items()
        ]

    def get_last_practiced(self, user_id: str, topic_id: str) -> Optional[str]:
        """Return the timestamp of the most recent score event, or None."""
        conn = sqlite3.connect(self.db_path)
        row = conn.execute(
            "SELECT MAX(created_at) FROM score_events WHERE user_id = ? AND topic_id = ?",
            (user_id, topic_id),
        ).fetchone()
        conn.close()
        return row[0] if row and row[0] else None

    def get_all_mastery(self, user_id: str) -> dict:
        """Return mastery for all topics the user has practiced."""
        conn = sqlite3.connect(self.db_path)
        rows = conn.execute(
            "SELECT DISTINCT topic_id FROM score_events WHERE user_id = ?",
            (user_id,),
        ).fetchall()
        conn.close()
        result = {}
        for (tid,) in rows:
            result[tid] = self.get_mastery(user_id, tid)
        return result

    def get_topic_summary(self, user_id: str, topic_id: str) -> dict:
        """Get summary for a topic: mastery, last score, last practiced."""
        conn = sqlite3.connect(self.db_path)
        rows = conn.execute(
            "SELECT score_delta, mode, evidence, created_at FROM score_events "
            "WHERE user_id = ? AND topic_id = ? ORDER BY created_at DESC LIMIT 1",
            (user_id, topic_id),
        ).fetchall()
        conn.close()
        mastery = self.get_mastery(user_id, topic_id)
        if rows:
            last = rows[0]
            return {
                "mastery": mastery,
                "last_score_delta": last[0],
                "last_mode": last[1],
                "last_evidence": last[2],
                "last_practiced": last[3],
            }
        return {"mastery": mastery}

    def get_history(self, user_id: str, topic_id: str, limit: int = 10) -> list:
        conn = sqlite3.connect(self.db_path)
        rows = conn.execute(
            "SELECT score_delta, mode, evidence, created_at FROM score_events "
            "WHERE user_id = ? AND topic_id = ? ORDER BY created_at DESC LIMIT ?",
            (user_id, topic_id, limit),
        ).fetchall()
        conn.close()
        return [
            {"score_delta": r[0], "mode": r[1], "evidence": r[2], "timestamp": r[3]}
            for r in rows
        ]

    # -------- Skill assessments (per-session, dimension-level) -------- #

    def record_assessment(
        self,
        user_id: str,
        topic_id: str,
        domain: str,
        mode: str,
        overall_score: float,
        dimensions: list,
        strengths: Optional[list] = None,
        areas_to_improve: Optional[list] = None,
        session_id: Optional[str] = None,
    ) -> int:
        """Persist a structured skill assessment for one session.

        `dimensions` is a list of {name, score, evidence} dicts (already
        validated upstream by the scorer). Returns the new row id.
        """
        conn = sqlite3.connect(self.db_path)
        cur = conn.execute(
            "INSERT INTO skill_assessments "
            "(user_id, topic_id, domain, mode, session_id, overall_score, "
            " dimensions_json, strengths_json, areas_json) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                user_id,
                topic_id,
                domain,
                mode,
                session_id,
                float(overall_score),
                _json.dumps(dimensions or []),
                _json.dumps(strengths or []),
                _json.dumps(areas_to_improve or []),
            ),
        )
        new_id = cur.lastrowid
        conn.commit()
        conn.close()
        return new_id

    def get_assessments(
        self,
        user_id: str,
        domain: Optional[str] = None,
        topic_id: Optional[str] = None,
        limit: int = 50,
    ) -> list:
        """Return assessments (newest first) for the user, optionally filtered."""
        q = (
            "SELECT id, user_id, topic_id, domain, mode, session_id, "
            "overall_score, dimensions_json, strengths_json, areas_json, "
            "created_at FROM skill_assessments WHERE user_id = ?"
        )
        params: list = [user_id]
        if domain:
            q += " AND domain = ?"
            params.append(domain)
        if topic_id:
            q += " AND topic_id = ?"
            params.append(topic_id)
        q += " ORDER BY created_at DESC, id DESC LIMIT ?"
        params.append(limit)
        conn = sqlite3.connect(self.db_path)
        rows = conn.execute(q, params).fetchall()
        conn.close()
        results = []
        for r in rows:
            try:
                dims = _json.loads(r[7]) if r[7] else []
            except (ValueError, TypeError):
                dims = []
            try:
                strengths = _json.loads(r[8]) if r[8] else []
            except (ValueError, TypeError):
                strengths = []
            try:
                areas = _json.loads(r[9]) if r[9] else []
            except (ValueError, TypeError):
                areas = []
            results.append({
                "id": r[0],
                "user_id": r[1],
                "topic_id": r[2],
                "domain": r[3],
                "mode": r[4],
                "session_id": r[5],
                "overall_score": r[6],
                "dimensions": dims,
                "strengths": strengths,
                "areas_to_improve": areas,
                "created_at": r[10],
            })
        return results

    def get_skill_trajectory(
        self,
        user_id: str,
        domain: str,
        limit: int = 20,
    ) -> dict:
        """Build a per-dimension trajectory for `domain`.

        Returns {dim_name: [{score, created_at, topic_id, mode}, ...]} oldest→newest.
        Useful for plotting growth curves.
        """
        rows = self.get_assessments(user_id, domain=domain, limit=limit)
        rows.reverse()  # oldest first for nicer sparklines
        traj: dict = {}
        for r in rows:
            for d in r.get("dimensions", []):
                name = d.get("name")
                if not name:
                    continue
                try:
                    score = float(d.get("score"))
                except (TypeError, ValueError):
                    continue
                traj.setdefault(name, []).append({
                    "score": score,
                    "created_at": r["created_at"],
                    "topic_id": r["topic_id"],
                    "mode": r["mode"],
                })
        return traj
