# 📌 Aide-Mémoire DocuMind AI

## 🚀 Commandes Rapides

### Démarrage
```powershell
# Terminal 1
.\start-backend.ps1

# Terminal 2
.\start-frontend.ps1
```

### Tests
```powershell
# Backend (10 tests)
cd backend
.\.venv\Scripts\python.exe -m pytest -v

# Frontend TypeScript
cd frontend
npm run typecheck
```

### Vérification Installation
```powershell
.\verify.ps1
```

---

## 🌐 URLs Importantes

| Service | URL |
|---------|-----|
| 🖥️ **Application** | http://localhost:3000 |
| 🔧 **API Backend** | http://127.0.0.1:8000 |
| 📖 **API Docs (Swagger)** | http://127.0.0.1:8000/docs |
| 📖 **API Docs (ReDoc)** | http://127.0.0.1:8000/redoc |

---

## 📁 Fichiers Clés à Connaître

### Configuration
```
backend/.env              → Config backend (LLM, embeddings, RAG)
frontend/.env.local       → Config frontend (optionnel)
```

### Points d'Entrée
```
backend/app/main.py       → Backend FastAPI
frontend/app/page.tsx     → Dashboard
frontend/app/layout.tsx   → Layout global
```

### Services Principaux
```
backend/app/services/chat_service.py       → Logique chat
backend/app/services/document_service.py   → Logique documents
backend/app/rag/pipeline.py                → Pipeline RAG
```

---

## 🎯 Endpoints API Principaux

### Documents
```
POST   /api/documents/upload           → Upload PDF
GET    /api/documents                  → Liste documents
GET    /api/documents/{id}             → Détail document
DELETE /api/documents/{id}             → Supprimer
POST   /api/documents/{id}/index       → Réindexer
```

### Chat
```
POST   /api/chat/{id}/messages         → Poser question
GET    /api/conversations              → Liste conversations
POST   /api/conversations              → Créer conversation
DELETE /api/conversations/{id}         → Supprimer
```

### Génération
```
POST   /api/documents/{id}/summarize   → Résumé
POST   /api/documents/{id}/quiz        → QCM
POST   /api/documents/compare          → Comparaison
```

### Autres
```
GET    /api/health                     → Health check
GET    /api/dashboard/stats            → Statistiques
GET    /api/settings                   → Config actuelle
PUT    /api/settings                   → Modifier config
```

---

## ⚙️ Configuration `.env`

### Variables Essentielles
```env
# LLM
LLM_PROVIDER=demo                    # demo | openai | ollama
LLM_MODEL=gpt-4o-mini
OPENAI_API_KEY=                      # Si provider=openai

# Embeddings
EMBEDDING_PROVIDER=sentence-transformers
EMBEDDING_MODEL=paraphrase-multilingual-MiniLM-L12-v2

# RAG
RAG_TOP_K=6                          # Nombre de passages
RAG_SCORE_THRESHOLD=0.25             # Seuil similarité

# Chunking
CHUNK_SIZE=520                       # Taille passage
CHUNK_OVERLAP=90                     # Chevauchement
```

---

## 🔧 Changements Courants

### Activer OpenAI
```env
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-votre-cle-ici
LLM_MODEL=gpt-4o-mini
```

### Activer Ollama
```env
LLM_PROVIDER=ollama
OLLAMA_MODEL=llama3.1
OLLAMA_BASE_URL=http://127.0.0.1:11434
```

### Ajuster RAG
```env
RAG_TOP_K=10              # Plus de contexte
RAG_SCORE_THRESHOLD=0.15  # Moins strict
```

### Augmenter Taille Upload
```env
MAX_UPLOAD_MB=50
```

---

## 🧪 Tests Rapides

### Vérifier Backend
```powershell
curl http://127.0.0.1:8000/api/health
```

### Vérifier Frontend
```
Ouvrir http://localhost:3000
```

### Tester Upload
```
Déposer un PDF sur le dashboard
```

---

## 🐛 Résolution Problèmes Courants

### Backend ne démarre pas
```powershell
cd backend
Remove-Item -Recurse -Force .venv
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### Frontend ne démarre pas
```powershell
cd frontend
Remove-Item -Recurse -Force node_modules
npm install
```

### "Backend injoignable"
1. Vérifier backend lancé (terminal 1)
2. Tester : http://127.0.0.1:8000/api/health
3. Vérifier CORS_ORIGINS dans `.env`

### Embeddings lents
Premier démarrage : téléchargement modèle (~120 Mo)
Ensuite : rapide (modèle en cache)

---

## 📊 Statuts Documents

| Statut | Signification |
|--------|---------------|
| **ready** | ✅ Indexé, prêt pour recherche |
| **indexing** | ⏳ Indexation en cours |
| **pending** | ⏸️ En attente de traitement |
| **error** | ❌ Erreur lors du traitement |
| **scanned** | 📸 PDF scanné (OCR désactivé) |
| **empty** | 🔍 Pas assez de texte extractible |

---

## 📚 Documentation

| Document | Contenu |
|----------|---------|
| `DEMARRAGE-RAPIDE.md` | Guide utilisateur |
| `STATUS.md` | État technique complet |
| `REPRISE-COMPLETE.md` | Documentation reprise |
| `README.md` | Documentation générale |
| `docs/architecture.md` | Architecture détaillée |
| `docs/rag-pipeline.md` | Pipeline RAG |
| `docs/api.md` | Documentation API |

---

## 🎨 Raccourcis Clavier

| Action | Raccourci |
|--------|-----------|
| Menu mobile | Hamburger icon |
| Thème clair/sombre | Icône soleil/lune |
| Nouvelle conversation | Bouton "+" dans chat |
| Upload | Drag & drop ou clic zone |

---

## 📈 Métriques de Performance

| Opération | Temps Moyen |
|-----------|-------------|
| Upload PDF (10 pages) | 2-5s |
| Indexation | 3-8s |
| Recherche vectorielle | <500ms |
| Génération réponse (OpenAI) | 2-5s |
| Génération réponse (Ollama) | 5-15s |

---

## ✅ Tests - 10/10 Passent

```
✓ test_health
✓ test_extract_valid_pdf
✓ test_extract_invalid_pdf
✓ test_extract_empty_pdf
✓ test_chunking_keeps_page_numbers
✓ test_conversation_lifecycle
✓ test_missing_routes
✓ test_upload_index_search_filter_delete
✓ test_invalid_and_empty_upload
✓ test_summarize_quiz_compare
```

---

## 🎯 Navigation UI

```
Dashboard (/)
├── Documents (/documents)
│   └── Détail Document (/documents/[id])
├── Chat (/chat)
│   └── Conversation (/chat/[id])
├── Résumés (/summaries)
├── QCM (/quizzes)
├── Comparaison (/compare)
└── Paramètres (/settings)
```

---

## 🔒 Sécurité

✅ Rate limiting (upload/chat)
✅ Validation PDF stricte
✅ Déduplication SHA-256
✅ Sanitization filenames
✅ Validation Pydantic
✅ CORS configuré
✅ Protection injection prompts

---

## 💡 Tips

### Meilleurs Résultats RAG
- Questions précises et ciblées
- Sélection documents pertinents
- Ajuster TOP_K selon besoin contexte
- Diminuer SCORE_THRESHOLD si peu de résultats

### Performance
- Utiliser SQLite en dev, PostgreSQL en prod
- ChromaDB persiste automatiquement
- Embeddings mis en cache

### Développement
- Backend : Hot reload activé (uvicorn --reload)
- Frontend : Hot reload Next.js automatique
- Tests : Lancer après chaque modification

---

**Dernière mise à jour** : 24 octobre 2026  
**Statut** : ✅ Opérationnel
