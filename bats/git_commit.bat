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
    set /p mensaje=Escriba el mensaje del commit y presione ENTER:
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
echo Este BAT NO ejecuta automaticamente:
echo.
echo     git add .
echo.
echo Prepare previamente el staging con los archivos
echo que desea incluir en el commit.
echo.
echo Al continuar se verificara si existe
echo un staging valido.
echo.
set /p dummy=Presione ENTER para iniciar la verificacion del staging:

git diff --cached --quiet

if %errorlevel%==0 (
    echo.
    echo =====================================
    echo NO SE DETECTO STAGING
    echo =====================================
    echo.
    echo No existen archivos preparados para el commit.
    echo.
    echo Prepare previamente el staging y vuelva a ejecutar este BAT.
    echo.
    pause
    exit /b
)
echo.
echo =====================================
echo STAGING DETECTADO
echo =====================================
echo.
echo Se encontraron archivos preparados para el commit.
echo A continuacion se muestran los archivos incluidos:
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

