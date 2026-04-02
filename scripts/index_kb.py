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
    "low-level-design": "algorithms",
    "salary-negotiation": "behavioral",
    "blog": "system_design",  # most blog posts are SD-related
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


def parse_vtt(text: str) -> str:
    """Convert VTT subtitle file to plain text."""
    lines = []
    for line in text.split('\n'):
        line = line.strip()
        # Skip timestamps, WEBVTT header, empty lines
        if not line or line.startswith('WEBVTT') or '-->' in line or line.isdigit():
            continue
        # Strip HTML tags
        line = re.sub(r'<[^>]+>', '', line)
        if line and line not in lines[-1:]:  # dedup consecutive
            lines.append(line)
    return ' '.join(lines)


def index_youtube(kb: KnowledgeStore, youtube_dir: str):
    """Index YouTube VTT transcripts."""
    count = 0
    for fname in sorted(os.listdir(youtube_dir)):
        if not fname.endswith('.vtt'):
            continue
        filepath = os.path.join(youtube_dir, fname)
        with open(filepath, 'r') as f:
            text = parse_vtt(f.read())

        if len(text) < 100:
            continue

        # Extract title from filename
        title = fname.rsplit('[', 1)[0].strip().rstrip('.')
        # Guess category from title
        title_lower = title.lower()
        if 'behavioral' in title_lower:
            category = 'behavioral'
        elif 'coding' in title_lower or 'leetcode' in title_lower:
            category = 'algorithms'
        elif 'ml' in title_lower or 'ai' in title_lower:
            category = 'ai_agent'
        else:
            category = 'system_design'

        # Split into ~800 char chunks
        words = text.split()
        chunk_size = 120  # ~120 words per chunk
        batch = []
        for i in range(0, len(words), chunk_size):
            chunk_text = ' '.join(words[i:i + chunk_size])
            if len(chunk_text) > 80:
                batch.append({
                    "content": chunk_text,
                    "source": f"youtube_{fname[:50]}",
                    "section": title[:80],
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
    # Index article directories
    for dirname, category in DIR_CATEGORY.items():
        dirpath = os.path.join(KB_DIR, dirname)
        if not os.path.isdir(dirpath):
            print(f"  Skip {dirname} (not found)")
            continue
        count = index_directory(kb, dirpath, category)
        print(f"  {dirname}: {count} chunks indexed as '{category}'")
        total += count

    # Index YouTube transcripts
    youtube_dir = os.path.join(os.path.dirname(KB_DIR), "hellointerview-youtube")
    if os.path.isdir(youtube_dir):
        yt_count = index_youtube(kb, youtube_dir)
        print(f"  youtube: {yt_count} chunks indexed")
        total += yt_count

    stats = kb.get_stats()
    print(f"\n  Total: {total} chunks indexed")
    print(f"  KB stats: {stats}")


if __name__ == "__main__":
    main()
