import json
import os

# --------------------------------------------------
# RUTAS BASE DEL PROYECTO
# --------------------------------------------------

BASE_DIR = BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data_compartida", "data")

RECETAS_DETALLE_FILE = os.path.join(DATA_DIR, "recetas_detalle_version.json")
RECETAS_FILE = os.path.join(DATA_DIR, "recetas.json")
INGREDIENTES_FILE = os.path.join(DATA_DIR, "ingredientes.json")
PLATOS_FILE = os.path.join(DATA_DIR, "platos.json")
UNIDADES_FILE = os.path.join(DATA_DIR, "unidades.json")
CONFIG_FILE = os.path.join(DATA_DIR, "config.json")
RECETAS_CATALOGO_FILE = os.path.join(DATA_DIR, "recetas_catalogo.json")
RECETAS_MAESTRO_FILE = os.path.join(DATA_DIR, "recetas_maestro.json")
RECETAS_ING_FILE = os.path.join(DATA_DIR, "recetas_ingredientes.json")

# --------------------------------------------------
# FUNCIONES DE SOPORTE
# --------------------------------------------------


def asegurar_directorio():
    """
    Garantiza que el directorio de datos exista.
    No valida contenido ni estructura de archivos.
    """
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


# --------------------------------------------------
# FUNCIONES PÚBLICAS DE PERSISTENCIA
# --------------------------------------------------


def cargar_datos(ruta, por_defecto):
    """
    Carga datos desde un archivo JSON.
    Si el archivo no existe o es inválido, devuelve el valor por defecto.
    """
    if not os.path.exists(ruta):
        return por_defecto

    try:
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return por_defecto


def guardar_datos(ruta, datos):
    """
    Guarda datos en un archivo JSON.
    No valida estructura ni contenido de los datos.
    """
    asegurar_directorio()
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)


# --------------------------------------------------
# NOMENCLADORES — PLATOS / INGREDIENTES / UNIDADES
# --------------------------------------------------

def cargar_platos():
    print(">>> LEYENDO PLATOS DESDE:", PLATOS_FILE)
    return cargar_datos(PLATOS_FILE, [])


def guardar_platos(platos):
    guardar_datos(PLATOS_FILE, platos)


def cargar_ingredientes():
    return cargar_datos(INGREDIENTES_FILE, [])


def guardar_ingredientes(ingredientes):
    guardar_datos(INGREDIENTES_FILE, ingredientes)


def cargar_unidades():
    return cargar_datos(UNIDADES_FILE, [])


def guardar_unidades(unidades):
    guardar_datos(UNIDADES_FILE, unidades)        


# --------------------------------------------------
# NUEVO MODELO DE RECETAS (CATÁLOGO + MAESTRO)
# --------------------------------------------------

def cargar_recetas_catalogo():
    return cargar_datos(RECETAS_CATALOGO_FILE, [])


def cargar_recetas_maestro():

    print(">>> LEYENDO RECETAS DESDE:", RECETAS_MAESTRO_FILE)

    datos = cargar_datos(RECETAS_MAESTRO_FILE, [])

    print(">>> TOTAL RECETAS LEIDAS:", len(datos))

    return datos


def cargar_versiones_activas():
    maestro = cargar_recetas_maestro()
    return [r for r in maestro if r.get("estado") == "activa"]


def cargar_recetas_operativas():
    """
    Devuelve recetas listas para usar en GUI y cálculo:
    combina catálogo + versión activa
    """
    catalogo = cargar_recetas_catalogo()
    versiones = cargar_versiones_activas()

    recetas = []

    for v in versiones:
        plato = next((c for c in catalogo if c["id"] == v["receta_id"]), None)
        if not plato:
            continue

        receta = {
            "receta_maestro_id": v["id"],
            "receta_id": plato["id"],
            "nombre": plato["nombre"],
            "tipo_plato": plato.get("tipo_plato", ""),
            "version": v["version"],
            "raciones_base": v["raciones_base"],
            "peso_racion": v.get("peso_racion", 0),
        }

        recetas.append(receta)

    return recetas

# --------------------------------------------------
# DETALLE DE RECETA — TEXTO TÉCNICO POR VERSIÓN
# --------------------------------------------------

def cargar_detalle_receta(receta_maestro_id):
    """
    Devuelve el detalle técnico de una receta por versión.
    Si no existe, devuelve un diccionario vacío.
    """
    detalles = cargar_datos(RECETAS_DETALLE_FILE, [])

    for d in detalles:
        if d.get("receta_maestro_id") == receta_maestro_id:
            return d

    return {}

# --------------------------------------------------
# INGREDIENTES DE RECETA — COMPOSICIÓN POR VERSIÓN
# --------------------------------------------------

def cargar_ingredientes_receta(receta_maestro_id):
    """
    Devuelve la lista de ingredientes asociados a una versión de receta.
    Si no existen, devuelve una lista vacía.
    """
    ingredientes = cargar_datos(RECETAS_ING_FILE, [])

    return [
        i for i in ingredientes
        if i.get("receta_maestro_id") == receta_maestro_id
    ]

def guardar_detalle_receta(receta_maestro_id, datos):
    """
    Guarda o actualiza el detalle técnico de una receta por versión.
    """
    detalles = cargar_datos(RECETAS_DETALLE_FILE, [])

    # eliminar detalle previo de esa versión (si existe)
    detalles = [
        d for d in detalles
        if d.get("receta_maestro_id") != receta_maestro_id
    ]

    datos_guardar = dict(datos)
    datos_guardar["receta_maestro_id"] = receta_maestro_id

    detalles.append(datos_guardar)

    guardar_datos(RECETAS_DETALLE_FILE, detalles)



