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
# ADMIN RECETAS — LISTADO
# ==================================================

@app.route("/admin/recetas/listado", methods=["GET"])
def admin_recetas_listado():
    recetas_listado = db_cargar_recetas_maestro_listado()
    return render_template("admin_recetas_listado.html", recetas=recetas_listado)

# ==================================================
# NUEVA RECETA (MASTER)
# ==================================================

@app.route("/admin/recetas/nueva", methods=["GET", "POST"])
def admin_recetas_nueva():
    platos = db_cargar_platos()
    ingredientes = cargar_ingredientes_con_unidad()

    if request.method == "POST":
        plato_id = request.form.get("plato_id", "").strip()
        raciones_base = request.form.get("raciones_base", "").strip()

        if not plato_id:
            flash("Debe seleccionar un plato.", "error")
            return render_template("admin_recetas_nueva.html", platos=platos, ingredientes=ingredientes)

        try:
            raciones_base_int = int(raciones_base)
            if raciones_base_int <= 0:
                flash("Raciones base debe ser mayor que 0.", "error")
                return render_template("admin_recetas_nueva.html", platos=platos, ingredientes=ingredientes)
        except:
            flash("Raciones base debe ser numérico.", "error")
            return render_template("admin_recetas_nueva.html", platos=platos, ingredientes=ingredientes)

        ingredientes_ids = request.form.getlist("ingrediente_id[]")
        cantidades = request.form.getlist("cantidad[]")
        roles = request.form.getlist("rol[]")

        filas_validas = []

        for i in range(len(ingredientes_ids)):
            ing_id = ingredientes_ids[i].strip()
            cant = cantidades[i].strip()
            rol = roles[i].strip()

            if not ing_id:
                continue

            try:
                cant_f = float(cant)
            except:
                continue

            try:
                rol_f = float(rol) if rol else 0.0
            except:
                rol_f = 0.0

            # -----------------------------
            # 🔒 VALIDACIONES IMPORTANTES
            # -----------------------------

            if cant_f <= 0:
                continue

            # ❌ ROL no puede ser mayor que CANTIDAD
            if rol_f > cant_f:
                flash("El Rol no puede ser mayor que la Cantidad en un ingrediente.", "error")
                return render_template("admin_recetas_nueva.html", platos=platos, ingredientes=ingredientes)

            filas_validas.append((int(ing_id), cant_f, rol_f))

        if not filas_validas:
            flash("La receta debe tener al menos un ingrediente con cantidad > 0.", "error")
            return render_template("admin_recetas_nueva.html", platos=platos, ingredientes=ingredientes)

        try:
            conn = get_connection()
            cur = conn.cursor()

            # Insert cabecera
            cur.execute(
                "INSERT INTO recetas_maestro (plato_id, raciones_base) VALUES (?, ?)",
                (int(plato_id), raciones_base_int)
            )
            receta_id = cur.lastrowid

            # Insert ingredientes
            for (ing_id, cant_f, rol_f) in filas_validas:
                cur.execute(
                    "INSERT INTO recetas_ingredientes (receta_id, ingrediente_id, cantidad, rol) VALUES (?, ?, ?, ?)",
                    (receta_id, ing_id, cant_f, rol_f)
                )

            conn.commit()
            conn.close()

            flash("Receta creada correctamente.", "ok")
            return redirect("/admin/recetas/listado")

        except Exception as e:
            print("ERROR guardando receta:", e)
            flash("Error al guardar la receta.", "error")

    return render_template("admin_recetas_nueva.html", platos=platos, ingredientes=ingredientes)

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