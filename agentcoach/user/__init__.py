"""User profile — stores target companies, levels, and preferences."""
import json
import os
import sqlite3
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class UserProfile:
    name: str = ""
    target_companies: list = field(default_factory=list)     # ["Google", "Meta"]
    target_levels: dict = field(default_factory=dict)         # {"Google": "L5"}
    current_role: str = ""
    years_experience: int = 0
    strongest_areas: list = field(default_factory=list)
    weakest_areas: list = field(default_factory=list)
    interview_date: str = ""   # ISO date string


class UserProfileStore:
    """SQLite-backed user profile storage."""

    def __init__(self, db_path: str = ""):
        if not db_path:
            db_path = os.path.expanduser("~/.agentcoach/user.db")
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS user_profiles (
                user_id TEXT PRIMARY KEY,
                data TEXT NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()

    def save(self, user_id: str, profile: UserProfile):
        conn = sqlite3.connect(self.db_path)
        data = json.dumps({
            "name": profile.name,
            "target_companies": profile.target_companies,
            "target_levels": profile.target_levels,
            "current_role": profile.current_role,
            "years_experience": profile.years_experience,
            "strongest_areas": profile.strongest_areas,
            "weakest_areas": profile.weakest_areas,
            "interview_date": profile.interview_date,
        })
        conn.execute(
            "INSERT OR REPLACE INTO user_profiles (user_id, data) VALUES (?, ?)",
            (user_id, data),
        )
        conn.commit()
        conn.close()

    def load(self, user_id: str) -> Optional[UserProfile]:
        conn = sqlite3.connect(self.db_path)
        row = conn.execute(
            "SELECT data FROM user_profiles WHERE user_id = ?", (user_id,)
        ).fetchone()
        conn.close()
        if not row:
            return None
        data = json.loads(row[0])
        return UserProfile(**data)

    def format_for_prompt(self, user_id: str) -> str:
        """Format user profile as context for Coach prompt."""
        profile = self.load(user_id)
        if not profile:
            return ""
        parts = []
        if profile.name:
            parts.append(f"Name: {profile.name}")
        if profile.current_role:
            parts.append(f"Current role: {profile.current_role} ({profile.years_experience}y exp)")
        if profile.target_companies:
            targets = ", ".join(
                f"{c} ({profile.target_levels.get(c, '?')})" for c in profile.target_companies
            )
            parts.append(f"Targeting: {targets}")
        if profile.weakest_areas:
            parts.append(f"Weak areas: {', '.join(profile.weakest_areas)}")
        if profile.interview_date:
            parts.append(f"Interview date: {profile.interview_date}")
        return "\n".join(parts)
