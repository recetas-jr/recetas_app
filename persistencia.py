import json
import os
import sqlite3
from pathlib import Path

# --------------------------------------------------
# RUTAS BASE DEL PROYECTO
# --------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
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

# SQLite
DB_PATH = Path(BASE_DIR) / "modulo_web" / "recetas.db"

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


def get_db_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


# --------------------------------------------------
# FUNCIONES PÚBLICAS DE PERSISTENCIA (JSON)
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
    """
    Lee platos desde SQLite. Si algo falla, cae a JSON.
    """
    try:
        conn = get_db_conn()
        cur = conn.cursor()
        cur.execute("""
            SELECT
                p.id,
                p.nombre,
                tp.nombre AS tipo_plato,
                p.activo,
                p.peso_racion
            FROM platos p
            LEFT JOIN tipos_plato tp ON tp.id = p.tipo_plato_id
            ORDER BY p.nombre;
        """)
        filas = cur.fetchall()
        conn.close()

        platos = []
        for r in filas:
            platos.append({
                "id": r["id"],
                "nombre": r["nombre"],
                "tipo_plato": r["tipo_plato"] or "",
                "activo": bool(r["activo"]),
                "peso_racion": r["peso_racion"] if r["peso_racion"] is not None else 0.0,
                "foto": ""
            })

        print(">>> LEYENDO PLATOS DESDE: SQLite")
        return platos
    except Exception as e:
        print(">>> ERROR DB, usando JSON para platos:", e)
        print(">>> LEYENDO PLATOS DESDE:", PLATOS_FILE)
        return cargar_datos(PLATOS_FILE, [])


def guardar_platos(platos):
    guardar_datos(PLATOS_FILE, platos)


def cargar_unidades():
    """
    Lee unidades desde SQLite. Si algo falla, cae a JSON.
    """
    try:
        conn = get_db_conn()
        cur = conn.cursor()
        cur.execute("""
            SELECT id, codigo, nombre
            FROM unidades
            ORDER BY codigo;
        """)
        filas = cur.fetchall()
        conn.close()

        unidades = []
        for r in filas:
            unidades.append({
                "id": r["id"],
                "codigo": r["codigo"],
                "nombre": r["nombre"],
            })

        print(">>> LEYENDO UNIDADES DESDE: SQLite")
        return unidades
    except Exception as e:
        print(">>> ERROR DB, usando JSON para unidades:", e)
        print(">>> LEYENDO UNIDADES DESDE:", UNIDADES_FILE)
        return cargar_datos(UNIDADES_FILE, [])


def guardar_unidades(unidades):
    guardar_datos(UNIDADES_FILE, unidades)


def cargar_ingredientes():
    """
    TERCER SWITCH A DB:
    Lee ingredientes desde SQLite (con su unidad_id).
    Si algo falla, cae a JSON.
    """
    try:
        conn = get_db_conn()
        cur = conn.cursor()
        cur.execute("""
            SELECT i.id, i.nombre, i.unidad_id, i.activo
            FROM ingredientes i
            ORDER BY i.nombre;
        """)
        filas = cur.fetchall()
        conn.close()

        ingredientes = []
        for r in filas:
            ingredientes.append({
                "id": r["id"],
                "nombre": r["nombre"],
                "unidad_id": r["unidad_id"],
                "activo": bool(r["activo"]),
            })

        print(">>> LEYENDO INGREDIENTES DESDE: SQLite")
        return ingredientes
    except Exception as e:
        print(">>> ERROR DB, usando JSON para ingredientes:", e)
        print(">>> LEYENDO INGREDIENTES DESDE:", INGREDIENTES_FILE)
        return cargar_datos(INGREDIENTES_FILE, [])


def guardar_ingredientes(ingredientes):
    guardar_datos(INGREDIENTES_FILE, ingredientes)


# --------------------------------------------------
# NUEVO MODELO DE RECETAS (CATÁLOGO + MAESTRO)
# --------------------------------------------------

def cargar_recetas_catalogo():
    return cargar_datos(RECETAS_CATALOGO_FILE, [])


def cargar_recetas_maestro():

    print("🔥🔥🔥 ENTRO A SQLITE 🔥🔥🔥")

    """
    Lee recetas desde SQLite.
    Si falla, usa JSON.
    """
    try:
        conn = get_db_conn()
        cur = conn.cursor()

        cur.execute("""
            SELECT id, plato_id, raciones_base, preparacion, elaboracion, presentacion, nutricion
            FROM recetas_maestro
        """)

        filas = cur.fetchall()
        conn.close()

        recetas = []
        for r in filas:
            recetas.append({
                "id": r["id"],
                "receta_id": r["receta_id"],
                "version": r["version"],
                "raciones_base": r["raciones_base"],
                "estado": r["estado"],
                "peso_racion": r["peso_racion"]
            })

        print(">>> LEYENDO RECETAS DESDE: SQLite")
        print(">>> TOTAL RECETAS LEIDAS:", len(recetas))

        return recetas

    except Exception as e:
        print(">>> ERROR DB, usando JSON:", e)
        print(">>> LEYENDO RECETAS DESDE:", RECETAS_MAESTRO_FILE)
        return cargar_datos(RECETAS_MAESTRO_FILE, [])


def cargar_versiones_activas():
    maestro = cargar_recetas_maestro()
    return [r for r in maestro if r.get("estado") == "activa"]


def cargar_recetas_operativas():
    catalogo = cargar_recetas_catalogo()
    versiones = cargar_versiones_activas()

    recetas = []

    for v in versiones:
        print("DEBUG VERSION:", v)

        plato = next((c for c in catalogo if c["id"] == v["receta_id"]), None)

        print("DEBUG PLATO:", plato)

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

    print("DEBUG RESULTADO FINAL:", recetas)

    return recetas
# --------------------------------------------------
# DETALLE DE RECETA — TEXTO TÉCNICO POR VERSIÓN
# --------------------------------------------------


def cargar_detalle_receta(receta_maestro_id):
    detalles = cargar_datos(RECETAS_DETALLE_FILE, [])
    for d in detalles:
        if d.get("receta_maestro_id") == receta_maestro_id:
            return d
    return {}

# --------------------------------------------------
# INGREDIENTES DE RECETA — COMPOSICIÓN POR VERSIÓN
# --------------------------------------------------


def cargar_ingredientes_receta(receta_maestro_id):
    ingredientes = cargar_datos(RECETAS_ING_FILE, [])
    return [
        i for i in ingredientes
        if i.get("receta_maestro_id") == receta_maestro_id
    ]


def guardar_detalle_receta(receta_maestro_id, datos):
    detalles = cargar_datos(RECETAS_DETALLE_FILE, [])
    detalles = [
        d for d in detalles
        if d.get("receta_maestro_id") != receta_maestro_id
    ]
    datos_guardar = dict(datos)
    datos_guardar["receta_maestro_id"] = receta_maestro_id
    detalles.append(datos_guardar)
    guardar_datos(RECETAS_DETALLE_FILE, detalles)


def traer_recetas_para_web():
    recetas_db = cargar_recetas_operativas()

    recetas_web = []

    for r in recetas_db:
        receta_id = r["receta_maestro_id"]

        detalle = cargar_detalle_receta(receta_id)
        ingredientes_db = cargar_ingredientes_receta(receta_id)

        ingredientes = []

        for ing in ingredientes_db:
            ingredientes.append({
                "nombre": ing.get("nombre", ""),
                "cantidad": ing.get("cantidad", 0),
                "unidad": ing.get("unidad", "")
            })

        recetas_web.append({
            "id": receta_id,
            "nombre": r.get("nombre", ""),
            "raciones_base": detalle.get("raciones", 1) if detalle else 1,
            "ingredientes": ingredientes
        })

    return recetas_web


def publicar_a_web():
    recetas = traer_recetas_para_web()

    ruta = os.path.join(BASE_DIR, "modulo_web", "web_data",
                        "recetas_publicadas.json")

    guardar_datos(ruta, recetas)

    print("✅ RECETAS PUBLICADAS A WEB")
