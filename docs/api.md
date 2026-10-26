# API REST

Base : `http://127.0.0.1:8000`  
Documentation interactive : `/docs`

## Santé

`GET /api/health` — statut, fournisseur LLM (sans secret), embeddings, vector store.

## Documents

- `POST /api/documents/upload` — multipart `file`
- `GET /api/documents`
- `GET /api/documents/{document_id}`
- `DELETE /api/documents/{document_id}`
- `POST /api/documents/{document_id}/index`
- `GET /api/documents/{document_id}/file` — PDF
- `GET /api/documents/{document_id}/pages/{page_number}`
- `POST /api/documents/{document_id}/summarize` — `{ "kind": "short|detailed|chapters|ideas|definitions|revision" }`
- `POST /api/documents/{document_id}/quiz` — `{ "count", "level", "document_ids" }`
- `POST /api/documents/compare` — `{ "document_ids": [...], "question": "..." }`

## Conversations et chat

- `POST /api/conversations` — `{ "title" }`
- `GET /api/conversations`
- `GET /api/conversations/{conversation_id}`
- `DELETE /api/conversations/{conversation_id}`
- `POST /api/chat/{conversation_id}/messages` — `{ "content", "document_ids", "regenerate" }`

Réponse chat : messages utilisateur/assistant, `sources` (nom, page, extrait, score), `generation` (provider, demo, erreurs).

Le streaming HTTP n’est pas activé : la génération est synchrone afin d’éviter un flux partiel non fiable.

## Statistiques et paramètres

- `GET /api/dashboard/stats`
- `GET /api/settings` — jamais de clé API
- `PUT /api/settings` — provider, modèle, température, top-k, seuil

## Erreurs

JSON `{ "detail": "...", "code": "..." }` avec codes HTTP 400/404/422/503.
