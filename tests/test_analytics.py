import os
import sqlite3
import tempfile
from agentcoach.analytics.store import AnalyticsStore


def test_record_and_get_mastery():
    """Recent score with quiz mode (weight=1.0) returns ~score value."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test_analytics.db")
        store = AnalyticsStore(db_path=db_path)
        store.record_score("user1", "system_design.caching", +20, "quiz", "Got basics right")
        mastery = store.get_mastery("user1", "system_design.caching")
        # Recent score with weight 1.0: decay ~1.0, so mastery ≈ 20
        assert 19 <= mastery <= 20


def test_mastery_accumulates():
    """Multiple recent scores accumulate with mode weighting."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test_analytics.db")
        store = AnalyticsStore(db_path=db_path)
        store.record_score("user1", "system_design.caching", +20, "quiz", "Good")       # weight 1.0
        store.record_score("user1", "system_design.caching", +15, "reinforce", "Better") # weight 1.0
        mastery = store.get_mastery("user1", "system_design.caching")
        # 20*1.0 + 15*1.0 ≈ 35 (tiny decay on recent scores)
        assert 33 <= mastery <= 35


def test_mastery_capped_at_100():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test_analytics.db")
        store = AnalyticsStore(db_path=db_path)
        store.record_score("user1", "system_design.caching", +80, "mock", "Great")   # 80*1.5=120
        store.record_score("user1", "system_design.caching", +50, "mock", "Perfect") # 50*1.5=75
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
        # mock weight=1.5: 80*1.5=120 → capped to 100
        assert any(p["topic_id"] == "system_design.caching" and p["mastery"] == 100 for p in progress)
        # quiz weight=1.0: 40*1.0 ≈ 39-40
        assert any(p["topic_id"] == "system_design.cap_theorem" and 38 <= p["mastery"] <= 40 for p in progress)


def test_unscored_topic_returns_zero():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test_analytics.db")
        store = AnalyticsStore(db_path=db_path)
        mastery = store.get_mastery("user1", "system_design.caching")
        assert mastery == 0


def test_mastery_decays_over_time():
    """Score from 60 days ago should be significantly decayed (half-life=30d → ~25% of original)."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test_analytics.db")
        store = AnalyticsStore(db_path=db_path)
        # Manually insert a score dated 60 days ago
        conn = sqlite3.connect(db_path)
        conn.execute(
            "INSERT INTO score_events (user_id, topic_id, score_delta, mode, evidence, created_at) "
            "VALUES (?, ?, ?, ?, ?, datetime('now', '-60 days'))",
            ("user1", "sd.caching", 80, "quiz", "Old score"),
        )
        conn.commit()
        conn.close()
        mastery = store.get_mastery("user1", "sd.caching")
        # 80 * 1.0 * 0.5^(60/30) = 80 * 0.25 = 20
        assert 18 <= mastery <= 22


def test_recent_scores_dominate_old():
    """A recent low score should outweigh a decayed high score."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test_analytics.db")
        store = AnalyticsStore(db_path=db_path)
        conn = sqlite3.connect(db_path)
        # Old high score (90 days ago → decayed to ~12%)
        conn.execute(
            "INSERT INTO score_events (user_id, topic_id, score_delta, mode, evidence, created_at) "
            "VALUES (?, ?, ?, ?, ?, datetime('now', '-90 days'))",
            ("user1", "sd.caching", 80, "quiz", "Old"),
        )
        conn.commit()
        conn.close()
        # Recent score
        store.record_score("user1", "sd.caching", 10, "quiz", "Recent")
        mastery = store.get_mastery("user1", "sd.caching")
        # 80 * 0.5^3 ≈ 10 + 10 * ~1.0 ≈ 20
        assert 18 <= mastery <= 22


def test_mode_weighting():
    """Mock mode (1.5x) should produce higher mastery than quiz (1.0x) for same score."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test_analytics.db")
        store_mock = AnalyticsStore(db_path=os.path.join(tmpdir, "mock.db"))
        store_quiz = AnalyticsStore(db_path=os.path.join(tmpdir, "quiz.db"))
        store_mock.record_score("u1", "t1", 40, "mock", "")
        store_quiz.record_score("u1", "t1", 40, "quiz", "")
        m_mock = store_mock.get_mastery("u1", "t1")
        m_quiz = store_quiz.get_mastery("u1", "t1")
        # mock: 40*1.5=60, quiz: 40*1.0=40
        assert m_mock > m_quiz
        assert 58 <= m_mock <= 60
        assert 39 <= m_quiz <= 40


def test_get_last_practiced():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test_analytics.db")
        store = AnalyticsStore(db_path=db_path)
        assert store.get_last_practiced("u1", "t1") is None
        store.record_score("u1", "t1", 10, "quiz", "")
        last = store.get_last_practiced("u1", "t1")
        assert last is not None
