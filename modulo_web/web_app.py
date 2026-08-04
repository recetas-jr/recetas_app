from flask import (
    Flask,
    render_template,
    request,
    redirect,
    flash,
    abort,
    session,
    jsonify
)
from markupsafe import Markup
from datetime import timedelta
from datetime import datetime

import sqlite3

from modulo_web.persistencia_db import (
    db_cargar_platos,
    db_cargar_unidades,

    db_insertar_equivalencia,
    db_borrar_equivalencia,
    db_cargar_recetas_maestro_listado,
    db_cargar_tipos_plato,
    db_cargar_receta_detalle,
    get_connection,
    db_cargar_recetas_publicadas,
    init_db,
    db_insertar_contacto,
    db_listar_contactos,
    db_cargar_contactos,
    db_cargar_contacto,
    db_marcar_contacto_atendido,
    db_cargar_unidades_disponibles_por_ingrediente,
    db_cargar_ingredientes,
    db_cargar_ingrediente_por_id,
    db_cargar_expresiones_culinarias
)

from modulo_web.motor_conversion import (
    obtener_equivalencias,
    representar,
    normalizar,
    puede_convertir,
    IngredienteSinEquivalencias
)

app = Flask(__name__)
app.secret_key = "recetas_app_secret_key_2026"
app.permanent_session_lifetime = timedelta(hours=4)

init_db()

app.config["PROPAGATE_EXCEPTIONS"] = True
ADMIN_USER = "admin"
ADMIN_PASS = "Recetas2026_Admin!"


@app.route("/")
def inicio():
    return redirect("/recetas")


@app.route("/admin")
def menu_admin():

    if "usuario" not in session:
        return redirect("/login")

    return render_template(
        "menu_principal.html"
    )


@app.before_request
def proteger_admin():

    ruta = request.path

    if ruta.startswith("/admin"):

        if not session.get("admin"):

            return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("admin"):
        return redirect("/admin")

    if request.method == "POST":

        usuario = request.form.get("usuario", "").strip()
        password = request.form.get("password", "").strip()

        if usuario == ADMIN_USER and password == ADMIN_PASS:

            session.permanent = True

            session["admin"] = True

            session["usuario"] = usuario

            flash("Login correcto.", "recetas")

            return redirect("/admin")

        flash("Usuario o contraseña incorrectos.", "error")

    return render_template("login.html")


@app.route("/logout")
def logout():

    session.clear()

    flash("Sesión cerrada.", "recetas")

    return redirect("/login")

# ==================================================
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

                cur.execute(
                    "SELECT id FROM tipos_plato WHERE LOWER(nombre) = LOWER(?)", (nombre,))
                existe = cur.fetchone()
                if existe:
                    conn.close()
                    errores.append(
                        f"⚠️ "
                        f"<span style='color:#cc0000; font-weight:bold;'>{nombre}</span> "
                        f"<span style='color:#0b5d1e; font-weight:bold;'>ya existe en</span> "
                        f"<span style='color:#cc0000; font-weight:bold;'>TIPO DE PLATO</span>"
                    )
                else:
                    cur.execute(
                        "INSERT INTO tipos_plato (nombre) VALUES (?)", (nombre,))
                    conn.commit()
                    conn.close()
                    flash(
                        f"Tipo de plato '<span class='item'>{nombre}</span>' creado correctamente.", "ok")
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

        cur.execute(
            "SELECT COUNT(*) as c FROM platos WHERE tipo_plato_id = ?", (tipo_id,))
        fila = cur.fetchone()
        if fila and fila["c"] > 0:
            cur.execute(
                "SELECT nombre FROM tipos_plato WHERE id = ?", (tipo_id,))
            fila_nombre = cur.fetchone()
            nombre = fila_nombre["nombre"] if fila_nombre else ""
            conn.close()

            flash(
                f"⚠️ "
                f"<span style='color:#cc0000; font-weight:bold;'>{nombre}</span> "
                f"<span style='color:#0b5d1e; font-weight:bold;'>no se borra por estar en uso en</span> "
                f"<span style='color:#cc0000; font-weight:bold;'>NOMENCLADOR DE PLATO</span>",
                "error"
            )
            return redirect("/admin/tipos_plato")

        cur.execute("SELECT nombre FROM tipos_plato WHERE id = ?", (tipo_id,))
        fila_nombre = cur.fetchone()
        nombre = fila_nombre["nombre"] if fila_nombre else ""

        cur.execute("DELETE FROM tipos_plato WHERE id = ?", (tipo_id,))
        conn.commit()
        conn.close()

        flash(
            f"Tipo de plato '<span class='item'>{nombre}</span>' borrado correctamente.", "ok")

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
        elif len(codigo) > 5:
            errores.append("El código no puede tener más de 5 caracteres.")

        if not nombre:
            errores.append("El nombre es obligatorio.")

        if not errores:
            try:
                conn = get_connection()
                cur = conn.cursor()

                # DUPLICADO POR CÓDIGO
                cur.execute(
                    "SELECT codigo FROM unidades WHERE LOWER(codigo) = LOWER(?)",
                    (codigo,)
                )
                existe_codigo = cur.fetchone()

                if existe_codigo:
                    conn.close()
                    errores.append(
                        f"⚠️ "
                        f"<span style='color:#cc0000; font-weight:bold;'>CÓDIGO {codigo}</span> "
                        f"<span style='color:#0b5d1e; font-weight:bold;'>ya existe en</span> "
                        f"<span style='color:#cc0000; font-weight:bold;'>NOMENCLADOR DE UNIDADES</span>"
                    )
                else:
                    # DUPLICADO POR DESCRIPCIÓN
                    cur.execute(
                        "SELECT nombre FROM unidades WHERE LOWER(nombre) = LOWER(?)",
                        (nombre,)
                    )
                    existe_nombre = cur.fetchone()

                    if existe_nombre:
                        conn.close()
                        errores.append(
                            f"⚠️ "
                            f"<span style='color:#cc0000; font-weight:bold;'>DESCRIPCIÓN {nombre}</span> "
                            f"<span style='color:#0b5d1e; font-weight:bold;'>ya existe en</span> "
                            f"<span style='color:#cc0000; font-weight:bold;'>NOMENCLADOR DE UNIDADES</span>"
                        )
                    else:
                        cur.execute(
                            "INSERT INTO unidades (codigo, nombre) VALUES (?, ?)",
                            (codigo, nombre)
                        )
                        conn.commit()
                        conn.close()
                        flash(
                            f"Unidad '<span class='item'>{codigo} - {nombre}</span>' creada correctamente.", "ok")
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

        # Obtener primero datos de la unidad
        cur.execute(
            "SELECT codigo, nombre FROM unidades WHERE id = ?", (unidad_id,))
        fila_nombre = cur.fetchone()
        codigo = fila_nombre["codigo"] if fila_nombre else ""
        nombre = fila_nombre["nombre"] if fila_nombre else ""

        # Verificar si está en uso
        cur.execute(
            "SELECT COUNT(*) as c FROM ingredientes WHERE unidad_id = ?", (unidad_id,))
        fila = cur.fetchone()

        if fila and fila["c"] > 0:
            conn.close()
            flash(
                f"⚠️ "
                f"<span style='color:#cc0000; font-weight:bold;'>{codigo} - {nombre}</span> "
                f"<span style='color:#0b5d1e; font-weight:bold;'>no se borra por estar en uso en</span> "
                f"<span style='color:#cc0000; font-weight:bold;'>NOMENCLADOR DE INGREDIENTES</span>",
                "error"
            )
            return redirect("/admin/unidades")

        cur.execute("DELETE FROM unidades WHERE id = ?", (unidad_id,))
        conn.commit()
        conn.close()

        flash(
            f"Unidad '<span class='item'>{codigo} - {nombre}</span>' borrada correctamente.", "ok")

    except Exception as e:
        print("ERROR borrando unidad:", e)
        flash("No se pudo borrar la unidad.", "error")

    return redirect("/admin/unidades")

# ==================================================
# ADMIN EXPRESIONES CULINARIAS
# ==================================================


@app.route("/admin/expresiones_culinarias", methods=["GET", "POST"])
def admin_expresiones_culinarias():

    errores = []

    if request.method == "POST":

        codigo = (request.form.get("codigo") or "").strip()

        nombre = (request.form.get("nombre") or "").strip()

        if not codigo:
            errores.append("El código es obligatorio.")

        if not nombre:
            errores.append("El nombre es obligatorio.")

        if not errores:
            conn = get_connection()
            cur = conn.cursor()

            cur.execute(
                "SELECT id FROM expresiones_culinarias WHERE LOWER(codigo) = LOWER(?)",
                (codigo,)
            )

            existe = cur.fetchone()
            if existe:

                conn.close()

                errores.append(
                    f"⚠️ "
                    f"<span style='color:#cc0000; font-weight:bold;'>CÓDIGO {codigo}</span> "
                    f"<span style='color:#0b5d1e; font-weight:bold;'>ya existe en</span> "
                    f"<span style='color:#cc0000; font-weight:bold;'>EXPRESIONES CULINARIAS</span>"
                )

            else:

                cur.execute(
                    "SELECT id FROM expresiones_culinarias WHERE LOWER(nombre) = LOWER(?)",
                    (nombre,)
                )

                existe = cur.fetchone()

                if existe:

                    conn.close()

                    errores.append(
                        f"⚠️ "
                        f"<span style='color:#cc0000; font-weight:bold;'>{nombre}</span> "
                        f"<span style='color:#0b5d1e; font-weight:bold;'>ya existe en</span> "
                        f"<span style='color:#cc0000; font-weight:bold;'>EXPRESIONES CULINARIAS</span>"
                    )

                else:

                    cur.execute(
                        """
                        INSERT INTO expresiones_culinarias
                        (codigo, nombre)
                        VALUES (?, ?)
                        """,
                        (codigo, nombre)
                    )

                    conn.commit()

                    conn.close()

                    flash(
                        f"Expresión culinaria '<span class='item'>{codigo} - {nombre}</span>' creada correctamente.",
                        "ok"
                    )

                    return redirect("/admin/expresiones_culinarias")

    expresiones = db_cargar_expresiones_culinarias()

    return render_template(
        "admin_expresiones_culinarias.html",
        expresiones=expresiones,
        errores=errores
    )


@app.route("/admin/expresiones_culinarias/borrar/<int:expresion_id>", methods=["POST"])
def borrar_expresion_culinaria(expresion_id):
    try:

        conn = get_connection()
        cur = conn.cursor()

        # Obtener código y nombre antes de borrar

        cur.execute(
            """
            SELECT codigo, nombre
            FROM expresiones_culinarias
            WHERE id = ?
            """,
            (expresion_id,)
        )

        fila = cur.fetchone()

        codigo = fila["codigo"] if fila else ""

        nombre = fila["nombre"] if fila else ""

        cur.execute(
            "DELETE FROM expresiones_culinarias WHERE id = ?",
            (expresion_id,)
        )

        conn.commit()

        conn.close()

        flash(
            f"Expresión culinaria '<span class='item'>{codigo} - {nombre}</span>' borrada correctamente.",
            "ok"
        )

    except Exception as e:

        print("ERROR borrando expresión culinaria:", e)

        flash(
            "No se pudo borrar la expresión culinaria.",
            "error"
        )

    return redirect("/admin/expresiones_culinarias")

# ==================================================
# ADMIN INGREDIENTES
# ==================================================


@app.route("/admin/ingredientes", methods=["GET", "POST"])
def admin_ingredientes():
    errores = []

    if request.method == "POST":
        nombre = (request.form.get("nombre") or "").strip().lower()
        unidad_id = (request.form.get("unidad_id") or "").strip()

        # VALIDACIONES
        if not nombre:
            errores.append("El nombre del ingrediente es obligatorio.")

        if not unidad_id:
            errores.append("Debe seleccionar una unidad de medida.")

        if not errores:
            try:
                conn = get_connection()
                cur = conn.cursor()

                # Verificar duplicado
                cur.execute(
                    "SELECT id FROM ingredientes WHERE LOWER(nombre) = LOWER(?)",
                    (nombre,)
                )
                existe = cur.fetchone()

                if existe:
                    conn.close()
                    errores.append(
                        f"⚠️ "
                        f"<span style='color:#cc0000; font-weight:bold;'>{nombre}</span> "
                        f"<span style='color:#0b5d1e; font-weight:bold;'>ya existe en</span> "
                        f"<span style='color:#cc0000; font-weight:bold;'>NOMENCLADOR DE INGREDIENTES</span>"
                    )
                else:
                    cur.execute(
                        "INSERT INTO ingredientes (nombre, unidad_id) VALUES (?, ?)",
                        (nombre, int(unidad_id))
                    )
                    conn.commit()
                    conn.close()

                    flash(
                        f"Ingrediente '<span class='item'>{nombre}</span>' creado correctamente.",
                        "ok"
                    )
                    return redirect("/admin/ingredientes")

            except Exception as e:
                print("ERROR creando ingrediente:", e)
                errores.append("Error al crear el ingrediente.")

    ingredientes = cargar_ingredientes_con_unidad()

    unidades = db_cargar_unidades()

    return render_template(
        "admin_ingredientes.html",
        ingredientes=ingredientes,
        unidades=unidades,
        errores=errores
    )


@app.route(
    "/admin/ingredientes/<int:ingrediente_id>/equivalencias",
    methods=["GET", "POST"]
)
def admin_equivalencias(ingrediente_id):
    errores = []

    unidades = db_cargar_unidades()

    if request.method == "POST":

        unidad_id = request.form.get("unidad_id")

        factor = request.form.get("factor")

        try:

            db_insertar_equivalencia(
                ingrediente_id,
                int(unidad_id),
                float(factor)
            )

            unidad_txt = ""

            for u in unidades:
                if u["id"] == int(unidad_id):
                    unidad_txt = f'{u["codigo"]} - {u["nombre"]}'
                    break

            flash(
                f"Equivalencia '<span class='item'>{unidad_txt}</span>' creada correctamente.",
                "ok"
            )

            return redirect(
                f"/admin/ingredientes/{ingrediente_id}/equivalencias"
            )

        except sqlite3.IntegrityError:

            unidad_txt = ""

            for u in unidades:
                if u["id"] == int(unidad_id):
                    unidad_txt = f'{u["codigo"]} - {u["nombre"]}'
                    break

            errores.append(
                f"⚠️ "
                f"<span style='color:#cc0000; font-weight:bold;'>{unidad_txt}</span> "
                f"<span style='color:#0b5d1e; font-weight:bold;'>ya existe en</span> "
                f"<span style='color:#cc0000; font-weight:bold;'>EQUIVALENCIAS DE INGREDIENTES</span>"
            )

    ingrediente = db_cargar_ingrediente_por_id(ingrediente_id)

    if ingrediente is None:
        abort(404)

    ingrediente_nombre = ingrediente["nombre"]

    unidad_canonica = {
        "codigo": ingrediente["unidad_codigo"],
        "nombre": ingrediente["unidad_nombre"]
    }

    try:

        equivalencias = obtener_equivalencias(
            ingrediente_id
        )

    except IngredienteSinEquivalencias:

        equivalencias = []

        flash(
            "Este ingrediente aún no tiene equivalencias registradas.",
            "info"
        )

    return render_template(
        "admin_equivalencias.html",
        ingrediente_id=ingrediente_id,
        ingrediente_nombre=ingrediente_nombre,
        equivalencias=equivalencias,
        unidades=unidades,
        errores=errores,
        unidad_canonica=unidad_canonica,
        menu_url="/admin/ingredientes",
        menu_texto="← Nomenclador de Ingredientes"
    )


@app.route(
    "/admin/ingredientes/<int:ingrediente_id>/equivalencias/borrar/<int:equivalencia_id>",
    methods=["POST"]
)
def borrar_equivalencia(ingrediente_id, equivalencia_id):
    try:

        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT u.codigo, u.nombre
            FROM ingredientes_equivalencias e
            JOIN unidades u
                ON u.id = e.unidad_id
            WHERE e.id = ?
            """,
            (equivalencia_id,)
        )

        fila = cur.fetchone()

        codigo = fila["codigo"] if fila else ""
        nombre = fila["nombre"] if fila else ""

        conn.close()

        db_borrar_equivalencia(equivalencia_id)

        flash(
            f"Equivalencia '<span class='item'>{codigo} - {nombre}</span>' borrada correctamente.",
            "ok"
        )

    except Exception as e:
        print("ERROR borrando equivalencia:", e)

    return redirect(
        f"/admin/ingredientes/{ingrediente_id}/equivalencias"
    )


@app.route("/admin/ingredientes/borrar/<int:ingrediente_id>", methods=["POST"])
def borrar_ingrediente(ingrediente_id):
    try:
        conn = get_connection()
        cur = conn.cursor()

        # Obtener nombre antes de cualquier validación
        cur.execute("SELECT nombre FROM ingredientes WHERE id = ?",
                    (ingrediente_id,))
        fila_nombre = cur.fetchone()
        nombre = fila_nombre["nombre"] if fila_nombre else ""

        # Verificar si está en uso
        cur.execute(
            "SELECT COUNT(*) as c FROM recetas_ingredientes WHERE ingrediente_id = ?",
            (ingrediente_id,)
        )
        fila = cur.fetchone()

        if fila and fila["c"] > 0:
            conn.close()
            flash(
                f"⚠️ "
                f"<span style='color:#cc0000; font-weight:bold;'>{nombre}</span> "
                f"<span style='color:#0b5d1e; font-weight:bold;'>no se borra por estar en uso en</span> "
                f"<span style='color:#cc0000; font-weight:bold;'>RECETAS</span>",
                "error"
            )
            return redirect("/admin/ingredientes")

        cur.execute("DELETE FROM ingredientes WHERE id = ?", (ingrediente_id,))
        conn.commit()
        conn.close()

        flash(
            f"Ingrediente '<span class='item'>{nombre}</span>' borrado correctamente.",
            "ok"
        )

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
# ADMIN PLATOS
# ==================================================

@app.route("/admin/platos", methods=["GET", "POST"])
def admin_platos():
    errores = []
    tipo_seleccionado = ""

    if request.method == "POST":
        nombre = (request.form.get("nombre") or "").strip()
        tipo_plato_id = (request.form.get("tipo_plato_id") or "").strip()
        peso_racion = (request.form.get("peso_racion") or "").strip()

        tipo_seleccionado = tipo_plato_id  # mantener selección

        # Validación nombre
        if not nombre:
            errores.append("El nombre del plato es obligatorio.")

        # Validación tipo
        if not tipo_plato_id:
            errores.append("Debe seleccionar un tipo de plato.")

        # Validación peso
        if not peso_racion:
            errores.append("El peso de la ración es obligatorio.")
        else:
            try:
                peso_float = float(peso_racion)
                if peso_float <= 0:
                    errores.append(
                        "El peso de la ración debe ser mayor que 0.")
            except:
                errores.append("El peso de la ración debe ser numérico.")

        if not errores:
            try:
                conn = get_connection()
                cur = conn.cursor()

                # Duplicado específico
                cur.execute(
                    "SELECT nombre FROM platos WHERE LOWER(nombre) = LOWER(?)",
                    (nombre,)
                )
                existe = cur.fetchone()

                if existe:
                    conn.close()
                    errores.append(
                        f"⚠️ "
                        f"<span style='color:#cc0000; font-weight:bold;'>{nombre}</span> "
                        f"<span style='color:#0b5d1e; font-weight:bold;'>ya existe en</span> "
                        f"<span style='color:#cc0000; font-weight:bold;'>NOMENCLADOR DE PLATOS</span>"
                    )
                else:
                    cur.execute(
                        "INSERT INTO platos (nombre, tipo_plato_id, peso_racion) VALUES (?, ?, ?)",
                        (nombre, int(tipo_plato_id), peso_float)
                    )
                    conn.commit()
                    conn.close()

                    flash(
                        f"Plato '<span class='item'>{nombre}</span>' creado correctamente.",
                        "platos"
                    )
                    return redirect("/admin/platos")

            except Exception as e:
                print("ERROR creando plato:", e)
                errores.append("Error al crear el plato.")

    platos = db_cargar_platos()
    tipos_plato = db_cargar_tipos_plato()

    return render_template(
        "admin_platos.html",
        platos=platos,
        tipos_plato=tipos_plato,
        errores=errores,
        tipo_seleccionado=tipo_seleccionado
    )


@app.route("/admin/platos/borrar/<int:plato_id>", methods=["POST"])
def borrar_plato(plato_id):
    try:
        conn = get_connection()
        cur = conn.cursor()

        # Obtener nombre del plato
        cur.execute("SELECT nombre FROM platos WHERE id = ?", (plato_id,))
        fila_nombre = cur.fetchone()
        nombre = fila_nombre["nombre"] if fila_nombre else ""

        # Verificar uso en RECETAS
        cur.execute(
            "SELECT COUNT(*) as c FROM recetas_maestro WHERE plato_id = ?",
            (plato_id,)
        )
        fila = cur.fetchone()

        if fila and fila["c"] > 0:
            conn.close()
            flash(
                f"⚠️ "
                f"<span style='color:#cc0000; font-weight:bold;'>{nombre}</span> "
                f"<span style='color:#0b5d1e; font-weight:bold;'>no se borra por estar en uso en</span> "
                f"<span style='color:#cc0000; font-weight:bold;'>RECETAS</span>",
                "platos"
            )
            return redirect("/admin/platos")

        cur.execute("DELETE FROM platos WHERE id = ?", (plato_id,))
        conn.commit()
        conn.close()

        flash(
            f"Plato '<span class='item'>{nombre}</span>' borrado correctamente.",
            "platos"
        )

    except Exception as e:
        print("ERROR borrando plato:", e)
        flash(
            "No se pudo borrar el plato.",
            "platos"
        )

    return redirect("/admin/platos")

# ==================================================
# INDEX
# ==================================================


@app.route("/", methods=["GET"])
def portada():
    return render_template("portada.html")


@app.route("/recetas", methods=["GET"])
def catalogo_publico():

    desde_admin = request.args.get("admin") == "1"

    recetas = db_cargar_recetas_publicadas()

    return render_template(
        "index.html",
        recetas=recetas,
        desde_admin=desde_admin
    )


@app.route("/receta/<int:receta_id>")
def receta_detalle(receta_id):

    desde_admin = request.args.get("admin") == "1"

    raciones_nuevas = request.args.get("raciones", type=float)

    receta = db_cargar_receta_detalle(receta_id)
    ingredientes = receta["ingredientes"]

    raciones_base = receta["raciones_base"]

    if raciones_base <= 0:
        raciones_base = 1

    if raciones_nuevas is None or raciones_nuevas <= 0:
        raciones_nuevas = raciones_base

    # límite superior para evitar locuras
    if raciones_nuevas > 1000:
        raciones_nuevas = raciones_base

    ingredientes_escalados = escalar_ingredientes(
        ingredientes,
        raciones_base,
        raciones_nuevas
    )

    for ingrediente in ingredientes_escalados:

        unidades = db_cargar_unidades_disponibles_por_ingrediente(
            ingrediente["ingrediente_id"]
        )

        ingrediente["conversion"] = {
            "permite": len(unidades) > 1,
            "unidad_actual": ingrediente["unidad_codigo"],
            "unidades": unidades,
        }

    return render_template(
        "receta_detalle.html",
        receta=receta,
        ingredientes=ingredientes_escalados,
        raciones_base=raciones_base,
        raciones_nuevas=raciones_nuevas,
        desde_admin=desde_admin
    )


@app.route("/receta/<int:receta_id>/preparacion")
def receta_preparacion(receta_id):

    receta = db_cargar_receta_detalle(receta_id)

    raciones_nuevas = request.args.get("raciones", type=float)

    if not raciones_nuevas or raciones_nuevas <= 0:
        raciones_nuevas = receta.get("raciones", 1)

    desde_admin = request.args.get("admin") == "1"

    return render_template(
        "receta_preparacion.html",
        receta=receta,
        raciones_nuevas=raciones_nuevas,
        desde_admin=desde_admin
    )

# ==================================================
# ADMIN RECETAS — LISTADO
# ==================================================


@app.route("/admin/recetas/listado", methods=["GET"])
def admin_recetas_listado():
    recetas_listado = db_cargar_recetas_maestro_listado()
    return render_template("admin_recetas_listado.html", recetas=recetas_listado)


# ==================================================
# API TEMPORAL
# VISOR DE NORMALIZACIÓN
# (Instrumentación Fase IV)
# ==================================================

@app.route("/api/normalizar", methods=["POST"])
def api_normalizar():

    datos = request.get_json()

    if datos is None:

        return jsonify({
            "ok": False,
            "error": "No se recibió un JSON válido."
        }), 400

    try:

        ingrediente_id = int(datos["ingredienteId"])

        cantidad = float(datos["cantidadCaptura"])

        deco = float(datos["decoCaptura"])

        unidad_origen = str(datos["unidadCaptura"])

        cantidad_canonica = normalizar(

            ingrediente_id=ingrediente_id,

            cantidad=cantidad,

            unidad_origen=unidad_origen

        )

        deco_canonica = normalizar(

            ingrediente_id=ingrediente_id,

            cantidad=deco,

            unidad_origen=unidad_origen

        )

        cocina_captura = cantidad - deco

        return jsonify({

            "ok": True,

            "cantidad_canonica": cantidad_canonica,

            "cocina_canonica":
            cantidad_canonica - deco_canonica,

            "deco_canonica":
                deco_canonica,

            "cocina_captura":
                cocina_captura,

        })

    except Exception as e:

        return jsonify({

            "ok": False,

            "error": str(e)

        }), 500

# ==================================================
# API DE REPRESENTACIÓN DEL MOTOR DE CONVERSIÓN
# ==================================================


@app.route("/api/convertir", methods=["POST"])
def api_representar():

    datos = request.get_json()

    if datos is None:
        return jsonify({
            "ok": False,
            "error": "No se recibió un JSON válido."
        }), 400

    ingrediente_id = int(datos["ingrediente_id"])

    cantidad_canonica = float(datos["cantidad_canonica"])

    cocina_canonica = float(
        datos.get("cocina_canonica", cantidad_canonica)
    )

    deco_canonica = float(
        datos.get("deco_canonica", 0)
    )

    unidad_canonica = str(datos["unidad_canonica"])

    unidad_destino = str(datos["unidad_destino"])

    cocina_convertida = representar(

        ingrediente_id,
        cocina_canonica,
        unidad_canonica,
        unidad_destino

    )

    deco_convertida = representar(

        ingrediente_id,
        deco_canonica,
        unidad_canonica,
        unidad_destino

    )

    cantidad_convertida = representar(

        ingrediente_id,
        cantidad_canonica,
        unidad_canonica,
        unidad_destino

    )

    return jsonify({
        "ok": True,
        "cocina_convertida": cocina_convertida,
        "deco_convertida": deco_convertida,
        "total_convertido": cantidad_convertida
    })


@app.route("/admin/recetas/nueva", methods=["GET", "POST"])
def admin_recetas_nueva():
    platos = db_cargar_platos()
    ingredientes = cargar_ingredientes_con_unidad()

    unidades_por_ingrediente = {}

    for ingrediente in ingredientes:
        unidades_por_ingrediente[ingrediente["id"]] = (
            db_cargar_unidades_disponibles_por_ingrediente(
                ingrediente["id"]
            )
        )

    contexto_receta = {
        "platos": platos,
        "ingredientes": ingredientes,
        "unidades_por_ingrediente": unidades_por_ingrediente
    }

    if request.method == "POST":

        plato_id = request.form.get("plato_id", "").strip()
        raciones_base = request.form.get("raciones_base", "").strip()
        preparacion = request.form.get("preparacion", "").strip()
        elaboracion = request.form.get("elaboracion", "").strip()
        presentacion = request.form.get("presentacion", "").strip()
        nutricion = request.form.get("nutricion", "").strip()

        if not plato_id:
            flash(
                f"⚠️ "
                f"<span style='color:#0b5d1e; font-weight:bold;'>Debe seleccionar un</span> "
                f"<span style='color:#cc0000; font-weight:bold;'>PLATO</span> "
                f"<span style='color:#0b5d1e; font-weight:bold;'>en</span> "
                f"<span style='color:#cc0000; font-weight:bold;'>RECETAS</span>",
                "recetas"
            )
            return render_template(
                "admin_recetas_nueva.html",
                **contexto_receta
            )

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
                    f"⚠️ "
                    f"<span style='color:#cc0000; font-weight:bold;'>{nombre_plato}</span> "
                    f"<span style='color:#0b5d1e; font-weight:bold;'>ya existe en</span> "
                    f"<span style='color:#cc0000; font-weight:bold;'>RECETAS</span>",
                    "recetas"
                )
                return render_template(
                    "admin_recetas_nueva.html",
                    **contexto_receta
                )
            conn.close()
        except Exception as e:
            print("ERROR verificando duplicado de receta:", e)
            flash("Error verificando duplicado de receta.", "error")
            return render_template(
                "admin_recetas_nueva.html",
                **contexto_receta
            )

        try:
            raciones_base_int = int(raciones_base)
            if raciones_base_int <= 0:
                flash(
                    f"⚠️ "
                    f"<span style='color:#cc0000; font-weight:bold;'>RACIONES BASE</span> "
                    f"<span style='color:#0b5d1e; font-weight:bold;'>debe ser mayor que 0 en</span> "
                    f"<span style='color:#cc0000; font-weight:bold;'>RECETAS</span>",
                    "recetas"
                )
                return render_template(
                    "admin_recetas_nueva.html",
                    **contexto_receta
                )
        except:
            flash(
                f"⚠️ "
                f"<span style='color:#cc0000; font-weight:bold;'>RACIONES BASE</span> "
                f"<span style='color:#0b5d1e; font-weight:bold;'>debe ser un valor numérico en</span> "
                f"<span style='color:#cc0000; font-weight:bold;'>RECETAS</span>",
                "recetas"
            )
            return render_template(
                "admin_recetas_nueva.html",
                **contexto_receta
            )

        ingredientes_ids = request.form.getlist("ingrediente_id[]")
        cantidades = request.form.getlist("cantidad[]")
        roles = request.form.getlist("rol[]")
        unidades = request.form.getlist("unidad[]")

        print("=" * 60)
        print("ingredientes_ids:", ingredientes_ids)
        print("unidades:", unidades)
        print("=" * 60)

        vistos = set()
        filas_validas = []

        print("=" * 60)
        print("RECORRIDO DE FILAS RECIBIDAS")
        print("=" * 60)

        max_filas = max(
            len(ingredientes_ids),
            len(cantidades),
            len(roles),
            len(unidades)
        )

        for j in range(max_filas):

            ing = ingredientes_ids[j] if j < len(
                ingredientes_ids) else "<NO EXISTE>"
            cant = cantidades[j] if j < len(cantidades) else "<NO EXISTE>"
            rol = roles[j] if j < len(roles) else "<NO EXISTE>"
            um = unidades[j] if j < len(unidades) else "<NO EXISTE>"

            print(
                f"Fila {j}: "
                f"Ingrediente=[{ing}]  "
                f"Cantidad=[{cant}]  "
                f"Rol=[{rol}]  "
                f"Unidad=[{um}]"
            )

            print("=" * 60)

        for i in range(len(ingredientes_ids)):
            ing_id = (ingredientes_ids[i] or "").strip()
            cant_txt = (cantidades[i] or "").strip()
            rol_txt = (roles[i] or "").strip()

            if not ing_id:
                continue

            unidad_id = (
                (unidades[i] if i < len(unidades) else "")
                or ""
            ).strip()

            if ing_id in vistos:
                flash("No se permiten ingredientes duplicados en la receta.", "error")
                return render_template(
                    "admin_recetas_nueva.html",
                    **contexto_receta
                )
            vistos.add(ing_id)

            try:
                cant_f = float(cant_txt)
            except:
                flash("La cantidad debe ser numérica.", "error")
                return render_template(
                    "admin_recetas_nueva.html",
                    **contexto_receta
                )

            if cant_f <= 0:
                flash(
                    "La cantidad debe ser mayor que 0 en todos los ingredientes.", "error")
                return render_template(
                    "admin_recetas_nueva.html",
                    **contexto_receta
                )

            if rol_txt == "":
                rol_f = 0.0
            else:
                try:
                    rol_f = float(rol_txt)
                except:
                    flash("La decoracion debe ser numérica.", "error")
                    return render_template(
                        "admin_recetas_nueva.html",
                        **contexto_receta
                    )

                if rol_f < 0:
                    flash("La decoracion no puede ser negativa.", "error")
                    return render_template(
                        "admin_recetas_nueva.html",
                        **contexto_receta
                    )

                if rol_f > cant_f:
                    flash("La decoracion no puede ser mayor que la cantidad.", "error")
                    return render_template(
                        "admin_recetas_nueva.html",
                        **contexto_receta
                    )

            filas_validas.append(
                (
                    int(ing_id),
                    cant_f,
                    rol_f,
                    unidad_id,
                    unidad_id
                )
            )

        if not filas_validas:
            flash(
                "La receta debe tener al menos un ingrediente con cantidad > 0.", "error")
            return render_template(
                "admin_recetas_nueva.html",
                **contexto_receta
            )

        try:
            conn = get_connection()
            cur = conn.cursor()

            cur.execute(
                """
                INSERT INTO recetas_maestro
                (
                    plato_id,
                    raciones_base,
                    preparacion,
                    elaboracion,
                    presentacion,
                    nutricion
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    int(plato_id),
                    raciones_base_int,
                    preparacion,
                    elaboracion,
                    presentacion,
                    nutricion
                )
            )
            receta_id = cur.lastrowid

            for (ing_id, cant_f, rol_f, unidad_id, unidad_presentacion) in filas_validas:

                cantidad_canonica = normalizar(
                    ingrediente_id=ing_id,
                    cantidad=cant_f,
                    unidad_origen=unidad_id
                )

                cur.execute(
                    """
                    INSERT INTO recetas_ingredientes
                    (
                        receta_id,
                        ingrediente_id,
                        cantidad,
                        unidad_codigo_presentacion,
                        rol
                    )
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        receta_id,
                        ing_id,
                        cantidad_canonica,
                        unidad_presentacion,
                        rol_f
                    )
                )

            conn.commit()
            conn.close()

            flash("Receta creada correctamente.", "recetas")
            return redirect("/admin/recetas/listado")

        except Exception as e:
            import traceback

            print("=" * 70)
            print("ERROR GUARDANDO RECETA")
            traceback.print_exc()
            print("=" * 70)

    return render_template(
        "admin_recetas_nueva.html",
        **contexto_receta
    )


# ==================================================
# EDITAR RECETA (MASTER)
# ==================================================

@app.route("/admin/recetas/editar/<int:receta_id>", methods=["GET", "POST"])
def admin_recetas_editar(receta_id):

    platos = db_cargar_platos()
    ingredientes = cargar_ingredientes_con_unidad()

    unidades_por_ingrediente = {}

    for ingrediente in ingredientes:
        unidades_por_ingrediente[ingrediente["id"]] = (
            db_cargar_unidades_disponibles_por_ingrediente(
                ingrediente["id"]
            )
        )

    contexto_receta = {
        "platos": platos,
        "ingredientes": ingredientes,
        "unidades_por_ingrediente": unidades_por_ingrediente
    }

    # ==================================================
    # GUARDAR CAMBIOS DE RECETA
    # ==================================================

    if request.method == "POST":

        plato_id = request.form.get("plato_id", "").strip()
        raciones_base = request.form.get("raciones_base", "").strip()

        # NUEVO: textos de la receta
        preparacion = request.form.get("preparacion", "").strip()
        elaboracion = request.form.get("elaboracion", "").strip()
        presentacion = request.form.get("presentacion", "").strip()
        nutricion = request.form.get("nutricion", "").strip()

        if not plato_id:
            flash("Debe seleccionar un plato.", "error")
            return redirect(f"/admin/recetas/editar/{receta_id}")

        try:
            raciones_base_int = int(raciones_base)
            if raciones_base_int <= 0:
                flash("RACIONES BASE debe ser mayor que 0.", "error")
                return redirect(f"/admin/recetas/editar/{receta_id}")
        except:
            flash("RACIONES BASE debe ser numérico.", "error")
            return redirect(f"/admin/recetas/editar/{receta_id}")

        ingredientes_ids = request.form.getlist("ingrediente_id[]")
        cantidades = request.form.getlist("cantidad[]")
        roles = request.form.getlist("rol[]")
        unidades = request.form.getlist("unidad[]")

        vistos = set()
        filas_validas = []

        for i in range(len(ingredientes_ids)):
            ing_id = (ingredientes_ids[i] or "").strip()
            cant_txt = (cantidades[i] or "").strip()
            rol_txt = (roles[i] or "").strip()
            unidad_id = (unidades[i] if i < len(unidades) else "").strip()

            if not ing_id:
                continue

            if ing_id in vistos:
                flash("No se permiten ingredientes duplicados en la receta.", "error")
                return render_template(
                    "admin_recetas_editar.html"
                    ** contexto_receta
                )
            vistos.add(ing_id)

            try:
                cant_f = float(cant_txt)
            except:
                flash("La cantidad debe ser numérica.", "error")
                return render_template(
                    "admin_recetas_editar.html"
                    ** contexto_receta
                )

            if cant_f <= 0:
                flash(
                    "La cantidad debe ser mayor que 0 en todos los ingredientes.", "error")
                return render_template(
                    "admin_recetas_editar.html"
                    ** contexto_receta
                )

            if rol_txt == "":
                rol_f = 0.0
            else:
                try:
                    rol_f = float(rol_txt)
                except:
                    flash("La decoracion debe ser numérica.", "error")
                    return render_template(
                        "admin_recetas_editar.html"
                        ** contexto_receta
                    )

                if rol_f < 0:
                    flash("La decoracion no puede ser negativa.", "error")
                    return render_template(
                        "admin_recetas_editar.html"
                        ** contexto_receta
                    )

                if rol_f > cant_f:
                    flash("La decoracion no puede ser mayor que la cantidad.", "error")
                    return render_template(
                        "admin_recetas_editar.html"
                        ** contexto_receta
                    )

            filas_validas.append(
                (
                    int(ing_id),
                    cant_f,
                    rol_f,
                    unidad_id,
                    unidad_id
                )
            )

        if not filas_validas:
            flash("La receta no puede quedar sin ingredientes.", "error")
            return redirect(f"/admin/recetas/editar/{receta_id}")

        try:

            conn = get_connection()

            cur = conn.cursor()

            cur.execute(
                """
                UPDATE recetas_maestro
                SET plato_id=?,
                    raciones_base=?,
                    preparacion=?,
                    elaboracion=?,
                    presentacion=?,
                    nutricion=?
                WHERE id=?
                """,
                (
                    int(plato_id),
                    raciones_base_int,
                    preparacion,
                    elaboracion,
                    presentacion,
                    nutricion,
                    receta_id
                )
            )

            cur.execute(
                "DELETE FROM recetas_ingredientes WHERE receta_id=?",
                (receta_id,)
            )

            for ing_id, cant_f, rol_f, unidad_id, unidad_presentacion in filas_validas:

                cantidad_canonica = normalizar(
                    ingrediente_id=ing_id,
                    cantidad=cant_f,
                    unidad_origen=unidad_id
                )

                cur.execute(
                    """
                    INSERT INTO recetas_ingredientes
                    (
                        receta_id,
                        ingrediente_id,
                        cantidad,
                        unidad_codigo_presentacion,
                        rol
                    )
                    VALUES (?,?,?,?,?)
                    """,
                    (
                        receta_id,
                        ing_id,
                        cantidad_canonica,
                        unidad_presentacion,
                        rol_f
                    )
                )

            conn.commit()

            flash(
                "Receta actualizada correctamente.",
                "recetas"
            )

            return redirect("/admin/recetas/listado")

        except Exception as e:

            print("ERROR REAL AL GUARDAR:", repr(e))

            try:

                conn.rollback()

            except Exception as e2:

                print("ERROR EN ROLLBACK:", e2)

            flash(
                "Error al actualizar la receta.",
                "error"
            )

            return redirect(
                f"/admin/recetas/editar/{receta_id}"
            )

        finally:

            try:

                conn.close()

            except Exception as e:

                print("ERROR CERRANDO CONEXION:", e)

    # ==================================================
    # CARGAR RECETA PARA EDICIÓN
    # ==================================================

    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT
                r.id,
                r.plato_id,
                r.raciones_base,
                r.preparacion,
                r.elaboracion,
                r.presentacion,
                r.nutricion,
                p.nombre as plato_nombre
            FROM recetas_maestro r
            JOIN platos p ON p.id = r.plato_id
            WHERE r.id = ?
        """, (receta_id,))

        receta = cur.fetchone()

        if not receta:
            flash("Receta no encontrada.", "error")
            return redirect("/admin/recetas/listado")

        cur.execute("""
            SELECT ingrediente_id, cantidad, rol
            FROM recetas_ingredientes
            WHERE receta_id = ?
            ORDER BY id
        """, (receta_id,))

        ingredientes_receta = cur.fetchall()

        conn.close()

    except Exception as e:
        print("ERROR cargando receta:", e)
        flash("Error cargando receta.", "error")
        return redirect("/admin/recetas/listado")

    contexto_receta["receta"] = receta
    contexto_receta["ingredientes_receta"] = ingredientes_receta

    return render_template(
        "admin_recetas_editar.html",
        **contexto_receta
    )

# ==================================================
# BORRAR RECETA
# ==================================================


@app.route("/admin/recetas/borrar/<int:receta_id>", methods=["POST"])
def borrar_receta(receta_id):
    try:
        conn = get_connection()
        cur = conn.cursor()

        # =========================
        # RECUPERAR NOMBRE RECETA
        # =========================

        cur.execute("""
            SELECT p.nombre
            FROM recetas_maestro r
            JOIN platos p ON p.id = r.plato_id
            WHERE r.id = ?
        """, (receta_id,))

        receta = cur.fetchone()

        nombre_receta = "SIN NOMBRE"

        if receta:
            nombre_receta = receta["nombre"]
        # =========================
        # BORRAR RECETA
        # =========================

        cur.execute(
            "DELETE FROM recetas_ingredientes WHERE receta_id = ?",
            (receta_id,)
        )

        cur.execute(
            "DELETE FROM recetas_detalle WHERE receta_id = ?",
            (receta_id,)
        )

        cur.execute(
            "DELETE FROM recetas_maestro WHERE id = ?",
            (receta_id,)
        )

        conn.commit()
        conn.close()

        # =========================
        # MENSAJE VISUAL
        # =========================

        flash(
            Markup(
                f'Receta <span style="color:red;">"{nombre_receta}"</span> eliminada correctamente.'
            ),
            "success"
        )

    except Exception as e:
        print("ERROR borrando receta:", e)

        flash(
            "No se pudo borrar la receta.",
            "error"
        )

    return redirect("/admin/recetas/listado")


@app.route("/admin/recetas/toggle-publicacion/<int:receta_id>", methods=["POST"])
def toggle_publicacion_receta(receta_id):

    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            UPDATE recetas_maestro
            SET visible_web =
                CASE
                    WHEN visible_web = 1 THEN 0
                    ELSE 1
                END
            WHERE id = ?
        """, (receta_id,))

        conn.commit()
        conn.close()

        flash("Estado de publicación actualizado.", "recetas")

    except Exception as e:
        print("ERROR toggle publicación:", e)
        flash("No se pudo actualizar la publicación.", "error")

    return redirect("/admin/recetas/listado")


def escalar_ingredientes(ingredientes, raciones_base, raciones_nuevas):
    factor = raciones_nuevas / raciones_base
    resultado = []

    for ing in ingredientes:

        cantidad = float(ing.get("cantidad", 0) or 0)
        deco = float(ing.get("rol", 0) or 0)

        cantidad_escalada = round(cantidad * factor, 2)
        deco_escalado = round(deco * factor, 2)

        deco_escalado = min(deco_escalado, cantidad_escalada)

        cocina_escalada = round(max(cantidad_escalada - deco_escalado, 0), 2)

        nuevo = dict(ing)
        nuevo["cantidad_escalada"] = cantidad_escalada
        nuevo["deco_escalado"] = deco_escalado
        nuevo["cocina_escalada"] = cocina_escalada

        resultado.append(nuevo)

    return resultado


@app.route("/admin/nomencladores")
def ver_nomencladores():

    tipos = db_cargar_tipos_plato()
    unidades = db_cargar_unidades()
    ingredientes = db_cargar_ingredientes()
    platos = db_cargar_platos()
    expresiones_culinarias = db_cargar_expresiones_culinarias()

    return render_template(
        "admin_nomencladores.html",
        tipos=tipos,
        unidades=unidades,
        ingredientes=ingredientes,
        platos=platos,
        expresiones_culinarias=expresiones_culinarias
    )


@app.route("/contacto", methods=["GET", "POST"])
def contacto():

    if request.method == "POST":

        nombre = request.form.get("nombre", "").strip()
        correo = request.form.get("correo", "").strip()
        asunto = request.form.get("asunto", "").strip()
        mensaje = request.form.get("mensaje", "").strip()

        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        db_insertar_contacto(
            fecha,
            nombre,
            correo,
            asunto,
            mensaje
        )

        return render_template(
            "contacto_ok.html"
        )

        return redirect("/contacto")

    desde_admin = request.args.get("admin") == "1"

    return render_template(
        "contacto.html",
        desde_admin=desde_admin
    )


@app.route("/admin/contactos")
def admin_contactos():

    if "usuario" not in session:
        return redirect("/login")

    contactos = db_cargar_contactos()

    pendientes = sum(1 for c in contactos if not c["atendido"])

    return render_template(
        "admin_contactos.html",
        contactos=contactos,
        pendientes=pendientes
    )


@app.route("/admin/contactos/<int:contacto_id>")
def admin_contacto_detalle(contacto_id):

    if "usuario" not in session:
        return redirect("/login")

    contacto = db_cargar_contacto(contacto_id)

    if not contacto:
        abort(404)

    return render_template(
        "admin_contacto_detalle.html",
        contacto=contacto
    )


@app.route("/admin/contactos/<int:contacto_id>/atender")
def admin_contacto_atender(contacto_id):

    if "usuario" not in session:
        return redirect("/login")

    db_marcar_contacto_atendido(contacto_id)

    flash(
        "Contacto marcado como atendido.",
        "recetas"
    )

    return redirect("/admin/contactos")


@app.route("/test_motor_conversion")
def test_motor_conversion():

    ingrediente_id = 26      # cebolla

    cantidad_lb = 2.0

    print()
    print("===================================")
    print("PRUEBA DEL MOTOR DE CONVERSIÓN")
    print("===================================")

    cantidad_canonica = normalizar(
        ingrediente_id,
        cantidad_lb,
        "lb"
    )

    cantidad_representada = representar(
        ingrediente_id,
        cantidad_canonica,
        "CAN",
        "lb"
    )

    print()
    print("RESULTADO FINAL")
    print("cantidad inicial :", cantidad_lb, "lb")
    print("cantidad canónica:", cantidad_canonica)
    print("cantidad final   :", cantidad_representada, "lb")
    print()

    return (
        f"<h2>Prueba Motor de Conversión</h2>"
        f"<p>Inicial: {cantidad_lb} lb</p>"
        f"<p>Canónica: {cantidad_canonica}</p>"
        f"<p>Final: {cantidad_representada} lb</p>"
    )

# ==================================================
# EJECUCIÓN
# ==================================================


if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5000, debug=False)
