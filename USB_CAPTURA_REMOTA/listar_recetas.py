# ------------------------------------------------------------
# ARCHIVO: USB_CAPTURA_REMOTA/listar_recetas.py
# PROPOSITO:
# Mostrar en pantalla todas las recetas capturadas en el USB.
# ------------------------------------------------------------

import os
import sys

# ------------------------------------------------------------
# CONFIGURACIÓN PORTABLE
# ------------------------------------------------------------

if getattr(sys, 'frozen', False):
    # Ejecutándose como .exe
    BASE_DIR = os.path.dirname(sys.executable)
else:
    # Ejecutándose como .py
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

RECETAS_DIR = os.path.join(BASE_DIR, "RECETAS")

# ------------------------------------------------------------
# VALIDACIÓN
# ------------------------------------------------------------

if not os.path.exists(RECETAS_DIR):
    print("\nLa carpeta RECETAS no existe.\n")
    input("Pulsa ENTER para continuar...")
    sys.exit()

# ------------------------------------------------------------
# LISTADO
# ------------------------------------------------------------

archivos = sorted(os.listdir(RECETAS_DIR))

print("\nRECETAS CAPTURADAS\n")

if not archivos:
    print("No hay recetas capturadas.")
else:
    for archivo in archivos:
        print(archivo)

print("\nFin del listado.\n")

# ------------------------------------------------------------
# PAUSA FINAL (IMPORTANTE PARA .exe)
# ------------------------------------------------------------

input("Pulsa ENTER para volver...")