import json
import re

import httpx

from app.core.config import Settings
from app.llm.base import LLMResult


class DemoLLMProvider:
    name = "demo"
    demo = True
    configured = False

    def __init__(self, model: str) -> None:
        self.model = model

    @staticmethod
    def _extract_question(user_prompt: str) -> str:
        marker = "Question de l'utilisateur :"
        if marker in user_prompt:
            question = user_prompt.split(marker, 1)[1]
            question = question.split("\n\nConsigne supplémentaire", 1)[0]
            return question.strip()
        return user_prompt[:300]

    def generate(self, *, system_prompt: str, user_prompt: str, temperature: float) -> LLMResult:
        del system_prompt, temperature
        content = (
            "⚠️ **Mode démonstration** : aucun fournisseur LLM n'est configuré, "
            "aucune réponse IA n'a donc été générée.\n\n"
            "Les passages pertinents trouvés par la recherche sémantique sont affichés "
            "dans les sources ci-dessous.\n\n"
            "**Pour activer l'IA** : créez `backend/.env` avec `LLM_PROVIDER=ollama` "
            "(ou `openai` + `OPENAI_API_KEY`), puis redémarrez le backend.\n\n"
            f"Question : {self._extract_question(user_prompt)}"
        )
        return LLMResult(content=content, provider=self.name, model=self.model, demo=True)


class FakeLLMProvider:
    name = "fake"
    demo = False
    configured = True

    def __init__(self, model: str = "fake-llm") -> None:
        self.model = model

    def generate(self, *, system_prompt: str, user_prompt: str, temperature: float) -> LLMResult:
        del system_prompt, temperature
        if "JSON" in user_prompt or "json" in user_prompt:
            source_match = __import__("re").search(r"chunk_id=([^ ]+)", user_prompt)
            payload = {
                "questions": [
                    {
                        "id": "q1",
                        "question": "Quelle est l'idée principale du passage ?",
                        "choices": [
                            {"id": "a", "text": "Une idée présente dans le document"},
                            {"id": "b", "text": "Une information absente"},
                            {"id": "c", "text": "Une date inventée"},
                            {"id": "d", "text": "Un auteur inconnu"},
                        ],
                        "correct_choice_id": "a",
                        "explanation": "La bonne réponse s'appuie sur le passage fourni.",
                        "chunk_id": source_match.group(1) if source_match else "",
                    }
                ]
            }
            content = json.dumps(payload, ensure_ascii=False)
        else:
            content = (
                "Réponse fondée exclusivement sur les extraits fournis. "
                "Si une information n'apparaît pas dans le contexte, elle n'est pas affirmée."
            )
        return LLMResult(content=content, provider=self.name, model=self.model)


class OpenAICompatProvider:
    name = "openai"
    demo = False

    def __init__(self, settings: Settings) -> None:
        self.model = settings.llm_model
        self.api_key = settings.openai_api_key
        self.base_url = settings.openai_base_url.rstrip("/")
        self.configured = bool(self.api_key)

    def generate(self, *, system_prompt: str, user_prompt: str, temperature: float) -> LLMResult:
        if not self.configured:
            return LLMResult(
                content="Le fournisseur OpenAI n'est pas configuré.",
                provider=self.name,
                model=self.model,
                error="missing_api_key",
            )
        try:
            response = httpx.post(
                f"{self.base_url}/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "model": self.model,
                    "temperature": temperature,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                },
                timeout=90.0,
            )
        except httpx.TimeoutException:
            return LLMResult(content="Le délai de réponse du fournisseur LLM a expiré.", provider=self.name, model=self.model, error="timeout")
        except httpx.HTTPError as exc:
            return LLMResult(
                content="Le fournisseur LLM est injoignable.",
                provider=self.name,
                model=self.model,
                error=type(exc).__name__,
            )
        if response.status_code == 401:
            return LLMResult(
                content="Clé API invalide.",
                provider=self.name,
                model=self.model,
                error="invalid_api_key",
            )
        if response.status_code == 429:
            return LLMResult(
                content="Quota API dépassé. Réessayez plus tard.",
                provider=self.name,
                model=self.model,
                error="quota_exceeded",
            )
        if response.status_code >= 400:
            return LLMResult(
                content="Erreur du fournisseur LLM.",
                provider=self.name,
                model=self.model,
                error=f"http_{response.status_code}",
            )
        try:
            data = response.json()
            content = data["choices"][0]["message"]["content"]
        except (ValueError, KeyError, IndexError, TypeError):
            return LLMResult(content="Réponse invalide du fournisseur LLM.", provider=self.name, model=self.model, error="invalid_response")
        if not isinstance(content, str) or not content.strip():
            return LLMResult(content="Le fournisseur LLM a renvoyé une réponse vide.", provider=self.name, model=self.model, error="empty_response")
        return LLMResult(
            content=content,
            provider=self.name,
            model=self.model,
            usage=data.get("usage") or {},
        )


class OllamaProvider:
    name = "ollama"
    demo = False

    def __init__(self, settings: Settings) -> None:
        self.model = settings.ollama_model or settings.llm_model
        self.base_url = settings.ollama_base_url.rstrip("/")
        self.configured = True

    def generate(self, *, system_prompt: str, user_prompt: str, temperature: float) -> LLMResult:
        try:
            quiz_match = re.search(r"Génère exactement (\d+) questions", user_prompt, re.IGNORECASE)
            if quiz_match:
                # Bound quiz output by its requested size; questions are prompted
                # to use short choices and explanations for local-model latency.
                num_predict = min(1200, max(500, int(quiz_match.group(1)) * 164))
            elif "Consigne supplémentaire" in user_prompt:
                normalized_prompt = user_prompt.casefold()
                if "synthèse concise" in normalized_prompt or "résumé court" in normalized_prompt:
                    num_predict = 256
                elif "fiche de révision" in normalized_prompt or "chapitre" in normalized_prompt:
                    num_predict = 768
                else:
                    num_predict = 512
            else:
                # Chat answers should stay short; CPU-only local models can take
                # several minutes when Ollama uses its default token budget.
                num_predict = 128
            payload = {
                "model": self.model,
                "stream": False,
                "options": {"temperature": temperature, "num_predict": num_predict},
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
            }
            if quiz_match:
                # Constrain the output shape so small local models do not spend
                # time producing JSON the quiz parser cannot consume.
                chunk_ids = re.findall(r"chunk_id=([^\s]+)", user_prompt)
                if chunk_ids:
                    quiz_schema = {
                        "type": "object",
                        "properties": {
                            "questions": {
                                "type": "array",
                                "minItems": int(quiz_match.group(1)),
                                "maxItems": int(quiz_match.group(1)),
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "question": {"type": "string"},
                                        "choices": {
                                            "type": "array",
                                            "minItems": 4,
                                            "maxItems": 4,
                                            "items": {"type": "string"},
                                        },
                                        "correct_choice_index": {"type": "integer", "enum": [0, 1, 2, 3]},
                                        "explanation": {"type": "string"},
                                        "chunk_id": {"type": "string", "enum": chunk_ids},
                                    },
                                    "required": [
                                        "question", "choices", "correct_choice_index", "explanation", "chunk_id"
                                    ],
                                    "additionalProperties": False,
                                },
                            }
                        },
                        "required": ["questions"],
                        "additionalProperties": False,
                    }
                    payload["format"] = quiz_schema
                else:
                    payload["format"] = "json"
            response = httpx.post(
                f"{self.base_url}/api/chat",
                json=payload,
                timeout=210.0 if quiz_match else 360.0,
            )
            if response.status_code == 404:
                return LLMResult(content=f"Le modèle Ollama « {self.model} » est absent. Installez-le avec `ollama pull {self.model}` puis réessayez.", provider=self.name, model=self.model, error="model_not_found")
            if response.status_code >= 400:
                return LLMResult(content=f"Ollama a renvoyé une erreur HTTP {response.status_code}.", provider=self.name, model=self.model, error=f"http_{response.status_code}")
            try:
                data = response.json()
            except ValueError:
                return LLMResult(content="Ollama a renvoyé une réponse JSON invalide.", provider=self.name, model=self.model, error="invalid_response")
            content = data.get("message", {}).get("content", "")
            if not isinstance(content, str) or not content.strip():
                return LLMResult(content="Ollama a renvoyé une réponse vide.", provider=self.name, model=self.model, error="empty_response")
            return LLMResult(content=content, provider=self.name, model=self.model)
        except httpx.TimeoutException:
            return LLMResult(content="Le délai de réponse d’Ollama a expiré. Essayez un modèle plus léger ou augmentez les ressources disponibles.", provider=self.name, model=self.model, error="timeout")
        except httpx.HTTPError as exc:
            return LLMResult(
                content="Ollama est injoignable. Démarrez le service et vérifiez OLLAMA_BASE_URL.",
                provider=self.name,
                model=self.model,
                error=type(exc).__name__,
            )
