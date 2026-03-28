# AgentCoach — AI Mock Interview Coach for Engineers

## Product Vision

A voice-first AI interview coach for SWEs transitioning to AI/Agent Engineer roles. Personalized mock interviews based on your real experience, target JDs, and industry trends.

## Core Value

Not a question bank — a coach that **knows you, challenges you, and tracks your growth**.

## Target User

SWE preparing for AI/Agent Engineer interviews. First user: javiswan.

## Tech Stack

| Layer | Choice | Rationale |
|-------|--------|-----------|
| Voice Input | Superwhisper (macOS) | Already available, native experience |
| Voice Output | Qwen3-TTS (0.6B) | Open-source, free, Chinese+English |
| AI Engine | Gemini (switchable) | Start here, architecture supports Claude/GPT |
| Memory | agentmem (SQLite+FTS5) | Local, fast, TTL/priority, MCP native |
| Future: Doc RAG | PageIndex | For reading books/tech blogs later |
| Frontend | Terminal CLI (MVP) | Fastest to ship |
| Language | Python | Best ecosystem for TTS/memory/AI |

## Architecture

```
Terminal CLI
    ├── Superwhisper (voice → text)
    ├── Qwen3-TTS (text → voice)
    └── Coach Engine
        ├── Session Manager (interview state machine)
        ├── Prompt Builder (JD + background + memory → prompt)
        ├── LLM Adapter (Gemini/Claude/GPT switchable)
        └── Feedback Engine (scoring + improvement suggestions)
            └── agentmem (SQLite + FTS5)
                ├── User profile (resume, projects)
                ├── JD analysis
                ├── Interview records
                ├── Weakness tracking
                └── Progress curve
```

## Interview Modes

1. **Behavioral** — STAR framework, project deep-dives, follow-up questions
2. **System Design** — Architecture problems, trade-off discussions, scaling
3. **Coding** — Algorithm problems with verbal walkthrough
4. **AI/Agent** — LLM fundamentals, agent architecture, RAG, fine-tuning, evaluation

## MVP Phases

### Phase 1 — Skeleton (minimal loop)
- Project init + git
- LLM Adapter (Gemini)
- CLI basic interaction: text in → Gemini reply
- Hardcoded behavioral interview prompt

### Phase 2 — Memory + Personalization
- Integrate agentmem
- Resume/project import
- JD parsing + storage
- Prompt Builder assembles context from memory

### Phase 3 — Voice
- Superwhisper input integration
- Qwen3-TTS output integration
- Voice conversation loop

### Phase 4 — Interview Quality
- 4 interview mode prompt templates
- Follow-up logic + difficulty progression
- Feedback scoring system
- Weakness tracking + targeted training

## Key Design Decisions

- **LLM Adapter abstraction**: `generate(messages) → response`, swap providers without touching business logic
- **Prompt Builder**: retrieves relevant memory before each question, injects into system prompt
- **Session Manager**: state machine (intro → question → follow-up → summary → feedback)
- **All local except LLM API calls**: privacy-first
