# Script de vérification de l'installation DocuMind AI

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "   DocuMind AI - Vérification de l'Installation  " -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""

$errors = @()
$warnings = @()

# 1. Vérifier Python
Write-Host "[1/10] Vérification Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1 | Out-String
    if ($pythonVersion -match "Python (\d+\.\d+)") {
        $version = [version]$matches[1]
        if ($version -ge [version]"3.11") {
            Write-Host "  ✓ Python $($matches[1]) installé" -ForegroundColor Green
        } else {
            $errors += "Python 3.11+ requis, version $($matches[1]) détectée"
            Write-Host "  ✗ Python $($matches[1]) trop ancien (requis: 3.11+)" -ForegroundColor Red
        }
    }
} catch {
    $errors += "Python non installé ou non dans PATH"
    Write-Host "  ✗ Python non trouvé" -ForegroundColor Red
}

# 2. Vérifier Node.js
Write-Host "[2/10] Vérification Node.js..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version 2>&1 | Out-String
    if ($nodeVersion -match "v(\d+)") {
        $version = [int]$matches[1]
        if ($version -ge 18) {
            Write-Host "  ✓ Node.js $nodeVersion installé" -ForegroundColor Green
        } else {
            $errors += "Node.js 18+ requis, version $nodeVersion détectée"
            Write-Host "  ✗ Node.js $nodeVersion trop ancien (requis: 18+)" -ForegroundColor Red
        }
    }
} catch {
    $errors += "Node.js non installé ou non dans PATH"
    Write-Host "  ✗ Node.js non trouvé" -ForegroundColor Red
}

# 3. Vérifier structure backend
Write-Host "[3/10] Vérification structure backend..." -ForegroundColor Yellow
$backendFiles = @(
    "backend\app\main.py",
    "backend\requirements.txt",
    "backend\.env.example"
)
$missingBackend = @()
foreach ($file in $backendFiles) {
    if (-not (Test-Path $file)) {
        $missingBackend += $file
    }
}
if ($missingBackend.Count -eq 0) {
    Write-Host "  ✓ Fichiers backend présents" -ForegroundColor Green
} else {
    $errors += "Fichiers backend manquants: $($missingBackend -join ', ')"
    Write-Host "  ✗ Fichiers manquants: $($missingBackend -join ', ')" -ForegroundColor Red
}

# 4. Vérifier environnement virtuel Python
Write-Host "[4/10] Vérification environnement virtuel Python..." -ForegroundColor Yellow
if (Test-Path "backend\.venv") {
    Write-Host "  ✓ Environnement virtuel créé" -ForegroundColor Green
} else {
    $warnings += "Environnement virtuel non créé (sera créé au premier démarrage)"
    Write-Host "  ⚠ Environnement virtuel non trouvé" -ForegroundColor Yellow
}

# 5. Vérifier fichier .env backend
Write-Host "[5/10] Vérification configuration backend..." -ForegroundColor Yellow
if (Test-Path "backend\.env") {
    Write-Host "  ✓ Fichier .env présent" -ForegroundColor Green
    $envContent = Get-Content "backend\.env" -Raw
    if ($envContent -match "LLM_PROVIDER=(\w+)") {
        Write-Host "    Provider LLM: $($matches[1])" -ForegroundColor Cyan
    }
    if ($envContent -match "EMBEDDING_PROVIDER=(\S+)") {
        Write-Host "    Provider Embeddings: $($matches[1])" -ForegroundColor Cyan
    }
} else {
    $warnings += "Fichier .env manquant (copier depuis .env.example)"
    Write-Host "  ⚠ Fichier .env manquant" -ForegroundColor Yellow
}

# 6. Vérifier structure frontend
Write-Host "[6/10] Vérification structure frontend..." -ForegroundColor Yellow
$frontendFiles = @(
    "frontend\package.json",
    "frontend\app\page.tsx",
    "frontend\app\layout.tsx"
)
$missingFrontend = @()
foreach ($file in $frontendFiles) {
    if (-not (Test-Path $file)) {
        $missingFrontend += $file
    }
}
if ($missingFrontend.Count -eq 0) {
    Write-Host "  ✓ Fichiers frontend présents" -ForegroundColor Green
} else {
    $errors += "Fichiers frontend manquants: $($missingFrontend -join ', ')"
    Write-Host "  ✗ Fichiers manquants: $($missingFrontend -join ', ')" -ForegroundColor Red
}

# 7. Vérifier node_modules
Write-Host "[7/10] Vérification dépendances Node.js..." -ForegroundColor Yellow
if (Test-Path "frontend\node_modules") {
    Write-Host "  ✓ Dépendances npm installées" -ForegroundColor Green
} else {
    $warnings += "Dépendances npm non installées (seront installées au premier démarrage)"
    Write-Host "  ⚠ node_modules non trouvé" -ForegroundColor Yellow
}

# 8. Vérifier fichier .env.local frontend
Write-Host "[8/10] Vérification configuration frontend..." -ForegroundColor Yellow
if (Test-Path "frontend\.env.local") {
    Write-Host "  ✓ Fichier .env.local présent" -ForegroundColor Green
} else {
    if (Test-Path "frontend\.env.example") {
        Write-Host "  ⚠ .env.local manquant (utilisation .env.example par défaut)" -ForegroundColor Yellow
        $warnings += "Copier .env.example vers .env.local si nécessaire"
    } else {
        Write-Host "  ✓ Configuration par défaut utilisée" -ForegroundColor Green
    }
}

# 9. Vérifier dossier data
Write-Host "[9/10] Vérification dossier data..." -ForegroundColor Yellow
if (Test-Path "data") {
    Write-Host "  ✓ Dossier data présent" -ForegroundColor Green
    if (Test-Path "data\uploads") {
        Write-Host "    - uploads: présent" -ForegroundColor Cyan
    }
    if (Test-Path "data\chroma") {
        Write-Host "    - chroma: présent" -ForegroundColor Cyan
    }
    if (Test-Path "data\app.db") {
        Write-Host "    - app.db: présent" -ForegroundColor Cyan
    }
} else {
    Write-Host "  ⚠ Dossier data manquant (sera créé automatiquement)" -ForegroundColor Yellow
}

# 10. Vérifier scripts de démarrage
Write-Host "[10/10] Vérification scripts de démarrage..." -ForegroundColor Yellow
$scripts = @(
    "start-backend.ps1",
    "start-frontend.ps1",
    "start.ps1"
)
$missingScripts = @()
foreach ($script in $scripts) {
    if (-not (Test-Path $script)) {
        $missingScripts += $script
    }
}
if ($missingScripts.Count -eq 0) {
    Write-Host "  ✓ Scripts de démarrage présents" -ForegroundColor Green
} else {
    $warnings += "Scripts manquants: $($missingScripts -join ', ')"
    Write-Host "  ⚠ Scripts manquants: $($missingScripts -join ', ')" -ForegroundColor Yellow
}

# Résumé
Write-Host ""
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "                    RÉSUMÉ                        " -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""

if ($errors.Count -eq 0 -and $warnings.Count -eq 0) {
    Write-Host "✅ Tout est parfait ! Prêt à démarrer." -ForegroundColor Green
    Write-Host ""
    Write-Host "Pour démarrer l'application:" -ForegroundColor Cyan
    Write-Host "  Terminal 1: .\start-backend.ps1" -ForegroundColor White
    Write-Host "  Terminal 2: .\start-frontend.ps1" -ForegroundColor White
} elseif ($errors.Count -eq 0) {
    Write-Host "⚠️  Installation OK avec quelques avertissements." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Avertissements:" -ForegroundColor Yellow
    foreach ($warning in $warnings) {
        Write-Host "  • $warning" -ForegroundColor Yellow
    }
    Write-Host ""
    Write-Host "L'application peut démarrer normalement." -ForegroundColor Green
    Write-Host ""
    Write-Host "Pour démarrer:" -ForegroundColor Cyan
    Write-Host "  Terminal 1: .\start-backend.ps1" -ForegroundColor White
    Write-Host "  Terminal 2: .\start-frontend.ps1" -ForegroundColor White
} else {
    Write-Host "❌ Erreurs détectées. Résolution nécessaire." -ForegroundColor Red
    Write-Host ""
    Write-Host "Erreurs:" -ForegroundColor Red
    foreach ($error in $errors) {
        Write-Host "  • $error" -ForegroundColor Red
    }
    if ($warnings.Count -gt 0) {
        Write-Host ""
        Write-Host "Avertissements:" -ForegroundColor Yellow
        foreach ($warning in $warnings) {
            Write-Host "  • $warning" -ForegroundColor Yellow
        }
    }
    Write-Host ""
    Write-Host "Veuillez corriger les erreurs avant de démarrer." -ForegroundColor Red
}

Write-Host ""
Write-Host "Documentation:" -ForegroundColor Cyan
Write-Host "  - DEMARRAGE-RAPIDE.md : Guide de démarrage" -ForegroundColor White
Write-Host "  - STATUS.md : État complet du projet" -ForegroundColor White
Write-Host "  - README.md : Documentation générale" -ForegroundColor White
Write-Host ""
