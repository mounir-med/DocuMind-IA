$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
if ((Split-Path -Leaf $Root) -eq "scripts") {
  $Root = Split-Path -Parent $Root
}

$backend = Join-Path $Root "backend"
$frontend = Join-Path $Root "frontend"
$python = Join-Path $backend ".venv\Scripts\python.exe"

if (-not (Test-Path $python)) {
  throw "Environnement Python absent. Exécutez d'abord scripts/setup.ps1"
}
if (-not (Test-Path (Join-Path $frontend "node_modules"))) {
  throw "Dépendances Node absentes. Exécutez d'abord scripts/setup.ps1"
}

Write-Host "Démarrage backend http://127.0.0.1:8000 et frontend http://localhost:3000" -ForegroundColor Cyan

Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$backend'; & '$python' -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$frontend'; npm run dev"
