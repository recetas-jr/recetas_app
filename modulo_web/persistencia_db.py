import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "recetas.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # Tabla: tipos_plato
    cur.execute("""
    CREATE TABLE IF NOT EXISTS tipos_plato (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL UNIQUE
    );
    """)

    # Tabla: platos
    cur.execute("""
    CREATE TABLE IF NOT EXISTS platos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL UNIQUE,
        tipo_plato_id INTEGER,
        activo INTEGER NOT NULL DEFAULT 1,
        peso_racion REAL,
        FOREIGN KEY (tipo_plato_id) REFERENCES tipos_plato(id)
    );
    """)

    # Tabla: unidades
    cur.execute("""
    CREATE TABLE IF NOT EXISTS unidades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo TEXT NOT NULL UNIQUE,
        nombre TEXT NOT NULL
    );
    """)

    # Tabla: ingredientes
    cur.execute("""
    CREATE TABLE IF NOT EXISTS ingredientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL UNIQUE,
        unidad_id INTEGER NOT NULL,
        activo INTEGER NOT NULL DEFAULT 1,
        FOREIGN KEY (unidad_id) REFERENCES unidades(id)
    );
    """)

    # Tabla: recetas_maestro
    cur.execute("""
    CREATE TABLE IF NOT EXISTS recetas_maestro (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        plato_id INTEGER NOT NULL,
        raciones_base INTEGER NOT NULL,
        fecha_creacion TEXT,
        activo INTEGER NOT NULL DEFAULT 1,
        FOREIGN KEY (plato_id) REFERENCES platos(id)
    );
    """)

    # Tabla: recetas_ingredientes
    cur.execute("""
    CREATE TABLE IF NOT EXISTS recetas_ingredientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        receta_id INTEGER NOT NULL,
        ingrediente_id INTEGER NOT NULL,
        cantidad REAL NOT NULL,
        rol TEXT NOT NULL,
        FOREIGN KEY (receta_id) REFERENCES recetas_maestro(id),
        FOREIGN KEY (ingrediente_id) REFERENCES ingredientes(id)
    );
    """)

    # Tabla: recetas_detalle
    cur.execute("""
    CREATE TABLE IF NOT EXISTS recetas_detalle (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        receta_id INTEGER NOT NULL,
        preparacion TEXT,
        elaboracion TEXT,
        presentacion TEXT,
        nutricion TEXT,
        FOREIGN KEY (receta_id) REFERENCES recetas_maestro(id)
    );
    """)

    conn.commit()
    conn.close()


# ==================================================
# FUNCIONES DE LECTURA (DB → dicts)
# ==================================================

def db_cargar_tipos_plato():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, nombre
        FROM tipos_plato
        ORDER BY nombre
    """)
    filas = cur.fetchall()
    conn.close()

    return [
        {"id": f["id"], "nombre": f["nombre"]}
        for f in filas
    ]


def db_cargar_platos():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            p.id,
            p.nombre,
            p.activo,
            p.peso_racion,
            t.nombre AS tipo_plato
        FROM platos p
        LEFT JOIN tipos_plato t ON p.tipo_plato_id = t.id
        WHERE p.activo = 1
        ORDER BY p.nombre
    """)

    filas = cur.fetchall()
    conn.close()

    resultado = []
    for f in filas:
        resultado.append({
            "id": f["id"],
            "nombre": f["nombre"],
            "tipo_plato": f["tipo_plato"] or "",
            "activo": f["activo"],
            "peso_racion": f["peso_racion"] if f["peso_racion"] is not None else 0.0
        })

    return resultado


def db_cargar_unidades():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, codigo, nombre FROM unidades ORDER BY nombre")
    filas = cur.fetchall()
    conn.close()

    return [
        {"id": f["id"], "codigo": f["codigo"], "nombre": f["nombre"]}
        for f in filas
    ]


def db_cargar_ingredientes():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, nombre, unidad_id
        FROM ingredientes
        WHERE activo = 1
        ORDER BY nombre
    """)
    filas = cur.fetchall()
    conn.close()

    return [
        {"id": f["id"], "nombre": f["nombre"], "unidad_id": f["unidad_id"]}
        for f in filas
    ]


def db_cargar_recetas_maestro_listado():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            r.id,
            r.plato_id,
            p.nombre AS plato_nombre,
            r.raciones_base,
            COUNT(ri.id) AS cantidad_ingredientes
        FROM recetas_maestro r
        JOIN platos p ON p.id = r.plato_id
        LEFT JOIN recetas_ingredientes ri ON ri.receta_id = r.id
        WHERE r.activo = 1
        GROUP BY r.id, r.plato_id, p.nombre, r.raciones_base
        ORDER BY p.nombre
    """)

    filas = cur.fetchall()
    conn.close()

    resultado = []
    for f in filas:
        resultado.append({
            "id": f["id"],
            "plato_id": f["plato_id"],
            "plato_nombre": f["plato_nombre"],
            "raciones_base": f["raciones_base"],
            "cantidad_ingredientes": f["cantidad_ingredientes"]
        })

    return resultado


def db_cargar_receta_detalle(receta_id):
    conn = get_connection()
    cur = conn.cursor()

    # 1) Cargar cabecera de receta + plato
    cur.execute("""
        SELECT
            r.id,
            r.plato_id,
            r.raciones_base,
            p.nombre AS plato_nombre
        FROM recetas_maestro r
        JOIN platos p ON p.id = r.plato_id
        WHERE r.id = ? AND r.activo = 1
    """, (receta_id,))

    fila = cur.fetchone()
    if not fila:
        conn.close()
        return None

    receta = {
        "id": fila["id"],
        "plato_id": fila["plato_id"],
        "raciones_base": fila["raciones_base"],
        "plato_nombre": fila["plato_nombre"],
        "ingredientes": []
    }

    # 2) Cargar ingredientes de la receta
    cur.execute("""
        SELECT
            ri.ingrediente_id,
            i.nombre AS ingrediente_nombre,
            ri.cantidad,
            u.codigo AS unidad_codigo
        FROM recetas_ingredientes ri
        JOIN ingredientes i ON i.id = ri.ingrediente_id
        JOIN unidades u ON u.id = i.unidad_id
        WHERE ri.receta_id = ?
        ORDER BY i.nombre
    """, (receta_id,))

    filas_ing = cur.fetchall()
    conn.close()

    for f in filas_ing:
        receta["ingredientes"].append({
            "ingrediente_id": f["ingrediente_id"],
            "nombre": f["ingrediente_nombre"],
            "cantidad": f["cantidad"],
            "unidad": f["unidad_codigo"]
        })

    return receta


if __name__ == "__main__":
    init_db()
