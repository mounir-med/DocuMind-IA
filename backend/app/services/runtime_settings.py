from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.llm.factory import get_llm_provider
from app.models.entities import AppSetting
from app.schemas.settings import PublicSettings, SettingsUpdate


OVERRIDABLE = {"llm_provider", "llm_model", "llm_temperature", "rag_top_k", "rag_score_threshold"}


def _load_overrides(db: Session) -> dict[str, str]:
    rows = db.query(AppSetting).all()
    return {row.key: row.value for row in rows}


def apply_overrides(db: Session) -> None:
    settings = get_settings()
    overrides = _load_overrides(db)
    if "llm_provider" in overrides:
        settings.llm_provider = overrides["llm_provider"]
    if "llm_model" in overrides:
        settings.llm_model = overrides["llm_model"]
        # The settings screen exposes one active model field for all providers.
        settings.ollama_model = overrides["llm_model"]
    if "llm_temperature" in overrides:
        settings.llm_temperature = float(overrides["llm_temperature"])
    if "rag_top_k" in overrides:
        settings.rag_top_k = int(overrides["rag_top_k"])
    if "rag_score_threshold" in overrides:
        settings.rag_score_threshold = float(overrides["rag_score_threshold"])
    get_llm_provider.cache_clear()


def public_settings(db: Session) -> PublicSettings:
    apply_overrides(db)
    settings = get_settings()
    llm = get_llm_provider()
    return PublicSettings(
        llm_provider=settings.llm_provider,
        llm_model=llm.model,
        llm_temperature=settings.llm_temperature,
        llm_configured=bool(llm.configured) and settings.llm_provider != "demo",
        has_api_key=bool(settings.openai_api_key),
        embedding_provider=settings.embedding_provider,
        embedding_model=settings.embedding_model,
        rag_top_k=settings.rag_top_k,
        rag_score_threshold=settings.rag_score_threshold,
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
        max_upload_mb=settings.max_upload_mb,
        app_name=settings.app_name,
        app_version=settings.app_version,
    )


def update_settings(db: Session, payload: SettingsUpdate) -> PublicSettings:
    data = payload.model_dump(exclude_none=True)
    for key, value in data.items():
        if key not in OVERRIDABLE:
            continue
        row = db.get(AppSetting, key)
        if row is None:
            row = AppSetting(key=key, value=str(value))
            db.add(row)
        else:
            row.value = str(value)
    db.commit()
    get_llm_provider.cache_clear()
    return public_settings(db)
