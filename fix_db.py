import sqlite3
from pathlib import Path

db_path = Path("modulo_web") / "recetas.db"

print("Usando DB en:", db_path)

conn = sqlite3.connect(db_path)
cur = conn.cursor()

try:
    cur.execute("ALTER TABLE platos ADD COLUMN peso_racion REAL;")
    print("✅ Columna peso_racion agregada correctamente.")
except Exception as e:
    print("ℹ️ Aviso:", e)

conn.commit()
conn.close()

print("Listo.")