"""Analytics store — tracks per-topic mastery scores."""
import sqlite3
import os


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

    def get_mastery(self, user_id: str, topic_id: str) -> int:
        conn = sqlite3.connect(self.db_path)
        row = conn.execute(
            "SELECT COALESCE(SUM(score_delta), 0) FROM score_events WHERE user_id = ? AND topic_id = ?",
            (user_id, topic_id),
        ).fetchone()
        conn.close()
        raw = row[0] if row else 0
        return max(0, min(100, raw))

    def get_progress(self, user_id: str, domain: str) -> list:
        conn = sqlite3.connect(self.db_path)
        rows = conn.execute(
            "SELECT topic_id, SUM(score_delta) FROM score_events "
            "WHERE user_id = ? AND topic_id LIKE ? GROUP BY topic_id",
            (user_id, f"{domain}.%"),
        ).fetchall()
        conn.close()
        return [
            {"topic_id": r[0], "mastery": max(0, min(100, r[1]))}
            for r in rows
        ]

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
