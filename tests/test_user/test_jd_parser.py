"""Tests for agentcoach/user/jd_parser.py"""
import json
import pytest
from unittest.mock import MagicMock

from agentcoach.user.jd_parser import (
    Skill,
    ParsedJD,
    SKILL_TO_TOPIC_MAP,
    map_skills_to_topics,
    parse_jd_with_llm,
    parse_jd_offline,
)


SAMPLE_JD = """Senior Software Engineer
Google — Cloud AI Team

We are looking for an experienced software engineer to join the Cloud AI team.

Requirements:
- 5+ years of experience in software engineering
- Strong knowledge of distributed systems and caching
- Experience with API design and database management
- Familiarity with machine learning and LLMs
- BS or MS in Computer Science

Preferred:
- Experience with Kafka and message queues
- Leadership experience mentoring junior engineers

Responsibilities:
- Design and build scalable AI infrastructure
- Lead cross-functional projects
- Mentor junior engineers
"""


class TestSkillDataclass:
    def test_skill_creation(self):
        s = Skill(name="Distributed Systems", priority="must", category="system_design")
        assert s.name == "Distributed Systems"
        assert s.priority == "must"
        assert s.category == "system_design"
        assert s.mapped_topics == []

    def test_skill_with_mapped_topics(self):
        s = Skill(name="Caching", priority="must", category="system_design", mapped_topics=["sd.caching"])
        assert s.mapped_topics == ["sd.caching"]


class TestParsedJD:
    def test_default_values(self):
        jd = ParsedJD()
        assert jd.company == ""
        assert jd.role_title == ""
        assert jd.required_skills == []
        assert jd.years_experience is None

    def test_with_values(self):
        jd = ParsedJD(company="Google", role_title="SWE", years_experience=5)
        assert jd.company == "Google"
        assert jd.years_experience == 5


class TestMapSkillsToTopics:
    def test_maps_known_skills(self):
        skills = [
            Skill(name="Distributed Systems", priority="must", category="system_design"),
            Skill(name="Caching", priority="must", category="system_design"),
        ]
        topics = map_skills_to_topics(skills)
        assert "system_design.networking" in topics
        assert "system_design.cap_theorem" in topics
        assert "system_design.caching" in topics

    def test_skill_gets_mapped_topics_attribute(self):
        skills = [Skill(name="Database management", priority="must", category="data")]
        map_skills_to_topics(skills)
        assert "system_design.data_modeling" in skills[0].mapped_topics

    def test_unmapped_skill_without_syllabus(self):
        skills = [Skill(name="Quantum Computing", priority="nice_to_have", category="ml")]
        topics = map_skills_to_topics(skills)
        assert topics == []

    def test_unmapped_skill_with_syllabus_fuzzy(self):
        mock_syllabus = MagicMock()
        mock_syllabus.get_domains.return_value = ["system_design"]
        mock_syllabus.get_topics.return_value = [
            {"id": "sd.quantum", "name": "Quantum Computing Basics"},
        ]
        skills = [Skill(name="quantum computing", priority="nice_to_have", category="ml")]
        topics = map_skills_to_topics(skills, syllabus=mock_syllabus)
        assert "sd.quantum" in topics

    def test_multiple_skills_dedup(self):
        skills = [
            Skill(name="Machine Learning", priority="must", category="ml"),
            Skill(name="LLM Fine-tuning", priority="must", category="ml"),
        ]
        topics = map_skills_to_topics(skills)
        # Both map to ai_agent.transformer — should appear only once
        assert topics.count("ai_agent.transformer") <= 1
        assert "ai_agent.transformer" in topics


class TestParseJdOffline:
    def test_extracts_role_title(self):
        jd = parse_jd_offline(SAMPLE_JD)
        assert jd.role_title == "Senior Software Engineer"

    def test_detects_company(self):
        jd = parse_jd_offline(SAMPLE_JD)
        assert jd.company == "Google"

    def test_detects_experience(self):
        jd = parse_jd_offline(SAMPLE_JD)
        assert jd.years_experience == 5

    def test_preserves_raw_text(self):
        jd = parse_jd_offline(SAMPLE_JD)
        assert "Cloud AI Team" in jd.raw_text

    def test_no_company_detection(self):
        jd = parse_jd_offline("Software Engineer\nSmallStartup Inc.\n3 years experience")
        assert jd.company == ""
        assert jd.years_experience == 3

    def test_empty_input(self):
        jd = parse_jd_offline("")
        assert jd.role_title == ""
        assert jd.company == ""


class TestParseJdWithLlm:
    def test_parses_llm_json_response(self):
        mock_llm = MagicMock()
        mock_llm.generate.return_value = json.dumps({
            "company": "Meta",
            "role_title": "ML Engineer",
            "level": "E5",
            "team": "FAIR",
            "required_skills": [{"name": "PyTorch", "priority": "must", "category": "ml"}],
            "preferred_skills": [{"name": "CUDA", "priority": "nice_to_have", "category": "infrastructure"}],
            "key_responsibilities": ["Build ML models"],
            "inferred_interview_topics": ["coding: algorithms"],
            "leadership_signals": ["tech lead"],
            "years_experience": 4,
            "education": "MS in CS",
        })
        jd = parse_jd_with_llm("Some JD text", mock_llm)
        assert jd.company == "Meta"
        assert jd.role_title == "ML Engineer"
        assert jd.level == "E5"
        assert len(jd.required_skills) == 1
        assert jd.required_skills[0].name == "PyTorch"
        assert jd.years_experience == 4

    def test_fallback_on_bad_json(self):
        mock_llm = MagicMock()
        mock_llm.generate.return_value = "I cannot parse this"
        jd = parse_jd_with_llm("Some JD text", mock_llm)
        assert jd.raw_text == "Some JD text"
        assert jd.company == ""

    def test_fallback_on_exception(self):
        mock_llm = MagicMock()
        mock_llm.generate.side_effect = Exception("API error")
        jd = parse_jd_with_llm("Some JD text", mock_llm)
        assert jd.raw_text == "Some JD text"
