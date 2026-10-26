from functools import lru_cache

import chromadb

from app.core.config import get_settings
from app.document_processing.chunking import TextChunk


class VectorStore:
    def __init__(self) -> None:
        settings = get_settings()
        self.client = chromadb.PersistentClient(path=str(settings.chroma_dir))
        self.collection = self.client.get_or_create_collection(
            name="documind_chunks",
            metadata={"hnsw:space": "cosine"},
        )

    def upsert_chunks(self, chunks: list[TextChunk], embeddings: list[list[float]]) -> None:
        if not chunks:
            return
        self.collection.upsert(
            ids=[chunk.chunk_id for chunk in chunks],
            embeddings=embeddings,
            documents=[chunk.text for chunk in chunks],
            metadatas=[
                {
                    "document_id": chunk.document_id,
                    "document_name": chunk.document_name,
                    "page_number": chunk.page_number,
                    "chunk_id": chunk.chunk_id,
                }
                for chunk in chunks
            ],
        )

    def delete_document(self, document_id: str) -> None:
        try:
            self.collection.delete(where={"document_id": document_id})
        except Exception:  # noqa: BLE001
            return

    def query(
        self,
        embedding: list[float],
        top_k: int,
        document_ids: list[str] | None = None,
    ) -> list[dict]:
        count = self.collection.count()
        if count == 0:
            return []
        where = None
        if document_ids:
            if len(document_ids) == 1:
                where = {"document_id": document_ids[0]}
            else:
                where = {"document_id": {"$in": document_ids}}
        try:
            result = self.collection.query(
                query_embeddings=[embedding],
                n_results=min(max(top_k, 1), count),
                where=where,
                include=["documents", "metadatas", "distances"],
            )
        except Exception:  # noqa: BLE001
            return []
        items: list[dict] = []
        ids = (result.get("ids") or [[]])[0]
        docs = (result.get("documents") or [[]])[0]
        metas = (result.get("metadatas") or [[]])[0]
        distances = (result.get("distances") or [[]])[0]
        for chunk_id, text, meta, distance in zip(ids, docs, metas, distances):
            score = max(0.0, 1.0 - float(distance))
            items.append(
                {
                    "chunk_id": chunk_id,
                    "document_id": meta.get("document_id"),
                    "document_name": meta.get("document_name"),
                    "page_number": int(meta.get("page_number") or 1),
                    "excerpt": text,
                    "score": round(score, 4),
                }
            )
        return items

    def available(self) -> bool:
        try:
            self.collection.count()
            return True
        except Exception:  # noqa: BLE001
            return False


@lru_cache
def get_vector_store() -> VectorStore:
    return VectorStore()
