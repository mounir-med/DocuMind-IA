import hashlib
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.exceptions import NotFoundError, ValidationAppError
from app.core.security import sanitize_filename
from app.document_processing.chunking import chunk_pages
from app.document_processing.clean import clean_text
from app.document_processing.pdf import extract_pdf
from app.embeddings.factory import get_embedding_provider
from app.models.entities import Document
from app.vector_store.chroma import get_vector_store


def _now() -> datetime:
    return datetime.now(timezone.utc)


def list_documents(db: Session) -> list[Document]:
    return db.query(Document).order_by(Document.created_at.desc()).all()


def get_document(db: Session, document_id: str) -> Document:
    document = db.get(Document, document_id)
    if document is None:
        raise NotFoundError("Document introuvable.")
    return document


def stored_path(document: Document) -> Path:
    return get_settings().uploads_dir / document.stored_name


def upload_document(db: Session, filename: str, payload: bytes) -> Document:
    settings = get_settings()
    if len(payload) > settings.max_upload_bytes:
        raise ValidationAppError(f"Fichier trop volumineux (max {settings.max_upload_mb} Mo).")
    digest = hashlib.sha256(payload).hexdigest()
    existing = db.query(Document).filter(Document.sha256 == digest).first()
    if existing:
        raise ValidationAppError("Ce PDF a déjà été importé (empreinte SHA-256 identique).")

    document_id = str(uuid4())
    stored_name = f"{document_id}.pdf"
    path = settings.uploads_dir / stored_name
    path.write_bytes(payload)

    document = Document(
        id=document_id,
        filename=sanitize_filename(filename),
        stored_name=stored_name,
        sha256=digest,
        size_bytes=len(payload),
        status="pending",
    )
    db.add(document)
    db.commit()
    db.refresh(document)
    return index_document(db, document.id, payload)


def index_document(db: Session, document_id: str, payload: bytes | None = None) -> Document:
    document = get_document(db, document_id)
    document.status = "indexing"
    document.error_message = None
    db.commit()

    try:
        data = payload if payload is not None else stored_path(document).read_bytes()
        extraction = extract_pdf(data)
        document.page_count = extraction.page_count
        if extraction.likely_scanned:
            document.status = "scanned"
            document.chunk_count = 0
            document.error_message = (
                "PDF probablement scanné : aucun texte extractible. "
                "OCR (Tesseract) n'est pas activé dans cette version."
            )
            get_vector_store().delete_document(document.id)
            db.commit()
            db.refresh(document)
            return document
        if extraction.char_count < 40:
            document.status = "empty"
            document.chunk_count = 0
            document.error_message = "Le document ne contient pas assez de texte extractible."
            get_vector_store().delete_document(document.id)
            db.commit()
            db.refresh(document)
            return document

        chunks = chunk_pages(
            document_id=document.id,
            document_name=document.filename,
            pages=extraction.pages,
            chunk_size=get_settings().chunk_size,
            overlap=get_settings().chunk_overlap,
        )
        embeddings = get_embedding_provider().embed([chunk.text for chunk in chunks])
        store = get_vector_store()
        store.delete_document(document.id)
        store.upsert_chunks(chunks, embeddings)
        document.chunk_count = len(chunks)
        document.status = "ready"
        document.indexed_at = _now()
        document.error_message = None
    except Exception as exc:  # noqa: BLE001
        document.status = "error"
        document.error_message = str(exc)
        db.commit()
        db.refresh(document)
        raise

    db.commit()
    db.refresh(document)
    return document


def delete_document(db: Session, document_id: str) -> None:
    document = get_document(db, document_id)
    get_vector_store().delete_document(document.id)
    path = stored_path(document)
    if path.exists():
        path.unlink()
    db.delete(document)
    db.commit()


def get_page_text(document: Document, page_number: int) -> str:
    if page_number < 1 or page_number > max(document.page_count, 1):
        raise ValidationAppError("Numéro de page invalide.")
    data = stored_path(document).read_bytes()
    extraction = extract_pdf(data)
    for page in extraction.pages:
        if page.page_number == page_number:
            return clean_text(page.text)
    return ""
