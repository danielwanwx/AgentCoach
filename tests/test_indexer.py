import os
import tempfile
from agentcoach.kb.indexer import index_directory
from agentcoach.kb.store import KnowledgeStore

def test_index_directory():
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create some markdown files
        os.makedirs(os.path.join(tmpdir, "docs"))
        with open(os.path.join(tmpdir, "docs", "design.md"), "w") as f:
            f.write("# System Design\n\n## Caching\n\nRedis is commonly used for caching hot data.\n\n## Sharding\n\nSharding distributes data across multiple database instances.\n")
        with open(os.path.join(tmpdir, "docs", "algo.md"), "w") as f:
            f.write("# Algorithms\n\n## Binary Search\n\nBinary search works on sorted arrays in O(log n) time.\n")

        db_path = os.path.join(tmpdir, "test_kb.db")
        ks = KnowledgeStore(db_path=db_path, use_vectors=False)
        stats = index_directory(os.path.join(tmpdir, "docs"), ks, category="interview_prep")

        assert stats["files_processed"] == 2
        assert stats["chunks_added"] > 0

        # Verify searchable
        results = ks.search("caching redis")
        assert len(results) > 0

def test_index_directory_skips_non_markdown():
    with tempfile.TemporaryDirectory() as tmpdir:
        with open(os.path.join(tmpdir, "readme.md"), "w") as f:
            f.write("# Hello\n\nSome content that is long enough to be a chunk.\n")
        with open(os.path.join(tmpdir, "data.json"), "w") as f:
            f.write('{"key": "value"}')

        db_path = os.path.join(tmpdir, "test_kb.db")
        ks = KnowledgeStore(db_path=db_path, use_vectors=False)
        stats = index_directory(tmpdir, ks, category="test")

        assert stats["files_processed"] == 1  # only .md
