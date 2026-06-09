:: DEPLOY_RENDER.BAT

@echo off
setlocal EnableDelayedExpansion
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
for /f %%a in ('git rev-list --count origin/main..HEAD') do set commits_pendientes=%%a

if not "!commits_pendientes!"=="0" (

    echo =====================================
    echo COMMITS PENDIENTES DE DEPLOY DETECTADOS
    echo =====================================
    echo.
    echo Hay !commits_pendientes! commits pendientes.
    echo.
    echo 1. Realizar Deploy
    echo 9. Cancelar
    echo.

    set /p opcion_deploy=Seleccione una opcion:

    if "!opcion_deploy!"=="9" (
        echo.
        echo DEPLOY CANCELADO POR EL USUARIO
        echo.
        pause
        exit /b
    )

    if "!opcion_deploy!"=="1" (

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
echo 9. Cancelar deploy
echo.

set /p opcion=Seleccione una opcion:

if "%opcion%"=="9" (
    echo.
    echo =====================================
    echo DEPLOY CANCELADO POR EL USUARIO
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
git add modulo_web
git add docs
git add bats

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
echo =====================================
echo ULTIMO COMMIT REALIZADO
echo =====================================
git show --stat --oneline HEAD

echo.
echo =====================================
echo REVISE EL COMMIT ANTES DEL PUSH
echo.
echo Verifique:
echo - Que los archivos esperados esten incluidos
echo - Que no entren backups por error
echo - Que recetas.db este incluida cuando corresponda
echo.
echo Pulse una tecla para continuar con el PUSH...
echo =====================================
pause

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