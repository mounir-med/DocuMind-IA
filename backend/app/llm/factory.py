from functools import lru_cache

from app.core.config import get_settings
from app.llm.providers import DemoLLMProvider, FakeLLMProvider, OllamaProvider, OpenAICompatProvider


@lru_cache
def get_llm_provider():
    settings = get_settings()
    provider = settings.llm_provider.lower()
    if provider == "fake":
        return FakeLLMProvider(settings.llm_model)
    if provider == "openai":
        return OpenAICompatProvider(settings)
    if provider == "ollama":
        return OllamaProvider(settings)
    return DemoLLMProvider(settings.llm_model)
