import os
import tempfile
from agentcoach.analytics.store import AnalyticsStore
from agentcoach.analytics.recommender import Recommender

FAKE_TOPICS = [
    {"id": "sd.caching", "name": "Caching", "domain": "system_design"},
    {"id": "sd.cap", "name": "CAP Theorem", "domain": "system_design"},
    {"id": "sd.sharding", "name": "Sharding", "domain": "system_design"},
]

def test_recommend_learn_for_unstarted():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        store = AnalyticsStore(db_path=db_path)
        rec = Recommender(store)
        suggestion = rec.recommend("user1", FAKE_TOPICS)
        assert suggestion["mode"] == "learn"

def test_recommend_learn_for_low_score():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        store = AnalyticsStore(db_path=db_path)
        store.record_score("user1", "sd.caching", 30, "quiz", "")
        store.record_score("user1", "sd.cap", 50, "quiz", "")
        store.record_score("user1", "sd.sharding", 50, "quiz", "")
        rec = Recommender(store)
        suggestion = rec.recommend("user1", FAKE_TOPICS)
        assert suggestion["topic_id"] == "sd.caching"
        assert suggestion["mode"] == "learn"

def test_recommend_reinforce_for_mid_score():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        store = AnalyticsStore(db_path=db_path)
        store.record_score("user1", "sd.caching", 55, "quiz", "")
        store.record_score("user1", "sd.cap", 55, "quiz", "")
        store.record_score("user1", "sd.sharding", 55, "quiz", "")
        rec = Recommender(store)
        suggestion = rec.recommend("user1", FAKE_TOPICS)
        assert suggestion["mode"] == "reinforce"

def test_recommend_mock_for_high_score():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        store = AnalyticsStore(db_path=db_path)
        store.record_score("user1", "sd.caching", 80, "mock", "")
        store.record_score("user1", "sd.cap", 80, "mock", "")
        store.record_score("user1", "sd.sharding", 80, "mock", "")
        rec = Recommender(store)
        suggestion = rec.recommend("user1", FAKE_TOPICS)
        assert suggestion["mode"] == "mock"
