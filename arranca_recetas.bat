@echo off

title recetas_app

echo Verificando Flask...

netstat -ano | findstr :5000 >nul

if errorlevel 1 (

    echo Flask no encontrado...
    echo Iniciando Flask en PowerShell...

    start "Flask recetas_app" powershell -NoExit -Command "python -m modulo_web.web_app"

:espera
    netstat -ano | findstr :5000 >nul

    if errorlevel 1 (
        timeout /t 1 >nul
        goto espera
    )
)

start http://127.0.0.1:5000/login