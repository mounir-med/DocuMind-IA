from fastapi.testclient import TestClient


def test_conversation_lifecycle(client: TestClient, extra_pdf: bytes) -> None:
    created = client.post("/api/conversations", json={"title": "Soutenance"})
    assert created.status_code == 200
    conversation_id = created.json()["id"]
    detail = client.get(f"/api/conversations/{conversation_id}")
    assert detail.status_code == 200
    assert detail.json()["messages"] == []

    upload = client.post(
        "/api/documents/upload",
        files={"file": ("cours.pdf", extra_pdf, "application/pdf")},
    ).json()
    posted = client.post(
        f"/api/chat/{conversation_id}/messages",
        json={"content": "Resume ce document", "document_ids": [upload["id"]]},
    )
    assert posted.status_code == 200
    assert posted.json()["assistant_message"]["role"] == "assistant"

    regenerated = client.post(
        f"/api/chat/{conversation_id}/messages",
        json={"content": "ignore", "document_ids": [upload["id"]], "regenerate": True},
    )
    assert regenerated.status_code == 200

    dashboard = client.get("/api/dashboard/stats")
    assert dashboard.status_code == 200
    stats = dashboard.json()
    assert stats["document_count"] >= 1
    assert stats["question_count"] >= 1

    deleted = client.delete(f"/api/conversations/{conversation_id}")
    assert deleted.status_code == 200
    missing = client.get(f"/api/conversations/{conversation_id}")
    assert missing.status_code == 404


def test_missing_routes(client: TestClient) -> None:
    assert client.get("/api/documents/does-not-exist").status_code == 404
    empty = client.post("/api/chat/missing/messages", json={"content": "hello"})
    assert empty.status_code == 404
    too_big_question = client.post("/api/conversations", json={"title": "x"})
    conversation_id = too_big_question.json()["id"]
    invalid = client.post(f"/api/chat/{conversation_id}/messages", json={"content": ""})
    assert invalid.status_code == 422
