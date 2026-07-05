:: DEPLOY_RENDER.BAT

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
    echo COMMITS PENDIENTES DE PUSH DETECTADOS
    echo =====================================
    echo.
    echo Hay !commits_pendientes! commits pendientes.
    echo.
    echo 1. Publicar cambios
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
        echo =====================================
        echo ULTIMO COMMIT A PUBLICAR
        echo =====================================
        echo.

        git show --stat --oneline HEAD

        echo.
        echo =====================================
        echo REVISE LOS CAMBIOS ANTES DE PUBLICAR
        echo =====================================
        echo.
        echo 1. Publicar cambios
        echo 9. Cancelar
        echo.

        set /p confirmar_push=Seleccione una opcion:

        if "!confirmar_push!"=="9" (
            echo.
            echo PUSH CANCELADO POR EL USUARIO
            echo.
            pause
            exit /b
        )

        echo.

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
echo NO HAY COMMITS PENDIENTES
echo =====================================
echo.
echo El ultimo Push ya fue realizado.
echo.
echo Si Render tiene Auto Deploy activado,
echo la publicacion ya se encuentra en proceso
echo o ya fue completada.
echo.
pause

