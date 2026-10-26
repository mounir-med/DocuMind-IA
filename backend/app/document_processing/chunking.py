from dataclasses import dataclass
import re

from app.document_processing.clean import clean_text
from app.document_processing.pdf import PageText

SENTENCE_SPLIT = re.compile(r"(?<=[\.!?…])\s+")


@dataclass
class TextChunk:
    chunk_id: str
    document_id: str
    document_name: str
    page_number: int
    text: str
    index: int


def _split_sentences(text: str) -> list[str]:
    parts = SENTENCE_SPLIT.split(text)
    return [part.strip() for part in parts if part.strip()]


def chunk_pages(
    *,
    document_id: str,
    document_name: str,
    pages: list[PageText],
    chunk_size: int,
    overlap: int,
) -> list[TextChunk]:
    chunks: list[TextChunk] = []
    buffer: list[tuple[int, str]] = []
    current_len = 0
    index = 0

    def flush(force: bool = False) -> None:
        nonlocal buffer, current_len, index
        if not buffer:
            return
        if not force and current_len < chunk_size:
            return
        text = " ".join(item[1] for item in buffer).strip()
        if not text:
            buffer = []
            current_len = 0
            return
        page_number = buffer[0][0]
        chunks.append(
            TextChunk(
                chunk_id=f"{document_id}:{index}",
                document_id=document_id,
                document_name=document_name,
                page_number=page_number,
                text=text,
                index=index,
            )
        )
        index += 1
        if overlap > 0 and not force:
            kept: list[tuple[int, str]] = []
            kept_len = 0
            for item in reversed(buffer):
                if kept_len + len(item[1]) > overlap:
                    break
                kept.append(item)
                kept_len += len(item[1]) + 1
            buffer = list(reversed(kept))
            current_len = kept_len
        else:
            buffer = []
            current_len = 0

    for page in pages:
        cleaned = clean_text(page.text)
        if not cleaned:
            continue
        sentences = _split_sentences(cleaned) or [cleaned]
        for sentence in sentences:
            buffer.append((page.page_number, sentence))
            current_len += len(sentence) + 1
            if current_len >= chunk_size:
                flush()
        # Never carry overlap across a page boundary: each chunk's page number
        # must identify the page containing its text and citations.
        flush(force=True)

    return chunks
