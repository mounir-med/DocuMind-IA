# 👨‍💻 Guide Développeur - DocuMind AI

## 🎯 Vue d'Ensemble

Ce guide vous aide à comprendre, modifier et étendre DocuMind AI.

---

## 🏗️ Architecture Globale

### Pattern MVC Étendu

```
Frontend (React/Next.js)
    ↓ HTTP REST
Backend (FastAPI)
    ↓
├── API Layer (routes)
├── Service Layer (logique métier)
├── Repository Layer (accès données)
└── External Services
    ├── Vector Store (ChromaDB)
    ├── LLM Providers (OpenAI/Ollama)
    └── Database (SQLite)
```

### Flux de Données Principal

```
1. Upload PDF
   User → Frontend → API → DocumentService
   → PDF Extraction → Chunking → Embeddings → ChromaDB

2. Question RAG
   User → Frontend → API → ChatService
   → Retriever (ChromaDB) → LLM → Response
```

---

## 📂 Structure Backend Détaillée

### Couche API (`app/api/`)
**Rôle** : Routes FastAPI, validation entrées, réponses HTTP

```python
# Exemple : app/api/documents.py
@router.post("/api/documents/upload")
async def upload_document(file: UploadFile, db: Session):
    # 1. Validation
    # 2. Appel service
    # 3. Retour DTO
    return DocumentOut.model_validate(document)
```

### Couche Service (`app/services/`)
**Rôle** : Logique métier, orchestration

```python
# Exemple : app/services/document_service.py
def upload_document(db: Session, filename: str, payload: bytes):
    # 1. Validation SHA-256
    # 2. Sauvegarde fichier
    # 3. Création entité DB
    # 4. Indexation (extraction + embeddings)
    return document
```

### Couche Modèle (`app/models/`)
**Rôle** : Entités SQLAlchemy (ORM)

```python
# Exemple : app/models/entities.py
class Document(Base):
    __tablename__ = "documents"
    id = Column(String, primary_key=True)
    filename = Column(String, nullable=False)
    status = Column(String, default="pending")
    # ...
```

### Couche Schéma (`app/schemas/`)
**Rôle** : Validation Pydantic, DTOs

```python
# Exemple : app/schemas/documents.py
class DocumentOut(BaseModel):
    id: str
    filename: str
    status: str
    # ...
    model_config = ConfigDict(from_attributes=True)
```

### Pipeline RAG (`app/rag/`)

```python
# app/rag/pipeline.py
def answer_question(question: str, document_ids: list[str]):
    # 1. Retrieve: Recherche vectorielle
    sources = retrieve(question, document_ids)
    
    # 2. Augment: Construction prompt
    prompt = build_user_prompt(question, sources)
    
    # 3. Generate: Appel LLM
    result = llm.generate(SYSTEM_PROMPT, prompt)
    
    return {"content": result.content, "sources": sources}
```

---

## 📂 Structure Frontend Détaillée

### Pages (`app/`)
**Rôle** : Routes Next.js, composants page

```tsx
// app/documents/page.tsx
export default function DocumentsPage() {
  const [documents, setDocuments] = useState<DocumentItem[]>([]);
  
  useEffect(() => {
    api.documents().then(setDocuments);
  }, []);
  
  return <div>...</div>;
}
```

### Composants (`components/`)
**Rôle** : Composants réutilisables

```tsx
// components/ui/Button.tsx
interface ButtonProps {
  variant?: "primary" | "secondary" | "danger";
  children: ReactNode;
  onClick?: () => void;
}

export function Button({ variant = "primary", ...props }: ButtonProps) {
  return <button className={cn(styles[variant])} {...props} />;
}
```

### API Client (`lib/api.ts`)
**Rôle** : Wrapper HTTP typé

```typescript
// lib/api.ts
export const api = {
  documents: () => request<DocumentItem[]>("/api/documents"),
  upload: (file: File) => {
    const body = new FormData();
    body.append("file", file);
    return request<DocumentItem>("/api/documents/upload", { 
      method: "POST", 
      body 
    });
  },
  // ...
};
```

---

## 🔧 Ajouter une Nouvelle Fonctionnalité

### Exemple : Ajouter "Favoris"

#### 1. Backend - Modèle

```python
# app/models/entities.py
class Document(Base):
    # ... existant
    is_favorite = Column(Boolean, default=False)  # Nouveau
```

#### 2. Backend - Migration

```python
# Créer le champ en base
# Option 1 : Recréer la DB (dev uniquement)
import os
os.remove("data/app.db")

# Option 2 : Migration manuelle (prod)
# ALTER TABLE documents ADD COLUMN is_favorite BOOLEAN DEFAULT 0;
```

#### 3. Backend - Schéma

```python
# app/schemas/documents.py
class DocumentOut(BaseModel):
    # ... existant
    is_favorite: bool  # Nouveau
```

#### 4. Backend - Service

```python
# app/services/document_service.py
def toggle_favorite(db: Session, document_id: str) -> Document:
    document = get_document(db, document_id)
    document.is_favorite = not document.is_favorite
    db.commit()
    db.refresh(document)
    return document
```

#### 5. Backend - Route

```python
# app/api/documents.py
@router.post("/api/documents/{document_id}/favorite")
def toggle_favorite(document_id: str, db: Session = Depends(get_db)):
    document = document_service.toggle_favorite(db, document_id)
    return DocumentOut.model_validate(document)
```

#### 6. Frontend - Type

```typescript
// lib/types.ts
export interface DocumentItem {
  // ... existant
  is_favorite: boolean;  // Nouveau
}
```

#### 7. Frontend - API

```typescript
// lib/api.ts
export const api = {
  // ... existant
  toggleFavorite: (id: string) => 
    request<DocumentItem>(`/api/documents/${id}/favorite`, { 
      method: "POST" 
    }),
};
```

#### 8. Frontend - UI

```tsx
// app/documents/page.tsx
<Button onClick={() => api.toggleFavorite(doc.id).then(load)}>
  {doc.is_favorite ? "★" : "☆"} Favori
</Button>
```

---

## 🧪 Ajouter des Tests

### Test Backend

```python
# backend/tests/test_favorites.py
def test_toggle_favorite(client):
    # 1. Upload document
    with open("tests/_tmp_data/sample.pdf", "rb") as f:
        response = client.post(
            "/api/documents/upload",
            files={"file": ("test.pdf", f, "application/pdf")}
        )
    doc_id = response.json()["id"]
    
    # 2. Toggle favorite
    response = client.post(f"/api/documents/{doc_id}/favorite")
    assert response.status_code == 200
    assert response.json()["is_favorite"] is True
    
    # 3. Toggle again
    response = client.post(f"/api/documents/{doc_id}/favorite")
    assert response.json()["is_favorite"] is False
```

### Lancer les Tests

```powershell
cd backend
.\.venv\Scripts\python.exe -m pytest tests/test_favorites.py -v
```

---

## 🎨 Ajouter un Composant UI

### Exemple : Badge de Statut

```tsx
// components/ui/StatusBadge.tsx
interface StatusBadgeProps {
  status: "ready" | "indexing" | "error" | "scanned" | "empty";
}

const STYLES = {
  ready: "bg-green-100 text-green-800",
  indexing: "bg-blue-100 text-blue-800",
  error: "bg-red-100 text-red-800",
  scanned: "bg-yellow-100 text-yellow-800",
  empty: "bg-gray-100 text-gray-800",
};

const LABELS = {
  ready: "✓ Prêt",
  indexing: "⏳ Indexation",
  error: "✗ Erreur",
  scanned: "📸 Scanné",
  empty: "⚠ Vide",
};

export function StatusBadge({ status }: StatusBadgeProps) {
  return (
    <span className={cn("rounded-full px-2 py-1 text-xs", STYLES[status])}>
      {LABELS[status]}
    </span>
  );
}
```

### Utilisation

```tsx
// app/documents/page.tsx
import { StatusBadge } from "@/components/ui/StatusBadge";

<StatusBadge status={doc.status} />
```

---

## 🔌 Ajouter un Provider LLM

### 1. Implémenter l'Interface

```python
# app/llm/providers.py
class AnthropicProvider(LLMProvider):
    def __init__(self):
        self.name = "anthropic"
        self.model = get_settings().anthropic_model
        self.configured = bool(get_settings().anthropic_api_key)
        self.demo = False
    
    def generate(self, system_prompt: str, user_prompt: str, temperature: float):
        import anthropic
        client = anthropic.Anthropic(api_key=get_settings().anthropic_api_key)
        
        response = client.messages.create(
            model=self.model,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
            temperature=temperature,
            max_tokens=2000
        )
        
        return LLMResponse(
            content=response.content[0].text,
            provider=self.name,
            model=self.model,
            usage={"input_tokens": response.usage.input_tokens}
        )
```

### 2. Ajouter à la Factory

```python
# app/llm/factory.py
def get_llm_provider() -> LLMProvider:
    provider = get_settings().llm_provider
    
    if provider == "openai":
        return OpenAIProvider()
    elif provider == "ollama":
        return OllamaProvider()
    elif provider == "anthropic":  # Nouveau
        return AnthropicProvider()
    else:
        return DemoProvider()
```

### 3. Ajouter Configuration

```python
# app/core/config.py
class Settings(BaseSettings):
    # ... existant
    anthropic_api_key: str = ""
    anthropic_model: str = "claude-3-sonnet-20240229"
```

### 4. Mettre à Jour `.env.example`

```env
# Anthropic (if using anthropic provider)
ANTHROPIC_API_KEY=your-anthropic-api-key-here
ANTHROPIC_MODEL=claude-3-sonnet-20240229
```

---

## 🗄️ Modifier le Schéma de Base de Données

### Option 1 : Reset (Développement)

```python
# Simple mais perte de données
import os
os.remove("data/app.db")
# Redémarrer le backend → tables recréées
```

### Option 2 : Migration Manuelle

```python
# Créer un script de migration
# scripts/migrate_add_favorites.py

from sqlalchemy import create_engine, text
from app.core.config import get_settings

settings = get_settings()
engine = create_engine(f"sqlite:///{settings.database_path}")

with engine.connect() as conn:
    conn.execute(text("""
        ALTER TABLE documents 
        ADD COLUMN is_favorite BOOLEAN DEFAULT 0
    """))
    conn.commit()

print("Migration terminée !")
```

```powershell
cd backend
.\.venv\Scripts\python.exe ../scripts/migrate_add_favorites.py
```

### Option 3 : Alembic (Production)

```powershell
# Installation
pip install alembic

# Initialisation
alembic init migrations

# Créer migration
alembic revision --autogenerate -m "add favorites"

# Appliquer
alembic upgrade head
```

---

## 🎨 Personnaliser le Thème

### Modifier les Couleurs

```css
/* frontend/app/globals.css */

:root {
  --accent: 220 90% 56%;        /* Bleu principal */
  --canvas: 0 0% 98%;           /* Fond clair */
  --surface: 0 0% 100%;         /* Surface clair */
  --ink: 220 13% 13%;           /* Texte sombre */
  --muted: 220 9% 46%;          /* Texte atténué */
  --line: 220 13% 91%;          /* Bordures */
}

.dark {
  --accent: 220 90% 56%;        /* Même bleu */
  --canvas: 220 13% 13%;        /* Fond sombre */
  --surface: 220 13% 18%;       /* Surface sombre */
  --ink: 220 13% 98%;           /* Texte clair */
  --muted: 220 9% 66%;          /* Texte atténué */
  --line: 220 13% 26%;          /* Bordures */
}
```

### Ajouter une Nouvelle Couleur

```css
:root {
  --success: 142 76% 36%;       /* Vert */
  --warning: 38 92% 50%;        /* Orange */
  --error: 0 72% 51%;           /* Rouge */
}
```

```tsx
// Utilisation
<div className="text-success">Succès !</div>
<div className="bg-warning text-white">Attention</div>
<div className="border-error">Erreur</div>
```

---

## 📊 Monitoring & Logs

### Ajouter des Logs Backend

```python
# app/services/document_service.py
import logging

logger = logging.getLogger(__name__)

def upload_document(db, filename, payload):
    logger.info(f"Upload started: {filename} ({len(payload)} bytes)")
    
    try:
        # ... traitement
        logger.info(f"Upload completed: {document.id}")
        return document
    except Exception as e:
        logger.error(f"Upload failed: {filename} - {e}")
        raise
```

### Configuration Logs

```python
# app/main.py
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler("logs/app.log"),
        logging.StreamHandler()
    ]
)
```

---

## 🔒 Sécurité - Best Practices

### 1. Validation Stricte

```python
# Toujours valider avec Pydantic
class ChatMessageRequest(BaseModel):
    content: str = Field(min_length=1, max_length=10000)
    document_ids: list[str] = Field(default_factory=list)
    
    @field_validator("document_ids")
    def validate_document_ids(cls, v):
        if len(v) > 50:
            raise ValueError("Maximum 50 documents")
        return v
```

### 2. Rate Limiting

```python
# app/core/rate_limit.py
from slowapi import Limiter

limiter = Limiter(key_func=client_key)

@router.post("/api/documents/upload")
@limiter.limit("10/minute")  # Max 10 uploads/minute
async def upload_document(...):
    pass
```

### 3. Sanitization

```python
# app/core/security.py
import re

def sanitize_filename(filename: str) -> str:
    # Supprimer caractères dangereux
    safe = re.sub(r'[^\w\s.-]', '', filename)
    # Limiter longueur
    return safe[:255]
```

### 4. Protection Injection Prompts

```python
# app/rag/prompts.py
def build_user_prompt(question: str, sources: list):
    # Échapper les instructions potentielles
    safe_question = question.replace("Ignore", "").strip()
    
    return f"""
    Question utilisateur : {safe_question}
    
    Contexte des documents :
    {format_sources(sources)}
    """
```

---

## 🚀 Performance

### 1. Cache Embeddings

```python
# app/embeddings/sentence_transformer.py
from functools import lru_cache

class SentenceTransformerProvider:
    @lru_cache(maxsize=1000)
    def embed_cached(self, text: str) -> list[float]:
        return self.model.encode(text).tolist()
```

### 2. Batch Processing

```python
# Traiter plusieurs documents en parallèle
from concurrent.futures import ThreadPoolExecutor

def batch_index(documents: list[Document]):
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [
            executor.submit(index_document, doc.id) 
            for doc in documents
        ]
        results = [f.result() for f in futures]
    return results
```

### 3. Pagination

```python
# app/api/documents.py
@router.get("/api/documents")
def list_documents(
    skip: int = 0, 
    limit: int = 50,
    db: Session = Depends(get_db)
):
    documents = db.query(Document)\
        .offset(skip)\
        .limit(limit)\
        .all()
    return [DocumentOut.model_validate(d) for d in documents]
```

---

## 📖 Documentation API

### Swagger UI
- URL : http://127.0.0.1:8000/docs
- Permet de tester les endpoints interactivement

### ReDoc
- URL : http://127.0.0.1:8000/redoc
- Documentation lisible et exportable

### Améliorer Documentation

```python
# app/api/documents.py
@router.post(
    "/api/documents/upload",
    response_model=DocumentOut,
    summary="Upload et indexe un PDF",
    description="""
    Upload un fichier PDF, extrait le texte, génère les embeddings
    et indexe dans ChromaDB pour recherche sémantique.
    
    - **file**: Fichier PDF (max 25 Mo)
    - **return**: Objet document avec statut d'indexation
    """,
    responses={
        200: {"description": "Document uploadé et indexé"},
        400: {"description": "Fichier invalide ou trop volumineux"},
        429: {"description": "Rate limit dépassé"}
    }
)
async def upload_document(...):
    pass
```

---

## 🛠️ Outils de Développement

### Backend

```powershell
# Auto-formatage
pip install black isort
black app/
isort app/

# Linting
pip install pylint
pylint app/

# Type checking
pip install mypy
mypy app/

# Coverage
pytest --cov=app --cov-report=html
```

### Frontend

```powershell
# Linting
npm run lint

# Type checking
npm run typecheck

# Formatage
npm install --save-dev prettier
npx prettier --write "**/*.{ts,tsx,json}"
```

---

## 📚 Ressources

### Documentation Externe
- [FastAPI](https://fastapi.tiangolo.com/)
- [Next.js](https://nextjs.org/docs)
- [ChromaDB](https://docs.trychroma.com/)
- [Pydantic](https://docs.pydantic.dev/)
- [Tailwind CSS](https://tailwindcss.com/docs)

### Communauté
- GitHub Issues pour bugs
- Stack Overflow pour questions
- Discord communauté (si disponible)

---

## ✅ Checklist Avant Commit

- [ ] Tests passent (`pytest -v`)
- [ ] TypeScript compile (`npm run typecheck`)
- [ ] Linting OK (`npm run lint`, `pylint`)
- [ ] Documentation mise à jour
- [ ] Variables sensibles dans `.env` (pas dans le code)
- [ ] Pas de console.log / print() debug
- [ ] Commit message descriptif

---

## 🎯 Contribution

### Workflow Git

```bash
# Créer une branche
git checkout -b feature/ma-fonctionnalite

# Développer et tester
# ...

# Committer
git add .
git commit -m "feat: ajout fonctionnalité favoris"

# Pousser
git push origin feature/ma-fonctionnalite

# Créer Pull Request sur GitHub
```

### Convention Commits

```
feat: nouvelle fonctionnalité
fix: correction bug
docs: documentation
style: formatage code
refactor: refactoring
test: ajout tests
chore: maintenance
```

---

**Bon développement !** 🚀
