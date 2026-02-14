import json
from pathlib import Path
import sqlite3

# ==============================
# RUTAS REALES A TUS JSON (FUENTE DE VERDAD)
# ==============================
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = (BASE_DIR / ".." / "data_compartida" / "data").resolve()

JSON_PLATOS = DATA_DIR / "platos.json"
JSON_UNIDADES = DATA_DIR / "unidades.json"
JSON_INGREDIENTES = DATA_DIR / "ingredientes.json"
JSON_RECETAS_CATALOGO = DATA_DIR / "recetas_catalogo.json"
JSON_RECETAS_MAESTRO = DATA_DIR / "recetas_maestro.json"
JSON_RECETAS_ING = DATA_DIR / "recetas_ingredientes.json"

DB_PATH = BASE_DIR / "recetas.db"


def load_json(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"No existe el archivo: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def ensure_tipos_from_platos(cur, platos):
    for p in platos:
        tipo = p.get("tipo_plato") or ""
        if tipo:
            cur.execute(
                "INSERT OR IGNORE INTO tipos_plato(nombre) VALUES (?);",
                (tipo,)
            )


def upsert_unidades(cur, unidades):
    for u in unidades:
        codigo = u.get("codigo")
        nombre = u.get("nombre") or codigo
        cur.execute(
            "INSERT OR IGNORE INTO unidades(codigo, nombre) VALUES (?, ?);",
            (codigo, nombre)
        )


def upsert_platos(cur, platos):
    """
    Inserta platos y devuelve un mapa: id_json -> id_sqlite
    """
    mapa = {}

    for p in platos:
        nombre = p["nombre"]
        tipo = p.get("tipo_plato") or None

        tipo_id = None
        if tipo:
            row = cur.execute(
                "SELECT id FROM tipos_plato WHERE nombre = ?;",
                (tipo,)
            ).fetchone()
            if row:
                tipo_id = row["id"]

        cur.execute(
            "INSERT OR IGNORE INTO platos(nombre, tipo_plato_id, activo) VALUES (?, ?, 1);",
            (nombre, tipo_id)
        )

        row = cur.execute(
            "SELECT id FROM platos WHERE nombre = ?;",
            (nombre,)
        ).fetchone()

        mapa[p["id"]] = row["id"]

    return mapa


def upsert_ingredientes(cur, ingredientes):
    for ing in ingredientes:
        nombre = ing["nombre"]
        unidad_id_json = ing.get("unidad_id")

        row = cur.execute(
            "SELECT id FROM unidades WHERE id = ?;",
            (unidad_id_json,)
        ).fetchone()
        if not row:
            raise RuntimeError(f"No existe la unidad con id '{unidad_id_json}' para el ingrediente '{nombre}'")

        cur.execute(
            "INSERT OR IGNORE INTO ingredientes(nombre, unidad_id, activo) VALUES (?, ?, 1);",
            (nombre, unidad_id_json)
        )


def insert_recetas(cur, mapa_platos, recetas_maestro, recetas_ing):
    # Insertar recetas_maestro (cabecera) con mapa de platos
    mapa_maestro = {}

    for r in recetas_maestro:
        plato_id_json = r.get("plato_id")
        raciones_base = r.get("raciones_base", 1)

        if plato_id_json not in mapa_platos:
            raise RuntimeError(f"No existe mapeo de plato para plato_id JSON = {plato_id_json}")

        plato_id_sqlite = mapa_platos[plato_id_json]

        cur.execute(
            "INSERT INTO recetas_maestro(plato_id, raciones_base, fecha_creacion, activo) VALUES (?, ?, NULL, 1);",
            (plato_id_sqlite, raciones_base)
        )
        nuevo_id = cur.lastrowid
        mapa_maestro[r["id"]] = nuevo_id

    # Insertar detalle de ingredientes desde recetas_ingredientes.json
    for d in recetas_ing:
        receta_maestro_id_json = d.get("receta_maestro_id")
        ingrediente_id = d.get("ingrediente_id")
        cantidad = float(d.get("cantidad", 0))
        rol = d.get("rol") or d.get("uso") or "BASE"

        if receta_maestro_id_json not in mapa_maestro:
            continue

        cur.execute(
            """
            INSERT INTO recetas_ingredientes(receta_id, ingrediente_id, cantidad, rol)
            VALUES (?, ?, ?, ?);
            """,
            (mapa_maestro[receta_maestro_id_json], ingrediente_id, cantidad, rol)
        )


def main():
    conn = get_conn()
    cur = conn.cursor()

    # Cargar JSON reales
    platos = load_json(JSON_PLATOS)
    unidades = load_json(JSON_UNIDADES)
    ingredientes = load_json(JSON_INGREDIENTES)
    recetas_catalogo = load_json(JSON_RECETAS_CATALOGO)
    recetas_maestro = load_json(JSON_RECETAS_MAESTRO)
    recetas_ing = load_json(JSON_RECETAS_ING)

    # Tipos de plato desde platos
    ensure_tipos_from_platos(cur, platos)

    # Insertar catálogos
    upsert_unidades(cur, unidades)
    mapa_platos = upsert_platos(cur, platos)
    upsert_ingredientes(cur, ingredientes)

    # Insertar recetas
    insert_recetas(cur, mapa_platos, recetas_maestro, recetas_ing)

    conn.commit()
    conn.close()

    print("Migración completada correctamente.")


if __name__ == "__main__":
    main()
