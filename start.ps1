# Script de démarrage DocuMind AI
# Lance le backend FastAPI et le frontend Next.js

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "         DocuMind AI - Démarrage                  " -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""

# Vérifier les prérequis
Write-Host "[1/4] Vérification des prérequis..." -ForegroundColor Yellow

# Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "  ✓ Python détecté: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Python n'est pas installé ou pas dans le PATH" -ForegroundColor Red
    exit 1
}

# Node.js
try {
    $nodeVersion = node --version 2>&1
    Write-Host "  ✓ Node.js détecté: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Node.js n'est pas installé ou pas dans le PATH" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "[2/4] Préparation de l'environnement backend..." -ForegroundColor Yellow

# Backend
Set-Location backend

# Vérifier l'environnement virtuel
if (-not (Test-Path ".venv")) {
    Write-Host "  • Création de l'environnement virtuel Python..." -ForegroundColor Cyan
    python -m venv .venv
}

# Activer l'environnement virtuel et installer les dépendances
Write-Host "  • Vérification des dépendances..." -ForegroundColor Cyan
& ".venv\Scripts\python.exe" -m pip install --quiet --upgrade pip
& ".venv\Scripts\python.exe" -m pip install --quiet -r requirements.txt

Write-Host "  ✓ Backend prêt" -ForegroundColor Green

Set-Location ..

Write-Host ""
Write-Host "[3/4] Préparation de l'environnement frontend..." -ForegroundColor Yellow

# Frontend
Set-Location frontend

if (-not (Test-Path "node_modules")) {
    Write-Host "  • Installation des dépendances npm..." -ForegroundColor Cyan
    npm install --silent
} else {
    Write-Host "  ✓ Dépendances npm déjà installées" -ForegroundColor Green
}

Set-Location ..

Write-Host ""
Write-Host "[4/4] Démarrage des serveurs..." -ForegroundColor Yellow
Write-Host ""
Write-Host "  • Backend FastAPI: http://127.0.0.1:8000" -ForegroundColor Cyan
Write-Host "  • Frontend Next.js: http://localhost:3000" -ForegroundColor Cyan
Write-Host "  • API Docs: http://127.0.0.1:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Appuyez sur Ctrl+C pour arrêter les serveurs" -ForegroundColor Gray
Write-Host ""

# Créer les dossiers data si nécessaire
if (-not (Test-Path "data")) {
    New-Item -ItemType Directory -Path "data" | Out-Null
}

# Démarrer le backend en arrière-plan
$backendJob = Start-Job -ScriptBlock {
    Set-Location $using:PWD
    Set-Location backend
    & ".venv\Scripts\python.exe" -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
}

Write-Host "⚡ Backend démarré (Job ID: $($backendJob.Id))" -ForegroundColor Green

# Attendre que le backend soit prêt
Write-Host "⏳ Attente du backend..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

# Démarrer le frontend en arrière-plan
$frontendJob = Start-Job -ScriptBlock {
    Set-Location $using:PWD
    Set-Location frontend
    npm run dev
}

Write-Host "⚡ Frontend démarré (Job ID: $($frontendJob.Id))" -ForegroundColor Green
Write-Host ""
Write-Host "==================================================" -ForegroundColor Green
Write-Host "    DocuMind AI est en cours d'exécution         " -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Ouvrez votre navigateur sur: http://localhost:3000" -ForegroundColor Cyan
Write-Host ""

# Attendre que l'utilisateur arrête les serveurs
try {
    # Afficher les logs en temps réel
    $continue = $true
    while ($continue) {
        $backendOutput = Receive-Job -Job $backendJob -ErrorAction SilentlyContinue
        $frontendOutput = Receive-Job -Job $frontendJob -ErrorAction SilentlyContinue
        
        if ($backendOutput) {
            Write-Host "[Backend] " -ForegroundColor Blue -NoNewline
            Write-Host $backendOutput
        }
        
        if ($frontendOutput) {
            Write-Host "[Frontend] " -ForegroundColor Magenta -NoNewline
            Write-Host $frontendOutput
        }
        
        # Vérifier si les jobs sont toujours en cours
        if ($backendJob.State -ne "Running" -and $frontendJob.State -ne "Running") {
            $continue = $false
        }
        
        Start-Sleep -Milliseconds 500
    }
} finally {
    # Nettoyer les jobs
    Write-Host ""
    Write-Host "Arrêt des serveurs..." -ForegroundColor Yellow
    Stop-Job -Job $backendJob, $frontendJob -ErrorAction SilentlyContinue
    Remove-Job -Job $backendJob, $frontendJob -ErrorAction SilentlyContinue
    Write-Host "✓ Serveurs arrêtés" -ForegroundColor Green
}
