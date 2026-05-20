@echo off

title recetas_app

echo ¿Flask ya está abierto?
echo.
echo 1 = SI
echo 2 = NO
echo.

set /p opcion=Seleccione:

if "%opcion%"=="2" (

    start cmd /c "python -m modulo_web.web_app"

    pause
)

start http://127.0.0.1:5000/login