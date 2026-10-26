# Démarrage du backend FastAPI DocuMind AI

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "    DocuMind AI - Backend FastAPI                 " -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""

Set-Location backend

# Vérifier l'environnement virtuel
if (-not (Test-Path ".venv")) {
    Write-Host "Création de l'environnement virtuel..." -ForegroundColor Yellow
    python -m venv .venv
    Write-Host "Installation des dépendances..." -ForegroundColor Yellow
    & ".venv\Scripts\python.exe" -m pip install -r requirements.txt
}

Write-Host "Démarrage du serveur FastAPI..." -ForegroundColor Green
Write-Host "API disponible sur: http://127.0.0.1:8000" -ForegroundColor Cyan
Write-Host "Documentation: http://127.0.0.1:8000/docs" -ForegroundColor Cyan
Write-Host ""

& ".venv\Scripts\python.exe" -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
