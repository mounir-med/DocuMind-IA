from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.schemas.conversations import ConversationCreate, ConversationDetail, ConversationOut, MessageOut
from app.services import chat_service

router = APIRouter(tags=["conversations"])


def _to_out(db: Session, conversation) -> ConversationOut:
    return ConversationOut(
        id=conversation.id,
        title=conversation.title,
        created_at=conversation.created_at,
        updated_at=conversation.updated_at,
        message_count=chat_service.message_count(db, conversation.id),
    )


@router.post("/api/conversations", response_model=ConversationOut)
def create_conversation(payload: ConversationCreate, db: Session = Depends(get_db)) -> ConversationOut:
    conversation = chat_service.create_conversation(db, payload.title)
    return _to_out(db, conversation)


@router.get("/api/conversations", response_model=list[ConversationOut])
def list_conversations(db: Session = Depends(get_db)) -> list[ConversationOut]:
    return [_to_out(db, item) for item in chat_service.list_conversations(db)]


@router.get("/api/conversations/{conversation_id}", response_model=ConversationDetail)
def get_conversation(conversation_id: str, db: Session = Depends(get_db)) -> ConversationDetail:
    conversation = chat_service.get_conversation(db, conversation_id)
    messages = [
        MessageOut(**chat_service.serialize_message(message))
        for message in sorted(conversation.messages, key=lambda item: item.created_at)
    ]
    base = _to_out(db, conversation)
    return ConversationDetail(**base.model_dump(), messages=messages)


@router.delete("/api/conversations")
def delete_all_conversations(db: Session = Depends(get_db)) -> dict:
    deleted = chat_service.delete_all_conversations(db)
    return {"ok": True, "deleted": deleted}


@router.delete("/api/conversations/{conversation_id}")
def delete_conversation(conversation_id: str, db: Session = Depends(get_db)) -> dict:
    chat_service.delete_conversation(db, conversation_id)
    return {"ok": True}
