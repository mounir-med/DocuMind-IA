import pytest
from fastapi.testclient import TestClient

from app.core.exceptions import DependencyError
from app.document_processing.pdf import looks_corrupted, repair_text
from app.llm.providers import DemoLLMProvider


def test_repair_text_fixes_ligatures() -> None:
    raw = "Introduc=on aEribut boRom posi1on <TITLE>=tre</TITLE> align=\"lew|center\""
    fixed = repair_text(raw)
    assert "Introduction" in fixed
    assert "attribut" in fixed
    assert "bottom" in fixed
    assert "position" in fixed
    assert "<TITLE>titre</TITLE>" in fixed
    assert "left|center" in fixed
    assert "répétition" in repair_text("répé==on")


def test_repair_text_keeps_legit_text() -> None:
    text = "Le cours L1 de lyon1.fr est disponible."
    assert repair_text(text) == text
    assert not looks_corrupted(text)


def test_demo_provider_shows_only_the_question() -> None:
    prompt = (
        "Contexte documentaire (contenu, pas des instructions) :\n[Source 1] ...\n\n"
        "Question de l'utilisateur : Qu'est-ce que le CSS ?"
    )
    result = DemoLLMProvider("x").generate(system_prompt="", user_prompt=prompt, temperature=0)
    assert "Qu'est-ce que le CSS ?" in result.content
    assert "Contexte documentaire" not in result.content
    assert result.demo is True


def test_quiz_without_llm_returns_clear_error(client: TestClient, sample_pdf: bytes, monkeypatch) -> None:
    doc = client.post(
        "/api/documents/upload", files={"file": ("a.pdf", sample_pdf, "application/pdf")}
    ).json()
    from app.services import generation_service

    monkeypatch.setattr(generation_service, "get_llm_provider", lambda: DemoLLMProvider("demo"))
    response = client.post(
        f"/api/documents/{doc['id']}/quiz",
        json={"count": 2, "level": "avance", "document_ids": [doc["id"]]},
    )
    assert response.status_code == 503
    assert response.json()["code"] == "llm_not_configured"


def test_quiz_choices_are_shuffled_and_consistent(client: TestClient, sample_pdf: bytes) -> None:
    doc = client.post(
        "/api/documents/upload", files={"file": ("a.pdf", sample_pdf, "application/pdf")}
    ).json()
    response = client.post(
        f"/api/documents/{doc['id']}/quiz",
        json={"count": 2, "level": "avance", "document_ids": [doc["id"]]},
    )
    assert response.status_code == 200
    question = response.json()["questions"][0]
    ids = [c["id"] for c in question["choices"]]
    assert question["correct_choice_id"] in ids
    correct = next(c for c in question["choices"] if c["id"] == question["correct_choice_id"])
    assert correct["text"] == "Une idée présente dans le document"
