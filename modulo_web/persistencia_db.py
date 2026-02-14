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

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()