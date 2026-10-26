import hashlib

import numpy as np


class FakeEmbeddingProvider:
    def __init__(self, dimension: int = 32) -> None:
        self.model_name = "fake-hash-embeddings"
        self.dimension = dimension
        self.ready = True

    def embed(self, texts: list[str]) -> list[list[float]]:
        vectors: list[list[float]] = []
        for text in texts:
            digest = hashlib.sha256(text.encode("utf-8")).digest()
            seed = int.from_bytes(digest[:8], "little")
            rng = np.random.default_rng(seed)
            vector = rng.normal(size=self.dimension)
            norm = np.linalg.norm(vector) or 1.0
            vectors.append((vector / norm).astype(float).tolist())
        return vectors
