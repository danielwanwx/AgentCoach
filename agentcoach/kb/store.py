"""Knowledge Store — SQLite FTS5 + optional vector search with RRF hybrid ranking.

Knowledge prioritization (inspired by AgentMem):
- P0: Core concepts, definitions, fundamental truths — never expire
- P1: Detailed explanations, case studies — 90 day relevance
- P2: Session fragments, examples — 30 day relevance
- Access tracking: frequently retrieved chunks get boosted in search ranking
"""
import sqlite3
import struct
import os
import math
from datetime import datetime


class KnowledgeStore:
    def __init__(self, db_path: str = "", use_vectors: bool = True,
                 embedding_model: str = "qwen3-embedding:8b"):
        if not db_path:
            db_path = os.path.expanduser("~/.agentcoach/knowledge.db")
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db_path = db_path
        self.use_vectors = use_vectors
        self._embedder = None
        self._embedding_model = embedding_model
        self._vector_dim = 4096
        self._init_db()

    @property
    def embedder(self):
        if self._embedder is None and self.use_vectors:
            from agentcoach.kb.embeddings import OllamaEmbedding
            self._embedder = OllamaEmbedding(model=self._embedding_model)
        return self._embedder

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS chunks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                source TEXT NOT NULL,
                section TEXT NOT NULL,
                category TEXT NOT NULL,
                embedding BLOB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS chunks_fts
            USING fts5(content, source, section, category, content=chunks, content_rowid=id)
        """)
        conn.execute("""
            CREATE TRIGGER IF NOT EXISTS chunks_ai AFTER INSERT ON chunks BEGIN
                INSERT INTO chunks_fts(rowid, content, source, section, category)
                VALUES (new.id, new.content, new.source, new.section, new.category);
            END
        """)
        # Migration: add priority + access tracking columns
        try:
            conn.execute("ALTER TABLE chunks ADD COLUMN priority INTEGER DEFAULT 2")
        except sqlite3.OperationalError:
            pass  # column already exists
        try:
            conn.execute("ALTER TABLE chunks ADD COLUMN summary TEXT")
        except sqlite3.OperationalError:
            pass
        try:
            conn.execute("ALTER TABLE chunks ADD COLUMN access_count INTEGER DEFAULT 0")
        except sqlite3.OperationalError:
            pass
        try:
            conn.execute("ALTER TABLE chunks ADD COLUMN last_accessed TIMESTAMP")
        except sqlite3.OperationalError:
            pass
        conn.commit()
        conn.close()

    # Priority constants
    P0_CORE = 0      # core concepts, never expire
    P1_DETAILED = 1  # detailed explanations, 90-day relevance
    P2_FRAGMENT = 2  # session fragments, 30-day relevance

    def _pack_vector(self, vec: list) -> bytes:
        return struct.pack(f'{len(vec)}f', *vec)

    def _unpack_vector(self, blob: bytes) -> list:
        n = len(blob) // 4
        return list(struct.unpack(f'{n}f', blob))

    def _cosine_similarity(self, a: list, b: list) -> float:
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = math.sqrt(sum(x * x for x in a))
        norm_b = math.sqrt(sum(x * x for x in b))
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot / (norm_a * norm_b)

    def add_chunk(self, content: str, source: str, section: str, category: str,
                   priority: int = 2, summary: str = ""):
        embedding_blob = None
        if self.use_vectors and self.embedder:
            vec = self.embedder.embed(content)
            embedding_blob = self._pack_vector(vec)

        conn = sqlite3.connect(self.db_path)
        conn.execute(
            "INSERT INTO chunks (content, source, section, category, embedding, priority, summary) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (content, source, section, category, embedding_blob, priority, summary or None),
        )
        conn.commit()
        conn.close()

    def add_chunks_batch(self, chunks: list):
        """Add multiple chunks efficiently. Each chunk is a dict with content, source, section, category."""
        embedding_blobs = [None] * len(chunks)
        if self.use_vectors and self.embedder:
            texts = [c["content"] for c in chunks]
            # Batch embed in groups of 32
            all_vecs = []
            for i in range(0, len(texts), 32):
                batch = texts[i:i+32]
                all_vecs.extend(self.embedder.embed_batch(batch))
            embedding_blobs = [self._pack_vector(v) for v in all_vecs]

        conn = sqlite3.connect(self.db_path)
        for chunk, emb_blob in zip(chunks, embedding_blobs):
            conn.execute(
                "INSERT INTO chunks (content, source, section, category, embedding) VALUES (?, ?, ?, ?, ?)",
                (chunk["content"], chunk["source"], chunk["section"], chunk["category"], emb_blob),
            )
        conn.commit()
        conn.close()

    def search(self, query: str, limit: int = 5, category: str = "") -> list:
        """Hybrid search: FTS5 + vector (if available), ranked by RRF + priority/source boost."""
        # Fetch more candidates for reranking (10x for large KB)
        candidate_count = max(limit * 5, 25)
        fts_results = self._search_fts(query, limit=candidate_count, category=category)

        if not self.use_vectors or not self.embedder:
            results = fts_results[:limit]
        else:
            vec_results = self._search_vector(query, limit=limit * 2, category=category)
            results = self._rrf_merge(fts_results, vec_results, limit=limit)

        # Boost by priority: P0 chunks float to top, P2 sink
        results = self._boost_by_priority(results)

        # Track access for returned results
        self._record_access([r["id"] for r in results if "id" in r])

        return results[:limit]

    # Source type weights: articles are denser than podcast transcripts
    SOURCE_WEIGHTS = {
        "core-concepts": 1.5,   # highest value: fundamental definitions
        "problem-breakdowns": 1.3,  # high value: worked examples
        "deep-dives": 1.2,
        "patterns": 1.2,
        "in-a-hurry": 1.1,
        "course": 1.0,
        "blog": 0.8,
        "lenny_pod": 0.4,      # podcast transcripts: verbose, low density
        "youtube": 0.5,         # video transcripts: better than podcast but still noisy
    }

    def _get_source_weight(self, source: str) -> float:
        """Get weight multiplier for a source based on content type."""
        for prefix, weight in self.SOURCE_WEIGHTS.items():
            if source.startswith(prefix) or prefix in source:
                return weight
        return 0.7  # default for unknown sources

    def _boost_by_priority(self, results: list) -> list:
        """Re-rank results by priority, source quality, and access frequency."""
        if not results:
            return results
        conn = sqlite3.connect(self.db_path)
        for r in results:
            if "id" not in r:
                r["_boost"] = 0
                continue
            row = conn.execute(
                "SELECT priority, access_count, source FROM chunks WHERE id = ?", (r["id"],)
            ).fetchone()
            if row:
                priority, access_count, source = row
                # Priority boost: P0=0.9, P1=0.6, P2=0.3
                priority_score = (3 - (priority or 2)) * 0.3
                # Source quality: articles > podcasts
                source_weight = self._get_source_weight(source or "")
                # Access frequency: popular content gets a small bump
                access_score = math.log1p(access_count or 0) * 0.05
                r["_boost"] = priority_score * source_weight + access_score
            else:
                r["_boost"] = 0
        conn.close()
        results.sort(key=lambda x: x.get("_boost", 0), reverse=True)
        return results

    def _record_access(self, chunk_ids: list):
        """Increment access count and update last_accessed timestamp."""
        if not chunk_ids:
            return
        conn = sqlite3.connect(self.db_path)
        now = datetime.utcnow().isoformat()
        for cid in chunk_ids:
            conn.execute(
                "UPDATE chunks SET access_count = COALESCE(access_count, 0) + 1, "
                "last_accessed = ? WHERE id = ?",
                (now, cid),
            )
        conn.commit()
        conn.close()

    def _search_fts(self, query: str, limit: int = 10, category: str = "") -> list:
        conn = sqlite3.connect(self.db_path)
        # Build FTS5 query with prefix matching (strip non-alphanumeric chars)
        import re as _re
        tokens = _re.findall(r'\w+', query)
        fts_query = " OR ".join(f"{t}*" for t in tokens if t)

        if category:
            rows = conn.execute(
                "SELECT c.id, c.content, c.source, c.section, c.category "
                "FROM chunks_fts f JOIN chunks c ON f.rowid = c.id "
                "WHERE chunks_fts MATCH ? AND c.category = ? LIMIT ?",
                (fts_query, category, limit),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT c.id, c.content, c.source, c.section, c.category "
                "FROM chunks_fts f JOIN chunks c ON f.rowid = c.id "
                "WHERE chunks_fts MATCH ? LIMIT ?",
                (fts_query, limit),
            ).fetchall()
        conn.close()
        return [{"id": r[0], "content": r[1], "source": r[2], "section": r[3], "category": r[4]} for r in rows]

    def _search_vector(self, query: str, limit: int = 10, category: str = "") -> list:
        query_vec = self.embedder.embed(query)
        conn = sqlite3.connect(self.db_path)
        if category:
            rows = conn.execute(
                "SELECT id, content, source, section, category, embedding FROM chunks WHERE embedding IS NOT NULL AND category = ?",
                (category,),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT id, content, source, section, category, embedding FROM chunks WHERE embedding IS NOT NULL"
            ).fetchall()
        conn.close()

        scored = []
        for row in rows:
            vec = self._unpack_vector(row[5])
            sim = self._cosine_similarity(query_vec, vec)
            scored.append({
                "id": row[0], "content": row[1], "source": row[2],
                "section": row[3], "category": row[4], "score": sim,
            })
        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[:limit]

    def _rrf_merge(self, fts_results: list, vec_results: list, limit: int = 5, k: int = 60) -> list:
        """Reciprocal Rank Fusion: combine FTS5 and vector rankings."""
        scores = {}
        for rank, r in enumerate(fts_results):
            rid = r["id"]
            scores[rid] = scores.get(rid, 0) + 1.0 / (k + rank + 1)
            if rid not in scores or not isinstance(scores.get(f"_data_{rid}"), dict):
                scores[f"_data_{rid}"] = r

        for rank, r in enumerate(vec_results):
            rid = r["id"]
            scores[rid] = scores.get(rid, 0) + 1.0 / (k + rank + 1)
            if f"_data_{rid}" not in scores:
                scores[f"_data_{rid}"] = r

        # Sort by RRF score
        items = []
        for key, val in scores.items():
            if isinstance(key, int):
                data = scores.get(f"_data_{key}", {})
                data["rrf_score"] = val
                items.append(data)
        items.sort(key=lambda x: x.get("rrf_score", 0), reverse=True)
        return items[:limit]

    def set_priority(self, chunk_id: int = None, source: str = None, priority: int = 2):
        """Set priority for a chunk by ID, or all chunks from a source."""
        conn = sqlite3.connect(self.db_path)
        if chunk_id:
            conn.execute("UPDATE chunks SET priority = ? WHERE id = ?", (priority, chunk_id))
        elif source:
            conn.execute("UPDATE chunks SET priority = ? WHERE source = ?", (priority, source))
        conn.commit()
        conn.close()

    def set_priority_by_section(self, section_pattern: str, priority: int):
        """Set priority for chunks whose section matches a pattern (SQL LIKE)."""
        conn = sqlite3.connect(self.db_path)
        conn.execute("UPDATE chunks SET priority = ? WHERE section LIKE ?",
                     (priority, f"%{section_pattern}%"))
        conn.commit()
        conn.close()

    def get_stats(self) -> dict:
        conn = sqlite3.connect(self.db_path)
        total = conn.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]
        categories = conn.execute("SELECT DISTINCT category FROM chunks").fetchall()
        sources = conn.execute("SELECT COUNT(DISTINCT source) FROM chunks").fetchone()[0]
        priority_dist = conn.execute(
            "SELECT COALESCE(priority, 2), COUNT(*) FROM chunks GROUP BY priority"
        ).fetchall()
        most_accessed = conn.execute(
            "SELECT source, section, access_count FROM chunks "
            "WHERE access_count > 0 ORDER BY access_count DESC LIMIT 5"
        ).fetchall()
        conn.close()
        return {
            "total_chunks": total,
            "categories": [c[0] for c in categories],
            "total_sources": sources,
            "priority_distribution": {f"P{p}": c for p, c in priority_dist},
            "most_accessed": [{"source": r[0], "section": r[1], "count": r[2]} for r in most_accessed],
        }
