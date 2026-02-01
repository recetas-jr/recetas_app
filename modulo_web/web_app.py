print("### ESTE ES EL WEB_APP QUE SE ESTA EJECUTANDO ###")

from flask import Flask, render_template, request, redirect, url_for

# --------------------------------------------------
# CAPA DE PERSISTENCIA (centralizada)
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

    cargar_recetas_catalogo,
    cargar_recetas_maestro,
    cargar_versiones_activas,
    cargar_recetas_operativas,
)

import persistencia
print("### WEB_APP EJECUTANDO DESDE:", __file__)
print("### PERSISTENCIA IMPORTADA DESDE:", persistencia.__file__)

app = Flask(__name__)

# =======================================
# CONFIGURACIÓN BÁSICA — SESIÓN / FLASH
# =======================================

app.secret_key = "recetas_app_clave_segura_temporal"

# =======================================
#  CARGAR INGREDIENTES CON UNIDAD (MASTER)
# =======================================

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


# ==============================
# INDEX — LISTADO DE RECETAS
# ==============================

@app.route("/", methods=["GET"])
def index():

    recetas = cargar_recetas_maestro()
    recetas = sorted(recetas, key=lambda r: r.get("nombre", ""))

    return render_template("index.html", recetas=recetas)

# =======================================
#        ADMIN PLATOS — GET (LISTADO)
# =======================================

@app.route("/admin/platos", methods=["GET"])
def admin_platos_get():

    platos = cargar_platos()
    platos = sorted(platos, key=lambda p: p["nombre"].lower())

    return render_template(
        "admin_platos.html",
        platos=platos,
        errores=[]
    )

# =======================================
#        ADMIN PLATOS — POST (GUARDAR)
# =======================================

@app.route("/admin/platos", methods=["POST"])
def admin_platos_post():

    platos = cargar_platos()
    errores = []

    nombre = request.form.get("nombre", "").strip()
    tipo_plato = request.form.get("tipo_plato", "").strip()
    peso_racion_txt = request.form.get("peso_racion", "").replace(",", ".")

    if not nombre:
        errores.append("Nombre del plato es obligatorio.")

    if not tipo_plato:
        errores.append("Tipo de plato es obligatorio.")

    try:
        peso_racion = float(peso_racion_txt)
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
        return render_template(
            "admin_platos.html",
            platos=platos,
            errores=errores
        )

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


# =======================================
#         ADMIN UNIDADES
# =======================================

@app.route("/admin/unidades", methods=["GET", "POST"])
def admin_unidades():

    unidades = cargar_unidades()
    errores = []

    if request.method == "POST":

        codigo = request.form.get("codigo", "").strip().upper()
        nombre = request.form.get("nombre", "").strip()

        if not codigo:
            errores.append("Debe teclear el código de la unidad de medida.")
        elif not codigo.isalpha():
            errores.append("El código solo puede contener letras.")
        elif len(codigo) not in (1, 2):
            errores.append("El código debe tener 1 o 2 letras.")

        if not nombre:
            errores.append("Debe teclear el nombre de la unidad de medida.")

        for u in unidades:
            if u["codigo"].upper() == codigo:
                errores.append(f"Código '{codigo}' ya existe.")
            if u["nombre"].upper() == nombre.upper():
                errores.append(f"Nombre '{nombre}' ya existe.")

        if errores:
            return render_template(
                "admin_unidades.html",
                unidades=unidades,
                errores=errores
            )

        nuevo_id = max([u["id"] for u in unidades], default=0) + 1

        unidades.append({
            "id": nuevo_id,
            "codigo": codigo,
            "nombre": nombre
        })

        guardar_unidades(unidades)

        return redirect("/admin/unidades")

    return render_template("admin_unidades.html", unidades=unidades)


# =======================================
#        ADMIN INGREDIENTES — NOMENCLADOR
# =======================================

@app.route("/admin/ingredientes")
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
        errores.append("Debe teclear el nombre del ingrediente.")

    try:
        unidad_id = int(unidad_id_txt)
    except:
        errores.append("Debe seleccionar una unidad de medida válida.")

    ingredientes = cargar_ingredientes()
    unidades = cargar_unidades()

    if unidad_id_txt:
        if not any(u["id"] == unidad_id for u in unidades):
            errores.append("La unidad de medida seleccionada no existe.")

    nombre_norm = nombre.upper()
    for i in ingredientes:
        if i["nombre"].upper() == nombre_norm:
            errores.append(f"Ingrediente duplicado: {nombre}")

    if errores:
        ingredientes = sorted(ingredientes, key=lambda x: x["nombre"])
        return render_template(
            "admin_ingredientes.html",
            ingredientes=ingredientes,
            unidades=unidades,
            error=" | ".join(errores)
        )

    nuevo_id = max([i["id"] for i in ingredientes], default=0) + 1

    ingredientes.append({
        "id": nuevo_id,
        "nombre": nombre_norm,
        "unidad_id": unidad_id
    })

    guardar_ingredientes(ingredientes)

    return redirect("/admin/ingredientes")


# =======================================
#         ADMIN RECETAS — MASTER
# =======================================

@app.route("/admin/recetas", methods=["GET", "POST"])
def admin_recetas():

    import json

    platos = cargar_platos()
    platos = sorted(platos, key=lambda p: p["nombre"].lower())

    ingredientes = cargar_ingredientes_con_unidad()
    ingredientes = sorted(ingredientes, key=lambda i: i["nombre"].lower())

    recetas = cargar_recetas_maestro()

    # -------------------------------------------------
    # CONSTRUIR LISTADO MASTER CON NOMBRE DE PLATO
    # Y ORDENAR ALFABÉTICAMENTE
    # -------------------------------------------------

    mapa_platos = {p["id"]: p["nombre"] for p in platos}

    recetas_listado = []
    for r in recetas:
        recetas_listado.append({
            "id": r["id"],
            "plato_id": r["plato_id"],
            "plato_nombre": mapa_platos.get(r["plato_id"], "—"),
            "raciones_base": r.get("raciones_base", 0)
        })

    recetas_listado = sorted(
        recetas_listado,
        key=lambda r: r["plato_nombre"].lower()
    )

    error = None

    # -----------------------------
    # POST — GUARDAR RECETA MASTER
    # -----------------------------
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
                error = "Error leyendo lista de ingredientes."

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

            guardar_datos("recetas_maestro.json", recetas)

            return redirect("/admin/recetas")

    return render_template(
        "admin_recetas.html",
        platos=platos,
        ingredientes=ingredientes,
        recetas=recetas_listado,
        error=error
    )


# =======================================
#     VER RECETA MASTER — DETALLE
# =======================================

@app.route("/admin/recetas/<int:receta_id>", methods=["GET"])
def ver_receta_master(receta_id):

    recetas = cargar_recetas_maestro()

    receta = next((r for r in recetas if r.get("id") == receta_id), None)

    if not receta:
        return "Receta MASTER no encontrada", 404

    platos = cargar_platos()
    ingredientes_cat = cargar_ingredientes_con_unidad()

    plato = next((p for p in platos if p["id"] == receta.get("plato_id")), None)
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


# =======================================
#     ELIMINAR RECETA MASTER
# =======================================

@app.route("/admin/recetas/<int:receta_id>/eliminar", methods=["GET"])
def eliminar_receta_master(receta_id):

    import json
    import os

    print("### ENTRÓ A eliminar_receta_master CON ID:", receta_id)

    recetas = cargar_recetas_maestro()
    print("### TOTAL ANTES:", len(recetas))

    recetas_filtradas = [r for r in recetas if r.get("id") != receta_id]
    print("### TOTAL DESPUÉS:", len(recetas_filtradas))

    base_dir = os.path.dirname(persistencia.__file__)
    ruta = os.path.abspath(
        os.path.join(base_dir, "data_compartida", "data", "recetas_maestro.json")
    )

    print("### GUARDANDO EN:", ruta)

    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(recetas_filtradas, f, indent=2, ensure_ascii=False)

    return redirect("/admin/recetas")


# =======================================
#     ELIMINAR UNIDAD DE MEDIDA (UM)
#     (CON VALIDACIÓN DE USO EN INGREDIENTES)
# =======================================

from flask import flash

@app.route("/admin/unidades/borrar", methods=["POST"])
def borrar_unidad():

    unidad_id = request.form.get("unidad_id")

    try:
        unidad_id = int(unidad_id)
    except:
        flash("Unidad inválida.", "error")
        return redirect("/admin/unidades")

    unidades = cargar_unidades()
    ingredientes = cargar_ingredientes()

    unidad = next((u for u in unidades if u.get("id") == unidad_id), None)
    if not unidad:
        flash("La unidad no existe.", "error")
        return redirect("/admin/unidades")

    # VALIDACIÓN: UM usada por algún ingrediente
    esta_usada = any(i.get("unidad_id") == unidad_id for i in ingredientes)

    if esta_usada:
        flash(
            f"No se puede borrar la unidad '{unidad['nombre']}' "
            f"porque está asociada a al menos un ingrediente.",
            "error"
        )
        return redirect("/admin/unidades")

    # BORRADO
    unidades_filtradas = [u for u in unidades if u.get("id") != unidad_id]
    guardar_unidades(unidades_filtradas)

    flash(
        f"La unidad '{unidad['nombre']}' fue borrada correctamente.",
        "ok"
    )

    return redirect("/admin/unidades")


# =======================================
#        ELIMINAR INGREDIENTE
# =======================================

@app.route("/admin/ingredientes/borrar/<int:ingrediente_id>", methods=["GET"])
def borrar_ingrediente(ingrediente_id):

    ingredientes = cargar_ingredientes()

    ingredientes_filtrados = [
        i for i in ingredientes if i.get("id") != ingrediente_id
    ]

    guardar_ingredientes(ingredientes_filtrados)

    return redirect("/admin/ingredientes")



# =======================================
#            EJECUCIÓN SERVIDOR
# =======================================

if __name__ == "__main__":
    app.run(debug=True)