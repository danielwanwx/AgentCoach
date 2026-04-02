"""Coach memory layer — lightweight SQLite FTS5 for profile/JD/feedback/transcript storage."""
import json
import sqlite3
import os
from datetime import datetime


class CoachMemory:
    def __init__(self, db_path: str = ""):
        if not db_path:
            db_path = os.path.expanduser("~/.agentcoach/memory.db")
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS memories_fts
            USING fts5(content, category, content=memories, content_rowid=id)
        """)
        conn.execute("""
            CREATE TRIGGER IF NOT EXISTS memories_ai AFTER INSERT ON memories BEGIN
                INSERT INTO memories_fts(rowid, content, category)
                VALUES (new.id, new.content, new.category);
            END
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS session_transcripts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                topic_id TEXT,
                topic_name TEXT,
                mode TEXT NOT NULL,
                transcript TEXT NOT NULL,
                score_summary TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()

    def _save(self, category: str, content: str):
        conn = sqlite3.connect(self.db_path)
        conn.execute("INSERT INTO memories (category, content) VALUES (?, ?)", (category, content))
        conn.commit()
        conn.close()

    def save_profile(self, content: str):
        self._save("profile", content)

    def save_jd(self, content: str):
        self._save("jd", content)

    def save_feedback(self, content: str):
        self._save("feedback", content)

    def save_learning(self, content: str):
        self._save("learning", content)

    def search(self, query: str, limit: int = 5) -> list:
        # Use prefix queries (word*) joined with OR for flexible matching
        import re as _re
        tokens = _re.findall(r'\w+', query)
        fts_query = " OR ".join(f"{t}*" for t in tokens) if tokens else query
        conn = sqlite3.connect(self.db_path)
        rows = conn.execute(
            "SELECT content FROM memories_fts WHERE memories_fts MATCH ? LIMIT ?",
            (fts_query, limit)
        ).fetchall()
        conn.close()
        return [row[0] for row in rows]

    def get_context(self) -> str:
        """Get all stored memory as formatted context for prompt injection."""
        conn = sqlite3.connect(self.db_path)
        sections = []
        for category, label in [("profile", "User Profile"), ("jd", "Target JD"),
                                ("feedback", "Past Feedback"), ("learning", "Learning History")]:
            rows = conn.execute(
                "SELECT content FROM memories WHERE category = ? ORDER BY created_at DESC LIMIT 5",
                (category,)
            ).fetchall()
            if rows:
                items = "\n".join(f"- {r[0]}" for r in rows)
                sections.append(f"### {label}\n{items}")
        conn.close()
        return "\n\n".join(sections)

    # ── Session transcripts ────────────────────────────────────

    def save_transcript(self, user_id: str, topic_id: str, topic_name: str,
                        mode: str, history: list, scores: list = None):
        """Save complete session transcript for review and ability assessment."""
        # Convert Message objects to dicts
        transcript = []
        for msg in history:
            transcript.append({
                "role": getattr(msg, "role", "unknown"),
                "content": getattr(msg, "content", str(msg)),
            })
        score_summary = json.dumps(scores) if scores else None
        conn = sqlite3.connect(self.db_path)
        conn.execute(
            "INSERT INTO session_transcripts "
            "(user_id, topic_id, topic_name, mode, transcript, score_summary) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (user_id, topic_id, topic_name, mode, json.dumps(transcript, ensure_ascii=False),
             score_summary),
        )
        conn.commit()
        conn.close()

    def get_transcripts(self, user_id: str, topic_id: str = "", limit: int = 10) -> list:
        """Get past session transcripts for review."""
        conn = sqlite3.connect(self.db_path)
        if topic_id:
            rows = conn.execute(
                "SELECT id, topic_id, topic_name, mode, transcript, score_summary, created_at "
                "FROM session_transcripts WHERE user_id = ? AND topic_id = ? "
                "ORDER BY created_at DESC LIMIT ?",
                (user_id, topic_id, limit),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT id, topic_id, topic_name, mode, transcript, score_summary, created_at "
                "FROM session_transcripts WHERE user_id = ? "
                "ORDER BY created_at DESC LIMIT ?",
                (user_id, limit),
            ).fetchall()
        conn.close()
        return [{
            "id": r[0], "topic_id": r[1], "topic_name": r[2], "mode": r[3],
            "transcript": json.loads(r[4]), "scores": json.loads(r[5]) if r[5] else None,
            "timestamp": r[6],
        } for r in rows]
