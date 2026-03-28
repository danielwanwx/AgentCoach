# Phase 1: AgentCoach Skeleton Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Get a working terminal loop where you speak a question topic, Gemini acts as an interview coach, and you can have a back-and-forth mock interview conversation.

**Architecture:** CLI main loop → LLM Adapter (Gemini) → print response. Simple stateless conversation with system prompt defining coach persona. No memory, no voice yet — just the text skeleton.

**Tech Stack:** Python 3.9+, google-generativeai SDK, pytest

---

### Task 1: Project Setup

**Files:**
- Create: `requirements.txt`
- Create: `agentcoach/__init__.py`
- Create: `tests/__init__.py`
- Create: `.gitignore`

**Step 1: Create .gitignore**

```
__pycache__/
*.pyc
.env
*.egg-info/
dist/
build/
.venv/
```

**Step 2: Create requirements.txt**

```
google-generativeai>=0.8.0
pytest>=8.0
python-dotenv>=1.0
```

**Step 3: Create package dirs**

```bash
mkdir -p agentcoach tests
touch agentcoach/__init__.py tests/__init__.py
```

**Step 4: Install dependencies**

```bash
pip3 install -r requirements.txt
```

**Step 5: Commit**

```bash
git add .gitignore requirements.txt agentcoach/__init__.py tests/__init__.py
git commit -m "chore: project setup with dependencies"
```

---

### Task 2: LLM Adapter — Base Interface

**Files:**
- Create: `tests/test_llm.py`
- Create: `agentcoach/llm/base.py`
- Create: `agentcoach/llm/__init__.py`

**Step 1: Write the failing test**

```python
# tests/test_llm.py
from agentcoach.llm.base import LLMAdapter, Message

def test_message_creation():
    msg = Message(role="user", content="hello")
    assert msg.role == "user"
    assert msg.content == "hello"

def test_adapter_is_abstract():
    """LLMAdapter cannot be instantiated directly."""
    import pytest
    with pytest.raises(TypeError):
        LLMAdapter()
```

**Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_llm.py -v`
Expected: FAIL — module not found

**Step 3: Write minimal implementation**

```python
# agentcoach/llm/__init__.py
```

```python
# agentcoach/llm/base.py
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Message:
    role: str  # "system", "user", "assistant"
    content: str


class LLMAdapter(ABC):
    @abstractmethod
    def generate(self, messages: list[Message]) -> str:
        """Send messages, return assistant response text."""
        ...
```

**Step 4: Run test to verify it passes**

Run: `python3 -m pytest tests/test_llm.py -v`
Expected: PASS (2 tests)

**Step 5: Commit**

```bash
git add agentcoach/llm/ tests/test_llm.py
git commit -m "feat: add LLM adapter base interface"
```

---

### Task 3: LLM Adapter — Gemini Implementation

**Files:**
- Create: `agentcoach/llm/gemini.py`
- Create: `.env` (NOT committed)
- Modify: `tests/test_llm.py`

**Step 1: Write the failing test**

Append to `tests/test_llm.py`:

```python
from unittest.mock import patch, MagicMock
from agentcoach.llm.gemini import GeminiAdapter

def test_gemini_adapter_generate():
    """GeminiAdapter calls Gemini API and returns text."""
    mock_model = MagicMock()
    mock_response = MagicMock()
    mock_response.text = "Tell me about your experience."
    mock_model.generate_content.return_value = mock_response

    with patch("agentcoach.llm.gemini.genai") as mock_genai:
        mock_genai.GenerativeModel.return_value = mock_model
        adapter = GeminiAdapter(api_key="fake-key", model="gemini-2.0-flash")
        result = adapter.generate([
            Message(role="system", content="You are an interview coach."),
            Message(role="user", content="Start the interview."),
        ])

    assert result == "Tell me about your experience."
    mock_model.generate_content.assert_called_once()
```

**Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_llm.py::test_gemini_adapter_generate -v`
Expected: FAIL — module not found

**Step 3: Write minimal implementation**

```python
# agentcoach/llm/gemini.py
import google.generativeai as genai
from agentcoach.llm.base import LLMAdapter, Message


class GeminiAdapter(LLMAdapter):
    def __init__(self, api_key: str, model: str = "gemini-2.0-flash"):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model)

    def generate(self, messages: list[Message]) -> str:
        # Gemini uses a different format: system instruction + contents
        system_parts = []
        contents = []
        for msg in messages:
            if msg.role == "system":
                system_parts.append(msg.content)
            elif msg.role == "user":
                contents.append({"role": "user", "parts": [msg.content]})
            elif msg.role == "assistant":
                contents.append({"role": "model", "parts": [msg.content]})

        if system_parts:
            self.model = genai.GenerativeModel(
                self.model.model_name,
                system_instruction="\n".join(system_parts),
            )

        response = self.model.generate_content(contents)
        return response.text
```

**Step 4: Run test to verify it passes**

Run: `python3 -m pytest tests/test_llm.py -v`
Expected: PASS (3 tests)

**Step 5: Create .env (do NOT commit)**

```
GEMINI_API_KEY=your-key-here
```

**Step 6: Commit**

```bash
git add agentcoach/llm/gemini.py tests/test_llm.py
git commit -m "feat: add Gemini LLM adapter"
```

---

### Task 4: Coach System Prompt

**Files:**
- Create: `agentcoach/prompt/__init__.py`
- Create: `agentcoach/prompt/templates.py`
- Create: `tests/test_prompt.py`

**Step 1: Write the failing test**

```python
# tests/test_prompt.py
from agentcoach.prompt.templates import get_coach_system_prompt

def test_behavioral_system_prompt():
    prompt = get_coach_system_prompt("behavioral")
    assert "interview" in prompt.lower()
    assert "behavioral" in prompt.lower()
    assert len(prompt) > 100  # non-trivial prompt

def test_unknown_mode_raises():
    import pytest
    with pytest.raises(ValueError):
        get_coach_system_prompt("unknown_mode")
```

**Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_prompt.py -v`
Expected: FAIL

**Step 3: Write minimal implementation**

```python
# agentcoach/prompt/__init__.py
```

```python
# agentcoach/prompt/templates.py

BEHAVIORAL_PROMPT = """You are an expert behavioral interview coach for software engineering positions, especially for engineers transitioning into AI/Agent Engineer roles.

Your job is to conduct a realistic mock behavioral interview. Follow these rules:

1. Start by briefly introducing yourself and asking the candidate what role they're targeting.
2. Ask ONE behavioral question at a time using the STAR framework (Situation, Task, Action, Result).
3. Listen to the candidate's answer, then ask 1-2 follow-up questions to dig deeper — just like a real interviewer would.
4. After 3-4 questions, provide a summary with:
   - What they did well
   - Specific areas to improve
   - A score from 1-10 with justification
5. Be encouraging but honest. Push them to be specific and quantitative.
6. Vary your questions across: leadership, conflict resolution, technical decision-making, failure/learning, and collaboration.

Speak naturally and conversationally, like a friendly but rigorous interviewer. Keep responses concise — this is a conversation, not a lecture."""

TEMPLATES = {
    "behavioral": BEHAVIORAL_PROMPT,
}

def get_coach_system_prompt(mode: str) -> str:
    if mode not in TEMPLATES:
        raise ValueError(f"Unknown mode: {mode}. Available: {list(TEMPLATES.keys())}")
    return TEMPLATES[mode]
```

**Step 4: Run test to verify it passes**

Run: `python3 -m pytest tests/test_prompt.py -v`
Expected: PASS (2 tests)

**Step 5: Commit**

```bash
git add agentcoach/prompt/ tests/test_prompt.py
git commit -m "feat: add behavioral interview system prompt template"
```

---

### Task 5: Coach Engine — Session Loop

**Files:**
- Create: `agentcoach/coach.py`
- Create: `tests/test_coach.py`

**Step 1: Write the failing test**

```python
# tests/test_coach.py
from unittest.mock import MagicMock
from agentcoach.coach import Coach
from agentcoach.llm.base import Message

def test_coach_start_sends_system_prompt():
    mock_llm = MagicMock()
    mock_llm.generate.return_value = "Hi! What role are you targeting?"

    coach = Coach(llm=mock_llm, mode="behavioral")
    response = coach.start()

    assert response == "Hi! What role are you targeting?"
    call_args = mock_llm.generate.call_args[0][0]
    assert call_args[0].role == "system"
    assert "behavioral" in call_args[0].content.lower()

def test_coach_respond_maintains_history():
    mock_llm = MagicMock()
    mock_llm.generate.side_effect = [
        "Hi! What role?",
        "Great. Tell me about a time you led a project.",
    ]

    coach = Coach(llm=mock_llm, mode="behavioral")
    coach.start()
    response = coach.respond("I'm targeting AI Engineer roles.")

    assert response == "Great. Tell me about a time you led a project."
    # Should have system + user greeting + assistant + user response = 4 messages
    call_args = mock_llm.generate.call_args[0][0]
    assert len(call_args) == 4
```

**Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_coach.py -v`
Expected: FAIL

**Step 3: Write minimal implementation**

```python
# agentcoach/coach.py
from agentcoach.llm.base import LLMAdapter, Message
from agentcoach.prompt.templates import get_coach_system_prompt


class Coach:
    def __init__(self, llm: LLMAdapter, mode: str = "behavioral"):
        self.llm = llm
        self.mode = mode
        system_prompt = get_coach_system_prompt(mode)
        self.history: list[Message] = [Message(role="system", content=system_prompt)]

    def start(self) -> str:
        """Start the interview session. Returns coach's opening message."""
        response = self.llm.generate(self.history)
        self.history.append(Message(role="assistant", content=response))
        return response

    def respond(self, user_input: str) -> str:
        """Send user's answer, get coach's next question/feedback."""
        self.history.append(Message(role="user", content=user_input))
        response = self.llm.generate(self.history)
        self.history.append(Message(role="assistant", content=response))
        return response
```

**Step 4: Run test to verify it passes**

Run: `python3 -m pytest tests/test_coach.py -v`
Expected: PASS (2 tests)

**Step 5: Commit**

```bash
git add agentcoach/coach.py tests/test_coach.py
git commit -m "feat: add Coach engine with conversation history"
```

---

### Task 6: CLI Entry Point

**Files:**
- Create: `agentcoach/cli.py`

**Step 1: Write the CLI**

```python
# agentcoach/cli.py
import os
import sys
from dotenv import load_dotenv
from agentcoach.llm.gemini import GeminiAdapter
from agentcoach.coach import Coach


def main():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: Set GEMINI_API_KEY in .env or environment")
        sys.exit(1)

    print("=== AgentCoach — AI Mock Interview Coach ===")
    print("Mode: Behavioral Interview")
    print("Type 'quit' to exit, 'feedback' for session summary")
    print()

    llm = GeminiAdapter(api_key=api_key)
    coach = Coach(llm=llm, mode="behavioral")

    # Start interview
    opening = coach.start()
    print(f"Coach: {opening}\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nSession ended.")
            break

        if not user_input:
            continue
        if user_input.lower() == "quit":
            print("Session ended. Good luck with your interviews!")
            break

        response = coach.respond(user_input)
        print(f"\nCoach: {response}\n")


if __name__ == "__main__":
    main()
```

**Step 2: Manual test**

```bash
# Make sure .env has your GEMINI_API_KEY
python3 -m agentcoach.cli
```

Expected: Coach greets you, you can type answers, coach responds with follow-ups.

**Step 3: Commit**

```bash
git add agentcoach/cli.py
git commit -m "feat: add CLI entry point for interactive mock interview"
```

---

### Task 7: Run All Tests + Final Commit

**Step 1: Run full test suite**

```bash
python3 -m pytest tests/ -v
```

Expected: ALL PASS (5 tests)

**Step 2: Manual smoke test**

```bash
python3 -m agentcoach.cli
```

Verify: Coach starts interview → you answer → coach follows up → conversation works.

**Step 3: Tag Phase 1**

```bash
git tag v0.1.0-phase1
```

---

## Phase 1 Complete Checklist

- [ ] Project structure with dependencies
- [ ] LLM Adapter interface + Gemini implementation
- [ ] Behavioral interview system prompt
- [ ] Coach engine with conversation history
- [ ] CLI interactive loop
- [ ] All tests passing
- [ ] Manual smoke test working
