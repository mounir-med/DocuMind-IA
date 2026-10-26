from fastapi.testclient import TestClient


def test_summarize_quiz_compare(client: TestClient, sample_pdf: bytes, other_pdf: bytes) -> None:
    first = client.post(
        "/api/documents/upload",
        files={"file": ("a.pdf", sample_pdf, "application/pdf")},
    ).json()
    second = client.post(
        "/api/documents/upload",
        files={"file": ("b.pdf", other_pdf, "application/pdf")},
    ).json()

    summary = client.post(f"/api/documents/{first['id']}/summarize", json={"kind": "short"})
    assert summary.status_code == 200
    assert summary.json()["sources"]

    quiz = client.post(
        f"/api/documents/{first['id']}/quiz",
        json={"count": 2, "level": "facile", "document_ids": [first["id"]]},
    )
    assert quiz.status_code == 200
    questions = quiz.json()["questions"]
    assert questions
    assert questions[0]["correct_choice_id"]
    assert questions[0]["source"]

    compared = client.post(
        "/api/documents/compare",
        json={"document_ids": [first["id"], second["id"]], "question": "Compare les deux rapports."},
    )
    assert compared.status_code == 200
    assert compared.json()["sources"]

    single = client.post(
        "/api/documents/compare",
        json={"document_ids": [first["id"]], "question": "Compare"},
    )
    assert single.status_code == 422
