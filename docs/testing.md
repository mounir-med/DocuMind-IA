# Tests

## Backend

Depuis `backend` (venv activé) :

```powershell
python -m pytest -q
```

Les tests utilisent `EMBEDDING_PROVIDER=fake` et `LLM_PROVIDER=fake` (conftest). Aucun appel payant.

Couverture visée :

- health check
- PDF valide / invalide / vide
- chunking et numéros de page
- upload, doublon SHA-256, indexation, recherche filtrée, suppression
- conversations, régénération, dashboard
- question sans réponse utile dans le corpus
- erreurs 404/422

## Évaluation RAG

```powershell
cd C:\Users\PC\Desktop\documind-ai
.\backend\.venv\Scripts\python.exe evaluation\run_eval.py
```

Le rapport `evaluation/last_report.json` calcule Recall@k et MRR sur un mini-corpus synthétique **avec embeddings factices**. Ce n’est pas un score de production.

## Frontend

```powershell
cd frontend
npm run typecheck
npm run lint
npm run test
npm run build
```

`npm run test` vérifie des utilitaires. Les parcours UI se valident manuellement une fois backend et frontend démarrés.
