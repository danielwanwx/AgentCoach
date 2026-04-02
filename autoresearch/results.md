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

| 3 | 3.3/5 | DISCARD | KB category filter + few-shot examples. kb_mastery 3.9 (ok) but pedagogy 2.8, coherence 3.2. Longer prompts hurt MiniMax performance |

## Final Conclusion (3 iterations)
All prompt modifications scored WORSE than baseline (3.7). The MiniMax model follows instructions
inconsistently — adding more instructions or examples makes it worse, not better.

The baseline prompts are the LOCAL OPTIMUM for this LLM. To go beyond 3.7:
1. Switch to Claude/GPT-4 as Coach LLM (strongest lever)
2. KB content is now indexed (2799 chunks) but needs category-filtered search (code ready, reverted due to test compat)
3. AgentMem-style knowledge prioritization (P0/P1/P2 + access tracking) for smarter retrieval
