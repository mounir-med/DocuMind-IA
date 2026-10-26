import pytest

from app.core.exceptions import ValidationAppError
from app.document_processing.chunking import chunk_pages
from app.document_processing.pdf import extract_pdf
from tests.conftest import make_pdf_bytes


def test_extract_valid_pdf() -> None:
    payload = make_pdf_bytes(["Page une avec du texte utile.", "Page deux avec une definition."])
    result = extract_pdf(payload)
    assert result.page_count == 2
    assert "Page une" in result.pages[0].text
    assert result.pages[1].page_number == 2
    assert result.likely_scanned is False


def test_extract_invalid_pdf() -> None:
    with pytest.raises(ValidationAppError):
        extract_pdf(b"this is not a pdf")


def test_extract_empty_pdf() -> None:
    payload = make_pdf_bytes(["", ""])
    result = extract_pdf(payload)
    assert result.char_count == 0
    assert result.likely_scanned is True


def test_chunking_keeps_page_numbers() -> None:
    payload = make_pdf_bytes(
        [
            "Phrase A. Phrase B. Phrase C. Phrase D. Phrase E. Phrase F.",
            "Phrase G. Phrase H. Phrase I. Phrase J. Phrase K. Phrase L.",
        ]
    )
    pages = extract_pdf(payload).pages
    chunks = chunk_pages(
        document_id="doc-1",
        document_name="cours.pdf",
        pages=pages,
        chunk_size=40,
        overlap=10,
    )
    assert chunks
    assert all(chunk.page_number in {1, 2} for chunk in chunks)
    assert chunks[0].document_id == "doc-1"
    assert "Phrase" in chunks[0].text
