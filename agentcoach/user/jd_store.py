"""JD Store — SQLite storage for parsed job descriptions."""
import json
import sqlite3
import os
from typing import Optional

from agentcoach.user.jd_parser import ParsedJD, Skill


class JDStore:
    def __init__(self, db_path: str = ""):
        if not db_path:
            db_path = os.path.expanduser("~/.agentcoach/jd.db")
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS jds (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                company TEXT,
                role_title TEXT,
                level TEXT,
                team TEXT,
                data TEXT NOT NULL,
                is_active INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()

    def save_jd(self, user_id: str, jd: ParsedJD) -> int:
        conn = sqlite3.connect(self.db_path)
        # Deactivate all existing
        conn.execute("UPDATE jds SET is_active = 0 WHERE user_id = ?", (user_id,))
        # Save new as active
        data = json.dumps({
            "required_skills": [
                {
                    "name": s.name,
                    "priority": s.priority,
                    "category": s.category,
                    "mapped_topics": s.mapped_topics,
                }
                for s in jd.required_skills
            ],
            "preferred_skills": [
                {
                    "name": s.name,
                    "priority": s.priority,
                    "category": s.category,
                    "mapped_topics": s.mapped_topics,
                }
                for s in jd.preferred_skills
            ],
            "key_responsibilities": jd.key_responsibilities,
            "inferred_interview_topics": jd.inferred_interview_topics,
            "leadership_signals": jd.leadership_signals,
            "years_experience": jd.years_experience,
            "education": jd.education,
            "raw_text": jd.raw_text[:5000],
        }, ensure_ascii=False)
        cursor = conn.execute(
            "INSERT INTO jds (user_id, company, role_title, level, team, data, is_active) VALUES (?, ?, ?, ?, ?, ?, 1)",
            (user_id, jd.company, jd.role_title, jd.level, jd.team, data),
        )
        jd_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return jd_id

    def get_active_jd(self, user_id: str) -> Optional[ParsedJD]:
        conn = sqlite3.connect(self.db_path)
        row = conn.execute(
            "SELECT company, role_title, level, team, data FROM jds WHERE user_id = ? AND is_active = 1 ORDER BY created_at DESC LIMIT 1",
            (user_id,),
        ).fetchone()
        conn.close()
        if not row:
            return None
        data = json.loads(row[4])
        return ParsedJD(
            company=row[0] or "",
            role_title=row[1] or "",
            level=row[2] or "",
            team=row[3] or "",
            required_skills=[Skill(**s) for s in data.get("required_skills", [])],
            preferred_skills=[Skill(**s) for s in data.get("preferred_skills", [])],
            key_responsibilities=data.get("key_responsibilities", []),
            inferred_interview_topics=data.get("inferred_interview_topics", []),
            leadership_signals=data.get("leadership_signals", []),
            years_experience=data.get("years_experience"),
            education=data.get("education"),
            raw_text=data.get("raw_text", ""),
        )

    def list_jds(self, user_id: str) -> list:
        conn = sqlite3.connect(self.db_path)
        rows = conn.execute(
            "SELECT id, company, role_title, level, is_active, created_at FROM jds WHERE user_id = ? ORDER BY created_at DESC",
            (user_id,),
        ).fetchall()
        conn.close()
        return [
            {
                "id": r[0],
                "company": r[1],
                "role_title": r[2],
                "level": r[3],
                "is_active": bool(r[4]),
                "created_at": r[5],
            }
            for r in rows
        ]

    def set_active_jd(self, user_id: str, jd_id: int):
        conn = sqlite3.connect(self.db_path)
        conn.execute("UPDATE jds SET is_active = 0 WHERE user_id = ?", (user_id,))
        conn.execute(
            "UPDATE jds SET is_active = 1 WHERE user_id = ? AND id = ?",
            (user_id, jd_id),
        )
        conn.commit()
        conn.close()

    def delete_jd(self, user_id: str, jd_id: int):
        conn = sqlite3.connect(self.db_path)
        conn.execute(
            "DELETE FROM jds WHERE user_id = ? AND id = ?", (user_id, jd_id)
        )
        conn.commit()
        conn.close()
