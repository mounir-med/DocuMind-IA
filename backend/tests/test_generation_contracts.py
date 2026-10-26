from fastapi.testclient import TestClient


def test_summary_kind_is_required_to_be_supported(client: TestClient, sample_pdf: bytes) -> None:
    document = client.post(
        "/api/documents/upload", files={"file": ("summary.pdf", sample_pdf, "application/pdf")}
    ).json()
    response = client.post(f"/api/documents/{document['id']}/summarize", json={"kind": "unknown"})
    assert response.status_code == 422


def test_each_summary_kind_has_distinct_instruction_and_selected_source(
    client: TestClient, sample_pdf: bytes, monkeypatch
) -> None:
    from app.services import generation_service

    document = client.post(
        "/api/documents/upload", files={"file": ("summary.pdf", sample_pdf, "application/pdf")}
    ).json()
    captured = []

    def fake_answer(_question, *, document_ids, extra, sources, **_kwargs):
        captured.append((extra, document_ids, sources))
        return {"content": extra, "sources": sources, "generation": {"demo": False}}

    monkeypatch.setattr(generation_service, "answer_question", fake_answer)
    db = _db_session()
    try:
        for kind in generation_service.SUMMARY_KINDS:
            result = generation_service.summarize_document(db, document["id"], kind)
            assert result["kind"] == kind
    finally:
        db.close()

    assert len(captured) == 6
    assert len({instruction for instruction, _, _ in captured}) == 6
    assert all(ids == [document["id"]] for _, ids, _ in captured)
    assert all(sources and all(s["document_id"] == document["id"] for s in sources) for _, _, sources in captured)


def _db_session():
    # Exercise the real service and isolated test database used by the API fixtures.
    from app.core.db import get_session_factory

    return get_session_factory()()


def test_quiz_rejects_unknown_level(client: TestClient, sample_pdf: bytes) -> None:
    document = client.post(
        "/api/documents/upload", files={"file": ("quiz.pdf", sample_pdf, "application/pdf")}
    ).json()
    response = client.post(
        f"/api/documents/{document['id']}/quiz",
        json={"count": 1, "level": "expert", "document_ids": [document["id"]]},
    )
    assert response.status_code == 422
