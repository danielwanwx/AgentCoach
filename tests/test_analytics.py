import os
import tempfile
from agentcoach.analytics.store import AnalyticsStore

def test_record_and_get_mastery():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test_analytics.db")
        store = AnalyticsStore(db_path=db_path)
        store.record_score("user1", "system_design.caching", +20, "quiz", "Got basics right")
        mastery = store.get_mastery("user1", "system_design.caching")
        assert mastery == 20

def test_mastery_accumulates():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test_analytics.db")
        store = AnalyticsStore(db_path=db_path)
        store.record_score("user1", "system_design.caching", +20, "quiz", "Good")
        store.record_score("user1", "system_design.caching", +15, "reinforce", "Better")
        mastery = store.get_mastery("user1", "system_design.caching")
        assert mastery == 35

def test_mastery_capped_at_100():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test_analytics.db")
        store = AnalyticsStore(db_path=db_path)
        store.record_score("user1", "system_design.caching", +80, "mock", "Great")
        store.record_score("user1", "system_design.caching", +50, "mock", "Perfect")
        mastery = store.get_mastery("user1", "system_design.caching")
        assert mastery == 100

def test_mastery_floor_at_0():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test_analytics.db")
        store = AnalyticsStore(db_path=db_path)
        store.record_score("user1", "system_design.caching", -50, "mock", "Bad")
        mastery = store.get_mastery("user1", "system_design.caching")
        assert mastery == 0

def test_get_progress():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test_analytics.db")
        store = AnalyticsStore(db_path=db_path)
        store.record_score("user1", "system_design.caching", +80, "mock", "Great")
        store.record_score("user1", "system_design.cap_theorem", +40, "quiz", "OK")
        progress = store.get_progress("user1", "system_design")
        assert len(progress) == 2
        assert any(p["topic_id"] == "system_design.caching" and p["mastery"] == 80 for p in progress)

def test_unscored_topic_returns_zero():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test_analytics.db")
        store = AnalyticsStore(db_path=db_path)
        mastery = store.get_mastery("user1", "system_design.caching")
        assert mastery == 0
