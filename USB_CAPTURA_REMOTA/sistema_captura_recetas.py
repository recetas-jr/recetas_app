# ============================================================
# RUTA: USB_CAPTURA_REMOTA/sistema_captura_recetas.py
# ARCHIVO: sistema_captura_recetas.py
# SISTEMA: captura remota de recetas (VERSIÓN CORREGIDA FINAL)
# ============================================================

import os
import sys
import subprocess

# ------------------------------------------------------------
# CONFIGURACIÓN BASE PORTABLE (CORRECTA)
# ------------------------------------------------------------

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

RECETAS_DIR = os.path.join(BASE_DIR, "RECETAS")
NOMENCLADORES_DIR = os.path.join(BASE_DIR, "NOMENCLADORES")

# ------------------------------------------------------------
# FUNCIONES DEL SISTEMA
# ------------------------------------------------------------


def capturar():

    if getattr(sys, 'frozen', False):
        subprocess.run(
            [os.path.join(BASE_DIR, "capturar_receta.exe")]
        )

    else:
        subprocess.run(
            [sys.executable, os.path.join(BASE_DIR, "capturar_receta.py")]
        )


def listar():

    if getattr(sys, 'frozen', False):
        subprocess.run(
            [os.path.join(BASE_DIR, "listar_recetas.exe")]
        )

    else:
        subprocess.run(
            [sys.executable, os.path.join(BASE_DIR, "listar_recetas.py")]
        )


def ver():

    archivos = sorted(os.listdir(RECETAS_DIR))

    if not archivos:
        print("\nNo hay recetas para visualizar.\n")
        return

    print("\nRECETAS DISPONIBLES\n")

    for i, archivo in enumerate(archivos, start=1):

        if "_" in archivo:
            nombre = archivo.split("_", 1)[1].replace(".txt", "")
        else:
            nombre = archivo.replace(".txt", "")

        if nombre == "":
            nombre = "(sin nombre)"

        print(f"{i} - {nombre}")

    opcion = input("\nNúmero de receta a visualizar (0 para  al Menú): ")

    if opcion == "0":
        return

    try:
        indice = int(opcion) - 1
        archivo = archivos[indice]
    except:
        print("Selección inválida.")
        return

    ruta = os.path.join(RECETAS_DIR, archivo)

    print("\n" + "-"*60)

    with open(ruta, "r", encoding="utf-8") as f:
        print(f.read())

    print("-"*60)

    input("\nPulsa ENTER para volver...")


def modificar():

    archivos = sorted(os.listdir(RECETAS_DIR))

    if not archivos:
        print("\nNo hay recetas para modificar.\n")
        return

    print("\nRECETAS DISPONIBLES\n")

    for i, archivo in enumerate(archivos, start=1):

        if "_" in archivo:
            nombre = archivo.split("_", 1)[1].replace(".txt", "")
        else:
            nombre = archivo.replace(".txt", "")

        if nombre == "":
            nombre = "(sin nombre)"

        print(f"{i} - {nombre}")

    opcion = input("\nNúmero de receta a modificar (0 para volver): ")
    if opcion == "0":
        return
    try:
        indice = int(opcion) - 1
        archivo = archivos[indice]
    except:
        print("Selección inválida.")
        return

    ruta = os.path.join(RECETAS_DIR, archivo)
    subprocess.run(["notepad.exe", ruta])
    input("\nPulsa ENTER para volver al menú...")


def borrar():

    archivos = sorted(os.listdir(RECETAS_DIR))

    if not archivos:
        print("\nNo hay recetas para borrar.\n")
        return

    print("\nRECETAS DISPONIBLES\n")

    for i, archivo in enumerate(archivos, start=1):

        if "_" in archivo:
            nombre = archivo.split("_", 1)[1].replace(".txt", "")
        else:
            nombre = archivo.replace(".txt", "")

        if nombre == "":
            nombre = "(sin nombre)"

        print(f"{i} - {nombre}")

    opcion = input("\nNúmero de receta a borrar (0 para volver): ")
    if opcion == "0":
        return

    try:
        indice = int(opcion) - 1
        archivo = archivos[indice]
    except:
        print("Selección inválida.")
        return

    confirmar = input(
        "¿Seguro que desea borrar esta receta? (S/N/0 cancelar): ")
    if confirmar == "0":
        return
    if confirmar.lower() == "s":
        os.remove(os.path.join(RECETAS_DIR, archivo))
        print("Receta eliminada.")

# ------------------------------------------------------------
# MENÚ PRINCIPAL
# ------------------------------------------------------------


def menu():

    while True:

        print("\nSISTEMA DE CAPTURA DE RECETAS\n")
        print("1 Capturar receta")
        print("2 Listar recetas")
        print("3 Ver receta")
        print("4 Modificar receta")
        print("5 Borrar receta")
        print("6 Salir")

        opcion = input("\nSeleccione una opción: ")

        if opcion == "1":
            capturar()

        elif opcion == "2":
            listar()

        elif opcion == "3":
            ver()

        elif opcion == "4":
            modificar()

        elif opcion == "5":
            borrar()

        elif opcion == "6":
            break
        else:
            print("Opción inválida")

# ------------------------------------------------------------
# EJECUCIÓN DEL SISTEMA
# ------------------------------------------------------------


if __name__ == "__main__":
    menu()

# ============================================================
# FIN DEL ARCHIVO
# ============================================================
