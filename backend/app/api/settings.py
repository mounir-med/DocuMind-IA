from fastapi import APIRouter, Depends
import httpx
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.schemas.settings import PublicSettings, SettingsUpdate
from app.services.runtime_settings import public_settings, update_settings

router = APIRouter(tags=["settings"])


@router.get("/api/settings", response_model=PublicSettings)
def get_settings_route(db: Session = Depends(get_db)) -> PublicSettings:
    return public_settings(db)


@router.put("/api/settings", response_model=PublicSettings)
def put_settings(payload: SettingsUpdate, db: Session = Depends(get_db)) -> PublicSettings:
    return update_settings(db, payload)


@router.post("/api/settings/diagnose")
def diagnose_llm(db: Session = Depends(get_db)) -> dict:
    from app.core.config import get_settings
    from app.llm.factory import get_llm_provider
    from app.services.runtime_settings import apply_overrides

    apply_overrides(db)
    settings = get_settings()
    provider = get_llm_provider()
    if provider.name == "demo":
        return {"ok": False, "provider": "demo", "code": "not_configured", "message": "Aucun fournisseur IA n’est activé. Choisissez Ollama ou OpenAI dans les paramètres."}
    if provider.name == "openai" and not provider.configured:
        return {"ok": False, "provider": "openai", "code": "missing_api_key", "message": "Clé API absente. Configurez OPENAI_API_KEY côté serveur."}
    if provider.name == "ollama":
        try:
            response = httpx.get(f"{settings.ollama_base_url.rstrip('/')}/api/tags", timeout=5)
        except httpx.TimeoutException:
            return {"ok": False, "provider": "ollama", "code": "timeout", "message": "Ollama ne répond pas dans le délai imparti. Vérifiez que son service est démarré."}
        except httpx.HTTPError:
            return {"ok": False, "provider": "ollama", "code": "unreachable", "message": "Ollama est inaccessible. Démarrez Ollama et vérifiez OLLAMA_BASE_URL."}
        if response.status_code >= 400:
            return {"ok": False, "provider": "ollama", "code": f"http_{response.status_code}", "message": f"Ollama a renvoyé une erreur HTTP {response.status_code}."}
        try:
            models = response.json().get("models", [])
        except (ValueError, AttributeError):
            return {"ok": False, "provider": "ollama", "code": "invalid_response", "message": "La réponse d’Ollama est invalide."}
        names = {str(item.get("name", "")) for item in models if isinstance(item, dict)}
        if provider.model not in names and f"{provider.model}:latest" not in names:
            return {"ok": False, "provider": "ollama", "code": "model_not_found", "message": f"Le modèle « {provider.model} » est absent. Installez-le avec `ollama pull {provider.model}`."}
        return {"ok": True, "provider": "ollama", "model": provider.model, "message": "Ollama est accessible et le modèle est installé."}
    return {"ok": True, "provider": provider.name, "model": provider.model, "message": "Le fournisseur est configuré. Le diagnostic de connexion OpenAI sera vérifié lors d’une génération."}
