import json
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError, ValidationAppError
from app.models.entities import Conversation, Message
from app.rag.pipeline import answer_question
from app.services.runtime_settings import apply_overrides


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _sources(raw: str | None) -> list[dict]:
    if not raw:
        return []
    try:
        data = json.loads(raw)
        return data if isinstance(data, list) else []
    except json.JSONDecodeError:
        return []


def _meta(raw: str | None) -> dict:
    if not raw:
        return {}
    try:
        data = json.loads(raw)
        return data if isinstance(data, dict) else {}
    except json.JSONDecodeError:
        return {}


def serialize_message(message: Message) -> dict:
    return {
        "id": message.id,
        "conversation_id": message.conversation_id,
        "role": message.role,
        "content": message.content,
        "sources": _sources(message.sources_json),
        "generation": _meta(message.meta_json),
        "created_at": message.created_at,
    }


def list_conversations(db: Session) -> list[Conversation]:
    return db.query(Conversation).order_by(Conversation.updated_at.desc()).all()


def get_conversation(db: Session, conversation_id: str) -> Conversation:
    conversation = db.get(Conversation, conversation_id)
    if conversation is None:
        raise NotFoundError("Conversation introuvable.")
    return conversation


def create_conversation(db: Session, title: str) -> Conversation:
    conversation = Conversation(title=title.strip() or "Nouvelle conversation")
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return conversation


def delete_conversation(db: Session, conversation_id: str) -> None:
    conversation = get_conversation(db, conversation_id)
    db.delete(conversation)
    db.commit()


def delete_all_conversations(db: Session) -> int:
    items = list_conversations(db)
    count = len(items)
    for conversation in items:
        db.delete(conversation)
    db.commit()
    return count


def message_count(db: Session, conversation_id: str | None = None) -> int:
    query = db.query(Message).filter(Message.role == "user")
    if conversation_id:
        query = query.filter(Message.conversation_id == conversation_id)
    return query.count()


def add_message(
    db: Session,
    conversation_id: str,
    content: str,
    document_ids: list[str],
    regenerate: bool = False,
) -> dict:
    conversation = get_conversation(db, conversation_id)
    question = content.strip()
    if not question:
        raise ValidationAppError("La question ne peut pas être vide.")

    if regenerate:
        last_user = (
            db.query(Message)
            .filter(Message.conversation_id == conversation_id, Message.role == "user")
            .order_by(Message.created_at.desc())
            .first()
        )
        if last_user is None:
            raise ValidationAppError("Aucune question à régénérer.")
        question = last_user.content
        last_assistant = (
            db.query(Message)
            .filter(Message.conversation_id == conversation_id, Message.role == "assistant")
            .order_by(Message.created_at.desc())
            .first()
        )
        if last_assistant:
            db.delete(last_assistant)
            db.commit()
        user_message = last_user
    else:
        user_message = Message(conversation_id=conversation.id, role="user", content=question)
        db.add(user_message)
        db.commit()
        db.refresh(user_message)

    apply_overrides(db)
    result = answer_question(question, document_ids=document_ids)
    assistant = Message(
        conversation_id=conversation.id,
        role="assistant",
        content=result["content"],
        sources_json=json.dumps(result["sources"], ensure_ascii=False),
        meta_json=json.dumps(result["generation"], ensure_ascii=False),
    )
    db.add(assistant)
    if conversation.title == "Nouvelle conversation":
        conversation.title = question[:80]
    conversation.updated_at = _now()
    db.commit()
    db.refresh(assistant)
    return {
        "user_message": serialize_message(user_message),
        "assistant_message": serialize_message(assistant),
    }
