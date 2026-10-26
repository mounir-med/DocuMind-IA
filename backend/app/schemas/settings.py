from typing import Literal

from pydantic import BaseModel, Field


class PublicSettings(BaseModel):
    llm_provider: str
    llm_model: str
    llm_temperature: float
    llm_configured: bool
    has_api_key: bool
    embedding_provider: str
    embedding_model: str
    rag_top_k: int
    rag_score_threshold: float
    chunk_size: int
    chunk_overlap: int
    max_upload_mb: int
    app_name: str
    app_version: str


class SettingsUpdate(BaseModel):
    llm_provider: Literal["demo", "openai", "ollama"] | None = None
    llm_model: str | None = Field(default=None, min_length=1, max_length=120)
    llm_temperature: float | None = Field(default=None, ge=0, le=1)
    rag_top_k: int | None = Field(default=None, ge=1, le=20)
    rag_score_threshold: float | None = Field(default=None, ge=0, le=1)
