# Phase A: Syllabus + Analytics + Mode Router Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build the data layer (syllabus, analytics, recommender) and mode selection UI so users can choose domain + mode, see their progress, and get recommendations.

**Architecture:** YAML syllabi define topic trees with resources. SQLite analytics store tracks per-topic mastery. Recommender uses mastery scores to suggest mode. CLI gets a new startup menu replacing the current auto-start-behavioral flow.

**Tech Stack:** Python 3.9, PyYAML, SQLite, existing LLM/Coach infrastructure

---

### Task 1: Install PyYAML + Create Syllabus Data Model

**Files:**
- Modify: `requirements.txt`
- Create: `agentcoach/syllabus/__init__.py`
- Create: `agentcoach/syllabus/loader.py`
- Create: `tests/test_syllabus.py`

**Step 1: Write the failing test**

```python
# tests/test_syllabus.py
import os
import tempfile
import yaml
from agentcoach.syllabus.loader import SyllabusLoader

SAMPLE_SYLLABUS = {
    "domain": "system_design",
    "name": "System Design",
    "topics": [
        {
            "id": "system_design.core_concepts",
            "name": "Core Concepts",
            "children": [
                {
                    "id": "system_design.caching",
                    "name": "Caching",
                    "resources": [
                        {"type": "video", "title": "Caching Explained", "url": "https://youtube.com/example"},
                        {"type": "article", "title": "Redis Caching Guide", "url": "https://example.com/redis"},
                    ],
                },
                {
                    "id": "system_design.cap_theorem",
                    "name": "CAP Theorem",
                    "resources": [
                        {"type": "article", "title": "CAP Theorem Explained", "url": "https://example.com/cap"},
                    ],
                },
            ],
        },
    ],
}

def _write_sample(tmpdir):
    os.makedirs(os.path.join(tmpdir, "data"))
    path = os.path.join(tmpdir, "data", "system_design.yaml")
    with open(path, "w") as f:
        yaml.dump(SAMPLE_SYLLABUS, f)
    return tmpdir

def test_load_domains(tmp_path):
    _write_sample(str(tmp_path))
    loader = SyllabusLoader(data_dir=os.path.join(str(tmp_path), "data"))
    domains = loader.get_domains()
    assert "system_design" in domains

def test_get_topics(tmp_path):
    _write_sample(str(tmp_path))
    loader = SyllabusLoader(data_dir=os.path.join(str(tmp_path), "data"))
    topics = loader.get_topics("system_design")
    ids = [t["id"] for t in topics]
    assert "system_design.caching" in ids
    assert "system_design.cap_theorem" in ids

def test_get_topic(tmp_path):
    _write_sample(str(tmp_path))
    loader = SyllabusLoader(data_dir=os.path.join(str(tmp_path), "data"))
    topic = loader.get_topic("system_design.caching")
    assert topic is not None
    assert topic["name"] == "Caching"
    assert len(topic["resources"]) == 2

def test_get_resources(tmp_path):
    _write_sample(str(tmp_path))
    loader = SyllabusLoader(data_dir=os.path.join(str(tmp_path), "data"))
    resources = loader.get_resources("system_design.caching")
    assert len(resources) == 2
    assert resources[0]["type"] == "video"

def test_get_topic_not_found(tmp_path):
    _write_sample(str(tmp_path))
    loader = SyllabusLoader(data_dir=os.path.join(str(tmp_path), "data"))
    topic = loader.get_topic("nonexistent")
    assert topic is None
```

**Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_syllabus.py -v`
Expected: FAIL — module not found

**Step 3: Write minimal implementation**

```python
# agentcoach/syllabus/__init__.py
```

```python
# agentcoach/syllabus/loader.py
"""Syllabus loader — reads YAML topic trees with resources."""
import os
import yaml


class SyllabusLoader:
    def __init__(self, data_dir: str = ""):
        if not data_dir:
            data_dir = os.path.join(os.path.dirname(__file__), "data")
        self.data_dir = data_dir
        self._syllabi = {}
        self._topic_index = {}
        self._load_all()

    def _load_all(self):
        if not os.path.isdir(self.data_dir):
            return
        for fname in os.listdir(self.data_dir):
            if not fname.endswith((".yaml", ".yml")):
                continue
            path = os.path.join(self.data_dir, fname)
            with open(path, "r") as f:
                data = yaml.safe_load(f)
            domain = data["domain"]
            self._syllabi[domain] = data
            self._index_topics(data["topics"], domain)

    def _index_topics(self, topics, domain, parent_id=""):
        for topic in topics:
            tid = topic["id"]
            self._topic_index[tid] = {
                "id": tid,
                "name": topic["name"],
                "domain": domain,
                "parent": parent_id,
                "resources": topic.get("resources", []),
            }
            children = topic.get("children", [])
            if children:
                self._index_topics(children, domain, parent_id=tid)

    def get_domains(self) -> list:
        return list(self._syllabi.keys())

    def get_topics(self, domain: str) -> list:
        return [t for t in self._topic_index.values() if t["domain"] == domain]

    def get_topic(self, topic_id: str):
        return self._topic_index.get(topic_id)

    def get_resources(self, topic_id: str) -> list:
        topic = self.get_topic(topic_id)
        if topic is None:
            return []
        return topic["resources"]
```

**Step 4: Install PyYAML and run tests**

```bash
pip3 install pyyaml
```

Add `pyyaml>=6.0` to requirements.txt.

Run: `python3 -m pytest tests/test_syllabus.py -v`
Expected: PASS (5 tests)

**Step 5: Commit**

```bash
git add agentcoach/syllabus/ tests/test_syllabus.py requirements.txt
git commit -m "feat: add SyllabusLoader with YAML topic tree support"
```

---

### Task 2: System Design Syllabus YAML

**Files:**
- Create: `agentcoach/syllabus/data/system_design.yaml`

**Step 1: Write the YAML**

```yaml
domain: system_design
name: System Design

topics:
  - id: system_design.core_concepts
    name: Core Concepts
    children:
      - id: system_design.networking
        name: Networking & Protocols
        resources:
          - type: video
            title: "Computer Networking Full Course (NetworkChuck)"
            url: "https://www.youtube.com/watch?v=IPvYjXCsTg8"
          - type: article
            title: "HelloInterview: Networking"
            url: "https://www.hellointerview.com/learn/system-design/in-a-hurry/core-concepts"

      - id: system_design.api_design
        name: API Design (REST, gRPC, GraphQL)
        resources:
          - type: video
            title: "REST vs gRPC vs GraphQL (ByteByteGo)"
            url: "https://www.youtube.com/watch?v=hkXzsB8D_mo"
          - type: article
            title: "HelloInterview: API Design"
            url: "https://www.hellointerview.com/learn/system-design/in-a-hurry/core-concepts"

      - id: system_design.data_modeling
        name: Data Modeling
        resources:
          - type: book
            title: "DDIA Chapter 2 - Data Models"
            url: null
          - type: video
            title: "Data Modeling for System Design (Gaurav Sen)"
            url: "https://www.youtube.com/watch?v=1jWuFaGJEaQ"

      - id: system_design.caching
        name: Caching (Redis, Memcached)
        resources:
          - type: video
            title: "Caching Strategies (ByteByteGo)"
            url: "https://www.youtube.com/watch?v=dGAgxozNWFE"
          - type: article
            title: "HelloInterview: Caching"
            url: "https://www.hellointerview.com/learn/system-design/deep-dives/redis"
          - type: book
            title: "DDIA Chapter 5 - Replication (Caching context)"
            url: null

      - id: system_design.sharding
        name: Sharding & Partitioning
        resources:
          - type: video
            title: "Database Sharding Explained (Gaurav Sen)"
            url: "https://www.youtube.com/watch?v=5faMjKuB9bc"
          - type: book
            title: "DDIA Chapter 6 - Partitioning"
            url: null

      - id: system_design.consistent_hashing
        name: Consistent Hashing
        resources:
          - type: video
            title: "Consistent Hashing (Gaurav Sen)"
            url: "https://www.youtube.com/watch?v=zaRkONvyGr8"
          - type: article
            title: "Consistent Hashing Explained"
            url: "https://www.toptal.com/big-data/consistent-hashing"

      - id: system_design.cap_theorem
        name: CAP Theorem
        resources:
          - type: video
            title: "CAP Theorem Simplified (ByteByteGo)"
            url: "https://www.youtube.com/watch?v=BHqjEjzAicY"
          - type: book
            title: "DDIA Chapter 9 - Consistency and Consensus"
            url: null

      - id: system_design.db_indexing
        name: Database Indexing
        resources:
          - type: video
            title: "Database Indexing Explained (Hussein Nasser)"
            url: "https://www.youtube.com/watch?v=-qNSXDUhTO8"
          - type: book
            title: "DDIA Chapter 3 - Storage and Retrieval"
            url: null

      - id: system_design.load_balancing
        name: Load Balancing
        resources:
          - type: video
            title: "Load Balancing (Gaurav Sen)"
            url: "https://www.youtube.com/watch?v=K0Ta65OqQkY"
          - type: article
            title: "NGINX Load Balancing Guide"
            url: "https://www.nginx.com/resources/glossary/load-balancing/"

      - id: system_design.message_queues
        name: Message Queues (Kafka)
        resources:
          - type: video
            title: "Apache Kafka in 6 minutes (James Cutajar)"
            url: "https://www.youtube.com/watch?v=Ch5VhJzaoaI"
          - type: article
            title: "HelloInterview: Kafka Deep Dive"
            url: "https://www.hellointerview.com/learn/system-design/deep-dives/kafka"

  - id: system_design.patterns
    name: Patterns
    children:
      - id: system_design.rate_limiting
        name: Rate Limiting
        resources:
          - type: video
            title: "Rate Limiting (System Design)"
            url: "https://www.youtube.com/watch?v=FU4WlwfS3G0"

      - id: system_design.circuit_breaker
        name: Circuit Breaker
        resources:
          - type: article
            title: "Circuit Breaker Pattern (Martin Fowler)"
            url: "https://martinfowler.com/bliki/CircuitBreaker.html"

      - id: system_design.event_sourcing
        name: Event Sourcing / CQRS
        resources:
          - type: video
            title: "Event Sourcing Explained (CodeOpinion)"
            url: "https://www.youtube.com/watch?v=AUj4M-st3ic"

      - id: system_design.leader_election
        name: Leader Election
        resources:
          - type: article
            title: "Leader Election in Distributed Systems"
            url: "https://www.baeldung.com/cs/leader-election"

  - id: system_design.problems
    name: Problem Breakdowns
    children:
      - id: system_design.url_shortener
        name: Design URL Shortener
        resources:
          - type: video
            title: "Design TinyURL (NeetCode)"
            url: "https://www.youtube.com/watch?v=fMZMm_0ZhK4"

      - id: system_design.whatsapp
        name: Design WhatsApp
        resources:
          - type: video
            title: "Design WhatsApp (Gaurav Sen)"
            url: "https://www.youtube.com/watch?v=vvhC64hQZMk"

      - id: system_design.youtube
        name: Design YouTube
        resources:
          - type: video
            title: "Design YouTube (ByteByteGo)"
            url: "https://www.youtube.com/watch?v=jPKTo1iGQiE"

      - id: system_design.uber
        name: Design Uber
        resources:
          - type: video
            title: "Design Uber (Gaurav Sen)"
            url: "https://www.youtube.com/watch?v=umWABit-wbk"
```

**Step 2: Write skeleton YAMLs for other domains**

Create `algorithms.yaml`, `ai_agent.yaml`, `behavioral.yaml` with basic structure (3-5 topics each, resources can be empty for now).

**Step 3: Verify loader works with real data**

```bash
python3 -c "from agentcoach.syllabus.loader import SyllabusLoader; s = SyllabusLoader(); print(s.get_domains()); print(len(s.get_topics('system_design')), 'topics')"
```

**Step 4: Commit**

```bash
git add agentcoach/syllabus/data/
git commit -m "feat: add syllabus YAML data for 4 domains"
```

---

### Task 3: Analytics Store

**Files:**
- Create: `agentcoach/analytics/__init__.py`
- Create: `agentcoach/analytics/store.py`
- Create: `tests/test_analytics.py`

**Step 1: Write the failing test**

```python
# tests/test_analytics.py
import os
import tempfile
from agentcoach.analytics.store import AnalyticsStore

def test_record_and_get_mastery():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test_analytics.db")
        store = AnalyticsStore(db_path=db_path)
        store.record_score("user1", "system_design.caching", +20, "quiz", "Got basics right")
        mastery = store.get_mastery("user1", "system_design.caching")
        assert mastery == 20

def test_mastery_accumulates():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test_analytics.db")
        store = AnalyticsStore(db_path=db_path)
        store.record_score("user1", "system_design.caching", +20, "quiz", "Good")
        store.record_score("user1", "system_design.caching", +15, "reinforce", "Better")
        mastery = store.get_mastery("user1", "system_design.caching")
        assert mastery == 35

def test_mastery_capped_at_100():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test_analytics.db")
        store = AnalyticsStore(db_path=db_path)
        store.record_score("user1", "system_design.caching", +80, "mock", "Great")
        store.record_score("user1", "system_design.caching", +50, "mock", "Perfect")
        mastery = store.get_mastery("user1", "system_design.caching")
        assert mastery == 100

def test_mastery_floor_at_0():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test_analytics.db")
        store = AnalyticsStore(db_path=db_path)
        store.record_score("user1", "system_design.caching", -50, "mock", "Bad")
        mastery = store.get_mastery("user1", "system_design.caching")
        assert mastery == 0

def test_get_progress():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test_analytics.db")
        store = AnalyticsStore(db_path=db_path)
        store.record_score("user1", "system_design.caching", +80, "mock", "Great")
        store.record_score("user1", "system_design.cap_theorem", +40, "quiz", "OK")
        progress = store.get_progress("user1", "system_design")
        assert len(progress) == 2
        assert any(p["topic_id"] == "system_design.caching" and p["mastery"] == 80 for p in progress)

def test_unscored_topic_returns_zero():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test_analytics.db")
        store = AnalyticsStore(db_path=db_path)
        mastery = store.get_mastery("user1", "system_design.caching")
        assert mastery == 0
```

**Step 2: Run test to verify it fails**

**Step 3: Write implementation**

```python
# agentcoach/analytics/__init__.py
```

```python
# agentcoach/analytics/store.py
"""Analytics store — tracks per-topic mastery scores."""
import sqlite3
import os


class AnalyticsStore:
    def __init__(self, db_path: str = ""):
        if not db_path:
            db_path = os.path.expanduser("~/.agentcoach/analytics.db")
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS score_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                topic_id TEXT NOT NULL,
                score_delta INTEGER NOT NULL,
                mode TEXT NOT NULL,
                evidence TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()

    def record_score(self, user_id: str, topic_id: str, score_delta: int,
                     mode: str, evidence: str = ""):
        conn = sqlite3.connect(self.db_path)
        conn.execute(
            "INSERT INTO score_events (user_id, topic_id, score_delta, mode, evidence) VALUES (?, ?, ?, ?, ?)",
            (user_id, topic_id, score_delta, mode, evidence),
        )
        conn.commit()
        conn.close()

    def get_mastery(self, user_id: str, topic_id: str) -> int:
        conn = sqlite3.connect(self.db_path)
        row = conn.execute(
            "SELECT COALESCE(SUM(score_delta), 0) FROM score_events WHERE user_id = ? AND topic_id = ?",
            (user_id, topic_id),
        ).fetchone()
        conn.close()
        raw = row[0] if row else 0
        return max(0, min(100, raw))

    def get_progress(self, user_id: str, domain: str) -> list:
        conn = sqlite3.connect(self.db_path)
        rows = conn.execute(
            "SELECT topic_id, SUM(score_delta) FROM score_events "
            "WHERE user_id = ? AND topic_id LIKE ? GROUP BY topic_id",
            (user_id, f"{domain}.%"),
        ).fetchall()
        conn.close()
        return [
            {"topic_id": r[0], "mastery": max(0, min(100, r[1]))}
            for r in rows
        ]

    def get_history(self, user_id: str, topic_id: str, limit: int = 10) -> list:
        conn = sqlite3.connect(self.db_path)
        rows = conn.execute(
            "SELECT score_delta, mode, evidence, created_at FROM score_events "
            "WHERE user_id = ? AND topic_id = ? ORDER BY created_at DESC LIMIT ?",
            (user_id, topic_id, limit),
        ).fetchall()
        conn.close()
        return [
            {"score_delta": r[0], "mode": r[1], "evidence": r[2], "timestamp": r[3]}
            for r in rows
        ]
```

**Step 4: Run tests**

Run: `python3 -m pytest tests/test_analytics.py -v`
Expected: PASS (6 tests)

**Step 5: Commit**

```bash
git add agentcoach/analytics/ tests/test_analytics.py
git commit -m "feat: add AnalyticsStore for per-topic mastery tracking"
```

---

### Task 4: Recommender

**Files:**
- Create: `agentcoach/analytics/recommender.py`
- Create: `tests/test_recommender.py`

**Step 1: Write the failing test**

```python
# tests/test_recommender.py
import os
import tempfile
from agentcoach.analytics.store import AnalyticsStore
from agentcoach.analytics.recommender import Recommender

# Fake syllabus topics for testing
FAKE_TOPICS = [
    {"id": "sd.caching", "name": "Caching", "domain": "system_design"},
    {"id": "sd.cap", "name": "CAP Theorem", "domain": "system_design"},
    {"id": "sd.sharding", "name": "Sharding", "domain": "system_design"},
]

def test_recommend_learn_for_unstarted():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        store = AnalyticsStore(db_path=db_path)
        rec = Recommender(store)
        suggestion = rec.recommend("user1", FAKE_TOPICS)
        assert suggestion["mode"] == "learn"
        # Should recommend an unstarted topic

def test_recommend_learn_for_low_score():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        store = AnalyticsStore(db_path=db_path)
        store.record_score("user1", "sd.caching", 30, "quiz", "")
        rec = Recommender(store)
        suggestion = rec.recommend("user1", FAKE_TOPICS)
        assert suggestion["topic_id"] == "sd.caching"
        assert suggestion["mode"] == "learn"

def test_recommend_reinforce_for_mid_score():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        store = AnalyticsStore(db_path=db_path)
        store.record_score("user1", "sd.caching", 55, "quiz", "")
        store.record_score("user1", "sd.cap", 55, "quiz", "")
        store.record_score("user1", "sd.sharding", 55, "quiz", "")
        rec = Recommender(store)
        suggestion = rec.recommend("user1", FAKE_TOPICS)
        assert suggestion["mode"] == "reinforce"

def test_recommend_mock_for_high_score():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        store = AnalyticsStore(db_path=db_path)
        store.record_score("user1", "sd.caching", 80, "mock", "")
        store.record_score("user1", "sd.cap", 80, "mock", "")
        store.record_score("user1", "sd.sharding", 80, "mock", "")
        rec = Recommender(store)
        suggestion = rec.recommend("user1", FAKE_TOPICS)
        assert suggestion["mode"] == "mock"
```

**Step 2: Run test to verify it fails**

**Step 3: Write implementation**

```python
# agentcoach/analytics/recommender.py
"""Recommender — suggests what to learn/practice next based on mastery scores."""
from agentcoach.analytics.store import AnalyticsStore


class Recommender:
    LEARN_THRESHOLD = 40
    REINFORCE_THRESHOLD = 70

    def __init__(self, store: AnalyticsStore):
        self.store = store

    def recommend(self, user_id: str, topics: list) -> dict:
        """Recommend next topic + mode based on mastery scores.

        Returns: {"topic_id": str, "topic_name": str, "mode": str, "mastery": int, "reason": str}
        """
        scored = []
        for topic in topics:
            tid = topic["id"]
            mastery = self.store.get_mastery(user_id, tid)
            scored.append({
                "topic_id": tid,
                "topic_name": topic["name"],
                "mastery": mastery,
            })

        # Priority: unstarted > lowest score
        unstarted = [s for s in scored if s["mastery"] == 0]
        if unstarted:
            pick = unstarted[0]
            return {**pick, "mode": "learn", "reason": "Not started yet"}

        # Find lowest scoring topic
        scored.sort(key=lambda x: x["mastery"])
        pick = scored[0]

        if pick["mastery"] < self.LEARN_THRESHOLD:
            return {**pick, "mode": "learn", "reason": f"Score {pick['mastery']}% — needs study"}
        elif pick["mastery"] < self.REINFORCE_THRESHOLD:
            return {**pick, "mode": "reinforce", "reason": f"Score {pick['mastery']}% — needs practice"}
        else:
            # All topics above 70% — recommend mock
            return {**pick, "mode": "mock", "reason": "Ready for mock interview"}
```

**Step 4: Run tests**

Run: `python3 -m pytest tests/test_recommender.py -v`
Expected: PASS (4 tests)

**Step 5: Commit**

```bash
git add agentcoach/analytics/recommender.py tests/test_recommender.py
git commit -m "feat: add Recommender for mode/topic suggestions"
```

---

### Task 5: CLI Mode Selection Menu + Progress View

**Files:**
- Modify: `agentcoach/cli.py`

**Step 1: Rewrite CLI startup to show mode selection**

Replace the current auto-start behavioral flow with a menu:

```
=== AgentCoach — AI Mock Interview Coach ===

Choose a domain:
  1. System Design
  2. Algorithms
  3. AI/Agent
  4. Behavioral

Choose a mode:
  L. Learn — study resources + quiz
  R. Reinforce — strengthen weak topics
  M. Mock — full interview simulation
  (or 'recommend' for Coach's suggestion)

Other commands:
  progress — view your mastery scores
  quit — exit
```

After domain + mode selection, create the appropriate Coach with mode-specific prompt and start the session.

For now, all 3 modes use the existing Coach with different system prompts. The actual mode handlers (Phase B) will replace this.

**Step 2: Add `progress` command**

Shows per-topic mastery for the selected domain using AnalyticsStore + SyllabusLoader:

```
=== System Design Progress ===
  ✅ Caching           82%
  ⚠️  CAP Theorem      45%
  ❌ Sharding          20%
  ❓ Consistent Hashing --
  ...
Overall: 49%
```

**Step 3: Run all tests**

Run: `python3 -m pytest tests/ -v`
Expected: ALL PASS

**Step 4: Commit**

```bash
git add agentcoach/cli.py
git commit -m "feat: add mode selection menu and progress view to CLI"
```

---

### Task 6: Run All Tests + Tag

**Step 1: Full test suite**

```bash
python3 -m pytest tests/ -v
```

Expected: ALL PASS

**Step 2: Manual smoke test**

```bash
python3 -m agentcoach
```

Verify: menu shows → select domain → select mode → interview starts → progress command works.

**Step 3: Tag**

```bash
git tag v0.4.0-phase-a
```

---

## Phase A Complete Checklist

- [ ] SyllabusLoader with YAML topic trees
- [ ] System Design syllabus with real resource links
- [ ] Skeleton syllabi for Algorithms, AI/Agent, Behavioral
- [ ] AnalyticsStore for per-topic mastery tracking
- [ ] Recommender for mode/topic suggestions
- [ ] CLI mode selection menu
- [ ] Progress view command
- [ ] All tests passing
