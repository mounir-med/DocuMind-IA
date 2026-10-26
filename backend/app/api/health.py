from fastapi import APIRouter

from app.core.config import get_settings
from app.embeddings.factory import get_embedding_provider
from app.llm.factory import get_llm_provider
from app.vector_store.chroma import get_vector_store

router = APIRouter(tags=["health"])


@router.get("/api/health")
def health() -> dict:
    settings = get_settings()
    llm = get_llm_provider()
    embeddings = get_embedding_provider()
    store_ok = get_vector_store().available()
    return {
        "status": "ok",
        "app": settings.app_name,
        "version": settings.app_version,
        "llm": {
            "provider": llm.name,
            "model": llm.model,
            "configured": llm.configured,
            "demo": getattr(llm, "demo", False),
        },
        "embeddings": {
            "provider": settings.embedding_provider,
            "model": embeddings.model_name,
            "ready": embeddings.ready,
        },
        "vector_store": store_ok,
    }
