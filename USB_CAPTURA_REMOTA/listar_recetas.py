# ------------------------------------------------------------
# ARCHIVO: RECETAS_APP/USB_CAPTURA_REMOTA/listar_recetas.py
# PROPOSITO:
# Mostrar en pantalla todas las recetas capturadas en el USB.
# Sirve para revisión visual rápida sin imprimir nada.
# ------------------------------------------------------------

import os

base = "USB_CAPTURA_REMOTA"
recetas_dir = os.path.join(base, "RECETAS")

if not os.path.exists(recetas_dir):
    print("La carpeta RECETAS no existe.")
    exit()

archivos = sorted(os.listdir(recetas_dir))

print("\nRECETAS CAPTURADAS\n")

if not archivos:
    print("No hay recetas capturadas.")
else:
    for archivo in archivos:
        print(archivo)

print("\nFin del listado.\n")

"""
RECETAS_APP/USB_CAPTURA_REMOTA/listar_recetas.py
"""