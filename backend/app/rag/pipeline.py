from app.core.config import get_settings
from app.core.exceptions import DependencyError
from app.llm.factory import get_llm_provider
from app.rag.prompts import SYSTEM_PROMPT, build_user_prompt
from app.rag.retriever import retrieve


def answer_question(
    question: str,
    document_ids: list[str] | None = None,
    extra: str = "",
    top_k: int | None = None,
    sources: list[dict] | None = None,
) -> dict:
    settings = get_settings()
    if sources is None:
        sources = retrieve(question, document_ids=document_ids, top_k=top_k)
    llm = get_llm_provider()
    if not sources:
        content = (
            "Aucun passage suffisamment pertinent n'a été retrouvé dans les documents "
            "sélectionnés. Reformulez la question ou élargissez la sélection."
        )
        return {
            "content": content,
            "sources": [],
            "generation": {
                "provider": llm.name,
                "model": llm.model,
                "demo": getattr(llm, "demo", False),
                "insufficient_context": True,
            },
        }

    result = llm.generate(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=build_user_prompt(question, sources, extra=extra),
        temperature=settings.llm_temperature,
    )
    if result.error:
        raise DependencyError(result.content, code=result.error)
    if not result.content or not result.content.strip():
        raise DependencyError("Le fournisseur IA a renvoyé une réponse vide. Réessayez ou vérifiez le modèle.", code="empty_response")
    content = result.content
    return {
        "content": content,
        "sources": sources,
        "generation": {
            "provider": result.provider,
            "model": result.model,
            "demo": result.demo,
            "error": result.error,
            "usage": result.usage,
            "insufficient_context": False,
        },
    }
