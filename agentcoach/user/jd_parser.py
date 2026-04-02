"""JD Parser — extracts structured interview intelligence from job descriptions."""
from dataclasses import dataclass, field
from typing import Optional, List
import json
import re


@dataclass
class Skill:
    name: str
    priority: str        # "must" | "nice_to_have"
    category: str        # "system_design" | "coding" | "data" | "ml" | "infrastructure" | "behavioral"
    mapped_topics: list = field(default_factory=list)


@dataclass
class ParsedJD:
    company: str = ""
    role_title: str = ""
    level: str = ""
    team: str = ""
    required_skills: list = field(default_factory=list)
    preferred_skills: list = field(default_factory=list)
    key_responsibilities: list = field(default_factory=list)
    inferred_interview_topics: list = field(default_factory=list)
    leadership_signals: list = field(default_factory=list)
    years_experience: Optional[int] = None
    education: Optional[str] = None
    raw_text: str = ""


# Skill-to-topic mapping
SKILL_TO_TOPIC_MAP = {
    "distributed systems": ["system_design.networking", "system_design.cap_theorem"],
    "caching": ["system_design.caching"],
    "database": ["system_design.data_modeling", "system_design.db_indexing"],
    "sharding": ["system_design.sharding"],
    "message queue": ["system_design.message_queues"],
    "kafka": ["system_design.message_queues"],
    "api design": ["system_design.api_design"],
    "load balancing": ["system_design.load_balancing"],
    "rate limiting": ["system_design.rate_limiting"],
    "machine learning": ["ai_agent.transformer", "ai_agent.evaluation"],
    "llm": ["ai_agent.transformer", "ai_agent.prompting"],
    "rag": ["ai_agent.rag"],
    "agent": ["ai_agent.agent_architecture", "ai_agent.tool_use"],
    "algorithms": ["algorithms.arrays_strings", "algorithms.trees_graphs"],
    "dynamic programming": ["algorithms.dynamic_programming"],
    "leadership": ["behavioral.leadership"],
    "conflict": ["behavioral.conflict"],
    "collaboration": ["behavioral.collaboration"],
}


def map_skills_to_topics(skills: list, syllabus=None) -> list:
    """Map JD skills to syllabus topic_ids."""
    all_topics = set()
    for skill in skills:
        name_lower = skill.name.lower()
        mapped = False
        for key, topic_ids in SKILL_TO_TOPIC_MAP.items():
            if key in name_lower:
                all_topics.update(topic_ids)
                skill.mapped_topics = topic_ids
                mapped = True
                break
        if not mapped and syllabus:
            # Fuzzy: check if skill name appears in any topic name
            for domain in syllabus.get_domains():
                for topic in syllabus.get_topics(domain):
                    if name_lower in topic["name"].lower() or any(
                        w in topic["name"].lower() for w in name_lower.split()
                    ):
                        all_topics.add(topic["id"])
                        skill.mapped_topics.append(topic["id"])
                        mapped = True
    return list(all_topics)


def parse_jd_with_llm(raw_text: str, llm) -> ParsedJD:
    """Use LLM to parse JD into structured format."""
    from agentcoach.llm.base import Message

    prompt = """Parse this job description and extract structured information.
Return ONLY a JSON object:
{
    "company": "company name",
    "role_title": "full role title",
    "level": "inferred level (L5, E5, SDE2, etc.)",
    "team": "team or org name",
    "required_skills": [{"name": "skill", "priority": "must", "category": "system_design|coding|data|ml|infrastructure|behavioral"}],
    "preferred_skills": [{"name": "skill", "priority": "nice_to_have", "category": "..."}],
    "key_responsibilities": ["responsibility 1", "responsibility 2"],
    "inferred_interview_topics": ["system design: topic", "coding: topic", "behavioral: topic"],
    "leadership_signals": ["signal 1"],
    "years_experience": 5,
    "education": "BS/MS in CS"
}

Job Description:
""" + raw_text[:3000]

    try:
        response = llm.generate([Message(role="user", content=prompt)])
        match = re.search(r'\{[\s\S]*\}', response)
        if match:
            data = json.loads(match.group())
            required = [
                Skill(
                    name=s["name"],
                    priority="must",
                    category=s.get("category", "system_design"),
                )
                for s in data.get("required_skills", [])
            ]
            preferred = [
                Skill(
                    name=s["name"],
                    priority="nice_to_have",
                    category=s.get("category", "system_design"),
                )
                for s in data.get("preferred_skills", [])
            ]
            return ParsedJD(
                company=data.get("company", ""),
                role_title=data.get("role_title", ""),
                level=data.get("level", ""),
                team=data.get("team", ""),
                required_skills=required,
                preferred_skills=preferred,
                key_responsibilities=data.get("key_responsibilities", []),
                inferred_interview_topics=data.get("inferred_interview_topics", []),
                leadership_signals=data.get("leadership_signals", []),
                years_experience=data.get("years_experience"),
                education=data.get("education"),
                raw_text=raw_text,
            )
    except Exception:
        pass
    # Fallback: return minimal parsed JD
    return ParsedJD(raw_text=raw_text)


def parse_jd_offline(raw_text: str) -> ParsedJD:
    """Parse JD without LLM using regex/heuristics (for testing)."""
    jd = ParsedJD(raw_text=raw_text)
    lines = raw_text.strip().split('\n')
    if lines:
        jd.role_title = lines[0].strip()
    # Simple company detection
    for line in lines[:5]:
        for company in [
            "Google", "Meta", "Amazon", "Apple", "Microsoft",
            "TikTok", "ByteDance", "Stripe", "OpenAI",
        ]:
            if company.lower() in line.lower():
                jd.company = company
                break
    # Experience detection
    exp_match = re.search(
        r'(\d+)\+?\s*years?\s*(of\s*)?experience', raw_text, re.IGNORECASE
    )
    if exp_match:
        jd.years_experience = int(exp_match.group(1))
    return jd
