# ------------------------------------------------------------
# ARCHIVO: RECETAS_APP/USB_CAPTURA_REMOTA/crear_usb_captura.py
# PROPOSITO:
# Preparar la estructura del USB de captura remota.
# Crea las carpetas necesarias y los nomencladores iniciales
# si todavía no existen.
# ------------------------------------------------------------

import os

base = "USB_CAPTURA_REMOTA"
nomencladores = os.path.join(base, "NOMENCLADORES")
recetas = os.path.join(base, "RECETAS")

os.makedirs(nomencladores, exist_ok=True)
os.makedirs(recetas, exist_ok=True)

ingredientes_file = os.path.join(nomencladores, "ingredientes.txt")
unidades_file = os.path.join(nomencladores, "unidades.txt")

if not os.path.exists(ingredientes_file):
    with open(ingredientes_file, "w", encoding="utf-8") as f:
        f.write("harina\n")
        f.write("azucar\n")
        f.write("huevo\n")
        f.write("leche\n")
        f.write("mantequilla\n")
        f.write("chocolate\n")

if not os.path.exists(unidades_file):
    with open(unidades_file, "w", encoding="utf-8") as f:
        f.write("g\n")
        f.write("kg\n")
        f.write("ml\n")
        f.write("l\n")
        f.write("u\n")

print("Estructura del USB de captura preparada correctamente.")

"""
RECETAS_APP/USB_CAPTURA_REMOTA/crear_usb_captura.py
"""