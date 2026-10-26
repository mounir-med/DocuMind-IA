from dataclasses import dataclass, field
from typing import Protocol


@dataclass
class LLMResult:
    content: str
    provider: str
    model: str
    demo: bool = False
    error: str | None = None
    usage: dict = field(default_factory=dict)


class LLMProvider(Protocol):
    name: str
    model: str
    configured: bool
    demo: bool

    def generate(self, *, system_prompt: str, user_prompt: str, temperature: float) -> LLMResult:
        ...
