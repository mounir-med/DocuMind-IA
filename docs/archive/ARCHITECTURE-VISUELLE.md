# 🏗️ Architecture Visuelle - DocuMind AI

## 📊 Vue d'Ensemble du Système

```
┌─────────────────────────────────────────────────────────────────────┐
│                        UTILISATEUR                                  │
│                     (Navigateur Web)                                │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             │ HTTP/REST
                             │
┌────────────────────────────▼────────────────────────────────────────┐
│                     FRONTEND (Next.js)                              │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  Pages : Dashboard, Documents, Chat, Résumés, QCM, Etc.     │  │
│  └──────────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  Composants UI : Cards, Buttons, Modals, Forms              │  │
│  └──────────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  API Client : Fetch typé vers backend                        │  │
│  └──────────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             │ API REST
                             │
┌────────────────────────────▼────────────────────────────────────────┐
│                     BACKEND (FastAPI)                               │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  API Routes : /documents, /chat, /conversations, etc.        │  │
│  └────────────┬─────────────────────────────────────────────────┘  │
│               │                                                      │
│  ┌────────────▼─────────────────────────────────────────────────┐  │
│  │  Services : Logique métier (chat, documents, generation)     │  │
│  └────┬───────────────┬───────────────┬───────────────┬─────────┘  │
│       │               │               │               │              │
│  ┌────▼────────┐ ┌────▼────────┐ ┌───▼──────┐ ┌─────▼──────────┐  │
│  │ RAG         │ │ Document    │ │ LLM      │ │ Embeddings     │  │
│  │ Pipeline    │ │ Processing  │ │ Provider │ │ Provider       │  │
│  └────┬────────┘ └────┬────────┘ └───┬──────┘ └─────┬──────────┘  │
└───────┼──────────────┼────────────────┼──────────────┼─────────────┘
        │              │                │              │
        │              │                │              │
┌───────▼──────┐ ┌─────▼─────┐  ┌──────▼──────┐ ┌────▼─────┐
│ ChromaDB     │ │ SQLite    │  │ OpenAI /    │ │ Sentence │
│ (Vecteurs)   │ │ (Metadata)│  │ Ollama      │ │Transform │
└──────────────┘ └───────────┘  └─────────────┘ └──────────┘
```

---

## 🔄 Flux de Données : Upload PDF

```
┌───────┐
│ User  │ Sélectionne PDF
└───┬───┘
    │
    │ 1. Upload File
    ▼
┌──────────────────┐
│ Frontend         │
│ - Validation     │ (Taille, type)
│ - FormData       │
└────────┬─────────┘
         │
         │ 2. POST /api/documents/upload
         ▼
    ┌─────────────────┐
    │ Backend API     │
    │ - Rate limit    │
    │ - Validation    │ (PDF header)
    └────────┬────────┘
             │
             │ 3. document_service.upload()
             ▼
        ┌──────────────────┐
        │ DocumentService  │
        │ - SHA-256 check  │ (Déduplication)
        │ - Save to disk   │ (data/uploads/)
        │ - Create DB row  │
        └────────┬─────────┘
                 │
                 │ 4. index_document()
                 ▼
            ┌────────────────────┐
            │ PDF Processing     │
            │ - PyMuPDF extract  │ → Text pages
            │ - Detect scanned   │
            └────────┬───────────┘
                     │
                     │ 5. chunking.chunk_pages()
                     ▼
                ┌──────────────────┐
                │ Text Chunking    │
                │ - Split by size  │ (520 chars)
                │ - Overlap        │ (90 chars)
                │ - Keep page #    │
                └────────┬─────────┘
                         │
                         │ 6. embeddings.embed()
                         ▼
                    ┌─────────────────────┐
                    │ Embedding Provider  │
                    │ - sentence-trans.   │ → Vectors
                    └────────┬────────────┘
                             │
                             │ 7. vector_store.upsert()
                             ▼
                        ┌──────────────┐
                        │ ChromaDB     │
                        │ - Index      │
                        │ - Persist    │
                        └──────────────┘
```

---

## 💬 Flux de Données : Question RAG

```
┌───────┐
│ User  │ Pose question : "Quel est le contenu du document ?"
└───┬───┘
    │
    │ 1. Send message
    ▼
┌──────────────────┐
│ Frontend         │
│ - Select docs    │
│ - Type question  │
└────────┬─────────┘
         │
         │ 2. POST /api/chat/{id}/messages
         ▼
    ┌─────────────────┐
    │ Backend API     │
    │ - Rate limit    │
    │ - Validation    │
    └────────┬────────┘
             │
             │ 3. chat_service.add_message()
             ▼
        ┌──────────────────┐
        │ ChatService      │
        │ - Save question  │ → SQLite
        │ - Call RAG       │
        └────────┬─────────┘
                 │
                 │ 4. rag.answer_question()
                 ▼
            ┌────────────────────────┐
            │ RAG Pipeline           │
            └────────┬───────────────┘
                     │
                     │ 5. RETRIEVE
                     ▼
                ┌──────────────────────┐
                │ retriever.retrieve() │
                │ - Embed question     │ (sentence-transformers)
                │ - Search ChromaDB    │ (cosine similarity)
                │ - Filter by score    │ (threshold 0.25)
                │ - Top-K results      │ (6 passages)
                └────────┬─────────────┘
                         │
                         │ Sources: [{text, page, doc}, ...]
                         │
                         │ 6. AUGMENT
                         ▼
                    ┌─────────────────────┐
                    │ prompts.build()     │
                    │ - System prompt     │
                    │ - Context passages  │
                    │ - User question     │
                    └────────┬────────────┘
                             │
                             │ Prompt: "Tu es un assistant..."
                             │
                             │ 7. GENERATE
                             ▼
                        ┌──────────────────┐
                        │ LLM Provider     │
                        │ - OpenAI         │ ─┐
                        │ - Ollama         │  │ → Response
                        │ - Demo (mock)    │ ─┘
                        └────────┬─────────┘
                                 │
                                 │ Answer text
                                 │
                                 │ 8. Save & Return
                                 ▼
                            ┌──────────────┐
                            │ ChatService  │
                            │ - Save reply │ → SQLite
                            │ - Return     │
                            └──────┬───────┘
                                   │
                                   │ JSON response
                                   ▼
                              ┌──────────┐
                              │ Frontend │
                              │ Display  │
                              └──────────┘
```

---

## 🗄️ Schéma Base de Données

```
┌──────────────────────────────────────┐
│          documents                   │
├──────────────────────────────────────┤
│ id (PK)          VARCHAR             │
│ filename         VARCHAR             │
│ stored_name      VARCHAR             │
│ sha256           VARCHAR (UNIQUE)    │
│ size_bytes       INTEGER             │
│ page_count       INTEGER             │
│ chunk_count      INTEGER             │
│ status           VARCHAR             │ (ready/indexing/error/etc.)
│ error_message    TEXT                │
│ indexed_at       TIMESTAMP           │
│ created_at       TIMESTAMP           │
└──────────────────────────────────────┘

┌──────────────────────────────────────┐
│        conversations                 │
├──────────────────────────────────────┤
│ id (PK)          VARCHAR             │
│ title            VARCHAR             │
│ created_at       TIMESTAMP           │
│ updated_at       TIMESTAMP           │
└──────────────────────────────────────┘
                    │
                    │ 1:N
                    ▼
┌──────────────────────────────────────┐
│          messages                    │
├──────────────────────────────────────┤
│ id (PK)          VARCHAR             │
│ conversation_id  VARCHAR (FK)        │
│ role             VARCHAR             │ (user/assistant)
│ content          TEXT                │
│ sources_json     TEXT                │
│ meta_json        TEXT                │
│ created_at       TIMESTAMP           │
└──────────────────────────────────────┘

┌──────────────────────────────────────┐
│        runtime_settings              │
├──────────────────────────────────────┤
│ id (PK)          INTEGER             │
│ key              VARCHAR (UNIQUE)    │
│ value            VARCHAR             │
│ updated_at       TIMESTAMP           │
└──────────────────────────────────────┘
```

---

## 🔍 Schéma ChromaDB (Vector Store)

```
Collection: "documind"

Document (Chunk):
{
  "id": "doc-uuid_chunk-0",
  "embedding": [0.123, -0.456, ...],  # 384 dimensions
  "metadata": {
    "document_id": "doc-uuid",
    "document_name": "rapport.pdf",
    "page_number": 1,
    "chunk_index": 0
  },
  "document": "Texte du passage extrait..."
}

Index:
- HNSW (Hierarchical Navigable Small World)
- Métrique: cosine similarity
- Persistance: data/chroma/
```

---

## 📦 Dépendances Principales

### Backend

```
FastAPI ───┬──► Pydantic (validation)
           └──► Starlette (ASGI)

SQLAlchemy ───► SQLite

PyMuPDF (fitz) ──► PDF extraction

ChromaDB ───┬──► ONNX Runtime
            ├──► NumPy
            └──► Persistance locale

sentence-transformers ───┬──► PyTorch
                         └──► Transformers (HuggingFace)

OpenAI SDK ──► OpenAI API (optionnel)

httpx ──► Ollama API (optionnel)
```

### Frontend

```
Next.js 15 ───┬──► React 19
              ├──► React DOM
              └──► Server Components

TypeScript ──► Compilation type-safe

Tailwind CSS ──► Styles utility-first

Lucide React ──► Icônes

React Markdown ───┬──► remark-gfm
                  └──► Syntax highlighting

Sonner ──► Notifications toast

Framer Motion ──► Animations
```

---

## 🔐 Flux Sécurité

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │
       │ 1. HTTP Request
       ▼
┌──────────────────┐
│ CORS Middleware  │ ✓ Origin check
└──────┬───────────┘
       │
       │ 2. Rate Limiter
       ▼
┌──────────────────┐
│ Rate Limit       │ ✓ 60 req/min
└──────┬───────────┘
       │
       │ 3. Route Handler
       ▼
┌──────────────────┐
│ Pydantic Schema  │ ✓ Validation stricte
└──────┬───────────┘
       │
       │ 4. Service Layer
       ▼
┌──────────────────┐
│ Business Logic   │ ✓ SHA-256 check
│                  │ ✓ Filename sanitize
│                  │ ✓ Size limits
└──────┬───────────┘
       │
       │ 5. Data Access
       ▼
┌──────────────────┐
│ Database/Store   │ ✓ SQLite / ChromaDB
└──────────────────┘
```

---

## 🎨 Structure UI Composants

```
AppShell (layout.tsx)
├── Navigation Sidebar
│   ├── Brand
│   ├── Nav Links
│   └── Theme Toggle
│
└── Main Content
    ├── Header (optional)
    │   ├── Title
    │   ├── Subtitle
    │   └── Actions
    │
    └── Page Content
        ├── Dashboard
        │   ├── StatCards
        │   ├── Dropzone
        │   ├── Recent Docs
        │   └── Recent Conversations
        │
        ├── Documents
        │   ├── Filters
        │   ├── Document Cards
        │   └── Actions (upload, delete)
        │
        ├── Chat
        │   ├── Conversation Sidebar
        │   ├── Document Selector
        │   ├── Message List
        │   │   ├── User Message
        │   │   └── Assistant Message
        │   │       ├── Markdown Content
        │   │       └── Sources
        │   └── Input Form
        │
        └── Other Pages...
```

---

## 🔄 États Composant Chat

```
Chat Page State Machine:

┌─────────────┐
│   Initial   │
└──────┬──────┘
       │ Load conversation
       ▼
┌─────────────┐
│   Loading   │
└──────┬──────┘
       │ Success
       ▼
┌─────────────┐
│   Loaded    │ ◄──┐
└──────┬──────┘    │
       │           │
       │ Send msg  │
       ▼           │
┌─────────────┐    │
│  Sending    │    │ Success
└──────┬──────┘    │
       │           │
       ├───────────┘
       │
       │ Error
       ▼
┌─────────────┐
│   Error     │
└─────────────┘
```

---

## 📁 Système de Fichiers

```
documind-ai/
│
├── data/                    # Données runtime (gitignored)
│   ├── uploads/                → PDF stockés
│   ├── chroma/                 → Index vectoriel
│   └── app.db                  → Base SQLite
│
├── backend/
│   ├── app/                    → Code source
│   ├── tests/                  → Tests pytest
│   ├── .venv/                  → Environnement Python
│   ├── .env                    → Configuration (secret)
│   └── requirements.txt
│
├── frontend/
│   ├── app/                    → Pages Next.js
│   ├── components/             → Composants React
│   ├── lib/                    → Utilitaires
│   ├── node_modules/           → Dépendances npm
│   ├── .env.local              → Config frontend (optionnel)
│   └── package.json
│
├── docs/                    # Documentation
├── scripts/                 # Scripts utilitaires
│
└── Configuration files
    ├── .gitignore
    ├── README.md
    ├── DEMARRAGE-RAPIDE.md
    ├── STATUS.md
    └── etc.
```

---

## 🚀 Flux Déploiement

```
┌──────────────┐
│ Development  │
│   localhost  │
└──────┬───────┘
       │
       │ 1. Tests pass
       │ 2. Build
       ▼
┌──────────────┐
│   Staging    │
│   (optional) │
└──────┬───────┘
       │
       │ 3. Validation
       ▼
┌──────────────────────────────┐
│        Production            │
├──────────────────────────────┤
│ Backend:                     │
│ - Docker container           │
│ - PostgreSQL                 │
│ - Redis (cache)              │
│ - Nginx (reverse proxy)      │
│                              │
│ Frontend:                    │
│ - Vercel / Next.js hosting   │
│ - CDN                        │
│                              │
│ Monitoring:                  │
│ - Logs                       │
│ - Metrics                    │
│ - Alerts                     │
└──────────────────────────────┘
```

---

## 📊 Performance Metrics

```
Upload & Indexation:
┌─────────────┐
│ Upload PDF  │  2-5s  (network + validation)
├─────────────┤
│ Extract     │  1-3s  (PyMuPDF)
├─────────────┤
│ Chunk       │  <1s   (text processing)
├─────────────┤
│ Embed       │  2-4s  (sentence-transformers)
├─────────────┤
│ Index       │  <1s   (ChromaDB)
└─────────────┘
Total: 5-15s (document 10 pages)

RAG Query:
┌─────────────┐
│ Embed Q     │  <1s   (sentence-transformers)
├─────────────┤
│ Search      │  <0.5s (ChromaDB)
├─────────────┤
│ LLM Gen     │  2-5s  (OpenAI) / 5-15s (Ollama)
└─────────────┘
Total: 3-20s selon provider
```

---

Cette architecture assure :
- ✅ **Séparation des préoccupations** (frontend/backend/storage)
- ✅ **Scalabilité** (ChromaDB indexe millions de vecteurs)
- ✅ **Maintenabilité** (code modulaire, tests, types)
- ✅ **Performance** (cache, batch, async)
- ✅ **Sécurité** (validation, rate limit, sanitization)
