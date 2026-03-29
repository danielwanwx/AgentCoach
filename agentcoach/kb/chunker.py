"""Markdown chunker — splits by headers, preserves hierarchy."""
import re


def chunk_markdown(text: str, source: str, category: str,
                   min_chunk_length: int = 50) -> list:
    """Split markdown by headers into chunks with hierarchy metadata.

    Returns list of dicts: {content, source, section, category}
    """
    if not text.strip():
        return []

    lines = text.split("\n")
    chunks = []
    current_headers = {}  # level -> header text
    current_content_lines = []
    current_section = ""

    for line in lines:
        header_match = re.match(r'^(#{1,6})\s+(.+)$', line.strip())
        if header_match:
            # Flush previous chunk
            content = "\n".join(current_content_lines).strip()
            if content:
                if len(content) >= min_chunk_length or not chunks:
                    chunks.append({
                        "content": content,
                        "source": source,
                        "section": current_section,
                        "category": category,
                    })
                else:
                    # Merge short content into previous chunk
                    chunks[-1]["content"] += "\n\n" + content

            # Update header hierarchy
            level = len(header_match.group(1))
            header_text = header_match.group(2).strip()
            current_headers[level] = header_text
            # Clear deeper levels
            for l in list(current_headers.keys()):
                if l > level:
                    del current_headers[l]

            # Build section path from hierarchy
            current_section = " > ".join(
                current_headers[l] for l in sorted(current_headers.keys())
            )
            current_content_lines = []
        else:
            current_content_lines.append(line)

    # Flush last chunk
    content = "\n".join(current_content_lines).strip()
    if content:
        if len(content) >= min_chunk_length or not chunks:
            chunks.append({
                "content": content,
                "source": source,
                "section": current_section,
                "category": category,
            })
        else:
            # Merge short content into previous chunk
            chunks[-1]["content"] += "\n\n" + content

    return chunks
