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


