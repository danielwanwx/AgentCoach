"""Knowledge Store — SQLite FTS5 + optional vector search with RRF hybrid ranking."""
import sqlite3
import struct
import os
import math


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
        conn.commit()
        conn.close()

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

    def add_chunk(self, content: str, source: str, section: str, category: str):
        embedding_blob = None
        if self.use_vectors and self.embedder:
            vec = self.embedder.embed(content)
            embedding_blob = self._pack_vector(vec)

        conn = sqlite3.connect(self.db_path)
        conn.execute(
            "INSERT INTO chunks (content, source, section, category, embedding) VALUES (?, ?, ?, ?, ?)",
            (content, source, section, category, embedding_blob),
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
        """Hybrid search: FTS5 + vector (if available), ranked by RRF."""
        fts_results = self._search_fts(query, limit=limit * 2, category=category)

        if not self.use_vectors or not self.embedder:
            return fts_results[:limit]

        vec_results = self._search_vector(query, limit=limit * 2, category=category)
        return self._rrf_merge(fts_results, vec_results, limit=limit)

    def _search_fts(self, query: str, limit: int = 10, category: str = "") -> list:
        conn = sqlite3.connect(self.db_path)
        # Build FTS5 query with prefix matching
        tokens = query.strip().split()
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

    def get_stats(self) -> dict:
        conn = sqlite3.connect(self.db_path)
        total = conn.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]
        categories = conn.execute("SELECT DISTINCT category FROM chunks").fetchall()
        sources = conn.execute("SELECT COUNT(DISTINCT source) FROM chunks").fetchone()[0]
        conn.close()
        return {
            "total_chunks": total,
            "categories": [c[0] for c in categories],
            "total_sources": sources,
        }
