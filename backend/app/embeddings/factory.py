from functools import lru_cache

from app.core.config import get_settings
from app.embeddings.fake import FakeEmbeddingProvider
from app.embeddings.sentence_transformer import SentenceTransformerProvider


@lru_cache
def get_embedding_provider():
    settings = get_settings()
    provider = settings.embedding_provider.lower()
    if provider == "fake":
        return FakeEmbeddingProvider()
    return SentenceTransformerProvider(settings.embedding_model)
