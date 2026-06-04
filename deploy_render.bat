:: DEPLOY_RENDER.BAT

@echo off
cls
color 0A

title RECETAS_APP - DEPLOY

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
git add arranca_recetas.bat
git add deploy_render.bat

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

if errorlevel 1 (
    echo.
    echo ERROR EN COMMIT
    pause
    exit
)

echo.
echo ===== PUSH A GITHUB =====
git push origin main

if errorlevel 1 (
    echo.
    echo ERROR EN PUSH
    pause
    exit
)

echo.
echo =====================================
echo CAMBIOS ENVIADOS A GITHUB
echo PUSH COMPLETADO CORRECTAMENTE
echo.
echo RENDER ACTUALIZARA LA WEB
echo EN SEGUNDO PLANO
echo.
echo YA PUEDE CERRAR ESTA VENTANA
echo =====================================
echo.

pause