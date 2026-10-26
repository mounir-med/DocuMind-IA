@echo off
echo ==================================================
echo    DocuMind AI - Frontend Next.js
echo ==================================================
echo.

cd frontend

REM Verifier node_modules
if not exist node_modules (
    echo Installation des dependances npm...
    npm install
)

echo Demarrage du serveur Next.js...
echo Application disponible sur: http://localhost:3000
echo.
echo Appuyez sur Ctrl+C pour arreter
echo.

npm run dev

pause
