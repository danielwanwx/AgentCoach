# AI-Native Engineer Coach Harness Design

Date: 2026-06-08

## Product Positioning

AgentCoach is an agentic coach for experienced software engineers who want to
transition into AI-native roles: AI Engineer, Agentic Engineer, Forward
Deployed Engineer (FDE), Applied AI Engineer, or AI platform/product engineer.

The product is not a NotebookLM clone, a HelloInterview clone, or a generic AI
mock interviewer. Those products solve adjacent problems:

- NotebookLM organizes and generates artifacts from sources.
- HelloInterview teaches interview content.
- AI mock interviewers simulate interviews and produce feedback.

AgentCoach's core job is different: diagnose a learner's current engineering
model, map it against current AI-native role expectations, run deliberate
practice, and advance mastery only when the learner can produce evidence under
pressure.

The product promise:

> Convert an experienced SWE's existing engineering base into AI-native
> interview readiness through diagnosis, deliberate practice, role intelligence,
> and evidence-backed mastery.

## Target Users

Primary users:

- Backend, full-stack, infra, platform, or data engineers moving toward AI
  Engineer or Applied AI Engineer roles.
- Traditional SDE/SWE candidates who still need system design, behavioral, and
  communication practice, but now need AI-era extensions.
- Engineers targeting FDE, AI deployment, solutions engineering, or applied AI
  roles where customer discovery, production deployment, and business impact
  matter.
- Engineers who know how to ship software but feel uncertain about LLM apps,
  RAG, agents, evaluation, and AI production constraints.

The emotional problem is not only "I need interview prep." It is:

- "Do my existing SWE skills still matter?"
- "What exactly do AI Engineer and FDE roles require?"
- "How do I prove I can build and deploy AI systems, not just talk about AI?"
- "How do I explain my old work in a way that maps to AI-native roles?"

## External Role Research Summary

The role market shows strong demand for people who bridge software engineering,
AI application development, production deployment, and customer/business
judgment.

Observed role families:

1. Forward Deployed AI Engineer / FDE
   - Examples: OpenAI, Anthropic, Snowflake, Scale AI, Databricks.
   - Pattern: customer discovery, technical scoping, system design, building,
     production rollout, adoption, eval-driven feedback, and business impact.

2. Applied AI / Product AI Engineer
   - Examples: OpenAI Codex, Anthropic Product Engineer, Tako, 360Learning,
     Newfront.
   - Pattern: shipping LLM or agent-powered product features with production
     code, retrieval, tools, evals, latency/cost/reliability judgment, and
     product sense.

3. Agentic Systems Engineer
   - Examples: BLEN, Unify Consulting, Snowflake, Scale AI, Supernal.
   - Pattern: agent runtime, tool integrations, workflow orchestration, MCP or
     equivalent tool standards, observability, guardrails, and failure analysis.

High-frequency requirement clusters:

- Core SWE: Python, TypeScript, backend APIs, full-stack shipping, distributed
  systems, data modeling, cloud, security.
- LLM application engineering: prompting, structured outputs, model APIs, model
  routing, context construction, latency and cost control.
- RAG and retrieval: embeddings, vector databases, retrieval quality, chunking,
  reranking, grounding, document workflows.
- Agentic engineering: tool calling, planner/executor split, multi-step
  workflows, memory/context, MCP/tool standards, orchestration, human-in-the-loop.
- Evaluation: golden datasets, eval harnesses, offline and online evals, failure
  taxonomy, regression tests, observability.
- Productionization: deployment, monitoring, MLOps/LLMOps, traces, guardrails,
  security, compliance, enterprise constraints.
- FDE/customer skill: discovery, scoping, business outcome mapping, technical
  advising, demo narrative, stakeholder communication.
- Behavioral/leadership: ambiguity, agency, low ego, collaboration, clear
  trade-off decisions under pressure.

Representative sources reviewed:

- OpenAI FDE: end-to-end customer deployment, scoping, system design,
  production rollout, measurable workflow impact, eval-driven feedback.
  https://openai.com/careers/forward-deployed-engineer-%28fde%29-sf-san-francisco/
- OpenAI Applied AI Engineer, Codex Core Agent: agent behavior, long-horizon
  workflows, evals, tool-use strategies, context construction, production
  feedback loops.
  https://openai.com/careers/applied-ai-engineer-codex-core-agent-san-francisco/
- Anthropic FDE and Product Engineer: production LLMs, agent development,
  evaluation frameworks, customer discovery, architecture guidance.
  https://www.anthropic.com/careers/jobs/4985877008
  https://www.anthropic.com/careers/jobs/5039498008
- Snowflake Applied AI FDE: RAG, agentic workflows, eval loops, golden datasets,
  observability, safety guardrails, production traces.
  https://careers.snowflake.com/
- Scale AI Frontier Agents / Forward Deployed AI Engineer: customer
  integration, data pipelines, custom AI solutions, multi-agent systems, eval
  frameworks.
  https://scale.com/careers/4694861005
- Databricks AI Engineer - FDE: GenAI applications, RAG, multi-agent systems,
  Text2SQL, fine-tuning, LLMOps, production-grade GenAI deployment.
  https://www.builtinsf.com/job/ai-engineer-fde-forward-deployed-engineer/9415140
- Tako Applied AI Engineer: AI infrastructure, MLOps, cloud/containerization,
  LLMs, RAG, vector databases.
  https://builtin.com/job/applied-ai-engineer-san-francisco/7311546
- LinkedIn 2026 labor market signal: AI Engineers and Forward-Deployed Engineers
  are highlighted as AI-enabled role categories where technical and human
  strengths combine.
  https://news.linkedin.com/2026/2026-Davos-Press-Release

LinkedIn-specific caveat: large-scale direct LinkedIn crawling requires login
and is likely restricted. First versions should rely on public company career
pages, user-pasted job descriptions, public search snippets, and configurable
job-source adapters rather than assuming full LinkedIn ingestion.

## Core Product Thesis

AgentCoach should make the learner feel like a serious coach is diagnosing and
training them, not like an AI assistant is organizing reading material.

The product should lead with:

1. Fast topic sniffing.
2. Diagnostic probes.
3. Role-transition diagnosis.
4. Training plan generation.
5. Evidence-based practice loops.
6. Retesting until stable.

The product should not lead with:

1. A library.
2. A study guide.
3. A generated roadmap.
4. A NotebookLM workspace.
5. A broad chat box.

## User Experience

### First Screen

The first screen asks for one input:

- A topic: "consistent hashing", "RAG evals", "agent memory".
- A pasted content fragment from HelloInterview, DDIA, a job description, a
  forum post, or a company role description.
- A role goal: "I want to prepare for OpenAI FDE", "I want to move from backend
  engineer to AI Engineer."

Optional context:

- Target role: AI Engineer, Agentic Engineer, FDE, Applied AI Engineer, SWE AI
  Platform.
- Target company.
- Target level.
- Interview deadline.
- Existing background: backend, infra, full-stack, data, ML, product-facing.

### Flow

```text
User pastes topic/content
  -> Topic Sniff
  -> Diagnostic Probes
  -> LearnerDiagnosis
  -> Role Intelligence Mapping
  -> Research Adapter Registry
  -> SourceManifest
  -> HarnessPlan
  -> HarnessRuntime
  -> EvidenceEvent
  -> MasteryLedger
  -> NextAction
```

### Step 1: Topic Sniff

This is a fast internal classification step, not full research.

It decides:

- What topic is being discussed?
- Is it a standard syllabus topic?
- Is it a pasted learning fragment, role requirement, or interview prompt?
- Which domain does it belong to?
- Which role track is relevant?
- Is there enough confidence to generate diagnostic probes?

Domain candidates:

- SWE baseline
- system design
- behavioral
- coding / LLD / debugging
- AI application engineering
- RAG / retrieval
- agentic systems
- AI eval / observability
- FDE / customer deployment

### Step 2: Diagnostic Probes

The coach should not immediately teach. It first asks 3 diagnostic probes by
default and at most 5.

Probe types:

- True/false: catches conceptual boundary errors.
- Multiple choice: tests trade-off and architecture selection.
- Short answer: tests whether the learner can explain in their own words.
- Micro-scenario: tests transfer into a realistic AI/SDE/FDE situation.

Example for "rate limiter":

- True/false: "A token bucket always guarantees fair per-user distribution."
- Choice: "For an LLM gateway, which rate limit dimension is most likely to
  protect cost: requests, tokens, tenants, or IPs?"
- Short answer: "Explain one failure mode if retries ignore rate limits."

The probes should reveal whether the user lacks:

- definition
- mechanism
- trade-off
- failure mode
- transfer to AI-native system
- interview communication
- FDE/customer framing

### Step 3: Learner Diagnosis

The diagnosis should be concise and actionable. It should not be a grade report
dump.

Fields:

- `concept_level`: `unknown`, `fuzzy`, `usable`, `interview_ready`
- `current_base`: backend, full-stack, infra, data, ML, product-facing, unknown
- `target_role`: AI Engineer, Agentic Engineer, FDE, Applied AI Engineer,
  SWE AI Platform
- `swe_base_strengths`: existing skills that transfer
- `ai_native_gaps`: missing AI-specific skills
- `fde_gaps`: missing customer/deployment/business framing
- `interview_gaps`: missing communication or pressure behavior
- `next_training_focus`: one to three concrete focus areas

### Step 4: Research and Tool Preparation

Research starts after diagnosis. This preserves the product identity: the coach
trains first and uses tools to prepare better practice.

First phase:

- Local KB is real.
- External adapters are defined and stubbed.
- NotebookLM is optional and asynchronous.

Future adapters:

- Company role intelligence adapter.
- Job board adapter.
- User-pasted JD adapter.
- Interview intelligence adapter.
- YouTube transcript adapter.
- Hot-topic trend adapter.
- NotebookLM artifact adapter.

### Step 5: Harness Plan

The plan is not a course syllabus. It is a training protocol.

Stages:

1. Learn: repair the mental model only if needed.
2. Recall: closed-book explanation.
3. Drill: targeted questions against one gap.
4. Transfer: apply the concept in an AI/SDE/FDE scenario.
5. Mock: pressure simulation with interviewer follow-ups.
6. Retest: revisit the same weak point after feedback.

The user-facing surface should show a compact coach brief and the next action.
Full provenance, sources, and adapter outputs can be available in a secondary
view or API payload.

### Step 6: Evidence-Based Mastery

Mastery should not move because the learner read a source or received a plan.
It moves when the learner produces evidence.

Evidence examples:

- Correct diagnostic answer.
- Clear closed-book explanation.
- Correct trade-off selection.
- Recovery after pushback.
- Successful transfer to an AI-native scenario.
- Clear FDE customer-facing framing.
- Passing retest after a previous mistake.

## Role Intelligence Layer

The Role Intelligence layer turns job market requirements into training
targets. It should be a first-class product module, not a static paragraph in a
prompt.

Suggested modules:

- `agentcoach/roles/schema.py`
- `agentcoach/roles/taxonomy.py`
- `agentcoach/roles/adapters/base.py`
- `agentcoach/roles/adapters/local_profiles.py`
- `agentcoach/roles/adapters/job_description.py`
- `agentcoach/roles/adapters/public_jobs_stub.py`
- `agentcoach/roles/extractor.py`
- `agentcoach/roles/gap_mapper.py`

### RoleRequirement

```python
RoleRequirement = {
    "requirement_id": str,
    "role_family": "ai_engineer" | "agentic_engineer" | "fde" | "applied_ai" | "swe_ai_platform",
    "company": str | None,
    "source_id": str,
    "skill_cluster": str,
    "skill": str,
    "evidence_text": str,
    "weight": float,
    "recency": str,
    "source_url": str | None,
}
```

### SkillTaxonomy

Top-level clusters:

- SWE baseline
- System design
- Behavioral and communication
- AI application engineering
- RAG and retrieval
- Agentic systems
- Evaluation and observability
- Productionization and LLMOps
- FDE/customer deployment
- Role-specific project storytelling

### CompanyExpectationProfile

For each target company or role family:

```python
CompanyExpectationProfile = {
    "company": str,
    "role_family": str,
    "must_have_clusters": list[str],
    "differentiators": list[str],
    "interview_likely_signals": list[str],
    "source_refs": list[dict],
}
```

Examples:

- OpenAI FDE: deployment ownership, model-to-production judgment, eval-driven
  feedback, customer ambiguity, full-stack shipping.
- Anthropic Applied AI/FDE: LLM implementation patterns, agent development,
  eval frameworks, safety/reliability, customer technical advising.
- Snowflake Applied AI FDE: enterprise AI, RAG/agents, eval loops, golden
  datasets, production observability, stakeholder communication.
- Databricks AI FDE: GenAI apps, RAG, multi-agent, Text2SQL, LLMOps,
  production-grade ML/AI deployments.

### TransitionGapMapper

The mapper compares:

```text
learner background + diagnostic evidence + target role requirements
```

and emits:

- Transfer strengths: what old SWE skill maps directly.
- Missing AI-native skills.
- Missing FDE/customer skills.
- Interview expression gaps.
- Recommended harness stages.

Example:

```text
Backend engineer + rate limiter + target FDE
  -> transfer strength: quota, service reliability, API design
  -> AI-native gap: token/cost limits, tenant budgets, LLM gateway observability
  -> FDE gap: explain limits as customer value and deployment safety
  -> next drill: "Design quota controls for an enterprise LLM deployment"
```

## NotebookLM Positioning

NotebookLM and `notebooklm-py` should be treated as an optional artifact/tool
adapter, not as the product core.

Useful capabilities from `notebooklm-py`:

- Create/list/update notebooks.
- Add URL, YouTube, text, file, and Drive sources.
- Retrieve source full text and source guides.
- Ask source-grounded questions.
- Run web/Drive research.
- Generate artifacts: quizzes, flashcards, reports, audio, video, slides, mind
  maps, data tables.
- Download generated artifacts in useful formats.

Product boundary:

- NotebookLM may generate study material.
- AgentCoach decides what to train next.
- NotebookLM quizzes/flashcards can become source material for probes, but
  AgentCoach owns diagnosis, scoring, evidence, and mastery.
- NotebookLM failures must not block the core training loop.

Risk:

- `notebooklm-py` is an unofficial package that uses undocumented Google APIs.
  It can break, change behavior, or be rate limited. It should run async and
  degrade gracefully.

Sources:

- https://github.com/teng-lin/notebooklm-py
- https://github.com/teng-lin/notebooklm-py/blob/main/docs/python-api.md
- https://github.com/teng-lin/notebooklm-py/blob/main/docs/cli-reference.md

## Mission and Harness Architecture

Mission is the task container. Harness is the product heart.

Suggested first-phase package layout:

```text
agentcoach/
  missions/
    schema.py
    store.py
    orchestrator.py
    adapters/
      base.py
      local_kb.py
      stubs.py
  diagnostics/
    schema.py
    probe_generator.py
    evaluator.py
  harness/
    schema.py
    planner.py
    runtime.py
    evidence.py
  roles/
    schema.py
    taxonomy.py
    gap_mapper.py
    adapters/
      base.py
      local_profiles.py
      job_description.py
      public_jobs_stub.py
```

Existing modules should remain useful:

- `agentcoach/cards`: renderable coaching objects.
- `agentcoach/content`: deterministic content compilation and provenance.
- `agentcoach/kb`: local retrieval.
- `agentcoach/analytics`: score history and skill profile.
- `agentcoach/web/server.py`: HTTP wiring.
- `agentcoach/planner`: existing system design route logic can be consumed by
  role-transition planning.

## Core Data Objects

### MissionRecord

```python
MissionRecord = {
    "mission_id": str,
    "user_id": str,
    "status": "created" | "diagnosing" | "planning" | "training" | "reviewing" | "complete" | "failed",
    "request": dict,
    "topic_sniff": dict,
    "diagnostic_probe": dict,
    "learner_diagnosis": dict,
    "source_manifest": dict,
    "role_profile": dict,
    "harness_plan": dict,
    "next_action": dict,
    "error": str,
    "created_at": str,
    "updated_at": str,
}
```

### DiagnosticProbe

```python
DiagnosticProbe = {
    "probe_id": str,
    "topic_id": str,
    "topic_name": str,
    "target_role": str,
    "questions": [
        {
            "question_id": str,
            "type": "true_false" | "multiple_choice" | "short_answer" | "micro_scenario",
            "prompt": str,
            "options": list[dict],
            "rubric": dict,
            "gap_signal": str,
        }
    ],
}
```

### EvidenceEvent

```python
EvidenceEvent = {
    "event_id": str,
    "mission_id": str,
    "user_id": str,
    "topic_id": str,
    "role_family": str,
    "stage": "diagnose" | "learn" | "recall" | "drill" | "transfer" | "mock" | "retest",
    "input_text": str,
    "score": float,
    "gap_signals": list[str],
    "strength_signals": list[str],
    "source_refs": list[dict],
    "created_at": str,
}
```

### HarnessPlan

```python
HarnessPlan = {
    "mission_id": str,
    "topic_id": str,
    "target_role": str,
    "objective": str,
    "stages": [
        {
            "stage": str,
            "reason": str,
            "success_signal": str,
            "prompt_strategy": str,
            "source_strategy": dict,
        }
    ],
    "next_action": dict,
}
```

## API Contract

First-phase API additions:

### Create Mission

```text
POST /api/missions
```

Request:

```json
{
  "user_id": "web-guest",
  "input_text": "consistent hashing",
  "target_role": "ai_engineer",
  "target_company": "OpenAI",
  "target_level": "senior",
  "deadline": "2026-07-01",
  "background": "backend"
}
```

Response:

```json
{
  "mission_id": "abc123",
  "status": "diagnosing",
  "topic_sniff": {},
  "diagnostic_probe": {}
}
```

### Submit Diagnostic Answers

```text
POST /api/missions/{mission_id}/diagnostic
```

Request:

```json
{
  "answers": [
    {"question_id": "q1", "answer": "false"},
    {"question_id": "q2", "answer": "tenant token budget"},
    {"question_id": "q3", "answer": "Retries can amplify cost and overload the model gateway."}
  ]
}
```

Response:

```json
{
  "mission_id": "abc123",
  "status": "planning",
  "learner_diagnosis": {},
  "next_step": "build_harness_plan"
}
```

### Get Mission

```text
GET /api/missions/{mission_id}
```

Response includes status, diagnosis, source manifest, role profile, harness
plan, and next action when available.

### Start Next Action Session

```text
POST /api/missions/{mission_id}/start-session
```

This bridges the mission's next action into the existing session/card runtime.

Response:

```json
{
  "session_id": "session123",
  "mission_id": "abc123",
  "frame": {},
  "opening": "..."
}
```

## First Implementation Milestone

Goal: implement a diagnostic-first backend slice that makes the new product
shape real without rewriting the frontend or all session logic.

Scope:

1. Add mission schema and SQLite store.
2. Add topic sniffing for common system design and AI-native topics.
3. Add deterministic diagnostic probe generation for a first topic set.
4. Add diagnostic answer evaluator.
5. Add role taxonomy and local role profiles for AI Engineer, Agentic Engineer,
   FDE, and Applied AI Engineer.
6. Add local KB adapter as the only real research adapter.
7. Add stubs for NotebookLM, YouTube transcript, interview intelligence, hot
   topic, and public job adapters.
8. Add harness planner that consumes diagnosis and role taxonomy.
9. Add mission APIs.
10. Bridge mission next action to existing session start.
11. Persist evidence events from diagnostic answers.

Recommended first topic coverage:

- rate limiting / LLM gateway quotas
- caching / RAG context caching
- vector search / retrieval
- evaluation / golden datasets
- agents / tool calling
- system design URL shortener as SWE baseline control

## Error Handling

- If topic sniff confidence is low, generate a clarification probe instead of a
  full harness.
- If local KB has no hit, use role taxonomy and syllabus fallback.
- If NotebookLM or any external adapter fails, record adapter status and proceed.
- If diagnostic evaluation is inconclusive, ask one follow-up probe, capped at
  five total diagnostic questions.
- If mission planning fails, preserve the diagnostic result and return a
  recoverable `failed` status with error details.

## Testing

Unit tests:

- Topic sniff maps common topics to expected domains and role tracks.
- Diagnostic probe generator returns 3-5 structured questions.
- Diagnostic evaluator emits expected gap signals.
- Role taxonomy contains required clusters for AI Engineer, Agentic Engineer,
  FDE, and Applied AI Engineer.
- Transition gap mapper maps SWE strengths into role-specific gaps.
- Local KB adapter emits source manifest entries with provenance.
- Stub adapters report capabilities without pretending to fetch real data.
- Mission store persists and retrieves mission state.
- Harness planner chooses a next action from diagnosis and role profile.

Integration tests:

- Create mission -> receive diagnostic probe.
- Submit diagnostic answers -> receive diagnosis and harness plan.
- Start mission session -> existing session start receives next action payload.
- Mission with missing KB still produces fallback plan.
- External adapter failure does not block mission planning.

## Non-Goals For First Milestone

- Do not rebuild the frontend.
- Do not implement real LinkedIn crawling.
- Do not make NotebookLM a required dependency.
- Do not build full web crawling or forum scraping.
- Do not generate a full exported exam document.
- Do not mark mastery based on reading completion.
- Do not replace the existing session/card runtime.

## Product Quality Bar

The first milestone succeeds if a user can paste a topic, answer a few
diagnostic questions, receive a role-aware diagnosis, get a focused next action,
and start a training session that is clearly about converting SWE skill into
AI-native interview readiness.

The experience should feel like:

> "This coach found the real gap and is now training me on the exact behavior I
> need for the role."

not:

> "This assistant generated a study plan."

