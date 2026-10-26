# DocuMind AI

DocuMind AI est une application web qui permet d’importer des documents PDF, de leur poser des questions et de créer des supports de révision. Les réponses s’appuient sur les passages retrouvés dans les documents (RAG) et affichent leurs sources.

## Fonctionnalités

- Import et indexation de plusieurs PDF
- Chat avec les documents et affichage des sources utilisées
- Résumés courts ou détaillés, synthèses par chapitre, idées principales, définitions et fiches de révision
- QCM adaptés au contenu des documents, avec plusieurs niveaux de difficulté
- Comparaison de documents
- Tableau de bord et réglages du modèle IA

## Architecture

- **Frontend :** Next.js, React, TypeScript et Tailwind CSS
- **Backend :** FastAPI et Python
- **Documents et index :** extraction PDF avec PyMuPDF, embeddings multilingues et ChromaDB
- **Métadonnées :** SQLite
- **Génération :** Ollama local ou API compatible OpenAI

## Prérequis

- Windows 10/11 et PowerShell (les scripts fournis sont conçus pour Windows)
- Python 3.11 ou plus récent
- Node.js 18 ou plus récent et npm
- Un fournisseur LLM pour générer les réponses, résumés et QCM : Ollama local ou une clé API OpenAI

## Installation et démarrage rapide

À partir du dossier du projet, ouvrez deux terminaux PowerShell.

**Terminal 1 — backend :**

```powershell
.\start-backend.ps1
```

**Terminal 2 — frontend :**

```powershell
.\start-frontend.ps1
```

L’application est disponible sur [http://localhost:3000](http://localhost:3000). La documentation interactive de l’API est disponible sur [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

Les scripts de démarrage installent les dépendances manquantes dans les environnements locaux du projet lorsqu’ils en ont besoin. Pour tout installer avant le démarrage, utilisez :

```powershell
.\scripts\setup.ps1
```

## Configurer la génération IA

Sans fournisseur LLM configuré, l’application peut afficher les passages trouvés, mais ne génère pas de réponses IA, de résumés ni de QCM.

1. Copiez le modèle de configuration :

   ```powershell
   Copy-Item backend/.env.example backend/.env
   ```

2. Ouvrez `backend/.env` et choisissez un fournisseur.

   **Ollama local :** gardez `LLM_PROVIDER=ollama`, installez et démarrez Ollama, puis téléchargez un modèle :

   ```powershell
   ollama pull llama3.1
   ollama list
   ```

   Le nom du modèle configuré dans `OLLAMA_MODEL` doit correspondre à celui affiché par `ollama list`. Le modèle et Ollama utilisent la mémoire et les ressources de votre ordinateur.

   **OpenAI :** définissez `LLM_PROVIDER=openai`, puis renseignez `OPENAI_API_KEY` et le modèle pris en charge dans `LLM_MODEL`.

3. Redémarrez le backend après toute modification du fichier `.env`.

Les valeurs enregistrées dans la page **Paramètres** peuvent remplacer les valeurs du fichier `.env`. Les clés API doivent rester dans le fichier local `backend/.env` et ne doivent pas être publiées.

## Configuration du frontend

Le frontend utilise par défaut `http://127.0.0.1:8000` pour joindre l’API. Si nécessaire, copiez `frontend/.env.example` vers `frontend/.env.local` et modifiez `NEXT_PUBLIC_API_URL`.

## Installation manuelle

### Backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

Dans un autre terminal :

```powershell
cd frontend
npm install
npm run dev
```

## Données locales

La base de métadonnées, l’index vectoriel et les PDF importés sont conservés localement dans `data/`. Ils sont ignorés par Git et ne sont pas inclus dans le dépôt. Pensez à sauvegarder séparément les documents que vous souhaitez conserver.

## Vérifications

Le script suivant vérifie la configuration locale et les services du projet :

```powershell
.\verify.ps1
```

Tests du backend :

```powershell
cd backend
pytest -v
```

Vérifications du frontend :

```powershell
cd frontend
npm run typecheck
npm run lint
npm test
npm run build
```

## Documentation

- [Architecture](docs/architecture.md)
- [API](docs/api.md)
- [Pipeline RAG](docs/rag-pipeline.md)
- [Guide de tests](docs/testing.md)
- [Présentation](docs/presentation.md)
- [Documentation archivée](docs/archive/)

## Licence

Le dépôt ne contient pas de fichier de licence. Vérifiez les droits applicables aux dépendances et aux documents importés avant toute redistribution.
