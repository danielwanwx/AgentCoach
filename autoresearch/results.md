# Autoresearch: AgentCoach Comprehensive E2E Testing

## Configuration
- Goal: Expose all bugs, edge cases, quality issues across all modes/domains/personas
- Metric: unique issues discovered and fixed
- Direction: maximize
- Iterations: 5

## Results Log

| Iter | Score | Kept/Discarded | Notes |
|------|-------|----------------|-------|
| 0 | 3.7/5 | baseline | Weakest: adaptability 3.2, pedagogy 3.1. Best: kb_mastery 4.0, correction 4.1 |
| 1 | 3.6/5 | DISCARD | Added adaptive rules to LEARN/REINFORCE. Helped overconfident (3.0→4.4) but hurt topic_jumper (3.9→2.7) |
| 2 | 3.5/5 | DISCARD | Full COACH_PERSONA rewrite. adaptability +0.3 but kb_mastery -0.8. Generic persona diluted domain expertise |

## Key Insight
Prompt changes have contradictory effects across personas. The baseline prompts are already well-tuned.
The bottleneck is NOT the prompt — it's the LLM (MiniMax) following instructions inconsistently.
Better Coach quality likely requires: (1) better base LLM, (2) richer KB content, (3) few-shot examples in prompt.
