"""Tests for JD weighting in study plan generation."""
import pytest

from agentcoach.planner import generate_study_plan
from agentcoach.user.jd_parser import ParsedJD, Skill


SAMPLE_TOPICS = [
    {"id": "system_design.caching", "name": "Caching", "difficulty_level": 2},
    {"id": "system_design.sharding", "name": "Sharding", "difficulty_level": 3},
    {"id": "algorithms.arrays_strings", "name": "Arrays & Strings", "difficulty_level": 1},
    {"id": "behavioral.leadership", "name": "Leadership", "difficulty_level": 1},
    {"id": "ai_agent.rag", "name": "RAG Pipeline", "difficulty_level": 2},
]


def _make_jd_with_skills():
    """Create a JD where caching is required and RAG is preferred."""
    return ParsedJD(
        company="TestCo",
        role_title="SWE",
        required_skills=[
            Skill(
                name="Caching",
                priority="must",
                category="system_design",
                mapped_topics=["system_design.caching"],
            ),
        ],
        preferred_skills=[
            Skill(
                name="RAG",
                priority="nice_to_have",
                category="ml",
                mapped_topics=["ai_agent.rag"],
            ),
        ],
    )


class TestJDWeighting:
    def test_required_skill_boosted(self):
        """Topics matching required_skills get higher urgency (2.0x)."""
        mastery = {}  # All zero mastery — same baseline
        plan_no_jd = generate_study_plan(SAMPLE_TOPICS, mastery, days_until_interview=3, sessions_per_day=5)
        plan_with_jd = generate_study_plan(SAMPLE_TOPICS, mastery, days_until_interview=3, sessions_per_day=5, active_jd=_make_jd_with_skills())

        # In the JD plan, caching should be first (highest urgency due to 2x boost)
        day1_topics_jd = [s["topic_id"] for s in plan_with_jd[0]["sessions"]]
        caching_idx = day1_topics_jd.index("system_design.caching")
        # Caching should be in first two positions (boosted)
        assert caching_idx <= 1, f"Caching at index {caching_idx}, expected <= 1"

    def test_preferred_skill_moderately_boosted(self):
        """Topics matching preferred_skills get 1.5x boost, ranked higher than unmatched."""
        mastery = {}
        plan = generate_study_plan(SAMPLE_TOPICS, mastery, days_until_interview=3, sessions_per_day=5, active_jd=_make_jd_with_skills())
        day1_topics = [s["topic_id"] for s in plan[0]["sessions"]]

        rag_idx = day1_topics.index("ai_agent.rag")
        # RAG (preferred, 1.5x) should rank above non-JD topics (0.5x)
        # but below required topics (2.0x)
        # arrays_strings has difficulty 1, so lower base urgency * 0.5
        arrays_idx = day1_topics.index("algorithms.arrays_strings")
        assert rag_idx < arrays_idx, f"RAG at {rag_idx}, arrays at {arrays_idx}"

    def test_non_jd_topics_deprioritized(self):
        """Topics not in JD get 0.5x urgency — appear later."""
        mastery = {}
        plan = generate_study_plan(SAMPLE_TOPICS, mastery, days_until_interview=3, sessions_per_day=5, active_jd=_make_jd_with_skills())
        day1_topics = [s["topic_id"] for s in plan[0]["sessions"]]

        # behavioral.leadership is not in JD — should be deprioritized
        leadership_idx = day1_topics.index("behavioral.leadership")
        caching_idx = day1_topics.index("system_design.caching")
        assert leadership_idx > caching_idx

    def test_no_jd_plan_unchanged(self):
        """Without active_jd, plan generation works as before."""
        mastery = {}
        plan = generate_study_plan(SAMPLE_TOPICS, mastery, days_until_interview=3)
        assert len(plan) == 3
        for day in plan:
            assert "sessions" in day
            for s in day["sessions"]:
                assert "topic_id" in s

    def test_jd_with_empty_skills(self):
        """JD with no skills should behave like no JD (0.5x on everything)."""
        empty_jd = ParsedJD(company="X", role_title="Y")
        mastery = {}
        plan = generate_study_plan(SAMPLE_TOPICS, mastery, days_until_interview=2, active_jd=empty_jd)
        assert len(plan) == 2
        # All topics get 0.5x, so relative order is same as without JD
        # Just verify it doesn't crash
        assert len(plan[0]["sessions"]) >= 1

    def test_jd_weighting_with_mastery(self):
        """JD weighting combines with mastery-based urgency."""
        mastery = {
            "system_design.caching": 60,   # medium mastery, but required (2x)
            "system_design.sharding": 0,   # zero mastery, not in JD (0.5x)
        }
        plan = generate_study_plan(SAMPLE_TOPICS, mastery, days_until_interview=2, sessions_per_day=5, active_jd=_make_jd_with_skills())
        day1_topics = [s["topic_id"] for s in plan[0]["sessions"]]
        # Caching has gap=10, urgency=10*1.4*2.0=28
        # Sharding has gap=70, urgency=70*1.6*0.5=56 — sharding still higher due to huge gap
        # This test just verifies both appear and no crash
        assert "system_design.caching" in day1_topics
        assert "system_design.sharding" in day1_topics
