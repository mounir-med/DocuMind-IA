from pydantic import BaseModel

from app.schemas.conversations import ConversationOut
from app.schemas.documents import DocumentOut


class DashboardStats(BaseModel):
    document_count: int
    indexed_count: int
    conversation_count: int
    question_count: int
    recent_documents: list[DocumentOut]
    recent_conversations: list[ConversationOut]
    llm_provider: str
    llm_ready: bool
    embedding_ready: bool
