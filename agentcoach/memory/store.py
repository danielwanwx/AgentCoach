"""Coach memory layer — lightweight SQLite FTS5 for profile/JD/feedback storage."""
import sqlite3
import os


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

    def search(self, query: str, limit: int = 5) -> list:
        # Use prefix queries (word*) joined with OR for flexible matching
        tokens = query.strip().split()
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
        for category, label in [("profile", "User Profile"), ("jd", "Target JD"), ("feedback", "Past Feedback")]:
            rows = conn.execute(
                "SELECT content FROM memories WHERE category = ? ORDER BY created_at DESC LIMIT 5",
                (category,)
            ).fetchall()
            if rows:
                items = "\n".join(f"- {r[0]}" for r in rows)
                sections.append(f"### {label}\n{items}")
        conn.close()
        return "\n\n".join(sections)
