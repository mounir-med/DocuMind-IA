from pydantic import BaseModel, Field


class ChatMessageRequest(BaseModel):
    content: str = Field(min_length=1, max_length=8000)
    document_ids: list[str] = Field(default_factory=list)
    regenerate: bool = False


class SourceOut(BaseModel):
    chunk_id: str
    document_id: str
    document_name: str
    page_number: int
    excerpt: str
    score: float | None = None


class ChatMessageResponse(BaseModel):
    user_message: dict
    assistant_message: dict
