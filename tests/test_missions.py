from pathlib import Path

from agentcoach.diagnostics import evaluate_diagnostic_answers, generate_diagnostic_probe, sniff_topic
from agentcoach.missions import MissionOrchestrator, MissionStore
from agentcoach.roles import get_role_profile, map_transition_gaps
from agentcoach.syllabus.loader import SyllabusLoader
from agentcoach.web.server import (
    ServerState,
    _create_mission,
    _end,
    _mission_diagnostic,
    _start_mission_session,
    _turn,
)


ROOT = Path(__file__).resolve().parents[1]


def test_topic_sniff_maps_llm_gateway_rate_limit_to_system_design():
    sniff = sniff_topic(
        "I need to understand rate limiting for an LLM gateway",
        target_role="ai_engineer",
        background="backend",
    )

    assert sniff["topic_id"] == "system_design.rate_limiting"
    assert sniff["cluster"] == "rate_limiting"
    assert sniff["role_hint"] == "ai_engineer"
    assert sniff["confidence"] >= 0.7


def test_diagnostic_probe_and_evaluator_emit_role_gap_signals():
    sniff = sniff_topic("RAG retrieval quality", target_role="ai_engineer")
    probe = generate_diagnostic_probe(sniff, target_role="ai_engineer")

    diagnosis = evaluate_diagnostic_answers(
        probe,
        answers=[
            {"question_id": "q1", "answer": "true"},
            {"question_id": "q2", "answer": "syntax_error"},
            {"question_id": "q3", "answer": "latency"},
        ],
        topic_sniff=sniff,
        target_role="ai_engineer",
        background="backend",
    )

    assert len(probe["questions"]) == 3
    assert diagnosis["concept_level"] in {"unknown", "fuzzy"}
    assert "evaluation" in diagnosis["gap_signals"]
    assert diagnosis["next_training_focus"]


def test_role_gap_mapper_preserves_swe_transfer_strengths():
    profile = get_role_profile("fde", company="OpenAI")
    gaps = map_transition_gaps(
        learner_diagnosis={
            "current_base": "backend",
            "gap_signals": ["transfer", "failure_mode"],
        },
        role_profile=profile,
        background="backend",
    )

    assert gaps["role_family"] == "fde"
    assert "core_swe" in gaps["transfer_strengths"]
    assert "fde_customer_deployment" in gaps["missing_clusters"]
    assert gaps["recommended_focus"]


def test_mission_orchestrator_creates_diagnostic_then_training_plan(tmp_path):
    store = MissionStore(db_path=str(tmp_path / "missions.db"))
    orchestrator = MissionOrchestrator(
        store=store,
        project_root=ROOT,
        syllabus=SyllabusLoader(),
    )
    mission = orchestrator.create_mission({
        "user_id": "u1",
        "input_text": "rate limiter for LLM gateway",
        "target_role": "fde",
        "target_company": "OpenAI",
        "background": "backend",
    })

    assert mission["status"] == "diagnosing"
    assert mission["diagnostic_probe"]["questions"]

    trained = orchestrator.submit_diagnostic(
        mission["mission_id"],
        [
            {"question_id": "q1", "answer": "false"},
            {"question_id": "q2", "answer": "tokens_per_tenant"},
            {"question_id": "q3", "answer": "retry storm without backoff can overload cost and quota"},
        ],
    )

    assert trained["status"] == "training"
    assert trained["learner_diagnosis"]["target_role"] == "fde"
    assert trained["source_manifest"]["adapter_status"]["local_kb"] in {"ready", "empty"}
    assert trained["source_manifest"]["adapter_status"]["notebooklm"] == "stub"
    assert trained["harness_plan"]["stages"]
    assert trained["next_action"]["mode"] in {"learn", "reinforce", "mock_system_design"}
    assert trained["evidence"][0]["stage"] == "diagnose"


def test_web_mission_flow_bridges_to_existing_session_start(tmp_path):
    state = ServerState(tmp_path, demo_mode=True)
    mission = _create_mission(state, {
        "user_id": "u1",
        "input_text": "agent tool use",
        "target_role": "agentic_engineer",
        "background": "backend",
    })

    assert mission["status"] == "diagnosing"

    trained = _mission_diagnostic(state, mission["mission_id"], {
        "answers": [
            {"question_id": "q1", "answer": "false"},
            {"question_id": "q2", "answer": "trace_steps"},
            {"question_id": "q3", "answer": "Use an allowlist and require approval for risky tools."},
        ]
    })

    started = _start_mission_session(state, mission["mission_id"])

    assert trained["status"] == "training"
    assert started["mission_id"] == mission["mission_id"]
    assert started["session_id"]
    assert started["frame"]["version"] == 2
    assert started["next_action"]["topic_id"] == "ai_engineering.agent_tool_use"


def test_mission_session_end_keeps_next_action_on_role_transition_route(tmp_path):
    state = ServerState(tmp_path, demo_mode=True)
    mission = _create_mission(state, {
        "user_id": "u1",
        "input_text": "rate limiting for an LLM gateway",
        "target_role": "fde",
        "target_company": "OpenAI",
        "background": "backend",
    })
    _mission_diagnostic(state, mission["mission_id"], {
        "answers": [
            {"question_id": "q1", "answer": "false"},
            {"question_id": "q2", "answer": "requests_per_ip"},
            {"question_id": "q3", "answer": "It may slow down."},
        ]
    })
    started = _start_mission_session(state, mission["mission_id"])

    _turn(state, {
        "session_id": started["session_id"],
        "user_text": (
            "At the LLM gateway, rate limiting protects tenant token budgets, "
            "prevents retry storms, and gives customer rollout safety."
        ),
    })
    report = _end(state, {"session_id": started["session_id"]})
    mission_after = state.mission_orchestrator.get_mission(mission["mission_id"])

    assert report["mission_id"] == mission["mission_id"]
    assert report["next_action"]["topic_id"] == "system_design.rate_limiting"
    assert report["next_action"]["mode"] == "reinforce"
    assert "Forward Deployed Engineer" in report["next_action"]["coach_brief"]
    assert mission_after["next_action"]["topic_id"] == "system_design.rate_limiting"
    assert len(mission_after["evidence"]) == 2
    assert mission_after["evidence"][-1]["stage"] == "learn"
