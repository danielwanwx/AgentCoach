from pathlib import Path

from agentcoach.content.compiler import EditorialUnit, compile_editorial_units, parse_markdown_sections
from agentcoach.coaching.learning_harness import (
    HELLOINTERVIEW_NETWORKING_KB_PATH,
    HELLOINTERVIEW_NETWORKING_URL,
    NETWORKING_AGENTIC_BLUEPRINT,
    NETWORKING_QUIZ,
    NETWORKING_UNIT_SOURCE_SECTIONS,
    NETWORKING_UNITS,
    handle_learning_step,
    initial_learning_frame,
    networking_coverage_summary,
    new_learning_state,
)


ROOT = Path(__file__).resolve().parents[1]


def test_markdown_parser_recovers_plain_heading_sections():
    sections = parse_markdown_sections(
        ROOT / HELLOINTERVIEW_NETWORKING_KB_PATH,
        known_titles=NETWORKING_UNIT_SOURCE_SECTIONS["networking.tcp_udp"],
        source_label="HelloInterview",
        project_root=ROOT,
    )

    assert "UDP: Fast but Unreliable" in sections
    udp = sections["UDP: Fast but Unreliable"]
    assert udp.paragraphs
    assert udp.paragraphs[0].local_path == HELLOINTERVIEW_NETWORKING_KB_PATH
    assert udp.paragraphs[0].line_start > udp.line_start
    assert udp.paragraphs[0].ref()["preview"]


def test_editorial_unit_compiles_with_paragraph_provenance():
    unit = EditorialUnit(
        id="networking.test",
        source_path=HELLOINTERVIEW_NETWORKING_KB_PATH,
        source_sections=["Networking 101", "Networking Layers"],
        title="Test",
        objective="Test objective",
        body="Polished body",
        example="Polished example",
        coach_script="Polished script",
        key_points=["One point"],
        check_prompt="Check?",
        options=[{"id": "a", "label": "A"}],
        correct_option_id="a",
        expected_keywords=["network"],
        repair="Repair",
        flash_body="Flash",
        quizzes=[],
    )

    compiled = compile_editorial_units([unit], kb_root=ROOT, project_root=ROOT)

    assert len(compiled) == 1
    assert compiled[0].body == "Polished body"
    assert compiled[0].draft["paragraph_count"] > 0
    assert compiled[0].source_paragraphs
    assert compiled[0].source_paragraphs[0]["section"] in {"Networking 101", "Networking Layers"}


def test_learning_harness_frame_exposes_compiler_provenance():
    state = new_learning_state("system_design.networking", "Networking & Protocols")
    frame = initial_learning_frame(state)
    detail = frame["card"]["detail"]

    assert "Covers:" not in frame["card"]["body"]
    assert len(frame["card"]["body"]) >= 350
    assert len(frame["card"]["body"]) <= 620
    assert detail["draft"]["compiler_version"] == 1
    assert detail["source_paragraphs"]
    assert detail["sources"][0]["paragraphs"]
    assert detail["sources"][0]["local_path"] == HELLOINTERVIEW_NETWORKING_KB_PATH
    assert detail["sources"][0]["url"] == HELLOINTERVIEW_NETWORKING_URL
    assert [source["label"] for source in detail["sources"]] == [
        "HelloInterview Networking Essentials"
    ]
    assert frame["source"]["resources"] == [
        {
            "label": "HelloInterview Networking Essentials",
            "url": HELLOINTERVIEW_NETWORKING_URL,
        }
    ]
    assert "ByteByteGo" not in str(frame["source"])
    assert "Grokking" not in str(frame["source"])
    assert detail["knowledge_points"]
    assert detail["quiz_dimensions"]
    assert detail["key_points"] == NETWORKING_UNITS[0].key_points
    assert detail["interview_script"].startswith("I start with one browser request")
    assert "simple web request narration" in detail["quiz_dimensions"]
    for term in ["DNS", "IP", "TCP", "HTTP"]:
        assert term in frame["card"]["body"]
    assert "caches" not in frame["card"]["body"].lower()
    assert "diagram below" in frame["card"]["body"]
    assert detail["visual"]["type"] == "request_path"
    assert [node["label"] for node in detail["visual"]["nodes"]] == [
        "Browser URL",
        "DNS lookup",
        "IP routing",
        "TCP handshake",
        "HTTP response",
        "Reuse / teardown",
    ]
    assert [action["id"] for action in frame["actions"]] == [
        "play",
        "ask",
        "quiz",
        "continue",
    ]
    assert "expand" not in {action["id"] for action in frame["actions"]}
    assert "Read" not in {action["label"] for action in frame["actions"]}
    assert not any(action["id"].startswith("source_") for action in frame["actions"])


def test_networking_key_points_are_memory_anchors():
    for unit in NETWORKING_UNITS:
        assert 3 <= len(unit.key_points) <= 5, unit.id
        for point in unit.key_points:
            assert ":" in point, (unit.id, point)
            label, copy = point.split(":", 1)
            assert 1 <= len(label.strip()) <= 20, (unit.id, point)
            assert copy.strip(), (unit.id, point)
            assert len(copy.strip()) <= 64, (unit.id, point)
            assert not point.endswith("."), (unit.id, point)


def test_networking_cards_include_memorizable_interview_script():
    state = new_learning_state("system_design.networking", "Networking & Protocols")
    blocked_terms = ("HelloInterview", "chapter", "article")

    for index, unit_id in enumerate(state["units"]):
        state["unit_index"] = index
        frame = initial_learning_frame(state)
        script = frame["card"]["detail"]["interview_script"]
        assert script, unit_id
        assert 80 <= len(script) <= 260, (unit_id, script)
        assert not any(term in script for term in blocked_terms), (unit_id, script)
        assert any(
            script.startswith(prefix)
            for prefix in ("I ", "I'd ", "If ", "For ", "Once ", "A ")
        ), (unit_id, script)


def test_networking_first_quiz_tracks_hello_interview_request_sequence():
    state = new_learning_state("system_design.networking", "Networking & Protocols")
    frame = handle_learning_step(state, action="quiz")
    check_text = str(frame["check"])

    for term in ["DNS", "IP", "TCP", "HTTP", "response"]:
        assert term in check_text
    assert "teardown" in check_text or "reuse" in check_text
    assert "chapter" not in check_text.lower()
    assert "article" not in check_text.lower()
    assert "HelloInterview" not in check_text
    assert "ByteByteGo" not in str(frame["source"])
    assert frame["source"]["url"] == HELLOINTERVIEW_NETWORKING_URL


def test_networking_public_copy_speaks_as_the_coach_not_the_source():
    blocked_terms = ("HelloInterview", "chapter", "article")
    unit_fields = ("title", "objective", "body", "example", "coach_script", "repair")
    quiz_fields = ("title", "prompt", "rationale", "repair")

    for unit in NETWORKING_UNITS:
        for field in unit_fields:
            value = str(getattr(unit, field))
            assert not any(term in value for term in blocked_terms), (unit.id, field, value)

    for unit_id, questions in NETWORKING_QUIZ.items():
        for question in questions:
            for field in quiz_fields:
                value = str(question.get(field, ""))
                assert not any(term in value for term in blocked_terms), (
                    unit_id,
                    question.get("id"),
                    field,
                    value,
                )


def test_learning_harness_feedback_uses_natural_tone():
    state = new_learning_state("system_design.networking", "Networking & Protocols")
    handle_learning_step(state, action="quiz")

    frame = handle_learning_step(state, action="answer_option", option_id="a")

    assert frame["evaluation"]["verdict"] == "solid"
    assert frame["card"]["body"].startswith("Yes.")
    assert "Right:" not in frame["card"]["body"]


def test_networking_coverage_summary_covers_key_kb_sections():
    summary = networking_coverage_summary()
    key_sections = set(summary["key_sections"])

    assert summary["topic_id"] == "system_design.networking"
    assert summary["source_path"] == HELLOINTERVIEW_NETWORKING_KB_PATH
    assert not summary["missing_sections"]["cards"]
    assert not summary["missing_sections"]["quizzes"]
    assert not summary["missing_sections"]["source"]

    assert {
        "Networking 101",
        "Network Layer Protocols",
        "Transport Layer Protocols",
        "HTTP/HTTPS: The Web's Foundation",
        "Server-Sent Events (SSE): Real-Time Push Communication",
        "Client-Side Load Balancing",
        "Load Balancing",
        "Regional Partitioning",
        "Circuit Breakers",
        "Wrapping Up",
    } <= key_sections
    assert set(summary["covered_sections"]["cards"]) == key_sections
    assert set(summary["covered_sections"]["quizzes"]) == key_sections
    assert all(summary["section_quiz_index"][section] for section in key_sections)
    assert summary["unit_count"] >= 13
    assert "layers.public_ip" in summary["section_quiz_index"]["Network Layer Protocols"]
    assert "protocol_choice.sse_one_way" in summary["section_quiz_index"][
        "Server-Sent Events (SSE): Real-Time Push Communication"
    ]
    assert "failures.circuit_breaker" in summary["section_quiz_index"]["Circuit Breakers"]

    realtime_unit = next(
        unit for unit in summary["units"] if unit["id"] == "networking.realtime_protocols"
    )
    assert "Server-Sent Events (SSE): Real-Time Push Communication" in realtime_unit["sections"]
    assert realtime_unit["quiz_count"] > 0


def test_networking_unit_titles_read_like_coach_prompts():
    titles = [unit.title for unit in NETWORKING_UNITS]
    directory_titles = {
        "Application Layer Protocols",
        "Client-Side Load Balancing",
        "Dedicated Load Balancers",
        "Load Balancing",
        "Network Layer Protocols",
        "Networking Layers",
        "Transport Layer Protocols",
        "WebRTC",
        "WebSockets",
    }

    assert len(titles) == 13
    assert all(len(title) <= 60 for title in titles)
    assert not directory_titles.intersection(titles)
    assert all(not title.endswith("Protocols") for title in titles)


def test_networking_quiz_covers_deep_agentic_dimensions():
    quiz_ids = {
        question["id"]
        for questions in NETWORKING_QUIZ.values()
        for question in questions
    }

    assert sum(len(questions) for questions in NETWORKING_QUIZ.values()) >= 40
    assert {
        "mental_model.scenario_recap",
        "layers.dns_ip_boundary",
        "layers.public_ip",
        "network_layer.private_boundary",
        "tcp_udp.quic_http3",
        "protocol_choice.graphql_resolvers",
        "protocol_choice.sse_one_way",
        "protocol_choice.websocket_infra",
        "protocol_choice.webrtc_nat",
        "protocol_choice.scenario_mix",
        "realtime.sse_reconnect",
        "webrtc.fit",
        "http_api.https_tls_boundary",
        "latency.regionalization_tradeoff",
        "latency.connection_setup",
        "load_balancing.l4_l7",
        "load_balancing.client_side_dns",
        "load_balancing.algorithm_fit",
        "lb_client_side.registry",
        "lb_dedicated.websocket_l4",
        "failures.jitter_storm",
        "failures.circuit_breaker",
        "failures.scenario_policy",
    } <= quiz_ids

    assert set(NETWORKING_AGENTIC_BLUEPRINT) == set(NETWORKING_QUIZ)
    for unit_id, blueprint in NETWORKING_AGENTIC_BLUEPRINT.items():
        assert blueprint["card_points"], unit_id
        assert blueprint["quiz_dimensions"], unit_id
        assert blueprint["dynamic_insert_rules"], unit_id


def test_free_text_quiz_requires_multiple_concepts():
    cases = [
        (
            "networking.mental_model",
            "mental_model.scenario_recap",
            "The request goes somewhere and networking happens.",
            (
                "The browser enters a URL, DNS resolves the name, IP routes packets, TCP "
                "establishes the connection, and HTTP returns the response; latency can "
                "come from lookup, setup, or extra packets."
            ),
        ),
        (
            "networking.realtime_protocols",
            "protocol_choice.scenario_mix",
            "Use WebSocket for everything because it is realtime.",
            (
                "Use HTTP/REST for initial page load, SSE for server alerts, WebSocket "
                "for bidirectional chat, and WebRTC for the video media path."
            ),
        ),
        (
            "networking.failures",
            "failures.scenario_policy",
            "Retry the payment call until it works.",
            (
                "Use a timeout budget, retry with capped exponential backoff and jitter, "
                "require an idempotency key, and open a circuit breaker if payments keeps failing."
            ),
        ),
    ]

    for unit_id, quiz_id, weak_answer, strong_answer in cases:
        state = new_learning_state("system_design.networking", "Networking & Protocols")
        state["unit_index"] = state["units"].index(unit_id)
        questions = NETWORKING_QUIZ[unit_id]
        quiz_index = next(
            index for index, question in enumerate(questions)
            if question["id"] == quiz_id
        )
        state["quiz_index"] = quiz_index

        weak = handle_learning_step(state, user_text=weak_answer)
        assert weak["evaluation"]["verdict"] == "not_yet", quiz_id

        state["quiz_index"] = quiz_index
        strong = handle_learning_step(state, user_text=strong_answer)
        assert strong["evaluation"]["verdict"] == "solid", quiz_id
