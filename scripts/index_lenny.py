#!/usr/bin/env python3
"""Index Lenny's Newsletter + Podcast data into AgentCoach KB.

Maps content to categories relevant to interview coaching:
- Interview/hiring articles → behavioral
- Leadership/management → behavioral
- Product strategy → system_design (PM interviews overlap with SD)
- Engineering/tech → system_design + ai_agent
- Podcasts → behavioral (leadership lessons from industry leaders)
"""
import os, sys, re

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agentcoach.kb.store import KnowledgeStore

LENNY_DIR = "/Users/javiswan/Projects/Her/kb/lennys-newsletterpodcastdata-all"


def classify_article(filename: str) -> tuple:
    """Classify article by filename into (category, priority)."""
    f = filename.lower()

    # P0: directly interview/career relevant
    if any(w in f for w in ['interview', 'hiring', 'career', 'resume', 'job-search',
                            'offer', 'salary', 'negotiat']):
        return 'behavioral', 0

    # P1: leadership and management (behavioral interview gold)
    if any(w in f for w in ['leadership', 'managing', 'manager', 'team', 'culture',
                            'decision', 'conflict', 'communicat', 'feedback',
                            'one-on-one', 'performance-review']):
        return 'behavioral', 1

    # P1: product/strategy (PM interviews + system design thinking)
    if any(w in f for w in ['product', 'strategy', 'metric', 'growth', 'retention',
                            'engagement', 'north-star', 'okr', 'roadmap']):
        return 'system_design', 1

    # P1: engineering/tech content
    if any(w in f for w in ['engineer', 'system', 'design', 'architect', 'scale',
                            'ai', 'machine-learning', 'tech', 'code', 'build']):
        return 'system_design', 1

    # P2: everything else (still useful context)
    return 'behavioral', 2


def chunk_markdown(text: str, max_chunk: int = 800) -> list:
    """Split by headers, respect max size."""
    sections = re.split(r'\n(?=#{1,3} )', text)
    chunks = []
    for sec in sections:
        lines = sec.strip().split('\n')
        if not lines:
            continue
        title = lines[0].lstrip('#').strip()
        body = '\n'.join(lines[1:]).strip()
        body = re.sub(r'<[^>]+>', '', body)
        body = re.sub(r'!\[.*?\]\(.*?\)', '', body)
        body = body.strip()
        if len(body) < 50:
            continue
        if len(body) > max_chunk:
            # Split on paragraphs
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


def index_newsletters(kb: KnowledgeStore):
    """Index newsletter articles."""
    newsletter_dir = os.path.join(LENNY_DIR, "02-newsletters")
    count = 0
    for fname in sorted(os.listdir(newsletter_dir)):
        if not fname.endswith('.md'):
            continue
        filepath = os.path.join(newsletter_dir, fname)
        with open(filepath, 'r') as f:
            text = f.read()

        category, priority = classify_article(fname)
        source = f"lenny_{fname.replace('.md', '')[:60]}"
        chunks = chunk_markdown(text)

        batch = []
        for title, body in chunks:
            batch.append({
                "content": body,
                "source": source,
                "section": title[:80],
                "category": category,
            })

        if batch:
            kb.add_chunks_batch(batch)
            # Set priority
            import sqlite3
            conn = sqlite3.connect(kb.db_path)
            conn.execute("UPDATE chunks SET priority = ? WHERE source = ?", (priority, source))
            conn.commit()
            conn.close()
            count += len(batch)

    return count


def index_podcasts(kb: KnowledgeStore):
    """Index podcast transcripts."""
    podcast_dir = os.path.join(LENNY_DIR, "03-podcasts")
    count = 0
    for fname in sorted(os.listdir(podcast_dir)):
        if not fname.endswith('.md'):
            continue
        filepath = os.path.join(podcast_dir, fname)
        with open(filepath, 'r') as f:
            text = f.read()

        if len(text) < 200:
            continue

        source = f"lenny_pod_{fname.replace('.md', '')[:50]}"
        category, priority = classify_article(fname)
        # Podcasts are mostly behavioral/leadership content
        if category == 'system_design':
            category = 'behavioral'

        chunks = chunk_markdown(text, max_chunk=600)

        batch = []
        for title, body in chunks:
            batch.append({
                "content": body,
                "source": source,
                "section": title[:80],
                "category": category,
            })

        if batch:
            kb.add_chunks_batch(batch)
            import sqlite3
            conn = sqlite3.connect(kb.db_path)
            conn.execute("UPDATE chunks SET priority = ? WHERE source = ?", (priority, source))
            conn.commit()
            conn.close()
            count += len(batch)

    return count


def main():
    kb = KnowledgeStore(use_vectors=False)

    print("Indexing Lenny's Newsletter...")
    nl_count = index_newsletters(kb)
    print(f"  Newsletters: {nl_count} chunks")

    print("Indexing Lenny's Podcasts...")
    pod_count = index_podcasts(kb)
    print(f"  Podcasts: {pod_count} chunks")

    stats = kb.get_stats()
    print(f"\n  Total KB: {stats['total_chunks']} chunks")
    print(f"  Priority: {stats['priority_distribution']}")
    print(f"  Sources: {stats['total_sources']}")


if __name__ == "__main__":
    main()
