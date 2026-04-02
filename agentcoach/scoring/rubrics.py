"""Scoring rubrics — structured evaluation criteria per domain and mode.

Each rubric defines dimensions with weights and level descriptors.
The Scorer uses these to produce consistent, calibrated evaluations.
"""

SYSTEM_DESIGN_RUBRIC = {
    "dimensions": {
        "requirements": {
            "weight": 0.15,
            "description": "Gathering functional and non-functional requirements",
            "levels": {
                5: "Proactively clarifies both functional and non-functional requirements, identifies edge cases and constraints",
                4: "Covers major requirements with minor gaps",
                3: "Only covers functional requirements, misses scale/latency",
                2: "Needs heavy prompting to list requirements",
                1: "Skips requirements entirely, jumps to solution",
            },
        },
        "high_level_design": {
            "weight": 0.25,
            "description": "Proposing a coherent architecture with main components",
            "levels": {
                5: "Clean, well-structured architecture with clear data flow between components",
                4: "Solid architecture, minor gaps in data flow",
                3: "Lists components but connections are vague",
                2: "Incomplete architecture, missing key components",
                1: "No clear architecture proposed",
            },
        },
        "deep_dive": {
            "weight": 0.25,
            "description": "Detailed design of specific components",
            "levels": {
                5: "Deep technical detail with concrete choices (specific DB, specific algorithm)",
                4: "Good detail on 2-3 components",
                3: "Surface-level detail on components",
                2: "Only discusses one component",
                1: "Cannot go deeper than high-level boxes",
            },
        },
        "scalability": {
            "weight": 0.15,
            "description": "Addressing scale, bottlenecks, and growth",
            "levels": {
                5: "Identifies bottlenecks, proposes concrete solutions with numbers",
                4: "Discusses scaling strategies with some specifics",
                3: "Mentions 'we can scale' without concrete plans",
                2: "Only scales when prompted",
                1: "Doesn't consider scale at all",
            },
        },
        "tradeoffs": {
            "weight": 0.20,
            "description": "Discussing alternatives, pros/cons, and design decisions",
            "levels": {
                5: "Proactively discusses multiple alternatives with clear pros/cons",
                4: "Discusses tradeoffs when relevant",
                3: "Acknowledges tradeoffs only when asked",
                2: "Struggles to articulate alternatives",
                1: "Treats design choices as obvious/given",
            },
        },
    },
}

BEHAVIORAL_RUBRIC = {
    "dimensions": {
        "star_structure": {
            "weight": 0.25,
            "description": "Using Situation-Task-Action-Result framework",
            "levels": {
                5: "Clear STAR with specific details, quantified results",
                4: "Good structure, could be more specific in places",
                3: "Has structure but missing one STAR element",
                2: "Rambling answer without clear structure",
                1: "Cannot articulate a coherent story",
            },
        },
        "specificity": {
            "weight": 0.25,
            "description": "Concrete details, numbers, names, timelines",
            "levels": {
                5: "Specific numbers, timelines, team sizes, measurable impact",
                4: "Good specifics with minor vagueness",
                3: "Some specifics but mostly general statements",
                2: "Very vague, hypothetical answers",
                1: "No concrete examples at all",
            },
        },
        "self_awareness": {
            "weight": 0.25,
            "description": "Honest reflection on mistakes, lessons learned",
            "levels": {
                5: "Genuine self-reflection, articulates specific lessons and growth",
                4: "Shows awareness of mistakes and lessons",
                3: "Surface-level reflection",
                2: "Blames others, doesn't own mistakes",
                1: "No self-awareness demonstrated",
            },
        },
        "communication": {
            "weight": 0.25,
            "description": "Clarity, conciseness, engagement",
            "levels": {
                5: "Clear, engaging, well-paced storytelling",
                4: "Good communication with minor tangents",
                3: "Adequate but could be more concise",
                2: "Rambling, hard to follow",
                1: "Incoherent or monosyllabic",
            },
        },
    },
}

ALGORITHMS_RUBRIC = {
    "dimensions": {
        "approach": {
            "weight": 0.30,
            "description": "Problem-solving approach and algorithm choice",
            "levels": {
                5: "Identifies optimal approach quickly, explains reasoning",
                4: "Good approach, may need a hint for optimal",
                3: "Starts with brute force, can optimize with guidance",
                2: "Struggles to find any approach",
                1: "Cannot start the problem",
            },
        },
        "complexity_analysis": {
            "weight": 0.20,
            "description": "Time and space complexity analysis",
            "levels": {
                5: "Correct time and space analysis with clear explanation",
                4: "Correct analysis, explanation could be clearer",
                3: "Partially correct (time right, space wrong or vice versa)",
                2: "Incorrect analysis",
                1: "Cannot analyze complexity",
            },
        },
        "edge_cases": {
            "weight": 0.20,
            "description": "Identifying and handling edge cases",
            "levels": {
                5: "Proactively identifies multiple edge cases before being asked",
                4: "Handles edge cases when prompted",
                3: "Identifies 1-2 edge cases",
                2: "Misses obvious edge cases",
                1: "Doesn't consider edge cases",
            },
        },
        "communication": {
            "weight": 0.30,
            "description": "Thinking out loud, explaining reasoning",
            "levels": {
                5: "Clear thought process, explains each step, good collaboration",
                4: "Generally communicates well",
                3: "Some silent stretches, needs prompting",
                2: "Mostly silent, hard to follow reasoning",
                1: "Cannot explain approach",
            },
        },
    },
}

AI_AGENT_RUBRIC = {
    "dimensions": {
        "fundamentals": {
            "weight": 0.25,
            "description": "LLM basics: transformers, attention, tokenization",
            "levels": {
                5: "Deep understanding of architecture, can explain mechanisms",
                4: "Solid conceptual understanding",
                3: "Knows basics but shallow on mechanisms",
                2: "Vague understanding, uses buzzwords",
                1: "Cannot explain fundamental concepts",
            },
        },
        "rag_pipeline": {
            "weight": 0.25,
            "description": "RAG: chunking, embedding, retrieval, generation",
            "levels": {
                5: "Can design a complete RAG system with tradeoff discussion",
                4: "Good understanding of pipeline stages",
                3: "Knows the stages but not the nuances",
                2: "Partial understanding",
                1: "Cannot describe RAG pipeline",
            },
        },
        "agent_systems": {
            "weight": 0.25,
            "description": "Agent architecture: tool use, planning, memory, eval",
            "levels": {
                5: "Can design agent systems, understands failure modes",
                4: "Good conceptual understanding of agent patterns",
                3: "Knows basics of tool use and planning",
                2: "Vague on agent architecture",
                1: "Cannot discuss agent systems",
            },
        },
        "practical_experience": {
            "weight": 0.25,
            "description": "Hands-on experience and real-world considerations",
            "levels": {
                5: "Discusses real deployment challenges, monitoring, cost",
                4: "Shows practical awareness beyond theory",
                3: "Theoretical knowledge with some practical awareness",
                2: "Purely theoretical",
                1: "No practical understanding",
            },
        },
    },
}

# Registry
RUBRICS = {
    "system_design": SYSTEM_DESIGN_RUBRIC,
    "behavioral": BEHAVIORAL_RUBRIC,
    "algorithms": ALGORITHMS_RUBRIC,
    "ai_agent": AI_AGENT_RUBRIC,
}


def get_rubric(domain: str) -> dict:
    """Get the scoring rubric for a domain."""
    return RUBRICS.get(domain, SYSTEM_DESIGN_RUBRIC)


def format_rubric_for_prompt(domain: str) -> str:
    """Format rubric as text for injection into scorer prompt."""
    rubric = get_rubric(domain)
    lines = ["Score each dimension on a 1-5 scale using this rubric:\n"]
    for dim_name, dim in rubric["dimensions"].items():
        lines.append(f"### {dim_name} (weight: {dim['weight']:.0%})")
        lines.append(f"{dim['description']}")
        for level, desc in sorted(dim["levels"].items(), reverse=True):
            lines.append(f"  {level}: {desc}")
        lines.append("")
    return "\n".join(lines)
