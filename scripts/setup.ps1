$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
if (-not $PSScriptRoot) { $Root = (Get-Location).Path }
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
if ((Split-Path -Leaf $Root) -eq "scripts") {
  $Root = Split-Path -Parent $Root
}

Write-Host "DocuMind AI — installation initiale" -ForegroundColor Cyan

function Require-Cmd($name) {
  if (-not (Get-Command $name -ErrorAction SilentlyContinue)) {
    throw "Commande introuvable : $name. Installez-la puis relancez scripts/setup.ps1."
  }
}

Require-Cmd python
Require-Cmd npm

New-Item -ItemType Directory -Force -Path (Join-Path $Root "data\uploads") | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $Root "data\chroma") | Out-Null

$backend = Join-Path $Root "backend"
$frontend = Join-Path $Root "frontend"

if (-not (Test-Path (Join-Path $backend ".env"))) {
  Copy-Item (Join-Path $backend ".env.example") (Join-Path $backend ".env")
  Write-Host "Fichier backend/.env créé depuis .env.example"
}
if (-not (Test-Path (Join-Path $frontend ".env.local"))) {
  Copy-Item (Join-Path $frontend ".env.example") (Join-Path $frontend ".env.local")
  Write-Host "Fichier frontend/.env.local créé depuis .env.example"
}

Set-Location $backend
if (-not (Test-Path ".venv")) {
  python -m venv .venv
}
& ".\.venv\Scripts\python.exe" -m pip install --upgrade pip
& ".\.venv\Scripts\python.exe" -m pip install -r requirements.txt

Set-Location $frontend
npm install

Write-Host "Installation terminée. Lancez ensuite scripts/start.ps1" -ForegroundColor Green
