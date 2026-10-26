import re
import unicodedata

from app.core.config import get_settings
from app.embeddings.factory import get_embedding_provider
from app.vector_store.chroma import get_vector_store

STOPWORDS = {
    "a", "à", "au", "aux", "avec", "ce", "ces", "dans", "de", "des", "du", "elle",
    "en", "et", "est", "expliquer", "explique", "la", "le", "les", "leur", "ma", "mais",
    "me", "mon", "ne", "nos", "notre", "ou", "par", "pas", "pour", "que", "qui", "quoi",
    "sa", "se", "ses", "son", "sur", "ta", "te", "tes", "ton", "tu", "un", "une", "vos",
    "votre", "comment", "pourquoi", "document", "sélectionné", "selectionne", "sert", "utilité",
}


def _normalise(value: str) -> str:
    decomposed = unicodedata.normalize("NFKD", value.casefold())
    return "".join(char for char in decomposed if not unicodedata.combining(char))


def _terms(question: str) -> tuple[set[str], set[str]]:
    normalized = _normalise(question)
    tags = set(re.findall(r"<\s*/?\s*([a-z][a-z0-9]*)", normalized))
    tokens = set(re.findall(r"[a-z0-9]+", normalized))
    terms = {token for token in tokens if token not in STOPWORDS and len(token) >= 3}
    terms.update(tags)
    # Two-letter HTML elements such as ul, ol, li, h1 and h2 carry meaning.
    html_elements = {"ul", "ol", "li", "h1", "h2", "h3", "br", "td", "th"}
    terms.update(token for token in tokens if token in html_elements)
    tags.update(token for token in tokens if token in html_elements)
    return terms, tags


def _where(document_ids: list[str] | None) -> dict | None:
    if not document_ids:
        return None
    return {"document_id": document_ids[0]} if len(document_ids) == 1 else {"document_id": {"$in": document_ids}}


def retrieve(question: str, document_ids: list[str] | None = None, top_k: int | None = None) -> list[dict]:
    settings = get_settings()
    if document_ids is not None and len(document_ids) == 0:
        return []
    embeddings = get_embedding_provider()
    store = get_vector_store()
    query_vec = embeddings.embed([question])[0]
    limit = top_k or settings.rag_top_k
    semantic_hits = store.query(
        embedding=query_vec,
        top_k=min(limit * 3, 60),
        document_ids=document_ids,
    )
    # Embedding similarity alone often confuses nearby course topics (for example
    # HTML lists and CSS). Add exact term and HTML-tag matching from the same
    # selected documents before choosing the final passages.
    terms, tags = _terms(question)
    lexical_hits: list[dict] = []
    if terms:
        data = store.collection.get(where=_where(document_ids), include=["documents", "metadatas"])
        for chunk_id, text, meta in zip(data.get("ids", []), data.get("documents", []), data.get("metadatas", [])):
            normalized_text = _normalise(text or "")
            words = set(re.findall(r"[a-z0-9]+", normalized_text))
            matched = terms.intersection(words)
            if not matched:
                continue
            weighted_total = sum(3 if term in tags else 1 for term in terms)
            weighted_matches = sum(3 if term in tags else 1 for term in matched)
            lexical_score = weighted_matches / max(weighted_total, 1)
            exact_tag_bonus = 0.2 if tags and any(re.search(rf"<\s*/?\s*{re.escape(tag)}\b", normalized_text) for tag in tags) else 0
            lexical_hits.append({
                "chunk_id": chunk_id,
                "document_id": meta.get("document_id"),
                "document_name": meta.get("document_name"),
                "page_number": int(meta.get("page_number") or 1),
                "excerpt": text,
                "score": min(1.0, lexical_score + exact_tag_bonus),
            })

    merged: dict[str, dict] = {}
    for hit in semantic_hits:
        merged[hit["chunk_id"]] = {**hit, "_semantic_score": float(hit.get("score") or 0), "_lexical_score": 0.0}
    for hit in lexical_hits:
        current = merged.get(hit["chunk_id"], {**hit, "_semantic_score": 0.0, "_lexical_score": 0.0})
        current["_lexical_score"] = hit["score"]
        merged[hit["chunk_id"]] = current

    ranked = []
    for item in merged.values():
        semantic_score = item.pop("_semantic_score")
        lexical_score = item.pop("_lexical_score")
        if tags and tags.intersection(set(re.findall(r"[a-z0-9]+", _normalise(item["excerpt"])) )):
            combined_score = max(0.8, semantic_score * 0.2 + lexical_score * 0.8)
        else:
            combined_score = semantic_score * 0.45 + lexical_score * 0.55
        item["score"] = round(combined_score, 4)
        ranked.append(item)
    ranked.sort(key=lambda hit: hit["score"], reverse=True)
    threshold = settings.rag_score_threshold
    return [hit for hit in ranked if hit["score"] >= threshold][:limit]
