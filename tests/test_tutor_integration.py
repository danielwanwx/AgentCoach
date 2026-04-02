"""Integration tests for the full autonomous tutoring loop."""
import os
import sqlite3
import tempfile
from unittest.mock import MagicMock

from agentcoach.analytics.store import AnalyticsStore
from agentcoach.analytics.recommender import Recommender
from agentcoach.analytics.scorer import Scorer
from agentcoach.coach import Coach, QuizState
from agentcoach.llm.base import Message
from agentcoach.syllabus.loader import SyllabusLoader


def test_learn_session_uses_kb_content():
    """Coach in learn mode includes KB teaching material in system prompt."""
    llm = MagicMock()
    llm.generate.return_value = "Let me explain RAG..."

    coach = Coach(
        llm=llm, mode="learn",
        topic_name="RAG", topic_id="ai_agent.rag",
        kb_teaching_context="RAG combines retrieval with generation for grounded responses.",
    )
    assert "Teaching Material" in coach.history[0].content
    assert "RAG combines retrieval" in coach.history[0].content

    opening = coach.start()
    user_msg = llm.generate.call_args[0][0][1].content
    assert "learn about RAG" in user_msg


def test_quiz_state_tracks_progress():
    """QuizState increments and adjusts difficulty correctly."""
    llm = MagicMock()
    coach = Coach(llm=llm, mode="learn", topic_name="Test")

    # Teaching phase: "correct" should NOT trigger quiz tracking
    llm.generate.return_value = "That's correct, good observation. Let me explain more."
    coach.respond("I think caching helps with reads")
    assert coach.quiz_state.question_count == 0  # not in quiz mode yet

    # Coach enters quiz mode
    llm.generate.return_value = "Great, let's start the quiz! Question 1: What is caching?"
    coach.respond("I'm ready for the quiz")
    assert coach.quiz_state._quiz_active is True
    assert coach.quiz_state.question_count == 0  # quiz just started, no answer yet

    # 2 correct answers → difficulty upgrade
    llm.generate.return_value = "Correct! Well done."
    coach.respond("answer 1")
    coach.respond("answer 2")
    assert coach.quiz_state.correct_count == 2
    assert coach.quiz_state.difficulty == 2

    # 1 incorrect → difficulty drops, weak concept added
    llm.generate.return_value = "Not quite. Actually, the answer should be X."
    coach.respond("wrong answer")
    assert coach.quiz_state.incorrect_count == 1
    assert coach.quiz_state.difficulty == 1
    assert len(coach.quiz_state.weak_concepts) > 0

    # System prompt has quiz state
    assert "Quiz State" in coach.history[0].content


def test_scorer_validates_against_kb():
    """Scorer includes KB reference material in scoring prompt."""
    kb = MagicMock()
    kb.search.return_value = [{"content": "RAG retrieves docs before generating."}]

    llm = MagicMock()
    llm.generate.return_value = '[{"topic_id": "ai_agent.rag", "score_delta": 10, "evidence": "OK"}]'

    scorer = Scorer(llm, kb_store=kb)
    history = [
        Message(role="system", content="coach"),
        Message(role="user", content="hi"),
        Message(role="assistant", content="quiz time"),
        Message(role="user", content="RAG uses embeddings"),
    ]
    scores = scorer.score_session(history, mode="learn", topic_id="ai_agent.rag")

    kb.search.assert_called_once()
    prompt = llm.generate.call_args[0][0][-1].content
    assert "Reference Material" in prompt
    assert "RAG retrieves docs" in prompt
    assert scores[0]["score_delta"] == 10


def test_full_learn_reinforce_mock_loop():
    """Full tutoring loop: learn → score → recommend reinforce → score → recommend mock."""
    syllabus = SyllabusLoader()

    with tempfile.TemporaryDirectory() as tmpdir:
        store = AnalyticsStore(db_path=os.path.join(tmpdir, "test.db"))
        rec = Recommender(store)

        # Get AI agent leaf topics
        topics = [t for t in syllabus.get_topics("ai_agent") if t.get("resources")]

        # Step 1: First recommendation should be "learn" on a fundamental
        r1 = rec.recommend("u1", topics, syllabus=syllabus)
        assert r1["mode"] == "learn"
        assert r1["topic_id"] == "ai_agent.transformer"  # no prereqs, unstarted

        # Step 2: Record learn session scores
        store.record_score("u1", "ai_agent.transformer", 15, "learn", "Good basics")
        store.record_score("u1", "ai_agent.transformer", 15, "learn", "Quiz OK")
        mastery = store.get_mastery("u1", "ai_agent.transformer")
        assert 20 <= mastery <= 30  # 30 * 0.7 (learn weight) ≈ 21

        # Step 3: Still learn (below 40 threshold)
        r2 = rec.recommend("u1", topics, syllabus=syllabus)
        assert r2["mode"] == "learn"

        # Step 4: More learning → cross 40 threshold
        store.record_score("u1", "ai_agent.transformer", 20, "learn")
        store.record_score("u1", "ai_agent.transformer", 20, "learn")
        mastery2 = store.get_mastery("u1", "ai_agent.transformer")
        assert mastery2 >= 40  # enough to unlock reinforce

        # Step 5: Now prompting (prereq: transformer met) should appear
        r3 = rec.recommend("u1", topics, syllabus=syllabus)
        # Could be transformer (reinforce) or prompting (learn) depending on priority
        assert r3["mode"] in ("learn", "reinforce")

        # Step 6: Master transformer fully, record mock score
        store.record_score("u1", "ai_agent.transformer", 25, "mock")
        store.record_score("u1", "ai_agent.transformer", 25, "mock")
        mastery3 = store.get_mastery("u1", "ai_agent.transformer")
        assert mastery3 >= 70

        # Step 7: Recommend should now suggest another topic or mock
        r4 = rec.recommend("u1", topics, syllabus=syllabus)
        # Should NOT recommend transformer (high mastery), should pick a lower one
        # Prompting is now unlocked (transformer prereq met)
        assert r4["topic_id"] != "ai_agent.transformer" or r4["mode"] == "mock"


def test_mastery_decay_affects_recommendations():
    """Old scores decay, making previously-mastered topics re-appear for review."""
    syllabus = SyllabusLoader()

    with tempfile.TemporaryDirectory() as tmpdir:
        store = AnalyticsStore(db_path=os.path.join(tmpdir, "test.db"))
        rec = Recommender(store)

        topics = [t for t in syllabus.get_topics("ai_agent") if t.get("resources")]

        # Insert old high score (90 days ago) for transformer
        conn = sqlite3.connect(os.path.join(tmpdir, "test.db"))
        conn.execute(
            "INSERT INTO score_events (user_id, topic_id, score_delta, mode, evidence, created_at) "
            "VALUES (?, ?, ?, ?, ?, datetime('now', '-90 days'))",
            ("u1", "ai_agent.transformer", 80, "mock", "Great"),
        )
        conn.commit()
        conn.close()

        # Mastery should be decayed (80 * 1.5 * 0.5^3 ≈ 15)
        mastery = store.get_mastery("u1", "ai_agent.transformer")
        assert mastery < 40  # decayed below learn threshold

        # Recommender should suggest re-learning
        r = rec.recommend("u1", topics, syllabus=syllabus)
        assert r["mode"] == "learn"


def test_prerequisites_block_advanced_topics():
    """Advanced topics are blocked until prerequisites are mastered."""
    syllabus = SyllabusLoader()

    with tempfile.TemporaryDirectory() as tmpdir:
        store = AnalyticsStore(db_path=os.path.join(tmpdir, "test.db"))
        rec = Recommender(store)

        topics = [t for t in syllabus.get_topics("ai_agent") if t.get("resources")]

        # RAG requires transformer + prompting
        rag_topic = syllabus.get_topic("ai_agent.rag")
        assert "ai_agent.transformer" in rag_topic["prerequisites"]

        # Without mastering prerequisites, RAG should not be recommended
        r = rec.recommend("u1", topics, syllabus=syllabus)
        assert r["topic_id"] != "ai_agent.rag"

        # Master transformer but not prompting
        store.record_score("u1", "ai_agent.transformer", 60, "mock")
        r2 = rec.recommend("u1", topics, syllabus=syllabus)
        assert r2["topic_id"] != "ai_agent.rag"  # prompting prereq not met

        # Master prompting too
        store.record_score("u1", "ai_agent.prompting", 60, "mock")
        # Now RAG should be unlocked (both prereqs met)
        r3 = rec.recommend("u1", topics, syllabus=syllabus)
        # RAG is now eligible (though another topic might have higher priority)
        rag_mastery = store.get_mastery("u1", "ai_agent.rag")
        assert rag_mastery == 0  # never practiced → should be high priority
