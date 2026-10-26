# Plan de soutenance — DocuMind AI

Titre : *Conception et développement d’un assistant intelligent de question-réponse sur des documents PDF basé sur l’architecture RAG*.

## 1. Introduction (1 min)

Présenter DocuMind AI comme une application locale qui permet d’interroger plusieurs PDF en français, avec des réponses vérifiables.

## 2. Problématique (1 min)

Comment retrouver les bons passages dans un corpus PDF et générer une réponse fondée, citée, plutôt qu’une hallucination ?

## 3. Objectifs (1 min)

Importer, indexer, questionner, résumer, comparer, générer des QCM, avec sources et persistance locale.

## 4. Architecture (2 min)

Montrer le schéma Mermaid frontend / FastAPI / SQLite / Chroma / LLM. Insister sur la séparation des secrets et l’absence d’authentification (démo locale).

## 5. Fonctionnement du RAG (3 min)

Ingestion PyMuPDF → chunks paginés → embeddings → Chroma → retriever → prompt anti-hallucination → sources. Montrer le diagramme de séquence.

## 6. Démonstration (5 min)

1. Importer deux PDF.
2. Poser une question ciblée, ouvrir une source à la page citée.
3. Générer un résumé et un QCM.
4. Comparer deux documents.
5. Montrer le mode démo si aucune clé n’est configurée.

## 7. Résultats des tests (1 min)

Citer uniquement les tests réellement exécutés (pytest, tsc, lint, build). Ne pas inventer de scores.

## 8. Limites (1 min)

Pas d’OCR, pas d’auth, embeddings lourds au premier téléchargement, score non probabiliste, LLM optionnel.

## 9. Conclusion (1 min)

Le RAG relie recherche et génération. Pistes : OCR, PostgreSQL, multi-utilisateurs, streaming, i18n EN/AR.
