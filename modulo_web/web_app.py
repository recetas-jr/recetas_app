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
# NUEVA RECETA (MASTER) — BACKEND BLINDADO
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

        # --- BLOQUEO: receta duplicada por plato (mensaje con colores) ---
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                SELECT p.nombre
                FROM recetas_maestro r
                JOIN platos p ON p.id = r.plato_id
                WHERE r.plato_id = ?
            """, (int(plato_id),))
            fila = cur.fetchone()
            if fila:
                nombre_plato = fila["nombre"]
                conn.close()
                flash(
                    f"<span style='color:#0b5d1e; font-weight:bold;'>LA RECETA </span>"
                    f"<span style='color:#cc0000; font-weight:bold;'>{nombre_plato}</span>"
                    f"<span style='color:#0b5d1e; font-weight:bold;'> YA EXISTE</span>",
                    "error"
                )
                return render_template("admin_recetas_nueva.html", platos=platos, ingredientes=ingredientes)
            conn.close()
        except Exception as e:
            print("ERROR verificando duplicado de receta:", e)
            flash("Error verificando duplicado de receta.", "error")
            return render_template("admin_recetas_nueva.html", platos=platos, ingredientes=ingredientes)

        # --- Validación raciones ---
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

        # --- Validaciones de ingredientes ---
        vistos = set()
        filas_validas = []

        for i in range(len(ingredientes_ids)):
            ing_id = (ingredientes_ids[i] or "").strip()
            cant_txt = (cantidades[i] or "").strip()
            rol_txt = (roles[i] or "").strip()

            # Si no hay ingrediente seleccionado, saltamos la fila
            if not ing_id:
                continue

            # Duplicados de ingrediente
            if ing_id in vistos:
                flash("No se permiten ingredientes duplicados en la receta.", "error")
                return render_template("admin_recetas_nueva.html", platos=platos, ingredientes=ingredientes)
            vistos.add(ing_id)

            # Cantidad obligatoria > 0
            try:
                cant_f = float(cant_txt)
            except:
                flash("La cantidad debe ser numérica.", "error")
                return render_template("admin_recetas_nueva.html", platos=platos, ingredientes=ingredientes)

            if cant_f <= 0:
                flash("La cantidad debe ser mayor que 0 en todos los ingredientes.", "error")
                return render_template("admin_recetas_nueva.html", platos=platos, ingredientes=ingredientes)

            # Rol opcional, pero numérico y >= 0 y <= cantidad
            if rol_txt == "":
                rol_f = 0.0
            else:
                try:
                    rol_f = float(rol_txt)
                except:
                    flash("El rol debe ser numérico.", "error")
                    return render_template("admin_recetas_nueva.html", platos=platos, ingredientes=ingredientes)

                if rol_f < 0:
                    flash("El rol no puede ser negativo.", "error")
                    return render_template("admin_recetas_nueva.html", platos=platos, ingredientes=ingredientes)

                if rol_f > cant_f:
                    flash("El rol no puede ser mayor que la cantidad.", "error")
                    return render_template("admin_recetas_nueva.html", platos=platos, ingredientes=ingredientes)

            filas_validas.append((int(ing_id), cant_f, rol_f))

        if not filas_validas:
            flash("La receta debe tener al menos un ingrediente con cantidad > 0.", "error")
            return render_template("admin_recetas_nueva.html", platos=platos, ingredientes=ingredientes)

        # --- Guardado en BD ---
        try:
            conn = get_connection()
            cur = conn.cursor()

            cur.execute(
                "INSERT INTO recetas_maestro (plato_id, raciones_base) VALUES (?, ?)",
                (int(plato_id), raciones_base_int)
            )
            receta_id = cur.lastrowid

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
# BORRAR RECETA
# ==================================================

@app.route("/admin/recetas/borrar/<int:receta_id>", methods=["POST"])
def borrar_receta(receta_id):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("DELETE FROM recetas_ingredientes WHERE receta_id = ?", (receta_id,))
        cur.execute("DELETE FROM recetas_detalle WHERE receta_id = ?", (receta_id,))
        cur.execute("DELETE FROM recetas_maestro WHERE id = ?", (receta_id,))

        conn.commit()
        conn.close()
        flash("Receta borrada correctamente.", "ok")

    except Exception as e:
        print("ERROR borrando receta:", e)
        flash("No se pudo borrar la receta.", "error")

    return redirect("/admin/recetas/listado")

# ==================================================
# EJECUCIÓN
# ==================================================

if __name__ == "__main__":
    app.run(debug=True)