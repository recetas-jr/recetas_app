# ------------------------------------------------------------
# ARCHIVO: USB_CAPTURA_REMOTA/capturar_receta.py
# PROPOSITO:
# Permitir capturar recetas en la "lejanía".
# Guarda la receta dentro de la carpeta RECETAS del mismo lugar
# donde se ejecuta el .exe (modo portable).
# ------------------------------------------------------------

import os
import sys

# ------------------------------------------------------------
# CONFIGURACIÓN PORTABLE (CORRECTA)
# ------------------------------------------------------------

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

RECETAS_DIR = os.path.join(BASE_DIR, "RECETAS")

# asegurar que exista la carpeta
os.makedirs(RECETAS_DIR, exist_ok=True)

# ------------------------------------------------------------
# CAPTURA DE DATOS
# ------------------------------------------------------------

nombre = input("Nombre de la receta: ")
raciones = input("Raciones: ")

print("\nIntroduce los ingredientes (formato: ingrediente | cantidad | unidad)")
print("Pulsa ENTER vacío para terminar")

ingredientes = []

while True:
    linea = input("> ")
    if linea.strip() == "":
        break
    ingredientes.append(linea)

print("\nPREPARACION (una línea por paso, ENTER vacío para terminar)")
preparacion = []

while True:
    linea = input("> ")
    if linea.strip() == "":
        break
    preparacion.append(linea)

print("\nELABORACION (una línea por paso, ENTER vacío para terminar)")
elaboracion = []

while True:
    linea = input("> ")
    if linea.strip() == "":
        break
    elaboracion.append(linea)

print("\nPRESENTACION (una línea por paso, ENTER vacío para terminar)")
presentacion = []

while True:
    linea = input("> ")
    if linea.strip() == "":
        break
    presentacion.append(linea)

# ------------------------------------------------------------
# GENERAR ARCHIVO
# ------------------------------------------------------------

archivos = os.listdir(RECETAS_DIR)

numeros = []

for archivo in archivos:
    if "_" in archivo:
        try:
            num = int(archivo.split("_")[0])
            numeros.append(num)
        except:
            pass

if numeros:
    numero = max(numeros) + 1
else:
    numero = 1
    
archivo_nombre = f"{numero:03d}_{nombre.replace(' ', '_')}.txt"
ruta = os.path.join(RECETAS_DIR, archivo_nombre)

with open(ruta, "w", encoding="utf-8") as f:

    f.write("RECETA\n")
    f.write(f"nombre: {nombre}\n")
    f.write(f"raciones: {raciones}\n\n")

    f.write("INGREDIENTES\n")
    for i in ingredientes:
        f.write(i + "\n")

    f.write("\nPREPARACION\n")
    for p in preparacion:
        f.write(p + "\n")

    f.write("\nELABORACION\n")
    for e in elaboracion:
        f.write(e + "\n")

    f.write("\nPRESENTACION\n")
    for p in presentacion:
        f.write(p + "\n")

print("\nReceta guardada correctamente.")
print("Archivo:", archivo_nombre)