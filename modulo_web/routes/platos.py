import json
import os
from flask import Blueprint, request, jsonify

bp_platos = Blueprint("platos", __name__)

DATA_FILE = os.path.join("web_data", "plato.json")

TIPOS_VALIDOS = ["Principal", "Guarnición", "Postre"]


# ---------------------------
# Persistencia
# ---------------------------

def cargar_platos():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def guardar_platos(platos):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(platos, f, ensure_ascii=False, indent=2)


def next_id(platos):
    if not platos:
        return 1
    return max(p["id"] for p in platos) + 1


# ---------------------------
# Validaciones
# ---------------------------

def validar_plato(nombre, tipo, peso_racion, platos, exclude_id=None):
    errores = []

    nombre = nombre.strip()

    if not nombre:
        errores.append("El nombre del plato es obligatorio.")

    for p in platos:
        if exclude_id is not None and p["id"] == exclude_id:
            continue
        if p["nombre"].lower() == nombre.lower():
            errores.append(f"Nombre duplicado: '{nombre}'.")
            break

    if tipo not in TIPOS_VALIDOS:
        errores.append("Tipo de plato inválido.")

    try:
        peso = float(peso_racion)
        if peso <= 0:
            errores.append("El peso por ración debe ser mayor que cero.")
    except:
        errores.append("El peso por ración debe ser un número válido.")

    return errores


# ---------------------------
# Rutas
# ---------------------------

@bp_platos.route("/", methods=["GET"])
def listar_platos():
    platos = cargar_platos()
    return jsonify(platos)


@bp_platos.route("/create", methods=["POST"])
def crear_plato():
    data = request.json

    nombre = data.get("nombre", "")
    tipo = data.get("tipo", "")
    peso_racion = data.get("peso_racion", "")

    platos = cargar_platos()

    errores = validar_plato(nombre, tipo, peso_racion, platos)

    if errores:
        return jsonify({"ok": False, "errores": errores}), 400

    nuevo = {
        "id": next_id(platos),
        "nombre": nombre.strip(),
        "tipo": tipo,
        "peso_racion": float(peso_racion)
    }

    platos.append(nuevo)
    guardar_platos(platos)

    return jsonify({"ok": True, "plato": nuevo})


@bp_platos.route("/update/<int:plato_id>", methods=["POST"])
def actualizar_plato(plato_id):
    data = request.json

    nombre = data.get("nombre", "")
    tipo = data.get("tipo", "")
    peso_racion = data.get("peso_racion", "")

    platos = cargar_platos()

    plato = None
    for p in platos:
        if p["id"] == plato_id:
            plato = p
            break

    if plato is None:
        return jsonify({"ok": False, "error": "Plato no encontrado"}), 404

    errores = validar_plato(nombre, tipo, peso_racion, platos, exclude_id=plato_id)

    if errores:
        return jsonify({"ok": False, "errores": errores}), 400

    plato["nombre"] = nombre.strip()
    plato["tipo"] = tipo
    plato["peso_racion"] = float(peso_racion)

    guardar_platos(platos)

    return jsonify({"ok": True})


@bp_platos.route("/delete/<int:plato_id>", methods=["POST"])
def eliminar_plato(plato_id):
    platos = cargar_platos()

    nuevos = [p for p in platos if p["id"] != plato_id]

    if len(nuevos) == len(platos):
        return jsonify({"ok": False, "error": "Plato no encontrado"}), 404

    guardar_platos(nuevos)

    return jsonify({"ok": True})