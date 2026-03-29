"""Embedding client — uses Ollama API for local embeddings."""
import json
import urllib.request


class OllamaEmbedding:
    def __init__(self, model: str = "qwen3-embedding:8b", base_url: str = "http://localhost:11434"):
        self.model = model
        self.base_url = base_url

    def embed(self, text: str) -> list:
        """Get embedding vector for a single text."""
        return self.embed_batch([text])[0]

    def embed_batch(self, texts: list) -> list:
        """Get embedding vectors for multiple texts."""
        data = json.dumps({"model": self.model, "input": texts}).encode()
        req = urllib.request.Request(
            f"{self.base_url}/api/embed",
            data=data,
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read())
        return result["embeddings"]
