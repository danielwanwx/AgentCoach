"""Directory indexer — walks a directory, chunks markdown files, stores in KnowledgeStore."""
import os
from agentcoach.kb.chunker import chunk_markdown
from agentcoach.kb.store import KnowledgeStore


def index_directory(directory: str, store: KnowledgeStore, category: str = "general") -> dict:
    """Index all markdown files in a directory into the KnowledgeStore.

    Returns stats: {files_processed, chunks_added, errors}
    """
    directory = os.path.expanduser(directory)
    if not os.path.isdir(directory):
        raise NotADirectoryError(f"Not a directory: {directory}")

    files_processed = 0
    chunks_added = 0
    errors = []

    for root, dirs, files in os.walk(directory):
        for fname in sorted(files):
            if not fname.endswith((".md", ".markdown", ".txt")):
                continue
            filepath = os.path.join(root, fname)
            rel_path = os.path.relpath(filepath, directory)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                chunks = chunk_markdown(content, source=rel_path, category=category)
                if chunks:
                    store.add_chunks_batch(chunks)
                    chunks_added += len(chunks)
                files_processed += 1
            except Exception as e:
                errors.append({"file": rel_path, "error": str(e)})

    return {
        "files_processed": files_processed,
        "chunks_added": chunks_added,
        "errors": errors,
    }
