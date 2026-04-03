"""KB CLI — index knowledge base content from kb/ directory."""
import os
import sys


def index_kb(kb_dir: str = "", use_vectors: bool = False):
    """Index all KB content into the KnowledgeStore SQLite database.

    Args:
        kb_dir: Path to kb/ directory. Defaults to kb/ in project root.
        use_vectors: Enable vector embeddings (requires Ollama + qwen3-embedding).
    """
    from agentcoach.kb.store import KnowledgeStore
    from agentcoach.kb.indexer import index_directory

    if not kb_dir:
        # Auto-detect: look for kb/ relative to this file's project root
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        kb_dir = os.path.join(project_root, "kb")

    if not os.path.isdir(kb_dir):
        print(f"Error: KB directory not found: {kb_dir}")
        sys.exit(1)

    store = KnowledgeStore(use_vectors=use_vectors)
    print(f"Indexing KB from: {kb_dir}")
    print(f"Vector embeddings: {'ON' if use_vectors else 'OFF (FTS5 only, fast)'}")
    print(f"Database: {store.db_path}")
    print()

    # Index each subdirectory as a category
    total_files = 0
    total_chunks = 0
    for subdir in sorted(os.listdir(kb_dir)):
        subdir_path = os.path.join(kb_dir, subdir)
        if not os.path.isdir(subdir_path) or subdir.startswith("."):
            continue

        # Map directory names to categories
        if "youtube" in subdir:
            category = "youtube"
        elif "podcast" in subdir or "lenny" in subdir:
            category = "podcast"
        else:
            category = "article"

        print(f"  {subdir}/ -> category={category} ... ", end="", flush=True)
        stats = index_directory(subdir_path, store, category=category)
        print(f"{stats['files_processed']} files, {stats['chunks_added']} chunks")
        if stats["errors"]:
            for e in stats["errors"]:
                print(f"    ERROR: {e['file']}: {e['error']}")
        total_files += stats["files_processed"]
        total_chunks += stats["chunks_added"]

    print(f"\nDone: {total_files} files -> {total_chunks} chunks indexed")
    db_stats = store.get_stats()
    print(f"Total in DB: {db_stats['total_chunks']} chunks, {db_stats['total_sources']} sources")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Index AgentCoach knowledge base")
    parser.add_argument("--kb-dir", default="", help="Path to kb/ directory")
    parser.add_argument("--vectors", action="store_true",
                        help="Enable vector embeddings (requires Ollama)")
    parser.add_argument("--stats", action="store_true",
                        help="Show KB stats without indexing")
    args = parser.parse_args()

    if args.stats:
        from agentcoach.kb.store import KnowledgeStore
        store = KnowledgeStore(use_vectors=False)
        stats = store.get_stats()
        if stats["total_chunks"] == 0:
            print("KB is empty. Run: agentcoach-kb to index.")
        else:
            print(f"Chunks: {stats['total_chunks']}")
            print(f"Sources: {stats['total_sources']}")
            print(f"Categories: {', '.join(stats['categories'])}")
            if stats.get("priority_distribution"):
                print(f"Priority: {stats['priority_distribution']}")
        return

    index_kb(kb_dir=args.kb_dir, use_vectors=args.vectors)


if __name__ == "__main__":
    main()
