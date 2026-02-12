from flask import Flask, render_template, request, redirect, flash

# --------------------------------------------------
# CAPA DE PERSISTENCIA (CENTRALIZADA)
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

app = Flask(__name__)
app.secret_key = "recetas_app_clave_segura_temporal"

# ==================================================
# UTILIDAD — INGREDIENTES CON UNIDAD
# ==================================================

def cargar_ingredientes_con_unidad():
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
    recetas = cargar_recetas_maestro()
    return render_template("index.html", recetas=recetas)


# ==================================================
# ADMIN PLATOS
# ==================================================

@app.route("/admin/platos", methods=["GET", "POST"])
def admin_platos():

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
                and p["tipo_plato"].lower() == tipo_plato.lower()
            ):
                errores.append("Plato duplicado (nombre + tipo).")

        if errores:
            platos = sorted(platos, key=lambda p: p["nombre"].lower())
            return render_template("admin_platos.html", platos=platos, errores=errores)

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
    return render_template("admin_platos.html", platos=platos, errores=[])


# =======================================
#        BORRAR PLATO (CON VALIDACIÓN)
# =======================================

@app.route("/admin/platos/borrar/<int:plato_id>", methods=["POST"])
def borrar_plato(plato_id):

    platos = cargar_platos()
    recetas = cargar_recetas_maestro()

    plato = next((p for p in platos if p.get("id") == plato_id), None)
    nombre_plato = plato["nombre"] if plato else f"(id {plato_id})"

    # ¿Está el plato usado en alguna receta?
    usado = any(r.get("plato_id") == plato_id for r in recetas)

    if usado:
        flash(
            f"No se puede borrar el plato <span style='color:#004aad; font-weight:bold;'>{nombre_plato}</span> porque está asociado a una receta.",
            "error"
        )
        return redirect("/admin/platos")

    # Borrado permitido
    platos_filtrados = [p for p in platos if p.get("id") != plato_id]

    guardar_platos(platos_filtrados)

    flash(
        f"Plato <span style='color:#004aad; font-weight:bold;'>{nombre_plato}</span> borrado correctamente.",
        "ok"
    )
    return redirect("/admin/platos")


# ==================================================
# ADMIN UNIDADES
# ==================================================

@app.route("/admin/unidades", methods=["GET", "POST"])
def admin_unidades():

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

    unidades = cargar_unidades()
    unidades = sorted(unidades, key=lambda u: u["nombre"].lower())

    return render_template(
        "admin_ingredientes.html",
        ingredientes=ingredientes,
        unidades=unidades
    )


@app.route("/admin/ingredientes/crear", methods=["POST"])
def crear_ingrediente():

    nombre = request.form.get("nombre", "").strip()
    unidad_id_txt = request.form.get("unidad_id", "").strip()

    errores = []

    if not nombre:
        errores.append("Debe teclear el nombre.")

    try:
        unidad_id = int(unidad_id_txt)
    except:
        errores.append("Unidad inválida.")

    ingredientes = cargar_ingredientes()
    unidades = cargar_unidades()

    if unidad_id_txt and not any(u["id"] == unidad_id for u in unidades):
        errores.append("Unidad no existe.")

    if any(i["nombre"].upper() == nombre.upper() for i in ingredientes):
        errores.append("Ingrediente duplicado.")

    if errores:
        ingredientes = cargar_ingredientes_con_unidad()
        return render_template(
            "admin_ingredientes.html",
            ingredientes=ingredientes,
            unidades=unidades,
            error=" | ".join(errores)
        )

    nuevo_id = max([i["id"] for i in ingredientes], default=0) + 1

    ingredientes.append({
        "id": nuevo_id,
        "nombre": nombre.upper(),
        "unidad_id": unidad_id
    })

    guardar_ingredientes(ingredientes)
    return redirect("/admin/ingredientes")


# ==================================================
# ADMIN RECETAS — MASTER
# ==================================================

@app.route("/admin/recetas", methods=["GET", "POST"])
def admin_recetas():

    import json

    platos = sorted(cargar_platos(), key=lambda p: p["nombre"].lower())
    ingredientes = sorted(cargar_ingredientes_con_unidad(), key=lambda i: i["nombre"].lower())
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
    error = None

    limpiar_form = False

    if request.method == "POST":

        plato_id_txt = request.form.get("plato_id", "").strip()
        raciones_txt = request.form.get("raciones_base", "").strip()
        ingredientes_json = request.form.get("ingredientes_json", "").strip()

        if not plato_id_txt:
            error = "Debe seleccionar un plato."
        elif not raciones_txt:
            error = "Debe indicar raciones base."
        else:
            try:
                plato_id = int(plato_id_txt)
                raciones_base = int(raciones_txt)
            except:
                error = "Datos numéricos inválidos."

        lista_ingredientes = []

        if not error and ingredientes_json:
            try:
                lista_ingredientes = json.loads(ingredientes_json)
            except:
                error = "Error leyendo ingredientes."

        # -------------------------------------------------
        # VALIDACIÓN DE DUPLICIDAD POR PLATO (REGLA MASTER)
        # -------------------------------------------------
        if not error:
            for r in recetas:
                try:
                    plato_id_existente = int(r.get("plato_id"))
                except:
                    continue

                print("DEBUG DUPLICIDAD -> existente:", plato_id_existente, "nuevo:", plato_id)

                if plato_id_existente == plato_id:
                    nombre_plato = mapa_platos.get(plato_id, "")
                    error = f"YA EXISTE LA RECETA {nombre_plato}"
                    limpiar_form = True   # bandera para limpiar todo en el HTML
                    break

        if not error:

            nuevo_id = max([r["id"] for r in recetas], default=0) + 1

            recetas.append({
                "id": nuevo_id,
                "plato_id": plato_id,
                "raciones_base": raciones_base,
                "preparacion": request.form.get("preparacion", ""),
                "elaboracion": request.form.get("elaboracion", ""),
                "presentacion": request.form.get("presentacion", ""),
                "nutricion": request.form.get("nutricion", ""),
                "ingredientes": lista_ingredientes
            })

            guardar_datos(RECETAS_MAESTRO_FILE, recetas)
            return redirect("/admin/recetas")

    return render_template(
        "admin_recetas.html",
        platos=platos,
        ingredientes=ingredientes,
        recetas=recetas_listado,
        error=error,
        limpiar_form=limpiar_form
    )


# ==================================================
# BORRAR RECETA MASTER
# ==================================================

@app.route("/admin/recetas/borrar/<int:receta_id>", methods=["POST"])
def borrar_receta_master(receta_id):

    recetas = cargar_recetas_maestro()
    recetas = [r for r in recetas if r["id"] != receta_id]

    guardar_datos(RECETAS_MAESTRO_FILE, recetas)
    return redirect("/admin/recetas/listado")


# ==================================================
# VER RECETA MASTER — DETALLE
# ==================================================

@app.route("/admin/recetas/<int:receta_id>", methods=["GET"])
def ver_receta_master(receta_id):

    recetas = cargar_recetas_maestro()
    receta = next((r for r in recetas if r.get("id") == receta_id), None)

    if not receta:
        return "Receta MASTER no encontrada", 404

    platos = cargar_platos()
    ingredientes_cat = cargar_ingredientes_con_unidad()

    plato = next((p for p in platos if p["id"] == receta["plato_id"]), None)
    nombre_plato = plato["nombre"] if plato else "—"

    mapa_ing = {i["id"]: i for i in ingredientes_cat}

    ingredientes_detalle = []
    for ing in receta.get("ingredientes", []):
        cat = mapa_ing.get(ing.get("ingrediente_id"))
        ingredientes_detalle.append({
            "nombre": cat["nombre"] if cat else "—",
            "cantidad": ing.get("cantidad", ""),
            "unidad": cat["unidad_codigo"] if cat else ""
        })

    return render_template(
        "admin_receta_detalle.html",
        receta=receta,
        nombre_plato=nombre_plato,
        ingredientes=ingredientes_detalle
    )


# ==================================================
#       ADMIN_RECETAS_LISTADO DEL MASTER
# ==================================================

@app.route("/admin/recetas/listado", methods=["GET"])
def admin_recetas_listado():

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
# EJECUCIÓN
# ==================================================

if __name__ == "__main__":
    app.run(debug=True)