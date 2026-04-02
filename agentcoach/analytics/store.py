"""Analytics store — tracks per-topic mastery scores with time decay."""
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
