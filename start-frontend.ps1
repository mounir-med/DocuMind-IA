# Démarrage du frontend Next.js DocuMind AI

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "    DocuMind AI - Frontend Next.js                " -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""

Set-Location frontend

# Vérifier les dépendances
if (-not (Test-Path "node_modules")) {
    Write-Host "Installation des dépendances npm..." -ForegroundColor Yellow
    npm install
}

Write-Host "Démarrage du serveur Next.js..." -ForegroundColor Green
Write-Host "Application disponible sur: http://localhost:3000" -ForegroundColor Cyan
Write-Host ""

npm run dev
