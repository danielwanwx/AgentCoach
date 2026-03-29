from agentcoach.prompt.templates import build_system_prompt


def test_build_prompt_with_kb_context():
    memory_ctx = "### User Profile\n- SWE, 5 years"
    kb_ctx = "### Relevant Knowledge\n- Consistent hashing uses a hash ring\n- CAP theorem: pick 2 of 3"
    prompt = build_system_prompt("behavioral", memory_context=memory_ctx, kb_context=kb_ctx)
    assert "hash ring" in prompt
    assert "SWE" in prompt
    assert "behavioral" in prompt.lower()


def test_build_prompt_without_kb():
    prompt = build_system_prompt("behavioral", memory_context="", kb_context="")
    assert "Relevant Knowledge" not in prompt


def test_build_prompt_kb_only_no_memory():
    kb_ctx = "- System design fundamentals"
    prompt = build_system_prompt("behavioral", memory_context="", kb_context=kb_ctx)
    assert "Relevant Knowledge Base" in prompt
    assert "What You Know About This Candidate" not in prompt


def test_coach_with_kb_store():
    """Test that Coach searches KB and updates system prompt."""
    from agentcoach.coach import Coach
    from agentcoach.llm.base import LLMAdapter, Message

    class MockLLM(LLMAdapter):
        def generate(self, messages):
            return "Mock response"

    class MockKBStore:
        def search(self, query, limit=3):
            return [
                {"section": "System Design", "content": "Consistent hashing distributes keys across nodes"},
                {"section": "Algorithms", "content": "Binary search runs in O(log n)"},
            ]

    llm = MockLLM()
    kb = MockKBStore()
    coach = Coach(llm=llm, mode="behavioral", memory_context="", kb_store=kb)

    response = coach.respond("Tell me about system design")
    assert response == "Mock response"
    # System prompt should now contain KB context
    assert "Consistent hashing" in coach.history[0].content


def test_coach_without_kb_store():
    """Test that Coach works fine without KB store."""
    from agentcoach.coach import Coach
    from agentcoach.llm.base import LLMAdapter, Message

    class MockLLM(LLMAdapter):
        def generate(self, messages):
            return "Mock response"

    llm = MockLLM()
    coach = Coach(llm=llm, mode="behavioral", memory_context="")
    # Should not raise
    response = coach.respond("Hello")
    assert response == "Mock response"


def test_coach_kb_search_failure_graceful():
    """Test that KB search failure doesn't break the interview."""
    from agentcoach.coach import Coach
    from agentcoach.llm.base import LLMAdapter, Message

    class MockLLM(LLMAdapter):
        def generate(self, messages):
            return "Mock response"

    class BrokenKBStore:
        def search(self, query, limit=3):
            raise RuntimeError("DB connection failed")

    llm = MockLLM()
    kb = BrokenKBStore()
    coach = Coach(llm=llm, mode="behavioral", memory_context="", kb_store=kb)

    # Should not raise despite KB failure
    response = coach.respond("Tell me about system design")
    assert response == "Mock response"
