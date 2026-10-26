from datetime import datetime

from typing import Literal

from pydantic import BaseModel, Field


class DocumentOut(BaseModel):
    id: str
    filename: str
    sha256: str
    size_bytes: int
    page_count: int
    chunk_count: int
    status: str
    error_message: str | None = None
    created_at: datetime
    indexed_at: datetime | None = None

    model_config = {"from_attributes": True}


class PageOut(BaseModel):
    document_id: str
    page_number: int
    text: str


class SummarizeRequest(BaseModel):
    kind: Literal["short", "detailed", "chapters", "ideas", "definitions", "revision"] = "short"


class SummarizeResponse(BaseModel):
    document_id: str
    kind: str
    content: str
    sources: list[dict]
    generation: dict
