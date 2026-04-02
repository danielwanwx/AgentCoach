# Phase 2: Memory + Personalization Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Integrate agentmem for persistent memory so the Coach knows the user's background, resume, target JDs, and past interview performance across sessions.

**Architecture:** agentmem stores user profile + JD + session feedback. Prompt Builder retrieves relevant memory before each LLM call and injects it into the system prompt. Coach becomes personalized.

**Tech Stack:** agentmem (SQLite+FTS5), existing Coach engine, Prompt Builder

---

### Task 1: Install agentmem + Verify

**Files:**
- Modify: `requirements.txt`

**Step 1: Install agentmem**

```bash
pip3 install agentmem
```

**Step 2: Verify it works**

```bash
python3 -c "from agentmem.store import MemoryStore; print('agentmem OK')"
```

**Step 3: Update requirements.txt** — add `agentmem>=0.1.0`

**Step 4: Commit**

```bash
git add requirements.txt
git commit -m "chore: add agentmem dependency"
```

---

### Task 2: Memory Store Wrapper

**Files:**
- Create: `agentcoach/memory/__init__.py`
- Create: `agentcoach/memory/store.py`
- Create: `tests/test_memory.py`

**Step 1: Write the failing test**

```python
# tests/test_memory.py
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
```

**Step 2: Run test to verify it fails**

**Step 3: Write implementation**

```python
# agentcoach/memory/__init__.py
```

```python
# agentcoach/memory/store.py
"""Coach memory layer — wraps agentmem or falls back to simple SQLite FTS5."""
import sqlite3
import os


class CoachMemory:
    def __init__(self, db_path: str = ""):
        if not db_path:
            db_path = os.path.expanduser("~/.agentcoach/memory.db")
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS memories_fts
            USING fts5(content, category, content=memories, content_rowid=id)
        """)
        # Triggers to keep FTS in sync
        conn.execute("""
            CREATE TRIGGER IF NOT EXISTS memories_ai AFTER INSERT ON memories BEGIN
                INSERT INTO memories_fts(rowid, content, category)
                VALUES (new.id, new.content, new.category);
            END
        """)
        conn.commit()
        conn.close()

    def _save(self, category: str, content: str):
        conn = sqlite3.connect(self.db_path)
        conn.execute("INSERT INTO memories (category, content) VALUES (?, ?)", (category, content))
        conn.commit()
        conn.close()

    def save_profile(self, content: str):
        self._save("profile", content)

    def save_jd(self, content: str):
        self._save("jd", content)

    def save_feedback(self, content: str):
        self._save("feedback", content)

    def search(self, query: str, limit: int = 5) -> list:
        conn = sqlite3.connect(self.db_path)
        rows = conn.execute(
            "SELECT content FROM memories_fts WHERE memories_fts MATCH ? LIMIT ?",
            (query, limit)
        ).fetchall()
        conn.close()
        return [row[0] for row in rows]

    def get_context(self) -> str:
        """Get all stored memory as formatted context for prompt injection."""
        conn = sqlite3.connect(self.db_path)
        sections = []
        for category, label in [("profile", "User Profile"), ("jd", "Target JD"), ("feedback", "Past Feedback")]:
            rows = conn.execute(
                "SELECT content FROM memories WHERE category = ? ORDER BY created_at DESC LIMIT 5",
                (category,)
            ).fetchall()
            if rows:
                items = "\n".join(f"- {r[0]}" for r in rows)
                sections.append(f"### {label}\n{items}")
        conn.close()
        return "\n\n".join(sections)
```

**Step 4: Run tests to verify they pass**

**Step 5: Commit**

```bash
git add agentcoach/memory/ tests/test_memory.py
git commit -m "feat: add CoachMemory with SQLite FTS5 for profile/JD/feedback storage"
```

---

### Task 3: Prompt Builder with Memory Context

**Files:**
- Modify: `agentcoach/prompt/templates.py`
- Create: `tests/test_prompt_builder.py`

**Step 1: Write the failing test**

```python
# tests/test_prompt_builder.py
from agentcoach.prompt.templates import build_system_prompt

def test_build_prompt_with_context():
    context = "### User Profile\n- SWE, 5 years Python"
    prompt = build_system_prompt("behavioral", context)
    assert "behavioral" in prompt.lower()
    assert "SWE" in prompt
    assert "Python" in prompt

def test_build_prompt_without_context():
    prompt = build_system_prompt("behavioral", "")
    assert "behavioral" in prompt.lower()
    assert "User Profile" not in prompt
```

**Step 2: Run to verify failure**

**Step 3: Add `build_system_prompt` to templates.py**

Add this function to the existing `agentcoach/prompt/templates.py`:

```python
def build_system_prompt(mode: str, memory_context: str = "") -> str:
    base = get_coach_system_prompt(mode)
    if not memory_context:
        return base
    return f"{base}\n\n## What You Know About This Candidate\n\n{memory_context}"
```

**Step 4: Run tests**

**Step 5: Commit**

```bash
git add agentcoach/prompt/templates.py tests/test_prompt_builder.py
git commit -m "feat: add build_system_prompt with memory context injection"
```

---

### Task 4: Wire Memory into Coach + CLI

**Files:**
- Modify: `agentcoach/coach.py`
- Modify: `agentcoach/cli.py`

**Step 1: Update Coach to accept memory context**

In `coach.py`, modify `__init__` to use `build_system_prompt`:

```python
from agentcoach.prompt.templates import build_system_prompt

class Coach:
    def __init__(self, llm, mode="behavioral", memory_context=""):
        self.llm = llm
        self.mode = mode
        system_prompt = build_system_prompt(mode, memory_context)
        self.history = [Message(role="system", content=system_prompt)]
```

**Step 2: Update CLI to load memory and support commands**

Add memory import, load context before creating Coach. Add commands:
- `import resume <text>` — save profile
- `import jd <text>` — save JD
- `memory` — show current memory

**Step 3: Run all tests**

**Step 4: Commit**

```bash
git add agentcoach/coach.py agentcoach/cli.py
git commit -m "feat: wire memory into Coach and CLI with import commands"
```

---

### Task 5: Resume + JD Import from File

**Files:**
- Modify: `agentcoach/cli.py`
- Create: `agentcoach/memory/importer.py`

**Step 1: Create importer that reads files**

```python
# agentcoach/memory/importer.py
import os

def import_file(filepath: str) -> str:
    filepath = os.path.expanduser(filepath)
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    with open(filepath, "r") as f:
        return f.read().strip()
```

**Step 2: Add CLI commands**

- `load resume <filepath>` — read file, save as profile
- `load jd <filepath>` — read file, save as JD

**Step 3: Test with a sample file**

**Step 4: Commit**

```bash
git add agentcoach/memory/importer.py agentcoach/cli.py
git commit -m "feat: add file import for resume and JD"
```

---

### Task 6: Post-Session Feedback Auto-Save

**Files:**
- Modify: `agentcoach/coach.py`
- Modify: `agentcoach/cli.py`

**Step 1: Add feedback generation to Coach**

Add a `get_feedback_summary` method that asks the LLM to summarize strengths/weaknesses from the session.

**Step 2: On 'quit', auto-generate and save feedback to memory**

**Step 3: Run all tests**

**Step 4: Commit**

```bash
git add agentcoach/coach.py agentcoach/cli.py
git commit -m "feat: auto-save session feedback to memory on quit"
```

---

### Task 7: Run All Tests + Tag

**Step 1: Run full test suite**

```bash
python3 -m pytest tests/ -v
```

**Step 2: Tag**

```bash
git tag v0.2.0-phase2
```

---

## Phase 2 Complete Checklist

- [ ] agentmem/SQLite FTS5 memory store
- [ ] Profile, JD, feedback storage + search
- [ ] Prompt Builder injects memory context
- [ ] CLI commands: import resume/JD, view memory
- [ ] File import for resume/JD
- [ ] Auto-save feedback after sessions
- [ ] All tests passing
