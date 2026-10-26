# 🚀 Démarrage Manuel - DocuMind AI

## ⚠️ Si les Scripts PowerShell Ne Fonctionnent Pas

Si vous avez l'erreur "l'exécution de scripts est désactivée", utilisez ce guide.

---

## 📋 Prérequis

Avant de commencer, assurez-vous d'avoir :

- ✅ Python 3.11+ installé
- ✅ Node.js 18+ installé
- ✅ PowerShell ou Command Prompt

Vérification rapide :
```powershell
python --version
node --version
```

---

## 🎯 Méthode 1 : Démarrage Direct (Recommandé)

### Étape 1 : Lancer le Backend

**Ouvrir un terminal PowerShell** et exécuter :

```powershell
cd C:\Users\PC\Desktop\documind-ai\backend
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Résultat attendu** :
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

✅ Le backend est lancé ! Laissez ce terminal ouvert.

---

### Étape 2 : Lancer le Frontend

**Ouvrir un NOUVEAU terminal PowerShell** et exécuter :

```powershell
cd C:\Users\PC\Desktop\documind-ai\frontend
npm run dev
```

**Résultat attendu** :
```
> documind-ai-frontend@1.0.0 dev
> next dev --port 3000

  ▲ Next.js 15.1.6
  - Local:        http://localhost:3000
  - Ready in 2.3s
```

✅ Le frontend est lancé ! Laissez ce terminal ouvert.

---

### Étape 3 : Ouvrir le Navigateur

Ouvrez votre navigateur et accédez à :

**http://localhost:3000**

🎉 L'application est maintenant accessible !

---

## 🎯 Méthode 2 : Avec Command Prompt (cmd)

Si vous préférez Command Prompt :

### Terminal 1 - Backend

```cmd
cd C:\Users\PC\Desktop\documind-ai\backend
.venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Terminal 2 - Frontend

```cmd
cd C:\Users\PC\Desktop\documind-ai\frontend
npm run dev
```

---

## 🔧 Si l'Environnement Virtuel N'Existe Pas

Si vous avez l'erreur "le chemin spécifié est introuvable" pour `.venv` :

### Créer l'Environnement Virtuel Backend

```powershell
cd C:\Users\PC\Desktop\documind-ai\backend
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Puis relancez le backend.

---

## 🔧 Si node_modules N'Existe Pas

Si vous avez l'erreur pour le frontend :

### Installer les Dépendances Frontend

```powershell
cd C:\Users\PC\Desktop\documind-ai\frontend
npm install
```

Puis relancez le frontend.

---

## 🌐 URLs Importantes

Une fois les deux serveurs lancés :

| Service | URL |
|---------|-----|
| 🌐 **Application** | http://localhost:3000 |
| 🔧 **API Backend** | http://127.0.0.1:8000 |
| 📖 **API Docs** | http://127.0.0.1:8000/docs |

---

## 🛑 Arrêter les Serveurs

Pour arrêter proprement :

1. Dans chaque terminal, appuyez sur **Ctrl+C**
2. Fermez les terminaux

---

## 🔄 Redémarrer

Pour redémarrer après un arrêt :

1. Répétez les Étapes 1 et 2
2. Pas besoin de réinstaller les dépendances

---

## 🐛 Résolution de Problèmes

### Backend ne démarre pas

**Erreur : "python n'est pas reconnu"**
```powershell
# Vérifier Python
python --version

# Si non trouvé, installer Python 3.11+
```

**Erreur : "No module named 'fastapi'"**
```powershell
cd backend
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

---

### Frontend ne démarre pas

**Erreur : "npm n'est pas reconnu"**
```powershell
# Vérifier Node.js
node --version
npm --version

# Si non trouvé, installer Node.js 18+
```

**Erreur : "Cannot find module"**
```powershell
cd frontend
npm install
```

---

### "Backend injoignable" dans l'interface

1. Vérifier que le backend tourne (terminal 1)
2. Tester : http://127.0.0.1:8000/api/health
3. Si erreur, vérifier les logs du terminal backend

---

### Port déjà utilisé

**Erreur : "Address already in use"**

**Backend (port 8000) :**
```powershell
# Trouver le processus
netstat -ano | findstr :8000

# Tuer le processus (remplacer PID)
taskkill /PID <PID> /F
```

**Frontend (port 3000) :**
```powershell
# Trouver le processus
netstat -ano | findstr :3000

# Tuer le processus (remplacer PID)
taskkill /PID <PID> /F
```

---

## 🎯 Commandes Complètes (Copier-Coller)

### Pour le Backend

```powershell
cd C:\Users\PC\Desktop\documind-ai\backend
if (-not (Test-Path .venv)) { python -m venv .venv; .\.venv\Scripts\python.exe -m pip install -r requirements.txt }
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Pour le Frontend

```powershell
cd C:\Users\PC\Desktop\documind-ai\frontend
if (-not (Test-Path node_modules)) { npm install }
npm run dev
```

---

## 📝 Alternative : Fichiers Batch (.bat)

Si PowerShell pose problème, créez des fichiers `.bat` :

### `start-backend.bat`

```batch
@echo off
cd backend
if not exist .venv (
    echo Creation environnement virtuel...
    python -m venv .venv
    .venv\Scripts\python.exe -m pip install -r requirements.txt
)
echo Demarrage backend...
.venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
pause
```

### `start-frontend.bat`

```batch
@echo off
cd frontend
if not exist node_modules (
    echo Installation dependances...
    npm install
)
echo Demarrage frontend...
npm run dev
pause
```

Double-cliquez sur ces fichiers pour démarrer !

---

## ✅ Checklist Démarrage

- [ ] Terminal 1 ouvert
- [ ] Backend lancé (port 8000)
- [ ] Backend affiche "Application startup complete"
- [ ] Terminal 2 ouvert
- [ ] Frontend lancé (port 3000)
- [ ] Frontend affiche "Ready in X.Xs"
- [ ] Navigateur ouvert sur http://localhost:3000
- [ ] Page s'affiche correctement

---

## 🎉 C'est Parti !

Une fois les deux terminaux lancés et l'application ouverte :

1. **Testez la connexion** : Le dashboard doit s'afficher
2. **Uploadez un PDF** : Glissez-déposez un fichier
3. **Créez une conversation** : Cliquez sur "Chat IA"
4. **Posez une question** : Testez le RAG !

---

## 📚 Plus d'Aide

- **Documentation complète** : [DEMARRAGE-RAPIDE.md](./DEMARRAGE-RAPIDE.md)
- **Problèmes courants** : [DEMARRAGE-RAPIDE.md](./DEMARRAGE-RAPIDE.md#-résolution-de-problèmes)
- **Guide développeur** : [GUIDE-DEVELOPPEUR.md](./GUIDE-DEVELOPPEUR.md)

---

**Bon démarrage ! 🚀**
