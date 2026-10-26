from fastapi.testclient import TestClient


def _upload(client: TestClient, payload: bytes, name: str) -> dict:
    response = client.post(
        "/api/documents/upload",
        files={"file": (name, payload, "application/pdf")},
    )
    assert response.status_code == 200, response.text
    return response.json()


def test_upload_index_search_filter_delete(client: TestClient, sample_pdf: bytes, other_pdf: bytes) -> None:
    first = _upload(client, sample_pdf, "photosynthese.pdf")
    second = _upload(client, other_pdf, "respiration.pdf")
    assert first["status"] == "ready"
    assert first["page_count"] == 2
    assert first["chunk_count"] >= 1

    duplicate = client.post(
        "/api/documents/upload",
        files={"file": ("copy.pdf", sample_pdf, "application/pdf")},
    )
    assert duplicate.status_code == 422

    conversation = client.post("/api/conversations", json={"title": "Test RAG"}).json()
    filtered = client.post(
        f"/api/chat/{conversation['id']}/messages",
        json={"content": "Quels sont les reactifs de la photosynthese ?", "document_ids": [first["id"]]},
    )
    assert filtered.status_code == 200
    sources = filtered.json()["assistant_message"]["sources"]
    assert sources
    assert all(item["document_id"] == first["id"] for item in sources)
    assert all("page_number" in item and item["excerpt"] for item in sources)

    unanswerable = client.post(
        f"/api/chat/{conversation['id']}/messages",
        json={"content": "Quel est le mot de passe Wi-Fi du campus ?", "document_ids": [first["id"]]},
    )
    assert unanswerable.status_code == 200
    generation = unanswerable.json()["assistant_message"]["generation"]
    assert "insufficient_context" in generation or unanswerable.json()["assistant_message"]["content"]

    listed = client.get("/api/documents").json()
    assert len(listed) >= 2
    deleted = client.delete(f"/api/documents/{second['id']}")
    assert deleted.status_code == 200
    remaining = {item["id"] for item in client.get("/api/documents").json()}
    assert second["id"] not in remaining

    after_delete = client.post(
        f"/api/chat/{conversation['id']}/messages",
        json={"content": "respiration cellulaire glucose", "document_ids": [second["id"]]},
    )
    assert after_delete.status_code == 200
    assert after_delete.json()["assistant_message"]["sources"] == []


def test_invalid_and_empty_upload(client: TestClient) -> None:
    invalid = client.post(
        "/api/documents/upload",
        files={"file": ("bad.pdf", b"not-a-pdf", "application/pdf")},
    )
    assert invalid.status_code == 422

    from tests.conftest import make_pdf_bytes

    empty = client.post(
        "/api/documents/upload",
        files={"file": ("empty.pdf", make_pdf_bytes([""]), "application/pdf")},
    )
    assert empty.status_code == 200
    assert empty.json()["status"] in {"empty", "scanned"}


def test_hybrid_retrieval_prefers_exact_html_tag_source(client: TestClient) -> None:
    from app.rag.retriever import retrieve
    from tests.conftest import make_pdf_bytes

    filler = "Présentation générale " + "cours " * 120 + "."
    payload = make_pdf_bytes(
        [
            filler,
            "Balises <UL>, <OL>, <LI> : les listes. <UL> signifie Unnumbered List et crée une liste non numérotée.",
        ]
    )
    document = _upload(client, payload, "html-listes.pdf")
    hits = retrieve("À quoi sert la balise <ul> ?", document_ids=[document["id"]], top_k=3)
    assert hits
    assert hits[0]["page_number"] == 2
    assert "Unnumbered List" in hits[0]["excerpt"]
