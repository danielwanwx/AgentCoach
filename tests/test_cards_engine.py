from agentcoach.cards.engine import LOCAL_CARD_ACTIONS, TARGETED_NETWORKING_TITLES
from agentcoach.runtime.observer import observe_interaction
from agentcoach.web.server import ServerState, _start_session, _turn


def test_train_start_returns_diagnostic_card_frame(tmp_path):
    state = ServerState(tmp_path, demo_mode=True)

    result = _start_session(state, {
        "mode": "reinforce",
        "topic_id": "system_design.caching",
        "user_id": "test-user",
    })

    frame = result["frame"]
    assert frame["version"] == 2
    assert frame["mode"] == "reinforce"
    assert frame["kind"] == "diagnose"
    assert frame["card"]["stage"] == "diagnose"
    assert frame["card"]["body"]
    assert frame["check"]["type"] == "free_text"


def test_mock_start_returns_interview_stage_card_frame(tmp_path):
    state = ServerState(tmp_path, demo_mode=True)

    result = _start_session(state, {
        "mode": "mock_system_design",
        "topic_id": "system_design.url_shortener",
        "user_id": "test-user",
    })

    frame = result["frame"]
    assert frame["version"] == 2
    assert frame["mode"] == "mock_system_design"
    assert frame["kind"] == "interview"
    assert frame["card"]["stage"] == "interview"
    assert "requirements" in frame["card"]["body"].lower()


def test_learn_start_normalizes_legacy_harness_frame(tmp_path):
    state = ServerState(tmp_path, demo_mode=True)

    result = _start_session(state, {
        "mode": "learn",
        "topic_id": "system_design.networking",
        "user_id": "test-user",
    })

    frame = result["frame"]
    assert frame["version"] == 2
    assert frame["mode"] == "learn"
    assert frame["card"]["card_id"]
    assert frame["card"]["visible_body"] == frame["card"]["body"]


def test_vague_mock_answer_inserts_repair_card(tmp_path):
    state = ServerState(tmp_path, demo_mode=True)
    started = _start_session(state, {
        "mode": "mock_system_design",
        "topic_id": "system_design.url_shortener",
        "user_id": "test-user",
    })

    result = _turn(state, {
        "session_id": started["session_id"],
        "user_text": "Maybe some stuff kind of does things and probably stores it.",
    })

    assert result["signal"]["recommended_action"] == "insert_repair_card"
    assert result["frame"]["kind"] == "repair"
    assert result["frame"]["card"]["stage"] == "repair"


def test_explanation_request_in_train_recommends_learn_card():
    signal = observe_interaction(
        session_id="s1",
        topic_id="system_design.caching",
        mode="reinforce",
        event_type="utterance",
        raw_text="Can you explain what caching is first?",
    )

    assert signal["detected_gap"] == "needs_teaching_in_pressure_mode"
    assert signal["recommended_action"] == "recommend_learn_card"


def test_networking_observer_consumes_dynamic_insert_rules(tmp_path):
    state = ServerState(tmp_path, demo_mode=True)
    started = _start_session(state, {
        "mode": "mock_system_design",
        "topic_id": "system_design.networking",
        "user_id": "test-user",
    })

    result = _turn(state, {
        "session_id": started["session_id"],
        "user_text": "Use WebRTC for the video call.",
    })

    assert result["signal"]["detected_gap"] == "networking.webrtc_signaling_missing"
    assert result["signal"]["recommended_card_id"] == "networking.webrtc"
    assert "WebRTC" in result["signal"]["coach_brief"]
    assert result["frame"]["kind"] == "repair"
    assert result["frame"]["card"]["title"] == "Let's name signaling and NAT traversal"
    assert result["frame"]["card"]["detail"]["recommended_card_id"] == "networking.webrtc"


def test_networking_targeted_titles_keep_coach_tone():
    assert TARGETED_NETWORKING_TITLES
    assert all(title.startswith("Let's ") for title in TARGETED_NETWORKING_TITLES.values())
    assert not any("Repair the" in title for title in TARGETED_NETWORKING_TITLES.values())
    assert all(len(title) <= 60 for title in TARGETED_NETWORKING_TITLES.values())


def test_local_card_actions_use_listen_without_read_overlay():
    assert LOCAL_CARD_ACTIONS == [{"id": "play", "label": "Listen", "kind": "local"}]
