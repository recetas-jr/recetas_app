:: Archivo: arranca_recetas.bat

@echo off
setlocal EnableDelayedExpansion

title recetas_app

set PROYECTO=%~dp0..
set PID_FLASK=

echo.
echo ==========================================
echo         ARRANQUE DE RECETAS_APP
echo ==========================================
echo.

echo Verificando puerto 5000...

for /f "tokens=5" %%P in ('netstat -ano ^| findstr ":5000" ^| findstr "LISTENING"') do (
    set PID_FLASK=%%P
    goto puerto_ocupado
)

echo Puerto 5000 libre. No hay Flask activo.
goto arrancar_flask


:puerto_ocupado
echo.
echo Ya existe un proceso escuchando en el puerto 5000.
echo PID detectado: !PID_FLASK!
echo.
echo R = Reiniciar Flask
echo A = Abrir navegador sin reiniciar
echo X = Cancelar
echo.

set /p ACCION=Seleccione opcion [R/A/X]: 

if /I "!ACCION!"=="R" goto reiniciar_flask
if /I "!ACCION!"=="A" goto abrir_navegador
if /I "!ACCION!"=="X" goto fin

echo.
echo Opcion no valida.
goto puerto_ocupado


:reiniciar_flask
echo.
echo Cerrando proceso PID !PID_FLASK!...
taskkill /PID !PID_FLASK! /F

echo Esperando liberacion del puerto 5000...

:espera_liberacion
set PID_FLASK=
for /f "tokens=5" %%P in ('netstat -ano ^| findstr ":5000" ^| findstr "LISTENING"') do (
    set PID_FLASK=%%P
)

if defined PID_FLASK (
    timeout /t 1 >nul
    goto espera_liberacion
)

goto arrancar_flask


:arrancar_flask
echo.
echo Iniciando Flask en PowerShell...
start "Flask recetas_app" powershell -NoExit -Command "cd '!PROYECTO!'; python -m modulo_web.web_app"

echo Esperando que Flask levante en puerto 5000...

:espera_flask
set PID_FLASK=
for /f "tokens=5" %%P in ('netstat -ano ^| findstr ":5000" ^| findstr "LISTENING"') do (
    set PID_FLASK=%%P
)

if not defined PID_FLASK (
    timeout /t 1 >nul
    goto espera_flask
)

echo Flask detectado en puerto 5000. PID: !PID_FLASK!
goto abrir_navegador


:abrir_navegador
echo.
echo Abriendo navegador...
start http://127.0.0.1:5000/login
goto fin


:fin
exit /b:: Archivo: backup_proyecto.bat

@echo off

cd /d "%~dp0.."

py backup_proyecto.py

echo.
pause:: Archivo: backup_recetas.bat

@echo off

cd /d "%~dp0.."

py backup_recetas.py

echo.
pause:: DEPLOY_RENDER.BAT

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

pause@echo off
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
    echo Hay !commits_pendientes! commit(s) pendiente(s).
    echo.
    echo 1. Realizar Push
    echo 9. Cancelar
    echo.

    set /p opcion_push=Seleccione una opcion:

    if "!opcion_push!"=="9" (
        echo.
        echo PUSH CANCELADO POR EL USUARIO
        echo.
        pause
        exit /b
    )

    if "!opcion_push!"=="1" (

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
echo 9. Cancelar Git Push
echo.

set /p opcion=Seleccione una opcion:

if "%opcion%"=="9" (
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
echo ULTIMO COMMIT REALIZADO
echo =====================================
git show --stat --oneline HEAD

echo.
echo =====================================
echo REVISE EL COMMIT ANTES DEL PUSH
echo =====================================
echo.
pause

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
echo 7. Nomenclador de commits
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
if "%opcion%"=="7" call "%~dp0nomenclador_commits.bat"
if "%opcion%"=="0" goto fin

goto menu

:fin
exit /b@echo off

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
exit /bRECETAS: correcciones menores y estabilizacion general
RECETAS: actualizar documentacion tecnica
RECETAS: mejoras de navegacion
RECETAS: mejoras modulo Contactos Web
RECETAS: ajustes editor de recetas
RECETAS: reorganizacion herramientas BAT
RECETAS: mejoras proceso Deploy Render
RECETAS: estabilizacion herramientas administrativas BAT
RECETAS: mejora ergonomia proceso Git Push
:: Archivo: backup_proyecto.bat

@echo off

cd /d "%~dp0.."

py backup_proyecto.py

echo.
pause:: Archivo: backup_recetas.bat

@echo off

cd /d "%~dp0.."

py backup_recetas.py

echo.
pause:: DEPLOY_RENDER.BAT

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

pause@echo off
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
    echo Hay !commits_pendientes! commit(s) pendiente(s).
    echo.
    echo 1. Realizar Push
    echo 9. Cancelar
    echo.

    set /p opcion_push=Seleccione una opcion:

    if "!opcion_push!"=="9" (
        echo.
        echo PUSH CANCELADO POR EL USUARIO
        echo.
        pause
        exit /b
    )

    if "!opcion_push!"=="1" (

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
echo 9. Cancelar Git Push
echo.

set /p opcion=Seleccione una opcion:

if "%opcion%"=="9" (
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
echo ULTIMO COMMIT REALIZADO
echo =====================================
git show --stat --oneline HEAD

echo.
echo =====================================
echo REVISE EL COMMIT ANTES DEL PUSH
echo =====================================
echo.
pause

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
echo 7. Nomenclador de commits
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
if "%opcion%"=="7" call "%~dp0nomenclador_commits.bat"
if "%opcion%"=="0" goto fin

goto menu

:fin
exit /b@echo off

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
exit /bRECETAS: correcciones menores y estabilizacion general
RECETAS: actualizar documentacion tecnica
RECETAS: mejoras de navegacion
RECETAS: mejoras modulo Contactos Web
RECETAS: ajustes editor de recetas
RECETAS: reorganizacion herramientas BAT
RECETAS: mejoras proceso Deploy Render
RECETAS: estabilizacion herramientas administrativas BAT
RECETAS: mejora ergonomia proceso Git Push
