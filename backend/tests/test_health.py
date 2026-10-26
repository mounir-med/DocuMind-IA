from fastapi.testclient import TestClient


def test_health(client: TestClient) -> None:
    response = client.get("/api/health")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["llm"]["provider"] == "fake"
    assert payload["embeddings"]["ready"] is True
    assert payload["vector_store"] is True
