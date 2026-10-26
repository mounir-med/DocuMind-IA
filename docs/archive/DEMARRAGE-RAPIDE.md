# 🚀 Guide de Démarrage Rapide - DocuMind AI

## ⚡ Démarrage en 2 Minutes

### 1️⃣ Ouvrir deux terminaux PowerShell

**Terminal 1 - Backend:**
```powershell
cd C:\Users\PC\Desktop\documind-ai
.\start-backend.ps1
```

**Terminal 2 - Frontend:**
```powershell
cd C:\Users\PC\Desktop\documind-ai
.\start-frontend.ps1
```

### 2️⃣ Ouvrir votre navigateur

Accédez à: **http://localhost:3000**

C'est tout ! 🎉

---

## 📖 Utilisation de l'Application

### Dashboard (Page d'Accueil)
- Glissez-déposez des PDF directement sur la zone de dépôt
- Consultez les statistiques en temps réel
- Accédez rapidement aux documents et conversations récents

### 📄 Gestion des Documents
1. Cliquez sur **"Documents"** dans le menu latéral
2. Déposez vos fichiers PDF (jusqu'à 25 Mo par fichier)
3. L'application va automatiquement :
   - Extraire le texte
   - Découper en passages intelligents
   - Générer les embeddings
   - Indexer dans ChromaDB
4. Statuts possibles :
   - ✅ **ready** : Document prêt pour les recherches
   - ⏳ **indexing** : En cours d'indexation
   - ⚠️ **error** : Erreur lors du traitement
   - 📸 **scanned** : PDF scanné (OCR non disponible)
   - 🔍 **empty** : Pas assez de texte

### 💬 Chat RAG
1. Cliquez sur **"Chat IA"**
2. Créez une **nouvelle conversation**
3. Sélectionnez les **documents** à interroger
4. Posez votre **question en français**
5. L'IA va :
   - Rechercher les passages pertinents
   - Générer une réponse contextualisée
   - Afficher les sources utilisées

**Fonctionnalités:**
- 📝 Historique complet des conversations
- 🔄 Régénération de réponses
- 📚 Sources traçables avec numéro de page
- 🎯 Sélection multi-documents

### 📝 Résumés
1. Cliquez sur **"Résumés"**
2. Sélectionnez un document
3. Choisissez le type de résumé :
   - **Court** : Résumé en quelques phrases
   - **Détaillé** : Analyse complète
   - **Par chapitre** : Structure détaillée
4. Cliquez sur **"Générer"**

### 🎓 QCM (Quiz)
1. Cliquez sur **"QCM"**
2. Sélectionnez un ou plusieurs documents
3. Configurez :
   - Nombre de questions (5/10/15)
   - Niveau de difficulté (débutant/intermédiaire/avancé)
4. Répondez aux questions
5. Validez pour voir votre score

### 🔄 Comparaison de Documents
1. Cliquez sur **"Comparaison"**
2. Sélectionnez 2 documents ou plus
3. Posez une question comparative
4. Exemple : "Quelles sont les différences entre ces deux contrats ?"

### ⚙️ Paramètres
Configurez l'application sans redémarrage :
- **LLM** : Provider (demo/openai/ollama), modèle, température
- **Embeddings** : Modèle d'embeddings
- **RAG** : Top-K résultats, seuil de score
- **Chunking** : Taille des passages, overlap

---

## 🔧 Configuration Avancée

### Activer un vrai LLM (OpenAI)

1. Obtenez une clé API OpenAI : https://platform.openai.com/api-keys
2. Éditez `backend\.env` :
```env
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-votre-cle-ici
LLM_MODEL=gpt-4o-mini
```
3. Redémarrez le backend

### Activer Ollama (LLM Local)

1. Installez Ollama : https://ollama.ai
2. Téléchargez un modèle :
```powershell
ollama pull llama3.1
```
3. Éditez `backend\.env` :
```env
LLM_PROVIDER=ollama
OLLAMA_MODEL=llama3.1
```
4. Redémarrez le backend

---

## 🧪 Tests

### Backend
```powershell
cd backend
.\.venv\Scripts\python.exe -m pytest -v
```

**Résultat attendu :** 10/10 tests passent ✅

### Frontend
```powershell
cd frontend
npm run typecheck
npm run lint
```

---

## 🎨 Mode Sombre/Clair

Cliquez sur l'icône **Soleil/Lune** en haut à droite pour basculer entre les thèmes.
Le choix est automatiquement sauvegardé.

---

## 📊 URLs Importantes

| Service | URL | Description |
|---------|-----|-------------|
| 🌐 Application | http://localhost:3000 | Interface utilisateur |
| 🔧 API Backend | http://127.0.0.1:8000 | API REST |
| 📖 API Docs | http://127.0.0.1:8000/docs | Documentation Swagger |
| 📖 ReDoc | http://127.0.0.1:8000/redoc | Documentation alternative |

---

## ❓ Résolution de Problèmes

### Le backend ne démarre pas
```powershell
# Vérifier Python
python --version  # Doit être 3.11+

# Réinstaller les dépendances
cd backend
Remove-Item -Recurse -Force .venv
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### Le frontend ne démarre pas
```powershell
# Vérifier Node.js
node --version  # Doit être 18+

# Réinstaller les dépendances
cd frontend
Remove-Item -Recurse -Force node_modules
npm install
```

### "Backend injoignable"
1. Vérifiez que le backend est démarré (terminal 1)
2. Vérifiez l'URL : http://127.0.0.1:8000/api/health
3. Si erreur CORS, vérifiez `CORS_ORIGINS` dans `backend\.env`

### Les embeddings sont lents au premier démarrage
C'est normal ! Le modèle `paraphrase-multilingual-MiniLM-L12-v2` (384 dimensions) se télécharge au premier lancement (~120 Mo).

### PDF scanné non traité
L'OCR (Tesseract) n'est pas activé dans cette version. 
Les PDF scannés (images) ne peuvent pas être traités.
Solution : Utiliser un outil externe pour OCR le PDF avant import.

---

## 📚 Documentation Complète

- [STATUS.md](./STATUS.md) - État complet du projet
- [Architecture](./docs/architecture.md) - Architecture technique
- [Pipeline RAG](./docs/rag-pipeline.md) - Détails du pipeline
- [API](./docs/api.md) - Documentation API
- [Tests](./docs/testing.md) - Guide de test

---

## 🎯 Fonctionnalités Principales

✅ Upload et indexation PDF automatique
✅ Recherche sémantique multilingue
✅ Chat RAG avec sources traçables
✅ Génération de résumés (3 types)
✅ QCM interactifs avec correction
✅ Comparaison multi-documents
✅ Configuration runtime (sans redémarrage)
✅ Mode sombre/clair
✅ Design responsive
✅ Rate limiting
✅ Déduplication SHA-256
✅ Tests complets (10/10 ✅)

---

## 💡 Conseils d'Utilisation

### Pour de meilleurs résultats :
1. **Utilisez des PDF de qualité** : Texte extractible (pas scanné)
2. **Posez des questions précises** : Plus la question est ciblée, meilleure est la réponse
3. **Sélectionnez les bons documents** : Limitez aux documents pertinents pour votre question
4. **Ajustez les paramètres RAG** : 
   - Augmentez `TOP_K` pour plus de contexte
   - Diminuez `SCORE_THRESHOLD` pour des résultats plus larges

### Mode démo vs Production
- **Mode démo** : Réponses simulées pour tester l'interface
- **Mode production** : Configurez OpenAI ou Ollama pour de vraies réponses

---

## 🚀 Prêt à Démarrer !

```powershell
# Terminal 1
.\start-backend.ps1

# Terminal 2
.\start-frontend.ps1
```

Puis ouvrez http://localhost:3000 et commencez à interroger vos PDF ! 🎉
