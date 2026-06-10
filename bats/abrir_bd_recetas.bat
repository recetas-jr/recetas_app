:: Archivo: bats/abrir_bd_recetas.bat

@echo off

set PROYECTO=%~dp0..

start "" "C:\Program Files\DB Browser for SQLite\DB Browser for SQLite.exe" "%PROYECTO%\modulo_web\recetas.db"