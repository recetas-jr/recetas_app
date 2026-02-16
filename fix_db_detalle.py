import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "modulo_web" / "recetas.db"

print("Usando DB en:", DB_PATH)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

try:
    cur.execute("""
        CREATE TABLE IF NOT EXISTS recetas_detalle (
            receta_id INTEGER PRIMARY KEY,
            preparacion TEXT,
            elaboracion TEXT,
            presentacion TEXT,
            nutricion TEXT,
            FOREIGN KEY (receta_id) REFERENCES recetas_maestro(id) ON DELETE CASCADE
        );
    """)
    print("✅ Tabla recetas_detalle creada (o ya existía).")
except Exception as e:
    print("❌ Error creando tabla recetas_detalle:", e)

conn.commit()
conn.close()

print("Listo.")