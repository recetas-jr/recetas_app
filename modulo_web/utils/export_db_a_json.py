import json
import sqlite3
import os
from datetime import datetime

# Raíz del proyecto (subimos dos niveles desde este archivo)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

DB_PATH = os.path.join(BASE_DIR, "data", "recetas.db")
EXPORT_DIR = os.path.join(BASE_DIR, "backups")

def exportar_sqlite_a_json():
    if not os.path.exists(EXPORT_DIR):
        os.makedirs(EXPORT_DIR)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(EXPORT_DIR, f"backup_sqlite_{timestamp}.json")

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    data = {}

    # Obtener todas las tablas reales de la DB
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tablas = [row["name"] for row in cur.fetchall()]

    for tabla in tablas:
        cur.execute(f"SELECT * FROM {tabla}")
        rows = cur.fetchall()
        data[tabla] = [dict(row) for row in rows]

    conn.close()

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return output_file

if __name__ == "__main__":
    archivo = exportar_sqlite_a_json()
    print(f"Backup generado en: {archivo}")