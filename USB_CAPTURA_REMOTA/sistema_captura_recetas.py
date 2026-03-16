# ============================================================
# RUTA: C:\Users\jrmon\Documents\recetas_app\USB_CAPTURA_REMOTA
# ARCHIVO: sistema_captura_recetas.py
# SISTEMA: captura remota de recetas
# ============================================================

import os
import sys
import subprocess


# ------------------------------------------------------------
# CONFIGURACIÓN BASE PORTABLE
# ------------------------------------------------------------

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

RECETAS_DIR = os.path.join(BASE_DIR, "RECETAS")


# ------------------------------------------------------------
# FUNCIONES DEL SISTEMA
# ------------------------------------------------------------

def capturar():
    subprocess.run([os.path.join(BASE_DIR, "capturar_receta.exe")])


def listar():
    subprocess.run([os.path.join(BASE_DIR, "listar_recetas.exe")])


def modificar():

    archivos = sorted(os.listdir(RECETAS_DIR))

    if not archivos:
        print("\nNo hay recetas para modificar.\n")
        return

    print("\nRECETAS DISPONIBLES\n")

    for i, archivo in enumerate(archivos, start=1):
        nombre = archivo.split("_",1)[1].replace(".txt","")
        print(f"{i} - {nombre}")

    opcion = input("\nNúmero de receta a modificar: ")

    try:
        indice = int(opcion) - 1
        archivo = archivos[indice]
    except:
        print("Selección inválida.")
        return

    ruta = os.path.join(RECETAS_DIR, archivo)

    subprocess.run(["notepad.exe", ruta])


# ------------------------------------------------------------
# MENÚ PRINCIPAL
# ------------------------------------------------------------

def menu():

    while True:

        print("\nSISTEMA DE CAPTURA DE RECETAS\n")

        print("1 Capturar receta")
        print("2 Listar recetas")
        print("3 Modificar receta")
        print("4 Salir")

        opcion = input("\nSeleccione una opción: ")

        if opcion == "1":
            capturar()

        elif opcion == "2":
            listar()

        elif opcion == "3":
            modificar()

        elif opcion == "4":
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
# RUTA: C:\Users\jrmon\Documents\recetas_app\USB_CAPTURA_REMOTA
# ARCHIVO: sistema_captura_recetas.py
# ============================================================