@echo off
echo ==================================================
echo    DocuMind AI - Backend FastAPI
echo ==================================================
echo.

cd backend

REM Verifier environnement virtuel
if not exist .venv (
    echo Creation de l'environnement virtuel...
    python -m venv .venv
    echo Installation des dependances...
    .venv\Scripts\python.exe -m pip install --upgrade pip
    .venv\Scripts\python.exe -m pip install -r requirements.txt
)

echo Demarrage du serveur FastAPI...
echo API disponible sur: http://127.0.0.1:8000
echo Documentation: http://127.0.0.1:8000/docs
echo.
echo Appuyez sur Ctrl+C pour arreter
echo.

.venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

pause
