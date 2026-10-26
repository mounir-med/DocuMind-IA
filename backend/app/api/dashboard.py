from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.embeddings.factory import get_embedding_provider
from app.llm.factory import get_llm_provider
from app.schemas.conversations import ConversationOut
from app.schemas.dashboard import DashboardStats
from app.schemas.documents import DocumentOut
from app.services import chat_service, document_service

router = APIRouter(tags=["dashboard"])


@router.get("/api/dashboard/stats", response_model=DashboardStats)
def stats(db: Session = Depends(get_db)) -> DashboardStats:
    documents = document_service.list_documents(db)
    conversations = chat_service.list_conversations(db)
    llm = get_llm_provider()
    embeddings = get_embedding_provider()
    return DashboardStats(
        document_count=len(documents),
        indexed_count=sum(1 for item in documents if item.status == "ready"),
        conversation_count=len(conversations),
        question_count=chat_service.message_count(db),
        recent_documents=[DocumentOut.model_validate(item) for item in documents[:5]],
        recent_conversations=[
            ConversationOut(
                id=item.id,
                title=item.title,
                created_at=item.created_at,
                updated_at=item.updated_at,
                message_count=chat_service.message_count(db, item.id),
            )
            for item in conversations[:5]
        ],
        llm_provider=llm.name,
        llm_ready=bool(llm.configured) and not getattr(llm, "demo", False),
        embedding_ready=embeddings.ready,
    )
