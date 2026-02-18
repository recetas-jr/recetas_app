from flask import Flask, render_template, request, redirect, flash
import json
import os

# --------------------------------------------------
# CAPA DE PERSISTENCIA (JSON) — Fallbacks legacy
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
    RECETAS_MAESTRO_FILE,
    RECETAS_ING_FILE,
    RECETAS_DETALLE_FILE,
)

# --------------------------------------------------
# CAPA DB (SQLite)
# --------------------------------------------------

from modulo_web.persistencia_db import (
    db_cargar_platos,
    db_cargar_unidades,
    db_cargar_ingredientes,
    db_cargar_recetas_maestro_listado,
    get_connection
)

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
# ADMIN TIPOS DE PLATO (SQLite)
# ==================================================

@app.route("/admin/tipos_plato", methods=["GET", "POST"])
def admin_tipos_plato():

    conn = get_connection()
    cur = conn.cursor()

    errores = []

    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()

        if not nombre:
            errores.append("Debe teclear el nombre del tipo de plato.")

        # Verificar duplicado
        cur.execute("SELECT id FROM tipos_plato WHERE lower(nombre) = lower(?)", (nombre,))
        if cur.fetchone():
            errores.append(f"El tipo de plato '{nombre}' ya existe.")

        if errores:
            cur.execute("SELECT id, nombre FROM tipos_plato ORDER BY nombre")
            tipos = cur.fetchall()
            conn.close()
            return render_template("admin_tipos_plato.html", tipos=tipos, errores=errores)

        try:
            cur.execute("INSERT INTO tipos_plato (nombre) VALUES (?)", (nombre,))
            conn.commit()
            flash("Tipo de plato guardado en SQLite.", "ok")
        except Exception as e:
            print("ERROR guardando tipo de plato:", e)
            flash("Error al guardar tipo de plato.", "error")

        conn.close()
        return redirect("/admin/tipos_plato")

    # GET
    cur.execute("SELECT id, nombre FROM tipos_plato ORDER BY nombre")
    tipos = cur.fetchall()
    conn.close()

    return render_template("admin_tipos_plato.html", tipos=tipos, errores=[])

@app.route("/admin/tipos_plato/borrar/<int:tipo_id>", methods=["POST"])
def borrar_tipo_plato(tipo_id):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM tipos_plato WHERE id = ?", (tipo_id,))
        conn.commit()
        conn.close()
        flash("Tipo de plato borrado correctamente.", "ok")
    except Exception as e:
        print("ERROR borrando tipo de plato:", e)
        flash("Error al borrar tipo de plato.", "error")

    return redirect("/admin/tipos_plato")

# ==================================================
# ADMIN PLATOS
# ==================================================

@app.route("/admin/platos", methods=["GET", "POST"])
def admin_platos():

    try:
        platos = db_cargar_platos()
    except:
        platos = cargar_platos()

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
            return render_template("admin_platos.html", platos=platos, errores=errores)

        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO platos (nombre, tipo_plato_id, activo, peso_racion) VALUES (?, NULL, 1, ?)",
                (nombre, peso_racion)
            )
            conn.commit()
            conn.close()
            flash("Plato guardado en SQLite.", "ok")
            return redirect("/admin/platos")
        except Exception as e:
            print("ERROR guardando plato en DB, usando JSON fallback:", e)

        nuevo_id = max([p["id"] for p in platos], default=0) + 1

        platos.append({
            "id": nuevo_id,
            "nombre": nombre,
            "tipo_plato": tipo_plato,
            "peso_racion": peso_racion,
            "foto": ""
        })

        guardar_platos(platos)
        flash("Plato guardado en JSON (fallback).", "ok")
        return redirect("/admin/platos")

    platos = sorted(platos, key=lambda p: p["nombre"].lower())
    return render_template("admin_platos.html", platos=platos, errores=[])

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

        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO unidades (codigo, nombre) VALUES (?, ?)",
                (codigo, nombre)
            )
            conn.commit()
            conn.close()
            flash("Unidad guardada en SQLite.", "ok")
            return redirect("/admin/unidades")
        except Exception as e:
            print("ERROR guardando unidad en DB, usando JSON fallback:", e)

        nuevo_id = max([u["id"] for u in unidades], default=0) + 1

        unidades.append({
            "id": nuevo_id,
            "codigo": codigo,
            "nombre": nombre
        })

        guardar_unidades(unidades)
        flash("Unidad guardada en JSON (fallback).", "ok")
        return redirect("/admin/unidades")

    return render_template("admin_unidades.html", unidades=unidades, errores=[])

# ==================================================
# ADMIN INGREDIENTES
# ==================================================

@app.route("/admin/ingredientes", methods=["GET", "POST"])
def admin_ingredientes():

    ingredientes = cargar_ingredientes_con_unidad()
    ingredientes = sorted(ingredientes, key=lambda i: i["nombre"].lower())

    try:
        unidades = db_cargar_unidades()
    except:
        unidades = cargar_unidades()

    unidades = sorted(unidades, key=lambda u: u["nombre"].lower())

    errores = []

    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        unidad_id = request.form.get("unidad_id", "").strip()

        if not nombre:
            errores.append("Debe teclear el nombre del ingrediente.")
        if not unidad_id:
            errores.append("Debe seleccionar una unidad de medida.")

        for i in ingredientes:
            if i["nombre"].lower() == nombre.lower():
                errores.append("Ingrediente duplicado.")

        if errores:
            return render_template(
                "admin_ingredientes.html",
                ingredientes=ingredientes,
                unidades=unidades,
                errores=errores
            )

        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO ingredientes (nombre, unidad_id, activo) VALUES (?, ?, 1)",
                (nombre, int(unidad_id))
            )
            conn.commit()
            conn.close()
            flash("Ingrediente guardado en SQLite.", "ok")
            return redirect("/admin/ingredientes")
        except Exception as e:
            print("ERROR guardando ingrediente en DB, usando JSON fallback:", e)

        data = cargar_ingredientes()
        nuevo_id = max([i["id"] for i in data], default=0) + 1
        data.append({
            "id": nuevo_id,
            "nombre": nombre,
            "unidad_id": int(unidad_id),
            "activo": True
        })
        guardar_ingredientes(data)
        flash("Ingrediente guardado en JSON (fallback).", "ok")
        return redirect("/admin/ingredientes")

    return render_template(
        "admin_ingredientes.html",
        ingredientes=ingredientes,
        unidades=unidades,
        errores=[]
    )

# ==================================================
# ADMIN RECETAS — CAPTURA
# ==================================================

@app.route("/admin/recetas", methods=["GET", "POST"])
def admin_recetas():

    try:
        platos = db_cargar_platos()
    except:
        platos = cargar_platos()

    ingredientes = cargar_ingredientes_con_unidad()

    error = None

    if request.method == "POST":

        plato_id = request.form.get("plato_id", "").strip()
        raciones_base = request.form.get("raciones_base", "").strip()
        ingredientes_json = request.form.get("ingredientes_json", "").strip()

        preparacion = request.form.get("preparacion", "").strip()
        elaboracion = request.form.get("elaboracion", "").strip()
        presentacion = request.form.get("presentacion", "").strip()
        nutricion = request.form.get("nutricion", "").strip()

        if not plato_id:
            error = "Debe seleccionar un plato."
        elif not raciones_base.isdigit() or int(raciones_base) <= 0:
            error = "Raciones base inválidas."
        elif not ingredientes_json:
            error = "Debe agregar al menos un ingrediente."

        if error:
            return render_template(
                "admin_recetas.html",
                platos=platos,
                ingredientes=ingredientes,
                error=error,
                limpiar_form=False
            )

        lista_ing = json.loads(ingredientes_json)

        try:
            conn = get_connection()
            cur = conn.cursor()

            cur.execute(
                "INSERT INTO recetas_maestro (plato_id, raciones_base, activo) VALUES (?, ?, 1)",
                (int(plato_id), int(raciones_base))
            )
            receta_id = cur.lastrowid

            for it in lista_ing:
                cur.execute(
                    "INSERT INTO recetas_ingredientes (receta_id, ingrediente_id, cantidad, rol) VALUES (?, ?, ?, ?)",
                    (receta_id, it["ingrediente_id"], it["cantidad"], "principal")
                )

            cur.execute(
                "INSERT INTO recetas_detalle (receta_id, preparacion, elaboracion, presentacion, nutricion) VALUES (?, ?, ?, ?, ?)",
                (receta_id, preparacion, elaboracion, presentacion, nutricion)
            )

            conn.commit()
            conn.close()

            flash("Receta guardada en SQLite (con detalle).", "ok")
            return redirect("/admin/recetas/listado")

        except Exception as e:
            print("ERROR guardando receta en DB, usando JSON fallback:", e)

        flash("Error al guardar receta.", "error")
        return redirect("/admin/recetas")

    return render_template(
        "admin_recetas.html",
        platos=platos,
        ingredientes=ingredientes,
        error=None,
        limpiar_form=False
    )

# ==================================================
# ADMIN RECETAS — LISTADO
# ==================================================

@app.route("/admin/recetas/listado", methods=["GET"])
def admin_recetas_listado():

    try:
        recetas_listado = db_cargar_recetas_maestro_listado()
    except:
        recetas = cargar_recetas_maestro()
        recetas_listado = recetas

    return render_template(
        "admin_recetas_listado.html",
        recetas=recetas_listado
    )

# ==================================================
# BORRAR RECETA MASTER
# ==================================================

@app.route("/admin/recetas/borrar/<int:receta_id>", methods=["POST"])
def borrar_receta_master(receta_id):

    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM recetas_ingredientes WHERE receta_id = ?", (receta_id,))
        cur.execute("DELETE FROM recetas_detalle WHERE receta_id = ?", (receta_id,))
        cur.execute("DELETE FROM recetas_maestro WHERE id = ?", (receta_id,))
        conn.commit()
        conn.close()
        flash("Receta borrada correctamente (DB).", "ok")
        return redirect("/admin/recetas/listado")
    except Exception as e:
        print("ERROR borrando en DB:", e)
        flash("Error al borrar receta.", "error")

    return redirect("/admin/recetas/listado")

# ==================================================
# EJECUCIÓN
# ==================================================

if __name__ == "__main__":
    app.run(debug=True)