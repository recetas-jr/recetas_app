:: Archivo: bats/menu_administracion_tecnica.bat

@echo off

:menu

cls

echo.
echo ===================================================
echo      RECETAS_APP - Centro de Administracion Tecnica
echo ===================================================
echo.
echo 1. Arrancar sistema
echo 2. Abrir base de datos
echo.
echo 3. Backup proyecto
echo 4. Backup recetas
echo.
echo 5. Git Push
echo 6. Deploy Render
echo.
echo 0. SALIR
echo.

set /p opcion=Seleccione opcion: 

if "%opcion%"=="1" call "%~dp0arranca_recetas.bat"
if "%opcion%"=="2" call "%~dp0abrir_bd_recetas.bat"
if "%opcion%"=="3" call "%~dp0backup_proyecto.bat"
if "%opcion%"=="4" call "%~dp0backup_recetas.bat"
if "%opcion%"=="5" call "%~dp0git_push.bat"
if "%opcion%"=="6" call "%~dp0deploy_render.bat"
if "%opcion%"=="0" goto fin

goto menu

:fin
exit /b