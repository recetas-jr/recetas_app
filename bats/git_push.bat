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
    echo X. Cancelar
    echo.

    set /p opcion_push=Seleccione una opcion:

    
    if /I "!opcion_push!"=="X" (
        echo.
        echo PUSH CANCELADO POR EL USUARIO
        echo.
        pause
        exit /b
    )

    if "!opcion_push!"=="1" (
        
        cls

        echo.
        echo =====================================
        echo ULTIMO COMMIT A ENVIAR
        echo =====================================
        echo.

        git show --stat --oneline HEAD

        echo.

        echo.
        echo.
        echo =====================================
        echo REVISE EL COMMIT ANTES DEL PUSH
        echo =====================================
        echo.
        echo 1. Continuar con el Push
        echo X. Cancelar
        echo.

        set /p confirmar_push=Seleccione una opcion:

        if /I "!confirmar_push!"=="X" (
            echo.
            echo PUSH CANCELADO POR EL USUARIO
            echo.
            pause
            exit /b
        )

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
echo X. Cancelar Git Push
echo.

set /p opcion=Seleccione una opcion:

if /I "%opcion%"=="X" (
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

if not "%opcion%"=="0" if /I not "%opcion%"=="X" (

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
echo =====================================
echo ARCHIVOS INCLUIDOS EN EL COMMIT
echo =====================================
git diff --cached --name-only

echo.
echo =====================================
echo REVISE LOS ARCHIVOS ANTES DEL COMMIT
echo =====================================
echo.
echo 1. Continuar
echo X. Cancelar
echo.

set /p confirmar_archivos=Seleccione una opcion:

if /I "!confirmar_archivos!"=="X" (
    echo COMMIT CANCELADO POR EL USUARIO
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
echo REVISE EL COMMIT ANTES DEL PUSH
echo =====================================
echo.
echo 1. Continuar con el Push
echo X. Cancelar
echo.

set /p confirmar_push=Seleccione una opcion:

if /I "!confirmar_push!"=="X" (
    echo.
    echo PUSH CANCELADO POR EL USUARIO
    echo.
    pause
    exit /b
)

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
