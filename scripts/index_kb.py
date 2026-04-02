#!/usr/bin/env python3
"""Index all hellointerview KB content into AgentCoach's KnowledgeStore.

Reads markdown files from kb/hellointerview/ and indexes them as chunks.
"""
import os, sys, re

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agentcoach.kb.store import KnowledgeStore

KB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "kb", "hellointerview")

# Map directories to categories
DIR_CATEGORY = {
    "system-design": "system_design",
    "behavioral": "behavioral",
    "code": "algorithms",
    "ai-coding": "ai_agent",
    "ml-system-design": "ai_agent",
}


def chunk_markdown(text: str, max_chunk: int = 800) -> list:
    """Split markdown by headers into chunks, respecting max size."""
    sections = re.split(r'\n(?=#{1,3} )', text)
    chunks = []
    for sec in sections:
        lines = sec.strip().split('\n')
        if not lines:
            continue
        title = lines[0].lstrip('#').strip()
        body = '\n'.join(lines[1:]).strip()
        # Strip HTML, images
        body = re.sub(r'<[^>]+>', '', body)
        body = re.sub(r'!\[.*?\]\(.*?\)', '', body)
        body = body.strip()
        if len(body) < 50:
            continue
        # Split long sections
        if len(body) > max_chunk:
            paragraphs = body.split('\n\n')
            current = ""
            for p in paragraphs:
                if len(current) + len(p) + 2 <= max_chunk:
                    current = f"{current}\n\n{p}".strip() if current else p
                else:
                    if current:
                        chunks.append((title, current))
                    current = p[:max_chunk]
            if current:
                chunks.append((title, current))
        else:
            chunks.append((title, body))
    return chunks


def index_directory(kb: KnowledgeStore, directory: str, category: str):
    """Index all .md files in a directory."""
    count = 0
    for fname in sorted(os.listdir(directory)):
        if not fname.endswith('.md') or fname.startswith('_'):
            continue
        filepath = os.path.join(directory, fname)
        with open(filepath, 'r') as f:
            text = f.read()

        source = fname.replace('.md', '')
        chunks = chunk_markdown(text)

        batch = []
        for title, body in chunks:
            batch.append({
                "content": body,
                "source": source,
                "section": title,
                "category": category,
            })

        if batch:
            kb.add_chunks_batch(batch)
            count += len(batch)

    return count


def main():
    # Use the default KB path
    kb = KnowledgeStore(use_vectors=False)

    total = 0
    for dirname, category in DIR_CATEGORY.items():
        dirpath = os.path.join(KB_DIR, dirname)
        if not os.path.isdir(dirpath):
            print(f"  Skip {dirname} (not found)")
            continue
        count = index_directory(kb, dirpath, category)
        print(f"  {dirname}: {count} chunks indexed as '{category}'")
        total += count

    stats = kb.get_stats()
    print(f"\n  Total: {total} chunks indexed")
    print(f"  KB stats: {stats}")


if __name__ == "__main__":
    main()
