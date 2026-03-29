import os
import tempfile
from agentcoach.kb.store import KnowledgeStore

def test_add_and_search_fts():
    """FTS5 keyword search works."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test_kb.db")
        ks = KnowledgeStore(db_path=db_path, use_vectors=False)
        ks.add_chunk(
            content="Consistent hashing distributes data across nodes using a hash ring.",
            source="system_design/partitioning.md",
            section="Consistent Hashing",
            category="system_design",
        )
        ks.add_chunk(
            content="CAP theorem states you can only have two of: Consistency, Availability, Partition tolerance.",
            source="system_design/cap.md",
            section="CAP Theorem",
            category="system_design",
        )
        results = ks.search("consistent hashing", limit=5)
        assert len(results) > 0
        assert "hash ring" in results[0]["content"]

def test_search_returns_metadata():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test_kb.db")
        ks = KnowledgeStore(db_path=db_path, use_vectors=False)
        ks.add_chunk(
            content="Redis is an in-memory data store used for caching.",
            source="technologies/redis.md",
            section="Overview",
            category="key_technologies",
        )
        results = ks.search("redis caching", limit=5)
        assert len(results) > 0
        assert results[0]["source"] == "technologies/redis.md"
        assert results[0]["section"] == "Overview"

def test_get_stats():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test_kb.db")
        ks = KnowledgeStore(db_path=db_path, use_vectors=False)
        ks.add_chunk(content="chunk1", source="a.md", section="s1", category="cat1")
        ks.add_chunk(content="chunk2", source="b.md", section="s2", category="cat2")
        stats = ks.get_stats()
        assert stats["total_chunks"] == 2
        assert len(stats["categories"]) == 2
