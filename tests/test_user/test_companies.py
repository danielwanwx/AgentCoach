"""Tests for agentcoach/companies/__init__.py"""
import pytest
from unittest.mock import patch, mock_open

from agentcoach.companies import load_company, list_companies, format_company_for_prompt


class TestListCompanies:
    """Tests for list_companies."""

    def test_list_companies_returns_4(self):
        """The data directory contains exactly 4 company profiles."""
        companies = list_companies()
        assert len(companies) == 4
        assert set(companies) == {"amazon", "google", "meta", "tiktok"}


class TestLoadCompany:
    """Tests for load_company."""

    def test_load_google_has_required_fields(self):
        """Google profile has name, interview_style, common_topics, and levels."""
        data = load_company("google")
        assert data is not None
        assert data["name"] == "Google"
        assert "interview_style" in data
        assert isinstance(data["interview_style"], list)
        assert "common_topics" in data
        assert "levels" in data
        assert "L5" in data["levels"]

    def test_load_meta_has_required_fields(self):
        """Meta profile has name and interview_style."""
        data = load_company("meta")
        assert data is not None
        assert data["name"] == "Meta"
        assert "interview_style" in data
        assert isinstance(data["interview_style"], list)

    def test_load_case_insensitive(self):
        """Loading by 'Google' (capitalized) works via case normalization."""
        data = load_company("Google")
        assert data is not None
        assert data["name"] == "Google"

    def test_load_nonexistent_returns_none(self):
        """Loading a company that has no YAML file returns None."""
        result = load_company("nonexistent_corp")
        assert result is None


class TestFormatCompanyForPrompt:
    """Tests for format_company_for_prompt."""

    def test_format_company_for_prompt(self):
        """Formatted prompt contains company name and interview style."""
        result = format_company_for_prompt("google")
        assert isinstance(result, str)
        assert "Google" in result
        assert "Interview style" in result

    def test_format_company_with_level(self):
        """Formatted prompt with level includes level-specific data."""
        result = format_company_for_prompt("google", level="L5")
        assert "L5" in result

    def test_format_company_includes_common_topics(self):
        """Formatted prompt includes common interview topics."""
        result = format_company_for_prompt("google")
        assert "Common topics" in result
        assert "system_design" in result

    def test_format_nonexistent_company_returns_empty(self):
        """Formatting a nonexistent company returns empty string."""
        result = format_company_for_prompt("nonexistent_corp")
        assert result == ""
