# Archivo: modulo_web/persistencia_db.py

import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "recetas.db"


def get_connection():

    conn = sqlite3.connect(
        DB_PATH,
        timeout=30
    )

    conn.row_factory = sqlite3.Row

    conn.execute(
        "PRAGMA foreign_keys = ON;"
    )

    return conn


def init_db():

    conn = get_connection()
    cur = conn.cursor()

    # ----------------------------
    # TABLAS BASE
    # ----------------------------

    cur.execute("""
    CREATE TABLE IF NOT EXISTS tipos_plato (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL UNIQUE
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS platos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL UNIQUE,
        tipo_plato_id INTEGER,
        activo INTEGER NOT NULL DEFAULT 1,
        peso_racion REAL,
        foto TEXT,
        FOREIGN KEY (tipo_plato_id) REFERENCES tipos_plato(id)
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS unidades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo TEXT NOT NULL UNIQUE,
        nombre TEXT NOT NULL
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS ingredientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL UNIQUE,
        unidad_id INTEGER NOT NULL,
        activo INTEGER NOT NULL DEFAULT 1,
        FOREIGN KEY (unidad_id) REFERENCES unidades(id)
    );
    """)

    # ----------------------------
    # TABLAS DEL MASTER DE RECETAS
    # ----------------------------

    cur.execute("""
    CREATE TABLE IF NOT EXISTS recetas_maestro (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           plato_id INTEGER NOT NULL,
           raciones_base INTEGER NOT NULL,
           preparacion TEXT,
           elaboracion TEXT,
           presentacion TEXT,
           nutricion TEXT,
           visible_web INTEGER NOT NULL DEFAULT 1,
           FOREIGN KEY (plato_id) REFERENCES platos(id)
    );
    """)

    try:
        cur.execute("""
            ALTER TABLE recetas_maestro
            ADD COLUMN visible_web INTEGER NOT NULL DEFAULT 1;
        """)
    except sqlite3.OperationalError:
        pass

    cur.execute("""
    CREATE TABLE IF NOT EXISTS recetas_ingredientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        receta_id INTEGER NOT NULL,
        ingrediente_id INTEGER NOT NULL,
        cantidad REAL NOT NULL,
        rol REAL NOT NULL,
        FOREIGN KEY (receta_id) REFERENCES recetas_maestro(id),
        FOREIGN KEY (ingrediente_id) REFERENCES ingredientes(id)
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS recetas_detalle (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        receta_id INTEGER NOT NULL UNIQUE,
        preparacion TEXT,
        elaboracion TEXT,
        presentacion TEXT,
        nutricion TEXT,
        FOREIGN KEY (receta_id) REFERENCES recetas_maestro(id)
    );
    """)

    # ----------------------------
    # CONTACTOS WEB
    # ----------------------------

    cur.execute("""
    CREATE TABLE IF NOT EXISTS contactos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TEXT NOT NULL,
        nombre TEXT NOT NULL,
        correo TEXT NOT NULL,
        asunto TEXT NOT NULL,
        mensaje TEXT NOT NULL,
        atendido INTEGER NOT NULL DEFAULT 0
    );
    """)

    conn.commit()
    conn.close()


# ==================================================
# FUNCIONES DE ESCRITURA
# ==================================================

def db_crear_receta(plato_id, raciones_base, textos, ingredientes):

    conn = get_connection()

    try:

        cur = conn.cursor()

        conn.execute("BEGIN")

        cur.execute(
            "INSERT INTO recetas_maestro (plato_id, raciones_base) VALUES (?, ?)",
            (int(plato_id), int(raciones_base))
        )

        receta_id = cur.lastrowid

        cur.execute(
            """
            INSERT INTO recetas_detalle (receta_id, preparacion, elaboracion, presentacion, nutricion)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                receta_id,
                textos.get("preparacion", ""),
                textos.get("elaboracion", ""),
                textos.get("presentacion", ""),
                textos.get("nutricion", ""),
            )
        )

        for it in ingredientes:

            cur.execute(
                """
                INSERT INTO recetas_ingredientes (receta_id, ingrediente_id, cantidad, rol)
                VALUES (?, ?, ?, ?)
                """,
                (
                    receta_id,
                    int(it["ingrediente_id"]),
                    float(it["cantidad"]),
                    float(it["rol"]),
                )
            )

        conn.commit()

        return receta_id

    except Exception:

        conn.rollback()

        raise

    finally:

        conn.close()


# ==================================================
# FUNCIONES DE LECTURA
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

    return [{"id": f["id"], "nombre": f["nombre"]} for f in filas]


def db_cargar_platos():

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""
        SELECT
            p.id,
            p.nombre,
            p.activo,
            p.peso_racion,
            p.foto,
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
            "tipo_nombre": f["tipo_plato"] or "",
            "activo": f["activo"],
            "peso_racion": f["peso_racion"] if f["peso_racion"] is not None else 0.0,
            "foto": f["foto"]

        })

    return resultado


def db_cargar_unidades():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, codigo, nombre FROM unidades ORDER BY nombre")

    filas = cur.fetchall()

    conn.close()

    return [{"id": f["id"], "codigo": f["codigo"], "nombre": f["nombre"]} for f in filas]


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

    return [{"id": f["id"], "nombre": f["nombre"], "unidad_id": f["unidad_id"]} for f in filas]


def db_cargar_recetas_maestro_listado():
    """
    Devuelve listado de recetas con:
    - cantidad_ingredientes
    - tiene_decoracion = 1 SOLO si existe algún ingrediente con rol > 0
    """

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""
        SELECT
            r.id,
            r.plato_id,
            p.nombre AS plato_nombre,
            r.raciones_base,
            r.visible_web,
            COUNT(ri.id) AS cantidad_ingredientes,
            MAX(
                CASE
                    WHEN CAST(IFNULL(ri.rol, 0) AS REAL) > 0 THEN 1
                    ELSE 0
                END
            ) AS tiene_decoracion

        FROM recetas_maestro r

        JOIN platos p
            ON p.id = r.plato_id

        LEFT JOIN recetas_ingredientes ri
            ON ri.receta_id = r.id

        GROUP BY
            r.id,
            r.plato_id,
            p.nombre,
            r.raciones_base

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

            "visible_web": f["visible_web"],

            "cantidad_ingredientes": f["cantidad_ingredientes"],

            "tiene_decoracion":
                f["tiene_decoracion"]
                if f["tiene_decoracion"] is not None
                else 0

        })

    return resultado


def db_cargar_recetas_publicadas():

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

        WHERE r.visible_web = 1

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

    cur.execute("""

        SELECT

            r.id,

            r.plato_id,

            r.raciones_base,

            r.preparacion,

            r.elaboracion,

            r.presentacion,

            r.nutricion,

            p.nombre AS plato_nombre,

            p.foto AS plato_foto

        FROM recetas_maestro r

        JOIN platos p ON p.id = r.plato_id

        WHERE r.id = ?

    """, (receta_id,))

    fila = cur.fetchone()

    if not fila:

        conn.close()

        return None

    receta = {

        "id": fila["id"],

        "plato_id": fila["plato_id"],

        "plato_nombre": fila["plato_nombre"],

        "plato_foto": fila["plato_foto"],

        "raciones_base": fila["raciones_base"],

        "preparacion": fila["preparacion"] or "",

        "elaboracion": fila["elaboracion"] or "",

        "presentacion": fila["presentacion"] or "",

        "nutricion": fila["nutricion"] or "",

        "textos": {

            "preparacion": fila["preparacion"] or "",

            "elaboracion": fila["elaboracion"] or "",

            "presentacion": fila["presentacion"] or "",

            "nutricion": fila["nutricion"] or ""

        },

        "ingredientes": []

    }

    cur.execute("""

        SELECT

            ri.ingrediente_id,

            i.nombre AS ingrediente_nombre,

            ri.cantidad,

            ri.rol,

            u.nombre AS unidad_nombre

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

            "rol": f["rol"],

            "unidad_nombre": f["unidad_nombre"]

        })

    return receta


def db_insertar_contacto(fecha, nombre, correo, asunto, mensaje):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""
        INSERT INTO contactos (
            fecha,
            nombre,
            correo,
            asunto,
            mensaje
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        fecha,
        nombre,
        correo,
        asunto,
        mensaje
    ))

    conn.commit()

    conn.close()


# ================================
#
#    CARGAR CONTACTO EN GENERAL
#
# ================================


def db_cargar_contactos():

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""
        SELECT
            id,
            fecha,
            nombre,
            correo,
            asunto,
            atendido
        FROM contactos
        ORDER BY id DESC
    """)

    filas = cur.fetchall()

    conn.close()

    return filas


# ================================
#
#    CARGAR CONTACTO ESPECIFICO
#
# ================================


def db_cargar_contacto(contacto_id):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""
        SELECT
            id,
            fecha,
            nombre,
            correo,
            asunto,
            mensaje,
            atendido
        FROM contactos
        WHERE id = ?
    """, (contacto_id,))

    fila = cur.fetchone()

    conn.close()

    return fila


def db_listar_contactos():

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""
        SELECT
            id,
            fecha,
            nombre,
            correo,
            asunto,
            mensaje,
            atendido
        FROM contactos
        ORDER BY id DESC
    """)

    filas = cur.fetchall()

    conn.close()

    return filas


def db_marcar_contacto_atendido(contacto_id):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""
        UPDATE contactos
        SET atendido = 1
        WHERE id = ?
    """, (contacto_id,))

    conn.commit()

    conn.close()


def db_cargar_equivalencias(ingrediente_id):

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""

        SELECT
            e.id,
            e.factor,
            u.id as unidad_id,
            u.codigo,
            u.nombre

        FROM ingredientes_equivalencias e

        JOIN unidades u
            ON u.id = e.unidad_id

        WHERE e.ingrediente_id = ?

        ORDER BY u.nombre

    """, (ingrediente_id,))

    filas = cur.fetchall()

    conn.close()

    return filas


def db_insertar_equivalencia(
    ingrediente_id,
    unidad_id,
    factor
):

    conn = get_connection()

    try:

        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO ingredientes_equivalencias
            (
                ingrediente_id,
                unidad_id,
                factor
            )
            VALUES (?, ?, ?)
            """,
            (
                ingrediente_id,
                unidad_id,
                factor
            )
        )

    except Exception as e:

        print("[RTN-016A] ERROR REAL EN INSERTAR EQUIVALENCIA:", repr(e))

        conn.rollback()

        raise

    finally:

        conn.close()


def db_borrar_equivalencia(equivalencia_id):

    conn = get_connection()

    try:
        cur = conn.cursor()

        cur.execute(
            """
            DELETE FROM ingredientes_equivalencias
            WHERE id = ?
            """,
            (equivalencia_id,)
        )

        conn.commit()

    except:
        conn.rollback()
        raise

    finally:
        conn.close()


if __name__ == "__main__":
    init_db()

# Fin del archivo: modulo_web/persistencia_db.py
