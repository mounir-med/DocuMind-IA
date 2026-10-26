"""Évaluation locale du retriever RAG. N'appelle pas de fournisseur LLM payant."""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

os.environ.setdefault("LLM_PROVIDER", "fake")
os.environ.setdefault("EMBEDDING_PROVIDER", "fake")
os.environ.setdefault("RAG_SCORE_THRESHOLD", "0.0")

import fitz

from app.core.config import get_settings
from app.core.db import init_db, reset_engine
from app.document_processing.chunking import chunk_pages
from app.document_processing.pdf import extract_pdf
from app.embeddings.factory import get_embedding_provider
from app.rag.retriever import retrieve
from app.vector_store.chroma import get_vector_store


def pdf_from_pages(pages: list[str]) -> bytes:
    document = fitz.open()
    for text in pages:
        page = document.new_page()
        page.insert_text((72, 72), text)
    payload = document.tobytes()
    document.close()
    return payload


def main() -> None:
    get_settings.cache_clear()
    get_embedding_provider.cache_clear()
    get_vector_store.cache_clear()
    reset_engine()
    get_settings().ensure_directories()
    init_db()

    spec = json.loads((ROOT / "evaluation" / "questions.json").read_text(encoding="utf-8"))
    store = get_vector_store()
    embedder = get_embedding_provider()

    doc_ids: dict[str, str] = {}
    for index, item in enumerate(spec["corpus"], start=1):
        document_id = f"eval-{index}"
        payload = pdf_from_pages(item["pages"])
        pages = extract_pdf(payload).pages
        chunks = chunk_pages(
            document_id=document_id,
            document_name=item["filename"],
            pages=pages,
            chunk_size=get_settings().chunk_size,
            overlap=get_settings().chunk_overlap,
        )
        vectors = embedder.embed([chunk.text for chunk in chunks])
        store.delete_document(document_id)
        store.upsert_chunks(chunks, vectors)
        doc_ids[item["filename"]] = document_id

    latencies: list[float] = []
    hits = 0
    mrr_total = 0.0
    rows = []
    for case in spec["cases"]:
        start = time.perf_counter()
        sources = retrieve(case["question"], document_ids=[doc_ids[case["document"]]], top_k=5)
        elapsed = time.perf_counter() - start
        latencies.append(elapsed)
        rank = None
        tokens = [token.lower() for token in case.get("must_contain_any") or []]
        for position, source in enumerate(sources, start=1):
            excerpt = source["excerpt"].lower()
            if tokens and any(token in excerpt for token in tokens):
                rank = position
                break
        if case["unanswerable"]:
            joined = " ".join(item["excerpt"].lower() for item in sources)
            ok = "wifi" not in joined and "mot de passe" not in joined
        else:
            ok = rank is not None
            if rank:
                mrr_total += 1 / rank
                hits += 1
        rows.append({"id": case["id"], "ok": ok, "k": len(sources), "latency_ms": round(elapsed * 1000, 1)})

    answered = [case for case in spec["cases"] if not case["unanswerable"]]
    report = {
        "cases": rows,
        "recall_at_k": hits / max(len(answered), 1),
        "mrr": mrr_total / max(len(answered), 1),
        "avg_latency_ms": round(sum(latencies) / len(latencies) * 1000, 1),
        "note": "Métriques calculées avec embeddings factices déterministes, pas un modèle de production.",
    }
    out = ROOT / "evaluation" / "last_report.json"
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
