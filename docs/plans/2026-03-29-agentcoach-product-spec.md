# AgentCoach — Product Specification

## Product Vision

A voice-first AI mock interview coach that helps engineers **quantify their skills, expose weaknesses, and improve through targeted practice**. The core value is mock testing, not knowledge delivery.

## Target User

Software engineers transitioning to AI/Agent Engineer roles. First user: javiswan.

## Core Principle

**AgentCoach is a coach, not a textbook.** It tests you, tells you where you're weak, points you to learning resources, then tests you again. The app never becomes a knowledge library — it stays focused on mock testing + analytics.

---

## Three Modes

| Mode | Purpose | Experience | Duration |
|------|---------|-----------|----------|
| **Learn** | Learn new topics | Coach recommends resources → user studies → quick Quiz to verify | 5-10 min/topic |
| **Reinforce** | Strengthen weak areas | Targeted follow-up questions on low-scoring topics, concept + application | 10-15 min |
| **Mock** | Simulate real interviews | Full interview role-play, interviewer-style follow-ups | 30-45 min |

## Four Domains

1. **System Design** — distributed systems, architecture design
2. **Algorithms** — data structures & algorithms
3. **AI/Agent** — LLM, RAG, agent architecture, evaluation
4. **Behavioral** — STAR framework, project storytelling

---

## Syllabus Structure

Each domain has a structured syllabus of topics. Each topic has:

```python
{
    "id": "system_design.caching",
    "name": "Caching",
    "domain": "system_design",
    "parent": "system_design.core_concepts",
    "resources": [
        {"type": "video", "title": "Caching Explained", "url": "https://youtube.com/..."},
        {"type": "article", "title": "HelloInterview: Caching", "url": "https://hellointerview.com/..."},
        {"type": "book", "title": "DDIA Chapter 5", "url": null},
    ],
    "quiz_questions_count": 5,
    "mock_weight": 0.8,
}
```

### System Design Syllabus (example)

```
System Design
├── Core Concepts
│   ├── Networking & Protocols
│   ├── API Design (REST, gRPC, GraphQL)
│   ├── Data Modeling
│   ├── Caching (Redis, Memcached)
│   ├── Sharding & Partitioning
│   ├── Consistent Hashing
│   ├── CAP Theorem
│   ├── Database Indexing
│   ├── Load Balancing
│   └── Message Queues (Kafka)
├── Patterns
│   ├── Rate Limiting
│   ├── Circuit Breaker
│   ├── Event Sourcing / CQRS
│   └── Leader Election
└── Problem Breakdowns
    ├── Design URL Shortener
    ├── Design WhatsApp
    ├── Design YouTube
    └── Design Uber
```

### Coach Recommendation Logic

- Topic not started → recommend Learn mode
- Topic score < 40% → "Study these resources first, then quiz"
- Topic score 40-70% → recommend Reinforce mode
- Topic score > 70% → ready for Mock

---

## Mode Details

### Learn Mode Flow

1. User selects topic (or Coach recommends lowest/unstarted topic)
2. Coach displays resource list for that topic:
   ```
   "Consistent Hashing — recommended resources:
    📺 YouTube: Consistent Hashing Explained (15min)
    📄 HelloInterview: Consistent Hashing Guide
    📖 DDIA Chapter 6 - Partitioning"
   ```
3. User studies on their own (app waits)
4. User returns and says "ready" to start Quiz
5. Coach asks 3-5 knowledge-check questions:
   - "What is consistent hashing? What problem does it solve?"
   - "When a new node is added, how is data redistributed?"
   - "What do virtual nodes solve?"
6. Coach judges each answer, gives brief correction if wrong
7. Session ends → topic score updated in analytics

### Reinforce Mode Flow

1. User selects topic (or Coach recommends 40-70% topics)
2. Coach knows user has learned but isn't solid. Uses follow-up style:
   - Starts with concept confirmation
   - Then application: "If your DB needs to scale from 3 to 10 nodes, how would you use consistent hashing?"
   - Follow-up on details: "What if a node crashes?"
   - Gradually increases difficulty
3. Deeper than Quiz, more focused than Mock (single topic)
4. Session ends → topic score updated

### Mock Mode Flow

1. User selects domain (System Design / Algorithms / AI-Agent / Behavioral)
2. Coach becomes interviewer, runs full 30-45 min simulation
3. System Design example:
   - "Design a messaging system like WhatsApp"
   - Follow-ups: requirements clarification → high-level design → component deep-dive → scalability → trade-offs
4. Coach uses KB internally to evaluate answer quality (user doesn't see KB)
5. Session ends:
   - Overall score (1-10)
   - Per-topic breakdown scores
   - Specific improvement suggestions
   - Analytics updated

---

## Analytics System

### Per-Topic Mastery Score (0-100)

Scoring sources:

| Behavior | Score Impact | Weight |
|----------|-------------|--------|
| Quiz correct | + | Low (concept level) |
| Quiz wrong | - | Low |
| Reinforce good answer | + | Medium (application level) |
| Reinforce poor answer | - | Medium |
| Mock good performance on topic | + | High (real interview) |
| Mock poor performance on topic | - | High |
| Time since last practice | Slow decay | Low (forgetting curve) |

### Scoring Flow

```
Session ends
    → LLM analyzes conversation
    → Extracts which topics were covered
    → Scores each topic
    → Stores to Analytics DB:
        {
            "user_id": "javiswan",
            "topic_id": "system_design.caching",
            "score_delta": +8,
            "mode": "mock",
            "evidence": "Correctly explained cache invalidation strategies,
                        missed write-through vs write-back distinction",
            "timestamp": "2026-03-29"
        }
```

### User-Facing Progress View

```
=== Your Progress ===
System Design: 58% overall
  ✅ Caching           82%
  ✅ CAP Theorem       75%
  ⚠️ Sharding          45%  ← Coach suggests Reinforce
  ❌ Consistent Hashing 20%  ← Coach suggests Learn first
  ❓ Message Queues     --   ← Not started
```

---

## Technical Architecture

### Project Structure

```
agentcoach/
├── cli.py                  # Mode selection menu + interaction loop
├── coach.py                # Mode-aware coach orchestrator
├── modes/                  # Mode-specific logic
│   ├── learn.py            # Learn: show resources → quiz
│   ├── reinforce.py        # Reinforce: targeted follow-ups
│   └── mock.py             # Mock: full interview simulation
├── syllabus/               # Domain syllabi
│   ├── loader.py           # Load syllabus YAML files
│   └── data/
│       ├── system_design.yaml
│       ├── algorithms.yaml
│       ├── ai_agent.yaml
│       └── behavioral.yaml
├── analytics/              # Scoring + progress tracking
│   ├── scorer.py           # LLM extracts per-topic scores from session
│   ├── store.py            # SQLite score storage + history
│   └── recommender.py      # Recommends what to learn/practice next
├── kb/                     # Knowledge base (Coach internal, not user-facing)
│   ├── store.py
│   ├── chunker.py
│   ├── indexer.py
│   └── embeddings.py
├── memory/                 # User profile, JD, feedback
│   ├── store.py
│   └── importer.py
├── llm/                    # LLM adapters (MiniMax, Gemini, etc.)
│   ├── base.py
│   ├── gemini.py
│   └── openai_compat.py
├── voice/                  # TTS output
│   └── tts.py
└── prompt/                 # Prompt templates per mode
    └── templates.py
```

### Data Flow

```
User selects mode → Mode Router → Mode Handler
                                      ↓
                          Prompt Builder (injects: syllabus + analytics + KB)
                                      ↓
                                  LLM conversation
                                      ↓
                          Session ends → Scorer (LLM extracts topic scores)
                                      ↓
                          Analytics Store updated
                                      ↓
                          Recommender calculates next suggestion
```

### Unchanged Components

- **LLM Adapter** — MiniMax/Gemini switchable
- **KB** — Coach internal use, evaluates answer quality
- **Memory** — User profile, JD, preferences
- **Voice** — Superwhisper input + TTS output

---

## Tech Stack

| Layer | Choice |
|-------|--------|
| Language | Python 3.9+ |
| LLM | MiniMax M2.7 (switchable) |
| Voice Input | Superwhisper (macOS native) |
| Voice Output | macOS say (default) / Qwen3-TTS (optional) |
| KB Search | SQLite FTS5 (BM25) + Ollama qwen3-embedding:8b |
| Analytics DB | SQLite |
| Syllabus | YAML files |
| Frontend | Terminal CLI (MVP) → Web/Mobile (future) |
