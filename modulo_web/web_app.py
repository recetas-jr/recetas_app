# modulo_web/web_app.py

from flask import Flask, render_template, request, redirect, flash

from modulo_web.persistencia_db import (
    db_cargar_platos,
    db_cargar_unidades,
    db_cargar_ingredientes,
    db_cargar_recetas_maestro_listado,
    db_cargar_tipos_plato,
    get_connection
)

app = Flask(__name__)
app.secret_key = "recetas_app_clave_segura_temporal"

# ==================================================
# UTILIDAD — INGREDIENTES CON UNIDAD
# ==================================================

def cargar_ingredientes_con_unidad():
    ingredientes = db_cargar_ingredientes()
    unidades = db_cargar_unidades()

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
    recetas = db_cargar_recetas_maestro_listado()
    return render_template("index.html", recetas=recetas)

# ==================================================
# ADMIN TIPOS DE PLATO
# ==================================================

@app.route("/admin/tipos_plato", methods=["GET", "POST"])
def admin_tipos_plato():
    conn = get_connection()
    cur = conn.cursor()

    errores = []

    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip().lower()

        if not nombre:
            errores.append("Debe teclear el nombre del tipo de plato.")

        cur.execute("SELECT id FROM tipos_plato WHERE lower(nombre) = lower(?)", (nombre,))
        if cur.fetchone():
            errores.append(f"El tipo de plato '{nombre}' ya existe.")

        if errores:
            cur.execute("SELECT id, nombre FROM tipos_plato ORDER BY nombre")
            tipos = cur.fetchall()
            conn.close()
            for e in errores:
                flash(e, "error")
            return render_template("admin_tipos_plato.html", tipos=tipos, errores=[])

        try:
            cur.execute("INSERT INTO tipos_plato (nombre) VALUES (?)", (nombre,))
            conn.commit()
            flash("Tipo de plato guardado correctamente.", "ok")
        except Exception as e:
            print("ERROR guardando tipo de plato:", e)
            flash("Error al guardar tipo de plato.", "error")

        conn.close()
        return redirect("/admin/tipos_plato")

    cur.execute("SELECT id, nombre FROM tipos_plato ORDER BY nombre")
    tipos = cur.fetchall()
    conn.close()
    return render_template("admin_tipos_plato.html", tipos=tipos, errores=[])

@app.route("/admin/tipos_plato/borrar/<int:tipo_id>", methods=["POST"])
def borrar_tipo_plato(tipo_id):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT nombre FROM tipos_plato WHERE id = ?", (tipo_id,))
        fila = cur.fetchone()
        if not fila:
            conn.close()
            flash("El tipo de plato no existe.", "error")
            return redirect("/admin/tipos_plato")

        nombre = fila["nombre"]

        cur.execute("SELECT COUNT(*) AS total FROM platos WHERE tipo_plato_id = ?", (tipo_id,))
        total = cur.fetchone()["total"]
        if total > 0:
            conn.close()
            flash(f"<span class='item'>{nombre}</span> está en uso en Pla.", "error")
            return redirect("/admin/tipos_plato")

        cur.execute("DELETE FROM tipos_plato WHERE id = ?", (tipo_id,))
        conn.commit()
        conn.close()

        flash(f"<span class='item'>{nombre}</span> borrado de T.P. correctamente.", "ok")

    except Exception as e:
        print("ERROR borrando tipo de plato:", e)
        flash("No se pudo borrar el tipo de plato.", "error")

    return redirect("/admin/tipos_plato")

# ==================================================
# ADMIN PLATOS
# ==================================================

@app.route("/admin/platos", methods=["GET", "POST"])
def admin_platos():
    platos = db_cargar_platos()
    tipos_plato = db_cargar_tipos_plato()

    errores = []

    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip().lower()
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
            elif peso_racion > 1000:
                errores.append("Peso por ración no puede ser mayor que 1000.0.")
        except:
            errores.append("Peso por ración debe ser numérico.")

        if errores:
            platos = sorted(platos, key=lambda p: p["nombre"].lower())
            for e in errores:
                flash(e, "error")
            return render_template("admin_platos.html", platos=platos, tipos_plato=tipos_plato, errores=[])

        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO platos (nombre, tipo_plato_id, activo, peso_racion) VALUES (?, ?, 1, ?)",
                (nombre, int(tipo_plato), peso_racion)
            )
            conn.commit()
            conn.close()
            flash(f"Plato '{nombre}' guardado correctamente.", "ok")
            return redirect("/admin/platos")
        except Exception as e:
            print("ERROR guardando plato:", e)
            flash("Error al guardar plato.", "error")

    platos = sorted(platos, key=lambda p: p["nombre"].lower())
    return render_template("admin_platos.html", platos=platos, tipos_plato=tipos_plato, errores=[])

@app.route("/admin/platos/borrar/<int:plato_id>", methods=["POST"])
def borrar_plato(plato_id):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT nombre FROM platos WHERE id = ?", (plato_id,))
        fila = cur.fetchone()
        if not fila:
            conn.close()
            flash("El plato no existe.", "error")
            return redirect("/admin/platos")

        nombre_plato = fila["nombre"]

        cur.execute("SELECT COUNT(*) as total FROM recetas_maestro WHERE plato_id = ?", (plato_id,))
        total = cur.fetchone()["total"]
        if total > 0:
            conn.close()
            flash(f"<span class='item'>{nombre_plato}</span> está en uso en M.R.", "error")
            return redirect("/admin/platos")

        cur.execute("DELETE FROM platos WHERE id = ?", (plato_id,))
        conn.commit()
        conn.close()
        flash(f"<span class='item'>{nombre_plato}</span> borrado de Pla. correctamente.", "ok")

    except Exception as e:
        print("ERROR borrando plato:", e)
        flash("No se pudo borrar el plato.", "error")

    return redirect("/admin/platos")

# ==================================================
# ADMIN UNIDADES
# ==================================================

@app.route("/admin/unidades", methods=["GET", "POST"])
def admin_unidades():
    unidades = db_cargar_unidades()
    errores = []

    if request.method == "POST":
        codigo = request.form.get("codigo", "").strip().upper()
        nombre = request.form.get("nombre", "").strip().lower()

        if not codigo:
            errores.append("Debe teclear el código.")
        elif not codigo.isalpha() or len(codigo) not in (1, 2):
            errores.append("El código debe tener 1 o 2 letras.")

        if not nombre:
            errores.append("Debe teclear el nombre.")

        for u in unidades:
            if u["codigo"].upper() == codigo:
                errores.append(f"Código '{codigo}' ya existe.")
            if u["nombre"].lower() == nombre:
                errores.append(f"Nombre '{nombre}' ya existe.")

        if errores:
            for e in errores:
                flash(e, "error")
            return render_template("admin_unidades.html", unidades=unidades, errores=[])

        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("INSERT INTO unidades (codigo, nombre) VALUES (?, ?)", (codigo, nombre))
            conn.commit()
            conn.close()
            flash("Unidad guardada correctamente.", "ok")
            return redirect("/admin/unidades")
        except Exception as e:
            print("ERROR guardando unidad:", e)
            flash("Error al guardar unidad.", "error")

    return render_template("admin_unidades.html", unidades=unidades, errores=[])

@app.route("/admin/unidades/borrar/<int:unidad_id>", methods=["POST"])
def borrar_unidad(unidad_id):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT codigo, nombre FROM unidades WHERE id = ?", (unidad_id,))
        fila = cur.fetchone()
        if not fila:
            conn.close()
            flash("La unidad no existe.", "error")
            return redirect("/admin/unidades")

        nombre_unidad = f"{fila['codigo']} - {fila['nombre']}"

        cur.execute("SELECT COUNT(*) as total FROM ingredientes WHERE unidad_id = ?", (unidad_id,))
        total = cur.fetchone()["total"]
        if total > 0:
            conn.close()
            flash(f"<span class='item'>{nombre_unidad}</span> está en uso en Ing.", "error")
            return redirect("/admin/unidades")

        cur.execute("DELETE FROM unidades WHERE id = ?", (unidad_id,))
        conn.commit()
        conn.close()
        flash(f"<span class='item'>{nombre_unidad}</span> borrado de UM correctamente.", "ok")

    except Exception as e:
        print("ERROR borrando unidad:", e)
        flash("No se pudo borrar la unidad.", "error")

    return redirect("/admin/unidades")

# ==================================================
# ADMIN INGREDIENTES
# ==================================================

@app.route("/admin/ingredientes", methods=["GET", "POST"])
def admin_ingredientes():
    ingredientes = cargar_ingredientes_con_unidad()
    ingredientes = sorted(ingredientes, key=lambda i: i["nombre"].lower())
    unidades = db_cargar_unidades()
    unidades = sorted(unidades, key=lambda u: u["nombre"].lower())

    errores = []

    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip().lower()
        unidad_id = request.form.get("unidad_id", "").strip()

        if not nombre:
            errores.append("Debe teclear el nombre del ingrediente.")
        if not unidad_id:
            errores.append("Debe seleccionar una unidad de medida.")

        for i in ingredientes:
            if i["nombre"].lower() == nombre:
                errores.append("Ingrediente duplicado.")

        if errores:
            for e in errores:
                flash(e, "error")
            return render_template("admin_ingredientes.html", ingredientes=ingredientes, unidades=unidades, errores=[])

        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("INSERT INTO ingredientes (nombre, unidad_id, activo) VALUES (?, ?, 1)", (nombre, int(unidad_id)))
            conn.commit()
            conn.close()
            flash("Ingrediente guardado correctamente.", "ok")
            return redirect("/admin/ingredientes")
        except Exception as e:
            print("ERROR guardando ingrediente:", e)
            flash("Error al guardar ingrediente.", "error")

    return render_template("admin_ingredientes.html", ingredientes=ingredientes, unidades=unidades, errores=[])

@app.route("/admin/ingredientes/borrar/<int:ingrediente_id>", methods=["POST"])
def borrar_ingrediente(ingrediente_id):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT nombre FROM ingredientes WHERE id = ?", (ingrediente_id,))
        fila = cur.fetchone()
        if not fila:
            conn.close()
            flash("El ingrediente no existe.", "error")
            return redirect("/admin/ingredientes")

        nombre_ing = fila["nombre"]

        cur.execute("SELECT COUNT(*) as total FROM recetas_ingredientes WHERE ingrediente_id = ?", (ingrediente_id,))
        total = cur.fetchone()["total"]
        if total > 0:
            conn.close()
            flash(f"<span class='item'>{nombre_ing}</span> está en uso en M.R.", "error")
            return redirect("/admin/ingredientes")

        cur.execute("DELETE FROM ingredientes WHERE id = ?", (ingrediente_id,))
        conn.commit()
        conn.close()
        flash(f"<span class='item'>{nombre_ing}</span> borrado de Ing. correctamente.", "ok")

    except Exception as e:
        print("ERROR borrando ingrediente:", e)
        flash("No se pudo borrar el ingrediente.", "error")

    return redirect("/admin/ingredientes")

# ==================================================
# ADMIN RECETAS — LISTADO
# ==================================================

@app.route("/admin/recetas/listado", methods=["GET"])
def admin_recetas_listado():
    recetas_listado = db_cargar_recetas_maestro_listado()
    return render_template("admin_recetas_listado.html", recetas=recetas_listado)

# ==================================================
# BORRAR RECETA (CASCADE MANUAL)
# ==================================================

@app.route("/admin/recetas/borrar/<int:receta_id>", methods=["POST"])
def borrar_receta(receta_id):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT p.nombre AS plato_nombre
            FROM recetas_maestro r
            JOIN platos p ON p.id = r.plato_id
            WHERE r.id = ?
        """, (receta_id,))
        fila = cur.fetchone()
        nombre_plato = fila["plato_nombre"] if fila else "receta"

        cur.execute("DELETE FROM recetas_ingredientes WHERE receta_id = ?", (receta_id,))
        cur.execute("DELETE FROM recetas_detalle WHERE receta_id = ?", (receta_id,))
        cur.execute("DELETE FROM recetas_maestro WHERE id = ?", (receta_id,))

        conn.commit()
        conn.close()
        flash(f"<span class='item'>{nombre_plato}</span> borrado del M.R.", "ok")

    except Exception as e:
        print("ERROR borrando receta:", e)
        flash("No se pudo borrar la receta.", "error")

    return redirect("/admin/recetas/listado")

# ==================================================
# EJECUCIÓN
# ==================================================

if __name__ == "__main__":
    app.run(debug=True)