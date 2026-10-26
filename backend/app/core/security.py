import re
from pathlib import Path


UNSAFE_CHARS = re.compile(r"[^A-Za-z0-9._-]+")


def sanitize_filename(name: str) -> str:
    cleaned = Path(name.replace("\\", "/")).name
    cleaned = UNSAFE_CHARS.sub("_", cleaned).strip("._")
    if not cleaned.lower().endswith(".pdf"):
        cleaned = f"{cleaned or 'document'}.pdf"
    return cleaned[:180]


def is_pdf_header(payload: bytes) -> bool:
    return payload.lstrip().startswith(b"%PDF")
