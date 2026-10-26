from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.rate_limit import chat_limiter, client_key
from app.schemas.chat import ChatMessageRequest, ChatMessageResponse
from app.services import chat_service

router = APIRouter(tags=["chat"])


@router.post("/api/chat/{conversation_id}/messages", response_model=ChatMessageResponse)
def post_message(
    conversation_id: str,
    payload: ChatMessageRequest,
    request: Request,
    db: Session = Depends(get_db),
) -> ChatMessageResponse:
    chat_limiter.check(client_key(request))
    result = chat_service.add_message(
        db,
        conversation_id,
        payload.content,
        payload.document_ids,
        regenerate=payload.regenerate,
    )
    return ChatMessageResponse(**result)
