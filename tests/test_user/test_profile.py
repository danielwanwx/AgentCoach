"""Tests for agentcoach/user/__init__.py"""
import os
import pytest
import tempfile

from agentcoach.user import UserProfile, UserProfileStore


class TestUserProfile:
    """Tests for UserProfile dataclass."""

    def test_default_profile(self):
        """A default profile has empty fields."""
        p = UserProfile()
        assert p.name == ""
        assert p.target_companies == []
        assert p.years_experience == 0


class TestUserProfileStore:
    """Tests for SQLite-backed profile store."""

    def test_create_and_save_profile(self):
        """Saving a profile creates a DB entry that can be loaded back."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = os.path.join(tmpdir, "user.db")
            store = UserProfileStore(db_path=db_path)
            profile = UserProfile(
                name="Alice",
                target_companies=["Google", "Meta"],
                target_levels={"Google": "L5", "Meta": "E5"},
                current_role="SWE",
                years_experience=5,
                strongest_areas=["algorithms"],
                weakest_areas=["system_design"],
                interview_date="2026-04-15",
            )

            store.save("alice-01", profile)

            loaded = store.load("alice-01")
            assert loaded is not None
            assert loaded.name == "Alice"
            assert loaded.target_companies == ["Google", "Meta"]
            assert loaded.target_levels == {"Google": "L5", "Meta": "E5"}
            assert loaded.years_experience == 5

    def test_load_profile(self):
        """Loading a previously saved profile returns the same data."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = os.path.join(tmpdir, "user.db")
            store = UserProfileStore(db_path=db_path)
            profile = UserProfile(name="Bob", current_role="ML Engineer")

            store.save("bob-01", profile)
            loaded = store.load("bob-01")

            assert loaded.name == "Bob"
            assert loaded.current_role == "ML Engineer"

    def test_load_nonexistent_returns_none(self):
        """Loading a user_id that was never saved returns None."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = os.path.join(tmpdir, "user.db")
            store = UserProfileStore(db_path=db_path)

            result = store.load("no-such-user")

            assert result is None

    def test_format_for_prompt_with_full_profile(self):
        """format_for_prompt with a complete profile includes all sections."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = os.path.join(tmpdir, "user.db")
            store = UserProfileStore(db_path=db_path)
            profile = UserProfile(
                name="Charlie",
                target_companies=["Google"],
                target_levels={"Google": "L5"},
                current_role="Backend Engineer",
                years_experience=4,
                weakest_areas=["system_design", "behavioral"],
                interview_date="2026-05-01",
            )
            store.save("charlie", profile)

            result = store.format_for_prompt("charlie")

            assert "Charlie" in result
            assert "Backend Engineer" in result
            assert "4y exp" in result
            assert "Google (L5)" in result
            assert "system_design" in result
            assert "2026-05-01" in result

    def test_format_for_prompt_empty_profile(self):
        """format_for_prompt with a nonexistent user returns empty string."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = os.path.join(tmpdir, "user.db")
            store = UserProfileStore(db_path=db_path)

            result = store.format_for_prompt("nobody")

            assert result == ""

    def test_save_overwrites_existing(self):
        """Saving the same user_id again overwrites the previous data."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = os.path.join(tmpdir, "user.db")
            store = UserProfileStore(db_path=db_path)

            store.save("u1", UserProfile(name="Old"))
            store.save("u1", UserProfile(name="New"))

            loaded = store.load("u1")
            assert loaded.name == "New"
