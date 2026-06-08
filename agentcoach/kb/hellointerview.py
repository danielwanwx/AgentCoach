"""Local HelloInterview markdown loader for session-scoped coaching KB."""
from __future__ import annotations

import re
from pathlib import Path

KB_DOMAIN_DIR = {
    "system_design": "system-design",
    "low_level_design": "low-level-design",
    "ml_system_design": "ml-system-design",
    "ai_agent": "ai-coding",
    "behavioral": "behavioral",
}

KB_TOPIC_TERMS = {
    "system_design.url_shortener": ["bitly", "url-shortener", "shortener"],
    "system_design.message_queues": ["kafka", "message-queues"],
    "system_design.caching": ["caching", "redis"],
    "system_design.sharding": ["sharding", "partitioning"],
    "system_design.distributed_rate_limiter": ["distributed-rate-limiter", "rate-limiter"],
    "system_design.rate_limiting": ["rate-limiter", "rate-limiting"],
    "system_design.networking": ["networking-essentials", "networking"],
    "system_design.numbers_to_know": ["numbers-to-know"],
    "system_design.scaling_reads": ["scaling-reads"],
    "system_design.scaling_writes": ["scaling-writes"],
    "system_design.realtime_updates": ["realtime-updates"],
    "system_design.long_running_tasks": ["long-running-tasks"],
    "system_design.dealing_with_contention": ["dealing-with-contention"],
    "system_design.large_blobs": ["large-blobs"],
    "system_design.multi_step_processes": ["multi-step-processes"],
}


def _clean_search_term(value: str) -> str:
    return (
        value.lower()
        .replace("&", "and")
        .replace("/", " ")
        .replace("(", " ")
        .replace(")", " ")
        .replace("_", "-")
        .strip()
    )


def _kb_terms_for_topic(topic_id: str, topic_name: str) -> list[str]:
    tail = topic_id.split(".", 1)[-1]
    terms = list(KB_TOPIC_TERMS.get(topic_id, []))
    terms.extend([
        tail.replace("_", "-"),
        _clean_search_term(topic_name).replace(" ", "-"),
        _clean_search_term(topic_name).split(" ")[0],
    ])
    seen: set[str] = set()
    clean_terms: list[str] = []
    for term in terms:
        term = term.strip("- ")
        if term and term not in seen:
            seen.add(term)
            clean_terms.append(term)
    return clean_terms


def _chunk_markdown_for_web(text: str, max_chunk: int = 1200) -> list[tuple[str, str]]:
    """Small local markdown chunker for session-scoped web KB excerpts."""
    sections = re.split(r"\n(?=#{1,3} )", text)
    chunks: list[tuple[str, str]] = []
    for sec in sections:
        lines = sec.strip().splitlines()
        if not lines:
            continue
        title = lines[0].lstrip("#").strip() or "Notes"
        body = "\n".join(lines[1:]).strip()
        body = re.sub(r"<[^>]+>", "", body)
        body = re.sub(r"!\[.*?\]\(.*?\)", "", body)
        body = body.strip()
        if len(body) < 80:
            continue
        if len(body) <= max_chunk:
            chunks.append((title, body))
            continue
        paragraphs = body.split("\n\n")
        current = ""
        for paragraph in paragraphs:
            if len(current) + len(paragraph) + 2 <= max_chunk:
                current = f"{current}\n\n{paragraph}".strip() if current else paragraph
            else:
                if current:
                    chunks.append((title, current))
                current = paragraph[:max_chunk]
        if current:
            chunks.append((title, current))
    return chunks


def load_hellointerview_chunks(
    kb_root: Path,
    topic_id: str,
    topic_name: str,
    domain: str,
    *,
    max_files: int = 4,
    max_chunks: int = 12,
) -> list[dict]:
    domain_dir = KB_DOMAIN_DIR.get(domain, domain.replace("_", "-"))
    search_root = kb_root / domain_dir
    if not search_root.exists():
        return []

    terms = _kb_terms_for_topic(topic_id, topic_name)
    matches: list[Path] = []
    for path in sorted(search_root.glob("*.md")):
        name = path.name.lower()
        if path.name.startswith("_"):
            continue
        if any(term in name for term in terms):
            matches.append(path)
    if not matches and domain == "system_design":
        matches = sorted((kb_root / "system-design").glob("in-a-hurry_core-concepts.md"))[:1]

    chunks: list[dict] = []
    for path in matches[:max_files]:
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        try:
            source = str(path.relative_to(kb_root.parent.parent))
        except ValueError:
            source = str(path)
        for section, content in _chunk_markdown_for_web(text):
            chunks.append({
                "content": content,
                "source": source,
                "section": section,
                "category": domain,
            })
            if len(chunks) >= max_chunks:
                return chunks
    return chunks


__all__ = ["load_hellointerview_chunks"]
