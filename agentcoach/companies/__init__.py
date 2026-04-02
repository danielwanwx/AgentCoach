"""Company interview profiles — per-company interview style, topics, and tips."""
import os
import yaml
from typing import Optional

_COMPANIES_DIR = os.path.join(os.path.dirname(__file__), "data")
_cache = {}


def load_company(name: str) -> Optional[dict]:
    """Load a company profile by name (case-insensitive)."""
    key = name.lower().strip()
    if key in _cache:
        return _cache[key]

    filepath = os.path.join(_COMPANIES_DIR, f"{key}.yaml")
    if not os.path.exists(filepath):
        return None

    with open(filepath, "r") as f:
        data = yaml.safe_load(f)
    _cache[key] = data
    return data


def list_companies() -> list:
    """List all available company profiles."""
    if not os.path.isdir(_COMPANIES_DIR):
        return []
    return [f.replace(".yaml", "") for f in os.listdir(_COMPANIES_DIR) if f.endswith(".yaml")]


def format_company_for_prompt(name: str, level: str = "") -> str:
    """Format company profile as text for injection into Coach prompt."""
    company = load_company(name)
    if not company:
        return ""

    lines = [f"## Company: {company.get('name', name)}"]

    if "interview_style" in company:
        lines.append("\nInterview style:")
        for tip in company["interview_style"]:
            lines.append(f"- {tip}")

    if level and "levels" in company:
        lvl_data = company["levels"].get(level, {})
        if lvl_data:
            lines.append(f"\nLevel {level}:")
            for k, v in lvl_data.items():
                if isinstance(v, list):
                    lines.append(f"- {k}: {', '.join(v)}")
                else:
                    lines.append(f"- {k}: {v}")

    if "common_topics" in company:
        lines.append("\nCommon topics:")
        for domain, topics in company["common_topics"].items():
            lines.append(f"- {domain}: {', '.join(topics[:5])}")

    return "\n".join(lines)
