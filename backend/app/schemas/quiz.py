from typing import Literal

from pydantic import BaseModel, Field


class QuizRequest(BaseModel):
    count: int = Field(default=5, ge=1, le=15)
    level: Literal["facile", "intermediaire", "avance"] = "intermediaire"
    document_ids: list[str] = Field(default_factory=list)


class QuizChoice(BaseModel):
    id: str
    text: str


class QuizQuestion(BaseModel):
    id: str
    question: str
    choices: list[QuizChoice]
    correct_choice_id: str
    explanation: str
    source: dict | None = None


class QuizResponse(BaseModel):
    document_ids: list[str]
    level: str
    questions: list[QuizQuestion]
    notice: str | None = None
    generation: dict


class CompareRequest(BaseModel):
    document_ids: list[str] = Field(min_length=2, max_length=5)
    question: str = Field(default="Compare ces documents.")


class CompareResponse(BaseModel):
    content: str
    sources: list[dict]
    generation: dict
