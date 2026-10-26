import os
from pathlib import Path

TEST_ROOT = Path(__file__).resolve().parent / "_tmp_data"
TEST_ROOT.mkdir(parents=True, exist_ok=True)
os.environ["DATA_DIR"] = str(TEST_ROOT)
os.environ["LLM_PROVIDER"] = "fake"
os.environ["EMBEDDING_PROVIDER"] = "fake"
os.environ["RAG_SCORE_THRESHOLD"] = "0.0"
os.environ["RAG_TOP_K"] = "5"
os.environ["CORS_ORIGINS"] = "http://testserver"

from app.core.config import get_settings  # noqa: E402
from app.core.db import init_db, reset_engine  # noqa: E402
from app.embeddings.factory import get_embedding_provider  # noqa: E402
from app.llm.factory import get_llm_provider  # noqa: E402
from app.vector_store.chroma import get_vector_store  # noqa: E402

get_settings.cache_clear()
get_embedding_provider.cache_clear()
get_llm_provider.cache_clear()
get_vector_store.cache_clear()
reset_engine()
get_settings().ensure_directories()
init_db()

import fitz  # noqa: E402
import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402


def make_pdf_bytes(pages: list[str]) -> bytes:
    document = fitz.open()
    for text in pages:
        page = document.new_page()
        if text:
            page.insert_text((72, 72), text)
    payload = document.tobytes()
    document.close()
    return payload


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def sample_pdf() -> bytes:
    return make_pdf_bytes(
        [
            "DocuMind est un assistant RAG. La photosynthesis convertit la lumiere en energie chimique. Unique A.",
            "Le chapitre 2 explique que l'eau et le dioxyde de carbone sont les reactifs de la photosynthese.",
        ]
    )


@pytest.fixture
def other_pdf() -> bytes:
    return make_pdf_bytes(
        [
            "Rapport B : la respiration cellulaire consomme du glucose et produit du dioxyde de carbone. Unique B.",
            "Conclusion B : respiration et photosynthese sont des processus complementaires.",
        ]
    )


@pytest.fixture
def extra_pdf() -> bytes:
    return make_pdf_bytes(
        [
            "Cours C unique. La photosynthesis convertit la lumiere. L'eau et le dioxyde de carbone sont les reactifs.",
            "Le glucose est un produit. Unique C.",
        ]
    )
