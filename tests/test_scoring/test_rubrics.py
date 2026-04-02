"""Tests for agentcoach/scoring/rubrics.py"""
import pytest

from agentcoach.scoring.rubrics import (
    RUBRICS,
    get_rubric,
    format_rubric_for_prompt,
    SYSTEM_DESIGN_RUBRIC,
    BEHAVIORAL_RUBRIC,
    ALGORITHMS_RUBRIC,
    AI_AGENT_RUBRIC,
)


class TestRubricRegistry:
    """Tests for the rubric registry and data integrity."""

    def test_rubric_exists_for_all_domains(self):
        """All four expected domains have rubrics registered."""
        expected_domains = {"system_design", "behavioral", "algorithms", "ai_agent"}
        assert set(RUBRICS.keys()) == expected_domains

    def test_rubric_dimensions_have_5_levels(self):
        """Every dimension in every rubric has exactly 5 scoring levels (1-5)."""
        for domain, rubric in RUBRICS.items():
            for dim_name, dim in rubric["dimensions"].items():
                levels = set(dim["levels"].keys())
                assert levels == {1, 2, 3, 4, 5}, (
                    f"{domain}.{dim_name} has levels {levels}, expected {{1,2,3,4,5}}"
                )

    def test_rubric_dimensions_have_weights_summing_to_1(self):
        """Dimension weights within each rubric sum to 1.0."""
        for domain, rubric in RUBRICS.items():
            total = sum(dim["weight"] for dim in rubric["dimensions"].values())
            assert abs(total - 1.0) < 1e-6, (
                f"{domain} weights sum to {total}, expected 1.0"
            )

    def test_rubric_dimensions_have_description(self):
        """Every dimension has a non-empty description string."""
        for domain, rubric in RUBRICS.items():
            for dim_name, dim in rubric["dimensions"].items():
                assert isinstance(dim["description"], str)
                assert len(dim["description"]) > 0, (
                    f"{domain}.{dim_name} has empty description"
                )


class TestGetRubric:
    """Tests for get_rubric lookup."""

    def test_get_rubric_known_domain(self):
        """get_rubric returns the correct rubric for a known domain."""
        assert get_rubric("system_design") is SYSTEM_DESIGN_RUBRIC
        assert get_rubric("behavioral") is BEHAVIORAL_RUBRIC
        assert get_rubric("algorithms") is ALGORITHMS_RUBRIC
        assert get_rubric("ai_agent") is AI_AGENT_RUBRIC

    def test_get_rubric_unknown_domain_falls_back(self):
        """get_rubric with an unknown domain falls back to system_design."""
        result = get_rubric("nonexistent_domain")
        assert result is SYSTEM_DESIGN_RUBRIC


class TestFormatRubricForPrompt:
    """Tests for prompt-formatting of rubrics."""

    def test_format_rubric_for_prompt_returns_string(self):
        """format_rubric_for_prompt returns a non-empty string."""
        for domain in RUBRICS:
            result = format_rubric_for_prompt(domain)
            assert isinstance(result, str)
            assert len(result) > 50

    def test_format_rubric_contains_dimension_names(self):
        """Formatted rubric includes all dimension names."""
        result = format_rubric_for_prompt("system_design")
        for dim_name in SYSTEM_DESIGN_RUBRIC["dimensions"]:
            assert dim_name in result

    def test_format_rubric_contains_weights(self):
        """Formatted rubric includes weight percentages."""
        result = format_rubric_for_prompt("behavioral")
        # All behavioral dims have 25% weight
        assert "25%" in result

    def test_format_rubric_contains_level_descriptors(self):
        """Formatted rubric includes the level 5 and level 1 descriptors."""
        result = format_rubric_for_prompt("algorithms")
        # Check a level-5 descriptor fragment
        assert "Identifies optimal approach" in result
        # Check a level-1 descriptor fragment
        assert "Cannot start the problem" in result
