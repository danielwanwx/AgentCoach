"""Source-grounded content compiler.

This module is the stable bridge between raw KB markdown and coach cards:

KB markdown -> section paragraphs -> unit draft -> editorial unit -> provenance.

The compiler is intentionally deterministic. LLM polish can sit on top of the
``draft`` payload later, but the paragraph provenance should stay reproducible
and independent of a model call.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable


@dataclass(frozen=True)
class MarkdownParagraph:
    id: str
    source_label: str
    source_url: str
    local_path: str
    section: str
    line_start: int
    line_end: int
    text: str

    def ref(self, *, preview_chars: int = 220) -> dict[str, Any]:
        preview = " ".join(self.text.split())
        if len(preview) > preview_chars:
            preview = preview[:preview_chars].rsplit(" ", 1)[0].rstrip(" ,;:") + "."
        return {
            "id": self.id,
            "source": self.source_label,
            "url": self.source_url,
            "local_path": self.local_path,
            "section": self.section,
            "line_start": self.line_start,
            "line_end": self.line_end,
            "preview": preview,
        }


@dataclass(frozen=True)
class MarkdownSection:
    title: str
    local_path: str
    source_url: str
    line_start: int
    line_end: int
    paragraphs: list[MarkdownParagraph] = field(default_factory=list)


@dataclass(frozen=True)
class EditorialUnit:
    """Human/LLM-polished unit over a deterministic source draft."""

    id: str
    source_path: str
    source_sections: list[str]
    title: str
    objective: str
    body: str
    example: str
    coach_script: str
    key_points: list[str]
    check_prompt: str
    options: list[dict[str, str]]
    correct_option_id: str
    expected_keywords: list[str]
    repair: str
    flash_body: str = ""
    quizzes: list[dict[str, Any]] = field(default_factory=list)


@dataclass(frozen=True)
class CompiledUnit:
    id: str
    title: str
    objective: str
    body: str
    example: str
    coach_script: str
    key_points: list[str]
    check_prompt: str
    options: list[dict[str, str]]
    correct_option_id: str
    expected_keywords: list[str]
    repair: str
    flash_body: str
    quizzes: list[dict[str, Any]]
    source_path: str
    source_url: str
    source_sections: list[str]
    source_paragraphs: list[dict[str, Any]]
    draft: dict[str, Any]


def parse_markdown_sections(
    path: Path,
    *,
    known_titles: Iterable[str] = (),
    source_label: str = "Knowledge Base",
    project_root: Path | None = None,
) -> dict[str, MarkdownSection]:
    """Parse markdown into section paragraphs with stable paragraph ids.

    Some scraped KB files are not strict markdown: many headings are stored as
    plain standalone lines instead of ``##`` headings. ``known_titles`` lets the
    compiler recover those source sections deterministically from the unit
    blueprint.
    """
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    local_path = _local_path(path, project_root)
    source_url = _extract_source_url(lines)
    known = {t.strip(): t.strip() for t in known_titles if t.strip()}

    heading_lines: list[tuple[int, str]] = []
    for i, raw in enumerate(lines, start=1):
        line = raw.strip()
        if not line:
            continue
        md_heading = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if md_heading:
            heading_lines.append((i, _clean_heading(md_heading.group(2))))
            continue
        if line in known:
            heading_lines.append((i, line))

    # Deduplicate while preserving order. A strict markdown heading can also be
    # listed in ``known_titles``.
    deduped: list[tuple[int, str]] = []
    seen_lines: set[int] = set()
    for item in sorted(heading_lines, key=lambda x: x[0]):
        if item[0] in seen_lines:
            continue
        seen_lines.add(item[0])
        deduped.append(item)

    sections: dict[str, MarkdownSection] = {}
    for idx, (line_no, title) in enumerate(deduped):
        next_line = deduped[idx + 1][0] if idx + 1 < len(deduped) else len(lines) + 1
        paragraphs = _paragraphs_for_section(
            lines,
            title=title,
            start_line=line_no + 1,
            end_line=next_line - 1,
            source_label=source_label,
            source_url=source_url,
            local_path=local_path,
        )
        section = MarkdownSection(
            title=title,
            local_path=local_path,
            source_url=source_url,
            line_start=line_no,
            line_end=next_line - 1,
            paragraphs=paragraphs,
        )
        existing = sections.get(title)
        if existing is None or (not existing.paragraphs and section.paragraphs):
            sections[title] = section
    return sections


def compile_editorial_units(
    units: Iterable[EditorialUnit],
    *,
    kb_root: Path,
    project_root: Path,
    source_label: str = "HelloInterview",
) -> list[CompiledUnit]:
    units = list(units)
    known_titles = sorted({section for unit in units for section in unit.source_sections})
    section_cache: dict[str, dict[str, MarkdownSection]] = {}
    compiled: list[CompiledUnit] = []
    for unit in units:
        source_path = str(unit.source_path)
        if source_path not in section_cache:
            section_cache[source_path] = parse_markdown_sections(
                kb_root / source_path,
                known_titles=known_titles,
                source_label=source_label,
                project_root=project_root,
            )
        sections = section_cache[source_path]
        paragraphs: list[MarkdownParagraph] = []
        missing_sections: list[str] = []
        for title in unit.source_sections:
            section = sections.get(title)
            if section:
                paragraphs.extend(section.paragraphs)
            else:
                missing_sections.append(title)

        source_url = _first_source_url(sections, unit.source_sections)
        draft = _draft_from_paragraphs(
            unit_id=unit.id,
            source_sections=unit.source_sections,
            paragraphs=paragraphs,
            missing_sections=missing_sections,
        )
        compiled.append(CompiledUnit(
            id=unit.id,
            title=unit.title,
            objective=unit.objective,
            body=unit.body,
            example=unit.example,
            coach_script=unit.coach_script,
            key_points=list(unit.key_points),
            check_prompt=unit.check_prompt,
            options=[dict(option) for option in unit.options],
            correct_option_id=unit.correct_option_id,
            expected_keywords=list(unit.expected_keywords),
            repair=unit.repair,
            flash_body=unit.flash_body,
            quizzes=[_deepcopy_dict(q) for q in unit.quizzes],
            source_path=unit.source_path,
            source_url=source_url,
            source_sections=list(unit.source_sections),
            source_paragraphs=[p.ref() for p in paragraphs],
            draft=draft,
        ))
    return compiled


def _paragraphs_for_section(
    lines: list[str],
    *,
    title: str,
    start_line: int,
    end_line: int,
    source_label: str,
    source_url: str,
    local_path: str,
) -> list[MarkdownParagraph]:
    paragraphs: list[MarkdownParagraph] = []
    current: list[str] = []
    current_start = start_line

    def flush(line_end: int) -> None:
        nonlocal current, current_start
        text = _clean_paragraph(" ".join(current))
        if _is_useful_paragraph(text):
            para_index = len(paragraphs) + 1
            paragraphs.append(MarkdownParagraph(
                id=f"{_slug(title)}:p{para_index:02d}",
                source_label=source_label,
                source_url=source_url,
                local_path=local_path,
                section=title,
                line_start=current_start,
                line_end=line_end,
                text=text,
            ))
        current = []
        current_start = line_end + 1

    for line_no in range(start_line, end_line + 1):
        raw = lines[line_no - 1] if line_no - 1 < len(lines) else ""
        line = raw.strip()
        if not line:
            if current:
                flush(line_no - 1)
            current_start = line_no + 1
            continue
        if _skip_source_line(line):
            if current:
                flush(line_no - 1)
            current_start = line_no + 1
            continue
        if not current:
            current_start = line_no
        current.append(line)
    if current:
        flush(end_line)
    return paragraphs


def _draft_from_paragraphs(
    *,
    unit_id: str,
    source_sections: list[str],
    paragraphs: list[MarkdownParagraph],
    missing_sections: list[str],
) -> dict[str, Any]:
    candidates = [
        p.ref(preview_chars=260) for p in paragraphs
        if len(p.text.split()) >= 10
    ][:8]
    keywords = _top_keywords(" ".join(p.text for p in paragraphs))
    generated_body = _generated_body(paragraphs)
    generated_points = _generated_key_points(paragraphs)
    return {
        "compiler_version": 1,
        "unit_id": unit_id,
        "source_sections": list(source_sections),
        "paragraph_count": len(paragraphs),
        "missing_sections": list(missing_sections),
        "candidate_paragraphs": candidates,
        "keywords": keywords,
        "generated_card": {
            "title": source_sections[0] if source_sections else unit_id,
            "body": generated_body,
            "key_points": generated_points,
        },
        "generated_quiz": {
            "prompt": f"What is the core interview use of {source_sections[0] if source_sections else unit_id}?",
            "expected_keywords": keywords[:6],
            "source_paragraph_ids": [p["id"] for p in candidates[:3]],
        },
        "status": "editorial_polished",
    }


def _extract_source_url(lines: list[str]) -> str:
    for line in lines[:30]:
        match = re.match(r"^>\s*Source:\s*(\S+)", line.strip())
        if match:
            return match.group(1)
    return ""


def _first_source_url(sections: dict[str, MarkdownSection], titles: list[str]) -> str:
    for title in titles:
        section = sections.get(title)
        if section and section.source_url:
            return section.source_url
    for section in sections.values():
        if section.source_url:
            return section.source_url
    return ""


def _local_path(path: Path, project_root: Path | None) -> str:
    if project_root:
        try:
            return str(path.resolve().relative_to(project_root.resolve()))
        except ValueError:
            pass
    return str(path)


def _clean_heading(value: str) -> str:
    return value.strip().strip("#").strip()


def _clean_paragraph(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"!\[.*?\]\(.*?\)", "", text)
    text = re.sub(r"\[(.*?)\]\((.*?)\)", r"\1", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _skip_source_line(line: str) -> bool:
    if line.startswith("> Source:") or line.startswith("> Scraped:"):
        return True
    if line.startswith("![") or line.startswith("http"):
        return True
    return line in {
        "Watch Video Walkthrough",
        "Watch the author walk through the problem step-by-step",
        "Watch Now",
        "Test Your Knowledge",
        "Start Quiz",
        "Mark as read",
        "Next: API Design",
    }


def _is_useful_paragraph(text: str) -> bool:
    if len(text) < 40:
        return False
    if text.startswith("|") and text.endswith("|"):
        return False
    if text.lower().startswith("how would you rate"):
        return False
    return True


def _slug(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "section"


def _top_keywords(text: str, limit: int = 12) -> list[str]:
    stop = {
        "about", "after", "also", "because", "been", "being", "between",
        "both", "could", "does", "doing", "each", "every", "from", "have",
        "into", "like", "more", "most", "need", "only", "over", "same",
        "that", "than", "their", "them", "then", "there", "these", "they",
        "this", "through", "when", "where", "which", "while", "with",
        "without", "your", "youre", "using", "will", "would", "the", "and",
        "for", "you", "are", "can", "our", "we", "its", "it's", "not",
        "but", "was", "were", "has", "had",
    }
    counts: dict[str, int] = {}
    for token in re.findall(r"[a-zA-Z][a-zA-Z0-9+-]{2,}", text.lower()):
        if token in stop:
            continue
        counts[token] = counts.get(token, 0) + 1
    return [
        token for token, _ in sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:limit]
    ]


def _generated_body(paragraphs: list[MarkdownParagraph], limit: int = 360) -> str:
    sentences: list[str] = []
    for paragraph in paragraphs:
        for sentence in _sentences(paragraph.text):
            if len(sentence.split()) >= 8:
                sentences.append(sentence)
            if len(sentences) >= 3:
                break
        if len(sentences) >= 3:
            break
    body = " ".join(sentences[:3])
    if len(body) > limit:
        body = body[:limit].rsplit(" ", 1)[0].rstrip(" ,;:") + "."
    return body


def _generated_key_points(paragraphs: list[MarkdownParagraph], limit: int = 4) -> list[str]:
    points: list[str] = []
    for paragraph in paragraphs:
        for sentence in _sentences(paragraph.text):
            clean = sentence.strip()
            if 45 <= len(clean) <= 180 and clean not in points:
                points.append(clean)
            if len(points) >= limit:
                return points
    return points


def _sentences(text: str) -> list[str]:
    normalized = " ".join(text.split())
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9])", normalized)
    return [p.strip() for p in parts if p.strip()]


def _deepcopy_dict(value: dict[str, Any]) -> dict[str, Any]:
    copied: dict[str, Any] = {}
    for key, item in value.items():
        if isinstance(item, dict):
            copied[key] = _deepcopy_dict(item)
        elif isinstance(item, list):
            copied[key] = [
                _deepcopy_dict(v) if isinstance(v, dict) else v
                for v in item
            ]
        else:
            copied[key] = item
    return copied
