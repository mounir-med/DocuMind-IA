# DocuMind AI

Assistant IA professionnel de question-réponse sur documents PDF basé sur l'architecture RAG (Retrieval-Augmented Generation).

## 🎯 Fonctionnalités

- **Dashboard** : Statistiques d'utilisation et métriques en temps réel
- **Gestion des PDF** : Upload multi-fichiers, dédoublonnage SHA-256, prévisualisation
- **Chat RAG Intelligent** : Questions-réponses contextuelles avec sources traçables
- **Génération de Résumés** : Court, détaillé, ou par chapitre
- **QCM Interactifs** : Génération automatique de quiz avec validation
- **Comparaison de Documents** : Analyse comparative multi-PDF
- **Paramètres Avancés** : Configuration LLM, chunking, et retrieval

## 🛠️ Stack Technique

### Frontend
- Next.js 14+ (App Router, TypeScript)
- Tailwind CSS + shadcn/ui
- React Markdown, Framer Motion
- Mode sombre/clair

### Backend
- Python 3.11+
- FastAPI + Pydantic v2
- PyMuPDF (extraction PDF)
- ChromaDB (base vectorielle)
- sentence-transformers (embeddings multilingues)
- SQLite (métadonnées)

## 📋 Prérequis

- Node.js 18+
- Python 3.11+
- npm ou yarn
- pip

## 🚀 Installation & Lancement

### ⚡ Démarrage Rapide (2 Minutes)

**Terminal 1 - Backend:**
```powershell
.\start-backend.ps1
```

**Terminal 2 - Frontend:**
```powershell
.\start-frontend.ps1
```

Puis ouvrez **http://localhost:3000** 🎉


## 🤖 Configurer le LLM (indispensable)

Sans LLM, l'application est en **mode démonstration** : elle ne génère aucune réponse, aucun résumé ni QCM
(seules les sources retrouvées sont affichées).

1. Ouvrez `backend/.env` (copié depuis `backend/.env.example`).
2. Choisissez **un** fournisseur :
   - **Ollama** (local, gratuit) : `LLM_PROVIDER=ollama` et `OLLAMA_MODEL=llama3.1:latest`.
   - **OpenAI** : `LLM_PROVIDER=openai` et `OPENAI_API_KEY=sk-...`.
3. Pour Windows, ouvrez PowerShell et lancez `ollama serve` (ou démarrez l'application Ollama), puis
   `ollama pull llama3.1:latest`. Vérifiez le nom réellement installé avec `ollama list` et utilisez
   exactement ce nom dans `OLLAMA_MODEL` et `LLM_MODEL`.
4. Redémarrez le backend. Dans *Paramètres*, le modèle effectif est affiché et **Tester la connexion IA**
   vérifie que le service Ollama répond et que le modèle sélectionné est installé.
5. Les paramètres enregistrés dans la base priment sur `.env`. Modifiez le fournisseur et le modèle dans
   *Paramètres* pour les appliquer immédiatement, ou supprimez seulement les réglages correspondants de la
   base si vous souhaitez reprendre les valeurs de `.env`.

Le téléchargement du modèle n'est jamais lancé par l'application ; les modèles Ollama peuvent être volumineux.
Sans LLM configuré, les réponses de démonstration sont explicitement marquées et aucun résumé ou QCM fictif n'est généré.

## 📄 Qualité d'extraction des PDF

Certains PDF (exports Keynote/PowerPoint) ont des ligatures mal encodées (`Introduc=on`). Le backend les
répare automatiquement (`repair_text` dans `backend/app/document_processing/pdf.py`). Si vous aviez importé
un document avant cette correction, **supprimez-le et réimportez-le** pour reconstruire l'index.

### 📖 Documentation Complète

- **[DEMARRAGE-RAPIDE.md](./docs/archive/DEMARRAGE-RAPIDE.md)** - Guide utilisateur complet
- **[STATUS.md](./docs/archive/STATUS.md)** - État technique du projet
- **[REPRISE-COMPLETE.md](./docs/archive/REPRISE-COMPLETE.md)** - Documentation reprise
- **[AIDE-MEMOIRE.md](./docs/archive/AIDE-MEMOIRE.md)** - Aide-mémoire développeur

### 🔍 Vérification Installation

```powershell
.\verify.ps1
```

### Configuration Manuelle (Optionnel)

#### Backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\activate  # Windows
pip install -r requirements.txt

# Configurer les variables d'environnement
copy .env.example .env
# Éditer .env avec vos clés API

# Lancer le serveur
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend

```powershell
cd frontend
npm install

# Configurer les variables d'environnement (optionnel)
copy .env.example .env.local

# Lancer le serveur de développement
npm run dev
```

## 🧪 Tests

### Backend
```bash
cd backend
pytest -v --cov=app
```

### Frontend
```bash
cd frontend
npm run test
npm run typecheck
npm run lint
npm run build
```

## 📚 Documentation

**📌 [INDEX-DOCUMENTATION.md](./INDEX-DOCUMENTATION.md)** - Index complet de toute la documentation

### 🚀 Guides de Démarrage
- **[COMMENCER-ICI.md](./COMMENCER-ICI.md)** - 👈 **COMMENCEZ PAR ICI !**
- [DEMARRAGE-RAPIDE.md](./docs/archive/DEMARRAGE-RAPIDE.md) - Guide utilisateur complet
- [AIDE-MEMOIRE.md](./docs/archive/AIDE-MEMOIRE.md) - Commandes et configuration rapides

### 📖 Documentation Technique
- [STATUS.md](./docs/archive/STATUS.md) - État complet du projet
- [REPRISE-COMPLETE.md](./docs/archive/REPRISE-COMPLETE.md) - Documentation de reprise
- [ARCHITECTURE-VISUELLE.md](./ARCHITECTURE-VISUELLE.md) - Schémas et diagrammes
- [GUIDE-DEVELOPPEUR.md](./GUIDE-DEVELOPPEUR.md) - Guide pour développeurs

### 📋 Documentation Détaillée
- [Architecture](./docs/architecture.md) - Architecture technique
- [Pipeline RAG](./docs/rag-pipeline.md) - Détails du pipeline RAG
- [API Documentation](./docs/api.md) - Documentation API REST
- [Guide de Tests](./docs/testing.md) - Guide de tests
- [Présentation](./docs/presentation.md) - Présentation du projet

## 🔒 Sécurité

- Dédoublonnage des fichiers par empreinte SHA-256
- Validation stricte des entrées (Pydantic)
- Rate limiting sur les endpoints
- Protection contre l'injection de prompt
- Variables d'environnement pour les secrets

## 📝 Licence

MIT

## 👥 Contributeurs

Projet développé dans le cadre d'une démonstration d'architecture RAG professionnelle.
