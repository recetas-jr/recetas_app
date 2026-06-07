@echo off

:menu

cls

echo.
echo =====================================
echo      NOMENCLADOR DE COMMITS
echo =====================================
echo.
echo 1. Ver mensajes
echo 2. Agregar mensaje
echo 3. Eliminar mensaje
echo.
echo 0. Volver al Centro de Administracion Tecnica
echo.

set /p opcion=Seleccione opcion:

if "%opcion%"=="1" goto ver
if "%opcion%"=="2" goto agregar
if "%opcion%"=="3" goto eliminar
if "%opcion%"=="0" goto menu_principal

goto menu

:ver

cls

echo.
echo =====================================
echo MENSAJES DISPONIBLES
echo =====================================
echo.

set i=0

for /f "usebackq delims=" %%a in ("%~dp0nomenclador_commits.txt") do (
    set /a i+=1
    call echo %%i%%. %%a
)

echo.
pause

goto menu

:agregar

cls

echo.
echo =====================================
echo AGREGAR MENSAJE
echo =====================================
echo.
echo Escriba el nuevo mensaje y pulse Enter.
echo.
echo 0 = Cancelar
echo.

set /p nuevo= Mensaje :

if "%nuevo%"=="0" goto menu

if "%nuevo%"=="" goto agregar

echo %nuevo%>>"%~dp0nomenclador_commits.txt"

echo.
echo Mensaje agregado correctamente.
echo.
pause

goto menu

:eliminar

cls

echo.
echo =====================================
echo ELIMINAR MENSAJE
echo =====================================
echo.

set i=0

for /f "usebackq delims=" %%a in ("%~dp0nomenclador_commits.txt") do (
    set /a i+=1
    call echo %%i%%. %%a
)

echo.
echo 0 = Cancelar
echo.

set /p borrar=Numero a eliminar:

if "%borrar%"=="0" goto menu

echo.

set mensaje=

setlocal EnableDelayedExpansion

set contador=0

for /f "usebackq delims=" %%a in ("%~dp0nomenclador_commits.txt") do (
    set /a contador+=1

    if "!contador!"=="%borrar%" (
        set mensaje=%%a
    )
)

echo.
echo Mensaje seleccionado:
echo !mensaje!
echo.
set /p confirma=Confirma eliminar este mensaje ? (S/N):

if /i not "%confirma%"=="S" (
    endlocal
    goto menu
)

endlocal

setlocal EnableDelayedExpansion

set contador=0

(
for /f "usebackq delims=" %%a in ("%~dp0nomenclador_commits.txt") do (
    set /a contador+=1

    if NOT "!contador!"=="%borrar%" (
        echo %%a
    )
)
) > "%~dp0nomenclador_tmp.txt"

move /y "%~dp0nomenclador_tmp.txt" "%~dp0nomenclador_commits.txt" >nul

endlocal

echo.
echo Mensaje eliminado correctamente.
echo.
pause

goto menu

:menu_principal
call "%~dp0menu_administracion_tecnica.bat"
exit /b