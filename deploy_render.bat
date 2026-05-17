@echo off
cls
color 0A

echo =====================================
echo    RECETAS_APP - DEPLOY RENDER
 echo =====================================
echo.

cd /d C:\Users\jrmon\Documents\recetas_app

echo.
echo ===== ESTADO GIT =====
git status

echo.
set /p mensaje=Escriba mensaje del commit:

echo.
echo ===== AGREGANDO ARCHIVOS =====
git add modulo_web
git add docs

REM ===== VALIDAR CAMBIOS =====

git diff --cached --quiet

if %errorlevel%==0 (
    echo.
    echo =====================================
    echo   NO HAY CAMBIOS PARA PUBLICAR
    echo =====================================
    echo.
    pause
    exit
)

echo.
echo ===== COMMIT =====
git commit -m "%mensaje%"

echo.
echo ===== PUSH A GITHUB =====
git push origin main

echo.
echo =====================================
echo      DEPLOY ENVIADO A RENDER
 echo =====================================
echo.
pause
