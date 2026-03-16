# ============================================================
# RUTA: C:\Users\jrmon\Documents\recetas_app
# ARCHIVO: detectar_usb.py
# ============================================================

import ctypes
import os
import shutil

def detectar_usb():

    unidades = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    for letra in unidades:

        ruta = f"{letra}:\\"

        if os.path.exists(ruta):

            tipo = ctypes.windll.kernel32.GetDriveTypeW(ruta)

            if tipo == 2:
                return ruta

    return None


def copiar_sistema(usb):

    archivos = [
        "sistema_captura_recetas.exe",
        "capturar_receta.exe",
        "listar_recetas.exe",
        "crear_usb_captura.exe"
    ]

    origen = r"C:\Users\jrmon\Documents\recetas_app\USB_CAPTURA_REMOTA\dist"

    for archivo in archivos:

        origen_archivo = os.path.join(origen, archivo)
        destino_archivo = os.path.join(usb, archivo)

        if os.path.exists(origen_archivo):
            shutil.copy(origen_archivo, destino_archivo)
            print("Copiado:", archivo)
        else:
            print("No encontrado:", archivo)


    # --------------------------------------------------------
    # Copiar carpetas necesarias
    # --------------------------------------------------------

    carpetas = ["RECETAS", "NOMENCLADORES"]

    for carpeta in carpetas:

        origen_carpeta = os.path.join(origen, carpeta)
        destino_carpeta = os.path.join(usb, carpeta)

        if os.path.exists(origen_carpeta):
            shutil.copytree(origen_carpeta, destino_carpeta, dirs_exist_ok=True)
            print("Carpeta copiada:", carpeta)
        else:
            print("Carpeta no encontrada:", carpeta)


if __name__ == "__main__":

    usb = detectar_usb()

    if usb:
        print("USB detectado en:", usb)
        copiar_sistema(usb)
    else:
        print("No se detectó ningún USB conectado.")


# ============================================================
# FIN DEL ARCHIVO
# RUTA: C:\Users\jrmon\Documents\recetas_app
# ARCHIVO: detectar_usb.py
# ============================================================