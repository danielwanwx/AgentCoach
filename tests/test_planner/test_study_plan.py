"""Tests for agentcoach/planner/__init__.py"""
import pytest
from datetime import datetime

from agentcoach.planner import generate_study_plan, format_plan


# Reusable fixtures
SAMPLE_TOPICS = [
    {"id": "sd-1", "name": "URL Shortener Design", "difficulty_level": 2},
    {"id": "sd-2", "name": "Rate Limiter Design", "difficulty_level": 3},
    {"id": "algo-1", "name": "Binary Search Variants", "difficulty_level": 1},
    {"id": "beh-1", "name": "Conflict Resolution", "difficulty_level": 1},
    {"id": "ai-1", "name": "RAG Pipeline", "difficulty_level": 2},
]


class TestGenerateStudyPlan:
    """Tests for the study plan generator."""

    def test_plan_has_correct_number_of_days(self):
        """Plan length equals the days_until_interview parameter."""
        plan = generate_study_plan(
            syllabus_topics=SAMPLE_TOPICS,
            mastery_data={},
            days_until_interview=10,
        )
        assert len(plan) == 10
        assert plan[0]["day"] == 1
        assert plan[-1]["day"] == 10

    def test_plan_prioritizes_low_mastery_topics(self):
        """Topics with lower mastery appear earlier in the plan."""
        mastery = {
            "sd-1": 80,  # high mastery
            "sd-2": 10,  # low mastery
            "algo-1": 90,  # high mastery
            "beh-1": 5,  # very low mastery
            "ai-1": 15,  # low mastery
        }
        plan = generate_study_plan(
            syllabus_topics=SAMPLE_TOPICS,
            mastery_data=mastery,
            days_until_interview=7,
        )
        # First day's first session should be a low-mastery topic
        first_session = plan[0]["sessions"][0]
        assert first_session["topic_id"] in ("sd-2", "beh-1", "ai-1"), (
            f"Expected a low-mastery topic first, got {first_session['topic_id']}"
        )

    def test_plan_includes_weekly_mock(self):
        """Day 7 (index 6) includes a 'Full Mock Interview' session."""
        plan = generate_study_plan(
            syllabus_topics=SAMPLE_TOPICS,
            mastery_data={},
            days_until_interview=14,
        )
        # Day 7 is at index 6 (day_num=6, which is 6 % 7 == 6)
        day_7 = plan[6]
        session_names = [s["topic_name"] for s in day_7["sessions"]]
        assert "Full Mock Interview" in session_names

        # Day 14 is at index 13 (day_num=13, which is 13 % 7 == 6)
        day_14 = plan[13]
        session_names_14 = [s["topic_name"] for s in day_14["sessions"]]
        assert "Full Mock Interview" in session_names_14

    def test_plan_sessions_have_required_keys(self):
        """Each session in the plan has topic_id, topic_name, mode, reason."""
        plan = generate_study_plan(
            syllabus_topics=SAMPLE_TOPICS,
            mastery_data={},
            days_until_interview=3,
        )
        for day in plan:
            assert "day" in day
            assert "date" in day
            assert "sessions" in day
            for session in day["sessions"]:
                assert "topic_id" in session
                assert "topic_name" in session
                assert "mode" in session
                assert "reason" in session

    def test_plan_mode_assignment(self):
        """Topics are assigned correct modes based on mastery levels."""
        mastery = {
            "sd-1": 0,   # learn (0%)
            "sd-2": 30,  # learn (<40%)
            "algo-1": 50,  # reinforce (40-69%)
            "beh-1": 75,  # mock (>=70%)
            "ai-1": 0,   # learn
        }
        plan = generate_study_plan(
            syllabus_topics=SAMPLE_TOPICS,
            mastery_data=mastery,
            days_until_interview=14,
            sessions_per_day=5,  # enough to cover all topics on day 1
        )
        # Collect all sessions from day 1 (should have all 5 topics)
        day1_sessions = {s["topic_id"]: s["mode"] for s in plan[0]["sessions"]}

        # Check modes for topics that appear on day 1
        if "sd-1" in day1_sessions:
            assert day1_sessions["sd-1"] == "learn"
        if "algo-1" in day1_sessions:
            assert day1_sessions["algo-1"] == "reinforce"
        if "beh-1" in day1_sessions:
            assert day1_sessions["beh-1"] == "mock"

    def test_plan_dates_are_sequential(self):
        """Plan dates are consecutive ISO-format strings."""
        plan = generate_study_plan(
            syllabus_topics=SAMPLE_TOPICS,
            mastery_data={},
            days_until_interview=5,
        )
        dates = [day["date"] for day in plan]
        for i in range(1, len(dates)):
            prev = datetime.fromisoformat(dates[i - 1])
            curr = datetime.fromisoformat(dates[i])
            assert (curr - prev).days == 1


class TestFormatPlan:
    """Tests for plan formatting."""

    def test_format_plan_output(self):
        """format_plan returns a human-readable string with day labels."""
        plan = generate_study_plan(
            syllabus_topics=SAMPLE_TOPICS,
            mastery_data={},
            days_until_interview=10,
        )
        output = format_plan(plan, days_to_show=3)

        assert isinstance(output, str)
        assert "Day 1" in output
        assert "Day 2" in output
        assert "Day 3" in output
        # Should mention remaining days
        assert "more days" in output

    def test_format_plan_shows_modes(self):
        """Formatted plan includes mode labels (LEARN, REINFORCE, MOCK)."""
        plan = generate_study_plan(
            syllabus_topics=SAMPLE_TOPICS,
            mastery_data={"sd-1": 50},
            days_until_interview=3,
        )
        output = format_plan(plan)

        # At least one mode label should appear
        assert any(mode in output for mode in ["LEARN", "REINFORCE", "MOCK"])
