from flask import Flask, render_template, request, redirect, flash

# --------------------------------------------------
# CAPA DE PERSISTENCIA (JSON)
# --------------------------------------------------

from persistencia import (
    cargar_datos,
    guardar_datos,

    cargar_platos,
    guardar_platos,

    cargar_ingredientes,
    guardar_ingredientes,

    cargar_unidades,
    guardar_unidades,

    cargar_recetas_maestro,
    RECETAS_MAESTRO_FILE
)

# --------------------------------------------------
# CAPA DB (SQLite) — LECTURA
# --------------------------------------------------

from modulo_web.persistencia_db import (
    db_cargar_platos,
    db_cargar_unidades,
    db_cargar_ingredientes,
    db_cargar_recetas_maestro_listado,
    get_connection
)

# --------------------------------------------------
# Tipos de platos (JSON)
# --------------------------------------------------

import os

DATA_DIR = "data"
TIPOS_PLATOS_FILE = os.path.join(DATA_DIR, "tipos_platos.json")

def cargar_tipos_platos():
    return cargar_datos(TIPOS_PLATOS_FILE, [])

def guardar_tipos_platos(tipos):
    guardar_datos(TIPOS_PLATOS_FILE, tipos)

app = Flask(__name__)
app.secret_key = "recetas_app_clave_segura_temporal"

# ==================================================
# UTILIDAD — INGREDIENTES CON UNIDAD
# ==================================================

def cargar_ingredientes_con_unidad():
    try:
        ingredientes = db_cargar_ingredientes()
        unidades = db_cargar_unidades()
    except:
        ingredientes = cargar_ingredientes()
        unidades = cargar_unidades()

    mapa_unidades = {u["id"]: u for u in unidades}

    resultado = []
    for ing in ingredientes:
        u = mapa_unidades.get(ing["unidad_id"])
        resultado.append({
            "id": ing["id"],
            "nombre": ing["nombre"],
            "unidad_id": ing["unidad_id"],
            "unidad_codigo": u["codigo"] if u else "",
            "unidad_nombre": u["nombre"] if u else ""
        })

    return resultado


# ==================================================
# INDEX
# ==================================================

@app.route("/", methods=["GET"])
def index():
    try:
        recetas = db_cargar_recetas_maestro_listado()
    except:
        recetas = cargar_recetas_maestro()
    return render_template("index.html", recetas=recetas)


# ==================================================
# ADMIN PLATOS
# ==================================================

@app.route("/admin/platos", methods=["GET", "POST"])
def admin_platos():

    try:
        platos = db_cargar_platos()
    except:
        platos = cargar_platos()

    tipos_platos = cargar_tipos_platos()
    tipos_platos = sorted(tipos_platos, key=lambda t: t["nombre"].lower())

    errores = []

    if request.method == "POST":

        nombre = request.form.get("nombre", "").strip()
        tipo_plato = request.form.get("tipo_plato", "").strip()
        peso_txt = request.form.get("peso_racion", "").replace(",", ".")

        if not nombre:
            errores.append("Nombre del plato es obligatorio.")
        if not tipo_plato:
            errores.append("Tipo de plato es obligatorio.")

        try:
            peso_racion = float(peso_txt)
            if peso_racion <= 0:
                errores.append("Peso por ración debe ser mayor que 0.")
        except:
            errores.append("Peso por ración debe ser numérico.")

        for p in platos:
            if (
                p["nombre"].lower() == nombre.lower()
                and p.get("tipo_plato","").lower() == tipo_plato.lower()
            ):
                errores.append("Plato duplicado (nombre + tipo).")

        if errores:
            platos = sorted(platos, key=lambda p: p["nombre"].lower())
            return render_template("admin_platos.html", platos=platos, errores=errores, tipos_platos=tipos_platos)

        nuevo_id = max([p["id"] for p in platos], default=0) + 1

        platos.append({
            "id": nuevo_id,
            "nombre": nombre,
            "tipo_plato": tipo_plato,
            "peso_racion": peso_racion,
            "foto": ""
        })

        guardar_platos(platos)
        return redirect("/admin/platos")

    platos = sorted(platos, key=lambda p: p["nombre"].lower())
    return render_template("admin_platos.html", platos=platos, errores=[], tipos_platos=tipos_platos)


# ==================================================
# ADMIN UNIDADES
# ==================================================

@app.route("/admin/unidades", methods=["GET", "POST"])
def admin_unidades():

    try:
        unidades = db_cargar_unidades()
    except:
        unidades = cargar_unidades()

    errores = []

    if request.method == "POST":

        codigo = request.form.get("codigo", "").strip().upper()
        nombre = request.form.get("nombre", "").strip()

        if not codigo:
            errores.append("Debe teclear el código.")
        elif not codigo.isalpha() or len(codigo) not in (1, 2):
            errores.append("El código debe tener 1 o 2 letras.")

        if not nombre:
            errores.append("Debe teclear el nombre.")

        for u in unidades:
            if u["codigo"].upper() == codigo:
                errores.append(f"Código '{codigo}' ya existe.")
            if u["nombre"].upper() == nombre.upper():
                errores.append(f"Nombre '{nombre}' ya existe.")

        if errores:
            return render_template("admin_unidades.html", unidades=unidades, errores=errores)

        nuevo_id = max([u["id"] for u in unidades], default=0) + 1

        unidades.append({
            "id": nuevo_id,
            "codigo": codigo,
            "nombre": nombre
        })

        guardar_unidades(unidades)
        return redirect("/admin/unidades")

    return render_template("admin_unidades.html", unidades=unidades, errores=[])


# ==================================================
# ADMIN INGREDIENTES
# ==================================================

@app.route("/admin/ingredientes", methods=["GET"])
def admin_ingredientes():

    ingredientes = cargar_ingredientes_con_unidad()
    ingredientes = sorted(ingredientes, key=lambda i: i["nombre"].lower())

    try:
        unidades = db_cargar_unidades()
    except:
        unidades = cargar_unidades()

    unidades = sorted(unidades, key=lambda u: u["nombre"].lower())

    return render_template(
        "admin_ingredientes.html",
        ingredientes=ingredientes,
        unidades=unidades
    )


# ==================================================
# ADMIN RECETAS — LISTADO (DESDE DB)
# ==================================================

@app.route("/admin/recetas/listado", methods=["GET"])
def admin_recetas_listado():

    try:
        recetas_listado = db_cargar_recetas_maestro_listado()
    except:
        platos = sorted(cargar_platos(), key=lambda p: p["nombre"].lower())
        recetas = cargar_recetas_maestro()

        mapa_platos = {p["id"]: p["nombre"] for p in platos}

        recetas_listado = []
        for r in recetas:
            recetas_listado.append({
                "id": r["id"],
                "plato_id": r["plato_id"],
                "plato_nombre": mapa_platos.get(r["plato_id"], "—"),
                "raciones_base": r.get("raciones_base", 0),
                "cantidad_ingredientes": len(r.get("ingredientes", []))
            })

        recetas_listado = sorted(recetas_listado, key=lambda r: r["plato_nombre"].lower())

    return render_template(
        "admin_recetas_listado.html",
        recetas=recetas_listado
    )


# ==================================================
# BORRAR RECETA MASTER (DB + FALLBACK JSON)
# ==================================================

@app.route("/admin/recetas/borrar/<int:receta_id>", methods=["POST"])
def borrar_receta_master(receta_id):

    # --- Intentar borrar en SQLite ---
    try:
        conn = get_connection()
        cur = conn.cursor()

        # Primero borrar ingredientes de la receta
        cur.execute("DELETE FROM recetas_ingredientes WHERE receta_id = ?", (receta_id,))

        # Luego borrar la receta
        cur.execute("DELETE FROM recetas_maestro WHERE id = ?", (receta_id,))

        conn.commit()
        conn.close()

        flash("Receta borrada correctamente (DB).", "ok")
        return redirect("/admin/recetas/listado")

    except Exception as e:
        print("ERROR borrando en DB, usando fallback JSON:", e)

    # --- Fallback: borrar en JSON ---
    recetas = cargar_recetas_maestro()
    recetas = [r for r in recetas if r["id"] != receta_id]
    guardar_datos(RECETAS_MAESTRO_FILE, recetas)

    flash("Receta borrada correctamente (JSON fallback).", "ok")
    return redirect("/admin/recetas/listado")


# ==================================================
# EJECUCIÓN
# ==================================================

if __name__ == "__main__":
    app.run(debug=True)