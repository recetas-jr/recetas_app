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

#==================================================
# ADMIN TIPOS DE PLATO
# ==================================================

@app.route("/admin/tipos_plato", methods=["GET", "POST"])
def admin_tipos_plato():
    errores = []

    if request.method == "POST":
        nombre = (request.form.get("nombre") or "").strip()

        if not nombre:
            errores.append("El nombre no puede estar vacío.")
        elif len(nombre) > 40:
            errores.append("El nombre no puede tener más de 40 caracteres.")

        if not errores:
            try:
                conn = get_connection()
                cur = conn.cursor()

                # Verificar duplicado (case-insensitive)
                cur.execute("SELECT id FROM tipos_plato WHERE LOWER(nombre) = LOWER(?)", (nombre,))
                existe = cur.fetchone()
                if existe:
                    conn.close()
                    errores.append("Ese tipo de plato ya existe.")
                else:
                    cur.execute("INSERT INTO tipos_plato (nombre) VALUES (?)", (nombre,))
                    conn.commit()
                    conn.close()
                    flash(f"Tipo de plato '<span class='item'>{nombre}</span>' creado correctamente.", "ok")
                    return redirect("/admin/tipos_plato")

            except Exception as e:
                print("ERROR creando tipo de plato:", e)
                errores.append("Error al crear el tipo de plato.")

    tipos = db_cargar_tipos_plato()
    return render_template("admin_tipos_plato.html", tipos=tipos, errores=errores)


@app.route("/admin/tipos_plato/borrar/<int:tipo_id>", methods=["POST"])
def borrar_tipo_plato(tipo_id):
    try:
        conn = get_connection()
        cur = conn.cursor()

        # Verificar si está en uso por algún plato
        cur.execute("SELECT COUNT(*) as c FROM platos WHERE tipo_plato_id = ?", (tipo_id,))
        fila = cur.fetchone()
        if fila and fila["c"] > 0:
            conn.close()
            flash("No se puede borrar el tipo de plato porque está en uso.", "error")
            return redirect("/admin/tipos_plato")

        # Obtener nombre para mensaje
        cur.execute("SELECT nombre FROM tipos_plato WHERE id = ?", (tipo_id,))
        fila_nombre = cur.fetchone()
        nombre = fila_nombre["nombre"] if fila_nombre else ""

        cur.execute("DELETE FROM tipos_plato WHERE id = ?", (tipo_id,))
        conn.commit()
        conn.close()

        flash(f"Tipo de plato '<span class='item'>{nombre}</span>' borrado correctamente.", "ok")

    except Exception as e:
        print("ERROR borrando tipo de plato:", e)
        flash("No se pudo borrar el tipo de plato.", "error")

    return redirect("/admin/tipos_plato")

# ==================================================
# ADMIN UNIDADES DE MEDIDA (UM)
# ==================================================

@app.route("/admin/unidades", methods=["GET", "POST"])
def admin_unidades():
    errores = []

    if request.method == "POST":
        codigo = (request.form.get("codigo") or "").strip().upper()
        nombre = (request.form.get("nombre") or "").strip().lower()

        if not codigo:
            errores.append("El código es obligatorio.")
        elif len(codigo) > 2:
            errores.append("El código no puede tener más de 2 caracteres.")

        if not nombre:
            errores.append("El nombre es obligatorio.")

        if not errores:
            try:
                conn = get_connection()
                cur = conn.cursor()

                # Verificar duplicados (código o nombre)
                cur.execute(
                    "SELECT id FROM unidades WHERE LOWER(codigo) = LOWER(?) OR LOWER(nombre) = LOWER(?)",
                    (codigo, nombre)
                )
                existe = cur.fetchone()
                if existe:
                    conn.close()
                    errores.append("Ya existe una unidad con ese código o nombre.")
                else:
                    cur.execute(
                        "INSERT INTO unidades (codigo, nombre) VALUES (?, ?)",
                        (codigo, nombre)
                    )
                    conn.commit()
                    conn.close()
                    flash(f"Unidad '<span class='item'>{codigo} - {nombre}</span>' creada correctamente.", "ok")
                    return redirect("/admin/unidades")

            except Exception as e:
                print("ERROR creando unidad:", e)
                errores.append("Error al crear la unidad.")

    unidades = db_cargar_unidades()
    return render_template("admin_unidades.html", unidades=unidades, errores=errores)


@app.route("/admin/unidades/borrar/<int:unidad_id>", methods=["POST"])
def borrar_unidad(unidad_id):
    try:
        conn = get_connection()
        cur = conn.cursor()

        # Verificar si está en uso por algún ingrediente
        cur.execute("SELECT COUNT(*) as c FROM ingredientes WHERE unidad_id = ?", (unidad_id,))
        fila = cur.fetchone()
        if fila and fila["c"] > 0:
            conn.close()
            flash("No se puede borrar la unidad porque está en uso por algún ingrediente.", "error")
            return redirect("/admin/unidades")

        # Obtener nombre para mensaje
        cur.execute("SELECT codigo, nombre FROM unidades WHERE id = ?", (unidad_id,))
        fila_nombre = cur.fetchone()
        codigo = fila_nombre["codigo"] if fila_nombre else ""
        nombre = fila_nombre["nombre"] if fila_nombre else ""

        cur.execute("DELETE FROM unidades WHERE id = ?", (unidad_id,))
        conn.commit()
        conn.close()

        flash(f"Unidad '<span class='item'>{codigo} - {nombre}</span>' borrada correctamente.", "ok")

    except Exception as e:
        print("ERROR borrando unidad:", e)
        flash("No se pudo borrar la unidad.", "error")

    return redirect("/admin/unidades")


# ==================================================
# ADMIN INGREDIENTES
# ==================================================

@app.route("/admin/ingredientes", methods=["GET", "POST"])
def admin_ingredientes():
    errores = []

    if request.method == "POST":
        nombre = (request.form.get("nombre") or "").strip().lower()
        unidad_id = (request.form.get("unidad_id") or "").strip()

        if not nombre:
            errores.append("El nombre del ingrediente es obligatorio.")

        if not unidad_id:
            errores.append("Debe seleccionar una unidad de medida.")

        if not errores:
            try:
                conn = get_connection()
                cur = conn.cursor()

                # Verificar duplicado por nombre (case-insensitive)
                cur.execute("SELECT id FROM ingredientes WHERE LOWER(nombre) = LOWER(?)", (nombre,))
                existe = cur.fetchone()
                if existe:
                    conn.close()
                    errores.append("Ese ingrediente ya existe.")
                else:
                    cur.execute(
                        "INSERT INTO ingredientes (nombre, unidad_id) VALUES (?, ?)",
                        (nombre, int(unidad_id))
                    )
                    conn.commit()
                    conn.close()
                    flash(f"Ingrediente '<span class='item'>{nombre}</span>' creado correctamente.", "ok")
                    return redirect("/admin/ingredientes")

            except Exception as e:
                print("ERROR creando ingrediente:", e)
                errores.append("Error al crear el ingrediente.")

    ingredientes = db_cargar_ingredientes()
    unidades = db_cargar_unidades()
    return render_template(
        "admin_ingredientes.html",
        ingredientes=ingredientes,
        unidades=unidades,
        errores=errores
    )


@app.route("/admin/ingredientes/borrar/<int:ingrediente_id>", methods=["POST"])
def borrar_ingrediente(ingrediente_id):
    try:
        conn = get_connection()
        cur = conn.cursor()

        # Verificar si está en uso en alguna receta
        cur.execute("SELECT COUNT(*) as c FROM recetas_ingredientes WHERE ingrediente_id = ?", (ingrediente_id,))
        fila = cur.fetchone()
        if fila and fila["c"] > 0:
            conn.close()
            flash("No se puede borrar el ingrediente porque está en uso en alguna receta.", "error")
            return redirect("/admin/ingredientes")

        # Obtener nombre para mensaje
        cur.execute("SELECT nombre FROM ingredientes WHERE id = ?", (ingrediente_id,))
        fila_nombre = cur.fetchone()
        nombre = fila_nombre["nombre"] if fila_nombre else ""

        cur.execute("DELETE FROM ingredientes WHERE id = ?", (ingrediente_id,))
        conn.commit()
        conn.close()

        flash(f"Ingrediente '<span class='item'>{nombre}</span>' borrado correctamente.", "ok")

    except Exception as e:
        print("ERROR borrando ingrediente:", e)
        flash("No se pudo borrar el ingrediente.", "error")

    return redirect("/admin/ingredientes")

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