import time
from app.core.exceptions import DependencyError


class SentenceTransformerProvider:
    def __init__(self, model_name: str, max_retries: int = 3) -> None:
        self.model_name = model_name
        self.dimension = 384
        self.ready = False
        self._model = None
        self._error = None
        self._max_retries = max_retries
        
        # Try to initialize with retries
        for attempt in range(max_retries):
            try:
                from sentence_transformers import SentenceTransformer

                self._model = SentenceTransformer(model_name)
                self.dimension = int(self._model.get_sentence_embedding_dimension())
                self.ready = True
                print(f"Embeddings model '{model_name}' loaded successfully (attempt {attempt + 1}/{max_retries})")
                break
            except Exception as exc:  # noqa: BLE001
                self._error = str(exc)
                print(f"Failed to load embeddings model (attempt {attempt + 1}/{max_retries}): {exc}")
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt  # Exponential backoff: 1s, 2s, 4s
                    print(f"Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    print(f"Failed to load embeddings model after {max_retries} attempts")

    def embed(self, texts: list[str]) -> list[list[float]]:
        if not self.ready or self._model is None:
            error_msg = f"Le modèle d'embeddings est indisponible. Vérifiez l'installation de sentence-transformers."
            if self._error:
                error_msg += f" Erreur: {self._error}"
            raise DependencyError(
                error_msg,
                code="embeddings_unavailable",
            )
        vectors = self._model.encode(texts, normalize_embeddings=True)
        return [vector.tolist() for vector in vectors]
