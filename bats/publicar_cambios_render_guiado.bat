@echo off
setlocal EnableDelayedExpansion
cls
color 0A

title RECETAS_APP - PUBLICAR CAMBIOS GUIADO

echo ============================================================
echo             RECETAS_APP - PUBLICAR CAMBIOS
echo ============================================================
echo.
echo Este BAT guia SOLO el flujo de publicacion.
echo NO repite pruebas funcionales ya realizadas.
echo.
echo Flujo:
echo   1. Revisar cambios locales
echo   2. Seleccionar archivos a publicar
echo   3. Crear commit
echo   4. Publicar en GitHub
echo   5. Abrir Deploys de Render
echo   6. Confirmar que el cambio quede listo
echo.
echo NO se ejecuta "git add ."
echo ============================================================
echo.

cd /d C:\Users\jrmon\Documents\recetas_app

if errorlevel 1 (
    echo [ERROR] No se pudo entrar al proyecto.
    pause
    exit /b 1
)

echo.
echo [ETAPA 1/6] ESTADO LOCAL
echo ------------------------------------------------------------
echo.
git status

echo.
echo ---------------- PAUSA 1 ----------------
echo.
echo REVISION DEL ESTADO LOCAL
echo.
echo Detencion para revisar los cambios que existen en el proyecto
echo antes de seleccionar que sera publicado.
echo.
echo Pulsa ENTER para continuar.
pause >nul

echo.
echo [ETAPA 2/6] STAGING SELECTIVO
echo ------------------------------------------------------------
echo.
echo Escribe UNO POR UNO los archivos que SI deseas publicar.
echo Pulsa ENTER sin escribir archivo cuando hayas terminado.
echo.

set contador=0

:pedir_archivo
set /a siguiente=contador+1
set "archivo="
set /p "archivo=ARCHIVO !siguiente!: "

if "!archivo!"=="" goto revisar_staging

if not exist "!archivo!" (
    echo.
    echo [ERROR] El archivo no existe:
    echo !archivo!
    echo.
    goto pedir_archivo
)

git add -- "!archivo!"

if errorlevel 1 (
    echo.
    echo [ERROR] No se pudo preparar:
    echo !archivo!
    echo.
    goto pedir_archivo
)

set /a contador+=1
echo [OK] Preparado: !archivo!
echo.
goto pedir_archivo

:revisar_staging

echo.
echo ===== CAMBIOS PREPARADOS =====
git status

echo.
echo ===== RESUMEN =====
git diff --cached --stat

git diff --cached --quiet

if not errorlevel 1 (
    echo.
    echo [ATENCION] NO HAY ARCHIVOS PREPARADOS PARA PUBLICAR.
    echo.
    echo El BAT no continuara hacia COMMIT.
    echo Debes seleccionar al menos un archivo.
    echo.
    pause
    exit /b 2
)

echo.
echo ---------------- PAUSA 2 ----------------
echo.
echo REVISION DEL STAGING
echo.
echo Detencion para confirmar que SOLO estan preparados los archivos
echo que deseas incluir en este commit.
echo.
echo Pulsa ENTER para continuar.
pause >nul

echo.
echo [ETAPA 3/6] CREAR COMMIT
echo ------------------------------------------------------------
echo.

set "mensaje_commit="
set /p "mensaje_commit=MENSAJE DEL COMMIT: "

if "!mensaje_commit!"=="" (
    echo.
    echo [ERROR] Debes indicar un mensaje de commit.
    pause
    exit /b 1
)

echo.
git commit -m "!mensaje_commit!"

if errorlevel 1 (
    echo.
    echo [ERROR] El commit no se pudo crear.
    pause
    exit /b 1
)

echo.
echo ===== ULTIMO COMMIT =====
git log -1 --oneline

echo.
echo ---------------- PAUSA 3 ----------------
echo.
echo CONFIRMACION DEL COMMIT
echo.
echo Detencion antes de publicar en GitHub.
echo El commit ya fue creado y debe revisarse antes del push.
echo.
echo Pulsa ENTER para continuar.
pause >nul

echo.
echo [ETAPA 4/6] PUBLICAR EN GITHUB
echo ------------------------------------------------------------
echo.

git push origin main

if errorlevel 1 (
    echo.
    echo [ERROR] El push fallo.
    pause
    exit /b 1
)

for /f "delims=" %%a in ('git rev-parse --short HEAD') do set commit_publicado=%%a

echo.
echo [OK] GitHub recibio el commit:
echo !commit_publicado!

echo.
echo ---------------- PAUSA 4 ----------------
echo.
echo CONFIRMACION DEL PUSH
echo.
echo Detencion despues de publicar en GitHub y antes de comprobar
echo el despliegue en Render.
echo.
echo Pulsa ENTER para continuar.
pause >nul

echo.
echo [ETAPA 5/6] DEPLOY EN RENDER
echo ------------------------------------------------------------
echo.
echo Se abrira la pantalla de Deploys de recetas-master.
echo.
echo Debes comprobar que el commit:
echo.
echo     !commit_publicado!
echo.
echo aparezca como Live o Deployed.
echo.

start "" "https://dashboard.render.com/web/srv-d810861j2pic73binp10/deploys"

echo.
echo ---------------- PAUSA 5 ----------------
echo.
echo CONFIRMACION DEL DEPLOY
echo.
echo Detencion para comprobar en Render que el commit publicado
echo esta Live/Deployed antes de dar las modificaciones por listas.
echo.
echo Pulsa ENTER para continuar.
pause >nul

echo.
echo [ETAPA 6/6] CAMBIO LISTO PARA UTILIZARSE
echo ------------------------------------------------------------
echo.
echo Commit publicado: !commit_publicado!
echo.
echo ============================================================
echo              PUBLICACION COMPLETADA
echo ============================================================
echo.
echo Este BAT no realiza pruebas funcionales.
echo Las pruebas de la aplicacion se realizan aparte.
echo.
pause
