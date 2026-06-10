:: Archivo: arranca_recetas.bat

@echo off
setlocal EnableDelayedExpansion

title recetas_app

set PROYECTO=%~dp0..

echo Verificando Flask...

netstat -ano | findstr :5000 >nul

if errorlevel 1 (

    echo Flask no encontrado...
    echo Iniciando Flask en PowerShell...

    start "Flask recetas_app" powershell -NoExit -Command "cd '!PROYECTO!'; python -m modulo_web.web_app"

:espera
    netstat -ano | findstr :5000 >nul

    if errorlevel 1 (
        timeout /t 1 >nul
        goto espera
    )
)

start http://127.0.0.1:5000/login