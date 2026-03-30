from unittest.mock import MagicMock
from agentcoach.analytics.scorer import Scorer
from agentcoach.llm.base import Message


def test_scorer_parses_llm_response():
    mock_llm = MagicMock()
    mock_llm.generate.return_value = '[{"topic_id": "system_design.caching", "score_delta": 15, "evidence": "Good understanding of cache invalidation"}, {"topic_id": "system_design.cap_theorem", "score_delta": -5, "evidence": "Confused availability with consistency"}]'

    scorer = Scorer(mock_llm)
    history = [
        Message(role="system", content="You are an interviewer"),
        Message(role="user", content="ready"),
        Message(role="assistant", content="What is caching?"),
        Message(role="user", content="Caching stores frequently accessed data in memory"),
        Message(role="assistant", content="Good. What about CAP theorem?"),
        Message(role="user", content="It means you can have all three properties"),
    ]
    results = scorer.score_session(history, mode="learn", topic_id="system_design.caching")
    assert len(results) == 2
    assert results[0]["topic_id"] == "system_design.caching"
    assert results[0]["score_delta"] == 15


def test_scorer_handles_invalid_json():
    mock_llm = MagicMock()
    mock_llm.generate.return_value = "Sorry, I cannot parse this."

    scorer = Scorer(mock_llm)
    history = [Message(role="system", content="test"), Message(role="user", content="hi"), Message(role="assistant", content="hello")]
    results = scorer.score_session(history, mode="quiz", topic_id="test")
    assert results == []


def test_scorer_handles_json_in_text():
    mock_llm = MagicMock()
    mock_llm.generate.return_value = 'Here are the scores:\n[{"topic_id": "sd.caching", "score_delta": 10, "evidence": "OK"}]\nDone.'

    scorer = Scorer(mock_llm)
    history = [Message(role="system", content="test"), Message(role="user", content="hi"), Message(role="assistant", content="hello")]
    results = scorer.score_session(history, mode="learn", topic_id="sd.caching")
    assert len(results) == 1
    assert results[0]["score_delta"] == 10


def test_scorer_skips_short_history():
    mock_llm = MagicMock()
    scorer = Scorer(mock_llm)
    results = scorer.score_session([Message(role="system", content="hi")], mode="learn", topic_id="x")
    assert results == []
    mock_llm.generate.assert_not_called()
