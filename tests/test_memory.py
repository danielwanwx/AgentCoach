import os
import tempfile
from agentcoach.memory.store import CoachMemory

def test_save_and_search_profile():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test_memory.db")
        mem = CoachMemory(db_path=db_path)
        mem.save_profile("I am a SWE with 5 years of Python experience, transitioning to AI Engineer.")
        results = mem.search("Python experience")
        assert len(results) > 0
        assert "Python" in results[0]

def test_save_and_search_jd():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test_memory.db")
        mem = CoachMemory(db_path=db_path)
        mem.save_jd("AI Engineer at OpenAI: Experience with LLMs, RAG, agent frameworks. 5+ years SWE.")
        results = mem.search("LLM agent")
        assert len(results) > 0

def test_save_and_search_feedback():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test_memory.db")
        mem = CoachMemory(db_path=db_path)
        mem.save_feedback("Weakness: needs more specific metrics in STAR answers. Strength: good technical depth.")
        results = mem.search("weakness metrics")
        assert len(results) > 0

def test_get_context_for_prompt():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test_memory.db")
        mem = CoachMemory(db_path=db_path)
        mem.save_profile("SWE, 5 years Python, transitioning to AI Engineer")
        mem.save_jd("AI Engineer at OpenAI: LLMs, RAG, agents")
        mem.save_feedback("Weakness: vague metrics in answers")
        context = mem.get_context()
        assert "Python" in context or "SWE" in context
