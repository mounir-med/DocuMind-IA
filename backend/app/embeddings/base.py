from typing import Protocol


class EmbeddingProvider(Protocol):
    model_name: str
    dimension: int
    ready: bool

    def embed(self, texts: list[str]) -> list[list[float]]:
        ...
