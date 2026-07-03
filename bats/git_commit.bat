@echo off
setlocal EnableDelayedExpansion
cls
color 0A

title RECETAS_APP - GIT COMMIT

echo =====================================
echo      RECETAS_APP - GIT COMMIT
echo =====================================
echo.

cd /d C:\Users\jrmon\Documents\recetas_app

echo.
echo ===== ESTADO GIT =====
git status

echo.
 
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
echo X. Cancelar Git Commit
echo.

set /p opcion=Seleccione una opcion:

if /I "%opcion%"=="X" (
    echo.
    echo =====================================
    echo GIT COMMIT CANCELADO POR EL USUARIO
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
echo =====================================
echo VERIFICANDO STAGING
echo =====================================
echo.
echo Este BAT ya no ejecuta git add .
echo.
echo Prepare previamente el staging con los archivos
echo que desea incluir en el commit.
echo.
pause

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
echo COMMIT REALIZADO CORRECTAMENTE
echo =====================================

echo.
pause
exit /b

