from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.db import get_db
from app.core.exceptions import ValidationAppError
from app.core.rate_limit import client_key, upload_limiter
from app.core.security import is_pdf_header
from app.schemas.documents import DocumentOut, PageOut, SummarizeRequest, SummarizeResponse
from app.schemas.quiz import CompareRequest, CompareResponse, QuizRequest, QuizResponse
from app.services import document_service, generation_service

router = APIRouter(tags=["documents"])


@router.post("/api/documents/upload", response_model=DocumentOut)
async def upload_document(
    request: Request,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> DocumentOut:
    upload_limiter.check(client_key(request))
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise ValidationAppError("Seuls les fichiers PDF sont acceptés.")
    # Read at most one byte beyond the configured limit so a large upload cannot
    # consume unbounded memory before the service rejects it.
    max_bytes = get_settings().max_upload_bytes
    payload = await file.read(max_bytes + 1)
    if len(payload) > max_bytes:
        raise HTTPException(status_code=413, detail=f"Fichier trop volumineux (max {get_settings().max_upload_mb} Mo).")
    if not is_pdf_header(payload):
        raise ValidationAppError("Le fichier n'est pas un PDF valide.")
    document = document_service.upload_document(db, file.filename, payload)
    return DocumentOut.model_validate(document)


@router.get("/api/documents", response_model=list[DocumentOut])
def list_documents(db: Session = Depends(get_db)) -> list[DocumentOut]:
    return [DocumentOut.model_validate(item) for item in document_service.list_documents(db)]


@router.get("/api/documents/{document_id}", response_model=DocumentOut)
def get_document(document_id: str, db: Session = Depends(get_db)) -> DocumentOut:
    return DocumentOut.model_validate(document_service.get_document(db, document_id))


@router.delete("/api/documents/{document_id}")
def delete_document(document_id: str, db: Session = Depends(get_db)) -> dict:
    document_service.delete_document(db, document_id)
    return {"ok": True}


@router.post("/api/documents/{document_id}/index", response_model=DocumentOut)
def reindex_document(document_id: str, db: Session = Depends(get_db)) -> DocumentOut:
    document = document_service.index_document(db, document_id)
    return DocumentOut.model_validate(document)


@router.get("/api/documents/{document_id}/file")
def download_document(document_id: str, db: Session = Depends(get_db)) -> FileResponse:
    document = document_service.get_document(db, document_id)
    path = document_service.stored_path(document)
    return FileResponse(path, media_type="application/pdf", filename=document.filename)


@router.get("/api/documents/{document_id}/pages/{page_number}", response_model=PageOut)
def get_page(document_id: str, page_number: int, db: Session = Depends(get_db)) -> PageOut:
    document = document_service.get_document(db, document_id)
    text = document_service.get_page_text(document, page_number)
    return PageOut(document_id=document.id, page_number=page_number, text=text)


@router.post("/api/documents/{document_id}/summarize", response_model=SummarizeResponse)
def summarize(document_id: str, payload: SummarizeRequest, db: Session = Depends(get_db)) -> SummarizeResponse:
    result = generation_service.summarize_document(db, document_id, payload.kind)
    return SummarizeResponse(**result)


@router.post("/api/documents/{document_id}/quiz", response_model=QuizResponse)
def quiz(document_id: str, payload: QuizRequest, db: Session = Depends(get_db)) -> QuizResponse:
    ids = payload.document_ids or [document_id]
    result = generation_service.generate_quiz(db, ids, payload.count, payload.level)
    return QuizResponse(**result)


@router.post("/api/documents/compare", response_model=CompareResponse)
def compare(payload: CompareRequest, db: Session = Depends(get_db)) -> CompareResponse:
    result = generation_service.compare_documents(db, payload.document_ids, payload.question)
    return CompareResponse(**result)


@router.get("/api/config/limits")
def limits() -> dict:
    settings = get_settings()
    return {"max_upload_mb": settings.max_upload_mb}
