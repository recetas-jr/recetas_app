@echo off
setlocal EnableDelayedExpansion
cls
color 0A

title RECETAS_APP - GIT PUSH

echo =====================================
echo      RECETAS_APP - GIT PUSH
echo =====================================
echo.

cd /d C:\Users\jrmon\Documents\recetas_app

echo.
echo ===== ESTADO GIT =====
git status

echo.
for /f %%a in ('git rev-list --count origin/main..HEAD') do set commits_pendientes=%%a

if not "!commits_pendientes!"=="0" (

    echo =====================================
    echo COMMITS PENDIENTES DE PUSH DETECTADOS
    echo =====================================
    echo.
    echo Hay !commits_pendientes! commits pendientes.
    echo.
    echo 1. Realizar Push
    echo 9. Cancelar
    echo.

    set /p opcion_push=Seleccione una opcion:

    if "!opcion_push!"=="9" (
        echo.
        echo PUSH CANCELADO POR EL USUARIO
        echo.
        pause
        exit /b
    )

    if "!opcion_push!"=="1" (

        echo.
        echo ===== PUSH A GITHUB =====
        git push origin main

        if errorlevel 1 (
            echo.
            echo ERROR EN PUSH
            pause
            exit /b
        )

        echo.
        echo =====================================
        echo PUSH COMPLETADO CORRECTAMENTE
        echo =====================================
        echo.
        pause
        exit /b
    )

    exit /b
)

echo.
echo =====================================
echo MENSAJES DE COMMIT DISPONIBLES
echo =====================================
echo.

set i=0

for /f "usebackq delims=" %%a in ("bats\nomenclador_commits.txt") do (
    set /a i+=1
    call echo %%i%%. %%a
)

echo 0. Escribir mensaje manualmente
echo 9. Cancelar Git Push
echo.

set /p opcion=Seleccione una opcion:

if "%opcion%"=="9" (
    echo.
    echo =====================================
    echo GIT PUSH CANCELADO POR EL USUARIO
    echo =====================================
    echo.
    pause
    exit /b
)

if "%opcion%"=="0" (
    echo.
    set /p mensaje=Escriba mensaje del commit:
)

if not "%opcion%"=="0" if not "%opcion%"=="9" (

    set i=0

    for /f "usebackq delims=" %%a in ("bats\nomenclador_commits.txt") do (

        set /a i+=1

        if "!i!"=="%opcion%" (
            set mensaje=%%a
        )
    )
)

echo.
echo ===== AGREGANDO ARCHIVOS =====
git add .

git diff --cached --quiet

if %errorlevel%==0 (
    echo.
    echo =====================================
    echo NO HAY CAMBIOS PARA PUBLICAR
    echo =====================================
    echo.
    pause
    exit /b
)

echo.
echo ===== COMMIT =====
git commit -m "%mensaje%"

if errorlevel 1 (
    echo.
    echo ERROR EN COMMIT
    pause
    exit /b
)

echo.
echo =====================================
echo ULTIMO COMMIT REALIZADO
echo =====================================
git show --stat --oneline HEAD

echo.
echo =====================================
echo REVISE EL COMMIT ANTES DEL PUSH
echo =====================================
echo.
pause

echo.
echo ===== PUSH A GITHUB =====
git push origin main

if errorlevel 1 (
    echo.
    echo ERROR EN PUSH
    pause
    exit /b
)

echo.
echo =====================================
echo PUSH COMPLETADO CORRECTAMENTE
echo =====================================
echo.

pause
