# 🎯 COMMENCER ICI - DocuMind AI

## Bienvenue sur DocuMind AI ! 👋

Vous découvrez ce projet ? Voici comment démarrer selon votre profil.

---

## 🚀 Je veux LANCER l'application maintenant !

### Étape 1 : Ouvrir 2 terminaux PowerShell

**Terminal 1 - Backend :**
```powershell
cd C:\Users\PC\Desktop\documind-ai
.\start-backend.ps1
```

**Terminal 2 - Frontend :**
```powershell
cd C:\Users\PC\Desktop\documind-ai
.\start-frontend.ps1
```

### Étape 2 : Ouvrir votre navigateur

Accédez à : **http://localhost:3000**

### Étape 3 : Commencer à utiliser

1. Glissez-déposez un PDF sur le dashboard
2. Attendez l'indexation (5-15 secondes)
3. Allez dans "Chat IA"
4. Créez une conversation
5. Sélectionnez votre document
6. Posez votre question !

**➡️ Guide complet :** [DEMARRAGE-RAPIDE.md](./DEMARRAGE-RAPIDE.md)

---

## 📖 Je veux COMPRENDRE le projet

### Vue d'Ensemble Rapide

DocuMind AI est une application RAG (Retrieval-Augmented Generation) qui permet d'interroger des documents PDF avec une IA.

**Architecture :**
- **Frontend** : Next.js 15 (React, TypeScript, Tailwind)
- **Backend** : FastAPI (Python, SQLAlchemy, ChromaDB)
- **Embeddings** : sentence-transformers (multilingue)
- **LLM** : OpenAI / Ollama / Mode démo

**Fonctionnalités principales :**
- 📄 Upload et indexation PDF
- 💬 Chat RAG avec sources
- 📝 Génération de résumés
- 🎓 QCM interactifs
- 🔄 Comparaison de documents
- ⚙️ Configuration runtime

**➡️ Documentation complète :** [STATUS.md](./STATUS.md)

**➡️ Architecture visuelle :** [ARCHITECTURE-VISUELLE.md](./ARCHITECTURE-VISUELLE.md)

---

## 👨‍💻 Je veux DÉVELOPPER / MODIFIER le projet

### Pour les Développeurs

**Prérequis :**
- Python 3.11+
- Node.js 18+
- Connaissance FastAPI et Next.js

**Points d'entrée code :**
- Backend : `backend/app/main.py`
- Frontend : `frontend/app/page.tsx`
- Pipeline RAG : `backend/app/rag/pipeline.py`

**Tests :**
```powershell
# Backend (10 tests)
cd backend
.\.venv\Scripts\python.exe -m pytest -v

# Frontend
cd frontend
npm run typecheck
```

**➡️ Guide développeur :** [GUIDE-DEVELOPPEUR.md](./GUIDE-DEVELOPPEUR.md)

**➡️ Aide-mémoire :** [AIDE-MEMOIRE.md](./AIDE-MEMOIRE.md)

---

## 🔧 Je veux CONFIGURER / PERSONNALISER

### Configuration Backend

Éditez `backend\.env` :

```env
# Changer le provider LLM
LLM_PROVIDER=openai              # demo | openai | ollama
OPENAI_API_KEY=sk-votre-cle

# Ajuster le RAG
RAG_TOP_K=10                     # Plus de contexte
RAG_SCORE_THRESHOLD=0.15         # Moins strict

# Modifier le chunking
CHUNK_SIZE=1000                  # Passages plus longs
CHUNK_OVERLAP=200                # Plus de chevauchement
```

### Configuration Frontend

Éditez `frontend\.env.local` (optionnel) :

```env
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

**➡️ Toutes les options :** [AIDE-MEMOIRE.md](./AIDE-MEMOIRE.md#%EF%B8%8F-configuration-env)

---

## 🐛 J'ai un PROBLÈME

### Problèmes Courants

#### Backend ne démarre pas
```powershell
cd backend
Remove-Item -Recurse -Force .venv
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

#### Frontend ne démarre pas
```powershell
cd frontend
Remove-Item -Recurse -Force node_modules
npm install
```

#### "Backend injoignable"
1. Vérifiez que le backend tourne (terminal 1)
2. Testez : http://127.0.0.1:8000/api/health
3. Vérifiez CORS_ORIGINS dans `.env`

#### Tests ne passent pas
```powershell
cd backend
.\.venv\Scripts\python.exe -m pytest -v --tb=short
```

**➡️ Plus de solutions :** [DEMARRAGE-RAPIDE.md](./DEMARRAGE-RAPIDE.md#-résolution-de-problèmes)

---

## 🎓 Je veux APPRENDRE l'architecture RAG

### Pipeline RAG en 3 étapes

1. **RETRIEVE** : Recherche vectorielle dans ChromaDB
   - Embedding de la question
   - Calcul similarité cosine
   - Top-K passages pertinents

2. **AUGMENT** : Construction du prompt
   - Prompt système
   - Contexte (passages retrouvés)
   - Question utilisateur

3. **GENERATE** : Génération LLM
   - Appel OpenAI/Ollama
   - Réponse contextualisée
   - Sources traçables

**➡️ Détails complets :** [docs/rag-pipeline.md](./docs/rag-pipeline.md)

**➡️ Schémas visuels :** [ARCHITECTURE-VISUELLE.md](./ARCHITECTURE-VISUELLE.md)

---

## 📚 Toute la Documentation

### Guides Utilisateurs
- **[DEMARRAGE-RAPIDE.md](./DEMARRAGE-RAPIDE.md)** - Démarrage et utilisation
- **[README.md](./README.md)** - Documentation générale

### Documentation Technique
- **[STATUS.md](./STATUS.md)** - État complet du projet
- **[REPRISE-COMPLETE.md](./REPRISE-COMPLETE.md)** - Guide reprise projet
- **[ARCHITECTURE-VISUELLE.md](./ARCHITECTURE-VISUELLE.md)** - Schémas architecture

### Guides Développeur
- **[GUIDE-DEVELOPPEUR.md](./GUIDE-DEVELOPPEUR.md)** - Guide développement
- **[AIDE-MEMOIRE.md](./AIDE-MEMOIRE.md)** - Commandes et config rapides

### Documentation Détaillée
- **[docs/architecture.md](./docs/architecture.md)** - Architecture complète
- **[docs/rag-pipeline.md](./docs/rag-pipeline.md)** - Pipeline RAG
- **[docs/api.md](./docs/api.md)** - Documentation API
- **[docs/testing.md](./docs/testing.md)** - Guide tests

---

## ✅ Vérification Installation

Lancez le script de vérification :

```powershell
.\verify.ps1
```

Vous verrez :
- ✅ Prérequis (Python, Node.js)
- ✅ Structure fichiers
- ✅ Configuration
- ✅ Dépendances

---

## 🎯 Parcours Recommandés

### 👤 Utilisateur Final
```
1. DEMARRAGE-RAPIDE.md    → Lancer l'app
2. Utiliser l'interface    → Dashboard, Chat, etc.
3. AIDE-MEMOIRE.md         → Référence rapide
```

### 🧑‍💼 Chef de Projet / Product Owner
```
1. README.md               → Vue d'ensemble
2. STATUS.md               → État et fonctionnalités
3. docs/presentation.md    → Présentation complète
```

### 👨‍💻 Développeur Backend
```
1. ARCHITECTURE-VISUELLE.md → Comprendre l'archi
2. GUIDE-DEVELOPPEUR.md     → Patterns et conventions
3. backend/app/             → Code source
4. docs/api.md              → Endpoints API
```

### 👩‍💻 Développeur Frontend
```
1. ARCHITECTURE-VISUELLE.md → Comprendre l'archi
2. frontend/app/            → Pages Next.js
3. frontend/components/     → Composants React
4. GUIDE-DEVELOPPEUR.md     → Ajouter fonctionnalités
```

### 🔬 Data Scientist / ML Engineer
```
1. docs/rag-pipeline.md     → Pipeline RAG
2. backend/app/rag/         → Code RAG
3. backend/app/embeddings/  → Modèles embeddings
4. backend/app/llm/         → Providers LLM
```

### 🛠️ DevOps / SysAdmin
```
1. DEMARRAGE-RAPIDE.md      → Setup environnement
2. backend/.env.example     → Configuration
3. requirements.txt         → Dépendances Python
4. package.json             → Dépendances Node
```

---

## 🚀 Prochaines Étapes

### Débutant
1. ✅ Lire ce fichier (vous y êtes !)
2. ✅ Lancer l'application ([DEMARRAGE-RAPIDE.md](./DEMARRAGE-RAPIDE.md))
3. ✅ Tester les fonctionnalités
4. ✅ Lire [STATUS.md](./STATUS.md) pour comprendre le projet

### Intermédiaire
1. ✅ Étudier [ARCHITECTURE-VISUELLE.md](./ARCHITECTURE-VISUELLE.md)
2. ✅ Lire le code backend et frontend
3. ✅ Lancer les tests
4. ✅ Modifier la configuration

### Avancé
1. ✅ Suivre [GUIDE-DEVELOPPEUR.md](./GUIDE-DEVELOPPEUR.md)
2. ✅ Ajouter une fonctionnalité
3. ✅ Écrire des tests
4. ✅ Contribuer au projet

---

## 📊 État du Projet

**Statut** : ✅ **100% OPÉRATIONNEL**

- Backend FastAPI : ✅ Complet et testé
- Frontend Next.js : ✅ Complet et responsive
- Tests : ✅ 10/10 passent
- Documentation : ✅ Complète
- Prêt pour : ✅ Démo / Production

---

## 💡 Besoin d'Aide ?

### Ressources
- 📖 **Documentation** : Tous les `.md` dans le projet
- 🧪 **Tests** : `backend/tests/` - exemples d'utilisation
- 💬 **Code** : Commentaires dans le code source
- 🔍 **API Docs** : http://127.0.0.1:8000/docs (après démarrage)

### Commandes Utiles
```powershell
# Vérifier l'installation
.\verify.ps1

# Lancer l'application
.\start-backend.ps1  # Terminal 1
.\start-frontend.ps1 # Terminal 2

# Lancer les tests
cd backend
.\.venv\Scripts\python.exe -m pytest -v
```

---

## 🎉 Prêt à Commencer !

**Commencez maintenant :**

```powershell
# Terminal 1
.\start-backend.ps1

# Terminal 2  
.\start-frontend.ps1
```

Puis ouvrez **http://localhost:3000** 🚀

---

**Bon voyage dans DocuMind AI !** 🎯
